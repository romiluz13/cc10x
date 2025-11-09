---
name: parallel-agent-dispatch
description: Use when facing 3+ independent failures that can be investigated without shared state or dependencies - orchestrator dispatches multiple bug-investigator subagents to investigate and fix independent problems concurrently
---

# Parallel Agent Dispatch - Orchestrator-Driven

## Overview

When you have multiple unrelated failures (different test files, different subsystems, different bugs), investigating them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** Orchestrator dispatches one bug-investigator subagent per independent problem domain. Let them work concurrently.

**Integration with cc10x**: This skill is used by the DEBUG workflow orchestrator to coordinate parallel subagent dispatch for independent bugs.

## When to Use

**Use when:**

- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations
- No dependencies between bugs

**Don't use when:**

- Failures are related (fix one might fix others)
- Need to understand full system state
- Bugs share files or resources
- Bugs have dependencies (fixing one requires fixing another first)

## Independence Detection

**Orchestrator analyzes bugs for independence:**

1. **File Overlap Check**: Do bugs touch different files?
   - Different files → Likely independent
   - Same files → Check further

2. **Resource Overlap Check**: Do bugs use different resources?
   - Different databases, APIs, services → Likely independent
   - Same resources → Check further

3. **Dependency Check**: Does fixing one bug require fixing another?
   - No dependencies → Independent
   - Has dependencies → Sequential required

4. **State Check**: Do bugs modify shared state?
   - No shared state → Independent
   - Shared state → Sequential required

**Decision Logic**:

- All checks pass → Independent → Parallel dispatch
- Any check fails → Dependent → Sequential execution

## The Pattern

### 1. Identify Independent Domains

Group failures by what's broken:

- File A tests: Tool approval flow
- File B tests: Batch completion behavior
- File C tests: Abort functionality

Each domain is independent - fixing tool approval doesn't affect abort tests.

### 2. Create Focused Subagent Tasks

Each bug-investigator subagent gets:

- **Specific scope:** One test file or subsystem
- **Clear goal:** Make these tests pass
- **Constraints:** Don't change other code
- **Expected output:** Summary of what you found and fixed

### 3. Orchestrator Dispatches in Parallel

**Orchestrator coordinates**:

- Dispatch bug-investigator subagent for each independent bug
- All subagents run concurrently
- Orchestrator tracks progress for each subagent
- Orchestrator waits for all to complete

**Example**:

```
Orchestrator detects 3 independent bugs:
- Bug 1: agent-tool-abort.test.ts failures
- Bug 2: batch-completion-behavior.test.ts failures
- Bug 3: tool-approval-race-conditions.test.ts failures

Orchestrator dispatches:
- bug-investigator → Bug 1 (parallel)
- bug-investigator → Bug 2 (parallel)
- bug-investigator → Bug 3 (parallel)

All three run concurrently, orchestrator coordinates.
```

### 4. Review and Integrate

When subagents return:

- Orchestrator collects summaries from all subagents
- Verify fixes don't conflict
- Run full test suite
- Integrate all changes

## Subagent Prompt Structure

Good subagent prompts are:

1. **Focused** - One clear problem domain
2. **Self-contained** - All context needed to understand the problem
3. **Specific about output** - What should the subagent return?

**Example**:

```
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" - expects 'interrupted at' in message
2. "should handle mixed completed and aborted tools" - fast tool aborted instead of completed
3. "should properly track pendingToolCount" - expects 3 results but gets 0

These are timing/race condition issues. Your task:

1. Read the test file and understand what each test verifies
2. Identify root cause - timing issues or actual bugs?
3. Fix by:
   - Replacing arbitrary timeouts with event-based waiting
   - Fixing bugs in abort implementation if found
   - Adjusting test expectations if testing changed behavior

Do NOT just increase timeouts - find the real issue.

Return: Summary of what you found and what you fixed.
```

## Common Mistakes

**❌ Too broad:** "Fix all the tests" - subagent gets lost
**✅ Specific:** "Fix agent-tool-abort.test.ts" - focused scope

**❌ No context:** "Fix the race condition" - subagent doesn't know where
**✅ Context:** Paste the error messages and test names

**❌ No constraints:** Subagent might refactor everything
**✅ Constraints:** "Do NOT change production code" or "Fix tests only"

**❌ Vague output:** "Fix it" - you don't know what changed
**✅ Specific:** "Return summary of root cause and changes"

## When NOT to Use

**Related failures:** Fixing one might fix others - investigate together first
**Need full context:** Understanding requires seeing entire system
**Exploratory debugging:** You don't know what's broken yet
**Shared state:** Subagents would interfere (editing same files, using same resources)
**Dependencies:** Fixing one bug requires fixing another first

## Integration with DEBUG Workflow

**Orchestrator Integration**:

1. **Bug Classification**: DEBUG workflow classifies bugs (reproducible/intermittent/independent)
2. **Independence Analysis**: Orchestrator analyzes bugs for independence using this skill
3. **Parallel Dispatch**: If independent → Orchestrator dispatches bug-investigator subagents in parallel
4. **Sequential Fallback**: If dependent → Orchestrator executes sequentially (existing behavior)
5. **Coordination**: Orchestrator tracks all subagents, collects results, verifies no conflicts

**Workflow**:

```
DEBUG Workflow:
├─ Phase 1: Bug Classification
├─ Phase 2: Independence Analysis (uses this skill)
│   ├─ Independent? → Parallel dispatch
│   └─ Dependent? → Sequential execution
├─ Phase 3: Subagent Coordination
│   ├─ Parallel: Orchestrator dispatches multiple bug-investigator subagents
│   └─ Sequential: Orchestrator dispatches bug-investigator subagent one at a time
└─ Phase 4: Integration and Verification
```

## Key Benefits

1. **Parallelization** - Multiple investigations happen simultaneously
2. **Focus** - Each subagent has narrow scope, less context to track
3. **Independence** - Subagents don't interfere with each other
4. **Speed** - 3 problems solved in time of 1
5. **Orchestrator Coordination** - Centralized management of parallel execution

## Verification

After subagents return:

1. **Review each summary** - Understand what changed
2. **Check for conflicts** - Did subagents edit same code?
3. **Run full suite** - Verify all fixes work together
4. **Spot check** - Subagents can make systematic errors

## Real-World Impact

From debugging sessions:

- 6 failures across 3 files
- 3 bug-investigator subagents dispatched in parallel
- All investigations completed concurrently
- All fixes integrated successfully
- Zero conflicts between subagent changes

## Summary

**For Orchestrator**:

- Analyze bugs for independence
- If independent → Dispatch bug-investigator subagents in parallel
- If dependent → Execute sequentially
- Coordinate all subagents, collect results, verify no conflicts

**For Subagents**:

- Focus on one problem domain
- Work independently
- Return summary of findings and fixes

**Result**: Faster debugging for multiple independent bugs, orchestrator manages coordination.
