## 2a. Workflow Artifact And Hook Policy

CC10X durable orchestration state lives in:

```text
.cc10x/workflows/{workflow_uuid}.json
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
- `plan_mode`
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
- The workflow UUID is generated independently of Claude task ids and is the canonical workflow identifier everywhere in the orchestration system.
- `workflow_id` remains as a compatibility alias and must equal `workflow_uuid` in new artifacts.
- `state_root` must equal `.cc10x`.
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
- `plan_mode`, `verification_rigor`, and `proof_status` mirror the router-owned interface fields from workflow preparation (`direct|execution_plan|decision_rfc`, `standard|critical_path`, `passed|gaps_found|human_needed`).
- `traceability` stores requirement→phase→verification→remediation linkage arrays (`requirements`, `phases`, `verification`, `remediation`).
- `deferred_findings` accumulates non-blocking Minor findings across phases (each entry: `source`, `phase_id`, `finding`, `severity:minor`); surfaced once at BUILD-DONE triage, never consumed mid-flight. See `build-workflow.md` §Deferred Minor findings roll-up.
- `evidence` stores proof-of-work grouped by agent:
  - `builder`
  - `investigator`
  - `reviewer`
  - `hunter` (ACTIVE — the standalone failure-hunter agent's evidence)
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

Router gates:

- `plan_trust_gate`
- `phase_exit_gate`
- `failure_stop_gate`
- `memory_sync_gate`
- `skill_precedence_gate`

These are router-owned checks, not advisory hints.

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
- Default mode is audit-only, with ONE exception: `artifactIntegrity` ships in `block` mode — the PostToolUse guard rejects (exit 2) a write to a workflow artifact that is malformed JSON or missing required keys. It blocks only writes to the artifact itself; writes to other files are audited, never blocked. Do not rely on hooks as the only source of truth; the router still owns orchestration decisions.
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

SELF-CHECK BLOCKLIST — before dispatch, the router greps its own drafted prompt for these literal phrases:

- `do not flag`
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

For write agents, parse the final fenced YAML block under `### Router Contract (MACHINE-READABLE)`.

Expected fields:

| Agent | Required fields |
| ------- | ----------------- |
| component-builder | `STATUS`, `CONFIDENCE`, `PHASE_ID`, `PHASE_STATUS`, `PHASE_EXIT_READY`, `CHECKPOINT_TYPE`, `PROOF_STATUS`, `BUILD_PREFLIGHT_EMITTED`, `INPUTS`, `EXPECTED_ARTIFACTS`, `TDD_RED_EXIT`, `TDD_RED_REASON_KIND`, `TDD_GREEN_EXIT`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `BLOCKED_ITEMS`, `SKIPPED_ITEMS`, `SCOPE_INCREASES`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `MEMORY_NOTES` |
| bug-investigator | `STATUS`, `VERIFICATION_RIGOR`, `CONFIDENCE`, `ROOT_CAUSE`, `TDD_RED_EXIT`, `TDD_GREEN_EXIT`, `VARIANTS_COVERED`, `BLAST_RADIUS_SCAN`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `NEEDS_EXTERNAL_RESEARCH`, `RESEARCH_REASON`, `MEMORY_NOTES` |
| planner | `STATUS`, `PLAN_MODE`, `VERIFICATION_RIGOR`, `CONFIDENCE`, `PLAN_FILE`, `PHASES`, `RISKS_IDENTIFIED`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `OPEN_DECISIONS`, `DIFFERENCES_FROM_AGREEMENT`, `RECOMMENDED_DEFAULTS`, `ALTERNATIVES`, `DRAWBACKS`, `PROVABLE_PROPERTIES`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `GATE_PASSED`, `USER_INPUT_NEEDED`, `MEMORY_NOTES` |
| researcher | `STATUS`, `FILE_PATH`, `BACKEND_MODE`, `SOURCES_ATTEMPTED`, `SOURCES_USED`, `QUALITY_LEVEL`, `KEY_FINDINGS_COUNT`/`IMPLEMENTATIONS_FOUND`, `WHAT_CHANGED_RECOMMENDATION`, `MEMORY_NOTES` |
| doc-syncer | `STATUS`, `IMPACT_LEVEL`, `DOC_LAYERS_EVALUATED`, `DOC_FILES_UPDATED`, `DOC_FILES_SKIPPED`, `SKIP_REASON`, `AUDIT_DOCS_CREATED`, `AUDIT_DOCS_UPDATED`, `MEMORY_NOTES` |

If the YAML block is missing or malformed, treat the task as invalid output, do not continue the workflow based on prose alone, and re-run inline verification and fail safe.

### Contract overrides

| Agent | Override |
| ------- | ---------- |
| component-builder | `STATUS=PASS` requires `TDD_RED_EXIT=1`, `TDD_RED_REASON_KIND=behavioral` (a false-RED — `TDD_RED_REASON_KIND=error` from import/syntax/collection failure — is rejected same as missing RED), `TDD_GREEN_EXIT=0`, `BUILD_PREFLIGHT_EMITTED=true`, `PHASE_STATUS=completed`, `PHASE_EXIT_READY=true`, `PROOF_STATUS=passed`, empty `BLOCKED_ITEMS`, and a non-empty `SCENARIOS` array with at least one passing scenario. That passing scenario must include non-empty `name`, `command`, `expected`, `actual`, and `exit_code`. |
| bug-investigator | `STATUS=FIXED` requires `VERIFICATION_RIGOR` to be explicit, `TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0`, a non-empty `BLAST_RADIUS_SCAN`, and a non-empty `SCENARIOS` array unless it explicitly set `NEEDS_EXTERNAL_RESEARCH=true`. At least one scenario name must start with `Regression:` (non-empty `command`, `expected`, `actual`, `exit_code`). A `Variant:` scenario with `VARIANTS_COVERED>=1` is required ONLY when the bug has applicable variants; if `VARIANTS_NOT_APPLICABLE` is set with a reason and `VARIANTS_COVERED=0`, accept FIXED without a `Variant:` scenario. Do not force a fabricated variant. |
| code-reviewer | `APPROVE` + critical issues becomes `CHANGES_REQUESTED` |
| code-reviewer | `APPROVE` with zero findings across ALL dimensions AND fewer than 3 file:line evidence citations → trigger fallback inline verification. Rubber-stamp approvals without substantive analysis are invalid. |
| code-reviewer | An `APPROVE` with zero findings across ALL dimensions AND fewer than 3 file:line evidence citations → trigger fallback inline verification. Rubber-stamp approvals without substantive analysis are invalid. |
| failure-hunter | A `CLEAN` verdict that states zero error-handling sites inspected OR zero files scanned → trigger fallback inline verification. A clean silent-failure verdict requires stated scan scope. |
| integration-verifier | `PASS` + critical issues becomes `FAIL`; scenario totals must reconcile with the scenario table and evidence array; every counted scenario must map to a concrete evidence row; every scenario row must contain non-empty `Expected` and `Actual` values |
| planner | `PLAN_CREATED` or `DECISION_RFC_CREATED` requires non-empty `PLAN_FILE`, explicit `PLAN_MODE`, explicit `VERIFICATION_RIGOR`, `CONFIDENCE>=50`, `GATE_PASSED=true`, a non-empty `SCENARIOS` array, `OPEN_DECISIONS=[]`, and `DIFFERENCES_FROM_AGREEMENT` explicitly present. `PLAN_MODE=decision_rfc` also requires non-empty `ALTERNATIVES` and `DRAWBACKS`; `VERIFICATION_RIGOR=critical_path` requires non-empty `PROVABLE_PROPERTIES`. |
| doc-syncer | `STATUS=COMPLETE` requires `DOC_LAYERS_EVALUATED` non-empty and at least one entry in `DOC_FILES_UPDATED` or `AUDIT_DOCS_CREATED`; `STATUS=SKIPPED` requires non-empty `SKIP_REASON` — `DOC_LAYERS_EVALUATED` MAY be empty (fast-path classifier exits before per-layer evaluation when `IMPACT_LEVEL=none` is detected immediately); `STATUS=PARTIAL` requires at least one entry in `DOC_FILES_UPDATED` or `AUDIT_DOCS_CREATED` and at least one layer in `DOC_LAYERS_EVALUATED` — router advances to Memory Update and persists `doc_sync_partial=true` in `results.doc_syncer`; `STATUS=FAIL` blocks workflow. |
| plan-gap-reviewer | `PASS` requires `BLOCKING_FINDINGS_COUNT=0` and `REPLAN_NEEDED=false`; `FINDINGS` requires explicit finding buckets and a non-empty `REPLAN_REASON` when blocking findings exist. |
