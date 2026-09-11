#!/usr/bin/env python3
"""Self-contained invariant tests for the QA route's phase sets.

No framework. Run:  python3 test_cc10x_qa_phase_invariants.py   (exit 0 = pass)

Why this file exists
--------------------
`qa-preflight` provisions and probes the real environment. If it ever lands in
`cc10x_qa_isolation_guard.PLAN_PHASES`, the guard blocks the phase from doing
the only thing it exists to do — and the failure is silent and total: nothing
prints, and the edit *looks* like a strengthening of the plan-phase read-only
guarantee. Prose cannot prevent that. These assertions can.

The behavioural half (PP-6) is the part that matters most: it invokes the guard
as a subprocess against synthesized workflow artifacts, so it proves what the
guard DOES rather than what its constants say.

Properties
----------
PP-1  "qa-preflight" is NOT in PLAN_PHASES
PP-2  no existing plan phase was lost from PLAN_PHASES
PP-3  PLAN_PHASES and PROVISIONING_PHASES are disjoint
PP-4  every phase: token in qa-workflow.md appears in the SKILL.md §3 enum
PP-5  every DISPATCHABLE QA phase in the §3 enum has exactly one §7 dispatcher row
PP-6  the guard denies at qa-plan, denies at the bare parent "qa", allows at
      qa-preflight, and allows via the status_history[-1].phase fallback
PP-9  every §N reference resolves to a real "## N." heading in the file its
      citation prefix names
PP-10(a) no block of the router state machine writes planning_review_status=
      passed without BOTH `plan_revision` and `last_reviewed_revision` in the
      SAME block, and the whole-file count of `passed` writes equals the number
      of guarded blocks (the out-of-block escape the per-block loop never visits)
PP-10(b) the two AUTHORING RULES (a) is structurally blind to: every `When ...:`
      heading is BARE, and no heading carries a `passed` literal. Both defects
      were injected live and left (a) green; see the note below.
PP-11 `revised_after_review` is REACHABLE: planner.md still declares it in the
      PLANNING_REVIEW_STATUS enum AND remediation-and-research.md contains at
      least one write site. The enum alone is exactly the bug this catches.
PP-12 the byte-duplicated harness PASS rule agrees with itself: each of
      {assertion_falsified, survived, LIVENESS_PROBES} appears in BOTH
      qa-harness-builder.md and workflow-artifact-and-hook-policy.md
PP-13 the artifact guard ENFORCES revision consistency behaviourally and does
      not brick legacy artifacts: four synthesized artifacts, one at a time,
      guard invoked as a subprocess in `artifactIntegrity: block` mode
PP-16 every dispatch-metadata value the route law WRITES is a member of the
      enum the route law DECLARES: (a) every concrete `origin:<value>` in
      SKILL.md and references/*.md is in the SKILL.md origin enum; (b) every
      `phase:<value>` in plan-workflow.md is in the SKILL.md phase enum.
      PP-4 already does (b) for qa-workflow.md only; plan-workflow.md was
      unguarded, and NOTHING checked the origin enum at all.
PP-18 the measure-before-you-ask law holds and is NORMATIVE, in three parts:
      (a) step 0a itself carries both halves of the rule -- checked inside the
      0a window, because the phrase is deliberately repeated in 0b and a
      whole-file test is satisfied by the copy; (b) step 0b is a unique
      line-anchored block that PRECEDES the research fan-out and still has its
      operative body -- present/confirm/dispatch-after and its own
      non-deferrability clause, because an ordering proof says nothing about
      whether the gate still has content; (c) the lane-split paragraph routes
      through 0b and neither it nor the paragraph after it defers to a gate in
      qa-plan, which runs after the lanes it would govern.
      Every assertion runs over a NORMALISED copy with HTML comments and fenced
      blocks removed: a law inside <!-- --> is not law, and the first draft of
      this property was green with the whole rule commented out.
PP-19 the report is produced by a TEMPLATE ON DISK like the other four QA
      artifacts, not by a shape described in a prompt: (a) qa-report.template.md
      still leads with the `## 1. Failure classes` block the executor's
      reconciliation rule cites, carrying a row for every value that rule
      reconciles; (b) REACH, asserted per duty -- the law must CP the template
      into place and the agent must NAME it. A template nothing copies is worse
      than no template: it looks like a governed artifact while governing
      nothing.

Negative control (run and recorded when this file was written): temporarily
adding "qa-preflight" to PLAN_PHASES turns PP-1, PP-3 and PP-6 case (c) red.
A test never observed failing is unproven.

Negative control for PP-12 (run and recorded when PP-12 was added): deleting the
token `survived` from the `qa-harness-builder` row of
workflow-artifact-and-hook-policy.md ONLY, leaving qa-harness-builder.md intact,
turns PP-12 red naming `survived` and naming the hook-policy file. That is the
byte-duplication trap in the exact direction it historically drifts.

Negative control for PP-10 and PP-11 (four runs, recorded when they were added):
  (a) deleting the `last_reviewed_revision = plan_revision` precondition line from
      the pass-2 PASS block ONLY, leaving pass 1 guarded, turns PP-10 red naming
      the pass-2 block and only that block. It proves the loop visits EVERY
      block, not just the first one that matches.
      The precondition must be the SOLE carrier of both revision literals. An
      earlier draft also repeated `plan_revision == last_reviewed_revision` on
      the `passed` line itself; this injection was then GREEN, because the line
      the injection deletes was not the only line carrying the literals. A
      per-block content assertion is only as strong as the uniqueness of the
      text it looks for.
  (b) a stray `- Set planning_review_status=passed` in the PROLOGUE, before the
      first `When ...:` heading, turns PP-10 red on the COUNT RECONCILIATION
      clause specifically (2 guarded, 3 whole-file). This is the out-of-block
      escape the per-block loop cannot see. Note that appending the same line at
      END of file does NOT exercise this clause: EOF is inside the last block,
      so the write is counted on both sides and the per-block half fires instead.
  (c) deleting the single `planning_review_status=revised_after_review` write
      site, leaving planner.md's enum intact, turns PP-11 red. This reproduces
      VERBATIM the state of the repo before this property existed: a declared
      enum value no transition could ever produce.
  (d) removing `revised_after_review` from planner.md's PLANNING_REVIEW_STATUS
      enum, leaving the write site intact, turns PP-11 red on the other half.
      Both halves are asserted independently; either alone is satisfiable by a
      state machine that is half-wired.

What PP-10(a) does not catch, and why PP-10(b) exists. Two heading defects are
invisible to (a), both real — both were made in a draft of the change that added
the amendment block, and BOTH left the suite exit 0 when injected:
  - a heading that is not BARE (`> **When ...`) is not a block boundary at all.
    The orphaned body folds into the block ABOVE, which is already guarded, so
    (a) stays green while the guard is applied to the wrong transition.
  - a `planning_review_status=passed` literal in the HEADING of a block whose
    body already carries both revision literals is counted on BOTH sides of the
    reconciliation (whole-file +1, guarded-block +1), so the counts agree and
    (a) stays green.
Until PP-10(b) these were enforced only by two one-shot greps in one phase's
checklist, which is not a durable guard. They are now a property.

Negative control for PP-10(b) (three runs, recorded when it was added; the third
is the one that matters and the first two are kept because they show how easy it
is to write an injection that proves less than it appears to):
  (i)   dressing the amendment heading as `> **When ...:**` turns PP-10(b) red on
        RULE 2 naming line 135, while PP-10(a) stays GREEN at 9 blocks. This is
        B2's first defect, caught.
  (ii)  adding ` and planning_review_status=passed` to the pass-2 PASS heading
        turns (b) red on RULE 1 — but ALSO turns (a) red on the count
        reconciliation (3 whole-file vs 2 guarded), because that block already
        contained a `passed` write, so the heading match lifts only one side.
        The same literal appended to the pass-2 FINDINGS heading turns (a) red on
        the PER-BLOCK half instead, because that block carries no revision
        literals. Neither run demonstrates the blind spot.
  (iii) the literal in the AMENDMENT block's heading — a block with both revision
        literals in its body and no other `passed` write — turns (b) red on RULE 1
        with (a) GREEN at 3 guarded / 3 whole-file. That is the blind spot exactly,
        and it is the only one of the three that shows it.

Negative control for PP-13 (two runs, recorded when it was added):
  (a) inverting the guard's comparison (`!=` -> `==`) turns PP-13(a) AND PP-13(b)
      red together. An inverted comparison breaks in both directions, which is
      stronger evidence than either case alone.
  (d) adding `plan_revision` and `last_reviewed_revision` to the guard's
      REQUIRED_WORKFLOW_KEYS turns PP-13(d) ONLY red, with `missing-keys:` in the
      blocking message. This is the backward-compatibility hazard made mechanical:
      it is the single most damaging way to get this change wrong, and it is now
      caught by a test rather than by an incident on a legacy artifact.

Negative control for PP-18 (eight constructions, all run against the SHIPPED
form and all red; seven of the eight were GREEN against an earlier draft of this
same property, which is why each defence exists):
  I-1 0a rule deleted from step 0a and re-parked verbatim at EOF inside a ```text
      fence                                                  -> (a) red
  I-2 only the bold "Never ask..." sentence deleted from 0a, leaving 0b's copy of
      "came back empty" to satisfy the other token           -> (a) red
  I-3 gate block moved to sit AFTER "#### Research fan-out" with a forward
      reference left at the old offset to capture find()     -> (b) red
  I-4 the 0a bullet and the whole 0b block wrapped in <!-- --> so every byte of
      the law is present but non-normative                   -> (a)+(b) red
  I-5 0b gutted to a bare heading, its whole operative body deleted -- position
      preserved, gate gone                                   -> (b) red
  I-6 deferral reworded to "the environment topology checkpoint in `qa-plan`" to
      dodge the literal token                                -> (c) red
  I-7 deferral left out of the split paragraph and placed in the FOLLOWING one
                                                             -> (c) red
  I-8 `unproven by stub` removed from the test-plan template, leaving the duty
      stated only in the law that imposes it                 -> (d) red
Only I-3 and I-6/I-7 were red against the first draft. I-1, I-2, I-4, I-5 and I-8
all shipped GREEN there: the first draft tested whole-file substrings and two
offsets, which proves a label exists somewhere, not that a gate is in force.

Negative controls for PP-19 (six runs, recorded when PP-19 was added). Before the
template existed the shape lived in the agent prompt, and deleting the block whole
with the rule that cites it left standing was GREEN at 29/29 -- the same shape as a
gate placed after the work it governs:
  I-9  the heading deleted from the template   -> (a) red: not a heading
  I-10 the `defect` row removed                -> (a) red: no `| defect |` row
  I-11 the block moved below `## 2. Summary` -- position is load-bearing, since a
       zero count read after the scenario table is a footnote, not the frame
                                               -> (a) red: not first
  I-12 the `cp` deleted from the law, dispatch text still claiming the file was
       seeded from the template                -> (b) red
  I-13 the template pointer removed from the agent -> (b) red
  I-14 the template file deleted outright      -> (a) red: does not exist
I-12 is why (b) asserts the COPY and not the filename. The first draft of (b)
tested whether each file MENTIONED the template, and I-12 shipped GREEN against it:
the dispatch text still said report.md "has been seeded from" a template that
nothing put on disk. A name is not a mechanism.

Negative control for PP-16 (three runs, recorded when PP-16 was added; all three
are mandatory because a set-membership assertion has a vacuity shape the token
checks do not):
  (a) rewriting one `origin:router` in qa-workflow.md to `origin:qa-plumber`
      turns PP-16 red naming `qa-plumber` and the origin half. A plausible
      out-of-enum origin is the exact direction this drifts.
  (b) rewriting one `phase:plan-review-gap-1` in plan-workflow.md to
      `phase:plan-review-amend` turns PP-16 red naming `plan-review-amend` and
      the phase half. The NEAR-MISS spelling also proves the check is
      exact-match rather than prefix-match.
  (c) breaking the extraction regexes so they match nothing (`origin=` /
      `phase=` instead of `origin:` / `phase:`) turns PP-16 red on the
      len(found) >= N PRECONDITION, not on membership. An empty extracted set
      must fail loudly instead of passing trivially — that is the whole reason
      the precondition is asserted first.
"""

import importlib.util
import json
import re
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
PLUGIN = SCRIPTS.parent
GUARD = SCRIPTS / "cc10x_qa_isolation_guard.py"
ROUTER = PLUGIN / "skills" / "cc10x-router"
QA_WORKFLOW = ROUTER / "references" / "qa-workflow.md"
SKILL_MD = ROUTER / "SKILL.md"
ENV_PLAN_TPL = PLUGIN / "templates" / "qa-env-plan.template.md"
HARNESS_AGENT = PLUGIN / "agents" / "qa-harness-builder.md"
HOOK_POLICY = ROUTER / "references" / "workflow-artifact-and-hook-policy.md"
PLAN_WORKFLOW = ROUTER / "references" / "plan-workflow.md"
REMEDIATION = ROUTER / "references" / "remediation-and-research.md"
PLANNER_AGENT = PLUGIN / "agents" / "planner.md"
ARTIFACT_GUARD = SCRIPTS / "cc10x_posttooluse_artifact_guard.py"
SKELETON = ROUTER / "references" / "workflow-artifact.skeleton.json"
REFERENCES = ROUTER / "references"

# PP-16 anti-vacuity floors. These are LIVE BASELINES, counted against the tree
# at the moment PP-16 was written, not aspirational minima:
#   origins: {router, bug-investigator, code-reviewer, integration-verifier}
#   phases in plan-workflow.md: {plan-create, plan-review-gap-1, re-plan,
#                                plan-review-gap-2, memory-finalize}
# A membership assertion over an EMPTY set passes trivially, so the extraction
# must be proven to still extract before the membership question is asked.
PP16_MIN_ORIGINS = 4
PP16_MIN_PHASES = 5

# PP-12. One token per structural property of the mutation schema:
# assertion_falsified = the only outcome that satisfies the floor,
# survived            = the automatic-FAIL outcome,
# LIVENESS_PROBES     = the separate list that cannot satisfy the floor.
# A restatement missing any one of them permits a verdict the other site forbids.
MUTATION_PASS_TOKENS = ("assertion_falsified", "survived", "LIVENESS_PROBES")

# PP-12(b). The SHAPE tokens above say nothing about the floor's MAGNITUDE, and
# that blindness is how the two byte-duplicated PASS rules came to disagree by a
# factor of n with the suite green. One token per branch of the floor selector:
#   per provable property        = branch 1's unit
#   At risk of appearing proven  = branch 2's self-flag
#   per tier and per wave        = branch 3's fallback unit
#   both, not either             = the conjunction branch 3 turns on; a bare
#                                  "both" would match anywhere and be vacuous.
MUTATION_FLOOR_MAGNITUDE_TOKENS = (
    "per provable property",
    "At risk of appearing proven",
    "per tier and per wave",
    "both, not either",
)

# PP-14. The wording law forbids a bare `reviewed`/`approved` in a plan header,
# and our own QA test-plan template offered exactly that. Asserted on the SINGLE
# anchored `**Status:**` line, never a whole-file search: the word "approved"
# appears in ordinary prose elsewhere in this template and a file-wide search
# would be satisfied by it, masking the defect the property exists to catch.
# The qualifier is `@r` because that is the notation P9 step 5 actually writes
# (`reviewed@r{n}`); a property that guards a notation it does not match is
# untestable against its own target.
QA_TEST_PLAN_TPL = PLUGIN / "templates" / "qa-test-plan.template.md"
PP14_STATUS_LINE = re.compile(r"^\*\*Status:\*\*")
PP14_UNQUALIFIED = re.compile(r"\b(?:reviewed|approved)\b")
PP14_QUALIFIER = "@r"

EXECUTOR_AGENT = PLUGIN / "agents" / "qa-executor.md"

# PP-19. The report is produced by a template on disk, like the other four QA
# artifacts, and not by a shape described in an agent prompt. The distinction is
# not tidiness: `qa-executor.md` states that every FAILURE_CLASS_COUNTS entry
# "appears as a row in report.md's `## 1. Failure classes` block", and while that
# shape lived only in the prompt, the block could be deleted whole with the rule
# left standing and the suite stayed green at 29/29. A rule naming a section that
# does not exist is the same defect shape as a gate standing after the work it
# governs -- PP-18 catches that in the law, this catches it in the artifact.
#
# (a) is the shape: the template still LEADS with the block and still carries a
# row for every value the rule reconciles. (b) is REACH, in PP-18(d)'s shape and
# for a sharper reason: a template nothing points at is worse than no template,
# because it looks like a governed artifact while governing nothing. Both the law
# that copies it into place and the agent that fills it must name the file.
PP19_TPL = PLUGIN / "templates" / "qa-report.template.md"
PP19_HEADING = "## 1. Failure classes"
# The three-valued FAILURE_CLASS vocabulary PP-15(c) pins, plus `unconfirmed`.
# `unconfirmed` is NOT a fourth class -- it is the severity floor a stale baseline
# imposes -- but it is a mandatory row, because a reader who cannot see how much of
# the red rests on an unchecked revision cannot price the verdict. Listing it here
# rather than deriving it keeps the two concepts from collapsing into one.
PP19_ROWS = ("missing-input", "wrong-guess", "defect", "unconfirmed")
# Reach is asserted per duty, not by name-anywhere. Injection I-12 deleted the cp
# command and left PP-19(b) GREEN, because the dispatch text still SAYS the file was
# seeded from the template -- an instruction promising a shape nothing puts on disk,
# which is the defect this half exists to catch. The law must carry the COPY; the
# agent need only name the file it is told to fill.
PP19_COPY = re.compile(r"Bash\(command=.*cp .*qa-report\.template\.md.*report\.md")


# PP-15(a). Branch currency on the measuring agent. One token per structural
# piece: the list, the gate that carries the ask, the number, and the axis the
# number is measured against.
PP15_HARNESS_TOKENS = (
    "REPO_CURRENCY",
    "CURRENCY_GATE",
    "commits_behind",
    "default_branch",
)

# PP-15(b). The executor half. measured_on/branch_axis are Move 5; the last
# three backstop P3, which otherwise adds no property of its own.
PP15_EXECUTOR_TOKENS = (
    "measured_on",
    "branch_axis",
    "siblings_swept",
    "failure_class",
    "FAILURE_CLASS_COUNTS",
)

# PP-15(c). NEGATIVE assertion, and negative assertions have TWO failure modes,
# not one: a misspelled token passes forever, and a scope containing a
# legitimate use fails forever. Scope is therefore the two AGENT files only —
# the only files where this token would be a FAILURE_CLASS enum value.
# qa-workflow.md contains `stale-baseline` in benign prose about a failure mode,
# so a four-file or repo-wide scope is red at HEAD and stays red for the wrong
# reason. Spelling is proven by the mandatory injection recorded above.
FAILURE_CLASS_FOURTH_VALUE = "stale-baseline"

# PP-15(d). Cross-file, in PP-12's shape: a contract stated on the agent and
# absent where the router validates is a gate that disagrees with itself.
PP15_CROSS_FILE_TOKENS = ("REPO_CURRENCY", "CURRENCY_GATE")

# The bare parent value is a workflow-type marker used in `phase:qa`, not a
# dispatch target — the §7 table has never had a row for it. Excluding it is
# required: without this, PP-5 is false against SKILL.md as it stands today.
NON_DISPATCHABLE = {"qa"}

# Plan phases that existed before qa-preflight was added. PP-2 guards against an
# edit that adds the new phase by accidentally replacing one of these.
EXPECTED_PLAN_PHASES = {
    "qa",
    "qa-research",
    "qa-plan",
    "qa-plan-review",
    "qa-re-plan",
    "qa-plan-review-2",
}

# Deliberately outside the guard's default mutation_allowlist
# ([".cc10x/", "/tmp/cc10x-"]) — a target inside it is allowed regardless of
# phase, which would make the deny cases pass for the wrong reason.
PROBE_TARGET = f"/tmp/pp6-probe-{os.getpid()}"

# PP-13. Same one-artifact-at-a-time discipline as PP-6, for the same reason
# (latest_workflow_file() resolves by mtime). The pid keeps two concurrent runs
# of this suite from colliding on one workflow id.
PP13_WF_ID = f"wf-test-pp13-{os.getpid()}"

failures: list[str] = []
checked: list[str] = []


def check(prop: str, ok: bool, detail: str) -> None:
    checked.append(prop)
    status = "ok  " if ok else "FAIL"
    print(f"  [{status}] {prop}: {detail}")
    if not ok:
        failures.append(f"{prop}: {detail}")


def load_guard():
    spec = importlib.util.spec_from_file_location("qa_guard", GUARD)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPTS))  # cc10x_hooklib is a sibling import
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def artifact(phase: str | None, *, history_phase: str | None = None) -> dict:
    """A minimal QA workflow artifact.

    `workflow_type` must be QA or the guard returns 0 immediately
    (cc10x_qa_isolation_guard.py, main()) and every case would trivially pass.
    """
    payload: dict = {
        "workflow_uuid": "wf-test-pp6",
        "workflow_id": "wf-test-pp6",
        "workflow_type": "QA",
        "qa": {"isolation": {"plan_phase_readonly": True}},
        "status_history": [{"event": "started", "phase": history_phase or "qa"}],
    }
    if phase is not None:
        payload["phase_cursor"] = phase
    return payload


def run_guard(project_dir: Path, payload: dict) -> bool:
    """Write ONE artifact, invoke the guard, return True if it denied.

    One artifact at a time is load-bearing: cc10x_hooklib.latest_workflow_file()
    sorts .cc10x/workflows/*.json by mtime and returns only the newest, so
    several artifacts in one directory would all resolve to the same file and
    every case but the last would assert against the wrong one.
    """
    wf_dir = project_dir / ".cc10x" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    wf_file = wf_dir / "wf-test-pp6.json"
    wf_file.write_text(json.dumps(payload))
    try:
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project_dir))
        result = subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps(
                {"tool_name": "Bash", "tool_input": {"command": f"mkdir -p {PROBE_TARGET}"}}
            ),
            capture_output=True,
            text=True,
            env=env,
        )
        return '"permissionDecision": "deny"' in result.stdout
    finally:
        wf_file.unlink(missing_ok=True)


def closure_artifact(**overrides) -> dict:
    """A COMPLETE workflow artifact, built from the shipped skeleton.

    Load-bearing: every one of the guard's 12 REQUIRED_WORKFLOW_KEYS must be
    present. A hand-rolled minimal payload makes the guard append
    `missing-keys:` and exit 2 BEFORE the review-closure predicate is ever
    consulted — case (a) would then pass for the wrong reason and (b)(c)(d)
    would fail for one. Starting from workflow-artifact.skeleton.json is the
    only way to stay in step with that key list as it changes.

    A key whose override value is the string "__ABSENT__" is DELETED, which is
    how case (d) synthesizes a legacy artifact that predates both revision keys.
    """
    payload = json.loads(SKELETON.read_text())
    payload["workflow_uuid"] = PP13_WF_ID
    payload["workflow_id"] = PP13_WF_ID
    payload["workflow_type"] = "BUILD"
    payload["updated_at"] = "2026-01-01T00:00:00+00:00"
    for key, value in overrides.items():
        if value == "__ABSENT__":
            payload.pop(key, None)
        else:
            payload[key] = value
    return payload


def run_artifact_guard(project_dir: Path, plugin_root: Path, payload: dict):
    """Write ONE artifact plus its event log, invoke the guard, return the run.

    `artifactIntegrity: block` comes from a hook-mode.json synthesized under a
    temp CLAUDE_PLUGIN_ROOT rather than the repo's own config, so the property
    cannot go green or red because someone flipped the shipped mode file.
    """
    wf_dir = project_dir / ".cc10x" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    wf_file = wf_dir / f"{PP13_WF_ID}.json"
    events = wf_dir / f"{PP13_WF_ID}.events.jsonl"
    wf_file.write_text(json.dumps(payload))
    events.write_text(json.dumps({"event": "workflow_started"}) + "\n")
    try:
        env = dict(
            os.environ,
            CLAUDE_PROJECT_DIR=str(project_dir),
            CLAUDE_PLUGIN_ROOT=str(plugin_root),
        )
        return subprocess.run(
            [sys.executable, str(ARTIFACT_GUARD)],
            input=json.dumps(
                {"tool_name": "Write", "tool_input": {"file_path": str(wf_file)}}
            ),
            capture_output=True,
            text=True,
            env=env,
        )
    finally:
        wf_file.unlink(missing_ok=True)
        events.unlink(missing_ok=True)


def main() -> int:
    print("QA phase invariants")
    guard = load_guard()

    plan = guard.PLAN_PHASES
    prov = guard.PROVISIONING_PHASES

    check(
        "PP-1",
        "qa-preflight" not in plan,
        "'qa-preflight' is not in PLAN_PHASES — preflight must be able to provision",
    )
    missing = EXPECTED_PLAN_PHASES - plan
    check(
        "PP-2",
        not missing,
        f"no plan phase lost from PLAN_PHASES (missing: {sorted(missing) or 'none'})",
    )
    overlap = plan & prov
    check(
        "PP-3",
        not overlap,
        f"PLAN_PHASES and PROVISIONING_PHASES are disjoint (overlap: {sorted(overlap) or 'none'})",
    )

    # PP-6 — behavioural, one synthesized artifact per case.
    cases = [
        ("a", "phase_cursor='qa-plan'", artifact("qa-plan"), True),
        ("b", "phase_cursor='qa' (bare parent)", artifact("qa"), True),
        ("c", "phase_cursor='qa-preflight'", artifact("qa-preflight"), False),
        (
            "d",
            "no phase_cursor, status_history fallback -> 'qa-preflight'",
            artifact(None, history_phase="qa-preflight"),
            False,
        ),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp)
        for tag, label, payload, want_deny in cases:
            got_deny = run_guard(project_dir, payload)
            verb = "denies" if want_deny else "allows"
            check(
                f"PP-6({tag})",
                got_deny == want_deny,
                f"guard {verb} `mkdir {PROBE_TARGET}` when {label}"
                + ("" if got_deny == want_deny else f" — got deny={got_deny}"),
            )

    # PP-4 / PP-5 — phase-name drift between the route law and the router kernel.
    wf_text = QA_WORKFLOW.read_text()
    skill_text = SKILL_MD.read_text()
    wf_phases = set(re.findall(r"phase:([a-z0-9-]+)", wf_text))
    enum_match = re.search(r"^phase:\{([^}]+)\}", skill_text, re.M)
    enum = set(enum_match.group(1).split("|")) if enum_match else set()
    undeclared = sorted(wf_phases - enum)
    check(
        "PP-4",
        not undeclared and bool(enum),
        f"every phase: in qa-workflow.md is declared in the SKILL.md enum "
        f"(undeclared: {undeclared or 'none'})",
    )

    dispatch_rows = re.findall(r"^\|\s*((?:`[a-z0-9-]+`(?:,\s*)?)+)\s*\|", skill_text, re.M)
    dispatchable = {p for p in re.findall(r"`([a-z0-9-]+)`", " ".join(dispatch_rows))}
    qa_enum = {p for p in enum if p.startswith("qa")} - NON_DISPATCHABLE
    unrouted = sorted(qa_enum - dispatchable)
    check(
        "PP-5",
        not unrouted,
        f"every dispatchable QA phase has a §7 dispatcher row "
        f"(unrouted: {unrouted or 'none'}; bare 'qa' excluded by design)",
    )

    # PP-10 — the review-closure state machine. Two assertions, because either
    # alone is escapable.
    #
    # (i) PER BLOCK: the file is a sequence of transition blocks delimited by
    #     BARE `When ...:` headings. Any block that writes `passed` must carry
    #     both revision literals in the SAME block; a precondition stated in a
    #     neighbouring block guards nothing.
    # (ii) WHOLE FILE: count(passed writes) == count(guarded blocks). A `passed`
    #     written outside any block — in the prologue, or in prose — is never
    #     visited by the per-block loop, so the loop alone can be satisfied by a
    #     state machine that writes `passed` somewhere it does not look.
    #
    # AUTHORING RULE this property imposes on every block added to that file:
    # the heading MUST match BLOCK_HEADING literally (no `>` prefix, no `**`
    # emphasis, no leading whitespace) or the body folds silently into the block
    # above and the guard is applied to the wrong transition; and no heading may
    # contain the `passed` literal, which would raise the whole-file count above
    # the guarded-block count and turn (ii) red against a correct machine.
    remediation_text = REMEDIATION.read_text()
    heading_re = re.compile(r"^When .*:[ \t]*$", re.M)
    passed_re = re.compile(r"planning_review_status\s*=\s*passed")
    starts = [m.start() for m in heading_re.finditer(remediation_text)]
    bounds = starts + [len(remediation_text)]
    pp10_problems: list[str] = []
    guarded_blocks = 0
    for i, start in enumerate(starts):
        block = remediation_text[start : bounds[i + 1]]
        heading = block.splitlines()[0].rstrip()
        if not passed_re.search(block):
            continue
        guarded_blocks += 1
        for literal in ("plan_revision", "last_reviewed_revision"):
            if literal not in block:
                pp10_problems.append(
                    f"`{heading}` writes planning_review_status=passed without "
                    f"`{literal}` in the same block"
                )
    whole_file = len(passed_re.findall(remediation_text))
    if whole_file != guarded_blocks:
        pp10_problems.append(
            f"count reconciliation: {whole_file} `passed` write(s) in the whole file "
            f"but only {guarded_blocks} inside a `When ...:` block — the difference is "
            f"written where the per-block guard never looks"
        )
    check(
        "PP-10(a)",
        not pp10_problems,
        f"every planning_review_status=passed write in {REMEDIATION.name} is inside a "
        f"`When ...:` block that also carries plan_revision and last_reviewed_revision "
        f"({guarded_blocks} guarded block(s), {whole_file} whole-file write(s), "
        f"{len(starts)} block(s) total)"
        + ("" if not pp10_problems else " — " + "; ".join(pp10_problems)),
    )

    # PP-10(b) — the two AUTHORING RULES that PP-10(a) is structurally blind to.
    # Both defects were injected live while P6 was built and the suite stayed
    # exit 0 BOTH times, so they are a property now rather than a one-shot grep
    # in one phase's checklist:
    #   rule 1 — a `passed` literal sitting in a HEADING line is counted on BOTH
    #            sides of (a)'s reconciliation (whole-file +1, guarded-block +1),
    #            so 3 == 3 and (a) stays green while a heading claims closure.
    #   rule 2 — a heading dressed in `>` or `**` is not a block boundary under
    #            the bare `^When .*:$` delimiter at all, so its body folds
    #            silently into the PRECEDING block. That block is already
    #            guarded, so (a) stays green with the guard applied to the wrong
    #            transition — the worse of the two, because it reads correct.
    dressed_heading_re = re.compile(r"^\s*>?\s*\*?\*?When .*:\s*\*?\*?\s*$")
    pp10b_problems: list[str] = []
    seen_bare_heading = False
    for lineno, line in enumerate(remediation_text.splitlines(), 1):
        is_bare = bool(heading_re.match(line))
        looks_like_heading = bool(dressed_heading_re.match(line))
        if is_bare:
            seen_bare_heading = True
        elif looks_like_heading:
            pp10b_problems.append(
                f"rule 2 (a block heading MUST be bare): line {lineno} reads as a "
                f"`When ...:` heading to a human but is not a block boundary to the "
                f"parser, so its body folds into the block above — {line.strip()!r}"
            )
        if passed_re.search(line):
            if is_bare or looks_like_heading:
                pp10b_problems.append(
                    f"rule 1 (no `passed` literal in a heading): line {lineno} puts the "
                    f"literal in a block heading, where PP-10(a) counts it on BOTH sides "
                    f"of the reconciliation and stays green — {line.strip()!r}"
                )
            elif not seen_bare_heading:
                pp10b_problems.append(
                    f"rule 1 (every `passed` write lives inside a block): line {lineno} "
                    f"precedes every bare `When ...:` heading — {line.strip()!r}"
                )
    check(
        "PP-10(b)",
        not pp10b_problems,
        f"every `When ...:` heading in {REMEDIATION.name} is bare, no heading carries a "
        f"planning_review_status=passed literal, and every `passed` write sits inside a "
        f"block ({len(starts)} bare heading(s), {len(remediation_text.splitlines())} "
        f"line(s) scanned)"
        + ("" if not pp10b_problems else " — " + "; ".join(pp10b_problems)),
    )

    # PP-11 — `revised_after_review` is reachable, not a second dead enum value.
    # BOTH halves are required. The enum entry with no write site anywhere is
    # not a near-miss of the bug; it IS the bug, verbatim, as it stood at HEAD
    # before this phase.
    pp11_problems: list[str] = []
    planner_text = PLANNER_AGENT.read_text()
    enum_lines = [
        line
        for line in planner_text.splitlines()
        if line.startswith("PLANNING_REVIEW_STATUS:")
    ]
    if not enum_lines:
        pp11_problems.append(
            f"no `PLANNING_REVIEW_STATUS:` enum line found in {PLANNER_AGENT.name}"
        )
    elif not any("revised_after_review" in line for line in enum_lines):
        pp11_problems.append(
            f"`revised_after_review` is not declared in the PLANNING_REVIEW_STATUS "
            f"enum in {PLANNER_AGENT.name}"
        )
    write_sites = len(
        re.findall(r"planning_review_status\s*=\s*revised_after_review", remediation_text)
    )
    if write_sites < 1:
        pp11_problems.append(
            f"`revised_after_review` has zero write sites in {REMEDIATION.name} — it is "
            f"an enum value no transition can ever produce"
        )
    check(
        "PP-11",
        not pp11_problems,
        f"`revised_after_review` is declared in planner.md's PLANNING_REVIEW_STATUS enum "
        f"AND has {write_sites} write site(s) in {REMEDIATION.name}"
        + ("" if not pp11_problems else " — " + "; ".join(pp11_problems)),
    )

    # PP-12 — the two statements of the harness PASS rule must agree.
    # Asserted PER TOKEN with a per-token failure message, never one alternation:
    # a single `a|b|c` search returns >=1 while two of the three are missing.
    pp12_missing: list[str] = []
    for token in MUTATION_PASS_TOKENS:
        for path in (HARNESS_AGENT, HOOK_POLICY):
            if token not in path.read_text():
                pp12_missing.append(f"`{token}` missing from {path.name}")
    check(
        "PP-12(a)",
        not pp12_missing,
        "each of {assertion_falsified, survived, LIVENESS_PROBES} appears in BOTH "
        "qa-harness-builder.md and workflow-artifact-and-hook-policy.md"
        + ("" if not pp12_missing else " — " + "; ".join(pp12_missing)),
    )

    # PP-12(b) — the floor's MAGNITUDE, not just its shape. PP-12(a) is
    # satisfied by two restatements that agree on the vocabulary and disagree on
    # how many falsified assertions are required; that is the exact drift that
    # happened, and it was found by hand rather than by this suite.
    pp12b_missing: list[str] = []
    for token in MUTATION_FLOOR_MAGNITUDE_TOKENS:
        for path in (HARNESS_AGENT, HOOK_POLICY):
            if token not in path.read_text():
                pp12b_missing.append(f"`{token}` missing from {path.name}")
    check(
        "PP-12(b)",
        not pp12b_missing,
        "each of {per provable property, At risk of appearing proven, per tier and "
        "per wave, both/not either} appears in BOTH qa-harness-builder.md and "
        "workflow-artifact-and-hook-policy.md"
        + ("" if not pp12b_missing else " — " + "; ".join(pp12b_missing)),
    )

    # PP-13 — the ONLY property in this suite that answers "does the gate WORK".
    # Four synthesized artifacts, one at a time (the latest_workflow_file()
    # mtime hazard PP-6 documents applies identically), the guard invoked as a
    # SUBPROCESS in `artifactIntegrity: block` mode. Reading the new predicate's
    # source back out of the guard would prove nothing about its exit code.
    #
    # (b)(c)(d) are the backward-compatibility half and they are not decoration:
    # (c) proves only `passed` is gated — differing revisions are the NORMAL
    # mid-flight state — and (d) proves a legacy artifact written before either
    # key existed still passes. Adding the two keys to REQUIRED_WORKFLOW_KEYS
    # would brick every such artifact, which is what (d) turns into a test.
    pp13_cases = [
        (
            "a",
            "passed + plan_revision=3 / last_reviewed_revision=2",
            closure_artifact(
                planning_review_status="passed",
                plan_revision=3,
                last_reviewed_revision=2,
            ),
            2,
        ),
        (
            "b",
            "passed + plan_revision=3 / last_reviewed_revision=3",
            closure_artifact(
                planning_review_status="passed",
                plan_revision=3,
                last_reviewed_revision=3,
            ),
            0,
        ),
        (
            "c",
            "findings_received + plan_revision=3 / last_reviewed_revision=2",
            closure_artifact(
                planning_review_status="findings_received",
                plan_revision=3,
                last_reviewed_revision=2,
            ),
            0,
        ),
        (
            "d",
            "legacy artifact: passed, NEITHER revision key present",
            closure_artifact(
                planning_review_status="passed",
                plan_revision="__ABSENT__",
                last_reviewed_revision="__ABSENT__",
            ),
            0,
        ),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        project_dir = Path(tmp) / "project"
        plugin_root = Path(tmp) / "plugin"
        (plugin_root / "config").mkdir(parents=True)
        (plugin_root / "config" / "hook-mode.json").write_text(
            json.dumps({"artifactIntegrity": "block"})
        )
        for tag, label, payload, want_exit in pp13_cases:
            result = run_artifact_guard(project_dir, plugin_root, payload)
            pp13_problems: list[str] = []
            if result.returncode != want_exit:
                pp13_problems.append(
                    f"exit {result.returncode}, wanted {want_exit}"
                )
            # The REASON, never only the code. A payload missing any required
            # key also exits 2, with `missing-keys:` — indistinguishable from a
            # closure block if the code alone is asserted.
            if want_exit == 2:
                for needle in (
                    "review-closure:",
                    "plan_revision=3",
                    "last_reviewed_revision=2",
                ):
                    if needle not in result.stderr:
                        pp13_problems.append(
                            f"the blocking message never names `{needle}`"
                        )
            elif result.stderr.strip():
                pp13_problems.append(
                    f"expected silence, got stderr: {result.stderr.strip()[:200]}"
                )
            check(
                f"PP-13({tag})",
                not pp13_problems,
                f"guard in block mode exits {want_exit} on an artifact with {label}"
                + ("" if not pp13_problems else " — " + "; ".join(pp13_problems)),
            )

    # PP-14 — the wording law is not contradicted by our own template.
    # Anti-vacuity: the anchored line must EXIST and be unique first. A regex
    # that stops matching would otherwise scan zero lines and pass trivially,
    # which is the failure shape the §7 anti-vacuity note names for anchored
    # assertions.
    tpl_lines = QA_TEST_PLAN_TPL.read_text().splitlines()
    status_lines = [ln for ln in tpl_lines if PP14_STATUS_LINE.match(ln)]
    pp14_problems: list[str] = []
    if len(status_lines) != 1:
        pp14_problems.append(
            f"expected exactly 1 `**Status:**` line in {QA_TEST_PLAN_TPL.name}, "
            f"found {len(status_lines)} — the anchor the property asserts on is gone"
        )
    else:
        status_line = status_lines[0]
        for m in PP14_UNQUALIFIED.finditer(status_line):
            if status_line[m.end() : m.end() + len(PP14_QUALIFIER)] != PP14_QUALIFIER:
                pp14_problems.append(
                    f"bare `{m.group(0)}` at col {m.start()} of the `**Status:**` line "
                    f"is not qualified by `{PP14_QUALIFIER}` — the wording law forbids "
                    f"a status claim that does not name the revision it applies to"
                )
    check(
        "PP-14",
        not pp14_problems,
        "the single `**Status:**` line of qa-test-plan.template.md offers no bare "
        "`reviewed` or `approved` — every one is qualified by `@r`"
        + ("" if not pp14_problems else " — " + "; ".join(pp14_problems)),
    )

    # PP-15(a) — branch currency exists on the agent that measures it.
    harness_text = HARNESS_AGENT.read_text()
    executor_text = EXECUTOR_AGENT.read_text()
    pp15a_missing = [
        f"`{token}` missing from {HARNESS_AGENT.name}"
        for token in PP15_HARNESS_TOKENS
        if token not in harness_text
    ]
    check(
        "PP-15(a)",
        not pp15a_missing,
        "each of {REPO_CURRENCY, CURRENCY_GATE, commits_behind, default_branch} "
        "appears in qa-harness-builder.md"
        + ("" if not pp15a_missing else " — " + "; ".join(pp15a_missing)),
    )

    # PP-15(b) — the executor half, plus the severity cap asserted on the
    # ANCHORED enum line of BOTH emitters. A whole-file search for
    # `unconfirmed` is satisfied by the word appearing in prose, which is not
    # the same claim as the enum offering the value.
    pp15b_missing = [
        f"`{token}` missing from {EXECUTOR_AGENT.name}"
        for token in PP15_EXECUTOR_TOKENS
        if token not in executor_text
    ]
    for path, text in ((EXECUTOR_AGENT, executor_text), (HARNESS_AGENT, harness_text)):
        enum_lines = [ln for ln in text.splitlines() if re.match(r"^\s*severity:", ln)]
        if not enum_lines:
            pp15b_missing.append(f"no `severity:` enum line found in {path.name}")
        elif not any("unconfirmed" in ln for ln in enum_lines):
            pp15b_missing.append(
                f"`unconfirmed` is not on the severity: enum line in {path.name}"
            )
    check(
        "PP-15(b)",
        not pp15b_missing,
        "each of {measured_on, branch_axis, siblings_swept, failure_class, "
        "FAILURE_CLASS_COUNTS} appears in qa-executor.md, and `unconfirmed` is on "
        "the anchored severity: enum line of BOTH emitters"
        + ("" if not pp15b_missing else " — " + "; ".join(pp15b_missing)),
    )

    # PP-15(c) — the FAILURE_CLASS vocabulary did not grow a fourth value.
    pp15c_present = [
        path.name
        for path, text in ((HARNESS_AGENT, harness_text), (EXECUTOR_AGENT, executor_text))
        if FAILURE_CLASS_FOURTH_VALUE in text
    ]
    check(
        "PP-15(c)",
        not pp15c_present,
        f"`{FAILURE_CLASS_FOURTH_VALUE}` appears in neither agent file — the "
        f"FAILURE_CLASS vocabulary is still three-valued"
        + (
            ""
            if not pp15c_present
            else " — a fourth value appeared in " + ", ".join(pp15c_present)
        ),
    )

    # PP-15(d) — the router-side restatement. Round-1 PP-15 asserted only
    # WITHIN the agent files and so could not detect an agent/router split even
    # in principle. Two reads, never one grep over two files.
    pp15d_missing: list[str] = []
    for token in PP15_CROSS_FILE_TOKENS:
        for path in (HARNESS_AGENT, HOOK_POLICY):
            if token not in path.read_text():
                pp15d_missing.append(f"`{token}` missing from {path.name}")
    if "REPO_CURRENCY" not in QA_WORKFLOW.read_text():
        pp15d_missing.append(f"the branch-currency duty is absent from {QA_WORKFLOW.name}")
    check(
        "PP-15(d)",
        not pp15d_missing,
        "REPO_CURRENCY and CURRENCY_GATE each appear in BOTH qa-harness-builder.md "
        "and workflow-artifact-and-hook-policy.md, and the duty reaches qa-workflow.md"
        + ("" if not pp15d_missing else " — " + "; ".join(pp15d_missing)),
    )

    # PP-16 — every dispatch-metadata value the route law writes is declared.
    # Placeholder forms are discarded by the leading `{`: `origin:{router|...}`
    # IS the enum declaration and `origin:{originating agent}` is a template
    # slot; treating either as a written value would make the check assert
    # against itself.
    def concrete_origins(text: str) -> set[str]:
        return {
            v for v in re.findall(r"origin:(\{?[A-Za-z0-9_-]*)", text)
            if v and not v.startswith("{")
        }

    origin_enum_match = re.search(r"^origin:\{([^}]+)\}", skill_text, re.M)
    origin_enum = set(origin_enum_match.group(1).split("|")) if origin_enum_match else set()

    found_origins: set[str] = concrete_origins(skill_text)
    for ref in sorted(REFERENCES.glob("*.md")):
        found_origins |= concrete_origins(ref.read_text())
    found_phases = set(re.findall(r"phase:([a-z0-9-]+)", PLAN_WORKFLOW.read_text()))

    pp16_problems: list[str] = []
    # Preconditions FIRST — a broken regex must fail here, never pass on an
    # empty set. This is the third vacuity shape, unique to set membership.
    if len(found_origins) < PP16_MIN_ORIGINS:
        pp16_problems.append(
            f"extraction broken: only {len(found_origins)} concrete origin: values found "
            f"(live baseline is {PP16_MIN_ORIGINS}) — {sorted(found_origins) or 'none'}"
        )
    if not origin_enum:
        pp16_problems.append("the SKILL.md origin: enum line did not parse")
    if len(found_phases) < PP16_MIN_PHASES:
        pp16_problems.append(
            f"extraction broken: only {len(found_phases)} phase: values found in "
            f"plan-workflow.md (live baseline is {PP16_MIN_PHASES}) — "
            f"{sorted(found_phases) or 'none'}"
        )
    if not pp16_problems:
        for value in sorted(found_origins - origin_enum):
            pp16_problems.append(f"origin:{value} is written but not declared in the origin enum")
        for value in sorted(found_phases - enum):
            pp16_problems.append(
                f"phase:{value} in plan-workflow.md is not declared in the phase enum"
            )
    check(
        "PP-16",
        not pp16_problems,
        f"every origin: ({len(found_origins)}) and every plan-workflow phase: "
        f"({len(found_phases)}) the route law writes is declared in the SKILL.md enum it "
        f"belongs to"
        + ("" if not pp16_problems else " — " + "; ".join(pp16_problems)),
    )

    # PP-9 — §N references resolve, using the CITATION PREFIX to pick the file.
    # qa-workflow.md cites at least four different documents, so a naive
    # "assume the env-plan template" rule fails on `SKILL.md §14`.
    env_headings = {
        int(m) for m in re.findall(r"^## (\d+)\.", ENV_PLAN_TPL.read_text(), re.M)
    }
    bad: list[str] = []
    unresolved = 0
    for path in (ENV_PLAN_TPL, HARNESS_AGENT, QA_WORKFLOW):
        text = path.read_text()
        for m in re.finditer(r"(\w[\w .`-]{0,14}?)?§(\d+)", text):
            prefix = (m.group(1) or "").lower()
            num = int(m.group(2))
            if "env plan" in prefix or "env-plan" in prefix:
                target = env_headings
            elif path is ENV_PLAN_TPL and not prefix.strip(" `"):
                target = env_headings          # bare §N inside the template = self
            else:
                unresolved += 1                # test plan / SKILL.md / RFC / ambiguous
                continue
            if num not in target:
                bad.append(f"{path.name}: §{num} has no '## {num}.' heading")
    check(
        "PP-9",
        not bad,
        f"every resolvable §N points at a real heading "
        f"({len(bad)} bad, {unresolved} unresolved-and-skipped)",
    )

    # ---------------------------------------------------------------- PP-18
    # Assert the measure-before-you-ask law, and assert it where it is NORMATIVE.
    #
    # Eleven injections were run against this property's first two drafts; seven
    # of them shipped GREEN against a broken law. Each defence below is here
    # because one of those constructions defeated its predecessor:
    #
    #   normalise -> a law inside ```fences``` or <!-- --> is not law, so both
    #                are stripped before any token is looked for
    #   window    -> a whole-file substring test cannot say WHERE a rule lives;
    #                `came back empty` is deliberately in BOTH 0a and 0b, so the
    #                file-scoped form let 0b satisfy 0a's half of the assertion
    #   ^-anchor  -> find() anchors to the first TEXTUAL occurrence, not to the
    #                structural element; a forward reference left at the old
    #                offset made a gate relocated AFTER the fan-out read as
    #                preceding it. Line-start regex + exactly-one-match.
    #   body      -> position is the easy half. The 1,332-byte body of 0b could
    #                be deleted down to its heading and all three sub-cases
    #                stayed green, which is the incident behaviour restored.
    #                (b) therefore asserts the operative clauses too.
    #   two-para  -> (c) pairs a positive assertion with an absence clause and
    #                sweeps the FOLLOWING paragraph as well, because a deferral
    #                merely moved one paragraph down defeated a one-para slice.
    def _normative(text: str) -> str:
        """Drop HTML comments and fenced blocks: neither is enforceable law."""
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        return re.sub(r"^```.*?^```", "", text, flags=re.DOTALL | re.MULTILINE)

    qa_norm = _normative(wf_text)

    m_0a = re.search(r"(?m)^0a\. \*\*Capability discovery", qa_norm)
    m_0b_all = re.findall(r"(?m)^0b\. \*\*Repo-set enumeration", qa_norm)
    m_fan_all = re.findall(r"(?m)^#### Research fan-out", qa_norm)
    m_0b = re.search(r"(?m)^0b\. \*\*Repo-set enumeration", qa_norm)
    m_fan = re.search(r"(?m)^#### Research fan-out", qa_norm)
    m_step1 = re.search(r"(?m)^1\. \*\*Resolve QA scope", qa_norm)

    # (a) both halves of the rule live INSIDE the 0a section, not merely in the file
    win_0a = qa_norm[m_0a.end() : m_0b.start()] if (m_0a and m_0b) else ""
    tokens_a = (
        "came back empty",
        "Never ask the user whether something exists on their machine",
    )
    missing_a = [tok for tok in tokens_a if tok not in win_0a]
    check(
        "PP-18(a)",
        bool(win_0a) and not missing_a,
        f"the measure-before-you-ask rule is normative inside step 0a "
        f"(window={len(win_0a)}B, {len(tokens_a) - len(missing_a)}/{len(tokens_a)} "
        f"tokens" + (f", missing {missing_a}" if missing_a else "") + ")",
    )

    # (b) the gate is unique, precedes the lanes, AND still has its operative body
    win_0b = (
        qa_norm[m_0b.end() : m_step1.start()]
        if (m_0b and m_step1 and m_0b.end() < m_step1.start())
        else ""
    )
    tokens_b = (
        "PRESENT the set on screen",
        "explicit confirmation",
        "only after that confirmation",
        "This gate cannot be deferred",
    )
    missing_b = [tok for tok in tokens_b if tok not in win_0b]
    check(
        "PP-18(b)",
        len(m_0b_all) == 1
        and len(m_fan_all) == 1
        and m_0b is not None
        and m_fan is not None
        and m_0b.start() < m_fan.start()
        and bool(win_0b)
        and not missing_b,
        f"step 0b is a unique line-anchored block that precedes the research "
        f"fan-out and retains its operative body "
        f"(0b x{len(m_0b_all)}@{m_0b.start() if m_0b else -1} < "
        f"fan-out x{len(m_fan_all)}@{m_fan.start() if m_fan else -1}, "
        f"body={len(win_0b)}B, {len(tokens_b) - len(missing_b)}/{len(tokens_b)} "
        f"clauses" + (f", missing {missing_b}" if missing_b else "") + ")",
    )

    # (c) the split routes through 0b, and nothing near it defers to a later gate
    m_split = re.search(r"(?m)^\*\*Splitting the `code` lane per repo", qa_norm)
    DEFERRALS = ("topology gate", "topology checkpoint", "qa-plan")
    if m_split:
        paras = qa_norm[m_split.start() :].split("\n\n")
        scope_c = "\n\n".join(paras[:2])
        deferrals_found = [d for d in DEFERRALS if d in scope_c]
        ok_c = "step 0b" in paras[0] and not deferrals_found
    else:
        scope_c, deferrals_found, ok_c = "", ["<paragraph not found>"], False
    # (d) the cross-file duty actually REACHES the file that must honour it.
    # PP-15(d) sets this convention: a duty stated in exactly one file is prose.
    tpl_text = QA_TEST_PLAN_TPL.read_text(encoding="utf-8")
    reach = {
        "qa-workflow.md": "unproven by stub" in qa_norm,
        "qa-test-plan.template.md": "unproven by stub" in tpl_text,
    }
    check(
        "PP-18(d)",
        all(reach.values()),
        f"the `unproven by stub` duty reaches both the law that imposes it and "
        f"the template that must carry the row ({reach})",
    )

    check(
        "PP-18(c)",
        ok_c,
        f"the lane-split paragraph routes through step 0b and neither it nor "
        f"the paragraph after it defers to a later gate "
        f"(scope={len(scope_c)}B, deferrals={deferrals_found or 'none'})",
    )


    # PP-19(a) — the template still leads with the block the rule reconciles against.
    tpl_text = PP19_TPL.read_text(encoding="utf-8") if PP19_TPL.exists() else ""
    tpl_headings = re.findall(r"(?m)^## .+$", tpl_text)
    pp19a_faults = []
    if not tpl_text:
        pp19a_faults.append(f"{PP19_TPL.name} does not exist")
    elif PP19_HEADING not in tpl_headings:
        pp19a_faults.append(
            f"`{PP19_HEADING}` is not a heading in the template "
            f"(headings: {tpl_headings or 'none'})"
        )
    elif tpl_headings[0] != PP19_HEADING:
        # Position is load-bearing, not cosmetic: a zero count read after the
        # scenario table is a footnote rather than the frame the run is read in.
        pp19a_faults.append(
            f"`{PP19_HEADING}` is present but not first — the template's first "
            f"section is `{tpl_headings[0]}`"
        )
    else:
        idx = tpl_text.index(PP19_HEADING)
        nxt = tpl_text.find("\n## ", idx + 1)
        section = tpl_text[idx : nxt if nxt != -1 else len(tpl_text)]
        pp19a_faults += [
            f"no `| {row} |` row under the heading"
            for row in PP19_ROWS
            if not re.search(r"(?m)^\|\s*" + re.escape(row) + r"\s*\|", section)
        ]
    check(
        "PP-19(a)",
        not pp19a_faults,
        f"qa-report.template.md leads with `{PP19_HEADING}` carrying a row for each "
        f"of {{{', '.join(PP19_ROWS)}}}"
        + ("" if not pp19a_faults else " — " + "; ".join(pp19a_faults)),
    )

    # PP-19(b) — REACH, per duty. A template nothing copies governs nothing.
    pp19b_missing = []
    if not PP19_COPY.search(QA_WORKFLOW.read_text(encoding="utf-8")):
        pp19b_missing.append(
            "qa-workflow.md has no Bash cp of the template into report.md — a "
            "dispatch that only NAMES the template promises a shape nothing lays down"
        )
    if PP19_TPL.name not in EXECUTOR_AGENT.read_text(encoding="utf-8"):
        pp19b_missing.append("qa-executor.md does not name the template it must fill")
    check(
        "PP-19(b)",
        not pp19b_missing,
        f"the law COPIES `{PP19_TPL.name}` into place and the agent NAMES it"
        + ("" if not pp19b_missing else " — " + "; ".join(pp19b_missing)),
    )

    print(f"\nproperties checked: {', '.join(checked)}")
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("all QA phase invariants hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
