# cc10x Usage Examples

This document provides real-world examples of cc10x commands in action, showing the complete workflow from start to finish.

---

## Table of Contents

1. [Example 1: Feature Build - User Authentication](#example-1-feature-build---user-authentication)
2. [Example 2: Bug Fix - Payment Processing Error](#example-2-bug-fix---payment-processing-error)
3. [Example 3: Code Review - Pull Request](#example-3-code-review---pull-request)
4. [Example 4: Feature Build - API Endpoint](#example-4-feature-build---api-endpoint)
5. [Example 5: Bug Fix - Memory Leak](#example-5-bug-fix---memory-leak)

---

## Example 1: Feature Build - User Authentication

### Scenario
You need to add JWT-based authentication to a Node.js/Express API that uses PostgreSQL.

### Command

```bash
/feature-build Add user authentication with JWT tokens
```

### Expected Workflow

#### Phase 1: Context Analysis (2 minutes)

```
[Orchestrator]
Analyzing request: "Add user authentication with JWT tokens"
Intent: New feature (keywords: "Add", "authentication")
Workflow selected: /feature-build

[Phase 1: Context Analysis] 🔄
Launching context-analyzer sub-agent...
Auto-invoking skill: codebase-navigation

Searching for similar features...
✅ Found reference: Order management (src/features/orders/)
✅ Pattern identified: Service + Controller + Database layer
✅ Tech stack: Express + TypeScript + Prisma
✅ Testing framework: Jest + Supertest

Context Report:
- Architecture: Feature-based (src/features/<feature-name>/)
- Database: Prisma ORM with PostgreSQL
- API: RESTful with Express Router
- Auth pattern: JWT (jsonwebtoken library already installed)
- Testing: 80%+ coverage requirement
- Error handling: Custom ApiError class

[Quality Gate] ✅ PASS
- Similar feature found
- Project patterns documented
- Dependencies identified
```

#### Phase 2: Planning (3 minutes)

```
[Phase 2: Planning] 🔄

Architecture Decisions:
1. Location: src/features/auth/
2. Files to create:
   - auth.service.ts (business logic)
   - auth.controller.ts (HTTP handlers)
   - auth.routes.ts (Express routes)
   - auth.test.ts (unit tests)
   - auth.integration.test.ts (E2E tests)
3. Database: Use existing User model, add password hashing
4. Middleware: Create authMiddleware.ts for token validation

Implementation Plan:
Task 1 (8 min): Auth Service
- hashPassword(password: string): Promise<string>
- comparePassword(password: string, hash: string): Promise<boolean>
- generateToken(userId: string): string
- verifyToken(token: string): Promise<{userId: string}>

Task 2 (6 min): Auth Controller
- POST /auth/register
- POST /auth/login
- POST /auth/refresh

Task 3 (4 min): Auth Middleware
- requireAuth middleware
- optionalAuth middleware

Task 4 (2 min): Route registration
- Register routes in main app.ts

Total estimated time: 23 minutes

[Quality Gate] ✅ PASS
- Architecture clear
- Implementation steps defined
- No ambiguity in requirements
```

#### Phase 3: Implementation (20 minutes)

```
[Phase 3: Implementation] 🔄

Task 1/4: Auth Service
Launching implementer sub-agent...
Auto-invoking skills:
- test-driven-development (TDD enforcement)
- code-generation (clean code patterns)
- verification-before-completion (quality checks)

[TDD Cycle 1: hashPassword]
RED: Writing failing test...
✅ Test written: auth.service.test.ts:10
   expect(hashPassword('password123')).toBeDefined()

RED: Running test...
✅ Test fails correctly: "hashPassword is not defined"

GREEN: Implementing hashPassword...
✅ Code written: auth.service.ts:15-20
   Uses bcrypt.hash with 10 rounds

GREEN: Running test...
✅ Test passes

[TDD Cycle 2: comparePassword]
RED: Writing failing test...
✅ Test written: auth.service.test.ts:20

GREEN: Implementing comparePassword...
✅ Code written: auth.service.ts:25-30

GREEN: Running test...
✅ Test passes

[... continues for generateToken and verifyToken ...]

Task 1 Complete: Auth Service ✅ (8 min)
- 4 functions implemented
- 12 unit tests passing
- Coverage: 95%

---

Task 2/4: Auth Controller
Launching implementer sub-agent...

[TDD Cycle 1: POST /auth/register]
RED: Writing failing integration test...
✅ Test written: auth.integration.test.ts:15
   POST /auth/register with valid data
   Expect 201 + token

RED: Running test...
✅ Test fails: "Cannot POST /auth/register"

GREEN: Implementing register handler...
✅ Code written: auth.controller.ts:20-40
   Validates input
   Checks user doesn't exist
   Creates user with hashed password
   Returns token

GREEN: Running test...
✅ Test passes

[... continues for login and refresh ...]

Task 2 Complete: Auth Controller ✅ (6 min)
- 3 endpoints implemented
- 15 integration tests passing
- Error handling complete

---

Task 3/4: Auth Middleware
Launching implementer sub-agent...

[TDD Cycle 1: requireAuth middleware]
RED: Writing failing test...
✅ Test written: auth.middleware.test.ts:10
   Expects 401 if no token
   Expects 403 if invalid token
   Expects user in req.user if valid token

GREEN: Implementing requireAuth...
✅ Code written: auth.middleware.ts:10-30

GREEN: Running tests...
✅ All tests pass

Task 3 Complete: Auth Middleware ✅ (4 min)
- 2 middleware functions
- 8 tests passing

---

Task 4/4: Route Registration
Launching implementer sub-agent...

✅ Registered auth routes in app.ts
✅ Applied middleware to protected routes
✅ Updated API documentation

Task 4 Complete ✅ (2 min)

[Phase 3: Implementation Complete]
Total time: 20 minutes
Total tests: 35 (all passing)
```

#### Phase 4: Verification (2 minutes)

```
[Phase 4: Verification] 🔄

Quality Gate Checklist:
✅ All tests pass (35/35)
✅ No existing tests broken (120/120 still passing)
✅ No debug code (console.log, debugger, TODO)
✅ Error handling present (all endpoints have try-catch)
✅ Code follows project patterns (feature-based structure)
✅ TypeScript types defined (no 'any' types)
✅ Integration tests cover happy + error paths
✅ Coverage meets threshold (92% vs 80% required)

[Quality Gate] ✅ PASS
```

#### Phase 5: Finalization (1 minute)

```
[Phase 5: Finalization] 🔄

Git status:
  new file:   src/features/auth/auth.service.ts
  new file:   src/features/auth/auth.controller.ts
  new file:   src/features/auth/auth.routes.ts
  new file:   src/features/auth/auth.middleware.ts
  new file:   src/features/auth/__tests__/auth.service.test.ts
  new file:   src/features/auth/__tests__/auth.integration.test.ts
  new file:   src/features/auth/__tests__/auth.middleware.test.ts
  modified:   src/app.ts

Creating semantic commit message...
✅ Committed:

feat(auth): add JWT-based authentication

Implemented complete authentication system with:
- User registration and login endpoints
- JWT token generation and verification
- Authentication middleware for protected routes
- Password hashing with bcrypt
- Comprehensive test coverage (35 tests, 92% coverage)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

Updated working-plan.md...
✅ Progress saved

[Feature Complete] ✅
Time: 28 minutes
Tests: 35 added, 120 existing (all passing)
Coverage: 92%
```

### Summary

**Command**: `/feature-build Add user authentication with JWT tokens`
**Duration**: 28 minutes
**Token Usage**: ~165k tokens
**Output**: Complete auth feature with 35 tests, 92% coverage, production-ready

---

## Example 2: Bug Fix - Payment Processing Error

### Scenario
Users report that payment processing fails with a 500 error when using expired credit cards.

### Command

```bash
/bug-fix Payment processing returns 500 error for expired cards
```

### Expected Workflow

#### Phase 1: Minimal Context (1 minute)

```
[Orchestrator]
Analyzing request: "Payment processing returns 500 error for expired cards"
Intent: Bug fix (keywords: "500 error", "fails")
Workflow selected: /bug-fix (progressive context loading)

[Phase 1: Minimal Context] 🔄
Loading only error logs...

Recent error logs (last 24h):
✅ Found 47 instances of error
✅ All from src/features/payments/stripe.service.ts:128
✅ Error: "Cannot read property 'status' of undefined"
✅ Timestamp pattern: Correlates with expired card attempts

Stack trace:
  at StripeService.processPayment (stripe.service.ts:128)
  at PaymentController.createPayment (payment.controller.ts:45)

[Quality Gate] ✅ PASS
- Error logs located
- Error pattern identified
- Source file pinpointed
```

#### Phase 2: Investigation (4 minutes)

```
[Phase 2: Investigation] 🔄

Parallel Intelligence Gathering:

Agent 1: Log Analysis 🔄
Analyzing error patterns...
✅ All errors occur when card.exp_year < current year
✅ No errors for valid cards
✅ Error started after Stripe API upgrade (2 days ago)

Agent 2: Code Analysis 🔄
Reading stripe.service.ts...
✅ Line 128: const status = response.paymentIntent.status
✅ Issue: Not checking if response.paymentIntent exists
✅ Stripe API change: Expired cards now return different structure

Agent 3: Test Coverage Analysis 🔄
Checking existing tests...
❌ No test for expired card scenario
❌ Missing test for Stripe API error responses

Synthesis:
Root Cause: Code assumes response.paymentIntent always exists
Stripe API change: Expired cards return response.error instead
Missing: Error handling for malformed responses

[Quality Gate] ✅ PASS
- Root cause identified
- Reproduction steps clear
- Test gap identified
```

#### Phase 3: Fix (5 minutes)

```
[Phase 3: Fix] 🔄

Launching implementer sub-agent...
Auto-invoking: test-driven-development skill

[TDD Cycle: Handle expired card error]
RED: Writing failing test...
✅ Test written: stripe.service.test.ts:145
   describe('processPayment with expired card', () => {
     it('should throw BadRequestError with clear message', async () => {
       mockStripe.paymentIntents.create.mockResolvedValue({
         error: { code: 'card_expired', message: 'Your card has expired' }
       });

       await expect(
         stripeService.processPayment(...)
       ).rejects.toThrow(BadRequestError);
     });
   });

RED: Running test...
✅ Test fails correctly: "Cannot read property 'status' of undefined"

GREEN: Implementing fix...
✅ Code updated: stripe.service.ts:120-135

Before (❌):
```typescript
const response = await stripe.paymentIntents.create({...});
const status = response.paymentIntent.status; // Crashes if paymentIntent undefined
```

After (✅):
```typescript
const response = await stripe.paymentIntents.create({...});

// Handle Stripe API errors
if (response.error) {
  throw new BadRequestError(
    response.error.message || 'Payment processing failed'
  );
}

// Safe to access paymentIntent now
const status = response.paymentIntent.status;
```

GREEN: Running test...
✅ New test passes
✅ All existing tests pass (45/45)

[Phase 3: Fix Complete] ✅
Time: 5 minutes
Files changed: 1 (stripe.service.ts)
Tests added: 3 (expired card, declined card, network error)
```

#### Phase 4: Verify (2 minutes)

```
[Phase 4: Verify] 🔄

Regression Testing:
✅ All unit tests pass (48/48, +3 new)
✅ All integration tests pass (22/22)
✅ Manual test with expired card: Returns 400 (Bad Request) with clear message
✅ Manual test with valid card: Still works (200 OK)

Quality Checks:
✅ Error handling comprehensive
✅ Error messages user-friendly
✅ Logging added for debugging
✅ No other instances of similar pattern

[Quality Gate] ✅ PASS
- Bug fixed
- Tests cover the scenario
- No regressions
```

#### Phase 5: Finalization (1 minute)

```
[Phase 5: Finalization] 🔄

Git status:
  modified:   src/features/payments/stripe.service.ts
  modified:   src/features/payments/__tests__/stripe.service.test.ts

Committing...
✅ Committed:

fix(payments): handle expired card errors correctly

Fixed 500 error when processing payments with expired cards.

Root cause: After Stripe API upgrade, expired cards return
response.error instead of response.paymentIntent, causing
undefined access.

Changes:
- Added error response checking before accessing paymentIntent
- Added user-friendly error messages
- Added tests for expired/declined/network error scenarios

Resolves #234

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>

[Bug Fix Complete] ✅
Time: 13 minutes
Token usage: ~58k tokens
```

### Summary

**Command**: `/bug-fix Payment processing returns 500 error for expired cards`
**Duration**: 13 minutes
**Token Usage**: ~58k tokens (66% less than feature-build due to progressive context)
**Output**: Bug fixed, 3 tests added, clear error messages, no regressions

---

## Example 3: Code Review - Pull Request

### Scenario
A teammate submitted a PR adding a new user profile feature. You want comprehensive review across security, quality, performance, UX, and accessibility.

### Command

```bash
/review https://github.com/yourorg/yourproject/pull/123
```

or

```bash
/review src/features/user-profile/
```

### Expected Workflow

#### Phase 1: Parallel Multi-Dimensional Analysis (5 minutes)

```
[Orchestrator]
Analyzing request: Review PR #123
Files changed: 8 files (+450, -20 lines)
- src/features/user-profile/profile.service.ts
- src/features/user-profile/profile.controller.ts
- src/features/user-profile/components/ProfileForm.tsx
- src/features/user-profile/components/AvatarUpload.tsx
- src/features/user-profile/__tests__/*

[Phase 1: Parallel Multi-Dimensional Analysis] 🔄
Launching 5 specialized reviewers in parallel...

════════════════════════════════════════════════════════
Agent 1: Security Reviewer 🔒 (5 min)
Auto-invoking: security-patterns skill

Analyzing for OWASP Top 10 vulnerabilities...

❌ CRITICAL: SQL Injection Risk
File: profile.service.ts:45
```typescript
// Current code:
const query = `SELECT * FROM profiles WHERE username = '${username}'`;
```
**Issue**: Direct string interpolation in SQL query
**OWASP**: A03:2021 - Injection
**Fix**: Use parameterized queries
**Severity**: Critical

✅ GOOD: Password Hashing
File: profile.service.ts:78
Properly using bcrypt with 10 rounds for password updates.

❌ HIGH: Missing Input Validation
File: profile.controller.ts:32
No validation on email format before saving to database.
**OWASP**: A03:2021 - Injection (via malformed input)
**Fix**: Add email validation middleware
**Severity**: High

❌ MEDIUM: Weak File Upload Validation
File: avatar.controller.ts:15
Only checking MIME type, not file content.
**OWASP**: A09:2021 - Security Logging and Monitoring Failures
**Fix**: Use file content validation (magic bytes)
**Severity**: Medium

Security Score: 6/10 (3 issues found)

════════════════════════════════════════════════════════
Agent 2: Quality Reviewer 📋 (5 min)
Auto-invoking: code-review-patterns skill

Code smell detection...

❌ HIGH: Long Method (Bloater)
File: profile.service.ts:updateProfile()
Lines: 85 (threshold: 40)
**Smell**: Method doing too many things
**Impact**: Hard to test, maintain
**Fix**: Extract methods (validateProfile, updateDatabase, sendNotification)

❌ MEDIUM: Duplicate Code
Files: ProfileForm.tsx:45-60, SettingsForm.tsx:78-93
Identical form validation logic duplicated.
**Fix**: Extract to shared useFormValidation hook

✅ GOOD: Naming Conventions
All variables and functions follow project naming conventions.

❌ LOW: Missing JSDoc
File: profile.service.ts
Public methods lack documentation comments.

Quality Score: 7/10 (3 issues found)

════════════════════════════════════════════════════════
Agent 3: Performance Analyzer ⚡ (5 min)
Auto-invoking: performance-patterns skill

Performance analysis...

❌ CRITICAL: N+1 Query Problem
File: profile.service.ts:getUserProfiles()
```typescript
// Current code:
const users = await db.query('SELECT * FROM users');
for (const user of users) {
  user.profile = await db.query('SELECT * FROM profiles WHERE user_id = ?', [user.id]);
}
```
**Issue**: N+1 queries (1 + N database calls)
**Impact**: 100 users = 101 queries (should be 1)
**Fix**: Use JOIN or batch query
**Severity**: Critical

❌ HIGH: Missing React Memoization
File: ProfileForm.tsx:useFormValidation()
Hook recreated on every render, causing child re-renders.
**Fix**: Wrap with useMemo
**Severity**: High (UX impact)

✅ GOOD: Image Optimization
Avatar images properly resized and compressed before upload.

❌ MEDIUM: Large Bundle Impact
New dependency: lodash (+70KB)
Only using 2 functions (debounce, throttle).
**Fix**: Import specific functions or use native alternatives
**Severity**: Medium

Performance Score: 6/10 (3 issues found)

════════════════════════════════════════════════════════
Agent 4: UX Reviewer 🎨 (5 min)
Auto-invoking: ux-patterns skill

User experience analysis...

❌ HIGH: Missing Loading State
File: ProfileForm.tsx:handleSubmit()
No loading indicator during save operation.
**Impact**: Users click multiple times, duplicate submissions
**Fix**: Add isLoading state + disabled button

❌ HIGH: Poor Error Messages
File: profile.controller.ts
Generic "Something went wrong" for all errors.
**Fix**: Specific messages ("Email already taken", "Username too short")

✅ GOOD: Optimistic Updates
Profile updates show immediately, rollback on error.

❌ MEDIUM: No Empty State
When user has no posts/followers, shows blank space.
**Fix**: Add encouraging empty state with CTA

❌ LOW: Missing Form Feedback
No success message after profile update.
**Fix**: Show toast notification

UX Score: 6/10 (4 issues found)

════════════════════════════════════════════════════════
Agent 5: Accessibility Reviewer ♿ (5 min)
Auto-invoking: accessibility-patterns skill

WCAG 2.1 Level AA compliance check...

❌ CRITICAL: Missing Keyboard Navigation
File: AvatarUpload.tsx:ImageCropper
Custom image cropper not keyboard accessible.
**WCAG**: 2.1.1 Keyboard (Level A)
**Impact**: Screen reader users cannot crop images
**Fix**: Add keyboard handlers (arrow keys for adjustment)

❌ HIGH: Low Color Contrast
File: ProfileForm.css:error-message
Contrast ratio: 3.2:1 (required: 4.5:1)
**WCAG**: 1.4.3 Contrast (Level AA)
**Fix**: Darken error text color to #CC0000

❌ MEDIUM: Missing ARIA Labels
File: ProfileForm.tsx:form inputs
Input fields lack aria-label or aria-describedby for errors.
**WCAG**: 4.1.2 Name, Role, Value (Level A)

✅ GOOD: Semantic HTML
Using proper <form>, <label>, <button> elements.

❌ LOW: Missing Focus Indicators
Custom button styles remove default focus outline.
**WCAG**: 2.4.7 Focus Visible (Level AA)

Accessibility Score: 5/10 (4 issues found)

════════════════════════════════════════════════════════
[Phase 1 Complete] ✅
All 5 reviewers finished in 5 minutes (parallel execution)
Sequential would take: 25 minutes (5x longer)
```

#### Phase 2: Synthesis & Prioritization (2 minutes)

```
[Phase 2: Synthesis & Prioritization] 🔄

Consolidating findings from 5 reviewers...

## Critical Issues (BLOCK MERGE) 🚨

1. **SQL Injection** (Security)
   - File: profile.service.ts:45
   - Impact: Database compromise, data theft
   - Fix effort: 5 minutes
   - Auto-fixable: ✅ Yes

2. **N+1 Query Problem** (Performance)
   - File: profile.service.ts:getUserProfiles()
   - Impact: 100x slower with scale
   - Fix effort: 10 minutes
   - Auto-fixable: ✅ Yes

3. **Keyboard Navigation** (Accessibility)
   - File: AvatarUpload.tsx
   - Impact: Feature unusable for 15% of users
   - Fix effort: 20 minutes
   - Auto-fixable: ❌ No (requires UX design)

## High Priority (FIX BEFORE MERGE) ⚠️

4. Missing input validation (Security) - 5 min - ✅ Auto-fixable
5. Long method (Quality) - 15 min - ✅ Auto-fixable
6. Missing React memoization (Performance) - 5 min - ✅ Auto-fixable
7. Missing loading state (UX) - 10 min - ✅ Auto-fixable
8. Poor error messages (UX) - 10 min - ✅ Auto-fixable
9. Low color contrast (Accessibility) - 2 min - ✅ Auto-fixable

## Medium Priority (CAN FIX LATER) 📋

10. Weak file upload validation (Security)
11. Duplicate code (Quality)
12. Large bundle impact (Performance)
13. No empty state (UX)
14. Missing ARIA labels (Accessibility)

## Summary

**Total Issues**: 14
**Critical**: 3 (2 auto-fixable)
**High**: 6 (all auto-fixable)
**Medium**: 5 (3 auto-fixable)

**Auto-fix Available**: 11 issues (~60 minutes if sequential, ~20 minutes with checkpoints)
**Manual Fix Required**: 3 issues (keyboard nav, empty state, comprehensive accessibility)

**Recommendation**: ❌ Do not merge until Critical and High issues resolved.
```

#### Phase 3: Optional Auto-Fix (Conditional, 20 minutes)

```
[Phase 3: Optional Auto-Fix] 🔄

User choice: Apply safe auto-fixes? [y/N] y

Applying fixes with checkpoint strategy...

Fix 1/11: SQL Injection → Parameterized Query
✅ Applied fix to profile.service.ts:45
✅ Running tests... All pass (35/35)
✅ Git checkpoint: "fix(security): use parameterized query for username lookup"

Fix 2/11: N+1 Query → JOIN Query
✅ Applied fix to profile.service.ts:getUserProfiles()
✅ Running tests... All pass (35/35)
✅ Git checkpoint: "fix(perf): eliminate N+1 query with JOIN"

Fix 3/11: Input Validation → Zod Schema
✅ Applied validation middleware
✅ Running tests... All pass (38/38, +3 validation tests)
✅ Git checkpoint: "fix(security): add input validation for profile endpoints"

[... continues through all auto-fixable issues ...]

Fix 11/11: Color Contrast → Updated CSS
✅ Applied contrast fix
✅ Running accessibility tests... All pass
✅ Git checkpoint: "fix(a11y): improve error message color contrast"

[Phase 3: Auto-Fix Complete] ✅
Fixed: 11/14 issues
Remaining: 3 manual fixes required
Time: 18 minutes
All tests passing: 45/45
```

#### Final Report

```
══════════════════════════════════════════════════════
📊 CODE REVIEW COMPLETE - PR #123
══════════════════════════════════════════════════════

⏱️ **Review Time**: 25 minutes (5 min analysis + 2 min synthesis + 18 min auto-fix)
🤖 **Reviewers**: 5 specialized agents (parallel execution)
📁 **Files Reviewed**: 8 files (+450, -20 lines)

══════════════════════════════════════════════════════
✅ **AUTO-FIXED** (11 issues)
══════════════════════════════════════════════════════

Security (2):
✅ SQL injection → Parameterized queries
✅ Missing input validation → Zod schemas

Performance (2):
✅ N+1 query → JOIN query
✅ Missing memoization → useMemo added

Quality (2):
✅ Long method → Extracted 3 helper methods
✅ Missing JSDoc → Added documentation

UX (3):
✅ Missing loading state → Added isLoading
✅ Poor error messages → Specific messages
✅ Missing success feedback → Toast notifications

Accessibility (2):
✅ Color contrast → Updated to 4.8:1
✅ Missing focus indicators → Added visible outlines

══════════════════════════════════════════════════════
⚠️ **MANUAL FIX REQUIRED** (3 issues)
══════════════════════════════════════════════════════

1. ❌ Keyboard navigation for image cropper (Accessibility - Critical)
   → Requires UX design for keyboard controls

2. ❌ Empty state design (UX - Medium)
   → Requires mockups/design

3. ❌ File content validation (Security - Medium)
   → Requires magic bytes library integration

══════════════════════════════════════════════════════
📈 **SCORES** (After Auto-Fix)
══════════════════════════════════════════════════════

Security: 6/10 → 9/10 ✅ (+3)
Quality: 7/10 → 9/10 ✅ (+2)
Performance: 6/10 → 9/10 ✅ (+3)
UX: 6/10 → 8/10 ✅ (+2)
Accessibility: 5/10 → 7/10 ⚠️ (+2, keyboard nav still needed)

══════════════════════════════════════════════════════
✅ **RECOMMENDATION**: Merge after addressing 3 manual fixes
══════════════════════════════════════════════════════

Next steps:
1. Design keyboard navigation for image cropper (Critical)
2. Create empty state designs
3. Add file content validation library

Commits created: 11 (one per fix, all tested)
Tests added: 8 new tests
All tests passing: 45/45 ✅
```

### Summary

**Command**: `/review https://github.com/yourorg/yourproject/pull/123`
**Duration**: 25 minutes (5 parallel + 2 synthesis + 18 auto-fix)
**Token Usage**: ~42k tokens
**Output**: 11 issues auto-fixed, 3 flagged for manual review, comprehensive multi-dimensional analysis
**Key Benefit**: 67% faster than sequential review (25 min vs 75 min)

---

## Example 4: Feature Build - API Endpoint

### Scenario
Quick example: Adding a simple GET endpoint to fetch user statistics.

### Command

```bash
/feature-build Add GET /api/users/:id/stats endpoint
```

### Expected Output (Abbreviated)

```
[Phase 1: Context Analysis] ✅ (1 min)
Found similar: /api/users/:id/profile
Pattern: Express + TypeScript

[Phase 2: Planning] ✅ (2 min)
Files: stats.service.ts, stats.controller.ts, stats.routes.ts
Tests: stats.test.ts

[Phase 3: Implementation] ✅ (8 min)
Task 1: Service (3 min) - ✅ 5 tests passing
Task 2: Controller (3 min) - ✅ 8 tests passing
Task 3: Routes (2 min) - ✅ Registered

[Phase 4: Verification] ✅ (1 min)
All tests pass: 13/13

[Phase 5: Finalization] ✅ (1 min)
Committed: "feat(users): add user statistics endpoint"

Total: 13 minutes
```

---

## Example 5: Bug Fix - Memory Leak

### Scenario
React component causing memory leak due to missing cleanup.

### Command

```bash
/bug-fix Memory leak in UserDashboard component
```

### Expected Output (Abbreviated)

```
[Phase 1: Context] ✅ (1 min)
Error logs: "Maximum update depth exceeded"
Component: UserDashboard.tsx

[Phase 2: Investigation] ✅ (3 min)
Root cause: WebSocket connection not cleaned up
Missing: useEffect cleanup function

[Phase 3: Fix] ✅ (4 min)
RED: Test for cleanup
GREEN: Added return () => ws.close()
✅ Test passes

[Phase 4: Verify] ✅ (1 min)
No memory leak in profiler
All tests pass

[Phase 5: Finalization] ✅ (1 min)
Committed: "fix(dashboard): cleanup WebSocket on unmount"

Total: 10 minutes
```

---

## Tips for Using cc10x

### 1. Be Specific in Commands

❌ Bad: `/feature-build Add authentication`
✅ Good: `/feature-build Add JWT-based authentication with email/password login`

### 2. Trust the Process

The orchestrator knows when to use parallel vs sequential execution. Don't override unless you have a specific reason.

### 3. Review Quality Gates

If a quality gate fails, address the issue before proceeding. Skipping gates leads to bugs in production.

### 4. Leverage Auto-Fix

For `/review`, auto-fix handles 80% of issues automatically. Focus your time on the 20% that need design decisions.

### 5. Keep Working Plan Updated

The orchestrator uses `working-plan.md` to maintain context. Keep it updated with current priorities.

---

## Next Steps

- Try running `/feature-build` on a small feature in your project
- Use `/bug-fix` for your next bug investigation
- Run `/review` on your next pull request

See [README.md](README.md) for full documentation.
