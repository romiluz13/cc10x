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
| 2b | Planner needs clarification | Ask the user, persist answers, then restart PLAN with a fresh visible DAG after clarification. |
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
- If this was the initial `plan-create` task, prune the unused pre-created review branch before continuing:
  - mark `plan-review-gap-1`, `re-plan`, and `plan-review-gap-2` as `deleted`
- Persist answers in `activeContext.md ## Decisions`.
- Create a follow-up PLAN workflow after the user answers clarification.
- Do not mutate BUILD/DEBUG/REVIEW. Clarification answers restart PLAN with a fresh visible DAG.

When planner returns `STATUS=PLAN_CREATED` or `STATUS=DECISION_RFC_CREATED`:
- Verify `PLAN_FILE` exists with `Glob(...)`.
- Extract the intent/spec header from the saved plan and persist it into workflow artifact `intent`.
- Update the parent workflow task `plan:` line to the saved plan path.
- Update the pending memory task `plan:` line to the same saved plan path so resume and finalization stay scoped to the real artifact.
- Persist planner fresh-review fields when present:
  - `planning_review_runs`
  - `planning_review_status`
- Do not create a new review task here. The bounded PLAN DAG already contains both fresh-review passes.
- If the completed planner phase was `plan-create`:
  - update the pre-created `plan-review-gap-1` task `plan:` line to `{plan_file}`
  - keep `planning_review_status=pending_review`
- If the completed planner phase was `re-plan`:
  - update the pre-created `plan-review-gap-2` task `plan:` line to `{plan_file}`
  - keep `planning_review_status=pending_review`
- `planning_review_runs` counts only completed fresh-review passes with valid contract output. Invalid or malformed reviewer output must fail closed without consuming one of the two allowed passes.

When `plan-gap-reviewer` pass 1 returns `PASS`:
- Increment `planning_review_runs += 1`
- Set `planning_review_status=passed`
- Persist findings summary into `results.planning_reviewer`
- Mark the pre-created `re-plan` and `plan-review-gap-2` tasks as `deleted`
- Continue to memory finalization

When `plan-gap-reviewer` pass 1 returns `FINDINGS`:
- Increment `planning_review_runs += 1`
- Persist findings into:
  - `planning_review_findings`
  - `planning_review_status=findings_received`
  - `results.planning_reviewer`
- Do not create a new `re-plan` task. The pre-created `re-plan` task becomes the next runnable PLAN node.

When `plan-gap-reviewer` pass 2 returns `PASS`:
- Increment `planning_review_runs += 1`
- Set `planning_review_status=passed`
- Persist findings summary into `results.planning_reviewer`
- Continue to memory finalization

When `plan-gap-reviewer` pass 2 returns `FINDINGS`:
- Increment `planning_review_runs += 1`
- Persist findings into:
  - `planning_review_findings`
  - `planning_review_status=needs_clarification`
  - `results.planning_reviewer`
- Stop with clarification:
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
- Plan references an external API, SDK, or service whose current behavior must be verified.
- Plan proposes an architecture pattern not currently used in the codebase.
- Bug investigation suspects a dependency version regression or behavioral change.
- Two or more remediation cycles on the same issue without convergence.
- PLAN workflow where the planner needs to choose between approaches with external precedent.
- [EASY TO MISS: LLM training data may be stale. When a dependency, API, or framework version post-dates the model cutoff, treat pre-training knowledge as unreliable and require research evidence before planning or building.]

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
