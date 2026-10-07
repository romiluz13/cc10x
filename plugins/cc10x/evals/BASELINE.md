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
| `qa-seed-template-path` | B11 | red: `references/qa-workflow.md:140` and `:464` run `cp` from a literal plugin-root variable path in a Bash command; the P1.T6 spike (R-B11) measured the variable empty in the Bash tool, and 6 of 6 first attempts emitted the literal variable and failed with the empty-prefix error (`/templates/qa-...`) | P4.T1.5b item (e); contingency P4.T1.4b |
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

## Visibility

Every tracked path under `evals/cases/` and this file must report `git check-ignore -q` exit 1; `evals/results/x.json` must report exit 0. Grader file names avoid the substrings `test` and `audit` because `.gitignore` globs `*test*.md` and `*audit*.md` would silently untrack them.
