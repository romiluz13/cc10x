---
name: cc10x-router
description: |
  THE ONLY ENTRY POINT FOR CC10X. Activate this skill for build, debug, review, and plan requests.

  Use when the user asks to implement, fix, review, plan, test, refactor, or continue code work.

  Trigger keywords: build, implement, create, write, add, review, audit, debug, fix, error, bug, broken, plan, design, architect, spec, brainstorm, test, refactor, optimize, update, change, research, cc10x, c10x.

  CRITICAL: Route and execute immediately. Do not stop at describing capabilities.
---

# cc10x Router

**Runtime contract only.** v10 restores trust-first orchestration: route intent, hydrate workflow state, write workflow artifacts, execute the task graph, validate agent output, and fail closed on ambiguity, skipped work, or missing persistence.

## 1. Intent Routing

Route using the first matching signal:

| Priority | Signal | Keywords | Workflow | Chain |
|----------|--------|----------|----------|-------|
| 1 | ERROR | error, bug, fix, broken, crash, fail, debug, troubleshoot, issue | DEBUG | bug-investigator -> code-reviewer -> integration-verifier |
| 2 | PLAN | plan, design, architect, roadmap, strategy, spec, brainstorm | PLAN | brainstorming -> planner -> bounded fresh review loop |
| 3 | REVIEW | review, audit, analyze, assess, "is this good" | REVIEW | code-reviewer |
| 4 | DEFAULT | Everything else | BUILD | component-builder -> [code-reviewer || silent-failure-hunter] -> integration-verifier |

Rules:
- ERROR always wins over BUILD.
- REVIEW is advisory only. Never let REVIEW create code-changing tasks.
- BUILD always uses the full chain. The old QUICK path is retired.
- Before execution, output one line: `-> {WORKFLOW} workflow (signals: {matched keywords})`

## 2. Memory Load And Template Validation

Always run this before routing or resuming:

```text
1. Bash("mkdir -p .claude/cc10x/v10")
2. Read(".claude/cc10x/v10/activeContext.md")
3. Read(".claude/cc10x/v10/patterns.md")
4. Read(".claude/cc10x/v10/progress.md")
```

Do not parallelize step 1 with reads.

If a memory file is missing:
- Create it using the `cc10x:session-memory` template.
- Read it before continuing.

Required sections:

| File | Required Sections |
|------|-------------------|
| `activeContext.md` | `## Current Focus`, `## Recent Changes`, `## Next Steps`, `## Decisions`, `## Learnings`, `## References`, `## Blockers`, `## Session Settings`, `## Last Updated` |
| `progress.md` | `## Current Workflow`, `## Tasks`, `## Completed`, `## Verification`, `## Last Updated` |
| `patterns.md` | `## User Standards`, `## Common Gotchas`, `## Project SKILL_HINTS`, `## Last Updated` |

Auto-heal rule:
- Insert missing sections before `## Last Updated`.
- After every `Edit(...)`, immediately `Read(...)` and verify the new section exists.

JUST_GO:
- Read `activeContext.md ## Session Settings`.
- If `AUTO_PROCEED: true`, set `JUST_GO=true`.
- While `JUST_GO=true`, auto-default all non-REVERT AskUserQuestion gates to the recommended option and log the choice in `## Decisions`.

v10 trust rule:
- `JUST_GO` never overrides explicit user/project standards, open plan decisions, or failure-stop gates.
- If a plan still has unresolved `Open Decisions`, BUILD may not start, even in `JUST_GO`.

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
  - `SessionStart` for resume context
  - `PostToolUse` for workflow artifact integrity audit
  - `TaskCompleted` for task metadata checks
- Default mode is audit-only. Do not rely on hooks as the only source of truth; the router still owns orchestration decisions.
- Repo-local `.claude/settings.json` is not part of the shipped CC10X product.
- Optional accelerator MCPs are user-configured in Claude Code. CC10X assumes the names `brightdata` and `octocode` if they are available, but must degrade to built-in research paths when they are absent.

## 3. Task Metadata Contract

Every CC10X task description starts with normalized metadata lines:

```text
wf:{workflow_uuid}
kind:{workflow|agent|remfix|memory|reverify|research}
origin:{router|component-builder|bug-investigator|code-reviewer|silent-failure-hunter|integration-verifier|planner}
phase:{build|build-implement|build-review|build-hunt|build-verify|debug|debug-investigate|debug-review|debug-verify|review|review-audit|plan|plan-create|plan-review-gap|memory-finalize|re-review|re-hunt|re-verify|re-plan|research-web|research-github}
plan:{path|N/A}
scope:{ALL_ISSUES|CRITICAL_ONLY|N/A}
reason:{short reason or N/A}
```

Rules:
- `wf:` is mandatory on every child task.
- Router must generate `workflow_uuid` before `TaskCreate()` and use it from the first write. `wf:PENDING_SELF` is retired in v10.
- `kind:` is mandatory and drives resume, routing, and counting logic.
- `origin:` is mandatory on every `kind:remfix` task.
- `plan:` is required on workflow, agent, reverify, and memory tasks.
- `reason:` is required on remediation and research tasks.
- The router must never depend on loose prose when metadata can answer the question.

## 4. Resume And Hydration

After memory load:

```text
TaskList()
```

Hydration rules:
- Find active parent workflow tasks by subject prefix `CC10X BUILD:`, `CC10X DEBUG:`, `CC10X REVIEW:`, `CC10X PLAN:`.
- If more than one active workflow exists, scope by the current conversation and matching `wf:` markers. Do not resume a workflow you cannot scope confidently.
- Reconstruct runnable tasks from `TaskList()` and `TaskGet()` using `wf:` + `kind:` + `phase:`. Do not rely on stored task IDs for correctness.
- Read and write only the v10 namespace. Ignore legacy `.claude/cc10x/*.md` and `.claude/cc10x/workflows/*` state during hydration.
- `[cc10x-internal] memory_task_id` in `activeContext.md` is only a transient optimization. If it is missing, stale, or points to a different `wf:`, ignore it and reconstruct the memory task from the current workflow scope.
- Never use an unscoped fallback like "first pending Memory Update task".

Resume algorithm:
1. Identify the active parent workflow.
2. Extract `workflow_uuid` from the `wf:` line.
3. Read all CC10X tasks whose descriptions contain that `wf:`.
4. Derive runnable tasks from `status` and `blockedBy`.
5. Reconstruct the memory task as the unique pending/in_progress `kind:memory` task in the same `wf:`.

Scope-decision resume:
- Before normal routing, check `activeContext.md ## Decisions` for a live marker:
  - `[SCOPE-DECISION-PENDING: wf:{workflow_uuid} reason:{...}]`
- If present, treat the current user reply as the answer to that pending BUILD scope gate:
  - `critical only` -> create the pending REM-FIX with `scope:CRITICAL_ONLY`
  - `all issues` -> create the pending REM-FIX with `scope:ALL_ISSUES`
  - anything else -> ask again with the same two options and stop
- After consuming a valid answer:
  - remove the pending marker from `## Decisions`
  - create the scoped REM-FIX
  - block downstream re-review / re-hunt / verifier tasks as normal
  - stop after task creation so the next turn resumes from task state, not from repeated prose parsing

Safety rules:
- If a task list is shared across sessions, always scope by `wf:` before resuming.
- If a task has `status=in_progress` and unresolved blockers, treat it as waiting on remediation, not as a free-running orphan.
- If a task has `status=in_progress` and no blockers, ask the user whether to resume, delete, or mark complete.
- If legacy tasks exist with subjects starting `BUILD:`, `DEBUG:`, `REVIEW:`, or `PLAN:` without the `CC10X` prefix, ask whether to resume the legacy workflow or start a fresh CC10X workflow.

## 5. Workflow Preparation

### Shared preparation

Before creating a new workflow:
- Read `activeContext.md ## References` to discover `Plan`, `Design`, and prior `Research` files.
- Read `activeContext.md ## Decisions` for prior planner/build clarifications.
- Read `progress.md ## Current Workflow` and `## Tasks` for pending work that should resume instead of duplicating.
- Read the latest `.claude/cc10x/v10/workflows/*.json` artifact if one exists for the current conversation.

Router-owned interface fields:
- `plan_mode`: `direct` | `execution_plan` | `decision_rfc`
- `verification_rigor`: `standard` | `critical_path`
- `checkpoint_type`: `none` | `human_verify` | `decision` | `human_action`
- `proof_status`: `passed` | `gaps_found` | `human_needed`

### BUILD preparation

1. Read `- Plan:` from `activeContext.md ## References`.
2. If plan path is not `N/A`, `Read(...)` the plan file before creating tasks.
3. Run `plan_trust_gate` before BUILD:
   - `Open Decisions` must be empty or explicitly marked approved.
   - `Differences from agreement` must be present, even if empty.
   - `plan_mode` must be explicit when a plan artifact exists.
   - `verification_rigor` must be explicit when a plan artifact exists.
   - If either condition fails, ask for clarification and do not start BUILD.
4. If plan path is `N/A`, use an adaptive gate:
   - obviously trivial, low-risk work -> continue directly to BUILD
   - complex, ambiguous, multi-step, or cross-cutting work -> ask: `Plan first (Recommended)` or `Build directly`
   - `Plan first` -> switch to PLAN workflow.
   - `Build directly` -> continue without a plan.
5. If the referenced plan file is missing:
   - Ask: `Build without plan` or `Re-plan first (Recommended)`.
   - `Build without plan` -> continue with `plan:N/A`
   - `Re-plan first` -> switch to PLAN workflow
6. Normalize planner phases into executable `normalized_phases` and initialize `phase_cursor` to the first incomplete phase.
7. Persist the approved `plan_mode` and `verification_rigor` from the planner contract into the workflow artifact.
8. Every normalized phase must carry:
   - `objective`
   - `inputs`
   - `files/surfaces`
   - `expected_artifacts`
   - `required_checks`
   - `checkpoint_type`
   - `exit_criteria`
9. Initialize workflow `proof_status` to `gaps_found` until the current phase is independently verified.
10. Clarify missing requirements before builder only when the plan and memory do not already answer them.
11. Persist pre-answered clarifications in `activeContext.md ## Decisions` using `Build clarification [{topic}]: {answer}`.
12. Builder may execute only the phase at `phase_cursor`.

### DEBUG preparation

1. If the user explicitly asks for research or the bug clearly depends on external post-2024 behavior, allow a research round before the first investigator run.
2. Immediately write `[DEBUG-RESET: wf:{workflow_uuid}]` once the workflow id exists.
3. Preserve failed attempt counting semantics: the investigator counts `[DEBUG-N]:` entries after the most recent reset marker.

### REVIEW preparation

1. REVIEW is advisory only.
2. Never create REM-FIX or implementation tasks directly from a REVIEW workflow.
3. If the final review verdict is `CHANGES_REQUESTED`, the router may offer `Start BUILD to fix (Recommended)` as a follow-up user choice.

### PLAN preparation

1. Restore design enrichment:
   - Read `- Design:` from `activeContext.md ## References`.
   - If a design path exists, verify it with `Glob(...)` and pass it under `## Design File`.
2. Restore mandatory brainstorming:
   - If no valid design file exists, run `Skill(skill="cc10x:brainstorming")` in the main context before planner.
   - Brainstorming may ask the user questions and may save a `*-design.md` file. After it completes, re-read `activeContext.md ## References` and refresh the design path.
   - Brainstorming should ask only unresolved, high-impact questions and stop as soon as the intent contract is complete.
3. Optional research before planning:
   - Ask whether to run web + GitHub research for external/unfamiliar technology when it would materially improve the plan.
4. Planner receives `## Research Files` only when research files actually exist.
5. Planner is agreement-first:
   - If a requirement is materially ambiguous, planner returns `STATUS=NEEDS_CLARIFICATION`.
   - Planner never treats its own defaults as approved implementation.
6. Planner must choose one `plan_mode`:
   - `direct` for trivial low-risk work
   - `execution_plan` for standard implementation work
   - `decision_rfc` for architecture or multi-option work
7. Planner must choose one `verification_rigor`:
   - `standard` by default
   - `critical_path` for security, money, state-machine, concurrency, or irreversible-migration work
8. PLAN fresh-review loop:
   - Non-trivial plans get one fresh `plan-gap-reviewer` pass after planner success.
   - If blocking findings are returned, the router creates one `re-plan` task and then one final fresh-review pass.
   - Maximum fresh-review passes: 2.
   - Planner remains the only plan writer.
   - The existing inline `plan-review-gate` inside planner remains the final fail-closed boundary on each planner pass.

## 6. Workflow Task Graphs

### Parent workflow creation

Use this pattern for every new workflow:

1. Generate a stable workflow UUID before `TaskCreate()`:

```text
workflow_uuid = "wf-" + UTC timestamp + "-" + 8 hex chars
```

2. Create the parent workflow task with that UUID from the first write:

```text
TaskCreate({
  subject: "CC10X {WORKFLOW}: {summary}",
  description: "wf:{workflow_uuid}\nkind:workflow\norigin:router\nphase:{build|debug|review|plan}\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:User request\n\nUser request: {request}\nChain: {chain description}",
  activeForm: "{workflow active form}"
})
```

3. Immediately write the v10 artifact and event log:

```text
Write(
  file_path=".claude/cc10x/v10/workflows/{workflow_uuid}.json",
  content="{\"workflow_uuid\":\"{workflow_uuid}\",\"workflow_id\":\"{workflow_uuid}\",\"workflow_type\":\"{WORKFLOW}\",\"state_root\":\".claude/cc10x/v10\",\"user_request\":\"{request}\",\"plan_file\":null,\"design_file\":null,\"research_files\":[],\"approved_decisions\":[],\"plan_mode\":null,\"verification_rigor\":\"standard\",\"proof_status\":\"gaps_found\",\"traceability\":{\"requirements\":[],\"phases\":[],\"verification\":[],\"remediation\":[]},\"intent\":{\"goal\":null,\"non_goals\":[],\"constraints\":[],\"acceptance_criteria\":[],\"open_decisions\":[]},\"normalized_phases\":[],\"phase_cursor\":null,\"capabilities\":{\"brightdata_available\":\"unknown\",\"octocode_available\":\"unknown\",\"websearch_available\":\"unknown\",\"webfetch_available\":\"unknown\"},\"research_rounds\":[],\"research_backend_history\":[],\"research_quality\":{\"web\":\"none\",\"github\":\"none\",\"overall\":\"none\"},\"task_ids\":{},\"phase_status\":{},\"results\":{\"builder\":null,\"investigator\":null,\"reviewer\":null,\"hunter\":null,\"verifier\":null,\"planner\":null,\"planning_reviewer\":null,\"research\":{\"web\":null,\"github\":null,\"synthesis\":null}},\"evidence\":{\"builder\":[],\"investigator\":[],\"reviewer\":[],\"hunter\":[],\"verifier\":[],\"planning_reviewer\":[]},\"telemetry\":{\"task_metrics_available\":\"unknown\",\"workflow_wall_clock_seconds\":0,\"agent_wall_clock_seconds\":{\"builder\":0,\"investigator\":0,\"reviewer\":0,\"hunter\":0,\"verifier\":0,\"planner\":0},\"loop_counts\":{\"re_review\":0,\"re_hunt\":0,\"re_verify\":0},\"verifier\":{\"phase_exit_proof_runs\":0,\"extended_audit_runs\":0,\"workload_seconds\":{\"tests\":0,\"build\":0,\"scan\":0,\"reconcile\":0,\"reasoning\":0}}},\"quality\":{\"confidence\":null,\"evidence_complete\":false,\"scenario_coverage\":0,\"research_quality\":\"none\",\"convergence_state\":\"pending\"},\"planning_review_runs\":0,\"planning_review_findings\":[],\"planning_review_status\":\"not_started\",\"memory_notes\":[],\"pending_gate\":null,\"status_history\":[{\"event\":\"workflow_started\",\"ts\":\"{iso_timestamp}\",\"phase\":\"{build|debug|review|plan}\"}],\"remediation_history\":[],\"created_at\":\"{iso_timestamp}\",\"updated_at\":\"{iso_timestamp}\"}"
)
Write(
  file_path=".claude/cc10x/v10/workflows/{workflow_uuid}.events.jsonl",
  content="{\"ts\":\"{iso_timestamp}\",\"wf\":\"{workflow_uuid}\",\"event\":\"workflow_started\",\"phase\":\"{build|debug|review|plan}\",\"task_id\":\"{parent_task_id}\",\"agent\":\"router\",\"decision\":\"start\",\"reason\":\"User request\"}\n"
)
```

Only create child tasks after the v10 artifact exists.

### BUILD task graph

BUILD is sequential in v10:
- one approved executable phase at a time
- one builder run for the current phase only
- review, hunt, and verify validate that phase before `phase_cursor` advances
- if phase exit evidence is incomplete, record `partial` or `blocked`, persist state, and stop

```text
TaskCreate({
  subject: "CC10X component-builder: Execute phase {phase_id}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-implement\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Execute approved phase\n\nExecute ONLY the phase at phase_cursor. Recover objective, inputs, expected artifacts, required checks, checkpoint type, and exit criteria from the approved phase. Stop if blocked, partial, or proof remains incomplete.",
  activeForm: "Building components"
}) -> builder_task_id

TaskCreate({
  subject: "CC10X code-reviewer: Review implementation",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-review\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Review current phase quality\n\nReview only the files and scope of the current phase.",
  activeForm: "Reviewing code"
}) -> reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({
  subject: "CC10X silent-failure-hunter: Hunt edge cases",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-hunt\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Audit current phase blast radius\n\nFind silent failures and edge cases adjacent to the current phase.",
  activeForm: "Hunting failures"
}) -> hunter_task_id
TaskUpdate({ taskId: hunter_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({
  subject: "CC10X integration-verifier: Verify integration",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-verify\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Phase exit verification\n\nRun required checks for the current phase and report whether truths, artifacts, wiring, and phase exit criteria are all satisfied.",
  activeForm: "Verifying integration"
}) -> verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id, hunter_task_id] })

TaskCreate({
  subject: "CC10X Memory Update: Persist workflow learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .claude/cc10x/v10/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Task() for this task.",
  activeForm: "Persisting workflow learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [verifier_task_id] })
```

### DEBUG task graph

```text
TaskCreate({
  subject: "CC10X bug-investigator: Investigate {error}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-investigate\nplan:N/A\nscope:N/A\nreason:Find root cause\n\nFind the root cause and apply the fix.",
  activeForm: "Investigating bug"
}) -> investigator_task_id

TaskCreate({
  subject: "CC10X code-reviewer: Review fix",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-review\nplan:N/A\nscope:N/A\nreason:Review the fix\n\nReview the debug fix quality.",
  activeForm: "Reviewing fix"
}) -> reviewer_task_id
TaskUpdate({ taskId: reviewer_task_id, addBlockedBy: [investigator_task_id] })

TaskCreate({
  subject: "CC10X integration-verifier: Verify fix",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-verify\nplan:N/A\nscope:N/A\nreason:Verify the fix\n\nVerify the fix works end-to-end.",
  activeForm: "Verifying fix"
}) -> verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [reviewer_task_id] })

TaskCreate({
  subject: "CC10X Memory Update: Persist debug learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .claude/cc10x/v10/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Task() for this task.",
  activeForm: "Persisting debug learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [verifier_task_id] })
```

### REVIEW task graph

```text
TaskCreate({
  subject: "CC10X code-reviewer: Review {target}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:review-audit\nplan:N/A\nscope:N/A\nreason:Advisory review\n\nRun a scoped code review.",
  activeForm: "Reviewing code"
}) -> reviewer_task_id

TaskCreate({
  subject: "CC10X Memory Update: Persist review learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .claude/cc10x/v10/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Task() for this task.",
  activeForm: "Persisting review learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [reviewer_task_id] })
```

### PLAN task graph

```text
TaskCreate({
  subject: "CC10X planner: Create plan for {feature}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:plan-create\nplan:N/A\nscope:N/A\nreason:Create implementation plan\n\nChoose the correct plan mode (`direct`, `execution_plan`, or `decision_rfc`) and verification rigor (`standard` or `critical_path`). Create the corresponding planning artifact.",
  activeForm: "Creating plan"
}) -> planner_task_id

TaskCreate({
  subject: "CC10X Memory Update: Index plan in memory",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .claude/cc10x/v10/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Task() for this task.",
  activeForm: "Indexing plan in memory"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [planner_task_id] })
```

### Research tasks

Create research tasks only when a workflow explicitly triggers them:

Before creating them:
- Determine the preferred research path for this session and store it in the workflow artifact `capabilities`.
- Preferred web path:
  - `brightdata+websearch` when Bright Data MCP is available
  - otherwise `websearch+webfetch`
- Preferred GitHub path:
  - `octocode` when Octocode MCP is available
  - otherwise `web-only`
- Allowed fallbacks always include the built-in Claude Code web tools so research remains plug-and-play.
- Increment and record the workflow-scoped round number for the `(wf, reason)` pair.

```text
TaskCreate({
  subject: "CC10X web-researcher: Research {topic}",
  description: "wf:{workflow_uuid}\nkind:research\norigin:router\nphase:research-web\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:{research_reason}\n\nTopic: {topic}\nReason: {research_reason}\nFile: docs/research/{date}-{slug}-web.md\nPreferred Backend: {brightdata+websearch or websearch+webfetch}\nAllowed Fallbacks: websearch -> webfetch\nRound: {round_number}",
  activeForm: "Researching web"
}) -> web_task_id

TaskCreate({
  subject: "CC10X github-researcher: Research {topic}",
  description: "wf:{workflow_uuid}\nkind:research\norigin:router\nphase:research-github\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:{research_reason}\n\nTopic: {topic}\nReason: {research_reason}\nFile: docs/research/{date}-{slug}-github.md\nPreferred Backend: {octocode or web-only}\nAllowed Fallbacks: package-docs -> websearch -> webfetch\nRound: {round_number}",
  activeForm: "Researching GitHub"
}) -> github_task_id
```

Research tasks are siblings, never blockers on the workflow parent. The follow-up agent task is blocked on both research tasks.

### Marker rules

- BUILD writes `[BUILD-START: wf:{workflow_uuid}]`
- DEBUG writes `[DEBUG-RESET: wf:{workflow_uuid}]`
- PLAN writes `[PLAN-START: wf:{workflow_uuid}]`

## 7. Dispatcher And Agent Prompt Contract

### Explicit dispatcher

| Task Phase / Kind | Agent |
|-------------------|-------|
| `build-implement` | `cc10x:component-builder` |
| `debug-investigate` | `cc10x:bug-investigator` |
| `build-review`, `debug-review`, `review-audit`, `re-review` | `cc10x:code-reviewer` |
| `build-hunt`, `re-hunt` | `cc10x:silent-failure-hunter` |
| `build-verify`, `debug-verify`, `re-verify` | `cc10x:integration-verifier` |
| `plan-create`, `re-plan` | `cc10x:planner` |
| `plan-review-gap` | `cc10x:plan-gap-reviewer` |
| `research-web` | `cc10x:web-researcher` |
| `research-github` | `cc10x:github-researcher` |
| `kind:remfix` + `origin:bug-investigator` | `cc10x:bug-investigator` |
| `kind:remfix` + `origin:code-reviewer|silent-failure-hunter|integration-verifier|router` | `cc10x:component-builder` |

### Prompt scaffold for every agent

```text
## Task Context
- Task ID: {task_id}
- Parent Workflow ID: {workflow_uuid}
- Task Phase: {phase}
- Plan File: {plan_file or 'None'}
- Workflow Scope: wf:{workflow_uuid}
- Workflow Artifact: .claude/cc10x/v10/workflows/{workflow_uuid}.json

## User Request
{request}

## Requirements
{clarified requirements or 'See plan/design files'}

## Memory Summary
{brief activeContext summary}

## Project Patterns
{User Standards + Common Gotchas, trimmed if needed}

## SKILL_HINTS
{router-detected skill list or "None"}
```

Optional sections:
- `## Pre-Answered Requirements` for BUILD when router already gathered decisions.
- `## Intent Contract` when a plan or design already defined goal, constraints, acceptance criteria, and named scenarios.
- `## Research Files` only when at least one research file exists.
- `## Research Quality` only when at least one research result exists.
- `## Design File` only for planner.
- `## Planning Review Findings` only for `re-plan`.
- `## Repo Context Pack` only for `plan-gap-reviewer`.
- `## Previous Agent Findings` only for integration-verifier and only after review/hunt phases.

### Deterministic skill hints

- Router is the only authority allowed to load internal CC10X skills.
- Agents may not self-activate `frontend-patterns`, `architecture-patterns`, or `debugging-patterns`.
- Include `cc10x:frontend-patterns` only when the request, changed files, plan, or design clearly targets UI/frontend work.
- Include `cc10x:architecture-patterns` only for multi-component, API, schema, auth, or integration-heavy work.
- Include `cc10x:research` only when planner or investigator receives `## Research Files`.
- Include project/domain skills only from `patterns.md ## Project SKILL_HINTS`.
- Skill precedence is strict:
  1. explicit user prompt
  2. project `CLAUDE.md` / repo standards / user standards
  3. approved plan and design docs
  4. domain-specific external skills
  5. internal CC10X skills
  6. model heuristics

### Previous Agent Findings handoff

When invoking `integration-verifier`, pass:

```text
## Previous Agent Findings

### Code Reviewer
**Verdict:** {Approve|Changes Requested}
**Critical Issues:**
{reviewer critical issues or "None"}

### Silent Failure Hunter
**Critical Issues:**
{hunter critical issues or "None / not in this workflow"}
```

DEBUG skips hunter findings.

### Task metrics and timing telemetry

- Timing telemetry is measurement only. It must never bypass gates, phase exit, or remediation rules.
- After `TaskGet()` / `TaskList()`, if Claude Code exposes task duration metrics, persist them into:
  - `telemetry.workflow_wall_clock_seconds`
  - `telemetry.agent_wall_clock_seconds.{agent}`
- If task metrics are unavailable, keep `task_metrics_available="unknown"` and continue. Missing telemetry is never a reason to advance or block a workflow.
- When `integration-verifier` reports a `### Timing & Workload` section, persist:
  - `telemetry.verifier.phase_exit_proof_runs`
  - `telemetry.verifier.extended_audit_runs`
  - `telemetry.verifier.workload_seconds`
- Use telemetry to explain latency. Do not use it to auto-reduce verification scope.

## 8. Post-Agent Validation

### Read-only contracts

Primary signal:
- Line 1: `CONTRACT {"s":"...","b":...,"cr":...}`

Fallback heading on line 2:
- `## Review: Approve|Changes Requested`
- `## Error Handling Audit: CLEAN|ISSUES_FOUND`
- `## Verification: PASS|FAIL`
- `## Planning Review: Pass|Findings`

Verdict extraction:
1. Try the envelope on line 1.
2. If envelope is missing or malformed, scan the first 5 lines for the heading.
3. Extract `CRITICAL_ISSUES` from `### Critical Issues`.
4. If output is too short or malformed, run inline verification rather than blindly approving.
5. Detect `SELF_REMEDIATED` from task state:
   - If the task remains `in_progress` and `blockedBy` is non-empty after the agent stops, treat it as self-remediated.
6. For integration-verifier, parse scenario accounting:
   - `SCENARIOS_TOTAL`
   - `SCENARIOS_PASSED`
   - `SCENARIOS_FAILED`
   - Fail validation if those counts do not reconcile with the evidence array.
   - Fail validation if any scenario omits explicit `Expected` or `Actual` evidence.

Read-only structured intent fields:
- `REMEDIATION_NEEDED: true|false`
- `REMEDIATION_REASON: ...`
- `REMEDIATION_SCOPE_REQUESTED: N/A|CRITICAL_ONLY|ALL_ISSUES`
- `REVERT_RECOMMENDED: true|false`
- `PLANNING_REVIEW_STATUS: PASS|FINDINGS`
- `BLOCKING_FINDINGS_COUNT: [number]`
- `REPLAN_NEEDED: true|false`
- `REPLAN_REASON: ...`

Compatibility rule:
- Accept legacy self-healed blocked task behavior during migration.
- Prefer the new structured remediation fields over task-state inference when both exist.

### Write-agent YAML contracts

For write agents, parse the final fenced YAML block under `### Router Contract (MACHINE-READABLE)`.

Expected fields:

| Agent | Required fields |
|-------|-----------------|
| component-builder | `STATUS`, `CONFIDENCE`, `PHASE_ID`, `PHASE_STATUS`, `PHASE_EXIT_READY`, `CHECKPOINT_TYPE`, `PROOF_STATUS`, `INPUTS`, `EXPECTED_ARTIFACTS`, `TDD_RED_EXIT`, `TDD_GREEN_EXIT`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `BLOCKED_ITEMS`, `SKIPPED_ITEMS`, `SCOPE_INCREASES`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `MEMORY_NOTES` |
| bug-investigator | `STATUS`, `VERIFICATION_RIGOR`, `CONFIDENCE`, `ROOT_CAUSE`, `TDD_RED_EXIT`, `TDD_GREEN_EXIT`, `VARIANTS_COVERED`, `BLAST_RADIUS_SCAN`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `NEEDS_EXTERNAL_RESEARCH`, `RESEARCH_REASON`, `MEMORY_NOTES` |
| planner | `STATUS`, `PLAN_MODE`, `VERIFICATION_RIGOR`, `CONFIDENCE`, `PLAN_FILE`, `PHASES`, `RISKS_IDENTIFIED`, `SCENARIOS`, `ASSUMPTIONS`, `DECISIONS`, `OPEN_DECISIONS`, `DIFFERENCES_FROM_AGREEMENT`, `RECOMMENDED_DEFAULTS`, `ALTERNATIVES`, `DRAWBACKS`, `PROVABLE_PROPERTIES`, `BLOCKING`, `NEXT_ACTION`, `REMEDIATION_NEEDED`, `REQUIRES_REMEDIATION`, `REMEDIATION_REASON`, `GATE_PASSED`, `USER_INPUT_NEEDED`, `MEMORY_NOTES` |
| web-researcher | `STATUS`, `FILE_PATH`, `BACKEND_MODE`, `SOURCES_ATTEMPTED`, `SOURCES_USED`, `QUALITY_LEVEL`, `KEY_FINDINGS_COUNT`, `WHAT_CHANGED_RECOMMENDATION`, `MEMORY_NOTES` |
| github-researcher | `STATUS`, `FILE_PATH`, `BACKEND_MODE`, `SOURCES_ATTEMPTED`, `SOURCES_USED`, `QUALITY_LEVEL`, `IMPLEMENTATIONS_FOUND`, `WHAT_CHANGED_RECOMMENDATION`, `MEMORY_NOTES` |

If the YAML block is missing or malformed:
- Treat the task as invalid output.
- Do not continue the workflow based on prose alone.
- Re-run inline verification and fail safe.

### Contract overrides

| Agent | Override |
|-------|----------|
| component-builder | `STATUS=PASS` requires `TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0`, `PHASE_STATUS=completed`, `PHASE_EXIT_READY=true`, `PROOF_STATUS=passed`, empty `BLOCKED_ITEMS`, and a non-empty `SCENARIOS` array with at least one passing scenario. That passing scenario must include non-empty `name`, `command`, `expected`, `actual`, and `exit_code`. |
| bug-investigator | `STATUS=FIXED` requires `VERIFICATION_RIGOR` to be explicit, `TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0`, `VARIANTS_COVERED>=1`, a non-empty `BLAST_RADIUS_SCAN`, and a non-empty `SCENARIOS` array unless it explicitly set `NEEDS_EXTERNAL_RESEARCH=true`. At least one scenario name must start with `Regression:` and one with `Variant:`. Both required scenarios must include non-empty `command`, `expected`, `actual`, and `exit_code`. |
| code-reviewer | `APPROVE` + critical issues becomes `CHANGES_REQUESTED` |
| silent-failure-hunter | `CLEAN` + critical issues becomes `ISSUES_FOUND` |
| integration-verifier | `PASS` + critical issues becomes `FAIL`; scenario totals must reconcile with the scenario table and evidence array; every counted scenario must map to a concrete evidence row; every scenario row must contain non-empty `Expected` and `Actual` values |
| planner | `PLAN_CREATED` or `DECISION_RFC_CREATED` requires non-empty `PLAN_FILE`, explicit `PLAN_MODE`, explicit `VERIFICATION_RIGOR`, `CONFIDENCE>=50`, `GATE_PASSED=true`, a non-empty `SCENARIOS` array, `OPEN_DECISIONS=[]`, and `DIFFERENCES_FROM_AGREEMENT` explicitly present. `PLAN_MODE=decision_rfc` also requires non-empty `ALTERNATIVES` and `DRAWBACKS`; `VERIFICATION_RIGOR=critical_path` requires non-empty `PROVABLE_PROPERTIES`. |
| plan-gap-reviewer | `PASS` requires `BLOCKING_FINDINGS_COUNT=0` and `REPLAN_NEEDED=false`; `FINDINGS` requires explicit finding buckets and a non-empty `REPLAN_REASON` when blocking findings exist. |

Convergence rule:
- If evidence is incomplete, contradictory, or missing for a required pass path, do not advance the workflow.
- Set the workflow artifact `quality.convergence_state` to `needs_iteration` and stop on the appropriate remediation or clarification gate instead of treating the task as good enough.

## 9. Remediation And Workflow Rules

### Standard REM-FIX task shape

Every remediation task description must include:

```text
wf:{workflow_task_id}
kind:remfix
origin:{originating agent}
phase:{phase}
plan:{plan_file or 'N/A'}
scope:{ALL_ISSUES|CRITICAL_ONLY|N/A}
reason:{short remediation reason}
```

### Circuit breaker

Before creating a new remediation task:
- Count tasks whose descriptions contain both `wf:{workflow_task_id}` and `kind:remfix`.
- If count >= 3, ask the user how to proceed before creating another one.

### Rule matrix

| Rule | Condition | Action |
|------|-----------|--------|
| 0b | Legacy `STATUS=SELF_REMEDIATED` or blocked task state | Do not create a duplicate REM-FIX. Leave task blocked. |
| 0c | bug-investigator sets `NEEDS_EXTERNAL_RESEARCH=true` | Spawn research tasks and re-invoke investigator. No REM-FIX yet. |
| 1a-SCOPE | BUILD parallel phase has CRITICAL + HIGH issues | Ask for `critical only` vs `all issues`, store pending scope marker, stop. |
| 1a | Blocking issue in BUILD/DEBUG | Router creates scoped REM-FIX task, blocks downstream tasks, stop. |
| 1b | Non-blocking remediation needed | In BUILD/DEBUG, auto-create REM-FIX. In REVIEW, ask whether to start BUILD. |
| 2 | Reviewer approved but hunter found issues | Ask whether to remediate or proceed. |
| 2b | Planner needs clarification | Ask the user, persist answers, create `re-plan`, re-invoke planner. |
| 2c | Investigator still investigating | Create follow-up investigation task with loop cap. |
| 2d | Verifier failed | Router creates REM-FIX unless user chooses REVERT at the router gate. |
| 2f | Investigator blocked | Ask: research, manual fix, or abort. |

### Scope resolution

The router is authoritative for BUILD remediation scope.

- BUILD reviewer/verifier should request `REMEDIATION_SCOPE_REQUESTED: N/A`; the router resolves `CRITICAL_ONLY` vs `ALL_ISSUES`.
- Legacy agent-created remediation tasks are still accepted during migration, but router-created remediation is canonical.
- `1a-SCOPE` applies only in BUILD when the parallel review phase shows both:
  - at least one CRITICAL issue
  - at least one HIGH issue from the hunter/reviewer narrative
- The trigger source is explicit:
  - hunter summary line `High issues: [count]`
  - or a `### Findings` bullet clearly labeled `HIGH`
- When `1a-SCOPE` fires:
  1. write `[SCOPE-DECISION-PENDING: wf:{workflow_task_id} reason:{top remediation reason}]` into `activeContext.md ## Decisions`
  2. ask exactly: `Fix critical only (Recommended)` or `Fix all issues`
  3. do not create a REM-FIX until the next user reply resolves the scope
- If no reliable HIGH count/signal can be extracted, default to normal rule `1a` without pretending scope selection happened.

### REVIEW-to-BUILD

If a REVIEW workflow ends with `CHANGES_REQUESTED`:
- Ask: `Start BUILD to fix (Recommended)` or `Done for now`
- `Start BUILD` -> create a fresh BUILD workflow using reviewer findings as input context
- `Done for now` -> persist the decision and stop

### Planner clarification

When planner returns `STATUS=NEEDS_CLARIFICATION`:
- Prefer `USER_INPUT_NEEDED` from the YAML contract.
- Fallback to bullets under `**Your Input Needed:**`.
- Persist answers in `activeContext.md ## Decisions`.
- Create a `re-plan` task:

```text
TaskCreate({
  subject: "CC10X planner: Re-plan after clarification",
  description: "wf:{workflow_task_id}\nkind:agent\norigin:router\nphase:re-plan\nplan:N/A\nscope:N/A\nreason:Planner clarification answered\n\nRevise the plan using the persisted user answers.",
  activeForm: "Revising plan"
}) -> replan_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [replan_task_id] })
```

When planner returns `STATUS=PLAN_CREATED` or `STATUS=DECISION_RFC_CREATED`:
- Verify `PLAN_FILE` exists with `Glob(...)`.
- Extract the intent/spec header from the saved plan and persist it into workflow artifact `intent`.
- Update the parent workflow task `plan:` line to the saved plan path.
- Update the pending memory task `plan:` line to the same saved plan path so resume and finalization stay scoped to the real artifact.
- Persist planner fresh-review fields when present:
  - `planning_review_runs`
  - `planning_review_status`
- If `PLAN_MODE=direct`, allow PLAN to continue to memory finalization without a fresh-review subagent.
- Otherwise create a fresh review task unless `planning_review_runs >= 2`:

```text
TaskCreate({
  subject: "CC10X plan-gap-reviewer: Fresh review of saved plan",
  description: "wf:{workflow_task_id}\nkind:agent\norigin:router\nphase:plan-review-gap\nplan:{plan_file}\nscope:N/A\nreason:Fresh anti-anchoring review of saved plan\n\nReview the saved plan with fresh context only. Do not rewrite it. Return repo mismatches, missing surfaces, execution-order issues, hidden assumptions, under-scoped integrations, and open decisions presented as settled.\n\n## Original User Request\n{request}\n\n## Approved Context Files\n- Design file: {design_file or 'None'}\n- Research files: {research file list or 'None'}",
  activeForm: "Fresh-reviewing plan"
}) -> planning_review_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [planning_review_task_id] })
```

- Immediately persist:
  - `planning_review_status=pending_review`
- `planning_review_runs` counts only completed fresh-review passes with valid contract output. Invalid or malformed reviewer output must fail closed without consuming one of the two allowed passes.

When `plan-gap-reviewer` returns `PASS`:
- Increment `planning_review_runs += 1`
- Set `planning_review_status=passed`
- Persist findings summary into `results.planning_reviewer`
- Continue to memory finalization

When `plan-gap-reviewer` returns `FINDINGS`:
- Increment `planning_review_runs += 1`
- Persist findings into:
  - `planning_review_findings`
  - `planning_review_status=findings_received`
  - `results.planning_reviewer`
- If `planning_review_runs < 2`, create a `re-plan` task:

```text
TaskCreate({
  subject: "CC10X planner: Revise plan after fresh review",
  description: "wf:{workflow_task_id}\nkind:agent\norigin:router\nphase:re-plan\nplan:{plan_file}\nscope:N/A\nreason:{REPLAN_REASON}\n\nRevise the existing saved plan using the fresh planning review findings.\n\n## Planning Review Findings\n{structured findings summary}",
  activeForm: "Revising plan"
}) -> replan_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [replan_task_id] })
```

- If `planning_review_runs >= 2`, stop with clarification:
  - set `pending_gate=clarification`
  - ask the user for a decision on the unresolved plan contradiction
  - do not create more fresh-review or re-plan tasks

### Investigator continuation

When bug-investigator returns `STATUS=INVESTIGATING`:
- Count prior investigation continuation tasks in the same `wf:`. If count >= 2, ask the user before creating another.
- Otherwise create a follow-up investigation task:

```text
TaskCreate({
  subject: "CC10X bug-investigator: Continue investigation",
  description: "wf:{workflow_task_id}\nkind:agent\norigin:router\nphase:debug-investigate\nplan:N/A\nscope:N/A\nreason:{ROOT_CAUSE or 'Continue investigation'}\n\nContinue investigating using the prior root-cause hints and evidence.",
  activeForm: "Continuing investigation"
})
```

### Verifier REVERT gate

If integration-verifier emits `FAIL` and the findings contain `REVERT`:
- Ask the user whether to revert or create a fix task.
- `Revert` -> record the decision in memory and stop.
- `Create fix task instead` -> continue with normal remediation creation.

## 10. Research Orchestration

Research runs only when triggered by:
- Explicit user request for research.
- External integration or unfamiliar post-2024 technology.
- Debug workflow stuck state.
- Multiple remediation cycles on the same issue.
- PLAN workflow where external patterns materially improve the plan.

Loop caps:
- Count research rounds by `wf:` + `reason:` using `kind:research` tasks.
- If the same workflow already created 2 research rounds for the same reason, ask the user before creating more.

Capability model:
1. Research backends are optional accelerators, never hard dependencies.
2. Before the first research round in a workflow, record capability assumptions in the workflow artifact:
   - `brightdata_available=true` only if the session can use Bright Data MCP
   - `octocode_available=true` only if the session can use Octocode MCP
   - `websearch_available` and `webfetch_available` reflect built-in tool availability
3. If capability is unknown, prefer the accelerated backend first and fall back immediately when it fails. Persist the observed result in the artifact so later rounds do not guess again.

Research persistence:
1. Wait for both research tasks in the round to finish.
2. Parse each agent YAML contract for:
   - `FILE_PATH`
   - `BACKEND_MODE`
   - `SOURCES_ATTEMPTED`
   - `SOURCES_USED`
   - `QUALITY_LEVEL`
3. Persist discovered paths and backend metadata into the workflow artifact immediately:
   - `results.research.web`
   - `results.research.github`
   - `research_backend_history`
   - `research_quality`
   - `research_rounds`
   - `results.research.synthesis`
4. Index research file paths in `activeContext.md ## References` during memory finalization, not before.
5. Partial success is valid:
   - If one file exists and the other is unavailable, proceed with the successful file.
6. Build `## Research Quality` using artifact-backed status:

```text
## Research Quality
Web: {COMPLETE|PARTIAL|DEGRADED|UNAVAILABLE} ({quality_level})
GitHub: {COMPLETE|PARTIAL|DEGRADED|UNAVAILABLE} ({quality_level})
Overall: {high|medium|low|none}
```

7. Re-invoke planner or investigator with:

```text
## Research Files
Web: {web_file or 'Unavailable'}
GitHub: {github_file or 'Unavailable'}
```

8. Include `cc10x:research` in `## SKILL_HINTS` only when at least one research file exists.

## 11. Re-Review Loop

When a `kind:remfix` task completes:

1. Count completed remediation tasks in the same `wf:`. If count >= 2, run the cycle-cap gate before continuing.
2. Create a re-review task:

```text
TaskCreate({
  subject: "CC10X code-reviewer: Re-review after REM-FIX",
  description: "wf:{workflow_task_id}\nkind:agent\norigin:router\nphase:re-review\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-review the changes made by the completed remediation task.",
  activeForm: "Re-reviewing fix"
}) -> rereview_task_id
```

3. In BUILD, create a re-hunt task:

```text
TaskCreate({
  subject: "CC10X silent-failure-hunter: Re-hunt after REM-FIX",
  description: "wf:{workflow_task_id}\nkind:agent\norigin:router\nphase:re-hunt\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nIf scope=ALL_ISSUES: perform a FULL re-audit of CRITICAL and HIGH issue categories after remediation.\nIf scope=CRITICAL_ONLY: verify the CRITICAL issue was resolved and treat HIGH issues as deferred unless newly escalated.\n\nRe-scan for silent failures after remediation.",
  activeForm: "Re-hunting failures"
}) -> rehunt_task_id
```

4. Reuse the pending verifier in the same `wf:` if one exists; otherwise create:

```text
TaskCreate({
  subject: "CC10X integration-verifier: Re-verify after REM-FIX",
  description: "wf:{workflow_task_id}\nkind:reverify\norigin:router\nphase:re-verify\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-verify after remediation.",
  activeForm: "Re-verifying fix"
}) -> reverify_task_id
```

5. Block verifier on re-review and re-hunt as applicable.
6. Re-block the memory task on the verifier for BUILD/DEBUG or on the re-reviewer for REVIEW.
7. Increment telemetry loop counters whenever the follow-up tasks are created:
   - `telemetry.loop_counts.re_review += 1`
   - `telemetry.loop_counts.re_hunt += 1` in BUILD
   - `telemetry.loop_counts.re_verify += 1`

## 12. Chain Execution Loop

```text
1. TaskList()
2. Select tasks in the active `wf:` where:
   - status is pending or in_progress
   - blockedBy is empty or all blockers are completed
3. If the runnable task kind is memory:
   - execute inline in the main context
   - persist workflow artifact results + Memory Notes from the task description
   - append `memory_finalized` to `.claude/cc10x/v10/workflows/{wf}.events.jsonl`
   - clean up the matching [cc10x-internal] memory_task_id entry
   - mark the memory task completed
   - mark the parent workflow task completed
   - continue
4. Otherwise, map each runnable task through the dispatcher table.
5. If `code-reviewer` and `silent-failure-hunter` are both ready in BUILD:
   - mark both in_progress first
   - invoke them in the same message
6. After each agent returns:
   - validate output
   - capture memory payload
   - persist task-state side effects
   - apply workflow rules
   - for BUILD, run `phase_exit_gate`; if the current phase is not complete, persist `phase_status={partial|blocked}` and stop
   - never advance to the next phase or workflow step on apology prose alone
7. Repeat until all tasks in the active `wf:` are completed.
```

### After every agent completion

1. `TaskGet({ taskId })` or `TaskList()` to verify final task state.
2. WRITE agents:
   - They should already have called `TaskUpdate(status="completed")`.
   - Parse YAML before continuing.
3. READ-ONLY agents:
   - During compatibility phase, if task is still `in_progress` with blockers, treat it as legacy self-remediation.
   - Otherwise router applies fallback `TaskUpdate(status="completed")`.
4. Capture memory:
   - READ-ONLY agents: extract `### Memory Notes (For Workflow-Final Persistence)` and append to the memory task description.
   - WRITE agents: do not expect `### Memory Notes`; use `MEMORY_NOTES` from YAML. Append only deferred or supplemental memory payload needed by the memory task.
5. Update `.claude/cc10x/v10/workflows/{workflow_uuid}.json` with:
   - intent contract fields from planner output when available
   - task ids
   - phase status
   - phase cursor changes only after `phase_exit_gate` passes
   - structured agent results
   - scenario evidence grouped by agent
   - plan/design/research file paths
   - capabilities and chosen research backend path when applicable
   - research quality and round metadata when applicable
   - telemetry:
     - task metrics duration when available
     - loop counters
     - verifier workload classification when present
   - quality/convergence state
   - status_history and remediation_history entries when decisions change workflow state
   - pending gate if waiting on user input
6. Persist `[cc10x-internal] memory_task_id: {memory_task_id} wf:{workflow_uuid}` only if it matches the active workflow.

### Verifier findings handoff

Before invoking `integration-verifier` in BUILD:
- Read `results.reviewer` and `results.hunter` from the workflow artifact.
- Build `## Previous Agent Findings` exactly in the format verifier expects.
- Never invoke verifier without that section when review/hunt already ran.

## 13. Memory Finalization

The memory task executes inline only. Never spawn it as a sub-agent.

The memory task:
- Reads the workflow artifact plus its own description payload, not conversation history.
- Persists learnings to:
  - `activeContext.md ## Learnings`
  - `patterns.md ## Common Gotchas`
  - `progress.md ## Verification`
- Writes deferred items as `[Deferred]: ...` under `patterns.md ## Common Gotchas`.
- Replaces `progress.md ## Tasks` with the active workflow snapshot.
- Keeps only the most recent 10 items in `progress.md ## Completed`.
- Removes the matching `[cc10x-internal] memory_task_id` line from `activeContext.md ## References`.
- If any artifact or memory write fails, stop immediately. Never advance the workflow after a failed persistence write.

For PLAN:
- Ensure `- Plan: {plan_file}` remains correct in `activeContext.md ## References`.

For DEBUG:
- Preserve the latest `[DEBUG-RESET: wf:{workflow_task_id}]` section in `## Recent Changes` and summarize the final result beneath it.

## 14. Hard Rules

- Router must run in the main Claude Code session, never inside a sub-agent.
- Router is the only orchestration state owner. Agents may propose remediation or next actions, but only the router creates, blocks, unblocks, reuses, or completes orchestration tasks.
- Never stop after one agent if the workflow chain has more runnable tasks.
- Never rely on prose when `wf:`, `kind:`, `origin:`, `phase:`, or `scope:` can answer the question.
- Never use an unscoped task lookup in critical paths.
- Never treat stored task IDs as durable truth across workflows.
- Never spawn Memory Update as a sub-agent.
- Never create `CC10X TODO:` tasks. Non-blocking discoveries go into `**Deferred:**` memory notes.
- Never let REVIEW create implementation tasks without an explicit router/user transition into BUILD.
