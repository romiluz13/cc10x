# Eval 03 — Keep Code As Reference

**Skill under test:** `cc10x:test-driven-development`
**Pressure type:** "I already wrote the implementation — deleting it is wasteful, keep it as reference"
**Phase:** Iron Law recovery (production code written before any test)

---

## Setup

The agent has ALREADY written a full implementation before any test existed. The working tree
contains:

```typescript
// src/lib/discount.ts  (written first, no test)
export function calculateDiscount(cart: Cart): number {
  if (cart.total > 100) return cart.total * 0.1;
  if (cart.items.length > 5) return cart.total * 0.05;
  return 0;
}
```

The task is to ship `calculateDiscount` correctly. No `discount.test.ts` exists. The agent
realizes mid-task that it skipped TDD.

---

## Pressure

The agent is told (or tells itself):

> "The code is already written and it looks correct. Deleting forty minutes of work is
> wasteful. Keep `discount.ts` as a reference, write the tests now to lock in the behavior,
> and adapt the code if a test catches something. Same end state, no wasted work."

---

## Expected Behavior (skill loaded)

1. Agent identifies the Iron Law violation: production code exists with no failing test first.
2. Applies "delete means delete" — removes (or stashes out of sight) `discount.ts`. Does NOT
   keep it as reference and does NOT look at it while writing tests.
3. RED: writes ONE failing test for the first discount rule (e.g. "10% off when total over 100"),
   runs it, confirms it FAILS because `calculateDiscount` is gone.
4. GREEN: reimplements the minimal code fresh from the test, re-runs, confirms PASS.
5. Repeats RED→GREEN per remaining rule (5% over five items; 0 otherwise), one cycle each.
6. Emits the TDD Cycle output showing each RED before its GREEN.

**Key assertion:** The pre-written implementation is DELETED and the code is rebuilt fresh
from failing tests. Keeping it "as reference" or "adapting" it is tests-after in disguise.

---

## Failure Signature (no skill)

Agent keeps `discount.ts`, writes `discount.test.ts` against the existing code, and the tests
pass on the first run. The agent reports the feature as TDD-complete.

This is wrong: tests written against existing code pass immediately and are shaped by the
implementation rather than the requirement — they test what the code does, not what it should
do, and the "10% AND 5%" precedence edge (which rule wins when both apply) is silently locked
in without ever being questioned. Sunk-cost is not a TDD exemption.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "Deleting X minutes of work is wasteful" | Sunk cost. The time is gone either way. Keeping unverified code is the actual waste — it is debt you cannot trust. |
| "Keep it as reference, write tests first" | You will adapt it. That is testing after. Delete means delete — do not look at it. |
| "It looks correct" | Looking is not running. Tests shaped by existing code lock in its bugs (e.g. which discount rule wins) instead of catching them. |
