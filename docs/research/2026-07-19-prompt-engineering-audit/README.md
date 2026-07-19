# Prompt-Engineering Audit — 2026-07-19

Deep content audit of every CC10x skill, reference, and agent prompt, judged **purely as LLM instructions** (orchestration explicitly out of scope). Benchmark: `mattpocock/skills` at 9603c1c (2026-07-16), rubric derived from its `writing-great-skills` meta-skill. Five parallel fresh-context auditors; functional files only, no historical audits consulted.

## Reports

| Report | Scope | Headline |
| --- | --- | --- |
| [1 — Core workflow](pe-audit-1-core-workflow.md) | building, debugging, planning, code-review | Ideas beat the benchmark; discipline slips — 2 self-contradictions, debugging ends "gates are advisory" |
| [2 — Design/knowledge](pe-audit-2-design-knowledge.md) | codebase-design, domain-modeling, architecture, hygiene, exploration, research | Ported cores faithful; damage clusters in additions — architecture misstates the two-adapter rule twice |
| [3 — Meta/process](pe-audit-3-meta-process.md) | verification, memory-and-handoff, diff-driven-docs, plan-review-gate, update, agent-common, frontend, mcp-cli, merge-conflicts | Best decision procedures in either corpus; systemic rule-stated-2-4-times duplication |
| [4 — Agent prompts](pe-audit-4-agents.md) | all 11 agents + agent-common | 4 true contradictions incl. TaskUpdate preamble-vs-body; code-reviewer confidence math doesn't add up; invalid-YAML field examples |
| [5 — Router prose](pe-audit-5-router-prose.md) | cc10x-router SKILL.md + 8 references | References near-benchmark; SKILL.md retracts its own opening routing sentence; ~112 "never"s; all fixes wording-only |

## Cross-cutting verdict

**CC10x's original ideas are state-of-the-art — often better than the benchmark.** False-RED guard, causal-chain gate, rationalization tables, zero-finding halt, metric honesty, quote-the-line auto-demotion, fail-closed vocabulary, anti-bias blocklists, same-name disambiguation, `[EASY TO MISS]` local flags. Auditors independently confirmed 70+ better-than-benchmark items.

**Its failures are discipline, not ideas** — five recurring diseases:

1. **True contradictions (≈10, highest priority):** exit-1=RED vs false-RED guard; trust-framework vs verify-with-test; confidence bands differing across files; TaskUpdate preamble vs 5 agent bodies; wontfix stop-AND-proceed; reviewer confidence formula vs zero-finding gate; three-vs-four doc layers; "caps cycles at 3" vs checkpoint-at-3; routing first-match vs nominate; lint blocker vs "when practical".
2. **Duplication with drift:** key rules stated 2-4× (anti-"should" ×3, SKIP list ×4, motion rules ×3, ownership ×3, never-abort ×3). Estimated 20-30% of the corpus prunable at zero behavior loss.
3. **Author-facing prose in runtime bodies:** "## Note" sections, canonicity claims, "don't restate here", provenance trivia, GSD/BMAD name-drops.
4. **Undecidable adjectives in gates:** "too weak", "over-engineered", "obvious error paths", unscored CONFIDENCE numbers, "30-90 minutes"/"3 sprints" (agent-imperceptible metrics).
5. **Missing WHYs on hard rules (~60):** CI=true, ≥80 floor, loop caps, shell-write ban — rationale is what lets an LLM generalize instead of surface-match.

## Aggregate finding counts

dead-weight/contradiction 90 · vague-adjective 55 · missing-WHY 62 · hedged/passive 41 · head-to-head comparisons 46 · better-than-benchmark 70+ · concrete before→after rewrites 121 (5 ranked top-10/15 lists).

All proposed rewrites are **behavior-preserving wording changes** — no gate, priority, or authority moves.
