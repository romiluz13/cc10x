# Deep Comparison: Debugging & Root Cause Analysis

## Projects Analyzed

| Project | Files Examined | Core Artifact |
| --------- | --------------- | --------------- |
| **cc10x** | `debugging/SKILL.md`, `debug-workflow.md`, `bug-investigator.md`, `investigation-hygiene.md`, `root-cause-playbooks.md` | Bug-investigator agent + debugging skill + router workflow |
| **Superpowers** | `systematic-debugging/SKILL.md`, `CREATION-LOG.md`, `condition-based-waiting.md`, `defense-in-depth.md`, `root-cause-tracing.md`, `test-academic.md`, `test-pressure-1/2/3.md`, `condition-based-waiting-example.ts`, `find-polluter.sh` | Systematic-debugging skill with supporting technique files |
| **Matt Pocock** | `diagnosing-bugs/SKILL.md`, `scripts/hitl-loop.template.sh` | Diagnosing-bugs skill (single file + HITL template) |

---

## 1. How Does Each Project Approach Debugging? (Systematic vs Ad-hoc)

### cc10x — **Systematic, Agent-Orchestrated, Multi-Layer**

cc10x treats debugging as a **first-class workflow** with three coupled artifacts:

1. **`debugging/SKILL.md`** — the knowledge base: a 4-phase process (Root Cause → Pattern Analysis → Hypothesis → Implementation) with a 10-rung "construction ladder" for building feedback loops, LSP-powered tracing, hypothesis quality criteria with confidence scoring (0-100), and scenario playbooks.
2. **`bug-investigator.md`** — the agent persona: operationalizes the skill into a strict ordered process (13 steps, "never skip, never reorder"), with mandatory gates (Feedback Loop Gate, No-Loop-No-Hypothesis Gate, Anti-Hardcode Gate, Boundary Instrumentation Matrix), decision checkpoints for escalation, a machine-readable router contract YAML, and debug attempt tracking with a 3-hypothesis cap.
3. **`debug-workflow.md`** — the orchestration layer: a task graph that spawns investigator → reviewer → verifier → memory-persist, with an opt-in fan-out for independent multi-domain bugs gated by a formal independence test (separable understanding + disjoint files), and a fan-in conflict-check before verification.

**Key characteristics:**

- Systematic and **enforced** — gates are "MANDATORY" and "REQUIRED"
- Agent-native: assumes an AI agent is doing the debugging, not a human
- Machine-readable contract output (YAML with strict rules)
- Multi-agent coordination (fan-out/fan-in for parallel debugging)
- Traceable: every step has a specific output or status

### Superpowers — **Systematic, Human-Centric, Pressure-Resistant**

Superpowers treats debugging as a **discipline skill** with a single comprehensive SKILL.md plus four supporting technique files:

1. **`SKILL.md`** — a 4-phase process (Root Cause Investigation → Pattern Analysis → Hypothesis & Testing → Implementation) governed by "The Iron Law" (NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST). Phases must be completed in order.
2. **Supporting files** — `root-cause-tracing.md` (backward tracing technique), `defense-in-depth.md` (multi-layer validation), `condition-based-waiting.md` (replacing arbitrary timeouts), `find-polluter.sh` (test pollution bisection script).
3. **Test files** — 3 pressure tests + 1 academic test that validate the skill's resistance to rationalization under time pressure, sunk cost, and authority/social pressure.

**Key characteristics:**

- Systematic and **pressure-resistant** — explicit anti-rationalization language
- Human-centric: written for a human or AI following a process
- Focus on **cognitive friction** — anti-patterns section lists exact thoughts that should trigger STOP
- Includes "your human partner's signals" — external cues that you're doing it wrong
- Rich testing methodology for the skill itself (pressure tests are unique)

### Matt Pocock — **Systematic, Feedback-Loop-First, Minimalist**

Matt Pocock's approach is a **single-file skill** with 6 phases:

1. **Phase 1: Build a feedback loop** — "This is the skill. Everything else is mechanical." Disproportionate effort here. 10 ranked construction methods (nearly identical to cc10x's ladder).
2. **Phase 2: Reproduce + minimise** — confirm it's the user's bug, shrink to smallest repro.
3. **Phase 3: Hypothesise** — generate 3-5 ranked hypotheses before testing any. Show to user as cheap checkpoint.
4. **Phase 4: Instrument** — one probe per hypothesis, tagged logs, debugger preferred over logs.
5. **Phase 5: Fix + regression test** — test before fix, seam check, watch fail then pass.
6. **Phase 6: Cleanup + post-mortem** — remove instrumentation, verify repro gone, architectural handoff.

**Key characteristics:**

- Systematic but **lean** — no YAML contracts, no agent orchestration, no multi-agent fan-out
- Feedback-loop-centric: Phase 1 is explicitly "the skill"
- User-collaborative: hypotheses shown to user for domain knowledge
- Includes "minimise" step (shrink repro) that others lack as an explicit phase
- Pragmatic: "Skip phases only when explicitly justified"

### Summary Comparison

| Dimension | cc10x | Superpowers | Matt Pocock |
| ----------- | ------- | ------------- | ------------- |
| **Systematic?** | Yes, enforced by gates | Yes, enforced by "Iron Law" | Yes, enforced by "no loop, no Phase 2" |
| **Phases** | 4 phases + 13-step agent process | 4 phases | 6 phases |
| **Enforcement mechanism** | Mandatory gates + machine-readable contract | Anti-pattern catalog + pressure tests | Completion checklist per phase |
| **Target audience** | AI agent (Claude Code) | Human or AI | Human or AI |
| **Orchestration** | Multi-agent task graph | Single agent | Single agent |
| **Feedback loop emphasis** | High (10-rung ladder, mandatory gate) | Medium (reproduce consistently) | Highest (Phase 1 IS the skill) |

---

## 2. What Root Cause Analysis Techniques Does Each Project Use?

### cc10x

| Technique | Description |
| ----------- | ------------- |
| **LSP-Powered Tracing** | Go to Definition, Find References, Go to Type Definition, Hover — trace values through codebase with type info instead of grepping |
| **Boundary Instrumentation Matrix** | For multi-component bugs: instrument each boundary (data-in, data-out, env+config), find first wrong data-out |
| **Runtime Stack-Capture Fallback** | For dynamic/async dispatch where LSP dead-ends: `new Error().stack` at suspect site |
| **Git History Analysis** | `git log --oneline -20 -- <files>`, `git blame`, `git diff BASE..HEAD` |
| **Hypothesis Quality Criteria** | Hypotheses must state a specific mechanism, predict a test outcome, be falsifiable, and explain ALL symptoms |
| **Confidence Scoring** | 0-100 scale: <60 speculative (don't act), 60-79 plausible (investigate more), 80-89 strong, 90-100 verified |
| **3-Hypothesis Cap** | After 3 failed hypotheses, set `NEEDS_EXTERNAL_RESEARCH: true` — prevents pattern-matching death spiral |
| **Scenario Playbooks** | Pre-built playbooks for: build/type failures, test failures, runtime failures, browser/console failures, intermittent/async failures, "it worked before" (git bisect), multi-component boundary tracing, nearby duplicate scan |
| **Variant Scan** | Identify which variant dimensions must keep working (locale, config, env, platform, data shape, concurrency) |

### Superpowers

| Technique | Description |
| ----------- | ------------- |
| **Backward Call Chain Tracing** | `root-cause-tracing.md`: observe symptom → find immediate cause → ask "what called this?" → keep tracing up → find original trigger → fix at source |
| **Stack Trace Instrumentation** | Add `new Error().stack` logging before dangerous operations, use `console.error` not logger |
| **Multi-Component Boundary Logging** | Log data-in/data-out at each component boundary, run once, find where truth changes |
| **Find-Polluter Bisection** | `find-polluter.sh` script: run tests one-by-one to find which test creates pollution |
| **Working Example Comparison** | Find similar working code in same codebase, compare against reference implementation (read COMPLETELY, don't skim) |
| **3-Fix Architectural Escalation** | After 3+ failed fixes, question architecture (not just implementation) — "Is this pattern fundamentally sound?" |
| **Single Hypothesis Rule** | Form ONE hypothesis, test minimally, one variable at a time |
| **Defense-in-Depth (post-fix)** | 4-layer validation: entry point + business logic + environment guards + debug instrumentation |

### Matt Pocock

| Technique | Description |
| ----------- | ------------- |
| **Feedback Loop as Root Cause Engine** | The tight loop itself IS the root cause tool — bisection, hypothesis testing, and instrumentation all consume it |
| **Repro Minimisation** | Shrink repro to smallest scenario that still goes red — cut inputs, callers, config one at a time. "Every remaining element is load-bearing." |
| **3-5 Ranked Hypotheses** | Generate multiple hypotheses before testing any — prevents anchoring on first plausible idea |
| **User as Domain Knowledge Source** | Show ranked hypotheses to user before testing — "cheap checkpoint, big time saver" |
| **Tagged Instrumentation** | Unique prefix per debug session (`[DEBUG-a4f2]`), cleanup is single grep |
| **Performance Baseline Bisect** | For perf regressions: establish baseline measurement, bisect — "measure first, fix second" |
| **Correct Seam Check** | Verify the test exercises the real bug pattern at the call site. If no correct seam exists, that IS the finding |
| **Architectural Handoff** | "What would have prevented this bug?" → if architectural, hand off to `/improve-codebase-architecture` |

### Cross-Project Comparison

| Technique | cc10x | Superpowers | Matt Pocock |
| ----------- | ------- | ------------- | ------------- |
| LSP-powered tracing | ✅ Unique | ❌ | ❌ |
| Backward call chain | ✅ (via playbooks) | ✅ (dedicated file) | ❌ (implicit) |
| Boundary instrumentation | ✅ (matrix format) | ✅ (narrative format) | ✅ (probe per hypothesis) |
| Confidence scoring (0-100) | ✅ Unique | ❌ | ❌ |
| Hypothesis quality criteria | ✅ (4 explicit criteria) | ❌ (single hypothesis) | ✅ (falsifiability required) |
| Multi-hypothesis generation | ✅ (H1/H2/H3) | ❌ (single at a time) | ✅ (3-5 ranked) |
| Repro minimisation | ❌ | ❌ | ✅ Unique explicit phase |
| User collaboration checkpoint | ❌ | ❌ | ✅ Unique |
| Scenario playbooks | ✅ Unique (8 scenarios) | ❌ | ❌ |
| Architectural escalation | ✅ (decision checkpoints) | ✅ (3-fix rule) | ✅ (post-mortem handoff) |
| Find-polluter script | ❌ | ✅ Unique | ❌ |
| Stack-capture fallback | ✅ (for async/dynamic) | ✅ (for manual tracing) | ❌ |
| Git bisect | ✅ (rung 8) | ✅ (playbook) | ✅ (rung 8) |

---

## 3. How Does Each Project Handle Pressure / Debugging Under Time Constraints?

### cc10x

cc10x handles pressure **structurally** rather than rhetorically:

- **No explicit pressure test scenarios** — pressure is handled by the process being mandatory regardless of context
- **Gates enforce discipline**: Feedback Loop Gate, No-Loop-No-Hypothesis Gate, Anti-Hardcode Gate — these fire regardless of urgency
- **Decision checkpoints** provide escape hatches: return `STATUS: BLOCKED` when fix requires >3 files, changes public API, or has multiple valid root causes
- **Debug attempt tracking with cap**: After 3 failed hypotheses → `NEEDS_EXTERNAL_RESEARCH: true`. This prevents death-spiral under pressure by forcing a reset
- **Self-managed research**: Router spawns researcher in parallel — pressure doesn't mean you're alone
- **Machine-readable contract**: Forces structured output even under pressure — no vague "I think it's fixed"
- **No "quick fix" exception**: The process has no escape valve for urgency — it's designed to be followed always

**Weakness:** No explicit acknowledgment that pressure exists or strategies for resisting it. An agent under pressure could still rationalize skipping steps if gates aren't technically enforced by the system.

### Superpowers

Superpowers handles pressure **explicitly and with the most depth**:

- **Pressure tests as first-class artifacts**: 3 dedicated pressure test scenarios:
  - `test-pressure-1.md`: Production outage, $15k/minute revenue loss, manager demanding fix NOW. Tests whether you follow process or take quick fix.
  - `test-pressure-2.md`: 4 hours sunk, 8pm, dinner plans, exhaustion. Tests sunk-cost fallacy and "good enough" rationalization.
  - `test-pressure-3.md`: Senior engineer + tech lead + social pressure to accept quick fix. Tests authority compliance vs process adherence.
- **Anti-rationalization language**: "ALWAYS" / "NEVER" (not "should" / "try to"), "even if faster", "STOP and re-analyze"
- **Common Rationalizations table**: Explicitly lists excuses ("Emergency, no time for process" → "Systematic debugging is FASTER than guess-and-check thrashing")
- **Red Flags section**: Lists exact thoughts that mean STOP ("Quick fix for now, investigate later", "Just try changing X and see if it works")
- **"Your human partner's signals"**: External cues that you're doing it wrong ("Stop guessing", "Ultra-think this")
- **Explicit claim**: "Systematic debugging is FASTER than guess-and-check thrashing" — reframes process as the fast path
- **Real-world impact stats**: "15-30 minutes to fix vs 2-3 hours of thrashing", "95% vs 40% first-time fix rate"

**Strength:** Most pressure-resistant debugging methodology. The pressure tests are unique across all three projects and provide a validation mechanism that the skill actually resists shortcuts.

### Matt Pocock

Matt Pocock handles pressure **pragmatically and through loop discipline**:

- **"Be aggressive. Be creative. Refuse to give up."** — the energy for Phase 1 (building the loop) is explicitly high-effort
- **"Spend disproportionate effort here"** — acknowledges that the loop-building phase feels slow but is the highest-leverage investment
- **No-loop-no-progress rule**: "If you catch yourself reading code to build a theory before this command exists, stop" — prevents the most common pressure failure (jumping to hypothesis)
- **Skip phases only when explicitly justified**: "Skip phases only when explicitly justified" — allows pragmatic deviation but requires justification
- **User as pressure valve**: Showing hypotheses to user ("They often have domain knowledge that re-ranks instantly") — leverages human knowledge to accelerate under pressure
- **Perf branch**: Separate track for performance regressions — "measure first, fix second" prevents frantic guessing on perf bugs
- **No explicit pressure tests or anti-rationalization catalog**

**Strength:** The "refuse to give up" framing on loop-building is unique — it acknowledges that the hardest part of debugging is the patience to build the loop, not the fix itself.

### Summary

| Pressure Handling | cc10x | Superpowers | Matt Pocock |
| ------------------- | ------- | ------------- | ------------- |
| Explicit pressure tests | ❌ | ✅ (3 scenarios) | ❌ |
| Anti-rationalization catalog | ❌ | ✅ (table + red flags) | ❌ |
| Process-as-faster framing | ❌ | ✅ ("faster than thrashing") | ✅ (loop is 90% of fix) |
| Mandatory gates (no escape) | ✅ (strongest) | ❌ (relies on discipline) | ✅ (no-loop gate) |
| Decision checkpoints / escape hatches | ✅ | ✅ (3-fix rule) | ✅ (skip with justification) |
| User collaboration under pressure | ❌ | ❌ | ✅ (hypothesis checkpoint) |
| Sunk-cost resistance | ❌ | ✅ (test-pressure-2) | ❌ |
| Authority resistance | ❌ | ✅ (test-pressure-3) | ❌ |

---

## 4. Defense-in-Depth Patterns — What Does Each Project Recommend?

### cc10x

cc10x integrates defense-in-depth as **Step 11b in the bug-investigator process**:

> "for invalid-data bugs: validate at entry-point + business-logic + environment-guard + forensic instrumentation. Make the bug CLASS structurally impossible."

- **4 layers**: entry_point, business_logic, environment_guard, forensic_instrumentation
- **Machine-readable**: `DEFENSE_IN_DEPTH` field in router contract YAML with `applicable`, `layers` array
- **Triggered conditionally**: only for invalid-data bugs (not all bugs)
- **Integrated into close-out**: defense-in-depth is part of the agent's standard process, not a separate reference

### Superpowers

Superpowers has a **dedicated file** (`defense-in-depth.md`) with the most detailed treatment:

- **Same 4 layers**: Entry Point Validation, Business Logic Validation, Environment Guards, Debug Instrumentation
- **Concrete code examples** for each layer (TypeScript)
- **Data flow mapping**: Trace data flow → map all checkpoints → add validation at each → test each layer
- **Real-world example**: Empty `projectDir` causing `git init` in source code — shows all 4 layers applied
- **Key insight**: "All four layers were necessary. During testing, each layer caught bugs the others missed" — different code paths bypassed entry validation, mocks bypassed business logic, edge cases needed environment guards
- **Philosophy**: "Single validation: 'We fixed the bug'. Multiple layers: 'We made the bug impossible.'"

### Matt Pocock

Matt Pocock **does not have an explicit defense-in-depth pattern**:

- The post-mortem in Phase 6 asks "what would have prevented this bug?" but doesn't prescribe multi-layer validation
- Architectural handoff to `/improve-codebase-architecture` is the closest analog — if the answer involves architectural change, hand off
- The "correct seam" concept is related (test at the right level) but is about test placement, not defense layers
- No mention of entry-point validation, environment guards, or forensic instrumentation

### Comparison

| Defense-in-Depth | cc10x | Superpowers | Matt Pocock |
| ------------------ | ------- | ------------- | ------------- |
| Explicit 4-layer model | ✅ | ✅ | ❌ |
| Code examples per layer | ❌ | ✅ | ❌ |
| Real-world case study | ❌ | ✅ | ❌ |
| Integrated into process | ✅ (step 11b) | ✅ (referenced from SKILL.md) | ❌ |
| Machine-readable tracking | ✅ (YAML field) | ❌ | ❌ |
| "Make bug impossible" philosophy | ✅ (explicit) | ✅ (explicit) | ❌ |

---

## 5. How Does Each Project Handle Debugging Multi-File Issues?

### cc10x

cc10x has the **most sophisticated multi-file debugging approach**:

1. **Boundary Instrumentation Matrix**: For multi-component bugs (frontend→API→worker→DB), instrument EACH boundary with data-in/data-out/env+config. Find the first boundary where data-out is wrong → that layer owns the bug. Presented as a structured table.

2. **Multi-Component Boundary Tracing** (in playbooks): Explicit technique for bugs crossing components/services — instrument boundaries at handoff points where values could be corrupted.

3. **Blast Radius Scan**: After fix, search same file for identical anti-patterns, scan adjacent files for same signature. Three outcomes: fixed all safe duplicates, fixed repro only with deferred duplicates, blocked scope expansion.

4. **Fan-out/Fan-in for Multi-Domain Bugs** (debug-workflow.md):
   - **Independence Test**: Two halves must pass — (a) Separable understanding (each problem fixable without knowing the other's root cause), (b) Disjoint files (no file in two groups)
   - If both pass: fan out one investigator per domain, each scoped to non-overlapping file set
   - If either fails: single investigator over all failures
   - **Fan-in Conflict-Check**: Before unified verifier, intersect edited-file sets pairwise. If any file edited by two investigators → conflict → reconcile → re-check
   - **Single unified verifier**: Never one verifier per domain — a real fix must hold across the whole suite

5. **Decision Checkpoints**: Return `STATUS: BLOCKED` when fix requires changing >3 files or changes public API/interface.

6. **Nearby Duplicate Scan** (in playbooks): After root cause, `rg -n "same_bad_pattern" src test` — check sibling handlers, parallel code paths, duplicate transforms.

### Superpowers

Superpowers handles multi-file issues through:

1. **Multi-component boundary logging**: Log data-in/data-out at each component boundary, run once, find where truth changes. Example with CI → build → signing pipeline.

2. **Backward call chain tracing** (`root-cause-tracing.md`): Trace through the call chain across files — `WorktreeManager → Session → Project → test`. This naturally spans multiple files.

3. **Find-polluter bisection** (`find-polluter.sh`): For test pollution across files — runs tests one-by-one to find which test creates unwanted state. Multi-file by design.

4. **Defense-in-depth data flow mapping**: "Trace the data flow — where does bad value originate? Where used? Map all checkpoints" — spans multiple files/layers.

5. **No fan-out or parallelism**: Superpowers assumes a single agent/human doing the work. No concept of parallel investigators or file-set scoping.

6. **Architectural escalation**: After 3 failed fixes touching different layers, question the architecture — "each fix reveals new shared state/coupling/problem in different place."

### Matt Pocock

Matt Pocock handles multi-file issues through:

1. **Feedback loop spanning components**: The 10-rung construction ladder includes "throwaway harness" (minimal subset of system with mocked deps) and "differential loop" (old vs new version) — both can span files.

2. **Minimisation step**: Shrink repro by cutting inputs, callers, config one at a time — naturally involves identifying which files/components are load-bearing.

3. **Instrumentation at boundaries**: "Targeted logs at the boundaries that distinguish hypotheses" — implies multi-file boundary awareness.

4. **Correct seam check**: If no correct seam exists, "the codebase architecture is preventing the bug from being locked down" — architectural handoff for multi-file structural issues.

5. **No fan-out, no conflict detection, no file-set scoping**: Single-agent model throughout.

### Comparison

| Multi-File Capability | cc10x | Superpowers | Matt Pocock |
| ---------------------- | ------- | ------------- | ------------- |
| Boundary instrumentation matrix | ✅ (structured table) | ✅ (narrative) | ✅ (probe per hypothesis) |
| Multi-agent fan-out | ✅ Unique | ❌ | ❌ |
| Independence test for fan-out | ✅ Unique | ❌ | ❌ |
| Fan-in conflict check | ✅ Unique | ❌ | ❌ |
| Blast radius scan | ✅ (same file + adjacent) | ❌ | ❌ |
| Nearby duplicate scan | ✅ (playbook) | ❌ | ❌ |
| Find-polluter bisection | ❌ | ✅ Unique | ❌ |
| Repro minimisation across files | ❌ | ❌ | ✅ Unique |
| >3 files → escalate | ✅ (decision checkpoint) | ✅ (architectural escalation) | ❌ |

---

## 6. What Debugging Patterns Does cc10x Have That the Others DON'T?

| Unique Pattern | Description | Value |
| --------------- | ------------- | ------- |
| **LSP-Powered Root Cause Tracing** | Use Go to Definition, Find References, Go to Type Definition, Hover to trace through codebase with type information instead of grepping | High — leverages AI agent's LSP access for precise tracing |
| **Machine-Readable Router Contract (YAML)** | Structured output with 25+ fields including STATUS, CONFIDENCE, TDD_RED_EXIT, VARIANTS_COVERED, FEEDBACK_LOOP, BOUNDARY_MATRIX, etc. | High — enables programmatic verification that debugging was done correctly |
| **Contract Rules** | Explicit rules: `STATUS=FIXED` requires TDD_RED_EXIT=1, TDD_GREEN_EXIT=0, non-empty BLAST_RADIUS_SCAN, FEEDBACK_LOOP.rung != "none", DEBUG_CLOSEOUT.instrumentation_removed=true | High — prevents false "fixed" claims |
| **Multi-Agent Fan-Out with Independence Test** | Parallel debugging of independent bugs with formal separability + disjoint-files test | High — unique parallel debugging capability |
| **Fan-In Conflict Check** | Pairwise file-set intersection before unified verification | High — prevents silent clobbering in parallel debugging |
| **Hypothesis Confidence Scoring (0-100)** | Quantified confidence with action thresholds (<60 don't act, 80+ implement) | Medium — adds precision to hypothesis evaluation |
| **Anti-Hardcode Gate** | Mandatory check for variant dependencies (locale, config, env, platform, time, data shape, concurrency) before fix | Medium — prevents single-case fixes |
| **Variant Scan** | Identify which variant dimensions must keep working | Medium — ensures fix doesn't break other configurations |
| **Regression Seam Discipline** | Explicit concept of "correct seam" vs "shallow test" — if no correct seam, document as finding, flag for architecture | Medium — prevents false confidence from shallow tests |
| **Debug Close-Out Protocol** | Mandatory grep-remove of tagged instrumentation, confirm repro no longer fires, state winning hypothesis, architectural handoff | Medium — ensures clean exit |
| **Scenario Playbooks (8 scenarios)** | Pre-built debugging playbooks for build/type, test, runtime, browser, intermittent/async, "it worked before", multi-component, nearby duplicate | Medium — accelerates debugging for common patterns |
| **Self-Managed Research Integration** | Router spawns researcher in parallel when investigator is stuck, re-invokes with research files | Medium — external knowledge injection |
| **Memory Note Persistence** | Learnings, patterns, verification, deferred issues persisted to `.cc10x/*.md` | Low-Medium — institutional memory |
| **Investigation Hygiene Reference** | Context-budget discipline, evidence log format, hypothesis tracking format, stalled-instruction detection, reset protocol | Medium — meta-discipline for the investigation itself |

---

## 7. What Debugging Patterns Do the Others Have That cc10x SHOULD Adopt?

### From Superpowers

| Pattern | Description | Why cc10x Should Adopt It |
| --------- | ------------- | -------------------------- |
| **Pressure Tests** | 3 explicit scenarios (production outage, sunk cost, authority pressure) that validate the skill resists shortcuts under pressure | cc10x's debugging skill is never tested. Adding pressure tests would validate that the agent actually follows the gates under duress. Currently, gates are declared "MANDATORY" but there's no evidence they hold under pressure. |
| **Anti-Rationalization Catalog** | Explicit table mapping excuses to reality ("Emergency, no time for process" → "Systematic debugging is FASTER") | cc10x relies on gates for enforcement but doesn't address the cognitive process of rationalization. An agent could skip a gate and rationalize it. The catalog creates cognitive friction. |
| **Red Flags Section** | Lists exact thoughts that mean STOP ("Quick fix for now", "Just try changing X") | cc10x has "When to Restart Investigation" but doesn't enumerate the specific failure-mode thoughts. More actionable than abstract rules. |
| **"Systematic is Faster" Framing** | Explicitly reframes process as the fast path with stats (15-30 min vs 2-3 hours, 95% vs 40% first-fix rate) | cc10x's gates feel bureaucratic. Reframing them as time-savers would improve adoption. |
| **Defense-in-Depth Code Examples** | Concrete TypeScript examples for each of the 4 layers | cc10x names the 4 layers but doesn't show what they look like. Examples would make the pattern actionable. |
| **Dedicated Root-Cause Tracing File** | Complete backward tracing technique with decision tree, stack trace tips, real-world example | cc10x covers this in playbooks but doesn't have a standalone reference. A dedicated file would be more discoverable. |
| **Find-Polluter Script** | Bisection script for finding which test creates pollution | Practical tool that cc10x's playbooks don't include. Very useful for test-pollution bugs. |
| **Condition-Based Waiting Pattern** | Replace arbitrary timeouts with condition polling; includes complete TypeScript implementation | cc10x mentions flaky bugs but doesn't prescribe the fix pattern. This is a concrete technique for a common debug outcome. |
| **3-Fix Architectural Escalation** | After 3+ failed fixes, explicitly question architecture (not just implementation) | cc10x has a 3-hypothesis cap → research, but doesn't explicitly escalate to "question the architecture." Superpowers' framing is more fundamental. |

### From Matt Pocock

| Pattern | Description | Why cc10x Should Adopt It |
| --------- | ------------- | -------------------------- |
| **Repro Minimisation as Explicit Phase** | After reproducing, shrink to smallest scenario that still goes red — cut inputs one at a time, re-run after each cut | cc10x doesn't have this as a step. Minimisation shrinks hypothesis space and produces cleaner regression tests. High value. |
| **3-5 Ranked Hypotheses Before Testing** | Generate multiple hypotheses before testing any, to avoid anchoring | cc10x says "H1/H2/H3" but doesn't explicitly require generating all before testing any. Matt Pocock's "3-5 ranked" is more specific and includes anti-anchoring rationale. |
| **User as Domain Knowledge Checkpoint** | Show ranked hypotheses to user before testing — "cheap checkpoint, big time saver" | cc10x is agent-autonomous and doesn't leverage user knowledge during hypothesis ranking. This is a cheap acceleration. |
| **Completion Checklist per Phase** | Explicit checkboxes for each phase's completion criteria | cc10x uses prose gates. Checkboxes are more scannable and verifiable. |
| **"This is the skill" Framing for Feedback Loop** | Explicit statement that the feedback loop IS the skill, everything else is mechanical | cc10x treats the loop as one step among many. Matt Pocock's framing correctly identifies it as the highest-leverage activity. |
| **Perf Branch** | Separate track for performance regressions: "establish baseline, bisect, measure first fix second" | cc10x's playbooks mention performance degradation but don't prescribe a distinct approach. Perf bugs need measurement, not logging. |
| **HITL Loop Template Script** | Structured bash script for human-in-the-loop reproduction | cc10x lists HITL as "LAST resort" rung 10 but doesn't provide a template. Matt Pocock's template makes it structured rather than ad-hoc. |

---

## 8. Rating Each Project's Debugging Methodology (1-10)

### cc10x — **8.5/10**

**Strengths:**

- Most comprehensive debugging system: skill + agent + workflow + references
- LSP-powered tracing is unique and leverages AI agent capabilities
- Machine-readable contract enables programmatic verification
- Multi-agent fan-out/fan-in for parallel debugging is unique and powerful
- Scenario playbooks provide accelerators for common bug types
- Formal gates prevent skipping critical steps
- Investigation hygiene reference addresses meta-discipline
- Debug close-out protocol ensures clean exit

**Weaknesses:**

- No pressure testing or anti-rationalization mechanisms — gates are declared but not validated
- No repro minimisation step — misses a key technique for shrinking hypothesis space
- No user collaboration checkpoint during hypothesis ranking
- Defense-in-depth lacks code examples (just names the layers)
- No condition-based waiting pattern for flaky test fixes
- No find-polluter utility
- Single-hypothesis testing not explicitly anti-anchoring (allows testing H1 before generating H2/H3)
- Process is heavy — 13 mandatory steps may be overkill for simple bugs (no "skip with justification" like Matt Pocock)

### Superpowers — **7.5/10**

**Strengths:**

- Most pressure-resistant methodology — explicit tests, anti-rationalization catalog, red flags
- "Systematic is faster" framing with real-world stats
- Dedicated technique files (root-cause-tracing, defense-in-depth, condition-based-waiting)
- Find-polluter script — practical tool
- Defense-in-depth with code examples and real-world case study
- 3-fix architectural escalation — questions fundamentals, not just implementation
- Condition-based waiting pattern — concrete technique for flaky tests
- Skill creation log shows rigorous development methodology

**Weaknesses:**

- No LSP-powered tracing — relies on manual/grep-based tracing
- No machine-readable output — can't programmatically verify debugging was done correctly
- No multi-agent coordination — single-agent model
- No scenario playbooks — less acceleration for common bug types
- No confidence scoring for hypotheses
- No variant scan or anti-hardcode gate
- No blast radius scan as explicit step
- No regression seam discipline concept
- Single-hypothesis rule (one at a time) may be slower than multi-hypothesis generation
- No repro minimisation step
- No user collaboration checkpoint
- Written for humans first — less agent-native than cc10x

### Matt Pocock — **7.0/10**

**Strengths:**

- Feedback-loop-first philosophy is correct — "This is the skill"
- Repro minimisation as explicit phase is unique and valuable
- 3-5 ranked hypotheses before testing prevents anchoring
- User collaboration checkpoint is practical and cheap
- Correct seam concept prevents false confidence
- Perf branch for performance regressions
- HITL loop template makes last-resort repro structured
- Lean and readable — 6 phases, clear checklists
- "Refuse to give up" energy for loop-building
- Phase completion checklists are scannable
- Tagged instrumentation with unique prefix
- Architectural handoff post-fix

**Weaknesses:**

- No LSP-powered tracing
- No multi-agent coordination
- No machine-readable output
- No pressure testing or anti-rationalization
- No defense-in-depth pattern
- No scenario playbooks
- No confidence scoring
- No variant scan or anti-hardcode gate
- No blast radius scan
- No debug attempt tracking or cap
- No formal close-out protocol (has checklist but less rigorous than cc10x)
- No investigation hygiene reference
- No memory/learning persistence
- Single file — less discoverable structure

---

## Verdict

### Overall Ranking

1. **cc10x: 8.5/10** — Most comprehensive and agent-native. Best for AI agent debugging at scale. Needs pressure resistance and repro minimisation.
2. **Superpowers: 7.5/10** — Most pressure-resistant and human-cognitive. Best for teaching debugging discipline. Needs agent-native features (LSP, contracts, multi-agent).
3. **Matt Pocock: 7.0/10** — Most focused and pragmatic. Best feedback-loop philosophy and repro minimisation. Needs comprehensive coverage for complex scenarios.

### Key Insight

The three projects represent **complementary philosophies**:

- **cc10x** = *Enforcement* — mandatory gates, machine-readable contracts, multi-agent coordination. The assumption is that the agent will try to cut corners, so the system makes it structurally hard to do so.
- **Superpowers** = *Cognitive resistance* — anti-rationalization language, pressure tests, red flags. The assumption is that the human/agent will rationalize shortcuts, so the skill creates cognitive friction at the exact moments of weakness.
- **Matt Pocock** = *Leverage* — feedback loop is everything, minimize ruthlessly, use the user as a knowledge source. The assumption is that debugging speed comes from the quality of the repro signal, not the breadth of the process.

### Ideal Debugging Methodology (Synthesis)

The ideal methodology would combine:

1. **cc10x's** LSP tracing, machine-readable contract, multi-agent fan-out, scenario playbooks, and formal gates
2. **Superpowers'** pressure tests, anti-rationalization catalog, defense-in-depth code examples, find-polluter script, and condition-based waiting pattern
3. **Matt Pocock's** repro minimisation phase, 3-5 ranked hypotheses before testing, user collaboration checkpoint, and perf branch

### Top 5 Recommendations for cc10x

1. **Add pressure tests** (from Superpowers) — validate that gates hold under production-outage, sunk-cost, and authority-pressure scenarios
2. **Add repro minimisation as explicit step** (from Matt Pocock) — after reproducing, shrink to smallest red scenario before hypothesis
3. **Add anti-rationalization catalog** (from Superpowers) — map common excuses to reality, create cognitive friction
4. **Add user collaboration checkpoint** (from Matt Pocock) — show ranked hypotheses to user before testing
5. **Add condition-based waiting pattern** (from Superpowers) — concrete technique for fixing flaky tests after root cause is found

---

*Analysis completed. All files from all three projects were read in full.*
