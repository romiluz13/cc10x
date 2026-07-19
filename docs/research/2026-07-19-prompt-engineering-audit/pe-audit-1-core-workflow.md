# Prompt-Engineering Audit — CC10x Core Workflow Skills vs mattpocock-skills Benchmark

Scope: `building/`, `debugging/`, `planning/`, `code-review/` under `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/`, audited purely as LLM instructions. Orchestration (router contracts, hooks, dispatch) is out of scope and graded only where its *placement or wording* affects how the model reads the rest of the file.

---

## STEP 1 — The rubric, extracted from the benchmark

Source files: `/Users/rom.iluz/Dev/mattpocock-skills/skills/productivity/writing-great-skills/SKILL.md`, `CLAUDE.md`/`AGENTS.md`, and the six engineering skills.

### R1. No-op hunting / sentence economy
> "Hunt **no-ops** sentence by sentence … The test: does it change behaviour versus the default? … most prose that fails should go, not be rewritten." (writing-great-skills)

Every sentence must alter model behavior relative to its default. `implement/SKILL.md` is the extreme exemplar: the whole skill is 6 sentences ("Use /tdd where possible, at pre-agreed seams. … Commit your work to the current branch.").

### R2. Leading words used, not defined
> "A **leading word** is a compact concept already living in the model's pretraining … Repeated throughout the text … it accumulates a distributed definition." (writing-great-skills)

The benchmark never publishes a glossary table inside a working skill; it just *uses* the words: "the loop is **tight** and **red-capable**", "each test a **tracer bullet**". The word does the compression work in-line.

### R3. Rationale-carrying rules (WHY before/with WHAT)
Nearly every hard rule in the benchmark ships its why, which is what lets an LLM generalize to unlisted cases:
> "Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea." (diagnosing-bugs)
> "Why bother: a minimal repro shrinks the hypothesis space in Phase 3 … and becomes the clean regression test in Phase 5." (diagnosing-bugs)
> "Do NOT include specific file paths or code snippets. They may end up being outdated very quickly." (to-spec)

### R4. Checkable completion criteria and hard stop conditions
> "Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** … that you have **already run at least once** (paste the invocation and its output)" (diagnosing-bugs)
> "No red-capable command, no Phase 2." / "Do not proceed until you have reproduced **and** minimised."

Criteria are observable (a command, an exit state, a pasted output), never adjectival. Vague quantities get operationalized: "**Fast** — seconds, not minutes", sub-agent briefs capped at "Under 400 words".

### R5. Decision procedures instead of adjectives
The smell catalog is the pattern: each entry is *detector → action* ("**Data Clumps** — the same few fields or params keep travelling together … → bundle them into one type, pass that."). Ordered ladders ("try them in roughly this order", 10 rungs) convert judgment into procedure.

### R6. Negative examples with mechanism
> "**Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)` …), so it passes by construction and can never disagree with the code." (tdd)

The *because* clause is what makes the prohibition transferable. Also memorable causal aphorisms: "Untagged logs survive; tagged logs die."

### R7. Positive framing over negation
> "**Negation** — steering by prohibition backfires … Prompt the **positive** — state the target behaviour so the banned one is never spoken; keep a prohibition only as a hard guardrail … and even then pair it with what to do instead." (writing-great-skills)

### R8. Edge cases handled explicitly, with an escape hatch that is itself a procedure
> "When you genuinely cannot build a loop — Stop and say so explicitly. List what you tried. Ask the user for: (a) … (b) … (c) …" (diagnosing-bugs)
> "**Wide refactors are the exception to vertical slicing.** … sequence it as **expand–contract**." (to-tickets)
> "**If no correct seam exists, that itself is the finding.**" (diagnosing-bugs Phase 5)

### R9. XML tags for verbatim templates, headings for process
Benchmark uses `<spec-template>`, `<vertical-slice-rules>`, `<local-ticket-template>` to fence copy-shaped material; prose/steps live under `##` headings. The fence tells the model "this is a shape to reproduce", not "this is an instruction to obey".

### R10. Endings are handoffs, not summaries
Skills end with a stopping condition or a pointer to the next behavior:
> "**Then ask: what would have prevented this bug?** … hand off to the `/improve-codebase-architecture` skill … **after** the fix is in, not before — you have more information now than when you started." (diagnosing-bugs)
> "Work the frontier one ticket at a time with `/implement`, clearing context between tickets." (to-tickets)

### R11. Single source of truth
> "Keep each meaning in a **single source of truth**: one authoritative place, so changing the behaviour is a one-place edit." Duplication "inflates a meaning's prominence on the ladder past its real rank."

### R12. Exact utterances for interaction points
When the model should say something, the benchmark scripts it: `Ask: "What's the public interface, and which seams should we test?"` — zero degrees of freedom at the moment of contact.

---

## STEP 2 — File-by-file audit

# 1. building/SKILL.md (182 lines)

### (a) Dead weight / redundant / self-contradictory

1. **The "Leading Words" table (lines 15–24) is meta-commentary, not instruction — and half its rows are never used.** The table defines `deep` and `shallow`, but neither word appears anywhere else in the file or its references. The "Replaces" column ("Replaces: 'write a test that fails because the feature is missing'") is authoring documentation addressed to the skill's maintainer, not the executing model. Per R2, leading words earn their keep by being *used*; a glossary that fronts 10 lines of context load and then goes unreferenced is sediment. `red`, `green`, `tight`, `seam` are already self-defining in the sections that use them.

2. **Self-contradiction inside RED:** line 45: "Run it. **Exit 1 = RED achieved.**" followed immediately by line 47: "Exit 1 from import/syntax/collection ERROR is NOT a real RED." The first sentence teaches exactly the rule the second sentence has to un-teach. An LLM skimming under pressure can anchor on the bolded first rule. State the correct rule once: RED = behavioral failure, never mere exit code.

3. **Horizontal-slicing prohibition stated twice.** "Vertical Slicing (CRITICAL)" (line 68: "A horizontal slice (all UI, then all API, then all logic) defers integration risk…") and "Seam Discipline" (line 72: "Don't write all tests first then all implementation (horizontal slicing)"). Two adjacent sections, same meaning — violates R11 and inflates the concept's apparent rank.

4. **Behavior-over-implementation stated three times.** Line 76 ("Implementation-coupled anti-pattern… Test through the public interface, not internals"), line 174 ("**Behavioral focus:** Test what the function DOES, not how it's implemented"), and `references/testing-patterns.md` "Behavior Over Internals". One in-skill statement plus the reference is enough.

5. **"Minimal Diffs" (line 114) restates GREEN (line 51).** "No extra features, no abstractions for hypothetical futures" vs. "A one-shot operation doesn't need a helper. Don't add error handling … for scenarios that cannot happen." Merge or cross-reference.

6. **Genuine steering contradiction — framework trust.** Line 114: "Trust internal code and framework guarantees. Only validate at system boundaries." Rationalization table line 126: "'The framework handles this' → Verify with a test. Framework guarantees have edge cases." These give opposite instructions for the identical situation. A model deciding whether to test framework-adjacent behavior gets a coin flip. The reconcilable rule ("trust guarantees for *runtime validation code*, verify guarantees with a *test* when your feature depends on one") is never stated.

7. Lines 78–91 (Router Contract seam fields) are orchestration plumbing — out of audit scope — but note their *placement*: 14 lines of enum bookkeeping sit inside "Seam Discipline", splitting the test-thinking material ("use the highest seam possible") from its consumer ("If the plan provides a `### Test Seams` subsection"). The craft content would steer better if the bookkeeping were a trailing subsection or reference.

### (b) Vague adjectives without decision procedures

1. Line 55: "**REFACTOR — Clean Up.** Improve code quality while keeping tests green." — "Improve code quality" is unoperationalized (contrast the benchmark, which *removes* refactor from the loop entirely: "Refactoring is not part of the loop. It belongs to the review stage"). Rewrite: "REFACTOR: remove only what this cycle introduced — duplication between the new test and an existing one, a name that no longer fits, dead branches. Anything larger belongs to review. Re-run tests after every step; revert on failure."
2. Line 38: "`timeout 60s npx vitest run` if uncertain about CI=true" — "if uncertain" is a feeling. Rewrite: "If the runner's watch-mode default is unknown for this repo, always wrap: `timeout 60s …`."
3. Line 94: "read 2-3 existing similar components" — actually a good, countable procedure. Keep (positive note).

### (c) Rules missing their WHY

1. Line 36: "**Always use run mode:** `CI=true npm test`, `npx vitest run` (NOT `npx vitest`)" — no why. Missing rationale: *watch mode never exits, so the agent blocks forever waiting for a prompt that never returns.* With the why, the model generalizes to any unlisted runner.
2. Line 38: "**After TDD cycle:** `pgrep -f "vitest|jest" || echo "Clean"`. Kill if found." — why: *orphaned watchers hold ports/files and re-run stale code, producing false greens in later cycles.*
3. Line 55: "If tests fail during refactor, revert." — why: *a refactor by definition preserves behavior; a red test proves it wasn't a refactor, and debugging forward mixes two changes.*
4. Lines 156–157 (Loop Caps): "GREEN fails 3 consecutive times on same test → FAIL" — why: *three failures means the approach is wrong, not unlucky; continuing burns context on pattern-matching* (the debugging skill states exactly this why — reuse it here).
5. Lines 165–168 (Test Prioritization): ranked list with no reason for the ranking — why: *behavioral tests catch the most bugs per token; performance tests without a stated requirement are speculative work.*

### (d) Imperative buried under hedging / passive

Building is mostly commendably imperative. Two slips:
1. Line 182: "TDD evidence **may use** manual browser verification." — permission-shaped where it should be procedure-shaped: "If no test runner exists, verify manually in the browser and record what you checked; set TDD_RED_EXIT=1 …".
2. Line 161: "If `coverage-thresholds.json` exists, run coverage and compare." — "compare" underspecifies the action; say "run coverage; any metric below its threshold → FAIL naming the metric."

### (e) Head-to-head

- **Red before green.** Benchmark: "**Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features." CC10x: Iron Law banner plus "**False-RED guard (CRITICAL):** Exit 1 from import/syntax/collection ERROR is NOT a real RED. A genuine RED is a behavioral failure ('X is not a function', 'expected 3, received undefined'). Record the observed failure reason verbatim." **Verdict: CC10x wins.** The false-RED guard names the exact observable strings that distinguish real from fake RED and adds an evidence obligation ("record verbatim") — this closes the single most common agent TDD failure (import error counted as RED). The benchmark's tdd skill has no equivalent.
- **Seam agreement.** Benchmark: "**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. … agreeing the seams up front is how testing effort lands on the critical paths … Ask: 'What's the public interface, and which seams should we test?'" CC10x: same doctrine, but agreement resolves into an enum (`confirmed | proposed | disagreed | not_applicable`). **Verdict: benchmark wins on steering.** It gives the model a scripted utterance (R12) and a crisp gate ("No test is written at an unconfirmed seam"); CC10x's version steers the model toward *filling in a status field* rather than toward the conversation/thought the field is supposed to certify.
- **Tautological tests.** Benchmark defines it in prose; CC10x adds a BAD/GOOD code pair (lines 143–150). **Verdict: CC10x wins** — the worked example (R6) is inlined at point of use.
- **Vertical slices.** Benchmark: "each test a **tracer bullet** that responds to what the last cycle taught you" — leading word + feedback rationale. CC10x line 72 copies the tracer-bullet sentence, then line 68 re-explains horizontally. **Verdict: tie on content, benchmark wins on economy.**

### (f) Better than benchmark

- False-RED guard (see above) — best single addition in the file.
- **Safety-Check Guard** (lines 57–64): "If a safety check seems unnecessary, verify with a test that proves it's dead code before removing. 'Looks redundant' is not sufficient evidence." Concrete, rationale-implied, closes a real refactor failure mode; no benchmark equivalent.
- **Rationalization Table** (lines 118–126): pre-empting the model's own excuses in excuse→reality pairs is a technique the benchmark tdd skill lacks, and it is well executed ("'After' never comes. Write the test first — it IS the spec.").
- **Red Flags — STOP** list (lines 128–137): a self-monitoring checklist keyed to observable intentions ("You're about to commit without running the full test suite") — strong.
- **Decision Checkpoints table** (lines 102–110): each trigger is countable (">3 files not in plan") — genuine decision procedures.

### References (building/)

- `testing-patterns.md`, `test-data-and-mocks.md`: benchmark-quality — concrete, exampled, each rule cheap. "The test should still teach you something real about the system" and the Mock Quality Gate triggers ("mock setup is longer than the test body") are excellent decision procedures. SDK-style BAD/GOOD pair is exemplary R6.
- **Tables of Contents in every reference file are dead weight.** An LLM does not scroll; the anchor links steer nothing. 8–10 lines × every reference file in this slice (7 files) ≈ 60 lines of pure token cost.
- `integration-and-live-proof.md`: "Live-Proof Triggers — 'production-like', 'real data', 'connect all the dots' …" — quoting the user phrases that must escalate verification is a genuinely good trigger design. Weak spot: "Think in layers" adds nothing; the bullet list beneath it is the instruction.

# 2. debugging/SKILL.md (196 lines) + references

### (a) Dead weight / redundant / self-contradictory

1. **"Sharpen the loop" (line 37) and "Tighten the loop" (lines 39–44) are the same instruction under two names, back to back.** "Sharpen: sub-second beats sub-minute. Assert the exact failing fact… Same input → same red, no drift." then "Tighten: Faster? … Sharper signal? … More deterministic?" This is the exact duplication writing-great-skills says to collapse into ONE leading word ("tight"). Two names for one behavior also *weakens* the leading word: the model can no longer treat "tight" as the single anchor.
2. **Phase structure is scrambled by trailing sections that belong inside the phases.** "Repro Minimisation" (lines 146–150) and "Ranked Hypotheses Before Testing" (lines 152–156) appear *after* "Phase 4: Implementation". Reading order is instruction order for an LLM: by the time it reaches the minimisation rule, it has already read the implementation phase. The benchmark keeps a strict Phase 1→6 spine with everything nested in place. Worse, "Ranked Hypotheses" duplicates Phase 3 with a *different number*: Phase 3 says "Form H1/H2/H3" (three); line 154 says "Generate 3-5 ranked hypotheses". Same skill, two counts.
3. **Confidence bands contradict across SKILL.md and investigation-hygiene.md.** SKILL.md: "60-79 Plausible: fits some evidence but gaps remain — investigate more | <60 Speculative: do not act". investigation-hygiene.md: "below 50 = speculation | 50-79 = needs more evidence | 80+ = strong enough". A hypothesis at 55 is simultaneously "do not act — speculative" and "needs more evidence" (a milder verdict). One table, one place (R11).
4. **The ending sabotages the skill.** Lines 190–196 ("Pressure Testing") close with: "If a gate can be talked out of by pressure, it belongs in a hook (enforced), not in prose (advisory). **The debugging gates here are advisory** — the router and hooks enforce the structural ones." Telling the model, as the final sentence it reads, that everything above is *advisory* is an open invitation to rationalize under exactly the pressure the section warns about. The three "Would this gate hold…" questions are good; the closing meta-classification is anti-prompt-engineering. Compare the benchmark ending (R10): a post-mortem checklist plus a forward handoff.
5. "**LSP-Powered Root Cause Tracing**" (lines 63–72) partially repeats itself: "Find References — find all callers" (line 68) then "Don't grep for a function name — use Find References to get every caller with type info" (line 72). Keep the negative-pair version (it carries the why); cut the list row.
6. `investigation-hygiene.md` line 13: "Borrow the good part of GSD's context-budget discipline without importing its orchestration model" and `review-order-and-checkpoints.md` line 13: "Borrow the best part of BMAD's checkpoint thinking". These name external frameworks (GSD, BMAD) the executing model has no definition for — insider changelog talk, zero behavioral effect, possible confusion. Delete the attribution; keep the rules.

### (b) Vague adjectives

1. Phase 4 line 128: "**Verify** — regression test passes + **relevant** suite passes" — "relevant" has no selector. Rewrite: "the suite for every file the fix touched, plus every caller found in the blast-radius scan."
2. Line 82 Phase 1 step 4: "**LOG FIRST** — collect error logs, stack traces, run failing commands" — "collect" is unbounded. Rewrite: "capture the exact error text and stack trace verbatim into the evidence log before touching any code — paraphrased errors lose the searchable signature."
3. investigation-hygiene.md line 22: "checkpoint the current facts" — no format given at point of use (the Observed/Confirmed/Unknown template arrives 10 lines later; point to it).

### (c) Rules missing their WHY

1. Line 82: "LOG FIRST" — why missing: *the error text is the highest-density evidence you will ever get; acting first destroys or masks it.* (The rationalization table hints at this — "Random changes destroy evidence" — but the phase step itself is bare.)
2. Line 84 "Variant Scan — identify which variant dimensions must keep working (locale, config, env, platform…)" — why missing: *a fix verified on one variant routinely breaks a sibling variant; naming the dimensions up front turns 'it works' into 'it works everywhere it must'.*
3. Line 129 "**Prevention** — recommend lint rule, test, type guard, or monitoring" — why missing (benchmark version carries it and adds timing rationale: "Make the recommendation **after** the fix is in, not before — you have more information now than when you started.").
4. Construction ladder rung ordering (lines 27–36) — the benchmark implies order = decreasing tightness; CC10x says "try in rank order, stop at first that works" but never says what the rank optimizes, so the model can't judge when to deviate. Add: "ordered by loop tightness — earlier rungs are faster and more deterministic."

### (d) Hedging / passive

Minimal — this file is admirably imperative ("STOP. Do NOT advance to hypothesis. Return BLOCKED"). One slip: playbooks line 65 "If you are tempted to add a defensive null check immediately, stop and confirm whether the value is actually allowed to be null there" — good content, but "are tempted" frames it as feeling; sharper: "Before adding a defensive null check, prove the value can legitimately be null at that site; if it can't, the check hides the real bug upstream."

### (e) Head-to-head

- **Feedback-loop completion criterion.** Benchmark: "you can name **one command** … that you have **already run at least once** (paste the invocation and its output)". CC10x (line 46): "one command … that you have **already run at least once**" — the *paste the output* evidence obligation is dropped. **Verdict: benchmark wins narrowly.** The paste requirement converts "I ran it" from claim to artifact; CC10x, which is otherwise obsessed with evidence, omitted the cheapest evidence rule in the source.
- **Cannot-build-a-loop escape hatch.** Benchmark: stop, "List what you tried. Ask the user for: (a) access … (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), (c) permission to add temporary production instrumentation." CC10x (lines 56–61): "Return BLOCKED with: What was tried: each rung attempted and why it failed; Concrete ask: the one thing that would unblock…". **Verdict: tie.** CC10x's "each rung attempted and why it failed" is more checkable; the benchmark's concrete artifact examples (HAR file, core dump) give the model better nouns to ask for. Merge both.
- **Hypothesis quality.** Benchmark: "Each hypothesis must be **falsifiable**: state the prediction it makes. > Format: 'If <X> is the cause, then <changing Y> will make the bug disappear…' If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it." CC10x (lines 96–101): four-bullet quality criteria including "Explains ALL observed symptoms, not just the primary one". **Verdict: split.** CC10x's "explains ALL observed symptoms" criterion is a real improvement (rules out partial-cause hypotheses). The benchmark's fill-in-the-blank prediction template and the "vibe" epithet are stickier at generation time. Best version = CC10x criteria + benchmark template.
- **Causal chain.** CC10x "Causal Chain Gate" (lines 158–162): "'Somehow X leads to Y' is a gap, not an explanation. … If the prediction is wrong but the fix 'works,' you found a symptom fix, not the root cause." **Verdict: CC10x wins — no benchmark equivalent.** This is one of the best-written passages in the whole slice: negative example, mechanism, and a falsification procedure in three sentences.
- **Instrumentation.** Both carry "One breakpoint beats ten logs", tagged prefixes, never-log-everything. Benchmark adds the aphorism "Untagged logs survive; tagged logs die" (memorable causal WHY). Effectively identical; benchmark's phrasing is slightly stickier.

### (f) Better than benchmark

- Causal Chain Gate (above).
- **Hypothesis confidence scoring table** (lines 112–119): converts "confident enough to act" into numbered bands with entry criteria ("Verified: traced with LSP, reproduces the bug…"). The benchmark has no numeric act/don't-act threshold. (Fix the cross-file contradiction, though.)
- **Rationalization Table** (lines 164–175): "'Emergency, no time for process' → Systematic debugging is FASTER than guess-and-check thrashing (15-30 min vs 2-3 hours)" — pressure inoculation with a quantified claim; nothing like it in diagnosing-bugs.
- **Restart trigger** (line 121): "If 3 hypotheses fail, you're pattern-matching, not investigating." Countable trigger + diagnosis of the model's own failure mode.
- `root-cause-playbooks.md` is a strong progressive-disclosure artifact: "Read only the section that matches the failure shape in front of you"; each playbook is an ordered procedure with runnable commands ("Read the first real error, not the whole scrollback" is an excellent LLM-specific instruction). Its "Nearby Duplicate Scan" ("Fixing one instance while leaving its duplicates behind is a partial diagnosis, not a finished investigation") ends the file on a rule with its why — benchmark-grade.
- `investigation-hygiene.md` stall detection ("you have tried 2 fixes without understanding why they failed", "you cannot explain the current behavior in one paragraph") — observable self-diagnostics an LLM can actually run on itself.

# 3. planning/SKILL.md (163 lines) + live-verification-strategy.md

### (a) Dead weight / redundant

1. Line 13: "Distill plans into durable, buildable artifacts. A plan is a contract, not a brainstorm." — the second sentence is a strong leading frame; the first is a weaker paraphrase of it. Cut the first.
2. Line 120's long parenthetical re-explaining the builder-side seam-gate enum duplicates `building/SKILL.md` lines 78–91 nearly in full (violates R11 — two places to edit when the enum changes). One line ("Planned seams are the starting contract, not a suggestion — the builder must confirm or formally disagree; see `cc10x:building`") carries the steering content.
3. "Wide-Refactor Phasing" (lines 122–130) is copied from to-tickets almost verbatim — good content, correctly imported; no complaint beyond noting provenance.

### (b) Vague adjectives / non-executable procedures

1. Line 21: "Each task must be completable in one focused session (**30-90 minutes**)." An LLM cannot perceive minutes; this is a human metric wearing a number. Benchmark's version is calibrated to what an agent *can* sense: "Each slice is sized to fit in a single fresh context window" (to-tickets). Rewrite: "Each task must fit one fresh context window: one builder can read the referenced files, implement, and test without compaction. Signs it's too big: 'and then…', multiple unrelated files, more than 3 sub-steps."
2. Line 106: "**Score = Probability × Impact.** High-score risks need deterministic tests." — multiplying ordinal labels (low/med/high) is undefined; "high-score" has no threshold. Rewrite as a lookup: "high/high or high/med → deterministic test required; med/med → deterministic or probabilistic; any low/low → manual checklist acceptable."
3. Line 163: "Will this abstraction be used by >1 caller **within the next 3 sprints**?" — sprints are invisible to the model and to most repos. Rewrite: "by >1 caller *in this plan*? If not, inline it." Also, the "(Advisory)" heading label softens the rule for no gain (same disease as debugging's ending) — the question is cheap; just ask it.
4. Line 77 (Durability-Horizon): "'sprint' (refactor likely)" — same sprint-blindness; use "this-plan / near-term-refactor / stable".

### (c) Rules missing WHY

1. Line 21 task-splitting — why missing: *a task that outlives its context window gets finished by a degraded agent; splitting is context hygiene, not project management.*
2. Line 92 "Every task lists exact file paths (not 'the auth module' — `src/auth/handler.ts`)" — the contrastive example is excellent, but note the tension with the benchmark's opposite rule ("Do NOT include specific file paths … They may end up being outdated very quickly", to-spec). These serve different artifact lifetimes (spec vs execution plan) — but neither CC10x nor the plan explains *why exact paths are safe here* (the plan is executed immediately; a spec lives for weeks). One clause would immunize the model against importing the wrong rule.
3. Line 94 "Consumes/Produces are verbatim-matched across phases (no spelling drift)" — the why (drift = phase B calls a function phase A never produced) is implied by "spelling drift" — adequate.
4. ADR section (lines 147–159) — "Record ADRs inline in the plan. They are durable — the next session inherits them." Carries its why. Good.

### (d) Hedging / passive

Planning is template-dominant and mostly fine. One: line 83 "If manual, state the checklist. If deterministic, state the command." — crisp; no complaints. The main hedging offender is the "(Advisory)" label noted above.

### (e) Head-to-head

- **Task sizing.** Benchmark: "sized to fit in a single fresh context window." CC10x: "30-90 minutes." **Verdict: benchmark wins decisively** — its metric is one the executing agent can actually evaluate and it carries the real reason (context death), not a proxy.
- **Templates.** Benchmark fences with XML (`<spec-template>`); CC10x fences with markdown code blocks. **Verdict: near-tie, benchmark slightly better** — code fences inside a markdown doc can collide with the template's own fenced examples, and XML tags unambiguously signal "reproduce this shape"; but CC10x's templates are more operationally complete (Consumes/Produces, Checkpoint Type, Exit Criteria — richer than anything in to-spec/to-tickets).
- **Completeness gating.** Benchmark to-tickets gates through the *user* ("Iterate until the user approves the breakdown") with three scripted questions. CC10x gates through a 10-item self-checklist ("No placeholders/TBD — every section holds a real decision"). **Verdict: CC10x wins for an autonomous context** — every check is self-verifiable with a contrastive example ('not "done" — "test passes, build succeeds, type-check clean"'). This is the strongest section of the file.

### (f) Better than benchmark

- The **Plan Completeness Gate** (lines 85–98) — ten checkable, mostly-exampled criteria. Benchmark has nothing equivalent.
- **Distillation Rule** (line 75): "Reference files by path with a one-line reason. Do not paste contents. The next agent reads the file, not your summary of it." Perfect R3 form — rule + why in 3 sentences.
- **Functionality Flow Mapping** (lines 132–145): "Unmapped steps are untested steps" — a closing aphorism that binds the template.
- `live-verification-strategy.md`: the named-field contract (Manifest/Reset/Health/Proof/Cleanup) plus "If the data cannot be reset, the scenario is not trustworthy enough" and "Proof answers 'does the flow work?'; stress answers 'does it still work under load?'" — clean rationale-carrying distinctions throughout. Benchmark-grade file.

# 4. code-review/SKILL.md (177 lines) + references

### (a) Dead weight / redundant / self-contradictory

1. **The closing "## Note" (lines 175–177) is maintainer-facing meta:** "The Fowler Code Smells catalog … are defined once above … There is no second copy — apply those sections during both…" The first two sentences describe the document to its editor; only the final clause ("apply those sections during both passes") steers the model. Replace the section with that one clause placed at the RECEIVING mode header — and the skill then *ends* on the Precedence rule, a proper R10 ending.
2. The file never tells a standalone reader **how to choose between its two modes.** The frontmatter description says the router selects — fine — but two headers ("Mode: ADVERSARIAL REVIEW" / "Mode: RECEIVING REVIEW") with no selection sentence means a model loading the whole file reads both modes as simultaneously active. One line fixes it: "ADVERSARIAL when you are producing findings on a diff; RECEIVING when acting on findings someone else produced."
3. Zero-Finding Halt is defined twice — SKILL.md line 68 and `review-order-and-checkpoints.md` lines 64–75 — with the reference version being stronger (it has the 4-step re-examination procedure and "A bare 'looks good' is invalid"). Acceptable as summary+disclosure, but the SKILL.md line should point at the procedure rather than restate the doctrine.

### (b) Vague adjectives

1. Line 25: "**Be opinionated.**" — vague on its own; it is rescued by its neighbor "Present a recommendation, not a menu", which *is* the decision procedure. Cut "Be opinionated", keep the neighbor.
2. `security-review-checklist.md` line 67: "request timeouts and retry behavior are **sane**" — no procedure. Rewrite: "every outbound request has an explicit timeout; retries are bounded and idempotent (no retry on non-idempotent writes)."
3. heuristics line 23: "Flag only when the problem **materially** increases bug risk or future change cost" — "materially" is a judgment word, but the surrounding false-positive-prevention list (SKILL.md lines 123–131) supplies the operational half; borderline acceptable.

### (c) Rules missing WHY

1. Line 25: "Only report issues with confidence ≥80." — the why (below 80 the finding is more likely noise than signal, and noise findings burn the fix-loop's trust and tokens) is never stated; a model that doesn't understand *why* the floor exists will inflate its confidence scores to smuggle findings through. One clause fixes it.
2. Smell table numeric triggers ("Method > 20 lines", "> 4 parameters") — no why and no softener at the trigger site; the "each is a judgement call, never a hard violation" framing that the *benchmark* attaches ("Always a judgement call. Each smell is a labelled heuristic ('possible Feature Envy')") appears in CC10x only for repo overrides. Without it, ">20 lines" reads as a lint rule and generates mechanical findings.
3. Receiving step 1: "Read all feedback before responding to any item" — why missing: *later comments often supersede or contextualize earlier ones; item-by-item response commits you before you've seen the whole picture.*

### (d) Hedging / passive

This file is the least hedged of the four; findings language is appropriately absolute ("Never fabricate metrics", "Do not approve based on intent. Approve based on fresh proof."). No significant findings.

### (e) Head-to-head

- **Smell catalog.** Benchmark (12 smells): "**Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that." CC10x (16 smells): "**Data Clumps** | 3+ values always passed together | Extract into an object". **Verdict: split decision.** CC10x's numeric detectors ("3+ values", ">20 lines") are better *detection* procedures for an LLM scanning a diff; the benchmark's prose carries better *judgment* framing ("a type wanting to be born" is a leading phrase; the per-smell "possible X, never a hard violation" rule prevents mechanical flagging). Best version: CC10x's table + the benchmark's judgement-call sentence attached to the table header.
- **Findings format.** Benchmark caps sub-agent reports ("Under 400 words") and demands "Quote the spec line for each finding". CC10x: "One finding with `file:line` evidence and a fix is worth more than ten generic observations. Never report a pattern without showing where it lives" plus severity + confidence tables plus the security-checklist's exemplar finding block ("If you cannot describe the exploit path and evidence, the finding is not ready"). **Verdict: CC10x wins** — its evidence discipline is more complete and the worked finding format in `security-review-checklist.md` is exactly the R6/R9 pattern.
- **Two-axis separation.** Benchmark: separate Standards/Spec sub-agents with an explicit anti-merge rule and its why ("Do **not** merge or rerank findings — the two axes are deliberately separate… Reporting them separately stops one axis from masking the other"). CC10x: two *stages* run by one reviewer, and the parallel-assessment isolation lives in the router-merge section. **Verdict: benchmark wins on the why** — CC10x's isolation rule ("Forms opinion WITHOUT seeing the hunter's scan") states the mechanism but never the masking rationale, so a model under token pressure has no reason not to collapse the stages.
- **Receiving review.** Benchmark has no receiving skill in the audited set. CC10x's "Verify before agreeing", YAGNI-grep ("grep the codebase for the pattern the reviewer claims is wrong. If the pattern is project convention … push back"), and the push-back situation table are all decision procedures. **CC10x wins by default, and on merit** — "'I prefer my way' is not a valid push-back. 'This is project convention, see patterns.md line X' is valid" is a model contrastive pair.

### (f) Better than benchmark

- **Zero-Finding Halt** + its reference procedure — converts the classic rubber-stamp failure into a mandatory re-scan with named checks. Nothing comparable in the benchmark.
- **Confidence floor with security exception** (lines 49–56): the exception is precisely engineered — sub-80 security findings get demoted to "explicit open question" with a worked example phrase, instead of being dropped or inflated. Sophisticated, and correctly reasoned in-text.
- **AI-Generated Anti-Patterns** (lines 95–108): a catalog of *this model's own* failure modes ("Sequential awaits … (latency multiplier)", "Configurable when it should be constant") — self-targeted review guidance the benchmark lacks entirely.
- **Metric Honesty Rule** (lines 110–117): "An LLM reading static source code cannot measure real-world LCP… State what you CAN verify from code. Tag anything else as 'potential impact, not measured' — never invent numbers." Epistemics-aware prompting at its best.
- **False Positive Prevention** list — explicit do-NOT-flag categories prevent the noisy-reviewer default.
- `review-order-and-checkpoints.md` "Checkpoint Questions" ("Where would being wrong hurt the most?") and "Do not approve based on intent. Approve based on fresh proof." — benchmark-grade closers.

---

## (g) Top 10 rewrite recommendations (before → after)

**1. building/SKILL.md — kill the RED self-contradiction.**
Before: "Write one failing test for the current slice. Run it. **Exit 1 = RED achieved.** / **False-RED guard (CRITICAL):** Exit 1 from import/syntax/collection ERROR is NOT a real RED…"
After: "Write one failing test for the current slice. Run it. **RED = a behavioral failure** ('X is not a function', 'expected 3, received undefined') — never a bare exit code. Exit 1 from an import/syntax/collection error is a broken harness, not a RED: fix the harness and re-run. Record the observed failure reason verbatim."

**2. building/SKILL.md — resolve the framework-trust contradiction.**
Before: "Trust internal code and framework guarantees. Only validate at system boundaries." vs "'The framework handles this' → Verify with a test. Framework guarantees have edge cases."
After (Minimal Diffs): "Trust internal code and framework guarantees in *production code* — no runtime validation for scenarios the types or the framework already exclude. When your feature *depends* on a framework behavior, pin it with a test instead: guarantees have edge cases, and the test costs less than the defensive code." (Then align the rationalization-table row to say "Pin it with a test, don't re-validate at runtime.")

**3. building/SKILL.md — delete the Leading Words table; use the words instead.**
Before: the 10-line Word/Means/Replaces table.
After: delete it. `red`, `green`, `tight`, `seam` are already defined by use in their sections; `deep`/`shallow` are unused in this skill — if module-depth guidance is wanted, add one sentence where it applies ("Prefer a deep module: small interface, complexity hidden behind it") rather than a glossary row.

**4. debugging/SKILL.md — merge "Sharpen"/"Tighten" into one passage under one word.**
Before: "**Sharpen the loop:** sub-second beats sub-minute…" + "**Tighten the loop** — treat it as a product…"
After: "**Tighten the loop** — treat it as a product. Faster? (cache setup, skip unrelated init, narrow scope — sub-second beats sub-minute). Sharper? (assert the exact failing fact, not 'didn't crash'). More deterministic? (pin time, seed RNG, isolate filesystem — same input → same red, no drift). A 30-second flaky loop is barely better than none; a 2-second deterministic one is a debugging superpower."

**5. debugging — restore phase order; unify hypothesis count and confidence bands.**
Move "Repro Minimisation" into Phase 1→2 position (immediately after the loop goes red, before Pattern Analysis) and fold "Ranked Hypotheses Before Testing" into Phase 3. Pick ONE count ("Generate 3–5 ranked hypotheses; fewer than 3 means you anchored") and ONE confidence table; delete the conflicting bands in `investigation-hygiene.md` and point it at the SKILL.md table.

**6. debugging/SKILL.md — rewrite the ending so it doesn't disarm itself.**
Before: "…If a gate can be talked out of by pressure, it belongs in a hook (enforced), not in prose (advisory). The debugging gates here are advisory — the router and hooks enforce the structural ones…"
After: "Before trusting a debug cycle, ask: would this gate hold if the user said 'just fix it now'? If the bug seemed obvious? At 3am? Pressure is exactly when the gates pay for themselves — the feedback-loop gate exists *because* 'obvious' bugs are so often wrong diagnoses." (Move the hook-vs-prose enforcement taxonomy to maintainer docs; end the skill on the cleanup checklist + a prevention handoff, benchmark-style.)

**7. planning/SKILL.md — replace human time with agent-perceivable size.**
Before: "Each task must be completable in one focused session (30-90 minutes)."
After: "Each task must fit a single fresh context window: one builder can read the referenced files, implement, and test it without compaction. A task that outlives its window gets finished by a degraded agent. Signs it's too big: 'and then…', multiple unrelated files, multiple test scenarios, more than 3 sub-steps." (Same fix for "3 sprints" → "in this plan" and the Durability-Horizon "sprint" tier.)

**8. planning/SKILL.md — make the risk score executable.**
Before: "Score = Probability × Impact. High-score risks need deterministic tests. Low-score risks can use manual validation."
After: "Map directly: high/high or high/med (either order) → deterministic test required; med/med → deterministic or probabilistic with stated flake policy; anything involving a low → manual checklist acceptable. When unsure between two cells, take the stricter one."

**9. code-review/SKILL.md — replace the maintainer Note with a mode selector, and give the ≥80 floor its why.**
Before: "## Note / The Fowler Code Smells catalog … There is no second copy…" and "Only report issues with confidence ≥80."
After: at the top of the mode sections — "Run ADVERSARIAL when producing findings on a diff; run RECEIVING when acting on findings someone else produced. The smell catalog, AI anti-patterns, Metric Honesty, and Deferred Findings rules apply in both modes." And: "Only report issues with confidence ≥80 — below that, a finding is more likely noise than signal, and noise burns the fix loop's time and trust. Do not inflate a score to smuggle a hunch through; a genuine security hunch goes to the Summary as an open question instead."

**10. All references — delete Tables of Contents and third-party attributions.**
Before: 8–10-line "## Table of Contents" blocks in all 7 reference files; "Borrow the good part of GSD's…"; "Borrow the best part of BMAD's checkpoint thinking…"
After: delete all of them. An LLM doesn't navigate by anchor links, and GSD/BMAD are undefined tokens to the executing model — the rules they introduce stand alone. (~70 lines recovered across the slice at zero behavioral cost.)

---

## Verdict

CC10x's core-workflow skills are substantially *derived from* the benchmark (whole passages of tdd/diagnosing-bugs/to-tickets appear near-verbatim) and in several places genuinely surpass it: false-RED detection, the causal-chain gate, rationalization tables, zero-finding halt, metric honesty, and the AI-anti-pattern catalog are state-of-the-art prompt engineering the benchmark lacks. Where CC10x loses is discipline, not ideas: duplicated meanings (sharpen/tighten, three statements of behavior-over-implementation, two zero-finding definitions), two outright self-contradictions (exit-1-RED, framework trust), one cross-file numeric contradiction (confidence bands), human-calibrated metrics an agent can't perceive (minutes, sprints), missing WHYs on its hard process rules (CI=true, loop caps, the ≥80 floor), scrambled phase order in debugging, and one actively self-sabotaging ending ("the gates here are advisory"). The benchmark's writing-great-skills pruning pass — no-op hunting, single source of truth, rationale on every hard rule, endings as handoffs — applied to these four skills would cut ~20% of tokens and remove every contradiction while keeping everything that makes CC10x better.
