# Comparison #15: Karpathy-Inspired Guidelines vs cc10x

## Source: multica-ai/andrej-karpathy-skills

**Repo:** A single `CLAUDE.md` file with four behavioral principles derived from Andrej Karpathy's observations on LLM coding pitfalls. Distributed as a Claude Code plugin, Cursor rule, and standalone CLAUDE.md.

**Files read (all):** README.md, CLAUDE.md, CURSOR.md, EXAMPLES.md, README.zh.md, skills/karpathy-guidelines/SKILL.md

---

## 1. The Four Principles

| # | Principle | Core Directive |
| --- | ----------- | ---------------- |
| 1 | **Think Before Coding** | Don't assume. Don't hide confusion. Surface tradeoffs. State assumptions explicitly, present multiple interpretations, push back when warranted, stop when confused. |
| 2 | **Simplicity First** | Minimum code that solves the problem. No speculative features, no abstractions for single-use code, no unrequested flexibility, no error handling for impossible scenarios. |
| 3 | **Surgical Changes** | Touch only what you must. Clean up only your own mess. Don't "improve" adjacent code. Match existing style. Mention dead code — don't delete it. Every changed line traces to the user's request. |
| 4 | **Goal-Driven Execution** | Define success criteria. Loop until verified. Transform imperative tasks into verifiable goals. Write a test that reproduces the bug, then make it pass. State plans with per-step verification. |

## 2. How Each Principle Addresses a Karpathy Observation

### Karpathy's Three Observations (from his X post)

> **(A)** "The models make wrong assumptions on your behalf and just run along with them without checking. They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."

> **(B)** "They really like to overcomplicate code and APIs, bloat abstractions, don't clean up dead code... implement a bloated construction over 1000 lines when 100 would do."

> **(C)** "They still sometimes change/remove comments and code they don't sufficiently understand as side effects, even if orthogonal to the task."

> **(D)** "LLMs are exceptionally good at looping until they meet specific goals... Don't tell it what to do, give it success criteria and watch it go."

### Mapping

| Principle | Karpathy Observation | Mechanism |
| ----------- | --------------------- | ----------- |
| Think Before Coding | (A) wrong assumptions, hidden confusion, missing tradeoffs | Forces explicit assumption-stating, multiple-interpretation presentation, and push-back before implementation begins |
| Simplicity First | (B) overcomplication, bloated abstractions | Prohibits speculative features, single-use abstractions, unrequested configurability. The "senior engineer test" heuristic. |
| Surgical Changes | (C) orthogonal edits, touching code you shouldn't | "Every changed line should trace directly to the user's request." Orphan cleanup scoped to only YOUR changes. Don't delete pre-existing dead code. |
| Goal-Driven Execution | (D) LLMs are good at looping toward goals | Transform "fix the bug" into "write a test that reproduces it, then make it pass." Per-step verification plans. Strong success criteria enable autonomous looping. |

## 3. Unique Patterns Used to Enforce the Principles

### 3.1 The "Confusion Management" Concept (Think Before Coding)

The guideline explicitly names "confusion" as something to manage:

- "If something is unclear, stop. Name what's confusing. Ask."
- "Don't hide confusion."
- "State your assumptions explicitly. If uncertain, ask."

This is a behavioral directive aimed at the LLM's tendency to silently resolve ambiguity. It frames confusion as a first-class signal that requires action (stop + name + ask), not a feeling to push through.

### 3.2 The "Senior Engineer Test" Heuristic (Simplicity First)

> Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

A self-check heuristic — not a gate, not a contract field, but a cognitive nudge. It's a lightweight test that works by analogy rather than formal criteria.

### 3.3 The "Orphan Cleanup" Distinction (Surgical Changes)

A precise two-tier rule:

- **Remove** imports/variables/functions that YOUR changes made unused (your mess)
- **Don't remove** pre-existing dead code unless asked (not your mess)

This is a nuanced distinction that addresses a specific LLM failure mode: the model sees dead code and "helpfully" deletes it, polluting the diff with unrelated changes.

### 3.4 The "Mention, Don't Delete" Rule (Surgical Changes)

> If you notice unrelated dead code, mention it — don't delete it.

This is a communication pattern: surface observations as notes, not as actions. It separates awareness from intervention.

### 3.5 The Imperative → Declarative Transformation Table (Goal-Driven Execution)

| Instead of... | Transform to... |
| -------------- | ----------------- |
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

A concrete pattern for converting vague instructions into verifiable goals with test-first methodology.

### 3.6 The Per-Step Verification Plan Format

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

A structured plan format that pairs every action with its verification check. This is lighter than a full BDD scenario but heavier than a plain checklist.

### 3.7 The EXAMPLES.md Anti-Pattern Catalog

The repo includes a detailed catalog of anti-patterns with ❌/✅ code examples for each principle:

- Hidden assumptions in export functions
- Over-abstraction (strategy pattern for a single discount calculation)
- Speculative features (cache+validation+notify for a simple save)
- Drive-by refactoring (reformatting code while fixing a bug)
- Style drift (changing quotes, adding type hints while adding logging)
- Vague vs. verifiable task framing
- Test-first bug reproduction

This is a training artifact — it teaches by showing the wrong way and the right way side by side.

### 3.8 The "Working Signals" Feedback Loop

The README includes a self-assessment section:
> These guidelines are working if you see:
>
> - Fewer unnecessary changes in diffs
> - Fewer rewrites due to overcomplication
> - Clarifying questions come before implementation
> - Clean, minimal PRs

This is an observability layer for the guidelines — success metrics for behavioral change.

## 4. Comparison to cc10x's Agent-Common Preamble

### 4.1 Structural Comparison

| Dimension | Karpathy Guidelines | cc10x agent-common |
| ----------- | -------------------- | -------------------- |
| **Format** | Human-readable CLAUDE.md, 4 numbered principles | Machine-readable preamble with memory protocol, contract envelope, output rules |
| **Enforcement** | Advisory — relies on the LLM reading and internalizing | Structural — contract fields, hooks, gates, fail-closed validation |
| **Scope** | Single agent (Claude Code session) | Multi-agent orchestration (router → builder → reviewer → verifier) |
| **Memory** | None | First-class: activeContext.md, patterns.md, progress.md |
| **Verification** | "Loop until verified" as a principle | TDD RED/GREEN/REFACTOR + scenario evidence + convergence state |
| **Assumption management** | "State assumptions explicitly" | Builder `ASSUMPTIONS` contract field + planner hidden-assumption pass |
| **Surgical changes** | "Every changed line traces to user's request" | Builder deviation discipline + decision checkpoints + reviewer SPEC_COMPLIANCE EXTRA bucket |
| **Simplicity** | "No speculative features" | Building skill: "No extra features, no abstractions for hypothetical futures" + reviewer SPEC_COMPLIANCE |
| **Confusion** | "Stop. Name what's confusing. Ask." | Builder pre-flight check + planner NEEDS_CLARIFICATION |

### 4.2 Principle-by-Principle Coverage

#### Principle 1: Think Before Coding

| Karpathy Pattern | cc10x Equivalent | cc10x Stronger? |
| ----------------- | ----------------- | ----------------- |
| State assumptions explicitly | Builder `ASSUMPTIONS` contract field, planner hidden-assumption pass (classify as `proven_by_code`/`inferred`/`needs_user_confirmation`) | ✅ Yes — machine-validated, not just advisory |
| Present multiple interpretations | Planner: "Multiple valid interpretations with material impact → STATUS=NEEDS_CLARIFICATION" | ✅ Yes — blocks execution, not just suggests |
| Push back when warranted | Code-review skill: "Push back on rejected items — with evidence, not opinion"; plan-gap-reviewer adversarial framing | ✅ Yes — structured push-back with evidence requirements |
| Stop when confused | Builder pre-flight: "If unsafe without clarification: STATUS=FAIL"; planner NEEDS_CLARIFICATION; Intent Readiness Gate contradiction-free check | ✅ Yes — fail-closed, not optional |

#### Principle 2: Simplicity First

| Karpathy Pattern | cc10x Equivalent | cc10x Stronger? |
| ----------------- | ----------------- | ----------------- |
| No features beyond what was asked | Reviewer SPEC_COMPLIANCE: EXTRA bucket ("something built that was not requested — over-engineering / scope creep / speculative nice to have") | ✅ Yes — gates to CHANGES_REQUESTED, independent of code quality |
| No abstractions for single-use code | Building skill: "No extra features, no abstractions for hypothetical futures" | ≈ Equal — advisory in building skill, enforced by reviewer |
| No unrequested flexibility/configurability | Plan-review-gate: "No scope creep — extra abstractions, refactoring, or features beyond the request" | ✅ Yes — blocking gate |
| If 200 lines could be 50, rewrite | (No direct equivalent) | ❌ Missing — no line-count self-check |
| Senior engineer test heuristic | (No direct equivalent) | ❌ Missing — no self-check heuristic |

#### Principle 3: Surgical Changes

| Karpathy Pattern | cc10x Equivalent | cc10x Stronger? |
| ----------------- | ----------------- | ----------------- |
| Don't "improve" adjacent code | Builder deviation discipline: "Only absorb work directly caused by the current phase's changes" | ✅ Yes — with decision checkpoints for >3 files |
| Don't refactor things that aren't broken | Builder: "Surface and stop: broader refactors, unrelated warnings, later-phase work" | ✅ Yes — structured FAIL with reason |
| Match existing style | Building skill: "Study Project Patterns First — read 2-3 existing similar components, match naming, file structure, export style, test patterns" | ✅ Yes — with LSP verification |
| Mention dead code, don't delete | (No direct equivalent — no "mention don't delete" rule) | ❌ Missing — cc10x has no "mention, don't delete" pattern |
| Remove YOUR orphans only | (No direct equivalent — no orphan-scoped cleanup rule) | ❌ Missing — no explicit two-tier orphan rule |
| Every changed line traces to request | Reviewer SPEC_COMPLIANCE gates on EXTRA findings; builder deviation discipline | ✅ Yes — enforced by reviewer, not just self-discipline |

#### Principle 4: Goal-Driven Execution

| Karpathy Pattern | cc10x Equivalent | cc10x Stronger? |
| ----------------- | ----------------- | ----------------- |
| Transform imperative to verifiable goals | TDD RED/GREEN/REFACTOR cycle + scenario evidence (given/when/then/command/expected/actual/exit_code) | ✅ Significantly stronger — machine-verified with exit codes |
| Write test that reproduces bug, then fix | Bug-investigator: TDD_RED_EXIT + TDD_GREEN_EXIT + VARIANTS_COVERED + regression evidence | ✅ Yes — contract-enforced, not advisory |
| Per-step verification plan format | Planner phase contracts with `exit_criteria`, `required_checks`, `checkpoint_type` | ✅ Yes — structured and machine-readable |
| Loop until verified | Router chain execution loop + convergence state (`needs_iteration` → `converged`) + 3-cycle remediation cap | ✅ Yes — bounded loop with circuit breaker |
| Strong criteria enable autonomous looping | JUST_GO mode + autonomous mode (loop without checkpointing for reversible actions) | ✅ Yes — with safety guardrails |

## 5. What Could cc10x Adopt?

### 5.1 Verdict: Minimal Adoption Needed

cc10x already covers all four Karpathy principles with **stronger, machine-enforced mechanisms**. The Karpathy guidelines are a lightweight advisory layer; cc10x is a structural enforcement system. However, there are **three micro-patterns** worth considering:

### 5.2 Pattern A: "Mention, Don't Delete" for Dead Code (LOW VALUE)

**What:** When the builder encounters unrelated dead code during a phase, it should note it in `DEFERRED` memory notes rather than deleting it.

**cc10x gap:** cc10x's builder deviation discipline says "surface and stop" for broader refactors, and the memory protocol has `Deferred` items. But there's no explicit rule saying "mention dead code you notice, don't delete it."

**Assessment:** cc10x's deviation discipline + SPEC_COMPLIANCE EXTRA bucket already catches unauthorized deletions at review time. The "mention don't delete" rule is a nice-to-have but the enforcement gap is small — the reviewer would flag a dead-code deletion as scope creep anyway. The `DEFERRED` memory notes pattern already exists for non-blocking discoveries.

**Recommendation:** **Skip.** cc10x's reviewer SPEC_COMPLIANCE + deviation discipline already covers this. Adding a "mention don't delete" rule would be redundant with the existing "surface and stop" directive.

### 5.3 Pattern B: The "Senior Engineer Test" Self-Check Heuristic (NOVEL BUT LOW IMPACT)

**What:** A cognitive nudge: "Would a senior engineer say this is overcomplicated? If yes, simplify."

**cc10x gap:** cc10x has no self-check heuristic. It relies on the reviewer's SPEC_COMPLIANCE EXTRA bucket to catch over-engineering after the fact.

**Assessment:** This is a preventive (builder-side) heuristic vs. cc10x's detective (reviewer-side) enforcement. The heuristic is lightweight and could reduce the number of remediation cycles by catching over-engineering before the reviewer sees it. However, cc10x's building skill already says "No extra features, no abstractions for hypothetical futures" and "Write minimal diffs" — the senior engineer test is just a memorable framing of the same idea.

**Recommendation:** **Skip.** The building skill already has equivalent directives. The "senior engineer test" is a communication framing, not a new enforcement mechanism. cc10x's formal SPEC_COMPLIANCE check is stronger.

### 5.4 Pattern C: The "Confusion Management" Behavioral Framing (NOVEL CONCEPT, ALREADY COVERED STRUCTURALLY)

**What:** Explicitly naming "confusion" as a first-class signal. "Don't hide confusion. Name what's confusing. Ask."

**cc10x gap:** cc10x handles confusion structurally — builder pre-flight check returns FAIL when unsafe, planner returns NEEDS_CLARIFICATION, Intent Readiness Gate checks for contradictions. But cc10x never uses the word "confusion" or frames it as a thing to "manage."

**Assessment:** This is a framing difference, not a functional gap. cc10x's `STATUS=FAIL` + `REMEDIATION_REASON: "Builder blocked on missing requirement: {question}"` IS confusion management — it just calls it "blocked on missing requirement." The Karpathy framing is more human-readable and might improve LLM compliance through clearer language, but cc10x's structural enforcement is already stronger.

**Recommendation:** **Skip.** cc10x's structural confusion management (pre-flight check, NEEDS_CLARIFICATION, Intent Readiness Gate) is already stronger than the advisory framing. The word "confusion" is a communication choice, not a functional gap.

### 5.5 Pattern D: The EXAMPLES.md Anti-Pattern Catalog (TRAINING ARTIFACT, NOT ENFORCEMENT)

**What:** A catalog of ❌/✅ code examples showing common LLM mistakes and correct alternatives.

**cc10x gap:** cc10x has no equivalent training catalog. Its skills are procedural instructions, not example-driven teaching.

**Assessment:** This is a documentation/training artifact, not an enforcement mechanism. It would be valuable as a reference document for cc10x users to understand WHY the rules exist, but it wouldn't change runtime behavior. cc10x's skills already encode the rules the examples illustrate.

**Recommendation:** **Skip for runtime. Consider as documentation.** The anti-pattern catalog could be useful as `docs/anti-pattern-catalog.md` for onboarding and understanding, but it's not something to add to the agent skill chain.

### 5.6 Pattern E: The "Working Signals" Feedback Loop (OBSERVABILITY, ALREADY EXISTS)

**What:** Success metrics for the guidelines: "fewer unnecessary changes in diffs, fewer rewrites, clarifying questions before implementation."

**cc10x gap:** cc10x has telemetry (latency, loop counters, verifier workload) but no behavioral quality metrics like "unnecessary changes in diffs."

**Assessment:** cc10x's telemetry is runtime-focused (performance), not behavior-focused (quality of changes). The "working signals" concept is interesting but would require a diff-analysis tool to measure automatically. cc10x's SPEC_COMPLIANCE EXTRA bucket already catches unnecessary changes per-workflow.

**Recommendation:** **Skip.** cc10x's per-workflow SPEC_COMPLIANCE review already catches the same issues the "working signals" describe, but per-build rather than as a trend metric.

## 6. Is "Confusion Management" Unique?

**Concept uniqueness:** The explicit framing of "confusion" as a managed state is unique to the Karpathy guidelines. No other repo studied uses this exact framing.

**Functional uniqueness:** **No.** cc10x has comprehensive confusion management, just under different names:

| Karpathy "Confusion Management" | cc10x Equivalent |
| ------------------------------- | ----------------- |
| "State assumptions explicitly" | Builder `ASSUMPTIONS` contract field (machine-parsed) |
| "If uncertain, ask" | Planner `STATUS=NEEDS_CLARIFICATION` (blocks execution) |
| "Present multiple interpretations" | Planner: "Multiple valid interpretations with material impact → NEEDS_CLARIFICATION" |
| "Stop when confused" | Builder pre-flight: `STATUS=FAIL`, `PHASE_STATUS=blocked` |
| "Name what's confusing" | `REMEDIATION_REASON: "Builder blocked on missing requirement: {question}"` |
| "Surface inconsistencies" | Intent Readiness Gate: contradiction-free check; plan-gap-reviewer: `hidden_assumptions` |

cc10x's confusion management is **structural and fail-closed** — it blocks the workflow when confusion is detected. The Karpathy guidelines are **advisory** — they tell the LLM to stop but can't enforce it. cc10x is strictly stronger.

## 7. Is "Surgical Changes" Unique? Comparison to cc10x's Scope Guard

### Karpathy's "Surgical Changes"

A behavioral directive with five sub-rules:

1. Don't "improve" adjacent code, comments, or formatting
2. Don't refactor things that aren't broken
3. Match existing style, even if you'd do it differently
4. If you notice unrelated dead code, mention it — don't delete it
5. Remove only YOUR orphans; don't remove pre-existing dead code

**The test:** "Every changed line should trace directly to the user's request."

### cc10x's "Scope Guard" and Related Mechanisms

cc10x has **multiple surgical-changes mechanisms** operating at different points in the workflow:

| Mechanism | Where | How It Works |
| ----------- | ------- | ------------- |
| **Builder Deviation Discipline** | component-builder.md | "Only absorb work directly caused by the current phase's changes or required to satisfy its exit criteria. Fix inline: direct breakage, missing glue, test/build failures. Surface and stop: broader refactors, unrelated warnings, later-phase work, unapproved architecture choices." |
| **Decision Checkpoints** | component-builder.md | Changing >3 files not in plan → FAIL; Choosing between 2+ valid patterns → FAIL; Breaking existing API contract → FAIL; Adding dependency not in plan → FAIL; Touching a later planned phase early → FAIL |
| **Reviewer SPEC_COMPLIANCE EXTRA** | code-reviewer.md | "EXTRA — something built that was not requested (over-engineering / scope creep / speculative nice to have). This is a real finding, NOT a courtesy: YAGNI violations are flagged, not waved through." Gates to CHANGES_REQUESTED. |
| **Plan Review Gate Scope Check** | plan-review-gate/SKILL.md | "No scope creep — extra abstractions, refactoring, or features beyond the request" + "Complexity proportional — solution is over-engineered for the problem" |
| **Building Skill Minimal Diffs** | building/SKILL.md | "Write minimal diffs. A bug fix doesn't need surrounding cleanup. A one-shot operation doesn't need a helper. Don't add error handling, fallbacks, or validation for scenarios that cannot happen." |
| **Reviewer Scope Guard** | code-reviewer.md | "If you have read >10 files without writing any finding, produce a preliminary verdict based on what you have. Review scope should be proportional to change size." |
| **Clean-Baseline Diff** | router inline fallback | "Record the baseline before the build phase, and at verification diff the working tree against it so the verifier checks only this workflow's changes." |

### Comparison

| Dimension | Karpathy Surgical Changes | cc10x Surgical Changes |
| ----------- | -------------------------- | ---------------------- |
| **Enforcement** | Advisory (LLM self-discipline) | Structural (contract fields, gates, reviewer enforcement) |
| **Coverage** | 5 sub-rules | 7+ mechanisms across builder, reviewer, plan gate, and building skill |
| **"Mention don't delete" dead code** | ✅ Explicit rule | ❌ No explicit rule (but reviewer catches deletions as scope creep) |
| **Orphan cleanup scoping** | ✅ Two-tier: your orphans vs pre-existing | ❌ No explicit two-tier rule |
| **Style matching** | "Match existing style, even if you'd do it differently" | "Study Project Patterns First — read 2-3 existing similar components, match naming, file structure, export style, test patterns" + LSP verification |
| **"Every line traces to request"** | Stated as a test | Enforced via SPEC_COMPLIANCE EXTRA bucket (gates to CHANGES_REQUESTED) |
| **Scope escalation detection** | Not addressed | Builder `SCOPE_INCREASES` contract field + decision checkpoints for >3 files |
| **Baseline diff tracking** | Not addressed | Clean-baseline diff in inline fallback mode |

### Verdict

cc10x's surgical changes enforcement is **strictly stronger and more comprehensive** than the Karpathy guidelines. The two micro-gaps are:

1. **"Mention, don't delete" dead code rule** — cc10x's deviation discipline says "surface and stop" for unrelated work, which implies not deleting dead code, but it's not as explicit as the Karpathy rule. However, the reviewer's SPEC_COMPLIANCE EXTRA bucket would catch an unauthorized dead-code deletion as scope creep.

2. **Two-tier orphan cleanup** — cc10x has no explicit rule distinguishing "your orphans" from "pre-existing dead code." The building skill says "Write minimal diffs" and the deviation discipline says "only absorb work directly caused by the current phase's changes," which implies the same thing, but the Karpathy rule is more precise.

**These gaps are cosmetic, not functional.** cc10x's enforcement mechanisms (reviewer SPEC_COMPLIANCE, deviation discipline, decision checkpoints) catch the same failure modes the Karpathy rules address, just through different paths.

## 8. Summary: Unique Patterns cc10x Should Adopt

### Final Assessment

| Pattern | Karpathy Novel? | cc10x Has It? | Adopt? | Priority |
| --------- | ---------------- | -------------- | -------- | ---------- |
| Confusion management framing | Yes (framing) | Yes (structural, different name) | No | — |
| Surgical changes | No (common concept) | Yes (7+ mechanisms) | No | — |
| "Mention, don't delete" dead code | Yes (explicit rule) | Partially (implied by deviation discipline) | No | — |
| Two-tier orphan cleanup | Yes (explicit distinction) | Partially (implied by minimal diffs) | No | — |
| Senior engineer test heuristic | Yes (self-check framing) | No (but building skill covers the same idea) | No | — |
| Imperative → declarative transformation table | Yes (teaching pattern) | Yes (TDD cycle is stronger) | No | — |
| Per-step verification plan format | Yes (lightweight format) | Yes (phase contracts are stronger) | No | — |
| EXAMPLES.md anti-pattern catalog | Yes (training artifact) | No | Maybe as docs | LOW |
| "Working signals" feedback loop | Yes (observability concept) | Partially (telemetry is runtime, not behavioral) | No | — |

### Bottom Line

**cc10x should adopt nothing from this repo.** Every Karpathy principle is already covered by a stronger, machine-enforced cc10x mechanism. The Karpathy guidelines are an elegant, minimal advisory layer — exactly what a single-agent CLAUDE.md should be. But cc10x is a multi-agent orchestration system with structural enforcement, and the advisory patterns in the Karpathy guidelines are subsets of what cc10x already enforces.

The one thing that would be genuinely useful but isn't worth the maintenance cost: an anti-pattern catalog (`docs/anti-pattern-catalog.md`) showing ❌/✅ examples for onboarding. This is a documentation artifact, not a runtime mechanism, and could be created independently of this analysis.

### Comparison to Other Repos in This Series

The Karpathy guidelines are the **most philosophically aligned** repo studied — they describe exactly the problems cc10x was built to solve, but at the advisory level. Where other repos offer novel enforcement mechanisms (hooks, parallel review, subagent dispatch), the Karpathy repo offers novel framing of the same problems cc10x already addresses. This makes it a validation of cc10x's design philosophy rather than a source of new patterns.
