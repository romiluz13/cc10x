# Risk Analysis Pattern Library

## 7-Stage Risk Framework (Functionality-Focused)

**Apply to functionality flows, not generically**:

### 1. Data Flow Risks (Based on Functionality)

**What data flows through functionality?**

- What validation is needed?
- What risks affect functionality?

**Example**: File upload - invalid file type breaks upload functionality

**Risk Pattern**:

```
Risk: Invalid data breaks functionality
- Source: [Functionality flow step]
- Impact: [How it breaks functionality]
- Mitigation: [Specific validation/transformation]
```

### 2. Dependency Risks (Based on Functionality)

**What external services does functionality depend on?**

- What happens if dependencies fail?
- What risks affect functionality?

**Example**: File upload - CRM API down breaks upload functionality

**Risk Pattern**:

```
Risk: External dependency failure breaks functionality
- Source: [Functionality flow step]
- Impact: [How it breaks functionality]
- Mitigation: [Retry logic, fallback, graceful degradation]
```

### 3. Timing/Concurrency Risks (Based on Functionality)

**What timing constraints does functionality have?**

- What race conditions might occur?
- What risks affect functionality?

**Example**: File upload - concurrent uploads might cause race conditions

**Risk Pattern**:

```
Risk: Timing/concurrency issue breaks functionality
- Source: [Functionality flow step]
- Impact: [How it breaks functionality]
- Mitigation: [Locks, queues, idempotency]
```

### 4. UX & Accessibility Risks (Based on Functionality)

**What UX issues might prevent functionality use?**

- What accessibility issues might prevent functionality use?
- What risks affect functionality?

**Example**: File upload - missing progress indicator confuses users

**Risk Pattern**:

```
Risk: UX/accessibility issue prevents functionality use
- Source: [User flow step]
- Impact: [How it prevents use]
- Mitigation: [Progress indicator, error messages, keyboard support]
```

### 5. Security & Compliance Risks (Based on Functionality)

**What security issues might break functionality?**

- What compliance issues might affect functionality?
- What risks affect functionality?

**Example**: File upload - malicious files might break functionality

**Risk Pattern**:

```
Risk: Security/compliance issue breaks functionality
- Source: [Functionality flow step]
- Impact: [How it breaks functionality]
- Mitigation: [Validation, sanitization, access control]
```

### 6. Performance & Scalability Risks (Based on Functionality)

**What performance issues might break functionality?**

- What scalability issues might affect functionality?
- What risks affect functionality?

**Example**: File upload - large files might cause timeouts

**Risk Pattern**:

```
Risk: Performance/scalability issue breaks functionality
- Source: [Functionality flow step]
- Impact: [How it breaks functionality]
- Mitigation: [Chunking, caching, optimization]
```

### 7. Failure & Recovery Risks (Based on Functionality)

**What failures might break functionality?**

- How can functionality recover?
- What risks affect functionality?

**Example**: File upload - network failure might break upload

**Risk Pattern**:

```
Risk: Failure breaks functionality without recovery
- Source: [Functionality flow step]
- Impact: [How it breaks functionality]
- Mitigation: [Retry logic, error handling, state recovery]
```

---

## Risk Scoring (Functionality-Focused)

**Score risks by functionality impact**:

```
Risk: [Description specific to functionality]
- Probability: 1-5 (how likely to affect functionality)
- Impact: 1-5 (how much it affects functionality)
- Score: P × I
- Source: [Functionality requirement/flow that created this risk]
- Mitigation: [Specific action to prevent risk from affecting functionality]
- Owner: [Role responsible]
- Status: [Open/Tracking/Mitigated]
```

**Scoring Guide**:

**Probability**:

- 1: Very unlikely (rare edge case)
- 2: Unlikely (occasional)
- 3: Possible (happens sometimes)
- 4: Likely (happens often)
- 5: Very likely (happens frequently)

**Impact**:

- 1: Minor (slight degradation)
- 2: Moderate (some functionality affected)
- 3: Significant (major functionality affected)
- 4: Critical (most functionality broken)
- 5: Catastrophic (complete functionality failure)

**Priority Thresholds**:

- Score 15-25: Critical (must mitigate immediately)
- Score 8-14: Important (should mitigate soon)
- Score 1-7: Minor (can defer)

---

## Risk Mitigation Patterns

### Retry Logic with Exponential Backoff

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  retries = 3,
): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000); // Exponential backoff
    }
  }
  throw new Error("Retry exhausted");
}
```

### Fallback Storage

```typescript
async function handleDependencyFailure(data: Data) {
  // Store in local queue for retry
  await db.queue.create({
    ...data,
    status: "pending",
    retryAt: new Date(Date.now() + 60000),
  });
  // Background job will retry
}
```

### Graceful Degradation

```typescript
async function uploadFile(file: File) {
  try {
    await uploadToPrimaryStorage(file);
  } catch (error) {
    // Fallback to secondary storage
    await uploadToSecondaryStorage(file);
    showNotification("File uploaded to backup storage");
  }
}
```

### Validation & Sanitization

```typescript
function validateAndSanitize(file: File): ValidationResult {
  // Validate file type
  if (!ALLOWED_TYPES.includes(file.type)) {
    return { valid: false, error: "Invalid file type" };
  }
  // Validate file size
  if (file.size > MAX_SIZE) {
    return { valid: false, error: "File too large" };
  }
  // Sanitize filename
  const sanitized = sanitizeFilename(file.name);
  return { valid: true, file: { ...file, name: sanitized } };
}
```

### Rate Limiting

```typescript
const rateLimiter = new RateLimiter({
  windowMs: 60000, // 1 minute
  max: 100, // 100 requests per minute
});

app.post("/api/files/upload", rateLimiter, uploadHandler);
```

### Idempotency

```typescript
async function uploadFile(file: File, idempotencyKey: string) {
  // Check if already processed
  const existing = await db.files.findOne({ idempotencyKey });
  if (existing) return existing;

  // Process upload
  const result = await processUpload(file);
  await db.files.create({ ...result, idempotencyKey });
  return result;
}
```
