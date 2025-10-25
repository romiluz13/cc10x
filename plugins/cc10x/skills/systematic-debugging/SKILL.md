---
name: systematic-debugging
description: Enforces LOG FIRST FIX LATER methodology to prevent assumption-driven debugging that wastes hours. Always verify runtime data by logging complete object structures before making assumptions about field names or data shapes. Particularly critical for third-party integrations, authentication systems, API responses, and data flow issues where assumptions about data structure commonly cause debugging cycles. Use when debugging fails repeatedly, investigating why expected data is missing, working with unfamiliar APIs, or when you've tried multiple fixes without success. Prevents the anti-pattern of assumption then try fix then still broken then repeat. Real-world testing saved 2 hours by logging first instead of guessing. Loaded by tdd-enforcer agent during DEBUGGING workflow.
license: MIT
---

# Systematic Debugging

**Core Philosophy**: Never guess what the data looks like - ALWAYS log the complete structure first, then fix based on what you SEE, not what you ASSUME.

---

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)

- **Skill**: Systematic Debugging
- **Purpose**: Prevent assumption-driven debugging that wastes hours/days
- **When**: Any bug involving third-party integrations, authentication, APIs, data flow issues
- **Core Rule**: Add comprehensive logging BEFORE attempting any fixes
- **The Anti-Pattern**: Assumption → Try Fix → Still Broken → Try Another Fix → Repeat 10x ❌
- **The Solution**: LOG FIRST → See Actual Data → Apply Correct Fix → Done in 5 min ✅
- **Sections Available**: The 5-Minute Rule, LOG FIRST Pattern, Red Flags Checklist, Comprehensive Logging Guide

---

### Stage 2: Quick Reference (triggered - ~500 tokens)

## The 5-Minute Rule

**If you've been debugging for more than 30 minutes without seeing the actual data → STOP → Add comprehensive logging first.**

## The LOG FIRST Pattern

### ❌ BAD: Assuming Field Names

```typescript
// Don't guess what the data looks like
console.log("Role:", user.role);
console.log("User ID:", user.id);
```

**Problem**: You're assuming:
- The field is called "role" (might be "userRole" or "roles")
- The field exists at the top level (might be nested)
- The data structure matches the documentation

### ✅ GOOD: Logging Complete Structure

```typescript
// See the ACTUAL data structure first
console.log("=== FULL USER OBJECT ===");
console.log(JSON.stringify(user, null, 2));

console.log("=== FULL SESSION CLAIMS ===");
console.log(JSON.stringify(sessionClaims, null, 2));

console.log("=== FULL REQUEST HEADERS ===");
console.log(JSON.stringify(req.headers, null, 2));
```

**Benefits**:
- See ALL available fields
- Discover nested structures
- Find field name mismatches
- Identify data type issues

## Red Flags (ADD LOGGING NOW)

Stop and add comprehensive logging if:

- ⚠️ **Third-party service not behaving as expected** (Clerk, Stripe, Auth0, etc.)
- ⚠️ **Authentication/authorization issues** (JWT, sessions, cookies)
- ⚠️ **Data not appearing where it should** (missing fields, undefined values)
- ⚠️ **We've tried 3+ fixes without success** (we're guessing, not debugging)
- ⚠️ **Documentation says X but behavior is Y** (docs lie, runtime doesn't)
- ⚠️ **Dashboard UI shows data but code doesn't see it** (UI ≠ API response)

## Quick Logging Commands

```typescript
// For any object (most useful!)
console.log("FULL OBJECT:", JSON.stringify(obj, null, 2));

// For errors
console.log("FULL ERROR:", JSON.stringify(error, Object.getOwnPropertyNames(error), 2));

// For API responses
console.log("RESPONSE:", JSON.stringify({ status, headers, data }, null, 2));

// For authentication
console.log("AUTH:", JSON.stringify({ user, session, claims, cookies }, null, 2));
```

## Common Third-Party Mismatches

Real-world examples of docs vs reality:

| Service | Documentation Says | Runtime Actually Uses |
|---------|-------------------|---------------------|
| Clerk | `publicMetadata` (in dashboard UI) | `metadata` (in JWT) |
| Auth0 | `user.roles` | `user['https://app.com/roles']` |
| Stripe | `payment.status` | `payment.payment_intent.status` |

**Lesson**: Dashboard UI field names ≠ API response field names. Always verify!

---

### Stage 3: Detailed Guide (on-demand - ~2500 tokens)

## Comprehensive Logging Guide

### Authentication Issues

When debugging any authentication problem (login, JWT, sessions, cookies):

```typescript
// Step 1: Log EVERYTHING authentication-related
console.log("=== AUTHENTICATION DEBUG ===");

// JWT / Session Claims
console.log("FULL sessionClaims:", JSON.stringify(sessionClaims, null, 2));
console.log("FULL user object:", JSON.stringify(user, null, 2));

// Cookies
console.log("ALL cookies:", JSON.stringify(req.cookies, null, 2));
console.log("Cookie headers:", req.headers.cookie);

// Headers
console.log("Authorization header:", req.headers.authorization);
console.log("ALL headers:", JSON.stringify(req.headers, null, 2));

// Configuration
console.log("Domain config:", process.env.DOMAIN);
console.log("Cookie domain:", cookieOptions.domain);
console.log("Secure flag:", cookieOptions.secure);
console.log("SameSite:", cookieOptions.sameSite);

// User ID / Session ID
console.log("User ID:", user?.id);
console.log("Session ID:", session?.id);

console.log("=== END AUTH DEBUG ===");
```

**Real-world example** (the Clerk metadata bug you hit):

```typescript
// ❌ What you tried (based on docs/dashboard):
const role = auth.sessionClaims?.publicMetadata?.role;
console.log("Role:", role); // undefined (why??)

// ✅ What you should have done first:
console.log("FULL sessionClaims:", JSON.stringify(auth.sessionClaims, null, 2));
// Output shows: { "metadata": { "role": "admin" } }
// ^ AHA! It's "metadata", not "publicMetadata"!

// ✅ Correct fix (found in 5 minutes instead of 3 days):
const role = auth.sessionClaims?.metadata?.role;
```

### API Integration Issues

When debugging external API calls (REST, GraphQL, webhooks):

```typescript
// Step 1: Log complete request
console.log("=== API REQUEST DEBUG ===");
console.log("Method:", request.method);
console.log("URL:", request.url);
console.log("Headers:", JSON.stringify(request.headers, null, 2));
console.log("Body:", JSON.stringify(request.body, null, 2));
console.log("Query params:", JSON.stringify(request.query, null, 2));

// Step 2: Log complete response
console.log("=== API RESPONSE DEBUG ===");
console.log("Status:", response.status);
console.log("Status Text:", response.statusText);
console.log("Headers:", JSON.stringify(response.headers, null, 2));
console.log("Body:", JSON.stringify(response.data, null, 2));

// Step 3: Log error if present
if (error) {
  console.log("=== API ERROR DEBUG ===");
  console.log("Error object:", JSON.stringify(error, Object.getOwnPropertyNames(error), 2));
  console.log("Error message:", error.message);
  console.log("Error response:", JSON.stringify(error.response?.data, null, 2));
}

// Step 4: Log environment/config
console.log("=== CONFIG DEBUG ===");
console.log("API Base URL:", process.env.API_BASE_URL);
console.log("API Key (first 10 chars):", process.env.API_KEY?.substring(0, 10));
console.log("SDK version:", client.version);
```

### Data Flow Issues

When data isn't flowing through your system as expected:

```typescript
// Log at every transformation step
console.log("=== DATA FLOW DEBUG ===");

// Input
console.log("1. INPUT (raw):", JSON.stringify(inputData, null, 2));

// After validation
console.log("2. AFTER VALIDATION:", JSON.stringify(validatedData, null, 2));

// After transformation
console.log("3. AFTER TRANSFORM:", JSON.stringify(transformedData, null, 2));

// Database query
console.log("4. DB QUERY:", query);
console.log("4. DB PARAMS:", JSON.stringify(params, null, 2));

// Database result
console.log("5. DB RESULT:", JSON.stringify(dbResult, null, 2));

// Output
console.log("6. OUTPUT (final):", JSON.stringify(output, null, 2));
```

### Database Issues

When debugging database queries, ORMs, or data persistence:

```typescript
// Step 1: Log the query
console.log("=== DATABASE DEBUG ===");
console.log("Query:", query);
console.log("Parameters:", JSON.stringify(params, null, 2));

// Step 2: Log the result
console.log("Result:", JSON.stringify(result, null, 2));
console.log("Row count:", result.rowCount || result.length);

// Step 3: For ORMs (Prisma, TypeORM, etc.)
console.log("Generated SQL:", prisma.$queryRaw`...`);

// Step 4: Log connection status
console.log("Database URL:", process.env.DATABASE_URL?.substring(0, 20) + "...");
console.log("Connection pool:", pool.totalCount, "total,", pool.idleCount, "idle");
```

### Performance Issues

When debugging slow operations or memory leaks:

```typescript
// Step 1: Add timing logs
console.time("Operation");
console.log("=== PERFORMANCE DEBUG ===");

// Before expensive operation
console.log("Memory before:", process.memoryUsage());
console.log("Items to process:", items.length);

// During operation (in loop)
items.forEach((item, index) => {
  if (index % 100 === 0) {
    console.log(`Progress: ${index}/${items.length}`);
    console.log("Memory:", process.memoryUsage().heapUsed);
  }
});

// After operation
console.log("Memory after:", process.memoryUsage());
console.timeEnd("Operation");
```

## The Systematic Debugging Workflow

### Step-by-Step Process

```
1. ❌ DON'T START WITH: "Let me try changing X..."
   ✅ START WITH: "Let me add logging to see what X actually is..."

2. Add comprehensive logging (5 minutes)
   - Log FULL objects with JSON.stringify(obj, null, 2)
   - Log at multiple points in the flow
   - Log inputs, transformations, outputs

3. Run the code and capture logs
   - Save to file if too long
   - Share with team/AI for analysis

4. Analyze the ACTUAL data
   - Compare to documentation
   - Find mismatches (field names, structure, types)
   - Identify the root cause

5. Apply the correct fix
   - Based on what you SEE, not what you ASSUME
   - Usually takes 5 minutes once you see the data

6. Verify the fix
   - Check logs show expected values
   - Remove or reduce logging after confirming
```

## Real-World Case Study: The Clerk Metadata Bug

### The Problem

User reported: "Clerk authentication works, but user roles aren't being read. Dashboard shows the role in `publicMetadata`, but code returns `undefined`."

### ❌ What Was Done (3 Days Wasted)

```typescript
// Day 1: Try various field names (guessing)
const role = auth.sessionClaims?.publicMetadata?.role; // undefined
const role = auth.sessionClaims?.public_metadata?.role; // undefined
const role = auth.sessionClaims?.user_metadata?.role; // undefined

// Day 2: Try fixing CORS, domains, cookies (wrong direction)
// ... 5+ different configuration changes ...
// Still undefined

// Day 3: Finally add logging
console.log("FULL sessionClaims:", JSON.stringify(auth.sessionClaims, null, 2));
// Output: { "metadata": { "role": "admin" }, ... }
```

**Time wasted**: 3 days
**Root cause found**: 5 minutes after adding logging

### ✅ What SHOULD Have Been Done (5 Minutes Total)

```typescript
// Minute 1: User reports issue
// Minute 2: Add comprehensive logging
console.log("=== CLERK AUTH DEBUG ===");
console.log("FULL sessionClaims:", JSON.stringify(auth.sessionClaims, null, 2));
console.log("FULL user:", JSON.stringify(auth.user, null, 2));

// Minute 3: Run code, capture logs
// Output shows: { "metadata": { "role": "admin" } }

// Minute 4: Identify mismatch
// Dashboard says "publicMetadata" but JWT uses "metadata"

// Minute 5: Apply correct fix
const role = auth.sessionClaims?.metadata?.role; // ✅ Works!
```

**Time saved**: 2 days, 23 hours, 55 minutes

### The Lesson

**Dashboard UI ≠ JWT structure**. Clerk's dashboard shows "Public Metadata" in the UI, but the actual JWT token uses the field name `metadata`.

**Never trust the UI** - always verify with runtime logging.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Assumption-Driven Debugging

```typescript
// ❌ BAD: Making assumptions
// "The docs say it's in publicMetadata, so..."
const role = user.publicMetadata.role;

// ❌ BAD: Trying random fixes
// "Maybe it's called user_metadata?"
const role = user.user_metadata?.role;

// ❌ BAD: Changing everything
// "Let me try fixing CORS, domains, cookies all at once..."

// ✅ GOOD: Log first, understand, then fix
console.log("FULL USER:", JSON.stringify(user, null, 2));
// See actual structure → Apply correct fix
```

### Anti-Pattern 2: Partial Logging

```typescript
// ❌ BAD: Only logging what you think is relevant
console.log("Role:", role); // undefined (not helpful!)

// ✅ GOOD: Log the complete object
console.log("FULL OBJECT:", JSON.stringify(sessionClaims, null, 2));
// Shows ALL fields, nested structure, actual field names
```

### Anti-Pattern 3: Trusting Documentation Alone

```typescript
// ❌ BAD: Assuming docs are correct
// Docs say: "User roles are in user.roles"
const roles = user.roles;

// ✅ GOOD: Verify with runtime data
console.log("FULL USER:", JSON.stringify(user, null, 2));
// Actual structure: user['https://myapp.com/roles']
```

## Logging Best Practices

### 1. Use Structured Logging

```typescript
// ✅ GOOD: Easy to find in logs
console.log("=== AUTHENTICATION DEBUG ===");
console.log("Step 1: Session Claims");
console.log(JSON.stringify(sessionClaims, null, 2));
console.log("Step 2: Cookies");
console.log(JSON.stringify(cookies, null, 2));
console.log("=== END DEBUG ===");
```

### 2. Log at Multiple Points

```typescript
// ✅ GOOD: See data transformation
console.log("INPUT:", JSON.stringify(input, null, 2));
console.log("AFTER VALIDATION:", JSON.stringify(validated, null, 2));
console.log("AFTER TRANSFORM:", JSON.stringify(transformed, null, 2));
console.log("OUTPUT:", JSON.stringify(output, null, 2));
```

### 3. Include Context

```typescript
// ✅ GOOD: Know what you're looking at
console.log("User", userId, "at", new Date().toISOString());
console.log("Request ID:", requestId);
console.log("Environment:", process.env.NODE_ENV);
```

### 4. Handle Large Objects

```typescript
// For very large objects, log keys first
console.log("Available keys:", Object.keys(largeObject));

// Then log specific parts
console.log("Relevant section:", JSON.stringify(largeObject.section, null, 2));
```

### 5. Clean Up After

```typescript
// After finding the issue, either:
// 1. Remove debug logs
// 2. Or keep as conditional logging:

if (process.env.DEBUG === 'true') {
  console.log("DEBUG:", JSON.stringify(data, null, 2));
}
```

## Integration-Specific Checklists

### Clerk / Auth0 / Firebase Auth

When debugging authentication:
- [ ] Log full JWT payload / sessionClaims
- [ ] Log all cookie headers
- [ ] Log domain configuration
- [ ] Log user ID and session ID
- [ ] Compare dashboard UI fields vs actual JWT fields
- [ ] Check cookie domain matches your app domain
- [ ] Verify token expiration timestamps

### Stripe / Payment Gateways

When debugging payment processing:
- [ ] Log full webhook payload
- [ ] Log payment intent complete structure
- [ ] Log customer object
- [ ] Log webhook signature verification result
- [ ] Check API version mismatch (docs vs your version)
- [ ] Log error responses in full

### Database / ORM

When debugging data persistence:
- [ ] Log the generated SQL query
- [ ] Log query parameters
- [ ] Log result row count
- [ ] Log full result set (or first few rows)
- [ ] Check connection pool status
- [ ] Log transaction state

## When to Stop Logging

You can reduce logging once you:
- ✅ Found the root cause
- ✅ Applied the fix
- ✅ Verified it works
- ✅ Understand the issue for future reference

Keep minimal logging for production monitoring:
```typescript
// Keep: Error cases
logger.error("Payment failed", { userId, amount, error });

// Keep: Important events
logger.info("User logged in", { userId, timestamp });

// Remove: Verbose debug logs
// console.log("FULL OBJECT:", ...); // Remove after debugging
```

## Summary: The Golden Rules

1. **LOG FIRST, FIX LATER** - Add comprehensive logging before attempting any fixes
2. **LOG COMPLETE OBJECTS** - Use `JSON.stringify(obj, null, 2)` to see everything
3. **NEVER TRUST DOCS ALONE** - Verify field names and structure with runtime data
4. **THE 5-MINUTE RULE** - If debugging > 30 min without seeing data, stop and log
5. **DASHBOARD ≠ API** - UI field names often differ from actual API responses
6. **SEE, DON'T ASSUME** - Base fixes on what you SEE in logs, not what you ASSUME

---

**Time Saved**: Using this systematic approach saves hours or even days by finding issues in minutes instead of trying random fixes.

**Success Rate**: Issues found in 5-10 minutes vs hours/days of assumption-driven debugging.
