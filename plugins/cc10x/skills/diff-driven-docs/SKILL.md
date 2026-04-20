---
name: diff-driven-docs
description: >-
  Use when a BUILD phase completes, a commit is staged, or a PR is about to
  be created, and the diff has not yet been reflected in documentation.
  Also use when the user says "update docs", "sync docs", "document this",
  or asks whether documentation is up to date.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
skills:
  - cc10x:verification-before-completion
---

# diff-driven-docs

## Overview

Stale documentation is worse than no documentation — it actively misleads contributors, users, and future maintainers. diff-driven-docs treats documentation as a first-class deliverable of every BUILD phase, not an afterthought. Just as test-driven-development enforces that tests must be produced as part of the code-change cycle, diff-driven-docs enforces that doc updates must accompany code changes before the workflow closes. The doc-syncer agent analyzes the actual diff, classifies documentation impact across three layers (business, technical, audit), and writes only the updates that are genuinely needed — skipping trivially low-impact changes fast.

## Impact Classifier

Run this classifier before any doc work. Use it to determine which layers to evaluate and which to skip.

| Diff Characteristic | Business Layer | Technical Layer | Audit Layer |
|---------------------|---------------|----------------|-------------|
| Internal utility, helper, or type change only | SKIP | CHECK | SKIP |
| Test addition with no new pattern | SKIP | SKIP | SKIP |
| Style / formatting change | SKIP | SKIP | SKIP |
| Dependency version bump (no API change) | SKIP | SKIP | SKIP |
| Routine bug fix (existing behavior corrected) | SKIP | CHECK | SKIP |
| Simple refactor (behavior unchanged) | SKIP | CHECK if signatures changed | SKIP |
| New exported function / hook / component | SKIP | CHECK | CHECK |
| New page or route | CHECK | CHECK | CHECK |
| Architectural pattern introduced | SKIP | CHECK | CREATE |
| Technology choice made | SKIP | CHECK | CREATE |
| Breaking change to public API | CHECK | CHECK | CREATE |
| Permission or role change | CHECK | CHECK | CHECK |
| Security or compliance impact | CHECK | CHECK | CREATE or UPDATE |

**SKIP business docs if:** no user-facing surface changed; only internal utils, types, or tests were modified.

**SKIP audit docs if:** the diff is a routine bug fix, style change, test addition, or simple refactor with no new pattern.

**ALWAYS check technical docs** when hooks, components, migrations, schema, routes, or exported library APIs changed.

**CREATE an audit doc if:** an architectural decision was made, a new pattern was introduced, a non-obvious tradeoff was accepted, or a team member six months from now would ask "why did we do it this way?"

If all three layers are SKIP, set `IMPACT_LEVEL: none` and emit a SKIPPED contract immediately without opening any doc files.

## The Three Layers

### Business Layer

User-facing guides, admin documentation, and feature descriptions. Business docs describe what users and administrators can do — not how the system works internally.

- Scope: user guides, admin guides, settings references, feature descriptions, permissions documentation
- Update trigger: new or changed user-facing behavior, new page or route, permission change, config option that affects user behavior
- What to write: describe the feature from the user's perspective; do not expose internal implementation details

### Technical Layer

Hooks reference, components catalog, schema documentation, architecture notes, and JSDoc on exported APIs. Technical docs describe how the system is built — for developers working on the codebase.

- Scope: hooks reference, components catalog, API reference, edge function reference, database schema docs, environment variable docs, architecture notes
- Update trigger: any exported function, hook, or component whose signature was added or changed; any migration or schema change; any new route or page
- What to write: name, file path, description, signature, params, return value, key behaviors; for React components, JSDoc on the Props interface is sufficient

### Audit Layer

Decision records capturing what changed, why, alternatives considered, and impact. Audit docs are written for future contributors who need to understand the reasoning behind a decision.

- Scope: docs/decisions/ (or project equivalent), compliance notes, migration guides for breaking changes
- Update trigger: new architectural pattern, technology choice, non-obvious tradeoff, breaking change, security or compliance impact
- What to write: structured record following the four-section format below

## Audit Doc Guidance

### When to Create vs. Update vs. Skip

**CREATE new when:**
- A pattern is introduced for the first time in this codebase
- An architectural decision is made that future contributors will need to understand
- A non-obvious tradeoff is accepted (performance vs. correctness, simplicity vs. extensibility)
- A technology is chosen over alternatives

**UPDATE existing when:**
- An existing decision is amended or reversed
- A previous tradeoff is resolved differently in a new context
- Additional impact or context is discovered for a prior decision

**SKIP when:**
- Routine bug fix (correcting behavior to match existing intent)
- Test addition with no new pattern
- Style or formatting change
- Dependency version bump with no API change

### Filename Pattern

`docs/YYYY-MM-DD-{topic}-decision.md` — adapt to the project's actual convention (e.g., `docs/decisions/`, `docs/adr/`).

### Audit Doc Structure

```markdown
## What Changed
[One paragraph describing the technical change]

## Why
[The primary reason for this decision]

## Alternatives Considered
- **{Alternative A}:** [Why it was not chosen]
- **{Alternative B}:** [Why it was not chosen]

## Impact
[Who is affected; any migration steps; ongoing maintenance implications]
```

## Workflow

The doc-syncer agent follows these five steps in order:

**Step 1 — Get the diff**

```bash
# For pre-commit (staged changes)
git diff --cached --stat && git diff --cached

# For post-build (last commit)
git diff HEAD~1 --stat && git diff HEAD~1
```

Read the full diff output before classifying.

**Step 2 — Classify impact**

Run the Impact Classifier table against the diff. Determine `IMPACT_LEVEL` (none / low / medium / high) and which layers to evaluate. If `IMPACT_LEVEL` is `none`, emit the SKIPPED contract immediately and stop.

**Step 3 — Map changed files to doc targets**

Use the project's `## Doc Targets` from `CLAUDE.md` if present. Otherwise apply the generic heuristics in `references/doc-target-heuristics.md`. For each changed file, identify zero or more target documentation files.

**Step 4 — Read then write**

For each doc target:
1. `Read` the entire target file first
2. Apply minimal, targeted edits using `Edit` — do not rewrite sections that are not affected by the diff
3. `Read` the file again after writing to verify the edit landed correctly

For audit docs: check whether an existing decision doc covers this topic. If yes, update it. If no, create a new file following the filename pattern.

**Step 5 — Self-review**

Before emitting the contract, verify:
- Every updated doc accurately reflects the diff (no hallucinated details)
- Cross-references between docs are consistent
- If a new doc file was created, it is indexed in the relevant `## Docs` section of `CLAUDE.md`
- No doc content was duplicated in `CLAUDE.md` (it is an index only)

## Router Integration

This skill is loaded by the `doc-syncer` agent in the BUILD chain. The router spawns `doc-syncer` after `integration-verifier` passes and before the Memory Update task. The agent emits a `### Router Contract (MACHINE-READABLE)` YAML block that the router validates before advancing.

**Opt-out:** Add `DIFF_DRIVEN_DOCS: skip` to the `## Session Settings` section of `CLAUDE.md` to disable the doc-syncer for projects that manage documentation separately.

## Rationalization Table

| Common excuse | Counter |
|---------------|---------|
| "docs can wait" | Docs are a deliverable, not a follow-up. The workflow does not close until they are done. |
| "it's just a refactor" | If file paths, function signatures, or exported APIs changed, technical docs need updating. |
| "the diff is small" | Run the Impact Classifier. Small diffs still trigger technical doc updates when signatures change. |
| "nobody reads those docs" | Stale docs actively mislead. Empty docs are better than wrong ones. |
| "I'll add JSDoc later" | JSDoc on exported APIs is a technical doc update. Later means never. |
| "the tests document the behavior" | Tests document correctness, not usage. They are not a substitute for doc updates. |
