# Error Handling & Fallback Strategies Guide

## Overview

Error handling and fallback strategies ensure workflows continue operating even when subagents fail or skills are unavailable.

---

## Error Handling Patterns

### Pattern 1: Subagent Failure → Sequential Fallback

**When**: A subagent fails or times out

**Fallback Strategy**:
```
Parallel Execution (3 subagents):
  ├─ Subagent 1: ✅ Success
  ├─ Subagent 2: ❌ FAILED
  └─ Subagent 3: ✅ Success

Fallback to Sequential:
  ├─ Subagent 2 (retry): ✅ Success (on retry)
  └─ Continue with results
```

**Implementation**:
```typescript
async function executeWithFallback(subagents) {
  try {
    // Try parallel execution
    const results = await Promise.all(subagents.map(s => s.execute()));
    return results;
  } catch (error) {
    // Fallback to sequential
    const results = [];
    for (const subagent of subagents) {
      try {
        results.push(await subagent.execute());
      } catch (err) {
        results.push(await subagent.executeWithRetry());
      }
    }
    return results;
  }
}
```

**Benefits**:
- ✅ Continues execution even if one subagent fails
- ✅ Retries failed subagents
- ✅ Maintains quality
- ✅ Slower but reliable

---

### Pattern 2: Skill Failure → Cached Version

**When**: A skill fails to load or execute

**Fallback Strategy**:
```
Load Skill:
  ├─ Primary: ❌ FAILED
  ├─ Fallback to Cache: ✅ Success
  └─ Use cached version
```

**Implementation**:
```typescript
async function loadSkillWithFallback(skillName) {
  try {
    // Try to load skill
    return await loadSkill(skillName);
  } catch (error) {
    // Fallback to cached version
    const cached = await getCachedSkill(skillName);
    if (cached) {
      return cached;
    }
    // If no cache, use minimal version
    return getMinimalSkill(skillName);
  }
}
```

**Benefits**:
- ✅ Continues execution even if skill unavailable
- ✅ Uses cached version (may be slightly outdated)
- ✅ Maintains workflow continuity
- ✅ Graceful degradation

---

### Pattern 3: Timeout Handling

**When**: A subagent or skill takes too long

**Fallback Strategy**:
```
Execute with Timeout:
  ├─ Start execution
  ├─ Wait 5 minutes
  ├─ Timeout reached: ⏱️ TIMEOUT
  └─ Use partial results or fallback
```

**Implementation**:
```typescript
async function executeWithTimeout(fn, timeoutMs = 300000) {
  return Promise.race([
    fn(),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeoutMs)
    )
  ]).catch(error => {
    if (error.message === 'Timeout') {
      return getPartialResults();
    }
    throw error;
  });
}
```

**Benefits**:
- ✅ Prevents infinite waits
- ✅ Returns partial results
- ✅ Maintains responsiveness
- ✅ Prevents resource exhaustion

---

### Pattern 4: Graceful Degradation

**When**: Multiple failures occur

**Fallback Strategy**:
```
Full Workflow:
  ├─ Parallel subagents: ❌ FAILED
  ├─ Sequential fallback: ❌ FAILED
  └─ Minimal workflow: ✅ Success (degraded)

Minimal Workflow:
  ├─ Load core skills only
  ├─ Skip optional analysis
  └─ Return basic results
```

**Implementation**:
```typescript
async function executeWithDegradation(workflow) {
  try {
    // Try full workflow
    return await workflow.executeFull();
  } catch (error) {
    try {
      // Try degraded workflow
      return await workflow.executeDegraded();
    } catch (error) {
      // Return minimal results
      return workflow.executeMinimal();
    }
  }
}
```

**Benefits**:
- ✅ Always returns some result
- ✅ Graceful quality degradation
- ✅ Better than complete failure
- ✅ Maintains user experience

---

## Error Recovery Strategies

### Strategy 1: Automatic Retry

```typescript
async function executeWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      // Exponential backoff: 1s, 2s, 4s
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

**When to use**:
- Transient failures (network, temporary unavailability)
- Exponential backoff prevents overwhelming system

---

### Strategy 2: Circuit Breaker

```typescript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failures = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit breaker is OPEN');
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      setTimeout(() => {
        this.state = 'HALF_OPEN';
      }, this.timeout);
    }
  }
}
```

**When to use**:
- Prevent cascading failures
- Stop calling failing services
- Allow time for recovery

---

### Strategy 3: Fallback Chain

```typescript
async function executeWithFallbackChain(strategies) {
  for (const strategy of strategies) {
    try {
      return await strategy.execute();
    } catch (error) {
      // Try next strategy
      continue;
    }
  }
  throw new Error('All strategies failed');
}

// Usage
const result = await executeWithFallbackChain([
  { execute: () => loadSkillFromPrimary() },
  { execute: () => loadSkillFromCache() },
  { execute: () => loadSkillFromMinimal() }
]);
```

**When to use**:
- Multiple fallback options available
- Try each in order until one succeeds

---

## Error Handling in Workflows

### REVIEW Workflow Error Handling

```markdown
## Error Handling

**If Subagent Fails**:
1. Retry failed subagent (up to 3 times)
2. If still fails, use sequential analysis
3. If sequential fails, use cached results
4. Return partial review with available results

**If Skill Fails**:
1. Try to load from cache
2. If no cache, use minimal skill
3. Continue with available skills
4. Note missing analysis in results
```

### BUILD Workflow Error Handling

```markdown
## Error Handling

**If Component Builder Fails**:
1. Retry component building (up to 3 times)
2. If still fails, build components sequentially
3. If sequential fails, use template components
4. Continue with available components

**If Code Reviewer Fails**:
1. Retry code review (up to 3 times)
2. If still fails, skip review
3. Continue with integration verification
4. Note missing review in results
```

### DEBUG Workflow Error Handling

```markdown
## Error Handling

**If Bug Investigation Fails**:
1. Retry investigation (up to 3 times)
2. If still fails, use manual debugging approach
3. If manual fails, escalate to human
4. Return investigation notes

**If Fix Verification Fails**:
1. Retry verification (up to 3 times)
2. If still fails, use basic testing
3. If basic fails, mark as unverified
4. Return fix with verification notes
```

---

## Monitoring & Alerting

### Error Metrics to Track

```
- Subagent failure rate (target: < 1%)
- Skill failure rate (target: < 0.5%)
- Timeout rate (target: < 0.1%)
- Fallback usage rate (target: < 5%)
- Recovery success rate (target: > 95%)
```

### Alert Conditions

```
- Subagent failure rate > 5%
- Skill failure rate > 2%
- Timeout rate > 1%
- Fallback usage rate > 20%
- Recovery success rate < 80%
```

---

## Implementation Checklist

- [ ] Add retry logic to all subagents
- [ ] Add timeout handling to all workflows
- [ ] Implement circuit breaker for skills
- [ ] Add fallback chain for skill loading
- [ ] Add graceful degradation to workflows
- [ ] Add error logging and monitoring
- [ ] Add error metrics tracking
- [ ] Add alert conditions
- [ ] Test all error scenarios
- [ ] Document error handling in user guide

---

## Benefits

✅ **Improved reliability** (continues on failures)
✅ **Better UX** (graceful degradation)
✅ **Faster recovery** (automatic retries)
✅ **Prevents cascades** (circuit breaker)
✅ **Maintains quality** (fallback strategies)
✅ **Better monitoring** (error metrics)

---

**Status**: Ready for implementation
**Confidence**: Very High
**Timeline**: 1 day for full implementation

