---
name: planning-patterns
description: Context-aware planning guidance covering requirements analysis and feature planning. Use PROACTIVELY when planning features. First understands functionality requirements and maps them to functionality flows, then gathers requirements, identifies gaps, and creates testable acceptance criteria. Focuses on planning functionality, not generic feature planning. Provides structured planning templates and decision frameworks.
allowed-tools: Read, Grep, Glob
---

# Planning Patterns - Context-Aware & Functionality First

## Purpose

This skill provides comprehensive planning guidance covering requirements analysis, tech stack research, feature planning, and technical writing. It deeply understands requirements before formatting, maps requirements to functionality, identifies gaps, creates testable acceptance criteria, evaluates technology options, and structures documentation.

**Unique Value**:

- Deeply understands requirements before planning (Socratic questioning, stakeholder analysis)
- Maps requirements to functionality flows
- Identifies missing requirements
- Creates testable acceptance criteria
- Provides tech stack research with 2-3 options and trade-offs
- Feature planning with solo developer estimation (double initial estimate)
- Technical writing with audience-first, examples-first approach
- Provides structured planning templates

**When to Use**:

- When planning new features
- When gathering requirements
- When analyzing stakeholder needs
- When defining acceptance criteria
- When researching technology options
- When writing technical documentation

---

## Quick Start

Plan features by first understanding functionality, then mapping requirements to flows and identifying gaps.

**Example:**

1. **Understand functionality**: User needs file upload (User Flow: select → upload → confirm)
2. **Map requirements**: "Must accept PDF files" → maps to User Flow step 1 (file selection)
3. **Identify gaps**: Missing requirement for error handling when upload fails
4. **Create acceptance criteria**: "Given user selects invalid file type, When upload attempted, Then error message displayed"
5. **Assess complexity**: Moderate (3) - 200-500 LOC, 2-5 files
6. **Create plan**: Architecture, components, risks, implementation roadmap

**Result:** Requirements mapped to functionality with testable acceptance criteria and implementation plan.

## Functionality First Mandate

**BEFORE planning features, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do? (specific, testable)
   - Constraints: What are the limits?
   - Dependencies: What does it need?
   - Edge Cases: What can go wrong?
   - Verification: How do we know it works? (Acceptance criteria)
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type):
   - UI Features → User Flow, Admin Flow, System Flow
   - Backend APIs → Request Flow, Response Flow, Error Flow, Data Flow
   - Integrations → Integration Flow, Data Flow, Error Flow, State Flow
   - Database → Migration Flow, Query Flow, Data Flow, State Flow

3. **THEN map requirements to functionality** - Map requirements to flows

4. **THEN identify gaps** - Identify missing requirements

5. **THEN create acceptance criteria** - Create testable acceptance criteria

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any planning, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions (especially Requirements - what must it do?)
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this feature supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc.)

---

### Phase 2: Map Requirements to Functionality (MANDATORY SECOND STEP)

**After understanding functionality, map requirements to functionality flows**:

1. **Map Requirements to User Flows**:
   - For each requirement, identify which user flow steps it supports
   - Map requirements to user actions and system responses

2. **Map Requirements to System Flows**:
   - For each requirement, identify which system flow steps it supports
   - Map requirements to system processing steps

3. **Map Requirements to Integration Flows** (if applicable):
   - For each requirement, identify which integration flow steps it supports
   - Map requirements to external system interactions

4. **Identify Missing Requirements**:
   - Check if all functionality flows have requirements
   - Check if all user actions have requirements
   - Check if all system responses have requirements
   - Check if all error cases have requirements

**Document Requirements Mapping**:

- Requirements mapped to user flows
- Requirements mapped to system flows
- Requirements mapped to integration flows
- Missing requirements identified

---

### Phase 3: Identify Gaps (MANDATORY THIRD STEP)

**After mapping requirements, identify gaps**:

1. **Check Functionality Coverage**:
   - Are all user flows covered by requirements?
   - Are all admin flows covered by requirements?
   - Are all system flows covered by requirements?
   - Are all integration flows covered by requirements?

2. **Check Edge Cases**:
   - Are error cases covered by requirements?
   - Are boundary conditions covered by requirements?
   - Are failure scenarios covered by requirements?

3. **Check Constraints**:
   - Are performance constraints covered by requirements?
   - Are scale constraints covered by requirements?
   - Are security constraints covered by requirements?

**Document Gaps**:

- Missing functionality requirements
- Missing edge case requirements
- Missing constraint requirements
- Missing dependency requirements

---

### Phase 4: Create Testable Acceptance Criteria (MANDATORY FOURTH STEP)

**After identifying gaps, create testable acceptance criteria**:

1. **Create Acceptance Criteria for User Flows**:
   - For each user flow step, create testable acceptance criteria
   - Criteria should be specific, measurable, and testable

2. **Create Acceptance Criteria for System Flows**:
   - For each system flow step, create testable acceptance criteria
   - Criteria should verify system behavior

3. **Create Acceptance Criteria for Error Cases**:
   - For each error case, create testable acceptance criteria
   - Criteria should verify error handling

4. **Format Acceptance Criteria**:
   - Use Given-When-Then format (if applicable)
   - Use specific, testable language
   - Include expected outcomes

---

### Phase 5: Complexity Assessment

**Assess complexity to determine planning depth**:

**Complexity Rubric (1-5)**:

- **1 - Trivial** (<50 LOC, single function, no dependencies) → Implement directly
- **2 - Simple** (50-200 LOC, single file, minimal risk) → Brief planning (5-10 min)
- **3 - Moderate** (200-500 LOC, 2-5 files, adds/updates tests) → Planning workflow valuable (~30 min)
- **4 - Complex** (500+ LOC, 5-10 files, novel patterns or integrations) → Comprehensive planning critical (~1-2 hours)
- **5 - Architectural** (1000+ LOC, 10+ files, cross-cutting changes) → Multi-stage planning with approval gates

**Decision Point**: If complexity ≤2, confirm with user before proceeding with full planning.

---

### Phase 6: Create Implementation Plan

**After complexity assessment, create implementation plan**:

1. **Architecture Design**: Map functionality to architecture (user flows → components)
2. **Component Design**: Design components to support functionality flows
3. **Risk Analysis**: Identify risks affecting functionality
4. **Implementation Roadmap**: Create phased implementation plan

**Bite-Sized Task Granularity**:

- Each step is one action (2-5 minutes)
- If tests included: "Write failing test" → "Run to fail" → "Implement minimal code" → "Run to pass" → "Commit"
- If no tests: "Implement code" → "Verify with typecheck/lint" → "Commit"

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Planning Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Requirements Mapping

[Requirements mapped to functionality flows from Phase 2]

## Gap Analysis

[Missing requirements identified from Phase 3]

## Acceptance Criteria

[Testable acceptance criteria from Phase 4]

## Complexity Assessment

[Complexity score and rationale from Phase 5]

## Implementation Plan

[Architecture, components, risks, roadmap from Phase 6]

## Requirements (SMART Format)

[Requirements formatted using SMART criteria]

## User Stories

[User stories aligned with functionality flows]

## Scope Statement

[In scope, out of scope, constraints - based on functionality]

## Recommendations

[Prioritized list - Critical first, then Important, then Minor]
```

---

## Reference Materials

**For detailed templates and frameworks, see**:

- **PATTERNS.md**: Complete pattern library covering requirements analysis, tech stack research, feature planning, technical writing
- **Requirements Template**: SMART criteria, acceptance criteria format, user stories format
- **Tech Stack Research**: Technology evaluation, comparison framework, trade-off analysis, context analysis
- **Feature Planning**: Feature breakdown, solo developer estimation, phased implementation, success criteria
- **Technical Writing**: Audience-first writing, documentation structure, writing quality patterns
- **Architecture Template**: System context, containers, components, data models
- **Risk Register Template**: Risk identification, probability, impact, mitigation
- **Implementation Roadmap Template**: Phased implementation, dependencies, milestones

---

## Usage Guidelines

### For Planning Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis)
2. **Then**: Complete Phase 2 (Map Requirements to Functionality)
3. **Then**: Complete Phase 3 (Identify Gaps)
4. **Then**: Complete Phase 4 (Create Testable Acceptance Criteria)
5. **Then**: Complete Phase 5 (Complexity Assessment)
6. **Then**: Complete Phase 6 (Create Implementation Plan)
7. **Focus**: Document WHAT user needs, not just format compliance

### Key Principles

1. **Functionality First**: Always understand functionality before formatting requirements
2. **Map to Flows**: Map requirements to functionality flows
3. **Identify Gaps**: Identify missing requirements
4. **Testable Criteria**: Create testable acceptance criteria aligned with flows
5. **Prioritize by Impact**: Critical (core functionality) > Important (supporting functionality) > Minor (format compliance)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to requirements formatting
2. **Generic Requirements**: Don't write generic requirements - map to functionality flows
3. **Missing Gaps**: Don't assume all requirements are present - identify gaps
4. **Vague Acceptance Criteria**: Don't write vague criteria - make them testable and aligned with flows
5. **Format Over Functionality**: Don't prioritize format over functionality understanding
6. **No Mapping**: Don't just list requirements - map them to functionality flows

---

## Troubleshooting

**Common Issues:**

1. **Requirements don't map to functionality flows**
   - **Symptom**: Requirements listed but not connected to user/system flows
   - **Cause**: Skipped Phase 2 (Map Requirements to Functionality)
   - **Fix**: Complete Phase 2, map each requirement to flow steps
   - **Prevention**: Always complete functionality analysis before mapping

2. **Missing requirements not identified**
   - **Symptom**: Gaps found later during implementation
   - **Cause**: Skipped Phase 3 (Identify Gaps)
   - **Fix**: Complete Phase 3, check all flows for missing requirements
   - **Prevention**: Always check functionality coverage after mapping

3. **Acceptance criteria not testable**
   - **Symptom**: Criteria vague, can't write tests from them
   - **Cause**: Didn't align criteria with functionality flows
   - **Fix**: Rewrite criteria aligned with flow steps, make them specific
   - **Prevention**: Always create criteria from functionality flows

**If issues persist:**

- Verify functionality analysis was completed first
- Check that all phases were completed in order
- Ensure requirements map to functionality flows

---

_This skill enables context-aware planning that deeply understands requirements, maps them to functionality, identifies gaps, and creates testable acceptance criteria aligned with functionality flows._
