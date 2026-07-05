## Review: Planning + Exploration (v12 vs v11.1.0 baseline)

### Files read in full
- `plugins/cc10x/skills/planning/SKILL.md` (153 lines) + `references/live-verification-strategy.md` (57 lines, byte-identical to v11 baseline)
- `plugins/cc10x/skills/plan-review-gate/SKILL.md` (139 lines) — **zero diff vs `v11.1.0`** (`git diff v11.1.0..HEAD` returns empty)
- `plugins/cc10x/skills/exploration/SKILL.md` (171 lines, merges brainstorming 537 + prototyping 151 → net compression)
- `plugins/cc10x/agents/planner.md` (125 lines, down from 414 in v11.1.0)

---

### Item 25 — Interfaces block (Consumes/Produces): **INTACT**
- `planning/SKILL.md:55-61` — Task Structure template: `**Consumes:** [...] / **Produces:** [...]`, with explicit fallback `Consumes: none / Produces: none`.
- `planner.md` step 10 — "Interfaces block: Consumes: exact signatures... Produces: exact names later phases rely on... verbatim."
- `planner.md` step 11b — "Plan Self-Review: every Consumes in a later phase must verbatim-match a Produces... dangling references are PLAN FAILURES."
- `plan-review-gate/SKILL.md` Check 1 row 6 — "Consumes/Produces are verbatim-matched across phases (no spelling drift)" as a blocking criterion.
- Verdict: wording is condensed from v11's more elaborate explanation (which included a worked example: `clearLayers()` vs `clearFullLayers()`), but the mechanism — declare, verbatim-match, self-review before save, gate-enforced — is functionally identical. No loss.

### Item 26 — Codebase Reality Check with ADR reading: **INTACT**
- `planner.md` step 5: "**Read pre-existing ADRs as constraints:** glob `docs/adr/`, `docs/decisions/`, `docs/rfcs/`, `*ADR*.md`. Treat every matching ADR as SETTLED. If the plan contradicts one, FLAG it explicitly — do NOT silently override." Nearly verbatim to v11's equivalent instruction.
- `plan-review-gate/SKILL.md` Check 1: "Codebase reality check is present | Read artifact for `Codebase Reality Check`" is still a blocking criterion (file unchanged since v11.1.0).
- Note (MEDIUM, see below): the v11 planner.md's "Output" template had explicit sub-bullets forcing the ADR treatment into the saved artifact ("Decision records in scope (treated as SETTLED)" / "Contradicted decisions (flagged, not silently overridden)"). That literal template is gone from v12's planner.md and was not relocated into `planning/SKILL.md`. The instruction to do the ADR check survives; the forced output shape that makes it auditable does not.

### Item 30 — Prototyping Hard Wall: **INTACT** (functionally), with a minor enforcement checklist loss
- `exploration/SKILL.md` Mode: SPIKE → "### Hard Wall (read before writing any prototype)": *"A prototype's rules NEVER leak into a BUILD. 'No tests, no abstractions, move fast' lives and dies inside the spike. If the answer is 'build it for real,' that is a fresh BUILD through the router with full TDD/reviewer/verifier gates. The spike's code does not become production by surviving."*
- The scar comment is preserved verbatim with its original date: `<!-- scar: 2026-06-17 — spike's "move fast, no tests" code promoted to production by inertia, skipping TDD/verifier gates... -->`
- Step 4 Close-Out still enforces DELETE-or-ABSORB with no third option, and ABSORB explicitly triggers "a fresh BUILD through the router (full gates)."
- What was dropped from v11's `prototyping/SKILL.md` (151 lines) and NOT carried into the merge: the named `skill_precedence` YAML block enumerating exactly which gates apply (test-driven-development's Iron Law, integration-verifier, code-reviewer, silent-failure-hunter by name), the "Anti-Patterns" list (explicit "Promoting the spike directly to production. This is the Hard Wall violation."), and the "Final Check" pre-completion checklist item "Hard Wall honored: no prototype rule followed into a BUILD." The rule's substance survives in one condensed paragraph; the itemized, checklist-enforced version does not.

---

## Issues Found

**HIGH** — `plugins/cc10x/agents/planner.md` (whole file) / `plugins/cc10x/skills/planning/SKILL.md:17` / `plugins/cc10x/skills/plan-review-gate/SKILL.md`
v11.1.0's planner.md had a mandatory, explicitly-triggered section: *"## Live Verification Strategy (MANDATORY when requested or risk-critical) — If the request requires real, seeded, production-like, API-driven, browser, or stress validation: read `.../live-verification-strategy.md`, include a `### Live Verification Strategy` section..."* This entire trigger is gone from current `planner.md` (`grep -i "live.verification"` returns 0 matches in planner.md, and 0 matches anywhere in plan-review-gate). The reference file itself (`planning/references/live-verification-strategy.md`) is untouched and still listed under "Reference Files" in `planning/SKILL.md:17`, but nothing tells the planner *when* to read it or requires the artifact to contain the section. `plan-review-gate` also has no check for it. Net effect: a fully-specified live-verification harness mechanism (manifest, runner commands) is now orphaned — reachable only if the planner independently decides to open the reference file. This is a genuine functional regression, not a wording simplification.

**MEDIUM** — `plugins/cc10x/agents/planner.md` vs `plugins/cc10x/skills/planning/SKILL.md`
v11.1.0 planner.md's full "## Output" template (Executive Summary, Codebase Reality Check with ADR sub-bullets, Assumption Ledger, Fresh Review Resolution, Phase Dependency Map, Phase Autonomy Classification table, Plan Self-Review section, Confidence Score table with point-value factors, Checkpoint Triggers reason-category table) was removed wholesale and not relocated to `planning/SKILL.md` (which only provides "Plan Document Header" + "Task Structure," missing Codebase Reality Check, Assumption Ledger, Confidence scoring guidance, and Phase Autonomy Classification as concrete templates). `plan-review-gate` still blocks on several of these being present in prose form (Check 1/2 rows reference "Codebase Reality Check," "Assumption ledger," "Phase dependency map"), so enforcement is not lost, but the planner now has to infer exact section shape each run rather than follow a fixed template — raising inconsistency risk across planning runs.

**LOW** — `plugins/cc10x/agents/planner.md`
Confidence-score guidance table (0-49/50-69/70-89/90-100 bands + point-value factors: "+25 context references," "+20 edge cases," etc.) dropped entirely. Only `CONFIDENCE: [0-100]` plus contract rule `CONFIDENCE≥50` remains. Self-assessment is now unanchored to concrete criteria.

**LOW** — `plugins/cc10x/skills/exploration/SKILL.md` (Mode: SPIKE)
"Anti-Patterns" list and "Final Check" pre-completion checklist from v11 `prototyping/SKILL.md` were dropped in the merge (not restored anywhere in `exploration/SKILL.md`). The Hard Wall rule itself survives in prose, but the explicit "confirm Hard Wall honored before closing out" checkpoint is gone.

**Positive finding (no issue)** — `plugins/cc10x/skills/plan-review-gate/SKILL.md:12,14`
This file is byte-identical to v11.1.0. It correctly and honestly self-describes as running inline with no subagent isolation ("not true reviewer isolation... do not pretend fresh runtime separation exists when it does not") and does **not** claim to run or gate `plan-gap-reviewer`. `plan-gap-reviewer` is a genuinely separate, router-owned fresh-context Task (confirmed in `plugins/cc10x/skills/cc10x-router/references/plan-workflow.md:46-65`, spawned as its own TaskCreate with "Fresh anti-anchoring review"). The two mechanisms are distinct and each is accurately documented in its own scope — no contradiction, no overclaiming.

---

## Verdict

Planning + Exploration is **near publish-ready** but not clean: all three specifically-flagged innovations (Interfaces block, ADR-aware Codebase Reality Check, Prototyping Hard Wall) survive functionally after the v12 compression, and `plan-review-gate` is unchanged and honest about its own limits with no false claims about `plan-gap-reviewer`. The one finding that should block or at least be fixed before publish is the **HIGH**-severity disappearance of the Live Verification Strategy trigger from `planner.md` — a maintained, non-trivial harness mechanism is now unreachable through the normal planning workflow. The **MEDIUM** loss of the concrete Output-template (Codebase Reality Check/Assumption Ledger/Confidence/Phase Autonomy sub-templates) is a leaner-file tradeoff that the review gate partially backstops but increases inconsistency risk and is worth a follow-up pass. The **LOW** items (confidence scoring guidance, spike checklist) are acceptable compression if intentional.