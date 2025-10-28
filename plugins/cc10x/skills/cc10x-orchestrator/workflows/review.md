# REVIEW Workflow - Multi-Dimensional Code Analysis

**Triggered by:** User requests code review, security audit, quality check



---

## Overview

This workflow invokes 5 specialized reviewer agents in PARALLEL for comprehensive multi-dimensional analysis:
1. Security vulnerabilities
2. Code quality issues
3. Performance bottlenecks
4. UX problems
5. Accessibility violations

---

## Phase 1: Scope Determination

**Parse user request to identify:**

1. **Target files:**
   - Specific file: `src/auth.js`
   - Directory: `src/features/auth/`
   - Pattern: `src/**/*.js`
   - Entire codebase: `src/`

2. **Focus area (if specified):**
   - Security only: Skip other agents
   - Performance only: Skip other agents
   - All dimensions: Invoke all 5 agents

3. **File count estimate:**
   - 1-3 files: Small scope
   - 4-10 files: Medium scope
   - 10+ files: Large scope

---

## Phase 2: Invoke 5 Reviewer Agents in Parallel

**EXECUTE THESE CONCURRENTLY:**

### Agent 1: Security Reviewer

**The agent will:**
1. Load domain skills:
   - `risk-analysis` skill (Stages 1: Data Flow, 2: Dependencies, 5: Security)
   - `security-patterns` skill (authentication, authorization, injection)
2. Analyze target files for:
   - SQL injection, XSS, CSRF vulnerabilities
   - Authentication bypasses
   - Authorization flaws
   - Secret management issues
   - Dependency vulnerabilities
3. Return findings with severity: CRITICAL/HIGH/MEDIUM/LOW

**Agent output format:**
```markdown
## Security Review Findings

### CRITICAL
- [File:Line] SQL injection in user login query
  Impact: Full database access
  Fix: Use parameterized queries

- [File:Line] Hardcoded API key in source
  Impact: API abuse, cost
  Fix: Move to environment variables

### HIGH
- [File:Line] Missing rate limiting on auth endpoint
  Impact: Brute force attacks
  Fix: Implement express-rate-limit

[etc.]
```

---

### Agent 2: Quality Reviewer

**The agent will:**
1. Load domain skills:
   - `code-generation` skill (quality patterns, SOLID principles)
   - `safe-refactoring` skill (refactoring patterns)
2. Analyze for:
   - Code smells (long functions, god objects, duplicates)
   - SOLID violations
   - Complexity issues (cyclomatic complexity > 10)
   - Naming conventions
   - Documentation gaps
3. Return findings with refactoring suggestions

**Agent output format:**
```markdown
## Quality Review Findings

### HIGH
- [File:Line] Function exceeds 50 lines (currently 120)
  Issue: Hard to test and maintain
  Fix: Extract methods for validation, db operations, response

- [File:Line] Duplicate code across 3 files
  Issue: Maintenance burden, bug spread
  Fix: Extract to shared utility function

### MEDIUM
[etc.]
```

---

### Agent 3: Performance Analyzer

**The agent will:**
1. Load domain skills:
   - `performance-patterns` skill (optimization patterns)
   - `risk-analysis` skill (Stage 6: Performance/Scalability)
2. Analyze for:
   - N+1 query problems
   - Missing database indexes
   - Memory leaks (closures, event listeners)
   - Inefficient algorithms (O(n¬≤) loops)
   - Missing caching opportunities
3. Return findings with optimization strategies

**Agent output format:**
```markdown
## Performance Review Findings

### HIGH
- [File:Line] N+1 query in user listing
  Impact: 1000 users = 1000 queries (5s response)
  Fix: Use JOIN or batch loading

- [File:Line] Missing index on email column
  Impact: Full table scan on every login
  Fix: ADD INDEX idx_users_email

### MEDIUM
[etc.]
```

---

### Agent 4: UX Reviewer

**The agent will:**
1. Load domain skills:
   - `ux-patterns` skill (user experience patterns)
   - `risk-analysis` skill (Stage 4: UX/Human Factors)
2. Analyze for:
   - Error message quality (helpful vs cryptic)
   - Edge case handling (empty states, loading, errors)
   - User feedback (success/failure indicators)
   - Input validation messages
   - Confirmation dialogs for destructive actions
3. Return findings with UX improvements

**Agent output format:**
```markdown
## UX Review Findings

### HIGH
- [File:Line] Cryptic error: "Error 401"
  Impact: User confusion
  Fix: "Invalid credentials. Please check your email and password."

- [File:Line] No loading state during login
  Impact: User clicks multiple times
  Fix: Show spinner, disable button

### MEDIUM
[etc.]
```

---

### Agent 5: Accessibility Reviewer

**The agent will:**
1. Load domain skills:
   - `accessibility-patterns` skill (WCAG guidelines, a11y patterns)
2. Analyze for:
   - Missing alt text on images
   - Keyboard navigation issues
   - Screen reader compatibility
   - Color contrast problems
   - ARIA labels missing
   - Focus management
3. Return findings with WCAG compliance level

**Agent output format:**
```markdown
## Accessibility Review Findings

### CRITICAL (WCAG A)
- [File:Line] Button has no accessible label
  Impact: Screen readers can't identify purpose
  Fix: Add aria-label="Submit login form"

- [File:Line] Form inputs have no labels
  Impact: Cannot navigate with keyboard
  Fix: Add <label for="email">Email</label>

### HIGH (WCAG AA)
[etc.]
```

---

## Phase 3: Compile Results

**After all 5 agents complete:**

1. **Aggregate findings** from all agents
2. **Deduplicate** overlapping issues (e.g., security and quality both flag same function)
3. **Prioritize** by severity (CRITICAL ‚ÜHIGH ‚ÜMEDIUM ‚ÜLOW)
4. **Cross-reference** related issues
5. **Calculate** total issue count and breakdown

---

## Phase 4: Format Comprehensive Report

```markdown
# Code Review Results

## Executive Summary
- **Total Issues:** X found
- **Critical:** Y (immediate action required)
- **High Priority:** Z (fix before deployment)
- **Recommendation:** [DEPLOY / HOLD / REWORK]

---

## Critical Issues (Fix Immediately)

### Security (CRITICAL)
1. **SQL Injection** in `src/auth.js:45`
   - Impact: Full database access
   - Fix: Use parameterized queries
   - Priority: IMMEDIATE

2. **Hardcoded Secret** in `src/config.js:12`
   - Impact: API key exposed in source
   - Fix: Move to `.env`, add to `.gitignore`
   - Priority: IMMEDIATE

### Accessibility (CRITICAL - WCAG A)
3. **Missing Form Labels** in `src/components/LoginForm.jsx:20`
   - Impact: Unusable for screen reader users
   - Fix: Add `<label>` elements for all inputs
   - Priority: Before deploy

---

## High Priority (Fix Before Deploy)

### Security (HIGH)
[List high-priority security issues]

### Performance (HIGH)
[List high-priority performance issues]

### Quality (HIGH)
[List high-priority quality issues]

---

## Medium Priority (Fix Soon)

[Organized by category: Security, Quality, Performance, UX, Accessibility]

---

## Low Priority / Suggestions

[Nice-to-have improvements]

---

## Detailed Findings by Dimension

### Security Analysis
[All security findings grouped]

### Quality Analysis
[All quality findings grouped]

### Performance Analysis
[All performance findings grouped]

### UX Analysis
[All UX findings grouped]

### Accessibility Analysis
[All accessibility findings grouped]

---

## Recommendations

**Immediate Actions:**
1. Fix X CRITICAL issues (estimated: Y hours)
2. Address Z HIGH security issues
3. Implement WCAG A compliance fixes

**Before Deployment:**
- All CRITICAL fixed
- All HIGH security fixed
- Basic accessibility (WCAG A)

**Post-Deployment:**
- MEDIUM priority refactoring
- Performance optimizations
- WCAG AA compliance

**Deployment Decision:** [READY / HOLD / REWORK]
```

---

## Phase 5: Return Results

**Present the comprehensive report to user.**

**DO NOT automatically:**
- ‚ùStart fixing issues
- ‚ùCreate a plan to address findings
- ‚ùRefactor code
- ‚ùSuggest building tests

**Instead OFFER next steps:**
```
Review complete! Found X issues (Y critical).

What would you like to do?
- Create a plan to fix critical issues?
- Prioritize which issues to tackle first?
- Need help understanding any findings?
- Want me to fix specific issues?
```

**Let user decide the next action.**


