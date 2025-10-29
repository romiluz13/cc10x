---
name: build-workflow
description: Coordinates feature implementation via TDD, review, and integration verification. Loads shared skills and invokes component-builder, code-reviewer, and integration-verifier sequentially.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Build Workflow

TDD-driven implementation with review and integration verification.

## Process
For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/build.md`.

## Quick Reference
- Gate: use orchestrator Complexity Rubric; confirm if score <=2
- Loop: RED -> GREEN -> REFACTOR; capture verification outputs
- Subagents: component-builder -> code-reviewer -> integration-verifier (sequential)

## Output Format (REQUIRED)
Return an implementation report:

1) Executive Summary (components implemented; status)
2) Component Breakdown
   - For each component: TDD cycle summary (RED/GREEN/REFACTOR), key diffs
3) Reviews & Integration
   - code-reviewer findings (resolved/open)
   - integration-verifier scenarios (pass/fail with logs)
4) Verification Summary (commands → exit codes; coverage if applicable)
5) Follow-ups / Tech Debt / Next Steps
