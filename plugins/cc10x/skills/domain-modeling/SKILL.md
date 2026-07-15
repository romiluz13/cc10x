---
name: domain-modeling
description: |
  Actively build and sharpen a project's domain model — challenge terms against
  the glossary, sharpen fuzzy language, stress-test with edge-case scenarios,
  update CONTEXT.md inline, and offer ADRs sparingly. The active discipline
  loaded by language-shaping agents (planner, doc-syncer, exploration). Builders
  load a read-only/obey variant: they read CONTEXT.md and obey it, emitting a
  proposal on contradiction rather than resolving it. See the Active vs
  read-only section for which mode applies.
allowed-tools: Read Edit Write Glob Grep
user-invocable: false
---

<!-- Upstream: github.com/mattpocock/skills @ e9fcdf95b402d360f90f1db8d776d5dd450f9234
     Classification: ADAPTED (autonomous transform on human-gates; read-only builder
     variant added; cc10x frontmatter). Companions (CONTEXT-FORMAT.md, ADR-FORMAT.md)
     ported verbatim. -->

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## Active vs read-only

This skill loads in two modes depending on which agent invoked it:

- **ACTIVE** (planner, doc-syncer, exploration in DESIGN mode): you shape the domain model. You challenge terms, sharpen language, write `CONTEXT.md` inline, and offer ADRs. You are a designated CONTEXT.md writer.
- **READ-ONLY / OBEY** (component-builder, bug-investigator): you read `CONTEXT.md` and use the project's domain vocabulary in all output. You do NOT write or edit `CONTEXT.md`. If you discover a contradiction between the glossary and the code, **emit a proposal** in your Memory Notes (`**Domain proposal:** term X is defined as Y in CONTEXT.md but the code does Z — which is right?`) or block (`STATUS: FAIL`, `REMEDIATION_REASON: "Domain glossary contradicts code at term X"`) — do NOT resolve the contradiction yourself. Resolving domain language is the job of shaping phases, not build phases.

The agent's persona prompt determines which mode is in effect. If unsure, default to READ-ONLY — the cost of an opportunistic glossary rewrite during a build is higher than the cost of a deferred proposal.

## Autonomous transform (how human-gates route here)

Matt's original skill is human-gated ("ask the user", "challenge the user"). In cc10x's autonomous workflow, every gate routes through **evidence + blast radius**, not reversibility alone:

| Situation | Transform |
| --- | --- |
| The repo/spec/code already proves one interpretation, AND the choice has no external semantic impact | Proceed. Record the resolved term in `CONTEXT.md` inline. |
| No proof in repo, but low blast radius (no contracts, persistence, or user-language affected) | Proceed with the recommended interpretation, record it in `CONTEXT.md` with an explicit `**Assumed:**` note, and continue. |
| Domain ambiguity affecting contracts, persistence, or user language (e.g. "account" = Customer or User?) | **STOP.** Return `STATUS: NEEDS_CLARIFICATION` (planner) or emit the proposal and block (builder). Do NOT auto-answer. |
| A hard-to-reverse decision with no proof | **STOP.** Failure-stop. Offer the ADR only after the human decides. |

**Grilling is NOT auto-answered.** Auto-answering an interview removes its information source. In JUST_GO mode, the exploration interview asks questions, records the recommended answer + assumption, and proceeds ONLY for low-blast-radius decisions. Domain-shaping questions always stop for human input.

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session (ACTIVE mode)

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?" In autonomous mode, if the contradiction affects contracts/persistence/user-language, STOP per the transform table; otherwise surface it and proceed with the sharpened term.

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things." Domain-shaping sharpening stops for human input; low-blast-radius sharpening proceeds with a recorded assumption.

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force precision about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md). Append-only glossary entries avoid parallel-write clashes when multiple shaping phases run.

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

## During the session (READ-ONLY mode)

Read `CONTEXT.md` if present. Use the project's domain vocabulary in all test names, variable names, and output. If you find a contradiction:

1. **Do not rewrite `CONTEXT.md`.**
2. Emit a `**Domain proposal:**` line in Memory Notes describing the contradiction (term, glossary definition, code behavior).
3. If the contradiction makes the current phase's work ambiguous, block: `STATUS: FAIL`, `REMEDIATION_REASON: "Domain glossary contradicts code at term '{X}' — needs shaping-phase resolution"`.
4. If it does not block the work, proceed using the code's behavior as truth and flag the proposal for the next shaping phase.
