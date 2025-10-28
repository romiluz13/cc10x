---
name: security-patterns
description: Identifies OWASP Top 10 vulnerabilities including SQL injection, XSS, authentication bypasses, insecure direct object references, CSRF, broken access control, and security misconfigurations. Use when analyzing code for security vulnerabilities, reviewing authentication and authorization logic, auditing input validation and output encoding, checking for injection attacks, or ensuring secure coding practices.
license: MIT
---

# Security Patterns - Stage 1: Metadata

## Skill Overview

**Name**: Security Patterns
**Purpose**: Identify security vulnerabilities and ensure secure coding practices
**When to Use**: Security analysis, code review, vulnerability scanning, auth implementation
**Core Rule**: Assume all input is malicious until validated

---

## Security Coverage

**OWASP Top 10 Vulnerabilities**:
- A01: Broken Access Control (RBAC, ABAC)
- A02: Cryptographic Failures (hashing, encryption, TLS)
- A03: Injection (SQL, NoSQL, command, XSS)
- A07: Authentication Failures (MFA, sessions, JWT)
- Security headers
- Rate limiting

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

## When to Use

**Always loaded at workflow start**:
- Shared context in REVIEW workflow
- Shared context in BUILD workflow

**Use when**:
- Implementing authentication
- Handling payment processing
- Storing sensitive data
- Building public APIs
- Analyzing code for vulnerabilities
