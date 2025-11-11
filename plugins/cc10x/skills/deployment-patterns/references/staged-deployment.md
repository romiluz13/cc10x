# Staged Deployment - Functionality-Focused

**Reference**: Part of `deployment-patterns` skill. See main SKILL.md for overview.

## Strategy: Staged Deployment (Based on Functionality Testing)

**CRITICAL**: Staged rollout must test functionality at each stage, not just deployment success.

## Staged Rollout Pattern

**Example: File Upload to CRM**

**Staged Rollout** (tests functionality at each stage):

### Stage 1: 10% of Users (Test Functionality)

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

**Focus**: Test functionality with small user base. Verify core functionality works before scaling.

**Success Criteria**:

- Upload success rate > 95%
- No critical errors
- Functionality works as expected

### Stage 2: 50% of Users (Test Functionality at Scale)

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

**Focus**: Test functionality at medium scale. Verify performance and integration work under load.

**Success Criteria**:

- Upload success rate > 95%
- Upload latency < 30s
- CRM API success rate > 90%
- No performance degradation

### Stage 3: 100% of Users (Full Rollout)

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

**Focus**: Full rollout with comprehensive monitoring. Verify all functionality metrics meet thresholds.

**Success Criteria**:

- Upload success rate > 95%
- Upload latency < 30s
- CRM API success rate > 90%
- Storage success rate > 99%
- All functionality flows working

## Staged Rollout Decision Tree

```
Ready to deploy?
│
├─ Stage 1: 10% rollout
│  ├─ Functionality works? → Continue to Stage 2
│  └─ Functionality broken? → Rollback, investigate, fix
│
├─ Stage 2: 50% rollout
│  ├─ Functionality works at scale? → Continue to Stage 3
│  └─ Functionality broken? → Rollback, investigate, fix
│
└─ Stage 3: 100% rollout
   ├─ Functionality works at full scale? → Success
   └─ Functionality broken? → Rollback, investigate, fix
```

## Functionality Testing at Each Stage

**Stage 1 (10%)**:

- Test core functionality (does it work?)
- Verify basic flows (User Flow, System Flow)
- Check for critical errors

**Stage 2 (50%)**:

- Test functionality at scale (does it work under load?)
- Verify performance (latency, throughput)
- Check integration stability (CRM API, storage)

**Stage 3 (100%)**:

- Test functionality at full scale (does it work for all users?)
- Verify all metrics meet thresholds
- Check for edge cases and failures

## Monitoring During Staged Rollout

**Key Metrics to Monitor**:

- Functionality success rate (core metric)
- Functionality latency (performance)
- Error rate (stability)
- Integration success rate (external dependencies)
- User reports (user impact)

**Alert Thresholds**:

- **Critical**: Success rate < 50% → Immediate rollback
- **Warning**: Success rate < 95% → Investigate, consider rollback
- **Info**: Success rate 95-99% → Monitor, optimize

## Rollback During Staged Rollout

**If functionality breaks at any stage**:

1. **Rollback immediately**: Disable functionality (feature flag)
2. **Investigate**: Understand why functionality broke
3. **Fix**: Address root cause
4. **Test**: Verify fix works in staging
5. **Restart**: Begin staged rollout again from Stage 1

## Best Practices

- **Start small**: Begin with 10% of users
- **Monitor closely**: Watch functionality metrics at each stage
- **Wait between stages**: Allow time to observe functionality (15-30 minutes minimum)
- **Have rollback ready**: Know how to rollback quickly
- **Document stages**: Record what was deployed and when
- **Learn from stages**: Improve based on observations

## Alternative Staged Rollout Patterns

**Pattern 1: Canary Deployment**

- Deploy to single server/instance first
- Monitor functionality
- Gradually expand to more instances

**Pattern 2: Blue-Green Deployment**

- Deploy to green environment
- Test functionality in green
- Switch traffic from blue to green
- Monitor functionality after switch

**Pattern 3: Feature Flag Rollout**

- Deploy code with feature flag disabled
- Enable feature flag for 10% → 50% → 100%
- Monitor functionality at each percentage

---

**See Also**: `references/rollback-strategies.md` for rollback guidance, `references/monitoring-observability.md` for monitoring setup.
