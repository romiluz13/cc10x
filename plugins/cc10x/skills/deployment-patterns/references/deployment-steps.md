# Deployment Steps - Functionality-Focused

**Reference**: Part of `deployment-patterns` skill. See main SKILL.md for overview.

## Strategy: Deployment Steps (Based on Functionality Flows)

**CRITICAL**: Plan deployment steps aligned with functionality flows. Deploy dependencies first, verify functionality at each step.

## Example: File Upload to CRM

**Deployment Steps** (aligned with System Flow):

### 1. Deploy Backend API (`api/files.ts`)

```bash
# Build backend
npm run build:backend

# Deploy to staging
npm run deploy:staging:backend

# Verify API endpoint works
curl https://staging-api.example.com/api/files/upload -X POST -F "file=@test.pdf"
# Expected: 200 OK with file ID
```

### 2. Deploy Storage Service (`services/storage.ts`)

```bash
# Deploy S3 bucket configuration
aws s3api create-bucket --bucket staging-files --region us-east-1

# Verify storage works
aws s3 ls s3://staging-files/
# Expected: Empty bucket (ready for files)
```

### 3. Deploy CRM Integration (`services/crm-client.ts`)

```bash
# Set CRM API credentials
export CRM_API_KEY=staging_key
export CRM_API_URL=https://staging-crm.example.com

# Verify CRM integration works
curl -H "Authorization: Bearer $CRM_API_KEY" $CRM_API_URL/api/files
# Expected: 200 OK
```

### 4. Deploy Frontend (`components/UploadForm.tsx`)

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

## General Pattern

### Deployment Order Principles

1. **Deploy Dependencies First**: Services/components that other parts depend on
2. **Deploy in Flow Order**: Follow the functionality flow (System Flow, Integration Flow)
3. **Verify at Each Step**: Test functionality after each deployment
4. **Deploy Frontend Last**: UI components typically depend on backend services

### Verification Checklist

After each deployment step:

- [ ] Service/component deployed successfully
- [ ] Functionality works (test the specific functionality)
- [ ] Dependencies available (if other components depend on this)
- [ ] Health checks pass (if applicable)
- [ ] No errors in logs

### Common Deployment Patterns

**Pattern 1: Backend-First**

- Deploy backend services first
- Verify API endpoints work
- Then deploy frontend that depends on backend

**Pattern 2: Database-First**

- Run database migrations first
- Verify schema changes applied
- Then deploy code that uses new schema

**Pattern 3: Infrastructure-First**

- Set up infrastructure (storage, queues, etc.)
- Verify infrastructure accessible
- Then deploy services that use infrastructure

**Pattern 4: Integration-First**

- Set up external integrations first
- Verify integration credentials work
- Then deploy services that use integrations

## Functionality-Focused Deployment

**Key Principle**: Each deployment step should support a specific part of the functionality flow.

**Example Mapping**:

- System Flow Step 1 (receive request) → Deploy Backend API
- System Flow Step 2 (validate) → Deploy Validation Service
- System Flow Step 3 (store) → Deploy Storage Service
- System Flow Step 4 (integrate) → Deploy Integration Service
- System Flow Step 5 (respond) → Deploy Frontend

**Focus**: Deploy in order that supports functionality flow, not generic deployment order.

## Error Handling

**If deployment step fails**:

1. **STOP**: Don't proceed to next step
2. **Investigate**: Check logs, verify configuration
3. **Fix**: Resolve the issue
4. **Verify**: Test functionality before proceeding
5. **Continue**: Only proceed if functionality works

**If functionality broken after deployment**:

1. **Rollback**: Revert the deployment step
2. **Investigate**: Understand why functionality broke
3. **Fix**: Address root cause
4. **Redeploy**: Deploy again with fix
5. **Verify**: Test functionality before proceeding

## Best Practices

- **Deploy incrementally**: One component at a time
- **Verify functionality**: Test after each step
- **Monitor logs**: Watch for errors during deployment
- **Have rollback plan**: Know how to revert each step
- **Document steps**: Record what was deployed and when

---

**See Also**: `references/rollback-strategies.md` for rollback guidance, `references/staged-deployment.md` for staged rollout patterns.
