---
name: code-review
description: |
  Two-mode skill: (1) adversarial review — spec compliance + code quality + security,
  confidence-scored findings with file:line evidence; (2) receiving review — verify-before-
  agreeing discipline for acting on external/human review feedback.
allowed-tools: Read Grep Glob LSP Bash
user-invocable: false
---

# Code Review (Adversarial + Receiving)

## Reference Files

- `references/review-order-and-checkpoints.md` — review order, checkpoint discipline
- `references/code-review-heuristics.md` — heuristics, pattern recognition, false-positive prevention
- `references/security-review-checklist.md` — security review checklist

---

## Mode: ADVERSARIAL REVIEW

Only report issues with confidence ≥80. Every finding states category, impact, and why it matters. Present a recommendation, not a menu. Be opinionated.

**Signal quality rule:** One finding with `file:line` evidence and a fix is worth more than ten generic observations. Never report a pattern without showing where it lives.

### Two-Stage Review

**Stage 1: Spec Compliance** — Does the code do what the plan/spec asked? Check: phase exit criteria met, interfaces match plan's Consumes/Produces, no scope drift, no missing scenarios.

**Stage 2: Code Quality** — Is the code well-built? Check: correctness, performance, security, clarity, test coverage.

### Review Order

Top-down (spec → architecture → module → function → line) for first pass. Bottom-up (line → function → module) for detail pass. See `references/review-order-and-checkpoints.md`.

### Severity Classification

| Severity | Criteria |
| ---------- | ---------- |
| CRITICAL | Data loss, security breach, silent data corruption |
| HIGH | User-visible broken behavior |
| MEDIUM | Suboptimal but functional |
| LOW | Code smell, style |

### Confidence Scoring

| Confidence | Meaning |
| ----------- | --------- |
| 90-100 | Verified: read the code, confirmed the issue, can cite file:line |
| 80-89 | Strong: read surrounding context, pattern is clear |
| <80 | Do not report — insufficient evidence |

### Parallel Review + Router Merge

When `code-reviewer` and `failure-hunter` run in parallel (BUILD workflow):

- **code-reviewer** (Assessment A): correctness, performance, spec compliance. Forms opinion WITHOUT seeing the hunter's scan.
- **failure-hunter** (Assessment B): silent failure scan using red-flags table. Does NOT see the reviewer's findings.
- **Router-owned merge:** after both complete, the router writes a merged findings summary into the workflow artifact before verifier handoff. Where both agree → high confidence. Where the hunter caught what the reviewer missed → keep. Where the hunter finding is a false positive → drop with reason. Contradictory verdicts: stricter verdict wins, logged in `status_history`.

### Zero-Finding Halt

Zero findings on a non-trivial change → insufficient depth, not perfect code. Re-scan against heuristics and security checklist before reporting CLEAN.

### Code Smells (Fowler Catalog)

Scan for these 12 named smells during review. Each is actionable — not a style preference. "Messy" is not actionable; "Mysterious Name" is:

| Smell | Signal | Fix |
| ------ | ------ | ---- |
| **Mysterious Name** | Function/variable name doesn't reveal intent | Rename to describe what it does |
| **Long Method** | Method > 20 lines doing multiple things | Extract sub-methods |
| **Long Parameter List** | > 4 parameters — consider parameter object | Extract into an object |
| **Large Class** | Class with too many responsibilities | Split by responsibility |
| **Data Class** | Holds data, no behavior — anemic domain model | Move behavior in, or inline the class |
| **Duplicated Code** | Same logic in 3+ places | Extract shared function |
| **Feature Envy** | Method reads more from another class than its own | Move method to the class it envies |
| **Shotgun Surgery** | One change requires touching many files | Consolidate responsibility |
| **Divergent Change** | One class changes for different reasons | Split into separate classes |
| **Primitive Obsession** | Using primitives where a small value object would add meaning | Create a value object |
| **Repeated Switches** | Same switch/if-else on a type across files | Replace with polymorphism |
| **Speculative Generality** | Abstraction for future use that never comes | Delete it (YAGNI) |
| **Message Chains** | `a.b().c().d()` — client knows the object graph | Hide the chain behind a method |
| **Middle Man** | Class just delegates to another — adds no logic | Remove the middleman, use the real object |
| **Refused Bequest** | Subclass doesn't use parent's methods | Replace inheritance with composition |
| **Data Clumps** | 3+ values always passed together | Extract into an object |

**Repo standards override baseline:** if the repo's documented conventions endorse something this baseline would flag, suppress the smell.

### AI-Generated Anti-Patterns

Patterns commonly produced by AI code generation — flag with elevated priority:

- **Over-eager memoization** — `useMemo`/`useCallback`/`React.memo` wrapping everything without profiling evidence
- **State duplication** — same state stored in 2+ places, kept in sync manually (source of truth unclear)
- **Sequential awaits** — independent async calls awaited sequentially instead of `Promise.all` (latency multiplier)
- **Over-fetching** — fetching full objects (or more than the current view needs) when only one field is needed
- **Premature abstraction / speculative generality** — interface with single implementation "for future flexibility"
- **Configurable when it should be constant** — adding options/flags for flexibility nobody asked for
- **Defensive coding for impossible states** — null checks / over-engineered error handling for scenarios that can't happen (values typed non-nullable, internal code boundaries)
- **Test mirrors implementation** — test recomputes expected value using the same logic as the code (tautological test)
- **Factory overkill** — factory pattern for objects with no polymorphism
- **Type assertions instead of type guards** — `as any`/`as Type` instead of narrowing with a runtime check

### Metric Honesty Rule

Never fabricate metrics. An LLM reading static source code cannot measure real-world LCP, INP, CLS, memory usage, or runtime performance.

- **Can assess from code:** algorithmic complexity (O(n) vs O(n²)), N+1 query patterns, obvious hot loops, missing indices
- **Cannot assess from code:** real-world latency, actual memory pressure, real INP/LCP/CLS values

State what you CAN verify from code. Tag anything else as "potential impact, not measured" — never invent numbers. Recommend specific tools (Lighthouse, profiler, benchmark suite) when runtime measurement is the real answer.

### Deferred Findings (Not "Residual" — Already Wired)

Minor/Medium findings you don't fix in this pass are NOT dropped, but you do NOT need a separate file or a separate CONTRACT field for them. Just report them normally with severity and file:line in your output. **The router already handles persistence**: it reads your findings, appends every non-blocking Minor item to the workflow artifact's `deferred_findings` array (source, phase, finding, severity), and surfaces the accumulated list for explicit user triage at BUILD-DONE finishing. Nothing is silently discarded — this is automatic on the router side, not something you need to engineer in your response.

### False Positive Prevention

Do NOT flag:

- Code that matches an explicit project convention (check patterns.md)
- Intentional simplification documented in the plan
- Test-only code using test patterns (mocks, fixtures, stubs)
- Performance "issues" without a measured bottleneck
- Style preferences that don't match project conventions

---

## Mode: RECEIVING REVIEW

Discipline for acting on external/human review feedback (pasted PR comments, review notes, "can you change X"). This governs the MAIN session, not the internal reviewer→router→fix loop.

### The 6-Step Loop

1. **Read all feedback** before responding to any item
2. **Categorize** each item: CRITICAL (must fix), IMPORTANT (should fix), MINOR (optional), REJECT (with reason)
3. **Verify before agreeing** — don't blindly accept. Check if the feedback is correct against the code.
4. **Fix accepted items** — CRITICAL first, then IMPORTANT
5. **Push back on rejected items** — with evidence, not opinion
6. **Report** — what was fixed, what was rejected and why

### Verify Before Agreeing

Before implementing a suggestion, check:

- Does the issue actually exist in the code? (read the file:line)
- Is the suggested fix correct? (would it actually fix the issue?)
- Does the fix introduce new problems? (side effects, breaking changes)
- Is the suggestion based on a correct understanding of the code?

### YAGNI-Grep Before Implementing

Before implementing a suggestion, grep the codebase for the pattern the reviewer claims is wrong. If the pattern is project convention (appears in many places, is in patterns.md), push back. If it's genuinely isolated, fix it.

### When To Push Back

| Situation | Response |
| ----------- | ---------- |
| Reviewer misunderstood the code | Explain with file:line evidence |
| Suggestion contradicts project convention | Cite the convention, push back |
| Suggestion adds unnecessary complexity | YAGNI — state why the simpler approach is better |
| Suggestion is correct but out of scope | Acknowledge, defer to a follow-up |
| Suggestion is a style preference | Acknowledge, apply only if it matches project conventions |

### Precedence

Pushing back ≠ refusing. You must either fix the issue or provide evidence why it's not an issue. "I prefer my way" is not a valid push-back. "This is project convention, see patterns.md line X" is valid.

## Note

The Fowler Code Smells catalog, AI-Generated Anti-Patterns, Metric Honesty Rule, and Deferred Findings handling are defined once above under **Mode: ADVERSARIAL REVIEW**. There is no second copy — apply those sections during both the adversarial pass and any receiving-review triage.
