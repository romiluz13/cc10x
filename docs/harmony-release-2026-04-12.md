# CC10X Harmony Release Plan

Date: 2026-04-12
Target release: 10.1.19, unless implementation scope expands beyond a patch release

## Harmony Definition

Harmony means every change strengthens the existing CC10X control plane instead of adding another one.

For this release, a change is harmonious only if it:
- preserves `cc10x-router` as the only orchestration authority
- reuses the existing workflow artifact, task metadata, memory finalization, and agent contracts
- removes duplicated or conflicting instructions instead of adding parallel wording
- lands in the most native existing surface for that responsibility
- avoids new agents, new workflow types, new memory channels, new routing syntax, and new prompt stacks
- improves clarity without increasing decision surfaces

This release is not a feature expansion. It is a harmonization pass: tighten what already exists, remove drift, and make the current system more internally consistent.

## Non-Goals

- Do not add a new router, planner, reviewer, verifier, classifier, or synthesis agent.
- Do not add a new workflow type or YAML/state-machine contract field.
- Do not add a new memory write path.
- Do not add a new public positioning story based on outside sources.
- Do not broaden prompts with general inspiration language.
- Do not change package manager, repo layout, hook architecture, or plugin installation flow.

## Phase 1: Clean Existing Contradictions

Goal: remove active conflicts before refining behavior.

Required changes:
- Update `CLAUDE.md` so orientation and router invocation no longer contradict each other.
- Replace the stale MongoDB skill alias in `CLAUDE.md` with the installed `mongodb-query-optimizer` name.
- Update `plugins/cc10x/agents/bug-investigator.md` so debug attempt tracking reads memory and emits memory notes, but never instructs the agent to edit `.claude/cc10x/v10/*.md` directly.
- Update `plugins/cc10x/agents/code-reviewer.md` so internal CC10X skills are loaded only when passed by the router through `## SKILL_HINTS`.
- Update stale planner terminology where `Dev Journal` no longer matches the live plan contract language.

Exit criteria:
- No instruction tells an agent to bypass router-owned memory persistence.
- No read-only agent self-activates internal CC10X skills.
- The top-level entrypoint rule has one interpretation.

## Phase 2: Tighten Router-Owned Prompt Handoffs

Goal: make agent prompts more self-contained without creating a prompt-builder subsystem.

Required changes:
- Update `plugins/cc10x/skills/cc10x-router/SKILL.md` under the existing prompt scaffold to require routed prompts to be assembled from the workflow artifact, approved files, current task contract, and active decisions.
- Add wording that completed-phase narrative should be omitted unless it remains an active blocker, dependency, or unresolved finding.
- Keep this as router scaffold law only. Do not create new prompt files or helper layers.

Exit criteria:
- Every handoff rule still lives under the existing router prompt scaffold.
- No new prompt authority exists outside the router.

## Phase 3: Clarify Fresh Phase Boundaries

Goal: make phase-local execution explicit in the existing workflow references.

Required changes:
- Update `plugins/cc10x/skills/cc10x-router/references/build-workflow.md` so BUILD handoffs are explicitly phase-local.
- Review `plugins/cc10x/skills/cc10x-router/references/plan-workflow.md` and `plugins/cc10x/skills/cc10x-router/references/debug-workflow.md` for the same principle, but only edit if a real ambiguity exists.
- Preserve the existing workflow graph and phase cursor model.

Exit criteria:
- Current-phase objective, inputs, expected artifacts, checks, checkpoint type, exit criteria, and approved clarifications are clearly the live handoff frame.
- Prior phase detail is included only when still active.
- No workflow graph changes were made.

## Phase 4: Fix Completion Capture Order And Review Fan-In

Goal: close the documented capture-order race and make existing review signals easier for the router to interpret.

Required changes:
- Update `plugins/cc10x/skills/cc10x-router/SKILL.md` so memory payload capture happens before validation or task-state mutation after an agent returns.
- Update the `After every agent completion` section to make early capture step zero.
- Add one router-owned merge point for existing BUILD review and hunt outputs before verifier handoff.
- Store any merged summary in existing workflow result/status fields; do not create a new agent, task type, or contract field.

Exit criteria:
- The capture order matches the documented compaction recommendation.
- Review/hunt fan-in is router-owned and uses existing workflow artifact state.
- The verifier remains the independent final phase-exit authority.

## Phase 5: Sync Source-Of-Truth Docs

Goal: remove docs drift so public and internal instructions describe the live system.

Required changes:
- Update `docs/cc10x-orchestration-bible.md` to match current write-agent versus read-only-agent completion semantics.
- Update `docs/cc10x-orchestration-bible.md` research routing text to match the current web/GitHub dual-backend model.
- Update `docs/known-flaws.md` if the capture-order mitigation is changed from recommendation to live router law.
- Update `docs/prompt-invariants.md`, `docs/router-invariants.md`, `docs/agent-contract-registry.md`, and `docs/prompt-surface-inventory.md` only where their status notes or invariant descriptions become stale.
- Update local CC10X meta-skills if they still point maintainers at stale release assumptions or stale docs.

Exit criteria:
- No doc claims the bible is in sync unless it is actually aligned with live prompts.
- No doc describes old task completion or research behavior as current.
- No doc introduces a second source of truth.

## Phase 6: Update Verification And Audit Coverage

Goal: ensure the release is locked by tests and audits, not just prose.

Required changes:
- Run `python3 scripts/cc10x_harness_audit.py` from `plugins/cc10x`.
- Run `python3 scripts/cc10x_workflow_replay_check.py` from `plugins/cc10x`.
- Run `python3 scripts/cc10x_instructions_loaded_audit.py` from `plugins/cc10x`.
- Run `python3 scripts/cc10x_latency_audit.py --fixtures` from `plugins/cc10x`.
- Add or update audit/replay coverage only if an existing check cannot detect a changed invariant.

Exit criteria:
- Existing replay and harness checks pass.
- Any new invariant introduced by wording changes is covered or explicitly documented as manual semantic review.
- No broad test expansion is added without a specific invariant gap.

## Phase 7: Release Alignment Sweep

Goal: align every user-facing, maintainer-facing, and release-facing surface before tagging.

Required changes:
- Bump plugin version surfaces to the target release:
  - `plugins/cc10x/.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`
  - `README.md`
  - `CHANGELOG.md`
- Add a concise `CHANGELOG.md` entry focused on harmony, contradiction cleanup, router-owned handoffs, capture-order hardening, and docs alignment.
- Update `README.md` current version and version history.
- Review `plugins/cc10x/hooks/README.md` for release/audit wording drift.
- Review docs under `docs/` that mention the current version, prompt surface status, router invariants, contract registry, safety, or release checklist.
- Run a wording sweep across changed files for external-attribution or copied-from language. Release notes should describe CC10X-native harmonization only.
- Confirm `git status --short` contains only intentional files.
- Create the GitHub tag after verification and changelog alignment, using the target release version.

Exit criteria:
- README, changelog, plugin metadata, marketplace metadata, prompt docs, and hook docs describe the same release.
- No changed release-facing file uses external-attribution framing for this work.
- The tag matches the shipped version.
- The final release notes describe what CC10X now does better, not where any pattern came from.

## Final Release Gate

Do not tag the release unless all of the following are true:
- router remains the only orchestration authority
- workflow graph and task metadata contract are unchanged unless explicitly approved
- no new agent or skill was added
- memory writes remain router-finalized
- docs and README match the live prompt stack
- harness audit and replay check pass
- release metadata and tag target agree
