# CC10X Agent Contract Registry

> **Status note:** Aligned to the `v12.10.0` product line as released on 2026-10-07 (v12.10.0; the release before it was v12.9.1); one row per agent in `plugins/cc10x/agents/` (14), and `harness_audit.py` fails when a row drifts from disk.
> **Purpose:** Quick contract map for maintainers. It summarizes what the agent prompts enforce; the prompts are the source of truth and this file adds no behavior.

## Return Format

Every agent returns the same shape:

1. Line 1: `CONTRACT {"s":"<STATUS>","b":<true|false>,"cr":<N>}`, the fast-path envelope.
2. Line 2: a stable heading (`## Build: PASS`, `## Review: Approve`, ...), the fallback when the YAML block is absent.
3. A fenced `yaml` Router Contract. Its `STATUS` decides; the router branches on it, not on the envelope.
4. Prose sections.

Envelope keys are `s` (STATUS), `b` (BLOCKING) and `cr` (CRITICAL_ISSUES). There is no `bf` key. `plan-gap-reviewer` uses the same keys: `b` means at least one blocking finding exists and `cr` is the blocking finding count (`BLOCKING_FINDINGS_COUNT`).

No agent calls `TaskUpdate` or creates tasks. The router completes each task after it validates the contract.

## Build, Debug, Plan And Docs Agents

| Agent | Contract type | Completion states | Key blocking signal | Memory payload |
| ------ | --------------- | ------------------- | --------------------- | ---------------- |
| `component-builder` | YAML Router Contract | `PASS`, `FAIL` | `BLOCKING=true`, `PHASE_STATUS!=completed`, or `PROOF_STATUS!=passed`; `PASS` also needs TDD evidence and the seam fields (`TEST_SEAMS`, `SEAM_GATE_STATUS`) | YAML `MEMORY_NOTES` |
| `bug-investigator` | YAML Router Contract | `FIXED`, `INVESTIGATING`, `BLOCKED` | `STATUS!=FIXED`, or research escalation (`NEEDS_EXTERNAL_RESEARCH`); `FIXED` needs `FEEDBACK_LOOP` and `DEBUG_CLOSEOUT` | YAML `MEMORY_NOTES` |
| `planner` | YAML Router Contract | `PLAN_CREATED`, `DECISION_RFC_CREATED`, `NEEDS_CLARIFICATION` | non-empty `OPEN_DECISIONS` forces `NEEDS_CLARIFICATION` with `BLOCKING=true` | YAML `MEMORY_NOTES` |
| `doc-syncer` | YAML Router Contract | `COMPLETE`, `SKIPPED`, `PARTIAL`, `FAIL` | `FAIL`, or `PARTIAL` with required layers missing | YAML `MEMORY_NOTES` |
| `researcher` | YAML Router Contract | `COMPLETE`, `PARTIAL`, `DEGRADED`, `UNAVAILABLE` | `BLOCKING` is `false`; the router reads `STATUS` and `QUALITY_LEVEL` | YAML `MEMORY_NOTES` |

### REM-FIX executors and disputes

`component-builder` and `bug-investigator` are the only executors of a `kind:remfix` task. The router picks one by the task's `origin:` (see its executor table).

- On a REM-FIX, `PASS` or `FIXED` also needs `COVERING_TESTS`, `TEST_COMMAND` and `TEST_OUTPUT` for every finding applied.
- An executor that can disprove a finding reports `FINDING_DISPUTED`, `VERIFY_COMMAND` and `VERIFY_OUTPUT` (same order in all three lists) instead of applying it. It never rules on its own dispute.
- `integration-verifier` is the only adjudicator: it re-runs `VERIFY_COMMAND` and lists 1-based positions of `FINDING_DISPUTED` in `DISPUTE_UPHELD` or `DISPUTE_REJECTED`. `code-reviewer` and `failure-hunter` never rule on a dispute.

## QA Agents

| Agent | Contract type | Completion states | Key blocking signal | Memory payload |
| ------ | --------------- | ------------------- | --------------------- | ---------------- |
| `qa-researcher` | YAML Router Contract | `PASS`, `FAIL` | reading outside the assigned `SOURCE` is `FAIL`; an empty or unavailable source reported honestly is `PASS` | YAML `MEMORY_NOTES` |
| `qa-harness-builder` | YAML Router Contract | `PASS`, `FAIL`, `BLOCKED` | `PRODUCT_CODE_TOUCHED=true`, a survived `MUTATION_CHECKS` entry, or non-empty `SERVICES_PROVISIONED` in preflight is `FAIL`; non-empty `BLOCKED_ITEMS`, `HUMAN_PREREQUISITES` or `CURRENCY_GATE` is `BLOCKED` with `NEXT_ACTION: gate` | YAML `MEMORY_NOTES` |
| `qa-executor` | YAML Router Contract | `PASS`, `FAIL`, `BLOCKED` | `TEST_CODE_TOUCHED` or `PRODUCT_CODE_TOUCHED` is `FAIL`; `TEARDOWN_STATUS` of `leaked` or `not_run` is `FAIL`; `SCENARIOS_BLOCKED>0` is `BLOCKED` | YAML `MEMORY_NOTES` |

## Read-Only Review Agents

| Agent | Primary machine signal | Heading fallback | Completion states |
| ------ | ------------------------- | ------------------ | ------------------- |
| `code-reviewer` | `CONTRACT {"s":"APPROVE\|CHANGES_REQUESTED","b":...,"cr":...}`; `b:true` only for `CHANGES_REQUESTED` with at least one CRITICAL finding | `## Review: Approve` / `## Review: Changes Requested` | `APPROVE`, `CHANGES_REQUESTED` |
| `failure-hunter` | `CONTRACT {"s":"CLEAN\|ISSUES_FOUND","b":...,"cr":...}`; `s=ISSUES_FOUND` for any CRITICAL or HIGH, `b:true` only when CRITICAL>0 | `## Error Handling Audit: CLEAN` / `## Error Handling Audit: ISSUES_FOUND` | `CLEAN`, `ISSUES_FOUND` |
| `integration-verifier` | `CONTRACT {"s":"PASS\|FAIL","b":...,"cr":...}` plus `PROOF_STATUS` in the YAML | `## Verification: PASS` / `## Verification: FAIL` | `PASS`, `FAIL` |
| `plan-gap-reviewer` | `CONTRACT {"s":"PASS\|FINDINGS","b":...,"cr":...}`; the YAML verdict key is `PLANNING_REVIEW_STATUS` | `## Planning Review: Pass` | `PASS`, `FINDINGS` |

`plan-gap-reviewer` has no `### Router Contract` heading; the router anchors on the first fenced `yaml` block after the line-2 heading. It echoes the lane it ran in `REVIEW_MODE_APPLIED` (`fresh` or `amendment`) and emits no memory notes.

## Advisory On-Ramp Agents

| Agent | Contract type | Completion states | Key blocking signal | Memory payload |
| ------ | --------------- | ------------------- | --------------------- | ---------------- |
| `triage-agent` | YAML Router Contract | `TRIAGED`, `NEEDS_INFO`, `WONTFIX` | `BLOCKING` is true when the run stops for human input (`NEEDS_INFO`, `WONTFIX`, or `NEEDS_GRILLING`); `cr` is always 0 | YAML `MEMORY_NOTES` and prose Memory Notes |
| `architecture-scanner` | YAML Router Contract | `CANDIDATES_FOUND`, `NO_CANDIDATES` | none: `b` and `cr` are always 0 (advisory) | YAML `MEMORY_NOTES` and prose Memory Notes |

## Skill Preload

Each agent's `skills:` frontmatter preloads these skills.

| Agent | Preloaded skills |
| ------ | ------------------ |
| architecture-scanner | `agent-common`, `codebase-hygiene`, `codebase-design` |
| bug-investigator | `agent-common`, `debugging`, `building`, `verification`, `codebase-design` |
| code-reviewer | `agent-common`, `code-review`, `verification`, `codebase-design` |
| component-builder | `agent-common`, `building`, `verification`, `codebase-design`, `domain-modeling` |
| doc-syncer | `agent-common`, `diff-driven-docs`, `verification`, `domain-modeling` |
| failure-hunter | `agent-common`, `code-review` |
| integration-verifier | `agent-common`, `verification` |
| plan-gap-reviewer | none (reads no memory and loads no skills, by design) |
| planner | `agent-common`, `planning`, `codebase-design`, `domain-modeling` |
| qa-executor | `agent-common`, `qa-strategy`, `verification` |
| qa-harness-builder | `agent-common`, `qa-strategy`, `verification` |
| qa-researcher | `agent-common`, `qa-strategy` |
| researcher | `agent-common`; its tools include `Skill` |
| triage-agent | `agent-common`, `domain-modeling` |

## Router Expectations

- Router reads line-1 envelopes first.
- Router falls back to stable headings if an envelope is malformed or absent.
- Router interprets contracts and owns every workflow decision after the agent returns.
- Router kernel may point to mandatory workflow/reference playbooks; those reads remain router-owned orchestration behavior.
- Router remains the only orchestration owner for:
  - task creation
  - blocking / unblocking
  - remediation creation
  - phase advancement
  - memory finalization

## Memory Handoff Rules

- No agent edits `.cc10x/*.md` directly.
- Build, debug, plan, docs, research and QA agents carry `MEMORY_NOTES` in their YAML Router Contract.
- Read-only agents emit `### Memory Notes (For Workflow-Final Persistence)`; `code-reviewer`, `failure-hunter`, `integration-verifier`, `triage-agent` and `architecture-scanner` also carry the YAML key.
- Router persists the notes into workflow artifacts first, then final markdown memory.

## Related Sources

- [cc10x-router/SKILL.md](../plugins/cc10x/skills/cc10x-router/SKILL.md)
- [router-invariants.md](router-invariants.md)
- [prompt-invariants.md](prompt-invariants.md)
