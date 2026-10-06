# L2 eval baseline

Eight cases under `cases/`. Every status below is an analytical expectation from reading the router at the cited lines. Paths are relative to `plugins/cc10x/`; router paths are under `skills/cc10x-router/`.

## L2 baseline: NOT RUN (no spend authorization, AD-2)

Counts below are analytical expectations, not measurements. To measure: run `claude plugin eval plugins/cc10x --case <id> --runs 3 --scaffold --no-publish --max-cost-usd <ceiling>` after setting a ceiling (C3.1).

## Per-case expectations

| case id | finding guarded | expected status at baseline (by analysis) | owning P4 task |
| --- | --- | --- | --- |
| `build-trivial-happy` | trivial-build (no finding; regression guard) | green: `references/build-workflow.md:92` reduced graph builder, verifier, memory is the documented trivial path | none (stays green) |
| `build-multiphase-memory-finalize` | B3 | red: `references/build-workflow.md:82` ("one approved executable phase at a time") and `:128-164` define a single-phase graph whose phase 1 `memory-finalize` task (`:164`) can finalize after phase 1; `SKILL.md:607,641` gate only phase advance, no next-phase graph rule or once-per-workflow Memory Update rule | P4.T1.3 |
| `triage-loads-reference` | B2 | red: `SKILL.md` has no pointer to `references/triage-workflow.md` (grep finds zero hits); `SKILL.md:147` hydration prefixes list BUILD, DEBUG, REVIEW, PLAN, QA only and the artifact `phase:` enum at `SKILL.md:262` omits triage, so a run reaches the reference only by luck | P4.T1.4, P4.T1.5a |
| `remfix-gate-producer` | B1 | red: the re-review precondition gate (`references/remediation-and-research.md:204`, `:355`; `SKILL.md:565`) demands `COVERING_TESTS`, `TEST_COMMAND`, `TEST_OUTPUT`, but no file under `agents/` names them and there is no REM-FIX `TaskCreate` template, so no fix agent is told to emit them. Probabilistic: the run must also produce a HIGH finding | P4.T1.1, P4.T4.2 |
| `two-workflow-resume` | B14 | red: `SKILL.md:147-148` scopes resume by `wf:` marker, but hooks resolve the newest-mtime artifact (`scripts/cc10x_hooklib.py:105-123`, used by `scripts/cc10x_qa_isolation_guard.py:491`), so the newer unrelated workflow is what hooks see. The router-side wording is the part P4 fixes; the hook change is P5.T5 | P4.T1.2 (wording), P5.T5 (hook) |
| `qa-seed-template-path` | B11 | red: `references/qa-workflow.md:140` and `:464` run `cp` from a literal plugin-root variable path in a Bash command; the P1.T6 spike (R-B11, local note `.cc10x/anchors/P1-spikes.md`) measured the variable empty in the Bash tool and 6 of 6 first attempts failing with an empty-prefix path | P4.T1.5b item (e); contingency P4.T1.4b |
| `route-precedence` | B4 | green: `SKILL.md:19` primary-deliverable rule plus `:35-38` and `:55` already resolve the four phrasings (REVIEW advisory, ORIENT over REVIEW, QA over REVIEW and BUILD, ERROR over BUILD) in the intended direction; B4 is a wording inconsistency, so this is a regression guard for the rewrite | P4.T1.5a (must stay green) |
| `seam-gate` | C9 | green: `agents/component-builder.md:60-71` sets `confirmed` when the plan supplies `test_seams` (`references/build-workflow.md:63`), and the contract carries `TEST_SEAMS` and `SEAM_GATE_STATUS` (`:133`). Moderate confidence: depends on the builder's contract being readable by the run | none (stays green) |

Red cases: 5 of 8 (B1, B2, B3, B11, B14). Green regression guards: 3 of 8. Each red case maps to the P4 task above; no case is red without an owner.

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
