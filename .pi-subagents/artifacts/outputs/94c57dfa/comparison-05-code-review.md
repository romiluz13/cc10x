# Deep Comparison: Code Review & Quality Enforcement

## Projects Analyzed

| Project | Files Reviewed |
| --------- | --------------- |
| **cc10x** | `code-reviewer.md`, `silent-failure-hunter.md`, `silent-failure-red-flags.md`, `code-review/SKILL.md`, `review-workflow.md`, `code-review-heuristics.md`, `review-order-and-checkpoints.md`, `security-review-checklist.md` |
| **Superpowers** | `receiving-code-review/SKILL.md`, `requesting-code-review/SKILL.md`, `requesting-code-review/code-reviewer.md` |
| **Matt Pocock** | `engineering/code-review/SKILL.md` |

---

## 1. How Each Project Structures Code Review (Passes, Dimensions, Severity)

### cc10x

**Structure: 6 ordered passes + parallel agent split**

cc10x runs two specialized agents in parallel — a **code-reviewer** and a **silent-failure-hunter** — then the router merges their findings. The code-reviewer itself runs 6 sequential passes:

| Pass | Focus | Severity Class |
| ------ | ------- | --------------- |
| Pass 1 | Security (auth, injection, secrets, XSS/CSRF) | HARD (CRITICAL) |
| Pass 2 | Performance (N+1, hot loops, memory, caching) | SOFT |
| Pass 3 | Quality (complexity, naming, error handling, DRY, types) | MIXED |
| Pass 4 | Friction Scan (architectural coupling, fragmentation, shallow modules) | SOFT |
| Pass 5 | Plan Validity (is the PLAN itself correct?) | PLAN_DEFECT |
| Pass 6 | Spec Compliance (does code diverge from approved spec?) | First-class verdict |

**Severity levels:** CRITICAL → HIGH → MEDIUM → LOW, with explicit decision trees.

**Confidence scoring:** Numerical 0–100 per dimension. HARD dimensions (security, correctness) can zero out the entire score. SOFT dimensions (performance, maintainability, UX) cap the score via `avg(SOFT) - 10`. Only findings at ≥80 confidence are reported.

**Multi-signal scoring formula:** `CONFIDENCE = min(HARD scores)` capped by `avg(SOFT scores) - 10`. This is the most quantitative scoring system of the three.

### Superpowers

**Structure: Single-pass, template-driven, severity-tiered**

Superpowers uses a single `general-purpose` subagent with a detailed prompt template (`code-reviewer.md`). The review covers five categories in one pass:

1. Plan alignment
2. Code quality (separation of concerns, error handling, types, DRY, edge cases)
3. Architecture (design, scalability, security, integration)
4. Testing (real behavior vs mocks, edge cases, integration tests)
5. Production readiness (migrations, backward compatibility, docs, bugs)

**Severity levels:** Critical (Must Fix) → Important (Should Fix) → Minor (Nice to Have). Three tiers, no numerical scoring.

**Output format:** Strengths → Issues (by severity) → Recommendations → Assessment (Ready to merge? Yes/No/With fixes).

**No confidence scoring** — findings are qualitative with file:line references. Calibration is instructed ("not everything is Critical") but there's no quantitative mechanism.

### Matt Pocock

**Structure: Two-axis parallel sub-agent split**

Matt Pocock's approach is structurally unique: two parallel sub-agents run simultaneously on two independent axes:

- **Standards axis** — does code conform to the repo's documented coding standards + a fixed Fowler code-smells baseline?
- **Spec axis** — does code faithfully implement the originating issue/PRD/spec?

Each sub-agent has a strict 400-word limit. The aggregator presents both reports side-by-side **without merging or reranking** — the axes are deliberately separate to prevent one from masking the other.

**Severity:** No explicit severity tiers. The Standards axis distinguishes "hard violations" (documented standard breaches) from "judgement calls" (baseline smells). The Spec axis categorizes findings as missing/partial, scope creep, or wrong implementation.

**Code smells baseline:** 12 named Fowler smells (Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest) — each with a "what it is → how to fix" format. Repo-documented standards override the baseline.

---

## 2. How Each Project Handles Review Feedback (Receiving, Acting On, Resolving)

### cc10x

cc10x has a **dual-mode feedback system**:

**Internal loop (reviewer → router → builder):**

- Reviewer emits structured `CONTRACT` JSON envelope (`s`, `b`, `cr`) + heading as machine-readable signal
- Router reads the contract, decides remediation scope (`CRITICAL_ONLY` vs `ALL_ISSUES`)
- Router creates REM-FIX tasks for the builder — the reviewer never creates tasks directly
- Remediation intent fields (`REMEDIATION_NEEDED`, `REMEDIATION_SCOPE_REQUESTED`, `REVERT_RECOMMENDED`) communicate intent to the router
- `PLAN_DEFECT` is routed to the **planner**, not the builder — code may be correct but the plan is wrong
- `SPEC_COMPLIANCE` divergences route to the **implementer** as REM-FIX
- `CANNOT_VERIFY_CROSS_PHASE` items require router reconciliation before phase exit gate passes

**External loop (receiving human feedback) — defined in code-review SKILL.md Mode: RECEIVING REVIEW:**

- 6-step loop: Read all → Categorize → Verify before agreeing → Fix accepted → Push back on rejected → Report
- YAGNI-Grep before implementing: grep for the pattern the reviewer claims is wrong; if it's project convention, push back
- Explicit push-back table: reviewer misunderstood code, contradicts convention, adds complexity, out of scope, style preference
- "Pushing back ≠ refusing" — must either fix or provide evidence why it's not an issue

### Superpowers

Superpowers has the **most developed receiving-feedback discipline** of the three:

**Receiving Code Review skill (`receiving-code-review/SKILL.md`):**

- 6-step response pattern: READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT
- **Forbidden responses:** "You're absolutely right!", "Great point!", "Let me implement that now" (before verification)
- **Source-specific handling:** Human partner feedback (trusted, still ask if scope unclear) vs External reviewer feedback (skeptical, check 5 criteria before implementing)
- **YAGNI check:** grep for actual usage before implementing "professional" features
- **Implementation order:** Clarify unclear items FIRST → blocking issues → simple fixes → complex fixes → test each individually
- **Graceful correction:** If you pushed back and were wrong, state factually and move on — no long apologies
- **GitHub thread replies:** Reply in comment threads, not top-level PR comments

**Requesting Code Review skill (`requesting-code-review/SKILL.md`):**

- Dispatch a subagent with precisely crafted context (not session history)
- Review after each task in subagent-driven development (mandatory)
- Review before merge (mandatory)
- Act on feedback: fix Critical immediately, fix Important before proceeding, note Minor for later, push back if wrong

### Matt Pocock

Matt Pocock has **no explicit feedback-receiving or resolution discipline**. The skill is purely about generating the review — the two sub-agents produce their reports, the aggregator presents them side-by-side, and the output ends with a one-line summary per axis. There is no guidance on:

- How to act on the findings
- How to verify feedback before implementing
- How to push back on incorrect findings
- How to track resolution of issues
- Whether findings block or are advisory

The skill is a **review generation tool**, not a review lifecycle system.

---

## 3. Review Dimensions Covered

| Dimension | cc10x | Superpowers | Matt Pocock |
| ----------- | ------- | ------------- | ------------- |
| Security | ✅ Dedicated pass + security checklist + quick-scan commands | ✅ Listed under Architecture | ❌ Not explicitly covered |
| Performance | ✅ Dedicated pass (N+1, hot loops, memory, caching) | ✅ Listed under Architecture ("reasonable scalability") | ❌ Not explicitly covered |
| Correctness/Logic | ✅ HARD signal (logic errors = 0) | ✅ Listed under Code Quality | ✅ Via Spec axis (implementation looks wrong) |
| Error Handling | ✅ Dedicated silent-failure-hunter agent | ✅ Listed under Code Quality | ❌ Not explicitly covered |
| Spec Compliance | ✅ First-class verdict (Pass 6, independent gating) | ✅ Listed under Plan alignment | ✅ Dedicated Spec axis sub-agent |
| Plan Validity | ✅ Unique Pass 5 (is the PLAN wrong?) | ✅ "If you find issues with the plan itself, say so" | ❌ Not explicitly separated |
| Maintainability | ✅ SOFT signal + friction scan | ✅ DRY, separation of concerns | ✅ Via Standards axis (Fowler smells) |
| Code Smells | ✅ Sloppy pattern scan in heuristics | ✅ Implicit | ✅ 12 named Fowler smells as baseline |
| Testing | ✅ Tests verify behavior (not just presence) | ✅ Dedicated section (real behavior vs mocks, edge cases) | ❌ Not explicitly covered |
| Architecture | ✅ Friction scan (fragmentation, coupling, shallow modules) | ✅ Dedicated section | ✅ Implicit via Fowler smells |
| Types | ✅ No `any`, types match runtime | ✅ "Type safety where applicable" | ❌ Not explicitly covered |
| UX/A11y | ✅ SOFT signal (missing states) | ❌ Not covered | ❌ Not covered |
| Naming | ✅ MEDIUM severity finding | ❌ Not explicitly covered | ✅ Mysterious Name smell |
| Duplication | ✅ MEDIUM severity (DRY) | ✅ DRY principle | ✅ Duplicated Code smell |
| Production Readiness | ❌ Not explicitly covered as a dimension | ✅ Dedicated section (migrations, backward compat, docs) | ❌ Not explicitly covered |
| Silent Failures | ✅ Dedicated parallel agent (unique) | ❌ Not covered | ❌ Not covered |
| Cross-phase Verification | ✅ CANNOT_VERIFY_CROSS_PHASE mechanism | ❌ Not covered | ❌ Not covered |

---

## 4. How Each Project Enforces Review Gates (Blocking vs Advisory)

### cc10x

**Multi-layered gate system — the most sophisticated of the three:**

1. **CRITICAL findings → CHANGES_REQUESTED** — automatically blocks. Any HARD:0 dimension = CONFIDENCE:0 regardless of other dimensions.
2. **SPEC_COMPLIANCE → independent gate** — any MISSING/EXTRA/MISUNDERSTOOD finding gates to CHANGES_REQUESTED even when all SIGNAL_SCORES are clean. "Built the wrong thing well" still blocks.
3. **PLAN_DEFECT → routed to planner** — the code may be APPROVABLE as written, but the plan needs revision. This is a separate routing path, not a code-fix.
4. **CANNOT_VERIFY_CROSS_PHASE → unresolved = FAILED review** — the phase exit gate does not pass on an unverified cross-phase requirement.
5. **Zero-Finding Gate** — if all passes produce zero findings, the reviewer MUST: (a) verify they read changed files, (b) name at least one positive assertion with file:line evidence, (c) if still zero, set CONFIDENCE to min(CONFIDENCE, 70). A zero-finding review at CONFIDENCE ≥90 is **invalid** without positive-assertion evidence.
6. **Security Stop** — if ANY pass (not just Pass 1) surfaces a security signal, it's immediately CRITICAL regardless of which pass found it.
7. **REVIEW workflow mode** — advisory only. The reviewer can emit CHANGES_REQUESTED but cannot create REM-FIX tasks. The router may offer "Start BUILD to fix" as a user choice.
8. **BUILD/DEBUG workflow mode** — router owns remediation. Reviewer requests scope; router decides CRITICAL_ONLY vs ALL_ISSUES after merging with silent-failure-hunter findings.
9. **Anti-anchoring** — reviewer is explicitly forbidden from reading `activeContext.md` (the implementer's self-assessment) before review, to prevent anchoring bias.

### Superpowers

**Severity-based gating with human judgment:**

- **Critical (Must Fix)** — fix immediately
- **Important (Should Fix)** — fix before proceeding
- **Minor (Nice to Have)** — note for later
- **Assessment verdict:** Ready to merge? Yes / No / With fixes

Gating is **advisory with strong norms** — the instructions say "Never skip review because 'it's simple'" and "Never proceed with unfixed Important issues" but there is no automated blocking mechanism. The human or orchestrator decides whether to proceed.

The requesting skill mandates review "after each task in subagent-driven development" and "before merge to main" — these are process gates, not technical gates.

### Matt Pocock

**No gating mechanism.** The skill produces a report with two axes side-by-side. There is:

- No blocking mechanism
- No severity-based gating
- No approval/rejection verdict
- No automated routing of findings
- No "ready to merge" assessment

The skill is purely informational. The user or orchestrator must decide what to do with the findings. The one-line summary gives "total findings per axis, and the worst issue within each axis" but does not prescribe action.

---

## 5. Parallel Review Patterns

### cc10x — ✅ Most Sophisticated

**Parallel agent architecture:**

- `code-reviewer` (Assessment A): correctness, performance, spec compliance, plan validity — forms opinion **WITHOUT** seeing the hunter's findings
- `silent-failure-hunter` (Assessment B): silent failure scan using red-flags table — does **NOT** see the reviewer's findings
- Both agents are deliberately isolated to prevent opinion contamination

**Router-owned merge:**

- Where both agree → high confidence
- Where hunter caught what reviewer missed → keep
- Where hunter finding is a false positive → drop with reason
- Contradictory verdicts → **stricter verdict wins**, logged in `status_history`

**Merge is post-hoc and asymmetric:** the router has authority to drop false positives, escalate agreements, and resolve contradictions. The two agents never see each other's work — the merge is a third-party reconciliation.

### Matt Pocock — ✅ Parallel, Structured Differently

**Two parallel sub-agents on orthogonal axes:**

- Standards sub-agent: checks code against documented standards + Fowler smells baseline
- Spec sub-agent: checks code against originating issue/PRD/spec

**Key difference from cc10x:** The axes are **deliberately non-overlapping** — Standards and Spec are orthogonal concerns. cc10x's two agents both review the same dimensions (quality + failures) from different angles. Matt Pocock's agents review **different dimensions** entirely.

**Aggregation rule:** Present both reports **verbatim or lightly cleaned**. Do NOT merge or rerank. "Don't pick a single winner across axes — that's the reranking the separation exists to prevent." This is a philosophical stance: the two axes should never mask each other.

### Superpowers — ❌ No Parallel Review

Superpowers dispatches a single `general-purpose` subagent. There is no parallel review pattern. The receiving-code-review skill addresses human review feedback, not parallel agent review.

---

## 6. What Review Patterns Does cc10x Have That Others DON'T?

| Pattern | Description |
| --------- | ------------- |
| **Silent Failure Hunter** | A dedicated parallel agent that exclusively hunts silent failures (empty catches, log-only handlers, generic errors, `?.` chains without logging, ` | | defaultValue` masking). Language-specific red flags for Python, Go, Java, Rust, Shell, JS/TS. Neither Superpowers nor Matt Pocock has anything like this. |
| **Plan Validity Pass (Pass 5)** | Separates "the code is wrong" from "the plan is wrong." If the code faithfully implements a flawed plan, it emits `PLAN_DEFECT` which routes to the planner, not the builder. This is a unique architectural insight — other projects conflate plan issues with code issues. |
| **Spec Compliance as first-class verdict** | Spec compliance is a SEPARATE verdict from code quality, with its own gating. Code can be high-quality but spec-non-compliant ("built the wrong thing well") and that still blocks. Matt Pocock has a Spec axis but doesn't gate on it. |
| **CANNOT_VERIFY_CROSS_PHASE** | A mechanism for requirements wired in one phase but consumed in another. The router must reconcile before the phase exit gate passes. Neither other project addresses cross-phase verification. |
| **Quantitative confidence scoring** | 0–100 numerical scoring with HARD/SOFT signal classification and a formula: `min(HARD)` capped by `avg(SOFT) - 10`. Other projects use qualitative severity tiers. |
| **Zero-Finding Gate** | If all passes produce zero findings, the review is under-supported. The reviewer must produce positive assertions with file:line evidence or downgrade confidence. A zero-finding review at ≥90 confidence is **invalid**. Neither other project has this. |
| **Anti-anchoring protocol** | Reviewer is explicitly forbidden from reading the implementer's self-assessment (`activeContext.md`) before review. This is a deliberate bias-prevention mechanism unique to cc10x. |
| **Memory-first protocol** | Reviewer reads `patterns.md` (project conventions) and `progress.md` (known issues) before review — so it doesn't re-flag known issues and enforces real conventions. Neither other project has this. |
| **Friction Scan (Pass 4)** | Architectural friction detection with quantitative thresholds: >4 files across >2 directories for one concept = MEDIUM, interface surface > implementation = MEDIUM, >3 cross-imports with no boundary = HIGH. Neither other project has quantitative architectural thresholds. |
| **Security Stop** | If ANY pass (not just the security pass) surfaces a security signal, it's immediately CRITICAL. This cross-pass escalation rule is unique. |
| **Diff package discipline** | Explicit rules about not re-reading changed files from disk (use hunk context), not moving HEAD, using `git worktree` for alternative revisions. Neither other project has this level of git hygiene. |
| **Verdict-before-response rule** | The verdict must be decided BEFORE writing the final response, and the first two lines of the response state it. "Never write a provisional verdict intending to revise it later." This prevents verdict drift. |
| **Forbidden verdict-softeners** | "looks fine", "LGTM", "ship it", "no major issues", "should be okay", "probably safe" are explicitly banned. Other projects allow qualitative language. |
| **Self-grading downgrade prevention** | An implementer's stated rationale ("left it per YAGNI", "intentional, see plan") cannot downgrade a finding's severity. It's the implementer grading their own work. Neither other project addresses this bias. |
| **Scope guard** | If >10 files read without any finding, produce a preliminary verdict. Additional reads must be justified by a specific hypothesis. Prevents scope creep in review. |
| **Review workflow advisory mode** | REVIEW workflow is advisory-only — the reviewer can emit CHANGES_REQUESTED but cannot create REM-FIX tasks. The router may offer "Start BUILD to fix" as a user choice. This separates advisory review from enforcement. |

---

## 7. What Review Patterns Do the Others Have That cc10x SHOULD Adopt?

### From Superpowers

| Pattern | Why cc10x Should Adopt It |
| --------- | -------------------------- |
| **Forbidden performative responses** | Superpowers explicitly bans "You're absolutely right!", "Great point!", "Thanks for catching that!" and ALL gratitude expressions. cc10x bans verdict-softeners but doesn't address the social/performative dimension. This is a valuable anti-sycophancy pattern. |
| **Source-specific handling** | Superpowers distinguishes between trusted human partner feedback (implement after understanding) and external reviewer feedback (skeptical, check 5 criteria). cc10x's receiving-review mode treats all feedback uniformly. |
| **Graceful correction protocol** | When you pushed back and were wrong, Superpowers says: state factually, move on, no long apology, no defending why you pushed back. cc10x doesn't address the case where the reviewer's push-back was itself wrong. |
| **GitHub thread reply guidance** | Superpowers specifies replying in comment threads via `gh api`, not top-level PR comments. cc10x has no GitHub integration guidance. |
| **Implementation order for multi-item feedback** | Superpowers prescribes: clarify unclear items FIRST → blocking issues → simple fixes → complex fixes → test each individually. cc10x's receiving-review mode has a 6-step loop but doesn't prescribe fix ordering. |
| **"If you're uncomfortable pushing back out loud"** | Superpowers acknowledges the emotional difficulty of pushback and suggests naming the tension. This is a psychological safety pattern cc10x lacks. |
| **Review when stuck** | Superpowers suggests requesting review when stuck (fresh perspective) and before refactoring (baseline check). cc10x only reviews at phase boundaries. |

### From Matt Pocock

| Pattern | Why cc10x Should Adopt It |
| --------- | -------------------------- |
| **Fowler code smells baseline** | 12 named smells (Mysterious Name, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest) with "what it is → how to fix" format. cc10x has a sloppy-pattern scan and friction scan but lacks this structured, named-smell vocabulary. This is more actionable than generic "maintainability" checks. |
| **Repo-overrides-baseline rule** | Documented repo standards always win over the baseline. Where a repo endorses something the baseline would flag, suppress the smell. cc10x has a false-positive prevention section but doesn't explicitly subordinate its heuristics to repo-documented standards. |
| **Deliberate non-merging of orthogonal axes** | Matt Pocock's philosophy that Standards and Spec should never mask each other — "don't pick a single winner across axes" — is a design principle cc10x could benefit from. cc10x merges everything into one CONFIDENCE score, which could let a clean code-quality score mask a spec-compliance failure. (cc10x does gate SPEC_COMPLIANCE independently, but the SIGNAL_SCORES summary could still be misleading.) |
| **Strict word limit on sub-agent reports** | 400 words per sub-agent. This forces concision and prevents rambling. cc10x has no output length constraints. |
| **Three-dot diff for merge-base comparison** | `git diff <fixed-point>...HEAD` (three-dot) compares against the merge-base, which is more correct for branched workflows. cc10x uses two-dot `$BASE..HEAD` which compares the tips directly. |
| **Spec source discovery pipeline** | Matt Pocock has a structured process for finding the spec: issue references in commits → user-provided path → PRD/spec files matching branch name → ask user. cc10x assumes the spec is provided by the router. |
| **Pre-flight validation** | Before spawning sub-agents, Matt Pocock confirms the fixed point resolves and the diff is non-empty. "A bad ref or empty diff should fail here — not inside two parallel sub-agents." cc10x doesn't have this pre-flight check. |

---

## 8. Rating Each Project's Code Review Methodology

### cc10x — **8.5/10**

**Strengths:**

- Most comprehensive multi-pass review system (6 ordered passes)
- Only project with a dedicated silent-failure-hunter agent running in parallel
- Quantitative confidence scoring with HARD/SOFT signal separation
- Plan Validity pass is a unique architectural insight (separate plan defects from code defects)
- Spec compliance as an independent first-class gating verdict
- Zero-Finding Gate prevents rubber-stamp approvals
- Anti-anchoring protocol prevents reviewer bias
- Memory-first protocol enforces real conventions and avoids re-flagging known issues
- Cross-phase verification mechanism
- Router-owned remediation with structured routing (planner vs builder vs implementer)
- Friction scan with quantitative architectural thresholds
- Self-grading downgrade prevention

**Weaknesses:**

- No structured code-smell vocabulary (could adopt Matt Pocock's Fowler baseline)
- No output length constraints on agent reports
- Receiving-review mode lacks the social/performative discipline of Superpowers
- No pre-flight validation before spawning agents
- Two-dot diff instead of three-dot merge-base comparison
- No GitHub integration guidance
- The system is complex — 6 passes + 2 parallel agents + router merge + memory protocol may be difficult to maintain and calibrate

### Superpowers — **6.5/10**

**Strengths:**

- Best receiving-feedback discipline of the three (forbidden performative responses, source-specific handling, graceful correction, YAGNI check)
- Clear implementation ordering for multi-item feedback
- Practical GitHub integration guidance
- Psychological safety acknowledgment ("if you're uncomfortable pushing back")
- Simple, actionable requesting workflow with template
- Review-early-review-often philosophy with mandatory checkpoints

**Weaknesses:**

- No parallel review
- No quantitative scoring or confidence system
- No dedicated security pass (security is a sub-item under Architecture)
- No silent failure detection
- No plan-validity separation
- No spec-compliance as independent gating
- Single-pass review with a general-purpose subagent (no specialization)
- No automated gating mechanism (advisory only)
- No memory/convention awareness
- No zero-finding guard

### Matt Pocock — **5.5/10**

**Strengths:**

- Elegant two-axis parallel structure (Standards vs Spec) with deliberate non-merging
- 12 named Fowler code smells as a structured, actionable baseline
- Repo-overrides-baseline rule is well-thought-out
- Strict 400-word limit forces concision
- Pre-flight validation before spawning agents
- Spec source discovery pipeline
- Three-dot diff for correct merge-base comparison
- Philosophical clarity on why axes should remain separate

**Weaknesses:**

- No gating mechanism at all (purely informational)
- No receiving-feedback or resolution discipline
- No security dimension explicitly covered
- No performance dimension explicitly covered
- No testing dimension explicitly covered
- No error handling / silent failure detection
- No confidence scoring
- No plan-validity separation
- No memory/convention awareness
- No cross-phase verification
- No production readiness checks
- Coverage is narrow — only Standards and Spec, missing security, performance, testing, error handling

---

## Structured Comparison Summary

| Criterion | cc10x | Superpowers | Matt Pocock |
| ----------- | ------- | ------------- | ------------- |
| **Passes/Structure** | 6 ordered passes + parallel agent | Single-pass, 5 categories | 2 parallel axes (Standards + Spec) |
| **Parallel Review** | ✅ 2 agents, same dimensions, router merges | ❌ | ✅ 2 agents, orthogonal axes, no merge |
| **Severity System** | CRITICAL/HIGH/MEDIUM/LOW + 0-100 confidence | Critical/Important/Minor | Hard violation vs judgement call |
| **Quantitative Scoring** | ✅ HARD/SOFT formula | ❌ | ❌ |
| **Spec Compliance** | ✅ First-class independent gate | ✅ Sub-item | ✅ Dedicated axis |
| **Plan Validity** | ✅ Separate from code quality | ✅ Mentioned | ❌ |
| **Security** | ✅ Dedicated pass + checklist + quick-scan | ✅ Sub-item | ❌ |
| **Silent Failures** | ✅ Dedicated parallel agent | ❌ | ❌ |
| **Cross-phase Verification** | ✅ | ❌ | ❌ |
| **Receiving Feedback** | ✅ 6-step loop + YAGNI-grep | ✅ Best-in-class | ❌ |
| **Push-back Discipline** | ✅ Push-back table | ✅ Detailed + emotional | ❌ |
| **Anti-sycophancy** | ✅ Verdict-softeners banned | ✅ Performative responses banned | ❌ |
| **Memory/Convention Awareness** | ✅ patterns.md + progress.md | ❌ | ✅ Repo standards override baseline |
| **Code Smells** | ✅ Sloppy pattern scan | ✅ Implicit | ✅ 12 named Fowler smells |
| **Zero-Finding Guard** | ✅ Mandatory with confidence downgrade | ❌ | ❌ |
| **Gating Mechanism** | ✅ Multi-layered (auto-block + advisory mode) | ⚠️ Advisory with norms | ❌ None |
| **Output Constraints** | ❌ No length limit | ❌ No length limit | ✅ 400 words per sub-agent |
| **GitHub Integration** | ❌ | ✅ Thread reply guidance | ❌ |
| **Production Readiness** | ❌ | ✅ Dedicated section | ❌ |
| **Pre-flight Validation** | ❌ | ❌ | ✅ |
| **Rating** | **8.5/10** | **6.5/10** | **5.5/10** |

---

## Verdict

**cc10x has the most sophisticated and comprehensive code review methodology of the three projects.** It is the only system that combines:

1. Multi-pass adversarial review with quantitative confidence scoring
2. A dedicated parallel silent-failure-hunter agent
3. Plan-validity as a distinct concern from code quality
4. Spec compliance as an independent gating verdict
5. Cross-phase verification
6. Memory-driven convention awareness
7. Anti-anchoring bias prevention
8. Zero-finding guards with mandatory positive assertions
9. Router-owned remediation with structured routing

**However, cc10x should adopt three key patterns from the others:**

1. **From Matt Pocock:** The 12 named Fowler code smells as a structured baseline vocabulary — this is more actionable than cc10x's generic "maintainability" scan. Also the repo-overrides-baseline rule and three-dot diff.

2. **From Superpowers:** The forbidden performative responses pattern (banning "Great point!" etc.) — cc10x bans verdict-softeners but not social sycophancy. Also the implementation ordering for multi-item feedback and GitHub thread reply guidance.

3. **From Matt Pocock:** Pre-flight validation before spawning agents and strict output length constraints to force concision.

**Superpowers excels at the human dimension** — how to receive, evaluate, and act on review feedback — but lacks the technical depth and automated gating of cc10x.

**Matt Pocock has the most elegant structural philosophy** (orthogonal axes that never mask each other) and the most actionable code-smell vocabulary, but lacks gating, security coverage, and feedback resolution discipline.

The ideal system would combine cc10x's multi-pass adversarial engine with Matt Pocock's Fowler smells baseline and orthogonal-axis philosophy, and Superpowers' receiving-feedback discipline and anti-sycophancy patterns.
