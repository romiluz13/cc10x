# Complexity Assessment Template

**Use for Phase 0 and Phase 3c to evaluate feature complexity and cc10x value**

## Complexity Scoring Rubric (1-5 Scale)

### Score 1: TRIVIAL
- **Lines of code:** <50
- **Files affected:** 1
- **Pattern:** Standard (copying existing code)
- **Integration:** None (isolated change)
- **Risk:** None (can't break anything)
- **Examples:** Add config value, fix typo, update text

**Recommendation:** ❌ Skip cc10x - Just do it (5-10 min, 0-2k tokens)

---

### Score 2: SIMPLE
- **Lines of code:** 50-200
- **Files affected:** 2-3
- **Pattern:** Using well-documented library
- **Integration:** Minimal (middleware, single integration point)
- **Risk:** Low (library handles complexity)
- **Examples:** Add rate limiting (express-rate-limit), form validation (Zod), email sending (Nodemailer)

**Recommendation:** ❌ Skip cc10x - Follow library docs (30-60 min, 5k tokens)

**Real test case:** Rate limiting (complexity 2)
- cc10x: 100k tokens, 90 min, tests failed
- Manual: 5k tokens, 30 min, working code
- **Verdict: Manual was 20x better**

---

### Score 3: MODERATE
- **Lines of code:** 200-500
- **Files affected:** 4-6
- **Pattern:** Established (exists in codebase)
- **Integration:** Multiple points (3-5 components)
- **Risk:** Moderate (some edge cases to handle)
- **Examples:** Pagination with caching, file upload with storage, search with filters

**Recommendation:** ⚠️ Maybe - Show tradeoffs, let user decide

**Tradeoffs:**
- cc10x: 100k tokens, comprehensive docs, systematic approach
- Manual: 15k tokens, faster iteration, ad-hoc
- **Worth systematic if:** Team alignment valued, documentation needed
- **Manual better if:** Solo dev, token budget matters

---

### Score 4: COMPLEX
- **Lines of code:** 500-1,000
- **Files affected:** 7-15
- **Pattern:** Novel (not in codebase yet)
- **Integration:** Many points (6-10 components)
- **Risk:** High (architecture decisions needed)
- **Examples:** Real-time notifications (WebSockets), complex state management, API versioning

**Recommendation:** ✅ Use cc10x - Prevents architecture mistakes

**Why cc10x adds value:**
- Novel patterns need design decisions
- Multiple integration points need coordination
- Architecture mistakes costly to fix later
- Risk mitigation planning prevents incidents

**Token economics:**
- cc10x: 60-120k tokens
- Manual: 20-30k tokens
- **4-6x MORE but prevents costly rework**

---

### Score 5: VERY COMPLEX
- **Lines of code:** >1,000
- **Files affected:** 15+
- **Pattern:** Novel + challenging
- **Integration:** Extensive (10+ components)
- **Risk:** Critical (security, data integrity, scalability)
- **Examples:** Multi-tenancy with data isolation, payment processing (Stripe integration), real-time collaboration

**Recommendation:** ✅✅ Use cc10x - Essential for success

**Why cc10x essential:**
- Architecture decisions critical (wrong choice = rewrite)
- Security analysis prevents breaches
- File manifest prevents scope explosion
- Deployment strategy essential for safety
- Risk analysis identifies edge cases humans miss

**Token economics:**
- cc10x: 120-180k tokens
- Manual: 40-60k tokens
- **3-4x MORE but one prevented breach >> infinite tokens**

---

## Assessment Factors

### Factor 1: File Count

**Quick heuristic:**
- 1-3 files = Simple (1-2)
- 4-6 files = Moderate (3)
- 7-15 files = Complex (4)
- 15+ files = Very Complex (5)

---

### Factor 2: Pattern Novelty

**Is this pattern already in the codebase?**
- Exists and well-documented = -1 to score (simpler)
- Exists but needs adaptation = 0 (neutral)
- Novel but documented (library) = 0 (neutral)
- Novel and custom = +1 to score (more complex)

---

### Factor 3: Integration Points

**How many components does this touch?**
- 0-1 integration points = Simple
- 2-3 integration points = Moderate
- 4-7 integration points = Complex
- 8+ integration points = Very Complex

---

### Factor 4: Risk Level

**Domain risk assessment:**
- General features = Use file count
- **Auth/payments/data = Automatic 4-5 (high-risk overrides)**

**Why:** Security breaches, payment failures, data corruption have infinite cost.

---

### Factor 5: Team vs Solo

**Team projects:** +0.5 to score (documentation valuable)
**Solo projects:** -0.5 to score (documentation less critical)

---

## Assessment Template

```markdown
## Complexity Assessment: [Feature Name]

### Scoring Factors

**Files affected:** [X] files → Score: [Y]
- [List key files]

**Pattern novelty:** [Novel/Established/Library] → Adjustment: [+1/0/-1]
- [Explanation]

**Integration points:** [X] → Score: [Y]
- [List integration points]

**Risk level:** [Low/Moderate/High/Critical]
- Domain: [general/auth/payment/data]
- Automatic adjustment: [if high-risk]

**Team/Solo:** [Team/Solo] → Adjustment: [+0.5/-0.5]

---

### Calculation

Base score: [files + integration complexity]
Novelty adjustment: [+/-]
Risk adjustment: [if applicable]
Team adjustment: [+/-]

**Final Score: [X]/5**

---

### Interpretation

[Based on score, provide recommendation using rubric above]

**Recommendation:** [Skip cc10x / Maybe / Use cc10x]

**Rationale:**
[Specific reasons for THIS feature]

---

### Token Economics

**cc10x planning:** ~[X]k tokens
**cc10x building:** ~[Y]k tokens
**Total:** ~[Z]k tokens

**Manual equivalent:** ~[X]k tokens

**Multiplier:** [Z]x MORE with cc10x

**Worth it because:**
[Specific value for THIS feature, or "NOT worth it - manual better"]

---

### Decision

**If score 1-2:** Strongly recommend manual
**If score 3:** Show this assessment, let user decide
**If score 4-5:** Proceed with confidence
```

---

## Common Defaults by Domain

### Authentication Features

```markdown
## Intelligent Defaults: Authentication

1. OAuth: NO (defer to v2)
   - v1: Email/password only
   - v2: Add Google, GitHub OAuth

2. Email verification: NO (defer to v2)
   - v1: Users can login immediately
   - v2: Add email confirmation

3. Password reset: NO (defer to v2)
   - v1: Contact admin for reset
   - v2: Self-service reset flow

4. Token expiry: 15min access, 7-day refresh
   - Industry standard
   - Balances security and UX

5. Token storage: httpOnly cookies
   - Prevents XSS attacks
   - Best practice for web apps

6. Hashing: bcrypt cost factor 12
   - Recommended by OWASP
   - Balances security and performance

7. Rate limiting: 5 attempts per 15 min
   - Prevents brute force
   - OWASP recommendation
```

### API Features

```markdown
## Intelligent Defaults: API

1. Format: REST (not GraphQL)
   - Simpler, more common
   - GraphQL only if mentioned

2. Response format: JSON
   - Standard for REST APIs

3. Pagination: Offset-based (limit/skip)
   - Simpler than cursor-based
   - Sufficient for most use cases

4. Versioning: NO (v1 only)
   - Add versioning when needed

5. Rate limiting: 100 req/15min (general endpoints)
   - Reasonable for most APIs
```

### Database Features

```markdown
## Intelligent Defaults: Database

1. Database: MongoDB
   - User preference from rules

2. ORM: Mongoose
   - Schema validation
   - Standard for MongoDB + Node.js

3. Migrations: NO (for MongoDB)
   - MongoDB is schemaless
   - Migrations rarely needed

4. Indexes: On frequently queried fields
   - Email (for lookups)
   - User ID (for relationships)
```

---

## How to Use This Template

### In Phase 0 (Quick Complexity Check)

Use simplified version:
1. Count files (quick estimate)
2. Library or novel?
3. High-risk domain?
4. Calculate score
5. Make recommendation

**Time:** 30 seconds - 2 minutes

---

### In Phase 0a (Quick Default Plan)

Use this template to:
1. Present assumptions clearly
2. Offer 3 options (proceed/customize/manual)
3. Get user validation
4. Avoid 120k token waste

**Time:** 3-5 minutes, 3-5k tokens

---

### In Phase 3c (Final Complexity Assessment)

Use full assessment after architecture analysis:
1. All factors analyzed
2. Detailed rationale
3. Token economics comparison
4. Final recommendation with context

**Time:** 5-10 minutes, within planning workflow

---

## Remember

The goal is to:
1. **Assess quickly** (don't overthink, use heuristics)
2. **Be honest** (recommend manual when appropriate)
3. **Validate assumptions** (present defaults, get user input)
4. **Save tokens** (stop early if user chooses manual)

**Don't inflate complexity to justify cc10x!**

**Use this template to provide honest, helpful assessments.**

