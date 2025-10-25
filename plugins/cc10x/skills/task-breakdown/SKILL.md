---
name: task-breakdown
description: Breaks down feature plans into actionable Claude Code tasks with file size constraints and dependencies. Use when converting comprehensive plans or PRDs into TODO lists for implementation. Ensures each task respects 500-line file limit and marks dependencies clearly for sequential execution.
license: MIT
---

# Task Breakdown Skill

Converts feature plans into actionable task lists compatible with Claude Code, enforcing file size constraints.

## When to Use

This skill is invoked by the BUILD workflow (Phase 2) to convert comprehensive plans into concrete implementation tasks.

## Input

Receives:
- PRD document from `.claude/plans/{feature-name}-prd.md`
- Architecture document (if exists)
- File change manifest (if exists from planning Phase 5b)

## Output Format

Generate `.claude/tasks/TODO.md`:

```markdown
# [Feature Name] - Implementation Tasks

## Phase 1: Setup
- [ ] Task 1: Setup project structure
  - Create directories: auth/, auth/__tests__/
  - Add to .gitignore if needed
  
- [ ] Task 2: Install dependencies
  - bcrypt@5.1.1 (password hashing)
  - jsonwebtoken@9.0.2 (JWT tokens)
  - Run: npm install bcrypt jsonwebtoken

- [ ] Task 3: Configure development environment
  - Add env vars: JWT_SECRET, JWT_EXPIRY
  - Create .env.example template

## Phase 2: Core Implementation
- [ ] Task 4: Implement auth service (<400 lines)
  - Create UserService class
  - Add JWT token generation
  - Implement session management
  - File: `src/auth/service.ts`
  - Tests: Unit tests for all methods
  
- [ ] Task 5: Create login component (<200 lines)
  - Build form with validation
  - Add error handling
  - Implement loading states
  - File: `src/components/LoginForm.tsx`
  - Tests: Component tests with React Testing Library
  
- [ ] Task 6: Add validation utilities (<300 lines)
  - Email validation
  - Password strength checking
  - Input sanitization
  - File: `src/auth/validation.ts`
  - Tests: Edge cases (null, malformed, injection)

## Phase 3: Testing
- [ ] Task 7: Write unit tests (>80% coverage)
  - Auth service tests (30+ tests)
  - Component tests (15+ tests)
  - Utility tests (10+ tests)
  - Target: Functions 100%, Branches >80%, Lines >90%
  
- [ ] Task 8: Integration tests
  - Login flow end-to-end
  - Token refresh flow
  - Session handling
  - Error scenarios (invalid credentials, expired tokens)

## Phase 4: Documentation
- [ ] Task 9: API documentation
  - Document endpoints (POST /auth/login, /auth/register, /auth/refresh)
  - Add request/response examples
  - Include error codes and meanings
  
- [ ] Task 10: README updates
  - Usage instructions for authentication
  - Configuration guide (env vars)
  - Deployment steps

## Dependencies
- Task 4 → Task 5 (component needs service)
- Task 4 → Task 6 (validation used by service)
- Task 5,6 → Task 7 (tests need implementation)
- Task 4,5,6 → Task 8 (integration tests need all components)

## Estimates
- Phase 1: 30 min
- Phase 2: 4-6 hours
- Phase 3: 2-3 hours
- Phase 4: 1-2 hours
Total: ~8-12 hours
```

## Task Guidelines

### File Size Constraints (USER RULE - CRITICAL)

Break tasks to ensure files stay under 500 lines:
- Components: <200 lines per file
- Utilities: <300 lines per file
- Services: <400 lines per file
- Config: <100 lines per file

**If a task would create a larger file, split it:**

❌ Bad:
```markdown
- [ ] Implement authentication system (800 lines in one file)
```

✅ Good:
```markdown
- [ ] Implement auth service (<400 lines)
  - File: src/auth/service.ts
  
- [ ] Implement auth middleware (<200 lines)
  - File: src/auth/middleware.ts
  
- [ ] Implement token utilities (<300 lines)
  - File: src/auth/token.ts
```

### Task Specificity

Be specific and actionable:

❌ Vague:
```markdown
- [ ] Add authentication
```

✅ Specific:
```markdown
- [ ] Implement JWT authentication service
  - User login with email/password
  - Token generation (15min access, 7-day refresh)
  - Token validation middleware
  - Refresh token rotation
  - File: src/auth/service.ts (<400 lines)
  - Tests: 25+ unit tests covering edge cases
```

### Include Quality Tasks

Always include:
- Testing tasks (>80% coverage explicitly stated)
- Error handling verification
- Input validation checks
- Documentation updates
- Code review checkpoints (run REVIEW workflow)
- File size validation

### Dependencies

Clearly mark dependencies:
```markdown
- [ ] Task A: Create User model
- [ ] Task B: Create auth service (depends on Task A)
- [ ] Task C: Create login endpoint (depends on Task A, Task B)
```

### Validation Checkpoints

Add validation tasks between phases:
```markdown
## Phase 2: Core Implementation
[...implementation tasks...]

## Validation Checkpoint
- [ ] Validate file sizes (all <500 lines)
- [ ] Run linter (0 errors)
- [ ] Check test coverage (>80%)
- [ ] Run security scan (0 CRITICAL)

## Phase 3: Testing
[...testing tasks...]
```

## Task Breakdown Patterns

### For New Features

```markdown
## Phase 1: Planning & Setup
- [ ] Review PRD and architecture
- [ ] Identify dependencies
- [ ] Setup directory structure

## Phase 2: Foundation
- [ ] Data models (<200 lines each)
- [ ] Service layer (<400 lines each)
- [ ] Type definitions (<200 lines)

## Phase 3: Implementation
- [ ] Core logic (<400 lines per file)
- [ ] UI components (<200 lines each)
- [ ] Integration layer (<300 lines)

## Phase 4: Quality
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Error handling review
- [ ] File size validation

## Phase 5: Documentation
- [ ] API documentation
- [ ] README updates
- [ ] Inline comments for complex logic
```

### For Refactoring

```markdown
## Phase 1: Analysis
- [ ] Identify code to refactor
- [ ] Document current behavior
- [ ] Define success criteria
- [ ] Establish baseline tests

## Phase 2: Testing Safety Net
- [ ] Add tests for current behavior (>80% coverage)
- [ ] Verify all tests pass (baseline)

## Phase 3: Refactoring
- [ ] Refactor module 1 (<500 lines after split)
  - Ensure tests still pass after each change
- [ ] Refactor module 2 (<500 lines after split)
- [ ] Verify no behavior changes

## Phase 4: Validation
- [ ] All tests still pass
- [ ] Check performance (no degradation)
- [ ] Update documentation
- [ ] Run REVIEW workflow
```

### For Bug Fixes

```markdown
## Phase 1: Investigation
- [ ] Reproduce bug consistently
- [ ] Add logging (LOG FIRST pattern)
- [ ] Identify root cause from logs
- [ ] Document expected behavior

## Phase 2: Fix with TDD
- [ ] Write failing regression test
- [ ] Implement minimal fix
- [ ] Verify test passes
- [ ] Verify all tests pass (no new issues)

## Phase 3: Prevention
- [ ] Add tests for related edge cases
- [ ] Update validation logic if needed
- [ ] Document learnings
- [ ] Check for similar bugs elsewhere
```

## Estimation Guidelines

Provide rough time estimates:
- Simple task (CRUD operations): 1-2 hours
- Medium task (service logic): 2-4 hours
- Complex task (integration, novel patterns): 4-8 hours
- Testing: 25-50% of implementation time
- Documentation: 10-15% of total time

## Best Practices

1. **One task per file/component** when possible
2. **Group related tasks** into logical phases
3. **Mark dependencies** explicitly
4. **Include validation** after each phase
5. **Add buffer time** for unexpected issues
6. **Break down large tasks** (>4 hours → split)
7. **Include non-coding tasks** (review, deploy, documentation)
8. **Reference file size limits** in every task
9. **Specify test coverage targets** (>80%)
10. **Note integration points** for each task

## Output Checklist

Before delivering TODO.md:
- [ ] All tasks are specific and actionable
- [ ] File size constraints noted (<500 lines per file)
- [ ] Dependencies clearly marked
- [ ] Testing tasks included (>80% coverage target)
- [ ] Documentation tasks included
- [ ] Phases logically organized
- [ ] Estimates provided
- [ ] Validation checkpoints between phases

## Integration with BUILD Workflow

**When BUILD workflow invokes this skill:**

1. Load plan from `.claude/plans/FEATURE_[NAME].md`
2. Extract requirements, architecture, file manifest
3. Generate TODO.md with file-size-aware task breakdown
4. Save to `.claude/tasks/TODO.md`
5. Return control to BUILD workflow (Phase 3 proceeds with tasks)

## Remember

Your task breakdown directly guides implementation. Good task breakdown prevents:
- File size violations (by splitting early)
- Scope creep (by being specific)
- Missing tests (by including explicitly)
- Integration issues (by marking dependencies)

**Make tasks concrete, actionable, and file-size-aware.**
