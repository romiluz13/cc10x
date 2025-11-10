---
name: security-patterns
description: Context-aware security analysis that verifies functionality works securely. Use PROACTIVELY when reviewing code that handles user input, authentication, authorization, file uploads, API integrations, or sensitive data. First understands project's security model and functionality requirements, then checks for security vulnerabilities that affect functionality. Provides specific remediation with code examples aligned with project patterns. Focuses on security issues that block or degrade functionality, not generic OWASP checklist.
allowed-tools: Read, Grep, Glob
---

# Security Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware security analysis that understands the project's security model before checking for vulnerabilities. It focuses on security issues that affect functionality, providing specific remediation with code examples aligned with project patterns.

**Unique Value**:

- Context-aware security analysis (not generic OWASP checklist)
- Focuses on security issues that affect functionality
- Provides specific remediation with code examples
- Understands project's security model before checking

**When to Use**:

- After functionality is verified
- When reviewing code that handles user input, authentication, authorization, file uploads, API integrations, or sensitive data
- When security issues might affect functionality

---

## Functionality First Mandate

**BEFORE applying security checks, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (Security constraints)
   - Dependencies: What does it need? (Auth libraries, security services)
   - Edge Cases: What can go wrong? (Security edge cases)
   - Verification: How do we know it works? (Security tests)
   - Context: Where does it fit? (Codebase structure)

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type):
   - UI Features → User Flow, Admin Flow, System Flow
   - Backend APIs → Request Flow, Response Flow, Error Flow, Data Flow
   - Utilities → Input Flow, Processing Flow, Output Flow, Error Flow
   - Integrations → Integration Flow, Data Flow, Error Flow, State Flow

3. **THEN understand project's security model** - Before checking security

4. **THEN check security** - Only security issues that affect functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Reference Materials

**For detailed patterns and reference materials, see:**

- **PATTERNS.md**: Security Pattern Library (Authentication, Authorization, Injection Prevention, File Upload, Secrets Management)
- **REFERENCE.md**: Security Coverage, Quick Facts, Authentication Decision Framework, Access Control Patterns, Cryptography Patterns, Security Headers, Rate Limiting, Quick Security Checklist, Red Flags

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any security checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this code supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc. - context-dependent)

3. **Verify Functionality Works**:
   - Does functionality work? (tested)
   - Do flows work? (tested)
   - Does error handling work? (tested)

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely in S3
- Must send file metadata to CRM API
- Must display upload progress to user
- Must handle errors gracefully

**Constraints**:

- Security: Files must be encrypted at rest, access controlled
- Performance: Upload must complete within 30 seconds
- Scale: Must handle 100 concurrent uploads

**User Flow**:

1. User clicks "Upload File" button
2. User selects file from device
3. User sees upload progress indicator
4. User sees success message with file link
5. User can view uploaded file in CRM

**System Flow**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type and size
3. System stores file in secure storage (S3 bucket)
4. System sends file metadata to CRM API
5. System returns success response to user

**Functional Verification**:

- ✅ User can upload file (tested)
- ✅ File appears in CRM (tested)
- ✅ Error handling works (tested: invalid file type, size limit)

---

### Phase 2: Understand Project's Security Model (MANDATORY SECOND STEP)

**Before checking security, understand how this project handles security**:

1. **Load Project Context Understanding**:
   - Load `project-context-understanding` skill
   - Map project's security patterns
   - Identify authentication patterns used
   - Identify authorization patterns used
   - Identify data handling patterns used

2. **Map Authentication Patterns**:

   ```bash
   # Find authentication implementation
   grep -r "jwt\|session\|oauth\|auth" --include="*.ts" --include="*.tsx" | head -20

   # Find authentication middleware
   grep -r "authenticate\|verifyToken\|checkAuth" --include="*.ts" | head -20
   ```

3. **Map Authorization Patterns**:

   ```bash
   # Find authorization checks
   grep -r "authorize\|permission\|role\|canAccess" --include="*.ts" | head -20

   # Find access control patterns
   grep -r "RBAC\|ABAC\|ACL" --include="*.ts" -i | head -20
   ```

4. **Map Data Handling Patterns**:

   ```bash
   # Find data validation
   grep -r "validate\|sanitize\|escape" --include="*.ts" | head -20

   # Find encryption/decryption
   grep -r "encrypt\|decrypt\|hash\|bcrypt" --include="*.ts" | head -20
   ```

5. **Map Trust Boundaries**:
   - Identify where user input enters the system
   - Identify where data crosses trust boundaries
   - Identify where authentication/authorization checks occur
   - Identify where sensitive data is stored/transmitted

**Document Project's Security Model**:

- Authentication: JWT, Sessions, OAuth, etc.
- Authorization: RBAC, ABAC, ACL, etc.
- Data Validation: Libraries used, patterns followed
- Encryption: Where used, algorithms used
- Trust Boundaries: Where checks occur

**Example Output**:

```
Project Security Model:
Authentication: JWT tokens (HS256), stored in httpOnly cookies
Authorization: RBAC (admin, editor, viewer roles)
Data Validation: Zod schemas for API inputs, React Hook Form for UI
Encryption: AES-256 for file storage, TLS for transport
Trust Boundaries:
- API endpoints: JWT verification middleware
- File uploads: Authentication + file validation
- Database queries: Parameterized queries only
```

---

### Phase 3: Security Analysis (Only Issues Affecting Functionality)

**After understanding functionality and project security model, check security**:

1. **Map Security Issues to Functionality**:
   - For each functionality flow, identify security risks
   - Check if security issues affect functionality
   - Prioritize: Critical (blocks functionality) > Important (affects functionality) > Minor (defer)

2. **Check Authentication** (if functionality requires auth):
   - Is authentication implemented correctly?
   - Does it prevent unauthorized access to functionality?
   - Are tokens validated properly?
   - Are sessions managed securely?

3. **Check Authorization** (if functionality requires authorization):
   - Is authorization implemented correctly?
   - Does it prevent unauthorized access to functionality?
   - Are permissions checked at the right boundaries?
   - Are role checks correct?

4. **Check Input Validation** (if functionality handles user input):
   - Is input validated correctly?
   - Does validation prevent functionality from working incorrectly?
   - Are edge cases handled?
   - Are injection attacks prevented?

5. **Check Data Handling** (if functionality handles sensitive data):
   - Is sensitive data handled securely?
   - Is data encrypted at rest and in transit?
   - Are secrets managed securely?
   - Are error messages safe?

**Provide Specific Fixes with Code Examples**:

For each security issue found, provide:

- **Issue**: Clear description of the security issue
- **Impact**: How it affects functionality
- **Location**: File path and line number
- **Fix**: Specific code example aligned with project patterns
- **Priority**: Critical, Important, or Minor

**Example**:

````markdown
## Security Finding: Missing Authentication Check

**Issue**: File upload endpoint lacks authentication check, allowing unauthorized uploads.

**Impact**: Blocks functionality - unauthorized users can upload files, breaking access control.

**Location**: `src/api/files.ts:45`

**Current Code**:

```typescript
app.post("/api/files/upload", upload.single("file"), async (req, res) => {
  const file = req.file;
  // Missing: Authentication check
  await storage.upload(file);
  res.json({ success: true });
});
```
````

**Fix** (aligned with project's JWT pattern):

```typescript
import { authenticate } from "../middleware/auth";

app.post(
  "/api/files/upload",
  authenticate,
  upload.single("file"),
  async (req, res) => {
    const file = req.file;
    // Now authenticated - req.user is available
    await storage.upload(file, { userId: req.user.id });
    res.json({ success: true });
  },
);
```

**Priority**: Critical (blocks functionality)

````

---

## Priority Classification

**Critical (Must Fix - Blocks Functionality)**:

- Blocks functionality (injection attacks, broken auth)
- Prevents feature from working (unauthorized access, data corruption)
- Breaks user flows (XSS stealing data, CSRF breaking actions)
- Examples:
  - Missing authentication on protected endpoints
  - SQL injection allowing data corruption
  - File upload allowing malicious files that break functionality

**Important (Should Fix - Affects Functionality)**:

- Affects functionality negatively (weak auth, missing validation)
- Degrades user experience (leaked errors, broken flows)
- Examples:
  - Weak password hashing (if passwords are used)
  - Missing input validation (if causes incorrect behavior)
  - Insecure error messages (if leak sensitive data)

**Minor (Can Defer - Doesn't Affect Functionality)**:

- Doesn't affect functionality (security headers, perfect hashing)
- Generic best practices (rate limiting, perfect CSP)
- Examples:
  - Missing security headers (if functionality works)
  - Rate limiting (if not causing issues)
  - Perfect password hashing (if basic hashing works)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Security Analysis Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Project Security Model Summary

[Brief summary of project's security patterns from Phase 2]

## Security Findings

### Critical Issues (Blocks Functionality)

[For each critical issue:]

- **Issue**: [Description]
- **Impact**: [How it affects functionality]
- **Location**: [File:line]
- **Fix**: [Specific code example aligned with project patterns]
- **Priority**: Critical

### Important Issues (Affects Functionality)

[For each important issue:]

- **Issue**: [Description]
- **Impact**: [How it affects functionality]
- **Location**: [File:line]
- **Fix**: [Specific code example aligned with project patterns]
- **Priority**: Important

### Minor Issues (Can Defer)

[For each minor issue:]

- **Issue**: [Description]
- **Impact**: [Why it doesn't affect functionality]
- **Location**: [File:line]
- **Fix**: [Specific code example - optional]
- **Priority**: Minor

## Recommendations

[Prioritized list of fixes - Critical first, then Important, then Minor]
```

---

## Usage Guidelines

### For Review Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis)
2. **Then**: Complete Phase 2 (Understand Project's Security Model)
3. **Then**: Complete Phase 3 (Security Analysis - Only Issues Affecting Functionality)
4. **Focus**: Security issues that block or degrade functionality

### Key Principles

1. **Functionality First**: Always understand functionality before checking security
2. **Context-Aware**: Understand project's security model before checking
3. **Specific Fixes**: Provide code examples aligned with project patterns
4. **Prioritize by Impact**: Critical (blocks functionality) > Important (affects functionality) > Minor (defer)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to security checks
2. **Ignoring Project Context**: Don't provide generic fixes - align with project patterns
3. **Generic OWASP Checklist**: Don't check everything - focus on functionality-affecting issues
4. **Missing Specific Fixes**: Don't just identify issues - provide specific code examples
5. **Wrong Priority**: Don't mark minor issues as critical - prioritize by functionality impact
6. **No Code Examples**: Don't just describe issues - show how to fix them

---

_This skill enables context-aware security analysis that understands project's security model and focuses on security issues affecting functionality, providing specific remediation with code examples aligned with project patterns._
````
