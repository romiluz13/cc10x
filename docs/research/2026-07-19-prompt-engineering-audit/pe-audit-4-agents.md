# Prompt-Engineering Audit — cc10x Agent Prompts (11 agents + agent-common)

Audit date: 2026-07-19. Lens: prompt engineering / LLM-instruction quality only. Rubric built from `/Users/rom.iluz/Dev/mattpocock-skills/` (writing-great-skills, tdd, code-review, diagnosing-bugs, implement). Functional files only; no historical audits consulted.

---

## STEP 1 — Rubric (from mattpocock-skills)

Distilled criteria, with exemplars quoted from the source:

1. **Predictability is the root virtue.** "A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same _process_ every run — is the root virtue" (writing-great-skills:7). Every sentence must earn its place by changing behavior.
2. **No-op test, applied per sentence.** "hunt **no-ops** sentence by sentence … when one fails, delete the whole sentence rather than trim words from it" (writing-great-skills:59). "A weak leading word (_be thorough_ when the agent is already thorough-ish) is a no-op; the fix is a stronger word (_relentless_)" (:82).
3. **Decision procedures over adjectives.** diagnosing-bugs never says "reproduce reliably" — it says: "**Red-capable** … it drives the actual bug code path and asserts the **user's exact symptom**" and "you can name **one command** … that you have **already run at least once** (paste the invocation and its output)" (diagnosing-bugs:53-58). A checkable completion criterion, not a virtue.
4. **Rationale-carrying rules.** "Why bother: a minimal repro shrinks the hypothesis space in Phase 3 … and becomes the clean regression test in Phase 5" (diagnosing-bugs:76). "Single-hypothesis generation anchors on the first plausible idea" (:84). Rules travel with their WHY so the model can generalize under novel pressure.
5. **Worked examples that match the formula.** code-review's smell baseline gives each smell as *what it is → how to fix*, e.g. "**Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type" (code-review:48). tdd's tautological-test rule includes the exact code shape: "`expect(add(a, b)).toBe(a + b)`" (tdd:29).
6. **Explicit stopping conditions.** "Done when **every remaining element is load-bearing** — removing any one of them makes the loop go green" (diagnosing-bugs:78). "If you catch yourself reading code to build a theory before this command exists, **stop**" (:60).
7. **Leading words compress instruction.** "_tight_", "_red_", "_tracer bullet_", "_seam_" — "anchors a whole region of behaviour in the fewest tokens, by recruiting priors the model already holds" (writing-great-skills:63).
8. **Positive phrasing over negation.** "steering by prohibition backfires … Prompt the **positive** — state the target behaviour so the banned one is never spoken; keep a prohibition only as a hard guardrail … and even then pair it with what to do instead" (writing-great-skills:83).
9. **Single source of truth; duplication inflates prominence and drifts.** (:55, :79).
10. **Sentence economy as house style.** implement/SKILL.md is 16 lines total and fully operational.

---

## STEP 2 — Per-Agent Audit

Legend for categories: (a) dead-weight/redundant/contradictory, (b) vague adjectives without procedure, (c) rules missing WHY, (d) ambiguities resolved wrongly under pressure, (e) persona/opening, (f) output-format as prose.

### 0. Cross-cutting: agent-common vs. agent bodies

The single biggest prompt-quality issue in the fleet is **agent-common and agent bodies fighting over task completion**.

**(a/d) CONTRADICTION — TaskUpdate.** agent-common's SINGLE FINAL RESPONSE RULE step 2 says, unconditionally: "**Stop your turn — the router handles task completion automatically.**" (agent-common:60). But five agents (bug-investigator:123, component-builder:100-102, doc-syncer:132-134, planner:78-80, researcher:100-108) command the opposite: "Call `TaskUpdate({ taskId: … status: 'completed' })` directly — BEFORE emitting your final contract response. Writing text is NOT sufficient." agent-common:53 does carve this out ("Agents that own task completion call TaskUpdate BEFORE the final contract response") — but that carve-out sits in the CONTRACT Envelope section, while the SINGLE FINAL RESPONSE RULE, seven lines later, restates the unconditional "router handles task completion automatically" without the carve-out. An LLM that internalizes the later, bolder sentence will skip TaskUpdate. The two shared-preamble sentences need to agree with each other, not rely on the agent body to break the tie.

**(a) Boilerplate re-stated with drift.** Memory First, SKILL_HINTS, Key anchors, SINGLE FINAL RESPONSE RULE, and the Memory Notes format are all defined in agent-common yet re-pasted (with wording variance) into architecture-scanner, code-reviewer, failure-hunter, doc-syncer, and triage-agent. Repetition of a gate can be intentional; *variant* repetition is drift bait:
- code-reviewer:48 — "Do not self-activate internal CC10X skills, including `cc10x:frontend`."
- failure-hunter:48 — "Do not self-load internal CC10X skills. The router is the only authority…"
- agent-common:42 — "Do not self-activate internal cc10x skills not passed in SKILL_HINTS."
Three phrasings of one rule. The model cannot tell whether the differences are meaningful (is `cc10x:frontend` special-cased only for the reviewer?).

**(a) "Mode: READ-ONLY" stated twice in one file.** code-reviewer:24 "**Mode:** READ-ONLY. Do NOT edit any files…" and code-reviewer:40 "**Mode:** READ-ONLY. You do NOT have Edit tool…" — same rule, two wordings, 16 lines apart. failure-hunter has the same double (lines 19 and 41).

**(a/d) Anchors for a forbidden file.** code-reviewer:52-55 lists "Key anchors … activeContext.md: `## Learnings`, `## Recent Changes`" — in an agent explicitly forbidden from reading activeContext.md (:38). The anchors are for Memory Notes routing, but nothing says so; under pressure this reads as an invitation to open the file the anti-anchoring rule just banned.

**(c) Shell Safety rule has no WHY.** agent-common:76 "Do NOT write files through shell redirection. Use Write and Edit tools…" — no rationale (auditability? permission hooks? checkpointing?). Per the rubric, a WHY-less prohibition is obeyed literally and generalized wrongly (e.g. the model may think `tee` is fine).

**(e) agent-common has no orientation cost** — it is preamble, fine. But researcher loads it and thereby inherits a mandatory three-file memory read that researcher's own body never uses or mentions; for a web-research agent this is pure ritual (a no-op by the rubric's test) plus latency.

**(f) Memory Notes format** (agent-common:66-72) is exemplified once and consistently reused — good. But agents' YAML `MEMORY_NOTES:` keys (`learnings/patterns/verification/deferred`) and the prose `### Memory Notes` section duplicate the same data in two formats in one response; no agent file says whether they must match. researcher's contract omits `patterns`/`deferred` keys entirely — inconsistent with the shared format it loads.

---

### 1. architecture-scanner.md

**(e) Opening: good.** "**Core:** Surface architectural friction and propose deepening opportunities … The aim is testability and AI-navigability. Never write production code" — identity, goal, non-goal in three sentences. Strong.

**(b) "Explore organically"** (:42) — vague verb posing as method. The bullets that follow are real questions, but "organically" adds nothing and invites drift. Rewrite: "Walk the codebase module by module, asking the five friction questions below; stop when you have 3-5 candidates or have covered the hot spots from step 1."

**(b) Recommendation strength badges** `Strong | Worth exploring | Speculative` (:63) have no assignment criteria anywhere. Two runs will badge the same candidate differently — the exact predictability failure the rubric exists to prevent. Rewrite: "Strong = deletion test says 'concentrates' AND the module appears in git-log hot spots; Speculative = based on a single reading with no churn evidence; else Worth exploring."

**(a/d) "tell the user: 'Which of these would you like to explore?'"** (:71) fights the SINGLE FINAL RESPONSE RULE it inherits: the router, not the user, receives the final turn, and the Output section then prescribes a contract format with no such question in it. The model must choose between "tell the user X" and the mandated output template. Delete the sentence or move the question into the template's Summary.

**(c) "Use Tailwind via CDN … Mermaid via CDN"** (:54) — no WHY (self-contained report? offline?), and no fallback if CDN-blocked. Minor.

**(g) Good:** deletion test is a genuine decision procedure with its own worked verdict ("'Concentrates' = deep (leave it); 'just moves' = shallow"); Memory-first block; scoping by `git log` hot spots carries its WHY ("Deepening a module pays off by making future changes to it easier").

**(f)** Output template fully exemplified (envelope, YAML, prose table). Clean.

---

### 2. bug-investigator.md

**(e) Opening: excellent.** "**Core:** Evidence-first debugging. No root cause, no fix. No variant coverage, no confidence. No loop, no hypothesis." Four aphorisms that each gate a behavior. Best opening in the fleet.

**(a/d) CONTRADICTION in Decision Checkpoints** (:91-95): header says "return `STATUS: BLOCKED` when:" but the third bullet says "Multiple valid root causes (confidence gap <20 between H1/H2) → `STATUS: INVESTIGATING`". A bullet under a "return BLOCKED" header that returns something else is exactly the kind of local contradiction an LLM under pressure resolves by coin flip. Retitle: "Decision Checkpoints — stop and return the named STATUS when:".

**(d) Confidence numbers with no procedure.** "H1/H2/H3 with 0-100 confidence. Proceed to fix only when one reaches 80+" (:79). Nothing tells the model what earns 80 vs 60. The Causal Chain Gate (:80) is the real criterion — bind them: "Confidence ≥80 requires: causal chain complete with no 'somehow' links AND at least one confirmed prediction from instrumentation." Otherwise the model will simply assert 85.

**(d) Exit-code fields read as booleans.** `TDD_RED_EXIT: [1 if regression test failed before fix, null if missing]` (:139). Is this the literal process exit code (which could be 2) or a flag? Contract rule "requires `TDD_RED_EXIT=1`" suggests literal 1, which would wrongly fail a runner exiting 2 on assertion failure. Same in component-builder. Say: "the observed exit code; any non-zero behavioral failure counts — record the actual code."

**(f) "Regression:" / "Variant:" scenario name prefixes are never exemplified.** Contract rule :197 requires a "`Regression:` scenario" and "`Variant:` scenario", but the SCENARIOS template (:169-178) shows `name: "[scenario name]"` with no prefixed example. A fresh LLM will not infer that the *name field must start with the literal string* `Regression:`. Add one example row per prefix.

**(b) "when low-cost"** (:84, blast radius adjacent scan) — no threshold. Rewrite: "adjacent files: scan only files that import the fixed symbol; cap at 5 files."

**(c) Missing WHY:** "Use `console.error`/stderr, not the app logger" (:58) — the reason (app logger may be buffered/filtered/the thing under test) is absent, so the model can't generalize to e.g. print vs logging in Python.

**(g) Good:** construction ladder with rank order and stop rule; No-Loop-No-Hypothesis fail-closed gate with a concrete ask list; Assumption Audit ("Many wrong hypotheses are correct hypotheses tested against wrong assumptions" — a WHY that earns its tokens); flaky-rate notation `3/50` exemplified; Debug History carve-out precisely scoped ("`[DEBUG-N]` lines under `## Debug History` ONLY").

---

### 3. code-reviewer.md (longest file, most findings)

**(e) Opening: good** — Core, Posture, Feedback form, Mode in four labeled lines. "Alternatives are context, not cover" is a genuine leading phrase. But 303 lines total means the highest-value rules (Quote-the-line gate, Zero-Finding Gate) sit 130+ lines deep — sprawl by the rubric's definition.

**(d) THE CONFIDENCE SYSTEM DOES NOT ADD UP.** Three problems:
1. Two meanings of CONFIDENCE collide: per-finding confidence ("Only report issues with confidence ≥80", :18; "auto-demoted to confidence 50", :166) and overall review CONFIDENCE (`min(HARD) capped by avg(SOFT)-10`, :182). Same word, two scales, one YAML field. A model will conflate them.
2. The formula makes CONFIDENCE=100 impossible: perfect code scores HARD 100/100, SOFT 100/100 → cap = 100−10 = 90. So a flawless review caps at 90 — never stated, and it silently interacts with…
3. The Zero-Finding Gate (:130): "if still zero findings after positive-assertion pass, set CONFIDENCE to min(CONFIDENCE, 70) … A zero-finding review at CONFIDENCE >= 90 is invalid" — but per the formula a zero-finding review computes to exactly 90. Is 90 "≥90 invalid" or the formula's own honest output? The gate and the formula give different numbers for the same clean review (70 vs 90) with no precedence rule.
Fix: name two fields (`FINDING_CONFIDENCE` per finding, `REVIEW_CONFIDENCE` overall), state the cap explicitly ("REVIEW_CONFIDENCE maxes at 90 by construction"), and make the zero-finding rule "REVIEW_CONFIDENCE = 70" (not min()) so there is one number.

**(d) Envelope `b` is never defined for this agent.** Step 0 shows `"b":true|false` (:85) and the Output example shows `"b":false` (:240), but unlike bug-investigator ("BLOCKING: true if STATUS != FIXED") or component-builder, no rule maps CHANGES_REQUESTED→b. The YAML block has no BLOCKING field at all. Under pressure the model will guess; the router presumably branches on it. State: "`b:true` iff STATUS=CHANGES_REQUESTED with ≥1 CRITICAL."

**(f) SPEC_COMPLIANCE field is described but exemplified with invalid YAML.** `SPEC_COMPLIANCE: [PASS | list of {bucket, item} … e.g. [{MISSING, "rate-limit guard on /login"}]]` (:257). `{MISSING, "…"}` is not parseable YAML (flow mapping needs `key: value`). A fresh LLM told "emit YAML" and shown this will produce something the router's parser may reject. Show one real YAML example:
```yaml
SPEC_COMPLIANCE:
  - bucket: MISSING
    item: "rate-limit guard on /login"
```
Same disease in `PLAN_DEFECT: [false | brief description…]` and `CANNOT_VERIFY_CROSS_PHASE: [None | requirement(s)…]` — prose-in-brackets instead of two literal alternatives shown.

**(a) Triple-statement of spec-compliance independence.** The rule "spec compliance is separate from code quality and gates on its own" is stated in full at :135 (Pass 6 intro), :140 (Pass 6 bullet), and :303 (SPEC_COMPLIANCE gating paragraph) — three near-identical paragraphs. Ditto PLAN_DEFECT (:132-134 and :299). Sediment; keep one authoritative statement each and a pointer.

**(a) Instructions about a tool the agent doesn't have.** ":210 do NOT call TaskUpdate(status: completed)" — TaskUpdate is not in this agent's `tools:` list. Telling a model not to use a tool it cannot see is dead weight and mildly confusing ("do I have it after all?"). Replace with failure-hunter's phrasing, which at least explains: "this agent does not have that tool."

**(b) "Adversarial multi-dimensional review"** — mostly redeemed by the doubt-theater check and named-hypothesis requirement (real procedures). But "Be opinionated" (:20) is redeemed too ("recommend the strongest one and state why"). Genuinely vague leftovers: "OWASP quick checks" (:92 — which checks? the five bullets that follow are the answer, so "OWASP quick checks" is a dangling label), and "Review scope should be proportional to change size" (:70 — the >10-files rule above it is the procedure; this trailing sentence is a no-op).

**(c) Missing WHY:** the −10 SOFT cap (why 10?); "Cyclomatic complexity > 10" (threshold with no rationale — fine as convention, but paired rules elsewhere carry WHYs, so its absence is felt).

**(g) Good — genuinely state-of-the-art:**
- Quote-the-line gate with its WHY ("proves the finding lives in the code, not in plausible-sounding hallucination") and an auto-demotion consequence — a self-executing evidence standard.
- "Decide the verdict BEFORE writing the final response … line 1 cannot be revised after it is emitted" — names a real autoregressive failure mode and gives the fix (return to tool turns).
- Forbidden-language list (:198) — "looks fine, LGTM, ship it…" — bans the exact verdict-softening tokens.
- Anti-anchoring exception with full rationale (:38) — the best rationale-carrying rule in the fleet.
- Calibration rule (:168): "A stated design rationale from the implementer … is the implementer grading their own work."
- Context Hygiene: named-risk-only reads with a worked example ("risk: lock-ordering inversion; checked: the two other acquire sites…").

---

### 4. component-builder.md

**(e) Opening: strong.** "No code without a failing test first. No work outside the current phase." Plus the leading aphorism "Task completion is not goal achievement" (shared with integration-verifier — good deliberate repetition of a leading phrase).

**(d) The Seam Gate table row is self-inconsistent in tense.** Row 1: "`confirmed` (used plan's seams)"; row 2: "`proposed` (you propose at BUILD_PREFLIGHT)"; row 3: "`proposed` (you proposed at BUILD_PREFLIGHT)" — propose vs proposed across identical cases. Trivial, but in a table the model treats as spec, inconsistency invites the question "is row 2 a different action than row 3?" Make them identical.

**(d) Where does the seam proposal go?** ":65-66 `proposed` (you propose at BUILD_PREFLIGHT)" — but the BUILD_PREFLIGHT token format (:47) is a fixed four-field line with no seam slot: `BUILD_PREFLIGHT: context=pass patterns=pass uncertainty=pass mutation=open`. The model is told to propose seams "at BUILD_PREFLIGHT" in a token that cannot carry them. Under pressure it will either mutate the token format (breaking the hook grep) or silently skip the proposal. Say explicitly: "the proposal lives in TEST_SEAMS in your final contract; BUILD_PREFLIGHT stays exactly four fields."

**(a) False-RED guard duplicated with bug-investigator and the `building` skill** — acceptable as a deliberate gate repetition, but the wording differs slightly everywhere ("import/syntax/collection ERROR" here). Pick one canonical sentence.

**(c) Missing WHY:** "Always use run mode: `CI=true npm test`, `npx vitest run` (NOT `npx vitest`)" — the reason (watch mode never exits; the agent hangs) is absent. A model in a repo using a different runner (pytest, cargo) cannot generalize "avoid watch/interactive modes" without the WHY.

**(d) Coverage gate placement.** "**Coverage gate:** If `coverage-thresholds.json` exists…" (:104) sits *under* the Task Completion heading, after "Call TaskUpdate… BEFORE emitting your final contract response." Reading order implies coverage is checked after completion is signaled. Move it into Process step 5.

**(g) Good:** Decision Checkpoints table (five concrete triggers, each with the required FAIL payload — "FAIL with extra files named"); loop caps with exact counts and REMEDIATION_REASON templates; "Report scope truthfully — Do not narrate partial as success"; the trivial/standard seam matrix; false-RED guard with verbatim examples ("expected 3, received undefined").

---

### 5. doc-syncer.md

**(e) Opening: adequate.** One dense Core sentence. Fine for a haiku-model agent — but precisely because `model: haiku`, this file should be the *most* example-driven, and instead it contains the fleet's longest run-on instruction:

**(a/d) The audit-doc step 2 mega-sentence** (:88): "If an existing doc covers this topic: read it, then apply a targeted update using `Edit`. Record it in `AUDIT_DOCS_UPDATED`. **Also add the path to `DOC_FILES_UPDATED`** — the router override accepts `DOC_FILES_UPDATED` or `AUDIT_DOCS_CREATED` for COMPLETE/PARTIAL, so any updated or migrated audit path MUST appear in `DOC_FILES_UPDATED` too. If the existing doc is a legacy `docs/decisions/` file, migrate it … (read old, write new at the canonical path, delete old) — record the new `docs/adr/` path in both …" — four obligations, a router-internals rationale, and a lazy-migration procedure braided into one paragraph. For a small model this is the highest-risk passage in the fleet. Rewrite as a 4-line checklist.

**(d) Is `glossary` a layer or not?** The Impact Classification section discusses exactly three layers ("all three layers are SKIP", :59) but the output template lists four: `DOC_LAYERS_EVALUATED: - business - technical - audit - glossary` (:150-154). A model following the prose will emit three; one copying the template will emit four; the router presumably validates one of them. Reconcile.

**(a) Shell Safety section duplicates agent-common's verbatim rule** (:19-23 vs agent-common:74-76) — with a doc-syncer-specific addition ("Bash is for `git diff`, `grep`, and file existence checks only") that's actually narrower. Keep only the delta.

**(g) Good:** Read-first / Edit-minimal / Verify-after triple for every doc touch; the IMPACT_LEVEL=none fast path with explicit "Do not open any doc files"; Completion State Rules table mapping each STATUS to a checkable condition; the BASE-not-HEAD~1 rule carries its WHY ("a phase legitimately makes MULTIPLE commits … so HEAD~1 would analyze only the last commit").

---

### 6. failure-hunter.md

**(e) Opening: excellent posture line.** "Assume errors are present until evidence proves otherwise. A neutral scan produces neutral results. Your job is to find problems, not to confirm cleanliness." This is what "adversarial" looks like when written as a procedure-shaping stance rather than an adjective.

**(b) `\|\| defaultValue` — "Masks errors"** (:62) is the fleet's worst false-positive generator. Defaulting is idiomatic and usually correct (`options.timeout || 30`). No decision procedure separates a legitimate default from a masked error. Rewrite: "`|| defaultValue` applied to a *function call's return* where the falsy value signals failure (e.g. `parse(x) || fallback` hiding a parse error) — flag; a default for an optional config value — ignore." Same issue, milder, for "`?.` chains without logging" — flagging every optional chain would bury the report.

**(d) Envelope `b` semantics underdefined.** ":118 `CONTRACT {"s":"ISSUES_FOUND","b":true,"cr":N}` (critical failures found)" — so ISSUES_FOUND with only HIGH issues: is s still ISSUES_FOUND, and is b then false? The STATUS vocabulary is CLEAN|ISSUES_FOUND but the parenthetical binds ISSUES_FOUND to critical. HIGH-only runs are the ambiguous middle a model will resolve inconsistently. State: "s=ISSUES_FOUND when any CRITICAL or HIGH exists; b=true only when CRITICAL>0."

**(c) The 200-character OUTPUT QUALITY GATE has no WHY** and is a weird proxy (character-counting one's own prose). The real intent — "the router treats near-empty output as a failed run" — is stated for the single-response rule but not here. Also (a): the gate restates "full output always required" three times (:144, :153-157, :159-160).

**(a) Red Flags table + Language-Specific table duplicated verbatim in `references/silent-failure-red-flags.md`.** Two sources of truth for the same tables; they have already begun life as exact copies and will drift. Keep the reference file, point at it — or delete the reference (nothing in the fleet points to it).

**(g) Good:** Zero-results path (":123 'Nothing found' is a valid audit result. It is NOT permission to skip output") — anticipates a real small-model failure; Zero-Results Suspicion Gate with a concrete floor ("at least 3 concrete error-handling sites … with file:line evidence"); severity decision tree (4 yes/no questions); GOOD/BAD code pair; quote-the-line gate with auto-demotion; scoping heuristic with the BASE WHY.

---

### 7. integration-verifier.md

**(e) Opening: strong.** "Verify that the phase achieved its goal, not that prior agents said it did" — the auditor identity in one sentence.

**(d) Scenario-status arithmetic excludes BLOCKED.** The Environment escape hatch says "Mark scenarios BLOCKED, not FAIL" (:23), but the contract has only `SCENARIOS_PASSED`/`SCENARIOS_FAILED` and the rule "SCENARIOS_TOTAL = PASSED + FAILED" (:184). A BLOCKED scenario has no bucket; the model must either miscount it as FAILED (violating the escape hatch) or break the arithmetic rule. Add `SCENARIOS_BLOCKED` and make TOTAL = PASSED + FAILED + BLOCKED. Same for the Test Honesty Gates' "UNVERIFIED, not PASS" (:69) — UNVERIFIED is a status with no home in the table (Result column shows only PASS) or the arithmetic.

**(d) Forward reference: `REVERT_RECOMMENDED: [true if Option B]`** (:118) — "Option B" is defined 40 lines later in the Rollback Decision prose. A model filling the YAML top-down meets an undefined term. Inline it: "[true if decision = revert]".

**(a) Per-finding validation paragraph** (:41) is one 250-word sentence-cluster doing five jobs (restate, verify, classify, drop, fail-safe). The content is excellent; the packaging fights it. Numbered list, one clause each.

**(c) Missing WHY:** run-cap ">15 → stop, report scope" (why 15? what failure is this preventing — cost? thrash?); "re-run once" for flaky tests (why once and not twice — the WHY "never convert flaky pass into unconditional confidence" is there, good, but the count is bare).

**(g) Good — arguably the best file:** claim-extraction protocol (UNVERIFIED→VERIFIED/CONTRADICTED/UNVERIFIABLE) is a full epistemic procedure; validated:false/degraded distinction with fail-safe direction explicitly reasoned ("a transient access failure must never silently remove a critical finding"); Test Honesty Gates ship the exact grep for each red flag; forbidden-language list; "Never convert missing proof into PASS."

---

### 8. plan-gap-reviewer.md

**(e) Opening: the cleanest in the fleet.** Standalone by design (the HTML comment explaining the no-skills choice is a model-visible rationale — good). Core states goal AND non-goals ("You do not own orchestration, plan approval, or plan edits").

**(b) "Freshness rule: Stay context-clean and anti-anchored."** — two adjectives; but the three bullets beneath are the actual procedure, so the header sentence is a harmless label rather than a live rule. Borderline no-op; could delete the sentence and keep the bullets.

**(f) Heading case inconsistency.** Example shows `## Planning Review: Pass` (:100) — every other agent uses the bracketed-options convention (`## Triage: [TRIAGED/NEEDS_INFO/WONTFIX]`) and uppercase status words. Also the YAML key here is `PLANNING_REVIEW_STATUS` while every sibling uses `STATUS` — the file never says the router accepts the different key (the envelope comment addresses `cr` reuse but not this). One sentence would settle it.

**(g) Good:** finding buckets each with a calibration example ("`execution_order_issues`: Phase 2 imports a module that Phase 3 creates") — exactly the rubric's worked-example standard; verification depth checklist is six checkable predicates; "What To Ignore" list kills the classic reviewer scope-creep ("extra abstractions you personally prefer"); "You are looking for gaps that would force the user to say: 'compare the plan to the code again'" — a completion criterion phrased as the user-pain it prevents.

---

### 9. planner.md

**(e) Opening: good**, and the blockquote warning "**NEVER call `EnterPlanMode`.** … Entering plan mode blocks Write/Edit and prevents the plan from saving" is a model-visible WHY on a prohibition — textbook.

**(d) Two review-iteration numbers.** Process step 15: plan-review-gate "max 3 iterations". Contract: `PLANNING_REVIEW_RUNS: [0-2]`. These are (probably) different counters — gate iterations vs fresh-review passes — but nothing says so, and the near-identical names invite conflation. Rename one (`GATE_ITERATIONS` vs `FRESH_REVIEW_RUNS`) or add a disambiguating clause.

**(d) `CONFIDENCE: [0-100]` with a threshold (`CONFIDENCE≥50` required for PLAN_CREATED) but no scoring procedure** — same disease as bug-investigator. The model will emit 75 by vibe. Tie it to checkables: "start at 90; −15 per `inferred` critical assumption; −25 if any RECOMMENDED_DEFAULTS entry exists; floor at the Research Quality level when research files present."

**(a) Step 10's phase-field list** enumerates 13 fields inline; the `cc10x:planning` skill (loaded in frontmatter) presumably owns this schema. If both define it, drift; if only this file does, fine — but "drawn from the `### Test Seams` subsection of the planning skill" mid-list confirms split ownership of one schema across two documents.

**(g) Good:** ambiguity-handling table (five situations → five actions — a real decision procedure replacing "use judgment"); auto-trigger list for decision_rfc; Interfaces block with "verbatim, the spelling later builders must match" and its enforcement twin in step 11b ("Every `Consumes` … must verbatim-match a `Produces`"); the open-decision anti-burial rule (:130) anticipates the exact gaming move ("never bury one in RECOMMENDED_DEFAULTS … to qualify for PLAN_CREATED — hiding an open decision is a contract violation, not a shortcut").

---

### 10. researcher.md

**(e) Opening: adequate.** Core + Invoked-by + Mode orient fast. Minor: "Bright Data accelerates web research; Octocode accelerates GitHub/package research" is capability inventory, not instruction — borderline no-op since the ladders below restate it operationally.

**(a) Inherited memory ritual is dead weight** (see cross-cutting): agent-common forces three `.cc10x` reads that nothing in this agent consumes.

**(b) "the most promising pages"** (:32), "one additional promising page" (:39) — no selection criterion. Cheap fix: "prefer official docs and pages whose title matches the topic's error string/version."

**(g) Good — the best stopping conditions in the fleet:** "3+ independent sources agree → stop and synthesize. Two full rounds yield no new actionable info → stop and save. Do not exceed 6 total search/fetch calls per round" — three independent, checkable brakes. Source-quality tiers with tie-handling ("Contradictory sources → note the conflict; do not silently pick one"). The Save Findings block exemplifies the entire output file inline — a fresh LLM could produce it exactly. `SOURCES_ATTEMPTED` vs `SOURCES_USED` distinction spelled out at the end.

**(f)** Clean. One nit: `## What Changed the Recommendation` presumes a recommendation existed to change — on a first-round research task there is none; the model must improvise the section's meaning. Add: "(first round: the highest-signal finding that should shape the plan)".

---

### 11. triage-agent.md

**(e) Opening: good.** Core + two crisp non-goals ("Never write code. Never auto-route into BUILD/DEBUG").

**(a/d) CONTRADICTION — does wontfix stop or proceed?** The Autonomous transform table row 2: "**STOP for human** on wontfix — a wrong wontfix closes a real bug." Rows 3-4, same table: "Redundancy check … Proceed — if found, wontfix with a pointer to the existing code" and "Prior rejection check … Proceed — if found, wontfix with a link." Step 4 then reasserts "wontfix stops for human." So a redundancy-found wontfix is simultaneously "proceed" and "stop." This is the fleet's clearest table-level self-contradiction; a model will pick whichever row it read last. Fix by splitting the verb: "recommend wontfix and STOP for human sign-off (rows 3-4 included: the evidence gathering proceeds; the wontfix action itself always stops)" — or genuinely exempt evidence-backed wontfixes and say so in row 2.

**(d) "`b=true` only if wontfix is contested"** (:126) — contested by whom, detected how? No signal in the process produces "contested." Dead branch or missing procedure; either delete or define ("reporter pushed back on a prior wontfix comment in-thread").

**(b) "Write scope (LAW)"** — "LAW" is emphasis-inflation (the rubric's weak-leading-word problem inverted: shouting instead of sharpening). The rule itself is precise; drop the label.

**(g) Good:** AI-disclaimer rule with the exact string to prepend; redundancy vs prior-rejection distinction with the KB-hygiene WHY ("do NOT write to `.out-of-scope/` — that KB is for rejected requests, not built ones"); agent brief template fully exemplified; "Search … by domain concept (not just the request's wording)".

---

## (g) What this fleet does BETTER than typical — honest summary

1. **Machine-contract discipline with fallback.** Envelope-line-1 + heading-line-2 + YAML, uniformly, with "router reads envelope first; falls back to heading scan if malformed" — degradation path stated. Most agent fleets never tell the model *why* the format matters; this one does ("this is why output reaches the router").
2. **The SINGLE FINAL RESPONSE RULE names a real harness constraint** ("The router receives ONLY your LAST response turn") instead of just demanding a format — rationale-carrying at its best.
3. **Evidence gates with self-executing consequences.** Quote-the-line + auto-demotion, zero-finding gate, doubt-theater check, claim-extraction with validated:true/false/degraded — these operationalize "don't hallucinate findings" better than anything in the mattpocock corpus.
4. **Fail-closed vocabulary everywhere.** BLOCKED/NEEDS_CLARIFICATION/no-loop-no-hypothesis/"Never convert missing proof into PASS" — the fleet consistently prefers refusing over improvising.
5. **Anti-anchoring as designed information flow** (reviewer skips activeContext, plan-gap-reviewer loads nothing) with the rationale written where the model can read it.
6. **Forbidden-language lists** ("LGTM", "should pass", "looks good") — banning the exact softener tokens is a technique the rubric's own corpus doesn't use.
7. **Anticipated gaming moves.** planner's "never bury an open decision in RECOMMENDED_DEFAULTS", agent-common's Spirit-vs-Letter, verifier's test-tampering grep — the prompts model the model's failure modes, not just the task.

Weaknesses relative to the rubric are equally consistent: duplication-with-drift between agent-common and bodies, unverifiable self-scored confidence numbers, prose-in-brackets where a literal example belongs, and a handful of genuine contradictions (TaskUpdate, wontfix, BLOCKED/INVESTIGATING).

---

## (h) Top 15 Rewrites — before → after, ranked by expected behavioral impact

**1. agent-common:60 — resolve the TaskUpdate contradiction.**
Before: "Stop your turn — the router handles task completion automatically."
After: "Stop your turn. If your agent doc says to call TaskUpdate, call it in your last tool turn, BEFORE the final response; otherwise the router completes the task for you."
(Impact: prevents five agents from skipping/duplicating a completion signal the router depends on.)

**2. triage-agent:36-41 — fix the wontfix stop/proceed contradiction.**
Before: "STOP for human on wontfix" (row 2) vs "Proceed — if found, wontfix with a pointer" (rows 3-4).
After: "Any wontfix outcome — including redundancy- and prior-rejection-backed ones — is a RECOMMENDATION: gather evidence, draft the comment, then STOP for human sign-off. Only category and needs-info proceed autonomously."

**3. code-reviewer — split the two CONFIDENCEs and reconcile the zero-finding number.**
Before: one `CONFIDENCE` meaning per-finding score, formula output, and gate target; formula yields 90 for clean code while the gate calls ≥90 invalid.
After: `FINDING_CONFIDENCE` (per finding, ≥80 to report) and `REVIEW_CONFIDENCE` (= min(HARD) capped at avg(SOFT)−10; note: max is 90 by construction). Zero-finding rule: "if zero findings after the positive-assertion pass, REVIEW_CONFIDENCE = 70 exactly."

**4. code-reviewer:257 — show SPEC_COMPLIANCE as real YAML.**
Before: `SPEC_COMPLIANCE: [PASS | list of {bucket, item} … e.g. [{MISSING, "rate-limit guard on /login"}]]`
After:
```yaml
SPEC_COMPLIANCE: PASS
# or:
SPEC_COMPLIANCE:
  - bucket: MISSING
    item: "rate-limit guard on /login"
```
(Apply the same literal-alternatives treatment to PLAN_DEFECT and CANNOT_VERIFY_CROSS_PHASE.)

**5. integration-verifier — give BLOCKED/UNVERIFIED scenarios a home.**
Before: "Mark scenarios BLOCKED, not FAIL" + "SCENARIOS_TOTAL = PASSED + FAILED".
After: add `SCENARIOS_BLOCKED: [count]`; "SCENARIOS_TOTAL = PASSED + FAILED + BLOCKED. A Test-Honesty hit marks its scenario BLOCKED (result column: BLOCKED) until re-proven through the real interface."

**6. bug-investigator:91-95 — retitle the checkpoint block.**
Before: "Decision Checkpoints — return `STATUS: BLOCKED` when:" (third bullet returns INVESTIGATING).
After: "Decision Checkpoints — stop and return the named STATUS: >3 files → BLOCKED; public-API change → BLOCKED; H1/H2 confidence gap <20 → INVESTIGATING."

**7. failure-hunter:62 — give `|| defaultValue` a discrimination procedure.**
Before: "`\|\| defaultValue` | Masks errors | Check explicitly first"
After: "`\|\| default` on a fallible call's return (`parse(x) \|\| fallback` — hides the failure) → flag. `\|\| default` on optional config/input → ignore. Test: could the left side be falsy because an operation FAILED? Flag only then."

**8. component-builder Seam Gate — say where the proposal lives.**
Before: "`proposed` (you propose at BUILD_PREFLIGHT)" with a token format that has no seam field.
After: "`proposed` — record the seams in TEST_SEAMS in your final contract; decide them before emitting BUILD_PREFLIGHT. The token itself stays exactly four fields — never extend it."

**9. bug-investigator / component-builder — define exit-code fields as observations.**
Before: `TDD_RED_EXIT: [1 if regression test failed before fix, null if missing]` + rule "requires TDD_RED_EXIT=1".
After: "`TDD_RED_EXIT`: the actual exit code observed on the RED run (any non-zero behavioral failure qualifies); null if RED never ran." Rule: "requires TDD_RED_EXIT non-zero with TDD_RED_REASON_KIND=behavioral."

**10. bug-investigator:79 — bind hypothesis confidence to checkables.**
Before: "H1/H2/H3 with 0-100 confidence. Proceed to fix only when one reaches 80+."
After: "A hypothesis reaches 80+ only when BOTH hold: (1) causal chain complete, no 'somehow' links; (2) at least one prediction confirmed by instrumentation. Otherwise cap it at 60."

**11. doc-syncer — reconcile the three-vs-four layer story and unbraid step 2.**
Before: prose says "all three layers"; template lists business/technical/audit/glossary; audit step 2 is one 90-word obligation cluster.
After: name the four layers once in Impact Classification (or drop glossary from the template); rewrite audit step 2 as: "1. Edit the existing doc. 2. Append its path to AUDIT_DOCS_UPDATED **and** DOC_FILES_UPDATED (the router's COMPLETE check reads DOC_FILES_UPDATED). 3. Legacy `docs/decisions/` file? Migrate: write `docs/adr/NNNN-{topic}.md`, delete old, record the new path in both lists."

**12. code-reviewer — deduplicate READ-ONLY, spec-independence, and PLAN_DEFECT statements.**
Before: READ-ONLY stated at :24 and :40; spec-compliance independence at :135, :140, :303; PLAN_DEFECT routing at :132-134 and :299.
After: one authoritative statement each (keep the Output-section versions, since they sit next to the fields), one-line pointers elsewhere. Cuts ~40 lines and removes drift surface.

**13. architecture-scanner:63 — give the strength badge criteria.**
Before: "**Recommendation strength** — `Strong` | `Worth exploring` | `Speculative` (as a badge)"
After: "`Strong` = deletion test says 'concentrates' AND the files appear in git-log hot spots. `Speculative` = single-read impression, no churn or test-pain evidence. Everything else = `Worth exploring`."

**14. planner — disambiguate the two review counters and score CONFIDENCE.**
Before: "max 3 iterations" (gate) vs `PLANNING_REVIEW_RUNS: [0-2]`; bare `CONFIDENCE: [0-100]` with a ≥50 gate.
After: rename to `GATE_ITERATIONS: [0-3]` and `FRESH_REVIEW_RUNS: [0-2]` (or one clause: "these are different counters"); "CONFIDENCE: start 90; −15 per inferred critical assumption; −25 if RECOMMENDED_DEFAULTS non-empty; when research files present, cap at the Research Quality tier."

**15. failure-hunter / code-reviewer — define envelope `b` per status.**
Before: code-reviewer never maps b; failure-hunter binds it only parenthetically ("(critical failures found)").
After (each Output section): "`b:true` iff CRITICAL_ISSUES ≥ 1 (code-reviewer: iff STATUS=CHANGES_REQUESTED with ≥1 CRITICAL); otherwise false. HIGH-only findings: s=ISSUES_FOUND, b=false."

---

## Per-Category Tallies

| Category | Count | Notes |
|---|---|---|
| (a) dead-weight / redundant / contradictory | 14 | 4 true contradictions (TaskUpdate, wontfix, BLOCKED/INVESTIGATING header, three-vs-four layers); rest duplication-with-drift |
| (b) vague adjectives without procedure | 9 | worst: `\|\| defaultValue` mask rule, strength badges, "explore organically", "promising pages", "when low-cost" |
| (c) rules missing WHY | 8 | CI=true/run-mode, shell-redirection ban, −10 SOFT cap, 200-char gate, stderr-not-logger, run cap 15, CDN choice, complexity>10 |
| (d) pressure-ambiguities | 12 | confidence system (3 sub-issues), envelope `b` (×2), exit-code-as-boolean, BLOCKED-scenario arithmetic, seam-proposal location, review counters, glossary layer, Option B forward-ref, Regression:/Variant: prefixes |
| (e) persona/opening quality | 11 assessed | 8 strong (bug-investigator, plan-gap-reviewer, failure-hunter best), 3 adequate (doc-syncer, researcher, architecture-scanner); zero wasted-opening failures |
| (f) output-format-as-prose gaps | 6 | invalid-YAML SPEC_COMPLIANCE family (3 fields), unexemplified scenario name prefixes, heading-case/STATUS-key deviation in plan-gap-reviewer, "What Changed the Recommendation" on round 1 |
| (g) better-than-state-of-the-art strengths | 7 | envelope+fallback, harness-rationale, evidence gates, fail-closed vocabulary, anti-anchoring flow, forbidden-token lists, anticipated gaming |
