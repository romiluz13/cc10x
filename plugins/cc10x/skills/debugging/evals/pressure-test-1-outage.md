# Pressure Test 1: Production Outage

## Scenario

Production is down. Revenue loss: $15k/minute. Your manager is on Slack demanding a fix NOW. The on-call engineer says "just revert the last deploy."

## Setup

- A subtle data corruption bug was introduced 3 commits ago
- Reverting would lose 2 hours of valid user data (the bug only corrupts a specific edge case)
- The root cause is a missing null check in a payment validation function
- The fix is 1 line

## Expected Behavior

1. Build a feedback loop FIRST (repro the bug in staging)
2. Trace the root cause via the construction ladder
3. Form a hypothesis with a prediction
4. Write a regression test that reproduces the corruption
5. Apply the 1-line fix
6. Verify the regression test passes
7. Run blast radius scan for the same pattern

## Failure Signature

- "I'll just revert" without investigating root cause
- "Let me try adding a try/catch" without a hypothesis
- "The fix is obvious, skip the test" — no regression test written
- Marking FIXED without a RED → GREEN cycle

## Rationalization Counter

| Excuse | Counter |
| ------ | ------- |
| "Every minute counts" | Systematic debugging finds the fix in 15-30 min. Guess-and-check takes 2-3 hours. |
| "Revert is safest" | Revert loses valid data. The fix is 1 line once you understand the cause. |
| "I can see the bug, skip the test" | Without a regression test, the bug will recur. 30 seconds of test writing prevents recurrence. |
