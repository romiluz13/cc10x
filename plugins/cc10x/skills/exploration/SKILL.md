---
name: exploration
description: |
  Two-mode exploration skill: (1) design dialogue — turn rough ideas into validated
  designs through collaborative interview before planning; (2) spike — throwaway
  code answering ONE design question, deleted or absorbed, never shipped.
  Router invokes mode via dispatch context.
allowed-tools: Read Grep Glob AskUserQuestion Write Edit Bash
user-invocable: false
---

# Exploration (Design + Spike)

Two modes, selected by router dispatch context: `design` (brainstorm a design) or `spike` (throwaway prototype).

## Mode: DESIGN

Turn rough ideas into validated designs through collaborative dialogue. Understand what to build BEFORE designing how to build it. Use the user's domain language — don't invent new terminology when the repo or prompt already has a stable name.

### Scope Triage (Front of Flow)

Before opening the interview, decide whether this is ONE design or MANY. A request spanning multiple independent subsystems produces a sprawling, unfocused design.

**Multi-subsystem trigger:** 2+ pieces that could be built, tested, and shipped independently — different surfaces, data stores, deploy targets, or pieces joined only by "and."

If multi-subsystem: emit a decomposition recommendation (independent pieces, relationships, build order), then brainstorm ONLY the first sub-project. The router carries the rest forward.

### Synthesize-Now Fast Path

If goal + constraints + acceptance are ALL already evident from the prompt or context: skip the interview, draft the design directly, present for confirmation in ONE pass. Still record rejected alternatives (ADR notes). On correction, fix the named gap — don't restart the full interview.

**Gate:** take the fast path ONLY when all three are stated, not inferred. When in doubt, interview.

### Interview (when fast path gate fails)

Cover these 5 dimensions, but only ask about dimensions that are still unresolved. Skip a question when the answer is already explicit — write the inferred answer, mention the assumption, continue.

1. **Purpose** — what problem does this solve?
2. **Users** — who will use this?
3. **Success** — how will we know it works?
4. **Constraints** — limitations, requirements, out-of-scope
5. **Scope** — single module, single file, full feature, cross-cutting

Always ask: "What is explicitly NOT part of this?" (out-of-scope discovery).

One question at a time. Multiple choice preferred. Present 2-3 approaches with trade-offs before asking which to pursue. YAGNI ruthlessly — defer what is not essential.

**Intent Completeness Gate** (before proceeding to design): (1) small enough to fit in one paragraph, (2) contradiction-free, (3) sufficiently specific that a builder could act without clarifying questions. If any fails, ask one more targeted question.

### Domain Glossary + ADR Notes

Accrete domain vocabulary as the interview names terms. Record load-bearing rejected alternatives as ADR notes. Both are emitted in the handoff so the planner inherits the project's language and the rationale for rejected directions.

### Design Output

Save to `docs/plans/YYYY-MM-DD-<feature>-design.md` (use `-design.md` suffix, not `-plan.md`, to prevent collision with planner output).

Template: Purpose, Users, Success Criteria, Constraints, Out of Scope, Approach Chosen, Domain Glossary (if any), Decisions/ADR notes (if any), Architecture, Components, Data Flow, Error Handling, Testing Strategy, Observability (if applicable), UI Mockup (if UI feature), Questions Resolved.

### Design Self-Review Gate (MANDATORY — before handoff)

Scan the design for the 4 failures that corrupt downstream plans. Fix inline — no second review pass.

1. **No placeholders/TBD** — every section holds a real decision, not a stub. If N/A, say so explicitly.
2. **Internally consistent** — components in Architecture all appear in Data Flow; Error Handling covers the chosen Approach's failure modes; Success Criteria don't conflict with Constraints/Out-of-Scope.
3. **Single-plan scope** — one coherent thing a single plan can sequence. If it grew to span multiple subsystems, narrow to the first and record the rest in Out of Scope.
4. **No two-way-ambiguous requirements** — pick ONE interpretation, state it explicitly.

### Design Handoff (MACHINE-READABLE — do NOT edit .cc10x/*.md)

```yaml
### Brainstorming Handoff (MACHINE-READABLE)
DESIGN_FILE: "{PROJECT_DIR}/docs/plans/YYYY-MM-DD-<feature>-design.md"
DESIGN_SUMMARY: "[one-sentence summary]"
MEMORY_NOTES:
  glossary:
    - term: "[Term]"
      meaning: "[precise meaning]"
  decisions:
    - decision: "[what was chosen]"
      rejected: "[alternative not taken]"
      why: "[the constraint or trade-off that decided it]"
```

Router carries design forward and persists memory. Do NOT write memory yourself.

---

## Mode: DOUBT (Doubt-Driven Development)

For non-trivial decisions where correctness matters more than speed: subject the decision to a fresh-context adversarial review BEFORE it stands. This is IN-FLIGHT course correction, not post-hoc review.

### When to Use

- Working in unfamiliar code
- Stakes are high (production, security-sensitive, irreversible operations)
- A confident output would be cheaper to verify now than to debug later
- The decision involves >2 non-trivial trade-offs

### The 5-Step Cycle

1. **CLAIM** — state the decision as a testable claim in one paragraph: "We will use X because Y"
2. **EXTRACT** — extract the artifacts the claim depends on: the key assumptions, plus concrete evidence (code samples, API signatures, data flows) that support them
3. **DOUBT** — spawn a fresh-context adversarial review. The reviewer gets the ARTIFACT + CONTRACT only, NOT the CLAIM — prevents biasing toward agreement. The reviewer's job: find the weakest assumption, the scenario where the decision backfires.
4. **RECONCILE** — compare the reviewer's independent assessment against the original claim. Where they agree → high confidence. Fix the decision, strengthen the assumption, or reject the finding with evidence.
5. **STOP** — escalate to the user when EITHER: (a) a cycle produces substantive findings but zero are classified as actionable (doubt theater, not doubting), or (b) 3 cycles complete without convergence (the 3-cycle cap — don't loop forever).

**Cross-model option:** in interactive mode, offer to run the doubt review through a different model family (e.g., Gemini, Codex) for genuine independence. Never silently skip offering this.

**Rationalization guard:** "This is too simple to doubt" → simple decisions have simple artifacts, so the doubt review is fast. No excuse to skip.

### What This Is NOT

- NOT post-hoc review on completed work — this is in-flight, while changes are still cheap
- NOT self-critique — the doubter must be a fresh context, not the same reasoning head
- NOT perfectionism — one cycle is often enough. Escalate only when findings are substantive AND actionable.

---

## Mode: SPIKE

A prototype is **throwaway code that answers exactly ONE design question**. It exists to de-risk an unknown cheaply before paying for the full BUILD chain.

### Hard Wall (read before writing any prototype)

A prototype's rules NEVER leak into a BUILD. "No tests, no abstractions, move fast" lives and dies inside the spike. If the answer is "build it for real," that is a **fresh BUILD through the router** with full TDD/reviewer/verifier gates. The spike's code does not become production by surviving.

<!-- scar: 2026-06-17 — spike's "move fast, no tests" code promoted to production by inertia, skipping TDD/verifier gates. The prototype proving a question is NOT the same as the answer being shipped. -->

### Step 1: State the ONE Question

Write it down — one sentence at the top. The prototype exists only to answer it. If you can't name the question in one sentence, you need design mode or a plan, not a spike.

### Step 2: Pick the Branch

**Branch A — LOGIC question** ("does this logic/state model feel right?"):

- Build a tiny interactive harness/TUI that drives the model by hand
- Isolate the salvageable core behind a pure interface (reducer, state machine, pure functions) — no I/O, no terminal code inside it. This is the part that can be lifted later
- No persistence unless persistence IS the question

**Branch B — UI question** ("what should this look like?"):

- Generate 3-5 structurally DIFFERENT variants on an existing route, switchable via `?variant=` URL param
- Variants must differ structurally (layout, hierarchy, primary affordance) — not just color or copy
- Switcher is dev-only: gate on `process.env.NODE_ENV !== 'production'`
- Read-only: point mutations at a stub

### Step 3: Hand It Over

Give the user the one run command (Branch A) or the URL + `?variant=` keys (Branch B). They drive it. The valuable moments are "wait, that shouldn't be possible" (logic bug) and "I want header from B with sidebar from C" (the real design).

### Step 4: Close-Out (MANDATORY)

**4a. Capture the answer** (router-owned — do NOT write memory directly):

```yaml
### Prototype Handoff (MACHINE-READABLE)
PROTOTYPE_QUESTION: "[the one question]"
PROTOTYPE_ANSWER: "[the verdict]"
PROTOTYPE_DISPOSITION: "delete" | "absorb"
ABSORB_TARGET: "[module/route to build for real, or N/A]"
MEMORY_NOTES: "[one-line durable lesson, or N/A]"
```

**4b. DELETE or ABSORB** (no third option):

- **DELETE** — spike answered the question, nothing salvageable. Remove spike code, throwaway route, switcher. Answer survives in memory; code does not.
- **ABSORB** — spike's pure core or winning variant is worth keeping. This triggers a **fresh BUILD through the router** (full gates). Delete the throwaway harness; re-implement the core under TDD/reviewer/verifier. Set `PROTOTYPE_DISPOSITION: absorb` and name `ABSORB_TARGET` so the router opens the absorbing BUILD.

The prototype skill NEVER transitions itself into BUILD. It emits the verdict and hands back to the router.
