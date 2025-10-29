---
name: build-workflow
description: Coordinates feature implementation via TDD, review, and integration verification. Loads shared skills and invokes component-builder, code-reviewer, and integration-verifier sequentially.
allowed-tools: Read, Grep, Glob
---

# Build Workflow

TDD-driven implementation with review and integration verification.

## Process
For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/build.md`.

## Quick Reference
- Gate: use orchestrator Complexity Rubric; confirm if score <=2
- Loop: RED -> GREEN -> REFACTOR; capture verification outputs
- Subagents: component-builder -> code-reviewer -> integration-verifier (sequential)
