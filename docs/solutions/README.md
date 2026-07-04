# Solutions — Compounded Knowledge

This directory holds durable, cross-project learnings — the output of cc10x's
Knowledge Compounding Loop (see `cc10x:memory-and-handoff` skill, §Knowledge
Compounding Loop).

## What goes here

A solution doc is written automatically during Memory Finalization (router §13)
when a BUILD or DEBUG workflow crosses one of these thresholds:

- The problem took 3+ hypotheses to solve (tracked via `[DEBUG-N]:` entries)
- The defect pattern was found in 3+ files (blast-radius scan)
- The winning fix contradicted a documented assumption in `patterns.md`

Mechanical fixes (typos, import errors, one-line changes) never generate a
solution doc — they stay in session memory (`activeContext.md`) only.

## Format

```markdown
# [Problem Title]
Category: [debugging | architecture | testing | workflow | conventions]
Tags: [comma-separated]
Date: YYYY-MM-DD

## Problem
[What went wrong — symptoms, not just the error message]

## What Didn't Work
[Hypotheses that failed and why]

## Solution
[What actually worked — with code example if applicable]

## Why
[Why the solution works — the underlying principle]

## Prevention
[How to prevent this class of problem in the future]
```

## Directory structure

```
docs/solutions/
  debugging/
  architecture/
  testing/
  workflow/
  conventions/
```

## Maintenance

Periodically audit these docs: Keep / Update / Consolidate / Replace / Delete
(same five-outcome model as memory consolidation in `cc10x:memory-and-handoff`).
Delete docs whose lesson is now enforced structurally elsewhere (a hook, a
contract field) — a solution doc that's been superseded by a hard gate is
noise, not signal.
