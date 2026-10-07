### TRIAGE workflow

**Advisory-only.** Categorizes, verifies, and writes agent-ready briefs for incoming issues/PRs. Never writes code. Never auto-routes into BUILD/DEBUG — the user routes on a fresh request after the brief is presented.

### TRIAGE preparation

1. Restore any design/research references from `activeContext.md ## References`.
2. The router creates the workflow artifact with `workflow_type: TRIAGE`.
3. Emit `[DEBUG-RESET]`-equivalent: none — TRIAGE is single-pass, no attempt tracking.

### TRIAGE task graph

Single-pass advisory workflow (no phases; `phase_cursor` stays null until finalize sets it to `memory-finalize`). The graph created with the workflow holds ONLY the agent task:

```text
TaskCreate({
  subject: "CC10X triage-agent: Triage {issue_ref}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:triage\nplan:N/A\nscope:N/A\nreason:Categorize and verify incoming issue\n\nRead the issue/PR, verify the claim, check for redundancy and prior rejection, categorize, assign state, write an agent-ready brief.",
  activeForm: "Triaging issue"
}) -> triage_task_id
```

Memory Update is created ONLY at the terminal state, never with the graph above. The terminal states are `STATUS=TRIAGED` with `NEEDS_GRILLING` not true, and `STATUS=WONTFIX`. On `STATUS=NEEDS_INFO`, or on `NEEDS_GRILLING=true`, the workflow pauses on `pending_gate` (`needs_info` or `needs_grilling`), no Memory Update task exists or is runnable, and nothing is finalized. When the pause is answered, the router dispatches a new `phase:triage` agent task carrying the new context (the second pass). The router creates Memory Update when a pass returns a terminal state, blocked by that pass's triage task:

```text
TaskCreate({
  subject: "CC10X Memory Update: Persist triage learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .cc10x/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Persisting triage learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [triage_task_id] })
```

The Memory Update task is router-inline bookkeeping, not a second agent: TRIAGE stays advisory-only and still ends when the brief is presented (a terminal state).

After the triage-agent emits its contract:

- If `STATUS=NEEDS_INFO`: the router presents the needs-info questions to the user. The workflow pauses (`pending_gate: needs_info`) with no Memory Update task. When the reporter replies, re-dispatch the triage-agent with the updated context (a new `phase:triage` task, second pass).
- If `STATUS=TRIAGED` and `STATE=ready-for-agent`: the router presents the brief path to the user. The user routes to BUILD or DEBUG on a fresh request — TRIAGE does NOT auto-dispatch.
- If `STATUS=TRIAGED` and `STATE=ready-for-human`: the router presents the brief + the "why it can't be delegated" note to the user.
- If `STATUS=WONTFIX`: the router presents the wontfix reason. For a rejected enhancement, the agent writes to `.out-of-scope/`; for an already-implemented feature, it points to the existing implementation.
- If the issue needed fleshing out (`triage-agent` set `NEEDS_GRILLING=true`): dispatch `exploration` in DESIGN mode to grill the issue into shape. Domain ambiguity stops for human input. The workflow pauses (`pending_gate: needs_grilling`) with no Memory Update task until the grilled result has fed a second triage-agent pass that returns a terminal state.

### TRIAGE failure and abandonment

A triage-agent error or a malformed contract sets `failure_stop_gate` (the existing gate) with `pending_gate` `triage_agent_failed`; the router persists any captured notes to the artifact `memory_notes`, creates NO Memory Update, and reports the failure to the user. The workflow stays open until the user retries (a new `phase:triage` task with changed input) or ends it; ending it is recorded as `workflow_failed` in `status_history` and clears `pending_gate`.

Only the user's decline or end finalizes a pause; an unanswered pause stays open (nothing finalizes it, and its notes stay in the artifact `memory_notes`). If the user ends a `needs_info` or `needs_grilling` pause instead of answering, that is the terminal state and the router creates Memory Update as above.

### TRIAGE completion

The router owns task completion for the triage-agent (read-only agents use the router-owned completion fallback). The triage-agent emits its contract and stops its turn — the router marks the task completed. On a terminal result it then creates the Memory Update task (blocked by that triage task) and runs it inline to persist the memory notes after the brief is presented; on a pause it does neither. No BUILD/DONE finishing menu — the workflow ends when the brief is presented.
