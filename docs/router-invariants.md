# CC10x Router Behavioral Invariant Registry

> **Status note:** Current product line is `v9.1.1`. This registry is fully aligned to the live router structure in `plugins/cc10x/skills/cc10x-router/SKILL.md` as of 2026-03-07.

## Purpose

This file maps each load-bearing router behavior to the failure it prevents.
If a router section changes, the matching invariant must be updated in the same change.

## Audit Snapshot

Validated against the live plugin surface:
- workflow artifacts under `.claude/cc10x/workflows/{wf}.json`
- workflow event logs under `.claude/cc10x/workflows/{wf}.events.jsonl`
- plugin hooks in `plugins/cc10x/hooks/hooks.json`
- router-owned remediation creation
- fail-closed scenario evidence rules for BUILD / DEBUG / VERIFY
- memory finalization and transient `memory_task_id`

## Current Invariants

### INV-001: Workflow artifact creation is immediate and durable
**Covers:** Router `## 2a. Workflow Artifact And Hook Policy`, `## 6. Workflow Task Graphs`
**Enforces:** Every workflow gets a JSON artifact and append-only event log as soon as the parent workflow task id is known.
**If removed:** Resume, verifier handoff, research quality tracking, and hook-based context injection become conversation-dependent and non-durable.
**Safe to remove:** Never.

### INV-002: Parent workflow task uses two-step backfill
**Covers:** Router `## 3. Task Metadata Contract`, `## 6. Workflow Task Graphs`
**Enforces:** Parent workflow tasks may start with `wf:PENDING_SELF`, but the router must immediately rewrite the full metadata block with the real `wf:{task_id}` before child task creation.
**If removed:** Child tasks can be created under ambiguous scope and hydration can attach to the wrong workflow.
**Safe to remove:** Never.

### INV-003: Every CC10X child task is workflow-scoped
**Covers:** Router `## 3. Task Metadata Contract`
**Enforces:** Child tasks must carry `wf`, `kind`, `origin`, `phase`, `plan`, `scope`, and `reason`.
**If removed:** Resume, remediation counting, and re-review routing degrade into subject parsing and shared-task-list collisions.
**Safe to remove:** Never.

### INV-004: Router is the only orchestration owner
**Covers:** Router `## 7. Dispatcher And Agent Prompt Contract`, `## 9. Remediation And Workflow Rules`, `## 11. Re-Review Loop`
**Enforces:** Workers emit contracts and remediation intent; the router creates, blocks, resumes, and completes orchestration tasks.
**If removed:** Reviewer/verifier drift back into mutating orchestration state and task ownership becomes ambiguous again.
**Safe to remove:** Never.

### INV-005: Scope decision is a first-class BUILD pause
**Covers:** Router `## 8. Post-Agent Validation`, `## 9. Remediation And Workflow Rules`
**Enforces:** Mixed CRITICAL + HIGH findings in BUILD pause for explicit scope selection before remediation is created.
**If removed:** HIGH issues are silently dropped when CRITICAL-only fixes are chosen by default.
**Safe to remove:** Only if re-hunt is forced to `ALL_ISSUES` in every BUILD remediation path.

### INV-006: Remediation loops are workflow-scoped and bounded
**Covers:** Router `## 9. Remediation And Workflow Rules`, `## 11. Re-Review Loop`
**Enforces:** `kind:remfix` counting, re-review task creation, and cycle limits all use the current `wf` scope.
**If removed:** Remediation loops can count unrelated tasks, overrun, or deadlock in shared task lists.
**Safe to remove:** Never.

### INV-007: Research quality is durable, not conversational
**Covers:** Router `## 10. Research Orchestration`, `## Research Quality`, `## Research Files`
**Enforces:** Research backend choice, quality level, and file paths are written into workflow artifacts and passed forward explicitly.
**If removed:** Planner/debugger decisions begin depending on transient research prose and old memory references.
**Safe to remove:** Never.

### INV-008: Read-only outputs fail closed
**Covers:** Router `## 8. Post-Agent Validation`
**Enforces:** Read-only agent outputs must produce a valid contract signal, and verifier scenario totals must reconcile with evidence.
**If removed:** APPROVE / CLEAN / PASS can slip through with malformed evidence or incomplete verification.
**Safe to remove:** Never.

### INV-009: Write-agent contracts fail closed
**Covers:** Router `## 8. Post-Agent Validation`
**Enforces:** BUILD / DEBUG / PLAN outputs must contain the expected YAML contract fields and satisfy pass rules before the workflow advances.
**If removed:** Builder, investigator, or planner can self-report success without enough proof.
**Safe to remove:** Never.

### INV-010: Scenario evidence gates BUILD, DEBUG, and VERIFY
**Covers:** Router `## 8. Post-Agent Validation`
**Enforces:**
- BUILD requires at least one passing named scenario with concrete command/expected/actual proof
- DEBUG requires regression plus variant evidence when a fix is claimed
- VERIFY requires scenario totals to match evidence rows
**If removed:** CC10X stops behaving like a BDD-style evidence system and reverts to narrative confidence.
**Safe to remove:** Never.

### INV-011: Convergence state blocks “good enough” progression
**Covers:** Router `## 8. Post-Agent Validation`, `## 12. Chain Execution Loop`
**Enforces:** Incomplete or contradictory evidence sets `quality.convergence_state=needs_iteration` and stops workflow advancement.
**If removed:** The system starts silently tolerating partial proof and ambiguous completion.
**Safe to remove:** Never.

### INV-012: Memory finalization is router-owned and compaction-safe
**Covers:** Router `## 12. Chain Execution Loop`, `## 13. Memory Finalization`
**Enforces:** Read-only Memory Notes are copied into the memory task immediately; final persistence happens inline through the Memory Update task; transient `memory_task_id` is removed on completion.
**If removed:** Memory becomes conversation-dependent or leaks stale workflow pointers across sessions.
**Safe to remove:** Never.

### INV-013: Plugin hooks are guardrails, not orchestration
**Covers:** Router `## 2a. Workflow Artifact And Hook Policy`, plugin hooks
**Enforces:** Hooks remain minimal and audit-first:
- `PreToolUse` protects memory writes
- `SessionStart` injects workflow context
- `PostToolUse` audits workflow artifact integrity
- `TaskCompleted` checks task metadata
**If removed:** Either runtime safety degrades, or hooks sprawl into a second orchestration system.
**Safe to remove:** Only if an equivalent plugin-native guardrail replaces the specific hook behavior.

### INV-014: Workflow replay fixtures are part of the safety contract
**Covers:** `plugins/cc10x/scripts/cc10x_workflow_replay_check.py`, `plugins/cc10x/tests/fixtures/`
**Enforces:** PLAN / BUILD / DEBUG / REVIEW / VERIFY decision paths are regression-checked without relying on a live Claude session.
**If removed:** Future router/prompt edits can regress core orchestration behavior without a deterministic detection path.
**Safe to remove:** Never.

## Legacy Appendix

Pre-`v9.x` invariants were reorganized rather than preserved one-for-one. Historical context remains in git history. The current source of truth is this live registry plus:
- `plugins/cc10x/skills/cc10x-router/SKILL.md`
- `plugins/cc10x/scripts/cc10x_harness_audit.py`
- `plugins/cc10x/scripts/cc10x_workflow_replay_check.py`
