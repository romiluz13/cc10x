---
name: debugging-patterns
description: Systematic debugging with functionality-first, context-dependent approach covering systematic debugging, root cause analysis, and log analysis. Use PROACTIVELY when diagnosing bugs. First understands expected functionality using universal questions and context-dependent flows, then maps observed behavior to expected behavior, then investigates bugs systematically. Enforces LOG FIRST, hypothesis-driven fixes, and regression tests. Focuses on bugs that affect functionality, not generic debugging patterns.
allowed-tools: Read, Grep, Glob, Bash
---

# Debugging Patterns - Functionality First, Context-Dependent

## Purpose

This skill provides comprehensive debugging guidance covering systematic debugging, root cause analysis, and log analysis. It understands expected functionality before debugging, maps observed to expected behavior, and investigates bugs systematically with evidence-based approaches.

**Unique Value**:

- Understands expected functionality before debugging
- Maps observed behavior to expected behavior
- Enforces LOG FIRST methodology
- Provides systematic debugging strategies
- Covers root cause analysis and log analysis

**When to Use**:

- When diagnosing bugs
- When investigating test failures
- When troubleshooting unexpected behavior

---

## Quick Start

Debug systematically by first understanding expected functionality, then logging evidence, then investigating.

**Example:**

1. **Understand expected functionality**: File upload should work (User Flow: select → upload → confirm)
2. **Map observed**: Upload fails at step 2 (upload), error: "network timeout"
3. **LOG FIRST**: Capture error logs, network requests, state at failure point
4. **Investigate**: Check network requests, verify timeout settings
5. **Root cause**: Missing timeout configuration → functionality breaks
6. **Fix**: Increase timeout, add retry logic
7. **Verify**: Functionality works, tests pass

**Result:** Bug fixed through systematic investigation with evidence.

## Functionality First Mandate

**CRITICAL**: Before debugging, understand expected functionality using context-dependent analysis.

**Core Principle**: Understand what functionality should work (using universal questions and context-dependent flows), then map observed behavior to expected behavior, then debug bugs that affect functionality. Bugs exist in the context of functionality, not in isolation.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any debugging, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Expected Functionality**:
   - What should this code do?
   - What functionality should work?
   - What are the expected flows? (User, Admin, System, Integration, etc.)

3. **Map Observed to Expected**:
   - Compare observed behavior to expected flows
   - Identify where expected flow diverges from observed flow
   - Focus debugging on the divergence point

---

### Phase 2: LOG FIRST (MANDATORY SECOND STEP)

**CRITICAL**: No fixes without root-cause evidence. If you have not logged or observed the failing state, you are guessing.

**Log functionality-related data**:

- Log the full object/response with `JSON.stringify(value, null, 2)` (functionality data)
- Record headers, cookies, environment variables (masking secrets) (functionality context)
- For HTTP issues, log method, URL, payload, status, and body (functionality requests)
- For auth, log session claims, roles, and config (functionality auth)

**Focus**: Log data that helps understand functionality, not generic logging.

---

### Phase 3: Systematic Investigation (Functionality-Focused)

**After logging evidence, investigate systematically**:

1. **Reproduce the functionality issue reliably**
2. **Capture complete error messages, logs, request/response payloads related to functionality**
3. **Inspect recent changes that might affect functionality**
4. **Map observed behavior to expected behavior (where does the flow break?)**

**Investigation Checklist**:

- [ ] Expected functionality understood (context-dependent analysis)
- [ ] Observed behavior mapped to expected behavior (where does flow break?)
- [ ] Bug reproduced consistently
- [ ] Evidence captured (logs, errors, state)
- [ ] Root cause location identified (which flow step breaks?)

---

### Phase 4: Root Cause Analysis (Functionality-Focused)

**After investigation, identify root cause**:

**Root Cause Analysis Strategies**:

1. **5 Whys Framework**: Apply "Why?" 5 times, focusing on how each answer affects functionality
2. **Symptom-to-Cause Mapping**: Map symptoms to functionality root causes
3. **Flow-Based Analysis**: Trace expected flow vs observed flow, identify where flow breaks
4. **Evidence-Based Analysis**: Gather evidence (logs, code, recent changes), analyze to identify root cause
5. **Backward Tracing**: When error is deep in call stack, trace backward through call chain to find original trigger

**Root Cause Checklist**:

- [ ] Root cause breaks user flow (user can't complete tasks)
- [ ] Root cause breaks system flow (system doesn't process)
- [ ] Root cause breaks integration flow (external systems don't work)
- [ ] Root cause identified at source (not symptom)

---

### Phase 5: Hypothesis + Minimal Fix (Functionality-Focused)

**After root cause identified, fix bugs affecting functionality**:

1. **State the suspected root cause** in one sentence (how it affects functionality)
2. **Write a failing regression test** that proves the bug affects functionality
3. **Apply the smallest change** to make functionality work
4. **Test minimally** (one variable at a time)
5. **If 3+ fixes fail**: Question architecture

**Fix Checklist**:

- [ ] Root cause affects functionality (verified)
- [ ] Failing regression test written (proves bug affects functionality)
- [ ] Minimal fix applied (smallest change to restore functionality)
- [ ] Fix tested (functionality works)

---

### Phase 6: Verification (Functionality-Focused)

**After fix applied, verify functionality works**:

1. **Run the regression test** and surrounding suite
2. **Verify functionality works** (user flow, admin flow, system flow)
3. **Summarize the fix**, evidence, and follow-up monitoring

**Verification Checklist**:

- [ ] Regression test passes
- [ ] Functionality works (user flow, admin flow, system flow)
- [ ] Tests pass
- [ ] Fix documented

---

## Log Analysis Strategies

**After understanding expected functionality, analyze logs**:

1. **Trace Functionality Flow Through Logs**: Find request ID, trace flow steps through logs
2. **Compare Expected vs Observed Log Patterns**: Compare expected log pattern to observed pattern
3. **Analyze Logs by Functionality Flow Step**: Check logs for each flow step
4. **Analyze Error Logs for Functionality Issues**: Find all errors, group by error type, analyze most common
5. **Analyze Performance Logs for Functionality Issues**: Find slow requests, analyze bottlenecks

**Focus**: Logs that help understand functionality issues, not generic logs.

---

## Red Flags - STOP

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "One more fix attempt" (when already tried 2+)
- "Each fix reveals new problem in different place"

**ALL of these mean: STOP. Return to Phase 1 (Investigate).**

**If 3+ fixes failed**: Question the architecture.

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Debugging Report

## Expected Functionality Summary

[Brief summary of expected functionality from Phase 1]

## Observed Behavior Summary

[Brief summary of observed behavior and where it diverges from expected]

## Evidence Captured

[Logs, errors, state captured from Phase 2]

## Root Cause Analysis

[Root cause identified from Phase 4, analysis strategy used]

## Fix Applied

[Minimal fix applied from Phase 5, regression test written]

## Verification

[Functionality verified from Phase 6, tests passing]

## Prevention Strategies

[How to prevent this bug from recurring]
```

---

## Priority Classification

**Critical (Must Fix)**:

- Blocks functionality (breaks user flow, system flow, integration flow)
- Prevents feature from working
- Breaks functionality completely

**Important (Should Fix)**:

- Affects functionality negatively (degrades user experience, slows functionality)
- Degrades functionality significantly

**Minor (Can Defer)**:

- Doesn't affect functionality (cosmetic issues, minor performance)
- Generic bugs not related to functionality

---

## Usage Guidelines

### For Debug Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis)
2. **Then**: Complete Phase 2 (LOG FIRST - Capture Evidence)
3. **Then**: Complete Phase 3 (Systematic Investigation)
4. **Then**: Complete Phase 4 (Root Cause Analysis)
5. **Then**: Complete Phase 5 (Hypothesis + Minimal Fix)
6. **Then**: Complete Phase 6 (Verification)
7. **Focus**: Bugs that affect functionality, not generic bugs

### Key Principles

1. **Functionality First**: Always understand expected functionality before debugging
2. **LOG FIRST**: Never fix without evidence
3. **Map Observed to Expected**: Always compare observed behavior to expected flows
4. **Systematic Investigation**: Follow systematic process, don't guess
5. **Minimal Fixes**: Apply smallest change to restore functionality
6. **Verify Functionality**: Always verify functionality works after fix

---

## Common Mistakes to Avoid

1. **Debugging without understanding expected functionality**
   - **Symptom**: Can't identify where functionality breaks
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, understand expected flows
   - **Prevention**: Always understand expected functionality before debugging

2. **LOG FIRST not followed**
   - **Symptom**: Fixing bugs without evidence
   - **Cause**: Didn't capture logs before fixing
   - **Fix**: Capture logs first, then investigate
   - **Prevention**: Always log first, never fix without evidence

3. **Observed behavior not mapped to expected**
   - **Symptom**: Can't identify where flow breaks
   - **Cause**: Didn't map observed to expected behavior
   - **Fix**: Map observed to expected flows, identify break point
   - **Prevention**: Always map observed to expected before debugging

---

## Troubleshooting

**Common Issues:**

1. **Debugging without understanding expected functionality**
   - **Symptom**: Can't identify where functionality breaks
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first
   - **Prevention**: Always understand expected functionality before debugging

2. **LOG FIRST not followed**
   - **Symptom**: Fixing bugs without evidence
   - **Cause**: Didn't capture logs before fixing
   - **Fix**: Capture logs first, then investigate
   - **Prevention**: Always log first, never fix without evidence

**If issues persist:**

- Verify expected functionality was understood first
- Check that LOG FIRST was followed (evidence captured)
- Ensure observed was mapped to expected
- Review log analysis strategies

---

_This skill enables systematic debugging with functionality-first approach, enforcing LOG FIRST methodology, root cause analysis, and log analysis to fix bugs that affect functionality._
