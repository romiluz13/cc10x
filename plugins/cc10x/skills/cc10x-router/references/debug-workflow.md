### DEBUG preparation

1. If the user explicitly asks for research or the bug clearly depends on external post-2024 behavior, allow a research round before the first investigator run.
2. Immediately write `[DEBUG-RESET: wf:{workflow_uuid}]` once the workflow id exists.
3. Preserve failed attempt counting semantics: the investigator counts `[DEBUG-N]:` entries after the most recent reset marker.

### DEBUG task graph

```text
TaskCreate({
  subject: "CC10X bug-investigator: Investigate {error}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-investigate\nplan:N/A\nscope:N/A\nreason:Find root cause\n\nFind the root cause and apply the fix.",
  activeForm: "Investigating bug"
}) -> investigator_task_id

TaskCreate({
  subject: "CC10X code-reviewer: Review fix",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-review\nplan:N/A\nscope:N/A\nreason:Review the fix\n\nReview the debug fix quality.",
  activeForm: "Reviewing fix"
}) -> reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [investigator_task_id] })

TaskCreate({
  subject: "CC10X integration-verifier: Verify fix",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-verify\nplan:N/A\nscope:N/A\nreason:Verify the fix\n\nVerify the fix works end-to-end.",
  activeForm: "Verifying fix"
}) -> verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id] })

TaskCreate({
  subject: "CC10X Memory Update: Persist debug learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .cc10x/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Persisting debug learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [verifier_task_id] })
```

### DEBUG independence-test gate (opt-in fan-out)

Default to a SINGLE investigator. Fan-out is an opt-in optimization, gated on provable independence — when in doubt, serialize.

Only consider fanning out when the user reports many tests red across files AND the failures look like distinct root causes. Before fanning out, both halves of the INDEPENDENCE TEST must PASS:

1. **Separable understanding** — each problem is understandable and fixable without reading the others. If fixing A requires knowing B's root cause, they are one problem: serialize.
2. **Disjoint files** — group the failures by domain and list the files each group must touch. If any file appears in two groups, the groups are NOT independent: serialize (or merge the overlapping groups into one investigator).

If EITHER half fails, run a single investigator over all the failures.

When BOTH halves PASS, fan out one scoped `bug-investigator` per domain — each scoped to its own non-overlapping file set. State the scope explicitly in the task description so each agent stays in its lane:

```text
TaskCreate({
  subject: "CC10X bug-investigator: Investigate {domain} failures",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-investigate\nplan:N/A\nscope:{files this investigator owns — do NOT edit outside this set}\nreason:Independent root cause for {domain}\n\nFind the root cause and apply the fix WITHIN your scoped files only.",
  activeForm: "Investigating {domain} bug"
}) -> investigator_task_id_{domain}
```

### DEBUG fan-in conflict-check

On return from a fan-out, BEFORE running the unified verifier, run a fan-in CONFLICT-CHECK — two WRITE agents that strayed past their scope will silently clobber each other:

1. Collect the actual set of files each investigator edited (not the declared scope — what changed).
2. Intersect the edited-file sets pairwise. If any file was edited by two investigators, you have a conflict.
3. On conflict: do NOT proceed to verify. Reconcile the overlapping edits (re-investigate the shared file with a single agent that sees both fixes), then re-run the conflict-check.
4. Only when all edited-file sets are pairwise disjoint, proceed to the single unified verifier (the existing `integration-verifier` task) over the full test suite — never one verifier per domain, since a real fix must hold across the whole suite.
