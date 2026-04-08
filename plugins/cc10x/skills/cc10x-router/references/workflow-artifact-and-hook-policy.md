## 2a. Workflow Artifact And Hook Policy

CC10X durable orchestration state lives in:

```text
.claude/cc10x/v10/workflows/{workflow_uuid}.json
```

Artifact schema must include:
 - `workflow_uuid`
- `workflow_id`
- `workflow_type`
- `state_root`
- `user_request`
- `plan_file`
- `design_file`
- `research_files`
- `approved_decisions`
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
- `evidence`
- `telemetry`
- `quality`
- `planning_review_runs`
- `planning_review_findings`
- `planning_review_status`
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
- The workflow UUID is generated independently of Claude task ids and is the canonical workflow identifier everywhere in v10.
- `workflow_id` remains as a compatibility alias and must equal `workflow_uuid` in new artifacts.
- `state_root` must equal `.claude/cc10x/v10`.
- `phase_cursor` points at the only BUILD phase that may run next.
- `normalized_phases` stores planner-approved executable phases with:
  - `phase_id`
  - `title`
  - `objective`
  - `files`
  - `checks`
  - `exit_criteria`
- Bright Data MCP and Octocode MCP are optional accelerators. Base CC10X installs must continue to work with built-in Claude Code tools only.
- When optional user-configured Claude Code MCP servers are available, use the server names `brightdata` and `octocode` so the research agents can auto-detect them without prompt edits.
- `capabilities` records the session-level research backend availability model:
  - `brightdata_available`
  - `octocode_available`
  - `websearch_available`
  - `webfetch_available`
- `results.research` must be structured as `web`, `github`, and `synthesis`.
- `intent` stores the durable spec header for the workflow:
  - `goal`
  - `non_goals`
  - `constraints`
  - `acceptance_criteria`
  - `open_decisions`
- `approved_decisions` stores decisions explicitly approved by the user or already fixed in the saved plan.
- `evidence` stores proof-of-work grouped by agent:
  - `builder`
  - `investigator`
  - `reviewer`
  - `hunter`
  - `verifier`
- `quality` stores convergence state:
  - `confidence`
  - `evidence_complete`
  - `scenario_coverage`
  - `research_quality`
  - `convergence_state`
- PLAN-local fresh review tracking stores:
  - `planning_review_runs`
  - `planning_review_findings`
  - `planning_review_status`
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
- `pending_gate` is required whenever BUILD/PLAN/DEBUG is waiting on user clarification, scope selection, or persistence repair.
- `status_history` and `remediation_history` are append-only summaries of major router decisions.

v10 router gates:
- `plan_trust_gate`
- `phase_exit_gate`
- `failure_stop_gate`
- `memory_sync_gate`
- `skill_precedence_gate`

These are router-owned checks, not advisory hints.

Workflow event log:
- For every workflow, keep a lightweight append-only companion file:

```text
.claude/cc10x/v10/workflows/{workflow_uuid}.events.jsonl
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
- Event types:
  - `workflow_started`
  - `agent_started`
  - `agent_completed`
  - `contract_parsed`
  - `remediation_created`
  - `scope_decision_requested`
  - `scope_decision_resolved`
  - `memory_finalized`
  - `workflow_completed`
  - `workflow_failed`

Hook policy:
- CC10X plugin hooks live in the plugin bundle under `hooks/hooks.json` and should stay minimal:
  - `PreToolUse` for protected writes
  - `SessionStart` for resume context (fires on startup|resume|compact)
  - `PostToolUse` for workflow artifact integrity audit
  - `TaskCompleted` for task metadata checks
  - `PostCompact` for compaction event capture in workflow event log (audit only)
  - `SubagentStop` for agent contract presence audit (telemetry only)
  - `PreCompact` for workflow state snapshot before compaction (persistence only)
  - `Stop` for workflow state snapshot on session stop (persistence only, never blocks)
- `StopFailure` for API error logging to workflow event log (async, telemetry only)
- `InstructionsLoaded` for instruction file load audit trail (async, telemetry only)
- Default mode is audit-only. Do not rely on hooks as the only source of truth; the router still owns orchestration decisions.
- Repo-local `.claude/settings.json` is not part of the shipped CC10X product.
- Optional accelerator MCPs are user-configured in Claude Code. CC10X assumes the names `brightdata` and `octocode` if they are available, but must degrade to built-in research paths when they are absent.
