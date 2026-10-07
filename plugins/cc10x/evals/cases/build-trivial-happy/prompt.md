---
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent, TaskCreate, TaskGet, TaskList, TaskUpdate]
---

Use cc10x to build this: create a file named greeting.txt in the repo root containing exactly the single line `hello`. It is a trivial one-file change.

When the workflow has finished, read the workflow artifact JSON under .cc10x/workflows/ and write a file named outcome.txt in the repo root with exactly these lines, filled in from that artifact:

WORKFLOW_TYPE=<workflow_type>
PROOF_STATUS=<proof_status>
