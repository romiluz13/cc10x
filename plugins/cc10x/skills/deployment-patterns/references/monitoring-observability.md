# Monitoring & Observability - Functionality-Focused

**Reference**: Part of `deployment-patterns` skill. See main SKILL.md for overview.

## Strategy: Monitoring Setup (Based on Functionality Metrics)

**CRITICAL**: Monitor functionality metrics aligned with flows, not generic metrics.

## Functionality Metrics (Aligned with Flows)

**Example: File Upload to CRM**

### User Flow Metrics

- Upload success rate (core functionality)
- Upload latency (functionality performance)
- Upload error rate (functionality errors)

### System Flow Metrics

- File storage success rate (system functionality)
- File storage latency (system performance)
- Database write success rate (data persistence)

### Integration Flow Metrics

- CRM API success rate (integration functionality)
- CRM API latency (integration performance)
- CRM API error rate (integration errors)

## Monitoring Setup

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

## Functionality-Focused Monitoring

**Key Principle**: Monitor metrics that directly reflect functionality health, not generic system metrics.

**Example Mapping**:

- User Flow → Upload success rate, upload latency
- System Flow → Storage success rate, database write success rate
- Integration Flow → CRM API success rate, CRM API latency

**Focus**: Track functionality metrics, not generic metrics like CPU usage or memory (unless they directly affect functionality).

## Alert Configuration

### Critical Alerts (Immediate Action)

**Functionality Broken**:

- Success rate < 50%
- Error rate > 50%
- Data loss or corruption

**Action**: Immediate rollback (Level 1: Feature Flag).

### Warning Alerts (Investigate)

**Functionality Degraded**:

- Success rate < 95%
- Latency > threshold
- Error rate > 10%

**Action**: Investigate, determine root cause, consider rollback.

### Info Alerts (Monitor)

**Functionality Suboptimal**:

- Success rate 95-99%
- Latency slightly elevated
- Occasional errors

**Action**: Monitor, optimize if needed.

## Rollback Triggers Based on Metrics

**Immediate Rollback** (No Discussion):

- Upload success rate < 50%
- Upload error rate > 50%
- CRM API integration fails > 50%
- File storage fails > 50%
- Data loss or corruption

**Evaluate Within 15 Minutes**:

- Upload success rate < 95%
- Upload latency > 30s
- CRM API integration fails > 10%
- File storage fails > 10%
- 10+ user reports

**Monitor But Don't Rollback**:

- Upload success rate 95-99%
- Upload latency 10-30s
- Single user report
- Non-critical issues

## Health Checks

**Functionality Health Checks** (not just service health):

```bash
# Health check that verifies functionality
curl https://api.example.com/health/functionality/upload
# Expected: {
#   "status": "healthy",
#   "success_rate": 98,
#   "latency_p95": 25,
#   "errors": 0
# }
```

**Focus**: Check if functionality works, not just if service is up.

## Monitoring Best Practices

- **Monitor functionality metrics**: Track success rate, latency, error rate
- **Set appropriate thresholds**: Based on functionality requirements, not generic thresholds
- **Alert on functionality issues**: Alert when functionality breaks, not just when system metrics spike
- **Track trends**: Monitor functionality trends over time
- **Correlate metrics**: Understand relationships between metrics (e.g., latency affects success rate)

## Observability Setup

**Logs**: Log functionality events (upload started, upload completed, upload failed)
**Metrics**: Track functionality metrics (success rate, latency, error rate)
**Traces**: Trace functionality flows (User Flow → System Flow → Integration Flow)

**Focus**: Observability that helps understand functionality, not just system internals.

## Dashboard Configuration

**Functionality Dashboard**:

- User Flow metrics (success rate, latency, errors)
- System Flow metrics (storage, database)
- Integration Flow metrics (CRM API, external services)
- Alert status (critical, warning, info)

**Focus**: Dashboard that shows functionality health, not just system health.

---

**See Also**: `references/rollback-strategies.md` for rollback guidance, `references/staged-deployment.md` for staged rollout patterns.
