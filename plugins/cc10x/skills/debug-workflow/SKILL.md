---
name: debug-workflow
description: Coordinates systematic debugging by loading investigation skills and delegating to bug-investigator, code-reviewer, and integration-verifier sequentially.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Debug Workflow

Systematic debugging with evidence-first verification.

## Process
For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/debug.md`.

## Quick Reference
- Intake: confirm repro, errors/logs, recent changes
- Loop: bug-investigator -> code-reviewer -> integration-verifier (sequential)
- Evidence: logs + failing test -> fix -> GREEN; include Verification Summary
