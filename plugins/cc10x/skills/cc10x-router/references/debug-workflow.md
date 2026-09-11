### DEBUG preparation

1. If the user explicitly asks for research or the bug clearly depends on external post-2024 behavior, allow a research round before the first investigator run.
2. Immediately write `[DEBUG-RESET: wf:{workflow_uuid}]` once the workflow id exists.
3. Preserve failed attempt counting semantics: the investigator counts `[DEBUG-N]:` entries after the most recent reset marker.

### QA-seeded DEBUG preparation

When this DEBUG was started from a QA `BUG_CANDIDATE` (the user accepted the offer in `qa-workflow.md` §Bug handoff):

1. This is a **new workflow**, not a QA phase — QA may not edit product code and DEBUG must. Generate a fresh `workflow_uuid` and run the standard DEBUG task graph unchanged.
2. Link it: set `source_wf` to the QA `workflow_uuid` and `source_bug_candidate` to the candidate `title` in the DEBUG artifact.
3. `[DEBUG-RESET: wf:{new_uuid}]` as normal. **QA's run is not a failed debug attempt** — attempt counting starts at zero. Seeding the counter would trip the 3-cycle human checkpoint early on a bug nobody has actually attempted yet.
4. Read the candidate from the QA artifact at `qa.bug_candidates`, not from conversation history. It was persisted precisely so this handoff survives compaction and a fresh session.
5. Build the `## QA Bug Context` section per `qa-workflow.md` §4 and add it to the `bug-investigator` dispatch. Apply the anti-anchoring rule in §5 there: `suspected_service` travels only with its `suspicion_basis`, labelled a hint, or is omitted entirely.
6. Everything else about DEBUG is unchanged — the investigator still owns its Feedback Loop Gate, and the seeded loop only satisfies that gate **after the investigator personally observes it go red**.

**On completion**, the router MAY offer to re-run the originating QA scenario via `re-qa-execute` against the harness from `source_wf` (see `qa-workflow.md` §6). A unit regression test proves the root cause is fixed; re-running the E2E scenario proves the user-visible symptom is gone. Only the second closes what QA opened.

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
