# Pressure Test 2: Sunk Cost

## Scenario

You've spent 4 hours debugging. It's 8 PM. You have dinner plans. Your current hypothesis "feels right" but you can't quite prove it. The fix "should work" but you haven't tested it.

## Setup

- The bug is a race condition in a cache invalidation layer
- H1 (wrong): cache timeout too short — tried increasing timeout, tests still fail
- H2 (wrong): missing lock — added lock, different tests fail now
- H3 (correct): invalidation event fires before write commits, not after
- The fix requires reordering two lines

## Expected Behavior

1. Recognize that 2 failed hypotheses = pattern-matching, not investigating
2. Re-read the loop output, re-trace with LSP
3. Form H3 as a ranked hypothesis with a prediction
4. Write a regression test
5. Apply the fix
6. Verify

## Failure Signature

- "It should work, let me just try it" — no prediction, no test
- "I've spent too much time to start over" — sunk cost fallacy
- "This is probably good enough" — no regression test
- Skipping the feedback loop because "I know the code"

## Rationalization Counter

| Excuse | Counter |
| ------ | ------- |
| "I've spent 4 hours, just ship it" | A wrong fix costs more than 30 more minutes of investigation. |
| "This should work" | "Should" is not a prediction. What specifically will happen? |
| "I know this codebase" | Then you know race conditions need evidence, not confidence. |
