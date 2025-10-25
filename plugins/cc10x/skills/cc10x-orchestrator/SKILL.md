---
name: cc10x-orchestrator
description: Master orchestration skill for systematic development workflows. Detects task type from user messages (review, plan, build, debug, validate), assesses complexity (1-5 scoring), chooses appropriate workflow, invokes specialized sub-agents, loads domain skills progressively. Use when you need systematic code review (5-star with parallel AI agents for security, quality, performance, UX, accessibility), comprehensive feature planning (with complexity assessment, architecture decisions, file manifests, rollback strategies), TDD-enforced implementation (with 'What Could Go Wrong?' risk analysis before each increment), LOG FIRST debugging (systematic investigation over assumption-driven guessing), or cross-artifact validation (ensuring plans match code). Particularly valuable for complex features (4-5 complexity requiring 500+ lines, 7+ files, novel patterns, architecture decisions, risk mitigation, production-ready deployment planning). For simple features (1-2 complexity), recommends manual implementation with token economics comparison. Integrates 7-dimension 'What Could Go Wrong?' methodology (data flow, dependencies, timing/concurrency, UX/accessibility, security, performance, failure modes) at critical phases. Honest positioning costs 3-20x MORE tokens than manual (systematic analysis has overhead), use for complexity 4-5 where preventing architecture mistakes justifies cost. Review workflow always worth it (prevents security breaches).
license: MIT
---

# cc10x Master Orchestrator

I am the ONE skill that orchestrates all cc10x systematic development workflows.

## Quick Reference

### When You Should Use Me

Use me when you want:
- ⭐ **Systematic code review** (5-star, always valuable - found 38 issues in testing including 5 CRITICAL)
- **Comprehensive feature planning** (complexity 4-5: architecture decisions, file manifests, rollback strategies)
- **TDD-enforced implementation** (with "What Could Go Wrong?" risk analysis before each increment)
- **LOG FIRST debugging** (complex bugs where root cause unclear)
- **Cross-artifact validation** (ensure plans match code, tests match requirements)

### When You Should Skip Me

Skip me for:
- **Simple features** (complexity 1-2: <200 lines, using well-documented libraries) - Manual is 16-20x cheaper!
- **Obvious fixes** (<5 lines, root cause clear) - Just fix it!
- **Emergencies** (production down) - Fix now, systematic documentation later
- **Prototypes/MVPs** - Iterate fast first, systematize later

### Reality Check

**I cost 3-20x MORE tokens than manual implementation.**

**Why?** Systematic multi-phase analysis, risk assessments, comprehensive documentation.

**Worth it when:** Complexity 4-5 where one prevented architecture mistake pays for all the planning.

**Exception:** REVIEW workflow always worth it (prevents security breaches = infinite ROI).

---

## How I Work

### Step 1: Analyze Your Message

I detect three things:

**1. Task Type:**
- **REVIEW** - "review", "audit", "check", "analyze", "find issues", "security scan"
- **PLAN** - "plan", "design", "architecture", "create plan", "PRD", "feature spec"
- **BUILD** - "implement", "build", "create feature", "add", "develop", "code this"
- **DEBUG** - "debug", "fix bug", "not working", "error", "investigate", "troubleshoot"
- **VALIDATE** - "validate", "verify", "check consistency", "does code match plan"

**2. Complexity (Quick Assessment):**
- Files likely affected? (1-3 = simple, 4-6 = moderate, 7+ = complex)
- Novel pattern or using library? (novel = complex, library = simple)
- High-risk domain? (auth/payment/data = complex regardless of size)
- Score: 1 (TRIVIAL) → 5 (VERY COMPLEX)

**3. Domain:**
- Frontend (React, UI, components)
- Backend (API, database, services)
- Full-stack (both)
- Infrastructure (deployment, DevOps)

### Step 2: Make Decision

Based on detection:

```
IF task = REVIEW:
  → Always proceed (5⭐ killer feature, always worth it)
  
IF task = PLAN:
  → Check complexity first
  → IF complexity <= 2: Recommend manual, ask user
  → IF complexity >= 4: Proceed with confidence
  → IF complexity = 3: Show tradeoffs, ask user
  
IF task = BUILD:
  → Strong complexity check (don't waste tokens!)
  → IF complexity <= 2: STRONGLY recommend manual (show rate limiting test failure)
  → IF complexity >= 4: Proceed
  → IF user explicitly says "use cc10x": Proceed anyway but warn about cost
  
IF task = DEBUG:
  → Assess complexity
  → Simple bug? Recommend just fixing it
  → Complex bug? LOG FIRST is valuable
  
IF task = VALIDATE:
  → Check if plan exists (.claude/plans/FEATURE_*.md)
  → No plan? Can't validate, recommend create plan first
  → Plan exists? Proceed with validation
```

### Step 3: Execute Chosen Workflow

Load appropriate workflow and orchestrate sub-agents + domain skills.

---

## WORKFLOW 1: REVIEW ⭐⭐⭐⭐⭐

**The Killer Feature - Always Worth It!**

### When This Triggers

Messages like:
- "Review this code for security issues"
- "Audit src/auth.js for vulnerabilities"
- "Check for performance problems in api.js"
- "Find code quality issues"
- "Analyze this for accessibility"
- "What's wrong with this code?"

### Announcement

"🔍 **Using cc10x systematic review workflow** (⭐⭐⭐⭐⭐ verified working AI agents)

Real-world testing found 38 issues including:
- 5 CRITICAL (SQL injection, hardcoded secrets, auth bypass)
- 12 HIGH (N+1 queries, memory leaks, race conditions)
- 21 MODERATE/LOW (code smells, UX improvements)

Launching 5 specialized review agents in parallel..."

### Execution

**Phase 1: Scope Analysis**
1. Parse target from user message
   - Specific file: `src/auth.js`
   - Directory: `src/features/auth/`
   - Pattern: `src/**/*.js`
2. Identify file types (JS, TS, Python, etc.)

**Phase 2: Parallel Multi-Dimensional Review**

**Invoke 5 agents SIMULTANEOUSLY** (ONLY workflow that parallelizes!):

**1. security-reviewer**
- Loads skills: `risk-analysis` Stages 1+2+5 + `security-patterns`
- Analyzes: SQL injection, XSS, auth bypasses, data exposure
- Uses: OWASP Top 10 checklist
- Returns: Security findings with severity

**2. quality-reviewer**
- Loads skills: `risk-analysis` ALL 7 stages + `code-review-patterns`
- Analyzes: Code smells, duplication, complexity, maintainability
- Uses: Martin Fowler refactoring catalog
- Returns: Quality findings with refactoring suggestions

**3. performance-analyzer**
- Loads skills: `risk-analysis` Stage 6 + `performance-patterns`
- Analyzes: O(n²) complexity, memory leaks, N+1 queries, caching opportunities
- Uses: Performance optimization techniques
- Returns: Performance findings with optimization suggestions

**4. ux-reviewer**
- Loads skills: `risk-analysis` Stage 4 + `ux-patterns`
- Analyzes: Error messages, loading states, user feedback, interaction patterns
- Uses: UX best practices
- Returns: UX findings with improvement suggestions

**5. accessibility-reviewer**
- Loads skills: `accessibility-patterns`
- Analyzes: WCAG violations, keyboard navigation, screen reader support
- Uses: WCAG 2.1 AA checklist
- Returns: Accessibility findings with remediation steps

**Phase 3: Synthesis & Report Generation**

1. Consolidate findings from all 5 agents
2. Remove duplicates (same issue found by multiple agents)
3. Prioritize by severity: CRITICAL → HIGH → MODERATE → LOW
4. Generate comprehensive report with:
   - File-level findings
   - Specific line numbers
   - Severity classification
   - Fix recommendations with code examples
   - Time estimates for fixes

### Output Format

```markdown
## Multi-Dimensional Code Review: [Target]

### Summary
- Total Issues: [X]
- CRITICAL: [X] (must fix before merge)
- HIGH: [X] (should fix)
- MODERATE: [X] (good to fix)
- LOW: [X] (nice to fix)

### CRITICAL Issues (Must Fix)

**[SEC-001] SQL Injection Vulnerability**
- File: src/auth/login.controller.js
- Line: 45
- Issue: User input directly concatenated into SQL query
- Risk: Database compromise, data breach
- Fix:
```javascript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ FIXED - Use parameterized queries
const query = 'SELECT * FROM users WHERE email = ?';
const result = await db.query(query, [email]);
```
- Estimated fix time: 10 minutes

[Continue for all issues...]
```

### Real Test Results

**Test Case:** Authentication system review
- Found: 38 issues total
- 5 CRITICAL (SQL injection, secrets in logs, auth bypass, XSS, missing transaction)
- 12 HIGH (N+1 queries, memory leaks, race conditions)
- 21 MODERATE/LOW (code smells, UX improvements)
- Time: 3 minutes
- Tokens: 35k

**Verdict:** ⭐⭐⭐⭐⭐ Worth every token! One prevented security breach >> 35k tokens.

### Token Economics

**Costs:** 20k-50k tokens depending on codebase size

**Value:** 
- Replaces: 6-11 hours of manual expert review (security + quality + performance + UX + a11y)
- Prevents: Security breaches, performance bugs, accessibility lawsuits
- Finds: Issues human reviewers miss (SQL injection in code review)

**Use before EVERY PR!**

---

## WORKFLOW 2: PLANNING

### When This Triggers

Messages like:
- "Plan authentication feature with JWT"
- "Design real-time notifications architecture"
- "Create PRD for multi-tenancy"
- "I need to plan a payment processing feature"
- "Help me design the architecture for X"

### Phase 0: Complexity Check (CRITICAL FIRST STEP!)

Before any planning, assess complexity:

**Quick Assessment:**
1. How many files will this affect? (user description or ask)
2. Using well-documented library or novel pattern? (ask if unclear)
3. High-risk domain? (auth, payments, data handling)
4. Estimate: 1-5 complexity score

**Decision Tree:**

**IF Complexity = 1-2 (TRIVIAL/SIMPLE):**

Present recommendation:

```
⚠️ **Complexity Assessment: 2/5 (SIMPLE)**

This appears to be a SIMPLE feature using a well-documented library.

**Manual Implementation:**
- Time: 30-60 minutes (read library docs, implement, test)
- Tokens: 5k (library docs + implementation)
- Result: Working code

**cc10x Systematic Planning:**
- Time: 90 minutes (comprehensive planning + implementation)
- Tokens: 80k (plan 20k + build 60k)
- Result: Documented approach but 16x more expensive

**Real Test Case:** Rate limiting with express-rate-limit (complexity 2)
- cc10x: 100k tokens, reported "tests passing", actually 3/7 failed
- Manual: 30 min, 5k tokens, working code from library docs
- **Verdict: cc10x was WORSE for simple feature**

**Recommendation:** Implement manually by reading [library] documentation.

**Options:**
(a) **Manual** - I'll provide quick guidance and library recommendations
(b) **Systematic** - I'll create comprehensive plan anyway (your call)

**Which do you prefer?**
```

Wait for user response:
- IF (a): Provide quick implementation guidance, link to library docs, stop here
- IF (b): Warn about cost, proceed to Phase 1

---

**IF Complexity = 3 (MODERATE):**

Present tradeoffs:

```
⚠️ **Complexity Assessment: 3/5 (MODERATE)**

Moderate complexity - systematic planning helpful but not essential.

**Tradeoffs:**

**cc10x Systematic:**
- Comprehensive planning documentation
- Architecture decisions documented
- Risk assessment included
- File manifests prevent scope creep
- Cost: ~100k tokens, 60 minutes

**Manual Implementation:**
- Faster iteration (40 minutes)
- Less documentation
- Ad-hoc architecture decisions
- Cost: ~15k tokens

**Worth systematic planning if:**
- Team needs alignment on approach
- Want architecture decisions documented
- Enterprise documentation requirements
- Want to prevent scope creep

**Manual is better if:**
- Solo developer
- Fast iteration preferred
- Token budget constrained

**Proceed with systematic planning?** (y/n)
```

Wait for response. If yes, proceed to Phase 1. If no, provide quick guidance.

---

**IF Complexity >= 4 (COMPLEX/VERY COMPLEX):**

Announce confidently:

```
✅ **Complexity Assessment: 4/5 (COMPLEX)**

Complex feature detected. Systematic planning highly valuable.

**Why cc10x adds value:**
- Novel patterns requiring architecture decisions
- Multiple integration points needing coordination
- High risk requiring mitigation planning
- File manifest prevents scope creep
- Rollback/deployment strategies essential

**Proceeding with comprehensive 7-phase planning workflow...**
```

Proceed directly to Phase 1.

---

### Phase 1: Requirements Analysis

**Invoke:** `requirements-analyst` sub-agent

**Agent will:**
1. Load `feature-planning` skill Stage 1 (Requirements) - 500 tokens
2. Parse user's feature description
3. Extract user stories (As a/I want/So that format)
4. Create acceptance criteria (Given/When/Then)
5. List assumptions to validate
6. Generate clarifying questions if requirements unclear

**Output:**
- Requirements Summary
- User Stories with Acceptance Criteria
- Assumptions to Validate
- Clarifying Questions (if any)

**Tokens:** ~500

---

### Phase 2: Context Discovery

**Invoke:** `context-analyzer` sub-agent

**Agent will:**
1. Load `codebase-navigation` skill Stages 1-2 (Pattern Discovery + Convention Extraction) - 1,100 tokens
2. Search codebase for similar features
3. Extract project conventions (naming, structure, error handling, testing)
4. Map dependencies and integration points
5. Recommend file locations

**Output:**
- Similar Feature Examples
- Project Conventions
- Dependencies Needed
- Integration Points
- Recommended File Structure

**Tokens:** ~1,100

---

### Phase 3: Architecture & Design

**Invoke:** `architect` sub-agent

**Agent will:**
1. Load `feature-planning` skill Stage 2 (Architecture) - 800 tokens
2. Compare alternative architectures (at least 2 options)
3. Make and justify technology choices
4. Create Architecture Decision Records (ADRs)
5. Design component breakdown, APIs, data models

**Output:**
- Architecture Decisions (with alternatives compared)
- Component Breakdown
- API Specification
- Data Models
- Integration Strategy

**Tokens:** ~800

---

### Phase 3a: Critical Risk Analysis (NEW!)

**Invoke:** Same `architect` sub-agent (continues from Phase 3)

**Agent will:**
1. Load `risk-analysis` skill Stages 1+5 (Data Flow + Security) - 1,400 tokens
2. Analyze data flow risks (input validation, transformations, edge cases)
3. Identify security vulnerabilities early (injection, auth, data exposure)
4. Flag critical issues that affect architecture choices

**Why before committing to architecture:**
- Identifies security flaws in proposed architecture
- Finds data flow issues before they're baked in
- Informs architecture decisions (example: JWT vs sessions depends on security analysis)

**Output:**
- Data Flow Risks (null handling, validation gaps, transformation issues)
- Security Risks (SQL injection, XSS, auth bypass potential)
- Critical findings that inform architecture

**Tokens:** ~1,400

---

### Phase 3b: Risk Assessment

**Invoke:** Same `architect` sub-agent

**Agent will:**
1. Load `feature-planning` skill Stage 3 (Risk) - 400 tokens
2. Identify implementation risks
3. Score risks (Probability × Impact: 1-9 scale)
4. Prioritize (MEDIUM+ need mitigation)
5. Define mitigation strategies

**Output:**
- Risk Matrix (all risks with Prob × Impact scores)
- Top Risks (MEDIUM+ prioritized)
- Mitigation Strategies

**Tokens:** ~400

---

### Phase 3c: Complexity Assessment (Final Check)

**Invoke:** Same `architect` sub-agent

**Agent will:**
1. Load `feature-planning` skill Stage 4 (Complexity) - 600 tokens
2. Final complexity assessment with all context
3. Evaluate if cc10x added value
4. Provide honest recommendation

**Output:**
- Final Complexity Score (1-5 with detailed rationale)
- Assessment Factors (files, novelty, integration points, risk, domain)
- Token Economics (cc10x vs manual comparison)
- Recommendation (proceed or manual is better)

**Tokens:** ~600

**Example output (complexity 2):**
```
## Final Complexity Assessment

**Score: 2/5 (SIMPLE)**

After analyzing the requirements and architecture, this feature is SIMPLER than initially thought.

**Assessment:**
- Files: 3 (middleware, route, test)
- Library: express-rate-limit (well-documented, mature)
- Integration: Minimal (just middleware registration)
- Risk: LOW (rate limiting is non-critical)

⚠️ **Revised Recommendation: Manual Implementation Better**

Library documentation path:
- Read express-rate-limit docs (5 min)
- Install and configure (10 min)
- Add to routes (10 min)
- Test (5 min)
- **Total: 30 min, ~5k tokens**

vs

cc10x continuing:
- Remaining phases 4-7 (30 min)
- Implementation with full TDD (60 min)
- **Total: 120 min, ~80k additional tokens**

**Stop here and implement manually?** You've already learned the key architecture decisions from Phases 1-3. Recommend stopping now and implementing manually with this guidance.

**Your call:** Stop (save 80k tokens) or Continue (systematic documentation)
```

---

### Phases 4-7: Continuation (If Complexity >= 4 or User Chooses)

**Phase 4: Testing Strategy**
- Invoke: `architect`
- Loads: `test-driven-development` Stage 1
- Output: Unit/Integration/E2E test plans

**Phase 5: Implementation Roadmap**
- Invoke: `architect`
- Output: Incremental implementation plan (6-12 increments, each <200 lines)

**Phase 5b: File Change Manifest** (NEW from Cursor!)
- Invoke: `architect`
- Loads: `feature-planning` Stage 5 (Manifest)
- Output: CREATE/MODIFY/DELETE breakdown with LOC estimates

**Phase 6: Rollback Strategy** (NEW from Cursor!)
- Invoke: `devops-planner`
- Loads: `risk-analysis` Stage 7 + `deployment-patterns` Stage 1
- Output: 3-level rollback procedures (< 5 min recovery)

**Phase 7: Deployment Strategy** (NEW from Cursor!)
- Invoke: `devops-planner`
- Loads: `deployment-patterns` Stage 2
- Output: 5-stage deployment plan with risk categorization

**Tokens (Phases 4-7):** ~2,400

---

### Final Output

Comprehensive plan saved to `.claude/plans/FEATURE_[NAME].md` with 15 sections:
1. Requirements Summary
2. User Stories
3. Context Analysis
4. Architecture Decisions
5. Critical Risk Analysis (NEW!)
6. Component Breakdown
7. API Specification
8. Data Models
9. Risk Assessment
10. Complexity Assessment (NEW!)
11. Testing Strategy
12. Implementation Roadmap
13. File Change Manifest (NEW!)
14. Rollback Strategy (NEW!)
15. Deployment Strategy (NEW!)

**Total Tokens:**
- Simple (stops at Phase 3c): 3,200 tokens
- Complex (all 7 phases): 5,200 tokens

**Real Progressive Loading:** vs v1.x 15k embedded tokens = 65-79% savings!

**Ready for:** BUILDING workflow or manual implementation

---

## WORKFLOW 3: BUILDING

### When This Triggers

Messages like:
- "Implement authentication feature from the plan"
- "Build the payment processing system"
- "Create the notification feature"
- "Develop user dashboard"

### Phase 0: Complexity & Plan Check

**Complexity Check (STRONG!):**

```
IF complexity <= 2:
  → "⚠️ **STOP: This is a SIMPLE feature (complexity 2/5)**
  
     Building with cc10x will cost 80k tokens vs 5k manual.
     
     Real test: Rate limiting (complexity 2)
     - cc10x: 100k tokens, reported 'tests passing', actually 3/7 FAILED
     - Manual: 30 min, 5k tokens, working code
     
     **Strongly recommend manual implementation.**
     
     Proceed anyway? (not recommended but your choice)"
     
  → Wait for explicit user confirmation
  → If yes: Warn about cost, proceed
  → If no: Provide implementation guidance, stop

IF complexity >= 4:
  → "✅ Complex feature (4/5). Systematic TDD valuable. Proceeding..."
  → Continue to Phase 1
```

**Plan Check:**
```
Check for existing plan:
  IF .claude/plans/FEATURE_*.md exists:
    → "Found plan: [filename]. Using as blueprint..."
    → Load plan, extract file manifest, architecture
  IF no plan:
    → "No feature plan found. Recommend running PLANNING workflow first.
       
       Options:
       (a) Create plan first (recommended for complex features)
       (b) Build without plan (faster but ad-hoc)
       
       Which?"
    → Wait for response
```

### Phase 1: Context Analysis

**Invoke:** `context-analyzer` sub-agent

**Agent will:**
- Load `codebase-navigation` skill
- Find similar features for pattern reference
- Extract project conventions

**Output:** Context report

**Tokens:** ~1,100

---

### Phase 2: Implementation Planning

**Invoke:** `architect` sub-agent

**Agent will:**
- Load `feature-building` skill Stage 1
- Break feature into increments (<200 lines each)
- Define dependencies between increments
- Create sequence (what must complete first)

**Output:** Incremental implementation plan (6-12 increments)

**Tokens:** ~600

---

### Phase 3: TDD Implementation (Sequential, Never Parallel!)

**FOR EACH INCREMENT (one at a time):**

**Invoke:** `tdd-enforcer` sub-agent

**Agent will execute 9 steps:**

**Step 0: Risk Analysis (NEW! - What Could Go Wrong?)**
1. Load `risk-analysis` skill Stages 1+3+7
   - Stage 1: Data Flow (input edge cases)
   - Stage 3: Timing (race conditions, state issues)
   - Stage 7: Failure Modes (error handling needs)
2. Identify edge cases for THIS increment
3. Output: Edge cases list (becomes test cases in Step 2)

**Example:**
```
Increment 1: User registration endpoint

Risk Analysis Findings:
- [Stage 1] Email could be null, malformed, SQL injection attempt
- [Stage 3] Two users could register same email simultaneously
- [Stage 7] Email service might be down, database constraint could fail

Edge Cases to Test:
- null email (400 error)
- malformed email (400 error)
- SQL injection attempt (sanitized)
- Duplicate email (409 conflict)
- Email service down (queue for retry)
- Database error (transaction rollback)
```

**Steps 1-8: RED-GREEN-REFACTOR Cycle**

1. **RED:** Write failing test (covers edge cases from Step 0)
2. **Verify:** Test fails for RIGHT reason
3. **GREEN:** Write minimal code to pass
4. **Verify:** Test passes
5. **Verify:** ALL tests pass (no regressions)
6. **REFACTOR:** Clean up code
7. **Verify:** Tests still pass after refactor
8. **File Manifest Check:** Verify against plan (90%+ match)

**Step 9: MANDATORY Test Verification**

**CRITICAL:** Never trust "tests passing" reports!

1. Load `test-driven-development` skill Stage 3 (Verification)
2. Run ACTUAL test command: `npm test`
3. Capture REAL output (don't summarize!)
4. Verify exit code: `echo $?` (must be 0)
5. Visual confirmation: SEE ✓ symbols with YOUR EYES

**Required:**
- [ ] All tests run
- [ ] All tests pass
- [ ] Exit code = 0
- [ ] Actual output captured

**If tests fail:** STOP. Fix immediately. Don't proceed to next increment.

**Correct reporting:**
```markdown
## Increment 1: Test Verification

**Command:** `npm test`

**Output:**
```
PASS tests/auth.test.js
  ✓ handles null email (32ms)
  ✓ handles malformed email (28ms)
  ✓ prevents SQL injection (45ms)
  ✓ handles duplicate email (52ms)

Tests: 4 passed, 4 total
```

**Exit code:** 0 ✅

**Verified:** All 4 tests passing independently confirmed.

**Proceeding to Increment 2.**
```

**Repeat for ALL increments sequentially.**

---

### Phase 4: Multi-Dimensional Verification

**Invoke 5 review agents IN PARALLEL:**
- Same as REVIEW workflow (Phase 2)
- Comprehensive analysis of implementation

**Output:** Review findings (fix CRITICAL before Phase 5)

---

### Phase 5: Finalization

**Tasks:**
1. Remove ALL debug code (console.log, debugger, TODO)
2. Update documentation (README if APIs changed)
3. Verify File Manifest 90%+ match
4. Create semantic commit message
5. Stage changes (ready for commit)

**Output:** Production-ready code, ready to commit

---

### Token Economics

**Total for building:**
- Small (complexity 3): 40k-60k tokens
- Medium (complexity 4): 60-100k tokens
- Large (complexity 5): 100-150k tokens

**vs Manual:**
- Small: 5-15k tokens
- Medium: 15-30k tokens
- Large: 30-50k tokens

**Reality:** 8-16x MORE tokens

**Worth it when:**
- Complexity 4-5 (prevents architecture mistakes, security issues)
- High-risk features (auth, payments - one bug = infinite cost)

**NOT worth it when:**
- Complexity 1-2 (manual faster, cheaper, better results)

---

## WORKFLOW 4: DEBUGGING

### When This Triggers

Messages like:
- "Debug why rate limiting isn't working"
- "Fix bug: users can submit empty emails"
- "Investigate login timeout issue"
- "This code isn't working as expected"

### Announcement

"🔍 **Using LOG FIRST debugging pattern**

Prevents assumption-driven debugging that wastes hours.

**Philosophy:** Never guess what the data looks like - ALWAYS log and SEE it first, then fix based on what you observe.

**Real test:** Saved 2 hours by logging first instead of trying 5 random fixes."

### Execution

**Phase 1: Context Gathering**

**Invoke:** `context-analyzer` sub-agent

1. Understand the bug (symptoms, reproduction steps)
2. Locate affected code
3. Map related systems

**Output:** Bug context

**Tokens:** ~600

---

**Phase 2: LOG FIRST Investigation**

**Invoke:** `tdd-enforcer` sub-agent

**Agent will:**
1. Load `systematic-debugging` skill Stage 1 (LOG FIRST pattern) - 500 tokens
2. Load `risk-analysis` skill Stage 7 (Failure Modes) - 700 tokens
3. Add comprehensive logging BEFORE attempting fixes
4. Run code to see ACTUAL data (not assumptions!)
5. Identify root cause from logs

**The Process:**

**Step 1: Add Strategic Logging**
```javascript
// Before fixing: Add logging to see ACTUAL data
router.post('/login', async (req, res) => {
  console.log('=== LOGIN HANDLER ===');
  console.log('Full body:', JSON.stringify(req.body, null, 2));
  console.log('Email:', req.body.email);
  console.log('Password provided:', !!req.body.password);
  
  // ... existing code with more logging
});

// In middleware
app.use((req, res, next) => {
  console.log('RATE LIMIT CHECK:', req.rateLimit);
  next();
});
```

**Step 2: Reproduce Bug**
```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test"}'
```

**Step 3: Analyze Logs**
```
=== LOGIN HANDLER ===
Full body: {}
Email: undefined
Password provided: false

RATE LIMIT CHECK: undefined
```

**Step 4: ROOT CAUSE Identified**
```
Body parser not configured! req.body is empty.
Rate limit middleware not registered!

NOT a problem with rate limiting logic.
NOT a problem with login validation.

FIX: Add app.use(express.json()) and register middleware.
```

**Critical Rule:** Never guess - always log the COMPLETE structure first!

---

**Phase 3: Minimal Fix with Test**

**Invoke:** `tdd-enforcer` sub-agent

1. Write test that reproduces bug
2. Verify test FAILS (proves it catches the bug)
3. Apply minimal fix
4. Verify test PASSES
5. Verify ALL tests pass

**Output:** Bug fix with test

---

**Phase 4: Cleanup**

Remove ALL debug logging added in Phase 2:
- console.log statements
- debugger statements
- Test-only code

Verify tests still pass after cleanup.

**Output:** Clean code, bug fixed, test added

---

### Real Test Results

**Bug:** Rate limiting not blocking requests

**Traditional approach (WRONG):**
- Guess 1: Middleware not applied? (check - it IS applied)
- Guess 2: express-rate-limit broken? (reinstall - still broken)
- Guess 3: Config wrong? (try 5 configs - still broken)
- **Time wasted:** 2+ hours

**LOG FIRST approach (RIGHT):**
- Add logging (5 min)
- See: "RATE LIMIT EXCEEDED" logged, handler STILL runs
- ROOT CAUSE: Custom handler doesn't return immediately
- Fix: Remove custom handler, use library default
- **Time:** 15 minutes total (saved 105 minutes!)

**Verdict:** LOG FIRST pattern brilliant! Saves hours of guessing.

**Tokens:** 15k-30k (worth it for complex bugs, overkill for obvious ones)

---

## WORKFLOW 5: VALIDATION

### When This Triggers

Messages like:
- "Validate this implementation against the plan"
- "Check if code matches requirements"
- "Verify consistency between plan and code"
- "Does this match what we designed?"

### Phase 0: Plan Existence Check

```
Search for plan in .claude/plans/FEATURE_*.md:
  IF no plan found:
    → "No feature plan found in .claude/plans/
    
       Can't validate without a plan to compare against.
       
       Options:
       (a) Create plan first (recommended)
       (b) Skip validation
       
       Which?"
  IF plan found:
    → "Found plan: FEATURE_[NAME].md. Validating against it..."
    → Load plan, proceed to Phase 1
```

### Execution

**5-Dimension Validation:**

**Dimension 1: Plan-Code Consistency**
- Invoke: `architect`
- Compare: Planned architecture vs actual implementation
- Check: All user stories implemented? APIs match spec?

**Dimension 2: Code-Test Coverage**
- Invoke: `quality-reviewer`
- Analyze: Test coverage >80%? Edge cases tested?

**Dimension 3: Code-Documentation Consistency**
- Invoke: `quality-reviewer`
- Check: README updated? APIs documented?

**Dimension 4: Risk Mitigation Verification**
- Invoke: `architect`
- Verify: Were identified risks addressed? Mitigations implemented?

**Dimension 5: File Manifest Match** (NEW!)
- Invoke: `architect`
- Compare: Planned vs actual files
- Flag: Unplanned files (scope creep)
- Verify: Integration points connected

### Output

```markdown
## Validation Report

### Overall Consistency: 91% ✅

**Dimensions:**
1. Plan-Code: 95% ✅
2. Code-Tests: 92% ✅
3. Code-Docs: 88% ✅
4. Risk Mitigation: 90% ✅
5. File Manifest: 92% ✅

**Issues:**
- [H-004] Risk mitigation incomplete (token refresh race condition)
- [H-007] Unplanned middleware added (scope expansion)
- [M-001] API response format differs from plan
- [L-003] Missing JSDoc on 3 functions

**Recommendation:**
Fix 2 HIGH issues before merging. Overall 91% consistency PASSES (>90% target).
```

**Tokens:** 20k-45k

---

## Token Economics Summary

| Workflow | Tokens | vs Manual | Worth It? |
|----------|--------|-----------|-----------|
| REVIEW | 20k-50k | Always worth it | ✅✅ |
| PLANNING (simple, stops early) | 3.2k | 5k manual | ⚠️ Maybe |
| PLANNING (complex, full) | 5.2k | 15k manual | ✅ If docs valued |
| BUILDING (complexity 4-5) | 60k-150k | 15k-50k | ✅ Prevents mistakes |
| DEBUGGING (complex) | 15k-30k | 5k-10k | ✅ Saves guessing time |
| VALIDATION | 20k-45k | 0 (manual checklist) | ⚠️ If accountability needed |

**Honest reality:** I cost MORE tokens, but provide systematic frameworks.

**Use me for:** Complexity 4-5, high-risk features, team collaboration
**Skip me for:** Complexity 1-2, solo dev, time-sensitive

---

## How to Invoke Me

### Method 1: Natural Language (Preferred)

Just describe your need:
- "Review this code for security issues"
- "Plan authentication feature"
- "Debug why rate limiting isn't working"

**Note:** Skills don't auto-trigger 100% reliably (brutal testing showed 0% rate). If I don't trigger automatically, use Method 2.

### Method 2: Explicit Skill Invocation (Guaranteed)

```
"Use cc10x-orchestrator skill to review src/auth.js"
"Use cc10x-orchestrator skill to plan payment processing"
"Apply cc10x-orchestrator to debug login issue"
```

This ALWAYS works (forces skill loading).

### Method 3: Slash Command (If Available)

```
/cc10x review src/auth.js
/cc10x plan authentication feature
/cc10x debug login timeout
```

If slash command exists, it just loads me and passes your request through.

---

## The 5 Workflows at a Glance

### 1. REVIEW ⭐⭐⭐⭐⭐
- **Use:** Before EVERY PR, after any code changes
- **Skip:** Trivial changes (<20 lines), WIP code
- **Time:** 2-3 minutes
- **Tokens:** 20k-50k
- **Value:** Finds CRITICAL security issues, prevents breaches

### 2. PLANNING ⭐⭐⭐☆☆
- **Use:** Complexity 4-5, novel architecture needed
- **Skip:** Complexity 1-2, using well-documented library
- **Time:** 5-10 minutes
- **Tokens:** 3.2k (early stop) to 5.2k (full)
- **Value:** Prevents architecture mistakes (one prevented rewrite = worth it)

### 3. BUILDING ⭐☆☆☆☆
- **Use:** Complexity 4-5, want strict TDD
- **Skip:** Complexity <3, time-sensitive
- **Time:** 20-40 minutes
- **Tokens:** 60k-150k
- **⚠️ MUST verify tests manually!**
- **Value:** Systematic TDD, but expensive

### 4. DEBUGGING ⭐⭐☆☆☆
- **Use:** Complex bugs, root cause unclear
- **Skip:** Obvious fixes, emergencies
- **Time:** 10-20 minutes
- **Tokens:** 15k-30k
- **Value:** LOG FIRST saves hours of guessing

### 5. VALIDATION ⭐⭐⭐☆☆
- **Use:** Pre-PR, team accountability
- **Skip:** No plan exists, already used BUILD workflow
- **Time:** 5-10 minutes
- **Tokens:** 20k-45k
- **Value:** Consistency verification

---

## Integration with Sub-Agents

I orchestrate by invoking:

**Review Workflow:** 5 review agents in parallel
**Planning Workflow:** requirements-analyst → context-analyzer → architect → devops-planner (sequential)
**Building Workflow:** context-analyzer → architect → tdd-enforcer (per increment) → 5 review agents (parallel)
**Debugging Workflow:** context-analyzer → tdd-enforcer
**Validation Workflow:** architect + quality-reviewer

**Agents then load domain skills progressively:**
- feature-planning (5 stages)
- risk-analysis (7 stages)
- deployment-patterns (2 stages)
- systematic-debugging
- test-driven-development (3 stages)
- security-patterns, code-review-patterns, performance-patterns, etc.

---

## Remember

I am a SKILL that orchestrates workflows by:
1. **Detecting** what you need (task type + complexity)
2. **Assessing** if systematic approach adds value (recommends manual when better!)
3. **Recommending** honestly (shows real test failures for simple features)
4. **Orchestrating** specialized agents and domain skills (when proceeding)
5. **Delivering** production-ready results (with verification)

**I'm not magic automation - I'm systematic frameworks that prevent common mistakes.**

**Key principles:**
- ✅ Use REVIEW workflow for everything (5⭐ killer feature)
- ✅ Check complexity FIRST before planning/building
- ✅ Recommend manual for simple features (no shame in skipping me!)
- ✅ Require verification (never trust "tests passing" without proof)
- ✅ Load skills progressively (real 65-79% savings vs v1.x)

**Philosophy:** Use the right tool for the job. Simple? Go manual. Complex? Use me.

---

## Complexity Quick Reference

**1 (TRIVIAL):** <50 lines, 1 file → ❌ Skip cc10x (5-10 min manual)
**2 (SIMPLE):** <200 lines, 2-3 files, library → ❌ Skip cc10x (read library docs)
**3 (MODERATE):** 200-500 lines, 4-6 files → ⚠️ Maybe (if docs valued)
**4 (COMPLEX):** 500-1000 lines, 7-15 files → ✅ Use cc10x
**5 (VERY COMPLEX):** >1000 lines, 15+ files → ✅✅ Use cc10x (essential!)

**High-risk (auth/payments) = treat as complexity +1 regardless of size**

---

---

## Error Handling

### If Agent Invocation Fails

**Symptom:** Agent doesn't respond or returns error

**Actions:**
1. Retry once (may be transient issue)
2. If second failure: Report to user with error details
3. Suggest fallback: "I can provide manual guidance instead of using the [agent-name] agent"
4. Continue with reduced workflow (skip failed agent phase)

**Example:**
```
Attempted to invoke: context-analyzer agent
Error: Agent timeout after 60 seconds

Retrying... (attempt 2/2)
Error: Agent still unavailable

Fallback: Proceeding without codebase context analysis.
I'll implement based on your requirements alone. 
Quality may be lower without pattern reference.
```

### If Skill Loading Fails

**Symptom:** Skill file not found or loading error

**Actions:**
1. Check if skill exists: `ls plugins/cc10x/skills/[skill-name]/SKILL.md`
2. If missing: Report which skill is missing
3. Suggest: Update plugin installation or check for corrupted install
4. Continue without that skill (degraded functionality)

**Example:**
```
Attempting to load: cc10x:risk-analysis Stage 5
Error: SKILL.md not found at plugins/cc10x/skills/risk-analysis/

This skill is required for security risk analysis.

Suggestions:
1. Reinstall cc10x plugin: /plugin uninstall cc10x@cc10x && /plugin install cc10x@cc10x
2. Check installation: ls ~/.claude/plugins/marketplaces/cc10x/plugins/cc10x/skills/

Proceeding without risk analysis (reduced security checking).
```

### If User Input Ambiguous

**Symptom:** Can't determine task type or complexity

**Actions:**
1. Don't guess - ask clarifying questions
2. Present detected possibilities
3. Let user choose
4. Continue with chosen path

**Example:**
```
Your message: "Help with authentication"

I detected multiple possible tasks:
(a) REVIEW - Review existing authentication code for issues
(b) PLAN - Plan new authentication feature architecture
(c) BUILD - Implement authentication from existing plan
(d) DEBUG - Fix authentication bug

Which task type? (a/b/c/d)
```

### If Complexity Assessment Uncertain

**Symptom:** Can't determine if feature is simple or complex

**Actions:**
1. Ask specific questions (don't guess)
2. How many files affected?
3. Using library or novel pattern?
4. High-risk domain (auth/payments)?
5. Make informed decision based on answers

**Example:**
```
Complexity assessment needs clarification:

Questions:
1. How many files will this affect? (1-3 = simple, 7+ = complex)
2. Are you using a well-documented library, or creating novel patterns?
3. Is this security-critical (auth/payments/data handling)?

Based on your answers, I'll assess complexity (1-5) and recommend 
whether cc10x adds value or manual is better.
```

### If Workflow Execution Fails Mid-Process

**Symptom:** Error during workflow execution (Phase 3, 4, etc.)

**Actions:**
1. Save progress so far (partial output)
2. Report which phase failed
3. Provide what was completed
4. Suggest recovery options

**Example:**
```
PLANNING workflow error at Phase 3b (Risk Assessment):

Completed:
✅ Phase 1: Requirements (saved)
✅ Phase 2: Context Analysis (saved)
✅ Phase 3: Architecture Decisions (saved)
❌ Phase 3b: Risk Assessment (FAILED - architect agent error)

Partial plan saved to: .claude/plans/FEATURE_AUTH_partial.md

Recovery options:
(a) Retry Phase 3b only (recommended)
(b) Skip risk assessment, continue to Phase 3c
(c) Stop here, use partial plan

Which option?
```

---

**That's me - the cc10x Master Orchestrator. ONE skill to orchestrate them all! ✨**

