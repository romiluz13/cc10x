---
name: architecture-patterns
description: Context-aware architecture design covering system architecture, API design, and integration patterns. Use PROACTIVELY when planning features. First understands functionality requirements and existing architecture, then designs architecture, APIs, and integrations to support that functionality. Maps system context, containers, components, API endpoints, and integration strategies based on functionality. Provides architecture decisions with trade-offs and implementation roadmap. Focuses on architecture that enables functionality, not generic patterns.
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

## Quick Start

Design architecture by first understanding functionality and existing architecture, then designing to support functionality.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Understand existing architecture**: Project uses microservices, REST APIs
3. **Design architecture**: Map flows to components, design system context
4. **Provide decisions**: Architecture decisions with trade-offs and roadmap

**Result:** Architecture designed to support functionality with clear decisions.

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

6. **Design API Endpoints** (based on functionality):
   - Map user flows → API endpoints (user actions)
   - Map admin flows → API endpoints (admin actions)
   - Map system flows → API endpoints (system processing)
   - Design request/response schemas aligned with functionality
   - Design error handling aligned with functionality error cases

7. **Design Integration Strategies** (based on functionality):
   - Map integration flows → integration clients/adapters
   - Design retry logic aligned with functionality reliability needs
   - Design circuit breakers aligned with functionality resilience needs
   - Design error handling aligned with functionality error flows

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

## Troubleshooting

**Common Issues:**

1. **Architecture design without understanding functionality**
   - **Symptom**: Architecture doesn't support functionality flows
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, then design architecture
   - **Prevention**: Always understand functionality before architecture design

2. **Generic architecture patterns instead of functionality-focused**
   - **Symptom**: Architecture follows generic patterns but doesn't support functionality
   - **Cause**: Didn't map functionality flows to architecture needs
   - **Fix**: Map flows to architecture, design to support flows
   - **Prevention**: Always map functionality to architecture needs first

3. **Architecture decisions not aligned with project patterns**
   - **Symptom**: Architecture doesn't match project's architecture patterns
   - **Cause**: Didn't understand existing architecture
   - **Fix**: Understand existing architecture, align design
   - **Prevention**: Always understand existing architecture first

**If issues persist:**

- Verify functionality analysis was completed first
- Check that functionality flows were mapped to architecture
- Ensure architecture design aligns with project patterns
- Review PATTERNS.md for detailed guidance

## Reference Materials

**For detailed architecture patterns and reference materials, see:**

- **PATTERNS.md**: Architecture Pattern Library (Architecture Views, Component Boundaries, Data Modeling, Data Flow, Cross-Cutting Concerns, NFRs Checklist, ADR Template)
- **API Design Patterns**: RESTful structure, request/response schemas, error handling, authentication & authorization, versioning (merged from api-design-patterns)
- **Integration Patterns**: Retry logic, circuit breakers, error handling, reliability patterns, resilience & consistency patterns (merged from integration-patterns)

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

### API Design

[Endpoints mapped from functionality flows, request/response schemas, error handling - based on functionality]

### Integration Strategies

[Integration clients/adapters mapped from integration flows, retry logic, circuit breakers, error handling - based on functionality]

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
