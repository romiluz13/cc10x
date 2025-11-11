---
name: ux-patterns
description: Context-aware UX analysis that understands user flows before checking. Use PROACTIVELY when reviewing user-facing interfaces. First understands functionality requirements and user flows, then checks for UX issues that affect functionality or user satisfaction. Provides specific improvements with examples aligned with user flows. Focuses on UX issues that block or degrade functionality, not perfect UX patterns.
allowed-tools: Read, Grep, Glob
---

# UX Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware UX analysis that understands user flows before checking. It focuses on UX issues that affect functionality or user satisfaction, providing specific improvements with examples aligned with user flows.

**Unique Value**:

- Understands user flows before checking UX
- Focuses on UX issues affecting functionality
- Provides specific improvements with examples
- Understands project's UX patterns and conventions

**When to Use**:

- After functionality is verified
- When reviewing user-facing interfaces
- When analyzing user flows
- When checking form usability

---

## Quick Start

Check UX by first understanding functionality and user flows, then checking for UX issues affecting functionality.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Check UX**: Upload button hidden → blocks user flow
3. **Provide improvement**: Make upload button prominent, add visual feedback
4. **Align with flows**: UX improvements support user flow steps

**Result:** UX issues affecting functionality identified and improved.

## Functionality First Mandate

**BEFORE applying UX checks, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (UX constraints)
   - Dependencies: What does it need?
   - Edge Cases: What can go wrong? (UX edge cases)
   - Verification: How do we know it works? (UX tests)
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type - UI Features):
   - User Flow: Step-by-step how users interact with the feature
   - Admin Flow: Step-by-step how admins manage the feature (if applicable)
   - System Flow: Step-by-step how the system processes user actions

3. **THEN understand project's UX patterns** - Before checking UX

4. **THEN check UX** - Only UX issues that affect functionality or user satisfaction

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any UX checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions
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

**Purpose**: Users need to upload files to their CRM system with clear feedback and error handling.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must display upload progress to user
- Must show success/error feedback

**User Flow**:

1. User clicks "Upload File" button
2. User selects file from device (file picker opens)
3. User sees upload progress indicator (0% → 100%)
4. User sees success message: "File uploaded successfully"
5. User sees link to view uploaded file
6. User clicks link to view file in CRM

**Functional Verification**:

- ✅ User can upload file (tested)
- ✅ File appears in CRM (tested)
- ✅ Error handling works (tested)

---

### Phase 2: Understand Project's UX Patterns (MANDATORY SECOND STEP)

**Before checking UX, understand how this project handles UX**:

1. **Load Project Context Understanding**:
   - Load `project-context-understanding` skill
   - Map project's UX patterns (loading states, error handling, form validation)
   - Identify UX conventions used
   - Identify UI component patterns used

2. **Map Loading State Patterns**:

   ```bash
   # Find loading state patterns
   grep -r "loading\|isLoading\|spinner\|skeleton" --include="*.tsx" | head -20

   # Find loading components
   find src -name "*loading*" -o -name "*spinner*" -o -name "*skeleton*"
   ```

3. **Map Error Handling Patterns**:

   ```bash
   # Find error handling patterns
   grep -r "error\|Error\|toast\|notification\|alert" --include="*.tsx" | head -20

   # Find error components
   find src -name "*error*" -o -name "*toast*" -o -name "*notification*"
   ```

4. **Map Form Validation Patterns**:

   ```bash
   # Find form validation patterns
   grep -r "validate\|validation\|form\|Form" --include="*.tsx" | head -20

   # Find form components
   find src -name "*form*" -o -name "*input*"
   ```

5. **Map Feedback Patterns**:
   ```bash
   # Find feedback patterns
   grep -r "success\|Success\|feedback\|Feedback\|message\|Message" --include="*.tsx" | head -20
   ```

**Document Project's UX Patterns**:

- Loading States: How are loading states shown? (Spinner, skeleton, progress bar?)
- Error Handling: How are errors displayed? (Toast, inline, modal?)
- Form Validation: How is validation shown? (Inline, on submit, real-time?)
- Feedback: How is success feedback shown? (Toast, inline, notification?)
- UI Components: What UI library/framework is used? (Material UI, Ant Design, custom?)

**Example Output**:

```
Project UX Patterns:
Loading States:
- Uses Skeleton components for list loading
- Uses Spinner component for button loading
- Uses ProgressBar component for file uploads

Error Handling:
- Uses Toast component for API errors
- Uses InlineError component for form errors
- Uses Modal for critical errors

Form Validation:
- Uses React Hook Form with Zod validation
- Shows inline errors on blur
- Shows success checkmark on valid input

Feedback:
- Uses Toast for success messages
- Uses InlineSuccess for form success
- Uses Notification for important updates

UI Components:
- Material UI (MUI) components
- Custom components in components/ui/
```

---

### Phase 3: UX Analysis (Only Issues Affecting Functionality or User Satisfaction)

**After understanding functionality and project UX patterns, check UX**:

1. **Map UX Issues to User Flows**:
   - For each user flow step, identify UX risks
   - Check if UX issues affect functionality or user satisfaction
   - Prioritize: Critical (blocks functionality) > Important (degrades UX) > Minor (style improvements)

2. **Check Loading States** (if affects user understanding):
   - Are loading states present and aligned with project patterns?
   - Do users know functionality is working?
   - Are loading states clear and helpful?

3. **Check Error Handling** (if affects user recovery):
   - Are error messages user-friendly and aligned with project patterns?
   - Can users understand and fix errors?
   - Are errors displayed appropriately?

4. **Check Form Validation** (if affects form completion):
   - Is validation clear and aligned with project patterns?
   - Can users complete forms successfully?
   - Is validation feedback helpful?

5. **Check Action Feedback** (if affects user confidence):
   - Is success feedback present and aligned with project patterns?
   - Do users know actions succeeded?
   - Is feedback clear and timely?

**Provide Specific Improvements with Code Examples**:

For each UX issue found, provide:

- **Issue**: Clear description of the UX issue
- **Impact**: How it affects functionality or user satisfaction
- **Location**: File path and line number
- **User Flow Step**: Which step in user flow is affected
- **Fix**: Specific code example aligned with project UX patterns
- **Priority**: Critical, Important, or Minor

**Example**:

````markdown
## UX Finding: Missing Loading State

**Issue**: File upload button shows no loading state, users don't know upload is in progress.

**Impact**: Blocks functionality - users think upload failed and click multiple times, causing duplicate uploads.

**Location**: `src/components/UploadForm.tsx:45`

**User Flow Step**: Step 3 - "User sees upload progress indicator"

**Current Code** (not aligned with project Spinner pattern):

```typescript
function UploadForm() {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (file) => {
    setUploading(true);
    await uploadFile(file);
    setUploading(false);
  };

  return (
    <button onClick={() => handleUpload(file)}>
      Upload File
    </button>
  );
}
```
````

**Fix** (aligned with project Spinner component pattern):

```typescript
import { Spinner } from '@/components/ui/Spinner';

function UploadForm() {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (file) => {
    setUploading(true);
    await uploadFile(file);
    setUploading(false);
  };

  return (
    <button onClick={() => handleUpload(file)} disabled={uploading}>
      {uploading ? (
        <>
          <Spinner size="small" />
          Uploading...
        </>
      ) : (
        'Upload File'
      )}
    </button>
  );
}
```

**Priority**: Critical (blocks functionality)

````

---

## UX Pattern Library

**Reference**: See [PATTERNS.md](./PATTERNS.md) for detailed UX patterns including:
- Loading states
- Error messages
- Form validation
- Action feedback
- Touch targets (mobile)
- Consistency patterns

---

## Priority Classification

**Critical (Must Fix - Blocks Functionality)**:

- Blocks functionality (users can't complete tasks)
- Prevents feature from working (confusing UI, missing feedback)
- Breaks user flows (can't find functionality, can't use it)
- Examples:
  - Missing loading states preventing users from knowing functionality is working
  - Poor error messages preventing users from fixing issues
  - Form validation preventing users from completing functionality

**Important (Should Fix - Degrades UX)**:

- Affects functionality negatively (frustrating UX, slow interactions)
- Degrades user experience significantly (confusing, inconsistent)
- Examples:
  - Confusing interfaces preventing users from finding functionality
  - Inconsistent patterns confusing users about how to use functionality
  - Small touch targets preventing users from interacting with functionality

**Minor (Can Defer - Style Improvements)**:

- Doesn't affect functionality (perfect UX patterns, ideal animations)
- Generic best practices (perfect form validation UX)
- Examples:
  - Perfect loading animations (if functionality works)
  - Ideal form validation UX (if functionality works)
  - Perfect consistency (if functionality works)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# UX Analysis Report

## Functionality Analysis Summary

[Brief summary of functionality and user flows from Phase 1]

## Project UX Patterns Summary

[Brief summary of project UX patterns from Phase 2]

## UX Findings

### Critical Issues (Blocks Functionality)

[For each critical issue:]

- **Issue**: [Description]
- **Impact**: [How it blocks functionality]
- **Location**: [File:line]
- **User Flow Step**: [Which step is affected]
- **Fix**: [Specific code example aligned with project UX patterns]
- **Priority**: Critical

### Important Issues (Degrades UX)

[For each important issue:]

- **Issue**: [Description]
- **Impact**: [How it degrades UX]
- **Location**: [File:line]
- **User Flow Step**: [Which step is affected]
- **Fix**: [Specific code example aligned with project UX patterns]
- **Priority**: Important

### Minor Issues (Style Improvements)

[For each minor issue:]

- **Issue**: [Description]
- **Impact**: [Why it's minor]
- **Location**: [File:line]
- **Fix**: [Specific code example - optional]
- **Priority**: Minor

## Recommendations

[Prioritized list of improvements - Critical first, then Important, then Minor]
```

---

## Usage Guidelines

### For Review Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis - especially User Flow)
2. **Then**: Complete Phase 2 (Understand Project UX Patterns)
3. **Then**: Complete Phase 3 (UX Analysis - Only Issues Affecting Functionality or User Satisfaction)
4. **Focus**: UX issues that block functionality or degrade user satisfaction significantly

### Key Principles

1. **Functionality First**: Always understand functionality and user flows before checking UX
2. **Context-Aware**: Understand project UX patterns before checking
3. **Specific Improvements**: Provide code examples aligned with project UX patterns
4. **Prioritize by Impact**: Critical (blocks functionality) > Important (degrades UX) > Minor (style improvements)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to UX checks
2. **Ignoring User Flows**: Don't check UX without understanding user flows
3. **Ignoring Project Patterns**: Don't provide generic improvements - align with project UX patterns
4. **Generic UX Checklist**: Don't check everything - focus on functionality/user satisfaction-affecting issues
5. **Missing Specific Fixes**: Don't just identify issues - provide specific code examples aligned with project patterns
6. **Wrong Priority**: Don't mark style issues as critical - prioritize by functionality/user satisfaction impact

---

## Troubleshooting

**Common Issues:**

1. **UX checks without understanding user flows**
   - **Symptom**: Finding UX issues that don't affect functionality or user satisfaction
   - **Cause**: Skipped functionality analysis or user flow understanding
   - **Fix**: Complete functionality analysis with user flows first
   - **Prevention**: Always understand user flows before UX checks

2. **Generic improvements not aligned with project patterns**
   - **Symptom**: UX improvements don't match project's UX patterns
   - **Cause**: Didn't understand project's UX patterns
   - **Fix**: Understand project patterns, provide aligned improvements
   - **Prevention**: Always understand project patterns before providing improvements

3. **Perfect UX patterns instead of functionality blockers**
   - **Symptom**: Focusing on minor UX violations instead of blockers
   - **Cause**: Didn't prioritize by functionality/user satisfaction impact
   - **Fix**: Focus on UX issues that block or degrade functionality/user satisfaction
   - **Prevention**: Always prioritize functionality/user satisfaction-affecting issues

**If issues persist:**

- Verify functionality analysis with user flows was completed first
- Check that project's UX patterns were understood
- Ensure improvements align with project patterns
- Review REFERENCE.md for UX pattern examples

---

_This skill enables context-aware UX analysis that understands user flows and project UX patterns, focusing on UX issues affecting functionality or user satisfaction, providing specific improvements with examples aligned with user flows and project patterns._
````
