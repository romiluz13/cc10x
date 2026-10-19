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
      the `{ts, phase, reason, cycle_number}` shape the audit-backstopped circuit
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
# reader who disagrees must argue with (the paragraph itself: docs/adr holds no QA ADR).
PP30A_TOKENS = (
    "the system under test",
    "a worktree is a different checkout",
    "this paragraph is the decision record",
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
# One token per clause of the ADR-1 argument (design-time name; docs/adr has no such file, the paragraph is the record) that a future editor must actually read. Not
# decoration: each is a distinct cost of the rename, and a block that dropped
# any one of them would read as a style note.
PP31_RATIONALE_TOKENS = (
    "this paragraph is the decision record",
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
# A section number may carry ONE letter suffix (`§6b`, `## 2c.`). Without it
# `§6b` parses as `§6` and resolves against the wrong heading -- or, inside
# the env plan, against a heading that exists, so a citation of a section
# the env plan does not have reads as valid. The negative lookahead keeps
# `§3and` from eating the first letter of a glued word. Keys are strings.
PP40_CITATION = re.compile(r"§(\d+(?:[a-z](?![a-z]))?)")
PP40_HEADING = re.compile(r"^## (\d+[a-z]?)\. (.+)$", re.M)
# Citations whose trailing words describe the citing sentence rather than the
# cited section. Measured; both are correct citations. SET EQUALITY, not
# containment: a citation that JOINS this class is a tokeniser regression, and
# one that LEAVES it is a prose edit nobody recorded. Either way, red. I-92 and
# I-93 are both silent unless this is an equality -- each moves exactly one
# correct citation INTO the class and produces no mismatch at all.
# Re-measured at dcee43c + step 0c: the 8 lines of 0c moved the line from
# 119 to 127 (the citations other comments in this file call `:119`).
# Re-measured at a7e1ef3 + the 0b recall bullet: 127 -> 128.
PP40_UNDESCRIPTIVE = {
    ("qa-workflow.md", 128, "3"),   # "wave count and in the"  vs  ## 3. Build order
    ("qa-workflow.md", 128, "2"),   # "id rollups"             vs  ## 2. Coverage plan
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


def _pp40_order(num: str) -> tuple[int, str]:
    """Numeric order for section keys: `2` < `2c` < `10`."""
    digits = num.rstrip("abcdefghijklmnopqrstuvwxyz")
    return int(digits), num[len(digits):]


def _pp40_headings(path: Path) -> dict[str, str]:
    return {
        m.group(1): m.group(2).strip()
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

# Deliberately outside the guard's default mutation_allowlist ([".cc10x/", "~/.cc10x/qa/topology/"]) —
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
PP43B_MIN_EXTRACTED = 11  # measured 20 at b966c52; P4.T7.2 deleted 5 tokens (4 placeholder references, 1 building-reference path), measured 14, floor 16 -> 11 keeps the same headroom of 3
PP43B_MIN_RESOLVED = 8  # measured 9 at 79a909c (11 at b966c52 before P4C removed two resolvable tokens); headroom 1
# Declared-future files under an explicit **PLACEHOLDER** banner. NAMED, not
# line-ranged: `tools/live_harness_runner.py` shares the fourth bullet's line and
# DOES exist, so a line-range drop would swallow a live token. A declared
# placeholder is not a broken link; an UNdeclared one is. The exclusion is a
# loan against the banner and dies with it -- see the three assertions in the
# check body.
# P4.T7.2 emptied the set: the four references were deleted from qa-strategy
# (plan: delete the pointers to files that do not exist) rather than kept as
# declared-future files, so the loan is repaid. The machinery stays so a future
# declared placeholder is still a named loan against its banner.
PP43B_PLACEHOLDER_EXCLUSIONS: set[str] = set()
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

# --- PP-47: the input space has a non-UI half, and it is enumerated too ---
# The researcher's USER_ACTION_INVENTORY covers what the screen offers. Auth
# roles, flags/config and declared limits change behaviour without appearing on
# the screen; BEHAVIOUR_SURFACE is their unreduced inventory. (a) the contract
# block, (b) the MUST rules, (c) the process step, (d) the feature-map section
# that receives it and the handoff that sends it on.
PP47_W_START = re.compile(r"(?m)^BEHAVIOUR_SURFACE:")
PP47_W_FIELDS = (
    "dimension:",
    "name:",
    "where:",
    "values:",
    "default:",
    "enumerated_from:",
    "complete:",
    "changes:",
)
PP47_DIMENSIONS = ("auth", "flag", "config", "limit")
# measured 535 at f346ebe + this change; headroom 285. The smallest block that
# still carries every pinned token (8 field names + 4 quoted dimensions) is
# 131B, so 250 > 131: a block gutted down to its names goes red.
PP47_W_MIN_BYTES = 250
PP47C_START = re.compile(r"(?m)^2b\. \*\*Build the Behaviour-varying Surface")
PP47C_END = re.compile(r"(?m)^3\. \*\*Extract the system-side flow")
PP47C_TOKENS = (
    "**auth**",
    "**flag / config**",
    "**limit**",
    "MAX_*",
    "Do NOT reduce",
    "GAPS",
)
# measured 1170 at f346ebe + this change; headroom 620 (pinned-token
# skeleton 104B < 550).
PP47C_MIN_BYTES = 550
PP47D_START = re.compile(r"(?m)^## 6b\. Behaviour-varying surface — UNREDUCED$")
PP47D_SECTION_END = re.compile(r"(?m)^## ")
PP47D_S6 = re.compile(r"(?m)^## 6\. ")
PP47D_S7 = re.compile(r"(?m)^## 7\. ")
PP47D_HANDOFF = re.compile(r"(?m)^## 9\. Handoff to the plan")
PP47D_TOKENS = (
    "| Dimension |",
    "Enumerated from",
    "Complete?",
    "Changes what",
    "`BEHAVIOUR_SURFACE`",
    "Do not trim",
    "not_enumerated",
    "almost always wrong",
    "roles are data",
)
# measured 944 at f346ebe + this change; headroom 494 (pinned-token
# skeleton 182B < 450).
PP47D_MIN_BYTES = 450

# --- PP-48: a dimension the env plan fixes is reduced by the test plan, too ---
# PP-47 made BEHAVIOUR_SURFACE an unreduced inventory. Without a reduction
# obligation the env plan still fixes each entry to one value and no scenario
# varies it. (a) the test plan's coverage-by-behaviour-dimension table, (b) the
# env plan's back-reference column, (c) the strategy section that names the
# three dimensions, (d) the qa-plan and qa-plan-review dispatches.
PP48A_S2 = re.compile(r"(?m)^## 2\. Coverage plan")
PP48A_S2C = re.compile(r"(?m)^## 2c\. ")
PP48A_START = re.compile(r"(?m)^### Coverage by behaviour dimension$")
PP48_SECTION_END = re.compile(r"(?m)^### |^## ")
# The ## 2. intro (up to its first ### ) must name both halves of the space
# as ONE sentence: three fragments passed with the conjunction inverted
# ("... §6 rows are the full input space. A scenario may also touch ... §6b").
PP48A_INTRO_TOKENS = (
    "The User Action Inventory (feature map §6) and the Behaviour-varying "
    "surface (feature map §6b) are the full input space.",
)
PP48A_HEADER_CELLS = (
    "Dimension",
    "Entry (feature map §6b)",
    "Space size",
    "Technique",
    "Cases",
    "Leaves uncovered — and why that is acceptable",
)
# first cell of a data row -> a technique that row must name
PP48A_ROWS = {
    "auth": "every-option-once",
    "flag / config": "pairwise",
    "limit": "boundary-values (N-1, N, N+1)",
}
PP48A_TOKENS = (
    "`BEHAVIOUR_SURFACE`",
    "§6b",
    "boundary-values",
    "N-1",
    "full-combinatorial",
    "traceable to scenario rows",
    "`N (S3, S7)`",
    "reconciled with §3's waves and §4's total",
)
# The operative clauses, each line-anchored and required EXACTLY once in the
# window: a phrase pair on one line passed "Not every `BEHAVIOUR_SURFACE` row
# ... appears here exactly once".
PP48A_CLAUSES = (
    re.compile(
        r"(?m)^Every `BEHAVIOUR_SURFACE` row in the feature map's §6b appears "
        r"here exactly once"
    ),
    re.compile(
        r"A dimension the env plan fixes to one value and no scenario varies is "
        r"a constant, and belongs in the `Leaves uncovered` column, not nowhere\."
    ),
)
# measured 1011 at e3e41ac + this change; headroom 361. Raised from 500 after
# the failure hunt grew the pinned-token skeleton to 576B: the floor must sit
# above it, so 650 > 576.
PP48A_MIN_BYTES = 650
PP48B_START = re.compile(r"(?m)^## 2\. Feature flags, settings, and entitlements")
PP48B_END = re.compile(r"(?m)^### Flags that must be OFF")
PP48B_TOKENS = (
    "`BEHAVIOUR_SURFACE`",
    "section 6b",
    "**Every row names the feature-map section 6b entry it fixes.**",
    "is a constant the plan must list as uncovered",
    "is an uncontrolled variable",
)
# measured 1371 at e3e41ac + this change; headroom 721 (pinned-token
# skeleton 227B < 650).
PP48B_MIN_BYTES = 650
PP48C_START = re.compile(
    r"(?m)^### Auth, flags and config, and declared limits are coverage "
    r"dimensions, not setup details$"
)
PP48C_OLD = re.compile(r"(?m)^### Feature flags are a coverage dimension")
PP48C_TOKENS = (
    "`BEHAVIOUR_SURFACE`",
    "**auth**",
    "**flag / config**",
    "**limit**",
    "Each is a dimension to vary, not a constant to set",
    "**Limits take boundary values.**",
    "N-1",
    "N+1",
    "that is a finding rather than a gap",
    "coverage-by-behaviour-dimension table",
    "Flag OFF",
    "Toggled mid-session",
    "**The OFF path is where the expensive incidents live.**",
    "flag-on + entitlement-off",
    "**Confirm a flag applied, do not confirm it was set.**",
)
# measured 2035 at e3e41ac + this change; headroom 1035 (pinned-token
# skeleton 464B after the failure hunt < 1000).
PP48C_MIN_BYTES = 1000
# The group is the description string's BODY, bounded at its closing quote
# (escapes honoured): a sentence moved past the quote on the same physical
# line is outside the string the agent receives.
PP48D_DISPATCH = {
    "qa-plan": re.compile(
        r'(?m)^\s*description: "wf:\{[a-z_]+\}\\nkind:agent\\norigin:router'
        r'\\nphase:qa-plan\\n((?:[^"\\\n]|\\.)*)"'
    ),
    "qa-plan-review": re.compile(
        r'(?m)^\s*description: "wf:\{[a-z_]+\}\\nkind:agent\\norigin:router'
        r'\\nphase:qa-plan-review\\n((?:[^"\\\n]|\\.)*)"'
    ),
}
PP48D_TOKENS = {
    "qa-plan": (
        "Cover the Behaviour-varying surface the same way",
        "every BEHAVIOUR_SURFACE entry in feature-map section 6b",
        "is reduced by a named technique",
        "coverage-by-behaviour-dimension table with what it leaves uncovered stated",
        "limits get boundary values at N-1, N and N+1",
        "every env-plan feature-flag row names the entry it fixes",
        "Never edit product code",
    ),
    "qa-plan-review": (
        "Does every BEHAVIOUR_SURFACE entry in the feature map",
        "appear in the coverage-by-behaviour-dimension table with a named "
        "technique and a stated uncovered remainder",
        "silently fixed to one value by the env plan and never varied",
    ),
}

# ---------------------------------------------------------------- PP-49
# The QA route asked its questions one agent at a time and shipped a test plan
# nobody approved. Step 0c negotiates grants + the approval policy ONCE and
# persists them to `qa.negotiation`; the router halts on the reviewed plan
# under `pending_gate="qa_test_plan_approval"` when the policy is `wait`.
# (a) skeleton shape, (b) policy line + `qa.negotiation` bullet, (c) step 0c,
# (d) the gate paragraph + its probe placement, (e) one vocabulary across all.
PP49_NEGOTIATION_KEYS = (
    "recorded_at",
    "grants",
    "test_plan_approval",
    "users_words",
    "pending_grant",
)
PP49_GRANTS = (
    "mcp_servers",
    "settings_changes",
    "db_access",
    "package_install",
    "service_start",
    "external_network",
    "writes_outside_allowlist",
)
# (b) The pending_gate bullet must be unique and carry the gate list as ONE
# sentence: three tokens scattered over the line passed with "exactly two"
# still in front of them. Re-measured in Phase 4: four gates, the fourth the
# grant gate (`qa_grant_needed`).
PP49B_LINE = re.compile(r"(?m)^- `pending_gate` is required .*QA sets exactly four: .*$")
# The line is pinned WHOLE (prefix + gate sentence): a qualifier inserted in
# the middle of the line ("is required (advisory for QA ...) whenever", Phase 4
# hunt H10) left both the stem regex and the sentence tail intact.
PP49B_LINE_PREFIX = (
    "- `pending_gate` is required whenever BUILD/PLAN/DEBUG/QA/TRIAGE/"
    "CODEBASE-HEALTH is waiting on user clarification, scope selection, or "
    "persistence repair. "
)
PP49B_GATE_SENTENCE = (
    "QA sets exactly four: `qa_preflight_human_prerequisites` (the batched "
    "preflight ask), `qa_source_contradiction` (consolidation found sources "
    "that disagree about what to test), `qa_test_plan_approval` (the "
    "reviewed test plan is on screen and `qa.negotiation.test_plan_approval` "
    "is `wait`) and `qa_grant_needed` (an acting QA agent returned "
    "`GRANT_NEEDED`; the batched grant ask is on screen)."
)
# The bullet is pinned WHOLE (prefix + clauses + final period, whitespace
# normalised): clauses pinned exactly once still passed a trailing sentence
# that re-defined `ask` on the same bullet line (failure hunt H6).
# Re-measured at the Phase 4 REM-FIX on c08b99f: the prefix no longer says
# `written once` -- the grant gate amends `grants` and `pending_grant`.
PP49B_BULLET_PREFIX = (
    '- `qa.negotiation` is created at QA step 0c (a regression run seeds it '
    'from the source QA workflow), amended only by the grant-gate law — '
    '`grants` on an answer, `pending_grant` while a question is open, '
    'whichever gate raised it — and read by every QA dispatch: '
)
# Derived from the prefix, never retyped: it carries `(`, `)`, `.` and `—`.
PP49B_BULLET = re.compile(r"(?m)^" + re.escape(PP49B_BULLET_PREFIX) + r".*$")
PP49B_BULLET_CLAUSES = (
    "`grants` (each `granted | denied | ask`; `ask` means a batched router gate "
    "when first needed, never an agent question)",
    "`test_plan_approval` (`wait | run`)",
    "`users_words` (the user's answer, verbatim)",
    "`recorded_at`",
    "`pending_grant` (the open grant request while the grant gate is raised, "
    "else null)",
)
PP49B_BULLET_TEXT = PP49B_BULLET_PREFIX + ", ".join(PP49B_BULLET_CLAUSES) + "."
PP49B_LINE_TEXT = PP49B_LINE_PREFIX + PP49B_GATE_SENTENCE
# (c) Step 0c sits between 0a and 0b; the anchors are PP-18's own.
PP49C_0A = re.compile(r"(?m)^0a\. \*\*Capability discovery")
PP49C_0B = re.compile(r"(?m)^0b\. \*\*Repo-set enumeration")
PP49C_START = re.compile(r"(?m)^0c\. \*\*Negotiation")
# The step IS these lines: the window's non-blank lines must equal them in
# order. A swapped default (`run` ... the default) or a dropped grant changes a
# pinned line; a seventh bullet laid over the blank line before 0b (line count
# unchanged, failure hunt H3') makes the list longer. No byte floor: equality
# is stricter than any floor could be.
PP49C_LINES = (
    "0c. **Negotiation (ONE `AskUserQuestion`, runs once, after 0a's "
    "measurement and before 0b's on-screen repo set).**",
    "- Propose grants from what 0a measured as **needed** for this run — not "
    "the whole list. A grant nothing will use is noise, and noise is how a "
    "user stops reading the question.",
    "- The grants are `mcp_servers`, `settings_changes`, `db_access`, "
    "`package_install`, `service_start`, `external_network`, "
    "`writes_outside_allowlist`; each answer is `granted | denied | ask`. "
    "`ask` means: when an agent first needs it, it returns `STATUS: BLOCKED` "
    "with `NEXT_ACTION: gate` and the router raises ONE batched question — "
    "never an agent question.",
    "- Ask the approval policy in the same question: `test_plan_approval: "
    "wait` (halt on the reviewed plan — the default) or `run`.",
    "- Persist the answer to `qa.negotiation` NOW: `qa.negotiation.grants`, "
    "`qa.negotiation.test_plan_approval`, `qa.negotiation.users_words` "
    "(verbatim), `qa.negotiation.recorded_at`; append `negotiation_recorded` "
    "to the event log. `JUST_GO` takes the proposed grants and `wait`.",
    "- Every QA agent dispatch after this point carries the `## Grants` block "
    "rendered from `qa.negotiation.grants` (defined under *QA-specific "
    "rules*).",
)
# grant names, read back out of the grants line by regex (never retyped)
PP49C_GRANT_LINE = re.compile(r"(?m)^- The grants are ((?:`[a-z_]+`, )+`[a-z_]+`);")
# (d) The gate paragraph sits after the Pass-1 FINDINGS bullet and before the
# amendment rule, and IS its sentences: the whitespace-normalised window must
# equal them joined by one space. Sentences pinned exactly once plus a floor
# passed a sentence appended inside the paragraph (failure hunt H1).
PP49D_START = re.compile(r"(?m)^\*\*Test-plan approval gate — ")
# File-wide: the heading's stem exactly once, so a second, differently-headed
# gate paragraph ("... gate, fast path — ") cannot sit elsewhere (hunt H4).
PP49D_HEAD_STEM = re.compile(r"(?m)^\*\*Test-plan approval gate")
PP49D_END = re.compile(r"(?m)^\*\*|^#### |^```")
PP49D_AFTER = re.compile(r"(?m)^- \*\*Pass 1 returns `FINDINGS`\*\* ")
PP49D_BEFORE = re.compile(r"(?m)^\*\*An amendment is never self-certified")
PP49D_SENTENCES = (
    '**Test-plan approval gate — `pending_gate="qa_test_plan_approval"`.**',
    "When the last review pass returns `PASS` (pass 1, or pass 2 after an "
    "amendment) and `qa.negotiation.test_plan_approval` is `wait`: present the "
    "plan ON SCREEN — the scenario total with its arithmetic, the waves with "
    "their stop-ifs, every reduction technique from both coverage tables and "
    "what each leaves uncovered, the open contradictions, the env mode and the "
    'real-time cost — set `pending_gate="qa_test_plan_approval"`, raise '
    "exactly one `AskUserQuestion`, and halt.",
    "Do not unblock `qa_preflight_task_id` until the answer is recorded "
    "(`test_plan_approved` in the event log, `pending_gate` cleared).",
    "When the policy is `run`, append `test_plan_approval_skipped` and continue.",
    "The same halt applies in `qa_scope=probe` after `qa-plan` returns, "
    "because the deliverable is the same.",
    "A plan the user never looked at is not an approved plan — the rule the "
    "env plan already lives under.",
)
# The probe graph names the gate in its own section too, as prose (no node).
PP49D_PROBE_START = re.compile(r"(?m)^#### Reduced task graph \(`qa_scope=probe`\)$")
PP49D_PROBE_END = re.compile(r"(?m)^### |^#### ")
PP49D_PROBE_SENTENCE = (
    "The test-plan approval gate is not dropped with the review: after "
    "`qa-plan` returns, preflight is unblocked only after the "
    "`qa_test_plan_approval` gate clears or the policy is `run`."
)
# (e) gate tokens are DERIVED from each surface, never retyped
PP49E_GATE = re.compile(r"qa_[a-z_]+approval")
PP49E_KEY = re.compile(r"^[a-z_]*approval$")
# the grant gate's token, read out of the policy line beside the approval one
PP49E_GRANT = re.compile(r"qa_grant_[a-z_]+")

# ---------------------------------------------------------------- PP-50
# The no-ask rule lived in ONE dispatch of ten (preflight's), and the BLOCKED it
# told agents to return was not in qa-researcher's contract at all. Phase 4
# defines a `## Grants` block once, renders it into every QA-agent dispatch in
# one of two variants (acting / planning), carries the acting duty into the
# three acting contracts, and gives the router a grant gate that consumes it.
# (a) census + partition + per-line tail, (b) one vocabulary per variant,
# (c) agent-file reach, (d) re-qa-execute seeding, (e) the grant gate,
# (f) SKILL.md's optional-sections registry.
PP50_PLACEHOLDER = (
    "{one line per qa.negotiation.grants entry: name: granted|denied|ask}"
)
PP50_BLOCK_HEAD = "\n\n## Grants\n" + PP50_PLACEHOLDER + "\n"
PP50_ACTING_SENTENCE = (
    "Do NOT ask the user anything — act within the grants; outside them "
    'return STATUS: BLOCKED, NEXT_ACTION: "gate", GRANT_NEEDED naming the '
    "grant, and stop."
)
PP50_PLANNING_SENTENCE = (
    "Plan within these grants; they bound what the harness builder may do. "
    "A plan that needs a grant marked denied or ask is an open decision: the "
    "planner returns STATUS: NEEDS_CLARIFICATION naming the grant in "
    "USER_INPUT_NEEDED; the reviewer records it as a FINDING. Neither asks "
    "the user."
)
PP50_ACTING = frozenset(
    {"qa-research", "qa-preflight", "qa-build", "re-qa-build", "qa-execute",
     "re-qa-execute"}
)
PP50_PLANNING = frozenset(
    {"qa-plan", "qa-re-plan", "qa-plan-review", "qa-plan-review-2"}
)
# phase -> the agent its SUBJECT line must name (the dispatch string does not)
PP50_EXCLUDED = {"qa-review": "code-reviewer", "qa-hunt": "failure-hunter"}
PP50_MEMORY = frozenset({"memory-finalize"})
# measured 13 at 024c047; headroom 0 — equal to the pinned partition
# (6 acting + 4 planning + 2 excluded + 1 memory), so it cannot sit below it
PP50_ALL_DISPATCH_MIN = 13
PP50_WF_LINE = re.compile(r'(?m)^[ \t]*description: "wf:')
# Bounded at the string's closing quote: the content is non-quote characters
# or backslash escapes, then `"`, then at most a comma before end of line —
# text appended after the closing quote drops the line out of the census.
PP50_DISPATCH = re.compile(
    r'(?m)^[ \t]*description: "(wf:\{[a-z_]+\}\\nkind:(?:agent|remfix)'
    r'\\norigin:[a-z-]+\\nphase:([a-z0-9-]+)\\n(?:[^"\\\n]|\\.)*)",?[ \t]*$'
)
PP50_MEMORY_LINE = re.compile(
    r'(?m)^[ \t]*description: "wf:\{[a-z_]+\}\\nkind:memory\\norigin:[a-z-]+'
    r'\\nphase:([a-z0-9-]+)\\n(?:[^"\\\n]|\\.)*",?[ \t]*$'
)
PP50_SUBJECT = re.compile(r'^[ \t]*subject: "CC10X ([a-z-]+):')
# (b) the definition paragraph, pinned whole (whitespace-normalised)
PP50B_START = re.compile(r"(?m)^\*\*The `## Grants` block — one vocabulary, one owner\.\*\*")
PP50B_HEAD_STEM = re.compile(r"(?m)^\*\*The `## Grants` block")
PP50_PARA_END = re.compile(r"(?m)^\*\*|^### ")
PP50B_PARAGRAPH = (
    "**The `## Grants` block — one vocabulary, one owner.** Every QA-agent "
    "dispatch carries, after its task text, a `## Grants` section rendered "
    "from `qa.negotiation.grants` — one line per grant, `name: granted | "
    "denied | ask` — followed by ONE of two sentences. **Acting dispatches** "
    "(`qa-research`, `qa-preflight`, `qa-build`, `re-qa-build`, `qa-execute`, "
    "`re-qa-execute` — the agents that touch a machine): `"
    + PP50_ACTING_SENTENCE
    + "` **Planning dispatches** (`qa-plan`, `qa-re-plan`, `qa-plan-review`, "
    "`qa-plan-review-2` — planner and plan-gap-reviewer, read-only): `"
    + PP50_PLANNING_SENTENCE
    + "` **Not QA agents** (`qa-review`, `qa-hunt` — `code-reviewer` and "
    "`failure-hunter` reading the harness): no block; they touch no machine "
    "and ask no one. The sentences live here and in the dispatches only; an "
    "agent file restates the duty, never the wording. The preflight dispatch "
    "used to carry its own version; it now carries the block, so there is "
    "exactly one owner."
)
PP50B_TOKENS = (
    "`qa.negotiation.grants`",
    "`name: granted | denied | ask`",
    "**Acting dispatches**",
    "**Planning dispatches**",
    "**Not QA agents**",
)
# each variant's phase list and sentence are READ BACK out of the paragraph
PP50B_VARIANT = re.compile(
    r"\*\*(Acting dispatches|Planning dispatches|Not QA agents)\*\* "
    r"\(([^)]*)\): ([^*]*)"
)
PP50B_OLD = "let the router raise one batched question"
# (c) the acting duty in each acting agent's own file
PP50C_HEAD = re.compile(r"(?m)^## Grants$")
PP50C_END = re.compile(r"(?m)^## ")
# Re-measured at the Phase 4 REM-FIX on c08b99f: `denied` is no longer a
# gate trigger -- the agent works without it and reports what it blocks.
PP50C_SECTION = "## Grants " + (
    'Your dispatch carries a `## Grants` block recorded at QA step 0c. Act '
    'within it. When you need something it marks `ask`, or something it does '
    'not list, stop and return `STATUS: BLOCKED` with `NEXT_ACTION: "gate"` '
    "and the grant's name in `GRANT_NEEDED` — the router asks the user once, "
    'batched, and re-dispatches you. When you need something it marks '
    '`denied`, the user has already answered: never request it, and never '
    'turn it into a product verdict. Do what you can without it, and record '
    'the work it gates as blocked by the denied grant in the field your '
    'CONTRACT RULES name for it — `GRANT_NEEDED` stays empty and '
    '`NEXT_ACTION` is never `"gate"` for a denied grant. You never ask.'
)
PP50C_YAML_START = re.compile(r"(?m)^```yaml$")
PP50C_YAML_END = re.compile(r"(?m)^```$")
PP50C_CONTRACT_HEAD = re.compile(r"(?m)^### Router Contract \(MACHINE-READABLE\)$")
# Re-measured at the Phase 4 REM-FIX on c08b99f; tuple-valued: each
# sentence is a rule of its own, named by index when it is missing.
PP50C_RULES = {
    "qa-researcher.md": (
        (
            '- `STATUS: BLOCKED` requires `NEXT_ACTION: "gate"` and non-empty '
            '`GRANT_NEEDED`; it is the only way out when a source needs a grant the '
            'block marks ask or does not list. A source a `denied` grant keeps from '
            'you is `SOURCE_COVERAGE: unavailable` (or `partial`) with '
            '`SOURCE_COVERAGE_REASON: "denied grant: <name>"` — a `PASS` under the '
            'coverage rule above, never `BLOCKED`, never `FAIL`. You never ask.'
        ),
    ),
    "qa-executor.md": (
        (
            '- `NEXT_ACTION: "gate"` requires `STATUS: BLOCKED` and non-empty '
            '`GRANT_NEEDED`. Execution stops at the first scenario that needs the '
            'grant; `SCENARIOS_BLOCKED` counts the rest. A scenario that needs a '
            'grant marked `denied` is `status: BLOCKED` with `actual: "denied grant: '
            '<name>"` — the slot an ENVIRONMENT signal lands in, no `failure_class` — '
            'and counts in `SCENARIOS_BLOCKED`, so `STATUS: BLOCKED` by the rule '
            'above, with `GRANT_NEEDED` empty and `NEXT_ACTION: "complete"`: the '
            'report carries it, as it carries ENVIRONMENT; never `"gate"`, never '
            '`FAIL`.'
        ),
    ),
    "qa-harness-builder.md": (
        (
            '- `NEXT_ACTION: "gate"` with empty `GRANT_NEEDED` and empty '
            '`HUMAN_PREREQUISITES` and empty `CURRENCY_GATE` is a contract violation '
            '— a gate names what it waits for. A grant marked `denied` is never a '
            'gate, in either mode: the work it blocks is a `BLOCKED_ITEMS` entry '
            '`denied grant: <name> — <what it blocks>`, `STATUS: BLOCKED`, '
            '`GRANT_NEEDED` empty, `NEXT_ACTION: "abort"` unless something else on '
            'the same return is a gate; such an entry is reported, never requested, '
            'and never escalates `qa_scope`.'
        ),
        (
            '- Non-empty `BLOCKED_ITEMS` or `HUMAN_PREREQUISITES` forces `STATUS: '
            'BLOCKED`, and forces `NEXT_ACTION: gate` unless every `BLOCKED_ITEMS` '
            'entry is a `denied grant: <name>` item and `HUMAN_PREREQUISITES` is '
            'empty (a denied grant is reported, never requested — the gate rule '
            'above). Never `PASS`, never `FAIL` — a missing credential is not a '
            'product failure, and rounding it to either one destroys the distinction '
            'preflight exists to draw.'
        ),
        (
            '- Non-empty `BLOCKED_ITEMS` escalates `qa_scope=probe` to `standard`, '
            'except entries that are `denied grant: <name>` items — a refused grant '
            "is the user's decision, not a scope finding. **Harness mode only** — see "
            'the preflight rule below for why.'
        ),
    ),
}
# The policy's qa-harness-builder validation row says the same as :430.
PP50C_POLICY_ROW_SENTENCE = (
    'Non-empty `BLOCKED_ITEMS` or `HUMAN_PREREQUISITES` forces `STATUS: '
    'BLOCKED`, never `PASS` and never `FAIL`, and forces `NEXT_ACTION: gate` '
    'unless every `BLOCKED_ITEMS` entry is a `denied grant: <name>` item and '
    '`HUMAN_PREREQUISITES` is empty — a denied grant is reported, never '
    'requested.'
)
# (d) the regression run inherits the grants the user already gave
PP50D_START = re.compile(r"(?m)^- \*\*A new QA workflow — not a resume, not a DEBUG task\.\*\*")
PP50D_END = re.compile(r"(?m)^- \*\*|^### |^#### ")
# The bullet is pinned WHOLE: a contradicting sentence inserted before the
# seeding tail left an ends-with test green (Phase 4 hunt H12).
PP50D_BULLET = "- **A new QA workflow — not a resume, not a DEBUG task.** The originating QA workflow ended with `memory_finalized`; its artifact is closed, and reopening it would falsify its own §2 rollups. The DEBUG workflow that fixed the bug is a `DEBUG`-type workflow, and a QA phase cannot run inside it. So the router seeds a fresh QA artifact with `source_wf` pointing at the ORIGINAL QA workflow, and everything the executor needs — the saved test plan, the built harness — resolves through that link. The task is created only after the DEBUG workflow's verification PASS, which is the same precondition as the offer itself. The router seeds the regression artifact's `qa.negotiation` from the source QA workflow, so the `## Grants` block renders from the grants the user already gave."
PP50D_SENTENCE = (
    "The router seeds the regression artifact's `qa.negotiation` from the "
    "source QA workflow, so the `## Grants` block renders from the grants the "
    "user already gave."
)
# (e) the grant gate, pinned whole (whitespace-normalised)
PP50E_START = re.compile(r"(?m)^\*\*The grant gate — ")
PP50E_HEAD_STEM = re.compile(r"(?m)^\*\*The grant gate")
# Re-measured at the Phase 4 REM-FIX on c08b99f: the preflight fold-in, the
# denied answer (no FAIL), the empty-GRANT_NEEDED stop, and the cap-spent
# resolution clause.
PP50E_PARAGRAPH = (
    '**The grant gate — `pending_gate="qa_grant_needed"`.** On `STATUS: '
    'BLOCKED` with `NEXT_ACTION: "gate"` and non-empty `GRANT_NEEDED` from '
    'any acting QA agent: persist `{phase, grants, blocks}` to '
    '`qa.negotiation.pending_grant`, append `grant_requested` to the event '
    'log, set `pending_gate="qa_grant_needed"`, and raise **exactly one** '
    '`AskUserQuestion` naming every grant requested and what each blocks — '
    "batched, as preflight's ask is. When a `qa-preflight` return carries "
    '`GRANT_NEEDED` alongside `HUMAN_PREREQUISITES` or `CURRENCY_GATE` '
    'entries it is still one question: the grant lines fold into the '
    'preflight batched ask under '
    '`pending_gate="qa_preflight_human_prerequisites"` (the `pending_grant` '
    'write and the `grant_requested` event still happen), and the preflight '
    're-dispatch cap counts both — one counter per phase, whichever gate '
    'raised it. On the answer: write each grant into `qa.negotiation.grants` '
    'as `granted` or `denied`, append `grant_recorded`, clear `pending_grant` '
    'and `pending_gate`, and re-dispatch a fresh task of the blocked phase '
    'with the re-rendered `## Grants` block — the preflight pattern, same '
    'cap: **2 re-dispatches per phase, then a `human_action` checkpoint.** A '
    '`denied` answer re-dispatches too; the re-dispatched agent then works '
    'without the grant and records what it blocks the way its contract says — '
    'never a product verdict, never a second request, never a scope finding. '
    "A `BLOCKED` return with empty `GRANT_NEEDED` is not this gate's: the "
    "executor's report carries its blocked scenarios as it does for "
    'ENVIRONMENT, and a harness-builder return blocked by a denied grant '
    'alone (`NEXT_ACTION: "abort"`, nothing to ask) stops at a `human_action` '
    'checkpoint carrying its `BLOCKED_ITEMS` — the plan needs a grant the '
    'user refused, and only the user can change the plan or the grant. On '
    'resolution, re-render the `## Grants` block from `qa.negotiation.grants` '
    'and re-dispatch the same phase (`qa-preflight` or `qa-build`), counted '
    "against that phase's re-dispatch cap — when that cap is already spent at "
    "resolution, stop at the cap's existing `human_action` checkpoint instead "
    'of re-dispatching; when the user changes the plan instead, route '
    '`qa-re-plan`. Any grant the user changes outside this gate — a plan '
    "clarification's answer, or that checkpoint's — is written the same way, "
    '`qa.negotiation.grants` and `grant_recorded`. A request for a grant that '
    'is already `granted` or already `denied` is a contract violation, not a '
    'gate.'
)
# A refused grant is not a scope finding: both escalation statements say so.
PP50E_ESCALATION_SENTENCES = (
    '- Escalation `probe` → `standard` is mandatory when the harness builder '
    'reports non-empty `SCOPE_INCREASES` in **either** mode, or '
    '`BLOCKED_ITEMS` with any entry other than a `denied grant: <name>` item '
    "in **`MODE: harness`** (mirrors BUILD's trivial→full escalation; a "
    'refused grant is not a scope finding). A **preflight** `BLOCKED_ITEMS` '
    'does NOT escalate — see the reduced-graph section.',
    'Escalate to the full graph when the harness builder reports non-empty '
    '`SCOPE_INCREASES` (**either mode**) or `BLOCKED_ITEMS` with any entry '
    'other than a `denied grant: <name>` item (**`MODE: harness` only** — a '
    "refused grant is the user's decision, not a scope finding): create the "
    'plan-review, reviewer, and hunter tasks, re-block the executor on '
    '`[qa_reviewer_task_id, qa_hunter_task_id]`, persist `qa_scope=standard` '
    'and an escalation entry in `status_history`.',
)
PP50E_TOKENS = (
    'pending_gate="qa_grant_needed"',
    "`GRANT_NEEDED`",
    "`qa.negotiation.pending_grant`",
    "`grant_requested`",
    "`grant_recorded`",
    "exactly one",
    "AskUserQuestion",
    "re-dispatch",
    "2 re-dispatches",
    "human_action",
)
# (f) SKILL.md's optional-sections registry, in order: it grew by one
PP50F_START = re.compile(r"(?m)^Optional sections:$")
PP50F_SHAPE = re.compile(r"- `(## [^`]+)` ")
# (b)/(e) both paragraphs live in ### QA-specific rules (hunt H6b/H6c moved them
# out under another heading and every pinned-whole test stayed green)
PP50_RULES_START = re.compile(r"(?m)^### QA-specific rules$")
PP50_RULES_END = re.compile(r"(?m)^### ")
# (a) text that marks a grants block or its sentences, forbidden in the two
# not-QA-agent tasks whatever heading it sits under (hunt H1a/H1b)
PP50A_EXCLUDED_FORBID = (
    "## Grants",
    PP50_PLACEHOLDER,
    "act within the grants",
    "Plan within these grants",
    "GRANT_NEEDED",
    "NEEDS_CLARIFICATION naming the grant",
)
# (c) file-wide no-ask negative over the three acting agents' normative text:
# `AskUserQuestion` never; "ask the user" / "ask directly" only inside the
# pinned ## Grants window or in the listed pre-existing no-ask sentences
# (PP-15(c)'s scope discipline: a benign baseline use is allowed by name, so the
# negative is neither vacuous nor red for the wrong reason). Hunt H8.
PP50C_ASK = re.compile(r"(?i)\bask (?:the user|directly)\b")
PP50C_ASK_ALLOWED = ("**You never ask the user yourself.**",)
PP50F_SECTIONS = (
    "## Pre-Answered Requirements",
    "## Intent Contract",
    "## Research Files",
    "## Research Quality",
    "## Design File",
    "## Planning Review Findings",
    "## Original User Request",
    "## Approved Context Files",
    "## Previous Agent Findings",
    "## QA Bug Context",
    "## Grants",
)
PP50F_BULLET = (
    "- `## Grants` only for QA-agent dispatches (the ten `phase:qa-*` / "
    "`re-qa-*` dispatches to `qa-researcher`, `qa-harness-builder`, "
    "`qa-executor`, `planner` and `plan-gap-reviewer`; never `qa-review` or "
    "`qa-hunt`), rendered from `qa.negotiation.grants` per "
    "`references/qa-workflow.md` *QA-specific rules*; two sentence variants, "
    "acting and planning — the reference is the owner of both."
)

# ---------------------------------------------------------------- PP-51
# The topology record script (scripts/cc10x_qa_topology.py) is the only code
# that reads or writes `<home>/qa/topology/<slug>/topology.md`. Its unit suite
# pins the promises a record cannot show by being read: one slug read, no
# secret-shaped line written, no member removed, a superset run resolved to
# the existing record. A suite nobody runs proves none of that, so PP-51 runs
# it here -- inside the release gate's existing invariants step, with no change
# to the gate's durable suite list -- and refuses a vacuous green: rc 0, an
# empty stderr (every child in the suite captures its output), and a final
# count line at or above the floor.
TOPOLOGY_SCRIPT = SCRIPTS / "cc10x_qa_topology.py"
TOPOLOGY_SUITE = SCRIPTS / "test_cc10x_qa_topology.py"
TOPOLOGY_TPL = PLUGIN / "templates" / "qa-topology.template.md"
PP51_COUNT_LINE = re.compile(r"^topology unit checks: (\d+) passed$")
PP51_MIN_UNIT_CHECKS = 89  # measured 96 at 6a440b9 + this REM-FIX; headroom 7
PP51_SELFTEST_ENV = "CC10X_TOPOLOGY_SELFTEST_FAIL"
PP51_SELFTEST_TAIL = re.compile(r"^topology unit checks: \d+ passed, 1 failed$")
PP52_FIXTURE = PLUGIN / "tests" / "fixtures" / "qa-route-happy-path.json"
PP52_TOPOLOGY_ENTRY = "~/.cc10x/qa/topology/"
PP53A_TOKENS = (
    "Recall the topology record", "cc10x_qa_topology.py", "`results.topology`",
    "`one`", "`none`", "`tie`", "`superset`", "never forked", "`topology_resolved`",
    "derived_slug", "never a human-chosen name",
    "`warnings`", "`corrupt_renamed`", "lexicographically first member",
)
PP53A_ORDER = ("Recall the topology record", "PRESENT the set on screen")
PP53B_START = re.compile(r"(?m)^\*\*Environment topology gate — recall, verify")
PP53B_END = re.compile(r"(?m)^A plan written to a file")
PP53B_TOKENS = (
    "**Recall**", "**Verify**", "**Ask only the deltas**",
    "PRESENT the proposed topology on screen", "explicit confirmation",
    "--status confirmed", "`topology_written`", "freshness hint",
    "bounded evidence checklist", "derived_slug",
    "before the plan-review task is unblocked", "nothing to verify",
    "only the paths the recall's", "verify {slug} --repos",
    "before the `qa-plan` task is dispatched", "`verify` exit 2",
)
PP53B_STEPS = (
    "1. **Recall**", "2. **Verify**", "3. **Ask only the deltas**",
    "4. **PRESENT the proposed topology on screen**", "5. Write `env-plan.md`",
    "6. **Write the record",
)
PP53B_REPOS_RULE = "only the paths the recall's"  # step 2 and step 6: two occurrences
PP53B_MIN_BYTES = 950  # measured 1969 at a7e1ef3 + this change; floor ~50%
PP53C_START = re.compile(r"(?m)^\*\*Before the memory task runs, update the topology record\*\*")
PP53C_END = re.compile(r"(?m)^```")
PP53C_TOKENS = (
    "--status executed", "--corrections", "`topology_written`", "never an agent",
    "never replaces gotchas already in the record", "status: skipped",
)
PP53C_FENCE = "CC10X Memory Update: Persist QA learnings"
PP53C_LAST_SENTENCE = "Router-inline, never an agent."
PP53D_START = re.compile(r"(?m)^### Determining the topology — recall, then verify")
PP53D_END = re.compile(r"(?m)^### ")
PP53D_TOKENS = (
    "Recall", "Verify", "Ask only the deltas", "explicit confirmation",
    "stop when it is exhausted", "ground_truth",
    "Helm", "EXPOSE", "client constructors",
)
PP53D_RUNGS = (
    "(1) compose", "(2) k8s", "(3) Procfile", "(4) Dockerfile", "(5) `*_URL`", "(6) README run",
)
PP53D_MIN_BYTES = 550  # measured 1144 at a7e1ef3 + this change; floor ~50%
PP53E_DOTTED = re.compile(r"`results\.topology\.[a-z_]+`")
PP53F_START = re.compile(r"(?m)^\*\*Rule 1 — planning phases mutate nothing\.\*\*")
PP53F_END = re.compile(r"(?m)^\*\*")
PP53F_TOKEN = "~/.cc10x/qa/topology/"
PP54_README = PLUGIN.parent.parent / "README.md"
PP54_GUIDE = PLUGIN / "skills" / "cc10x-guide" / "SKILL.md"
PP54_FLOW_START = re.compile(r"(?m)^→ Router detects QA intent")
PP54_FLOW_END = re.compile(r"(?m)^$")
PP54_FLOW_TOKENS = ("negotiation", "approval", "~/.cc10x/qa/topology/")
PP54_TREE_LINE = re.compile(r"(?m)^.*\{doc-target-overlay,.*\}\.md$")
PP54_TREE_MEMBER = re.compile(r"qa-topology\.template[,}]")
PP54_TEMPLATE = PLUGIN / "templates" / "qa-topology.template.md"
PP54_ROWS = (
    (
        "cc10x-guide/SKILL.md",
        PP54_GUIDE,
        re.compile(r"(?m)^\| QA \|.*$"),
        re.compile(r"(?m)^\| Intent \| Example triggers \| Shape \|"),
        3,
    ),
    (
        "README.md",
        PP54_README,
        re.compile(r"(?m)^\| 5 \| \*\*QA\*\* \|.*$"),
        re.compile(r"(?m)^\| Priority \| Workflow \| Trigger words \| What happens \|"),
        4,
    ),
)
PP54_ROW_TOKENS = ("behaviour-varying surface", "grants", "approval", "topology")
PP54_FLOW_ORDER = (
    ("negotiation", "topology is recalled"),
    ("topology is recalled", "survey"),
    ("topology is recalled", "provisions the environment"),
)
PP54_AGENT_ROW = re.compile(r"(?m)^\| \*\*qa-researcher\*\* \|.*$")
PP54_AGENT_TOKEN = "behaviour-varying surface"
PP54_FENCE = "```"


def _yaml_enum_offers(line: str, token: str) -> bool:
    """True when a contract-YAML enum line offers `token` as an alternative.

    The trailing YAML comment is dropped and the value split on `|`; a token
    that only appears in a comment ("# BLOCKED retired", hunt H7a/H7b) or
    inside another alternative is not offered.
    """
    value = line.split(":", 1)[1].split("#", 1)[0] if ":" in line else ""
    return token in [alt.strip() for alt in value.split("|")]


def _yaml_offers_grant(line: str) -> bool:
    """True when a GRANT_NEEDED line offers a non-empty list of known grants."""
    value = line.split(":", 1)[1].split("#", 1)[0] if ":" in line else ""
    for alt in (a.strip() for a in value.split("|")):
        names = re.findall(r'"([a-z_]+)"', alt)
        if alt.startswith("[") and alt.endswith("]") and names and all(
            n in PP49_GRANTS for n in names
        ):
            return True
    return False


def load_skeleton() -> tuple[dict, list[str]]:
    """Parse the skeleton with every repeated key, at any depth, reported.

    Plain `json.loads` keeps the LAST of two equal keys, so a gutted
    `"negotiation"` written before the real one parsed clean (failure hunt
    H5). The hook does not raise: a raise here would crash the suite in the
    first fixture builder, before any property could name the fault. Every
    skeleton read goes through this loader; PP-49(a) fails on any repeat.
    """
    repeats: list[str] = []

    def hook(pairs: list[tuple[str, object]]) -> dict:
        seen: set[str] = set()
        for key, _ in pairs:
            if key in seen:
                repeats.append(
                    f"{key!r} repeated in the object with keys {[k for k, _ in pairs]}"
                )
            seen.add(key)
        return dict(pairs)

    data = json.loads(SKELETON.read_text(encoding="utf-8"), object_pairs_hook=hook)
    return data, repeats


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
    project_dir: Path,
    payload: dict,
    tool_payload: dict,
    *,
    extra_env: dict[str, str] | None = None,
    python: str | None = None,
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
    the Bash mkdir probe PP-6 uses. `extra_env` can only SET variables
    (HOME, CC10X_HOME); a case that needs one unset sets it to "".
    `python` picks the interpreter (default: the one running this suite).
    """
    wf_dir = project_dir / ".cc10x" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    wf_file = wf_dir / "wf-test-pp6.json"
    wf_file.write_text(json.dumps(payload))
    try:
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project_dir))
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [python or sys.executable, str(GUARD)],
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
    payload, _ = load_skeleton()
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
    # Section keys keep a one-letter suffix (`6b`): see PP40_CITATION.
    env_headings = set(
        re.findall(r"^## (\d+[a-z]?)\.", ENV_PLAN_TPL.read_text(), re.M)
    )
    bad: list[str] = []
    unresolved = 0
    for path in (ENV_PLAN_TPL, HARNESS_AGENT, QA_WORKFLOW):
        text = path.read_text()
        for m in re.finditer(r"(\w[\w .`-]{0,14}?)?§(\d+(?:[a-z](?![a-z]))?)", text):
            prefix = (m.group(1) or "").lower()
            num = m.group(2)
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

    def _dispatch_lines(text: str) -> dict[str, tuple[str, str]]:
        """Map each `kind:agent|remfix` dispatch's phase to (subject, task).

        `text` is `_decommented` law (the dispatches live in fences). The task
        is the description string DECODED (`\\n` -> newline, `\\"` -> `"`)
        and bounded at its closing quote; the subject is the line directly
        above it, or "" when that line is not a `subject: "CC10X ...` line.
        A phase dispatched twice keeps its last line; PP-50(a) counts both.
        """
        out: dict[str, tuple[str, str]] = {}
        for m in PP50_DISPATCH.finditer(text):
            prev = text[: m.start()].rstrip("\n").rsplit("\n", 1)[-1]
            subject = prev if PP50_SUBJECT.match(prev) else ""
            task = re.sub(
                r"\\(.)",
                lambda e: "\n" if e.group(1) == "n" else e.group(1),
                m.group(1),
            )
            out[m.group(2)] = (subject, task)
        return out

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
    skeleton, skeleton_repeats = load_skeleton()

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
            f"in the shape the audit-backstopped breaker counts "
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
    pp36_skel, _ = load_skeleton()
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

    # P5.T1 retired the NotebookRead probe: the tools reference documents no such
    # tool (Read handles notebooks), so it left READ_TOOLS and the matcher.
    check(
        "PP-38(a)",
        "NotebookRead" not in load_guard().READ_TOOLS,
        "NotebookRead (not a documented tool) is not a READ_TOOLS member",
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
    # vacuously true. 1 entry and 7 required tools measured at this commit.
    if len(pp38_entries) != 1:
        pp38f_ok = False
        pp38f_detail = (
            f"PRECONDITION failed: {len(pp38_entries)} hooks.json entries invoke "
            f"cc10x_qa_isolation_guard.py, expected exactly 1 -- any matcher "
            f"result below is vacuous"
        )
    elif len(pp38_required) < 7:
        pp38f_ok = False
        pp38f_detail = (
            f"PRECONDITION failed: READ_TOOLS | WRITE_TOOLS | {{Bash}} holds "
            f"{len(pp38_required)} tools, expected >= 7 -- the guard's tool sets "
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
                num = cite.group(1)
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
                        m
                        for m in sorted(titles, key=_pp40_order)
                        if m != num and cited & title_tokens[m]
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
    pp43a_rows: list[tuple[str, str]] = []
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
    # P4.T7.1 removed the pointer: the router forbids loading qa-strategy outside
    # the QA route, so the BUILD reference no longer sends a builder there. The
    # property that remains is that neither the pointer nor a "use the ... defined
    # there" promise comes back; a returning clause would again name a target the
    # reader does not load.
    pp43d_src = PLUGIN / "skills" / "building" / "references" / "integration-and-live-proof.md"
    pp43d_txt = pp43d_src.read_text(encoding="utf-8")
    pp43d_m = PP43D_CLAUSE.findall(pp43d_txt)
    pp43d_bad = []
    if pp43d_m:
        pp43d_bad.append(f"'use the ... defined there' clause {pp43d_m!r} is back")
    if "qa-strategy" in pp43d_txt:
        pp43d_bad.append("the file names qa-strategy again")
    check(
        "PP-43(d)",
        not pp43d_bad,
        f"{pp43d_src.name} carries no 'defined there' promise and no qa-strategy pointer"
        + ("" if not pp43d_bad else " -- " + "; ".join(pp43d_bad)),
    )

    # ---------------------------------------------------------------- PP-47
    # The input space is enumerated on both sides: what the screen offers
    # (USER_ACTION_INVENTORY) and what changes behaviour without being shown
    # (BEHAVIOUR_SURFACE). Every window reuses `_pp41_window` (start exactly
    # once, end searched after the start) and prints its byte size.
    pp47_researcher_raw = RESEARCHER_AGENT.read_text(encoding="utf-8")
    pp47_researcher_dec = _decommented(pp47_researcher_raw)

    # PP-47(a) -- the contract block carries attribution fields and the enum.
    pp47a_faults: list[str] = []
    pp47_w, pp47_w_fault = _pp41_window(
        pp47_researcher_dec, PP47_W_START, PP41_W4_END, "BEHAVIOUR_SURFACE block"
    )
    if pp47_w_fault:
        pp47a_faults.append(pp47_w_fault)
    else:
        if len(pp47_w.encode("utf-8")) < PP47_W_MIN_BYTES:
            pp47a_faults.append(
                f"block is {len(pp47_w.encode('utf-8'))}B, floor "
                f"{PP47_W_MIN_BYTES}B -- the fields have been cut"
            )
        missing = [t for t in PP47_W_FIELDS if t not in pp47_w]
        missing += [f'"{d}"' for d in PP47_DIMENSIONS if f'"{d}"' not in pp47_w]
        if missing:
            pp47a_faults.append(f"block omits {missing}")
    check(
        "PP-47(a)",
        not pp47a_faults,
        f"{RESEARCHER_AGENT.name} BEHAVIOUR_SURFACE block "
        f"{len(pp47_w.encode('utf-8'))}B (floor {PP47_W_MIN_BYTES}B), "
        f"{len(PP47_W_FIELDS)} fields + {len(PP47_DIMENSIONS)} dimension values"
        + ("" if not pp47a_faults else " -- " + "; ".join(pp47a_faults)),
    )

    # PP-47(b) -- the MUST rules name the key: attribution and no pre-reduction.
    pp47b_faults: list[str] = []
    pp47_w9, pp47_w9_fault = _pp41_window(
        pp47_researcher_dec,
        PP41_CONTRACT_RULES,
        PP41_SECTION_END,
        "W9 (qa-researcher CONTRACT RULES)",
        end_optional=True,
    )
    pp47b_bt = pp47_w9.count("`BEHAVIOUR_SURFACE`")
    pp47b_bare = pp47_w9.count("BEHAVIOUR_SURFACE")
    if pp47_w9_fault:
        pp47b_faults.append(pp47_w9_fault)
    else:
        if pp47b_bt < 2:
            pp47b_faults.append(
                f"backticked `BEHAVIOUR_SURFACE` appears {pp47b_bt}x (need >= 2)"
            )
        if pp47b_bare < 3:
            pp47b_faults.append(
                f"BEHAVIOUR_SURFACE appears {pp47b_bare}x (need >= 3)"
            )
        # The count above cannot tell the empty-surface rule from its inverse;
        # the operative clause must sit on the line that names the empty list.
        if not any(
            "BEHAVIOUR_SURFACE: []" in ln and "MUST be explained in `GAPS`" in ln
            for ln in pp47_w9.splitlines()
        ):
            pp47b_faults.append(
                "no line names `BEHAVIOUR_SURFACE: []` and 'MUST be explained "
                "in `GAPS`' -- the empty-surface rule is gone or inverted"
            )
        if "Do NOT pre-reduce `BEHAVIOUR_SURFACE`" not in pp47_w9:
            pp47b_faults.append("no 'Do NOT pre-reduce `BEHAVIOUR_SURFACE`' rule")
        if not any(
            "BEHAVIOUR_SURFACE" in ln
            and "MUST set `enumerated_from` and `complete`" in ln
            for ln in pp47_w9.splitlines()
        ):
            pp47b_faults.append(
                "no line names BEHAVIOUR_SURFACE and 'MUST set `enumerated_from` "
                "and `complete`'"
            )
    check(
        "PP-47(b)",
        not pp47b_faults,
        f"{RESEARCHER_AGENT.name} CONTRACT RULES {len(pp47_w9.encode('utf-8'))}B: "
        f"`BEHAVIOUR_SURFACE` x{pp47b_bt}, BEHAVIOUR_SURFACE x{pp47b_bare}"
        + ("" if not pp47b_faults else " -- " + "; ".join(pp47b_faults)),
    )

    # PP-47(c) -- the process step is normative law, not a comment or a fence.
    pp47c_faults: list[str] = []
    pp47c_w, pp47c_fault = _pp41_window(
        _normative(pp47_researcher_raw), PP47C_START, PP47C_END, "step 2b"
    )
    if pp47c_fault:
        pp47c_faults.append(pp47c_fault)
    else:
        if len(pp47c_w.encode("utf-8")) < PP47C_MIN_BYTES:
            pp47c_faults.append(
                f"step 2b is {len(pp47c_w.encode('utf-8'))}B, floor "
                f"{PP47C_MIN_BYTES}B"
            )
        missing = [t for t in PP47C_TOKENS if t not in pp47c_w]
        if missing:
            pp47c_faults.append(f"step 2b omits {missing}")
    check(
        "PP-47(c)",
        not pp47c_faults,
        f"{RESEARCHER_AGENT.name} normative step 2b "
        f"{len(pp47c_w.encode('utf-8'))}B (floor {PP47C_MIN_BYTES}B), "
        f"{len(PP47C_TOKENS)} tokens"
        + ("" if not pp47c_faults else " -- " + "; ".join(pp47c_faults)),
    )

    # PP-47(d) -- the feature map has a §6b to receive it, and §9 hands it on.
    pp47d_faults: list[str] = []
    pp47_fm = _decommented(QA_FEATURE_MAP_TPL.read_text(encoding="utf-8"))
    pp47d_w, pp47d_fault = _pp41_window(
        pp47_fm, PP47D_START, PP47D_SECTION_END, "§6b"
    )
    if pp47d_fault:
        pp47d_faults.append(pp47d_fault)
    else:
        pos = pp47_fm.find(pp47d_w)
        m6 = PP47D_S6.search(pp47_fm)
        m7 = PP47D_S7.search(pp47_fm)
        if not (m6 and m7 and m6.start() < pos < m7.start()):
            pp47d_faults.append("§6b does not sit between ## 6. and ## 7.")
        if len(pp47d_w.encode("utf-8")) < PP47D_MIN_BYTES:
            pp47d_faults.append(
                f"§6b is {len(pp47d_w.encode('utf-8'))}B, floor {PP47D_MIN_BYTES}B"
            )
        missing = [t for t in PP47D_TOKENS if t not in pp47d_w]
        if missing:
            pp47d_faults.append(f"§6b omits {missing}")
    pp47d_h, pp47d_h_fault = _pp41_window(
        pp47_fm, PP47D_HANDOFF, PP47D_SECTION_END, "§9 handoff", end_optional=True
    )
    if pp47d_h_fault:
        pp47d_faults.append(pp47d_h_fault)
    elif "§6b" not in pp47d_h:
        pp47d_faults.append("§9 handoff never names §6b")
    check(
        "PP-47(d)",
        not pp47d_faults,
        f"{QA_FEATURE_MAP_TPL.name} §6b {len(pp47d_w.encode('utf-8'))}B "
        f"(floor {PP47D_MIN_BYTES}B), {len(PP47D_TOKENS)} tokens; §9 "
        f"{len(pp47d_h.encode('utf-8'))}B"
        + ("" if not pp47d_faults else " -- " + "; ".join(pp47d_faults)),
    )

    # ---------------------------------------------------------------- PP-48
    # The surface PP-47 enumerates is reduced on purpose: the test plan names a
    # technique per dimension and what it leaves uncovered, the env plan names
    # the entry each fixed value belongs to, the strategy skill teaches the
    # three dimensions, and both planning dispatches carry the duty.
    def _pp48_cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("|").split("|")]

    def _pp48_table(window: str) -> list[str]:
        return [ln for ln in window.splitlines() if ln.lstrip().startswith("|")]

    # PP-48(a) -- the test plan reduces every dimension by a named technique.
    pp48a_faults: list[str] = []
    pp48_tp = _decommented(QA_TEST_PLAN_TPL.read_text(encoding="utf-8"))
    pp48a_intro, pp48a_intro_fault = _pp41_window(
        pp48_tp, PP48A_S2, re.compile(r"(?m)^### "), "## 2. intro"
    )
    if pp48a_intro_fault:
        pp48a_faults.append(pp48a_intro_fault)
    else:
        missing = [t for t in PP48A_INTRO_TOKENS if t not in pp48a_intro]
        if missing:
            pp48a_faults.append(f"## 2. intro omits {missing}")
    pp48a_w, pp48a_fault = _pp41_window(
        pp48_tp, PP48A_START, PP48_SECTION_END, "### Coverage by behaviour dimension"
    )
    if pp48a_fault:
        pp48a_faults.append(pp48a_fault)
    else:
        pos = pp48_tp.find(pp48a_w)
        m2 = PP48A_S2.search(pp48_tp)
        m2c = PP48A_S2C.search(pp48_tp)
        if not (m2 and m2c and m2.start() < pos < m2c.start()):
            pp48a_faults.append("the section does not sit inside ## 2. (before ## 2c.)")
        if len(pp48a_w.encode("utf-8")) < PP48A_MIN_BYTES:
            pp48a_faults.append(
                f"section is {len(pp48a_w.encode('utf-8'))}B, floor "
                f"{PP48A_MIN_BYTES}B"
            )
        rows = _pp48_table(pp48a_w)
        header = _pp48_cells(rows[0]) if rows else []
        if header != list(PP48A_HEADER_CELLS):
            pp48a_faults.append(
                f"table header is {header}, not exactly {list(PP48A_HEADER_CELLS)}"
            )
        # The technique must sit IN the Technique column, not anywhere on the row.
        ti = header.index("Technique") if "Technique" in header else -1
        by_first = {_pp48_cells(r)[0]: _pp48_cells(r) for r in rows[2:]}
        for first, technique in PP48A_ROWS.items():
            cells = by_first.get(first)
            if cells is None:
                pp48a_faults.append(f"no '{first}' row")
            elif ti < 0 or ti >= len(cells) or technique not in cells[ti]:
                got = cells[ti] if 0 <= ti < len(cells) else None
                pp48a_faults.append(
                    f"'{first}' row's Technique cell is {got!r}, not one naming "
                    f"'{technique}'"
                )
        missing = [t for t in PP48A_TOKENS if t not in pp48a_w]
        if missing:
            pp48a_faults.append(f"section omits {missing}")
        for rx in PP48A_CLAUSES:
            n = len(rx.findall(pp48a_w))
            if n != 1:
                pp48a_faults.append(
                    f"operative clause {rx.pattern!r} matched {n}x (need exactly 1)"
                )
    check(
        "PP-48(a)",
        not pp48a_faults,
        f"{QA_TEST_PLAN_TPL.name} ### Coverage by behaviour dimension "
        f"{len(pp48a_w.encode('utf-8'))}B (floor {PP48A_MIN_BYTES}B), "
        f"{len(PP48A_HEADER_CELLS)} header cells, {len(PP48A_ROWS)} rows, "
        f"{len(PP48A_TOKENS)} tokens, {len(PP48A_CLAUSES)} clauses; ## 2. intro "
        f"{len(pp48a_intro.encode('utf-8'))}B"
        + ("" if not pp48a_faults else " -- " + "; ".join(pp48a_faults)),
    )

    # PP-48(b) -- every env-plan flag row names the feature-map entry it fixes.
    pp48b_faults: list[str] = []
    pp48b_env = _decommented(ENV_PLAN_TPL.read_text(encoding="utf-8"))
    pp48b_w, pp48b_fault = _pp41_window(
        pp48b_env,
        PP48B_START,
        PP48B_END,
        "env plan ## 2.",
    )
    if pp48b_fault:
        pp48b_faults.append(pp48b_fault)
    else:
        if len(pp48b_w.encode("utf-8")) < PP48B_MIN_BYTES:
            pp48b_faults.append(
                f"## 2. is {len(pp48b_w.encode('utf-8'))}B, floor {PP48B_MIN_BYTES}B"
            )
        rows = _pp48_table(pp48b_w)
        header = _pp48_cells(rows[0]) if rows else []
        if not header or header[-1] != "Feature-map entry":
            pp48b_faults.append(
                f"table header's last cell is {header[-1:]!r}, not 'Feature-map entry'"
            )
        widths = sorted({len(_pp48_cells(r)) for r in rows})
        if len(rows) < 3 or len(widths) != 1:
            pp48b_faults.append(
                f"{len(rows)} table rows with cell counts {widths} -- header, "
                f"separator and example row must all carry the column"
            )
        missing = [t for t in PP48B_TOKENS if t not in pp48b_w]
        if missing:
            pp48b_faults.append(f"## 2. omits {missing}")
        if "§6b" in pp48b_w:
            pp48b_faults.append(
                "## 2. writes §6b -- PP-9/PP-40 resolve § against the env plan; "
                "write 'section 6b'"
            )
    # Whole file, not only ## 2.: PP-9 resolves a bare env-plan §N against the
    # env plan only when nothing precedes it, so "(cross-check §6b)" anywhere
    # else is skipped there and must be caught here.
    pp48b_glyph = [
        i for i, ln in enumerate(pp48b_env.splitlines(), 1) if "§6b" in ln
    ]
    if pp48b_glyph:
        pp48b_faults.append(
            f"env plan writes §6b at decommented line(s) {pp48b_glyph} -- the env "
            f"plan has no 6b section; write 'feature-map section 6b'"
        )
    check(
        "PP-48(b)",
        not pp48b_faults,
        f"{ENV_PLAN_TPL.name} ## 2. {len(pp48b_w.encode('utf-8'))}B "
        f"(floor {PP48B_MIN_BYTES}B), {len(PP48B_TOKENS)} tokens, §6b forbidden file-wide"
        + ("" if not pp48b_faults else " -- " + "; ".join(pp48b_faults)),
    )

    # PP-48(c) -- the strategy skill teaches all three dimensions as normative law.
    pp48c_faults: list[str] = []
    pp48c_norm = _normative(qa_strategy_md.read_text(encoding="utf-8"))
    pp48c_w, pp48c_fault = _pp41_window(
        pp48c_norm, PP48C_START, PP48_SECTION_END, "qa-strategy dimensions section"
    )
    if pp48c_fault:
        pp48c_faults.append(pp48c_fault)
    else:
        if len(pp48c_w.encode("utf-8")) < PP48C_MIN_BYTES:
            pp48c_faults.append(
                f"section is {len(pp48c_w.encode('utf-8'))}B, floor "
                f"{PP48C_MIN_BYTES}B"
            )
        missing = [t for t in PP48C_TOKENS if t not in pp48c_w]
        if missing:
            pp48c_faults.append(f"section omits {missing}")
    if PP48C_OLD.search(pp48c_norm):
        pp48c_faults.append("the flags-only heading is still there beside it")
    check(
        "PP-48(c)",
        not pp48c_faults,
        f"{qa_strategy_md.name} normative dimensions section "
        f"{len(pp48c_w.encode('utf-8'))}B (floor {PP48C_MIN_BYTES}B), "
        f"{len(PP48C_TOKENS)} tokens"
        + ("" if not pp48c_faults else " -- " + "; ".join(pp48c_faults)),
    )

    # PP-48(d) -- the qa-plan and qa-plan-review dispatches carry the duty.
    # The dispatches live in ```text fences: the basis is `_decommented`.
    pp48d_faults: list[str] = []
    pp48d_wf = _decommented(QA_WORKFLOW.read_text(encoding="utf-8"))
    for phase, rx in PP48D_DISPATCH.items():
        bodies = rx.findall(pp48d_wf)
        if len(bodies) != 1:
            pp48d_faults.append(
                f"PRECONDITION failed: {phase} dispatch matched {len(bodies)} "
                f"times (expected exactly 1)"
            )
            continue
        # tokens are searched in the string body only, never past its quote
        missing = [t for t in PP48D_TOKENS[phase] if t not in bodies[0]]
        if missing:
            pp48d_faults.append(f"{phase} dispatch omits {missing}")
    check(
        "PP-48(d)",
        not pp48d_faults,
        f"{QA_WORKFLOW.name} dispatches "
        + ", ".join(f"{p} ({len(t)} tokens)" for p, t in PP48D_TOKENS.items())
        + " inside each description string"
        + ("" if not pp48d_faults else " -- " + "; ".join(pp48d_faults)),
    )

    # ---------------------------------------------------------------- PP-49
    # One negotiation at step 0c, persisted to `qa.negotiation`, and a router
    # halt on the reviewed plan when the policy is `wait`.
    # PP-49(a) -- the skeleton carries the negotiation state at its defaults.
    pp49a_faults: list[str] = []
    if skeleton_repeats:
        pp49a_faults.append(
            f"the skeleton repeats a key (json keeps the last copy): {skeleton_repeats}"
        )
    pp49_neg = skeleton.get("qa", {}).get("negotiation")
    if not isinstance(pp49_neg, dict):
        pp49a_faults.append("qa.negotiation is absent or not an object")
        pp49_neg = {}
    else:
        if list(pp49_neg) != list(PP49_NEGOTIATION_KEYS):
            pp49a_faults.append(
                f"qa.negotiation keys are {list(pp49_neg)}, not exactly "
                f"{list(PP49_NEGOTIATION_KEYS)}"
            )
        grants = pp49_neg.get("grants")
        if not isinstance(grants, dict) or list(grants) != list(PP49_GRANTS):
            pp49a_faults.append(
                f"qa.negotiation.grants keys are "
                f"{list(grants) if isinstance(grants, dict) else grants!r}, not "
                f"exactly {list(PP49_GRANTS)}"
            )
        else:
            not_ask = {k: v for k, v in grants.items() if v != "ask"}
            if not_ask:
                pp49a_faults.append(f"grants not defaulted to 'ask': {not_ask}")
        if pp49_neg.get("test_plan_approval") != "wait":
            pp49a_faults.append(
                f"test_plan_approval default is "
                f"{pp49_neg.get('test_plan_approval')!r}, not 'wait'"
            )
        for k in ("recorded_at", "users_words", "pending_grant"):
            if k in pp49_neg and pp49_neg[k] is not None:
                pp49a_faults.append(f"{k} default is {pp49_neg[k]!r}, not null")
    check(
        "PP-49(a)",
        not pp49a_faults,
        f"{SKELETON.name} qa.negotiation: {len(PP49_NEGOTIATION_KEYS)} keys, "
        f"{len(PP49_GRANTS)} grants at 'ask', test_plan_approval 'wait', "
        f"3 nulls, no repeated key at any depth"
        + ("" if not pp49a_faults else " -- " + "; ".join(pp49a_faults)),
    )

    # PP-49(b) -- the policy names the third gate and documents qa.negotiation.
    pp49b_faults: list[str] = []
    pp49_policy = _normative(HOOK_POLICY.read_text(encoding="utf-8"))
    pp49b_lines = PP49B_LINE.findall(pp49_policy)
    pp49b_line = pp49b_lines[0] if len(pp49b_lines) == 1 else ""
    if len(pp49b_lines) != 1:
        pp49b_faults.append(
            f"PRECONDITION failed: the pending_gate line {PP49B_LINE.pattern!r} "
            f"matched {len(pp49b_lines)} times (expected exactly 1)"
        )
    else:
        # the gate sentence is the LAST thing on the line: a sentence after it
        # ("The third is advisory ...", hunt H2) qualifies all three away
        if " ".join(pp49b_line.split()) != " ".join(PP49B_LINE_TEXT.split()):
            pp49b_faults.append(
                "the pending_gate line is not exactly the pinned line"
                + (" (the four-gate sentence is not its tail, carried once)"
                   if pp49b_line.count(PP49B_GATE_SENTENCE) != 1
                   or not pp49b_line.rstrip().endswith(PP49B_GATE_SENTENCE)
                   else " (something was added before the gate sentence)")
            )
        for stale in ("exactly two", "exactly three"):
            if stale in pp49b_line:
                pp49b_faults.append(f"the pending_gate line still says {stale!r}")
    pp49b_bullets = PP49B_BULLET.findall(pp49_policy)
    pp49b_bullet = pp49b_bullets[0] if len(pp49b_bullets) == 1 else ""
    if len(pp49b_bullets) != 1:
        pp49b_faults.append(
            f"PRECONDITION failed: the qa.negotiation bullet "
            f"{PP49B_BULLET.pattern!r} matched {len(pp49b_bullets)} times "
            f"(expected exactly 1)"
        )
    else:
        if " ".join(pp49b_bullet.split()) != " ".join(PP49B_BULLET_TEXT.split()):
            bad = [c for c in PP49B_BULLET_CLAUSES if pp49b_bullet.count(c) != 1]
            pp49b_faults.append(
                "the qa.negotiation bullet is not exactly the pinned bullet"
                + (f" (clauses not present exactly once: {bad})" if bad else
                   " (every clause present: something was added or reordered)")
            )
    check(
        "PP-49(b)",
        not pp49b_faults,
        f"{HOOK_POLICY.name}: pending_gate line {len(pp49b_line)}B pinned whole "
        f"(four-gate sentence), qa.negotiation bullet {len(pp49b_bullet)}B with "
        f"{len(PP49B_BULLET_CLAUSES)} clauses, pinned whole"
        + ("" if not pp49b_faults else " -- " + "; ".join(pp49b_faults)),
    )

    # PP-49(c) -- step 0c negotiates once, between 0a and 0b.
    pp49c_faults: list[str] = []
    pp49_wf_norm = _normative(QA_WORKFLOW.read_text(encoding="utf-8"))
    pp49c_w, pp49c_fault = _pp41_window(
        pp49_wf_norm, PP49C_START, PP49C_0B, "step 0c"
    )
    if pp49c_fault:
        pp49c_faults.append(pp49c_fault)
    else:
        m_a = PP49C_0A.search(pp49_wf_norm)
        m_c = PP49C_START.search(pp49_wf_norm)
        m_bs = PP49C_0B.findall(pp49_wf_norm)
        m_b = PP49C_0B.search(pp49_wf_norm)
        if not (m_a and m_b and len(m_bs) == 1 and m_a.start() < m_c.start() < m_b.start()):
            pp49c_faults.append(
                f"0c is not between 0a and 0b (0a@{m_a.start() if m_a else -1}, "
                f"0c@{m_c.start()}, 0b x{len(m_bs)}@{m_b.start() if m_b else -1})"
            )
        got = [ln for ln in pp49c_w.splitlines() if ln.strip()]
        if got != list(PP49C_LINES):
            first = next(
                (i for i, (g, w) in enumerate(zip(got, PP49C_LINES)) if g != w),
                min(len(got), len(PP49C_LINES)),
            )
            seen = got[first][:70] if first < len(got) else "<end of step>"
            pp49c_faults.append(
                f"step 0c has {len(got)} non-blank lines, not the "
                f"{len(PP49C_LINES)} pinned; first difference at line {first}: "
                f"{seen!r}"
            )
        gl = PP49C_GRANT_LINE.findall(pp49c_w)
        named = tuple(re.findall(r"`([a-z_]+)`", gl[0])) if len(gl) == 1 else ()
        if named != PP49_GRANTS:
            pp49c_faults.append(
                f"step 0c names grants {list(named)}, not {list(PP49_GRANTS)} "
                f"(the list PP-49(a) holds the skeleton to)"
            )
    check(
        "PP-49(c)",
        not pp49c_faults,
        f"{QA_WORKFLOW.name} normative step 0c {len(pp49c_w.encode('utf-8'))}B "
        f"between 0a and 0b, exactly the {len(PP49C_LINES)} pinned lines, "
        f"grant list read back equal to PP-49(a)'s"
        + ("" if not pp49c_faults else " -- " + "; ".join(pp49c_faults)),
    )

    # PP-49(d) -- the router halts on the reviewed plan, in both graphs.
    pp49d_faults: list[str] = []
    pp49d_w, pp49d_fault = _pp41_window(
        pp49_wf_norm, PP49D_START, PP49D_END, "test-plan approval gate"
    )
    if pp49d_fault:
        pp49d_faults.append(pp49d_fault)
    else:
        m_g = PP49D_START.search(pp49_wf_norm)
        m_after = PP49D_AFTER.findall(pp49_wf_norm)
        m_bef = PP49D_BEFORE.findall(pp49_wf_norm)
        a = PP49D_AFTER.search(pp49_wf_norm)
        b = PP49D_BEFORE.search(pp49_wf_norm)
        if not (
            len(m_after) == 1 and len(m_bef) == 1
            and a.start() < m_g.start() < b.start()
        ):
            pp49d_faults.append(
                "the gate paragraph does not sit after the Pass-1 FINDINGS "
                "bullet and before the amendment rule"
            )
        if " ".join(pp49d_w.split()) != " ".join(PP49D_SENTENCES):
            bad = [s[:60] for s in PP49D_SENTENCES if pp49d_w.count(s) != 1]
            pp49d_faults.append(
                "the gate paragraph is not exactly the pinned sentences"
                + (f" (not present exactly once: {bad})" if bad else
                   " (every sentence present: something was added or reordered)")
            )
    pp49d_heads = PP49D_HEAD_STEM.findall(pp49_wf_norm)
    if len(pp49d_heads) != 1:
        pp49d_faults.append(
            f"'**Test-plan approval gate' heads {len(pp49d_heads)} paragraphs "
            f"in {QA_WORKFLOW.name} (need exactly 1)"
        )
    pp49d_p, pp49d_p_fault = _pp41_window(
        pp49_wf_norm, PP49D_PROBE_START, PP49D_PROBE_END, "reduced task graph"
    )
    if pp49d_p_fault:
        pp49d_faults.append(pp49d_p_fault)
    elif pp49d_p.count(PP49D_PROBE_SENTENCE) != 1:
        pp49d_faults.append(
            "the reduced task graph does not name the gate's probe placement "
            "exactly once"
        )
    check(
        "PP-49(d)",
        not pp49d_faults,
        f"{QA_WORKFLOW.name} normative gate paragraph "
        f"{len(pp49d_w.encode('utf-8'))}B is exactly its "
        f"{len(PP49D_SENTENCES)} pinned sentences, heading unique file-wide; "
        f"reduced task graph names the gate"
        + ("" if not pp49d_faults else " -- " + "; ".join(pp49d_faults)),
    )

    # The grant gate's window is PP-50(e)'s; it is sliced here because PP-49(e)
    # confines the grant token to it, and PP-50(e) reuses the slice.
    pp50e_w, pp50e_fault = _pp41_window(
        pp49_wf_norm, PP50E_START, PP50_PARA_END, "grant gate"
    )

    # PP-49(e) -- one vocabulary: the gate token and the policy key, each read
    # out of its own surface by regex, agree across skeleton, policy, router.
    pp49e_faults: list[str] = []
    pp49e_keys = [k for k in pp49_neg if PP49E_KEY.match(k)]
    pp49e_key = pp49e_keys[0] if len(pp49e_keys) == 1 else None
    pp49e_tokens = {
        "policy line": set(PP49E_GATE.findall(pp49b_line)),
        "gate paragraph": set(PP49E_GATE.findall(pp49d_w)),
        "reduced task graph": set(PP49E_GATE.findall(pp49d_p)),
    }
    for where, toks in pp49e_tokens.items():
        if len(toks) != 1:
            pp49e_faults.append(f"{where} carries gate tokens {sorted(toks)}, need 1")
    # File-wide: every gate token in the normative law sits inside one of the
    # two windows. A second paragraph that names the gate under any heading
    # (hunt H4) is an occurrence outside both, named by its line.
    pp49e_spans = []
    for rx, win in ((PP49D_START, pp49d_w), (PP49D_PROBE_START, pp49d_p)):
        m = rx.search(pp49_wf_norm) if win else None
        if m:
            pp49e_spans.append((m.start(), m.start() + len(win)))
    pp49e_stray = [
        pp49_wf_norm[pp49_wf_norm.rfind("\n", 0, m.start()) + 1 :].split("\n", 1)[0][:80]
        for m in PP49E_GATE.finditer(pp49_wf_norm)
        if not any(a <= m.start() < b for a, b in pp49e_spans)
    ]
    if pp49e_stray:
        pp49e_faults.append(
            f"{len(pp49e_stray)} gate token(s) outside the gate paragraph and "
            f"the reduced task graph, on line(s) {pp49e_stray}"
        )
    distinct = set().union(*pp49e_tokens.values())
    if len(distinct) != 1:
        pp49e_faults.append(f"the surfaces disagree on the gate: {sorted(distinct)}")
    # The grant gate: its token is read out of the policy line, must be the one
    # the grant-gate paragraph raises, and occurs nowhere else in the law.
    pp49e_grant = set(PP49E_GRANT.findall(pp49b_line))
    pp49e_grant_w = set(PP49E_GRANT.findall(pp50e_w))
    if len(pp49e_grant) != 1:
        pp49e_faults.append(
            f"policy line carries grant-gate tokens {sorted(pp49e_grant)}, need 1"
        )
    elif pp49e_grant_w != pp49e_grant:
        pp49e_faults.append(
            f"the grant-gate paragraph carries {sorted(pp49e_grant_w)}, not the "
            f"policy line's {sorted(pp49e_grant)}"
            + (f" ({pp50e_fault[:60]}...)" if pp50e_fault else "")
        )
    pp50e_m = PP50E_START.search(pp49_wf_norm) if pp50e_w else None
    pp49e_gspan = (pp50e_m.start(), pp50e_m.start() + len(pp50e_w)) if pp50e_m else (0, 0)
    pp49e_gstray = [
        pp49_wf_norm[pp49_wf_norm.rfind("\n", 0, m.start()) + 1 :].split("\n", 1)[0][:80]
        for m in PP49E_GRANT.finditer(pp49_wf_norm)
        if not pp49e_gspan[0] <= m.start() < pp49e_gspan[1]
    ]
    if pp49e_gstray:
        pp49e_faults.append(
            f"{len(pp49e_gstray)} grant-gate token(s) outside the grant-gate "
            f"paragraph, on line(s) {pp49e_gstray}"
        )
    # The policy file too (hunt H11): a gate token on any line other than the
    # two pinned ones (the pending_gate line, the qa.negotiation bullet) is a
    # second statement of the gate nobody pins.
    pp49e_pstray = [
        ln[:80]
        for ln in pp49_policy.splitlines()
        if (PP49E_GATE.search(ln) or PP49E_GRANT.search(ln))
        and ln not in (pp49b_line, pp49b_bullet)
    ]
    if pp49e_pstray:
        pp49e_faults.append(
            f"{len(pp49e_pstray)} gate token line(s) in {HOOK_POLICY.name} "
            f"outside the pinned pending_gate line and qa.negotiation bullet: "
            f"{pp49e_pstray}"
        )
    if pp49e_key is None:
        pp49e_faults.append(
            f"the skeleton's qa.negotiation has {len(pp49e_keys)} approval keys "
            f"({pp49e_keys}), need 1"
        )
    else:
        if distinct and distinct != {f"qa_{pp49e_key}"}:
            pp49e_faults.append(
                f"gate {sorted(distinct)} is not qa_ + the skeleton key "
                f"{pp49e_key!r}"
            )
        dotted = f"qa.negotiation.{pp49e_key}"
        # step 0c is PP-49(c)'s: naming it here would turn one fault into two
        for where, text in (
            ("policy line", pp49b_line),
            ("gate paragraph", pp49d_w),
        ):
            if f"`{dotted}`" not in text:
                pp49e_faults.append(f"{where} does not name `{dotted}`")
        if f"`{pp49e_key}` (`wait | run`)" not in pp49b_bullet:
            pp49e_faults.append(
                f"the qa.negotiation bullet does not document `{pp49e_key}`"
            )
    check(
        "PP-49(e)",
        not pp49e_faults,
        f"gate {sorted(distinct)} agrees across the policy line, the gate "
        f"paragraph and the reduced task graph, and occurs nowhere else in the "
        f"normative {QA_WORKFLOW.name}; skeleton key {pp49e_key!r} is "
        f"named in the policy line, its bullet and the gate; grant gate "
        f"{sorted(pp49e_grant)} read from the policy line is the one the "
        f"grant-gate paragraph ({len(pp50e_w.encode('utf-8'))}B) raises, and "
        f"occurs nowhere else; no gate token on any other {HOOK_POLICY.name} line"
        + ("" if not pp49e_faults else " -- " + "; ".join(pp49e_faults)),
    )

    # ---------------------------------------------------------------- PP-50
    # PP-50(a) -- census: every QA dispatch is classified, and each class ends
    # with its own block (acting / planning) or carries none (not QA agents).
    pp50a_faults: list[str] = []
    pp50_dec = _decommented(QA_WORKFLOW.read_text(encoding="utf-8"))
    pp50_lines = _dispatch_lines(pp50_dec)
    pp50_all = len(PP50_WF_LINE.findall(pp50_dec))
    pp50_agent_n = len(PP50_DISPATCH.findall(pp50_dec))
    pp50_mem = [m.group(1) for m in PP50_MEMORY_LINE.finditer(pp50_dec)]
    if pp50_all < PP50_ALL_DISPATCH_MIN:
        pp50a_faults.append(
            f"PRECONDITION failed: {pp50_all} `description: \"wf:` lines, "
            f"floor {PP50_ALL_DISPATCH_MIN}"
        )
    if pp50_all != pp50_agent_n + len(pp50_mem):
        unparsed = [
            "phase " + (re.findall(r"\\nphase:([a-z0-9-]+)", ln) or ["?"])[0]
            for ln in pp50_dec.splitlines()
            if PP50_WF_LINE.match(ln)
            and not PP50_DISPATCH.match(ln)
            and not PP50_MEMORY_LINE.match(ln)
        ]
        pp50a_faults.append(
            f"{pp50_all - pp50_agent_n - len(pp50_mem)} dispatch line(s) do not "
            f"parse as one quoted string (agent/remfix or memory): {unparsed}"
        )
    if pp50_agent_n != len(pp50_lines):
        pp50a_faults.append(
            f"{pp50_agent_n} agent/remfix dispatch lines over "
            f"{len(pp50_lines)} phases: a phase is dispatched twice"
        )
    if set(pp50_mem) != PP50_MEMORY:
        pp50a_faults.append(f"kind:memory phases are {sorted(pp50_mem)}, not {sorted(PP50_MEMORY)}")
    pp50_classes = PP50_ACTING | PP50_PLANNING | set(PP50_EXCLUDED)
    if set(pp50_lines) != pp50_classes:
        pp50a_faults.append(
            f"partition broken: unclassified {sorted(set(pp50_lines) - pp50_classes)}, "
            f"missing {sorted(pp50_classes - set(pp50_lines))}"
        )
    for phase, agent in sorted(PP50_EXCLUDED.items()):
        subj, task = pp50_lines.get(phase, ("", ""))
        got = PP50_SUBJECT.match(subj)
        if not got or got.group(1) != agent:
            pp50a_faults.append(
                f"{phase}: subject line names {got.group(1) if got else None!r}, "
                f"not {agent!r}"
            )
        bad = [tk for tk in PP50A_EXCLUDED_FORBID if tk in task]
        if bad:
            pp50a_faults.append(
                f"{phase}: a not-QA-agent dispatch carries grants text {bad}"
            )
    for phase, sentence, need, forbid in (
        *((ph, PP50_ACTING_SENTENCE,
           ("act within the grants", 'NEXT_ACTION: "gate"', "GRANT_NEEDED"), ())
          for ph in sorted(PP50_ACTING)),
        *((ph, PP50_PLANNING_SENTENCE,
           ("Plan within these grants", "NEEDS_CLARIFICATION", "FINDING"),
           ("GRANT_NEEDED",))
          for ph in sorted(PP50_PLANNING)),
    ):
        _, task = pp50_lines.get(phase, ("", ""))
        if task.count("## Grants") != 1:
            pp50a_faults.append(f"{phase}: ## Grants occurs {task.count('## Grants')} times, need 1")
        if not task.endswith(PP50_BLOCK_HEAD + sentence):
            pp50a_faults.append(f"{phase}: the task does not END with its ## Grants block")
        miss = [c for c in need if c not in task]
        if miss:
            pp50a_faults.append(f"{phase}: missing {miss}")
        bad = [c for c in forbid if c in task]
        if bad:
            pp50a_faults.append(f"{phase}: a planning dispatch carries {bad}")
    check(
        "PP-50(a)",
        not pp50a_faults,
        f"{QA_WORKFLOW.name}: {pp50_all} wf dispatch lines = {pp50_agent_n} "
        f"agent/remfix + {len(pp50_mem)} kind:memory (memory-finalize, excluded "
        f"by the kind alternation); {len(pp50_lines)} phases partition exactly "
        f"into {len(PP50_ACTING)} acting / {len(PP50_PLANNING)} planning / "
        f"{len(PP50_EXCLUDED)} not-QA-agent (attributed by subject); every "
        f"acting and planning task ends with its one ## Grants block"
        + ("" if not pp50a_faults else " -- " + "; ".join(pp50a_faults)),
    )

    pp50_rules_w, pp50_rules_fault = _pp41_window(
        pp49_wf_norm, PP50_RULES_START, PP50_RULES_END, "### QA-specific rules"
    )
    pp50_rules_m = PP50_RULES_START.search(pp49_wf_norm)
    pp50_rules_span = (
        (pp50_rules_m.start(), pp50_rules_m.start() + len(pp50_rules_w))
        if pp50_rules_m and not pp50_rules_fault else (0, 0)
    )

    def _in_rules(start_re: "re.Pattern[str]") -> str | None:
        """None when start_re's one match sits inside ### QA-specific rules."""
        if pp50_rules_fault:
            return pp50_rules_fault[:90]
        m = start_re.search(pp49_wf_norm)
        if m and not pp50_rules_span[0] <= m.start() < pp50_rules_span[1]:
            return "the paragraph is not under ### QA-specific rules"
        return None

    # PP-50(b) -- one vocabulary per variant, defined once, read back from the
    # definition and compared with what the dispatches actually carry.
    pp50b_faults: list[str] = []
    pp50b_w, pp50b_fault = _pp41_window(
        pp49_wf_norm, PP50B_START, PP50_PARA_END, "## Grants definition"
    )
    pp50b_variants: dict[str, tuple[set[str], str]] = {}
    if pp50b_fault:
        pp50b_faults.append(pp50b_fault)
    else:
        if " ".join(pp50b_w.split()) != " ".join(PP50B_PARAGRAPH.split()):
            miss = [tk for tk in PP50B_TOKENS if tk not in pp50b_w]
            pp50b_faults.append(
                "the definition paragraph is not exactly the pinned paragraph"
                + (f" (missing {miss})" if miss else
                   " (every token present: something was added or reworded)")
            )
        for m in PP50B_VARIANT.finditer(" ".join(pp50b_w.split())):
            phases = set(re.findall(r"`([a-z0-9-]+)`", m.group(2).split(" — ")[0]))
            said = re.findall(r"`([^`]+)`", m.group(3))
            pp50b_variants[m.group(1)] = (phases, said[0] if said else "")
    if pp50b_w and (where := _in_rules(PP50B_START)):
        pp50b_faults.append(f"definition: {where}")
    pp50b_heads = PP50B_HEAD_STEM.findall(pp49_wf_norm)
    if len(pp50b_heads) != 1:
        pp50b_faults.append(f"'**The `## Grants` block' heads {len(pp50b_heads)} paragraphs, need 1")
    for label, want in (
        ("Acting dispatches", PP50_ACTING),
        ("Planning dispatches", PP50_PLANNING),
        ("Not QA agents", set(PP50_EXCLUDED)),
    ):
        if pp50b_variants.get(label, (set(), ""))[0] != set(want):
            pp50b_faults.append(
                f"the definition's {label} list is "
                f"{sorted(pp50b_variants.get(label, (set(), ''))[0])}, not {sorted(want)}"
            )
    for label, members in (("Acting dispatches", PP50_ACTING), ("Planning dispatches", PP50_PLANNING)):
        tails = {
            pp50_lines[ph][1].rsplit("\n## Grants\n", 1)[1].partition("\n")[2]
            for ph in members
            if ph in pp50_lines and "\n## Grants\n" in pp50_lines[ph][1]
        }
        defined = pp50b_variants.get(label, (set(), ""))[1]
        if tails and tails != {defined}:
            pp50b_faults.append(
                f"{label}: {len(tails)} distinct sentence(s) after the block, "
                f"not the one the definition quotes"
            )
    for sentence in (PP50_ACTING_SENTENCE, PP50_PLANNING_SENTENCE):
        n = pp49_wf_norm.count(sentence)
        if n != 1:
            pp50b_faults.append(f"sentence {sentence[:40]!r} occurs {n} times in normative law, need 1 (the definition)")
    for agent_path in (RESEARCHER_AGENT, HARNESS_AGENT, EXECUTOR_AGENT):
        a_txt = agent_path.read_text(encoding="utf-8")
        for sentence in (PP50_ACTING_SENTENCE, PP50_PLANNING_SENTENCE):
            if sentence in a_txt:
                pp50b_faults.append(f"{agent_path.name} restates a dispatch sentence word for word")
    pp50b_old = sum(task.count(PP50B_OLD) for _, task in pp50_lines.values())
    if pp50b_old:
        pp50b_faults.append(f"the old preflight fragment {PP50B_OLD!r} survives {pp50b_old} time(s) in dispatches")
    check(
        "PP-50(b)",
        not pp50b_faults,
        f"{QA_WORKFLOW.name} definition paragraph {len(pp50b_w.encode('utf-8'))}B "
        f"pinned whole, heading unique; phase lists and both sentences read back "
        f"from it equal the dispatches' (one sentence per variant); neither "
        f"sentence restated in an agent file; old preflight fragment gone"
        + ("" if not pp50b_faults else " -- " + "; ".join(pp50b_faults)),
    )

    # PP-50(c) -- the acting duty reaches the three acting contracts.
    pp50c_faults: list[str] = []
    pp50c_sizes: list[str] = []
    for agent_path in (RESEARCHER_AGENT, EXECUTOR_AGENT, HARNESS_AGENT):
        raw = agent_path.read_text(encoding="utf-8")
        norm = _normative(raw)
        name = agent_path.name
        sec, sec_fault = _pp41_window(norm, PP50C_HEAD, PP50C_END, f"{name} ## Grants")
        if sec_fault:
            pp50c_faults.append(f"{name}: {sec_fault[:90]}")
        elif " ".join(sec.split()) != " ".join(PP50C_SECTION.split()):
            miss = [tk for tk in ("GRANT_NEEDED", 'NEXT_ACTION: "gate"', "You never ask") if tk not in sec]
            pp50c_faults.append(
                f"{name}: ## Grants section is not the pinned paragraph"
                + (f" (missing {miss})" if miss else "")
            )
        for i, rule in enumerate(PP50C_RULES[name]):
            if norm.count(rule) != 1:
                pp50c_faults.append(
                    f"{name}: the grant contract rule (sentence {i + 1}) is not present exactly once"
                )
        dec = _decommented(raw)
        head = PP50C_CONTRACT_HEAD.search(dec)
        yml, y_fault = _pp41_window(dec, PP50C_YAML_START, PP50C_YAML_END, f"{name} contract YAML")
        if y_fault or not head or dec.find(yml) < head.end():
            pp50c_faults.append(f"{name}: no contract YAML after the Router Contract heading")
            continue
        pp50c_sizes.append(f"{name} {len(yml.encode('utf-8'))}B")
        for key, need in (("STATUS", "BLOCKED"), ("NEXT_ACTION", '"gate"'), ("GRANT_NEEDED", "")):
            hits = re.findall(rf"(?m)^{key}:.*$", yml)
            if len(hits) != 1:
                pp50c_faults.append(f"{name}: top-level {key}: occurs {len(hits)} times in the contract YAML, need 1")
            elif need and not _yaml_enum_offers(hits[0], need):
                pp50c_faults.append(f"{name}: {key}: does not offer {need} as an enum alternative")
            elif not need and not _yaml_offers_grant(hits[0]):
                pp50c_faults.append(
                    f"{name}: GRANT_NEEDED: offers no non-empty list of known grants"
                )
        scan = norm.replace(sec, "") if sec else norm
        for allowed in PP50C_ASK_ALLOWED:
            scan = scan.replace(allowed, "")
        if "AskUserQuestion" in norm:
            pp50c_faults.append(f"{name}: names AskUserQuestion {norm.count('AskUserQuestion')} time(s); an acting agent never asks")
        asks = [m.group(0) for m in PP50C_ASK.finditer(scan)]
        if asks:
            pp50c_faults.append(
                f"{name}: {asks!r} outside the pinned ## Grants paragraph"
            )
    if _normative(HOOK_POLICY.read_text(encoding="utf-8")).count(PP50C_POLICY_ROW_SENTENCE) != 1:
        pp50c_faults.append(
            f"{HOOK_POLICY.name}: the qa-harness-builder validation row does not "
            f"carry the denied-grant sentence exactly once"
        )
    check(
        "PP-50(c)",
        not pp50c_faults,
        f"## Grants paragraph pinned whole + each grant rule sentence once in "
        f"each acting agent and the policy validation row; contract YAML ({', '.join(pp50c_sizes)}) offers STATUS BLOCKED, "
        f'NEXT_ACTION "gate" as enum alternatives and a top-level GRANT_NEEDED '
        f"offering known grants; no AskUserQuestion and no ask-the-user outside "
        f"the paragraph"
        + ("" if not pp50c_faults else " -- " + "; ".join(pp50c_faults)),
    )

    # PP-50(d) -- the regression run inherits the source workflow's grants.
    pp50d_faults: list[str] = []
    pp50d_w, pp50d_fault = _pp41_window(pp49_wf_norm, PP50D_START, PP50D_END, "re-qa-execute bullet")
    if pp50d_fault:
        pp50d_faults.append(pp50d_fault)
    else:
        flat = " ".join(pp50d_w.split())
        if flat != " ".join(PP50D_BULLET.split()):
            pp50d_faults.append(
                "the bullet is not exactly the pinned bullet"
                + (" (it does not END with the seeding sentence, carried once)"
                   if flat.count(PP50D_SENTENCE) != 1 or not flat.endswith(PP50D_SENTENCE)
                   else " (something was added or reworded before the tail)")
            )
        miss = [tk for tk in ("`qa.negotiation`", "source QA workflow") if tk not in pp50d_w]
        if miss:
            pp50d_faults.append(f"the bullet does not name {miss}")
    check(
        "PP-50(d)",
        not pp50d_faults,
        f"{QA_WORKFLOW.name} re-qa-execute bullet {len(pp50d_w.encode('utf-8'))}B "
        f"pinned whole, ending with the qa.negotiation seeding sentence"
        + ("" if not pp50d_faults else " -- " + "; ".join(pp50d_faults)),
    )

    # PP-50(e) -- the router grant gate consumes GRANT_NEEDED (window sliced
    # before PP-49(e)).
    pp50e_faults: list[str] = []
    if pp50e_fault:
        pp50e_faults.append(pp50e_fault)
    elif " ".join(pp50e_w.split()) != " ".join(PP50E_PARAGRAPH.split()):
        miss = [tk for tk in PP50E_TOKENS if tk not in pp50e_w]
        pp50e_faults.append(
            "the grant-gate paragraph is not exactly the pinned paragraph"
            + (f" (missing {miss})" if miss else
               " (every token present: something was added or reworded)")
        )
    if pp50e_w and (where := _in_rules(PP50E_START)):
        pp50e_faults.append(f"grant gate: {where}")
    pp50e_heads = PP50E_HEAD_STEM.findall(pp49_wf_norm)
    if len(pp50e_heads) != 1:
        pp50e_faults.append(f"'**The grant gate' heads {len(pp50e_heads)} paragraphs, need 1")
    # a policy line with no single grant token is PP-49(e)'s fault, not this one's
    if pp50e_w and len(pp49e_grant) == 1 and set(PP49E_GRANT.findall(pp50e_w)) != pp49e_grant:
        pp50e_faults.append(
            f"the paragraph's gate {sorted(set(PP49E_GRANT.findall(pp50e_w)))} is "
            f"not the policy line's {sorted(pp49e_grant)}"
        )
    for i, sentence in enumerate(PP50E_ESCALATION_SENTENCES):
        if pp49_wf_norm.count(sentence) != 1:
            pp50e_faults.append(f"escalation sentence {i + 1} is not present exactly once")
    check(
        "PP-50(e)",
        not pp50e_faults,
        f"{QA_WORKFLOW.name} grant-gate paragraph {len(pp50e_w.encode('utf-8'))}B "
        f"pinned whole ({len(PP50E_TOKENS)} tokens), heading unique, gate "
        f"{sorted(pp49e_grant)} = the policy line's, escalation exemption "
        f"{len(PP50E_ESCALATION_SENTENCES)}/{len(PP50E_ESCALATION_SENTENCES)}"
        + ("" if not pp50e_faults else " -- " + "; ".join(pp50e_faults)),
    )

    # PP-50(f) -- SKILL.md registers ## Grants; the registry grew, nothing left.
    pp50f_faults: list[str] = []
    pp50f_norm = _normative(SKILL_MD.read_text(encoding="utf-8"))
    pp50f_starts = list(PP50F_START.finditer(pp50f_norm))
    pp50f_bullets: list[str] = []
    if len(pp50f_starts) != 1:
        pp50f_faults.append(f"PRECONDITION failed: 'Optional sections:' matched {len(pp50f_starts)} times")
    else:
        for ln in pp50f_norm[pp50f_starts[0].end() :].split("\n")[1:]:
            if ln.startswith("- "):
                pp50f_bullets.append(ln)
            elif ln.strip():
                break
        names = tuple(
            m.group(1) for m in (re.match(r"- `(## [^`]+)`", b) for b in pp50f_bullets) if m
        )
        off_shape = [b[:60] for b in pp50f_bullets if not PP50F_SHAPE.match(b)]
        if off_shape:
            pp50f_faults.append(
                f"{len(off_shape)} registry bullet(s) are not '- `## <section>` ...' "
                f"entries: {off_shape}"
            )
        if names != PP50F_SECTIONS:
            pp50f_faults.append(f"the registry lists {list(names)}, not {list(PP50F_SECTIONS)}")
        if pp50f_bullets.count(PP50F_BULLET) != 1:
            pp50f_faults.append("the ## Grants bullet is not the pinned bullet")
    check(
        "PP-50(f)",
        not pp50f_faults,
        f"{SKILL_MD.name} optional sections: {len(pp50f_bullets)} bullets equal "
        f"the {len(PP50F_SECTIONS)} pinned names in order (## QA Bug Context kept, "
        f"## Grants added, pinned whole)"
        + ("" if not pp50f_faults else " -- " + "; ".join(pp50f_faults)),
    )

    # ---------------------------------------------------------------- PP-51
    # The topology unit suite is executed, green, quiet on stderr, and
    # non-vacuous. Run as a child so a crash in it is a red here, not a crash.
    # A second run with the self-test variable set must fail exactly once:
    # the suite's failure path is proven to reach its exit code and tail.
    pp51_faults: list[str] = []
    pp51_count = None
    pp51_run = subprocess.run(
        [sys.executable, str(TOPOLOGY_SUITE)],
        capture_output=True,
        text=True,
        env={k: v for k, v in os.environ.items() if k != PP51_SELFTEST_ENV},
    )
    if "[FAIL]" in pp51_run.stdout:
        pp51_faults.append("stdout carries '[FAIL]' outside the failure list")
    pp51_self = subprocess.run(
        [sys.executable, str(TOPOLOGY_SUITE)],
        capture_output=True,
        text=True,
        env={**os.environ, PP51_SELFTEST_ENV: "1"},
    )
    pp51_self_last = pp51_self.stdout.rstrip("\n").split("\n")[-1]
    if pp51_self.returncode != 1:
        pp51_faults.append(f"self-test run exited {pp51_self.returncode}, expected 1")
    if not PP51_SELFTEST_TAIL.match(pp51_self_last):
        pp51_faults.append(
            f"self-test tail is {pp51_self_last[:120]!r}, not "
            f"'topology unit checks: N passed, 1 failed'"
        )
    if pp51_run.returncode != 0:
        pp51_faults.append(f"the suite exited {pp51_run.returncode}")
    if pp51_run.stderr:
        pp51_faults.append(f"stderr is not empty: {pp51_run.stderr[:400]!r}")
    pp51_lines = pp51_run.stdout.rstrip("\n").split("\n")
    pp51_match = PP51_COUNT_LINE.match(pp51_lines[-1]) if pp51_lines else None
    if pp51_match is None:
        pp51_faults.append(
            f"the last stdout line is {pp51_lines[-1][:120]!r}, not "
            f"'topology unit checks: N passed'"
        )
    else:
        pp51_count = int(pp51_match.group(1))
        if pp51_count < PP51_MIN_UNIT_CHECKS:
            pp51_faults.append(
                f"{pp51_count} unit checks < floor {PP51_MIN_UNIT_CHECKS}"
            )
    for pp51_path in (TOPOLOGY_SCRIPT, TOPOLOGY_TPL):
        if not pp51_path.is_file():
            pp51_faults.append(f"{pp51_path.relative_to(PLUGIN)} does not exist")
    check(
        "PP-51",
        not pp51_faults,
        f"{TOPOLOGY_SUITE.relative_to(PLUGIN)} rc={pp51_run.returncode}, "
        f"{'no count line' if pp51_count is None else str(pp51_count) + ' unit checks passed'} "
        f"(floor {PP51_MIN_UNIT_CHECKS}), "
        f"stderr {len(pp51_run.stderr)}B; "
        f"self-test rc={pp51_self.returncode}, 1 failed; "
        f"{TOPOLOGY_SCRIPT.relative_to(PLUGIN)} and "
        f"{TOPOLOGY_TPL.relative_to(PLUGIN)} present"
        + ("" if not pp51_faults else " -- " + "; ".join(pp51_faults)),
    )

    # ---------------------------------------------------------------- PP-52
    # The confirmation-time topology write is legal by default: the default
    # mutation_allowlist carries the topology dir, `~/.cc10x/` follows
    # $CC10X_HOME when it is set (replacing, never adding), and the happy-path
    # fixture carries the skeleton's default. Each guard case asserts the
    # triple rc == 0, stderr == "", decision -- a crash reads as ALLOW.
    pp52_faults: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        pp52_root = Path(tmp)
        pp52_proj = pp52_root / "project"
        pp52_home = pp52_root / "home"
        pp52_other = pp52_root / "other"
        for d in (pp52_proj, pp52_home, pp52_other):
            d.mkdir()
        pp52_rec = "qa/topology/acme/topology.md"
        pp52_unset = {"HOME": str(pp52_home), "CC10X_HOME": ""}
        pp52_moved = {"HOME": str(pp52_home), "CC10X_HOME": str(pp52_other)}
        pp52_cases: list[tuple[str, dict[str, str], dict, bool]] = [
            ("a", pp52_unset, {"tool_name": "Write", "tool_input": {
                "file_path": str(pp52_home / ".cc10x" / pp52_rec), "content": "x"}}, False),
            ("b", pp52_unset, {"tool_name": "Write", "tool_input": {
                "file_path": str(pp52_home / ".cc10x" / "qa" / "notes.md"), "content": "x"}}, True),
            ("c", pp52_moved, {"tool_name": "Write", "tool_input": {
                "file_path": str(pp52_other / pp52_rec), "content": "x"}}, False),
            ("d", pp52_moved, {"tool_name": "Write", "tool_input": {
                "file_path": str(pp52_home / ".cc10x" / pp52_rec), "content": "x"}}, True),
            ("e", pp52_unset, {"tool_name": "Bash", "tool_input": {"command":
                'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc10x_qa_topology.py" write acme '
                "--from .cc10x/qa/x/env-plan.md --status confirmed --repos ."}}, False),
            ("f", pp52_unset, {"tool_name": "Bash", "tool_input": {"command":
                f"mkdir -p {pp52_home / '.cc10x' / 'qa' / 'topology' / 'acme'}"}}, False),
        ]
        for tag, env_over, tool, want_deny in pp52_cases:
            r = run_guard_raw(pp52_proj, artifact("qa-plan"), tool, extra_env=env_over)
            got_deny = '"permissionDecision": "deny"' in r.stdout
            if not (r.returncode == 0 and r.stderr == "" and got_deny == want_deny):
                pp52_faults.append(
                    f"({tag}) -> deny={got_deny} want {want_deny} "
                    f"(rc={r.returncode} stderr={(r.stderr.strip().splitlines() or [''])[-1]!r})"
                )

        def _pp52_probe(tag: str, art: dict, env_over: dict[str, str], target: str,
                        want_deny: bool, py: str | None = None) -> None:
            """One Write probe; a fault names the tag, the decision and the crash, if any."""
            r = run_guard_raw(
                pp52_proj, art,
                {"tool_name": "Write", "tool_input": {"file_path": target, "content": "x"}},
                extra_env=env_over, python=py,
            )
            got_deny = '"permissionDecision": "deny"' in r.stdout
            if not (r.returncode == 0 and r.stderr == "" and got_deny == want_deny):
                pp52_faults.append(
                    f"({tag}) -> deny={got_deny} want {want_deny} "
                    f"(rc={r.returncode} stderr={(r.stderr.strip().splitlines() or [''])[-1]!r})"
                )

        # (h) a non-list allowlist falls back to the default AND says so.
        pp52_art_h = artifact("qa-plan")
        pp52_art_h["qa"]["isolation"]["mutation_allowlist"] = "bogus"
        _pp52_probe("h", pp52_art_h, pp52_unset, str(pp52_home / ".cc10x" / pp52_rec), False)
        _pp52_probe("h", pp52_art_h, pp52_unset, str(pp52_home / ".cc10x" / "qa" / "notes.md"), True)
        pp52_log = pp52_proj / ".cc10x" / "cc10x-hook-events.log"
        pp52_events: list[dict] = []
        if pp52_log.is_file():
            for line in pp52_log.read_text(encoding="utf-8").splitlines():
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                if isinstance(rec, dict):
                    pp52_events.append(rec)
        if not any(
            e.get("event") == "config_malformed"
            and e.get("reason") == "mutation_allowlist not a list of strings; default applied"
            for e in pp52_events
        ):
            pp52_faults.append("(h) events log lacks config_malformed")

        # (i) only `~/.cc10x/` follows CC10X_HOME; any other tilde entry stays under HOME.
        pp52_art_i = artifact("qa-plan")
        pp52_art_i["qa"]["isolation"]["mutation_allowlist"] = [
            ".cc10x/", "~/.cc10x/qa/topology/", "~/notes/",
        ]
        _pp52_probe("i", pp52_art_i, pp52_moved, str(pp52_other / "x.md"), True)
        _pp52_probe("i", pp52_art_i, pp52_moved, str(pp52_home / "notes" / "x.md"), False)

        # (j) an unresolvable path is a decision, never a crash: a symlink loop
        # (raises on 3.9, resolves on newer Pythons) and an embedded NUL.
        pp52_loop = pp52_other / "loop"
        os.symlink(str(pp52_loop), str(pp52_loop))
        pp52_art_j = artifact("qa-plan")
        pp52_art_j["qa"]["isolation"]["mutation_allowlist"] = [".cc10x/", "~/.cc10x/qa/topology/"]
        pp52_pythons = [sys.executable] + [
            p for p in ("/usr/bin/python3",) if Path(p).is_file() and p != sys.executable
        ]
        pp52_39 = "ran" if len(pp52_pythons) > 1 else "absent"
        for py in pp52_pythons:
            probe = subprocess.run(
                [py, "-c", "import pathlib,sys; p=pathlib.Path(sys.argv[1]);\n"
                 "try: p.resolve(); sys.exit(0)\nexcept Exception: sys.exit(3)",
                 str(pp52_loop / "qa")],
                capture_output=True, text=True,
            )
            _pp52_probe(
                f"j1@{py}", pp52_art_j,
                {"HOME": str(pp52_home), "CC10X_HOME": str(pp52_loop)},
                str(pp52_loop / "qa" / "topology" / "a.md"), probe.returncode == 3, py,
            )
            _pp52_probe(
                f"j2@{py}", pp52_art_j, pp52_unset,
                str(pp52_home / ".cc10x" / "qa" / "topology" / "acme" / "top\x00ology.md"),
                True, py,
            )
    pp52_skel, _ = load_skeleton()
    pp52_skel_val = ((pp52_skel.get("qa") or {}).get("isolation") or {}).get("mutation_allowlist")
    pp52_fix = json.loads(PP52_FIXTURE.read_text(encoding="utf-8"))
    pp52_fix_val = (
        ((pp52_fix.get("starting_artifact") or {}).get("qa") or {}).get("isolation") or {}
    ).get("mutation_allowlist")
    if pp52_fix_val != pp52_skel_val:
        pp52_faults.append(
            f"(g) fixture {PP52_FIXTURE.name} mutation_allowlist {pp52_fix_val!r} != "
            f"skeleton {pp52_skel_val!r}"
        )
    if not isinstance(pp52_skel_val, list) or PP52_TOPOLOGY_ENTRY not in pp52_skel_val:
        pp52_faults.append(f"(g) skeleton mutation_allowlist {pp52_skel_val!r} lacks {PP52_TOPOLOGY_ENTRY!r}")
    check(
        "PP-52",
        not pp52_faults,
        f"the default allowlist admits the topology record and nothing else under the "
        f"home ({len(pp52_cases) + 3} guard cases a-f, h, i, j: HOME/CC10X_HOME substitution, "
        f"the topology CLI, mkdir of its dir, the non-list fallback + config_malformed "
        f"event, a foreign tilde entry, a symlink loop and a NUL under "
        f"{', '.join(pp52_pythons)}; 3.9 probe: {pp52_39}), and fixture {PP52_FIXTURE.name} == "
        f"skeleton {SKELETON.name} == {pp52_skel_val!r} (g)"
        + ("" if not pp52_faults else " -- " + "; ".join(pp52_faults)),
    )

    # ---------------------------------------------------------------- PP-53
    # The user is not the memory of how the system runs: step 0b recalls the
    # topology record, the gate is recall -> verify -> deltas -> confirm, the
    # record is written at confirmation and before memory-finalize, the
    # strategy skill bounds first-time reconstruction, Rule 1 names the write,
    # and the template table points at the record's template.
    pp53_law = QA_WORKFLOW.read_text(encoding="utf-8")
    pp53_norm = _normative(pp53_law)
    pp53_decom = _decommented(pp53_law)

    def _pp53_tokens(label: str, window: str, fault: str | None,
                     tokens: tuple[str, ...], floor: int = 1) -> list[str]:
        """Faults for one window: a vacuous window, a short window, missing tokens."""
        if fault:
            return [fault]
        out: list[str] = []
        size = len(window.encode("utf-8"))
        if size < floor:
            out.append(f"{label} window {size}B < floor {floor}B")
        missing = [tok for tok in tokens if tok not in window]
        if missing:
            out.append(f"{label} missing {missing}")
        return out

    # (a) inside PP-18(b)'s own window.
    pp53a_win = win_0b
    pp53a_faults = _pp53_tokens(
        "0b", pp53a_win,
        None if pp53a_win else "PRECONDITION failed: the 0b window is empty",
        PP53A_TOKENS,
    )
    pp53a_o1, pp53a_o2 = (pp53a_win.find(tok) for tok in PP53A_ORDER)
    if pp53a_win and not (pp53a_o1 >= 0 and pp53a_o2 >= 0 and pp53a_o1 < pp53a_o2):
        pp53a_faults.append(
            f"0b: the recall bullet does not precede the PRESENT bullet "
            f"(recall@{pp53a_o1}, present@{pp53a_o2})"
        )
    check(
        "PP-53(a)",
        not pp53a_faults,
        f"step 0b ({len(pp53a_win.encode('utf-8'))}B, _normative) recalls the "
        f"topology record BEFORE the repo set is presented: {len(PP53A_TOKENS)} tokens incl. the four outcomes, "
        f"derived_slug and never forked"
        + ("" if not pp53a_faults else " -- " + "; ".join(pp53a_faults)),
    )

    # (b) the gate.
    pp53b_win, pp53b_fault = _pp41_window(pp53_norm, PP53B_START, PP53B_END, "topology gate")
    pp53b_faults = _pp53_tokens("gate", pp53b_win, pp53b_fault, PP53B_TOKENS, PP53B_MIN_BYTES)
    pp53b_step_offsets = [pp53b_win.find(s) for s in PP53B_STEPS]
    pp53b_steps_ok = bool(pp53b_win) and -1 not in pp53b_step_offsets and all(
        a < b for a, b in zip(pp53b_step_offsets, pp53b_step_offsets[1:])
    )
    if pp53b_win and not pp53b_steps_ok:
        pp53b_faults.append(
            "gate: steps out of order or missing: "
            + ", ".join(f"{s!r}@{o}" for s, o in zip(PP53B_STEPS, pp53b_step_offsets))
        )
    if pp53b_steps_ok:
        pp53b_step2 = pp53b_win[pp53b_step_offsets[1]:pp53b_step_offsets[2]]
        pp53b_step6 = pp53b_win[pp53b_step_offsets[5]:]
        for pp53b_n, pp53b_slice in (("2", pp53b_step2), ("6", pp53b_step6)):
            if PP53B_REPOS_RULE not in pp53b_slice:
                pp53b_faults.append(f"gate: the --repos un-warned rule is missing from step {pp53b_n}")
    check(
        "PP-53(b)",
        not pp53b_faults,
        f"the topology gate in {QA_WORKFLOW.name} is recall -> verify -> deltas -> "
        f"confirm -> write in that order ({len(pp53b_win.encode('utf-8'))}B >= {PP53B_MIN_BYTES}B, "
        f"{len(PP53B_TOKENS)} tokens, {len(PP53B_STEPS)} steps ordered, --repos rule x2)"
        + ("" if not pp53b_faults else " -- " + "; ".join(pp53b_faults)),
    )

    # (c) the memory-finalize write (the window ends at the memory fence, so
    # the basis is _decommented: _normative would strip the end anchor).
    pp53c_win, pp53c_fault = _pp41_window(pp53_decom, PP53C_START, PP53C_END, "memory write")
    pp53c_faults = _pp53_tokens("memory", pp53c_win, pp53c_fault, PP53C_TOKENS)
    pp53c_start = PP53C_START.search(pp53_decom)
    pp53c_fence = pp53_decom.find(PP53C_FENCE)
    if not (pp53c_start and pp53c_fence >= 0 and pp53c_start.start() < pp53c_fence):
        pp53c_faults.append("memory: the paragraph does not precede the memory TaskCreate fence")
    if not pp53c_win.split("\n\n")[0].rstrip().endswith(PP53C_LAST_SENTENCE):
        pp53c_faults.append(
            f"memory: the paragraph does not end with the sentence {PP53C_LAST_SENTENCE!r}"
        )
    check(
        "PP-53(c)",
        not pp53c_faults,
        f"the record is updated before the memory task runs, ahead of its fence, "
        f"closing on {PP53C_LAST_SENTENCE!r} "
        f"({len(pp53c_win.encode('utf-8'))}B, {len(PP53C_TOKENS)} tokens)"
        + ("" if not pp53c_faults else " -- " + "; ".join(pp53c_faults)),
    )

    # (d) the strategy skill, with the six rungs in order.
    pp53d_text = _normative(qa_strategy_md.read_text(encoding="utf-8"))
    pp53d_win, pp53d_fault = _pp41_window(pp53d_text, PP53D_START, PP53D_END, "strategy topology")
    pp53d_faults = _pp53_tokens("strategy", pp53d_win, pp53d_fault, PP53D_TOKENS, PP53D_MIN_BYTES)
    pp53d_offsets = [pp53d_win.find(r) for r in PP53D_RUNGS]
    if pp53d_win and (-1 in pp53d_offsets or pp53d_offsets != sorted(pp53d_offsets)
                      or len(set(pp53d_offsets)) != len(pp53d_offsets)):
        pp53d_faults.append(
            "rungs not in strictly increasing order: "
            + ", ".join(f"{r}@{o}" for r, o in zip(PP53D_RUNGS, pp53d_offsets))
        )
    check(
        "PP-53(d)",
        not pp53d_faults,
        f"{qa_strategy_md.parent.name}/SKILL.md's topology section "
        f"({len(pp53d_win.encode('utf-8'))}B >= {PP53D_MIN_BYTES}B) is recall-first "
        f"with a bounded checklist, {len(PP53D_RUNGS)} numbered rungs (1)..(6) in order"
        + ("" if not pp53d_faults else " -- " + "; ".join(pp53d_faults)),
    )

    # (e) the skeleton key, null, and no dotted literal under it.
    pp53e_skel, _ = load_skeleton()
    pp53e_results = pp53e_skel.get("results") or {}
    pp53e_faults: list[str] = []
    if "topology" not in pp53e_results:
        pp53e_faults.append(f"{SKELETON.name} results has no topology key")
    elif pp53e_results["topology"] is not None:
        pp53e_faults.append(f"{SKELETON.name} results.topology is {pp53e_results['topology']!r}, not null")
    pp53e_texts = (
        (QA_WORKFLOW.name, pp53_decom),
        (HOOK_POLICY.name, _decommented(HOOK_POLICY.read_text(encoding="utf-8"))),
        (f"{qa_strategy_md.parent.name}/SKILL.md", _decommented(qa_strategy_md.read_text(encoding="utf-8"))),
    )
    for pp53e_name, pp53e_text in pp53e_texts:
        pp53e_dotted = PP53E_DOTTED.search(pp53e_text)
        if pp53e_dotted:
            pp53e_faults.append(
                f"{pp53e_name} names {pp53e_dotted.group(0)} under a null skeleton key"
            )
    check(
        "PP-53(e)",
        not pp53e_faults,
        f"{SKELETON.name} results.topology exists and is null; no "
        f"`results.topology.<field>` literal in {', '.join(n for n, _ in pp53e_texts)}"
        + ("" if not pp53e_faults else " -- " + "; ".join(pp53e_faults)),
    )

    # (f) Rule 1 names the one outside write.
    pp53f_win, pp53f_fault = _pp41_window(pp53_norm, PP53F_START, PP53F_END, "Rule 1")
    pp53f_faults = _pp53_tokens("Rule 1", pp53f_win, pp53f_fault, (PP53F_TOKEN,))
    check(
        "PP-53(f)",
        not pp53f_faults,
        f"Rule 1 ({len(pp53f_win.encode('utf-8'))}B) names {PP53F_TOKEN}"
        + ("" if not pp53f_faults else " -- " + "; ".join(pp53f_faults)),
    )

    # (g) the template table carries the record's row (PP-43(a)'s window and row regex).
    pp53g_win, pp53g_fault = _pp41_window(
        _normative(pp43a_text), PP43A_WINDOW_START, PP43A_WINDOW_END, "template table"
    )
    pp53g_rows: list[tuple[str, str]] = []
    for _c1, _c2 in PP43A_ROW.findall(pp53g_win):
        if _c1.strip() == "Artifact" and _c2.strip() == "Template":
            continue  # header
        if set(_c1.strip()) <= {"-"} or set(_c2.strip()) <= {"-"}:
            continue  # separator
        pp53g_rows.append((_c1.strip(), _c2.strip()))
    pp53g_ok = not pp53g_fault and any(
        a == "`topology.md`" and "templates/qa-topology.template.md" in b
        for a, b in pp53g_rows
    )
    check(
        "PP-53(g)",
        pp53g_ok,
        f"the artifact-template table in {qa_strategy_md.name} has a `topology.md` "
        f"row naming templates/qa-topology.template.md (_normative; {len(pp53g_rows)} rows)"
        + ("" if pp53g_ok else " -- " + (pp53g_fault or "no such row")),
    )

    # ---------------------------------------------------------------- PP-54
    # The two places that describe the route to a reader name the three
    # changes: the README QA flow block, the templates tree line, and the
    # QA routing rows of the guide and the README (twins, asserted per row).
    pp54_readme = _decommented(PP54_README.read_text(encoding="utf-8"))
    pp54_faults: list[str] = []
    pp54_flow, pp54_flow_fault = _pp41_window(
        pp54_readme, PP54_FLOW_START, PP54_FLOW_END, "README QA flow block"
    )
    if pp54_flow_fault:
        pp54_faults.append(pp54_flow_fault)
    else:
        pp54_missing = [tok for tok in PP54_FLOW_TOKENS if tok not in pp54_flow]
        if pp54_missing:
            pp54_faults.append(f"README QA flow block missing {pp54_missing}")
    pp54_tree = PP54_TREE_LINE.findall(pp54_readme)
    if len(pp54_tree) != 1:
        pp54_faults.append(
            f"PRECONDITION failed: README templates tree line matched {len(pp54_tree)} times (expected exactly 1)"
        )
    elif not PP54_TREE_MEMBER.search(pp54_tree[0]):
        pp54_faults.append("README templates tree line does not list qa-topology.template as a brace member")
    if not PP54_TEMPLATE.is_file():
        pp54_faults.append("templates/qa-topology.template.md is not on disk")
    for pp54_first, pp54_second in PP54_FLOW_ORDER:
        pp54_o1, pp54_o2 = pp54_flow.find(pp54_first), pp54_flow.find(pp54_second)
        if pp54_o1 < 0 or pp54_o2 < 0 or pp54_o1 >= pp54_o2:
            pp54_faults.append(
                f"README QA flow block order: {pp54_first!r} must precede {pp54_second!r} ({pp54_o1}, {pp54_o2})"
            )
    for pp54_name, pp54_path, pp54_row_re, pp54_hdr_re, pp54_idx in PP54_ROWS:
        pp54_text = _decommented(pp54_path.read_text(encoding="utf-8"))
        pp54_rows = pp54_row_re.findall(pp54_text)
        if len(pp54_rows) != 1:
            pp54_faults.append(
                f"PRECONDITION failed: the {pp54_name} QA routing row matched {len(pp54_rows)} times (expected exactly 1)"
            )
            continue
        pp54_hdrs = pp54_hdr_re.findall(pp54_text)
        if len(pp54_hdrs) != 1:
            pp54_faults.append(
                f"PRECONDITION failed: the {pp54_name} table header matched {len(pp54_hdrs)} times"
            )
            continue
        pp54_row_m = pp54_row_re.search(pp54_text)
        pp54_hdr_m = pp54_hdr_re.search(pp54_text)
        if pp54_row_m is None or pp54_hdr_m is None or pp54_row_m.start() <= pp54_hdr_m.end():
            pp54_faults.append(f"the {pp54_name} QA routing row sits above its table header")
            continue
        if PP54_FENCE in pp54_text[pp54_hdr_m.end() : pp54_row_m.start()]:
            pp54_faults.append(
                f"a fence opens between the {pp54_name} table header and its QA routing row"
            )
            continue
        pp54_cells = pp54_rows[0].split("|")
        if len(pp54_cells) <= pp54_idx:
            pp54_faults.append(
                f"the {pp54_name} QA routing row has {len(pp54_cells)} cells, expected the description at index {pp54_idx}"
            )
            continue
        pp54_missing = [tok for tok in PP54_ROW_TOKENS if tok not in pp54_cells[pp54_idx]]
        if pp54_missing:
            pp54_faults.append(
                f"the {pp54_name} QA routing row's description cell is missing {pp54_missing}"
            )
    pp54_agent = PP54_AGENT_ROW.findall(pp54_readme)
    if len(pp54_agent) != 1:
        pp54_faults.append(
            f"PRECONDITION failed: the README qa-researcher agent row matched {len(pp54_agent)} times"
        )
    else:
        pp54_last = [c for c in pp54_agent[0].split("|") if c.strip()][-1]
        if PP54_AGENT_TOKEN not in pp54_last:
            pp54_faults.append(f"the README qa-researcher agent row's last cell lacks {PP54_AGENT_TOKEN!r}")
    check(
        "PP-54",
        not pp54_faults,
        f"README QA flow block ({len(pp54_flow.encode('utf-8'))}B) names "
        f"{len(PP54_FLOW_TOKENS)} tokens in route order (negotiation < recall < survey, "
        f"recall < provisioning), the templates tree lists qa-topology.template as a brace "
        f"member and the file is on disk, the QA routing rows of "
        f"{' and '.join(r[0] for r in PP54_ROWS)} each carry {len(PP54_ROW_TOKENS)} tokens in "
        f"their description cell under their own table header, and the README qa-researcher "
        f"agent row names behaviour-varying surface"
        + ("" if not pp54_faults else " -- " + "; ".join(pp54_faults)),
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
