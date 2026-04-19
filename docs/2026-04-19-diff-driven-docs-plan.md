# Plan: diff-driven-docs — Documentation Sync Skill

**Date:** 2026-04-19  
**Status:** Approved  
**Branch:** `feat/diff-driven-docs`  
**plan_mode:** execution_plan  
**verification_rigor:** standard

---

## Goal

Add a `diff-driven-docs` skill and companion `doc-syncer` agent to the cc10x BUILD chain. After `integration-verifier` passes, the router spawns `doc-syncer` to analyze the diff, classify documentation impact across three layers (business, technical, audit), and write any needed doc updates before the workflow closes. Documentation becomes a first-class deliverable of every BUILD phase — not an afterthought.

## Non-Goals

- Does not generate API reference docs from source (no typedoc tooling)
- Does not update CHANGELOG.md (owned by release automation)
- Does not write commit messages or PR descriptions (owned by other skills)
- Does not replace JSDoc generation tooling

## Motivation

Stale documentation is worse than no documentation — it actively misleads. The current BUILD chain verifies that code works but has no gate ensuring docs reflect what changed. This adds that gate.

The name `diff-driven-docs` was chosen deliberately to parallel `test-driven-development` already in this repo: both disciplines enforce that a deliverable (tests / docs) must be produced as part of the code-change cycle, not retroactively.

---

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Name | `diff-driven-docs` | Parallels TDD naming; mechanism-first |
| Flow position | After `integration-verifier`, before `Memory Update` | Code proven correct first; docs before workflow closes |
| Generality | File-pattern heuristics; project paths in CLAUDE.md | Skill must work across any project, not one codebase |
| Impact classifier | Fast-path skip for low-impact diffs | Avoids over-documenting trivial changes |
| Agent vs inline | Dedicated `doc-syncer` write agent | Diff analysis + multi-file writes warrant context isolation |
| New hooks | None | Existing `PreToolUse`/`PostToolUse` guards cover doc-syncer writes |
| Opt-out | `DIFF_DRIVEN_DOCS: skip` in Session Settings | Consistent with existing `AUTO_PROCEED` pattern |

---

## Acceptance Criteria

1. `plugins/cc10x/skills/diff-driven-docs/SKILL.md` exists with correct frontmatter, impact classifier, three-layer evaluation, and router integration section
2. `plugins/cc10x/skills/diff-driven-docs/references/doc-target-heuristics.md` exists with generic file-pattern → doc-area mapping table
3. `plugins/cc10x/agents/doc-syncer.md` exists with agent frontmatter, write-agent contract format, and YAML Router Contract fields
4. `build-workflow.md` BUILD task graph includes `build-doc-sync` task blocked by `verifier_task_id`; Memory Update blocked by `doc_sync_task_id`
5. `cc10x-router/SKILL.md` dispatcher table maps `build-doc-sync` → `cc10x:doc-syncer`; router contract section includes `doc-syncer` fields
6. `agent-contract-registry.md` registers `doc-syncer` in the Write Agents table
7. Two test fixtures exist: `build-doc-sync-happy-path.json` and `build-doc-sync-skipped.json`
8. `templates/doc-target-overlay.md` provides a copy-paste CLAUDE.md snippet for project-specific doc target configuration
9. All modified files read cleanly with no broken references

---

## Phases

### Phase 1 — Skill and Reference

**Objective:** Create the skill and its reference file.

**Files to create:**
- `plugins/cc10x/skills/diff-driven-docs/SKILL.md`
- `plugins/cc10x/skills/diff-driven-docs/references/doc-target-heuristics.md`

**Exit criteria:**
- Skill frontmatter is valid YAML (name, description, allowed-tools, skills)
- Description is triggering-conditions only (no workflow summary)
- Impact classifier section present
- Three-layer evaluation section present (business / technical / audit)
- Heuristics reference file uses generic file patterns, no hardcoded project paths

---

### Phase 2 — Agent

**Objective:** Create the `doc-syncer` agent.

**Files to create:**
- `plugins/cc10x/agents/doc-syncer.md`

**Exit criteria:**
- Agent frontmatter valid (name, description, model, color, tools, skills)
- Agent loads `cc10x:diff-driven-docs` skill
- Agent emits `### Router Contract (MACHINE-READABLE)` YAML block
- YAML fields: `STATUS`, `IMPACT_LEVEL`, `DOC_LAYERS_EVALUATED`, `DOC_FILES_UPDATED`, `DOC_FILES_SKIPPED`, `SKIP_REASON`, `MEMORY_NOTES`
- Completion states: `COMPLETE`, `SKIPPED`, `PARTIAL`, `FAIL`

---

### Phase 3 — Router Wiring

**Objective:** Wire `build-doc-sync` into the BUILD chain in two places.

**Files to modify:**
- `plugins/cc10x/skills/cc10x-router/references/build-workflow.md`
- `plugins/cc10x/skills/cc10x-router/SKILL.md`

**Changes to `build-workflow.md`:**
- Add `TaskCreate` for `build-doc-sync` task, blocked by `verifier_task_id`
- Update Memory Update task to also be blocked by `doc_sync_task_id`

**Changes to `cc10x-router/SKILL.md`:**
- Add `build-doc-sync` → `cc10x:doc-syncer` row to the dispatcher table (Section 7)
- Add `doc-syncer` to the write agents' YAML contract fields (Section 8)
- Add `doc-syncer` result field to the workflow artifact post-agent validation
- Reference `DIFF_DRIVEN_DOCS: skip` in Session Settings as an opt-out

**Exit criteria:**
- BUILD chain sequence is correct: builder → reviewer||hunter → verifier → doc-syncer → Memory Update
- No broken references to phase names or task IDs
- Dispatcher table has exactly one row for `build-doc-sync`

---

### Phase 4 — Contract Registry and Tests

**Objective:** Register the agent contract and add test fixtures.

**Files to modify:**
- `docs/agent-contract-registry.md`

**Files to create:**
- `plugins/cc10x/tests/fixtures/build-doc-sync-happy-path.json`
- `plugins/cc10x/tests/fixtures/build-doc-sync-skipped.json`

**Registry addition:** Add `doc-syncer` row to Write Agents table with states `COMPLETE`, `SKIPPED`, `PARTIAL`, `FAIL`.

**Happy-path fixture:** Builder and verifier contracts already completed; doc-syncer contract shows `STATUS: COMPLETE`, at least one doc file updated, `IMPACT_LEVEL: medium`.

**Skipped fixture:** Doc-syncer contract shows `STATUS: SKIPPED`, `IMPACT_LEVEL: none`, `SKIP_REASON` explaining why all three layers were skipped.

**Exit criteria:**
- Registry table updated with correct states and memory payload format
- Both fixtures are valid JSON with `id`, `workflow_type`, `agent_outputs`, and `expected` fields matching the existing fixture schema

---

### Phase 5 — Template

**Objective:** Provide a project configuration overlay template.

**Files to create:**
- `plugins/cc10x/templates/doc-target-overlay.md`

**Exit criteria:**
- Template shows how to add a `## Doc Targets` table to CLAUDE.md
- Includes at least three example rows (hooks, components, migrations)
- Instructions are copy-paste ready

---

## Risks

| Risk | Mitigation |
|------|-----------|
| Router context grows with doc-sync task in chain | Agent is isolated; router only processes contract, not diff content |
| Doc-syncer writes conflict with concurrent writes | Doc files are project-owned; no other agent writes docs in BUILD |
| Skill loads but heuristics are too generic to be useful | `doc-target-overlay.md` template lets projects tune targets in CLAUDE.md |
| Phase adds latency to BUILD | Agent only runs after verifier passes; skip path exits fast for low-impact diffs |

---

## Open Decisions

*(none — all resolved above)*
