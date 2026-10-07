---
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent, TaskCreate, TaskGet, TaskList, TaskUpdate]
---

Use cc10x QA to plan integration tests for calc.py. Perform only the QA workflow's artifact-seeding step, the step that copies the test-plan template into place as .cc10x/qa/<workflow_uuid>/test-plan.md (any workflow id directory matching .cc10x/qa/*/test-plan.md), and then stop. Do not continue to later QA phases and do not write tests.
