# Enforced Seam Gate in the Builder Contract

Sub-project 2a made the seam gate enforced via the existing contract-override
mechanism: the builder's Router Contract now carries `TEST_SEAMS` and
`SEAM_GATE_STATUS` (confirmed | proposed | disagreed | not_applicable), and
the router validates these per `build_scope`. Sub-project 1 shipped the gate
as advisory (TEST_SEAMS in DECISIONS only) because enforcing it required
router/contract schema changes, which were deferred to avoid touching the
load-bearing layer in the same commit as the payload swap.

## Context

Matt Pocock's `tdd` skill makes "test only at pre-agreed seams" a first-class
discipline. cc10x's builder previously had no seam field in its contract —
the verifier caught tautological/implementation-coupled tests at verify-time,
but the builder had no enforced step to declare which seam it tested at. The
question was whether to enforce the gate (contract fields + router validation)
or keep it advisory (builder records seams in DECISIONS, verifier checks
behavior).

## Decision

Enforce the gate via the existing contract-override mechanism — no new gate
kind, no new hook. The builder declares `TEST_SEAMS` + `SEAM_GATE_STATUS`;
the router validates per `build_scope`:

- standard + plan with `test_seams` → confirmed (used plan's seams) or
  disagreed (better seam + rationale, OR ambiguity block)
- standard + legacy plan (no `test_seams`) → proposed (builder proposes at
  BUILD_PREFLIGHT) — legacy fallback so pre-2a plans don't break
- direct/no-plan → proposed
- trivial → not_applicable

`disagreed` with empty `TEST_SEAMS` is only valid as the genuine-ambiguity
block (`STATUS=FAIL` + the exact `REMEDIATION_REASON`). This prevents a
builder from rubber-stamping `disagreed` to skip the gate.

## Rejected alternatives

- **Keep it advisory (sub-project 1 state).** Rejected: the verifier catching
  bad tests at verify-time is late; the builder should declare its seams at
  BUILD_PREFLIGHT so the verifier can confirm the test exercised the declared
  seam. Advisory meant a builder could skip declaring seams with no enforceable
  consequence.
- **A new gate kind / hook.** Rejected: the contract-override mechanism already
  validates the builder contract; adding a seam-specific gate would duplicate
  the validation surface and increase router complexity. Reusing the existing
  mechanism keeps the change minimal and the router graph untouched.

## Consequences

- Pre-2a saved plans whose phases omit `test_seams` are accepted via the
  `proposed` legacy fallback; the next plan-save backfills `test_seams`.
- The `build-happy-path` and `build-phase-blocked` fixtures now carry the new
  fields; `validate_builder_contract` enforces them (backward-compat: fixtures
  predating the fields are still accepted when the fields are absent).
- The `disagreed` + empty + FAIL + ambiguity-reason path is the ONLY way to
  block on seam ambiguity; any other empty-seam disagreed is rejected.
