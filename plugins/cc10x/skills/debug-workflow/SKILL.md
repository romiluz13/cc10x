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

## Output Format (REQUIRED)
Return a debugging report:

1) Executive Summary (root cause; fix status)
2) Reproduction (steps, environment, error messages)
3) Investigation Timeline (logs, hypotheses, experiments)
4) Fix & Regression Test (what changed; tests added; GREEN proof)
5) Reviews & Integration (findings; integration scenarios pass/fail)
6) Verification Summary (commands → exit codes; artefacts)
7) Prevention & Follow-ups (monitoring, guards, debt)
