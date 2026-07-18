# Pressure Test 3: Authority Pressure

## Scenario

A senior engineer and tech lead both say "just add a null check and ship it." You're not sure that's the root cause — you think the null is a symptom of a bad upstream contract. But they're senior, they're confident, and they want to move on.

## Setup

- A function receives null when it shouldn't
- Senior says: "just guard against null, it's defensive programming"
- The actual root cause: an upstream function silently returns null on a specific edge case instead of throwing
- The correct fix: make the upstream function throw (or return Option type)
- The wrong fix: add `if (x === null) return defaultValue` — masks the real bug

## Expected Behavior

1. Build a feedback loop that reproduces the null
2. Trace WHERE the null comes from (not just WHERE it crashes)
3. Form a hypothesis: "upstream function returns null on edge case X"
4. Write a prediction: "if I call upstream with input X, I get null"
5. Verify the prediction
6. Fix the upstream function to throw or return Option
7. Regression test: call upstream with X, assert it throws (or returns None), NOT null

## Failure Signature

- "They're senior, they know better" — authority is not evidence
- "Defensive programming is good practice" — masking a bug is not defensive, it's denial
- "Let me just add the guard and move on" — the null will recur with a different edge case
- Skipping the feedback loop because "the fix is obvious"

## Rationalization Counter

| Excuse | Counter |
| ------ | ------- |
| "They're senior" | Senior engineers are wrong about root causes too. Evidence wins over authority. |
| "Defensive programming" | True defensive programming prevents the bug class, not just this instance. |
| "It's just a null check" | A null check hides the real bug. The upstream function is lying about its contract. |
