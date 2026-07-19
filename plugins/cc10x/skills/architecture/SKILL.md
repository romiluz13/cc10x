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

**Before finalizing any component boundary, apply the Deletion Test and Two-Adapter Rule (defined below under Architecture Vocabulary).** A component that fails the deletion test (complexity vanishes if deleted) or fails the two-adapter rule (it is a port with only one adapter — callers and tests don't count as adapters) is not a real boundary yet — fold it into its caller or defer the split until a second concrete need appears.

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

## Architecture Vocabulary

The canonical deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality, the deletion test, the two-adapter rule) lives in `cc10x:codebase-design`. **Use those terms exactly** — don't restate them here. Depth is leverage at the interface (a lot of behaviour behind a small interface), NOT a lines-ratio — `codebase-design` explicitly rejects the Ousterhout implementation-lines/interface-lines framing.

Three extra terms specific to greenfield architecture (not in codebase-design):

- **Concealed complexity** — work done behind a simple interface. The goal of deep modules.
- **Temporal coupling** — caller must know the order of operations. Design defect — remove or document explicitly.
- **Leaky abstraction** — interface exposes internal details callers must know. Design defect — fix the interface.

Before finalizing any component boundary, apply the **Deletion Test** and **Two-Adapter Rule** as defined in `cc10x:codebase-design` — not restated here. A component that fails the deletion test (complexity vanishes if deleted) or fails the two-adapter rule (it is a port with only one adapter — callers and tests don't count as adapters) is not a real boundary yet — fold it into its caller or defer the split until a second concrete need appears.

## Design It Twice

When a module's interface is non-trivial, design it twice:

1. **First design:** the obvious approach. Write it out fully.
2. **Second design:** a different approach (not a refinement of the first).

Compare both. The first design is usually shallow — it mirrors the implementation. The second design reveals what the interface *should* hide. Use the better one, or a hybrid.

**Why:** One-pass interfaces optimize for the implementer. Two-pass interfaces optimize for the caller.

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

## Note

Deep-module vocabulary, the Deletion Test, and the Two-Adapter Rule are defined once in `cc10x:codebase-design` and pointed to above under **Architecture Vocabulary**. The one-line application rule (a boundary that fails either test is folded into its caller or deferred) is deliberately repeated at its two points of use — Design Components and Architecture Vocabulary; the definitions themselves are not restated.
