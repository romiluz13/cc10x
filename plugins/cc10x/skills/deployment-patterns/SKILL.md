---
name: deployment-patterns
description: Rollback strategies and staged deployment patterns for production-ready feature releases. Creates fast recovery procedures with 3-level escalation (feature flag under 5 minutes, configuration under 10 minutes, code rollback under 15 minutes) and risk-aware deployment sequences (5-stage rollout from infrastructure to canary to partial to full). Use when planning production deployments for new features, creating disaster recovery procedures, designing staged rollouts to minimize blast radius, or defining rollback triggers and monitoring metrics. Provides rollback strategy templates, deployment sequencing patterns, monitoring dashboard guidance, and failure mode analysis integration. Loaded by devops-planner agent during feature planning Phase 6-7 or explicitly for deployment planning tasks.
license: MIT
---

# Deployment Patterns - Production Readiness

**Core Philosophy**: Every deployment must be recoverable in < 5 minutes. Staged rollouts catch issues before they affect all users.

---

## Progressive Loading Stages

- **Purpose**: Create fast recovery procedures when deployments go wrong
- **Target**: < 5 minute recovery time for Level 1
- **Levels**: Feature Flag → Configuration → Code Rollback
- **Use when**: Planning any production deployment
- **Sections Available**: 3-Level Rollback, Recovery Procedures, Rollback Triggers

---

## Stage 1: Rollback Strategies

### The 3-Level Escalation Model

**Philosophy**: Start with fastest, least disruptive rollback. Escalate only if needed.

#### Level 1: Feature Flag (< 5 min) ⚡

**When to use:** First response to ANY production issue

**Mechanism:** Toggle feature off via environment variable or configuration

**Procedure:**
```bash
# Update environment variable
FEATURE_NAME_ENABLED=false

# Restart service (zero-downtime reload)
pm2 reload app
# or
kubectl rollout restart deployment/app

# Verify flag is off
curl https://api.example.com/health | jq '.features.feature_name'
# Expected: false
```

**Benefits:**
- Fastest recovery (< 5 minutes)
- No code changes required
- Instant effect (after restart)
- Can re-enable quickly if false alarm

**Drawbacks:**
- Requires feature flag infrastructure
- Only works if flag controls the feature
- Doesn't fix underlying code issues

**When this isn't enough:**
- Feature flag doesn't exist
- Multiple features affected
- Configuration changes needed

---

#### Level 2: Configuration Rollback (< 10 min)

**When to use:** Feature flag insufficient, need to revert configuration

**Mechanism:** Revert configuration files to previous version

**Procedure:**
```bash
# Identify configuration files changed
git log --oneline config/ | head -5

# Revert specific config files
git checkout HEAD~1 config/database.js config/auth.js

# Verify changes
git diff HEAD config/

# Restart with new config
pm2 restart app

# Run health checks
npm run health:check
curl https://api.example.com/health

# Monitor for 10 minutes
watch -n 30 'curl -s https://api.example.com/metrics | jq ".error_rate"'
```

**Benefits:**
- Faster than full code rollback
- Reverts configuration without touching logic
- Can fix many deployment issues

**Drawbacks:**
- Only fixes config-related problems
- May break features relying on new config
- Requires knowing which config changed

**When this isn't enough:**
- Code changes caused the issue
- Database migrations ran
- Multiple components affected

---

#### Level 3: Code Rollback (< 15 min)

**When to use:** Configuration rollback insufficient, need to revert code

**Mechanism:** Git revert specific commits or rollback to previous version

**Procedure:**
```bash
# Identify problematic commit
git log --oneline --graph | head -10
# Find: feat: add authentication (abc1234)

# Option A: Revert specific commit
git revert abc1234 --no-edit
# Creates a new commit that undoes abc1234

# Option B: Rollback to previous tag
git checkout v1.2.3
# For emergency only (loses all commits after tag)

# Run full test suite (MANDATORY)
npm test
# Must see: All tests passing

# Build for production
npm run build

# Deploy
npm run deploy:production
# or
kubectl set image deployment/app app=myapp:v1.2.3

# Monitor deployment progress
kubectl rollout status deployment/app

# Verify deployment
curl https://api.example.com/version | jq '.commit'
# Should NOT show problematic commit

# Monitor for 1 hour minimum
# Dashboard: https://dashboard.example.com/health
```

**Files to Revert (Document in Rollback Plan):**
- **DELETE**: New files created in problematic commit
- **RESTORE**: Modified files to previous version
- **REVERT**: Database migrations (if applicable)

**Benefits:**
- Fixes code-level issues
- Complete rollback to working state
- Verifiable with tests

**Drawbacks:**
- Takes longer (10-15 minutes)
- Loses new features (if reverting to tag)
- May require database rollback
- Higher complexity

**Database Rollback (if needed):**
```bash
# Identify migration to rollback
npm run migrate:status

# Rollback migration
npm run migrate:down

# Verify database state
psql -c "\dt" | grep table_name
```

---

### Rollback Triggers

**Define clear criteria for when to rollback:**

#### Immediate Rollback (No Discussion)
- Security incident or vulnerability discovered
- Complete service outage (all users affected)
- Data loss or corruption detected
- Error rate >5% sustained
- Critical functionality completely broken

#### Evaluate Rollback Within 15 Minutes
- Error rate >0.5% sustained for 10 minutes
- API latency p95 >500ms sustained
- Success rate <99.5% for critical endpoints
- 10+ user reports of same issue
- Database connection pool exhausted

#### Monitor But Don't Rollback (Yet)
- Error rate 0.2-0.5% (warning level)
- Latency spike (investigate first)
- Single user report (may be user error)
- Non-critical feature broken

---

### Rollback Decision Matrix

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Error Rate | >0.2% | >0.5% | Level 1 rollback |
| Latency p95 | >300ms | >500ms | Investigate, Level 1 if sustained |
| Success Rate | <99.8% | <99.5% | Level 1 rollback |
| Database Errors | >10/min | >50/min | Level 1, investigate DB |
| Security Alert | ANY | ANY | Immediate Level 1 + incident response |

---

### Post-Rollback Procedure

**After executing ANY rollback:**

1. **Notify team** - Slack #incidents channel
2. **Update status page** - If customer-facing impact
3. **Document incident** - What happened, when, why rolled back
4. **Keep monitoring** - 24 hours minimum post-rollback
5. **Schedule postmortem** - Within 48 hours
6. **Fix root cause** - Before attempting re-deployment

**Postmortem Template:**
```markdown
## Incident: [Feature Name] Rollback

**Date:** YYYY-MM-DD HH:MM UTC
**Duration:** [X] minutes from deploy to rollback
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW]

### Timeline
- HH:MM - Deployment started
- HH:MM - Issue first detected
- HH:MM - Rollback decision made
- HH:MM - Rollback completed
- HH:MM - Service restored

### Root Cause
[Technical explanation of what went wrong]

### Impact
- Users affected: [X]
- Duration: [X] minutes
- Customer complaints: [X]
- Revenue impact: $[X]

### Rollback Level Used
Level [1/2/3]: [Feature Flag/Configuration/Code]
Recovery time: [X] minutes

### What Worked Well
- Detection: [How we found the issue]
- Response: [How quickly we acted]
- Recovery: [How fast we rolled back]

### What Didn't Work
- Gaps in testing: [What we missed]
- Monitoring gaps: [Alerts that should have fired]
- Process issues: [What slowed us down]

### Action Items
1. [ ] Fix root cause: [Specific task]
2. [ ] Add tests: [What tests prevent this]
3. [ ] Improve monitoring: [What alerts needed]
4. [ ] Update runbook: [Procedures to add]
5. [ ] Schedule re-deployment: [When safe to retry]
```

---

## Stage 2: Deployment Strategies

### Risk-Based Staged Deployment

**Philosophy**: Deploy incrementally, monitor at each stage, rollback at first sign of trouble.

### Risk Categorization

**Categorize ALL changes by risk level:**

#### ZERO-RISK Changes
**Definition:** Cannot possibly break production

**Examples:**
- Test files (unit, integration, E2E)
- Documentation (README, code comments)
- Code with feature flags OFF
- Internal tooling updates

**Deployment:**
- Deploy immediately
- No waiting period
- No special monitoring (changes are dormant)

---

#### LOW-RISK Changes
**Definition:** New code not yet integrated into main flow

**Examples:**
- New files not yet imported
- Utility functions not yet called
- Database tables not yet used
- Read-only operations

**Deployment:**
- Deploy with feature flag OFF
- Wait: 1 hour
- Monitor: No errors from new code paths (should be silent)

---

#### MEDIUM-RISK Changes
**Definition:** Changes to existing functionality, integration with existing systems

**Examples:**
- Middleware changes
- API route modifications
- Database migrations (backward compatible)
- Configuration changes
- Dependency updates

**Deployment:**
- Canary: 10% of users
- Wait: 2-4 hours
- Monitor: Error rate, latency, success rate
- Partial: 50% of users
- Wait: 4-8 hours
- Full: 100%

---

#### HIGH-RISK Changes
**Definition:** Security-critical, affects all users, data integrity

**Examples:**
- Authentication changes
- Payment processing
- Data writes/updates
- Database migrations (breaking changes)
- External API integrations

**Deployment:**
- Extended canary: 1-5% of users
- Wait: 8-24 hours
- Multiple partial stages: 10% → 25% → 50% → 75% → 100%
- Each stage: 4-8 hours wait
- Intensive monitoring at every stage

---

### The 5-Stage Deployment Sequence

#### Stage 1: Infrastructure (ZERO-RISK)

**Deploy:**
- All tests
- All documentation
- All code with feature flags OFF

**Wait:** 0 hours (proceed immediately to Stage 2)

**Monitor:**
- Deployment success (CI/CD pipeline)
- Application starts correctly
- No new errors in logs (code is dormant)

**Success Criteria:**
- Build succeeds
- Application healthy
- No errors from new code (shouldn't be active)

**Rollback:** Not needed (code not active, but can use Level 1 if issues)

---

#### Stage 2: Integration (LOW-RISK)

**Deploy:**
- All code deployed
- Feature flag still OFF
- New files/modules now on production (but unused)

**Wait:** 1 hour

**Monitor:**
- Memory/CPU usage (should be stable)
- No errors from new modules (should be unloaded)
- Application stability

**Success Criteria:**
- No increase in error rate
- No memory leaks (check after 1 hour)
- All existing functionality working

**Rollback:** Level 1 (disable feature flag) - though already off

---

#### Stage 3: Canary (MEDIUM-RISK)

**Deploy:**
- Enable feature flag for 10% of users
- Route via load balancer, user ID hash, or feature flag service

**Configuration:**
```javascript
// Feature flag configuration
if (hashUserId(user.id) % 10 === 0) {
  // 10% of users get new feature
  enableFeature('new-auth-flow');
}
```

**Wait:** 2-4 hours (minimum)

**Monitor (Real-Time Dashboard):**

| Metric | Baseline | Target | Warning | Critical |
|--------|----------|--------|---------|----------|
| Error Rate | 0.05% | <0.1% | >0.15% | >0.5% |
| Latency p95 | 150ms | <200ms | >300ms | >500ms |
| Success Rate | 99.95% | >99.9% | <99.8% | <99.5% |
| Custom Metrics | - | - | - | - |

**Custom Metrics to Track:**
- Feature-specific metrics (e.g., JWT tokens issued)
- Database query performance
- Cache hit rates
- External API call rates

**Success Criteria (ALL must pass):**
- No critical alerts for 2 hours minimum
- Error rate stable or decreased
- Latency within 10% of baseline
- Zero security incidents
- No increase in user complaints

**Rollback Triggers:**
- ANY critical alert
- 3+ warnings in 30 minutes
- Sustained degradation (>10 min)
- User complaints about new feature

**If rollback:** Execute Level 1 (feature flag to false) immediately

---

#### Stage 4: Partial (MEDIUM-RISK)

**Deploy:**
- Enable feature for 50% of users

**Wait:** 4-8 hours (include overnight period if possible)

**Monitor:** Same metrics as Stage 3, at scale

**Additional Checks:**
- Database connection pool (should not increase significantly)
- Cache performance (should improve or stay stable)
- Load balancer distribution (should be even)

**Success Criteria:**
- Metrics stable at 50% scale
- No degradation compared to 10% canary
- Database and cache performing well
- No increased operational load

**Rollback:** Level 1 if any metrics degrade

---

#### Stage 5: Full Rollout (HIGH-RISK → FINAL)

**Deploy:**
- Enable feature for 100% of users
- Remove canary infrastructure (optional, can keep flag for safety)

**Wait:** 24 hours continuous monitoring

**Monitor:** Full production metrics

**Expected at 100%:**
- Metrics should scale linearly from 50%
- No surprises (any issues should have appeared in canary)
- System stable under full load

**Post-Deployment Actions (after 24 hours stable):**

1. **Document learnings**
   - What went well
   - What was surprising
   - Metrics to watch next time

2. **Update runbook**
   - Add operational procedures
   - Document common issues
   - Update troubleshooting guide

3. **Remove feature flag** (after 1 week stable)
   - Clean up flag code
   - Remove conditional logic
   - Simplify codebase

4. **Celebrate!** 🎉
   - Feature shipped successfully
   - Team learned from the process
   - Production is stable

**Success:** Feature stable for 1 week → Mark as complete, remove from monitoring

---

### Monitoring Dashboard Setup

**Required Dashboards:**

1. **Error Rate Dashboard**
   - URL: `/dashboard/errors?filter=feature-name`
   - Metrics: Total errors, error rate %, top error messages
   - Alerts: >0.2% warning, >0.5% critical

2. **Latency Dashboard**
   - URL: `/dashboard/performance?service=service-name`
   - Metrics: p50, p95, p99 latency
   - Alerts: p95 >300ms warning, >500ms critical

3. **Success Rate Dashboard**
   - URL: `/dashboard/success?endpoint=/api/*`
   - Metrics: 2xx rate, 4xx rate, 5xx rate
   - Alerts: 5xx >0.5% critical

4. **Custom Metrics Dashboard**
   - URL: `/dashboard/custom?feature=feature-name`
   - Metrics: Feature-specific (e.g., tokens issued, logins/hour)
   - Alerts: Custom thresholds

**Alert Routing:**
- Warnings → #alerts channel (reviewed periodically)
- Critical → PagerDuty/on-call (immediate response)
- Security → Separate security channel + incident response team

---

### Deployment Checklist

**Pre-Deployment:**
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code review complete
- [ ] Security review complete (if high-risk)
- [ ] Rollback strategy documented
- [ ] Monitoring dashboards configured
- [ ] Feature flags configured
- [ ] On-call engineer assigned
- [ ] Stakeholders notified of deployment schedule
- [ ] Deployment window confirmed (avoid Fridays, weekends, holidays)

**During Deployment:**
- [ ] Start deployment (CI/CD pipeline)
- [ ] Monitor pipeline progress
- [ ] Verify Stage 1 (infrastructure) succeeds
- [ ] Wait 1 hour, monitor Stage 2 (integration)
- [ ] Enable 10% canary (Stage 3)
- [ ] Monitor for 2-4 hours, check all metrics
- [ ] Decision: Proceed to 50% or rollback?
- [ ] If proceeding: Enable 50% (Stage 4)
- [ ] Monitor for 4-8 hours
- [ ] Decision: Proceed to 100% or rollback?
- [ ] If proceeding: Enable 100% (Stage 5)
- [ ] Monitor for 24 hours

**Post-Deployment:**
- [ ] All metrics within acceptable ranges
- [ ] No critical alerts for 24 hours
- [ ] User feedback reviewed (support tickets, social media)
- [ ] Deployment marked as successful
- [ ] Postmortem scheduled (even for successful deploys!)
- [ ] Runbook updated with learnings
- [ ] Feature flag removal scheduled (1 week later)

---

## Deployment Timing

### Best Times to Deploy

**Optimal Windows:**
- **Tuesday-Thursday, 10am-2pm** (best)
- **Monday, 11am-2pm** (acceptable)

**Why:**
- Team is available for monitoring
- Issues can be addressed same day
- Avoid weekend/overnight incidents
- Post-lunch alertness (avoid morning groggy)

### Times to AVOID

**Never Deploy:**
- **Fridays after 12pm** - Risk weekend incidents
- **Before major holidays** - Team unavailable
- **During peak traffic** - Increased blast radius
- **After 4pm** - Team going home soon
- **During on-call transition** - Handoff confusion

**Emergency Exception:**
- Security hotfix: Deploy ASAP (any time)
- Critical production bug fix: Deploy ASAP
- All other changes: Wait for proper window

---

## Rollback-Ready Deployments

**Design every deployment to be easily reversible:**

1. **Feature Flags**
   - Every new feature behind a flag
   - Can toggle off instantly

2. **Backward-Compatible Database Migrations**
   - Add columns, don't remove
   - New tables, don't modify existing
   - Can rollback code without DB rollback

3. **Blue-Green Deployments** (Infrastructure)
   - Keep previous version running
   - Switch traffic atomically
   - Instant rollback to previous version

4. **Canary Deployments** (Traffic)
   - Route small percentage to new version
   - Instant rollback via routing change

---

## Invocation Methods

### Method 1: Explicit Invocation by Sub-Agents (Primary)

**How it works:**
- Commands invoke sub-agents (e.g., `devops-planner`)
- Sub-agents explicitly invoke this skill with stage parameter
- Progressive loading: Only loads specified stage

**Example:**
```
# In devops-planner sub-agent:
Invoke Skill: "cc10x:deployment-patterns"
Stage: "Stage 1: Rollback Strategies"
Loads: Rollback stage only
```

**Benefits:**
- Loads only what's needed
- Provides structure at right moment

### Method 2: Manual Invocation by User

**How it works:**
- User explicitly asks: "Use deployment-patterns skill to create rollback plan"
- Useful when working outside command workflows

**Example:**
```
User: "Use deployment-patterns skill to create rollback plan for auth changes"
```

### Method 3: Auto-Trigger (NOT WORKING)

**Status:** ⚠️ Skills don't currently auto-trigger in Claude Code

**Evidence:**
- Trigger phrases listed for future compatibility
- Extensive testing shows 0% auto-trigger rate
- Don't rely on auto-triggering

**Workaround:** Use commands (they explicitly invoke skills) or manual invocation

---

## Summary

**Stage 1: Rollback Strategies** provides:
- 3-level escalation model (flag → config → code)
- < 5 minute recovery target
- Clear rollback triggers
- Post-rollback procedures

**Stage 2: Deployment Strategies** provides:
- Risk-based categorization
- 5-stage deployment sequence
- Monitoring dashboard setup
- Deployment timing guidance

**Use this skill when:**
- Planning production deployments
- Need rollback procedures
- Designing staged rollouts
- Preparing for disaster recovery

**Progressive loading:**
- Stage 1: Rollback strategies
- Stage 2: Deployment strategies
- Load only what you need
