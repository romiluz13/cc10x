## 2a. Workflow Artifact And Hook Policy

CC10X durable orchestration state lives in:

```text
.cc10x/workflows/{workflow_uuid}.json
```

Artifact schema must include:

- `workflow_uuid`
- `workflow_id`
- `workflow_type` — one of `BUILD`, `DEBUG`, `PLAN`, `REVIEW`, `QA`, `ORIENT`, `TRIAGE`, `CODEBASE-HEALTH`, or `pending` (transitional value before routing resolves)
- `state_root`
- `user_request`
- `plan_file`
- `design_file`
- `research_files`
- `approved_decisions`
- `plan_mode`
- `build_scope`
- `worktree`
- `execution_mode`
- `inline_fallback_reason`
- `verification_rigor`
- `proof_status`
- `traceability`
- `intent`
- `capabilities`
- `phase_cursor`
- `normalized_phases`
- `research_rounds`
- `research_backend_history`
- `research_quality`
- `task_ids`
- `phase_status`
- `results`
- `deferred_findings`
- `evidence`
- `source_wf`
- `source_bug_candidate`
- `qa`
- `telemetry`
- `quality`
- `planning_review_runs`
- `planning_review_findings`
- `planning_review_status`
- `plan_revision`
- `last_reviewed_revision`
- `memory_notes`
- `pending_gate`
- `status_history`
- `remediation_history`
- `created_at`
- `updated_at`

Rules:

- Router creates the workflows directory before the first workflow artifact write.
- Router writes or updates the artifact after workflow creation, every agent completion, every remediation decision, every clarification answer, every phase completion, every blocking stop, and memory finalization.
- Resume uses task metadata first, then workflow artifact, then memory markdown.
- Verifier handoff and memory finalization read structured data from the workflow artifact, not transient conversation recovery.
- The workflow UUID is generated independently of Claude task ids and is the canonical workflow identifier everywhere in the orchestration system.
- `workflow_id` remains as a compatibility alias and must equal `workflow_uuid` in new artifacts.
- `state_root` must equal `.cc10x`.
- `phase_cursor` points at the only BUILD phase that may run next.
- `normalized_phases` stores planner-approved executable phases with (the same names `build-workflow.md` BUILD preparation step 8 requires):
  - `phase_id`
  - `title`
  - `objective`
  - `inputs`
  - `files/surfaces`
  - `expected_artifacts`
  - `required_checks`
  - `checkpoint_type`
  - `exit_criteria`
  - `test_seams` — array of seam names the phase tests at. **Required for `build_scope=standard` with a plan** (the builder draws `TEST_SEAMS` from here and sets `SEAM_GATE_STATUS=confirmed`); optional (empty or omitted) for `build_scope=trivial` or direct/no-plan. **Legacy fallback:** a pre-2a saved plan whose phase omits `test_seams` is accepted — the builder sets `SEAM_GATE_STATUS=proposed` and proposes seams at BUILD_PREFLIGHT (same as direct/no-plan), and the next plan-save backfills `test_seams`.
- Bright Data MCP and Octocode MCP are optional accelerators. Base CC10X installs must continue to work with built-in Claude Code tools only.
- When optional user-configured Claude Code MCP servers are available, use the server names `brightdata` and `octocode` so the research agents can auto-detect them without prompt edits.
- `capabilities` records the session-level research backend availability model:
  - `brightdata_available`
  - `octocode_available`
  - `websearch_available`
  - `webfetch_available`
- `results.research` must be structured as `web`, `github`, and `synthesis`.
- `results.disputes_in_flight` is the router-written list of disputed REM-FIX findings, one `{cycle_number, position, finding, ruling}` entry per `FINDING_DISPUTED` position, `ruling` null until the verifier adjudicates it (`remediation-and-research.md`, Re-review precondition gate).
- `intent` stores the durable spec header for the workflow:
  - `goal`
  - `non_goals`
  - `constraints`
  - `acceptance_criteria`
  - `open_decisions`
- `approved_decisions` stores decisions explicitly approved by the user or already fixed in the saved plan.
- `plan_mode`, `verification_rigor`, and `proof_status` mirror the router-owned interface fields from workflow preparation (`direct|execution_plan|decision_rfc`, `standard|critical_path`, `passed|gaps_found|human_needed`).
- `verification_rigor` ships as `null` in the skeleton, meaning undecided. The router must set explicitly `standard` or `critical_path`: `standard` at workflow preparation whenever no plan artifact exists yet (direct BUILD, DEBUG, REVIEW, QA, and PLAN before the planner returns), overwritten from the planner contract once a plan exists. `plan_trust_gate` fails while it is `null` and a plan artifact exists.
- `DIFF_DRIVEN_DOCS: skip` is read by the router from `activeContext.md ## Session Settings` (not from `CLAUDE.md`); when present, BUILD skips doc-sync task creation (`build-workflow.md`, opt-out check).
- `traceability` stores requirement→phase→verification→remediation linkage arrays (`requirements`, `phases`, `verification`, `remediation`).
- `deferred_findings` accumulates non-blocking Minor findings across phases (each entry: `source`, `phase_id`, `finding`, `severity:minor`); never consumed mid-flight, and surfaced once — at BUILD-DONE triage on the BUILD route, and on the QA route with the report, alongside the DEBUG offer, because QA has no BUILD-DONE triage to surface it at. See `build-workflow.md` §Deferred Minor findings roll-up and `qa-workflow.md` *Harness review*.
- `evidence` stores proof-of-work grouped by agent:
  - `builder`
  - `investigator`
  - `reviewer`
  - `hunter` (ACTIVE — the standalone failure-hunter agent's evidence)
  - `verifier`
  - `planning_reviewer` (ACTIVE — the plan-gap-reviewer's evidence, on PLAN and QA alike)
  - `qa_executor` (ACTIVE — the QA route's executor evidence)
- `quality` stores convergence state:
  - `confidence`
  - `evidence_complete`
  - `scenario_coverage`
  - `research_quality`
  - `convergence_state`
- `quality.convergence_state` takes one of `CONVERGENCE_STATES` (defined in `tools/workflow_replay_check.py`, which rejects any other value in a replay fixture): `pending` (default), `needs_iteration`, `converged`, `N/A` (advisory routes with no convergence loop: TRIAGE, CODEBASE-HEALTH).
- PLAN-local fresh review tracking stores:
  - `planning_review_runs`
  - `planning_review_findings`
  - `planning_review_status`
  - `plan_revision`
  - `last_reviewed_revision`
- `plan_revision` and `last_reviewed_revision` are integers, both default `0`, and together decide whether `planning_review_status=passed` is honest:
  - `plan_revision` increments on **every** planner write to the plan file, including a router amendment.
  - `last_reviewed_revision` is set to the then-current `plan_revision` **only** by a completed fresh review pass. Nothing else may write it.
  - `planning_review_status=passed` requires `plan_revision == last_reviewed_revision`. When the two differ, the plan has been changed since the last pass read it and the honest status is `revised_after_review`.
- `telemetry` is informational only and must never drive routing decisions:
  - `task_metrics_available`
  - `workflow_wall_clock_seconds`
  - `agent_wall_clock_seconds`
  - `loop_counts`
  - `verifier`
- `telemetry.agent_wall_clock_seconds` stores per-agent wall-clock timings when task metrics or explicit telemetry are available:
  - `builder`
  - `investigator`
  - `reviewer`
  - `hunter`
  - `verifier`
  - `planner`
- `telemetry.loop_counts` stores:
  - `re_review`
  - `re_hunt`
  - `re_verify`
- `telemetry.verifier` stores:
  - `phase_exit_proof_runs`
  - `extended_audit_runs`
  - `workload_seconds`
- `telemetry.verifier.workload_seconds` stores:
  - `tests`
  - `build`
  - `scan`
  - `reconcile`
  - `reasoning`
- `pending_gate` is required whenever BUILD/PLAN/DEBUG/QA/TRIAGE/CODEBASE-HEALTH is waiting on user clarification, scope selection, or persistence repair. QA sets exactly two: `qa_preflight_human_prerequisites` (the batched preflight ask) and `qa_source_contradiction` (consolidation found sources that disagree about what to test).
- `status_history` is an append-only summary of major router decisions; `remediation_history` holds exactly one entry per remediation round (see `### Circuit breaker` in `remediation-and-research.md`).

Router gates (operational definitions — a gate name without these semantics is meaningless):

- `plan_trust_gate` — before executing any phase from a plan: the plan file exists and passes the checks listed in `build-workflow.md` BUILD preparation step 3 (Open Decisions resolved, Differences from agreement present, explicit `plan_mode` and `verification_rigor`, phase `exit_criteria`, constraint cross-check). That list is the single definition. On failure, stop and ask the user; never build from a plan the artifact no longer trusts.
- `phase_exit_gate` — a phase task may complete only when its agent contract validates (per the Contract overrides table), its result is persisted to `results.{agent}`, and the matching event-log entry exists. A failed contract routes to remediation; it never advances `phase_cursor`.
- `failure_stop_gate` — any agent `FAIL`/`BLOCKED` halts chain advancement. Until it is cleared through remediation, research, or a user checkpoint, the router may not create or unblock downstream phase tasks.
- `memory_sync_gate` — the workflow may not reach final state until Memory Update ran (router-inline, never a subagent) and the `memory_finalized` event is in the event log; the TaskCompleted guard audits exactly this evidence.
- `skill_precedence_gate` — dispatched skills and instructions resolve conflicts by the precedence order (user > project standards > approved plans > domain skills > internal skills > defaults); the router records any conflict it resolved in `status_history`.

These are router-owned checks, not advisory hints. `phase_exit_gate` is enforced by the router, not by any hook: the hooks audit task metadata, artifact shape and memory-finalization evidence, and none of them checks that a phase's contract validated or that `phase_cursor` may advance.

Workflow event log:

- For every workflow, keep a lightweight append-only companion file:

```text
.cc10x/workflows/{workflow_uuid}.events.jsonl
```

- Append event objects with at least:
  - `ts`
  - `wf`
  - `event`
  - `phase`
  - `task_id`
  - `agent`
  - `decision`
  - `reason`
- Optionally append:
  - `duration_seconds`
  - `work_category`
  - `details`
- Event types the router appends:
  - `workflow_started` (at workflow bootstrap)
  - `result_persisted` (each agent result persisted to the artifact; `phase` is the task phase and `details.phase_id` is the `phase_cursor` value, written as the literal `N/A` when `phase_cursor` is null (routes without phases, a BUILD with no plan phases); `decision` is the contract status, written `NEEDS_GRILLING` when a TRIAGED result sets `NEEDS_GRILLING=true`)
  - `phase_started` (BUILD step 11a, once per phase; `details.phase_id` is the `phase_cursor` value)
  - `remediation_created` (one per remediation round, appended with its `remediation_history` entry; `details.phase_id` as above)
  - `memory_finalized` (Memory Update)
  - `inline_fallback_entered` (inline no-subagent mode)
  - `inline_fallback_exited` (the router resumes subagent dispatch)
  - `parallel_fallback` (reviewer and hunter fell back to sequential dispatch)
- `finding_dropped` is a `status_history` entry (post-verifier finding validation, `SKILL.md` §12), not an event-log type.
- Event types a hook appends to this log:
  - `compact_occurred` (PostCompact)
  - `artifact_mutated` (PostToolUse fallback append when the router logged no matching entry)
- Not emitted by any router step or hook (names kept so older artifacts and fixtures stay readable):
  - `agent_started`
  - `agent_completed`
  - `contract_parsed`
  - `scope_decision_requested`
  - `scope_decision_resolved`
- `workflow_completed` and `workflow_failed` are not appended by any router step either; the QA isolation guard accepts them, with `memory_finalized`, as terminal markers when one is present as the last `status_history` event.
- The hook scripts keep a separate log, `cc10x-hook-events.log`, for their own audit lines (`subagent_stop`, `instructions_loaded`, `stop_failure`, guard decisions); those are not workflow events.

Hook policy:

- CC10X plugin hooks live in the plugin bundle under `hooks/hooks.json` and should stay minimal:
  - `PreToolUse` for protected writes (`cc10x_pretooluse_guard.py`)
  - `PreToolUse` for git guardrails (`cc10x_git_guard.py`)
  - `PreToolUse` for QA isolation (`cc10x_qa_isolation_guard.py`) — engages only when the active workflow's `workflow_type` is `QA`, and then blocks three things: reads of denylisted paths, file writes during a planning phase, and Bash mutations during a planning phase. Outside a QA workflow it decides nothing.
  - `SessionStart` for resume context (fires on startup|resume|compact)
  - `PostToolUse` for workflow artifact integrity audit (`cc10x_posttooluse_artifact_guard.py`)
  - `TaskCompleted` for task metadata checks (`cc10x_task_completed_guard.py`)
  - `PostCompact` for compaction event capture in workflow event log (audit only)
  - `SubagentStop` for agent contract presence audit (hook log, telemetry only)
  - `PreCompact` for workflow state snapshot before compaction (persistence only)
  - `Stop` for workflow state snapshot on session stop (persistence only, never blocks)
  - `StopFailure` for API error logging to the hook log (async, telemetry only)
  - `InstructionsLoaded` for instruction file load audit trail in the hook log (async, telemetry only)
- Default mode is audit-only for the hooks that consult `hook-mode.json`, with one exception there: `artifactIntegrity` ships in `block` mode — the PostToolUse guard exits 2 after a write to a workflow artifact that is malformed JSON or missing required keys. PostToolUse runs after the write: exit 2 feeds stderr to the model and cannot undo the write, so the malformed artifact stays on disk until the model repairs it (the message says to repair it now). It signals only for writes to the artifact itself; writes to other files are audited, never signaled. Two blocking hooks do not consult `hook-mode.json` at all and block unconditionally whatever the mode says: the PreToolUse git guard `cc10x_git_guard.py` (next bullet) and the PreToolUse QA isolation guard `cc10x_qa_isolation_guard.py`. Do not rely on hooks as the only source of truth; the router still owns orchestration decisions.
- Hooks that read workflow state (the protected-writes guard, the QA isolation guard, SessionStart context, and the compaction and stop snapshots) resolve the artifact with the newest modification time in `.cc10x/workflows/`, not the `wf:` of the current task; the TaskCompleted guard reads the artifact named by the task's `wf:`. With two live workflows a hook can therefore evaluate the other one; the router, which scopes by `wf:`, stays the source of truth.
- Git-guard approval token: the PreToolUse git guard blocks `git push` and `git branch -D` unconditionally UNLESS a fresh single-use token exists at `.cc10x/state/git-approval.json` (`{"wf", "operations": ["push"|"branch-delete"], "expires_at"}`, ≤10 min). Only the BUILD-DONE finishing gate writes this token, and only immediately after the user's explicit menu choice (see `build-workflow.md` §BUILD-DONE finishing). The guard consumes the token on first use. `git reset --hard`, `git clean -f`, force-push, and `git checkout .` have no token path.
- Repo-local `.claude/settings.json` is not part of the shipped CC10X product.
- Optional accelerator MCPs are user-configured in Claude Code. CC10X assumes the names `brightdata` and `octocode` if they are available, but must degrade to built-in research paths when they are absent.

## Dispatch-Prompt Construction Rules

The router forbids verdict-softeners in agent OUTPUT. The same fail-closed bar applies to agent INPUT: a biased dispatch prompt is a verification defect equal to a softened verdict. The router must not pre-judge or soften the prompts it constructs for read-only agents.

Applies when the router builds a prompt for any read-only agent:

- `code-reviewer`
- `integration-verifier`
- `plan-gap-reviewer`
- `bug-investigator` (read/diagnose phase)

The dispatch prompt MUST NOT:

- Pre-judge findings or state a conclusion the agent is expected to confirm.
- Pre-rate severity or cap it (no "at most Minor", no "treat as low risk").
- Name what NOT to flag, or scope the agent away from a region the author assumes is fine.
- Tell the agent the plan or author already decided something is acceptable.
- Re-ask the implementer to re-run tests it already evidenced. Pass the evidence path instead (the `.cc10x/` artifact or `results.evidence` reference), and let the agent confirm against that proof.

The dispatch prompt MUST:

- State the surface to inspect (paths, diff package, phase scope) and the contract to return, neutrally.
- Let the agent assign its own severity and form its own verdict from primary evidence.

SELF-CHECK BLOCKLIST (single source of truth — SKILL.md §7 points here) — before dispatch, the router greps its own drafted prompt for these literal phrases (case-insensitive):

- `do not flag`
- `don't treat X as a defect`
- `don't worry about`
- `at most minor`
- `the plan chose`
- `already verified, just`
- `should be fine`
- `no need to check`

If any blocklist phrase appears in the drafted prompt, the prompt is biased. Rewrite it to remove the bias before dispatching. Fail closed: do not dispatch a prompt that pre-judges, pre-rates, or scopes away findings.

## Dispatch Context Hygiene

The router's context is the orchestration bottleneck. Pasting full briefs, plan bodies, or prior agent outputs inline bloats the router context and corrupts resume-after-compaction (a single dispatch has been observed at ~42k chars, ~99% pasted history). Dispatch by reference, not by blob.

Rules:

- Dispatch prompts pass PATHS, never pasted file bodies:
  - workflow artifact path (`.cc10x/workflows/{workflow_uuid}.json`)
  - `plan_file`
  - `design_file`
  - `research_files`
  - diff-package path
- Sub-agents write their full evidence and report to a `.cc10x/` artifact (under the workflow `state_root`), not into the returned message.
- Sub-agents RETURN only a thin CONTRACT envelope:
  - `status`
  - commits / files touched
  - one-line test summary
  - refs to concerns/findings artifacts (paths, not bodies)
- The router reads artifact paths on demand and never inlines large file content into the next dispatch prompt. The next agent receives the path and reads it itself.
- This reuses the existing artifact schema and `.cc10x/` workflow namespace: `state_root` is `.cc10x`, evidence is grouped under `evidence` and `results`, and handoff reads structured data from the workflow artifact, not from pasted conversation history.

Producers (dispatch-by-reference is now realized, not just prescribed):

- The `diff-package path` above is PRODUCED by `python3 "${CLAUDE_PLUGIN_ROOT}/tools/review_package.py" BASE [HEAD]`, which writes `.cc10x/review-<base7>..<head7>.diff` (commits + `git diff --stat` + `git diff -U10`) and prints the path. BASE must be the sha recorded before the phase started, NEVER `HEAD~1` (which silently drops all but the last commit of a multi-commit phase).
- The per-phase brief is PRODUCED by `python3 "${CLAUDE_PLUGIN_ROOT}/tools/phase_brief.py" PLAN_FILE PHASE`, which slices one approved phase out of the plan into `.cc10x/phase-<PHASE>-brief.md` and prints the path. Pass that path in the dispatch prompt instead of pasting the phase body.

## 8. Post-Agent Validation Contracts {#contracts}

This section is consulted at post-agent validation time only, not at routing time. The router kernel (`SKILL.md` §8) points here before validating any write-agent contract.

### Write-agent YAML required fields

Parsing direction, for every agent (write and read-only): the router branches on `STATUS` from the fenced YAML block that follows the `### Router Contract (MACHINE-READABLE)` heading when the heading exists, otherwise the first fenced `yaml` block after the envelope and heading. The line-1 `CONTRACT` envelope and the line-2 heading are quick presence signals read first (`SKILL.md` §8); if they disagree with the YAML block, the YAML block decides.

Expected fields:

| Agent | Required fields |
| ------- | ----------------- |
| component-builder | `STATUS`, `CONFIDENCE`, `PHASE_ID`, `PHASE_STATUS`, `PHASE_EXIT_READY`, `CHECKPOINT_TYPE`, `PROOF_STATUS`, `BUILD_PREFLIGHT_EMITTED`, `INPUTS`, `EXPECTED_ARTIFACTS`, `TDD_RED_EXIT`, `TDD_RED_REASON_KIND`, `TDD_RED_REASON`, `TDD_GREEN_EXIT`, `TEST_SEAMS`, `SEAM_GATE_STATUS`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `BLOCKED_ITEMS`, `SKIPPED_ITEMS`, `SCOPE_INCREASES`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `MEMORY_NOTES` |
| bug-investigator | `STATUS`, `VERIFICATION_RIGOR`, `CONFIDENCE`, `ROOT_CAUSE`, `TDD_RED_EXIT`, `TDD_GREEN_EXIT`, `VARIANTS_COVERED`, `VARIANTS_NOT_APPLICABLE`, `FEEDBACK_LOOP`, `NO_LOOP_BLOCKED`, `BOUNDARY_MATRIX`, `REGRESSION_SEAM`, `DEFENSE_IN_DEPTH`, `DEBUG_CLOSEOUT`, `BLAST_RADIUS_SCAN`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `NEEDS_EXTERNAL_RESEARCH`, `RESEARCH_REASON`, `MEMORY_NOTES` |
| planner | `STATUS`, `PLAN_MODE`, `VERIFICATION_RIGOR`, `CONFIDENCE`, `PLAN_FILE`, `PLAN_REVISION`, `LAST_REVIEWED_REVISION`, `PHASES`, `RISKS_IDENTIFIED`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `OPEN_DECISIONS`, `DIFFERENCES_FROM_AGREEMENT`, `RECOMMENDED_DEFAULTS`, `ALTERNATIVES`, `DRAWBACKS`, `PROVABLE_PROPERTIES`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `GATE_PASSED`, `USER_INPUT_NEEDED`, `MEMORY_NOTES`. On a `phase:qa-re-plan` return also `AMENDED_FILES`, `STALE_SWEEP`, `RECONCILIATION_RERUN` (the pass-2 gate in `qa-workflow.md` fails closed without all three). |
| researcher | `STATUS`, `FILE_PATH`, `BACKEND_MODE`, `SOURCES_ATTEMPTED`, `SOURCES_USED`, `QUALITY_LEVEL`, `KEY_FINDINGS_COUNT`, `WHAT_CHANGED_RECOMMENDATION`, `MEMORY_NOTES` |
| doc-syncer | `STATUS`, `IMPACT_LEVEL`, `DOC_LAYERS_EVALUATED`, `DOC_FILES_UPDATED`, `DOC_FILES_SKIPPED`, `SKIP_REASON`, `AUDIT_DOCS_CREATED`, `AUDIT_DOCS_UPDATED`, `MEMORY_NOTES` |
| qa-harness-builder | **`MODE` selects the set.** A contract omitting `MODE` is validated as `MODE: harness` — the pre-change behaviour, so nothing already written or in flight starts failing.<br>`MODE: harness` → `MODE`, `STATUS`, `CONFIDENCE`, `PHASE_STATUS`, `SCENARIOS_PLANNED`, `SCENARIOS_IMPLEMENTED`, `MUTATION_CHECKS`, `LIVENESS_PROBES`, `RERUN_CLEAN`, `TEARDOWN_VERIFIED`, `ENV_MODE`, `SERVICES_PROVISIONED`, `PRODUCT_CODE_TOUCHED`, `SCOPE_INCREASES`, `BLOCKED_ITEMS`, `BLOCKING`, `NEXT_ACTION`, `MEMORY_NOTES`, `ARTIFACTS_CREATED`, `HARNESS_MANIFEST`. Every other field in the block stays optional, exactly as before.<br>`MODE: preflight` → `MODE`, `STATUS`, `CONFIDENCE`, `PHASE_STATUS`, `COST_TIER_REACHED`, `CHECKS`, `HUMAN_PREREQUISITES`, `ENV_PLAN_CORRECTIONS`, `REPO_CURRENCY`, `CURRENCY_GATE`, `SETUP_RECORD`, `SETUP_RECORD_STALE`, `SERVICES_PROVISIONED`, `PRODUCT_CODE_TOUCHED`, `BUG_CANDIDATES`, `SCOPE_INCREASES`, `BLOCKED_ITEMS`, `BLOCKING`, `NEXT_ACTION`, `MEMORY_NOTES` |
| qa-executor | **This row is a deliberate TIGHTENING.** Neither table listed `qa-executor` before, so `qa-execute` has never been validated here and now will be. `STATUS`, `CONFIDENCE`, `REPORT_FILE`, `ENV_MODE`, `ENV_READY`, `SCENARIOS_TOTAL`, `SCENARIOS_PASSED`, `SCENARIOS_FAILED`, `SCENARIOS_BLOCKED`, `SCENARIOS_FLAKY`, `EVIDENCE`, `TEARDOWN_STATUS`, `TEARDOWN_EVIDENCE`, `LEAKED_RESOURCES`, `COVERAGE_GAPS`, `BUG_CANDIDATES`, `FAILURE_CLASS_COUNTS`, `HARNESS_ISSUES`, `TEST_CODE_TOUCHED`, `PRODUCT_CODE_TOUCHED`, `CRITICAL_ISSUES`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REMEDIATION_REASON`, `MEMORY_NOTES`. |

### Read-only and advisory agent required fields

These agents emit a Router Contract too; the fields below are what the router reads. Optional fields are named in the agent file.

| Agent | Required fields |
| ------- | ----------------- |
| code-reviewer | `STATUS`, `FUNCTIONALITY`, `CONFIDENCE`, `SIGNAL_SCORES`, `REMEDIATION_NEEDED`, `REMEDIATION_REASON`, `REMEDIATION_SCOPE_REQUESTED`, `REVERT_RECOMMENDED`, `SPEC_COMPLIANCE`, `PLAN_DEFECT`, `CANNOT_VERIFY_CROSS_PHASE`, `MEMORY_NOTES` |
| failure-hunter | `STATUS`, `TOTAL_HANDLERS_AUDITED`, `CRITICAL_ISSUES`, `HIGH_ISSUES`, `MEMORY_NOTES` |
| integration-verifier | `STATUS`, `PROOF_STATUS`, `SCENARIOS_TOTAL`, `SCENARIOS_PASSED`, `SCENARIOS_FAILED`, `REMEDIATION_NEEDED`, `REMEDIATION_REASON`, `REVERT_RECOMMENDED`, `MEMORY_NOTES` |
| triage-agent | `STATUS`, `CATEGORY`, `STATE`, `VERIFICATION_RESULT`, `REDUNDANCY_CHECK`, `PRIOR_REJECTION_CHECK`, `BRIEF_PATH`, `NEEDS_GRILLING`, `BLOCKING`, `MEMORY_NOTES` |
| architecture-scanner | `STATUS`, `CANDIDATES`, `REPORT_PATH`, `BLOCKING`, `MEMORY_NOTES` |

If the YAML block is missing or malformed, treat the task as invalid output, do not continue the workflow based on prose alone, and re-run inline verification and fail safe. "Inline verification" means the inline verification pass defined in `SKILL.md` section "Inline no-subagent execution": the router applies the integration-verifier's checks itself and writes the same scenario accounting into the artifact.

### Contract overrides

| Agent | Override |
| ------- | ---------- |
| component-builder | `STATUS=PASS` requires a non-zero `TDD_RED_EXIT` (1 by convention), `TDD_RED_REASON_KIND=behavioral` with **non-empty `TDD_RED_REASON`** (a false-RED — `TDD_RED_REASON_KIND=error` from import/syntax/collection failure — is rejected same as missing RED; a behavioral RED with an empty reason is also rejected), `TDD_GREEN_EXIT=0`, `BUILD_PREFLIGHT_EMITTED=true`, `PHASE_STATUS=completed`, `PHASE_EXIT_READY=true`, `PROOF_STATUS=passed`, empty `BLOCKED_ITEMS`, and a non-empty `SCENARIOS` array with at least one passing scenario. That passing scenario must include non-empty `name`, `command`, `expected`, `actual`, and `exit_code`. **Seam gate:** when `build_scope=standard` with a plan that provides `test_seams`, `SEAM_GATE_STATUS` must be `confirmed` (`TEST_SEAMS` non-empty, matching the plan's `test_seams`) or `disagreed` (with a DECISIONS rationale + a better seam in `TEST_SEAMS`, OR `STATUS=FAIL` with the ambiguity `REMEDIATION_REASON` and empty `TEST_SEAMS`); when `build_scope=standard` with a legacy plan whose phase omits `test_seams`, `SEAM_GATE_STATUS=proposed` is accepted (`TEST_SEAMS` non-empty — builder proposes at BUILD_PREFLIGHT); when direct/no-plan, `SEAM_GATE_STATUS=proposed` (`TEST_SEAMS` non-empty); when `build_scope=trivial`, `SEAM_GATE_STATUS=not_applicable` is accepted. **Documentation, prompt and config-only phases** have the same RED/GREEN requirement: the scripted check is a validator, grep or replay check with a real exit code, RED is that check failing before the edit and passing after, and it is `behavioral` when it asserts content, `error` when it only failed to run. **`kind:remfix` proof:** `STATUS=PASS` also requires non-empty `COVERING_TESTS`, `TEST_COMMAND` and `TEST_OUTPUT`, except on the **dispute-only return**: every dispatched finding is in `FINDING_DISPUTED` (equal count, the entries distinct and each mapping to one finding in the task), no code changed, so `TDD_RED_EXIT`, `TDD_RED_REASON_KIND`, `TDD_RED_REASON` and `TDD_GREEN_EXIT` are null and `COVERING_TESTS`, `TEST_COMMAND` and `TEST_OUTPUT` may be empty or null. That return is the only `PASS` accepted with `PHASE_EXIT_READY=false`: it must carry `PHASE_STATUS=partial`, `PROOF_STATUS=gaps_found`, empty `BLOCKED_ITEMS` and a scenario per dispute. The router persists `phase_status=partial` (the phase has not exited and `phase_cursor` does not advance), completes the REM-FIX task and enters the Re-Review loop, whose re-verify is the only thing that can close the gate; `partial` is the true state, and the stop it implies is a stop on advancing the phase, not on that loop. When the verifier adjudicates every dispute validly and returns `PASS`, the router sets `phase_status=completed` and runs `phase_exit_gate` on the verifier return and the phase's earlier builder evidence, never on the dispute-only report (Re-review precondition gate). A fabricated RED or GREEN on a dispute-only return is invalid output. A report with even one applied finding keeps every requirement above. |
| bug-investigator | `STATUS=FIXED` requires `VERIFICATION_RIGOR` to be explicit, a non-zero `TDD_RED_EXIT` (1 by convention), `TDD_GREEN_EXIT=0`, a non-empty `BLAST_RADIUS_SCAN`, and a non-empty `SCENARIOS` array unless it explicitly set `NEEDS_EXTERNAL_RESEARCH=true`. At least one scenario name must start with `Regression:` (non-empty `command`, `expected`, `actual`, `exit_code`). A `Variant:` scenario with `VARIANTS_COVERED>=1` is required ONLY when the bug has applicable variants; if `VARIANTS_NOT_APPLICABLE` is set with a reason and `VARIANTS_COVERED=0`, accept FIXED without a `Variant:` scenario. Do not force a fabricated variant. **Feedback loop + close-out:** `FEEDBACK_LOOP.rung` must not be `none` (with non-null `FEEDBACK_LOOP.command`), and `DEBUG_CLOSEOUT.instrumentation_removed=true` + `DEBUG_CLOSEOUT.repro_no_longer_fires=true` (the `kind:remfix` dispute-only return below is the one exception). No loop → STATUS MUST be BLOCKED with `NO_LOOP_BLOCKED` populated. For a bug in a documentation, prompt or config file the loop is a validator, grep or replay check with a real exit code (RED before the fix, GREEN after, `behavioral` when it asserts content). **`kind:remfix`:** `STATUS=FIXED` also requires non-empty `COVERING_TESTS`, `TEST_COMMAND` and `TEST_OUTPUT`, except on the **dispute-only return** (every dispatched finding in `FINDING_DISPUTED`, no code changed): `TDD_RED_EXIT` and `TDD_GREEN_EXIT` null, the proof fields empty or null, a `Regression:` scenario per dispute (its `command` is the `VERIFY_COMMAND`), `FEEDBACK_LOOP.rung=cli_snapshot` with `command` the first `VERIFY_COMMAND`, and `DEBUG_CLOSEOUT.instrumentation_removed` and `repro_no_longer_fires` both null (nothing was changed or reproduced). DEBUG runs no `phase_exit_gate`, so `FIXED` does not close anything: the verifier still adjudicates. A fabricated RED or GREEN there is invalid output. |
| code-reviewer | `APPROVE` + critical issues becomes `CHANGES_REQUESTED` |
| code-reviewer | `APPROVE` with zero findings across ALL dimensions AND fewer than 3 file:line evidence citations → trigger fallback inline verification. Rubber-stamp approvals without substantive analysis are invalid. This is a validity check on a zero-finding approval; it does not change the per-finding reporting floor. |
| failure-hunter | A `CLEAN` verdict that states zero error-handling sites inspected OR zero files scanned → trigger fallback inline verification. A clean silent-failure verdict requires stated scan scope. |
| integration-verifier | `PASS` + critical issues becomes `FAIL`; scenario totals must reconcile with the scenario table and evidence array; every counted scenario must map to a concrete evidence row; every scenario row must contain non-empty `Expected` and `Actual` values. **Disputes:** when the dispatch carried `FINDING_DISPUTED`, every 1-based position of that list must appear in exactly one of `DISPUTE_UPHELD` or `DISPUTE_REJECTED` (positions, not restated text: free text drifts when copied); an omitted, doubled, out-of-range or non-integer entry makes the whole return invalid output and every dispute in it stays unadjudicated (fail closed). A disputed finding the verifier also marks `validated: false` is upheld by validation and is listed in `DISPUTE_UPHELD`. A verifier that is absent, blocked or unavailable leaves the disputes unadjudicated and the gate closed. |
| planner | `PLAN_CREATED` or `DECISION_RFC_CREATED` requires non-empty `PLAN_FILE`, explicit `PLAN_MODE`, explicit `VERIFICATION_RIGOR`, `CONFIDENCE>=50`, `GATE_PASSED=true`, a non-empty `SCENARIOS` array, `OPEN_DECISIONS=[]`, and `DIFFERENCES_FROM_AGREEMENT` explicitly present. `PLAN_MODE=decision_rfc` also requires `ALTERNATIVES` with **length ≥2** (not just non-empty) and non-empty `DRAWBACKS`; `VERIFICATION_RIGOR=critical_path` requires non-empty `PROVABLE_PROPERTIES`. |
| doc-syncer | `STATUS=COMPLETE` requires `DOC_LAYERS_EVALUATED` non-empty and at least one entry in `DOC_FILES_UPDATED` or `AUDIT_DOCS_CREATED`; `STATUS=SKIPPED` requires non-empty `SKIP_REASON` — `DOC_LAYERS_EVALUATED` MAY be empty (fast-path classifier exits before per-layer evaluation when `IMPACT_LEVEL=none` is detected immediately); `STATUS=PARTIAL` requires at least one entry in `DOC_FILES_UPDATED` or `AUDIT_DOCS_CREATED` and at least one layer in `DOC_LAYERS_EVALUATED` — router advances to Memory Update and persists `doc_sync_partial=true` in `results.doc_syncer`; `STATUS=FAIL` blocks workflow. |
| plan-gap-reviewer | `PASS` requires `BLOCKING_FINDINGS_COUNT=0` and `REPLAN_NEEDED=false`; `FINDINGS` requires explicit finding buckets and a non-empty `REPLAN_REASON` when blocking findings exist. A return on `phase:plan-review-amendment` whose `REVIEW_MODE_APPLIED` is absent or `fresh` is **invalid output** — the wrong lane ran, and the verdict describes a read the router did not ask for. Without this the echo is decorative. |
| qa-researcher | **This row is a deliberate TIGHTENING.** Neither table listed `qa-researcher` before, so `qa-research` has never been validated here and now will be. `qa-researcher` is read-only, so it belongs here and not in the write-agent required-fields table above. `STATUS=PASS` requires `SOURCE_COVERAGE` set, and either non-empty `USER_FLOW`/`SYSTEM_FLOW` **or** a `SOURCE_COVERAGE` of `empty`/`unavailable` carrying a reason — an empty source honestly reported is a PASS. A `CLAIMS` entry with no `evidence` is **invalid output**: a claim without a locatable source is a guess, and it belongs in `GAPS` or nowhere. Reading outside the assigned `SOURCE` is `STATUS: FAIL` — the fan-out's whole value is that each lane reports one source's reading, and a lane that widened its own scope has destroyed the independence the consolidation step assumes. |
| qa-harness-builder | **This row is a deliberate TIGHTENING.** Neither table listed any QA agent before, so `qa-build` has never been validated here and now will be. `MODE: harness`: `STATUS=PASS` requires `SCENARIOS_IMPLEMENTED == SCENARIOS_PLANNED` (or every gap in `SCENARIOS_UNIMPLEMENTED` with a reason), `RERUN_CLEAN=true`, `TEARDOWN_VERIFIED=true`, **the mutation floor met on every unit the floor selects**, where every satisfying entry is a `MUTATION_CHECKS` entry with `outcome: assertion_falsified` and a non-empty `failing_assertion`. `STATUS=PASS` in harness mode also requires a **non-empty `ARTIFACTS_CREATED`** and a **non-null `HARNESS_MANIFEST`** — `HARNESS_MANIFEST: null` is legal only in `MODE: preflight`, where no harness is built. A harness build that enumerates nothing has skipped a deliverable, and a `qa-review` dispatched at that surface reads nothing. The floor's magnitude is the three branches `qa-harness-builder.md` states, and the first matching branch wins: (1) the test plan's `## 2c. Provable properties` present, non-empty and declaring 8 or fewer properties → one `assertion_falsified` **per provable property**; (2) §2c declaring more than 8 **and marking at least one row `At risk of appearing proven: yes`** → one per flagged property, the unflagged rows unfloored — **if §2c declares more than 8 properties and flags none, this branch does not match and the plan falls through to branch 3**, because a floor over an empty unit set is met by an empty `MUTATION_CHECKS`; (3) §2c absent or empty → one **per tier and per wave — both, not either**, so every tier in `TIER_COVERAGE` with a non-zero count and every wave in the build order needs one. A single falsified assertion satisfies this row only where the selected unit set has exactly one member, `BLOCKED_ITEMS=[]`. Any entry with `outcome: survived` is an automatic `FAIL` — a test that passes under sabotage is a fake test. `outcome: not_applied` is invalid output. `outcome: blocked` counts zero toward the floor and must carry `failing_assertion` and `blocked_reason`. `LIVENESS_PROBES` entries are informational and CANNOT satisfy the floor; a set of only `blocked` entries plus `LIVENESS_PROBES` is `gaps_found`, not `passed`. **A floor of zero is not a floor:** under every branch, at least one `assertion_falsified` is required regardless of which branch applies. `MUTATION_CHECKS` empty means no assertion was ever observed failing — the router treats an unproven suite as `gaps_found`, not `passed`. `MODE: preflight`: `STATUS=PASS` requires `SERVICES_PROVISIONED=[]`, `BLOCKED_ITEMS=[]`, `HUMAN_PREREQUISITES=[]`, `CURRENCY_GATE=[]` and every `CHECKS` entry `result: pass` — the scenario/mutation/teardown requirements do NOT apply, because preflight builds no suite and demanding them would make a clean preflight structurally unable to pass. Non-empty `BLOCKED_ITEMS` or `HUMAN_PREREQUISITES` forces `STATUS: BLOCKED` with `NEXT_ACTION: gate`, never `PASS` and never `FAIL`. Non-empty `SERVICES_PROVISIONED` in preflight mode is an automatic `FAIL` (the T4 ceiling was breached). **`REPO_CURRENCY` must carry one entry per repo in the topology — the repo set named by the feature map and env plan, not the subset preflight touched; a shorter list is invalid output.** **Non-empty `CURRENCY_GATE` forces `STATUS: BLOCKED` with `NEXT_ACTION: gate`, never `PASS` and never `FAIL`** — a stale checkout is an environment fact, and `CURRENCY_GATE` does not escalate `qa_scope`. **The gate's axis is `commits_behind`:** an entry is emitted for every repo with commits_behind > 0 and for no other reason. A modified working tree is a measured fact on the `REPO_CURRENCY` row and never a gate trigger — QA is usually pointed at uncommitted work, so gating on a modified tree would block the route's common case; the gate's third option (the uncommitted work is the system under test — measure as checked out and record the tree state) is usually the right answer for QA. Branch currency never produces a failed `CHECKS` row, so a fully current topology still reaches `PASS` exactly as before. A `BUG_CANDIDATES` entry with no `measured_on` is invalid output, and one whose `measured_on` carries any repo with `commits_behind > 0` may not be `severity: critical`. `PRODUCT_CODE_TOUCHED=true` is an automatic `FAIL` in both modes. **In neither mode may this agent move a repo checkout on its own initiative; a fast-forward is legal only on an answered `CURRENCY_GATE`.** |
| qa-executor | **This row is a deliberate TIGHTENING.** Neither table listed `qa-executor` before, so `qa-execute` has never been validated here and now will be. `STATUS=PASS` requires `SCENARIOS_TOTAL == SCENARIOS_PASSED`, `SCENARIOS_BLOCKED=0`, `SCENARIOS_FAILED=0`, `TEARDOWN_STATUS=clean`, `ENV_READY=true`, and `len(EVIDENCE) == SCENARIOS_TOTAL`. `TEST_CODE_TOUCHED=true` or `PRODUCT_CODE_TOUCHED=true` is an automatic `FAIL` — the executor witnesses, it does not repair. `TEARDOWN_STATUS=leaked` forces `FAIL` with a non-empty `LEAKED_RESOURCES`. A `BUG_CANDIDATES` entry missing `siblings_swept`, or one whose `findings` list is shorter than its `members` list, is **invalid output** — the sweep stopped at the first interesting answer. A failing `EVIDENCE` entry with no `failure_class` is **invalid output**; the vocabulary is `missing-input` | `wrong-guess` | `defect`, the same one preflight's `CHECKS[].classification` uses. A `BUG_CANDIDATE` with no `measured_on` is **invalid output**; a candidate whose `measured_on` includes any repo with `commits_behind > 0` **may not carry `severity: critical`** (it is capped at `unconfirmed`, a confidence floor and not an impact level); a cross-repo contract mismatch reporting only the checked-out reading, without `siblings_swept.branch_axis` giving both sides' `default_branch` reading, is **invalid output**. A `BUG_CANDIDATES` entry may only carry `failure_class: defect` — `missing-input` and `wrong-guess` failures are classified, counted in `FAILURE_CLASS_COUNTS`, and reported, never candidates (qa-workflow.md W6 states the rule at emission). `measured_on` and `branch_axis` are sub-fields of `BUG_CANDIDATES` and add no new top-level required field. |
