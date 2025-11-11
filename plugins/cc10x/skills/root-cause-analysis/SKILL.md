---
name: root-cause-analysis
description: Identifies root causes with functionality-first, context-dependent approach. Use PROACTIVELY when investigating bugs. First understands expected functionality using universal questions and context-dependent flows, then identifies root causes specific to that functionality. Focuses on root causes that affect functionality, not generic root cause analysis. Provides specific fixes with examples.
allowed-tools: Read, Grep, Glob, Bash
---

# Root Cause Analysis - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before analyzing root causes, understand expected functionality using context-dependent analysis.

**Core Principle**: Understand what functionality should work (using universal questions and context-dependent flows), then identify root causes specific to that functionality. Root causes exist in the context of functionality, not in isolation.

## Quick Start

Find root causes by first understanding expected functionality, then mapping observed to expected behavior.

**Example:**

1. **Understand expected functionality**: File upload should work (User Flow: select → upload → confirm)
2. **Map observed**: Upload fails at step 2 (upload) with "file too large" error
3. **Choose strategy**: Flow-based analysis (where does flow break?)
4. **Find root cause**: Missing file size validation before upload
5. **Fix**: Add validation at flow step 1 (file selection)

**Result:** Root cause identified and fixed at the source.

## Quick Decision Tree

```
ROOT CAUSE ANALYSIS NEEDED?
│
├─ Understand Expected Functionality First
│  ├─ Context-dependent analysis complete? → Continue
│  └─ Not complete? → STOP, complete functionality analysis first
│
├─ Map Observed to Expected
│  ├─ Where does flow break? → Continue
│  └─ Flow not mapped? → STOP, map observed to expected first
│
├─ Choose Analysis Strategy
│  ├─ Deep call stack? → Backward tracing
│  ├─ Symptom clear? → Symptom-to-cause mapping
│  ├─ Need systematic? → 5 Whys framework
│  └─ Flow-based? → Flow-based analysis
│
└─ Implement Fix
   ├─ Root cause identified? → Fix at source
   └─ Not identified? → Return to analysis strategies
```

## When to Use

**Use PROACTIVELY when**:

- Investigating recurring bugs
- Understanding failure patterns
- Preventing recurrence

**Functionality-First Process**:

1. **First**: Understand expected functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Map observed behavior to expected behavior (where does flow break?)
3. **Then**: Identify root causes specific to that functionality
4. **Then**: Apply root cause frameworks to analyze functionality-specific root causes
5. **Then**: Provide specific fixes with examples
6. **Focus**: Root causes that affect functionality, not generic root causes

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
- Focus root cause analysis on the divergence point

**Reference**: `references/functionality-analysis.md` for detailed context-dependent analysis patterns and examples.

### Step 2: Root Cause Analysis (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only analyze root causes AFTER you understand expected functionality. Analyze root causes specific to functionality, not generic root causes.

**Functionality-Focused Root Cause Checklist**:

**Priority: Critical (Core Functionality)**:

- [ ] Root cause breaks user flow (user can't complete tasks)
- [ ] Root cause breaks system flow (system doesn't process)
- [ ] Root cause breaks integration flow (external systems don't work)
- [ ] Root cause breaks error handling (errors not handled)

**Priority: Important (Supporting Functionality)**:

- [ ] Root cause affects functionality performance (slows functionality)
- [ ] Root cause affects functionality reliability (unreliable functionality)

## Root Cause Analysis Strategies

**CRITICAL**: Provide specific, actionable root cause analysis strategies with examples, not generic frameworks.

### Strategy 1: The 5 Whys Framework (Functionality-Focused)

Apply "Why?" 5 times, focusing on how each answer affects functionality. Trace from symptom to root cause.

**Reference**: `references/analysis-strategies.md` for detailed 5 Whys framework with examples.

### Strategy 2: Symptom-to-Cause Mapping (Functionality-Focused)

Map symptoms to functionality root causes. Investigate each possible cause, gather evidence, identify most likely root cause.

**Reference**: `references/analysis-strategies.md` for detailed symptom-to-cause mapping with examples.

### Strategy 3: Flow-Based Root Cause Analysis

Trace expected flow vs observed flow. Identify where flow breaks, analyze why it breaks at that point.

**Reference**: `references/analysis-strategies.md` for detailed flow-based analysis with examples.

### Strategy 4: Evidence-Based Root Cause Analysis

Gather evidence (logs, code, recent changes). Analyze evidence to identify root cause. Verify root cause with evidence.

**Reference**: `references/analysis-strategies.md` for detailed evidence-based analysis with examples.

### Strategy 5: Backward Tracing (Deep Call Stack)

When error is deep in call stack, trace backward through call chain to find original trigger. Fix at source, not at symptom.

**Reference**: `references/analysis-strategies.md` for detailed backward tracing patterns with examples.

## Quick Reference

| Strategy             | When to Use                   | Key Steps                                         |
| -------------------- | ----------------------------- | ------------------------------------------------- |
| **5 Whys**           | Need systematic analysis      | Ask "Why?" 5 times, focus on functionality impact |
| **Symptom-to-Cause** | Symptom clear, causes unclear | Map symptoms to causes, investigate each          |
| **Flow-Based**       | Flow breakdown obvious        | Trace expected vs observed flow, find divergence  |
| **Evidence-Based**   | Evidence available            | Gather evidence, analyze, verify root cause       |
| **Backward Tracing** | Deep call stack error         | Trace backward to original trigger                |

## Root Cause Analysis Checklist

**⚠️ Only check these AFTER functionality is understood**:

```
Investigation Process:
- [ ] Understand expected functionality (context-dependent analysis)
- [ ] Map observed behavior to expected behavior (where does flow break?)
- [ ] Reproduce functionality bug consistently
- [ ] Gather all relevant logs (functionality-related)
- [ ] Identify exact functionality failure point (which flow step?)
- [ ] Trace back to source (functionality root cause)
- [ ] Ask "Why?" 5 times (functionality-focused)
- [ ] Verify root cause (affects functionality)
- [ ] Plan prevention (prevents functionality issues)
- [ ] Implement fix (fixes functionality)
- [ ] Test thoroughly (verifies functionality works)
- [ ] Document findings (functionality-focused)
```

## Reference Files

**For detailed root cause analysis guidance, see**:

- **`references/functionality-analysis.md`**: Context-dependent analysis patterns, universal questions, flow mapping, examples
- **`references/analysis-strategies.md`**: 5 Whys framework, symptom-to-cause mapping, flow-based analysis, evidence-based analysis, backward tracing patterns with examples
- **`references/fix-implementation.md`**: Root cause fixes, verification patterns, prevention strategies, examples

## Prevention Strategies (Functionality-Focused)

**After finding root cause that affects functionality**:

1. **Understand why it happened** (functionality context)
2. **Implement prevention** (functionality-focused)
3. **Add safeguards** (functionality-focused)
4. **Document learning** (functionality-focused)

**Reference**: `references/fix-implementation.md` for detailed prevention strategies.

## Priority Classification

**Critical (Must Fix)**:

- Root cause breaks functionality (user flow, system flow, integration flow)
- Prevents functionality from working
- Breaks functionality completely

**Important (Should Fix)**:

- Root cause affects functionality negatively (slows functionality, unreliable functionality)
- Degrades functionality significantly

**Minor (Can Defer)**:

- Generic root causes that don't affect functionality
- Perfect root cause analysis (if functionality is fixed)

## Integration with Orchestrator

This skill is loaded by orchestrator workflows when root cause analysis is needed. The orchestrator coordinates:

- Functionality analysis (Phase 0)
- Skill loading (Phase 2)
- Root cause analysis execution

**CRITICAL**: Maintain functionality-first approach. Root cause analysis must follow functionality analysis.

---

## Troubleshooting

**Common Issues:**

1. **Root cause analysis without understanding expected functionality**
   - **Symptom**: Root causes identified but don't relate to functionality
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, understand expected flows
   - **Prevention**: Always understand expected functionality before analysis

2. **Observed behavior not mapped to expected**
   - **Symptom**: Can't identify where flow breaks
   - **Cause**: Didn't map observed to expected behavior
   - **Fix**: Map observed behavior to expected flows, identify break point
   - **Prevention**: Always map observed to expected before analysis

3. **Wrong analysis strategy chosen**
   - **Symptom**: Analysis doesn't find root cause
   - **Cause**: Chose wrong strategy for problem type
   - **Fix**: Review decision tree, choose appropriate strategy
   - **Prevention**: Always use decision tree to choose strategy

**If issues persist:**

- Verify expected functionality was understood first
- Check that observed was mapped to expected
- Ensure correct analysis strategy was chosen
- Review reference files for detailed guidance

---

**Remember**: Root causes exist in the context of functionality. Don't analyze generically - understand expected functionality, map observed to expected, then identify root causes specific to functionality! Provide specific root cause analysis strategies with examples, not generic frameworks.
