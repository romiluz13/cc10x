---
name: feature-build
description: Complete feature implementation with TDD enforcement (RED-GREEN-REFACTOR), context-aware pattern following, automatic quality gates, multi-dimensional verification, and clean semantic commits
aliases: [build, implement, develop]
category: development
priority: 10
---

# Feature Build Command

Implement complete features using strict Test-Driven Development (TDD) with automatic quality gates and multi-dimensional verification. This command orchestrates the full development lifecycle from context analysis through implementation to final verification and clean commits.

Perfect for building production-ready features that follow project patterns and maintain high quality standards.

## What This Does

This command orchestrates a 5-phase development workflow:

- **Phase 1: Context Analysis** - Automatically finds similar patterns in your codebase to follow
- **Phase 2: Planning** - Breaks feature into small, testable increments
- **Phase 3: Implementation** - TDD-enforced sequential development (RED → GREEN → REFACTOR)
- **Phase 4: Verification** - Multi-dimensional quality checks (security, performance, quality, UX, accessibility)
- **Phase 5: Finalization** - Clean commit with semantic message

**Key Features:**
- ✅ **Strict TDD Enforcement** - No production code without failing test first
- ✅ **Pattern Following** - Automatically adopts your project's conventions
- ✅ **Quality Gates** - Must pass before proceeding to next phase
- ✅ **Progressive Loading** - 93% token savings via staged context loading
- ✅ **Auto-Healing** - Snapshots at 75% token usage prevent context loss
- ✅ **File Conflict Prevention** - Sequential implementation (never parallel)
- ✅ **Lovable/Bolt Quality UI** - Production-ready components, not prototypes

## When to Use

Use `/feature-build` when you need to:

- **Implement a planned feature** - You have a plan (from `/feature-plan` or in your head)
- **Build with TDD** - You want test-first development enforced
- **Follow project patterns** - You want automatic pattern discovery and adherence
- **Ensure quality** - You want multi-dimensional verification before commit
- **Ship production code** - You need polished, complete, deployment-ready code

**Don't use when:**
- Just planning (use `/feature-plan` first)
- Fixing bugs (use `/bug-fix` instead - includes LOG FIRST pattern)
- Reviewing code (use `/review` instead)
- Making trivial changes (< 20 lines, just edit directly)

## Workflow

### Phase 1: Context Analysis (Automatic)

**Goal:** Understand existing codebase patterns to follow

**Sub-Agent:** context-analyzer

**Process:**
1. **Find Similar Features**
   - Search for features similar to what you're building
   - Identify existing implementations to learn from
   - Extract patterns and conventions

2. **Identify Project Conventions**
   - Naming conventions (camelCase vs snake_case, etc.)
   - File structure patterns (where things go)
   - Error handling approaches
   - Validation patterns
   - Testing patterns

3. **Map Integration Points**
   - Database connections and models
   - API endpoints and routing
   - External services and dependencies
   - State management patterns

4. **Understand Dependencies**
   - What this feature depends on
   - What might depend on this feature
   - Potential breaking changes

**Quality Gate:** Clear understanding of patterns to follow

**Output Example:**
```markdown
## Context Analysis Results

### Similar Features Found
- Authentication: src/features/auth/ (JWT-based, follows middleware pattern)
- User Management: src/features/users/ (CRUD with validation)

### Project Conventions
- **File Structure:** Feature-based (src/features/{name}/)
- **Naming:** camelCase for files, PascalCase for components
- **Error Handling:** Custom AppError class, centralized error middleware
- **Validation:** Joi schemas in validators/ subfolder
- **Testing:** Jest, tests in __tests__/ alongside code

### Integration Points
- **Database:** MongoDB with Mongoose (src/config/database.ts)
- **API Routes:** Express router in routes/ subfolder
- **Middleware:** Auth middleware at src/middleware/auth.ts

### Dependencies
- Depends on: User model, Auth middleware
- Impacts: None (new feature)
```

---

### Phase 2: Planning (Automatic)

**Goal:** Break feature into small, testable increments

**Process:**
1. **Decompose Feature**
   - Break into smallest independently valuable pieces
   - Each increment should be < 200 lines of code
   - Order by dependencies (what needs what)

2. **Define Test-First Approach**
   - Specify what test to write first for each increment
   - Identify test data needed
   - Plan assertions

3. **Identify Parallel vs Sequential**
   - What can be built in parallel (independent components)
   - What must be sequential (dependencies)
   - **CRITICAL:** Only ONE implementer at a time (prevent conflicts)

4. **Set Quality Gates**
   - Define "done" criteria for each increment
   - Specify coverage targets (>80%)
   - Plan verification steps

**Quality Gate:** Clear, actionable implementation plan

**Output Example:**
```markdown
## Implementation Plan

### Increment 1: Payment Model (Sequential, 1-2 hours)
**Goal:** Create database model for payments

**Test First:**
```javascript
describe('Payment Model', () => {
  it('should create payment with required fields', async () => {
    const payment = await Payment.create({
      userId: 'user123',
      amount: 29.99,
      currency: 'USD',
      status: 'pending'
    });
    expect(payment).toBeDefined();
    expect(payment.status).toBe('pending');
  });
});
```

**Implementation:**
1. Create src/features/payments/models/payment.ts
2. Define Mongoose schema
3. Add validation rules
4. Write 5+ unit tests

**Quality Gate:**
- All tests pass
- Coverage > 90%
- No linting errors

---

### Increment 2: Payment Service (Sequential, 2-3 hours)
**Goal:** Business logic for processing payments

[Continue for all increments...]
```

---

### Phase 3: Implementation (TDD-Enforced)

**Goal:** Build the feature with strict test-first development

**Sub-Agent:** implementer

**Process for EACH Increment:**

#### Step 1: RED (Write Failing Test)
```
1. Write test that defines desired behavior
2. Include edge cases
3. Make test specific and clear
4. Run test → MUST FAIL
5. Verify failure reason is correct
```

**CRITICAL RULE:** If test passes without implementation, test is wrong. Fix test first.

#### Step 2: GREEN (Make It Pass)
```
1. Write MINIMUM code to pass test
2. Don't add extra features
3. Don't optimize yet
4. Focus solely on making test green
5. Run test → MUST PASS
6. Run ALL tests → MUST ALL PASS
```

**CRITICAL RULE:** If existing tests break, fix immediately before proceeding.

#### Step 3: REFACTOR (Improve Quality)
```
1. Improve code structure (optional)
2. Extract reusable functions
3. Optimize performance if needed
4. Clean up duplication
5. Run ALL tests → MUST STILL PASS
```

**CRITICAL RULE:** Refactoring must not change behavior. Tests prove this.

#### Step 4: Verify Increment
```
1. Check coverage (>80% required)
2. Run linter (no errors allowed)
3. Verify patterns followed
4. Check no debug code (console.log, debugger, TODO)
5. Confirm quality gate met
```

#### Step 5: Move to Next Increment
```
Only after current increment is COMPLETE:
- Tests pass
- Coverage met
- Linting clean
- Quality gate passed
```

**Quality Gate:** All increments implemented with TDD, all tests passing, no linting errors

**Real-Time Example:**
```
🔴 RED: Writing test for Payment.create()...
✅ Test written: should create payment with required fields
❌ Test run: FAILED (Payment model doesn't exist) ← EXPECTED

🟢 GREEN: Writing Payment model...
✅ Model created: src/features/payments/models/payment.ts
✅ Test run: PASSED
✅ All tests run: PASSED (45/45)

🔵 REFACTOR: Extracting validation to helper...
✅ Refactored: validatePaymentAmount() helper
✅ All tests run: PASSED (45/45)

✅ INCREMENT 1 COMPLETE
Coverage: 92% | Tests: 45/45 passing | Linting: ✓ Clean

Moving to Increment 2...
```

---

### Phase 4: Verification (Multi-Dimensional)

**Goal:** Comprehensive quality check before commit

**Sub-Agents:** security-reviewer, quality-reviewer, performance-analyzer, ux-reviewer, accessibility-reviewer

**Process (Parallel Reviews):**

1. **Security Review**
   - Scan for vulnerabilities (SQL injection, XSS, etc.)
   - Check authentication/authorization
   - Verify input validation
   - Check for secrets in code
   - **BLOCKS commit if critical issues found**

2. **Quality Review**
   - Check code smells
   - Identify duplication
   - Assess maintainability
   - Verify patterns followed
   - **BLOCKS commit if major issues found**

3. **Performance Review**
   - Identify bottlenecks
   - Check for N+1 queries
   - Verify efficient algorithms
   - Check bundle size impact
   - **WARNS but doesn't block (can defer optimization)**

4. **UX Review**
   - Check error messages are clear
   - Verify loading states present
   - Assess user feedback
   - Check interaction patterns
   - **WARNS but doesn't block (can improve iteratively)**

5. **Accessibility Review**
   - Check WCAG 2.1 AA compliance
   - Verify keyboard navigation
   - Check screen reader support
   - Verify color contrast
   - **BLOCKS commit if critical a11y issues found**

**Quality Gate:** No critical issues, warnings acknowledged

**Output Example:**
```markdown
## Verification Results

### Security Review ✅ PASS
- ✅ Input validation present
- ✅ No secrets in code
- ✅ Authentication checked
- ✅ No SQL injection vectors
**Status:** Ready for commit

### Quality Review ✅ PASS
- ✅ No code smells detected
- ✅ Follows project patterns
- ✅ Test coverage 92% (target: 80%)
- ✅ No duplication
**Status:** Ready for commit

### Performance Review ⚠️ WARNINGS
- ⚠️ Payment.find() could use index on userId
- ℹ️ Consider pagination for payment list
**Status:** Can defer optimization, not blocking

### UX Review ⚠️ WARNINGS
- ⚠️ Error message "Invalid payment" could be more specific
- ℹ️ Consider adding loading spinner
**Status:** Can improve iteratively, not blocking

### Accessibility Review ✅ PASS
- ✅ ARIA labels present
- ✅ Keyboard navigation works
- ✅ Color contrast sufficient
**Status:** Ready for commit

---

**OVERALL:** ✅ Ready for commit (2 warnings to address in future)
```

---

### Phase 5: Finalization (Automatic)

**Goal:** Clean commit with semantic message

**Process:**
1. **Stage Changes**
   - Stage all modified files
   - Verify no unintended changes included
   - Check no sensitive data in commit

2. **Generate Semantic Commit Message**
   ```
   Format: <type>(<scope>): <subject>
   
   Types: feat, fix, refactor, test, docs, style, perf, chore
   Scope: feature name or component
   Subject: Present tense, lowercase, < 72 chars
   ```

3. **Commit**
   - Commit with generated message
   - Push to branch (if configured)

4. **Summary Report**
   - Files created/modified/deleted
   - Lines added/removed
   - Test coverage change
   - Build status

**Quality Gate:** Clean commit with descriptive message

**Output Example:**
```markdown
## Commit Summary

**Commit:** feat(payments): add payment processing with Stripe

**Changes:**
- Created: 8 files
- Modified: 3 files
- Deleted: 0 files

**Statistics:**
- Lines added: 487
- Lines removed: 12
- Net change: +475 lines

**Tests:**
- New tests: 24
- Total tests: 69
- Coverage: 91% (+3%)

**Status:** ✅ Committed to feature/payments branch

**Next Steps:**
1. Push to remote: `git push origin feature/payments`
2. Create PR for review
3. Run `/review src/features/payments/` for pre-PR check
```

---

## Examples

### Example 1: Building Authentication (With Existing Plan)

**Input:**
```bash
/feature-plan Add user authentication with JWT tokens
# Review plan...
/feature-build Implement authentication feature based on plan
```

**Process:**
```
Phase 1: Context Analysis
✅ Found similar pattern: src/features/auth/ (session-based)
✅ Conventions: Feature folders, Joi validation, Jest tests
✅ Integration: User model exists, Express app in src/app.ts

Phase 2: Planning
✅ Decomposed into 5 increments:
    1. User model updates (add password field)
    2. Auth controller (register, login, logout)
    3. JWT middleware
    4. Route protection
    5. Frontend integration

Phase 3: Implementation
🔴 Increment 1: Writing test for User.comparePassword()...
🟢 Increment 1: Implementing password hashing...
🔵 Increment 1: Refactoring to bcrypt helper...
✅ Increment 1 complete (3 files, 12 tests, 94% coverage)

[Continue for increments 2-5...]

✅ ALL INCREMENTS COMPLETE
- Files: 15 created, 4 modified
- Tests: 58 new (127 total)
- Coverage: 89%

Phase 4: Verification
✅ Security: No critical issues
✅ Quality: Follows patterns, no smells
⚠️ Performance: Consider caching JWT verification
✅ UX: Error messages clear
✅ Accessibility: N/A (API only)

Phase 5: Finalization
✅ Committed: feat(auth): add JWT authentication with register/login

**Time:** 8 hours
**Confidence:** High
```

**Output:**
```
✅ Feature Build Complete: Authentication

**Summary:**
- Components: User model, AuthController, AuthMiddleware, Auth routes
- Endpoints: POST /api/auth/register, POST /api/auth/login, POST /api/auth/logout
- Tests: 58 new tests, 127 total, 89% coverage
- Verification: PASSED (1 performance warning)
- Commit: feat(auth): add JWT authentication with register/login

**Files Created:**
- src/features/auth/controllers/auth.controller.ts
- src/features/auth/middleware/auth.middleware.ts
- src/features/auth/validators/auth.validator.ts
- src/features/auth/routes/auth.routes.ts
- src/features/auth/__tests__/ (8 test files)

**Next Steps:**
1. Push to remote: git push origin feature/auth
2. Create PR
3. Address performance warning (JWT caching) in future PR
```

---

### Example 2: Building UI Component (Lovable/Bolt Quality)

**Input:**
```bash
/feature-build Create a modern, accessible user profile card component
```

**Process:**
```
Phase 1: Context Analysis
✅ UI Framework: React with TypeScript
✅ Styling: Tailwind CSS (config at tailwind.config.js)
✅ Component Pattern: Functional components with hooks
✅ Testing: React Testing Library + Jest

Phase 2: Planning
✅ Decomposed into 3 increments:
    1. Basic profile card structure
    2. Responsive layout and interactions
    3. Accessibility and polish

Phase 3: Implementation
🔴 Increment 1: Writing test for ProfileCard renders user data...
🟢 Increment 1: Creating ProfileCard component...
🔵 Increment 1: Extracting Avatar subcomponent...
✅ Increment 1 complete

[Continue for increments 2-3...]

✅ ALL INCREMENTS COMPLETE
- Files: 4 created
- Tests: 15 new
- Coverage: 95%

Phase 4: Verification
✅ Security: N/A (no user input)
✅ Quality: Well-structured, reusable
✅ Performance: Optimized with memo
✅ UX: Smooth interactions, clear feedback, loading states
✅ Accessibility: WCAG 2.1 AA compliant, keyboard nav, ARIA labels, screen reader tested

Phase 5: Finalization
✅ Committed: feat(ui): add accessible profile card component

**Time:** 3 hours
**Confidence:** High
```

**Output:**
```
✅ Feature Build Complete: Profile Card Component

**Component Features:**
- ✅ Responsive (mobile, tablet, desktop)
- ✅ Dark mode support
- ✅ Loading skeleton state
- ✅ Error state handling
- ✅ Hover effects and animations
- ✅ WCAG 2.1 AA compliant
- ✅ Keyboard navigation
- ✅ Screen reader optimized
- ✅ 95% test coverage

**Files Created:**
- src/components/ProfileCard/ProfileCard.tsx
- src/components/ProfileCard/ProfileCard.test.tsx
- src/components/ProfileCard/ProfileCard.stories.tsx
- src/components/ProfileCard/index.ts

**Demo:**
<ProfileCard
  user={{
    name: "John Doe",
    email: "john@example.com",
    avatar: "/avatars/john.jpg",
    role: "Developer"
  }}
  onEdit={() => console.log('Edit')}
/>

**Next Steps:**
1. Import and use: import { ProfileCard } from '@/components/ProfileCard'
2. Review Storybook: npm run storybook
3. Push to remote: git push origin feature/profile-card
```

---

### Example 3: Database Migration

**Input:**
```bash
/feature-build Add user preferences table with migration
```

**Process:**
```
Phase 1: Context Analysis
✅ Database: PostgreSQL
✅ ORM: Prisma
✅ Migration Tool: Prisma Migrate
✅ Existing Tables: users, posts, comments

Phase 2: Planning
✅ Decomposed into 4 increments:
    1. Create migration file
    2. Define schema
    3. Write seed data
    4. Update user model to include preferences

Phase 3: Implementation
🔴 Increment 1: Writing test for preferences schema...
🟢 Increment 1: Creating migration...
[Continue...]

✅ ALL INCREMENTS COMPLETE
- Migration: 20231022_add_user_preferences.sql
- Schema updated
- Seed data added
- Tests: 12 new

Phase 4: Verification
✅ Security: SQL injection protected by Prisma
✅ Quality: Schema well-normalized
✅ Performance: Indexes on userId and updatedAt
✅ Migration: Tested up and down

Phase 5: Finalization
✅ Committed: feat(db): add user preferences table with migration

**Time:** 2 hours
**Confidence:** High
```

**Output:**
```
✅ Feature Build Complete: User Preferences Table

**Migration:**
- File: prisma/migrations/20231022_add_user_preferences/migration.sql
- Status: Applied successfully
- Rollback tested: ✅

**Schema:**
```sql
CREATE TABLE user_preferences (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  theme VARCHAR(20) DEFAULT 'light',
  notifications_enabled BOOLEAN DEFAULT true,
  language VARCHAR(10) DEFAULT 'en',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
```

**Next Steps:**
1. Run migration on staging: npm run prisma:migrate:deploy
2. Test on staging environment
3. Push to remote: git push origin feature/user-preferences
4. Deploy to production after testing
```

---

## Best Practices

### 1. **Plan First (When Possible)**
For complex features, run `/feature-plan` first. For simple features, `/feature-build` can plan automatically.

### 2. **Trust the TDD Process**
Write tests first. Always. Even when it feels slower. It's faster in the long run.

### 3. **Keep Increments Small**
Smaller increments = easier testing, faster feedback, less risk. Aim for < 200 lines per increment.

### 4. **Don't Skip Verification**
The multi-dimensional review catches issues before they become tech debt. Let it run.

### 5. **Address Warnings Strategically**
- **CRITICAL:** Fix before commit
- **WARNINGS:** Can defer but create tickets
- **INFO:** Nice to have, not required

### 6. **Review the Context Analysis**
If the command is following wrong patterns, the context analysis found wrong examples. Guide it explicitly.

### 7. **Commit Often**
The command commits at the end, but for large features you might want to commit per increment. That's fine.

### 8. **Read the Verification Report**
Don't just check if it passed. Read WHY. Learn from the feedback.

---

## Common Issues

### Issue: Tests are passing without implementation

**Symptom:** Test goes green immediately without writing code

**Cause:** Test isn't actually testing anything

**Solution:**
1. Check test has assertions
2. Verify test is actually running (not skipped)
3. Make test more specific
4. The implementer agent will catch this and fix the test

---

### Issue: Existing tests breaking

**Symptom:** New code breaks old tests

**Cause:** Changed behavior unintentionally

**Solution:**
1. Review what changed
2. Decide: Is new behavior correct?
   - **Yes:** Update old tests to reflect new behavior
   - **No:** Fix new code to maintain old behavior
3. The implementer agent stops and fixes immediately

---

### Issue: Context analysis found wrong patterns

**Symptom:** Command is following patterns you don't want

**Cause:** Context analysis found examples that aren't the pattern you want

**Solution:**
1. Be more explicit: `/feature-build Add auth using JWT (NOT session-based)`
2. Specify files to follow: `/feature-build Add payments following src/features/subscriptions/ pattern`
3. Override with explicit guidance

---

### Issue: Feature too large / running too long

**Symptom:** Implementation taking many hours, context filling up

**Cause:** Feature scope too large

**Solution:**
1. **Stop and split:** Break into smaller features
2. **Continue from plan:** If you have a plan, implement one increment at a time:
   - `/feature-build Implement increment 1 from plan: User model`
   - `/feature-build Implement increment 2 from plan: Auth controller`
3. **Auto-healing will save you:** At 75% token usage, automatic snapshot created

---

### Issue: Verification failing

**Symptom:** Critical issues found in verification phase

**Cause:** Code has security/quality/accessibility problems

**Solution:**
1. **Read the report carefully** - Understand what's wrong
2. **Fix the issues** - The command will guide you
3. **Re-run verification** - Must pass before commit
4. **Don't bypass** - Critical issues block commit for good reason

---

### Issue: Commit message not descriptive enough

**Symptom:** Generated commit message is too generic

**Cause:** Feature description was vague

**Solution:**
1. **Edit the commit message** - You can always amend: `git commit --amend`
2. **Be more specific next time:** 
   - Bad: `/feature-build Add payments`
   - Good: `/feature-build Add Stripe payment processing with webhook handling`

---

## Related Commands

### `/feature-plan`
**Use before** `/feature-build` for complex features.

**Workflow:**
```bash
/feature-plan Add real-time notifications
# Review plan...
/feature-build Implement notifications based on plan
```

---

### `/bug-fix`
**Use instead of** `/feature-build` when fixing issues.

**When to use which:**
- New functionality → `/feature-build`
- Broken functionality → `/bug-fix` (includes LOG FIRST pattern)

---

### `/review`
**Use after** `/feature-build` for additional verification before PR.

**Workflow:**
```bash
/feature-build Add user dashboard
/review src/features/dashboard/  # Pre-PR check
# Create PR
```

---

## Quality Gates Summary

Each phase has mandatory quality gates:

### Phase 1: Context Analysis
- ✅ Patterns identified
- ✅ Integration points mapped

### Phase 2: Planning
- ✅ Feature decomposed into increments
- ✅ TDD approach defined

### Phase 3: Implementation (per increment)
- ✅ Test written FIRST
- ✅ Test fails correctly (RED)
- ✅ Code makes test pass (GREEN)
- ✅ All tests pass (including existing)
- ✅ Coverage > 80%
- ✅ No linting errors
- ✅ No debug code

### Phase 4: Verification
- ✅ No critical security issues
- ✅ No major quality issues
- ✅ No critical accessibility issues
- ⚠️ Performance warnings acknowledged
- ⚠️ UX warnings acknowledged

### Phase 5: Finalization
- ✅ Changes staged correctly
- ✅ Semantic commit message
- ✅ No sensitive data in commit

**If ANY gate fails, process stops and issues must be fixed.**

---

## Token Usage

This command uses progressive loading and auto-healing:

### Progressive Loading (93% savings)
- **Stage 1:** Metadata only (~50 tokens)
- **Stage 2:** Context analysis (~500 tokens)
- **Stage 3:** Implementation details (~1,000-2,000 tokens per increment)

### Auto-Healing (Context Preservation)
- **At 75% token usage:** Automatic snapshot created
- **At 100%:** New context window with summary
- **Seamless continuation:** No loss of progress

**Typical usage:** 3,000-8,000 tokens for small features, 15,000-30,000 for large features

**Without progressive loading:** 50,000-100,000 tokens for same features

---

## Success Metrics

A successful feature build has:

- ✅ **Tests written first** - TDD cycle followed for all code
- ✅ **All tests passing** - New and existing
- ✅ **High coverage** - >80% (typically 85-95%)
- ✅ **No linting errors** - Clean code
- ✅ **No debug code** - No console.log, debugger, TODO
- ✅ **Patterns followed** - Matches project conventions
- ✅ **Verification passed** - No critical issues
- ✅ **Clean commit** - Semantic message, no extra files
- ✅ **Production-ready** - Can deploy immediately

**If missing any of these, feature is not complete.**

---

## Configuration

### TDD Enforcement
- **Strictness:** MAXIMUM (no exceptions)
- **Cycle:** RED → GREEN → REFACTOR (mandatory)
- **Test-first:** 100% (no code without test)

### File Conflict Prevention
- **Parallelization:** DISABLED for implementation
- **Sequential:** ONE increment at a time
- **Safe parallelization:** Only for analysis/review

### UI Quality Standard
- **Target:** Lovable/Bolt quality (production-ready)
- **Not acceptable:** Prototype, placeholder, "TODO: style this"
- **Requirements:** Responsive, accessible, polished

---

## Notes

- Implementation time varies: 2-20 hours depending on complexity
- TDD feels slower initially but prevents 5-10 hours of debugging
- Verification warnings are learning opportunities, not just boxes to check
- Auto-healing ensures you never lose progress on large features
- The command won't let you commit broken or low-quality code
- Trust the process, especially the TDD enforcement

