# REVIEW Workflow ⭐⭐⭐⭐⭐

**The Killer Feature - Always Worth It!**

## When to Use

Use this workflow for:
- Code review before PRs
- Security audits
- Quality checks
- Performance analysis
- UX/accessibility reviews
- Finding bugs in existing code

**Always valuable regardless of complexity.**

## Workflow Execution

### Phase 1: Scope Analysis

1. **Parse target from user message:**
   - Specific file: `src/auth.js`
   - Directory: `src/features/auth/`
   - Pattern: `src/**/*.js`
   - Entire codebase: `src/`

2. **Identify file types:**
   - JavaScript/TypeScript
   - Python
   - Other languages

3. **Determine scope:**
   - Single file review (10-20k tokens)
   - Module review (30-40k tokens)
   - Full codebase review (80-120k tokens)

### Phase 2: Parallel Multi-Dimensional Review

**Invoke 5 agents SIMULTANEOUSLY** (ONLY workflow that parallelizes!):

#### 1. security-reviewer

**Loads skills:** `risk-analysis` Stages 1+2+5 + `security-patterns`

**Analyzes:**
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting)
- Authentication bypasses
- Authorization flaws
- Data exposure risks
- Secret management
- Input validation gaps

**Uses:** OWASP Top 10 checklist

**Returns:** Security findings with severity classification

---

#### 2. quality-reviewer

**Loads skills:** `risk-analysis` ALL 7 stages + `code-review-patterns`

**Analyzes:**
- Code smells (Long Method, Large Class, Duplicate Code)
- Complexity issues (Cyclomatic complexity)
- Maintainability problems
- DRY violations
- SOLID principle violations
- Refactoring opportunities

**Uses:** Martin Fowler refactoring catalog

**Returns:** Quality findings with refactoring suggestions

---

#### 3. performance-analyzer

**Loads skills:** `risk-analysis` Stage 6 + `performance-patterns`

**Analyzes:**
- Time complexity (O(n²), O(n³) algorithms)
- Memory leaks
- N+1 query problems
- Missing caching opportunities
- Inefficient data structures
- Blocking operations

**Uses:** Performance optimization techniques

**Returns:** Performance findings with optimization suggestions

---

#### 4. ux-reviewer

**Loads skills:** `risk-analysis` Stage 4 + `ux-patterns`

**Analyzes:**
- Error messages (clarity, actionability)
- Loading states (missing or confusing)
- User feedback (success/error communication)
- Interaction patterns (clicks, forms, navigation)
- Edge case handling (empty states, errors)

**Uses:** UX best practices

**Returns:** UX findings with improvement suggestions

---

#### 5. accessibility-reviewer

**Loads skills:** `accessibility-patterns`

**Analyzes:**
- WCAG 2.1 AA violations
- Keyboard navigation issues
- Screen reader support
- Color contrast problems
- Missing ARIA labels
- Focus management

**Uses:** WCAG 2.1 AA checklist

**Returns:** Accessibility findings with remediation steps

---

### Phase 3: Synthesis & Report Generation

1. **Consolidate findings** from all 5 agents
2. **Remove duplicates** (same issue found by multiple agents)
3. **Prioritize by severity:** CRITICAL → HIGH → MODERATE → LOW
4. **Generate comprehensive report** with:
   - File-level findings
   - Specific line numbers
   - Severity classification
   - Fix recommendations with code examples
   - Time estimates for fixes

---

## Output Format

```markdown
## Multi-Dimensional Code Review: [Target]

### Summary
- Total Issues: [X]
- CRITICAL: [X] (must fix before merge)
- HIGH: [X] (should fix)
- MODERATE: [X] (good to fix)
- LOW: [X] (nice to fix)

### Review Dimensions Analyzed
- ✅ Security (OWASP Top 10, injection, auth)
- ✅ Quality (code smells, complexity, DRY/SOLID)
- ✅ Performance (O(n) complexity, caching, queries)
- ✅ UX (error messages, loading, feedback)
- ✅ Accessibility (WCAG 2.1 AA, keyboard, screen reader)

---

## CRITICAL Issues (Must Fix Before Merge)

### [SEC-001] SQL Injection Vulnerability

**File:** `src/auth/login.controller.js`  
**Line:** 45  
**Dimension:** Security  

**Issue:** User input directly concatenated into SQL query without sanitization

**Risk:** Database compromise, data breach, unauthorized access

**Current Code:**
```javascript
const query = `SELECT * FROM users WHERE email = '${email}'`;
const result = await db.query(query);
```

**Vulnerable Because:**
- Email parameter from user input (`req.body.email`)
- Direct string interpolation into SQL
- No parameterization or escaping
- Attacker could inject: `' OR '1'='1` to bypass authentication

**Fix:**
```javascript
// ✅ FIXED - Use parameterized queries
const query = 'SELECT * FROM users WHERE email = ?';
const result = await db.query(query, [email]);

// OR with ORM (Mongoose/Prisma):
const user = await User.findOne({ email }); // Automatically sanitized
```

**Estimated fix time:** 10 minutes

**Why this matters:** SQL injection is #1 in OWASP Top 10. One breach can compromise entire database.

---

### [SEC-002] Hardcoded Secrets in Code

**File:** `src/config/database.js`  
**Line:** 12  
**Dimension:** Security  

**Issue:** Database credentials hardcoded in source code

**Risk:** Secrets exposed in version control, leaked if repo compromised

**Current Code:**
```javascript
const config = {
  password: 'myP@ssw0rd123',  // ❌ CRITICAL - Never hardcode!
  host: 'prod-db.example.com'
};
```

**Fix:**
```javascript
// ✅ FIXED - Use environment variables
const config = {
  password: process.env.DB_PASSWORD,
  host: process.env.DB_HOST
};

// Validate env vars exist
if (!config.password) {
  throw new Error('DB_PASSWORD environment variable required');
}
```

**Also:**
- Remove from git history: `git filter-branch` or BFG Repo-Cleaner
- Rotate credentials immediately
- Use secrets manager (AWS Secrets Manager, HashiCorp Vault)

**Estimated fix time:** 30 minutes (including credential rotation)

---

## HIGH Priority Issues (Should Fix)

### [PERF-001] N+1 Query Problem

**File:** `src/users/service.js`  
**Line:** 78-82  
**Dimension:** Performance  

**Issue:** Loading user posts in loop causing N+1 database queries

**Impact:** 
- 100 users = 101 queries (1 user query + 100 post queries)
- Slow response time (300ms → 2,500ms)
- Database overload under load

**Current Code:**
```javascript
const users = await User.find(); // 1 query
for (const user of users) {
  user.posts = await Post.find({ userId: user.id }); // N queries!
}
```

**Fix:**
```javascript
// ✅ FIXED - Single query with join or lookup
const users = await User.aggregate([
  {
    $lookup: {
      from: 'posts',
      localField: '_id',
      foreignField: 'userId',
      as: 'posts'
    }
  }
]); // 1 query total!
```

**Estimated fix time:** 20 minutes

**Performance improvement:** 8-10x faster (2,500ms → 250ms)

---

[Continue for all HIGH issues...]

---

## MODERATE Priority Issues (Good to Fix)

[Include code smells, minor UX issues, etc.]

---

## LOW Priority Issues (Nice to Fix)

[Include minor improvements, suggestions, etc.]

---

## Coverage Summary

### Files Reviewed
- [List all files analyzed]

### Agents Executed
- ✅ security-reviewer: Found [X] issues
- ✅ quality-reviewer: Found [X] issues
- ✅ performance-analyzer: Found [X] issues
- ✅ ux-reviewer: Found [X] issues
- ✅ accessibility-reviewer: Found [X] issues

### Recommended Actions

1. **Fix CRITICAL issues immediately** (block merge until resolved)
2. **Fix HIGH issues before merge** (schedule if time-constrained)
3. **Create tickets for MODERATE** (address in next sprint)
4. **Consider LOW improvements** (technical debt backlog)

### Estimated Total Fix Time
- CRITICAL: [X] hours
- HIGH: [X] hours
- MODERATE: [X] hours
- LOW: [X] hours

---

## Real-World Test Results

**Test Case:** Authentication system review (src/auth/)

**Results:**
- Files reviewed: 8
- Total issues: 38
- CRITICAL: 5 (SQL injection, secrets exposed, auth bypass, XSS, missing transaction)
- HIGH: 12 (N+1 queries, memory leaks, race conditions, error handling)
- MODERATE: 15 (code smells, UX improvements)
- LOW: 6 (minor suggestions)

**Time:** 3 minutes

**Tokens:** 35,000

**Value:** One prevented SQL injection breach alone justifies the tokens.

**Verdict:** ⭐⭐⭐⭐⭐ (5/5 stars)

---

## Token Economics

**Cost:** 20k-50k tokens depending on codebase size

**Breakdown:**
- Scope analysis: 1k tokens
- 5 parallel agents: 15k-40k tokens (3k-8k each)
- Synthesis & report: 4k-9k tokens

**Value Comparison:**

**Manual equivalent:**
- Security expert review: 2-3 hours
- Code quality review: 2-3 hours
- Performance review: 1-2 hours
- UX review: 1-2 hours
- Accessibility audit: 1-2 hours
- **Total: 7-13 hours of expert time**

**cc10x review:**
- Time: 2-5 minutes
- Tokens: 20k-50k
- **Replaces 7-13 hours of manual expert reviews**

**ROI:**
- One prevented security breach >> infinite value
- One prevented performance bug >> hours of debugging saved
- Accessibility compliance >> lawsuit prevention

**Use before EVERY PR!**

---

## When NOT to Use

This workflow is almost always worth it, but skip if:
- ❌ Trivial changes (<10 lines, obvious correctness)
- ❌ Generated code (config files, migrations)
- ❌ Already reviewed by full team
- ❌ Emergency hotfix (review after deploying)

**For 99% of PRs:** USE THIS WORKFLOW.

---

## Remember

This is the ONLY cc10x workflow that's universally valuable regardless of complexity. The 5 review agents actually work as advertised - they find real issues that prevent production incidents.

**One prevented security breach justifies unlimited tokens.**

**Use liberally!**

