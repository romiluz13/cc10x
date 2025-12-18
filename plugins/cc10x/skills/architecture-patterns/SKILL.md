---
name: architecture-patterns
description: This skill should be used when the user asks to "design architecture", "plan system design", "create API endpoints", "design data models", "plan integrations", or mentions system architecture, containers, components, or data flow.
---

# Architecture Patterns

Design architecture to support functionality, not generic patterns.

## Process

### 1. Understand Functionality First

Before designing architecture, understand what needs to be built:

- What problem does this solve?
- What are the user flows?
- What are the system flows?
- What are the integration requirements?

### 2. Map Existing Architecture

Understand current architecture before designing:

```bash
# Find project structure
find src -type d -maxdepth 3

# Find patterns used
grep -r "interface\|service\|model" --include="*.ts" src/ | head -20
```

Document: System context, containers, components, data models.

### 3. Design to Support Functionality

Map functionality to architecture:

| Functionality | Architecture |
|---------------|--------------|
| User flows | UI components |
| System flows | Services |
| Integration flows | Clients/adapters |
| Data flows | Data models |

### 4. Document Decisions

For each decision, document:

- **Context**: What functionality requirement drives this?
- **Options**: What alternatives were considered?
- **Trade-offs**: Pros and cons of each
- **Decision**: Which option and why

## Architecture Views

### System Context
- External actors (users, admins, external systems)
- System responsibilities
- External dependencies

### Containers
- Web app (UI)
- API service (business logic)
- Database (data storage)
- External services (integrations)

### Components
- UI components (mapped from user flows)
- Services (mapped from system flows)
- Clients/adapters (mapped from integration flows)
- Models (mapped from data flows)

## API Design

Design APIs aligned with functionality:

```
POST /api/files          # Create (from user flow: upload)
GET /api/files/:id       # Read (from user flow: view)
PUT /api/files/:id       # Update (from user flow: edit)
DELETE /api/files/:id    # Delete (from admin flow: delete)
```

For each endpoint:
- Request schema (what the flow needs)
- Response schema (what the flow returns)
- Error handling (what can go wrong in the flow)

## Integration Patterns

Design integrations aligned with functionality:

- **Retry logic**: When integrations can fail transiently
- **Circuit breakers**: When integrations can fail persistently
- **Error handling**: Map to functionality error flows

## Output Format

```markdown
# Architecture Design

## Functionality Summary
[What this architecture supports]

## System Context
[External actors, responsibilities, dependencies]

## Architecture
[Containers, components, data models]

## Decisions
[Key decisions with trade-offs]

## Implementation Roadmap
[Prioritized steps: Critical → Important → Minor]
```

## Common Mistakes

1. **Designing without understanding functionality** - Always understand flows first
2. **Generic patterns over functionality** - Design to support specific flows
3. **Missing trade-offs** - Document why each decision was made
4. **No implementation roadmap** - Provide prioritized steps
