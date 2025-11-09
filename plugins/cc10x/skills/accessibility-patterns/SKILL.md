---
name: accessibility-patterns
description: Context-aware accessibility analysis that understands accessibility requirements before checking. Use PROACTIVELY when reviewing user-facing interfaces. First understands functionality requirements and accessibility standards, then checks for accessibility issues that prevent users from using functionality. Provides specific fixes with code examples aligned with project patterns. Focuses on accessibility blockers (keyboard navigation, screen readers, contrast), not perfect WCAG compliance.
allowed-tools: Read, Grep, Glob
---

# Accessibility Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware accessibility analysis that understands accessibility requirements before checking. It focuses on accessibility issues that prevent users from using functionality, providing specific fixes with code examples aligned with project patterns.

**Unique Value**:

- Understands accessibility requirements before checking
- Focuses on accessibility issues affecting functionality
- Provides specific fixes with code examples
- Understands project's accessibility standards

**When to Use**:

- After functionality is verified
- When reviewing user-facing interfaces
- When building UI components
- When checking keyboard navigation and screen reader compatibility

---

## Functionality First Mandate

**BEFORE applying accessibility checks, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (Accessibility constraints: WCAG level, standards)
   - Dependencies: What does it need?
   - Edge Cases: What can go wrong? (Accessibility edge cases)
   - Verification: How do we know it works? (Accessibility tests, screen reader tests)
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type - UI Features):
   - User Flow: Step-by-step how users interact with the feature
   - Admin Flow: Step-by-step how admins manage the feature (if applicable)
   - System Flow: Step-by-step how the system processes user actions

3. **THEN understand accessibility requirements** - Before checking accessibility

4. **THEN check accessibility** - Only accessibility issues that prevent users from using functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any accessibility checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions (especially Constraints - accessibility requirements)
   - Complete Phase 2: Context-Dependent Flow Questions (UI Features - User Flow, Admin Flow, System Flow)

2. **Understand Functionality**:
   - What is this code supposed to do?
   - What functionality does user need?
   - What are the user flows? (Step-by-step user interactions)

3. **Understand User Flows** (from Phase 2):
   - How do users interact with the feature?
   - What are the user actions?
   - What are the system responses?
   - What are the user outcomes?

4. **Verify Functionality Works**:
   - Does functionality work? (tested)
   - Do user flows work? (tested)
   - Does error handling work? (tested)

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system, accessible via keyboard and screen readers.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must be accessible via keyboard navigation
- Must be accessible via screen readers
- Must display upload progress accessibly

**Constraints** (Accessibility):

- WCAG Level: AA compliance required
- Keyboard navigation: All functionality must be keyboard accessible
- Screen readers: Must announce upload progress and status

**User Flow**:

1. User clicks "Upload File" button (or presses Enter/Space)
2. User selects file from device
3. User sees upload progress (or screen reader announces progress)
4. User sees success message (or screen reader announces success)
5. User can view uploaded file

**Functional Verification**:

- ✅ User can upload file (tested)
- ✅ File appears in CRM (tested)
- ✅ Error handling works (tested)

---

### Phase 2: Understand Accessibility Requirements (MANDATORY SECOND STEP)

**Before checking accessibility, understand accessibility requirements**:

1. **Extract Accessibility Requirements from Constraints**:
   - WCAG Level: AA, AAA, or project-specific standards
   - Keyboard Navigation: All functionality must be keyboard accessible
   - Screen Readers: Must announce status and progress
   - Color Contrast: Minimum contrast ratios required
   - Focus Management: Focus indicators and focus order

2. **Map Project's Accessibility Standards**:

   ```bash
   # Find accessibility patterns
   grep -r "aria-\|role=\|tabIndex\|alt=" --include="*.tsx" | head -20

   # Find accessibility components
   find src -name "*accessibility*" -o -name "*a11y*"

   # Find accessibility utilities
   grep -r "keyboard\|screen.*reader\|focus" --include="*.ts" -i | head -20
   ```

3. **Identify Accessibility Patterns Used**:
   - ARIA patterns (aria-label, aria-describedby, aria-live)
   - Keyboard navigation patterns (tabIndex, onKeyDown)
   - Focus management patterns (focus trapping, focus restoration)
   - Screen reader patterns (aria-live regions, announcements)

**Document Accessibility Requirements**:

- WCAG Level: AA, AAA, or project-specific
- Keyboard Navigation: Requirements for keyboard accessibility
- Screen Readers: Requirements for screen reader support
- Color Contrast: Minimum contrast ratios
- Focus Management: Focus indicators and focus order
- Project Patterns: ARIA patterns, keyboard patterns, focus patterns used

**Example Output**:

```
Accessibility Requirements:
WCAG Level: AA compliance required
Keyboard Navigation:
- All interactive elements must be keyboard accessible
- Tab order must be logical
- Focus indicators must be visible

Screen Readers:
- All form inputs must have labels
- Status changes must be announced (aria-live)
- Progress must be announced

Color Contrast:
- Text: 4.5:1 for normal text, 3:1 for large text
- UI components: 3:1 for non-text content

Focus Management:
- Focus indicators: 2px solid outline
- Focus order: Logical tab order
- Focus trapping: In modals

Project Patterns:
- Uses aria-label for icon buttons
- Uses aria-live="polite" for status announcements
- Uses role="button" for custom buttons
```

---

### Phase 3: Accessibility Analysis (Only Issues Affecting Functionality)

**After understanding functionality and accessibility requirements, check accessibility**:

1. **Map Accessibility Issues to User Flows**:
   - For each user flow step, identify accessibility risks
   - Check if accessibility issues prevent users from using functionality
   - Prioritize: Critical (blocks functionality) > Important (violates WCAG) > Minor (style improvements)

2. **Check Keyboard Navigation** (if prevents access):
   - Are all interactive elements keyboard accessible?
   - Is tab order logical?
   - Are keyboard traps present?

3. **Check Screen Reader Support** (if prevents understanding):
   - Are form labels present?
   - Are status changes announced?
   - Is semantic HTML used?

4. **Check Color Contrast** (if prevents reading):
   - Is contrast sufficient for readability?
   - Are color-only indicators avoided?

5. **Check Focus Management** (if prevents navigation):
   - Are focus indicators visible?
   - Is focus order logical?
   - Is focus trapped in modals?

**Provide Specific Fixes with Code Examples**:

For each accessibility issue found, provide:

- **Issue**: Clear description of the accessibility issue
- **Impact**: How it prevents users from using functionality
- **Location**: File path and line number
- **User Flow Step**: Which step in user flow is affected
- **Fix**: Specific code example aligned with project accessibility patterns
- **Priority**: Critical, Important, or Minor

**Example**:

````markdown
## Accessibility Finding: Missing Keyboard Support

**Issue**: File upload button is a div with onClick, not keyboard accessible.

**Impact**: Blocks functionality - keyboard users cannot upload files, breaking file upload feature.

**Location**: `src/components/UploadForm.tsx:45`

**User Flow Step**: Step 1 - "User clicks 'Upload File' button (or presses Enter/Space)"

**Current Code** (not keyboard accessible):

```tsx
<div onClick={handleUpload} className="upload-button">
  Upload File
</div>
```
````

**Fix** (aligned with project button pattern and keyboard support):

```tsx
<button
  onClick={handleUpload}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleUpload();
    }
  }}
  className="upload-button"
>
  Upload File
</button>
```

**Priority**: Critical (blocks functionality)

````

---

## Accessibility Pattern Library (Reference - Use AFTER Understanding Accessibility Requirements)

### Keyboard Navigation

**Understand accessibility requirements first, then check**:

**Keyboard Accessible Buttons** (aligned with project pattern):
```tsx
// Check: Is button keyboard accessible?
// BAD - Div as button (flag if prevents access)
<div onClick={handleClick}>Submit</div>

// GOOD - Proper button (aligned with project pattern)
<button onClick={handleClick}>Submit</button>

// GOOD - Custom element with keyboard support (aligned with project pattern)
<span
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Submit
</span>
````

### Screen Reader Support

**Understand accessibility requirements first, then check**:

**Form Labels** (aligned with project pattern):

```tsx
// Check: Are form inputs labeled?
// BAD - No label (flag if prevents screen reader users)
<input type="text" placeholder="Email" />

// GOOD - Proper label (aligned with project pattern)
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// GOOD - aria-label (aligned with project pattern)
<input type="email" aria-label="Email address" />
```

**Alt Text** (aligned with project pattern):

```tsx
// Check: Are images accessible?
// BAD - Missing alt text (flag if prevents understanding)
<img src="logo.png" />

// GOOD - Descriptive alt text (aligned with project pattern)
<img src="logo.png" alt="Company name logo" />

// GOOD - Decorative image hidden (aligned with project pattern)
<img src="decoration.png" alt="" aria-hidden="true" />
```

**Status Announcements** (aligned with project pattern):

```tsx
// Check: Are status changes announced?
// BAD - No announcement (flag if prevents understanding)
<div>{uploadStatus}</div>

// GOOD - aria-live announcement (aligned with project aria-live pattern)
<div aria-live="polite" aria-atomic="true">
  {uploadStatus}
</div>
```

### Color Contrast

**Understand accessibility requirements first, then check**:

**Color Contrast** (only flag if prevents reading):

```css
/* Check: Is contrast sufficient? */
/* BAD - Low contrast (flag if prevents reading) */
color: #7b7b7b;
background: #cccccc; /* 3.2:1 - fails WCAG AA */

/* GOOD - WCAG AA compliant (aligned with project 4.5:1 requirement) */
color: #5a5a5a;
background: #ffffff; /* 4.5:1 - passes WCAG AA */
```

### Focus Management

**Understand accessibility requirements first, then check**:

**Focus Indicators** (aligned with project pattern):

```css
/* Check: Are focus indicators visible? */
/* BAD - Missing focus indicator (flag if prevents navigation) */
button:focus {
  outline: none; /* Bad! */
}

/* GOOD - Visible focus indicator (aligned with project 2px solid outline pattern) */
button:focus {
  outline: 2px solid blue;
  outline-offset: 2px;
}
```

**Semantic HTML** (aligned with project pattern):

```tsx
// Check: Is semantic HTML used?
// BAD - Div soup (flag if prevents understanding)
<div onClick={handleClick}>
  <div>Submit</div>
</div>

// GOOD - Semantic HTML (aligned with project pattern)
<button onClick={handleClick}>
  Submit
</button>
```

---

## Priority Classification

**Critical (Must Fix - Blocks Functionality)**:

- Blocks functionality (keyboard navigation broken, screen readers can't use it)
- Prevents feature from working (missing labels, keyboard traps)
- Breaks user flows (can't navigate, can't understand)
- Examples:
  - Missing keyboard support preventing users from accessing functionality
  - Missing labels preventing screen reader users from using functionality
  - Keyboard traps preventing users from navigating functionality

**Important (Should Fix - Violates WCAG)**:

- Affects functionality negatively (low contrast, missing focus indicators)
- Violates WCAG requirements (fails AA compliance)
- Examples:
  - Low contrast preventing users from reading functionality
  - Missing focus indicators preventing users from navigating functionality
  - Non-semantic HTML preventing screen readers from understanding functionality

**Minor (Can Defer - Style Improvements)**:

- Doesn't affect functionality (perfect WCAG compliance, ideal ARIA)
- Generic best practices (perfect contrast ratios)
- Examples:
  - Perfect WCAG AAA compliance (if AA is met)
  - Ideal ARIA patterns (if functionality is accessible)
  - Perfect color contrast ratios (if readable)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Accessibility Analysis Report

## Functionality Analysis Summary

[Brief summary of functionality and user flows from Phase 1]

## Accessibility Requirements Summary

[Brief summary of accessibility requirements from Phase 2]

## Accessibility Findings

### Critical Issues (Blocks Functionality)

[For each critical issue:]

- **Issue**: [Description]
- **Impact**: [How it blocks functionality]
- **Location**: [File:line]
- **User Flow Step**: [Which step is affected]
- **Fix**: [Specific code example aligned with project accessibility patterns]
- **Priority**: Critical

### Important Issues (Violates WCAG)

[For each important issue:]

- **Issue**: [Description]
- **Impact**: [How it violates WCAG]
- **Location**: [File:line]
- **User Flow Step**: [Which step is affected]
- **Fix**: [Specific code example aligned with project accessibility patterns]
- **Priority**: Important

### Minor Issues (Style Improvements)

[For each minor issue:]

- **Issue**: [Description]
- **Impact**: [Why it's minor]
- **Location**: [File:line]
- **Fix**: [Specific code example - optional]
- **Priority**: Minor

## Recommendations

[Prioritized list of fixes - Critical first, then Important, then Minor]
```

---

## Usage Guidelines

### For Review Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis - especially User Flow)
2. **Then**: Complete Phase 2 (Understand Accessibility Requirements)
3. **Then**: Complete Phase 3 (Accessibility Analysis - Only Issues Affecting Functionality)
4. **Focus**: Accessibility issues that block functionality or violate WCAG requirements

### Key Principles

1. **Functionality First**: Always understand functionality and user flows before checking accessibility
2. **Requirements-Driven**: Understand accessibility requirements before checking
3. **Specific Fixes**: Provide code examples aligned with project accessibility patterns
4. **Prioritize by Impact**: Critical (blocks functionality) > Important (violates WCAG) > Minor (style improvements)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to accessibility checks
2. **Ignoring User Flows**: Don't check accessibility without understanding user flows
3. **Ignoring Project Patterns**: Don't provide generic fixes - align with project accessibility patterns
4. **Generic WCAG Checklist**: Don't check everything - focus on functionality-blocking issues
5. **Missing Specific Fixes**: Don't just identify issues - provide specific code examples aligned with project patterns
6. **Wrong Priority**: Don't mark style issues as critical - prioritize by functionality impact

---

_This skill enables context-aware accessibility analysis that understands accessibility requirements and focuses on accessibility issues preventing users from using functionality, providing specific fixes with code examples aligned with project accessibility patterns._
