---
name: frontend-patterns
description: Context-aware frontend analysis covering UX, UI design, and accessibility. Use PROACTIVELY when reviewing or designing user-facing interfaces. First understands functionality requirements and user flows, then checks for UX issues, visual design problems, and accessibility blockers that affect functionality. Provides specific improvements with examples aligned with project patterns. Focuses on issues that prevent users from using functionality, not perfect UX/UI/accessibility patterns.
allowed-tools: Read, Grep, Glob
---

# Frontend Patterns - Context-Aware & Functionality First

## Purpose

This skill provides comprehensive frontend analysis covering UX, UI design, and accessibility. It understands functionality and user flows before checking, focusing on issues that prevent users from using functionality and providing specific improvements aligned with project patterns.

**Unique Value**:

- Understands user flows before checking UX/UI/accessibility
- Covers UX, UI design, and accessibility in one skill
- Focuses on issues affecting functionality
- Provides specific improvements with examples
- Understands project's frontend patterns

**When to Use**:

- After functionality is verified
- When reviewing user-facing interfaces
- When designing UI components
- When checking accessibility compliance

---

## Quick Start

Review frontend by first understanding functionality and user flows, then checking for UX, UI, and accessibility issues affecting functionality.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Understand project patterns**: Material UI, React hooks, WCAG AA
3. **Check UX**: Missing loading state → blocks user flow
4. **Check UI**: Poor visual hierarchy → hard to find functionality
5. **Check accessibility**: Missing keyboard support → blocks keyboard users
6. **Provide improvements**: Specific code examples aligned with project patterns

**Result:** UX, UI, and accessibility issues affecting functionality identified and improved.

## Functionality First Mandate

**BEFORE applying frontend checks, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (UX, accessibility constraints)
   - Dependencies: What does it need?
   - Edge Cases: What can go wrong?
   - Verification: How do we know it works?
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (UI Features):
   - User Flow: Step-by-step how users interact with the feature
   - Admin Flow: Step-by-step how admins manage the feature (if applicable)
   - System Flow: Step-by-step how the system processes user actions

3. **THEN understand project's frontend patterns** - Before checking

4. **THEN check UX, UI, accessibility** - Only issues that affect functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any frontend checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions
   - Complete Phase 2: Context-Dependent Flow Questions (UI Features - User Flow, Admin Flow, System Flow)

2. **Understand Functionality**:
   - What is this code supposed to do?
   - What functionality does user need?
   - What are the user flows? (Step-by-step user interactions)

3. **Verify Functionality Works**:
   - Does functionality work? (tested)
   - Do user flows work? (tested)
   - Does error handling work? (tested)

---

### Phase 2: Understand Project's Frontend Patterns (MANDATORY SECOND STEP)

**Before checking, understand how this project handles UX, UI, and accessibility**:

1. **Map UX Patterns**:

   ```bash
   grep -r "loading\|isLoading\|spinner\|skeleton" --include="*.tsx" | head -20
   grep -r "error\|Error\|toast\|notification\|alert" --include="*.tsx" | head -20
   grep -r "validate\|validation\|form\|Form" --include="*.tsx" | head -20
   ```

2. **Map UI Patterns**:

   ```bash
   grep -r "button\|Button\|input\|Input" --include="*.tsx" | head -20
   find src -name "*component*" -o -name "*ui*"
   ```

3. **Map Accessibility Patterns**:
   ```bash
   grep -r "aria-\|role=\|tabIndex\|alt=" --include="*.tsx" | head -20
   find src -name "*accessibility*" -o -name "*a11y*"
   ```

**Document Project's Frontend Patterns**:

- UX: Loading states, error handling, form validation, feedback patterns
- UI: Visual hierarchy, design tokens, layout systems, typography, state design
- Accessibility: Keyboard navigation, screen reader support, color contrast, focus management

---

### Phase 3: UX Analysis (Only Issues Affecting Functionality or User Satisfaction)

**After understanding functionality and project UX patterns, check UX**:

**Check Loading States** (if affects user understanding):

- Are loading states present and aligned with project patterns?
- Do users know functionality is working?
- Are loading states clear and helpful?

**Check Error Handling** (if affects user recovery):

- Are error messages user-friendly and aligned with project patterns?
- Can users understand and fix errors?
- Are errors displayed appropriately?

**Check Form Validation** (if affects form completion):

- Is validation clear and aligned with project patterns?
- Can users complete forms successfully?
- Is validation feedback helpful?

**Check Action Feedback** (if affects user confidence):

- Is success feedback present and aligned with project patterns?
- Do users know actions succeeded?
- Is feedback clear and timely?

**Priority Classification**:

- **Critical**: Blocks functionality (users can't complete tasks)
- **Important**: Degrades UX (frustrating UX, slow interactions)
- **Minor**: Style improvements (perfect UX patterns, ideal animations)

---

### Phase 4: UI Design Analysis (Only Issues Affecting Functionality)

**After understanding functionality, check UI design**:

**Check Visual Hierarchy** (if affects finding functionality):

- Does visual hierarchy guide users to functionality?
- Are important elements prominent?
- Is structure clear and aligned with functionality flows?

**Check Design Tokens** (if affects consistency):

- Are design tokens used consistently?
- Do tokens align with project theme?
- Are tokens applied correctly?

**Check Layout Systems** (if affects functionality flows):

- Does layout support functionality flows?
- Are components organized logically?
- Is spacing appropriate?

**Priority Classification**:

- **Critical**: Blocks functionality (can't find functionality, can't use it)
- **Important**: Affects functionality negatively (confusing UI, inconsistent patterns)
- **Minor**: Style improvements (perfect visual design, ideal consistency)

---

### Phase 5: Accessibility Analysis (Only Issues Affecting Functionality)

**After understanding functionality and accessibility requirements, check accessibility**:

**Check Keyboard Navigation** (if prevents access):

- Are all interactive elements keyboard accessible?
- Is tab order logical?
- Are keyboard traps present?

**Check Screen Reader Support** (if prevents understanding):

- Are form labels present?
- Are status changes announced?
- Is semantic HTML used?

**Check Color Contrast** (if prevents reading):

- Is contrast sufficient for readability?
- Are color-only indicators avoided?

**Check Focus Management** (if prevents navigation):

- Are focus indicators visible?
- Is focus order logical?
- Is focus trapped in modals?

**Priority Classification**:

- **Critical**: Blocks functionality (keyboard navigation broken, screen readers can't use it)
- **Important**: Violates WCAG (low contrast, missing focus indicators)
- **Minor**: Style improvements (perfect WCAG compliance, ideal ARIA)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Frontend Analysis Report

## Functionality Analysis Summary

[Brief summary of functionality and user flows from Phase 1]

## Project Frontend Patterns Summary

[Brief summary of project patterns from Phase 2]

## UX Findings

### Critical Issues (Blocks Functionality)

- **Issue**: [Description]
- **Impact**: [How it blocks functionality]
- **Location**: [File:line]
- **User Flow Step**: [Which step is affected]
- **Fix**: [Specific code example aligned with project UX patterns]
- **Priority**: Critical

## UI Design Findings

### Critical Issues (Blocks Functionality)

[Similar format]

## Accessibility Findings

### Critical Issues (Blocks Functionality)

[Similar format]

## Recommendations

[Prioritized list - Critical first, then Important, then Minor]
```

---

## Reference Materials

**For detailed patterns, see**:

- **UX Patterns**: Loading states, error messages, form validation, action feedback, touch targets, consistency patterns
- **UI Design Patterns**: Visual hierarchy, design tokens, layout systems, typography, state design
- **Accessibility Patterns**: Keyboard navigation, screen reader support, color contrast, focus management, semantic HTML, WCAG compliance

---

## Usage Guidelines

### For Review Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis - especially User Flow)
2. **Then**: Complete Phase 2 (Understand Project Frontend Patterns)
3. **Then**: Complete Phases 3-5 (UX, UI, Accessibility Analysis)
4. **Focus**: Issues that block functionality or prevent users from using it

### Key Principles

1. **Functionality First**: Always understand functionality and user flows before checking
2. **Context-Aware**: Understand project frontend patterns before checking
3. **Specific Improvements**: Provide code examples aligned with project patterns
4. **Prioritize by Impact**: Critical (blocks functionality) > Important (degrades UX/violates WCAG) > Minor (style improvements)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to frontend checks
2. **Ignoring User Flows**: Don't check UX/UI/accessibility without understanding user flows
3. **Ignoring Project Patterns**: Don't provide generic improvements - align with project patterns
4. **Generic Checklists**: Don't check everything - focus on functionality-blocking issues
5. **Missing Specific Fixes**: Don't just identify issues - provide specific code examples
6. **Wrong Priority**: Don't mark style issues as critical - prioritize by functionality impact

---

## Troubleshooting

**Common Issues:**

1. **Frontend checks without understanding user flows**
   - **Symptom**: Finding issues that don't affect functionality or user satisfaction
   - **Cause**: Skipped functionality analysis or user flow understanding
   - **Fix**: Complete functionality analysis with user flows first
   - **Prevention**: Always understand user flows before frontend checks

2. **Generic improvements not aligned with project patterns**
   - **Symptom**: Improvements don't match project's frontend patterns
   - **Cause**: Didn't understand project's frontend patterns
   - **Fix**: Understand project patterns, provide aligned improvements
   - **Prevention**: Always understand project patterns before providing improvements

**If issues persist:**

- Verify functionality analysis with user flows was completed first
- Check that project's frontend patterns were understood
- Ensure improvements align with project patterns

---

_This skill enables comprehensive frontend analysis covering UX, UI design, and accessibility with functionality-first approach, providing specific improvements with examples aligned with project patterns._
