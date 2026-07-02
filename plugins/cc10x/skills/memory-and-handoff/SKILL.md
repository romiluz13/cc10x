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

- `references/memory-model-and-ownership.md` — memory surfaces, ownership, promotion, workflow markers
- `references/memory-operations.md` — permission-free operations, router-only persistence, edit patterns
- `references/memory-file-contracts.md` — required headings, stable anchors, templates, auto-heal rules
- `references/context-budget-and-checkpointing.md` — context-budget rules, warning signs, checkpoint triggers

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
- WRITE agents read memory but do NOT edit `.cc10x/*.md` directly
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

Keep each entry one line. Prefer stable nouns over temporary wording. Put verification truth in `verification`, not prose. Put non-blocking work in `deferred`, not ad-hoc tasks.

**Persist only memory-worthy items:** decisions that change direction, learnings that prevent mistakes, verification evidence with commands and exit truth, deferred non-blocking issues, plan/design/research references, clarified user standards.

**Do not persist:** whole diffs, verbose logs, celebratory narration, "looked correct" without evidence, duplicate notes, raw secrets/PII in outward artifacts.

### Secret Redaction (OUTWARD artifacts only)

Before router persists cc10x-authored content into outward artifacts (`docs/plans/*`, `docs/research/*`, design docs, persisted memory notes): redact pasted tokens, API keys, connection-strings, credentials, PII. Replace with `<redacted:secret>`. Keep surrounding constraint intact. Does NOT apply to internal machine-owned `.cc10x/` orchestration state — that stays verbatim for resume/dedupe keys.

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

1. **Write to OS temp dir, never into the repo.** `HANDOFF="${TMPDIR:-/tmp}/handoff-$(date +%Y%m%d-%H%M%S).md"`. Print the absolute path.
2. **Reference artifacts by path/URL, never paste contents.** The next reader has the repo. They need a map, not a copy. Prefer behavioral descriptions over `file:line` where code may still drift.
3. **Redact secrets and PII before writing.** Replace with `<redacted:secret>`, `<redacted:pii>`. Keep surrounding constraint intact. When unsure, redact.

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
