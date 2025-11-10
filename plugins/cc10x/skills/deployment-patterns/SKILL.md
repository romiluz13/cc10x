---
name: deployment-patterns
description: Plans deployment with functionality-first, context-dependent approach. Use PROACTIVELY when planning feature deployments. First understands functionality using universal questions and context-dependent flows, then plans deployment strategy to support that functionality. Understands project deployment patterns and conventions. Focuses on deployment that enables functionality, not generic deployment patterns. Provides specific deployment and rollback strategies with examples.
allowed-tools: Read, Grep, Glob
---

# Deployment Patterns - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before planning deployment, understand functionality using context-dependent analysis.

**Core Principle**: Understand what functionality needs deployment (using universal questions and context-dependent flows), then plan deployment strategy to support that functionality. Deployment exists to enable functionality, not for its own sake.

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

## Step 2: Understand Project Deployment Patterns (BEFORE Planning)

**CRITICAL**: Understand how this project deploys before planning deployment strategy.

### Project Context Analysis

1. **Read Deployment Configuration**:
   - `package.json` scripts (deploy, build, start)
   - `Dockerfile`, `docker-compose.yml`
   - CI/CD configs (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)
   - Infrastructure configs (`terraform/`, `kubernetes/`, `serverless.yml`)

2. **Identify Deployment Patterns**:
   - Deployment method (Docker, serverless, VM, Kubernetes)
   - Rollback strategy (feature flags, code rollback, config rollback)
   - Staging strategy (blue-green, canary, staged rollout)
   - Monitoring approach (logs, metrics, alerts)

3. **Understand Project Conventions**:
   - How are features deployed? (all at once, feature flags, microservices)
   - How are rollbacks handled? (automated, manual, feature flags)
   - How is monitoring set up? (which metrics, which alerts)

### Example: Project Deployment Patterns

**From `package.json`**:

```json
{
  "scripts": {
    "build": "next build",
    "deploy:staging": "vercel --env staging",
    "deploy:production": "vercel --env production"
  }
}
```

**From `.github/workflows/deploy.yml`**:

```yaml
- name: Deploy to Staging
  run: npm run deploy:staging
- name: Deploy to Production
  run: npm run deploy:production
  if: github.ref == 'refs/heads/main'
```

**Identified Patterns**:

- Deployment method: Vercel (serverless)
- Rollback strategy: Vercel rollback (previous deployment)
- Staging strategy: Staging environment first, then production
- Monitoring: Vercel analytics

**Conventions**:

- Features deployed via Git push (automatic deployment)
- Rollbacks via Vercel dashboard (one-click rollback)
- Monitoring via Vercel analytics (automatic)

---

## Step 3: Plan Deployment Strategy (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only plan deployment AFTER you understand functionality and project deployment patterns. Plan deployment to support functionality, not generic deployment patterns.

### Functionality-Focused Deployment Checklist

**Priority: Critical (Core Functionality)**:

- [ ] Deployment steps support functionality flows (deploy services/components needed for functionality)
- [ ] Deployment order supports functionality dependencies (deploy dependencies first)
- [ ] Rollback strategy supports functionality (can rollback if functionality breaks)
- [ ] Monitoring supports functionality (monitor functionality metrics, not just generic metrics)
- [ ] Health checks verify functionality (check if functionality works, not just if service is up)

**Priority: Important (Supporting Functionality)**:

- [ ] Staged rollout tests functionality (test functionality at each stage, not just deployment)
- [ ] Feature flags support functionality (can disable functionality if broken)
- [ ] Environment variables support functionality (config needed for functionality)
- [ ] Database migrations support functionality (if functionality needs schema changes)

**Priority: Minor (Pattern Compliance)**:

- [ ] Perfect deployment pipeline (if functionality is supported)
- [ ] Ideal rollback strategy (if functionality is supported)
- [ ] Perfect monitoring setup (if functionality is supported)

---

## Step 4: Provide Specific Deployment Strategies (WITH EXAMPLES)

**CRITICAL**: Provide specific, actionable deployment strategies with examples, not generic patterns.

### Strategy 1: Deployment Steps (Based on Functionality Flows)

**Example: File Upload to CRM**

**Deployment Steps** (aligned with System Flow):

1. **Deploy Backend API** (`api/files.ts`):

   ```bash
   # Build backend
   npm run build:backend

   # Deploy to staging
   npm run deploy:staging:backend

   # Verify API endpoint works
   curl https://staging-api.example.com/api/files/upload -X POST -F "file=@test.pdf"
   # Expected: 200 OK with file ID
   ```

2. **Deploy Storage Service** (`services/storage.ts`):

   ```bash
   # Deploy S3 bucket configuration
   aws s3api create-bucket --bucket staging-files --region us-east-1

   # Verify storage works
   aws s3 ls s3://staging-files/
   # Expected: Empty bucket (ready for files)
   ```

3. **Deploy CRM Integration** (`services/crm-client.ts`):

   ```bash
   # Set CRM API credentials
   export CRM_API_KEY=staging_key
   export CRM_API_URL=https://staging-crm.example.com

   # Verify CRM integration works
   curl -H "Authorization: Bearer $CRM_API_KEY" $CRM_API_URL/api/files
   # Expected: 200 OK
   ```

4. **Deploy Frontend** (`components/UploadForm.tsx`):

   ```bash
   # Build frontend
   npm run build:frontend

   # Deploy to staging
   npm run deploy:staging:frontend

   # Verify UI works
   curl https://staging.example.com/upload
   # Expected: 200 OK (page loads)
   ```

**Deployment Order**: Backend API → Storage Service → CRM Integration → Frontend (supports System Flow dependencies)

### Strategy 2: Rollback Strategy (Based on Functionality)

**Example: File Upload to CRM**

**3-Level Rollback Model** (aligned with functionality):

**Level 1: Feature Flag (< 5 min)** - Instant functionality disable:

```bash
# Toggle functionality off
export FILE_UPLOAD_ENABLED=false
pm2 reload app

# Verify functionality disabled
curl https://api.example.com/health | jq '.features.file_upload'
# Expected: false

# Verify UI shows disabled state
curl https://example.com/upload
# Expected: "File upload temporarily unavailable"
```

**Use when**: Functionality breaks, need instant rollback.

**Level 2: Configuration Rollback (< 10 min)** - Revert config affecting functionality:

```bash
# Revert config that affects functionality
git checkout HEAD~1 config/crm-api.js
pm2 restart app

# Monitor functionality
curl -X POST https://api.example.com/api/files/upload -F "file=@test.pdf"
# Expected: 200 OK (if config was the issue)
```

**Use when**: Configuration breaks functionality.

**Level 3: Code Rollback (< 15 min)** - Revert code breaking functionality:

```bash
# Revert code that breaks functionality
git revert abc1234 --no-edit

# MANDATORY: Run tests (verify functionality)
npm test
# Expected: All tests pass

# Deploy
npm run deploy:production

# Monitor functionality for 1 hour minimum
watch -n 5 'curl -X POST https://api.example.com/api/files/upload -F "file=@test.pdf" | jq .success'
# Expected: success: true (functionality works)
```

**Use when**: Code breaks functionality.

### Strategy 3: Rollback Triggers (Based on Functionality Metrics)

**Example: File Upload to CRM**

**Immediate Rollback (No Discussion)** - Functionality completely broken:

- Upload success rate < 50% (functionality broken)
- Upload error rate > 50% (functionality broken)
- CRM API integration fails > 50% (integration broken)
- File storage fails > 50% (storage broken)
- Data loss or corruption (critical)

**Evaluate Within 15 Minutes** - Functionality degraded:

- Upload success rate < 95% (functionality degraded)
- Upload latency > 30s (performance issue affecting functionality)
- CRM API integration fails > 10% (integration degraded)
- File storage fails > 10% (storage degraded)
- 10+ user reports of upload issues (user impact)

**Monitor But Don't Rollback** - Functionality works but suboptimal:

- Upload success rate 95-99% (acceptable)
- Upload latency 10-30s (acceptable but slow)
- Single user report (may be user error)
- Non-critical functionality issues

### Strategy 4: Staged Deployment (Based on Functionality Testing)

**Example: File Upload to CRM**

**Staged Rollout** (tests functionality at each stage):

**Stage 1: 10% of users** (test functionality):

```bash
# Deploy to 10% of users (via feature flag)
export FILE_UPLOAD_ROLLOUT_PERCENT=10
pm2 reload app

# Monitor functionality metrics
watch -n 5 'curl https://api.example.com/metrics | jq ".upload.success_rate"'
# Expected: > 95%

# Rollback if functionality broken
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -lt 95 ]; then
  export FILE_UPLOAD_ENABLED=false
  pm2 reload app
fi
```

**Stage 2: 50% of users** (test functionality at scale):

```bash
# Deploy to 50% of users
export FILE_UPLOAD_ROLLOUT_PERCENT=50
pm2 reload app

# Monitor functionality metrics (more critical at scale)
watch -n 5 'curl https://api.example.com/metrics | jq ".upload.success_rate, .upload.latency, .crm_api.success_rate"'
# Expected: success_rate > 95%, latency < 30s, crm_api.success_rate > 90%

# Rollback if functionality broken
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -lt 95 ] || \
   [ $(curl -s https://api.example.com/metrics | jq ".upload.latency") -gt 30 ]; then
  export FILE_UPLOAD_ENABLED=false
  pm2 reload app
fi
```

**Stage 3: 100% of users** (full rollout):

```bash
# Deploy to 100% of users
export FILE_UPLOAD_ROLLOUT_PERCENT=100
pm2 reload app

# Monitor functionality metrics (full scale)
watch -n 5 'curl https://api.example.com/metrics | jq ".upload.success_rate, .upload.latency, .crm_api.success_rate, .storage.success_rate"'
# Expected: success_rate > 95%, latency < 30s, crm_api.success_rate > 90%, storage.success_rate > 99%

# Rollback if functionality broken
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -lt 95 ] || \
   [ $(curl -s https://api.example.com/metrics | jq ".upload.latency") -gt 30 ] || \
   [ $(curl -s https://api.example.com/metrics | jq ".crm_api.success_rate") -lt 90 ]; then
  export FILE_UPLOAD_ENABLED=false
  pm2 reload app
fi
```

**Focus**: Staged rollout that tests functionality at each stage, not just deployment.

### Strategy 5: Monitoring Setup (Based on Functionality Metrics)

**Example: File Upload to CRM**

**Functionality Metrics** (aligned with flows):

**User Flow Metrics**:

- Upload success rate (core functionality)
- Upload latency (functionality performance)
- Upload error rate (functionality errors)

**System Flow Metrics**:

- File storage success rate (system functionality)
- File storage latency (system performance)
- Database write success rate (data persistence)

**Integration Flow Metrics**:

- CRM API success rate (integration functionality)
- CRM API latency (integration performance)
- CRM API error rate (integration errors)

**Monitoring Setup**:

```bash
# Set up monitoring for functionality metrics
cat > monitoring-config.json <<EOF
{
  "metrics": {
    "upload_success_rate": {
      "type": "gauge",
      "description": "Upload success rate (functionality)",
      "alert_threshold": 95,
      "rollback_threshold": 50
    },
    "upload_latency": {
      "type": "histogram",
      "description": "Upload latency (functionality performance)",
      "alert_threshold": 30,
      "rollback_threshold": 60
    },
    "crm_api_success_rate": {
      "type": "gauge",
      "description": "CRM API success rate (integration functionality)",
      "alert_threshold": 90,
      "rollback_threshold": 50
    },
    "storage_success_rate": {
      "type": "gauge",
      "description": "Storage success rate (system functionality)",
      "alert_threshold": 99,
      "rollback_threshold": 50
    }
  },
  "alerts": {
    "functionality_broken": {
      "condition": "upload_success_rate < 50",
      "action": "rollback_immediate"
    },
    "functionality_degraded": {
      "condition": "upload_success_rate < 95",
      "action": "alert_team"
    }
  }
}
EOF

# Apply monitoring config
curl -X POST https://monitoring.example.com/config -d @monitoring-config.json
```

**Focus**: Monitoring that tracks functionality metrics, not generic metrics.

---

## Reference Materials

**For detailed patterns and reference materials, see:**

- **PATTERNS.md**: Deployment Pattern Library (Blue-Green, Canary, Feature Flag) and Rollback-Ready Design Patterns
- **REFERENCE.md**: Deployment Strategy Decision Matrix, 5-Stage Deployment Sequence, Monitoring Metrics, Deployment Timing, Post-Rollback Procedure, Pre-Deployment Checklist, Decision Framework

---

## Priority Classification

**Critical (Must Have)**:

- Deployment steps support functionality flows (deploy services/components needed for functionality)
- Deployment order supports functionality dependencies (deploy dependencies first)
- Rollback strategy supports functionality (can rollback if functionality breaks)
- Monitoring supports functionality (tracks functionality metrics, not just generic metrics)
- Health checks verify functionality (check if functionality works, not just if service is up)

**Important (Should Have)**:

- Staged rollout tests functionality (test functionality at each stage, not just deployment)
- Feature flags support functionality (can disable functionality if broken)
- Environment variables support functionality (config needed for functionality)
- Database migrations support functionality (if functionality needs schema changes)

**Minor (Can Defer)**:

- Perfect deployment pipeline (if functionality is supported)
- Ideal rollback strategy (if functionality is supported)
- Perfect monitoring setup (if functionality is supported)

---

## When to Use

**Use PROACTIVELY when**:

- Planning feature deployments
- Creating rollback strategies
- Setting up monitoring
- Designing staged rollouts

**Functionality-First Process**:

1. **First**: Understand functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Understand project deployment patterns and conventions
3. **Then**: Plan deployment strategy to support that functionality
4. **Then**: Provide specific deployment strategies with examples
5. **Focus**: Deployment that enables functionality, not generic deployment patterns

---

## Skill Overview

- **Skill**: Deployment Patterns
- **Purpose**: Plan deployment with functionality-first, context-dependent approach (not generic deployment patterns)
- **When**: Planning deployments, rollback strategies, monitoring setup
- **Core Rule**: Functionality first (context-dependent analysis), then deployment. Understand project patterns, then plan to support functionality.

---

**Remember**: Deployment exists to support functionality. Don't plan deployment for deployment's sake! Understand functionality first, understand project patterns second, then plan deployment to support functionality.
