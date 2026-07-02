---
name: architecture
description: |
  Greenfield architecture design: map functionality flows, draw components, design APIs,
  classify dependencies, plan observability. For multi-component, API, schema, auth, or
  integration-heavy work. For retrofitting existing code, use codebase-hygiene instead.
allowed-tools: Read Grep Glob LSP Bash
user-invocable: false
---

# Architecture

Design systems from scratch: map flows, then draw components. For retrofitting existing code, use `codebase-hygiene` instead.

## Intake Routing

| Request type | Use |
| ------------- | ----- |
| New system/major feature (greenfield) | This skill |
| Existing code with shallow modules | `codebase-hygiene` |
| Multi-component integration | This skill |
| Single-component refactor | `planning` + `building` |

## Functionality-First Design Process

### Phase 1: Map Functionality Flows

Map every user flow end-to-end before designing any component:

```
Flow: [name]
1. [step] → [what the system does] → [what the user sees]
2. [step] → [what the system does] → [what the user sees]
Error paths:
- [error] → [system response] → [user sees]
```

Every flow must have its error paths mapped. Unmapped error paths become unmapped components.

### Phase 2: Map to Architecture

Translate flows into components:

- Each flow step maps to one or more components
- Each error path maps to a component's error handling
- Data crossings between components become interfaces

### Phase 3: Design Components

For each component:

- **Interface:** what it receives and returns (the contract)
- **Responsibility:** what it does (one sentence)
- **Dependencies:** what it needs (other components, external services)
- **State:** what it remembers (if anything)
- **Error handling:** what can go wrong and what it does about it

## Architecture Views

### System Context (C4 Level 1)

Box diagram: your system + external systems it talks to. One paragraph per external system: what it provides, what you depend on.

### Container View (C4 Level 2)

Internal boxes: web app, API, database, queue, worker. Arrows show data flow. One paragraph per container: technology choice, responsibility.

### Component View (C4 Level 3)

Inside each container: the modules/classes. Arrows show call relationships. This is what the builder will implement.

## LSP-Powered Architecture Analysis

Use LSP to understand existing architecture before designing new:

- **Go to Definition** on key functions to trace the call graph
- **Find References** to understand blast radius of existing interfaces
- **Go to Type Definition** to understand data models
- **Incoming/Outgoing Calls** to map the dependency graph

## API Design (Functionality-Aligned)

Design APIs from the flow, not from the data model:

1. **What does the user need to do?** (action, not resource)
2. **What's the minimal interface that enables it?** (fewest endpoints/parameters)
3. **What's the error contract?** (every error case from the flow mapping)
4. **What's the type contract?** (input/output types, not just shapes)

```typescript
// Good: functionality-aligned
POST /orders/{id}/cancel  →  { status, cancelledAt }

// Bad: data-model-aligned
PUT /orders/{id}  →  { ..., status: "cancelled", ... }
```

## Integration Patterns

For each integration:

| Field | Value |
| ------- | ------- |
| **System** | [name] |
| **Protocol** | [HTTP/gRPC/CLI/message queue] |
| **Direction** | [we call them / they call us / both] |
| **Contract** | [request/response schema or event schema] |
| **Failure mode** | [what happens when it's down] |
| **Retry policy** | [retries, backoff, circuit breaker] |

### Dependency Classification

| Class | Meaning | Example |
| ------- | --------- | --------- |
| **Owned** | We control the code and deploy it | Internal service |
| **Wrapped** | We depend on it but wrap it in our interface | Third-party SDK behind adapter |
| **Consumed** | We depend on it directly, no wrapper | External API called directly |
| **Infra** | Platform-level dependency | Database, message queue |

Wrapped dependencies can be swapped. Consumed dependencies cannot. Track which is which — it determines your coupling risk.

## Observability Design

For each component:

- **Logging:** what to log (not "everything" — specific events)
- **Metrics:** what to track (business-relevant, not infra noise)
- **Tracing:** what to trace (cross-component flows, not every function call)
- **Alerting:** when to alert (user-visible impact, not internal noise)

## Decision Framework

For architectural decisions with material trade-offs:

```markdown
### Decision: [Title]
**Context:** [why this decision is needed]
**Options:** [2-3 alternatives with trade-offs]
**Decision:** [what was chosen]
**Rejected:** [what was not chosen and why]
**Consequences:** [what this enables and prevents]
**Reversibility:** [reversible or irreversible — irreversible decisions need more evidence]
```
