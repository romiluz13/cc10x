---
name: prototyping
description: "Use when you need to answer ONE design question or de-risk an unknown before committing to a real build — a throwaway spike that is deleted or absorbed, never shipped."
allowed-tools: Read Grep Glob Bash Write Edit
user-invocable: false
---

# Prototyping (Throwaway Spikes)

> **DIVERGENCE FROM matt-pocock:prototype:** Adapted, not forked. The two-branch shape (logic spike behind a throwaway harness; UI variants behind a `?variant=` switcher) and the throwaway-from-day-one discipline are shared. CC10x ADDS: the explicit single-question contract, a router-owned answer-capture handoff (no direct memory writes), the mandatory delete-or-absorb close-out mapped onto the BUILD-DONE finishing menu, and — most importantly — a HARD WALL forbidding prototype rules from leaking into the BUILD workflow.

## Overview

A prototype is **throwaway code that answers exactly ONE design question**. It exists to de-risk an unknown CHEAPLY before the team pays for the full BUILD chain (TDD, review, hunter, verifier). The question decides the shape; the answer is the only thing kept.

**Core principle:** State the question first. The prototype that answers the wrong question is pure waste.

cc10x can already PLAN and BUILD. What it cannot otherwise do is throw a cheap spike at an unknown and then throw the spike away. This skill is that mode — and the close-out is what makes it cc10x-shaped rather than a license to ship unverified code.

## The Iron Law (read before writing any prototype)

```
A PROTOTYPE'S RULES NEVER LEAK INTO A BUILD.
"No tests, no abstractions, move fast" lives and dies inside the spike.
```

<!-- scar: 2026-06-17 — a spike's "move fast, no tests" code promoted to production by inertia, skipping TDD/verifier gates because it "already worked in the prototype." The prototype proving a question is NOT the same as the answer being shipped. Remove only if prototype code can no longer reach a release path. -->

The prototype runs OUTSIDE the gated chain on purpose. That exemption is the whole point — and it is also the whole danger. If the answer is "build it for real," that is a **fresh BUILD through the router** with the full TDD / reviewer / hunter / verifier gates. The spike's code does not become production by surviving. See **Hard Wall** below — it sits high in this file deliberately, by the keep-gates-high principle.

## Hard Wall: skill_precedence

**This is a router-owned precedence note. Read it as law, not advice.**

```text
skill_precedence:
  - The prototyping relaxations (no failing test first, no abstraction, no
    error handling, no coverage floor, persistence skipped) apply ONLY to the
    throwaway spike. They have ZERO authority over any BUILD workflow.
  - test-driven-development's Iron Law (NO PRODUCTION CODE WITHOUT A FAILING
    TEST FIRST) is NOT waived by a prior prototype. If prototype code is
    absorbed, it is re-implemented fresh from tests — deleted, then rebuilt
    RED → GREEN → REFACTOR. "It already worked in the spike" is rationalization.
  - integration-verifier, code-reviewer, and silent-failure-hunter gates apply
    in full to the absorbing BUILD. The spike's green-on-the-screen is not
    verification evidence.
  - The router is the only authority that may start the absorbing BUILD. The
    prototype skill NEVER transitions itself into BUILD; it emits the verdict
    and hands back to the router.
```

If you ever feel the pull of "this prototype code is good enough to keep as-is" — STOP. That feeling IS the leak this wall exists to stop.

## Step 1: State the ONE Question

Before writing a single line, write the question down — one sentence, at the top of the prototype file or its `NOTES.md`. The prototype exists only to answer it. Examples:

- "Does this state machine handle order-cancelled-then-refunded without a dead state?" (logic)
- "What should the settings dashboard look like — sidebar nav, tabbed, or single-scroll?" (UI)

If you cannot name the question in one sentence, you are not ready to prototype — you need brainstorming or a plan, not a spike. Route back.

## Step 2: Pick the Branch

The question's shape decides the artifact. Getting this wrong wastes the whole spike.

### Branch A — LOGIC question

> "Does this logic / state model / data shape feel right?"

Build a tiny interactive **harness or terminal TUI** that drives the model by hand through cases that are hard to reason about on paper.

- **Isolate the salvageable core.** Put the actual logic — the bit answering the question — behind a small **pure** interface (a reducer `(state, action) => state`, an explicit state machine, or a set of pure functions). No I/O, no terminal code inside it. This is the part that can be lifted out later; the harness around it is throwaway.
- **Build the thinnest shell that surfaces state.** On every action, re-render the full relevant state so the user sees exactly what changed. Keystroke → handler → mutate → re-render → loop until quit.
- **No persistence** unless persistence IS the question — then hit a scratch store named so it screams "PROTOTYPE, wipe me."
- One command to run it, using the project's existing task runner. Never make the user remember a path.

### Branch B — UI question

> "What should this look like?"

Generate **3-5 structurally DIFFERENT variants** on an existing route, switchable via a dev-only-gated `?variant=` URL param.

- **Prefer mounting on an existing route** (real header, real data, real density) over a bare new route — a variant in a vacuum always looks fine. Only create a throwaway route when the thing genuinely has no home; name it so `prototype` is obvious in the path, and follow the project's existing routing convention.
- **Variants must differ structurally** — different layout, hierarchy, primary affordance — not just colour or copy. Three tweaked card grids is wallpaper, not a prototype. Default to 3; cap at 5.
- **Switcher is dev-only.** Gate the floating switcher on `process.env.NODE_ENV !== 'production'` (or the project's equivalent) so a stray merge can never ship it. Arrow keys / arrows cycle variants and update the URL param so a variant is shareable and reload-stable. Don't intercept arrows while an input is focused.
- **Read-only.** Point any mutation at a stub. The question is "what should this look like," not "does the backend work."

If the question is genuinely ambiguous and the user is unreachable, default by surrounding code (backend module → Branch A; page/component → Branch B) and state the assumption at the top of the spike.

## Step 3: Hand It Over and Let It Run

Give the user the one run command (Branch A) or the URL plus `?variant=` keys (Branch B). They drive it. The valuable moments are "wait, that shouldn't be possible" (logic bug in the IDEA) and "I want the header from B with the sidebar from C" (the real design). Add actions or variants if asked — prototypes evolve.

## Step 4: Close-Out — Capture, Then Delete-or-Absorb (MANDATORY)

This is the accountable part. A spike with no close-out is a liability rotting in the repo. Two obligations, in order:

### 4a. Capture the ANSWER (router-owned — do NOT write memory directly)

The answer to the question is the only thing worth keeping. Do **NOT** edit `.cc10x/*.md` from this skill — memory stays single-writer and router-owned. Emit a machine-readable handoff at the end of your response so the router persists it via memory finalization:

```yaml
### Prototype Handoff (MACHINE-READABLE)
PROTOTYPE_QUESTION: "[the one question this spike answered]"
PROTOTYPE_ANSWER: "[the verdict — what the spike taught]"
PROTOTYPE_DISPOSITION: "delete" | "absorb"
ABSORB_TARGET: "[module/route to build for real, or N/A]"
MEMORY_NOTES: "[one-line durable lesson for ## Learnings, or N/A]"
```

The router routes `MEMORY_NOTES` into the workflow's memory-finalize task — the same path every cc10x agent uses. Never persist memory yourself.

### 4b. Decide: DELETE or ABSORB (no third option)

A prototype is never left as-is. Map this onto the **BUILD-DONE finishing menu + memory capture** the router already owns:

- **DELETE** — the spike answered the question and there is nothing salvageable to keep (a UI variant lost; a logic model was rejected; the answer is "don't build this"). Remove the spike code, the throwaway route, the switcher. Report the path removed. The answer survives in memory; the code does not.
- **ABSORB** — the spike's pure core (Branch A reducer/machine) or winning variant (Branch B) is worth keeping. This does **NOT** mean copy-pasting the spike into production. It means: the answer is "build it for real," which triggers a **fresh BUILD through the router** (see Hard Wall). Delete the throwaway harness/switcher; the salvageable core is re-implemented under full gates. Set `PROTOTYPE_DISPOSITION: absorb` and name `ABSORB_TARGET` so the router can open the absorbing BUILD.

The router treats this like its finishing gate: an explicit, gated decision before close — never an automatic, never-destructive-without-choice action. Deleting spike code the user might still want, or promoting it unverified, are both failures.

## Anti-Patterns

- **Adding tests to the spike.** A prototype that needs tests is no longer a prototype. (Tests belong to the absorbing BUILD.)
- **Wiring the spike to the real database / real mutations.** In-memory or stub, unless persistence is literally the question.
- **Generalising.** No "what if we want X later." One question, one answer.
- **Blurring the pure core into the harness/TUI.** The core must stay liftable; the shell is disposable.
- **Promoting the spike directly to production.** This is the Hard Wall violation. Absorb = fresh BUILD, not merge.
- **Writing memory directly.** Emit the handoff; the router persists.
- **Leaving the spike in the repo with no disposition.** Every prototype ends in delete or absorb.

## Router Routing Note

The router selects this skill for de-risking intents, not build/plan intents:

- Triggers: **"spike," "try out," "what should this look like," "prototype," "throwaway," "de-risk," "play with," "feel out," "rough version to see if."**
- Distinguish from PLAN (brainstorming/planner answer "what should we build and how" via dialogue — no runnable code) and from BUILD (ships gated, verified production code). Prototyping answers ONE narrow design question with disposable runnable code, then hands the verdict back.
- After close-out, the router decides next: a `delete` disposition ends the spike; an `absorb` disposition with an `ABSORB_TARGET` is the router's cue to open a fresh BUILD (which re-validates from scratch). The prototype skill never starts that BUILD itself.

## Final Check

Before completing a prototype:

- [ ] The ONE question is written down, verbatim, at the top of the spike
- [ ] Correct branch chosen (logic harness vs. UI variants); assumption stated if ambiguous
- [ ] Branch A: pure core isolated and liftable; no persistence unless that's the question
- [ ] Branch B: 3-5 structurally-different variants; switcher dev-only-gated
- [ ] Answer captured via the router-owned `### Prototype Handoff` block (no direct memory writes)
- [ ] Disposition decided: DELETE (code removed) or ABSORB (fresh BUILD named, not promoted)
- [ ] Hard Wall honored: no prototype rule followed into a BUILD
