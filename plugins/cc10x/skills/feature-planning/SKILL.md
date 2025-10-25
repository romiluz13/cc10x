---
name: feature-planning
description: Creates comprehensive PRD-style feature plans with user stories, architecture decisions, component breakdowns, API contracts, data models, edge cases, testing strategies, complexity assessment, file change manifests, and implementation roadmaps. Use for strategic planning before implementing complex features (4-5 complexity). Provides 5 progressive stages (requirements analysis, architecture design, risk assessment, complexity scoring with recommendations to skip if simple, and file manifest creation). Loaded by requirements-analyst and architect agents during PLANNING workflow. Particularly valuable for novel architectures, high-risk features, or when team alignment documentation needed. For simple features using well-documented libraries, recommend manual implementation instead (faster and more token-efficient).
license: MIT
---

# Feature Planning - Strategic Design Before Building

## Overview

Create comprehensive, actionable feature plans BEFORE any code is written. Generate persistent markdown checklists ready for `/feature-build` execution.

**Core principle:** "Plan twice, code once" - A great plan makes implementation 10x faster and prevents costly mistakes.

**Announce at start:** "I'm using the feature-planning skill to create the implementation plan."

**Output Location:** `.claude/docs/checklist-[feature-name].md`

## 6-Phase Planning Workflow

```
Phase 1: Understand the Feature (requirements gathering)
    ↓
Phase 2: Design Architecture (technical decisions)
    ↓
Phase 3: Break Down Components (what to build)
    ↓
Phase 4: Define APIs & Data Models (contracts)
    ↓
Phase 5: Identify Edge Cases (prevent bugs)
    ↓
Phase 6: Plan Testing Strategy (quality assurance)
    ↓
Output: Comprehensive Plan → Ready for /feature-build
```

**Estimated Time**: 5-10 minutes
**Estimated Tokens**: ~20k tokens

---

## Phase 1: Understand the Feature

**Objective**: Clarify requirements and user needs
**Duration**: 1-2 minutes

### Questions to Answer

```markdown
[Feature Understanding]

1. What problem does this solve?
   - User pain point: _______________
   - Current workaround: _______________
   - Desired outcome: _______________

2. Who are the users?
   - Primary users: _______________
   - Secondary users: _______________
   - User expertise level: _______________

3. What's the scope?
   - Must-have features: _______________
   - Nice-to-have features: _______________
   - Explicitly out of scope: _______________

4. What are the constraints?
   - Time constraints: _______________
   - Technical constraints: _______________
   - Budget constraints: _______________
```

### User Stories

**Format**: "As a [user type], I want to [action], so that [benefit]"

```markdown
[User Stories]

Story 1: Core Functionality
As a [user type],
I want to [action],
So that [benefit]

Acceptance Criteria:
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

Story 2: [Additional functionality]
...

Story 3: [Edge case handling]
...
```

**Quality Gate**:
- ✅ User stories are clear and testable
- ✅ Acceptance criteria are specific
- ✅ Scope is well-defined
- ❌ If unclear → Ask user for clarification

---

## Phase 2: Design Architecture

**Objective**: Make strategic technical decisions
**Duration**: 2-3 minutes

### Technical Decisions

```markdown
[Architecture Decisions]

1. Frontend Architecture
   - Framework: React / Next.js / etc.
   - State Management: Context / Redux / Zustand
   - Routing: React Router / Next.js App Router
   - Styling: Tailwind / CSS Modules / Styled Components
   - UI Components: Headless UI / shadcn/ui / custom

2. Backend Architecture
   - Language: Node.js / Python / Go
   - Framework: Express / Fastify / Django / FastAPI
   - API Style: REST / GraphQL / tRPC
   - Authentication: JWT / OAuth / Session-based
   - Database: PostgreSQL / MongoDB / MySQL

3. Data Flow
   - Client → API → Database
   - Real-time: WebSockets / Server-Sent Events / Polling
   - Caching: Redis / In-memory / CDN

4. Third-Party Services
   - Authentication: Clerk / Auth0 / Firebase
   - Payments: Stripe / PayPal
   - Storage: AWS S3 / Cloudinary
   - Email: SendGrid / Resend
```

### Architecture Diagram (Text-Based)

```markdown
[System Architecture]

┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   API Layer     │
│   (Express)     │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌────────┐
│Database│ │ Cache  │
│(Postgres)│ (Redis)│
└────────┘ └────────┘
```

**Quality Gate**:
- ✅ Technology choices align with existing stack
- ✅ Architecture is scalable
- ✅ Decisions are documented
- ❌ If misaligned → Adjust to project conventions

---

## Phase 3: Break Down Components

**Objective**: Identify what needs to be built
**Duration**: 2-3 minutes

### Component Breakdown

```markdown
[Components to Build]

Frontend Components:
1. Component Name (e.g., LoginForm)
   - Purpose: User authentication form
   - Props: onSubmit, error, loading
   - State: email, password, validation errors
   - Children: EmailInput, PasswordInput, SubmitButton
   - Complexity: Medium
   - Estimated time: 30 minutes

2. Component Name (e.g., UserProfile)
   - Purpose: Display and edit user information
   - Props: userId, onUpdate
   - State: user data, editing mode
   - Children: Avatar, ProfileFields, SaveButton
   - Complexity: High
   - Estimated time: 60 minutes

Backend Services:
1. Service Name (e.g., AuthService)
   - Purpose: Handle authentication logic
   - Methods:
     - register(email, password): Promise<User>
     - login(email, password): Promise<{ token, user }>
     - verifyToken(token): Promise<User>
   - Dependencies: Database, JWT library
   - Complexity: Medium
   - Estimated time: 45 minutes

2. Service Name (e.g., UserService)
   - Purpose: User CRUD operations
   - Methods:
     - getUser(id): Promise<User>
     - updateUser(id, data): Promise<User>
     - deleteUser(id): Promise<void>
   - Dependencies: Database
   - Complexity: Low
   - Estimated time: 30 minutes

Middleware/Utils:
1. authMiddleware
   - Purpose: Verify JWT tokens on protected routes
   - Complexity: Low
   - Estimated time: 15 minutes

2. validation
   - Purpose: Input validation helpers
   - Complexity: Low
   - Estimated time: 15 minutes
```

**Total Estimated Time**: Sum of all components

**Quality Gate**:
- ✅ All necessary components identified
- ✅ Dependencies between components clear
- ✅ Time estimates realistic
- ❌ If incomplete → Add missing components

---

## Phase 3b: Risk Assessment

**Objective**: Identify and mitigate risks before implementation (BMAD METHOD pattern)
**Duration**: 1-2 minutes

### Risk Identification Process

Systematically identify risks across 4 key categories:

```markdown
[Risk Assessment]

### Security Risks
- Authentication bypass (token validation, session hijacking)
- Injection attacks (SQL, NoSQL, XSS, command injection)
- Data exposure (sensitive data in logs, APIs, errors)
- Authorization failures (privilege escalation, IDOR)
- Cryptography misuse (weak algorithms, hardcoded secrets)

### Performance Risks
- N+1 queries (missing JOINs, inefficient ORMs)
- Memory leaks (unclosed connections, circular references)
- Bottlenecks (synchronous operations, missing indexes)
- Infinite loops (recursive logic, missing termination)
- Resource exhaustion (uncontrolled growth, no pagination)

### Data Integrity Risks
- Data loss (missing transactions, no backups)
- Data corruption (race conditions, invalid state transitions)
- Inconsistent state (distributed system sync issues)
- Orphaned records (missing cascades, incomplete cleanup)
- Migration failures (schema changes break existing data)

### Technical Risks
- Dependency issues (unmaintained packages, version conflicts)
- Breaking changes (API compatibility, data format changes)
- Complexity explosion (over-engineering, tight coupling)
- Technical debt (shortcuts that need fixing later)
- Maintainability (hard to understand, test, or modify)
```

### Risk Scoring Matrix

For each identified risk:

**Probability Scale:**
- **Low (1)**: Unlikely to happen (< 10% chance)
- **Medium (2)**: Could happen (10-50% chance)
- **High (3)**: Likely to happen (> 50% chance)

**Impact Scale:**
- **Low (1)**: Minor inconvenience, easy fix
- **Medium (2)**: Significant issue, requires work to fix
- **High (3)**: Critical failure, major rework needed

**Risk Score = Probability × Impact (1-9)**

**Priority Levels:**
- **HIGH (7-9)**: Must address in implementation plan
- **MEDIUM (4-6)**: Mitigate through testing strategy
- **LOW (1-3)**: Document and accept

### Risk Assessment Table Format

```markdown
| Risk ID | Risk Description | Category | Probability | Impact | Score | Priority | Mitigation Strategy |
|---------|------------------|----------|-------------|--------|-------|----------|---------------------|
| R-001 | JWT signature validation bypass | Security | 2 | 3 | 6 | MEDIUM | Use verified JWT library, add signature validation tests |
| R-002 | N+1 query when loading nested data | Performance | 3 | 2 | 6 | MEDIUM | Use eager loading/JOINs, add performance tests |
| R-003 | Race condition on concurrent writes | Data | 2 | 3 | 6 | MEDIUM | Use database transactions, add concurrency tests |
| R-004 | Unmaintained dependency vulnerability | Technical | 1 | 3 | 3 | LOW | Use Dependabot, regular security audits |
```

### Mitigation Planning

For each MEDIUM/HIGH risk, define concrete mitigation:

```markdown
[Risk Mitigation Plan]

**HIGH Risks (Score 7-9):** [Count]
[For each HIGH risk]
- **Risk ID**: [ID]
- **Mitigation Steps**:
  1. [Specific action in implementation]
  2. [Specific test to validate mitigation]
  3. [Monitoring/alerting to detect if it occurs]

**MEDIUM Risks (Score 4-6):** [Count]
[For each MEDIUM risk]
- **Risk ID**: [ID]
- **Mitigation Steps**:
  1. [Specific action]
  2. [Test coverage]
  3. [Fallback strategy]

**LOW Risks (Score 1-3):** [Count] - Accepted as-is
- Document for awareness but no active mitigation needed
```

### Integration into Implementation Roadmap

Map mitigations back to implementation phases:

```markdown
[Risk Mitigation Integration]

**Phase 1 (Foundation):**
- Mitigation for R-001: [Action]
- Mitigation for R-004: [Action]

**Phase 2 (Core Features):**
- Mitigation for R-002: [Action]
- Mitigation for R-003: [Action]

**Phase 3 (Testing & Validation):**
- Test for R-001: [Test description]
- Test for R-002: [Performance test]
- Test for R-003: [Concurrency test]
```

**Quality Gate**:
- ✅ All HIGH risks have concrete mitigations in plan
- ✅ MEDIUM risks have test coverage planned
- ✅ Risk mitigations integrated into implementation phases
- ❌ If HIGH risk without mitigation → Cannot proceed until addressed

---

## Phase 4: Define APIs & Data Models

**Objective**: Establish contracts between frontend and backend
**Duration**: 2-3 minutes

### API Endpoints

```markdown
[API Design]

POST /api/auth/register
Request:
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
Response (201 Created):
{
  "token": "eyJhbGc...",
  "user": {
    "id": "usr_123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2025-10-22T10:00:00Z"
  }
}
Error (400 Bad Request):
{
  "error": "Email already exists"
}

POST /api/auth/login
Request:
{
  "email": "user@example.com",
  "password": "securepassword123"
}
Response (200 OK):
{
  "token": "eyJhbGc...",
  "user": { ... }
}
Error (401 Unauthorized):
{
  "error": "Invalid credentials"
}
```

### Data Models

```markdown
[Database Schema]

Table: users
┌─────────────┬──────────────┬─────────────┐
│ Column      │ Type         │ Constraints │
├─────────────┼──────────────┼─────────────┤
│ id          │ UUID         │ PRIMARY KEY │
│ email       │ VARCHAR(255) │ UNIQUE, NOT NULL │
│ password_hash│ VARCHAR(255)│ NOT NULL    │
│ name        │ VARCHAR(255) │ NOT NULL    │
│ created_at  │ TIMESTAMP    │ DEFAULT NOW │
│ updated_at  │ TIMESTAMP    │ DEFAULT NOW │
└─────────────┴──────────────┴─────────────┘

Indexes:
- idx_users_email ON users(email)
```

**Quality Gate**:
- ✅ API contracts are complete and consistent
- ✅ Data models support all required operations
- ✅ Indexes for query performance
- ❌ If inconsistent → Align API with data model

---

## Phase 5: Identify Edge Cases

**Objective**: Think through failure scenarios and edge cases
**Duration**: 1-2 minutes

### Edge Cases Checklist

```markdown
[Edge Cases to Handle]

Authentication Edge Cases:
- [ ] User tries to register with existing email
- [ ] User enters invalid email format
- [ ] Password doesn't meet requirements
- [ ] Token expires while user is active
- [ ] User tries to access protected route without token
- [ ] Token is invalid or tampered with
- [ ] Multiple login attempts (rate limiting)

Data Validation Edge Cases:
- [ ] Empty required fields
- [ ] SQL injection attempts
- [ ] XSS attempts in user input
- [ ] Very long strings (buffer overflow)
- [ ] Special characters in names/emails
- [ ] Unicode characters handling

Network Edge Cases:
- [ ] API request timeout
- [ ] Network connection lost mid-request
- [ ] Server returns 500 error
- [ ] Rate limit exceeded (429)
- [ ] Duplicate form submissions

UI/UX Edge Cases:
- [ ] Loading states (spinner while fetching)
- [ ] Empty states (no users found)
- [ ] Error states (failed to load)
- [ ] Slow network (show skeleton loaders)
- [ ] Mobile viewport (responsive design)
- [ ] Accessibility (keyboard navigation, screen readers)
```

### Error Handling Strategy

```markdown
[Error Handling]

Frontend:
- Show user-friendly error messages (not technical errors)
- Provide actionable next steps ("Try again" button)
- Log errors to monitoring service (Sentry)
- Graceful degradation (show cached data if API fails)

Backend:
- Return consistent error format
- Log errors with context (user ID, request ID)
- Don't expose internal errors to frontend
- Use HTTP status codes correctly (400, 401, 403, 404, 500)
```

**Quality Gate**:
- ✅ All major edge cases identified
- ✅ Error handling strategy defined
- ✅ User experience considered for failures
- ❌ If incomplete → Add more edge cases

---

## Phase 6: Plan Testing Strategy

**Objective**: Ensure quality through comprehensive testing
**Duration**: 1-2 minutes

### Testing Breakdown

```markdown
[Testing Strategy]

Unit Tests (70% coverage minimum):
- Service functions (business logic)
- Utility functions (validation, formatting)
- React component logic (not UI)

Files to test:
- auth.service.test.ts
  - test('registers new user successfully')
  - test('throws error for duplicate email')
  - test('hashes password correctly')

Integration Tests (API endpoints):
- End-to-end API flow tests
- Database interactions
- Authentication middleware

E2E Tests (User journeys):
- Critical user paths
- Cross-browser compatibility
- Mobile responsiveness

Manual Testing Checklist:
- [ ] Register with valid email
- [ ] Register with duplicate email (expect error)
- [ ] Login with correct credentials
- [ ] Login with wrong password (expect error)
- [ ] Access protected route with valid token
- [ ] Access protected route without token (expect 401)
```

**Quality Gate**:
- ✅ Test coverage plan is comprehensive
- ✅ Both happy and error paths covered
- ✅ E2E scenarios identified
- ❌ If gaps → Add missing test scenarios

---

## Complete Plan Output

After all phases, generate a **persistent markdown checklist**:

**Output Location**: `.claude/docs/checklist-[feature-name].md`

**Format**:

```markdown
# [Feature Name] Implementation Checklist

**Generated**: [Date]
**Status**: Not Started
**Estimated Time**: [X hours/days]

---

## 📋 Overview

[Brief summary from Phase 1: Understanding]

**Key Goals**:
- Goal 1 (from user stories)
- Goal 2 (from user stories)
- Goal 3 (from user stories)

---

## 📊 Progress Dashboard

- **Total Tasks**: [Count all checklist items]
- **Completed**: 0 (0%)
- **Remaining**: [Total tasks]

**Phase Progress**:
- Phase 1 (Foundation): 0/X tasks □□□□□
- Phase 2 (Core Features): 0/X tasks □□□□□
- Phase 3 (Testing & Polish): 0/X tasks □□□□□

---

## 🏗️ Phase 1: Foundation

### 1.1 Data Models & Schema

**Deliverable**: Complete data models [from Phase 4]
**Acceptance Criteria**:
- All models have proper TypeScript types
- Validation rules defined
- Database migrations created and tested
**Dependencies**: None

- [ ] 1.1.1 Create [table name] with [specific fields]
- [ ] 1.1.2 Add validation schemas (Zod/Yup)
- [ ] 1.1.3 Create migrations
- [ ] 1.1.4 Test model creation

[... Continue with all phases ...]

---

## 📝 Implementation Notes

### Technical Decisions
[Copy from Phase 2: Architecture]

### Risks & Mitigations
[Derive from Phase 5: Edge Cases]

---

## ✅ Completion Criteria

**Feature is complete when**:
- ✅ All phases checked off
- ✅ All automated tests passing
- ✅ Manual testing verified
- ✅ Documentation updated
- ✅ Code reviewed (optional: `/review`)
- ✅ Ready for production

---

**NEXT STEP: Use `/feature-build` to implement tasks from current phase**
```

**Save the checklist file** to `.claude/docs/checklist-[feature-name].md` for persistent tracking.

---

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `.claude/docs/checklist-[feature-name].md`. Ready to implement with `/feature-build`?"**

---

## Stage 4: Complexity Assessment (~600 tokens)

**Objective**: Honest evaluation of whether cc10x adds value for this feature

**Purpose:** Prevent using cc10x for features where manual implementation is faster/better

### The 1-5 Complexity Scoring Rubric

**Assessment Factors:**
- Files affected (count)
- Novel patterns vs familiar (ratio)
- Integration points (count)
- Risk level (1-5)
- Domain complexity (simple/moderate/high)

#### 1. TRIVIAL (<50 lines, single file, well-documented)

**Example:** Add validation to form field

**Characteristics:**
- Single file modification
- < 50 lines of code
- Well-documented pattern exists
- No new dependencies
- No architecture decisions

**Recommendation:** ❌ Skip cc10x (5-10 min manual implementation)

**Why:**
- Planning overhead (20-30k tokens) exceeds implementation time
- Manual implementation faster than writing the plan
- No architecture decisions needed

**Token Economics:**
- cc10x: 40k tokens (plan + build)
- Manual: 2k tokens (just implement)
- **20x more expensive with cc10x**

---

#### 2. SIMPLE (50-200 lines, 2-3 files, using library)

**Example:** Add rate limiting with express-rate-limit library

**Characteristics:**
- 2-3 files affected
- Using well-documented library
- Clear implementation path from library docs
- Minimal integration complexity
- Standard patterns

**Recommendation:** ❌ Skip cc10x (30-60 min following library docs)

**Why:**
- Library documentation is more current and specific
- Implementation path is clear
- No novel architecture needed
- Fast to implement manually

**Token Economics:**
- cc10x: 80k tokens (comprehensive planning + build)
- Manual: 5k tokens (library docs + implementation)
- **16x more expensive with cc10x**

**Real test data:** Rate limiting feature
- cc10x: 100k tokens, reported false success, tests failed
- Manual: Would have been 30 min, 5k tokens, working code

---

#### 3. MODERATE (200-500 lines, 4-6 files, some novelty)

**Example:** Add pagination with caching

**Characteristics:**
- 4-6 files affected
- Some novel patterns (not pure library use)
- Multiple integration points
- Moderate risk
- Architecture decisions needed

**Recommendation:** ⚠️ MAYBE use cc10x (if team docs valued)

**Why:**
- Structure helps but not critical
- Could go either way depending on:
  - Team collaboration needs (plan valuable for alignment)
  - Developer familiarity (junior dev benefits more)
  - Documentation requirements (enterprise needs docs)

**Token Economics:**
- cc10x: 80-100k tokens
- Manual: 15-20k tokens
- **4-5x more expensive with cc10x**

**Worth it if:**
- Team needs alignment on approach
- Want systematic TDD enforcement
- Documentation valuable for future
- Prevents rework (architecture decisions matter)

---

#### 4. COMPLEX (500-1000 lines, 7-15 files, novel patterns)

**Example:** Real-time notifications with WebSockets

**Characteristics:**
- 7-15 files affected
- Novel patterns (not in codebase)
- Many integration points (API, DB, Redis, WebSockets)
- High risk (affects all users)
- Critical architecture decisions

**Recommendation:** ✅ Use cc10x (structure prevents rework)

**Why:**
- Architecture decisions matter (WebSocket strategy, scaling, error handling)
- Integration complexity (many moving parts)
- Risk mitigation planning essential
- File manifest helps track scope creep
- Systematic approach prevents costly mistakes

**Token Economics:**
- cc10x: 100-150k tokens
- Manual: 30-50k tokens
- **3-5x more expensive BUT...**

**ROI Calculation:**
- One major rework: 80k tokens + 4 hours wasted
- One missed edge case in production: Incident response costs
- One security issue: Infinite cost
- **Structure prevents these scenarios**

---

#### 5. VERY COMPLEX (>1000 lines, 15+ files, system-wide)

**Example:** Multi-tenancy with data isolation

**Characteristics:**
- 15+ files affected
- System-wide changes
- Multiple novel patterns
- Very high risk (data isolation = security critical)
- Many critical architecture decisions
- Long-term maintenance implications

**Recommendation:** ✅✅ Use cc10x (prevents costly mistakes)

**Why:**
- Comprehensive planning ESSENTIAL
- Architecture mistakes expensive to fix later
- Risk assessment critical (data isolation bugs = breaches)
- File manifest essential (scope easily creeps)
- Rollback/deployment planning necessary
- Documentation required for team

**Token Economics:**
- cc10x: 150-200k tokens
- Manual: 50-80k tokens
- **3-4x more expensive BUT...**

**ROI Calculation:**
- One architecture mistake: Complete rewrite (weeks of work)
- One security bug: Data breach (company-ending)
- One missed edge case: Production incident (customer trust)
- **Planning cost is insurance against disaster**

---

### Quality Gate for Complexity Assessment

**If complexity < 3 (TRIVIAL or SIMPLE):**

Output honest recommendation to user:

```markdown
## Complexity Assessment

**Score: 2/5 (SIMPLE)**

⚠️ **Recommendation: Consider Manual Implementation**

This feature uses well-documented library (express-rate-limit).
A developer familiar with Express could implement in 30-60 min.

**cc10x adds value if:**
- Team needs documentation/alignment on rate limiting strategy
- Want strict TDD enforcement for quality assurance
- Enterprise requires formal planning documentation

**Manual implementation is better if:**
- Time-sensitive (manual is faster - 30 min vs 90 min with planning)
- Token budget constrained (saves 75k tokens)
- Solo developer comfortable with the library
- Quick iteration preferred over documentation

**Token Economics:**
- cc10x: ~80k tokens (plan + build + review)
- Manual: ~5k tokens (library docs + implementation)
- **16x more tokens for structure**

**Your call:** Proceed with cc10x for systematic approach, or implement manually for speed?
```

**If complexity >= 4 (COMPLEX or VERY COMPLEX):**

Proceed with confidence:

```markdown
## Complexity Assessment

**Score: 4/5 (COMPLEX)**

✅ **Recommendation: Use cc10x**

This feature has significant complexity:
- 12 files affected (controllers, services, models, middleware, tests)
- Novel patterns (WebSocket event handling not in codebase)
- 8 integration points (API, DB, Redis, WebSocket server, auth, logging)
- High risk (affects all connected users simultaneously)
- Multiple architecture decisions (connection pooling, event routing, scaling)

**Why cc10x adds value:**
- Architecture decisions critical (poor WebSocket design = scaling issues)
- Risk assessment essential (connection storms, memory leaks, cascading failures)
- Integration complexity (many moving parts to coordinate)
- File manifest prevents scope creep (easy to over-engineer real-time)
- Rollback strategy necessary (rollback real-time changes is complex)

**Token Economics:**
- cc10x: ~120k tokens (comprehensive planning + systematic build)
- Manual: ~40k tokens (ad-hoc implementation)
- **3x more tokens, BUT structure prevents:**
  - Major rework if architecture wrong (80k tokens + days of work)
  - Production incidents from missed edge cases (infinite cost)
  - Technical debt from rushed implementation (compounds over time)

**ROI: One prevented rework pays for planning cost**

**Proceeding with systematic cc10x workflow...**
```

---

## Stage 5: File Change Manifest (~500 tokens)

**Objective**: Create concrete implementation targets for verification

**Purpose:** Prevent scope creep, enable systematic verification during implementation

### Manifest Structure

For detailed File Change Manifest templates and examples, see the complete specification in the plan structure. Key elements include:

- **Summary**: Count of CREATE/MODIFY/DELETE files, estimated LOC
- **New Files**: Path, purpose, exports, dependencies, complexity, LOC estimate
- **Modified Files**: Path, locations, changes (ADD/MODIFY/DELETE), impact level
- **Deleted Files**: Path, reason, migration path, risk assessment
- **Integration Points**: How files connect (imports, function calls, data flow)
- **Verification Checklist**: Items to verify during implementation

**Use during implementation to:**
- Detect scope creep (unplanned files created)
- Verify completeness (all planned files exist)
- Check integration (connections work as planned)
- Validate estimates (LOC within ±30%)

**Quality Gate:** 90%+ match required before claiming completion

---

## Tips for Great Plans

### 1. Start with Why
Always clarify the user problem before jumping to solutions.

### 2. Be Specific
"Authentication" is vague. "JWT-based authentication with email/password, refresh tokens, and password reset" is specific.

### 3. Think Edge Cases Early
It's easier to plan for edge cases now than to fix bugs later.

### 4. Estimate Realistically
Add 20-30% buffer to time estimates for unexpected complexity.

### 5. Keep It Simple
Don't over-engineer. Build the simplest version that solves the problem.

---

## Anti-Patterns to Avoid

### ❌ Planning Too Little
```
User wants: "Add authentication"
Plan: "Use JWT"
→ Missing: What endpoints? What data model? What edge cases?
```

### ❌ Planning Too Much
```
Plan includes: Custom crypto library, distributed session store
→ Overengineered for simple use case
```

### ❌ Ignoring Existing Stack
```
Plan: "Use MongoDB for users"
Existing: PostgreSQL for everything else
→ Inconsistent technology choices
```

### ❌ No Edge Case Consideration
```
Plan: "User can register and login"
→ Missing: What if email exists? Token expires? Network fails?
```

---

## Remember

**A great plan is**:
- ✅ Comprehensive (covers all aspects)
- ✅ Specific (clear decisions, not vague)
- ✅ Actionable (ready to implement)
- ✅ Realistic (achievable time estimates)
- ✅ Documented (serves as spec for implementation)

**Time invested in planning = Time saved in implementation + bugs prevented**

**5-10 minutes planning → Hours of smooth implementation ✨**
