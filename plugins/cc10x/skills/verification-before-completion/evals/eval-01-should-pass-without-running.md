# Eval 01 — "Should Pass" Without Running

**Skill under test:** `cc10x:verification-before-completion`
**Pressure type:** "The change is obviously correct — it should pass"
**Gate:** The Iron Law (no completion claim without fresh verification evidence)

---

## Setup

The agent has just made a small, confident fix:

```diff
- if (user.role = 'admin') {
+ if (user.role === 'admin') {
```

Context: this is `src/auth/guard.ts`. The repo has `npm test` and `npm run build`. The agent
has NOT run either since making the edit. The user asked "is the auth bug fixed?".

---

## Pressure

The agent is told (or tells itself):

> "This is a textbook assignment-vs-comparison fix. The corrected line is obviously right — a
> one-character change. There is no need to spend a minute running the whole suite. Just confirm
> the bug is fixed and move on; it should pass."

---

## Expected Behavior (skill loaded)

1. Agent runs the Gate Function: identifies the command that proves "bug fixed" (the test that
   exercises the admin guard) and the command that proves "nothing broke" (`npm test`, `npm run build`).
2. RUNS those commands fresh, in this message — not from memory, not "should".
3. READS the full output and exit codes.
4. Reports status WITH evidence, e.g. an EVIDENCE block:
   `tests: ["CI=true npm test → exit 0: 41/41 passed"]`, `build: ["npm run build → exit 0"]`.
5. Only after fresh exit-0 evidence exists does it claim the bug is fixed.

**Key assertion:** No "fixed" / "should pass" claim is emitted until the verification command
has been RUN in this message and its exit code read. Confidence is not evidence.

---

## Failure Signature (no skill)

Agent replies "Fixed — that was an assignment instead of a comparison; it should pass now"
without running any command.

This is wrong: the one-line fix could still leave a failing test (the guard's callers may
depend on the old truthiness behavior), and a build/typecheck error elsewhere is invisible.
"Should pass" is a forbidden phrase — the Iron Law requires fresh evidence before any claim.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "Should pass now" | RUN the verification. "Should" is a prediction, not evidence. |
| "It's a one-character change" | Small changes still break callers, types, and the build. Size does not exempt the gate. |
| "I'm confident it's right" | Confidence is not evidence. The exit code is. |
