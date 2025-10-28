# PLANNING Workflow - Comprehensive Feature Planning

**Triggered by:** User requests feature plan, architecture design, PRD creation

**Token cost:** ~25k tokens (orchestrator + workflow + agents + skills)

---

## Phase 0: Complexity Assessment

**CRITICAL GATE:** Assess if systematic planning is worth the token cost.

**Quick assessment:**
1. How many files affected? (1-3=simple, 4-6=moderate, 7+=complex)
2. Using library or novel pattern? (library=simple, novel=complex)
3. High-risk domain? (auth/payment/data=complex)

**IF Complexity <= 2 (SIMPLE):**
- STOP execution
- Warn user about 16x token multiplier
- Show example: Rate limiting = 5k manual vs 80k systematic
- ASK: "Continue anyway? (yes/no)"
- If NO: Exit
- If YES: Proceed with warning

**IF Complexity >= 4 (COMPLEX):**
- Proceed with confidence (systematic planning prevents costly mistakes)

---

## Phase 1: Requirements Analysis

**Invoke requirements-analyst agent:**

Follow instructions in [../../agents/requirements-analyst.md](../../agents/requirements-analyst.md)

**Agent task:**
1. Parse user's feature description
2. Identify core functionality
3. Extract implicit requirements
4. Generate user stories with acceptance criteria
5. List assumptions to validate
6. Create clarifying questions (if any)

**Agent loads skills:**
- `feature-planning` skill (requirements patterns)

**Output:**
- Requirements summary
- User stories (As a [role], I want [feature], so that [benefit])
- Acceptance criteria per story
- Assumptions list
- Clarifying questions (if requirements unclear)

---

## Phase 2: Context Analysis

**Invoke context-analyzer agent:**

Follow instructions in [../../agents/context-analyzer.md](../../agents/context-analyzer.md)

**Agent task:**
1. Search codebase for similar features
2. Identify existing patterns to follow
3. Find naming conventions
4. Locate integration points
5. Discover relevant existing code

**Agent loads skills:**
- `codebase-navigation` skill (search strategies)

**Output:**
- Similar features found
- Patterns to follow
- Naming conventions
- Integration points
- Files to modify/create

---

## Phase 3: Architecture & Design

**Invoke architect agent:**

Follow instructions in [../../agents/architect.md](../../agents/architect.md)

**Agent task:**
1. Design system architecture
2. Evaluate technology options
3. Make architecture decisions (with trade-offs)
4. Create component breakdown
5. Design API specifications
6. Plan data models

**Agent loads skills:**
- `feature-planning` skill (architecture patterns)
- `risk-analysis` skill (Stage 1: Data Flow, Stage 2: Dependencies)

**Output:**
- Architecture diagram (text-based)
- Technology decisions with justification
- Component breakdown
- API specification
- Data models
- Sequence diagrams

---

## Phase 4: Risk Assessment

**Agent continues with risk-analysis skill:**

**Load 7-dimension framework:**
See [../../skills/risk-analysis/SKILL.md](../../skills/risk-analysis/SKILL.md)

**Agent analyzes:**
1. Data Flow transformations (Stage 1)
2. Dependency integration (Stage 2)
3. Timing/Concurrency (Stage 3)
4. UX/Human Factors (Stage 4)
5. Security validation (Stage 5)
6. Performance/Scalability (Stage 6)
7. Failure Modes/Recovery (Stage 7)

**Output:**
- Risk matrix (Probability × Impact)
- Top 5 risks prioritized
- Mitigation strategies per risk
- Residual risks after mitigation

---

## Phase 5: Testing Strategy

**Invoke tdd-enforcer agent (planning mode):**

Follow instructions in [../../agents/tdd-enforcer.md](../../agents/tdd-enforcer.md)

**Agent task:**
1. Plan unit tests (what to test)
2. Plan integration tests (how components interact)
3. Plan e2e tests (user journeys)
4. Define test coverage goals (>80%)
5. Identify edge cases to test

**Agent loads skills:**
- `test-driven-development` skill (testing patterns)

**Output:**
- Test plan (unit, integration, e2e)
- Coverage goals
- Edge cases to test
- Testing tools recommended

---

## Phase 6: Implementation Roadmap

**Invoke devops-planner agent:**

Follow instructions in [../../agents/devops-planner.md](../../agents/devops-planner.md)

**Agent task:**
1. Break feature into incremental phases
2. Create file manifest (files to create/modify)
3. Plan deployment strategy
4. Create rollback procedures
5. Estimate lines of code

**Agent loads skills:**
- `deployment-patterns` skill (deployment strategies)

**Output:**
- Implementation phases (6-10 increments)
- File manifest with estimated LOC
- Deployment strategy (blue-green, canary, etc.)
- Rollback plan with steps
- Timeline estimate

---

## Phase 7: Compile Comprehensive Plan

**Create final plan document:**

```markdown
# Feature Plan: [Feature Name]

## 1. Requirements
[Requirements from Phase 1]

## 2. Architecture
[Architecture from Phase 3]

## 3. Risk Assessment
[Risks from Phase 4]

## 4. Testing Strategy
[Tests from Phase 5]

## 5. Implementation Roadmap
[Roadmap from Phase 6]

## 6. File Manifest
[Files to create/modify from Phase 6]

## 7. Deployment Strategy
[Deployment plan from Phase 6]

## 8. Rollback Procedures
[Rollback steps from Phase 6]
```

**Save to:**
```bash
.claude/plans/FEATURE_[name].md
```

---

## Phase 8: Return Results

**Present plan to user:**

```
Comprehensive plan created!

Summary:
- Complexity: X/5
- Files to modify: Y
- Estimated LOC: Z
- Implementation phases: N
- Top risks: [list top 3]

Plan saved to: .claude/plans/FEATURE_[name].md

What would you like to do?
- Build this feature now? (invoke BUILD workflow)
- Refine the plan?
- Start with specific phase?
```

**DO NOT automatically start building!**

Let user decide next step.

---

## Token Economics

**Typical planning workflow:**
- Orchestrator: 1.5k
- This workflow: 2k
- Requirements agent: 2k
- Context agent: 3k
- Architect agent: 4k
- TDD agent: 2k
- DevOps agent: 3k
- Domain skills: 8k (risk-analysis, feature-planning, deployment-patterns)
- **Total: ~25k tokens**

**Time:** 5-10 minutes

**Value:** Prevents costly architecture mistakes (one avoided mistake = ROI)
