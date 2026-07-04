# Orphaned Skills Check — Verification Report

## Methodology

For each of the 17 skills in `/Users/rom.iluz/Dev/cc10x/plugins/cc10x/skills/`, I checked:

1. **Agent frontmatter `skills:`** — which of the 9 agent files list this skill in their `skills:` YAML frontmatter
2. **Router SKILL_HINTS / dispatcher** — whether the cc10x-router SKILL.md references the skill in §7 "Deterministic skill hints" or the dispatcher table
3. **Cross-skill references** — whether any other skill's SKILL.md references this skill
4. **Agent body `Skill()` calls** — whether any agent invokes the skill via `Skill(skill="cc10x:...")` in its body text
5. **`user-invocable` frontmatter** — whether the skill is marked `user-invocable: false` (internal only) or left unset (potentially user-facing)

## Agent Skills Frontmatter Summary

| Agent | Skills in Frontmatter |
| ------- | ---------------------- |
| bug-investigator | agent-common, debugging, building, verification |
| code-reviewer | agent-common, code-review, verification, codebase-hygiene |
| component-builder | agent-common, building, verification |
| doc-syncer | agent-common, diff-driven-docs, verification |
| integration-verifier | agent-common, verification |
| plan-gap-reviewer | _(none — no `skills:` field; intentionally context-free)_ |
| planner | agent-common, planning, architecture |
| researcher | agent-common, mcp-cli |
| silent-failure-hunter | agent-common, code-review |

## Router SKILL_HINTS (§7 Deterministic Skill Hints)

The router loads these skills via `## SKILL_HINTS` in agent dispatch prompts:

| Skill | Router SKILL_HINTS Condition |
| ------- | ------------------------------ |
| cc10x:frontend | UI/frontend work detected |
| cc10x:architecture | Multi-component, API, schema, auth, integration-heavy work |
| cc10x:research | Planner or investigator receives `## Research Files` |
| cc10x:exploration | Explicit de-risk/spike intent |
| cc10x:codebase-hygiene | Reuse/consolidation audit or shallow module deepening |
| cc10x:mcp-cli | Researcher needs one-off MCP capability |
| cc10x:code-review | Human/external reviewer feedback must be acted on |
| cc10x:memory-and-handoff | Work being handed to a coworker/different tool |

Additionally, the router references `cc10x:memory-and-handoff` in §2 as the template for creating memory files, and invokes `cc10x:exploration` via `Skill()` in the PLAN workflow (per `references/plan-workflow.md`).

## Skills Not in Any Agent Frontmatter but Active via Other Mechanisms

| Skill | Loading Mechanism |
| ------- | ------------------- |
| exploration | Router SKILL_HINTS + PLAN workflow `Skill(skill="cc10x:exploration")` call |
| frontend | Router SKILL_HINTS (agents explicitly prohibited from self-activating) |
| research | Router SKILL_HINTS (loaded when research files are available) |
| memory-and-handoff | Router §2 template + SKILL_HINTS for handoff scenarios |
| plan-review-gate | Planner agent body: `Skill(skill="cc10x:plan-review-gate")` (step 15) |

## User-Facing Skills (no `user-invocable: false`)

| Skill | Frontmatter Signal | Purpose |
| ------- | ------------------- | --------- |
| cc10x-router | No `user-invocable` field; description says "THE ONLY ENTRY POINT FOR CC10X" | Main entry point skill activated by users |
| update | No `user-invocable` field; description lists user trigger keywords ("update cc10x", "upgrade") | Self-maintenance skill for upgrading the cc10x plugin |
| diff-driven-docs | No `user-invocable` field; description mentions user triggers ("update docs", "sync docs") | Documentation sync; also loaded by doc-syncer agent |

## Cross-Skill References

- `mcp-cli/SKILL.md` mentions composing with `cc10x:research`
- `research/SKILL.md` references `cc10x:researcher` (agent, not skill)
- `cc10x-router/SKILL.md` references `cc10x:memory-and-handoff` as template
- `cc10x-router/references/plan-workflow.md` invokes `cc10x:exploration`
- `cc10x-router/references/remediation-and-research.md` references `cc10x:research` in SKILL_HINTS
- `planner.md` (agent body) invokes `cc10x:plan-review-gate` and references `cc10x:research`
- `code-reviewer.md` (agent body) references `cc10x:frontend` (prohibiting self-activation)

## Final Status Table

| # | Skill | Status | Loaded By | `user-invocable` | Notes |
| --- | ------- | -------- | ----------- | ------------------- | ------- |
| 1 | agent-common | **ACTIVE** | 8 agents (frontmatter): bug-investigator, code-reviewer, component-builder, doc-syncer, integration-verifier, planner, researcher, silent-failure-hunter | `disable-model-invocation: true` | Shared preamble; not in plan-gap-reviewer (intentional — fresh review) |
| 2 | architecture | **ACTIVE** | planner (frontmatter) + router SKILL_HINTS | `false` | Greenfield architecture design |
| 3 | building | **ACTIVE** | bug-investigator, component-builder (frontmatter) | `false` | TDD implementation skill |
| 4 | cc10x-router | **USER-FACING** | N/A — IS the router entry point | not set | Main entry point skill; activated directly by users |
| 5 | code-review | **ACTIVE** | code-reviewer, silent-failure-hunter (frontmatter) + router SKILL_HINTS | `false` | Adversarial review + receiving-review discipline |
| 6 | codebase-hygiene | **ACTIVE** | code-reviewer (frontmatter) + router SKILL_HINTS | `false` | Duplicate detection + module deepening |
| 7 | debugging | **ACTIVE** | bug-investigator (frontmatter) | `false` | Feedback-loop-first debugging discipline |
| 8 | diff-driven-docs | **ACTIVE** | doc-syncer (frontmatter) | not set | Doc sync; also potentially user-facing (description mentions user triggers) |
| 9 | exploration | **ACTIVE** | router SKILL_HINTS + PLAN workflow `Skill()` invocation | `false` | Design dialogue + spike; loaded by router, not agent frontmatter |
| 10 | frontend | **ACTIVE** | router SKILL_HINTS (agents prohibited from self-activating) | `false` | UI authoring + critique; router-gated only |
| 11 | mcp-cli | **ACTIVE** | researcher (frontmatter) + router SKILL_HINTS | `false` | Transient MCP server access |
| 12 | memory-and-handoff | **ACTIVE** | router §2 template + SKILL_HINTS | `false` | Session memory + handoff packages |
| 13 | plan-review-gate | **ACTIVE** | planner agent body `Skill(skill="cc10x:plan-review-gate")` (step 15) | `false` | Inline spec review gate; not in frontmatter but invoked via Skill() |
| 14 | planning | **ACTIVE** | planner (frontmatter) | `false` | Execution plan + decision RFC discipline |
| 15 | research | **ACTIVE** | router SKILL_HINTS + cross-ref from mcp-cli skill | `false` | Research synthesis guidance; loaded via SKILL_HINTS when research files exist |
| 16 | update | **USER-FACING** | N/A — self-maintenance skill | not set | Plugin upgrade skill; user-triggered |
| 17 | verification | **ACTIVE** | 5 agents (frontmatter): bug-investigator, code-reviewer, component-builder, doc-syncer, integration-verifier | `false` | Verification discipline; most widely loaded skill after agent-common |

## Summary

**ORPHANED SKILLS: NONE (0/17)**

All 17 skills are accounted for:

- **14 ACTIVE (internal, loaded by agents or router)**: agent-common, architecture, building, code-review, codebase-hygiene, debugging, exploration, frontend, mcp-cli, memory-and-handoff, plan-review-gate, planning, research, verification
- **3 potentially USER-FACING**: cc10x-router (main entry point), update (plugin self-upgrade), diff-driven-docs (user-triggered doc sync, also loaded by doc-syncer agent)

### Key observations

1. **agent-common** is the most widely loaded skill (8 of 9 agents). The only agent without it is `plan-gap-reviewer`, which is intentionally context-free for anti-anchoring.

2. **verification** is the second most widely loaded skill (5 agents), reflecting the system's "task completion is not goal achievement" philosophy.

3. **Five skills are NOT in any agent's `skills:` frontmatter** but are still active via other loading mechanisms:
   - `exploration` — router SKILL_HINTS + PLAN workflow `Skill()` call
   - `frontend` — router SKILL_HINTS only (agents explicitly prohibited from self-activating)
   - `research` — router SKILL_HINTS only
   - `memory-and-handoff` — router template reference + SKILL_HINTS
   - `plan-review-gate` — planner agent body `Skill()` invocation (not frontmatter)

4. **plan-review-gate** is the only skill loaded exclusively via an agent body `Skill()` call rather than frontmatter or router SKILL_HINTS. This is by design — it's an inline self-review gate the planner runs on its own plan before output.

5. **diff-driven-docs** lacks `user-invocable: false`, suggesting it can be both user-invoked (user says "update docs") and agent-loaded (doc-syncer frontmatter). This dual-use pattern is intentional.

6. **No orphaned skills exist.** Every skill has at least one concrete loading path — either an agent frontmatter entry, a router SKILL_HINTS rule, an agent body `Skill()` call, or user-facing activation.