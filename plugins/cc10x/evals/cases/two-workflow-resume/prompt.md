---
max_turns: 100
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Two cc10x workflows are in flight in this repo (see .cc10x/workflows/). Use cc10x to resume ONLY the one whose request is about alpha.txt, and finish it. Do not touch or advance the other workflow.

When done, write a file named outcome.txt in the repo root with exactly these lines:

RESUMED_WF=<workflow_uuid of the workflow you resumed>
OTHER_WF_PHASE_CURSOR=<phase_cursor now stored in the other workflow's artifact>
