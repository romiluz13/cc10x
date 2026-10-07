# CC10X Prompt Behavioral Invariant Registry

> **Status note:** Aligned to the `v12.10.0` remediation tree on 2026-10-07 (last released line `v12.9.1`), against `plugins/cc10x/agents/` and `plugins/cc10x/skills/`. Release history lives in `CHANGELOG.md`. PINV-013 to PINV-019 register the seven agents added after the original set; the companion registry `router-invariants.md` is aligned to the same tree.

## Purpose

This file maps each load-bearing prompt behavior to the failure it prevents.
If a Tier 1 or Tier 2 prompt contract changes, the matching invariant must be reviewed in the same change.

This registry complements, but does not replace, [router-invariants.md](router-invariants.md).

`cc10x-router` itself is not treated as a prompt-only surface here. The router
kernel and its mandatory references are orchestration-sensitive and must stay in
the router/runtime lane with audit and replay.

## Audit Snapshot

Validated against the live prompt surface:

- planner, component-builder, integration-verifier
- plan-gap-reviewer
- plan-review-gate, verification
- memory-and-handoff
- advisory skill descriptions for `frontend` and `debugging`
- qa-researcher, qa-harness-builder, qa-executor
- triage-agent, architecture-scanner
- researcher, doc-syncer

`bug-investigator`, `code-reviewer` and `failure-hunter` have no dedicated PINV here; their router-side gates are INV-009, INV-008 and INV-020 in `router-invariants.md`.

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

**Covers:** `plugins/cc10x/skills/verification/SKILL.md`
**Enforces:** No completion/fix/pass claim without fresh verification evidence from the current session.
**Failure prevented:** False completion, stale-evidence claims, and “should pass” rationalization.
**Wording drift that breaks it:** Softening “no completion claims” or allowing inferred success language.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if it stays wording-only and does not add runtime steps.

### PINV-006: Internal skills remain advisory under explicit user/project authority

**Covers:** planner, component-builder, integration-verifier, bug-investigator, `frontend`, `debugging`
**Enforces:** User prompt, `CLAUDE.md`, repo standards, and approved plans outrank internal CC10X skills.
**Failure prevented:** Internal patterns silently competing with explicit project direction.
**Wording drift that breaks it:** Skill descriptions or agent wording that sound authoritative or self-authorizing.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

### PINV-007: Skill descriptions describe when to use, not workflow summaries

**Covers:** `frontend`, `debugging`, `plan-review-gate`, `verification`
**Enforces:** Descriptions stay trigger-oriented and do not summarize workflow steps that Claude may follow instead of reading the body.
**Failure prevented:** Trigger false positives and workflow shortcuts caused by over-descriptive metadata.
**Wording drift that breaks it:** Descriptions that explain process details instead of symptoms/conditions for invocation.
**Safe to weaken:** No.
**Safe to strengthen:** Yes, as long as trigger accuracy improves.

### PINV-008: Goal-backward verification framing remains intact

**Covers:** `integration-verifier`, `verification`
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

### PINV-011: Live-proof requirements cannot silently downgrade

**Covers:** `plugins/cc10x/agents/planner.md`, `plugins/cc10x/skills/planning/SKILL.md`, `plugins/cc10x/agents/integration-verifier.md`, `plugins/cc10x/skills/verification/SKILL.md`
**Enforces:** When the request or accepted plan requires real, seeded, production-like verification, the plan must keep that requirement explicit and the verifier must not substitute replay-only, unit-only, or manual-only checks as equivalent proof.
**Failure prevented:** CC10X reporting trust-grade verification while only exercising deterministic fixtures or lightweight local checks.
**Wording drift that breaks it:** Framing live verification as optional when the plan made it required, or describing replay/unit/manual checks as interchangeable with live-system proof.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if runtime orchestration ownership remains with the router.

### PINV-012: Session memory stays router-subordinate and distilled

**Covers:** `plugins/cc10x/skills/memory-and-handoff/SKILL.md`
**Enforces:** Agents load versioned memory early, emit distilled memory notes, and do not bypass router-owned final markdown persistence.
**Failure prevented:** Duplicate memory write paths, bloated memory notes, and durable-state drift between workflow artifacts and markdown memory.
**Wording drift that breaks it:** Telling write agents to edit `.cc10x/*.md` directly, weakening the distillation rule, or implying chat history can substitute for durable memory.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if router-owned persistence and the `.cc10x/` state root remain unchanged.

### PINV-013: QA research reports one source and cites every claim

**Covers:** `plugins/cc10x/agents/qa-researcher.md`
**Enforces:** The agent reads only its assigned `SOURCE`, every `CLAIMS` entry carries locatable `evidence`, observability points carry a `provenance` of `V`, `Vp` or `I`, and an empty or unavailable source is reported as such rather than padded.
**Failure prevented:** A feature understanding built from guesses or from sources the plan did not assign, which then seeds the test plan.
**Wording drift that breaks it:** Allowing reads outside `SOURCE`, accepting claims without evidence, or treating an empty source as a failure to hide.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if the contract fields the router reads stay unchanged.

### PINV-014: QA harness builder never touches product code and proves its assertions can fail

**Covers:** `plugins/cc10x/agents/qa-harness-builder.md`
**Enforces:** `PRODUCT_CODE_TOUCHED=true` is `STATUS: FAIL` in both modes; a `MUTATION_CHECKS` entry that survived is `FAIL`; preflight provisions nothing (`SERVICES_PROVISIONED` is `[]`); missing credentials or a currency gate return `BLOCKED` with `NEXT_ACTION: gate`, and the agent never asks the user itself.
**Failure prevented:** A harness that edits the code it is meant to test, assertions that pass whatever the system does, and preflight turning into the environment it exists to check.
**Wording drift that breaks it:** Softening the product-code boundary, counting liveness probes toward the mutation floor, or letting a blocked prerequisite round to `FAIL` or `PASS`.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes, if router-owned gate semantics stay unchanged.

### PINV-015: QA executor witnesses and does not repair

**Covers:** `plugins/cc10x/agents/qa-executor.md`
**Enforces:** The agent edits neither test nor product code (`TEST_CODE_TOUCHED` or `PRODUCT_CODE_TOUCHED` is `FAIL`); every plan scenario runs and every observation point is asserted; blocked scenarios force `BLOCKED`; `TEARDOWN_STATUS` of `leaked` or `not_run` forces `FAIL`; `PASS` needs evidence that reconciles with the scenario totals.
**Failure prevented:** A green run produced by repairing the test, a skipped scenario counted as absent, and leaked environments reported as clean.
**Wording drift that breaks it:** Letting the executor fix a failing scenario, rounding blocked to pass, or accepting a summary count without matching evidence rows.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

### PINV-016: Triage stays advisory and inside its write scope

**Covers:** `plugins/cc10x/agents/triage-agent.md`
**Enforces:** The agent never writes code and never auto-routes into BUILD or DEBUG; `Write` is permitted only under `.scratch/` and `.out-of-scope/`; the redundancy check and the prior-rejection check run and are reported; a category or wontfix decision stops for human input (`BLOCKING` true).
**Failure prevented:** Triage turning into an unreviewed code change, or a high-blast-radius wontfix decided without the user.
**Wording drift that breaks it:** Widening the write scope, dropping either check, or letting `NEEDS_INFO` and `WONTFIX` proceed without a stop.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

### PINV-017: Architecture scanner is read-only and advisory

**Covers:** `plugins/cc10x/agents/architecture-scanner.md`
**Enforces:** The agent writes no production code; its only write is the HTML report in the OS temp directory (a prompt rule, not a tool restriction); it has unrestricted `Bash` in its tool list and the prompt names only `git log --oneline` and `open <path>`; the envelope is always `b:false` and `cr:0`.
**Failure prevented:** An advisory scan that edits the codebase or blocks a workflow.
**Wording drift that breaks it:** Allowing edits, writing the report into the repo, or making candidates blocking.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

### PINV-018: Research reports what it attempted, what it used and how good it is

**Covers:** `plugins/cc10x/agents/researcher.md`
**Enforces:** Findings are persisted to a file named in `FILE_PATH`; `SOURCES_ATTEMPTED` lists every backend tried and `SOURCES_USED` only those that produced findings; `QUALITY_LEVEL` and `BACKEND_MODE` are stated; a degraded or unavailable backend returns `DEGRADED` or `UNAVAILABLE`, not `COMPLETE`.
**Failure prevented:** A plan or diagnosis resting on research whose backend failed or whose quality was overstated.
**Wording drift that breaks it:** Listing only successful backends, dropping the quality level, or reporting `COMPLETE` for partial results.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

### PINV-019: Doc sync is diff-scoped, minimal and reports skipped layers

**Covers:** `plugins/cc10x/agents/doc-syncer.md`
**Enforces:** The agent classifies the diff's `IMPACT_LEVEL` first; at `none` it returns `STATUS: SKIPPED` with a `SKIP_REASON` and opens no doc file; otherwise it edits with the smallest change that matches the diff and lists `DOC_FILES_UPDATED` and `DOC_FILES_SKIPPED` with reasons; it never pastes doc content into `CLAUDE.md`.
**Failure prevented:** Documentation rewrites unrelated to the change, or silent skips that look like a clean sync.
**Wording drift that breaks it:** Removing the skip path, allowing broad rewrites, or dropping the skipped-file reasons.
**Safe to weaken:** Never.
**Safe to strengthen:** Yes.

## Change Policy

- Tier 1 prompt edits require audit + replay + manual semantic review.
- Tier 2 prompt edits require audit + targeted semantic review.
- Tier 3 description edits require audit only unless they affect trigger authority or precedence.
- If a prompt change implies new runtime behavior, it is not a prompt-only change and must leave the prompt-only lane.
