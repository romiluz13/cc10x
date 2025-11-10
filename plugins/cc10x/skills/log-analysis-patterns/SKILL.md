---
name: log-analysis-patterns
description: Analyzes logs with functionality-first, context-dependent approach. Use PROACTIVELY when debugging functionality issues. First understands expected functionality using universal questions and context-dependent flows, then analyzes logs to verify functionality or identify where it breaks. Focuses on logs that help understand functionality issues, not generic log analysis. Provides specific log analysis strategies with examples.
allowed-tools: Read, Grep, Glob, Bash
---

# Log Analysis Patterns - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before analyzing logs, understand expected functionality using context-dependent analysis.

**Core Principle**: Understand what functionality should work (using universal questions and context-dependent flows), then analyze logs to verify functionality or identify where it breaks. Logs exist to help understand functionality, not for their own sake.

---

## Step 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

### Reference Template

**Reference**: See [Functionality Analysis Template](../cc10x-orchestrator/templates/functionality-analysis.md) for complete template.

### Process

1. **Detect Code Type**: Identify if this is UI, API, Utility, Integration, Database, Configuration, CLI, or Background Job
2. **Universal Questions First**: Answer Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Answer flow questions based on code type:
   - **UI**: User Flow, Admin Flow, System Flow
   - **API**: Request Flow, Response Flow, Error Flow, Data Flow
   - **Integration**: Integration Flow, Data Flow, Error Flow, State Flow
   - **Database**: Migration Flow, Query Flow, Data Flow, State Flow
   - **Background Jobs**: Job Flow, Processing Flow, State Flow, Error Flow
   - **CLI**: Command Flow, Processing Flow, Output Flow, Error Flow
   - **Configuration**: Configuration Flow, Validation Flow, Error Flow
   - **Utility**: Input Flow, Processing Flow, Output Flow, Error Flow

### Example: File Upload Broken (API Feature)

**Universal Questions (Expected)**:

**Purpose**: Users should be able to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements (Expected)**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely in S3
- Must send file metadata to CRM API
- Must return success response

**Context-Dependent Flows (Expected - API Feature)**:

**Request Flow (Expected)**:

1. API receives POST /api/files/upload request
2. API validates authentication token
3. API validates request body (file, metadata)
4. API validates file type and size
5. API generates unique filename
6. API uploads file to storage service
7. API calls CRM API with file metadata
8. API stores file record in database
9. API returns success response with file ID

**Observed Behavior (What's Broken)**:

- ❌ Request Flow Broken: API receives request → validation fails → no response

**THEN Analyze Logs**: Check logs for request received, validation errors, CRM API calls.

---

## Step 2: Log Analysis (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only analyze logs AFTER you understand expected functionality. Analyze logs to verify functionality or identify where it breaks.

### Functionality-Focused Log Analysis Checklist

**Priority: Critical (Core Functionality)**:

- [ ] Logs show functionality flow (user flow, system flow, integration flow)
- [ ] Logs show functionality errors (errors that break functionality)
- [ ] Logs show functionality performance (performance that affects functionality)
- [ ] Logs help identify where functionality breaks (where expected flow diverges)

**Priority: Important (Supporting Functionality)**:

- [ ] Logs are structured (helps understand functionality)
- [ ] Logs have request IDs (helps trace functionality)
- [ ] Logs have timestamps (helps understand functionality timing)

**Priority: Minor (Can Defer)**:

- [ ] Perfect log structure (if functionality logs are clear)
- [ ] Ideal log levels (if functionality logs are clear)
- [ ] Perfect log aggregation (if functionality logs are searchable)

---

## Step 3: Provide Specific Log Analysis Strategies (WITH EXAMPLES)

**CRITICAL**: Provide specific, actionable log analysis strategies with examples, not generic patterns.

### Strategy 1: Trace Functionality Flow Through Logs

**Example: File Upload Broken**

**Expected Flow** (from functionality analysis):

1. API receives POST /api/files/upload request
2. API validates file type and size
3. API stores file in S3
4. API calls CRM API
5. API returns success response

**Log Analysis**:

```bash
# Find request ID from error log
grep "ERROR.*file_upload" combined.log | head -1
# Output: 2024-01-15T10:30:00Z ERROR file_upload_failed requestId=req-123 userId=456

# Trace functionality flow using request ID
grep "req-123" combined.log | sort
# Output:
# 2024-01-15T10:30:00Z INFO request_start requestId=req-123 method=POST path=/api/files/upload
# 2024-01-15T10:30:01Z INFO file_validation requestId=req-123 fileType=PDF fileSize=1024 valid=true
# 2024-01-15T10:30:02Z INFO file_stored requestId=req-123 fileId=file-123 storageUrl=s3://...
# 2024-01-15T10:30:03Z ERROR crm_api_called requestId=req-123 error="Connection timeout"
# 2024-01-15T10:30:04Z ERROR file_upload_failed requestId=req-123 reason="CRM API timeout"

# Analysis: Functionality breaks at step 4 (CRM API call fails)
# Expected: CRM API called successfully
# Observed: CRM API timeout
# Root cause: CRM API unavailable or slow
```

### Strategy 2: Compare Expected vs Observed Log Patterns

**Example: File Upload Broken**

**Expected Log Pattern** (from functionality analysis):

```
request_start → file_validation → file_stored → crm_api_called → request_end (200)
```

**Observed Log Pattern**:

```
request_start → file_validation → file_stored → crm_api_called (ERROR) → file_upload_failed
```

**Analysis**:

- Expected: All steps succeed, request ends with 200
- Observed: CRM API call fails, request ends with error
- Divergence: Step 4 (CRM API call) fails
- Root cause: CRM API timeout

### Strategy 3: Analyze Logs by Functionality Flow Step

**Example: File Upload Broken**

**Step-by-Step Log Analysis**:

**Step 1: Request Received**

```bash
grep "request_start.*file_upload" combined.log | tail -10
# Expected: Multiple requests received
# Observed: ✅ Requests received
```

**Step 2: File Validation**

```bash
grep "file_validation.*req-123" combined.log
# Expected: file_validation valid=true
# Observed: ✅ file_validation valid=true
```

**Step 3: File Stored**

```bash
grep "file_stored.*req-123" combined.log
# Expected: file_stored fileId=file-123
# Observed: ✅ file_stored fileId=file-123
```

**Step 4: CRM API Called**

```bash
grep "crm_api_called.*req-123" combined.log
# Expected: crm_api_called success=true
# Observed: ❌ crm_api_called error="Connection timeout"
```

**Analysis**: Functionality breaks at step 4 (CRM API call).

### Strategy 4: Analyze Error Logs for Functionality Issues

**Example: File Upload Broken**

**Error Log Analysis**:

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
# Output: All errors occur during CRM API call

# Analysis: Most common error is CRM API timeout (affects functionality)
```

### Strategy 5: Analyze Performance Logs for Functionality Issues

**Example: File Upload Slow**

**Performance Log Analysis**:

```bash
# Find slow file upload requests (> 30 seconds)
grep "request_end.*file_upload" combined.log | awk -F'duration=' '{if ($2 > 30000) print}' | tail -10

# Analyze slow requests
grep "req-456" combined.log | grep -E "(duration|file_stored|crm_api_called)"
# Output:
# file_stored duration=500ms
# crm_api_called duration=35000ms
# request_end duration=36000ms

# Analysis: CRM API call takes 35 seconds (affects functionality performance)
# Expected: Upload completes within 30 seconds
# Observed: Upload takes 36 seconds
# Root cause: CRM API slow
```

---

## Log Analysis Pattern Library

**Reference**: See [PATTERNS.md](./PATTERNS.md) for detailed log analysis patterns including:

- Log levels (functionality-focused)
- Structured logging patterns
- Request tracing strategies
- Error logging patterns
- Grep patterns for debugging
- Step-by-step debugging techniques

---

## Priority Classification

**Critical (Must Have)**:

- Logs show functionality flow (user flow, system flow, integration flow)
- Logs show functionality errors (errors that break functionality)
- Logs help identify where functionality breaks (where expected flow diverges)

**Important (Should Have)**:

- Logs are structured (helps understand functionality)
- Logs have request IDs (helps trace functionality)
- Logs have timestamps (helps understand functionality timing)

**Minor (Can Defer)**:

- Perfect log structure (if functionality logs are clear)
- Ideal log levels (if functionality logs are clear)
- Perfect log aggregation (if functionality logs are searchable)

---

## When to Use

**Use PROACTIVELY when**:

- Analyzing logs for debugging
- Investigating errors
- Troubleshooting functionality issues

**Functionality-First Process**:

1. **First**: Understand expected functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Analyze logs to verify functionality or identify where it breaks
3. **Then**: Use log analysis strategies to find functionality issues
4. **Focus**: Logs that help understand functionality, not generic logs

---

## Skill Overview

- **Skill**: Log Analysis Patterns
- **Purpose**: Analyze logs with functionality-first, context-dependent approach (not generic log analysis)
- **When**: Debugging, log analysis, troubleshooting functionality issues
- **Core Rule**: Functionality first (context-dependent analysis), then log analysis. Analyze logs to verify functionality or identify where it breaks.

---

**Remember**: Logs exist to help understand functionality. Don't analyze logs generically - understand expected functionality first, then analyze logs to verify functionality or identify where it breaks! Provide specific log analysis strategies with examples, not generic patterns.
