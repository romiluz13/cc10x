---
max_turns: 120
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Use cc10x to build a `median(values)` function in src/stats.py with a unittest for it in tests/test_stats.py. It must raise ValueError on an empty list, and the module must handle empty input consistently. Treat any reviewer or hunter finding of HIGH severity or above as requiring a remediation (REM-FIX) task; do not ask me, just remediate.

When the workflow has finished, write a file named outcome.txt in the repo root with exactly these lines, filled in from the workflow artifact and the last completed REM-FIX task report (use `none` where no REM-FIX ran):

REMFIX_COUNT=<number of REM-FIX tasks created>
COVERING_TESTS=<the COVERING_TESTS value that REM-FIX report carried>
TEST_COMMAND=<the TEST_COMMAND value that REM-FIX report carried>
