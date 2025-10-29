---
name: integration-patterns
description: Focused integration design and reliability guidance. Thin wrapper around the Integration section of design-patterns with a compact checklist and examples. Used by integration-verifier, planning-workflow, and debug workflows when integrations fail.
---

# Integration Patterns (Focused)

## Progressive Loading Stages

### Stage 1: Metadata
- Purpose: Make integrations reliable, observable, and resilient
- When: Designing or verifying service/service or service/third-party interactions
- Core Rule: Integrations fail; design for failure and recovery

---

### Stage 2: Quick Reference

#### Integration Checklist
```
Reliability
- [ ] Timeouts set (client + server)
- [ ] Retries with exponential backoff and jitter
- [ ] Idempotency keys for retryable operations
- [ ] Circuit breaker around downstream dependencies

Resilience & Consistency
- [ ] Dead-letter queue or compensating actions
- [ ] Outbox/inbox where needed (avoid dual writes)
- [ ] Event/version compatibility; schema evolution plan

Observability & Ops
- [ ] Correlated logs/trace IDs
- [ ] Dashboards and alerts for SLOs
- [ ] Runbooks for common failures
```

#### Examples
**Exponential Backoff (TS pseudo)**
```ts
for (let i = 0; i < max; i++) {
  const delay = Math.min(base * 2 ** i + jitter(), cap);
  try { return await call(); } catch (e) { await sleep(delay); }
}
throw new Error('exhausted retries');
```

**Circuit Breaker Settings**
- Failure threshold, half-open probe, cooldown window

---

### Stage 3: Verification Procedure
1) Simulate timeouts and verify retry/backoff/circuit breaker behavior
2) Verify idempotency on repeated calls
3) Check logs/traces contain correlation IDs and diagnoses
4) Validate DLQ/outbox handling and runbooks

---

### Stage 4: Outputs
- Integration Verification Checklist with results and logs
- Incidents and runbook gaps captured

---

### Stage 5: Links
- See also: design-patterns (Integration section), log-analysis-patterns, systematic-debugging, risk-analysis

