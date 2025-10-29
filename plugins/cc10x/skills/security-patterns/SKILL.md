---
name: security-patterns
description: Identifies OWASP Top 10 vulnerabilities including SQL injection, XSS, authentication bypasses, insecure direct object references, CSRF, broken access control, and security misconfigurations. Use when analyzing code for security vulnerabilities, reviewing authentication and authorization logic, auditing input validation and output encoding, checking for injection attacks, or ensuring secure coding practices.
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

---

# Stage 2: Quick Reference

## Authentication Decision Framework

### Decision Matrix: JWT vs Sessions vs OAuth

**Use JWT when**:
- Stateless microservices
- Mobile apps (token refresh)
- Cross-domain authentication
- High read:write ratio

**Use Sessions when**:
- Traditional web apps
- Need instant revocation
- Sensitive operations (banking)
- Server-side rendering

**Use OAuth when**:
- Third-party authentication
- API delegation (Google, GitHub)
- Multi-tenant SaaS
- Social login

**Critical JWT Pitfalls**:
```typescript
// INSECURE - No algorithm verification
const decoded = jwt.verify(token, secret);

// SECURE - Explicit algorithm
const decoded = jwt.verify(token, secret, { algorithms: ['HS256'] });
```

## Injection Patterns

### SQL Injection

```typescript
// VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.query(query);
// Attack: email = "' OR '1'='1"

// SECURE - Parameterized queries
const query = 'SELECT * FROM users WHERE email = ?';
db.query(query, [email]);
```

### NoSQL Injection (MongoDB)

```typescript
// VULNERABLE
db.collection('users').findOne({ email: req.body.email });
// Attack: { "email": { "$ne": null } } returns all users

// SECURE - Type validation
const email = String(req.body.email);
if (typeof email !== 'string') throw new Error('Invalid input');
db.collection('users').findOne({ email });
```

### XSS (Cross-Site Scripting)

```typescript
// VULNERABLE
element.innerHTML = userInput;
// Attack: userInput = "<img src=x onerror='alert(1)'>"

// SECURE - Text nodes or sanitization
element.textContent = userInput;
// OR: use DOMPurify for HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Command Injection

```typescript
// VULNERABLE
exec(`convert ${filename} output.png`);
// Attack: filename = "image.jpg; rm -rf /"

// SECURE - Parameterized execution
execFile('convert', [filename, 'output.png']);
```

## Access Control Patterns

### Decision Framework: RBAC vs ABAC

**Role-Based Access Control (RBAC)**:
```typescript
// Use when: Fixed roles, simple permissions
const roles = {
  admin: ['read', 'write', 'delete'],
  editor: ['read', 'write'],
  viewer: ['read']
};

function hasPermission(user, action) {
  return roles[user.role]?.includes(action);
}
```

**Attribute-Based Access Control (ABAC)**:
```typescript
// Use when: Complex conditions, context-aware
function canEdit(user, document) {
  return user.id === document.ownerId
    || user.role === 'admin'
    || (user.department === document.department && user.role === 'manager');
}
```

### Insecure Direct Object References (IDOR)

```typescript
// VULNERABLE
app.get('/api/users/:id', (req, res) => {
  const user = db.users.findById(req.params.id);
  res.json(user); // Any user can access any ID
});

// SECURE - Authorization check
app.get('/api/users/:id', auth, (req, res) => {
  const requestedId = req.params.id;
  if (requestedId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = db.users.findById(requestedId);
  res.json(user);
});
```

## Cryptography Patterns

### Password Hashing

```typescript
// INSECURE
const hash = crypto.createHash('md5').update(password).digest('hex');

// SECURE - Bcrypt with salt
import bcrypt from 'bcrypt';
const saltRounds = 12;
const hash = await bcrypt.hash(password, saltRounds);
const isValid = await bcrypt.compare(inputPassword, hash);
```

### Secrets Management

```typescript
// INSECURE
const API_KEY = 'sk_live_abc123def456';

// SECURE - Environment variables
const API_KEY = process.env.STRIPE_API_KEY;
if (!API_KEY) throw new Error('Missing STRIPE_API_KEY');

// SECURE - Secret rotation
async function getSecret(name) {
  const secret = await secretsManager.getSecretValue(name);
  return JSON.parse(secret.SecretString);
}
```

## Security Headers

```typescript
// Express.js security headers
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

## Rate Limiting

```typescript
// Decision: When to rate limit
// - Public APIs: Always
// - Login endpoints: Always (prevent brute force)
// - Password reset: Always
// - File uploads: Always
// - Search: If expensive

import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, try again later'
});

app.post('/api/login', loginLimiter, loginHandler);
```

## Quick Security Checklist

```
Critical Checks (Before any code review):
- [ ] No hardcoded secrets (API keys, passwords)
- [ ] All inputs validated (type, length, format)
- [ ] SQL/NoSQL queries parameterized
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Authentication on protected routes
- [ ] Authorization checks (IDOR prevention)
- [ ] CSRF protection on state-changing requests
- [ ] Security headers configured
- [ ] Rate limiting on public endpoints
- [ ] XSS prevention (escape output)
- [ ] HTTPS enforced
- [ ] Error messages don't leak sensitive info
```

## Red Flags (Grep for these)

```bash
# Hardcoded secrets
grep -r "password.*=.*['\"]" --include="*.ts" --include="*.js"
grep -r "api[_-]?key.*=.*['\"]" --include="*.ts"

# Dangerous functions
grep -r "eval\|exec\|innerHTML\|dangerouslySetInnerHTML" src/

# SQL concatenation
grep -r "SELECT.*\${" --include="*.ts"

# Missing authentication
grep -r "app\.\(get\|post\|put\|delete\)" src/ | grep -v "auth\|Auth"
```
