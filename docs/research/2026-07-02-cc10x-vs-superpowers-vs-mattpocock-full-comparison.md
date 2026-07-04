# cc10x vs Superpowers vs Matt Pocock — Full Comparison Findings

> **Date:** 2026-07-02
> **Method:** 10 parallel subagents, each read every file in all three projects
> **Purpose:** Ensure cc10x is the #1 harness for Claude Code by learning from the best

## Projects Compared

| Project | Location | Type | Files Analyzed |
| --------- | ---------- | ------ | ---------------- |
| **cc10x** | `/Users/rom.iluz/Dev/cc10x/` | Claude Code plugin (v12.2.0) | 17 skills, 9 agents, 9 hook scripts, 8 tools, router + 6 references |
| **Superpowers** | `/Users/rom.iluz/Dev/superpowers/` | Multi-harness plugin (v6.1.1) | 14 skills, hooks, tests, 9 harness manifests |
| **Matt Pocock** | `/Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/` | Skills repo | 15+ skills across engineering/productivity/personal categories |

## Final Score Card

| # | Dimension | cc10x | Superpowers | Matt Pocock | Winner |
| --- | ----------- | ------- | ------------- | ------------- | -------- |
| 1 | Orchestration & Routing | **9/10** | 6/10 | 3/10 | cc10x |
| 2 | Skill Design & Format | 7.5/10 | **8/10** | 7/10 | Superpowers |
| 3 | TDD & Testing | **8.5/10** | 7.5/10 | 6.5/10 | cc10x |
| 4 | Debugging | **8.5/10** | 7.5/10 | 7/10 | cc10x |
| 5 | Code Review | **8.5/10** | 6.5/10 | 5.5/10 | cc10x |
| 6 | Planning & Architecture | **8.5/10** | 7/10 | 7.5/10 | cc10x |
| 7 | Memory & Handoff | **8.5/10** | 5/10 | 3/10 | cc10x |
| 8 | Hooks & Enforcement | **9/10** | 2/10 | 4/10 | cc10x |
| 9 | Agent Architecture | **8.5/10** | 7/10 | 5.5/10 | cc10x |
| 10 | DX & Ecosystem | 7.5/10 | **8.5/10** | 5.5/10 | Superpowers |
| | **OVERALL** | **8.35** | **6.55** | **5.15** | **cc10x** |

## Where cc10x Already Wins Decisively

### Orchestration (9/10)

- Router kernel with priority-matched intent routing table (5 workflows)
- Deterministic agent dispatcher with 9 named agents
- Full DAG via `blockedBy` + workflow artifact (40+ field JSON state machine)
- Parallel read-only agents (reviewer ‖ hunter) + DEBUG fan-out with independence test
- 10-layer fallback system (circuit breaker, change-before-re-dispatch, inline mode, model escalation, scope escalation, REVERT gate, FINDING_DISPUTED, parallel fallback, research backend fallback, contract override)
- Per-role model-tier policy with reviewer floor
- Machine-readable agent contracts with override conditions
- Anti-anchoring dispatch rules with self-check blocklist
- Hook policy with block-mode artifact integrity guard
- Telemetry, convergence tracking, traceability, deferred findings
- Resume & hydration with stop-state hints and scope-decision markers
- BUILD-DONE finishing with merge-then-cleanup invariant and git-guard tokens

### Hooks & Enforcement (9/10)

- 9 hook event types covering entire agent lifecycle
- Configurable audit/block modes per enforcement category
- Approval token system with expiry and single-use consumption
- Multi-layer artifact validation (12 required keys, event logs, freshness)
- Auto-remediation for missed event log entries
- Comprehensive structured logging (JSONL)
- State persistence for compaction/session resume
- Shared hooklib for DRY enforcement logic
- **Gap:** Missing `git restore .` pattern (Matt Pocock catches this)

### Memory & Handoff (8.5/10)

- 3-file persistent memory (activeContext, patterns, progress) with ownership separation
- Workflow artifacts (JSON) + event logs (JSONL)
- Multi-layered compaction defense (PreCompact snapshot, memory files, SessionStart injection, rubric)
- Auto-heal contracts (missing sections inserted automatically)
- Structured MEMORY_NOTES protocol (machine-parseable)
- Secret redaction protocol
- Context budget monitoring with degradation tiers
- **Gap:** No file-based subagent handoffs, no per-dispatch model selection, no compact progress ledger

### Agent Architecture (8.5/10)

- 9 specialized agents with enforced tool boundaries (READ-ONLY vs mutation)
- Machine-readable router contracts with boolean contract rules
- Deep anti-anchoring patterns (forbidden memory files, verdict-before-prose, claim extraction)
- Parallel agent dispatch (code-reviewer + silent-failure-hunter)
- Multi-signal scoring with HARD/SOFT dimensions
- Comprehensive verification gates (test honesty, proof reconciliation, zero-finding gate)
- **Gap:** No per-dispatch model selection, no file-based context handoffs

## Where cc10x Has Gaps — The 23 Patterns to Adopt

### Tier 1: High-Impact (Do Now)

| # | Pattern | Source | What It Does | Target File in cc10x |
| --- | --------- | -------- | ------------- | ---------------------- |
| 1 | **Rationalization tables** | Superpowers | Maps common excuses to reality checks. E.g., "Too simple to test" → "Simple code breaks. Test takes 30 seconds." 11 entries in TDD skill, 8 in verification, 8 in debugging. | `building/SKILL.md`, `verification/SKILL.md`, `debugging/SKILL.md` |
| 2 | **Red flags / STOP lists** | Superpowers | Explicit thoughts that mean "stop and reconsider." 13 signals in TDD, 8 in debugging, 8 in verification. Creates cognitive friction at moments of weakness. | `building/SKILL.md`, `debugging/SKILL.md`, `verification/SKILL.md` |
| 3 | **Spirit-vs-letter principle** | Superpowers | "Violating the letter of the rules is violating the spirit of the rules." Single sentence cuts off entire class of meta-rationalizations. | `agent-common/SKILL.md` (shared preamble) |
| 4 | **Deep-module vocabulary + deletion test + two-adapter rule** | Matt Pocock | Precise architecture language: module, interface, seam, adapter, depth, leverage, locality. Deletion test: "Imagine deleting the module. If complexity vanishes, it was a pass-through." Two-adapter rule: "One adapter = hypothetical seam. Two = real." | `architecture/SKILL.md` |
| 5 | **Repro minimisation + 3-5 ranked hypotheses** | Matt Pocock | After reproducing, shrink to smallest red scenario before hypothesizing. Generate 3-5 ranked hypotheses before testing any — prevents anchoring on first plausible idea. | `debugging/SKILL.md`, `agents/bug-investigator.md` |
| 6 | **Tautological test anti-pattern** | Matt Pocock | Tests where assertion recomputes expected value the way code does — passes by construction, can never disagree. "Expected values must come from an independent source of truth." | `building/SKILL.md` or `building/references/testing-patterns.md` |
| 7 | **12 named Fowler code smells** | Matt Pocock | Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. Each with "what it is → how to fix." | `code-review/SKILL.md` or `code-review/references/code-review-heuristics.md` |
| 8 | **SDK-style interfaces for mockability** | Matt Pocock | Specific functions per external operation vs one generic fetcher. Each mock returns one specific shape, no conditional logic in test setup, type safety per endpoint. | `building/references/test-data-and-mocks.md` |
| 9 | **`git restore .` in blocked patterns** | Matt Pocock | Same destructive effect as `git checkout .` — cc10x blocks `git checkout .` but misses `git restore .` | `scripts/cc10x_git_guard.py` |
| 10 | **Pressure tests for debugging** | Superpowers | 3 scenarios validating gates hold under: (1) production outage ($15k/min), (2) sunk cost (4 hours, 8pm), (3) authority pressure (senior engineer + tech lead). | `debugging/SKILL.md` or new `debugging/evals/` directory |

### Tier 2: Medium-Impact (Do Later)

| # | Pattern | Source | What It Does | Target File in cc10x |
| --- | --------- | -------- | ------------- | ---------------------- |
| 11 | **Per-dispatch model selection** | Superpowers | Match model capability to task complexity (cheap for mechanical, standard for integration, capable for architecture). "Turn count beats token price." | Router SKILL.md §7 dispatcher table |
| 12 | **Regression test verification pattern** | Superpowers | Write → pass → revert fix → MUST FAIL → restore → pass. Concrete bug-fix verification protocol. | `verification/SKILL.md` or `debugging/SKILL.md` |
| 13 | **Out-of-scope/rejected-approaches KB** | Matt Pocock | Persistent records of rejected approaches with concept-based dedup. Prevents re-litigating settled architectural decisions. | New: `.cc10x/rejected-approaches/` or section in `patterns.md` |
| 14 | **File-based context handoffs** | Superpowers | Brief files, report files, diff packages — everything moves as files, not pasted text. Reduces controller context pollution. | Router SKILL.md §7 dispatch protocol |
| 15 | **Durable progress ledger** | Superpowers | One-line-per-task with commit SHAs for fast post-compaction scanning. "Trust the ledger and git log over recollection." | `memory-and-handoff/SKILL.md` or new compact ledger format |
| 16 | **Pre-flight plan conflict scan** | Superpowers | Scan plan once before Task 1 for inter-task conflicts. Present as batched question. | Router SKILL.md §5 or `planning/SKILL.md` |
| 17 | **CONTEXT.md domain glossary** | Matt Pocock | Persistent domain language file across sessions. "Use the project's domain glossary vocabulary." | New: `patterns.md` section or separate `CONTEXT.md` concept |
| 18 | **Design It Twice** | Matt Pocock | Spawn 3+ parallel sub-agents with different design constraints (minimize interface, maximize flexibility, optimize common case). Compare on depth, locality, seam placement. | `exploration/SKILL.md` or `architecture/SKILL.md` |
| 19 | **Forbidden performative responses** | Superpowers | Ban "Great point!", "Excellent!", "You're absolutely right!" in review feedback. cc10x bans verdict-softeners but not social sycophancy. | `code-review/SKILL.md` receiving-review mode |
| 20 | **Condition-based waiting pattern** | Superpowers | Replace arbitrary timeouts with condition polling. Complete TypeScript implementation. | `debugging/SKILL.md` or new reference file |
| 21 | **Find-polluter bisection script** | Superpowers | Run tests one-by-one to find which test creates pollution. Practical tool for test-pollution bugs. | `debugging/SKILL.md` or new reference file |
| 22 | **Completion criteria as checkboxes** | Matt Pocock | Observable, scannable phase boundaries with checkboxes instead of prose gates. | All skills with gates |
| 23 | **Automated eval runner** | Superpowers | Drill harness with 10 test directories for systematic skill testing. cc10x has 3 manual evals, no runner. | New: `plugins/cc10x/skills/*/evals/` with runner script |

## Dimension-by-Dimension Detail

### 1. Orchestration & Routing (cc10x: 9, Superpowers: 6, Matt Pocock: 3)

**cc10x unique patterns:**

- Router kernel as sole entry point
- Durable workflow artifact (40+ field JSON)
- Event log (JSONL audit trail)
- Workflow UUID system
- Task metadata contract (7 mandatory fields)
- Resume & hydration
- Intent Readiness Gate, Plan Trust Gate, Phase Exit Gate
- Complexity gradient (trivial vs standard)
- Circuit breaker + change-before-re-dispatch
- FINDING_DISPUTED adjudication
- Deferred findings roll-up
- Telemetry + convergence tracking

**Patterns to adopt from others:**

- Vertical-slice decomposition (Matt Pocock) — tracer bullets cutting all layers
- Out-of-scope KB (Matt Pocock) — institutional memory for rejected ideas
- Pre-flight plan conflict scan (Superpowers) — batch conflicts before execution
- Continuous execution mandate (Superpowers) — "do not pause between tasks"

### 2. Skill Design & Format (cc10x: 7.5, Superpowers: 8, Matt Pocock: 7)

**cc10x unique patterns:**

- `allowed-tools` frontmatter (blast-radius control)
- Centralized router activation model
- `user-invocable: false` flag
- CONTRACT envelope (machine-readable output)
- Workflow artifacts
- Eval scenarios shipped with skills
- `<!-- scar -->` comments (failure origin documentation)
- Explicit leading words vocabulary table
- Anti-anchoring protocol
- Model-tier policy
- Two-mode skills (code-review, frontend, exploration, etc.)

**Patterns to adopt from others:**

- Rationalization tables (Superpowers) — every discipline skill has one
- Red Flags / STOP lists (Superpowers) — terminal self-checks
- Spirit-vs-letter principle (Superpowers) — meta-rationalization defense
- TDD for skills (Superpowers) — test before writing, document failures, write to address them
- "Use when…" description format (Superpowers) — pure triggers
- `disable-model-invocation` as first-class concept (Matt Pocock)
- Completion criteria as checkboxes (Matt Pocock) — observable, scannable
- Leading words as formal concept / Leitwort (Matt Pocock)
- Information hierarchy (Matt Pocock) — 3-rung ladder for what goes where
- No-op test (Matt Pocock) — prune lines the model already obeys
- Glossary as disclosed reference (Matt Pocock)

### 3. TDD & Testing (cc10x: 8.5, Superpowers: 7.5, Matt Pocock: 6.5)

**cc10x unique patterns:**

- Contract-enforced TDD gates (`TDD_RED_EXIT=1`, `TDD_RED_REASON_KIND=behavioral`, `TDD_GREEN_EXIT=0`)
- False-RED classification (behavioral vs import/syntax error)
- Loop caps (3-strike GREEN failure → FAIL)
- Scope escalation (`SCOPE_INCREASES` with decision checkpoints)
- Evidence array protocol (mandatory structured format)
- Self-critique gate (pre-verification checklist)
- Validation levels (4 types: deterministic, probabilistic, manual, live)
- Goal-backward lens (4-step backward walk)
- Live/production proof harness
- Auditor posture
- Near-miss negative tests
- Coverage threshold

**Patterns to adopt from others:**

- Anti-rationalization toolkit (Superpowers) — 11 rationalizations, 13 red flags
- Good/Bad inline examples (Superpowers, Matt Pocock) — examples in SKILL.md, not just references
- Tautological test anti-pattern (Matt Pocock) — tests that re-implement code
- Pre-agreed seams with user confirmation (Matt Pocock)
- CONTEXT.md / ADR awareness (Matt Pocock)
- SDK-style interfaces for mockability (Matt Pocock)
- Regression test verification pattern (Superpowers) — write → pass → revert → fail → restore → pass
- Gate functions for anti-patterns (Superpowers) — structured IF/THEN decisions
- "Why Order Matters" section (Superpowers) — philosophical foundation
- Visual diagram of TDD cycle (Superpowers) — DOT graph

### 4. Debugging (cc10x: 8.5, Superpowers: 7.5, Matt Pocock: 7)

**cc10x unique patterns:**

- LSP-powered root cause tracing (Go to Definition, Find References, Hover)
- Machine-readable router contract (25+ field YAML)
- Contract rules (STATUS=FIXED requires TDD_RED_EXIT=1, etc.)
- Multi-agent fan-out with independence test + fan-in conflict check
- Hypothesis confidence scoring (0-100)
- Anti-hardcode gate (variant dependencies)
- Scenario playbooks (8 scenarios)
- Self-managed research integration
- Investigation hygiene reference
- Debug close-out protocol

**Patterns to adopt from others:**

- Pressure tests (Superpowers) — 3 scenarios for outage/sunk-cost/authority
- Anti-rationalization catalog (Superpowers) — "Emergency, no time" → "Systematic is FASTER"
- Red Flags section (Superpowers) — "Quick fix for now", "Just try changing X"
- "Systematic is Faster" framing (Superpowers) — 15-30 min vs 2-3 hours, 95% vs 40%
- Defense-in-depth code examples (Superpowers) — concrete TypeScript per layer
- Find-polluter script (Superpowers) — bisection for test pollution
- Condition-based waiting (Superpowers) — replace arbitrary timeouts
- 3-fix architectural escalation (Superpowers) — question architecture, not just implementation
- Repro minimisation (Matt Pocock) — shrink to smallest red scenario
- 3-5 ranked hypotheses before testing (Matt Pocock) — anti-anchoring
- User as domain knowledge checkpoint (Matt Pocock) — show hypotheses before testing
- Perf branch (Matt Pocock) — separate track for performance regressions
- HITL loop template (Matt Pocock) — structured bash for human-in-the-loop

### 5. Code Review (cc10x: 8.5, Superpowers: 6.5, Matt Pocock: 5.5)

**cc10x unique patterns:**

- Silent failure hunter (dedicated parallel agent)
- Plan validity pass (separate plan defects from code defects)
- Spec compliance as first-class independent gate
- CANNOT_VERIFY_CROSS_PHASE mechanism
- Quantitative confidence scoring (0-100, HARD/SOFT)
- Zero-finding gate (must produce positive assertions)
- Anti-anchoring protocol (forbidden memory files)
- Memory-first protocol (patterns.md + progress.md)
- Friction scan with quantitative thresholds
- Security stop (any pass → CRITICAL)
- Verdict-before-response rule
- Forbidden verdict-softeners
- Self-grading downgrade prevention
- Scope guard (>10 files → preliminary verdict)

**Patterns to adopt from others:**

- Forbidden performative responses (Superpowers) — ban "Great point!", "Excellent!"
- Source-specific handling (Superpowers) — trusted human vs skeptical external
- Graceful correction protocol (Superpowers) — state factually, move on
- Implementation order for multi-item feedback (Superpowers) — clarify → blocking → simple → complex
- Fowler code smells baseline (Matt Pocock) — 12 named smells
- Repo-overrides-baseline rule (Matt Pocock)
- Strict word limit on sub-agent reports (Matt Pocock) — 400 words
- Three-dot diff for merge-base (Matt Pocock) — `git diff <fixed-point>...HEAD`
- Pre-flight validation (Matt Pocock) — confirm diff non-empty before spawning agents

### 6. Planning & Architecture (cc10x: 8.5, Superpowers: 7, Matt Pocock: 7.5)

**cc10x unique patterns:**

- Tri-mode planning (direct / execution_plan / decision_rfc)
- Verification rigor levels (standard / critical_path)
- Fresh-review DAG with anti-anchoring
- Plan review gate (3-check adversarial, fail-closed)
- Consumes/Produces typed contract graph
- Autonomy classification (AFK / HITL)
- Machine-readable router contract
- Risk-based testing matrix
- Functionality flow mapping
- Durability-horizon rule
- Test-seam selection discipline
- Prefactor question
- Scar records
- Agreement-first protocol
- LSP-powered architecture analysis
- Dependency classification (Owned/Wrapped/Consumed/Infra)

**Patterns to adopt from others:**

- Deep-module vocabulary (Matt Pocock) — module, interface, seam, adapter, depth, leverage, locality
- Deletion test (Matt Pocock) — "Imagine deleting the module"
- Two-adapter rule (Matt Pocock) — "One = hypothetical, two = real"
- Design It Twice (Matt Pocock) — 3+ parallel sub-agents with different constraints
- Dependency-category testing strategy (Matt Pocock) — in-process, local-substitutable, remote-but-owned, true-external
- Minimal ADR format with qualification gates (Matt Pocock) — hard to reverse, surprising, real trade-off
- CONTEXT.md domain glossary (Matt Pocock)
- HTML architecture reports (Matt Pocock) — visual before/after diagrams
- Complete code in every plan step (Superpowers)
- No-placeholders catalog (Superpowers) — explicit forbidden patterns list
- User review gate on spec (Superpowers)
- Visual companion for brainstorming (Superpowers)
- Grilling loop for architecture candidates (Matt Pocock)

### 7. Memory & Handoff (cc10x: 8.5, Superpowers: 5, Matt Pocock: 3)

**cc10x unique patterns:**

- Multi-surface memory with ownership separation
- Structured MEMORY_NOTES protocol
- Compaction KEEP/SUMMARIZE/DROP rubric
- Context budget degradation tiers
- PreCompact + Stop state snapshots
- Workflow artifacts + event logs
- Auto-heal memory contracts
- Promotion ladder
- Secret redaction protocol
- Router Contract envelope
- Hook event log
- Defensive hook design

**Patterns to adopt from others:**

- File-based subagent handoffs (Superpowers) — brief files, report files, diff packages
- Progress ledger as recovery map (Superpowers) — one-line-per-task with commit SHAs
- Model selection per task (Superpowers)
- Background agent launch (Matt Pocock) — `claude --bg --name "..." "<summary>"`
- Plan-to-execution handoff header (Superpowers) — explicit "REQUIRED SUB-SKILL" header
- Pre-flight plan conflict scan (Superpowers)
- Worktree provenance check (Superpowers)

### 8. Hooks & Enforcement (cc10x: 9, Superpowers: 2, Matt Pocock: 4)

**cc10x unique patterns:**

- 9 hook event types
- Configurable audit/block modes
- Approval token system (single-use, time-limited)
- PostToolUse artifact integrity validation (12 required keys)
- TaskCompleted metadata validation (7 fields)
- Memory task finalization validation
- Artifact freshness detection
- Auto-remediation (event log auto-append)
- SubagentStop contract audit
- PreCompact state snapshot
- Stop state persistence
- InstructionsLoaded audit
- Structured event logging (JSONL)
- Scope discipline in PostToolUse
- SessionStart workflow context injection
- Shared hooklib module

**Patterns to adopt from others:**

- `git restore .` blocking (Matt Pocock) — cc10x misses this
- Pre-commit hooks / Husky (Matt Pocock) — commit-time enforcement
- Cross-platform hook wrapper (Superpowers) — polyglot for Windows

### 9. Agent Architecture (cc10x: 8.5, Superpowers: 7, Matt Pocock: 5.5)

**cc10x unique patterns:**

- Machine-readable router contracts (YAML)
- Contract rules (boolean conditions gating STATUS)
- Parallel agent dispatch (reviewer + hunter)
- Tool allowlists per agent (READ-ONLY enforced)
- Skills dependencies per agent
- Feedback loop gate (10-rung ladder)
- Boundary instrumentation matrix
- Test honesty gates (7 grep-based)
- Proof reconciliation (truths + artifacts + wiring)
- PLAN_DEFECT routing
- Multi-signal scoring (HARD/SOFT)
- Zero-finding gate
- Debug attempt tracking with cap
- BUILD_PREFLIGHT token
- Variant scan
- Effort levels in frontmatter
- Color coding

**Patterns to adopt from others:**

- Per-dispatch model selection (Superpowers) — cheap/standard/capable per task
- File-based context handoffs (Superpowers)
- Durable real-time progress ledger (Superpowers)
- "Never dispatch without a diff file" (Superpowers)
- Anti-pre-judging in dispatch prompts (Superpowers)
- ONE fix subagent for all findings (Superpowers)
- Out-of-scope KB (Matt Pocock)
- Redundancy check before planning (Matt Pocock)
- Durability over precision in specs (Matt Pocock) — interfaces not paths

### 10. DX & Ecosystem (cc10x: 7.5, Superpowers: 8.5, Matt Pocock: 5.5)

**cc10x unique patterns:**

- Setup wizard with installed-skill scanning
- Safe-update skill with patch rebasing
- Version-sync validator
- Pain-to-solution marketing table
- Workflow-state-on-disk with UUIDs
- Fail-closed hook enforcement
- Complexity gradient
- `.cc10x/` namespace outside `.claude/`

**Patterns to adopt from others:**

- Automated eval runner / drill harness (Superpowers)
- Contributor guidelines for AI agents (Superpowers) — 94% PR rejection warning
- Per-harness tool-mapping references (Superpowers)
- Telemetry opt-out (Superpowers)
- Discord community + release announcements (Superpowers)
- Porting guide for new harnesses (Superpowers)
- Per-repo interactive setup with explainers (Matt Pocock)
- Issue tracker integration (Matt Pocock)
- Domain modeling (CONTEXT.md + ADRs) (Matt Pocock)

## Key Artifacts

All 10 subagent reports are at:

- `/Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/94c57dfa_scout_{0-4}_output.md` (batch 1: dimensions 1-5)
- `/Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/cf3397b3_scout_{0-4}_output.md` (batch 2: dimensions 6-10)

## Current cc10x State

- **Version:** 12.2.0
- **Agents:** 9 (planner, bug-investigator, component-builder, code-reviewer, silent-failure-hunter, integration-verifier, doc-syncer, plan-gap-reviewer, researcher)
- **Skills:** 17
- **Hook scripts:** 9
- **Router:** 750+ lines (the orchestration brain)
- **Repo:** <https://github.com/romiluz13/cc10x>
- **Branch:** main
- **Latest commit:** `0e1b305` (parallel review restoration)

## Constraint Reminder

- **Claude Code only** — don't adopt multi-platform patterns that would dilute the Claude Code focus
- **Zero quality regression** — every adoption must be additive, not destructive
- **Orchestration is #1** — never weaken the router to add a pattern
- **Agent colors must be preserved**
- **No Fable 5 mentions**
