---
name: security-patterns
description: Identifies OWASP Top 10 vulnerabilities including SQL injection, XSS, authentication bypasses, insecure direct object references, CSRF, broken access control, and security misconfigurations. Use when analyzing code for security vulnerabilities, reviewing authentication and authorization logic, auditing input validation and output encoding, checking for injection attacks, or ensuring secure coding practices. Progressive loading: Stage 1 (metadata), Stage 2 (QUICK-REFERENCE.md), Stage 3 (DETAILED-GUIDE.md).
license: MIT
---

# Security Patterns - Stage 1: Metadata

## Skill Overview

**Name**: Security Patterns
**Purpose**: Identify security vulnerabilities and ensure secure coding practices
**When to Use**: Security analysis, code review, vulnerability scanning, auth implementation
**Core Rule**: Assume all input is malicious until validated

---

## Available Sections

### Stage 2: Quick Reference (~500 tokens)
**File**: `QUICK-REFERENCE.md`

Contains:
- OWASP Top 10 quick check
- Critical security patterns
- Red flags to search for
- Common mistakes
- Quick audit checklist

**Load when**: Security analysis is needed

### Stage 3: Detailed Guide (~3000 tokens)
**File**: `DETAILED-GUIDE.md`

Contains:
- A01: Broken Access Control (RBAC, ABAC)
- A02: Cryptographic Failures (hashing, encryption, TLS)
- A03: Injection (SQL, NoSQL, command, XSS)
- A07: Authentication Failures (MFA, sessions, JWT)
- Security headers
- Rate limiting

**Load when**: Implementing security-critical features

---

## Quick Facts

| Aspect | Details |
|--------|---------|
| **OWASP Top 10** | A01-A10 covered |
| **Key Focus** | Input validation, auth, secrets |
| **Common Mistakes** | Plain text passwords, no validation, hardcoded secrets |
| **Red Flags** | eval, exec, innerHTML, hardcoded secrets |
| **Best Practice** | Assume all input is malicious |

---

## When to Load Each Stage

**Stage 1 (Metadata)**: Always loaded at workflow start
- Shared context in REVIEW workflow
- Shared context in BUILD workflow

**Stage 2 (Quick Reference)**: Load when security analysis needed
- Subagent analysis-risk-security (REVIEW)
- Subagent code-reviewer (BUILD, DEBUG)

**Stage 3 (Detailed Guide)**: Load on-demand for implementation
- When implementing authentication
- When handling payment processing
- When storing sensitive data
- When building public APIs

---

## Token Economics

| Stage | Tokens | When |
|-------|--------|------|
| Stage 1 | ~50 | Always |
| Stage 2 | ~500 | On demand |
| Stage 3 | ~3000 | On demand |
| **Total** | **~3550** | **All stages** |

**Savings**: 30-50% by loading only needed stages

---

## Next Steps

1. Load `QUICK-REFERENCE.md` for security analysis
2. Load `DETAILED-GUIDE.md` for implementation details
3. Use red flags checklist for code scanning
4. Reference OWASP Top 10 for vulnerability mapping

---

**See QUICK-REFERENCE.md for Stage 2 content**
**See DETAILED-GUIDE.md for Stage 3 content**
