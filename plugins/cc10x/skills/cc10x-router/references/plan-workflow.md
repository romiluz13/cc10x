### PLAN preparation

1. Restore design enrichment:
   - Read `- Design:` from `activeContext.md ## References`.
   - If a design path exists, verify it with `Glob(...)` and hold it as fallback.
2. Mandatory brainstorming (ALWAYS runs for PLAN workflows):
   - ALWAYS run `Skill(skill="cc10x:brainstorming")` in the main context before planner. Brainstorming is how the user explores and clarifies intent — skipping it means the planner works from assumptions instead of understanding.
   - If a valid design file exists from step 1: brainstorming uses it as a foundation (the skill's Spec File Workflow reads and expands the existing design rather than starting from scratch).
   - If no design file exists: brainstorming starts from the user's request and explores the idea space.
   - Brainstorming may ask the user questions and may save a `*-design.md` file. After it completes, parse `### Brainstorming Handoff (MACHINE-READABLE)` and capture `DESIGN_FILE`.
   - If `DESIGN_FILE` is present, persist it into the workflow artifact `design_file` field and pass it under `## Design File`.
   - If no handoff is present, fall back to the pre-existing memory design reference from step 1.
   - Brainstorming should ask only unresolved, high-impact questions and stop as soon as the intent contract is complete.
3. Optional research before planning:
   - Ask whether to run web + GitHub research for external/unfamiliar technology when it would materially improve the plan.
4. Planner receives `## Research Files` only when research files actually exist.
5. Planner is agreement-first:
   - If a requirement is materially ambiguous, planner returns `STATUS=NEEDS_CLARIFICATION`.
   - Planner never treats its own defaults as approved implementation.
6. Planner must choose one `plan_mode`:
   - `direct` for trivial low-risk work
   - `execution_plan` for standard implementation work
   - `decision_rfc` for architecture or multi-option work
7. Planner must choose one `verification_rigor`:
   - `standard` by default (covers most work; keeps verification proportional to risk)
   - `critical_path` for security, money, state-machine, concurrency, or irreversible-migration work (failure in these domains is irreversible or high-blast-radius; justifies extended scenario coverage)
8. PLAN fresh-review loop:
   - Every PLAN workflow pre-creates a bounded review DAG: `plan-create -> plan-review-gap-1 -> re-plan -> plan-review-gap-2 -> memory-finalize`.
   - Every saved plan artifact enters that DAG, including `direct`, `execution_plan`, and `decision_rfc`.
   - If pass 1 succeeds, the router prunes the unused `re-plan` and pass 2 branch explicitly.
   - If pass 1 finds blocking issues, the router keeps the pre-created `re-plan` and pass 2 branch alive.
   - Maximum fresh-review passes: 2.
   - Planner remains the only plan writer.
   - The existing inline `plan-review-gate` inside planner remains the final fail-closed boundary on each planner pass.

### PLAN task graph

```text
TaskCreate({
  subject: "CC10X planner: Create plan for {feature}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:plan-create\nplan:N/A\nscope:N/A\nreason:Create implementation plan\n\nChoose the correct plan mode (`direct`, `execution_plan`, or `decision_rfc`) and verification rigor (`standard` or `critical_path`). Create the corresponding planning artifact.",
  activeForm: "Creating plan"
}) -> planner_task_id

TaskCreate({
  subject: "CC10X plan-gap-reviewer: Fresh review pass 1",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:plan-review-gap-1\nplan:N/A\nscope:N/A\nreason:Fresh anti-anchoring review of saved plan (pass 1)\n\nWait for the planner to save a plan artifact, then review it against the original user request and any approved design/research files.",
  activeForm: "Fresh-reviewing plan"
}) -> planning_review_pass1_task_id
TaskUpdate({ taskId: planning_review_pass1_task_id, addBlockedBy: [planner_task_id] })

TaskCreate({
  subject: "CC10X planner: Revise plan after fresh review",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:re-plan\nplan:N/A\nscope:N/A\nreason:Revise plan if fresh review finds blocking issues\n\nOnly run if pass 1 finds blocking issues. Revise the existing saved plan using structured planning review findings.",
  activeForm: "Revising plan"
}) -> planner_replan_task_id
TaskUpdate({ taskId: planner_replan_task_id, addBlockedBy: [planning_review_pass1_task_id] })

TaskCreate({
  subject: "CC10X plan-gap-reviewer: Fresh review pass 2",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:plan-review-gap-2\nplan:N/A\nscope:N/A\nreason:Fresh anti-anchoring review of saved plan (pass 2)\n\nOnly run if the re-plan task produces a revised saved plan after pass 1 findings.",
  activeForm: "Fresh-reviewing revised plan"
}) -> planning_review_pass2_task_id
TaskUpdate({ taskId: planning_review_pass2_task_id, addBlockedBy: [planner_replan_task_id] })

TaskCreate({
  subject: "CC10X Memory Update: Index plan in memory",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .claude/cc10x/v10/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Indexing plan in memory"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [planner_task_id, planning_review_pass1_task_id, planner_replan_task_id, planning_review_pass2_task_id] })
```
