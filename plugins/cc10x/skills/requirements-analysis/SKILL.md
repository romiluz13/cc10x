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

## Requirements Format Patterns (Reference - Use AFTER Understanding Functionality)

### SMART Criteria

**Use AFTER functionality is understood**:

**Format Requirements Using SMART**:

- **Specific**: Clear, unambiguous requirement aligned with functionality
- **Measurable**: Quantifiable outcome aligned with functionality flows
- **Achievable**: Feasible with available resources and constraints
- **Relevant**: Aligned with functionality purpose
- **Time-bound**: Clear deadline for functionality delivery

**Example**:

```
BAD REQUIREMENT (No functionality understanding):
"The system should be fast"
"Users should be able to search"
"The API should be reliable"

GOOD REQUIREMENT (Functionality understood, then formatted):
Specific: "Users can upload PDF, DOCX, JPG, PNG files up to 10MB"
Measurable: "Upload completes within 30 seconds for files up to 10MB"
Achievable: "Using S3 storage and CRM API v2 with proper authentication"
Relevant: "Enables users to attach files to CRM records"
Time-bound: "Complete by end of sprint"
```

### Acceptance Criteria Format

**Use AFTER functionality flows are documented**:

**Given-When-Then Format** (aligned with functionality flows):

```
Feature: File Upload to CRM

Scenario: User uploads valid file
  Given user is on upload page
  When user selects valid file (PDF, < 10MB)
  And clicks "Upload"
  Then upload progress shows (0% → 100%)
  And file is uploaded to S3
  And file metadata is sent to CRM API
  And success message appears: "File uploaded successfully"
  And link to view file is displayed

Scenario: User uploads invalid file type
  Given user is on upload page
  When user selects invalid file type (TXT)
  And clicks "Upload"
  Then error message appears: "File type not supported"
  And file is NOT uploaded
  And user can select different file
```

### User Stories Format

**Use AFTER functionality flows are documented**:

**User Story Format** (aligned with functionality):

```
INCOMPLETE (No functionality understanding):
"As a user, I want to upload files"

COMPLETE (Functionality understood, then formatted):
"As a customer, I want to upload files to my CRM records
So that I can attach documents to customer interactions
Acceptance Criteria:
- Upload box visible on CRM record page
- Accepts PDF, DOCX, JPG, PNG files
- File size limit: 10MB
- Upload completes within 30 seconds
- Progress indicator shows upload status
- Success message confirms upload
- File appears in CRM record
- Invalid files show clear error message"
```

---

## Requirement Elicitation Techniques

### Stakeholder Interviews

**Focus on functionality, not format**:

**Questions to Ask** (aligned with functionality analysis):

1. What problem are we solving? (Purpose)
2. Who are the users? (User flows)
3. What are their pain points? (Functionality issues)
4. What success looks like? (Functional outcomes)
5. What are the constraints? (Constraints)
6. What's the timeline? (Time-bound)
7. What are the dependencies? (Dependencies)
8. How will we measure success? (Verification)

### User Story Mapping

**Map functionality flows, not just stories**:

**User Story Map** (aligned with functionality flows):

```
Epic: File Upload to CRM
|-Story 1: User Upload Flow
  |-Task: User clicks upload button (User Flow Step 1)
  |-Task: User selects file (User Flow Step 2)
  |-Task: User sees progress (User Flow Step 3)
  |-Task: User sees success (User Flow Step 4)
|-Story 2: Admin View Flow
  |-Task: Admin sees file list (Admin Flow Step 1)
  |-Task: Admin filters files (Admin Flow Step 2)
  |-Task: Admin downloads files (Admin Flow Step 3)
|-Story 3: System Integration Flow
  |-Task: System validates file (System Flow Step 2)
  |-Task: System stores file (System Flow Step 3)
  |-Task: System sends to CRM API (System Flow Step 4)
```

---

## Scope Management

### Scope Statement

**Focus on functionality scope, not generic scope**:

**In Scope** (Functionality):

- User upload flow (click → select → progress → success → view)
- Admin view flow (list → filter → download → delete)
- System integration flow (validate → store → send to CRM)
- Error handling (invalid file type, size limit, network error)

**Out of Scope** (Functionality):

- File editing (not needed for MVP)
- File versioning (not needed for MVP)
- Bulk upload (Phase 2)
- File preview (Phase 2)

**Constraints** (Functionality):

- File size: 10MB max (CRM API limit)
- File types: PDF, DOCX, JPG, PNG (CRM API supports)
- Rate limit: 100 uploads/minute (CRM API limit)

---

## Requirements Analysis Checklist

### Gathering

- [ ] All stakeholders identified
- [ ] Interviews conducted
- [ ] User stories created
- [ ] Use cases documented
- [ ] Constraints identified
- [ ] Assumptions listed
- [ ] Risks identified

### Analysis

- [ ] Requirements are clear
- [ ] Requirements are testable
- [ ] Requirements are feasible
- [ ] Requirements are necessary
- [ ] Acceptance criteria defined
- [ ] Dependencies mapped
- [ ] Conflicts resolved

### Validation

- [ ] Stakeholders approve
- [ ] Requirements are prioritized
- [ ] Effort estimated
- [ ] Timeline realistic
- [ ] Resources allocated
- [ ] Risks mitigated

### Documentation

- [ ] Requirements documented
- [ ] User stories written
- [ ] Acceptance criteria clear
- [ ] Use cases documented
- [ ] Constraints listed
- [ ] Assumptions documented
- [ ] Glossary provided

---

## Requirements Traceability Matrix

```
| ID | Requirement | User Story | Test Case | Status |
|----|-------------|-----------|-----------|--------|
| R1 | Users can register | US-1 | TC-1, TC-2 | Done |
| R2 | Email validation | US-1 | TC-3, TC-4 | In Progress |
| R3 | Password strength | US-1 | TC-5 | Pending |
```

---

## Priority Classification

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
