name: feature-planning
description: Provides guidance for gathering requirements, analysing architecture, and preparing implementation plans. Used by the planning workflow and related subagents.
allowed-tools: Read, Grep, Glob
---

# Feature Planning Guidance

## Purpose
Support the planning workflow with structured templates for requirements, architecture, risks, testing, and implementation phases.

## Usage Overview
1. **Assess Complexity**
   - Use the orchestrator's Complexity Rubric (1-5). If score <=2, confirm before proceeding.
2. **Capture Requirements**
   - Document stakeholders, user stories, acceptance criteria, assumptions, and open questions.
3. **Design Architecture**
   - Create system context, container, and component views.
   - Specify data models, interfaces, and integration points.
4. **Evaluate Risks**
   - Use the seven-stage framework from `risk-analysis` (data flow, dependencies, timing, UX, security, performance, failure modes).
5. **Plan Implementation**
   - Produce file manifest, phased roadmap, testing strategy, deployment and rollback steps.

## Templates
### Requirements Block
```
## Requirements
- Goal: <summary>
- User Stories:
  - As a <role>, I want <behaviour> so that <outcome>.
- Acceptance Criteria: <list>
- Assumptions: <list>
- Questions: <list>
```

### Architecture Block
```
## Architecture
- System Context: <text diagram>
- Containers: <services/data stores>
- Components: <responsibilities + boundaries>
- Data Models: <entities and relationships>
```

### Risk Register
```
## Risks
| Stage | Description | Probability | Impact | Mitigation | Owner |
|-------|-------------|-------------|--------|------------|-------|
```

### Implementation Roadmap
```
## Implementation Plan
Phase 1: <summary>
- Files: <list>
- Tests: <planned tests>
- Exit Criteria: <definition>
```

## Verification Reminder
Always end with a verification summary noting inputs reviewed, outstanding questions, and follow-up tasks.

## How to Fill the Templates (Guidance)
- Requirements: Make user stories testable; add concrete acceptance criteria and assumptions.
- Architecture: Prefer simple boundaries; list key decisions with trade-offs and risks.
- Risks: Rate probability/impact; tie each risk to a requirement or decision; propose mitigations.
- Implementation: Produce a minimal file manifest and a phased roadmap; note dependencies.

## References
- Skill structure: `docs/reference/04-SKILLS.md`
- Risk framework: `plugins/cc10x/skills/risk-analysis/SKILL.md`
