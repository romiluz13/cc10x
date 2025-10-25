# cc10x v3 Quick Start Guide

## Installation

### Method 1: From GitHub (Recommended)

In Claude Code, run:
```bash
# Add the marketplace
/plugin marketplace add romiluz13/cc10x

# Install the plugin
/plugin install cc10x@cc10x
```

### Method 2: Local Testing

```bash
# Add local marketplace
/plugin marketplace add /Users/rom.iluz/Dev/cc10x_v2

# Install plugin
/plugin install cc10x@cc10x
```

## Verify Installation

```bash
# Check plugin installed
/plugin

# Expected output: cc10x listed

# Check sub-agents available
/agents

# Expected: 9 agents listed
# - feature-planner
# - architect
# - code-writer
# - test-generator
# - security-reviewer
# - quality-reviewer
# - performance-analyzer
# - ux-reviewer
# - accessibility-reviewer
```

## First Use: The Killer Feature

### Test the REVIEW Workflow (5-Star, Always Worth It!)

Just describe what you want:

```
/cc10x review src/auth.js
```

**The orchestrator will automatically:**
1. Launch 5 specialized review agents in parallel
2. Analyze from 5 dimensions (security, quality, performance, UX, accessibility)
3. Find real issues (testing found 38 including 5 CRITICAL)
4. Report findings with specific fixes

**Use before EVERY PR!**

---

## Understanding cc10x v3

### The 4+5 Architecture

**4 Core Execution Agents** (sequential workflows):
- `feature-planner` → Creates comprehensive PRDs
- `architect` → Designs systems, assesses complexity
- `code-writer` → TDD implementation (<500 lines enforced)
- `test-generator` → Comprehensive tests (>80% coverage)

**5 Review Agents** (parallel analysis):
- `security-reviewer` → Finds vulnerabilities
- `quality-reviewer` → Finds code smells
- `performance-analyzer` → Finds bottlenecks
- `ux-reviewer` → Finds UX issues
- `accessibility-reviewer` → Finds WCAG violations

### TRUE Progressive Disclosure

**What this means:**
- Master orchestrator: 150 lines (always loaded)
- Workflow files: 300-600 lines (loaded only when needed)
- **Token savings: 50-75% vs monolithic approach**

**Example:**
```
User: "/cc10x review code"
→ Loads: Orchestrator (150 lines) + review workflow (400 lines)
→ Total: 550 lines (~5.5k tokens)

vs old v2:
→ Loaded: Everything (1,325 lines, ~13k tokens)

Savings: 58%!
```

---

## Example Usage Patterns

### 1. Code Review (Always Valuable)

```
/cc10x review src/auth.js
```

**What happens:**
- 5 agents execute in parallel (2-3 minutes)
- Find real issues across 5 dimensions
- Report with specific line numbers and fixes

**Cost:** 20k-50k tokens
**ROI:** One prevented security breach = infinite value

---

### 2. Simple Feature (Get Honest Recommendation)

```
/cc10x plan add todo list
```

**What happens:**
1. Quick complexity assessment (likely 2/5)
2. Recommends: "Skip cc10x, implement manually (16x cheaper)"
3. Shows token economics comparison
4. Offers quick guidance if you choose manual

**Saves you from wasting 80k tokens on a simple feature!**

---

### 3. Complex Feature with Quick Defaults

```
/cc10x plan authentication with JWT
```

**What happens:**
1. Complexity 5/5 detected
2. **Phase 0a: Quick default plan** (3-5k tokens)
   - Shows intelligent defaults (15min tokens, httpOnly cookies, etc.)
   - Presents 3 options: proceed / customize / manual
3. **If proceed:** Full 7-phase planning (30k tokens)
4. **Result:** Comprehensive plan in .claude/plans/

**Avoids 120k waste if assumptions wrong!**

---

### 4. End-to-End Automation

```
/cc10x plan and build authentication
```

**What happens:**
1. Full planning workflow (30-40k tokens)
2. **Auto-continues to building** (no second command needed!)
3. TDD implementation with risk analysis
4. Test generation with mandatory verification
5. **Result:** Complete, tested, production-ready code

**One command, end-to-end!**

---

### 5. Bug Fixing with LOG FIRST

```
/cc10x debug rate limiting not working
```

**What happens:**
1. Adds strategic logging
2. Reproduces bug, observes logs
3. Identifies root cause from actual data
4. Implements minimal fix
5. Adds regression test

**Saves hours of guessing!**

---

## What Makes cc10x v3 Different?

### vs Traditional Claude Code

**Traditional:**
```
User: "Build auth"
↓
Claude: Implements directly
↓
Result: Might be >500 lines, missing tests, has TODOs
```

**cc10x v3:**
```
User: "/cc10x plan and build auth"
↓
Orchestrator: Analyzes (complexity 5/5)
↓
Quick defaults: Shows assumptions, gets approval
↓
feature-planner: Creates PRD (separate context)
↓
architect: Designs system (separate context)
↓
task-breakdown: Generates TODO.md
↓
code-writer: Implements per task (enforces <500 lines)
↓
test-generator: Creates tests (>80% coverage)
↓
Orchestrator: Aggregates & delivers
↓
Result: Complete, tested, documented, production-ready
**All files <500 lines, no placeholders, comprehensive tests**
```

### vs cc10x v2

**v2 Problems:**
- 11 agents (overlapping roles, confusing)
- Monolithic orchestrator (1,325 lines always loaded)
- No quick defaults (wasted 120k tokens on wrong assumptions)
- Separate commands (had to invoke plan, then build)

**v3 Solutions:**
- 4+5 agents (clear roles, cc10x_V2-main inspired)
- Progressive disclosure (150-line core + workflows on-demand)
- Phase 0a quick defaults (present assumptions, get validation)
- End-to-end automation (plan and build in one flow)

---

## Progressive Disclosure in Action

The orchestrator uses Claude's 3-level progressive disclosure:

**Level 1 (Always Loaded - 100 tokens):**
```yaml
name: cc10x-orchestrator
description: [400-word description with all keywords]
```

**Level 2 (Loaded When Triggered - 1,500 tokens):**
- Core SKILL.md (150 lines)
- Task detection, complexity assessment, workflow selection

**Level 3 (Loaded As Needed - 3,000-6,000 tokens):**
- Specific workflow file (review.md, plan.md, build.md, debug.md, validate.md)
- Only the workflow you're using loads!

**Result:** 4,600-7,600 tokens vs old 13,000 tokens = **50-75% savings**

---

## Quality Enforcement

cc10x v3 automatically enforces:

### Via PostToolUse Hook
- ✅ Files <500 lines (hook validates after Write/Edit)
- ✅ Warning appears immediately if >500 lines
- ✅ Suggests how to split (components <200, utilities <300, services <400)

### Via Agent Prompts
- ✅ No placeholders/TODOs (code-writer rejects)
- ✅ Production-ready code only
- ✅ >80% test coverage (test-generator targets)
- ✅ DRY, SOLID principles (code-writer enforces)
- ✅ TypeScript for JS (code-writer enforces)
- ✅ Comprehensive error handling

### Via Mandatory Verification
- ✅ User MUST verify tests pass (prevents false success reports)
- ✅ Exit code checked
- ✅ Actual output captured
- ✅ No trust, only verification

---

## When to Use Each Workflow

### REVIEW: Use Liberally ⭐⭐⭐⭐⭐

**When:** Before EVERY PR, any complexity
**Why:** Finds real bugs, prevents disasters
**Cost:** 20k-50k tokens
**ROI:** One prevented security breach >> all tokens ever used

**Example:**
```
/cc10x review src/
```

---

### PLANNING: Use for Complexity 4-5 ⭐⭐⭐☆☆

**When:** 500+ lines, 7+ files, novel patterns, architecture decisions needed
**Why:** Prevents architecture mistakes, systematic approach
**Cost:** 30k-60k tokens (vs 15k manual)
**ROI:** One prevented architecture mistake >> planning cost

**Skip for:** Simple features (1-2 complexity) - manual is 16x cheaper

**Example:**
```
/cc10x plan real-time notifications with WebSockets
```

---

### BUILDING: Use with Caution ⭐⭐☆☆☆

**When:** Want strict TDD, mandatory verification, complexity 4-5
**Why:** Systematic implementation, prevents edge cases
**Cost:** 40k-80k tokens (vs 20k manual)
**Warning:** MUST verify tests manually (can report false success)

**Skip for:** Time-sensitive, simple implementations

**Example:**
```
/cc10x build from plan authentication
```

Or combined:
```
/cc10x plan and build authentication
```

---

### DEBUGGING: Use for Complex Bugs ⭐⭐⭐☆☆

**When:** Root cause unclear, spent >30 min guessing
**Why:** LOG FIRST pattern saves hours
**Cost:** 15k-30k tokens (vs 5k manual)
**ROI:** Saves 1-3 hours of guessing

**Skip for:** Obvious fixes, emergencies

**Example:**
```
/cc10x debug login timeout issue
```

---

### VALIDATION: Use for Team Projects ⭐⭐⭐☆☆

**When:** Pre-PR checks, team accountability
**Why:** Ensures plan matches code
**Cost:** 20k-45k tokens
**ROI:** Catches drift before it's technical debt

**Skip for:** Solo dev, no plan exists

**Example:**
```
/cc10x validate
```

---

## Complexity Guide

The orchestrator assesses complexity and recommends:

| Score | Name | Files | Lines | Examples | Recommendation |
|-------|------|-------|-------|----------|----------------|
| 1 | TRIVIAL | 1 | <50 | Config change, typo | ❌ Skip (manual 20x cheaper) |
| 2 | SIMPLE | 2-3 | 50-200 | Library integration | ❌ Skip (follow library docs) |
| 3 | MODERATE | 4-6 | 200-500 | Pagination, search | ⚠️ Maybe (if team docs valued) |
| 4 | COMPLEX | 7-15 | 500-1000 | WebSockets, state mgmt | ✅ Use cc10x |
| 5 | VERY COMPLEX | 15+ | >1000 | Multi-tenancy, payments | ✅✅ Use cc10x (essential!) |

**Exception:** REVIEW always worth it (any complexity)

---

## Troubleshooting

### Orchestrator not triggering?

**Solution:** Use slash command:
```bash
/cc10x [your request]
```

Brutal testing showed 0% natural language trigger rate. Slash command guarantees loading.

---

### File size warnings?

**This is CORRECT!** cc10x is enforcing the <500 line rule.

**Solution:** Split the file:
```
large-file.ts (600 lines)
  ↓ Split into:
core.ts (350 lines)
utils.ts (250 lines)
```

PostToolUse hook fires after every Write/Edit.

---

### Tests reported passing but actually failed?

**This happened in v2 testing!** Code-writer said "All tests passing" when 3/7 FAILED.

**Solution:** ALWAYS verify manually:
```bash
npm test
echo $?  # Must be 0
```

v3 requires mandatory user verification. Don't trust reports!

---

### Want to see available workflows?

```bash
# List all skills
ls plugins/cc10x/skills/

# Read a workflow
cat plugins/cc10x/skills/cc10x-orchestrator/workflows/review.md
```

---

## Advanced Usage

### Explicit Workflow Selection

```
/cc10x use REVIEW workflow on src/auth/
/cc10x use PLANNING workflow for authentication
/cc10x use DEBUG workflow for login issue
```

### Customize Complexity Threshold

```
/cc10x plan todo list (complexity 2 but I want systematic approach anyway)
```

Orchestrator will warn about token cost, then proceed if you confirm.

---

### Progressive Loading Example

```
User: "/cc10x plan simple feature"
→ Loads: Orchestrator SKILL.md (150 lines, 1.5k tokens)
→ Detects: PLANNING workflow
→ Loads: workflows/plan.md (600 lines, 6k tokens)
→ Assesses: Complexity 2/5 (SIMPLE)
→ Recommends: Skip cc10x (saves 30k tokens)
→ User chooses: (c) Manual
→ Provides: Quick guidance (2k tokens)
→ Total used: 9.5k tokens vs 40k if proceeded

Savings: 76% by stopping early!
```

---

## Best Practices

### 1. Always Start with /review

```
/cc10x review src/your-changes.js
```

This is the ONLY workflow universally valuable. Use before every PR.

---

### 2. Check Complexity Before Planning

**Quick mental check:**
- Files: <3 = simple, 7-15 = complex
- Library or novel? library = simple
- High-risk domain? (auth/payment) = complex

**If complexity <3:** Skip cc10x, implement manually
**If complexity >=4:** Use cc10x planning

---

### 3. Use End-to-End for Complex Features

```
/cc10x plan and build real-time notifications
```

One command, complete implementation!

---

### 4. Trust the Complexity Assessment

The orchestrator will honestly tell you:
- "This is simple (2/5), manual is 16x cheaper"
- "This is complex (5/5), systematic planning prevents disasters"

**Listen to it!** Don't force cc10x on simple features.

---

## What to Expect

### For REVIEW Workflow
- **Time:** 2-5 minutes
- **Tokens:** 20k-50k
- **Output:** Comprehensive findings with fixes
- **Value:** Always worth it (found 38 issues in testing)

### For PLAN Workflow (Complexity 4-5)
- **Time:** 10-30 minutes
- **Tokens:** 30-60k
- **Output:** 7-phase comprehensive plan
- **Value:** Prevents architecture mistakes

### For BUILD Workflow (Complexity 4-5)
- **Time:** 30-90 minutes
- **Tokens:** 40-80k
- **Output:** Tested, production-ready code
- **Warning:** Verify tests manually!

### For DEBUG Workflow
- **Time:** 10-30 minutes
- **Tokens:** 15-30k
- **Output:** Root cause + fix + regression test
- **Value:** Saves hours of guessing

### For VALIDATE Workflow
- **Time:** 5-15 minutes
- **Tokens:** 20-45k
- **Output:** Consistency report
- **Value:** Team accountability

---

## Success Metrics

You'll know cc10x v3 is working when:

✅ You describe a task naturally
✅ Orchestrator detects type and complexity
✅ Recommends skip for simple features (honest!)
✅ Quick defaults presented (avoid 120k waste)
✅ Workflows load progressively (see token savings)
✅ File size hook enforces <500 lines
✅ Test verification is mandatory (prevents false success)
✅ End-to-end works ("plan and build" in one flow)
✅ Review finds real issues (5-star proven)

---

## Token Economics (Brutal Honesty)

cc10x v3 costs **3-20x MORE tokens than manual** for most workflows.

**Why?**
- Systematic analysis (multiple phases)
- Risk assessments (comprehensive)
- Documentation (comprehensive)
- Quality enforcement (strict)

**Worth it when:**
- Complexity 4-5 (one prevented mistake >> token cost)
- Security-sensitive (one breach >> infinite tokens)
- Team projects (documentation enables alignment)

**NOT worth it when:**
- Complexity 1-2 (manual 16-20x cheaper)
- Solo dev, familiar pattern
- Time-sensitive
- Token budget matters

**Exception:** REVIEW always worth it!

---

## Next Steps

1. **Try REVIEW first:** `/cc10x review src/` (the killer feature!)
2. **Test complexity detection:** `/cc10x plan simple feature` (will recommend skip)
3. **Try complex feature:** `/cc10x plan and build [complex feature]` (end-to-end)
4. **Check progress:** Use progress-tracker skill
5. **Review outputs:** PRDs, architecture docs, code, tests

---

## Getting Help

- **Repository:** https://github.com/romiluz13/cc10x
- **Issues:** https://github.com/romiluz13/cc10x/issues
- **Documentation:** plugins/cc10x/CLAUDE.md (comprehensive user guide)
- **Architecture:** README.md (technical details)

---

## Philosophy

**cc10x v3 = Best of both worlds:**
- cc10x_V2-main's simplicity + progressive disclosure
- cc10x v2's 5-star review + risk analysis

**Result:**
- Simpler (4+5 agents vs 11)
- More efficient (50-75% token savings)
- More honest (recommends skip for simple features)
- More powerful (end-to-end automation)
- More reliable (mandatory verification)

**Built with BMAD methodology principles**
**Powered by Claude Sonnet 4.5**
**Following Anthropic's exact patterns**
**Inspired by cc10x_V2-main architecture**

---

**Ready to go 10x on COMPLEX features? Start with `/cc10x review`!**

