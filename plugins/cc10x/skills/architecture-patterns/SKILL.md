---
name: architecture-patterns
description: Context-aware architecture design that understands existing architecture before designing. Use PROACTIVELY when planning features. First understands functionality requirements and existing architecture, then designs architecture to support that functionality. Maps system context, containers, components based on functionality. Provides architecture decisions with trade-offs and implementation roadmap. Focuses on architecture that enables functionality, not generic architecture patterns.
allowed-tools: Read, Grep, Glob
---

# Architecture Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware architecture design that understands existing architecture before designing. It maps functionality to architecture (user flows → components) and designs architecture to support functionality, providing architecture decisions with trade-offs.

**Unique Value**:

- Understands existing architecture before designing
- Designs architecture to support functionality (not generic patterns)
- Maps system context, containers, components based on functionality
- Provides architecture decisions with trade-offs

**When to Use**:

- When planning new features
- When designing system architecture
- When planning component boundaries
- When creating data models

---

## Functionality First Mandate

**BEFORE designing architecture, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (Architecture constraints: scale, performance, integration)
   - Dependencies: What does it need? (Services, APIs, databases)
   - Edge Cases: What can go wrong? (Architecture edge cases)
   - Verification: How do we know it works? (Architecture tests)
   - Context: Where does it fit? (Codebase structure)

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type):
   - UI Features → User Flow, Admin Flow, System Flow
   - Backend APIs → Request Flow, Response Flow, Error Flow, Data Flow
   - Integrations → Integration Flow, Data Flow, Error Flow, State Flow
   - Database → Migration Flow, Query Flow, Data Flow, State Flow

3. **THEN understand existing architecture** - Before designing

4. **THEN design architecture** - Design to support functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any architecture design, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions (especially Constraints - architecture constraints)
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this feature supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc. - context-dependent)

3. **Understand Requirements** (from Phase 1):
   - What must it do? (specific, testable)
   - What are the constraints? (scale, performance, integration)
   - What are the dependencies? (services, APIs, databases)

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely
- Must send file metadata to CRM API
- Must display upload progress to user
- Must allow admins to view, download, and delete files

**Constraints** (Architecture):

- Scale: Must handle 1000 concurrent users
- Performance: Upload must complete within 30 seconds
- Integration: Must integrate with CRM API
- Storage: Must store files securely (S3)

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

**Integration Flow**:

1. CRM API receives file metadata
2. CRM API stores file reference
3. CRM API returns file ID

---

### Phase 2: Understand Existing Architecture (MANDATORY SECOND STEP)

**Before designing architecture, understand existing architecture**:

1. **Load Project Context Understanding**:
   - Load `project-context-understanding` skill
   - Map existing architecture (system context, containers, components)
   - Identify architecture patterns used
   - Identify data models used
   - Identify integration patterns used

2. **Map System Context**:

   ```bash
   # Find system boundaries
   grep -r "system\|System\|application\|Application" --include="*.ts" | head -20

   # Find external dependencies
   grep -r "api\|API\|service\|Service\|client\|Client" --include="*.ts" | head -20
   ```

3. **Map Containers**:

   ```bash
   # Find containers (web app, API, database, etc.)
   find . -name "package.json" -o -name "Dockerfile" -o -name "docker-compose.yml"

   # Find container boundaries
   grep -r "app\|server\|database\|db\|storage" --include="*.ts" -i | head -20
   ```

4. **Map Components**:

   ```bash
   # Find component structure
   find src -type d -maxdepth 3

   # Find component patterns
   grep -r "component\|Component\|service\|Service\|model\|Model" --include="*.ts" | head -20
   ```

5. **Map Data Models**:

   ```bash
   # Find data models
   grep -r "interface\|type\|class\|model\|Model\|schema\|Schema" --include="*.ts" | head -20

   # Find database patterns
   grep -r "db\|database\|Database\|orm\|ORM\|prisma\|mongoose" --include="*.ts" | head -20
   ```

**Document Existing Architecture**:

- System Context: External actors, system responsibilities, external dependencies
- Containers: Web app, API service, database, file storage, etc.
- Components: Component structure, service structure, model structure
- Data Models: Entities, relationships, indexes
- Integration Patterns: API clients, adapters, integration patterns

**Example Output**:

```
Existing Architecture:
System Context:
- External actors: Users, Admins, CRM API
- System responsibilities: File management, CRM integration
- External dependencies: CRM API, S3 storage

Containers:
- Web App: React frontend (handles user interactions)
- API Service: Node.js backend (handles system processing)
- Database: PostgreSQL (stores metadata)
- File Storage: S3 (stores files)

Components:
- Frontend: components/, pages/, hooks/
- Backend: api/, services/, models/, utils/
- Integration: clients/, adapters/

Data Models:
- User: {id, email, name, role}
- File: {id, name, type, size, url, userId}
- Relationships: User has many Files

Integration Patterns:
- REST API clients for external services
- Adapter pattern for external APIs
```

---

### Phase 3: Architecture Design (Design to Support Functionality)

**After understanding functionality and existing architecture, design architecture**:

1. **Map Functionality to Architecture**:
   - For each functionality flow, identify architecture needs
   - Map user flows → components (UI components)
   - Map system flows → services (business logic)
   - Map integration flows → clients/adapters (external integrations)
   - Map data flows → data models (entities, relationships)

2. **Design System Context** (based on functionality):
   - External actors: Users (user flow), Admins (admin flow), External APIs (integration flow)
   - System responsibilities: Map to functionality flows
   - External dependencies: Map to integration flows

3. **Design Containers** (based on functionality):
   - Web App: Handles user/admin flows
   - API Service: Handles system flows
   - Database: Handles data storage
   - File Storage: Handles file storage
   - External Services: Handles integration flows

4. **Design Components** (based on functionality):
   - UI Components: Map to user/admin flows
   - Services: Map to system flows
   - Clients/Adapters: Map to integration flows
   - Models: Map to data flows

5. **Design Data Models** (based on functionality):
   - Entities: Map to functionality requirements
   - Relationships: Map to functionality flows
   - Indexes: Map to functionality queries

**Provide Architecture Decisions with Trade-offs**:

For each architecture decision, provide:

- **Decision**: Clear description of architecture decision
- **Context**: Functionality requirement that drives this decision
- **Options**: Alternative options evaluated
- **Trade-offs**: Pros and cons of each option
- **Chosen Option**: Option that best supports functionality
- **Consequences**: How decision affects functionality

**Example**:

```markdown
## Architecture Decision: File Storage

**Decision**: Use S3 for file storage

**Context**: File upload functionality needs reliable, scalable storage for files up to 10MB, supporting 1000 concurrent users.

**Options Evaluated**:

1. **Local filesystem**: Simple, but not scalable (fails at scale constraint)
2. **S3**: Scalable, reliable, supports functionality (meets all constraints)
3. **Database BLOB**: Works, but not optimal for large files (fails performance constraint)

**Trade-offs**:

- S3: ✅ Scalable, ✅ Reliable, ✅ Supports functionality, ❌ Adds AWS dependency
- Local filesystem: ✅ Simple, ❌ Not scalable, ❌ Single point of failure
- Database BLOB: ✅ Integrated, ❌ Not optimal for large files, ❌ Performance issues

**Chosen Option**: S3 (best supports functionality - scalable, reliable)

**Consequences**:

- Positive: Supports functionality growth, reliable storage, meets scale/performance constraints
- Negative: Adds AWS dependency, requires credentials management, adds cost

**Related**: File upload functionality requirement (scale: 1000 concurrent users, performance: <30s upload)
```

---

## Architecture Pattern Library (Reference - Use AFTER Understanding Functionality and Existing Architecture)

### Architecture Views (C4-inspired)

**Use AFTER functionality is understood and existing architecture is mapped**:

**System Context** (based on functionality):

```
External Actors:
- Users (user flow: upload files, view files)
- Admins (admin flow: view files, download files, delete files)
- CRM API (integration flow: receive file metadata)

System Responsibilities:
- File upload (user flow)
- File management (admin flow)
- CRM integration (integration flow)

External Dependencies:
- CRM API (integration flow)
- S3 storage (system flow)
```

**Containers** (based on functionality):

```
- Web App: Handles user/admin flows (upload form, progress, success, admin panel)
- API Service: Handles system flows (validation, storage, CRM integration)
- File Storage (S3): Handles system flow (file storage)
- Database: Handles system flow (metadata storage)
```

**Components** (based on functionality):

```
UI Components (User/Admin Flows):
- UploadForm: User flow (file selection, progress, success)
- AdminPanel: Admin flow (file list, filter, download, delete)

Services (System Flows):
- FileService: System flow (validation, storage)
- CRMClient: Integration flow (API calls)

Models (Data Flows):
- File: Data model (metadata)
- UploadStatus: Data model (progress tracking)
```

### Component Boundaries & Contracts

**Design boundaries to support functionality** (aligned with existing architecture):

**Component Boundaries**:

- Single responsibility per component (supports functionality)
- Public interfaces stable (supports functionality evolution)
- Inputs/outputs validated at boundary (supports functionality reliability)
- Idempotency where applicable (supports functionality retries)
- Failure and timeout policies (supports functionality reliability)

**Example**:

```typescript
// Component: FileService (supports system flow)
interface FileService {
  // Supports user flow: upload file
  uploadFile(file: File, userId: string): Promise<FileMetadata>;

  // Supports admin flow: get files
  getFiles(userId?: string, filters?: FileFilters): Promise<File[]>;

  // Supports admin flow: delete file
  deleteFile(fileId: string, userId: string): Promise<void>;
}

// Component: CRMClient (supports integration flow)
interface CRMClient {
  // Supports integration flow: sync file to CRM
  syncFile(fileMetadata: FileMetadata): Promise<string>; // Returns CRM file ID
}
```

### Data Modeling & Storage

**Design data models to support functionality** (aligned with existing data models):

**Entities** (based on functionality):

```typescript
// Entity: File (supports user/admin flows)
interface File {
  id: string;
  name: string;
  type: string;
  size: number;
  storageUrl: string; // S3 URL
  crmFileId?: string; // CRM file ID (integration flow)
  userId: string; // User flow: file owner
  uploadedAt: Date; // Admin flow: filter by date
}

// Entity: UploadStatus (supports user flow: progress tracking)
interface UploadStatus {
  fileId: string;
  progress: number; // 0-100
  status: "pending" | "uploading" | "syncing" | "completed" | "failed";
  error?: string;
}
```

**Relationships** (based on functionality):

- File belongs to User (user flow: user owns files)
- File has UploadStatus (user flow: progress tracking)
- File linked to CRM (integration flow: CRM sync)

**Indexes** (based on functionality queries):

- userId index (admin flow: filter by user)
- uploadedAt index (admin flow: filter by date)
- type index (admin flow: filter by type)

### Data Flow & Integration

**Design flows to support functionality** (aligned with existing integration patterns):

**Critical Flows** (based on functionality):

```
User Upload Flow:
UploadForm → FileService → FileStorage (S3) → CRMClient → CRM API → Database

Admin View Flow:
AdminPanel → FileService → Database

System Integration Flow:
FileService → CRMClient → CRM API
```

**Sync vs Async** (based on functionality):

- Upload: Sync (user needs immediate feedback)
- CRM integration: Async (can happen in background)
- File processing: Async (can happen in background)

**Reliability** (based on functionality):

- Retry CRM API calls (integration flow reliability)
- Timeout handling (system flow reliability)
- Error handling (all flows reliability)

---

## Cross-Cutting Concerns

**Design cross-cutting concerns to support functionality**:

### Security

- [ ] AuthN/AuthZ model (who can do what)
- [ ] Input validation and output encoding
- [ ] Secrets management and rotation
- [ ] Data-at-rest and in-transit encryption

### Performance & Scalability

- [ ] Bottlenecks identified; capacity assumptions listed
- [ ] Caching strategy (what/where/invalidation)
- [ ] Fan-out limits and bulkheads
- [ ] Backpressure and queue sizing

### Reliability & Resilience

- [ ] SLOs/SLA targets and error budgets
- [ ] Timeouts, retries, circuit breakers
- [ ] Graceful degradation and fallbacks
- [ ] Rollback/rollforward procedures

### Observability & Operations

- [ ] Structured logs with correlation IDs
- [ ] Metrics with RED/USE coverage
- [ ] Tracing across services
- [ ] Health checks and readiness probes

---

## Non-Functional Requirements (NFRs) Checklist

- [ ] Scalability targets (RPS, concurrency)
- [ ] Latency budgets (p50/p95/p99)
- [ ] Availability target (e.g., 99.9%)
- [ ] Cost budget/constraints
- [ ] Compliance/regulatory constraints

---

## Architecture Decision Record (ADR) Template

**Use AFTER functionality is understood**:

```markdown
Title: [Architecture Decision for Functionality]
Status: [Proposed/Accepted/Deprecated]
Context: [Functionality requirement that drives this decision]
Options: [A, B, C - evaluated for functionality support]
Decision: [Chosen option - best supports functionality]
Trade-offs: [Pros and cons of chosen option]
Consequences: [How decision affects functionality]
Related: [Links to functionality requirements]
```

### Risk Entry Template

```markdown
Risk: [Description]
Category: [Security/Performance/Operational/Technical]
Impact/Probability: [H/M/L]
Owner: [Name]
Mitigation: [Plan]
Fallback: [Plan]
Status: [Open/Tracking/Mitigated]
```

---

## Integration with planning-architecture-risk

- This skill is model-invoked by planning-architecture-risk.
- Use Stage 2 checklists to structure Subagent Phase 2/3 analysis.
- Produce outputs aligned with Planning Phase 5 sections (Architecture, Risk, ADRs).

---

## Verification Before Completion (Gate)

Before marking planning complete, verify:

- Views complete and consistent (context/container/component/deployment)
- Interfaces stable and versioned where needed
- Critical flows have timeouts/retries/CB documented
- Data model queries have indexes planned
- SLOs/error budgets set and testable
- Risks logged with owners and mitigations

---

## Ready Signals

- Requirements trace to architecture elements
- Clear contracts unblock downstream API/component design
- Risks are visible with mitigation paths
- NFRs are measurable and budgeted

---

## Priority Classification

**Critical (Must Have - Core Functionality)**:

- Architecture supports core functionality (user flow, system flow)
- Blocks functionality if missing
- Required for functionality to work
- Examples:
  - Components/services for user interactions
  - Components/services for system processing
  - Data models for functionality

**Important (Should Have - Supporting Functionality)**:

- Architecture supports functionality growth
- Architecture supports functionality changes
- Architecture supports functionality reliability
- Examples:
  - Scalable architecture (supports functionality growth)
  - Maintainable architecture (supports functionality changes)
  - Observable architecture (supports functionality debugging)

**Minor (Can Defer - Pattern Compliance)**:

- Perfect architecture patterns (if functionality is supported)
- Ideal component boundaries (if functionality is supported)
- Perfect data modeling (if functionality is supported)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Architecture Design Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Existing Architecture Summary

[Brief summary of existing architecture from Phase 2]

## Architecture Design

### System Context

[External actors, system responsibilities, external dependencies - based on functionality]

### Containers

[Web app, API service, database, etc. - based on functionality]

### Components

[UI components, services, clients, models - mapped from functionality flows]

### Data Models

[Entities, relationships, indexes - based on functionality]

### Data Flow & Integration

[Critical flows, sync/async decisions, reliability - based on functionality]

## Architecture Decisions

### Decision 1: [Title]

- **Context**: [Functionality requirement]
- **Options**: [A, B, C]
- **Trade-offs**: [Pros and cons]
- **Decision**: [Chosen option]
- **Consequences**: [How it affects functionality]

## Implementation Roadmap

[Prioritized list of implementation steps - Critical first, then Important, then Minor]
```

---

## Usage Guidelines

### For Planning Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis)
2. **Then**: Complete Phase 2 (Understand Existing Architecture)
3. **Then**: Complete Phase 3 (Architecture Design - Design to Support Functionality)
4. **Focus**: Architecture that enables functionality, not generic patterns

### Key Principles

1. **Functionality First**: Always understand functionality before designing architecture
2. **Context-Aware**: Understand existing architecture before designing
3. **Map Flows to Components**: Map functionality flows to architecture components
4. **Document Trade-offs**: Provide architecture decisions with trade-offs
5. **Prioritize by Impact**: Critical (core functionality) > Important (supporting functionality) > Minor (pattern compliance)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to architecture design
2. **Ignoring Existing Architecture**: Don't design without understanding existing architecture
3. **Generic Architecture Patterns**: Don't apply generic patterns - design to support functionality
4. **Missing Trade-offs**: Don't just make decisions - document trade-offs
5. **No Implementation Roadmap**: Don't just design - provide implementation roadmap
6. **Wrong Priority**: Don't prioritize pattern compliance over functionality support

---

_This skill enables context-aware architecture design that understands existing architecture and designs to support functionality, mapping flows to components and providing architecture decisions with trade-offs._
