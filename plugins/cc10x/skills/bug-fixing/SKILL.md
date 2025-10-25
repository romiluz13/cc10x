---
name: bug-fixing
description: Complete bug-fixing workflow using LOG FIRST pattern to prevent assumption-driven debugging that wastes hours. Always verify runtime data by adding comprehensive logging BEFORE making fixes, then fix based on observed data rather than assumptions. Use when debugging issues where root cause is unclear, fixing bugs in production systems, investigating test failures, resolving unexpected behavior, or troubleshooting integration problems. Prevents wasting time on random fix attempts by forcing systematic investigation. Loaded by tdd-enforcer agent during DEBUGGING workflow or master orchestrator skill when bug-fixing tasks detected.
license: MIT
---

# Bug Fixing - Systematic Debugging Workflow

## Overview

Fast, focused bug fixes using LOG FIRST pattern and progressive context loading. Prevents wasting hours on assumptions by seeing actual data first.

**Core principle:** "LOG FIRST, FIX LATER" - Add comprehensive logging to see actual data structures before attempting fixes.

**Announce at start:** "I'm using the bug-fixing skill to debug and fix this issue."

## Task Tracking for Bug Fixes

Bug fixes are **lightweight workflows** (12-17 minutes) and typically don't need persistent checklists or TodoWrite tool tracking.

**When to use TodoWrite**:
- ✅ Complex bug with multiple fixes needed (use TodoWrite for 3-5 tasks)
- ✅ Bug fix spans multiple sessions
- ❌ Simple, single-session bug fix (no tracking needed)

**Why minimal tracking**:
- Bug fixes are quick (12-17 min)
- Clear workflow phases (investigate → fix → verify)
- Real-time progress visible through workflow phases
- No need for persistent tracking across sessions

**Example TodoWrite usage** (complex bug only):
```
- [ ] Phase 2: Add comprehensive logging (2-3 min)
- [ ] Phase 3: Analyze logs and identify root cause (3-5 min)
- [ ] Phase 4: Implement fix with failing test first (5-7 min)
- [ ] Phase 5: Verify fix and run regression tests (2-3 min)
```

## Bug Classification (Choose Your Approach)

**Before starting, classify the bug to choose the right workflow:**

### Type 1: Obvious Bug (5-15 min) - Just Fix It!

**Symptoms:**
- Typo in code (e.g., `utills` instead of `utils`)
- Syntax error (missing semicolon, bracket)
- Missing import statement
- Off-by-one error (loop boundary)
- Obvious logic error

**Approach:** Skip LOG FIRST, just fix it directly

**Example:** "Cannot find module './utills'" → Fix typo to './utils'

**When to use:** Root cause is immediately visible in error message

---

### Type 2: Unclear Bug (12-25 min) - Use LOG FIRST ⭐

**Symptoms:**
- "Feature not working" (vague)
- Data not appearing as expected
- Integration issues (third-party APIs)
- Unexpected behavior (no clear error)

**Approach:** Full LOG FIRST workflow (this skill!)

**Example:** "Login not working" → Log req.body, discover it's undefined, find body parser missing

**When to use:** Root cause not obvious, need to see actual data

---

### Type 3: Complex/Intermittent Bug (1-3 hours) - Full Investigation

**Symptoms:**
- Race conditions (only fails sometimes)
- Intermittent failures (works locally, fails in production)
- Memory leaks (slow degradation over time)
- Concurrency issues

**Approach:** Extended LOG FIRST + profiling + monitoring

**Example:** "Users randomly get logged out" → Investigate session management, token expiry, race conditions

**When to use:** Bug is complex or doesn't reproduce consistently

---

**Quick Decision Guide:**
- Can you see the problem in error message? → Type 1 (just fix)
- Need to see what data looks like? → Type 2 (LOG FIRST - this skill!)
- Intermittent or complex investigation? → Type 3 (full debugging)

**Most bugs are Type 2** - this is where LOG FIRST shines!

---

## Workflow Overview

```
Phase 1: Minimal Context (error logs only)
    ↓
Phase 2: Investigation (LOG FIRST ⭐ → parallel analysis)
    ↓
Phase 3: Root Cause (systematic debugging)
    ↓
Phase 4: Fix (TDD: test → implement)
    ↓
Phase 5: Verify (regression testing)
```

**Estimated Time**: 12-17 minutes (includes comprehensive logging)
**Estimated Tokens**: ~58k (vs 160k for feature-build)

**Key Innovation**: Phase 2 now enforces "LOG FIRST, FIX LATER" pattern to prevent wasting hours on assumption-driven debugging ⭐

## Parallel Execution Rules ⚡

| Phase | Max Parallel Agents | Reasoning |
|-------|-------------------|-----------|
| Phase 1 (Context) | **1 agent** | Load minimal error context only |
| Phase 2.1 (Logging) ⭐ | **0 agents** | Orchestrator adds comprehensive logging first |
| Phase 2.2 (Investigation) | **2 agents** ✅ | Parallel analysis (logs + code) safe - ONLY after logging |
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

## Phase 2: Investigation (ENHANCED with Systematic Debugging) ⭐

**Objective**: Identify where the bug occurs

**Duration**: ~5-7 minutes (includes comprehensive logging)

**CRITICAL**: Follow "LOG FIRST, FIX LATER" pattern to avoid wasting hours on assumptions

### Step 1: Add Comprehensive Logging FIRST ⭐ (2-3 minutes)

**Before analyzing or attempting any fixes, add comprehensive logging to see ACTUAL data:**

```markdown
[Comprehensive Logging Phase - MANDATORY]

Based on bug type, add logging:

For Third-Party Integration Bugs (Clerk, Stripe, Auth0, etc.):
```typescript
// Log COMPLETE response structure
console.log("=== THIRD-PARTY DEBUG ===");
console.log("FULL response:", JSON.stringify(response, null, 2));
console.log("FULL user object:", JSON.stringify(user, null, 2));
console.log("FULL sessionClaims:", JSON.stringify(sessionClaims, null, 2));
console.log("=== END DEBUG ===");
```

For Authentication Bugs:
```typescript
// Log ALL auth-related data
console.log("=== AUTH DEBUG ===");
console.log("FULL sessionClaims:", JSON.stringify(auth.sessionClaims, null, 2));
console.log("ALL cookies:", JSON.stringify(req.cookies, null, 2));
console.log("Authorization header:", req.headers.authorization);
console.log("User ID:", user?.id);
console.log("Session ID:", session?.id);
console.log("=== END DEBUG ===");
```

For API Bugs:
```typescript
// Log complete request/response
console.log("=== API DEBUG ===");
console.log("Request:", JSON.stringify({ method, url, headers, body }, null, 2));
console.log("Response:", JSON.stringify({ status, headers, data }, null, 2));
console.log("Error:", JSON.stringify(error, Object.getOwnPropertyNames(error), 2));
console.log("=== END DEBUG ===");
```

For Data Flow Bugs:
```typescript
// Log at every transformation step
console.log("=== DATA FLOW DEBUG ===");
console.log("INPUT:", JSON.stringify(input, null, 2));
console.log("AFTER VALIDATION:", JSON.stringify(validated, null, 2));
console.log("AFTER TRANSFORM:", JSON.stringify(transformed, null, 2));
console.log("OUTPUT:", JSON.stringify(output, null, 2));
console.log("=== END DEBUG ===");
```

**Action**: Add appropriate logging, run code, capture complete logs
**Share logs with user**: Show actual data structures before proceeding
```

**Quality Gate (MANDATORY)**:
- ✅ Can see the ACTUAL data structures? (not assumptions)
- ✅ Have verified field names? (docs often lie)
- ✅ Can see what third-party service REALLY returns?
- ❌ If NO to any → Add more logging, don't proceed

**Red Flags** (means you MUST add logging NOW):
- ⚠️ Third-party integration not behaving as expected
- ⚠️ Authentication/authorization issues
- ⚠️ Data not appearing where it should
- ⚠️ Dashboard shows data but code doesn't see it
- ⚠️ Tried 2+ fixes without success (you're guessing!)

**The 5-Minute Rule**: If debugging > 30 minutes without seeing actual data → STOP → Add comprehensive logging first

### Step 2: Analyze ACTUAL Data (1-2 minutes)

Now that you have the REAL data from logs:

```markdown
[Data Analysis - Based on Runtime Logs]

From logs, identify:
1. Actual field names (compare to docs - they often differ!)
   - Docs said: _______________
   - Logs show: _______________

2. Actual data structure (nested? flat? different than expected?)

3. Actual values (null? undefined? wrong type?)

4. Common mismatches:
   - Dashboard UI field names ≠ API response field names
   - Documentation version ≠ Your API version
   - Example code ≠ Production behavior
```

### Step 3: Parallel Investigation (Only After Logging) ⭐ (2 minutes)

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
- systematic-debugging ⭐ (LOG FIRST pattern, prevents assumption-driven debugging)
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
- ✅ LOG FIRST ⭐ (see actual data, not assumptions)
- ✅ Expand progressively (load files as needed)
- ✅ Parallel investigation (2 agents analyze simultaneously)
- ✅ Focused fix (change only what's needed)
- ✅ TDD prevents regressions (test-first always)

**Bug fix workflow is SAFE because**:
- ✅ Comprehensive logging reveals actual data structures
- ✅ Test reproduces bug before fixing
- ✅ Regression testing mandatory
- ✅ Minimal changes (no refactoring)
- ✅ Quality gates enforce standards

**Bug fix workflow is SMART because** ⭐:
- ✅ "LOG FIRST, FIX LATER" prevents wasting hours/days
- ✅ Verifies field names vs docs (they often differ!)
- ✅ Sees what third-party services REALLY return
- ✅ The 5-Minute Rule: If debugging > 30 min without data → ADD LOGGING

**12-17 minutes to fix most bugs. ~58k tokens (vs 160k feature-build).** ⚡

**Real-world impact**: Finds bugs in 5-10 minutes instead of hours/days of assumption-driven debugging.
