# CC10X Verifier Latency Model

## Summary

This document defines the safe optimization boundary for BUILD -> review -> hunt -> verify latency work.

The goal is not to weaken verification. The goal is to separate:
- proof work that must never be removed
- duplicated work that may be narrowed only with evidence
- deeper audit work that can eventually become trigger-based

This model complements [router-invariants.md](/Users/rom.iluz/Dev/cc10x_v5/cc10x/docs/router-invariants.md). It does not replace it.

## Non-Negotiable Invariants

Any latency reduction must preserve:
- `INV-016` BUILD advances only through phase exit
- `INV-019` verifier remains independent from builder/reviewer/hunter approval
- `INV-020` hunter reports scan scope truthfully
- `INV-022` spec gate remains blocking
- `INV-023` proof status remains the phase completion gate

## Verifier Work Buckets

### `must_keep_core`

This is the minimum proof required before phase exit:
- truths verification
- artifacts verification
- wiring verification
- scenario accounting
- evidence reconciliation
- one fresh proof path for the claimed phase outcome
- contradiction detection against prior findings

This bucket must never weaken in prompt-only or latency-only changes.

### `candidate_duplicate`

This is work that may overlap with upstream agents and therefore needs measurement:
- repeated checks already fully proven by builder or reviewer
- repeated scans whose evidence is already carried forward in structured form
- repeated generic checks that do not change the phase-exit decision

Items in this bucket may only be reduced if:
- timing data shows real cost
- replay/evals show no trust regression
- the remaining verifier still proves the phase independently

### `triggered_deep_checks`

This is heavier audit work that adds confidence but may not be proportional on every phase:
- broad stub sweeps
- broad auth / retry / wiring sweeps
- repo-wide pattern scans outside the changed scope
- extra blast-radius checks beyond the current phase-exit claim

These checks may become conditional only when:
- the trigger is explicit and conservative
- the workflow remains fail-closed if proof is incomplete
- critical-path work still runs full rigor

## Operating Model

### `phase_exit_proof`

This is the minimum verifier scope required to let a phase advance.

It must answer:
- what must be true
- what must exist
- what must be wired
- whether scenario totals reconcile
- whether any contradiction remains unresolved

### `extended_audit`

This is additional verification work beyond the minimum phase-exit proof.

For now, CC10X should classify this work separately for telemetry. It should not silently drop it without measurement and replay coverage.

## Measurement Contract

Telemetry is informational only. It must not change routing or approval behavior.

Telemetry should capture:
- per-agent wall-clock time
- re-review / re-hunt / re-verify loop counts
- verifier workload split:
  - tests
  - build
  - scan
  - reconcile
  - reasoning/report
- whether the verifier work performed was:
  - `phase_exit_proof`
  - `extended_audit`

If any timing source is unavailable, record `unknown` rather than inventing numbers.

## Release Gate For Latency Work

Before merging any latency reduction:
- collect before/after timing on the same scenarios
- keep replay checks green
- review changes explicitly against `INV-016`, `INV-019`, `INV-020`, `INV-022`, `INV-023`
- record what changed, why it was low-yield, and why trust did not regress

If a proposed reduction cannot be explained in those terms, it should not ship.
