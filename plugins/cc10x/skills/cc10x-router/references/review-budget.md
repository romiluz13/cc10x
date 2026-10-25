# Review budget protocol

This is the canonical parent-side dispatch policy for every route, child and
substantive inline equivalent. Pending graph nodes cost nothing. Before starting
work, reserve it through `scripts/cc10x_review_budget.py`; only an allowed,
persisted reservation permits dispatch. Children never write budget state.
Existing quality, scope, research, QA and approval gates still apply.

## Accounting and continuity

A **lineage** is one independent user request, including related continuations.
A **subject** is the stable artifact/guarantees being reviewed across phases.
An **attempt** is an invocation, including a failed start. A **node** is its
approved logical graph slot; changing task names does not create a new node.

Default policy: 32 aggregate work units; each ordinary invocation reserves one,
each planner reserves four including its three inline spec-gate iterations.
Charges never refund. Invalid/cancelled/lost reviews earn no valid review credit.
Valid FINDINGS counts as a valid review. Unknown measurements stay null, with
availability `unknown` or `partial`; units are a fallback, not token or money metering.

Per-subject checkpoints: two valid fresh reviews, three attempted amendments,
three created remediation waves, four valid code reviews. Unresolved fresh/code
reviews hold slots; invalid/cancelled/lost completion releases only their slot.
Amendment/remediation slots count attempts and never release. Hunter/verifier
calls spend units without a separate lane limit. Two phase reviews plus three
repair reviews need five slots: configure five initially with recorded authority,
or obtain a lane-only grant for the fifth. Neither resets spending.

PLAN→BUILD, REVIEW→BUILD, QA→DEBUG, clarification, retries and related worktrees
retain lineage, subject and source ledger. A genuinely different subject needs
recorded scope rationale and still shares lineage units. Preserve QA `source_wf`;
budget membership separately uses `source_workflow_uuid`.

## CLI and storage

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc10x_review_budget.py" --state-root /workspace/sample/.cc10x --workflow /workspace/sample/.cc10x/workflows/wf-a.json --request /tmp/budget-request.json
```

The request is a JSON object. `init` takes `lineage_id`, `subject_id`, optional
finite `policy`, and explicit `migration` evidence for historical work. `join`
takes `source_workflow` (the actual source workflow path).
`join` may specify a distinct `subject_id` only with content-digested
`subject_rationale={ref,digest}` backed by the parent's approved scope decision.
This changes no lineage funds or grant rights. `inspect` and
`reconcile` are read-only. `reserve`, `finish`, `checkpoint`, `extend`, `finding`
take the matching event payload defined by the module's typed event union.
Exit 0 means allowed/consistent; 2 means blocked; 3 means invalid schema/I/O.
Output contains `status`, `reasons`, `projection`, `ledger_revision`.
Reservation output also includes request-specific `eligible_units`, its persisted
`reservation`, and `dispatch: new|resume`; `resume` never authorizes another copy.

The v1 projection carries `version`, `lineage_id`, `ledger_path`, `subject_id`,
`ledger_revision`, `charged_units`, `remaining_units`, and `counts` with aggregate
`attempts` plus subject `fresh_valid`, `amendment_valid`, `code_review_valid`,
`remediation_attempts`. Ledger v1 carries `version`, `lineage_id`, `revision`,
`event_count`, immutable `policy`/`opening`, append-only `members` and typed
`events`. Opening counts are keyed by subject, including `amendment_attempts`
when known. The module's `Reserved`, `Finished`, `Checkpoint`, `Extension` and
`Finding` TypedDicts define event payload fields; event IDs are idempotency keys.
Migration reconciles observed artifact/companion-log lower bounds and records
deduplicated imported IDs in optional immutable `opening.evidence_attempt_ids`.
Only those old receipts are recognized; later unledgered attempts still conflict.
History rows linking an attempt ID and cycle number make them aliases of one
repair round across all receipt sources. Disjoint rounds remain distinct;
contradictory attempt/cycle links block accounting.
Empty nested result placeholders are not historical work. Failed ledger writes
return invalid without dispatch authorization, even when recovery finds a charge
already committed; inspect/reconcile before continuing.

`--state-root` is the actual `.cc10x` directory: append no extra `.cc10x`.
The ledger lives at its resolved `budgets/{lineage_id}.json`. Every v1
`review_budget.ledger_path` is absolute and canonical. Joining a different root
retains the source ledger's path, including symlink resolution; never rebase it.
The helper alone writes the ledger, using atomic replacement and a sibling
POSIX lock with a five-second bound. This is the narrow exception to the ban on
shell-written orchestration state; it never writes workflow artifacts.

Write ledger first, then use normal artifact tools to copy the returned projection
to `review_budget`. Append event/attempt references to the existing workflow log.
A crash between writes retains the debit. Reconcile and persist the projection
before new dispatch. A higher count, missing ledger, unledgered task/event,
conflicting identity or corrupt sequence is an accounting conflict, not a reset.
If initialization committed the ledger but the workflow projection is absent,
retry `init` with the original `lineage_id` and `subject_id` in the original state
root. Under the ledger lock it checks lineage, membership, subject and current
artifact/log evidence, then returns the existing projection without writing the
ledger. Recovery ignores requested policy/migration overrides; no revision,
charge, event, membership or funding changes. Copy the returned projection before
ordinary inspect/reconcile or dispatch. For an interrupted cross-root join, retry
`join` with the original source workflow instead.
Revision counts transactions including joins; event seq counts typed events only.
Idempotent replay changes neither. Never equate revision with event_count.

Legacy absent/null fields remain readable, especially completed workflows and
unrelated edits. Before resuming work, import complete corroborated history once
as immutable `opening` with deduplicated IDs and conservative planner costs.
Unknown history consumes the base allowance and retains `coverage: unknown`;
only an authorized finite grant can continue it. Unknown metrics on an otherwise
complete v1 ledger do not imply unknown invocation history. Ambiguous unfinished
legacy node mapping blocks. Never synthesize a fresh PASS from scalar counts.

An imported historical `planning_review_status: passed` is provenance, not a new
ledger fresh PASS. When that is the sole unresolved check, `init` (including
retry recovery) persists/returns the accounting projection with exit 2 and
`fresh_pass_required`. Copy this projection even though closure is blocked;
preserve the historical status, revisions, decisions and receipts. Stale-mirror
`reconcile` also returns the current projection without claiming closure.
For an imported opening with source references, this single reason permits only
checkpoints, finite grants scoped exclusively to `fresh`, fresh review
reservations, and completion of those fresh attempts. All normal identity,
scope, input/proof, funding and lane checks still apply. Exhausted funds/slots
need an applicable scoped grant; historical permissions are not new grants.
Bind `plan_input_digest` to the actual current review input before dispatch.
While the unsupported historical passed claim is current, ordinary work,
amendment reviews and joins stay blocked; inspect/replay report the closure
failure. Only a genuine current fresh PASS satisfies passed closure.

After an actual role-valid fresh FINDINGS for the current revision/input, first
persist its immutable finish and projection. Preserve historical approval,
decisions and receipts in existing `status_history`/result evidence; then set
the current `planning_review_status=findings_received`, current findings and
reviewed revision/input binding. Re-ingestion must be idempotent. A crash before
that status update retains the closure conflict and restricted admission;
recover from the recorded finish. Once honestly `findings_received`, scoped
planner/repair work can use existing finite grants and reservation checks.
After editing use `revised_after_review`; BUILD approval still needs current
fresh PASS. Accounting consistency is not approval. Never clear passed to evade
proof acquisition or use invalid, amendment or stale results for this transition.

## Dispatch and result ingestion

1. Read the exact workflow, ledger, current tasks and event evidence. Resolve
   semantic continuity before `init`; new workflow identity never means new funds.
2. Build `node_descriptor={lineage_id,subject_id,step_key,phase_id,role,source_id,repository_id}`.
   Include explicit nulls and hash sorted-key, compact UTF-8 JSON with SHA-256.
   `step_key` is the approved graph slot, not a display name or retry ordinal.
   Verify source/repository IDs against the existing QA inventory; fingerprint
   the relevant graph/inventory row in `input_refs`. Distinct siblings retain
   distinct node IDs even in the same phase/role. Dependencies use frozen node IDs.
3. Derive lane from role/mode/approved graph: fresh/amendment plan review,
   code_review, remediation for REM-FIX, otherwise work. Hash the canonical input
   descriptor from relevant content digests, scope, decisions, proof/diagnostics,
   role and actual controllable model selection. Sort findings/references;
   timestamps, task/attempt/parent/grant IDs and unsupported model claims cannot
   change input. Static corrective instructions are `input_refs`, never fake runs.
   The exact hash envelope is `{scope_digest,role,input_refs}` using sorted-key,
   compact UTF-8 JSON; sort refs by `(ref,digest)`. Put content, decisions, proof
   inputs and actual model-selection evidence in those content-digested refs.
4. Reserve distinct siblings serially, persist each projection, then launch the
   allowed set in parallel only when the route permits. Invalid or ineligible
   reservations launch nothing. An existing reservation is recovery information,
   never permission to launch a duplicate. Recover its known execution/result,
   or finish it lost before a changed-input retry. A provably unstarted attempt
   may launch once after current input/scope/authority revalidation; otherwise
   cancel without refund. A child always needs its own reservation.
5. Validate the existing role contract before `finish`. Record invalid, cancelled
   or lost outcomes too. Persist the exact reviewed input, mode, revision, verdict,
   contract ref/digest and checked evidence refs. Parent owns attempt IDs; no new
   mandatory envelope key is added to every agent. Set `planning_review_runs`
   from the subject's fresh-valid projection, not an independent increment.

Fresh dispatch receives original request, current plan/code, approved decisions
and opaque attempt/input identifiers only: no prior findings, budget pressure,
progress labels or planner confidence. Amendment receives accepted findings and
the intended diff only. Amendment PASS never sets `last_reviewed_revision` or
whole-plan approval. v1 closure also requires `plan_input_digest` matching an
actual valid fresh PASS for the current revision. Exhaustion is not closure.

## Progress, proof and finite extensions

Before a retry/re-review, every cap, or a second reopening of an invariant,
record a cheap parent checkpoint using existing evidence: changes, improved
proof/findings, reopenings, scope changes and remaining units. No meta-reviewer.
Unchanged input or no verified progress stops. For retry name the latest attempt
in `retry_of`; an unresolved same-node attempt blocks even if input changed.

Execution `proof_refs` bind ref/digest/input_digest to producer attempt, node and
subject, matching its valid completion's `evidence_refs`. The producer must be
the prior node or a declared dependency. Preserve exact covering tests, command,
output and current tested revision; dispute-only and QA keep their existing proof
contracts. A sibling's proof is not interchangeable. Proof transfers no funding.

For a malformed role contract only, an optional v1 checkpoint member admits one
instruction correction per same-node `retry_of` chain:
`contract_correction={invalid_attempt_id,instruction:{ref,digest}}`. Omit it for
ordinary retries; null, incomplete objects and extra nested keys are invalid.
The latest same-node attempt must have a terminal invalid finish with validated
`contract_ref`/`contract_digest` for the raw malformed output. Diagnose the missing
contract requirement in the parent rationale, and put that receipt pair plus the
instruction pair in `changed_input_refs`. Neither is execution proof.

Name that exact invalid attempt in `retry_of`. Preserve node, subject, lane,
scope and dependency IDs; retain every prior input pair and add exactly the
named, previously absent instruction pair. The instruction supplies only the
missing contract requirement. Raw malformed output and prior findings stay out
of fresh reviewer input. Parent checks semantic narrowness and proof relevance.
Use a matching `continue` checkpoint with non-none progress and safe scope;
reservation requires ledger revision = observed_revision + 1. Obtain grants
before this checkpoint; any intervening mutation stales it.

Retain all proof refs from the invalid attempt's prior checkpoint and validate
their producer/dependency/digest and current relevance normally. Only an invalid
initial review without inherited proof obligation may use empty proofs. Ordinary
retries, valid findings, cancellation and loss still need covering proof. A second
malformed result cannot reuse the exception, even with a different instruction.
Reserve and charge normally; invalid results refund nothing and earn no review
credit. Fresh/code invalid results release only held review slots; amendment
attempts stay consumed. Existing stricter retry caps remain. Bind the corrected
current plan input before fresh dispatch: an old-input PASS cannot close it.

At a finite boundary, eligible progress produces `needs_authorization`; without
applicable recorded authority, stop with one finite proposal. Existing standing
authority may fund repeated finite grants without asking again. Each grant needs
a distinct current checkpoint (ledger revision = observed_revision + 1), scope,
authority evidence and grant ID. A single-use authority cannot fund twice.
Default maximum per grant is eight units and +1 per applicable lane; units-only
and lane-only grants are independent. At least one increment must be positive.
Duplicate identical grant IDs are no-ops; conflicting, stale or consumed grants fail.
For v1 this checkpoint decision governs continuation beyond the default local
caps in route references; those counters are projections, not an additional
approval question. Create authorized extra fresh-review graph slots on demand.
Record `attempt_id` and stable `finding_ids` in each new remediation-history row.

Units remain separate sources: base first, then eligible grants by sequence.
Eligibility requires exact subject/scope/lane plus current affirmative
`authorization_checks` with evidence ref/digest. Apply the same checks to lane
slots independently. Insufficient eligible funds/slots rejects atomically even
when aggregate remaining units are positive. Parent pointers do not inherit
authority. Recheck revocation before consumption/launch; never erase prior debits.

Batch all available review/hunt findings in one wave into one repair. Parent
assigns stable finding IDs with source provenance and aliases for renamed
summaries. Preserve positional dispute→finding-ID maps; incomplete adjudication
stays blocking. Matching in-flight disputes create no repair. Upheld findings
need changed evidence to reopen; ambiguous identity stays explicitly open.
Repeated invariants without verified progress require diagnosis, never a free retry.

Ordinary feedback and test consolidation may proceed within allowance as
`implementation`/`test_allocation` when requirement→proof mapping preserves every
unique assertion. Removed regression proof blocks. Architecture/product/security
changes or contradictory guarantees require the existing operator gate. Comments,
amendments and scope labels neither grant authority nor replenish budgets.

## Enforcement boundary

The CLI validates local accounting, structural proof bindings and reservations;
replay uses the same validator. The hook only audits budget conflicts after a
write, preserving its existing corruption/closure signals. The router still owns
semantic graph authority, current evidence relevance, external authorization and
actual invocation. Local POSIX locking is not distributed scheduling. Coordinated
erasure of all evidence cannot be detected; arbitrary harness calls cannot be
intercepted. This bounds conforming-router invocation volume, not provider cost.
