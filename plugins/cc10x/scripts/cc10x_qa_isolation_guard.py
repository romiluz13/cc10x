#!/usr/bin/env python3
"""PreToolUse guard for the QA route.

Enforces three properties that prompt text alone cannot:

1. DENYLIST — a QA workflow may declare paths no agent is allowed to read.
   Prose in a brief is a request; this is a refusal.

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

3. BASH COUNTS AS A WRITE — an agent declared "READ-ONLY" in its prompt while
   holding Bash is not read-only. Edit/Write matchers never see `cat > file`,
   `mkdir -p`, `rm -rf`, or `git init`. This inspects Bash commands too.

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
workflow is QA and its phase cursor is a planning phase. Fail closed: if the
guard cannot determine the phase, it does not block (a guard that misfires on
unrelated work gets disabled, and a disabled guard protects nothing).
"""

from __future__ import annotations

import fnmatch
import os
import re
import shlex
from pathlib import Path

from cc10x_hooklib import (
    latest_workflow_payload,
    load_input,
    load_mode,
    log_event,
    pretool_deny,
)

READ_TOOLS = {"Read", "Grep", "Glob", "NotebookRead"}
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

# Commands that mutate state outside the process, regardless of arguments.
MUTATING_COMMANDS = {
    "mkdir", "rm", "rmdir", "mv", "cp", "touch", "ln", "chmod", "chown",
    "truncate", "dd", "install", "tee", "make",
}

# Tools that both inspect and mutate. Anything NOT in the read-only set is
# treated as a mutation. Capability discovery (step 0a) depends on the
# read-only members staying allowed — `docker info` must not be blocked.
SUBCOMMAND_TOOLS: dict[str, set[str]] = {
    "docker": {"info", "ps", "images", "version", "inspect", "logs", "port", "top", "stats", "diff", "history"},
    "docker-compose": {"config", "ps", "logs", "images", "version", "top"},
    "podman": {"info", "ps", "images", "version", "inspect", "logs"},
    "kubectl": {"get", "describe", "logs", "explain", "version", "api-resources", "config", "top", "cluster-info"},
    "helm": {"list", "status", "get", "show", "version", "search", "template", "lint"},
    "terraform": {"show", "output", "validate", "version", "providers", "graph", "fmt"},
    "npm": {"ls", "list", "view", "info", "config", "outdated", "why", "ping", "version", "root", "prefix", "search"},
    "pnpm": {"ls", "list", "view", "info", "config", "outdated", "why", "root"},
    "yarn": {"list", "info", "config", "why", "versions"},
    "pip": {"list", "show", "freeze", "check", "config", "index"},
    "pip3": {"list", "show", "freeze", "check", "config", "index"},
    "git": {
        "log", "show", "status", "diff", "rev-parse", "rev-list", "branch", "ls-files",
        "ls-remote", "cat-file", "describe", "blame", "shortlog", "config", "remote",
        "tag", "merge-base", "grep", "count-objects", "for-each-ref", "symbolic-ref",
    },
}

# Redirections that create or append to a file.
REDIRECT_RE = re.compile(r"(?<![0-9<>])>{1,2}(?!&)")


def _norm(path: str) -> str:
    return str(Path(os.path.expanduser(path)).resolve())


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
                target = str(Path(expanded).resolve())
            except OSError:
                continue
            if resolved == target or resolved.startswith(target.rstrip("/") + "/"):
                return pat
    return None


def _bash_paths(command: str) -> list[str]:
    """Best-effort extraction of path-like tokens from a shell command."""
    try:
        tokens = shlex.split(command, comments=True)
    except ValueError:
        tokens = command.split()
    out = []
    for tok in tokens:
        if tok.startswith("-") or "=" in tok.split("/")[0] and "/" not in tok:
            continue
        if "/" in tok or tok.startswith("~") or tok.endswith((".md", ".json", ".ts", ".py")):
            out.append(tok)
    return out


def _bash_mutates(command: str) -> str | None:
    """Return a reason string if this Bash command mutates state, else None."""
    if REDIRECT_RE.search(command):
        return "shell redirection creates or appends to a file"

    try:
        tokens = shlex.split(command, comments=True)
    except ValueError:
        tokens = command.split()

    # Walk segments split on shell operators so `a && mkdir b` is caught.
    segment: list[str] = []
    segments = [segment]
    for tok in tokens:
        if tok in {"&&", "||", ";", "|"}:
            segment = []
            segments.append(segment)
        else:
            segment.append(tok)

    for seg in segments:
        if not seg:
            continue
        # Skip leading env assignments (FOO=bar cmd).
        idx = 0
        while idx < len(seg) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[idx]):
            idx += 1
        if idx >= len(seg):
            continue
        argv0 = Path(seg[idx]).name
        rest = seg[idx + 1:]

        if argv0 == "sed":
            if any(a.startswith("-i") for a in rest):
                return "sed -i edits in place"
            continue

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
            continue

        if argv0 in MUTATING_COMMANDS:
            return f"`{argv0}` mutates state"
    return None


def main() -> int:
    data = load_input()
    tool_name = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}

    workflow = latest_workflow_payload()
    if (workflow.get("workflow_type") or "").upper() != "QA":
        return 0

    qa = workflow.get("qa") or {}
    isolation = qa.get("isolation") or {}
    denied_reads = isolation.get("denied_reads") or []
    deny_reason = isolation.get("denied_read_reason") or "declared off-limits for this workflow"
    plan_readonly = isolation.get("plan_phase_readonly", True)
    allowlist = isolation.get("mutation_allowlist") or [".cc10x/", "/tmp/cc10x-"]

    phase = (workflow.get("phase_cursor") or workflow.get("status_history", [{}])[-1].get("phase") or "")
    wf_id = workflow.get("workflow_uuid") or workflow.get("workflow_id")

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
        if tool_name in READ_TOOLS:
            for key in ("file_path", "path", "pattern"):
                val = tool_input.get(key)
                if isinstance(val, str):
                    candidates.append(val)
        elif tool_name == "Bash":
            candidates.extend(_bash_paths(tool_input.get("command") or ""))

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

    # ---- 2 & 3. Plan phase performs no environment mutation ------------------
    if plan_readonly and phase in PLAN_PHASES:
        target = None
        reason = None

        if tool_name in WRITE_TOOLS:
            target = tool_input.get("file_path") or ""
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
            if tool_name == "Bash" and any(
                a.strip("/") in (tool_input.get("command") or "") for a in allowlist
            ):
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
