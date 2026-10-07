---
max_turns: 60
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent, TaskCreate, TaskGet, TaskList, TaskUpdate]
---

Use cc10x to triage the incoming issue described in issues/ISSUE-1.md. Triage only: categorize it and write the brief; write no code.

When the workflow has finished, read the workflow artifact JSON under .cc10x/workflows/ and write a file named outcome.txt in the repo root with exactly this line, filled in from that artifact:

WORKFLOW_TYPE=<workflow_type>
