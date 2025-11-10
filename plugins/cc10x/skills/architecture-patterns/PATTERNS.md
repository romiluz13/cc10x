# Architecture Patterns - Pattern Library

Reference architecture patterns. Use AFTER understanding functionality and existing architecture (see SKILL.md Phases 1-2).

## Architecture Pattern Library

### Architecture Views (C4-inspired)

**System Context** (Level 1):

- External actors → System → External services
- Focus: What functionality does system provide? Who uses it?

**Containers** (Level 2):

- Services, databases, applications
- Focus: What containers support functionality? How do they interact?

**Components** (Level 3):

- Within containers: modules, classes, functions
- Focus: What components implement functionality? What are their responsibilities?

**Code** (Level 4):

- Implementation details
- Focus: How is functionality implemented? (Usually not needed for architecture design)

### Component Boundaries & Contracts

**Component Boundaries**:

- **Single Responsibility**: Each component has ONE reason to change (functionality-related)
- **Cohesion**: Components grouped by functionality (not by technology)
- **Coupling**: Components communicate through well-defined interfaces

**Contracts**:

- **Inputs**: What data does component need? (from functionality flows)
- **Outputs**: What data does component produce? (for functionality flows)
- **Errors**: What errors can component return? (from functionality error flows)

### Data Modeling & Storage

**Data Models** (aligned with functionality):

- **Entities**: Core data structures (User, File, Order - from functionality)
- **Relationships**: How entities relate (User has Files, Order has Items)
- **Constraints**: Data rules (email unique, file size limit - from functionality requirements)

**Storage Decisions**:

- **SQL**: Structured data, relationships, transactions (user accounts, orders)
- **NoSQL**: Flexible schema, high scale (file metadata, logs)
- **Cache**: Fast access, temporary data (session data, API responses)

### Data Flow & Integration

**Data Flow** (from functionality flows):

- **Request Flow**: User → API → Database → Response
- **Integration Flow**: System → External API → Response
- **Error Flow**: Error → Logging → Monitoring → Alerting

**Integration Patterns**:

- **Synchronous**: Real-time (user actions, immediate feedback)
- **Asynchronous**: Background (file processing, notifications)
- **Event-Driven**: Decoupled (user events, system events)

## Cross-Cutting Concerns

### Security

- Authentication: Who can access functionality?
- Authorization: What can users do with functionality?
- Data Protection: How is sensitive data protected?

### Performance & Scalability

- **Caching**: Cache frequently accessed functionality data
- **Load Balancing**: Distribute functionality load across instances
- **Database Optimization**: Optimize queries for functionality flows

### Reliability & Resilience

- **Error Handling**: Handle errors gracefully (from functionality error flows)
- **Retries**: Retry failed operations (from functionality flows)
- **Circuit Breakers**: Prevent cascading failures (from functionality integration flows)

### Observability & Operations

- **Logging**: Log functionality events (user actions, system events)
- **Monitoring**: Monitor functionality metrics (success rate, latency)
- **Alerting**: Alert on functionality issues (errors, performance degradation)

## Non-Functional Requirements (NFRs) Checklist

**Performance**:

- [ ] Response time < X ms (from functionality requirements)
- [ ] Throughput > X requests/sec (from functionality scale requirements)
- [ ] Latency < X ms (from functionality performance requirements)

**Scalability**:

- [ ] Handles X concurrent users (from functionality scale requirements)
- [ ] Scales horizontally (from functionality scale requirements)
- [ ] Database scales (from functionality data requirements)

**Reliability**:

- [ ] Uptime > 99.9% (from functionality availability requirements)
- [ ] Error rate < 0.1% (from functionality quality requirements)
- [ ] Recovery time < X minutes (from functionality recovery requirements)

**Security**:

- [ ] Authentication required (from functionality security requirements)
- [ ] Authorization checks (from functionality access requirements)
- [ ] Data encrypted (from functionality data protection requirements)

## Architecture Decision Record (ADR) Template

```markdown
## Architecture Decision: [Decision Name]

**Context**: [What functionality requires this decision?]

**Decision**: [What architecture decision was made?]

**Rationale**: [Why this decision supports functionality?]

**Trade-offs**:

- **Pros**: [How this supports functionality]
- **Cons**: [What limitations this has for functionality]

**Alternatives Considered**:

- **Alternative 1**: [Why not chosen - doesn't support functionality as well]
- **Alternative 2**: [Why not chosen - doesn't support functionality as well]

**Consequences**:

- **Positive**: [How this enables functionality]
- **Negative**: [What constraints this adds for functionality]
```
