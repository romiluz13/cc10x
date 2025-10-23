---
name: feature-plan
description: Creates comprehensive PRD-style feature plans with architecture decisions, edge cases, API design, data models, implementation roadmap, and automatic pattern discovery (93% token savings via progressive loading)
aliases: [plan, planning, design]
category: planning
priority: 9
---

# Feature Planning Command

Create production-ready feature plans before writing any code. This command generates comprehensive Product Requirements Document (PRD) style specifications that include user stories, architecture decisions, component breakdowns, API designs, data models, edge cases, testing strategies, and implementation roadmaps.

Perfect for starting new features with clarity and avoiding costly rework.

## What This Does

This command orchestrates comprehensive feature planning with:

- **User Story Analysis** - Converts high-level ideas into detailed user stories with acceptance criteria
- **Architecture Decisions** - Evaluates patterns, proposes solutions, justifies technology choices
- **Component Breakdown** - Identifies all components, services, and modules needed
- **API Design** - Specifies endpoints, request/response formats, error handling
- **Data Model Design** - Defines schemas, relationships, indexes, constraints
- **Edge Case Identification** - Proactively finds error conditions, edge cases, failure modes
- **Testing Strategy** - Plans unit, integration, and E2E tests before implementation
- **Implementation Roadmap** - Creates phased, iterative development plan
- **Progressive Loading** - Loads only necessary context (saves 93% tokens vs full codebase scan)

## When to Use

Use `/feature-plan` when you need to:

- **Start a new feature** - Before writing any code, create a comprehensive plan
- **Clarify requirements** - Transform vague ideas into concrete specifications
- **Evaluate approaches** - Compare multiple solutions before committing
- **Align with team** - Create documentation for review and discussion
- **Estimate complexity** - Understand scope before committing to timelines
- **Avoid rework** - Identify problems before implementation

**Don't use when:**
- Feature is already fully planned (use `/feature-build` instead)
- Making tiny changes (under 50 lines)
- Just exploring code (use codebase search)

## Workflow

### Phase 1: Requirements Gathering

**Goal:** Understand the feature request and extract key requirements

**Process:**
1. Parse user's feature description
2. Identify core functionality
3. Extract implied requirements
4. List assumptions to validate
5. Generate clarifying questions if needed

**Quality Gate:** Clear understanding of what feature should do

**Example Output:**
```markdown
## Requirements Summary
- **Core Need:** User authentication with JWT tokens
- **Primary Users:** Web app users (authenticated access)
- **Key Flows:** Login, registration, logout, token refresh
- **Assumptions:** Email-based auth, password hashing with bcrypt
```

---

### Phase 2: Context Analysis

**Goal:** Find similar patterns in codebase to follow project conventions

**Process:**
1. Search for similar features in project
2. Identify naming conventions
3. Find existing patterns (error handling, validation, etc.)
4. Map integration points (database, APIs, services)
5. Note dependencies and constraints

**Quality Gate:** Understanding of project patterns and conventions

**Example Output:**
```markdown
## Existing Patterns Found
- **Auth Pattern:** src/middleware/auth.ts uses JWT verification
- **Error Handling:** Custom AppError class in src/errors/
- **Database:** MongoDB with Mongoose schemas in src/models/
- **Validation:** Joi schemas in src/validators/
- **API Structure:** RESTful endpoints in src/routes/
```

---

### Phase 3: Architecture & Design

**Goal:** Create comprehensive technical specification

**Process:**
1. **User Stories**
   - Write detailed user stories with acceptance criteria
   - Include happy paths and error scenarios
   
2. **Architecture Decisions**
   - Evaluate approaches (pros/cons of each)
   - Choose solution with justification
   - Document trade-offs
   
3. **Component Design**
   - List all components needed
   - Define responsibilities
   - Map interactions
   
4. **API Design**
   - Specify all endpoints
   - Define request/response formats
   - Document error codes
   
5. **Data Model**
   - Design database schemas
   - Define relationships and indexes
   - Plan migrations if needed
   
6. **Edge Cases**
   - Identify failure modes
   - Plan error handling
   - Consider security implications

**Quality Gate:** Complete specification ready for review

**Example Output:**
```markdown
## Architecture Decision

### Approach: JWT-based stateless authentication

**Why this approach:**
- ✅ Scalable (no server-side session storage)
- ✅ Matches existing pattern in codebase
- ✅ Works with current React frontend
- ✅ Industry standard

**Alternatives considered:**
- Session-based auth: Requires Redis, adds complexity
- OAuth only: Need our own auth too (not just 3rd party)

### Components

1. **AuthController** (src/controllers/auth.ts)
   - Handles login, register, logout endpoints
   - Validates credentials
   - Issues JWT tokens
   
2. **AuthMiddleware** (src/middleware/auth.ts)  
   - Verifies JWT on protected routes
   - Extracts user from token
   - Handles token expiration
   
3. **User Model** (src/models/user.ts)
   - Stores user credentials
   - Hashes passwords with bcrypt
   - Validates email format

### API Endpoints

**POST /api/auth/register**
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}

Response (201):
{
  "success": true,
  "data": {
    "user": { "id": "...", "email": "...", "name": "..." },
    "token": "eyJhbGc..."
  }
}

Errors:
- 400: Invalid email or weak password
- 409: Email already registered
```

[Continue for all endpoints...]

### Data Model

```typescript
User Schema:
{
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true, select: false },
  name: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
  lastLogin: { type: Date }
}

Indexes:
- email (unique)
```

### Edge Cases

1. **Expired Token**: Return 401, client refreshes
2. **Concurrent Logins**: Allow (stateless, multiple devices OK)
3. **Password Reset**: Not in v1 (add in v2)
4. **Rate Limiting**: 5 failed login attempts → 15min lockout
5. **SQL Injection**: Using Mongoose (protected), but validate anyway
```

---

### Phase 4: Testing Strategy

**Goal:** Plan all tests before implementation (TDD preparation)

**Process:**
1. List all unit tests needed
2. Identify integration test scenarios
3. Plan E2E test cases
4. Document test data requirements
5. Specify coverage targets (>80%)

**Quality Gate:** Complete test plan ready for TDD

**Example Output:**
```markdown
## Test Plan

### Unit Tests (target: 90% coverage)

**AuthController:**
- ✓ Register with valid data creates user
- ✓ Register with duplicate email returns 409
- ✓ Register with invalid email returns 400
- ✓ Register with weak password returns 400
- ✓ Login with correct credentials returns token
- ✓ Login with wrong password returns 401
- ✓ Login with non-existent email returns 401

**AuthMiddleware:**
- ✓ Valid token allows request
- ✓ Expired token returns 401
- ✓ Malformed token returns 401
- ✓ Missing token returns 401
- ✓ User from token attached to req.user

**User Model:**
- ✓ Password is hashed before save
- ✓ comparePassword method works correctly
- ✓ Password is excluded from queries
- ✓ Email validation works

### Integration Tests

- ✓ Register → Login → Access Protected Route (full flow)
- ✓ Register → Logout → Access Protected Route (should fail)
- ✓ Login → Token Expires → Access Protected (should fail)

### E2E Tests

- ✓ User can register and login via UI
- ✓ Protected pages redirect to login when not authenticated
- ✓ User can logout and session ends
```

---

### Phase 5: Implementation Roadmap

**Goal:** Create step-by-step implementation plan

**Process:**
1. Break feature into small, testable increments
2. Order by dependencies (what needs what)
3. Identify parallel vs sequential work
4. Estimate complexity for each step
5. Define "done" criteria for each increment

**Quality Gate:** Clear, actionable roadmap ready for implementation

**Example Output:**
```markdown
## Implementation Phases

### Increment 1: User Model & Basic Registration (2-3 hours)
**Goal:** Users can register (no login yet)

**Tasks:**
1. Create User schema (src/models/user.ts)
2. Add password hashing with bcrypt
3. Write unit tests for User model
4. Create POST /api/auth/register endpoint
5. Write tests for registration
6. Validate email format and password strength

**Done when:** 
- Users can register via API
- Passwords are hashed
- All tests pass (>80% coverage)

---

### Increment 2: Login & JWT (2-3 hours)
**Goal:** Users can login and receive token

**Tasks:**
1. Install jsonwebtoken package
2. Create JWT signing helper
3. Add POST /api/auth/login endpoint
4. Write tests for login flow
5. Return token on successful login
6. Handle invalid credentials

**Done when:**
- Users can login via API
- Valid JWT returned
- All tests pass

---

### Increment 3: Auth Middleware (1-2 hours)
**Goal:** Protected routes work

**Tasks:**
1. Create auth middleware (src/middleware/auth.ts)
2. Verify JWT and extract user
3. Handle token expiration
4. Write middleware tests
5. Apply to protected routes

**Done when:**
- Protected routes require valid token
- Expired tokens rejected
- All tests pass

---

### Increment 4: Frontend Integration (3-4 hours)
**Goal:** UI can login/register

**Tasks:**
1. Create login form component
2. Create registration form component
3. Add auth context/state management
4. Store token in localStorage
5. Add token to API requests
6. Handle logout

**Done when:**
- Users can login/register via UI
- Token persists across page refresh
- Logout clears token

---

### Increment 5: Edge Cases & Polish (2-3 hours)
**Goal:** Production-ready

**Tasks:**
1. Add rate limiting (5 failed attempts)
2. Add input sanitization
3. Improve error messages
4. Add logging for security events
5. Write E2E tests
6. Update documentation

**Done when:**
- All edge cases handled
- Security hardened
- E2E tests pass
- Ready for production
```

---

## Examples

### Example 1: Authentication Feature

**Input:**
```bash
/feature-plan Add user authentication with JWT tokens
```

**Process:**
1. Analyzes requirement: "user authentication with JWT"
2. Finds existing auth patterns in codebase
3. Designs JWT-based stateless auth
4. Specifies User model, AuthController, AuthMiddleware
5. Defines API endpoints (register, login, logout)
6. Plans comprehensive test coverage
7. Creates 5-increment implementation roadmap

**Output:**
```
✅ Feature Plan Created: USER_AUTHENTICATION.md

## Summary
- **User Stories:** 3 (Register, Login, Access Protected Resources)
- **Components:** 3 (User Model, AuthController, AuthMiddleware)
- **API Endpoints:** 3 (POST /register, POST /login, POST /logout)
- **Data Models:** 1 (User with email, password, name)
- **Edge Cases:** 8 identified and planned
- **Tests:** 25 unit + 3 integration + 3 E2E
- **Increments:** 5 phases, 10-15 hours total
- **Confidence:** High (follows existing patterns)

📝 Next step: Review plan, then run /feature-build to implement
```

---

### Example 2: Real-time Notifications

**Input:**
```bash
/feature-plan Add real-time notifications using WebSockets
```

**Process:**
1. Analyzes requirement: "real-time notifications with WebSockets"
2. Searches codebase for existing real-time features (finds none)
3. Evaluates WebSocket libraries (Socket.io vs ws)
4. Designs notification system architecture
5. Plans server-side event handling and client-side subscriptions
6. Identifies edge cases (reconnection, missed notifications)
7. Creates incremental implementation plan

**Output:**
```
✅ Feature Plan Created: REALTIME_NOTIFICATIONS.md

## Summary
- **User Stories:** 4 (Receive notifications, View history, Mark as read, Subscribe to events)
- **Components:** 5 (WebSocket Server, NotificationService, NotificationModel, Client Manager, UI Components)
- **Architecture Decision:** Socket.io (easier than ws, has reconnection built-in)
- **Data Models:** 2 (Notification, UserSubscription)
- **Edge Cases:** 12 identified (reconnection, offline handling, duplicate events, etc.)
- **Tests:** 35 unit + 5 integration + 4 E2E
- **Increments:** 7 phases, 20-25 hours total
- **Confidence:** Medium (new pattern for this project, needs research)

⚠️  Recommendation: Review Socket.io docs before implementation
📝 Next step: Review plan, then run /feature-build to implement
```

---

### Example 3: Payment Integration

**Input:**
```bash
/feature-plan Integrate Stripe payment processing for subscription billing
```

**Process:**
1. Analyzes requirement: "Stripe payment processing for subscriptions"
2. Searches codebase for existing payment code (finds none)
3. Reviews Stripe API patterns and webhook handling
4. Designs subscription management system
5. Plans webhook security (signature verification)
6. Identifies critical edge cases (failed payments, cancellations, refunds)
7. Creates comprehensive test plan including Stripe test mode

**Output:**
```
✅ Feature Plan Created: STRIPE_SUBSCRIPTIONS.md

## Summary
- **User Stories:** 6 (Subscribe, Cancel, Update card, View invoices, Handle failed payment, Admin refunds)
- **Components:** 7 (StripeService, WebhookController, Subscription Model, Payment Model, etc.)
- **API Endpoints:** 8 (create subscription, cancel, update card, webhooks, etc.)
- **Data Models:** 3 (Subscription, PaymentMethod, Invoice)
- **Webhooks:** 6 events to handle (invoice.paid, invoice.payment_failed, customer.subscription.deleted, etc.)
- **Edge Cases:** 15 identified (failed payments, double billing, prorated charges, etc.)
- **Security:** Webhook signature verification, PCI compliance considerations
- **Tests:** 45 unit + 8 integration + 6 E2E (using Stripe test mode)
- **Increments:** 8 phases, 30-35 hours total
- **Confidence:** Medium-Low (complex third-party integration)

⚠️  CRITICAL: Must handle webhooks correctly (financial data!)
⚠️  RECOMMENDATION: Test thoroughly in Stripe test mode before production
📝 Next step: Review Stripe docs, then review plan, then implement carefully
```

---

## Best Practices

### 1. **Plan Before Building**
Always run `/feature-plan` before `/feature-build`. The 1-2 hours spent planning saves 5-10 hours of rework.

### 2. **Review the Plan**
Don't blindly implement. Read the generated plan, validate assumptions, adjust as needed.

### 3. **Share with Team**
Use the plan document for code reviews, team discussions, and stakeholder alignment.

### 4. **Update as You Learn**
If you discover issues during implementation, update the plan. Keep it as living documentation.

### 5. **Consider Incremental Delivery**
Follow the roadmap's increments. Ship value early and often instead of big-bang releases.

### 6. **Don't Skip Edge Cases**
The plan identifies edge cases. Don't ignore them. Handle them in implementation or explicitly defer to v2.

### 7. **Trust the Architecture Decisions**
The plan evaluates alternatives and justifies choices. Trust the analysis unless you have new information.

---

## Common Issues

### Issue: Plan is too generic

**Symptom:** Plan doesn't match your project's patterns

**Cause:** Insufficient codebase context

**Solution:**
1. Be more specific in your request: `/feature-plan Add JWT auth using existing User model in src/models/`
2. The command automatically searches for patterns, but explicit guidance helps
3. Review "Context Analysis" section - if it's empty, no patterns were found

---

### Issue: Plan is too detailed / too simple

**Symptom:** Plan is overwhelming or too basic

**Cause:** Feature complexity mismatch

**Solution:**
- **Too detailed:** Break feature into smaller pieces: `/feature-plan Add login endpoint only`
- **Too simple:** Combine features: `/feature-plan Complete auth system with login, register, logout, password reset`
- The command adapts to complexity, but you control scope

---

### Issue: Missing important consideration

**Symptom:** Plan doesn't address security/performance/scalability concern

**Cause:** Context not captured in initial request

**Solution:**
1. Add constraints to request: `/feature-plan Add auth with rate limiting and brute force protection`
2. Edit the generated plan to add the concern
3. Run `/review` after implementation to catch issues

---

### Issue: Plan conflicts with existing code

**Symptom:** Suggested approach doesn't work with current architecture

**Cause:** Context analysis found wrong pattern or codebase changed

**Solution:**
1. Review "Context Analysis" section of plan
2. Override with explicit guidance: `/feature-plan Add auth using Express sessions (NOT JWT)`
3. Edit plan before running `/feature-build`

---

### Issue: Uncertain about estimates

**Symptom:** Roadmap time estimates seem off

**Cause:** Estimates are educated guesses based on complexity

**Solution:**
- Estimates are ranges (2-3 hours, 5-8 hours)
- Your experience may vary based on skill level and codebase familiarity
- Track actual time and adjust future estimates
- Use estimates for prioritization, not commitments

---

## Related Commands

### `/feature-build`
**Use after** `/feature-plan` to implement the planned feature with strict TDD.

**Example workflow:**
```bash
/feature-plan Add user authentication
# Review generated plan...
/feature-build Implement user authentication based on plan
```

---

### `/review`
**Use after** implementation to validate the feature with multi-dimensional review.

**Example workflow:**
```bash
/feature-plan Add payment processing
/feature-build Implement payment processing
/review src/payment/  # Security, quality, performance, UX, accessibility
```

---

### `/bug-fix`
**Use instead of** `/feature-plan` when fixing issues, not building features.

**When to use which:**
- New functionality → `/feature-plan`
- Existing functionality broken → `/bug-fix`

---

## Output Format

The `/feature-plan` command generates a markdown document (e.g., `FEATURE_AUTH.md`) containing:

1. **Executive Summary** - One-paragraph overview
2. **Requirements** - Core needs, assumptions, constraints
3. **Context Analysis** - Existing patterns found in codebase
4. **User Stories** - Detailed stories with acceptance criteria
5. **Architecture Decisions** - Chosen approach with justification
6. **Component Design** - All components with responsibilities
7. **API Specification** - Endpoints, requests, responses, errors
8. **Data Models** - Schemas, relationships, indexes
9. **Edge Cases** - Failure modes and handling strategies
10. **Testing Strategy** - Unit, integration, E2E test plans
11. **Implementation Roadmap** - Phased, incremental plan
12. **Notes** - Additional considerations, risks, dependencies

---

## Configuration

This command uses progressive loading (saves 93% tokens):

- **Stage 1:** Loads only planning skill and metadata (~50 tokens)
- **Stage 2:** Loads relevant context based on feature request (~500 tokens)
- **Stage 3:** Deep-loads only files/components mentioned (~variable)

Total: ~1,000 tokens average vs ~15,000 for full codebase scan

---

## Success Metrics

A good feature plan has:

- ✅ **Clear Requirements** - No ambiguity about what to build
- ✅ **Architecture Justification** - Why this approach over alternatives
- ✅ **Complete Component List** - Nothing missing
- ✅ **Detailed API Specs** - Implementation-ready
- ✅ **Edge Case Coverage** - All failure modes identified
- ✅ **Comprehensive Test Plan** - Ready for TDD
- ✅ **Incremental Roadmap** - Ship value iteratively
- ✅ **Confidence Level** - Honest assessment of uncertainty

**If plan is missing any of these, it's not ready for implementation.**

---

## Notes

- Planning takes 1-2 hours but saves 5-10 hours of rework
- Plans are living documents - update as you learn
- Share plans with team for alignment
- Don't skip planning for "simple" features - they're never as simple as they seem
- The best time to find problems is before writing code

