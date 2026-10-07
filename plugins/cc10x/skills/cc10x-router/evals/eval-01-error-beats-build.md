# Eval 01 — The Primary Deliverable Decides (ERROR vs BUILD)

**Skill under test:** `cc10x:cc10x-router` (Section 1 — Intent Routing)
**Pressure type:** "It's phrased as an addition, so it's a BUILD"
**Rule under test:** a keyword hit only nominates a row; the primary deliverable decides. Repairing broken behavior IS the deliverable here, so ERROR wins over BUILD.

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

1. Router scans the table for keyword hits. They only NOMINATE rows: priority 1 ERROR matches
   on "crash" and "throwing". "Add" is not a keyword of any row; BUILD is the priority-8
   DEFAULT row, which only takes what no other row claims.
2. Asks what the primary deliverable is. The work exists because checkout already crashes, so
   repairing that behavior is the deliverable and the added guard is the means. (Contrast:
   "add a dark-mode toggle and fix the button alignment" delivers new functionality with a
   small fix inside it, so that one is BUILD.)
3. Selects the DEBUG workflow with chain
   `bug-investigator -> code-reviewer -> integration-verifier`.
4. Emits exactly one route line, e.g.
   `-> DEBUG workflow (signals: crash, throwing)`.

**Key assertion:** A request whose deliverable is repairing an existing crash routes DEBUG,
not BUILD, whatever verb it opens with. The lower Priority number only breaks a genuine tie;
here ERROR (priority 1) also wins the deliverable test, and BUILD is the priority-8 default.

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
| "It says 'Add', so it's a BUILD" | The primary deliverable decides, not the opening verb. A crash that motivates the change makes the repair the deliverable, so DEBUG (priority 1) over BUILD (the priority-8 default). |
| "The crash is just context" | The crash IS the work — diagnose root cause before patching. A BUILD path skips bug-investigator. |
