---
max_turns: 120
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent, TaskCreate, TaskGet, TaskList, TaskUpdate]
---

Use cc10x to execute the approved plan in docs/plans/two-phase-plan.md. Both phases are approved; run them in order to completion; they create phase-one.txt and phase-two.txt in the repo root.

When the workflow has finished, read the workflow artifact JSON under .cc10x/workflows/ and write a file named outcome.txt in the repo root with exactly these lines, filled in from that artifact:

PHASES_COMPLETED=<number of phases whose phase_status is completed>
MEMORY_FINALIZED_HISTORY=<number of status_history entries recording memory_finalized>
MEMORY_FINALIZED_EVENTS=<number of lines recording memory_finalized in the companion .events.jsonl file next to that artifact (0 if there is none)>
