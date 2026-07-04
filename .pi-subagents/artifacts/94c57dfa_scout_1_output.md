# Skill Design & Format Methodology: Deep Comparison

> **Projects compared:** cc10x (17 skills) · Superpowers (14 skills) · Matt Pocock (15 engineering skills)
> **Date:** 2025-07
> **Scope:** Frontmatter format, body structure, skill-writing pedagogy, discoverability, reference files, unique patterns, and behavioral steering effectiveness.

---

## 1. Skill Frontmatter Format Comparison

### cc10x

| Field | Usage | Notes |
| --- | --- | --- |
| `name` | All 17 skills | Single word or hyphenated |
| `description` | All 17 | Multi-line YAML block scalar (`\|` or `>-`). Describes what the skill covers + loaded-by agent. Some include trigger keywords (router, update). |
| `allowed-tools` | 15/17 | Restrictive tool allowlist per skill. E.g., `verification` allows `Read Bash Grep Glob` only. `agent-common` and `update` omit it. |
| `user-invocable` | 14/17 | Set to `false` for internal skills. Only `update` and `diff-driven-docs` appear user-facing. |
| `disable-model-invocation` | 1/17 | Only `agent-common` uses this — a shared preamble not intended for autonomous invocation. |

**Pattern:** cc10x frontmatter is **operational**: it encodes who loads the skill, what tools are available, and whether the user can invoke it directly. The description doubles as an activation description ("Loaded by planner agent") and, for the router, an exhaustive trigger-keyword list.

### Superpowers

| Field | Usage | Notes |
| --- | --- | --- |
| `name` | All skills | Hyphenated, verb-first or gerund form |
| `description` | All skills | Single-line, always starts with "Use when…" — trigger-focused, third person. Max 1024 chars per Anthropic spec. |

**Pattern:** Superpowers frontmatter is **minimal and discoverability-obsessed**. Two fields only. The description is purely a trigger — it never summarizes the workflow. This is an explicit design rule documented in their writing-skills skill: "Description = When to Use, NOT What the Skill Does."

### Matt Pocock

| Field | Usage | Notes |
| --- | --- | --- |
| `name` | All skills | Hyphenated |
| `description` | All skills | Starts with "Use when…" or a topic sentence + trigger conditions. Third person. |
| `disable-model-invocation` | ~40% of skills | Used for skills that should only fire when the user explicitly types the name (`implement`, `writing-great-skills`, `teach`). |
| `argument-hint` | Some skills | e.g., `teach` has `argument-hint: "What would you like to learn about?"` |

**Pattern:** Matt Pocock frontmatter is **invocation-strategic**. The `disable-model-invocation` flag is the key lever: it deliberately trades agent self-discovery for zero context-load when a skill should only fire by explicit user command. This is a first-class concept in their writing-great-skills glossary (model-invoked vs. user-invoked).

### Verdict on Frontmatter

| Dimension | cc10x | Superpowers | Matt Pocock |
| --- | --- | --- | --- |
| Fields used | 4-5 | 2 | 2-4 |
| Tool restriction | ✅ `allowed-tools` | ❌ | ❌ |
| Invocation control | `user-invocable: false` | (not used) | `disable-model-invocation: true` |
| Description philosophy | Operational (what it covers + who loads it) | Trigger-only ("Use when…") | Trigger + invocation axis |
| Agent autonomy | Router-controlled (SKILL_HINTS) | Agent self-discovers | Per-skill toggle |

**Key insight:** cc10x treats frontmatter as an **orchestration contract** (who loads this, what tools it gets). Superpowers treats it as a **discovery beacon** (when should the agent find this). Matt Pocock treats it as an **invocation decision** (should the agent fire this or only the human?).

---

## 2. Skill Body Structure (Sections, Formatting, Length)

### Length Distribution

| Project | Median lines | Min | Max | Total |
| --- | --- | --- | --- | --- |
| cc10x (excl. router) | 113 | 63 | 176 | 1,914 |
| cc10x (with router) | 113 | 63 | 751 | 2,665 |
| Superpowers | 174 | 62 | 689 | 3,322 |
| Matt Pocock (eng) | 75 | 7 | 134 | 1,050 |

cc10x skills are **medium-length and dense**. Superpowers skills are **longer and pedagogically exhaustive**. Matt Pocock skills are **short and high-leverage** — the `implement` skill is 15 lines.

### Section Patterns

**cc10x canonical structure:**

```
# [Skill Name]
[1-sentence thesis / iron law]
## Reference Files (if any)
## [Core methodology sections]
[Tables, templates, gates]
## [Failure modes / anti-patterns]
```

- Heavy use of **tables** (decision matrices, severity, validation levels)
- **Templates** in fenced blocks (plan headers, evidence arrays, ADRs)
- **Gates** as explicit checklists ("Plan Completeness Gate — MANDATORY")
- Minimal prose, maximal structure
- `<!-- scar: date -->` comments documenting failure origins

**Superpowers canonical structure:**

```
# [Skill Name]
## Overview (core principle in 1-2 sentences)
## When to Use (symptoms + exceptions)
## The Iron Law (code block with absolute rule)
## [Core process — often with graphviz flowchart]
## Good/Bad code examples (in <Good>/<Bad> tags)
## Common Rationalizations (table)
## Red Flags - STOP and Start Over
## Verification Checklist
```

- **Rationalization tables** are a signature pattern — every discipline skill has one
- **Red Flags lists** as terminal self-checks
- **Graphviz dot diagrams** for decision flowcharts
- `<Good>` / `<Bad>` code comparison blocks
- Heavy first-person imperative ("YOU MUST", "Never", "Always")
- "Violating the letter is violating the spirit" as a foundational principle

**Matt Pocock canonical structure:**

```
# [Skill Name]
[1-2 sentence positioning paragraph]
## [Phase N — Name]
[Completion criteria as checkboxes]
## [Phase N+1 — Name]
...
```

- **Phase-structured** with explicit completion criteria
- **Checkbox gates** at phase boundaries (`- [ ] Red-capable`, `- [ ] Deterministic`)
- Minimal anti-pattern coverage — trusts the agent's intelligence
- Leading words defined inline (e.g., "tight", "seam", "tracer bullet")
- No rationalization tables, no red-flags lists
- Context.md / ADR awareness as a cross-cutting concern

### Formatting Comparison

| Element | cc10x | Superpowers | Matt Pocock |
| --- | --- | --- | --- |
| Tables | Very frequent (decision matrices) | Moderate (rationalizations, quick-ref) | Rare |
| Code blocks | Templates, evidence formats | Good/Bad comparisons | Minimal |
| Flowcharts | None | Graphviz dot diagrams | None |
| Checkboxes | Gates (Plan Completeness) | Verification checklists | Completion criteria |
| Rationalization tables | None | Signature pattern | None |
| Red Flags lists | None | Signature pattern | None |
| `<!-- scar -->` comments | Yes (failure origin) | No | No |
| Iron Law blocks | Building, Debugging | TDD, Debugging, Verification | No |
| Leading words vocabulary table | Building | No (but uses leading words) | No |

---

## 3. How Each Project Teaches Skill Writing

### Superpowers: `writing-skills` (689 lines — the most pedagogically complete)

**Core thesis:** Skill creation IS TDD applied to process documentation.

**Methodology:**

1. **RED:** Run pressure scenarios with subagents WITHOUT the skill. Document exact rationalizations verbatim.
2. **GREEN:** Write minimal skill addressing those specific failures. Re-test.
3. **REFACTOR:** Close loopholes. Find new rationalizations. Add counters. Re-test until bulletproof.

**Key concepts taught:**

- Skill Discovery Optimization (SDO): description = triggers only, keyword coverage, descriptive naming
- Token efficiency targets (<150 words for frequently-loaded, <500 for others)
- Match the Form to the Failure: prohibition vs. recipe vs. structural vs. conditional
- Bulletproofing against rationalization (close every loophole, address spirit-vs-letter)
- Micro-testing wording before full scenarios (5+ reps, no-guidance control)
- Persuasion principles (Cialdini): authority, commitment, scarcity, social proof, unity
- Testing all skill types (discipline, technique, pattern, reference)
- Progressive disclosure and file organization

**Supporting files:**

- `anthropic-best-practices.md` — Anthropic's official skill authoring guide (embedded as reference)
- `persuasion-principles.md` — research foundation for why imperative language works
- `testing-skills-with-subagents.md` — complete testing methodology with worked examples
- `examples/CLAUDE_MD_TESTING.md` — full test campaign for CLAUDE.md documentation variants

### Matt Pocock: `writing-great-skills` (83 lines + 1 GLOSSARY.md)

**Core thesis:** A skill exists to wrangle determinism out of a stochastic system. Predictability is the root virtue.

**Methodology:** No TDD-for-skills. Instead, a **vocabulary-driven design philosophy**:

**Key concepts taught (via GLOSSARY.md, ~180 lines):**

- **Predictability** — same process every run, not same output
- **Model-invoked vs. user-invoked** — the invocation axis (context load vs. cognitive load)
- **Information hierarchy** — steps (in-file) → reference (in-file) → external reference (behind pointer)
- **Leading words** — compact pretrained concepts that anchor behavior (Leitwort)
- **Completion criterion** — checkable + exhaustive; prevents premature completion
- **Progressive disclosure** — push reference behind context pointers
- **Branching** — different paths through a skill; drives disclosure decisions
- **Failure modes** — premature completion, duplication, sediment, sprawl, no-op
- **Pruning** — single source of truth, relevance, no-op test

**Teaching style:** Dense, conceptual, glossary-driven. The skill itself is "all reference" (no steps) — it practices what it preaches about information hierarchy.

### cc10x: Implicit (no dedicated skill-writing skill)

cc10x does NOT have a `writing-skills` equivalent. Skill design principles are **encoded in the skills themselves** rather than taught meta-level. Observations:

- The `building` skill has a "Leading Words" vocabulary table — a cc10x-specific innovation
- The `agent-common` skill defines the CONTRACT envelope and memory protocol
- The router skill is a master class in orchestration but not a skill-writing guide
- No rationalization tables, no red-flags lists, no testing methodology for skills
- No documented skill authoring process

### Verdict on Pedagogy

| Dimension | cc10x | Superpowers | Matt Pocock |
| --- | --- | --- | --- |
| Has dedicated skill-writing skill | ❌ | ✅ (689 lines) | ✅ (83 lines + glossary) |
| Testing methodology for skills | ❌ | ✅ (TDD for skills) | ❌ |
| Theoretical framework | Implicit | TDD + persuasion research | Predictability + information hierarchy |
| Vocabulary system | Leading words table (building) | SDO, bulletproofing | Leading words, completion criteria, failure modes |
| Supporting reference files | 0 (for skill writing) | 4 files | 1 glossary |
| Practical actionability | Low (no guide) | Very high (step-by-step) | Medium (conceptual) |

---

## 4. Leading Words / Activation Patterns — Discoverability

### cc10x

**Leading words:** The `building` skill has an explicit vocabulary table mapping compact words to behavioral concepts:

| Word | Means |
| --- | --- |
| red | Failing test (behavioral, not error) |
| green | Passing test after minimal code |
| tight | Fast, deterministic, sub-second feedback loop |
| deep | Module with small interface, lots hidden inside |
| shallow | Module with interface as complex as implementation |
| seam | Place where a test can attach to exercise real behavior |

These words appear throughout cc10x skills (debugging uses "red-capable", "tight loop"; architecture uses "deep/shallow modules"). This is a **distributed vocabulary** that creates shared language across skills.

**Activation:** Router-controlled. The `cc10x-router` skill has an exhaustive trigger-keyword list in its description: "build, implement, create, write, add, review, audit, debug, fix, error, bug, broken, plan, design, architect, spec, brainstorm, test, refactor, optimize, update, change, research." Agents don't self-discover skills — the router detects intent and passes `SKILL_HINTS` to the dispatched agent. This is a **centralized activation model**.

### Superpowers

**Leading words:** Used implicitly throughout — "root cause", "tight loop", "tracer bullets", "fog of war" appear in skills. The writing-skills skill explicitly teaches the concept but doesn't formalize a vocabulary table.

**Activation:** Agent self-discovery via description. The `using-superpowers` skill is the activation engine:

- "If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST invoke the skill"
- Red flags table for rationalizing skipping skill checks
- Skills are found by searching descriptions with grep
- Priority: process skills first, then implementation skills

This is a **decentralized, agent-driven activation model**. The agent is responsible for checking the skills directory before any task.

### Matt Pocock

**Leading words:** Formalized in the writing-great-skills glossary as "Leitwort" — compact concepts already in the model's pretraining. Used throughout skills: "tight" (loop), "seam", "tracer bullet", "red-capable". The concept is taught but the vocabulary is emergent per-skill.

**Activation:** Two-tier:

- **Model-invoked skills** (description present): agent self-discovers via description triggers
- **User-invoked skills** (`disable-model-invocation: true`): only the human can fire them

The `writing-great-skills` skill explicitly teaches the trade-off: model-invocation costs context load (description always in window) but enables agent autonomy; user-invocation costs cognitive load (human must remember) but saves context.

### Discoverability Verdict

| Dimension | cc10x | Superpowers | Matt Pocock |
| --- | --- | --- | --- |
| Activation model | Centralized (router) | Decentralized (agent self-discovery) | Hybrid (per-skill toggle) |
| Leading words | Explicit vocabulary table | Implicit usage | Taught as concept, emergent per-skill |
| Description philosophy | Operational + trigger keywords | Trigger-only ("Use when…") | Trigger + invocation axis |
| Agent autonomy in skill selection | Low (router decides) | High (agent must check) | Per-skill (model or user) |
| Anti-skip mechanism | Router enforces SKILL_HINTS | Red flags table + "1% chance" rule | None (trusts user/agent) |

---

## 5. Reference Files — Supporting Docs Within Skills

### cc10x

**Pattern:** Heavy use of `references/` subdirectories. Each complex skill has 2-5 reference files.

| Skill | Reference files |
| --- | --- |
| building | testing-patterns.md, test-data-and-mocks.md, integration-and-live-proof.md |
| code-review | review-order-and-checkpoints.md, code-review-heuristics.md, security-review-checklist.md |
| debugging | investigation-hygiene.md, root-cause-playbooks.md |
| frontend | 5 reference files (UI state, accessibility, performance, design-md, inspiration-index) |
| memory-and-handoff | 4 reference files (memory model, operations, file contracts, context budget) |
| cc10x-router | 6 reference files (build/debug/review/plan workflows, artifact policy, remediation) |
| verification | live-production-testing.md |
| planning | live-verification-strategy.md |
| diff-driven-docs | doc-target-heuristics.md |

**Additional:** Three skills have `evals/` directories with evaluation scenarios:

- `cc10x-router/evals/` — 3 evals
- `verification/evals/` — 3 evals
- `diff-driven-docs/evals/` — 2 evals

**Design rule:** Reference files are listed in a `## Reference Files` section at the top of the skill with a one-line reason each. The skill body contains the decision logic; the reference files contain the detailed checklists/playbooks.

### Superpowers

**Pattern:** Minimal reference files. Most skills are self-contained SKILL.md files. The writing-skills skill is the exception with 4 supporting files.

| Skill | Reference files |
| --- | --- |
| writing-skills | anthropic-best-practices.md, persuasion-principles.md, testing-skills-with-subagents.md, examples/CLAUDE_MD_TESTING.md, graphviz-conventions.dot, render-graphs.js |
| systematic-debugging | root-cause-tracing.md, defense-in-depth.md, condition-based-waiting.md (referenced in body) |
| test-driven-development | testing-anti-patterns.md (referenced in body) |

**Design rule:** "Keep inline: principles, code patterns (<50 lines), everything else. Separate files for heavy reference (100+ lines) and reusable tools."

### Matt Pocock

**Pattern:** Moderate use. Some skills have supporting files, others are fully self-contained.

| Skill | Reference files |
| --- | --- |
| writing-great-skills | GLOSSARY.md (180-line domain model) |
| teach | MISSION-FORMAT.md, LEARNING-RECORD-FORMAT.md, RESOURCES-FORMAT.md, GLOSSARY-FORMAT.md |
| tdd | tests.md, mocking.md (referenced in body) |
| diagnosing-bugs | scripts/hitl-loop.template.sh (referenced in body) |

**Design rule (from writing-great-skills):** Progressive disclosure via context pointers. Reference goes behind a pointer when only some branches need it. The GLOSSARY.md is the canonical example — disclosed reference for the skill's domain model.

### Reference File Verdict

| Dimension | cc10x | Superpowers | Matt Pocock |
| --- | --- | --- | --- |
| Reference files per complex skill | 2-6 | 0-4 | 1-4 |
| Evaluation scenarios (evals/) | ✅ (3 skills) | ❌ | ❌ |
| Reference file naming | Descriptive (what it holds) | Descriptive | Format-suffixed (e.g., `-FORMAT.md`) |
| Context pointer discipline | Listed at top with one-line reason | Inline link with context | Inline link, conceptually justified |
| Progressive disclosure | Implicit (router loads on demand) | Explicit (taught in writing-skills) | Explicit (taught as core concept) |

---

## 6. Skill Design Patterns cc10x Has That Others DON'T

1. **`allowed-tools` frontmatter** — cc10x restricts tool access per skill (e.g., verification can only `Read Bash Grep Glob`). Neither Superpowers nor Matt Pocock does this. This is a powerful blast-radius control: a read-only skill literally cannot write files.

2. **Centralized router activation model** — The `cc10x-router` skill is the sole entry point. Agents don't self-discover skills; the router detects intent, selects skills, and passes them as `SKILL_HINTS`. This eliminates the "agent forgot to check for skills" failure mode that Superpowers fights with red-flags tables.

3. **`user-invocable: false` flag** — Most cc10x skills are explicitly non-user-invocable internal skills. This is different from Matt Pocock's `disable-model-invocation: true` (which makes a skill user-ONLY). cc10x's flag makes skills router-ONLY.

4. **CONTRACT envelope** — Every agent output starts with `CONTRACT {"s":"...","b":...,"cr":...}` as a machine-readable signal. This is a structured output protocol that neither other project has.

5. **Workflow artifacts** — cc10x persists orchestration state to `.cc10x/workflows/{uuid}.json` with event logs. Skills are designed to read/write these artifacts. Neither other project has durable workflow state.

6. **Eval scenarios shipped with skills** — cc10x includes `evals/` directories with evaluation scenarios for verification, router, and diff-driven-docs. Superpowers teaches testing methodology but doesn't ship evals with skills.

7. **`<!-- scar -->` comments** — cc10x skills include HTML comments documenting the failure that motivated a specific rule (e.g., `<!-- scar: 2026-06-17 — spike's "move fast, no tests" code promoted to production -->`). This is a unique institutional-memory pattern.

8. **Explicit leading words vocabulary table** — The `building` skill has a formal table mapping compact words ("red", "green", "tight", "deep", "shallow", "seam") to their meanings and what verbose phrasing they replace. Matt Pocock teaches the concept but doesn't formalize it this way.

9. **Anti-anchoring protocol** — Read-only agents (reviewers) deliberately omit memory summaries from their prompts to avoid anchoring on the implementer's narrative. This is a unique adversarial-design pattern.

10. **Model-tier policy** — The router includes a per-role model-tier recommendation table (cheap/standard/capable) for dispatching agents. Neither other project addresses model selection per skill.

11. **Self-remediation and loop caps** — cc10x skills include explicit failure caps ("TDD Failure Cap: GREEN fails 3 consecutive times → FAIL") and self-remediation logic. Superpowers has "3+ fixes = question architecture" but not as a formal cap system.

12. **Two-mode skills** — Several cc10x skills are explicitly two-mode: `code-review` (adversarial + receiving), `frontend` (authoring + critique), `exploration` (design + spike), `codebase-hygiene` (duplicate detection + module deepening), `memory-and-handoff` (session memory + handoff package). The router selects mode via dispatch context. This is a branching pattern neither other project formalizes.

---

## 7. Skill Design Patterns Others Have That cc10x SHOULD Adopt

### From Superpowers

1. **Rationalization tables** — Every discipline skill in Superpowers has a table of common excuses ("Too simple to test" → "Simple code breaks. Test takes 30 seconds.") and a "Red Flags - STOP" list. cc10x skills state rules but don't anticipate the rationalizations agents will use to bypass them. This is a proven anti-bypass technique (Superpowers tested it with subagents).

2. **TDD for skills (test before writing)** — Superpowers requires running pressure scenarios WITHOUT a skill before writing it, documenting exact failures, then writing the skill to address those specific failures. cc10x skills are written from design intent, not from observed failure modes. Adopting this would make cc10x skills more empirically grounded.

3. **"Use when…" description format** — Superpowers descriptions are pure triggers ("Use when implementing any feature or bugfix, before writing implementation code"). cc10x descriptions mix operational info ("Loaded by planner agent") with trigger keywords. The Superpowers format is more effective for agent self-discovery (though cc10x's router model reduces the need).

4. **Spirit-vs-letter foundational principle** — "Violating the letter of the rules is violating the spirit of the rules." This single sentence cuts off an entire class of rationalization. cc10x has strong rules but no equivalent meta-principle.

5. **Micro-testing wording** — Superpowers tests wording with 5+ reps per variant against a no-guidance control before running full pressure scenarios. cc10x has evals but doesn't test wording variants.

6. **Match the Form to the Failure** — Superpowers explicitly classifies failure types (skips rule under pressure vs. wrong-shaped output vs. omitted element) and prescribes different forms (prohibition vs. recipe vs. structural). cc10x uses tables and gates uniformly without this taxonomy.

### From Matt Pocock

1. **`disable-model-invocation: true` as a first-class concept** — Matt Pocock teaches the invocation axis as a design decision: model-invoked (pays context load, gains agent discovery) vs. user-invoked (zero context load, human must remember). cc10x's `user-invocable: false` is the opposite direction but doesn't frame the trade-off explicitly. Adopting this vocabulary would clarify when a skill should be router-loaded vs. user-typed.

2. **Completion criteria as checkboxes** — Matt Pocock's `diagnosing-bugs` has explicit completion criteria at phase boundaries with checkboxes:

   ```
   - [ ] Red-capable — it drives the actual bug code path
   - [ ] Deterministic — same verdict every run
   - [ ] Fast — seconds, not minutes
   - [ ] Agent-runnable
   ```

   cc10x has gates ("Plan Completeness Gate — MANDATORY") but they're prose checklists, not phase-boundary checkboxes with observable criteria. The checkbox format is more scannable and more checkable.

3. **Leading words as a formal concept (Leitwort)** — Matt Pocock's writing-great-skills teaches leading words as a technique: "a compact concept already living in the model's pretraining that the agent thinks with while running the skill." cc10x has a leading words table in `building` but doesn't teach the concept. Formalizing it would help skill authors across cc10x.

4. **Information hierarchy as a design tool** — Matt Pocock teaches a 3-rung ladder (steps → in-skill reference → external reference) for deciding what goes where. cc10x uses reference files extensively but without an explicit decision framework for what stays inline vs. what gets disclosed.

5. **No-op test** — "Does this line change behavior versus the default?" Matt Pocock teaches pruning lines that the model already obeys. cc10x skills are dense but haven't been systematically pruned for no-ops.

6. **`argument-hint` frontmatter** — Matt Pocock's `teach` skill has `argument-hint: "What would you like to learn about?"`. This is a small UX touch that cc10x user-facing skills (like `update`) could benefit from.

7. **Glossary as disclosed reference** — Matt Pocock's `writing-great-skills/GLOSSARY.md` is a 180-line domain model that the skill points to. It defines every bold term used in the skill body. cc10x has reference files but none are structured as a domain-model glossary. A cc10x glossary could define terms like "gate", "blast radius", "scope drift", "evidence array" that recur across skills.

---

## 8. Behavioral Steering Effectiveness — Rating

### Rating Criteria

- **Compliance under pressure:** Does the skill resist rationalization?
- **Output shape control:** Does the skill produce predictable output structure?
- **Discoverability:** Can the agent find and activate the skill when needed?
- **Failure prevention:** Does the skill prevent the specific failures it targets?
- **Token efficiency:** Does the skill earn its context cost?

### Ratings

| Project | Score | Justification |
| --- | --- | --- |
| **Superpowers** | **8/10** | The most empirically tested. Rationalization tables, red-flags lists, and the "1% chance" rule create multiple layers of defense. The TDD-for-skills methodology means every skill was tested against observed failure modes. Spirit-vs-letter principle closes meta-rationalizations. Loses points for: long skills (371 lines for TDD) that may dilute attention; no tool restriction; no structured output protocol; agent self-discovery can fail when the agent rationalizes skipping the skill check. |
| **cc10x** | **7.5/10** | The most operationally sophisticated. Router-controlled activation eliminates the "forgot to check" failure. `allowed-tools` prevents blast radius. CONTRACT envelope ensures machine-readable output. Workflow artifacts enable resume. Two-mode skills are elegant. Reference files keep SKILL.md lean. Eval scenarios show empirical testing. Loses points for: no rationalization tables (agents can bypass rules with excuses that aren't anticipated); no spirit-vs-letter principle; no formal skill-writing methodology; the router skill at 751 lines is a context monster; centralized activation is a single point of failure. |
| **Matt Pocock** | **7/10** | The most conceptually elegant. Leading words and completion criteria are powerful steering levers. The `diagnosing-bugs` skill's checkbox completion criteria are the best phase-boundary gates in any project. Information hierarchy framework is the best design tool. `disable-model-invocation` gives precise invocation control. Loses points for: very short skills (15 lines for `implement`) may under-specify; no rationalization defense; no testing methodology; no structured output protocol; relies heavily on agent intelligence to fill gaps. |

### Detailed Assessment

**Superpowers excels at:** Discipline enforcement. The combination of rationalization tables + red flags + spirit-vs-letter + pressure-tested wording creates the strongest anti-bypass defense. If you need an agent to ALWAYS follow a rule under pressure, Superpowers' methodology produces the most bulletproof skills.

**cc10x excels at:** Operational orchestration. The router model, tool restrictions, CONTRACT envelopes, and workflow artifacts create a system where skills are components in a pipeline rather than standalone documents. This is the most scalable architecture for multi-agent workflows. The eval scenarios show the beginning of empirical validation.

**Matt Pocock excels at:** Conceptual density. The writing-great-skills glossary is the most sophisticated skill-design framework in any project. The information hierarchy and leading-word concepts are portable to any skill system. The completion-criteria-as-checkboxes pattern is the cleanest phase-gate pattern. If you want skills that are short, sharp, and theoretically grounded, Matt Pocock's approach is the model.

---

## Summary Comparison Table

| Dimension | cc10x | Superpowers | Matt Pocock |
| --- | --- | --- | --- |
| Frontmatter fields | 4-5 (operational) | 2 (discovery) | 2-4 (invocation) |
| Tool restriction | ✅ `allowed-tools` | ❌ | ❌ |
| Activation model | Centralized router | Agent self-discovery | Per-skill toggle |
| Median skill length | 113 lines | 174 lines | 75 lines |
| Skill-writing pedagogy | Implicit | TDD for skills (689 lines) | Vocabulary-driven (83 lines) |
| Rationalization defense | ❌ | ✅ (tables + red flags) | ❌ |
| Leading words | Vocabulary table (building) | Implicit | Taught as concept |
| Reference files | 2-6 per complex skill | 0-4 | 1-4 |
| Eval scenarios | ✅ (3 skills) | ❌ (taught, not shipped) | ❌ |
| Two-mode skills | ✅ (formalized) | ❌ | ❌ |
| Structured output | ✅ (CONTRACT envelope) | ❌ | ❌ |
| Workflow state | ✅ (JSON artifacts) | ❌ | ❌ |
| Spirit-vs-letter | ❌ | ✅ | ❌ |
| Completion criteria | Gates (prose) | Checklists | Checkboxes (observable) |
| Scar comments | ✅ | ❌ | ❌ |
| Model-tier policy | ✅ | ❌ | ❌ |
| Anti-anchoring | ✅ | ❌ | ❌ |
| Information hierarchy | Implicit | Taught (progressive disclosure) | Taught (3-rung ladder) |
| No-op pruning | ❌ | ❌ | ✅ (taught) |
| Steering effectiveness | 7.5/10 | 8/10 | 7/10 |

---

## Verdict

**No single project dominates.** Each has a distinct philosophy:

- **cc10x** is an **orchestration system** that treats skills as pipeline components. Its strengths are operational: tool restriction, router-controlled activation, structured output, workflow artifacts, eval scenarios. Its weakness is that it lacks the anti-rationalization defense and empirical skill-testing methodology that make skills bulletproof under pressure.

- **Superpowers** is a **discipline system** that treats skills as behavioral contracts. Its strengths are defensive: rationalization tables, red-flags lists, spirit-vs-letter, TDD-for-skills. Its weakness is that it lacks the operational scaffolding (tool restriction, structured output, workflow state) that makes skills work in multi-agent pipelines.

- **Matt Pocock** is a **design philosophy** that treats skills as information artifacts. Its strengths are conceptual: leading words, information hierarchy, completion criteria, invocation axis. Its weakness is that it lacks both the anti-rationalization defense and the operational scaffolding.

**The ideal skill system would combine:**

1. cc10x's operational architecture (router, tool restriction, CONTRACT, workflow artifacts, evals)
2. Superpowers' anti-rationalization defense (tables, red flags, spirit-vs-letter, TDD-for-skills)
3. Matt Pocock's design framework (leading words, information hierarchy, completion criteria checkboxes, no-op pruning, glossary)

**For cc10x specifically, the highest-leverage adoptions are:**

1. Add rationalization tables to discipline skills (building, verification, debugging)
2. Add "Red Flags - STOP" lists to gate-based skills
3. Adopt the spirit-vs-letter foundational principle
4. Formalize completion criteria as observable checkboxes (Matt Pocock pattern)
5. Create a cc10x skill-writing guide that teaches leading words, information hierarchy, and no-op pruning
6. Adopt "Use when…" description format for user-facing skills