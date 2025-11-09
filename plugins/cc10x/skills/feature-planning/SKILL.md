---
name: feature-planning
description: Provides feature planning guidance with functionality-first approach. Use PROACTIVELY when planning features. First understands functionality (user flow, admin flow, system flow, integration flow), then gathers requirements and prepares implementation plans. Focuses on planning functionality, not generic feature planning. Used by the planning workflow and related subagents.
allowed-tools: Read, Grep, Glob
---

# Feature Planning Guidance - Functionality First

## Functionality First Mandate

**BEFORE planning features, understand functionality**:

1. **What functionality needs to be planned?**
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?
   - What are the integration flows?

2. **THEN plan** - Plan features to support that functionality

3. **Use frameworks** - Apply planning frameworks AFTER functionality is understood

---

## Purpose

Support structured feature planning with concrete templates, examples, and decision frameworks. Ensure requirements are testable, architecture is clear, risks are mitigated, and implementation is phased.

---

## Stage 1: Complexity Assessment

### Complexity Rubric (1-5)

Use this rubric to determine if comprehensive planning is warranted:

**1 - Trivial** (<50 LOC, single function, no dependencies)

- Examples: Add validation helper, format date string
- Recommendation: Implement directly, no planning needed

**2 - Simple** (50-200 LOC, single file, minimal risk)

- Examples: Add form field, update CSS styling
- Recommendation: Brief planning (5-10 min), implement

**3 - Moderate** (200-500 LOC, 2-5 files, adds/updates tests)

- Examples: Add API endpoint, create new component
- Recommendation: Planning workflow valuable, ~30 min

**4 - Complex** (500+ LOC, 5-10 files, novel patterns or integrations)

- Examples: Authentication flow, payment integration
- Recommendation: Comprehensive planning critical, ~1-2 hours

**5 - Architectural** (1000+ LOC, 10+ files, cross-cutting changes)

- Examples: Database migration, microservice split
- Recommendation: Multi-stage planning with approval gates

**Decision Point**: If complexity ≤2, confirm with user before proceeding with full planning.

---

## Stage 2: Requirements Gathering

### Requirements Template

```markdown
## Requirements

**Goal**: <One-sentence summary of what we're building and why>

**Stakeholders**:

- <Role>: <Name/Team> - <What they care about>

**User Stories**:
As a <role>, I want <capability> so that <business value>.

**Acceptance Criteria** (testable):

- [ ] <Specific, measurable criterion>
- [ ] <Specific, measurable criterion>

**Out of Scope** (what we're NOT doing):

- <Feature or capability explicitly excluded>

**Assumptions**:

- <Assumption that could affect design>

**Open Questions**:

- <Question requiring stakeholder input>
```

### Populated Example: User Authentication

```markdown
## Requirements

**Goal**: Allow users to create accounts and log in securely using email/password.

**Stakeholders**:

- Product: Sarah - Wants seamless onboarding, <2s login time
- Security: Mike - Requires bcrypt hashing, rate limiting
- Support: Lisa - Needs clear error messages for troubleshooting

**User Stories**:

- As a new user, I want to create an account with email/password so that I can access personalized features.
- As a returning user, I want to log in quickly so that I can resume my work.
- As a security-conscious user, I want my password to be securely hashed so that my account is protected.

**Acceptance Criteria**:

- [ ] User can register with valid email (format validated)
- [ ] Password must be 12+ chars with upper, lower, number, symbol
- [ ] Passwords hashed with bcrypt (12 rounds)
- [ ] Login rate limited to 5 attempts per 15 minutes
- [ ] JWT token issued on successful login
- [ ] Token expires after 7 days
- [ ] Clear error messages (e.g., "Invalid credentials", not "Wrong password")

**Out of Scope**:

- Social login (Google, GitHub) - Phase 2
- Two-factor authentication - Phase 2
- Password reset via email - Phase 2

**Assumptions**:

- MongoDB for user storage
- JWT for session management (stateless)
- No existing authentication system to migrate from

**Open Questions**:

- Should we support "remember me" functionality? (extends token to 30 days)
- Password strength indicator on registration form?
```

---

## Stage 3: Architecture Design

### Architecture Template

````markdown
## Architecture

**System Context**:
<High-level: External actors → System → External services>

**Containers** (services, databases):

- <Container name>: <Technology> - <Purpose>

**Components** (within container):

- <Component>: <Responsibility> - <Key interfaces>

**Data Models**:

```typescript
// Entity definitions
```
````

**Key Decisions**:

- <Decision>: <Rationale> - <Trade-offs>

**Integration Points**:

- <External service>: <How we integrate> - <Error handling>

````

### Populated Example: User Authentication

```markdown
## Architecture

**System Context**:
User (Browser) → API (Node.js) → Database (MongoDB)

**Containers**:
- API: Node.js/Express - Handles authentication routes
- Database: MongoDB - Stores user credentials
- Cache: Redis (future) - Session invalidation (out of scope Phase 1)

**Components**:
- AuthController: Handles /register and /login endpoints
  - registerUser(email, password) → {userId, token}
  - loginUser(email, password) → {userId, token}
- AuthService: Business logic for authentication
  - hashPassword(plaintext) → hash
  - verifyPassword(plaintext, hash) → boolean
  - generateToken(userId) → JWT string
- UserRepository: Database operations
  - createUser(email, hashedPassword) → User
  - findUserByEmail(email) → User | null

**Data Models**:
```typescript
interface User {
  _id: ObjectId;
  email: string;           // Unique, indexed
  hashedPassword: string;  // Bcrypt hash
  createdAt: Date;
  lastLoginAt: Date | null;
}

interface JWT {
  userId: string;
  iat: number;  // Issued at
  exp: number;  // Expires (7 days)
}
````

**Key Decisions**:

- **JWT vs Sessions**: JWT (stateless, no Redis needed Phase 1)
  - Trade-off: Can't instantly revoke tokens, but simpler infrastructure
  - Mitigation: Short expiry (7 days), add Redis invalidation in Phase 2
- **Bcrypt vs Argon2**: Bcrypt (industry standard, proven)
  - Trade-off: Argon2 slightly more secure, but less ecosystem support
- **MongoDB vs PostgreSQL**: MongoDB (team familiarity, flexible schema)
  - Risk: NoSQL injection if not careful (mitigation: type validation)

**Integration Points**:

- Email service (future): Password reset emails - Phase 2
- Rate limiter: Express-rate-limit middleware
  - Error handling: Return 429 Too Many Requests

````

---

## Stage 4: Risk Analysis

### Risk Register Template

```markdown
## Risks

| Stage | Risk Description | Probability | Impact | Mitigation | Owner |
|-------|------------------|-------------|--------|-----------|-------|
| <Framework stage> | <What could go wrong> | H/M/L | H/M/L | <How we'll prevent/handle> | <Team/person> |
````

### Populated Example: User Authentication

```markdown
## Risks

| Stage         | Risk Description                        | Probability | Impact   | Mitigation                                                                | Owner   |
| ------------- | --------------------------------------- | ----------- | -------- | ------------------------------------------------------------------------- | ------- |
| Security      | NoSQL injection via email field         | Medium      | High     | Validate input type (must be string), use parameterized queries           | Backend |
| Security      | Brute force password guessing           | High        | High     | Rate limit 5 attempts/15min, lock account after 10 failed attempts        | Backend |
| Security      | JWT secret leaked                       | Low         | Critical | Store in env var, rotate every 90 days, never commit to git               | DevOps  |
| UX            | Vague error messages help attackers     | Medium      | Medium   | Generic "Invalid credentials" message (don't reveal if email exists)      | Backend |
| Performance   | Bcrypt hashing blocks event loop        | Medium      | Medium   | Use bcrypt.hash (async), not bcrypt.hashSync                              | Backend |
| Data Flow     | Password sent over HTTP (not HTTPS)     | Low         | Critical | Enforce HTTPS in production, redirect HTTP → HTTPS                        | DevOps  |
| Failure Modes | MongoDB connection failure during login | Low         | High     | Retry logic (3 attempts), graceful error "Service unavailable, try again" | Backend |
```

### Risk Scoring Guide

**Probability**:

- High: Likely to occur (>50% chance)
- Medium: Could occur (10-50%)
- Low: Unlikely (<10%)

**Impact**:

- High: System unusable, data loss, security breach
- Medium: Degraded performance, user frustration
- Low: Minor inconvenience, easy workaround

**Priority** = Probability × Impact

- High × High = P0 (must address before launch)
- High × Medium or Medium × High = P1 (address before launch if possible)
- All others = P2 (monitor and address post-launch)

---

## Stage 5: Implementation Plan

### Implementation Roadmap Template

```markdown
## Implementation Plan

**Phase 1**: <Summary>

- **Files to Create**: <list>
- **Files to Modify**: <list>
- **Tests to Add**: <list>
- **Exit Criteria**: <How we know this phase is done>
- **Estimated Time**: <hours/days>

**Phase 2**: <Summary>
...

**Testing Strategy**:

- Unit tests: <what to test>
- Integration tests: <what to test>
- E2E tests: <what to test>

**Deployment Strategy**:

- Risk level: <ZERO/LOW/MEDIUM/HIGH>
- Rollout plan: <feature flag? canary? immediate?>
- Rollback plan: <how to undo if it breaks>
```

### Populated Example: User Authentication

```markdown
## Implementation Plan

**Phase 1: Core Authentication** (Complexity: 4)

- **Files to Create**:
  - `src/auth/auth.controller.ts` - Express routes
  - `src/auth/auth.service.ts` - Business logic
  - `src/auth/auth.middleware.ts` - JWT verification
  - `src/models/user.model.ts` - MongoDB schema
  - `src/repositories/user.repository.ts` - DB operations
  - `tests/auth.spec.ts` - Unit tests
  - `tests/integration/auth.integration.spec.ts` - Integration tests
- **Files to Modify**:
  - `src/app.ts` - Register auth routes
  - `src/config/database.ts` - Add User collection
  - `.env.example` - Add JWT_SECRET, BCRYPT_ROUNDS
- **Tests to Add**:
  - Unit: hashPassword, verifyPassword, generateToken
  - Integration: POST /register, POST /login (success and failure cases)
  - E2E: Full registration → login flow
- **Exit Criteria**:
  - All tests passing (100% coverage for auth module)
  - Manual test: Register + login works in staging
  - Rate limiting verified (5 attempts then blocked)
- **Estimated Time**: 8-12 hours

**Phase 2: Rate Limiting & Error Handling**

- **Files to Create**:
  - `src/middleware/rate-limiter.ts`
  - `src/utils/error-responses.ts`
- **Files to Modify**:
  - `src/auth/auth.controller.ts` - Add rate limiter middleware
- **Exit Criteria**:
  - Rate limiter blocks after 5 attempts
  - Error messages are user-friendly and secure
- **Estimated Time**: 2-3 hours

**Phase 3: Deployment**

- Feature flag: `AUTH_ENABLED=true`
- Rollout: LOW-RISK (new feature, no existing users)
  - Deploy with flag OFF
  - Wait 1 hour (verify app stable)
  - Enable flag for 10% users (internal team)
  - Wait 24 hours
  - Enable for 100%
- **Rollback**: Set `AUTH_ENABLED=false`, restart app (<5 min)

**Testing Strategy**:

- **Unit tests** (20 tests):
  - Password hashing/verification
  - JWT token generation/validation
  - Input validation (email format, password strength)
- **Integration tests** (15 tests):
  - POST /register success (valid input)
  - POST /register failures (duplicate email, weak password)
  - POST /login success
  - POST /login failures (wrong password, nonexistent user)
  - Rate limiting (6th attempt blocked)
- **E2E tests** (3 scenarios):
  - Happy path: Register → Login → Access protected route
  - Error path: Invalid credentials → Retry → Success
  - Rate limit: 5 failed attempts → 429 error

**Deployment Strategy**:

- **Risk Level**: MEDIUM (authentication is security-critical)
- **Pre-Deployment Checklist**:
  - [ ] JWT_SECRET configured in production env
  - [ ] HTTPS enforced
  - [ ] MongoDB indexes created (email unique)
  - [ ] Rate limiter tested (5 attempts limit)
  - [ ] Error messages don't leak sensitive info
  - [ ] Monitoring dashboard configured (login success rate, error rate)
```

---

## Decision Frameworks

### When to Skip Comprehensive Planning

**Skip if** (Complexity 1-2):

- Single file change <200 LOC
- No external dependencies
- Clear, well-documented pattern exists
- Low risk (no security, auth, or data integrity concerns)

**Example**: Adding a formatDate helper function → Just implement it

### When Planning is Critical

**Always plan if** (Complexity 4-5):

- Security-critical (auth, payments, data access)
- Novel architecture pattern
- Breaking changes
- Multiple integrations
- High user impact

**Example**: Authentication system → Comprehensive planning mandatory

---

## How to Fill Templates Effectively

### Requirements Block

**Goal**:

- ❌ Bad: "Improve authentication"
- ✅ Good: "Allow users to create accounts and log in securely using email/password"

**User Stories**:

- ❌ Bad: "As a user, I want auth"
- ✅ Good: "As a new user, I want to create an account with email/password so that I can access personalized features"

**Acceptance Criteria**:

- ❌ Bad: "Auth works"
- ✅ Good: "Password must be 12+ chars with upper, lower, number, symbol"

### Architecture Block

**Data Models**:

- ❌ Bad: "User has email and password"
- ✅ Good: Provide TypeScript interface with field types and constraints

**Key Decisions**:

- ❌ Bad: "Use JWT"
- ✅ Good: "JWT vs Sessions: JWT (stateless) - Trade-off: can't revoke instantly, Mitigation: short expiry + Redis Phase 2"

### Risk Register

**Risk Description**:

- ❌ Bad: "Security issue"
- ✅ Good: "NoSQL injection via email field"

**Mitigation**:

- ❌ Bad: "Be careful"
- ✅ Good: "Validate input type (must be string), use parameterized queries"

---

## Verification Reminder

Always end planning with a verification summary:

```markdown
## Planning Verification

**Inputs Reviewed**:

- [ ] User requirements gathered from stakeholders
- [ ] Existing auth patterns in codebase analyzed
- [ ] Security best practices consulted

**Outstanding Questions**:

- "Remember me" functionality decision pending (ask product team)

**Follow-Up Tasks**:

- Review with security team before implementation
- Set up monitoring dashboard for auth metrics
- Schedule deployment for Tuesday 2pm (avoid Friday)

**Next Step**: Proceed to BUILD workflow with this plan
```

---

## References

- Complexity Rubric: `plugins/cc10x/skills/cc10x-orchestrator/SKILL.md`
- Risk Framework: `plugins/cc10x/skills/risk-analysis/SKILL.md`
- Deployment Strategy: `plugins/cc10x/skills/deployment-patterns/SKILL.md`
- Architecture Patterns: `plugins/cc10x/skills/architecture-patterns/SKILL.md`
