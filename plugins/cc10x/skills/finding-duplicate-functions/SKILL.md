---
name: finding-duplicate-functions
description: "Use when auditing a codebase for semantic duplication — functions that do the same thing under different names — especially in LLM-grown code where reuse was skipped."
allowed-tools: Read Grep Glob Bash
user-invocable: false
---

# Finding Duplicate Functions

## Overview

LLM-generated codebases accumulate **semantic** duplicates: functions that serve the same purpose but were implemented independently, under different names, in different files. Classical copy-paste detectors (jscpd and friends) catch **syntactic** duplicates — identical token runs — but they are blind to "same intent, different implementation." That is the gap this audit closes.

**Core principle:** Syntactic detection is cheap and already handled by tooling. Semantic detection requires reading for intent, and intent comparison is where the value — and the model cost — lives.

This skill is loadable by the **code-reviewer** as a focused reuse pass, or runnable standalone as a consolidation audit. Either way it emits reuse-consolidation findings through the reviewer's existing finding contract (confidence-scored, `file:line`-cited, fix-bearing) — it does not invent a new output format.

## When To Use

- Codebase grown organically across many contributors (human or LLM).
- You suspect utility functions were reimplemented instead of reused.
- Before a major refactor, to consolidate first and refactor once.
- After jscpd (or equivalent) has already cleaned up syntactic dupes — this is the second pass that finds what jscpd can't see.

## Two-Phase Method

Classical extraction first, then intent clustering. The split matters because it lets the cheap tier do the bulk filtering and reserves the capable tier for the one judgment it alone can make.

### Phase 1 — Extract the function catalog

Use `Grep`/`Glob` to enumerate **exported** functions across the target surface. Capture name, file, line, and signature.

- Glob the source tree for the relevant extensions, then Grep for export/definition patterns (`export function`, `export const … =>`, `def `, `public … (`, etc. — match the language).
- Record each hit as `name | file:line | signature`. This catalog is the unit of analysis.

### Phase 2a — Categorize by domain (cheap tier)

Group the catalog into domains: validation, formatting, path manipulation, HTTP/response shaping, date handling, etc. This is mechanical bucketing — route it to the router's **cheap** model tier. It exists only to shrink the comparison space; getting a bucket slightly wrong costs nothing because Phase 2b re-reads within the bucket.

### Phase 2b — Split into worthwhile categories

Only categories with **3+ functions** are worth comparing. A category of 1–2 cannot hide a meaningful duplication pattern; drop it. Comparing the full catalog instead of per-category buckets produces noise, not findings.

### Phase 2c — Detect duplicates per category (capable tier)

Within each surviving category, read the implementations and decide which functions share intent. **This step requires the router's `capable` tier — never the cheap tier.** The cheap tier misses subtle semantic dupes (it anchors on names and surface shape and rubber-stamps "these look different"); the whole point of the audit is the comparison the cheap tier cannot make. This mirrors the router's reviewer FLOOR: a gating judgment never runs on the cheapest model.

### Phase 3 — Emit prioritized findings

Group findings by confidence, highest first, and route each through the code-reviewer finding contract:

```markdown
### Reuse / Consolidation
- [90] `formatErr()` at `src/utils/errors.ts:12` duplicates `toErrorString()` at `src/lib/format.ts:88` — same intent (Error → display string), divergent impls
  → Fix: keep `toErrorString` (has tests at `test/format.test.ts`), repoint 4 callers, delete `formatErr`
  → Evidence: both stringify `err.message` + `err.stack`; `formatErr` callers at `src/api/{users,posts}.ts`
```

Every finding states what is duplicated, why it matters, the fix, and `file:line` evidence — same bar as any other reviewer finding. A duplicate claim without evidence is not reported.

## High-Risk Zones

Concentrate the audit here — this is where independent reimplementation clusters:

| Zone | Why it duplicates |
|------|-------------------|
| `utils/`, `helpers/`, `lib/` | Catch-all dumping grounds; nobody checks what's already there |
| Validation code | "Is this a valid email/id/url" gets rewritten per feature |
| Error formatting | Every module invents its own `Error → string` |
| Path manipulation | Join/normalize/relativize reimplemented around platform quirks |
| String formatting | Truncate, slugify, titlecase, pad — re-rolled constantly |
| Date formatting | Parse/format/diff scattered, each slightly different |
| API response shaping | Envelope/pagination/error-body builders copied per endpoint |

## Common Mistakes

| Mistake | Why it hurts | Do instead |
|---------|--------------|-----------|
| Extracting too much | Internal helpers flood the catalog with noise | Focus on **exported** functions — they're the reusable surface |
| Skipping categorization | Full-catalog comparison drowns real dupes in noise | Bucket by domain first, compare only within buckets of 3+ |
| Using the cheap tier for detection | Misses subtle semantic dupes; false "all clear" | Cheap tier categorizes; **capable** tier detects |
| Consolidating without tests | Deleting the wrong survivor breaks behavior silently | Confirm the survivor has tests before deleting anything |

## Consolidation Discipline (cc10x Verification Ethos)

Finding a duplicate is the cheap part. Removing one is a behavior change and gets cc10x's full verification bar. **Never delete a duplicate** until all three hold:

1. **Survivor has tests.** Pick the implementation with real coverage as the survivor. If neither has tests, write the test against the chosen survivor *first* — you cannot safely delete the other without a behavioral anchor.
2. **All callers updated.** Repoint every caller of the deleted function to the survivor. Use Grep to enumerate callers — missing one is a silent break.
3. **Re-run after consolidation.** Run the test suite (and a build/typecheck) after the merge. Green tests on the survivor are what license the deletion. A consolidation that isn't re-verified is not done.

This is the same discipline cc10x applies everywhere: a change isn't complete until it's been re-verified against reality, not assumed correct because it "looks equivalent."
