# CC10x Router Behavioral Invariant Registry

> **Status note:** Current product line is `v10.0.0`. This registry is aligned to the live router structure in `plugins/cc10x/skills/cc10x-router/SKILL.md` as of 2026-03-12.

## Purpose

This file maps each load-bearing router behavior to the failure it prevents.
If a router section changes, the matching invariant must be updated in the same change.

## Audit Snapshot

Validated against the live plugin surface:
- workflow artifacts under `.claude/cc10x/v10/workflows/{wf}.json`
- workflow event logs under `.claude/cc10x/v10/workflows/{wf}.events.jsonl`
- plugin hooks in `plugins/cc10x/hooks/hooks.json`
- router-owned remediation creation
- fail-closed scenario evidence rules for BUILD / DEBUG / VERIFY
- memory finalization and transient `memory_task_id`
- v10-only agent memory reads under `.claude/cc10x/v10/*.md`
- verifier independence from builder/reviewer/hunter verdicts

## Current Invariants

### INV-025: Latency telemetry is informational only
**Covers:** Router workflow artifact schema, workflow event log, latency audit tooling
**Enforces:** Timing fields, loop counters, and verifier workload breakdowns may inform optimization work, but they may not change routing, approval, remediation, or phase-advance decisions by themselves.
**If removed:** Performance instrumentation can quietly become a second decision system and weaken trust gates under the banner of speed.
**Safe to remove:** Never.

### INV-021: Router owns plan mode selection semantics
**Covers:** Router `## 5. Workflow Preparation`, planner contract, replay fixtures
**Enforces:** Every planning artifact declares exactly one `plan_mode` and the router treats `direct`, `execution_plan`, and `decision_rfc` as different safety levels.
**If removed:** Architecture work can regress into weak direct plans and broad work can bypass the stronger decision-grade contract.
**Safe to remove:** Never.

### INV-022: Spec gate is a blocking trust boundary
**Covers:** Router `## 5. Workflow Preparation`, `plan-review-gate`, `## 8. Post-Agent Validation`
**Enforces:** Planner artifacts must survive feasibility, completeness, and alignment review before BUILD may start.
**If removed:** Planner defaults and hidden assumptions can leak straight into execution again.
**Safe to remove:** Never.

### INV-023: Proof status gates phase completion
**Covers:** Router `## 5. Workflow Preparation`, `## 8. Post-Agent Validation`, BUILD/VERIFY prompts
**Enforces:** `proof_status` remains `gaps_found` until truths, artifacts, and wiring are reconciled; BUILD does not advance on narrative confidence alone.
**If removed:** CC10X can report completed work that never proved the actual user outcome.
**Safe to remove:** Never.

### INV-024: Traceability is durable across planning, execution, and remediation
**Covers:** Router artifact schema, replay fixtures, memory finalization
**Enforces:** Requirements, phases, verification, and remediation keep an explicit link chain in the workflow artifact.
**If removed:** The system becomes harder to audit, harder to resume safely, and easier to bluff with prose.
**Safe to remove:** Never.

### INV-001: Workflow artifact creation is immediate and durable
**Covers:** Router `## 2a. Workflow Artifact And Hook Policy`, `## 6. Workflow Task Graphs`
**Enforces:** Every workflow gets a JSON artifact and append-only event log under the v10 namespace as soon as the workflow UUID is known.
**If removed:** Resume, verifier handoff, research quality tracking, and hook-based context injection become conversation-dependent and non-durable.
**Safe to remove:** Never.

### INV-002: Workflow identity is stable and task-id independent
**Covers:** Router `## 3. Task Metadata Contract`, `## 6. Workflow Task Graphs`
**Enforces:** Router generates a stable workflow UUID before task creation and uses that UUID across artifacts, event logs, task metadata, resume, and hook context.
**If removed:** Child tasks can collide across sessions and hydration can attach to the wrong workflow.
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

### INV-015: Open decisions block BUILD
**Covers:** Router `## 5. Workflow Preparation`, `## 8. Post-Agent Validation`
**Enforces:** Plans with unresolved open decisions or missing `Differences From Agreement` cannot transition into BUILD.
**If removed:** Planner defaults begin masquerading as approved requirements again.
**Safe to remove:** Never.

### INV-016: Phase exit is the only way BUILD advances
**Covers:** Router `## 6. Workflow Task Graphs`, `## 8. Post-Agent Validation`, `## 12. Chain Execution Loop`
**Enforces:** BUILD advances `phase_cursor` only after RED, GREEN, and phase-exit evidence are complete with no unresolved blocked items.
**If removed:** BUILD can skip steps, reorder work, or continue after partial execution.
**Safe to remove:** Never.

### INV-017: Internal skills are advisory
**Covers:** Router `## 7. Dispatcher And Agent Prompt Contract`, internal skills
**Enforces:** Explicit user instructions, `CLAUDE.md`, repo standards, and approved plans outrank CC10X internal skills.
**If removed:** `frontend-patterns` / `architecture-patterns` / `debugging-patterns` can silently compete with user intent again.
**Safe to remove:** Never.

### INV-018: Agents use only the v10 state namespace
**Covers:** Router `## 2. Memory Load And Template Validation`, agent memory-read sections
**Enforces:** BUILD / DEBUG / REVIEW / VERIFY agents read from `.claude/cc10x/v10/*.md` only and never mix legacy memory paths into active orchestration.
**If removed:** Agents can read stale state, leak legacy decisions into live workflows, or disagree about the active workflow memory surface.
**Safe to remove:** Never.

### INV-019: Verification is independent of upstream approval
**Covers:** Router `## 8. Post-Agent Validation`, verifier contract, BUILD chain
**Enforces:** Reviewer approval, hunter CLEAN, or builder success are inputs to verification, not substitutes for independent scenario proof.
**If removed:** The workflow can regress into self-certified completion where one agent's confidence is mistaken for verification.
**Safe to remove:** Never.

### INV-020: Silent-failure analysis must state scan coverage truthfully
**Covers:** Router `## 8. Post-Agent Validation`, hunter contract
**Enforces:** The silent-failure hunter must describe scanned scope and blind spots before a CLEAN result is accepted.
**If removed:** CLEAN verdicts can hide incomplete search coverage and create false confidence in error-handling quality.
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
