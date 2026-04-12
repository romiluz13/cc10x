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
- NEVER use Claude Code's native plan mode (EnterPlanMode). CC10x owns planning. All "plan", "design", "architect", "brainstorm" requests route to the CC10x PLAN workflow — not to the built-in plan mode tool. EnterPlanMode bypasses CC10x orchestration, memory, workflow artifacts, and verification entirely.
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

Core law:
- Durable router state lives under `.claude/cc10x/v10/workflows/{workflow_uuid}.json`
- Companion event log lives under `.claude/cc10x/v10/workflows/{workflow_uuid}.events.jsonl`
- Router-owned gates still include `plan_trust_gate`, `phase_exit_gate`, `failure_stop_gate`, `memory_sync_gate`, and `skill_precedence_gate`

Mandatory reference read:
- Before workflow creation, artifact mutation, hook policy changes, or resume logic that depends on artifact fields, immediately read `references/workflow-artifact-and-hook-policy.md`.
- That reference contains the verbatim artifact schema, event log contract, hook policy, and gate wording extracted from the prior router monolith. Treat it as load-bearing orchestration law, not optional background.

## 3. Task Metadata Contract

Every CC10X task description starts with normalized metadata lines:

```text
wf:{workflow_uuid}
kind:{workflow|agent|remfix|memory|reverify|research}
origin:{router|component-builder|bug-investigator|code-reviewer|silent-failure-hunter|integration-verifier|planner}
phase:{build|build-implement|build-review|build-hunt|build-verify|debug|debug-investigate|debug-review|debug-verify|review|review-audit|plan|plan-create|plan-review-gap-1|plan-review-gap-2|memory-finalize|re-review|re-hunt|re-verify|re-plan|research-web|research-github}
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
- `[cc10x-internal] memory_task_id` in `activeContext.md` is only a transient optimization. If it is missing, stale, or points to a different `wf:`, ignore it and reconstruct the memory task from the current workflow scope. [EASY TO MISS: stale memory_task_id is the #1 cause of cross-workflow pollution]
- Never use an unscoped fallback like "first pending Memory Update task". [EASY TO MISS: unscoped lookups silently pick up orphan tasks from prior workflows]

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
  - [EASY TO MISS: When persisting user decisions, use the user's exact words. Paraphrasing introduces drift that compounds across resume cycles.]

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

**Intent Readiness Gate (MANDATORY before PLAN or BUILD):**
Before dispatching to planner or builder, verify the intent contract meets three conditions:
1. **Context-bounded:** The full intent (goal + constraints + acceptance criteria) fits within the agent's prompt scaffold without truncation. If the intent requires loading more than 5 source files to be understood, decompose first (switch to PLAN).
2. **Contradiction-free:** No acceptance criterion contradicts a stated constraint or non-goal. If contradictions exist, halt and persist `pending_gate="intent_contradiction"`.
3. **Sufficiently specific:** Every acceptance criterion maps to at least one verifiable scenario. If a criterion is unverifiable ("make it better" without a metric), halt and ask for specificity.

Router-owned interface fields:
- `plan_mode`: `direct` | `execution_plan` | `decision_rfc`
- `verification_rigor`: `standard` | `critical_path`
- `checkpoint_type`: `none` | `human_verify` | `decision` | `human_action`
- `proof_status`: `passed` | `gaps_found` | `human_needed`

### BUILD preparation

- Before any BUILD-specific readiness decision or child-task creation, immediately read `references/build-workflow.md`.
- Use the `### BUILD preparation` and `### BUILD task graph` blocks in that file as the canonical BUILD law.

### DEBUG preparation

- Before any DEBUG-specific readiness decision or child-task creation, immediately read `references/debug-workflow.md`.
- Use the `### DEBUG preparation` and `### DEBUG task graph` blocks in that file as the canonical DEBUG law.

### REVIEW preparation

- Before any REVIEW-specific readiness decision or child-task creation, immediately read `references/review-workflow.md`.
- Use the `### REVIEW preparation` and `### REVIEW task graph` blocks in that file as the canonical REVIEW law.

### PLAN preparation

- Before any PLAN-specific readiness decision or child-task creation, immediately read `references/plan-workflow.md`.
- Use the `### PLAN preparation` and `### PLAN task graph` blocks in that file as the canonical PLAN law.
- If planner clarification, review-loop findings, or plan remediation rules trigger later in the workflow, also read `references/remediation-and-research.md` before continuing.

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
  content="{\"workflow_uuid\":\"{workflow_uuid}\",\"workflow_id\":\"{workflow_uuid}\",\"workflow_type\":\"{WORKFLOW}\",\"state_root\":\".claude/cc10x/v10\",\"user_request\":\"{request}\",\"plan_file\":null,\"design_file\":null,\"research_files\":[],\"approved_decisions\":[],\"plan_mode\":null,\"verification_rigor\":\"standard\",\"proof_status\":\"gaps_found\",\"traceability\":{\"requirements\":[],\"phases\":[],\"verification\":[],\"remediation\":[]},\"intent\":{\"goal\":null,\"non_goals\":[],\"constraints\":[],\"acceptance_criteria\":[],\"open_decisions\":[]},\"normalized_phases\":[],\"phase_cursor\":null,\"capabilities\":{\"brightdata_available\":\"unknown\",\"octocode_available\":\"unknown\",\"websearch_available\":\"unknown\",\"webfetch_available\":\"unknown\"},\"research_rounds\":[],\"research_backend_history\":[],\"research_quality\":{\"web\":\"none\",\"github\":\"none\",\"overall\":\"none\"},\"task_ids\":{\"planner_create\":null,\"planning_review_pass1\":null,\"planner_replan\":null,\"planning_review_pass2\":null,\"memory_finalize\":null},\"phase_status\":{},\"results\":{\"builder\":null,\"investigator\":null,\"reviewer\":null,\"hunter\":null,\"verifier\":null,\"planner\":null,\"planning_reviewer\":null,\"research\":{\"web\":null,\"github\":null,\"synthesis\":null}},\"evidence\":{\"builder\":[],\"investigator\":[],\"reviewer\":[],\"hunter\":[],\"verifier\":[],\"planning_reviewer\":[]},\"telemetry\":{\"task_metrics_available\":\"unknown\",\"workflow_wall_clock_seconds\":0,\"agent_wall_clock_seconds\":{\"builder\":0,\"investigator\":0,\"reviewer\":0,\"hunter\":0,\"verifier\":0,\"planner\":0},\"loop_counts\":{\"re_review\":0,\"re_hunt\":0,\"re_verify\":0},\"verifier\":{\"phase_exit_proof_runs\":0,\"extended_audit_runs\":0,\"workload_seconds\":{\"tests\":0,\"build\":0,\"scan\":0,\"reconcile\":0,\"reasoning\":0}}},\"quality\":{\"confidence\":null,\"evidence_complete\":false,\"scenario_coverage\":0,\"research_quality\":\"none\",\"convergence_state\":\"pending\"},\"planning_review_runs\":0,\"planning_review_findings\":[],\"planning_review_status\":\"not_started\",\"memory_notes\":[],\"pending_gate\":null,\"status_history\":[{\"event\":\"workflow_started\",\"ts\":\"{iso_timestamp}\",\"phase\":\"{build|debug|review|plan}\"}],\"remediation_history\":[],\"created_at\":\"{iso_timestamp}\",\"updated_at\":\"{iso_timestamp}\"}"
)
Write(
  file_path=".claude/cc10x/v10/workflows/{workflow_uuid}.events.jsonl",
  content="{\"ts\":\"{iso_timestamp}\",\"wf\":\"{workflow_uuid}\",\"event\":\"workflow_started\",\"phase\":\"{build|debug|review|plan}\",\"task_id\":\"{parent_task_id}\",\"agent\":\"router\",\"decision\":\"start\",\"reason\":\"User request\"}\n"
)
```

Only create child tasks after the v10 artifact exists.

### BUILD task graph

- See `references/build-workflow.md` and apply its `### BUILD task graph` block verbatim before creating BUILD child tasks.

### DEBUG task graph

- See `references/debug-workflow.md` and apply its `### DEBUG task graph` block verbatim before creating DEBUG child tasks.

### REVIEW task graph

- See `references/review-workflow.md` and apply its `### REVIEW task graph` block verbatim before creating REVIEW child tasks.

### PLAN task graph

- See `references/plan-workflow.md` and apply its `### PLAN task graph` block verbatim before creating PLAN child tasks.

### Research tasks

- When a workflow explicitly triggers research task creation, immediately read `references/remediation-and-research.md`.
- Use the `## 10. Research Orchestration`, `## Research Quality`, and `## Research Files` blocks there before creating or consuming research tasks.

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
| `plan-review-gap-1`, `plan-review-gap-2` | `cc10x:plan-gap-reviewer` |
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

## Domain Context
{If UBIQUITOUS_LANGUAGE.md, DOMAIN_GLOSSARY.md, docs/domain/*.md, or project-context.md exist, include content. Otherwise omit section.}

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
- `## Original User Request` only for `plan-gap-reviewer`.
- `## Approved Context Files` only for `plan-gap-reviewer`.
- `## Previous Agent Findings` only for integration-verifier and only after review/hunt phases.

### Prompt assembly rule

- Every routed prompt must be self-contained from the workflow artifact, approved files, and the current task contract.
- Do not rely on prior chat turns or completed-phase narrative when the same fact already exists in the workflow artifact, plan, design, or research files.
- Include only the current-phase objective, live blockers, approved decisions, and directly relevant evidence. Omit unrelated completed-phase detail.

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

### Inline brainstorming handoff

After `Skill(skill="cc10x:brainstorming")`, parse the fenced YAML block under
`### Brainstorming Handoff (MACHINE-READABLE)`.

Required field:
- `DESIGN_FILE`

If present:
- persist it into workflow artifact `design_file`
- pass it to planner as `## Design File`
- do not require `activeContext.md` to be updated first

### Contract overrides

| Agent | Override |
|-------|----------|
| component-builder | `STATUS=PASS` requires `TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0`, `PHASE_STATUS=completed`, `PHASE_EXIT_READY=true`, `PROOF_STATUS=passed`, empty `BLOCKED_ITEMS`, and a non-empty `SCENARIOS` array with at least one passing scenario. That passing scenario must include non-empty `name`, `command`, `expected`, `actual`, and `exit_code`. |
| bug-investigator | `STATUS=FIXED` requires `VERIFICATION_RIGOR` to be explicit, `TDD_RED_EXIT=1`, `TDD_GREEN_EXIT=0`, `VARIANTS_COVERED>=1`, a non-empty `BLAST_RADIUS_SCAN`, and a non-empty `SCENARIOS` array unless it explicitly set `NEEDS_EXTERNAL_RESEARCH=true`. At least one scenario name must start with `Regression:` and one with `Variant:`. Both required scenarios must include non-empty `command`, `expected`, `actual`, and `exit_code`. |
| code-reviewer | `APPROVE` + critical issues becomes `CHANGES_REQUESTED` |
| code-reviewer | `APPROVE` with zero findings across ALL dimensions AND fewer than 3 file:line evidence citations → trigger fallback inline verification. Rubber-stamp approvals without substantive analysis are invalid. |
| silent-failure-hunter | `CLEAN` + critical issues becomes `ISSUES_FOUND` |
| silent-failure-hunter | `CLEAN` with zero error-handling sites inspected OR zero files scanned → trigger fallback inline verification. A CLEAN verdict requires stated scope. |
| integration-verifier | `PASS` + critical issues becomes `FAIL`; scenario totals must reconcile with the scenario table and evidence array; every counted scenario must map to a concrete evidence row; every scenario row must contain non-empty `Expected` and `Actual` values |
| planner | `PLAN_CREATED` or `DECISION_RFC_CREATED` requires non-empty `PLAN_FILE`, explicit `PLAN_MODE`, explicit `VERIFICATION_RIGOR`, `CONFIDENCE>=50`, `GATE_PASSED=true`, a non-empty `SCENARIOS` array, `OPEN_DECISIONS=[]`, and `DIFFERENCES_FROM_AGREEMENT` explicitly present. `PLAN_MODE=decision_rfc` also requires non-empty `ALTERNATIVES` and `DRAWBACKS`; `VERIFICATION_RIGOR=critical_path` requires non-empty `PROVABLE_PROPERTIES`. |
| plan-gap-reviewer | `PASS` requires `BLOCKING_FINDINGS_COUNT=0` and `REPLAN_NEEDED=false`; `FINDINGS` requires explicit finding buckets and a non-empty `REPLAN_REASON` when blocking findings exist. |

Convergence rule:
- If evidence is incomplete, contradictory, or missing for a required pass path, do not advance the workflow.
- Set the workflow artifact `quality.convergence_state` to `needs_iteration` and stop on the appropriate remediation or clarification gate instead of treating the task as good enough.

## 9. Remediation And Workflow Rules

- When remediation, scope resolution, review-to-build escalation, planner clarification, investigation continuation, or the verifier REVERT gate is in play, immediately read `references/remediation-and-research.md`.
- Use the `## 9. Remediation And Workflow Rules` block there as canonical router law.

## 10. Research Orchestration

- See `references/remediation-and-research.md` and apply its `## 10. Research Orchestration`, `## Research Quality`, and `## Research Files` blocks whenever research is triggered or consumed.

## Research Quality

- See `references/remediation-and-research.md` and apply its `## Research Quality` block whenever research quality must be summarized or persisted.

## Research Files

- See `references/remediation-and-research.md` and apply its `## Research Files` block whenever research file paths are handed to planner or investigator.

## 11. Re-Review Loop

- See `references/remediation-and-research.md` and apply its `## 11. Re-Review Loop` block whenever a `kind:remfix` task completes.

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
   - If parallel invocation fails or is unavailable (API error, rate limit): fall back to sequential execution (reviewer first, then hunter). Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log.
6. After each agent returns:
   - capture memory payload immediately
   - validate output
   - persist task-state side effects
   - if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff
   - apply workflow rules
   - for BUILD, run `phase_exit_gate`; if the current phase is not complete, persist `phase_status={partial|blocked}` and stop
   - never advance to the next phase or workflow step on apology prose alone
   - if two agents in the same phase return contradictory verdicts (e.g., reviewer approves but verifier fails on the same evidence), treat the stricter verdict as authoritative and do not average or reconcile the signals. Log the contradiction in `status_history`.
7. Repeat until all tasks in the active `wf:` are completed.
```

### After every agent completion

Pre-check before processing agent output:
- Did the agent address the assigned scope (not a subset or superset)?
- Did tests, builds, or checks referenced in the contract actually run (not merely described)?
- Is follow-up work needed that the agent did not self-remediate?
If any answer is "no" or "unknown", treat as incomplete and apply the fallback validation path below.

0. Capture memory payload first, before validation or task-state mutation.
   - READ-ONLY agents: extract `### Memory Notes (For Workflow-Final Persistence)` immediately after return.
   - WRITE agents: extract `MEMORY_NOTES` from YAML immediately after return.
1. `TaskGet({ taskId })` or `TaskList()` to verify final task state.
2. WRITE agents:
   - They should already have called `TaskUpdate(status="completed")`.
   - Parse YAML before continuing.
3. READ-ONLY agents:
   - Router owns completion fallback for read-only tasks.
   - If the task is still not completed after agent return, router applies fallback `TaskUpdate(status="completed")`.
   - Blockers or findings may change workflow routing, but they never transfer orchestration ownership back to the read-only agent.
4. Memory payload was already captured in step 0:
   - READ-ONLY agents: append extracted notes to the memory task description.
   - WRITE agents: append deferred or supplemental payload needed by the memory task.
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
- Ensure `- Design: {design_file}` remains correct in `activeContext.md ## References` when a design exists.
- If a plan exists, record `Plan saved: {plan_file}` in `activeContext.md ## Recent Changes`.
- If a plan exists, set `activeContext.md ## Next Steps` to `1. Execute plan: {plan_file}` unless the workflow ended in clarification-needed state.

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
- Never report a workflow outcome (pass, fixed, complete) to the user without first confirming the verification evidence that supports that claim. "I believe it works" is not evidence. [EASY TO MISS: "I ran the tests and they passed" without showing command output, exit codes, or scenario evidence is also not evidence. Require concrete proof artifacts, not agent assertions.]
- Never let a remediation loop run more than 3 cycles without a human checkpoint. Drift accumulates silently in long chains.
- Only parallelize agents whose file-write surfaces do not overlap. Reviewer and hunter are read-only and safe to parallelize. Two write agents on overlapping files must be serialized. [EASY TO MISS: Each parallel agent must have a distinct phase value and unique task description. Identical prompts cause agents to duplicate work or silently clobber each other's output.]
- Agents must never inherit raw conversation context. They receive only the structured scaffold from the dispatcher. Leaking conversation history into agent prompts causes scope pollution and non-reproducible behavior.
- Maintain professional objectivity in all routing decisions. Do not rationalize a failing workflow as "close enough" or downgrade critical findings to avoid remediation. The router exists to enforce quality, not to please.
- Agents must never reference or read internal skill files from other agents or skills (e.g., component-builder must never read code-review-patterns/SKILL.md). Cross-agent knowledge flows exclusively through router-mediated scaffolds and workflow artifacts.
- Never use EnterPlanMode. Claude Code's native plan mode is incompatible with CC10x. Planning requests go through the CC10x PLAN workflow (brainstorming → planner → bounded fresh review → memory finalization), which provides orchestration state, workflow artifacts, intent contracts, and verification. Native plan mode provides none of these.
