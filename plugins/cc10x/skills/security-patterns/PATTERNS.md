# Security Patterns - Pattern Library

Reference security patterns. Use AFTER understanding functionality and project security model (see SKILL.md Phases 1-2).

## Security Pattern Library

### Authentication Patterns

**Understand project's authentication pattern first, then check**:

**JWT Pattern** (if project uses JWT):

```typescript
// Check: Is algorithm specified?
// VULNERABLE (if project uses JWT)
const decoded = jwt.verify(token, secret);

// SECURE (aligned with project pattern)
const decoded = jwt.verify(token, secret, { algorithms: ["HS256"] });

// Check: Are tokens validated on every request?
// VULNERABLE
app.get("/api/protected", (req, res) => {
  // Missing: Token validation
  res.json({ data: sensitiveData });
});

// SECURE (aligned with project pattern)
import { authenticate } from "../middleware/auth";
app.get("/api/protected", authenticate, (req, res) => {
  res.json({ data: sensitiveData });
});
```

**Session Pattern** (if project uses sessions):

```typescript
// Check: Are sessions managed securely?
// VULNERABLE
app.use(
  session({
    secret: "hardcoded-secret", // Should be env variable
    cookie: { httpOnly: false }, // Should be httpOnly: true
  }),
);

// SECURE (aligned with project pattern)
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    cookie: {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
    },
  }),
);
```

### Authorization Patterns

**Understand project's authorization pattern first, then check**:

**RBAC Pattern** (if project uses RBAC):

```typescript
// Check: Are role checks correct?
// VULNERABLE
function canDelete(user, file) {
  return user.role === "admin"; // Missing: Check file ownership
}

// SECURE (aligned with project pattern)
function canDelete(user, file) {
  return user.role === "admin" || file.ownerId === user.id;
}
```

**ABAC Pattern** (if project uses ABAC):

```typescript
// Check: Are attribute checks complete?
// VULNERABLE
function canEdit(user, document) {
  return user.id === document.ownerId; // Missing: Department check
}

// SECURE (aligned with project pattern)
function canEdit(user, document) {
  return (
    user.id === document.ownerId ||
    (user.department === document.department && user.role === "manager")
  );
}
```

### Injection Prevention Patterns

**Understand project's validation pattern first, then check**:

**SQL Injection** (if project uses SQL):

```typescript
// Check: Are queries parameterized?
// VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.query(query);

// SECURE (aligned with project pattern)
const query = "SELECT * FROM users WHERE email = ?";
db.query(query, [email]);
```

**NoSQL Injection** (if project uses MongoDB):

```typescript
// Check: Is input validated?
// VULNERABLE
db.collection("users").findOne({ email: req.body.email });

// SECURE (aligned with project pattern - if project uses Zod)
import { z } from "zod";
const emailSchema = z.string().email();
const email = emailSchema.parse(req.body.email);
db.collection("users").findOne({ email });
```

**XSS Prevention** (if project renders user input):

```typescript
// Check: Is user input sanitized?
// VULNERABLE
element.innerHTML = userInput;

// SECURE (aligned with project pattern)
element.textContent = userInput;
// OR if HTML needed (aligned with project pattern)
import DOMPurify from "dompurify";
element.innerHTML = DOMPurify.sanitize(userInput);
```

### File Upload Security Patterns

**Understand project's file handling pattern first, then check**:

```typescript
// Check: Is file validation correct?
// VULNERABLE
app.post("/api/files/upload", upload.single("file"), (req, res) => {
  const file = req.file;
  // Missing: File type validation, size check
  await storage.upload(file);
});

// SECURE (aligned with project pattern)
import { z } from "zod";
const fileSchema = z.object({
  mimetype: z.enum(["application/pdf", "image/jpeg", "image/png"]),
  size: z.number().max(10 * 1024 * 1024), // 10MB
});

app.post(
  "/api/files/upload",
  authenticate,
  upload.single("file"),
  async (req, res) => {
    const file = req.file;
    fileSchema.parse(file); // Validates type and size
    const sanitizedFilename = sanitizeFilename(file.originalname);
    await storage.upload(file, { filename: sanitizedFilename });
  },
);
```

### Secrets Management Patterns

**Understand project's secrets management pattern first, then check**:

```typescript
// Check: Are secrets managed securely?
// VULNERABLE
const API_KEY = "sk_live_abc123def456";

// SECURE (aligned with project pattern)
const API_KEY = process.env.STRIPE_API_KEY;
if (!API_KEY) throw new Error("Missing STRIPE_API_KEY");

// OR if project uses secrets manager
import { getSecret } from "../services/secrets";
const API_KEY = await getSecret("stripe-api-key");
```
