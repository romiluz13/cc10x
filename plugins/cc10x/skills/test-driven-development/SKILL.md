---
name: test-driven-development
description: This skill should be used when the user asks to "write tests first", "use TDD", "test-driven", or when building features that require the RED-GREEN-REFACTOR cycle.
---

# Test-Driven Development (TDD)

Build features using the RED → GREEN → REFACTOR cycle.

## The TDD Cycle

### RED: Write Failing Test First

Write a test that captures the requirement. Run it. **It MUST fail.**

```bash
# Run test - should fail (exit 1)
npm test -- --grep "should calculate total"
# Expected: FAIL (exit code 1)
```

If test passes without implementation, the test is wrong.

### GREEN: Minimal Implementation

Write the minimum code to make the test pass. Nothing more.

```bash
# Run test - should pass (exit 0)
npm test -- --grep "should calculate total"
# Expected: PASS (exit code 0)
```

Do NOT add extra features. Only make the test pass.

### REFACTOR: Clean Up

Improve code quality while keeping tests green.

```bash
# Run all tests after each change
npm test
# Expected: PASS (exit code 0)
```

Refactor in small steps. Run tests after each change.

## Process

### 1. Understand Requirements

Before writing tests:

- What functionality is needed?
- What are the inputs?
- What are the expected outputs?
- What are the edge cases?

### 2. Write Test First

```typescript
describe('calculateTotal', () => {
  it('should return sum of item prices', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

### 3. Run Test (Verify RED)

```bash
npm test -- --grep "calculateTotal"
# MUST fail - function doesn't exist yet
```

### 4. Implement Minimal Code

```typescript
function calculateTotal(items: { price: number }[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### 5. Run Test (Verify GREEN)

```bash
npm test -- --grep "calculateTotal"
# MUST pass now
```

### 6. Refactor If Needed

Improve code while tests stay green.

## Evidence Requirements

Every TDD cycle must capture:

- **RED**: Test name + exit code 1 (failure)
- **GREEN**: Test name + exit code 0 (success)
- **REFACTOR**: All tests + exit code 0

## Output Format

```markdown
## TDD Cycle

### Requirements
[What functionality is being built]

### RED Phase
- Test: [test name]
- Command: `npm test -- --grep "test name"`
- Result: exit 1 (FAIL as expected)

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

## Common Mistakes

1. **Writing code before tests** - Tests MUST come first
2. **Test passes immediately** - Test is wrong, fix it
3. **Adding extra features in GREEN** - Only make test pass
4. **Skipping REFACTOR** - Clean up while tests are green
5. **Not capturing exit codes** - Evidence required
