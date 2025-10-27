---
name: systematic-debugging
description: Scientific debugging methodology for finding and fixing bugs efficiently. Use when debugging complex issues.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Systematic Debugging Methodology

Scientific approach to finding and fixing bugs efficiently.

## The Scientific Method for Debugging

### 1. Observe
- What is the actual behavior?
- What is the expected behavior?
- When did it start?
- Can you reproduce it consistently?

### 2. Question
- What changed recently?
- Under what conditions does it occur?
- What doesn't trigger the bug?
- Who/what is affected?

### 3. Hypothesize
- List possible causes
- Rate likelihood (1-5)
- Identify which to test first

### 4. Test
- Design experiment to test hypothesis
- Execute test in isolation
- Document results

### 5. Analyze
- Did the test prove or disprove hypothesis?
- What did we learn?
- Next hypothesis to test?

### 6. Conclude
- Root cause identified?
- Fix implemented?
- Verified fix works?

## LOG FIRST Methodology

**BEFORE deep investigation, add strategic logs:**

```typescript
// ❌ No logging - flying blind
function processOrder(order: Order) {
  const total = calculateTotal(order.items);
  const payment = processPayment(total);
  updateInventory(order.items);
  return { success: true };
}

// ✅ Strategic logging
function processOrder(order: Order) {
  logger.debug('Processing order', { orderId: order.id, itemCount: order.items.length });
  
  const total = calculateTotal(order.items);
  logger.debug('Total calculated', { total });
  
  try {
    const payment = processPayment(total);
    logger.info('Payment processed', { paymentId: payment.id, amount: total });
  } catch (error) {
    logger.error('Payment failed', { orderId: order.id, error });
    throw error;
  }
  
  updateInventory(order.items);
  logger.info('Order processed successfully', { orderId: order.id });
  
  return { success: true };
}
```

## Reproduction Steps

### Make It Reproducible
```markdown
## Bug Report Template

**Actual Behavior:**
[What happens]

**Expected Behavior:**
[What should happen]

**Steps to Reproduce:**
1. Navigate to /page
2. Click button X
3. Enter value Y
4. Observe error

**Environment:**
- Browser: Chrome 120
- OS: macOS 14
- User role: Admin
- Data: Order #12345

**Frequency:**
- [ ] Always
- [ ] Sometimes (50%)
- [ ] Rare (< 10%)

**First Occurred:**
- Date: 2024-10-20
- Version: v2.3.0
- Recent changes: [List]
```

## Isolation Techniques

### Binary Search Debugging
```bash
# Find which commit introduced bug
git bisect start
git bisect bad HEAD
git bisect good v1.0.0

# Git will checkout middle commit
# Test if bug exists
git bisect bad  # or git bisect good

# Repeat until found
```

### Disable Features
```typescript
// Isolate which feature causes issue
const FEATURES = {
  caching: false,      // Disable one at a time
  validation: true,
  notifications: true
};

if (FEATURES.caching && cache.has(key)) {
  return cache.get(key);
}
```

### Minimal Reproduction
```typescript
// Reduce to minimal code that shows bug
// ❌ Complex test case
test('full e2e flow', async () => {
  // 100 lines of setup
});

// ✅ Minimal reproduction
test('payment fails with negative amount', async () => {
  await expect(processPayment(-100)).rejects.toThrow();
});
```

## Common Bug Patterns

### Off-by-One Errors
```typescript
// ❌ Bug
for (let i = 0; i <= arr.length; i++) {  // Should be i < arr.length
  console.log(arr[i]);  // arr[arr.length] is undefined!
}

// ✅ Fix
for (let i = 0; i < arr.length; i++) {
  console.log(arr[i]);
}
```

### Race Conditions
```typescript
// ❌ Bug - race condition
let counter = 0;
async function increment() {
  const current = counter;  // Read
  await delay(10);
  counter = current + 1;    // Write (might be stale)
}

// ✅ Fix - atomic operation
let counter = 0;
async function increment() {
  counter += 1;  // Atomic
}

// ✅ Better - mutex/lock
const mutex = new Mutex();
async function increment() {
  await mutex.lock();
  counter += 1;
  mutex.unlock();
}
```

### Null/Undefined Issues
```typescript
// ❌ Bug
function getUser(id: string) {
  const user = users.find(u => u.id === id);
  return user.name;  // Error if undefined!
}

// ✅ Fix
function getUser(id: string): string | undefined {
  const user = users.find(u => u.id === id);
  return user?.name;
}
```

### Memory Leaks
```typescript
// ❌ Bug - event listener not removed
class Component {
  mount() {
    window.addEventListener('resize', this.handleResize);
  }
}

// ✅ Fix - cleanup
class Component {
  mount() {
    window.addEventListener('resize', this.handleResize);
  }
  
  unmount() {
    window.removeEventListener('resize', this.handleResize);
  }
}
```

### Async/Await Errors
```typescript
// ❌ Bug - missing await
async function loadData() {
  const data = fetchData();  // Missing await!
  console.log(data);  // Logs Promise, not data
}

// ✅ Fix
async function loadData() {
  const data = await fetchData();
  console.log(data);
}
```

## Debugging Tools

### Console Debugging
```typescript
// Levels of logging
console.debug('Detailed info');
console.log('General info');
console.info('Important info');
console.warn('Warning');
console.error('Error');

// Grouping
console.group('Processing order');
console.log('Step 1');
console.log('Step 2');
console.groupEnd();

// Timing
console.time('operation');
expensiveOperation();
console.timeEnd('operation'); // "operation: 123.45ms"

// Tables
console.table([
  { name: 'Alice', age: 25 },
  { name: 'Bob', age: 30 }
]);
```

### Debugger Statement
```typescript
function complexFunction(data) {
  // Pause execution here when debugger is open
  debugger;
  
  // Inspect variables in browser dev tools
  const result = processData(data);
  return result;
}
```

### Network Debugging
```bash
# Chrome DevTools Network tab
# Filter by:
# - XHR/Fetch (API calls)
# - Doc (HTML pages)
# - CSS, JS, Img

# Check:
# - Status codes
# - Request/response headers
# - Request/response body
# - Timing breakdown
```

### Git Blame
```bash
# Find who/when changed line
git blame src/file.ts

# See commit details
git show <commit-hash>

# Find when bug introduced
git log -S "buggy code" --source --all
```

## Debugging Checklist

### Before Investigation
- [ ] Can reproduce bug consistently?
- [ ] Have minimal reproduction?
- [ ] Checked recent changes (git log)?
- [ ] Reviewed error messages/stack traces?
- [ ] Added strategic logging?

### During Investigation
- [ ] Formed hypothesis about cause?
- [ ] Tested hypothesis in isolation?
- [ ] Eliminated impossible causes?
- [ ] Checked assumptions?
- [ ] Verified data at each step?

### After Fix
- [ ] Root cause identified?
- [ ] Fix implemented?
- [ ] Regression test added?
- [ ] All tests pass?
- [ ] No side effects?
- [ ] Documented in commit message?

## Root Cause Analysis (5 Whys)

```markdown
## Example: User login fails

Why? → Token validation fails
Why? → Token expired
Why? → Token lifetime is 1 minute
Why? → Configuration used wrong unit (seconds vs milliseconds)
Why? → No validation of config values

**Root Cause:** Missing config validation
**Fix:** Add config validation + default values
**Prevention:** Add config schema validation
```

## Debugging Strategies by Symptom

### "Works on my machine"
- Check environment variables
- Compare dependencies (package.json)
- Check OS-specific code
- Verify database state
- Check permissions

### Intermittent/Flaky
- Race condition?
- Timing-dependent?
- Random data in tests?
- External service dependency?
- Cache issues?

### Performance Issue
- Profile with dev tools
- Check database queries (N+1?)
- Look for memory leaks
- Check bundle size
- Verify caching

### UI Not Updating
- Check state management
- Verify event handlers
- Check component re-render
- Inspect React DevTools
- Check mutations vs immutability

## Advanced Debugging

### Time Travel Debugging
```typescript
// Redux DevTools
// - Inspect every action
// - Time travel through state changes
// - Export/import state for reproduction
```

### Remote Debugging
```bash
# Node.js
node --inspect app.js

# Chrome
# chrome://inspect
# Connect to remote target
```

### Production Debugging
```typescript
// Error tracking
import * as Sentry from '@sentry/node';

Sentry.init({ dsn: process.env.SENTRY_DSN });

try {
  riskyOperation();
} catch (error) {
  Sentry.captureException(error);
  throw error;
}
```

## When Stuck

1. **Take a break** - Fresh eyes help
2. **Explain to someone** - Rubber duck debugging
3. **Read docs again** - Missed something?
4. **Check issues** - Known bug?
5. **Simplify** - Reduce to minimal case
6. **Question assumptions** - What if X isn't true?
7. **Start over** - Clean slate approach

## Documentation

```markdown
# Bug Fix Report

## Issue
Payment processing fails for orders > $1000

## Root Cause
Integer overflow in cents calculation:
1000 * 100 = 100,000 exceeds INT16_MAX (32,767)

## Investigation
1. Added logging to payment flow
2. Identified overflow at line 45
3. Verified with test case
4. Confirmed fix resolves issue

## Solution
Changed `amount_cents` column from INT16 to INT32

## Prevention
- Added validation for max order amount
- Added test for large amounts
- Added monitoring alert for payment failures

## Files Changed
- schema.sql
- payment.service.ts
- payment.test.ts
```

## Debugging Mindset

✅ **Do:**
- Be systematic
- Test one thing at a time
- Document findings
- Think scientifically
- Check assumptions
- Use version control

❌ **Don't:**
- Change multiple things at once
- Guess randomly
- Skip logging
- Ignore error messages
- Give up too soon
- Leave debug code in production

