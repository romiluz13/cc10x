# Memory Model And Ownership

## Contents

- Purpose
- Memory surfaces
- Ownership
- Promotion ladder
- What belongs where
- Distillation standard
- Project skill hints

## Purpose

This file explains what CC10X memory is, which layer owns each part, and what kind of
information belongs where.

## Memory Surfaces

- `activeContext.md`
  - current focus
  - recent changes
  - decisions
  - learnings
  - references
  - blockers
- `patterns.md`
  - durable user standards
  - architecture and code conventions
  - testing patterns
  - common gotchas
  - project skill hints
- `progress.md`
  - current workflow
  - task snapshot
  - completed items
  - verification evidence
- `docs/plans/*` and `docs/research/*`
  - detailed artifacts that memory points to
- `.claude/cc10x/v10/workflows/{wf}.json`
  - canonical workflow state
- `.claude/cc10x/v10/workflows/{wf}.events.jsonl`
  - append-only event trail

## Ownership

### Router

- loads and auto-heals the three memory files before routing or resume
- owns workflow artifacts and event logs
- owns final markdown persistence during the memory-finalize step
- owns transient workflow markers such as:
  - `[DEBUG-RESET: wf:{...}]`
  - `[cc10x-internal] memory_task_id: ...`

### WRITE Agents

- read memory at start and before key decisions
- do not edit `.claude/cc10x/v10/*.md` directly
- emit structured `MEMORY_NOTES` in their Router Contract

### READ-ONLY Agents

- read memory via their own prompts
- emit `### Memory Notes (For Workflow-Final Persistence)`
- never mutate markdown memory files

## Promotion Ladder

- one-off observation -> `activeContext.md`
- repeated or reusable lesson -> `patterns.md`
- detailed analysis -> `docs/research/*` or `docs/plans/*` plus a reference from
  `activeContext.md`
- hard proof -> `progress.md ## Verification`
- orchestration state -> workflow artifact, not markdown memory

## What Belongs Where

| Kind of information | Best home |
|---------------------|-----------|
| current blocker | `activeContext.md ## Blockers` |
| approved decision with rationale | `activeContext.md ## Decisions` |
| reusable gotcha or convention | `patterns.md` |
| command + exit truth | `progress.md ## Verification` |
| long design or research detail | `docs/plans/*` / `docs/research/*` |
| pending orchestration state | workflow artifact |

## Distillation Standard

Preserve:

- stable file paths and module boundaries
- decisions and why they changed the work
- verification commands, expected truth, and actual truth
- named external artifacts the next workflow needs

Strip:

- decorative narration
- large code excerpts unless they are the artifact itself
- unstable line numbers when file paths or section names are enough
- repeated rephrasing of the same fact

## Project Skill Hints

`patterns.md ## Project SKILL_HINTS` is durable project guidance.

- agents read it after memory load
- router may also pass `## SKILL_HINTS` directly in the agent scaffold
- this section should contain exact skill ids only
- adding or changing hints is a durable-memory concern, not an ad-hoc agent edit
