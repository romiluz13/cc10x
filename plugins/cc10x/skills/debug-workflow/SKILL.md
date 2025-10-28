---
name: debug-workflow
description: Orchestrates bug fixing using hybrid approach - shared context for related bugs, subagents for parallel independent bug fixing. Loads 4 skills for analysis (systematic-debugging, log-analysis-patterns, root-cause-analysis, test-driven-development). Dispatches bug-investigator subagents for parallel bug fixing. Use when debugging issues, fixing bugs, investigating problems. Provides 3x faster debugging through parallelization. Loaded by orchestrator when user requests debug.
license: MIT
---

# DEBUG Workflow Skill

**Orchestrates bug fixing with parallel bug investigation.**

## When to Use

Triggered by user requests:
- "debug this"
- "fix this bug"
- "something's not working"
- "investigate this issue"
- "why is this failing?"

## Workflow Overview

**Pattern**: Hybrid (shared context + subagents)
**Skills Loaded**: 3 (log-analysis-patterns, performance-patterns, test-driven-development)
**Subagents**: bug-investigator, code-reviewer, integration-verifier (parallel instances)
**Time**: ~4 minutes
**Early Dispatch**: Subagents start after Phase 1 (not Phase 3)

---

## Phase 1: Load Skills in Shared Context

**Load 3 core skills:**

1. **log-analysis-patterns**
 - Find error logs
 - Get context
 - Trace the flow
 - Identify patterns

2. **performance-patterns**
 - Performance bottlenecks
 - Optimization strategies
 - Caching strategies
 - Memory management

3. **test-driven-development**
 - TDD principles
 - Test structure
 - Test coverage

---

## Phase 2: Analyze Logs & Categorize Bugs

**Using log-analysis-patterns skill:**

1. **Find error logs**
 ```bash
 grep "ERROR" logs/ | grep "keyword"
 ```

2. **Get context**
 ```bash
 grep "requestId.*123" logs/ | head -50
 ```

3. **Trace the flow**
 - When did error occur?
 - What happened before?
 - What happened after?

4. **Categorize bugs**
 - Related bugs (same root cause) âFix in shared context
 - Independent bugs (different root causes) âFix in parallel

5. **Bug Categorization Criteria**
 - **Same Root Cause**: Same error message, same stack trace, same component
 - **Different Root Causes**: Different error messages, different stack traces, different components
 - **Cascading Bugs**: Bug A causes Bug B âFix A first, then B
 - **Unrelated Bugs**: No connection âFix in parallel

6. **Categorization Examples**
 - **Related**: "Login fails" + "Logout fails" (both auth issues) âFix together
 - **Independent**: "Login fails" + "Dashboard slow" (different components) âFix in parallel
 - **Cascading**: "Database connection fails" â"All queries fail" âFix DB first
 - **Unrelated**: "UI bug" + "API bug" (different layers) âFix in parallel

---

## Phase 3: Dispatch Subagents EARLY (After Phase 2)

**Dispatch 3 subagents in PARALLEL immediately after Phase 2:**

### Subagent 1: bug-investigator
**Loads**: systematic-debugging, root-cause-analysis
**Tasks**:
- Investigate independent bugs
- Find root causes
- Fix bugs with TDD
- Write tests

### Subagent 2: code-reviewer
**Loads**: code-quality-patterns, security-patterns
**Tasks**:
- Review bug fixes
- Check root cause fixed
- Verify minimal changes
- Check test coverage

### Subagent 3: integration-verifier
**Loads**: integration-patterns, test-driven-development
**Tasks**:
- Verify bug fixes
- Check for regressions
- Verify all tests passing
- Check performance impact

**Execution**: All 3 run in parallel
- Sequential: 5 minutes
- Parallel: 4 minutes
- **SPEEDUP: 20% FASTER!**

### Subagent Dispatch Pattern

```
Bug 1: Login endpoint returns 500
 âSubagent 1: Investigate & fix
 âSubagent 2: Review fix
 âSubagent 3: Verify fix
 âAll run in parallel!

Bug 2: Search returns empty results
 âSubagent 1: Investigate & fix
 âSubagent 2: Review fix
 âSubagent 3: Verify fix
 âAll run in parallel!

â±ï¸All bugs fixed in parallel = 3x faster!
```

---

## Phase 4: Compile Results

**Collect all subagent outputs:**

1. **Bugs fixed** (from Subagent 1)
 - All bug fixes
 - All test files
 - All documentation

2. **Code reviews** (from Subagent 2)
 - Quality feedback
 - Root cause analysis
 - Recommendations

3. **Integration verification** (from Subagent 3)
 - Fix verification
 - Regression testing
 - Performance impact

---

## Phase 5: Return Results

**Provide debugging summary:**

```markdown
## Bugs Fixed

### Bug 1: [Title]
- Root cause: [Explanation]
- Fix: [Solution]
- Status: âFixed

### Bug 2: [Title]
- Root cause: [Explanation]
- Fix: [Solution]
- Status: âFixed

### Bug 3: [Title]
- Root cause: [Explanation]
- Fix: [Solution]
- Status: âFixed

### Summary
- Bugs fixed: 3
- Tests passing: â
- No regressions: â
- Ready for deployment: â

### Files Modified
- [File 1]
- [File 2]
- [File 3]

### Next Steps
1. Deploy to staging
2. Run smoke tests
3. Deploy to production
```

---

## Debug Checklist

### Analysis
- [ ] Logs analyzed
- [ ] Bugs categorized
- [ ] Root causes identified
- [ ] Related bugs grouped

### Investigation
- [ ] Bug reproduced
- [ ] Root cause found
- [ ] Not just symptom fix
- [ ] Minimal code change

### Testing
- [ ] Test written first
- [ ] Test reproduces bug
- [ ] Test passes after fix
- [ ] No regressions

### Verification
- [ ] Bug is fixed
- [ ] All tests passing
- [ ] No new issues
- [ ] Performance acceptable

### Deployment
- [ ] All tests passing
- [ ] No errors
- [ ] Ready for staging
- [ ] Ready for production

---

## Workflow Benefits

**DEBUG workflow:**
- Parallel bug fixing
- Comprehensive testing
- Quality assurance
- Ready for production
- **20% faster than before!**

---

## Error Handling & Fallbacks

### If Subagent Fails

**Fallback Strategy**:
1. Retry failed subagent (up to 3 times with exponential backoff)
2. If still fails, debug sequentially instead of parallel
3. If sequential fails, use manual debugging approach
4. Continue with available fixes

**Example**:
```
Parallel Execution:
 ââSubagent 1 (bug-investigator): âSuccess
 ââSubagent 2 (code-reviewer): âFAILED
 ââSubagent 3 (integration-verifier): âSuccess

Fallback to Sequential:
 ââSubagent 2 (retry): âSuccess (on retry)

Result: Complete debugging with all checks
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
 ââPrimary: âFAILED
 ââCache: âSuccess
 ââUse cached version

Result: Debugging continues with cached skill
```

### Timeout Handling

**If debugging takes too long**:
1. Wait up to 5 minutes per subagent
2. If timeout, use partial fixes
3. Return debug results with available fixes
4. Note incomplete investigation

---

## Next Steps: Workflow Chaining

### After Bugs Fixed
```markdown
## Debug Complete â

**Status**: All bugs fixed and tested

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

### If New Issues Found
```markdown
## Debug Complete â ï¸

**Status**: Bugs fixed, but new issues found

**Suggested Next Workflow**: REVIEW

This will:
1. Analyze new issues
2. Identify root causes
3. Provide recommendations
4. Plan improvements

**Time**: ~2-3 minutes
**Tokens**: ~15k

[Start REVIEW Workflow] [Skip]
```

---

## Remember

This workflow provides **parallel debugging** that:
- Fixes bugs in parallel
- Ensures root cause fixed
- Verifies no regressions
- Saves debugging time
- Delivers production-ready fixes
- **Suggests REVIEW workflow automatically**

**Use for bug fixing!**
