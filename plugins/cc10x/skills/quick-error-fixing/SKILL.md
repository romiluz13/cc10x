---
name: quick-error-fixing
description: Use when user request contains single clear error message from bash output with obvious fix (syntax error, missing import, typo, type mismatch) - quickly fixes simple errors without full DEBUG workflow
---

# Quick Error Fixing

## Overview

Quickly fix simple, obvious errors from bash output without invoking the full DEBUG workflow. This skill handles single-file errors with clear, actionable fixes.

## Quick Start

Fix simple errors quickly without full debug workflow.

**Example:**

1. **Detect error**: Single syntax error in bash output: "Missing semicolon at line 45"
2. **Identify fix**: Add semicolon at line 45
3. **Apply fix**: Make minimal change
4. **Verify**: Check syntax correct, no new errors

**Result:** Simple error fixed quickly, no workflow needed.

## When to Use

- User request contains bash output or error messages
- Error count == 1 (single error)
- Error message is clear and actionable
- Fix is obvious (syntax error, missing import, typo, etc.)

## When NOT to Use

- Multiple errors (use DEBUG workflow)
- Complex errors requiring investigation (use DEBUG workflow)
- Cross-file errors (use DEBUG workflow)
- Intermittent errors (use DEBUG workflow)
- Errors requiring architectural changes (use DEBUG workflow)

## Quick Fix Criteria

**Use this skill for:**

- **Syntax errors:** Missing semicolon, bracket, parenthesis, etc.
- **Import errors:** Missing import statement, wrong import path
- **Type errors:** Simple type mismatches (string vs number, etc.)
- **Typo errors:** Variable name typos, function name typos
- **Single file errors:** Errors contained within one file

**Don't use for:**

- Multiple errors across files
- Complex logic errors
- Performance issues
- Integration errors
- Architecture problems

## Process

### 1. Read Error Message

- Extract error message from user request
- Identify error type (syntax, import, type, typo)
- Locate file and line number from error

### 2. Identify Cause

- Read the problematic file at error location
- Identify root cause (missing character, wrong name, etc.)
- Verify fix is obvious and safe

### 3. Apply Fix

- Make minimal change to fix error
- Preserve existing code structure
- Don't refactor or optimize

### 4. Verify Fix

- Check syntax is correct
- Verify import paths are correct
- Confirm type matches expected
- If verification fails → Report failure, proceed to DEBUG workflow

### 5. Report Result

- If fix succeeds → Report success, done (no workflow needed)
- If fix fails → Report failure, proceed to DEBUG workflow

## Integration with cc10x Orchestrator

This skill is invoked automatically by the orchestrator in Phase 3 (Intent and Context Check) when:

- User request contains single clear error
- Error meets quick fix criteria
- Fix is obvious and actionable

**Execution Flow:**

1. Orchestrator Phase 0: Functionality Analysis (MANDATORY FIRST)
2. Orchestrator: Context Preset Detection (automatic)
3. Orchestrator Phase 3: Error Detection (this skill)
4. If quick fix succeeds → Done
5. If quick fix fails → Proceed to DEBUG workflow

## Troubleshooting

**Common Issues:**

1. **Quick fix attempted for complex error**
   - **Symptom**: Fix doesn't work, error persists or multiplies
   - **Cause**: Error doesn't meet quick fix criteria (multiple errors, complex, cross-file)
   - **Fix**: Proceed to DEBUG workflow instead
   - **Prevention**: Always verify error meets quick fix criteria first

2. **Fix applied but new errors introduced**
   - **Symptom**: Original error fixed but new errors appear
   - **Cause**: Fix wasn't minimal or didn't preserve code structure
   - **Fix**: Revert fix, proceed to DEBUG workflow
   - **Prevention**: Always make minimal changes, verify no new errors

3. **Error not reproducible or unclear**
   - **Symptom**: Can't identify exact error or fix
   - **Cause**: Error message unclear or fix not obvious
   - **Fix**: Proceed to DEBUG workflow for investigation
   - **Prevention**: Only use quick fix for clear, obvious errors

**If issues persist:**

- Verify error meets quick fix criteria (single, clear, obvious)
- Check that fix is minimal and preserves structure
- If fix fails, proceed to DEBUG workflow immediately
- Don't attempt multiple quick fixes

## Example Scenarios

**Scenario 1: Missing Semicolon**

```
Error: Missing semicolon at line 45
File: src/utils/helper.ts:45
```

→ Fix: Add semicolon at line 45

**Scenario 2: Missing Import**

```
Error: Cannot find module './types'
File: src/components/Button.tsx:3
```

→ Fix: Add import statement or fix import path

**Scenario 3: Typo**

```
Error: 'userName' is not defined
File: src/auth/login.ts:12
```

→ Fix: Correct variable name typo

## Success Criteria

- Error is fixed with minimal change
- Code compiles/runs without error
- No new errors introduced
- Fix is verified before reporting success

## Fallback to DEBUG Workflow

If quick fix fails or doesn't apply:

- Report failure clearly
- Explain why quick fix didn't work
- Proceed to DEBUG workflow automatically
- Don't attempt multiple quick fixes
