# Deployment Patterns - Reference

Reference materials for deployment planning. Use AFTER understanding functionality and project patterns.

## Deployment Strategy Decision Matrix

### Choose deployment approach based on risk:

**ZERO-RISK: Deploy Immediately**

- Test files, documentation, code with flags OFF
- Wait: 0 hours
- Monitor: Deployment success only

**LOW-RISK: Flag-Gated**

- New files not yet integrated
- Utility functions not yet called
- Wait: 1 hour with flag OFF
- Monitor: No errors from new code (should be silent)

**MEDIUM-RISK: Canary**

- Middleware changes, API modifications
- Database migrations (backward compatible)
- Stages: 10% (2-4 hrs) → 50% (4-8 hrs) → 100%
- Monitor: Error rate, latency, success rate

**HIGH-RISK: Extended Canary**

- Authentication, payment processing
- Data writes, breaking DB migrations
- Stages: 1-5% (8-24 hrs) → 10% → 25% → 50% → 75% → 100%
- Each stage: 4-8 hours minimum
- Intensive monitoring at every stage

## The 5-Stage Deployment Sequence

### Stage 1: Infrastructure (ZERO-RISK)

Deploy tests, docs, code with flags OFF

- Wait: 0 hours
- Success: Build succeeds, app healthy

### Stage 2: Integration (LOW-RISK)

All code deployed, flag still OFF

- Wait: 1 hour
- Success: No memory leaks, no new errors

### Stage 3: Canary (MEDIUM-RISK)

Enable for 10% of users

- Wait: 2-4 hours
- Success: Error rate stable, latency within 10% baseline
- Rollback: Level 1 if ANY critical alert

### Stage 4: Partial (MEDIUM-RISK)

Enable for 50% of users

- Wait: 4-8 hours (include overnight if possible)
- Success: Metrics stable at scale

### Stage 5: Full Rollout (HIGH-RISK)

Enable for 100% of users

- Wait: 24 hours continuous monitoring
- Success: Metrics scale linearly, no surprises

## Monitoring Metrics

### Required Dashboard Metrics

| Metric          | Baseline | Warning | Critical | Action                            |
| --------------- | -------- | ------- | -------- | --------------------------------- |
| Error Rate      | <0.05%   | >0.2%   | >0.5%    | Level 1 rollback                  |
| Latency p95     | 150ms    | >300ms  | >500ms   | Investigate, Level 1 if sustained |
| Success Rate    | 99.95%   | <99.8%  | <99.5%   | Level 1 rollback                  |
| Database Errors | <5/min   | >10/min | >50/min  | Level 1, investigate DB           |
| Security Alert  | 0        | ANY     | ANY      | Immediate Level 1 + incident      |

### Custom Metrics to Track

- Feature-specific metrics (e.g., JWT tokens issued)
- Database query performance
- Cache hit rates
- External API call rates

## Deployment Timing

### Best Times

- **Tuesday-Thursday, 10am-2pm** (optimal)
- **Monday, 11am-2pm** (acceptable)

### Never Deploy

- **Fridays after 12pm** - Weekend incident risk
- **Before holidays** - Team unavailable
- **After 4pm** - Team leaving soon
- **During peak traffic** - Increased blast radius

**Exception**: Security hotfixes deploy ASAP (any time)

## Post-Rollback Procedure

After ANY rollback:

1. **Notify team** - #incidents channel
2. **Update status page** - If customer impact
3. **Document incident** - What, when, why rolled back
4. **Keep monitoring** - 24 hours minimum
5. **Schedule postmortem** - Within 48 hours
6. **Fix root cause** - Before re-deployment attempt

## Pre-Deployment Checklist

```
Critical Checks:
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code review complete
- [ ] Rollback strategy documented (which level to use)
- [ ] Monitoring dashboards configured
- [ ] Feature flags configured (if needed)
- [ ] On-call engineer assigned
- [ ] Deployment window confirmed (avoid Fridays!)
- [ ] Alert thresholds configured
- [ ] Database migrations backward compatible
- [ ] Stakeholders notified of schedule
```

## Decision Framework: Blue/Green vs Canary vs Phased

**Blue/Green (Infrastructure-Level)**:

- Use when: Need instant atomic switchover
- Best for: Infrastructure changes, complete version swaps
- Benefit: Instant rollback (flip load balancer)
- Cost: 2x infrastructure during deployment

**Canary (Traffic-Level)**:

- Use when: Testing new code with subset of users
- Best for: Application changes, new features
- Benefit: Gradual risk exposure, real user testing
- Pattern: 10% → 50% → 100%

**Phased (Feature-Level)**:

- Use when: Gradual feature adoption desired
- Best for: Major UX changes, new workflows
- Benefit: User feedback before full rollout
- Pattern: Internal → Beta users → All users
