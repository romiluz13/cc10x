# Memory Model And Ownership

## Purpose

This file explains what CC10X memory is, which layer owns each part, and what kind of
information belongs where.

## Memory Surfaces

See the `### Memory Surfaces` table in SKILL.md.

## Ownership

Ownership: see SKILL.md `### Ownership` — the authoritative statement.

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
