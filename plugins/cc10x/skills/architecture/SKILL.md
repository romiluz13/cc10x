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

## Architecture Vocabulary (Precise Language)

Use these terms to evaluate design quality. They make trade-offs explicit:

| Term | Meaning | Signal |
| ------- | --------- | ------- |
| **Deep module** | Small interface, lots hidden inside | Good — complexity is contained |
| **Shallow module** | Interface as complex as implementation | Bad — wrapper adds complexity without hiding any |
| **Concealed complexity** | Work done behind a simple interface | The goal of deep modules |
| **Leaky abstraction** | Interface exposes internal details callers must know | Design defect — fix the interface |
| **Temporal coupling** | Caller must know the order of operations | Design defect — remove or document explicitly |

### The Deletion Test

For every module, ask: "If I deleted this module and inlined its code at every call site, would the code get simpler or more complex?"

- **Simpler** → the module is shallow. It adds indirection without hiding complexity. Remove it or deepen its interface.
- **More complex** → the module is deep. It earns its existence by hiding complexity.

### The Two-Adapter Rule

When wrapping a third-party dependency:

1. **First adapter** is allowed — it isolates the external API behind your interface.
2. **Second adapter** on top of the first is a smell — it means the first adapter's interface is wrong. Fix the first adapter instead of stacking abstractions.

Three+ layers of adaptation = you're hiding a design problem behind indirection.

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

## Deep-Module Vocabulary

Use these terms exactly — don't substitute. They carry precise meaning from Ousterhout's "A Philosophy of Software Design":

| Term | Means |
| ------ | ------- |
| **module** | A unit of code with an interface and hidden implementation |
| **interface** | The surface a module exposes — the contract, not the signature |
| **seam** | A place where behavior can be substituted (test boundary, adapter point) |
| **adapter** | Code that bridges your interface to an external system |
| **depth** | How much complexity is hidden behind the interface (deep = lots hidden, small interface) |
| **leverage** | Ratio of complexity hidden to interface size. Deep modules have high leverage. |
| **locality** | Whether related logic lives together. Good locality = changes touch few files. |

### Deletion Test

Before adding a module or abstraction, ask: **"If I delete this module, where does the complexity go?"**

- If complexity vanishes → it was a pass-through. Delete it.
- If complexity reappears across N callers → it was earning its keep. Keep it.

This is a falsifiable test for whether an abstraction is justified.

### Two-Adapter Rule

- **One adapter** means a hypothetical seam — something *might* need to vary.
- **Two adapters** means a real seam — something *does* vary.

Don't introduce a seam until you have two concrete adapters that use it. One adapter is premature abstraction; two is evidence-based design.
