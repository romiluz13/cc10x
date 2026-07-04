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

Use these named smells for precision. "Messy" is not actionable; "Long Parameter List" is:

| Smell | Signal |
| ---------- | -------- |
| **Long Method** | Method > 20 lines doing multiple things |
| **Long Parameter List** | > 4 parameters — consider parameter object |
| **Large Class** | Class with too many responsibilities |
| **Data Class** | Holds data, no behavior — anemic domain model |
| **Duplicate Code** | Same logic in 2+ places |
| **Feature Envy** | Method uses another class's data more than its own |
| **Shotgun Surgery** | One change requires touching many classes |
| **Divergent Change** | One class changes for different reasons |
| **Primitive Obsession** | Using primitives where a value object applies |
| **Long Parameter List** | Excessive parameters suggest hidden responsibility |
| **Speculative Generality** | Abstractions with no current caller |
| **Data Clumps** | Same 3+ fields always passed together — extract a value object |

### AI-Generated Anti-Patterns

Patterns commonly produced by AI code generation — flag with elevated priority:

- **Over-eager memoization** — `useMemo`/cache on values that are cheap to compute (adds overhead, not saves it)
- **State duplication** — same state stored in 2+ places, kept in sync manually (source of truth unclear)
- **Sequential awaits** — independent async calls awaited sequentially instead of `Promise.all` (latency multiplier)
- **Over-fetching** — fetching full objects when only one field is needed
- **Premature abstraction** — interface with single implementation "for future flexibility"
- **Defensive coding for impossible states** — null checks on values typed non-nullable
- **Test mirrors implementation** — test recomputes expected value using same logic as code (tautological test)
- **Factory overkill** — factory pattern for objects with no polymorphism

### Metric Honesty Rule

Never fabricate metrics. An LLM reading static source code cannot measure real-world LCP, INP, CLS, memory usage, or runtime performance. When reviewing performance:

- **Can assess:** algorithmic complexity (O(n) vs O(n²)), N+1 query patterns, obvious hot loops, missing indices
- **Cannot assess:** real-world latency, actual memory pressure, real INP/LCP values

State what you CAN verify from code. Flag what REQUIRES runtime measurement. Never invent numbers.

### Residual Review Findings

Findings classified as MEDIUM/LOW that are not fixed in this cycle are NOT dropped. The reviewer must:

1. List each unaddressed finding with severity and file:line
2. State why it was deferred (out of scope, requires larger refactor, needs design decision)
3. Emit them in the CONTRACT under `RESIDUAL_FINDINGS`

The router persists residual findings into the workflow artifact. Future REVIEW workflows read prior residual findings and check whether they've been addressed. Deferred issues never become invisible.

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

## Fowler Code Smells Baseline

Scan for these 12 named code smells during review. Each is actionable — not a style preference:

| Smell | What It Is | Fix |
| ------ | ----------- | ----- |
| Mysterious Name | Function/variable name doesn't reveal intent | Rename to describe what it does |
| Duplicated Code | Same logic in 3+ places | Extract shared function |
| Feature Envy | Method reads more from another class than its own | Move method to the class it envies |
| Data Clumps | 3+ values always passed together | Extract into an object |
| Primitive Obsession | Using primitives where a small class would add meaning | Create a value object |
| Repeated Switches | Same switch/if-else on a type across files | Replace with polymorphism |
| Shotgun Surgery | One change requires touching many files | Consolidate responsibility |
| Divergent Change | One class changes for different reasons | Split into separate classes |
| Speculative Generality | Abstraction for future use that never comes | Delete it (YAGNI) |
| Message Chains | `a.b().c().d()` — client knows the object graph | Hide the chain behind a method |
| Middle Man | Class just delegates to another — adds no logic | Remove the middleman, use the real object |
| Refused Bequest | Subclass doesn't use parent's methods | Replace inheritance with composition |

**Repo standards override baseline:** if the repo's documented conventions endorse something the baseline would flag, suppress the smell.

## AI-Generated Anti-Patterns

LLM-generated code has specific failure modes. Scan for these during review:

- **Over-eager memoization:** `useMemo`/`useCallback`/`React.memo` wrapping everything without profiling evidence
- **State duplication:** same state stored in two places with manual sync logic instead of lifting state
- **Sequential awaits** when `Promise.all` would work — unnecessary serialization of independent operations
- **Over-fetching** data "just in case" — fetching more than the current view needs
- **Over-engineered error handling** for scenarios that can't happen (internal code boundaries)
- **Configurable when it should be constant** — adding options/flags for flexibility nobody asked for
- **Type assertions instead of type guards** — `as any` or `as Type` instead of narrowing with a runtime check

## Metric Honesty Rule

Never fabricate performance metrics. An LLM reading static source code cannot measure real-world LCP, INP, CLS, memory usage, or execution time. If no measurement data is available:

- Tag all performance findings as "potential impact", not measurements
- Mark the scorecard "not measured"
- Recommend specific tools to get real data (Lighthouse, profiler, benchmark suite)

## Residual Review Findings

When review findings are not applied in the current PR, persist them as a durable artifact:

```markdown
# Residual Review Findings
Source: cc10x review run {run_id} on branch {branch}
Verdict: {verdict}, {total} findings, {applied} applied.

## Residual Findings
- **{severity}** — {file:line} — {description}
  Resolution: {why not applied | filed issue URL}
```

Write to `docs/residual-review-findings/{branch}.md`. A residual finding without a resolution note is a TODO, not a residual. The next review run reads this file to see what was previously deferred.
