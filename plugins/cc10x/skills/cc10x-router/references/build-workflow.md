### BUILD preparation

0. **Workspace isolation offer (optional, runs once per workflow, before any builder dispatch).**
   - Skip entirely when `build_scope=trivial` (resolved in step 4) or when already inside a linked worktree. Record `worktree=existing` and continue.
   - If a native worktree primitive is available (a tool named `EnterWorktree`, a `/worktree` command, or a `--worktree` flag), prefer it. In `JUST_GO` mode invoke it on the recommended default; otherwise offer one `AskUserQuestion`: `Isolate in a worktree (Recommended)` or `Work in current branch`. On accept, defer to the native primitive (it owns directory placement, branch creation, and cleanup) and record `worktree=native`.
   - If NO native primitive exists, do NOT shell out to `git worktree add`. Skip silently and record `worktree=in_place`. cc10x never hard-requires git worktrees.
   - Persist the chosen `worktree` mode in the workflow artifact; this drives the finishing step's cleanup ownership.
0a. **Git pre-flight (READ-ONLY, runs once after entering the workspace, before any builder dispatch).**
   - This is a read-only orientation pass — issue no git mutations here. Record results in the workflow artifact under `results.git_preflight`; the BUILD-DONE finishing menu reuses them.
   - Compare `git rev-parse --git-dir` against `git rev-parse --git-common-dir`. If they DIFFER, this tree is already an isolated linked worktree → record `isolated=true` and skip the step-0 isolation offer (do not re-offer). If they are equal but `git rev-parse --show-superproject-working-tree` returns a path, this is a submodule, not a worktree → record `isolated=submodule` and treat as in-place.
   - Read `git branch --show-current`. If it is EMPTY, the workspace is in detached HEAD → record `detached_head=true`. This flows to the finishing menu's reduced form (drop local-merge; note "branch needed before PR").
   - If any git command fails or is blocked by the sandbox, do not error out. Record `git_preflight=degraded` and continue; downstream gates that depend on git degrade gracefully and still OUTPUT suggested branch/commit/PR text instead of executing it.
0b. **Dependency install on a fresh workspace (runs once, before the rank-`0c` baseline run and before the first builder dispatch).**
   - Only when step 0 produced an isolated workspace (`worktree=native` or `isolated=true`) whose dependencies are NOT yet installed. Skip silently for in-place work where deps already exist.
   - Detect the stack from a manifest at the workspace root: `package.json` (node), `Cargo.toml` (rust), `requirements.txt` / `pyproject.toml` (python), `go.mod` (go). If NO manifest is present, skip silently and record `deps=no_manifest`.
   - Run the matching install using the project's EXISTING runner — do not invent one. Prefer the lockfile-implied tool (`pnpm install` / `yarn install` / `npm ci` per the present lockfile; `cargo fetch`; `pip install -r requirements.txt` or the project's `pyproject` runner; `go mod download`). Record `deps=installed` (or `deps=install_failed` with the error) in the workflow artifact.
   - Rationale: a tree with no installed deps makes the first TDD RED fail for a spurious reason (missing `node_modules`), burning a builder strike on noise rather than the change.
0c. **Clean-baseline snapshot (runs once, AFTER dependency install, before the first builder dispatch).**
   - Run the project's existing test suite ONCE against the untouched workspace and record the baseline into the workflow artifact under `results.baseline`: total test count `N`, and the explicit set of tests ALREADY failing (`baseline_failures`, captured by test id/name, not just a count).
   - If the suite cannot run (no test command, or `git_preflight=degraded` blocks it), record `baseline=unavailable` with the reason and continue; downstream verification then falls back to treating ANY failure as suspect and says so explicitly.
   - This baseline is the anchor against the false-attribution family: without it the verifier cannot separate a NEW failure from a PRE-EXISTING one. The `phase_exit_gate` / `integration-verifier` DIFFS post-build results against `baseline_failures` so that ONLY newly-introduced failures block the phase exit; baseline-failing tests that remain failing do not block (but are surfaced, not hidden).
1. Read `- Plan:` from `activeContext.md ## References`.
2. If plan path is not `N/A`, `Read(...)` the plan file before creating tasks.
3. Run `plan_trust_gate` before BUILD:
   - `Open Decisions` must be empty or explicitly marked approved.
   - `Differences from agreement` must be present, even if empty.
   - `plan_mode` must be explicit when a plan artifact exists.
   - `verification_rigor` must be explicit when a plan artifact exists.
   - If `plan_mode` is `execution_plan` or `decision_rfc`: every phase in `normalized_phases` must carry non-empty `exit_criteria`, and `intent.acceptance_criteria` must be non-empty. Field presence is not enough — field completeness is required.
   - Cross-check `intent.constraints` against approved decisions. If any approved decision explicitly contradicts an `intent.constraint`, emit NOGO with the contradiction and ask the user to resolve before BUILD starts.
   - If any condition fails, ask for clarification and do not start BUILD.
4. If plan path is `N/A`, assess scope before dispatch and record `build_scope`:
   - **Trivial** (single concern, one file group, one failure mode) → set `build_scope=trivial` and continue directly to BUILD.
     Heuristic signals: touches 1-2 files, single logical change, one testable outcome, no cross-module wiring.
     [EASY TO MISS: When the task is clearly trivial, do not ask clarifying questions or suggest planning. Execute directly. Analysis paralysis on trivial work is a net negative.]
   - **Non-trivial** (spans multiple independent file groups, has separable concerns, or involves distinct failure modes) → set `build_scope=standard` and ask: `Plan first (Recommended)` or `Build directly`.
     Heuristic signals: touches 3+ files across different directories, multiple independent concerns that could fail separately, changes to both interface and implementation, or new cross-module dependencies.
   - `Plan first` -> switch to PLAN workflow.
   - `Build directly` -> continue without a plan.
   - When a plan artifact exists (plan path is not `N/A`), `build_scope=standard` always. Planned work never takes the trivial graph.
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
13. Router handoff for the current BUILD phase must be phase-local:
   - include only the current phase objective, inputs, expected artifacts, required checks, checkpoint type, exit criteria, and approved clarifications still in force
   - include prior-phase detail only when it remains an active blocker, dependency, or unresolved finding
   - do not rehydrate broad historical narrative when the workflow artifact already captures it

### BUILD task graph

BUILD is sequential:
- one approved executable phase at a time
- one builder run for the current phase only
- review, hunt, and verify validate that phase before `phase_cursor` advances
- if phase exit evidence is incomplete, record `partial` or `blocked`, persist state, and stop

**Complexity gradient (read `build_scope` from BUILD preparation step 4):**
The router is still the sole entry point for every BUILD, but the task graph scales to the work. This is a deliberate gradient, not the retired unconditional QUICK path: trivial work earns a reduced graph; everything else pays the full chain.

- `build_scope=trivial` → use the **reduced task graph** below: `component-builder` → `integration-verifier` → `Memory Update`. NO separate `code-reviewer` task, NO `silent-failure-hunter` task, NO standalone `doc-syncer` task. The verifier still runs its real proof path (never weaken `verifier-latency-model.md` must_keep_core) and folds a brief review/edge-case pass into its report.
- `build_scope=standard` (default, and always when a plan exists) → use the **full task graph** further below.

**Escalation rule (trivial → full):** after the builder returns, if its Router Contract reports non-empty `SCOPE_INCREASES` or non-empty `BLOCKED_ITEMS`, the work was not actually trivial. Before advancing, promote the workflow to the full graph: create the `code-reviewer` and `silent-failure-hunter` tasks (blocked by the builder) and the `doc-syncer` task (blocked by the verifier), and re-block Memory Update on `doc_sync_task_id`. Persist `build_scope=standard` and an escalation entry in `status_history`.

#### Reduced task graph (`build_scope=trivial`)

```text
TaskCreate({
  subject: "CC10X component-builder: Execute phase {phase_id}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-implement\nplan:N/A\nscope:N/A\nreason:Execute trivial change\n\nExecute the trivial change. Recover objective, inputs, expected artifacts, required checks, and exit criteria. Stop if blocked, partial, or scope grows beyond trivial (report SCOPE_INCREASES so the router can escalate to the full review/hunt chain).",
  activeForm: "Building components"
}) -> builder_task_id

TaskCreate({
  subject: "CC10X integration-verifier: Verify integration",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-verify\nplan:N/A\nscope:N/A\nreason:Trivial-path phase exit verification\n\nRun required checks for the change and report whether truths, artifacts, wiring, and exit criteria are satisfied. Fold a brief correctness/edge-case review into your report since no separate reviewer/hunter ran.",
  activeForm: "Verifying integration"
}) -> verifier_task_id
TaskUpdate({ taskId: verifier_task_id, addBlockedBy: [builder_task_id] })

TaskCreate({
  subject: "CC10X Memory Update: Persist workflow learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .cc10x/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Persisting workflow learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [verifier_task_id] })
```

If the builder triggers the escalation rule, convert this into the full graph before running the verifier: add reviewer + hunter (blocked by builder), add doc-syncer (blocked by verifier), re-block verifier on `[reviewer_task_id, hunter_task_id]`, and re-block Memory Update on `doc_sync_task_id`.

#### Full task graph (`build_scope=standard`)

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

**Opt-out check:** Before creating the doc-sync task, read `activeContext.md ## Session Settings`. If `DIFF_DRIVEN_DOCS: skip` is present, skip doc-sync task creation entirely and update Memory Update to block on `verifier_task_id` directly instead of `doc_sync_task_id`. Skip the remaining doc-sync task graph below.

TaskCreate({
  subject: "CC10X doc-syncer: Sync documentation",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:build-doc-sync\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Sync docs to reflect diff\n\nAnalyze the diff from this BUILD phase. Classify doc impact. Update documentation across business, technical, and audit layers as applicable. Emit SKIPPED contract immediately if IMPACT_LEVEL=none.",
  activeForm: "Syncing documentation"
}) -> doc_sync_task_id
TaskUpdate({ taskId: doc_sync_task_id, addBlockedBy: [verifier_task_id] })

TaskCreate({
  subject: "CC10X Memory Update: Persist workflow learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:{plan_file or 'N/A'}\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .cc10x/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Persisting workflow learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [doc_sync_task_id] })
```

### Deferred Minor findings roll-up

Minor findings that do not block a phase exit must not silently evaporate — that violates the "no finding silently discarded" rule. The workflow artifact carries a `deferred_findings` array for exactly this:
- When `code-reviewer` or `silent-failure-hunter` raise a Minor finding that does NOT block the current `phase_exit_gate`, the router appends it to `deferred_findings` (each entry: `source` agent, `phase_id`, terse `finding`, and `severity:minor`) rather than dropping it. Blocking findings still gate the phase as before — this array is only for the non-blocking remainder.
- The array accumulates across phases for the whole workflow. Nothing consumes it mid-flight; it is surfaced once at BUILD-DONE (see the finishing block's triage step) so the user can decide explicitly: fix now, file as follow-up, or knowingly accept. No automatic action is taken on a deferred finding.
- In the reduced task graph (`build_scope=trivial`) there is no separate reviewer/hunter, so the verifier's folded review/edge-case pass appends any Minor leftovers to `deferred_findings` the same way.

### doc-syncer SKIPPED state

If doc-syncer returns `STATUS: SKIPPED` (i.e., `IMPACT_LEVEL: none`), the router treats it as a passing state — equivalent to `COMPLETE` for workflow-advance purposes. The router must not block Memory Update when the SKIPPED contract is present and `SKIP_REASON` is non-empty. Advance to Memory Update immediately.

### BUILD-DONE finishing (optional)

Finishing is a router-owned, optional step that runs AFTER the final phase's `integration-verifier` returns `PASS` and Memory Update is otherwise ready — it does NOT add a child agent task or a contract-enforced phase. It is a single inline router gate, tagged `phase:build-finish` only if the router chooses to log it in the event stream. It exists to close the end-to-end gap vs. superpowers `finishing-a-development-branch` without forking that skill.

**When it runs:**
- Only when `build_scope=standard` AND the workflow actually produced committable changes. Skip for `build_scope=trivial` and skip when no files changed.
- Only after the final phase verified `PASS`. Never offer finishing while any phase is `partial`, `blocked`, or has unresolved remediation — finishing presupposes green.
- At most once per workflow, immediately before Memory Update. Finishing never blocks Memory Update: if the user defers, persist the choice and let Memory Update proceed.

**How it runs (gated, never auto-destructive):**
1. Confirm verification is green from the workflow artifact (`proof_status=passed`, final phase `completed`). Do not re-derive from prose.
1a. **Surface deferred Minor findings before the menu.** Read `deferred_findings` from the workflow artifact. If non-empty, present the accumulated list (source, phase, finding) for explicit triage BEFORE offering the finishing menu, so nothing rolls off silently. Let the user fix now, file as follow-up, or knowingly accept; record the disposition in the artifact. An empty array is fine — just note "no deferred findings" and continue. This is surfacing-and-triage only; the router takes no automatic action on these findings.
2. Detect environment: normal repo vs. linked worktree vs. detached HEAD. Reuse the `worktree` mode recorded in BUILD preparation step 0 AND the read-only `results.git_preflight` recorded in step 0a (`isolated`, `detached_head`, degraded). Re-run a single read-only pre-flight here only if step 0a was skipped. This selects the menu and the cleanup owner. If `git_preflight=degraded` (sandbox blocks git), degrade gracefully: skip every git mutation and instead OUTPUT the suggested branch name, commit message, and PR title/body text for the user to run manually.
3. Offer exactly one `AskUserQuestion` with safe-by-default options:
   - `Keep the branch as-is (Recommended)` — default; no git mutation.
   - `Merge to base branch locally`
   - `Push and open a Pull Request`
   - `Discard this work`
   On detached HEAD (`detached_head=true`), use the REDUCED menu: drop `Merge to base branch locally` entirely (there is no current branch to merge), offer `Push as new branch + PR` instead, and note "branch needed before PR" so the user creates a branch first.
4. Execute ONLY the chosen option. Hard constraints:
   - `Keep as-is`: no git command. Report the branch/worktree path. (This is the `JUST_GO` auto-default.)
   - `Merge`: follow the **merge-then-cleanup ordering invariant** below — verify on the merged result before any teardown. Never delete a branch before its worktree is removed, and never remove/delete before merge+tests confirm.
   - `PR`: push + open PR; preserve the worktree (the user still needs it). Never force-push.
   - `Discard`: require a typed `discard` confirmation before any `git branch -D` or worktree removal. JUST_GO must NOT auto-select discard.
   - Worktree cleanup: only for `Merge`/`Discard`, and only when cc10x created the worktree (see the **worktree cleanup provenance** rule below). If `worktree=native`, defer cleanup to the native primitive (`ExitWorktree`); if `worktree=existing` or harness-owned, leave it in place — never remove a workspace cc10x did not create. If `worktree=in_place`, there is nothing to clean up.
5. Persist the finishing decision into the workflow artifact (`results.finishing.choice`) and append a `build_finished` event to the event log. Then advance to Memory Update.

**Merge-then-cleanup ordering invariant (`Merge to base branch locally`):**
Execute these steps STRICTLY in order; do not reorder, and do not start teardown until the post-merge gate is green. A branch that was clean before merge can break after merging onto a moved base — that is exactly what the post-merge re-run catches.
1. `git checkout <base>` (the branch the work targets).
2. `git pull` to bring the base up to date.
3. `git merge <work-branch>` (no force).
4. **Post-merge verification gate:** RE-RUN the project's test suite ON THE MERGED RESULT. Diff against `results.baseline` (BUILD preparation step 0c) so only NEWLY-introduced failures count. If the merge introduces any new failure → STOP. Do NOT remove the worktree, do NOT delete the branch. Report the breakage and leave everything in place for the user to resolve.
5. ONLY on a green post-merge run: tear down the worktree per the provenance rule (native `ExitWorktree` when `worktree=native`) — REMOVE THE WORKTREE FIRST.
6. THEN delete the now-merged branch. Never delete the branch before its worktree is removed; never remove/delete anything before steps 4 confirms green.

**Worktree cleanup provenance:** cc10x defers worktree CREATE to the native `EnterWorktree` primitive; teardown is symmetric. NEVER shell out to `git worktree remove`. Tear down ONLY worktrees cc10x itself created (`worktree=native`), and route ALL teardown through the native exit tool (`ExitWorktree`). Leave harness-owned or pre-existing workspaces (`worktree=existing`, `isolated=true` from step 0a but not created by cc10x) to the harness's own exit tool — removing a harness-created worktree leaves phantom state the harness can no longer see or reconcile.

**JUST_GO interaction:** the finishing gate auto-defaults to `Keep the branch as-is` and logs the choice in `## Decisions`. JUST_GO never auto-merges, auto-pushes, or auto-discards — those touch durable git state and the failure-stop / non-destructive rules outrank JUST_GO.
