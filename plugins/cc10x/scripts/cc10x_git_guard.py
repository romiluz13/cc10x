#!/usr/bin/env python3
"""Git guardrails — blocks dangerous git commands that can destroy work.

PreToolUse hook for Bash commands. Blocks:
- git push (to remote — local commits are safe)
- git reset --hard
- git clean -f / git clean -fd
- git branch -D (force delete)
- git checkout . (discard all changes)
- git checkout -- . (discard all changes)
"""
import json
import re
import sys


BLOCKED_PATTERNS = [
    (r"\bgit\s+push\b", "git push — pushing to remote. Use a branch and PR instead."),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard — destroys uncommitted changes."),
    (r"\bgit\s+clean\s+-[a-z]*f[a-z]*\b", "git clean -f — removes untracked files permanently."),
    (r"\bgit\s+branch\s+-D\b", "git branch -D — force-deletes a branch."),
    (r"\bgit\s+checkout\s+\.\s*$", "git checkout . — discards all uncommitted changes."),
    (r"\bgit\s+checkout\s+--\s+\.\s*$", "git checkout -- . — discards all uncommitted changes."),
    (r"\bgit\s+checkout\s+\*\s*$", "git checkout * — discards all uncommitted changes."),
]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    command = data.get("tool_input", {}).get("command", "")
    if not command:
        return 0

    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            output = {
                "decision": "block",
                "reason": f"cc10x git guardrails blocked: {reason} "
                "If this is intentional, ask the user to run it manually.",
            }
            print(json.dumps(output))
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
