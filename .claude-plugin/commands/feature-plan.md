---
name: feature-plan
description: Comprehensive feature planning before implementation. Generates PRD-style plan with user stories, architecture, components, APIs, data models, edge cases, and testing strategy. Use BEFORE /feature-build to ensure strategic planning.
---

# Feature Planning - Strategic Design Before Building

You are orchestrating a comprehensive feature planning workflow that creates a detailed, actionable plan BEFORE any code is written.

## Command Usage

```
/feature-plan <feature-description>
```

**Examples**:
- `/feature-plan Add user authentication with JWT`
- `/feature-plan Build a real-time chat system`
- `/feature-plan Create a payment processing flow with Stripe`

## Philosophy

**"Plan twice, code once"** - A great plan makes implementation 10x faster and prevents costly mistakes.

## Workflow Overview

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
**Output**: Detailed plan document ready for implementation

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

GET /api/users/:id
Headers:
  Authorization: Bearer <token>
Response (200 OK):
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2025-10-22T10:00:00Z"
}
Error (404 Not Found):
{
  "error": "User not found"
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

Table: sessions (if using session-based auth)
┌─────────────┬──────────────┬─────────────┐
│ Column      │ Type         │ Constraints │
├─────────────┼──────────────┼─────────────┤
│ id          │ UUID         │ PRIMARY KEY │
│ user_id     │ UUID         │ FOREIGN KEY → users(id) │
│ token       │ VARCHAR(500) │ UNIQUE, NOT NULL │
│ expires_at  │ TIMESTAMP    │ NOT NULL    │
│ created_at  │ TIMESTAMP    │ DEFAULT NOW │
└─────────────┴──────────────┴─────────────┘

Indexes:
- idx_sessions_token ON sessions(token)
- idx_sessions_user_id ON sessions(user_id)
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
- [ ] Password doesn't meet requirements (length, complexity)
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

- auth.controller.test.ts
  - test('POST /register returns 201 with token')
  - test('POST /register returns 400 for invalid email')
  - test('POST /login returns 200 with token')

Integration Tests (API endpoints):
- End-to-end API flow tests
- Database interactions
- Authentication middleware

Files to test:
- auth.integration.test.ts
  - test('user can register, login, and access protected route')
  - test('expired token is rejected')

E2E Tests (User journeys):
- Critical user paths
- Cross-browser compatibility
- Mobile responsiveness

Scenarios to test:
- User registration flow (happy path)
- User login flow (happy path)
- User login with wrong password (error path)
- Token expiration handling

Manual Testing Checklist:
- [ ] Register with valid email
- [ ] Register with duplicate email (expect error)
- [ ] Login with correct credentials
- [ ] Login with wrong password (expect error)
- [ ] Access protected route with valid token
- [ ] Access protected route without token (expect 401)
- [ ] Token refresh flow
- [ ] Logout flow
```

**Quality Gate**:
- ✅ Test coverage plan is comprehensive
- ✅ Both happy and error paths covered
- ✅ E2E scenarios identified
- ❌ If gaps → Add missing test scenarios

---

## Complete Plan Output

After all phases, generate a **persistent markdown checklist** using the template format from `.claude/docs/checklist-template.md`:

**Output Location**: `.claude/docs/checklist-[feature-name].md`

**Format**: Use the checklist template structure with these sections:

```markdown
# [Feature Name] Implementation Checklist

**Source**: `/feature-plan` command output
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
- **In Progress**: 0
- **Remaining**: [Total tasks]

**Phase Progress**:
- Phase 1 (Foundation): 0/X tasks □□□□□
- Phase 2 (Core Features): 0/X tasks □□□□□
- Phase 3 (Testing & Polish): 0/X tasks □□□□□

---

## 🏗️ Phase 1: Foundation

### 1.1 Data Models & Schema

**Deliverable**: Complete data models [from Phase 4: Data Models]
**Acceptance Criteria**:
- All models have proper TypeScript types
- Validation rules defined
- Database migrations created and tested
**Dependencies**: None

- [ ] 1.1.1 Create [table name] with [specific fields from data model]
- [ ] 1.1.2 Add validation schemas (Zod/Yup)
- [ ] 1.1.3 Create migrations
- [ ] 1.1.4 Test model creation

### 1.2 API Routes & Middleware

**Deliverable**: Functional API endpoints [from Phase 4: API Design]
**Acceptance Criteria**:
- Routes respond with correct status codes
- Middleware configured
- Error handling returns meaningful messages
**Dependencies**: 1.1 (Data Models)

- [ ] 1.2.1 Create [endpoint 1 from API design]
- [ ] 1.2.2 Create [endpoint 2 from API design]
- [ ] 1.2.3 Add middleware [from architecture decisions]
- [ ] 1.2.4 Test endpoints

---

## 🎨 Phase 2: Core Features

### 2.1 Frontend Components

**Deliverable**: UI components [from Phase 3: Components]
**Acceptance Criteria**:
- Components render without errors
- Props properly typed
- Lovable/Bolt-quality UIs (gradients, shadows, animations)
- Responsive design
**Dependencies**: 1.2 (API Routes)

- [ ] 2.1.1 Implement [Component 1 from breakdown]
- [ ] 2.1.2 Implement [Component 2 from breakdown]
- [ ] 2.1.3 Add loading and error states
- [ ] 2.1.4 Style with modern design patterns

### 2.2 Business Logic

**Deliverable**: Complete feature workflow [from User Stories]
**Acceptance Criteria**:
- User actions trigger correct API calls
- Data persists correctly
- UI updates reflect backend state
- Edge cases handled [from Phase 5]
**Dependencies**: 2.1 (UI Components)

- [ ] 2.2.1 Implement [workflow from user story 1]
- [ ] 2.2.2 Add state management [from architecture]
- [ ] 2.2.3 Connect UI to API
- [ ] 2.2.4 Handle edge cases [reference Phase 5 edge cases]

---

## 🔍 Phase 3: Testing & Polish

### 3.1 Automated Testing

**Deliverable**: Test coverage [from Phase 6: Testing Strategy]
**Acceptance Criteria**:
- Unit tests for all business logic
- Integration tests for API endpoints
- Component tests for UI
- Coverage > 70%
**Dependencies**: 2.2 (Business Logic)

- [ ] 3.1.1 Write unit tests [list from Phase 6]
- [ ] 3.1.2 Write integration tests [list from Phase 6]
- [ ] 3.1.3 Write component tests
- [ ] 3.1.4 Achieve >70% coverage

### 3.2 Manual Testing

**Deliverable**: Verified edge cases [from Phase 5]
**Acceptance Criteria**:
- All happy paths work
- Edge cases handled gracefully
- Error messages helpful
**Dependencies**: 3.1 (Automated Testing)

- [ ] 3.2.1 Test [edge case 1 from Phase 5]
- [ ] 3.2.2 Test [edge case 2 from Phase 5]
- [ ] 3.2.3 Test error handling
- [ ] 3.2.4 Test on mobile

### 3.3 Documentation

**Deliverable**: Updated documentation
**Acceptance Criteria**:
- Code commented
- API documented
- README updated
- No debug code
**Dependencies**: 3.2 (Manual Testing)

- [ ] 3.3.1 Add JSDoc comments
- [ ] 3.3.2 Document API endpoints
- [ ] 3.3.3 Update README
- [ ] 3.3.4 Remove debug code

---

## 📝 Implementation Notes

### Technical Decisions
[Copy from Phase 2: Architecture]

### Risks & Mitigations
[Derive from Phase 5: Edge Cases]

### Future Enhancements
[Copy from "out of scope" items in Phase 1]

---

## 🎯 Usage with TodoWrite Tool

**For active development sessions**:
1. Copy current phase tasks (5-10 items) to TodoWrite tool
2. Mark complete in both TodoWrite and this checklist
3. Update progress dashboard after each phase

**Why hybrid approach?**
- This checklist = Persistent, long-term tracking, version controlled
- TodoWrite = Ephemeral, real-time UI tracking during active coding

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
**Last Updated**: [Date] by cc10x `/feature-plan` command
```

**Save the checklist file** to `.claude/docs/checklist-[feature-name].md` for persistent tracking.

---

## Using the Plan with /feature-build

Once the persistent checklist is created at `.claude/docs/checklist-[feature-name].md`:

**Hybrid Workflow**:

1. **Long-term tracking** (Persistent checklist):
   - All tasks organized by phases in `.claude/docs/checklist-[feature-name].md`
   - Version controlled, team-visible
   - Progress dashboard shows overall completion

2. **Active session tracking** (TodoWrite tool):
   - Copy current phase tasks (5-10 items) to TodoWrite
   - Real-time UI updates during implementation
   - Marks progress visibly in Claude Code interface

**Implementation commands**:

```bash
# Option 1: Implement specific phase
/feature-build Implement Phase 1 from checklist-authentication.md

# Option 2: Implement specific subsection
/feature-build Implement Phase 2.1 (Frontend Components) from checklist-authentication.md

# Option 3: Implement specific tasks
/feature-build Implement tasks 1.1.1-1.1.4 (Data Models) from checklist-authentication.md
```

**During /feature-build execution**:
- TodoWrite tool tracks 5-10 active tasks from current phase
- After phase complete, update persistent checklist
- Move to next phase tasks

The persistent checklist serves as a **complete specification** that `/feature-build` can execute from, ensuring:
- ✅ No guessing about architecture
- ✅ No missing edge cases
- ✅ No unclear requirements
- ✅ Faster implementation (clear roadmap)
- ✅ Progress tracking across sessions
- ✅ Team collaboration on long-term features

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
Plan includes: Custom crypto library, distributed session store, blockchain verification
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
