# Workflow Chaining Guide

## Overview

Workflow chaining allows workflows to suggest the next workflow to run, improving UX and saving time by automating the next step.

---

## Chaining Patterns

### Pattern 1: PLAN → BUILD
**When**: User completes planning and wants to implement

**Suggestion**:
```markdown
## Next Steps

Your plan is ready! Ready to build?

**Suggested Next Workflow**: BUILD

This will:
1. Load your plan as requirements
2. Implement components
3. Write tests
4. Verify integration

**Time**: ~4 minutes
**Tokens**: ~40k

[Start BUILD Workflow] [Skip]
```

**Benefits**:
- Seamless transition from planning to implementation
- Automatic context passing
- 2 min saved (no manual context setup)

---

### Pattern 2: BUILD → REVIEW
**When**: User completes building and wants code review

**Suggestion**:
```markdown
## Next Steps

Your code is ready! Ready for review?

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

**Benefits**:
- Automatic quality assurance
- Catches issues before deployment
- 2 min saved (no manual context setup)

---

### Pattern 3: REVIEW → PLAN (Improvements)
**When**: Review finds issues and suggests improvements

**Suggestion**:
```markdown
## Next Steps

Review found improvement opportunities!

**Suggested Next Workflow**: PLAN (Improvements)

This will:
1. Plan refactoring
2. Design improvements
3. Create implementation roadmap
4. Estimate effort

**Time**: ~4-5 minutes
**Tokens**: ~22k

[Start PLAN Workflow] [Skip]
```

**Benefits**:
- Structured improvement planning
- Prioritized roadmap
- 2 min saved (no manual context setup)

---

### Pattern 4: DEBUG → REVIEW (After Fix)
**When**: User fixes bugs and wants to verify quality

**Suggestion**:
```markdown
## Next Steps

Bugs fixed! Ready for quality check?

**Suggested Next Workflow**: REVIEW

This will:
1. Verify bug fixes
2. Check for regressions
3. Ensure code quality
4. Confirm no new issues

**Time**: ~2-3 minutes
**Tokens**: ~15k

[Start REVIEW Workflow] [Skip]
```

**Benefits**:
- Ensures fixes don't introduce new issues
- Comprehensive quality check
- 2 min saved (no manual context setup)

---

## Implementation Strategy

### For Each Workflow:

1. **Add "Next Steps" Section** at end of results
2. **Suggest appropriate next workflow** based on context
3. **Provide one-click action** to start next workflow
4. **Pass context automatically** to next workflow
5. **Allow user to skip** if not needed

---

## Workflow Chaining Sequence

```
PLAN
  ↓ (user clicks "Start BUILD")
BUILD
  ↓ (user clicks "Start REVIEW")
REVIEW
  ├─ (if issues found) → PLAN (Improvements)
  │   ↓
  │   BUILD (Improvements)
  │   ↓
  │   REVIEW (Verification)
  │
  └─ (if bugs found) → DEBUG
      ↓
      REVIEW (After Fix)
```

---

## Context Passing

### PLAN → BUILD
```markdown
**Context Passed**:
- Feature requirements
- Architecture design
- Component breakdown
- API specification
- Testing strategy
- File manifest
```

### BUILD → REVIEW
```markdown
**Context Passed**:
- Implemented code
- Test files
- Documentation
- Build artifacts
- Performance metrics
```

### REVIEW → PLAN
```markdown
**Context Passed**:
- Review findings
- Issues identified
- Improvement suggestions
- Priority ranking
- Effort estimates
```

### DEBUG → REVIEW
```markdown
**Context Passed**:
- Bug fixes
- Test files
- Root cause analysis
- Verification results
- Performance impact
```

---

## Token Savings

### Without Chaining
```
PLAN:   22k tokens
BUILD:  40k tokens
REVIEW: 15k tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:  77k tokens (+ 6 min for manual context setup)
```

### With Chaining
```
PLAN:   22k tokens
BUILD:  40k tokens (context auto-passed)
REVIEW: 15k tokens (context auto-passed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:  77k tokens (- 6 min for manual context setup)
```

**Savings**: 6 minutes per chain (2 min per workflow transition)

---

## Implementation Checklist

- [ ] Add "Next Steps" section to REVIEW workflow
- [ ] Add "Next Steps" section to PLAN workflow
- [ ] Add "Next Steps" section to BUILD workflow
- [ ] Add "Next Steps" section to DEBUG workflow
- [ ] Implement context passing mechanism
- [ ] Add one-click action buttons
- [ ] Test all chaining sequences
- [ ] Verify context preservation
- [ ] Update orchestrator to handle chaining
- [ ] Document chaining in user guide

---

## Benefits

✅ **Better UX** (seamless workflow transitions)
✅ **Time savings** (2 min per chain)
✅ **Automatic context** (no manual setup)
✅ **Guided workflow** (clear next steps)
✅ **Improved quality** (automatic review after build)
✅ **Faster iteration** (quick improvement cycles)

---

## Next Steps

1. Update REVIEW workflow with chaining suggestions
2. Update PLAN workflow with chaining suggestions
3. Update BUILD workflow with chaining suggestions
4. Update DEBUG workflow with chaining suggestions
5. Implement context passing mechanism
6. Test all chaining sequences
7. Deploy to production

