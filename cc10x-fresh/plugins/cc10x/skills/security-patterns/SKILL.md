---
name: security-patterns
description: Security best practices and vulnerability prevention patterns. Use when reviewing code for security issues, implementing auth, or handling sensitive data.
allowed-tools: Read, Grep
---

# Security Patterns & Best Practices

Common security vulnerabilities and how to prevent them.

## 1. Authentication & Authorization

### ✅ Secure Pattern
```typescript
// Hash passwords
import bcrypt from 'bcrypt';
const hashedPassword = await bcrypt.hash(password, 10);

// JWT with expiration
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// Authorization middleware
function requireRole(role: string) {
  return (req, res, next) => {
    if (!req.user || req.user.role !== role) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}
```

### ❌ Insecure Pattern
```typescript
// Plaintext passwords - NEVER
const user = { password: req.body.password };

// No expiration - DANGEROUS
const token = jwt.sign({ userId }, secret);

// No authorization check - SECURITY HOLE
app.delete('/users/:id', deleteUser);
```

## 2. Input Validation

### ✅ Secure Pattern
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email().max(255),
  age: z.number().int().min(0).max(150),
  username: z.string().min(3).max(50).regex(/^[a-zA-Z0-9_]+$/)
});

try {
  const validated = userSchema.parse(req.body);
} catch (error) {
  return res.status(400).json({ error: 'Invalid input' });
}
```

### ❌ Insecure Pattern
```typescript
// No validation - SQL/XSS risk
const email = req.body.email;
db.query(`SELECT * FROM users WHERE email = '${email}'`);
```

## 3. SQL Injection Prevention

### ✅ Secure Pattern
```typescript
// Parameterized queries
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// ORM with escaping
const user = await User.findOne({ where: { email } });
```

### ❌ Insecure Pattern
```typescript
// String concatenation - VULNERABLE
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);
```

## 4. XSS Prevention

### ✅ Secure Pattern
```typescript
// React auto-escapes
<div>{userInput}</div>

// Manual escaping if needed
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

// Content Security Policy
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline'"
  );
  next();
});
```

### ❌ Insecure Pattern
```typescript
// dangerouslySetInnerHTML - RISKY
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// Direct DOM manipulation with user input
element.innerHTML = userInput;
```

## 5. Secrets Management

### ✅ Secure Pattern
```typescript
// Environment variables
const apiKey = process.env.API_KEY;
if (!apiKey) throw new Error('API_KEY not configured');

// Never log secrets
logger.info('API call', { endpoint, status }); // Don't log apiKey

// .env.example for documentation
// API_KEY=your_key_here
```

### ❌ Insecure Pattern
```typescript
// Hardcoded secrets - NEVER COMMIT
const apiKey = 'sk_live_abc123xyz';

// Secrets in logs
logger.info('Request', { apiKey, password });

// Secrets in error messages
throw new Error(`Auth failed with key: ${apiKey}`);
```

## 6. CORS Configuration

### ✅ Secure Pattern
```typescript
import cors from 'cors';

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### ❌ Insecure Pattern
```typescript
// Allow all origins - DANGEROUS in production
app.use(cors({ origin: '*', credentials: true }));
```

## 7. Rate Limiting

### ✅ Secure Pattern
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests'
});

app.use('/api/', limiter);
```

## 8. File Upload Security

### ✅ Secure Pattern
```typescript
import multer from 'multer';
import path from 'path';

const upload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|pdf/;
    const ext = path.extname(file.originalname).toLowerCase();
    const mime = allowedTypes.test(file.mimetype);
    
    if (ext && mime) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  }
});
```

## Security Checklist

### Pre-Deployment
- [ ] No hardcoded secrets
- [ ] All inputs validated
- [ ] SQL queries parameterized
- [ ] XSS protection enabled
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting active
- [ ] Dependencies audited (`npm audit`)
- [ ] Authentication required for sensitive endpoints
- [ ] Authorization checks in place

### Code Review
- [ ] Sensitive data never logged
- [ ] Errors don't expose system info
- [ ] File uploads restricted
- [ ] Session management secure
- [ ] Third-party libraries trusted

## Quick Checks

```bash
# Find potential secrets
grep -r "password\|api_key\|secret\|token" --include="*.ts" --include="*.js"

# Check dependencies
npm audit --audit-level=moderate

# Find SQL concatenation
grep -r "query\s*=.*\${" --include="*.ts"

# Find dangerouslySetInnerHTML
grep -r "dangerouslySetInnerHTML" --include="*.tsx"
```

## Common Vulnerabilities (OWASP Top 10)

1. **Broken Access Control**: Missing authorization checks
2. **Cryptographic Failures**: Weak encryption, plaintext passwords
3. **Injection**: SQL, XSS, Command injection
4. **Insecure Design**: Missing security requirements
5. **Security Misconfiguration**: Default credentials, verbose errors
6. **Vulnerable Components**: Outdated dependencies
7. **Authentication Failures**: Weak passwords, no MFA
8. **Data Integrity Failures**: No signature verification
9. **Logging Failures**: Missing security event logs
10. **SSRF**: Server-side request forgery

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Security Headers: https://securityheaders.com/
- npm audit: `npm audit --help`
