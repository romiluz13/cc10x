### TRIAGE workflow

**Advisory-only.** Categorizes, verifies, and writes agent-ready briefs for incoming issues/PRs. Never writes code. Never auto-routes into BUILD/DEBUG — the user routes on a fresh request after the brief is presented.

### TRIAGE preparation

1. Restore any design/research references from `activeContext.md ## References`.
2. The router creates the workflow artifact with `workflow_type: TRIAGE`.
3. Emit `[DEBUG-RESET]`-equivalent: none — TRIAGE is single-pass, no attempt tracking.

### TRIAGE task graph

Single-pass advisory workflow (no `phase_cursor`, no phases):

```text
TaskCreate({
  subject: "CC10X triage-agent: Triage {issue_ref}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:triage\nplan:N/A\nscope:N/A\nreason:Categorize and verify incoming issue\n\nRead the issue/PR, verify the claim, check for redundancy and prior rejection, categorize, assign state, write an agent-ready brief.",
})
```

After the triage-agent emits its contract:

- If `STATUS=NEEDS_INFO`: the router presents the needs-info questions to the user. The workflow pauses (`pending_gate: needs_info`). When the reporter replies, re-dispatch the triage-agent with the updated context.
- If `STATUS=TRIAGED` and `STATE=ready-for-agent`: the router presents the brief path to the user. The user routes to BUILD or DEBUG on a fresh request — TRIAGE does NOT auto-dispatch.
- If `STATUS=TRIAGED` and `STATE=ready-for-human`: the router presents the brief + the "why it can't be delegated" note to the user.
- If `STATUS=WONTFIX`: the router presents the wontfix reason. For a rejected enhancement, the agent writes to `.out-of-scope/`; for an already-implemented feature, it points to the existing implementation.
- If the issue needed fleshing out (`triage-agent` set `NEEDS_GRILLING=true`): dispatch `exploration` in DESIGN mode to grill the issue into shape. Domain ambiguity stops for human input. The grilled result feeds back into a second triage-agent pass.

### TRIAGE completion

The router owns task completion for the triage-agent (read-only agents use the router-owned completion fallback). The triage-agent emits its contract and stops its turn — the router marks the task completed and persists memory notes at workflow-final. No BUILD/DONE finishing menu — the workflow ends when the brief is presented.
