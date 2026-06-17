---
name: test-driven-development
description: "Internal cc10x skill, loaded by the router for the builder and bug-investigator. Use when writing production code or fixing a bug where a failing test must precede implementation (RED → GREEN → REFACTOR)."
allowed-tools: Read Grep Glob Bash Write Edit
user-invocable: false
---

# Test-Driven Development (TDD)

> **DIVERGENCE FROM superpowers:test-driven-development:** Forked. The RED-GREEN-REFACTOR Iron Law, the worked retry/bug-fix examples, and the rationalization table are core TDD discipline assumed here. CC10x ADDS: watch-mode process hygiene, vertical-slicing enforcement, an 80% coverage floor, Integration And Live Proof, cross-agent Test Contracts (planner spec → builder green → reviewer re-run), condition-based-waiting as a test-authoring discipline, and a per-gate dated scar-note convention. Read references/ for the cc10x deepening.

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

**Exceptions (ask the user):**
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

> **Scar-note (why this gate exists):** Every test that proves you cannot ship implementation written before its failing test will eventually feel redundant to a reader who has only ever seen it pass. It is not. It is the absence of the failure it prevents — code that was never validated because it was authored before any test could disprove it.

### Per-Gate Scar-Note Convention

Each Iron Law and gate carries a short dated note recording the failure it covers, so a future simplification pass cannot delete a rule without first seeing the cost of removing it. The rule's existence is not self-justifying once it has been green for a long time; the scar note is the memory of why it was added.

Format — one line, attached at the gate:

```
<!-- scar: YYYY-MM-DD — <the failure this gate prevents, stated concretely>. Remove only if that failure is now impossible. -->
```

Convention:
- Add a scar note when introducing a new Iron Law or gate. Date it.
- State the *failure*, not the rule (the rule is already visible above the note).
- A simplification pass that wants to drop a gate must address the scar note's failure first. No scar note → treat as undocumented and investigate before removing.

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

### RED → GREEN → REFACTOR (worked examples)

The worked RED/GREEN/REFACTOR code examples (the retryOperation retry test, the email-validation bug-fix walkthrough), the Good-Tests quality table, the "Why Order Matters" rationale, the Red-Flags STOP list, and the excuse/reality Rationalization table are core TDD discipline — assumed, not repeated here (see superpowers:test-driven-development). Apply the loop: write ONE minimal failing test, run it and watch it fail for the right reason, write the minimal code to pass, re-run to confirm, refactor on green, repeat. The cc10x deltas below (coverage floor, Integration And Live Proof, Test Contracts Across Agents) are what this skill adds.

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

### Condition-Based Waiting (Test-Authoring Discipline)

When a test must wait for an async result, poll the actual condition — never sleep a guessed duration. A `setTimeout`/`sleep(N)` that "usually passes" is a false GREEN: it proves the clock advanced, not that the behavior happened.

**Rule:** wait on the condition you care about, with a bounded poll.
- Poll the real assertion (`waitFor` / retry-until-true) on a short interval (~10ms) under a timeout cap.
- The timeout is a failure ceiling, not the expected duration — a passing test returns the instant the condition holds.
- **Principle:** wait for the condition you care about, not a guess about how long it takes. A 2s deterministic loop beats a 30s flaky one.

**Legitimate timed-wait exception:** when timing itself is the contract (debounce, TTL, rate-limit window), first wait for the *triggering* condition, THEN do a justified timed wait against the known, documented interval — never against a hopeful guess.

```
WRONG:  trigger(); await sleep(2000); expect(result).toBe(...)   // guessed; flaky or slow
RIGHT:  trigger(); await waitFor(() => result === ..., { timeout: 2000, interval: 10 })
EXCEPT: await waitFor(() => debounceArmed);  // trigger condition first
        await sleep(DEBOUNCE_MS + ε); expect(firedOnce).toBe(true)  // justified by known timing
```

> **Scar-note (why this gate exists):** A sleep long enough to pass on a fast machine is a coin-flip on a slow CI box and dead weight on every run in between. The flake it eventually produces reads as "the code is broken" when the only thing broken was the guess.

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
| Don't know how to test | Write wished-for API. Write assertion first. Ask the user. |
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

No exceptions without the user's permission.
