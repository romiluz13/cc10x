# cc10x Orchestrator - Quick Reference

**One-page reference for AI to quickly understand orchestrator activation and workflow selection.**

## 🚨 AUTO-LOAD TRIGGERS

**This skill MUST be loaded automatically when user request contains ANY of these keywords:**

### PLAN Workflow Keywords

plan, planning, planner, plan a, plan the, plan for, design, designing, designer, design a, design the, architect, architecture, architectural, system design, roadmap, road map, strategy, strategic planning, feature planning, project planning, implementation plan

### BUILD Workflow Keywords

build, building, builder, build a, build the, implement, implementation, implementing, create, creating, create a, create the, write code, write a, write the, coding, code, develop, development, developing, developer, make, making, make a, make the, add feature, implement feature, build feature

### REVIEW Workflow Keywords

review, reviewing, reviewer, review this, review the, audit, auditing, auditor, audit this, analyze, analysis, analyzing, analyze this, assess, assessment, assessing, assess this, evaluate, evaluation, evaluating, evaluate this, inspect, inspection, inspecting, inspect this, examine, examination, examining, examine this

### DEBUG Workflow Keywords

debug, debugging, debugger, debug this, fix, fixing, fix this, fix the, fix a, error, errors, error in, error with, bug, bugs, bug in, bug with, investigate, investigation, investigating, failure, failures, failed, failing, broken, broke, break, breaking, issue, issues, issue with, problem, problems, troubleshoot, troubleshooting, diagnose, diagnosis

### VALIDATE Workflow Keywords

validate, validation, validating, validate this, verify, verification, verifying, verify this, check, checking, check this, check the, confirm implementation, alignment check, consistency check

**If user request contains ANY keyword above → LOAD ORCHESTRATOR SKILL IMMEDIATELY**

## Workflow Selection Decision Tree

```
User request?
├─ Contains "plan"/"design"/"architect"/"roadmap"/"strategy"?
│   └─ YES → PLAN workflow
├─ Contains "build"/"implement"/"create"/"write code"/"develop"/"make"?
│   └─ YES → BUILD workflow
├─ Contains "review"/"audit"/"analyze"/"assess"/"evaluate"/"inspect"/"examine"?
│   └─ YES → REVIEW workflow
├─ Contains "debug"/"fix"/"error"/"bug"/"investigate"/"failure"/"broken"/"issue"/"problem"/"troubleshoot"/"diagnose"?
│   └─ YES → DEBUG workflow
├─ Contains "validate"/"verify"/"check"/"confirm implementation"/"alignment check"/"consistency check"?
│   └─ YES → VALIDATE workflow
├─ Multiple keywords matched?
│   └─ YES → Intent Disambiguation required
└─ No keywords matched?
    └─ YES → Ask user: "Which workflow should I run? (review/plan/build/debug/validate)"
```

## Workflow Selection Examples

- User says "plan a feature" → Load orchestrator → PLAN workflow activates
- User says "build a component" → Load orchestrator → BUILD workflow activates
- User says "review this code" → Load orchestrator → REVIEW workflow activates
- User says "debug this error" → Load orchestrator → DEBUG workflow activates
- User says "validate implementation" → Load orchestrator → VALIDATE workflow activates

## Why Orchestrator is Mandatory

**Bypass Prevention:**

- DO NOT write code directly - orchestrator coordinates subagents
- DO NOT skip TDD cycle - orchestrator enforces RED → GREEN → REFACTOR
- DO NOT skip Actions Taken tracking - orchestrator validates at checkpoints
- DO NOT skip inventory checks - orchestrator verifies skills/subagents loaded
- DO NOT skip memory integration - orchestrator queries/stores patterns
- DO NOT skip web fetch integration - orchestrator fetches external docs

**Enforcement Mechanisms:**

- Runtime Compliance Checks at 4 validation points
- Skills Inventory Check before Phase 3
- Subagents Inventory Check before Phase 4
- Actions Taken validation before final report
- Workflow stops if validation fails

## What Happens After Orchestrator Loads

1. **Phase 0: Functionality Analysis** (MANDATORY FIRST)
   - Understand user/admin/system flows
   - Verify functionality works
   - Extract acceptance criteria

2. **Workflow Selection**
   - Detect workflow keywords
   - Select appropriate workflow
   - Activate workflow file

3. **Skill Loading**
   - Load required skills (parallel if independent)
   - Load conditional skills (if detected)
   - Update Actions Taken

4. **Subagent Invocation**
   - Invoke subagents based on workflow
   - Sequential or parallel based on dependencies
   - Update Actions Taken

5. **Validation & Completion**
   - Validate at checkpoints
   - Generate verification summary
   - Complete workflow

## Enforcement Mechanisms Summary

1. **Skill Discovery** - Forces orchestrator loading FIRST
2. **Description Keywords** - Auto-loads on workflow keywords
3. **Context.json Rules** - AlwaysApply rules enforce orchestrator usage
4. **Workflow Validation Gates** - Runtime checks at key phases
5. **Explicit Triggers** - Keyword list makes activation clear

**Result**: Orchestrator activates automatically for 95%+ of workflow requests.
