# CC10x Router Behavioral Invariant Registry

> **Status note:** Aligned to the `v12.10.0` product line as released on 2026-10-07 (v12.10.0; the release before it was v12.9.1), against `plugins/cc10x/skills/cc10x-router/SKILL.md`, `plugins/cc10x/skills/cc10x-router/references/*.md` and `plugins/cc10x/hooks/hooks.json`. Release history lives in `CHANGELOG.md`. Invariants for the QA route, ORIENT, the seam gate and the git guard are registered below.

## Purpose

This file maps each load-bearing router behavior to the failure it prevents.
If a router section changes, the matching invariant must be updated in the same change.

## Audit Snapshot

Validated against the live plugin surface:

- workflow artifacts under `.cc10x/workflows/{wf}.json`
- workflow event logs under `.cc10x/workflows/{wf}.events.jsonl`
- plugin hooks in `plugins/cc10x/hooks/hooks.json`
- router-owned remediation creation
- bounded fresh planning review via `plan-gap-reviewer`
- fail-closed scenario evidence rules for BUILD / DEBUG / VERIFY
- memory finalization and transient `memory_task_id`
- agent memory reads under `.cc10x/*.md`
- verifier independence from builder/reviewer/hunter verdicts
- router kernel plus mandatory workflow/reference playbooks
- the QA route, its phase sets and the QA isolation guard
- the ORIENT move
- the builder seam gate (`TEST_SEAMS`, `SEAM_GATE_STATUS`)
- the git guard (`classify_git_command`)

## Current Invariants

### INV-027: Router kernel must explicitly load mandatory references

**Covers:** Router `## 2a. Workflow Artifact And Hook Policy`, `## 5. Workflow Preparation`, `## 6. Workflow Task Graphs`, and `plugins/cc10x/skills/cc10x-router/references/*.md`
**Enforces:** Universal orchestration law stays inline in the router kernel while workflow-specific and appendix-heavy law remains in one-level-deep references that are named explicitly at each decision point.
**If removed:** Either the router swells back into a monolith, or branch-specific orchestration rules become optional context that Claude may skip under pressure.
**Safe to remove:** Never.

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

### INV-026: Fresh planning review is bounded and planner-owned

**Covers:** Router `## 5. Workflow Preparation`, `## 9. Remediation And Workflow Rules`, planner, `plan-gap-reviewer`
**Enforces:** Every PLAN workflow pre-creates a DAG-visible bounded fresh-review chain (`plan-create -> plan-review-gap-1 -> re-plan -> plan-review-gap-2 -> memory-finalize`) capped at two `REVIEW_MODE: fresh` passes. Amendments to a saved plan are verified by an on-demand `plan-review-amendment` task (`REVIEW_MODE: amendment`) that is not pre-created, is uncapped, does not count against the fresh-pass cap and cannot close the review loop; `PLANNING_REVIEW_STATUS: passed` needs `plan_revision == last_reviewed_revision`. The planner remains the only writer and the router the only orchestration owner.
**If removed:** PLAN can drift into hidden dynamic orchestration, ambiguous plan ownership, unreviewed amendments, or open-ended token-heavy refinement loops that are not auditable from the task graph.
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

**Covers:** Router `## 2a. Workflow Artifact And Hook Policy`, `## 6. Workflow Task Graphs`, `references/workflow-artifact-and-hook-policy.md`
**Enforces:** Every workflow gets a JSON artifact and append-only event log under the `.cc10x/` state root as soon as the workflow UUID is known.
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

**Covers:** Router `## 9. Remediation And Workflow Rules`, `## 11. Re-Review Loop`, `references/remediation-and-research.md`
**Enforces:** `kind:remfix` counting, re-review task creation, and cycle limits all use the current `wf` scope.
**If removed:** Remediation loops can count unrelated tasks, overrun, or deadlock in shared task lists.
**Safe to remove:** Never.

### INV-007: Research quality is durable, not conversational

**Covers:** Router `## 10. Research Orchestration`, `## Research Quality`, `## Research Files`, `references/remediation-and-research.md`
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
**If removed:** Skills such as `frontend`, `architecture` and `debugging` can silently compete with user intent again.
**Safe to remove:** Never.

### INV-018: Agents use only the `.cc10x/` state namespace

**Covers:** Router `## 2. Memory Load And Template Validation`, agent memory-read sections
**Enforces:** BUILD / DEBUG / REVIEW / VERIFY agents read from `.cc10x/*.md` only and never mix legacy memory paths (`.claude/cc10x/`, `.cc10x/v10/`) into active orchestration.
**If removed:** Agents can read stale state, leak legacy decisions into live workflows, or disagree about the active workflow memory surface.
**Safe to remove:** Never.

### INV-019: Verification is independent of upstream approval

**Covers:** Router `## 8. Post-Agent Validation`, verifier contract, BUILD chain
**Enforces:** Reviewer approval, hunter CLEAN, or builder success are inputs to verification, not substitutes for independent scenario proof.
**If removed:** The workflow can regress into self-certified completion where one agent's confidence is mistaken for verification.
**Safe to remove:** Never.

### INV-020: Failure analysis must state scan coverage truthfully

**Covers:** Router `## 8. Post-Agent Validation`, `failure-hunter` contract
**Enforces:** The `failure-hunter` must describe scanned scope and blind spots before a CLEAN result is accepted.
**If removed:** CLEAN verdicts can hide incomplete search coverage and create false confidence in error-handling quality.
**Safe to remove:** Never.

### INV-012: Memory finalization is router-owned and compaction-safe

**Covers:** Router `## 12. Chain Execution Loop`, `## 13. Memory Finalization`, `references/build-workflow.md`, `references/debug-workflow.md`, `references/review-workflow.md`, `references/plan-workflow.md`
**Enforces:** Read-only Memory Notes are copied into the memory task immediately; final persistence happens inline through the Memory Update task; transient `memory_task_id` is removed on completion; and a `kind:memory` task is not considered trustworthy unless the workflow event log records `memory_finalized`.
**If removed:** Memory becomes conversation-dependent or leaks stale workflow pointers across sessions.
**Safe to remove:** Never.

### INV-013: Plugin hooks are guardrails, not orchestration

**Covers:** Router `## 2a. Workflow Artifact And Hook Policy`, `references/workflow-artifact-and-hook-policy.md`, plugin hooks
**Enforces:** `hooks.json` registers ten events, and every hook stays a guard, an audit, a context injection or a state snapshot, never a second orchestrator. `plugins/cc10x/hooks/README.md` lists each hook once and is the maintained table:

- `PreToolUse`: the memory-write guard (audit by default), the git guard and the QA isolation guard (both unconditional blockers)
- `SessionStart`: the Python preflight and resume-context injection
- `PostToolUse`: workflow artifact integrity (`artifactIntegrity`, ships as block) and Bash workflow-write audit
- `TaskCompleted`: task metadata and memory-finalize evidence (`taskMetadata`, ships as audit)
- `PostCompact`, `SubagentStop`, `StopFailure`, `InstructionsLoaded`: audit logging
- `PreCompact`, `Stop`: workflow state snapshots
**If removed:** Either runtime safety degrades, or hooks sprawl into a second orchestration system.
**Safe to remove:** Only if an equivalent plugin-native guardrail replaces the specific hook behavior.

### INV-014: Workflow replay fixtures are part of the safety contract

**Covers:** `plugins/cc10x/tools/workflow_replay_check.py`, `plugins/cc10x/tests/fixtures/`
**Enforces:** PLAN / BUILD / DEBUG / REVIEW / VERIFY / QA / TRIAGE / CODEBASE-HEALTH decision paths are regression-checked without relying on a live Claude session.
**If removed:** Future router/prompt edits can regress core orchestration behavior without a deterministic detection path.
**Safe to remove:** Never.

### INV-028: QA phase sets keep planning read-only and preflight able to provision

**Covers:** Router `## 3. Task Metadata Contract` (phase enum), `references/qa-workflow.md`, `plugins/cc10x/scripts/cc10x_qa_isolation_guard.py`, `plugins/cc10x/scripts/test_cc10x_qa_phase_invariants.py`
**Enforces:** The QA planning phases (`qa`, `qa-research`, `qa-plan`, `qa-plan-review`, `qa-re-plan`, `qa-plan-review-2`) deny environment mutation, while `qa-preflight` is deliberately outside that set so it can probe the real environment; the router sets `phase_cursor` to `qa-preflight` before dispatching it. A quarantined path declared by the workflow is refused for reads in both directions (named path, and a search root that contains it). The guard resolves the phase from every `status_history` shape without failing open on legacy artifacts.
**If removed:** Planning phases can provision or mutate the environment, or preflight is silently blocked from the one thing it exists to do; either failure prints nothing.
**Safe to remove:** Never. The phase-set properties are asserted by `test_cc10x_qa_phase_invariants.py` (release-gate step `suite_qa_phase_invariants`).

### INV-029: QA route law is single-sourced and enumerations agree

**Covers:** Router `## 1. Intent Routing`, `## 3. Task Metadata Contract`, `## 6. Workflow Task Graphs`, `## 7. Dispatcher And Agent Prompt Contract`, `references/qa-workflow.md`, `references/workflow-artifact-and-hook-policy.md`
**Enforces:** Every `phase:` token in `qa-workflow.md` and `plan-workflow.md` is in the phase enum; every dispatchable QA phase has exactly one dispatcher row; every `origin:` value the route law writes is in the origin enum; QA is a member of every enumeration of workflow types; every filesystem path the QA law names resolves; the QA phase-token spellings are frozen. The same suite checks that the harness PASS rule (`assertion_falsified`, `survived`, `LIVENESS_PROBES`) agrees between the harness builder and the hook-policy reference, and that the revision-pair guard on the workflow artifact rejects inconsistent `planning_review_status` writes.
**If removed:** The route gains a phase no dispatcher row handles, an origin no enum admits, or two copies of a rule that disagree, and nothing fails until a live QA run.
**Safe to remove:** Never. Asserted by `test_cc10x_qa_phase_invariants.py`.

### INV-030: QA loops are bounded and no QA finding goes unconsumed

**Covers:** `references/qa-workflow.md`, `plugins/cc10x/scripts/test_cc10x_qa_phase_invariants.py`
**Enforces:** The QA re-dispatch loops are bounded and counted; no QA finding reaches the executor unconsumed and no Minor finding evaporates; a defect found at any QA phase reaches the sink the DEBUG offer reads; no QA phase holds a write tool without a stated product-code boundary; the measure-before-you-ask step precedes the research fan-out.
**If removed:** QA can loop without a cap, drop findings, or let a write-capable phase edit product code.
**Safe to remove:** Never. Asserted by `test_cc10x_qa_phase_invariants.py`.

### INV-031: ORIENT is read-only and spawns no agents

**Covers:** Router `## 1. Intent Routing` (priority 4 and the `### ORIENT move (read-only)` block), `## 2a. Workflow Artifact And Hook Policy`
**Enforces:** A request to understand existing code is answered inline: no `TaskCreate`, no new workflow artifact, no phase graph, no write agent. A pre-created `workflow_type: pending` artifact is closed as `ORIENT` with `phase_cursor` `orient` and no graph. A follow-up change request is re-routed from scratch. The deliverable decides between ORIENT and REVIEW ("explain" versus "what is wrong"); only a genuine tie goes to REVIEW.
**If removed:** "Help me understand this code" falls through to DEFAULT and spawns a write builder, or ORIENT quietly grows task state.
**Safe to remove:** Never.

### INV-032: The builder seam gate is enforced by the contract override

**Covers:** `references/workflow-artifact-and-hook-policy.md` (component-builder contract fields and override), `references/build-workflow.md` (`test_seams` on each phase), `plugins/cc10x/agents/component-builder.md`, `plugins/cc10x/tools/workflow_replay_check.py`, `docs/adr/0001-enforced-seam-gate.md`
**Enforces:** The builder contract carries `TEST_SEAMS` and `SEAM_GATE_STATUS` (`confirmed`, `proposed`, `disagreed`, `not_applicable`) and the router validates them per `build_scope`: a standard plan phase with `test_seams` is `confirmed` or `disagreed`; a standard legacy phase or a direct build is `proposed`; a trivial build is `not_applicable`. `disagreed` with empty `TEST_SEAMS` is valid only as the ambiguity block (`STATUS=FAIL` plus the exact remediation reason). The replay check rejects a builder PASS fixture without `SEAM_GATE_STATUS`.
**If removed:** Builders stop declaring where they tested, and a rubber-stamped `disagreed` skips the gate.
**Safe to remove:** Never.

### INV-033: The git guard is default-deny for destructive git text

**Covers:** `plugins/cc10x/scripts/cc10x_git_guard.py` (`classify_git_command`), `plugins/cc10x/hooks/README.md` (Git guard limits), `plugins/cc10x/scripts/test_cc10x_guards.py`
**Enforces:** The guard denies the destructive set (push, hard reset, forced clean, forced branch delete, discard-all checkout and restore, stash clear) over the raw command text and over wrapper, chain, substitution and nested-shell forms. Destructive text is allowed only as quoted data in one strict pipeline allowance (`echo`, `printf` or `grep` family feeding plain text filters, with no redirect, group, loop or substitution); every other command gets the full pattern list. A command over 64 KB (65,536 characters) that names `git` as a word is denied as `command-too-large` before any pattern runs, and nesting past eight levels is denied. A classifier crash denies any command containing `git`. Only remote publish and branch force-delete can be unlocked, by a single-use approval token under `.cc10x/state/`; a command mixing an unlockable with a non-unlockable operation is denied as the non-unlockable one. The guard is a text heuristic that protects against accidents; the token is a plain file and is not a defended boundary.
**If removed:** A destructive git command runs without the user's explicit finishing choice, or the quadratic legacy pattern times out and fails open.
**Safe to remove:** Never.

## Legacy Appendix

Pre-`v9.x` invariants were reorganized rather than preserved one-for-one. Historical context remains in git history. The current source of truth is this live registry plus:

- `plugins/cc10x/skills/cc10x-router/SKILL.md`
- `plugins/cc10x/tools/harness_audit.py`
- `plugins/cc10x/tools/workflow_replay_check.py`
