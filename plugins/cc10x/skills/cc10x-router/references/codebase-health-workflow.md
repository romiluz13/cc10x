### CODEBASE-HEALTH workflow

**Advisory-only upkeep.** Surfaces deepening candidates and grills the chosen one. Never writes code. A chosen candidate routes to PLAN only on a fresh user request.

### CODEBASE-HEALTH preparation

1. The router creates the workflow artifact with `workflow_type: CODEBASE-HEALTH`.
2. Restore any design/research references from `activeContext.md ## References`.

### CODEBASE-HEALTH task graph

Single-pass advisory workflow (no `phase_cursor`, no phases):

```text
TaskCreate({
  subject: "CC10X architecture-scanner: Scan for deepening opportunities",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:codebase-health\nplan:N/A\nscope:N/A\nreason:Surface shallow modules and deepening candidates\n\nWalk the codebase using the canonical deep-module vocabulary, find shallow modules / pass-throughs / semantic duplicates, apply the deletion test, produce an HTML report with before/after diagrams.",
  activeForm: "Scanning for deepening opportunities"
}) -> scanner_task_id

TaskCreate({
  subject: "CC10X Memory Update: Persist codebase-health learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .cc10x/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Persisting codebase-health learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [scanner_task_id] })
```

The Memory Update task is router-inline bookkeeping, not a second agent: CODEBASE-HEALTH stays advisory-only and still ends when the report is presented.

After the architecture-scanner emits its contract:

- If `STATUS=CANDIDATES_FOUND`: the router opens the HTML report for the user and presents the candidates. The user picks one (or declines).
- If `STATUS=NO_CANDIDATES`: the router reports the codebase is healthy; the workflow ends.
- If the user picks a candidate: dispatch `exploration` in DESIGN mode to grill the deepening design. Domain ambiguity stops for human. The grilled design feeds the PLAN workflow on a fresh user request — CODEBASE-HEALTH does NOT auto-dispatch to PLAN.

### CODEBASE-HEALTH completion

The router owns task completion for the architecture-scanner (read-only agents use the router-owned completion fallback). The architecture-scanner emits its contract and stops its turn — the router marks the task completed, then runs the Memory Update task inline to persist the memory notes (blocked by the scanner task). No BUILD/DONE finishing menu — the workflow ends when the report is presented and (optionally) a candidate is grilled.
