# cc10x Upstream Steal-List — 2026-06-17

Comprehensive harvest of superpowers 6.0.2 + superpowers-lab + matt-pocock skills, diffed against cc10x's live capability map. **34 agents, 30 skills deep-read, 332 raw ideas → 54 ranked, 18 rejected, 6 critic-caught misses.** This is the decision surface: Rom approves per-batch, then validator-gated implement passes (same discipline as Campaigns 1–2).

## Key findings

- **superpowers upstream = 6.0.2 (released 2026-06-17). Our local cache IS the latest.** No newer version, no missing core skills. The 6.0.x changes were internal *rewrites* of existing skills (subagent-driven-development reworked to file-handoff + named-model dispatch + controllers-cannot-suppress-findings; writing-plans gained Global Constraints + Interfaces blocks; worktrees moved to in-project `.worktrees/`).
- **The genuinely-new ideas live in `obra/superpowers-lab` (experimental, separate install):** `finding-duplicate-functions` (semantic dup audit for LLM-grown codebases), `mcp-cli` (on-demand MCP invocation, no permanent context pollution), `using-tmux-for-interactive-commands`, `windows-vm` (niche, skip).
- **#1 theme — guard the orchestrator's INPUTS, not just agent outputs.** cc10x validates everything agents return but never polices what the router injects into dispatch prompts (pre-judged findings, pasted 42k-char blobs, missing model tiers). Superpowers' subagent-driven model treats the dispatch prompt itself as an accountability surface.

## The 6 cross-cutting themes (the philosophy to absorb)

1. **Guard dispatch INPUTS, not just outputs** — the router prompt is an accountability surface.
2. **Bidirectional review loops** — receiver verifies, can dispute-with-evidence, can flag the PLAN itself; cc10x's remediation is one-directional (finding → blind fix → comply-or-circuit-break).
3. **Baseline-before-change + feedback-loop-first** — record which tests were already red; build a deterministic repro loop BEFORE hypothesizing. Closes the false-attribution / looks-successful-but-does-nothing family.
4. **Test/mock honesty as a first-class gate** — the un-inherited `testing-anti-patterns.md` content catches false-GREENs at authoring time, not late at E2E.
5. **Evals + disciplined self-authoring** — behavior-shaping docs are testable artifacts (pressure scenarios, should_trigger cases, prohibitions-backfire). cc10x's single clearest gap: no way to measure if its own router triggers correctly.
6. **Destructive-action provenance + ordering invariants** — re-verify on the merged result, only tear down what you provisioned, detached-HEAD-aware menus, graceful sandbox degrade.

---

## BATCH A — Dispatch-input accountability (the #1 theme)

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 1 | Router must not pre-judge/soften reviewer/hunter/verifier dispatch prompts (self-check phrase blocklist before dispatch) | delta | workflow-artifact-and-hook-policy.md | S/high |
| 2 | File-handoff context hygiene: dispatch passes PATHS not blobs; agents write full report to `.cc10x/`, return thin CONTRACT envelope | delta | workflow-artifact-and-hook-policy.md | M/high |
| 14 | Per-role model-tier selection (cheapest tier per role; always specify model explicitly; turn-count beats token price) | delta | cc10x-router/SKILL.md | M/med |
| 31 | Terse-imperative loophole: "just add X" sets scope not method — does NOT waive the workflow/gates | delta | cc10x-router/SKILL.md | S/med |
| M5 | Reviewer context-hygiene: diff context lines ARE the changed files; crawl outside diff only for a named risk (lock-ordering/API-contract/shared-mutable-state) | delta | code-reviewer.md | S/med |

## BATCH B — Bidirectional review & remediation

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 3 | Bidirectional remediation: fix agent VERIFIES finding vs codebase before applying; may DISPUTE with evidence (FINDING_DISPUTED, adjudicated by verifier not reviewer) | delta | remediation-and-research.md | M/high |
| 8 | Two-isolated-assessments + WEAVE reconciliation (agree / detector-only / false-positive), anti-anchoring rationale (replaces bare "stricter wins") | delta | code-review-patterns | M/high |
| 16 | Fix-wave consolidation: one REM-FIX dispatch w/ complete findings list, counts as 1 cycle not N | delta | remediation-and-research.md | S/med |
| 17 | Re-review precondition gate: fix report must contain {covering tests, command, output} before re-dispatching reviewer | delta | remediation-and-research.md | S/med |
| 19 | Plan-mandated-finding adjudication carve-out: finding that contradicts an explicit plan mandate escalates to human, not auto-dismissed by precedence | delta | remediation-and-research.md | S/med |
| 29 | Reviewer CANNOT_VERIFY_CROSS_PHASE field; router reconciles before phase_exit | delta | code-reviewer.md | S/med |
| 34 | Reviewer may flag PLAN_DEFECT (not just code-vs-plan); a stated rationale never downgrades severity | delta | code-reviewer.md | S/med |
| 39 | Anchored 0-4 quality rubric (per-integer criteria + "most code scores mid-band, don't inflate") | delta | code-review-patterns | M/med |

## BATCH C — Baseline & feedback-loop-first debugging

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 4 | Pre-work clean-baseline snapshot: record which tests are ALREADY red before any change; verifier diffs against it | delta | build-workflow.md | M/high |
| 6 | Feedback-loop-first debugging: build fast/deterministic/agent-runnable repro as gating phase, 10-rung construction ladder | delta | debugging-patterns | M/high |
| 7 | No-loop-no-hypothesis fail-closed gate w/ concrete ask-list (env access / HAR / core dump) when repro impossible | delta | bug-investigator.md | M/high |
| 18 | Independence-test gate for parallel debug fan-out (scoped investigator per domain) + fan-in conflict-check | delta | debug-workflow.md | M/med |
| 20 | Defense-in-depth durable fix: validate at every data-flow layer to make the bug class structurally impossible | delta | bug-investigator.md | M/med |
| 21 | Multi-component boundary instrumentation matrix BEFORE hypothesis; runtime stack-capture fallback when LSP dead-ends | delta | bug-investigator.md | M/med |
| 32 | Debug close-out: winning-hypothesis → MEMORY_NOTES + tagged-instrumentation cleanup + post-mortem architecture handoff | delta | bug-investigator.md | M/med |
| 33 | Regression-test-only-if-correct-seam-exists; absence of a correct seam IS the finding (no shallow false-confidence test) | delta | bug-investigator.md | M/med |

## BATCH D — Test/mock honesty

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 5 | Mock/test honesty gates: assert real behavior not mock-existence, schema-complete mocks, no DB-bypass verification | delta | integration-verifier.md | M/high |
| M2 | + test-only-methods-in-production red flag; + mocking-without-understanding (run real first, then mock minimally) — the 2 anti-patterns rank 5 dropped | delta | integration-verifier.md | S/med |
| 25 | Verify-RED is a behavioral failure w/ expected message, not a typo/import ERROR (close false-RED loophole) | delta | component-builder.md | S/med |
| M1 | **Condition-based-waiting** as first-class authoring technique: poll the condition (waitFor + 10ms), not arbitrary sleeps; documented-timeout exception. Full upstream skill reduced to ONE line in cc10x. *(critic: strongest miss)* | delta | test-driven-development + integration-verifier | M/high |

## BATCH E — Plan & build contracts

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 13 | Per-task Interfaces block (Consumes/Produces w/ exact signatures) in the execution contract | delta | planner.md | M/med |
| M6 | Plan self-review type-consistency scan + no-dangling-reference rule (verifies Interfaces blocks close) | delta | planner.md / planning-patterns | S/med |
| 22 | Read existing ADRs/Durable Decisions for the touched area before planning; flag contradictions loudly | delta | planner.md | M/med |
| 24 | Test-seam selection discipline: highest seam, fewest seams (ideal one), confirm before building | delta | planning-patterns | S/med |
| 28 | YAGNI grep-check on "implement it properly" findings (grep for usage → propose deletion if unused) | delta | code-generation | S/med |
| 42 | Prefactor-first planner pre-step ("make the change easy, then make the easy change") | delta | planning-patterns | S/med |
| 43 | Per-phase right-sizing heuristic: a phase = smallest unit worth a fresh reviewer's gate; independently demoable | delta | planning-patterns | S/med |
| 44 | Durability-horizon rule: behavioral + named signatures (no volatile file:line) for decision_rfc/AFK artifacts | delta | planning-patterns | M/med |
| 45 | Reason-categorized HITL/[CHECKPOINT] markers (judgment / external-access / design-decision / manual-verification) | delta | planner.md | S/med |

## BATCH F — Finishing & worktree safety

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 11 | Merge-then-cleanup ordering invariant: re-verify tests ON the merged result before removing anything | delta | build-workflow.md | M/high |
| 12 | Worktree cleanup provenance: only tear down what cc10x provisioned; defer to native ExitWorktree | delta | build-workflow.md | M/high |
| 15 | Deferred-Minor-findings roll-up surfaced for triage at BUILD-DONE (a roll-up nobody reads = silent discard) | delta | build-workflow.md | M/med |
| 35 | Detached-HEAD-aware / already-isolated git pre-flight driving the finishing-menu shape + graceful sandbox degrade | delta | build-workflow.md | S/med |
| 36 | Auto-detect manifest & install deps after entering fresh workspace (so first TDD RED isn't spurious missing-deps) | delta | build-workflow.md | S/med |

## BATCH G — Net-new skills (SURFACE GROWTH — weigh vs un-bloat goal)

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 9 | **skill-eval-harness**: trigger-evals.json (should_trigger incl. hard negatives) + pressure-scenario dispatch (cc10x's single clearest gap) | net-new | skills/skill-eval-harness | L/high |
| M4 | + meta-test diagnosis loop (3-way classifier: defiance / missing-content / invisibility) folded into eval harness | net-new | skills/skill-eval-harness | — |
| 10 | **authoring-cc10x-guidance** meta-skill: match-the-form-to-the-failure (prohibitions backfire on shaping problems), RED-GREEN-REFACTOR-for-skills | net-new | skills/authoring-cc10x-guidance | M/high |
| M3 | + SDO description-shape rule (describe WHEN not the workflow; self-apply to cc10x's 25 descriptions) | net-new | skills/authoring-cc10x-guidance | — |
| 48 | **finding-duplicate-functions**: semantic (not syntactic) dup-helper audit for LLM-grown codebases *(superpowers-lab)* | net-new | skills/finding-duplicate-functions | L/med |
| 49 | **prototyping/spike** mode: answer ONE design question, then delete-or-absorb; "no tests" hard-walled from BUILD | net-new | skills/prototyping | L/med |
| 50 | **mcp-cli**: invoke MCP servers on-demand vs pre-loading as permanent context pollution *(superpowers-lab)* | net-new | skills/mcp-cli | M/low |

## BATCH H — Intent routing & gate visibility

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 23 | Read-only ORIENT/UNDERSTAND intent so "explain/map this code" doesn't mis-route to BUILD | delta | cc10x-router/SKILL.md | M/med |
| 26 | Design self-review gate after the brainstorming spec (placeholder/contradiction/scope/ambiguity, pick-one-explicit) | delta | brainstorming | S/med |
| 27 | Scope-triage/decomposition gate at front of brainstorming (is this really N projects?) | delta | brainstorming | S/med |
| 30 | Hoist completion/exit gates into guaranteed-loaded band (rules below chunked-read window silently no-op); restore VBC's scannable tables inline | delta | verification-before-completion | S/med |
| 51 | Self-suppressing capability offers (own message, honest about cost, never re-offered if declined) | delta | cc10x-router/SKILL.md | S/low |

## BATCH I — Safety, memory & research hygiene

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 37 | Redact secrets/PII before persisting any cc10x-authored artifact (scoped to outward artifacts) | delta | session-memory | S/med |
| 38 | Single-line machine-readable BUILD_PREFLIGHT token emitted right before first file mutation | delta | component-builder.md | S/med |
| 40 | Don't misread a tool/fallback message as a hard blocker ("you ARE the provider" anti-pattern) | delta | remediation-and-research.md | S/med |
| 52 | Compaction KEEP/SUMMARIZE/DROP rubric pinning user hard-constraints verbatim into the live transcript | delta | session-memory | S/low |
| 53 | Disambiguate same-name retrieval noise against the resolved canonical entity | delta | research | S/low |
| 54 | Per-rule dated "why this gate exists" scar notes on Iron Laws/gates | delta | test-driven-development | M/low |

## BATCH J — Frontend (cherry-picked from impeccable; visual-craft bulk rejected)

| # | Idea | Cls | Target | Eff/Imp |
|---|------|-----|--------|---------|
| 41 | Mock-fidelity ingredient inventory: design → per-ingredient acceptance checklist; silently-dropped ingredient = P0 | delta | frontend-patterns | M/med |
| 46 | Two-altitude anti-AI-slop reflex check (first-order AND second-order default) + maintained reflex-reject lists | delta | frontend-patterns | S/med |
| 47 | Design-system drift root-cause classifier (missing-token / one-off-impl / conceptual-misalignment) + match-flow-shape-to-neighbors | delta | frontend-patterns | S/med |

---

## Consciously REJECTED (18 — do not implement)

Browser/HTTP+WS visual-mockup server; visual before/after HTML architecture report; praise-first reviewer / mandatory Strengths section; find-polluter.sh; HITL bash send-keys loop; raw `git worktree add` fallback + gitignore-then-commit; out-of-scope rejection KB; external issue-tracker publishing (to-prd/to-issues GitHub/Linear); issue-triage state machine; GitHub inline-thread reply + "no file paths" rule; social-media research engine; wholesale impeccable frontend surface (~34 refs); 1% skill-invocation threshold; skill-discovery/npx-skills package-manager; deliberate skill-SELECTION pass (skill-router core); manual pre-emptive compaction command; + a long already-have list (router single-entry, durable wf JSON, machine contracts, skill_precedence_gate, complexity gradient, Iron Laws, rationalization tables, vertical-slicing, etc.).

**Reject rationale theme:** anything that ships a stateful server/CDN payload, auto-commits, mutates external state, adds an intake queue, or creates a 2nd orchestration path the router doesn't own — all fight cc10x's lean, fail-closed, single-writer, artifact-on-disk identity.

---

## Implementation notes

- **Tension to resolve (Rom's call):** Batch G grows cc10x's surface (4-5 new skills), which cuts against the un-bloat goal that drove Campaigns 1–2. Recommendation: take the two *accountability-shaped* net-new skills (9 eval-harness, 10 meta-authoring) since they deepen the identity; treat 48/49/50 (capability-expansion) as opt-in.
- **Cheap because of fork-strip:** the 4 stripped fork skills are thin deltas now — adopting an upstream refinement = edit the delta + DIVERGENCE note, not re-merge.
- **Discipline (unchanged):** trust only real loadable content; 4 validators green per commit; grep harness needles before rewording; branch off main, ff-merge, push, co-author `Claude Fable 5 <noreply@anthropic.com>`.
- **superpowers-lab** items (48, 50) require pointing at `obra/superpowers-lab`, not the core cache.
