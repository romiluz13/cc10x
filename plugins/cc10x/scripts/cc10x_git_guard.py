#!/usr/bin/env python3
"""Git guardrails — blocks dangerous git commands that can destroy work.

PreToolUse hook for Bash commands. Blocks:
- git push (to remote — local commits are safe), force forms included
- git reset --hard
- git clean -f / git clean --force
- git branch -D / git branch --delete --force (force delete)
- git checkout . / -- . / -f, git switch -f, git restore . (discard all changes;
  `.`, `./.`, `:/` and `:(top)` all name the whole tree)
- git worktree remove --force
- git stash clear

`classify_git_command` is the pure decision. By construction it denies at
least everything the legacy regex list (BLOCKED_PATTERNS) denies on the RAW
command text, and adds denials for wrapped and chained commands (env/sudo/
xargs/..., `git -C`, `git -c alias.x=`, `bash -c`, `eval`, `$(...)`,
backticks, newlines, shell comments). The one exception is a strict,
default-deny allowance for read-only quoted data (`_quoted_data_only`): the
whole command must be a single `echo|printf|grep` pipeline into plain text
filters with no shell operator outside quotes. Anything else gets the floor
over the entire raw command plus the extra scan. It is a text heuristic, not
a shell parser: a model can still build a command the text does not show
(variables, scripts written then run, `git config alias`).

Approval token (single-use unlock for router-sanctioned finishing flows):
`git push` and `git branch -D` — and ONLY those two — can be unlocked by a
fresh token at .cc10x/state/git-approval.json written by the router
immediately after the user's explicit BUILD-DONE finishing choice:

    {"wf": "wf-...", "operations": ["push"], "expires_at": "<UTC ISO>"}

The token is consumed (deleted) on first matching allow, and ignored when
expired (or older than MAX_TOKEN_AGE_SECONDS as a backstop). Destructive
history/worktree operations (reset --hard, clean -f, checkout ., force-push)
have NO token path and stay blocked unconditionally. The token is a plain
file: a model that can write files can write one itself; that limitation is
documented, not defended.
"""

from __future__ import annotations

import contextlib
import fnmatch
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

from cc10x_hooklib import load_input, log_event, pretool_deny, state_root

MAX_TOKEN_AGE_SECONDS = 600  # backstop even if expires_at is missing/garbled

# (pattern, reason, approvable-operation-or-None)
BLOCKED_PATTERNS = [
    (
        r"\bgit\s+push\b.*(--force\b|-f\b|--force-with-lease\b)",
        "git push --force — force-pushing rewrites remote history.",
        None,  # force-push is never token-approvable
    ),
    (
        r"\bgit\s+push\b",
        "git push — pushing to remote. Use a branch and PR instead.",
        "push",
    ),
    (
        r"\bgit\s+reset\s+--hard\b",
        "git reset --hard — destroys uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+clean\s+-[a-z]*f[a-z]*\b",
        "git clean -f — removes untracked files permanently.",
        None,
    ),
    (
        r"\bgit\s+branch\s+-D\b",
        "git branch -D — force-deletes a branch.",
        "branch-delete",
    ),
    (
        r"\bgit\s+checkout\s+\.\s*$",
        "git checkout . — discards all uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+checkout\s+--\s+\.\s*$",
        "git checkout -- . — discards all uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+checkout\s+\*\s*$",
        "git checkout * — discards all uncommitted changes.",
        None,
    ),
    (
        r"\bgit\s+restore\s+\.\s*$",
        "git restore . — discards all uncommitted changes (same as checkout .).",
        None,
    ),
]


def _log_token(event: str, reason: str, **extra: str) -> None:
    log_event(
        f"plugin_{event}",
        {
            "wf": None,
            "phase": "build-finish",
            "task_id": None,
            "agent": "router",
            "event": event,
            "decision": "deny",
            "reason": reason,
            **extra,
        },
    )


def approval_token_path() -> Path:
    return state_root() / "state" / "git-approval.json"


def consume_approval(operation: str) -> str | None:
    """Return the approving wf id if a fresh token covers `operation`.

    The token is single-use: it is deleted whether or not it matched, as long
    as it was parsed — a stale or mismatched token must not linger and approve
    a later, different command.
    """
    path = approval_token_path()
    if not path.exists():
        return None
    try:
        token = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        token = None
    if not isinstance(token, dict):
        # Truncated, corrupt or valid JSON that is not an object: no token.
        with contextlib.suppress(OSError):
            path.unlink()
        _log_token("git_guard_token_invalid", "unparseable-or-not-an-object")
        return None

    now = datetime.now(timezone.utc)
    fresh = False
    expires_at = token.get("expires_at")
    if isinstance(expires_at, str):
        try:
            expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            fresh = now <= expiry
        except ValueError:
            fresh = False
    # backstop: even a "fresh" token older than MAX_TOKEN_AGE_SECONDS is stale
    try:
        age = now.timestamp() - path.stat().st_mtime
        if age > MAX_TOKEN_AGE_SECONDS:
            fresh = False
    except OSError:
        fresh = False

    operations = token.get("operations")
    matched = fresh and isinstance(operations, list) and operation in operations

    with contextlib.suppress(OSError):
        path.unlink()  # single-use, consumed regardless of match

    if matched:
        return token.get("wf") or "unknown"
    return None


def command_segments(command: str) -> list[str]:
    """Split a shell command into the simple commands the patterns expect.

    Multi-line scripts, `&&`/`||` chains, `;` sequences, and pipelines each
    hide a git invocation from end-anchored patterns; match per segment.
    """
    parts = re.split(r"\n|;|\|\||&&|\|", command)
    return [part.strip() for part in parts if part.strip()]


GIT_GLOBAL_FLAGS = (
    r"\bgit\s+((-C\s+\S+|-c\s+\S+|--git-dir(=|\s+)\S+|--work-tree(=|\s+)\S+"
    r"|-P|--no-pager|--paginate)\s+)+"
)


def normalize_segment(segment: str) -> str:
    """Collapse git's global flags so `git -C dir <op>` matches `git <op>`,
    and strip trailing shell comments so `git restore . # tidy` still hits
    the end-anchored discard patterns. (Heuristic: ` #` outside quotes is
    rare in legitimate git arguments; erring toward deny is the safe side.)

    Linear on purpose: substituting a whitespace-run-then-hash pattern
    backtracks quadratically on long runs of spaces and outlasts the hook
    timeout."""
    comment = re.search(r"\s#", segment)
    if comment:
        segment = segment[: comment.start()].rstrip()
    return re.sub(GIT_GLOBAL_FLAGS, "git ", segment)


# Reason key per BLOCKED_PATTERNS entry (same order). Approvable keys name the
# approval-token operation.
FLOOR_KEYS = (
    "push-force",
    "push",
    "reset-hard",
    "clean-force",
    "branch-delete",
    "discard-all",
    "discard-all",
    "discard-all",
    "discard-all",
)
APPROVABLE = {"push": "push", "branch-delete": "branch-delete"}
# Non-approvable reasons win over approvable ones in a mixed command, so a
# token for `push` can never unlock `push && reset --hard`.
PRIORITY = (
    "push-force",
    "reset-hard",
    "clean-force",
    "discard-all",
    "checkout-force",
    "worktree-force",
    "stash-clear",
    "classifier-error",
    "command-too-large",
    "push",
    "branch-delete",
)

MSG_PUSH_FORCE = BLOCKED_PATTERNS[0][1]
MSG_PUSH = BLOCKED_PATTERNS[1][1]
MSG_RESET = BLOCKED_PATTERNS[2][1]
MSG_CLEAN = BLOCKED_PATTERNS[3][1]
MSG_BRANCH = BLOCKED_PATTERNS[4][1]
MSG_CHECKOUT = BLOCKED_PATTERNS[5][1]
MSG_RESTORE = BLOCKED_PATTERNS[8][1]
MSG_CHECKOUT_FORCE = "git checkout -f — discards uncommitted changes."
MSG_SWITCH_FORCE = "git switch --force — discards uncommitted changes."
MSG_WORKTREE_FORCE = "git worktree remove --force — deletes a worktree with uncommitted changes."
MSG_STASH_CLEAR = "git stash clear — permanently discards every stash."
MSG_CLASSIFIER_ERROR = (
    "the git guard classifier failed on this command, so it cannot be cleared."
)
MSG_DEPTH = (
    "the command nests deeper than the git guard reads (depth cap), so it "
    "cannot be cleared."
)

MSG_TOO_LARGE = (
    "the command is too large for the git guard to read in time, so it cannot "
    "be cleared."
)
MSG_OPAQUE_GIT = (
    "the git command or subcommand word is built by a brace, glob or "
    "substitution the guard cannot resolve, so it cannot be cleared."
)

SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
# Their quoted arguments are scanned as text that a consumer might execute.
DATA_COMMANDS = {"echo", "printf", "grep", "egrep", "fgrep"}
# The only members the quoted-data allowance accepts behind its data command:
# none of them writes a file or runs what it reads (sort and uniq can write).
TEXT_FILTERS = {"grep", "egrep", "fgrep", "cat", "head", "tail", "wc", "tr", "cut"}
ALLOWANCE_FORBIDDEN_CHARS = set("#\\\r$`(){};&<>\n")
ALLOWANCE_FORBIDDEN_WORDS = {
    "exec", "eval", "source", ".", "function", "for", "while", "until", "if",
    "case", "do", "done", "then", "fi",
}
# Zero-argument prefixes that only continue into the real command.
KEYWORDS = {
    "if", "then", "else", "elif", "do", "while", "until", "!", "{", "}",
    "time", "exec", "builtin", "command", "nohup",
}
# Wrapper -> option flags that consume the following word.
WRAPPERS = {
    "env": {"-u", "-C"},
    "sudo": {"-u", "-g", "-h", "-p", "-C", "-D", "-R", "-T", "-U", "-r", "-t"},
    "nice": {"-n"},
    "timeout": {"-s", "-k"},
    "stdbuf": set(),
    "xargs": {"-I", "-n", "-P", "-L", "-d", "-E", "-s", "-a", "-J"},
}
GIT_VALUE_FLAGS = {
    "-C", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env",
    "--attr-source",
}
GIT_DESTRUCTIVE_SUBS = (
    "push", "reset", "clean", "branch", "checkout", "restore", "stash", "switch", "worktree",
)
BRACE_EXPANSION = re.compile(r"(?<!\$)\{[^{}]*(,|\.\.)[^{}]*\}")
MAX_COMMAND_CHARS = 65536
GROUP_OPS = {"&&", "||", ";", ";;", "&", "(", ")", "\n"}
MAX_DEPTH = 8
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
GIT_WORD = re.compile(r"\bgit\b", re.IGNORECASE)


class _Tok(NamedTuple):
    text: str
    quoted: bool = False
    op: bool = False
    subst: tuple[str, ...] = ()


def _skip_quote(text: str, start: int) -> int:
    """Index after the quoted region opening at `start`, or -1 if unterminated."""
    quote = text[start]
    i = start + 1
    while i < len(text):
        if quote == '"' and text[i] == "\\":
            i += 2
        elif text[i] == quote:
            return i + 1
        else:
            i += 1
    return -1


def _capture_paren(text: str, start: int) -> tuple[str, int] | None:
    """Body of a `$(` that opened just before `start`, and the index after `)`."""
    depth = 1
    i = start
    while i < len(text):
        char = text[i]
        if char == "\\":
            i += 2
            continue
        if char in "'\"":
            i = _skip_quote(text, i)
            if i < 0:
                return None
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:i], i + 1
        i += 1
    return None


def _capture_backtick(text: str, start: int) -> tuple[str, int] | None:
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
        elif text[i] == "`":
            return text[start:i], i + 1
        else:
            i += 1
    return None


def _lex(command: str, tails: list[str] | None = None) -> list[_Tok] | None:
    """Words and shell operators with quoting resolved; None if a quote or a
    substitution is left open.

    A `#` at a word start ends the scan of its line, but the text it drops is
    appended to `tails` for the caller to scan: a `#` inside `${y/ #/}` is not
    a comment to the shell, and the text after it still runs. Without `tails`
    a `#` is an ordinary character. CR is a word character, as in bash.

    A hand-rolled scanner rather than shlex: shlex drops whether a word was
    quoted, which is what separates data from an executable argument. Words
    record the bodies of `$(...)` and backticks that the shell would expand
    (not those inside single quotes) so the caller can classify them.
    """
    toks: list[_Tok] = []
    buf: list[str] = []
    subst: list[str] = []
    state = {"word": False, "quoted": False}

    def flush() -> None:
        if state["word"]:
            toks.append(_Tok("".join(buf), state["quoted"], False, tuple(subst)))
        buf.clear()
        subst.clear()
        state["word"] = state["quoted"] = False

    i, n = 0, len(command)
    while i < n:
        char = command[i]
        if char in " \t":
            flush()
            i += 1
        elif char == "\n":
            flush()
            toks.append(_Tok("\n", op=True))
            i += 1
        elif char == "&" and (
            (state["word"] and buf and buf[-1] in "<>") or command.startswith(">", i + 1)
        ):
            buf.append(char)  # `2>&1`, `&>file`: part of a redirection word
            state["word"] = True
            i += 1
        elif char in ";&|()":
            flush()
            pair = command[i : i + 2]
            if pair in ("&&", "||", "|&", ";;"):
                toks.append(_Tok(pair, op=True))
                i += 2
            else:
                toks.append(_Tok(char, op=True))
                i += 1
        elif char == "\\":
            if i + 1 < n and command[i + 1] != "\n":
                buf.append(command[i + 1])
                state["word"] = state["quoted"] = True
            i += 2
        elif char == "#" and not state["word"] and tails is not None:
            end = command.find("\n", i)
            end = n if end < 0 else end
            tails.append(command[i + 1 : end])
            i = end
        elif char == "$" and command.startswith("'", i + 1):
            escapes = {"n": "\n", "t": "\t", "r": "\r"}
            decoded: list[str] = []
            j = i + 2
            while j < n and command[j] != "'":
                if command[j] == "\\" and j + 1 < n:
                    decoded.append(escapes.get(command[j + 1], command[j + 1]))
                    j += 2
                else:
                    decoded.append(command[j])
                    j += 1
            if j >= n:
                return None
            buf.append("".join(decoded))
            state["word"] = state["quoted"] = True
            i = j + 1
        elif char in "<>" and command.startswith("(", i + 1):
            captured = _capture_paren(command, i + 2)
            if captured is None:
                return None
            subst.append(captured[0])
            buf.append(char + "(" + captured[0] + ")")
            state["word"] = True
            i = captured[1]
        elif char == "'":
            end = command.find("'", i + 1)
            if end < 0:
                return None
            buf.append(command[i + 1 : end])
            state["word"] = state["quoted"] = True
            i = end + 1
        elif char == '"':
            state["word"] = state["quoted"] = True
            i += 1
            while True:
                if i >= n:
                    return None
                inner = command[i]
                if inner == '"':
                    i += 1
                    break
                if inner == "\\" and i + 1 < n:
                    following = command[i + 1]
                    if following in '"\\$`':
                        buf.append(following)
                    elif following != "\n":
                        buf.append(inner + following)
                    i += 2
                elif inner == "$" and command.startswith("(", i + 1):
                    captured = _capture_paren(command, i + 2)
                    if captured is None:
                        return None
                    subst.append(captured[0])
                    buf.append("$(" + captured[0] + ")")
                    i = captured[1]
                elif inner == "`":
                    captured = _capture_backtick(command, i + 1)
                    if captured is None:
                        return None
                    subst.append(captured[0])
                    buf.append("`" + captured[0] + "`")
                    i = captured[1]
                else:
                    buf.append(inner)
                    i += 1
        elif char == "$" and command.startswith("(", i + 1):
            captured = _capture_paren(command, i + 2)
            if captured is None:
                return None
            subst.append(captured[0])
            buf.append("$(" + captured[0] + ")")
            state["word"] = True
            i = captured[1]
        elif char == "`":
            captured = _capture_backtick(command, i + 1)
            if captured is None:
                return None
            subst.append(captured[0])
            buf.append("`" + captured[0] + "`")
            state["word"] = True
            i = captured[1]
        else:
            buf.append(char)
            state["word"] = True
            i += 1
    flush()
    return toks


def _fallback_tokens(line: str) -> list[_Tok]:
    """Unparseable line: whitespace words, nothing counts as quoted data."""
    toks: list[_Tok] = []
    for part in re.split(r"(&&|\|\||\|&|;|\||&|\(|\))", line):
        if part in ("&&", "||", "|&", ";", "|", "&", "(", ")"):
            toks.append(_Tok(part, op=True))
        else:
            toks.extend(_Tok(word) for word in part.split())
    return toks


def _floor(text: str) -> list[tuple[str, str]]:
    """The legacy regex list over `text`: the deny floor for executable text."""
    segments = [normalize_segment(segment) for segment in command_segments(text)]
    return [
        (key, reason)
        for (pattern, reason, _operation), key in zip(BLOCKED_PATTERNS, FLOOR_KEYS)
        if any(re.search(pattern, segment) for segment in segments)
    ]


def _short_flags(args: list[str]) -> str:
    return "".join(
        arg[1:] for arg in args if len(arg) > 1 and arg[0] == "-" and arg[1:].isalpha()
    )


def _git_subcommand(sub: str, rest: list[str]) -> list[tuple[str, str]]:
    long_flags = {arg for arg in rest if arg.startswith("--")}
    short = _short_flags(rest)
    discards_all = any(arg in (".", "*", "./", "./.", ":/", ":(top)") for arg in rest)
    if sub == "push":
        forced = (
            "--force" in long_flags
            or any(arg.startswith("--force-with-lease") for arg in rest)
            or "f" in short
            or any(arg.startswith("+") and len(arg) > 1 for arg in rest)
        )
        return [("push-force", MSG_PUSH_FORCE) if forced else ("push", MSG_PUSH)]
    if sub == "reset" and "--hard" in long_flags:
        return [("reset-hard", MSG_RESET)]
    if sub == "clean" and ("--force" in long_flags or "f" in short):
        return [("clean-force", MSG_CLEAN)]
    if sub == "branch":
        forced = "--force" in long_flags or "f" in short
        deleting = "--delete" in long_flags or "d" in short
        if "D" in short or (deleting and forced):
            return [("branch-delete", MSG_BRANCH)]
    if sub == "checkout":
        found = []
        if discards_all:
            found.append(("discard-all", MSG_CHECKOUT))
        if "--force" in long_flags or "f" in short:
            found.append(("checkout-force", MSG_CHECKOUT_FORCE))
        return found
    if sub == "switch" and ("--force" in long_flags or "--discard-changes" in long_flags or "f" in short):
        return [("checkout-force", MSG_SWITCH_FORCE)]
    if sub == "worktree" and rest[:1] == ["remove"] and ("--force" in long_flags or "f" in short):
        return [("worktree-force", MSG_WORKTREE_FORCE)]
    if sub == "restore" and discards_all:
        staged_only = ("--staged" in long_flags or "S" in short) and not (
            "--worktree" in long_flags or "W" in short
        )
        if not staged_only:
            return [("discard-all", MSG_RESTORE)]
    if sub == "stash" and rest[:1] == ["clear"]:
        return [("stash-clear", MSG_STASH_CLEAR)]
    return []


def _git(args: list[str], depth: int) -> list[tuple[str, str]]:
    """Findings for the words after `git`: global flags skipped, aliases resolved."""
    aliases: dict[str, str] = {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in GIT_VALUE_FLAGS:
            i += 2
        elif arg == "-c":
            if i + 1 < len(args):
                name, _, value = args[i + 1].partition("=")
                if name.lower().startswith("alias."):
                    aliases[name[6:].lower()] = value
            i += 2
        elif arg.startswith("-"):
            i += 1
        else:
            break
    else:
        return []
    sub, rest = args[i], args[i + 1 :]
    found = _git_subcommand(sub, rest)
    if _built(sub, GIT_DESTRUCTIVE_SUBS):
        found.append(("classifier-error", MSG_OPAQUE_GIT))
    value = aliases.get(sub.lower())
    if value is not None:
        tail = " ".join(rest)
        script = value[1:] if value.startswith("!") else "git " + value
        found += _scan(f"{script} {tail}", depth + 1, False)
    return found


def _built(text: str, names: tuple[str, ...]) -> bool:
    """True when a brace expansion, a substitution or a glob in `text` could
    build one of `names` (a word the guard cannot resolve to a literal)."""
    if BRACE_EXPANSION.search(text) or "$(" in text or "`" in text:
        return True
    base = text.rsplit("/", 1)[-1]
    return any(c in base for c in "*?[") and any(
        fnmatch.fnmatchcase(name, base) for name in names
    )


def _env_split(flag: str, following: str | None) -> tuple[str, bool] | None:
    """The `-S`/`--split-string` script in an env option word and whether it is
    the next word, else None."""
    if flag.startswith("--"):
        name, equals, value = flag[2:].partition("=")
        if not name or not "split-string".startswith(name):
            return None
        return (value, False) if equals else (following or "", True)
    for pos, char in enumerate(flag[1:], 1):
        if char in "uC":
            return None
        if char == "S":
            rest = flag[pos + 1 :]
            return (rest, False) if rest else (following or "", True)
    return None


def _command_words(segment: list[_Tok], scripts: list[str]) -> list[_Tok]:
    """The segment from its real command on: assignments, keywords and wrapper
    prefixes (with their own options) skipped. The scripts of `env -S` are
    appended to `scripts` for the caller to scan."""
    i = 0
    while i < len(segment):
        text = segment[i].text
        name = text.rsplit("/", 1)[-1]
        if ASSIGNMENT.match(text) or name in KEYWORDS:
            i += 1
        elif name in WRAPPERS:
            takes = WRAPPERS[name]
            i += 1
            while i < len(segment) and segment[i].text.startswith("-"):
                flag = segment[i].text
                i += 1
                if flag == "--":
                    break
                if name == "env":
                    following = segment[i].text if i < len(segment) else None
                    split = _env_split(flag, following)
                    if split is not None:
                        scripts.append(split[0])
                        i += split[1]
                        continue
                if flag in takes:
                    i += 1
            if name == "timeout":
                i += 1
        else:
            break
    return segment[i:]


def _shell_script_arg(words: list[_Tok]) -> int | None:
    """Index of the script word after `-c` in a shell invocation, if any."""
    for idx in range(1, len(words)):
        text = words[idx].text
        if not text.startswith("-"):
            return None
        if not text.startswith("--") and "c" in text[1:]:
            return idx + 1
    return None


def _name(words: list[_Tok]) -> str:
    return words[0].text.rsplit("/", 1)[-1] if words else ""


def _segment(
    segment: list[_Tok], words: list[_Tok], depth: int
) -> list[tuple[str, str]]:
    name = _name(words)
    found = _floor(" ".join(tok.text for tok in segment))
    args = [tok.text for tok in words[1:]]
    if name in DATA_COMMANDS:
        for tok in words[1:]:
            if tok.quoted:
                found += _scan(tok.text, depth + 1)
    elif name == "git" or (words and _built(words[0].text, ("git",))):
        found += _git(args, depth)
    elif name in SHELLS:
        idx = _shell_script_arg(words)
        if idx is not None and idx < len(words):
            found += _scan(words[idx].text, depth + 1)
    elif name == "eval":
        found += _scan(" ".join(args), depth + 1)
    return found


def _groups(toks: list[_Tok]) -> list[list[list[_Tok]]]:
    """Commands split on control operators; each is a pipeline of segments."""
    groups: list[list[list[_Tok]]] = [[[]]]
    for tok in toks:
        if not tok.op:
            groups[-1][-1].append(tok)
        elif tok.text in GROUP_OPS:
            groups.append([[]])
        else:
            groups[-1].append([])
    return groups


def _scan(command: str, depth: int, comments: bool = True) -> list[tuple[str, str]]:
    """Every finding for `command`, with nothing exempt: quoted arguments of
    echo/grep/printf are scanned as text a consumer might execute, and the
    text a `#` drops is scanned too. The depth cap denies."""
    if depth > MAX_DEPTH:
        return [("classifier-error", MSG_DEPTH)] + _floor(command)
    found: list[tuple[str, str]] = []
    tails: list[str] | None = [] if comments else None
    toks = _lex(command, tails)
    if toks is None:
        toks = []
        if tails is not None:
            tails.clear()
        for line in command.split("\n"):
            line_toks = _lex(line, tails)
            if line_toks is None:
                found += _floor(line)
                line_toks = _fallback_tokens(line)
            toks += line_toks + [_Tok("\n", op=True)]
    for tail in tails or ():
        found += _scan(tail, depth + 1, False)
    for pipeline in _groups(toks):
        scripts: list[str] = []
        words = [_command_words(segment, scripts) for segment in pipeline]
        for script in scripts:
            found += _scan(script, depth + 1)
        for segment, segment_words in zip(pipeline, words):
            for tok in segment:
                for body in tok.subst:
                    found += _scan(body, depth + 1)
            found += _segment(segment, segment_words, depth)
    return found


def _quoted_data_only(command: str) -> bool:
    """The one allowance for quoted destructive text, default deny.

    True only for a single pipeline `A | B | ...` where A is echo, printf or
    grep/egrep/fgrep and every other member is a plain text filter (bare
    names: no path, no quoting), with none of ALLOWANCE_FORBIDDEN_CHARS
    outside quotes, none of ALLOWANCE_FORBIDDEN_WORDS as an unquoted word,
    no `$`, backtick or backslash inside double quotes, no newline or CR
    anywhere, and nothing destructive anywhere but inside A's quoted text
    (the floor runs over the rest of the command as written).
    """
    members: list[list[tuple[str, bool]]] = [[]]
    raw: list[list[str]] = [[]]
    kept: list[str] = []
    word: list[str] = []
    quote = ""
    quoted_word = False

    def end_word() -> None:
        nonlocal word, quoted_word
        if word or quoted_word:
            members[-1].append(("".join(word), quoted_word))
        word, quoted_word = [], False

    for char in command:
        if char in "\r\n":
            return False
        if quote:
            raw[-1].append(char)
            if char == quote:
                quote = ""
                if len(members) == 1:
                    kept.append(" ")
            elif quote == '"' and char in "\\$`":
                return False
            continue
        if char in "'\"":
            quote, quoted_word = char, True
            raw[-1].append(char)
            continue
        if char == "|":
            end_word()
            if not members[-1]:
                return False
            members.append([])
            raw.append([])
            continue
        if char in ALLOWANCE_FORBIDDEN_CHARS:
            return False
        raw[-1].append(char)
        if len(members) == 1:
            kept.append(char)
        if char in " \t":
            end_word()
        else:
            word.append(char)
    if quote:
        return False
    end_word()
    if not members[-1]:
        return False
    for index, member in enumerate(members):
        text, quoted = member[0]
        if quoted or text not in (DATA_COMMANDS if index == 0 else TEXT_FILTERS):
            return False
    if any(
        not quoted and text in ALLOWANCE_FORBIDDEN_WORDS
        for member in members
        for text, quoted in member
    ):
        return False
    remainder = "|".join(["".join(kept)] + ["".join(chars) for chars in raw[1:]])
    return not _floor(remainder)


def _pick(found: list[tuple[str, str]]) -> tuple[str, str] | None:
    if not found:
        return None
    return min(found, key=lambda item: PRIORITY.index(item[0]))


def classify_git_command(command: str) -> tuple[str, str] | None:
    """`(reason_key, message)` for a command that must be blocked, else None.

    Pure: no I/O, no approval-token handling. `reason_key` is `push` or
    `branch-delete` for the two token-unlockable operations; every other key
    has no unlock path. Everything the legacy floor denies on the raw text is
    denied, except what `_quoted_data_only` allows.
    """
    if len(command) > MAX_COMMAND_CHARS and GIT_WORD.search(command):
        return ("command-too-large", MSG_TOO_LARGE)
    if _quoted_data_only(command):
        return None
    return _pick(_floor(command) + _scan(command, 0))


def _log_classifier_failure(exc: Exception, command: str) -> None:
    log_event(
        "plugin_git_guard_classifier_failed",
        {
            "wf": None,
            "phase": "unknown",
            "task_id": None,
            "agent": "unknown",
            "event": "git_guard_classifier_failed",
            "decision": "deny" if GIT_WORD.search(command) else "allow",
            "reason": "classifier-error",
            "error": exc.__class__.__name__,
        },
    )


def main() -> int:
    try:
        data = load_input()
    except Exception:
        return 0

    tool_input = data.get("tool_input") if isinstance(data, dict) else None
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not command:
        return 0

    try:
        verdict = classify_git_command(command)
    except Exception as exc:
        # Fail closed when the text names git as a word: a silent fallback to
        # the floor would be weaker than the classifier it replaces.
        _log_classifier_failure(exc, command)
        verdict = (
            ("classifier-error", MSG_CLASSIFIER_ERROR)
            if GIT_WORD.search(command)
            else None
        )
    if verdict is None:
        return 0

    key, reason = verdict
    operation = APPROVABLE.get(key)
    if operation is not None:
        try:
            wf = consume_approval(operation)
        except Exception as exc:
            _log_token("git_guard_token_check_failed", exc.__class__.__name__)
            wf = None
        if wf is not None:
            log_event(
                "plugin_git_guard_approved",
                {
                    "wf": wf,
                    "phase": "build-finish",
                    "task_id": None,
                    "agent": "router",
                    "event": "git_guard_token_consumed",
                    "decision": "allow",
                    "reason": f"approval token covered operation:{operation}",
                    "command": command,
                },
            )
            return 0
    log_event(
        "plugin_git_guard_blocked",
        {
            "wf": None,
            "phase": "unknown",
            "task_id": None,
            "agent": "unknown",
            "event": "git_guard_blocked",
            "decision": "deny",
            "reason": reason,
            "command": command,
        },
    )
    if operation is not None:
        hint = (
            "If this is a router-sanctioned finishing step, the router "
            "must first record the user's explicit menu choice as an "
            "approval token (.cc10x/state/git-approval.json). Otherwise "
            "ask the user to run it manually."
        )
    else:
        hint = (
            "This operation has no approval-token path. "
            "If it is intentional, ask the user to run it manually."
        )
    pretool_deny(f"cc10x git guardrails blocked: {reason} {hint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
