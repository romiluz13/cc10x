---
name: planning-workflow
description: Coordinates the planning workflow by running requirements intake and planning subagents, then compiling a complete plan.
allowed-tools: Read, Grep, Glob
---

# Planning Workflow

Coordinates structured planning and delegated analysis.

## Process
For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/plan.md`.

## Quick Reference
- Gate: use the orchestrator's Complexity Rubric; confirm if score <=2
- Intake: summarise goals, stories, acceptance criteria, assumptions
- Delegate: `planning-architecture-risk`, `planning-design-deployment`
- Output: consolidated plan + Verification Summary
