# Eval 01 — ERROR Beats BUILD

**Skill under test:** `cc10x:cc10x-router` (Section 1 — Intent Routing)
**Pressure type:** "It's phrased as an addition, so it's a BUILD"
**Rule under test:** ERROR always wins over BUILD

---

## Setup

The router receives this request:

> "Users keep hitting a crash on the checkout page when the cart is empty. Add a guard so it
> stops throwing and shows an empty-cart message instead."

Context: the phrasing leads with "Add a guard" (a BUILD-shaped verb), but the motivating
condition is an existing crash ("keep hitting a crash", "stops throwing").

---

## Pressure

The agent is told (or tells itself):

> "The user said 'Add a guard … shows a message' — that is building a new behavior, a clear
> feature addition. Route it BUILD and send it to the component-builder. The crash is just the
> reason; the work itself is additive."

---

## Expected Behavior (skill loaded)

1. Router scans for the first matching signal in priority order. Priority 1 ERROR keywords
   match: "crash", "throwing", "stops throwing" (and the implied "fix").
2. Applies the rule **ERROR always wins over BUILD** — the presence of "Add" does not demote it.
3. Selects the DEBUG workflow with chain
   `bug-investigator -> code-reviewer -> integration-verifier`.
4. Emits exactly one route line, e.g.
   `-> DEBUG workflow (signals: crash, throwing)`.

**Key assertion:** A request that combines a fix-motivation with additive phrasing routes
DEBUG, not BUILD. ERROR signals take priority 1 over the priority-4 default.

---

## Failure Signature (no skill)

Agent routes BUILD (or skips routing and just starts editing) because the sentence opens with
"Add a guard", sending it down the component-builder chain.

This is wrong: the work originates from an existing crash, so the bug-investigator must
diagnose the root cause first; jumping to BUILD risks patching a symptom (one empty-cart guard)
while the underlying null-handling defect persists elsewhere. The router rule is explicit:
ERROR always wins over BUILD.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "It says 'Add', so it's a BUILD" | ERROR keywords are priority 1 and win over BUILD's priority 4. A crash that motivates the change routes DEBUG regardless of additive verbs. |
| "The crash is just context" | The crash IS the work — diagnose root cause before patching. A BUILD path skips bug-investigator. |
