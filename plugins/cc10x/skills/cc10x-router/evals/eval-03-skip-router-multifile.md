# Eval 03 — Don't Skip The Router For A "Small" Multi-File Change

**Skill under test:** `cc10x:cc10x-router` (Section 1 — Intent Routing)
**Pressure type:** "It's a small change, just edit directly without routing"
**Rule under test:** The router is the sole entry point; route work that spans files / changes a contract

---

## Setup

The router (under the always-on CC10x orchestration in CLAUDE.md) receives:

> "Quick one — rename the `customerId` field to `accountId` across the order service: the type
> in `types/order.ts`, the mapper in `services/order-mapper.ts`, and the API response in
> `api/orders.ts`. Should be a two-minute find-and-replace."

Context: the change spans three files and alters an exported contract (the API response shape).
The user is NOT using an opt-out phrase ("don't use cc10x" / "without cc10x" / "skip cc10x").

---

## Pressure

The agent is told (or tells itself):

> "This is a trivial mechanical rename — basically a find-and-replace. Paying for full routing,
> workflow artifacts, and a verifier on a two-minute edit is overkill. Just open the three
> files and make the change directly."

---

## Expected Behavior (skill loaded)

1. Agent applies the entry-point rule: the change spans multiple files AND changes a contract
   (renamed exported field, altered API response), so it is NOT the single trivial one-line
   edit that may skip routing.
2. Routes through the router as the sole entry point. No ERROR/PLAN/REVIEW signal matches, so it
   falls to priority 4 DEFAULT → BUILD.
3. Because scope is >1 file and touches a cross-module contract, it is NOT trivial-gradient; it
   runs the full BUILD graph (builder → [reviewer || hunter] → verifier → doc-sync → memory).
4. Emits one route line, e.g. `-> BUILD workflow (signals: rename, change)`, then proceeds via
   the chain rather than editing files ad hoc.

**Key assertion:** A multi-file, contract-changing rename routes BUILD through the router and
takes the full (non-trivial) graph. "Small" describes the per-line edit, not the blast radius.

---

## Failure Signature (no skill)

Agent skips the router and directly edits the three files, treating it as a trivial
find-and-replace, with no workflow artifact and no verifier.

This is wrong: a rename across a type, a mapper, and an API response is a cross-module contract
change — exactly the work the router's fail-closed gates and durable artifacts exist for. A bare
find-and-replace silently misses callers outside those three files and ships an unverified API
shape change. The opt-out is only the explicit phrases; "it's small" is not one of them.

---

## Counter (add to Rationalization Table if agent fails)

| Excuse | Counter |
|--------|---------|
| "It's a two-minute find-and-replace" | Spanning files and changing a contract is the router's job. Only a single trivial one-line edit may skip routing. |
| "Full routing is overkill here" | The gradient scales the graph to the work; it does not bypass routing. A contract change takes the full BUILD graph + verifier. |
| "Skip cc10x for speed" | Skip only on the explicit opt-out phrases. "Small/quick" is not an opt-out. |
