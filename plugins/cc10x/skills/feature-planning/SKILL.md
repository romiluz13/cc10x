---
name: feature-planning
description: Creates comprehensive PRD-style feature plans with user stories, architecture decisions, component breakdowns, API contracts, data models, edge cases, testing strategies, complexity assessment, file change manifests, and implementation roadmaps. Use for strategic planning before implementing complex features (4-5 complexity). Provides 5 progressive stages (requirements analysis, architecture design, risk assessment, complexity scoring with recommendations to skip if simple, and file manifest creation). Loaded by requirements-analyst and architect agents during PLANNING workflow. Particularly valuable for novel architectures, high-risk features, or when team alignment documentation needed. For simple features using well-documented libraries, recommend manual implementation instead (faster and more token-efficient).
license: MIT
---

# Feature Planning - Strategic Design Before Building

## Overview

Create comprehensive, actionable feature plans BEFORE any code is written. Generate persistent markdown checklists ready for `/feature-build` execution.

**Core principle:** "Plan twice, code once" - A great plan makes implementation 10x faster and prevents costly mistakes.

**Announce at start:** "I'm using the feature-planning skill to create the implementation plan."

**Output Location:** `.claude/docs/checklist-[feature-name].md`

## 6-Phase Planning Workflow

```
Phase 1: Understand the Feature (requirements gathering)
    ↓
Phase 2: Design Architecture (technical decisions)
    ↓
Phase 3: Break Down Components (what to build)
    ↓
Phase 4: Define APIs & Data Models (contracts)
    ↓
Phase 5: Identify Edge Cases (prevent bugs)
    ↓
Phase 6: Plan Testing Strategy (quality assurance)
    ↓
Output: Comprehensive Plan → Ready for /feature-build
```

**Estimated Time**: 5-10 minutes

---

## Phase 1: Understand the Feature

**Quick Summary**:
- Clarify requirements and user needs
- Define user stories and acceptance criteria
- Identify stakeholders and success metrics
- Duration: 1-2 minutes

---

## Phase 2: Design Architecture

**Quick Summary**:
- Make strategic technical decisions
- Choose frameworks, databases, APIs
- Create architecture diagrams
- Document technology choices
- Duration: 2-3 minutes

---

## Phase 3: Break Down Components

**Quick Summary**:
- Identify what needs to be built
- List frontend components and backend services
- Estimate complexity and time
- Duration: 2-3 minutes

---

## Phase 4: Define APIs & Data Models

**Quick Summary**:
- Define API endpoints and contracts
- Design database schemas
- Specify request/response formats
- Duration: 2-3 minutes

---

## Phase 5: Identify Edge Cases

**Quick Summary**:
- Identify potential bugs and edge cases
- Plan error handling strategies
- Consider security implications
- Duration: 1-2 minutes

---

## Phase 6: Plan Testing Strategy

**Quick Summary**:
- Plan unit, integration, and E2E tests
- Define test coverage goals
- Identify critical test scenarios
- Duration: 1-2 minutes

---

## Final Output Template

The plan should be saved to `.claude/docs/checklist-[feature-name].md` with this structure:

```markdown
# Feature Plan: [Feature Name]

## Phase 1: Requirements
[Requirements analysis and user stories]

## Phase 2: Architecture
[Architecture design and technical decisions]

## Phase 3: Components
[Component breakdown and implementation plan]

## Phase 4: APIs & Data
[API contracts and data models]

## Phase 5: Edge Cases
[Edge cases and error handling]

## Phase 6: Testing
[Testing strategy and coverage]

## Implementation Checklist
- [ ] Set up project structure
- [ ] Implement core components
- [ ] Add API endpoints
- [ ] Write tests
- [ ] Handle edge cases
- [ ] Deploy
```

---

## Complexity Assessment & Recommendations

Before proceeding with full planning, assess if cc10x adds value:

**Complexity Scale (1-5):**
- **1-2 (Simple)**: Well-documented library integration, CRUD operations
  - **Recommendation**: ❌ Skip cc10x - Manual implementation more efficient
  - **Example**: "Add a login form using Auth0"

- **3 (Moderate)**: Multiple components, some integration complexity
  - **Recommendation**: ⚠️ Consider manual - cc10x may be overkill
  - **Example**: "Add user profile page with edit functionality"

- **4-5 (Complex)**: Novel architecture, high risk, team alignment needed
  - **Recommendation**: ✅ Use cc10x - Systematic approach prevents costly mistakes
  - **Example**: "Real-time collaborative editing with conflict resolution"

**If complexity ≤ 2**: Ask user permission to continue or recommend manual approach

---

## Best Practices

1. **Start with user needs**, not technical solutions
2. **Document decisions** with rationale (future you will thank you)
3. **Identify risks early** - easier to mitigate in planning than in production
4. **Be realistic** with time estimates (add 50% buffer)
5. **Keep it simple** - avoid over-engineering
6. **Plan for failure** - what happens when things go wrong?

---

## Common Pitfalls to Avoid

- ❌ Skipping requirements phase (leads to rework)
- ❌ Over-engineering (YAGNI - You Aren't Gonna Need It)
- ❌ Ignoring edge cases (they always happen in production)
- ❌ No testing strategy (bugs found late are expensive)
- ❌ Unclear acceptance criteria (when is it "done"?)
- ❌ Missing error handling (happy path only)

---

## Success Criteria

A great plan should:
- ✅ Be actionable (clear next steps)
- ✅ Be testable (clear acceptance criteria)
- ✅ Be realistic (achievable time estimates)
- ✅ Address risks (identified and mitigated)
- ✅ Be documented (persistent markdown file)
- ✅ Be ready for `/feature-build` execution

---

## Example Output Location

`.claude/docs/checklist-authentication-system.md`

This file becomes the source of truth for implementation.
