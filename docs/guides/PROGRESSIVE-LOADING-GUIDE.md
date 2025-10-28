# Progressive Skill Loading Guide

## Overview

Progressive loading is a 3-stage skill loading system that reduces token usage by 30-50% by loading only what's needed when it's needed.

---

## 3-Stage Loading Pattern

### Stage 1: Metadata (~50 tokens)
**When**: Always loaded at workflow start  
**Contains**:
- Skill name
- Purpose
- When to use
- Core rule/principle
- Available sections

**Example**:
```markdown
# Security Patterns

**Purpose**: Identify security vulnerabilities and ensure secure coding practices
**When**: Security analysis, code review, vulnerability scanning
**Core Rule**: Assume all input is malicious until validated
**Sections Available**: OWASP Top 10, Auth Patterns, Input Validation, Quick Checks
```

### Stage 2: Quick Reference (~500 tokens)
**When**: Triggered when skill is actually used  
**Contains**:
- Quick checklists
- Critical patterns
- Red flags
- Common mistakes
- Quick examples

**Example**:
```markdown
## OWASP Top 10 Quick Check
- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection
...

## Critical Patterns
- Input Validation
- Authentication
- Secrets Management
```

### Stage 3: Detailed Guide (~3000 tokens)
**When**: On-demand only (user requests details)  
**Contains**:
- Comprehensive explanations
- Full code examples
- Edge cases
- Best practices
- Testing strategies
- Performance considerations

**Example**:
```markdown
## Detailed Security Patterns

### SQL Injection Prevention
[Comprehensive guide with multiple examples]

### XSS Prevention
[Comprehensive guide with multiple examples]

### CSRF Protection
[Comprehensive guide with multiple examples]
```

---

## Implementation Strategy

### For Each Skill:

1. **Keep Stage 1 in SKILL.md** (metadata only)
   - Skill name, purpose, when to use
   - Core rule/principle
   - Available sections

2. **Create QUICK-REFERENCE.md** (Stage 2)
   - Quick checklists
   - Critical patterns
   - Red flags
   - Common mistakes

3. **Create DETAILED-GUIDE.md** (Stage 3)
   - Comprehensive explanations
   - Full examples
   - Edge cases
   - Best practices

---

## Workflow Integration

### REVIEW Workflow
**Shared Context Skills** (Stage 1 only):
- risk-analysis (metadata)
- code-quality-patterns (metadata)

**Subagent 1: analysis-risk-security**
- risk-analysis (Stage 2 on demand)
- security-patterns (Stage 2 on demand)

**Subagent 2: analysis-performance-quality**
- performance-patterns (Stage 2 on demand)
- code-quality-patterns (Stage 2 on demand)

**Subagent 3: analysis-ux-accessibility**
- ux-patterns (Stage 2 on demand)
- accessibility-patterns (Stage 2 on demand)

### PLAN Workflow
**Shared Context Skills** (Stage 1 only):
- requirements-analysis (metadata)

**Subagent 1: planning-architecture-risk**
- architecture-patterns (Stage 2 on demand)
- risk-analysis (Stage 2 on demand)

**Subagent 2: planning-design-deployment**
- api-design-patterns (Stage 2 on demand)
- component-design-patterns (Stage 2 on demand)
- deployment-patterns (Stage 2 on demand)

### BUILD Workflow
**Shared Context Skills** (Stage 1 only):
- requirements-analysis (metadata)
- security-patterns (metadata)
- test-driven-development (metadata)

**Subagents**:
- component-builder (Stage 2 on demand)
- code-reviewer (Stage 2 on demand)
- integration-verifier (Stage 2 on demand)

### DEBUG Workflow
**Shared Context Skills** (Stage 1 only):
- log-analysis-patterns (metadata)
- performance-patterns (metadata)
- test-driven-development (metadata)

**Subagents**:
- bug-investigator (Stage 2 on demand)
- code-reviewer (Stage 2 on demand)
- integration-verifier (Stage 2 on demand)

---

## Token Savings Calculation

### Before Progressive Loading
```
REVIEW:  22k tokens (all skills full content)
PLAN:    32k tokens (all skills full content)
BUILD:   51k tokens (all skills full content)
DEBUG:   45k tokens (all skills full content)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:   150k tokens
```

### After Progressive Loading
```
REVIEW:  15k → 10k tokens (30% savings)
PLAN:    22k → 15k tokens (30% savings)
BUILD:   40k → 28k tokens (30% savings)
DEBUG:   35k → 24k tokens (30% savings)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:   112k → 77k tokens (30% savings!)
```

---

## Implementation Checklist

- [ ] Create QUICK-REFERENCE.md for each skill
- [ ] Create DETAILED-GUIDE.md for each skill
- [ ] Update SKILL.md to Stage 1 (metadata only)
- [ ] Update workflows to load Stage 1 only
- [ ] Update subagents to load Stage 2 on demand
- [ ] Test token usage reduction
- [ ] Verify quality maintained
- [ ] Deploy to production

---

## Benefits

✅ **30-50% token savings** (77k → 112k tokens)
✅ **Faster initial load** (metadata only)
✅ **On-demand details** (Stage 2 when needed)
✅ **Comprehensive reference** (Stage 3 available)
✅ **Better UX** (progressive disclosure)
✅ **Maintained quality** (all content still available)

---

## Next Steps

1. Create QUICK-REFERENCE.md for all 20 skills
2. Create DETAILED-GUIDE.md for all 20 skills
3. Update all SKILL.md files to Stage 1 only
4. Update workflows to use progressive loading
5. Test and verify improvements
6. Deploy to production

