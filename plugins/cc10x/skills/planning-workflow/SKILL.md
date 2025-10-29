---
name: planning-workflow
description: Coordinates the planning workflow by running requirements intake and planning subagents, then compiling a complete plan.
allowed-tools: Read, Grep, Glob, Task, Bash
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

## Output Format (REQUIRED)
Return a plan document with:

1) Executive Summary (scope, constraints, goals)
2) Requirements Overview (user stories, acceptance criteria)
3) Architecture & Component Design (views, responsibilities)
4) API/Data Models (tables, endpoints, contracts)
5) Risk Register (probability, impact, mitigation, owner)
6) Implementation Roadmap (phases, file manifest)
7) Testing & Deployment Strategy
8) Open Questions / Assumptions
