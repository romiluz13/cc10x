---
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Apply the cc10x router's intent routing to each of the four requests below. Only decide the route for each: do not run any workflow, create any task or artifact, or edit any file other than outcome.txt.

R1: "Review the new payments module in src/payments.py and fix anything sketchy you find while you are in there."
R2: "Walk me through how src/calc.py works."
R3: "Prove checkout works: write end-to-end tests for it."
R4: "Users hit a crash on checkout when the cart is empty. Add a guard so it stops throwing."

Write a file named outcome.txt in the repo root with exactly these lines, each value one of DEBUG, PLAN, REVIEW, ORIENT, QA, TRIAGE, CODEBASE-HEALTH, BUILD:

ROUTE_1=<route for R1>
ROUTE_2=<route for R2>
ROUTE_3=<route for R3>
ROUTE_4=<route for R4>
