---
name: 8-dimensions
description: Comprehensive risk analysis using 8 dimensions - Security, Performance, Quality, UX, Accessibility, Testing, Deployment, Maintainability. Use when analyzing risks or planning features.
allowed-tools: Read, Grep
---

# 8 Dimensions Risk Analysis

Systematic framework for identifying risks across all critical dimensions.

## When to Use
- Feature planning
- Architecture reviews
- Pre-deployment checks
- Risk assessments

## The 8 Dimensions

### 1. Security
**What Could Go Wrong?**
- Authentication/authorization bypass
- Data exposure or leakage
- Injection vulnerabilities (SQL, XSS, Command)
- Insecure dependencies
- Secret exposure in code/logs

**Quick Checks:**
```bash
# Check for secrets
grep -r "password\|api_key\|secret" --exclude-dir=node_modules

# Check dependencies
npm audit || pip-audit
```

### 2. Performance
**What Could Go Wrong?**
- Slow response times (> 200ms)
- Memory leaks
- N+1 queries
- Large bundle sizes
- Blocking operations

**Quick Checks:**
- Database queries: Look for loops with DB calls
- Bundle size: Check import sizes
- Algorithms: O(n²) or worse?

### 3. Quality
**What Could Go Wrong?**
- High complexity (> 10 cyclomatic)
- Code duplication
- Missing error handling
- Poor naming/organization
- Technical debt accumulation

**Quick Checks:**
- Functions > 50 lines?
- Try/catch present?
- Clear variable names?

### 4. UX (User Experience)
**What Could Go Wrong?**
- Confusing user flows
- Missing loading states
- Poor error messages
- Slow perceived performance
- Mobile usability issues

**Quick Checks:**
- Error messages clear and actionable?
- Loading indicators present?
- Mobile-responsive design?

### 5. Accessibility
**What Could Go Wrong?**
- Keyboard navigation broken
- Screen reader incompatible
- Low color contrast
- Missing ARIA labels
- Non-semantic HTML

**Quick Checks:**
- Tab through UI - everything accessible?
- Alt text on images?
- Color contrast ratio >= 4.5:1?

### 6. Testing
**What Could Go Wrong?**
- Insufficient test coverage (< 80%)
- Missing edge case tests
- Flaky tests
- No integration tests
- Untestable code

**Quick Checks:**
- Test coverage report
- Edge cases in tests?
- Tests deterministic?

### 7. Deployment
**What Could Go Wrong?**
- Breaking changes without migration
- Missing environment variables
- Database migration failures
- Rollback difficulties
- Zero-downtime deployment issues

**Quick Checks:**
- Breaking API changes?
- New env vars documented?
- Migration scripts tested?

### 8. Maintainability
**What Could Go Wrong?**
- Future developers can't understand code
- Tight coupling
- No documentation
- Hard to modify
- Knowledge silos

**Quick Checks:**
- README up to date?
- Complex logic commented?
- Modular architecture?

## Risk Scoring

For each dimension, rate: **Low (1) | Medium (2) | High (3) | Critical (4)**

```markdown
| Dimension       | Risk | Notes                    |
|-----------------|------|--------------------------|
| Security        | 3    | Missing input validation |
| Performance     | 2    | N+1 query in users list  |
| Quality         | 1    | Good test coverage       |
| UX              | 2    | Loading state missing    |
| Accessibility   | 3    | No keyboard nav          |
| Testing         | 2    | 75% coverage             |
| Deployment      | 1    | Standard process         |
| Maintainability | 2    | Needs more docs          |
```

**Total Risk Score**: Sum / 32 × 100 = **X%**

## Action Matrix

- **Critical (4)**: BLOCK deployment, fix immediately
- **High (3)**: Must fix before next release
- **Medium (2)**: Should fix, schedule soon
- **Low (1)**: Monitor, fix if time permits

## Example Analysis

```markdown
# Risk Analysis: User Authentication Feature

## 1. Security ⚠️ HIGH (3)
- **Risk**: Password storage without hashing
- **Impact**: User accounts compromised if DB leaked
- **Mitigation**: Use bcrypt with salt rounds >= 10

## 2. Performance ✅ LOW (1)
- **Risk**: Login query is indexed and fast
- **Impact**: None

## 3. Quality ⚠️ MEDIUM (2)
- **Risk**: 80-line function, could be split
- **Impact**: Hard to test edge cases
- **Mitigation**: Extract validation logic

... (continue for all 8)

## Overall Risk: 54% (Medium-High)
## Recommendation: Fix Security & Accessibility before deploy
```

## Best Practices

✅ **Do:**
- Analyze ALL 8 dimensions
- Be specific about risks
- Suggest concrete mitigations
- Prioritize by severity

❌ **Don't:**
- Skip dimensions even if they seem fine
- Be vague ("might have issues")
- Just list risks without mitigations
- Overwhelm with low-priority items

## Quick Reference

**Pre-Commit**: Security, Quality, Testing
**Pre-Deploy**: All 8 dimensions
**Architecture Review**: Performance, Maintainability, Quality
**Feature Planning**: UX, Accessibility, All 8
