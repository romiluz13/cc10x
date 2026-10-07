# CC10x remediation: prompt change record (Phase 4)

One section per task. Classification for every task: `orchestration_sensitive` (ASM-7, authorized by the autonomous-build instruction). Checklist sections 3-4 (Tier 1): `harness_audit`, `workflow_replay_check`, manual semantic drift review, prompt diff review.

## P4.T1.1 `references/remediation-and-research.md`

Findings: B1, B6, B9 (part), B10 (part), A4 (part).

Files: `plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md`; new pins in `plugins/cc10x/tools/prompt_clause_assertions.py` (5 added).

What changed:
- Added `### REM-FIX TaskCreate template` (one literal call carrying the seven metadata lines, with a body that asks the fix agent for `COVERING_TESTS`, `TEST_COMMAND`, `TEST_OUTPUT`, or the dispute triple).
- Added `### Producers of the REM-FIX gate fields`: the remediating builder produces `COVERING_TESTS`/`TEST_COMMAND`/`TEST_OUTPUT` and `FINDING_DISPUTED`/`VERIFY_COMMAND`/`VERIFY_OUTPUT`; `integration-verifier` produces `DISPUTE_UPHELD`/`DISPUTE_REJECTED` (it was already named the adjudicator in the same file).
- Circuit breaker: the `### Circuit breaker` block is the single definition. The "Change-something" paragraph, Fix-wave consolidation and the Re-review loop step 1 and precondition-gate bullet now point at it. The Re-review loop no longer re-counts at REM-FIX completion; the limit is evaluated at creation only (plan: "one trigger point").
- Count semantics kept as the hooks implement them: the router counts `kind:remfix` tasks per `wf:` before creating one (ask at count >= 3); the guard counts `remediation_history` entries (appended at creation) and flags above 3. The plan text said "count completed REM-FIX tasks"; the hook counts created entries, so the hook version was kept (rule 4: pick the version enforced by hooks).
- "Hook-enforced backstop" relabeled "Audit backstop" and states the real behavior: `taskMetadata` ships as `audit` (log and stderr warning); it blocks only when set to `block`.
- Dead branches: removed "Legacy agent-created remediation tasks are still accepted" (no agent creates a REM-FIX; code-reviewer and failure-hunter say so) and "or on the re-reviewer for REVIEW" in the re-review loop (REVIEW never creates a REM-FIX per `review-workflow.md`; stated once in step 1).
- No dangling ADR or RFC references existed in this file, so none were changed (those live in `qa-workflow.md`, task T1.4).

Why safe: the number of allowed cycles (3), the ask-before-fourth rule, the artifact-authoritative tiebreak, the re-review precondition gate and its fail-closed rule, and verify-before-implement are unchanged. The guard code is untouched.

Claim boundary: now true: every gate field has a named producer and the router has a template that asks for it. Still not claimed: the agent contracts do not yet carry the fields (P4.T4.2/T4.3), and the shipped hook mode only warns.

Pins and fixtures: 5 new clause pins (template, producers, single circuit breaker, audit wording, unreachable branches). `remfix-gate.json` unchanged and green. No existing pin was edited or removed.

## P4.T1.2 `references/workflow-artifact-and-hook-policy.md` and `workflow-artifact.skeleton.json`

Findings: B7, B8, B10 (part), C2 (part), B14 (part).

Files: the policy reference; the skeleton; `plugins/cc10x/tools/workflow_replay_check.py` (new `CONVERGENCE_STATES`, enum check over every fixture, `build-happy-path` expectation); five fixtures migrated (`build-happy-path`, `build-doc-sync-happy-path`, `build-doc-sync-skipped`, `qa-route-happy-path`, `multi-phase-memory-finalize`: `stable` becomes `converged`); 12 new clause pins in `prompt_clause_assertions.py`.

What changed:
- Required-field tables: new "Read-only and advisory agent required fields" table with rows for `code-reviewer`, `failure-hunter`, `integration-verifier`, `triage-agent`, `architecture-scanner`, each copied from the keys in the agent's own YAML block (checked mechanically by a pin). `IMPLEMENTATIONS_FOUND` dropped from the researcher row (the agent emits `KEY_FINDINGS_COUNT`). Planner row gains `PLAN_REVISION`, `LAST_REVIEWED_REVISION` (the agent already emits both) and, on a `phase:qa-re-plan` return, `AMENDED_FILES`, `STALE_SWEEP`, `RECONCILIATION_RERUN` (addenda item 2; `qa-workflow.md` already fails the pass-2 gate without them, `planner.md` does not yet carry them: P4.T4.4 owns that, and the pin exempts exactly these three names until then).
- Parsing direction: one paragraph for every agent: the router branches on `STATUS` from the YAML block; envelope and heading are quick presence signals; the YAML block decides on disagreement. This follows the agent files ("the router branches on STATUS, it MUST appear in the YAML block"). Quoted from `agents/code-reviewer.md` and `agents/failure-hunter.md`, Output sections.
- `normalized_phases` names now match `build-workflow.md` BUILD preparation step 8 (`inputs`, `files/surfaces`, `expected_artifacts`, `required_checks`, `checkpoint_type`), keeping the identity keys `phase_id`/`title` that the replay fixture reads. `build-workflow.md` itself is untouched (T1.3).
- `plan_trust_gate`: one definition, pointing at the checks in `build-workflow.md` BUILD preparation step 3; the phantom `plan_trust` anchor is gone.
- `DIFF_DRIVEN_DOCS: skip`: stated as read from `activeContext.md ## Session Settings`, where the router reads it.
- `verification_rigor`: skeleton default `null`; policy states it must be set explicitly, and `plan_trust_gate` fails while it is null with a plan present.
- `CONVERGENCE_STATES` = pending, needs_iteration, converged, N/A. Values in use were pending, needs_iteration, stable, N/A, and the router prose (`SKILL.md` convergence row) says `converged`; `converged` was chosen because the router text names it and `SKILL.md` cannot be edited in this task, so `stable` (five fixtures) was migrated. `N/A` is kept for the two advisory routes.
- Event types: split into router-appended (`workflow_started`, `result_persisted`, `memory_finalized`, `inline_fallback_entered`), hook-appended (`compact_occurred`, `artifact_mutated`) and not emitted (`agent_started`, `agent_completed`, `contract_parsed`, `remediation_created`, `scope_decision_requested`, `scope_decision_resolved`); `workflow_completed`/`workflow_failed` described as terminal markers the QA guard accepts but no router step appends. Hook-log events (`subagent_stop`, `instructions_loaded`, `stop_failure`) are named as a separate log, and the StopFailure/InstructionsLoaded/SubagentStop bullets now say "hook log". The plan counted "six unemitted and seven unlisted"; verified counts: six unemitted router names, and seven unlisted emitted names once the three hook-log names are included with the four workflow-log ones.
- PostToolUse: "rejects" replaced with the documented behavior (exit 2 after the write, stderr to the model, malformed artifact stays on disk until repaired), matching the hooks README and guard docstring from P1.T10.
- Hooks key on the newest-mtime artifact (named guards), TaskCompleted keys on the task's `wf:`; `phase_exit_gate` is router-enforced and no hook checks it.
- Citation bounce (C4.2 default, floor unchanged): the "fewer than 3 file:line evidence citations" rule is kept verbatim and labelled a validity check that does not change the per-finding reporting floor. The agent half (its Zero-Finding Gate asks for one positive assertion and sets CONFIDENCE 70, which is below the router's three-citation bar) is for P4.T4.3, which must align the agent to this router text rather than the reverse, because lowering the router bar would weaken a fail-closed gate.

Why safe: no gate semantics changed. The three-citation rule, plan_trust checks, memory_sync and phase_exit semantics, the artifact guard behavior and the hooks are untouched; the new text describes behavior the hooks already have. The only behavior-adjacent edits are `verification_rigor` null (presence-only checks still pass; the explicit-set rule was already in `build-workflow.md` step 3) and the `converged` value, which is already what `SKILL.md` documents.

Claim boundary: now true: no two policy tables disagree on field names with the agent files (pin-checked); the event list says which names are live. Still not claimed: `SKILL.md` still says the skeleton "ships every required key already populated with safe defaults" and does not list `verification_rigor` among the fields the router fills (a T1.5 item, not edited here); `skills/diff-driven-docs/SKILL.md:171` still says the opt-out lives in `CLAUDE.md` (a skill-side fix, outside P4.T1.2; deferred to the P4C pass); the `planner.md` amendment-lane fields land in P4.T4.4.

Pins and fixtures: 12 new pins (assertion count 276: 259 at P4 start, plus 5 in T1.1, plus 12 here; floor 253 plus additions holds); five fixtures migrated; `build-happy-path` expected value moved to `converged` in the replay check. No existing pin was edited, weakened or removed.

Classification: `orchestration_sensitive`.
