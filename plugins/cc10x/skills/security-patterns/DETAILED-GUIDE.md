# Security Patterns - Detailed Guide (Stage 3)

## A01: Broken Access Control

### Authentication vs Authorization
```typescript
// Authentication: Who are you?
const user = await authenticateUser(username, password);

// Authorization: What can you do?
if (!user.roles.includes('admin')) {
  throw new UnauthorizedError('Admin access required');
}
```

### Role-Based Access Control (RBAC)
```typescript
const rolePermissions = {
  admin: ['read', 'write', 'delete', 'manage-users'],
  editor: ['read', 'write'],
  viewer: ['read']
};

function checkPermission(user, action) {
  const permissions = rolePermissions[user.role];
  if (!permissions.includes(action)) {
    throw new ForbiddenError(`${user.role} cannot ${action}`);
  }
}
```

### Attribute-Based Access Control (ABAC)
```typescript
function canAccess(user, resource) {
  return user.department === resource.department &&
         user.clearanceLevel >= resource.requiredLevel &&
         resource.allowedRoles.includes(user.role);
}
```

---

## A02: Cryptographic Failures

### Password Hashing
```typescript
import bcrypt from 'bcrypt';

// Hashing
const hash = await bcrypt.hash(password, 12);

// Verification
const isValid = await bcrypt.compare(password, hash);
```

### Encryption at Rest
```typescript
import crypto from 'crypto';

const algorithm = 'aes-256-gcm';
const key = crypto.scryptSync(masterKey, 'salt', 32);

function encrypt(data) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();
  return `${iv.toString('hex')}:${encrypted}:${authTag.toString('hex')}`;
}

function decrypt(encrypted) {
  const [iv, data, authTag] = encrypted.split(':');
  const decipher = crypto.createDecipheriv(algorithm, key, Buffer.from(iv, 'hex'));
  decipher.setAuthTag(Buffer.from(authTag, 'hex'));
  let decrypted = decipher.update(data, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}
```

### TLS/HTTPS
```typescript
// Enforce HTTPS
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https') {
    res.redirect(`https://${req.header('host')}${req.url}`);
  } else {
    next();
  }
});

// HSTS Header
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  next();
});
```

---

## A03: Injection

### SQL Injection Prevention
```typescript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ SAFE: Parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);
```

### NoSQL Injection Prevention
```typescript
// ❌ VULNERABLE
const user = await User.findOne({ email: req.body.email });

// ✅ SAFE: Validate input type
const email = String(req.body.email).trim();
const user = await User.findOne({ email });
```

### Command Injection Prevention
```typescript
// ❌ VULNERABLE
exec(`ls ${userInput}`);

// ✅ SAFE: Use array syntax
execFile('ls', [userInput]);
```

### XSS Prevention
```typescript
// ❌ VULNERABLE
res.send(`<h1>${userInput}</h1>`);

// ✅ SAFE: Escape HTML
import DOMPurify from 'isomorphic-dompurify';
const safe = DOMPurify.sanitize(userInput);
res.send(`<h1>${safe}</h1>`);
```

---

## A07: Authentication Failures

### Multi-Factor Authentication (MFA)
```typescript
async function loginWithMFA(email, password) {
  // Step 1: Verify password
  const user = await User.findOne({ email });
  const isValid = await bcrypt.compare(password, user.passwordHash);
  if (!isValid) throw new UnauthorizedError('Invalid credentials');

  // Step 2: Send MFA code
  const mfaCode = generateCode();
  await sendMFACode(user.phone, mfaCode);

  // Step 3: Verify MFA code
  const verified = await verifyMFACode(user.id, mfaCode);
  if (!verified) throw new UnauthorizedError('Invalid MFA code');

  // Step 4: Issue token
  return generateJWT(user);
}
```

### Session Management
```typescript
// Secure session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,        // HTTPS only
    httpOnly: true,      // No JavaScript access
    sameSite: 'strict',  // CSRF protection
    maxAge: 3600000      // 1 hour
  }
}));
```

### JWT Best Practices
```typescript
import jwt from 'jsonwebtoken';

// Issue token with short expiry
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '15m' }  // Short expiry
);

// Verify token
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  // Token valid
} catch (err) {
  // Token invalid or expired
}
```

---

## Security Headers

```typescript
app.use((req, res, next) => {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');

  // Prevent MIME sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Enable XSS protection
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Content Security Policy
  res.setHeader('Content-Security-Policy', "default-src 'self'");

  // Referrer Policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  next();
});
```

---

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // 100 requests per window
  message: 'Too many requests'
});

app.post('/login', limiter, loginHandler);
```

---

**Use**: When implementing security-critical features
**Reference**: OWASP Top 10 2021

