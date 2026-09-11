# QA Report: {feature}

**Verdict:** PASS | FAIL | BLOCKED
**Run:** {iso_ts} · **Environment:** {env_mode} · **Duration:** {seconds}s
**Workflow:** `wf:{workflow_uuid}` · **Test plan:** `.cc10x/qa/{workflow_uuid}/test-plan.md`

> **This file records what the run OBSERVED. A claim it cannot point at evidence for does not go in.**
>
> The test plan is a prediction of what will be exercised; this is the account of what was. Where
> they disagree, this file is right and the plan is the thing that was wrong — say so in
> `## Coverage gaps` rather than quietly narrowing the plan to match the run.
>
> **Sections are not optional when empty.** A section omitted because it had nothing in it reads as
> a section that was considered and came back clean, and those are not the same claim. Every heading
> below stays, with `None` under it if that is the truth.

---

## 1. Failure classes

<!-- FIRST section, and mandatory even when every count is zero. A reader who cannot see that zero
     checks failed for want of an input cannot tell a clean run from an unexamined one. Every count
     in the executor's FAILURE_CLASS_COUNTS gets a row here, zeros included — this is a table of the
     counts the contract emits, not a fixed list, so a count added to the contract appears here
     without this template having to change. -->

| Class | Count |
| ----- | ----- |
| missing-input | |
| wrong-guess | |
| defect | |
| unconfirmed | |

<!-- `unconfirmed` is not a fourth failure class. It is the severity floor a stale measurement
     baseline imposes, and it says how much of the red below rests on a revision nobody re-checked.
     A confidence floor, never an impact level. -->

**What the counts mean here:** <!-- one or two sentences. If all four are zero, say what that does
and does not establish, because a reader who takes `defect: 0` as the headline may have read the
opposite of what the run found. -->

## 2. Summary

| Tier | Total | Passed | Failed | Blocked | Flaky |
| ---- | ----- | ------ | ------ | ------- | ----- |
| | | | | | |

<!-- Blocked scenarios are not passes. The verdict cannot be PASS while any scenario is blocked. -->

## 3. Scenario results

<!-- One block per scenario in the test plan. A scenario the plan named and this run did not reach
     still gets a block here, marked BLOCKED with the reason — dropping it from the list is how a
     coverage hole becomes invisible. -->

### {scenario} — PASS | FAIL | BLOCKED

**Class:** happy-path | error-handling | edge-case
**Command:** `{exact command, runnable as written}`
**Exit code:** {n}

| Observation point | Expected | Actual | Result |
| ----------------- | -------- | ------ | ------ |
| UI | | | |
| API | | | |
| DB | | | |
| Queue | | | |
| Logs | | | |

<!-- Every observation point the plan named is asserted, or the scenario is not PASS. An
     unasserted point is a hole in the proof, not a detail. -->

**Stub reach:** <!-- `none`, or name each stub this scenario's verdict depended on. A scenario whose
green rests on a stub derived from the traced repo's own belief about the wire is `unproven by
stub`: such a stub cannot disagree with the repo it came from, so it cannot fail. Say so here and
carry it into §7. -->

## 4. Failures

<!-- Per failure: what broke, the evidence, and the narrowest repro that reproduces it. A bug report
     a debugger cannot start from is noise. `None` if the run had none. -->

### {failure}

**Failure class:** missing-input | wrong-guess | defect
**Severity:** critical | high | medium | low | unconfirmed
**Measured on:** <!-- per repo the finding spans: branch, short sha, commits_behind, dirty y/n.
                     MEASURED at report time, never copied from setup.md. -->
**Siblings swept:** <!-- the set you compared against, and a finding for every member you listed. -->
**Siblings swept — branch axis:** <!-- required when the defect IS a cross-repo
contract mismatch: the reading on BOTH repos' default branches, not just the checked-out
one. A cross-repo mismatch reported from one side is invalid output. `n/a` otherwise. -->
**Sibling set:** <!-- the set_name you compared within. A defect with no sibling set says
so here rather than leaving the field off. -->
**Env setup:** `{command that brings the environment to the reproducing state}`
**Repro:** `{command, runnable as written}`
**Evidence:** <!-- exact output, log line, or diff. Quote it; do not summarise it. -->

## 5. Harness issues

<!-- Defects in the TEST SYSTEM, not the product: a teardown that ignores its own exit
     code, a fixture that leaks between scenarios, an assertion that cannot fail. These
     are kept apart from §4 because they say something different — a harness issue means
     the run's own evidence is weaker than it looks, and it is what sends the workflow
     back to qa-build rather than to DEBUG. `None` if the harness held. -->

| Issue | What it undermines | Rebuild needed |
| ----- | ------------------ | -------------- |
| | | |

## 6. Environment

<!-- What was provisioned, what was stubbed, readiness times, and the teardown result. A leaked
     container or a surviving volume is stated here even when every scenario passed. -->

| Fact | Value |
| ---- | ----- |
| Services provisioned | |
| Services stubbed | |
| Readiness wait | |
| Teardown status | clean \| leaked |
| Teardown evidence | <!-- what was CHECKED and what it showed, not "teardown ran" --> |
| Leaked resources | <!-- `None`, or name each one. A leak forces FAIL even if every scenario passed, so an unnamed leak is an unexplained FAIL. --> |
| Product code touched | false <!-- any other value invalidates the run --> |
| Test code touched | false <!-- any other value invalidates the run --> |

## 7. Coverage gaps

<!-- Mandatory, even when empty. A report that lists only what ran reads as complete coverage;
     naming what did not run is how the reader prices the PASS.
     Three things belong here: what the plan named and this run could not exercise; what no test
     could have caught given the harness built; and every scenario marked `unproven by stub` in §3,
     restated so a reader of this section alone can see it. -->

| Gap | Why it was not covered | What would close it |
| --- | ---------------------- | ------------------- |
| | | |

## 8. Bug candidates

<!-- The machine-readable handoff to DEBUG, one entry per candidate, matching the executor's
     BUG_CANDIDATES contract. `None` if the run produced none. -->
