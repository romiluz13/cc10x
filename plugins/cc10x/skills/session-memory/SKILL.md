---
name: session-memory
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: Read, Write, Edit, Bash
user-invocable: false
---

# Session Memory (MANDATORY)

## Overview

CC10X memory is a small, stable, versioned Markdown index plus durable workflow artifacts.
It exists to survive compaction, preserve decisions, and keep BUILD / DEBUG / REVIEW / PLAN
aligned across sessions.

**Memory is an index, not a transcript.**
Be brief. Distill decisions, learnings, references, and verification evidence into durable,
reusable notes.

## Reference Map

Keep this file as the control plane. Read only the reference you need:

- `references/memory-model-and-ownership.md` for memory surfaces, ownership, promotion, and
  workflow markers
- `references/memory-operations.md` for permission-free operations, router-only persistence,
  and targeted edit patterns
- `references/memory-file-contracts.md` for required headings, stable anchors, templates, and
  auto-heal rules
- `references/context-budget-and-checkpointing.md` for context-budget rules, warning signs,
  and checkpoint triggers

## The Iron Law

```
EVERY WORKFLOW MUST:
1. LOAD memory at START and before key decisions
2. EMIT memory-worthy notes before finishing
3. LET the router/workflow finalizer persist markdown memory
```

If memory is skipped, the workflow becomes conversation-dependent.
If memory is narrated instead of distilled, it bloats context and loses signal.

## Load-Bearing Boundaries

- Memory lives under `.claude/cc10x/v10/`.
- The router loads and auto-heals memory files before routing or resume.
- WRITE agents read memory, but do **not** edit `.claude/cc10x/v10/*.md` directly.
- WRITE agents emit structured `MEMORY_NOTES` in their Router Contract.
- READ-ONLY agents emit `### Memory Notes (For Workflow-Final Persistence)`.
- The router-owned memory-finalize task is the only final writer of memory markdown files.
- Workflow artifacts under `.claude/cc10x/v10/workflows/{wf}.json` remain the durable
  execution truth; markdown memory is the stable index.
- Required headings and anchors are a contract. Do not invent new file layouts or marker
  schemes.
- Router-owned markers such as `[DEBUG-RESET: wf:{...}]` and
  `[cc10x-internal] memory_task_id` are read and respected by agents; agents do not invent
  replacements.

## Memory Surfaces

Use the right layer for the right kind of information:

- `activeContext.md`: current focus, recent changes, decisions, learnings, references,
  blockers
- `patterns.md`: reusable project standards, gotchas, conventions, and skill hints
- `progress.md`: current workflow, tasks snapshot, completed items, verification evidence
- `docs/plans/*` and `docs/research/*`: the detailed artifacts; memory points to them
- `.claude/cc10x/v10/workflows/{wf}.json` and `.events.jsonl`: the durable orchestration
  truth

Read `references/memory-model-and-ownership.md` if you need the full ownership model or the
promotion ladder.

## Distillation Rule

Memory entries must be distilled, not narrated.

Preserve:

- decisions with rationale
- causal learnings
- stable module boundaries and file paths
- verification commands and exit truth
- external artifact paths the next session will need

Strip:

- decorative prose
- step-by-step diary text
- speculation that was never resolved
- redundant retellings of the prompt
- unstable line numbers unless they are the only durable locator available

Test:

If a fresh agent reading memory cannot reconstruct the current constraints and next move
without re-reading the whole conversation, the memory is under-distilled.

## What To Load

### Always Load

At workflow start, continuation, or resume, read all three memory files:

```text
.claude/cc10x/v10/activeContext.md
.claude/cc10x/v10/patterns.md
.claude/cc10x/v10/progress.md
```

### Re-Read Before These Actions

| Action | Re-read | Why |
|--------|---------|-----|
| Architectural decision | `patterns.md` + `activeContext.md ## Decisions` | avoid contradicting project standards |
| Choosing implementation approach | `patterns.md` + `activeContext.md` | align with conventions and recent decisions |
| Debugging | `activeContext.md` + `patterns.md` + `progress.md` | reuse prior attempts, gotchas, and evidence |
| Planning next steps | `progress.md` + `activeContext.md` | avoid duplicate work and preserve order |
| Claiming completion | `progress.md` + current plan/design/research references | verify that proof and scope still match |
| User says "continue" | all three files | restore the durable state, not the chat summary |

### File Selection Matrix

| Need | Read |
|------|------|
| current focus / blockers | `activeContext.md` |
| prior decisions / rationale | `activeContext.md ## Decisions` |
| learned gotchas | `patterns.md` |
| project conventions | `patterns.md` |
| what is done / remaining | `progress.md` |
| proof commands and exits | `progress.md ## Verification` |
| detailed plan / research | `activeContext.md ## References` then the referenced file |

## What To Persist

Emit only memory-worthy items:

- decisions that change implementation direction
- learnings that prevent repeating the same mistake
- verification evidence with commands and exit truth
- deferred non-blocking issues that should survive the session
- plan, design, or research references the next workflow must follow
- clarified user standards or conventions that should become durable project patterns

Do not persist:

- whole diffs
- verbose execution logs
- celebratory narration
- "looked correct" claims without evidence
- duplicate notes that add no new constraint

## Agent Output Contract

WRITE agents persist memory through the Router Contract:

```yaml
MEMORY_NOTES:
  learnings: ["Key causal insight"]
  patterns: ["Reusable gotcha or convention"]
  verification: ["`npm test` -> exit 0"]
  deferred: ["Non-blocking follow-up or risk"]
```

Rules:

- Keep each entry one line when possible.
- Prefer stable nouns over temporary wording.
- Put verification truth in `verification`, not in narrative prose.
- Put non-blocking follow-up work in `deferred`, not in ad-hoc tasks.
- If a complementary skill failed to load or a durable artifact was missing in a way that
  matters, note it in `learnings` or `deferred`.

READ-ONLY agents use their own `### Memory Notes (For Workflow-Final Persistence)` section,
but the router persists both shapes into the same final memory update.

## Project Skill Hints

After loading memory, check `patterns.md ## Project SKILL_HINTS`.

- Invoke listed skills after memory load when they are relevant and installed.
- Treat missing skills as non-fatal; note the miss in memory-worthy output if it changed the
  workflow.
- Do not invent or rewrite skill IDs from this skill.
- Do not try to "maintain" `## Project SKILL_HINTS` from a write agent by editing memory
  directly. If a new durable recommendation matters, surface it in planner output or memory
  notes for router-owned persistence.

## Workflow Pattern

### Start

1. Read all three memory files.
2. Read current plan, design, or research files from `activeContext.md ## References` only if
   the workflow needs them.
3. Load approved project/domain skills from `## Project SKILL_HINTS` after memory is loaded.
4. If context is already getting heavy, apply
   `references/context-budget-and-checkpointing.md`.

### During

- Re-read memory before key decisions, not after the mistake.
- Respect router-owned markers such as `[DEBUG-RESET: wf:{...}]`.
- Keep notes distilled enough to survive compaction.
- Prefer durable artifacts and file paths over long conversational summaries.

### End

1. Distill decisions, learnings, verification, and deferred items into `MEMORY_NOTES`.
2. Keep each note factual and reusable.
3. Assume the router/workflow finalizer will persist the markdown files.
4. Do not report the workflow as truly complete if the memory cycle is missing.

## Context Budget And Checkpointing

Long sessions degrade before they fail loudly.

Use `references/context-budget-and-checkpointing.md` when:

- debugging has gone through multiple failed attempts
- planning/research is pulling in many large files
- the session has already accumulated many tool calls
- you notice vagueness, skipped protocol steps, or rising uncertainty

Checkpoint principle:

- persist durable state into workflow artifacts, plans, research files, and memory notes
- do not rely on the conversation transcript to carry load-bearing context

## Red Flags

Stop and correct course if you catch yourself:

- starting work without loading memory
- making decisions without checking `## Decisions` or project patterns
- writing long diary-style memory notes
- claiming you will "remember later"
- editing `.claude/cc10x/v10/*.md` directly from a write agent
- inventing new headings, markers, or memory file shapes
- treating stale conversation context as better than durable memory

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Small task, no need" | Small tasks still create decisions and evidence. |
| "I'll remember" | You won't; compaction will win. |
| "The conversation already has it" | Durable memory beats transcript lore. |
| "I'll just tweak the markdown directly" | Router-owned persistence exists to keep memory coherent. |
| "The note can be verbose" | Verbose notes burn context and hide the signal. |

## Verification Checklist

- [ ] Memory loaded at workflow start
- [ ] Relevant decisions/patterns checked before new decisions
- [ ] Notes distilled into `MEMORY_NOTES`
- [ ] Verification truth captured in memory-worthy form
- [ ] No direct write-agent edits to `.claude/cc10x/v10/*.md`
- [ ] Context-budget checkpointing considered if the session got heavy

Cannot check these boxes? The memory cycle is incomplete.
