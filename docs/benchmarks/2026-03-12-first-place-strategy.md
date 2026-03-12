# CC10X First-Place Strategy

## Goal

Win on the thing that matters: helping Claude Code produce and maintain better code than the best harnesses in the reference set.

This strategy treats product quality as two linked layers:
- orchestration trust
- prompt engineering sharpness

The harness wins only if both are stronger together than the alternatives.

## Competition Thesis

CC10X should not try to become the biggest prompt zoo.
CC10X should become the strongest default trust harness:
- clearer planning modes than `metaswarm`
- stronger execution discipline than `get-shit-done`
- more durable recovery and replay than `babysitter`
- harsher anti-false-completion wording than `superpowers`
- cleaner centralized contracts than all of them

## Locked Product Bets

1. Router-owned planning modes:
   - `direct`
   - `execution_plan`
   - `decision_rfc`
2. Explicit verification rigor:
   - `standard`
   - `critical_path`
3. Hard spec gate before BUILD on non-trivial work.
4. Proof-oriented BUILD phase completion:
   - truths
   - artifacts
   - wiring
5. Durable traceability from requirement to remediation.

## Scorecard

| Dimension | Winning bar |
|-----------|-------------|
| Planning | `decision_rfc` handles broad choices without hidden defaults |
| Execution | No silent phase skipping, no success without proof |
| Verification | Fails closed on evidence mismatch |
| Recovery | Resume restores active phase, pending gates, and proof posture |
| Prompt quality | Shorter, sharper, more contractual, less aspirational |
| Competition proof | Replay fixtures + benchmark docs + honest claim boundaries |

## Current Implementation Focus

1. Spec gate and plan-mode discipline
2. Builder proof contract
3. Verifier truth/artifact/wiring reconciliation
4. Workflow traceability fields
5. Replay fixtures that encode the new rules

## Honest Claim Boundary

CC10X should claim superiority only where the repo can prove it with:
- contract audits
- replay fixtures
- benchmark notes
- manual comparative analysis

No “best in the world” claim is valid until those four layers point the same way.
