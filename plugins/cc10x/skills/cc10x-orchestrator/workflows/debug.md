# DEBUGGING Workflow - LOG FIRST Approach

**Triggered by:** User reports bug, something not working



---

## Phase 0: Bug Complexity Assessment

**Quick triage:**

**IF OBVIOUS (typo, syntax, missing import):**
```
This looks like a simple fix:
- Typo: `utills` → `utils`
- Missing import: Add `import X from 'Y'`
- Syntax: Missing semicolon

Recommendation: Just fix it!

Want me to fix it anyway? (yes/no)
```

**IF COMPLEX (root cause unclear):**
- Proceed with LOG FIRST systematic approach

---

## Phase 1: LOG FIRST - Add Strategic Logging

**The Philosophy:**
> Never guess what data looks like - ALWAYS log and see it first

**Add logging at key points:**

1. **Function entry:** Log inputs
2. **Before conditionals:** Log condition values
3. **Before operations:** Log state before transform
4. **After operations:** Log results
5. **Before return:** Log output

**Example:**
```javascript
function processPayment(userId, amount) {
  console.log('[DEBUG] processPayment called:', {userId, amount});
  
  const user = await getUser(userId);
  console.log('[DEBUG] User loaded:', user);
  
  if (user.balance >= amount) {
    console.log('[DEBUG] Balance sufficient, processing...');
    // ...
  } else {
    console.log('[DEBUG] Insufficient balance:', {balance: user.balance, required: amount});
  }
}
```

---

## Phase 2: Reproduce with Logging

**Run the failing scenario:**
```bash
# Run tests or reproduce manually
npm test
# or
curl -X POST http://localhost:3000/endpoint
```

**Capture logs:**
- Save output to file
- Review log sequence
- Identify where behavior diverges from expected

---

## Phase 3: Analyze Logs

**Look for:**
1. **Data surprises:** "Expected X, got Y"
2. **Missing steps:** Function not called when it should
3. **Wrong order:** Steps execute in unexpected sequence
4. **State issues:** Variable has wrong value at critical point
5. **Async issues:** Race conditions, promises not awaited

**Example Analysis:**
```
Log: [DEBUG] User loaded: null
Expected: User object

AHA! getUser() returns null
→ Either user doesn't exist OR query is wrong
→ Add logging inside getUser() to investigate
```

---

## Phase 4: Form Hypothesis

**Based on logs, hypothesize root cause:**

```markdown
## Hypothesis

**What:** getUser() returns null

**Why (possible causes):**
1. User ID passed is undefined
2. Database query has wrong field name
3. User doesn't exist in test database
4. Async issue - not awaiting query

**Most likely:** #1 (userId is undefined)
**Evidence:** Log shows userId: undefined in processPayment call
```

---

## Phase 5: Test Hypothesis

**Add targeted logging to verify:**

```javascript
function processPayment(userId, amount) {
  if (!userId) {
    console.error('[DEBUG] BUG FOUND: userId is undefined!');
    console.trace(); // Show call stack
  }
  // ...
}
```

**Run again → Confirms hypothesis**

---

## Phase 6: Implement Minimal Fix

**Fix ONLY what's needed:**

```javascript
// Before (bug):
router.post('/payment', async (req, res) => {
  await processPayment(req.body.user_id, req.body.amount);
});

// After (fixed):
router.post('/payment', async (req, res) => {
  const userId = req.body.userId; // Was reading wrong field!
  await processPayment(userId, req.body.amount);
});
```

---

## Phase 7: Verify Fix

**Run tests again:**
```bash
npm test
```

**Confirm:**
- Tests pass
- Bug no longer reproduces
- No new issues introduced

---

## Phase 8: Clean Up Logging

**Remove debug logs:**
- Keep strategic logging (errors, critical points)
- Remove verbose debug logs added during investigation
- Don't leave `console.log` in production code

---

## Phase 9: Return Results

**Report to user:**

```markdown
## Bug Fixed!

**Root Cause:** Field name mismatch
- Code read: `req.body.user_id`
- Client sent: `req.body.userId`

**Fix:** Updated field name to match API contract

**Verification:** All tests passing

**Files Modified:**
- src/routes/payment.js (line 45)

**Prevention:** Consider adding request validation middleware
```


