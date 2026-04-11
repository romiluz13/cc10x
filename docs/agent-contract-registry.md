# CC10X Agent Contract Registry

> **Status note:** Aligned to the live agent and router prompt stack as of 2026-04-12 (`v10.1.19`).
> **Purpose:** Quick contract map for maintainers. This document summarizes what the live prompts already enforce; it does not add new behavior.

## Write Agents

| Agent | Contract type | Completion states | Key blocking signal | Memory payload |
|------|---------------|-------------------|---------------------|----------------|
| `component-builder` | YAML `### Router Contract` | `PASS`, `FAIL` | `BLOCKING=true`, `PHASE_STATUS!=completed`, or `PROOF_STATUS!=passed` | `MEMORY_NOTES` |
| `bug-investigator` | YAML `### Router Contract` | `FIXED`, `INVESTIGATING`, `BLOCKED` | `STATUS!=FIXED` or research escalation | `MEMORY_NOTES` |
| `planner` | YAML `### Router Contract` | `PLAN_CREATED`, `DECISION_RFC_CREATED`, `NEEDS_CLARIFICATION` | open decisions, failed spec gate, or blocking clarification need | `MEMORY_NOTES` |
| `web-researcher` | YAML result block | `COMPLETE`, `PARTIAL`, `DEGRADED`, `UNAVAILABLE` | degraded or unavailable backend | `MEMORY_NOTES` |
| `github-researcher` | YAML result block | `COMPLETE`, `PARTIAL`, `DEGRADED`, `UNAVAILABLE` | degraded or unavailable backend | `MEMORY_NOTES` |

## Read-Only Review Agents

| Agent | Primary machine signal | Heading fallback | Completion states |
|------|-------------------------|------------------|-------------------|
| `code-reviewer` | `CONTRACT {"s":"APPROVE|CHANGES_REQUESTED","b":...,"cr":...}` | `## Review: Approve` / `## Review: Changes Requested` | `APPROVE`, `CHANGES_REQUESTED` |
| `silent-failure-hunter` | `CONTRACT {"s":"CLEAN|ISSUES_FOUND","b":...,"cr":...}` | `## Error Handling Audit: CLEAN` / `## Error Handling Audit: ISSUES_FOUND` | `CLEAN`, `ISSUES_FOUND` |
| `integration-verifier` | `CONTRACT {"s":"PASS|FAIL","b":...,"cr":...}` | `## Verification: PASS` / `## Verification: FAIL` | `PASS`, `FAIL` |

All three emit `### Memory Notes (For Workflow-Final Persistence)` instead of YAML
`MEMORY_NOTES`.

## Fresh Planning Review Agent

| Agent | Primary machine signal | Meaning |
|------|-------------------------|---------|
| `plan-gap-reviewer` | `CONTRACT {"s":"PASS|FINDINGS","b":...,"bf":...}` | fresh read-only challenge pass over a saved plan |

`b` means at least one blocking finding exists.
`bf` is the blocking finding count.

## Router Expectations

- Router reads line-1 envelopes first for read-only agents.
- Router falls back to stable headings if an envelope is malformed or absent.
- Router interprets contracts and owns every workflow decision after the agent returns.
- Router kernel may point to mandatory workflow/reference playbooks, but those
  reads remain router-owned orchestration behavior.
- Router remains the only orchestration owner for:
  - task creation
  - blocking / unblocking
  - remediation creation
  - phase advancement
  - memory finalization

## Memory Handoff Rules

- WRITE agents never edit `.claude/cc10x/v10/*.md` directly.
- WRITE agents emit YAML `MEMORY_NOTES`.
- READ-ONLY agents emit `### Memory Notes (For Workflow-Final Persistence)`.
- Router persists both shapes into workflow artifacts first, then final markdown memory.

## Related Sources

- [cc10x-router/SKILL.md](/Users/rom.iluz/Dev/cc10x_v5/cc10x/plugins/cc10x/skills/cc10x-router/SKILL.md)
- [router-invariants.md](/Users/rom.iluz/Dev/cc10x_v5/cc10x/docs/router-invariants.md)
- [prompt-invariants.md](/Users/rom.iluz/Dev/cc10x_v5/cc10x/docs/prompt-invariants.md)
