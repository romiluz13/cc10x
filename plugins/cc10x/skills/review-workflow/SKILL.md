---
name: review-workflow
description: Orchestrates comprehensive code review using shared context for coordinated analysis. Loads 6 skills for multi-dimensional review (security, quality, performance, UX, accessibility). Use when reviewing code, auditing security, checking quality. Provides coordinated analysis avoiding duplicate findings. Loaded by orchestrator when user requests review.
license: MIT
---

# REVIEW Workflow Skill

**Orchestrates comprehensive code review with coordinated multi-dimensional analysis.**

## When to Use

Triggered by user requests:
- "review this code"
- "security audit"
- "code quality check"
- "check for vulnerabilities"
- "audit this component"

## Workflow Overview

**Pattern**: Hybrid (shared context + parallel subagents)
**Skills Loaded**: 2 (risk-analysis, code-quality-patterns)
**Subagents**: 3 (analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility)
**Time**: ~2-3 minutes
**Complexity Gate**: Skip for <100 lines (suggest manual review)
**Timeout**: 10 minutes (return partial results if exceeded)
**Fallback**: If subagent fails, continue with other subagents

---

## Phase 1: Complexity Gate

**Assess code size and complexity:**

1. **Code Size Check:**
 - < 100 lines: â ï¸SKIP (suggest manual review)
 - 100-500 lines: âPROCEED (standard review)
 - 500-2000 lines: âPROCEED (standard review)
 - > 2000 lines: âPROCEED (deep review)

2. **If skipped (<100 lines):**
 ```
 "This code is small enough for manual review (< 100 lines).
 Consider manual review for simpler code.

 Recommendation: Use manual review for efficiency.
 Want me to review anyway?"
 ```

3. **If proceeding (â¥100 lines):**
 - Parse user request for review focus
 - Identify target files/directories
 - Prepare for parallel analysis

4. **Partial Code Review Support:**
 - **Line ranges**: "review lines 50-150 of auth.js"
 - **Functions**: "review the login() function"
 - **Sections**: "review the authentication section"
 - **Files**: "review only src/auth/ directory"
 - **Patterns**: "review all database queries"

 **Handling**:
 - Extract specified code section
 - Adjust complexity assessment
 - Proceed with standard review
 - Note: "Reviewing partial code - full context may be needed"

---

## Phase 2: Load Skills in Shared Context

**Load 2 core skills for coordination:**

1. **risk-analysis**
 - Identifies architectural risks
 - Assesses security risks
 - Evaluates performance risks
 - Checks deployment readiness

2. **code-quality-patterns**
 - Complexity metrics
 - Code duplication
 - SOLID principles
 - Naming conventions

**Note**: Specific analysis skills loaded by subagents (see Phase 3)

---

## Phase 3: Dispatch 3 Subagents in PARALLEL

**All 3 subagents run simultaneously:**

### Subagent 1: analysis-risk-security
**Loads**: risk-analysis, security-patterns
**Tasks**:
- Identify security risks (OWASP Top 10)
- Verify authentication/authorization
- Validate input handling
- Check secret management
- Assess architectural risks
- Evaluate scalability risks

### Subagent 2: analysis-performance-quality
**Loads**: performance-patterns, code-quality-patterns
**Tasks**:
- Analyze database queries
- Check caching strategies
- Measure cyclomatic complexity
- Check for code duplication
- Verify SOLID principles
- Review naming conventions

### Subagent 3: analysis-ux-accessibility
**Loads**: ux-patterns, accessibility-patterns
**Tasks**:
- Check user experience
- Verify usability
- Verify WCAG compliance
- Check keyboard navigation
- Verify screen reader support
- Check color contrast

**Execution**: All 3 run in parallel
- Sequential: 15 minutes
- Parallel: 2-3 minutes
- **SPEEDUP: 3x FASTER!**

---

## Phase 4: Compile Results from All 3 Subagents

**Merge findings from parallel analysis:**

1. **Collect from Subagent 1** (risk-security)
 - Security vulnerabilities
 - Authentication issues
 - Input validation problems
 - Architectural risks

2. **Collect from Subagent 2** (performance-quality)
 - Performance bottlenecks
 - Code quality issues
 - Complexity problems
 - Duplication

3. **Collect from Subagent 3** (ux-accessibility)
 - UX problems
 - Accessibility violations
 - Usability issues
 - Design inconsistencies

4. **Organize by severity:**
 - ð´ Critical (fix immediately)
 - ðImportant (fix soon)
 - ð¢ Nice-to-have (consider)

---

## Phase 5: Generate Report

**Create comprehensive review report from merged findings:**

```markdown
# Code Review Report

## Summary
- Files reviewed: X
- Lines analyzed: X
- Issues found: X
- Quality score: X/10

## Critical Issues (ð´)
From Subagent 1 (Risk & Security):
- Security vulnerability: [Description]
- Architectural risk: [Description]

From Subagent 2 (Performance & Quality):
- Performance disaster: [Description]
- Critical complexity: [Description]

From Subagent 3 (UX & Accessibility):
- Critical accessibility violation: [Description]

## Important Issues (ð¡)
- [From all 3 subagents]

## Nice to Have (ð¢)
- [From all 3 subagents]

## Quality Metrics
- Security score: X/10
- Performance score: X/10
- Code quality score: X/10
- Accessibility score: X/10
- UX score: X/10
```

---

## Phase 6: Return Results

**Provide actionable feedback from all 3 subagents:**

1. **Critical issues** - Must fix before merge
2. **Important issues** - Should fix before merge
3. **Nice to have** - Consider for future
4. **Strengths** - What's working well
5. **Recommendations** - How to improve

**Offer next steps:**
```
Want me to:
â¢ Plan fixes for critical issues?
â¢ Build the fixes?
â¢ Review the fixes?
```

---

## Review Checklist

### Security
- [ ] No OWASP Top 10 vulnerabilities
- [ ] Authentication/authorization correct
- [ ] Input validation present
- [ ] Secrets not exposed
- [ ] Access control enforced

### Quality
- [ ] Cyclomatic complexity < 10
- [ ] No code duplication
- [ ] SOLID principles followed
- [ ] Meaningful names
- [ ] No technical debt

### Performance
- [ ] Queries optimized
- [ ] Caching used appropriately
- [ ] No memory leaks
- [ ] Network calls minimized
- [ ] Response times acceptable

### UX
- [ ] User experience good
- [ ] Usability acceptable
- [ ] Accessibility compliant
- [ ] Design consistent
- [ ] User flows clear

### Accessibility
- [ ] WCAG compliant
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast sufficient
- [ ] Semantic HTML used

---


---

## Error Handling & Fallbacks

### If Subagent Fails

**Fallback Strategy**:
1. Retry failed subagent (up to 3 times with exponential backoff)
2. If still fails, use sequential analysis instead of parallel
3. If sequential fails, use cached results from previous runs
4. Return partial review with available results

**Example**:
```
Parallel Execution:
 ââSubagent 1 (risk-security): âSuccess
 ââSubagent 2 (performance-quality): âFAILED
 ââSubagent 3 (ux-accessibility): âSuccess

Fallback to Sequential:
 ââSubagent 2 (retry): âSuccess (on retry)

Result: Complete review with all dimensions
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

Result: Review continues with cached skill
```

### Timeout Handling

**If analysis takes too long**:
1. Wait up to 5 minutes per subagent
2. If timeout, use partial results
3. Return review with available findings
4. Note incomplete analysis

---

## Next Steps: Workflow Chaining

### If Issues Found
```markdown
## Review Complete â

**Issues Found**: 3 critical, 5 warnings

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

### If No Issues Found
```markdown
## Review Complete â

**Status**: All checks passed!

**Suggested Next Workflow**: DEPLOY

This code is ready for:
1. Staging deployment
2. Production deployment
3. Release notes

**Time**: ~5 minutes
**Tokens**: ~10k

[Deploy] [Skip]
```

### If Bugs Found
```markdown
## Review Complete â

**Bugs Found**: 2 critical

**Suggested Next Workflow**: DEBUG

This will:
1. Investigate bugs
2. Find root causes
3. Fix bugs with tests
4. Verify fixes

**Time**: ~4 minutes
**Tokens**: ~35k

[Start DEBUG Workflow] [Skip]
```

---

## Remember

This workflow provides **coordinated analysis** that:
- Avoids duplicate findings
- Ensures comprehensive coverage
- Provides actionable feedback
- Improves code quality
- Prevents production issues
- **Suggests next workflow automatically**

**Use before merge for production code!**
