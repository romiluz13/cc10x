---
name: memory-and-handoff
description: |
  Two-mode skill: (1) session memory — load/persist durable workflow state under .cc10x/
  (activeContext, patterns, progress) so context survives compaction; (2) handoff package —
  portable, secrets-redacted export for a coworker, different tool, or fresh non-cc10x session.
allowed-tools: Read Write Edit Bash Grep Glob
user-invocable: false
---

# Memory & Handoff

## Reference Files

Read only what's needed:

- `references/memory-model-and-ownership.md` — memory surfaces, ownership, promotion, workflow markers; load when deciding which surface holds a piece of state or who may write it
- `references/memory-operations.md` — permission-free operations, router-only persistence, edit patterns; load when actually reading or writing `.cc10x/` files
- `references/memory-file-contracts.md` — required headings, stable anchors, templates, auto-heal rules; load when creating a memory file or healing a malformed one
- `references/context-budget-and-checkpointing.md` — context-budget rules, warning signs, checkpoint triggers; load when context is getting heavy or before a compaction/checkpoint decision

---

## Mode: SESSION MEMORY

Memory is an index, not a transcript. Distill decisions, learnings, references, and verification evidence into durable, reusable notes.

### Memory Surfaces

| File | Holds |
| ------ | ------- |
| `.cc10x/activeContext.md` | current focus, recent changes, decisions, learnings, references, blockers |
| `.cc10x/patterns.md` | reusable project standards, gotchas, conventions, skill hints |
| `.cc10x/progress.md` | current workflow, tasks snapshot, completed items, verification evidence |
| `.cc10x/workflows/{wf}.json` + `.events.jsonl` | durable orchestration truth (machine-owned, verbatim) |
| `docs/plans/*`, `docs/research/*` | detailed artifacts; memory points to them |

### Ownership

- Router loads and auto-heals memory files before routing or resume
- WRITE agents read memory but do NOT edit `.cc10x/*.md` (sole carve-out: bug-investigator's `[DEBUG-N]` lines)
- WRITE agents emit structured `MEMORY_NOTES` in their Router Contract
- READ-ONLY agents emit `### Memory Notes (For Workflow-Final Persistence)`
- Router-owned memory-finalize task is the only final writer of memory markdown files
- Router-owned markers (`[DEBUG-RESET: wf:{...}]`, `[cc10x-internal] memory_task_id`) are read and respected; agents do not invent replacements

### Load (MANDATORY at workflow start)

Read all three: `activeContext.md`, `patterns.md`, `progress.md`.

Re-read before: architectural decisions (`patterns.md` + `activeContext.md ## Decisions`), implementation choices (`patterns.md` + `activeContext.md`), debugging (all three), planning next steps (`progress.md` + `activeContext.md`), claiming completion (`progress.md` + plan/design/research refs), user says "continue" (all three).

### Persist

Emit `MEMORY_NOTES` in Router Contract:

```yaml
MEMORY_NOTES:
  learnings: ["Key causal insight"]
  patterns: ["Reusable gotcha or convention"]
  verification: ["`npm test` -> exit 0"]
  deferred: ["Non-blocking follow-up or risk"]
```

Keep each entry one line — memory reloads every session; each extra line is a recurring tax. Prefer stable nouns over temporary wording. Put verification truth in `verification`, not prose. Put non-blocking work in `deferred`, not ad-hoc tasks.

**Persist only memory-worthy items:** decisions that change direction, learnings that prevent mistakes, verification evidence with commands and exit truth, deferred non-blocking issues, plan/design/research references, clarified user standards.

**Do not persist:** whole diffs, verbose logs, celebratory narration, "looked correct" without evidence, duplicate notes, raw secrets/PII in outward artifacts.

### Secret Redaction (OUTWARD artifacts only)

Before router persists cc10x-authored content into outward artifacts (`docs/plans/*`, `docs/research/*`, design docs, persisted memory notes): redact pasted tokens, API keys, connection-strings, credentials, PII. Replace with `<redacted:secret>` (PII: `<redacted:pii>`). Keep surrounding constraint intact. When unsure, redact. Does NOT apply to internal machine-owned `.cc10x/` orchestration state — that stays verbatim for resume/dedupe keys.

### Compaction KEEP / SUMMARIZE / DROP Rubric

| Tier | What | Rule |
| ------ | ------ | ------ |
| KEEP | user hard-constraints/prohibitions, exact next step, open failures + errors | preserve VERBATIM — never paraphrase a constraint or error |
| SUMMARIZE | resolved decisions with rationale, concluded attempts, discovered file/module boundaries | distill to one durable line each |
| DROP | decorative prose, step-by-step diary, superseded speculation, redundant prompt retellings | discard |

Persist user PROHIBITIONS verbatim into workflow artifact's intent field as soon as stated — compaction may fire before router's normal persist.

### Project Skill Hints

After loading memory, check `patterns.md ## Project SKILL_HINTS`. Invoke listed skills when relevant and installed. Treat missing skills as non-fatal. Do not invent skill IDs. Do not edit `## Project SKILL_HINTS` directly — surface recommendations in planner output or memory notes.

---

## Mode: HANDOFF PACKAGE

A portable, human-readable export for when the next reader is NOT this cc10x session — a coworker, a different tool, or a clean session with no cc10x router.

cc10x's own resume is structural (`.cc10x/` + router rehydrates). The handoff package is the bridge OUT to a reader who cannot read `.cc10x/` orchestration state.

### Rules

1. **Write to OS temp dir, never into the repo** — a repo-committed handoff becomes a stale doc the next reader mistakes for current truth. `HANDOFF="${TMPDIR:-/tmp}/handoff-$(date +%Y%m%d-%H%M%S).md"`. Print the absolute path.
2. **Reference artifacts by path/URL, never paste contents.** The next reader has the repo. They need a map, not a copy. Prefer behavioral descriptions over `file:line` where code may still drift.
3. **Redact secrets and PII before writing.** Redact per `### Secret Redaction` above.

### Contents

| Section | Holds |
| --------- | ------- |
| Goal | one-line objective, verbatim user intent if stated |
| Current state | where things stand, one short paragraph |
| What's done | reference artifacts by path; do not re-narrate |
| What's next | EXACT next step — concrete enough to start cold |
| Open blockers / failures | unresolved errors VERBATIM, failing commands, dead ends tried |
| Suggested skills / tools | which skills the next agent should invoke to continue |
| Artifacts (by path) | plan, diff/PR, key source files with behavioral descriptions |

The "suggested skills/tools" pointer is load-bearing: tell the next agent how to continue. If cc10x is present: invoke `cc10x-router`. If not: name domain skills and point at plan/research docs.

---

## Knowledge Compounding Loop

Memory is not just for context survival — it's for system self-improvement. After every BUILD or DEBUG cycle, structured learnings should compound into reusable knowledge. Memory files (`activeContext.md`, `patterns.md`, `progress.md`) hold session-scoped context; **durable, structured learnings that survive across projects and sessions** go to `docs/solutions/`.

### The Loop

1. **Capture** — During workflow-finalize, the router writes structured learnings from agent `MEMORY_NOTES` into `activeContext.md ## Learnings` and `patterns.md ## Common Gotchas`; learnings that cross the solution-doc threshold (below) are written to `docs/solutions/`.
2. **Ground** — Before starting new work, agents read `patterns.md`, `activeContext.md`, and `docs/solutions/` to avoid repeating solved problems.
3. **Consolidate** — When the same gotcha appears 3+ times in `patterns.md`, promote it to a solution doc under `docs/solutions/`.
4. **Refresh** — Periodically audit learnings and solution docs with the five-outcome model (below).
5. **Discover** — Ensure `CLAUDE.md` or `AGENTS.md` points to `docs/solutions/` so agents can find it.

### When to Write a Solution Doc

After any non-trivial debug or build cycle, the router (during memory-finalize) evaluates whether to write a solution doc:

- **Write** if: the problem took 3+ hypotheses (debug attempts) to solve, OR the same defect pattern appears in 3+ files, OR the solution contradicts a documented assumption in `patterns.md`
- **Skip** if: the fix was mechanical (typo, import error, one-line change)
- **Offer neutrally** if: the lesson is one sentence (mention in memory notes instead)

### Compounding Outcomes

When reviewing prior learnings during memory-finalize (or auditing solution docs), apply one of five outcomes:

| Outcome | When | Action |
| ---------- | ------ | -------- |
| **Keep** | Learning is still accurate and useful | Leave as-is |
| **Update** | Learning is correct but incomplete | Add the missing detail |
| **Consolidate** | Same lesson appears multiple times | Merge into one entry, remove duplicates |
| **Replace** | Learning is outdated or superseded | Replace with the current truth |
| **Delete** | Learning no longer applies (framework changed, code removed) | Remove it |

**Why this matters:** Without consolidation, memory accumulates stale entries that mislead future work. The compounding loop ensures memory gets sharper over time, not just larger.

### Solution Doc Format

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
