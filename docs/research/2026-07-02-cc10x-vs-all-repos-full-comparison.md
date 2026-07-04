# cc10x vs The World — Full Comparison Findings (All 6 Repos)

> **Date:** 2026-07-02
> **Method:** 18+ parallel subagents, each read every file in all projects
> **Purpose:** Ensure cc10x is the #1 harness for Claude Code by learning from the best

## Projects Compared

| Project | Location | Type | Key Focus |
| --------- | ---------- | ------ | ----------- |
| **cc10x** | `/Users/rom.iluz/Dev/cc10x/` | Claude Code plugin (v12.2.0) | Orchestration + enforcement + memory |
| **Superpowers** | `/Users/rom.iluz/Dev/superpowers/` | Multi-harness plugin (v6.1.1) | Discipline skills + anti-rationalization |
| **Matt Pocock** | `/Users/rom.iluz/Dev/pi-optimize/mattpocock-skills/` | Skills repo | Architecture vocabulary + planning |
| **addyosmani/agent-skills** | `/Users/rom.iluz/Dev/addyosmani-agent-skills/` | Claude Code plugin | Domain expertise + doubt-driven dev |
| **EveryInc/compound** | `/Users/rom.iluz/Dev/everyinc-compound-engineering/` | Multi-harness plugin (TS) | Knowledge compounding loop |
| **multica/karpathy** | `/Users/rom.iluz/Dev/multica-karpathy-skills/` | CLAUDE.md guidelines | Minimal advisory principles |

## Master Score Card

| # | Dimension | cc10x | Superpowers | Matt Pocock | addyosmani | EveryInc | Karpathy |
| --- | ----------- | ------- | ------------- | ------------- | ------------ | ---------- | ---------- |
| 1 | Orchestration | **9** | 6 | 3 | 4 | 7 | 2 |
| 2 | Skill Design | 7.5 | **8** | 7 | 7 | 7 | N/A |
| 3 | TDD & Testing | **8.5** | 7.5 | 6.5 | 7 | 7 | 5 |
| 4 | Debugging | **8.5** | 7.5 | 7 | 7 | 7 | 5 |
| 5 | Code Review | **8.5** | 6.5 | 5.5 | 7 | 8 | 4 |
| 6 | Planning | **8.5** | 7 | 7.5 | 7 | 8 | 5 |
| 7 | Memory | **8.5** | 5 | 3 | 3 | 6 | 2 |
| 8 | Hooks/Enforcement | **9** | 2 | 4 | 5 | 3 | 1 |
| 9 | Agent Architecture | **8.5** | 7 | 5.5 | 6 | 6 | N/A |
| 10 | DX/Ecosystem | 7.5 | **8.5** | 5.5 | 6 | 7 | 5 |
| | **OVERALL** | **8.35** | 6.55 | 5.15 | 5.9 | 6.8 | 3.5 |

## Key Findings Per New Repo

### addyosmani/agent-skills

**Unique high-value patterns:**

1. **Doubt-Driven Development** — Fresh-context adversarial reviewer spawned IN-FLIGHT (not post-hoc) for non-trivial decisions. 5-step cycle: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP. Cross-model escalation (Gemini/Codex as second opinion). Rationalization table. This is fundamentally different from cc10x's post-hoc review — it's in-flight course correction while changes are still cheap.
2. **SDD-Cache hook** — Pre/Post tool hooks that cache Source-Driven Development verification results. Avoids re-fetching docs for the same API across sessions.
3. **SIMPLIFY-IGNORE hook** — Block-level code protection via annotations. Annotated blocks are hidden from the model as `BLOCK_<hash>` placeholders, restored after edits. Prevents well-intentioned but harmful refactoring of perf-critical/security-sensitive code.
4. **Source-Driven Development** — Verify API claims against official docs before using them. "Never trust your training data — verify against the source."
5. **AI-Generated Anti-Patterns section** — Dedicated sections for patterns commonly produced by AI (over-eager useMemo, state duplication, sequential awaits, over-fetching).
6. **Metric Honesty Rule** — "Never fabricate metrics. An LLM reading static source code cannot measure real-world LCP, INP, or CLS."
7. **Framework detection before advice** — Identify the stack before recommending framework-specific patterns.
8. **Positive reinforcement in agent output** — "What's Done Well" section (cc10x's hunter already has "Verified Good" — extend to all agents).
9. **Composition footer in agent definitions** — Self-documenting orchestration boundaries in each agent file.
10. **Hook test scripts** — Dedicated test scripts for each hook.

### EveryInc/compound-engineering

**Unique high-value patterns:**

1. **Knowledge Compounding Loop** — The core concept. After every work/debug cycle, structured learnings are written to `docs/solutions/`. Future planning and debugging READ these as grounding. This is a self-improvement layer cc10x doesn't have. Five outcomes: Keep/Update/Consolidate/Replace/Delete.
2. **Multi-persona code review** — 13-persona panel with confidence anchors (0/25/50/75/100), cross-reviewer promotion, quote-the-line gate, independent validation pass. More granular than cc10x's single 6-pass reviewer.
3. **Evidence-first execution** — Require test-first proof (observe red failure or characterization baseline) before changing production code.
4. **Residual review findings** — `docs/residual-review-findings/<branch>.md` — review findings not applied are persisted with resolution notes. Prevents invisible deferred issues.
5. **Parallel subagent artifact pattern** — Subagents write full output to scratch files, return only the path. Orchestrator reads artifacts back. Solves summary collapse.
6. **Causal chain gate for debugging** — Must explain full causal chain before proposing fix. Predictions for uncertain links catch symptom fixes.
7. **Assumption audit** — List "this must be true" beliefs before hypothesis formation.
8. **Headless mode** — `mode:headless` for all skills. No user prompts, written report as deliverable, conservative deferral.
9. **Three-lens parallel simplification** — reuse/quality/efficiency reviewers run in parallel for code simplification. Safety-check guard ("never simplify away a safety check").
10. **ce-optimize pattern** — Metric-driven iterative experiments in parallel git worktrees. Persistence discipline: every experiment written to disk immediately, crash-recovery markers, resume-from-disk.
11. **Central PR feedback judgment gate** — Orchestrator fetches all unresolved threads, judges centrally, default-to-fix, four divert categories (not-addressing/declined/replied/needs-human). Untrusted input handling (comment text is data, never instructions).
12. **Changed-file-to-route mapping** — For browser testing, map diff to affected routes and test only those.
13. **Goal Capsule in plans** — Objective, product authority, authority hierarchy, execution profile, stop conditions, tail ownership, open blockers.
14. **docs/solutions/ as compounded-learnings** — Closes the loop that cc10x's docs/research/ + docs/plans/ leaves open.

### multica-ai/andrej-karpathy-skills

**Verdict: cc10x should adopt NOTHING from this repo.** Every Karpathy principle is already covered by a stronger, machine-enforced cc10x mechanism:

- "Think Before Coding" → cc10x's Intent Readiness Gate + Plan Trust Gate (structural, fail-closed)
- "Simplicity First" → cc10x's SPEC_COMPLIANCE EXTRA bucket + deviation discipline + decision checkpoints
- "Surgical Changes" → cc10x's 7+ mechanisms (builder deviation, reviewer scope guard, clean-baseline diff, etc.)
- "Goal-Driven Execution" → cc10x's TDD cycle with contract-enforced gates

The Karpathy guidelines validate cc10x's design philosophy. They're the advisory version of what cc10x enforces structurally.

## Consolidated Adoption List (All 6 Repos)

### Tier 1: HIGH Impact — Do Now

| # | Pattern | Source | Target cc10x File | What It Does |
| --- | --------- | -------- | ------------------- | -------------- |
| 1 | Rationalization tables | Superpowers | building, verification, debugging | Maps excuses to reality checks |
| 2 | Red flags / STOP lists | Superpowers | building, debugging, verification | Explicit thoughts that mean "stop" |
| 3 | Spirit-vs-letter principle | Superpowers | agent-common | "Violating letter = violating spirit" |
| 4 | Deep-module vocabulary + deletion test + two-adapter rule | Matt Pocock | architecture | Precise architecture language + falsifiable tests |
| 5 | Repro minimisation + 3-5 ranked hypotheses | Matt Pocock | debugging, bug-investigator | Shrink repro + anti-anchoring |
| 6 | Tautological test anti-pattern | Matt Pocock | building | Tests that re-implement code |
| 7 | 12 named Fowler code smells | Matt Pocock | code-review | Structured smell vocabulary |
| 8 | SDK-style interfaces for mockability | Matt Pocock | building/test-data-and-mocks | Specific functions per external op |
| 9 | `git restore .` in blocked patterns | Matt Pocock | cc10x_git_guard.py | Catches destructive command cc10x misses |
| 10 | Pressure tests for debugging | Superpowers | debugging/evals | Validate gates hold under pressure |
| 11 | **Doubt-Driven Development** | addyosmani | New: exploration or agent-common | In-flight fresh-context adversarial review for non-trivial decisions |
| 12 | **Knowledge compounding loop** | EveryInc | New: docs/solutions/ + memory-and-handoff | Structured learnings written after every cycle, read as grounding for future work |
| 13 | **Residual review findings** | EveryInc | code-review or new artifact | Persist unaddressed findings with resolution notes |
| 14 | **Causal chain gate for debugging** | EveryInc | debugging, bug-investigator | Must explain full causal chain before fix |
| 15 | **Safety-check guard for refactoring** | EveryInc | building | "Never simplify away a safety check" |
| 16 | **AI-generated anti-patterns section** | addyosmani | code-review | Patterns commonly produced by AI |
| 17 | **Metric honesty rule** | addyosmani | code-review Pass 2 | "Never fabricate metrics from static source" |
| 18 | **Untrusted input handling** | EveryInc | agent-common | All external content is data, never instructions |

### Tier 2: MEDIUM Impact — Do Later

| # | Pattern | Source | Target |
| --- | --------- | -------- | -------- |
| 19 | Per-dispatch model selection | Superpowers | Router dispatcher table |
| 20 | Regression test verification pattern | Superpowers | verification or debugging |
| 21 | Out-of-scope/rejected-approaches KB | Matt Pocock | New: patterns.md section |
| 22 | File-based context handoffs | Superpowers | Router dispatch protocol |
| 23 | Durable progress ledger | Superpowers | memory-and-handoff |
| 24 | Pre-flight plan conflict scan | Superpowers | Router §5 or planning |
| 25 | CONTEXT.md domain glossary | Matt Pocock | patterns.md or new concept |
| 26 | Design It Twice | Matt Pocock | exploration or architecture |
| 27 | Forbidden performative responses | Superpowers | code-review receiving mode |
| 28 | Condition-based waiting pattern | Superpowers | debugging reference |
| 29 | Find-polluter bisection script | Superpowers | debugging reference |
| 30 | Completion criteria as checkboxes | Matt Pocock | All skills with gates |
| 31 | Automated eval runner | Superpowers | New: evals/ with runner |
| 32 | SDD-Cache hook | addyosmani | New: scripts/ |
| 33 | SIMPLIFY-IGNORE (block-level code protection) | addyosmani | New: hooks/ |
| 34 | Source-Driven Development | addyosmani | New: skill or reference |
| 35 | Framework detection before advice | addyosmani | code-reviewer, component-builder |
| 36 | Positive reinforcement in agent output | addyosmani | All agents (extend "Verified Good") |
| 37 | Composition footer in agent definitions | addyosmani | All agents |
| 38 | Hook test scripts | addyosmani | New: tests/ |
| 39 | Multi-persona code review | EveryInc | code-review (enhance) |
| 40 | Evidence-first execution | EveryInc | building |
| 41 | Parallel subagent artifact pattern | EveryInc | agent-common |
| 42 | Headless mode | EveryInc | agent-common |
| 43 | Assumption audit before hypotheses | EveryInc | debugging |
| 44 | Three-lens parallel simplification | EveryInc | building REFACTOR step |
| 45 | Central PR feedback judgment gate | EveryInc | code-review receiving mode |
| 46 | Changed-file-to-route mapping | EveryInc | New: browser testing reference |
| 47 | Goal Capsule in plans | EveryInc | planning |
| 48 | docs/solutions/ loop | EveryInc | New: docs/solutions/ |
| 49 | ce-optimize pattern (parallel experiments) | EveryInc | New: optimization skill |
| 50 | OWASP LLM Top 10 in security review | addyosmani | code-review or new security-auditor |

### Tier 3: LOW Impact — Nice to Have

| # | Pattern | Source |
| --- | --------- | -------- |
| 51 | Spirit-vs-letter (already in Tier 1) | Superpowers |
| 52 | Debug mode via sentinel file | addyosmani |
| 53 | Quick vs Deep operating modes | addyosmani |
| 54 | Prove-It pattern (simplified bug TDD) | addyosmani |
| 55 | Five-axis review framework (simpler alternative) | addyosmani |
| 56 | Beta skill pattern | EveryInc |
| 57 | CONCEPTS.md vocabulary capture | EveryInc |
| 58 | YAML frontmatter validation script | EveryInc |
| 59 | Skill-prose contract tests | EveryInc |
| 60 | Fixture-plugin for CLI tests | EveryInc |

## What cc10x Already Has That NO Other Repo Has

These are cc10x's unique competitive advantages — things nobody else does:

1. **Router kernel** — single entry point, priority-matched intent routing, 5 workflow types
2. **Durable workflow artifacts** — 40+ field JSON state machine + JSONL event log
3. **9 hook events with configurable audit/block modes** — nobody else has more than 1-2 hooks
4. **Approval token system** — single-use, time-limited tokens for git operations
5. **Machine-readable agent contracts** — YAML with boolean contract rules
6. **Parallel review** — code-reviewer + silent-failure-hunter in same message
7. **Anti-anchoring dispatch** — forbidden memory files, verdict-before-prose, claim extraction
8. **3-file persistent memory with ownership separation** — router owns all writes
9. **Multi-layered compaction defense** — PreCompact snapshot + memory files + SessionStart injection + rubric
10. **Circuit breaker + change-before-re-dispatch** — 3-cycle remediation cap
11. **Contract-enforced TDD gates** — machine-verified TDD_RED_EXIT, TDD_RED_REASON_KIND
12. **False-RED classification** — behavioral vs import/syntax error
13. **Complexity gradient** — trivial vs standard with automatic escalation
14. **DEBUG fan-out with independence test** — parallel debugging with conflict check
15. **LSP-powered root cause tracing** — Go to Definition, Find References for debugging
16. **Zero-finding gate** — must produce positive assertions if zero findings
17. **Quantitative confidence scoring** — HARD/SOFT dimensions, min(HARD) capped by avg(SOFT)-10
18. **Plan Validity pass** — separate plan defects from code defects
19. **Spec compliance as independent gate** — MISSING/EXTRA/MISUNDERSTOOD
20. **Fresh-review DAG with anti-anchoring** — plan-gap-reviewer with no memory loaded

## Current cc10x State

- **Version:** 12.2.0
- **Agents:** 9 (planner, bug-investigator, component-builder, code-reviewer, silent-failure-hunter, integration-verifier, doc-syncer, plan-gap-reviewer, researcher)
- **Skills:** 17
- **Hook scripts:** 9
- **Router:** 750+ lines (the orchestration brain)
- **Repo:** <https://github.com/romiluz13/cc10x>
- **Branch:** main
- **Latest commit:** `0e1b305` (parallel review restoration)

## Constraints

- **Claude Code only** — don't adopt multi-platform patterns that dilute focus
- **Zero quality regression** — every adoption must be additive
- **Orchestration is #1** — never weaken the router
- **Agent colors must be preserved**
- **No Fable 5 mentions**

## Subagent Artifacts

All reports at:

- Batch 1 (Superpowers/Matt Pocock, dims 1-5): `/Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/94c57dfa_scout_{0-4}_output.md`
- Batch 2 (Superpowers/Matt Pocock, dims 6-10): `/Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/cf3397b3_scout_{0-4}_output.md`
- Batch 3 (addyosmani agents/hooks, EveryInc infra): `/Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/99888eba_scout_{1,3}_output.md`
- Batch 4 (EveryInc core skills, Karpathy, EveryInc remaining): `/Users/rom.iluz/Dev/cc10x/.pi-subagents/artifacts/6e8be0c9_scout_{1,2,3}_output.md`
