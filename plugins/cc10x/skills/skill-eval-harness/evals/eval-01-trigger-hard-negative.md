# Eval 01 — Trigger Eval Must Include A Hard Negative

**Skill under test:** `cc10x:skill-eval-harness` (§1 — Trigger Evals)
**Pressure type:** "Every realistic query should route; ship the positive cases and move on"
**Rule under test:** Trigger evals MUST include hard negatives; a false-positive is a FAIL

---

## Setup

The agent is asked to write a trigger-eval set proving a routing change to `cc10x-router`
fires correctly. It receives:

> "I tightened the ERROR keyword list. Write `trigger-evals.json` for the router and confirm
> it still triggers correctly on the new keywords."

Context: the author cares about the keywords they just added ("crash", "throwing"). The change
also touches the boundary where routing should NOT fire — a query that names an exact file and
line, which is a direct edit, not orchestration.

---

## Pressure

The agent is told (or tells itself):

> "The author wants to confirm the new ERROR keywords trigger. I'll list a handful of crash/bug
> queries with `should_trigger: true` and `expected_route: DEBUG`. They all pass. Done — the
> change is proven. Negative cases are extra work the author didn't ask for."

---

## Expected Behavior (skill loaded)

1. Agent applies §1: a trigger set with only positive cases **cannot catch a false-positive**, so
   it proves nothing about over-firing.
2. Adds at least one entry from each mandatory hard-negative class, including a named-file-path
   direct edit:
   `{ "query": "change customerId to id in types/order.ts line 12", "should_trigger": false, "expected_route": "direct-edit" }`,
   plus an orient query (`should_trigger: false`, route `ORIENT`) and an explicit opt-out
   (`should_trigger: false`, route `opt-out`).
3. Runs every entry, reports **false-positive and false-negative counts separately**, and treats
   the named-file-path query triggering DEBUG as a FAIL — not a near-miss.
4. Status SHIP only if every entry's observed behavior matches both `should_trigger` and
   `expected_route`.

**Key assertion:** A trigger-eval set without hard negatives is incomplete by definition. The
named-file-path / orient / opt-out cases that must STAY SILENT are what prove the trigger is not
over-firing — and a single false-positive is a FAIL, not a warning.

---

## Failure Signature (no skill)

Agent writes only positive crash/bug cases, observes them all trigger DEBUG, and reports
"trigger verified — ships". No negative case is tested.

This is wrong: the set cannot detect that the tightened keyword list now also fires on
"change `customerId` in `types/order.ts` line 12" (a direct edit) or on "explain the retry
logic" (an orient). An over-firing trigger that hijacks direct edits and orient questions into a
full BUILD workflow ships unnoticed, because the eval never asked the question that would catch it.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "The author only asked about the new keywords" | A trigger change has two failure modes — under-fire and over-fire. Positive-only evals test one. Hard negatives are mandatory, not optional. |
| "All my positive cases pass, so it's proven" | Proven against false-negatives only. A false-positive (a negative case that triggers) is also a FAIL and needs its own entries. |
| "Negative cases are extra work" | The named-file-path, orient, and opt-out cases are the cheapest way to catch the most expensive failure: orchestration hijacking a direct edit. |
