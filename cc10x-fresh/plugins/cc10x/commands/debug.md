---
description: Systematically debug issues with log analysis, code tracing, and root cause analysis
argument-hint: [error-description or log-file]
---

# Debugging Workflow

You are systematically debugging an issue.

## Context
- Issue: $ARGUMENTS
- Recent logs: !`tail -n 50 *.log 2>/dev/null || echo "No logs found"`
- Git blame: !`git log --oneline -10`
- Current branch: !`git branch --show-current`

## Complexity Assessment

Rate bug complexity (1-5):
- 1-2: Simple (syntax, typo, obvious fix)
- 3: Moderate (logic error, missing validation)
- 4-5: Complex (race condition, architecture, integration)

## Your Task

### Phase 1: Information Gathering
1. Reproduce the error
2. Collect error messages/stack traces
3. Note when it started
4. Check recent changes: `git log --since="3 days ago" --oneline`

### Phase 2: LOG FIRST Methodology
BEFORE deep investigation:
1. Add strategic logging/breakpoints
2. Re-run to collect data
3. Analyze logs for patterns
4. Narrow down location

### Phase 3: Code Investigation
1. Trace execution flow
2. Check variable states
3. Verify assumptions
4. Review related code

### Phase 4: Root Cause Analysis
Use the `systematic-debugging` skill to:
- Eliminate impossible causes
- Test hypotheses
- Identify root cause
- Verify understanding

### Phase 5: Fix & Verify
1. Implement fix
2. Add regression test
3. Run all tests
4. Verify fix works
5. Check for side effects

## Debugging Checklist
- [ ] Error reproduced consistently
- [ ] Logs analyzed
- [ ] Recent changes reviewed
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Regression test added
- [ ] All tests pass
- [ ] Side effects checked

## Output
```markdown
# Bug Fix Summary

## Issue
- Description: [What was broken]
- Severity: [Critical/High/Medium/Low]
- Root Cause: [What caused it]

## Investigation
- [Key findings from logs/traces]
- [Relevant code sections]

## Solution
- Files changed: [List]
- Fix description: [What was done]
- Regression test: [Location]

## Verification
- ✅ Original issue fixed
- ✅ Tests pass
- ✅ No side effects
```

