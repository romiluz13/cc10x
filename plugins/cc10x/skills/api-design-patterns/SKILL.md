---
name: api-design-patterns
description: Context-aware API design that understands API requirements from flows before designing. Use PROACTIVELY when planning features that need APIs. First understands functionality requirements and maps them to API needs, then designs API endpoints to support that functionality. Provides specific API designs with examples aligned with project API conventions. Focuses on APIs that enable functionality, not generic REST patterns.
allowed-tools: Read, Grep, Glob
---

# API Design Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware API design that understands API requirements from flows before designing. It maps functionality to API endpoints and designs APIs to support functionality, providing specific API designs with examples aligned with project API conventions.

**Unique Value**:

- Understands API requirements before designing
- Designs APIs to support functionality (not generic REST)
- Provides specific API designs with examples
- Understands project's API conventions

**When to Use**:

- When planning features that need APIs
- When designing API contracts
- When reviewing API endpoints

---

## Quick Start

Design APIs by first understanding functionality and mapping to API needs, then designing endpoints aligned with project conventions.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Map to API needs**: Need POST /api/files/upload endpoint
3. **Understand API conventions**: Project uses REST, JSON responses, Bearer auth
4. **Design API**: POST /api/files/upload with request/response aligned with conventions

**Result:** API endpoints designed to support functionality using project conventions.

## Requirements

**Dependencies:**

- Functionality analysis template - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
- Project API conventions understanding - Must understand project's API patterns

**Prerequisites:**

- Phase 1: Context-Dependent Functionality Analysis completed (MANDATORY FIRST STEP)
- Functionality flows mapped to API needs (Request Flow, Response Flow, Error Flow, Data Flow)
- Project API conventions understood (REST patterns, versioning, error handling)

**Tool Access:**

- Required tools: Read, Grep, Glob
- Read tool: To analyze project API patterns
- Grep tool: To find API endpoint patterns

**When to Use:**

- When planning features that need APIs
- When designing API contracts
- When reviewing API endpoints

**Focus Areas:**

- APIs that enable functionality (not generic REST patterns)
- Endpoints aligned with functionality flows
- APIs aligned with project conventions

## Functionality First Mandate

**BEFORE designing APIs, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (API constraints: rate limits, payload size)
   - Dependencies: What does it need? (External APIs, services)
   - Edge Cases: What can go wrong? (API error cases)
   - Verification: How do we know it works? (API tests)
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type - Backend APIs):
   - Request Flow: Step-by-step how requests are received and processed
   - Response Flow: Step-by-step how responses are generated
   - Error Flow: Step-by-step how errors are handled
   - Data Flow: Step-by-step how data moves through the system

3. **THEN understand project's API conventions** - Before designing APIs

4. **THEN design APIs** - Design endpoints to support functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any API design, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions (especially Constraints - API constraints)
   - Complete Phase 2: Context-Dependent Flow Questions (Backend APIs - Request Flow, Response Flow, Error Flow, Data Flow)

2. **Understand Functionality**:
   - What is this API supposed to do?
   - What functionality does user need?
   - What are the flows? (Request, Response, Error, Data - context-dependent)

3. **Understand API Requirements** (from flows):
   - What endpoints are needed? (from Request Flow)
   - What data formats are needed? (from Data Flow)
   - What error handling is needed? (from Error Flow)

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system via API.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely
- Must send file metadata to CRM API
- Must return file ID and status

**Request Flow**:

1. API receives POST /api/files/upload request
2. API validates authentication token
3. API validates request body (file, metadata)
4. API validates file type and size
5. API generates unique filename
6. API uploads file to storage service
7. API calls CRM API with file metadata
8. API stores file record in database
9. API returns success response with file ID

**Response Flow**:

1. API formats response data (file ID, status, URL)
2. API includes relevant headers (Content-Type, Cache-Control)
3. API sets appropriate HTTP status code (200, 201, 400, 500)
4. API serializes response to JSON
5. API sends response to client

**Error Flow**:

1. API detects error (validation, storage, CRM API failure)
2. API logs error with context
3. API determines error type (client error vs server error)
4. API formats error response (message, code, details)
5. API returns appropriate HTTP status code
6. API includes error details for debugging (if development)

---

### Phase 2: Understand Project's API Conventions (MANDATORY SECOND STEP)

**Before designing APIs, understand how this project designs APIs**:

1. **Load Project Context Understanding**:
   - Load `project-context-understanding` skill
   - Map project's API patterns (REST, GraphQL, gRPC)
   - Identify API conventions used
   - Identify API versioning patterns used
   - Identify error handling patterns used

2. **Map API Patterns**:

   ```bash
   # Find API route definitions
   grep -r "router\.\|app\.(get|post|put|delete)" --include="*.ts" | head -20

   # Find API versioning patterns
   grep -r "v1\|v2\|version" --include="*.ts" | head -20

   # Find API error handling patterns
   grep -r "error\|Error\|status.*code" --include="*.ts" | head -20
   ```

3. **Map API Conventions**:

   ```bash
   # Find API naming conventions
   grep -r "/api/" --include="*.ts" | head -20

   # Find API response patterns
   grep -r "res\.json\|res\.send\|response" --include="*.ts" | head -20

   # Find API authentication patterns
   grep -r "auth\|Auth\|authenticate\|jwt\|token" --include="*.ts" | head -20
   ```

**Document Project's API Conventions**:

- API Pattern: REST, GraphQL, gRPC, etc.
- API Versioning: URL versioning (/v1/), header versioning, etc.
- API Naming: Resource naming conventions, endpoint naming conventions
- Error Handling: Error response format, error codes, error messages
- Authentication: Auth patterns (JWT, OAuth, API keys)
- Response Format: Response structure, pagination, filtering

**Example Output**:

```
Project API Conventions:
API Pattern: RESTful APIs
API Versioning: URL versioning (/api/v1/)
API Naming:
- Resources: Plural nouns (files, users, orders)
- Endpoints: RESTful verbs (GET, POST, PUT, DELETE)
- Paths: kebab-case (/api/files/upload)

Error Handling:
- Error format: { error: { code, message, status, details } }
- Error codes: UPPER_SNAKE_CASE (FILE_TOO_LARGE)
- Status codes: Standard HTTP status codes

Authentication:
- JWT tokens in Authorization header
- Bearer token format

Response Format:
- JSON responses
- Pagination: ?page=1&limit=20
- Filtering: ?status=active&type=pdf
```

---

### Phase 3: API Design (Design to Support Functionality)

**After understanding functionality and project API conventions, design APIs**:

1. **Map Functionality to API Endpoints**:
   - For each functionality flow, identify API endpoint needs
   - Map user flows → API endpoints (user actions)
   - Map admin flows → API endpoints (admin actions)
   - Map system flows → API endpoints (system processing)
   - Map integration flows → API endpoints (external systems)

2. **Design Endpoints** (based on functionality):
   - Design endpoints aligned with project API conventions
   - Design request/response schemas aligned with functionality
   - Design error handling aligned with functionality

3. **Design Request Schemas** (based on functionality):
   - Map functionality inputs to request schemas
   - Include validation aligned with functionality requirements
   - Include authentication aligned with functionality security

4. **Design Response Schemas** (based on functionality):
   - Map functionality outputs to response schemas
   - Include data aligned with functionality needs
   - Include metadata aligned with functionality needs

5. **Design Error Handling** (based on functionality):
   - Map functionality error cases to error responses
   - Include error codes aligned with functionality
   - Include error messages aligned with functionality

**Provide Specific API Designs with Examples**:

For each API endpoint, provide:

- **Endpoint**: HTTP method and path (aligned with project conventions)
- **Purpose**: Functionality it supports
- **Request**: Request schema with examples
- **Response**: Response schema with examples
- **Errors**: Error responses with examples
- **Flow Step**: Which functionality flow step it supports

**Example**:

````markdown
## API Endpoint: POST /api/v1/files/upload

**Purpose**: Supports user flow - file upload functionality

**Functionality Flow Step**: Request Flow Step 1-9 (file upload request → validation → storage → CRM sync → response)

**Request** (aligned with project JSON format):

```json
POST /api/v1/files/upload
Authorization: Bearer {jwt_token}
Content-Type: multipart/form-data

{
  "file": <file binary>,
  "metadata": {
    "name": "document.pdf",
    "type": "application/pdf",
    "description": "Customer contract"
  }
}
```
````

**Response** (aligned with project response format):

```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "file": {
    "id": "file_123",
    "name": "document.pdf",
    "type": "application/pdf",
    "size": 5242880,
    "url": "https://storage.example.com/files/file_123",
    "crmFileId": "crm_456",
    "status": "uploaded",
    "uploadedAt": "2024-01-15T10:30:00Z"
  }
}
```

**Errors** (aligned with project error format):

```json
HTTP/1.1 413 Payload Too Large
Content-Type: application/json

{
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "File exceeds 10MB limit",
    "status": 413,
    "details": {
      "maxSize": "10MB",
      "fileSize": "15MB"
    }
  }
}
```

**Priority**: Critical (core functionality)

````

---

## API Design Pattern Library

**Reference**: See [PATTERNS.md](./PATTERNS.md) for detailed API design patterns including:
- RESTful structure
- Request/response schemas
- Error handling
- Authentication & authorization
- Versioning

---

## Priority Classification

**Critical (Must Have - Core Functionality)**:

- API endpoints support core functionality (user flow, system flow)
- Blocks functionality if missing
- Required for functionality to work
- Examples:
  - Endpoints for user actions (upload, view)
  - Endpoints for system processing (validate, store)
  - Request/response schemas for functionality

**Important (Should Have - Supporting Functionality)**:

- API supports functionality growth
- API supports functionality changes
- API supports functionality reliability
- Examples:
  - Error handling for functionality reliability
  - Authentication for functionality security
  - Rate limiting for functionality performance

**Minor (Can Defer - Pattern Compliance)**:

- Perfect REST structure (if functionality is supported)
- Ideal versioning (if functionality is supported)
- Perfect OpenAPI spec (if functionality is supported)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# API Design Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Project API Conventions Summary

[Brief summary of project API conventions from Phase 2]

## API Design

### Endpoints

[For each endpoint:]

- **Endpoint**: [HTTP method and path]
- **Purpose**: [Functionality it supports]
- **Request**: [Request schema with examples]
- **Response**: [Response schema with examples]
- **Errors**: [Error responses with examples]
- **Flow Step**: [Which functionality flow step it supports]
- **Priority**: [Critical, Important, or Minor]

### Request/Response Schemas

[Request and response schemas aligned with functionality]

### Error Handling

[Error handling aligned with functionality error cases]

### Authentication & Authorization

[Auth patterns aligned with functionality security]

## Recommendations

[Prioritized list of API designs - Critical first, then Important, then Minor]
```

---

## Troubleshooting

**Common Issues:**

1. **API design without understanding functionality**
   - **Symptom**: Designing APIs that don't support functionality flows
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, then design APIs
   - **Prevention**: Always understand functionality before API design

2. **Generic REST patterns instead of functionality-focused**
   - **Symptom**: APIs follow generic REST but don't support functionality
   - **Cause**: Didn't map functionality flows to API needs
   - **Fix**: Map flows to API needs, design endpoints to support flows
   - **Prevention**: Always map functionality to API needs first

3. **API designs not aligned with project conventions**
   - **Symptom**: APIs don't match project's API patterns
   - **Cause**: Didn't understand project's API conventions
   - **Fix**: Understand project conventions, align API design
   - **Prevention**: Always understand project API conventions first

**If issues persist:**

- Verify functionality analysis was completed first
- Check that functionality flows were mapped to API needs
- Ensure API designs align with project conventions
- Review REFERENCE.md for API design examples

---

## Usage Guidelines

### For Planning Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis - especially Request/Response/Error/Data Flows)
2. **Then**: Complete Phase 2 (Understand Project API Conventions)
3. **Then**: Complete Phase 3 (API Design - Design to Support Functionality)
4. **Focus**: APIs that enable functionality, not generic REST patterns

### Key Principles

1. **Functionality First**: Always understand functionality before designing APIs
2. **Context-Aware**: Understand project API conventions before designing
3. **Map Flows to Endpoints**: Map functionality flows to API endpoints
4. **Specific Designs**: Provide specific API designs with examples aligned with project conventions
5. **Prioritize by Impact**: Critical (core functionality) > Important (supporting functionality) > Minor (pattern compliance)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to API design
2. **Ignoring Project Conventions**: Don't design without understanding project API conventions
3. **Generic REST Patterns**: Don't apply generic REST patterns - design to support functionality
4. **Missing Specific Designs**: Don't just describe endpoints - provide specific schemas and examples
5. **No Flow Mapping**: Don't just list endpoints - map them to functionality flows
6. **Wrong Priority**: Don't prioritize pattern compliance over functionality support

---

_This skill enables context-aware API design that understands API requirements from flows and designs APIs to support functionality, providing specific API designs with examples aligned with project API conventions._
````
