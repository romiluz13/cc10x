---
name: code-reviewing
description: Use when performing comprehensive code reviews - launches 5 parallel specialized reviewers (security, quality, performance, UX, accessibility) for multi-dimensional analysis; provides prioritized findings with optional auto-fix
---

# Code Reviewing - Multi-Dimensional Analysis Workflow

## Overview

Comprehensive code review with parallel multi-dimensional analysis. Five specialized reviewers examine code simultaneously for complete coverage.

**Core principle:** Parallel read-only analysis across all quality dimensions, synthesize findings, prioritize actions.

**Announce at start:** "I'm using the code-reviewing skill to analyze this code."

## Workflow Overview

```
Phase 1: Parallel Multi-Dimensional Analysis (5 reviewers)
    ↓
Phase 2: Synthesis & Prioritization (orchestrator)
    ↓
Phase 3: Optional Auto-Fix (conditional, 1 agent)
```

**Estimated Time**: 5-10 minutes
**Estimated Tokens**: ~40k (parallel execution)

## Parallel Execution Rules ⚡

| Phase | Max Parallel Agents | Reasoning |
|-------|-------------------|-----------|
| Phase 1 (Analysis) | **5 agents** ✅ | All read-only, completely independent |
| Phase 2 (Synthesis) | **0 agents** | Orchestrator handles (no sub-agents) |
| Phase 3 (Auto-Fix) | **1 agent** ⚠️ | Conditional, only if safe fixes available |

## Phase 1: Parallel Multi-Dimensional Analysis

**Objective**: Analyze code across all quality dimensions simultaneously

**Duration**: ~3-5 minutes

**Sub-Agents**: Launch 5 specialized reviewers in parallel (all read-only, safe)

### Security Reviewer

```markdown
Task: Analyze code for security vulnerabilities

Focus areas:
1. Authentication & Authorization issues
2. Input validation and sanitization
3. SQL injection, XSS, CSRF vulnerabilities
4. Secrets in code or config
5. Insecure dependencies
6. OWASP Top 10 compliance

Auto-invoked skill: security-patterns

Output: security-findings.md
- Critical issues (security vulnerabilities)
- High priority (potential exploits)
- Medium priority (security best practices)
- Recommendations with code examples
```

### Quality Reviewer

```markdown
Task: Analyze code quality and maintainability

Focus areas:
1. Code complexity (cyclomatic complexity)
2. Code duplication (DRY violations)
3. Naming conventions and clarity
4. Function/class size and responsibilities
5. Code organization and structure
6. Documentation and comments
7. Test coverage and quality

Auto-invoked skill: code-review-patterns

Output: quality-findings.md
- Code smells identified
- Refactoring opportunities
- Maintainability score
- Recommendations with examples
```

### Performance Analyzer

```markdown
Task: Analyze performance bottlenecks and optimization opportunities

Focus areas:
1. N+1 query problems
2. Unnecessary re-renders (React/Vue)
3. Memory leaks
4. Inefficient algorithms (O(n²) → O(n))
5. Bundle size and lazy loading
6. Database query optimization
7. Caching opportunities

Auto-invoked skill: performance-patterns

Output: performance-findings.md
- Critical bottlenecks
- Optimization opportunities (with estimated impact)
- Performance anti-patterns
- Recommendations with benchmarks
```

### UX Reviewer

```markdown
Task: Analyze user experience and interaction design

Focus areas:
1. Loading states and feedback
2. Error messages and handling
3. Form validation and UX
4. Mobile responsiveness
5. Keyboard navigation
6. Visual hierarchy
7. Consistency with design system

Auto-invoked skill: ux-patterns

Output: ux-findings.md
- UX issues (confusing flows, poor feedback)
- Accessibility issues (keyboard, screen readers)
- Responsive design problems
- Recommendations with mockups/examples
```

### Accessibility Reviewer

```markdown
Task: Analyze accessibility compliance (WCAG 2.1 AA)

Focus areas:
1. Semantic HTML usage
2. ARIA labels and roles
3. Keyboard accessibility
4. Screen reader compatibility
5. Color contrast ratios
6. Focus management
7. Alt text for images

Auto-invoked skill: accessibility-patterns

Output: accessibility-findings.md
- WCAG violations (with severity)
- Screen reader issues
- Keyboard navigation problems
- Recommendations with ARIA examples
```

**Parallel Execution Benefits**:
```
Sequential: 5 reviews × 3 min = 15 minutes
Parallel:   max(5 reviews) = 3-5 minutes
Time saved: 67% faster ⚡
```

**Quality Gate**:
- ✅ All 5 reviewers completed
- ✅ Findings documented with severity
- ✅ Recommendations actionable
- ❌ If any reviewer fails → Report error, continue with others

## Phase 2: Synthesis & Prioritization

**Objective**: Consolidate findings and prioritize actions

**Duration**: ~2 minutes

**Responsibility**: Orchestrator (you)

**Synthesis Process**:

```markdown
[Consolidate Findings]

Review all 5 outputs:
- security-findings.md
- quality-findings.md
- performance-findings.md
- ux-findings.md
- accessibility-findings.md

Categorize by severity:
1. 🔴 Critical (must fix immediately)
   - Security vulnerabilities
   - Accessibility blockers
   - Performance killers

2. 🟠 High Priority (fix before merge)
   - Security best practices
   - Major code smells
   - UX confusions

3. 🟡 Medium Priority (address soon)
   - Refactoring opportunities
   - Performance optimizations
   - UX improvements

4. 🟢 Low Priority (nice to have)
   - Code style improvements
   - Minor optimizations
   - Documentation enhancements

Identify safe auto-fixes:
- Formatting issues
- Import sorting
- Unused variable removal
- Simple refactorings (const vs let, etc.)
```

**Prioritization Matrix**:

| Severity | Impact | Examples |
|----------|--------|----------|
| Critical | Security breach, data loss | SQL injection, XSS, auth bypass |
| High | Poor UX, maintenance burden | Complex code, N+1 queries, a11y issues |
| Medium | Technical debt, optimization | Duplication, inefficient algorithms |
| Low | Polish, consistency | Naming, comments, formatting |

**Output Format**:

```markdown
## Code Review Summary

**Files Reviewed**: [list]
**Total Issues**: [count by severity]

### 🔴 Critical Issues (must fix immediately)
1. [Security] SQL injection in user.service.ts:45
   - Impact: Data breach potential
   - Recommendation: Use parameterized queries
   - Example: [code snippet]

### 🟠 High Priority (fix before merge)
...

### 🟡 Medium Priority (address soon)
...

### 🟢 Low Priority (nice to have)
...

### Safe Auto-Fixes Available
- [ ] Format code with Prettier
- [ ] Sort imports
- [ ] Remove 5 unused variables
- [ ] Convert 3 var → const
```

**Quality Gate**:
- ✅ All findings categorized by severity
- ✅ Recommendations are actionable
- ✅ Safe auto-fixes identified
- ✅ Summary is clear and concise
- ❌ If no actionable recommendations → Report "code looks good"

## Phase 3: Optional Auto-Fix

**Objective**: Automatically fix safe issues (conditional)

**Duration**: ~2-3 minutes (if executed)

**Condition**: Only runs if safe auto-fixes available

**Sub-Agent**: Launch auto-fixer (ONE agent, sequential)

```markdown
Task for auto-fixer:

Apply safe fixes identified in Phase 2:
- Formatting (Prettier/ESLint)
- Import sorting
- Unused variable removal
- Simple const/let conversions
- Missing semicolons/commas

Auto-invoked skill: safe-refactoring

Requirements:
1. Apply ONLY safe fixes (no behavior changes)
2. Run tests after EACH change (checkpoint-driven)
3. Rollback on test failure
4. Report what was fixed

DO NOT:
- Change logic or behavior
- Refactor complex code
- Modify critical files (auth, payment, etc.)
- Make breaking changes
```

**Safe Refactoring Guidelines**:

```markdown
✅ Safe Auto-Fixes:
- Formatting (whitespace, indentation)
- Import organization (alphabetical, grouped)
- Unused imports/variables removal
- const vs let (when immutable)
- Add missing semicolons
- Fix typos in comments
- Add missing return types (TypeScript)

❌ NOT Safe Auto-Fixes:
- Logic changes
- Renaming public APIs
- Database schema changes
- Authentication/authorization changes
- Complex refactorings
- Dependency updates
```

**Checkpoint-Driven Execution**:

```
For each safe fix:
1. Apply change
2. Run tests
3. If tests pass → Commit change
4. If tests fail → Rollback change, report
5. Continue with next fix
```

**Quality Gate**:
- ✅ All safe fixes applied successfully
- ✅ Tests pass after all changes
- ✅ Git status clean (no uncommitted changes)
- ❌ If tests fail → Rollback, report failed fixes

## Finalization

**Objective**: Provide comprehensive review report

**Review Report Format**:

```markdown
# Code Review Report

**Reviewed**: [files or PR]
**Date**: [timestamp]
**Reviewers**: Security, Quality, Performance, UX, Accessibility

---

## Executive Summary

**Overall Assessment**: [Good / Needs Improvement / Requires Fixes]

**Critical Issues**: [count] 🔴
**High Priority**: [count] 🟠
**Medium Priority**: [count] 🟡
**Low Priority**: [count] 🟢

**Safe Auto-Fixes Applied**: [count] ✅

---

## Detailed Findings

### 🔴 Critical Issues (must fix immediately)

#### 1. [Issue Title]
- **Category**: Security
- **Location**: src/auth/login.ts:45
- **Severity**: Critical
- **Impact**: Potential SQL injection vulnerability
- **Current Code**:
  ```typescript
  const query = `SELECT * FROM users WHERE email = '${email}'`;
  ```
- **Recommendation**:
  ```typescript
  const query = `SELECT * FROM users WHERE email = $1`;
  const result = await db.query(query, [email]);
  ```
- **References**: OWASP SQL Injection Prevention Cheat Sheet

---

[... repeat for all issues by severity ...]

---

## Metrics

| Dimension | Score | Notes |
|-----------|-------|-------|
| Security | 6/10 | SQL injection risks, missing input validation |
| Quality | 7/10 | Some code duplication, good structure overall |
| Performance | 8/10 | Minor N+1 query in user list |
| UX | 9/10 | Good loading states, minor keyboard nav issues |
| Accessibility | 6/10 | Missing ARIA labels, low contrast on buttons |

**Overall Score**: 7.2/10

---

## Action Items

**Before Merge** (Critical + High):
- [ ] Fix SQL injection in login.ts
- [ ] Add input validation to user registration
- [ ] Fix keyboard navigation in modal
- [ ] Add ARIA labels to form inputs

**Follow-Up** (Medium + Low):
- [ ] Refactor duplicated validation code
- [ ] Optimize user list query
- [ ] Improve error message clarity
- [ ] Add JSDoc comments to public APIs

---

## Auto-Fixes Applied ✅

- [x] Formatted 8 files with Prettier
- [x] Sorted imports in 12 files
- [x] Removed 5 unused variables
- [x] Converted 3 var → const

All tests passing after auto-fixes.

---

**Review complete**. Address critical and high-priority issues before merging.

🤖 Generated with [Claude Code](https://claude.com/claude-code) (cc10x)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Error Handling

### If No Files Specified

```markdown
⚠️ No files specified for review

Action: Ask user
- "Which files should I review?"
- "Do you want to review a PR? (provide URL)"
- "Should I review the entire codebase? (may take longer)"
```

### If PR URL Provided

```markdown
[Fetch PR Information]

1. Use gh CLI to fetch PR details:
   - Files changed
   - Commit messages
   - PR description

2. Review only changed files (efficient)

3. Include PR context in review:
   - Does implementation match PR description?
   - Are commit messages clear?
   - Are there test updates?
```

### If Reviewer Fails

```markdown
⚠️ [Reviewer] failed to complete

Action: Continue with other reviewers
- Note failure in report
- Provide partial review
- User can re-run failed reviewer separately
```

### If No Issues Found

```markdown
✅ Code looks good!

All reviewers report no critical or high-priority issues.

Minor suggestions:
- [list any low-priority improvements]

No auto-fixes needed.
```

## Parallel Execution Example

**Traditional Sequential Review**:
```
Security review:    3 min
Quality review:     3 min
Performance review: 3 min
UX review:          3 min
A11y review:        3 min
Total:             15 minutes
```

**cc10x Parallel Review**:
```
All 5 reviews simultaneously: 5 minutes (max duration)
Synthesis:                    2 minutes
Auto-fix (optional):          3 minutes
Total:                        10 minutes (67% faster!)
```

## Complete Example

```markdown
User: /review src/auth/

[Phase 1: Parallel Multi-Dimensional Analysis] 🔄 (5 min)
Launching 5 specialized reviewers in parallel...

✅ Security Reviewer: 2 critical issues, 3 high priority
✅ Quality Reviewer: 4 code smells, good structure overall
✅ Performance Reviewer: 1 N+1 query, minor optimization opportunities
✅ UX Reviewer: Good UX, 2 minor improvements suggested
✅ Accessibility Reviewer: 3 WCAG violations, keyboard nav issues

[Phase 2: Synthesis & Prioritization] 🔄 (2 min)
Consolidating findings across all dimensions...

✅ Total issues: 2 critical, 5 high, 4 medium, 3 low
✅ Prioritized by impact
✅ Identified 8 safe auto-fixes

[Phase 3: Auto-Fix] 🔄 (3 min)
Applying safe fixes...

✅ Formatted 5 files
✅ Sorted imports in 8 files
✅ Removed 3 unused variables
✅ All tests passing

[Review Complete] ✅ (10 minutes total)

📊 Overall Score: 7.2/10

🔴 Critical Issues: 2 (must fix immediately)
1. SQL injection in login.ts:45
2. Missing authentication check in resetPassword.ts:78

🟠 High Priority: 5 (fix before merge)
...

Report saved: code-review-report.md
```

## Remember

**Code review workflow is FAST because**:
- ✅ Parallel multi-dimensional analysis (5 reviewers simultaneously)
- ✅ Specialized expertise (each reviewer focused on one dimension)
- ✅ Auto-invoked skills (comprehensive checklists automatically applied)
- ✅ Optional auto-fixes (safe improvements applied automatically)

**Code review workflow is COMPREHENSIVE because**:
- ✅ 5 dimensions covered (security, quality, performance, UX, a11y)
- ✅ Expert skills auto-invoked (OWASP, WCAG, best practices)
- ✅ Prioritized findings (critical → low)
- ✅ Actionable recommendations (with code examples)

**10 minutes for comprehensive review. ~40k tokens (vs 80k sequential).** ⚡

