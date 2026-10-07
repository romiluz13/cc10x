### CODEBASE-HEALTH workflow

**Advisory-only upkeep.** Surfaces deepening candidates and grills the chosen one. Never writes code. A chosen candidate routes to PLAN only on a fresh user request.

### CODEBASE-HEALTH preparation

1. The router creates the workflow artifact with `workflow_type: CODEBASE-HEALTH`.
2. Restore any design/research references from `activeContext.md ## References`.

### CODEBASE-HEALTH task graph

Single-pass advisory workflow (no phases; `phase_cursor` stays null until finalize sets it to `memory-finalize`). The graph created with the workflow holds ONLY the agent task:

```text
TaskCreate({
  subject: "CC10X architecture-scanner: Scan for deepening opportunities",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:codebase-health\nplan:N/A\nscope:N/A\nreason:Surface shallow modules and deepening candidates\n\nWalk the codebase using the canonical deep-module vocabulary, find shallow modules / pass-throughs / semantic duplicates, apply the deletion test, produce an HTML report with before/after diagrams.",
  activeForm: "Scanning for deepening opportunities"
}) -> scanner_task_id
```

Memory Update is created ONLY at the terminal state, never with the graph above. The terminal state is `STATUS=NO_CANDIDATES`, or `STATUS=CANDIDATES_FOUND` with the report presented and the user declined or moved on, or the chosen candidate's grill completed. While candidates wait for a choice or a grill is running, the workflow pauses on `pending_gate` (`candidate_choice`), no Memory Update task exists or is runnable, and nothing is finalized. The router creates Memory Update at the terminal state, blocked by the scanner task:

```text
TaskCreate({
  subject: "CC10X Memory Update: Persist codebase-health learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .cc10x/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Persisting codebase-health learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [scanner_task_id] })
```

The Memory Update task is router-inline bookkeeping, not a second agent: CODEBASE-HEALTH stays advisory-only and still ends when the report is presented and any chosen candidate is grilled (a terminal state).

After the architecture-scanner emits its contract:

- If `STATUS=CANDIDATES_FOUND`: the router opens the HTML report for the user and presents the candidates. The workflow pauses on `candidate_choice`. The user picks one (or declines); a fresh request that picks none counts as declined.
- If `STATUS=NO_CANDIDATES`: the router reports the codebase is healthy; the workflow ends.
- If the user picks a candidate: dispatch `exploration` in DESIGN mode to grill the deepening design. Domain ambiguity stops for human. The workflow stays paused through the grill; its terminal state, and Memory Update, come when the grill completes. The grilled design feeds the PLAN workflow on a fresh user request — CODEBASE-HEALTH does NOT auto-dispatch to PLAN.

### CODEBASE-HEALTH failure and abandonment

A scanner error or a malformed contract sets `failure_stop_gate` (the existing gate) with `pending_gate` `architecture_scanner_failed`; the router persists any captured notes to the artifact `memory_notes`, creates NO Memory Update, and reports the failure to the user. The workflow stays open until the user retries (a new `phase:codebase-health` task with changed input) or ends it; ending it is recorded as `workflow_failed` in `status_history` and clears `pending_gate`.

Only the user's decline or end finalizes a pause (a fresh request that picks no candidate counts as that); an unanswered pause stays open (nothing finalizes it, and its notes stay in the artifact `memory_notes`).

### CODEBASE-HEALTH completion

The router owns task completion for the architecture-scanner (read-only agents use the router-owned completion fallback). The architecture-scanner emits its contract and stops its turn — the router marks the task completed. At the terminal state it then creates the Memory Update task (blocked by the scanner task) and runs it inline to persist the memory notes; while the workflow is paused it does neither. No BUILD/DONE finishing menu — the workflow ends when the report is presented and (optionally) a candidate is grilled.
