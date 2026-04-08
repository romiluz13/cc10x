# CC10x Orchestration Logic Analysis

> **Last synced with live router/agents:** 2026-04-09 (`v10.1.18`)
> **Status:** IN SYNC WITH CURRENT MAIN
> **Relationship to Bible:** The bible is the canonical specification. This document explains the practical mechanics and why the system is shaped this way.

## What CC10X Actually Is

CC10X is a **Claude Code plugin-native orchestration harness**.

It is not:
- a standalone agent service
- an issue tracker worker
- a hidden repo-local sidecar

It is:
- one router skill
- a small set of specialized agents
- a small set of plugin hooks
- optional user-configured MCP acceleration
- reference-first advisory skills with one-level-deep `references/`
- workflow artifacts under `.claude/cc10x/v10/workflows/`

The system is still mostly **English orchestration**, but it is no longer prompt-only. The current design mixes:
- prompt contracts
- reference-first skill packaging
- task metadata
- durable workflow artifacts
- plugin hooks
- replay/audit scripts

That mix is the current reliability model.

## Current Layers

### 1. Claude Code platform layer
Owned by Claude Code:
- plugin packaging
- subagents
- hooks
- MCP
- task primitives

### 2. CC10X orchestration layer
Owned by this plugin:
- intent routing
- workflow selection
- task graph creation
- workflow-scoped metadata
- remediation loops
- contract parsing
- memory finalization

### 3. Safety layer
Also owned by this plugin:
- hook guards
- workflow artifacts
- workflow event logs
- harness audit
- workflow replay fixtures
- invariant registry

## The Real Runtime Flow

### Entry
The router loads memory, checks for active workflow state, and either:
- resumes a workflow
- or routes into BUILD / DEBUG / REVIEW / PLAN

### Workflow state
Every workflow gets:
- a parent task
- workflow-scoped child tasks
- `.claude/cc10x/v10/workflows/{wf}.json`
- `.claude/cc10x/v10/workflows/{wf}.events.jsonl`

This is the durable truth for orchestration.

### Worker model
Agents are narrow workers:
- write agents produce YAML contracts
- read-only agents produce envelope-first contracts
- all agents emit structured memory notes instead of writing markdown memory directly
- router interprets outputs and owns state transitions

The important design boundary is:
- workers analyze/build/fix/verify
- router decides what happens next

### Hook model
Hooks are intentionally small:
- `PreToolUse` protects memory writes
- `SessionStart` re-injects workflow context
- `PostToolUse` audits workflow artifact integrity
- `TaskCompleted` audits metadata completeness

Hooks are not a second router.

## Why The Current Shape Is Better Than The Old Shape

Older CC10X revisions leaned too hard on:
- very large router prose
- worker-side orchestration
- repo-local runtime assumptions
- memory markdown as live truth

Current main is better because:
- orchestration ownership is centralized
- the router is now a kernel with mandatory workflow/reference playbooks instead of one giant always-loaded monolith
- workflow state is durable
- plugin behavior is plugin-native
- research is capability-aware and fallback-safe
- evidence is stricter and more scenario-based
- advisory skills are increasingly reference-first instead of monolithic
- safety is checked by scripts, not only memory

## The Six SDLC Capabilities CC10X Actually Optimizes

CC10X is intentionally optimized for:
- `PLAN`
- `BUILD`
- `DEBUG`
- `REVIEW`
- `VERIFY`
- `RESEARCH`

It is not trying to be a full deployment/ops/compliance platform.

Within that scope, the current design center is:
- intent-first planning
- TDD-driven building/debugging
- adversarial review
- BDD-style verification evidence
- router-owned convergence and remediation
- plugin-native research acceleration

## Where The Remaining Risk Still Lives

Even after the stability hardening, the main remaining risk areas are:
- live Claude runtime behavior under long sessions
- model interpretation of router prose in unusual edge cases
- doc drift when trust docs are not refreshed with prompt/runtime edits
- oversized control planes that have not yet been split into references, especially if they are still always-loaded
- prompt drift if agent contracts and router expectations diverge
- future changes that bypass the replay/audit checks

That is why the safety stack now includes:
- `cc10x_harness_audit.py`
- `cc10x_workflow_replay_check.py`
- `router-invariants.md`

## Maintenance Rule

When changing orchestration, always update in this order:
1. router/runtime behavior
2. replay fixtures/checker
3. harness audit
4. invariant registry
5. bible / logic / safety docs

If one of those is skipped, future-you loses context immediately.
