# Planning Recovery Note

## Goal

Recover the best planning strengths from `cc10x-v7`, `metaswarm`, and `get-shit-done` without touching router semantics or weakening agreement-first safety.

## What Changed

- Planner now requires a code-grounded final pass for non-trivial work.
- Non-trivial plans must surface:
  - `Codebase Reality Check`
  - `Plan-vs-Code Gaps`
  - `Assumption Ledger`
  - `Phase Dependency Map`
- Planner output is split into a short human layer and a stricter execution contract layer.
- Plan review is now more explicitly repo-grounded, not just structurally adversarial.
- Planning replay coverage now includes:
  - repo-alignment preservation
  - contradiction-to-clarification behavior

## Sources Stolen From

- `cc10x-v7`
  - first-draft decisiveness
  - readable top-level planning UX
  - explicit confidence and input-needed framing
- `metaswarm`
  - fail-closed adversarial review language
  - “repo-wrong plan is fail” posture
- `get-shit-done`
  - plan as execution contract
  - stronger phase dependency and scope-drift language

## Honest Claim Boundary

This round improves planning quality and planning-specific audits, but it does not change router selection, BUILD topology, approvals, or verifier gating.
It is a planning recovery round, not an orchestration redesign.
