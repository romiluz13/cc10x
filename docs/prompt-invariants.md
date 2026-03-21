# CC10X Prompt Behavioral Invariant Registry

> **Status note:** This registry is aligned to the live prompt stack in `plugins/cc10x/agents/` and `plugins/cc10x/skills/` as of 2026-03-21.

## Purpose

This file maps each load-bearing prompt behavior to the failure it prevents.
If a Tier 1 or Tier 2 prompt contract changes, the matching invariant must be reviewed in the same change.

This registry complements, but does not replace, [router-invariants.md](/Users/rom.iluz/Dev/cc10x_v5/cc10x/docs/router-invariants.md).

## Audit Snapshot

Validated against the live prompt surface:
- planner, component-builder, integration-verifier
- plan-gap-reviewer
- plan-review-gate, verification-before-completion
- bug-investigator, code-reviewer, silent-failure-hunter
- advisory skill descriptions for frontend/debugging patterns

## Current Invariants

### PINV-001: Planner cannot silently approve open decisions
**Covers:** `plugins/cc10x/agents/planner.md`
**Enforces:** Open decisions remain explicit, recommended defaults remain unapproved, and differences from agreement remain visible.
**Failure prevented:** Planner defaults masquerade as approved requirements.
**Wording drift that breaks it:** Replacing blocking/explicit language with “reasonable default,” “proceed,” or “accepted unless objected.”
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if the prompt stays non-runtime and does not change router gating semantics.

### PINV-002: Plan review stays fail-closed and verdict-based
**Covers:** `plugins/cc10x/skills/plan-review-gate/SKILL.md`
**Enforces:** Review is adversarial, evidence-backed, and binary enough to block execution on unresolved issues.
**Failure prevented:** “Approved with comments” behavior sneaks back into plan review.
**Wording drift that breaks it:** Introducing advisory/suggestion framing or softening blocking findings into collaborative notes.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if runtime isolation is not falsely implied.

### PINV-003: Builder treats the approved phase as the contract
**Covers:** `plugins/cc10x/agents/component-builder.md`
**Enforces:** The builder follows only the current approved phase, reports scope truthfully, and does not improvise later-phase work.
**Failure prevented:** Silent phase skipping, hidden scope creep, and narrative success on partial execution.
**Wording drift that breaks it:** Changing “must/stop/fail” phrasing into “try/consider/may continue.”
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if it does not add new router-owned checkpoints or task graph behavior.

### PINV-004: Verifier remains independent from upstream approval
**Covers:** `plugins/cc10x/agents/integration-verifier.md`
**Enforces:** Reviewer approval, hunter CLEAN, or builder confidence are inputs to verification, never substitutes for proof.
**Failure prevented:** Self-certified completion where one agent’s confidence is mistaken for verification.
**Wording drift that breaks it:** Allowing trust in summaries, success reports, or narrative confidence without local evidence.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if it does not alter router remediation flow.

### PINV-005: Verification-before-completion preserves fresh-evidence discipline
**Covers:** `plugins/cc10x/skills/verification-before-completion/SKILL.md`
**Enforces:** No completion/fix/pass claim without fresh verification evidence from the current session.
**Failure prevented:** False completion, stale-evidence claims, and “should pass” rationalization.
**Wording drift that breaks it:** Softening “no completion claims” or allowing inferred success language.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if it stays wording-only and does not add runtime steps.

### PINV-006: Internal skills remain advisory under explicit user/project authority
**Covers:** planner, component-builder, integration-verifier, bug-investigator, `frontend-patterns`, `debugging-patterns`
**Enforces:** User prompt, `CLAUDE.md`, repo standards, and approved plans outrank internal CC10X skills.
**Failure prevented:** Internal patterns silently competing with explicit project direction.
**Wording drift that breaks it:** Skill descriptions or agent wording that sound authoritative or self-authorizing.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

### PINV-007: Skill descriptions describe when to use, not workflow summaries
**Covers:** `frontend-patterns`, `debugging-patterns`, `plan-review-gate`, `verification-before-completion`
**Enforces:** Descriptions stay trigger-oriented and do not summarize workflow steps that Claude may follow instead of reading the body.
**Failure prevented:** Trigger false positives and workflow shortcuts caused by over-descriptive metadata.
**Wording drift that breaks it:** Descriptions that explain process details instead of symptoms/conditions for invocation.
**Safe to weaken:** No.
**Safe to strengthen:** Yes, as long as trigger accuracy improves.

### PINV-008: Goal-backward verification framing remains intact
**Covers:** `integration-verifier`, `verification-before-completion`
**Enforces:** Verification still reasons over truths, artifacts, and wiring, not only exit codes or file presence.
**Failure prevented:** Stubs, unwired implementations, and local illusions passing as complete.
**Wording drift that breaks it:** Removing truths/artifacts/wiring or collapsing them into generic “tests passed.”
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

### PINV-009: Non-trivial plans must be grounded in repo reality
**Covers:** `plugins/cc10x/agents/planner.md`, `plugins/cc10x/skills/plan-review-gate/SKILL.md`
**Enforces:** Non-trivial plans expose a codebase reality check, plan-vs-code gaps, an assumption ledger, and phase dependencies before they can pass review.
**Failure prevented:** Plans that look rigorous on paper but ignore the actual codebase and force the user into repeated “compare it to the code again” loops.
**Wording drift that breaks it:** Removing explicit repo-comparison language, hiding contradictions behind summary prose, or collapsing assumptions back into confident narrative text.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if it remains inside planning artifacts and review wording only.

### PINV-010: Fresh planning review stays reviewer-only
**Covers:** `plugins/cc10x/agents/plan-gap-reviewer.md`, `plugins/cc10x/agents/planner.md`
**Enforces:** The fresh planning reviewer can challenge the plan, but it cannot rewrite the plan, own memory, ask the user questions, or take over workflow decisions from the planner/router.
**Failure prevented:** Subagent freshness turning into orchestration drift or multi-owner plan artifacts.
**Wording drift that breaks it:** Allowing the reviewer to rewrite the plan directly, to own approval language, or to depend on broad session history instead of curated evidence.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

## Change Policy

- Tier 1 prompt edits require audit + replay + manual semantic review.
- Tier 2 prompt edits require audit + targeted semantic review.
- Tier 3 description edits require audit only unless they affect trigger authority or precedence.
- If a prompt change implies new runtime behavior, it is not a prompt-only change and must leave the prompt-only lane.
