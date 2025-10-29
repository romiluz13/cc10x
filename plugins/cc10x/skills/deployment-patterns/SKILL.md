---
name: deployment-patterns
description: Summarises deployment and rollback guidance for production releases. Use when planning a rollout, staging strategy, or recovery playbook; consult the detailed playbook for full procedures.
allowed-tools: Read, Grep, Glob
---

# Deployment Patterns - Stage 1: Metadata

## Skill Overview

**Name**: Deployment Patterns
**Purpose**: Create safe, reversible production deployments with fast recovery
**When to Use**: Planning deployments, rollback strategies, risk-based rollouts
**Core Rule**: Every deployment must be recoverable in < 5 minutes
**Sections Available**: 3-Level Rollback, Staged Deployment, Monitoring Setup

---

## Core Philosophy

**Deployment = Risk Management**: Minimize blast radius, maximize recovery speed

**Key Principles**:
- Feature flags for instant rollback (< 5 min)
- Staged rollouts catch issues early (10% → 50% → 100%)
- Monitor before proceeding (no alerts = proceed)
- Clear rollback triggers (no debate during incidents)

---

# Stage 2: Quick Reference

## Rollback Decision Framework

### The 3-Level Escalation Model

Start with fastest rollback, escalate only if needed.

**Level 1: Feature Flag (< 5 min)**
```bash
# Toggle feature off
FEATURE_NAME_ENABLED=false
pm2 reload app

# Verify
curl https://api.example.com/health | jq '.features.feature_name'
# Expected: false
```

**Use when**: First response to ANY issue. Requires feature flag infrastructure.

**Level 2: Configuration Rollback (< 10 min)**
```bash
# Revert config files
git checkout HEAD~1 config/database.js config/auth.js
pm2 restart app

# Monitor
curl https://api.example.com/health
```

**Use when**: Feature flag insufficient, config changes caused issue.

**Level 3: Code Rollback (< 15 min)**
```bash
# Revert commit
git revert abc1234 --no-edit

# MANDATORY: Run tests
npm test

# Deploy
npm run deploy:production

# Monitor for 1 hour minimum
```

**Use when**: Configuration rollback insufficient, code changes broke production.

---

## Rollback Triggers

### Immediate Rollback (No Discussion)
- Security incident discovered
- Complete service outage (all users)
- Data loss or corruption
- Error rate >5% sustained
- Critical functionality completely broken

### Evaluate Within 15 Minutes
- Error rate >0.5% sustained for 10 min
- API latency p95 >500ms sustained
- Success rate <99.5% for critical endpoints
- 10+ user reports of same issue

### Monitor But Don't Rollback
- Error rate 0.2-0.5% (warning level)
- Latency spike (investigate first)
- Single user report (may be user error)

---

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

---

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

---

## Monitoring Metrics

### Required Dashboard Metrics

| Metric | Baseline | Warning | Critical | Action |
|--------|----------|---------|----------|--------|
| Error Rate | <0.05% | >0.2% | >0.5% | Level 1 rollback |
| Latency p95 | 150ms | >300ms | >500ms | Investigate, Level 1 if sustained |
| Success Rate | 99.95% | <99.8% | <99.5% | Level 1 rollback |
| Database Errors | <5/min | >10/min | >50/min | Level 1, investigate DB |
| Security Alert | 0 | ANY | ANY | Immediate Level 1 + incident |

### Custom Metrics to Track
- Feature-specific metrics (e.g., JWT tokens issued)
- Database query performance
- Cache hit rates
- External API call rates

---

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

---

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

---

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

---

## Rollback-Ready Design Patterns

**1. Feature Flags**
```typescript
// Every new feature behind a flag
const isEnabled = process.env.NEW_AUTH_ENABLED === 'true';
if (isEnabled) {
  return newAuthFlow(user);
}
return legacyAuthFlow(user);
```

**2. Backward-Compatible Migrations**
```javascript
// ADD columns, don't REMOVE
// NEW tables, don't MODIFY existing
// Can rollback code without DB rollback
await db.schema.alterTable('users', (table) => {
  table.string('new_field').nullable(); // Nullable for compatibility
});
```

**3. Configuration-Driven Behavior**
```javascript
// Allow runtime changes without code deploy
const config = {
  maxRetries: process.env.MAX_RETRIES || 3,
  timeout: process.env.API_TIMEOUT || 5000
};
```

---

## Post-Rollback Procedure

After ANY rollback:

1. **Notify team** - #incidents channel
2. **Update status page** - If customer impact
3. **Document incident** - What, when, why rolled back
4. **Keep monitoring** - 24 hours minimum
5. **Schedule postmortem** - Within 48 hours
6. **Fix root cause** - Before re-deployment attempt

---

## For Detailed Procedures

This skill provides quick reference patterns and decision frameworks. For detailed runbooks, operational roles, and complete procedures, see:

**[Deployment Playbook](PLAYBOOK.md)** includes:
- Detailed rollback procedures with commands
- Complete 5-stage deployment sequence
- Monitoring dashboard setup
- Postmortem templates
- Change ticket templates
- Environment readiness checks

**When to consult playbook**:
- Executing actual rollback (need exact commands)
- Setting up new deployment pipeline
- Creating monitoring dashboards
- Writing postmortem after incident
- Training team on deployment procedures

---

## Integration with Other Skills

- `risk-analysis`: Identify deployment risks before planning
- `verification-before-completion`: Evidence-based verification at each stage
- `integration-patterns`: External API deployment coordination
- `log-analysis-patterns`: Monitoring and alerting setup
