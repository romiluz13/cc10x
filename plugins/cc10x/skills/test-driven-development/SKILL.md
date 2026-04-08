---
name: test-driven-development
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read Grep Glob Bash Write Edit
user-invocable: false
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## Reference Files

Read only the references needed for the current test cycle:

- `references/testing-patterns.md` for naming, AAA structure, near-miss negatives, behavioral focus, and anti-pattern checks
- `references/test-data-and-mocks.md` for factories, mock boundaries, common boundary mocks, and env/time handling
- `references/integration-and-live-proof.md` when unit tests are not enough, or the plan requires real APIs, seeded data, browser flows, or stress proof

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Test Process Discipline (CRITICAL)

**Problem:** Test runners (Vitest, Jest) default to watch mode, leaving processes hanging indefinitely.

**Mandatory Rules:**
1. **Always use run mode** — Never invoke watch mode:
   - Vitest: `npx vitest run` (NOT `npx vitest`)
   - Jest: `CI=true npx jest` or `npx jest --watchAll=false`
   - npm scripts: `CI=true npm test` or `npm test -- --run`
2. **Prefer CI=true prefix** for all test commands: `CI=true npm test`
3. **After TDD cycle complete**, verify no orphaned processes:
   `pgrep -f "vitest|jest" || echo "Clean"`
4. **Kill if found**: `pkill -f "vitest" 2>/dev/null || true`

## Red-Green-Refactor

```
    ┌─────────┐       ┌─────────┐       ┌───────────┐
    │   RED   │──────>│  GREEN  │──────>│ REFACTOR  │
    │ (Fail)  │       │ (Pass)  │       │ (Clean)   │
    └─────────┘       └─────────┘       └───────────┘
         ^                                    │
         │                                    │
         └────────────────────────────────────┘
                    Next Feature
```

### Vertical Slicing (CRITICAL)

```
WRONG (horizontal — all tests then all code):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical — one feature at a time):
  RED->GREEN: test1->impl1
  RED->GREEN: test2->impl2
  RED->GREEN: test3->impl3
```

**DO NOT write all tests first, then all implementation.** This produces bad tests:
- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things rather than user-facing behavior
- Tests become insensitive to real changes — pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach:** One test → one implementation → repeat. Each test responds to what you learned from the previous cycle.

### RED - Write Failing Test

Write one minimal test showing what should happen.

**Good:**
```typescript
test('retries failed operations 3 times', async () => {
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
Clear name, tests real behavior, one thing

**Bad:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Vague name, tests mock not code

**Requirements:**
- One behavior
- Clear name
- Real code (no mocks unless unavoidable)

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
CI=true npm test path/to/test.test.ts
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write simplest code to pass the test.

**Good:**
```typescript
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
Just enough to pass

**Bad:**
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI - You Ain't Gonna Need It
}
```
Over-engineered

Don't add features, refactor other code, or "improve" beyond the test. Don't hard-code test values - implement general logic that works for ALL inputs.

### Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
CI=true npm test path/to/test.test.ts
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next feature.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |

For deeper test structure, near-miss negative tests, behavior-vs-internals, and
smell checks, read `references/testing-patterns.md`.

For factories, mocks, and env/time handling, read
`references/test-data-and-mocks.md`.

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:
- Might test wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and rewrite with TDD (X more hours, high confidence)
- Keep it and add tests after (30 min, low confidence, likely bugs)

The "waste" is keeping code you can't trust. Working code without real tests is technical debt.

## Red Flags - STOP and Start Over

If you catch yourself:

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Example: Bug Fix

**Bug:** Empty email accepted

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**
```bash
$ npm test
PASS
```

**REFACTOR**
Extract validation for multiple fields if needed.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered
- [ ] No hanging test processes (pgrep -f "vitest|jest" returns empty)

Can't check all boxes? You skipped TDD. Start over.

## Integration And Live Proof

When the accepted plan or risk profile goes beyond local behavior, read
`references/integration-and-live-proof.md`.

Unit tests are not enough when the task depends on:
- real API calls
- seeded or resettable data
- browser or worker orchestration
- cross-service side effects
- load or stress behavior

In those cases, keep TDD for the inner loop and escalate verification depth for
the outer proof.

## Coverage Threshold (Project Default)

Target: **80%+ code coverage** across:
- Branches: 80%
- Functions: 80%
- Lines: 80%
- Statements: 80%

**Verify with:** `npm run test:coverage` or equivalent.

**Below threshold?** Add missing tests before claiming completion.

### Test Prioritization

80% coverage means deliberate choices about what to test first. Focus effort on:
- Critical user-facing paths (auth, payments, data integrity)
- Complex logic with multiple branches
- Code that has broken before (regression-prone areas)

Do NOT skip tests because code "looks simple" — simple code breaks too. The 80% target is a floor, not a ceiling.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Design for Testability (When Tests Are Hard)

If tests are hard to write, the interface needs work:

1. **Accept dependencies, don't create them**
   - Testable: `function processOrder(order, paymentGateway) {}`
   - Hard to test: `function processOrder(order) { const gw = new StripeGateway(); }`

2. **Return results, don't produce side effects**
   - Testable: `function calculateDiscount(cart): Discount {}`
   - Hard to test: `function applyDiscount(cart): void { cart.total -= discount; }`

3. **Small surface area** — fewer methods = fewer tests needed, fewer params = simpler setup

### Behavioral Focus

Test how objects collaborate, not what they contain. If a test inspects `.state`, `.length`, or private fields, it is testing structure — and will break when internals change without behavior changing.

| Test target | Correct | Wrong |
|-------------|---------|-------|
| Function output | `expect(calculate(input)).toBe(result)` | `expect(calculator.internalCache).toContain(...)` |
| Component behavior | `expect(screen.getByText('Saved')).toBeTruthy()` | `expect(component.state.saved).toBe(true)` |
| Service interaction | `expect(response.status).toBe(201)` | `expect(service.callCount).toBe(1)` |

This is already implied by the "Testing implementation" smell in the Test Smells table. Make it the default lens: every assertion should answer "what did the user/caller observe?" not "what happened inside?"

### Test Contracts Across Agents

When CC10x routes work across multiple agents (planner writes test specs, builder implements, reviewer verifies), the test file IS the contract:

- **Planner** defines expected behavior as test names and assertions in the plan
- **Builder** writes tests first, implements to green — the test file proves the contract is met
- **Reviewer** re-runs the same tests — pass means contract fulfilled, fail means contract broken

Do not duplicate the contract in prose. If the test file expresses the requirement, the test file is the requirement.

## Output Format

```markdown
## TDD Cycle

### Requirements
[What functionality is being built]

### RED Phase
- Test: [test name]
- Command: `npm test -- --grep "test name"`
- Result: exit 1 (FAIL as expected)
- Failure reason: [function not defined / expected X got Y]

### GREEN Phase
- Implementation: [summary]
- File: [path:line]
- Command: `npm test -- --grep "test name"`
- Result: exit 0 (PASS)

### REFACTOR Phase
- Changes: [what was improved]
- Command: `npm test`
- Result: exit 0 (all tests pass)
```

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.
