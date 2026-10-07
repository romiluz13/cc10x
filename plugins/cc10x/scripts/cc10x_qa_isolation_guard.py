#!/usr/bin/env python3
"""PreToolUse guard for the QA route.

Enforces four properties that prompt text alone cannot:

1. DENYLIST — a QA workflow may declare paths no agent is allowed to read.
   Prose in a brief is a request; this is a refusal. The refusal is ROOT-AWARE
   in both directions: a tool that names a quarantined path directly is denied,
   and so is a tool whose search ROOT contains a quarantined path — a Grep over
   the project root, or a Bash `grep -r` from an ancestor directory, reads the
   quarantined content as surely as a Read of the file itself. Glob patterns
   are matched directly only: whether one glob's results fall inside another
   glob's is not decidable here, and pretending otherwise would create
   allow-shaped exceptions in a deny rule.

2. PLAN-PHASE IS READ-ONLY — during qa / qa-research / qa-plan / qa-plan-review /
   qa-re-plan / qa-plan-review-2, no environment mutation. The planning phases
   exist to produce documents, not to provision anything.

   `qa-preflight` is DELIBERATELY EXCLUDED from PLAN_PHASES and is declared in
   PROVISIONING_PHASES instead. Preflight's entire job is to probe the real
   environment — bind a port, stat a credential, run `docker info` — so adding
   it here would block the phase from doing the only thing it exists to do,
   while looking like a strengthening of this guarantee. The two sets are
   asserted disjoint by scripts/test_cc10x_qa_phase_invariants.py.

   Note the bare parent value "qa" is a member. A workflow whose phase_cursor
   is left at "qa" is treated as a plan phase, so the router must set
   phase_cursor="qa-preflight" BEFORE dispatching preflight.

   The escape hatch is the workflow's `mutation_allowlist`, and it is matched
   against the paths a command WRITES — never against the raw command string,
   and never against the paths it merely READS. `cp` source operands are
   reads: the router's mandatory template copy
   (`cp ${CLAUDE_PLUGIN_ROOT}/templates/... .cc10x/qa/{id}/test-plan.md`)
   sources from outside the allowlist and must still be allowed, because its
   only write is the destination inside `.cc10x/`.

3. BASH COUNTS AS A WRITE — an agent declared "READ-ONLY" in its prompt while
   holding Bash is not read-only. Edit/Write matchers never see `cat > file`,
   `mkdir -p`, `rm -rf`, or `git init`. This inspects Bash commands too.

   The parser splits on NEWLINES first and tokenizes with
   `shlex.shlex(posix=True, punctuation_chars=True)`, so `;`, `&&`, `||` and
   `|` are their own tokens whether or not they are space-separated, and a
   newline separates commands exactly like `;` does. Wrapper commands
   (`sudo`, `env`, `bash -c`, `xargs`, ...) are recursed into, so
   `sudo rm -rf x` and `bash -c "mkdir y"` are classified by what they wrap.
   `find` with `-delete`/`-exec`/`-ok` is classified as the mutation it is.
   `>/dev/null` is exempt from the redirect rule: it creates no file, and
   `docker info >/dev/null` is the idiomatic capability probe step 0a depends
   on. Redirect targets are WRITE paths: an append into the workflow's own
   event log (`printf '%s\n' '{...}' >> .cc10x/workflows/{wf}.events.jsonl`)
   is the router's documented persistence mechanism and passes the same
   allowlist test every other write passes — nothing is exempt from the list,
   the list is just applied to the right operand.
   Residual gap, stated plainly: interpreted-code runners (`python -c`,
   `node -e`) are not classified by body inspection; the denylist and the
   audit trail are the layers behind this one.

4. A FINISHED WORKFLOW DISENGAGES THE GUARD — a QA workflow whose phase
   cursor is `memory-finalize`, or whose last `status_history` entry is a
   terminal event (`memory_finalized`, `workflow_completed`,
   `workflow_failed`), no longer denies anything. A workflow that stopped at
   the plan phase must not leave the repo locked against every later Write
   and Bash call for as long as its artifact is the newest on disk.

Config lives in the workflow artifact under `qa.isolation`:

    "qa": {
      "isolation": {
        "denied_reads": ["/abs/path/answer-sheet.md", "**/test/*.e2e-spec.ts"],
        "denied_read_reason": "quarantined for benchmark comparison",
        "plan_phase_readonly": true,
        "mutation_allowlist": [".cc10x/"]
      }
    }

Absent config, the plan-phase read-only rule still applies whenever the active
workflow is QA and its phase cursor is a planning phase. Fail open: if the
guard cannot determine the phase, it does not block (a guard that misfires on
unrelated work gets disabled, and a disabled guard protects nothing).

Relative paths — the allowlist's `.cc10x/`, a candidate `.cc10x/qa/x`, a
Grep root of `.` — are resolved against the PROJECT directory
(`CLAUDE_PROJECT_DIR`, falling back to the process cwd), never against
whatever directory the hook process happens to be running from. A guard that
resolved `.cc10x/` against its own cwd checked an allowlist that pointed at a
different repo than the one the tool was about to touch.
"""

from __future__ import annotations

import fnmatch
import os
import re
import shlex
from pathlib import Path

from cc10x_hooklib import (
    TERMINAL_EVENTS,
    latest_workflow_payload,
    load_input,
    log_event,
    pretool_deny,
    project_dir,
)

READ_TOOLS = {"Read", "Grep", "Glob"}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit"}

PLAN_PHASES = {
    "qa",
    "qa-research",
    "qa-plan",
    "qa-plan-review",
    "qa-re-plan",
    "qa-plan-review-2",
}

# Phases that legitimately mutate the environment. Declared so the read-only
# invariant is machine-checkable: PLAN_PHASES and PROVISIONING_PHASES must stay
# disjoint. This set is documentation for the test, not a control-flow input —
# the guard branches only on PLAN_PHASES, so a phase absent from both is simply
# unguarded, which is the pre-existing behaviour for every non-QA phase.
PROVISIONING_PHASES = {
    "qa-preflight",
    "qa-build",
    "qa-execute",
}

# Property 4: a workflow in one of these states is finished. The cursor value
# and the status_history event names are the router's vocabulary (SKILL.md §12
# step 3 and the workflow skeleton); this set must not invent its own.
TERMINAL_PHASES = {"memory-finalize"}

# Commands that mutate state outside the process, regardless of arguments.
# `rsync`/`scp` are unconditional copiers — their source/dest split is handled
# in `_bash_paths`, but the mutation itself must be detected here first.
MUTATING_COMMANDS = {
    "mkdir", "rm", "rmdir", "mv", "cp", "touch", "ln", "chmod", "chown",
    "truncate", "dd", "install", "tee", "make", "rsync", "scp",
}

# Wrappers that add nothing but privilege or environment around a real
# command: strip them and classify what they wrap. `timeout`'s duration
# argument is dropped with them; classifying `5` as a command is a no-op.
WRAPPER_COMMANDS = {"sudo", "env", "nice", "nohup", "stdbuf", "timeout", "xargs"}
# `bash -c "script"` / `sh -c "script"`: the wrapped script is the command.
SHELL_COMMANDS = {"bash", "sh", "zsh", "dash", "ksh"}

# Commands that walk a directory tree, so their path operands (or the cwd,
# when none are given) are READ ROOTS for the denylist. The grep family only
# when -r/-R is passed; the others are recursive by nature.
GREP_FAMILY = {"grep", "egrep", "fgrep"}
ALWAYS_RECURSIVE = {"find", "rg", "ag", "ack"}

# Shell operator tokens that separate one command from the next. Parentheses
# and `&` are included: `echo $(mkdir x)` and `mkdir x &` are two commands,
# and treating the grouping/background sigil as an ordinary word hides the
# second one from every rule below.
SEGMENT_OPERATORS = {"&&", "||", ";", "|", "|&", "(", ")", "&"}

# Redirection tokens as the punctuation-aware tokenizer emits them. `>&`
# followed by a bare digit (`2>&1`) is a duplication, not a file; followed by
# anything else it redirects to a file, as `&>` always does.
REDIRECT_TOKENS = {">", ">>", ">&", "&>"}

# Tools that both inspect and mutate. Anything NOT in the read-only set is
# treated as a mutation. Capability discovery (step 0a) depends on the
# read-only members staying allowed — `docker info` must not be blocked.
#
# THE RULE THAT GOVERNS THIS DICT: a subcommand belongs here only if EVERY
# invocation of it is read-only REGARDLESS OF FLAGS. The parser below discards
# flags deliberately (`if arg.startswith("-"): continue`), so a subcommand
# whose read/write character depends on its flags cannot be expressed here at
# all — `git config --get` reads and `git config user.email x` writes, and this
# dict sees the same token for both. Thirteen mutating invocations were allowed
# at plan phases because `branch`, `config`, `remote`, `tag` and `fmt` were
# entered wholesale; `terraform fmt` needed no flag at all to rewrite files.
# The cost of the rule is that the read-only halves go with them: prefer the
# workflow's `mutation_allowlist` to re-widening this set.
# OX Agent: least-privilege command classification prevented flag-blind fail-open
SUBCOMMAND_TOOLS: dict[str, set[str]] = {
    "docker": {"info", "ps", "images", "version", "inspect", "logs", "port", "top", "stats", "diff", "history"},
    "docker-compose": {"config", "ps", "logs", "images", "version", "top"},
    "podman": {"info", "ps", "images", "version", "inspect", "logs"},
    "kubectl": {"get", "describe", "logs", "explain", "version", "api-resources", "top", "cluster-info"},
    "helm": {"list", "status", "get", "show", "version", "search", "template", "lint"},
    "terraform": {"show", "output", "validate", "version", "providers", "graph"},
    "npm": {"ls", "list", "view", "info", "outdated", "why", "ping", "version", "root", "prefix", "search"},
    "pnpm": {"ls", "list", "view", "info", "outdated", "why", "root"},
    "yarn": {"list", "info", "why", "versions"},
    "pip": {"list", "show", "freeze", "check", "index"},
    "pip3": {"list", "show", "freeze", "check", "index"},
    "git": {
        "log", "show", "status", "diff", "rev-parse", "rev-list", "ls-files",
        "ls-remote", "cat-file", "describe", "blame", "shortlog",
        "merge-base", "grep", "count-objects", "for-each-ref", "symbolic-ref",
    },
}

# Redirections that create or append to a file. Used only as the FALLBACK when
# the tokenizer cannot parse the command (unbalanced quotes): the primary
# redirect detection is token-based, which is what catches `2>file` — a
# file-creating redirect the digit lookbehind here deliberately excludes
# because `2>&1` must not match.
REDIRECT_RE = re.compile(r"(?<![0-9<>])>{1,2}(?!&)")


def _norm(path: str) -> str:
    """Resolve `path` against the PROJECT directory, not the process cwd.

    The hook process can be started from anywhere; `.cc10x/` in an allowlist
    and `.cc10x/qa/x` in a command must resolve to the same tree or the
    comparison is between two different repos.
    """
    p = Path(os.path.expanduser(path))
    if not p.is_absolute():
        p = project_dir() / p
    return str(p.resolve())


def _matches(path: str, patterns: list[str]) -> str | None:
    """Return the pattern that matched, or None."""
    resolved = _norm(path)
    for pat in patterns:
        expanded = os.path.expanduser(pat)
        if fnmatch.fnmatch(resolved, expanded) or fnmatch.fnmatch(path, expanded):
            return pat
        # Bare path: match it and anything beneath it.
        if "*" not in expanded and "?" not in expanded:
            try:
                target = _norm(expanded)
            except OSError:
                continue
            if resolved == target or resolved.startswith(target.rstrip("/") + "/"):
                return pat
    return None


def _covers(root: str, patterns: list[str]) -> str | None:
    """Return the BARE denied pattern that lies INSIDE `root`, or None.

    `_matches` catches a tool that names the quarantined path itself; this
    catches the other direction — a search ROOT that contains one. `Grep` over
    the project root, or a Bash `grep -r` from an ancestor directory, reads
    every file beneath it, quarantined or not. Glob patterns are skipped:
    containment is only decidable for bare paths.
    """
    try:
        root_n = _norm(root).rstrip("/") + "/"
    except OSError:
        return None
    for pat in patterns:
        expanded = os.path.expanduser(pat)
        if "*" in expanded or "?" in expanded:
            continue
        try:
            target = _norm(expanded)
        except OSError:
            continue
        if target != root_n.rstrip("/") and target.startswith(root_n):
            return pat
    return None


def _tokenize(command: str) -> list[list[str]]:
    """One token list per LINE of the command, operators as their own tokens.

    `shlex` with `punctuation_chars=True` makes `;`, `&&`, `|`, `>` … separate
    tokens whether or not they are space-separated, so `echo hi;mkdir x` and
    `echo hi && mkdir x` reach the classifier as the same two commands. A
    newline is a command separator too, which plain `shlex.split` collapses
    into whitespace — splitting the lines FIRST is what keeps `echo hi\nmkdir
    x` from parsing as one long `echo`. Unparseable lines (unbalanced quotes)
    degrade to whitespace splitting rather than to an allow.
    """
    out: list[list[str]] = []
    for line in command.splitlines():
        if not line.strip():
            continue
        try:
            lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
            lexer.whitespace_split = True
            out.append(list(lexer))
        except ValueError:
            out.append(line.split())
    return out


def _segments(tokens: list[str]) -> list[list[str]]:
    """Split a token list on shell operators into command segments."""
    segment: list[str] = []
    segments = [segment]
    for tok in tokens:
        if tok in SEGMENT_OPERATORS:
            segment = []
            segments.append(segment)
        else:
            segment.append(tok)
    return [s for s in segments if s]


def _argv(seg: list[str]) -> tuple[str, list[str]]:
    """(argv0, rest) with leading FOO=bar assignments skipped."""
    idx = 0
    while idx < len(seg) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[idx]):
        idx += 1
    if idx >= len(seg):
        return "", []
    return Path(seg[idx]).name, seg[idx + 1:]


def _segment_mutates(seg: list[str]) -> str | None:
    """Classify one command segment; wrappers are recursed into."""
    argv0, rest = _argv(seg)
    if not argv0:
        return None

    if argv0 in SHELL_COMMANDS:
        # bash -c "inner script": the wrapped script is the command.
        if "-c" in rest:
            inner = " ".join(a for a in rest if a != "-c")
            return _bash_mutates(inner)
        return None

    if argv0 == "xargs":
        # xargs rm -rf x: classify by what it wraps, flags dropped.
        return _segment_mutates([a for a in rest if not a.startswith("-")])

    if argv0 in WRAPPER_COMMANDS:
        # sudo/env/nohup ...: strip the wrapper (and its KEY=v assignments,
        # handled by _argv on the next pass) and classify the real command.
        return _segment_mutates(rest)

    if argv0 == "sed":
        if any(a.startswith("-i") for a in rest):
            return "sed -i edits in place"
        return None

    if argv0 == "find":
        # find needs no command name to mutate: -delete removes, -exec/-ok
        # run an arbitrary command per hit.
        if any(
            a in {"-delete", "-exec", "-execdir", "-ok", "-okdir"}
            or a.startswith(("-delete", "-exec", "-execdir", "-ok", "-okdir"))
            for a in rest
        ):
            return "`find -delete`/`-exec` mutates state"
        return None

    if argv0 in SUBCOMMAND_TOOLS:
        # First non-flag argument is the subcommand. `git -C path log` → log.
        sub = ""
        skip_next = False
        for arg in rest:
            if skip_next:
                skip_next = False
                continue
            if arg in {"-C", "-c", "--git-dir", "--work-tree", "--context", "-n", "--namespace"}:
                skip_next = True
                continue
            if arg.startswith("-"):
                continue
            sub = arg
            break
        if sub and sub not in SUBCOMMAND_TOOLS[argv0]:
            return f"`{argv0} {sub}` mutates state"
        return None

    if argv0 in MUTATING_COMMANDS:
        return f"`{argv0}` mutates state"
    return None


def _redirect_targets(tokens: list[str]) -> list[str]:
    """File operands of `>`, `>>`, `>&`, `&>` — the files a command creates or
    appends to. `>/dev/null` and `>&1`-style duplications create nothing."""
    out: list[str] = []
    for i, tok in enumerate(tokens):
        if tok in REDIRECT_TOKENS and i + 1 < len(tokens):
            target = tokens[i + 1]
            if target in {"/dev/null", "1", "2"}:
                continue
            out.append(target)
    return out


def _bash_mutates(command: str) -> str | None:
    """Return a reason string if this Bash command mutates state, else None."""
    for line in command.splitlines():
        if not line.strip():
            continue
        try:
            lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            # Unbalanced quotes: the line cannot be tokenized, so redirect
            # detection falls back to the raw regex with /dev/null forms
            # blanked first. Failing OPEN on an unparseable line would make
            # `mkdir x'` — one stray quote — the cheapest bypass in the file.
            stripped = re.sub(r"(?:\d+)?&?>>?\s*/dev/null\b", " ", line)
            if REDIRECT_RE.search(stripped):
                return "shell redirection creates or appends to a file"
            tokens = line.split()
        # A redirect to a real file is a mutation even inside an otherwise
        # read-only command. `>/dev/null` and `>&1`-style duplications create
        # nothing and are skipped per-token in _redirect_targets. The token
        # path also catches `2>file`, which the digit-lookbehind regex cannot
        # express without also matching `2>&1`.
        if _redirect_targets(tokens):
            return "shell redirection creates or appends to a file"
        for seg in _segments(tokens):
            reason = _segment_mutates(seg)
            if reason:
                return reason
    return None


def _is_pathish(tok: str) -> bool:
    if tok.startswith("-") or tok in {"/dev/null"}:
        return False
    if tok.startswith("{"):
        # A quoted JSON payload (`printf '%s\n' '{"ts":...}'`) is data, not a
        # path, whatever its contents name.
        return False
    if "=" in tok.split("/")[0] and "/" not in tok:
        return False
    return (
        "/" in tok
        or tok.startswith("~")
        or tok.endswith((".md", ".json", ".ts", ".py"))
    )


def _bash_paths(command: str, *, writes_only: bool = False) -> list[str]:
    """Path-like tokens from a shell command.

    `writes_only` drops the READ operands of the copy/move family: `cp src
    dst` reads `src` and writes `dst`, so the plan-phase allowlist — a list of
    writable places — must be matched against `dst` alone. The denylist
    branch uses the full set: a `cp` whose SOURCE is quarantined is as much a
    read of the quarantine as a `cat` of it. Redirect targets are writes and
    are collected on both passes.
    """
    out: list[str] = []
    for tokens in _tokenize(command):
        out.extend(_redirect_targets(tokens))
        for seg in _segments(tokens):
            argv0, rest = _argv(seg)
            operands = [
                a for a in ([argv0] + rest) if _is_pathish(a)
            ]
            if writes_only and argv0 in {"cp", "mv", "ln", "install", "rsync", "scp"}:
                # Every non-flag operand but the LAST is a read (cp src... dst);
                # only the destination is matched against the writable list.
                operands = operands[-1:]
            out.extend(operands)
    return out


def _bash_read_roots(command: str) -> list[str]:
    """Directories a recursive reader will walk, `.` for the cwd when it names
    none. These are ROOTS for the denylist: a tree walk that starts at or
    above a quarantined path reads it."""
    roots: list[str] = []
    for tokens in _tokenize(command):
        for seg in _segments(tokens):
            argv0, rest = _argv(seg)
            recursive = argv0 in ALWAYS_RECURSIVE or (
                argv0 in GREP_FAMILY
                and any(
                    a in {"-r", "-R"} or a.startswith(("--recursive", "-r", "-R"))
                    for a in rest
                )
            )
            if not recursive:
                continue
            operands = [a for a in rest if not a.startswith("-")]
            roots.extend(operands or ["."])
    return roots


def main() -> int:
    data = load_input()
    tool_name = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}

    workflow = latest_workflow_payload()
    if (workflow.get("workflow_type") or "").upper() != "QA":
        return 0

    # The same fail-open logic as status_history below applies to the config
    # block itself: `qa` and `isolation` are attacker-adjacent state read off
    # disk, and a non-dict where a dict is expected must degrade to "no
    # config", never to a traceback. A PreToolUse hook that raises exits
    # non-zero with no decision on stdout, which fails OPEN.
    # OX Agent: Improper Input Validation prevented
    qa = workflow.get("qa")
    qa = qa if isinstance(qa, dict) else {}
    isolation = qa.get("isolation")
    isolation = isolation if isinstance(isolation, dict) else {}
    denied_reads = isolation.get("denied_reads") or []
    if not isinstance(denied_reads, list):
        denied_reads = []
    denied_reads = [d for d in denied_reads if isinstance(d, str)]
    deny_reason = isolation.get("denied_read_reason") or "declared off-limits for this workflow"
    plan_readonly = isolation.get("plan_phase_readonly", True)
    allowlist = isolation.get("mutation_allowlist") or [".cc10x/"]
    if not isinstance(allowlist, list) or not all(isinstance(a, str) for a in allowlist):
        allowlist = [".cc10x/"]

    # A PreToolUse hook that raises exits non-zero with no decision on stdout,
    # which fails OPEN -- the guard silently stops guarding. status_history is
    # attacker-adjacent state read off disk, so every shape is narrowed before
    # it is indexed: `isinstance(history, list)` absorbs null, a bare scalar and
    # an object; `history and` absorbs `[]`; the inner isinstance absorbs a list
    # whose last entry is not a dict.
    # OX Agent: Improper Input Validation prevented
    history = workflow.get("status_history")
    history = history if isinstance(history, list) else []
    prev_phase = history[-1].get("phase") if history and isinstance(history[-1], dict) else ""
    phase = (workflow.get("phase_cursor") or prev_phase or "")
    wf_id = workflow.get("workflow_uuid") or workflow.get("workflow_id")

    # ---- 0. A finished workflow disengages the guard entirely ---------------
    # Property 4 in the module docstring, checked BEFORE the denylist: a
    # quarantine belongs to a live workflow, and a completed one must not
    # leave it behind as a standing repo-wide lock. The phase-cursor form
    # covers a workflow that finalised its memory and moved on; the
    # status_history form covers one that was closed or abandoned with the
    # cursor left where it last was.
    if phase in TERMINAL_PHASES:
        return 0
    if history and isinstance(history[-1], dict):
        last_event = history[-1].get("event")
        if isinstance(last_event, str) and last_event in TERMINAL_EVENTS:
            return 0

    def _log(decision: str, reason: str, target: str) -> None:
        log_event(
            "qa_isolation_guard",
            {
                "wf": wf_id,
                "phase": phase,
                "task_id": None,
                "agent": "qa",
                "tool_name": tool_name,
                "path": target,
                "event": "qa_isolation_guard",
                "decision": decision,
                "reason": reason,
            },
        )

    # ---- 1. Denylist: no agent reads a quarantined path ----------------------
    if denied_reads:
        candidates: list[str] = []
        read_roots: list[str] = []
        if tool_name in READ_TOOLS:
            # `notebook_path` is the key the Notebook tools pass; every other
            # read tool passes file_path/path/pattern. Omitting it collected no
            # candidates for NotebookRead, so the loop below never ran and a
            # quarantined notebook was ALLOWED. The new key is appended to the
            # same candidate list and is matched by the same `_matches`, so it
            # inherits the resolve-and-compare semantics rather than bypassing
            # them.
            # OX Agent: Improper Access Control prevented
            for key in ("file_path", "path", "pattern", "notebook_path"):
                val = tool_input.get(key)
                if isinstance(val, str):
                    candidates.append(val)
            # A search ROOT that contains a quarantined path reads it. Grep
            # and Glob search the whole project when no path is passed, so
            # the absent root is the project root, not "no root".
            if tool_name in ("Grep", "Glob"):
                root = tool_input.get("path")
                read_roots.append(root if isinstance(root, str) and root else ".")
        elif tool_name == "Bash":
            command = tool_input.get("command") or ""
            candidates.extend(_bash_paths(command))
            read_roots.extend(_bash_read_roots(command))

        for cand in candidates:
            hit = _matches(cand, denied_reads)
            if hit:
                _log("deny", f"denied_read:{hit}", cand)
                pretool_deny(
                    f"CC10X QA isolation: `{cand}` is on this workflow's read denylist "
                    f"(matched `{hit}` — {deny_reason}).\n\n"
                    "This is not advisory. Reading it invalidates the workflow's premise. "
                    "Proceed using only allowed sources, and record the limitation in "
                    "GAPS rather than working around this guard."
                )
                return 0
        for root in read_roots:
            hit = _covers(root, denied_reads)
            if hit:
                _log("deny", f"denied_read_root:{hit}", root)
                pretool_deny(
                    f"CC10X QA isolation: the search root `{root}` contains `{hit}`, "
                    f"which is on this workflow's read denylist ({deny_reason}).\n\n"
                    "A tree search reads quarantined content as surely as opening it. "
                    "Scope the search to exclude the denied path, and record the "
                    "limitation in GAPS rather than working around this guard."
                )
                return 0

    # ---- 2 & 3. Plan phase performs no environment mutation ------------------
    if plan_readonly and phase in PLAN_PHASES:
        target = None
        reason = None

        if tool_name in WRITE_TOOLS:
            # Same missing key, opposite defect. NotebookEdit passes
            # `notebook_path`, so `target` was always "" and the allowlist
            # escape below (`if target and ...`) was unreachable: a notebook
            # write INTO the allowlist was wrongly denied. The fallback chain
            # ends in `or ""` and NOT in an unconditional allow -- a notebook
            # path outside the allowlist still reaches `_matches` and is still
            # denied.
            # OX Agent: Improper Access Control prevented
            target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
            reason = f"{tool_name} writes a file"
        elif tool_name == "Bash":
            command = tool_input.get("command") or ""
            mutation = _bash_mutates(command)
            if mutation:
                target = command[:200]
                reason = mutation

        if reason:
            # Writing the workflow's own artifacts is the point of the phase.
            if target and tool_name in WRITE_TOOLS and _matches(target, allowlist):
                return 0
            # The allowlist names PATHS, so it is matched against the paths
            # the command WRITES -- not against the raw command string, and
            # not against its READ operands. A substring test read
            # `rm -rf /etc/x # .cc10x` as allowed: seven characters inside a
            # shell comment that `_bash_mutates` had already stripped before
            # deciding the command mutates. The copy/move family's SOURCE
            # operands are dropped (`writes_only`) because the router's own
            # mandatory template copy sources from the plugin root, outside
            # every project allowlist, while writing only into `.cc10x/`.
            # Redirect targets are collected as writes, so the event-log
            # append passes the same test every other `.cc10x/` write passes.
            # `paths and` first, because `all([])` is True and would wave
            # through every command no path could be extracted from; `all`
            # rather than `any`, because a command touching one allowed path
            # and one forbidden path is a forbidden command.
            # OX Agent: Path Traversal prevented
            if tool_name == "Bash":
                paths = _bash_paths(tool_input.get("command") or "", writes_only=True)
                if paths and all(_matches(p, allowlist) for p in paths):
                    return 0

            _log("deny", f"plan_phase_mutation:{reason}", str(target))
            pretool_deny(
                f"CC10X QA isolation: the `{phase}` phase does not mutate the environment "
                f"({reason}).\n\n"
                "Planning phases produce documents. Provisioning, installing fixtures, "
                "creating workspaces, and running setup belong to `qa-build` and "
                "`qa-execute`, after the plan is reviewed and approved.\n\n"
                "Write what the environment SHOULD be into env-plan.md. Do not build it."
            )
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
