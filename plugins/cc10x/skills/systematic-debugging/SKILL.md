---
name: systematic-debugging
description: Debugs issues with functionality-first, context-dependent approach. Use PROACTIVELY when diagnosing bugs. First understands expected functionality using universal questions and context-dependent flows, then maps observed behavior to expected behavior, then investigates bugs systematically. Focuses on bugs that affect functionality, not generic debugging patterns. Enforces LOG FIRST, hypothesis-driven fixes, and regression tests. Provides specific debugging strategies with examples.
allowed-tools: Read, Grep, Glob, Bash
---

# Systematic Debugging - Functionality First, Context-Dependent

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**CRITICAL**: Before debugging, understand expected functionality using context-dependent analysis. If you have not logged or observed the failing state, you are guessing.

## Functionality First Mandate

**CRITICAL**: Before debugging, understand expected functionality using context-dependent analysis.

**Core Principle**: Understand what functionality should work (using universal questions and context-dependent flows), then map observed behavior to expected behavior, then debug bugs that affect functionality. Bugs exist in the context of functionality, not in isolation.

## Quick Start

Debug systematically by first understanding expected functionality, then logging evidence, then investigating.

**Example:**

1. **Understand expected functionality**: File upload should work (User Flow: select → upload → confirm)
2. **LOG FIRST**: Capture error logs, network requests, state at failure point
3. **Map observed**: Upload fails at step 2, error: "network timeout"
4. **Investigate**: Check network requests, verify timeout settings
5. **Fix**: Increase timeout, add retry logic

**Result:** Bug fixed through systematic investigation with evidence.

## Quick Decision Tree

```
BUG DETECTED?
│
├─ Understand Expected Functionality First
│  ├─ Context-dependent analysis complete? → Continue
│  └─ Not complete? → STOP, complete functionality analysis first
│
├─ Map Observed to Expected
│  ├─ Where does flow break? → Continue
│  └─ Flow not mapped? → STOP, map observed to expected first
│
├─ Investigate (Phase 1)
│  ├─ Evidence captured? → Continue to Phase 2
│  └─ No evidence? → STOP, capture evidence first
│
├─ Pattern Analysis (Phase 2)
│  ├─ Root cause identified? → Continue to Phase 3
│  └─ Not identified? → Return to Phase 1, gather more evidence
│
├─ Hypothesis + Fix (Phase 3)
│  ├─ Fix works? → Continue to Phase 4
│  └─ Fix doesn't work? → Return to Phase 1, form new hypothesis
│
└─ Verification (Phase 4)
   ├─ Functionality works? → Success
   └─ Functionality broken? → Return to Phase 1
```

## When to Use

**Use PROACTIVELY when**:

- Diagnosing bugs
- Test failures
- Unexpected behavior

**Functionality-First Process**:

1. **First**: Understand expected functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Map observed behavior to expected behavior (where does the flow break?)
3. **Then**: Investigate bugs that affect functionality
4. **Then**: Fix bugs systematically
5. **Focus**: Bugs that affect functionality, not generic bugs

## Core Process Overview

### Step 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Reference**: See [Functionality Analysis Template](../cc10x-orchestrator/templates/functionality-analysis.md) for complete template.

**Process**:

1. **Detect Code Type**: Identify if this is UI, API, Utility, Integration, Database, Configuration, CLI, or Background Job
2. **Universal Questions First**: Answer Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Answer flow questions based on code type (User Flow, System Flow, Integration Flow, etc.)

**Then Map Observed to Expected**:

- Compare observed behavior to expected flows
- Identify where expected flow diverges from observed flow
- Focus debugging on the divergence point

### Step 2: Systematic Debugging Process (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only debug AFTER you understand expected functionality and have mapped observed to expected. Debug bugs that affect functionality, not generic bugs.

**Core Principle**:

```
No fixes without root-cause evidence.
If you have not logged or observed the failing state, you are guessing.
```

**Functionality-First Debugging**:

1. **Understand Expected Functionality**: What should work? (context-dependent analysis)
2. **Map Observed to Expected**: What's broken? (compare observed to expected flows)
3. **Investigate**: Reproduce the bug, capture evidence
4. **Pattern Analysis**: Compare failing paths to working examples
5. **Hypothesis + Minimal Fix**: Fix the bug affecting functionality
6. **Verification**: Verify functionality works

## Four Phases

### Phase 1: Investigate (Functionality-Focused)

**Focus on functionality, not generic investigation**:

- Reproduce the functionality issue reliably
- Capture complete error messages, logs, request/response payloads related to functionality
- Inspect recent changes that might affect functionality
- Map observed behavior to expected behavior (where does the flow break?)

**Reference**: `references/root-cause-investigation.md` for detailed investigation guidance, multi-component diagnostic instrumentation, and examples.

### Phase 2: Pattern Analysis (Functionality-Focused)

**Compare failing functionality to working functionality**:

- Compare failing paths to working examples (same code type, similar functionality)
- Identify where expected flow diverges from observed flow
- Consult relevant skill guidance only if affects functionality

**Reference**: `references/pattern-analysis.md` for detailed pattern comparison guidance and examples.

### Phase 3: Hypothesis + Minimal Fix (Functionality-Focused)

**Fix bugs affecting functionality**:

- State the suspected root cause in one sentence (how it affects functionality)
- Write a failing regression test that proves the bug affects functionality
- Apply the smallest change to make functionality work
- Test minimally (one variable at a time)
- If 3+ fixes fail: Question architecture

**Reference**: `references/implementation-verification.md` for detailed hypothesis testing, minimal fix patterns, and architecture questioning guidance.

### Phase 4: Verification (Functionality-Focused)

**Verify functionality works**:

- Run the regression test and surrounding suite
- Verify functionality works (user flow, admin flow, system flow)
- Summarize the fix, evidence, and follow-up monitoring

**Reference**: `references/implementation-verification.md` for detailed verification patterns and deliverable templates.

## Red Flags - STOP

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1 (Investigate).**

**If 3+ fixes failed**: Question the architecture (see Phase 3 reference).

## Quick Reference

| Phase                   | Key Activities                                        | Success Criteria                                  |
| ----------------------- | ----------------------------------------------------- | ------------------------------------------------- |
| **1. Investigate**      | Reproduce, capture evidence, map observed to expected | Evidence captured, root cause location identified |
| **2. Pattern Analysis** | Compare failing to working, identify differences      | Root cause identified                             |
| **3. Hypothesis + Fix** | Form hypothesis, test minimally, fix                  | Fix works, functionality restored                 |
| **4. Verification**     | Run tests, verify functionality                       | Functionality works, tests pass                   |

## LOG FIRST Playbook (Functionality-Focused)

**Log functionality-related data**:

Whenever functionality behavior is unclear:

- Log the full object/response with `JSON.stringify(value, null, 2)` (functionality data)
- Record headers, cookies, environment variables (masking secrets) (functionality context)
- For HTTP issues, log method, URL, payload, status, and body (functionality requests)
- For auth, log session claims, roles, and config (functionality auth)

**Focus**: Log data that helps understand functionality, not generic logging.

## Reference Files

**For detailed debugging guidance, see**:

- **`references/root-cause-investigation.md`**: Phase 1 detailed guidance, multi-component diagnostic instrumentation, evidence capture patterns, examples
- **`references/pattern-analysis.md`**: Phase 2 detailed guidance, pattern comparison strategies, working example analysis, examples
- **`references/implementation-verification.md`**: Phases 3-4 detailed guidance, hypothesis testing, minimal fix patterns, architecture questioning, verification patterns, deliverable templates

## Anti-Patterns

- **Skipping functionality understanding**: Don't debug without understanding expected functionality
- **Generic debugging**: Don't debug bugs that don't affect functionality
- **Applying multiple fixes**: Don't fix without proving the cause affects functionality
- **Trusting documentation**: Don't trust docs over runtime data for functionality
- **Reporting success without logs/tests**: Always verify functionality works
- **Not mapping observed to expected**: Always compare observed behavior to expected flows

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

## Integration with Orchestrator

This skill is loaded by orchestrator workflows when debugging is detected. The orchestrator coordinates:

- Functionality analysis (Phase 0)
- Skill loading (Phase 2)
- Debugging execution

**CRITICAL**: Maintain functionality-first approach. Debugging must follow functionality analysis.

## Troubleshooting

**Common Issues:**

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

**If issues persist:**

- Verify expected functionality was understood first
- Check that LOG FIRST was followed (evidence captured)
- Ensure observed was mapped to expected
- Review reference files for detailed guidance

## References

- Official debugging guidance: `docs/reference/03-SUBAGENTS.md`
- Verification requirements: `plugins/cc10x/skills/verification-before-completion/SKILL.md`

---

**Remember**: Bugs exist in the context of functionality. Don't debug generically - understand expected functionality, map observed to expected, then debug bugs that affect functionality! Provide specific debugging strategies with examples, not generic patterns.
