# Deep Comparison: Planning & Architecture Methodology

**Projects analyzed:** cc10x, Superpowers, Matt Pocock (pi-optimize)
**Date:** 2025-07-14
**Scope:** Planning approaches, architecture decisions, planning gates, brainstorming/ideation, unique patterns, cross-project adoption opportunities, and methodology ratings.

---

## Table of Contents

1. [How Each Project Approaches Planning](#1-how-each-project-approaches-planning)
2. [How Each Project Handles Architecture Decisions](#2-how-each-project-handles-architecture-decisions)
3. [Planning Gates Each Project Enforces](#3-planning-gates-each-project-enforces)
4. [How Each Project Handles Brainstorming/Ideation](#4-how-each-project-handles-brainstormingideation)
5. [Planning Patterns cc10x Has That the Others DON'T](#5-planning-patterns-cc10x-has-that-the-others-dont)
6. [Planning Patterns the Others Have That cc10x SHOULD Adopt](#6-planning-patterns-the-others-have-that-cc10x-should-adopt)
7. [Methodology Ratings](#7-methodology-ratings)
8. [Verdict](#8-verdict)

---

## 1. How Each Project Approaches Planning

### cc10x — Multi-Mode Contract-First Planning

cc10x has the most structurally sophisticated planning system of the three. It uses a **tri-mode planning system** routed through a dedicated planner agent:

| Mode | Trigger | Content Required |
| ------ | --------- | ----------------- |
| `direct` | Trivial, low-risk, single-surface | Requirements, constraints, acceptance checks |
| `execution_plan` | Standard implementation with sequential phases | Requirements, constraints, open decisions, phase plan, acceptance checks |
| `decision_rfc` | Architecture decisions, refactors, library choices | Motivation, current state, alternatives, drawbacks, recommendation, phased plan |

**Key design principles:**

- **A plan is a contract, not a brainstorm** — the planning SKILL says this explicitly.
- **Agreement-first:** if a requirement is materially ambiguous, the planner returns `STATUS=NEEDS_CLARIFICATION` rather than guessing. No hidden assumptions, no implied approval.
- **Bite-sized tasks:** Each task must be completable in 30-90 minutes. "Test per task" is mandatory — if you can't name the test, the task isn't specific enough.
- **Consumes/Produces blocks:** Every task lists exact signatures it uses from earlier phases (`Consumes`) and exact names later phases rely on (`Produces`), verbatim-matched. This creates a typed contract graph across tasks.
- **Two-layer artifact:** Human Layer (what + why) on top, Execution Contract Layer (buildable without improvisation) below.
- **Codebase Reality Check:** The planner must identify exact files, modules, patterns, and integration points from the real repo. A "structurally neat but repo-wrong plan is a failed plan."
- **Verification rigor:** Two levels — `standard` (default) and `critical_path` (for security, money, state machines, concurrency, irreversible migrations). Critical-path plans require behavior contracts, edge-case catalogs, provable properties, purity boundary maps.
- **Autonomy classification:** Each phase is labeled `AFK` or `HITL` with a reason-category (judgment-call, external-access, design-decision, manual-verification).

**Plan document structure:**

```
# [Feature Name] Plan
## Metadata (status, verification rigor, plan mode)
## Agreement Snapshot (goal, constraints, in/out of scope, open decisions)
## Tasks (each with: objective, files, dependencies, scope, drift, artifacts, checks, checkpoint, exit criteria, consumes, produces)
## Risk-Based Testing Matrix
## Functionality Flow Mapping
## ADRs (inline)
```

### Superpowers — Spec-to-Plan Linear Pipeline

Superpowers uses a **two-stage linear pipeline**: brainstorming → writing-plans → executing-plans. Each stage produces a distinct artifact that feeds the next.

**Stage 1 — Brainstorming (spec):** Collaborative dialogue that produces a design spec saved to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`. The spec covers architecture, components, data flow, error handling, and testing. A HARD-GATE prevents any implementation until the design is approved.

**Stage 2 — Writing Plans:** Takes the approved spec and creates a detailed implementation plan saved to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`. Key principles:

- **Assume zero context and questionable taste** — the plan is written for an engineer who knows almost nothing about the codebase or domain.
- **Bite-sized steps (2-5 minutes each):** "Write the failing test" → "Run it to see it fail" → "Implement minimal code" → "Run test to verify pass" → "Commit." Each step is one action.
- **No placeholders rule:** Every step must contain actual content. "TBD", "add appropriate error handling", "write tests for the above" are all listed as **plan failures**.
- **Complete code in every step:** If a step changes code, it shows the full code.
- **File structure mapping:** Before defining tasks, map which files will be created/modified and what each is responsible for. Decomposition decisions are locked here.
- **Self-review:** After writing the plan, the author does a 3-point check: spec coverage, placeholder scan, type consistency. Fixes are inline.

**Stage 3 — Executing Plans:** Load plan → review critically → execute tasks with checkboxes → run verifications → report. Stops immediately on blockers.

**Key difference from cc10x:** Superpowers writes the plan as a step-by-step recipe with complete code inline. cc10x writes the plan as a contract with typed interfaces between phases. Superpowers is more prescriptive about *how* to build; cc10x is more prescriptive about *what* must be agreed upon before building.

### Matt Pocock — Deep-Module Design Discipline

Matt Pocock's approach is fundamentally different from both cc10x and Superpowers. It's not a planning pipeline — it's an **architecture vocabulary and design methodology**.

**Core concept — Deep Modules:** Design modules with "a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface." This is based on Ousterhout's "A Philosophy of Software Design" but adapted (depth-as-leverage instead of depth-as-line-ratio).

**Four skills form the architecture toolkit:**

1. **codebase-design:** Shared vocabulary (module, interface, seam, adapter, depth, leverage, locality). Principles: deletion test, "interface is the test surface", "one adapter = hypothetical seam, two = real."
2. **domain-modeling:** Active discipline of building a ubiquitous language glossary (`CONTEXT.md`) and recording ADRs (`docs/adr/`). ADRs are offered sparingly — only when hard to reverse, surprising without context, and the result of a real trade-off.
3. **improve-codebase-architecture:** Scans codebase for "deepening opportunities" (shallow → deep module refactors). Produces an HTML report with before/after diagrams, then grills through the chosen candidate.
4. **prototype:** Throwaway code answering ONE design question. Two branches: LOGIC (interactive TUI driving a state model) and UI (multiple structurally different variants on a route, switchable via `?variant=`).

**There is no "plan" artifact in Matt Pocock's system.** There are design decisions, domain models, ADRs, and prototypes. The planning is implicit in the design vocabulary — you design deep modules, and the implementation follows naturally from the interface contract.

**Key strengths:**

- **Design It Twice:** Spawn 3+ parallel sub-agents, each with a different design constraint (minimize interface, maximize flexibility, optimize common case). Compare on depth, locality, seam placement. This is a genuinely unique pattern.
- **Deepening methodology:** The DEEPENING.md file provides a dependency-category framework (in-process, local-substitutable, remote-but-owned, true-external) that determines testing strategy for each deepened module.
- **HTML architecture reports:** Visual before/after diagrams with Mermaid + custom SVG, showing the shallowness problem and the deepening solution.

---

## 2. How Each Project Handles Architecture Decisions

### cc10x

cc10x handles architecture decisions through three mechanisms:

1. **Inline ADRs in plans:** For decisions with material trade-offs (library choice, architecture pattern, data model), the planning SKILL specifies an ADR format: Context, Decision, Rejected Alternatives, Consequences. These are recorded inline in the plan and inherited by the next session.

2. **Architecture skill (greenfield):** A dedicated `architecture` SKILL for greenfield design with a functionality-first design process:
   - Phase 1: Map functionality flows (every flow, every error path)
   - Phase 2: Map flows to architecture (flow steps → components, error paths → error handling, data crossings → interfaces)
   - Phase 3: Design components (interface, responsibility, dependencies, state, error handling)
   - C4 views: System Context, Container View, Component View
   - LSP-powered analysis (go-to-definition, find-references, call graphs)
   - API design from functionality, not data model
   - Dependency classification: Owned, Wrapped, Consumed, Infra
   - Observability design per component
   - Decision framework with reversibility assessment

3. **Decision RFC mode:** The `decision_rfc` plan mode is specifically for architecture decisions, refactors, library choices. It requires motivation, current state, ≥2 alternatives, ≥1 drawbacks, recommendation, phased plan.

4. **ADR-as-constraint:** The planner reads pre-existing ADRs (`docs/adr/`, `docs/decisions/`, `docs/rfcs/`) and treats them as SETTLED. If a plan contradicts one, it must flag it explicitly.

### Superpowers

Superpowers handles architecture decisions within the brainstorming/spec phase:

- The brainstorming skill covers "architecture, components, data flow, error handling, testing" as design sections.
- Design for isolation and clarity: break system into smaller units with one clear purpose, well-defined interfaces, independently testable.
- "Design units with clear boundaries" is mentioned in writing-plans' File Structure section.
- No explicit ADR format or mechanism. No dedicated architecture skill.
- No dependency classification or observability design.
- Architecture decisions are embedded in the spec document but lack the structured ADR format that cc10x and Matt Pocock provide.

### Matt Pocock

Matt Pocock handles architecture decisions through two mechanisms:

1. **ADR system (domain-modeling skill):** ADRs live in `docs/adr/` with sequential numbering. The format is deliberately minimal — "An ADR can be a single paragraph." The value is in recording *that* a decision was made and *why*. Optional sections (Status, Considered Options, Consequences) only when they add genuine value.

   The ADR qualification criteria are the most precise of any project:
   - Hard to reverse
   - Surprising without context
   - Result of a real trade-off

   If any is missing, skip the ADR. This prevents ADR proliferation.

2. **Deep-module design methodology (codebase-design skill):** Architecture decisions are about *module shape* — depth, seam placement, interface size. The decision framework includes:
   - **Deletion test:** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
   - **One adapter = hypothetical seam, two = real:** Don't introduce a seam unless something actually varies across it.
   - **Design It Twice:** Generate 3+ radically different interface designs in parallel, compare on depth/locality/seam placement.
   - **Dependency categories** determine testing strategy: in-process (direct test), local-substitutable (stand-in), remote-but-owned (ports & adapters), true-external (mock).

3. **HTML architecture reports (improve-codebase-architecture skill):** Visual before/after diagrams with recommendation strength badges (Strong, Worth exploring, Speculative). ADR conflicts are flagged with warning callouts.

---

## 3. Planning Gates Each Project Enforces

### cc10x — Three-Layer Gate System

cc10x has the most elaborate gate system of any project:

**Gate 1: Plan Completeness Gate (inline, in planning SKILL)**
10 mandatory checks before save:

1. Every task has a test
2. Every task lists exact file paths
3. Every task has exit criteria
4. Dependencies are explicit (task IDs)
5. Scope drift is named
6. Consumes/Produces are verbatim-matched
7. Validation level stated for every task
8. Risk-based testing matrix is complete
9. No placeholders/TBD
10. Open decisions are listed

**Gate 2: Plan Review Gate (inline, in planner agent)**
A fail-closed adversarial review skill with 3 checks run in sequence:

- **Check 1: Feasibility** — file paths exist, codebase reality check present, dependency ordering correct, technical approach matches codebase, no unstated infra assumptions, plan mode fits, verification rigor fits.
- **Check 2: Completeness** — all requirements mapped, verification steps defined, edge cases addressed, cross-file integration covered, plan-vs-code gaps surfaced, assumption ledger honest, phase dependency map present, durable decisions present, decision-grade content for RFCs, critical-path spec present.
- **Check 3: Scope & Alignment** — matches user request, no scope creep, no under-scoping, execution order real, complexity proportional, defaults framed honestly, agreement fidelity holds, human layer matches execution contract, hidden future work explicit, architecture contradictions surfaced.

Result: `SPEC_GATE_PASS` or `SPEC_GATE_FAIL` (no "approved with comments"). Max 3 iterations before escalation.

**Gate 3: Fresh Review DAG (external, plan-gap-reviewer agent)**
A separate agent does an anti-anchoring review:

- Pre-created bounded review DAG: `plan-create → plan-review-gap-1 → re-plan → plan-review-gap-2 → memory-finalize`
- Maximum 2 fresh-review passes
- Reviewer stays context-clean: does NOT load `.cc10x/*.md`, does NOT infer authority from prior planner confidence
- Finding categories: `repo_mismatches`, `missing_surfaces`, `execution_order_issues`, `hidden_assumptions`, `under_scoped_integrations`, `open_decisions_presented_as_settled`
- Severity: `BLOCKING` or `ADVISORY`
- Freshness rule: uses only original user request, saved plan, current codebase, and explicitly provided design/research files

**Gate 4: Hidden-Assumption Pass (in planner agent)**
Classify all assumptions as `proven_by_code`, `inferred`, or `needs_user_confirmation`. Expose unproven critical assumptions.

**Gate 5: Plan Self-Review (in planner agent)**
Scan for cross-phase contract drift. Every `Consumes` in a later phase must verbatim-match a `Produces` in an earlier phase. Spelling/signature drift must be fixed inline. Dangling references are PLAN FAILURES.

### Superpowers — Two Gates

**Gate 1: Spec Self-Review (in brainstorming skill)**
4-point inline check after writing the spec:

1. Placeholder scan (TBD, TODO, incomplete sections)
2. Internal consistency (sections contradicting each other)
3. Scope check (focused enough for a single plan)
4. Ambiguity check (could any requirement be interpreted two ways?)

Fix inline, no re-review needed.

**Gate 2: User Review Gate**
After spec self-review passes, the user is explicitly asked to review the written spec before proceeding:
> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Wait for response. If changes requested, make them and re-run self-review. Only proceed once user approves.

**Gate 3: Plan Self-Review (in writing-plans skill)**
3-point inline check after writing the plan:

1. Spec coverage (can you point to a task for each spec requirement?)
2. Placeholder scan (search for red-flag patterns)
3. Type consistency (do types/signatures/property names match across tasks?)

Fix inline, no re-review needed.

**Gate 4: Critical Review at Execution (in executing-plans skill)**
Step 1 of execution: "Review critically - identify any questions or concerns about the plan." If concerns, raise them before starting.

**Gate 5: Spec Document Reviewer (optional subagent)**
A subagent dispatch template for reviewing the spec: checks completeness, consistency, clarity, scope, YAGNI. "Approve unless there are serious gaps that would lead to a flawed plan."

### Matt Pocock — Implicit Gates

Matt Pocock has the fewest explicit gates:

**Gate 1: ADR Qualification Gate (in domain-modeling skill)**
ADRs are only created when all three criteria are met: hard to reverse, surprising without context, result of a real trade-off. This is a gate against ADR proliferation.

**Gate 2: Deletion Test (in codebase-design skill)**
"Imagine deleting the module. If complexity vanishes, it was a pass-through." This is a design-time gate against shallow modules.

**Gate 3: Two-Adapter Rule (in codebase-design skill)**
"One adapter means a hypothetical seam. Two adapters means a real one." This is a gate against premature abstraction.

**Gate 4: Prototype Disposition (in prototype skill)**
After prototyping, there is no third option besides DELETE or ABSORB. If absorbing, a fresh BUILD through the router with full gates is required — the prototype's code doesn't become production by surviving.

**Gate 5: Architecture Report ADR Conflict Check (in improve-codebase-architecture skill)**
If a deepening candidate contradicts an existing ADR, it's only surfaced when the friction is real enough to warrant revisiting. Marked clearly with a warning callout.

---

## 4. How Each Project Handles Brainstorming/Ideation

### cc10x — Exploration Skill (Design + Spike Modes)

cc10x has a dedicated `exploration` SKILL with two modes dispatched by the router:

**Design Mode:**

- **Scope triage at front of flow:** If a request spans multiple independent subsystems (2+ pieces that could be built/tested/shipped independently), emit a decomposition recommendation and brainstorm only the first sub-project.
- **Synthesize-Now Fast Path:** If goal + constraints + acceptance are ALL already evident from the prompt, skip the interview and draft the design directly in ONE pass. Gate: only when all three are *stated*, not *inferred*. When in doubt, interview.
- **Interview (5 dimensions):** Purpose, Users, Success, Constraints, Scope. Only ask about dimensions that are still unresolved. Skip when the answer is already explicit. One question at a time. Multiple choice preferred. Present 2-3 approaches with trade-offs before asking which to pursue.
- **Intent Completeness Gate:** Before proceeding to design — (1) small enough for one paragraph, (2) contradiction-free, (3) specific enough that a builder could act without clarifying questions.
- **Domain Glossary + ADR Notes:** Accrete domain vocabulary as terms are named. Record load-bearing rejected alternatives as ADR notes. Both are emitted in the machine-readable handoff.
- **Design Self-Review Gate (mandatory before handoff):** 4 checks — no placeholders/TBD, internally consistent, single-plan scope, no two-way-ambiguous requirements. Fix inline.
- **Machine-readable handoff:** YAML format with DESIGN_FILE, DESIGN_SUMMARY, MEMORY_NOTES (glossary, decisions). Router carries design forward and persists memory.

**Spike Mode:**

- **One question only:** The prototype exists to answer exactly ONE design question. If you can't name it in one sentence, you need design mode or a plan, not a spike.
- **Hard Wall:** Prototype rules NEVER leak into BUILD. "No tests, no abstractions, move fast" lives and dies inside the spike.
- **Two branches:** LOGIC (interactive harness/TUI driving a state model, isolate salvageable core behind a pure interface) or UI (3-5 structurally different variants on an existing route, switchable via `?variant=` URL param).
- **Close-out is mandatory:** Capture the answer (machine-readable YAML handoff), then DELETE or ABSORB (no third option). Absorbing triggers a fresh BUILD through the router with full gates.
- **Scar record:** A dated note (2026-06-17) records a past failure where spike code was promoted to production by inertia, skipping TDD/verifier gates.

**Workflow integration:** Brainstorming ALWAYS runs for PLAN workflows. If a design file exists, brainstorming uses it as a foundation. If not, it starts from the user's request. After completion, the router parses the machine-readable handoff and passes it to the planner.

### Superpowers — Brainstorming Skill

Superpowers has a dedicated brainstorming skill that is the mandatory entry point for all creative work:

- **HARD-GATE:** "Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it."
- **Anti-pattern guard:** "This Is Too Simple To Need A Design" — every project goes through the process, even a todo list or config change. "Simple projects are where unexamined assumptions cause the most wasted work."
- **9-step checklist:** Explore project context → offer visual companion just-in-time → ask clarifying questions → propose 2-3 approaches → present design → write design doc → spec self-review → user reviews written spec → transition to writing-plans.
- **Visual companion:** A browser-based tool for showing mockups, diagrams, and visual options during brainstorming. Offered just-in-time (not upfront), per-question decision (browser vs terminal based on whether seeing is better than reading). Has a full server infrastructure with HTML content fragments, CSS classes, and interactive option selection.
- **Scope check:** If the spec covers multiple independent subsystems, suggest breaking into separate plans — one per subsystem.
- **One question at a time:** Multiple choice preferred. Focus on purpose, constraints, success criteria.
- **Design for isolation and clarity:** Break system into smaller units with one clear purpose, well-defined interfaces, independently testable.
- **Terminal state is always writing-plans:** The ONLY skill invoked after brainstorming is writing-plans. No other implementation skill.

### Matt Pocock — No Dedicated Brainstorming

Matt Pocock has **no dedicated brainstorming/ideation skill**. Instead, ideation is distributed across the architecture skills:

- **improve-codebase-architecture:** The "explore" phase walks the codebase looking for friction (shallow modules, pure functions extracted just for testability, coupled modules leaking across seams). This is exploration of existing code, not greenfield ideation.
- **codebase-design DESIGN-IT-TWICE:** The closest thing to brainstorming — spawns 3+ parallel sub-agents to design radically different interfaces for a chosen deepening candidate. This is parallel ideation on a specific design question.
- **prototype:** Throwaway code to answer ONE design question. This is empirical ideation — you don't brainstorm, you build a tiny thing and see what it teaches you.
- **domain-modeling:** "Discuss concrete scenarios" — stress-test domain relationships with specific scenarios that probe edge cases. This is dialectical ideation through conversation.

The philosophy is: **design through making, not through talking.** Prototype to learn. Design it twice to compare. Model the domain to sharpen language. Scan the codebase to find friction. There's no "sit down and brainstorm" step.

---

## 5. Planning Patterns cc10x Has That the Others DON'T

| Pattern | Description | Unique Value |
| --------- | ------------- | -------------- |
| **Tri-mode planning (direct / execution_plan / decision_rfc)** | Three distinct plan modes with different content requirements, auto-triggered based on task type | Prevents over-planning trivial work and under-planning complex decisions. Neither other project has this. |
| **Verification rigor levels (standard / critical_path)** | Two-tier verification with critical_path requiring provable properties, behavior contracts, edge-case catalogs, purity boundary maps | Proportional verification — not everything needs the same depth. Unique to cc10x. |
| **Fresh-review DAG with anti-anchoring** | Pre-created bounded review DAG (plan-create → review-gap-1 → re-plan → review-gap-2 → memory-finalize) with a separate context-clean agent | This is the most sophisticated review mechanism of any project. The anti-anchoring principle (reviewer doesn't load memory, doesn't infer authority from prior confidence) is genuinely novel. |
| **Plan Review Gate (3-check adversarial, fail-closed)** | Inline adversarial review with Feasibility, Completeness, Scope & Alignment checks. No "approved with comments." Max 3 iterations before escalation | Harder than Superpowers' self-review. More structured than Matt Pocock's implicit gates. |
| **Consumes/Produces typed contract graph** | Every task lists exact signatures consumed from earlier phases and exact names produced for later phases, verbatim-matched | Creates a typed dependency graph across tasks. Neither other project has this level of cross-task contract enforcement. |
| **Autonomy classification (AFK / HITL)** | Each phase labeled AFK or HITL with reason-category (judgment-call, external-access, design-decision, manual-verification) | Enables unattended execution planning. Neither other project has this. |
| **Machine-readable router contract** | YAML output with STATUS, PLAN_MODE, VERIFICATION_RIGOR, CONFIDENCE, SCENARIOS, ASSUMPTIONS, DECISIONS, OPEN_DECISIONS, etc. | Enables programmatic orchestration. Neither other project has machine-readable plan contracts. |
| **Risk-based testing matrix** | Probability × Impact scoring for each risk, with deterministic/manual/probabilistic validation levels | Forces explicit risk assessment. Neither other project has this. |
| **Functionality flow mapping** | Every user flow step and every error path mapped to a specific test name | Ensures no untested steps. Neither other project has this. |
| **Durability-horizon rule** | For each plan piece, state how long it's expected to last: "session-only", "sprint", "stable" | Determines abstraction effort. Neither other project has this. |
| **Test-seam selection discipline** | Choose where the test attaches: unit seam, integration seam, E2E seam. Prefer highest seam that still covers the risk | Neither other project has this. |
| **Prefactor question** | "Will this abstraction be used by >1 caller within the next 3 sprints?" If no, inline it | Gate against premature abstraction. Neither other project has this. |
| **Scar records** | Dated failure notes (e.g., "2026-06-17 — spike's 'move fast, no tests' code promoted to production by inertia") | Institutional memory of past failures. Neither other project has this. |
| **Agreement-first protocol** | Planner never treats its own defaults as approved. Returns NEEDS_CLARIFICATION for material ambiguity | Neither other project has this explicit protocol. |
| **LSP-powered architecture analysis** | Go-to-definition, find-references, incoming/outgoing calls to map the dependency graph before designing | cc10x architecture skill has this. Matt Pocock's codebase-design skill explores organically but doesn't mention LSP. |
| **Dependency classification (Owned/Wrapped/Consumed/Infra)** | Four-class system tracking coupling risk | Neither other project has this. Matt Pocock has dependency categories for testing (in-process, local-substitutable, remote-but-owned, true-external) but these serve a different purpose. |

---

## 6. Planning Patterns the Others Have That cc10x SHOULD Adopt

| Pattern | Source | Description | Why cc10x Should Adopt It |
| --------- | -------- | ------------- | --------------------------- |
| **Deep-module vocabulary** | Matt Pocock (codebase-design) | Consistent terminology: module, interface, seam, adapter, depth, leverage, locality. "Use these terms exactly — don't substitute." | cc10x's architecture skill uses generic terms (component, interface, dependency). A shared deep-module vocabulary would make architecture decisions more precise and comparable across plans. |
| **Deletion test** | Matt Pocock (codebase-design) | "Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep." | This is a stronger gate against shallow modules than cc10x's prefactor question. Both address premature abstraction, but the deletion test is more visceral and testable. |
| **Two-adapter rule** | Matt Pocock (codebase-design) | "One adapter means a hypothetical seam. Two adapters means a real one." Don't introduce a seam unless something actually varies across it. | More concrete than cc10x's prefactor question. Gives a falsifiable test for whether an abstraction is justified. |
| **Design It Twice (parallel interface exploration)** | Matt Pocock (codebase-design) | Spawn 3+ parallel sub-agents, each with a different design constraint (minimize interface, maximize flexibility, optimize common case). Compare on depth, locality, seam placement. | cc10x's exploration skill presents 2-3 approaches with trade-offs, but sequentially and conversationally. Parallel sub-agent exploration would produce more radically different designs and enable systematic comparison. This could be a new mode in the exploration skill. |
| **Dependency-category testing strategy** | Matt Pocock (DEEPENING.md) | Four categories (in-process, local-substitutable, remote-but-owned, true-external) each with a defined testing strategy (direct test, stand-in, ports & adapters, mock) | cc10x has dependency classification (Owned/Wrapped/Consumed/Infra) but doesn't connect it to testing strategy. Matt Pocock's categories directly determine how to test. cc10x should bridge this gap. |
| **Minimal ADR format** | Matt Pocock (domain-modeling) | "An ADR can be a single paragraph." Three-gate qualification (hard to reverse, surprising without context, real trade-off). Optional sections only when they add genuine value. | cc10x's ADR format (Context, Decision, Rejected Alternatives, Consequences) is more structured but may lead to ADR proliferation. Matt Pocock's minimal format and qualification gate prevent ceremony. |
| **CONTEXT.md domain glossary** | Matt Pocock (domain-modeling) | A living glossary file with "Be opinionated" rules, `_Avoid_` synonyms, tight definitions, and multi-context support via CONTEXT-MAP.md | cc10x's exploration skill accretes a domain glossary in the handoff, but it's ephemeral. A persistent CONTEXT.md would make domain language durable across sessions and plans. |
| **HTML architecture report with before/after diagrams** | Matt Pocock (improve-codebase-architecture) | Self-contained HTML file with Tailwind + Mermaid, before/after visualizations, recommendation strength badges, ADR conflict callouts | cc10x's architecture skill produces text-based C4 views. Visual reports would make architecture decisions more communicable to stakeholders. |
| **Complete code in every plan step** | Superpowers (writing-plans) | If a step changes code, show the full code. No "implement appropriate error handling" — show the actual code. | cc10x's plan structure focuses on contracts (Consumes/Produces, exit criteria) but doesn't require inline code. For execution_plan mode, requiring complete code in steps would reduce improvisation by builders. |
| **No-placeholders-as-plan-failures rule** | Superpowers (writing-plans) | Explicit list of forbidden patterns: "TBD", "add appropriate error handling", "handle edge cases", "write tests for the above", "similar to Task N" | cc10x has "No placeholders/TBD" as check #9 in the completeness gate, but Superpowers' explicit catalog of forbidden patterns is more actionable. |
| **Visual companion for brainstorming** | Superpowers (brainstorming) | Browser-based tool for showing mockups, diagrams, and visual options during brainstorming, with just-in-time offering and per-question browser/terminal decisions | cc10x's exploration skill is purely text-based. For UI-heavy features, a visual companion would dramatically improve design quality. |
| **User review gate on spec** | Superpowers (brainstorming) | After spec self-review passes, the user is explicitly asked to review the written spec before proceeding to planning | cc10x has the intent completeness gate and design self-review gate, but no explicit "user must review the design document" step. The machine-readable handoff goes to the router, not to the user for approval. |
| **Execution handoff with mode choice** | Superpowers (writing-plans) | After saving the plan, offer execution choice: subagent-driven (fresh subagent per task, review between tasks) vs inline (batch with checkpoints) | cc10x's router manages execution orchestration, but the plan itself doesn't surface execution mode options to the user. |
| **Grilling loop for architecture candidates** | Matt Pocock (improve-codebase-architecture) | After presenting deepening candidates, run a grilling skill to walk the design tree — constraints, dependencies, shape of the deepened module, what tests survive | cc10x's architecture skill has Phase 1-3 design process but no interactive grilling loop to stress-test the design. |

---

## 7. Methodology Ratings

### cc10x — Rating: 8.5/10

**Strengths:**

- Most structurally complete planning system of the three
- Tri-mode planning prevents both over-planning and under-planning
- Three-layer gate system (completeness gate, plan review gate, fresh-review DAG) is the most rigorous in the industry
- Machine-readable contracts enable programmatic orchestration
- Risk-based testing matrix, functionality flow mapping, and durability-horizon are genuinely novel
- Consumes/Produces typed contract graph catches cross-phase drift that other projects miss
- Autonomy classification (AFK/HITL) is essential for unattended execution
- Scar records provide institutional memory

**Weaknesses:**

- No shared architecture vocabulary (uses generic terms like "component" instead of "module", "interface", "seam")
- ADR format is structured but lacks qualification gates (may lead to ADR proliferation)
- No persistent domain glossary (glossary is ephemeral in the handoff)
- No visual companion for UI-heavy brainstorming
- No "Design It Twice" parallel interface exploration
- No explicit user review gate on the design document (machine-readable handoff goes to router)
- Heavy process — the three-layer gate system may be overkill for small tasks (mitigated by the `direct` mode and trivial-skip in plan-review-gate)
- No complete-code-in-steps requirement for execution plans

### Superpowers — Rating: 7/10

**Strengths:**

- Clean two-stage pipeline (spec → plan) with clear terminal states
- No-placeholders rule is the most actionable version of this pattern
- Complete code in every step ensures builders never need to improvise
- Visual companion is genuinely innovative for agentic brainstorming
- User review gate ensures human approval before planning begins
- HARD-GATE prevents implementation before design approval
- "This is too simple to need a design" anti-pattern guard is excellent
- Execution handoff with mode choice is user-friendly

**Weaknesses:**

- No tri-mode planning — one plan format for everything
- No verification rigor levels — everything gets the same depth
- No fresh-review agent — self-review only, no anti-anchoring
- No machine-readable contracts — plans are for humans only
- No risk-based testing matrix
- No Consumes/Produces typed contract graph
- No autonomy classification (AFK/HITL)
- No ADR format or mechanism
- No dependency classification
- No architecture-specific skill (greenfield or retrofit)
- Self-review is lighter than cc10x's adversarial gate
- Spec reviewer is optional subagent, not mandatory

### Matt Pocock — Rating: 7.5/10

**Strengths:**

- Deepest architecture vocabulary of the three (module, interface, seam, adapter, depth, leverage, locality)
- Deletion test and two-adapter rule are the most concrete abstraction-justification gates
- Design It Twice is a genuinely unique parallel-ideation pattern
- Dependency-category testing strategy is the most actionable testing framework
- Minimal ADR format with qualification gates prevents ceremony
- CONTEXT.md domain glossary is the best domain-language system
- HTML architecture reports are the most communicable format
- Prototype skill with LOGIC/UI branches is well-designed
- Grilling loop for architecture candidates is excellent

**Weaknesses:**

- No planning artifact — no "plan" document, just design decisions and domain models
- No plan gate system — no completeness check, no adversarial review, no fresh-review
- No risk-based testing matrix
- No functionality flow mapping
- No verification rigor levels
- No machine-readable contracts
- No autonomy classification
- No tri-mode planning
- No Consumes/Produces contract graph
- No execution skill — design is decoupled from implementation
- No workflow orchestration — skills are standalone, not pipeline-integrated
- No scar records or institutional memory
- Brainstorming is distributed and implicit, not a dedicated skill

---

## 8. Verdict

### Summary Table

| Dimension | cc10x | Superpowers | Matt Pocock |
| ----------- | ------- | ------------- | ------------- |
| **Planning approach** | Multi-mode contract-first | Spec-to-plan linear pipeline | Design-vocabulary-driven (no plan artifact) |
| **Architecture decisions** | Inline ADRs + dedicated architecture skill + decision_rfc mode | Embedded in spec, no ADR format | Minimal ADR + deep-module methodology + Design It Twice |
| **Planning gates** | 5 gates (completeness, review, fresh-review DAG, assumption pass, self-review) | 5 gates (spec self-review, user review, plan self-review, critical review, optional reviewer) | 5 implicit gates (ADR qualification, deletion test, two-adapter rule, prototype disposition, ADR conflict check) |
| **Brainstorming** | Exploration skill (design + spike modes) with scope triage, fast path, 5-dimension interview | Dedicated brainstorming skill with HARD-GATE, visual companion, 9-step checklist | No dedicated brainstorming — distributed across architecture skills (Design It Twice, prototype, domain modeling) |
| **Rating** | 8.5/10 | 7/10 | 7.5/10 |

### Key Takeaway

**cc10x is the best at planning *process*** — its tri-mode system, three-layer gate system, machine-readable contracts, and typed contract graph are industry-leading. No other project comes close on planning rigor and orchestration.

**Matt Pocock is the best at planning *content*** — its deep-module vocabulary, deletion test, two-adapter rule, Design It Twice, and dependency-category testing strategy produce better architectural *decisions* than either other project. The vocabulary is so precise that it makes architecture decisions communicable and comparable.

**Superpowers is the best at planning *execution*** — its complete-code-in-steps, no-placeholders rule, and visual companion make plans that are maximally executable by an engineer with zero context. The user review gate and HARD-GATE ensure human alignment.

### Recommended Adoption Priority for cc10x

1. **Adopt deep-module vocabulary** (from Matt Pocock) — Replace generic "component" with "module", "interface" (in the deep-module sense), "seam", "adapter", "depth". This would make cc10x's architecture skill substantially more precise.

2. **Adopt deletion test + two-adapter rule** (from Matt Pocock) — Replace or augment the prefactor question with these more concrete, falsifiable tests.

3. **Adopt CONTEXT.md domain glossary** (from Matt Pocock) — Make the ephemeral glossary from the exploration handoff into a persistent file. This would make domain language durable across sessions.

4. **Adopt Design It Twice** (from Matt Pocock) — Add a parallel-interface-exploration mode to the exploration skill for architecture-heavy work.

5. **Adopt minimal ADR format with qualification gates** (from Matt Pocock) — Add the three-gate ADR qualification (hard to reverse, surprising, real trade-off) to prevent ADR proliferation.

6. **Adopt complete-code-in-steps** (from Superpowers) — For `execution_plan` mode, require complete code in every step rather than just contracts.

7. **Adopt no-placeholders catalog** (from Superpowers) — Expand the "no placeholders/TBD" check with Superpowers' explicit list of forbidden patterns.

8. **Adopt user review gate on design** (from Superpowers) — Add an explicit "user must review the design document" step between exploration and planning.

9. **Adopt visual companion** (from Superpowers) — For UI-heavy brainstorming in the exploration skill's design mode.

10. **Adopt dependency-category testing strategy** (from Matt Pocock) — Bridge cc10x's dependency classification (Owned/Wrapped/Consumed/Infra) to testing strategy using Matt Pocock's four categories.