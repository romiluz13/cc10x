---
name: architecture-patterns
description: System architecture guidance for planning: high-level views, component boundaries, data models, data flows, and cross-cutting concerns (security, performance, reliability, observability). Use during planning-architecture-risk and architecture decisions to create scalable, maintainable, and operable systems with clear trade-offs and evidence-ready outputs.
---

# Architecture Patterns

Robust, decision-driven architecture guidance for planning.

## Progressive Loading Stages

### Stage 1: Metadata (this file's frontmatter)
- Trigger keywords: architecture, system design, components, data model, data flow, scalability, NFRs, cross-cutting

---

### Stage 2: Quick Reference (Checklists)

## A. Architecture Views (C4-inspired)
```
System Context
- [ ] External actors identified (users, services, infra)
- [ ] System responsibilities defined
- [ ] External dependencies listed

Containers (services/apps/data stores)
- [ ] Containers identified with responsibilities
- [ ] Technology choices justified
- [ ] Sync/async boundaries noted
- [ ] Data stores mapped to containers

Components (per container)
- [ ] Components grouped by responsibility
- [ ] Interfaces/contracts defined
- [ ] Inbound/outbound dependencies mapped
- [ ] Reuse and composition opportunities

Deployment View
- [ ] Environments (dev/stage/prod) mapped
- [ ] Scaling model (H/V) described
- [ ] Statefulness + session strategy
- [ ] Network/security zones
```

## B. Component Boundaries & Contracts
```
- [ ] Single responsibility per component
- [ ] Public interfaces stable; internal details private
- [ ] Inputs/outputs validated at the boundary
- [ ] Idempotency where applicable
- [ ] Backward-compatible changes planned
- [ ] Failure and timeout policies documented
```

## C. Data Modeling & Storage
```
- [ ] Entities and relationships defined
- [ ] Read/write patterns (OLTP/OLAP) clear
- [ ] Indexing and query access paths planned
- [ ] Migrations strategy (online/blue-green)
- [ ] Data lifecycle (retention/archival)
- [ ] PII/security classification & controls
```

## D. Data Flow & Integration
```
- [ ] Critical flows diagrammed (request  services  data)
- [ ] Sync vs async rationale (latency, coupling)
- [ ] Contracts and versioning strategy
- [ ] Reliability patterns (retry, backoff, CB)
- [ ] Observability (trace IDs, logs, metrics)
- [ ] Dead-letter and replay strategies
```

## E. Cross-Cutting Concerns
```
Security
- [ ] AuthN/AuthZ model (who can do what)
- [ ] Input validation and output encoding
- [ ] Secrets management and rotation
- [ ] Data-at-rest and in-transit encryption

Performance & Scalability
- [ ] Bottlenecks identified; capacity assumptions listed
- [ ] Caching strategy (what/where/invalidation)
- [ ] Fan-out limits and bulkheads
- [ ] Backpressure and queue sizing

Reliability & Resilience
- [ ] SLOs/SLA targets and error budgets
- [ ] Timeouts, retries, circuit breakers
- [ ] Graceful degradation and fallbacks
- [ ] Rollback/rollforward procedures

Observability & Operations
- [ ] Structured logs with correlation IDs
- [ ] Metrics with RED/USE coverage
- [ ] Tracing across services
- [ ] Health checks and readiness probes
```

## F. Non-Functional Requirements (NFRs)
```
- [ ] Scalability targets (RPS, concurrency)
- [ ] Latency budgets (p50/p95/p99)
- [ ] Availability target (e.g., 99.9%)
- [ ] Cost budget/constraints
- [ ] Compliance/regulatory constraints
```

---

### Stage 3: Procedures & Outputs

## Procedure: Produce an Architecture Package
```
Inputs
- Requirements document & user stories
- Constraints (tech, compliance, timeline)
- Existing systems/dependencies

Steps
1) Context & Goals
   - Define goals, constraints, and success metrics
   - Clarify scope boundaries
2) Views & Boundaries
   - Create context/container/component/deployment views
   - Define public interfaces and contracts
3) Data Model & Flows
   - Define entities, relationships, and indexing
   - Diagram critical data flows & integration points
4) Cross-Cutting
   - Fill security, performance, reliability, observability checklists
   - Document SLOs and error budgets
5) Trade-offs & Risks
   - Record evaluated options and decisions (ADR format)
   - Enumerate risks and mitigations
6) Validation
   - Run verification-before-completion checks
   - Confirm requirements traceability

Outputs
- Architecture overview (context  deployment views)
- Component contracts (interfaces, versioning)
- Data model spec (ERD + indexing notes)
- Critical flow diagrams (+ reliability mechanisms)
- ADRs (decisions with pros/cons and rationale)
- Risk register with mitigations
- NFRs with measurable thresholds
```

## Templates (inline)

### Architecture Decision Record (ADR)
```
Title: [Decision]
Status: [Proposed/Accepted/Deprecated]
Context: [Background and forces]
Options: [A, B, C]
Decision: [Chosen option]
Consequences: [Positive/negative]
Related: [Links to PRDs/Issues/Docs]
```

### Risk Entry
```
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

## Verification Before Completion (Gate)

Before marking planning complete, verify:
- Views complete and consistent (context/container/component/deployment)
- Interfaces stable and versioned where needed
- Critical flows have timeouts/retries/CB documented
- Data model queries have indexes planned
- SLOs/error budgets set and testable
- Risks logged with owners and mitigations

## Ready Signals
- Requirements trace to architecture elements
- Clear contracts unblock downstream API/component design
- Risks are visible with mitigation paths
- NFRs are measurable and budgeted

