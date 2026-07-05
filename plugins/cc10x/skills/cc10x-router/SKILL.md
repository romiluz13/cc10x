---
name: cc10x-router
description: |
  THE ONLY ENTRY POINT FOR CC10X. Activate this skill for build, debug, review, and plan requests.

  Use when the user asks to implement, fix, review, plan, test, refactor, or continue code work.

  Trigger keywords: build, implement, create, write, add, review, audit, debug, fix, error, bug, broken, plan, design, architect, spec, brainstorm, test, refactor, optimize, update, change, research, cc10x, c10x.

  CRITICAL: Route and execute immediately. Do not stop at describing capabilities.
---

# cc10x Router

**Runtime contract only.** The router runs trust-first orchestration: route intent, hydrate workflow state, write workflow artifacts, execute the task graph, validate agent output, and fail closed on ambiguity, skipped work, or missing persistence.

## 1. Intent Routing

Route using the first matching signal:

| Priority | Signal | Keywords | Workflow | Chain |
| ---------- | -------- | ---------- | ---------- | ------- |
| 1 | ERROR | error, bug, fix, broken, crash, fail, debug, troubleshoot, issue | DEBUG | bug-investigator -> code-reviewer -> integration-verifier |
| 2 | PLAN | plan, design, architect, roadmap, strategy, spec, brainstorm | PLAN | exploration -> planner -> bounded fresh review loop |
| 3 | REVIEW | review, audit, analyze, assess, "is this good" | REVIEW | code-reviewer |
| 4 | ORIENT | zoom out, explain, understand, "how does X work", unfamiliar, "map this", "walk me through", "where is", "what does this do" | ORIENT | advisory orientation (no agents) |
| 5 | DEFAULT | Everything else | BUILD | component-builder → [code-reviewer ‖ failure-hunter] → integration-verifier |

Rules:

- Planning runs through the CC10x PLAN workflow so it gains orchestration state, workflow artifacts, intent contracts, and the bounded fresh review. Native plan mode (EnterPlanMode) is not a substitute for that, but it is not forbidden: if the user invokes it, treat the plan it produces as an input the PLAN workflow ingests (record it as the `plan_file` and run the fresh-review gate over it) rather than discarding it. Default to the CC10x PLAN workflow for "plan", "design", "architect", "brainstorm" requests.
- ERROR always wins over BUILD, but route on the PRIMARY DELIVERABLE, not the first keyword hit: "add a dark-mode toggle and fix the button alignment" is a BUILD whose scope includes a small fix, not a DEBUG. Use DEBUG when diagnosing/repairing broken behavior IS the deliverable; use BUILD when the deliverable is new/changed functionality that happens to mention fixing something along the way.
- REVIEW is advisory only. Never let REVIEW create code-changing tasks.
- ORIENT is read-only and advisory. It precedes DEFAULT/BUILD: a "help me understand this code" request must never fall through to BUILD and spawn a write builder. ORIENT spawns NO write agents and creates NO phase graph. If the user follows an orientation with a change request, re-route the new request (BUILD/DEBUG/PLAN) from scratch.
- BUILD uses a complexity gradient (see `references/build-workflow.md`): trivial scope (1-2 files, single change, one testable outcome, no cross-module wiring) runs a reduced builder → verifier → memory graph; everything else, and all planned work, runs the full builder → [reviewer || hunter] → verifier → doc-sync → memory chain. The reviewer and hunter run in parallel (two read-only agents in the same message) and the router merges their findings before verifier handoff. The builder escalates trivial → full on any scope increase. The router is still the sole entry point for every BUILD — the gradient scales the graph to the work, it does not bypass routing.
- Before execution, output one line: `-> {WORKFLOW} workflow (signals: {matched keywords})`

### ORIENT move (read-only)

Triggered when the user wants to understand existing code, not change it ("zoom out", "explain", "how does X work", "I'm unfamiliar with", "map this", "walk me through", "where is X", "what does this do"). The router answers inline — no `TaskCreate`, no workflow artifact, no phase graph, no write agents.

Orientation procedure:

1. Map the relevant modules/files for the named subject (use `localViewStructure` / `localFindFiles` / `localSearchCode` to locate, read only the slices needed to explain).
2. Trace ONE layer up: callers and dependents of the focal symbols via LSP call-hierarchy (`lspCallHierarchy`) and references (`lspFindReferences`); run `localSearchCode` first to get the exact `lineHint` before any LSP call.
3. Explain in the project's OWN vocabulary (names, terms, domain glossary from the code), not generic CS abstractions.
4. Stop at understanding. Do not propose or apply edits. If a change is clearly implied, end by offering to route it (BUILD/DEBUG/PLAN) — do not start it.

Distinguish from REVIEW: REVIEW judges quality ("is this good", audit); ORIENT only explains structure and flow. When both could match, prefer ORIENT for "help me understand", REVIEW for "tell me what's wrong".

## 2. Memory Load And Template Validation

Always run this before routing or resuming:

```text
1. Bash("mkdir -p .cc10x")
2. Read(".cc10x/activeContext.md")
3. Read(".cc10x/patterns.md")
4. Read(".cc10x/progress.md")
```

Do not parallelize step 1 with reads.

If a memory file is missing:

- Create it using the `cc10x:memory-and-handoff` template.
- Read it before continuing.

Required sections:

| File | Required Sections |
| ------ | ------------------- |
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

Trust rule:

- `JUST_GO` never overrides explicit user/project standards, open plan decisions, or failure-stop gates.
- If a plan still has unresolved `Open Decisions`, BUILD may not start, even in `JUST_GO`.

## 2a. Workflow Artifact And Hook Policy

Core law:

- Durable router state lives under `.cc10x/workflows/{workflow_uuid}.json`
- Companion event log lives under `.cc10x/workflows/{workflow_uuid}.events.jsonl`
- Router-owned gates still include `plan_trust_gate`, `phase_exit_gate`, `failure_stop_gate`, `memory_sync_gate`, and `skill_precedence_gate`

Mandatory reference read:

- Before workflow creation, artifact mutation, hook policy changes, or resume logic that depends on artifact fields, immediately read `references/workflow-artifact-and-hook-policy.md`.
- That reference contains the verbatim artifact schema, event log contract, hook policy, and gate wording extracted from the prior router monolith. Treat it as load-bearing orchestration law, not optional background.

## 3. Task Metadata Contract

Every CC10X task description starts with normalized metadata lines:

```text
wf:{workflow_uuid}
kind:{workflow|agent|remfix|memory|reverify|research}
origin:{router|component-builder|bug-investigator|code-reviewer|integration-verifier|planner}
phase:{build|build-implement|build-review|build-hunt|build-verify|build-doc-sync|build-finish|debug|debug-investigate|debug-review|debug-verify|review|review-audit|plan|plan-create|plan-review-gap-1|plan-review-gap-2|memory-finalize|re-review|re-hunt|re-verify|re-plan|research-web|research-github}
plan:{path|N/A}
scope:{ALL_ISSUES|CRITICAL_ONLY|N/A}
reason:{short reason or N/A}
```

Rules:

- ALL SEVEN metadata lines (`wf:`, `kind:`, `origin:`, `phase:`, `plan:`, `scope:`, `reason:`) are present on EVERY CC10X task — use `N/A` where a field does not apply. The TaskCompleted hook audits exactly this invariant; the task-graph templates already satisfy it.
- `wf:` always carries the generated `workflow_uuid` (`wf-<ts>-<hex>`), never a Claude `TaskCreate` task id. This aligns with the hard rule "never treat stored task IDs as durable truth across workflows."
- Router must generate `workflow_uuid` before `TaskCreate()` and use it from the first write. `wf:PENDING_SELF` is not used.
- `kind:` drives resume, routing, and counting logic.
- `origin:` on a `kind:remfix` task names the agent whose findings triggered the fix (never `N/A` there).
- `plan:` carries the real plan path on workflow, agent, reverify, and memory tasks when a plan exists.
- `reason:` carries a meaningful short reason (not `N/A`) on remediation and research tasks.
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
- Read and write only the `.cc10x/` state namespace (memory `.cc10x/*.md`, workflows `.cc10x/workflows/*`). Ignore any legacy version-segmented layout such as `.cc10x/v10/*` or `.claude/cc10x/*` left over from older installs during hydration.
- `[cc10x-internal] memory_task_id` in `activeContext.md` is only a transient optimization. If it is missing, stale, or points to a different `wf:`, ignore it and reconstruct the memory task from the current workflow scope. [EASY TO MISS: stale memory_task_id is the #1 cause of cross-workflow pollution]
- Never use an unscoped fallback like "first pending Memory Update task". [EASY TO MISS: unscoped lookups silently pick up orphan tasks from prior workflows]

Resume algorithm:

0. If `.cc10x/stop-state.json` or `.cc10x/precompact-state.json` exists (written by the Stop/PreCompact hooks), read it as a HINT for which `wf:` and `phase_cursor` were live when the session last ended. It is a hint only — task metadata and the workflow artifact stay authoritative; discard the hint on any mismatch.
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
  - block downstream re-review / verifier tasks as normal
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
- Read the latest `.cc10x/workflows/*.json` artifact if one exists for the current conversation.

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

1. Create the parent workflow task with that UUID from the first write:

```text
TaskCreate({
  subject: "CC10X {WORKFLOW}: {summary}",
  description: "wf:{workflow_uuid}\nkind:workflow\norigin:router\nphase:{build|debug|review|plan}\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:User request\n\nUser request: {request}\nChain: {chain description}",
  activeForm: "{workflow active form}"
})
```

1. Immediately create the workflow artifact and event log. **Do NOT hand-type the artifact JSON.** Copy the canonical skeleton, then substitute only the live fields:

```text
Bash(command="mkdir -p .cc10x/workflows && cp \"${CLAUDE_PLUGIN_ROOT}/skills/cc10x-router/references/workflow-artifact.skeleton.json\" .cc10x/workflows/{workflow_uuid}.json")
```

Then `Edit` the copied file, replacing each placeholder token with the live value (the skeleton ships every required key already populated with safe defaults — you only fill these):

- `__WORKFLOW_UUID__` → `{workflow_uuid}` (appears twice: `workflow_uuid` and `workflow_id`)
- `__WORKFLOW_TYPE__` → `{WORKFLOW}` (BUILD | DEBUG | REVIEW | PLAN) — **if routing (§5) has not yet determined the workflow type, use `pending` and update it after §5 resolves.** Never hardcode BUILD before routing completes. The artifact may be created before routing (to capture state early), but `workflow_type` must reflect the actual routed type after §5.
- `__USER_REQUEST__` → the user request (JSON-escape quotes/newlines)
- `__PHASE__` → `{build|debug|review|plan}`
- `__ISO_TIMESTAMP__` → the current UTC ISO timestamp (appears 3×: `status_history[0].ts`, `created_at`, `updated_at`)

Use `Edit(replace_all=true)` for `__WORKFLOW_UUID__` and `__ISO_TIMESTAMP__` since each repeats. Then write the event log:

```text
Write(
  file_path=".cc10x/workflows/{workflow_uuid}.events.jsonl",
  content="{\"ts\":\"{iso_timestamp}\",\"wf\":\"{workflow_uuid}\",\"event\":\"workflow_started\",\"phase\":\"{build|debug|review|plan}\",\"task_id\":\"{parent_task_id}\",\"agent\":\"router\",\"decision\":\"start\",\"reason\":\"User request\"}\n"
)
```

**Read-back gate (MANDATORY before any child `TaskCreate`):** `Read(".cc10x/workflows/{workflow_uuid}.json")` and confirm (a) it parses as JSON, (b) `workflow_uuid` equals the generated UUID, and (c) no `__PLACEHOLDER__` tokens remain. If any check fails, fix the file and re-read before proceeding. The PostToolUse artifact guard also validates this write in `block` mode and will reject a malformed or key-missing artifact — but the router must not rely on the guard alone; confirm the read-back first.

Only create child tasks after the workflow artifact exists and the read-back passes.

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
| ------------------- | ------- |
| `build-implement` | `cc10x:component-builder` |
| `debug-investigate` | `cc10x:bug-investigator` |
| `build-review`, `debug-review`, `review-audit`, `re-review` | `cc10x:code-reviewer` |
| `build-hunt`, `re-hunt` | `cc10x:failure-hunter` |
| `build-verify`, `debug-verify`, `re-verify` | `cc10x:integration-verifier` |
| `plan-create`, `re-plan` | `cc10x:planner` |
| `plan-review-gap-1`, `plan-review-gap-2` | `cc10x:plan-gap-reviewer` |
| `research-web` | `cc10x:researcher` |
| `research-github` | `cc10x:researcher` |
| `kind:remfix` + `origin:bug-investigator` | `cc10x:bug-investigator` |
| `build-doc-sync` | `cc10x:doc-syncer` |
| `kind:remfix` + `origin:code-reviewer` / `origin:integration-verifier` / `origin:router` | `cc10x:component-builder` |

### Per-role model-tier policy

The router dispatches a full agent chain per phase. Match the model tier to the role's cognitive load instead of inheriting the session model for everything. Tiers are abstract: `cheap` (small/fast), `standard` (mid), `capable` (frontier). Resolve each to the concrete model id the host exposes at dispatch time.

| Role / phase | Recommended tier | Why |
| -------------- | ------------------ | ----- |
| `component-builder` on trivial scope, transcription/mechanical builds (rote wiring, single-change, codegen-from-spec) | cheap | Mechanical execution against an explicit spec; little judgment. |
| `doc-syncer` | cheap | Mechanical diff-driven doc edits. |
| `component-builder` on multi-file / cross-module integration | standard | Real wiring decisions across files; needs coherence. |
| `code-reviewer` | standard (FLOOR) | Judgment under adversarial intent; see reviewer floor below. |
| `bug-investigator` | standard | Hypothesis search; escalate to capable on a stubborn root cause. |
| `planner`, `plan-gap-reviewer` | capable | Architecture and decomposition; cheap planning poisons the whole chain. |
| `integration-verifier` (final phase, REVERT authority) | capable | Last line before "done"; must not miss scenario gaps. |
| `researcher` | standard | Retrieval + synthesis. |

How tiers are realized (ADVISORY — mechanism honesty): Claude Code selects a subagent's model from the agent's frontmatter `model:` field; the Task/Agent dispatch has NO per-call model parameter, so the router cannot set the model at dispatch time. cc10x therefore ships `model: haiku` on `doc-syncer` (safely mechanical) and `model: inherit` everywhere else so the user's session model choice is respected. Treat the table above as guidance for users tuning agent frontmatter (or for hosts that do expose per-dispatch model selection) — never claim a tier was applied when the mechanism cannot apply it.

Reviewer FLOOR — never run a verifier or reviewer (`code-reviewer`, `integration-verifier`, `plan-gap-reviewer`) on the cheapest tier. The cheapest tier rubber-stamps. Mid-tier is the floor for anything that gates quality; bump UP, never below.

Turn-count dominates price — a capable model that one-shots a phase is cheaper than a cheap model that loops three times re-reading state and re-trying. When a role tends to iterate (planner, verifier, stubborn investigation), prefer the higher tier even though its per-token cost is greater: fewer turns wins. Under `JUST_GO`, still apply this policy where the mechanism allows — never downgrade a gating role's frontmatter below the reviewer floor to save tokens.

### Prompt scaffold for every agent

```text
## Task Context
- Task ID: {task_id}
- Parent Workflow ID: {workflow_uuid}
- Task Phase: {phase}
- Plan File: {plan_file or 'None'}
- Workflow Scope: wf:{workflow_uuid}
- Workflow Artifact: .cc10x/workflows/{workflow_uuid}.json

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

Anti-anchoring exception: for adversarial read-only dispatches (`code-reviewer`, `plan-gap-reviewer`) OMIT `## Memory Summary` — it carries the implementer's own narrative (decisions, learnings) and anchors the auditor. Keep `## Project Patterns` (user standards and gotchas are neutral law, not author narrative). Approved decisions the reviewer genuinely needs travel via `## Pre-Answered Requirements` / `## Intent Contract`, never via the memory summary.

Optional sections:

- `## Pre-Answered Requirements` for BUILD when router already gathered decisions.
- `## Intent Contract` when a plan or design already defined goal, constraints, acceptance criteria, and named scenarios.
- `## Research Files` only when at least one research file exists.
- `## Research Quality` only when at least one research result exists.
- `## Design File` only for planner.
- `## Planning Review Findings` only for `re-plan`.
- `## Original User Request` only for `plan-gap-reviewer`.
- `## Approved Context Files` only for `plan-gap-reviewer`.
- `## Previous Agent Findings` only for integration-verifier and only after a review phase ran.

### Prompt assembly rule

- Every routed prompt must be self-contained from the workflow artifact, approved files, and the current task contract.
- Do not rely on prior chat turns or completed-phase narrative when the same fact already exists in the workflow artifact, plan, design, or research files.
- Include only the current-phase objective, live blockers, approved decisions, and directly relevant evidence. Omit unrelated completed-phase detail.
- **Anti-pre-judging guard (adversarial dispatches only):** before dispatching `code-reviewer`, `failure-hunter`, or `plan-gap-reviewer`, scan the constructed prompt for bias phrases — "do not flag", "don't treat X as a defect", "at most Minor", "the plan chose", "should be fine", "no need to check". If any are present, rewrite them out: you are pre-judging the reviewer's verdict before they have seen the code. The router knows the plan, the intent contract, and the approved decisions — that knowledge can unknowingly inject bias ("the plan chose approach X, so don't flag Y"). Reviewers must form their own opinion from the diff. State approved decisions as neutral facts ("approach X was approved for reason Z"), never as instructions to suppress findings.

### Deterministic skill hints

- Router is the only authority allowed to load internal CC10X skills.
- Agents may not self-activate `frontend` or `architecture`.
- Include `cc10x:frontend` only when the request, changed files, plan, or design targets UI/frontend work. The skill has two modes: authoring (build UI with patterns) and critique (score built UI). Router selects mode via dispatch context.
- Include `cc10x:architecture` only for multi-component, API, schema, auth, or integration-heavy work.
- Include `cc10x:research` only when planner or investigator receives `## Research Files`.
- Include `cc10x:exploration` only on an explicit de-risk/spike intent ("spike", "try out", "what should this look like", "prototype", "throwaway") — never as the default for a real build. The skill has two modes: design (brainstorm a design) and spike (throwaway prototype). Absorbing a spike's answer is a fresh gated BUILD, not promotion.
- Include `cc10x:codebase-hygiene` only when (a) the code-reviewer is asked for a reuse/consolidation audit or the request targets semantic duplication, OR (b) the request targets retrofitting/deepening shallow modules in EXISTING code (not greenfield architecture, which stays `cc10x:architecture`). The skill has two modes: duplicate detection and module deepening.
- Include `cc10x:mcp-cli` only when a researcher needs a one-off MCP capability that is not already mounted.
- Include `cc10x:code-review` only when a human/external reviewer's feedback (pasted PR comments, review notes, "can you change X") must be acted on — it governs verify-before-agreeing in the MAIN session, not the internal reviewer→router→fix loop.
- Include `cc10x:memory-and-handoff` only when work is being handed to a coworker, a different tool, or a fresh non-cc10x session.
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

### Failure Hunter
**Critical Issues:**
{hunter critical issues or "None / not in this workflow"}
```

DEBUG skips the hunter.

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

Before post-agent validation, read `references/workflow-artifact-and-hook-policy.md` §contracts for the per-agent required-field table and the contract-override pass conditions.

If the YAML block is missing or malformed:

- Treat the task as invalid output.
- Do not continue the workflow based on prose alone.
- Re-run inline verification and fail safe.

### Inline exploration handoff

After `Skill(skill="cc10x:exploration")`, parse the fenced YAML block under
`### Brainstorming Handoff (MACHINE-READABLE)`.

Required field:

- `DESIGN_FILE`

If present:

- persist it into workflow artifact `design_file`
- pass it to planner as `## Design File`
- do not require `activeContext.md` to be updated first

### Contract overrides

- Before treating any agent `STATUS`/verdict as a pass, read `references/workflow-artifact-and-hook-policy.md` §contracts and apply the per-agent contract-override pass conditions verbatim (the `STATUS=PASS`/`FIXED`/`APPROVE`/`PLAN_CREATED`/`COMPLETE` gates, plus the reviewer rubber-stamp fallback).

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

## 11b. Loop Discipline (Vocabulary)

The harness is a loop engine. These concepts govern how the loop runs:

| Concept | Meaning |
| --------- | --------- |
| **Trigger** | The event that starts or resumes a loop iteration — user request, agent completion, checkpoint resolution. Every loop iteration has exactly one trigger. |
| **Checkpoint** | A point where the loop pauses for human input. Only on irreversible actions, real scope changes, or input only the user can provide. Checkpoints are NOT for narration or "want me to continue?" prompts. |
| **Push right** | Defer checkpoints as far as possible — do maximal work before involving the human. The loop should never stop on a promise or plan when it could act. If the next step is reversible and follows from the original request, proceed without asking. |
| **Brief** | The decision-ready summary the loop produces when pausing. Not raw output, not a diary — the one thing the human needs to decide next. Outcome first, supporting detail second. |
| **Cycle** | One complete plan → build → verify → learn iteration. The circuit breaker caps cycles at 3 before requiring a human checkpoint. |
| **Convergence** | The loop's quality signal — when `quality.convergence_state` transitions from `needs_iteration` to `converged`, the loop is complete. Never declare convergence on prose alone. |

**Autonomous mode:** When the user sets a goal that spans multiple iterations (e.g., `/goal` or explicit "do this end-to-end"), the loop runs without checkpointing for reversible actions. The user is not watching in real time and cannot answer questions mid-task. Before ending a turn, check the last paragraph — if it is a plan, analysis, question, list of next steps, or a promise about work not yet done, do that work now with tool calls. End the turn only when the task is complete or blocked on input only the user can provide.

## 12. Chain Execution Loop

```text
1. TaskList()
2. Select tasks in the active `wf:` where:
   - status is pending or in_progress
   - blockedBy is empty or all blockers are completed
3. If the runnable task kind is memory:
   - execute inline in the main context
   - persist workflow artifact results + Memory Notes from the task description
   - append `memory_finalized` to `.cc10x/workflows/{wf}.events.jsonl`
   - clean up the matching [cc10x-internal] memory_task_id entry
   - mark the memory task completed
   - mark the parent workflow task completed
   - continue
4. Otherwise, map each runnable task through the dispatcher table.
5. Mark each task in_progress before invoking its agent. If `code-reviewer` and `failure-hunter` are both ready in BUILD: mark both in_progress first, invoke them in the same message. They are read-only and safe to parallelize.
   - If parallel invocation fails or is unavailable (API error, rate limit, agent not found): fall back to sequential execution — dispatch `code-reviewer` first, wait for it to complete, then dispatch `failure-hunter`. Do NOT substitute the hunter with a different agent (e.g., bug-investigator). Do NOT skip the hunter. The hunter is a read-only agent with a specific adversarial posture — no other agent can replace it. Never block a workflow because parallelism is unavailable. Log `event=parallel_fallback` in the workflow event log.
6. After each agent returns:
   - capture memory payload immediately
   - validate output
   - persist task-state side effects
   - if BUILD review and hunt are both complete for the current phase, write one router-owned merged findings summary into the existing workflow results before verifier handoff
   - apply workflow rules
   - for BUILD, run `phase_exit_gate`; if the current phase is not complete, persist `phase_status={partial|blocked}` and stop
   - never advance to the next phase or workflow step on apology prose alone
   - if two agents in the same phase return contradictory verdicts (e.g., reviewer approves but verifier fails on the same evidence), treat the stricter verdict as authoritative and do not average or reconcile the signals. Log the contradiction in `status_history`.
   - **Cross-reviewer agreement promotion:** if `code-reviewer` and `failure-hunter` independently flag the SAME finding (same file:line, same defect, raised from different passes), that is stronger signal than either alone — promote the merged finding's confidence by one tier (80→90, or mark it `cross-confirmed` in the merged findings summary). Agreement between two mutually-blind reviewers is independent confirmation; use it. Promotion never overrides the quote-the-line gate — a finding without a verbatim `file:line` quote cannot be promoted, only demoted.
   - doc-syncer `STATUS=SKIPPED` is a passing state; advance to Memory Update immediately
   - doc-syncer STATUS=PARTIAL: soft pass; advance to Memory Update; persist doc_sync_partial=true in workflow artifact results.doc_syncer for user review
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
5. Update `.cc10x/workflows/{workflow_uuid}.json` with:
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
   - **`updated_at` timestamp MUST be set to the current ISO timestamp** — a stale `updated_at` breaks resume logic and triggers the TaskCompleted guard's stale-artifact warning.
   **READ-BACK GATE (MANDATORY):** After writing the artifact, Read it back and confirm:
   - `updated_at` is set to a timestamp from THIS turn (not a prior turn)
   - `results.{agent_name}` exists and contains the agent's contract fields
   - If either check fails, rewrite the artifact immediately. Do not proceed to the next task.
6. **Append event log entry:** For each result persisted to the artifact in step 5, append a matching entry to `.cc10x/workflows/{wf}.events.jsonl`:

   ```json
   {"ts":"<ISO>","wf":"<wf_id>","event":"result_persisted","phase":"<phase>","task_id":"<task_id>","agent":"<agent_name>","decision":"<contract_status>","reason":"<one-line summary>"}
   ```

   The event log MUST stay in sync with the artifact. A mutation without an event log entry is a desync that breaks the audit trail. (The PostToolUse guard auto-appends a fallback `artifact_mutated` event, but the router MUST write the semantic `result_persisted` entry with agent-specific metadata.)
7. Persist `[cc10x-internal] memory_task_id: {memory_task_id} wf:{workflow_uuid}` only if it matches the active workflow.

### Verifier findings handoff

Before invoking `integration-verifier` in BUILD:

- Read `results.reviewer` and `results.hunter` from the workflow artifact.
- Build `## Previous Agent Findings` exactly in the format verifier expects:

  ```
  ## Previous Agent Findings

  ### Code Reviewer
  **Verdict:** {Approve|Changes Requested}
  **Critical Issues:**
  {reviewer critical issues or "None"}

  ### Failure Hunter
  **Critical Issues:**
  {hunter critical issues or "None / not in this workflow"}
  ```

- Never invoke verifier without that section when review/hunt already ran.

**Post-verifier finding validation (act on hallucinated findings):** after the verifier returns, read its `### Reviewer Finding Validation` section. For any finding the verifier marked `validated: false`, DROP that finding from the merged findings set before creating a REM-FIX task — a hallucinated critical finding must not gate the phase or waste a builder cycle. Log the dropped finding in `status_history` (`finding_dropped: hallucinated — verifier could not confirm quote at file:line`). For `validated: degraded` CRITICAL/HIGH findings, KEEP them in the blocking set (fail-safe — a transient access failure must never silently remove a critical finding). This gate runs BEFORE the REM-FIX scope decision in §remediation-and-research, so `CRITICAL_ONLY` / `ALL_ISSUES` scope is computed over validated findings only.

### Inline no-subagent execution (FALLBACK — not the default)

The default execution model is per-phase subagent dispatch: every phase runs in a fresh-context agent via the dispatcher (§7), and that remains the default whenever the Task/Agent primitive is available AND the work is separable. The fallback below is a bounded degrade mode, NOT a shortcut to reach for when dispatch feels heavy. Prefer subagents. Only enter inline mode on one of the two triggers, and record which one in `status_history`.

**Enter inline mode when EITHER trigger holds:**

1. **Primitive unavailable (graceful degrade):** the host harness does not expose the Task/Agent primitive (no `Agent(...)` dispatch path, or `TaskCreate`/`TaskList` are absent). Without it the router cannot spawn phase agents at all; rather than be inoperative, it executes the plan itself.
2. **Tightly-coupled work (anti-thrash):** the phases are so coupled that isolated phase agents would thrash — they cannot share in-flight state (e.g. a builder and its verifier must observe the same uncommitted in-memory/scratch state, or a phase boundary cannot be expressed as a self-contained scaffold without re-deriving most of the prior phase). Splitting such work across isolated agents loses the shared state at every handoff. When the §5 Intent Readiness Gate shows the phases cannot be cleanly decomposed into self-contained scaffolds, that is this trigger.

**What changes vs. default:** the ROUTER executes each phase's work inline, in the main session, instead of spawning the phase agent. Walk the same task graph in the same order the dispatcher would. Lose the subagent isolation — KEEP every gate.

**What does NOT change (the gates stay fail-closed):**

- Run `phase_exit_gate` at each phase boundary exactly as in the default loop step 6 — if the phase is not complete, persist `phase_status={partial|blocked}` and stop. No phase advances on prose.
- Persist structured results into the workflow artifact, including `results.baseline` and the per-phase results the spawned agent would have written. The artifact remains the source of truth; do not rely on conversation narrative.
- Compute the **clean-baseline diff** the same way: record the baseline before the build phase, and at verification diff the working tree against it so the verifier checks only this workflow's changes.
- Run an **inline verification pass** in place of spawning `integration-verifier`: the router itself applies the integration-verifier's checks (run the scenarios, capture `Expected`/`Actual` evidence per scenario, reconcile `SCENARIOS_TOTAL`/`PASSED`/`FAILED`, and honor the REVERT authority) and writes the same scenario-accounting into the artifact that §8 post-agent validation would parse. The point is to lose the subagent, not the verification — incomplete or contradictory evidence still sets `quality.convergence_state=needs_iteration` and stops on the remediation gate.
- All §14 hard rules still bind: never report pass/fixed/complete without confirming the verification evidence, never exceed the 3-cycle remediation limit without a human checkpoint, fail closed on ambiguity or skipped work.

**The cost — be disciplined about it:** inline mode forfeits fresh-context isolation. The router now carries the build, review, and verify context in one session, so context can bleed across phases (the very pollution subagents prevent). Counter it: between phases, re-ground from the workflow artifact rather than from earlier turns; include only the current-phase objective and live evidence when reasoning about a phase; treat completed-phase narrative as stale. If the session context grows large enough to threaten this discipline, prefer returning to subagent dispatch over pushing further inline.

**Mode bookkeeping:** persist `execution_mode="inline_fallback"` and `inline_fallback_reason={primitive_unavailable|tightly_coupled}` in the workflow artifact, and log an `event=inline_fallback_entered` entry in `.cc10x/workflows/{wf}.events.jsonl`. If the primitive becomes available again and the remaining work is separable, the router MAY resume default subagent dispatch for later phases; log `event=inline_fallback_exited`.

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
- **Knowledge compounding check (BUILD/DEBUG only):** before the final write, evaluate whether this workflow's evidence crosses the solution-doc threshold: (a) the debug attempt count in `activeContext.md` for this `wf:` reached 3+ `[DEBUG-N]:` entries before resolving, OR (b) the reviewer/hunter blast-radius scan touched 3+ files with the same defect pattern, OR (c) the winning fix contradicts a documented assumption in `patterns.md`. If any condition is true, write `docs/solutions/{category}/{slug}.md` using the format in `cc10x:memory-and-handoff` (Problem / What Didn't Work / Solution / Why / Prevention), then reference it from `activeContext.md ## Learnings`. If none apply, skip — do not create a solution doc for mechanical fixes.
- If any artifact or memory write fails, stop immediately. Never advance the workflow after a failed persistence write.

For PLAN:

- Ensure `- Plan: {plan_file}` remains correct in `activeContext.md ## References`.
- Ensure `- Design: {design_file}` remains correct in `activeContext.md ## References` when a design exists.
- If a plan exists, record `Plan saved: {plan_file}` in `activeContext.md ## Recent Changes`.
- If a plan exists, set `activeContext.md ## Next Steps` to `1. Execute plan: {plan_file}` unless the workflow ended in clarification-needed state.

For DEBUG:

- Preserve the latest `[DEBUG-RESET: wf:{workflow_uuid}]` section in `## Recent Changes` and summarize the final result beneath it.

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
- `DIFF_DRIVEN_DOCS: skip` in Session Settings disables doc-syncer for projects that manage documentation separately; when present, skip `build-doc-sync` task creation and block Memory Update on `verifier_task_id` directly.
- Agents must never read another agent's live contract output or router-internal task bookkeeping (TaskList/TaskGet state, `[cc10x-internal]` markers, `status_history`, other agents' `results.*` entries). The workflow artifact itself is dispatch-readable BY REFERENCE: an agent may read the artifact path handed to it in the scaffold, but only the sections its dispatch names (`intent`, `normalized_phases`, its own phase's `results`/`evidence`/`baseline`) — cross-agent orchestration knowledge still flows exclusively through router-mediated scaffolds. Reading a shared pattern/reference doc for domain guidance is fine; inheriting another agent's live state is not.
- Native plan mode (EnterPlanMode) is not the planning substrate — the CC10x PLAN workflow is, because it carries orchestration state, workflow artifacts, intent contracts, and the bounded fresh review. But a plan the user produced via native plan mode is an acceptable input: ingest it as the `plan_file` and run the fresh-review gate over it rather than rejecting it outright.
- Workspace isolation and branch finishing are router-owned, optional, and gated — never auto-run. At BUILD/PLAN start the router MAY offer worktree isolation, deferring to a native worktree primitive (e.g. EnterWorktree) when one exists and skipping silently when none does — cc10x never hard-requires git worktrees. After the final phase verifies PASS, the router MAY offer a finishing menu (merge / open-PR / keep / discard) via a single AskUserQuestion; it must never execute a destructive git operation (merge into a base branch, branch delete, force-push, discard) without the user's explicit menu choice, and JUST_GO auto-defaults this gate to the non-destructive `keep as-is` option. Both offers are skipped for `build_scope=trivial`. See references/build-workflow.md `### BUILD-DONE finishing (optional)` for the canonical wording.
- A terse imperative specifies the GOAL, not the METHOD. "just add the endpoint", "quickly fix X", "simply wire Y" name a destination; they do NOT waive `phase_exit_gate`, the TDD/verifier chain, the complexity gradient's trivial→full escalation, or any governing workflow. Terseness lowers ceremony, never rigor. Treat "just"/"quickly"/"simply" as urgency cues, not as permission to skip routing or gates.
- Route-and-load the governing workflow BEFORE asking clarifications or exploring. The workflow reference (`references/build-workflow.md`, `references/debug-workflow.md`, `references/review-workflow.md`, `references/plan-workflow.md`) tells you HOW to ask and what readiness it needs; do not freelance clarifying questions or broad exploration ahead of loading it.

### Capability-offer interaction principle

Optional, cost-bearing capabilities (worktree isolation, research accelerators / web+github researchers, the BUILD-DONE finishing menu) are offered under restraint:

- Offer only when warranted by the actual task, never reflexively.
- Put the offer in its OWN message — just the offer, nothing else bundled in — so it is easy to decline without derailing the work.
- Be honest about cost: name that the capability is token-/cost-intensive or slower when it is.
- NEVER re-offer a capability once the user has declined it, unless the user raises it again themselves. A declined offer is a closed decision for the rest of the session.
