# DEBUGGING Workflow

**LOG FIRST Pattern - Systematic Investigation Over Guessing**

## When to Use

Use this workflow for:
- Complex bugs (root cause unclear)
- Spent >30 minutes guessing without progress
- Bug involves multiple components
- Intermittent/hard-to-reproduce issues

**Skip for:**
- Obvious bugs (typos, syntax errors, missing imports)
- Simple fixes (<5 lines, cause clear from error message)
- Emergency production issues (fix first, investigate later)

---

## The LOG FIRST Philosophy

**Never guess what the data looks like - ALWAYS log and SEE it first, then fix based on what you observe.**

### Why This Works

**Assumption-Driven Debugging (Common Mistake):**
```
Bug: "Rate limiting not working"
↓
Guess: Maybe middleware not applied?
→ Check code, middleware IS applied
↓
Guess: Maybe express-rate-limit broken?
→ Try reinstalling...
→ Still broken
↓
Guess: Maybe...
→ Waste 2 hours trying random fixes
```

**LOG FIRST Debugging (Systematic):**
```
Bug: "Rate limiting not working"
↓
Add logging to see what's happening
↓
Run test, observe logs:
- "RATE LIMIT EXCEEDED" logged ✅
- Login handler ALSO runs ✅
↓
AHA! Handler not stopping after middleware
↓
Fix: Add return statement
↓
Time: 5 minutes
```

**Real test:** Saved 2 hours by logging first instead of guessing!

---

## Phase 1: Bug Classification

**Before starting, classify the bug:**

### Type 1: Obvious Bug (5-15 min) - Just Fix It!

**Symptoms:**
- Typo in code (`utills` instead of `utils`)
- Syntax error (missing bracket, semicolon)
- Missing import statement
- Off-by-one error (loop boundary)
- Error message clearly indicates problem

**Approach:** Skip LOG FIRST, just fix directly

**Example:** "Cannot find module './utills'" → Fix typo to './utils'

**When:** Root cause immediately visible

---

### Type 2: Unclear Bug (15-60 min) - Use LOG FIRST

**Symptoms:**
- Feature not behaving as expected
- Intermittent failures
- Works in dev, fails in production
- Integration issue between components
- Root cause not obvious from error

**Approach:** Use full LOG FIRST workflow

**Example:** "Rate limiting not blocking requests" → Add logging to see why

**When:** Need to see actual data to understand problem

---

### Type 3: Complex Bug (1-4 hours) - Use LOG FIRST + Risk Analysis

**Symptoms:**
- Race conditions
- Memory leaks
- Performance degradation
- Data corruption
- Multiple interacting systems

**Approach:** LOG FIRST + comprehensive risk analysis

**Example:** "Users occasionally see other users' data" → Race condition investigation

**When:** Bug involves timing, concurrency, or multiple failure modes

---

## Phase 2: Context Gathering

**Process:** Use `codebase-navigation` skill

**Activities:**
1. Understand bug symptoms
2. Locate affected code
3. Map related systems
4. Identify dependencies
5. Check recent changes (`git log`)

**Output:**
- Bug description
- Affected files
- Related components
- Recent changes that might have caused it

---

## Phase 3: LOG FIRST Investigation

**Invoke:** Uses `systematic-debugging` skill

### Step 1: Add Strategic Logging

**Add logging at critical points to see ACTUAL data:**

```javascript
// BEFORE rate limiting middleware
app.use((req, res, next) => {
  console.log('=== BEFORE RATE LIMIT ===');
  console.log('Path:', req.path);
  console.log('Method:', req.method);
  console.log('IP:', req.ip);
  next();
});

// AFTER rate limiting middleware
app.use(rateLimiter);
app.use((req, res, next) => {
  console.log('=== AFTER RATE LIMIT ===');
  console.log('Rate limit info:', req.rateLimit);
  console.log('Limit exceeded?:', req.rateLimit?.limit);
  next();
});

// IN login handler
router.post('/login', async (req, res) => {
  console.log('=== LOGIN HANDLER ===');
  console.log('Handler reached');
  console.log('Body:', req.body);
  // ... existing code
});
```

**Principle:** Log BEFORE making assumptions about what's happening.

---

### Step 2: Reproduce Bug

Run the failing scenario:

```bash
# For rate limiting bug
for i in {1..10}; do
  curl -X POST http://localhost:3000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"test"}'
  echo "Request $i"
done
```

---

### Step 3: Analyze Logs (Observe Reality)

**Read logs to see ACTUAL behavior:**

```
=== BEFORE RATE LIMIT ===
Path: /auth/login
Method: POST
IP: ::1

=== AFTER RATE LIMIT ===
Rate limit info: { limit: 5, current: 6, remaining: 0 }
Limit exceeded?: true

=== LOGIN HANDLER ===
Handler reached        ← ❌ PROBLEM FOUND!
Body: {...}
```

**Observation:** Even though rate limit exceeded, login handler still runs!

**Root Cause Identified:** Rate limiter not stopping the request chain.

---

### Step 4: Form Hypothesis

Based on logs:

```markdown
## Hypothesis

Problem: Rate limiter sets `req.rateLimit.limit = true` but doesn't stop the request.

Cause: express-rate-limit middleware by default only adds metadata, doesn't block request.

Solution: Need to configure middleware to return 429 status when limit exceeded.
```

---

### Step 5: Minimal Fix

**Fix based on observed data (not guesses):**

```javascript
// ❌ BEFORE (just adds metadata)
const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5
});

// ✅ AFTER (actually blocks requests)
const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: req.rateLimit.resetTime
    });
  }
});
```

**Principle:** Fix ONLY what logs showed is broken. Don't refactor unrelated code.

---

### Step 6: Verify Fix

**Run test again:**

```bash
for i in {1..10}; do
  curl -X POST http://localhost:3000/auth/login ...
  echo "Request $i"
done
```

**Expected logs:**
```
Request 1-5: Status 200 (allowed)
Request 6: Status 429 (blocked) ✅
Request 7-10: Status 429 (blocked) ✅
```

**Verification:**
- [ ] Bug reproduced before fix
- [ ] Fix applied
- [ ] Bug no longer occurs
- [ ] No new bugs introduced
- [ ] Tests pass

---

### Step 7: Write Regression Test

**Prevent this bug from returning:**

```typescript
describe('Rate Limiting', () => {
  it('should block requests after limit exceeded', async () => {
    // Make 5 requests (within limit)
    for (let i = 0; i < 5; i++) {
      const res = await request(app).post('/auth/login').send(validCredentials);
      expect(res.status).toBe(200);
    }
    
    // 6th request should be blocked
    const blockedRes = await request(app).post('/auth/login').send(validCredentials);
    expect(blockedRes.status).toBe(429);
    expect(blockedRes.body.error).toBe('Too many requests');
  });
});
```

**Run test:**
```bash
npm test -- rate-limiting
# Expected: PASS ✅
```

---

### Step 8: Clean Up Debug Code

**Remove temporary logging:**

```javascript
// ❌ Remove these
console.log('=== BEFORE RATE LIMIT ===');
console.log('=== AFTER RATE LIMIT ===');
console.log('=== LOGIN HANDLER ===');

// ✅ Keep permanent logging only
logger.info('Login attempt', { email, ip });
logger.warn('Rate limit exceeded', { ip, endpoint });
```

**Verification:**
- [ ] All console.log removed
- [ ] All debugger statements removed
- [ ] Permanent logging remains (logger.info/warn/error)
- [ ] Code is clean

---

### Step 9: Final Verification

**Run full test suite:**
```bash
npm test
# All tests must pass
```

**Check no regressions:**
- [ ] Original bug fixed
- [ ] No new bugs introduced
- [ ] All existing tests still pass
- [ ] New regression test added

---

## Output Format

```markdown
## Bug Fix Complete

### Bug Description
[Original bug symptoms]

### Root Cause
[What was actually wrong - identified from logs]

### Fix Applied
**File:** `src/middleware/rate-limiter.ts`
**Lines Modified:** 8-15
**Change:** Added handler configuration to return 429 when limit exceeded

**Code:**
```diff
- const rateLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 });
+ const rateLimiter = rateLimit({
+   windowMs: 15 * 60 * 1000,
+   max: 5,
+   handler: (req, res) => {
+     res.status(429).json({ error: 'Too many requests' });
+   }
+ });
```

### Investigation Summary
- Time spent: 15 minutes
- Approach: LOG FIRST pattern
- Logs added: 4 strategic points
- Root cause identified from: Actual log output (not guessing)
- Alternative approaches tried: 0 (logs showed exact problem)

### Tests Added
- `tests/rate-limiting.test.ts` - Regression test (blocks after limit)
- Coverage: Rate limiting now 100% covered

### Verification
- ✅ Bug reproduced before fix
- ✅ Fix applied
- ✅ Bug no longer occurs
- ✅ Regression test added
- ✅ All tests passing
- ✅ No debug code remaining
- ✅ Ready to commit

### Learnings
[What we learned from this bug that prevents future similar bugs]

---

## Compared to Ad-Hoc Debugging

WITHOUT LOG FIRST:
- Guessed for 2 hours
- Tried 5 random fixes
- Still not sure why it works now
- No test added (will break again)

WITH LOG FIRST:
- Added logs: 3 minutes
- Ran test, observed: 2 minutes
- Identified root cause: Immediate (saw in logs)
- Fixed: 5 minutes
- Added test: 5 minutes
- **Total: 15 minutes**

Saved: 105 minutes (87% time savings)
```

---

## Token Economics

**Cost:** 15k-30k tokens depending on bug complexity

**Breakdown:**
- Context gathering: 2k
- LOG FIRST investigation: 5k
- Fix implementation: 3-10k
- Regression test: 3-8k
- Verification: 2-5k

**vs Manual Ad-Hoc:**
- Just try fixes: 5-10k tokens
- **cc10x costs 3-6x MORE**

**BUT saves:**
- 1-3 hours of guessing (time value >> tokens)
- Prevents: Same bug recurring (regression test)
- Systematic: Root cause identified (not bandaid fix)

**Worth it when:**
- Bug is complex (root cause not obvious)
- Already spent >30 min without progress
- Want systematic investigation

**Skip when:**
- Obvious fix (typo, syntax error)
- Error message clearly shows problem
- Emergency (fix fast, investigate later)

---

## Remember

The LOG FIRST pattern is the core value of this workflow. Logging first prevents:
- ❌ Assumption-driven debugging (guessing what data looks like)
- ❌ Random fix attempts (trying things without understanding)
- ❌ Incomplete fixes (bandaid over symptom, not root cause)

**Always log, observe, then fix based on reality.**

**This workflow is valuable even for simple bugs because the pattern saves time.**

