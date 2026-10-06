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
      (c) QA is a member of the five enums the guard and the router read --
      the `workflow_type` enum LINE, the `evidence` agent list, and all THREE
      of SKILL.md's phase-enum lines (the event-log template, the
      parent-workflow `TaskCreate` template, and the `__PHASE__` substitution
      list) -- each asserted on its anchored line, never whole-file.
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
PP-25 the QA route's two re-dispatch loops are BOUNDED and COUNTED: (a) each
      loop states a numeric cap AND a named exhaustion state, asserted inside
      that loop's own bold-lead-in-anchored window, because the word "cap"
      appears in both and a file-wide test lets one satisfy the other;
      (b) the `kind:remfix` block mandates the `remediation_history` append, in
      the `{ts, phase, reason, cycle_number}` shape the hook-enforced circuit
      breaker counts. Without (b) the breaker counts 0 forever and QA's cap of
      2 is LLM-counted with no backstop at all
PP-26 no QA finding reaches the executor unconsumed and no Minor evaporates,
      and the carve-out that makes that possible names its parent BOTH WAYS:
      (a) the QA remediation block is uniquely line-anchored and, INSIDE ITS OWN
      window, names the triggering verdicts, the halted phase, the target phase
      `re-qa-build`, the `origin:` value and the `deferred_findings` sink --
      plus, in the same check id, the sink's own schema entry in the hook policy
      names QA's surfacing point, without which the route writes to an array
      whose documented reader is a BUILD-DONE triage ADR-2 removed;
      (b) TWO SEPARATELY-FAILING halves -- the QA block cites
      `remediation-and-research.md`'s rule matrix and re-review loop by section,
      AND SKILL.md's own `## 11.` section (the line a router actually executes
      when a `kind:remfix` completes) carries the reciprocal QA exception. One
      direction is not enough: a carve-out stated only in qa-workflow.md is
      invisible from the point of execution, and unqualified §11 re-reviews a
      completed `re-qa-build` through a precondition gate `qa-harness-builder`
      cannot satisfy -- it fails CLOSED on a correct QA remfix and hangs the run
PP-27 no QA phase holds a write tool without a stated product-code boundary,
      and every QA phase runs under the gate that governs phase exit:
      (a) all THREE statements of the no-product-code rule are exhaustive IN
      FACT -- each names the planner alongside the researcher, harness builder
      and executor, because `cc10x:planner` runs `qa-plan`/`qa-re-plan` holding
      `Edit, Write, Bash` -- and both plan-phase dispatch windows carry the
      boundary. Per SITE and per FILE, bullet-anchored: `planner` occurs 16x in
      SKILL.md alone, so a whole-file test is green against every injection this
      exists to catch;
      (b) `phase_exit_gate` names QA where it is INVOKED, anchored on the
      per-agent loop's `for <routes>, run` line -- never whole-file, and never
      the route-neutral inline-fallback invocation
PP-28 a defect found at any QA phase reaches the sink the DEBUG offer reads:
      the *Persist first* window merges preflight's `BUG_CANDIDATES` from
      `qa.preflight` into `qa.bug_candidates` on PREFLIGHT return, not only on
      the executor's. Both keys verbatim -- a merge with one key misspelled is
      the drift PP-21(a) already caught once in this same file
PP-29 every filesystem path the QA law NAMES resolves on disk: backticked
      path-shaped tokens from qa-workflow.md and SKILL.md's QA LINES (a frozen
      regex, not prose), resolved against FOUR bases -- repo root,
      plugins/cc10x/, ${CLAUDE_PLUGIN_ROOT}, and the directory of the file that
      named the token. The fourth base is not optional: `references/qa-workflow.md`
      resolves under none of the other three. Templated (`{...}`) and
      glob-bearing (`*`) tokens are excluded, frozen, and both exclusions were
      measured rather than assumed. P10 was one dangling RFC pointer; this is
      that correction made mechanical, so the next one is caught the day it is
      written
PP-30 the two surface corrections ADR-2 and ADR-3 part 3 decide: (a) QA offers
      no workspace isolation AND SAYS WHY -- a negative half over the offer's
      vocabulary and a positive half over the rationale block, BOTH required,
      because a negative alone rewards silent deletion and ADR-2's whole point
      is that the absence is argued; (b) both harness-review dispatches NAME
      their review surface (`ARTIFACTS_CREATED`, `HARNESS_MANIFEST`), asserted
      inside each dispatch's OWN window -- the two blocks share one ```text
      fence and both tokens live in qa-harness-builder.md, so anything wider is
      trivially satisfied. (b) is dispatch text ONLY; that the fields are
      required is PP-23(b)'s job, and the contrast run below is the measurement
      of why the split is not redundancy
PP-22 every agent file SPECIFIES the line-1 `CONTRACT {` envelope inside its
      OUTPUT SPECIFICATION -- the window from the last
      Output/Router Contract/Phase Contract heading before the file's first
      ```yaml fence, up to that fence. Unconditional over
      `plugins/cc10x/agents/*.md`: 11/14 at HEAD, 14/14 after. An agent that
      specifies no envelope leaves SKILL.md §8's verdict extraction with a
      heading scan that finds nothing, so the router trips inline verification
      on every lane of that agent.
PP-31 the QA phase-token spellings are FROZEN and the freeze CITES ITS REASON:
      the QA slice of the SKILL.md §3 phase enum equals a module-level frozen
      set, AND the ADR-1 naming-rationale block is anchored in qa-workflow.md
      carrying every clause of the argument. It is a TRIPWIRE, not a
      behavioural proof: its value is the argument it forces a future editor to
      read before renaming. The asymmetry (`qa-re-plan` prefixed where
      `re-qa-build`/`re-qa-execute` are infixed) is deliberate and PRICED, and
      editing the frozen constant to make a rename green is the WHOLE COST of
      the rename, not a formality -- see the constant's comment, and control
      I-45, which measures that cost
PP-32 EVERY DELIBERATE OMISSION IN THE QA LAW CARRIES ITS RATIONALE IN THE SAME
      BLOCK: three omissions -- probe drops plan review, no amendment lane, no
      `re-qa-preflight` -- each window-anchored to the block that makes it,
      because a file-wide test lets any one satisfy the others. This encodes
      something the route already does well and converts a culture into a
      check. The FOURTH omission (no workspace isolation) is PP-30(a)'s
      positive half and is deliberately NOT re-asserted here
PP-33 QA IS A MEMBER OF EVERY ENUMERATION OF WORKFLOW TYPES, and the
      extractors that find those enumerations still find them. Four sites in
      four syntactic shapes (parens+pipes, SQUARE+pipes, parens+COMMAS, and a
      bare marquee count) read under the normaliser each one's fence position
      demands. The guard returns 0 unless `workflow_type == "QA"`, so a router
      that never stamps QA makes every rule in qa-workflow.md unreachable in
      production -- fail-open by omission rather than by logic. (a) is the
      anti-vacuity half: every anchor matched exactly once, every extractor
      still yielded members, the routing table still has rows, and the stamping
      SHAPE is proved live on the two sibling route files that already carry it

PP-34 THE GUARD RESOLVES A PHASE FROM EVERY status_history SHAPE WITHOUT
      CRASHING, and rc/stderr are part of the verdict. A PreToolUse hook that
      raises exits non-zero with no decision on stdout, and a hook that emits
      no decision FAILS OPEN -- so a crash is indistinguishable from a
      deliberate allow to any property that reads the decision alone. Six
      shapes, each asserted as the triple (rc == 0, stderr == "", decision),
      all with `phase_cursor` absent because that is the only state in which
      status_history is consulted at all. (d) is the positive control: five of
      the six expect ALLOW and a guard that crashes on everything also allows
      everything, so without a case that must DENY the property is green on a
      wholly broken guard.

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

Negative controls for PP-25 (three runs, all red, plus one CONTRAST run that is
the argument for the property rather than a test of it). The two defects are the
two ways a retry loop goes wrong -- unbounded, and uncounted:
  I-32 the `remediation_history` bullet deleted whole from the `re-qa-build`
       block -- the M3 defect itself, restored
                                          -> PP-25(b) red: "0/2 tokens ...
                                             missing ['`remediation_history`',
                                             '`{ts, phase, reason,
                                             cycle_number}`']", window 3640B ->
                                             2609B, with PP-25(a) and the other
                                             39 checks green.
  I-33 THE CONTRAST, AND IT IS THE ONE THAT MATTERS. With I-32 still in place,
       the shipped skeleton was loaded, given a `wf`, written into a temp
       project, and the task-completed guard invoked as a subprocess on a
       `kind:remfix` completion under `taskMetadata: block`
                                          -> the artifact re-reads as valid
                                             JSON, `remediation_history` is
                                             `[]`, and the guard exits **0**
                                             with EMPTY stderr.
       So NO EXISTING CHECK CATCHES THIS, and that is the whole argument for
       PP-25(b)'s scope. The auditor's stated mechanism -- the guard "faults
       when remediation_history is not a list" -- is wrong twice over: the
       branch logs an audit event and `return 0` rather than faulting, and it is
       UNREACHABLE anyway because the skeleton ships `[]`, which IS a list. An
       invariant over the array's TYPE would therefore be green at HEAD *and*
       green against the defect. Only an invariant over the APPEND DUTY IN THE
       LAW can see it, which is why PP-25(b) has the scope it has.
  I-34 the numeric cap removed from the PREFLIGHT window ONLY (`**Cap: 2
       re-dispatches...` -> `**Cap the re-dispatches...`), leaving the
       `re-qa-build` block's `**Cap: 2 extra rounds` untouched
                                          -> PP-25(a) red naming the PREFLIGHT
                                             window alone ("the qa-preflight
                                             re-dispatch loop states 0 numeric
                                             caps (none) ... window=3024B")
                                             while reporting the re-qa-build
                                             window GREEN at cap=['2'] in the
                                             same detail string.
       MANDATORY: it is the run that proves the WINDOWING. Both blocks contain
       the word "cap", so a whole-file test -- the obvious way to write this
       property -- is GREEN against this injection, the surviving sibling
       satisfying the deleted one's half. That is PP-18's recorded I-2 shape in
       a fourth file, and it is why each loop is bracketed by its own pair of
       bold lead-ins rather than searched for in the file. It also shows why the
       cap is matched as a NUMBER: the injected wording still claims a cap.
Window sizes at the green state, recorded because a later phase deletes a fenced
block from this same file and its only mitigation is a before/after comparison
of exactly these numbers: PP-25(a) preflight window = 3023B; PP-25(a) and (b)
re-qa-build window = 3640B. Both are measured over `_normative()` text, and the
re-qa-build window CONTAINS a fenced block -- which is precisely why it is a
measurement there and a control for the preflight window, which sits earlier in
the file than any deletion and cannot move.

Negative controls for PP-27, PP-28 and the PP-21(c) extension (four runs, all
red, each naming the injected thing; two of the four carry a CONTRAST that is
the argument for the anchoring rather than a test of it):
  I-35 `planner` deleted from the SKILL.md statement of the no-product-code rule
       ONLY, leaving both qa-workflow.md statements corrected
                                          -> PP-27(a) red naming `SKILL.md
                                             (Never let QA edit product code)`
                                             ALONE: "enumerates 3/4 agents
                                             holding write tools in QA: missing
                                             ['planner'] (bullet=303B)", with
                                             the other two sites and both
                                             dispatch windows reported green in
                                             the same detail string. Bullet
                                             404B -> 303B.
       PER-FILE, PER-SITE naming is the point, not a nicety: the rule is stated
       three times across two files, and a red that says "some site omits the
       planner" sends the next reader to grep three windows in two files.
       CONTRAST, and it is why the property is bullet-anchored rather than
       file-scoped: with the injection in place `grep -c planner SKILL.md` still
       returns 16. A whole-file substring test -- the obvious way to write this
       -- is GREEN against this injection sixteen times over. PP-14's recorded
       trap, in a fifth file.
  I-36 the `phase_exit_gate` invocation line moved back to BUILD-only
       (`- for BUILD and QA, run` -> `- for BUILD, run`)
                                          -> PP-27(b) red: "the per-agent loop
                                             runs `phase_exit_gate` for BUILD
                                             ... missing ['QA']" (line 45B ->
                                             38B).
       CONTRAST, MANDATORY, and it is the whole reason the property is anchored
       on one line. With the injection in place `phase_exit_gate` still occurs
       FIVE times in SKILL.md -- the router-owned gates list (:105), this line
       (:602), the phase-cursor rule (:636), the inline-fallback section (:700)
       and the terse-imperative rule (:763) -- and `"phase_exit_gate" in text
       and "QA" in text` evaluates True. Every file-wide construction of this
       property is GREEN against the defect, which is PP-14's trap exactly. The
       `for <routes>, run` shape in the anchor is also what keeps the property
       off :700, whose route-neutrality ("exactly as in the default loop step
       6") is deliberate and must not be narrowed to a route list.
  I-37 the preflight merge paragraph deleted whole from the *Persist first*
       block, leaving the executor sentence -- which already names
       `qa.bug_candidates` -- standing
                                          -> PP-28 red: "missing
                                             ['`qa.preflight`', 'On
                                             `qa-harness-builder` preflight
                                             return']", window 959B -> 317B.
       The surviving executor sentence is why the SOURCE key and the
       preflight-return lead-in are asserted alongside the destination: a
       property asserting only `qa.bug_candidates` is GREEN at the pre-fix state,
       because the sink was always named -- what was missing was the second
       writer into it. CONTRAST: `grep -c 'qa\\.preflight'` on the file still
       returns 3 under the injection, so a whole-file key test is green too.
  I-38 `qa` removed from the `__PHASE__` substitution list -- ONE of the three
       anchored SKILL.md phase-enum lines, leaving the event-log template and
       the parent-workflow `TaskCreate` template correct
                                          -> PP-21(c) red naming that line
                                             specifically ("`qa` is missing from
                                             the `__PHASE__` substitution list
                                             phase enum ... members:
                                             build|debug|review|plan|orient|
                                             triage|codebase-health") with the
                                             other two halves green and no other
                                             check disturbed.
       This is the run that justifies EXTENDING PP-21(c) over three lines rather
       than adding a fourth check id. The three lines are one fact stated three
       times; when the property guarded only the event-log template, the other
       two drifted for a whole revision with the suite green at 41. A property
       that blesses one of three sites is the defect this phase closes, so
       reproducing that shape in the property closing it would have been a
       strange choice. The check-id count is unchanged by the extension.
Window sizes at the green state, recorded for the same reason PP-25's are -- a
later phase deletes a fenced block from qa-workflow.md and its only mitigation
is a before/after comparison of exactly these numbers:
  PP-27(a) SKILL.md bullet                = 404B   (control: other file)
  PP-27(a) QA-specific-rules bullet       = 1157B  (measurement: downstream)
  PP-27(a) qa-build-rules bullet          = 192B   (control: upstream of the
                                                    fence, cannot move)
  PP-27(a) qa-plan dispatch window        = 1873B  (control: upstream)
  PP-27(a) qa-re-plan dispatch window     = 1188B  (control: upstream)
  PP-27(b) invocation line                = 45B    (control: other file)
  PP-28  *Persist first* window           = 959B   (measurement: downstream)
PP-27(a)'s windows are measured over `_decommented()` text and PP-28's over
`_normative()`; only the two marked as measurements sit after the deletion point
and can move at all.

Negative controls for PP-29 and PP-30 (six runs, all red, each naming the
injected thing; two of the six are the runs that carry the design and neither
tests the property so much as justifies its shape):
  I-39 a worktree-offer sentence re-added above the rationale block
                                          -> PP-30(a) red on the NEGATIVE half
                                             alone, naming all four forbidden
                                             offer patterns with their line
                                             numbers, while the same detail
                                             string reports the rationale block
                                             green at 866B.
  I-40 THE ONE THAT PROVES THE PROPERTY DOES NOT REWARD SILENT DELETION, AND IT
       IS MANDATORY. The 866-byte rationale block deleted whole, the offer left
       absent -- i.e. M6 "fixed" by deleting step 0 and saying nothing
                                          -> PP-30(a) red on the POSITIVE half,
                                             "0/4 forbidden offer patterns ...
                                             the absence is then UNARGUED".
       A purely negative property -- which is the obvious way to write this --
       is GREEN against this, and green is exactly wrong: the next reader finds
       an unexplained absence, reads BUILD's step 0, and puts the offer back.
       ADR-2's argument is the artifact, not the deletion.
  I-41 `references/qa-mutation-floor.md` cited in qa-workflow.md, no such file
                                          -> PP-29 red naming the token and the
                                             file that names it, 5/6 resolving.
       This reproduces P10's defect in its own class rather than restoring the
       RFC line, so the property is shown to catch the CLASS and not one string.
  I-42 `HARNESS_MANIFEST` deleted from the `qa-hunt` dispatch ONLY
                                          -> PP-30(b) red naming `qa-hunt`
                                             (window 679B -> 635B) with
                                             `qa-review` reported green at 479B
                                             in the same detail string.
       CONTRAST: under the injection `grep -c HARNESS_MANIFEST qa-workflow.md`
       still returns 1, and both dispatch blocks live inside ONE ```text fence,
       so a whole-file test and a whole-fence test are both green. PP-18's
       recorded I-2 shape, now one nesting level in from PP-23(b)'s whole-ROW
       version of it.
  I-43 THE CONTRAST PP-23(b)'s OWN PHASE COULD NOT RUN, AND IT IS THE
       MEASUREMENT THAT JUSTIFIES SPLITTING M7 ACROSS TWO PHASES. With the
       dispatch text landed, `ARTIFACTS_CREATED` was deleted from the
       `MODE: harness` required-field slice of the hook-policy row (I-29 again)
                                          -> PP-23(b) red on the slice (435B ->
                                             414B) while PP-30(b) stayed GREEN.
       So a dispatch-text-only property is perfectly green while the field it
       promises the reviewer is OPTIONAL -- a prompt pointing at nothing, which
       is the same failure as BUILD's empty diff package one authority over.
       Neither half can be "improved" into the other: PP-30(b) cannot see an
       optional field, and PP-23(b) cannot see a dispatch that never points at
       it. The earlier phase recorded that this run was owed; this is it.
  I-44 the glob entry removed from PP29_EXCLUDE, i.e. the exclusion set written
       the way revision 1 of the property specified it
                                          -> PP-29 red naming
                                             `.cc10x/workflows/*.json`.
       MANDATORY: it proves the exclusion is LOAD-BEARING rather than defensive
       decoration. A glob names a runtime family under a state root absent from
       a clean checkout, so the property would have been red at HEAD, forever,
       on a token that is not a defect.

The M12 fence deletion, and the measurement that cleared it (Phase 8). The
stray empty ```text/``` pair was deleted from qa-workflow.md. `_normative()`
consumes fenced blocks in sequential non-greedy pairs, so a deletion that broke
parity would silently re-pair every later fence and leave every window-anchored
property green OVER DIFFERENT TEXT. The fence was located dynamically (its line
number had moved three times across earlier phases: 290 -> 296 -> 309 -> 317)
and confirmed to be the ONLY empty pair; the fence-line count was 36 before and
34 after, even on both sides. Every quantity below was re-measured immediately
before the deletion and again immediately after, and the deletion was made in
ISOLATION -- no other edit in the same step -- because an earlier edit in this
same phase (deleting a stale `:341` line reference) had already moved the
re-qa-build window from 3640B to 3626B, and a confounded comparison measures
nothing:
  PP-18(a) window                      2187B -> 2187B  (control: upstream)
  PP-18(b) body                        1907B -> 1907B  (control: upstream)
  PP-18(c) scope                       2046B -> 2046B  (control: upstream)
  PP-25(a) preflight window            3023B -> 3023B  (control: upstream)
  PP-25(a)/(b) re-qa-build window      3626B -> 3626B  (MEASUREMENT: downstream,
                                                        and it CONTAINS a fence)
  PP-27(a) QA-specific-rules bullet    1157B -> 1157B  (MEASUREMENT: downstream)
  PP-28 *Persist first* window          959B ->  959B  (MEASUREMENT: downstream)
  PP-30(b) qa-review / qa-hunt windows  479B/679B -> 479B/679B (downstream;
                                                        established this phase)
The four controls sit before the deletion point and `re.sub` scans left to
right, so they CANNOT move -- reporting them as evidence would be claiming
measurement where only control is held. The three genuine measurements are the
ones that clear the risk.

Negative controls for PP-26 (five runs; four red and each naming the injected
thing, plus I-52, whose subject is a PRE-EXISTING property and whose red is the
evidence for a decision rather than for PP-26. I-50 is recorded with the run
that FAILED to go red, because that failure is what shaped the property):
  I-49 the `deferred_findings` bullet deleted whole from the QA remediation
       block, the rest of the block intact -- i.e. P8 left open while P1 and M8
       are closed
                                          -> PP-26(a) red naming the missing
                                             token and the file: "qa-workflow.md:
                                             the QA remediation block does not
                                             name ['`deferred_findings`']
                                             (window=4293B)", window 4961B ->
                                             4293B, with the hook-policy sink
                                             bullet reported green at 442B in
                                             the same detail string and PP-26(b)
                                             undisturbed.
  I-50 THE RUN THAT WENT GREEN FIRST, AND IT IS WHY THE TOKEN TUPLE HAS FOUR
       MEMBERS INSTEAD OF THREE. The §11 citation deleted from the carve-out
       sentence only, leaving the rule-matrix citation in place
                                          -> first attempt: PP-26(b) GREEN. The
                                             block ALSO names
                                             `## 11. Re-Review Loop` in its
                                             closing pointer at SKILL.md's
                                             section of that name, and a
                                             substring test cannot tell a
                                             citation of the kernel's §11 from a
                                             pointer at SKILL.md's §11. PP-18's
                                             recorded I-2 shape one more time,
                                             and it survived inside a 4.9KB
                                             WINDOW, which is the part worth
                                             recording: windowing is not by
                                             itself a defence when the window is
                                             large enough to hold both mentions.
       `### Re-review precondition gate` was then added to PP26B_QA_TOKENS -- it
       is the sub-block of the KERNEL's §11 that actually fails closed on a QA
       remfix, it occurs exactly once, and SKILL.md's pointer has no reason to
       name it. Re-run of the same injection
                                          -> PP-26(b) red on DIRECTION 1 alone:
                                             "direction 1 (qa-workflow.md ->
                                             kernel): the QA carve-out does not
                                             cite what it carves out of --
                                             missing ['### Re-review
                                             precondition gate']
                                             (window=4867B)", with the SKILL.md
                                             §11 section reported green at 684B
                                             and PP-26(a) green.
  I-51 SF-7's control, and the pair I-50/I-51 is what makes "both directions" a
       measurement rather than a sentence. The QA exception clause deleted from
       SKILL.md's `## 11.` section ONLY, the QA block left whole -- i.e. ADR-4
       implemented exactly as ADR-4 was written, before SF-7 found the kernel
       side
                                          -> PP-26(b) red on DIRECTION 2 alone:
                                             "direction 2 (SKILL.md §11 -> QA):
                                             the kernel line a router executes
                                             on a completed `kind:remfix`
                                             carries no QA exception -- missing
                                             ['re-qa-build', 'qa-workflow.md',
                                             'exception'] (section=135B)",
                                             section 684B -> 135B, with
                                             direction 1 green at 4961B and
                                             PP-26(a) green.
       The two directions therefore fail independently and neither can mask the
       other. A single-direction property would have shipped green over the
       exact state that hangs a run.
  I-52 THE VOCABULARY CONTROL, and its subject is PP-16, not PP-26. The origin
       rationale in the new block rewritten from "`failure-hunter` is not a
       member of the §3 `origin:` enum" to "`origin:failure-hunter` is not a
       member ..." -- i.e. the rejected alternative written out as a concrete
       dispatch value
                                          -> PP-16 red: "origin:failure-hunter
                                             is written but not declared in the
                                             origin enum", extracted origins
                                             5 -> 6, with PP-4 and PP-5 green
                                             (no phase token was invented) and
                                             both PP-26 checks green.
       This is stronger evidence for the origin decision than the prose is: the
       guard that would have caught the enum extension is shown catching it, and
       it also fixes the wording rule for this block -- the rejected value may be
       discussed by AGENT NAME but never written as `origin:<value>`, because
       PP-16 reads concrete values out of every file in references/.
  I-53 SF-8's control. The QA surfacing point deleted from the
       `deferred_findings` schema bullet in the hook policy, restoring its HEAD
       text ("surfaced once at BUILD-DONE triage, never consumed mid-flight"),
       with the QA block still writing to the array
                                          -> PP-26(a) red on the SF-8 half
                                             alone: "the `deferred_findings`
                                             schema bullet does not name QA's
                                             surfacing point -- missing ['QA',
                                             'DEBUG offer', 'report']
                                             (bullet=261B); as written the
                                             array's only documented reader is a
                                             BUILD-DONE triage this route does
                                             not run", bullet 442B -> 261B, with
                                             the qa-workflow.md window half
                                             green at 4961B and PP-26(b) green.
       MANDATORY, and not decoration: without this half PP-26(a) is green over a
       route that appends Minors to a sink its own schema says nobody on this
       route reads -- P8 closed in appearance and open in fact.
Window sizes at the green state: PP-26(a)/(b) qa-workflow.md block = 4961B;
PP-26(a) hook-policy sink bullet = 442B; PP-26(b) SKILL.md §11 section = 684B.
The QA block sits DOWNSTREAM of the point where Phase 8's stray fence used to
be, but that deletion has already happened, so 4961B has no pre-deletion value
to compare against and none is offered as one -- I-49 and I-50 are its
validation instead, each moving it by the exact size of the text removed.

Negative controls for PP-31 and PP-32 (four runs: three red and naming the
injected thing, plus I-48, which is a control on the SPLIT between PP-32 and
PP-30(a) and whose correct result is PP-32 GREEN. I-45 is run in two STAGES and
the second stage is the evidence for ADR-1's central claim rather than a test of
PP-31):
  I-45 THE RENAME, PERFORMED THE WAY A RENAMER WOULD PERFORM IT. Stage (a):
       `qa-re-plan` -> `re-qa-plan` in the SKILL.md §3 phase enum ONLY
                                          -> PP-31 red naming BOTH sides of the
                                             drift ("unexpected
                                             ['re-qa-plan'], missing
                                             ['qa-re-plan']") and pointing the
                                             reader at ADR-1, with PP-4 red
                                             sympathetically because
                                             qa-workflow.md still writes
                                             `phase:qa-re-plan`. PP-2 stays
                                             GREEN at this stage, and that is a
                                             measurement, not an omission: PP-2
                                             reads
                                             `cc10x_qa_isolation_guard.PLAN_PHASES`,
                                             which a SKILL.md edit does not
                                             touch.
       Stage (b): the rename COMPLETED -- `phase:qa-re-plan` rewritten in
       qa-workflow.md and `"qa-re-plan"` rewritten in the guard's PLAN_PHASES,
       which a real rename MUST do or the renamed phase silently stops being
       read-only
                                          -> PP-31 red as before AND PP-2 red:
                                             "no plan phase lost from
                                             PLAN_PHASES (missing:
                                             ['qa-re-plan'])". PP-4 returns to
                                             green, so the pair PP-31 + PP-2 is
                                             the whole signal.
       THE SYMPATHETIC RED IS THE ARGUMENT. The only way to make PP-2 green
       again is to edit EXPECTED_PLAN_PHASES -- the constant PP-2 asserts
       against -- which is indistinguishable from defeating the property. That
       is ADR-1's central claim, and it is recorded here as a measurement rather
       than an assertion because the brief for this property specified only
       stage (a), under which PP-2 does NOT move. A one-stage control would have
       recorded ADR-1's strongest argument as unproven.
       Also observed under the injection: PP-5 stays green, because it filters
       enum members with `startswith("qa")` and `re-qa-plan` no longer matches.
       So the dispatcher-row property goes BLIND to a token the moment it is
       renamed out of the `qa` prefix -- a fourth surface the rename would
       quietly unguard, and one nobody had enumerated.
  I-46 the ADR-1 rationale block absent, the frozen set correct -- i.e. PP-31
       written as a token freeze with no anchored argument, which is how it
       would have shipped if the second half had been left out
                                          -> PP-31 red on the RATIONALE half
                                             ("not present exactly once in the
                                             NORMATIVE text ... 0 matches"),
                                             observed at the RED step of this
                                             phase before the block was written.
       The two halves are asserted in ONE check id on purpose: a freeze whose
       reason has been deleted is a rule with no reason attached, and that is
       precisely the "tidy it up" invitation the property exists to refuse.
  I-47 the P9 justification paragraph deleted whole from the reduced-task-graph
       block, the omission itself left in place -- i.e. probe drops plan review
       and says nothing, the pre-fix state
                                          -> PP-32 red naming the probe window
                                             alone: "the `probe drops plan
                                             review` omission is made but NOT
                                             argued in place: missing
                                             ['`build_scope=trivial`',
                                             'anti-anchoring'] (window=1526B)",
                                             with `no amendment lane` (722B) and
                                             ``no `re-qa-preflight``` (260B)
                                             reported green in the same detail
                                             string and no other check
                                             disturbed. Window 2754B -> 1526B.
       CONTRAST, and it is why the property is windowed per omission rather than
       written as a file-wide token test. Under the injection
       `grep -c anti-anchoring qa-workflow.md` still returns 2 and
       `grep -c SCOPE_INCREASES` still returns 4, so a whole-file test over
       three of the four tokens is GREEN against this injection; only
       `build_scope=trivial` is unique to the block. PP-18's recorded I-2 shape,
       and PP-25(a)'s I-34 in this same file, for a third time.
  I-48 the ADR-2 rationale block deleted -- the fourth omission, the one PP-32
       deliberately does NOT assert
                                          -> PP-30(a) red on its positive half
                                             (this is I-40, re-run at this phase
                                             to confirm the division of labour
                                             still holds) and PP-32 GREEN.
       Recorded as a control on the SPLIT rather than on either property: PP-32
       staying green here is correct, not a gap, because two properties owning
       one fact is the duplication that made the byte-duplicated PASS rule a
       trap. If PP-30(a) is ever narrowed to its negative half, PP32_OMISSIONS'
       comment is where the missing fourth omission is recorded.
Window sizes at the green state: PP-31 rationale block = 1687B; PP-32 probe
window = 2754B, amendment-lane window = 722B, `re-qa-preflight` window = 260B.
These are established AFTER Phase 8's fence deletion, so none of them has a
pre-deletion value to compare against and none is offered as one -- I-47 is
their validation instead, which is the right instrument for a window that was
never measured on the other side of that change.

Negative controls for PP-33 (eight runs, each restored and re-greened before
the next). The first four are one per SITE, because four shapes need four
injections: revision 1 of this property was a single paren regex with a single
injection, under which three of the four sites could have been reverted with
the property still green:
  I-54 ` QA |` deleted from the paren enum at cc10x-router/SKILL.md:276
                                          -> PP-33(b) red naming the site and
                                             printing what it did parse: "S1
                                             cc10x-router/SKILL.md paren enum
                                             omits QA (members=['BUILD',
                                             'DEBUG', 'REVIEW', 'PLAN',
                                             'ORIENT', 'TRIAGE',
                                             'CODEBASE-HEALTH'])", PP-33(a)
                                             green.
  I-85 ` QA |` deleted from the bracket enum at memory-file-contracts.md:103
                                          -> PP-33(b) red: "S2
                                             memory-file-contracts.md bracket
                                             enum omits QA". THE SQUARE
                                             BRACKETS ARE THE WHOLE POINT: the
                                             paren regex that catches S1 never
                                             reaches this line, so before the
                                             site table this site had no
                                             control at all.
  I-86 cc10x-guide/SKILL.md reverted to `4 workflows (BUILD, DEBUG, REVIEW,
       PLAN)`                             -> PP-33(b) red on the membership
                                             half ALONE: "S3
                                             cc10x-guide/SKILL.md paren+comma
                                             enum omits QA".
       ONE RED, NOT TWO, and the difference is recorded rather than smoothed
       over. The brief for this control predicted two -- membership AND the
       count/len mismatch -- but a revert of the WHOLE site moves the integer
       and the member list together, so 4 == len([4 members]) and the
       cardinality clause is satisfied by the defect. A prediction measured
       against a different expression than the one shipped is the same defect
       class this property exists to catch, so the clause got its own
       injection rather than a rewritten expectation:
  I-86b the integer alone reverted, `4 workflows (BUILD, DEBUG, REVIEW, PLAN,
       QA, ORIENT, TRIAGE, CODEBASE-HEALTH)`
                                          -> PP-33(b) red on the cardinality
                                             half alone: "S3
                                             cc10x-guide/SKILL.md says 4
                                             workflows but lists 8", membership
                                             green. Without this run the
                                             count/len clause would be a green
                                             nobody had ever seen go red.
  I-87 README.md reverted to `<strong>4 workflows</strong>`
                                          -> PP-33(b) red: "S4 README.md says 4
                                             workflows, routing table has 8".
                                             The expected value is DERIVED from
                                             the SKILL.md section 1 table in the
                                             same run, so this red cannot be
                                             silenced by editing a literal in
                                             this file.
  I-54b the `**Workflow type.**` paragraph deleted whole from qa-workflow.md
                                          -> PP-33(b) red: "qa-workflow.md's
                                             stamping line is [] (expected
                                             exactly ['QA'])", and PP-18(a),
                                             (b), (c), (d) ALL GREEN. That
                                             second half is the measurement
                                             that justifies the paragraph's
                                             placement: PP-18 anchors on `^0a.`,
                                             `^0b.` and `^1. **Resolve QA
                                             scope` with exactly-one-match
                                             semantics, so adding the line to
                                             the opening step list -- the
                                             obvious place, and where both
                                             siblings carry it -- would have
                                             renumbered four green checks red.
                                             It is prose for that reason.
The last two are the ANTI-VACUITY controls, and there are two of them because
two shapes fail independently; a single control does not cover both. A third
proves the normaliser column:
  I-55(i)  S1's paren extractor broken, `[A-Z]` -> `[0-9]`
                                          -> PP-33(a) red on the S1
                                             PRECONDITION -- "the paren enum
                                             extractor matched NOTHING on its
                                             own anchor line" -- NOT a green.
                                             An extractor that stops matching
                                             yields [] and `"QA" in []` is
                                             False for the wrong reason, which
                                             is why (a) is asserted first and
                                             names the site.
  I-55(ii) S2's bracket extractor broken the same way
                                          -> PP-33(a) red on the S2
                                             precondition, S1/S3/S4 still
                                             printing their parsed members in
                                             the same detail string.
  I-55(iii) S2's basis changed from `_decommented()` to `_normative()` -- i.e.
       the property written with one normaliser for the whole corpus, which is
       how it would have shipped
                                          -> PP-33(a) red: "its anchor matched
                                             0 lines under `_normative()`".
       THIS IS THE MEASUREMENT BEHIND THE NORMALISER COLUMN.
       memory-file-contracts.md's enum is at 103, inside the fence pair
       (98, 117); `_normative()` deletes fenced blocks, so a corpus-wide
       normaliser makes PP-33 red on a CORRECTLY EDITED repo. The column is not
       symmetry -- it is the difference between a property that can be green and
       one that cannot.
  I-54c the stamping SHAPE drifted on a SIBLING: triage-workflow.md:8 rewritten
       to "The router stamps the artifact TRIAGE."
                                          -> PP-33(a) red: "the stamping regex
                                             matched [] in triage-workflow.md
                                             (expected exactly ['TRIAGE']) --
                                             the shape has drifted, so its
                                             absence from qa-workflow.md would
                                             prove nothing". The siblings are
                                             the live proof that the regex still
                                             reaches anything; without them the
                                             QA assertion could pass or fail for
                                             reasons having nothing to do with
                                             QA.
Parsed state at green: S1 cc10x-router/SKILL.md:276 and S2
memory-file-contracts.md:103 and S3 cc10x-guide/SKILL.md:38 each list the same
8 members; S4 README.md:18 count=8; SKILL.md section 1 routing table = 8
distinct workflows.

Negative controls for PP-34 (two runs, each restored and re-greened before the
next). Both inject into cc10x_qa_isolation_guard.py's phase-resolution
expression. The pair exists because ONE injection cannot prove this property:
the first shows PP-34 catches the crash at all, the second shows it
discriminates between the two candidate fixes.
  I-56 the whole four-line narrowed form reverted to the original one-liner
       `phase = (workflow.get("phase_cursor") or
                 workflow.get("status_history", [{}])[-1].get("phase") or "")`
                                          -> FIVE reds, one per crashing shape,
                                             with (d) GREEN and all four PP-6
                                             checks green:
                                             PP-34(a) "got rc=1 deny=False
                                               stderr='IndexError: list index
                                               out of range'"
                                             PP-34(b) "AttributeError: 'str'
                                               object has no attribute 'get'"
                                             PP-34(c) "TypeError: 'NoneType'
                                               object is not subscriptable"
                                             PP-34(e) "KeyError: -1"
                                             PP-34(f) "TypeError: 'int' object
                                               is not subscriptable"
                                             (d) STAYING GREEN IS THE POINT: it
                                             shows the five reds are about the
                                             crash and not about the rig.
  I-88 the SHIPPED form replaced by the `or []` form -- `isinstance(history,
       list)` swapped for `or []` and nothing else changed:
           history = workflow.get("status_history") or []
           prev_phase = history[-1].get("phase") if history and isinstance(
                        history[-1], dict) else ""
           phase = (workflow.get("phase_cursor") or prev_phase or "")
                                          -> EXACTLY TWO reds, (e) "KeyError:
                                             -1" and (f) "TypeError: 'int'
                                             object is not subscriptable", with
                                             (a)(b)(c)(d) green.
       THIS IS THE CONTROL THAT PICKS THE FIX. `or []` looks like it closes the
       hole and closes only four of six: `{"a": 1}` and `5` are both TRUTHY, so
       `or []` never fires and `history[-1]` still raises. Only
       `isinstance(history, list)` closes all six. Note the shape of the
       injection: the two-line abbreviation "revision 1 used `or []`" WITHOUT
       the `isinstance(history[-1], dict)` guard reds on five instead of two and
       is red whichever fix is shipped -- it cannot tell them apart, which is
       this control's entire job.

Negative controls for PP-35 and PP-36 (each restored and re-greened before the
next; the target file was copied to a backup and restored with `cp`, never
`git checkout --`).
  I-57 the path-extracting Bash test at cc10x_qa_isolation_guard.py reverted to
       the substring escape it replaced:
           if tool_name == "Bash" and any(
               a.strip("/") in (tool_input.get("command") or "") for a in allowlist
           ):
                                          -> EXACTLY TWO reds, with (c)(e)
                                             green:
                                             PP-35(a) "got rc=0 deny=False"
                                             PP-35(b) "got rc=0 deny=False"
                                             (c) and (e) STAYING GREEN is what
                                             makes this a property about path
                                             semantics and not about denial.
  I-57b the Bash allow escape DELETED outright (the "deny everything" guard)
                                          -> PP-35(c) "got rc=0 deny=True".
       This is why (c) is in the table. Without it, I-57's fix could be
       "remove the escape", which reds nothing in the DENY rows and breaks
       every legitimate `.cc10x/` write the QA route depends on.
  I-57c the WRITE allow escape deleted (`if target and tool_name in
       WRITE_TOOLS and _matches(target, allowlist)`)
                                          -> PP-35(e) "got rc=0 deny=True".
       (e)'s counterpart to I-57b, on the branch this phase did not rewrite.
  I-57d the plan-phase branch disabled (`if False and plan_readonly and ...`)
                                          -> FOUR PP-35 reds, (a)(b)(d)(f),
                                             with (c)(e) green. This is the
                                             control for row (f), which no
                                             other injection reaches: (f)
                                             differs from (a) only by the
                                             appended `# .cc10x`, so (f) going
                                             red here is what proves (a)'s
                                             green is about the comment and
                                             not about the rig.
  I-58 `/tmp/cc10x-` restored to the line-228 default, path-aware Bash test
       LEFT IN PLACE
                                          -> ONE red, PP-36. **The plan
                                             predicted two (PP-35(d) as well)
                                             and the plan is wrong.** Measured:
                                             `_matches("/tmp/cc10x-pp35",
                                             ["/tmp/cc10x-"])` is None. The
                                             entry has no wildcard, so it takes
                                             the bare-path branch, which
                                             resolves it to
                                             `/private/tmp/cc10x-` and then
                                             requires either equality or a
                                             `/`-separated descendant. A
                                             PREFIX like `cc10x-pp35` is
                                             neither. So once the Bash branch
                                             stops being a substring test, the
                                             `/tmp/cc10x-` entry is genuinely
                                             dead -- it was live ONLY through
                                             the escape this phase removed.
                                             PP-35(d) is therefore held by the
                                             CONJUNCTION, not by either half.
  I-58b BOTH halves reverted (the pre-phase state at c82d562): the substring
       escape AND `/tmp/cc10x-` in the default
                                          -> FOUR reds, PP-35(a)(b)(d) and
                                             PP-36. (d) reds here and only
                                             here, because the substring
                                             `tmp/cc10x-` does occur in
                                             `mkdir -p /tmp/cc10x-pp35`. This
                                             is the control I-58 was meant to
                                             be, and it is the one that shows
                                             the ALLOW measured in R3 was real.
  I-59(i) PP-36's site-1 regex broken (`mutation_allowlist` ->
       `mutation_ALLOWLIST`) so it parses nothing
                                          -> PP-36 red on the PRECONDITION,
                                             not a vacuous green: "1 code ...
                                             pattern matched 0 times, expected
                                             exactly 1; PRECONDITION failed:
                                             ... parsed an empty list -- an
                                             empty parse makes the
                                             set-equality vacuous".
  I-59(ii) PP-36's site 5 switched from `_decommented()` to `_normative()`
                                          -> PP-36 red on the same
                                             precondition, naming site 5. This
                                             is the half worth running: site 5
                                             lives inside a fenced JSON block,
                                             `_normative()` strips fences, and
                                             without the precondition this is a
                                             FOUR-site property that prints
                                             "5" and passes.
Parsed state at green: all five declarations = ['.cc10x/'] -- code line 228,
the guard's own module docstring, workflow-artifact.skeleton.json
qa.isolation.mutation_allowlist, qa-workflow.md prose, qa-workflow.md fence.

Negative controls for PP-37 (each restored and re-greened before the next; the
guard was copied to a backup and restored with `cp`, never `git checkout --`).
The last two are a PAIR and they red OPPOSITE halves of the table; recording
them side by side is what makes PP-37 two-sided rather than a catalogue of
denials.
  I-60 `"config"` restored to the `git` set
                                          -> ONE red, PP-37(a):
                                             "`git config user.email x@y.z` ->
                                             ALLOW, want DENY".
  I-61 `"fmt"` restored to `terraform`    -> ONE red, PP-37(a), naming BOTH
                                             terraform rows: "`terraform fmt
                                             -write=true` -> ALLOW, want DENY;
                                             `terraform fmt` -> ALLOW, want
                                             DENY". The flagless row is the
                                             point: `terraform fmt` rewrites
                                             files with no flag at all, so no
                                             amount of flag-awareness in the
                                             parser would have saved it.
  I-62 SUBCOMMAND_TOOLS = {k: set() for k in SUBCOMMAND_TOOLS}
       (the VALUES emptied)               -> the OVER-denial control. All 7
                                             ALLOW rows red, all 13 DENY rows
                                             green: "`git log --oneline -1` ->
                                             DENY, want ALLOW; `git status
                                             --porcelain` -> DENY, want ALLOW;
                                             `docker info` ...". This is the
                                             control that prices ADR-1's blast
                                             radius: an over-fix that denied
                                             every capability probe step 0a
                                             runs would pass a deny-only
                                             property.
                                             It also settles, by execution, the
                                             claim that `git log --oneline -1`
                                             and `git status --porcelain` never
                                             reach the membership test because
                                             line 201 consumes every argument.
                                             They do reach it: both can only
                                             flip to DENY through it.
  I-89 SUBCOMMAND_TOOLS = {} (the whole DICT emptied)
                                          -> the UNDER-denial control, and the
                                             exact opposite red: all 13 DENY
                                             rows red, all 7 ALLOW rows green.
                                             `argv0 in SUBCOMMAND_TOOLS` is
                                             False, control falls through to
                                             MUTATING_COMMANDS where none of
                                             git/docker/kubectl/terraform
                                             appears, `_bash_mutates` returns
                                             None, and everything is allowed.
                                             "Someone deletes the dict" and
                                             "someone empties a tool's set" are
                                             distinct regressions with opposite
                                             signatures; one injection cannot
                                             stand for both.
Measured state at green: the 13 mutating invocations DENY and the 7 read-only
probes ALLOW at phase_cursor=qa-plan. Priced and accepted (ADR-1): the bare
read forms `git config --get user.email`, `npm config get registry` and
`kubectl config view` are DENIED too, because every argument after the
subcommand is a flag and the parser is flag-blind by design. Step 0a's
documented probes were re-measured against the fixed guard and all ALLOW --
`docker info`, `podman info`, the file-presence checks, the dependency-manifest
reads and the `which`/`command -v` lookups.

Negative controls for PP-38 (each restored with `cp` from a backup and
re-greened before the next; never `git checkout --`). Four injections because
the three edits are independently necessary and one of them is invisible to the
other two's checks.
  I-63 `for key in ("file_path", "path", "pattern"):`
       (the denylist tuple reverted)      -> ONE red, PP-38(a): "NotebookRead
                                             '/tmp/pp38-secret.ipynb' -> ALLOW,
                                             want DENY". (b) stays green, which
                                             localises the red to the key
                                             lookup and not to `_matches`.
  I-64 `target = tool_input.get("file_path") or ""`
       (the write-branch fallback reverted)
                                          -> ONE red, PP-38(c): "NotebookEdit
                                             '.cc10x/qa/pp38.ipynb' -> DENY,
                                             want ALLOW". This is the FALSE-DENY
                                             half, and it was live at HEAD:
                                             NotebookEdit was already in the
                                             matcher, so a notebook write into
                                             the workflow's own directory was
                                             being blocked in production.
                                             (d) and (e) stay green.
  I-65 `NotebookRead` removed from the hooks.json matcher
                                          -> ONE red, PP-38(f). Note what does
                                             NOT go red: PP-38(a) stays GREEN
                                             throughout, because (a)-(e) invoke
                                             the guard as a subprocess over
                                             stdin and never consult the
                                             PreToolUse matcher. A guard that
                                             decides correctly and is never
                                             invoked is indistinguishable from
                                             a correct guard at the subprocess
                                             seam. That is the whole reason (f)
                                             exists as a separate check rather
                                             than as an assertion inside (a).
  I-66 `READ_TOOLS = {..., "Sparkle"}` (a tool added to the guard but not to
       the matcher)                       -> ONE red, PP-38(f): "matcher
                                             'Read|Grep|Glob|NotebookRead|Edit|
                                             Write|NotebookEdit|Bash' never
                                             fires for ['Sparkle']". This is the
                                             frozen-copy control: (f) imports
                                             READ_TOOLS/WRITE_TOOLS from the
                                             live guard module via load_guard()
                                             rather than transcribing them, so
                                             the two sets cannot drift apart
                                             silently. A hard-coded copy of the
                                             sets would stay green here forever.
Measured state at green: NotebookRead of a denylisted path DENIES, NotebookEdit
into the allowlist ALLOWS, NotebookEdit outside it still DENIES, and the matcher
is exactly READ_TOOLS | WRITE_TOOLS | {"Bash"} (8 tools).

Negative controls for PP-39 (each restored with `cp` from a backup and
re-greened before the next; never `git checkout --`). TWO of the three planned
injections did not red as planned, and both are recorded here with the
measurement rather than smoothed away.
  I-67 `load_mode,` restored to the guard's
       import AND called once
       (`_ = load_mode()`)                -> ONE red, PP-39(b): "the mode
                                             paragraph calls
                                             ['cc10x_qa_isolation_guard.py']
                                             unconditional, but it calls
                                             load_mode -- the claim is false in
                                             the other direction".
                                             FIRST ATTEMPT WAS GREEN. PP-39(b)
                                             was written as the plan words it
                                             ("names every member of
                                             unconditional"), i.e. one-sided
                                             containment. I-67 SHRINKS
                                             `unconditional` from 2 to 1, and
                                             containment cannot see a paragraph
                                             that names one hook too many. Per
                                             the injection protocol -- an
                                             injection that does not red means
                                             the property is wrong, not the
                                             injection -- (b) was strengthened
                                             to SET EQUALITY between the `.py`
                                             basenames inside W8 and the
                                             computed set. Both directions are
                                             now held.
  I-68 the `PreToolUse` QA-isolation bullet deleted from the enumeration
                                          -> NO RED. Recorded as measured, not
                                             repaired. The plan predicted
                                             "[FAIL] PP-39(a)", but PP-39(a) is
                                             specified whole-file and edit 2
                                             names `cc10x_qa_isolation_guard.py`
                                             a SECOND time inside the mode
                                             paragraph -- so deleting the
                                             enumeration bullet leaves the
                                             basename present. The prediction
                                             was computed against the revision
                                             where edit 2 named the two hooks in
                                             PROSE; correcting that to basenames
                                             (finding A5) is what made this
                                             injection unfireable. CONSEQUENCE,
                                             disclosed: the QA guard's own
                                             enumeration bullet -- and only that
                                             bullet -- is held by no property.
                                             Each of the other four basenames
                                             occurs exactly once, so their
                                             bullets ARE held (see I-68b).
  I-68b `TaskCompleted` bullet's `(`cc10x_task_completed_guard.py`)` removed
                                          -> ONE red, PP-39(a):
                                             "workflow-artifact-and-hook-policy
                                             .md never names
                                             ['cc10x_task_completed_guard.py']".
                                             The substitute control, chosen
                                             because that basename occurs once.
  I-69 the mode paragraph's lead-in reworded to `- Hook mode defaults to
       audit-only ...` (vacuity control for the window)
                                          -> ONE red, PP-39(b) PRECONDITION:
                                             "W8 has 0 opening and 1 closing
                                             anchors ... any result over this
                                             window would be vacuous". Without
                                             the exactly-one-match assertion the
                                             window would be 0B and the set
                                             equality would compare two empty
                                             sets.
Measured state at green: 5 blocking hooks / 3 mode-aware / 2 unconditional
({cc10x_git_guard.py, cc10x_qa_isolation_guard.py}); W8 = 1249B normative
(962B before this commit's edit 2), carrying exactly those two `.py` tokens.

Negative controls for PP-40 (each restored with `cp` from a backup and
re-greened before the next; never `git checkout --`). Four of the six defend a
BRANCH of the verdict rule rather than the defect, because the risk here is not
that the property misses B2 -- it is that a stricter rule reds correct prose.
I-90 is the measurement of exactly that: the rule this property replaced.
  I-70 `§7 known gaps` reverted to `§6` on qa-workflow.md's `Then fill them in
       place.` line (the live defect, B2)
                                          -> ONE red, PP-40: "qa-workflow.md:143
                                             §6 'known gaps' names '## 7. Known
                                             gaps', not '## 6. Test data'".
  I-71 prefix inheritance deleted -- `_pp40_prefix` restricted to the 15
       characters immediately before the citation, so only DIRECTLY prefixed
       `§N` resolve       -> TWO reds in one line, both expected. Resolved drops
                             10 -> 6 (below the floor of 8) and the
                             undescriptive class empties, because both its
                             members are inherited: "PRECONDITION: only 6
                             citations resolved, floor is 8 ...; the
                             undescriptive class is not PP40_UNDESCRIPTIVE:
                             joined [], left [('qa-workflow.md', 119, 2),
                             ('qa-workflow.md', 119, 4)]". The four citations
                             lost are :119 §4, :119 §2, :143 §7 and :143 §10 --
                             B2's OWN citation is inherited, so without
                             inheritance this property is green on the live
                             defect.
  I-72 token overlap replaced by case-folded equality of the whole trailing
       phrase against the title (the over-strict control)
                                          -> ZERO mismatches and ONE
                                             set-equality red. The undescriptive
                                             class grows 2 -> 6: joined
                                             [('qa-harness-builder.md', 137, 11),
                                             ('qa-workflow.md', 119, 7),
                                             ('qa-workflow.md', 143, 2),
                                             ('qa-workflow.md', 143, 9)], every
                                             one a CORRECT citation. Recorded in
                                             full because the prediction this
                                             control shipped with was "six
                                             mismatches": under a four-branch
                                             rule an over-strict branch 2 falls
                                             through to branch 3, finds no OTHER
                                             title it equals either, and lands in
                                             branch 4. An over-strict matcher
                                             does not produce mismatches here --
                                             it produces silence, and the set
                                             equality is the only thing that
                                             hears it.
  I-90 branches 1, 3 and 4 collapsed into "zero token overlap = MISMATCH" -- the
       rule this property replaced     -> THREE mismatches, every one a correct
                                          citation: `qa-env-plan.template.md:71
                                          §3 ""`, `qa-workflow.md:119 §4 "wave
                                          count and in the"`, `:119 §2 "id
                                          rollups"`. Plus the set-equality red
                                          (the class empties) and the floor
                                          (7 < 8, because the three left the
                                          resolved side). This is the injection
                                          that reproduces what a one-comparison
                                          rule would ship: it asserts that every
                                          citation's trailing words paraphrase
                                          its heading, which is not how prose is
                                          written.
  I-92 `re.split(r"[^0-9A-Za-z-]+")` -- hyphens no longer split
                                          -> ONE set-equality red, naming one
                                             citation: joined
                                             [('qa-workflow.md', 119, 7)].
                                             `known-gaps table` stops overlapping
                                             `## 7. Known gaps`. No mismatch at
                                             all -- as a printed-only list this
                                             regression would have been silent.
  I-93 the trailing-`s` stem dropped -> ONE set-equality red, naming one
                                        citation: joined
                                        [('qa-harness-builder.md', 137, 11)].
                                        `blocker` stops matching `Blockers`.
                                        Silent for the same reason as I-92.
Measured state at green: 10 prefixed citations over the three files -- 7 matched
/ 1 fallback / 2 undescriptive -- plus 43 no-prefix, 53 `§N` seen in total. PP-9
is untouched and prints `0 bad, 49 unresolved-and-skipped` before and after the
`§6` -> `§7` edit: it is a SIBLING of PP-40, not its predecessor, and resolves
only `env plan`-prefixed citations, so the digit it never resolved is a digit it
still never resolves.

Negative controls for PP-41 (each restored with `cp` from a backup and
re-greened before the next; never `git checkout --`). All five windows are
sliced from `_decommented()`, never `_normative()`: `_normative()` deletes
fenced blocks, and three of the four anchors sit inside ```yaml fences.
Measured at this commit, anchor match counts under the two normalisers --
  W4 `^OBSERVABILITY_POINTS:`      decommented 1 / normative 0
  W3 `^TEARDOWN_STATUS:`           decommented 1 / normative 0
  W2 `^# --- preflight mode only`  decommented 1 / normative 0
  W2 `^# --- end preflight-only`   decommented 1 / normative 0
  W9 `^**CONTRACT RULES:**` (researcher)  decommented 1 / NORMATIVE 1
  W7 `^**CONTRACT RULES:**` (executor)    decommented 1 / NORMATIVE 1
-- so a PP-41 written over `_normative()` would go red on its own
exactly-one-anchor precondition for (a)'s W4 half, (b)'s W3 half and all of
(c), which is PP-20's trap (lines 1571-1572, "0/0 through _normative()") in
three new places. W9 and W7 are the two that survive `_normative()`, because
both CONTRACT RULES regions sit AFTER their file's closing fence. They read
`_decommented()` anyway, so each sub-check has one basis rather than two.
  I-73a line 152 reverted to `verbatim: [true|false]`, the MUST rule left fixed
                                          -> ONE red, PP-41(a), on the W4 half
                                             ONLY (W4 184B, W9 1459B): "W4
                                             declares no `provenance:` field
                                             ...; W4's provenance enum omits
                                             ['V', 'Vp', 'I'] ...; W4 still
                                             carries a `verbatim:` field".
  I-73b the MUST rule at 172 reverted ALONE, line 152 left fixed
                                          -> ONE red, PP-41(a), on the W9 half
                                             ONLY (W4 275B, W9 1104B): "the
                                             CONTRACT RULES region (W9) never
                                             names `provenance` ...; the
                                             CONTRACT RULES region (W9) still
                                             names `verbatim` as a field -- the
                                             MUST rule points at a field that no
                                             longer exists". This is the control
                                             that earns W9: line 172 is OUTSIDE
                                             the yaml fence (120-166) and
                                             therefore outside W4, so without a
                                             second window a builder edits 152,
                                             leaves 172, and this property is
                                             green on a contract whose MUST rule
                                             names a deleted field. The two
                                             halves red independently, which is
                                             what proves there are two of them.
  I-74 the report template's teardown row reverted to `clean | leaked` (the
       cell's literal text, escaped `\\|` in the markdown table)
                                          -> ONE red, PP-41(b): "executor
                                             ['clean', 'leaked', 'not_run'] !=
                                             template ['clean', 'leaked'] -- the
                                             report template offers no cell for
                                             a status the contract requires the
                                             executor to emit". SET equality,
                                             not containment: containment in
                                             either direction is green while one
                                             side quietly grows a value.
  I-75 `surface_tier:` renamed back to `tier:`
                                          -> ONE red, PP-41(c): "2 bare `tier:`
                                             fields in the preflight block, want
                                             1 ...; 0 `surface_tier:` fields
                                             ..., want 1" (W2 3960B). The count
                                             MUST use `(?<![A-Za-z0-9_])tier:`.
                                             Measured at green on the fixed
                                             file: the lookbehind counts 1, the
                                             bare substring `tier:` still counts
                                             2, because `surface_tier:` contains
                                             `tier:` -- a bare-substring check
                                             is red before AND after the fix,
                                             which is a control that cannot tell
                                             the defect from its repair.
  I-76 the `# --- end preflight-only` marker deleted (window control)
                                          -> ONE red, PP-41(c) PRECONDITION: "W2
                                             (preflight-only block) end anchor
                                             ... never matches after the start
                                             anchor -- the window runs to EOF,
                                             which is a runaway window, not a
                                             measurement". Without it the window
                                             swallows MEMORY_NOTES and every
                                             count below is measured over prose
                                             the block does not own.
Measured state at green, all five windows over `_decommented()` and all sizes
`len(w.encode("utf-8"))`: W4 = 275B (219B before this commit's edit), W9 =
1459B (1104B before), W3 = 107B (unchanged -- the enum already had all three
values), W7 = 6955B (6530B before), W2 = 4024B (3424B before). The four
pre-edit numbers reproduce the plan's R11 table exactly at e45b600.

Negative controls for PP-42 (each restored with `cp` from a backup and
re-greened before the next; never `git checkout --`). Two of the three
sub-checks read a DIFFERENT basis from their neighbours, and both departures
are measured rather than assumed:
  (a) W6 `^### The failure vocabulary` -> next `^### ` over `_normative()`.
      Anchor match counts at this commit: raw 1 / decommented 1 / normative 1,
      and the window is 1952 B under all three -- qa-workflow.md's fences do
      not span it. It was 1794 B before this commit's edit 3, which is the
      number the plan's R11 table records at c3ea86f.
      The W5 anchor `^### QA-specific rules` also matches once under all three
      bases (2226 B at HEAD) and is the WRONG window: the authority sentence
      is not in it. PP-42(a) anchored at W5 could never see the claim it
      asserts on.
  (b) RAW `QA_WORKFLOW.read_text()`, the same basis PP-19(b) uses. Measured:
      the `cp` line matches once in raw and once in `_decommented()`, and
      ZERO times in `_normative()` -- it sits inside a ```text fence. A
      PP-42(b) over `_normative()` would be red on a correct file.
  (c) `_decommented()` over templates/qa-*.template.md. The template carries
      no fences at all (measured: 0), so decommented and normative differ
      only in the rebuttal HTML comment -- which is exactly why the rebuttal
      is NOT where the cross-route sentence lives.
  I-77 `one authority: qa-harness-builder.md` restored at qa-executor.md, with
       the pointer left in place
                                          -> ONE red, PP-42(a): "2 file(s)
                                             claim authority over FAILURE_CLASS
                                             ['qa-executor.md',
                                             'qa-workflow.md'], want exactly 1
                                             (qa-workflow.md)". The count is
                                             asserted as EXACTLY 1 for this
                                             reason: the injected file still
                                             carries a correct pointer, so a
                                             `>= 1` or containment test is
                                             GREEN on the two-owner state that
                                             is the whole defect.
  I-77b the harness builder's pointer paragraph deleted (the OTHER half of (a),
       which I-77 cannot reach)
                                          -> ONE red, PP-42(a):
                                             "qa-harness-builder.md carries no
                                             pointer naming qa-workflow.md -- a
                                             non-owner that names no owner
                                             leaves the reader to guess".
                                             Recorded because the pointer half
                                             is satisfied by the whole file and
                                             would otherwise never be observed
                                             failing.
  I-78 the router's `cp` of qa-report.template.md into report.md deleted from
       qa-workflow.md (raw line 460 at this commit)
                                          -> TWO reds, both expected: PP-42(b)
                                             "0 router `cp` ..., want exactly
                                             1" and PP-19(b) "qa-workflow.md
                                             has no Bash cp of the template
                                             into report.md". PP-19(b) going
                                             red too is the point: it asserts
                                             only that the `cp` EXISTS, so with
                                             deliverable 9 dropped it is the
                                             single remaining writer and PP-42(b)
                                             is what notices there is now none.
  I-78b a report-producing row re-added to the deliverables table under a
       DIFFERENT name (`| 9 | Report skeleton | writes the report shape ...`)
                                          -> ONE red, PP-42(b), on BOTH
                                             clauses: "9 deliverable rows, want
                                             8" and "1 deliverable row(s) still
                                             claim the report shape". The row
                                             regex is keyed on the SHAPE
                                             (`report shape|emitter|skeleton`),
                                             not the literal "Report emitter":
                                             a test for the old row's title is
                                             green against the same defect
                                             spelled differently.
  I-78c the router-seeded disclaimer reworded so its anchor phrase is gone
                                          -> ONE red, PP-42(b):
                                             "qa-harness-builder.md does not
                                             state that the report shape is
                                             router-seeded". The positive half
                                             exists because a negative alone
                                             rewards silent deletion: with the
                                             row gone and no sentence saying
                                             why, the next editor reads an
                                             omission and puts the row back.
  I-79 the ORIGINAL blockquote line restored verbatim: `> The last two fields
       exist because cc10x's `plan_trust_gate` reads them.`
                                          -> ONE red, PP-42(c), on
                                             sub-assertion (iii) and BOTH its
                                             halves: "its line carries no other
                                             route's name" and "its line claims
                                             it applies to THIS artifact via
                                             ['reads them']". NOT a membership
                                             red -- the token is still excluded
                                             by name, and that is the point.
                                             C4's defect was never the presence
                                             of the token; it was the sentence
                                             shape, and the sentence shape is
                                             what this injects.
  I-80 vacuity control, both halves:
       (first)  the `*_gate` regex broken to `..._gateXX`
                                          -> ONE red, PP-42(c) PRECONDITION:
                                             "extracted 0 `*_gate` tokens ...
                                             (expected >= 2) -- the gate-token
                                             regex has stopped matching, so
                                             every membership result below is
                                             vacuous". Without the floor,
                                             `set() <= anything` is True and
                                             the property is green on a dead
                                             regex -- vacuity shape (a).
       (second) `"never_gate"` added to PP42C_CROSS_ROUTE_GATES
                                          -> ONE red, PP-42(c): "exclusion
                                             names ['never_gate'], absent from
                                             the extracted set
                                             ['phase_exit_gate',
                                             'plan_trust_gate'] -- an exclusion
                                             list has outlived its subject".
                                             The assertion is `<=`, NOT `<`:
                                             after this commit the two sets are
                                             EQUAL, and `set(a) < set(a)` is
                                             False in Python, so a
                                             proper-subset assertion is red on
                                             a correct tree and this control
                                             would have proved nothing.
  I-81 `qa_wave_gate` -- a gate name no route defines -- cited in
       qa-test-plan.template.md
                                          -> ONE red, PP-42(c) sub-assertion
                                             (iv): "['qa_wave_gate'] named in
                                             templates/qa-*.template.md but
                                             absent from qa-workflow.md".
                                             Recorded because the plan
                                             disclosed (iv) as UNPROVABLE --
                                             "there is no live example to prove
                                             that branch on". There is no live
                                             example; there is an injection,
                                             and it fires. (iv) is reachable.
Measured state at green: 3 files in the FAILURE_CLASS ownership triangle, 1
claim (qa-workflow.md, inside W6) and 2 pointers; 1 router `cp` and 8
deliverable rows; extracted gate tokens = {phase_exit_gate, plan_trust_gate},
BOTH excluded by name with their reasons carried in PP-42(c)'s own check line
on every run -- in the detail string rather than a side channel, so a reader of
the pass line cannot miss what was excluded or why. 0 live members.
The membership half of PP-42(c) is therefore INERT BY CONSTRUCTION at this
commit -- stated plainly here and in the check's own comment, because `<=`
against a full exclusion set looks stronger than it is. Its enforcement is (i)
the floor, (ii) the no-rot subset, (iii) the per-line route-attribution test,
and (iv) proven reachable by I-81.

Negative controls for PP-43 and for PP-38(f)'s second clause (each restored with
`cp` from a backup and re-greened before the next; never `git checkout --`).

ID NOTE, recorded rather than smoothed. Phase 10 was specified to produce
I-81..I-84 and I-91. By the time it ran, **I-81 was already taken** (Phase 9's
PP-42(c)(iv) control) and **I-83, I-90, I-92, I-93** were taken (Phase 7's PP-40
controls). The plan allocated Phase 10's ids against a draft that predated those
two phases' own allocations. The two colliding ids are renumbered here --
plan I-81 -> I-94, plan I-83 -> I-95 -- and I-82, I-84, I-91 keep their planned
numbers because they were still free. Nothing is dropped and nothing is reused.

The first four were observed against the LIVE DEFECT rather than a simulation of
it: PP-43 was written and run BEFORE any of Phase 10's six repo edits, so the
state that produced each red is the state the branch was actually in at b966c52,
byte for byte. That is strictly stronger than an injection, which can only
approximate the defect.
  I-94 (plan I-81) the C1 row as it stood: `| `report.md` | skeleton in
       `agents/qa-executor.md` |`
                                          -> ONE red, PP-43(a): "`report.md` ->
                                             'skeleton in
                                             `agents/qa-executor.md`' is not a
                                             templates/ path". The row count
                                             stays 6 and the window stays 805B,
                                             so the precondition is not what
                                             fires -- the membership half is.
  I-82 both path tokens on qa-harness-builder.md's manifest line reverted to
       their bare forms (the state at b966c52)
                                          -> TWO reds, PP-43(b), BOTH from the
                                             prefix-consistency clause:
                                             "qa-harness-builder.md:63 names
                                             `tools/live_harness_runner.py` bare
                                             beside
                                             `${CLAUDE_PLUGIN_ROOT}/templates/
                                             live-harness.template.json`" and
                                             the sibling line for
                                             `tests/live/manifests/
                                             cc10x-bootstrap.json`.
                                             NEITHER is a resolution failure,
                                             and that is the point: both paths
                                             EXIST and resolve under PP-29's
                                             bases. A red saying the path "does
                                             not resolve" would mean the wrong
                                             clause was built and the control
                                             had failed. See ADR-5. The site is
                                             :63, not the plan's :58 -- Phase 9
                                             dropped a deliverable row above it.
  I-95 (plan I-83) the C7 DRAFT header sentence as it stood
                                          -> TWO reds, PP-43(c): "SKILL.md claims
                                             `live-verification-strategy.md` does
                                             not exist; resolves at
                                             skills/planning/references/
                                             live-verification-strategy.md", and
                                             the sibling for
                                             `live-production-testing.md` at
                                             skills/verification/references/.
                                             Exactly two. ZERO reds would mean
                                             plugin-root resolution was built
                                             instead of basename resolution --
                                             both claims are BARE BASENAMES and
                                             resolve nowhere from the plugin
                                             root. A THIRD red naming
                                             `integration-and-live-proof.md`
                                             would mean the candidates were
                                             scoped to the whole sentence
                                             instead of to the object of the
                                             do-not-exist clause, flagging a
                                             CORRECT citation. Both are failed
                                             controls; neither occurred.
  I-91 `and proof commands` present at integration-and-live-proof.md:60 (the
       state at b966c52)
                                          -> ONE red, PP-43(d): "'proof command'
                                             promised by
                                             integration-and-live-proof.md:60,
                                             absent from qa-strategy/SKILL.md".
                                             C5 is PARTIAL: only this half is a
                                             defect. The `harness-manifest.md`
                                             half sits under an explicit
                                             **PLACEHOLDER** banner with three
                                             siblings in the same state, and a
                                             declared placeholder is not a broken
                                             link -- it is PP-43(b)'s NAMED,
                                             banner-anchored, printed exclusion.
  I-84 vacuity control. PP43A_ROW keyed on a leading `` | ` `` -- the regex the
       prose invites
                                          -> ONE red, PP-43(a), on the ROW-COUNT
                                             PRECONDITION and not on membership:
                                             "5 data rows in the 890B (raw)
                                             artifact-template window of SKILL.md
                                             (expected >= 6)". The `harness
                                             manifest` row's first cell is
                                             UNBACKTICKED where the other five
                                             are backticked, so the backtick-keyed
                                             regex finds 5. This is why the floor
                                             is 6 and why the row regex is keyed
                                             on the separator's absence instead.
                                             A floor of 7 -- which two earlier
                                             drafts of the plan carried -- would
                                             have been red on day one for a reason
                                             having nothing to do with C1.
  I-96 (new) `NotebookRead` deleted from the PROSE copy of the matcher at
       qa-workflow.md's Rule 1 paragraph ONLY, hooks.json left intact
                                          -> ONE red, PP-38(f)'s second clause:
                                             "qa-workflow.md restates the matcher
                                             as 'Read|Grep|Glob|Edit|Write|
                                             NotebookEdit|Bash', hooks.json
                                             declares 'Read|Grep|Glob|
                                             NotebookRead|Edit|Write|
                                             NotebookEdit|Bash' -- a second
                                             declaration of one value, drifted".
                                             This is the byte-duplication trap in
                                             the direction it has ALREADY drifted
                                             once on this branch: Phase 5 found
                                             the prose copy stale and synced it by
                                             hand, and nothing then held it.
Measured state at green: 6 data rows in an 890B artifact-template window, all
six naming a `templates/` path; 19 path-shaped tokens across four QA sources, 5
templated/glob-bearing, 4 PLACEHOLDER-excluded by NAME and printed with the
banner's site (SKILL.md:267) on every run, 10 candidates all resolving, 9 lines
carrying `${CLAUDE_PLUGIN_ROOT}/` and no bare sibling on any of them; PP-43(c)'s
pinned fixture yielding exactly its two expected candidates against a real corpus
whose do-not-exist hit count is now 0 and will stay 0 -- which is precisely why
the fixture exists, since a permanently empty candidate set makes a corpus-only
assertion prove nothing; one promised capability (`harness manifest`), present in
the file the promise points at.

TWO ITEMS THE PLAN LEFT HELD BY NO PROPERTY; Phase 10 decided both.
  PINNED -- qa-workflow.md's prose copy of the hooks.json matcher. It is a
    verbatim second declaration of a value with one owner, it has already gone
    stale once on this branch, and PP-38(f) ALREADY loads the authoritative
    string, so the pin costs one assertion and no new check. The prose copy is
    kept rather than deleted: the paragraph states which tools the isolation rule
    covers at the point where the rule is stated. Control I-96.
  NOT PINNED -- the QA guard's own enumeration bullet in the hook policy ("blocks
    three things: reads of denylisted paths, file writes during a planning phase,
    and Bash mutations during a planning phase"). Unlike the matcher there is no
    independent owner to compare it against: the guard's three blocks are three
    code paths, not a named set, so any property would have to hard-code the three
    nouns in the test -- manufacturing a THIRD declaration of the very thing being
    checked, and comparing a literal to a literal. That is the tautological-check
    shape, and it is weaker than the absence it replaces. PP-39(a) and PP-39(b)
    already pin that paragraph's load-bearing claims (which scripts block, and
    which of them are unconditional); the residual "three things" is a summary
    whose only machine referent would be a count the test itself invented.
"""

from __future__ import annotations

import ast
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
HOOKS_JSON = PLUGIN / "hooks" / "hooks.json"
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
# The fan-out lanes are the only in-workflow nodes with no predecessor, and
# that is a property of the route, not an oversight: consolidation after the
# lanes is deliberately INLINE (qa-workflow.md argues it), so there is no task
# between the researchers and qa-plan. `re_qa_execute_task_id` is a SECOND kind
# of entry point: the closing-loop regression run lives in its own NEW QA
# workflow (the original one is memory-finalized and closed), so within that
# graph it has no predecessor by construction — the DEBUG task that precedes it
# chronologically belongs to a different workflow and a different task graph.
# Adding a name here asserts a new ENTRY POINT to the QA graph -- it is not a
# way to quiet a node that lost its edge.
QA_DAG_ROOTS = frozenset({"researcher_task_id", "re_qa_execute_task_id"})
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
# THREE anchored SKILL.md enum lines, not one. The event-log template was the
# only one this property guarded when it was written (M10b); re-measurement
# found two siblings still omitting `qa`, both one-token additions:
#   - the parent-workflow `TaskCreate` template, which stamps a QA parent task
#     with a `phase:` token outside the enum it is copied from;
#   - the `__PHASE__` substitution list, which ALREADY carries the advisory
#     routes (orient, triage, codebase-health), so QA's absence there is an
#     omission rather than a scoping decision.
# Extending the existing check rather than adding a sibling half, deliberately:
# the three lines are one fact stated three times, they fail for the same reason
# and they are fixed by the same edit. A property that blesses one of three
# sites while the other two drift is the defect this phase is closing, so it
# would be a strange shape to reproduce in the property that closes it. The
# check-id count is therefore unchanged by this extension; the detail string
# names the failing LINE, which is what makes it actionable at three sites.
PP21_SKILL_ENUM_LINES = (
    ("event-log phase template", "workflow_started"),
    ("parent-workflow TaskCreate template", "kind:workflow"),
    ("`__PHASE__` substitution list", "- `__PHASE__` →"),
)
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


# PP-25. The two re-dispatch loops in the QA law: bound them, and COUNT them
# where a hook can see the count.
#
# (a) M2. The preflight re-dispatch ran uncapped while its own sibling three
# hundred lines down capped at 2 with a checkpoint. An uncapped retry is worse
# HERE than anywhere else in the route because preflight's retry arrives FROM
# THE USER, in place -- so an uncapped loop is a loop the user is inside, and
# each turn re-asks a question they have already answered.
#
# WINDOW-ANCHORED PER LOOP, and that is the load-bearing decision. The word
# "cap" appears in BOTH blocks, so a file-wide search lets one block satisfy
# the other's half of the assertion -- PP-18's recorded I-2 failure, in a third
# shape. Control (iii) is the run that proves the windowing: the cap deleted
# from the preflight window ONLY, with the re-qa-build window left green.
#
# ANCHORED ON BOLD LEAD-INS, not on headings, because NEITHER loop sits under
# one. The preflight loop lives between `**The batched ask...` and `**Four rules
# specific to this phase:**`, both inside `#### Environment preflight`; the
# re-qa-build loop lives between `**Extra rounds when the mutation floor is
# unmet...` and `**Hard boundary...`, both inside `#### Harness build`. Each of
# the four is a UNIQUE line-anchored match in the normalised text, and exactly-
# one-match is asserted as a PRECONDITION -- an anchor that stops matching must
# fail loudly, never yield an empty window that satisfies everything.
#
# Read over _normative() -- the same normalised copy PP-18 uses -- for two
# reasons. A law inside <!-- --> or re-parked into a ```fence``` is not law
# (PP-18's I-1/I-4). And the re-qa-build window CONTAINS a ```text fence, so its
# normalised size is exactly the quantity a later fence deletion elsewhere in
# this file could disturb: printing the sizes is what makes that a measurement
# instead of an argument.
#
# The cap is matched as a NUMBER, not as the word "cap": a block that says "this
# loop is capped" without saying at what states no bound. Exactly one numeric
# cap per window, so a second one cannot be added without deciding which binds.
PP25_LOOPS = (
    (
        "qa-preflight re-dispatch",
        re.compile(r"(?m)^\*\*The batched ask"),
        re.compile(r"(?m)^\*\*Four rules specific to this phase:\*\*"),
        # The exhaustion state is a checkpoint, not a third dispatch: two
        # unresolved preflights is an environment the user must fix OUTSIDE the
        # workflow. Both tokens are required -- naming the state without ruling
        # out the retry is the wording that let this loop run unbounded.
        ("`human_action` checkpoint", "not a third dispatch"),
    ),
    (
        "re-qa-build extra rounds",
        re.compile(r"(?m)^\*\*Extra rounds when the mutation floor is unmet"),
        re.compile(r"(?m)^\*\*Hard boundary"),
        ("the router stops and asks",),
    ),
)
PP25_CAP = re.compile(r"\*\*Cap: (\d+) ")

# (b) M3. The auditor said `cc10x_task_completed_guard.py` "faults when
# remediation_history is not a list". Measured: it logs an audit event, writes a
# stderr warning and `return 0` -- and the branch is UNREACHABLE anyway, because
# the shipped skeleton initialises `remediation_history: []`, which IS a list.
#
# That measurement is what decides this property's scope, and the scope is the
# whole point. An invariant asserting "the array is a list" would be green at
# HEAD *and* green against the defect. The real defect is one level down:
# `remediation-and-research.md`'s Circuit-breaker section makes appending
# `{ts, phase, reason, cycle_number}` MANDATORY on every `kind:remfix` creation,
# and the guard counts those entries as the hook-enforced backstop for the
# 3-cycle breaker -- while `qa-workflow.md` creates a `kind:remfix` task
# (`re-qa-build`) and contained the token `remediation_history` ZERO times. So
# the count stayed 0 for every QA workflow, the breaker could never fire, and
# QA's "cap: 2 extra rounds" was LLM-counted with no backstop at all: the
# precise condition that mandate exists to remove.
#
# The property therefore asserts the APPEND DUTY IS STATED IN THE QA LAW, and
# its negative control is the deletion of that duty. Control (ii) is the run
# that justifies the property existing: with the duty deleted the artifact is
# still valid JSON with `remediation_history: []` and the task-completed guard
# still exits 0 -- no existing check anywhere catches this.
#
# Asserted inside the re-qa-build window for PP-25(a)'s reason, and the SHAPE is
# asserted alongside the token: an append of the wrong shape is not the entry
# the guard's consumers read, and Phase 6 consumes this exact quadruple.
PP25_REMHIST_TOKENS = (
    "`remediation_history`",
    "`{ts, phase, reason, cycle_number}`",
)


# PP-26. P1 + M8 + M1b + M8b + P8, and the two surfaces (SF-7, SF-8) a gap
# review found after the phase was written. `qa-review` and `qa-hunt` run, and
# at HEAD NOTHING consumes their verdicts: `code-reviewer` emits
# `APPROVE`/`CHANGES_REQUESTED`, `failure_stop_gate` halts on `FAIL`/`BLOCKED`
# only, and `re-qa-build` existed solely for an unmet mutation floor. So a
# harness the reviewers rejected reached `qa-executor` and could PASS -- the
# route's own silently-green-suite failure mode, one level up, in the route
# that exists to catch it.
#
# (a) THE CONSEQUENCE IS NAMED, AND THE SINK ADMITS QA. Two halves, one check
# id, each named separately in the detail so a red sends the reader to one file:
#
#   half 1, qa-workflow.md -- the QA remediation block exists, is uniquely
#   line-anchored, and INSIDE ITS OWN WINDOW names the triggering verdicts, the
#   phase it halts, the target phase, the origin value, and the sink. Window-
#   scoped for PP-18's recorded reason and not merely for symmetry:
#   `deferred_findings`, `re-qa-build` and `CHANGES_REQUESTED` are all tokens
#   that plausibly appear elsewhere in a 600-line route law -- `re-qa-build`
#   already occurs in the mutation-floor block 80 lines above -- so a whole-file
#   test is satisfied by text that says nothing about a review finding.
#
#   half 2, workflow-artifact-and-hook-policy.md (SF-8) -- the `deferred_findings`
#   schema entry NAMES QA's surfacing point. Without this half the property
#   asserts that QA writes to an array whose own schema entry says it is
#   "surfaced once at BUILD-DONE triage, never consumed mid-flight" -- and
#   ADR-2 removed the finishing menu that would give QA a BUILD-DONE triage. A
#   sink whose schema documents no reader on this route is a Minor evaporating
#   with extra steps, which is the exact defect P8 is. Asserted on the
#   `deferred_findings` bullet ALONE, not the whole schema list: "QA" occurs
#   throughout that file and the bullet is the only place the array's readers
#   are enumerated.
PP26A_START = re.compile(r"(?m)^\*\*A harness review finding has a consequence")
PP26A_END = re.compile(r"(?m)^#### Execute \(`phase:qa-execute`\)$")
# The five things the block must name. Each is here because its absence is a
# distinct live defect, not because it rounds the list out:
#   the two verdicts   -- P1: neither is a value failure_stop_gate recognises,
#                         so the block that names them IS the gate;
#   `qa-execute`       -- the advancement being halted; a consequence that does
#                         not say what stops is a note, not a rule;
#   `re-qa-build`      -- M8: the target phase, chosen so no phase token is
#                         invented (PP-4/PP-5 are the guards on that decision);
#   the origin value   -- M8/M8b: the whole dispatch turns on it. `origin:` set
#                         to `code-reviewer` matches the SKILL.md §7 row that
#                         sends kind:remfix to `component-builder`, a product
#                         builder with a product-code licence dropped into the
#                         one phase that spends a hard boundary forbidding it;
#   `deferred_findings`-- P8: the sink, without which a QA Minor evaporates.
PP26A_TOKENS = (
    "`CHANGES_REQUESTED`",
    "`qa-hunt`",
    "`qa-execute`",
    "`re-qa-build`",
    "`origin:qa-harness-builder`",
    "`deferred_findings`",
)
# SF-8's half. The bullet is located by its own line anchor in the hook policy's
# artifact schema list; the tokens are QA's presence and the surfacing point the
# QA block promises, so the two files cannot drift into naming different points.
PP26A_SINK_BULLET = re.compile(r"(?m)^- `deferred_findings` accumulates .*$")
PP26A_SINK_TOKENS = ("QA", "DEBUG offer", "report")

# (b) THE CARVE-OUT NAMES WHAT IT CARVES OUT OF, IN BOTH DIRECTIONS, and the two
# directions are asserted as SEPARATELY FAILING halves because they protect
# against opposite mistakes.
#
# ADR-4 keeps `remediation-and-research.md` read-only and lands QA's remediation
# rules in `qa-workflow.md` instead. The stated cost was that a reader of the
# kernel file cannot see the QA exception, mitigated by making the QA block cite
# the kernel by section -- that is half 1.
#
# SF-7 found the cost is larger than ADR-4 priced it. `SKILL.md`'s `## 11.
# Re-Review Loop` says to apply the kernel's §11 block "whenever a `kind:remfix`
# task completes", unqualified. THAT is the line a router actually executes when
# a `re-qa-build` completes -- and §11 then creates a `code-reviewer` re-review
# and an `integration-verifier` re-verify, while its own precondition gate
# demands COVERING_TESTS / TEST_COMMAND / TEST_OUTPUT that `qa-harness-builder`
# does not emit. So it FAILS CLOSED on a correct QA remfix: the half that hangs
# a run. A carve-out that exists only in `qa-workflow.md` is invisible from the
# point of execution, so half 2 asserts the exception is stated at the kernel
# line too.
#
# Controls (ii) and (iii) delete one citation each and are what make "both
# directions" a measurement instead of a sentence.
# `### Re-review precondition gate` is in this tuple because of a control run,
# not for completeness. Control I-50 deleted the §11 citation from the carve-out
# sentence and half 1 stayed GREEN: the block ALSO names `## 11. Re-Review Loop`
# in its closing pointer at SKILL.md's own section of that name, and a substring
# test cannot tell the two citations apart. The precondition gate is the sub-block
# of the KERNEL's §11 that actually fails closed on a QA remfix (it demands
# COVERING_TESTS / TEST_COMMAND / TEST_OUTPUT), it occurs exactly once, and the
# SKILL.md pointer has no reason to name it. So it is the token that makes the
# citation half fail when the citation is what was removed.
PP26B_QA_TOKENS = (
    "remediation-and-research.md",
    "### Rule matrix",
    "## 11. Re-Review Loop",
    "### Re-review precondition gate",
)
# Half 2's window: the SKILL.md `## 11.` section, heading to next `## `. Anchored
# and exactly-one-match, never whole-file -- `re-qa-build` and `qa-workflow.md`
# both occur elsewhere in SKILL.md (the §7 dispatcher table names both), so a
# file-wide test for them is green with the kernel line still unqualified, which
# is precisely the state SF-7 found and this half exists to end.
PP26B_SKILL_START = re.compile(r"(?m)^## 11\. Re-Review Loop$")
PP26B_SKILL_END = re.compile(r"(?m)^## ")
PP26B_SKILL_TOKENS = ("re-qa-build", "qa-workflow.md", "exception")

# PP-27(a). P4 + S-5. The no-product-code rule is stated three times, and all
# three statements are EXHAUSTIVE ENUMERATIONS of three agents -- researcher,
# harness builder, executor. `cc10x:planner` runs `qa-plan` and `qa-re-plan`
# holding `Edit, Write, Bash` (planner.md:7), so the set is wrong by one at
# every site.
#
# The hole is narrower than the sentence is wrong, and saying which is which is
# the substance of the fix: `cc10x_qa_isolation_guard.PLAN_PHASES` carries
# `qa-plan` and `qa-re-plan`, so the filesystem outside `.cc10x/` is already
# ENFORCED shut for both. The sentence is the NOTICE. A rule that enumerates
# three agents and omits the fourth still teaches the reader the wrong set, and
# the reader is the router.
#
# Deliberately NOT fixed by adding `PRODUCT_CODE_TOUCHED` to the planner
# contract: the planner is shared with the PLAN route, so a QA-motivated
# required field would make every PLAN run emit it. That is why this property
# asserts a SENTENCE and a GUARD NAME rather than a contract field.
#
# PER SITE, PER FILE, and that is the load-bearing decision. Two of the three
# sentences live in the same file; a property reporting "some site omits the
# planner" over three sites sends the next reader to grep three windows. Control
# (i) deletes the token from the SKILL.md site alone and the red must name
# SKILL.md alone.
#
# Anchored per bullet -- the matched line plus its indented continuation lines --
# never whole-file. `planner` appears dozens of times in both files (it is an
# agent name, a phase prefix and a skill id), so a file-wide substring test is
# GREEN against every injection this property exists to catch. PP-14's recorded
# trap, in a fifth file pair.
#
# Read over _decommented() rather than _normative() because the DISPATCH half
# lives inside ```text fences, which are the normative surface for a dispatch
# (PP-21(a) takes the same position for the same reason). N-3: _decommented() is
# a NO-OP on qa-workflow.md -- zero HTML comments at HEAD -- so the helper is
# not what makes this property sound; control (i) is.
PP27A_SITES = (
    # (file-key, human label, line-anchored regex opening the bullet)
    ("SKILL.md", "Never let QA edit product code", r"^- Never let QA edit product code\."),
    (
        "qa-workflow.md",
        "QA-specific rules: QA never edits product code",
        r"^- \*\*QA never edits product code\.\*\*",
    ),
    (
        "qa-workflow.md",
        "qa-build rules: Never edit product code",
        r"^- \*\*Never edit product code\.\*\*",
    ),
)
# Four agents, because four agents hold write tools inside the QA route. The
# tokens are the spellings the prose already uses for the first three; `planner`
# is the addition.
PP27A_AGENTS = ("researcher", "harness builder", "executor", "planner")
# The ENFORCEMENT/NOTICE distinction is asserted at exactly one site -- the
# QA-specific rules block -- rather than at all three. Requiring the guard name
# in every sentence would push an implementation detail into SKILL.md's
# never-list, which is a list of rules, not of mechanisms.
PP27A_ENFORCEMENT_SITE = "QA-specific rules: QA never edits product code"
PP27A_ENFORCEMENT_TOKENS = ("PLAN_PHASES", "ENFORCEMENT", "NOTICE")
# The two plan-phase dispatch windows. Anchored on the unique task-id
# terminator line and walked BACK to the opening `TaskCreate({`, because the
# opening line is identical in all nine dispatch blocks in the file while the
# terminator is unique per node.
PP27A_DISPATCHES = (
    ("qa-plan", "qa_plan_task_id"),
    ("qa-re-plan", "qa_replan_task_id"),
)
PP27A_DISPATCH_TOKEN = "Never edit product code"

# PP-27(b). P6. `phase_exit_gate` is defined route-neutrally (hook policy
# "a phase task may complete only when its agent contract validates") but the
# per-agent loop INVOKES it "for BUILD" only. QA added seven phases under a loop
# that never runs the gate on any of them.
#
# ANCHORED ON THE INVOCATION LINE, never whole-file, and this is the property's
# whole point. `phase_exit_gate` occurs five times in SKILL.md: the router-owned
# gates list, this line, the phase-cursor rule, the inline-fallback section, and
# the terse-imperative rule -- plus once more in the hook policy's definitions.
# A file-wide search for the token is GREEN against the exact injection this
# property exists to catch, which is PP-14's recorded trap verbatim. Control
# (ii) runs the contrast: with the routes reverted to BUILD-only, `grep -c
# phase_exit_gate` on SKILL.md still returns 5.
#
# The inline-fallback invocation is route-neutral BY DESIGN ("at each phase
# boundary exactly as in the default loop step 6") and this property must not
# touch it -- hence the `for <routes>, run` shape in the anchor, which only the
# per-agent loop line has.
#
# Scope is deliberately BUILD + QA and not "every route". P6's premise -- the
# gate's definition is route-neutral -- makes widening tempting; widening is a
# behavioural change to DEBUG, REVIEW and PLAN that no finding in this set
# audited.
PP27B_INVOCATION = re.compile(r"(?m)^\s*- for (.+?), run `phase_exit_gate`;")
PP27B_ROUTES = ("BUILD", "QA")

# PP-28. P5. Preflight-mode `BUG_CANDIDATES` are persisted under `qa.preflight`
# (the law's step 1: "the rest of the contract to `qa.preflight`") and were never
# merged into `qa.bug_candidates`, which is the ONLY key the DEBUG offer reads.
# A preflight BLOCK is terminal for that run -- the executor is never reached --
# so a real defect found at T1-T4 died in a sub-key nothing consumes.
#
# Both keys are asserted VERBATIM, because a merge stated with one key spelled
# wrong is precisely the `results.` / `qa.` drift M9 already caught once in this
# same file. They are also the two keys PP-21(a) resolves full-depth into the
# skeleton, so a typo here is caught twice, from two directions.
#
# Window-anchored to the *Persist first* section, read over _normative(). The
# section sits DOWNSTREAM of the stray fence a later phase deletes, so its
# printed size is a genuine measurement rather than a control.
PP28_START = re.compile(r"(?m)^#### 1\. Persist first$")
PP28_END = re.compile(r"(?m)^#### 2\. Offer, do not start$")
PP28_TOKENS = ("`qa.preflight`", "`qa.bug_candidates`")
# The merge must be stated on the PREFLIGHT return, not only the executor's.
# Without this token the window is satisfied by the pre-existing executor
# sentence, which already names both keys' file and one of the keys.
PP28_PREFLIGHT_RETURN = "On `qa-harness-builder` preflight return"

# PP-29. P10, generalised. Every filesystem path the QA law NAMES must resolve
# on disk. P10 was one dangling pointer -- `docs/plans/2026-08-10-qa-route-rfc.md`,
# cited by both qa-workflow.md's status line and SKILL.md's QA note, and absent
# from the repo since before either line was written. A pointer to a document
# that does not exist is worse than no pointer: it sends the reader looking for
# a governing design and tells them nothing when they fail to find it. This
# property is that one-shot correction made mechanical, so the next one is
# caught the day it is written rather than by an audit.
#
# SCOPE, frozen and argued. Two surfaces: the whole of `qa-workflow.md`, and the
# QA LINES of SKILL.md. "SKILL.md's QA lines" is undefined prose unless it is
# pinned to a regex, so it is: every line matching PP29_SKILL_QA_LINE below
# (33 lines at HEAD). SKILL.md is a route-neutral file and the closed file set
# of this change covers only its QA-related lines; extracting from the whole
# file would make this property red on a BUILD or PLAN path defect it has no
# mandate to fix, in a file it may not edit.
#
# FOUR resolution bases, and the fourth is the one that took a review pass to
# find. `references/qa-workflow.md` (SKILL.md :235, :312, :420) resolves under
# NONE of repo-root, `plugins/cc10x/`, or `${CLAUDE_PLUGIN_ROOT}` --
# `plugins/cc10x/references/` does not exist. It is relative to the directory of
# the file that names it, `plugins/cc10x/skills/cc10x-router/`. Without that
# base this property is RED AT HEAD on a path that exists, which is red for the
# wrong reason from a property that is otherwise right. `${CLAUDE_PLUGIN_ROOT}`
# resolves to PLUGIN at runtime, so it is the same base and is not listed twice.
PP29_SKILL_QA_LINE = re.compile(r"\bQA\b|\bqa[-_]")
# Path-shaped: a backticked token containing a `/` and a file extension. The
# `/` requirement is what keeps bare filenames and code identifiers out; the
# extension is what keeps `.cc10x/qa/` style directory prefixes out.
PP29_PATH_TOKEN = re.compile(r"`([^`\s]*/[^`\s]*\.[A-Za-z0-9]+)`")
# The exclusion set is FROZEN and covers TWO kinds of token, not one. Revision 1
# of this property excluded only (a) and would have been red at HEAD on the glob.
#   (a) TEMPLATED -- any `{...}` segment (`{workflow_uuid}`, `{env_key}`). These
#       resolve only at runtime, against a workflow that has already started.
#   (b) GLOB-BEARING -- any `*`. `.cc10x/workflows/*.json` is the only member
#       today. A glob names a runtime FAMILY under a state root that does not
#       exist in a clean checkout, so `os.path.exists` on it is meaningless, and
#       resolving it AS a glob would assert that a workflow has already run --
#       turning a static document property into a test of session state.
# Both exclusions are load-bearing and both were measured: control (v) removes
# (b) and the property goes red naming the glob.
PP29_EXCLUDE = (re.compile(r"\{[^}]*\}"), re.compile(r"\*"))
# Two anti-vacuity floors, each grounded on a census taken against this tree
# rather than rounded: 8 path-shaped tokens at HEAD, 7 after the RFC pointer is
# removed, of which 5 survive the exclusions and all 5 resolve. A floor set just
# under the complete count silently does the membership half's job (PP-21(b)'s
# recorded mistake), so both floors sit clear of it: their only duty is proving
# the extraction and the exclusion set still produce a non-empty set to ask the
# existence question about.
PP29_MIN_EXTRACTED = 6
PP29_MIN_RESOLVED = 4

# PP-30(a). M6 / ADR-2. QA offers no workspace isolation, AND SAYS WHY.
#
# `qa-workflow.md` step 0 was a verbatim copy of BUILD's worktree offer ("Same
# policy as BUILD step 0"). BUILD's offer is safe because BUILD *authors* the
# change it isolates. QA does not author it: P3 establishes that QA's tree is
# dirty BY CONSTRUCTION, because the uncommitted work is frequently the system
# under test. A worktree is a DIFFERENT CHECKOUT, so accepting the offer does
# not isolate the run -- it silently substitutes what is being measured. The
# offer was copied without its precondition.
#
# BOTH HALVES ARE REQUIRED, and that is the property's whole design. A purely
# negative assertion ("no offer phrasing") rewards SILENT DELETION: the next
# reader finds an unexplained absence, reads BUILD's step 0, and puts it back.
# ADR-2's point is that the absence is ARGUED. Control (ii) deletes the
# rationale while leaving the offer absent and this property must go red -- it
# is the run that separates this construction from the cheap one.
#
# ASYMMETRIC NORMALISATION, deliberately. The NEGATIVE half reads the
# de-commented text, fences INCLUDED: an offer re-parked into a dispatch fence
# is a real offer, because dispatch text is the normative surface for a dispatch
# (PP-21(a) and PP-27(a) take the same position). The POSITIVE half reads
# `_normative()`: a rationale inside <!-- --> or inside a fence is not law, and
# a gutted argument parked in a code block is exactly PP-18's recorded I-1/I-4
# shape.
#
# The forbidden patterns are the OFFER's vocabulary, never the bare word
# "worktree" -- the rationale block itself must say "a worktree is a different
# checkout", so a property forbidding the word would forbid its own fix. That is
# the negative-assertion trap PP-15(c) and PP-24 both record: a scope containing
# a legitimate use fails forever.
PP30A_FORBIDDEN = (
    re.compile(r"(?i)workspace isolation"),
    re.compile(r"(?i)native worktree primitive"),
    re.compile(r"(?i)git worktree add"),
    re.compile(r"(?i)isolation is warranted"),
)
PP30A_RATIONALE = re.compile(
    r"(?m)^\*\*QA runs in the tree it was pointed at, and does not offer to move it\.\*\*"
)
# The three clauses that make the absence an ARGUMENT rather than a note: what
# QA does instead, why a worktree cannot serve it, and the decision record a
# reader who disagrees must argue with.
PP30A_TOKENS = (
    "the system under test",
    "a worktree is a different checkout",
    "ADR-2",
)

# PP-30(b). M7 / ADR-3 part 3. Both harness-review dispatches NAME their surface.
#
# `qa-review` and `qa-hunt` were dispatched with `scope:N/A` and no named
# surface, so each read-only agent chose its own. The correct surface is the
# harness builder's own enumeration: `ARTIFACTS_CREATED` (every path it wrote)
# and `HARNESS_MANIFEST`. BUILD's instrument -- `git_base_sha` plus a
# `BASE..HEAD` diff package -- is wrong here: `qa-harness-builder` never
# commits, so the diff is empty by construction and an empty diff package reads
# as "nothing changed".
#
# SCOPE IS THE DISPATCH TEXT ONLY, and the division is deliberate. That these
# two fields are REQUIRED, non-empty and non-null in `MODE: harness` is
# PP-23(b)'s assertion, over the hook-policy rows and the agent's declaration
# line. This property asserts only that the two dispatch prompts NAME them.
# Neither should later be "improved" into the other's job: a dispatch-text-only
# property stays GREEN while the field it names is optional (measured -- see the
# contrast recorded in the docstring), and a contract-only property stays green
# while no prompt ever points the reviewer at the field.
#
# WINDOW-ANCHORED PER DISPATCH, never whole-file and never whole-fence. Both
# tokens appear in `qa-harness-builder.md`'s contract block, so a repo-wide
# search is trivially satisfied; and both dispatch blocks share one ```text
# fence, so a fence-wide search lets `qa-review` satisfy `qa-hunt`'s half --
# PP-18's recorded I-2 shape, and exactly what control (iv) injects. Anchored
# the way PP-27(a)'s dispatch windows are: on the unique task-id terminator
# line, walked BACK to the opening `TaskCreate({`, because the opening line is
# identical in every dispatch block in the file while the terminator is unique.
#
# Read over `_decommented()` for PP-27(a)'s reason: the dispatch lives inside a
# ```text fence, which is its normative surface.
PP30B_DISPATCHES = (
    ("qa-review", "qa_reviewer_task_id"),
    ("qa-hunt", "qa_hunter_task_id"),
)
PP30B_TOKENS = ("`ARTIFACTS_CREATED`", "`HARNESS_MANIFEST`")

# PP-31. M5 / ADR-1. The QA phase-token spellings are FROZEN, and the freeze
# cites its reason.
#
# WHAT THIS PROPERTY IS, AND WHAT IT IS NOT. It is a TRIPWIRE. Its value is not
# that it proves anything about behaviour — it proves nothing about behaviour —
# but that it forces a future editor who reaches for these tokens to read the
# argument before changing them. The asymmetry it freezes is real and is
# deliberately left in place: `qa-re-plan` is prefixed where its siblings
# `re-qa-build` / `re-qa-execute` are infixed, and `qa-plan-review` /
# `qa-plan-review-2` do not match PLAN's `plan-review-gap-1` / `-2`. ADR-1
# prices that asymmetry and keeps it.
#
# EDITING THIS CONSTANT TO MAKE A RENAME GREEN IS THE WHOLE COST OF THE RENAME,
# NOT A FORMALITY. That sentence is the property. Three measured reasons:
#   1. `re-qa-build` / `re-qa-execute` follow the route-wide `re-` prefix
#      already in the enum (`re-review`, `re-hunt`, `re-verify`, `re-plan`).
#      They are the CONFORMING names; `qa-re-plan` is the single outlier. A
#      rename is a five-surface change to fix one token.
#   2. A rename must reach `cc10x_qa_isolation_guard.PLAN_PHASES` — a live
#      security-relevant constant that literally contains `"qa-re-plan"` — or
#      the renamed phase silently stops being read-only. Reaching it turns PP-2
#      red, and the only repair is editing `EXPECTED_PLAN_PHASES`, the constant
#      PP-2 asserts against. A change whose completion criterion is "edit the
#      guard until it stops complaining" is INDISTINGUISHABLE FROM DEFEATING THE
#      PROPERTY. Control (i) below runs exactly that and records the sympathetic
#      red; it is the evidence for ADR-1's central claim, not a side effect.
#   3. SKILL.md §4 reconstructs runnable tasks from `wf:` + `kind:` + `phase:`.
#      An in-flight task carrying `phase:qa-re-plan` becomes unroutable after a
#      rename and — worse — stops matching `PLAN_PHASES`, so the isolation guard
#      stops treating it as read-only. The rename opens the exact mutation hole
#      PP-1 and PP-3 exist to close, for every workflow spanning the change.
# And `plan-review-gap-N`'s `-gap-` infix is a fossil of `plan-gap-reviewer`'s
# older name, so aligning QA's clearer `qa-plan-review-N` down to it would be
# aligning to legacy.
#
# TWO HALVES, and the second is what stops the constant and the argument from
# drifting apart. A frozen set with no anchored rationale is a rule with no
# reason attached, which is precisely the "tidy it up" invitation this exists to
# refuse. So the rationale block in qa-workflow.md is asserted here, in the same
# check, over `_normative()` text — an argument inside `<!-- -->` or parked in a
# fence is not law (PP-18's recorded I-1/I-4 shape).
#
# Membership is by hyphen SEGMENT (`"qa" in token.split("-")`), never substring:
# a substring test would sweep in any future token merely containing the letters
# and quietly widen a set whose whole point is that it is closed.
PP31_QA_TOKENS = frozenset(
    {
        "qa",
        "qa-research",
        "qa-plan",
        "qa-plan-review",
        "qa-re-plan",
        "qa-plan-review-2",
        "qa-preflight",
        "qa-build",
        "qa-review",
        "qa-hunt",
        "qa-execute",
        "re-qa-build",
        "re-qa-execute",
    }
)
PP31_ENUM_LINE = re.compile(r"(?m)^phase:\{([^}]+)\}")
# Anti-vacuity floor on the WHOLE enum, not the QA slice: if the §3 line stops
# parsing, the QA slice is empty and `set() == frozenset(...)` is False, which
# would be red for the wrong reason with a message about missing tokens rather
# than about a dead anchor. 39 members at HEAD; the floor's only duty is proving
# the line still parses as an enum.
PP31_MIN_ENUM_MEMBERS = 30
PP31_RATIONALE = re.compile(
    r"(?m)^\*\*The QA phase tokens are asymmetric, and the asymmetry is priced\.\*\*"
)
# One token per clause of ADR-1 that a future editor must actually read. Not
# decoration: each is a distinct cost of the rename, and a block that dropped
# any one of them would read as a style note.
PP31_RATIONALE_TOKENS = (
    "ADR-1",
    "`PLAN_PHASES`",
    "`EXPECTED_PLAN_PHASES`",
    "in-flight",
    "`re-`",
)

# PP-32. P9 and its siblings. EVERY DELIBERATE OMISSION IN THE QA LAW CARRIES
# ITS RATIONALE IN THE SAME BLOCK.
#
# This property encodes something the route ALREADY DOES WELL and converts a
# culture into a check. The audit's own *Confirmed aligned* list credits QA
# three times for arguing an omission rather than asserting it. A culture
# survives exactly as long as the people who hold it; a check outlives them.
# What it forbids is the cheap kind of divergence — dropping a sibling route's
# lane and saying nothing — which reads to the next maintainer as an oversight
# and gets "fixed" back in.
#
# THREE omissions, each WINDOW-ANCHORED to the block that makes it, because the
# vocabulary of one omission's argument occurs in the others' neighbourhoods and
# a file-wide test lets any one satisfy all three (PP-18's recorded I-2 shape,
# and PP-25(a)'s I-34 in this same file):
#   (1) probe drops plan review     — the reduced-task-graph block
#   (2) no amendment lane           — the one-owner-per-route paragraph
#   (3) no `re-qa-preflight` phase  — the retry-source paragraph
#
# THE FOURTH OMISSION IS DELIBERATELY NOT HERE. "QA offers no workspace
# isolation" (ADR-2) is already asserted by PP-30(a)'s POSITIVE half, which
# requires the rationale block and its three argument clauses. Asserting it
# again here would be two properties owning one fact — the duplication that made
# the byte-duplicated PASS rule a trap, and the thing PP-30(b)/PP-23(b)'s split
# is comment-guarded against in the other direction. If PP-30(a) is ever
# narrowed to its negative half, THIS is the comment that says where the
# positive half went.
#
# On (1)'s tokens: the sibling named must be `build_scope=trivial`, not PLAN.
# PLAN mandates the fresh-review DAG for every saved plan, so measured against
# PLAN the omission is simply a violation; the sibling for a REDUCED TASK GRAPH
# is BUILD-trivial, which drops the separate reviewer and folds a review pass
# into the verifier — exactly what probe does by folding a harness sanity pass
# into the executor. Naming the wrong comparand is how a justification ends up
# arguing for the thing it was written to justify away.
PP32_OMISSIONS = (
    (
        "probe drops plan review",
        re.compile(r"(?m)^#### Reduced task graph \(`qa_scope=probe`\)$"),
        re.compile(r"(?m)^### Isolation and phase discipline \(ENFORCED\)$"),
        (
            "`build_scope=trivial`",
            "anti-anchoring",
            "`SCOPE_INCREASES`",
            "evidence protocol",
        ),
    ),
    (
        "no amendment lane",
        re.compile(r"(?m)^\*\*One owner per route,"),
        re.compile(r"(?m)^\*\*A correction believed in one artifact"),
        ("`phase:plan-review-amendment`", "PLAN-only", "no QA call site"),
    ),
    (
        "no `re-qa-preflight`",
        re.compile(r"(?m)^On resolution the router re-dispatches"),
        re.compile(r"(?m)^\*\*Cap: 2 re-dispatches"),
        ("`re-qa-preflight`", "`re-qa-build`", "downstream", "from the user"),
    ),
)


# PP-33 -- QA is a member of every enumeration of workflow types, and the
# extractors that look for those enumerations still find them.
#
# The defect: the `__WORKFLOW_TYPE__` enum in cc10x-router/SKILL.md was written
# before the QA route existed and was never extended. The isolation guard
# returns 0 immediately unless `workflow_type == "QA"`
# (cc10x_qa_isolation_guard.py:220), so every QA isolation rule is unreachable
# in production if the router never stamps QA. Hardening a guard behind an
# unreachable predicate is the same fail-open in a new costume.
#
# FOUR SITES, FOUR SYNTACTIC SHAPES -- which is why this is a table and not one
# regex. A single corpus-wide regex reaches exactly ONE of them:
#
#   S1  cc10x-router/SKILL.md      (BUILD | DEBUG | ...)          parens + pipes
#   S2  memory-file-contracts.md   [PLAN | BUILD | ...]           SQUARE + pipes
#   S3  cc10x-guide/SKILL.md       N workflows (A, B, C)          parens + COMMAS
#   S4  README.md                  <strong>N workflows</strong>   COUNT ONLY
#
# FOUR NORMALISERS, and that is the second reason this is a table. Measured:
# memory-file-contracts.md has fence pairs at (42, 75), (79, 94) and (98, 117)
# and the enum sits at 103 -- strictly INSIDE the third. `_normative()` deletes
# fenced blocks, so under `_normative()` S2's anchor matches ZERO times and
# PP-33(a) would be red on the precondition against a CORRECTLY EDITED repo.
# S2 is therefore read through `_decommented()`. The other three were measured
# the same way and are clean: cc10x-router/SKILL.md:276 sits BETWEEN the fence
# pairs at 269-271 and 283-288; cc10x-guide/SKILL.md:37 precedes that file's
# first fence at 45; README.md:18 is raw HTML with no fence or HTML comment
# above line 30. The normaliser is a per-site property recorded next to the
# measurement that forced it, never a file-wide default.
#
# S4 carries no member list, so it asserts the only thing it does carry: the
# count -- DERIVED from the SKILL.md section 1 Intent Routing table, not frozen
# as a literal. A literal would have to be edited by the same hand that adds a
# route, and that is precisely the hand that forgets.
#
# Anchoring is PER LINE, never whole-file. The bare token `QA` occurs dozens of
# times in each of these files, so `"QA" in text` is satisfied by any of them.
# Membership is asserted against the PARSED MEMBER LIST of the anchored line.
#
# Fields: (id, display, path, basis, anchor, extractor, split, count, label).
# `split` is None for a count-only site; `count` is a second regex for a site
# that states its own cardinality alongside its members.
PP33_SITES = (
    (
        "S1",
        "cc10x-router/SKILL.md",
        ROUTER / "SKILL.md",
        "normative",
        re.compile(r"(?m)^- `__WORKFLOW_TYPE__`.*$"),
        re.compile(r"\(([A-Z][A-Z-]*(?:\s*\|\s*[A-Z][A-Z-]*)+)\)"),
        "|",
        None,
        "paren enum",
    ),
    (
        "S2",
        "memory-file-contracts.md",
        PLUGIN
        / "skills"
        / "memory-and-handoff"
        / "references"
        / "memory-file-contracts.md",
        "decommented",
        re.compile(r"(?m)^\[PLAN \| BUILD.*$"),
        re.compile(r"\[([A-Z][A-Z-]*(?:\s*\|\s*[A-Z][A-Z-]*)+)\]"),
        "|",
        None,
        "bracket enum",
    ),
    (
        "S3",
        "cc10x-guide/SKILL.md",
        PLUGIN / "skills" / "cc10x-guide" / "SKILL.md",
        "normative",
        re.compile(r"(?m)^.*[0-9]+ workflows \(.*$"),
        re.compile(r"\(([A-Z][A-Z-]*(?:,\s*[A-Z][A-Z-]*)+)\)"),
        ",",
        re.compile(r"([0-9]+) workflows \("),
        "paren+comma enum",
    ),
    (
        "S4",
        "README.md",
        PLUGIN.parent.parent / "README.md",
        "normative",
        re.compile(r"(?m)^.*<strong>[0-9]+ workflows</strong>.*$"),
        re.compile(r"<strong>([0-9]+) workflows</strong>"),
        None,
        None,
        "marquee count",
    ),
)

# The Workflow column of the SKILL.md section 1 Intent Routing table. This is
# the source of truth S4 is measured against, so it gets its own floor: eight
# rows over eight distinct workflows at the time PP-33 was written.
PP33_ROUTING_ROW = re.compile(r"(?m)^\|\s*\d+\s*\|[^|]*\|[^|]*\|\s*([A-Z][A-Z-]*)\s*\|")
PP33_MIN_ROUTES = 8

# The stamping line. Its SHAPE is proved live by the two sibling route files
# that already carry it -- which is what makes the QA assertion a consistency
# claim across three files rather than three files each proved alone. If the
# shape drifts, the siblings stop matching and PP-33(a) reds on the
# precondition instead of PP-33(b) passing over a regex that reaches nothing.
PP33_STAMP = re.compile(
    r"The router creates the workflow artifact with `workflow_type: ([A-Z][A-Z-]*)`"
)
PP33_STAMP_SIBLINGS = (
    ("triage-workflow.md", "TRIAGE"),
    ("codebase-health-workflow.md", "CODEBASE-HEALTH"),
)


# PP-40. A `§N` citation whose trailing words name a section must not name a
# DIFFERENT section than the number does. Sibling of PP-9, not a rewrite of it:
# PP-9 asks whether the cited number EXISTS, which is why B2 -- `test plan §6
# known gaps` against a template whose `## 6.` is `Test data` and whose `## 7.`
# is `Known gaps` -- was green for as long as the digit was wrong. Existence is
# not resolution.
#
# The verdict rule is FOUR branches, and each one was forced by a measured false
# red on a CORRECT citation:
#   1. no trailing content tokens      -> RESOLVED (fallback). A citation that
#      names no words cannot contradict a title. (`qa-env-plan.template.md:71`,
#      `see test plan §3.`)
#   2. tokens overlap the cited title  -> RESOLVED.
#   3. tokens overlap a DIFFERENT title in the same template -> MISMATCH. This
#      branch is the whole property: it fires only when the words name another
#      section that actually EXISTS, which is exactly what a wrong digit looks
#      like, and is exactly B2.
#   4. tokens overlap no heading at all -> RESOLVED-UNDESCRIPTIVE. The trailing
#      words describe the CITING sentence rather than the cited section, so the
#      citation makes no title claim to check. `qa-workflow.md:119` cites `§3
#      wave count` and `§2 id rollups`; no tokeniser makes `wave count` overlap
#      `Build order`. A rule that reds these asserts that every citation
#      paraphrases its heading, which is not how prose is written. I-90 injects
#      exactly that rule and reds three correct citations.
#   5. the number is not a heading at all -> MISMATCH (`no such heading`).
PP40_MIN_CITATIONS = 8
# Matches `test plan`, `test-plan`, `test-plan.md` -- and the same for env.
# Deliberately as wide as PP-9's own rule (`"env plan" in prefix or "env-plan"`):
# a PP-40 narrower than PP-9 would leave a citation that PP-9 resolves by
# EXISTENCE and that nobody ever title-checks, which is the hole this property
# exists to close.
PP40_PREFIX_VOCAB = {
    "test": re.compile(r"test[-\s]plan"),
    "env": re.compile(r"env[-\s]plan"),
}
PP40_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "its", "it", "s",
    "this", "that", "see", "plan", "table", "list",
}
# Trailing words end at the first of these. `§` is in the set because
# `qa-workflow.md:119` reads `...the §4 wave count and in the §2 id rollups**`:
# without it the trailing words of §4 run past §2 and pick up unrelated prose.
# The 6-word cap is the same defence for lines with no terminator nearby.
PP40_TERMINATORS = (",", ";", ")", "|", ".", "—", "§", "**")
PP40_WORD_CAP = 6
PP40_CITATION = re.compile(r"§(\d+)")
PP40_HEADING = re.compile(r"^## (\d+)\. (.+)$", re.M)
# Citations whose trailing words describe the citing sentence rather than the
# cited section. Measured; both are correct citations. SET EQUALITY, not
# containment: a citation that JOINS this class is a tokeniser regression, and
# one that LEAVES it is a prose edit nobody recorded. Either way, red. I-92 and
# I-93 are both silent unless this is an equality -- each moves exactly one
# correct citation INTO the class and produces no mismatch at all.
PP40_UNDESCRIPTIVE = {
    ("qa-workflow.md", 119, 3),   # "wave count and in the"  vs  ## 3. Build order
    ("qa-workflow.md", 119, 2),   # "id rollups"             vs  ## 2. Coverage plan
}
# There is no exclusion list. The seven unprefixed `§N` in
# `qa-harness-builder.md`'s 64-71 table fall into the NO-PREFIX branch already --
# the bucket PP-9's unresolved contract owns -- and never reach the title
# comparison. A line-range exclusion over 64-71 would additionally drop `:70`,
# the one row in that table carrying an in-cell `test plan` prefix, which DOES
# resolve. An exclusion that only restates what the no-prefix branch does is a
# rule with nothing to do and a line range to rot.


def _pp40_tokens(text: str) -> set[str]:
    """Split on every non-alphanumeric run (hyphens INCLUDED), case-fold, drop
    stopwords, then stem a single trailing `s` from any token of length >= 4.

    Both halves close a measured false red on a correct citation:
      hyphens -- `qa-workflow.md:119` cites `§7 known-gaps table` against
                 `## 7. Known gaps`; unsplit, `known-gaps` is one token and the
                 overlap is 0. Control I-92.
      stem    -- `qa-harness-builder.md:137` cites `env-plan.md §11's predicted
                 blocker list` against `## 11. Blockers and open decisions`;
                 `blocker` != `blockers` and the overlap is 0. Control I-93.
    """
    out: set[str] = set()
    for tok in re.split(r"[^0-9A-Za-z]+", text):
        tok = tok.casefold()
        if not tok or tok in PP40_STOPWORDS:
            continue
        if len(tok) >= 4 and tok.endswith("s"):
            tok = tok[:-1]
        out.add(tok)
    return out


def _pp40_headings(path: Path) -> dict[int, str]:
    return {
        int(m.group(1)): m.group(2).strip()
        for m in PP40_HEADING.finditer(path.read_text(encoding="utf-8"))
    }


def _pp40_normative_lines(text: str) -> set[int]:
    """1-based line numbers inside spans `_normative()` deletes.

    PP-40 iterates the RAW file and skips these, rather than slicing
    `_normative(text)` and iterating that: line numbers in normalised text are
    not file line numbers, and every number this property prints must be one a
    human can open the file to.
    """
    skipped: set[int] = set()
    for pattern, flags in (
        (r"<!--.*?-->", re.DOTALL),
        (r"^```.*?^```", re.DOTALL | re.MULTILINE),
    ):
        for m in re.finditer(pattern, text, flags):
            first = text.count("\n", 0, m.start()) + 1
            last = text.count("\n", 0, m.end()) + 1
            skipped.update(range(first, last + 1))
    return skipped


def _pp40_trailing(rest: str) -> str:
    """Trailing words of a citation: drop a leading `'s`, cut at the first
    terminator, cap at PP40_WORD_CAP words."""
    if rest.startswith("'s"):
        rest = rest[2:]
    cut = len(rest)
    for term in PP40_TERMINATORS:
        found = rest.find(term)
        if found != -1:
            cut = min(cut, found)
    return " ".join(rest[:cut].split()[:PP40_WORD_CAP])


def _pp40_prefix(line: str, upto: int) -> str | None:
    """Most recent prefix-vocabulary match on this LINE before `upto`.

    Inheritance is line-scoped: `test plan §2 coverage table, §6 known gaps`
    resolves BOTH numbers against the test-plan template. Without it, resolved
    drops 10 -> 6 and B2's own citation stops being checked (control I-71).
    Where both vocabularies match, the later one wins: `... test plan §2 ...;
    env plan §9 ...` switches template mid-line.
    """
    best, prefix = -1, None
    for key, rx in PP40_PREFIX_VOCAB.items():
        for m in rx.finditer(line[:upto]):
            if m.start() >= best:
                best, prefix = m.start(), key
    return prefix


def _pp33_raw_lineno(raw: str, line: str) -> int:
    """Raw-file line number of an anchor matched in NORMALISED text.

    Line numbers inside normalised text are not file line numbers; a property
    that reports one is reporting a number no human can open the file to.
    """
    for _i, _l in enumerate(raw.splitlines(), 1):
        if _l == line:
            return _i
    return -1


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

# Deliberately outside the guard's default mutation_allowlist ([".cc10x/"]) —
# a target inside it is allowed regardless of phase, which would make the deny
# cases pass for the wrong reason. On the Bash branch the allowlist is now
# matched against the paths `_bash_paths` extracts from the command, resolved
# and compared as paths; `/tmp/pp6-probe-<pid>` matches no entry under that
# rule. NOTE: the ledger's claim that this comment was false is REFUTED — the
# comment was accurate for the Bash branch even under the old substring test,
# because the substring `.cc10x` does not occur in `mkdir -p /tmp/pp6-probe-N`.
# What was wrong here was only the list it cited.
PROBE_TARGET = f"/tmp/pp6-probe-{os.getpid()}"

# PP-13. Same one-artifact-at-a-time discipline as PP-6, for the same reason
# (latest_workflow_file() resolves by mtime). The pid keeps two concurrent runs
# of this suite from colliding on one workflow id.
PP13_WF_ID = f"wf-test-pp13-{os.getpid()}"

# PP-39. The BLOCKING hook set, derived rather than transcribed.
#
# Revision 1 of this property demanded the policy name all 8 scripts
# hooks.json references and computed `unconditional = 8 - 3 = 5`. Both halves
# were wrong: `cc10x_event_logger.py` and `cc10x_state_persist.py` block
# nothing, and `cc10x_sessionstart_context.py` runs at an event that cannot
# block. A policy that omits a hook which never denies omits nothing. So the
# scope is the set reachable from hooks.json at an event that CAN deny, whose
# source carries a block path.
#
# Measured at this commit — 5 blocking scripts, 3 of them mode-aware:
#   cc10x_pretooluse_guard.py            PreToolUse     load_mode: 1
#   cc10x_git_guard.py                   PreToolUse     load_mode: 0  UNCOND
#   cc10x_qa_isolation_guard.py          PreToolUse     load_mode: 0  UNCOND
#   cc10x_posttooluse_artifact_guard.py  PostToolUse    load_mode: 1
#   cc10x_task_completed_guard.py        TaskCompleted  load_mode: 1
PP39_EVENTS = ("PreToolUse", "PostToolUse", "TaskCompleted")
PP39_SCRIPT_REF = re.compile(r"([A-Za-z0-9_]+\.py)")
PP39_BLOCK_PATH = re.compile(r"pretool_deny\s*\(|sys\.exit\(2\)|return 2\b")
# The CALL, not the import. `cc10x_qa_isolation_guard.py` carried a dead
# `load_mode,` import line with no parenthesis; an importing-but-never-calling
# script is unconditional, and this regex is what makes that distinction.
PP39_LOAD_MODE_CALL = re.compile(r"load_mode\s*\(")
# Anti-vacuity floor, shape (a). `set() - set()` is empty and every membership
# test over an empty set passes. 5 measured at this commit; if the block-path
# regex stops matching the set shrinks and this floor is what notices.
PP39_MIN_HOOKS = 5
# W8 — the policy's mode paragraph. Window-anchored rather than whole-file
# (vacuity shape (b)): the hook enumeration above it now carries the same
# basenames, so `name in policy_text` would be satisfied by the enumeration
# and would never see a false mode claim. R9 semantics: the end anchor is
# searched over the whole text and required to match exactly once, AFTER the
# start anchor — an end regex that matches its own start line yields a 0-byte
# window in which every `not in` passes.
PP39_W8_START = re.compile(r"(?m)^- Default mode is audit-only")
PP39_W8_END = re.compile(r"(?m)^- Repo-local")

# ---------------------------------------------------------------- PP-41
# Every producer enum covers the values its consumers require. Three
# sub-checks over three different producers, one defect shape: the enum at
# the emitter is narrower than the contract downstream of it, so a
# conforming emitter has to lie or improvise.
#
# BASIS — all five windows read `_decommented()`, NEVER `_normative()`.
# Measured at this commit: `^OBSERVABILITY_POINTS:` (W4), `^TEARDOWN_STATUS:`
# (W3) and the two preflight markers (W2) match ONCE through
# `_decommented()` and ZERO times through `_normative()`, because all three
# sit inside ```yaml fences that `_normative()` deletes. This is PP-20's
# trap (lines 1571-1572, "0/0 through _normative()") in three new places.
#
# MEASURED CORRECTION to the plan's R11 table: W9 -- qa-researcher.md's
# `**CONTRACT RULES:**` region -- is claimed there to also vanish under
# `_normative()`. It does not. The researcher's yaml fence runs 120-166 and
# CONTRACT RULES starts at 168, so the anchor matches ONCE under both
# normalisers and the window is 1104 B under both. `_decommented()` is still
# the right basis (it is the basis its three siblings need and the window is
# byte-identical), but the fence-containment argument does not apply to W9.
RESEARCHER_AGENT = PLUGIN / "agents" / "qa-researcher.md"
QA_FEATURE_MAP_TPL = PLUGIN / "templates" / "qa-feature-map.template.md"
# The three provenance values, in the vocabulary both consumers already use.
PP41_PROVENANCE = ("V", "Vp", "I")
PP41_W4_START = re.compile(r"(?m)^OBSERVABILITY_POINTS:")
# R9 semantics: searched from AFTER the start-anchor line. `^[A-Z_]+:`
# searched from the start anchor's own offset matches the start anchor
# itself and yields a 0-byte window in which every `not in` passes.
PP41_W4_END = re.compile(r"(?m)^[A-Z_]+:")
PP41_CONTRACT_RULES = re.compile(r"(?m)^\*\*CONTRACT RULES:\*\*")
PP41_SECTION_END = re.compile(r"(?m)^#+ |^\*\*[A-Z]")
# The FIELD, not the English word. "verbatim" occurs 40+ times across the
# plugin as ordinary prose, and the rewritten MUST rule is allowed to say
# "verbatim but partial" — what it may not do is name a field that no
# longer exists. Hence the backticked-identifier form for W9 and the
# `name:` form for W4.
PP41_VERBATIM_FIELD = re.compile(r"(?<![A-Za-z0-9_])verbatim:")
PP41_PROVENANCE_FIELD = re.compile(r"(?<![A-Za-z0-9_])provenance:")
PP41_W3_START = re.compile(r"(?m)^TEARDOWN_STATUS:")
PP41_W3_END = re.compile(r"(?m)^LEAKED_RESOURCES")
PP41_ENUM_VALUE = re.compile(r'"([a-z_]+)"')
PP41_TEARDOWN_ROW = re.compile(r"(?m)^\| Teardown status \|(.+?)\|\s*$")
PP41_W2_START = re.compile(r"(?m)^# --- preflight mode only")
PP41_W2_END = re.compile(r"(?m)^# --- end preflight-only")
# Negative lookbehind, NOT the bare substring. `surface_tier:` CONTAINS
# `tier:`, so a bare-substring count reads 2 both before and after the fix
# and the check would stay red on a correct file — a control that cannot
# distinguish the defect from the fix is not a control.
PP41_TIER_FIELD = re.compile(r"(?<![A-Za-z0-9_])tier:")
PP41_SURFACE_TIER_FIELD = re.compile(r"(?<![A-Za-z0-9_])surface_tier:")
# The carve-out comment named three omitted executor fields and missed the
# fourth distinction — that preflight's surface tier is a DIFFERENT field
# from the CHECKS cost tier sharing the block with it.
PP41_CARVE_OUT_FIELDS = (
    "`siblings_swept`",
    "`branch_axis`",
    "`failure_class`",
    "`surface_tier`",
)

# ---------------------------------------------------------------- PP-42
# Each of three contested rules has exactly ONE declared owner. Three
# ownership defects, one shape: two documents each answering "who owns this?"
# with "I do", or one document citing an owner that never runs.
#
# (a) FAILURE_CLASS authority. qa-executor.md said "one authority:
#     qa-harness-builder.md" while qa-workflow.md said "Declared here, once,
#     at route level" -- two files, two answers. The count is asserted as
#     EXACTLY 1, never >= 1: the defect IS two claims, and a containment test
#     is green on two.
#
#     BASIS -- `_normative()`, window-anchored to W6
#     (`^### The failure vocabulary` -> next `^### `). NOT `### QA-specific
#     rules` (W5): measured, the authority sentence is not in W5 at all, it is
#     in the FOLLOWING section, so a property anchored at W5 could never see
#     the claim it asserts on. W6 is not inside any fence -- qa-workflow.md's
#     fences do not span it -- so `_normative()` is safe here and the window
#     is byte-identical under all three bases at this commit. The window is
#     needed because the token `failure_class` occurs on 4 lines of that file
#     case-insensitively; a whole-file test is vacuity shape (b).
#
# (b) One writer of the report shape. Dropping the harness builder's
#     "Report emitter" deliverable is only half: delete it AND the router's
#     `cp` and the route has no writer at all, and PP-19(b) -- which only
#     asserts the `cp` exists -- would stay green while the builder's
#     deliverable silently became the sole producer again. Both directions
#     asserted.
#
#     BASIS -- RAW `QA_WORKFLOW.read_text()`, as PP-19(b) does. The `cp` line
#     sits inside a ```text fence; `_normative()` deletes it and this check
#     would be red on a correct file.
#
# (c) No QA artifact cites a gate the QA route does not run, except by name.
#     See PP42C_CROSS_ROUTE_GATES for the two named exclusions and their
#     reasons, which are PRINTED on every run.
PP42_AUTHORITY_PHRASES = ("one authority", "Declared here, once")
PP42A_W6_START = re.compile(r"(?m)^### The failure vocabulary")
PP42A_W6_END = re.compile(r"(?m)^### ")
# Floor, not equality: the section is prose and will be edited. 1794 B
# measured at this commit under all three bases; a window that collapses
# below this has lost its end anchor or its body.
PP42A_W6_MIN_BYTES = 1200
PP42A_OWNER_NAME = "qa-workflow.md"
PP42A_POINTERS = ("qa-executor.md", "qa-harness-builder.md")

# PP-42(b). The `cp` is the router seeding report.md from the template; the
# harness builder must claim no row that writes that shape.
PP42B_CP_LINE = re.compile(r"cp [^\n]*qa-report\.template\.md[^\n]*report\.md")
PP42B_TABLE_START = re.compile(r"(?m)^## What you build")
PP42B_TABLE_END = re.compile(r"(?m)^### ")
PP42B_TABLE_ROW = re.compile(r"(?m)^\| \d+ \| ")
PP42B_EXPECTED_ROWS = 8
# A re-added row need not be spelled "Report emitter" to be the same defect.
PP42B_REPORT_PRODUCER = re.compile(r"report (?:shape|emitter|skeleton)", re.I)
PP42B_DISCLAIMER = "The report shape is not a deliverable here"

# PP-42(c). Backtick-agnostic on purpose: a gate named in prose is as much a
# claim as one named in code voice.
PP42C_GATE_TOKEN = re.compile(r"(?<![A-Za-z0-9_])([a-z][a-z0-9_]*_gate)\b")
PP42C_CROSS_ROUTE_GATES = {
    "phase_exit_gate":
        "qa-test-plan.template.md cites it as something the BUILD route does, in an "
        "argument for ordered waves -- not as a gate applied to this artifact. C4's "
        "defect was the opposite shape: a gate claimed to read THIS artifact's fields.",
    "plan_trust_gate":
        "qa-test-plan.template.md cites it as the BUILD-route gate that reads the SAME "
        "two fields this template requires for its own review. That sentence IS the "
        "PR-#91 rebuttal: the gate is real, it does read both fields "
        "(build-workflow.md:32-36), and the QA route never runs it. Deleting the token "
        "would delete the rebuttal; moving it into the <!-- --> note would hide it from "
        "_normative() and from anyone reading the rendered template.",
}
# Positive: an excluded token's own physical line must attribute it to another route.
PP42C_ROUTE_ATTRIBUTION = re.compile(r"\bBUILD\b")
# Negative: and must not claim the gate applies to THIS artifact.
PP42C_FIRST_PERSON = ("reads them", "requires this plan", "this plan's fields",
                      "gates this artifact")
PP42C_MIN_GATE_TOKENS = 2  # measured at this commit -- re-measure

# PP-38(f), second clause -- added in Phase 10, closing one of the two edits the
# plan left "held by no property". The PreToolUse matcher is declared a SECOND
# time, in prose, in qa-workflow.md's Rule 1 paragraph. Phase 5 found that copy
# STALE and synced it by hand; nothing then held it, so the next hooks.json
# change re-opens the same drift. It is pinned here rather than as a new
# property because PP-38(f) already holds the authoritative matcher string --
# the comparison costs one assertion and adds no check. The prose copy is not
# deleted: the paragraph states which tools the isolation rule covers at the
# point where the rule is stated, and is unreadable without them.
PP38F_PROSE_MATCHER = re.compile(r"matcher `([A-Za-z|]+)`")

# ---- PP-43. Phase 10. Pointers that name something that is not there. ----
#
# Four defect classes, one property each, all of the same shape: a reference
# whose target does not exist, is the wrong file, or does not say what the
# pointer claims.
#   (a) C1  -- the template table's `report.md` row pointed at
#              `agents/qa-executor.md`, which contains no skeleton and says the
#              OPPOSITE ("The template is the single source of the report's
#              shape"). Five of six rows pointed at `templates/`; one did not.
#   (b) A3  -- prefix consistency (ADR-5). NOT a dangling-pointer check: both
#              bare tokens on qa-harness-builder.md's manifest line RESOLVE.
#              The defect is that the line already demonstrates the
#              ${CLAUDE_PLUGIN_ROOT}/ convention on a sibling token.
#   (c) C7  -- the DRAFT header claimed two files do not exist. Both do, and
#              both are asserted by tools/harness_audit.py:46,53,669,674, so a
#              reader who acted on the header would turn that tool red.
#   (d) C5  -- "use the harness manifest and proof commands defined there"
#              promised a capability the target file does not have.

# --- PP-43(a): the template table (C1) ---
# Window-anchored: `templates/` occurs throughout SKILL.md, so a whole-file
# test is vacuity shape (b). The start anchor is asserted to match exactly once
# before slicing (shape (c)), and R9 window semantics apply -- the end anchor is
# searched from AFTER the start-anchor line, never from its own offset.
PP43A_WINDOW_START = re.compile(r"(?m)^\| Artifact \| Template \|")
PP43A_WINDOW_END = re.compile(r"(?m)^\*\*Why deletion is forbidden")
# A data row is any pipe-delimited line in the window that is neither the header
# nor the `| --- |` separator. Deliberately NOT keyed on a leading `` | ` ``:
# the `harness manifest` row's first cell is UNBACKTICKED where the other five
# are backticked, so a backtick-keyed regex finds 5 and makes a floor of 6
# permanently unreachable -- red on day one for a reason having nothing to do
# with C1. That is R9's recorded floor mistake in the other direction.
PP43A_ROW = re.compile(r"(?m)^\|([^|]+)\|([^|]+)\|\s*$")
PP43A_MIN_ROWS = 6  # measured 6 data rows at b966c52 (hdr 254, rows 256-261, end 263)
PP43A_TEMPLATE_DIR = "templates/"

# --- PP-43(b): path reachability + prefix consistency (A3 / ADR-5) ---
# Sources: the raw text of every agents/qa-*.md plus skills/qa-strategy/SKILL.md.
# RAW, as PP-29 reads raw -- fenced output shapes name real paths too.
PP43B_AGENT_GLOB = "qa-*.md"
# Identical to PP29_PATH_TOKEN: a backticked token with a `/` and a file extension.
PP43B_PATH_TOKEN = re.compile(r"`([^`\s]*/[^`\s]*\.[A-Za-z0-9]+)`")
PP43B_ROOT_PREFIX = "${CLAUDE_PLUGIN_ROOT}/"
# Applied AFTER stripping PP43B_ROOT_PREFIX -- otherwise every prefixed token is
# excluded as "templated", because ${...} matches the templated regex. PP-29
# never hit this because no ${CLAUDE_PLUGIN_ROOT} token is in its frozen scope.
PP43B_EXCLUDE = (re.compile(r"\{[^}]*\}"), re.compile(r"\*"))
PP43B_MIN_EXTRACTED = 16  # measured 20 at b966c52 -- re-measured, unchanged from c3ea86f
PP43B_MIN_RESOLVED = 8  # measured 11 at b966c52 -- re-measured, unchanged from c3ea86f
# Declared-future files under an explicit **PLACEHOLDER** banner. NAMED, not
# line-ranged: `tools/live_harness_runner.py` shares the fourth bullet's line and
# DOES exist, so a line-range drop would swallow a live token. A declared
# placeholder is not a broken link; an UNdeclared one is. The exclusion is a
# loan against the banner and dies with it -- see the three assertions in the
# check body.
PP43B_PLACEHOLDER_EXCLUSIONS = {
    "references/environment-topologies.md",
    "references/observability-assertions.md",
    "references/ui-qa-automation.md",
    "references/harness-manifest.md",
}
PP43B_PLACEHOLDER_BANNER = "**PLACEHOLDER**"
# Anti-vacuity for the prefix clause: the clause fires only on lines that
# already carry a prefixed token, so zero such lines makes it inert.
PP43B_MIN_PREFIXED_LINES = 4  # measured 8 at b966c52

# --- PP-43(c): no document claims a file does not exist when it does (C7) ---
PP43C_ABSENCE_PHRASES = (
    "which do not exist",
    "that do not exist",
    "do not exist",
    "does not exist",
)
# Sentence split: a terminator followed by whitespace and an opening character.
# `.md` inside a token is immune because no whitespace follows its period.
PP43C_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z*`#(])")
# Backticked token with a file extension. Unlike PP43B_PATH_TOKEN this does NOT
# require a `/`: C7's two false claims are BARE BASENAMES, which is exactly why
# a plugin-root-relative existence test read them as missing and stayed green.
PP43C_TOKEN = re.compile(r"`([^`\s]+\.[A-Za-z0-9]+)`")
# A pinned positive fixture the property runs on EVERY invocation, independent of
# corpus state. After Phase 10's own fix the real corpus matches the phrase list
# ZERO times, forever -- so without this fixture PP-43(c) is a green whose only
# evidence it ever worked is one-shot (I-95) and gone the moment I-95 stops being
# re-run. If the extractor silently stops working this goes red on the next run
# rather than at the next review.
PP43C_SELF_TEST = (
    "This skill fills the two paths `skills/building/references/"
    "integration-and-live-proof.md` already points at but that do not exist "
    "(`live-verification-strategy.md`, `live-production-testing.md`)."
)
PP43C_SELF_TEST_EXPECTED = {"live-verification-strategy.md", "live-production-testing.md"}
PP43C_MIN_FILES_SCANNED = 4  # measured 4 at b966c52

# --- PP-43(d): a pointer does not promise a capability its target lacks (C5) ---
# The edited file lies outside PP-43(b)'s declared scope, so C5 gets its own
# cheap property rather than no property at all.
PP43D_CLAUSE = re.compile(r"(?m)^- use the (.+) defined there\s*$")


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


def run_guard_raw(
    project_dir: Path, payload: dict, tool_payload: dict
) -> subprocess.CompletedProcess:
    """Write ONE artifact, invoke the guard, return the CompletedProcess.

    One artifact at a time is load-bearing: cc10x_hooklib.latest_workflow_file()
    sorts .cc10x/workflows/*.json by mtime and returns only the newest, so
    several artifacts in one directory would all resolve to the same file and
    every case but the last would assert against the wrong one.

    Returns rc and stderr as well as the decision, because a CRASHING guard
    emits no decision on stdout and therefore reads as ALLOW. A property that
    asserts only the decision cannot tell a deliberate allow from a traceback
    -- which is the exact defect PP-34 exists to catch. `tool_payload` is a
    parameter rather than a constant so a property can probe a tool other than
    the Bash mkdir probe PP-6 uses.
    """
    wf_dir = project_dir / ".cc10x" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    wf_file = wf_dir / "wf-test-pp6.json"
    wf_file.write_text(json.dumps(payload))
    try:
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project_dir))
        return subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps(tool_payload),
            capture_output=True,
            text=True,
            env=env,
        )
    finally:
        wf_file.unlink(missing_ok=True)


def run_guard(project_dir: Path, payload: dict) -> bool:
    """Write ONE artifact, invoke the guard, return True if it denied.

    Thin wrapper over run_guard_raw preserving PP-6's exact probe. PP-6's four
    detail strings are byte-identical across this refactor.
    """
    result = run_guard_raw(
        project_dir,
        payload,
        {"tool_name": "Bash", "tool_input": {"command": f"mkdir -p {PROBE_TARGET}"}},
    )
    return '"permissionDecision": "deny"' in result.stdout


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
    # `re-` prefixed too: `re-qa-build` / `re-qa-execute` are QA phases that do
    # not START with "qa", and a filter keyed on the "qa" prefix alone never
    # checked them -- deleting `re-qa-execute` from its §7 row left PP-5 green
    # (mutation M3, recorded in the PR-#91 review). The route-wide re- phases
    # (`re-review`, `re-hunt`, ...) do not carry the "re-qa" infix and stay out.
    qa_enum = (
        {p for p in enum if p.startswith("qa") or p.startswith("re-qa")}
        - NON_DISPATCHABLE
    )
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

    skill_lines = SKILL_MD.read_text(encoding="utf-8").splitlines()
    for enum_label, enum_anchor in PP21_SKILL_ENUM_LINES:
        hits = [line for line in skill_lines if enum_anchor in line]
        if len(hits) != 1:
            pp21c_gaps.append(
                f"PRECONDITION: expected exactly 1 `{enum_anchor}` line in "
                f"{SKILL_MD.name} ({enum_label}), found {len(hits)}"
            )
            continue
        enums = PP21_PHASE_ENUM.findall(hits[0])
        if len(enums) != 1:
            pp21c_gaps.append(
                f"PRECONDITION: expected exactly 1 pipe-separated enum on "
                f"{SKILL_MD.name}'s {enum_label} line, found {len(enums)}"
            )
        elif "qa" not in enums[0].split("|"):
            pp21c_gaps.append(
                f"`qa` is missing from the {enum_label} phase enum in "
                f"{SKILL_MD.name} (members: {enums[0]})"
            )

    check(
        "PP-21(c)",
        not pp21c_gaps,
        "QA is a member of the `workflow_type` enum line, the `evidence` list and "
        f"all {len(PP21_SKILL_ENUM_LINES)} anchored {SKILL_MD.name} phase-enum lines"
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

    # PP-25(a) -- every re-dispatch loop in the QA law states a numeric cap AND
    # its exhaustion behaviour, asserted INSIDE that loop's own window. See
    # PP25_LOOPS for why the windows are bold-lead-in-anchored (neither loop
    # sits under a heading) and why a whole-file test would let one loop satisfy
    # the other.
    pp25_windows: dict[str, str] = {}
    pp25_caps: dict[str, list[str]] = {}
    pp25a_precondition: list[str] = []
    pp25a_gaps: list[str] = []
    for label, start_re, end_re, exhaustion in PP25_LOOPS:
        starts = list(start_re.finditer(qa_norm))
        ends = list(end_re.finditer(qa_norm))
        if len(starts) != 1 or len(ends) != 1 or not starts[0].end() < ends[0].start():
            pp25a_precondition.append(
                f"could not bracket the {label} loop in {QA_WORKFLOW.name}: "
                f"{len(starts)} opening and {len(ends)} closing bold lead-ins "
                f"(expected exactly 1 of each, in that order) — the anchor has "
                f"stopped matching, so any result over the window would be vacuous"
            )
            continue
        win = qa_norm[starts[0].end() : ends[0].start()]
        pp25_windows[label] = win
        caps = PP25_CAP.findall(win)
        pp25_caps[label] = caps
        if len(caps) != 1:
            pp25a_gaps.append(
                f"the {label} loop states {len(caps)} numeric caps "
                f"({caps or 'none'}), expected exactly 1 (window={len(win)}B)"
            )
        missing = [tok for tok in exhaustion if tok not in win]
        if missing:
            pp25a_gaps.append(
                f"the {label} loop does not state its exhaustion behaviour: "
                f"missing {missing} (window={len(win)}B)"
            )

    if pp25a_precondition:
        pp25a_ok = False
        pp25a_detail = "PRECONDITION failed: " + "; ".join(pp25a_precondition)
    else:
        pp25a_ok = not pp25a_gaps
        pp25a_detail = (
            "both re-dispatch loops state a numeric cap and a named exhaustion "
            "state, each inside its own window ("
            + "; ".join(
                f"{label}: cap={pp25_caps[label] or 'none'} "
                f"window={len(pp25_windows[label])}B"
                for label, *_ in PP25_LOOPS
                if label in pp25_windows
            )
            + ")"
            + ("" if pp25a_ok else " — " + "; ".join(pp25a_gaps))
        )
    check("PP-25(a)", pp25a_ok, pp25a_detail)

    # PP-25(b) -- the `kind:remfix` block appends `remediation_history`, in the
    # shape the circuit-breaker mandate specifies. See PP25_REMHIST_TOKENS for
    # why this asserts the APPEND DUTY IN THE LAW rather than the array's type:
    # the type assertion is green at HEAD and green against the defect.
    PP25B_WINDOW = "re-qa-build extra rounds"
    rebuild_win = pp25_windows.get(PP25B_WINDOW)
    if rebuild_win is None:
        pp25b_ok = False
        pp25b_detail = (
            f"PRECONDITION failed: the {PP25B_WINDOW} window was not located "
            f"(see PP-25(a)); the append duty is therefore unscoped"
        )
    else:
        pp25b_missing = [tok for tok in PP25_REMHIST_TOKENS if tok not in rebuild_win]
        pp25b_ok = not pp25b_missing
        pp25b_detail = (
            f"the `kind:remfix` block mandates the `remediation_history` append "
            f"in the shape the hook-enforced breaker counts "
            f"(window={len(rebuild_win)}B, "
            f"{len(PP25_REMHIST_TOKENS) - len(pp25b_missing)}/"
            f"{len(PP25_REMHIST_TOKENS)} tokens)"
            + ("" if pp25b_ok else f" — missing {pp25b_missing}")
        )
    check("PP-25(b)", pp25b_ok, pp25b_detail)

    # PP-26(a) -- the QA remediation block names its consequence, and the sink
    # admits QA. See PP26A_START for why the block is window-anchored and why
    # SF-8's hook-policy half is part of the same check id.
    p26s = list(PP26A_START.finditer(qa_norm))
    p26e = list(PP26A_END.finditer(qa_norm))
    pp26a_parts: list[str] = []
    pp26a_gaps: list[str] = []
    pp26a_precondition: list[str] = []
    if len(p26s) != 1 or len(p26e) != 1 or not p26s[0].end() < p26e[0].start():
        pp26a_precondition.append(
            f"could not bracket the QA remediation block in {QA_WORKFLOW.name}: "
            f"{len(p26s)} opening bold lead-ins and {len(p26e)} closing "
            f"`#### Execute` headings (expected exactly 1 of each, in that "
            f"order) — the anchor has stopped matching, so any result over the "
            f"window would be vacuous"
        )
        pp26a_window = ""
    else:
        pp26a_window = qa_norm[p26s[0].end() : p26e[0].start()]
        missing = [t for t in PP26A_TOKENS if t not in pp26a_window]
        pp26a_parts.append(f"{QA_WORKFLOW.name} block window={len(pp26a_window)}B")
        if missing:
            pp26a_gaps.append(
                f"{QA_WORKFLOW.name}: the QA remediation block does not name "
                f"{missing} (window={len(pp26a_window)}B)"
            )
    policy_text = HOOK_POLICY.read_text(encoding="utf-8")
    sink = list(PP26A_SINK_BULLET.finditer(policy_text))
    if len(sink) != 1:
        pp26a_precondition.append(
            f"the `deferred_findings` schema bullet matched {len(sink)} times in "
            f"{HOOK_POLICY.name}, expected exactly 1 (whole-file occurrences of "
            f"the token: {policy_text.count('deferred_findings')})"
        )
    else:
        bullet = sink[0].group(0)
        pp26a_parts.append(f"{HOOK_POLICY.name} sink bullet={len(bullet)}B")
        miss_sink = [t for t in PP26A_SINK_TOKENS if t not in bullet]
        if miss_sink:
            pp26a_gaps.append(
                f"{HOOK_POLICY.name}: the `deferred_findings` schema bullet does "
                f"not name QA's surfacing point — missing {miss_sink} "
                f"(bullet={len(bullet)}B); as written the array's only "
                f"documented reader is a BUILD-DONE triage this route does not run"
            )
    if pp26a_precondition:
        pp26a_ok = False
        pp26a_detail = "PRECONDITION failed: " + "; ".join(pp26a_precondition)
    else:
        pp26a_ok = not pp26a_gaps
        pp26a_detail = (
            "the QA remediation block names the triggering verdicts, the halted "
            "phase, `re-qa-build`, the origin value and the `deferred_findings` "
            "sink, and the sink's schema entry names QA's surfacing point ("
            + "; ".join(pp26a_parts) + ")"
            + ("" if pp26a_ok else " — " + "; ".join(pp26a_gaps))
        )
    check("PP-26(a)", pp26a_ok, pp26a_detail)

    # PP-26(b) -- the carve-out names its parent AND the parent names the
    # carve-out. Two separately-named halves; see PP26B_QA_TOKENS for why one
    # direction is not enough and which control measures each.
    pp26b_parts: list[str] = []
    pp26b_gaps: list[str] = []
    pp26b_precondition: list[str] = []
    if not pp26a_window:
        pp26b_precondition.append(
            f"the QA remediation block window was not located in "
            f"{QA_WORKFLOW.name} (see PP-26(a)); the citation half is therefore "
            f"unscoped"
        )
    else:
        pp26b_parts.append(f"{QA_WORKFLOW.name} block window={len(pp26a_window)}B")
        miss_qa = [t for t in PP26B_QA_TOKENS if t not in pp26a_window]
        if miss_qa:
            pp26b_gaps.append(
                f"direction 1 ({QA_WORKFLOW.name} -> kernel): the QA carve-out "
                f"does not cite what it carves out of — missing {miss_qa} "
                f"(window={len(pp26a_window)}B)"
            )
    skill_full = SKILL_MD.read_text(encoding="utf-8")
    s11 = list(PP26B_SKILL_START.finditer(skill_full))
    if len(s11) != 1:
        pp26b_precondition.append(
            f"the `## 11. Re-Review Loop` heading matched {len(s11)} times in "
            f"{SKILL_MD.name}, expected exactly 1 — the anchor has stopped "
            f"matching, so any result over the section would be vacuous"
        )
    else:
        nxt = PP26B_SKILL_END.search(skill_full, s11[0].end())
        s11_win = skill_full[s11[0].end() : nxt.start() if nxt else len(skill_full)]
        pp26b_parts.append(f"{SKILL_MD.name} §11 section={len(s11_win)}B")
        miss_skill = [t for t in PP26B_SKILL_TOKENS if t not in s11_win]
        if miss_skill:
            pp26b_gaps.append(
                f"direction 2 ({SKILL_MD.name} §11 -> QA): the kernel line a "
                f"router executes on a completed `kind:remfix` carries no QA "
                f"exception — missing {miss_skill} (section={len(s11_win)}B); "
                f"unqualified, it re-reviews a `re-qa-build` through a "
                f"precondition gate `qa-harness-builder` cannot satisfy"
            )
    if pp26b_precondition:
        pp26b_ok = False
        pp26b_detail = "PRECONDITION failed: " + "; ".join(pp26b_precondition)
    else:
        pp26b_ok = not pp26b_gaps
        pp26b_detail = (
            "the QA carve-out cites the shared rules by section and those rules' "
            "execution point carries the reciprocal QA exception ("
            + "; ".join(pp26b_parts) + ")"
            + ("" if pp26b_ok else " — " + "; ".join(pp26b_gaps))
        )
    check("PP-26(b)", pp26b_ok, pp26b_detail)


    # PP-27(a) -- the no-product-code rule is exhaustive IN FACT, at all three
    # sites, and the two plan-phase dispatches carry the boundary. Per-site,
    # per-file. See PP27A_SITES for why the anchoring and the per-site naming
    # are load-bearing.
    pp27a_texts = {
        "SKILL.md": _decommented(SKILL_MD.read_text(encoding="utf-8")),
        "qa-workflow.md": dag_text,
    }
    pp27a_precondition: list[str] = []
    pp27a_gaps: list[str] = []
    pp27a_sizes: list[str] = []
    for fname, label, pattern in PP27A_SITES:
        text = pp27a_texts[fname]
        hits = list(re.finditer(pattern, text, re.M))
        if len(hits) != 1:
            pp27a_precondition.append(
                f"{fname} ({label}): the bullet anchor matched {len(hits)} times, "
                f"expected exactly 1 — any result over the window would be vacuous"
            )
            continue
        start = hits[0].start()
        lines = text[start:].splitlines()
        bullet = [lines[0]]
        for line in lines[1:]:
            if line.startswith("  ") and line.strip():
                bullet.append(line)
            else:
                break
        window = "\n".join(bullet)
        pp27a_sizes.append(f"{fname} ({label}) bullet={len(window)}B")
        missing = [a for a in PP27A_AGENTS if a not in window]
        if missing:
            pp27a_gaps.append(
                f"{fname} ({label}) enumerates {len(PP27A_AGENTS) - len(missing)}/"
                f"{len(PP27A_AGENTS)} agents holding write tools in QA: missing "
                f"{missing} (bullet={len(window)}B)"
            )
        if label == PP27A_ENFORCEMENT_SITE:
            miss_e = [t for t in PP27A_ENFORCEMENT_TOKENS if t not in window]
            if miss_e:
                pp27a_gaps.append(
                    f"{fname} ({label}) does not say which half is the guard and "
                    f"which is the notice: missing {miss_e} (bullet={len(window)}B)"
                )
    for phase_token, task_var in PP27A_DISPATCHES:
        wf = pp27a_texts["qa-workflow.md"]
        ends = list(re.finditer(rf"(?m)^\}}\) -> {re.escape(task_var)}$", wf))
        if len(ends) != 1:
            pp27a_precondition.append(
                f"qa-workflow.md ({phase_token} dispatch): the terminator "
                f"`}}) -> {task_var}` matched {len(ends)} times, expected exactly 1"
            )
            continue
        open_at = wf.rfind("TaskCreate({", 0, ends[0].start())
        if open_at == -1:
            pp27a_precondition.append(
                f"qa-workflow.md ({phase_token} dispatch): no opening "
                f"`TaskCreate({{` precedes the terminator"
            )
            continue
        window = wf[open_at : ends[0].end()]
        pp27a_sizes.append(f"qa-workflow.md ({phase_token} dispatch)={len(window)}B")
        if PP27A_DISPATCH_TOKEN not in window:
            pp27a_gaps.append(
                f"qa-workflow.md ({phase_token} dispatch) does not state the "
                f"product-code boundary: missing '{PP27A_DISPATCH_TOKEN}' "
                f"(window={len(window)}B)"
            )
    if pp27a_precondition:
        pp27a_ok = False
        pp27a_detail = "PRECONDITION failed: " + "; ".join(pp27a_precondition)
    else:
        pp27a_ok = not pp27a_gaps
        pp27a_detail = (
            "all three statements of the no-product-code rule name every agent "
            "that holds write tools in QA, and both plan-phase dispatches carry "
            "the boundary (" + "; ".join(pp27a_sizes) + ")"
            + ("" if pp27a_ok else " — " + "; ".join(pp27a_gaps))
        )
    check("PP-27(a)", pp27a_ok, pp27a_detail)

    # PP-27(b) -- `phase_exit_gate` names QA where it is INVOKED. Anchored on
    # the per-agent loop's invocation line; see PP27B_INVOCATION for why a
    # whole-file search is green against the injection this exists to catch.
    skill_text = pp27a_texts["SKILL.md"]
    inv = list(PP27B_INVOCATION.finditer(skill_text))
    if len(inv) != 1:
        pp27b_ok = False
        pp27b_detail = (
            f"PRECONDITION failed: the per-agent loop's `phase_exit_gate` "
            f"invocation line matched {len(inv)} times in {SKILL_MD.name}, "
            f"expected exactly 1 — the anchor has stopped matching, so any "
            f"result over it would be vacuous (whole-file occurrences of the "
            f"token: {skill_text.count('phase_exit_gate')})"
        )
    else:
        routes = inv[0].group(1)
        pp27b_missing = [r for r in PP27B_ROUTES if r not in routes]
        pp27b_ok = not pp27b_missing
        pp27b_detail = (
            f"the per-agent loop runs `phase_exit_gate` for {routes} "
            f"(line={len(inv[0].group(0))}B, whole-file occurrences of the "
            f"token: {skill_text.count('phase_exit_gate')})"
            + ("" if pp27b_ok else f" — missing {pp27b_missing}")
        )
    check("PP-27(b)", pp27b_ok, pp27b_detail)

    # PP-28 -- preflight bug candidates reach the sink the DEBUG offer reads.
    # See PP28_START for why both keys are asserted verbatim and why this
    # window's printed size is a measurement rather than a control.
    p28s = list(PP28_START.finditer(qa_norm))
    p28e = list(PP28_END.finditer(qa_norm))
    if len(p28s) != 1 or len(p28e) != 1 or not p28s[0].end() < p28e[0].start():
        pp28_ok = False
        pp28_detail = (
            f"PRECONDITION failed: could not bracket the *Persist first* section "
            f"in {QA_WORKFLOW.name}: {len(p28s)} opening and {len(p28e)} closing "
            f"headings (expected exactly 1 of each, in that order)"
        )
    else:
        win = qa_norm[p28s[0].end() : p28e[0].start()]
        pp28_missing = [
            t for t in (*PP28_TOKENS, PP28_PREFLIGHT_RETURN) if t not in win
        ]
        pp28_ok = not pp28_missing
        pp28_detail = (
            f"the *Persist first* block merges preflight's `BUG_CANDIDATES` from "
            f"`qa.preflight` into `qa.bug_candidates` on preflight return "
            f"(window={len(win)}B)"
            + ("" if pp28_ok else f" — missing {pp28_missing}")
        )
    check("PP-28", pp28_ok, pp28_detail)

    # PP-29 -- every filesystem path the QA law NAMES resolves on disk. See
    # PP29_PATH_TOKEN for the frozen scope ("SKILL.md's QA lines" is a regex,
    # not prose), the FOUR resolution bases, and why the exclusion set covers
    # glob-bearing tokens as well as templated ones.
    repo_root = PLUGIN.parent.parent
    pp29_sources = {
        QA_WORKFLOW: QA_WORKFLOW.read_text(encoding="utf-8"),
        SKILL_MD: "\n".join(
            ln
            for ln in SKILL_MD.read_text(encoding="utf-8").splitlines()
            if PP29_SKILL_QA_LINE.search(ln)
        ),
    }
    # token -> the file that NAMES it; the naming file's own directory is one of
    # the four bases, so the provenance has to survive extraction.
    pp29_extracted: dict[str, Path] = {}
    for _src, _text in pp29_sources.items():
        for _tok in PP29_PATH_TOKEN.findall(_text):
            pp29_extracted.setdefault(_tok, _src)
    pp29_excluded = sorted(
        t for t in pp29_extracted if any(x.search(t) for x in PP29_EXCLUDE)
    )
    pp29_resolvable = {
        t: s for t, s in pp29_extracted.items() if t not in pp29_excluded
    }
    if len(pp29_extracted) < PP29_MIN_EXTRACTED:
        pp29_ok = False
        pp29_detail = (
            f"PRECONDITION failed: extracted only {len(pp29_extracted)} "
            f"path-shaped tokens from {QA_WORKFLOW.name} + {SKILL_MD.name}'s QA "
            f"lines (expected >= {PP29_MIN_EXTRACTED}) — the token regex or the "
            f"QA-line filter has stopped matching, so any existence result "
            f"below would be vacuous"
        )
    elif len(pp29_resolvable) < PP29_MIN_RESOLVED:
        pp29_ok = False
        pp29_detail = (
            f"PRECONDITION failed: only {len(pp29_resolvable)} of "
            f"{len(pp29_extracted)} extracted tokens survive the exclusion set "
            f"(expected >= {PP29_MIN_RESOLVED}) — the exclusions have widened "
            f"until nothing is left to resolve; excluded: {pp29_excluded}"
        )
    else:
        pp29_dangling = []
        for _tok, _src in sorted(pp29_resolvable.items()):
            _bases = (repo_root, PLUGIN, _src.parent)
            if not any((b / _tok).exists() for b in _bases):
                pp29_dangling.append(
                    f"`{_tok}` (named in {_src.name}; resolves under none of "
                    f"repo root, {PLUGIN.name}/, or {_src.parent.name}/)"
                )
        pp29_ok = not pp29_dangling
        pp29_detail = (
            f"{len(pp29_extracted)} path-shaped tokens named by the QA law, "
            f"{len(pp29_excluded)} excluded as templated or glob-bearing "
            f"({pp29_excluded}), {len(pp29_resolvable) - len(pp29_dangling)}/"
            f"{len(pp29_resolvable)} of the rest resolve on disk"
            + ("" if pp29_ok else " — dangling: " + "; ".join(pp29_dangling))
        )
    check("PP-29", pp29_ok, pp29_detail)

    # PP-30(a) -- QA offers no workspace isolation, AND SAYS WHY. Both halves.
    # See PP30A_FORBIDDEN for why the negative half reads the de-commented text
    # (fences included) while the positive half reads _normative(), and why the
    # forbidden vocabulary is the OFFER's rather than the word "worktree".
    pp30a_faults: list[str] = []
    pp30a_hits: list[str] = []
    for _pat in PP30A_FORBIDDEN:
        for _m in _pat.finditer(dag_text):
            _ln = dag_text.count("\n", 0, _m.start()) + 1
            pp30a_hits.append(f"`{_m.group(0)}` at {QA_WORKFLOW.name}:~{_ln}")
    if pp30a_hits:
        pp30a_faults.append(
            "the workspace-isolation offer is back in "
            f"{QA_WORKFLOW.name}: " + "; ".join(pp30a_hits)
        )
    _rat = list(PP30A_RATIONALE.finditer(qa_norm))
    if len(_rat) != 1:
        rat_window = ""
        pp30a_faults.append(
            f"the ADR-2 rationale block is not present exactly once in the "
            f"NORMATIVE text of {QA_WORKFLOW.name} ({len(_rat)} matches) — the "
            f"offer may well be absent, but the absence is then UNARGUED, which "
            f"is the silent-deletion outcome this half exists to forbid"
        )
    else:
        _end = qa_norm.find("\n\n", _rat[0].end())
        rat_window = qa_norm[_rat[0].start() : _end if _end != -1 else len(qa_norm)]
        _miss = [t for t in PP30A_TOKENS if t not in rat_window]
        if _miss:
            pp30a_faults.append(
                f"the ADR-2 rationale block is present but does not argue the "
                f"absence: missing {_miss} (block={len(rat_window)}B)"
            )
    pp30a_ok = not pp30a_faults
    pp30a_detail = (
        f"{QA_WORKFLOW.name} offers no workspace isolation "
        f"(0/{len(PP30A_FORBIDDEN)} forbidden offer patterns) and argues the "
        f"absence in place (block={len(rat_window)}B)"
        + ("" if pp30a_ok else " — " + "; ".join(pp30a_faults))
    )
    check("PP-30(a)", pp30a_ok, pp30a_detail)

    # PP-30(b) -- both harness-review dispatches NAME their review surface.
    # Window-anchored PER DISPATCH: both blocks share one ```text fence, so a
    # fence-wide test lets `qa-review` satisfy `qa-hunt`'s half. Scope is the
    # dispatch text only; that the fields are REQUIRED is PP-23(b)'s assertion.
    pp30b_precondition: list[str] = []
    pp30b_gaps: list[str] = []
    pp30b_sizes: list[str] = []
    for _label, _task_var in PP30B_DISPATCHES:
        _ends = list(re.finditer(rf"(?m)^\}}\) -> {re.escape(_task_var)}$", dag_text))
        if len(_ends) != 1:
            pp30b_precondition.append(
                f"{QA_WORKFLOW.name} ({_label} dispatch): the terminator "
                f"`}}) -> {_task_var}` matched {len(_ends)} times, expected "
                f"exactly 1 — any result over the window would be vacuous"
            )
            continue
        _open = dag_text.rfind("TaskCreate({", 0, _ends[0].start())
        if _open == -1:
            pp30b_precondition.append(
                f"{QA_WORKFLOW.name} ({_label} dispatch): no opening "
                f"`TaskCreate({{` precedes the terminator"
            )
            continue
        _win = dag_text[_open : _ends[0].end()]
        pp30b_sizes.append(f"{_label}={len(_win)}B")
        _miss = [t for t in PP30B_TOKENS if t not in _win]
        if _miss:
            pp30b_gaps.append(
                f"the `{_label}` dispatch does not name the review surface the "
                f"harness builder's contract guarantees: missing {_miss} "
                f"(window={len(_win)}B)"
            )
    if pp30b_precondition:
        pp30b_ok = False
        pp30b_detail = "PRECONDITION failed: " + "; ".join(pp30b_precondition)
    else:
        pp30b_ok = not pp30b_gaps
        pp30b_detail = (
            "both harness-review dispatches name `ARTIFACTS_CREATED` and "
            "`HARNESS_MANIFEST` as the surface to inspect ("
            + "; ".join(pp30b_sizes)
            + ")"
            + ("" if pp30b_ok else " — " + "; ".join(pp30b_gaps))
        )
    check("PP-30(b)", pp30b_ok, pp30b_detail)

    # PP-31 -- the QA phase-token spellings are frozen, and the freeze cites its
    # reason. See PP31_QA_TOKENS for what this property is and is NOT, and for
    # why editing that constant is the whole cost of a rename rather than a
    # formality.
    pp31_faults: list[str] = []
    pp31_enum_line = SKILL_MD.read_text(encoding="utf-8")
    pp31_hits = list(PP31_ENUM_LINE.finditer(pp31_enum_line))
    pp31_found: set[str] = set()
    if len(pp31_hits) != 1:
        pp31_faults.append(
            f"PRECONDITION failed: the SKILL.md §3 `phase:{{...}}` enum line "
            f"matched {len(pp31_hits)} times, expected exactly 1 — the anchor "
            f"has stopped matching, so the extracted QA slice would be empty "
            f"and any comparison over it red for the wrong reason"
        )
    else:
        members = [m.strip() for m in pp31_hits[0].group(1).split("|")]
        if len(members) < PP31_MIN_ENUM_MEMBERS:
            pp31_faults.append(
                f"PRECONDITION failed: the §3 enum parsed only {len(members)} "
                f"members (expected >= {PP31_MIN_ENUM_MEMBERS}) — the line is no "
                f"longer an enum"
            )
        else:
            pp31_found = {m for m in members if "qa" in m.split("-")}
            _added = sorted(pp31_found - PP31_QA_TOKENS)
            _lost = sorted(PP31_QA_TOKENS - pp31_found)
            if _added or _lost:
                pp31_faults.append(
                    f"the QA phase-token spellings have DRIFTED from the frozen "
                    f"set: unexpected {_added or 'none'}, missing "
                    f"{_lost or 'none'} — if this is a deliberate rename, read "
                    f"ADR-1 in the constant's comment first: editing "
                    f"PP31_QA_TOKENS is the whole cost of the rename, and the "
                    f"rename must also reach "
                    f"cc10x_qa_isolation_guard.PLAN_PHASES (which turns PP-2 "
                    f"red) and every in-flight `phase:` token"
                )
    _p31r = list(PP31_RATIONALE.finditer(qa_norm))
    pp31_rat_window = ""
    if len(_p31r) != 1:
        pp31_faults.append(
            f"the ADR-1 naming-rationale block is not present exactly once in "
            f"the NORMATIVE text of {QA_WORKFLOW.name} ({len(_p31r)} matches) — "
            f"the frozen set and the argument that justifies it must not drift "
            f"apart, or the freeze is a rule with no reason attached"
        )
    else:
        _end = qa_norm.find("\n\n", _p31r[0].end())
        pp31_rat_window = qa_norm[
            _p31r[0].start() : _end if _end != -1 else len(qa_norm)
        ]
        _miss = [t for t in PP31_RATIONALE_TOKENS if t not in pp31_rat_window]
        if _miss:
            pp31_faults.append(
                f"the ADR-1 rationale block is present but does not carry the "
                f"argument: missing {_miss} (block={len(pp31_rat_window)}B)"
            )
    pp31_ok = not pp31_faults
    check(
        "PP-31",
        pp31_ok,
        f"the {len(pp31_found)} QA phase tokens in the SKILL.md §3 enum match "
        f"the frozen set, and the ADR-1 rationale is anchored in "
        f"{QA_WORKFLOW.name} (block={len(pp31_rat_window)}B)"
        + ("" if pp31_ok else " — " + "; ".join(pp31_faults)),
    )

    # PP-32 -- every deliberate omission in the QA law carries its rationale in
    # the same block. Three omissions, window-anchored per omission; the fourth
    # (no workspace isolation) is PP-30(a)'s positive half and is deliberately
    # NOT re-asserted here. See PP32_OMISSIONS.
    pp32_faults: list[str] = []
    pp32_sizes: list[str] = []
    for _label, _start_re, _end_re, _tokens in PP32_OMISSIONS:
        _s = list(_start_re.finditer(qa_norm))
        _e = list(_end_re.finditer(qa_norm))
        if len(_s) != 1 or len(_e) != 1 or not _s[0].end() < _e[0].start():
            pp32_faults.append(
                f"PRECONDITION failed for `{_label}`: {len(_s)} opening and "
                f"{len(_e)} closing anchors in {QA_WORKFLOW.name} (expected "
                f"exactly 1 of each, in that order) — any result over this "
                f"window would be vacuous"
            )
            continue
        _win = qa_norm[_s[0].start() : _e[0].start()]
        pp32_sizes.append(f"{_label}={len(_win)}B")
        _miss = [t for t in _tokens if t not in _win]
        if _miss:
            pp32_faults.append(
                f"the `{_label}` omission is made but NOT argued in place: "
                f"missing {_miss} (window={len(_win)}B)"
            )
    pp32_ok = not pp32_faults
    check(
        "PP-32",
        pp32_ok,
        f"all {len(PP32_OMISSIONS)} deliberate omissions in the QA law argue "
        f"themselves in place (" + "; ".join(pp32_sizes) + ")"
        + ("" if pp32_ok else " — " + "; ".join(pp32_faults)),
    )

    check(
        "PP-19(b)",
        not pp19b_missing,
        f"the law COPIES `{PP19_TPL.name}` into place and the agent NAMES it"
        + ("" if not pp19b_missing else " — " + "; ".join(pp19b_missing)),
    )

    # PP-33 -- QA is a member of every workflow-type enumeration, and the
    # per-site extractors still find enums. Four sites, four shapes, four
    # normalisers; see PP33_SITES for the fence measurement that forced S2's.
    _pp33_basis = {"normative": _normative, "decommented": _decommented}
    pp33_pre: list[str] = []
    pp33_bad: list[str] = []
    pp33_report: list[str] = []
    pp33_members: dict[str, list[str]] = {}
    pp33_counts: dict[str, int] = {}

    if len(PP33_SITES) != 4:
        pp33_pre.append(
            f"PRECONDITION failed: PP33_SITES has {len(PP33_SITES)} entries, "
            f"expected 4 -- one per syntactic shape"
        )

    for _sid, _disp, _spath, _sbasis, _anchor, _extract, _split, _count, _label in (
        PP33_SITES
    ):
        _raw = _spath.read_text(encoding="utf-8")
        _hits = _anchor.findall(_pp33_basis[_sbasis](_raw))
        if len(_hits) != 1:
            pp33_pre.append(
                f"PRECONDITION failed for {_sid} {_disp}: its anchor matched "
                f"{len(_hits)} lines under `_{_sbasis}()` (expected exactly 1) "
                f"-- any membership result over this site would be vacuous"
            )
            pp33_bad.append(f"{_sid} {_disp} was never parsed (see PP-33(a))")
            continue
        _line = _hits[0]
        _no = _pp33_raw_lineno(_raw, _line)
        _got = _extract.findall(_line)
        if not _got:
            pp33_pre.append(
                f"PRECONDITION failed for {_sid} {_disp}:{_no}: the {_label} "
                f"extractor matched NOTHING on its own anchor line -- an empty "
                f"member list makes `'QA' in members` False for the wrong reason"
            )
            pp33_bad.append(f"{_sid} {_disp} was never parsed (see PP-33(a))")
            continue
        if _split is None:
            pp33_counts[_sid] = int(_got[0])
            pp33_report.append(f"{_sid} {_disp}:{_no} count={_got[0]}")
            continue
        _members = [_m.strip() for _m in _got[0].split(_split)]
        pp33_members[_sid] = _members
        pp33_report.append(f"{_sid} {_disp}:{_no} {_members}")
        if _count is not None:
            _cm = _count.findall(_line)
            if not _cm:
                pp33_pre.append(
                    f"PRECONDITION failed for {_sid} {_disp}:{_no}: the site "
                    f"declares a cardinality but the count regex matched nothing"
                )
                continue
            pp33_counts[_sid] = int(_cm[0])

    # The source of truth S4 is measured against, with its own floor.
    pp33_routes = sorted(set(PP33_ROUTING_ROW.findall(_normative(SKILL_MD.read_text(
        encoding="utf-8")))))
    if len(pp33_routes) < PP33_MIN_ROUTES:
        pp33_pre.append(
            f"PRECONDITION failed: the SKILL.md section 1 Intent Routing table "
            f"yielded {len(pp33_routes)} distinct workflows (expected >= "
            f"{PP33_MIN_ROUTES}) -- the row regex has stopped matching, so S4's "
            f"count comparison below is vacuous"
        )

    # The stamping line's shape, proved live on the two siblings that carry it.
    pp33_stamp_report: list[str] = []
    for _fname, _expect in PP33_STAMP_SIBLINGS:
        _sm = PP33_STAMP.findall(_normative((REFERENCES / _fname).read_text(
            encoding="utf-8")))
        if _sm != [_expect]:
            pp33_pre.append(
                f"PRECONDITION failed: the stamping regex matched {_sm} in "
                f"{_fname} (expected exactly ['{_expect}']) -- the shape has "
                f"drifted, so its absence from qa-workflow.md would prove nothing"
            )
        else:
            pp33_stamp_report.append(f"{_fname}={_expect}")

    pp33_a_ok = not pp33_pre
    check(
        "PP-33(a)",
        pp33_a_ok,
        f"all {len(PP33_SITES)} workflow-type enum sites anchor exactly once "
        f"and still parse ("
        + "; ".join(pp33_report)
        + f"); the stamping shape is live on "
        + ", ".join(pp33_stamp_report)
        + f"; routing table = {len(pp33_routes)} workflows {pp33_routes}"
        + ("" if pp33_a_ok else " -- " + "; ".join(pp33_pre)),
    )

    # (b) membership. Asserted on the PARSED MEMBERS of the anchored line, never
    # on the file: `QA` as a bare token occurs dozens of times in each file.
    for _sid, _disp, _spath, _sbasis, _anchor, _extract, _split, _count, _label in (
        PP33_SITES
    ):
        if _split is not None and _sid in pp33_members:
            if "QA" not in pp33_members[_sid]:
                pp33_bad.append(
                    f"{_sid} {_disp} {_label} omits QA "
                    f"(members={pp33_members[_sid]})"
                )
            if _count is not None and _sid in pp33_counts:
                if pp33_counts[_sid] != len(pp33_members[_sid]):
                    pp33_bad.append(
                        f"{_sid} {_disp} says {pp33_counts[_sid]} workflows but "
                        f"lists {len(pp33_members[_sid])}"
                    )
        elif _split is None and _sid in pp33_counts:
            if pp33_counts[_sid] != len(pp33_routes):
                pp33_bad.append(
                    f"{_sid} {_disp} says {pp33_counts[_sid]} workflows, "
                    f"routing table has {len(pp33_routes)}"
                )

    pp33_qa_stamp = PP33_STAMP.findall(qa_norm)
    if pp33_qa_stamp != ["QA"]:
        pp33_bad.append(
            f"qa-workflow.md's stamping line is {pp33_qa_stamp} (expected "
            f"exactly ['QA']) -- the guard returns 0 on any other value, so an "
            f"unstamped route leaves every rule in this file unenforced, and "
            f"both sibling route files state theirs"
        )

    pp33_b_ok = not pp33_bad
    check(
        "PP-33(b)",
        pp33_b_ok,
        f"QA is a member of all {len(pp33_members)} workflow-type enums, the "
        f"marquee count matches the routing table, and the QA law stamps "
        f"`workflow_type: QA` like both its siblings"
        + ("" if pp33_b_ok else " -- " + "; ".join(pp33_bad)),
    )

    # PP-34 -- the guard resolves a phase from every artifact shape without
    # crashing, and rc/stderr are part of the verdict.
    #
    # A PreToolUse hook that raises exits non-zero with NOTHING on stdout, and
    # a hook that emits no decision FAILS OPEN: the tool call proceeds. So a
    # crash is indistinguishable from a deliberate allow if the property reads
    # only the decision. Every case below asserts the triple
    # (rc == 0, stderr == "", decision) -- never the decision alone.
    #
    # All six cases leave `phase_cursor` absent, because status_history is only
    # consulted when the cursor is falsy; with a cursor set, no shape of
    # status_history is reachable at all.
    #
    # (d) is the POSITIVE CONTROL and is not optional. (a)(b)(c)(e)(f) all
    # expect ALLOW, and a guard that crashes on everything also allows
    # everything -- without (d) the property is green on a totally broken
    # guard. (d) proves the guard is still engaged and still denying.
    #
    # `{}` and `"qa-plan"` also crash at HEAD, but they take the same branch as
    # (e) and (b) respectively and are covered by the edge-case catalog rather
    # than by their own checks.
    pp34_cases = [
        ("a", "[]", [], False),
        ("b", '["qa-plan"] (list of strings)', ["qa-plan"], False),
        ("c", "null", None, False),
        (
            "d",
            '[{"event":"s","phase":"qa-plan"}] (the fallback that must NOT regress)',
            [{"event": "s", "phase": "qa-plan"}],
            True,
        ),
        ("e", '{"a": 1} (a dict, not a list)', {"a": 1}, False),
        ("f", "5 (a bare int)", 5, False),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        pp34_dir = Path(tmp)
        for tag, label, history, want_deny in pp34_cases:
            pp34_payload = {
                "workflow_uuid": "wf-test-pp34",
                "workflow_id": "wf-test-pp34",
                "workflow_type": "QA",
                "qa": {"isolation": {"plan_phase_readonly": True}},
                "status_history": history,
            }
            r = run_guard_raw(
                pp34_dir,
                pp34_payload,
                {
                    "tool_name": "Bash",
                    "tool_input": {"command": f"mkdir -p {PROBE_TARGET}"},
                },
            )
            got_deny = '"permissionDecision": "deny"' in r.stdout
            stderr_tail = (r.stderr.strip().splitlines() or [""])[-1]
            ok = r.returncode == 0 and r.stderr == "" and got_deny == want_deny
            verb = "denies" if want_deny else "allows"
            check(
                f"PP-34({tag})",
                ok,
                f"rc=0 stderr='' and guard {verb} `mkdir {PROBE_TARGET}` when "
                f"status_history is {label} and phase_cursor is absent"
                + (
                    ""
                    if ok
                    else f" -- got rc={r.returncode} deny={got_deny} "
                    f"stderr={stderr_tail!r}"
                ),
            )

    # ---- PP-35: the plan-phase mutation allowlist is path-aware on BOTH -----
    # branches. The Bash branch was a bare substring test over the RAW command
    # string, so `.cc10x` appearing anywhere -- inside a shell comment, after a
    # `;`, in an unrelated argument -- bought arbitrary destruction at a phase
    # whose entire purpose is to mutate nothing. `_bash_mutates` splits with
    # `comments=True`, so the comment was stripped for PARSING and kept for the
    # escape test: the two halves of the same branch disagreed about what the
    # command said.
    #
    # The DENY rows alone are NOT a property. Delete the escape outright and
    # (a)(b)(d)(f) all pass while every legitimate `.cc10x/` write the QA route
    # depends on starts failing. (c) and (e) are the positive controls that
    # make this a property about path semantics rather than about denial.
    pp35_deny = "/etc/pp35-probe"
    pp35_allowed = ".cc10x/qa/pp35"
    pp35_cases: list[tuple[str, dict, bool, str]] = [
        (
            "a",
            {
                "tool_name": "Bash",
                "tool_input": {"command": f"rm -rf {pp35_deny} # .cc10x"},
            },
            True,
            f"Bash `rm -rf {pp35_deny} # .cc10x` (the comment-mention bypass)",
        ),
        (
            "b",
            {
                "tool_name": "Bash",
                "tool_input": {"command": f"rm -rf {pp35_deny}; echo .cc10x"},
            },
            True,
            f"Bash `rm -rf {pp35_deny}; echo .cc10x` (the trailing-mention bypass)",
        ),
        (
            "c",
            {
                "tool_name": "Bash",
                "tool_input": {"command": f"mkdir -p {pp35_allowed}"},
            },
            False,
            f"Bash `mkdir -p {pp35_allowed}` (the escape still works for real)",
        ),
        (
            "d",
            {
                "tool_name": "Bash",
                "tool_input": {"command": "mkdir -p /tmp/cc10x-pp35"},
            },
            True,
            "Bash `mkdir -p /tmp/cc10x-pp35` (the dropped `/tmp/cc10x-` entry)",
        ),
        (
            "e",
            {
                "tool_name": "Write",
                "tool_input": {"file_path": f"{pp35_allowed}.md", "content": "x"},
            },
            False,
            f"Write `{pp35_allowed}.md` (the Write branch unregressed)",
        ),
        (
            "f",
            {"tool_name": "Bash", "tool_input": {"command": f"rm -rf {pp35_deny}"}},
            True,
            f"Bash `rm -rf {pp35_deny}` (the control)",
        ),
    ]
    # Every probe path is under /etc/pp35-probe, /tmp/cc10x-pp35 or .cc10x/qa/
    # and NONE of them is ever executed: the guard is a PreToolUse hook invoked
    # as a subprocess over stdin, and it inspects the command string only.
    with tempfile.TemporaryDirectory() as tmp:
        pp35_dir = Path(tmp)
        for tag, tool_payload, want_deny, label in pp35_cases:
            r = run_guard_raw(pp35_dir, artifact("qa-plan"), tool_payload)
            got_deny = '"permissionDecision": "deny"' in r.stdout
            stderr_tail = (r.stderr.strip().splitlines() or [""])[-1]
            ok = r.returncode == 0 and r.stderr == "" and got_deny == want_deny
            verb = "denies" if want_deny else "allows"
            check(
                f"PP-35({tag})",
                ok,
                f"rc=0 stderr='' and guard {verb} {label} at phase_cursor=qa-plan"
                + (
                    ""
                    if ok
                    else f" -- got rc={r.returncode} deny={got_deny} "
                    f"stderr={stderr_tail!r}"
                ),
            )

    # ---- PP-36: all five declarations of the default mutation_allowlist -----
    # agree. The entry `/tmp/cc10x-` survived nine commits because the CODE was
    # the lone dissenter among five sites: the skeleton, the route law twice,
    # and the guard's own module docstring 193 lines above the wrong line all
    # said [".cc10x/"]. Every document a reader consulted agreed with every
    # other document, so nothing a reader could read would have caught it.
    pp36_guard_text = GUARD.read_text(encoding="utf-8")
    pp36_wf_raw = QA_WORKFLOW.read_text(encoding="utf-8")

    def _pp36_parse(site: str, text: str, pattern: str) -> tuple[str, list]:
        """Extract exactly one bracketed literal and parse it, or explain why not."""
        found = re.findall(pattern, text)
        if len(found) != 1:
            return (
                f"{site}: pattern matched {len(found)} times, expected exactly 1",
                [],
            )
        try:
            val = ast.literal_eval(found[0])
        except (ValueError, SyntaxError) as exc:
            return (f"{site}: `{found[0]}` did not parse ({exc})", [])
        if not isinstance(val, list):
            return (f"{site}: parsed a {type(val).__name__}, not a list", [])
        return ("", val)

    # Site 5 lives INSIDE a fenced JSON block, so its basis must be
    # _decommented(): _normative() strips fences and the site silently
    # vanishes, leaving a four-site property that prints "5". That is the
    # second half of I-59.
    pp36_sites: list[tuple[str, str, str]] = [
        (
            f"1 code {GUARD.name} `isolation.get(...) or [...]`",
            pp36_guard_text,
            r'isolation\.get\("mutation_allowlist"\)\s*or\s*(\[[^\]]*\])',
        ),
        (
            f"2 docstring {GUARD.name}",
            pp36_guard_text,
            r'"mutation_allowlist":\s*(\[[^\]]*\])',
        ),
        (
            f"4 law prose {QA_WORKFLOW.name} (_normative)",
            _normative(pp36_wf_raw),
            r"`mutation_allowlist`:\s*`(\[[^\]]*\])`",
        ),
        (
            f"5 law fence {QA_WORKFLOW.name} (_decommented)",
            _decommented(pp36_wf_raw),
            r'"mutation_allowlist":\s*(\[[^\]]*\])',
        ),
    ]
    pp36_problems: list[str] = []
    pp36_values: list[tuple[str, list]] = []
    for site, text, pattern in pp36_sites:
        err, val = _pp36_parse(site, text, pattern)
        if err:
            pp36_problems.append(err)
        pp36_values.append((site, val))

    # Site 3 is the one site parsed with json.load rather than a regex,
    # precisely because the skeleton is pretty-printed -- the key is on one
    # line and the value on the next, so any line-keyed parse of it is wrong.
    pp36_skel = json.loads(SKELETON.read_text(encoding="utf-8"))
    pp36_skel_val = ((pp36_skel.get("qa") or {}).get("isolation") or {}).get(
        "mutation_allowlist"
    )
    if not isinstance(pp36_skel_val, list):
        pp36_problems.append(
            f"3 skeleton {SKELETON.name} qa.isolation.mutation_allowlist: "
            f"got {type(pp36_skel_val).__name__}, not a list"
        )
        pp36_skel_val = []
    pp36_values.insert(2, (f"3 skeleton {SKELETON.name}", pp36_skel_val))

    # Anti-vacuity, asserted BEFORE the comparison: five failed parses give
    # set() == set() == set() == set() == set(), which is vacuously true. Four
    # of the five parses are regexes over text that gets reformatted, so this
    # is the likeliest way the property rots.
    pp36_empty = [site for site, val in pp36_values if not val]
    if pp36_empty:
        pp36_problems.append(
            "PRECONDITION failed: "
            + "; ".join(f"{site} parsed an empty list" for site in pp36_empty)
            + " -- an empty parse makes the set-equality vacuous"
        )
    pp36_printed = "; ".join(f"{site} = {val!r}" for site, val in pp36_values)
    if not pp36_problems:
        pp36_distinct = {tuple(sorted(set(val))) for _, val in pp36_values}
        if len(pp36_distinct) != 1:
            pp36_problems.append(
                "the five declarations disagree -- the values are printed "
                "above, and the site that differs is the one to fix"
            )
    check(
        "PP-36",
        not pp36_problems,
        "all five declarations of the default `mutation_allowlist` parse "
        f"non-empty and agree -- {pp36_printed}"
        + ("" if not pp36_problems else " -- " + "; ".join(pp36_problems)),
    )

    # ---- PP-37: a subcommand is read-only only if EVERY invocation of it ----
    # is read-only REGARDLESS OF FLAGS. `SUBCOMMAND_TOOLS` classified whole
    # subcommands, and the parser discards flags by design
    # (`if arg.startswith("-"): continue`), so a subcommand-granular allowlist
    # cannot express `git config --get` (read) vs `git config user.email x`
    # (write). Thirteen mutating invocations were therefore ALLOWED at a phase
    # whose entire purpose is to mutate nothing -- `terraform fmt` worst of
    # all, since it rewrites files with no flag at all.
    #
    # The DENY rows alone are NOT a property. Empty every value of
    # SUBCOMMAND_TOOLS and all thirteen go green while every capability probe
    # step 0a depends on (`docker info`, `kubectl get pods`, `terraform show`)
    # starts being denied. The ALLOW set is what makes this a property about
    # the rule rather than about denial; I-62 and I-89 are the two injections
    # that red the two sides separately.
    #
    # The cost of the flag-blind fix (inline ADR-1) is that only the BARE read
    # forms survive: `git config --get` is now denied too, because every
    # argument is a flag and `sub` resolves to "". That is priced, not missed.
    pp37_deny_set = [
        "git branch -D feature-x",
        "git config user.email x@y.z",
        "git tag -d v1",
        "git remote add evil https://e.example",
        "git branch -m old new",
        "terraform fmt -write=true",
        "terraform fmt",
        "npm config set registry https://e.example",
        "pip config set global.index-url https://e.example",
        "kubectl config use-context prod",
        "pnpm config set registry https://e.example",
        "yarn config set registry https://e.example",
        "kubectl config set-context prod",
    ]
    pp37_allow_set = [
        "git log --oneline -1",
        "git status --porcelain",
        "docker info",
        "kubectl get pods",
        "terraform show",
        "git show HEAD",
        "git rev-parse HEAD",
    ]
    # Anti-vacuity, asserted BEFORE the loop: a table emptied by a bad edit
    # iterates zero times and reports nothing wrong. Both floors are checked,
    # and both are reported through (a) so a truncated ALLOW set cannot hide
    # behind a green (b).
    pp37_pre: list[str] = []
    if len(pp37_deny_set) < 13:
        pp37_pre.append(
            f"DENY set holds {len(pp37_deny_set)} rows, expected >= 13"
        )
    if len(pp37_allow_set) < 7:
        pp37_pre.append(
            f"ALLOW set holds {len(pp37_allow_set)} rows, expected >= 7"
        )
    # None of these 20 command strings is ever executed: the guard is a
    # PreToolUse hook invoked as a subprocess over stdin and it inspects the
    # command string only. They are built here in the test source rather than
    # typed into a shell because cc10x_git_guard.py blocks some of them --
    # a second, independent line of defence that has nothing to say about
    # what this guard decides.
    pp37_wrong_deny: list[str] = []
    pp37_wrong_allow: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        pp37_dir = Path(tmp)
        for command, want_deny in [(c, True) for c in pp37_deny_set] + [
            (c, False) for c in pp37_allow_set
        ]:
            r = run_guard_raw(
                pp37_dir,
                artifact("qa-plan"),
                {"tool_name": "Bash", "tool_input": {"command": command}},
            )
            got_deny = '"permissionDecision": "deny"' in r.stdout
            stderr_tail = (r.stderr.strip().splitlines() or [""])[-1]
            if r.returncode == 0 and r.stderr == "" and got_deny == want_deny:
                continue
            problem = (
                f"`{command}` -> {'DENY' if got_deny else 'ALLOW'}, "
                f"want {'DENY' if want_deny else 'ALLOW'}"
            )
            if r.returncode != 0 or r.stderr != "":
                problem += f" (rc={r.returncode} stderr={stderr_tail!r})"
            (pp37_wrong_deny if want_deny else pp37_wrong_allow).append(problem)
    check(
        "PP-37(a)",
        not pp37_pre and not pp37_wrong_deny,
        f"rc=0 stderr='' and all {len(pp37_deny_set)} mutating invocations "
        "are DENIED at phase_cursor=qa-plan"
        + (
            ""
            if not pp37_pre and not pp37_wrong_deny
            else " -- " + "; ".join(pp37_pre + pp37_wrong_deny)
        ),
    )
    check(
        "PP-37(b)",
        not pp37_pre and not pp37_wrong_allow,
        f"rc=0 stderr='' and all {len(pp37_allow_set)} read-only capability "
        "probes are still ALLOWED at phase_cursor=qa-plan"
        + (
            ""
            if not pp37_pre and not pp37_wrong_allow
            else " -- " + "; ".join(pp37_pre + pp37_wrong_allow)
        ),
    )

    # ---- PP-38: the guard reads the key each tool actually passes, and the ---
    # matcher invokes it for every tool it handles.
    #
    # Claude Code's notebook tools pass `notebook_path`, not `file_path`. The
    # guard's denylist branch read only ("file_path", "path", "pattern") and its
    # plan-phase write branch read only `file_path`, so ONE missing key produced
    # two opposite defects:
    #   (a) a denylisted notebook was ALLOWED -- the quarantine was unreachable;
    #   (c) `target` was always "" for NotebookEdit, so the allowlist escape
    #       (`if target and ... _matches(target, allowlist)`) could not fire and
    #       a notebook write INTO `.cc10x/` was wrongly DENIED. That one is live
    #       today: NotebookEdit is already in the matcher.
    # (b) and (d) are the non-notebook controls: they pin that the denylist and
    # the allowlist themselves still behave, so a red on (a)/(c) localises to
    # the key lookup rather than to the matching semantics.
    #
    # (e) is not redundant with (c). The cheap way to "fix" the false-deny is to
    # make NotebookEdit's target unconditionally allowed, which passes (c) and
    # (d) and installs a NEW fail-open: notebook writes anywhere on disk during
    # a planning phase. (e) is the probe that refuses that fix.
    #
    # (f) is a separate check because (a)-(e) invoke the guard directly over
    # stdin and therefore BYPASS the PreToolUse matcher entirely. Every one of
    # them stays green while `NotebookRead` is absent from `hooks.json` and the
    # guard is consequently never invoked for it in production. The key fix and
    # the matcher fix are independently necessary, so they need independent
    # checks.
    pp38_denylist = ["/tmp/pp38-secret*"]

    def pp38_artifact(denied: list[str] | None = None) -> dict:
        payload = artifact("qa-plan")
        payload["qa"]["isolation"]["denied_reads"] = denied or []
        return payload

    # want=True means DENY. Each row is (id, artifact, tool payload, want_deny).
    pp38_cases = [
        (
            "a",
            pp38_artifact(pp38_denylist),
            {
                "tool_name": "NotebookRead",
                "tool_input": {"notebook_path": "/tmp/pp38-secret.ipynb"},
            },
            True,
        ),
        (
            "b",
            pp38_artifact(pp38_denylist),
            {
                "tool_name": "Read",
                "tool_input": {"file_path": "/tmp/pp38-secret.md"},
            },
            True,
        ),
        (
            "c",
            pp38_artifact(),
            {
                "tool_name": "NotebookEdit",
                "tool_input": {"notebook_path": ".cc10x/qa/pp38.ipynb"},
            },
            False,
        ),
        (
            "d",
            pp38_artifact(),
            {
                "tool_name": "Write",
                "tool_input": {"file_path": ".cc10x/qa/pp38.md"},
            },
            False,
        ),
        (
            "e",
            pp38_artifact(),
            {
                "tool_name": "NotebookEdit",
                "tool_input": {"notebook_path": "/tmp/pp38-out.ipynb"},
            },
            True,
        ),
    ]
    # None of these paths is created, read or written: the guard is a PreToolUse
    # hook that inspects the tool input and returns a decision on stdout.
    pp38_results: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as tmp:
        pp38_dir = Path(tmp)
        for case_id, payload, tool_payload, want_deny in pp38_cases:
            r = run_guard_raw(pp38_dir, payload, tool_payload)
            got_deny = '"permissionDecision": "deny"' in r.stdout
            stderr_tail = (r.stderr.strip().splitlines() or [""])[-1]
            if r.returncode != 0 or r.stderr != "":
                pp38_results[case_id] = (
                    f"{tool_payload['tool_name']} -> rc={r.returncode} "
                    f"stderr={stderr_tail!r} (a crashing guard emits no decision "
                    f"and reads as ALLOW)"
                )
            elif got_deny != want_deny:
                pp38_results[case_id] = (
                    f"{tool_payload['tool_name']} "
                    f"{sorted(tool_payload['tool_input'].values())[0]!r} -> "
                    f"{'DENY' if got_deny else 'ALLOW'}, "
                    f"want {'DENY' if want_deny else 'ALLOW'}"
                )

    check(
        "PP-38(a)",
        "a" not in pp38_results,
        "NotebookRead of a denylisted notebook_path is DENIED"
        + ("" if "a" not in pp38_results else " -- " + pp38_results["a"]),
    )
    check(
        "PP-38(b)",
        "b" not in pp38_results,
        "control: Read of a denylisted file_path is DENIED"
        + ("" if "b" not in pp38_results else " -- " + pp38_results["b"]),
    )
    check(
        "PP-38(c)",
        "c" not in pp38_results,
        "NotebookEdit of an allowlisted notebook_path is ALLOWED at qa-plan"
        + ("" if "c" not in pp38_results else " -- " + pp38_results["c"]),
    )
    check(
        "PP-38(d)",
        "d" not in pp38_results,
        "control: Write of an allowlisted file_path is ALLOWED at qa-plan"
        + ("" if "d" not in pp38_results else " -- " + pp38_results["d"]),
    )
    check(
        "PP-38(e)",
        "e" not in pp38_results,
        "NotebookEdit OUTSIDE the allowlist is still DENIED at qa-plan -- (c) "
        "is the allowlist working, not the notebook branch going silent"
        + ("" if "e" not in pp38_results else " -- " + pp38_results["e"]),
    )

    # PP-38(f). hooks.json is parsed as JSON and the QA guard's own entry is
    # located by its command string. A whole-file grep for "NotebookRead" is
    # satisfied by ANY other hook's matcher in the same file -- vacuity shape
    # (b). The required set is IMPORTED from the live guard module rather than
    # transcribed, so adding a tool to READ_TOOLS/WRITE_TOOLS without adding it
    # to the matcher is red (I-66); a hard-coded copy would stay green forever
    # while the real sets drift.
    pp38f_guard = load_guard()
    pp38_required = (
        set(pp38f_guard.READ_TOOLS) | set(pp38f_guard.WRITE_TOOLS) | {"Bash"}
    )
    pp38_hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    pp38_entries = [
        entry
        for matchers in pp38_hooks.get("hooks", {}).values()
        for entry in matchers
        if any(
            "cc10x_qa_isolation_guard.py" in (h.get("command") or "")
            for h in entry.get("hooks", [])
        )
    ]
    pp38f_detail = ""
    # Anti-vacuity, asserted BEFORE the containment test: zero entries makes the
    # loop iterate nothing, and an empty required set makes containment
    # vacuously true. 1 entry and 8 required tools measured at this commit.
    if len(pp38_entries) != 1:
        pp38f_ok = False
        pp38f_detail = (
            f"PRECONDITION failed: {len(pp38_entries)} hooks.json entries invoke "
            f"cc10x_qa_isolation_guard.py, expected exactly 1 -- any matcher "
            f"result below is vacuous"
        )
    elif len(pp38_required) < 8:
        pp38f_ok = False
        pp38f_detail = (
            f"PRECONDITION failed: READ_TOOLS | WRITE_TOOLS | {{Bash}} holds "
            f"{len(pp38_required)} tools, expected >= 8 -- the guard's tool sets "
            f"have been emptied, so any containment result below is vacuous"
        )
    else:
        pp38_matcher = pp38_entries[0].get("matcher") or ""
        pp38_declared = {t for t in pp38_matcher.split("|") if t}
        pp38_missing = sorted(pp38_required - pp38_declared)
        # Second clause: the prose restatement in qa-workflow.md must be the
        # same string. Exactly-one asserted before comparing -- a regex that
        # stopped matching would compare nothing and pass.
        pp38f_prose = PP38F_PROSE_MATCHER.findall(
            QA_WORKFLOW.read_text(encoding="utf-8")
        )
        pp38f_faults = (
            [
                f"matcher {pp38_matcher!r} never fires for {pp38_missing} -- "
                f"the guard is not invoked for them at all, so the key fix "
                f"above is unreachable in production"
            ]
            if pp38_missing
            else []
        )
        if len(pp38f_prose) != 1:
            pp38f_faults.append(
                f"PRECONDITION failed: {QA_WORKFLOW.name} states a `matcher "
                f"`...`` {len(pp38f_prose)} times, expected exactly 1 -- the "
                f"prose restatement cannot be compared and its drift is unheld"
            )
        elif pp38f_prose[0] != pp38_matcher:
            pp38f_faults.append(
                f"{QA_WORKFLOW.name} restates the matcher as "
                f"{pp38f_prose[0]!r}, hooks.json declares {pp38_matcher!r} -- "
                f"a second declaration of one value, drifted"
            )
        pp38f_ok = not pp38f_faults
        pp38f_detail = (
            f"hooks.json matcher declares all {len(pp38_required)} tools the "
            f"guard handles (READ_TOOLS | WRITE_TOOLS | {{Bash}}), and "
            f"{QA_WORKFLOW.name}'s prose restatement is byte-identical to it"
            if pp38f_ok
            else "; ".join(pp38f_faults)
        )
    check("PP-38(f)", pp38f_ok, pp38f_detail)

    # ---- PP-44: a FINISHED workflow disengages the guard entirely. ----------
    #
    # PR-#91 P1-1. A QA workflow scoped to the plan phase, or abandoned mid-
    # plan, leaves `phase_cursor` on a planning value forever. The guard keyed
    # ONLY on that cursor, so for as long as the abandoned artifact remained
    # the newest on disk it denied every Write and every mutating Bash call in
    # the repo -- including work that had nothing to do with the workflow, and
    # including the router's own documented way of starting the next workflow.
    # A quarantine and a read-only phase belong to a LIVE workflow; a finished
    # one must take both with it.
    #
    # (a) covers the cursor form the router is required to leave behind
    # (SKILL.md §12 step 3 sets `phase_cursor=memory-finalize`). (b) covers
    # every terminal status_history event, parametrised, with the cursor
    # REMOVED so the history fallback -- not the cursor -- is what disengages.
    # (c) is the control that keeps (a)/(b) a property about terminal state
    # rather than about a guard that stopped denying: same artifact, same
    # probe, last event non-terminal -> still DENY.
    pp44_probes = "/tmp/pp44-probe"
    pp44_cases: list[tuple[str, dict, bool]] = [
        (
            "a",
            {"phase_cursor": "memory-finalize"},
            False,
        ),
        *[
            (
                f"b-{evt}",
                {
                    "phase_cursor": None,
                    "status_history": [
                        {"event": "started", "phase": "qa"},
                        {"event": evt, "phase": "qa-plan"},
                    ],
                },
                False,
            )
            for evt in ("memory_finalized", "workflow_completed", "workflow_failed")
        ],
        (
            "c",
            {
                "phase_cursor": None,
                "status_history": [
                    {"event": "started", "phase": "qa"},
                    {"event": "result_persisted", "phase": "qa-plan"},
                ],
            },
            True,
        ),
    ]
    pp44_faults: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        pp44_dir = Path(tmp)
        for tag, overrides, want_deny in pp44_cases:
            pp44_payload = artifact(None)
            for key, val in overrides.items():
                if val is None:
                    pp44_payload.pop(key, None)
                else:
                    pp44_payload[key] = val
            r = run_guard_raw(
                pp44_dir,
                pp44_payload,
                {"tool_name": "Bash", "tool_input": {"command": f"mkdir -p {pp44_probes}"}},
            )
            got_deny = '"permissionDecision": "deny"' in r.stdout
            ok = r.returncode == 0 and r.stderr == "" and got_deny == want_deny
            if not ok:
                pp44_faults.append(
                    f"({tag}) -> deny={got_deny} want {want_deny} "
                    f"(rc={r.returncode} stderr={(r.stderr.strip().splitlines() or [''])[-1]!r})"
                )
    check(
        "PP-44",
        not pp44_faults,
        f"a terminal cursor or terminal last status_history event disengages the "
        f"guard ({len(pp44_cases)} cases incl. the non-terminal control), and a "
        f"non-terminal last event does not"
        + ("" if not pp44_faults else " -- " + "; ".join(pp44_faults)),
    )

    # ---- PP-45: the guard's Bash surface -- parser, router commands, --------
    # ---- redirects. PR-#91 P1-2 / P2-1 / P2-5.                              --
    #
    # Three defects in one function family, landed together because they are
    # one surface:
    #
    # P1-2 -- the guard denied commands the ROUTER is required to run during
    #         plan phases: the mandatory template copy (SKILL.md route law,
    #         qa-workflow.md `#### Plan`) and the event-log append (SKILL.md
    #         §12 step 7). Both write only into `.cc10x/`; the copy was denied
    #         because its SOURCE (the plugin root) is outside every allowlist
    #         and the old escape tested read operands as writes, the append
    #         because a redirect was denied before its target was ever matched
    #         against the allowlist. (a) and (b) are the LITERAL commands from
    #         the two documents, not paraphrases -- a paraphrase tests the
    #         paraphrase. (c) is the control: the escape is path-aware, not a
    #         blanket allow on the router's vocabulary.
    #
    # P2-1 -- the parser saw only whitespace-separated operators, so
    #         `echo hi;mkdir x`, `echo hi\nmkdir x`, `sudo rm -rf x`,
    #         `bash -c "mkdir y"` and `xargs rm` all reached the classifier as
    #         one innocent command. (d)-(i) pin each bypass closed, and (j) is
    #         the benign control that the tokenizer did not become
    #         operator-blind: quoted operators and redirects inside quotes are
    #         data, not commands.
    #
    # P2-5 -- redirect detection existed but had NO test (mutation M6: disable
    #         it and the suite stayed green), and it missed `2>file` because
    #         the digit-lookbehind that excludes `2>&1` excludes it too.
    #         (k)-(n) pin the four sides: /dev/null exempt (step 0a's
    #         `docker info >/dev/null` probe), allowlisted target allowed,
    #         non-allowlisted target denied, `2>file` detected.
    pp45_uuid = "2f9a8c4d"
    pp45_router_copy = (
        f'mkdir -p .cc10x/qa/{pp45_uuid} && cp "${{CLAUDE_PLUGIN_ROOT}}/templates/qa-test-plan.template.md" '
        f'.cc10x/qa/{pp45_uuid}/test-plan.md && cp "${{CLAUDE_PLUGIN_ROOT}}/templates/qa-env-plan.template.md" '
        f'.cc10x/qa/{pp45_uuid}/env-plan.md'
    )
    pp45_router_append = (
        'printf \'%s\\n\' \'{"ts":"2026-01-01T00:00:00Z","wf":"wf-pp45","event":"result_persisted",'
        '"phase":"qa-plan","agent":"qa-plan","decision":"ok","reason":"plan written"}\' '
        '>> .cc10x/workflows/wf-pp45.events.jsonl'
    )
    pp45_cases: list[tuple[str, str, bool]] = [
        ("a", pp45_router_copy, False),
        ("b", pp45_router_append, False),
        ("c", "mkdir -p /tmp/pp45-outside", True),
        ("d", f"echo hi\nmkdir -p {pp44_probes}-nl", True),
        ("e", f"echo hi;mkdir -p {pp44_probes}-semi", True),
        ("f", f"echo hi&&mkdir -p {pp44_probes}-and", True),
        ("g", f"sudo rm -rf {pp44_probes}-sudo", True),
        ("h", 'bash -c "mkdir -p %s-bashc"' % f"{pp44_probes}", True),
        ("i", f"echo x | xargs rm -rf {pp44_probes}-xargs", True),
        ("j", "echo 'a;b' && printf '%s' hi", False),
        ("k", "docker info >/dev/null", False),
        ("l", "echo done >> .cc10x/qa/progress.md", False),
        ("m", "echo done >> /tmp/pp45-redirect", True),
        ("n", f"grep pat f.md 2>{pp44_probes}-err", True),
    ]
    pp45_faults: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        pp45_dir = Path(tmp)
        for tag, command, want_deny in pp45_cases:
            r = run_guard_raw(
                pp45_dir,
                artifact("qa-plan"),
                {"tool_name": "Bash", "tool_input": {"command": command}},
            )
            got_deny = '"permissionDecision": "deny"' in r.stdout
            ok = r.returncode == 0 and r.stderr == "" and got_deny == want_deny
            if not ok:
                pp45_faults.append(
                    f"({tag}) `{command[:60]}` -> deny={got_deny} want {want_deny} "
                    f"(rc={r.returncode} stderr={(r.stderr.strip().splitlines() or [''])[-1]!r})"
                )
    check(
        "PP-45",
        not pp45_faults,
        f"router-mandated commands pass the plan-phase allowlist, parser bypasses "
        f"(newline / unspaced operators / sudo / bash -c / xargs) are denied, and "
        f"redirect detection is pinned on all four sides ({len(pp45_cases)} cases)"
        + ("" if not pp45_faults else " -- " + "; ".join(pp45_faults)),
    )

    # ---- PP-46: the denylist is ROOT-AWARE. PR-#91 P2-2. --------------------
    #
    # The denylist matched a tool that NAMED a quarantined path. A tool whose
    # search ROOT contains one -- Grep over the project, Grep over an ancestor
    # directory, a Bash `grep -r` from an ancestor -- reads the quarantined
    # content as surely as a Read of the file, and passed. The quarantine is
    # a refusal, not a request; a refusal with a recursive hole in it is a
    # request.
    #
    # (a) Grep over an ancestor of a quarantined absolute path. (b) Grep with
    # NO path -- Claude Code searches the whole project -- where the quarantine
    # lives inside the project: the absent root is the project root, not "no
    # root". (c) is the counter-control for (b): a quarantine OUTSIDE the
    # project does not make a pathless Grep deny. (d) the Bash recursive
    # reader from an ancestor. (e) the non-recursive control: `grep` without
    # -r reads only the files it names, and a file it names that is not
    # quarantined passes. (f) a `cp` whose SOURCE is quarantined: the read
    # operand is checked against the denylist even though the plan-phase
    # escape deliberately ignores read operands -- the two branches ask
    # different questions of the same token stream.
    pp46_denied_abs = "/tmp/pp46-denied/answers.md"
    pp46_cases: list[tuple[str, dict, dict, bool]] = [
        (
            "a",
            {"denied_reads": [pp46_denied_abs]},
            {"tool_name": "Grep", "tool_input": {"pattern": "answers", "path": "/tmp"}},
            True,
        ),
        (
            "b",
            {"denied_reads": [".cc10x/qa/answer-sheet.md"]},
            {"tool_name": "Grep", "tool_input": {"pattern": "answers"}},
            True,
        ),
        (
            "c",
            {"denied_reads": [pp46_denied_abs]},
            {"tool_name": "Grep", "tool_input": {"pattern": "answers"}},
            False,
        ),
        (
            "d",
            {"denied_reads": [pp46_denied_abs]},
            {"tool_name": "Bash", "tool_input": {"command": "grep -r answers /tmp"}},
            True,
        ),
        (
            "e",
            {"denied_reads": [pp46_denied_abs]},
            {"tool_name": "Bash", "tool_input": {"command": "grep answers /etc/hosts"}},
            False,
        ),
        (
            "f",
            {"denied_reads": [pp46_denied_abs]},
            {
                "tool_name": "Bash",
                "tool_input": {"command": f"cp {pp46_denied_abs} .cc10x/qa/x.md"},
            },
            True,
        ),
    ]
    pp46_faults: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        pp46_dir = Path(tmp)
        for tag, isolation_extra, tool_payload, want_deny in pp46_cases:
            pp46_payload = artifact("qa-plan")
            pp46_payload["qa"]["isolation"].update(isolation_extra)
            r = run_guard_raw(pp46_dir, pp46_payload, tool_payload)
            got_deny = '"permissionDecision": "deny"' in r.stdout
            ok = r.returncode == 0 and r.stderr == "" and got_deny == want_deny
            if not ok:
                pp46_faults.append(
                    f"({tag}) {tool_payload['tool_name']} -> deny={got_deny} "
                    f"want {want_deny} "
                    f"(rc={r.returncode} stderr={(r.stderr.strip().splitlines() or [''])[-1]!r})"
                )
    check(
        "PP-46",
        not pp46_faults,
        f"a search root that CONTAINS a quarantined path is denied, for Grep "
        f"(with and without a path) and for Bash recursive readers, without "
        f"denying non-recursive reads or out-of-project roots ({len(pp46_cases)} cases)"
        + ("" if not pp46_faults else " -- " + "; ".join(pp46_faults)),
    )

    # ---- PP-39: every BLOCKING hook is enumerated in the policy, and the ----
    # ---- policy's mode claim matches which of them call load_mode.       ----
    #
    # Both halves are computed from source. The enumeration is read out of the
    # parsed hooks.json, never out of a literal list in this file: a hook added
    # to hooks.json and not to the policy must be red here, and a transcribed
    # list would stay green forever while the two drifted apart.
    pp39_hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    pp39_candidates: dict[str, Path] = {}
    for _event in PP39_EVENTS:
        for _entry in pp39_hooks.get("hooks", {}).get(_event, []):
            for _h in _entry.get("hooks", []):
                for _name in PP39_SCRIPT_REF.findall(_h.get("command") or ""):
                    pp39_candidates[_name] = SCRIPTS / _name

    pp39_blocking: dict[str, str] = {}
    pp39_no_block: list[str] = []
    for _name, _path in sorted(pp39_candidates.items()):
        if not _path.exists():
            pp39_no_block.append(f"{_name} (no such script)")
            continue
        _src = _path.read_text(encoding="utf-8")
        if PP39_BLOCK_PATH.search(_src):
            pp39_blocking[_name] = _src
        else:
            pp39_no_block.append(f"{_name} (no block path)")

    pp39_mode_aware = sorted(
        n for n, s in pp39_blocking.items() if PP39_LOAD_MODE_CALL.search(s)
    )
    pp39_unconditional = sorted(set(pp39_blocking) - set(pp39_mode_aware))
    pp39_census = (
        f"{len(pp39_blocking)} blocking / {len(pp39_mode_aware)} mode-aware / "
        f"{len(pp39_unconditional)} unconditional {pp39_unconditional}"
    )
    # Anti-vacuity, asserted BEFORE either membership loop: an empty blocking
    # set makes (a) iterate nothing and makes (b)'s `unconditional` empty, and
    # both would pass while checking nothing.
    pp39_precondition = (
        ""
        if len(pp39_blocking) >= PP39_MIN_HOOKS
        else (
            f"PRECONDITION failed: {len(pp39_blocking)} blocking hooks derived "
            f"from {HOOKS_JSON.name} at {PP39_EVENTS}, expected >= "
            f"{PP39_MIN_HOOKS} — the block-path regex has stopped matching "
            f"(rejected: {pp39_no_block or 'none'}), so every membership "
            f"result below is vacuous"
        )
    )

    policy_norm = _normative(HOOK_POLICY.read_text(encoding="utf-8"))

    # (a) enumeration completeness. A hook the policy never names is a hook
    # nobody reading the policy knows can deny their tool call.
    pp39a_unnamed = [n for n in sorted(pp39_blocking) if n not in policy_norm]
    pp39a_ok = not pp39_precondition and not pp39a_unnamed
    check(
        "PP-39(a)",
        pp39a_ok,
        pp39_precondition
        or (
            f"{HOOK_POLICY.name} names all {len(pp39_blocking)} blocking hook "
            f"scripts by basename ({pp39_census})"
            if pp39a_ok
            else (
                f"{HOOK_POLICY.name} never names {pp39a_unnamed} — the policy "
                f"enumerates hooks by event and purpose, so a reader cannot "
                f"tell which file denies their call ({pp39_census})"
            )
        ),
    )

    # (b) the mode claim is arithmetically true, INSIDE the mode paragraph.
    pp39_w8_s = list(PP39_W8_START.finditer(policy_norm))
    pp39_w8_e = list(PP39_W8_END.finditer(policy_norm))
    pp39b_fault = pp39_precondition
    pp39_w8 = ""
    if not pp39b_fault and (
        len(pp39_w8_s) != 1
        or len(pp39_w8_e) != 1
        or not pp39_w8_s[0].end() < pp39_w8_e[0].start()
    ):
        pp39b_fault = (
            f"PRECONDITION failed: W8 has {len(pp39_w8_s)} opening and "
            f"{len(pp39_w8_e)} closing anchors in {HOOK_POLICY.name} (expected "
            f"exactly 1 of each, in that order) — the mode paragraph's lead-in "
            f"has moved or been reworded, and any result over this window "
            f"would be vacuous"
        )
    elif not pp39b_fault:
        pp39_w8 = policy_norm[pp39_w8_s[0].start() : pp39_w8_e[0].start()]
        # SET EQUALITY, not containment. Containment is one-sided and misses
        # the defect in the direction this phase actually travels: if a hook
        # starts calling load_mode, it leaves `unconditional` while the
        # paragraph still lists it, and a `names every member` test stays
        # green on a paragraph that is now false. I-67 injects exactly that.
        _declared = set(re.findall(r"[A-Za-z0-9_]+\.py", pp39_w8))
        _unnamed = sorted(set(pp39_unconditional) - _declared)
        _overnamed = sorted(_declared - set(pp39_unconditional))
        if _unnamed or _overnamed:
            pp39b_fault = (
                (
                    f"the mode paragraph does not name {_unnamed} — these "
                    f"scripts never call load_mode and block whatever the mode "
                    f"says, so a paragraph that omits them tells the reader the "
                    f"mode switch covers hooks it does not cover. "
                    if _unnamed
                    else ""
                )
                + (
                    f"the mode paragraph calls {_overnamed} unconditional, but "
                    f"{'it calls' if len(_overnamed) == 1 else 'they call'} "
                    f"load_mode — the claim is false in the other direction"
                    if _overnamed
                    else ""
                )
            ).strip()
    pp39_w8_py = sorted(set(re.findall(r"[A-Za-z0-9_]+\.py", pp39_w8)))
    check(
        "PP-39(b)",
        not pp39b_fault,
        f"the mode paragraph declares unconditional exactly the hooks that do not call load_mode "
        f"({pp39_census}; W8={len(pp39_w8.encode('utf-8'))}B normative, "
        f".py tokens in window: {pp39_w8_py or 'none'})"
        + ("" if not pp39b_fault else " — " + pp39b_fault),
    )

    # ---------------------------------------------------------------- PP-40
    # Sibling of PP-9. PP-9 asks whether `§N` EXISTS; PP-40 asks whether the
    # words next to it name the section the number points at. B2 lived in the
    # gap: `test plan §6 known gaps` is a citation whose number exists and whose
    # words name `## 7. Known gaps`. See the constants block for the four-branch
    # verdict rule and why each branch exists.
    pp40_titles = {
        "test": _pp40_headings(QA_TEST_PLAN_TPL),
        "env": _pp40_headings(ENV_PLAN_TPL),
    }
    pp40_title_tokens = {
        vocab: {num: _pp40_tokens(title) for num, title in titles.items()}
        for vocab, titles in pp40_titles.items()
    }
    pp40_mismatches: list[str] = []
    pp40_undescriptive: set[tuple[str, int, int]] = set()
    pp40_matched = pp40_fallback = pp40_noprefix = 0
    pp40_hits: dict[str, int] = {}
    for pp40_path in (ENV_PLAN_TPL, HARNESS_AGENT, QA_WORKFLOW):
        pp40_text = pp40_path.read_text(encoding="utf-8")
        pp40_skip = _pp40_normative_lines(pp40_text)
        pp40_hits[pp40_path.name] = 0
        for pp40_lineno, pp40_line in enumerate(pp40_text.splitlines(), 1):
            if pp40_lineno in pp40_skip:
                continue
            for cite in PP40_CITATION.finditer(pp40_line):
                pp40_hits[pp40_path.name] += 1
                num = int(cite.group(1))
                vocab = _pp40_prefix(pp40_line, cite.start())
                if vocab is None:
                    pp40_noprefix += 1          # SKILL.md / RFC / bare / ambiguous
                    continue
                titles = pp40_titles[vocab]
                title_tokens = pp40_title_tokens[vocab]
                words = _pp40_trailing(pp40_line[cite.end():])
                cited = _pp40_tokens(words)
                where = f"{pp40_path.name}:{pp40_lineno}"
                if num not in titles:           # branch 5
                    pp40_mismatches.append(
                        f'{where} §{num} "{words}" — no such heading in the '
                        f"{vocab}-plan template"
                    )
                elif not cited:                 # branch 1
                    pp40_fallback += 1
                elif cited & title_tokens[num]:  # branch 2
                    pp40_matched += 1
                else:
                    other = [
                        m for m in sorted(titles) if m != num and cited & title_tokens[m]
                    ]
                    if other:                   # branch 3 -- the whole property
                        named = other[0]
                        pp40_mismatches.append(
                            f'{where} §{num} "{words}" names '
                            f'"## {named}. {titles[named]}", not '
                            f'"## {num}. {titles[num]}"'
                        )
                    else:                       # branch 4
                        pp40_undescriptive.add((pp40_path.name, pp40_lineno, num))
    pp40_resolved = pp40_matched + pp40_fallback + len(pp40_undescriptive)
    # Anti-vacuity, asserted BEFORE the mismatch list. (a) a floor on the
    # enumerated corpus -- a resolver that silently stops resolving reports zero
    # mismatches and is indistinguishable from a clean tree. The floor sits clear
    # of the true count (10) so it does not do the membership half's job.
    # (c) the citation regex matched in every file scanned.
    pp40_faults: list[str] = []
    if pp40_resolved < PP40_MIN_CITATIONS:
        pp40_faults.append(
            f"PRECONDITION: only {pp40_resolved} citations resolved, floor is "
            f"{PP40_MIN_CITATIONS} — the resolver stopped resolving and a "
            f"resolver that resolves nothing reports no mismatches"
        )
    pp40_dead = sorted(name for name, n in pp40_hits.items() if n == 0)
    if pp40_dead:
        pp40_faults.append(
            f"PRECONDITION: the §N regex matched nothing in {pp40_dead}"
        )
    if pp40_undescriptive != PP40_UNDESCRIPTIVE:
        pp40_faults.append(
            "the undescriptive class is not PP40_UNDESCRIPTIVE: joined "
            f"{sorted(pp40_undescriptive - PP40_UNDESCRIPTIVE)}, left "
            f"{sorted(PP40_UNDESCRIPTIVE - pp40_undescriptive)}"
        )
    pp40_faults.extend(pp40_mismatches)
    check(
        "PP-40",
        not pp40_faults,
        f"every prefixed §N citation's trailing words name the section its "
        f"number names ({pp40_matched} matched / {pp40_fallback} fallback / "
        f"{len(pp40_undescriptive)} undescriptive / {pp40_noprefix} no-prefix "
        f"= {pp40_matched + pp40_fallback + len(pp40_undescriptive) + pp40_noprefix + len(pp40_mismatches)} "
        f"§N seen; undescriptive={sorted(pp40_undescriptive)})"
        + ("" if not pp40_faults else " — " + "; ".join(pp40_faults)),
    )

    # ---------------------------------------------------------------- PP-41
    # Every producer enum covers the values its consumers require.
    # All three sub-checks slice `_decommented()`; see the PP-41 constant
    # block for why `_normative()` would delete four of the five anchors.
    def _pp41_window(
        text: str,
        start_re: "re.Pattern[str]",
        end_re: "re.Pattern[str]",
        label: str,
        *,
        end_optional: bool = False,
    ) -> tuple[str, str | None]:
        """Slice one window under R9 semantics, or explain why it is vacuous.

        Anti-vacuity shape (c): the start anchor must match EXACTLY once over
        the whole text, and the end anchor is searched from AFTER the
        start-anchor match, never from its start offset — an end regex that
        matches its own start line yields a 0-byte window in which every
        `not in` test passes.
        """
        starts = list(start_re.finditer(text))
        if len(starts) != 1:
            return "", (
                f"PRECONDITION failed: {label} start anchor "
                f"{start_re.pattern!r} matched {len(starts)} times (expected "
                f"exactly 1) — the window has moved, been reworded, or been "
                f"normalised away, and every assertion over it would be vacuous"
            )
        s = starts[0]
        end = end_re.search(text, s.end())
        if end is None:
            if not end_optional:
                return "", (
                    f"PRECONDITION failed: {label} end anchor "
                    f"{end_re.pattern!r} never matches after the start anchor "
                    f"— the window runs to EOF, which is a runaway window, not "
                    f"a measurement"
                )
            return text[s.start() :], None
        return text[s.start() : end.start()], None

    researcher_dec = _decommented(RESEARCHER_AGENT.read_text(encoding="utf-8"))
    executor_dec = _decommented(EXECUTOR_AGENT.read_text(encoding="utf-8"))
    harness_dec = _decommented(HARNESS_AGENT.read_text(encoding="utf-8"))

    # PP-41(a) — provenance. Binary `verbatim` cannot express `Vp`, the value
    # both consumers mandate and the one the middle case needs.
    pp41a_faults: list[str] = []
    w4, w4_fault = _pp41_window(
        researcher_dec, PP41_W4_START, PP41_W4_END, "W4 (OBSERVABILITY_POINTS)"
    )
    w9, w9_fault = _pp41_window(
        researcher_dec,
        PP41_CONTRACT_RULES,
        PP41_SECTION_END,
        "W9 (qa-researcher CONTRACT RULES)",
        end_optional=True,  # CONTRACT RULES is the last section of the file
    )
    for f in (w4_fault, w9_fault):
        if f:
            pp41a_faults.append(f)
    if not w4_fault:
        if not PP41_PROVENANCE_FIELD.search(w4):
            pp41a_faults.append(
                "W4 declares no `provenance:` field — the OBSERVABILITY_POINTS "
                "block still cannot say which of V/Vp/I a log line is"
            )
        missing_vals = [v for v in PP41_PROVENANCE if f'"{v}"' not in w4]
        if missing_vals:
            pp41a_faults.append(
                f"W4's provenance enum omits {missing_vals} — the consumers "
                f"mandate all three, and the omitted value is the one a "
                f"conforming researcher has to lie about"
            )
        if PP41_VERBATIM_FIELD.search(w4):
            pp41a_faults.append(
                "W4 still carries a `verbatim:` field — a three-valued field "
                "called `verbatim` holding `I` is its own next bug"
            )
    if not w9_fault:
        # The MUST rule lives OUTSIDE the yaml fence and outside W4. Change
        # 152 and forget 172 and the contract rule points at a deleted field
        # while the W4 half of this property is green.
        if "`provenance`" not in w9:
            pp41a_faults.append(
                "the CONTRACT RULES region (W9) never names `provenance` — the "
                "MUST rule does not mandate the field the block declares"
            )
        if "`verbatim`" in w9:
            pp41a_faults.append(
                "the CONTRACT RULES region (W9) still names `verbatim` as a "
                "field — the MUST rule points at a field that no longer exists"
            )
    # End-to-end: the vocabulary must reach both documents that consume it.
    for tpl in (QA_TEST_PLAN_TPL, QA_FEATURE_MAP_TPL):
        tpl_dec = _decommented(tpl.read_text(encoding="utf-8"))
        absent = [v for v in PP41_PROVENANCE if f"`{v}`" not in tpl_dec]
        if absent:
            pp41a_faults.append(
                f"{tpl.name} does not name {absent} — the producer and its "
                f"consumer would be speaking different vocabularies"
            )
    check(
        "PP-41(a)",
        not pp41a_faults,
        f"qa-researcher's OBSERVABILITY_POINTS declares provenance V/Vp/I and "
        f"its CONTRACT RULES mandate the same field "
        f"(W4={len(w4.encode('utf-8'))}B, W9={len(w9.encode('utf-8'))}B, both "
        f"decommented)"
        + ("" if not pp41a_faults else " — " + "; ".join(pp41a_faults)),
    )

    # PP-41(b) — teardown. The template enumerated two of the contract's three.
    pp41b_faults: list[str] = []
    w3, w3_fault = _pp41_window(
        executor_dec, PP41_W3_START, PP41_W3_END, "W3 (TEARDOWN_STATUS enum)"
    )
    w7, w7_fault = _pp41_window(
        executor_dec,
        PP41_CONTRACT_RULES,
        PP41_SECTION_END,
        "W7 (qa-executor CONTRACT RULES)",
    )
    for f in (w3_fault, w7_fault):
        if f:
            pp41b_faults.append(f)
    contract_vals: set[str] = set()
    tpl_vals: set[str] = set()
    if not w3_fault:
        contract_vals = set(PP41_ENUM_VALUE.findall(w3.splitlines()[0]))
        if len(contract_vals) < 2:
            pp41b_faults.append(
                f"PRECONDITION: parsed only {sorted(contract_vals)} from the "
                f"TEARDOWN_STATUS enum line — the value regex has stopped "
                f"matching and a set equality between two empty sets holds"
            )
    rows = PP41_TEARDOWN_ROW.findall(PP19_TPL.read_text(encoding="utf-8"))
    if len(rows) != 1:
        pp41b_faults.append(
            f"PRECONDITION: {PP19_TPL.name} has {len(rows)} `| Teardown status |` "
            f"rows (expected exactly 1) — the row has been renamed and the "
            f"comparison below has nothing to compare"
        )
    else:
        tpl_vals = {v.strip() for v in rows[0].split(r"\|") if v.strip()}
    if contract_vals and tpl_vals:
        # SET EQUALITY, not containment. Containment in either direction
        # passes while one side quietly grows a value the other never learned.
        if contract_vals != tpl_vals:
            pp41b_faults.append(
                f"executor {sorted(contract_vals)} != template "
                f"{sorted(tpl_vals)} — the report template offers no cell for "
                f"a status the contract requires the executor to emit"
            )
    if not w7_fault and contract_vals:
        # Every value needs a stated PASS/FAIL consequence, not one inferred
        # from the PASS conjunction. `not_run` had none.
        unstated = sorted(
            v for v in contract_vals if f"TEARDOWN_STATUS={v}" not in w7
        )
        if unstated:
            pp41b_faults.append(
                f"the executor's CONTRACT RULES state no PASS/FAIL consequence "
                f"for TEARDOWN_STATUS={unstated} — a value the contract can "
                f"emit and the contract rules never adjudicate"
            )
    check(
        "PP-41(b)",
        not pp41b_faults,
        f"the teardown enum, its report row and its verdict rules agree on "
        f"{sorted(contract_vals) or 'nothing'} "
        f"(W3={len(w3.encode('utf-8'))}B, W7={len(w7.encode('utf-8'))}B, both "
        f"decommented)"
        + ("" if not pp41b_faults else " — " + "; ".join(pp41b_faults)),
    )

    # PP-41(c) — tier disambiguation. `tier` meant a T0-T4 cost tier on a
    # CHECKS entry and a harness tier on a BUG_CANDIDATES entry that
    # cross-references that very CHECKS entry, inside ONE output block.
    pp41c_faults: list[str] = []
    w2, w2_fault = _pp41_window(
        harness_dec, PP41_W2_START, PP41_W2_END, "W2 (preflight-only block)"
    )
    n_tier = n_surface = n_carve = -1
    if w2_fault:
        pp41c_faults.append(w2_fault)
    else:
        n_tier = len(PP41_TIER_FIELD.findall(w2))
        n_surface = len(PP41_SURFACE_TIER_FIELD.findall(w2))
        if n_tier != 1:
            pp41c_faults.append(
                f"{n_tier} bare `tier:` fields in the preflight block, want 1 "
                f"— two fields named `tier` in one output block, one holding "
                f"`\"T1\"` and one holding `\"ui\"`, is the defect"
            )
        if n_surface != 1:
            pp41c_faults.append(
                f"{n_surface} `surface_tier:` fields in the preflight block, "
                f"want 1 — the harness tier at which a defect surfaces has no "
                f"name of its own"
            )
        missing_carve = [f for f in PP41_CARVE_OUT_FIELDS if f not in w2]
        n_carve = len(PP41_CARVE_OUT_FIELDS) - len(missing_carve)
        if missing_carve:
            pp41c_faults.append(
                f"the executor-field carve-out comment does not name "
                f"{missing_carve} — the comment that exists to enumerate what "
                f"preflight deliberately does not share is incomplete"
            )
    check(
        "PP-41(c)",
        not pp41c_faults,
        f"the preflight block names its cost tier and its surface tier "
        f"differently ({n_tier} `tier:` / {n_surface} `surface_tier:`, "
        f"{n_carve}/{len(PP41_CARVE_OUT_FIELDS)} carve-out fields named; "
        f"W2={len(w2.encode('utf-8'))}B decommented)"
        + ("" if not pp41c_faults else " — " + "; ".join(pp41c_faults)),
    )

    # ---------------------------------------------------------------- PP-42
    # PP-42(a) -- FAILURE_CLASS has exactly one declared owner, and the other
    # two files point at it. Window-anchored to W6 over `_normative()`; see
    # the PP-42 constant block for why W5 cannot be used.
    pp42a_faults: list[str] = []
    wf_norm_42 = _normative(QA_WORKFLOW.read_text(encoding="utf-8"))
    w6, w6_fault = _pp41_window(
        wf_norm_42, PP42A_W6_START, PP42A_W6_END, "W6 (the failure vocabulary)"
    )
    w6_bytes = len(w6.encode("utf-8"))
    claim_files: list[str] = []
    if w6_fault:
        pp42a_faults.append(w6_fault)
    else:
        if w6_bytes < PP42A_W6_MIN_BYTES:
            pp42a_faults.append(
                f"PRECONDITION failed: W6 is {w6_bytes}B, below the "
                f"{PP42A_W6_MIN_BYTES}B floor -- the section has been gutted "
                f"and every assertion over it is vacuous"
            )
        else:
            if any(ph in w6 for ph in PP42_AUTHORITY_PHRASES):
                claim_files.append(QA_WORKFLOW.name)
            # A claim that migrated OUT of the owning section is still a
            # claim, and W6 alone cannot see it.
            stray = sum(
                wf_norm_42.count(ph) - w6.count(ph) for ph in PP42_AUTHORITY_PHRASES
            )
            if stray:
                pp42a_faults.append(
                    f"{stray} authority phrase(s) in {QA_WORKFLOW.name} outside "
                    f"W6 -- the claim has left the section that owns it"
                )
    agent_texts = {
        EXECUTOR_AGENT.name: _normative(EXECUTOR_AGENT.read_text(encoding="utf-8")),
        HARNESS_AGENT.name: _normative(HARNESS_AGENT.read_text(encoding="utf-8")),
    }
    for name, text in agent_texts.items():
        if any(ph in text for ph in PP42_AUTHORITY_PHRASES):
            claim_files.append(name)
        if PP42A_OWNER_NAME not in text:
            pp42a_faults.append(
                f"{name} carries no pointer naming {PP42A_OWNER_NAME} -- a "
                f"non-owner that names no owner leaves the reader to guess"
            )
    # EXACTLY 1, not >= 1. The defect was two claims; containment is green on
    # two, which is the state this property exists to forbid.
    if len(claim_files) != 1:
        pp42a_faults.append(
            f"{len(claim_files)} file(s) claim authority over FAILURE_CLASS "
            f"{sorted(claim_files)}, want exactly 1 ({QA_WORKFLOW.name})"
        )
    elif claim_files[0] != QA_WORKFLOW.name:
        pp42a_faults.append(
            f"the sole authority claim is in {claim_files[0]}, not "
            f"{QA_WORKFLOW.name} -- the vocabulary's home is the route law"
        )
    check(
        "PP-42(a)",
        not pp42a_faults,
        f"FAILURE_CLASS is claimed by exactly 1 file ({', '.join(sorted(claim_files)) or 'none'}) "
        f"and pointed at by {len(PP42A_POINTERS)} (W6={w6_bytes}B normative)"
        + ("" if not pp42a_faults else " -- " + "; ".join(pp42a_faults)),
    )

    # PP-42(b) -- one writer of the report shape, asserted in BOTH directions.
    # RAW text for the `cp`: it lives inside a ```text fence and `_normative()`
    # deletes it. Precedent is PP-19(b), which reads the same line raw.
    pp42b_faults: list[str] = []
    wf_raw_42 = QA_WORKFLOW.read_text(encoding="utf-8")
    n_cp = len(PP42B_CP_LINE.findall(wf_raw_42))
    if n_cp != 1:
        pp42b_faults.append(
            f"{n_cp} router `cp` of {PP19_TPL.name} into report.md in "
            f"{QA_WORKFLOW.name}, want exactly 1 -- with the builder's "
            f"deliverable dropped, deleting this line leaves the report shape "
            f"with no writer at all"
        )
    harness_raw_42 = HARNESS_AGENT.read_text(encoding="utf-8")
    tbl, tbl_fault = _pp41_window(
        harness_raw_42, PP42B_TABLE_START, PP42B_TABLE_END, "the deliverables table"
    )
    n_rows = -1
    if tbl_fault:
        pp42b_faults.append(tbl_fault)
    else:
        rows = [ln for ln in tbl.splitlines() if PP42B_TABLE_ROW.match(ln)]
        n_rows = len(rows)
        if n_rows != PP42B_EXPECTED_ROWS:
            pp42b_faults.append(
                f"{n_rows} deliverable rows, want {PP42B_EXPECTED_ROWS} -- the "
                f"table grew or shrank and the renumbering was not reviewed"
            )
        producers = [ln for ln in rows if PP42B_REPORT_PRODUCER.search(ln)]
        if producers:
            pp42b_faults.append(
                f"{len(producers)} deliverable row(s) still claim the report "
                f"shape: {[ln.strip()[:60] for ln in producers]} -- two writers "
                f"of one shape, and the builder's is the one that gets "
                f"overwritten"
            )
    if PP42B_DISCLAIMER not in harness_raw_42:
        pp42b_faults.append(
            f"{HARNESS_AGENT.name} does not state that the report shape is "
            f"router-seeded -- without it the dropped row reads as an omission "
            f"and the next editor puts it back"
        )
    check(
        "PP-42(b)",
        not pp42b_faults,
        f"one writer of the report shape: {n_cp} router `cp` (raw) and "
        f"{n_rows} deliverable rows, none of them a report producer"
        + ("" if not pp42b_faults else " -- " + "; ".join(pp42b_faults)),
    )

    # PP-42(c) -- no QA template cites a gate the QA route does not run,
    # except the two named, reasoned exclusions printed below.
    #
    # STATED PLAINLY, because `<=` plus a full exclusion set looks stronger
    # than it is: after this phase EVERY extracted gate token is excluded, so
    # the membership half (iv) has ZERO live members and cannot fail. All of
    # this property's enforcement power is in (i) the floor, (ii) the no-rot
    # subset, and (iii) the per-line sentence-shape test. (iii) is exactly the
    # assertion that C4's defect -- a gate claimed to read THIS artifact's
    # fields -- cannot reappear, and I-79 injects precisely that. What this
    # does NOT prove is the (iv) branch on a genuinely-missing QA gate; there
    # is no live example to prove it on. Named here rather than discovered.
    pp42c_faults: list[str] = []
    # Every exclusion is REPORTED with its reason on every run -- carried in
    # this check's own detail string rather than a side channel, so a reader
    # of the pass line cannot miss what was excluded and why.
    pp42c_reasons = " | ".join(
        f"EXCLUDED `{gate}`: {reason}"
        for gate, reason in sorted(PP42C_CROSS_ROUTE_GATES.items())
    )
    extracted: set[str] = set()
    gate_lines: dict[str, list[str]] = {}
    for tpl in sorted(PLUGIN.glob("templates/qa-*.template.md")):
        tpl_dec = _decommented(tpl.read_text(encoding="utf-8"))
        for line in tpl_dec.splitlines():
            for tok in PP42C_GATE_TOKEN.findall(line):
                extracted.add(tok)
                gate_lines.setdefault(tok, []).append(f"{tpl.name}: {line.strip()}")
    # (i) floor FIRST. A regex that stopped matching gives `set() <= anything`,
    # vacuously true -- vacuity shape (a), and precisely how C4 comes back.
    if len(extracted) < PP42C_MIN_GATE_TOKENS:
        check(
            "PP-42(c)",
            False,
            f"PRECONDITION failed: extracted {len(extracted)} `*_gate` tokens "
            f"from templates/qa-*.template.md (expected >= "
            f"{PP42C_MIN_GATE_TOKENS}) -- the gate-token regex has stopped "
            f"matching, so every membership result below is vacuous. "
            + pp42c_reasons,
        )
    else:
        # (ii) `<=`, NOT `<`. After this phase the two sets are EQUAL, and
        # `set(a) < set(a)` is False in Python -- a proper-subset assertion is
        # red on a correct tree. The property wanted is "no exclusion names a
        # token the templates no longer contain", which is `<=`.
        orphaned = sorted(set(PP42C_CROSS_ROUTE_GATES) - extracted)
        if orphaned:
            pp42c_faults.append(
                f"exclusion names {orphaned}, absent from the extracted set "
                f"{sorted(extracted)} -- an exclusion list has outlived its "
                f"subject"
            )
        # (iii) each excluded token's OWN physical line attributes it to
        # another route and does not claim it applies to this artifact.
        for gate in sorted(set(PP42C_CROSS_ROUTE_GATES) & extracted):
            for cited in gate_lines[gate]:
                if not PP42C_ROUTE_ATTRIBUTION.search(cited):
                    pp42c_faults.append(
                        f"`{gate}` is excluded, but its line carries no other "
                        f"route's name: {cited[:120]!r} -- the distinguishing "
                        f"feature of a legitimate cross-route citation is "
                        f"naming the other route"
                    )
                claimed = [ph for ph in PP42C_FIRST_PERSON if ph in cited]
                if claimed:
                    pp42c_faults.append(
                        f"`{gate}` is excluded, but its line claims it applies "
                        f"to THIS artifact via {claimed}: {cited[:120]!r} -- "
                        f"that phrase IS C4's defect stated in four words"
                    )
        # (iv) everything not excluded must actually exist on the QA route.
        live = sorted(extracted - set(PP42C_CROSS_ROUTE_GATES))
        dangling = [g for g in live if g not in wf_raw_42]
        if dangling:
            pp42c_faults.append(
                f"{dangling} named in templates/qa-*.template.md but absent "
                f"from {QA_WORKFLOW.name} -- a QA artifact citing a gate the "
                f"QA route does not run"
            )
        check(
            "PP-42(c)",
            not pp42c_faults,
            f"extracted = {sorted(extracted)} (len {len(extracted)} >= "
            f"{PP42C_MIN_GATE_TOKENS}); {len(PP42C_CROSS_ROUTE_GATES)} named "
            f"exclusions, each route-attributed on its own line; "
            f"{len(live)} live token(s) -- the membership half is inert by "
            f"construction and (i)/(ii)/(iii) carry this property. "
            + pp42c_reasons
            + ("" if not pp42c_faults else " -- " + "; ".join(pp42c_faults)),
        )

    # ---- PP-43: pointers that name something that is not there. ----
    # See the PP43* constants for the four defect classes and why (b) is a
    # prefix-consistency clause rather than a resolution clause.

    qa_strategy_md = PLUGIN / "skills" / "qa-strategy" / "SKILL.md"

    # --- PP-43(a). The template table points every artifact at templates/. ---
    pp43a_text = qa_strategy_md.read_text(encoding="utf-8")
    pp43a_starts = PP43A_WINDOW_START.findall(pp43a_text)
    if len(pp43a_starts) != 1:
        check(
            "PP-43(a)",
            False,
            f"PRECONDITION failed: the table anchor matched {len(pp43a_starts)} "
            f"times in {qa_strategy_md.name}, expected exactly 1 -- an anchor "
            f"that stopped matching yields an empty window and every row test "
            f"below passes vacuously",
        )
    else:
        _m = PP43A_WINDOW_START.search(pp43a_text)
        # R9 window semantics: search the end anchor from AFTER the start line.
        _tail = pp43a_text[_m.end():]
        _e = PP43A_WINDOW_END.search(_tail)
        pp43a_window = pp43a_text[_m.start(): _m.end() + (_e.start() if _e else len(_tail))]
        pp43a_rows = []
        for _c1, _c2 in PP43A_ROW.findall(pp43a_window):
            if _c1.strip() == "Artifact" and _c2.strip() == "Template":
                continue  # header
            if set(_c1.strip()) <= {"-"} or set(_c2.strip()) <= {"-"}:
                continue  # separator
            pp43a_rows.append((_c1.strip(), _c2.strip()))
        # Anti-vacuity FIRST: a row regex that stopped matching iterates zero
        # rows and passes. 6 data rows measured; the floor is 6, not 7 -- R9
        # records 7 as the measured-wrong floor.
        if len(pp43a_rows) < PP43A_MIN_ROWS:
            check(
                "PP-43(a)",
                False,
                f"PRECONDITION failed: {len(pp43a_rows)} data rows in the "
                f"{len(pp43a_window.encode('utf-8'))}B (raw) artifact-template "
                f"window of {qa_strategy_md.name} (expected >= "
                f"{PP43A_MIN_ROWS}) -- the row regex has stopped matching, so "
                f"every templates/ test below is vacuous",
            )
        else:
            pp43a_bad = [
                f"{_a} -> {_b!r} is not a {PP43A_TEMPLATE_DIR} path"
                for _a, _b in pp43a_rows
                if PP43A_TEMPLATE_DIR not in _b
            ]
            check(
                "PP-43(a)",
                not pp43a_bad,
                f"{len(pp43a_rows)} data rows (>= {PP43A_MIN_ROWS}) in the "
                f"{len(pp43a_window.encode('utf-8'))}B (raw) artifact-template "
                f"window, anchor matched exactly once; every row names a "
                f"{PP43A_TEMPLATE_DIR} path"
                + ("" if not pp43a_bad else " -- " + "; ".join(pp43a_bad)),
            )

    # --- PP-43(b). Path reachability, plus the ADR-5 prefix-consistency clause. ---
    pp43b_sources = sorted((PLUGIN / "agents").glob(PP43B_AGENT_GLOB)) + [qa_strategy_md]
    # token -> naming source; plus the per-line record the prefix clause needs.
    pp43b_extracted: dict[str, Path] = {}
    pp43b_sites: list[tuple[Path, int, str, str, bool]] = []
    pp43b_banner_lines: list[str] = []
    pp43b_allowed_placeholder_lines: set[tuple[Path, int]] = set()
    for _src in pp43b_sources:
        _lines = _src.read_text(encoding="utf-8").splitlines()
        for _i, _line in enumerate(_lines, 1):
            for _raw in PP43B_PATH_TOKEN.findall(_line):
                _pref = _raw.startswith(PP43B_ROOT_PREFIX)
                _tok = _raw[len(PP43B_ROOT_PREFIX):] if _pref else _raw
                pp43b_extracted.setdefault(_tok, _src)
                pp43b_sites.append((_src, _i, _raw, _tok, _pref))
            # The PLACEHOLDER exclusion is a loan against the banner: record
            # the contiguous `- ` bullet block that follows each banner (at most
            # one blank line between). Delete the banner and the four tokens
            # become live candidates -- red until the four files are written.
            if PP43B_PLACEHOLDER_BANNER in _line:
                pp43b_banner_lines.append(f"{_src.name}:{_i}")
                _j = _i  # 0-based index of the NEXT line
                if _j < len(_lines) and not _lines[_j].strip():
                    _j += 1
                while _j < len(_lines) and _lines[_j].startswith("- "):
                    pp43b_allowed_placeholder_lines.add((_src, _j + 1))
                    _j += 1
    pp43b_templated = sorted(
        _t for _t in pp43b_extracted if any(_x.search(_t) for _x in PP43B_EXCLUDE)
    )
    pp43b_candidates = {
        _t: _s
        for _t, _s in pp43b_extracted.items()
        if _t not in pp43b_templated and _t not in PP43B_PLACEHOLDER_EXCLUSIONS
    }
    pp43b_prefixed_lines = {(_s, _i) for _s, _i, _r, _t, _p in pp43b_sites if _p}
    # Every run prints the four excluded names WITH the banner's file and line.
    pp43b_report = (
        f"PLACEHOLDER exclusions (banner {PP43B_PLACEHOLDER_BANNER} at "
        f"{pp43b_banner_lines or 'NOWHERE'}): "
        f"{sorted(PP43B_PLACEHOLDER_EXCLUSIONS)}"
    )
    pp43b_faults: list[str] = []
    if len(pp43b_extracted) < PP43B_MIN_EXTRACTED:
        check(
            "PP-43(b)",
            False,
            f"PRECONDITION failed: extracted {len(pp43b_extracted)} path-shaped "
            f"tokens from {len(pp43b_sources)} sources (expected >= "
            f"{PP43B_MIN_EXTRACTED}) -- the token regex has stopped matching, so "
            f"every resolution and prefix result below is vacuous. "
            + pp43b_report,
        )
    elif len(pp43b_candidates) < PP43B_MIN_RESOLVED:
        check(
            "PP-43(b)",
            False,
            f"PRECONDITION failed: only {len(pp43b_candidates)} of "
            f"{len(pp43b_extracted)} tokens survive the exclusions (expected >= "
            f"{PP43B_MIN_RESOLVED}) -- the exclusions have widened until nothing "
            f"is left to resolve. " + pp43b_report,
        )
    elif len(pp43b_prefixed_lines) < PP43B_MIN_PREFIXED_LINES:
        check(
            "PP-43(b)",
            False,
            f"PRECONDITION failed: {len(pp43b_prefixed_lines)} source lines carry "
            f"a {PP43B_ROOT_PREFIX} token (expected >= "
            f"{PP43B_MIN_PREFIXED_LINES}) -- the prefix-consistency clause fires "
            f"only on such lines, so it is inert. " + pp43b_report,
        )
    else:
        # (1) An exclusion naming a token the corpus no longer contains is red.
        #     `<=`, not `<`, for the reason spelled out in PP-42(c)(ii).
        _orphaned = sorted(PP43B_PLACEHOLDER_EXCLUSIONS - set(pp43b_extracted))
        if _orphaned:
            pp43b_faults.append(
                f"PLACEHOLDER exclusion names {_orphaned}, absent from the "
                f"extracted set -- an exclusion list has outlived its subject"
            )
        # (2) Every excluded token must sit inside a banner's bullet block.
        for _s, _i, _raw, _tok, _p in pp43b_sites:
            if _tok in PP43B_PLACEHOLDER_EXCLUSIONS and (_s, _i) not in pp43b_allowed_placeholder_lines:
                pp43b_faults.append(
                    f"{_s.name}:{_i} names PLACEHOLDER-excluded `{_tok}` outside "
                    f"any {PP43B_PLACEHOLDER_BANNER} bullet block -- the "
                    f"exclusion is a loan against the banner and the banner is gone"
                )
        # (3) Resolution, against PP-29's three bases.
        pp43b_dangling = []
        for _tok, _s in sorted(pp43b_candidates.items()):
            if not any((_b / _tok).exists() for _b in (repo_root, PLUGIN, _s.parent)):
                pp43b_dangling.append(
                    f"`{_tok}` (named in {_s.name}; resolves under none of repo "
                    f"root, {PLUGIN.name}/, or {_s.parent.name}/)"
                )
        pp43b_faults.extend(pp43b_dangling)
        # (4) ADR-5. Where a line already demonstrates the convention, every
        #     other live token on it must too. Narrow by construction: it never
        #     asks a line with no opinion to acquire one.
        for _s, _i, _raw, _tok, _p in pp43b_sites:
            if _p or (_s, _i) not in pp43b_prefixed_lines:
                continue
            if _tok in pp43b_templated or _tok in PP43B_PLACEHOLDER_EXCLUSIONS:
                continue
            _sib = next(r for (s2, i2, r, t2, p2) in pp43b_sites if p2 and (s2, i2) == (_s, _i))
            pp43b_faults.append(
                f"{_s.name}:{_i} names `{_tok}` bare beside `{_sib}`"
            )
        check(
            "PP-43(b)",
            not pp43b_faults,
            f"{len(pp43b_extracted)} path-shaped tokens from "
            f"{[s.name for s in pp43b_sources]}; {len(pp43b_templated)} templated/"
            f"glob-bearing ({pp43b_templated}); "
            f"{len(PP43B_PLACEHOLDER_EXCLUSIONS)} PLACEHOLDER-excluded, all inside "
            f"the banner block; {len(pp43b_candidates)} candidates all resolve; "
            f"{len(pp43b_prefixed_lines)} lines carry {PP43B_ROOT_PREFIX} and no "
            f"sibling on them is bare. " + pp43b_report
            + ("" if not pp43b_faults else " -- " + "; ".join(pp43b_faults)),
        )

    # --- PP-43(c). No document claims a file does not exist when it does. ---
    # Resolution is by BASENAME via PLUGIN.rglob. Revision 2's plugin-root
    # relative test read C7's two bare basenames as missing and stayed GREEN on
    # the live defect; a CWD-relative Path("plugins/cc10x") would do the same
    # from any directory but the repo root, and this suite is run from three.
    def _pp43c_candidates(text: str) -> list[tuple[str, str]]:
        """-> [(token, sentence)] for tokens in the OBJECT of a do-not-exist clause.

        Scoped to the span AFTER the absence phrase, to the end of its sentence.
        The subject -- the file doing the pointing -- is never a candidate;
        without that scoping a correct citation in the same sentence is flagged.
        """
        out: list[tuple[str, str]] = []
        for _sent in PP43C_SENTENCE_SPLIT.split(text):
            _low = _sent.lower()
            _at = -1
            for _ph in PP43C_ABSENCE_PHRASES:
                _k = _low.find(_ph)
                if _k >= 0:
                    _at = max(_at, _k + len(_ph))
            if _at < 0:
                continue
            for _tok in PP43C_TOKEN.findall(_sent[_at:]):
                out.append((_tok, _sent))
        return out

    pp43c_faults: list[str] = []
    # (1) The pinned fixture, run every invocation, EXACT set equality.
    pp43c_fixture = {tok for tok, _ in _pp43c_candidates(PP43C_SELF_TEST)}
    if pp43c_fixture != PP43C_SELF_TEST_EXPECTED:
        pp43c_faults.append(
            f"SELF-TEST failed: fixture yielded {sorted(pp43c_fixture)}, expected "
            f"{sorted(PP43C_SELF_TEST_EXPECTED)} -- "
            + (
                "candidates were scoped to the whole sentence instead of the "
                "do-not-exist clause"
                if len(pp43c_fixture) > len(PP43C_SELF_TEST_EXPECTED)
                else "the phrase detector or the clause-scoped extractor has "
                "stopped working"
            )
        )
    # (2) Coverage.
    pp43c_bytes = 0
    pp43c_hits = 0
    for _src in pp43b_sources:
        _txt = _src.read_text(encoding="utf-8")
        pp43c_bytes += len(_txt.encode("utf-8"))
        for _tok, _sent in _pp43c_candidates(_txt):
            pp43c_hits += 1
            _base = _tok.rsplit("/", 1)[-1]
            _found = list(PLUGIN.rglob(_base))
            if _found:
                pp43c_faults.append(
                    f"{_src.name} claims `{_tok}` does not exist; resolves at "
                    + ", ".join(
                        str(f.relative_to(PLUGIN)) for f in sorted(_found)[:3]
                    )
                )
    if len(pp43b_sources) < PP43C_MIN_FILES_SCANNED:
        pp43c_faults.append(
            f"PRECONDITION failed: scanned {len(pp43b_sources)} files, expected "
            f">= {PP43C_MIN_FILES_SCANNED} -- the scan has gone quiet"
        )
    check(
        "PP-43(c)",
        not pp43c_faults,
        f"pinned fixture yields exactly {sorted(PP43C_SELF_TEST_EXPECTED)} "
        f"(2 candidates, the subject citation correctly not among them); real "
        f"corpus: {len(pp43b_sources)} files / {pp43c_bytes}B scanned, "
        f"{pp43c_hits} do-not-exist candidate(s) found"
        + ("" if not pp43c_faults else " -- " + "; ".join(pp43c_faults)),
    )

    # --- PP-43(d). A pointer does not promise a capability its target lacks. ---
    pp43d_src = PLUGIN / "skills" / "building" / "references" / "integration-and-live-proof.md"
    pp43d_txt = pp43d_src.read_text(encoding="utf-8")
    pp43d_m = PP43D_CLAUSE.findall(pp43d_txt)
    if len(pp43d_m) != 1:
        check(
            "PP-43(d)",
            False,
            f"PRECONDITION failed: the 'use the ... defined there' clause matched "
            f"{len(pp43d_m)} times in {pp43d_src.name}, expected exactly 1 -- a "
            f"clause that stopped matching promises nothing and passes vacuously",
        )
    else:
        pp43d_nouns = [
            _n.strip()
            for _n in re.split(r",\s*| and ", pp43d_m[0])
            if _n.strip()
        ]
        pp43d_keys = [
            _n[:-1] if _n.endswith("s") and not _n.endswith("ss") else _n
            for _n in pp43d_nouns
        ]
        pp43d_target = qa_strategy_md.read_text(encoding="utf-8")
        if not pp43d_keys:
            check(
                "PP-43(d)",
                False,
                f"PRECONDITION failed: the clause {pp43d_m[0]!r} yielded an empty "
                f"noun list -- nothing is promised, so nothing is checked",
            )
        else:
            pp43d_bad = [
                f"'{_k}' promised by {pp43d_src.name}:"
                f"{pp43d_txt[:pp43d_txt.index(pp43d_m[0])].count(chr(10)) + 1}, "
                f"absent from {qa_strategy_md.parent.name}/{qa_strategy_md.name}"
                for _k in pp43d_keys
                if _k not in pp43d_target
            ]
            check(
                "PP-43(d)",
                not pp43d_bad,
                f"{len(pp43d_keys)} promised capability/ies {pp43d_keys} in "
                f"{pp43d_src.name}'s 'defined there' list, each present in "
                f"{qa_strategy_md.parent.name}/{qa_strategy_md.name}"
                + ("" if not pp43d_bad else " -- " + "; ".join(pp43d_bad)),
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
