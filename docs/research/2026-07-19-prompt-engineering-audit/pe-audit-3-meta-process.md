# Prompt-Engineering Audit 3 — Meta/Process Skills (CC10x vs mattpocock-skills)

Lens: prompt engineering / LLM-instruction quality ONLY. Orchestration (routing, hooks, state plumbing) is out of scope and not judged. All findings are from functional files read this session; no historical audit docs consulted.

Benchmark corpus: `/Users/rom.iluz/Dev/mattpocock-skills/` (writing-great-skills, handoff, teach, grill-me, resolving-merge-conflicts, triage, setup-pre-commit, git-guardrails-claude-code).

Audited corpus: `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/` — verification, memory-and-handoff, diff-driven-docs, plan-review-gate, update, agent-common, frontend, mcp-cli, resolving-merge-conflicts (all SKILL.md + every references/ file).

---

## STEP 1 — Rubric extracted from the benchmark

The benchmark's own meta-skill (`writing-great-skills/SKILL.md`) states the criteria explicitly; the other seven skills demonstrate them. Nine techniques, each with a quoted exemplar:

### R1. The no-op test (sentence economy)
> "hunt **no-ops** sentence by sentence … The test: does it change behaviour versus the default? … when one fails, delete the whole sentence rather than trim words from it."

Every sentence must change model behavior relative to default. `grill-me/SKILL.md` is the extreme exemplar — its entire body is one line: `Run a \`/grilling\` session.`

### R2. Single source of truth (anti-duplication)
> "Keep each meaning in a **single source of truth**: one authoritative place, so changing the behaviour is a one-place edit." … "**Duplication** — the same meaning in more than one place. Costs maintenance and tokens, and inflates a meaning's prominence on the ladder past its real rank."

### R3. Rationale-carrying rules (the WHY travels with the rule)
`teach/SKILL.md`: "Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next." The rule (understand the mission first) carries three concrete consequences of skipping it. Also: "For acquiring knowledge, difficulty is the enemy. It eats working memory… For skill acquisition, difficulty is the tool."

### R4. Decision procedures, not adjectives
`setup-pre-commit`: "Check for `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun). Use whichever is present. Default to npm if unclear." — a vague word ("appropriate package manager") replaced by an observable check with a tiebreak. `triage` turns the fuzzy notion "triage this" into a literal state machine with named states and legal transitions.

### R5. Checkable completion criteria / stopping conditions
> "Each step ends on a **completion criterion** … Make it _checkable_ … and, where it matters, _exhaustive_ ('every modified model accounted for', not 'produce a change list')."

`git-guardrails` step 5: "Should exit with code 2 and print a BLOCKED message to stderr." — machine-observable done-signal. `setup-pre-commit` step 7 is a literal checklist plus a live smoke test ("Run `npx lint-staged` to verify it works").

### R6. Worked examples over prose
`git-guardrails` gives the exact verification command with a pasted JSON payload; `setup-pre-commit` gives full file bodies to write. The instruction IS the artifact.

### R7. Leading words
> "A **leading word** is a compact concept already living in the model's pretraining … anchors a whole region of behaviour in the fewest tokens." Examples: "'fast, deterministic, low-overhead' → _tight_"; "'a loop you believe in' → _red_".

### R8. Positive framing over negation
> "**Negation** — steering by prohibition backfires: _don't think of an elephant_ names the elephant … Prompt the **positive** … keep a prohibition only as a hard guardrail you can't phrase positively, and even then pair it with what to do instead."

`resolving-merge-conflicts` models the pairing: "Always resolve; never `--abort`" — positive first, prohibition as backstop.

### R9. Token discipline in descriptions & progressive disclosure
> "a description earns even harder pruning than the body … One trigger per branch. Synonyms that rename a single branch are **duplication**." And: "inline what every branch needs, and push behind a pointer what only some branches reach."

### R10. Audience integrity (implicit across the corpus)
Every benchmark sentence addresses exactly one reader: the executing agent. There is no author-facing meta-commentary inside runtime skills (meta lives in `writing-great-skills`, which is `disable-model-invocation: true`).

---

## STEP 2 — Per-file audits

Directory listings (verified this session):
- `verification/`: SKILL.md; `references/live-production-testing.md`; `evals/` (3 evals + README — eval fixtures, not runtime instructions; excluded from sentence audit)
- `memory-and-handoff/`: SKILL.md; `references/{memory-file-contracts,memory-model-and-ownership,context-budget-and-checkpointing,memory-operations}.md`
- `diff-driven-docs/`: SKILL.md; `references/doc-target-heuristics.md`; `evals/` (2 + README — excluded as above)
- `plan-review-gate/`: SKILL.md only (no references/)
- `update/`: SKILL.md only
- `agent-common/`: SKILL.md; `references/silent-failure-red-flags.md`
- `frontend/`: SKILL.md; `references/{performance-and-layout,design-md-inspiration-index,ui-state-and-feedback,design-md-authoring,accessibility-and-forms}.md`
- `mcp-cli/`: SKILL.md only
- `resolving-merge-conflicts/`: SKILL.md only

---

## 1. verification/SKILL.md (+ references/live-production-testing.md)

### (a) Dead weight / redundant / self-contradictory
1. > "A PASS without proof is a claim. A claim is not verification."
   The second sentence restates the first. One sentence carries it; the epigram form pays double.
2. > "**Authoring Rule: Keep Gates High.** Every gate in this skill exists because a specific failure mode was observed. Removing a gate without understanding what it prevents reintroduces the failure. Gates are scar notes — they encode hard-won lessons."
   This is addressed to the skill's *author*, not the executing agent (violates R10). The executing agent cannot remove gates. Three sentences of pure runtime dead weight; belongs in a maintenance comment (`<!-- -->`), not the loaded body.
3. Triple coverage of the same prohibition (violates R2): "should" language is banned in **Goal-Backward Lens** ("Forbidden language before proof: 'should pass', 'looks good'…"), again in the **Rationalization Table** ("'Should work now' | RUN the verification command. 'Should' is not evidence."), and again in **Red Flags** ("You're using 'should', 'probably', 'seems', or 'looks' before running tests"). One meaning, three sites.
4. **Auditor Posture** ("A reviewer approval, green unit test, or builder claim is never sufficient") restates the opening principle ("Verify that the phase achieved its goal, not that prior agents said it did") and Rationalization row 3 ("The agent said it passed"). Third telling of one idea.
5. > "Gates are scar notes — they encode hard-won lessons." — decorative; changes no behavior (fails R1).

### (b) Vague adjectives posing as instructions
1. > "Error handling covers the failure modes the change introduces" (Self-Critique checklist). "Covers" is unfalsifiable. Rewrite: "For each new throw/reject/error-return added by the diff, name the caller that handles it; any error path with no named handler fails the check."
2. > "**Live** | Production-like environment" — "production-like" is defined only by pointer to the reference; in the table it's an adjective. Rewrite the table cell: "Runs `live_harness_runner.py` against a seeded first-party environment."

### (c) Rules missing their WHY
1. > "Every verification must state its validation level."
   Missing why: *so a reader can judge evidence strength — a manual check and a deterministic exit code are not interchangeable proof, and unlabeled evidence lets weak proof masquerade as strong.*
2. > "Don't run tests you know will fail on code quality issues."
   Missing why: *a failing run wastes a cycle and produces noise evidence that then has to be explained away; fix-then-verify keeps every recorded run meaningful.*
3. > "re-run once. Pass on re-run → mark PASS with `flaky: true`."
   Why once and not N? Missing: *each extra retry raises the odds a genuine intermittent bug passes by luck; one retry distinguishes environment blips from real flake without laundering failures.* (The trailing "Never convert flaky pass into unconditional confidence" gestures at it but doesn't justify the specific cap.)

### (d) Hedged / passive imperatives
Essentially none — this file is admirably imperative. Borderline: "If you cannot independently reproduce a claimed success, return FAIL" is conditional but correctly so. No findings.

### (e) Head-to-head vs benchmark
The benchmark has no verification skill; the closest analogs are R5 (checkable criteria) and R1. The Evidence Array is a *better* completion criterion than anything in the benchmark ("SCENARIOS_PASSED must equal EVIDENCE.scenarios with exit 0 + Result=PASS" is exhaustive and machine-checkable, exactly what R5 asks for). But the file fails R2 badly: the same anti-"should" meaning holds three rungs at once, which per the benchmark "inflates a meaning's prominence on the ladder past its real rank." The benchmark would collapse Rationalization Table + Red Flags + Forbidden Language into one table.

### (f) What CC10x does BETTER
- `COMPLETION → TRUTH → PROOF` is a genuine leading-word triad (R7) — three tokens that anchor the whole file.
- "Environment escape" row is a sharp, non-obvious rule with a built-in decision procedure ("command not found, ECONNREFUSED → classify as ENVIRONMENT not code. Mark BLOCKED") — the benchmark has nothing this precise about failure classification.
- The reference file's fail-closed rules ("If stress is required but only proof ran, the task is incomplete") are exhaustive completion criteria the benchmark would applaud.
- Shipping evals alongside the skill (`evals/`) operationalizes "predictability" better than the benchmark itself does.

### (g) Top rewrites (before → after)
1. Delete: "A claim is not verification." → (keep only "A PASS without proof is a claim.")
2. "**Authoring Rule: Keep Gates High.** Every gate… hard-won lessons." → `<!-- maintenance: each gate encodes an observed failure; understand what a gate prevents before removing it -->` (out of runtime body).
3. Merge Rationalization Table + Red Flags + Forbidden Language into ONE table titled "Excuses and tells", each meaning once. Saves ~25 lines, restores single source of truth.
4. Delete "Auditor Posture" section; fold its one novel clause into the opener: "…not that prior agents said it did. If you cannot independently reproduce a claimed success, return FAIL."
5. "Error handling covers the failure modes the change introduces" → "Every new error path in the diff has a named handler; unhandled → fix before verifying."
6. "Every verification must state its validation level." → "State the validation level with every result — unlabeled evidence lets manual spot-checks masquerade as deterministic proof."
7. "re-run once" → "re-run once — one retry separates environment blips from real flake; more retries launder genuine failures."
8. Red Flags list (8 negations) → compress to the 3 not already covered by the merged table, phrased as tells: "satisfaction before exit 0", "weakening an assertion to pass", "committing without fresh evidence".
9. Table cell "Production-like environment" → "seeded first-party env via `live_harness_runner.py`".
10. reference `live-production-testing.md`: "Prefer a small number of meaningful scenarios over a large number of shallow checks" → "5 scenarios max: golden path, critical negative, boundary/side-effect, retry/recovery (if queues), stress (if concurrency)" — the list already exists below; make the count binding and delete the adjective sentence.

---

## 2. memory-and-handoff/SKILL.md (+ 4 references)

### (a) Dead weight / redundant / self-contradictory
1. Ownership rules exist in THREE places (violates R2): SKILL.md "### Ownership" (7 bullets), `references/memory-model-and-ownership.md` "## Ownership" (full section), and `references/memory-operations.md` ("Write agents normally do **not** edit `.cc10x/*.md` directly"). Same meaning, three files — a three-place edit for any ownership change.
2. Secret redaction stated twice in SKILL.md alone: "### Secret Redaction (OUTWARD artifacts only)" and Handoff rule 3 ("Redact secrets and PII before writing. Replace with `<redacted:secret>`…"). Same replacement token, same rule.
3. > "This closes the loop: every solved problem makes the next problem easier." — decorative summary of the numbered loop just given (fails R1).
4. Self-contradiction in modality: `agent-common` and SKILL.md say agents "do NOT edit `.cc10x/*.md` directly" (absolute, one named carve-out), but `memory-operations.md` says "Write agents **normally** do not edit…". "Normally" reopens a door the absolute rule closed. An agent holding both files has permission ambiguity.
5. `memory-model-and-ownership.md` "## Memory Surfaces" bullet list duplicates SKILL.md's "### Memory Surfaces" table almost item-for-item.
6. Both reference files open with a "## Contents" ToC for ~100-line files — pure token cost; the headings are visible one scroll away.

### (b) Vague adjectives posing as instructions
1. > "Prefer stable nouns over temporary wording." Opaque. Rewrite: "Name things by file path, module, or domain term — never by 'the new function', 'the fix from earlier', or anything only this session can resolve."
2. > "Checkpoint … before the session gets fragile" / tier signal "clear | context feels crisp" (`context-budget-and-checkpointing.md`). "Feels crisp" is unobservable. Rewrite the tier signals to countable tells: "clear: no rereads; warming: >2 rereads of the same file OR >30 tool calls; degrading: a protocol step skipped or an 'I think' without evidence; fragile: two contradictory recalls of the same fact."
3. > "Keep SKILL.md files lean" (Universal Rule 4) — "lean" with no bound; also an author-facing rule inside a runtime reference (R10 violation).

### (c) Rules missing their WHY
1. > "Keep each entry one line."
   Missing why: *memory files are reloaded at every workflow start; every extra line is a recurring tax on all future sessions.*
2. > "Write to OS temp dir, never into the repo." (Handoff rule 1)
   Missing why: *a handoff is ephemeral and personal; written into the repo it becomes an accidental commit and a stale doc the next reader mistakes for truth.* (Matt's version also omits this — chance to beat the benchmark.)
3. > "Never rename canonical headings to make one edit easier." (`memory-file-contracts.md`)
   Why is present nearby ("The headings are part of the durable CC10X protocol") but abstract. Sharpen: *renaming a heading silently breaks every future Edit anchored on it.*

### (d) Hedged / passive imperatives
1. > "Write agents normally do **not** edit `.cc10x/*.md` directly." — hedge ("normally") on a hard rule; see (a)4.
2. > "adding or changing hints is a durable-memory concern, not an ad-hoc agent edit" (`memory-model-and-ownership.md`) — passive classification instead of an imperative. Rewrite: "Do not edit `## Project SKILL_HINTS`. Surface hint recommendations in planner output or Memory Notes."
3. > "Checkpoint into workflow artifacts … before the session gets fragile." — the trigger is a feeling, not an event (see (b)2).

### (e) Head-to-head vs benchmark (`handoff/SKILL.md`, 5 sentences)
Matt covers the whole handoff in five sentences: temp dir, suggested-skills section, no duplication ("Reference them by path or URL instead"), redaction, tailor-to-args. CC10x's HANDOFF mode (~30 lines) covers the same five ideas plus a contents table. Line-by-line: CC10x's rule 2 ("Reference artifacts by path/URL, never paste contents. The next reader has the repo. They need a map, not a copy.") is Matt's rule *plus the why* — an improvement per R3. The contents table (Goal / Current state / What's next "EXACT next step — concrete enough to start cold" / blockers "unresolved errors VERBATIM") is a genuine upgrade: it converts Matt's "summarise the conversation" into checkable slots (R5). Cost: ~4x the tokens, and the SESSION MEMORY mode sharing the file means handoff guidance sits below 80 lines of memory protocol it never needs (a branch-split candidate per R9's disclosure test — the two modes share almost nothing).

### (f) What CC10x does BETTER
- KEEP / SUMMARIZE / DROP compaction rubric is a first-class decision procedure with the crucial verbatim rule ("never paraphrase a constraint or error") — nothing in the benchmark is this precise about compression.
- The five-outcome compounding table (Keep/Update/Consolidate/Replace/Delete) with its stated why ("Without consolidation, memory accumulates stale entries that mislead future work") is model R3+R4 practice.
- "Memory is an index, not a transcript" is a real leading phrase (R7).
- Handoff "suggested skills/tools" pointer marked "load-bearing" — good prominence signaling.

### (g) Top rewrites
1. Collapse the three ownership statements to one: keep SKILL.md's "### Ownership"; in both references replace their ownership sections with "Ownership: see SKILL.md ### Ownership."
2. Delete Handoff rule 3's body; replace with "Redact per ### Secret Redaction above."
3. "Write agents normally do not edit…" → "Write agents do not edit `.cc10x/*.md` (sole carve-out: bug-investigator's `[DEBUG-N]` lines)."
4. "Prefer stable nouns over temporary wording." → "Name by path/module/domain term, never 'the new function' or other session-relative references."
5. Degradation tier signals → countable tells (see (b)2).
6. "Keep each entry one line." → "Keep each entry one line — memory reloads every session; each line is a recurring tax."
7. Delete "This closes the loop: every solved problem makes the next problem easier."
8. Delete both "## Contents" ToCs in references.
9. `memory-model-and-ownership.md` "## Memory Surfaces" → delete; point at SKILL.md table.
10. Handoff rule 1 add why: "…never into the repo — a repo-committed handoff becomes a stale doc the next reader mistakes for current truth."

---

## 3. diff-driven-docs/SKILL.md (+ references/doc-target-heuristics.md)

### (a) Dead weight / redundant / self-contradictory
1. Overview throat-clearing: > "diff-driven-docs treats documentation as a first-class deliverable of every BUILD phase, not an afterthought. Just as test-driven-development enforces that tests must be produced as part of the code-change cycle, diff-driven-docs enforces that doc updates must accompany code changes before the workflow closes."
   The TDD analogy and "first-class deliverable" framing change no behavior (R1). Only two overview sentences earn their place: the stale-docs rationale and the classifier pointer.
2. > "writes only the updates that are genuinely needed — skipping trivially low-impact changes fast" — the classifier below IS this rule; the prose restatement is duplication (R2).
3. The SKIP set (routine bug fix / style change / test addition / dep bump) appears FOUR times: the Impact Classifier table rows, the "**SKIP audit docs if:**" bullet, "### When to Create vs. Update vs. Skip → SKIP when:", and `doc-target-heuristics.md` Audit Layer table. One meaning, four sites.
4. The CREATE-audit-doc trigger list (new pattern / tech choice / non-obvious tradeoff / breaking or compliance) likewise appears three times (classifier bullets, "CREATE new when:", heuristics table).
5. CLAUDE.md index rule duplicated: Step 5 self-review ("it is indexed in the relevant `## Docs` section… No doc content was duplicated in CLAUDE.md") and `doc-target-heuristics.md` "## CLAUDE.md Index Rule" (verbatim same two rules).

### (b) Vague adjectives posing as instructions
1. > "Determine `IMPACT_LEVEL` (none / low / medium / high)" — only `none` is ever defined ("all four layers SKIP"). low/medium/high have no assignment procedure yet are emitted in the contract. Rewrite: "none = all layers SKIP; low = only CHECKs, no CREATE; medium = ≥1 UPDATE or single-layer CREATE; high = any breaking-change / security row, or CREATE in ≥2 layers." (Exact mapping is the maintainers' call; the point is the values must be decidable.)
2. > "a team member six months from now would ask 'why did we do it this way?'" — good intuition pump, but as the *only* test it's a vibe. Pair it with the concrete triggers already listed (it is — acceptable; flag only that it should not stand alone in future edits).

### (c) Rules missing their WHY
1. > "`Read` the entire target file first" (Step 4).
   Missing why: *editing unread docs duplicates existing sections and contradicts surrounding prose; the read is what makes the edit minimal.*
2. > "Dedup rule: if a decision exists in both `docs/decisions/` and `docs/adr/`, the `docs/adr/` version wins; delete the legacy duplicate."
   Missing why: *two live copies will diverge and future readers can't tell which is authoritative.*
3. > "Read the file again after writing to verify the edit landed correctly." — why absent (and questionable: for tool-verified edits this is often a wasted read; if kept, the why is "Edit anchors can match in unexpected places").

### (d) Hedged / passive imperatives
1. > "doc updates must accompany code changes before the workflow closes" — passive construction of the gate; the Workflow steps carry the actual imperatives, so this is hedge-by-abstraction in the overview.
2. `doc-target-heuristics.md`: "Projects customize targets in CLAUDE.md" — descriptive where an imperative is meant ("Use the project's `## Doc Targets` table if present; else this table"). SKILL.md Step 3 already says it imperatively — the reference's version is the weak duplicate.

### (e) Head-to-head vs benchmark
Closest analog is `triage` (classification-driven state machine). The Impact Classifier table is fully in the benchmark's spirit — arguably cleaner than triage's prose transitions, because every cell is an enumerated verdict (SKIP/CHECK/CREATE). The fast-exit ("If all four layers are SKIP, set `IMPACT_LEVEL: none` and emit a SKIPPED contract immediately without opening any doc files") is a textbook stopping condition (R5) the benchmark itself never states this crisply. Where it loses to the benchmark: R2 — triage states each rule once; this file states its SKIP/CREATE sets 3-4 times.

### (f) What CC10x does BETTER
- The Rationalization Table rows are excellent rationale-carriers: "'the tests document the behavior' | Tests document correctness, not usage." — compact, memorable, behavioral.
- "Stale documentation is worse than no documentation — it actively misleads" is the right single WHY for the whole skill (R3), stated first.
- Layer scoping bullets ("What to write: name, file path, description, signature, params, return value…") are exhaustive per R5.

### (g) Top rewrites
1. Overview → two sentences: "Stale documentation is worse than no documentation — it actively misleads. Run the Impact Classifier on the diff; write only what a layer's verdict requires."
2. Define low/medium/high for `IMPACT_LEVEL` (see (b)1) or drop the unde­fined values from the contract.
3. Delete "**SKIP audit docs if:**" bullet (rows already in the table); keep the table as the single source.
4. Delete "### When to Create vs. Update vs. Skip"'s SKIP list; keep CREATE/UPDATE (they add detail the table lacks).
5. `doc-target-heuristics.md` Audit Layer table → delete the four SKIP rows (owned by SKILL.md classifier); keep only the CREATE/UPDATE signal rows.
6. Delete `## CLAUDE.md Index Rule` from the reference (verbatim duplicate of Step 5 items).
7. "Read the entire target file first" → add "— an unread edit duplicates sections and contradicts neighbors; the read is what makes the edit minimal."
8. Dedup rule → add "— two live copies diverge; readers can't tell which is authoritative."
9. "doc updates must accompany code changes before the workflow closes" → delete (Workflow + Router Integration already enforce it).
10. Reference line "Projects customize targets in CLAUDE.md (see templates/doc-target-overlay.md)." → delete from reference; SKILL.md Step 3 is the imperative home.

---

## 4. plan-review-gate/SKILL.md (no references/)

### (a) Dead weight / redundant / self-contradictory
1. Adjacent-paragraph duplication: > "The value is fail-closed blocking and adversarial framing, not fake reviewer independence." followed immediately by > "**Important limit:** This gate is stronger wording plus hard blocking, not true reviewer isolation… do not pretend fresh runtime separation exists when it does not." Same disclosure twice in consecutive paragraphs (R2).
2. Naming split: frontmatter/dir say `plan-review-gate`; H1 and every output token say "Spec Gate"/`SPEC_GATE_*`. Two names for one concept dilutes the leading word (R7) — the agent must hold both.
3. > "No suggestions, no softening, no collaborative rewrite advice." + Anti-pattern row "Reporting suggestions instead of verdicts | This gate is an auditor, not a collaborator" — same meaning twice.

### (b) Vague adjectives posing as instructions
1. > "Plan mode fits the task … Blocking if: Mode is too weak for the request." No procedure to decide "too weak". Rewrite: "Blocking if: request changes ≥3 files or any contract/schema/auth surface and mode is `direct`; or request asks for a decision between alternatives and mode is not `decision_rfc`."
2. > "Complexity proportional | Solution is over-engineered for the problem." Rewrite: "Blocking if: the plan introduces a file, abstraction, or dependency that no requirement row maps to."
3. > "Edge cases addressed | Obvious error paths, empty states, or boundary conditions missing." "Obvious" is the auditor's mood. Rewrite: "For each input surface the plan touches, the plan names its empty, invalid, and failure case — or states why none applies."
4. > "Verification rigor fits risk" — "fits" undecidable as written; the second half of the cell ("Critical-path work is missing `critical_path` rigor") partially rescues it, but "critical-path work" itself is undefined in-file.

### (c) Rules missing their WHY
1. > "There is no 'APPROVED WITH COMMENTS'."
   Missing why: *a middle verdict lets blocking issues ride along unfixed — comments get ignored, FAILs get fixed.*
2. > "IF SPEC_GATE_FAIL after 3 iterations → ESCALATION"
   Why 3? Missing: *if three targeted revisions can't clear the findings, the plan's premise is wrong, not its wording — more loops polish a wrong plan.* (The scar comment about counter reset is good practice but explains a different thing.)
3. > "Do NOT question the user from this skill."
   Missing why: *the gate runs inside the planner's turn; user questions from the gate would fork the dialogue the planner owns.* (Guessable from "The planner decides how to revise or escalate," but not stated.)

### (d) Hedged / passive imperatives
1. > "contradictions with existing architecture/patterns are hidden instead of made explicit" and several other Blocking-if cells are passive descriptions of a state rather than checks the auditor performs. Consistent table grammar would be "Blocking if you find: …" with an active verb per row.
2. > "Keep the auditor posture, but do not pretend fresh runtime separation exists when it does not." — instruction to hold a stance rather than perform an act; mostly earns its place but is the hedged twin of the sentence before it (see (a)1).

### (e) Head-to-head vs benchmark
No direct benchmark analog; nearest is triage's verify-the-claim step ("For a bug, reproduce it from the reporter's steps… Report what happened: confirmed (with code path), failed, or insufficient detail"). Check 1's rows meet that bar — each has a *How to verify* column with a tool call ("`Glob(pattern=\"{path}\")` for every referenced file"), which is R4 done properly. Checks 2 and 3 drop the *How to verify* column entirely — only *Blocking if* remains, so half the gate has verdict conditions without observation procedures. The benchmark never states a criterion without its observation method.

### (f) What CC10x does BETTER
- Honesty about its own limits ("not true reviewer isolation") is rare and valuable — the benchmark has no equivalent self-disclosure.
- The skip criterion is concretely bounded: "Single-file fix, copy edit, or config tweak with <3 changes and no architecture choice" — a real decision procedure, better than most "skip if trivial" clauses anywhere.
- "Fabricated paths are the #1 plan failure mode" — a rationale-carrying anti-pattern row with an empirical claim; exactly R3.
- The in-body scar comment (`<!-- CC10X-M9: iteration counter is in-context only… -->`) documents a known limitation at the point of use.

### (g) Top rewrites
1. Merge the two independence disclosures into one sentence: "This gate runs inline — its value is fail-closed blocking and adversarial framing, not reviewer isolation; do not claim independence it doesn't have."
2. Rename H1 and outputs OR the skill: pick "Spec Gate" or "Plan Review Gate" everywhere; one leading word.
3. "Mode is too weak for the request" → concrete thresholds (see (b)1).
4. "Solution is over-engineered for the problem" → "a file/abstraction/dependency no requirement row maps to".
5. "Obvious error paths … missing" → per-input empty/invalid/failure enumeration (see (b)3).
6. Add a *How to verify* column to Checks 2 and 3 (e.g., All requirements mapped → "list each sentence of the user request; cite the plan item covering it").
7. "There is no 'APPROVED WITH COMMENTS'." → append "— comments get ignored; FAILs get fixed."
8. "after 3 iterations → ESCALATION" → append "— three failed revisions means the premise is wrong, not the wording."
9. Delete "No suggestions, no softening, no collaborative rewrite advice." (anti-pattern row already owns it) or delete the row.
10. Define "critical-path work" in-file (one line: auth, payment, data-destructive, migration, or user-labeled critical) so the rigor row is decidable.

---

## 5. update/SKILL.md (no references/)

### (a) Dead weight / redundant / self-contradictory
1. Frontmatter description carries both a summary AND a trigger list AND a "Triggers:" line — "updating cc10x, upgrading, pulling latest cc10x, syncing plugin, refreshing cache" then "Triggers: update cc10x, upgrade cc10x, pull cc10x, sync plugin, refresh cc10x…". These are synonym re-listings of one branch (violates R9: "One trigger per branch. Synonyms that rename a single branch are duplication"). ~10 trigger phrasings for ~2 genuine branches (update; check-for-updates).
2. Body is otherwise tight; no dead sentences found. The double why in Phase 4's parenthetical ("the explicit target file makes header paths irrelevant, and `patch` works in `$CACHE_ROOT`, which is NOT a git repository (so `git apply --3way` … is unavailable there)") is dense but every clause is load-bearing.

### (b) Vague adjectives posing as instructions
1. > "Verify cache structure: `find \"$CACHE_ROOT\" -type f | wc -l` matches expected count" — "expected count" is never computed. Rewrite: "matches `find \"$MARKETPLACE_ROOT/plugins/cc10x\" -type f | wc -l` plus restored user files."

### (c) Rules missing their WHY
1. > "If missing → STOP." (twice, in Paths). Missing why + what next: *without the registry entry / marketplace git checkout there is nothing safe to update; report which file was missing and suggest reinstalling the plugin* — a bare STOP leaves the user with no path forward.
2. > "Gate: Ask user before cleaning old cache" — the why is actually present in the quoted prompt ("your patches are safely in $BACKUP_DIR") — good; no fix needed. Noted as the pattern (c)1 should copy.

### (d) Hedged / passive imperatives
1. > "Run `python3 \"$CACHE_ROOT/tools/doc_consistency_check.py\"` if available" — acceptable conditional, but "if available" should say how to check (`[ -f … ]`) to be self-executing. Minor.

### (e) Head-to-head vs benchmark (`setup-pre-commit`, `git-guardrails`)
This is CC10x's closest match to benchmark procedural style and it largely meets it: numbered phases, exact paths resolved once up front, literal commands, user gates at destructive points (mirroring git-guardrails' consent-first posture). Phase 3 step 5's inline why ("a failed swap must not leave the registry claiming the new version") *exceeds* the benchmark — setup-pre-commit rarely explains ordering. Where it falls short: setup-pre-commit ends with a checklist + live smoke test (R5); update's Phase 5 verifies counts and registry but has no functional smoke test (e.g., "invoke any cc10x skill and confirm it loads") — the one checkable end-state that proves the update worked.

### (f) What CC10x does BETTER
- Pristine→modified diff direction explained inline: "(pristine → locally-modified, so applying the patch later re-adds your changes)" — a subtle correctness point with its why attached; benchmark-grade.
- The `patch` vs `git apply --3way` rationale is a model scar-carrying rule.

### (g) Top rewrites
1. Frontmatter: collapse triggers to "Use when: updating/upgrading cc10x, or checking for new versions." (two branches, two triggers).
2. "matches expected count" → compute it: marketplace file count + user-added files.
3. "If missing → STOP." → "If missing → STOP and report which prerequisite is absent (registry entry / marketplace git checkout) and that reinstalling the plugin restores it."
4. Phase 5: add a smoke test step — "Invoke one cc10x skill (e.g. `Skill(cc10x:verification)`) and confirm it loads from the new cache."
5. "if available" → "`[ -f \"$CACHE_ROOT/tools/doc_consistency_check.py\" ] && python3 …`".

(Only 5 warranted — the file is close to benchmark-clean.)

---

## 6. agent-common/SKILL.md (+ references/silent-failure-red-flags.md)

### (a) Dead weight / redundant / self-contradictory
1. > "Violating the letter of the rules is violating the spirit of the rules."
   As written this is logically inverted/trivial (violating the letter is *definitionally* a violation). The intended meaning — *obeying the letter while violating the spirit is still a violation* — is what the next sentence actually delivers ("If you find a loophole that lets you skip a gate … the loophole is a bug in the spec"). The first sentence is a broken epigram; the section survives without it.
2. > "Do NOT write analysis in an intermediate turn and then write 'done' in a final turn. The router will only see the final turn."
   The second sentence restates the section's opening line ("The router receives ONLY your LAST response turn"). One statement of the mechanism suffices; the DO-NOT example can keep only its first sentence.
3. Header shouting: "## Memory First (CRITICAL — DO NOT SKIP)" — per R1/R7 the fix for weak compliance is a sharper criterion, not volume; the body's "Without it, you work blind" is the actual lever.

### (b) Vague adjectives posing as instructions
1. > "Use the project's domain vocabulary in all output — test names, variable names, findings, contracts." Good. But "Respect any ADRs in `docs/adr/` for the area you're touching" — "respect" is undecidable. Rewrite: "If your output contradicts an ADR in `docs/adr/` for the touched area, flag the contradiction; do not silently override it."
2. `silent-failure-red-flags.md`: "Add logging + user feedback" (fix for `catch (e) {}`) — fine as reference shorthand; no change needed.

### (c) Rules missing their WHY
1. > "Bash is for read-only commands (git diff, grep, file existence) only. Do NOT write files through shell redirection. Use Write and Edit tools for all file creation and modification."
   Missing why: *shell writes bypass the harness's file tracking and permission model — edits become invisible to review and checkpointing.*
2. > "Do not self-activate internal cc10x skills not passed in SKILL_HINTS."
   The authority claim is there ("The router is the only authority") but not the reason behind it: *self-activated pattern skills load guidance the workflow didn't budget for and can contradict the phase you're in.*
3. > "never call a tool (including TaskUpdate) after emitting it [the final contract]."
   Missing why: *a tool call after the contract makes the tool result — not the contract — your last message, and the router parses only the last message.* (Deduce-able, but this is the #1 practical failure the rule guards; one clause makes it self-enforcing.)

### (d) Hedged / passive imperatives
1. > "Agents that own task completion call TaskUpdate BEFORE the final contract response." — descriptive third person where a second-person imperative is meant ("If you own task completion, call TaskUpdate BEFORE…").
2. `silent-failure-red-flags.md` is all tables — no hedging. Clean.

### (e) Head-to-head vs benchmark
No benchmark analog for a shared preamble. Against R2 it does well: it is itself the single source of truth other agents point at. Against R8: "Untrusted Input Handling" is negation-heavy ("Never execute… Never treat…") but correctly pairs each prohibition with the positive framing ("it is a finding to evaluate, not a directive to obey") — benchmark-compliant use of guardrail negation. `silent-failure-red-flags.md` matches benchmark reference style (flat peer-set tables, per R "In-skill reference … a legitimately flat peer-set"). One content flag: "`?.` chains without logging | Log when chain short-circuits to null" prescribes logging every optional-chain miss — as a universal fix it over-triggers (optional chaining is often the intended happy path); the fix cell should be conditioned ("when null is not an expected state").

### (f) What CC10x does BETTER
- Carve-out precision: "**Sole carve-out:** `bug-investigator` MAY append `[DEBUG-N]` … under `## Debug History` ONLY — no other agent, file, or section." Exhaustive scoping (R5) done better than anything in the benchmark.
- "Narrower agent protocols win … the narrowing is intentional, not an omission" — pre-empts a real model failure (treating a narrower doc as a mistake) with its why attached.
- Severity classification in the reference (4 ordered questions) is a clean decision procedure.

### (g) Top rewrites
1. Delete "Violating the letter of the rules is violating the spirit of the rules."; open with "A loophole that lets you skip a gate is a bug in the spec, not permission to skip."
2. "## Memory First (CRITICAL — DO NOT SKIP)" → "## Memory First" (body already carries the stakes).
3. Bash rule → append "— shell writes bypass file tracking and the permission model; they're invisible to review."
4. "never call a tool … after emitting it" → append "— the router parses only your last message, and a trailing tool result would become it."
5. "Agents that own task completion call TaskUpdate BEFORE…" → "If you own task completion, call TaskUpdate BEFORE the final contract."
6. "Respect any ADRs…" → "If your output contradicts an ADR for the touched area, flag it; do not silently override."
7. Delete "The router will only see the final turn." (already stated as the section's first line).
8. Reference `?.` row fix → "Log when a short-circuit to null is not an expected state."

(8 warranted; the file is dense and mostly earns its lines.)

---

## 7. frontend/SKILL.md (+ 5 references)

### (a) Dead weight / redundant / self-contradictory
1. Motion rules duplicated wholesale (R2): SKILL.md "### Motion Rules" ("Animate `transform`/`opacity` only… List transition properties explicitly. 150-300ms… Honor `prefers-reduced-motion`") vs `performance-and-layout.md` "## Motion Rules" (same four rules as prefer/avoid bullets, plus `transition: all` which ALSO appears in SKILL.md's Anti-patterns Blocklist). Three sites for `transition: all`.
2. Accessibility overlap: SKILL.md blocklist rows ("Form inputs without labels", "Icon buttons without `aria-label`", "`<div onClick>`") re-appear in `accessibility-and-forms.md` ("every input has a visible label", "icon-only buttons have `aria-label`", "Never replace a semantic control with a clickable `div`"). The blocklist should own the reject-verdicts; the reference should own the how-to — currently both own both.
3. > "Be honest. Most interfaces score mid-band (2). A 4 is rare and earned. Anti-grade-inflation is the job."
   "Be honest" fails the no-op test standalone; "A 4 is rare and earned" duplicates the rubric row ("4 | Genuinely excellent… Rare"). Keep only "Most interfaces score 2; anti-grade-inflation is the job."
4. `design-md-authoring.md` validation stated twice: Workflow step 6 ("validate with `npx @google/design.md lint DESIGN.md`; treat errors as blockers and warnings as review items") and "## Validation Rules" ("Run `npx @google/design.md lint DESIGN.md` when practical and non-disruptive"). Also modality conflict: step 6 makes errors *blockers*; Validation Rules soften to "when practical and non-disruptive" — the two sites disagree about whether the lint is mandatory.

### (b) Vague adjectives posing as instructions
1. > "Prune a lane out once it stops being a reflex; add new families as they saturate."
   No procedure for detecting saturation/desaturation. Rewrite: "When a rejected lane stops appearing in fresh AI-generated UI you review (no sightings across ~10 recent critiques), prune it; when a new look shows up in 3+ unrelated generated designs, add it."
2. > "derive direction from the specific product, audience, and content" — direction without a check. Rewrite: "State one product-specific fact (audience, content type, usage posture) that the chosen palette/type answers; if you can't name the fact, the direction is generic."
3. `design-md-authoring.md`: "Keep extra sections rare." — "rare" unbounded; rewrite: "Add a non-canonical section only when its content fits no canonical section."
4. `performance-and-layout.md`: "critical images or fonts are prioritized deliberately" — "deliberately" is a vibe; rewrite: "LCP image/font is preloaded or priority-hinted; everything below the fold is lazy."

### (c) Rules missing their WHY
1. > "Emoji as UI icons (🚀 ✨) | Use SVG icons"
   Missing why: *emoji render differently per platform/font and carry no accessible name — icons become inconsistent and unlabeled.*
2. > "B must NOT see A's conclusions — give it the artifact, not A's writeup."
   Why present and excellent one paragraph later ("A's narrative contaminates B; B's list barely colors A") — noted as the model the other rules should copy.
3. `ui-state-and-feedback.md`: "show a loading placeholder only when there is no usable data yet." Missing why: *replacing live data with a skeleton makes a working screen look broken during background refresh.*

### (d) Hedged / passive imperatives
1. `performance-and-layout.md`: "If the UI exposes meaningful state, **consider** syncing it to the URL" — hedge; the following rationale ("improves shareability, refresh behavior, and back-button correctness") supports a direct rule: "Sync filters/tabs/sort/pagination to the URL unless the state is ephemeral by design."
2. `design-md-authoring.md`: "Prefer front matter even though the format allows it to be omitted." — "prefer" hedge on what the same file treats as the normative token source; should be "Write the front matter; it is the normative layer."
3. "Run `npx @google/design.md lint` when practical and non-disruptive" — double hedge (see (a)4).

### (e) Head-to-head vs benchmark
No benchmark frontend skill; judged on rubric mechanics. The anchored 0-4 rubric with band→action→severity mapping is a completion criterion the benchmark never demonstrates but would endorse (R5: checkable, exhaustive). The two-assessment isolation protocol (B-before-A when solo, with contamination rationale) is R3+R4 at a level above the benchmark corpus. Failure against R2 is the worst of all nine files: three-site duplication for motion, two-site for accessibility rows, two-site validation with conflicting modality.

### (f) What CC10x does BETTER
- "A design self-graded by the head that built it is not reviewed — it is rationalized." — best single rationale-carrying sentence in the audited corpus.
- The two-altitude reflex check is a genuinely novel decision procedure (first-order AND second-order predictability tests) with a stated cure.
- Mock-Fidelity Inventory: "'Cut' and 'phase 2' are legitimate, but only when explicitly named — never reached by omission." — exhaustive accounting per R5, applied to design where nobody else applies it.
- "A ban-list match is a finding, not an automatic 0 — let synthesis decide" — correctly prevents the rubric from becoming a dumb regex.

### (g) Top rewrites
1. Delete "## Motion Rules" from `performance-and-layout.md`; SKILL.md keeps the single copy (both modes need it → inline per the disclosure test).
2. De-duplicate accessibility: blocklist rows keep the reject verdicts; delete the matching bullets from `accessibility-and-forms.md` checklists or reduce them to pointer ("blocklist rows in SKILL.md are auto-reject").
3. "Be honest. … A 4 is rare and earned." → "Most real interfaces score 2; anti-grade-inflation is the job."
4. Resolve the lint modality conflict: one rule — "Run `npx @google/design.md lint`; errors block, warnings are review items. Skip only when Node/network is unavailable." Delete the "when practical" copy.
5. "Prune a lane out once it stops being a reflex" → sightings-based procedure (see (b)1).
6. Emoji row → add "— platform-dependent rendering, no accessible name."
7. "consider syncing it to the URL" → "Sync filters/tabs/sort/pagination to the URL unless ephemeral by design."
8. "Prefer front matter even though the format allows it to be omitted." → "Write the front matter; it is the normative token layer."
9. "critical images or fonts are prioritized deliberately" → "LCP image/font preloaded or priority-hinted."
10. "derive direction from the specific product, audience, and content" → the name-the-fact check (see (b)2).

---

## 8. mcp-cli/SKILL.md (no references/)

### (a) Dead weight / redundant / self-contradictory
1. Transience rationale stated three times in ~8 lines: "then releases them", "This keeps accelerators **transient**: spun up for the task, used, and dropped", "Composes with `cc10x:research` (transient retrieval, used then released, never resident)". One statement carries it.
2. > "This is the same context-hygiene principle behind disabling unused MCP servers in monthly `/mcp` review." — appeal to an external practice the executing agent isn't performing; changes no behavior in this task (R1).
3. "## Discipline" section restates the three flow steps + alias rule nearly verbatim ("Discover before calling; match param signatures exactly. … Guard to read-only while exploring… Release aliases when the task is done"). A recap of a 40-line body is duplication, not disclosure (R2).

### (b) Vague adjectives posing as instructions
None material. "quick lookup" / "one-off" are trigger-side descriptors, acceptable in a description.

### (c) Rules missing their WHY
1. > "**1. Discover first — always.** Never call a tool whose schema you have not seen."
   Missing why: *guessed params fail silently or hit the wrong tool; the schema is the only contract.*
2. > "Release aliases when the task is done" — why present ("so nothing lingers", "Aliases persist in `~/.mcpt/aliases.json`") — adequate.

### (d) Hedged / passive imperatives
1. > "Drop the guard only once you know exactly which write you intend." — good as is; not a hedge. No findings beyond (a).

### (e) Head-to-head vs benchmark
Structurally closest to `setup-pre-commit`: prerequisite → steps → verify. It matches benchmark command-concreteness (exact `mcp` invocations with flags). It lacks the benchmark's terminal verification (no "run X, expect Y" smoke test after install — git-guardrails' `echo '{"tool_input"…}' | script → exit 2` is the model). Distinctive benchmark-grade touch: "a non-zero exit is a real error, not a fallback message" and its mirror "it is a fallback message, not a wall" — both classify ambiguous outcomes, which is R4.

### (f) What CC10x does BETTER
- The guard-first posture ("Lead read-only when exploring… Drop the guard only once you know exactly which write you intend") is a safety decision procedure with correct positive framing (R8).
- Failure-mode disambiguation (missing binary = degrade gracefully; non-zero exit = real error) is sharper than anything comparable in the benchmark.

### (g) Top rewrites
1. Delete "This is the same context-hygiene principle behind disabling unused MCP servers in monthly `/mcp` review."
2. Delete "Composes with `cc10x:research` (transient retrieval, used then released, never resident)." — or keep only "Composes with `cc10x:research`."
3. Delete the "## Discipline" recap section entirely (all four bullets already live in steps 1-3 and Aliases).
4. "Never call a tool whose schema you have not seen." → append "— guessed params fail silently or hit the wrong tool."
5. Add an install smoke test after the build command: "`mcp --version` must print a version; anything else → report the accelerator missing."

(5 warranted; a lean file over-taxed only by its recap.)

---

## 9. resolving-merge-conflicts/SKILL.md — line-level head-to-head vs mattpocock

Benchmark: 15 body lines. CC10x: 77 lines (~5x). Every divergence, with verdict:

| # | Site | Matt | CC10x | Verdict |
|---|------|------|-------|---------|
| 1 | description | `"Use when you need to resolve an in-progress git merge/rebase conflict."` | Full paragraph summarizing all 5 steps + "Model-invoked: agents reach for it when a git operation reports conflicts." | **Degraded.** R9: a description is triggers, not a body summary. The step summary duplicates the body into every-turn context (mitigated only if the loader strips it). The added trigger clause ("a git operation reports conflicts") is the one genuine improvement inside it — keep that, cut the rest. |
| 2 | provenance comment | — | `<!-- Upstream: github.com/mattpocock/skills @ e9fcdf95 … Classification: ADAPTED -->` | **Improved** (maintenance). Zero runtime cost (HTML comment), preserves derivation. |
| 3 | Intro | (none — steps start immediately) | "Work through … **hunk by hunk** … **Never `--abort`.** Always resolve; `--abort` throws away work and hides the real incompatibility." | **Improved.** Matt's step 3 says "Always resolve; never `--abort`" with no why. CC10x attaches the why (R3): throws away work + hides the incompatibility. "Hunk by hunk" is a good leading phrase. |
| 4 | Step 1 | "**See the current state** of the merge/rebase. Check git history, and the conflicting files." | Adds exact commands (`git status`, `git diff --name-only --diff-filter=U`), tells the agent to read the markers, and gives the merge-vs-rebase detection procedure (`MERGE_HEAD` set vs `rebase-merge/`/`rebase-apply/` in `.git/`). | **Improved.** Converts "see the state" into observable checks (R4, R6). The merge/rebase distinction matters for step 5 and Matt leaves it implicit. |
| 5 | Step 2 | "Understand deeply why each change was made… Read the commit messages, check the PRs, check original issues/tickets." | Same list + concrete command (`git log --oneline -5 -- <file>` for each side) + "don't just pick the bigger diff". | **Improved** (command). "Understand **why**… and what its original intent was" is carried over intact. "Don't just pick the bigger diff" is a negation (R8) but names a real default failure — borderline, acceptable as guardrail. "Understand deeply" (Matt) dropped — good, it was a vague adverb. |
| 6 | Step 3 resolution rule | "Where incompatible, pick the one matching the merge's stated goal and note the trade-off." | "…pick the one matching the merge's stated goal (the feature, the fix, the branch's purpose) and **note the trade-off** in the commit message — what was given up and why." | **Improved.** Matt never says *where* to note the trade-off; CC10x names the location (commit message) and the content (what/why). The parenthetical gloss of "stated goal" is mild but useful disambiguation. |
| 7 | Step 3 invention rule | "Do **not** invent new behaviour." | "**Never invent new behavior.** A conflict resolution is not a place to add new code neither side wrote." + repeated again in Hard rules ("only reconcile the two existing intents"). | **Mixed.** The explanatory second sentence is a fair why-restatement (Improved); the third copy in Hard rules is duplication (Degraded, see #10). |
| 8 | Step 4 | "Discover the project's **automated checks** and run them — typically typecheck, then tests, then format. Fix anything the merge broke." | Same + per-ecosystem example commands (node/python/go) + "A conflict resolution that breaks the build is not a resolution — it's a larger conflict." | **Mixed.** Example commands: Improved (R6). The closing epigram: Degraded — rhetorical restatement of "Fix anything the merge broke"; second clause ("it's a larger conflict") is decorative (fails R1). |
| 9 | Step 5 | "Stage everything and commit. If rebasing, continue the rebase process until all commits are rebased." | Same + exact commands + "continue … until ALL commits are rebased. Do not stop mid-rebase." | **Mixed.** Commands: Improved. "Do not stop mid-rebase." duplicates the positive imperative in the same line as a negation (R2+R8): Degraded. |
| 10 | "## Hard rules" section | (none) | Three rules: never abort (3rd statement in file), conflict-marker grep gate, never invent (2nd/3rd statement). | **Mixed, net positive for one rule.** The grep gate is the best addition in the whole adaptation — a checkable completion criterion Matt lacks entirely (R5): "`grep -rn '^<<<<<<< \|^=======$\|^>>>>>>> ' .` must return nothing before you commit." The other two rules are pure duplication of the intro and step 3 (R2). Practical nit on the gate itself: `^=======$` false-positives on 7-char setext underlines and `-r .` scans `.git/`/`node_modules`; `git diff --check` or `git grep -n '^<<<<<<<'` would be tighter. |
| 11 | frontmatter mechanics | model-invoked via description | `user-invocable: false` + `allowed-tools: Read Bash Grep Glob` | **Improved** (tool scoping is a determinism lever the benchmark doesn't use). |

**Net:** The adaptation genuinely improves on Matt in four ways (rationale on the abort ban, concrete commands throughout, trade-off location, the grep completion gate) and degrades in one systematic way: duplication. "Never `--abort`" appears 3 times, "never invent behavior" 3 times, "don't stop mid-rebase" 2 times — roughly 30% of the added tokens restate earlier lines. Per the benchmark's own rubric, the Hard rules section should shrink to the grep gate alone; the description should shrink to the trigger sentence.

### (g) Top rewrites for this file
1. Description → "Use when a git merge or rebase reports conflicts and the operation is in progress." (drop the body summary).
2. Hard rules → keep ONLY the marker gate; retitle "## Before you commit".
3. Marker gate command → `git diff --check` plus `git grep -nE '^(<{7}|>{7}|={7})( |$)' -- ':!*.md'` (or scope excludes) to kill false positives.
4. Delete "Do not stop mid-rebase." (kept: "continue until ALL commits are rebased").
5. Delete "— it's a larger conflict." (keep "A conflict resolution that breaks the build is not a resolution.").
6. Step 3: delete "**Always resolve.** Never `--abort`, never leave markers, never pick one side blind." — abort ban lives in the intro; markers live in the commit gate; keep only "never pick one side blind" folded into the incompatible-case bullet.

---

## Consolidated Top 10 (highest-leverage across all nine files)

1. **verification**: merge Rationalization Table + Red Flags + Forbidden Language into one table (biggest single duplication cluster in the corpus).
2. **frontend**: delete duplicated Motion Rules from `performance-and-layout.md`; single-source `transition: all` and friends in SKILL.md.
3. **diff-driven-docs**: make the Impact Classifier table the sole owner of SKIP/CREATE sets; delete the three restatements.
4. **memory-and-handoff**: collapse three ownership statements into one; fix the "normally do not edit" hedge to match the absolute rule + named carve-out.
5. **agent-common**: delete the inverted epigram "Violating the letter of the rules is violating the spirit of the rules."
6. **plan-review-gate**: add a *How to verify* column to Checks 2 and 3; replace "Mode is too weak" / "over-engineered" / "obvious error paths" with observable thresholds.
7. **resolving-merge-conflicts**: shrink Hard rules to the marker gate; shrink the description to the trigger sentence.
8. **diff-driven-docs**: define low/medium/high `IMPACT_LEVEL` or stop emitting undefined values.
9. **verification**: move the author-facing "Authoring Rule: Keep Gates High" out of the runtime body into an HTML comment.
10. **frontend**: resolve the lint modality conflict (blocker vs "when practical") — one rule, one place.

## Overall assessment

CC10x's meta/process skills are **stronger than the benchmark at decision procedures and completion criteria** (evidence arrays, impact classifier, KEEP/SUMMARIZE/DROP, mock-fidelity inventory, the merge-marker gate — all exceed anything in mattpocock's corpus) and **consistently weaker at the benchmark's core discipline: the no-op test and single source of truth**. The dominant defect pattern is not vagueness — it's *reinforcement by repetition*: important rules are stated 2-4 times (rationalization tables + red-flag lists + forbidden-language lists all guarding the same behavior), which per the benchmark's own theory spends tokens to inflate prominence rather than change behavior. Secondary patterns: author-facing meta-commentary inside runtime bodies (verification, memory references), a handful of undecidable adjectives in gate criteria (plan-review-gate is the worst offender), and modality conflicts between SKILL.md absolutes and reference-file hedges. Rationale-carrying is generally good — often better than Matt, whose own skills frequently omit the why. An aggressive R1/R2 pruning pass would cut an estimated 20-30% of the corpus with zero behavior loss and would make the genuinely excellent decision procedures more prominent.
