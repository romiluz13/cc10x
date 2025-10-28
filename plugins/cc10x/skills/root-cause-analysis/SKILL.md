---
name: root-cause-analysis
description: Identifies root causes of bugs and issues by analyzing symptoms, logs, and code flow. Use when investigating why bugs occur, understanding failure patterns, analyzing error chains, and preventing recurrence. Provides root cause analysis frameworks, symptom-to-cause mapping, and prevention strategies. Loaded by DEBUG workflow for comprehensive bug investigation. Complements systematic-debugging with deeper analysis of why bugs happen, not just how to fix them. Critical for preventing recurring bugs and improving system reliability.
---

# Root Cause Analysis

**Find the real problem, not just the symptom.**

## Progressive Loading Stages

### Stage 1: Metadata

- **Skill**: Root Cause Analysis
- **Purpose**: Identify why bugs occur, not just fix symptoms
- **When**: Investigating recurring bugs, understanding failure patterns, preventing recurrence
- **Core Rule**: Symptoms are clues - follow them to the root cause
- **Sections Available**: The 5 Whys, Cause-Effect Mapping, Prevention Strategies, Quick Checks

---

### Stage 2: Quick Reference

## The 5 Whys Framework

**Problem**: Login returns 401 error

```
Why 1: Why does login return 401?
 Token validation fails

Why 2: Why does token validation fail?
 Token is expired

Why 3: Why is token expired?
 Refresh token endpoint not called

Why 4: Why isn't refresh token called?
 No refresh logic in auth service

Why 5: Why is there no refresh logic?
 Feature not implemented

ROOT CAUSE: Missing token refresh logic
FIX: Implement automatic token refresh
PREVENTION: Add token refresh to auth service
```

## Symptom-to-Cause Mapping

```
Symptom: "User can't login"
 Possible Causes:
   Database connection failed
   Password hash mismatch
   User account locked
   Rate limiting triggered
   Authentication service down
 Investigation: Check logs for each

Symptom: "Page loads slowly"
 Possible Causes:
   Database query slow
   Large data transfer
   Missing indexes
   N+1 query problem
   External API timeout
 Investigation: Profile each layer

Symptom: "Random crashes"
 Possible Causes:
   Memory leak
   Race condition
   Unhandled exception
   Resource exhaustion
   Third-party library bug
 Investigation: Check crash logs
```

## Root Cause Analysis Checklist

```
Investigation Process:
- [ ] Reproduce bug consistently
- [ ] Gather all relevant logs
- [ ] Identify exact failure point
- [ ] Trace back to source
- [ ] Ask "Why?" 5 times
- [ ] Verify root cause
- [ ] Plan prevention
- [ ] Implement fix
- [ ] Test thoroughly
- [ ] Document findings
```

---

### Stage 3: Detailed Guide

## Cause-Effect Analysis

### Direct Cause vs Root Cause

**Direct Cause** (symptom):
- What immediately caused the failure
- Example: "Token validation failed"
- Fixing this stops the symptom

**Root Cause** (underlying issue):
- Why the direct cause happened
- Example: "Token refresh logic not implemented"
- Fixing this prevents recurrence

### Failure Chain Analysis

```
User Action: Click Login
  
Expected: Auth service validates credentials
  
Actual: Auth service returns 401
  
Investigation:
  1. Check auth service logs
  2. Find: "Token expired"
  3. Check token refresh logic
  4. Find: "No refresh endpoint"
  5. ROOT CAUSE: Missing refresh logic
```

## Prevention Strategies

### Prevent Recurrence

**After finding root cause:**

1. **Understand why it happened**
   - Was it a missing feature?
   - Was it a design flaw?
   - Was it an oversight?

2. **Implement prevention**
   - Add feature if missing
   - Redesign if flawed
   - Add test if oversight

3. **Add safeguards**
   - Add monitoring
   - Add alerts
   - Add tests

4. **Document learning**
   - Why it happened
   - How to prevent
   - What to watch for

### Common Root Causes

**Performance Issues:**
- Missing database indexes
- N+1 query problems
- Inefficient algorithms
- Memory leaks
- Blocking operations

**Reliability Issues:**
- Missing error handling
- Race conditions
- Resource exhaustion
- Timeout issues
- Cascading failures

**Security Issues:**
- Missing validation
- Weak authentication
- Insufficient authorization
- Unencrypted data
- Injection vulnerabilities

---

## Investigation Workflow

### Step 1: Reproduce

```
Can you reproduce the bug?
- YES: Continue to Step 2
- NO: Gather more information
  - When does it happen?
  - What's the pattern?
  - Can you narrow it down?
```

### Step 2: Gather Evidence

```
Collect:
- Error messages
- Stack traces
- Log entries
- Timing information
- User actions
- System state
```

### Step 3: Isolate

```
Narrow down:
- Which component fails?
- Which function?
- Which line?
- What's the exact condition?
```

### Step 4: Trace Back

```
Follow the chain:
- Where did the bad data come from?
- Who called this function?
- What was the state before?
- When did it change?
```

### Step 5: Verify Root Cause

```
Confirm:
- Does fixing this prevent recurrence?
- Are there other instances?
- Is this the only cause?
- Are there related issues?
```

---

**Remember**: The best bugs to fix are the ones that never happen again. Find the root cause, fix it properly, and prevent recurrence.
