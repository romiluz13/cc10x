---
name: codebase-deepening
description: "Use when an existing codebase has accreted shallow modules — thin wrappers, pass-through layers, near-duplicate helpers — and you want to find and deepen them rather than design greenfield."
allowed-tools: Read Grep Glob Bash
user-invocable: false
---

# Codebase Deepening

## Overview

`architecture-patterns` designs systems from scratch — it maps flows, then draws components. This skill is its retrofit counterpart: the code already exists, it works, and the problem is **shape**, not features. LLM-grown codebases (functions written one prompt at a time, reuse skipped) accrete **shallow modules** — thin wrappers, layers that only forward a call, near-duplicate helpers. Each one looks harmless; together they spread complexity across every caller.

**Core principle:** A deep module hides a lot of behavior behind a small interface. A shallow module's interface is almost as complex as its implementation — it makes callers learn a thing without doing much for them. Deepening means **concentrating** complexity behind one interface so N callers stop paying for it.

This skill is **advisory and read-heavy.** It diagnoses and proposes; it does not refactor. Any actual change goes through the normal BUILD workflow with full gates (see the last section). It pairs with ORIENT — understand the surface first — and feeds the planner once the user picks a candidate.

## The Iron Law

```
NO DEEPER INTERFACE PROPOSED BEFORE THE DELETION TEST IS RUN ON EACH CANDIDATE
```

Shape opinions before evidence are how you "improve" code into a different mess. Find the shallow modules, prove they're shallow, present them — then design.

## The Deletion Test (the shallowness probe)

For each candidate module, ask one question:

> **If I deleted this module, would the complexity it holds CONCENTRATE somewhere, or just MOVE elsewhere?**

- **Complexity vanishes / stays put** → the module was earning its keep. A real abstraction: deleting it forces the same logic to reappear across every caller. **Leave it alone.**
- **Complexity just moves** → the module is a pass-through. Deleting it relocates the work without adding cost, because the module never hid anything — it forwarded. **Deepening candidate.**

A deep module fails the deletion test *productively*: you can't delete it without the complexity erupting across N call sites. A shallow module fails it trivially: deletion is a paste.

| Smell | What you'll see | Usually |
|-------|-----------------|---------|
| Thin wrapper | `doX(a){ return lib.doX(a) }` — renames, adds nothing | Shallow |
| Pass-through layer | A "service" whose every method calls one repo method 1:1 | Shallow |
| Near-duplicate helper | Same intent, different name, different file | Shallow (consolidate first) |
| Config/leverage module | Small interface, branching/validation/retry/state inside | Deep — keep |

## Diagnosis Flow

Run a **read-only** pass — no edits, no agents that write. Use Grep/Glob directly, or hand the sweep to the `Explore` agent or `cc10x:researcher` for breadth across naming conventions.

1. **Enumerate the surface.** Glob the source tree, Grep for exported definitions (`export function`, `export const … =>`, `def `, `class …`). Capture `name | file:line | signature`.
2. **Flag shallow shapes.** Pull the candidates the table above describes — functions/classes that forward, layers that map 1:1, modules whose interface ≈ implementation.
3. **Cross-reference near-duplicates.** Hand the duplicate question to `finding-duplicate-functions` — its semantic-duplication audit already finds "same intent, different name." Consolidate duplicates *before* deepening: two shallow copies merge into one, and only then is it worth asking whether that one should be deeper.
4. **Run the deletion test on each survivor.** Keep only the modules where deletion would merely move complexity. Discard the rest — a working deep module is not a deepening candidate.

Output of this phase is a **candidate list**, not a refactor.

## Present Candidates BEFORE Proposing Interfaces

Make the architectural recommendation **after** understanding, never before. Present the candidates and let the user pick which one (if any) is worth deepening — then design the deeper interface for the chosen one.

Badge each candidate by confidence:

- **Strong** — clearly shallow, deletion test is unambiguous, callers visibly repeat work the module should hide.
- **Worth-exploring** — looks shallow but the deepening has a real cost or risk; needs the user's domain judgment.
- **Speculative** — a hunch; flagged for completeness, low confidence, easy to reject.

For each candidate give a **before/after sketch** — current shallow interface vs. the proposed deeper one — so the user is choosing between concrete shapes, not adjectives:

```markdown
### [Strong] `formatApiError` + 3 call-site error shaping  →  deepen into one error boundary
Before: each route hand-builds `{ error, code, status }`; `formatApiError` only stringifies the message.
        4 call sites each repeat envelope + status mapping (src/api/{users,posts,orders,auth}.ts).
After:  one `toErrorResponse(err): ApiError` owns envelope + status + message. Routes call it and return.
        Deletion test: deleting it scatters the envelope/status mapping back across all 4 routes → it concentrates real complexity → worth deepening.
Seam:   the route→response boundary. Two adapters: production routes + the error-response unit test (see below).
```

Then stop and ask which to pursue. Do not design interfaces for candidates the user hasn't chosen.

## Place the Seam with the Two-Adapters Rule

`planning-patterns` states the rule; this is where it gets **used on existing code.** When you design the chosen module's deeper interface, you must decide **where its seam sits** — the location at which the interface lives and the test attaches.

> **A seam is only real when two concrete adapters use it — and the test double counts as the second.**

Apply it to the deepened module:

- The **first adapter** is the production caller(s) that will use the new deep interface.
- The **second adapter** is the test that exercises the same interface (the highest stable seam that still covers the behavior — the deep module's public interface, not its private internals).
- If only production code would ever cross the proposed seam and you can't name a second adapter that attaches there, **the seam is a guess.** Put the interface where a test can actually reach it, or don't introduce the seam — deepen behind an existing boundary instead.

This keeps the deepened module testable through its own interface and stops "deepening" from inventing private layers nothing can verify. The test file is the contract for the deeper shape.

## Red Flags — STOP

- Proposing a deeper interface before running the deletion test → go back, prove shallowness first.
- Deepening a module that passes the deletion test → it's already deep; you're adding, not concentrating.
- Designing interfaces for candidates the user didn't pick → present, then wait.
- A proposed seam with only one adapter → it's hypothetical; relocate or drop it.
- Layering a new wrapper *over* a shallow module to "deepen" it → that adds a shallow module. Deepen by absorbing the forwarding, not stacking on it.
- Letting this skill apply the change → it proposes only; refactors route through BUILD.

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This wrapper adds clarity" | Run the deletion test. If deletion just inlines it, it adds a name, not depth. |
| "More layers = cleaner architecture" | Depth is small interface + lots hidden, not more boxes. Layers that forward are shallow. |
| "I'll deepen all the candidates" | Present them; the user picks. Most shallow modules aren't worth the churn. |
| "The seam is obvious" | Name the two adapters. If you can't, the seam is a guess. |
| "While deepening I'll refactor X too" | Out of scope. Defer it; this skill proposes one deepening at a time. |

## Handoff to BUILD (gates stay on)

This skill ends at a chosen candidate + a deeper-interface proposal + a named seam. It does **not** edit code. The refactor is a behavior-preserving change and gets cc10x's full bar:

- It goes through the **planner** (the candidate + before/after + seam become the plan input), then the BUILD workflow — builder → [reviewer || code-reviewer] → verifier → doc-sync → memory.
- The deepening is verified against reality: the survivor interface has tests at its seam, every caller is repointed, the suite and typecheck pass after the merge. A deepening that isn't re-verified is not done.
- Do not let this skill become an ungated rewrite path. Proposing is read-only; changing is gated.
