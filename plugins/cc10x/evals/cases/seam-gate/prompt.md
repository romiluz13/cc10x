---
max_turns: 100
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent, TaskCreate, TaskGet, TaskList, TaskUpdate]
---

Use cc10x to execute the approved plan in docs/plans/slug-plan.md; its tests belong in tests/test_slug.py.

When the workflow has finished, write a file named outcome.txt in the repo root with exactly these lines, copied from the component-builder's final Router Contract for the phase:

SEAM_GATE_STATUS=<value>
TEST_SEAMS=<comma-separated seam names>
