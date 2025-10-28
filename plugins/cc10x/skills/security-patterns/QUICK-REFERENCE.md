# Security Patterns - Quick Reference (Stage 2)

## OWASP Top 10 (2021) Quick Check

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

---

## Critical Security Patterns

### Input Validation (A03 - Injection)
```typescript
// ❌ NEVER: String concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ ALWAYS: Parameterized queries
const query = `SELECT * FROM users WHERE id = $1`;
const result = await db.query(query, [userId]);
```

### Authentication (A01, A07)
```typescript
// ❌ NEVER: Missing auth check
app.get('/admin/users', getAllUsers);

// ✅ ALWAYS: Auth + authorization middleware
app.get('/admin/users', authMiddleware, adminMiddleware, getAllUsers);
```

### Secrets Management (A02)
```typescript
// ❌ NEVER: Hardcoded secrets
const API_KEY = 'sk_live_abc123';

// ✅ ALWAYS: Environment variables
const API_KEY = process.env.API_KEY;
```

### Password Hashing (A02, A07)
```typescript
// ❌ NEVER: Weak hashing
crypto.createHash('md5').update(password);

// ✅ ALWAYS: bcrypt/argon2 (10-12 rounds)
await bcrypt.hash(password, 12);
```

### CORS Configuration (A01)
```typescript
// ❌ NEVER: Allow all origins
app.use(cors({ origin: '*' }));

// ✅ ALWAYS: Whitelist specific origins
app.use(cors({ origin: ['https://example.com'] }));
```

### CSRF Protection (A01)
```typescript
// ❌ NEVER: No CSRF token
app.post('/transfer', transferMoney);

// ✅ ALWAYS: CSRF token validation
app.post('/transfer', csrfMiddleware, transferMoney);
```

---

## Red Flags 🚩

```bash
# Search for these patterns:
grep -r "eval\|exec\|innerHTML" src/
grep -r "password.*=.*['\"]" src/
grep -r "TODO.*security\|FIXME.*auth" src/
grep -r "http://" src/ | grep -v localhost
grep -r "console.log.*password\|console.log.*token" src/
```

---

## Common Mistakes

| Mistake | Risk | Fix |
|---------|------|-----|
| Storing passwords in plain text | A02, A07 | Use bcrypt/argon2 |
| No input validation | A03 | Validate all inputs |
| Hardcoded secrets | A02 | Use env variables |
| Missing auth checks | A01 | Add middleware |
| Weak crypto | A02 | Use strong algorithms |
| No HTTPS | A02 | Enforce HTTPS |
| No rate limiting | A07 | Add rate limiter |
| Verbose error messages | A01 | Generic messages |

---

## Quick Audit Checklist

- [ ] All endpoints have auth checks
- [ ] All inputs are validated
- [ ] No hardcoded secrets
- [ ] Passwords hashed with bcrypt/argon2
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] CSRF tokens used
- [ ] Rate limiting enabled
- [ ] Security headers set
- [ ] Dependencies up to date

---

## When to Load Stage 3 (Detailed Guide)

Load detailed guide when:
- Implementing authentication system
- Handling payment processing
- Storing sensitive data
- Building public APIs
- Reviewing security-critical code
- Investigating security vulnerabilities

---

**Token Cost**: ~500 tokens
**Use**: When security analysis is needed
**Next**: Load DETAILED-GUIDE.md for comprehensive patterns

