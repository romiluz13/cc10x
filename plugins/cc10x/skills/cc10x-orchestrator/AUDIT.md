# Orchestrator Skill Audit

## Current State

- **Lines**: 1,576 (3.15x over 500 limit, way over 200 words for frequently-loaded)
- **Words**: 10,460 (52x over 200 words for frequently-loaded)
- **Description**: ~1,200+ chars (2.4x over 500 ideal, over 1024 max)
- **Major Sections**: 46 sections identified

## Section Breakdown

### Core Sections (Must Keep in SKILL.md)

1. **EXECUTION MODE** (lines 9-43): Critical enforcement - must be concise
2. **AUTO-LOAD TRIGGERS** (lines 45-104): Keyword triggers - essential for activation
3. **CRITICAL ENFORCEMENT** (lines 106-148): Bypass prevention - core enforcement
4. **TL;DR Quick Checklist** (lines 150-172): Quick reference - essential
5. **Guardrails** (lines 174-190): Core principles - essential
6. **Purpose** (lines 269-278): Core purpose - essential
7. **Supported Workflows** (lines 280-288): Workflow list - essential
8. **Quick Reference** (lines 1287-1312): Quick reference - essential

### Sections to Split to REFERENCE.md

- Tool Selection Guide (lines 854-872)
- Search Guidance (lines 874-916)
- Ask Questions Tool Usage (lines 797-822)
- Task Tool Usage (lines 824-852)
- Tool Access Precedence (lines 793-795)

### Sections to Split to ENFORCEMENT.md

- Runtime Compliance Checks (lines 192-267)
- Validation Checklist (lines 918-984)
- Strict Mode Enforcement (lines 930-984)
- Error Recovery Protocol (lines 1039-1156)
- Pre-Final-Report Validation (lines 1366-1450)
- Actions Taken Validation (lines 1454-1504)

### Sections to Split to WORKFLOWS.md

- Operation (lines 302-448)
- Skill Loading Optimization (lines 450-791)
- Subagent Invocation Rules (lines 657-791)
- Skills Inventory Check (lines 548-589)
- Subagents Inventory Check (lines 723-791)
- Real-Time Activation Tracking (lines 591-655)

### Sections to Split to VALIDATION.md

- Validation Checklist (lines 918-984)
- Pre-Final-Report Validation (lines 1366-1450)
- Actions Taken Validation (lines 1454-1504)
- Evidence-First Expectations (lines 1314-1318)
- Final Report Output Format (lines 1320-1364)

### Sections to Split to INTEGRATION.md

- Memory Integration (lines 1506-1525)
- Web Fetch Integration (lines 1527-1552)
- Context Editing (lines 1554-1566)

### Sections to Split to COMPLEXITY.md

- Complexity Gate (lines 1218-1220)
- Complexity Rubric (lines 1222-1285)

### Sections to Split to PARALLEL.md

- Parallel Execution Strategy (lines 1158-1198)
- Parallel Execution Safety Validation (lines 1200-1216)

## Keywords in Description

All keywords preserved (condensed list):

- PLAN: plan, planning, planner, plan a, plan the, plan for, design, designing, designer, design a, design the, architect, architecture, architectural, system design, roadmap, road map, strategy, strategic planning, feature planning, project planning, implementation plan
- BUILD: build, building, builder, build a, build the, implement, implementation, implementing, create, creating, create a, create the, write code, write a, write the, coding, code, develop, development, developing, developer, make, making, make a, make the, add feature, implement feature, build feature
- REVIEW: review, reviewing, reviewer, review this, review the, audit, auditing, auditor, audit this, analyze, analysis, analyzing, analyze this, assess, assessment, assessing, assess this, evaluate, evaluation, evaluating, evaluate this, inspect, inspection, inspecting, inspect this, examine, examination, examining, examine this
- DEBUG: debug, debugging, debugger, debug this, fix, fixing, fix this, fix the, fix a, error, errors, error in, error with, bug, bugs, bug in, bug with, investigate, investigation, investigating, failure, failures, failed, failing, broken, broke, break, breaking, issue, issues, issue with, problem, problems, troubleshoot, troubleshooting, diagnose, diagnosis
- VALIDATE: validate, validation, validating, validate this, verify, verification, verifying, verify this, check, checking, check this, check the, confirm implementation, alignment check, consistency check

## Enforcement Mechanisms

1. **EXECUTION MODE warnings**: Lines 9-43
2. **CRITICAL ENFORCEMENT rules**: Lines 106-148
3. **Runtime Compliance Checks**: Lines 192-267
4. **Validation Gates**: Lines 196-255
5. **Strict Mode**: Lines 930-984
6. **Error Recovery Protocol**: Lines 1039-1156
7. **Inventory Checks**: Skills (lines 548-589), Subagents (lines 723-791)
8. **Pre-Final-Report Validation**: Lines 1366-1450
9. **Actions Taken Validation**: Lines 1454-1504

## Prompt Engineering Value

All sections contain critical prompt engineering:

- Keyword density for activation
- Enforcement mechanisms for compliance
- Validation gates for quality
- Error recovery for resilience
- Progressive disclosure for efficiency

## Transformation Plan

1. **Condense description** to <500 chars while preserving all keywords
2. **Split content** to 6 separate files (REFERENCE, ENFORCEMENT, WORKFLOWS, VALIDATION, INTEGRATION, COMPLEXITY, PARALLEL)
3. **Keep core SKILL.md** <200 lines with:
   - Condensed description
   - Core purpose
   - Keyword triggers (condensed)
   - Workflow selection (visual decision tree)
   - Links to detailed files
4. **Preserve all enforcement** mechanisms in ENFORCEMENT.md
5. **Preserve all keywords** in description (condensed format)
