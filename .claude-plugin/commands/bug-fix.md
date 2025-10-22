---
name: bug-fix
description: Lightweight debugging workflow for quickly identifying and fixing bugs. Progressive context loading (start minimal, load more as needed). Use when fixing errors, bugs, or broken functionality.
---

You are orchestrating a fast, focused bug fix workflow using progressive context loading and systematic debugging.

## Command Usage

```
/bug-fix <error-description>
```

**Examples**:
- `/bug-fix User login returns 500 error`
- `/bug-fix Payment processing fails with invalid token`
- `/bug-fix Dashboard charts not rendering`

## Workflow Overview

```
Phase 1: Minimal Context (error logs only)
    ↓
Phase 2: Investigation (parallel analysis)
    ↓
Phase 3: Root Cause (systematic debugging)
    ↓
Phase 4: Fix (TDD: test → implement)
    ↓
Phase 5: Verify (regression testing)
```

**Estimated Time**: 10-15 minutes
**Estimated Tokens**: ~55k (vs 160k for feature-build)

## Parallel Execution Rules ⚡

| Phase | Max Parallel Agents | Reasoning |
|-------|-------------------|-----------|
| Phase 1 (Context) | **1 agent** | Load minimal error context only |
| Phase 2 (Investigation) | **2 agents** ✅ | Parallel analysis (logs + code) safe |
| Phase 3 (Root Cause) | **0 agents** | Orchestrator analyzes findings |
| Phase 4 (Fix) | **1 agent** ⚠️ | ONE implementer (no parallelization) |
| Phase 5 (Verify) | **0 agents** | Orchestrator runs tests |

## Phase 1: Minimal Context

**Objective**: Load ONLY what's needed (error logs + recent changes)

**Duration**: ~1 minute

**Progressive Loading** - Start minimal, expand as needed:

```markdown
[Minimal Context Load]

Load ONLY:
1. Error logs (last 100 lines)
2. Stack trace (if available)
3. Recent commits (last 10 commits on this branch)

Do NOT load:
❌ Full codebase
❌ All project context
❌ Detailed architecture docs
❌ Full file history

Token budget: ~3k (vs 15k for feature-build Phase 1)
```

**Example**:
```bash
# Load error logs
tail -100 logs/error.log

# Recent commits
git log --oneline -10

# Current branch status
git status
```

**Quality Gate**:
- ✅ Error message captured
- ✅ Stack trace available (or error description clear)
- ✅ Recent changes identified
- ❌ If error unclear → Ask user for more details

## Phase 2: Investigation (Parallel)

**Objective**: Identify where the bug occurs

**Duration**: ~3-4 minutes

**Sub-Agents**: Launch 2 agents in parallel (read-only, safe)

### Agent 1: Error Analysis
```markdown
Task: Analyze error logs and stack trace

Questions to answer:
1. What is the exact error message?
2. When does it occur? (specific conditions)
3. Which file/function throws the error?
4. What are the error parameters/data?

Output: error-analysis.md
```

### Agent 2: Code Tracing
```markdown
Task: Trace code path to error location

Using:
- Stack trace
- Recent commits
- Git blame

Find:
1. Which recent commit might have introduced this?
2. What code changed in that area?
3. What functions are in the execution path?

Output: code-trace.md
```

**Progressive Context Expansion**:

```markdown
[After Phase 2 - NOW load relevant files]

Based on investigation findings:
→ Load ONLY the 2-3 files involved in the error
→ Load ONLY the recent changes to those files
→ Skip everything else

Token expansion: +5k (total ~8k, still efficient)
```

**Quality Gate**:
- ✅ Error location identified (file + line)
- ✅ Potential cause identified
- ✅ Recent changes analyzed
- ❌ If still unclear → Load more context, repeat investigation

## Phase 3: Root Cause Analysis

**Objective**: Understand WHY the bug occurs

**Duration**: ~2 minutes

**Responsibility**: Orchestrator (you) analyzes findings

**Systematic Debugging**:

```markdown
[Root Cause Analysis]

From investigation findings:

1. Error location: [file:line]
2. Error message: [exact message]
3. Recent change: [commit that introduced bug]

Hypothesis:
- What assumption was broken?
- What edge case wasn't handled?
- What validation is missing?

Root cause: [1-2 sentence explanation]
```

**Common Bug Patterns**:

| Pattern | Root Cause | Fix |
|---------|-----------|-----|
| "undefined is not a function" | Missing null check | Add validation |
| "Cannot read property 'x' of undefined" | Async timing issue | Add await or null check |
| "500 Internal Server Error" | Unhandled exception | Add try-catch |
| "ValidationError" | Missing input validation | Add validation schema |
| "404 Not Found" | Route/resource missing | Check routing/database |

**Quality Gate**:
- ✅ Root cause identified and understood
- ✅ Fix approach clear
- ✅ No ambiguity
- ❌ If still uncertain → Ask user for context

## Phase 4: Fix (TDD Enforced)

**Objective**: Fix the bug using test-first approach

**Duration**: ~4-6 minutes

**Sub-Agent**: Launch implementer (ONE agent, sequential)

```markdown
Task for implementer:

Fix bug: [description]

Root cause: [from Phase 3 analysis]
Location: [file:line]
Fix approach: [specific approach]

Requirements:
1. Write FAILING test that reproduces the bug (RED)
2. Verify test fails with the same error
3. Implement minimal fix (GREEN)
4. Verify test passes
5. Run all tests (ensure no regressions)

Auto-invoked skills:
- test-driven-development (TDD enforcement)
- code-generation (clean code patterns)
- verification-before-completion (quality checks)

Context provided:
- Error logs
- Stack trace
- Recent changes
- Affected files only (isolated context)

Fix ONLY the bug. Do not refactor or add features.
```

**TDD for Bug Fixes**:

```typescript
// 1. RED: Write test that reproduces the bug
test('handles null user in login', async () => {
  const result = await login(null);
  expect(result.error).toBe('User required');
});
// → Test FAILS with same error as production

// 2. GREEN: Minimal fix
async function login(user: User) {
  if (!user) {
    return { error: 'User required' };
  }
  // ... rest of function
}
// → Test PASSES

// 3. VERIFY: Run all tests
npm test
// → All tests pass (no regressions)
```

**Quality Gate**:
- ✅ Failing test written (reproduces bug)
- ✅ Test confirmed failing before fix
- ✅ Fix implemented
- ✅ Test now passes
- ✅ All existing tests still pass
- ❌ If tests fail → Fix implementation, don't skip

## Phase 5: Verification & Regression Testing

**Objective**: Ensure bug is fixed and nothing else broke

**Duration**: ~2 minutes

**Responsibility**: Orchestrator (you)

**Verification Steps**:

```bash
# 1. Run full test suite
npm test

# 2. Check for regressions
git diff --stat

# 3. Verify only bug fix (no extra changes)
git diff
```

**Regression Testing**:

```markdown
[Regression Check]

Changed files: [list]
Lines changed: [count]

Verify:
- ✅ Only affected files modified
- ✅ Fix is minimal (not over-engineered)
- ✅ No unrelated changes
- ✅ All tests pass
- ✅ No new warnings or errors
```

**Quality Gate**:
- ✅ Bug is fixed (original error gone)
- ✅ All tests pass
- ✅ No regressions introduced
- ✅ Changes are minimal and focused
- ❌ If regressions found → Fix them before finalizing

## Finalization

**Objective**: Commit fix with clear message

**Commit Message Format**:

```bash
git add [affected files]

git commit -m "fix: [brief description of bug]

- Root cause: [explanation]
- Fix: [what was changed]
- Test: Added regression test

Closes #[issue-number] (if applicable)

🤖 Generated with Claude Code (cc10x)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Example**:
```bash
git commit -m "fix: handle null user in login endpoint

- Root cause: Missing null check before accessing user.email
- Fix: Added validation to return error for null user
- Test: Added regression test for null user case

Closes #142

🤖 Generated with Claude Code (cc10x)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Error Handling

### If Bug Unclear After Phase 2

```markdown
⚠️ Bug location unclear after investigation

Action: Expand context progressively
1. Load more files (related modules)
2. Load more history (last 50 commits)
3. Ask user: "Can you provide steps to reproduce?"

Do NOT: Load entire codebase upfront
```

### If Fix Breaks Tests

```markdown
⚠️ Fix causes test failures

Action: Analyze failures
1. Which tests are failing?
2. Are they related to the fix?
3. Do tests need updating? (if logic changed)
4. Or does fix need adjustment? (if logic should stay same)

Fix appropriately, re-verify.
```

### If Root Cause Uncertain

```markdown
⚠️ Root cause not clear after investigation

Action: Ask user
- "I found the error in [file:line]"
- "It happens when [condition]"
- "Do you know when this started happening?"
- "What changed recently in this area?"

Get more context before fixing blindly.
```

## Progressive Context Loading Example

**Token Efficient Bug Fix**:

```markdown
Phase 1 (Minimal): 3k tokens
- Error logs
- Recent commits
- Git status

Phase 2 (Expand): +5k tokens (total 8k)
- Affected files only (2-3 files)
- Recent changes to those files

Phase 3-5 (Focused): +2k tokens (total 10k)
- Test files
- Related dependencies

Total: ~10k tokens for bug fix (vs 55k if loaded everything upfront)
Token savings: 82% 🎯
```

## Complete Example

```markdown
User: "/bug-fix User login returns 500 error"

[Phase 1: Minimal Context] (1m)
Loading error logs...
✅ Error: "Cannot read property 'email' of null"
✅ Stack trace: login.ts:45
✅ Recent commit: "Add email validation" (2 hours ago)

[Phase 2: Investigation - Parallel] (3m)
Agent 1 (Error Analysis):
- Error occurs when user object is null
- Happens during email validation
- Line 45 accesses user.email without null check

Agent 2 (Code Trace):
- Recent commit added email validation
- Change: Added user.email.toLowerCase()
- Didn't check if user exists first

✅ Investigation complete. Loading affected files...

[Phase 3: Root Cause] (2m)
Root cause: Recent email validation doesn't check for null user
Location: src/auth/login.ts:45
Fix: Add null check before accessing user.email

[Phase 4: Fix - TDD] (5m)
Launching implementer...
→ Writing failing test for null user
→ Test fails with same 500 error ✅
→ Adding null check: if (!user) return error
→ Test passes ✅
→ All tests passing ✅

[Phase 5: Verification] (2m)
Running full test suite...
✅ All 87 tests passing
✅ No regressions
✅ Only login.ts modified (7 lines changed)

[Finalization]
Committed: "fix: handle null user in login endpoint"

✅ Bug Fixed (13 minutes, ~12k tokens)
```

## Remember

**Bug fix workflow is FAST because**:
- ✅ Start minimal (error logs only)
- ✅ Expand progressively (load files as needed)
- ✅ Parallel investigation (2 agents analyze simultaneously)
- ✅ Focused fix (change only what's needed)
- ✅ TDD prevents regressions (test-first always)

**Bug fix workflow is SAFE because**:
- ✅ Test reproduces bug before fixing
- ✅ Regression testing mandatory
- ✅ Minimal changes (no refactoring)
- ✅ Quality gates enforce standards

**10-15 minutes to fix most bugs. ~55k tokens (vs 160k feature-build).** ⚡
