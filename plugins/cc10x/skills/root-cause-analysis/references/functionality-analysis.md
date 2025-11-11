# Functionality Analysis - Context-Dependent

**Reference**: Part of `root-cause-analysis` skill. See main SKILL.md for overview.

## Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**CRITICAL**: Before analyzing root causes, understand expected functionality using context-dependent analysis.

## Process

### 1. Detect Code Type

Identify if this is:

- **UI**: User interface components, forms, pages
- **API**: REST endpoints, GraphQL resolvers, service APIs
- **Utility**: Helper functions, utilities, shared code
- **Integration**: External service integrations, third-party APIs
- **Database**: Queries, migrations, data access
- **Configuration**: Config files, environment setup
- **CLI**: Command-line tools, scripts
- **Background Job**: Scheduled tasks, workers, queues

### 2. Universal Questions First

Answer these questions for expected functionality:

**Purpose**: What should this functionality do? Why does it exist?

**Requirements**: What must the functionality do? What are the must-have features?

**Constraints**: What are the limits? Performance, scale, security, storage?

**Dependencies**: What does this functionality depend on? Files, APIs, services, libraries?

**Edge Cases**: What edge cases must be handled? Error scenarios, boundary conditions?

**Verification**: How do we verify functionality works? Tests, acceptance criteria, success metrics?

**Context**: Where is this functionality? Location, codebase structure, architecture?

### 3. Context-Dependent Flows

Answer flow questions based on code type:

**UI**: User Flow, Admin Flow, System Flow
**API**: Request Flow, Response Flow, Error Flow, Data Flow
**Integration**: Integration Flow, Data Flow, Error Flow, State Flow
**Database**: Migration Flow, Query Flow, Data Flow, State Flow
**Background Jobs**: Job Flow, Processing Flow, State Flow, Error Flow
**CLI**: Command Flow, Processing Flow, Output Flow, Error Flow
**Configuration**: Configuration Flow, Validation Flow, Error Flow
**Utility**: Input Flow, Processing Flow, Output Flow, Error Flow

## Example: File Upload Broken (UI Feature)

**Universal Questions (Expected)**:

**Purpose**: Users should be able to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements (Expected)**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely in S3
- Must send file metadata to CRM API
- Must display upload progress to user
- Must handle errors gracefully

**Constraints**:

- Performance: Upload must complete within 30 seconds for files up to 10MB
- Scale: Must handle 100 concurrent uploads
- Security: Files must be encrypted at rest, access controlled
- Storage: 100GB storage limit

**Dependencies**:

- Files: `components/UploadForm.tsx`, `api/files.ts`, `services/storage.ts`, `services/crm-client.ts`
- APIs: CRM API (POST /crm/files)
- Services: S3 storage service, CRM API service
- Libraries: `aws-sdk`, `axios`, `react-dropzone`

**Edge Cases**:

- File exceeds size limit
- Invalid file type
- Network failure during upload
- CRM API unavailable
- Storage quota exceeded

**Verification**:

- E2E tests: Complete user flow from upload to CRM visibility
- Acceptance criteria: File appears in CRM within 5 seconds
- Success metrics: 99% upload success rate, <30s upload time

**Context**:

- Location: `src/features/file-upload/`
- Codebase structure: React frontend, Node.js backend, PostgreSQL database
- Architecture: MVC pattern, RESTful API

**Context-Dependent Flows (Expected - UI Feature)**:

**User Flow (Expected)**:

1. User navigates to "Upload File" page
2. User selects file from device
3. User sees upload progress indicator (0% → 100%)
4. User sees success message: "File uploaded successfully"
5. User sees link to view uploaded file

**System Flow (Expected)**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type and size
3. System stores file in secure storage (S3 bucket)
4. System sends file metadata to CRM API
5. System stores file record in database
6. System returns success response to user

**Integration Flow (Expected)**:

1. System sends file metadata to CRM API (POST /crm/files)
2. CRM API stores file reference
3. CRM API returns file ID
4. System receives response and updates local record

**Observed Behavior (What's Broken)**:

- ❌ User Flow Broken: User clicks upload → nothing happens (no progress, no response)
- ❌ System Flow Broken: No server logs, no API call, file not stored

**THEN Root Cause Analysis**: Identify why functionality breaks.

## Mapping Observed to Expected

**Key Step**: Compare observed behavior to expected flows:

- Expected: User sees upload progress → Observed: No progress indicator
- Expected: System receives request → Observed: No request received
- Expected: System validates file → Observed: Validation never runs
- Expected: System stores file → Observed: File not stored

**Divergence Point**: User clicks upload → nothing happens (expected: progress shown)

**Focus**: Root cause analysis on the divergence point.

## Functionality Analysis Checklist

After functionality analysis:

- [ ] Code type identified
- [ ] Universal questions answered
- [ ] Context-dependent flows defined
- [ ] Observed behavior mapped to expected
- [ ] Divergence point identified
- [ ] Ready for root cause analysis

---

**See Also**: `references/analysis-strategies.md` for root cause analysis strategies, `references/fix-implementation.md` for fix implementation.
