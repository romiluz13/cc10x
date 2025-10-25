# BUILDING Workflow

**TDD Implementation with Risk Analysis**

## When to Use

Use this workflow for:
- Implementing features from plans
- Building complex systems (complexity 4-5)
- Want strict TDD enforcement
- Need systematic quality assurance

**Skip for:**
- Simple features (1-2 complexity: manual is 8-16x cheaper and often better)
- Time-sensitive implementations
- Prototypes/MVPs (iterate fast first)

---

## Phase 0: Complexity & Plan Check

### Complexity Check (STRONG GATE!)

**IF Complexity <= 2:**

Present strong warning:

```markdown
⚠️ STOP: This is a SIMPLE feature (complexity 2/5)

Building with cc10x will cost 80k tokens vs 5k manual.

Real Test Case: Rate limiting (complexity 2)
- cc10x BUILD: 100k tokens, reported "tests passing", actually 3/7 FAILED
- Manual: 30 min, 5k tokens, working code from library docs
- Verdict: cc10x was WORSE for simple feature

Strongly recommend manual implementation.

OPTIONS:
(a) Manual - I'll provide implementation guidance (saves 75k tokens)
(b) Systematic - I'll use full TDD workflow anyway (costs 80k tokens)

Which do you choose?
```

**Wait for user response:**
- IF (a): Provide quick guidance, stop workflow
- IF (b): Warn "This will use 80k tokens for a simple feature", proceed

**IF Complexity >= 4:**

Announce confidently:

```markdown
✅ Complex feature (4/5). Systematic TDD valuable. Proceeding...
```

Continue to plan check.

### Plan Check

**Check for existing plan:**

```
IF .claude/plans/FEATURE_*.md exists:
  → "Found plan: [filename]. Using as blueprint..."
  → Load plan, extract file manifest, architecture
  → Proceed to Phase 1
  
IF no plan exists:
  → "No feature plan found. Recommend running PLANNING workflow first.
     
     OPTIONS:
     (a) Create plan first (recommended - prevents architecture mistakes)
     (b) Build without plan (faster but ad-hoc, higher risk)
     
     Which?"
  → Wait for response
  → IF (a): Switch to PLANNING workflow
  → IF (b): Proceed with ad-hoc building (warn about risks)
```

---

## Phase 1: Context Analysis

**Process:** Use `codebase-navigation` skill to find patterns

**Activities:**
1. Search for similar features
2. Extract project conventions (naming, structure, error handling)
3. Map dependencies
4. Identify reusable components
5. Recommend file locations

**Output:**
- Similar feature examples for pattern reference
- Project conventions to follow
- Dependency map
- Recommended file structure

---

## Phase 2: Task Breakdown

**Process:** Use `task-breakdown` skill (NEW in v3)

**Activities:**
1. Load plan from `.claude/plans/FEATURE_*.md`
2. Convert to Claude Code compatible TODO.md
3. Break into <500 line increments
4. Mark dependencies clearly
5. Add quality validation tasks

**Output:** Save to `.claude/tasks/TODO.md`

```markdown
# [Feature Name] - Implementation Tasks

## Phase 1: Foundation
- [ ] Task 1: Create auth service (<400 lines)
- [ ] Task 2: Add validation utilities (<200 lines)
- [ ] Task 3: Create type definitions (<150 lines)

## Phase 2: Core Logic
- [ ] Task 4: Implement JWT token generation (<300 lines)
  - Depends on: Task 1, Task 3
- [ ] Task 5: Implement token verification (<250 lines)
  - Depends on: Task 1, Task 3

## Phase 3: API Layer
- [ ] Task 6: Create login endpoint (<200 lines)
  - Depends on: Task 1, Task 4
- [ ] Task 7: Create register endpoint (<200 lines)
  - Depends on: Task 1, Task 2

## Phase 4: Testing
- [ ] Task 8: Unit tests for auth service (>80% coverage)
- [ ] Task 9: Integration tests for API endpoints
- [ ] Task 10: E2E tests for login flow

## Phase 5: Quality
- [ ] Task 11: Review (run REVIEW workflow)
- [ ] Task 12: Documentation (README, API docs)
```

---

## Phase 3: TDD Implementation (Sequential!)

**NEVER parallelize implementation - do ONE increment at a time!**

### For Each Increment:

**Invoke:** `code-writer` sub-agent for each task

#### Increment Workflow (9 Steps)

**Step 0: Risk Analysis - What Could Go Wrong?**

Before writing ANY code, analyze risks:

**Loads:** `risk-analysis` skill Stages 1+3+7
- Stage 1: Data Flow (input edge cases)
- Stage 3: Timing (race conditions, state)
- Stage 7: Failure Modes (error handling)

**Process:**
```markdown
## Risk Analysis: [Increment Name]

What am I about to implement?
[Brief description]

Critical Dimensions:
1. Data Flow: What transformations? Where can data corrupt?
   - [Identified risks]
   
2. Timing/State: Any race conditions? State issues?
   - [Identified risks]
   
3. Failure Modes: What can fail? How to handle?
   - [Identified risks]

Identified Risks → Become Test Cases:
1. Risk: [Description] → Test: [Test case]
2. Risk: [Description] → Test: [Test case]

Implementation Strategy Adjustments:
- [How to prevent these risks]
- [Additional validation needed]
- [Edge cases to explicitly handle]
```

---

**Step 1: RED - Write Failing Test**

Write test FIRST that defines expected behavior (including edge cases from risk analysis):

```typescript
describe('UserService.createUser', () => {
  // Happy path
  it('should hash password before storing', async () => {
    const user = await userService.createUser({
      email: 'test@example.com',
      password: 'plaintext'
    });
    
    expect(user.password).not.toBe('plaintext');
    expect(user.password).toMatch(/^\$2[ayb]\$/); // bcrypt pattern
  });
  
  // Edge cases from risk analysis
  it('should throw ValidationError for null email', async () => {
    await expect(userService.createUser({ email: null, password: 'test' }))
      .rejects.toThrow(ValidationError);
  });
  
  it('should throw ValidationError for malformed email', async () => {
    await expect(userService.createUser({ email: 'not-an-email', password: 'test' }))
      .rejects.toThrow(ValidationError);
  });
  
  it('should sanitize email to prevent injection', async () => {
    const malicious = "test@example.com' OR '1'='1";
    // Should either throw or sanitize
  });
  
  it('should handle duplicate email gracefully', async () => {
    await userService.createUser({ email: 'test@test.com', password: 'pass' });
    await expect(userService.createUser({ email: 'test@test.com', password: 'pass' }))
      .rejects.toThrow(DuplicateError);
  });
});
```

**Run test - MUST see FAIL:**
```bash
npm test -- UserService.createUser
# Expected output: FAIL (implementation doesn't exist)
```

---

**Step 2: Verify Test Fails for RIGHT Reason**

Check error message:
```
✅ Good: "Cannot find module './UserService'" (code doesn't exist)
❌ Bad: "Timeout" (test setup broken)
```

---

**Step 3: GREEN - Minimal Implementation**

Implement JUST enough to make tests pass:

```typescript
export class UserService {
  async createUser(data: { email: string; password: string }): Promise<User> {
    // Validation (from risk analysis)
    if (!data.email || !this.isValidEmail(data.email)) {
      throw new ValidationError('Invalid email');
    }
    
    // Check duplicate (from risk analysis)
    const existing = await User.findOne({ email: data.email });
    if (existing) {
      throw new DuplicateError('Email already exists');
    }
    
    // Hash password (from test requirement)
    const hashedPassword = await bcrypt.hash(data.password, 12);
    
    // Store
    const user = await User.create({
      email: data.email,
      password: hashedPassword
    });
    
    return user;
  }
  
  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

---

**Step 4: Verify Test Passes**

Run test again:
```bash
npm test -- UserService.createUser
# Expected: PASS (all 5 tests green)
```

---

**Step 5: Verify ALL Tests Pass (No Regressions)**

Run FULL test suite:
```bash
npm test
# Expected: All existing tests + new tests pass
```

---

**Step 6: REFACTOR - Improve Code Quality**

Now refactor with tests as safety net:

```typescript
// Extract validation (DRY)
import { validateEmail } from './validation';

// Extract password hashing (Single Responsibility)
import { hashPassword } from './crypto';

export class UserService {
  async createUser(data: CreateUserDTO): Promise<User> {
    // Validation
    this.validateUserData(data);
    
    // Check duplicates
    await this.ensureEmailUnique(data.email);
    
    // Business logic
    const hashedPassword = await hashPassword(data.password);
    
    // Persistence with error handling
    try {
      const user = await User.create({
        email: data.email,
        password: hashedPassword
      });
      
      logger.info('User created', { userId: user.id });
      return user;
    } catch (error) {
      logger.error('User creation failed', { error, email: data.email });
      throw new DatabaseError('Failed to create user', { cause: error });
    }
  }
  
  private validateUserData(data: CreateUserDTO): void {
    if (!validateEmail(data.email)) {
      throw new ValidationError('Invalid email format');
    }
    if (data.password.length < 8) {
      throw new ValidationError('Password must be at least 8 characters');
    }
  }
  
  private async ensureEmailUnique(email: string): Promise<void> {
    const existing = await User.findOne({ email });
    if (existing) {
      throw new DuplicateError('Email already registered');
    }
  }
}
```

---

**Step 7: Verify Tests Still Pass After Refactor**

```bash
npm test
# Expected: All tests still green
```

---

**Step 8: File Manifest Verification**

Check implementation matches plan:

```markdown
## File Manifest Check - Increment 1

Planned (from Phase 5b of PLANNING workflow):
- CREATE: `src/services/UserService.ts` (~350 lines)
- CREATE: `src/validation/index.ts` (~200 lines)
- CREATE: `src/crypto/password.ts` (~150 lines)

Actual:
- ✅ `src/services/UserService.ts` (287 lines) - Within ±30%
- ✅ `src/validation/index.ts` (178 lines) - Within ±30%
- ✅ `src/crypto/password.ts` (134 lines) - Within ±30%

Unplanned Files:
- None (good - no scope creep)

Integration Points Verified:
- ✅ UserService → validation module
- ✅ UserService → crypto module
- ✅ UserService → User model

Status: ✅ Matches plan
```

---

**Step 9: MANDATORY Test Verification (CRITICAL!)**

**NEVER trust "tests passing" reports!**

During v2 testing, code-writer reported:
> "✅ All 33 tests passing!"

**Reality:** 3 out of 7 tests FAILED

**Mandatory Verification Process:**

1. Run tests independently:
```bash
npm test
```

2. Capture ACTUAL output (don't summarize):
```
PASS tests/auth.test.js
  ✓ should hash password before storing (45ms)
  ✓ should throw ValidationError for null email (12ms)
  ✓ should throw ValidationError for malformed email (15ms)
  ✓ should sanitize inputs (23ms)
  ✓ should handle duplicate email (38ms)

Tests: 5 passed, 5 total
Time: 1.234s
```

3. Verify exit code:
```bash
echo $?
# Must output: 0
```

4. **SEE with YOUR EYES:** Green checkmarks, "X passed, X total"

5. **Report to user:**
```markdown
## ⚠️ MANDATORY USER VERIFICATION REQUIRED

I have completed Increment 1. Tests appear to pass, but historical testing showed false reports.

YOU MUST verify independently:

Run this command:
```bash
npm test
```

Verify you see:
- Tests: X passed, X total (no failures)
- Exit code: 0

DO NOT proceed to Increment 2 until you've personally confirmed tests pass.

Reply with: "Verified: All tests passing" to continue.
```

**Wait for user confirmation before next increment.**

---

### Repeat for All Increments

Execute Steps 0-9 for EACH increment sequentially.

**Do NOT parallelize!** Each increment builds on previous ones.

---

## Phase 4: Comprehensive Test Generation

**Invoke:** `test-generator` sub-agent

**Agent will:**
1. Analyze all implemented code
2. Identify test gaps
3. Create comprehensive test suite
4. Target >80% coverage
5. Include: unit, integration, e2e tests (based on complexity)

**Output:**
- Test files created
- Expected coverage (Functions: 100%, Branches: >80%, Lines: >90%)
- Mandatory user verification instructions

**Complexity Scaling:**
- Simple: 10-20 tests
- Moderate: 30-50 tests
- Complex: 80-200 tests

---

## Phase 5: Multi-Dimensional Review

**Invoke:** 5 review agents IN PARALLEL

**Same as REVIEW workflow:**
- security-reviewer
- quality-reviewer
- performance-analyzer
- ux-reviewer
- accessibility-reviewer

**Purpose:** Find issues before considering "done"

**Action:** Fix ALL CRITICAL findings before Phase 6

---

## Phase 6: Finalization

**Tasks:**

1. **Remove debug code:**
   - All console.log statements
   - debugger statements
   - Commented-out code
   - TODO comments

2. **Update documentation:**
   - README if public APIs changed
   - API documentation
   - Inline comments for complex logic

3. **Final manifest verification:**
   ```markdown
   ## Final Manifest Verification
   
   Planned files: [X]
   Created files: [Y]
   Match rate: [%]
   
   Unplanned files: [list if any] - Scope creep indicator
   
   LOC planned: [X]
   LOC actual: [Y]
   Variance: [%] (±30% acceptable)
   ```

4. **Create commit message:**
   ```
   feat: [feature-name]
   
   - [What was implemented]
   - [Key components created]
   - [Tests added: X passing, >80% coverage]
   
   Complexity: [X]/5
   Files: [created X, modified Y]
   LOC: [~Z lines]
   Tests: [N tests, M% coverage]
   ```

5. **Stage changes:**
   ```bash
   git add .
   git status  # Review what's being committed
   ```

**Output:** Production-ready code, staged and ready to commit

---

## Output Format

After building complete:

```markdown
## Implementation Complete

### Files Created/Modified
- `src/auth/service.ts` (352 lines) - Authentication service
- `src/auth/middleware.ts` (187 lines) - Auth middleware
- `src/auth/types.ts` (124 lines) - TypeScript types
- `src/auth/__tests__/service.test.ts` (198 lines) - Unit tests
- `src/auth/__tests__/integration.test.ts` (165 lines) - Integration tests

### Implementation Summary
Implemented JWT authentication system with:
- Email/password registration
- Token generation and validation
- Refresh token rotation
- Rate limiting protection
- Comprehensive error handling

### TDD Cycles Completed
- 12 increments (RED-GREEN-REFACTOR each)
- 47 tests written before implementation
- Coverage: Functions 100%, Branches 94%, Lines 96%
- **User verified: All tests passing ✅**

### Risk Mitigations Implemented
- Data validation: Email format, password strength
- Security: bcrypt hashing (cost 12), SQL injection prevention
- Concurrency: Duplicate email check with transaction
- Error handling: All failure paths covered with meaningful messages
- Failure modes: Database errors, external service failures handled

### Review Findings Addressed
- CRITICAL: 0 (none found or all fixed)
- HIGH: 2 fixed (memory leak in token generation, N+1 query)
- MODERATE: 5 fixed (code smells, UX improvements)

### File Manifest Verification
- ✅ Planned files: 8
- ✅ Created files: 8
- ✅ Match rate: 100%
- ✅ Unplanned files: 0 (no scope creep)
- ✅ LOC variance: -8% (planned 1,200, actual 1,104)

### Dependencies Added
- `bcrypt@5.1.1` - Password hashing
- `jsonwebtoken@9.0.2` - JWT tokens
- `express-rate-limit@7.1.5` - Rate limiting

### Git Status
```bash
# Changes staged and ready to commit:
# 8 files created
# 3 files modified
# Commit message prepared
```

### Next Steps
- ✅ All tests passing (user verified)
- ✅ No CRITICAL review findings
- ✅ File manifest matches plan
- ✅ Ready to commit
- **Recommended:** Run final `npm test` one more time, then commit

---

## ⚠️ MANDATORY USER ACTIONS

Before considering this complete:

1. **Run final test verification:**
   ```bash
   npm test
   ```
   Confirm: All tests pass, coverage >80%

2. **Review changes:**
   ```bash
   git diff --cached
   ```
   Verify: No debug code, no TODOs, looks production-ready

3. **Commit when ready:**
   ```bash
   git commit
   # Use prepared commit message or edit
   ```

DO NOT skip these verifications!
```

---

## Token Economics

**Total Building Cost:**

**By Complexity:**
- Simple (3): 40k-60k tokens (vs 5-15k manual = 8-12x MORE)
- Medium (4): 60-100k tokens (vs 15-30k manual = 4-6x MORE)
- Large (5): 100-150k tokens (vs 30-50k manual = 3-5x MORE)

**Breakdown:**
- Phase 0: Complexity check (1k)
- Phase 1: Context analysis (2k)
- Phase 2: Task breakdown (3k)
- Phase 3: TDD implementation (30-100k) - varies by complexity
- Phase 4: Test generation (5-20k)
- Phase 5: Review (15-25k)
- Phase 6: Finalization (2k)

**vs Manual:**
- Just implement it: 5-50k tokens (depending on complexity)
- **cc10x costs 2-16x MORE**

**Worth it when:**
- Complexity 4-5 (prevents architecture mistakes, security issues)
- High-risk (auth, payments - one bug = infinite cost)
- Want strict TDD enforcement

**NOT worth it when:**
- Complexity 1-2 (manual faster, cheaper, often better)
- Time-sensitive
- Familiar pattern

---

## Common Issues & Solutions

### Issue: Tests Reported Passing But Actually Failed

**Symptom:** Agent says "All tests passing" but they're not

**Solution:** MANDATORY user verification (Step 9)
- Run `npm test` yourself
- See actual output
- Verify exit code = 0
- Don't trust reports

### Issue: File Size Exceeded During Implementation

**Symptom:** File approaches 500 lines

**Solution:** Split immediately
- Extract utilities (<300 lines)
- Extract types (<200 lines)
- Create focused modules
- Refactor keeps tests passing

### Issue: Scope Creep (Unplanned Files)

**Symptom:** File manifest shows unplanned files created

**Solution:**
- Review: Is this scope creep or necessary?
- If necessary: Update plan, document reason
- If creep: Remove, stay focused on plan

### Issue: Implementation Doesn't Match Architecture

**Symptom:** Code differs from architecture design

**Solution:**
- Stop and analyze why
- If better approach found: Update architecture doc, document reason
- If misunderstanding: Refactor to match architecture
- Don't let implementation drift from design

---

## Success Indicators

Building workflow successful if:
- [ ] All increments completed with TDD
- [ ] All tests passing (user verified)
- [ ] Coverage >80%
- [ ] All files <500 lines
- [ ] No placeholders or TODOs
- [ ] Review findings addressed (CRITICAL fixed)
- [ ] File manifest matches plan (±30%)
- [ ] No scope creep
- [ ] Production-ready code staged

---

## Remember

This workflow enforces systematic quality through:
- **Risk analysis before each increment** (prevents edge cases)
- **TDD (RED-GREEN-REFACTOR)** (prevents bugs)
- **Mandatory verification** (prevents false success)
- **File size enforcement** (prevents bloat)
- **Manifest tracking** (prevents scope creep)

**The value is in quality and systematization, not speed.**

**Use for complexity 4-5. Skip for 1-2. Decide for 3.**

