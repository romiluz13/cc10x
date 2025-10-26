# cc10x v3 - User Guide

**The Perfect Fusion: Simplicity + Power**

---

## Reality Check (Read This First!)

### What cc10x v3 Actually Is

**✅ ONE KILLER FEATURE:** `/cc10x review` ⭐⭐⭐⭐⭐
- 5 parallel AI agents (security, quality, performance, UX, accessibility)
- Found 38 real issues in testing (5 CRITICAL: SQL injection, secrets, auth bypass)
- **Use before EVERY PR!**

**✅ FOUR SYSTEMATIC WORKFLOWS:**
- PLANNING ⭐⭐⭐☆☆ - Quick defaults → comprehensive planning (complexity 4-5)
- BUILDING ⭐⭐☆☆☆ - TDD enforcement (requires manual test verification!)
- DEBUGGING ⭐⭐⭐☆☆ - LOG FIRST pattern (saves hours of guessing)
- VALIDATION ⭐⭐⭐☆☆ - Cross-artifact consistency (team projects)

**✅ HONEST POSITIONING:**
- **Costs 3-20x MORE tokens than manual** (not savings!)
- Valuable for complexity 4-5 (prevents costly mistakes)
- Recommends SKIP for simple features (saves your tokens!)
- Review workflow always worth it (prevents security breaches)

### What You're NOT Getting

❌ Autonomous AI magic (you do the work, prompts guide you)
❌ Token savings for simple tasks (costs MORE for systematic approach)
❌ Always better than manual (use for complex features only)
❌ Auto-triggering (use `/cc10x` command for reliability)

### What's NEW in v3

✅ **4+5 architecture** - 4 execution + 5 review agents (vs 11 overlapping)
✅ **TRUE progressive disclosure** - 50-75% token savings (workflows load on-demand)
✅ **Quick default plans** - Phase 0a avoids 120k waste on wrong assumptions
✅ **End-to-end automation** - "plan and build" in one command
✅ **PostToolUse hook** - Enforces <500 lines automatically
✅ **Mandatory test verification** - Prevents false "tests passing" reports
✅ **ONE workflow scales** - Simple to complex naturally

**Inspired by:** cc10x_V2-main (simplicity) + cc10x v2 (proven patterns)

---

## Quick Start

### Step 1: Install

```bash
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x
```

### Step 2: Try the Killer Feature

```bash
/cc10x review src/your-code.js
```

This ALWAYS works and ALWAYS provides value. Use liberally!

---

## The 5 Workflows

### 1. REVIEW ⭐⭐⭐⭐⭐ (Always Worth It!)

**Use:** Before EVERY PR, any complexity

**Command:**
```bash
/cc10x review src/auth.js
/cc10x audit src/features/payment/
```

**What happens:**
1. 5 agents launch in parallel (2-3 minutes)
2. Security → SQL injection, XSS, auth bypasses
3. Quality → Code smells, DRY/SOLID violations
4. Performance → O(n²) loops, N+1 queries, caching
5. UX → Error messages, loading states
6. Accessibility → WCAG violations, keyboard nav

**Real results:**
- Found: 38 issues (5 CRITICAL, 12 HIGH)
- Time: 3 minutes
- Tokens: 20k-50k

**Verdict:** Worth EVERY token. One prevented breach >> infinite tokens.

**Use before EVERY PR!**

---

### 2. PLANNING ⭐⭐⭐☆☆ (Complexity 4-5)

**Use:** Complex features (500+ lines, 7+ files, architecture decisions)

**Skip:** Simple features (complexity 1-2: manual is 16x cheaper!)

**Command:**
```bash
/cc10x plan real-time notifications with WebSockets
```

**What happens:**
1. **Phase 0:** Complexity check (1-5 scoring)
   - If 1-2: "This is SIMPLE. Manual is 16x cheaper. Skip cc10x?"
   - If 3: "Moderate complexity. Show token tradeoffs. Proceed?"
   - If 4-5: "Complex. Systematic planning valuable. Proceeding..."

2. **Phase 0a:** Quick default plan (3-5k tokens) **[NEW in v3!]**
   - Shows intelligent defaults (OAuth: NO, tokens: 15min/7day, etc.)
   - Lists 5-7 critical assumptions
   - OPTIONS: (a) Proceed / (b) Customize / (c) Manual
   - **Prevents 120k waste if assumptions wrong!**

3. **Phases 1-7:** Full planning (if user approves)
   - Requirements (feature-planner agent) → PRD
   - Architecture (architect agent) → Design + technology decisions
   - Risk analysis (7 dimensions) → Edge cases identified
   - Testing strategy → Unit/integration/e2e plans
   - File manifest → CREATE/MODIFY/DELETE breakdown
   - Rollback strategy → <5 min recovery
   - Deployment strategy → 5-stage rollout

**Output:** Comprehensive plan in `.claude/plans/FEATURE_[NAME].md`

**Cost:** 30-60k tokens (vs 15k manual = 2-4x MORE)

**Worth it:** Complexity 4-5 (prevents architecture mistakes >> token cost)

---

### 3. BUILDING ⭐⭐☆☆☆ (Use with Caution)

**Use:** Complexity 4-5, want strict TDD enforcement

**Skip:** Simple features, time-sensitive (manual often better)

**Command:**
```bash
/cc10x build from plan authentication

# Or end-to-end (NEW in v3!):
/cc10x plan and build authentication
```

**What happens:**
1. **Phase 0:** Strong complexity check
   - If <=2: "STOP! Rate limiting test: cc10x WORSE than manual. Skip?"

2. **Phase 1-2:** Context + task breakdown
   - Finds similar features
   - Creates TODO.md with file-size-aware tasks

3. **Phase 3:** TDD implementation (sequential!)
   - **For each increment:**
     - Risk analysis (what could go wrong?)
     - RED: Write failing test
     - GREEN: Minimal implementation
     - REFACTOR: Improve code
     - File manifest check
     - **MANDATORY verification:** User must confirm tests pass!

4. **Phase 4:** Test generation (test-generator agent)
   - Comprehensive tests (>80% coverage)
   - **MANDATORY verification:** User runs `npm test`, confirms

5. **Phase 5:** Multi-dimensional review (5 agents parallel)
   - Fix CRITICAL issues before finalizing

6. **Phase 6:** Finalization
   - Remove debug code
   - Update documentation
   - Stage for commit

**⚠️ CRITICAL:** v2 testing showed false "tests passing" reports. v3 REQUIRES you manually verify. Don't trust reports!

**Cost:** 40-80k tokens (vs 20k manual = 2-4x MORE)

**Worth it:** Complexity 4-5 with strict TDD needs

---

### 4. DEBUGGING ⭐⭐⭐☆☆ (LOG FIRST Pattern)

**Use:** Complex bugs, root cause unclear, spent >30 min guessing

**Skip:** Obvious fixes, emergencies

**Command:**
```bash
/cc10x debug rate limiting not blocking requests
```

**The LOG FIRST Pattern:**
1. **Add logging** to see ACTUAL data (don't assume!)
2. **Reproduce bug**, observe logs
3. **Identify root cause** from actual data
4. **Minimal fix** based on observations
5. **Add regression test**
6. **Remove debug logging**

**Real test:** Saved 2 hours by logging first instead of trying 5 random fixes.

**Cost:** 15-30k tokens (vs 5k manual = 3-6x MORE)

**Worth it:** Saves 1-3 hours of guessing (time >> tokens)

---

### 5. VALIDATION ⭐⭐⭐☆☆ (Team Accountability)

**Use:** Team projects, pre-PR checks

**Skip:** Solo dev, no plan exists

**Command:**
```bash
/cc10x validate
```

**What it checks:**
1. Plan → Code (did we build what we planned?)
2. Code → Tests (is code tested >80%?)
3. Code → Docs (is code documented?)
4. Risks → Mitigations (were risks addressed?)
5. File Manifest → Actual (matches plan? scope creep?)

**Cost:** 20-45k tokens

**Worth it:** Team projects (prevents drift, enables accountability)

---

## How to Invoke

### Method 1: Slash Command (Recommended - Guaranteed)

```bash
/cc10x [your request]
```

**Why:** Natural language triggering is unreliable. Slash command guarantees orchestrator loads.

**Examples:**
```bash
/cc10x review src/auth.js
/cc10x plan and build authentication
/cc10x debug login timeout
```

### Method 2: Natural Language (May Not Trigger)

```
"Review this code for security"
"Plan authentication feature"
```

**If skill triggers:** Works perfectly  
**If skill doesn't trigger:** Nothing happens

**Recommendation:** Use `/cc10x` for reliability

---

## Complexity Guide (Critical!)

cc10x v3 **honestly** assesses complexity and recommends the right approach:

### Complexity 1: TRIVIAL
- **Files:** 1
- **Lines:** <50
- **Examples:** Config change, typo fix
- **Recommendation:** ❌ Skip cc10x (manual 20x cheaper, just do it!)

### Complexity 2: SIMPLE
- **Files:** 2-3
- **Lines:** 50-200
- **Examples:** Add rate limiting (express-rate-limit), form validation (Zod)
- **Recommendation:** ❌ Skip cc10x (follow library docs, manual 16x cheaper)

**Real test:** Rate limiting (complexity 2)
- cc10x: 100k tokens, 90 min, reported "tests passing", actually 3/7 FAILED
- Manual: 5k tokens, 30 min, working code from library docs
- **Verdict: cc10x was WORSE!**

### Complexity 3: MODERATE
- **Files:** 4-6
- **Lines:** 200-500
- **Examples:** Pagination with caching, file upload, search filters
- **Recommendation:** ⚠️ Maybe (if team docs valued, otherwise manual better)

### Complexity 4: COMPLEX
- **Files:** 7-15
- **Lines:** 500-1,000
- **Examples:** Real-time notifications (WebSockets), complex state management
- **Recommendation:** ✅ Use cc10x (prevents architecture mistakes)

### Complexity 5: VERY COMPLEX
- **Files:** 15+
- **Lines:** >1,000
- **Examples:** Multi-tenancy with data isolation, payment processing (Stripe)
- **Recommendation:** ✅✅ Use cc10x (essential for success!)

**Exception:** REVIEW always worth it (any complexity)

---

## The 4+5 Architecture

### 4 Core Execution Agents (Sequential)

**From cc10x_V2-main - proven simple architecture:**

1. **feature-planner** - Product manager
   - Creates: Comprehensive PRDs with user stories
   - Scales: 200 lines (simple) to 1,000+ lines (complex)

2. **architect** - System designer
   - Creates: Architecture docs, technology decisions, file manifests
   - Scales: 150 lines (simple) to 1,000+ lines (complex)

3. **code-writer** - TDD enforcer
   - Implements: With strict TDD (RED-GREEN-REFACTOR)
   - Enforces: <500 lines per file, no placeholders, production-ready only

4. **test-generator** - Testing specialist
   - Creates: Comprehensive tests (>80% coverage)
   - Requires: Mandatory user verification (you must run `npm test`)

### 5 Review Agents (Parallel) ⭐⭐⭐⭐⭐

**The ONLY truly autonomous agents:**

5. **security-reviewer** - OWASP Top 10, SQL injection, XSS
6. **quality-reviewer** - Code smells, DRY/SOLID, complexity
7. **performance-analyzer** - O(n²), memory leaks, N+1 queries
8. **ux-reviewer** - Error messages, loading states, UX friction
9. **accessibility-reviewer** - WCAG 2.1 AA, keyboard, screen readers

**Status:** Proven effective (found 38 real issues in validation)

---

## TRUE Progressive Disclosure

**The Innovation (from cc10x_V2-main):**

```
Old v2 (monolithic):
→ Orchestrator SKILL.md: 1,325 lines
→ ALL loaded when skill triggers
→ ~13,000 tokens always

New v3 (progressive):
→ Core SKILL.md: 150 lines (~1,500 tokens)
→ Workflow file: 300-600 lines (~3,000-6,000 tokens) - loaded on-demand
→ Total: 4,500-7,500 tokens (only what's needed)

Savings: 50-75%!
```

**How it works:**
- You: `/cc10x review code`
- Loads: Core (150 lines) + review workflow (400 lines) = 550 lines total
- Doesn't load: plan, build, debug, validate workflows (not needed!)
- **Token efficient!**

---

## Quick Default Plans (Phase 0a)

**The Problem v3 Fixes:**

```
v2 behavior:
→ User: "Plan authentication"
→ cc10x: Generates 12 questions, never asks them
→ Proceeds with assumptions
→ 120k tokens later...
→ User: "Wait, I wanted OAuth!"
→ 120k tokens wasted on wrong assumptions
```

**v3 solution:**

```
v3 behavior:
→ User: "/cc10x plan authentication"
→ cc10x: Quick complexity check (5/5 - complex)
→ Phase 0a: Quick default plan (3-5k tokens)
  Shows assumptions:
  - OAuth: NO (defer to v2)
  - Tokens: 15min access, 7-day refresh
  - Storage: httpOnly cookies
  - Email verification: NO
  
  OPTIONS:
  (a) Proceed with defaults (fast track, +30k)
  (b) Customize (I'll ask questions, +40k)
  (c) Manual (quick guidance, +2k, STOP)

→ User validates BEFORE cc10x wastes 120k!

If (a): 35k total (vs 120k)
If (b): 45k with customization
If (c): 7k then stops (huge savings!)
```

**Prevents wasting tokens on wrong direction!**

---

## End-to-End Automation

**One Command, Complete Implementation:**

```bash
/cc10x plan and build authentication
```

**What happens:**
1. PLANNING workflow executes (with Phase 0a defaults)
2. Plan saved to `.claude/plans/`
3. **AUTO-CONTINUES to BUILDING** (no second command!)
4. BUILD workflow implements with TDD
5. Complete, tested implementation delivered

**vs v2:** Had to run `/feature-plan`, then `/feature-build` separately

**Supported:**
- "plan and build" → PLAN + BUILD
- "review and refactor" → REVIEW + BUILD
- "debug and fix" → DEBUG + implementation

**From cc10x_V2-main end-to-end approach.**

---

## Token Economics (Honest Assessment)

### The Reality

**cc10x v3 costs 3-20x MORE tokens than manual.**

| Workflow | Simple (1-2) | Moderate (3) | Complex (4-5) | Worth It? |
|----------|--------------|--------------|---------------|-----------|
| REVIEW | 20k-50k | 20k-50k | 20k-50k | ✅✅ ALWAYS |
| PLANNING | 40k vs 5k manual | 60k vs 10k manual | 60k vs 20k manual | ❌ / ⚠️ / ✅ |
| BUILDING | 80k vs 10k manual | 100k vs 20k manual | 100k vs 40k manual | ❌ / ⚠️ / ✅ |
| DEBUGGING | 25k vs 8k manual | 25k vs 8k manual | 30k vs 10k manual | ⚠️ Maybe |
| VALIDATION | 35k | 35k | 45k | ⚠️ Teams only |

**Simple (1-2):** ❌ Skip cc10x (manual 8-20x cheaper and often better)
**Moderate (3):** ⚠️ Maybe (if team docs valued, otherwise skip)
**Complex (4-5):** ✅ Use cc10x (prevents mistakes >> token cost)

**Exception:** REVIEW always worth it!

---

## When to Use cc10x v3

### ✅ Always Use REVIEW

- Before EVERY PR
- Security audits
- Performance checks
- Any complexity
- **One prevented breach >> all tokens ever used**

### ✅ Use PLANNING for:

- Complexity 4-5 features (500+ lines, 7+ files)
- Novel patterns (not in codebase)
- High-risk domains (auth, payments, data)
- Architecture decisions needed
- Team alignment required

**Examples:**
- Real-time notifications (WebSockets)
- Multi-tenancy (data isolation)
- Payment processing (Stripe integration)
- Complex state management

### ✅ Use BUILDING for:

- Complexity 4-5 (want strict TDD)
- High-risk implementations
- Need systematic quality

**⚠️ Warning:** Requires manual test verification (can report false success)

### ✅ Use DEBUGGING for:

- Complex bugs (root cause unclear)
- Spent >30 min without progress
- Multiple interacting systems
- LOG FIRST saves time

### ❌ Skip cc10x For:

- Simple features (complexity 1-2)
  - Add rate limiting with library
  - Form validation with Zod
  - Simple CRUD operations
  - **Just read library docs! 16-20x cheaper**

- Obvious fixes
  - Typos, syntax errors
  - Missing imports
  - Clear from error message

- Emergencies
  - Production down
  - Fix now, document later

- Prototypes/MVPs
  - Iterate fast first
  - Systematize later

**v3 will honestly tell you to skip if manual is better!**

---

## Quality Enforcement

### PostToolUse Hook (Automatic)

**After EVERY Write/Edit:**
- ✅ File size validated
- ✅ Warning if >500 lines
- ✅ Split suggestions provided

**Example:**
```
⚠️ WARNING: src/auth/service.ts exceeds 500 lines (652 lines)

USER RULE VIOLATION: Files must be < 500 lines!

Split immediately:
  - Components: <200 lines
  - Utilities: <300 lines
  - Services: <400 lines

Example:
  auth/service.ts (652 lines)
    ↓ Split into:
  auth/core.ts (350 lines)
  auth/validation.ts (200 lines)
  auth/utils.ts (102 lines)
```

**From cc10x_V2-main hooks - actually enforces, not just recommends!**

### code-writer Enforcement

- ✅ No placeholders or TODOs (rejects "implement this later")
- ✅ Production-ready only
- ✅ Comprehensive error handling (all failure paths)
- ✅ Input validation (all functions)
- ✅ TypeScript for JavaScript
- ✅ DRY and SOLID principles

### test-generator Requirements

- ✅ >80% coverage target
- ✅ Meaningful tests (not just coverage numbers)
- ✅ Unit + integration + e2e (based on complexity)
- ✅ **MANDATORY user verification** (prevents false reports)

---

## Best Practices

### 1. Always Start with /cc10x review

```bash
/cc10x review src/
```

This is the ONLY universally valuable workflow. Use before every PR.

---

### 2. Check Complexity Before Planning

**Quick mental check:**
- Files: <3 = simple (skip cc10x)
- Files: 7+ = complex (use cc10x)
- Library or novel? Library = simple
- Auth/payment? = Complex (high-risk overrides)

**If complexity <=2:** Manual is 16-20x cheaper!

---

### 3. Use End-to-End for Complex

```bash
/cc10x plan and build real-time notifications
```

One command, complete implementation!

---

### 4. Always Verify Tests Manually

**Never trust "tests passing" reports!**

```bash
npm test
echo $?  # Must be 0
```

See results with YOUR EYES before proceeding.

---

### 5. Trust the Complexity Assessment

When orchestrator says:
- "This is SIMPLE (2/5), manual is 16x cheaper" → **Listen!**
- "This is COMPLEX (5/5), systematic planning prevents disasters" → **Proceed!**

**Don't force cc10x on simple features.**

---

## Comparison

### cc10x v3 vs v2

**Simpler:**
- 9 agents vs 11 (4+5 clear architecture)
- 150-line core vs 1,325-line monolith

**More Efficient:**
- 50-75% token savings (progressive workflows)
- 65-95% waste prevention (Phase 0a)

**More Honest:**
- Recommends skip for simple features
- Shows real token economics
- Requires manual verification

**More Powerful:**
- End-to-end automation
- PostToolUse hook enforcement
- Quick default validation

**Inspired by:**
- cc10x_V2-main (simplicity, progressive disclosure)
- cc10x v2 (5-star review, risk analysis)

---

## Common Questions

### Q: Why costs MORE tokens if it has progressive loading?

**A:** Progressive loading (v3) saves 50-75% vs monolithic (v2), but BOTH cost more than manual because systematic analysis has overhead.

- Manual: 5-50k tokens (ad-hoc implementation)
- v2 monolithic: 80-180k tokens (loaded everything)
- v3 progressive: 30-100k tokens (loads only needed workflows)

**v3 is more efficient than v2, but both cost more than manual.**

### Q: When should I actually use cc10x?

**A:** 
- REVIEW: Always (before every PR)
- PLANNING: Complexity 4-5 only
- BUILDING: Complexity 4-5, want TDD
- DEBUGGING: Complex bugs
- VALIDATION: Team projects

**Skip for simple features!**

### Q: What if I'm not sure about complexity?

**A:** Run `/cc10x plan [feature]` - it will assess complexity and recommend:
- "Skip cc10x, manual is 16x cheaper" (complexity 1-2)
- "Show tradeoffs, your call" (complexity 3)
- "Proceeding, cc10x valuable" (complexity 4-5)

**Trust the assessment!**

### Q: Can I force cc10x for simple features?

**A:** Yes, but orchestrator will warn:
```
⚠️ This is SIMPLE (2/5). Manual is 16x cheaper.

Real test showed cc10x WORSE for simple features.

Proceed anyway? (costs 80k tokens for 5k-value feature)
```

If you confirm, it will proceed (but not recommended!).

### Q: How do I know if tests actually pass?

**A:** You MUST run tests yourself:
```bash
npm test
echo $?  # Verify = 0
```

v2 testing showed false reports. v3 requires your eyes on results.

---

## File Limits

**USER RULE (enforced by PostToolUse hook):**

- Components: <200 lines
- Utilities: <300 lines
- Services: <400 lines
- Config: <100 lines
- **Maximum: 500 lines (hard limit)**

**Hook validates after EVERY file write.**

---

## Support

- **Quick Start:** [QUICK-START.md](../../QUICK-START.md)
- **Technical Details:** [README.md](../../README.md)
- **Changelog:** [CHANGELOG.md](../../CHANGELOG.md)
- **Issues:** https://github.com/romiluz13/cc10x/issues

---

## Remember

**cc10x v3 = The Perfect Fusion**

**Best of:**
- cc10x_V2-main (simplicity, efficiency, enforcement)
- cc10x v2 (5-star review, risk analysis, honesty)

**Result:**
- Simpler (4+5 vs 11 agents)
- More efficient (50-75% progressive savings)
- More honest (recommends skip for simple)
- More powerful (end-to-end automation)
- More reliable (mandatory verification)

**Philosophy:**
Use the right tool for the job.
- Simple? Go manual (16-20x cheaper).
- Complex? Use cc10x (prevents costly mistakes).
- Review? ALWAYS use (prevents disasters).

**Start with `/cc10x review` - the killer feature!**
