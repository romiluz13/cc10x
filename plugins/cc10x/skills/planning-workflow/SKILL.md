---
name: planning-workflow
description: Coordinates the planning workflow by running requirements intake and planning subagents, then compiling a complete plan. Use when planning new features, architecting systems, designing APIs, or creating implementation roadmaps.
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

**MANDATORY TEMPLATE** - Use exact structure from orchestrator:

```markdown
# Planning Report

## Executive Summary
[2-3 sentences summarizing scope, constraints, goals, and overall plan status]

## Actions Taken
- Skills loaded: requirements-analysis, architecture-patterns, risk-analysis, api-design-patterns, component-design-patterns, deployment-patterns
- Subagents invoked: planning-architecture-risk, planning-design-deployment
- Inputs reviewed: [list]
- Tools used: [list]

## Findings / Decisions

### Requirements Overview
- Goals: [list]
- User Stories: [list with acceptance criteria]
- Stakeholders: [list]
- Constraints: [list]

### Architecture & Component Design
- System Context: [textual diagram]
- Container View: [components and responsibilities]
- Component Breakdown: [detailed components]
- Data Models: [tables, entities, relationships]

### API/Data Models
- Endpoints: [list with contracts]
- Data Models: [entities with fields]
- Integration Points: [external services, events]

### Risk Register
- Risk 1: [description] - Probability: [1-5] - Impact: [1-5] - Score: [P×I] - Mitigation: [action] - Owner: [role]

### Implementation Roadmap
- Phase 1: [components] - Dependencies: [list] - Files: [manifest]
- Phase 2: [components] - Dependencies: [list] - Files: [manifest]

### Testing & Deployment Strategy
- Unit Testing: [approach]
- Integration Testing: [approach]
- Deployment: [strategy, rollback plan]

## Verification Summary
Scope: <feature/system planned>
Inputs: <sources reviewed>
Decisions: <key architecture decisions with rationale>
Open Questions: <items awaiting user confirmation>
Implementability: <all checks passed or concerns flagged>

## Recommendations / Next Steps
[Prioritized: Critical decisions needed, then implementation phases]

## Open Questions / Assumptions
[If any conflicts detected, implementability concerns, or assumptions made]
```

**Validation Checklist**:
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes inputs, decisions, open questions
- [ ] All architecture decisions have rationale
- [ ] Risk register includes probability/impact scores
- [ ] File manifest and roadmap include dependencies
- [ ] Implementability checks documented
- [ ] Conflicts resolved or flagged
- [ ] All subagents/skills documented in Actions Taken
