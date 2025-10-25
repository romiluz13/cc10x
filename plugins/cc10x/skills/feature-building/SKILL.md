---
name: feature-building
description: Complete feature implementation workflow orchestrating 5-phase development with context analysis, implementation planning, TDD-enforced sequential development with risk analysis before each increment, multi-dimensional verification, and finalization. Use when building complete features from start to finish with strict test-first methodology. Provides guidance on breaking features into increments under 200 lines each, implementing with RED-GREEN-REFACTOR cycles, file manifest verification, and mandatory test verification. Loaded by implementer and tdd-enforcer agents during BUILDING workflow. Integrates with risk-analysis skill to identify edge cases before each increment. Critical for complex features requiring systematic TDD discipline and comprehensive quality gates.
license: MIT
---

# Feature Building - Complete Implementation Workflow

## Overview

Orchestrate complete feature development from planning to production-ready code. Coordinates sub-agents and automatically invokes domain skills.

**Core principle:** Test-first, quality gates between phases, sequential implementation to prevent conflicts.

**Announce at start:** "I'm using the feature-building skill to implement this feature."

**💡 Pro Tip**: For complex features, use PLANNING workflow (via master orchestrator or /cc10x plan) FIRST to create a comprehensive plan, then implement from that plan.

## Task Tracking Approach

**Simple task tracking optimized for implementation workflow**:

### When You Have a Plan

If PLANNING workflow created a comprehensive plan (`.claude/plans/FEATURE_[NAME].md`):

1. **Load plan** to reference architecture decisions and file manifest
2. **Track current increment** with TodoWrite tool (5-10 active tasks)
3. **Update after each increment** - mark complete, load next increment tasks
4. **Reference plan** for architecture, risks, manifest throughout implementation

**Example workflow**:
```
# User ran PLANNING workflow: "Plan authentication feature"
# Created: .claude/plans/FEATURE_AUTH.md

# Now in BUILDING workflow
# Step 1: Load plan to understand architecture and increments
# Step 2: Create TodoWrite tasks for Increment 1 (5-7 tasks)
# Step 3: Implement Increment 1, mark tasks complete
# Step 4: Load Increment 2 tasks, repeat
```

### When Building Without Plan

If building directly (smaller features):

1. **Create tasks in Phase 2** (Planning phase breaks feature into increments)
2. **Track with TodoWrite** (5-10 tasks for current increment)
3. **Update as you progress** through increments
4. **No persistent plan needed** (ad-hoc implementation)

**Benefits:**
- ✅ Simple tracking (TodoWrite for current work)
- ✅ Reference plan for architecture (if exists)
- ✅ Increment-focused (5-10 tasks at a time)
- ✅ No complex dual-tracking system

## Workflow Overview

```
Phase 1: Context Analysis (parallel, read-only)
    ↓
Phase 2: Planning (sequential, with architecture decisions)
    ↓
Phase 3: Implementation (sequential, TDD enforced)
    ↓
Phase 4: Verification (quality gates)
    ↓
Phase 5: Finalization (commit, docs)
```

## Parallel Execution Rules ⚡

**Critical for preventing file conflicts and maximizing speed**:

| Phase | Max Parallel Agents | Reasoning |
|-------|-------------------|-----------|
| Phase 1 (Context) | **1 agent** | Single codebase, sequential analysis faster |
| Phase 2 (Planning) | **0 agents** | Orchestrator handles (no sub-agents) |
| Phase 3 (Implementation) | **1 agent** ⚠️ | NEVER parallelize implementers = file conflicts |
| Phase 4 (Verification) | **2-3 agents** ✅ | Read-only reviews safe to parallelize |
| Phase 5 (Finalization) | **0 agents** | Orchestrator handles (no sub-agents) |

### Why Never Parallelize Implementers? ⚠️

```
❌ BAD (Will cause merge conflicts):
Parallel {
  Implementer A → Edits src/auth/auth.service.ts
  Implementer B → Edits src/auth/auth.service.ts  // CONFLICT!
}

✅ GOOD (Sequential, safe):
Sequential {
  Implementer A → Edits src/auth/auth.service.ts → Complete
  Implementer B → Edits src/middleware/auth.ts → Complete
}
```

**Even different files can conflict** if they import each other or share dependencies.

**The Rule**: ONE implementer at a time, always sequential.

## Phase 1: Context Analysis

**Objective**: Gather all relevant context before implementation begins

**Duration**: ~2-3 minutes

**Sub-Agents**: Launch context-analyzer (read-only, safe)

```markdown
Task for context-analyzer:

Analyze the codebase for implementing: {feature-description}

Provide:
1. Similar existing features (for pattern reference)
2. Project conventions (naming, structure, errors, testing)
3. Dependencies needed (database, services, utilities)
4. Integration points (APIs, database, external services)
5. Recommended file locations and structure

Generate a comprehensive context report.
```

**Output**: Context Analysis Report
- Location for new files
- Patterns to follow
- Dependencies to use
- Integration points
- Reference implementations

**Quality Gate**:
- ✅ At least 1 similar feature found for reference
- ✅ Clear patterns documented
- ✅ All dependencies identified
- ✅ Integration points located
- ❌ If no similar features found → Proceed with caution, follow closest pattern

## Phase 2: Planning with Architecture

**Objective**: Create implementation plan with architecture decisions

**Duration**: ~3-5 minutes

**Responsibility**: Main agent (you) plans based on context

**Planning Steps**:

1. **Review Context Report**: Read findings from context-analyzer

2. **Architecture Decisions**:
   ```
   Architecture for {feature-description}:

   Location:
   - Files will be created in: [path based on context]
   - Follow pattern: [pattern from context]

   Design:
   - Data model: [if database changes needed]
   - API contract: [if API endpoints]
   - Dependencies: [list from context analysis]
   - Integration: [how it connects to existing code]

   Patterns to follow:
   - Naming: [from context]
   - Structure: [from context]
   - Error handling: [from context]
   - Testing: [from context]
   ```

3. **Implementation Plan**:
   ```
   Implementation Steps:

   Step 1: [High-level task]
   - Files: [specific files]
   - Dependencies: [what's needed]
   - Estimated time: [15-30 min]

   Step 2: [High-level task]
   - Files: [specific files]
   - Dependencies: [what's needed]
   - Estimated time: [15-30 min]

   [Continue with 3-6 steps total]
   ```

4. **Create Task List**:

   **If persistent checklist exists** (from `/feature-plan`):
   ```
   1. Read .claude/docs/checklist-[feature-name].md
   2. Identify current phase tasks
   3. Copy 5-10 tasks from current phase to TodoWrite tool
   4. Reference persistent checklist for dependencies and acceptance criteria
   ```

   **If no persistent checklist** (standalone feature):
   ```
   Use TodoWrite tool to create tasks:
   - [ ] Step 1: [Description] (depends on: none)
   - [ ] Step 2: [Description] (depends on: Step 1)
   - [ ] Step 3: [Description] (depends on: Step 1, can parallelize with Step 2)
   ...
   ```

**Quality Gate**:
- ✅ Architecture decisions documented
- ✅ Implementation plan has 3-6 clear steps
- ✅ Each step is 15-30 minutes
- ✅ Dependencies are identified
- ✅ Tasks loaded to TodoWrite tool (from persistent checklist OR created new)
- ❌ If plan is unclear → Ask clarifying questions before proceeding

## Phase 3: Implementation with TDD

**Objective**: Implement the feature using strict TDD methodology

**Duration**: Variable (depends on complexity)

**Sub-Agents**: Launch implementer for each major task (NEVER parallelize implementers!)

**Critical Rule**: ⚠️ **NEVER parallelize multiple implementer sub-agents** - they will edit the same files and cause conflicts

**For each TODO task**:

```markdown
Task for implementer:

Implement: [specific task from TODO list]

Context:
- Follow patterns from: [reference feature from context analysis]
- Use dependencies: [specific dependencies identified]
- Location: [specific file path]
- Testing pattern: [from context analysis]

Requirements:
1. Write failing test FIRST (RED)
2. Verify test fails correctly
3. Implement minimal code (GREEN)
4. Verify test passes
5. Refactor while keeping tests green
6. Run all tests (ensure no regressions)
7. Verify quality before completing

Auto-invoked skills:
- test-driven-development (TDD enforcement)
- code-generation (clean code patterns)
- ui-design ⭐ (Lovable/Bolt-quality beautiful UIs for frontend)
- verification-before-completion (quality gates)
```

**Between tasks**:
1. Mark current task as completed in TODO list
2. Review implementer's output
3. Verify tests pass
4. Move to next task

**Quality Gate (after each task)**:
- ✅ Failing test was written first
- ✅ Test failure was verified
- ✅ Implementation makes test pass
- ✅ All tests pass (including existing tests)
- ✅ No console.logs or debug code
- ✅ Error handling present
- ✅ Code follows project patterns
- ❌ If quality gate fails → Fix before moving to next task

## Phase 4: Verification

**Objective**: Ensure feature is production-ready

**Duration**: ~2-3 minutes

**Responsibility**: Main agent (you)

**Verification Checklist**:

```
Production Ready:
- [ ] All tests pass
- [ ] No errors or warnings in output
- [ ] Code follows project conventions
- [ ] No debug code (console.log, debugger, TODO, FIXME)
- [ ] Error handling present for all failure paths
- [ ] Edge cases covered in tests
- [ ] Files properly organized
- [ ] No file conflicts (git status clean)
- [ ] Integration points working (if applicable)
```

**Run verification**:
```bash
# Run all tests
npm test
# or appropriate test command

# Check for debug code
grep -r "console.log\|debugger\|TODO\|FIXME" src/ --include="*.ts" --include="*.js"

# Check git status
git status
```

**Quality Gate**:
- ✅ All checklist items pass
- ❌ If any item fails → Back to Phase 3, fix issues

## Phase 5: Finalization

**Objective**: Commit work and prepare for next task

**Duration**: ~1-2 minutes

**Responsibility**: Main agent (you)

**Finalization Steps**:

1. **Generate commit message**:
   ```bash
   git add [files]

   git commit -m "feat: [feature description]

   - [Key change 1]
   - [Key change 2]
   - [Key change 3]

   Tests:
   - [X new tests added]
   - All tests passing

   🤖 Generated with Claude Code (cc10x)

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

2. **Update documentation** (if needed):
   - Update README if public API changed
   - Update CHANGELOG if maintaining one
   - Add migration notes if breaking changes

3. **Update task tracking**:

   **If persistent checklist exists**:
   ```
   1. Mark all TodoWrite tasks as completed
   2. Update persistent checklist (.claude/docs/checklist-[feature-name].md):
      - Check off completed tasks in current phase
      - Update progress dashboard (completed count, percentage)
      - Add any notes or discoveries in Implementation Notes section
   3. Clear TodoWrite for next session
   ```

   **If no persistent checklist** (standalone feature):
   ```
   Use TodoWrite to archive completed tasks:
   - Move completed todos to "archived" status
   - Remove from active list
   ```

4. **Summary Report**:
   ```markdown
   ## Feature Implementation Complete: [Feature Name]

   ### What Changed
   - [High-level description]

   ### Files Created/Modified
   - src/path/to/file.ts (created)
   - src/path/to/other.ts (modified)

   ### Tests
   - X new tests added
   - All tests passing (Y total)

   ### Next Steps
   - [Optional: Suggested follow-up work]

   Ready for review/merge.
   ```

**Quality Gate**:
- ✅ Work is committed with semantic message
- ✅ TODO list is clean
- ✅ Summary report provided
- ✅ Ready for next task

## Error Handling

### If Context Analysis Fails
```
Problem: No similar features found, patterns unclear
Solution: Use closest available pattern, proceed cautiously, ask user for guidance if needed
```

### If Planning is Unclear
```
Problem: Requirements ambiguous, multiple approaches possible
Solution: Ask user clarifying questions before implementation
```

### If Implementation Fails
```
Problem: Tests failing, errors occurring, blocked
Solution:
1. Review error messages carefully
2. Check context analysis - are we following correct patterns?
3. Verify dependencies are available
4. Ask user for help if blocked
5. Don't proceed until issue resolved
```

### If Quality Gate Fails
```
Problem: Verification checklist has failures
Solution: Back to Phase 3, fix issues, re-verify
```

## Orchestration Rules

### ✅ DO

- ✅ Run context-analyzer FIRST (always)
- ✅ Create detailed plan BEFORE coding
- ✅ Use implementer sub-agent for ALL implementation work
- ✅ Enforce TDD strictly (test-first, no exceptions)
- ✅ Verify quality between tasks
- ✅ Follow patterns found in context analysis
- ✅ Update TODO list as you progress

### ❌ DON'T

- ❌ Skip context analysis (never guess patterns)
- ❌ Start coding without a plan
- ❌ Parallelize multiple implementers (file conflicts!)
- ❌ Write code without tests first
- ❌ Ignore quality gate failures
- ❌ Introduce new patterns without reason
- ❌ Leave work uncommitted

## Example Workflow

**User**: `/feature-build Add user profile API endpoints`

**Phase 1 - Context Analysis (2 min)**:
```
Launching context-analyzer...

✅ Context Analysis Complete:
- Found reference: Orders API (src/features/orders/)
- Pattern: Express routes + service layer + Prisma
- Location: Create src/features/profile/
- Dependencies: Database, Logger, Auth middleware
- Integration: Register in src/api/routes.ts
```

**Phase 2 - Planning (3 min)**:
```
Architecture:
- Location: src/features/profile/
- Files: profile.service.ts, profile.controller.ts, profile.types.ts, profile.test.ts
- Pattern: Follow orders feature structure exactly
- Database: Use existing User model

Plan:
1. Create profile service with getProfile, updateProfile methods (20 min)
2. Create profile controller with GET /profile, PUT /profile routes (15 min)
3. Register routes and add auth middleware (10 min)

TODO list created with 3 tasks.
```

**Phase 3 - Implementation (45 min)**:
```
Task 1: Create profile service
Launching implementer...
✅ Tests written and passing
✅ Service implemented with error handling
✅ All existing tests still pass

Task 2: Create profile controller
Launching implementer...
✅ Tests written and passing
✅ Controller implemented following pattern
✅ Validation added

Task 3: Register routes
Launching implementer...
✅ Routes registered
✅ Auth middleware applied
✅ Integration tests passing
```

**Phase 4 - Verification (2 min)**:
```
Running verification...
✅ All tests pass (15 new tests, 87 total)
✅ No debug code found
✅ Code follows project patterns
✅ Error handling present
✅ Git status clean
```

**Phase 5 - Finalization (1 min)**:
```
Committing work...
✅ Committed: "feat: add user profile API endpoints"
✅ TODO list cleaned
✅ Summary report generated

Feature Implementation Complete: User Profile API

Files Created:
- src/features/profile/profile.service.ts
- src/features/profile/profile.controller.ts
- src/features/profile/profile.types.ts
- src/features/profile/profile.test.ts

Tests: 15 new tests, all passing (87 total)

Ready for review.
```

**Total time: 53 minutes**

## Success Metrics

**This workflow succeeds when**:
- ✅ Feature works correctly
- ✅ All tests pass
- ✅ Code follows existing patterns
- ✅ No file conflicts
- ✅ Clean commit history
- ✅ Ready for production

**This workflow fails when**:
- ❌ Skipped context analysis → inconsistent code
- ❌ Skipped planning → unclear implementation
- ❌ Skipped TDD → untested code
- ❌ Skipped verification → bugs in production
- ❌ Parallelized implementers → file conflicts

## Remember

**The orchestration pattern is**:
```
Context (parallel read)
    → Plan (sequential think)
        → Implement (sequential write, TDD)
            → Verify (quality gates)
                → Finalize (commit)
```

**This pattern achieves**:
- 🎯 Consistent code (follows patterns)
- 🎯 High quality (TDD + verification)
- 🎯 No conflicts (sequential implementation)
- 🎯 Fast execution (parallel context gathering)
- 🎯 Predictable results (same workflow every time)

**Never skip phases. Never parallelize implementers. Always follow TDD. Always verify quality.**
