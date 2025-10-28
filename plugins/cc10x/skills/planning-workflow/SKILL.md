---
name: planning-workflow
description: Orchestrates comprehensive feature planning using shared context for sequential phases. Loads 7 skills for complete planning (feature-planning, requirements-analysis, architecture-patterns, api-design-patterns, component-design-patterns, risk-analysis, deployment-patterns). Use when planning features, designing architecture, creating PRDs. Provides coordinated planning with sequential phases building on each other. Loaded by orchestrator when user requests planning.
license: MIT
---

# PLANNING Workflow Skill

**Orchestrates comprehensive feature planning with sequential phases.**

## When to Use

Triggered by user requests:
- "plan this feature"
- "design the architecture"
- "create a PRD"
- "plan the implementation"
- "design the system"

## Workflow Overview

**Pattern**: Hybrid (shared context + parallel subagents)
**Skills Loaded**: 1 (requirements-analysis)
**Subagents**: 2 (planning-architecture-risk, planning-design-deployment)
**Time**: ~4-5 minutes
**Complexity Gate**: Skip for simple features (1-2 user stories)

---

## Phase 1: Complexity Gate

**Assess feature complexity:**

1. **Feature Size Check:**
   - Simple (1-2 user stories): ⚠️ SKIP (suggest manual planning)
   - Medium (3-5 user stories): ✅ PROCEED (standard planning)
   - Complex (6+ user stories): ✅ PROCEED (deep planning)

2. **If skipped (simple features):**
   ```
   "This is a simple feature (1-2 user stories).
   Consider manual planning for simpler features.

   Recommendation: Use manual planning for efficiency.
   Want me to plan anyway?"
   ```

3. **If proceeding (medium/complex):**
   - Proceed to Phase 2

---

## Phase 2: Requirements Analysis (Shared Context)

**Load requirements-analysis skill:**

Analyze and document:
1. **Stakeholder analysis**
   - Who are the users?
   - What are their pain points?
   - What success looks like?

2. **Requirement elicitation**
   - Functional requirements
   - Non-functional requirements
   - Constraints
   - Assumptions

3. **User stories**
   - As a [user], I want [feature] so that [benefit]
   - Acceptance criteria
   - Edge cases

4. **Scope definition**
   - In scope
   - Out of scope
   - MVP vs Phase 2

**Output:**
- Requirements document
- User stories
- Acceptance criteria
- Scope statement

---

## Phase 3: Dispatch 2 Subagents in PARALLEL

**All 2 subagents run simultaneously (1.5x faster):**

**Context Passing**:
- Both subagents receive: Requirements document + user stories
- Subagent 1 output → Passed to Subagent 2 (architecture decisions)
- Subagent 2 output → Passed to Subagent 1 (deployment constraints)
- Coordination: Resolve conflicts in Phase 4

### Subagent 1: planning-architecture-risk
**Loads**: architecture-patterns, risk-analysis
**Receives**: Requirements document
**Tasks**:
- Design system architecture
- Choose technologies
- Break down components
- Design data models
- Specify APIs
- Identify security risks
- Assess performance risks
- Plan mitigations
**Outputs**: Architecture design, risk assessment

### Subagent 2: planning-design-deployment
**Loads**: api-design-patterns, component-design-patterns, deployment-patterns
**Receives**: Requirements document + Architecture design
**Tasks**:
- Design RESTful endpoints
- Design request/response formats
- Design authentication/authorization
- Design component hierarchy
- Design props interfaces
- Plan state management
- Plan implementation phases
- Create file manifest
- Plan testing strategy
- Plan deployment strategy
**Outputs**: Detailed design, deployment plan

**Execution**: All 2 run in parallel
- Sequential: 10 minutes
- Parallel: 4-5 minutes
- **SPEEDUP: 1.5x FASTER!**

---

## Phase 4: Compile Results from Both Subagents

**Merge planning from parallel analysis:**

1. **Collect from Subagent 1** (architecture-risk)
   - System architecture
   - Technology decisions
   - Component breakdown
   - Data models
   - API specification
   - Risk register
   - Mitigation strategies

2. **Collect from Subagent 2** (design-deployment)
   - API design details
   - Component hierarchy
   - Props interfaces
   - State management plan
   - Implementation phases
   - File manifest
   - Testing strategy
   - Deployment plan

---

## Phase 5: Generate Comprehensive Plan

**Create comprehensive plan document:**

```markdown
# Feature Plan: [Feature Name]

## 1. Requirements
[Requirements from Phase 2]

## 2. Architecture
[Architecture from Subagent 1]

## 3. API Design
[API design from Subagent 2]

## 4. Component Design
[Component design from Subagent 2]

## 5. Risk Assessment
[Risks from Subagent 1]

## 6. Implementation Roadmap
[Roadmap from Subagent 2]

## 7. File Manifest
[Files to create/modify]

## 8. Deployment Strategy
[Deployment plan]

## 9. Timeline
[Estimated timeline]

## 10. Success Criteria
[How to measure success]
```

---

## Planning Checklist

### Requirements
- [ ] Stakeholders identified
- [ ] Requirements documented
- [ ] User stories written
- [ ] Acceptance criteria defined
- [ ] Scope defined
- [ ] Assumptions listed

### Architecture
- [ ] System architecture designed
- [ ] Technology choices justified
- [ ] Components identified
- [ ] Data models designed
- [ ] API specified

### Design
- [ ] Component hierarchy defined
- [ ] Props interfaces designed
- [ ] State management planned
- [ ] Composition patterns identified

### Risk Management
- [ ] Security risks identified
- [ ] Performance risks identified
- [ ] Operational risks identified
- [ ] Mitigations planned

### Implementation
- [ ] Phases defined
- [ ] File manifest created
- [ ] Testing strategy defined
- [ ] Deployment strategy defined
- [ ] Timeline estimated

---


---

## Error Handling & Fallbacks

### If Subagent Fails

**Fallback Strategy**:
1. Retry failed subagent (up to 3 times with exponential backoff)
2. If still fails, plan sequentially instead of parallel
3. If sequential fails, use cached plan from similar features
4. Continue with available planning

**Example**:
```
Parallel Execution:
  ├─ Subagent 1 (architecture-risk): ✅ Success
  └─ Subagent 2 (design-deployment): ❌ FAILED

Fallback to Sequential:
  └─ Subagent 2 (retry): ✅ Success (on retry)

Result: Complete plan with all phases
```

### If Skill Fails

**Fallback Strategy**:
1. Try to load skill from cache
2. If no cache, use minimal skill (metadata only)
3. Continue with available skills
4. Note missing analysis in results

**Example**:
```
Load Skill:
  ├─ Primary: ❌ FAILED
  ├─ Cache: ✅ Success
  └─ Use cached version

Result: Planning continues with cached skill
```

### Timeout Handling

**If planning takes too long**:
1. Wait up to 5 minutes per subagent
2. If timeout, use partial plan
3. Return plan with available phases
4. Note incomplete planning

---

## Next Steps: Workflow Chaining

### After Planning Complete
```markdown
## Plan Complete ✅

**Status**: Architecture, design, and deployment strategy ready

**Suggested Next Workflow**: BUILD

This will:
1. Implement components
2. Write tests
3. Verify integration
4. Deliver production-ready code

**Time**: ~4 minutes
**Tokens**: ~40k

[Start BUILD Workflow] [Skip]
```

### If Risks Identified
```markdown
## Plan Complete ⚠️

**Risks Identified**: 3 high-priority risks

**Suggested Next Workflow**: REVIEW (Risk Assessment)

This will:
1. Deep dive into risks
2. Identify mitigations
3. Plan contingencies
4. Update architecture

**Time**: ~2-3 minutes
**Tokens**: ~15k

[Start REVIEW Workflow] [Skip]
```

---

## Remember

This workflow provides **comprehensive planning** that:
- Aligns stakeholders
- Identifies risks early
- Enables parallel work
- Prevents rework
- Saves implementation time
- **Suggests BUILD workflow automatically**

**Use before implementation for complex features!**
