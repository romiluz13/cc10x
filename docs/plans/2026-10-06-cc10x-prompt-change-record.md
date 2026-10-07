# CC10x remediation: prompt change record (Phase 4)

One section per task. Classification for every task: `orchestration_sensitive` (ASM-7, authorized by the autonomous-build instruction). Checklist sections 3-4 (Tier 1): `harness_audit`, `workflow_replay_check`, manual semantic drift review, prompt diff review.

## P4.T1.1 `references/remediation-and-research.md`

Findings: B1, B6, B9 (part), B10 (part), A4 (part).

Files: `plugins/cc10x/skills/cc10x-router/references/remediation-and-research.md`; new pins in `plugins/cc10x/tools/prompt_clause_assertions.py` (5 added).

What changed:
- Added `### REM-FIX TaskCreate template` (one literal call carrying the seven metadata lines, with a body that asks the fix agent for `COVERING_TESTS`, `TEST_COMMAND`, `TEST_OUTPUT`, or the dispute triple).
- Added `### Producers of the REM-FIX gate fields`: the remediating builder produces `COVERING_TESTS`/`TEST_COMMAND`/`TEST_OUTPUT` and `FINDING_DISPUTED`/`VERIFY_COMMAND`/`VERIFY_OUTPUT`; `integration-verifier` produces `DISPUTE_UPHELD`/`DISPUTE_REJECTED` (it was already named the adjudicator in the same file).
- Circuit breaker: the `### Circuit breaker` block is the single definition. The "Change-something" paragraph, Fix-wave consolidation and the Re-review loop step 1 and precondition-gate bullet now point at it. The Re-review loop no longer re-counts at REM-FIX completion; the limit is evaluated at creation only (plan: "one trigger point").
- Count semantics kept as the hooks implement them: the router counts `kind:remfix` tasks per `wf:` before creating one (ask at count >= 3); the guard counts `remediation_history` entries (appended at creation) and flags above 3. The plan text said "count completed REM-FIX tasks"; the hook counts created entries, so the hook version was kept (rule 4: pick the version enforced by hooks).
- "Hook-enforced backstop" relabeled "Audit backstop" and states the real behavior: `taskMetadata` ships as `audit` (log and stderr warning); it blocks only when set to `block`.
- Dead branches: removed "Legacy agent-created remediation tasks are still accepted" (no agent creates a REM-FIX; code-reviewer and failure-hunter say so) and "or on the re-reviewer for REVIEW" in the re-review loop (REVIEW never creates a REM-FIX per `review-workflow.md`; stated once in step 1).
- No dangling ADR or RFC references existed in this file, so none were changed (those live in `qa-workflow.md`, task T1.4).

Why safe: the number of allowed cycles (3), the ask-before-fourth rule, the artifact-authoritative tiebreak, the re-review precondition gate and its fail-closed rule, and verify-before-implement are unchanged. The guard code is untouched.

Claim boundary: now true: every gate field has a named producer and the router has a template that asks for it. Still not claimed: the agent contracts do not yet carry the fields (P4.T4.2/T4.3), and the shipped hook mode only warns.

Pins and fixtures: 5 new clause pins (template, producers, single circuit breaker, audit wording, unreachable branches). `remfix-gate.json` unchanged and green. No existing pin was edited or removed.

## P4.T1.2 `references/workflow-artifact-and-hook-policy.md` and `workflow-artifact.skeleton.json`

Findings: B7, B8, B10 (part), C2 (part), B14 (part).

Files: the policy reference; the skeleton; `plugins/cc10x/tools/workflow_replay_check.py` (new `CONVERGENCE_STATES`, enum check over every fixture, `build-happy-path` expectation); five fixtures migrated (`build-happy-path`, `build-doc-sync-happy-path`, `build-doc-sync-skipped`, `qa-route-happy-path`, `multi-phase-memory-finalize`: `stable` becomes `converged`); 12 new clause pins in `prompt_clause_assertions.py`.

What changed:
- Required-field tables: new "Read-only and advisory agent required fields" table with rows for `code-reviewer`, `failure-hunter`, `integration-verifier`, `triage-agent`, `architecture-scanner`, each copied from the keys in the agent's own YAML block (checked mechanically by a pin). `IMPLEMENTATIONS_FOUND` dropped from the researcher row (the agent emits `KEY_FINDINGS_COUNT`). Planner row gains `PLAN_REVISION`, `LAST_REVIEWED_REVISION` (the agent already emits both) and, on a `phase:qa-re-plan` return, `AMENDED_FILES`, `STALE_SWEEP`, `RECONCILIATION_RERUN` (addenda item 2; `qa-workflow.md` already fails the pass-2 gate without them, `planner.md` does not yet carry them: P4.T4.4 owns that, and the pin exempts exactly these three names until then).
- Parsing direction: one paragraph for every agent: the router branches on `STATUS` from the YAML block; envelope and heading are quick presence signals; the YAML block decides on disagreement. This follows the agent files ("the router branches on STATUS, it MUST appear in the YAML block"). Quoted from `agents/code-reviewer.md` and `agents/failure-hunter.md`, Output sections.
- `normalized_phases` names now match `build-workflow.md` BUILD preparation step 8 (`inputs`, `files/surfaces`, `expected_artifacts`, `required_checks`, `checkpoint_type`), keeping the identity keys `phase_id`/`title` that the replay fixture reads. `build-workflow.md` itself is untouched (T1.3).
- `plan_trust_gate`: one definition, pointing at the checks in `build-workflow.md` BUILD preparation step 3; the phantom `plan_trust` anchor is gone.
- `DIFF_DRIVEN_DOCS: skip`: stated as read from `activeContext.md ## Session Settings`, where the router reads it.
- `verification_rigor`: skeleton default `null`; policy states it must be set explicitly, and `plan_trust_gate` fails while it is null with a plan present.
- `CONVERGENCE_STATES` = pending, needs_iteration, converged, N/A. Values in use were pending, needs_iteration, stable, N/A, and the router prose (`SKILL.md` convergence row) says `converged`; `converged` was chosen because the router text names it and `SKILL.md` cannot be edited in this task, so `stable` (five fixtures) was migrated. `N/A` is kept for the two advisory routes.
- Event types: split into router-appended (`workflow_started`, `result_persisted`, `memory_finalized`, `inline_fallback_entered`), hook-appended (`compact_occurred`, `artifact_mutated`) and not emitted (`agent_started`, `agent_completed`, `contract_parsed`, `remediation_created`, `scope_decision_requested`, `scope_decision_resolved`); `workflow_completed`/`workflow_failed` described as terminal markers the QA guard accepts but no router step appends. Hook-log events (`subagent_stop`, `instructions_loaded`, `stop_failure`) are named as a separate log, and the StopFailure/InstructionsLoaded/SubagentStop bullets now say "hook log". The plan counted "six unemitted and seven unlisted"; verified counts: six unemitted router names, and seven unlisted emitted names once the three hook-log names are included with the four workflow-log ones.
- PostToolUse: "rejects" replaced with the documented behavior (exit 2 after the write, stderr to the model, malformed artifact stays on disk until repaired), matching the hooks README and guard docstring from P1.T10.
- Hooks key on the newest-mtime artifact (named guards), TaskCompleted keys on the task's `wf:`; `phase_exit_gate` is router-enforced and no hook checks it.
- Citation bounce (C4.2 default, floor unchanged): the "fewer than 3 file:line evidence citations" rule is kept verbatim and labelled a validity check that does not change the per-finding reporting floor. The agent half (its Zero-Finding Gate asks for one positive assertion and sets CONFIDENCE 70, which is below the router's three-citation bar) is for P4.T4.3, which must align the agent to this router text rather than the reverse, because lowering the router bar would weaken a fail-closed gate.

Why safe: no gate semantics changed. The three-citation rule, plan_trust checks, memory_sync and phase_exit semantics, the artifact guard behavior and the hooks are untouched; the new text describes behavior the hooks already have. The only behavior-adjacent edits are `verification_rigor` null (presence-only checks still pass; the explicit-set rule was already in `build-workflow.md` step 3) and the `converged` value, which is already what `SKILL.md` documents.

Claim boundary: now true: no two policy tables disagree on field names with the agent files (pin-checked); the event list says which names are live. Still not claimed: `SKILL.md` still says the skeleton "ships every required key already populated with safe defaults" and does not list `verification_rigor` among the fields the router fills (a T1.5 item, not edited here); `skills/diff-driven-docs/SKILL.md:171` still says the opt-out lives in `CLAUDE.md` (a skill-side fix, outside P4.T1.2; deferred to the P4C pass); the `planner.md` amendment-lane fields land in P4.T4.4.

Pins and fixtures: 12 new pins (assertion count 276: 259 at P4 start, plus 5 in T1.1, plus 12 here; floor 253 plus additions holds); five fixtures migrated; `build-happy-path` expected value moved to `converged` in the replay check. No existing pin was edited, weakened or removed.

Classification: `orchestration_sensitive`.

## P4.T1.3 `build-workflow.md`, `debug-workflow.md`, `plan-workflow.md`, `review-workflow.md`

Findings: B3, B8 (part), B10 (part), B11 (part).

Files: `build-workflow.md` (new `#### Multi-phase iteration`), `debug-workflow.md` (fan-out `scope:`), `workflow-artifact-and-hook-policy.md` (one definition of "inline verification", one sentence); four new clause pins in `prompt_clause_assertions.py`. `plan-workflow.md` and `review-workflow.md` needed no edit (see below).

What changed:
- Multi-phase BUILD rule, one home under "BUILD task graph": the next phase's graph is created only after the previous phase's `phase_exit_gate` passes and `phase_cursor` advances (builder blocked on the previous verifier, BASE re-recorded per step 11a); Memory Update is created once per workflow with the last phase's graph, blocked on the last phase's verifier or its doc-sync task, never finalized after an earlier phase. This is the rule the `multi-phase-memory-finalize` fixture encodes (its checker requires memory blocked by the last verifier or its doc-sync task and by no earlier-phase task); the text was written to match the fixture, not the reverse.
- DEBUG fan-out: the template carried a free-text `scope:{files ...}` value outside the closed `scope:` enum in `SKILL.md` section 3 (`ALL_ISSUES|CRITICAL_ONLY|N/A|{source}|code:{repo}`). It is now `scope:N/A`, and the owned file set moves into the description body, the same choice the QA route already made for its finding text. The fan-in conflict check now speaks of the declared file set.
- "Run inline verification": the phrase appears in `SKILL.md` and in the policy reference, defined nowhere. The policy reference sentence at the malformed-YAML rule now says what it means and points at the `SKILL.md` section "Inline no-subagent execution" (its inline verification pass). The `SKILL.md` occurrences are left for T1.5.
- `normalized_phases` names: already aligned with `build-workflow.md` in T1.2; no change here.

Not changed, with reason:
- `[BUILD-START]` / `[PLAN-START]`: neither marker appears in any of the four reference files. They live only in `SKILL.md` ("Marker rules"; written, read nowhere). Default is remove: pending for T1.5a.
- The 14 plugin-root reference lines (R-B11 verdict BROKEN; P4.T1.4b skipped, deferred): untouched, including `build-workflow.md` lines 7 and 207 equivalents.
- B10 sub-item "spike SKILL_HINTS unreachable": the only text is `SKILL.md` ("Include `cc10x:exploration` only on an explicit de-risk/spike intent"); pending for T1.5a, not a reference-file edit.
- B10 sub-items "REVIEW re-review branch" and "legacy agent-created remediation": done in P4.T1.1.
- `review-workflow.md` already states REVIEW never creates REM-FIX tasks; nothing dead remained there. `plan-workflow.md` has no defect named by the task.

Why safe: no gate semantics changed. `phase_exit_gate`, `plan_trust_gate`, the memory sync gate, per-phase review/verify, and the Memory Update blocking rule (last verifier or doc-sync) are as documented before; the rule is stated once where it was only implied. The scope enum change removes a value no hook or fixture reads (the TaskCompleted guard audits only that the seven lines are present).

Claim boundary: now true: the multi-phase graph/memory rule is written down once and matches the fixture; the fan-out template stays inside the metadata enum. Still not claimed: the `SKILL.md` marker rules, the spike hint and the remaining "inline verification" mentions are unedited until T1.5a.

Pins and fixtures: four new pins (assertion count 280). No existing pin was edited, weakened or removed. No fixture changed.

Classification: `orchestration_sensitive`.

## P4.T1.4 `qa-workflow.md`, `triage-workflow.md`, `codebase-health-workflow.md`

Findings: B2, B9 (part), A5 (part), B11 (part), plus the QA half of B1/C2 wording.

Files: the three references; `plugins/cc10x/tools/workflow_replay_check.py` (`MEMORY_TASK_WORKFLOW_TYPES` extended, docstring updated, advisory-route Memory Update check); fixtures `triage-happy-path.json` and `codebase-health-happy-path.json` (now carry the agent task and the Memory Update task); `scripts/test_cc10x_validators.py` (TRIAGE and CODEBASE-HEALTH moved from "may complete without a finalize" to "must finalize"); `scripts/test_cc10x_qa_phase_invariants.py` (two pin tokens and comment wording); five new clause pins.

What changed:
- TRIAGE and CODEBASE-HEALTH graphs gain a router-inline Memory Update task (`kind:memory`, `phase:memory-finalize`, blocked by the triage or scanner task), copied from the REVIEW graph. The completion paragraphs now say the router runs it after completing the agent task. ADR 0002 is untouched: both routes stay advisory-only, with no phases, no `phase_cursor` and no auto-dispatch; the added task is router bookkeeping, not an agent.
- Replay checker: `MEMORY_TASK_WORKFLOW_TYPES` now covers every route except ORIENT; the docstring says so, and warns that a real TRIAGE or CODEBASE-HEALTH artifact completed without a finalize under the old graph now fails the artifact check. The two advisory fixtures assert one agent task plus one Memory Update task blocked by it.
- Dangling citations in `qa-workflow.md`: `docs/adr` holds only 0001 and 0002, so "ADR-1/2/4" and "RFC section 6c/6d" named nothing. Each was replaced by a plain statement: the worktree paragraph and the phase-token paragraph now say "this paragraph is the decision record"; the finishing-menu mention points at step 0; the QA-owned-rules sentence and the two RFC parentheticals lose their citation. Pins that required the literal tokens (`PP30A_TOKENS` "ADR-2", `PP31_RATIONALE_TOKENS` "ADR-1") now require "this paragraph is the decision record", so the property (the rationale block must carry its decision record) is kept, not weakened. Test-file comments that use the design-time ADR names were left, with one clarifying note.
- "hook-enforced" circuit-breaker lines (two sites): now "audit backstop" with the real behavior (`taskMetadata` ships as `audit`; blocks only when set to `block`), and "the same circuit breaker", consistent with P4.T1.1. The QA-local cap of 2 and the artifact-count agreement rule are unchanged.
- Planner write path (A5): the `qa-plan` dispatch description now says not to save a plan under `docs/plans/` and names the two `.cc10x/qa/` artifacts as the only write targets, because `planner.md` step 14 saves to `docs/plans/`. The planner-side text is P4.T5.3 (not done here). The `qa-re-plan` dispatch was not changed (not named by the task).
- Amendment-lane fields: `qa-workflow.md` already states `AMENDED_FILES`, `STALE_SWEEP`, `RECONCILIATION_RERUN` as the pass-2 gate and the policy reference already lists them as planner return fields; no text change was needed. The producer is the planner (P4.T4.4); `planner.md` does not carry them yet.

Not changed, with reason:
- The five `${CLAUDE_PLUGIN_ROOT}` lines in `qa-workflow.md` (R-B11 verdict BROKEN, P4.T1.4b skipped and deferred): untouched.
- B9 "ORIENT names Octocode tools no agent has": that sentence is in `SKILL.md`, not in these references; recorded for T1.5a: reword to tools available in a base install, with optional accelerators named as optional.
- Pointers from `SKILL.md` to the triage and codebase-health references, and hydration prefixes covering both Memory Update tasks, are PENDING in T1.5a (item a). Until then the router still reads the references through the existing route-and-load text. The `[DEBUG-RESET]-equivalent: none` line in the TRIAGE preparation list is a no-op marker mention tied to the `SKILL.md` marker rules (T1.5a).

Why safe: no QA protocol semantics changed (cap of 2, sweep gate, templates, windows, isolation rules); the edits are citations, one backstop label, one dispatch sentence. The Memory Update addition follows the REVIEW graph shape and the existing `memory_sync_gate` ownership (router inline).

Claim boundary: now true: both advisory routes create a Memory Update task and the replay checker requires a finalize for them; no QA citation points at a missing document. Still not claimed: the router's `SKILL.md` has not yet been told about the new tasks (T1.5a); a live run of the `triage-loads-reference` and `qa-seed-template-path` cases was not performed (AD-2, no paid evals).

Pins and fixtures: five new pins (assertion count 285; floor 253 plus additions holds); two pin tokens re-pointed as above; two fixtures extended. No pin deleted.

Classification: `orchestration_sensitive`.

## P4.T1.5a `SKILL.md`, pass 1 of 3: routing and precedence

Findings: B2, B4, B5, B6, B10 (part).

Files: `plugins/cc10x/skills/cc10x-router/SKILL.md` (781 lines before, 781 after); `plugins/cc10x/tools/prompt_clause_assertions.py` (six new pins); `plugins/cc10x/evals/BASELINE.md` (analytical post-P4 note).

What changed:
- (a, B2) Section 5 and section 6 each gain one bullet pointing at `references/triage-workflow.md` and `references/codebase-health-workflow.md` and naming their preparation and task graph blocks; the route-and-load hard rule now lists both references. The hydration bullet states that TRIAGE and CODEBASE-HEALTH create no parent task (their graphs hold an agent task and a Memory Update task only), so resume finds them by the `CC10X triage-agent:` / `CC10X architecture-scanner:` subject or the pending `CC10X Memory Update:` task, scoped by `wf:`, and that ORIENT creates no task. No new subject prefix was added to the parent-task list because no parent task exists for these routes; the Memory Update task is already reconstructed by `wf:` + `kind:memory` in the resume algorithm.
- (b, B4) The routing table is untouched. The opening paragraph keeps one tie-break sentence ("the lower Priority number wins") and adds that the QA, ORIENT and REVIEW cases are applications of the primary-deliverable test, not exceptions. "QA beats REVIEW" became "QA over REVIEW": the deliverable test separates "prove it works" from "tell me what's wrong", so no tie arises. "Prefer ORIENT for help me understand" became: the deliverable decides, and only a genuine tie goes to REVIEW (lower number). That last change makes the rare true tie resolve by the table, where the old text preferred ORIENT; ORIENT stays advisory and read-only either way, so the worst case of a mis-tie is an advisory review instead of an advisory explanation.
- (c, B6) The inline-mode hard-rule bullet that restated "the 3-cycle remediation limit" now points at `### Circuit breaker` in `references/remediation-and-research.md`. The other two SKILL.md mentions (the Cycle row in Loop Discipline and the hard rule near the end) already point at the single definition and carry pins (the 3rd-cycle wording), so they were left. Count semantics are unchanged.
- (d, B10) The `[BUILD-START]` and `[PLAN-START]` marker rules are removed: neither marker is read by any reference, hook or pin (the matching reference text was removed in P4.T1.3). `[DEBUG-RESET]` stays (the debug workflow and the memory skill read it, and a harness check pins it) and `[QA-START]` stays (the QA workflow writes it).
- (b2, B5) One sentence appended to the terse-imperative hard rule: only an explicit user opt-out ("don't use cc10x", "without cc10x", "skip cc10x") skips the router's gates; a small edit still routes as BUILD trivial scope. SKILL.md had no "trivial one-line edit" exemption; the exemption sits in the repo root `CLAUDE.md`, which is not in this file list. Root `CLAUDE.md` wording is a P6 item (P6.T11).

Not changed, with reason (still pending or unassigned):
- Pass 2 (T1.5b): task-tools-optional text, completion wording, claim corrections, the hints-law amendment, the plugin-root resolver, the ORIENT tool-name reword (B9).
- Pass 3 (T1.5c): description and prose items.
- The spike `SKILL_HINTS` sentence (B10): the plan's T1.5a item list (a)-(d), (b2) does not include it, so it was left; it needs an owner (T1.5b, T1.5c or a named T1.5d).
- The `[DEBUG-RESET]-equivalent: none` line in `references/triage-workflow.md`: a reference file outside this task's list; it is now a mention of a marker that SKILL.md no longer defines for TRIAGE (it never did). Left for a reference-file task.
- Parent-task description template in section 6 still lists five `phase:` values for parent tasks; TRIAGE and CODEBASE-HEALTH have no parent, so no change.

Why safe: no routing-table row, gate, workflow graph or contract field changed. The precedence edit restates the existing rule; the only behavior difference is the genuine ORIENT/REVIEW tie, resolved by the table order. `route-precedence` keeps the same four routes by the deliverable test.

Claim boundary: now true: SKILL.md points at both advisory-route references and says how to find those workflows on resume; precedence has one tie-break statement; the breaker count lives in one place plus two pinned pointers; two dead markers are gone; opt-out phrases are the stated sole bypass. Still not claimed: any L2 run (AD-2); that root `CLAUDE.md` agrees (P6).

Pins and fixtures: six new pins (assertion count 291). No existing pin edited, weakened or deleted; no fixture changed. BASELINE.md gains an analytical post-P4 note (no table row changed).

Classification: `orchestration_sensitive`.

## P4.T1.5b `SKILL.md`, pass 2 of 3: task tools, claims, hints law, plugin root

Findings: A3, A4, A6 (router half), B9 (ORIENT), B10 (spike hint), B11.

Files: `plugins/cc10x/skills/cc10x-router/SKILL.md` (781 lines before, 787 after); `plugins/cc10x/tools/prompt_clause_assertions.py` (seven new pins, two existing pins re-pointed); `plugins/cc10x/evals/BASELINE.md` (analytical note).

What changed:
- (e, B11) R-B11 is BROKEN, so item (e) applies. One body line in section 2a: `Plugin root for commands in reference files: ${CLAUDE_PLUGIN_ROOT}; ...`. Claude Code substitutes the variable in the `SKILL.md` body (the existing `cp` command in section 6 relies on the same substitution), so the line resolves to the absolute root. The explanation after the `;` says "plugin-root placeholder" instead of repeating the variable, so it is not substituted into nonsense. A reference command or agent prompt that carries the placeholder means that path. The reference-file lines are untouched (P4.T1.4b stays skipped), so the four pinned QA paths and `cc10x_qa_isolation_guard.py:35` are unchanged.
- (f, A3) New "Task tools are optional" paragraph in section 4: task tools ship only on some models (docs, Task tool availability); the artifact is the source of truth; absent tools take the existing inline fallback (section 12, trigger 1) and resume from the artifact; `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` recommended, `CLAUDE_CODE_TASK_LIST_ID` optional (both variables checked against the env-vars page). Completion text: write agents "may have called" `TaskUpdate`; if the task is still not completed after the contract validates, the router applies the fallback. That is true both while the five agent bodies still say to call it and after P4.T4.5b removes the instruction. The `TaskGet`/`TaskList` state check says to skip when the tools are absent.
- (g, A4) Per-invocation model: the Agent tool has a `model` parameter that outranks frontmatter; the text now says the router passes none, so model selection stays in frontmatter and the table stays advisory. Nothing new is enabled. `TaskOutput` is named deprecated; the check reads the task output file path instead (tools reference). The main-session hard rule no longer says sub-agents cannot spawn: the docs say up to three layers by default, and the rule keeps router-only dispatch and sole ownership of user gates. R-A8: a lead paragraph under "After every agent completion" says a dispatched agent may run in the background and, in auto mode, report through `SubagentHandback`, so the router reads the contract from whichever channel carries it and takes the missing-contract path otherwise. The hook-side reader is a separate P-task (the logger), not done here.
- (j, A6, C4.3) Hints law: "frontmatter `skills:` preloads carry each agent's role-core skills; everything else reaches an agent only through SKILL_HINTS; the router is the only authority that adds situational skills; the router never passes a skill the agent already preloads." True before and after the P4.T4.1 frontmatter pass. The hints list itself is unchanged except the spike line (next bullet).
- (B10, addenda item 2) The spike `SKILL_HINTS` bullet was unreachable: no dispatched agent loads `cc10x:exploration`; the router runs it inline. The bullet now says so, keeps the trigger phrases and the "fresh gated BUILD, not promotion" sentence, and is no longer worded as an include rule.
- (B9) ORIENT procedure names `Glob`, `Grep`, `Read` and the `LSP` tool; the Octocode tools are named as optional accelerators.
- Skeleton claim: now "carries every required key; undecided fields such as `verification_rigor` ship as `null`".

Not changed, with reason: pass 3 items (description, trigger verbs, prose); agent files and frontmatter (P4.T4.1, P4.T4.5b); the Per-role table rows; the logger fix for `SubagentHandback`.

Pins and fixtures: seven new pins (assertion count 298). Two existing pins re-pointed, named per rule 3: "router: main-session rule carries the sub-agent-gates why" (old token: "sub-agents cannot open user gates or spawn the phase agents", now requires "never inside a sub-agent", "only dispatcher of phase agents", "up to three layers") and "router: tier table marked ADVISORY with live rules separated" (two tokens re-worded: "the router does not act on this table" and the per-invocation-model sentence; the two live rules and the `JUST_GO` rule are still required verbatim). No pin deleted, no fixture changed.

Size: `SKILL.md` 787 lines against the 781 budget (+6: resolver paragraph 2, task-tools paragraph 2, handback paragraph 2). Overrun recorded per AD-6; no gate text was trimmed. Pass 3 must land the cumulative count at or under 781 only by tightening prose it owns.

Classification: `orchestration_sensitive`.

Claim boundary: now true: the router tolerates absent task tools, the completion text holds under both ownership models, no stale model/TaskOutput/sub-agent-spawn claim remains, and the plugin-root placeholder has a resolver in the body. Still not claimed: that the resolver makes `qa-seed-template-path` green in a live run (analytical only, AD-2); that agents stop calling `TaskUpdate` (P4.T4.5b); any frontmatter change (P4.T4.1).
