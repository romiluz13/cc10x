# CC10x Quick Start

Get started with CC10x in 5 minutes and experience intelligent AI orchestration.

## Installation

```bash
# Copy plugin to your Claude Code plugins directory
cp -r plugins/cc10x ~/.claude-code/plugins/

# Reload Claude Code
```

Verify installation:
```bash
/cc10x review --help
```

## Your First Success (2 Minutes)

### Try the Killer Feature

```bash
/cc10x review src/your-code.js
```

**What happens:**
1. Orchestrator detects "review" intent
2. Loads review workflow (progressive, efficient)
3. 5 agents analyze in parallel (2-3 minutes):
   - Security → SQL injection, XSS, secrets
   - Quality → Code smells, complexity
   - Performance → O(n²), memory leaks
   - UX → Error messages, loading states
   - Accessibility → WCAG violations

**Result:** Comprehensive findings with severity ratings

## Your First Feature (15 Minutes)

Let's build a complete feature with intelligent orchestration.

### Step 1: Plan (5 minutes)

```bash
/cc10x plan "Add user settings page with theme toggle"
```

**Orchestrator does:**
1. **Assesses complexity** (1-5 scoring)
2. **Checks if cc10x worth it** (warns if manual is better)
3. **Loads planning workflow** (progressive loading)
4. **Quick defaults** (validates assumptions before waste)
5. **7-dimension risk analysis** ("What Could Go Wrong")
6. **Creates PLAN.md** with phases and verification split

**Review the plan** - Make adjustments if needed.

### Step 2: Build (10 minutes)

```bash
/cc10x build from plan user-settings

# Or end-to-end (plan + build in one command):
/cc10x plan and build user settings
```

**Orchestrator does:**
1. **Complexity gate** (confirms plan complexity assessment)
2. **TDD cycles** (RED → GREEN → REFACTOR)
3. **Risk analysis** ("What Could Go Wrong" at each step)
4. **Automated checks**:
   ```
   ✅ Tests: 15/15 passing
   ✅ Type check: Clean
   ✅ Lint: Clean
   ✅ Build: Success
   ```
5. **⏸️ PAUSES** - "Please verify feature works in UI"
6. **You test and confirm**: "Looks good!"
7. **Builder continues to next phase**

### Step 3: Review (3 minutes)

```bash
/cc10x review src/settings/
```

**Orchestrator routes to 5 parallel reviewers:**
- Security: ⚠️ HIGH - Missing CSRF protection
- Quality: ✅ Clean, well-structured
- Performance: ✅ No issues
- UX: ⚠️ LOW - Loading state not shown during save
- Accessibility: 🔴 HIGH - Theme toggle missing aria-label

**Fix issues** and re-review until clean.

## How the Orchestrator Works

### Intelligent Intent Detection

```bash
# You say:
/cc10x review this code for security

# Orchestrator:
1. Detects intent: REVIEW
2. Loads: review.md workflow (4k tokens)
3. Activates: 5 review agents (parallel)
4. Loads skills: security-patterns (as needed)
5. Returns: Findings with severity ratings
```

### Progressive Loading Example

**Old (monolithic):**
- Always loads: 13k tokens
- Even if you just wanted review!

**New (orchestrated):**
- Core: 3.5k tokens (always)
- + Review workflow: 4k tokens (on-demand)
- + Review agents: 7.5k tokens (parallel)
- **Total: 15k instead of 30k+ (50% savings!)**

### Complexity Gate Example

```bash
# You: /cc10x plan rate limiting

# Orchestrator assesses:
Complexity: 2/5 (SIMPLE - just use express-rate-limit library)

# Orchestrator warns:
⚠️ STOP: This is SIMPLE (2/5)

Token Economics:
- Manual: 5k tokens, 30 min (read library docs)
- cc10x: 80k tokens, similar time, needs verification
- Multiplier: 16x MORE tokens

Recommendation: Implement manually. Use cc10x for review only.

Continue anyway? (yes/no)

# You: no

# Orchestrator: Exiting. Good call! 😊
```

## Common Commands

### Review (Use Before EVERY PR!)

```bash
/cc10x review src/auth.js
/cc10x audit src/features/payment/
/cc10x review this code for security issues
```

**Always worth it - prevents disasters!**

### Planning (Complexity 4-5)

```bash
/cc10x plan authentication with JWT
/cc10x plan real-time notifications
/cc10x design payment processing system
```

**Orchestrator checks complexity first!**

### Building (Complexity 4-5)

```bash
/cc10x build from plan authentication
/cc10x implement user registration
/cc10x plan and build real-time chat
```

**Orchestrator enforces TDD with pause points.**

### Debugging (Complex Bugs)

```bash
/cc10x debug login timeout issue
/cc10x fix rate limiting not working
/cc10x debug this error
```

**Orchestrator applies LOG FIRST methodology.**

## Understanding Orchestration

### The Focus Rule

Orchestrator **ONLY** does what you request:

```bash
# You ask: "review this code"
# Orchestrator: ONLY reviews (doesn't plan or build)

# You ask: "plan and build authentication"
# Orchestrator: Plans THEN builds (explicitly requested)
```

**After completion:**
- Orchestrator delivers results
- OFFERS: "Want me to review it?"
- YOU decide next step (no auto-chaining)

### Progressive Skill Loading

```bash
# You: /cc10x review src/auth.js

# Orchestrator loads:
✅ Core (3.5k tokens)
✅ review.md workflow (4k tokens)
✅ 5 review agents (parallel)
✅ security-patterns skill (as needed)
✅ performance-patterns skill (as needed)

# Orchestrator DOESN'T load:
❌ plan.md workflow (not needed)
❌ build.md workflow (not needed)
❌ debug.md workflow (not needed)
❌ Execution agents (not needed)
❌ TDD skills (not needed)

Result: 50-75% token savings!
```

## Complexity Guide

### Simple (1-2) - Skip cc10x

**Examples:**
- Rate limiting (use express-rate-limit)
- Form validation (use Zod)
- CSV export
- Config changes

**Orchestrator says:**
```
⚠️ This is SIMPLE (2/5)
Manual is 16x cheaper.
Recommendation: Skip cc10x.
```

### Moderate (3) - Maybe

**Examples:**
- User registration
- Pagination with caching
- Search filters

**Orchestrator says:**
```
⚠️ MODERATE (3/5)
Manual cheaper but team docs may be valuable.
Your call.
```

### Complex (4-5) - Use cc10x

**Examples:**
- Authentication system
- Payment processing
- Real-time chat
- Multi-tenancy
- RBAC

**Orchestrator says:**
```
✅ COMPLEX (5/5)
Systematic planning prevents architecture mistakes.
Proceeding...
```

**Exception:** REVIEW always worth it (any complexity)!

## Tips for Success

### 1. Trust the Complexity Gate

When orchestrator warns "manual is 16x cheaper" → **Listen!**

Simple features don't need systematic orchestration.

### 2. Actually Test at Pause Points

When builder pauses for manual verification:
- Open the app
- Test the feature
- Check edge cases
- Confirm or report issues

**Don't just say "continue" without testing!**

### 3. Review Early and Often

Don't wait until everything is done. Run `/cc10x review` after each major component.

### 4. Use Natural Language

Orchestrator detects intent from natural language:

```bash
/cc10x review this for security
/cc10x plan auth feature
/cc10x build user settings
/cc10x debug login bug
```

All work! Orchestrator routes intelligently.

### 5. Read the Full User Guide

The orchestrator auto-loads `CLAUDE.md` - a 767-line comprehensive guide with:
- All 5 workflows explained
- 12 agent details
- 21 skill descriptions
- Real-world examples
- Token economics
- Best practices

## The Workflow Pattern

Every complex feature follows this orchestrated pattern:

```
/cc10x plan [feature]
      ↓
Orchestrator assesses complexity
      ↓
(If complex) Creates PLAN.md with risk analysis
      ↓
/cc10x build from plan [feature]
      ↓
Orchestrator implements with TDD + pause points
      ↓
/cc10x review [files]
      ↓
Orchestrator routes to 5 parallel reviewers
      ↓
Fix issues → Production!
```

## Common Scenarios

### Security Audit

```bash
/cc10x review src/auth/ src/api/
```

Orchestrator activates security-reviewer with security-patterns skill.

### Performance Optimization

```bash
/cc10x review this code for performance
```

Orchestrator detects "performance" intent, activates performance-analyzer.

### Bug Fixing

```bash
/cc10x debug "Login button not working on mobile Safari"
```

Orchestrator applies LOG FIRST:
1. Add strategic logging
2. Reproduce bug
3. Analyze patterns
4. Find root cause
5. Minimal fix
6. Regression test

### Quick Feature

```bash
/cc10x plan and build user profile page
```

Orchestrator does end-to-end:
1. Assesses complexity
2. Creates plan (if complex) or warns (if simple)
3. Implements with TDD
4. Delivers complete feature

## What Makes CC10x Different

### 🎯 Intelligent Orchestration

Not just delegation - **smart routing** based on:
- Your intent (detected from natural language)
- Complexity assessment (1-5 scoring)
- "What Could Go Wrong" analysis
- Progressive loading strategy

### 💰 Honest Economics

Orchestrator **honestly** tells you:
- When manual is better (16-20x cheaper)
- When cc10x worth it (prevents architecture mistakes)
- Real token costs (3-20x MORE than manual)
- Why it's worth it (or not)

### 🎛️ Progressive Efficiency

- **Old:** 13k tokens always loaded
- **New:** 3.5k core + workflow on-demand
- **Savings:** 50-75% vs monolithic!

### 🛡️ Quality Enforcement

- PostToolUse hooks (automatic file size checks)
- No placeholders or TODOs
- Mandatory test verification
- Comprehensive error handling
- >80% coverage target

## Need More Help?

- **Full Guide**: `CLAUDE.md` (auto-loaded, 767 lines)
- **README**: `README.md` (comprehensive docs)
- **Orchestrator Details**: `skills/cc10x-orchestrator/SKILL.md`

## Remember

**Start Simple:**
```bash
/cc10x review src/
```

This is the ONLY universally valuable workflow.

**Trust the Orchestrator:**
- It detects intent intelligently
- It assesses complexity honestly
- It loads progressively efficiently
- It prevents waste automatically

**Use the Right Tool:**
- Simple (1-2)? Go manual (16-20x cheaper)
- Complex (4-5)? Use cc10x (prevents mistakes)
- Review? ALWAYS use (prevents disasters)

---

**Ready? Start with `/cc10x review` and experience intelligent orchestration!** 🚀

