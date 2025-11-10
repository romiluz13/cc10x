# Requirements Analysis Reference

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
