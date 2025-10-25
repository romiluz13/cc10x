# PLANNING Workflow

**Comprehensive Feature Planning for Complexity 4-5**

## When to Use

Use this workflow for:
- Complex features (4-5 complexity: 500+ lines, 7+ files, novel patterns)
- High-risk domains (auth, payments, data integrity)
- Architecture decisions needed
- Team alignment required

**Skip for:**
- Simple features (1-2 complexity: <200 lines, using libraries)
- Obvious implementations
- Prototypes/MVPs

---

## Phase 0: Complexity Assessment (CRITICAL FIRST STEP!)

Before any planning, perform quick complexity check:

### Quick Assessment Questions

1. **How many files will this affect?**
   - 1-3 files = Simple (1-2)
   - 4-6 files = Moderate (3)
   - 7-15 files = Complex (4)
   - 15+ files = Very Complex (5)

2. **Using library or novel pattern?**
   - Well-documented library (express-rate-limit, Stripe SDK) = Simple
   - Novel pattern (custom real-time sync) = Complex

3. **High-risk domain?**
   - Auth/payments/data handling = Complex (regardless of size)
   - General features = Use file count

4. **Calculate score (1-5)**

### Decision Tree

**IF Complexity = 1-2 (TRIVIAL/SIMPLE):**

Present honest recommendation:

```markdown
⚠️ Complexity Assessment: 2/5 (SIMPLE)

This appears to be a SIMPLE feature using a well-documented library.

Manual Implementation:
- Time: 30-60 minutes (read library docs, implement, test)
- Tokens: 5k (library docs + implementation)
- Result: Working code

cc10x Systematic Planning:
- Time: 90 minutes (comprehensive planning + implementation)
- Tokens: 80k (plan 30k + build 50k)
- Result: Documented approach but 16x more expensive

Real Test Case: Rate limiting with express-rate-limit (complexity 2)
- cc10x: 100k tokens, reported "tests passing", actually 3/7 failed
- Manual: 30 min, 5k tokens, working code from library docs
- Verdict: cc10x was WORSE for simple feature

Recommendation: Implement manually by reading [library-name] documentation.

OPTIONS:
(a) Manual - I'll provide quick guidance and library recommendations
(b) Systematic - I'll create comprehensive plan anyway (costs 16x more tokens)

Which do you prefer?
```

**Wait for user response:**
- IF (a): Provide quick guidance, link library docs, STOP HERE
- IF (b): Warn "This will use 80k tokens", proceed to Phase 0a

---

**IF Complexity = 3 (MODERATE):**

Present tradeoffs:

```markdown
⚠️ Complexity Assessment: 3/5 (MODERATE)

Moderate complexity - systematic planning helpful but not essential.

cc10x Systematic:
- Comprehensive planning documentation
- Architecture decisions documented
- Risk assessment included
- File manifests prevent scope creep
- Cost: ~100k tokens, 60 minutes

Manual Implementation:
- Faster iteration (40 minutes)
- Less documentation
- Ad-hoc architecture decisions
- Cost: ~15k tokens

Worth systematic planning if:
- Team needs alignment on approach
- Want architecture decisions documented
- Enterprise documentation requirements
- Want to prevent scope creep

Manual is better if:
- Solo developer
- Fast iteration preferred
- Token budget constrained

Proceed with systematic planning? (y/n)
```

**Wait for response.** If yes, proceed to Phase 0a. If no, provide quick guidance.

---

**IF Complexity >= 4 (COMPLEX/VERY COMPLEX):**

Announce confidently:

```markdown
✅ Complexity Assessment: [4 or 5]/5 (COMPLEX)

Complex feature detected. Systematic planning highly valuable.

Why cc10x adds value:
- Novel patterns requiring architecture decisions
- Multiple integration points needing coordination
- High risk requiring mitigation planning
- File manifest prevents scope creep
- Rollback/deployment strategies essential

Token Economics:
- cc10x: ~60k tokens for planning
- Manual: ~20k tokens (3x more)
- BUT prevents architecture mistakes that cost infinitely more to fix

Proceeding with comprehensive 7-phase planning workflow...
```

Proceed directly to Phase 0a (no wait).

---

## Phase 0a: Quick Default Plan with Intelligent Defaults (NEW!)

**Goal:** Present quick plan with assumptions for user validation BEFORE wasting 120k tokens

### Step 1: Generate Minimal Plan (3-5k tokens)

Create 500-line quick plan:

```markdown
# [Feature Name] - Quick Default Plan

## Overview
[2-3 sentence summary]

## Core Requirements (What We Know)
- [Requirement 1 from user message]
- [Requirement 2 from user message]
- [Requirement 3 inferred]

## Intelligent Defaults (FOR YOUR REVIEW)

I've made these assumptions while planning:

1. **OAuth NOT in v1** - Only email/password auth initially
   - Rationale: Simpler to implement, can add OAuth later
   
2. **MongoDB database** - Per user preference
   - Rationale: User rules specify MongoDB
   
3. **httpOnly cookies for tokens** - Not localStorage
   - Rationale: Security best practice (prevents XSS)
   
4. **15-min access, 7-day refresh tokens** - Standard expiry
   - Rationale: Industry standard, balances security and UX
   
5. **Rate limiting: 5 attempts/15min** - Prevents brute force
   - Rationale: OWASP recommendation
   
6. **Email verification deferred to v2** - Not in initial release
   - Rationale: Can launch without, add later
   
7. **No password reset in v1** - Deferred to v2
   - Rationale: Reduces initial scope

## Quick Architecture

[Minimal component diagram showing 3-5 key components]

## Estimated Scope
- Files: [X]
- LOC: [estimate]
- Time: [estimate]

## Key Risks
- [Top 3 risks only]

---

## YOUR DECISION NEEDED

OPTIONS:
(a) PROCEED with these defaults → Continue to full planning (20-30 min, +30k tokens)
(b) CUSTOMIZE assumptions → I'll ask targeted questions, then plan (30-40 min, +40k tokens)
(c) MANUAL planning → I'll provide implementation guidance (5 min, +2k tokens)

Which do you choose?
```

### Step 2: Wait for User Response

**If (a) PROCEED:**
- Continue to Phase 1 with defaults
- Fast track (user validated assumptions)
- Token cost: 3-5k (quick plan) + 30k (full planning) = 33-35k total

**If (b) CUSTOMIZE:**
- Ask targeted clarifying questions (5-10 questions maximum)
- User answers
- Regenerate quick plan with custom choices
- Then proceed to Phase 1
- Token cost: 3-5k (quick plan) + 5k (questions) + 5k (regenerate) + 30k (full) = 43-45k total

**If (c) MANUAL:**
- Provide quick implementation guidance
- Link to relevant libraries/docs
- Stop systematic workflow
- Token cost: 3-5k (quick plan) + 2k (guidance) = 5-7k total
- **Huge savings if user realizes they don't need comprehensive planning**

---

## Phase 1: Requirements Analysis

**Invoke:** `feature-planner` sub-agent

**Agent will:**
1. Analyze feature request thoroughly
2. Research similar patterns in codebase
3. Generate comprehensive PRD with user stories
4. List key assumptions for validation
5. Identify initial risks

**Output:**
- Comprehensive PRD saved to `.claude/plans/{feature-name}-prd.md`
- User stories (As a/I want/So that)
- Functional and non-functional requirements
- Acceptance criteria
- Success metrics
- Out of scope items
- Key assumptions highlighted

**Complexity Scaling:**
- Simple: 200-line PRD, 3-5 user stories
- Moderate: 500-line PRD, 8-12 user stories
- Complex: 1,000+ line PRD, 20+ user stories

---

## Phase 2: Context Discovery

**Invoke:** Uses `codebase-navigation` skill (not a separate agent in v3)

**Process:**
1. Search codebase for similar features
2. Extract project conventions (naming, structure, error handling)
3. Map dependencies and integration points
4. Identify reusable components
5. Recommend file locations

**Output:**
- Similar feature examples
- Project conventions to follow
- Dependencies needed
- Integration points
- Recommended file structure

---

## Phase 3: Architecture & Design

**Invoke:** `architect` sub-agent

**Agent will:**
1. Design system architecture
2. Compare alternatives (at least 2 options)
3. Make technology choices with rationale
4. Create component breakdown
5. Define data models
6. Plan API contracts
7. Document decisions with Technology Decision Framework

**Output:**
- System architecture diagram (Mermaid)
- Technology decisions (with alternatives compared)
- Component breakdown
- Data models
- API contracts
- File organization plan (enforcing <500 lines per file)

**Complexity Scaling:**
- Simple: 150 lines, basic diagram, 2-3 components
- Moderate: 400 lines, detailed diagrams, 5-8 components
- Complex: 1,000+ lines, comprehensive diagrams, 10+ components

---

## Phase 3a: Critical Risk Analysis

**Invoke:** Same `architect` sub-agent

**Loads:** `risk-analysis` skill Stages 1+5 (Data Flow + Security)

**Purpose:** Identify security and data flow risks BEFORE committing to architecture

**Analysis:**
1. **Data Flow Risks:**
   - Input validation gaps
   - Transformation edge cases
   - Null/undefined handling
   - Type coercion issues

2. **Security Risks:**
   - SQL injection potential
   - XSS vulnerabilities
   - Authentication bypass paths
   - Authorization flaws
   - Data exposure risks

**Output:**
- Critical risks that inform architecture
- Security findings that shape design
- Data flow issues requiring handling

**Why this matters:** Prevents choosing architectures with inherent security flaws

---

## Phase 3b: Comprehensive Risk Assessment

**Invoke:** Same `architect` sub-agent

**Loads:** `risk-analysis` skill (comprehensive)

**Process:**
1. Identify all implementation risks
2. Score: Probability (1-3) × Impact (1-3) = 1-9
3. Prioritize: MEDIUM+ (score 4+) need mitigation
4. Define mitigation strategies for each risk

**7 Dimensions Analyzed:**
1. Data Flow & Transformations
2. Dependency & Integration Mapping
3. Timing, Concurrency & State
4. User Experience & Human Factors
5. Security & Validation
6. Performance & Scalability
7. Failure Modes & Recovery

**Output:**
- Risk matrix with all risks scored
- Top risks prioritized (MEDIUM, HIGH, CRITICAL)
- Mitigation strategy for each top risk
- Owner/timeline for mitigations

---

## Phase 3c: Complexity Assessment (Final Validation)

**Invoke:** Same `architect` sub-agent

**Process:**
1. Final complexity assessment with full context
2. Evaluate if cc10x added value so far
3. Honest recommendation

**Scoring Factors:**
- Files affected
- Novelty of patterns
- Integration points
- Risk level
- Domain complexity

**Output:**
```markdown
## Final Complexity Assessment

Score: [1-5]/5

Assessment Factors:
- Files: [X]
- Novel patterns: [High/Medium/Low]
- Integration points: [X]
- Risk level: [1-5]
- Domain: [auth/payment/general]

Recommendation: [Proceed / Consider manual / Manual better]

Token Economics:
- cc10x remaining: ~[X]k tokens
- Manual equivalent: ~[X]k tokens
- Multiplier: [X]x more with cc10x

Worth it because: [specific reasons for THIS feature]
```

If complexity assessment reveals feature is simpler than thought, recommend stopping and going manual.

---

## Phase 4: Testing Strategy

**Process:**
1. Plan unit tests (every function, >80% coverage)
2. Plan integration tests (component interactions)
3. Plan E2E tests (if frontend, critical user flows)
4. Define test data needs
5. Identify mocking requirements

**Output:**
- Test categories (unit/integration/e2e)
- Test count estimates
- Coverage targets
- Mocking strategy

**Complexity Scaling:**
- Simple: 10-20 tests, basic coverage
- Moderate: 30-50 tests, comprehensive units
- Complex: 80-200 tests, unit + integration + e2e

---

## Phase 5: Implementation Roadmap

**Process:**
1. Break feature into incremental steps
2. Each increment: Single responsibility, <200 lines
3. Order by dependencies (foundational first)
4. TDD cycle for each increment
5. Verification checkpoints

**Output:**
- 6-12 implementation increments
- Each with: What to build, Files to create, Tests to write
- Dependencies clearly marked
- Verification checklist

**Complexity Scaling:**
- Simple: 3-5 increments
- Moderate: 6-10 increments
- Complex: 10-15 increments

---

## Phase 5b: File Change Manifest (NEW!)

**Purpose:** Concrete implementation targets for scope tracking

**Process:**
1. List every file to CREATE
2. List every file to MODIFY
3. List every file to DELETE (if refactoring)
4. Estimate LOC for each
5. Map integration points
6. Create verification checklist

**Output:**
```markdown
## File Change Manifest

### CREATE (New Files)
- `src/auth/service.ts` (~350 lines) - Authentication service
  - Integrates with: database, crypto module
  - Dependencies: bcrypt, jsonwebtoken
  
- `src/auth/middleware.ts` (~180 lines) - Auth middleware
  - Integrates with: auth service, routes
  
- `src/auth/types.ts` (~120 lines) - TypeScript types
  - Used by: service, middleware, controllers

[...continue for all new files...]

### MODIFY (Existing Files)
- `src/app.ts` (+25 lines) - Register auth routes
  - Line 45: Add import
  - Line 120: Mount auth router
  
- `src/config/index.ts` (+15 lines) - Add JWT config
  - Section: JWT settings (secret, expiry)

[...continue for all modified files...]

### DELETE (Removed Files)
- `src/legacy/old-auth.js` (deprecated, replaced by new auth service)

### Totals
- CREATE: [X] files, ~[Y] LOC
- MODIFY: [X] files, ~[Y] LOC
- DELETE: [X] files
- **Total LOC: ~[estimate]**

### Integration Points
1. Auth service ↔ Database (User model)
2. Auth middleware ↔ Express routes
3. Auth service ↔ Crypto module (password hashing)
4. Frontend ↔ Auth API (login/register/refresh)

### Verification Checklist
- [ ] All planned files created
- [ ] No unplanned files (scope creep check)
- [ ] LOC within ±30% of estimates
- [ ] Integration points connected
- [ ] All file sizes <500 lines
```

**This prevents scope creep and provides concrete verification targets.**

---

## Phase 6: Rollback Strategy (NEW!)

**Purpose:** Ensure <5 minute recovery if feature breaks

**Invoke:** Uses `deployment-patterns` skill Stage 1 (Rollback)

**Process:**
1. Design 3-level rollback strategy
2. Document procedures for each level
3. Estimate recovery time
4. Identify rollback triggers

**Output:**
```markdown
## Rollback Strategy

### Level 1: Feature Flag (Instant - <1 min)

**Trigger:** Feature broken but not critical

**Procedure:**
1. Set `FEATURE_AUTH_ENABLED=false` in environment
2. Restart application
3. Feature disabled, app continues working

**Recovery Time:** <1 minute

**When to use:** Non-critical issues, want to investigate before reverting code

---

### Level 2: Configuration Rollback (<5 min)

**Trigger:** Configuration causing issues, code is fine

**Procedure:**
1. Revert `config/auth.json` to previous version
2. Run: `git checkout HEAD~1 -- config/auth.json`
3. Restart application

**Recovery Time:** <5 minutes

**When to use:** Configuration errors, wrong token expiry, etc.

---

### Level 3: Code Rollback (<15 min)

**Trigger:** Code has critical bugs, must revert

**Procedure:**
1. Identify commit to revert: `git log --oneline -10`
2. Create revert commit: `git revert [commit-hash]`
3. Push: `git push origin main`
4. Deploy: `./deploy.sh` (automated pipeline)

**Recovery Time:** <15 minutes

**When to use:** Critical bugs, security vulnerabilities, data corruption

**Files to revert:**
- All files from File Change Manifest (Phase 5b)
- Database migrations (if any)
- Configuration changes

---

### Rollback Testing

Before deployment, test rollback:
- [ ] Feature flag toggle works
- [ ] Configuration rollback tested in staging
- [ ] Code revert procedure documented
- [ ] Team knows rollback triggers
- [ ] Monitoring alerts configured
```

---

## Phase 7: Deployment Strategy (NEW!)

**Purpose:** Safe, staged rollout

**Invoke:** Uses `deployment-patterns` skill Stage 2 (Deployment)

**Process:**
1. Design 5-stage rollout
2. Define monitoring for each stage
3. Plan rollback triggers
4. Risk-based sequencing

**Output:**
```markdown
## Deployment Strategy

### Stage 1: Infrastructure (Pre-deployment)

**What:** Database migrations, environment variables, dependencies

**Actions:**
1. Run migrations: `npm run migrate`
2. Set env vars: `JWT_SECRET`, `JWT_EXPIRY`
3. Install deps: `npm install`

**Verification:**
- [ ] Migrations succeeded
- [ ] Env vars set correctly
- [ ] Dependencies installed

**Rollback:** Database rollback script ready

---

### Stage 2: Canary (1-5% traffic)

**What:** Deploy to small user subset first

**Duration:** 2-4 hours

**Monitoring:**
- Error rate: <0.1%
- Response time: <200ms p95
- Auth success rate: >98%

**Success Criteria:**
- Zero CRITICAL errors
- Performance within targets
- No user complaints

**Rollback Trigger:** >0.5% error rate or any CRITICAL error

---

### Stage 3: Partial (20% traffic)

**What:** Expand to 20% of users

**Duration:** 12-24 hours

**Monitoring:** Same as Stage 2

**Success Criteria:**
- Consistent with canary metrics
- No degradation at scale

---

### Stage 4: Majority (80% traffic)

**What:** Expand to 80% of users

**Duration:** 24-48 hours

**Monitoring:** Continue

---

### Stage 5: Full (100% traffic)

**What:** All users on new feature

**Post-deployment:**
- Remove feature flag (or keep for future use)
- Monitor for 1 week
- Document learnings
- Update team runbook
```

---

## Final Planning Document

After all 7 phases, generate comprehensive plan:

**Save to:** `.claude/plans/FEATURE_[NAME].md`

**Structure:**
```markdown
# [Feature Name] - Comprehensive Plan

## Phase 1: Requirements
[Full PRD from feature-planner]

## Phase 2: Context
[Codebase patterns, conventions, similar features]

## Phase 3: Architecture
[Design decisions, technology choices, components]

## Phase 3a: Critical Risks
[Data flow and security risks that informed architecture]

## Phase 3b: Risk Assessment
[Comprehensive 7-dimension risk matrix]

## Phase 3c: Complexity
[Final assessment and token economics]

## Phase 4: Testing Strategy
[Test plans, coverage targets, mocking strategy]

## Phase 5: Implementation Roadmap
[6-12 incremental steps with TDD cycles]

## Phase 5b: File Change Manifest
[CREATE/MODIFY/DELETE breakdown with LOC estimates]

## Phase 6: Rollback Strategy
[3-level rollback procedures with <5 min recovery]

## Phase 7: Deployment Strategy
[5-stage rollout with monitoring and rollback triggers]

---

## Summary

**Complexity:** [1-5]/5
**Estimated Scope:** [X] files, ~[Y] LOC
**Estimated Time:** [Z] hours
**Top Risks:** [Top 3]
**Recommended Next Step:** Execute /feature-build or implement manually with this plan
```

---

## Token Economics

**Total Planning Cost:**
- Phase 0: Complexity check (1k)
- Phase 0a: Quick default plan (3-5k)
- Phases 1-7: Full planning (25-40k if complexity 4-5)
- **Total: 30-45k tokens**

**Manual Planning Equivalent:**
- Mental planning: 0 tokens
- Basic notes: 2-5k tokens
- **Comparison: 6-20x MORE with cc10x**

**Worth it when:**
- Complexity 4-5 (prevents architecture mistakes)
- Team alignment needed (documentation valuable)
- High-risk domains (security planning essential)

**NOT worth it when:**
- Complexity 1-2 (just read library docs)
- Solo dev, familiar pattern
- Token budget limited

---

## Success Indicators

Planning workflow successful if:
- [ ] Complexity appropriately assessed
- [ ] User validated assumptions (or used intelligent defaults)
- [ ] Architecture decisions compared alternatives
- [ ] Top risks identified and mitigated
- [ ] File manifest provides concrete targets
- [ ] Rollback strategy enables <5 min recovery
- [ ] Deployment strategy staged and monitored
- [ ] Plan saved to `.claude/plans/` for implementation

---

## Remember

This workflow provides systematic thinking for complex features. The value is in:
- **Preventing architecture mistakes** (one mistake >> 45k tokens cost)
- **Risk identification** (security analysis prevents breaches)
- **Team alignment** (documentation enables collaboration)
- **Scope control** (file manifest prevents creep)

**Use for complexity 4-5. Skip for 1-2. Decide for 3.**

