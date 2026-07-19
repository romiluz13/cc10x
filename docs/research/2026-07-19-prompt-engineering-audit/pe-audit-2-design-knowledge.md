# Prompt-Engineering Audit — CC10x Design/Knowledge Skills vs mattpocock-skills Benchmark

Scope: prompt-engineering / LLM-instruction quality ONLY. Orchestration (routing, hooks, state plumbing) ignored except where it corrupts the prose an executing agent must read. Files audited from `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/`; benchmark from `/Users/rom.iluz/Dev/mattpocock-skills/`.

---

## STEP 1 — Rubric extracted from the benchmark

The benchmark's `writing-great-skills/SKILL.md` is itself a meta-standard; the other files are its exemplars. Ten concrete techniques, each with a quoted exemplar:

1. **Predictability as root virtue.** "A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same _process_ every run, not producing the same output — is the root virtue; every lever below serves it." Every sentence must buy process-determinism.

2. **The no-op test.** "does it change behaviour versus the default? A weak leading word (_be thorough_ when the agent is already thorough-ish) is a no-op; the fix is a stronger word (_relentless_), not a different technique." And: "hunt no-ops sentence by sentence… when one fails, delete the whole sentence rather than trim words from it."

3. **Big ideas compressed into operational tests.** Ousterhout's entire deep-modules thesis becomes two falsifiable checks in `codebase-design`: "**The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep." and "**One adapter means a hypothetical seam. Two adapters means a real one.**" The agent never has to *judge* depth; it *runs a test*.

4. **Rationale rides the rule.** Every prohibition carries its why in the same sentence. Grilling: "Asking multiple questions at once is bewildering." ADR-FORMAT: "If a decision is easy to reverse, skip it — you'll just reverse it." Rejected framings: "Depth as ratio of implementation-lines to interface-lines (Ousterhout): rewards padding the implementation." Improve-codebase-architecture: "Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed."

5. **Sentence economy / all-reference skills.** `research/SKILL.md` is three numbered sentences, yet contains a complete epistemic policy: "Follow every claim back to the source that owns it." `grill-with-docs` is one line: "Run a `/grilling` session, using the `/domain-modeling` skill."

6. **Decision procedures over adjectives.** Wayfinder's "Fog or ticket? The test is whether you can state the question precisely now — _not_ whether you can answer it now." Domain-modeling's ADR gate: three named conditions, "If any of the three is missing, skip the ADR." Grilling: "If a *fact* can be found by exploring the environment… look it up rather than asking me. The *decisions*, though, are mine."

7. **Stopping conditions.** Wayfinder: "**never resolve more than one ticket per session**"; "Stop — charting is one session's work; it hand-resolves nothing." Improve-codebase-architecture: "Do NOT propose interfaces yet. After the file is written, ask the user."

8. **Examples and counter-examples as the definition.** Domain-modeling defines its behaviors by quoted dialogue: "'Your glossary defines cancellation as X, but you seem to mean Y — which is it?'" Codebase-design's testability rules are paired good/bad code snippets, not prose.

9. **Leading words.** Compact pretrained concepts anchor whole behavior regions: *fog of war*, *frontier*, *destination*, *seam*, *deletion test*. "Repeated throughout the text… it accumulates a distributed definition and anchors a whole region of behaviour in the fewest tokens."

10. **Anti-duplication / single source of truth.** "Keep each meaning in a **single source of truth**… Costs maintenance and tokens, and inflates a meaning's prominence on the ladder past its real rank." And negation-avoidance: "Prompt the **positive**… keep a prohibition only as a hard guardrail you can't phrase positively, and even then pair it with what to do instead."

---

## STEP 2 — Per-file audits

# 1. codebase-design/SKILL.md (+ DEEPENING.md, DESIGN-IT-TWICE.md)

References dir: `DEEPENING.md`, `DESIGN-IT-TWICE.md` (no `references/` subdir; companions sit beside SKILL.md).

The body is a near-verbatim port of the benchmark — which is largely why it's the strongest file in the set. The additions are where the problems live.

### (a) Dead-weight / redundant / self-contradictory

1. "This skill is the **canonical source** for the deep-module vocabulary. Other cc10x skills (`architecture`, `codebase-hygiene`, `building`, `planning`) reference these terms instead of restating them, so there is one source of truth." — Restates the frontmatter description almost word-for-word ("The single source of truth for these terms; other skills… point here instead of restating them"). The executing agent's behavior does not change by being told it is reading the canonical copy. Pure duplication of an author-facing fact — the exact failure the sentence is about.
2. "This verdict is **canonical**: `codebase-hygiene` and `architecture` agree with it." — No-op for the reading agent. Knowing two sibling files agree changes nothing about how it applies the test. (And factually shaky: hygiene restates the test with drifted phrasing — see file 4.)
3. The Deletion Test appears **twice**: as its own promoted `## The Deletion Test` section, and again in Principles as "**The deletion test** (above) — falsifiable, canonical." The benchmark had it once, as one principle bullet. Per the benchmark's own rule, duplication "inflates a meaning's prominence on the ladder past its real rank" — and the stub bullet "(above) — falsifiable, canonical" is content-free.
4. The 3-line upstream-provenance HTML comment ("Upstream: github.com/mattpocock/skills @ e9fcdf…") is loaded into context every invocation and steers nothing. Maintenance metadata belongs in git history or a manifest, not the prompt.

### (b) Vague adjectives posing as instructions

The ported body is clean — the glossary is definitionally precise. One inherited softness: "placed at a clean seam" (also in benchmark). "Clean" is never operationalized. Rewrite: "placed at a seam a test can reach" — which is exactly the operational test `codebase-hygiene` later invented ("If only production code crosses the seam and no test can reach it → the seam is a guess"). The suite has the decision procedure; this file just doesn't use it.

### (c) Rules missing their WHY

1. "Don't introduce a port unless something actually varies across it." — Why is carried in DEEPENING.md ("A single-adapter seam is just indirection") but not at the point of statement in SKILL.md. One clause fixes it.
2. Ported as-is from benchmark: "Can I reduce the number of methods? / Can I simplify the parameters? / Can I hide more complexity inside?" carry their why from the surrounding depth definition — fine.

### (d) Hedged / passive imperatives

1. "the module is probably the wrong shape" (inherited from benchmark) — the hedge "probably" weakens the one line meant to redirect the agent away from white-box testing. Rewrite: "the module is the wrong shape — redesign the interface before writing the test."
2. DESIGN-IT-TWICE step 2: "the agent emits a **Design-It-Twice request** in its Memory Notes / handoff for the router to dispatch, OR (if the surrounding workflow supports it) the router spawns the parallel design sub-agents directly." — An either/or addressed to two different readers (the executing agent and the router) in one sentence. The executing agent can only do the first branch; the second is noise to it.

### (e) Head-to-head vs benchmark

- **Two-adapter rule.** Benchmark: "One adapter means a hypothetical seam. Two adapters means a real one. Don't introduce a seam unless something actually varies across it." CC10x: same, plus: "This rule is about **ports** — external dependency seams where you inject an adapter… It does NOT apply to every internal seam or test boundary… an ordinary caller or test exercising a public interface is NOT an adapter." **Verdict: CC10x wins.** The benchmark's rule, read literally, forbids every internal seam that has one implementation — a real over-application trap. CC10x closes it with a genuine distinction (ports vs seams), not filler. Minor loss: three negations in a row where one positive statement ("Apply this rule only to ports — injected external-dependency seams") would carry it.
- **Deletion test.** Benchmark: two sentences inside Principles. CC10x: a full section with the inlining framing ("If I deleted this module and inlined its code at every call site, where does the complexity go?") — a sharper mental operation than "imagine deleting" — plus "This is a falsifiable test, not a matter of taste — apply it before accepting any new module boundary," which converts it from observation to gate. **Genuine improvements**, wrapped in two sentences of canonicity chest-thumping and a duplicate stub bullet that dilute them.
- Everything else (glossary, diagrams, testability snippets, Relationships, Rejected framings) is verbatim — full fidelity, nothing dropped.

### (f) What CC10x does better

- The ports-vs-seams clarification of the two-adapter rule is the single best prompt-engineering *addition* in the whole audited set — it fixes a live over-application bug in the benchmark's most-quoted rule.
- "apply it before accepting any new module boundary" gives the deletion test a *when*, which the benchmark leaves implicit.
- `allowed-tools: Read Grep Glob LSP` scopes the skill read-only at the schema level — steering by capability rather than prose.

### (g) Rewrites (file-local)

1. Delete: "This skill is the **canonical source**… one source of truth." (already in frontmatter).
2. Delete: "This verdict is **canonical**: `codebase-hygiene` and `architecture` agree with it."
3. Collapse Principles bullet "**The deletion test** (above) — falsifiable, canonical." into the section header reference — or demote the section back into the bullet, benchmark-style.
4. "It does NOT apply to every internal seam or test boundary" → "Apply it only to ports; an internal seam needs test-reachability, not a second adapter."

---

# 2. domain-modeling/SKILL.md (+ ADR-FORMAT.md, CONTEXT-FORMAT.md)

Companions ported verbatim (confirmed by diff-reading) — and they are excellent; no findings in either beyond what the benchmark itself carries.

### (a) Dead-weight / redundant / self-contradictory

1. The READ-ONLY contract is stated **twice in full**: once in "Active vs read-only" ("you read `CONTEXT.md`… emit a proposal… or block… do NOT resolve the contradiction yourself") and again as the closing section "During the session (READ-ONLY mode)" (4 numbered steps saying the same thing, including the same `STATUS: FAIL` / `REMEDIATION_REASON` strings). Same meaning, two places, both normative — a maintenance fork waiting to diverge. Keep the numbered section; reduce the intro to one line pointing at it.
2. The blast-radius transform is stated three times: in the table, then re-appended to "Challenge against the glossary" ("In autonomous mode, if the contradiction affects contracts/persistence/user-language, STOP per the transform table; otherwise surface it and proceed") and to "Sharpen fuzzy language" ("Domain-shaping sharpening stops for human input; low-blast-radius sharpening proceeds with a recorded assumption"). Point-of-use reminders can be legitimate, but these *restate the rule* rather than point ("STOP per the transform table" alone would do); the second restatement adds a new term ("domain-shaping") not used by the table, inviting drift.
3. Frontmatter description: "The active discipline loaded by language-shaping agents (planner, doc-syncer, exploration). Builders load a read-only/obey variant… See the Active vs read-only section for which mode applies." — Per the benchmark's description rule ("Cut identity that's already in the body. Keep the description to triggers"), the agent-roster and the see-section pointer are body content sitting in an always-loaded slot. Roughly half this description does no invocation work.

### (b) Vague adjectives posing as instructions

1. "Offer ADRs sparingly" — inherited, but the benchmark immediately cashes "sparingly" into the three-condition gate, so it's fine. Preserved intact. ✓
2. "low blast radius (no contracts, persistence, or user-language affected)" — actually *good*: the vague term is defined parenthetically at first use. Model treatment of a vague term.
3. "If unsure, default to READ-ONLY" — "unsure" is the trigger and it's inherently fuzzy, but the tie-break carries its why (see (c)), which is the right compensation.

### (c) Rules missing their WHY — mostly absent; this file is the best WHY-carrier in the set

- "If unsure, default to READ-ONLY — the cost of an opportunistic glossary rewrite during a build is higher than the cost of a deferred proposal." ✓ asymmetric-cost rationale, exactly the benchmark pattern.
- "**Grilling is NOT auto-answered.** Auto-answering an interview removes its information source." ✓ one of the best rule+why sentences in either repo.
- One miss: "Append-only glossary entries avoid parallel-write clashes when multiple shaping phases run." — has a why, but the *rule* ("write append-only") is smuggled inside a rationale clause bolted onto "Update CONTEXT.md inline"; an agent skimming for imperatives will miss it. Promote to an imperative: "Append entries; never rewrite existing ones — parallel shaping phases clash on rewrites."

### (d) Hedged / passive imperatives

1. "The agent's persona prompt determines which mode is in effect." — passive-ish and unactionable as written; the agent cannot inspect "its persona prompt" as an object. The very next sentence (default READ-ONLY) is the real instruction; lead with it.
2. Transform table row 2: "Proceed with the recommended interpretation, record it in `CONTEXT.md` with an explicit `**Assumed:**` note, and continue." — "Proceed… and continue" is doubled motion; harmless but flabby.

### (e) Head-to-head vs benchmark

- Core sections (file structure, five "During the session" behaviors, ADR gate) preserved verbatim including the quoted-dialogue exemplars ("Your glossary defines 'cancellation' as X…"). **No fidelity loss in the ported core.**
- Benchmark: "call it out immediately" → CC10x keeps it, then adds the STOP/proceed fork. The fork is a real improvement for an autonomous context — it converts "challenge the user" (impossible with no user present) into a decision procedure keyed on blast radius. This is the **best human-gate→autonomous transform in the audited set**.
- One subtle drift: benchmark's "force the user to be precise" became "force precision about the boundaries between concepts" — depersonalized correctly for autonomy; no loss.

### (f) What CC10x does better

- The transform table is a genuine PE artifact the benchmark lacks: four situations × four dispositions, each row a checkable condition. It turns "sharpen fuzzy language" from a social skill into an executable one.
- "Auto-answering an interview removes its information source" is a sharper why than anything the benchmark offers for its own HITL stance.

### (g) Rewrites (file-local)

1. Description → "Actively build and sharpen a project's domain model — challenge terms, stress-test with edge cases, update CONTEXT.md inline, offer ADRs sparingly. Use when changing the domain model, not just consuming it." (Cut the agent roster and mode pointer.)
2. Collapse the duplicated READ-ONLY contract into the numbered section; the intro bullet becomes "READ-ONLY / OBEY (builders): see 'During the session (READ-ONLY mode)'."
3. In "Challenge against the glossary," replace the restated fork with "…call it out immediately, then dispose of it per the transform table."

---

# 3. architecture/SKILL.md (no references dir — single file)

Original CC10x material; no direct benchmark counterpart (closest: improve-codebase-architecture, which is retrofit-side and maps to hygiene). Structurally strong — templates and tables everywhere — but it contains the worst single fidelity bug in the set.

### (a) Dead-weight / redundant / self-contradictory

1. **The two-adapter rule is misstated — twice — in direct contradiction of the canonical source it cites.** "A component that fails the deletion test (complexity vanishes if deleted) or fails the two-adapter rule (**only one caller/adapter exists**)…" — `codebase-design` (the file this section says to defer to) states explicitly: "an ordinary caller or test exercising a public interface is NOT an adapter." "Caller/adapter" collapses exactly the distinction the canonical file was amended to draw. An agent reading this will refuse to create any module with a single caller — which is nearly every module in a greenfield design. This is the drift the "single source of truth" architecture was supposed to prevent, occurring *inside the sentence that pledges allegiance to it*. Appears verbatim in Phase 3 and again under Architecture Vocabulary.
2. The entire `## Note` section: "Deep-module vocabulary… are defined once in `cc10x:codebase-design` and pointed to above… The one-line application rule… is deliberately repeated at its two points of use — Design Components and Architecture Vocabulary; the definitions themselves are not restated." — This is a maintainer's changelog comment addressed to future editors, spending ~60 tokens of every invocation to defend a duplication that itself costs ~50. Zero effect on the executing agent. Delete outright (or demote to an HTML comment if the editorial defense must survive).
3. Architecture Vocabulary paragraph: "**Use those terms exactly** — don't restate them here." — "don't restate them here" is author-facing (the agent isn't editing the file). Also duplicates codebase-design's own "Use these terms exactly."
4. "Depth is leverage at the interface (a lot of behaviour behind a small interface), NOT a lines-ratio — `codebase-design` explicitly rejects the Ousterhout implementation-lines/interface-lines framing." — restates a definition and a rejected framing the same paragraph says it won't restate. Self-contradiction inside one paragraph.
5. The deletion-test/two-adapter application sentence is repeated verbatim in Phase 3 and Architecture Vocabulary (self-acknowledged in the Note). One of these should be a pointer.

### (b) Vague adjectives posing as instructions

1. "When a module's interface is **non-trivial**, design it twice" — no test for non-trivial. Rewrite with a decision procedure: "Design it twice when the interface has ≥2 plausible shapes you can name, or when it will have ≥3 callers. If you can't sketch a second genuinely different design in five minutes, it was trivial — move on."
2. "**Second design:** a different approach (not a refinement of the first)." — "different" is doing all the work and is unenforceable as stated. Borrow exploration's operational phrasing for UI variants: "different in structure — a different interface shape or seam placement, not renamed methods on the first."
3. Observability: "**Metrics:** what to track (business-relevant, not infra noise)" — "business-relevant" and "noise" are judgment words. Rewrite: "Metrics: track what a flow's Success step needs to prove it ran — one metric per mapped flow outcome; skip anything no mapped flow reads."
4. "Map every user flow end-to-end" is checkable only because "every" quantifies it — fine. But Phase 3 has no completion criterion at all (benchmark rubric: "Each step ends on a completion criterion… a vague criterion invites premature completion"). Add: "Done when every flow step from Phase 1 names its component and every error path names its handler."

### (c) Rules missing their WHY

1. "Every flow must have its error paths mapped. Unmapped error paths become unmapped components." ✓ — carries its why, aphorism-grade. Best line in the file.
2. "Wrapped dependencies can be swapped. Consumed dependencies cannot. Track which is which — it determines your coupling risk." ✓ good.
3. "**Temporal coupling** — caller must know the order of operations. Design defect — remove or document explicitly." — Missing why, and hedged (see (d)). Supply: "…a caller that calls in the wrong order fails at runtime with no type error to warn it."
4. "Design APIs from the flow, not from the data model" — the why arrives only implicitly via the good/bad example. One sentence would lock it: "Data-model-aligned APIs force every caller to re-derive the business rule (which fields make an order 'cancelled'); flow-aligned APIs keep it behind the seam."
5. C4 views section: three view types with no why or when — an agent doesn't know if all three are mandatory per design or chosen by scale. Add a selector: "Small systems: Component view only. Add Container when there are ≥2 deploy units; add Context when there are external systems."

### (d) Hedged / passive imperatives

1. "remove **or document explicitly**" (temporal coupling) — the escape hatch swallows the rule; "document explicitly" is what an agent will always choose because it's cheaper. Rewrite: "remove it by folding the ordered steps behind one entry point; document it only when the order is imposed by an external protocol you don't control."
2. "Use the better one, **or a hybrid**." — fine content, but paired with no tie-break. Benchmark DESIGN-IT-TWICE ends "Be opinionated — the user wants a strong read, not a menu"; this file's inline version dropped that closer and with it the anti-hedging pressure.

### (e) Head-to-head vs benchmark

- **Design It Twice.** CC10x inline version: "The first design is usually shallow — it mirrors the implementation… **Why:** One-pass interfaces optimize for the implementer. Two-pass interfaces optimize for the caller." vs benchmark/cc10x companion DESIGN-IT-TWICE.md's parallel-brief pattern with per-agent constraints ("Minimize the interface — aim for 1–3 entry points max"). The inline version's implementer/caller why is *better than anything in the companion* — but the companion's concrete per-design constraints are better than the inline "a different approach." Neither references the other's strength; the suite holds two half-versions of one idea (duplication + fidelity split).
- **Vocabulary deferral vs improve-codebase-architecture.** Benchmark: "Run the `/codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**…). Use these terms exactly in every suggestion — don't drift into 'component,' 'service,' 'API,' or 'boundary.'" — a pointer plus the enforcement rule, no restatement. CC10x's equivalent paragraph restates the depth definition and the Ousterhout rejection while claiming not to. Benchmark executes the pattern more cleanly.
- Notably: this skill's own Phase 2/3 vocabulary is "**components**" throughout — the exact word the vocabulary it imports says to avoid ("_Avoid_: unit, component, service"). The file mandates a glossary with one hand and violates it ~20 times with the other. (Defensible for C4 alignment, but then the file should say so explicitly; silently carrying both vocabularies invites the drift codebase-design bans.)

### (f) What CC10x does better

- No benchmark counterpart covers greenfield at all — the flow-mapping template, integration table (Failure mode / Retry policy rows especially), and dependency classification are real, checkable structures the benchmark simply doesn't have.
- "Unmapped error paths become unmapped components" is benchmark-grade aphorism writing.
- The Decision Framework's "**Reversibility:** [reversible or irreversible — irreversible decisions need more evidence]" quietly encodes a proportionality principle the benchmark's ADR gate only implies.

### (g) Rewrites (file-local)

1. Both occurrences: "fails the two-adapter rule (only one caller/adapter exists)" → "fails the two-adapter rule (it's a port with only one adapter — callers don't count as adapters)".
2. Delete `## Note` entirely.
3. Architecture Vocabulary paragraph → "The deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality, deletion test, two-adapter rule) is defined in `cc10x:codebase-design`. Use those terms exactly." (Cut the restated depth definition and Ousterhout clause.)
4. "When a module's interface is non-trivial" → concrete trigger (see (b)1).
5. Reconcile the component/module vocabulary: either "This skill says 'component' for C4 alignment; component = module in codebase-design's sense" — one sentence — or rename.

---

# 4. codebase-hygiene/SKILL.md (no references dir — single file)

Maps to benchmark's improve-codebase-architecture (retrofit side). The strongest original writing in the set — and one genuine incoherence.

### (a) Dead-weight / redundant / self-contradictory

1. **The deletion-test question and its answers use different dichotomies.** Question: "If I deleted this module, would the complexity it holds **CONCENTRATE** somewhere, or just **MOVE** elsewhere?" Answers: "Complexity **vanishes** → shallow… Complexity **reappears across N call sites** → deep." Neither answer term matches either question term — an agent must guess whether "concentrate" maps to "vanish" or "reappear" (and the intuitive reading is arguably inverted: complexity *reappearing across N sites* sounds like "moving elsewhere," yet it's the *keep* verdict). The benchmark/codebase-design phrasing ("where does the complexity go? It vanishes / It reappears") is coherent; the hygiene rewrite drifted the question and kept the old answers. This is precisely the drift the "canonical, not restated" architecture claims to prevent — and here the test IS restated in full, contradicting architecture's "not restated here" policy for the same rule.
2. "This verdict agrees with `cc10x:codebase-design` (canonical) and `cc10x:architecture`." — same no-op agreement claim as in codebase-design; changes no behavior.
3. Header/description mismatch: description says "Advisory and **read-only**"; body opens "Advisory and **read-heavy**"; Diagnosis Flow header says "(READ-ONLY)". Two of these are the contract, one is a hedge — pick one.
4. Handoff section: "The deepening is verified: survivor interface has tests at its seam, every caller is repointed, suite + typecheck pass after merge." — describes work this skill explicitly does not do ("It does NOT edit code"), restating Consolidation Discipline's three conditions in future tense for a different agent. Cut to a pointer or drop.

### (b) Vague adjectives posing as instructions

1. "**Worth-exploring** (real cost/risk)" — "real" is the whole criterion. But note: the benchmark's identical badges (`Strong`, `Worth exploring`, `Speculative`) have *no* definitions at all, so even one-word glosses are an improvement. To finish the job: "Strong — deletion test verdict is unambiguous and ≥3 call sites are affected; Worth-exploring — verdict clear but blast radius or effort is; Speculative — verdict itself is a guess."
2. "Drop categories with <3 functions — can't hide a meaningful duplication pattern." — "meaningful" wobbles, but the numeric threshold above it does the work; acceptable.
3. "group by confidence, highest first" — confidence is never scaled in this file (no high/medium/low anchor as research/SKILL.md provides). Import that scale or point at it.

### (c) Rules missing their WHY — this file mostly carries them, e.g.:

- "**Never use cheap tier for detection** — it anchors on names and rubber-stamps 'these look different.'" ✓ rule + mechanism in one line; benchmark-grade.
- "Missing one is a silent break." ✓. "Green tests on the survivor license the deletion." ✓.
- Miss: "run duplicate detection mode first — consolidate before deepening" — why? Supply: "a near-duplicate pair fails the deletion test in both directions; consolidate first or you'll deepen two copies of one module."
- Miss: "Mechanical bucketing to shrink comparison space" explains step 2, but step 1's `name | file:line | signature` format is asserted with no why (it's so findings carry evidence downstream — one clause).

### (d) Hedged / passive imperatives

1. "Advisory and read-heavy. Diagnoses and proposes; does not refactor." — terse and strong, actually; the hedge is only the "read-heavy"/"read-only" wobble noted above.
2. "Badge each candidate" / "Then stop and ask which to pursue. Do not design interfaces for candidates the user hasn't chosen." — clean stopping condition, faithfully ported from benchmark's "Do NOT propose interfaces yet." ✓ no hedging.

### (e) Head-to-head vs benchmark (improve-codebase-architecture)

- **Scoping — LOST.** Benchmark: "**Scope before you scan — YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed… walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots." CC10x hygiene has **no scoping step at all** — "Extract catalog — Grep/Glob for exported functions" scans the entire exported surface unconditionally. The benchmark's rationale (deepening pays off proportionally to future change) is dropped along with the mechanism. On a large repo this is the difference between a targeted audit and an unbounded crawl. **Worst single fidelity loss in the set.**
- **Domain-language anchoring — LOST.** Benchmark: "Use CONTEXT.md vocabulary for the domain… If `CONTEXT.md` defines 'Order,' talk about 'the Order intake module' — not 'the FooBarHandler.'" and "ADRs in `docs/adr/` record decisions this command should not re-litigate… if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting… Don't list every theoretical refactor an ADR forbids." Hygiene never mentions CONTEXT.md or ADRs. In a suite whose domain-modeling skill is this elaborate, the retrofit scanner not reading the glossary or respecting settled ADRs is a hole, and the re-litigation guard is exactly the kind of rule that stops an autonomous scanner from re-proposing rejected refactors every run.
- **Exploration heuristics — traded, defensibly.** Benchmark: "Don't follow rigid heuristics — explore organically and note where you experience friction" + five friction questions ("Where does understanding one concept require bouncing between many small modules?"). CC10x: a rigid 5-step mechanical method with a tier split. For an autonomous, repeatable agent, the mechanical method is arguably *more* predictable (the benchmark's own root virtue) — a legitimate divergence, not drift. But the friction questions themselves were free discovery prompts and could have survived as a sidebar.
- **Two-adapters section — IMPROVED.** "If only production code crosses the seam and no test can reach it → the seam is a guess. Put the interface where a test can reach it, or don't introduce it." — a genuinely new, operational test for non-port seams that neither the benchmark nor codebase-design states. Best original PE sentence in the file.

### (f) What CC10x does better

- Duplicate-detection mode has no benchmark counterpart and is well-written: the High-Risk Zones table (each zone with its why: "Catch-all dumping grounds," "rewritten per feature"), the cheap/capable tier split with anchoring rationale, and the three-condition Consolidation Discipline are all checkable, why-bearing structures.
- "Proposing is read-only; changing is gated." — a whole permission model in seven words.
- The Smell → Usually table compresses four judgment calls into lookups.

### (g) Rewrites (file-local)

1. Deletion test question → "If I deleted this module and inlined its code at every call site, where does the complexity go?" (align with codebase-design; answers already match) — or better, replace the whole restated block with a two-line pointer + the smell table.
2. Insert scoping step 0: "Scope before you scan: `git log --oneline` for hot spots; weight recently-changed areas — deepening pays off in proportion to future change. If the user named a target, take it and skip inference."
3. Add: "Read `CONTEXT.md` and `docs/adr/` for the area first; name candidates in domain vocabulary; a candidate contradicting an ADR is surfaced only if the friction justifies reopening it."
4. "Advisory and read-heavy" → "Advisory and read-only."
5. Define the three badges with checkable criteria (see (b)1).

---

# 5. exploration/SKILL.md (no references dir — single file)

Absorbs benchmark's brainstorming-equivalent, grilling (partially), and prototype. The longest file; densest mix of excellent and diluted.

### (a) Dead-weight / redundant / self-contradictory

1. The "spike never becomes production" meaning appears **four times**: Hard Wall ("The spike's code does not become production by surviving"), the scar comment ("The prototype proving a question is NOT the same as the answer being shipped"), Step 4b ABSORB ("re-implement the core under TDD/reviewer/verifier"), and the closer ("The prototype skill NEVER transitions itself into BUILD"). The scar comment is sanctioned by house convention; the other three should collapse to Hard Wall + one pointer. Per the benchmark rubric, this quadruplication "inflates a meaning's prominence" — here it crowds out the branch-specific content that only appears once.
2. "DESIGN includes an optional inline sub-procedure, the Doubt Pass, for high-stakes decisions — it is not a third mode." — the clause "it is not a third mode" pre-rebuts a confusion no reader has yet had; naming the elephant (benchmark: negation "makes it more available, not less"). The section placement already shows it's a sub-procedure.
3. Doubt Pass step 3 (DOUBT) buries the procedure under a 60-token orchestration aside: "This is an inline self-check, not true fresh-context isolation — the agent loading this skill has NO `Agent`/subagent tool; sub-agent fan-out is router-owned (see `cc10x:codebase-design/DESIGN-IT-TWICE.md` for the same rule)…" — mid-step, mid-sentence-flow, addressed half to the agent, half to the skill author. The actual instruction ("work from the ARTIFACT + CONTRACT only") is excellent and drowning.
4. "What This Is NOT" — three negations. The first and third restate content already present positively ("in-flight, while changes are still cheap" appears in the intro; "one cycle is often enough" duplicates the STOP rule's spirit). The middle one ("the doubt pass reasons from the artifacts alone, never from the claim's framing") is the only load-bearing line — and it's a restatement of step 3. The whole section can go.

### (b) Vague adjectives posing as instructions

1. "YAGNI ruthlessly — defer what is not essential." — "essential" undefined at the point where the agent is *deciding scope*, its highest-leverage moment. Rewrite: "Defer anything not required by a Success criterion. If no Success criterion needs it, it's Out of Scope — write it there."
2. Doubt Pass trigger "Stakes are high (production, security-sensitive, irreversible operations)" — actually fine: the parenthetical operationalizes it. ✓ model treatment.
3. "Multiple choice preferred." — preferred by whom, over what, why? Rewrite: "Offer 2-4 concrete options per question — options surface constraints the user forgot to state; open questions get vague answers."
4. Intent Completeness Gate — "(1) small enough to fit in one paragraph, (2) contradiction-free, (3) sufficiently specific that a builder could act without clarifying questions" — all three checkable. ✓ benchmark-grade completion criterion.

### (c) Rules missing their WHY

1. "One question at a time." — **the why was dropped in porting.** Benchmark grilling: "Asking multiple questions at once is bewildering." Four words that make the rule self-enforcing; restore them.
2. The facts-vs-decisions rule is **gone entirely**: benchmark grilling's "If a *fact* can be found by exploring the environment… look it up rather than asking me. The *decisions*, though, are mine." Exploration's "Skip a question when the answer is already explicit" covers half (already-stated answers) but not the other half (answers *discoverable* in the repo). An interviewing agent without this rule asks the user for facts `grep` would return. Highest-value single restoration in the set.
3. "Variants must differ structurally (layout, hierarchy, primary affordance) — not just color or copy" — has an implicit why; make it explicit: "same-structure variants answer a styling question, not the design question."
4. "Switcher is dev-only: gate on `process.env.NODE_ENV !== 'production'`" — why is guessable but absent: "so a half-finished variant can never ship."
5. "Present 2-3 approaches with trade-offs before asking which to pursue." ✓ fine as-is.

### (d) Hedged / passive imperatives

1. "For non-trivial decisions where correctness matters more than speed" — double-vague trigger ("non-trivial," "matters more") immediately rescued by the concrete When-to-Use list below it. Delete the fuzzy lead-in; keep the list.
2. "Escalate only when findings are substantive AND actionable." — "substantive" is defined nowhere though the STOP rule references classifying findings as actionable; half-anchored.
3. "Still record rejected alternatives (ADR notes)." — "Still" hedges; and passive about where. "Record rejected alternatives as ADR notes in the design file."

### (e) Head-to-head vs benchmark

- **Grilling.** Benchmark: 5 sentences, three of them decision procedures with whys. CC10x's interview: gains structure (5 named dimensions, resolve-only-unresolved, fast-path gate, completeness gate) but **loses** both of grilling's whys (bewildering; facts-vs-decisions) and its closer "Do not act on it until I confirm we have reached a shared understanding" — partially replaced by the Self-Review Gate, which checks the *document*, not the *shared understanding*. Net: more deterministic process, thinner rationale.
- **Prototype discipline.** Benchmark repo's prototype concept (per AGENTS.md: "throwaway, answer the question, discard — prototype code NEVER becomes production by surviving") is faithfully carried — "If you can't name the question in one sentence, you need design mode or a plan, not a spike" is a **better** entry gate than anything benchmark states. The Branch A "Isolate the salvageable core behind a pure interface… This is the part that can be lifted later" quietly reuses codebase-design's seam thinking without naming it — a missed leading-word opportunity (say *seam*).
- **Fast path.** "take the fast path ONLY when all three are stated, not inferred. When in doubt, interview." — stated/inferred is a crisp, checkable distinction; no benchmark counterpart. ✓ CC10x original, benchmark-grade.

### (f) What CC10x does better

- The scar comment ("<!-- scar: 2026-06-17 — spike's 'move fast, no tests' code promoted to production by inertia…") is rationale-carrying at its best: a dated, specific failure attached to the rule it produced. The benchmark has no equivalent convention.
- The Doubt Pass's "Rationalization guard: 'This is too simple to doubt' → simple decisions have simple artifacts, so the doubt pass is fast. No excuse to skip." — pre-empts the exact rationalization an LLM produces, and answers it with a cost argument rather than a prohibition. Excellent.
- DELETE-or-ABSORB "no third option" forces a binary where the benchmark leaves disposal implicit.

### (g) Rewrites (file-local)

1. "One question at a time. Multiple choice preferred." → "One question at a time — asking several at once is bewildering. Offer 2-4 concrete options; open questions get vague answers."
2. Add to Interview: "Look up facts in the repo instead of asking; only decisions go to the user."
3. Doubt Pass step 3 → keep "adversarially re-read the extracted artifacts while deliberately setting the CLAIM aside: work from the ARTIFACT + CONTRACT only, and hunt for the weakest assumption"; move the no-Agent-tool aside to a one-line note outside the numbered steps.
4. Delete "What This Is NOT"; fold its middle clause into step 3 if not already covered.
5. Collapse the four never-ships restatements to Hard Wall + scar; Step 4b just points: "ABSORB triggers a fresh BUILD (see Hard Wall)."

---

# 6. research/SKILL.md (no references dir — single file)

Different job than benchmark's research (synthesis of delivered findings vs performing research), so head-to-head is limited — but the benchmark's epistemic core still applies and is partially absent.

### (a) Dead-weight / redundant / self-contradictory

1. `## Overview` first paragraph restates the frontmatter description nearly verbatim ("This skill is loaded via SKILL_HINTS by `cc10x:planner` and `cc10x:bug-investigator` when the router passes research files" ≈ description "Synthesis guidance loaded via SKILL_HINTS by planner and bug-investigator when research files are available"). Duplication with zero behavioral delta.
2. Two adjacent Include-bullets say the same thing: "Conflict resolution (when sources disagree, prefer GitHub real code over docs)" and "Source conflict resolution: high-confidence sources (cross-confirmed, code-backed) override low-confidence (single blog, no code)…" The second subsumes the first (code-backed > docs is an instance of high > low). Merge; keeping both invites an agent to treat them as two different rules.
3. "Confidence calibration from the router-provided `## Research Quality` block" — but the file *also* ships its own quality-weighting scale at the bottom ("high: multiple concrete sources or code-backed findings…"). Which is authoritative when they disagree? Two confidence sources, no precedence rule — a latent self-contradiction.

### (b) Vague adjectives posing as instructions

1. Exclude: "**Obvious things the AI already knows**" — unoperationalized; every model considers different things obvious, which is the opposite of the benchmark's predictability virtue. Rewrite: "Exclude any finding you could have written before reading the research files — if deleting the citation leaves the sentence just as defensible, cut the sentence."
2. "Reflects evidence quality **honestly**" — adverb posing as method. The quality scale at the bottom *is* the method; wire them: "Rate evidence per the quality scale below; the synthesis states the rating, not adjectives."
3. "Specific code snippets only when they **materially change** the recommendation" — borderline; "materially" is soft but the structure (only-when gate) is right. Sharpen: "…only when the recommendation cites the snippet's exact behavior."
4. "Gotchas the user probably hasn't considered" — "probably hasn't considered" is unknowable; the real filter is novelty relative to the Reason field. "Gotchas not implied by the Reason field."

### (c) Rules missing their WHY

1. "when sources disagree, prefer GitHub real code over docs" — why? "Docs describe intent; shipped code is what actually runs." One clause.
2. "Do not fabricate web findings" — a hard guardrail (negation acceptable per benchmark rubric) but unpaired with its positive: pair with what to do instead — already adjacent ("Note it in the synthesis header") — so restructure: "State the gap in the header; the synthesis proceeds GitHub-only" and the prohibition becomes nearly redundant.
3. Same-Name section carries its whys beautifully throughout ("The most-starred or most-trafficked same-name hit is often not the project's"; "This is retrieval noise, not a source conflict") — no findings.

### (d) Hedged / passive imperatives

1. "Partial matches (one strong source only) **require adaptation** — state the adaptation rationale explicitly." — passive construction hides the actor and the action; what *is* adapting? Rewrite: "With only one strong source, adapt its pattern to this repo's constraints and say in one line what you changed and why."
2. "Lower confidence and rely on repo-local evidence first." — fine, active. ✓
3. "surface the most durable takeaway through the host agent's `MEMORY_NOTES`" — "surface… through" is passive plumbing-speak; "Write the single most durable takeaway into MEMORY_NOTES."

### (e) Head-to-head vs benchmark

- Benchmark research is 3 sentences with one epistemic anchor: "Investigate the question against **primary sources**… Follow every claim back to the source that owns it." CC10x's synthesis skill never states a primary-source preference — its nearest analogue is "prefer GitHub real code over docs," which is an instance, not the principle. A synthesis agent weighing a secondary blog against first-party docs has no rule to apply. **Fidelity loss of the benchmark's only load-bearing principle**, in the one cc10x skill descended from it.
- Benchmark: "citing each claim's source." CC10x's synthesis format has a References-for-debugging section but no per-claim citation requirement — claims and sources decouple. Loss.
- Structure: CC10x's fixed synthesis template ("**What changed the recommendation most:** [single sentence]") is a genuinely strong determinism device with no benchmark counterpart — that single-sentence forcing function makes the agent rank its own evidence.

### (f) What CC10x does better

- The Same-Name Disambiguation section is the best original prompt-engineering writing in all six files: a concrete failure mode the benchmark never considers, resolved with an operational anchor rule ("Pin to the version/scope in the project's manifest… the `owner/repo` the lockfile or import path points at") and a quotable principle: "**A finding about the wrong `left-pad` is wrong, not low-confidence.**" That sentence does what benchmark leading-word doctrine asks — collapses a whole policy (don't average, don't hedge, reject) into one memorable token sequence.
- Degradation handling (web-only / GitHub-only / both-down) enumerates the partial-failure matrix exhaustively — checkable, no judgment required.

### (g) Rewrites (file-local)

1. Delete Overview's first paragraph (duplicate of description); keep only "This skill does NOT execute research" + the two researcher pointers.
2. Merge the two conflict-resolution bullets into one: "When sources disagree: code-backed, cross-confirmed findings override single-source prose; shipped code overrides docs (docs describe intent; code is what runs)."
3. Add the missing principle: "Prefer primary sources — the doc, spec, or repo that owns the claim. A secondary write-up citing a primary loses to the primary."
4. "Obvious things the AI already knows" → the deletable-citation test ((b)1).
5. State precedence between router-provided Research Quality and the local scale: "The router's `## Research Quality` block wins; use the local scale only when the block is absent."

---

## Consolidated Top 10 rewrites (suite-wide, ranked by impact)

1. **architecture/SKILL.md ×2** — BEFORE: "fails the two-adapter rule (only one caller/adapter exists)" → AFTER: "fails the two-adapter rule (it is a port with only one adapter — callers and tests don't count as adapters)". Fixes an active contradiction with the canonical source that would veto nearly every single-caller module.
2. **codebase-hygiene** — BEFORE: "would the complexity it holds CONCENTRATE somewhere, or just MOVE elsewhere?" (answers: vanish/reappear) → AFTER: adopt codebase-design's phrasing verbatim: "If I deleted this module and inlined its code at every call site, where does the complexity go? It vanishes → shallow. It reappears across N call sites → deep." Question and answers finally share a vocabulary.
3. **codebase-hygiene** — BEFORE: method starts at "Extract catalog — Grep/Glob for exported functions" → AFTER: prepend "Step 0 — Scope before you scan: take the user's named target, else `git log --oneline` for hot spots; weight recently-changed code — deepening pays off in proportion to future change." Restores the benchmark's YAGNI scoping and its rationale.
4. **exploration** — BEFORE: "One question at a time. Multiple choice preferred." → AFTER: "One question at a time — several at once is bewildering. Offer 2-4 concrete options; open questions get vague answers. Look up facts in the repo instead of asking; only decisions go to the user." Restores grilling's two dropped whys and its facts/decisions split.
5. **architecture** — BEFORE: the entire `## Note` section → AFTER: (deleted). Maintainer changelog masquerading as instruction; ~60 tokens per invocation, zero steering.
6. **research** — BEFORE: "Obvious things the AI already knows" → AFTER: "Any finding you could have written before reading the research files — if deleting the citation leaves the sentence just as defensible, cut the sentence." Vague adjective becomes a runnable test.
7. **domain-modeling** — BEFORE: duplicated READ-ONLY contract (intro bullet + closing section, including duplicated STATUS/REMEDIATION strings) → AFTER: intro bullet becomes "READ-ONLY / OBEY (builders): see 'During the session (READ-ONLY mode)'"; the numbered section is the single source.
8. **codebase-design** — BEFORE: "This skill is the **canonical source**… one source of truth." + "This verdict is **canonical**: `codebase-hygiene` and `architecture` agree with it." → AFTER: (both deleted — the first lives in frontmatter; the second is a no-op agreement claim).
9. **architecture** — BEFORE: "When a module's interface is non-trivial, design it twice… **Second design:** a different approach (not a refinement of the first)." → AFTER: "Design it twice when you can name ≥2 plausible interface shapes or expect ≥3 callers. The second design must differ in shape or seam placement — renamed methods on the first design don't count. Be opinionated in the comparison: recommend one, don't present a menu."
10. **research** — BEFORE: no primary-source principle; two overlapping conflict bullets → AFTER: one merged rule: "Prefer the source that owns the claim (spec, first-party docs, shipped code); code-backed, cross-confirmed findings override single-source prose — docs describe intent, code is what runs."

---

## Cross-cutting observations

1. **The "canonical vocabulary" architecture is prompt-engineered inconsistently.** codebase-design declares itself canonical; architecture pledges not to restate and then restates (and misstates); hygiene restates in full with drifted phrasing. The suite spends ~150 tokens on canonicity *claims* — sentences describing the single-source-of-truth policy — which steer the executing agent not at all, while the actual duplicates drift underneath them. The benchmark's improve-codebase-architecture shows the clean pattern: one pointer, one enforcement rule ("Use these terms exactly in every suggestion"), zero meta-commentary.
2. **Author-facing prose leaks into agent-facing files.** The `## Note` section, "don't restate them here," "Do NOT instruct the agent to call an `Agent` tool it does not have" (DESIGN-IT-TWICE), the upstream HTML comments, and the mid-procedure orchestration asides in exploration's Doubt Pass all address the skill *editor* or the *router author*, not the agent executing the skill. The benchmark contains none of this register-mixing; every sentence has one audience.
3. **CC10x's genuine strengths are real and consistent:** operationalizing what the benchmark leaves fuzzy (ports-vs-seams, badge definitions, stated-not-inferred fast-path gate, blast-radius transform table, same-name disambiguation), and rationale devices the benchmark lacks (scar comments, "Rationalization guard," asymmetric-cost tie-breaks). Where CC10x writes new material, it frequently meets or beats the rubric. Where it *ports*, it is faithful. The failures cluster in the *seams between skills* — restatements, glosses, and cross-references — exactly where no single file's author was looking.

---

## Category counts

| File | (a) dead-weight/contradiction | (b) vague-adjective | (c) missing WHY | (d) hedged/passive | (e) head-to-head comparisons | (f) better-than-benchmark |
|---|---|---|---|---|---|---|
| codebase-design (+2 refs) | 4 | 1 | 1 | 2 | 3 | 3 |
| domain-modeling (+2 refs) | 3 | 1 | 1 | 2 | 3 | 2 |
| architecture | 5 | 4 | 5 | 2 | 3 | 3 |
| codebase-hygiene | 4 | 3 | 3 | 1 | 4 | 3 |
| exploration | 4 | 3 | 5 | 3 | 3 | 3 |
| research | 3 | 4 | 3 | 3 | 3 | 2 |
| **Total** | **23** | **16** | **18** | **13** | **19** | **16** |

Top-10 consolidated rewrites: 10 (plus 22 file-local rewrites embedded in per-file (g) sections).
