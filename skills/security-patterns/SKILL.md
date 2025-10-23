---
name: Security Patterns
description: |
  Identifies OWASP Top 10 vulnerabilities, authentication issues, injection attacks, and insecure coding practices. Use when analyzing code for security vulnerabilities and ensuring secure implementation.
  
  Trigger phrases: "security review", "security audit", "check for vulnerabilities", 
  "security scan", "OWASP", "authentication security", "SQL injection", "XSS", 
  "security issues", "secure this code", "security patterns", "vulnerability check",
  "auth security", "security best practices".
  
  Activates on: security analysis, code review for vulnerabilities, authentication implementation,
  input validation review, security audits, pre-production security checks.
progressive: true
---

# Security Patterns

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)
- **Skill**: Security Patterns
- **Purpose**: Identify security vulnerabilities and ensure secure coding practices
- **When**: Security analysis, code review, vulnerability scanning
- **Core Rule**: Assume all input is malicious until validated
- **Sections Available**: OWASP Top 10, Auth Patterns, Input Validation, Quick Checks

---

### Stage 2: Quick Reference (triggered - ~500 tokens)

#### OWASP Top 10 (2021) Quick Check

```
Security Checklist:
- [ ] A01: Broken Access Control (auth checks present?)
- [ ] A02: Cryptographic Failures (secrets exposed? weak crypto?)
- [ ] A03: Injection (SQL, XSS, command injection?)
- [ ] A04: Insecure Design (threat modeling done?)
- [ ] A05: Security Misconfiguration (defaults changed?)
- [ ] A06: Vulnerable Components (npm audit clean?)
- [ ] A07: Auth Failures (weak passwords? no MFA?)
- [ ] A08: Data Integrity Failures (no validation?)
- [ ] A09: Logging Failures (security events logged?)
- [ ] A10: SSRF (user-controlled URLs validated?)
```

#### Critical Security Patterns

**Input Validation** (A03 - Injection):
```typescript
// ❌ NEVER: String concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ ALWAYS: Parameterized queries
const query = `SELECT * FROM users WHERE id = $1`;
const result = await db.query(query, [userId]);
```

**Authentication** (A01, A07):
```typescript
// ❌ NEVER: Missing auth check
app.get('/admin/users', getAllUsers);

// ✅ ALWAYS: Auth + authorization middleware
app.get('/admin/users', authMiddleware, adminMiddleware, getAllUsers);
```

**Secrets** (A02):
```typescript
// ❌ NEVER: Hardcoded secrets
const API_KEY = 'sk_live_abc123';

// ✅ ALWAYS: Environment variables
const API_KEY = process.env.API_KEY;
```

**Password Hashing** (A02, A07):
```typescript
// ❌ NEVER: Weak hashing
crypto.createHash('md5').update(password);

// ✅ ALWAYS: bcrypt/argon2 (10-12 rounds)
await bcrypt.hash(password, 12);
```

#### Red Flags 🚩
```bash
# Search for these patterns:
grep -r "eval\|exec\|innerHTML" src/
grep -r "password.*=.*['\"]" src/
grep -r "SELECT.*FROM.*\${" src/
grep -r "md5\|sha1" src/
```

---

### Stage 3: Detailed Guide (on-demand - ~3000 tokens)

## OWASP Top 10 Detailed

### A01: Broken Access Control

**What**: Users can access resources they shouldn't.

**Examples**:
```typescript
// ❌ Missing authorization check
app.delete('/api/users/:id', async (req, res) => {
  await User.delete(req.params.id);
  // Anyone can delete any user!
});

// ✅ Proper authorization
app.delete('/api/users/:id', authMiddleware, async (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  await User.delete(req.params.id);
});
```

**How to Find**:
- Check all protected routes have auth middleware
- Verify users can only access their own data
- Test with different user roles

### A02: Cryptographic Failures

**What**: Sensitive data exposed or weakly encrypted.

**Examples**:
```typescript
// ❌ Plain text passwords
await db.query('INSERT INTO users (email, password) VALUES ($1, $2)',
  [email, password]);

// ✅ Hashed passwords
const hashedPassword = await bcrypt.hash(password, 12);
await db.query('INSERT INTO users (email, password_hash) VALUES ($1, $2)',
  [email, hashedPassword]);

// ❌ Weak JWT
jwt.sign({ userId }, 'secret123');

// ✅ Strong JWT with expiry
jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '15m' });
```

**How to Find**:
```bash
# Find weak hashing
grep -r "md5\|sha1\|sha256" src/ --include="*.ts"

# Find hardcoded secrets
grep -r "password.*=.*['\"]" src/
grep -r "api[_-]?key.*=.*['\"]" src/
```

### A03: Injection

**What**: Attacker can inject malicious code/queries.

**SQL Injection**:
```typescript
// ❌ String concatenation
const email = req.body.email; // "admin@example.com' OR '1'='1"
const query = `SELECT * FROM users WHERE email = '${email}'`;
// Result: Returns ALL users!

// ✅ Parameterized query
const query = `SELECT * FROM users WHERE email = $1`;
const result = await db.query(query, [email]);
```

**XSS (Cross-Site Scripting)**:
```typescript
// ❌ Unsafe HTML injection
element.innerHTML = userInput; // "<script>alert('XSS')</script>"

// ✅ Safe text content
element.textContent = userInput;

// ✅ Or sanitize HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

**Command Injection**:
```typescript
// ❌ User input in shell command
exec(`ping ${userInput}`); // "8.8.8.8; rm -rf /"

// ✅ Validate input or avoid shell
if (!/^[\d.]+$/.test(userInput)) {
  throw new Error('Invalid IP');
}
exec(`ping ${userInput}`);
```

### A07: Identification and Authentication Failures

**Weak Password Policy**:
```typescript
// ❌ Weak validation
if (password.length > 6) { /* accept */ }

// ✅ Strong validation
const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$/;
if (!strongPassword.test(password)) {
  throw new Error('Password must be 12+ chars with upper, lower, number, symbol');
}
```

**Session Management**:
```typescript
// ❌ Session never expires
app.use(session({
  secret: 'secret',
  cookie: { maxAge: undefined } // Never expires!
}));

// ✅ Session expires
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    maxAge: 15 * 60 * 1000, // 15 minutes
    httpOnly: true,
    secure: true, // HTTPS only
    sameSite: 'strict'
  }
}));
```

## Security Testing Commands

```bash
# Check for known vulnerabilities
npm audit
npm audit fix

# Find potential SQL injection
grep -rn "query.*\${" src/ --include="*.ts"
grep -rn "SELECT.*FROM.*+" src/ --include="*.ts"

# Find XSS risks
grep -rn "innerHTML\|dangerouslySetInnerHTML" src/ --include="*.tsx"

# Find hardcoded secrets
grep -rn "password.*=\|api.*key.*=\|secret.*=" src/ --include="*.ts"

# Find eval/exec usage
grep -rn "eval\|exec" src/ --include="*.ts"

# Check for weak crypto
grep -rn "md5\|sha1" src/ --include="*.ts"
```

## Secure Coding Checklist

### Authentication
- [ ] All protected routes require authentication
- [ ] Passwords hashed with bcrypt/argon2 (10-12 rounds)
- [ ] JWT tokens have expiry (< 1 hour for access tokens)
- [ ] Refresh token rotation implemented
- [ ] Password reset tokens expire (< 1 hour)
- [ ] Multi-factor authentication available
- [ ] Account lockout after failed attempts

### Authorization
- [ ] Users can only access their own data
- [ ] Role-based access control (RBAC) enforced
- [ ] Admin functions require admin role
- [ ] Indirect object references (never expose IDs directly)

### Input Validation
- [ ] All user input validated (whitelist, not blacklist)
- [ ] Parameterized queries used (no string concatenation)
- [ ] File uploads validated (type, size, content)
- [ ] URL redirects validated (no open redirects)
- [ ] JSON schema validation for API inputs

### Data Protection
- [ ] No secrets in code or config files (.env in .gitignore)
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced (no HTTP)
- [ ] Secure cookies (httpOnly, secure, sameSite)
- [ ] No sensitive data in logs
- [ ] PII/PHI properly handled (GDPR/HIPAA if applicable)

### Dependencies
- [ ] npm audit clean (no known vulnerabilities)
- [ ] Dependencies updated regularly
- [ ] Lock files committed (package-lock.json)
- [ ] Unused dependencies removed

### Headers & CORS
- [ ] CORS configured (not wildcard *)
- [ ] Content-Security-Policy header set
- [ ] X-Frame-Options: DENY or SAMEORIGIN
- [ ] X-Content-Type-Options: nosniff
- [ ] Strict-Transport-Security (HSTS) header

### Logging & Monitoring
- [ ] Security events logged (login, logout, access denied)
- [ ] Failed authentication attempts monitored
- [ ] Anomalous behavior detected
- [ ] Logs don't contain sensitive data

## Common Vulnerabilities Reference

| Vulnerability | Pattern | Fix |
|--------------|---------|-----|
| SQL Injection | `query = "SELECT * FROM users WHERE id = " + id` | Use parameterized queries |
| XSS | `element.innerHTML = userInput` | Use `textContent` or sanitize |
| Command Injection | `exec("ping " + userInput)` | Validate input, avoid shell |
| Path Traversal | `fs.readFile("./uploads/" + filename)` | Validate filename, use path.join |
| Weak Crypto | `crypto.createHash('md5')` | Use bcrypt/argon2 |
| Hardcoded Secrets | `const KEY = "abc123"` | Use environment variables |
| Missing Auth | `app.get('/admin', handler)` | Add auth middleware |
| CORS Misconfiguration | `cors({ origin: '*' })` | Specify allowed origins |

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

**Remember**: Security is not optional. Every line of code is a potential vulnerability. Think like an attacker!
