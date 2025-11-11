---
name: feature-planning
description: Provides feature planning guidance with functionality-first approach. Use PROACTIVELY when planning features. First understands functionality (user flow, admin flow, system flow, integration flow), then gathers requirements and prepares implementation plans. Focuses on planning functionality, not generic feature planning. Used by the planning workflow and related subagents.
allowed-tools: Read, Grep, Glob
---

# Feature Planning Guidance - Functionality First

## Functionality First Mandate

**BEFORE planning features, understand functionality**:

1. **What functionality needs to be planned?**
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?
   - What are the integration flows?

2. **THEN plan** - Plan features to support that functionality

3. **Use frameworks** - Apply planning frameworks AFTER functionality is understood

---

## Quick Start

Plan features by first understanding functionality, then creating structured implementation plan.

**Example:**

1. **Understand functionality**: User needs file upload (User Flow: select → upload → confirm)
2. **Assess complexity**: Moderate (3) - 200-500 LOC, 2-5 files
3. **Gather requirements**: Goals, user stories, acceptance criteria
4. **Create plan**: Architecture, components, risks, implementation roadmap

**Result:** Complete feature plan aligned with functionality requirements.

## Purpose

Support structured feature planning with concrete templates, examples, and decision frameworks. Ensure requirements are testable, architecture is clear, risks are mitigated, and implementation is phased.

---

## Stage 1: Complexity Assessment

### Complexity Rubric (1-5)

Use this rubric to determine if comprehensive planning is warranted:

**1 - Trivial** (<50 LOC, single function, no dependencies)

- Examples: Add validation helper, format date string
- Recommendation: Implement directly, no planning needed

**2 - Simple** (50-200 LOC, single file, minimal risk)

- Examples: Add form field, update CSS styling
- Recommendation: Brief planning (5-10 min), implement

**3 - Moderate** (200-500 LOC, 2-5 files, adds/updates tests)

- Examples: Add API endpoint, create new component
- Recommendation: Planning workflow valuable, ~30 min

**4 - Complex** (500+ LOC, 5-10 files, novel patterns or integrations)

- Examples: Authentication flow, payment integration
- Recommendation: Comprehensive planning critical, ~1-2 hours

**5 - Architectural** (1000+ LOC, 10+ files, cross-cutting changes)

- Examples: Database migration, microservice split
- Recommendation: Multi-stage planning with approval gates

**Decision Point**: If complexity ≤2, confirm with user before proceeding with full planning.

---

## Reference Materials

**For detailed templates, examples, and decision frameworks, see:**

- **REFERENCE.md**: Requirements Template, Architecture Template, Risk Register Template, Implementation Roadmap Template, Decision Frameworks, How to Fill Templates Effectively, Risk Scoring Guide, Verification Reminder, Detailed Implementation Plan Creation

---

## Stage 2: Requirements Gathering

**Use Requirements Template from REFERENCE.md** to gather requirements.

---

## Stage 3: Architecture Design

**Use Architecture Template from REFERENCE.md** to design architecture.

---

## Stage 4: Risk Analysis

**Use Risk Register Template from REFERENCE.md** to analyze risks.

---

## Stage 5: Implementation Plan

**Use Implementation Roadmap Template from REFERENCE.md** to create implementation plan.

For detailed implementation plan creation with bite-sized tasks, see REFERENCE.md section "Detailed Implementation Plan Creation".

---

## Troubleshooting

**Common Issues:**

1. **Planning without understanding functionality**
   - **Symptom**: Plan doesn't align with functionality requirements
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, then plan
   - **Prevention**: Always understand functionality before planning

2. **Complexity assessment incorrect**
   - **Symptom**: Plan too detailed for simple feature or too simple for complex feature
   - **Cause**: Didn't use complexity rubric correctly
   - **Fix**: Re-assess complexity using rubric, adjust plan accordingly
   - **Prevention**: Always use complexity rubric before planning

3. **Missing requirements or acceptance criteria**
   - **Symptom**: Plan incomplete, missing requirements
   - **Cause**: Didn't complete requirements gathering stage
   - **Fix**: Complete Stage 2 (Requirements Gathering), use template
   - **Prevention**: Always complete all planning stages

**If issues persist:**

- Verify functionality analysis was completed first
- Check that complexity was assessed correctly
- Ensure all planning stages were completed
- Review REFERENCE.md for templates and examples

---
