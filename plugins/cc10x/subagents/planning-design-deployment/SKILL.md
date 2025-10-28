---
name: planning-design-deployment
description: Parallel subagent for PLANNING workflow. Designs API, components, and deployment strategy. Loads api-design-patterns, component-design-patterns, and deployment-patterns skills. Runs in parallel with planning-architecture-risk for 1.5x faster planning.
license: MIT
---

# Planning Design & Deployment Subagent

**Parallel planning of API design, component design, and deployment strategy.**

## When Used

Dispatched by PLANNING workflow when planning features for:
- API design
- Component design
- State management
- Implementation phases
- File manifest
- Testing strategy
- Deployment strategy

## Workflow

**Pattern**: Parallel execution (runs simultaneously with other planning subagent)  
**Skills Loaded**: api-design-patterns, component-design-patterns, deployment-patterns  
**Time**: ~4-5 minutes (parallel with other subagent)  

---

## Phase 1: Load Skills

**Load in independent context:**

1. **api-design-patterns**
   - RESTful endpoint design
   - Request/response formats
   - Authentication/authorization
   - API versioning

2. **component-design-patterns**
   - Component hierarchy
   - Props design
   - State management
   - Composition patterns

3. **deployment-patterns**
   - Implementation phases
   - File manifest
   - Testing strategy
   - Deployment strategy

---

## Phase 2: Design API

**Design the API specification:**

### RESTful Endpoints
- [ ] Resource design
- [ ] HTTP verbs (GET, POST, PUT, DELETE)
- [ ] Status codes
- [ ] URL structure
- [ ] Query parameters

### Request/Response Formats
- [ ] JSON schema
- [ ] Validation rules
- [ ] Error responses
- [ ] Success responses
- [ ] Pagination

### Authentication & Authorization
- [ ] Auth strategy (JWT, OAuth, etc.)
- [ ] Permission model
- [ ] Role-based access control
- [ ] Token management
- [ ] Security considerations

### API Versioning
- [ ] Versioning strategy
- [ ] Deprecation plan
- [ ] Backward compatibility
- [ ] Migration path
- [ ] Documentation

---

## Phase 3: Design Components

**Design the component architecture:**

### Component Hierarchy
- [ ] Component tree
- [ ] Component responsibilities
- [ ] Component interfaces
- [ ] Component dependencies
- [ ] Reusability

### Props Design
- [ ] Props interface
- [ ] Default values
- [ ] Validation
- [ ] Type definitions
- [ ] Documentation

### State Management
- [ ] State structure
- [ ] State updates
- [ ] Side effects
- [ ] Data flow
- [ ] Performance optimization

### Composition Patterns
- [ ] Reusable components
- [ ] Composition strategies
- [ ] Code sharing
- [ ] Higher-order components
- [ ] Render props

---

## Phase 4: Plan Deployment

**Plan implementation and deployment:**

### Implementation Phases
- [ ] Phase breakdown
- [ ] Incremental delivery
- [ ] Dependencies
- [ ] Milestones
- [ ] Timeline

### File Manifest
- [ ] Files to create
- [ ] Files to modify
- [ ] Estimated LOC
- [ ] Directory structure
- [ ] File organization

### Testing Strategy
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests
- [ ] Test coverage goals
- [ ] Test data

### Deployment Strategy
- [ ] Deployment approach
- [ ] Rollback plan
- [ ] Monitoring plan
- [ ] Health checks
- [ ] Incident response

---

## Phase 5: Compile Design & Deployment Plan

**Organize design and deployment findings:**

### API Design Plan
- RESTful endpoints
- Request/response formats
- Authentication/authorization
- API versioning

### Component Design Plan
- Component hierarchy
- Props interfaces
- State management
- Composition patterns

### Deployment Plan
- Implementation phases
- File manifest
- Testing strategy
- Deployment strategy

---

## Phase 6: Return Results

**Provide design and deployment planning:**

```markdown
## API Design

### Endpoints
- [Endpoint 1]: [Description]
  - Method: [GET/POST/PUT/DELETE]
  - Path: [/path]
  - Auth: [Required/Optional]

### Request/Response
- [Request format]: [Description]
- [Response format]: [Description]
- [Error handling]: [Description]

### Authentication
- [Strategy]: [Description]
- [Permissions]: [Description]

## Component Design

### Component Hierarchy
- [Component 1]: [Description]
  - Props: [List]
  - State: [List]
  - Children: [List]

### State Management
- [State structure]: [Description]
- [State updates]: [Description]
- [Side effects]: [Description]

## Deployment Plan

### Implementation Phases
- Phase 1: [Description]
  - Duration: [Time]
  - Deliverables: [List]

### File Manifest
- [File 1]: [Description]
- [File 2]: [Description]
- [Total LOC]: [Estimate]

### Testing Strategy
- Unit tests: [Coverage]
- Integration tests: [Coverage]
- E2E tests: [Coverage]

### Deployment Strategy
- [Approach]: [Description]
- [Rollback]: [Strategy]
- [Monitoring]: [Plan]
```

---

## Integration

**Runs in parallel with:**
- planning-architecture-risk

**Merged by**: planning-workflow

**Result**: 1.5x faster planning (4-5 min vs 7 min)

