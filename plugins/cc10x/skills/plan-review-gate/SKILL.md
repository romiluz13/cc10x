---
name: plan-review-gate
description: "Adversarial plan review gate — spawns 3 independent reviewers (Feasibility, Completeness, Scope) in parallel. All must PASS before plan reaches user. Max 3 iterations then escalate."
allowed-tools: Read, Bash, Grep, Glob, Task, AskUserQuestion
---

# Plan Review Gate

**Core principle:** No plan reaches the user without surviving 3 independent adversarial checks.

## When to Run

**Run when plan has:** 2+ work units OR touches 3+ files OR involves architecture decisions.

**Skip when plan is trivial:** Single-file fix, copy edit, config tweak with <3 changes → present plan directly.

## The 3 Reviewers

Each reviewer is a fresh `Task()` instance with read-only access. Binary verdict: PASS or FAIL.

| Reviewer | Focus | Blocking Criteria |
|----------|-------|-------------------|
| Feasibility | Can this be executed? | Fabricated file paths; circular deps; incompatible patterns |
| Completeness | Does it cover the full request? | Missing requirement; no verification step; missing cross-file integration |
| Scope & Alignment | Is it right-sized? | Scope creep; under-scoping; diverges from user request |

## Workflow

```text
1. Plan drafted by planner
2. Skip gate if plan is trivial (see When to Run)
3. Spawn 3 reviewers in PARALLEL (fresh Task() instances)
4. Collect verdicts
4a. If any reviewer output does not contain PASS or FAIL as its verdict (e.g., partial output, timeout, error): treat as FAIL. Include the raw output as the blocking issue evidence.
5. IF all PASS → present plan to user with gate summary
6. IF any FAIL:
   a. Planner reads ALL feedback
   b. Planner revises plan OR rebuts with evidence
   c. Spawn 3 NEW reviewer instances (never reuse — prevents anchoring)
   d. Increment iteration counter
7. After 3 iterations without consensus → escalate to user (show remaining issues)
```

## Reviewer Prompts

### Feasibility Reviewer

```
You are the FEASIBILITY REVIEWER for a plan review gate.
Mode: Adversarial — find failures, not approve.

User Request: {user_request}
Plan: {plan_text}

Check each of these. Cite file:line or glob results as evidence:
1. File paths exist — Use glob/grep to verify every referenced file path. Fabricated = BLOCKING FAIL.
2. Dependency ordering — No circular deps; work units don't reference things from later steps.
3. Technical approach — Patterns/libraries match actual codebase. Read existing code to verify.
4. No unstated assumptions — Plan doesn't silently depend on services or infra that doesn't exist.

Rules:
- Any BLOCKING issue = overall FAIL.
- No suggestions. Only PASS or FAIL with evidence.
- Evidence required for both PASS and FAIL verdicts.

Output format:
## Feasibility — [PASS/FAIL]
### Evidence
- [finding]: [file:line or specific gap]
### Verdict
[PASS: All criteria met] OR [FAIL: {numbered blocking issues with evidence}]
```

### Completeness Reviewer

```
You are the COMPLETENESS REVIEWER for a plan review gate.
Mode: Adversarial — find gaps, not approve.

User Request: {user_request}
Plan: {plan_text}

Check each of these:
1. All requirements mapped — Every user requirement maps to a plan item. Missing = BLOCKING FAIL.
2. Verification steps — Each change has a way to verify it worked. Missing = BLOCKING FAIL.
3. Edge cases — Error scenarios, empty states, boundary conditions addressed.
4. Cross-file integration — Files that import/depend on changed files are accounted for.

Rules:
- Any BLOCKING issue = overall FAIL.
- No suggestions. Only PASS or FAIL with evidence.

Output format:
## Completeness — [PASS/FAIL]
### Evidence
- [finding]: [specific requirement or plan item reference]
### Verdict
[PASS: All requirements mapped] OR [FAIL: {numbered blocking issues}]
```

### Scope & Alignment Reviewer

```
You are the SCOPE & ALIGNMENT REVIEWER for a plan review gate.
Mode: Adversarial — find misalignment, not approve.

User Request: {user_request}
Plan: {plan_text}

Check each of these:
1. Matches user request — Plan solves what was asked. Divergence = BLOCKING FAIL.
2. No scope creep — No features/abstractions/refactoring beyond the request. Extras = BLOCKING FAIL.
3. No under-scoping — Obvious implications of the request not omitted.
4. Complexity proportional — Solution complexity matches problem complexity.

Rules:
- Any BLOCKING issue = overall FAIL.
- No suggestions. Only PASS or FAIL with evidence.

Output format:
## Scope & Alignment — [PASS/FAIL]
### Evidence
- [finding]: [request quote vs plan quote]
### Verdict
[PASS: Plan matches request] OR [FAIL: {numbered blocking issues}]
```

## Gate Output

### All PASS

```markdown
## Plan Review Gate — APPROVED (iteration N of 3)

| Reviewer | Verdict | Key Finding |
|----------|---------|-------------|
| Feasibility | PASS | All file paths verified, deps ordered |
| Completeness | PASS | All requirements mapped |
| Scope & Alignment | PASS | Plan matches request, no scope creep |

Plan is ready for user review.
```

### Any FAIL

```markdown
## Plan Review Gate — REVISION NEEDED (iteration N of 3)

| Reviewer | Verdict | Blocking Issues |
|----------|---------|-----------------|
| Feasibility | PASS | — |
| Completeness | FAIL | [N] blocking issues |
| Scope & Alignment | FAIL | [N] blocking issues |

### Blocking Issues (MUST ADDRESS)
[List each blocker with evidence]

Iteration: N of 3. Planner must address all blocking issues and resubmit.
```

### Escalation (3/3 iterations exhausted)

```markdown
## Plan Review Gate — ESCALATION REQUIRED (3/3 iterations exhausted)

### Remaining Blocking Issues
[List by reviewer]

### Options
1. Override — Proceed with plan (remaining issues become known risks)
2. Revise — Continue iterating manually
3. Simplify — Reduce scope to eliminate contentious items
4. Cancel — Abandon and start fresh

Please choose an option.
```

## Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|--------------|-----------|-----|
| Reusing reviewer instances | Anchoring bias | Always spawn fresh Task() |
| Cross-reviewer contamination | Destroys independence | Each reviewer sees only: plan + request |
| FAIL as advisory | Undermines gate | FAIL = revise and re-review |
| Skipping for "simple" plans | Simplicity is what the gate validates | Run if 2+ units or 3+ files |
| Planner self-reviewing | Confirmation bias | Reviewers must be separate Task() instances |
| >3 iterations | Diminishing returns | Max 3, then escalate |
