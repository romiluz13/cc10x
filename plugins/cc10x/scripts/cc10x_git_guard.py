#!/usr/bin/env python3
"""Git guardrails — blocks dangerous git commands that can destroy work.

PreToolUse hook for Bash commands. Blocks:
- git push (to remote — local commits are safe)
- git reset --hard
- git clean -f / git clean -fd
- git branch -D (force delete)
- git checkout . (discard all changes)
- git checkout -- . (discard all changes)

Approval token (single-use unlock for router-sanctioned finishing flows):
`git push` and `git branch -D` — and ONLY those two — can be unlocked by a
fresh token at .cc10x/state/git-approval.json written by the router
immediately after the user's explicit BUILD-DONE finishing choice:

    {"wf": "wf-...", "operations": ["push"], "expires_at": "<UTC ISO>"}

The token is consumed (deleted) on first matching allow, and ignored when
expired (or older than MAX_TOKEN_AGE_SECONDS as a backstop). Destructive
history/worktree operations (reset --hard, clean -f, checkout ., force-push)
have NO token path and stay blocked unconditionally.
"""

import contextlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from cc10x_hooklib import log_event, pretool_deny, state_root

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
        with contextlib.suppress(OSError):
            path.unlink()
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


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    command = data.get("tool_input", {}).get("command", "")
    if not command:
        return 0

    for pattern, reason, operation in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            if operation is not None:
                wf = consume_approval(operation)
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
