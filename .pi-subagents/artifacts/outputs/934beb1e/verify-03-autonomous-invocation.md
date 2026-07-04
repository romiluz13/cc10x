# Verification 03 — Autonomous Invocation

**Scope:** Does every cc10x workflow activate without manual intervention, and do the supporting hooks fire automatically?

**Source of truth examined:**

- `plugins/cc10x/skills/cc10x-router/SKILL.md` (all 752 lines)
- `references/build-workflow.md`, `debug-workflow.md`, `review-workflow.md`, `plan-workflow.md`
- `references/remediation-and-research.md`
- `references/workflow-artifact-and-hook-policy.md`
- `references/workflow-artifact.skeleton.json`
- `hooks/hooks.json`
- `scripts/cc10x_sessionstart_context.py`
- `scripts/cc10x_posttooluse_artifact_guard.py`
- `scripts/cc10x_task_completed_guard.py`
- `scripts/cc10x_state_persist.py`
- `scripts/cc10x_event_logger.py`
- `agents/*.md` (agent definitions present for every dispatched role)

---

## 1. BUILD workflow — PASS

**Trace: user request → router detection → workflow creation → agent dispatch → completion**

1. **Detection:** §1 Intent Routing table — DEFAULT (priority 5) routes everything not matching ERROR/PLAN/REVIEW/ORIENT to BUILD. Keywords: build, implement, create, write, add, refactor, optimize, update, change, test. The router emits `-> BUILD workflow (signals: {matched keywords})`.
2. **Memory load + readiness:** §2 loads `.cc10x/activeContext.md`, `patterns.md`, `progress.md`; §5 reads `references/build-workflow.md` before any BUILD-specific decision; the Intent Readiness Gate (§5) checks context-bounded, contradiction-free, sufficiently-specific.
3. **Workflow artifact creation:** §6 Parent workflow creation — generates `workflow_uuid` → `TaskCreate` parent task with full 7-line metadata → copies `workflow-artifact.skeleton.json` to `.cc10x/workflows/{wf}.json` → fills placeholders via `Edit(replace_all=true)` → writes the first `workflow_started` event to `{wf}.events.jsonl` → mandatory read-back gate confirms JSON parses, UUID matches, no `__PLACEHOLDER__` tokens remain.
4. **Task graph creation:** `references/build-workflow.md` defines two graphs:
   - **Trivial** (`build_scope=trivial`): builder → verifier → memory (reduced chain).
   - **Standard** (default, always when a plan exists): builder → [reviewer ‖ hunter] → verifier → doc-syncer → memory. Reviewer and hunter are both `blockedBy: [builder_task_id]` and run in parallel (§12 step 5: "mark both in_progress first, invoke them in the same message"). Verifier is `blockedBy: [reviewer_task_id, hunter_task_id]`. Doc-syncer is `blockedBy: [verifier_task_id]`. Memory is `blockedBy: [doc_sync_task_id]` (or directly on verifier when `DIFF_DRIVEN_DOCS: skip`).
5. **Dispatch:** §7 dispatcher table maps `build-implement` → `cc10x:component-builder`, `build-review`/`re-review` → `cc10x:code-reviewer`, `build-hunt`/`re-hunt` → `cc10x:silent-failure-hunter`, `build-verify`/`re-verify` → `cc10x:integration-verifier`, `build-doc-sync` → `cc10x:doc-syncer`. All agents exist under `plugins/cc10x/agents/`.
6. **Chain execution loop:** §12 runs `TaskList()` → selects runnable tasks (pending/in_progress, blockers resolved) → dispatches → validates output → persists results → applies workflow rules → repeats until all tasks complete. No user interaction between phases.
7. **Completion:** Memory task runs inline (§12 step 3, §13) — persists to `.cc10x/*.md`, appends `memory_finalized` event, marks parent workflow completed.

**Autonomy gaps:** None. The full chain runs without user intervention. The only optional user-touch points are: (a) workspace isolation offer (step 0, skippable under JUST_GO or when no native primitive exists), (b) BUILD-DONE finishing menu (optional, auto-defaults to "keep as-is" under JUST_GO, and never blocks Memory Update), (c) scope-decision gate (`1a-SCOPE`) which only fires when reviewer/hunter report BOTH CRITICAL and HIGH issues — a genuine ambiguity gate, not a routine checkpoint. The trivial path has zero user gates. The standard path has the `plan_trust_gate` which halts only when the plan has unresolved Open Decisions — a correctness gate, not a missing autonomy feature.

**Verdict: PASS** — The BUILD workflow can be autonomously invoked, create its artifact, dispatch the builder, run the full chain, and complete without user intervention for the normal case.

---

## 2. DEBUG workflow — PASS

**Trace:**

1. **Detection:** §1 Intent Routing — Priority 1 (ERROR) — keywords: error, bug, fix, broken, crash, fail, debug, troubleshoot, issue. ERROR always wins over BUILD. The "primary deliverable" rule clarifies that "add X and fix Y" is BUILD, not DEBUG — DEBUG is for when diagnosing/repairing broken behavior IS the deliverable.
2. **Memory load + preparation:** §5 reads `references/debug-workflow.md`. DEBUG preparation writes `[DEBUG-RESET: wf:{workflow_uuid}]` once the workflow id exists; preserves failed-attempt counting semantics.
3. **Workflow artifact creation:** Same §6 parent workflow creation pattern — UUID generation, parent task, skeleton copy, placeholder fill, read-back gate, event log write.
4. **Task graph:** `references/debug-workflow.md` — `debug-investigate` (bug-investigator) → `debug-review` (code-reviewer, blockedBy investigator) → `debug-verify` (integration-verifier, blockedBy reviewer) → `memory-finalize` (inline, blockedBy verifier). Sequential chain, no parallel agents.
5. **Dispatch:** §7 dispatcher table: `debug-investigate` → `cc10x:bug-investigator`, `debug-review` → `cc10x:code-reviewer`, `debug-verify` → `cc10x:integration-verifier`.
6. **Chain execution:** §12 loop runs the sequential chain. Investigator can self-remediate or request continuation (remediation-and-research.md §Investigator continuation: up to 2 continuation tasks before asking the user). Remediation creates REM-FIX tasks with circuit breaker (count ≥ 3 → human checkpoint).
7. **Completion:** Memory task runs inline, persists debug learnings, preserves `[DEBUG-RESET:]` marker in `## Recent Changes`.

**Autonomy gaps:** None for the normal case. User intervention is required only on: (a) verifier REVERT gate (§9 Rule 2d — FAIL + REVERT → ask user revert vs fix), (b) circuit breaker at 3 remediation cycles, (c) investigator blocked → ask research/manual/abort (§9 Rule 2f), (d) investigator needs external research → spawns research tasks and re-invokes (autonomous). These are all genuine ambiguity/failure-stop gates, not missing automation.

**Verdict: PASS** — The DEBUG workflow detects errors, creates the workflow, dispatches the bug-investigator, and runs investigator → reviewer → verifier → memory autonomously.

---

## 3. REVIEW workflow — PASS

**Trace:**

1. **Detection:** §1 Intent Routing — Priority 3 (REVIEW) — keywords: review, audit, analyze, assess, "is this good". REVIEW is advisory only; it never creates code-changing tasks.
2. **Preparation:** §5 reads `references/review-workflow.md`. REVIEW preparation: advisory only, never create REM-FIX or implementation tasks directly.
3. **Workflow artifact creation:** Same §6 pattern.
4. **Task graph:** `references/review-workflow.md` — single `review-audit` task (code-reviewer) → `memory-finalize` (inline, blockedBy reviewer). Minimal two-node graph.
5. **Dispatch:** §7 dispatcher table: `review-audit` → `cc10x:code-reviewer`.
6. **Chain execution:** §12 loop — reviewer runs, router owns completion fallback for read-only tasks (step 3 of "After every agent completion"), memory task runs inline.
7. **Post-review:** If verdict is `CHANGES_REQUESTED`, router may offer "Start BUILD to fix" as a follow-up user choice — but this is a transition offer, not a gap in the REVIEW workflow itself.

**Autonomy gaps:** None. The REVIEW workflow is a single-agent advisory chain that runs start-to-finish without user intervention. The post-review BUILD offer is an optional transition, not a required step.

**Verdict: PASS** — The router detects review requests and dispatches the code-reviewer autonomously.

---

## 4. PLAN workflow — PASS

**Trace:**

1. **Detection:** §1 Intent Routing — Priority 2 (PLAN) — keywords: plan, design, architect, roadmap, strategy, spec, brainstorm. Native plan mode (EnterPlanMode) is not a substitute but its output is ingested as `plan_file`.
2. **Preparation:** §5 reads `references/plan-workflow.md`. PLAN preparation includes: restoring design enrichment, **mandatory brainstorming** (`Skill(skill="cc10x:exploration")` always runs before planner), optional research offer, planner is agreement-first.
3. **Workflow artifact creation:** Same §6 pattern.
4. **Task graph:** `references/plan-workflow.md` — pre-creates the full bounded fresh-review DAG:
   - `plan-create` (planner) → `plan-review-gap-1` (plan-gap-reviewer, blockedBy planner) → `re-plan` (planner, blockedBy gap-1) → `plan-review-gap-2` (plan-gap-reviewer, blockedBy re-plan) → `memory-finalize` (inline, blockedBy all four).
   - If pass 1 succeeds: router prunes `re-plan` and `plan-review-gap-2` (mark deleted/completed with "pruned — unused review branch"), verifies memory task unblocks.
   - If pass 1 finds blocking issues: `re-plan` and pass 2 branch stay alive.
   - Maximum fresh-review passes: 2.
5. **Dispatch:** §7 dispatcher table: `plan-create`/`re-plan` → `cc10x:planner`, `plan-review-gap-1`/`plan-review-gap-2` → `cc10x:plan-gap-reviewer`.
6. **Chain execution:** §12 loop runs the DAG. Remediation-and-research.md §Planner clarification handles `STATUS=NEEDS_CLARIFICATION` (prunes unused branch, asks user, restarts PLAN with fresh DAG) and `STATUS=PLAN_CREATED`/`DECISION_RFC_CREATED` (verifies plan file, extracts intent, updates task `plan:` lines).
7. **Completion:** Memory task runs inline, indexes plan in memory (`activeContext.md ## References`, `## Recent Changes`, `## Next Steps`).

**Autonomy gaps:** None for the normal case. User intervention is required only on: (a) planner returns `NEEDS_CLARIFICATION` (genuine ambiguity), (b) pass 2 returns `FINDINGS` (unresolved plan contradiction → `pending_gate=clarification`), (c) optional research offer (user can decline). The pruning logic for pass-1-success is fully autonomous — the router marks tasks deleted/completed and verifies memory unblocks without user input.

**Verdict: PASS** — The router detects planning requests, dispatches the planner, and runs the fresh-review DAG (plan → gap-review-1 → [re-plan → gap-review-2] → memory) autonomously.

---

## 5. ORIENT workflow — PASS

**Trace:**

1. **Detection:** §1 Intent Routing — Priority 4 (ORIENT) — keywords: zoom out, explain, understand, "how does X work", unfamiliar, "map this", "walk me through", "where is", "what does this do". ORIENT precedes DEFAULT/BUILD so "help me understand this code" never falls through to BUILD.
2. **Execution:** The ORIENT move (§1) is explicitly read-only and inline — **no `TaskCreate`, no workflow artifact, no phase graph, no write agents**. The router answers inline using `localViewStructure`, `localFindFiles`, `localSearchCode`, `lspCallHierarchy`, `lspFindReferences`.
3. **Procedure:** (1) Map relevant modules/files, (2) trace one layer up via LSP, (3) explain in project's own vocabulary, (4) stop at understanding. If a change is clearly implied, offer to route it (BUILD/DEBUG/PLAN) — do not start it.
4. **Distinction from REVIEW:** ORIENT explains structure and flow; REVIEW judges quality. When both could match, prefer ORIENT for "help me understand", REVIEW for "tell me what's wrong".

**Autonomy gaps:** None. ORIENT is inherently autonomous — it's a read-only inline response with no agent dispatch and no workflow state. The only user interaction is the optional offer to route a follow-up change request at the end.

**Verdict: PASS** — The router detects orientation requests and runs read-only without spawning agents.

---

## 6. SessionStart hook injects workflow context for resume — PASS

**Evidence:** `hooks/hooks.json` defines a `SessionStart` hook with matcher `startup|resume|compact` that runs `scripts/cc10x_sessionstart_context.py`. The script:

- Calls `latest_workflow_payload()` to read the most recent workflow artifact.
- Extracts `pending_gate`, `phase_status`, incomplete phases, `workflow_uuid`, `workflow_type`, `plan_file`, `design_file`, `phase_cursor`, `research_quality`.
- Constructs a context message and injects it via `session_context(message)`.
- Logs a `session_context` event with `decision: inject`.

This fires on all three trigger types (startup, resume, compact), providing the router with workflow context for resume decisions. When no workflow exists, it returns 0 silently.

**Verdict: PASS**

---

## 7. Resume logic for interrupted workflows — PASS

**Evidence:** §4 Resume And Hydration defines a complete resume algorithm:

1. **Memory load first** (§2), then `TaskList()`.
2. **Hydration rules:** Find active parent workflow tasks by subject prefix (`CC10X BUILD:`, `CC10X DEBUG:`, etc.). Scope by `wf:` markers. Reconstruct runnable tasks from `TaskList()` and `TaskGet()` using `wf:` + `kind:` + `phase:` — never rely on stored task IDs.
3. **Stop/PreCompact hint:** Step 0 reads `.cc10x/stop-state.json` or `.cc10x/precompact-state.json` (written by `scripts/cc10x_state_persist.py` on Stop/PreCompact hooks) as a HINT for which `wf:` and `phase_cursor` were live. It's a hint only — task metadata and the workflow artifact stay authoritative; discard on mismatch.
4. **Resume algorithm steps 1-5:** Identify active parent → extract `workflow_uuid` → read all CC10X tasks with that `wf:` → derive runnable tasks from `status` and `blockedBy` → reconstruct memory task as unique pending/in_progress `kind:memory` in same `wf:`.
5. **Scope-decision resume:** Checks `activeContext.md ## Decisions` for `[SCOPE-DECISION-PENDING: wf:{...}]` marker. If present, treats the current user reply as the answer to the pending BUILD scope gate.
6. **Safety rules:** Always scope by `wf:` before resuming. `in_progress` + unresolved blockers = waiting on remediation. `in_progress` + no blockers = ask user. Legacy tasks without `CC10X` prefix = ask user.
7. **Stale memory_task_id handling:** `[cc10x-internal] memory_task_id` is transient only — if missing/stale/different `wf:`, ignore and reconstruct from current workflow scope. Never use unscoped fallback like "first pending Memory Update task".

The `cc10x_state_persist.py` script writes snapshots on PreCompact and Stop events containing `workflow_uuid`, `workflow_type`, `phase_cursor`, `phase_status`, `plan_file`. The SessionStart hook (item 6) injects this context on resume.

**Verdict: PASS**

---

## 8. Memory-finalize task runs automatically at workflow end — PASS

**Evidence:**

1. **Every workflow task graph includes a memory task:** BUILD (both trivial and standard graphs), DEBUG, REVIEW, and PLAN all end with a `kind:memory` `phase:memory-finalize` task blocked by the last agent task.
2. **§12 Chain Execution Loop step 3:** "If the runnable task kind is memory: execute inline in the main context, persist workflow artifact results + Memory Notes, append `memory_finalized` to events, clean up `[cc10x-internal] memory_task_id`, mark memory task completed, mark parent workflow task completed, continue."
3. **§13 Memory Finalization:** The memory task reads the workflow artifact (not conversation history), persists to `activeContext.md ## Learnings`, `patterns.md ## Common Gotchas`, `progress.md ## Verification`, replaces `progress.md ## Tasks`, trims `## Completed` to 10, removes `[cc10x-internal] memory_task_id` line. PLAN and DEBUG have specialized finalization steps.
4. **§14 Hard Rules:** "Never spawn Memory Update as a sub-agent." — memory always runs inline in the router.
5. **TaskCompleted guard** (`cc10x_task_completed_guard.py`): validates that memory tasks have `origin=router`, the "ROUTER ONLY: execute inline." marker, subject starting "CC10X Memory Update:", and that `memory_finalized` event exists in the event log. In block mode, it rejects (exit 2) memory task completion without this evidence.

**Verdict: PASS**

---

## 9. Event log appended automatically (via PostToolUse guard) — PASS

**Evidence:**

1. **Router-side (primary):** §12 "After every agent completion" step 6 mandates: "For each result persisted to the artifact, append a matching entry to `.cc10x/workflows/{wf}.events.jsonl`" with `event: result_persisted` and agent-specific metadata. The router also writes `workflow_started` on creation and `memory_finalized` on completion.
2. **PostToolUse guard (fallback):** `scripts/cc10x_posttooluse_artifact_guard.py` — when the written file IS a workflow artifact and it passes validation, the guard **auto-appends an `artifact_mutated` event** to the event log:

   ```python
   workflow_event_log_append(wf_id, {
       "ts": now_iso(), "wf": wf_id, "event": "artifact_mutated",
       "phase": payload.get("phase_cursor", "unknown"),
       "agent": "hook", "decision": "auto-logged",
       "reason": "posttool_guard_auto_append",
   })
   ```

   This ensures every artifact write gets a matching event log entry even if the router skips it under context pressure.
3. **Missing event log detection:** The guard checks `workflow_event_log_exists()` and reports `missing-event-log` as a reason (audit-only, not blocking) if absent.
4. **PostCompact hook:** `scripts/cc10x_event_logger.py` postcompact mode appends a `compact_occurred` event to the workflow event log.

The event log contract (§2a / workflow-artifact-and-hook-policy.md) specifies required fields: `ts`, `wf`, `event`, `phase`, `task_id`, `agent`, `decision`, `reason`. Event types include `workflow_started`, `agent_started`, `agent_completed`, `contract_parsed`, `remediation_created`, `scope_decision_requested/resolved`, `memory_finalized`, `workflow_completed`, `workflow_failed`.

**Verdict: PASS**

---

## 10. Artifact freshness check after every task completion — PASS

**Evidence:** `scripts/cc10x_task_completed_guard.py` function `check_artifact_freshness()`:

1. **Trigger:** Runs after every non-memory CC10X task completes (the `main()` function calls it after metadata validation and memory-task validation pass).
2. **Check:** Reads the workflow artifact via `read_workflow_state(workflow_id)`, then calls `workflow_artifact_is_fresh(artifact_path, max_age_seconds=300)`. If the artifact hasn't been touched in 5+ minutes after a task completes, it's flagged as stale.
3. **Action:** Logs a `task_completed_stale_artifact` event with `decision: audit` and writes a warning to stderr: "CC10X WARNING: workflow artifact {name} appears stale after task completion... Ensure the router updates the artifact with agent results before proceeding."
4. **Design note:** The check is audit-only (not blocking) because the model may update the artifact in the next turn. But the audit log entry creates an observable signal for stress tests.
5. **Complementary router-side check:** §12 "After every agent completion" step 5 includes a MANDATORY read-back gate: "After writing the artifact, Read it back and confirm: `updated_at` is set to a timestamp from THIS turn, `results.{agent_name}` exists. If either check fails, rewrite the artifact immediately."
6. **PostToolUse guard also checks freshness:** `cc10x_posttooluse_artifact_guard.py` calls `workflow_artifact_is_fresh(artifact_path)` when the write target is the artifact itself, and reports `stale-artifact-write` (audit-only).

**Verdict: PASS** — The freshness check runs automatically after every task completion via the TaskCompleted guard, with complementary checks in the PostToolUse guard and the router's own mandatory read-back gate.

---

## Summary Table

| # | Verification Item | Verdict | Key Evidence |
| --- | --- | --- | --- |
| 1 | BUILD workflow autonomous invocation | **PASS** | §1 routing, §6 artifact creation, build-workflow.md full task graph, §7 dispatcher, §12 chain loop, §13 memory |
| 2 | DEBUG workflow autonomous invocation | **PASS** | §1 priority-1 ERROR routing, debug-workflow.md task graph, §7 dispatcher, §12 chain loop |
| 3 | REVIEW workflow autonomous invocation | **PASS** | §1 priority-3 routing, review-workflow.md single-agent graph, advisory-only constraint |
| 4 | PLAN workflow autonomous invocation | **PASS** | §1 priority-2 routing, plan-workflow.md bounded fresh-review DAG, pruning logic, §7 dispatcher |
| 5 | ORIENT workflow autonomous invocation | **PASS** | §1 priority-4 routing, inline read-only move, no TaskCreate/artifact/agents |
| 6 | SessionStart hook injects resume context | **PASS** | hooks.json SessionStart matcher, cc10x_sessionstart_context.py |
| 7 | Resume logic for interrupted workflows | **PASS** | §4 resume algorithm, stop-state/precompact-state hints, wf-scoped hydration |
| 8 | Memory-finalize runs automatically at workflow end | **PASS** | Every graph includes memory task, §12 step 3 inline execution, §13 finalization, TaskCompleted guard |
| 9 | Event log appended automatically | **PASS** | §12 step 6 router-side, PostToolUse guard auto-append fallback |
| 10 | Artifact freshness check after every task | **PASS** | TaskCompleted guard check_artifact_freshness(), PostToolUse guard, router read-back gate |

**Overall: 10/10 PASS.** Every workflow can be autonomously invoked from user request through completion without manual intervention for the normal (non-ambiguity, non-failure) case. User-facing gates that exist (scope-decision, verifier REVERT, circuit breaker, planner clarification, finishing menu) are all genuine ambiguity/failure-stop gates required by the trust-first contract, not missing automation.

---

## Residual Risks

1. **JUST_GO scope-decision gate:** The `1a-SCOPE` gate (BUILD reviewer + hunter report both CRITICAL and HIGH) requires user input even under `JUST_GO` — this is by design (scope changes are irreversible-ish), but means a BUILD that hits this gate will pause. This is a correctness feature, not a defect.
2. **Planner clarification restart:** When planner returns `NEEDS_CLARIFICATION`, the PLAN workflow prunes the unused review branch and asks the user. After the user answers, it restarts PLAN "with a fresh visible DAG." The freshness of the restarted DAG depends on the router correctly pruning and recreating tasks — if the host task system doesn't support deletion, the fallback marks tasks `completed` with "pruned — unused review branch", which could confuse `TaskList()` hydration if the `wf:` scoping is imperfect. Low risk given the `wf:` scoping rules, but observable.
3. **Artifact freshness check is audit-only:** The `check_artifact_freshness()` function in the TaskCompleted guard logs and warns but does not block (exit 2). A stale artifact after task completion will not halt the workflow — it relies on the router's own read-back gate (§12 step 5) to catch and fix it. If the router skips the read-back gate under context pressure, the staleness could persist unnoticed until resume. The PostToolUse guard's `stale-artifact-write` check is also audit-only.
4. **Parallel dispatch fallback:** §12 step 5 specifies that if parallel invocation of reviewer + hunter fails (API error, rate limit), fall back to sequential. This is autonomous, but the `parallel_fallback` event log entry depends on the router remembering to log it — there's no hook-level enforcement of this logging.
5. **Inline fallback mode:** §12 "Inline no-subagent execution" is a bounded degrade mode when the Task/Agent primitive is unavailable or work is tightly-coupled. It forfeits fresh-context isolation and relies on router discipline to re-ground from the artifact between phases. Context bleed is a residual risk in this mode.
