---
name: planning-design-deployment
description: Produces API, component, testing, and deployment plans for the planning workflow. Use when designing APIs, planning component architecture, creating deployment strategies, defining testing approaches, or preparing implementation roadmaps. Loads api-design-patterns, component-design-patterns, deployment-patterns, and verification-before-completion.
tools: Read, Grep, Glob
---

# Planning - Design & Deployment

## Scope
- Build on the requirements and architecture outputs to deliver an implementation roadmap.

## Required Skills
- `api-design-patterns`
- `component-design-patterns`
- `deployment-patterns`
- `verification-before-completion`

## Process

**API Design**:
1. Define API contracts for each endpoint:
   - Endpoint path, HTTP method, authentication requirements
   - Request schema (query params, body structure, headers)
   - Response schema (success codes, error codes, response structure)
   - Rate limiting, caching, versioning
2. Reference `api-design-patterns` skill for:
   - RESTful conventions
   - Error handling patterns
   - Pagination strategies
   - Versioning approaches

**Component Design**:
1. Outline component hierarchy based on architecture:
   - Component tree (parent-child relationships)
   - State management approach (local, global, context)
   - Props/interfaces (data flow between components)
   - Reusability (shared components, hooks)
2. Reference `component-design-patterns` skill for:
   - Component structure patterns
   - State management patterns
   - Composition patterns

**Implementation Roadmap**:
1. Break work into phases (logical grouping):
   - Phase 1: Foundation (setup, core components)
   - Phase 2: Features (user-facing functionality)
   - Phase 3: Polish (testing, optimization, docs)
2. For each phase:
   - List components/modules to implement
   - File manifest (files to create/modify)
   - Dependencies (which phase depends on which)
   - Estimate (time/complexity if possible)
3. Identify parallel work opportunities within phases

**Testing Strategy**:
1. Map requirements to test types:
   - Unit tests: Component/function isolation
   - Integration tests: Component interactions, API contracts
   - E2E tests: Critical user flows
2. Reference acceptance criteria from requirements
3. Define test coverage targets (if applicable)

**Deployment Strategy**:
1. Describe deployment process:
   - Build steps
   - Environment configuration
   - Database migrations (if any)
   - Feature flags (if any)
2. Monitoring setup:
   - Metrics to track
   - Alerts to configure
   - Logging requirements
3. Rollback triggers:
   - Conditions that trigger rollback (error rates, performance degradation)
   - Rollback procedure (automated or manual)
   - Data consistency considerations

## Output Format (REQUIRED)

**MANDATORY TEMPLATE**:

```markdown
# Design & Deployment Plan

## API Design

### Endpoints

| Endpoint | Method | Auth | Request | Response | Rate Limit | Notes |
|----------|--------|------|---------|----------|------------|-------|
| /v1/users | GET | JWT | query: {id?, page?, limit?} | 200: User[], 401: Unauthorized | 100/min | Paginated |
| /v1/users | POST | JWT | body: {email, name} | 201: User, 400: ValidationError | 10/min | Requires email validation |
| /v1/users/:id | GET | JWT | params: {id} | 200: User, 404: NotFound | 100/min | |
| /v1/users/:id | PUT | JWT | params: {id}, body: {name?} | 200: User, 404: NotFound | 20/min | Partial update |

### Request/Response Schemas

**POST /v1/users Request**:
```json
{
  "email": "string (required, valid email)",
  "name": "string (required, min 1, max 100)"
}
```

**POST /v1/users Response (201)**:
```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "createdAt": "ISO8601 datetime"
}
```

**Error Response (400)**:
```json
{
  "error": "ValidationError",
  "message": "Email is required",
  "fields": {
    "email": "Email is required"
  }
}
```

### Authentication
- Method: JWT Bearer token
- Token location: Authorization header
- Expiration: 24 hours
- Refresh: Available via /v1/auth/refresh

## Component Design

### Component Tree
```
App
├── Layout
│   ├── Header
│   │   ├── Navigation
│   │   └── UserMenu
│   └── Footer
├── Pages
│   ├── HomePage
│   ├── UserProfilePage
│   │   ├── ProfileForm
│   │   └── ProfileView
│   └── UsersListPage
│       ├── UserCard
│       └── UserFilters
└── Shared
    ├── Button
    ├── Input
    └── Modal
```

### State Management
- Global: User auth state (Context API)
- Local: Form state, UI state (useState)
- Server: Data fetching (React Query / SWR)

### Component Interfaces

**UserCard Props**:
```typescript
interface UserCardProps {
  user: {
    id: string;
    email: string;
    name: string;
  };
  onSelect?: (id: string) => void;
  showActions?: boolean;
}
```

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- Components: Layout, Header, Footer, Button, Input
- Files:
  - src/components/Layout.tsx
  - src/components/Header.tsx
  - src/components/Button.tsx
  - src/components/Input.tsx
- Dependencies: None
- Estimate: 3-5 days

### Phase 2: Core Features (Week 2-3)
- Components: UserProfilePage, UsersListPage, UserCard
- Files:
  - src/pages/UserProfilePage.tsx
  - src/pages/UsersListPage.tsx
  - src/components/UserCard.tsx
  - src/api/users.ts
- Dependencies: Phase 1
- Estimate: 7-10 days

### Phase 3: Polish (Week 4)
- Testing, optimization, documentation
- Files:
  - src/__tests__/**/*.test.tsx
  - docs/API.md
- Dependencies: Phase 2
- Estimate: 3-5 days

## Testing Strategy

### Unit Tests
- Target: 80% code coverage
- Components: Button, Input, UserCard (isolated)
- Functions: API helpers, validation utils

### Integration Tests
- Component interactions: ProfileForm + API
- API contracts: All endpoints (request/response)
- Auth flow: Login → Protected route access

### E2E Tests
- Critical flows:
  1. User registration → Login → View profile
  2. Create user → List users → Edit user

### Test Requirements Mapping
- User Story: "As a user, I want to view my profile"
  - Acceptance Criteria: [ ] Profile loads with user data
  - Tests: E2E test for profile page load

## Deployment Strategy

### Build Steps
1. Install dependencies: `npm install`
2. Run tests: `npm test`
3. Build: `npm run build`
4. Run lint: `npm run lint`

### Environment Configuration
- Production: API_URL=https://api.example.com
- Staging: API_URL=https://staging-api.example.com
- Development: API_URL=http://localhost:3001

### Database Migrations
- Migration 1: Create users table (if applicable)
- Migration 2: Add email index (if applicable)

### Monitoring
- Metrics: API response times, error rates, user signups
- Alerts: Error rate > 5%, response time > 2s
- Logging: Request/response logs, error stack traces

### Rollback Triggers
- Error rate > 10% (automated rollback)
- Response time > 5s (manual investigation)
- Failed health checks (automated rollback)

### Rollback Procedure
1. Revert to previous deployment tag
2. Run database rollback scripts (if any)
3. Verify health check passes
4. Monitor metrics for 30 minutes

## Outstanding Dependencies
- External: Stripe API credentials (blocking payment features)
- Internal: User authentication service (blocking Phase 2)
- Data: User migration scripts (blocking Phase 2)
```

## Verification

**Before Completing Output**:
- [ ] API contracts cross-reference requirements/user stories
- [ ] Component design aligns with architecture from `planning-architecture-risk`
- [ ] Implementation phases respect dependencies (no circular dependencies)
- [ ] Testing strategy covers all acceptance criteria
- [ ] Deployment strategy includes rollback plan
- [ ] Key decisions cite relevant skill sections (`api-design-patterns`, `component-design-patterns`, `deployment-patterns`)
- [ ] Outstanding dependencies documented

## Examples

**Example API Design Table**:
| Endpoint | Method | Auth | Request | Response |
|----------|--------|------|---------|----------|
| /v1/users | GET | JWT | query: {id?} | 200: User[] |
| /v1/users | POST | JWT | body: {email, name} | 201: User |

