# Testing Patterns

## Table of Contents
- [Arrange-Act-Assert](#arrange-act-assert)
- [Test Naming](#test-naming)
- [Near-Miss Negative Tests](#near-miss-negative-tests)
- [Behavior Over Internals](#behavior-over-internals)
- [Test Smells](#test-smells)
- [Pre-Run Sanity Check](#pre-run-sanity-check)

## Arrange-Act-Assert

Keep tests readable:

```typescript
it('rejects an empty email', async () => {
  // Arrange
  const input = { email: '' };

  // Act
  const result = await submitForm(input);

  // Assert
  expect(result.error).toBe('Email required');
});
```

If the test mixes many concerns, split it.

## Test Naming

Prefer names that describe user-observable behavior:
- `creates a task with pending status`
- `returns 401 without authentication`
- `shows validation error for empty title`

Avoid:
- `works`
- `test1`
- names that describe implementation details instead of behavior

## Near-Miss Negative Tests

Add rejection tests for values that are almost valid:
- boundary minus one
- wrong type with plausible shape
- missing required field
- expired or stale state

These catch the bugs happy-path tests miss.

## Behavior Over Internals

Ask: "What does the caller or user observe?"

Prefer:
- return values
- rendered output
- API status and payload
- visible side effects

Avoid asserting on:
- private fields
- internal state containers
- implementation-only helper details

## Test Smells

Common smells:
- giant setup blocks
- dependent tests
- mock-heavy tests that do not execute real logic
- assertions on implementation internals
- no assertions at all
- names that lie about behavior

If a test is hard to understand, it is not helping TDD.

## Pre-Run Sanity Check

Before running the suite:
- no test depends on execution order
- no test uses arbitrary sleeps where condition-based waits belong
- no test mocks the module it is supposed to verify
- assertions target behavior, not structure

If any check fails, fix the test before trusting the result.
