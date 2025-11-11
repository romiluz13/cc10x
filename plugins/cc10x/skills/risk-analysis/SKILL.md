---
name: risk-analysis
description: Identifies risks with functionality-first, context-dependent approach. Use PROACTIVELY when planning features or reviewing code. First understands functionality using universal questions and context-dependent flows, then identifies risks specific to that functionality. Focuses on risks that affect functionality, not generic risks. Provides specific mitigation strategies with examples.
allowed-tools: Read, Grep, Glob
---

# Risk Analysis - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before analyzing risks, understand functionality using context-dependent analysis.

**Core Principle**: Understand what functionality needs risk analysis (using universal questions and context-dependent flows), then identify risks specific to that functionality. Risks exist in the context of functionality, not in isolation.

## Quick Start

Analyze risks by first understanding functionality, then identifying risks specific to that functionality.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Identify functionality risks**: Upload fails if network unstable → blocks user flow
3. **Analyze risk**: High impact (blocks functionality), Medium probability
4. **Mitigate**: Add retry logic, show user-friendly error message

**Result:** Risks affecting functionality identified and mitigated.

## Quick Decision Tree

```
RISK ANALYSIS NEEDED?
│
├─ Understand Expected Functionality First
│  ├─ Context-dependent analysis complete? → Continue
│  └─ Not complete? → STOP, complete functionality analysis first
│
├─ Identify Functionality Risks
│  ├─ Risks mapped to flows? → Continue
│  └─ Generic risks? → STOP, refocus on functionality risks
│
├─ Analyze Risks
│  ├─ Risk framework applied? → Continue
│  └─ Not applied? → Apply functionality-focused risk framework
│
└─ Mitigate Risks
   ├─ Mitigation strategies specific? → Implement
   └─ Generic strategies? → STOP, create functionality-specific mitigations
```

## When to Use

**Use PROACTIVELY when**:

- Planning features
- Reviewing code
- Identifying potential issues

**Functionality-First Process**:

1. **First**: Understand expected functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Map observed behavior to expected behavior (where does flow break?)
3. **Then**: Identify risks specific to that functionality
4. **Then**: Apply risk frameworks to analyze functionality-specific risks
5. **Then**: Provide specific mitigation strategies with examples
6. **Focus**: Risks that affect functionality, not generic risks

## Core Process Overview

### Step 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Reference**: See [Functionality Analysis Template](../cc10x-orchestrator/templates/functionality-analysis.md) for complete template.

**Process**:

1. **Detect Code Type**: Identify if this is UI, API, Utility, Integration, Database, Configuration, CLI, or Background Job
2. **Universal Questions First**: Answer Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Answer flow questions based on code type (User Flow, System Flow, Integration Flow, etc.)

**Reference**: `references/functionality-analysis.md` for detailed functionality analysis patterns.

### Step 2: Risk Identification (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only identify risks AFTER you understand functionality. Focus on risks specific to that functionality.

**Functionality-Focused Risk Checklist**:

**Priority: Critical (Blocks Functionality)**:

- [ ] Data flow risks that break functionality
- [ ] Dependency risks that break functionality
- [ ] Timing risks that break functionality
- [ ] Security risks that break functionality
- [ ] Performance risks that break functionality
- [ ] Failure risks that break functionality

**Priority: Important (Affects Functionality)**:

- [ ] UX risks that degrade functionality
- [ ] Performance risks that degrade functionality
- [ ] Scalability risks that affect functionality

**Reference**: `references/risk-identification.md` for detailed risk identification patterns and examples.

### Step 3: Risk Analysis Framework

**Apply functionality-focused risk framework**:

- 7-Stage Risk Framework (Data Flow, Dependency, Timing/Concurrency, UX & Accessibility, Security & Compliance, Performance & Scalability, Failure & Recovery)
- Risk scoring guide (functionality-focused)
- Risk mitigation patterns

**Reference**: `references/risk-framework.md` for detailed risk analysis framework and scoring.

### Step 4: Mitigation Strategies

**Provide specific, actionable mitigation strategies** with examples, not generic patterns.

**Reference**: `references/mitigation-strategies.md` for detailed mitigation strategies with examples.

## Quick Reference

| Risk Category   | Functionality Impact   | Mitigation Focus              |
| --------------- | ---------------------- | ----------------------------- |
| **Data Flow**   | Breaks functionality   | Validation, error handling    |
| **Dependency**  | Breaks functionality   | Retry logic, fallbacks        |
| **Timing**      | Breaks functionality   | Timeouts, concurrency control |
| **Security**    | Breaks functionality   | Input validation, auth        |
| **Performance** | Degrades functionality | Optimization, caching         |
| **Failure**     | Breaks functionality   | Error handling, recovery      |

## Reference Files

**For detailed risk analysis guidance, see**:

- **`references/functionality-analysis.md`**: Context-dependent analysis patterns, flow mapping, examples
- **`references/risk-identification.md`**: Risk identification patterns, functionality-focused risk checklist, examples
- **`references/risk-framework.md`**: 7-stage risk framework, risk scoring guide, risk analysis patterns
- **`references/mitigation-strategies.md`**: Mitigation strategies with examples, retry logic, fallbacks, error handling

**For additional patterns, see**:

- **PATTERNS.md**: Detailed risk analysis framework including 7-Stage Risk Framework, risk scoring guide, risk mitigation patterns

## Priority Classification

**Critical (Must Fix)**:

- Risk breaks functionality (user flow, system flow, integration flow)
- Prevents functionality from working
- Breaks functionality completely

**Important (Should Fix)**:

- Risk affects functionality negatively (slows functionality, unreliable functionality)
- Degrades functionality significantly

**Minor (Can Defer)**:

- Generic risks that don't affect functionality
- Perfect risk mitigation (if functionality works)

## Integration with Orchestrator

This skill is loaded by orchestrator workflows when risk analysis is needed. The orchestrator coordinates:

- Functionality analysis (Phase 0)
- Skill loading (Phase 2)
- Risk analysis execution

**CRITICAL**: Maintain functionality-first approach. Risk analysis must follow functionality analysis.

---

## Troubleshooting

**Common Issues:**

1. **Risk analysis without understanding functionality**
   - **Symptom**: Risks identified but don't relate to functionality
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, understand functionality flows
   - **Prevention**: Always understand functionality before risk analysis

2. **Generic risks instead of functionality-specific**
   - **Symptom**: Risks are generic, not mapped to functionality flows
   - **Cause**: Didn't map risks to functionality flows
   - **Fix**: Map risks to functionality flows, identify functionality-specific risks
   - **Prevention**: Always map risks to functionality flows

3. **Mitigation strategies not specific**
   - **Symptom**: Generic mitigations that don't address functionality risks
   - **Cause**: Didn't create functionality-specific mitigations
   - **Fix**: Create mitigations specific to functionality risks
   - **Prevention**: Always create functionality-specific mitigations

**If issues persist:**

- Verify functionality analysis was completed first
- Check that risks were mapped to functionality flows
- Ensure mitigations are functionality-specific
- Review reference files for detailed guidance

---

**Remember**: Risks exist in the context of functionality. Don't analyze generically - understand expected functionality, map observed to expected, then identify risks specific to functionality! Provide specific risk analysis and mitigation strategies with examples, not generic patterns.
