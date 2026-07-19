---
name: planning
description: |
  Planning discipline for creating execution plans and decision RFCs. Covers task
  decomposition, context references, validation levels, risk-based testing, ADR format,
  plan completeness gate, and functionality flow mapping. Loaded by planner agent.
allowed-tools: Read Write Edit Grep Glob LSP
user-invocable: false
---

# Planning

Distill plans into durable, buildable artifacts. A plan is a contract, not a brainstorm.

## Reference Files

- `references/live-verification-strategy.md` — when and how to plan live/production verification; load when the request calls for production-like confidence (real integrations, deployment, live data) or any task's validation level is Live

## Bite-Sized Task Granularity

Each task must be completable in one focused session (30-90 minutes). If a task takes longer, split it. Signs a task is too big: "and then...", multiple unrelated files, multiple test scenarios, more than 3 sub-steps.

**Test per task:** Every task must have at least one test that verifies its completion. If you can't name the test, the task isn't specific enough.

## Plan Document Header

```markdown
# [Feature Name] Plan

## Metadata
- Created: [date]
- Status: [draft|approved|in-progress|complete]
- Verification Rigor: [standard|critical_path]
- Plan Mode: [direct|execution_plan|decision_rfc]

## Agreement Snapshot
- **Goal:** [one sentence]
- **Constraints:** [list]
- **In Scope:** [list]
- **Out of Scope:** [list]
- **Open Decisions:** [list or "none"]
```

## Task Structure

Each task in the plan:

```markdown
### Task N: [Component Name]
**Objective:** [what this task achieves]
**Files/Surfaces:** [exact files to create/modify]
**Dependencies:** [previous task IDs or "none"]
**Allowed Scope:** [what's in bounds]
**Out-of-Scope Drift:** [what would be scope creep]
**Expected Artifacts:** [what this produces]
**Required Checks:** [tests/verification needed]
**Checkpoint Type:** [none|human_verify|decision|human_action]
**Exit Criteria:** [how to know this task is done]

**Consumes:** [exact signatures used from earlier phases — verbatim]
**Produces:** [exact names later phases rely on — verbatim]
```

If no Consumes/Produces: write `Consumes: none` / `Produces: none` explicitly.

## Context References Section (MUST READ before planning)

List files the builder MUST read before starting:

- **Patterns to follow:** existing components/modules that demonstrate the project's conventions
- **Configuration files:** tsconfig, package.json, .eslintrc, etc.
- **Related documentation:** API docs, architecture docs, existing ADRs
- **Compounded knowledge:** if `docs/solutions/` exists, check it for prior write-ups on the same problem category before designing from scratch — a past debugging/architecture lesson may already explain the constraint you're about to rediscover

**Distillation Rule:** Reference files by path with a one-line reason. Do not paste contents. The next agent reads the file, not your summary of it.

**Durability-Horizon Rule:** For each piece of the plan, state how long it's expected to last: "session-only" (throwaway), "sprint" (refactor likely), "stable" (architectural). This determines how much effort to spend on abstraction.

## Validation Levels

The canonical Validation Levels table (Deterministic / Probabilistic / Manual / **Live**) is defined once in `cc10x:verification` under `## Validation Levels` — do not restate it here.

Planner-specific mapping: every task must state its validation level. If manual, state the checklist. If deterministic, state the command. If probabilistic, state the flake rate and retry policy. If live, state the harness command and add a `### Live Verification Strategy` section (see `references/live-verification-strategy.md`).

## Plan Completeness Gate (MANDATORY — before save)

Scan the plan against these 10 checks. Fix inline.

1. Every task has a test that verifies completion
2. Every task lists exact file paths (not "the auth module" — `src/auth/handler.ts`)
3. Every task has exit criteria (not "done" — "test passes, build succeeds, type-check clean")
4. Dependencies are explicit (task IDs, not "after the API stuff")
5. Scope drift is named (what would pull this task off-track)
6. Consumes/Produces are verbatim-matched across phases (no spelling drift)
7. Validation level is stated for every task
8. Risk-based testing matrix is complete (see below)
9. No placeholders/TBD — every section holds a real decision
10. Open decisions are listed (not hidden in prose)

## Risk-Based Testing Matrix

| Risk | Probability | Impact | Test Required |
|------|------------|--------|---------------|
| [what could go wrong] | [low/med/high] | [low/med/high] | [test name or "manual: checklist"] |

Score = Probability × Impact. High-score risks need deterministic tests. Low-score risks can use manual validation.

## Test-Seam Selection Discipline

Choose the seam where the test attaches:

- **Unit seam:** pure function, no dependencies — fastest, most stable
- **Integration seam:** module boundary, real dependencies for adjacent layers — catches wiring
- **E2E seam:** user flow, all real dependencies — catches interaction bugs

Prefer the highest seam that still covers the risk. A unit test that doesn't exercise the real code path is a shallow test. An E2E test for a pure function is overkill.

**Prefer existing seams to new ones.** The fewer seams across the codebase, the better — the ideal number is one. If new seams are needed, propose them at the highest point you can.

**Record proposed seams in each phase.** Each phase's plan carries a `### Test Seams` line naming the seam(s) that phase will test at. These feed the builder's **enforced** seam gate (`TEST_SEAMS` + `SEAM_GATE_STATUS`, validated fail-closed per `build_scope`). Planned seams are the starting contract, not a suggestion — the builder must confirm or formally disagree; see `cc10x:building`.

## Wide-Refactor Phasing

A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**:

1. **Expand** — add the new form beside the old so nothing breaks. One phase.
2. **Migrate** — move call sites to the new form in batches sized by blast radius (per package, per directory). Each batch is its own phase, blocked by the expand, keeping CI green batch to batch because the old form still exists.
3. **Contract** — delete the old form once no caller remains. One phase, blocked by every migrate batch.

When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify phase — green is promised only there.

## Functionality Flow Mapping

Map each user flow to test paths:

```
Flow: [user flow name]
1. [step 1] → test: [test name]
2. [step 2] → test: [test name]
3. [step 3] → test: [test name]
Error paths:
- [error case] → test: [test name]
```

Every flow step and every error path must have a test. Unmapped steps are untested steps.

## Architecture Decision Records (ADR)

For decisions with material trade-offs (library choice, architecture pattern, data model):

```markdown
### ADR: [Decision Title]
**Context:** [why this decision is needed]
**Decision:** [what was chosen]
**Rejected Alternatives:** [what was not chosen and why]
**Consequences:** [what this decision enables and prevents]
```

Record ADRs inline in the plan. They are durable — the next session inherits them.

## Prefactor Question (Advisory)

Before adding an abstraction: "Will this abstraction be used by >1 caller within the next 3 sprints?" If no, inline it. Abstractions without multiple callers are premature.
