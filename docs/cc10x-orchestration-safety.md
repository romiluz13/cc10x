# CC10x Orchestration Safety

> **Purpose:** Practical guardrails for changing CC10X without breaking the live harness.
> **Audience:** Future maintainers working on router, hooks, agents, skills, or workflow artifacts.

## Source Of Truth Order

When behavior conflicts, trust sources in this order:
1. `plugins/cc10x/skills/cc10x-router/SKILL.md`
2. `plugins/cc10x/agents/*.md`
3. `plugins/cc10x/hooks/hooks.json`
4. `plugins/cc10x/scripts/cc10x_harness_audit.py`
5. `plugins/cc10x/scripts/cc10x_workflow_replay_check.py`
6. `docs/router-invariants.md`
7. `docs/cc10x-orchestration-bible.md`
8. this document

## Do Not Break These

### 1. Router-owned orchestration
Workers may emit intent, but only the router owns:
- task creation
- task blocking/unblocking
- remediation creation
- workflow advancement
- memory finalization

### 2. Workflow-scoped metadata
Every child task must remain scoped by:
- `wf`
- `kind`
- `origin`
- `phase`
- `plan`
- `scope`
- `reason`

### 3. Workflow artifact durability
Every workflow must keep:
- `.claude/cc10x/v10/workflows/{wf}.json`
- `.claude/cc10x/v10/workflows/{wf}.events.jsonl`

If those drift, resume and hook context degrade immediately.

### 4. Fail-closed evidence
Do not weaken:
- builder scenario evidence
- investigator regression/variant evidence
- verifier scenario reconciliation
- convergence-state stopping behavior

### 5. Hooks stay small
Hooks are allowed to:
- guard
- audit
- inject context

Hooks are not allowed to become:
- a second orchestrator
- a hidden task system
- a replacement for router logic

## Required Checks Before Any Orchestration Change

Run all of these:

```bash
python3 plugins/cc10x/scripts/cc10x_harness_audit.py
python3 plugins/cc10x/scripts/cc10x_workflow_replay_check.py
python3 -m py_compile plugins/cc10x/scripts/*.py
git diff --check
```

If the change touches plugin metadata or docs, also verify:
- `plugins/cc10x/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `README.md`
- `CHANGELOG.md`
- optional MCP instructions still clearly state the expected Claude Code server names: `brightdata`, `octocode`

## When A Change Is Unsafe

Treat the change as unsafe until proven otherwise if it:
- changes task metadata shape
- changes workflow artifact keys
- changes router contract rules
- changes hook events or hook file names
- changes any remediation or re-review behavior
- changes how scenario evidence is validated

In those cases, update:
- replay fixtures
- harness audit
- invariant registry

in the same change.

## Safe Improvement Pattern

The preferred order for future improvements:
1. make behavior explicit in the router
2. add replay coverage
3. add audit coverage
4. update invariants
5. update bible/logic docs

This keeps the plugin understandable and prevents silent drift.
