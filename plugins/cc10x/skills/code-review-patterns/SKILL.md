---
name: code-review-patterns
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Grep, Glob
---

# Code Review Patterns

## Overview

Code reviews catch bugs before they ship. But reviewing code quality before functionality is backwards.

**Core principle:** First verify it works, THEN verify it's good.

## Quick Review Checklist (Reference Pattern)

**For rapid reviews, check these 8 items:**

- [ ] Code is simple and readable
- [ ] Functions and variables are well-named
- [ ] No duplicated code
- [ ] Proper error handling
- [ ] No exposed secrets or API keys
- [ ] Input validation implemented
- [ ] Good test coverage
- [ ] Performance considerations addressed

## The Iron Law

```
NO CODE QUALITY REVIEW BEFORE SPEC COMPLIANCE
```

If you haven't verified the code meets requirements, you cannot review code quality.

## Two-Stage Review Process

### Stage 1: Spec Compliance Review

**Does it do what was asked?**

1. **Read the Requirements**
   - What was requested?
   - What are the acceptance criteria?
   - What are the edge cases?

2. **Trace the Implementation**
   - Does the code implement each requirement?
   - Are all edge cases handled?
   - Does it match the spec exactly?

3. **Test Functionality**
   - Run the tests
   - Manual test if needed
   - Verify outputs match expectations

**Gate:** Only proceed to Stage 2 if Stage 1 passes.

### Stage 2: Code Quality Review

**Is it well-written?**

Review in priority order:

1. **Security** - Vulnerabilities that could be exploited
2. **Correctness** - Logic errors, edge cases missed
3. **Performance** - Unnecessary slowness
4. **Maintainability** - Hard to understand or modify
5. **UX** - User experience issues (if UI involved)
6. **Accessibility** - A11y issues (if UI involved)

## Security Review Checklist

| Check | Looking For | Example Vulnerability |
|-------|-------------|----------------------|
| Input validation | Unvalidated user input | SQL injection, XSS |
| Authentication | Missing auth checks | Unauthorized access |
| Authorization | Missing permission checks | Privilege escalation |
| Secrets | Hardcoded credentials | API key exposure |
| SQL queries | String concatenation | SQL injection |
| Output encoding | Unescaped output | XSS attacks |
| CSRF | Missing tokens | Cross-site request forgery |
| File handling | Path traversal | Reading arbitrary files |

**For each security issue found:**
```markdown
- [CRITICAL] SQL injection at `src/api/users.ts:45`
  - Problem: User input concatenated into query
  - Fix: Use parameterized query
  - Code: `db.query(\`SELECT * FROM users WHERE id = ?\`, [userId])`
```

## Quality Review Checklist

| Check | Good | Bad |
|-------|------|-----|
| **Naming** | `calculateTotalPrice()` | `calc()`, `doStuff()` |
| **Functions** | Does one thing | Multiple responsibilities |
| **Complexity** | Linear flow | Nested conditions |
| **Duplication** | DRY where sensible | Copy-paste code |
| **Error handling** | Graceful failures | Silent failures |
| **Testability** | Injectable dependencies | Global state |

## Performance Review Checklist

| Pattern | Problem | Fix |
|---------|---------|-----|
| N+1 queries | Loop with DB call | Batch query |
| Unnecessary loops | Iterating full list | Early return |
| Missing cache | Repeated expensive ops | Add caching |
| Memory leaks | Objects never cleaned | Cleanup on dispose |
| Sync blocking | Blocking main thread | Async operation |

## UX Review Checklist (UI Code)

| Check | Verify |
|-------|--------|
| Loading states | Shows loading indicator |
| Error states | Shows helpful error message |
| Empty states | Shows appropriate empty message |
| Success feedback | Confirms action completed |
| Form validation | Shows inline errors |
| Responsive | Works on mobile/tablet |

## Accessibility Review Checklist (UI Code)

| Check | Verify |
|-------|--------|
| Semantic HTML | Uses correct elements (button, not div) |
| Alt text | Images have meaningful alt text |
| Keyboard | All interactions keyboard accessible |
| Focus | Focus visible and logical order |
| Color contrast | Meets WCAG AA (4.5:1 text) |
| Screen reader | Labels and ARIA where needed |

## Severity Classification

| Severity | Definition | Action |
|----------|------------|--------|
| **CRITICAL** | Security vulnerability or blocks functionality | Must fix before merge |
| **MAJOR** | Affects functionality or significant quality issue | Should fix before merge |
| **MINOR** | Style issues, small improvements | Can merge, fix later |
| **NIT** | Purely stylistic preferences | Optional |

## Priority Output Format (Feedback Grouping)

**Organize feedback by priority (from reference pattern):**

```markdown
## Code Review Feedback

### Critical (must fix before merge)
- [95] SQL injection at `src/api/users.ts:45`
  → Fix: Use parameterized query `db.query('SELECT...', [userId])`

### Warnings (should fix)
- [85] N+1 query at `src/services/posts.ts:23`
  → Fix: Batch query with WHERE IN clause

### Suggestions (consider improving)
- [70] Function `calc()` could be renamed to `calculateTotal()`
  → More descriptive naming
```

**ALWAYS include specific examples of how to fix each issue.**
Don't just say "this is wrong" - show the correct approach.

## Red Flags - STOP and Re-review

If you find yourself:

- Reviewing code style before checking functionality
- Not running the tests
- Skipping the security checklist
- Giving generic feedback ("looks good")
- Not providing file:line citations
- Not explaining WHY something is wrong
- Not providing fix recommendations

**STOP. Start over with Stage 1.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Tests pass so it's fine" | Tests can miss requirements. Check spec compliance. |
| "Code looks clean" | Clean code can still be wrong. Verify functionality. |
| "I trust this developer" | Trust but verify. Everyone makes mistakes. |
| "It's a small change" | Small changes cause big bugs. Review thoroughly. |
| "No time for full review" | Bugs take more time than reviews. Do it properly. |
| "Security is overkill" | One vulnerability can sink the company. Check it. |

## Output Format

```markdown
## Code Review: [PR Title/Component]

### Stage 1: Spec Compliance ✅/❌

**Requirements:**
- [x] Requirement 1 - implemented at `file:line`
- [x] Requirement 2 - implemented at `file:line`
- [ ] Requirement 3 - NOT IMPLEMENTED

**Tests:** PASS (24/24)

**Verdict:** [Meets spec / Missing requirements]

---

### Stage 2: Code Quality

**Security:**
- [CRITICAL] Issue at `file:line` - Fix: [recommendation]
- No issues found ✅

**Performance:**
- [MAJOR] N+1 query at `file:line` - Fix: Use batch query
- No issues found ✅

**Quality:**
- [MINOR] Unclear naming at `file:line` - Suggestion: rename to X
- No issues found ✅

**UX/A11y:** (if UI code)
- [MAJOR] Missing loading state - Fix: Add spinner
- No issues found ✅

---

### Summary

**Decision:** Approve / Request Changes

**Critical:** [count]
**Major:** [count]
**Minor:** [count]

**Required fixes before merge:**
1. [Most important fix]
2. [Second fix]
```

## Review Loop Protocol

After requesting changes:

1. **Wait for fixes** - Developer addresses issues
2. **Re-review** - Check that fixes actually fix the issues
3. **Verify no regressions** - Run tests again
4. **Approve or request more changes** - Repeat if needed

**Never approve without verifying fixes work.**

## Final Check

Before approving:

- [ ] Stage 1 complete (spec compliance verified)
- [ ] Stage 2 complete (all checklists reviewed)
- [ ] All critical/major issues addressed
- [ ] Tests pass
- [ ] No regressions introduced
- [ ] Evidence captured for each claim
