---
max_turns: 120
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent, TaskCreate, TaskGet, TaskList, TaskUpdate]
---

Use cc10x to build a `median(values)` function in src/stats.py with a unittest for it in tests/test_stats.py. It must raise ValueError on an empty list, and the module must handle empty input consistently. Treat any reviewer or hunter finding of HIGH severity or above as requiring a remediation (REM-FIX) task; do not ask me, just remediate.

When the workflow has finished, write a file named outcome.txt in the repo root. Its first line is exactly:

REMFIX_COUNT=<number of REM-FIX tasks created>

If a REM-FIX task ran, the rest of the file is the proof section of the last completed REM-FIX task's report, copied verbatim (do not summarize or reformat it). If none ran, the second line is `none`.
