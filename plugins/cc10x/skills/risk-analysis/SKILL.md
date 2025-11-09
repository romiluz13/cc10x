---
name: risk-analysis
description: Identifies risks with functionality-first, context-dependent approach. Use PROACTIVELY when planning features or reviewing code. First understands functionality using universal questions and context-dependent flows, then identifies risks specific to that functionality. Focuses on risks that affect functionality, not generic risks. Provides specific mitigation strategies with examples.
allowed-tools: Read, Grep, Glob
---

# Risk Analysis - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before analyzing risks, understand functionality using context-dependent analysis.

**Core Principle**: Understand what functionality needs risk analysis (using universal questions and context-dependent flows), then identify risks specific to that functionality. Risks exist in the context of functionality, not in isolation.

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

### Example: File Upload to CRM (UI Feature)

**Universal Questions**:

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely in S3
- Must send file metadata to CRM API
- Must display upload progress to user
- Must handle errors gracefully

**Constraints**:

- Performance: Upload must complete within 30 seconds for files up to 10MB
- Scale: Must handle 100 concurrent uploads
- Security: Files must be encrypted at rest, access controlled
- Storage: 100GB storage limit

**Dependencies**:

- Files: `components/UploadForm.tsx`, `api/files.ts`, `services/storage.ts`, `services/crm-client.ts`
- APIs: CRM API (POST /crm/files)
- Services: S3 storage service, CRM API service
- Libraries: `aws-sdk`, `axios`, `react-dropzone`

**Edge Cases**:

- File exceeds size limit
- Invalid file type
- Network failure during upload
- CRM API unavailable
- Storage quota exceeded

**Verification**:

- E2E tests: Complete user flow from upload to CRM visibility
- Acceptance criteria: File appears in CRM within 5 seconds
- Success metrics: 99% upload success rate, <30s upload time

**Context**:

- Location: `src/features/file-upload/`
- Codebase structure: React frontend, Node.js backend, PostgreSQL database
- Architecture: MVC pattern, RESTful API

**Context-Dependent Flows (UI Feature)**:

**User Flow**:

1. User navigates to "Upload File" page
2. User selects file from device
3. User sees upload progress indicator (0% → 100%)
4. User sees success message: "File uploaded successfully"
5. User sees link to view uploaded file

**System Flow**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type and size
3. System stores file in secure storage (S3 bucket)
4. System sends file metadata to CRM API
5. System stores file record in database
6. System returns success response to user

**Integration Flow**:

1. System sends file metadata to CRM API (POST /crm/files)
2. CRM API stores file reference
3. CRM API returns file ID
4. System receives response and updates local record

---

## Step 2: Risk Identification (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only identify risks AFTER you understand functionality. Focus on risks specific to that functionality, not generic risks.

### Functionality-Focused Risk Checklist

**Priority: Critical (Blocks Functionality)**:

- [ ] Data flow risks that break functionality (invalid data, missing validation, data corruption)
- [ ] Dependency risks that break functionality (external API down, service unavailable, integration failure)
- [ ] Timing risks that break functionality (timeouts, race conditions, concurrency issues)
- [ ] Security risks that break functionality (injection attacks, broken auth, unauthorized access)
- [ ] Performance risks that break functionality (timeouts, crashes, resource exhaustion)
- [ ] Failure risks that break functionality (network errors, storage failures, system crashes)

**Priority: Important (Affects Functionality)**:

- [ ] UX risks that degrade functionality (confusing flows, missing feedback, poor error messages)
- [ ] Performance risks that degrade functionality (slow loading, laggy interactions, high latency)
- [ ] Scalability risks that affect functionality (can't handle load, resource limits)

**Priority: Minor (Can Defer)**:

- [ ] Generic risks that don't affect functionality
- [ ] Perfect risk mitigation (if functionality works)
- [ ] Ideal risk monitoring (if functionality works)

---

## Step 3: Risk Analysis Framework (Based on Functionality)

**⚠️ Use this framework to analyze functionality-specific risks, not generic risks**.

### 7-Stage Risk Framework (Applied to Functionality)

**Apply to functionality flows, not generically**:

1. **Data Flow Risks** (Based on Functionality):
   - What data flows through functionality?
   - What validation is needed?
   - What risks affect functionality?
   - **Example**: File upload - invalid file type breaks upload functionality

2. **Dependency Risks** (Based on Functionality):
   - What external services does functionality depend on?
   - What happens if dependencies fail?
   - What risks affect functionality?
   - **Example**: File upload - CRM API down breaks upload functionality

3. **Timing/Concurrency Risks** (Based on Functionality):
   - What timing constraints does functionality have?
   - What race conditions might occur?
   - What risks affect functionality?
   - **Example**: File upload - concurrent uploads might cause race conditions

4. **UX & Accessibility Risks** (Based on Functionality):
   - What UX issues might prevent functionality use?
   - What accessibility issues might prevent functionality use?
   - What risks affect functionality?
   - **Example**: File upload - missing progress indicator confuses users

5. **Security & Compliance Risks** (Based on Functionality):
   - What security issues might break functionality?
   - What compliance issues might affect functionality?
   - What risks affect functionality?
   - **Example**: File upload - malicious files might break functionality

6. **Performance & Scalability Risks** (Based on Functionality):
   - What performance issues might break functionality?
   - What scalability issues might affect functionality?
   - What risks affect functionality?
   - **Example**: File upload - large files might cause timeouts

7. **Failure & Recovery Risks** (Based on Functionality):
   - What failures might break functionality?
   - How can functionality recover?
   - What risks affect functionality?
   - **Example**: File upload - network failure might break upload

### Risk Scoring (Functionality-Focused)

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

---

## Step 4: Provide Specific Mitigation Strategies (WITH EXAMPLES)

**CRITICAL**: Provide specific, actionable mitigation strategies with examples, not generic patterns.

### Example Risk Register: File Upload to CRM

**Based on Functionality Analysis**:

**Critical Risks (Blocks Functionality)**:

**Risk 1: CRM API Down Prevents File Upload**

- **Probability**: 3 (happens occasionally)
- **Impact**: 5 (completely breaks functionality)
- **Score**: 15
- **Source**: Integration flow requirement (System Flow step 4: "System sends file metadata to CRM API")
- **Mitigation**:

  ```typescript
  // Retry logic with exponential backoff
  async function uploadToCRM(
    fileMetadata: FileMetadata,
    retries = 3,
  ): Promise<string> {
    for (let i = 0; i < retries; i++) {
      try {
        const response = await axios.post(
          CRM_API_URL + "/files",
          fileMetadata,
          {
            timeout: 5000,
            headers: { Authorization: `Bearer ${CRM_API_KEY}` },
          },
        );
        return response.data.fileId;
      } catch (error) {
        if (i === retries - 1) throw error;
        await sleep(Math.pow(2, i) * 1000); // Exponential backoff
      }
    }
  }

  // Fallback storage if CRM API fails
  async function handleCRMUploadFailure(fileMetadata: FileMetadata) {
    await db.files.create({
      ...fileMetadata,
      status: "pending_sync",
      crm_sync_retry_at: new Date(Date.now() + 60000), // Retry in 1 minute
    });
    // Background job will retry CRM sync
  }

  // User notification
  if (crmUploadFailed) {
    showNotification(
      "File uploaded but CRM sync pending. Will retry automatically.",
    );
  }
  ```

- **Owner**: Backend team
- **Status**: Open

**Risk 2: File Validation Fails, Malicious Files Break Functionality**

- **Probability**: 2 (rare but possible)
- **Impact**: 5 (breaks functionality)
- **Score**: 10
- **Source**: System flow requirement (System Flow step 2: "System validates file type and size")
- **Mitigation**:

  ```typescript
  // Strict file type validation
  const ALLOWED_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg",
    "image/png",
  ];
  const MAX_SIZE = 10 * 1024 * 1024; // 10MB

  function validateFile(file: File): ValidationResult {
    // Check MIME type (not just extension)
    if (!ALLOWED_TYPES.includes(file.type)) {
      return {
        valid: false,
        error: "File type not supported. Only PDF, DOCX, JPG, PNG allowed.",
      };
    }

    // Check file size
    if (file.size > MAX_SIZE) {
      return {
        valid: false,
        error: `File exceeds ${MAX_SIZE / 1024 / 1024}MB limit.`,
      };
    }

    // Check file extension matches MIME type
    const extension = file.name.split(".").pop()?.toLowerCase();
    const expectedExtensions = {
      "application/pdf": ["pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        ["docx"],
      "image/jpeg": ["jpg", "jpeg"],
      "image/png": ["png"],
    };
    if (!expectedExtensions[file.type]?.includes(extension || "")) {
      return {
        valid: false,
        error: "File extension does not match file type.",
      };
    }

    return { valid: true };
  }

  // Virus scanning (if available)
  async function scanFile(file: File): Promise<ScanResult> {
    const formData = new FormData();
    formData.append("file", file);
    const response = await axios.post(SCAN_API_URL, formData);
    return response.data; // { clean: true/false, threats: [...] }
  }
  ```

- **Owner**: Backend team
- **Status**: Open

**Risk 3: Network Failure During Upload Breaks Functionality**

- **Probability**: 4 (common)
- **Impact**: 5 (breaks functionality)
- **Score**: 20
- **Source**: User flow requirement (User Flow step 3: "User sees upload progress")
- **Mitigation**:

  ```typescript
  // Chunked upload with resume capability
  async function uploadFileChunked(
    file: File,
    onProgress: (progress: number) => void,
  ): Promise<string> {
    const CHUNK_SIZE = 1024 * 1024; // 1MB chunks
    const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
    const uploadId = await initiateUpload(file.name, file.size);

    for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
      const start = chunkIndex * CHUNK_SIZE;
      const end = Math.min(start + CHUNK_SIZE, file.size);
      const chunk = file.slice(start, end);

      let retries = 3;
      while (retries > 0) {
        try {
          await uploadChunk(uploadId, chunkIndex, chunk);
          onProgress(((chunkIndex + 1) / totalChunks) * 100);
          break;
        } catch (error) {
          retries--;
          if (retries === 0) throw error;
          await sleep(1000 * (4 - retries)); // Exponential backoff
        }
      }
    }

    return await finalizeUpload(uploadId);
  }

  // Resume failed upload
  async function resumeUpload(uploadId: string, file: File): Promise<string> {
    const status = await getUploadStatus(uploadId);
    const uploadedChunks = status.uploadedChunks;
    // Resume from last uploaded chunk
    return await uploadFileChunked(
      file.slice(uploadedChunks * CHUNK_SIZE),
      onProgress,
    );
  }
  ```

- **Owner**: Frontend team
- **Status**: Open

**Important Risks (Affects Functionality)**:

**Risk 4: Large Files Cause Slow Upload, Degrades UX**

- **Probability**: 4 (common)
- **Impact**: 3 (affects functionality)
- **Score**: 12
- **Source**: User flow requirement (User Flow step 3: "User sees upload progress")
- **Mitigation**:

  ```typescript
  // Progress indicator with estimated time
  function UploadProgress({ progress, speed }: { progress: number, speed: number }) {
    const remaining = 100 - progress;
    const estimatedSeconds = Math.ceil((remaining / 100) * fileSize / speed);

    return (
      <div>
        <ProgressBar value={progress} />
        <div>Uploading... {progress}%</div>
        <div>Estimated time remaining: {formatTime(estimatedSeconds)}</div>
        <div>Speed: {formatBytes(speed)}/s</div>
      </div>
    );
  }

  // Chunked upload for large files
  if (file.size > 5 * 1024 * 1024) { // > 5MB
    await uploadFileChunked(file, onProgress);
  } else {
    await uploadFileDirect(file, onProgress);
  }
  ```

- **Owner**: Frontend team
- **Status**: Open

**Risk 5: Storage Quota Exceeded Breaks Functionality**

- **Probability**: 2 (rare)
- **Impact**: 4 (breaks functionality)
- **Score**: 8
- **Source**: Constraint (Storage: 100GB storage limit)
- **Mitigation**:

  ```typescript
  // Check storage quota before upload
  async function checkStorageQuota(): Promise<{
    available: boolean;
    used: number;
    limit: number;
  }> {
    const usage = await db.storage.getUsage();
    const limit = 100 * 1024 * 1024 * 1024; // 100GB
    return {
      available: usage.used < limit,
      used: usage.used,
      limit: limit,
    };
  }

  // Prevent upload if quota exceeded
  const quota = await checkStorageQuota();
  if (!quota.available) {
    showError(
      `Storage quota exceeded. ${formatBytes(quota.used)} / ${formatBytes(quota.limit)} used.`,
    );
    return;
  }

  // Warn user if approaching limit
  if (quota.used / quota.limit > 0.9) {
    showWarning(
      `Storage almost full. ${formatBytes(quota.limit - quota.used)} remaining.`,
    );
  }
  ```

- **Owner**: Backend team
- **Status**: Open

**Minor Risks (Can Defer)**:

**Risk 6: Perfect Security Headers Missing**

- **Probability**: 1 (low)
- **Impact**: 1 (doesn't affect functionality)
- **Score**: 1
- **Source**: Generic best practice (not functionality-specific)
- **Mitigation**: Add security headers (defer if functionality works)
- **Owner**: DevOps team
- **Status**: Deferred

---

## Priority Classification

**Critical (Must Mitigate)**:

- Blocks functionality (breaks user flow, system flow, integration flow)
- Prevents feature from working
- Breaks functionality completely
- **Action**: Mitigate immediately, block deployment if not mitigated

**Important (Should Mitigate)**:

- Affects functionality negatively (degrades user experience, slows functionality)
- Degrades functionality significantly
- **Action**: Mitigate before production, monitor closely

**Minor (Can Defer)**:

- Doesn't affect functionality (generic risks, perfect mitigation)
- Generic best practices
- **Action**: Defer to future iteration, document for reference

---

## When to Use

**Use PROACTIVELY when**:

- Planning new features
- Reviewing code for risks
- Analyzing security vulnerabilities
- Assessing performance risks
- Before deployment

**Functionality-First Process**:

1. **First**: Understand functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Identify risks specific to that functionality (not generic risks)
3. **Then**: Apply 7-stage framework to analyze functionality-specific risks
4. **Then**: Provide specific mitigation strategies with examples
5. **Focus**: Risks that affect functionality, not generic risks

---

## Skill Overview

- **Skill**: Risk Analysis
- **Purpose**: Identify risks with functionality-first, context-dependent approach (not generic risk framework)
- **When**: Planning features, reviewing code, before deployment
- **Core Rule**: Functionality first (context-dependent analysis), then risks. Focus on risks specific to functionality.

---

## References

- [Risk Analysis Playbook](PLAYBOOK.md) - Detailed framework (use AFTER functionality understood)
- Related skills: `security-patterns`, `performance-patterns`, `verification-before-completion`

---

**Remember**: Risks exist in the context of functionality. Don't analyze risks generically - analyze risks that affect functionality! Provide specific mitigation strategies with examples, not generic patterns.
