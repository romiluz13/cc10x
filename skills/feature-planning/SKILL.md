---
name: feature-planning
description: |
  Creates comprehensive PRD-style feature plans with user stories, architecture decisions, component breakdowns, API contracts, data models, edge cases, and testing strategies. Use for strategic planning before implementation.
  
  Trigger phrases: "plan feature", "feature plan", "design feature", "planning",
  "plan this", "create plan", "feature design", "architecture plan",
  "feature spec", "requirements", "PRD", "plan before building",
  "design document", "feature planning", "plan implementation".
  
  Activates on: feature planning requests, architecture design, requirements analysis,
  PRD creation, strategic planning, pre-implementation design.
progressive: true
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
