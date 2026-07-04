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

When `code-reviewer` and `silent-failure-hunter` run in parallel (BUILD workflow):

- **code-reviewer** (Assessment A): correctness, performance, spec compliance. Forms opinion WITHOUT seeing the hunter's scan.
- **silent-failure-hunter** (Assessment B): silent failure scan using red-flags table. Does NOT see the reviewer's findings.
- **Router-owned merge:** after both complete, the router writes a merged findings summary into the workflow artifact before verifier handoff. Where both agree → high confidence. Where the hunter caught what the reviewer missed → keep. Where the hunter finding is a false positive → drop with reason. Contradictory verdicts: stricter verdict wins, logged in `status_history`.

### Zero-Finding Halt

Zero findings on a non-trivial change → insufficient depth, not perfect code. Re-scan against heuristics and security checklist before reporting CLEAN.

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
