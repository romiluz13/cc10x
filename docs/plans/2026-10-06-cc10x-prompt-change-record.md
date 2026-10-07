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
