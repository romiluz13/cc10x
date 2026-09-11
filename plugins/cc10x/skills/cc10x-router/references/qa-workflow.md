### QA preparation

**Status: DRAFT.** Sections marked `PLACEHOLDER` are agreed in shape but not yet specified. See `docs/plans/2026-08-10-qa-route-rfc.md` for the governing design and open decisions.

**Target repo (`CC10X_REPO_DIR`).** Same rule as BUILD: when set, every git command, dependency install, service start, and test run in this workflow operates on that absolute path; `.cc10x/` state stays at the session cwd. Record the resolved target under `results.target_repo`.

0. **Workspace isolation offer.** Same policy as BUILD step 0 — prefer a native worktree primitive when one exists, skip silently when none does, never shell out to `git worktree add`. QA builds real files (harness scripts, tests), so isolation is warranted for `qa_scope=standard`. Skip for `qa_scope=probe`.

0a. **Capability discovery (READ-ONLY, runs once, before any QA agent dispatch).**

- This is a read-only orientation pass. Record results under `results.qa_env_preflight`; the env-plan step consumes them.
- **Inventory the session's own tooling FIRST.** Before deciding anything is unavailable, enumerate what this session actually has — MCP servers, skills, plugins, and agents — and plan to use it. Ticket/spec access, log access, and UI driving frequently come from tooling rather than from the repo. Discover this at runtime; never hardcode a list, because it differs per user and grows over time.
- **Nothing is "unavailable" until a check that could have found it came back empty.** This applies to every kind of thing this step records — a tool, an MCP server, a repo, a path, a credential file. **Never ask the user whether something exists on their machine.** "Do you have that repo cloned?" is the router outsourcing a measurement it can take in one command, and the answer it gets back is a *belief* where `ls` would have produced a *fact*. Measure first, then ask what to do about what you measured. This is the same discipline the setup record enforces on preflight — record only what was observed — applied one phase earlier, where the cost of guessing is an entire lane.
- Then detect what the machine can do, and record each as available / unavailable:
  - container runtime — `docker info`, `podman info`
  - orchestration — presence of `docker-compose.yml`, `compose.yaml`, `Tiltfile`, `skaffold.yaml`, `kind`/`k3d`
  - test-harness libs — `testcontainers` in the dependency manifest
  - UI automation — Playwright installed; `ox-playwright` skill present; `claude-in-chrome` tools present
  - cloud ephemeral — project-declared ephemeral-env tooling
  - log access — local stdout vs. a log platform (`ox-datadog-toolset`)
- If NOTHING is available, do not fail. Record `qa_env=none_detected` and route the env-plan to `manual_instructions` mode: the plan documents the environment a human must provide, and the workflow stops at a `human_action` checkpoint rather than pretending it can provision.
- If any probe command is blocked by the sandbox, record `qa_env_preflight=degraded` and continue.

0b. **Repo-set enumeration (READ-ONLY, runs once, BEFORE the research fan-out is dispatched).**

Enumerate every repository the feature's traced path touches — *including* the ones this workflow does not intend to test — and measure whether each is present on this machine. Record the set under `results.qa_repo_set`, one entry per candidate carrying `present: true|false` and, when present, the resolved absolute path.

- Derive the candidate set from the request, the target repo's outbound calls and clients, its dependency manifest, and any design docs already discovered — **not** from what the user named. A repo nobody mentioned is exactly the one this step exists to surface.
- **Measure each candidate.** A repo is absent only after a check that could have found it came back empty.
- **PRESENT the set on screen** — every candidate, its measured presence, its path — and get explicit confirmation of which repos are in scope for the `code` lane split.
- Dispatch the research fan-out only after that confirmation.
- **Re-measure and re-present if step 2 surfaces a repo this set does not contain.** Step 2 asks the user which ticket or spec the effort belongs to, and the ticket is the artifact that most often names an adjacent service nothing in the code points at. A set confirmed at 0b and never revisited would exclude exactly that repo — silently, which is the failure this step exists to prevent. Fold the re-presentation into step 2's own on-screen confirmation rather than raising a second gate.

**This gate cannot be deferred to the environment topology gate.** That gate lives in `qa-plan`, which runs *after* the fan-out has already returned. An offer made there arrives with every lane already spent and can be honoured only by re-running research from the start. A repo excluded before this step is excluded from the feature map, the test plan, and the harness — silently, and for the rest of the workflow.

1. **Resolve QA scope** and record `qa_scope`:
   - **`probe`** (single service, single feature, integration tier only, environment already runnable) → reduced task graph.
     Heuristic signals: one service, no cross-service hop, no UI tier, an existing test command already works.
   - **`standard`** (default; always when the request spans services, includes a UI tier, or requires provisioning) → full task graph.
   - Escalation `probe` → `standard` is mandatory when the harness builder reports non-empty `SCOPE_INCREASES` in **either** mode, or non-empty `BLOCKED_ITEMS` in **`MODE: harness`** (mirrors BUILD's trivial→full escalation). A **preflight** `BLOCKED_ITEMS` does NOT escalate — see the reduced-graph section.

2. **Resolve available input sources** for the research step and record `qa_sources`. For each of the four, mark `available` / `unavailable`:
   - `code` — always available
   - `spec_docs` — repo docs, `DESIGN.md`, `docs/**`, Confluence via `ox-atlassian-toolset`
   - `tickets` — Jira via `ox-atlassian-toolset`, MRs via `ox-gitlab-toolset`
   - `cc10x_artifacts` — `- Plan:` / `- Design:` in `activeContext.md ## References`, and `.cc10x/workflows/*.json`
   - **Source identification order is FIXED — ask, detect, show, confirm:**
     1. **ASK the user** which ticket / spec / epic this effort belongs to. One question beats an hour of wrong inference.
     2. **If they do not know or do not say, apply heuristics** — branch name, recent commit subjects, `activeContext.md ## Current Focus`, open MRs touching the feature's files.
     3. **PRESENT what was found ON SCREEN** — in the conversation, not only written to a file — and get explicit confirmation before any researcher is dispatched.
     4. Only then mark sources `available` and proceed.
   - Rationale: a test plan built from the wrong ticket tests the wrong system, and the failure is **silent** — everything passes, against the wrong spec. That is worth one round-trip.

2a. **Persist `qa.isolation` into the workflow artifact NOW — before any researcher is dispatched.**
   - `denied_reads`: absolute paths and globs no agent may read. Ask the user if the workflow implies quarantined material (a comparison baseline, out-of-scope repos, material that would bias the result).
   - `plan_phase_readonly`: `true` unless the user explicitly waives it.
   - `mutation_allowlist`: `[".cc10x/"]` by default.
   - The PreToolUse guard reads this artifact. A denylist that exists only in a prompt is unenforced.

3. **Immediately write `[QA-START: wf:{workflow_uuid}]`** into `activeContext.md ## Recent Changes` once the workflow id exists.

4. **Create the QA artifact directory:** `Bash("mkdir -p .cc10x/qa/{workflow_uuid}")`. All QA artifacts (`feature-map.md`, `test-plan.md`, `env-plan.md`, `report.md`) live there.

5. **Intent Readiness Gate** applies unchanged (SKILL.md §5). For QA, "sufficiently specific" means: the feature or flow under test is named concretely enough that a scenario matrix can be written against it. "test my app" is not sufficiently specific — ask what flow.

6. Initialize workflow `proof_status` to `gaps_found`. QA never starts optimistic.

---

### QA task graph

QA is sequential with one fan-out (research) and one parallel pair (review ‖ hunt):

```
qa-researcher × N (parallel)
  → router-owned consolidation into feature-map.md
  → qa-plan (test-plan.md + env-plan.md)
  → plan-gap-reviewer (fresh, anti-anchoring)
  → qa-preflight (qa-harness-builder in preflight mode — measures, never boots)
  → qa-harness-builder
  → [code-reviewer ‖ failure-hunter]
  → qa-executor
  → Memory Update
```

#### Research fan-out (`phase:qa-research`)

**Fan-out is the DEFAULT here.** This inverts DEBUG's default-to-single rule, and the inversion is justified against the same INDEPENDENCE TEST in `debug-workflow.md`:

1. **Separable understanding** — PASS. Reading the Jira ticket does not require having read the code; each source is comprehensible alone.
2. **Disjoint files** — PASS trivially. All four researchers are READ-ONLY. There is no write surface to collide on.

Create one task per source marked `available` in `qa_sources`:

```text
TaskCreate({
  subject: "CC10X qa-researcher: Scan {source}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-research\nplan:N/A\nscope:{source}\nreason:Build feature understanding from {source}\n\nScan ONLY the {source} surface. Report what this source says the feature does, from both the user's side and the system's side. Report gaps and anything this source contradicts. Do not read the other sources.",
  activeForm: "Scanning {source}"
}) -> researcher_task_id_{source}
```

**Scope isolation is deliberate:** each researcher reads ONE source and is blind to the others. A researcher that reads both the ticket and the code will silently reconcile them in its head, and the contradiction — the highest-value output of this step — disappears. Blindness is the feature.

**Splitting the `code` lane per repo (multi-repo features).** When the feature spans several services, dispatch one `code` researcher **per repository** rather than one for all of them, over the repo set enumerated, shown and confirmed at step 0b. Cross-repo contract mismatches — a field one service sends and another never reads, two ends of a wire that disagree about a shape — are the signature defect class of a multi-service feature, and they are exactly what vanishes when a single agent reconciles all the repos in its own head. The same blindness argument that justifies the source fan-out justifies this sub-fan-out. The lane's `scope:` becomes `code:{repo}`, and the router consolidates them like any other lanes.

**Declaring the other side out of scope does not make it testable by stub.** A harness that stubs an adjacent service is built from the traced repo's own belief about the wire — the field names it sends, the shape it expects back. A stub authored from one side's belief cannot disagree with that side, so the scenario it serves goes green whether or not the real service reads the field at all. That is a self-confirming test: it proves the caller is internally consistent and says nothing whatever about the contract. When an adjacent repo is present and its wire is in the traced path, it gets a lane. When it is genuinely absent, the harness may still stub it — but every scenario that depends on that stub carries a **`unproven by stub`** row in the test plan's §7 known-gaps table, whose `What a PASS does NOT prove` column states plainly that a green run here is consistent with the real service never having read the field. **The scenario stays in the §4 wave count and in the §2 id rollups** — dropping it would break the reconciliation those sections require — but it is excluded from the coverage `Cases` column, and the difference is carried in *Uncovered — and why that is acceptable*. A gap that is silently deducted from a total is indistinguishable from an arithmetic error; a gap with a row is a finding.

**Anti-anchoring for the fan-out.** If `## Project Patterns` (or any memory section) is itself one of the sources a lane is assigned to read — `cc10x_artifacts` most often is — omit it from the *other* lanes' scaffolds. Injecting it everywhere leaks one lane into all of them and destroys the independence the fan-out exists to create. This is the same rule §7 applies to adversarial dispatches, applied for the same reason.

**Router-owned consolidation (inline, no agent).** After all researchers return, the router merges into `.cc10x/qa/{workflow_uuid}/feature-map.md`, using `templates/qa-feature-map.template.md`. Contradictions between sources are recorded, never resolved by the router — resolving them is a user decision or a QA finding.

Consolidation stays inline deliberately. The router is the only thing that has seen every lane, it raises gates (contradictions, incidents) that only a user can answer, and it needs the resulting understanding for every decision after this point. Dispatching it to an agent relocates the same context and then forces the router to re-read the result.

**The `Changes what we test?` column is the filter, not decoration.** A contradiction with no test-design consequence is documentation debt and belongs in §8, not §3. Most contradictions are that. Keeping them all in §3 buries the two or three that decide whether the run measures anything — and it is those that must be marked `blocking` and settled, by a probe or by the user, before the plan is trusted.

**§8 must leave the workflow.** Live defects, stale artifacts, and product-level disagreements found during consolidation are real findings that outlive this test effort. Surface them to the user with the feature map; offer DEBUG for defects per §4 rather than letting them die inside a QA artifact nobody re-opens.

If consolidation surfaces a contradiction that changes what should be tested, halt on `pending_gate="qa_source_contradiction"` and ask the user which source is authoritative. Do not plan against an unresolved contradiction.

#### Plan (`phase:qa-plan`)

Dispatches the existing `cc10x:planner` with `cc10x:qa-strategy` in `SKILL_HINTS` (RFC §6c — decided). Fork `qa-planner` later only if the planner repeatedly emits build phases with tests bolted on instead of a scenario matrix.

**Templates are mandatory — copy, do not improvise:**

```text
Bash(command="mkdir -p .cc10x/qa/{workflow_uuid} && cp \"${CLAUDE_PLUGIN_ROOT}/templates/qa-test-plan.template.md\" .cc10x/qa/{workflow_uuid}/test-plan.md && cp \"${CLAUDE_PLUGIN_ROOT}/templates/qa-env-plan.template.md\" .cc10x/qa/{workflow_uuid}/env-plan.md")
```

Then fill them in place. A section that does not apply is marked `N/A` with a reason — **never deleted**. The mandatory sections (test plan §2 coverage table, §6 known gaps; env plan §9 teardown verification, §10 re-runnability) exist because they are exactly what a plan omits when it is optimistic, and an omitted section is invisible while an `N/A` is arguable.

**Environment topology gate — ask, detect, SHOW, confirm.** Before the plan agent writes `env-plan.md`:

1. ASK the user how this system is meant to run for testing.
2. Detect from the machine and from discovered tooling (step 0a).
3. **PRESENT the proposed topology on screen** and get explicit confirmation.
4. Write `env-plan.md` only after confirmation.

A plan written to a file the user never looked at is not an approved plan. The environment is the most expensive thing here to get wrong — a bad topology produces failures that look like product bugs, which is how a team learns to distrust its own suite.

```text
TaskCreate({
  subject: "CC10X qa-plan: Design test plan and environment for {feature}",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-plan\nplan:N/A\nscope:N/A\nreason:Design test scenarios and test environment\n\nRead the feature map at .cc10x/qa/{workflow_uuid}/feature-map.md and the capability discovery results from the workflow artifact. Produce TWO artifacts: (1) .cc10x/qa/{workflow_uuid}/test-plan.md — a scenario matrix covering happy path, error handling, and edge cases, where every scenario names its observation points across UI, API, DB, queue, and logs, and where every group of controls states which reduction technique was applied (every-option-once, pairwise, boundary values, full combinatorial) and what it leaves uncovered; (2) .cc10x/qa/{workflow_uuid}/env-plan.md — how the test environment is built, wired, seeded, gated on readiness, and torn down. Cover the User Action Inventory from the feature map: reduce it deliberately, never silently. Order the scenarios into WAVES with objectives, dependencies and a stop-if condition — a flat scenario list is not a buildable plan, and every other cc10x plan carries ordered phases. Wave 1 is the thinnest slice that proves the pipeline is wired, including any probe that binds a variable later waves consume. Reconcile every rollup: the scenario ids across coverage-by-class, coverage-by-tier and the waves must all equal the total scenario count, and the total must be stated with its arithmetic shown. Both artifacts must be executable by an agent that has not read this conversation.",
  activeForm: "Designing test plan"
}) -> qa_plan_task_id
```

#### Plan review (`phase:qa-plan-review`)

Reuses the existing `cc10x:plan-gap-reviewer` unchanged. Fresh-context, anti-anchoring, read-only — same role it plays in PLAN.

```text
TaskCreate({
  subject: "CC10X plan-gap-reviewer: Fresh review of test plan",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-plan-review\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Anti-anchoring coverage review of saved test plan\n\nReview the saved test plan and environment plan against the original user request and the feature map. Judge COVERAGE: are error paths represented, not just happy paths? Are edge cases concrete rather than gestured at? Could every assertion actually fail, or are some unfalsifiable? Does every group of controls in the User Action Inventory get reduced by a NAMED technique that states what it leaves uncovered — or is coverage silently dropped? Is the environment plan executable, or does it hand-wave provisioning? Check the feature map's contradiction table against the plan: does every row marked `blocking` get settled — by a probe scenario, a bound variable, or a recorded user decision — before anything that depends on it runs? Does every `deferred` row name the scenario it shaped, and does that scenario exist? A contradiction recorded and then quietly planned around is the failure mode here: the plan reads as confident and rests on a coin flip. Then reconcile the plan against itself: do the scenario ids in every rollup — by class, by tier, by wave — add up to the stated total, and does each claimed case count name the scenario rows that deliver it? A rollup that drops a scenario disproportionately drops the odd one out, which is usually the blocking probe or the one deliberate expected-failure.",
  activeForm: "Fresh-reviewing test plan"
}) -> qa_plan_review_task_id
TaskUpdate({ taskId: qa_plan_review_task_id, addBlockedBy: [qa_plan_task_id] })
```

**Coverage lens via `SKILL_HINTS`, not a new rubric (RFC §6d).** `plan-gap-reviewer` natively asks "is this plan buildable?"; a QA plan needs "is this plan thorough?". Inject `cc10x:qa-strategy` on this dispatch and let the discipline supply the lens. Only add a rubric section to the agent file if the hint proves too weak — keeping the reviewer domain-agnostic is what makes it reusable across PLAN and QA.

**One pass by default; a second whenever pass 1 finds blocking issues.** PLAN pre-creates a bounded `plan-create -> plan-review-gap-1 -> re-plan -> plan-review-gap-2` DAG and keeps the second half alive only when pass 1 returns findings. QA follows the same shape, for the same reason.

- **Pass 1 returns `PASS`** -> prune `qa-re-plan` and `qa-plan-review-2` explicitly (mark `deleted`; if the host task system cannot delete, mark `completed` with the note `pruned — unused review branch`). Verify no downstream task is left blocked by a pruned one.
- **Pass 1 returns `FINDINGS`** -> keep both alive. The amendment runs as `qa-re-plan`; `qa-plan-review-2` reviews the amended artifacts in fresh context. **Maximum fresh-review passes: 2.**

**An amendment is never self-certified — the same fail-closed rule BUILD applies to a REM-FIX.** BUILD refuses to re-dispatch a reviewer on an unverified fix: the REM-FIX report must first carry proof the fix was exercised. QA's proof is a *sweep* rather than a test run, because a QA amendment is a text change spread across three coupled artifacts instead of a code change in one place. Before `qa-plan-review-2` is dispatched, the `qa-re-plan` report MUST carry all three of:

- `AMENDED_FILES:` every artifact touched, with the revision marker (`r2`, `r3`, …) written into each one's header. **All three plan artifacts are in scope on every amendment.** An amendment naming only `test-plan.md` has not been swept: the feature map's handoff section and the env plan's blocker, prerequisite and degradation tables restate the same facts in their own words, and a `grep` for the corrected phrasing will not find them.
- `STALE_SWEEP:` for each corrected fact, the search used to locate every restatement of the **pre-amendment** claim, and the hit count remaining in the amended tree. A non-zero count that is not individually justified fails the gate.
- `RECONCILIATION_RERUN:` the arithmetic restated after the amendment — class ids = tier ids = wave ids = stated total — plus every rollup, wave size, prose sum and degradation denominator the scenario-count change touched.

If any of the three is missing or empty, the gate fails closed: do **NOT** create the pass-2 task. Send the `qa-re-plan` back until the sweep is supplied.

**One owner per route, stated so the next reader does not go looking for a missing lane.** This sweep gate **is** QA's amendment verification, and it is the stronger of the two available mechanisms: it refuses to create the pass-2 task at all, where a review lane would only produce findings the router must then act on. The PLAN route's amendment lane (`phase:plan-review-amendment`, `REVIEW_MODE: amendment`) is therefore **PLAN-only and has no QA call site** — `qa-plan-review` and `qa-plan-review-2` deliberately set no `REVIEW_MODE` and inherit the `fresh` default, which is correct because both QA passes *are* fresh. Two mechanisms owning one job is the duplication that made the byte-duplicated PASS rule a trap.

**A correction believed in one artifact and contradicted in another is worse than the original error**, because the reader who checks one file comes away confident. This is the same stale-baseline failure the memory discipline already warns about, one level up: the stale baseline is now the plan's own retracted claim.

**A plan-phase-only stop makes pass 2 MANDATORY.** The single-pass default is justified by execution reviewing the plan implicitly — a plan with bad coverage produces a report with thin evidence, and that surfaces. When the user scopes the workflow to the plan phase and no `qa-build`/`qa-execute` task is ever created, **that safety net does not exist and nothing downstream will catch an unswept amendment.** Run pass 2 whenever pass 1 returned findings, and do not offer to skip it.

```text
TaskCreate({
  subject: "CC10X qa-plan: Revise test plan after fresh review",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-re-plan\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Revise plan artifacts if fresh review finds blocking issues\n\nOnly run if pass 1 finds blocking issues. Amend the saved artifacts using the structured review findings. Verify every finding against the cited source before accepting it, and record which findings were the plan's error versus the reviewer's. SWEEP ALL THREE ARTIFACTS — feature-map.md, test-plan.md and env-plan.md — for every restatement of each corrected fact, including handoff sections, scope statements, provenance paragraphs, open-question tables, routed-out findings, prerequisite tables and degradation tables. Re-run every rollup and every stated arithmetic sum the amendment touched. Report AMENDED_FILES, STALE_SWEEP and RECONCILIATION_RERUN — the pass-2 gate fails closed without all three.",
  activeForm: "Revising test plan"
}) -> qa_replan_task_id
TaskUpdate({ taskId: qa_replan_task_id, addBlockedBy: [qa_plan_review_task_id] })

TaskCreate({
  subject: "CC10X plan-gap-reviewer: Fresh review of revised test plan",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-plan-review-2\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Anti-anchoring review of the amended test plan (pass 2)\n\nOnly run if qa-re-plan produced revised artifacts after pass 1 findings. Apply the same coverage lens as pass 1, and additionally judge the AMENDMENT ITSELF: does every corrected fact now read consistently across all three artifacts, or does some section still state the retracted position as current? Do the rollups, wave sizes and every prose arithmetic sum reflect the new scenario count? Does every scenario added by the amendment appear in a coverage-table row, a wave, a class bucket and a tier bucket? Does every fixture, observability row and open decision the amendment invalidated get updated rather than left pointing at the old values? A half-propagated correction is the specific failure this pass exists to catch.",
  activeForm: "Fresh-reviewing revised test plan"
}) -> qa_plan_review_pass2_task_id
TaskUpdate({ taskId: qa_plan_review_pass2_task_id, addBlockedBy: [qa_replan_task_id] })
```

#### Preflight (`phase:qa-preflight`)

Runs `cc10x:qa-harness-builder` in **`MODE: preflight`** — a new mode on the existing agent, not a
new agent. It already provisions and it already carries the absolute no-product-code boundary,
which preflight must inherit unchanged; inheriting it from the same file means it cannot drift.

**Why this is its own phase and not the first section of `qa-build`.** `qa-build`'s contract is a
*build report*. A preflight BLOCK arriving through it is indistinguishable from a build failure by
any parse the router can perform — which forfeits the entire point: telling `missing-input` apart
from `defect`. A distinguishable verdict is worth one phase value.

**The router MUST set `phase_cursor="qa-preflight"` before dispatching.** See Rule 1 — the bare
parent value `qa` is in `PLAN_PHASES`, and leaving the cursor there makes the isolation guard block
preflight's own provisioning while looking correct.

```text
TaskCreate({
  subject: "CC10X qa-preflight: Can this run happen?",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-preflight\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Measure the environment before anything expensive runs\n\nRun in MODE: preflight. Read .cc10x/qa/env/{env_key}/setup.md if it exists (T0), and at T0 also measure branch currency for EVERY repo in the topology — enumerate the repo set from the feature map and env plan first, then per repo run git rev-parse --abbrev-ref HEAD, git rev-parse --short HEAD, git rev-list --count HEAD..{default_branch} and git status --porcelain, and emit a REPO_CURRENCY row for each. A REPO_CURRENCY list shorter than the topology's repo set is invalid output: measuring only the repos you touch is what leaves one side current and one side stale. Emit a CURRENCY_GATE entry for every repo with commits_behind > 0 or a dirty tree, carrying failure_class: wrong-guess and the question 'measure against {branch} as checked out, or pull forward to {default_branch}?'; non-empty CURRENCY_GATE forces STATUS: BLOCKED with NEXT_ACTION: gate. Do NOT fast-forward, rebase or otherwise move any checkout on your own initiative — measuring is always legal, deciding is never yours. Then run checks in strict cost order T1 -> T4 and STOP THERE. Never boot a service: report SERVICES_PROVISIONED: [] — a non-empty value is an automatic FAIL. Classify every failing check as missing-input, wrong-guess or defect; a failed check with no classification is invalid output. Measure which human-owned prerequisites are ACTUALLY missing rather than transcribing env-plan.md §11's predicted list, and give every one a real acquisition recipe. Append everything measured to the setup record, never overwrite: a stable row whose re-probe disagrees becomes superseded and sets SETUP_RECORD_STALE, a derived row whose fingerprint no longer matches becomes unverified. Do NOT ask the user anything — return STATUS: BLOCKED with NEXT_ACTION: gate and let the router raise one batched question.",
  activeForm: "Measuring the environment"
}) -> qa_preflight_task_id
TaskUpdate({ taskId: qa_preflight_task_id, addBlockedBy: [qa_plan_review_task_id, qa_replan_task_id, qa_plan_review_pass2_task_id] })
```

Preflight inherits the three blockers `qa-build` carried before this phase existed, so the effective
ordering is unchanged.

**The batched ask — router-owned, and the agent never raises it.** On `STATUS: BLOCKED` with
non-empty `HUMAN_PREREQUISITES` **or non-empty `CURRENCY_GATE`** — two independent triggers, one
question. A `CURRENCY_GATE` entry is not a prerequisite and must not be forced into that list: a
stale checkout is not something the human must *acquire*, it is a decision they must *make*, and an
entry with no `acquisition` recipe is invalid output. Take the question text verbatim from the entry:

1. Persist the list verbatim to `qa.preflight.human_prerequisites`, the gate entries to
   `qa.preflight.currency_gate`, and the rest of the contract to `qa.preflight`.
2. Append a `preflight_blocked` event to the event log.
3. Set `pending_gate="qa_preflight_human_prerequisites"`.
4. Raise **exactly one** `AskUserQuestion`, in its own message, listing every prerequisite with its
   `acquisition` recipe and what it blocks, **and every `CURRENCY_GATE` repo with its
   `commits_behind` and its two options**. One batched question, whatever mix of missing
   prerequisites and stale repos produced it.

One question, once, with an accurate list — not drip-fed across a bring-up sequence. This is a
**gate**, not a capability offer: the never-re-offer restraint does not apply, and the workflow
cannot advance until it is answered. A question raised inside a subagent instead would leave no
record in the workflow artifact, would not survive compaction, and could not stop a workflow —
`SKILL.md` §14 makes the router the only orchestration state owner.

On resolution the router re-dispatches a fresh `qa-preflight` task. There is no `re-qa-preflight`
phase: `re-qa-build` and `re-qa-execute` exist because remediation arrives from a *downstream*
phase, whereas preflight's retry arrives from the user, in place.

**Four rules specific to this phase:**

- **The T4 ceiling.** Preflight never boots a service. `SERVICES_PROVISIONED: []` is the
  machine-checkable proof, and a non-empty value fails the phase.
- **Never convert an environment problem into a product verdict.** A missing prerequisite is
  `BLOCKED`, never `FAIL`. That distinction is the phase's whole output.
- **Never move a checkout unasked.** Preflight measures branch currency; it does not act on it. No
  fast-forward, no rebase, no reset on the agent's own initiative — the pull is legal only on an
  **answered currency gate**. This rule binds `qa-build` identically (`qa-harness-builder` states it
  mode-independently, and `env-plan.md`'s `harness`-owned *"checkout fast-forward"* licence is scoped
  to the same answered gate), because a route that requires one repo to be measured while licensing
  another to be silently moved has simply relocated the asymmetry. **Measuring is always legal;
  deciding is never the agent's.**
- **Never edit product code.** The same absolute prohibition the researcher, harness builder and
  executor carry — restated here so it is not read as applying only to the other three.

**Naming, disambiguated.** Step 0a's capability discovery writes `qa.qa_env_preflight`: read-only,
before any dispatch, answering *"what can this machine do?"*. This phase writes `qa.preflight`:
provisioning-capable, after plan review, answering *"can this specific run happen?"*. Same word,
two different things, two different artifact keys — do not conflate them.

#### Harness build (`phase:qa-build`)

```text
TaskCreate({
  subject: "CC10X qa-harness-builder: Build test harness",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-build\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Build test environment and test suites\n\nBuild the harness described by the test plan and environment plan: environment provisioning scripts (up/seed/health-gate/down), integration tests, backend E2E scripts, UI automation, observability probes, the harness manifest, fixtures, cleanup verification, and the report emitter. Do NOT modify product code. Stop if blocked, partial, or scope grows beyond the plan.",
  activeForm: "Building test harness"
}) -> qa_build_task_id
TaskUpdate({ taskId: qa_build_task_id, addBlockedBy: [qa_preflight_task_id] })
```

**Exactly one blocker, and that is deliberate.** Preflight already inherits the three plan-review
blockers, so the transitive ordering is identical. Keeping the three *and* adding preflight would be
harmless but redundant; keeping the three and *not* adding preflight orphans the new phase — the
build would run before anything measured the environment, which is the whole failure this phase
exists to prevent. Do not re-add them.

```text
```

**Extra rounds when the mutation floor is unmet (`phase:re-qa-build`).**

The harness builder returns `gaps_found`, not `passed`, when the mutation floor is unmet. The floor's
three branches live in `qa-harness-builder.md` and are not restated here: one `assertion_falsified`
per provable property when the test plan declares a non-empty provable-properties section (applying
only to the self-flagged rows once that section declares more than 8), and one per tier **and** one
per wave when it does not. The router may dispatch a re-build round to close the gap.

```text
TaskCreate({
  subject: "CC10X qa-harness-builder: Close the unmet mutation floor",
  description: "wf:{workflow_uuid}\nkind:remfix\norigin:qa-harness-builder\nphase:re-qa-build\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Mutation floor unmet for {named properties or tiers}\n\nUnfloored: {the named provable properties, or the named tiers and waves}. Every `outcome: blocked` entry from the previous round, with its `blocked_reason`, verbatim: {list}. For each one, falsify a named assertion and record `applied_evidence` and `failing_assertion` — or move it to `TESTABILITY_BLOCKERS` naming the seam the product does not offer. Do NOT modify product code.",
  activeForm: "Closing the mutation floor"
}) -> qa_rebuild_task_id
TaskUpdate({ taskId: qa_rebuild_task_id, addBlockedBy: [qa_build_task_id] })
```

- **`origin:qa-harness-builder`. Do not "simplify" this to `origin:router`.** The `kind:remfix`
  dispatcher row in SKILL.md §7 (HEAD `:341`) matches `origin:router`, `origin:code-reviewer` and
  `origin:integration-verifier` and sends them to `component-builder` — a product builder dispatched
  into a QA phase, with a licence to edit product code that this phase spends a hard boundary
  forbidding. `qa-harness-builder` is not a member of that row's origin set, so the row cannot fire,
  and the `qa-build, re-qa-build` row matches unambiguously. It is also the semantically correct
  value: SKILL.md §3 binds `origin:` on a `kind:remfix` task to *the agent whose findings triggered
  the fix*, and an unmet mutation floor is the harness builder's own finding about its own suite.
- **It is not the executor, and this note stays in the file so nobody re-derives the wrong answer.**
  Setting `origin:` to `qa-executor` here was wrong twice over: the value was absent from SKILL.md's
  origin enum, and it named an agent that has not run yet at `qa-build` time. The executor is a legal
  origin now, but for its own downstream `re-qa-build` path, never for this one.
- **This adds no phase and no dispatcher row.** `re-qa-build` is already declared in the SKILL.md
  `phase:` enum, and the `qa-build, re-qa-build` dispatcher row already routes it to
  `qa-harness-builder`. Only the origin vocabulary was short.
- **Cap: 2 extra rounds, then a user checkpoint.** Not a silent third. When two rounds have not
  floored the suite, the router stops and asks — an unprovable suite is a decision, not a retry.
- **Every round carries changed input**: the named unfloored properties or tiers, plus **every**
  `blocked_reason` from the round before. Never "try again". `remediation-and-research.md` already
  forbids re-dispatching a task with unchanged input, and this is that rule instantiated — the changed
  input is what makes the round legal, not the round counter.
- **The honest exit is `TESTABILITY_BLOCKERS`**, which escalates to a BUILD for the missing seam. Never
  a silent pass.

**Hard boundary — the harness builder must not touch product code.** If building the harness reveals that the product is untestable as written (no seam, no health endpoint, no log line to assert on), that is a FINDING, not a licence to refactor. Report it as `SCOPE_INCREASES` and let the router route a BUILD.

#### Harness review (`phase:qa-review` ‖ `phase:qa-hunt`)

Reuses `code-reviewer` and `failure-hunter` unchanged, in parallel, in one message — same rule as BUILD (SKILL.md §12 step 5), same sequential fallback if parallelism is unavailable.

```text
TaskCreate({
  subject: "CC10X code-reviewer: Review test harness",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-review\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Review harness code quality\n\nReview the harness code. Judge it as production code — it is.",
  activeForm: "Reviewing test harness"
}) -> qa_reviewer_task_id
TaskUpdate({ taskId: qa_reviewer_task_id, addBlockedBy: [qa_build_task_id] })

TaskCreate({
  subject: "CC10X failure-hunter: Hunt silent failures in harness",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-hunt\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Audit harness for silently-passing tests\n\nHunt for the harness-specific failure mode: assertions that cannot fail, swallowed errors in setup, teardown that ignores its own exit code, waits that mask races, and skipped tests that report as passed.",
  activeForm: "Hunting harness failures"
}) -> qa_hunter_task_id
TaskUpdate({ taskId: qa_hunter_task_id, addBlockedBy: [qa_build_task_id] })
```

> **Why the hunter is non-negotiable here.** A test harness that swallows errors does not merely fail — it reports PASS while proving nothing. A silently-green suite is strictly worse than no suite, because it converts an unknown into a false certainty. This is `failure-hunter`'s exact remit, applied to the one codebase where the failure mode is most dangerous.

#### Execute (`phase:qa-execute`)

```text
TaskCreate({
  subject: "CC10X qa-executor: Run test plan and report",
  description: "wf:{workflow_uuid}\nkind:agent\norigin:router\nphase:qa-execute\nplan:.cc10x/qa/{workflow_uuid}/test-plan.md\nscope:N/A\nreason:Execute scenarios and produce report\n\nBring the environment up per the env plan, gate on readiness, execute every scenario in the test plan, assert all observation points, capture expected/actual/exit-code evidence per scenario, tear down, verify teardown, and write .cc10x/qa/{workflow_uuid}/report.md. Emit BUG_CANDIDATES for every failure. Before comparing, enumerate the sibling set — the enum, the validation chain, both sides of the cross-repo contract — and emit siblings_swept on every candidate with a findings entry for every member you listed; a findings list shorter than its members list is invalid output, and a defect with no sibling set says so in set_name rather than omitting the field. Classify every failing check with failure_class (missing-input | wrong-guess | defect) — the same vocabulary qa-harness-builder's preflight CHECKS[].classification uses — and open report.md with a ## Failure classes section carrying every count in FAILURE_CLASS_COUNTS, zeros included. Before emitting ANY bug candidate, RE-MEASURE branch currency yourself, per repo the finding spans — git rev-parse --abbrev-ref HEAD, git rev-parse --short HEAD, git rev-list --count HEAD..{default_branch}, git status --porcelain — and do not copy commits_behind from setup.md, which records it as a volatile fact that is always re-checked and never trusted from the file. Emit measured_on on every candidate; a candidate without it is invalid output. Cap severity at unconfirmed when any measured_on entry has commits_behind > 0 — a confidence floor, not an impact level — and when the defect is a cross-repo contract mismatch, read the contract on both repos' default branches and state both readings in siblings_swept.branch_axis. Do NOT edit test code or product code to make a run pass.",
  activeForm: "Executing test plan"
}) -> qa_execute_task_id
TaskUpdate({ taskId: qa_execute_task_id, addBlockedBy: [qa_reviewer_task_id, qa_hunter_task_id] })
```

#### Memory

```text
TaskCreate({
  subject: "CC10X Memory Update: Persist QA learnings",
  description: "wf:{workflow_uuid}\nkind:memory\norigin:router\nphase:memory-finalize\nplan:N/A\nscope:N/A\nreason:Persist captured Memory Notes\n\nROUTER ONLY: execute inline. Read the workflow artifact and THIS task description payload, persist to .cc10x/*.md, then remove the matching [cc10x-internal] memory_task_id line from activeContext.md ## References. Never spawn Agent() for this task.",
  activeForm: "Persisting QA learnings"
}) -> memory_task_id
TaskUpdate({ taskId: memory_task_id, addBlockedBy: [qa_execute_task_id] })
```

---

#### Reduced task graph (`qa_scope=probe`)

`qa-researcher` (code source only) → `qa-plan` → `qa-harness-builder` → `qa-executor` → Memory.

No fan-out, no plan review, no separate reviewer/hunter tasks. The executor folds a brief harness sanity pass into its report. **The executor's evidence protocol is NOT weakened** — scenario accounting still reconciles, teardown is still verified.

Escalate to the full graph when the harness builder reports non-empty `SCOPE_INCREASES` (**either mode**) or non-empty `BLOCKED_ITEMS` (**`MODE: harness` only**): create the plan-review, reviewer, and hunter tasks, re-block the executor on `[qa_reviewer_task_id, qa_hunter_task_id]`, persist `qa_scope=standard` and an escalation entry in `status_history`.

**A preflight `BLOCKED_ITEMS` never escalates `qa_scope`.** Preflight runs *as* `qa-harness-builder`, so without this carve-out the rule above would fire on its first missing prerequisite — and a missing credential is the ordinary result of a cheap first check, not evidence the scope was wrong. Escalating there would make `probe`, the cheapest scope, the most expensive one the moment anything is unset. `SCOPE_INCREASES` still escalates in both modes, because a product testability blocker is a real scope finding wherever it is found.

**Preflight is included in the reduced graph.** `probe` scope *assumes* the environment is already runnable; preflight is the cheapest possible test of exactly that assumption, and it is the one phase probe scope should never drop.

---

### Isolation and phase discipline (ENFORCED)

These are enforced by `scripts/cc10x_qa_isolation_guard.py` (PreToolUse, matcher `Read|Grep|Glob|Edit|Write|NotebookEdit|Bash`). Prompt text alone was proven insufficient — a prior run installed global skill fixtures onto the user's machine during a planning phase, via `Bash`, which the `Edit|Write` guards never saw.

**Rule 1 — planning phases mutate nothing.** During `qa` (the bare parent value), `qa-research`, `qa-plan`, `qa-plan-review`, `qa-re-plan`, and `qa-plan-review-2`, no agent creates files outside `.cc10x/`, installs fixtures, provisions services, or runs setup. Planning produces documents. Building the environment is `qa-build`; running it is `qa-execute`. Write what the environment SHOULD be into `env-plan.md` — do not build it.

**`qa-preflight` is NOT a plan phase and is deliberately absent from that list.** It probes the real environment — binds a port, stats a credential, runs `docker info` — which is exactly the mutation this rule forbids during planning. It is declared in the guard's `PROVISIONING_PHASES` instead, and `scripts/test_cc10x_qa_phase_invariants.py` asserts the two sets stay disjoint.

**The router MUST set `phase_cursor="qa-preflight"` BEFORE dispatching preflight.** The bare parent value `qa` is a member of `PLAN_PHASES`, so a `phase_cursor` left at `qa` while preflight runs makes the guard block preflight's own provisioning — and it does so while looking entirely correct, with no error a reader would recognise as a misconfiguration. This is asserted behaviourally by PP-6 case (b).

**Rule 2 — `Bash` is a write surface.** Any agent holding `Bash` can mutate regardless of what its prompt calls it. `Bash` is for inspection (`git log`, `git show`, `grep`, `ls`, `--help`). Redirection, heredocs, `mkdir`, `rm`, `git init`, package installs, and container commands are mutations.

**Rule 3 — a read denylist is enforceable state, not prose.** When a workflow must not read certain paths (quarantined material, a comparison baseline, out-of-scope repos), the router persists them into the workflow artifact:

```json
"qa": { "isolation": {
  "denied_reads": ["/abs/path/answer-sheet.md", "**/test/*.e2e-spec.ts"],
  "denied_read_reason": "quarantined for benchmark comparison",
  "plan_phase_readonly": true,
  "mutation_allowlist": [".cc10x/"]
}}
```

The router MUST persist this **before dispatching the first researcher**. A denylist stated only in a prompt is a request; in the artifact it is a refusal, and it survives compaction and fresh sessions.

**Rule 4 — a blocked call means record a gap.** When the guard denies something, the agent notes the limitation in `GAPS` / `COVERAGE_GAPS` and continues. It does not route around the guard, and the router does not relax the denylist to make a phase pass.

**Rule 5 — the denylist covers the filesystem, and nothing else.** The guard is a PreToolUse hook over file reads. It cannot see a denied document reproduced inside a Jira comment, an MR description, a Confluence page, a Slack thread, or any MCP response — that content arrives through an allowlisted source, in a batch, whole. There is no hook that closes this, so do not design as though there were.

The control is procedural and it lives in `qa-researcher`: recognise, stop, self-report, tag the affected findings, and state which of them were also derived independently. When such an incident is reported, the router:

1. Records it as an artifact under `.cc10x/qa/{workflow_uuid}/research/` — not only in the event log.
2. Checks whether the tagged facts were independently derived by other lanes, and says so in the finding either way.
3. Escalates to the user **before consolidation** with the disposition options: continue-and-exclude the tagged items, drop the affected lane entirely, or abort.

The user rules on the disposition. The router does not absolve itself of a contamination it discovered, and does not abort a run over a leak that provably added nothing.

**When a denylist is worth using outside a benchmark.** Two real cases, both ordinary: *regression-blind planning* — deny the existing test suite so the plan is derived from the feature rather than converging on what is already covered; and *scope fencing* — deny other tenants' data, unrelated repos, or material the engagement does not cover. Set `denied_read_reason` to the real reason in both cases; it is quoted back to the agent in the denial message and it is what makes the refusal legible rather than arbitrary.

### QA-specific rules

- **QA never edits product code.** Not the researcher, not the harness builder, not the executor. Product defects are reported, never repaired inside QA. This is what keeps QA's verdict trustworthy: a route that can fix what it measures cannot be believed about what it measured.
- **The executor may not edit tests.** Making a red run green by touching the test is the design's worst failure mode. A harness bug routes to `re-qa-build`; a product bug routes to DEBUG (offered, never automatic).
- **Teardown failure is a workflow failure.** A run that leaves orphaned containers, databases, or cloud resources is not a passing run — it is a passing run plus a leak. The executor reports teardown as a scenario with its own evidence.
- **`qa-execute` is independently re-runnable.** Given a saved test plan and a built harness, the router may run `qa-execute` alone as a fresh workflow (regression run) without repeating research, planning, or build.
- **Environment unavailability is BLOCKED, not FAIL.** Same escape hatch `integration-verifier` uses: `command not found`, `ECONNREFUSED`, `ENOSPC`, version mismatch → classify as ENVIRONMENT, mark scenarios BLOCKED, never convert into a product-code verdict.
- **Never report a QA PASS without the report artifact on disk.** Prose is not a report (SKILL.md §14).

### The failure vocabulary — one name, three surfaces

**`FAILURE_CLASS` is `missing-input` | `wrong-guess` | `defect`. Declared here, once, at route
level.** Every QA surface that sorts a failure uses this vocabulary and no other:

| Surface | Field it travels in | Emitted by |
| --------- | --------------------- | ------------ |
| Preflight's prerequisite and probe rows | `CHECKS[].classification` | `qa-harness-builder` in `MODE: preflight` |
| A failing scenario or bug candidate | `failure_class` | `qa-executor` |
| The durable setup record | the `Class` column on `setup.md` sections 3 and 4 | preflight, appended |

**Three field names, one vocabulary — and that is a deliberate decision, not drift.** Preflight's
`classification` predates this vocabulary having a name; renaming it would touch five in-lockstep
sites for zero new information. What was actually missing was not a consistent field name but the
statement that these *are* the same three values. That statement is this section.

The values are exhaustive and dimensional, which is why there is no fourth:

- **`missing-input`** — the environment lacks something a human must supply. Blocks; never a product
  verdict.
- **`wrong-guess`** — a prediction the measurement contradicted. This is where a stale baseline
  lands: measuring the wrong revision is a wrong guess about what was being measured, not a new
  kind of failure.
- **`defect`** — the product is wrong. The only class that may ever become a bug candidate.

**A failing check with no class is invalid output**, at every one of the three surfaces. And a class
is a sort, not a severity: `defect` is not automatically `critical`, and `missing-input` is not
automatically minor. Severity is a separate axis carrying its own confidence floor.

---

### Bug handoff to DEBUG (advisory, mirrors REVIEW→BUILD)

QA is advisory about product defects. It never auto-starts DEBUG — it offers.

#### 1. Persist first

On `qa-executor` return, write `BUG_CANDIDATES` verbatim into the workflow artifact at `qa.bug_candidates`, and append a `bug_candidates_recorded` event. Do this **before** any offer: the user may decline now and want the bugs tomorrow, and a candidate that only ever existed in conversation is lost at compaction.

#### 2. Offer, do not start

After QA's Memory Update completes, if `qa.bug_candidates` is non-empty, the router MAY offer — in its **own message**, per the capability-offer restraint principle:

```
AskUserQuestion: "QA found {n} bug candidate(s). Start DEBUG for one?"
  - "Debug {highest-severity title} (Recommended)"
  - "Debug a different one"
  - "Not now — they are recorded in the QA report"
```

Never re-offer once declined (capability-offer principle). The candidates stay in the artifact and the report; the user can ask later.

#### 3. A QA-seeded DEBUG is a NEW workflow

Not a phase inside QA — QA may not edit product code, and DEBUG must. So: generate a fresh `workflow_uuid`, create a normal DEBUG workflow, and link it:

- set `source_wf` on the DEBUG artifact to the QA `workflow_uuid`
- set `source_bug_candidate` to the candidate's `title`
- write `[DEBUG-RESET: wf:{new_uuid}]` as normal — attempt counting starts fresh; QA's run is not a failed debug attempt

The DEBUG task graph is unchanged (`debug-workflow.md`). Only the investigator's prompt gains a section.

#### 4. The scaffold — `## QA Bug Context`

Add this optional section to the `bug-investigator` dispatch, built from the selected candidate. Registered in SKILL.md §7 optional sections.

```text
## QA Bug Context

Source: QA workflow {qa_workflow_uuid}, scenario "{scenario}" ({tier})
Severity: {severity}
Baseline: {regression|never_worked|unknown} — {baseline_evidence}

### Pre-built repro loop (VERIFY BEFORE TRUSTING)
Environment setup: {env_setup_command}
Repro command:     {repro_command}
Ladder rung:       {repro_ladder_rung}
Deterministic:     {repro_deterministic} {hit_rate}
Expected:          {expected}
Actual:            {actual}

### Environment
Mode: {env_mode}
Services required: {services_required}
Services stubbed:  {services_stubbed}

### Boundary observations (pipeline order — pre-filled matrix)
| # | Boundary | Kind | Expected | Actual | Result |
|---|----------|------|----------|--------|--------|
{rows from boundary_observations}
First failing boundary: {first_failing_boundary}

### Variants exercised
{variants_exercised}

### Evidence (verbatim)
{evidence}

### QA's suspicion (HINT ONLY — form your own hypothesis)
Suspected: {suspected_service}
Basis: {suspicion_basis}
```

#### 5. Anti-anchoring rule for this scaffold

`suspected_service` travels **only** with its `suspicion_basis`, and always labelled as a hint. Never phrase it as a conclusion, and never drop the basis to save tokens.

QA observed behavior from the outside; it did not read the code path. Passing its guess as a finding is the same pre-judging failure the §7 anti-pre-judging guard prevents for reviewers — it makes the investigation converge fast on the wrong layer. If a candidate has `suspected_service` but no `suspicion_basis`, omit the whole suspicion block.

Everything else in the scaffold is observed evidence and passes through verbatim.

#### 6. Closing the loop — `re-qa-execute`

After the DEBUG workflow verifies its fix, the router MAY offer to re-run the originating QA scenario:

```
"DEBUG verified the fix. Re-run the QA scenario that found it?"
```

This is cheap and it is the real proof. `qa-execute` was designed to run standalone from a saved plan and a built harness, so a regression run needs no research, planning, or build — dispatch `re-qa-execute` scoped to the originating scenario against the existing harness from `source_wf`.

A unit-level regression test proves the root cause is fixed. Re-running the E2E scenario proves the **user-visible symptom** is gone, which is the thing QA originally claimed was broken. They are different claims, and only the second one closes what QA opened.

---

## Deferred — recorded with triggers, not silently carried

Two known gaps in this route. Both are real, both are out of scope where they were found, and both
name the observation that should reopen them. A deferral without a trigger is an omission with
better manners.

### Deferred: machine-readable mutation log

The mutation gate is contract prose. Nothing mechanical can read a `MUTATION_CHECKS` block and tell
`assertion_falsified` from `blocked` — the outcome enum makes the distinction *sayable* and makes
`survived` fatal, but a router still takes the agent's word for which one happened. The
machine-readable version would be a `mode: 'mutation'` scenario class plus runner support for it,
and it is the only route to hook enforcement of the mutation gate.

**What it would touch:** `templates/live-harness.template.json`, whose keys today are `name`,
`workdir`, `required_env`, `environment`, `setup`, `reset`, `seed`, `healthcheck`, `scenarios` and
`cleanup` — **no mutation surface at all**. Adding one opens the manifest and the runner together.
That cost is stated here so the next reader sees it before deciding, rather than discovering it
mid-change.

**Trigger:** *if a run's mutation checks conflate `blocked` with `assertion_falsified` despite the
hardened contract, build the machine-readable mutation log.* Measure first, then build the
subsystem — not the other way round.

> **A deferral trigger must never name a specific run.** Naming one tells that run's agent what it
> is about to be measured on, and an agent told the win condition optimises for it — the measurement
> stops being evidence. This trigger named a run until it was caught doing exactly that: the run
> read this section during orientation and announced it would measure the trigger explicitly. State
> the *condition*, never the occasion.

### Deferred: no verifier for a QA plan amendment made after `qa-plan-review-2`

QA owns its own amendment verification through the fail-closed sweep gate: a `qa-re-plan` report
must carry `AMENDED_FILES`, `STALE_SWEEP` and `RECONCILIATION_RERUN` or the pass-2 task is never
created. That gate is strictly stronger than a review lane, which is why QA has no amendment lane
and does not need one.

**What it does not cover:** an amendment made *after* `qa-plan-review-2` has already passed. At that
point both the sweep gate and pass 2 are behind us, and nothing re-reads the plan. The hole is
smaller than the one the PLAN route had — pass 2 is mandatory on a plan-phase-only stop, and the
sweep gate re-runs on every amendment before it — but it is the same shape, and it is recorded here
so the next reader does not conclude the QA side is closed.

**Trigger:** if a QA run ships an unswept post-pass-2 amendment.
