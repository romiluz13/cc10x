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
PP-21 the workflow artifact's three authorities agree: (a) every backticked
      `results.*` / `qa.*` literal the QA law names resolves SEGMENT BY SEGMENT
      to FULL DEPTH in the shipped skeleton; (b) every top-level key the
      skeleton ships is documented in the hook policy's artifact schema list;
      (c) QA is a member of the three enums the guard and the router read --
      the `workflow_type` enum LINE, the `evidence` agent list, and SKILL.md's
      event-log phase template -- each asserted on its anchored line, never
      whole-file.
PP-23 the harness contract cannot pass while proving or enumerating nothing:
      (a) the mutation floor is never VACUOUS -- the floor minimum binds every
      branch and branch 2 names its fall-through, in BOTH byte-duplicated
      statements of the rule; (b) `ARTIFACTS_CREATED` and `HARNESS_MANIFEST` are
      REQUIRED, non-empty and non-null, in the `MODE: harness` slice of the rows
      that decide validity -- row-anchored AND mode-anchored, never whole-file
PP-24 the currency gate's axis is `commits_behind` and a dirty tree is not on
      it: the commits_behind-only phrasing in all three sites that state the
      trigger, the coupling phrase in none of them, and `dirty` still a
      REPO_CURRENCY field so the fix cannot be "delete the measurement"
PP-22 every agent file SPECIFIES the line-1 `CONTRACT {` envelope inside its
      OUTPUT SPECIFICATION -- the window from the last
      Output/Router Contract/Phase Contract heading before the file's first
      ```yaml fence, up to that fence. Unconditional over
      `plugins/cc10x/agents/*.md`: 11/14 at HEAD, 14/14 after. An agent that
      specifies no envelope leaves SKILL.md §8's verdict extraction with a
      heading scan that finds nothing, so the router trips inline verification
      on every lane of that agent.

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

Negative controls for PP-20 (three runs, all red, all with the right message).
The property guards the task graph, where a missing edge means an agent is
dispatched before the artifact it is told to read has been written:
  I-15 the `qa-plan` addBlockedBy deleted -- the M1 defect itself
                                          -> red: "dispatched with no incoming
                                             edge: qa_plan_task_id", naming the
                                             one node rather than "some node"
  I-16 the node regex `->` changed to `=>` so it matches nothing
                                          -> red on the PRECONDITION, not on
                                             membership. Mandatory: without it a
                                             dead regex yields an empty set and
                                             `set() - set() <= ROOTS` is
                                             vacuously TRUE forever, which is
                                             PP-16(c)'s recorded shape.
  I-17 _decommented() swapped for _normative() -- i.e. PP-20 written the way it
       was first specified                 -> red: 0 nodes extracted.
I-17 is the reason the helper exists. _normative() strips fenced blocks, and the
whole task graph is authored inside ```text fences, so that draft of PP-20 was
red at HEAD on its own precondition and no edit to the LAW could ever have made
it green. It was caught by review before it was written, and the control is
recorded here so the next person to reach for the shared normaliser sees the
measurement: 12 nodes raw, 12 de-commented, 0 normative.

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

Negative controls for PP-21 (six runs, all red, each naming the injected thing;
the depth contrast under I-21 is the one that carries the property's weight).
Before this property the three authorities had drifted in all three directions
at once and the suite was green at 32: the law named `results.qa_env_preflight`
where the skeleton said `qa.`, named `results.qa_repo_set` and
`qa.preflight.currency_gate` which the skeleton did not ship at all, the hook
policy's schema list was short by seven top-level keys, and QA was absent from
every one of the three enums:
  I-18 `results.qa_repo_set` deleted from the skeleton's `results` block
                                          -> (a) red: "named by the law, absent
                                             from the skeleton: results.qa_repo_set",
                                             naming the one key rather than a count.
  I-19 `source_wf` deleted from the hook policy's top-level list, leaving the
       skeleton shipping it       -> (b) red: 44/45, naming `source_wf`.
       The direction matters: the list is the thing that goes stale, because a
       key is added to the skeleton by the code that needs it and to the list by
       nobody.
  I-20 `QA` removed from the `workflow_type` enum LINE only, leaving all four
       other occurrences of the token "QA" in the file standing
                                          -> (c) red naming the enum line and
                                             printing its eight surviving members.
       MANDATORY, and it is the run that proves the anchoring: a whole-file
       substring test for `QA` is GREEN against this injection, which is PP-14's
       recorded trap in a second file.
  I-21 `currency_gate` deleted from the skeleton's `qa.preflight` block
                                          -> (a) red naming
                                             `qa.preflight.currency_gate`.
       Then, with the injection STILL IN PLACE, the resolver was truncated to
       depth=1 and re-run: GREEN. Truncated to depth=2: GREEN. Both truncations
       pass because `qa` and `qa.preflight` exist and only the LEAF is missing.
       Full-depth resolution is therefore not a stylistic choice — it is the
       only construction of this property that can see the defect, and the two
       shallower ones would have shipped green over a live gap.
  I-22 the backtick anchor of PP21_KEY_LITERAL changed to `@` so it matches
       nothing                            -> (a) red on the PRECONDITION,
                                             "extracted only 0 ... vacuous".
       Mandatory for the same reason as I-16: with no floor, an empty literal
       set makes "every literal resolves" vacuously true forever.
  I-23 the schema-list section heading reworded to "Artifact schema shall
       include:"                          -> (b) red on the PRECONDITION,
                                             naming the anchors that stopped
                                             bracketing a section.
A note on the (b) floor, because getting it wrong once is what produced this
comment. It was first written as `>= 40`, one short of the post-fix 45. Against
the pre-fix tree (38 entries) that floor fired the PRECONDITION and the red never
named the seven missing keys — red for the wrong reason, from a property that
was otherwise correct. A floor set just under the complete count silently does
the membership half's job and hides it. The floor is now 30: its only duty is
proving the slice still finds a list.

Negative controls for PP-22 (two runs, both red, each naming ONE file). The
property is a membership test over a glob, so it has both vacuity shapes this
file has been bitten by, and each control closes one:
  I-24 the newly added envelope line deleted from `qa-researcher.md` ONLY
                                          -> red: "13/14 ... no envelope in the
                                             output specification of:
                                             qa-researcher.md (window=271B)",
                                             with `qa-harness-builder.md` and
                                             `qa-executor.md` still counted
                                             green.
       Per-FILE naming is the point of the control, not a nicety. A property
       that reports "some agent is missing its envelope" over a 14-file glob
       sends the next reader to grep; this one sends them to a line.
  I-25 `code-reviewer.md:241` -- the envelope line inside the output
       specification -- deleted, with `:83` (a Process-step restatement) and
       `:328` (a prose CONTRACT rule) LEFT INTACT
                                          -> red naming `code-reviewer.md`
                                             alone, window 339B -> 297B, while
                                             `grep -c "CONTRACT {"` on the same
                                             file still returns 2.
       MANDATORY, and deliberately not run on a QA file: it is the only run that
       proves the ANCHORING rather than the membership. A whole-file substring
       test -- which is what this property would have been written as -- is
       GREEN against this injection, twice over. That is PP-18's recorded I-2
       shape in a third file, and `code-reviewer.md` is the file that can
       exhibit it because it is the one carrying three copies of the token.

Negative controls for PP-23 and PP-24 (six runs, all red, each naming the
injected thing). The three defects share one agent file and two hook-policy
rows, so they were landed and controlled together:
  I-26 "or a dirty tree" re-inserted into the qa-preflight DISPATCH TEXT only,
       leaving the agent and the policy row corrected
                                          -> PP-24 red naming
                                             `qa-workflow.md (qa-preflight
                                             dispatch text)` on BOTH halves: the
                                             axis phrasing absent AND the
                                             coupling phrase present.
       MANDATORY, and it is the run that proves the SPELLING of the forbidden
       token. A negative assertion has two failure modes a positive one does not
       -- a misspelled token passes forever, and a legitimate use inside scope
       fails forever -- so the token must be demonstrated to still match
       something, and the scope must be frozen to the three sites that state the
       trigger. This is PP-15(c)'s recorded discipline, applied to a second
       negative assertion.
  I-27 the floor-minimum sentence deleted from the hook-policy ROW only, leaving
       qa-harness-builder.md's copy standing
                                          -> PP-12(a) red naming the token and
                                             the hook-policy file, and PP-23(a)
                                             red on the same token.
       This is the byte-duplication trap in the direction it historically drifts
       (PP-12's original control, I-26's predecessor, is the same shape), and it
       is the run that justifies PP-12(a) staying a WHOLE-FILE substring while
       nearly everything else here is window-anchored: the divergence it exists
       to catch is CROSS-FILE, and no stray copy in one file can conjure the
       other file's copy. Both properties going red is expected and not
       redundancy to remove: PP-12(a) reports it as a duplication failure,
       PP-23(a) as a vacuity failure, and the two failure messages send a reader
       to different places.
  I-28 the `dirty:` field deleted from the agent's REPO_CURRENCY block
                                          -> PP-24 red: "`dirty` is no longer a
                                             REPO_CURRENCY field ...
                                             (block=460B)".
       MANDATORY. Without this half the property REWARDS THE WRONG FIX: deleting
       `dirty` outright satisfies "a dirty tree is not a trigger" perfectly while
       losing a measurement the route needs. Demoting a trigger to a fact and
       deleting the fact are indistinguishable to a purely negative assertion.
       The block anchor also matters -- `dirty:` appears again on the
       CURRENCY_GATE entry, so a file-wide search is GREEN against this
       injection.
  I-29 `ARTIFACTS_CREATED` deleted from the `MODE: harness` required-field slice
       of the `:287` row ONLY -- not from the agent, not from any dispatch text
                                          -> PP-23(b) red naming the slice
                                             (slice 435B -> 414B).
  I-30 THE ONE THAT PROVES THE MODE ANCHORING. Both tokens moved out of the
       harness sub-list and into the `MODE: preflight` sub-list of the SAME
       physical line -- the two enumerations are separated only by `<br>`
                                          -> PP-23(b) still red, naming both
                                             tokens and the harness slice
                                             (394B), while `grep -c
                                             ARTIFACTS_CREATED` on the file
                                             still returns 2.
       A row-anchored-but-not-mode-anchored property is GREEN against this, and
       preflight is precisely the mode where `HARNESS_MANIFEST: null` stays
       legal -- so the green would have blessed a contract that requires the
       review surface in the one mode that does not produce it. PP-18's I-2
       shape, one nesting level further in: the whole-file trap reappears as a
       whole-ROW trap once two enumerations share a line.
  I-31 `HARNESS_MANIFEST` set back to unconditional `| null` at the agent's
       declaration line, both policy halves left correct
                                          -> PP-23(b) red on the nullability
                                             half ALONE, quoting the offending
                                             line, with the slice and overrides
                                             halves green.
       The three halves are asserted independently; any one alone is satisfiable
       by a contract that is two-thirds wired.
A control this phase deliberately did NOT run: the contrast showing that a
dispatch-text-only property stays green under I-29. At this point neither
PP-30(b) nor its subject exists -- qa-workflow.md does not name either field
until the dispatch text is written -- so such a property would be red for the
absence of its subject, not green. The contrast is a real measurement only once
the dispatch text lands, and it belongs to that change.
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
# LIVENESS_PROBES     = the separate list that cannot satisfy the floor,
# the floor minimum   = no branch of the selector may floor at zero,
# MUTATION_CHECKS empty = the backstop for an empty entry set. This one lived in
#                       qa-harness-builder.md alone while the router's validation
#                       row said nothing, so the router-side authority resolved
#                       OPTIMISTICALLY on the exact shape the agent forbade —
#                       which is finding P2 in miniature.
# A restatement missing any one of them permits a verdict the other site forbids.
#
# Why a WHOLE-FILE substring is the right scope HERE and nowhere else. This suite
# window-anchors almost everything (PP-14, PP-18, PP-21(c), PP-22) because a
# second copy of a token elsewhere in the same file satisfies a file-wide search
# and hides the defect. That failure mode cannot apply to this property: the
# assertion is PER TOKEN PER FILE across two files that are meant to be
# byte-duplicates of one rule, and the only divergence it is about is a
# CROSS-FILE one. A stray copy inside qa-harness-builder.md cannot make the
# hook policy's copy appear. Control (ii) — deleting the floor-minimum sentence
# from the policy row only, leaving the agent's — is the run that demonstrates
# it, and it is recorded in the docstring above.
MUTATION_PASS_TOKENS = (
    "assertion_falsified",
    "survived",
    "LIVENESS_PROBES",
    "at least one `assertion_falsified` is required regardless of which branch applies",
    "`MUTATION_CHECKS` empty means no assertion was ever observed failing",
)

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

# PP-20 -- the QA task graph. Every node the law creates must have an incoming
# edge, or it is dispatched before the thing it reads has been written. M1 was
# exactly that: `qa-plan` ran in parallel with the researchers whose output is
# the feature map it is told to read.
#
# SCOPE, and why this is the one property that must NOT reuse _normative():
# _normative() strips fenced blocks, on the argument that law re-parked into an
# example is not law. That argument is right for prose and wrong here. The task
# graph is AUTHORED inside ```text fences -- they are code blocks, and the fence
# IS the normative surface. Measured on the shipped file: 12 nodes / 10 edges
# raw, 12 / 10 de-commented, and 0 / 0 through _normative(). A PP-20 built on
# _normative() would be red at HEAD on its own precondition and could never go
# green. _decommented() drops HTML comments only -- a graph inside <!-- --> is
# genuinely not a graph.
#
# _decommented() is currently a NO-OP on qa-workflow.md: the file carries zero
# HTML comments at HEAD. It is here so a future commented-out node cannot count,
# not because it does work today. Control I-17 is what actually proves PP-20.
PP20_NODE = re.compile(r"->\s*(\S+_task_id\S*)")
PP20_EDGE = re.compile(r"TaskUpdate\(\{\s*taskId:\s*(\w+),\s*addBlockedBy:")
# The fan-out lanes are the only nodes with no predecessor, and that is a
# property of the route, not an oversight: consolidation after the lanes is
# deliberately INLINE (qa-workflow.md argues it), so there is no task between
# the researchers and qa-plan. Adding a name here asserts a new ENTRY POINT to
# the QA graph -- it is not a way to quiet a node that lost its edge.
QA_DAG_ROOTS = frozenset({"researcher_task_id"})
# The lane variable is written `researcher_task_id_{source}` -- `{source}` is a
# template expansion the router substitutes per lane, not part of the name the
# graph refers to. Both sides are canonicalised so the frozen constant is a
# token the extraction can actually produce; SF-1 was a ROOTS member that
# `\w+` could never emit, which would have made the root read as unrouted.
PP20_TEMPLATE_SUFFIX = re.compile(r"_?\{[a-z_]+\}$")


# PP-21 -- artifact schema truth, in three directions. The defect class is the
# one this file already guards twice elsewhere (PP-12, PP-15(d)): two authorities
# describing the same thing, drifting apart with the suite green. Here the thing
# is the workflow artifact, and the authorities are the QA law, the shipped
# skeleton, and the hook policy's schema lists.
#
# (a) LAW -> SKELETON, resolved to FULL DEPTH. Every backticked `results.<...>`
# / `qa.<...>` literal in qa-workflow.md names a place in
# workflow-artifact.skeleton.json, and a rule that names a place in another file
# is only a rule if the place exists. DEPTH is the load-bearing decision, not an
# implementation detail: `qa.preflight.currency_gate` was missing its LEAF while
# `qa` and `qa.preflight` both existed, so a first-segment resolver is green on
# it and so is a two-segment one. Only full depth sees it. Measured before this
# phase: 9 distinct literals, 6 resolve, 3 miss -- `results.qa_env_preflight`,
# `results.qa_repo_set`, `qa.preflight.currency_gate` -- which were exactly this
# phase's three edits. Control I-21 is the run that proves depth is doing the work.
#
# Direction is law -> skeleton ONLY, deliberately. The reverse (every skeleton
# key is named by the law) is FALSE by design: the skeleton ships BUILD/DEBUG
# slots QA never writes, so a symmetric assertion would be red at HEAD for a
# reason that is not a defect.
#
# Read over _decommented() text for the same reason PP-20 is: a key named inside
# <!-- --> is not named. Not _normative(): several of these literals are inside
# ```text dispatch fences, which are the normative surface here, and the fenced
# `qa.isolation`/`qa.preflight` mentions are exactly the ones a reader trusts.
PP21_KEY_LITERAL = re.compile(r"`((?:results|qa)\.[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*)`")
# Anti-vacuity floor, asserted BEFORE resolution: a regex that stopped matching
# yields an empty set and "every literal resolves" is vacuously true forever.
# That is PP-16(c)'s recorded shape. 9 at HEAD.
PP21_MIN_LITERALS = 6

# (b) SKELETON -> HOOK POLICY, all top-level keys. Scoped to top level because
# nesting is documented selectively by design and a recursive assertion would be
# red at HEAD for the wrong reason.
#
# Measured when this property was written: the skeleton ships 45 top-level keys
# and the policy list carried 38. The SEVEN absent from the list were absent from
# the whole policy file: build_scope, worktree, execution_mode,
# inline_fallback_reason, source_wf, source_bug_candidate, qa. Only three of the
# seven are QA's; the four BUILD-era omissions (build_scope, worktree,
# execution_mode, inline_fallback_reason) were closed here DELIBERATELY, not
# incidentally. The alternative -- scoping this property to the QA-introduced
# keys -- would have shipped an invariant that cannot see the defect class it
# exists for, and would have left `build_scope`, a key the BUILD route branches
# on, undocumented in the document whose job is documenting it.
#
# `worktree` being on this list does NOT give QA a worktree: ADR-2 keeps
# `worktree` and `results.finishing` BUILD-only, and documenting a key the
# skeleton already ships for BUILD is a different act from offering QA one.
PP21_SCHEMA_LIST_START = re.compile(r"^Artifact schema must include:$", re.M)
PP21_SCHEMA_LIST_END = re.compile(r"^Rules:$", re.M)
PP21_LIST_ENTRY = re.compile(r"^- `([a-z_]+)`", re.M)
# The floor's ONLY job is proving the section slice still finds a list; the
# membership half is what proves the list is complete, and a floor set just under
# the complete count silently does the membership half's work instead. Set to 30
# for exactly that reason: at 40 the pre-fix tree (38 entries) failed the
# PRECONDITION and never reached membership, so the red never named the seven
# missing keys -- red for the wrong reason, the shape step 4 of the protocol
# exists to catch. 45 after this phase; a broken anchor yields ~0.
PP21_MIN_LISTED = 30

# (c) QA is a member of the enums the PostToolUse guard and the router actually
# read. Every assertion here is on the SINGLE anchored line that carries the
# enum, never a whole-file search: `QA` appears in prose throughout both files
# (and `qa` appears in dozens of phase tokens), so a file-wide test is satisfied
# by prose while the enum stays short. That is PP-14's recorded trap, and
# control I-20 is the run that proves the anchoring here.
PP21_WORKFLOW_TYPE_LINE = re.compile(r"^- `workflow_type`(.*)$", re.M)
PP21_ENUM_TOKEN = re.compile(r"`([A-Za-z_-]+)`")
PP21_EVIDENCE_HEAD = re.compile(
    r"^- `evidence` stores proof-of-work grouped by agent:$", re.M
)
PP21_EVIDENCE_ENTRY = re.compile(r"^  - `([a-z_]+)`")
PP21_EVENT_LOG_LINE = "workflow_started"
# The event-log template line carries four brace expansions ({iso_timestamp},
# {workflow_uuid}, {parent_task_id} and the phase enum). Requiring at least one
# `|` is what picks out the enum without hard-coding its membership -- a
# substring test for "qa" on this line would be satisfied by the word appearing
# anywhere on it, including inside a future task-id template.
PP21_PHASE_ENUM = re.compile(r"\{([a-z-]+(?:\|[a-z-]+)+)\}")


# PP-22 -- every agent file SPECIFIES the line-1 `CONTRACT {` envelope in its
# output specification. SKILL.md §8's verdict extraction reads the envelope
# first and falls back to a heading scan; an agent that specifies neither leaves
# the router with prose, so it trips inline verification on every lane. M4 named
# `qa-researcher`; re-measurement found all three QA agents lacked it and all
# eleven non-QA agents had it -- 11/14 at HEAD, 14/14 after this phase.
#
# UNCONDITIONAL over the glob, deliberately. An earlier draft gated the property
# on "the file declares a Router Contract block", which is fragile: the heading
# exists in three spellings across two levels (`## Router Contract
# (MACHINE-READABLE)` x3, `## Router Contract (REQUIRED)` x1, `### Router
# Contract (MACHINE-READABLE)` x4) in only 8 of the 14 files, so the conditional
# shrinks the denominator to 8 and buys nothing -- the property is true and
# wanted for all 14.
#
# WINDOW-ANCHORED, and that is the load-bearing decision. A whole-file
# `CONTRACT {` substring is the PP-18 I-2 shape: `code-reviewer.md` carries the
# token three times (:83 a Process-step restatement, :241 the output
# specification, :328 a prose CONTRACT rule), so deleting the SPECIFICATION
# leaves two copies standing and a naive check is green over a live gap. The
# window is the text from the LAST heading matching
# `^#{1,4} (Output|Router Contract|Phase Contract)` that precedes the file's
# FIRST ```yaml fence, up to that fence. Measured: the window exists in all 14
# files, is 202-368B in the 11 that pass and 39-85B in the three QA files.
# Control I-25 is the run that proves the anchoring.
#
# `integration-verifier.md` is EXCLUDED from this PR's file set (P-F7), and an
# unconditional property could in principle force an edit to it. Verified safe
# before widening: its envelope is already at :106 inside its :101->:110 window,
# so no edit is forced. The trade-off is priced and recorded here rather than
# discovered: a NEW agent added without an envelope turns this red, and if that
# agent is out of the editing set, closing it means widening the set. That is
# the intended cost -- an agent the router cannot parse is a defect wherever it
# lives.
AGENTS_DIR = PLUGIN / "agents"
PP22_WINDOW_HEADING = re.compile(
    r"^#{1,4} (?:Output|Router Contract|Phase Contract)\b.*$", re.M
)
PP22_YAML_FENCE = re.compile(r"^```yaml\s*$", re.M)
PP22_ENVELOPE = "CONTRACT {"
# Anti-vacuity floor, asserted BEFORE membership: a glob that stops matching
# yields an empty file list and "every file specifies it" is vacuously true.
# 14 at HEAD. A window that stops matching is the same shape one level down, so
# an empty or absent window is a PRECONDITION failure, never a pass.
PP22_MIN_AGENTS = 14

# PP-23(a). The mutation floor is never VACUOUS. PP-12(a) pins the floor's
# vocabulary and PP-12(b) its magnitude; NEITHER can see a branch whose selected
# UNIT SET is empty. Branch 2 floored only the rows a plan flags
# `At risk of appearing proven: yes`, so a §2c declaring more than 8 properties
# and flagging none selected no units at all, and an empty `MUTATION_CHECKS` met
# the floor. The file already BELIEVED otherwise: its anti-gaming paragraph
# asserts that a plan which "declares them and flags none `at risk`" buys branch
# 3's per-tier-and-per-wave floor. First-matching-branch-wins meant it bought
# branch 2 and nothing. The prose was right and the selector did not implement
# it, so the repair is to the selector.
# Two tokens, one per half of that repair, asserted PER TOKEN PER FILE with a
# per-token message — never one alternation, for PP-12(a)'s recorded reason: a
# single `a|b` search returns >= 1 while one of the two is missing.
PP23A_TOKENS = (
    "at least one `assertion_falsified` is required regardless of which branch applies",
    "falls through to branch 3",
)

# PP-23(b). The review surface is a REQUIRED field, in the rows that decide
# validity. ADR-3 names `ARTIFACTS_CREATED` + `HARNESS_MANIFEST` as the surface
# `qa-review` is dispatched at, in place of BUILD's `git_base_sha` diff package
# (empty by construction, because qa-harness-builder never commits). Measured
# before the fix: NEITHER token appeared anywhere in the hook policy, the
# `MODE: harness` required-field row ended "Every other field in the block stays
# optional", and the agent typed `HARNESS_MANIFEST: "[path]" | null`. Naming two
# absent-or-null fields as a review surface reproduces the empty-diff failure one
# authority over — a dispatch pointing at nothing.
#
# This property exists because a DISPATCH-TEXT-ONLY assertion is green against
# its own defect: a property that only reads the `qa-review` prompt stays green
# while the builder emits neither field. Splitting the claim in two — the
# contract here, the dispatch wording in PP-30(b) — is what makes either half
# falsifiable.
#
# ROW-ANCHORED, never whole-file, in both directions: both tokens appear in the
# agent's own contract block, so a whole-file search over the agent is satisfied
# by the field DECLARATION rather than by the requirement.
# The row anchors are CONJUNCTIONS and the conjunction is load-bearing: the bold
# phrase alone also matches the row immediately below it (`qa-executor` restates
# both), so `| qa-harness-builder |` must be required on the same line.
PP23B_ROW_REQUIRED = ("| qa-harness-builder |", "**`MODE` selects the set.**")
PP23B_ROW_OVERRIDES = ("| qa-harness-builder |", "**This row is a deliberate TIGHTENING.**")
# MODE-ANCHORED inside the row, and this is the subtlest defence here. The
# required-fields row carries the `MODE: harness` AND `MODE: preflight`
# enumerations on ONE physical line separated by `<br>`. "Assert inside the
# located row" is therefore satisfied by the tokens landing in the PREFLIGHT
# sub-list — precisely the mode where `HARNESS_MANIFEST: null` stays legal, so
# the injection that proves the property matters is the one that puts them
# there. The row is sliced at the `MODE: preflight` boundary and only the
# harness slice is searched.
PP23B_HARNESS_MARK = "`MODE: harness` →"
PP23B_PREFLIGHT_MARK = "`MODE: preflight` →"
PP23B_SURFACE_TOKENS = ("`ARTIFACTS_CREATED`", "`HARNESS_MANIFEST`")
PP23B_OVERRIDE_TOKENS = ("non-empty `ARTIFACTS_CREATED`", "non-null `HARNESS_MANIFEST`")
# The nullability half, asserted on the agent's single anchored declaration line
# rather than file-wide: the phrase would otherwise be satisfiable by prose.
PP23B_MANIFEST_LINE = re.compile(r"^HARNESS_MANIFEST:", re.M)
PP23B_MANIFEST_QUALIFIER = "null ONLY in MODE: preflight"

# PP-24. The currency gate's axis is `commits_behind`, and a dirty tree is not on
# it. The gate emitted on `commits_behind > 0` OR a dirty tree and forced
# BLOCKED — and QA over freshly built work has a dirty tree BY CONSTRUCTION, so
# the gate fired on the route's most common trigger. The same agent calls a
# slightly-behind checkout "the ordinary state of a working tree".
#
# The negative half has TWO failure modes, not one — a misspelled forbidden
# token passes forever, and a legitimate use of the phrase inside scope fails
# forever — so, exactly as PP-15(c)'s comment prescribes, the scope is FROZEN to
# the three sites that state the trigger (the agent, the router's validation
# row, and the qa-preflight dispatch text, which restates it verbatim) and the
# spelling is proven by the mandatory re-insertion injection recorded above.
PP24_AXIS_TOKEN = "commits_behind > 0 and for no other reason"
PP24_DIRTY_TRIGGER = "or a dirty tree"
# The POSITIVE field half. Without it the property rewards the wrong fix:
# deleting the `dirty` field outright satisfies "dirty is not a trigger" while
# losing a measurement the route needs. Anchored to the REPO_CURRENCY block of
# the agent's contract, because `dirty:` also appears on the CURRENCY_GATE entry
# and a file-wide search could not tell the two apart.
PP24_REPO_CURRENCY_BLOCK = "REPO_CURRENCY:"
PP24_DIRTY_FIELD = re.compile(r"^\s+dirty:", re.M)


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
    # PP-20 -- every QA DAG node except a declared root has an incoming edge.
    def _decommented(text: str) -> str:
        """Drop HTML comments ONLY. Fences are the graph's normative surface."""
        return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    def _canonical_node(token: str) -> str:
        return PP20_TEMPLATE_SUFFIX.sub("", token)

    dag_text = _decommented(QA_WORKFLOW.read_text(encoding="utf-8"))
    created = {_canonical_node(m) for m in PP20_NODE.findall(dag_text)}
    blocked = {_canonical_node(m) for m in PP20_EDGE.findall(dag_text)}
    # Anti-vacuity, asserted BEFORE membership: a regex that stopped matching
    # yields an empty `created`, and `set() - set() <= ROOTS` is vacuously true.
    # PP-16(c) shipped green in exactly that shape. 12 nodes at HEAD.
    if len(created) < 8:
        pp20_detail = (
            f"PRECONDITION failed: extracted only {len(created)} nodes from "
            f"{QA_WORKFLOW.name} (expected >= 8) — the node regex has stopped "
            f"matching, so any membership result below is vacuous"
        )
        pp20_ok = False
    else:
        unrouted = sorted(created - blocked - QA_DAG_ROOTS)
        pp20_ok = not unrouted
        pp20_detail = (
            f"{len(created)} nodes / {len(blocked)} edges / "
            f"{len(created & QA_DAG_ROOTS)} declared root"
            + (
                ""
                if pp20_ok
                else " — dispatched with no incoming edge: " + ", ".join(unrouted)
            )
        )
    check("PP-20", pp20_ok, pp20_detail)

    # PP-21(a) -- every artifact key the QA law names exists in the skeleton it
    # names, resolved segment by segment to FULL DEPTH.
    skeleton = json.loads(SKELETON.read_text(encoding="utf-8"))

    def _resolve(path: str, depth: int | None = None) -> bool:
        """Walk `path` through the skeleton. depth=None means full depth."""
        segments = path.split(".")
        if depth is not None:
            segments = segments[:depth]
        node = skeleton
        for segment in segments:
            if not isinstance(node, dict) or segment not in node:
                return False
            node = node[segment]
        return True

    key_literals = sorted(set(PP21_KEY_LITERAL.findall(dag_text)))
    if len(key_literals) < PP21_MIN_LITERALS:
        pp21a_ok = False
        pp21a_detail = (
            f"PRECONDITION failed: extracted only {len(key_literals)} artifact-key "
            f"literals from {QA_WORKFLOW.name} (expected >= {PP21_MIN_LITERALS}) — "
            f"the literal regex has stopped matching, so any resolution result "
            f"below is vacuous"
        )
    else:
        unresolved = [k for k in key_literals if not _resolve(k)]
        pp21a_ok = not unresolved
        pp21a_detail = (
            f"{len(key_literals)} artifact-key literals in {QA_WORKFLOW.name}, "
            f"{len(key_literals) - len(unresolved)} resolve at full depth in "
            f"{SKELETON.name}"
            + (
                ""
                if pp21a_ok
                else " — named by the law, absent from the skeleton: "
                + ", ".join(unresolved)
            )
        )
    check("PP-21(a)", pp21a_ok, pp21a_detail)

    # PP-21(b) -- every top-level key the skeleton ships is documented in the
    # hook policy's artifact schema list.
    policy_text = HOOK_POLICY.read_text(encoding="utf-8")
    start = PP21_SCHEMA_LIST_START.search(policy_text)
    end = PP21_SCHEMA_LIST_END.search(policy_text, start.end()) if start else None
    if start is None or end is None:
        pp21b_ok = False
        pp21b_detail = (
            f"PRECONDITION failed: could not slice the artifact schema list out of "
            f"{HOOK_POLICY.name} — the 'Artifact schema must include:' / 'Rules:' "
            f"anchors no longer bracket a section, so any membership result is vacuous"
        )
    else:
        listed = PP21_LIST_ENTRY.findall(policy_text[start.end() : end.start()])
        if len(listed) < PP21_MIN_LISTED:
            pp21b_ok = False
            pp21b_detail = (
                f"PRECONDITION failed: the schema list slice yielded only "
                f"{len(listed)} entries (expected >= {PP21_MIN_LISTED})"
            )
        else:
            undocumented = [k for k in skeleton if k not in set(listed)]
            pp21b_ok = not undocumented
            pp21b_detail = (
                f"{len(skeleton) - len(undocumented)}/{len(skeleton)} skeleton "
                f"top-level keys documented in {HOOK_POLICY.name}"
                + (
                    ""
                    if pp21b_ok
                    else " — shipped by the skeleton, undocumented by the policy: "
                    + ", ".join(undocumented)
                )
            )
    check("PP-21(b)", pp21b_ok, pp21b_detail)

    # PP-21(c) -- QA is a member of the three enums the guard and the router read.
    # Anchored per line; each half fails loudly if its anchor stops matching.
    pp21c_gaps: list[str] = []

    wt_lines = PP21_WORKFLOW_TYPE_LINE.findall(policy_text)
    if len(wt_lines) != 1:
        pp21c_gaps.append(
            f"PRECONDITION: expected exactly 1 `workflow_type` line in "
            f"{HOOK_POLICY.name}, found {len(wt_lines)}"
        )
    elif "QA" not in PP21_ENUM_TOKEN.findall(wt_lines[0]):
        pp21c_gaps.append(
            f"`QA` is not a member of the `workflow_type` enum LINE in "
            f"{HOOK_POLICY.name} (members: "
            f"{', '.join(PP21_ENUM_TOKEN.findall(wt_lines[0]))})"
        )

    ev_head = PP21_EVIDENCE_HEAD.search(policy_text)
    if ev_head is None:
        pp21c_gaps.append(
            f"PRECONDITION: the `evidence` sub-list heading is gone from "
            f"{HOOK_POLICY.name}"
        )
    else:
        ev_agents = []
        for line in policy_text[ev_head.end() :].splitlines()[1:]:
            m = PP21_EVIDENCE_ENTRY.match(line)
            if not m:
                break
            ev_agents.append(m.group(1))
        if len(ev_agents) < 5:
            pp21c_gaps.append(
                f"PRECONDITION: the `evidence` sub-list yielded only "
                f"{len(ev_agents)} agents (expected >= 5)"
            )
        elif "qa_executor" not in ev_agents:
            pp21c_gaps.append(
                f"`qa_executor` is missing from the `evidence` sub-list in "
                f"{HOOK_POLICY.name} (members: {', '.join(ev_agents)})"
            )

    event_lines = [
        line
        for line in SKILL_MD.read_text(encoding="utf-8").splitlines()
        if PP21_EVENT_LOG_LINE in line
    ]
    if len(event_lines) != 1:
        pp21c_gaps.append(
            f"PRECONDITION: expected exactly 1 `{PP21_EVENT_LOG_LINE}` line in "
            f"{SKILL_MD.name}, found {len(event_lines)}"
        )
    else:
        enums = PP21_PHASE_ENUM.findall(event_lines[0])
        if len(enums) != 1:
            pp21c_gaps.append(
                f"PRECONDITION: expected exactly 1 pipe-separated enum on "
                f"{SKILL_MD.name}'s event-log template line, found {len(enums)}"
            )
        elif "qa" not in enums[0].split("|"):
            pp21c_gaps.append(
                f"`qa` is missing from the event-log phase enum in "
                f"{SKILL_MD.name} (members: {enums[0]})"
            )

    check(
        "PP-21(c)",
        not pp21c_gaps,
        "QA is a member of the `workflow_type` enum line, the `evidence` list and "
        "the event-log phase template"
        + ("" if not pp21c_gaps else " — " + "; ".join(pp21c_gaps)),
    )

    # PP-22 -- every agent file specifies the line-1 envelope inside its
    # output-specification window (never a whole-file substring; see I-23).
    agent_files = sorted(AGENTS_DIR.glob("*.md"))
    pp22_precondition = []
    pp22_missing = []
    pp22_sizes = []
    if len(agent_files) < PP22_MIN_AGENTS:
        pp22_precondition.append(
            f"extracted only {len(agent_files)} agent files from "
            f"{AGENTS_DIR.name}/ (expected >= {PP22_MIN_AGENTS}) — the glob has "
            f"stopped matching, so any result below is vacuous"
        )
    else:
        for agent in agent_files:
            text = agent.read_text(encoding="utf-8")
            fence = PP22_YAML_FENCE.search(text)
            if fence is None:
                pp22_precondition.append(f"{agent.name}: no ```yaml fence")
                continue
            headings = [
                m
                for m in PP22_WINDOW_HEADING.finditer(text)
                if m.end() <= fence.start()
            ]
            if not headings:
                pp22_precondition.append(
                    f"{agent.name}: no Output/Router Contract/Phase Contract "
                    f"heading before the first ```yaml fence — the anchor has "
                    f"stopped matching, so this file's result would be vacuous"
                )
                continue
            # The window INCLUDES its own heading line: the boundary is the
            # heading's start, not its end, so a printed window size names a
            # slice a reader can find by eye. Measured at HEAD: 213-369B in the
            # 11 that pass, 40B in the three QA files.
            window = text[headings[-1].start() : fence.start()]
            pp22_sizes.append(len(window))
            if PP22_ENVELOPE not in window:
                pp22_missing.append(f"{agent.name} (window={len(window)}B)")
    if pp22_precondition:
        pp22_ok = False
        pp22_detail = "PRECONDITION failed: " + "; ".join(pp22_precondition)
    else:
        pp22_ok = not pp22_missing
        pp22_detail = (
            f"{len(agent_files) - len(pp22_missing)}/{len(agent_files)} agent files "
            f"specify a line-1 `{PP22_ENVELOPE}...}}` envelope inside their "
            f"output-specification window (windows "
            f"{min(pp22_sizes)}-{max(pp22_sizes)}B)"
            + (
                ""
                if pp22_ok
                else " — no envelope in the output specification of: "
                + ", ".join(pp22_missing)
            )
        )
    check("PP-22", pp22_ok, pp22_detail)

    # PP-23(a) -- the mutation floor is never vacuous. Per token, per file, with
    # a per-token message; see PP23A_TOKENS for why an alternation would not do.
    pp23a_missing: list[str] = []
    for token in PP23A_TOKENS:
        for path in (HARNESS_AGENT, HOOK_POLICY):
            if token not in path.read_text(encoding="utf-8"):
                pp23a_missing.append(f"`{token}` missing from {path.name}")
    check(
        "PP-23(a)",
        not pp23a_missing,
        "the floor minimum binds every branch and branch 2 names its fall-through, "
        "in BOTH qa-harness-builder.md and workflow-artifact-and-hook-policy.md"
        + ("" if not pp23a_missing else " — " + "; ".join(pp23a_missing)),
    )

    # PP-23(b) -- the review surface is required where validity is decided.
    # Three separately named assertions; the row anchors fail on the PRECONDITION
    # rather than passing over an empty row (PP-18's discipline).
    policy_lines = HOOK_POLICY.read_text(encoding="utf-8").splitlines()
    pp23b_precondition: list[str] = []
    pp23b_gaps: list[str] = []

    def _locate_row(anchors: tuple, label: str):
        hits = [ln for ln in policy_lines if all(a in ln for a in anchors)]
        if len(hits) != 1:
            pp23b_precondition.append(
                f"expected exactly 1 {label} row in {HOOK_POLICY.name} matching "
                f"{anchors!r}, found {len(hits)} — the row anchor has stopped "
                f"matching, so any result over it would be vacuous"
            )
            return None
        return hits[0]

    required_row = _locate_row(PP23B_ROW_REQUIRED, "qa-harness-builder required-fields")
    overrides_row = _locate_row(PP23B_ROW_OVERRIDES, "qa-harness-builder overrides")

    harness_slice = ""
    if required_row is not None:
        h = required_row.find(PP23B_HARNESS_MARK)
        f = required_row.find(PP23B_PREFLIGHT_MARK)
        if h < 0 or f < 0 or not h < f:
            pp23b_precondition.append(
                f"could not slice the required-fields row at the `MODE: preflight` "
                f"boundary (harness mark at {h}, preflight mark at {f}) — without "
                f"the slice the tokens could satisfy this check from the PREFLIGHT "
                f"sub-list, which is the one mode where a null manifest is legal"
            )
        else:
            harness_slice = required_row[h:f]
            for token in PP23B_SURFACE_TOKENS:
                if token not in harness_slice:
                    pp23b_gaps.append(
                        f"{token} is not in the `MODE: harness` required-field slice "
                        f"of {HOOK_POLICY.name} (slice={len(harness_slice)}B)"
                    )

    if overrides_row is not None:
        for token in PP23B_OVERRIDE_TOKENS:
            if token not in overrides_row:
                pp23b_gaps.append(
                    f"the qa-harness-builder overrides row of {HOOK_POLICY.name} "
                    f"does not require {token} for STATUS=PASS"
                )

    manifest_lines = [
        ln
        for ln in HARNESS_AGENT.read_text(encoding="utf-8").splitlines()
        if PP23B_MANIFEST_LINE.match(ln)
    ]
    if len(manifest_lines) != 1:
        pp23b_precondition.append(
            f"expected exactly 1 `HARNESS_MANIFEST:` declaration line in "
            f"{HARNESS_AGENT.name}, found {len(manifest_lines)}"
        )
    elif PP23B_MANIFEST_QUALIFIER not in manifest_lines[0]:
        pp23b_gaps.append(
            f"{HARNESS_AGENT.name}'s HARNESS_MANIFEST declaration does not restrict "
            f"`null` to MODE: preflight (line: {manifest_lines[0].strip()!r})"
        )

    if pp23b_precondition:
        pp23b_ok = False
        pp23b_detail = "PRECONDITION failed: " + "; ".join(pp23b_precondition)
    else:
        pp23b_ok = not pp23b_gaps
        pp23b_detail = (
            f"ARTIFACTS_CREATED and HARNESS_MANIFEST are required in the "
            f"`MODE: harness` slice of the required-fields row "
            f"(slice={len(harness_slice)}B), non-empty/non-null for STATUS=PASS in "
            f"the overrides row, and `null` is restricted to MODE: preflight in "
            f"{HARNESS_AGENT.name}"
            + ("" if pp23b_ok else " — " + "; ".join(pp23b_gaps))
        )
    check("PP-23(b)", pp23b_ok, pp23b_detail)

    # PP-24 -- the currency gate's axis is commits_behind; a dirty tree is a
    # measured fact, never a trigger. Positive phrasing in all three sites,
    # forbidden coupling in none of them, and `dirty` still a REPO_CURRENCY field.
    qa_law_lines = QA_WORKFLOW.read_text(encoding="utf-8").splitlines()
    dispatch_hits = [
        ln
        for ln in qa_law_lines
        if "phase:qa-preflight" in ln and 'description: "' in ln
    ]
    pp24_precondition: list[str] = []
    pp24_gaps: list[str] = []
    if len(dispatch_hits) != 1:
        pp24_precondition.append(
            f"expected exactly 1 qa-preflight dispatch `description:` line in "
            f"{QA_WORKFLOW.name}, found {len(dispatch_hits)} — the anchor has "
            f"stopped matching"
        )
    if overrides_row is None:
        pp24_precondition.append(
            f"the qa-harness-builder overrides row of {HOOK_POLICY.name} was not "
            f"located (see PP-23(b)); PP-24's policy site is therefore unscoped"
        )

    if not pp24_precondition:
        harness_text_now = HARNESS_AGENT.read_text(encoding="utf-8")
        sites = (
            (HARNESS_AGENT.name, harness_text_now),
            (f"{HOOK_POLICY.name} (qa-harness-builder overrides row)", overrides_row),
            (f"{QA_WORKFLOW.name} (qa-preflight dispatch text)", dispatch_hits[0]),
        )
        for label, text in sites:
            if PP24_AXIS_TOKEN not in text:
                pp24_gaps.append(
                    f"{label} does not state the gate's axis "
                    f"(`{PP24_AXIS_TOKEN}` absent)"
                )
            if PP24_DIRTY_TRIGGER in text:
                pp24_gaps.append(
                    f"{label} still couples a dirty tree to the gate trigger "
                    f"(`{PP24_DIRTY_TRIGGER}` present)"
                )
        # the positive field half, block-anchored
        start = harness_text_now.find(PP24_REPO_CURRENCY_BLOCK)
        if start < 0:
            pp24_precondition.append(
                f"no `{PP24_REPO_CURRENCY_BLOCK}` block found in "
                f"{HARNESS_AGENT.name}"
            )
        else:
            # scan from the line AFTER the block heading: position 0 of a slice
            # always matches `^` under re.M, which silently yields a 1-byte
            # "block" that no `dirty:` line can be inside. Observed once, here.
            body_at = harness_text_now.index("\n", start) + 1
            nxt = re.search(r"^\S", harness_text_now[body_at:], re.M)
            block = harness_text_now[
                start : (body_at + nxt.start()) if nxt else len(harness_text_now)
            ]
            if not PP24_DIRTY_FIELD.search(block):
                pp24_gaps.append(
                    f"`dirty` is no longer a REPO_CURRENCY field in "
                    f"{HARNESS_AGENT.name} (block={len(block)}B) — demoting the "
                    f"trigger must not delete the measurement"
                )

    if pp24_precondition:
        pp24_ok = False
        pp24_detail = "PRECONDITION failed: " + "; ".join(pp24_precondition)
    else:
        pp24_ok = not pp24_gaps
        pp24_detail = (
            "all three sites gate on commits_behind alone, none couples a dirty "
            "tree to the trigger, and `dirty` is still a REPO_CURRENCY field"
            + ("" if pp24_ok else " — " + "; ".join(pp24_gaps))
        )
    check("PP-24", pp24_ok, pp24_detail)

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
