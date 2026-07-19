# Prompt-Engineering Audit — cc10x-router prose

**Scope:** `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/cc10x-router/SKILL.md` + all 8 reference `.md` files (skeleton JSON excluded — data, not prose). `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/commands/` **does not exist** (plugin root contains `agents config hooks scripts skills templates tests tools`); nothing to audit there.
**Lens:** instruction quality only. Design is treated as fixed. All rewrites are behavior-preserving.

---

## STEP 1 — Rubric from mattpocock-skills

Files read: `skills/productivity/writing-great-skills/SKILL.md`, `CLAUDE.md`, `AGENTS.md` (identical content), and for style calibration `skills/engineering/tdd/SKILL.md`, `skills/engineering/diagnosing-bugs/SKILL.md`, `skills/engineering/code-review/SKILL.md`.

Techniques observed, with exemplars:

1. **Rationale-carrying rules.** Nearly every rule ships its WHY in the same sentence, which lets the model generalize instead of surface-matching:
   > "Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea." (diagnosing-bugs)
   > "Tag every debug log with a unique prefix … Untagged logs survive; tagged logs die." (diagnosing-bugs)
2. **Checkable completion criteria** instead of adjectives:
   > "Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** … that you have **already run at least once** (paste the invocation and its output)" (diagnosing-bugs)
   The adjective ("tight") is immediately operationalized ("2-second deterministic"; "Fast — seconds, not minutes").
3. **Leading words** — one pretrained token carrying a distributed definition ("red", "seam", "tracer bullet") repeated at decision points: "the loop goes _red_ on the bug, or it doesn't."
4. **No-op hunting as explicit doctrine:** "run the no-op test on each sentence in isolation, and when one fails, delete the whole sentence rather than trim words from it." (writing-great-skills)
5. **Negation discipline:** "_don't think of an elephant_ names the elephant … Prompt the **positive** — state the target behaviour so the banned one is never spoken; keep a prohibition only as a hard guardrail you can't phrase positively, and even then pair it with what to do instead." (writing-great-skills)
6. **Decision procedures over vibes:** the code-review smell list is `what it is → how to fix` pairs; the feedback-loop list is an ordered menu ("try them in roughly this order"), so the model always knows the next move.
7. **Fail-here-not-there placement:** "A bad ref or empty diff should fail here — not inside two parallel sub-agents." (code-review) — the check is stated at the exact step where it applies.
8. **Sentence economy:** rules are one clause of instruction + one clause of why; almost no restatement. tdd is 37 lines and loses nothing.
9. **Worked negative examples:** tautological test example `expect(add(a, b)).toBe(a + b)` — a concrete anti-instance the model can pattern-match against.

Rubric applied below: (R1) every rule carries its WHY or a checkable criterion; (R2) one meaning, one place; (R3) instruction where it's needed; (R4) adjectives operationalized; (R5) emphasis markers scarce; (R6) positive phrasing preferred; (R7) delete no-ops whole.

---

## STEP 2 — Findings

### (a) Dead-weight sentences (no behavioral effect) — 14 quoted

1. SKILL.md §heading: **"Runtime contract only."** — a label with no referent; the reader cannot act differently because of it. (The following sentence already enumerates what the router does.)
2. SKILL.md §2a: **"Treat it as load-bearing orchestration law, not optional background."** — the preceding sentence already says "immediately read"; this adds ceremony, not behavior.
3. SKILL.md §5 BUILD/DEBUG/REVIEW/PLAN preparation: **"Use the `### BUILD preparation` and `### BUILD task graph` blocks in that file as the canonical BUILD law."** ×4 near-identical sentences — "read X before Y" already binds; "canonical law" is marketing register. (Restatement, R2.)
4. SKILL.md §10/§Research Quality/§Research Files: three whole sections that each say only "See `references/remediation-and-research.md` and apply its `## …` block". §6 "Research tasks" already gives the same pointer. Four pointers to one file for one trigger — three are dead weight.
5. SKILL.md §14: **"Maintain professional objectivity in all routing decisions."** — the operative half is the next sentence ("Do not rationalize a failing workflow as 'close enough'…"); the opener is a no-op the model already defaults to.
6. SKILL.md §14: **"Drift accumulates silently in long chains."** — vibe-rationale attached to the circuit breaker; carries no test, no action. (Contrast: benchmark rationale always changes what the model would do.)
7. SKILL.md §11b table intro: **"The harness is a loop engine. These concepts govern how the loop runs:"** — ceremonial framing for a vocabulary table.
8. SKILL.md §7 tier table: **"Turn-count dominates price — a capable model that one-shots a phase is cheaper than a cheap model that loops three times re-reading state and re-trying."** — this WOULD be load-bearing, except the very next paragraph in the same file states the mechanism cannot select models per dispatch, making the whole paragraph advisory prose for a lever the router doesn't hold (it's user-documentation living in an agent prompt).
9. build-workflow.md §gradient: **"This is a deliberate gradient, not the retired unconditional QUICK path"** — references a retired design the reading model never saw; historical justification, zero steering.
10. build-workflow.md escalation rule: **"(The conversion note under the reduced graph below states the same rule — they are one rule, not two.)"** — an apology for duplication instead of removing it (R2); the sentence itself steers nothing.
11. build-workflow.md finishing: **"It exists to close the end-to-end gap vs. superpowers `finishing-a-development-branch` without forking that skill."** — provenance trivia.
12. workflow-artifact-and-hook-policy.md: **"These are router-owned checks, not advisory hints."** — the gates were just defined operationally; the disclaimer adds nothing checkable.
13. workflow-artifact-and-hook-policy.md §Dispatch Context Hygiene: **"(a single dispatch has been observed at ~42k chars, ~99% pasted history)"** — scar-anecdote is fine per repo convention, but as written it is mid-sentence trivia; the rule ("pass PATHS, never pasted file bodies") does all the work.
14. SKILL.md §1 rules: **"The router is still the sole entry point for every BUILD — the gradient scales the graph to the work, it does not bypass routing."** — restates the description's "THE ONLY ENTRY POINT" and §14's ownership rule (third statement of one meaning).

### (b) Ambiguity traps — 7

1. **SKILL.md §1:** "priority order breaks ties only between rows whose primary-deliverable conditions both genuinely hold"
   - Reading A: priority column is decisive whenever ≥2 rows' deliverable-conditions hold.
   - Reading B: priority is decorative except in that rare tie; otherwise ignore the column entirely — so what does "Route using the first matching signal" (the section's opening sentence) mean? The opening sentence instructs first-match routing; the second sentence retracts it ("a keyword hit only NOMINATES"). A busy model can follow the opener and stop.
   - Rewrite: delete "Route using the first matching signal." Open with: "A keyword hit NOMINATES a row; the primary deliverable of the request DECIDES. If the primary-deliverable test genuinely holds for more than one row, the lower Priority number wins."
2. **SKILL.md §2 JUST_GO:** "auto-default all non-REVERT AskUserQuestion gates to the recommended option"
   - Reading A: every gate except the verifier REVERT gate is auto-defaulted.
   - Reading B (correct per §14/build-workflow): failure-stop gates, unresolved Open Decisions, discard confirmation, and destructive finishing options are ALSO never auto-defaulted — but those exceptions live 600+ lines away in other sections/files.
   - Rewrite: "auto-default AskUserQuestion gates to the recommended option, EXCEPT: REVERT, failure-stop gates, destructive finishing options (JUST_GO picks `Keep as-is`), and unresolved plan Open Decisions (BUILD may not start)."
3. **SKILL.md §12 step 6:** "if two agents in the same phase return contradictory verdicts (e.g., reviewer approves but verifier fails on the same evidence), treat the stricter verdict as authoritative"
   - Reading A: "stricter" = the failing/blocking verdict.
   - Reading B: "stricter" = the verdict from the stricter agent (verifier outranks reviewer) — which gives the wrong answer when the verifier passes but the reviewer flags criticals.
   - Rewrite: "treat the verdict that blocks advancement as authoritative (FAIL beats PASS, CHANGES_REQUESTED beats APPROVE)."
4. **SKILL.md §8:** "If output is too short or malformed, run inline verification rather than blindly approving."
   - Reading A: "too short" = missing the contract envelope/required fields (checkable).
   - Reading B: "too short" = subjectively brief — inviting the router to inline-verify healthy terse contracts, or to accept long-but-empty output.
   - Rewrite: "If the envelope and fallback heading are both absent, or a required field is missing, run inline verification rather than approving."
5. **build-workflow.md step 4:** trivial = "touches 1-2 files, single logical change, one testable outcome, no cross-module wiring" vs non-trivial = "3+ files across different directories…". A 2-file change with two separable concerns matches neither list ("1-2 files" pulls trivial; "separable concerns" pulls standard).
   - Reading A: file count decides. Reading B: separability decides.
   - Rewrite: "Separability decides; file count is only a signal. If ANY non-trivial signal holds (separable concerns, distinct failure modes, interface+implementation both change, new cross-module dependency), set `build_scope=standard` even at 1-2 files."
6. **SKILL.md §7 skill hints:** "Include `cc10x:frontend` only when the request, changed files, plan, or design targets UI/frontend work."
   - Reading A: any of the four sources mentioning UI triggers inclusion. Reading B: "targets" means the PRIMARY deliverable is UI. A backend change that incidentally touches one `.tsx` file parses both ways.
   - Rewrite: "Include `cc10x:frontend` when the work product includes UI the user will see or interact with (components, styling, layout, UX states). Do not include it for backend changes that merely touch files under a frontend directory."
7. **remediation-and-research.md circuit breaker vs SKILL.md §11b:** SKILL.md: "The circuit breaker … caps cycles at 3." Reference: "If count >= 3, ask the user how to proceed before creating another one."
   - Reading A: 3 cycles max, hard cap. Reading B: 3 completed cycles then a human checkpoint, after which more cycles may run. The reference (checkpoint, not cap) is authoritative — SKILL.md's "caps cycles at 3" misleads.
   - Rewrite in SKILL.md §11b: "the circuit breaker … pauses for a human checkpoint at the 3rd remediation cycle (single definition: `references/remediation-and-research.md`)."

### (c) Instruction-density map

Load-bearing = a sentence whose deletion would change router behavior. Estimates by section-weighted read.

| File | Words | Load-bearing | Padding sources |
| --- | --- | --- | --- |
| SKILL.md | 8,053 | ~70% | pointer-section quadruplication (§10/RQ/RF), tier-table advisory prose, restated entry-point/ownership claims |
| build-workflow.md | 4,113 | ~80% | rationale paragraphs that repeat gate text; escalation rule stated twice |
| remediation-and-research.md | 2,920 | ~85% | tightest file; some duplicated circuit-breaker framing |
| workflow-artifact-and-hook-policy.md | 2,469 | ~85% | mostly schema (pure signal); "not advisory hints" style disclaimers |
| plan-workflow.md | 771 | ~85% | step 2 says "ALWAYS run" three ways |
| debug-workflow.md | 543 | ~90% | clean |
| triage-workflow.md | 313 | ~90% | clean |
| codebase-health-workflow.md | 246 | ~90% | clean |
| review-workflow.md | 125 | ~95% | clean |

**3 highest-padding sections:**
1. **SKILL.md §10 + "Research Quality" + "Research Files"** — three headed sections, ~60 words, 0 new instructions; §6 "Research tasks" already carries the identical pointer. ~100% padding.
2. **SKILL.md §7 "Per-role model-tier policy"** — ~330 words of tier guidance immediately self-revoked by "the router cannot set the model at dispatch time." The only live instructions are the reviewer FLOOR sentence and "never downgrade frontmatter below the floor." ~70% padding *for the reading agent* (it is user documentation misfiled into an agent prompt).
3. **SKILL.md §1 routing rules bullets** — each of TRIAGE/CODEBASE-HEALTH restates the primary-deliverable rule already given in the intro paragraph and in the ERROR-vs-BUILD bullet (three statements of one rule), plus the entry-point restatement. ~40% padding.

### (d) Vague adjectives posing as instructions — 6, with decision-procedure rewrites

1. **"Do not resume a workflow you cannot scope confidently."** (SKILL.md §4) → "Resume a workflow only when exactly one active parent task's `wf:` matches the current conversation's markers. Zero or multiple matches → ask the user which workflow to resume."
2. **"`reason:` carries a meaningful short reason (not `N/A`)"** (SKILL.md §3) → "`reason:` names the triggering finding or request in ≤10 words (e.g. `reason:verifier FAIL on scenario 3`); `N/A` and generic fillers (`fix issues`) fail the TaskCompleted audit."
3. **"Brainstorming should ask only unresolved, high-impact questions"** (plan-workflow.md step 2) → "Ask a question only if (a) memory/plan/design do not answer it AND (b) different answers produce different plans. Otherwise proceed with the recorded default."
4. **"If the session context grows large enough to threaten this discipline, prefer returning to subagent dispatch"** (SKILL.md §12 inline mode) → "If you catch yourself reasoning from earlier conversation turns instead of the workflow artifact, or the artifact re-read no longer fits alongside the current phase's evidence, return to subagent dispatch at the next phase boundary."
5. **"Offer only when warranted by the actual task, never reflexively."** (SKILL.md §14 capability offers) → "Offer a capability only when a concrete task property calls for it (worktree: multi-phase standard build; research: post-cutoff dependency or external API in the plan; finishing menu: committable changes exist). Absent such a property, do not offer."
6. **"when it would materially improve the plan"** (plan-workflow.md step 3, research offer) → "when the plan will depend on an external API/SDK/framework version, or on a pattern with no in-repo precedent" (these triggers already exist verbatim in remediation-and-research §10 — point at them instead of paraphrasing vaguely).

### (e) Rules missing their WHY — 6

(For contrast, the router often DOES carry WHYs — see (h). These don't:)

1. **"Do not parallelize step 1 with reads."** (SKILL.md §2) — no reason given; a model that doesn't see why (`mkdir -p` must exist before the reads can be created/healed) may "optimize" it away. Add: "— the reads assume the directory exists."
2. **"`wf:PENDING_SELF` is not used."** (SKILL.md §3) — a negative fact about a value the reader has never met; without the why (legacy value from an older scheme; generating the UUID first makes it unnecessary) it's noise a model can't generalize. Either add the why or delete.
3. **"Router must run in the main Claude Code session, never inside a sub-agent."** (SKILL.md §14) — no rationale (sub-agents can't spawn sub-agents / can't own AskUserQuestion gates). A fork-style agent may believe it can be the router. Add: "— sub-agents cannot open user gates or spawn the phase agents."
4. **"Never spawn Memory Update as a sub-agent."** (§13/§14, and every task-graph memory description) — the why (a sub-agent lacks the captured payload and the memory files' session context) is never stated anywhere.
5. **"Maximum fresh-review passes: 2."** (plan-workflow.md) — no why (diminishing returns; pass-2 findings escalate to the human instead). Without it, a model facing a third finding may be tempted to "just one more pass."
6. **"Router is the only authority allowed to load internal CC10X skills. Agents may not self-activate `frontend` or `architecture`."** (SKILL.md §7) — no rationale (deterministic hints keep dispatches reproducible; self-activation reintroduces the heuristic drift the hint system exists to remove).

### (f) Attention-budget issues

- **Marker inflation is LOW where it counts, but "never" is saturated:** SKILL.md: MUST×3, NEVER(caps)×2, lowercase "never"×57, MANDATORY×3, `[EASY TO MISS]`×5, CRITICAL×1 (frontmatter). build-workflow.md: never×24. Across the file set: **~112 "never"s**. Each individual "never" is defensible; in aggregate the word stops signaling — a reader cannot tell load-bearing prohibitions (never force-push) from stylistic ones ("never treat stored task IDs as durable truth" — already stated as a §3 rule). Per benchmark negation doctrine, many are prohibitions that could be positives ("Reconstruct tasks from `wf:`+`kind:`+`phase:`" already exists; the "never rely on task IDs" twin is redundant negation).
- **Critical rule buried mid-list:** the **read-back gate after artifact mutation** (§12 step 5, "READ-BACK GATE (MANDATORY)") sits as the 11th sub-bullet of step 5 inside a 7-step loop. It gates every phase advance yet is visually a footnote. Same for **"Capture memory payload first"** — step 0 of "After every agent completion," placed *after* a 4-bullet pre-check list, so the "first" is contradicted by its own position on the page.
- **Prose caption diluting its table:** §1's intro ("Route using the first matching signal") contradicts the nomination model that follows (see (b)1). Also §7's tier table is followed by a paragraph revoking the table's applicability — a table the reader must learn and then unlearn in the same section.
- **Far-from-use placement:** the JUST_GO exceptions (§2 Trust rule) vs. destructive-finishing JUST_GO behavior (§14 + build-workflow finishing) are three locations for one policy; a model at the finishing menu sees only the local fragment. The anti-bias blocklist appears twice in full (SKILL.md §7 prompt-assembly guard; workflow-artifact-and-hook-policy §Dispatch-Prompt rules) with slightly different phrase lists ("don't treat X as a defect" vs "don't worry about") — two SOTs that have already drifted.
- **`[EASY TO MISS: …]` is a good invention** (a locally-scoped attention flag rather than a global shout) — but at 9 occurrences across files it is becoming the new IMPORTANT; the two in §4 hydration are genuinely load-bearing, the one in build-workflow step 4 ("Analysis paralysis…") is commentary.

### (g) Head-to-head style comparison — 3 passages

1. **When to ask clarifying questions.**
   - Benchmark (diagnosing-bugs Phase 3): "**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly … Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK."
   - Router (build-workflow step 10 + plan-workflow step 2): "Clarify missing requirements before builder only when the plan and memory do not already answer them." / "Brainstorming should ask only unresolved, high-impact questions and stop as soon as the intent contract is complete."
   - Verdict: the benchmark tells the model what asking BUYS and what to do when no answer comes (non-blocking default). The router gates asking well ("only when plan/memory do not answer") but "high-impact" is unoperationalized (see (d)3) and there is no AFK/default behavior except the global JUST_GO machinery an ordinary run doesn't have. Benchmark wins on completeness-per-word.
2. **When to stop / completion.**
   - Benchmark (diagnosing-bugs): "Phase 1 is done when … you can name **one command** … that you have **already run at least once** (paste the invocation and its output)" — completion as a checkable artifact.
   - Router (§12): "for BUILD, run `phase_exit_gate`; if the current phase is not complete, persist `phase_status={partial|blocked}` and stop" + gate definition in the policy file ("a phase task may complete only when its agent contract validates … its result is persisted to `results.{agent}`, and the matching event-log entry exists").
   - Verdict: **router is as good or better here** — its completion criteria are machine-checkable (exit codes, YAML fields, reconciled scenario counts), a stricter standard than the benchmark's. The weakness is dispersion: "complete" is assembled from §8 + §12 + the policy file's gate definition + the contract-override table, where the benchmark states it in one block at the point of use.
3. **How to report findings.**
   - Benchmark (code-review step 4): "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule) … Under 400 words." — output contract with a hard length budget.
   - Router (workflow-artifact-and-hook-policy §Dispatch Context Hygiene): "Sub-agents RETURN only a thin CONTRACT envelope: `status`, commits / files touched, one-line test summary, refs to concerns/findings artifacts (paths, not bodies)."
   - Verdict: near-parity, different tools — benchmark uses a word budget, router uses a field schema. The router's is more machine-parseable; the benchmark's is more copy-pasteable into a dispatch. Router loses only in that the envelope spec lives in a reference file while §8's parsing spec lives in SKILL.md — the producer contract and consumer parser are in different files.

### (h) What the router prose does BETTER than the benchmark — honest

1. **Machine-checkable contracts.** The contract-override table (`STATUS=PASS requires TDD_RED_EXIT=1, TDD_RED_REASON_KIND=behavioral …`) is a harder gate than anything in the benchmark — verdicts are validated field-by-field, not trusted. The benchmark's sub-agents are trusted to report honestly; the router assumes they lie.
2. **Fail-open/fail-closed is always specified.** Nearly every failure path names its degrade behavior ("If any git command fails … Record `git_preflight=degraded` and continue"; "For `validated: degraded` CRITICAL/HIGH findings, KEEP them in the blocking set (fail-safe…)"). The benchmark rarely specifies degraded modes.
3. **Anti-bias engineering with a literal blocklist.** The grep-your-own-prompt blocklist (`do not flag`, `at most minor`, …) operationalizes anti-anchoring further than the benchmark's parallel-subagent isolation — it's a decision procedure the model can execute mechanically.
4. **Scar-comment discipline done well in places.** "BASE must be … NEVER `HEAD~1` (which silently drops all but the last commit of a multi-commit phase)" — rule + failure mode + mechanism in one line; benchmark-grade writing.
5. **`[EASY TO MISS: …]` local flags** are a better attention primitive than global IMPORTANT — they mark the trap at the trap.
6. **Anticipated rationalizations are pre-blocked with worked negatives:** "'I ran the tests and they passed' without showing command output … is also not evidence"; "'The fix agent decided the finding was wrong' is not a dispute." This is the benchmark's tautological-test technique applied to agent behavior, and the router does it more often.
7. **The "you ARE the provider" anti-pattern** (remediation-and-research §10) is a genuinely novel, well-written instruction the benchmark has no equivalent of — it names a real LLM failure mode (treating a backend's missing capability as its own) and gives the test to run.

### (i) Top 10 concrete rewrites (behavior-preserving)

1. **SKILL.md §1 opening — remove the self-contradiction.**
   - Before: "Route using the first matching signal. A keyword hit only NOMINATES a row — the primary-deliverable rules below decide."
   - After: "A keyword hit NOMINATES a row; the request's primary deliverable DECIDES the route. When the primary-deliverable test holds for more than one row, the lower Priority number wins."
   (Same routing outcome; deletes the sentence a skimming model would obey instead.)
2. **SKILL.md — collapse §10, "Research Quality", "Research Files", and §6 "Research tasks" into one pointer.**
   - Before: four sections each saying "See `references/remediation-and-research.md` and apply its `## …` block…"
   - After: one section: "**Research (trigger, quality, files):** when research is triggered, consumed, summarized, or handed to planner/investigator, read `references/remediation-and-research.md` and apply its §10, `## Research Quality`, and `## Research Files` blocks."
3. **SKILL.md §12 step 6 verdict-contradiction rule — operationalize "stricter".**
   - Before: "treat the stricter verdict as authoritative and do not average or reconcile the signals."
   - After: "treat the blocking verdict as authoritative (FAIL over PASS, CHANGES_REQUESTED over APPROVE); never average or reconcile. Log the contradiction in `status_history`."
4. **SKILL.md §2 JUST_GO — co-locate the exceptions.**
   - Before: "auto-default all non-REVERT AskUserQuestion gates to the recommended option…" (+Trust rule two paragraphs later, +finishing rules in two other files)
   - After: "auto-default AskUserQuestion gates to the recommended option EXCEPT: REVERT, failure-stop gates, destructive finishing options (auto-pick `Keep as-is`; never merge/push/discard), and plans with unresolved Open Decisions (BUILD may not start). Log each auto-choice in `## Decisions`."
   (All four exceptions already exist as behavior; this puts them where JUST_GO is defined.)
5. **SKILL.md §7 model-tier section — separate live instruction from user documentation.**
   - Before: 330-word tier table + revocation paragraph + floor + turn-count economics.
   - After (agent-facing残): "Model selection comes from agent frontmatter; the router cannot set it per dispatch. Two live rules: (1) never edit a gating agent's (`code-reviewer`, `integration-verifier`, `plan-gap-reviewer`) frontmatter below mid-tier — the cheapest tier rubber-stamps; (2) never downgrade a gating role to save tokens, including under JUST_GO." Move the tier table to user docs (or mark the whole block `ADVISORY — for humans tuning frontmatter`, one line, table intact).
6. **build-workflow.md step 4 — make the trivial/standard boundary a decision procedure.**
   - Before: two heuristic-signal lists that can both match.
   - After: "Set `build_scope=standard` if ANY holds: separable concerns, distinct failure modes, interface AND implementation both change, new cross-module dependency, or 3+ files across directories. Otherwise (single concern, one file group, one testable outcome) set `build_scope=trivial`. Separability outranks file count."
7. **SKILL.md §12 "After every agent completion" — restore step 0 to first position on the page.**
   - Before: a "Pre-check before processing agent output" bullet list, THEN "0. Capture memory payload first…".
   - After: "0. Capture memory payload FIRST — before the pre-check, validation, or any task-state mutation (compaction can fire between agent return and parse; an uncaptured payload is lost). 1. Pre-check: did the agent address the assigned scope…" (Order on the page now matches the ordinal; the WHY — compaction — is imported verbatim from the user's global rules where it already exists.)
8. **Unify the two bias-phrase blocklists into one source of truth.**
   - Before: SKILL.md §7 lists `"do not flag", "don't treat X as a defect", "at most Minor", "the plan chose", "should be fine", "no need to check"`; policy file lists `do not flag, don't worry about, at most minor, the plan chose, already verified just, should be fine, no need to check`.
   - After: keep the full union ONLY in `workflow-artifact-and-hook-policy.md` §Dispatch-Prompt rules; SKILL.md §7 keeps the principle plus: "grep the drafted prompt against the SELF-CHECK BLOCKLIST in `references/workflow-artifact-and-hook-policy.md`; any hit → rewrite before dispatch." (Same phrases banned; drift becomes impossible.)
9. **SKILL.md §8 "too short or malformed" — make it checkable.**
   - Before: "If output is too short or malformed, run inline verification rather than blindly approving."
   - After: "If the line-1 envelope AND the first-5-lines fallback heading are both absent, or any required contract field is missing, run inline verification rather than approving."
10. **SKILL.md §11b Cycle row — stop misstating the circuit breaker it cites.**
   - Before: "The circuit breaker (single definition: `references/remediation-and-research.md` — remediation count `>= 3` → human checkpoint) caps cycles at 3."
   - After: "The circuit breaker pauses the loop for a human checkpoint at the 3rd remediation cycle (single definition: `references/remediation-and-research.md`); cycles beyond 3 run only on explicit user go-ahead."
   (This is what the reference and §14 already enforce; "caps at 3" is the only wording that says otherwise.)

---

## Verdict summary

The router's reference files (debug/plan/review/triage/codebase-health, remediation, artifact-policy) are close to benchmark quality: dense, checkable, fail-mode-aware, often better-instrumented than mattpocock's prose. SKILL.md is the weak file: it triples the entry-point claim, quadruples one pointer, opens its routing section with a sentence its own second sentence retracts, spends 300+ words on a model-tier lever it admits it doesn't have, and dilutes ~112 "never"s to background noise. Every top-10 rewrite is a wording change; none moves a gate, a priority, or an authority.
