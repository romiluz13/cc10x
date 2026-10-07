# L2 eval baseline

Eight cases under `cases/`. Every status below is an analytical expectation from reading the router at the cited lines. Paths are relative to `plugins/cc10x/`; router paths are under `skills/cc10x-router/`.

## L2 baseline: NOT RUN (no spend authorization, AD-2)

Counts below are analytical expectations, not measurements. To measure, per case, after setting a ceiling (C3.1):

`claude plugin eval plugins/cc10x --case <id> --runs 3 --scaffold --allow-tools Bash Write Edit --ablation none --no-publish --max-cost-usd <ceiling>`

`--allow-tools` is required because file-writing cases cannot pass without Bash/Write/Edit, and `--ablation none` stops the default with-without ablation from doubling spend.

## Prerequisites and run conditions

- Every case except `route-precedence` lists `Agent, TaskCreate, TaskGet, TaskList, TaskUpdate` in its `allowed_tools`: a run only gets the tools listed, and without them the router falls back to inline mode (`SKILL.md` section 12, "Enter inline mode when EITHER trigger holds") and the dispatch graph analysed below is never produced. `route-precedence` only decides routes and creates no tasks, so it stays dispatch-free.
- The expectations for `build-multiphase-memory-finalize`, `remfix-gate-producer` and `seam-gate` depend on the Task tools being present: inline mode creates no REM-FIX task (so `REMFIX_COUNT=0`, red for a different reason) and no builder Router Contract (so `seam-gate` has nothing to copy). On a harness or model where the Task tools are not on by default, `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` would have to be in the child environment, but a case's `env` frontmatter accepts only `EVAL_*` keys, so it cannot be set from the case. Treat such a run as possibly inline: check the trace for `TaskCreate` before comparing counts, and record that the case ran inline rather than reading its count as a regression or a P4 flip.
- Whether subagents dispatched by `Agent` inherit `allowed_tools` or use their own agent definitions is not documented in the recorded schema; the file-writing results depend on it.
- `fixture.sh` scripts use `git init -b main`, which needs git 2.28 or newer.

## Per-case expectations

| case id | finding guarded | expected status at baseline (by analysis) | owning P4 task |
| --- | --- | --- | --- |
| `build-trivial-happy` | trivial-build (no finding; regression guard) | green: `references/build-workflow.md:92` reduced graph builder, verifier, memory is the documented trivial path | none (stays green) |
| `build-multiphase-memory-finalize` | B3 | red (needs Task tools): `references/build-workflow.md:82-84` ("one approved executable phase at a time") and `:126-164` define a single-phase graph whose phase 1 `memory-finalize` task (`:163-164`) becomes runnable once that phase's verifier completes and the router runs memory tasks inline when runnable (`SKILL.md:584-590`); `SKILL.md:607,641` gate only phase advance, no next-phase graph rule or once-per-workflow Memory Update rule | P4.T1.3 |
| `triage-loads-reference` | B2 | red: `SKILL.md` has no pointer to `references/triage-workflow.md` (grep for `triage-workflow` finds zero hits); the TRIAGE route (`:28`, `:39`) says what triage does but not where its task graph lives, `:147` hydration prefixes list BUILD, DEBUG, REVIEW, PLAN, QA only, and the parent-task description template at `:262` lists `phase:{build\|debug\|review\|plan\|qa}` without triage (the `phase:` enum at `:120` and `:278` does include it), so a run reaches the reference only by luck | P4.T1.4, P4.T1.5a |
| `remfix-gate-producer` | B1 | red (needs Task tools): the re-review precondition gate (`references/remediation-and-research.md:355-364`, fields `:358-360`, fail-closed `:364`, applied from `SKILL.md:564`) demands `COVERING_TESTS`, `TEST_COMMAND`, `TEST_OUTPUT`, but no file under `agents/` names them and there is no REM-FIX `TaskCreate` template, so no fix agent is told to emit them. The prompt asks the run to copy the REM-FIX proof section verbatim without naming the fields, so a producer instruction missing from the router shows up as missing fields. Probabilistic: the run must also produce a HIGH finding | P4.T1.1, P4.T4.2 |
| `two-workflow-resume` | scoped-resume | green: `SKILL.md:148` scopes resume by `wf:` marker, and the prompt names `alpha.txt`, so the router picks the alpha workflow by request text. This is a regression guard, not a B14 red case: B14 (hooks resolve the newest-mtime artifact, `scripts/cc10x_hooklib.py:105-119`, used by `scripts/cc10x_qa_isolation_guard.py:491`) is not observable by the graders, because the first router write makes alpha the newest file. B14 stays an L1/hook-level finding owned by P5.T5 | none (stays green; B14 owned by P5.T5) |
| `qa-seed-template-path` | B11 | red: `references/qa-workflow.md:140` and `:465` run `cp` from a literal plugin-root variable path in a Bash command; the P1.T6 spike (R-B11) measured the variable empty in the Bash tool, and 6 of 6 first attempts emitted the literal variable and failed with the empty-prefix error (`/templates/qa-...`) | P4.T1.5b item (e); contingency P4.T1.4b |
| `route-precedence` | B4 | green: `SKILL.md:19` primary-deliverable rule plus `:35-38` and `:55` already resolve the four phrasings (REVIEW advisory, ORIENT over REVIEW, QA over REVIEW and BUILD, ERROR over BUILD) in the intended direction; B4 is a wording inconsistency, so this is a regression guard for the rewrite | P4.T1.5a (must stay green) |
| `seam-gate` | C9 | green: `agents/component-builder.md:60-71` sets `confirmed` when the plan supplies `test_seams` (`references/build-workflow.md:63`), and the contract carries `TEST_SEAMS` and `SEAM_GATE_STATUS` (`agents/component-builder.md:132-133`). Moderate confidence, and it needs the Task tools: the builder's Router Contract exists only when the builder is dispatched, and the plan names its seam in a `### Test Seams` subsection that the router must normalize into the phase's `test_seams` | none (stays green) |

Red cases: 4 of 8 (B1, B2, B3, B11). Green regression guards: 4 of 8. Each red case maps to the P4 task above; no case is red without an owner.

## Pass rule proposal (C3.1, unanswered)

- An L2 case passes when at least 2 of 3 runs pass; one automatic re-run of a failing case before it counts.
- An L1 replay fixture passes at 100%.
- "No regression" in P4, P7 and P8 means no case drops below its baseline count.
- Spend ceiling and L2 go/no-go remain with the user (C3.1); without them P7 stays no-go.

## L1 baseline (measured at the P3-b tree)

- Replay fixtures: `fixtures=32` (28 existing plus the four shape fixtures from P3.T2).
- Pytest: 379 passed (`plugins/cc10x/scripts`, 59 of them structural eval-case checks).
- Prompt clause assertions: 259 passed.

## Post-P4 analytical expectations (read from the edited text; no L2 run, AD-2)

- After P4.T1.5a: `triage-loads-reference` (B2) is expected to flip red to green. `SKILL.md` section 5 and section 6 now point at `references/triage-workflow.md` and `references/codebase-health-workflow.md`, the route-and-load hard rule names both, and the hydration bullet says TRIAGE and CODEBASE-HEALTH create no parent task. This is a reading of the text, not a measured run.
- After P4.T1.5a: `route-precedence` (B4) is expected to stay green. The routing table rows are byte-identical; the rewritten sentences give the same four routes (R1 REVIEW, R2 ORIENT, R3 QA, R4 DEBUG) because the primary-deliverable test decides each one and none of them is a genuine tie. Line anchors cited above for `SKILL.md:19` and `:55` still hold; later `SKILL.md` line numbers in the baseline table are baseline-time numbers.
- After P4.T1.5b: `qa-seed-template-path` (B11) is expected to flip red to green, analytical only (no L2 run, AD-2). `SKILL.md` section 2a now carries one body line that Claude Code substitutes to the absolute plugin root and that tells the router a literal plugin-root placeholder in `references/qa-workflow.md:140` or `:465` means that path, so the seeding `cp` should no longer start with the empty prefix measured in R-B11. The reference lines are unchanged; if a live run still fails, contingency P4.T1.4b applies.
- After P4.T1.5b: `build-trivial-happy` and `two-workflow-resume` are expected to stay green; the task-tools-optional paragraph and the "may have called" completion wording add a fallback path and do not change the tools-present path.

## post-P4A expected (analytical, not measured)

Read from the router text and references as they stand after P4.T1.6 (`SKILL.md` 781 lines). No L2 run was made (AD-2): this column states what the edited text should produce, never a measurement. "Needs Task tools" carries over from the prerequisites above.

| case id | baseline (analytical) | post-P4A expected (analytical, not measured) | reason (edited text) |
| --- | --- | --- | --- |
| build-trivial-happy | green | green | the reduced graph is unchanged; T1.5b added a task-tools-absent fallback and "may have called" completion wording that do not alter the tools-present path |
| build-multiphase-memory-finalize | red (needs Task tools) | green (needs Task tools) | P4.T1.3 added `#### Multi-phase iteration` in `build-workflow.md` (next graph only after `phase_exit_gate`; one Memory Update after the last phase), written to match the `multi-phase-memory-finalize` fixture |
| triage-loads-reference | red | green | P4.T1.4 added the Memory Update task to the TRIAGE graph; P4.T1.5a added the route-and-load pointers and the hydration bullet for the advisory routes |
| remfix-gate-producer | red (needs Task tools) | green with lower confidence (needs Task tools; probabilistic) | P4.T1.1 added the REM-FIX `TaskCreate` template and named the producers of `COVERING_TESTS`/`TEST_COMMAND`/`TEST_OUTPUT`; the agent contracts themselves still do not carry the fields until P4.T4.2, so a run that ignores the template can still miss them |
| two-workflow-resume | green | green | resume scoping by `wf:` is unchanged; the task-tools-optional paragraph only adds an artifact-based path when the tools are absent |
| qa-seed-template-path | red | green with lower confidence | P4.T1.5b item (e): one body line resolves the plugin-root placeholder for reference commands; the reference lines are unchanged (P4.T1.4b skipped), so a live run could still fail and would then trigger that contingency |
| route-precedence | green | green | routing-table rows are byte-identical; precedence has one tie-break statement; T1.5c changed only the description wording and prose, not routing |
| seam-gate | green | green (needs Task tools) | no change in this sub-phase touches the builder contract or the seam text |

Flips expected: 4 red cases (B1, B2, B3, B11) to green by reading; none stays red without a recorded reason (B1 and B11 keep a lower-confidence note). B4 stays green; B14 wording is not part of these cases (owned by P5.T5).

Trigger sanity (T1.5c): the router `description` keeps every trigger verb, so activation is expected to be unchanged. Over-triggering is NOT assessed: no trigger eval was run.

## post-P4A remediation 1 expected (analytical, not measured)

Read from the router text and references after the P4A remediation 1 commits (`SKILL.md` 785 lines). Still no L2 run (AD-2). Only the cases the remediation touches are restated.

| case id | post-P4A | post-remediation 1 (analytical, not measured) | reason (edited text) |
| --- | --- | --- | --- |
| build-trivial-happy | green | green | the reduced graph is unchanged; with Task tools absent the router now dispatches the builder and verifier through the Agent tool (artifact-only graph mode) instead of running them inline |
| build-multiphase-memory-finalize | green (needs Task tools) | green (needs Task tools) | the next phase's builder now waits for the previous phase's last task (doc-sync, else verifier); the replay fixture and its mutation tests pin the ordering; the Memory Update exception is also stated at both graph templates |
| two-workflow-resume | green | green | `wf:` scoping unchanged; artifact-only resume scopes by the named `workflow_uuid` or `user_request`, never by modification time alone |
| remfix-gate-producer | green with lower confidence | green with lower confidence | the producers of the gate fields are now named per agent in the router; the agent files still do not declare them (P4B), so the gates fail closed until then |
| qa-seed-template-path | green with lower confidence | green with lower confidence | the plugin-root line now claims only that reference files read through Read arrive with the placeholder literal; the reference lines are still `qa-workflow.md:140` and `:465` |
| triage-loads-reference | green | green | Memory Update is now created only at the terminal state; the pointers and graphs are unchanged otherwise |

Measured in this remediation: replay fixtures `fixtures=34` (two new paused-advisory fixtures), pytest and prompt clause counts are in the prompt change record. No red case newly appears by reading.

## Visibility

Every tracked path under `evals/cases/` and this file must report `git check-ignore -q` exit 1; `evals/results/x.json` must report exit 0. Grader file names avoid the substrings `test` and `audit` because `.gitignore` globs `*test*.md` and `*audit*.md` would silently untrack them.
