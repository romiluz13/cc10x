# cc10x Refactoring Plan

## Executive Summary

cc10x v4.9.0 has **62.5% dead code** (20 of 32 skills are orphaned). The architecture is overly complex with broken skill chaining. This plan proposes radical simplification.

## Current State Analysis

### What Works
- 5 agents (component-builder, code-reviewer, bug-investigator, integration-verifier, planner)
- 12 skills actually used by agents
- Basic TDD workflow concept

### What's Broken
- 20 orphaned skills never invoked
- Workflow skills are empty shells (document dependencies but don't load them)
- Orchestrator is over-engineered (33k+ tokens of instructions that don't execute)
- No actual skill chaining happens
- Redundant skills (design-patterns vs architecture-patterns)

## Proposed Architecture: cc10x v5.0

### Option A: Radical Simplification (Recommended)

**Delete 20 orphaned skills. Keep 12 that work. Simplify orchestrator.**

#### Skills to KEEP (12 → consolidate to 8)

| Keep | Purpose | Notes |
|------|---------|-------|
| `architecture-patterns` | System design, API patterns | Absorb design-patterns |
| `code-generation` | Code writing patterns | Keep |
| `code-review-patterns` | Review checklists | Keep |
| `debugging-patterns` | LOG FIRST, root cause | Keep |
| `frontend-patterns` | UI/UX/A11y patterns | Keep |
| `planning-patterns` | Requirements, roadmaps | Keep |
| `test-driven-development` | RED-GREEN-REFACTOR | Keep |
| `verification-before-completion` | Exit criteria | Keep |

#### Skills to DELETE (20)

| Delete | Reason |
|--------|--------|
| `app-design-generation` | Slash command only, no workflow integration |
| `brainstorming` | Never used |
| `build-process-context` | Never used |
| `build-workflow` | Empty shell, logic should be in orchestrator |
| `cc10x-orchestrator` | Over-engineered, replace with simple router |
| `component-design-patterns` | Merge into frontend-patterns |
| `context-preset-management` | Never used |
| `cursor-rules-generation` | Slash command only |
| `debug-workflow` | Empty shell |
| `deployment-patterns` | Never used in practice |
| `design-patterns` | Redundant with architecture-patterns |
| `memory-tool-integration` | Never used |
| `parallel-agent-dispatch` | Never used |
| `planning-workflow` | Empty shell |
| `project-context-understanding` | Never used |
| `project-structure-generation` | Slash command only |
| `quick-error-fixing` | Never used |
| `review-workflow` | Empty shell |
| `risk-analysis` | Merge into planning-patterns |
| `session-summary` | Never used |
| `skill-authoring` | Never used |
| `skill-discovery` | Never used |
| `tech-stack-generation` | Slash command only |
| `web-fetch-integration` | Never used |

#### New Simple Orchestrator

Replace 33k token orchestrator with ~500 token router:

```markdown
# cc10x Router

## Detect Intent
- "build/implement/create" → BUILD
- "review/audit/check" → REVIEW
- "debug/fix/error" → DEBUG
- "plan/design/architect" → PLAN

## BUILD Flow
1. Invoke component-builder (loads: test-driven-development, code-generation)
2. Invoke code-reviewer (loads: code-review-patterns)
3. Invoke integration-verifier (loads: debugging-patterns)

## REVIEW Flow
1. Invoke code-reviewer (loads: code-review-patterns, frontend-patterns if UI)

## DEBUG Flow
1. Invoke bug-investigator (loads: debugging-patterns, test-driven-development)

## PLAN Flow
1. Invoke planner (loads: planning-patterns, architecture-patterns)
```

### Option B: Fix Everything (Not Recommended)

Wire up all 32 skills properly. This means:
- Add Skill() calls to all 4 workflow skills
- Create triggers for all orphaned skills
- Fix skill chaining throughout

**Problem:** This preserves complexity that doesn't add value.

### Option C: Complete Rewrite (Nuclear Option)

Start fresh with lessons learned:
- 5 agents
- 8 core skills
- Simple orchestrator
- Test-first development

## Recommended Path: Option A

### Phase 1: Delete Dead Code (Day 1)
- [ ] Delete 20 orphaned skill folders
- [ ] Update plugin.json
- [ ] Run tests

### Phase 2: Consolidate Skills (Day 1-2)
- [ ] Merge design-patterns → architecture-patterns
- [ ] Merge component-design-patterns → frontend-patterns
- [ ] Merge risk-analysis → planning-patterns
- [ ] Merge deployment-patterns → architecture-patterns
- [ ] Merge web-fetch-integration → architecture-patterns

### Phase 3: Simplify Orchestrator (Day 2-3)
- [ ] Replace cc10x-orchestrator with simple router (~500 tokens)
- [ ] Delete workflow skill folders (build-workflow, review-workflow, etc.)
- [ ] Move workflow logic into agent instructions

### Phase 4: Test Everything (Day 3)
- [ ] Test BUILD workflow end-to-end
- [ ] Test REVIEW workflow
- [ ] Test DEBUG workflow
- [ ] Test PLAN workflow

### Phase 5: Release v5.0 (Day 4)
- [ ] Update version to 5.0.0
- [ ] Update README with simplified architecture
- [ ] Push to GitHub

## Expected Outcomes

| Metric | Before (v4.9) | After (v5.0) |
|--------|---------------|--------------|
| Total Skills | 32 | 8 |
| Orphaned Skills | 20 (62.5%) | 0 (0%) |
| Orchestrator Size | ~33k tokens | ~500 tokens |
| Agent Count | 5 | 5 |
| Complexity | High | Low |
| Working | Partially | Fully |

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Lose functionality | Keep all 5 agents, only delete unused skills |
| Break existing users | Major version bump (5.0), document changes |
| Over-simplify | Keep 8 core skills that cover all use cases |

## Decision Needed

**Do you want to proceed with Option A (Radical Simplification)?**

This will:
1. Delete 20 orphaned skills
2. Consolidate remaining skills from 12 to 8
3. Replace complex orchestrator with simple router
4. Result in a working, maintainable system
