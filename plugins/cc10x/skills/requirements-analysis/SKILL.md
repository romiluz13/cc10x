---
name: requirements-analysis
description: Context-aware requirements analysis that deeply understands requirements before formatting. Use PROACTIVELY when planning features. First understands functionality requirements and maps them to functionality flows, then identifies gaps and creates testable acceptance criteria. Focuses on WHAT user needs, not just requirement format. Maps requirements to functionality, identifies missing requirements, and creates testable acceptance criteria aligned with functionality flows.
allowed-tools: Read, Grep, Glob
---

# Requirements Analysis - Context-Aware & Functionality First

## Purpose

This skill provides context-aware requirements analysis that deeply understands requirements before formatting. It maps requirements to functionality, identifies gaps, and creates testable acceptance criteria aligned with functionality flows.

**Unique Value**:

- Deeply understands requirements before planning
- Maps requirements to functionality
- Identifies missing requirements
- Creates testable acceptance criteria

**When to Use**:

- When planning new features
- When gathering requirements
- When analyzing stakeholder needs
- When defining acceptance criteria

---

## Quick Start

Analyze requirements by first understanding functionality, then mapping to flows and identifying gaps.

**Example:**

1. **Understand functionality**: User needs file upload feature (User Flow: select → upload → confirm)
2. **Map requirements**: "Must accept PDF files" → maps to User Flow step 1 (file selection)
3. **Identify gaps**: Missing requirement for error handling when upload fails
4. **Create acceptance criteria**: "Given user selects invalid file type, When upload attempted, Then error message displayed"

**Result:** Requirements mapped to functionality with testable acceptance criteria.

## Examples

### Example: File Upload Feature Requirements

**Context:** Analyzing requirements for file upload feature

**Step 1: Understand Functionality**

```
User Flow:
1. User selects file
2. User uploads file
3. User sees progress
4. User gets confirmation

System Flow:
1. System receives file
2. System validates file
3. System stores file
4. System syncs to CRM
```

**Step 2: Map Requirements to Functionality**

```
Requirement: "Must accept PDF files"
→ Maps to: User Flow step 1 (file selection)
→ Maps to: System Flow step 2 (file validation)

Requirement: "Must show upload progress"
→ Maps to: User Flow step 3 (see progress)
→ Maps to: System Flow step 3 (store file)

Requirement: "Files must sync to CRM"
→ Maps to: System Flow step 4 (sync to CRM)
```

**Step 3: Identify Gaps**

```
Missing Requirements:
- Error handling when upload fails
- File size limit specification
- Invalid file type handling
- Network failure handling
```

**Step 4: Create Testable Acceptance Criteria**

```
Given user selects valid PDF file
When user uploads file
Then file is uploaded successfully
And success message is displayed

Given user selects invalid file type
When user attempts upload
Then error message "File type not supported" is displayed

Given file size exceeds 10MB
When user attempts upload
Then error message "File exceeds size limit" is displayed
```

**Result:** Requirements mapped to functionality flows with testable acceptance criteria.

## Functionality First Mandate

**BEFORE analyzing requirements format, complete context-dependent functionality analysis**:

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

**Before any requirements analysis, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions (especially Requirements - what must it do?)
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this feature supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc. - context-dependent)

3. **Understand Requirements** (from Phase 1):
   - What must it do? (specific, testable)
   - What are the constraints?
   - What are the dependencies?

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely
- Must send file metadata to CRM API
- Must display upload progress to user
- Must allow admins to view, download, and delete files

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

**Example Output**:

```
Requirements Mapping:
User Flow Requirements:
- Step 1 (User clicks button): Requirement "Must accept file uploads"
- Step 2 (User selects file): Requirement "Must validate file type and size"
- Step 3 (User sees progress): Requirement "Must display upload progress"
- Step 4 (User sees success): Requirement "Must send file metadata to CRM API"

System Flow Requirements:
- Step 1 (Receive request): Requirement "Must accept file uploads"
- Step 2 (Validate): Requirement "Must validate file type and size (max 10MB)"
- Step 3 (Store): Requirement "Must store files securely"
- Step 4 (Send to CRM): Requirement "Must send file metadata to CRM API"

Missing Requirements:
- Error handling: "Must handle upload failures gracefully"
- Admin flow: "Must allow admins to view files" (partially covered)
- Admin flow: "Must allow admins to delete files" (not covered)
```

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

4. **Check Dependencies**:
   - Are external API requirements covered?
   - Are integration requirements covered?
   - Are data format requirements covered?

**Document Gaps**:

- Missing functionality requirements
- Missing edge case requirements
- Missing constraint requirements
- Missing dependency requirements

**Example Output**:

```
Gap Analysis:
Missing Functionality Requirements:
- Admin flow: "Must allow admins to delete files"
- Error handling: "Must handle upload failures gracefully"
- Error handling: "Must show user-friendly error messages"

Missing Edge Case Requirements:
- File size exceeds limit: "Must reject files > 10MB with clear error"
- Invalid file type: "Must reject invalid file types with clear error"
- Network failure: "Must handle network failures gracefully"

Missing Constraint Requirements:
- Performance: "Upload must complete within 30 seconds"
- Scale: "Must handle 1000 concurrent uploads"
- Security: "Files must be encrypted at rest"

Missing Dependency Requirements:
- CRM API: "Must authenticate with CRM API using Bearer token"
- CRM API: "Must handle CRM API rate limits (100 req/min)"
```

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

**Provide Specific Acceptance Criteria Examples**:

For each requirement, provide:

- **Requirement**: Clear description
- **Acceptance Criteria**: Specific, testable criteria aligned with functionality flows
- **Test Cases**: Specific test cases that verify criteria

**Example**:

```markdown
## Requirement: Users can upload files

**Acceptance Criteria** (aligned with user flow):

1. **Given** user is on upload page
   **When** user clicks "Upload File" button
   **Then** file picker opens
   **And** user can select file from device

2. **Given** user has selected valid file (PDF, DOCX, JPG, PNG, < 10MB)
   **When** user clicks "Upload"
   **Then** upload progress indicator shows (0% → 100%)
   **And** file is uploaded to secure storage
   **And** file metadata is sent to CRM API
   **And** success message appears: "File uploaded successfully"
   **And** link to view file is displayed

3. **Given** user has selected invalid file type
   **When** user clicks "Upload"
   **Then** error message appears: "File type not supported. Please upload PDF, DOCX, JPG, or PNG"
   **And** file is NOT uploaded
   **And** user can select different file

**Test Cases**:

- Test: Upload valid PDF file → Should succeed
- Test: Upload file > 10MB → Should show error
- Test: Upload invalid file type → Should show error
- Test: Network failure during upload → Should show error and allow retry
```

---

## Requirements Format Patterns

**Reference**: See [REFERENCE.md](./REFERENCE.md) for detailed requirements patterns including:

- SMART criteria
- Acceptance criteria format
- User stories format
- Requirement elicitation techniques
- Scope management
- Requirements analysis checklist
- Requirements traceability matrix

---

**Critical (Must Have - Core Functionality)**:

- Core functionality (user flow, system flow)
- Blocks feature from working
- Required for MVP
- Examples:
  - User can upload files
  - System validates file type and size
  - System stores files securely

**Important (Should Have - Supporting Functionality)**:

- Supporting functionality (admin flow, error handling)
- Affects user experience
- Nice to have for MVP
- Examples:
  - Admin can view files
  - Error handling for invalid files
  - Upload progress indicator

**Minor (Can Defer - Format Compliance)**:

- Format compliance (if functionality is clear)
- Perfect documentation (if functionality is clear)
- Generic best practices

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Requirements Analysis Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Requirements Mapping

[Requirements mapped to functionality flows from Phase 2]

## Gap Analysis

[Missing requirements identified from Phase 3]

## Acceptance Criteria

[Testable acceptance criteria from Phase 4]

## Requirements (SMART Format)

[Requirements formatted using SMART criteria]

## User Stories

[User stories aligned with functionality flows]

## Scope Statement

[In scope, out of scope, constraints - based on functionality]

## Recommendations

[Prioritized list of requirements - Critical first, then Important, then Minor]
```

---

## Usage Guidelines

### For Planning Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis)
2. **Then**: Complete Phase 2 (Map Requirements to Functionality)
3. **Then**: Complete Phase 3 (Identify Gaps)
4. **Then**: Complete Phase 4 (Create Testable Acceptance Criteria)
5. **Focus**: Document WHAT user needs, not just format compliance

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

_This skill enables context-aware requirements analysis that deeply understands requirements, maps them to functionality, identifies gaps, and creates testable acceptance criteria aligned with functionality flows._

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
- Review REFERENCE.md for detailed templates
- Ensure requirements map to functionality flows
