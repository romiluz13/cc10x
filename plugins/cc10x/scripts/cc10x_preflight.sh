#!/bin/sh
# SessionStart Python health preflight. Every other CC10X hook is a python3
# script, so when python3 is missing or older than 3.9 they all fail silently.
# This one is POSIX sh so it can still tell the agent. Always exits 0.

if command -v python3 >/dev/null 2>&1 &&
  python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
  exit 0
fi

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"CC10X WARNING: python3 is missing or older than 3.9, so every CC10X hook (protected-write guard, git guardrails, workflow artifact audit, resume context) is silently disabled. Tell the user to install or upgrade Python (3.13 recommended, 3.9 minimum) and restart the session."}}'
exit 0
