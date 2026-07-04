## 9. Remediation And Workflow Rules

### Standard REM-FIX task shape

Every remediation task description must include:

```text
wf:{workflow_uuid}
kind:remfix
origin:{originating agent}
phase:{phase}
plan:{plan_file or 'N/A'}
scope:{ALL_ISSUES|CRITICAL_ONLY|N/A}
reason:{short remediation reason}
```

### Circuit breaker

Before creating a new remediation task:

- Count tasks whose descriptions contain both `wf:{workflow_uuid}` and `kind:remfix`.
- If count >= 3, ask the user how to proceed before creating another one.

**Hook-enforced backstop (MANDATORY — do not skip):** immediately after creating any `kind:remfix` task, append an entry to the workflow artifact's `remediation_history` array: `{ts, phase, reason, cycle_number}` where `cycle_number` is this workflow's running REM-FIX count (starting at 1). The `TaskCompleted` guard independently counts `remediation_history` entries from the artifact on every `kind:remfix` completion and flags/blocks when the count exceeds 3 — this is the enforced version of the LLM-counted rule above and does not depend on the router's own counting being correct. If `remediation_history` and the router's own task count ever disagree, the artifact's `remediation_history` is authoritative.

### Change-something-before-re-dispatch

When an agent returns `BLOCKED` (or a fix attempt fails), the circuit breaker only BOUNDS the loop — it does not improve it. Re-dispatching the SAME agent with the SAME model on the SAME unchanged input just burns a circuit-breaker cycle and produces the same failure. Before any re-dispatch, the router MUST change at least one input:

1. Provide missing context — supply the file/spec/decision the agent said it lacked.
2. Escalate the model tier — re-dispatch on a more capable model when the task needs more reasoning.
3. Shrink the task scope — split an oversized task into smaller, completable pieces.
4. Escalate to the human — if the plan itself is wrong, stop and ask; do not loop.

NEVER re-dispatch the same agent with the same model on the same unchanged input. If the agent said it is stuck, something must change. This complements (does not replace) the `>= 3` circuit breaker above.

### Rule matrix

| Rule | Condition | Action |
| ------ | ----------- | -------- |
| 0b | Legacy `STATUS=SELF_REMEDIATED` or blocked task state | Do not create a duplicate REM-FIX. Leave task blocked. |
| 0c | bug-investigator sets `NEEDS_EXTERNAL_RESEARCH=true` | Spawn research tasks and re-invoke investigator. No REM-FIX yet. |
| 1a-SCOPE | BUILD parallel phase has CRITICAL + HIGH issues | Ask for `critical only` vs `all issues`, store pending scope marker, stop. |
| 1a | Blocking issue in BUILD/DEBUG | Router creates scoped REM-FIX task, blocks downstream tasks, stop. |
| 1b | Non-blocking remediation needed | In BUILD/DEBUG, auto-create REM-FIX. In REVIEW, ask whether to start BUILD. |
| 2 | Reviewer verdict is Approve but failure-hunter reports HIGH issues | Ask whether to remediate or proceed. (CRITICAL hunter issues never reach this row — the contract override already converts them to blocking.) |
| 2b | Planner needs clarification | Ask the user, persist answers, then restart PLAN with a fresh visible DAG after clarification. |
| 2c | Investigator still investigating | Create follow-up investigation task with loop cap. |
| 2d | Verifier failed | Router creates REM-FIX unless user chooses REVERT at the router gate. |
| 2f | Investigator blocked | Ask: research, manual fix, or abort. |

### Scope resolution

The router is authoritative for BUILD remediation scope.

- BUILD reviewer/verifier should request `REMEDIATION_SCOPE_REQUESTED: N/A`; the router resolves `CRITICAL_ONLY` vs `ALL_ISSUES`.
- Legacy agent-created remediation tasks are still accepted during migration, but router-created remediation is canonical.
- `1a-SCOPE` applies only in BUILD when the review phase shows both:
  - at least one CRITICAL issue
  - at least one HIGH issue in the reviewer or hunter narrative
- The trigger source is explicit:
  - a reviewer summary line `High issues: [count]`
  - or a `### Findings` bullet clearly labeled `HIGH`
- When `1a-SCOPE` fires:
  1. write `[SCOPE-DECISION-PENDING: wf:{workflow_uuid} reason:{top remediation reason}]` into `activeContext.md ## Decisions`
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
  - [FALLBACK: if the host task system does not support deleting tasks, mark each `completed` with the note `pruned — unused review branch` instead. A pruned task must never leave a downstream task blocked: verify the memory task's blockers all resolve after pruning.]
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
- Mark the pre-created `re-plan` and `plan-review-gap-2` tasks as `deleted` (same fallback as above: if deletion is unsupported, mark them `completed` with the note `pruned — unused review branch`, and confirm the memory task unblocks)
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
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:debug-investigate\nplan:N/A\nscope:N/A\nreason:{ROOT_CAUSE or 'Continue investigation'}\n\nContinue investigating using the prior root-cause hints and evidence.",
  activeForm: "Continuing investigation"
})
```

### Verifier REVERT gate

If integration-verifier emits `FAIL` and the findings contain `REVERT`:

- Ask the user whether to revert or create a fix task.
- `Revert` -> record the decision in memory and stop.
- `Create fix task instead` -> continue with normal remediation creation.

### Verify-before-implement (bidirectional remediation)

A reviewer/verifier finding is an input to be checked, not an order to blindly apply. The REM-FIX agent must restate each finding and confirm it against codebase reality before changing code.

For every finding in the dispatch, the fix agent first:

1. Restates the finding in one line (what is allegedly wrong, where).
2. Reads the cited code and confirms the defect actually exists as described.
3. Only then applies the fix.

A finding the fix agent believes is wrong may take the `FINDING_DISPUTED` path instead of being applied:

- A dispute is valid ONLY if it carries a concrete `VERIFY_COMMAND` whose output PROVES the finding false (a passing test, a grep showing the alleged-missing guard already present, a type-check refuting the claim).
- A dispute with no proving command is invalid. Treat it as unverified and apply the finding.
- The dispute is adjudicated by the INDEPENDENT VERIFIER (integration-verifier), never by the reviewer who raised it. The verifier re-runs the `VERIFY_COMMAND` and rules `DISPUTE_UPHELD` or `DISPUTE_REJECTED`. On `DISPUTE_REJECTED`, the original finding stands and the fix agent must apply it.
- [EASY TO MISS: this is evidence-gated and must NOT become a rationalization escape hatch. "The fix agent decided the finding was wrong" is not a dispute. Only a reproducible command that contradicts the finding is. Prose disagreement, "looks fine to me", or "the plan said so" are never grounds to dispute — they fall through to apply.]

REM-FIX report carries, per disputed finding:

```text
FINDING_DISPUTED: {finding id or one-line restatement}
VERIFY_COMMAND: {exact command}
VERIFY_OUTPUT: {output proving the finding false}
ADJUDICATOR: integration-verifier
```

### Fix-wave consolidation

Do NOT fire one REM-FIX agent per finding. Batch ALL findings from a single review pass into ONE REM-FIX dispatch carrying the implementer contract.

- One review pass -> one REM-FIX task -> counts as ONE cycle against the circuit breaker, not N.
- Per-finding dispatch is wasteful: each agent rebuilds context and re-runs the suite, and each inflates the `kind:remfix` count toward the count >= 3 circuit-breaker gate, tripping it on a single review's worth of work.
- The single dispatch lists every finding (each subject to verify-before-implement above); the fix agent works them as a batch and runs the covering tests once at the end.
- Findings from a LATER, distinct review pass form a new wave and a new cycle. Consolidation is within one pass, never across passes.

### Plan-mandated-finding adjudication carve-out

The `skill_precedence_gate` (plan > domain skills) must NOT be misread as "auto-dismiss any reviewer finding the plan mandated". A wrong plan cannot launder defects past the gates by claiming precedence.

- Normal precedence still applies when a finding merely prefers a different approach than the plan chose.
- CARVE-OUT: when a finding DIRECTLY CONTRADICTS an explicit plan mandate (e.g. the plan mandated a test and the finding is that the test asserts nothing, or the plan mandated a guard the finding shows is unsafe), the router does NOT silently apply precedence.
- Instead the router surfaces a which-governs `AskUserQuestion` that places the finding text BESIDE the plan mandate text so the user can see the contradiction directly:
  - option A: `Plan governs` (finding is dismissed, record why)
  - option B: `Finding governs` (plan mandate is overridden, REM-FIX applies the finding)
- The reviewer must STILL report the finding regardless of plan precedence. Precedence governs what the router does with a finding, never whether the reviewer is allowed to raise it.

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

1. Re-invoke planner or investigator with:

```text
## Research Files
Web: {web_file or 'Unavailable'}
GitHub: {github_file or 'Unavailable'}
```

1. Include `cc10x:research` in `## SKILL_HINTS` only when at least one research file exists.

Do not misread a tool/fallback message as a hard blocker (the "you ARE the provider" anti-pattern):

- When an MCP accelerator (octocode, brightdata) returns a missing-capability, degraded, or fallback message, that is a signal to route around the backend — NOT a reason to abort the round to BLOCKED.
- Before treating any such message as a blocker, the researcher must first ask: is the orchestrating model ITSELF the capability being requested? Tasks like summarizing, classifying, reasoning over fetched text, or comparing approaches are things the model does directly. A backend reporting it "cannot summarize" or "has no model for this" is irrelevant — the model is the provider; do the work and continue.
- [EASY TO MISS: a backend saying "capability X unavailable" describes the BACKEND, not the workflow. Map it to the next available path (accelerated -> WebSearch/WebFetch -> the model's own analysis) per the capability model above. Never abort to BLOCKED while a built-in fallback path still exists.]
- Only escalate to BLOCKED when EVERY path is genuinely exhausted: the accelerator failed, the built-in tools failed or are unavailable, AND the model cannot supply the capability itself. Record the exhausted paths in `research_backend_history` so the next round does not re-discover the same fallback.

## 11. Re-Review Loop

When a `kind:remfix` task completes:

1. Count completed remediation tasks in the same `wf:`. If count >= 2, run the cycle-cap gate before continuing.
2. Create a re-review task:

```text
TaskCreate({
  subject: "CC10X code-reviewer: Re-review after REM-FIX",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:re-review\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-review the changes made by the completed remediation task.\nIf scope=ALL_ISSUES: perform a FULL re-audit of CRITICAL and HIGH issue categories after remediation.\nIf scope=CRITICAL_ONLY: verify the CRITICAL issue was resolved and treat HIGH issues as deferred unless newly escalated.",
  activeForm: "Re-reviewing fix"
}) -> rereview_task_id
```

1. Create a re-hunt task (BUILD only — the hunter re-scans for silent failures after remediation):

```text
TaskCreate({
  subject: "CC10X failure-hunter: Re-hunt after REM-FIX",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:re-hunt\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-scan for silent failures after remediation. Focus on the remediated surface and its immediate call sites.",
  activeForm: "Re-hunting failures"
}) -> rehunt_task_id
```

1. Reuse the pending verifier in the same `wf:` if one exists; otherwise create:

```text
TaskCreate({
  subject: "CC10X integration-verifier: Re-verify after REM-FIX",
  description: "wf:{workflow_uuid}\nkind:reverify\norigin:router\nphase:re-verify\nplan:{plan_file or 'N/A'}\nscope:{scope from completed remfix}\nreason:{reason from completed remfix}\n\nRe-verify after remediation.",
  activeForm: "Re-verifying fix"
}) -> reverify_task_id
```

1. Block the verifier on both the re-review and re-hunt tasks.
2. Re-block the memory task on the verifier for BUILD/DEBUG or on the re-reviewer for REVIEW.
3. Increment telemetry loop counters whenever the follow-up tasks are created:
   - `telemetry.loop_counts.re_review += 1`
   - `telemetry.loop_counts.re_hunt += 1` (BUILD only)
   - `telemetry.loop_counts.re_verify += 1`

### Re-review precondition gate

The reviewer/verifier is NEVER re-dispatched on an unverified fix. Before step 2 above creates any re-review/re-verify task, the completed REM-FIX report MUST contain proof the fix was exercised:

```text
COVERING_TESTS: {test file names that cover the fixed behavior}
TEST_COMMAND: {exact command run}
TEST_OUTPUT: {its output}
```

- Name only the COVERING tests — the files that exercise the changed behavior — not the whole suite. "Ran all tests, green" is not sufficient; the report must point at the tests that would fail if this fix were wrong.
- If `COVERING_TESTS`, `TEST_COMMAND`, and `TEST_OUTPUT` are missing or empty, the gate fails closed: do NOT create the re-review task. Send the REM-FIX back (or block the task) until the proof is supplied.
- A `FINDING_DISPUTED` entry satisfies this gate for that finding via its `VERIFY_COMMAND`/`VERIFY_OUTPUT` pair (adjudicated by integration-verifier per Section 9), since the dispute itself carries the proving evidence.
- This precondition is independent of the cycle-cap gate in step 1; both must pass before re-dispatch.
