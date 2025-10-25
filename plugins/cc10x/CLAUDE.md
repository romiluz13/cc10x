# cc10x v2 - Reality-Based Development System

**One killer feature + Four systematic workflows**

## ⚠️ Reality Check (Read This First)

### What cc10x Actually Is

**✅ What You're Getting:**

**ONE EXCELLENT COMMAND:** `/review` ⭐⭐⭐⭐⭐
- Uses working AI agents (security, quality, performance, UX, accessibility)
- Runs in parallel (fast results)
- Found 38 real issues in testing (5 CRITICAL)
- Worth every token (one prevented breach = infinite ROI)

**FOUR SYSTEMATIC WORKFLOWS:**
- `/feature-plan` ⭐⭐⭐☆☆ - Complexity assessment, File manifests, Rollback/Deployment plans
- `/feature-build` ⭐☆☆☆☆ - TDD workflow (MUST verify outputs manually!)
- `/bug-fix` ⭐⭐☆☆☆ - LOG FIRST debugging pattern
- `/validate` ⭐⭐⭐☆☆ - Cross-artifact validation

**HONEST POSITIONING:**
- NOT faster (similar time, more systematic)
- NOT token savings for simple tasks (3-20x MORE)
- NOT autonomous (you do the work, we guide)
- YES valuable for complexity 4-5

### What You're NOT Getting

❌ Autonomous AI magic (you do the work, prompts guide you)
❌ Auto-triggering skills (commands explicitly invoke them)
❌ Token savings for simple tasks (costs MORE for structure)
❌ Always better than manual (use for complex features only)
❌ Guaranteed success (MUST verify test outputs manually)

---

## Quick Start: Use What Actually Works

### Step 1: Try /review (The Killer Feature)

```bash
/review src/your-code.js
```

**What happens:**
- 5 AI agents launch in parallel
- Analyze code from 5 dimensions
- Find real issues with specific fixes
- Report findings with line numbers

**Real test results:**
- Found: 38 issues (5 CRITICAL, 12 HIGH, 21 MODERATE/LOW)
- CRITICAL: SQL injection, hardcoded secrets, auth bypass
- Time: 2-3 minutes
- Tokens: 20k-50k

**Verdict:** ⭐⭐⭐⭐⭐ (5/5 stars) - Actually works as advertised!

**Use before EVERY PR.**

---

### Step 2: Consider Systematic Workflows (For Complex Features)

The other 4 commands provide structured frameworks by explicitly invoking sub-agents and skills.

**When to use:**
- Complex features (complexity 4-5: 500+ lines, 7+ files, novel patterns)
- Team documentation needed (alignment, accountability)
- Want to prevent common mistakes (systematic approach)

**When to skip:**
- Simple features (complexity 1-2: <200 lines, using libraries)
- Time-sensitive (manual faster)
- Token budget matters (costs 3-20x MORE)
- Solo dev, familiar pattern

## The Commands Explained

### /feature-plan ⭐⭐⭐☆☆

**What it does:** Creates comprehensive feature plans with complexity assessment

**When to use:** Complexity 4-5, need architecture decisions

**When to skip:** Complexity 1-2 (just read library docs instead)

**Example:**
```bash
/feature-plan Add real-time notifications with WebSockets
```

**Produces:**
- Requirements & user stories
- Architecture decisions (alternatives compared)
- Risk assessment (Probability × Impact)
- **Complexity assessment** (NEW! - Recommends skip if simple)
- **File change manifest** (NEW! - Prevents scope creep)
- **Rollback strategy** (NEW! - < 5 min recovery)
- **Deployment plan** (NEW! - Staged rollout)

**Time:** 5-10 minutes
**Tokens:** 20k-40k (3-8x MORE than manual)
**Value:** Prevents architecture mistakes (worth it for complex features)

---

### /feature-build ⭐☆☆☆☆

**What it does:** TDD workflow with risk analysis before each increment

**When to use:** Complexity 4-5, want strict TDD enforcement

**When to skip:** Complexity <3, time-sensitive, need reliability

**⚠️ CRITICAL:** Always manually verify tests pass! During testing, reported "✅ All 33 tests passing!" when 3/7 FAILED.

**Example:**
```bash
/feature-build Implement authentication from plan
```

**Process:**
- Context analysis (find patterns)
- Break into increments
- For each increment:
  - Risk analysis (what could go wrong?)
  - TDD cycle (RED-GREEN-REFACTOR)
  - File manifest check
  - **MANDATORY test verification** (you MUST see tests pass)
- Multi-dimensional review (5 agents)
- Finalization

**Time:** 20-40 minutes
**Tokens:** 40k-80k (8-16x MORE than manual)
**Value:** Systematic TDD, but MUST verify outputs

**Real test:** Rate limiting (complexity 2)
- cc10x: 100k tokens, false success, tests failed
- Manual: Would be 30 min, 5k tokens, working code
- **Lesson:** Don't use for simple features!

---

### /bug-fix ⭐⭐☆☆☆

**What it does:** Enforces LOG FIRST debugging pattern

**When to use:** Complex bugs, root cause unclear

**When to skip:** Obvious fixes, emergencies, know the cause

**Example:**
```bash
/bug-fix Rate limiting not blocking requests
```

**The LOG FIRST Pattern:**
1. Add comprehensive logging (see actual data)
2. Reproduce bug (observe logs)
3. Identify root cause (from actual data, not assumptions)
4. Minimal fix with test
5. Remove debug logging

**Time:** 10-20 minutes
**Tokens:** 15k-30k (5-10x MORE)
**Value:** LOG FIRST pattern is brilliant (saves hours of guessing)

**Real test:** Saved 2 hours by logging first instead of guessing

---

### /validate ⭐⭐⭐☆☆

**What it does:** Validates plan-code-tests-docs consistency

**When to use:** Pre-PR checks, periodic audits

**When to skip:** No plan exists, already used `/feature-build`

**Example:**
```bash
/validate
```

**Validates:**
- Plan matches code (did we build what we planned?)
- Code has tests (comprehensive coverage?)
- Code documented (README updated?)
- Risks mitigated (were mitigations implemented?)
- **File manifest** (NEW! - Files match plan?)

**Time:** 5-10 minutes
**Tokens:** 20k-45k
**Value:** Consistency verification, team accountability

---

## The 3-Layer Architecture (v2.0)

```
LAYER 1: COMMANDS (Orchestration)
  ↓ Thin files (150-300 lines) that invoke agents
  
LAYER 2: SUB-AGENTS (Execution)
  ↓ 11 specialized agents that load skills progressively
  
LAYER 3: SKILLS (Knowledge)
  ↓ 17 rich knowledge bases with progressive loading
```

### What This Enables

**Progressive Loading (REAL in v2.0!):**

Before (v1.x): Command loads 15k tokens upfront
After (v2.0): Command loads 200 tokens → Agents load skills on-demand

**Example (feature-plan):**
- Command: 200 tokens
- requirements-analyst: Loads Skill Stage 1 = 500 tokens
- context-analyzer: Loads Skill Stages 1-2 = 1,100 tokens
- architect: Loads Skill Stages 2-4 = 2,300 tokens
- devops-planner: Loads Skill Stages 1-2 = 1,100 tokens
- **Total: ~5,200 tokens (vs 15k before = 65% savings!)**

If feature is simple (complexity < 3), stops early:
- Only: 200 + 500 + 1,100 + 1,400 = 3,200 tokens
- **79% savings with early termination!**

**This is REAL progressive loading.** v1.x claim was false.

---

## The 11 Sub-Agents

### The 5 Working Agents (Review Command) ⭐⭐⭐⭐⭐

**Used by:** `/review` exclusively

1. **security-reviewer** - Finds SQL injection, XSS, auth bypasses
2. **quality-reviewer** - Finds code smells, duplication, maintainability issues
3. **performance-analyzer** - Finds O(n²) loops, memory leaks, bottlenecks
4. **ux-reviewer** - Finds UX issues, error message problems
5. **accessibility-reviewer** - Finds WCAG violations, keyboard navigation issues

**Status:** Fully working, parallel execution, 5⭐ verified

---

### The 4 NEW Orchestration Agents (v2.0)

**Used by:** Feature planning and building commands

6. **architect** - Architecture decisions, complexity assessment, file manifests
7. **devops-planner** - Rollback strategies, deployment plans
8. **requirements-analyst** - Requirements gathering, user stories
9. **tdd-enforcer** - Strict TDD enforcement, mandatory verification

**Status:** v2.0 addition, progressively load skills, enforce quality gates

---

### The 2 Implementation Agents

10. **context-analyzer** - Finds similar features, extracts project patterns
11. **implementer** - Feature implementation (can report false success - verify manually!)

**Status:** Enhanced in v2.0 with File Manifest verification

---

## The 17 Skills

Skills are knowledge bases that agents load progressively:

1. **accessibility-patterns** - WCAG patterns
2. **bug-fixing** - Bug fix strategies
3. **code-generation** - Code patterns
4. **code-review-patterns** - Code smells, refactoring
5. **code-reviewing** - Review methodologies
6. **codebase-navigation** - Search strategies
7. **feature-building** - Implementation patterns
8. **feature-planning** - Planning frameworks (5 stages!)
9. **performance-patterns** - Optimization techniques
10. **safe-refactoring** - Refactoring patterns
11. **security-patterns** - OWASP Top 10, secure coding
12. **systematic-debugging** - LOG FIRST pattern
13. **test-driven-development** - RED-GREEN-REFACTOR (3 stages!)
14. **ui-design** - Lovable/Bolt-quality UI patterns
15. **ux-patterns** - UX best practices
16. **verification-before-completion** - Quality checklists
17. **deployment-patterns** (NEW!) - Rollback & deployment strategies
18. **risk-analysis** (NEW!) - "What Could Go Wrong?" 7-dimension methodology

**Status:** Skills don't auto-trigger (must be explicitly invoked by agents)

---

## When cc10x Shines (And When It Doesn't)

### ✅ Use cc10x For:

**Complexity 4-5 Features:**
- 500-1000+ lines of code
- 7+ files affected
- Novel patterns (not in codebase)
- Critical architecture decisions
- High-risk changes (auth, payments, data integrity)

**Security-Sensitive Code:**
- Authentication/authorization
- Payment processing
- Data handling (PII, financial)
- API endpoints (public-facing)

**Team Collaboration:**
- Need documentation for alignment
- Want accountability (prove plan followed)
- Enterprise compliance requirements

**Examples that benefit:**
- Real-time notifications with WebSockets
- Multi-tenancy with data isolation
- Payment processing with Stripe
- Complex state management

---

### ❌ Skip cc10x For:

**Complexity 1-2 Features:**
- <200 lines of code
- Using well-documented libraries
- Single file changes
- Standard patterns

**Time-Sensitive:**
- Production emergencies
- Quick hotfixes
- Prototype/MVP development

**Solo Development:**
- Familiar patterns
- No documentation needed
- Comfortable with the technology

**Examples that don't benefit:**
- Add rate limiting with express-rate-limit (read library docs instead)
- Add form validation with Zod (follow Zod docs)
- Fix typo or syntax error (just fix it)

**Real test:** Simple rate limiting
- cc10x: 100k tokens, 90 minutes, tests failed
- Manual: 5k tokens, 30 minutes, working code
- **Verdict:** cc10x was WORSE for simple feature

---

## Token Economics (Brutal Honesty)

### The Reality

cc10x uses **3-20x MORE tokens** than manual implementation, not savings.

**Why?**
- Systematic multi-phase analysis
- Progressive skill loading still has overhead
- Multiple specialized agents
- Comprehensive documentation

**Is it worth it?**

| Feature Complexity | Tokens (cc10x) | Tokens (Manual) | Worth It? |
|-------------------|----------------|-----------------|-----------|
| 1 (TRIVIAL) | 40k | 2k | ❌ NO (20x more!) |
| 2 (SIMPLE) | 80k | 5k | ❌ NO (16x more!) |
| 3 (MODERATE) | 100k | 15k | ⚠️ MAYBE (7x more) |
| 4 (COMPLEX) | 120k | 30k | ✅ YES (4x more, prevents rework) |
| 5 (VERY COMPLEX) | 180k | 50k | ✅✅ YES (4x more, prevents disasters) |

**The ROI Calculation:**
- Complexity 1-2: Waste of tokens (just implement manually)
- Complexity 3: Borderline (worth it IF team docs valued)
- Complexity 4-5: Worth it (one prevented architecture mistake pays for planning)

**Special case - /review:**
- Always worth it (prevents security breaches, performance bugs)
- Use before EVERY PR regardless of complexity

---

## Best Practices

### 1. Start with /review

```bash
# ALWAYS start here (it actually works!)
/review src/your-changes.js
```

This is the ONLY command guaranteed to work. It will find real issues.

---

### 2. Check Complexity Before Planning

**Quick assessment:**
- How many files? (<3 = simple, 7-15 = complex)
- Using library? (simple) or novel pattern? (complex)
- High-risk? (auth/payments = complex regardless of size)

**If complexity < 3:** Skip cc10x, implement manually
**If complexity >= 4:** Use `/feature-plan`

---

### 3. ALWAYS Verify Test Outputs

**During testing, /feature-build reported:**
> "✅ All 33 tests passing!"

**Reality:** 3 out of 7 tests FAILED

**You MUST:**
```bash
npm test  # Run actual tests
echo $?   # Verify exit code = 0
# SEE the results with your eyes
```

**Never trust workflow success reports. Always verify independently.**

---

### 4. Use LOG FIRST for Complex Bugs

If you've spent >30 minutes guessing on a bug:

```bash
/bug-fix Description of the bug
```

The LOG FIRST pattern will save you hours by forcing you to see actual data before fixing.

---

### 5. Know When to Go Manual

**cc10x is NOT always better.** Go manual when:
- Simple feature (follow library docs faster)
- Emergency (fix now, document later)
- Time-sensitive (similar time but manual more direct)
- Token budget (cc10x is expensive)

**No shame in skipping cc10x for simple tasks!**

---

## How It Works

### The 3-Layer Architecture

```
YOU type: /feature-plan Add authentication
  ↓
COMMAND (Layer 1): Thin orchestrator (200 tokens)
  ↓ Invokes agents in sequence
SUB-AGENTS (Layer 2): Specialized workers (11 agents)
  ↓ Load skills progressively
SKILLS (Layer 3): Knowledge bases (17 skills, 500-2000 lines each)
  ↓ Provide frameworks, patterns, checklists
RESULT: Comprehensive plan with 7 phases
```

**Progressive Loading:**
- Commands don't embed instructions (v1.x was 15k tokens upfront)
- Agents load ONLY the skill stages they need
- Real token savings: 65-83% (vs v1.x embedded approach)

**Example (feature-plan):**
```
Phase 1: Invoke requirements-analyst
  → Loads feature-planning Skill Stage 1 (500 tokens)
  
Phase 2: Invoke context-analyzer
  → Loads codebase-navigation Skill Stages 1-2 (1,100 tokens)
  
Phase 3: Invoke architect
  → Loads feature-planning Skill Stage 2 (800 tokens)
  
Phase 3a: Same agent (NEW!)
  → Loads risk-analysis Stages 1+5 (1,400 tokens)
  
Phase 3b: Same agent
  → Loads feature-planning Skill Stage 3 (400 tokens)
  
Phase 3c: Same agent (NEW!)
  → Loads feature-planning Skill Stage 4 - Complexity (600 tokens)
  → If complexity < 3: Recommends skip cc10x!
  
If complexity >= 4, continues...
Phase 4-7: Testing, Roadmap, Manifest, Rollback, Deployment
  → Additional 1,400 tokens

Total: ~5,200 tokens (simple) or ~6,600 tokens (complex)

vs v1.x: 15,000 tokens upfront

Savings: 65-79% (REAL progressive loading!)
```

---

## What's NEW in v2.0

### 1. Risk Analysis Everywhere

**"What Could Go Wrong?" 7-Dimension Methodology:**

Invoked at multiple phases:
- **Planning:** architect invokes Stages 1+5 (Data Flow + Security)
- **Implementation:** tdd-enforcer invokes Stages 1+3+7 (before each increment)
- **Review:** quality-reviewer invokes ALL 7 stages (comprehensive)

**7 Dimensions:**
1. Data Flow & Transformations
2. Dependency & Integration Mapping
3. Timing, Concurrency & State
4. User Experience & Human Factors
5. Security & Validation
6. Performance & Scalability
7. Failure Modes & Recovery

**Result:** Finds edge cases BEFORE they become production bugs

---

### 2. Cursor IDE Enhancements Integrated

**Complexity Assessment (Phase 3c):**
- 1-5 scoring (TRIVIAL → VERY COMPLEX)
- Honest recommendation (skip cc10x if < 3)
- Token economics comparison

**File Change Manifest (Phase 5b):**
- CREATE/MODIFY/DELETE breakdown
- LOC estimates
- Integration points
- Prevents scope creep

**Rollback Strategy (Phase 6):**
- Level 1: Feature flag (< 5 min)
- Level 2: Configuration (< 10 min)
- Level 3: Code rollback (< 15 min)

**Deployment Plan (Phase 7):**
- 5-stage rollout (Infrastructure → Canary → Partial → Full)
- Risk-aware sequencing
- Monitoring dashboards

---

### 3. Mandatory Test Verification

**Problem (v1.x):** Agents reported false success

**Solution (v2.0):** Mandatory independent verification

```bash
# You MUST run and verify:
npm test
echo $?  # Must be 0

# Don't trust reports, see results with YOUR EYES
```

---

### 4. Honest Positioning

**v1.x claims (FALSE):**
- "93% token savings" ❌
- "Auto-triggering skills" ❌
- "10x faster" ❌
- "Always better" ❌

**v2.0 reality (HONEST):**
- "65-79% savings vs v1.x embedded prompts" ✅
- "3-20x MORE tokens than manual" ✅
- "More systematic, not faster" ✅
- "Better for complexity 4-5 only" ✅

---

## Complexity Guide

Use this to decide if cc10x adds value:

### Complexity 1: TRIVIAL
- **Example:** Add form field validation
- **Files:** 1
- **Lines:** <50
- **Decision:** ❌ Skip cc10x (5-10 min manual)

### Complexity 2: SIMPLE
- **Example:** Add rate limiting with express-rate-limit
- **Files:** 2-3
- **Lines:** 50-200
- **Decision:** ❌ Skip cc10x (follow library docs)

### Complexity 3: MODERATE
- **Example:** Add pagination with caching
- **Files:** 4-6
- **Lines:** 200-500
- **Decision:** ⚠️ Maybe (if team docs valued)

### Complexity 4: COMPLEX
- **Example:** Real-time notifications with WebSockets
- **Files:** 7-15
- **Lines:** 500-1000
- **Decision:** ✅ Use cc10x (prevents mistakes)

### Complexity 5: VERY COMPLEX
- **Example:** Multi-tenancy with data isolation
- **Files:** 15+
- **Lines:** >1000
- **Decision:** ✅✅ Use cc10x (essential!)

---

## Remember

cc10x is **structured prompt engineering**, not magic automation.

**Benefits:**
- `/review` actually works (5⭐, use liberally)
- Systematic workflows prevent common mistakes
- "What Could Go Wrong?" finds edge cases early
- Good for complex features (4-5 complexity)

**Limitations:**
- Expensive (3-20x more tokens)
- Not faster (similar time, more systematic)
- Must verify outputs (agents can report false success)
- Overkill for simple features

**Philosophy:**
Use the right tool for the job. Simple features? Go manual. Complex features? Use cc10x.

**Start with `/review` - it's the best part of cc10x!**
