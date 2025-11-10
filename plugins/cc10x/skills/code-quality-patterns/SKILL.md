---
name: code-quality-patterns
description: Context-aware code quality analysis that understands codebase standards before checking. Use PROACTIVELY when reviewing code that implements features. First understands project's codebase conventions and functionality requirements, then checks for quality issues that affect functionality or make it hard to maintain. Provides specific improvements with examples aligned with project patterns. Focuses on quality issues that matter (blocks changes, causes bugs, hard to understand), not generic code quality metrics.
allowed-tools: Read, Grep, Glob
---

# Code Quality Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware code quality analysis that understands the codebase's quality standards before checking. It focuses on quality issues that affect functionality or maintainability, providing specific improvements with examples aligned with project patterns.

**Unique Value**:

- Understands codebase's quality standards before checking
- Focuses on quality issues that matter (maintainability, readability)
- Provides specific improvements with examples
- Respects existing patterns and conventions

**When to Use**:

- After functionality is verified
- When reviewing code that implements features
- When analyzing code for maintainability issues
- When checking if code can be easily modified

---

## Functionality First Mandate

**BEFORE applying quality checks, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits?
   - Dependencies: What does it need?
   - Edge Cases: What can go wrong?
   - Verification: How do we know it works?
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type):
   - UI Features → User Flow, Admin Flow, System Flow
   - Backend APIs → Request Flow, Response Flow, Error Flow, Data Flow
   - Utilities → Input Flow, Processing Flow, Output Flow, Error Flow
   - Integrations → Integration Flow, Data Flow, Error Flow, State Flow

3. **THEN understand codebase conventions** - Before checking quality

4. **THEN check quality** - Only quality issues that affect functionality or maintainability

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any quality checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this code supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc. - context-dependent)

3. **Verify Functionality Works**:
   - Does functionality work? (tested)
   - Do flows work? (tested)
   - Does error handling work? (tested)

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely
- Must send file metadata to CRM API
- Must display upload progress to user

**User Flow**:

1. User clicks "Upload File" button
2. User selects file from device
3. User sees upload progress indicator
4. User sees success message with file link

**System Flow**:

1. System receives file upload request
2. System validates file type and size
3. System stores file in secure storage
4. System sends file metadata to CRM API
5. System returns success response

**Functional Verification**:

- ✅ User can upload file (tested)
- ✅ File appears in CRM (tested)
- ✅ Error handling works (tested)

---

### Phase 2: Understand Codebase Conventions (MANDATORY SECOND STEP)

**Before checking quality, understand how this codebase maintains quality**:

1. **Load Project Context Understanding**:
   - Load `project-context-understanding` skill
   - Map codebase conventions (naming, structure, style)
   - Identify quality patterns used
   - Identify testing patterns used

2. **Map Naming Conventions**:

   ```bash
   # Find file naming patterns
   ls -R src/ | grep -E "\.(ts|tsx|js|jsx)$" | head -20

   # Find function naming patterns
   grep -r "function \|const \|export const " --include="*.ts" | head -20

   # Find component naming patterns
   grep -r "export.*function\|export.*const.*=" --include="*.tsx" | head -20
   ```

3. **Map Structure Conventions**:

   ```bash
   # Find directory structure
   find src -type d -maxdepth 3

   # Find file organization patterns
   find src -name "*.ts" -o -name "*.tsx" | head -20
   ```

4. **Map Style Conventions**:

   ```bash
   # Read style guide if exists
   cat .eslintrc.json 2>/dev/null || cat .prettierrc 2>/dev/null || echo "No style config found"

   # Analyze code style from examples
   head -50 src/components/UploadForm.tsx 2>/dev/null || echo "File not found"
   ```

5. **Map Quality Patterns**:

   ```bash
   # Find testing patterns
   find . -name "*.test.*" -o -name "*.spec.*" | head -10

   # Find error handling patterns
   grep -r "try\|catch\|throw" --include="*.ts" | head -20

   # Find code organization patterns
   grep -r "export.*class\|export.*interface\|export.*type" --include="*.ts" | head -20
   ```

**Document Codebase Conventions**:

- Naming: Files (kebab-case?), Functions (camelCase?), Components (PascalCase?), Constants (UPPER_SNAKE_CASE?)
- Structure: Directory organization, file organization, module boundaries
- Style: Formatting rules, linting rules, indentation
- Quality Patterns: Testing patterns, error handling patterns, code organization patterns

**Example Output**:

```
Codebase Conventions:
Naming:
- Files: kebab-case (upload-form.tsx)
- Components: PascalCase (UploadForm)
- Functions: camelCase (uploadFile)
- Constants: UPPER_SNAKE_CASE (MAX_FILE_SIZE)

Structure:
- Components in components/
- Pages in pages/
- API routes in api/
- Services in services/
- Utils in utils/

Style:
- TypeScript strict mode
- ESLint with React plugin
- Prettier for formatting
- 2-space indentation

Quality Patterns:
- Testing: Jest with React Testing Library
- Error Handling: Try-catch with custom error classes
- Code Organization: Functional components with hooks
```

---

### Phase 3: Quality Analysis (Only Issues Affecting Functionality or Maintainability)

**After understanding functionality and codebase conventions, check quality**:

1. **Map Quality Issues to Functionality**:
   - For each functionality flow, identify quality risks
   - Check if quality issues affect functionality or maintainability
   - Prioritize: Critical (blocks changes) > Important (causes bugs) > Minor (hard to understand) > Style

2. **Check Readability** (if affects understanding functionality):
   - Is code readable enough to understand what it does?
   - Are names clear and aligned with codebase conventions?
   - Is structure clear and aligned with codebase patterns?
   - Are comments helpful (if needed)?

3. **Check Maintainability** (if affects modifying functionality):
   - Is code organized to support changes?
   - Are functions/classes focused and aligned with codebase patterns?
   - Is duplication preventing fixing bugs in one place?
   - Are dependencies clear and manageable?

4. **Check Error Handling** (if affects functionality):
   - Is error handling present and aligned with codebase patterns?
   - Are errors handled gracefully?
   - Are error messages helpful?

5. **Check Testability** (if affects verifying functionality):
   - Is code testable?
   - Are tests present and aligned with codebase testing patterns?
   - Can functionality be verified with tests?

**Provide Specific Improvements with Code Examples**:

For each quality issue found, provide:

- **Issue**: Clear description of the quality issue
- **Impact**: How it affects functionality or maintainability
- **Location**: File path and line number
- **Fix**: Specific code example aligned with codebase patterns
- **Priority**: Critical, Important, or Minor

**Example**:

````markdown
## Quality Finding: Unclear Function Name

**Issue**: Function name `process` doesn't indicate what it does, making it hard to understand functionality.

**Impact**: Blocks changes - developers can't understand what this function does without reading implementation.

**Location**: `src/services/file-service.ts:23`

**Current Code** (not aligned with codebase camelCase pattern):

```typescript
function process(file: File): Promise<string> {
  // Validates, uploads, and syncs file
  await validateFile(file);
  const url = await uploadToStorage(file);
  await syncToCRM(url);
  return url;
}
```
````

**Fix** (aligned with codebase camelCase pattern and naming conventions):

```typescript
function uploadAndSyncFile(file: File): Promise<string> {
  // Validates, uploads, and syncs file to CRM
  await validateFile(file);
  const url = await uploadToStorage(file);
  await syncToCRM(url);
  return url;
}
```

**Priority**: Important (affects maintainability)

````

---

## Reference Materials

**For detailed patterns and reference materials, see:**

- **PATTERNS.md**: Quality Pattern Library (naming, organization, error handling, testing, duplication, complexity) and SOLID Principles
- **REFERENCE.md**: Verification checklist and code quality metrics

---

## Priority Classification

**Critical (Must Fix - Blocks Changes)**:

- Blocks changes (unreadable code, high complexity preventing understanding)
- Prevents fixing bugs (duplication requiring fixes in multiple places)
- Examples:
  - Unclear naming preventing understanding functionality
  - High complexity preventing understanding flow
  - Duplication preventing fixing bugs in one place

**Important (Should Fix - Causes Bugs or Affects Maintainability)**:

- Causes bugs (missing error handling, unclear logic)
- Affects maintainability (long functions, large classes, deep nesting)
- Examples:
  - Missing error handling breaking functionality
  - Long functions making it hard to modify functionality
  - Missing tests making it hard to verify functionality

**Minor (Can Defer - Hard to Understand or Style Issues)**:

- Hard to understand (but functionality works)
- Style issues (naming conventions, formatting)
- Examples:
  - Complexity metrics (if code works and is readable)
  - Perfect SOLID principles (if code works)
  - File size (if code works and is organized)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Code Quality Analysis Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Codebase Conventions Summary

[Brief summary of codebase conventions from Phase 2]

## Quality Findings

### Critical Issues (Blocks Changes)

[For each critical issue:]

- **Issue**: [Description]
- **Impact**: [How it blocks changes or causes bugs]
- **Location**: [File:line]
- **Fix**: [Specific code example aligned with codebase patterns]
- **Priority**: Critical

### Important Issues (Causes Bugs or Affects Maintainability)

[For each important issue:]

- **Issue**: [Description]
- **Impact**: [How it causes bugs or affects maintainability]
- **Location**: [File:line]
- **Fix**: [Specific code example aligned with codebase patterns]
- **Priority**: Important

### Minor Issues (Hard to Understand or Style)

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

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis)
2. **Then**: Complete Phase 2 (Understand Codebase Conventions)
3. **Then**: Complete Phase 3 (Quality Analysis - Only Issues Affecting Functionality or Maintainability)
4. **Focus**: Quality issues that block changes, cause bugs, or make code hard to understand

### Key Principles

1. **Functionality First**: Always understand functionality before checking quality
2. **Context-Aware**: Understand codebase conventions before checking
3. **Specific Improvements**: Provide code examples aligned with codebase patterns
4. **Prioritize by Impact**: Critical (blocks changes) > Important (causes bugs) > Minor (hard to understand) > Style

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to quality checks
2. **Ignoring Codebase Conventions**: Don't provide generic improvements - align with codebase patterns
3. **Generic Quality Metrics**: Don't check everything - focus on functionality/maintainability-affecting issues
4. **Missing Specific Fixes**: Don't just identify issues - provide specific code examples aligned with codebase
5. **Wrong Priority**: Don't mark style issues as critical - prioritize by functionality/maintainability impact
6. **No Code Examples**: Don't just describe issues - show how to fix them aligned with codebase patterns

---

_This skill enables context-aware code quality analysis that understands codebase conventions and focuses on quality issues affecting functionality or maintainability, providing specific improvements with examples aligned with project patterns._
````
