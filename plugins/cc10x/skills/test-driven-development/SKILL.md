---
name: test-driven-development
description: Enforces strict RED-GREEN-REFACTOR methodology for all code implementation with mandatory test verification to prevent false success reports. Provides 3 progressive stages (TDD cycle patterns, quick reference for test-first development, and mandatory verification procedures). Use when implementing features with strict test-first discipline, fixing bugs with reproducible tests, or ensuring code quality through TDD. Requires writing failing test FIRST before any production code. Loaded by tdd-enforcer agent during BUILDING and DEBUGGING workflows. Stage 3 (Mandatory Verification) prevents false "all tests passing" claims by requiring independent verification (run actual test command, verify exit code equals zero, see results with your eyes). Critical for preventing the pattern where agents report success when tests actually failed.
license: MIT
---

# Test-Driven Development (TDD)

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: Test-Driven Development (TDD)
- **Purpose**: Enforce test-first methodology (RED-GREEN-REFACTOR)
- **When**: All feature implementation, bug fixes, behavior changes
- **Core Rule**: NO production code without failing test first
- **Sections Available**: Quick Reference, Detailed Guide, Examples, Anti-Patterns

---

### Stage 2: Quick Reference

#### The Iron Law
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
**Write code before test? Delete it. Start over.**

#### RED-GREEN-REFACTOR Cycle
```
TDD Progress:
- [ ] RED: Write failing test
- [ ] Verify: Confirm test fails correctly
- [ ] GREEN: Write minimal code to pass
- [ ] Verify: Confirm test passes
- [ ] REFACTOR: Clean up (keep green)
- [ ] Next feature
```

#### Quick Tips
**RED (Failing Test)**:
- One behavior per test
- Descriptive names (no "test1")
- Watch it fail before coding

**GREEN (Minimal Code)**:
- Simplest code that passes
- Don't add extra features
- Run all tests

**REFACTOR (Clean Up)**:
- Only after tests pass
- Keep tests green
- Don't add behavior

#### Red Flags 🚨
- ❌ Code exists before test
- ❌ Test passes immediately
- ❌ "I already tested manually"
- ❌ "Just this once"
- ❌ "Keep as reference"

**If rationalizing → You're doing it wrong**

#### Test Commands
```bash
# Run specific test
npm test path/to/test.test.ts

# Run all tests
npm test

# Watch mode
npm test -- --watch
```

---

### Stage 3: Detailed Content

## Detailed TDD Guide

### RED - Write Failing Test

Write one minimal test showing desired behavior.

```typescript
// ✅ Good: Clear, tests real behavior
test('retries operation 3 times on failure', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

```typescript
// ❌ Bad: Unclear, tests implementation
test('works', () => {
  const result = fn();
  expect(result).toBeTruthy();
});
```

**Requirements**:
- **One behavior per test** - Don't test multiple things
- **Descriptive name** - Explains what behavior is tested
- **Real code** - Avoid excessive mocking (tests become brittle)

### Verify RED - Watch It Fail

```bash
npm test path/to/test.test.ts
```

**Confirm**:
- ✅ Test **fails** (not errors, actual failure)
- ✅ Failure message is **expected** ("retryOperation is not defined")
- ✅ Fails because **feature is missing** (not a bug in test)

**Common Issues**:

| Symptom | Problem | Solution |
|---------|---------|----------|
| Test passes | Testing existing behavior | Write test for new behavior |
| Test errors | Syntax error or wrong import | Fix error first |
| Wrong failure | Test logic is incorrect | Fix test before coding |

### GREEN - Minimal Code

Write **simplest code** to pass test. No more, no less.

```typescript
// ✅ Good: Minimal, passes test
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```

```typescript
// ❌ Bad: Over-engineered, not required by test
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
    jitter?: boolean;
  }
): Promise<T> {
  // YAGNI - You Aren't Gonna Need It
  // Test only requires 3 retries, nothing else
}
```

**Don't**:
- ❌ Add features not required by test
- ❌ Refactor other code (wait for REFACTOR phase)
- ❌ Over-engineer for future needs

### Verify GREEN - Watch It Pass

```bash
npm test
```

**Confirm**:
- ✅ **New test passes**
- ✅ **All other tests pass** (no regressions)
- ✅ **No errors or warnings**

If any test fails → Fix before moving to REFACTOR

### REFACTOR - Clean Up

**Only after tests are green**:
- Remove duplication
- Improve variable/function names
- Extract helper functions
- Simplify logic

**Rules**:
- ✅ Keep all tests green
- ✅ Run tests after each refactor
- ❌ Don't add behavior (that's a new test)

```typescript
// Example refactor: Extract magic number
const MAX_RETRY_ATTEMPTS = 3;

async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < MAX_RETRY_ATTEMPTS; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === MAX_RETRY_ATTEMPTS - 1) throw e;
    }
  }
  throw new Error('unreachable');
}
```

## Why Test-First Matters

### Tests-After Don't Work

**"I'll write tests after"**:
- Test passes immediately → Proves nothing
- You test what code does, not what it should do
- Edge cases missed (code already "works")

**Test-first guarantees**:
- ✅ Test actually catches the bug
- ✅ Test verifies behavior, not implementation
- ✅ Edge cases discovered before coding

### Manual Testing Isn't Enough

**"Already manually tested"**:
- Ad-hoc (not repeatable)
- No record (forgotten tomorrow)
- Can't run on every change

**Automated tests**:
- ✅ Run in <1 second
- ✅ Run on every change
- ✅ Document expected behavior

### Sunk Cost Fallacy

**"Deleting code is wasteful"**:
- Keeping **unverified** code is technical debt
- You'll adapt it → That's testing-after

**Delete means delete**:
- Don't keep as "reference"
- Don't look at it
- Implement fresh from tests

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "Tests-after achieve same goal" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Keep as reference" | You'll adapt it. That's testing after. **Delete means delete.** |
| "TDD is dogmatic" | TDD is pragmatic: Finds bugs before commit, prevents regressions. |
| "Don't know how to test it" | Design problem - if hard to test, hard to use. Simplify. |
| "Tests slow me down" | TDD speeds you up: Fewer bugs, less debugging, safer refactoring. |

## Bug Fix Example

**Scenario**: Empty email accepted (should be rejected)

### RED - Write Failing Test
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**:
```bash
npm test
# FAIL: Expected error, got success
```

### GREEN - Minimal Fix
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ... rest of function
}
```

**Verify GREEN**:
```bash
npm test
# PASS: All tests passing
```

### REFACTOR - Clean Up (if needed)
```typescript
// Extract validation
function validateEmail(email: string): string | null {
  if (!email?.trim()) {
    return 'Email required';
  }
  return null;
}

function submitForm(data: FormData) {
  const emailError = validateEmail(data.email);
  if (emailError) {
    return { error: emailError };
  }
  // ... rest of function
}
```

## Completion Checklist

Before marking task complete:

```
TDD Compliance:
- [ ] Every new function has a test
- [ ] Watched each test fail first
- [ ] Wrote minimal code to pass
- [ ] All tests pass
- [ ] No errors or warnings
- [ ] Edge cases covered
```

**Can't check all boxes? Start over with TDD.**

## Final Rule

```
Production code exists → test exists and failed first
Otherwise → not TDD, delete and restart
```

**No exceptions without explicit permission.**

## Edge Case Coverage

Ensure tests cover:

```typescript
// Empty inputs
test('handles empty array', () => {
  expect(sum([])).toBe(0);
});

// Null/undefined
test('handles null input', () => {
  expect(() => sum(null)).toThrow('Input required');
});

// Boundary conditions
test('handles single element', () => {
  expect(sum([5])).toBe(5);
});

test('handles negative numbers', () => {
  expect(sum([-1, -2, -3])).toBe(-6);
});

// Error states
test('handles operation failure', async () => {
  const failing = () => Promise.reject('error');
  await expect(retryOperation(failing)).rejects.toThrow();
});
```

## Remember

**TDD succeeds when**:
- ✅ Tests written first (always)
- ✅ Tests watched failing (proving they work)
- ✅ Minimal code written (no over-engineering)
- ✅ All tests green (no regressions)
- ✅ Code refactored (clean and maintainable)

**TDD fails when**:
- ❌ Code written before test
- ❌ Tests written after
- ❌ Tests pass immediately
- ❌ Over-engineering happens
- ❌ Rationalizations made

**Discipline beats talent. TDD is discipline.**

---

**Purpose:** Prevent false success reports like "✅ All 33 tests passing!" when tests actually failed

**The Problem (Real Example from Brutal Testing):**
- Workflow reported: "All 33 tests passing!"
- Reality: 3 out of 7 tests FAILED
- Root cause: Reports not verified independently

**The Solution: MANDATORY Verification**

You MUST verify independently after ANY test execution:

#### Verification Procedure

**Step 1: Run Actual Test Command**
```bash
# Your project's test command
npm test
# or pytest
# or cargo test
# or go test
# or mvn test
```

**Step 2: Capture REAL Output**

Do not summarize. Copy the actual console output.

**Step 3: Verify Exit Code**
```bash
echo $?  # MUST be 0 for success
```

**Step 4: Visual Confirmation**

LOOK at the output with YOUR EYES. See ✓ symbols, green text, "X passed" messages.

#### Required Checklist

- [ ] All tests run (none skipped or filtered out)
- [ ] All tests pass (see green ✓ symbols)
- [ ] Exit code is 0 (verified with echo $?)
- [ ] No warnings about failures in output
- [ ] Actual output captured (not summarized)

#### Quality Gate

**YOU MUST SEE passing tests with YOUR EYES.**

Do NOT say: "✅ All tests passing!"

DO say: "Verified: npm test shows 33/33 passing (exit code 0). Output:\n[paste actual]"

#### If Tests Fail

**STOP immediately. Do NOT proceed.**

1. Don't move to next increment
2. Don't report partial success
3. Investigate failure root cause
4. Fix implementation or test
5. Re-run until ALL pass
6. Only then report success WITH PROOF

#### Example: Correct Reporting

```markdown
## Test Verification

**Command:** `npm test`

**Output:**
```
PASS tests/auth.test.js
  JWT Authentication
    ✓ should generate valid token (45ms)
    ✓ should reject invalid password (32ms)
    ✓ should handle missing email (28ms)

Tests: 3 passed, 3 total
Snapshots: 0 total
Time: 1.234s
```

**Exit code:** 0 (verified)

**Verification:** ✅ All 3 tests passing independently confirmed

**Proceeding to next increment**
```

#### Example: Failure Handling

```markdown
## Test Verification - FAILED

**Command:** `npm test`

**Output:**
```
FAIL tests/auth.test.js
  JWT Authentication
    ✓ should generate valid token
    ✕ should reject invalid password (expected 401, got 500)
    ✕ should handle missing email (expected 400, got 500)

Tests: 1 passed, 2 failed, 3 total
```

**Exit code:** 1 (FAILURE)

**Action:** STOPPING implementation. Fixing failures now.

**Root cause:** Error handling not implemented for edge cases

**Fix applied:** Added try/catch with proper HTTP status codes

**Retry result:** All 3 tests now passing ✅

**Now proceeding to next increment**
```

#### Anti-Patterns to Avoid

❌ **Don't:** Trust your own success reports without verification
✅ **Do:** Always run tests and see results

❌ **Don't:** Summarize test output ("tests passed")
✅ **Do:** Paste actual output with line counts

❌ **Don't:** Assume exit code without checking
✅ **Do:** Explicitly verify with `echo $?`

❌ **Don't:** Proceed if ANY test fails
✅ **Do:** Stop and fix until 100% pass

#### Why This Stage Exists

The "brutal truth" testing revealed that implementer agents reported false success. This stage exists to FORCE verification and prevent that pattern.

**Every test execution MUST go through this verification checklist.**
