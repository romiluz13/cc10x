# Log Analysis Pattern Library

## Log Levels (Functionality-Focused)

**Use log levels to understand functionality**:

```
ERROR:   Functionality errors (breaks user flow, system flow, integration flow)
WARN:    Functionality warnings (might affect functionality)
INFO:    Functionality events (user actions, system events, flow steps)
DEBUG:   Functionality details (detailed functionality flow)
TRACE:   Very detailed functionality information
```

**Focus**: Log levels that help understand functionality, not generic levels.

## Structured Logging (Functionality-Focused)

**Structure logs to understand functionality**:

```typescript
// UNSTRUCTURED (hard to understand functionality)
console.log("User 123 uploaded file at 2024-01-15 10:30:00");

// STRUCTURED (easy to understand functionality)
logger.info("file_upload_start", {
  requestId: "req-123",
  userId: 123,
  fileType: "PDF",
  fileSize: 1024,
  timestamp: "2024-01-15T10:30:00Z",
});

logger.info("file_validation", {
  requestId: "req-123",
  fileType: "PDF",
  fileSize: 1024,
  valid: true,
  reason: "File type and size valid",
});

logger.info("file_stored", {
  requestId: "req-123",
  fileId: "file-123",
  storageUrl: "s3://bucket/file-123.pdf",
  duration: 500,
});

logger.info("crm_api_called", {
  requestId: "req-123",
  crmFileId: "crm-456",
  duration: 2000,
  success: true,
});
```

## Request Tracing (Functionality-Focused)

**Trace requests to understand functionality flow**:

```typescript
// Add request ID to all logs
const requestId = generateRequestId();

logger.info("request_start", {
  requestId,
  method: "POST",
  path: "/api/files/upload",
  userId: 123,
});

// Use request ID in all subsequent logs
logger.info("file_validation", { requestId, fileType: "PDF" });
logger.info("file_stored", { requestId, fileId: "file-123" });
logger.info("crm_api_called", { requestId, crmFileId: "crm-456" });
logger.info("request_end", { requestId, status: 200, duration: 3000 });
```

## Error Logging (Functionality-Focused)

**Log errors to understand functionality failures**:

```typescript
// BAD - Generic error (hard to understand functionality)
logger.error("Error occurred");

// GOOD - Functionality-specific error (easy to understand)
logger.error("file_upload_failed", {
  requestId: "req-123",
  userId: 123,
  fileType: "PDF",
  fileSize: 1024,
  error: "CRM API timeout",
  step: "crm_api_call",
  duration: 30000,
  retryable: true,
});

// GOOD - Error with context (aligned with functionality flow)
try {
  await uploadToCRM(fileMetadata);
} catch (error) {
  logger.error("crm_api_called", {
    requestId: "req-123",
    error: error.message,
    errorCode: error.code,
    step: "crm_api_call",
    retryable: error.retryable,
  });
  throw error;
}
```

## Grep Patterns (Functionality-Focused)

**Use grep to find functionality-specific logs**:

```bash
# Find all file upload requests
grep "file_upload_start" combined.log

# Find all file upload errors
grep "ERROR.*file_upload" combined.log

# Find all requests for specific user
grep "userId=123" combined.log

# Find all CRM API calls
grep "crm_api_called" combined.log

# Find slow requests (> 30 seconds)
grep "request_end" combined.log | awk -F'duration=' '{if ($2 > 30000) print}'

# Trace specific request flow
grep "req-123" combined.log | sort

# Find errors by step
grep "ERROR.*step=crm_api_call" combined.log
```

## Debugging with Logs (Functionality-Focused)

**Use logs to debug functionality issues**:

### Strategy 1: Trace Functionality Flow

```bash
# Find request ID from error log
grep "ERROR.*file_upload" combined.log | head -1
# Output: 2024-01-15T10:30:00Z ERROR file_upload_failed requestId=req-123

# Trace functionality flow using request ID
grep "req-123" combined.log | sort
# Output:
# 2024-01-15T10:30:00Z INFO request_start requestId=req-123 method=POST path=/api/files/upload
# 2024-01-15T10:30:01Z INFO file_validation requestId=req-123 fileType=PDF fileSize=1024 valid=true
# 2024-01-15T10:30:02Z INFO file_stored requestId=req-123 fileId=file-123 storageUrl=s3://...
# 2024-01-15T10:30:03Z ERROR crm_api_called requestId=req-123 error="Connection timeout"
# 2024-01-15T10:30:04Z ERROR file_upload_failed requestId=req-123 reason="CRM API timeout"

# Analysis: Functionality breaks at step 4 (CRM API call fails)
```

### Strategy 2: Compare Expected vs Observed

```bash
# Expected log pattern (from functionality analysis)
# request_start → file_validation → file_stored → crm_api_called → request_end (200)

# Observed log pattern
# request_start → file_validation → file_stored → crm_api_called (ERROR) → file_upload_failed

# Analysis: Divergence at step 4 (CRM API call)
```

### Strategy 3: Analyze by Step

```bash
# Step 1: Request received
grep "request_start.*file_upload" combined.log | tail -10

# Step 2: File validation
grep "file_validation.*req-123" combined.log

# Step 3: File stored
grep "file_stored.*req-123" combined.log

# Step 4: CRM API called (ERROR)
grep "crm_api_called.*req-123" combined.log
# Output: ERROR crm_api_called requestId=req-123 error="Connection timeout"

# Analysis: Functionality breaks at step 4
```

### Strategy 4: Group Errors by Type

```bash
# Find all file upload errors
grep "ERROR.*file_upload" combined.log | tail -20

# Group by error type
grep "ERROR.*file_upload" combined.log | grep -o "error=[^ ]*" | sort | uniq -c
# Output:
#   5 error="Connection timeout"
#   2 error="Invalid file type"
#   1 error="File too large"

# Analyze most common error
grep "ERROR.*file_upload.*Connection timeout" combined.log | tail -5
# Analysis: Most common error is CRM API timeout
```

### Strategy 5: Analyze Performance

```bash
# Find slow requests (> 30 seconds)
grep "request_end.*file_upload" combined.log | awk -F'duration=' '{if ($2 > 30000) print}' | tail -10

# Analyze slow request
grep "req-456" combined.log | grep -E "(duration|file_stored|crm_api_called)"
# Output:
# file_stored duration=500ms
# crm_api_called duration=35000ms
# request_end duration=36000ms

# Analysis: CRM API call takes 35 seconds (affects functionality performance)
```
