# Rollback Strategies - Functionality-Focused

**Reference**: Part of `deployment-patterns` skill. See main SKILL.md for overview.

## Strategy: Rollback Strategy (Based on Functionality)

**CRITICAL**: Rollback strategy must support functionality. Rollback when functionality breaks, not just when deployment fails.

## 3-Level Rollback Model

**Example: File Upload to CRM**

### Level 1: Feature Flag (< 5 min) - Instant Functionality Disable

**Use when**: Functionality breaks, need instant rollback.

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

**Benefits**:

- Instant rollback (< 5 minutes)
- No code changes needed
- Can re-enable quickly if false alarm

**Limitations**:

- Requires feature flag infrastructure
- Doesn't fix underlying issue
- Temporary solution

### Level 2: Configuration Rollback (< 10 min) - Revert Config Affecting Functionality

**Use when**: Configuration breaks functionality.

```bash
# Revert config that affects functionality
git checkout HEAD~1 config/crm-api.js
pm2 restart app

# Monitor functionality
curl -X POST https://api.example.com/api/files/upload -F "file=@test.pdf"
# Expected: 200 OK (if config was the issue)
```

**Benefits**:

- Quick rollback (< 10 minutes)
- No code deployment needed
- Can isolate config issues

**Limitations**:

- Only works if config was the issue
- Requires config version control
- May need service restart

### Level 3: Code Rollback (< 15 min) - Revert Code Breaking Functionality

**Use when**: Code breaks functionality.

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

**Benefits**:

- Fixes root cause
- Permanent solution
- Restores previous working state

**Limitations**:

- Takes longer (< 15 minutes)
- Requires code deployment
- May lose other changes

## Rollback Triggers (Based on Functionality Metrics)

**Example: File Upload to CRM**

### Immediate Rollback (No Discussion) - Functionality Completely Broken

- Upload success rate < 50% (functionality broken)
- Upload error rate > 50% (functionality broken)
- CRM API integration fails > 50% (integration broken)
- File storage fails > 50% (storage broken)
- Data loss or corruption (critical)

**Action**: Rollback immediately using fastest method (Level 1: Feature Flag).

### Evaluate Within 15 Minutes - Functionality Degraded

- Upload success rate < 95% (functionality degraded)
- Upload latency > 30s (performance issue affecting functionality)
- CRM API integration fails > 10% (integration degraded)
- File storage fails > 10% (storage degraded)
- 10+ user reports of upload issues (user impact)

**Action**: Investigate, determine root cause, rollback if needed (Level 2 or 3).

### Monitor But Don't Rollback - Functionality Works But Suboptimal

- Upload success rate 95-99% (acceptable)
- Upload latency 10-30s (acceptable but slow)
- Single user report (may be user error)
- Non-critical functionality issues

**Action**: Monitor, optimize if needed, no rollback required.

## Functionality-Focused Rollback Decision

**Decision Tree**:

```
Functionality broken?
│
├─ Yes, completely broken (< 50% success)
│  └─ Rollback immediately (Level 1: Feature Flag)
│
├─ Yes, degraded (< 95% success)
│  ├─ Config issue? → Level 2: Configuration Rollback
│  └─ Code issue? → Level 3: Code Rollback
│
└─ No, works but suboptimal
   └─ Monitor, optimize, no rollback
```

## Rollback Verification

**After rollback, verify**:

- [ ] Functionality restored (test the specific functionality)
- [ ] Metrics improved (success rate, latency, error rate)
- [ ] User impact resolved (no more user reports)
- [ ] System stable (no cascading failures)

## Post-Rollback Actions

1. **Investigate**: Understand why functionality broke
2. **Fix**: Address root cause
3. **Test**: Verify fix works
4. **Redeploy**: Deploy fix with verification
5. **Monitor**: Watch functionality metrics closely

## Best Practices

- **Have rollback plan ready**: Know how to rollback before deploying
- **Test rollback process**: Verify rollback works in staging
- **Monitor functionality**: Track functionality metrics, not just deployment success
- **Document rollbacks**: Record what was rolled back and why
- **Learn from rollbacks**: Improve deployment process based on rollback causes

---

**See Also**: `references/deployment-steps.md` for deployment guidance, `references/monitoring-observability.md` for monitoring setup.
