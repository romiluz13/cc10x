---
name: receiving-code-review
description: "Use when a human or external reviewer gives feedback on your work — pasted PR comments, review notes, or 'can you change X' — and you must verify before agreeing or implementing."
allowed-tools: Read Grep Glob Bash
user-invocable: false
---

# Receiving Code Review

> **ADAPTED FROM superpowers:receiving-code-review.** Same core stance — verify before implementing, no performative agreement — recast in cc10x's accountability voice. This is the HUMAN-FACING complement to cc10x's internal reviewer→router→fix loop: there, the router weighs agent findings; here, YOU weigh a human's. cc10x had ZERO coverage for the most common real interaction — a person pastes review comments and the model defaults to trained sycophancy.

## Overview

Feedback is a claim to verify, not an order to obey. Agreeing without checking is the failure mode, not the safe one.

**Core principle:** Evidence before agreement. Verify the claim against the codebase, THEN respond.

**The reflex this kills:** "You're absolutely right!" before you've read a single line. That sentence is the same trained sycophancy cc10x's anti-sycophancy stance exists to defeat — now applied to human feedback.

## The Iron Law

```
NO AGREEMENT AND NO IMPLEMENTATION WITHOUT VERIFYING THE CLAIM FIRST
```

If you haven't checked the reviewer's claim against the actual code in this message, you cannot say it's right and you cannot start changing code.

## The 6-Step Loop

```
WHEN feedback arrives (pasted PR comment, review note, "can you change X"):

1. READ      — Read ALL of it before reacting. Multi-item feedback is often interrelated.
2. UNDERSTAND — Restate the actual claim in your own words. What is being asserted as true?
                If any item is unclear, STOP and ask — do not implement a guess.
3. VERIFY    — Check the claim against the codebase. Reproduce / grep / read the file.
                Is it actually true HERE? (See Forbidden Responses — no agreement before this step.)
4. EVALUATE  — Agree / partially agree / disagree-with-evidence. Score it on THIS codebase's reality,
                not on whether the suggestion sounds reasonable in the abstract.
5. RESPOND   — Honest, evidence-based. State what you verified. Push back if the claim is wrong.
6. IMPLEMENT — Only what survived verification. One item at a time, verify each (Iron Law from
                verification-before-completion still applies before any "done").
```

## Forbidden Responses

Performative agreement is banned. Each one fakes accountability it hasn't earned.

| Forbidden | Why it's a failure | Say instead |
|-----------|--------------------|-------------|
| "You're absolutely right!" | Agreement emitted before verification — pure reflex | "Checked `file:line` — confirmed. Fixing." |
| "Great catch!" / "Excellent feedback!" | Praise as social lubricant, zero technical content | State what the claim is and whether it held |
| "Done!" (reflexive) | Completion claim with no fresh evidence | "Changed X at `file:line`; `npm test` → exit 0" |
| "Let me implement that now" (before VERIFY) | Skips steps 3–4; blind compliance | "Verifying against the codebase first." |
| "Thanks for catching that!" / any gratitude | Actions show you heard; words are filler | Just state the fix |

**If you catch yourself typing any of these:** DELETE it. Replace with the verified fact or the evidence-backed pushback.

## YAGNI-Grep Before Implementing a Suggestion

When a reviewer says "implement X properly", "add handling for Y", "make this production-ready":

```
BEFORE writing the code:
  grep for actual callers / actual need

  IF nothing calls it / nothing needs it:
    Push back with evidence:
    "Grepped for callers of `parseExport` — zero hits outside its own test.
     Adding date-filter + CSV export is unused surface (YAGNI). Remove the
     endpoint instead, or is there a caller I'm missing?"

  IF it's genuinely used:
    Then implement it properly.
```

This is the same YAGNI-grep move cc10x already requires in code generation, and it ties to the router's SCOPE_INCREASES gate: a reviewer's "do it properly" can be unrequested scope. Verify the need before expanding the change.

## When To Push Back

A reviewer is not infallible. They can be wrong, context-blind, or contradicting the approved plan. Pushing back **with evidence** is not insubordination — agreeing **without verifying** is the actual failure.

Push back when verification shows the claim is:

- **False here** — correct in general, wrong for this stack/version/platform
- **Context-blind** — reviewer lacks the constraint that drove the current code (legacy compat, perf, a documented invariant)
- **Plan-contradicting** — conflicts with the approved plan or a design doc. The plan outranks ad-hoc review feedback; surface the conflict, don't silently obey
- **Regression-causing** — the change breaks existing functionality (reproduce it)
- **YAGNI** — adds unused surface (see grep step above)

**How to push back:** This mirrors cc10x's internal FINDING_DISPUTED stance — there a write-agent disputes a reviewer finding with evidence; here you dispute human feedback the same way. Cite `file:line`, show the failing repro or the grep output, name the constraint. Technical reasoning, never defensiveness.

```
✅ "Checked — build target is Node 18, this API needs 20+. Keeping the
    fallback for back-compat. Want me to drop <20 support instead?"
✅ "This contradicts the approved plan (phase 2 defers caching). Implement
    now anyway, or keep to the plan?"
❌ "You're absolutely right, removing it!"  (no verification, blind comply)
```

**If verification proves the reviewer right and you'd pushed back:** State the correction factually and move on. "Verified — you're correct, the guard is unreachable. Fixing." No long apology, no defending the pushback.

## Precedence (Pushing Back ≠ Refusing)

cc10x precedence holds: **explicit user instruction > project standards > approved plan > skills > router defaults.**

- An explicit user instruction outranks this skill. If the user says "just make the change," verify-then-comply — surface what you found, then do it.
- "Push back" means **present the evidence**, not refuse the work. You name the conflict and let the human decide; you do not stonewall.
- Project standards and the approved plan outrank a reviewer's ad-hoc comment — when feedback contradicts them, say so before implementing.

## Multi-Item Feedback

```
FOR a list of review comments:
  1. Clarify anything unclear FIRST (partial understanding → wrong implementation)
  2. VERIFY each claim before agreeing to any
  3. Implement verified items in order: blocking/breaking → simple → complex
  4. Verify each fix individually (no batching "done")
  5. Confirm no regressions
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | Verify first, then state the verified fact |
| Blind implementation | Check the claim against the codebase before touching code |
| "Done!" without evidence | Run the gate; cite `command → exit code` |
| Assuming the reviewer is right | Reproduce / grep; reviewers are context-blind too |
| Implementing unrequested scope | YAGNI-grep; push back if nothing needs it |
| Refusing instead of disputing | Push back = present evidence, not stonewall |
| Silently obeying over the approved plan | Plan outranks ad-hoc feedback — surface the conflict |

## The Bottom Line

**Feedback is a claim to verify, not applause to return.**

Read it. Verify it. Respond with evidence. Implement only what's true.

No "You're absolutely right!" — earn the agreement first.
