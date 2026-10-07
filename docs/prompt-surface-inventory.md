# CC10X Prompt Surface Inventory

> **Status note:** Aligned to the `v12.10.0` product line as released on 2026-10-07 (v12.10.0; the release before it was v12.9.1). One entry per agent in `plugins/cc10x/agents/` and per skill in `plugins/cc10x/skills/`; `harness_audit.py` fails when an entry, a path or a name drifts from disk.

## Purpose

This inventory records which prompt surfaces can affect trust-critical behavior and how much review an edit needs.

The router (`cc10x-router`) and its `plugins/cc10x/skills/cc10x-router/references/` files are orchestration surfaces. They are not prompt-only: change them with replay, audit and Claude validation.

Hooks (`plugins/cc10x/hooks/hooks.json`) and tools (`plugins/cc10x/tools/`) are code, not prompt surfaces, and are not listed here.

## Tiers

- Tier 1, trust-critical contracts: audit, replay and manual semantic review.
- Tier 2, supporting contracts: audit and targeted semantic review.
- Tier 3, advisory skills: audit; replay only if authority wording changes.

## Orchestration Surface

### cc10x-router

- Path: `plugins/cc10x/skills/cc10x-router/SKILL.md`
- Tier: orchestration (not eligible for a prompt-only change)
- Purpose: single entry point; intent routing, task graphs, workflow artifacts, gates, memory finalization

## Tier 1: Trust-Critical Contracts

### planner

- Path: `plugins/cc10x/agents/planner.md`
- Tier: 1
- Purpose: saved execution plan or decision RFC, agreement first

### component-builder

- Path: `plugins/cc10x/agents/component-builder.md`
- Tier: 1
- Purpose: executes the current approved phase test-first, with seam and evidence fields

### integration-verifier

- Path: `plugins/cc10x/agents/integration-verifier.md`
- Tier: 1
- Purpose: fail-closed end-to-end verification before any pass or advance claim

### qa-harness-builder

- Path: `plugins/cc10x/agents/qa-harness-builder.md`
- Tier: 1
- Purpose: builds the QA test environment and suites from an approved plan; never modifies product code

### qa-executor

- Path: `plugins/cc10x/agents/qa-executor.md`
- Tier: 1
- Purpose: runs an approved QA plan, records per-scenario evidence, emits bug candidates; never edits test or product code

### agent-common

- Path: `plugins/cc10x/skills/agent-common/SKILL.md`
- Tier: 1
- Purpose: preamble preloaded into 13 agents: memory protocol, contract format, output rules

### memory-and-handoff

- Path: `plugins/cc10x/skills/memory-and-handoff/SKILL.md`
- Tier: 1
- Purpose: session memory under `.cc10x/` and the portable, redacted handoff package

### plan-review-gate

- Path: `plugins/cc10x/skills/plan-review-gate/SKILL.md`
- Tier: 1
- Purpose: fail-closed plan review that blocks execution

### verification

- Path: `plugins/cc10x/skills/verification/SKILL.md`
- Tier: 1
- Purpose: goal-backward verification, evidence array protocol, fresh-evidence rule

## Tier 2: Supporting Contracts

### plan-gap-reviewer

- Path: `plugins/cc10x/agents/plan-gap-reviewer.md`
- Tier: 2
- Purpose: fresh, read-only challenge pass over a saved plan

### bug-investigator

- Path: `plugins/cc10x/agents/bug-investigator.md`
- Tier: 2
- Purpose: evidence-first debugging with variant and blast-radius coverage

### code-reviewer

- Path: `plugins/cc10x/agents/code-reviewer.md`
- Tier: 2
- Purpose: adversarial multi-dimension review with confidence-scored findings

### failure-hunter

- Path: `plugins/cc10x/agents/failure-hunter.md`
- Tier: 2
- Purpose: finds silent failures (empty catches, swallowed errors) in parallel with the code review

### qa-researcher

- Path: `plugins/cc10x/agents/qa-researcher.md`
- Tier: 2
- Purpose: scans one source and reports what the feature does, for QA test planning

### researcher

- Path: `plugins/cc10x/agents/researcher.md`
- Tier: 2
- Purpose: web and GitHub research persisted to dated files as a structured research contract

### triage-agent

- Path: `plugins/cc10x/agents/triage-agent.md`
- Tier: 2
- Purpose: categorizes and verifies issues and PRs and writes agent-ready briefs; no source writes

### architecture-scanner

- Path: `plugins/cc10x/agents/architecture-scanner.md`
- Tier: 2
- Purpose: read-only scan for shallow modules and duplicates, with an HTML report

### doc-syncer

- Path: `plugins/cc10x/agents/doc-syncer.md`
- Tier: 2
- Purpose: updates documentation layers to match the current diff

### building

- Path: `plugins/cc10x/skills/building/SKILL.md`
- Tier: 2
- Purpose: RED-GREEN-REFACTOR discipline, false-RED detection, seam discipline

### debugging

- Path: `plugins/cc10x/skills/debugging/SKILL.md`
- Tier: 2
- Purpose: feedback loop first, root cause before fix, blast radius after fix

### code-review

- Path: `plugins/cc10x/skills/code-review/SKILL.md`
- Tier: 2
- Purpose: adversarial review rubric and the verify-before-agreeing rule for received feedback

### planning

- Path: `plugins/cc10x/skills/planning/SKILL.md`
- Tier: 2
- Purpose: task decomposition, validation levels, plan completeness gate, decision RFC format

### qa-strategy

- Path: `plugins/cc10x/skills/qa-strategy/SKILL.md`
- Tier: 2
- Purpose: QA tiers, scenario matrices, environment isolation, fixture lifecycle, flake sources

### update

- Path: `plugins/cc10x/skills/update/SKILL.md`
- Tier: 2
- Purpose: cc10x upgrade through the plugin CLI across installed scopes

## Tier 3: Advisory Skills

### architecture

- Path: `plugins/cc10x/skills/architecture/SKILL.md`
- Tier: 3
- Purpose: greenfield architecture design: flows, components, APIs, dependencies

### cc10x-guide

- Path: `plugins/cc10x/skills/cc10x-guide/SKILL.md`
- Tier: 3
- Purpose: answers questions about cc10x itself; reads only, performs no work

### codebase-design

- Path: `plugins/cc10x/skills/codebase-design/SKILL.md`
- Tier: 3
- Purpose: deep-module vocabulary (module, interface, depth, seam) used by other skills

### codebase-hygiene

- Path: `plugins/cc10x/skills/codebase-hygiene/SKILL.md`
- Tier: 3
- Purpose: advisory search for semantic duplicates and shallow modules; changes route through BUILD

### diff-driven-docs

- Path: `plugins/cc10x/skills/diff-driven-docs/SKILL.md`
- Tier: 3
- Purpose: classifies a diff's documentation impact across business, technical and audit layers

### domain-modeling

- Path: `plugins/cc10x/skills/domain-modeling/SKILL.md`
- Tier: 3
- Purpose: glossary and ADR discipline; active for shaping agents, read-only for builders

### exploration

- Path: `plugins/cc10x/skills/exploration/SKILL.md`
- Tier: 3
- Purpose: design dialogue before planning, and throwaway spikes that answer one question

### frontend

- Path: `plugins/cc10x/skills/frontend/SKILL.md`
- Tier: 3
- Purpose: UI authoring guidance and a read-only scored critique of built UI

### mcp-cli

- Path: `plugins/cc10x/skills/mcp-cli/SKILL.md`
- Tier: 3
- Purpose: one-off call to an unmounted MCP server through the `mcp` CLI

### research

- Path: `plugins/cc10x/skills/research/SKILL.md`
- Tier: 3
- Purpose: synthesis of research files into a recommendation; does not run research

### resolving-merge-conflicts

- Path: `plugins/cc10x/skills/resolving-merge-conflicts/SKILL.md`
- Tier: 3
- Purpose: procedure for an in-progress merge or rebase that reports conflicts

## Review Classification

Every prompt change is classified before merge, as set out in `docs/prompt-change-checklist.md`:

- `metadata_only`
- `wording_only_low_risk`
- `wording_only_trust_sensitive`
- `orchestration_sensitive` (not eligible for a prompt-only release)
