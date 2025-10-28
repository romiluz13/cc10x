---
name: build-workflow
description: Orchestrates feature implementation using hybrid approach - shared context for analysis, subagents for parallel component building. Loads 5 skills for planning (feature-planning, requirements-analysis, component-design-patterns, code-generation, test-driven-development). Dispatches component-builder subagents for parallel implementation. Use when implementing features, building components, creating functionality. Provides 3x faster implementation through parallelization. Loaded by orchestrator when user requests build.
license: MIT
---

# BUILD Workflow Skill

**Orchestrates feature implementation with parallel component building.**

## When to Use

Triggered by user requests:
- "build this feature"
- "implement this"
- "create this component"
- "add this functionality"
- "develop this feature"

## Workflow Overview

**Pattern**: Hybrid (shared context + subagents)
**Skills Loaded**: 3 (requirements-analysis, security-patterns, test-driven-development)
**Subagents**: component-builder, code-reviewer, integration-verifier (parallel instances)
**Time**: ~4 minutes
**Early Dispatch**: Subagents start after Phase 2 (not Phase 4)

---

## Phase 1: Load Skills in Shared Context

**Load 3 core skills:**

1. **requirements-analysis**
   - Parse requirements
   - Identify components
   - Plan implementation

2. **security-patterns**
   - Security best practices
   - Input validation
   - Authentication/authorization
   - Secrets management

3. **test-driven-development**
   - TDD principles
   - Test structure
   - Test coverage

---

## Phase 2: Analyze Requirements

**Using requirements-analysis skill:**

1. **Parse requirements**
   - Functional requirements
   - Acceptance criteria
   - Edge cases

2. **Identify components**
   - Major components
   - Component dependencies
   - Component interfaces
   - Dependency graph

3. **Plan implementation**
   - Component breakdown
   - Implementation order (respecting dependencies)
   - Dependency resolution strategy
   - Circular dependency detection

4. **Dependency Resolution**
   - **Independent components**: Build in parallel
   - **Dependent components**: Build in sequence (dependency first)
   - **Circular dependencies**: Flag as error + suggest refactoring
   - **Shared dependencies**: Build once, reuse across components

---

## Phase 3: Dispatch Subagents EARLY (After Phase 2)

**Dispatch 3 subagents in PARALLEL immediately after Phase 2:**

### Subagent 1: component-builder
**Loads**: component-design-patterns, code-generation
**Tasks**:
- Design component specifications
- Build components with TDD
- Write tests
- Implement functionality

### Subagent 2: code-reviewer
**Loads**: code-quality-patterns, security-patterns
**Tasks**:
- Review code quality
- Check security
- Verify performance
- Check test coverage

### Subagent 3: integration-verifier
**Loads**: integration-patterns, test-driven-development
**Tasks**:
- Verify component integration
- Check data flows
- Verify error handling
- Check performance

**Execution**: All 3 run in parallel
- Sequential: 5 minutes
- Parallel: 4 minutes
- **SPEEDUP: 20% FASTER!**

### Subagent Dispatch Pattern

```
Component 1: UserCard
  �Subagent 1: Build UserCard (TDD)
  �Subagent 2: Review UserCard
  �Subagent 3: Verify UserCard integration
  �All run in parallel!

Component 2: LoginForm
  �Subagent 1: Build LoginForm (TDD)
  �Subagent 2: Review LoginForm
  �Subagent 3: Verify LoginForm integration
  �All run in parallel!

⏱�All components built in parallel = 3x faster!
```

---

## Phase 4: Compile Results

**Collect all subagent outputs:**

1. **Components built** (from Subagent 1)
   - All component files
   - All test files
   - All documentation

2. **Code reviews** (from Subagent 2)
   - Quality feedback
   - Security findings
   - Performance suggestions

3. **Integration verification** (from Subagent 3)
   - Integration status
   - Issues found
   - Recommendations

---

## Phase 5: Return Results

**Provide implementation summary:**

```markdown
## Implementation Complete

### Components Built
- �Component 1: [Status]
- �Component 2: [Status]
- �Component 3: [Status]

### Code Quality
- Quality score: X/10
- Test coverage: X%
- Security: �Pass
- Performance: �Pass

### Integration
- All components integrated: YES
- All tests passing: YES
- Ready for deployment: YES

### Files Created
- [File 1]
- [File 2]
- [File 3]

### Next Steps
1. Deploy to staging
2. Run smoke tests
3. Deploy to production
```

---

## Build Checklist

### Planning
- [ ] Requirements understood
- [ ] Components identified
- [ ] Implementation order defined
- [ ] Dependencies resolved

### Implementation
- [ ] All components built
- [ ] All tests passing
- [ ] Test coverage > 80%
- [ ] No console errors

### Quality
- [ ] Code reviewed
- [ ] Security checked
- [ ] Performance verified
- [ ] Accessibility checked

### Integration
- [ ] Components integrated
- [ ] Data flows correctly
- [ ] Error handling works
- [ ] Performance acceptable

### Deployment
- [ ] All tests passing
- [ ] No errors
- [ ] Ready for staging
- [ ] Ready for production

---

## Workflow Benefits

**BUILD workflow:**
- Parallel component building
- Comprehensive testing
- Quality assurance
- Ready for production

---

## Error Handling & Fallbacks

### If Subagent Fails

**Fallback Strategy**:
1. Retry failed subagent (up to 3 times with exponential backoff)
2. If still fails, build components sequentially instead of parallel
3. If sequential fails, use template components
4. Continue with available components

**Example**:
```
Parallel Execution:
  ├�Subagent 1 (component-builder): �Success
  ├�Subagent 2 (code-reviewer): �FAILED
  └�Subagent 3 (integration-verifier): �Success

Fallback to Sequential:
  └�Subagent 2 (retry): �Success (on retry)

Result: Complete build with all components
```

### If Skill Fails

**Fallback Strategy**:
1. Try to load skill from cache
2. If no cache, use minimal skill (metadata only)
3. Continue with available skills
4. Note missing guidance in results

**Example**:
```
Load Skill:
  ├�Primary: �FAILED
  ├�Cache: �Success
  └�Use cached version

Result: Build continues with cached skill
```

### Timeout Handling

**If building takes too long**:
1. Wait up to 5 minutes per subagent
2. If timeout, use partial components
3. Return build with available components
4. Note incomplete implementation

---

## Next Steps: Workflow Chaining

### After Successful Build
```markdown
## Build Complete

**Status**: All components built and tested

**Suggested Next Workflow**: REVIEW

This will:
1. Analyze code quality
2. Check security
3. Verify performance
4. Assess UX/accessibility

**Time**: ~2-3 minutes
**Tokens**: ~15k

[Start REVIEW Workflow] [Skip]
```

### If Build Issues Found
```markdown
## Build Complete (With Warnings)

**Issues Found**: 2 critical, 3 warnings

**Suggested Next Workflow**: DEBUG

This will:
1. Investigate issues
2. Find root causes
3. Fix bugs with tests
4. Verify fixes

**Time**: ~4 minutes
**Tokens**: ~35k

[Start DEBUG Workflow] [Skip]
```

---

## Remember

This workflow provides **parallel implementation** that:
- Builds components in parallel
- Ensures quality through review
- Verifies integration
- Saves implementation time
- Delivers production-ready code
- **Suggests REVIEW workflow automatically**

**Use for feature implementation!**
