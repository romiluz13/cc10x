# Build Process Folder Structure - Complete Specification

## Root Location

```
.claude/build-process/
├── requirements/     # WHAT we're building
├── decisions/        # WHY this approach
├── progress/         # WHERE we are now
├── learnings/        # WHAT we discovered
└── context/          # HOW things connect
```

## 1. requirements/ - The WHAT

**Purpose**: Store all requirements, user stories, and constraints. This folder answers "What are we building and why?"

### Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `REQUIREMENTS.md` | Master requirements document | At project start, major changes |
| `user-stories.md` | User stories with acceptance criteria | When stories added/changed |
| `constraints.md` | Business and technical constraints | When constraints discovered |
| `scope.md` | What's in scope vs out of scope | When scope changes |
| `stakeholders.md` | Who cares about this project | At project start |

### REQUIREMENTS.md Template

```markdown
# Project Requirements

## Overview
[Brief project description]

## Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

## Non-Functional Requirements
- Performance: [requirements]
- Security: [requirements]
- Accessibility: [requirements]
- Scalability: [requirements]

## Timeline
- Start: [date]
- Target completion: [date]
- Milestones: [list]
```

### user-stories.md Template

```markdown
# User Stories

## Epic: [Epic Name]

### US-001: [Story Title]
**As a** [user type]
**I want** [action]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

**Priority**: [High/Medium/Low]
**Status**: [Not Started/In Progress/Done]

---

### US-002: [Story Title]
[Same format]
```

### constraints.md Template

```markdown
# Project Constraints

## Technical Constraints
- [Constraint with rationale]
- [Constraint with rationale]

## Business Constraints
- [Constraint with rationale]
- [Constraint with rationale]

## Resource Constraints
- [Constraint with rationale]

## External Dependencies
- [Dependency and its constraints]
```

## 2. decisions/ - The WHY

**Purpose**: Store all decisions with their rationale. This folder answers "Why did we choose this approach?"

### Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `DECISIONS-INDEX.md` | Quick reference of all decisions | After each ADR |
| `ADR-001-*.md` | Individual Architecture Decision Records | When decisions made |
| `tech-stack.md` | Technology choices with rationale | At project start, tech changes |
| `rejected-approaches.md` | What we tried and why it failed | When approaches rejected |
| `trade-offs.md` | Explicit trade-off analysis | When trade-offs identified |

### DECISIONS-INDEX.md Template

```markdown
# Decisions Index

| ID | Decision | Date | Status |
|----|----------|------|--------|
| ADR-001 | [Title] | YYYY-MM-DD | Accepted |
| ADR-002 | [Title] | YYYY-MM-DD | Superseded by ADR-003 |

## Quick Reference
- **Database**: [choice] - ADR-001
- **Framework**: [choice] - ADR-002
- **Authentication**: [choice] - ADR-003
```

### ADR Template (ADR-XXX-title.md)

```markdown
# ADR-XXX: [Title]

## Status
[Proposed/Accepted/Deprecated/Superseded]

## Context
[What is the issue that we're seeing that is motivating this decision?]

## Decision
[What is the change that we're proposing and/or doing?]

## Consequences
### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

### Neutral
- [Implication 1]

## Alternatives Considered
1. **[Alternative 1]**: [Why rejected]
2. **[Alternative 2]**: [Why rejected]
```

### rejected-approaches.md Template

```markdown
# Rejected Approaches

## [Approach Name]
**Date Rejected**: YYYY-MM-DD
**Context**: [What problem we were trying to solve]
**Approach**: [What we tried]
**Why Rejected**: [Specific reasons]
**Lessons Learned**: [What we learned]

---

## [Another Approach]
[Same format]
```

## 3. progress/ - The WHERE

**Purpose**: Store current status, progress, and next steps. This folder answers "Where are we right now?"

### Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `STATUS.md` | Current overall status | Every session |
| `NEXT-STEPS.md` | Prioritized next actions | Every session |
| `completed.md` | What's done with evidence | After completions |
| `in-progress.md` | What's being worked on | During work |
| `blockers.md` | Current blockers and status | When blockers change |
| `milestones.md` | Project milestones | After milestones |

### STATUS.md Template (MOST CRITICAL)

```markdown
## Current State
[One sentence: what's happening right now]

## Last Session
- Date: [YYYY-MM-DD HH:MM]
- What was done: [2-3 bullet summary]
- Exit state: [clean/in-progress/blocked]

## Active Work
- Component: [name or "none"]
- Phase: [workflow phase]
- Status: [status description]

## Critical Context
- [Key fact 1 that AI must know]
- [Key fact 2 that AI must know]
- [Key fact 3 that AI must know]

## Blockers
[None / list of blockers with status]
```

### NEXT-STEPS.md Template

```markdown
## Immediate (Do First)
1. [Highest priority action with context]
2. [Second priority action with context]

## Soon (After Immediate)
- [Action]: [context/notes]
- [Action]: [context/notes]

## Later (When Time Permits)
- [Future action]

## Dependencies
- [Action X] depends on [Action Y]
- [Action A] blocked by [Blocker B]
```

### completed.md Template

```markdown
# Completed Work

## [Date: YYYY-MM-DD]

### [Component/Feature Name]
- **What**: [Description]
- **Evidence**: [Test results, file:line, exit codes]
- **Files Changed**:
  - `path/to/file` - [what changed]
- **Tests**: [X] tests passing
- **Notes**: [Any important notes]

---

## [Earlier Date]
[Same format]
```

### in-progress.md Template

```markdown
# In-Progress Work

## [Component/Feature Name]
- **Started**: [YYYY-MM-DD]
- **Current Phase**: [phase name]
- **Last Action**: [what was done last]
- **Next Action**: [what to do next]
- **Files Touched**:
  - `path/to/file` - [status]
- **Blockers**: [none / list]
- **Context**: [any important context for continuing]
```

### blockers.md Template

```markdown
# Current Blockers

## Active Blockers

### [Blocker Title]
- **Type**: [Technical/External/Resource/Decision]
- **Blocking**: [What work is blocked]
- **Since**: [Date discovered]
- **Status**: [Investigating/Waiting/Escalated]
- **Next Action**: [What's being done]
- **Owner**: [Who's responsible]

## Resolved Blockers

### [Resolved Blocker]
- **Resolved**: [Date]
- **Resolution**: [How it was resolved]
```

## 4. learnings/ - The WHAT WE DISCOVERED

**Purpose**: Store all learnings, patterns, and gotchas. This folder answers "What have we learned?"

### Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `LEARNINGS-INDEX.md` | Quick reference of learnings | After new learnings |
| `patterns.md` | Codebase patterns discovered | When patterns found |
| `gotchas.md` | Pitfalls to avoid | When gotchas discovered |
| `solutions.md` | Working solutions | After solutions found |
| `failures.md` | What didn't work | After failures |

### patterns.md Template

```markdown
# Codebase Patterns

## Component Patterns

### [Pattern Name]
**Location**: `path/to/example`
**Use When**: [When to use this pattern]
**Example**:
```[language]
[code example]
```
**Notes**: [Important notes]

## API Patterns

### [Pattern Name]
[Same structure]

## Testing Patterns

### [Pattern Name]
[Same structure]
```

### gotchas.md Template

```markdown
# Gotchas and Pitfalls

## [Category]

### [Gotcha Title]
**Symptom**: [What you'll see]
**Cause**: [Why it happens]
**Solution**: [How to fix/avoid]
**Example**:
```
[code or command showing the gotcha]
```

---

### [Another Gotcha]
[Same format]
```

### solutions.md Template

```markdown
# Working Solutions

## [Problem Category]

### [Problem Description]
**Context**: [When you encounter this]
**Solution**:
```[language]
[working code]
```
**Why It Works**: [Explanation]
**Alternatives Tried**: [What didn't work]
```

## 5. context/ - The HOW

**Purpose**: Store project structure and relationships. This folder answers "How does everything connect?"

### Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CONTEXT-SNAPSHOT.md` | Single-page project overview | Every major change |
| `architecture.md` | System architecture | When architecture changes |
| `file-map.md` | Key files and purposes | When key files change |
| `dependencies.md` | External dependencies | When deps change |
| `apis.md` | API contracts | When APIs change |

### CONTEXT-SNAPSHOT.md Template

```markdown
## Project
[One paragraph: what this project is and its purpose]

## Tech Stack
- Language: [language and version]
- Framework: [framework and version]
- Key Libraries: [list with versions]

## Architecture
[Brief architecture description - how components connect]

## Key Files
- `path/to/file` - [purpose]
- `path/to/file` - [purpose]
- `path/to/file` - [purpose]

## Current Focus
[What area of codebase is being worked on]

## Quick Commands
- Build: `[command]`
- Test: `[command]`
- Run: `[command]`
```

### architecture.md Template

```markdown
# System Architecture

## Overview
[High-level architecture description]

## Components

### [Component Name]
- **Purpose**: [What it does]
- **Location**: `path/to/component`
- **Depends On**: [Other components]
- **Depended On By**: [Components that use it]

## Data Flow
[Description of how data flows through the system]

## External Integrations
- **[Service Name]**: [How it integrates]

## Diagrams
[ASCII diagrams or references to visual diagrams]
```

### file-map.md Template

```markdown
# Key Files Map

## Entry Points
- `path/to/main` - Application entry point
- `path/to/index` - Module entry point

## Configuration
- `path/to/config` - [What it configures]

## Core Logic
- `path/to/file` - [Purpose]

## Utilities
- `path/to/utils` - [Purpose]

## Tests
- `path/to/tests` - [What they test]
```

### dependencies.md Template

```markdown
# External Dependencies

## Production Dependencies

| Package | Version | Purpose | Notes |
|---------|---------|---------|-------|
| [name] | [version] | [why needed] | [important notes] |

## Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [name] | [version] | [why needed] |

## External Services

| Service | Purpose | Credentials Location |
|---------|---------|---------------------|
| [service] | [why needed] | [where creds stored] |
```

### apis.md Template

```markdown
# API Contracts

## Internal APIs

### [API Name]
**Endpoint**: `[path]`
**Method**: [GET/POST/etc]
**Purpose**: [What it does]

**Request**:
```json
{
  "field": "type"
}
```

**Response**:
```json
{
  "field": "type"
}
```

**Errors**:
- `[code]`: [meaning]

## External APIs

### [External Service API]
**Documentation**: [link]
**Key Endpoints Used**:
- `[endpoint]` - [purpose]
```
