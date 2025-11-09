# Functionality Analysis Template - Context-Dependent

**Purpose**: Standard template for analyzing functionality before applying any specialized checks (security, quality, performance, UX, accessibility, architecture, etc.). Uses context-dependent approach: universal questions first, then context-specific flow questions based on code type.

**When to Use**:

- Before every code review
- Before every feature plan
- Before every build
- Before every debug session
- Before every validation

**Mandatory**: This analysis MUST be completed before applying any specialized skills or patterns.

---

## Format Requirements

**CRITICAL**: Follow the format below exactly. Incorrect formatting leads to incomplete analysis.

### CORRECT Format Examples

**Example 1: User Flow (CORRECT)**

```markdown
### User Flow

1. User clicks "Upload File" button
2. File picker opens
3. User selects file (PDF, DOCX, or image)
4. System validates file type and size
5. File uploads with progress indicator
6. System stores file securely
7. System sends metadata to CRM API
8. User sees success message
9. File appears in file list
```

**Example 2: System Flow (CORRECT)**

```markdown
### System Flow

1. Frontend receives file upload request
2. Frontend validates file client-side (type, size)
3. Frontend sends file to backend API endpoint `/api/files/upload`
4. Backend validates file server-side
5. Backend stores file in encrypted storage
6. Backend sends file metadata to CRM API
7. Backend returns success response to frontend
8. Frontend updates UI with new file
```

**Example 3: Scenario Format (CORRECT)**

```markdown
### Scenarios

**WHEN** user uploads valid PDF file (< 10MB)
**THEN** file uploads successfully
**AND** file appears in file list
**AND** metadata sent to CRM API

**WHEN** user uploads file > 10MB
**THEN** upload is rejected
**AND** error message displayed: "File too large. Maximum size: 10MB"

**WHEN** user uploads invalid file type
**THEN** upload is rejected
**AND** error message displayed: "Invalid file type. Allowed: PDF, DOCX, images"
```

### WRONG Format Examples

**Example 1: User Flow (WRONG - Too vague)**

```markdown
### User Flow

User uploads file. System processes it. User sees result.
```

❌ **Problem**: Missing step-by-step detail, no specific actions, no validation steps

**Example 2: System Flow (WRONG - Missing details)**

```markdown
### System Flow

Backend handles upload.
```

❌ **Problem**: No endpoints, no validation, no error handling, no integration details

**Example 3: Scenario Format (WRONG - Missing WHEN/THEN)**

```markdown
### Scenarios

File upload works sometimes.
```

❌ **Problem**: No conditions, no expected outcomes, no error cases

---

## Context Detection

**First, identify the code type** to determine which flow questions are relevant:

### Code Type Detection Logic

Use file patterns, imports, structure, and context to identify code type:

- **UI Features / Frontend Components**:
  - File patterns: `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `components/`, `pages/`, `views/`
  - Imports: React, Vue, Angular, UI libraries
  - Structure: Component files, UI-related directories

- **Backend APIs / Services**:
  - File patterns: `*api*.ts`, `*service*.ts`, `routes/`, `controllers/`, `handlers/`
  - Imports: Express, FastAPI, Flask, REST frameworks
  - Structure: API route files, service files, controller files

- **Utility Functions / Libraries**:
  - File patterns: `utils/`, `helpers/`, `lib/`, `*util*.ts`, `*helper*.ts`
  - Imports: Utility libraries, no framework dependencies
  - Structure: Standalone functions, utility modules

- **Integrations / External Services**:
  - File patterns: `integrations/`, `*client*.ts`, `*adapter*.ts`, `*connector*.ts`
  - Imports: HTTP clients, external SDKs, API clients
  - Structure: Integration modules, client wrappers

- **Database / Data Layer**:
  - File patterns: `models/`, `migrations/`, `schema/`, `*model*.ts`, `*migration*.ts`
  - Imports: ORMs, database clients, query builders
  - Structure: Model files, migration files, schema files

- **Configuration / Setup**:
  - File patterns: `config/`, `*.config.*`, `*.env.*`, `setup/`
  - Imports: Config libraries, environment variable loaders
  - Structure: Configuration files, setup scripts

- **CLI Tools / Scripts**:
  - File patterns: `cli/`, `scripts/`, `bin/`, `*.cli.*`
  - Imports: CLI frameworks, command parsers
  - Structure: CLI entry points, command files

- **Background Jobs / Workers**:
  - File patterns: `workers/`, `jobs/`, `tasks/`, `*worker*.ts`, `*job*.ts`
  - Imports: Job queues, task runners, schedulers
  - Structure: Worker files, job processors

---

## Phase 1: Universal Questions (ALWAYS ASK THESE FIRST)

**These questions apply to EVERY code review/plan/build/debug, regardless of code type:**

```markdown
## Functionality Analysis

### Purpose

[What problem does this solve? What is the goal? What user need does it address?]

**Example**: "Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users."

### Requirements

[What must it do? Be specific and testable. What are the must-haves?]

**Example**:

- Must accept file uploads (PDF, DOCX, images)
- Must validate file type and size (max 10MB)
- Must store files securely
- Must send file metadata to CRM API
- Must display upload progress to user
- Must handle errors gracefully

### Constraints

[What are the limits? Performance? Scale? Time? Security?]

**Example**:

- Performance: Upload must complete within 30 seconds for files up to 10MB
- Scale: Must handle 100 concurrent uploads
- Time: Must be completed in 2 weeks
- Security: Files must be encrypted at rest, access controlled
- Storage: 100GB storage limit

### Dependencies

[What does it need? Files? APIs? Services? Libraries?]

**Example**:

- Files: `api/files/upload.ts`, `services/storage.ts`, `services/crm-client.ts`
- APIs: CRM API (POST /crm/files)
- Services: S3 storage service, CRM API service
- Libraries: `aws-sdk`, `axios`, `multer`

### Edge Cases

[What can go wrong? Boundary conditions? Error scenarios?]

**Example**:

- Empty file upload
- File exceeds size limit
- Invalid file type
- Network failure during upload
- CRM API unavailable
- Storage quota exceeded
- Concurrent uploads from same user

### Verification

[How do we know it works? Tests? Acceptance criteria? Success metrics?]

**Example**:

- Unit tests: File validation logic, error handling
- Integration tests: Upload flow, CRM API integration
- E2E tests: Complete user flow from upload to CRM visibility
- Acceptance criteria:
  - User can upload valid file
  - File appears in CRM within 5 seconds
  - Invalid files are rejected with clear error
  - Upload progress is visible
- Success metrics: 99% upload success rate, <30s upload time

### Context

[Where does it fit? What files are involved? What's the codebase structure?]

**Example**:

- Location: `src/features/file-upload/`
- Related files: `components/UploadForm.tsx`, `api/files.ts`, `services/storage.ts`
- Codebase structure: React frontend, Node.js backend, PostgreSQL database
- Architecture: MVC pattern, RESTful API
```

---

## Phase 2: Context-Dependent Flow Questions

**After completing universal questions, ask flow questions based on detected code type:**

### For UI Features / Frontend Components

```markdown
### User Flow

[Step-by-step how users interact with the feature]

**Example**:

1. User navigates to "Upload File" page
2. User clicks "Upload File" button
3. User selects file from device (file picker opens)
4. User sees upload progress indicator (0% → 100%)
5. User sees success message: "File uploaded successfully"
6. User sees link to view uploaded file
7. User clicks link to view file in CRM

### Admin Flow (if applicable)

[Step-by-step how admins manage the feature]

**Example**:

1. Admin navigates to "Files" page
2. Admin sees list of uploaded files (table with filters)
3. Admin can filter by user/date/type
4. Admin clicks on file to view details
5. Admin can download file
6. Admin can delete file
7. Admin sees upload statistics (total files, storage used)

### System Flow

[Step-by-step how the system processes user actions]

**Example**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type (only PDF, DOCX, images)
3. System validates file size (max 10MB)
4. System generates unique filename
5. System stores file in secure storage (S3 bucket)
6. System sends file metadata to CRM API (POST /crm/files)
7. System receives CRM API response (file ID)
8. System stores file record in database
9. System returns success response to user
```

### For Backend APIs / Services

```markdown
### Request Flow

[Step-by-step how requests are received and processed]

**Example**:

1. API receives POST /api/files/upload request
2. API validates authentication token
3. API validates request body (file, metadata)
4. API validates file type and size
5. API generates unique filename
6. API uploads file to storage service
7. API calls CRM API with file metadata
8. API stores file record in database
9. API returns success response with file ID

### Response Flow

[Step-by-step how responses are generated]

**Example**:

1. API formats response data (file ID, status, URL)
2. API includes relevant headers (Content-Type, Cache-Control)
3. API sets appropriate HTTP status code (200, 201, 400, 500)
4. API serializes response to JSON
5. API sends response to client

### Error Flow

[Step-by-step how errors are handled]

**Example**:

1. API detects error (validation, storage, CRM API failure)
2. API logs error with context
3. API determines error type (client error vs server error)
4. API formats error response (message, code, details)
5. API returns appropriate HTTP status code
6. API includes error details for debugging (if development)

### Data Flow

[Step-by-step how data moves through the system]

**Example**:

1. File data received from client
2. File metadata extracted (name, type, size)
3. File stored in S3 bucket
4. File metadata sent to CRM API
5. File record stored in database
6. File ID returned to client
```

### For Utility Functions / Libraries

```markdown
### Input Flow

[Step-by-step how inputs are received and validated]

**Example**:

1. Function receives file object as parameter
2. Function validates file exists
3. Function validates file type
4. Function validates file size
5. Function extracts file metadata

### Processing Flow

[Step-by-step how processing happens]

**Example**:

1. Function reads file content
2. Function generates unique filename
3. Function uploads file to storage
4. Function returns file URL

### Output Flow

[Step-by-step how outputs are generated]

**Example**:

1. Function formats response data
2. Function returns file URL and metadata
3. Function throws error if processing fails

### Error Flow

[Step-by-step how errors are handled]

**Example**:

1. Function catches errors during processing
2. Function logs error with context
3. Function throws descriptive error
4. Function cleans up resources if needed
```

### For Integrations / External Services

```markdown
### Integration Flow

[Step-by-step how integration works]

**Example**:

1. System prepares file metadata for CRM API
2. System authenticates with CRM API (Bearer token)
3. System sends POST request to CRM API
4. CRM API validates request
5. CRM API stores file reference
6. CRM API returns file ID
7. System receives response and updates local record

### Data Flow

[Step-by-step how data moves between systems]

**Example**:

1. File metadata extracted from local system
2. Data transformed to CRM API format
3. Data sent to CRM API
4. CRM API response received
5. Response data stored in local system

### Error Flow

[Step-by-step how errors are handled]

**Example**:

1. CRM API request fails (network, auth, validation)
2. System detects error response
3. System logs error with context
4. System retries if transient error (with exponential backoff)
5. System returns error to caller if permanent failure

### State Flow

[Step-by-step how state changes]

**Example**:

1. File upload initiated (state: "pending")
2. File uploaded to storage (state: "uploading")
3. CRM API called (state: "syncing")
4. CRM API responds (state: "synced")
5. Error occurs (state: "failed")
```

### For Database / Data Layer

```markdown
### Migration Flow (if applicable)

[Step-by-step how migrations work]

**Example**:

1. Migration script reads schema changes
2. Migration validates current database state
3. Migration applies schema changes (CREATE TABLE, ALTER TABLE)
4. Migration migrates existing data if needed
5. Migration verifies changes applied correctly
6. Migration records migration in migrations table

### Query Flow

[Step-by-step how queries are executed]

**Example**:

1. Application constructs query (SELECT, INSERT, UPDATE, DELETE)
2. Query validated for SQL injection risks
3. Query executed against database
4. Results fetched and transformed
5. Results returned to application

### Data Flow

[Step-by-step how data moves]

**Example**:

1. Data received from application layer
2. Data validated against schema
3. Data transformed to database format
4. Data written to database
5. Data read from database
6. Data transformed to application format
7. Data returned to application layer

### State Flow

[Step-by-step how state changes]

**Example**:

1. Record created (state: "active")
2. Record updated (state: "modified")
3. Record deleted (state: "deleted")
4. Record archived (state: "archived")
```

### For Configuration / Setup

```markdown
### Configuration Flow

[Step-by-step how configuration is loaded/applied]

**Example**:

1. Application starts
2. Configuration loader reads environment variables
3. Configuration loader reads config files
4. Configuration validated against schema
5. Configuration merged (env vars override files)
6. Configuration applied to application
7. Configuration errors logged if invalid

### Validation Flow

[Step-by-step how configuration is validated]

**Example**:

1. Configuration loader receives config values
2. Each value validated against schema
3. Required values checked for presence
4. Value types validated (string, number, boolean)
5. Value ranges validated (min/max)
6. Invalid values rejected with error messages

### Error Flow

[Step-by-step how errors are handled]

**Example**:

1. Configuration loader detects invalid value
2. Error logged with context (key, value, reason)
3. Default value used if available
4. Application fails to start if critical value missing
5. Error message displayed to user/admin
```

### For CLI Tools / Scripts

```markdown
### Command Flow

[Step-by-step how commands are parsed and executed]

**Example**:

1. CLI receives command-line arguments
2. CLI parses arguments (command, options, flags)
3. CLI validates arguments
4. CLI routes to appropriate command handler
5. Command handler executes logic
6. Command handler returns exit code

### Processing Flow

[Step-by-step how processing happens]

**Example**:

1. Command handler reads input (files, stdin, API)
2. Command handler processes data
3. Command handler transforms data
4. Command handler writes output (files, stdout, API)

### Output Flow

[Step-by-step how outputs are generated]

**Example**:

1. Command handler formats results
2. Command handler writes to stdout/stderr
3. Command handler writes to files if specified
4. Command handler returns exit code (0 = success, non-zero = error)

### Error Flow

[Step-by-step how errors are handled]

**Example**:

1. Command handler detects error
2. Error logged to stderr
3. Error message displayed to user
4. Command handler returns non-zero exit code
5. Command handler cleans up resources
```

### For Background Jobs / Workers

```markdown
### Job Flow

[Step-by-step how jobs are triggered and processed]

**Example**:

1. Job scheduled (cron, queue, manual trigger)
2. Worker picks up job from queue
3. Worker validates job payload
4. Worker processes job (file upload, data sync, email send)
5. Worker updates job status (pending → processing → completed)
6. Worker stores job results
7. Worker handles job failure if error occurs

### Processing Flow

[Step-by-step how processing happens]

**Example**:

1. Worker reads job payload
2. Worker fetches required data
3. Worker processes data
4. Worker stores results
5. Worker sends notifications if needed

### State Flow

[Step-by-step how state changes]

**Example**:

1. Job created (state: "pending")
2. Worker picks up job (state: "processing")
3. Job completes successfully (state: "completed")
4. Job fails (state: "failed")
5. Job retried (state: "retrying")

### Error Flow

[Step-by-step how errors are handled]

**Example**:

1. Worker detects error during processing
2. Worker logs error with context
3. Worker updates job status to "failed"
4. Worker retries job if retryable error
5. Worker sends failure notification if max retries exceeded
```

---

## Complete Example: File Upload to CRM (UI Feature)

### Phase 1: Universal Questions

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users. Admins should be able to view and manage uploaded files.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely in S3
- Must send file metadata to CRM API
- Must display upload progress to user
- Must handle errors gracefully
- Must allow admins to view, download, and delete files

**Constraints**:

- Performance: Upload must complete within 30 seconds for files up to 10MB
- Scale: Must handle 100 concurrent uploads
- Time: Must be completed in 2 weeks
- Security: Files must be encrypted at rest, access controlled
- Storage: 100GB storage limit

**Dependencies**:

- Files: `components/UploadForm.tsx`, `api/files.ts`, `services/storage.ts`, `services/crm-client.ts`
- APIs: CRM API (POST /crm/files)
- Services: S3 storage service, CRM API service
- Libraries: `aws-sdk`, `axios`, `react-dropzone`

**Edge Cases**:

- Empty file upload
- File exceeds size limit (10MB)
- Invalid file type
- Network failure during upload
- CRM API unavailable
- Storage quota exceeded
- Concurrent uploads from same user
- Very large files (approaching 10MB limit)

**Verification**:

- Unit tests: File validation logic, error handling
- Integration tests: Upload flow, CRM API integration
- E2E tests: Complete user flow from upload to CRM visibility
- Acceptance criteria:
  - User can upload valid file
  - File appears in CRM within 5 seconds
  - Invalid files are rejected with clear error
  - Upload progress is visible
- Success metrics: 99% upload success rate, <30s upload time

**Context**:

- Location: `src/features/file-upload/`
- Related files: `components/UploadForm.tsx`, `api/files.ts`, `services/storage.ts`
- Codebase structure: React frontend, Node.js backend, PostgreSQL database
- Architecture: MVC pattern, RESTful API

### Phase 2: Context-Dependent Flow Questions (UI Feature)

**User Flow**:

1. User navigates to "Upload File" page
2. User clicks "Upload File" button
3. User selects file from device (file picker opens)
4. User sees upload progress indicator (0% → 100%)
5. User sees success message: "File uploaded successfully"
6. User sees link to view uploaded file
7. User clicks link to view file in CRM

**Admin Flow**:

1. Admin navigates to "Files" page
2. Admin sees list of uploaded files (table with filters)
3. Admin can filter by user/date/type
4. Admin clicks on file to view details
5. Admin can download file
6. Admin can delete file
7. Admin sees upload statistics (total files, storage used)

**System Flow**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type (only PDF, DOCX, images)
3. System validates file size (max 10MB)
4. System generates unique filename
5. System stores file in secure storage (S3 bucket)
6. System sends file metadata to CRM API (POST /crm/files)
   - File name, size, type, storage URL
   - User ID, upload timestamp
7. System receives CRM API response (file ID)
8. System stores file record in database
9. System returns success response to user
10. System handles errors:
    - Invalid file type → Error: "File type not supported"
    - File too large → Error: "File exceeds 10MB limit"
    - CRM API error → Error: "Failed to upload to CRM, please try again"

---

## Usage Guidelines

### For Review Workflow

1. **First**: Complete Phase 1 (Universal Questions)
2. **Then**: Detect code type and complete Phase 2 (Context-Dependent Flow Questions)
3. **Then**: Verify functionality works (test if possible)
4. **Then**: Check security/quality/performance issues affecting functionality
5. **Focus**: Issues that block or degrade functionality

### For Plan Workflow

1. **First**: Complete Phase 1 (Universal Questions)
2. **Then**: Detect feature type and complete Phase 2 (Context-Dependent Flow Questions)
3. **Then**: Research external APIs/constraints if needed
4. **Then**: Design architecture to support functionality
5. **Then**: Identify risks specific to functionality

### For Build Workflow

1. **First**: Complete Phase 1 (Universal Questions)
2. **Then**: Detect component type and complete Phase 2 (Context-Dependent Flow Questions)
3. **Then**: Build functionality (make it work)
4. **Then**: Test functionality (verify it works)
5. **Then**: Apply patterns (only if needed)

### For Debug Workflow

1. **First**: Complete Phase 1 (Universal Questions) - understand expected functionality
2. **Then**: Detect code type and complete Phase 2 (Context-Dependent Flow Questions) - understand expected flows
3. **Then**: Map observed behavior to expected behavior
4. **Then**: Debug functionality issues
5. **Focus**: Bugs that affect functionality

### For Validate Workflow

1. **First**: Complete Phase 1 (Universal Questions)
2. **Then**: Detect code type and complete Phase 2 (Context-Dependent Flow Questions)
3. **Then**: Map functionality to validation needs
4. **Then**: Validate functionality works as expected
5. **Focus**: Functionality verification

---

## Key Principles

1. **Functionality First**: Always understand what code should do before checking other concerns
2. **Universal Questions First**: Always start with Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Ask flow questions based on code type, not generic flows
4. **Specificity**: Be specific in requirements, flows, and verification criteria
5. **Research When Needed**: Fetch external API docs, constraints, limitations
6. **Verify Functionality**: Test if possible, verify with evidence
7. **Prioritize by Impact**: Focus on issues affecting functionality, defer others

---

## Common Mistakes to Avoid

1. **Skipping Universal Questions**: Don't jump straight to flow questions
2. **Forcing Generic Flows**: Don't force "User Flow" on backend APIs or utilities
3. **Missing Context Detection**: Always detect code type before asking flow questions
4. **Generic Requirements**: Don't write "must work" - be specific: "must accept PDF files up to 10MB"
5. **Missing Edge Cases**: Always consider boundary conditions and error scenarios
6. **No Verification**: Don't assume functionality works - verify it
7. **Ignoring Constraints**: Always document performance, scale, time, security constraints

---

_This template ensures context-dependent functionality-first approach across all CC10X workflows._
