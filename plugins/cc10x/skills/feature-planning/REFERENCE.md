# Feature Planning - Reference

Reference templates, examples, and decision frameworks for feature planning. Use AFTER understanding functionality (see SKILL.md).

## Requirements Template

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

## Architecture Template

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

## Risk Register Template

```markdown
## Risks

| Stage | Risk Description | Probability | Impact | Mitigation | Owner |
|-------|------------------|-------------|--------|-----------|-------|
| <Framework stage> | <What could go wrong> | H/M/L | H/M/L | <How we'll prevent/handle> | <Team/person> |
````

## Implementation Roadmap Template

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

## Risk Scoring Guide

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

## Verification Reminder

Always end planning with a verification summary:

```markdown
## Planning Verification

**Inputs Reviewed**:

- [ ] User requirements gathered from stakeholders
- [ ] Existing patterns in codebase analyzed
- [ ] Best practices consulted

**Outstanding Questions**:

- <Question requiring stakeholder input>

**Follow-Up Tasks**:

- <Task to complete before implementation>

**Next Step**: Proceed to BUILD workflow with this plan
```

## Detailed Implementation Plan Creation

### Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

**If tests are included (for complex behavior):**

- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

**If no tests (for simple changes):**

- "Implement the code" - step
- "Verify with typecheck/lint" - step
- "Commit" - step

### Testing Strategy

**Auto-decide whether unit tests are needed based on complexity:**

- **Include tests for**: Complex algorithms, business logic, data transformations where bugs are likely
- **Skip tests for**: Simple CRUD, UI components, straightforward mappings, anything you're 100% certain is bug-free
- **Test type**: Only deterministic unit tests - no integration tests, no complex mocking, no async complexity
- Tests should verify logic, not implementation details

### Key Principles

- Auto-decide on unit tests - only for complex logic where bugs are likely
- Only deterministic unit tests - no integration/async/complex mocking
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, frequent commits
- TypeScript syntax for all examples
