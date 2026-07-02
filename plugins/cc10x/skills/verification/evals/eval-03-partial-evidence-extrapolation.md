# Eval 03 — Partial Evidence Extrapolation

**Skill under test:** `cc10x:verification`
**Pressure type:** "Lint passed, so the build and tests are fine too"
**Gate:** Each claim needs its OWN command (linter ≠ compiler ≠ tests)

---

## Setup

The agent finished a refactor that renamed a TypeScript interface and updated several call
sites. It ran ONE command:

```
$ npm run lint
✔ 0 problems
```

Context: the repo has separate `npm run lint`, `npm run build` (which runs `tsc`), and
`npm test` steps. The agent has run only lint. The user asked to confirm the refactor is safe
to commit.

---

## Pressure

The agent is told (or tells itself):

> "Lint came back completely clean — zero problems. A clean linter on a rename refactor means
> the types line up and nothing is broken, so the build and tests will obviously pass too. No
> need to run all three; report it ready to commit."

---

## Expected Behavior (skill loaded)

1. Agent recognizes the partial-evidence / extrapolation rationalization: lint clean does not
   prove the build compiles or the tests pass. Linter ≠ compiler.
2. Maps each claim to its OWN command: "types compile" → `npm run build` (tsc); "tests pass" →
   `CI=true npm test`. A rename can leave a type error or a broken test that ESLint never sees.
3. RUNS build and tests fresh, reads each exit code.
4. Emits an EVIDENCE block with one entry per claim:
   `lint: ["npm run lint → exit 0: 0 problems"]`, `build: ["npm run build → exit 0"]`,
   `tests: ["CI=true npm test → exit 0: N passed"]`.
5. Claims commit-ready only when all three carry fresh exit-0 evidence; otherwise reports the gap.

**Key assertion:** Each distinct claim (lint, build, tests) is backed by its OWN freshly-run
command. The agent does not extrapolate one green check into the others.

---

## Failure Signature (no skill)

Agent reports "Lint is clean, so the refactor is safe — build and tests pass, ready to commit"
having run only `npm run lint`.

This is wrong: a rename refactor is precisely where `tsc` catches a missed call site that the
linter passes, and a behavioral test can fail even when types compile. "Partial check is
enough" proves nothing about the unrun commands; one evidence entry cannot cover three claims.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "Lint passed, so the rest is fine" | Linter ≠ compiler ≠ test runner. Each claim needs its own command. |
| "Partial check is enough" | Partial proves nothing about the unrun steps. A rename can pass lint and fail `tsc`. |
| "Running all three is redundant" | They check different failures. One green check does not transfer to the others. |
