---
name: code-review-patterns
description: "Internal cc10x skill, loaded by the code-reviewer and code-reviewer (Pass 1b). Use when reviewing a diff for correctness, security, performance, and maintainability with evidence-backed, confidence-scored findings."
allowed-tools: Read Grep Glob LSP
user-invocable: false
---

# Code Review Patterns

## Overview

Code reviews catch bugs before they ship. But reviewing code quality before functionality is backwards.

**Core principle:** First verify it works, THEN verify it's good.

## Reference Files

Read only the references needed for the current review:

- `references/review-order-and-checkpoints.md` for concern-first reading order, review checkpoints, zero-finding halts, and re-review loops
- `references/security-review-checklist.md` for auth, input/output, secrets, network, storage, and dependency checks
- `references/code-review-heuristics.md` for maintainability, performance, hidden-failure, edge-case, sloppy-pattern, and UI quick scans

## Signal Quality Rule

**Flag ONLY when certain. False positives erode trust and waste remediation cycles.**

| Flag | Do NOT Flag |
| ------ | ------------- |
| Will fail to compile/parse (syntax, type, import errors) | Style preferences not in project guidelines |
| Logic error producing wrong results for all inputs | Potential issues dependent on specific inputs/state |
| Clear guideline violation (quote the exact rule) | Subjective improvements or nitpicks |

## Quick Review Checklist (Reference Pattern)

**For rapid reviews, check these 8 items:**

- [ ] Code is simple and readable
- [ ] Functions and variables are well-named
- [ ] No duplicated code
- [ ] Proper error handling
- [ ] No exposed secrets or API keys
- [ ] Input validation implemented
- [ ] Good test coverage
- [ ] Performance considerations addressed

## The Iron Law

```
NO CODE QUALITY REVIEW BEFORE SPEC COMPLIANCE
```

If you haven't verified the code meets requirements, you cannot review code quality.

## Two-Stage Review Process

### Stage 1: Spec Compliance Review

**Does it do what was asked?**

1. **Read the Requirements**
   - What was requested?
   - What are the acceptance criteria?
   - What are the edge cases?

2. **Trace the Implementation**
   - Does the code implement each requirement?
   - Are all edge cases handled?
   - Does it match the spec exactly?

3. **Test Functionality**
   - Run the tests
   - Manual test if needed
   - Verify outputs match expectations

**Gate:** Only proceed to Stage 2 if Stage 1 passes.

### Stage 2: Code Quality Review

**Is it well-written?**

Review in priority order:

1. **Security** - Vulnerabilities that could be exploited
2. **Correctness** - Logic errors, edge cases missed
3. **Performance** - Unnecessary slowness
4. **Maintainability** - Hard to understand or modify
5. **UX** - User experience issues (if UI involved)
6. **Accessibility** - A11y issues (if UI involved)

## Review Order

Before scanning code line-by-line, read
`references/review-order-and-checkpoints.md` and reconstruct the change by
concern, not by raw diff order.

## Security Review

For auth, data, network, storage, or externally reachable code, read
`references/security-review-checklist.md` before forming findings.

## LSP-Powered Code Analysis

**Use LSP for semantic understanding during reviews:**

| Task | LSP Tool | Why Better Than Grep |
| ------ | ---------- | --------------------- |
| Find all callers of a function | `lspCallHierarchy(incoming)` | Finds actual calls, not string matches |
| Find all usages of a type/variable | `lspFindReferences` | Semantic, not text-based |
| Navigate to definition | `lspGotoDefinition` | Jumps to actual definition |
| Understand what function calls | `lspCallHierarchy(outgoing)` | Maps call chain |

**Review Workflow with LSP:**

1. `localSearchCode` → find symbol + get lineHint
2. `lspGotoDefinition(lineHint=N)` → understand implementation
3. `lspFindReferences(lineHint=N)` → check all usages for consistency
4. `lspCallHierarchy(incoming)` → verify callers handle changes

**CRITICAL:** Always get lineHint from localSearchCode first. Never guess line numbers.

## Review Heuristics

For performance, maintainability, edge cases, hidden failures, type-design
drift, or UI-specific checks, read `references/code-review-heuristics.md`.

**Wrong/Right — Silent optional chaining:**

```typescript
// WRONG: silently swallows null user
const name = user?.profile?.name ?? 'Unknown';

// RIGHT: log the gap, then degrade
const name = user?.profile?.name;
if (!name) {
  logger.warn('user profile missing name', { userId: user?.id });
}
return name ?? 'Unknown';
```

## Edge Case Classification Taxonomy

Reference checklist for systematic edge case scanning during review:

| Category | Examples | Detection |
| ---------- | ---------- | ----------- |
| Missing else/default | Switch without default, if without else for nullable | Check switch/if exhaustiveness |
| Unguarded inputs | No validation on user input, missing null checks | Direct parameter use without validation |
| Off-by-one | Loop bounds, array indexing, pagination | Review all `<` vs `<=`, `array[length]` vs `array[length-1]` |
| Arithmetic edge cases | Division by zero, integer overflow, floating point | `/` operator without divisor validation |
| Implicit type coercion | `==` instead of `===`, string-to-number, truthy/falsy | `==` (not `===`), `+` with mixed types |
| Race conditions | Shared mutable state, async without locking | Shared variables modified in async paths |
| Timeout/retry gaps | No timeout on network calls, no retry exhaustion | fetch/axios without timeout config |

Use during Stage 2 Quality Review. Check only categories relevant to the changed code.

## Clarity Over Brevity

- Nested ternary `a ? b ? c : d : e` → Use if/else or switch
- Dense one-liner saving 2 lines → 3 clear lines over 1 clever line
- Chained `.map().filter().reduce()` with complex callbacks → Named intermediates

## Pattern Recognition Criteria

**During reviews, identify patterns worth documenting:**

| Criteria | What to Look For | Example |
| ---------- | ------------------ | --------- |
| **Tribal** | Knowledge new devs wouldn't know | "All API responses use envelope structure" |
| **Opinionated** | Specific choices that could differ | "We use snake_case for DB, camelCase for JS" |
| **Unusual** | Not standard framework patterns | "Custom retry logic with backoff" |
| **Consistent** | Repeated across multiple files | "All services have health check endpoint" |

**If you spot these during review:**

1. Note the pattern in review feedback
2. Include in your **Memory Notes (Patterns section)** - router will persist to patterns.md via Memory Update task
3. Flag inconsistencies from established patterns

## Severity Classification

| Severity | Definition | Action |
| ---------- | ------------ | -------- |
| **CRITICAL** | Security vulnerability or blocks functionality | Must fix before merge |
| **MAJOR** | Affects functionality or significant quality issue | Should fix before merge |
| **MINOR** | Style issues, small improvements | Can merge, fix later |
| **NIT** | Purely stylistic preferences | Optional |

## Multi-Signal Review Methodology

**Each Stage 2 pass produces an independent signal. Score each dimension separately.**

**HARD signals** (any failure blocks approval):

- **Security:** One real vulnerability = dimension score 0
- **Correctness:** One logic error producing wrong output = dimension score 0

**SOFT signals** (concerns noted, don't block alone):

- **Performance:** Scaling concern without immediate impact
- **Maintainability:** Complex but functional code
- **UX/A11y:** Missing states but core flow works

**Aggregation rule:**

1. If ANY HARD signal = 0 → STATUS: CHANGES_REQUESTED (non-negotiable)
2. The exact CONFIDENCE formula and severity vocabulary are owned by the code-reviewer agent contract — do not restate the math here (a second copy drifts). Apply the agent's `CONFIDENCE = min(HARD scores) capped by avg(SOFT scores) - 10`, with a single HARD:0 forcing CONFIDENCE:0.
3. Include per-signal breakdown in Router Handoff for targeted remediation

### Zero-Finding Halt

If a review produces ZERO findings across ALL dimensions (security, correctness, performance, maintainability, UX/A11y), the review MUST halt and re-examine. Zero findings in a non-trivial change is a signal of insufficient review depth, not perfect code. Action: Re-read every changed file. Re-run the heuristic scans in `references/code-review-heuristics.md`. Re-run the security triage in `references/security-review-checklist.md`. If still zero findings after deliberate re-examination, document: "Zero findings confirmed after forced re-examination of [N files, M lines changed]. Reviewed: [list specific checks performed]." A bare "no issues" without re-examination proof is INVALID.

**Evidence requirement per signal:**
Each signal MUST cite specific file:line. A signal without evidence = not reported.

## Two Isolated Assessments + WEAVE Reconciliation

cc10x runs the **code-reviewer** and the **code-reviewer (Pass 1b)** in parallel on purpose.

**Why independence is non-negotiable:** Collapsing both passes into ONE reasoning head silently ANCHORS them — the first concern read biases the second, the broad reviewer rationalizes away a hidden-failure smell, and the two "independent" signals quietly converge on one opinion. Independence is the entire point. Each pass must form its findings without seeing the other's. Reconcile only AFTER both have committed their lists.

**WEAVE protocol (replaces a bare "stricter verdict wins" merge):** Before routing any finding, classify it.

| Class | Definition | Routing |
| ------- | ------------ | --------- |
| **AGREED** | Both passes independently surfaced it (same file:line, same root cause) | Highest trust — report; convergence is strong signal |
| **DETECTOR-ONLY** | Caught by exactly one pass (reviewer XOR code-reviewer (Pass 1b)) | Keep it — a finding the other missed is the value of running two passes, NOT noise. Carry the detecting pass's evidence and severity as-is |
| **FALSE-POSITIVE** | Triage suspect: no file:line, pre-existing, linter-owned, or refuted by the other pass's evidence | Drop, per "Do NOT Flag" and the Signal Quality Rule |

Weave order: AGREED → DETECTOR-ONLY → FALSE-POSITIVE triage. Never let a DETECTOR-ONLY finding get demoted just because the other pass stayed silent — silence is not refutation.

**Fallback — stricter verdict wins:** If, AFTER weaving, the two passes hold a genuine contradiction on the SAME finding (e.g. reviewer says safe, hunter says swallowed failure, neither's evidence refutes the other), the stricter verdict wins. Tie goes to CHANGES_REQUESTED. This is the residual rule, not the first move — weave first, escalate only on a true standoff.

## Do NOT Flag (False Positive Prevention)

- Pre-existing issues not introduced by this change
- Correct code that merely looks suspicious
- Pedantic nitpicks a senior engineer would not flag
- Issues linters already catch (don't duplicate tooling)
- General quality concerns not required by project guidelines
- Issues explicitly silenced via lint-ignore comments

## Priority Output Format (Feedback Grouping)

**Organize feedback by priority (from reference pattern):**

```markdown
## Code Review Feedback

### Critical (must fix before merge)
- [95] SQL injection at `src/api/users.ts:45`
  → Fix: Use parameterized query `db.query('SELECT...', [userId])`

### Warnings (should fix)
- [85] N+1 query at `src/services/posts.ts:23`
  → Fix: Batch query with WHERE IN clause

### Suggestions (consider improving)
- [70] Function `calc()` could be renamed to `calculateTotal()`
  → More descriptive naming
```

**ALWAYS include specific examples of how to fix each issue.**
Don't just say "this is wrong" - show the correct approach.

## Red Flags - STOP and Re-review

If you find yourself:

- Reviewing code style before checking functionality
- Not running the tests
- Skipping the security checklist
- Giving generic feedback ("looks good")
- Not providing file:line citations
- Not explaining WHY something is wrong
- Not providing fix recommendations

**STOP. Start over with Stage 1.**

## Rationalization Prevention

| Excuse | Reality |
| -------- | --------- |
| "Tests pass so it's fine" | Tests can miss requirements. Check spec compliance. |
| "Code looks clean" | Clean code can still be wrong. Verify functionality. |
| "I trust this developer" | Trust but verify. Everyone makes mistakes. |
| "It's a small change" | Small changes cause big bugs. Review thoroughly. |
| "No time for full review" | Bugs take more time than reviews. Do it properly. |
| "Security is overkill" | One vulnerability can sink the company. Check it. |

## Optional: Anchored 0-4 Quality Rubric (High-Rigor Reviews)

The CONFIDENCE score measures *certainty in the findings*, not *quality of the result*. For high-rigor reviews, the reviewer MAY emit an anchored 0-4 quality score ALONGSIDE the verdict. Each integer is anchored to spelled-out criteria so two reviewers land on the same number:

| Score | Criteria |
| ------- | ---------- |
| **0** | Broken or unsafe. Fails spec, ships a HARD-signal defect (security hole, wrong output), or hides a failure. Do not merge |
| **1** | Works in the happy path but fragile. Real gaps in error handling, edge cases, or validation that will bite under normal use |
| **2** | Solid and correct, but unremarkable. Some maintainability or clarity debt; nothing that blocks merge |
| **3** | Good. Correct, readable, well-tested, edge cases considered. The bar for code you would happily own |
| **4** | Genuinely excellent. Correct AND clear AND defensively complete AND the design makes the next change easy. Rare |

**Total band → action:**

| Score | Action |
| ------- | -------- |
| 0 | CHANGES_REQUESTED — non-negotiable (mirrors HARD-signal:0) |
| 1 | CHANGES_REQUESTED — name the fragility precisely |
| 2 | APPROVE with noted follow-ups |
| 3-4 | APPROVE |

**Calibration:** Most real code scores mid-band (2). A 4 is genuinely excellent — do not inflate. If every review you write scores 3-4, your scale is broken, not the code.

This is **additive** — it does NOT replace the existing verdict/CONFIDENCE contract owned by the code-reviewer agent. Its value is giving the router a cleaner gate input than a binary APPROVE: a graded 0-4 lets the router distinguish "barely passing, watch this" (1-2) from "ship it" (3-4) and route remediation effort accordingly.

## Output Format

```markdown
## Code Review: [PR Title/Component]

### Stage 1: Spec Compliance ✅/❌

**Requirements:**
- [x] Requirement 1 - implemented at `file:line`
- [x] Requirement 2 - implemented at `file:line`
- [ ] Requirement 3 - NOT IMPLEMENTED

**Tests:** PASS (24/24)

**Verdict:** [Meets spec / Missing requirements]

---

### Stage 2: Code Quality

**Security:**
- [CRITICAL] Issue at `file:line` - Fix: [recommendation]
- No issues found ✅

**Performance:**
- [MAJOR] N+1 query at `file:line` - Fix: Use batch query
- No issues found ✅

**Quality:**
- [MINOR] Unclear naming at `file:line` - Suggestion: rename to X
- No issues found ✅

**UX/A11y:** (if UI code)
- [MAJOR] Missing loading state - Fix: Add spinner
- No issues found ✅

---

### Summary

**Decision:** Approve / Request Changes

**Critical:** [count]
**Major:** [count]
**Minor:** [count]

**Required fixes before merge:**
1. [Most important fix]
2. [Second fix]
```

## Review Loop Protocol

After requesting changes:

1. **Wait for fixes** - Developer addresses issues
2. **Re-review** - Check that fixes actually fix the issues
3. **Verify no regressions** - Run tests again
4. **Approve or request more changes** - Repeat if needed

**Never approve without verifying fixes work.**

## Partial Phase Reviews

When reviewing code from a single phase of a multi-phase plan:

| Scope question | Rule |
| ---------------- | ------ |
| Review only this phase's changes? | YES — do not expand scope to future phases |
| Flag problems in untouched code discovered during review? | Note for follow-up; do not block this phase |
| Verify phase exit criteria? | YES — the plan defines exit criteria per phase; verify those, not the final product |
| Review integration points with future phases? | Flag interface concerns only — do not require future-phase implementation |

**Key principle:** A partial-phase review succeeds when the phase exit criteria are met and no regressions exist. "Incomplete feature" is not a valid rejection reason if the plan has more phases.

## Final Check

Before approving:

- [ ] Stage 1 complete (spec compliance verified)
- [ ] Stage 2 complete (all checklists reviewed)
- [ ] All critical/major issues addressed
- [ ] Tests pass
- [ ] No regressions introduced
- [ ] Evidence captured for each claim
