---
name: integration-patterns
description: Designs integrations with functionality-first, context-dependent approach. Use PROACTIVELY when planning features that need integrations. First understands integration requirements using universal questions and context-dependent flows, then designs integrations to support that functionality. Understands project integration patterns and conventions. Focuses on integrations that enable functionality, not generic integration patterns. Provides specific integration strategies with examples.
allowed-tools: Read, Grep, Glob
---

# Integration Patterns - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before designing integrations, understand functionality using context-dependent analysis.

**Core Principle**: Understand what functionality needs integrations (using universal questions and context-dependent flows), then design integrations to support that functionality. Integrations exist to support functionality, not for their own sake.

---

## Quick Start

Design integrations by first understanding functionality, then designing integration strategy.

**Example:**

1. **Understand functionality**: File upload needs CRM sync (Integration Flow)
2. **Understand integration requirements**: CRM API, retry logic, error handling
3. **Design integration**: API client with retry, circuit breaker, error recovery
4. **Align with flows**: Integration supports functionality flows

**Result:** Integration designed to support functionality with reliability patterns.

## Step 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

### Reference Template

**Reference**: See [Functionality Analysis Template](../cc10x-orchestrator/templates/functionality-analysis.md) for complete template.

### Process

1. **Detect Code Type**: Identify if this is UI, API, Utility, Integration, Database, Configuration, CLI, or Background Job
2. **Universal Questions First**: Answer Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Answer flow questions based on code type:
   - **Integration**: Integration Flow, Data Flow, Error Flow, State Flow
   - **API**: Request Flow, Response Flow, Error Flow, Data Flow
   - **UI**: User Flow, Admin Flow, System Flow

### Example: File Upload to CRM Integration

**Universal Questions**:

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and synced to CRM via integration.

**Requirements**:

- Must send file metadata to CRM API
- Must handle CRM API failures gracefully
- Must retry failed CRM API calls
- Must sync file status between systems

**Constraints**:

- Performance: CRM API call must complete within 5 seconds
- Reliability: Must handle CRM API downtime
- Scale: Must handle 100 concurrent uploads

**Dependencies**:

- CRM API (POST /crm/files)
- File storage service (S3)
- Database (file records)

**Edge Cases**:

- CRM API unavailable
- CRM API timeout
- CRM API rate limiting
- Network failure during sync

**Context-Dependent Flows (Integration Feature)**:

**Integration Flow**:

1. System sends file metadata to CRM API (POST /crm/files)
2. CRM API validates request
3. CRM API stores file reference
4. CRM API returns file ID
5. System receives response and updates local record

**Data Flow**:

1. File metadata extracted from local system
2. Data transformed to CRM API format
3. Data sent to CRM API
4. CRM API response received
5. Response data stored in local system

**Error Flow**:

1. CRM API request fails (network, auth, validation)
2. System detects error response
3. System logs error with context
4. System retries if transient error (with exponential backoff)
5. System returns error to caller if permanent failure

**State Flow**:

1. File upload initiated (state: "pending_sync")
2. CRM API called (state: "syncing")
3. CRM API responds (state: "synced")
4. Error occurs (state: "sync_failed")

---

## Step 2: Understand Project Integration Patterns (BEFORE Designing)

**CRITICAL**: Understand how this project handles integrations before designing integrations.

### Project Context Analysis

1. **Read Existing Integrations**:
   - Similar integrations (how are they structured?)
   - Retry patterns (exponential backoff, circuit breakers?)
   - Error handling (how are errors handled?)
   - Monitoring (how are integrations monitored?)

2. **Identify Integration Patterns**:
   - Retry strategy (exponential backoff, fixed delay, no retry?)
   - Circuit breaker (used, not used, which library?)
   - Error handling (try-catch, Result types, error boundaries?)
   - Monitoring (logs, metrics, alerts?)

3. **Understand Integration Conventions**:
   - How are external APIs called? (HTTP clients, SDKs, wrappers?)
   - How are timeouts configured? (per-request, global?)
   - How are retries configured? (max retries, backoff strategy?)

---

## Step 3: Design Integration (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only design integrations AFTER you understand functionality and project integration patterns. Design integrations to support functionality.

### Functionality-Focused Integration Checklist

**Priority: Critical (Core Functionality)**:

- [ ] Integrations support integration flow (external systems work for functionality)
- [ ] Integrations support data flow (data moves correctly for functionality)
- [ ] Error handling supports functionality (errors don't break functionality)
- [ ] Retry logic supports functionality (retries restore functionality)
- [ ] Integrations align with project patterns (follows existing structure)

**Priority: Important (Supporting Functionality)**:

- [ ] Timeouts support functionality (timeouts don't break functionality)
- [ ] Circuit breakers support functionality (fail fast if functionality broken)
- [ ] Monitoring supports functionality (monitor functionality metrics)

**Priority: Minor (Can Defer)**:

- [ ] Perfect integration patterns (if functionality works)
- [ ] Ideal retry strategies (if functionality works)
- [ ] Perfect circuit breaker settings (if functionality works)

---

## Step 4: Provide Specific Integration Strategies (WITH EXAMPLES)

**CRITICAL**: Provide specific, actionable integration strategies with examples, not generic patterns.

### Example: File Upload to CRM Integration

**Based on Functionality Analysis and Project Patterns**:

**1. Retry Logic with Exponential Backoff** (supports functionality reliability):

```typescript
// src/services/crm-client.ts
async function syncFileToCRM(
  metadata: CRMFileMetadata,
  retries = 3,
): Promise<string> {
  const baseDelay = 1000; // 1 second
  const maxDelay = 30000; // 30 seconds

  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      const response = await axios.post(`${CRM_API_URL}/files`, metadata, {
        headers: { Authorization: `Bearer ${CRM_API_KEY}` },
        timeout: 5000, // 5 seconds (from constraints)
      });

      if (response.data.status === "success") {
        return response.data.fileId;
      }

      throw new Error(response.data.message || "CRM API returned error");
    } catch (error) {
      const isLastAttempt = attempt === retries - 1;
      const isTransientError =
        axios.isAxiosError(error) &&
        (error.code === "ECONNABORTED" ||
          error.code === "ECONNRESET" ||
          (error.response?.status && error.response.status >= 500));

      if (isLastAttempt || !isTransientError) {
        throw new Error(
          `Failed to sync file to CRM after ${retries} attempts: ${error instanceof Error ? error.message : "Unknown error"}`,
        );
      }

      // Exponential backoff with jitter
      const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
      const jitter = Math.random() * 1000; // Add jitter to prevent thundering herd
      await sleep(delay + jitter);
    }
  }

  throw new Error("Unexpected retry exhaustion");
}
```

**2. Circuit Breaker** (supports functionality reliability):

```typescript
// src/services/crm-circuit-breaker.ts
class CRMCircuitBreaker {
  private failures = 0;
  private state: "closed" | "open" | "half-open" = "closed";
  private nextAttempt = 0;

  constructor(
    private failureThreshold = 5,
    private cooldownWindow = 60000, // 1 minute
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === "open") {
      if (Date.now() < this.nextAttempt) {
        throw new Error("Circuit breaker is open - CRM API unavailable");
      }
      this.state = "half-open";
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = "closed";
  }

  private onFailure() {
    this.failures++;
    if (this.failures >= this.failureThreshold) {
      this.state = "open";
      this.nextAttempt = Date.now() + this.cooldownWindow;
    }
  }
}

// Usage
const circuitBreaker = new CRMCircuitBreaker();
const crmFileId = await circuitBreaker.execute(() => syncFileToCRM(metadata));
```

**3. Error Handling** (supports functionality):

```typescript
// src/services/crm-client.ts
export async function syncFileToCRM(
  metadata: CRMFileMetadata,
): Promise<string> {
  try {
    return await syncFileToCRMWithRetry(metadata);
  } catch (error) {
    // Store for later retry (supports functionality recovery)
    await db.files.update(
      { id: metadata.fileId },
      {
        status: "sync_failed",
        syncError: error instanceof Error ? error.message : "Unknown error",
        syncRetryAt: new Date(Date.now() + 60000), // Retry in 1 minute
      },
    );

    // Log for monitoring (supports functionality debugging)
    logger.error("crm_sync_failed", {
      fileId: metadata.fileId,
      error: error instanceof Error ? error.message : "Unknown error",
      retryScheduled: true,
    });

    // Return error to caller (supports functionality error handling)
    throw new Error(
      `CRM sync failed: ${error instanceof Error ? error.message : "Unknown error"}`,
    );
  }
}
```

**Focus**: Integration strategies that support functionality flows, aligned with project patterns, not generic patterns.

---

## Troubleshooting

**Common Issues:**

1. **Integration design without understanding functionality**
   - **Symptom**: Integration doesn't support functionality flows
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, then design integration
   - **Prevention**: Always understand functionality before integration design

2. **Generic integration patterns instead of functionality-focused**
   - **Symptom**: Integration follows generic patterns but doesn't support functionality
   - **Cause**: Didn't map functionality flows to integration needs
   - **Fix**: Map flows to integration, design to support flows
   - **Prevention**: Always map functionality to integration needs first

3. **Integration design not aligned with project patterns**
   - **Symptom**: Integration doesn't match project's integration patterns
   - **Cause**: Didn't understand project integration patterns
   - **Fix**: Understand project patterns, align integration design
   - **Prevention**: Always understand project patterns first

**If issues persist:**

- Verify functionality analysis was completed first
- Check that functionality flows were mapped to integration needs
- Ensure integration design aligns with project patterns
- Review integration pattern library for detailed guidance

## Integration Pattern Library (Reference - Use AFTER Functionality Understood)

### Reliability Patterns (Functionality-Focused)

**Use AFTER functionality is understood**:

```
Reliability (Based on Functionality)
- [ ] Timeouts set (client + server) - supports functionality performance
- [ ] Retries with exponential backoff and jitter - supports functionality reliability
- [ ] Idempotency keys for retryable operations - supports functionality reliability
- [ ] Circuit breaker around downstream dependencies - supports functionality reliability

Resilience & Consistency (Based on Functionality)
- [ ] Dead-letter queue or compensating actions - supports functionality recovery
- [ ] Outbox/inbox where needed (avoid dual writes) - supports functionality consistency
- [ ] Event/version compatibility; schema evolution plan - supports functionality evolution

Observability & Ops (Based on Functionality)
- [ ] Correlated logs/trace IDs - supports functionality debugging
- [ ] Dashboards and alerts for functionality SLOs - supports functionality monitoring
- [ ] Runbooks for common functionality failures - supports functionality recovery
```

---

## Priority Classification

**Critical (Must Have)**:

- Integrations support core functionality (integration flow, data flow)
- Integrations align with project patterns (follows existing structure)
- Blocks functionality if missing
- Required for functionality to work

**Important (Should Have)**:

- Integrations support functionality growth
- Integrations support functionality changes
- Integrations support functionality reliability

**Minor (Can Defer)**:

- Perfect integration patterns (if functionality works)
- Ideal retry strategies (if functionality works)
- Perfect circuit breaker settings (if functionality works)

---

## When to Use

**Use PROACTIVELY when**:

- Designing integrations
- Planning service contracts
- Implementing retry strategies
- Handling integration failures

**Functionality-First Process**:

1. **First**: Understand functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Understand project integration patterns and conventions
3. **Then**: Design integrations aligned with project patterns to support functionality
4. **Then**: Apply integration patterns (retry, circuit breaker, error handling)
5. **Focus**: Integrations that enable functionality, not generic integration patterns

---

## Skill Overview

- **Skill**: Integration Patterns
- **Purpose**: Design integrations with functionality-first, context-dependent approach (not generic integration patterns)
- **When**: Designing integrations, planning service contracts
- **Core Rule**: Functionality first (context-dependent analysis), then integration design. Understand project patterns, then design integrations aligned with patterns to support functionality.

---

**Remember**: Integrations exist to support functionality. Don't design integrations generically - understand functionality first, understand project patterns second, then design integrations aligned with patterns to support functionality! Provide specific integration strategies with examples, not generic patterns.
