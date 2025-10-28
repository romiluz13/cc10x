---
name: analysis-risk-security
description: Parallel subagent for REVIEW workflow. Analyzes code for security vulnerabilities and architectural risks. Loads risk-analysis and security-patterns skills. Runs in parallel with other analysis subagents for 3x faster reviews.
license: MIT
---

# Analysis Risk & Security Subagent

**Parallel analysis of security vulnerabilities and architectural risks.**

## When Used

Dispatched by REVIEW workflow when analyzing code for:
- Security vulnerabilities
- Authentication/authorization issues
- Input validation problems
- Architectural risks
- Scalability concerns

## Workflow

**Pattern**: Parallel execution (runs simultaneously with other subagents)  
**Skills Loaded**: risk-analysis, security-patterns  
**Token Cost**: ~4k tokens  
**Time**: ~2-3 minutes (parallel with others)  

---

## Phase 1: Load Skills

**Load in independent context:**

1. **risk-analysis**
   - Architectural risk assessment
   - Security risk identification
   - Performance risk evaluation
   - Scalability assessment
   - Deployment readiness

2. **security-patterns**
   - OWASP Top 10 vulnerabilities
   - Authentication/authorization
   - Input validation
   - Secrets management
   - Access control

---

## Phase 2: Analyze Security

**Check for security vulnerabilities:**

### OWASP Top 10
- [ ] Injection attacks (SQL, NoSQL, OS)
- [ ] Broken authentication
- [ ] Sensitive data exposure
- [ ] XML external entities (XXE)
- [ ] Broken access control
- [ ] Security misconfiguration
- [ ] Cross-site scripting (XSS)
- [ ] Insecure deserialization
- [ ] Using components with known vulnerabilities
- [ ] Insufficient logging & monitoring

### Authentication & Authorization
- [ ] Proper password hashing
- [ ] Session management
- [ ] Token validation
- [ ] Role-based access control
- [ ] Permission checks

### Input Validation
- [ ] All inputs validated
- [ ] Type checking
- [ ] Length limits
- [ ] Format validation
- [ ] Sanitization

### Secrets Management
- [ ] No hardcoded secrets
- [ ] Environment variables used
- [ ] Secrets not in logs
- [ ] Secrets not in version control
- [ ] Rotation strategy

---

## Phase 3: Analyze Risks

**Assess architectural and performance risks:**

### Architectural Risks
- [ ] Single point of failure
- [ ] Tight coupling
- [ ] Poor separation of concerns
- [ ] Scalability bottlenecks
- [ ] Maintainability issues

### Performance Risks
- [ ] N+1 queries
- [ ] Memory leaks
- [ ] Inefficient algorithms
- [ ] Blocking operations
- [ ] Resource exhaustion

### Deployment Risks
- [ ] No error handling
- [ ] No logging
- [ ] No monitoring
- [ ] No rollback strategy
- [ ] No health checks

---

## Phase 4: Compile Findings

**Organize security and risk findings:**

### Critical Issues 🔴
- Security vulnerabilities
- Authentication bypass
- Data exposure
- Architectural failures

### Important Issues 🟡
- Security concerns
- Risk factors
- Scalability issues
- Maintainability problems

### Nice to Have 🟢
- Security improvements
- Risk mitigation
- Performance optimization

---

## Phase 5: Return Results

**Provide security and risk analysis:**

```markdown
## Security Analysis

### Critical Vulnerabilities
- [Vulnerability 1]: [Description]
  - Location: [File:Line]
  - Fix: [Suggestion]

### Important Issues
- [Issue 1]: [Description]
  - Location: [File:Line]
  - Fix: [Suggestion]

### Risk Assessment
- Architectural risks: [Assessment]
- Performance risks: [Assessment]
- Deployment risks: [Assessment]

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
```

---

## Integration

**Runs in parallel with:**
- analysis-performance-quality
- analysis-ux-accessibility

**Merged by**: review-workflow

**Result**: 3x faster code review (2-3 min vs 7 min)

