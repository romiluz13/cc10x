# Deep Analysis: EveryInc/compound-engineering-plugin Skills — What cc10x Should Steal

> **Source**: `/Users/rom.iluz/Dev/everyinc-compound-engineering/skills/`
> **Target**: `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/`
> **Method**: Read every SKILL.md in full (all 15 skills), plus CONCEPTS.md, CLAUDE.md, and README.md. Extracted unique patterns, compared to cc10x equivalents, and rated by impact.

---

## Executive Summary

The EveryInc compound-engineering plugin is a **mature, production-grade skill suite** built around a single philosophy: *each unit of engineering work should make subsequent units easier*. It implements a complete pipeline: brainstorm → plan → work → simplify → review → compound, with supporting skills for debugging, strategy, product pulse, dogfooding, feedback sweeping, and more.

cc10x is a strong agent workflow plugin with parallel agents, planning, debugging, code review, and memory management. The EveryInc plugin has several **high-impact patterns** cc10x doesn't have:

1. **Knowledge compounding** (ce-compound + ce-compound-refresh) — a durable learnings store that makes future work smarter
2. **Multi-persona parallel code review** with confidence anchors, cross-model adversarial passes, and deduplication
3. **Worktree isolation management** as a first-class skill
4. **Evidence-first execution** (test-first proof, characterization tests) baked into the work execution skill
5. **Structured artifacts as handoff contracts** between skills (unified plan with readiness levels)
6. **Dogfooding** — automated browser QA with persona-based judgment
7. **Feedback sweep** — closing the loop from user feedback back to engineering

The patterns below are ranked by impact and mapped to specific cc10x target files.

---

## Skill-by-Skill Analysis

### 1. ce-compound — The Core Compounding Concept

**What it does**: After a problem is solved, captures the solution as a structured doc in `docs/solutions/[category]/` with YAML frontmatter. Uses parallel subagents (Context Analyzer, Solution Extractor, Related Docs Finder) to research, cross-reference, and write. Also maintains `CONCEPTS.md` (shared domain vocabulary) and checks discoverability in instruction files.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Knowledge compounding loop** | After any fix/work, capture learnings as structured docs that future planning/debugging reads as grounding. Creates a self-improving system. | **HIGH** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` |
| **Parallel subagent artifact pattern** | Subagents write full output to `/tmp/compound-engineering/ce-compound/<run-id>/` scratch files and return only the path. Orchestrator reads artifacts back. Solves the "summary collapse" problem where subagents return executive summaries instead of full prose. | **HIGH** | `plugins/cc10x/skills/agent-common/SKILL.md` (add artifact-write protocol) |
| **CONCEPTS.md vocabulary capture** | Maintains a shared domain vocabulary file that anchors terminology across skills. Terms accrete as learnings are processed. | **MEDIUM** | New convention in `plugins/cc10x/skills/memory-and-handoff/` |
| **Discoverability check** | After writing learning docs, checks whether `AGENTS.md`/`CLAUDE.md` would lead an agent to discover and search the knowledge store. Edits instruction files if not. | **MEDIUM** | `plugins/cc10x/skills/diff-driven-docs/SKILL.md` |
| **Overlap assessment** | Before creating a new doc, checks if an existing doc covers the same problem. High overlap → update existing; moderate → flag for consolidation; low → create new. | **MEDIUM** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` |
| **Headless mode** | `mode:headless` runs skills unattended with no user prompts, producing a written report as the deliverable. Conservative deferral of ambiguous decisions. | **HIGH** | `plugins/cc10x/skills/agent-common/SKILL.md` (add headless mode protocol) |
| **Auto-memory scan** | Scans the "user's auto-memory" block in the system prompt for relevant notes before launching subagents. Tags memory-sourced content with origin. | **LOW** | `plugins/cc10x/skills/memory-and-handoff/SKILL.md` |
| **Track-based output** | Bug track vs knowledge track, each with different output sections (Problem/Symptoms/What Didn't Work/Solution/Why/Prevention vs Context/Guidance/Why/When/Examples) | **MEDIUM** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` |
| **YAML frontmatter validation** | Bundled Python validator for parser-safety of frontmatter (catches silent YAML corruption from unquoted `#` or `:` in scalar values) | **LOW** | New utility script in `plugins/cc10x/scripts/` |

**What cc10x should adopt**: The **knowledge compounding loop** is the single highest-value concept. cc10x currently has no mechanism to capture and reuse learnings. Adding a `knowledge-capture` skill that runs after debugging/building and writes structured docs to `docs/solutions/` would make the entire system self-improving. The **parallel subagent artifact pattern** (write to scratch, return path) should be adopted in `agent-common` as a reliability improvement for all parallel agent workflows.

---

### 2. ce-compound-refresh — Knowledge Maintenance

**What it does**: Audits existing `docs/solutions/` learnings against the current codebase. Classifies each as Keep/Update/Consolidate/Replace/Delete. Detects stale references, superseded solutions, overlapping docs, and cross-doc contradictions. Includes document-set analysis (overlap detection, supersession signals, canonical doc identification, retrieval-value test).

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Five-outcome maintenance model** | Keep/Update/Consolidate/Replace/Delete — a structured decision framework for maintaining knowledge artifacts over time | **HIGH** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` (refresh mode) |
| **Document-set analysis** | Evaluates docs as a whole, not just individually. Detects overlap (5 dimensions), supersession, canonical docs, retrieval-value test, cross-doc contradictions. | **MEDIUM** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` |
| **Drift classification** | Cosmetic drift (references moved, solution same → Update) vs substantive drift (solution changed → Replace). The boundary: "if you find yourself rewriting the solution section, that's Replace, not Update." | **MEDIUM** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` |
| **Inbound-link check before delete** | Before deleting a doc, searches the repo for citations. Decorative citations allow delete; substantive citations (citing doc relies on cited doc) signal Replace. | **MEDIUM** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` |
| **Broad-scope triage** | For 9+ docs, does lightweight triage: inventory, impact clustering, spot-check drift, recommend starting area | **LOW** | New skill: `plugins/cc10x/skills/knowledge-capture/SKILL.md` |
| **Commit changes phase** | After refresh, handles git commit (branch creation on main, selective staging, PR option) | **LOW** | `plugins/cc10x/skills/cc10x-router/references/build-workflow.md` |

**What cc10x should adopt**: The **five-outcome maintenance model** and **drift classification** are essential for any knowledge system to remain trustworthy over time. Without refresh, knowledge docs become stale and actively misleading. If cc10x adopts knowledge capture, it needs refresh as a companion.

---

### 3. ce-work — Work Execution

**What it does**: Takes a plan document or bare prompt and executes it systematically. Supports unified plans with readiness levels, worktree isolation, parallel subagent dispatch per implementation unit, evidence-first execution (test-first proof), and a structured shipping tail (simplify → review → commit).

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Unified plan artifact with readiness levels** | `artifact_readiness: requirements-only` (from brainstorm) → `implementation-ready` (from plan). Same file, enriched in place. Prevents duplicate artifacts. | **HIGH** | `plugins/cc10x/skills/planning/SKILL.md` |
| **Evidence-first execution** | Before changing behavior: create/update/strengthen the test and observe the red failure or characterization baseline BEFORE implementing. The worker witnesses this and reports it. | **HIGH** | `plugins/cc10x/skills/building/SKILL.md` |
| **Parallel safety check** | Before dispatching parallel units: map files to units, check file overlap, also serialize on shared types/APIs, DB migrations, generated artifacts, environment singletons. Cap concurrency at ~3-5. | **HIGH** | `plugins/cc10x/skills/cc10x-router/SKILL.md` or `plugins/cc10x/skills/building/SKILL.md` |
| **Return-to-caller mode** | `mode:return-to-caller` — implement and verify only, then return structured envelope instead of running shipping tail. Enables orchestrators like `lfg` to own simplification/review/PR. | **HIGH** | `plugins/cc10x/skills/building/SKILL.md` or `plugins/cc10x/skills/cc10x-router/SKILL.md` |
| **Test discovery** | Before implementing changes to a file, find its existing test files (search for test/spec files that import, reference, or share naming patterns). Use existing tests, update them, or add new ones. | **MEDIUM** | `plugins/cc10x/skills/building/SKILL.md` |
| **System-wide test check** | Before marking a task done: "What fires when this runs?" (callbacks, middleware, observers), "Do my tests exercise the real chain?" (mocks vs integration), "Can failure leave orphaned state?", "What other interfaces expose this?", "Do error strategies align across layers?" | **HIGH** | `plugins/cc10x/skills/verification/SKILL.md` |
| **Test scenario completeness** | Before writing tests: check happy path, edge cases, error/failure paths, integration — derive missing categories from the unit's context | **MEDIUM** | `plugins/cc10x/skills/verification/SKILL.md` |
| **Idempotency check** | If the unit's work is already present and matches the plan's intent, verify and mark complete. Don't silently reimplement. | **MEDIUM** | `plugins/cc10x/skills/building/SKILL.md` |
| **Bounded unit packets for subagents** | Give each worker a bounded unit packet (Goal Capsule, DoD, the unit's section, relevant verification entries) — not "read the whole plan" | **MEDIUM** | `plugins/cc10x/skills/building/SKILL.md` |
| **Meaningful branch name enforcement** | If branch name is meaningless/auto-generated, suggest renaming before continuing | **LOW** | `plugins/cc10x/skills/building/SKILL.md` |

**What cc10x should adopt**: The **evidence-first execution** pattern (test-first proof before implementation) is the most impactful. cc10x's building skill could be significantly strengthened by requiring the agent to observe a red failure or characterization baseline before changing production code. The **parallel safety check** is also critical — cc10x already has parallel agents but needs explicit contention detection. The **system-wide test check** five-question framework would dramatically improve verification quality.

---

### 4. ce-worktree — Worktree Management

**What it does**: Ensures work happens in an isolated workspace. Detects existing isolation first, prefers harness-native worktree tools, falls back to plain git. Two modes: new work (fresh branch) and isolate existing ref (PR/branch/commit).

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Detect-first worktree strategy** | Before creating anything, check if already in a linked worktree. Compare resolved absolute git dir vs common git dir. Distinguish submodule from worktree. Never create redundant worktree. | **HIGH** | New skill: `plugins/cc10x/skills/worktree/SKILL.md` |
| **Harness-native tool preference** | Use harness native worktree primitive (EnterWorktree, /worktree, --worktree flag) if available. Never do behind-the-back `git worktree add` that harness can't see. | **HIGH** | New skill: `plugins/cc10x/skills/worktree/SKILL.md` |
| **One-branch-one-worktree rule** | A branch can be checked out in only one worktree. If ref already checked out, don't create a second — report location and work in place. | **MEDIUM** | New skill: `plugins/cc10x/skills/worktree/SKILL.md` |
| **PR checkout on local branch** | For PR isolation: `git fetch origin pull/<n>/head:pr-<n>` then `git worktree add .worktrees/pr-<n> pr-<n>`. Never detached FETCH_HEAD. | **MEDIUM** | New skill: `plugins/cc10x/skills/worktree/SKILL.md` |
| **Gitignore before create** | Ensure `.worktrees/` is gitignored BEFORE creating worktree. Use `git check-ignore -q .worktrees/` (with trailing slash). | **MEDIUM** | New skill: `plugins/cc10x/skills/worktree/SKILL.md` |

**What cc10x should adopt**: cc10x has no worktree management skill. Adding one would enable safe parallel development. The **detect-first** approach is critical — blindly creating worktrees when already isolated creates phantom state. This should be a new standalone skill.

---

### 5. ce-proof — Collaborative Markdown Editor Integration

**What it does**: Publishes markdown documents to Proof (a collaborative editor) via web API or local bridge. Supports creating, reading, commenting, suggesting edits, and block-level operations.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Shareable document publishing** | Take a local markdown file and publish it as a shareable URL for human review | **LOW** | N/A (product-specific to Proof/Every) |
| **Narrowest edit primitive** | Prefer find_replace_in_doc → block operations → whole-doc rewrite. Never default to full-document replacement. | **LOW** | N/A |
| **BaseToken management** | Every mutation requires a baseToken; reuse from most recent read; on STALE_BASE, re-read and retry once. Idempotency-Key for safe retries. | **LOW** | N/A |

**What cc10x should adopt**: This is product-specific to Every's Proof editor. The general pattern of **publishing artifacts for human review** is interesting but low priority. The **narrowest edit primitive** philosophy could inform cc10x's diff-driven-docs skill.

---

### 6. ce-dogfood — Autonomous Browser QA

**What it does**: Acts as a QA engineer who dogfoods the active branch end-to-end. Diff-scoped (tests what changed vs trunk). Maps user flows as Mermaid flowcharts, derives test matrix, drives a real browser, fixes small breakages with regression tests, judges experience against product personas, writes a durable report.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Diff-scoped browser QA** | Tests only what the branch introduced/modified vs trunk, not whole-app exploration | **HIGH** | New skill: `plugins/cc10x/skills/browser-qa/SKILL.md` |
| **Flow-first test matrix** | Map user flows as Mermaid flowcharts FIRST, then derive the test matrix from the flows. Tests pages in context of the journey, not in isolation. | **HIGH** | New skill: `plugins/cc10x/skills/browser-qa/SKILL.md` |
| **Persona-based experience judgment** | Walk each journey from each primary persona's perspective. Identify "paper cuts" — small friction that wouldn't fail a functional test but degrades experience. | **MEDIUM** | New skill: `plugins/cc10x/skills/browser-qa/SKILL.md` |
| **Autonomous fix loop** | On failure: investigate root cause (use ce-debug), apply fix, add regression test, commit, re-run scenario. Judge fix size before touching code — auto-fix small/low-risk, escalate large/ambiguous. | **HIGH** | `plugins/cc10x/skills/verification/SKILL.md` |
| **Resumability** | Task list (session-scoped) + report doc (on disk) = checkpoint. Interrupted run leaves template-shaped checkpoint. Resume from report doc. | **MEDIUM** | `plugins/cc10x/skills/memory-and-handoff/SKILL.md` |
| **Durable report artifact** | Writes to `docs/dogfood-reports/` with flows, matrix, fixes, learnings, verdict | **MEDIUM** | New skill: `plugins/cc10x/skills/browser-qa/SKILL.md` |

**What cc10x should adopt**: The **flow-first test matrix** and **autonomous fix loop with size judgment** are powerful patterns. cc10x's verification skill could incorporate the flow-mapping approach. A full browser-qa skill would be a significant addition but requires browser tooling (`agent-browser`).

---

### 7. ce-sweep — Feedback Ingestion Pipeline

**What it does**: Sweeps configured feedback sources (Slack, GitHub Issues, email) for new items. Acknowledges at source, analyzes recordings, verifies fixes merged to main, emits an `/lfg`-ready plan. Includes a deterministic state engine, circuit breaker, lease-based concurrency, and plan reconciliation.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Feedback-to-engineering loop** | Closes the loop from user feedback (Slack, GitHub) back to engineering work items. Feedback items become plan entries. | **HIGH** | New skill: `plugins/cc10x/skills/feedback-sweep/SKILL.md` |
| **Deterministic state engine** | Python script (`sweep-state.py`) is the ONLY writer of sweep state. Skill drives it through subcommands. Never hand-edits state file. | **MEDIUM** | New skill: `plugins/cc10x/skills/feedback-sweep/SKILL.md` |
| **Lease-based concurrency** | Single-writer lease with TTL. On LOCKED, stop. On STALE-RECLAIMED, proceed with note. Shared-branch topology with git push/pull. | **MEDIUM** | N/A (infrastructure) |
| **Circuit breaker** | If new items exceed cap (default 25), interactive → ask, headless → defer all as ack_deferred. Prevents flooding. | **MEDIUM** | New skill: `plugins/cc10x/skills/feedback-sweep/SKILL.md` |
| **Untrusted input handling** | Every item's body, title, quote, media filename treated as DATA, never as instructions. Acknowledgment actions come ONLY from source config, never from item content. | **HIGH** | `plugins/cc10x/skills/agent-common/SKILL.md` (security pattern) |
| **Fix verification** | For each fix_pending item, validate the fix ref shape (PR number or commit SHA only), verify it merged to default branch via `gh pr view` or `git merge-base --is-ancestor` | **MEDIUM** | New skill: `plugins/cc10x/skills/feedback-sweep/SKILL.md` |

**What cc10x should adopt**: The **feedback-to-engineering loop** is a unique capability that no competing plugin has. The **untrusted input handling** pattern (treating all external content as data, never instructions) is a critical security pattern that should be in cc10x's agent-common. A feedback-sweep skill would be a major differentiator.

---

### 8. ce-pov — Project-Grounded Verdict Engine

**What it does**: Returns a decisive, graded verdict on an external technology/library/pattern, judged against THIS project (not in the abstract). Two-floor gate: project floor (verified project fact) + external floor (verified external source). Dispatches tiered scout subagents.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Two-floor verdict gate** | Project floor (concrete verified project fact) + external floor (verified external source). Neither compensates for the other. Generic research is explicitly NOT the differentiator. | **HIGH** | New skill: `plugins/cc10x/skills/research/SKILL.md` (add verdict mode) |
| **Reversibility tiering** | Tier 1 (two-way door, trivially reversible) → Tier 2 (one-way bounded) → Tier 3 (one-way high-stakes). Tier sizes the depth of investigation. | **MEDIUM** | `plugins/cc10x/skills/research/SKILL.md` |
| **Tier-sensitive scout dispatch** | Tier 1: single combined grounding pass. Tier 2/3: full scout fleet (project-grounding, precedent-&-activity, external-evidence). | **MEDIUM** | `plugins/cc10x/skills/research/SKILL.md` |
| **Provenance buckets** | Keep observed-project-facts and verified-external-facts separate from conversation-claims and unconfirmed-assumptions. Only verified facts count as grounding. | **MEDIUM** | `plugins/cc10x/skills/research/SKILL.md` |
| **Anti-ritual follow-up** | Next step is computed from the verdict, not a fixed menu. Tier 1/Reject → single prose line. Tier 2/3 actionable → blocking question with computed first option. | **LOW** | `plugins/cc10x/skills/research/SKILL.md` |

**What cc10x should adopt**: The **two-floor verdict gate** is a powerful research pattern that prevents generic "tell me about X" answers. cc10x's research skill could be significantly enhanced by requiring project-specific grounding before issuing a verdict. The **reversibility tiering** is a smart way to right-size investigation depth.

---

### 9. ce-strategy — Product Strategy Document

**What it does**: Creates and maintains `STRATEGY.md` — a short, durable anchor document capturing what the product is, who it serves, how it succeeds, and where the team is investing. Downstream skills read it as grounding.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Strategy as upstream anchor** | A single `STRATEGY.md` file that all downstream skills (ideate, brainstorm, plan) read as grounding. Product context flows into every feature decision. | **MEDIUM** | `plugins/cc10x/skills/planning/SKILL.md` (add strategy grounding) |
| **Interview with pushback** | Asks sharp questions, pushes back on weak answers (max 2 rounds per section). Anti-patterns: fluff, goals-as-strategy, feature-lists-as-strategy. | **MEDIUM** | `plugins/cc10x/skills/exploration/SKILL.md` |
| **Rerunnable updates** | On second run, updates in place, preserves what's working, challenges only stale/weak sections. `last_updated` in frontmatter. | **LOW** | `plugins/cc10x/skills/planning/SKILL.md` |

**What cc10x should adopt**: The **strategy-as-grounding** pattern is elegant — having a `STRATEGY.md` that planning and exploration read as context would improve decision quality. However, this is a product-management pattern that may be lower priority for a coding-focused plugin. The **interview-with-pushback** pattern could improve cc10x's exploration skill.

---

### 10. ce-product-pulse — Product Health Reports

**What it does**: Generates time-windowed product pulse reports from configured signals (analytics, tracing, payments, database). Single-page report (30-40 lines) covering usage, performance, errors, followups. Saved to `docs/pulse-reports/`.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Read-like-a-founder reports** | No hardcoded thresholds. Present numbers, let reader judge. Single page (30-40 lines). | **LOW** | N/A (product analytics, not coding) |
| **Strategy-seeded configuration** | If `STRATEGY.md` exists, reads it and carries forward product name and key metrics as seeds for pulse setup. | **LOW** | N/A |
| **15-minute trailing buffer** | Query `[now - window - 15m, now - 15m]` to account for analytics ingestion lag. | **LOW** | N/A |

**What cc10x should adopt**: This is a product-analytics skill outside cc10x's coding-focused scope. The **strategy-seeded configuration** pattern (upstream doc seeds downstream setup) is interesting but low priority.

---

### 11. ce-brainstorm — Collaborative Ideation

**What it does**: Explores vague/ambitious ideas into a requirements-only unified plan. Collaborative dialogue with one-question-at-a-time discipline. Routes verdict-shaped questions to ce-pov. Includes visual probe gate for inherently visual topics.

**Comparison to cc10x exploration**:

| Pattern | EveryInc (ce-brainstorm) | cc10x (exploration) | Impact |
| --------- | -------------------------- | --------------------- | -------- |
| **Question discipline** | One question at a time, prefer single-select multiple choice, use multi-select rarely, default to blocking question tool. Open-ended only when genuinely open. | cc10x exploration is more freeform | **MEDIUM** |
| **Scope assessment** | Lightweight / Standard / Deep — with Deep sub-mode (feature vs product). Visual probe tripwire for visual/spatial features. | cc10x has scope assessment but less nuanced | **MEDIUM** |
| **Product pressure test** | Scans user's opening for rigor gaps (per-tier lens catalog). Raises only found gaps during dialogue, not a pre-flight gauntlet. | cc10x doesn't have this | **MEDIUM** |
| **Grounding scout** | Dispatches extraction-tier subagent to scan repo and write a grounding dossier to scratch. Carries only gist in dialogue. Reads dossier on demand. | cc10x has researchers but not this specific pattern | **HIGH** |
| **Claim verification** | Dispatches a generation-tier verifier to check claims against the codebase during the confirmation wait. Fresh-context verifier replaces self-graded verification. | cc10x doesn't have this | **HIGH** |
| **Synthesis summary** | Two-stage shape: internal three-bucket draft → chat-time scoping synthesis. Affirmability test, keep-test criteria, detail test, tier-aware bullet budget. Path A (announce-only) vs Path B (full synthesis with confirmation). | cc10x doesn't have this structured synthesis | **MEDIUM** |
| **Output as unified plan** | Writes requirements-only unified plan with `artifact_contract: ce-unified-plan/v1`, `artifact_readiness: requirements-only`. Same file later enriched by ce-plan. | cc10x writes plans but doesn't have readiness levels | **HIGH** |
| **Verdict routing** | Detects "should we adopt X?" questions and routes to ce-pov instead of brainstorming. Clear separation of "what to build" vs "whether to commit to X". | cc10x doesn't have this routing | **MEDIUM** |
| **Visual probe gate** | For inherently visual topics (canvas, layout, diagrams), offers text-vs-visual choice before raising shape decisions. State-based gate. | cc10x has frontend skill but not this gate | **LOW** |

**What cc10x should adopt**: The **grounding scout + claim verification** pattern is powerful — dispatch a cheap scout to gather repo evidence, then verify claims against the codebase before writing them into a plan. The **artifact readiness levels** (requirements-only → implementation-ready) prevent the "planning invented product behavior" problem. The **verdict routing** (brainstorm scopes what to build, not whether to adopt X) is a clean separation cc10x could adopt.

---

### 12. ce-plan — Technical Planning

**What it does**: Enriches requirements-only plans into implementation-ready plans. Researches codebase, institutional learnings, and external guidance. Breaks work into implementation units with stable U-IDs. Includes confidence check and deepening, document review, and post-generation handoff menu.

**Comparison to cc10x planning**:

| Pattern | EveryInc (ce-plan) | cc10x (planning) | Impact |
| --------- | -------------------- | ------------------ | -------- |
| **Unified plan artifact** | Same file enriched in place. `artifact_readiness: requirements-only` → `implementation-ready`. Preserves Product Contract, adds Planning Contract. | cc10x writes a single plan doc | **HIGH** |
| **Stable U-IDs** | Implementation units get stable IDs (U1, U2, ...). IDs survive reordering, splitting, deletion. Never renumbered. Enables unambiguous cross-reference. | cc10x doesn't have stable unit IDs | **MEDIUM** |
| **Repo-profile cache** | Shared cache for question-agnostic project profile (stack, deps, conventions). Reused across skills. `python3 repo-profile-cache.py get/put`. | cc10x re-derives this every time | **HIGH** |
| **Execution direction signals** | Lightweight natural-language `Execution note` per unit: "Start with failing integration test", "Add characterization coverage before modifying", "Prefer smoke verification". Not an enum, not choreography. | cc10x doesn't have this | **MEDIUM** |
| **Confidence check and deepening** | After writing the plan, automatically evaluates whether it needs strengthening. Scoring checklists, section-to-agent dispatch mapping, auto vs interactive mode. | cc10x has plan-review-gate but not deepening | **MEDIUM** |
| **Test scenario completeness** | Each unit must have test scenarios from every applicable category (happy path, edge cases, error paths, integration). Specific enough that implementer knows exactly what to test. AE-link convention for acceptance examples. | cc10x has verification but not this completeness check | **MEDIUM** |
| **Mandatory completion contract** | Plan is not complete until handoff question is presented. "Plan ready at `<path>`. What would you like to do next?" with computed next-step options. | cc10x doesn't enforce this | **MEDIUM** |
| **Anti-expansion: tangential cleanup** | Adjacent refactors, "while we're here" cleanups, scope-adjacent nice-to-haves → routed to `### Deferred to Follow-Up Work`, not into active units. | cc10x doesn't have this explicitly | **MEDIUM** |
| **High-Level Technical Design audit** | For each architecture trigger (3+ components, 3+ protocol steps, 3+ state machine states, etc.), verify a corresponding sketch/diagram exists. Missing = incomplete. | cc10x doesn't have this audit | **LOW** |

**What cc10x should adopt**: The **repo-profile cache** is a high-impact optimization — cc10x currently re-derives stack/conventions on every skill invocation. A shared cache would save tokens and time across planning, building, debugging, and review. The **stable U-IDs** would improve cross-referencing between planning and building. The **execution direction signals** (lightweight natural-language, not an enum) are a better approach than cc10x's current implicit test strategy.

---

### 13. ce-code-review — Multi-Persona Review

**What it does**: Spawns parallel reviewer personas (correctness, testing, maintainability, project-standards, security, performance, api-contract, data-migration, reliability, adversarial, etc.). Each writes structured JSON to scratch artifacts. Orchestrator merges, deduplicates, validates, and presents findings. Includes cross-model adversarial pass, confidence anchors, and triage groups.

**Comparison to cc10x code-review**:

| Pattern | EveryInc (ce-code-review) | cc10x (code-review) | Impact |
| --------- | -------------------------- | --------------------- | -------- |
| **13 reviewer personas** | Layered conditionals: 4 always-on + 2 CE always-on + 7 cross-cutting/stack-specific conditionals. Each persona is a separate prompt file. | cc10x has a single code-reviewer agent + silent-failure-hunter | **HIGH** |
| **Confidence anchors** | 5 discrete values (0, 25, 50, 75, 100) with behavioral definitions. Cross-reviewer agreement promotes by one step. Quote-the-line gate: 75/100 findings must carry verbatim motivating line. | cc10x doesn't have this | **HIGH** |
| **Cross-model adversarial pass** | Run the same adversarial brief through a different model family via a peer CLI (Codex when host is Claude, Claude when host is Codex). Genuine independence. Non-blocking. | cc10x doesn't have this | **HIGH** |
| **Small-diff fast path** | EXEC_LINES 1-39 + UNCOUNTED_FILES=0 + no risk signals → lite roster (fast pass + correctness + standards only). Fail closed: any uncertainty → full roster. | cc10x doesn't right-size | **MEDIUM** |
| **Inline fast pass** | Orchestrator does a quick first-principles scan of the diff before dispatching personas. Emit preliminary findings in seconds. Capped at anchor 50, never counts toward cross-reviewer promotion. | cc10x doesn't have this | **MEDIUM** |
| **Validation pass** | Spawn one validator subagent per surviving finding. Validator confirms or rejects. P0/P1 never dropped on infra failure. Budget cap of 15. | cc10x doesn't have independent validation | **HIGH** |
| **Triage groups** | Group related findings by root cause/subsystem/failure mode. Mark as apply-queue or decision-gate. Name order/dependency. | cc10x doesn't have this | **MEDIUM** |
| **Mode:agent JSON contract** | Structured JSON for pipeline callers. `actionable_findings`, `triage_groups`, `requirements_completeness`, `coverage`. Deterministic contract for programmatic consumption. | cc10x doesn't have structured output | **HIGH** |
| **Requirements completeness** | When a plan is provided, verify each R-ID and U-ID has corresponding work in the diff. `explicit` plan → P1 findings for unaddressed requirements. `inferred` plan → P3 advisory. | cc10x has plan-gap-reviewer but less sophisticated | **MEDIUM** |
| **Stage 5c apply** | In default mode, applies safe fixes (clear improvements, reversible edits) before presenting report. Verify, then keep. Commit on clean tree. Never push. | cc10x's review is advisory only | **MEDIUM** |
| **Model tiering** | correctness/security/adversarial inherit session model. All others use mid-tier. Explicit tier list as internal working notes. | cc10x doesn't tier | **MEDIUM** |
| **PR-remote scope** | Review PRs without checkout. `local-aligned` (all 3 checks pass) vs `pr-remote` (workspace may be stale). Reviewers inspect via `git show <ref>:<path>` in remote mode. | cc10x requires local checkout | **MEDIUM** |

**What cc10x should adopt**: This is the area with the **most stealable value**. The multi-persona approach with **confidence anchors**, **cross-model adversarial pass**, and **independent validation** would transform cc10x's code review from a single-agent pass into a robust multi-perspective system. The **mode:agent JSON contract** enables pipeline integration (like lfg). The **small-diff fast path** would save tokens on trivial reviews. The **requirements completeness** check ties review back to planning.

---

### 14. ce-debug — Systematic Debugging

**What it does**: Systematic bug diagnosis: triage → investigate → root cause → fix → handoff. Requires full causal chain before proposing a fix. Predictions for uncertain links. One change at a time. Smart escalation when stuck.

**Comparison to cc10x debugging**:

| Pattern | EveryInc (ce-debug) | cc10x (debugging) | Impact |
| --------- | -------------------- | -------------------- | -------- |
| **Causal chain gate** | Do not propose a fix until you can explain the full causal chain from trigger to symptom with no gaps. "Somehow X leads to Y" is a gap. | cc10x has root-cause focus but no explicit gate | **HIGH** |
| **Predictions for uncertain links** | When causal chain has uncertain links, form a prediction (something in a different code path that must also be true). If prediction wrong but fix "works," you found a symptom, not the cause. | cc10x doesn't have this | **HIGH** |
| **Assumption audit** | Before hypothesis formation, list concrete "this must be true" beliefs. Mark each as verified or assumed. Many "wrong hypotheses" are correct hypotheses tested against wrong assumptions. | cc10x doesn't have this | **MEDIUM** |
| **Anti-pattern detection** | Load anti-patterns reference before forming hypotheses. Detect rationalizations: "quick fix for now", "this should work" (without prediction), "let me just try" (without hypothesis). | cc10x has investigation-hygiene but not this | **MEDIUM** |
| **Prior-attempt awareness** | If user indicates prior failed attempts, ask what they've already tried before investigating. Avoids repeating failed approaches. | cc10x doesn't have this | **MEDIUM** |
| **Tracker and PR history check** | Check issue tracker and PR history for prior work on the same bug. Open PR, merged-but-failed attempt, regression's original fix. | cc10x doesn't have this | **MEDIUM** |
| **Smart escalation table** | 4 patterns: hypotheses point to different subsystems → architecture problem; evidence contradicts itself → wrong mental model; works locally fails in CI → environment; fix works but prediction wrong → symptom fix. | cc10x has root-cause-playbooks but not this escalation matrix | **MEDIUM** |
| **3 failed fix attempts = escalation** | Return to Phase 2, explicitly invalidate current hypothesis, form new one. Don't retry variants of same theory. | cc10x doesn't have this limit | **MEDIUM** |
| **Conditional defense-in-depth** | If root-cause pattern found in 3+ files OR bug would have been catastrophic: four-layer model (entry validation, invariant check, environment guard, diagnostic breadcrumb). | cc10x doesn't have this | **MEDIUM** |
| **Conditional post-mortem** | If bug was in production OR pattern appears in 3+ locations: analyze how it was introduced and what allowed it to survive. | cc10x doesn't have this | **MEDIUM** |
| **Post-fix polish/review tail** | After fix: simplify (if >=30 lines), review (ce-code-review), handle residual findings, re-verify. Contextual overrides for "minimal hotfix only" preferences. | cc10x has some of this but less structured | **MEDIUM** |
| **Learning capture offer** | After PR: decide whether to offer learning capture. Skip silently for mechanical fixes. Offer neutrally for one-sentence lessons. Lean in for 3+ locations or wrong assumptions about shared dependencies. | cc10x doesn't have this | **MEDIUM** |

**What cc10x should adopt**: The **causal chain gate** and **predictions for uncertain links** are the most impactful debugging patterns. The **assumption audit** is a simple but powerful addition. The **smart escalation table** would improve cc10x's debugging skill significantly. The **3-failed-attempts limit** prevents the rationalization spiral. cc10x's bug-investigator agent could incorporate these patterns directly.

---

### 15. lfg — Autonomous Pipeline Orchestrator

**What it does**: Runs the full hands-off engineering pipeline: plan → work → simplify → review → apply fixes → handle residuals → browser test → commit/push/PR → CI watch/autofix → DONE. Each step is a gate.

**Unique patterns cc10x doesn't have**:

| Pattern | Description | Impact | Target cc10x File |
| --------- | ------------- | -------- | ------------------- |
| **Gated pipeline with verification at each step** | Each step is a GATE: STOP if the previous step didn't produce its artifact. Verify plan file exists before work. Verify implementation was performed before review. Verify review found actionable findings before residual handoff. | **HIGH** | `plugins/cc10x/skills/cc10x-router/SKILL.md` |
| **Autonomous residual handoff** | Downstream-resolver findings not applied → file in tracker, update PR body, or create fallback file. Never block DONE on tracker filing failures once residuals are durable. | **HIGH** | `plugins/cc10x/skills/cc10x-router/SKILL.md` |
| **CI watch and autofix loop** | Up to 3 fix iterations: wait for CI, pull failure logs, identify root cause, apply fix, push. Never weaken/skip/mock failing assertions. After 3 failures, compose "CI Failures Unresolved" section in PR body. | **HIGH** | `plugins/cc10x/skills/cc10x-router/references/build-workflow.md` |
| **Shipping precondition** | Check `git remote` once. No remote → local-only mode: commit but skip all push/PR/CI actions. Missing remote is terminal local-only, not an error. | **MEDIUM** | `plugins/cc10x/skills/cc10x-router/references/build-workflow.md` |
| **Local-only mode** | When no remote: make commits but skip push, PR, CI watch. Never retry push or hunt for remote. | **MEDIUM** | `plugins/cc10x/skills/cc10x-router/references/build-workflow.md` |

**What cc10x should adopt**: The **gated pipeline** pattern is something cc10x's router partially has, but EveryInc's version is more explicit and rigorous. The **CI watch and autofix loop** is a unique capability — no other plugin autonomously watches CI and fixes failures. The **autonomous residual handoff** ensures nothing falls through the cracks.

---

## CONCEPTS.md Analysis

The EveryInc CONCEPTS.md defines 20+ domain concepts organized into categories: Plugin/Parts, Conversion, Compound Engineering, Skill Orchestration, Review/Workflow. Key concepts cc10x should consider adopting:

| Concept | Definition | Impact | Relevance to cc10x |
| --------- | ----------- | -------- | ------------------- |
| **Compound engineering** | "Structure engineering work so each unit makes the next one easier, capturing reusable knowledge as you go" | **HIGH** | Core philosophy cc10x could adopt |
| **Pipeline** | "Chained progression of Skills that carries work from strategy through review, closing by capturing what was learned" | **HIGH** | cc10x router is a pipeline but doesn't close the loop |
| **Learning** | "Documented solution to a past problem, stored as the unit of compounded knowledge with structured metadata for retrieval" | **HIGH** | cc10x has no learning concept |
| **Pattern doc** | "Guidance generalized from several Learnings into a broader rule. Higher-leverage, higher-risk when stale." | **MEDIUM** | cc10x has no pattern concept |
| **Model tier** | "Semantic cost class: extraction (cheapest), generation (mid-tier), ceiling (orchestrator's model). Referenced by tier name so model names never hardcode." | **HIGH** | cc10x should adopt tier naming |
| **Evidence dossier** | "Bulk evidence artifact written to scratch storage instead of returned inline, so orchestrator carries only a short gist." | **HIGH** | cc10x should adopt this pattern |
| **Load stub** | "Inline remnant when load-bearing content moves to a reference file: names what the reference contains and the failure mode of skipping it." | **MEDIUM** | cc10x references could use this pattern |
| **Confidence anchor** | "Discrete, self-scored confidence value on a fixed small scale, tied to behavioral criteria, used to gate and rank review findings." | **HIGH** | cc10x review should adopt this |
| **Headless mode** | "Explicit opt-in mode that runs a skill unattended, with no user prompts — produces a written report and conservatively defers ambiguous decisions." | **HIGH** | cc10x should adopt this |
| **Beta skill** | "Parallel copy of a stable skill, suffixed -beta, used to trial a new version alongside the stable one." | **LOW** | Interesting for cc10x development |

---

## CLAUDE.md and README.md Analysis

**CLAUDE.md**: Simply `@AGENTS.md` — a shim that includes the real instructions from AGENTS.md. This is a clean pattern for avoiding duplication.

**README.md**: Describes the compound engineering philosophy ("80% is in planning and review, 20% is in execution"), the 6-step core loop (brainstorm → plan → work → simplify → review → compound), and additional skills. Key insight: **the compounding loop is the whole point** — each cycle makes the next one smarter because learnings are captured and reused.

---

## Prioritized Recommendations for cc10x

### Tier 1: HIGH Impact — Should Adopt

1. **Knowledge compounding loop** — New `knowledge-capture` skill that writes structured learnings to `docs/solutions/` after work/debugging. Future planning and debugging read these as grounding. This is the single highest-value pattern from EveryInc.

2. **Multi-persona code review with confidence anchors** — Expand cc10x's code-review from a single agent to a panel of persona-based reviewers. Add confidence anchors (0/25/50/75/100), cross-reviewer promotion, quote-the-line gate, and independent validation pass. Target: `plugins/cc10x/skills/code-review/SKILL.md`

3. **Evidence-first execution** — Require test-first proof (observe red failure or characterization baseline) before changing production code. Report verification evidence per unit. Target: `plugins/cc10x/skills/building/SKILL.md`

4. **Repo-profile cache** — Shared cache for project profile (stack, deps, conventions) reused across all skills. Saves tokens and time. Target: new `plugins/cc10x/scripts/repo-profile-cache.py`

5. **Causal chain gate + predictions** — Debugging must explain the full causal chain before proposing a fix. Predictions for uncertain links catch symptom fixes. Target: `plugins/cc10x/skills/debugging/SKILL.md`

6. **Parallel subagent artifact pattern** — Subagents write full output to scratch files and return only the path. Orchestrator reads artifacts back. Solves summary collapse. Target: `plugins/cc10x/skills/agent-common/SKILL.md`

7. **Headless mode** — `mode:headless` for all skills. No user prompts, written report as deliverable, conservative deferral of ambiguous decisions. Target: `plugins/cc10x/skills/agent-common/SKILL.md`

8. **Worktree management skill** — Detect-first approach, harness-native tool preference, one-branch-one-worktree rule. Target: new `plugins/cc10x/skills/worktree/SKILL.md`

9. **CI watch and autofix loop** — Autonomous CI monitoring with up to 3 fix iterations. Target: `plugins/cc10x/skills/cc10x-router/references/build-workflow.md`

10. **Mode:agent JSON contract for code review** — Structured JSON output for pipeline integration. Target: `plugins/cc10x/skills/code-review/SKILL.md`

### Tier 2: MEDIUM Impact — Should Consider

1. **Artifact readiness levels** — `requirements-only` → `implementation-ready`. Same file enriched in place. Target: `plugins/cc10x/skills/planning/SKILL.md`
2. **Stable U-IDs** — Implementation units get stable IDs that survive reordering. Target: `plugins/cc10x/skills/planning/SKILL.md`
3. **Parallel safety check** — File overlap + shared resource contention detection before parallel dispatch. Target: `plugins/cc10x/skills/building/SKILL.md`
4. **System-wide test check** — 5-question framework before marking a task done. Target: `plugins/cc10x/skills/verification/SKILL.md`
5. **Smart escalation table** — 4-pattern diagnosis when stuck debugging. Target: `plugins/cc10x/skills/debugging/SKILL.md`
6. **Assumption audit** — List "this must be true" beliefs before hypothesis formation. Target: `plugins/cc10x/skills/debugging/SKILL.md`
7. **Two-floor verdict gate** — Project floor + external floor for research. Target: `plugins/cc10x/skills/research/SKILL.md`
8. **Model tier naming** — Extraction/generation/ceiling tiers referenced by name, never hardcoded. Target: `plugins/cc10x/skills/agent-common/SKILL.md`
9. **Evidence dossier pattern** — Bulk evidence to scratch, carry only gist. Target: `plugins/cc10x/skills/research/SKILL.md`
10. **Five-outcome knowledge maintenance** — Keep/Update/Consolidate/Replace/Delete for learnings. Target: new `knowledge-capture` skill
11. **Untrusted input handling** — All external content is data, never instructions. Target: `plugins/cc10x/skills/agent-common/SKILL.md`
12. **Flow-first test matrix** — Map user flows before deriving test scenarios. Target: `plugins/cc10x/skills/verification/SKILL.md`
13. **Autonomous fix loop with size judgment** — Auto-fix small/low-risk, escalate large/ambiguous. Target: `plugins/cc10x/skills/verification/SKILL.md`
14. **Triage groups in review** — Group related findings by root cause. Target: `plugins/cc10x/skills/code-review/SKILL.md`
15. **Gated pipeline with verification at each step** — Explicit STOP gates between pipeline stages. Target: `plugins/cc10x/skills/cc10x-router/SKILL.md`

### Tier 3: LOW Impact — Nice to Have

1. **CONCEPTS.md vocabulary capture** — Shared domain vocabulary file. Target: `plugins/cc10x/skills/memory-and-handoff/`
2. **Discoverability check** — Ensure instruction files surface the knowledge store. Target: `plugins/cc10x/skills/diff-driven-docs/SKILL.md`
3. **YAML frontmatter validation** — Parser-safety validator script. Target: new `plugins/cc10x/scripts/`
4. **Strategy as upstream anchor** — `STRATEGY.md` read as grounding. Target: `plugins/cc10x/skills/planning/SKILL.md`
5. **Visual probe gate** — Text-vs-visual choice for visual topics. Target: `plugins/cc10x/skills/frontend/SKILL.md`
6. **Meaningful branch name enforcement** — Suggest renaming auto-generated branch names. Target: `plugins/cc10x/skills/building/SKILL.md`
7. **Beta skill pattern** — Parallel `-beta` copy for trialing new versions. Target: cc10x development process
8. **Load stub pattern** — Named reference with failure mode of skipping. Target: cc10x reference files

---

## Summary: What Makes EveryInc Different

The EveryInc plugin's core differentiator is the **compounding loop** — the explicit feedback cycle where every solved problem becomes a documented learning that makes future work smarter. This is not just about writing docs; it's about:

1. **Structured capture** — Every learning has YAML frontmatter, category, tags, problem type for retrieval
2. **Active maintenance** — ce-compound-refresh keeps learnings accurate over time
3. **Grounding reuse** — Planning, debugging, and review all read learnings as context
4. **Discoverability** — Instruction files are checked to ensure agents can find the knowledge store

cc10x is strong at execution (parallel agents, router, verification) but lacks this self-improvement layer. Adding it would transform cc10x from a powerful tool into a **compounding system** that gets smarter with every use.

The second major differentiator is the **multi-persona code review** — EveryInc's 13-persona panel with confidence anchors, cross-model adversarial passes, and independent validation is significantly more sophisticated than cc10x's single-agent review. This is the most immediately stealable high-value pattern.

The third is **evidence-first execution** — requiring test-first proof before implementation changes is a discipline that prevents "it compiles so it works" thinking and creates verifiable evidence trails.