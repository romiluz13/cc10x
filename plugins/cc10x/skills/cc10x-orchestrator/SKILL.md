---
name: cc10x-orchestrator
description: Master orchestration skill for systematic development workflows combining cc10x_V2-main simplicity with proven v2 patterns. Detects task type from user messages (review, plan, build, debug, validate), assesses complexity (1-5 scoring), chooses appropriate workflow, delegates to specialized sub-agents (feature-planner, architect, code-writer, test-generator), coordinates systematic execution. Use for systematic code review (5-star parallel AI agents finding security, quality, performance, UX, accessibility issues), comprehensive feature planning (complexity 4-5 with architecture decisions, file manifests, rollback strategies), TDD-enforced implementation (with risk analysis before increments), LOG FIRST debugging (systematic over guessing), or cross-artifact validation. Particularly valuable for complex features (4-5 complexity: 500+ lines, 7+ files, novel patterns, architecture decisions). Recommends manual for simple features (1-2 complexity: saves 16-20x tokens). Integrates 7-dimension What Could Go Wrong methodology at critical phases. Workflows load progressively (50-75% token savings vs monolithic). End-to-end automation support (plan and build in one flow). Honest positioning: costs 3-20x MORE tokens than manual due to systematic analysis overhead, use for complexity 4-5 where preventing architecture mistakes justifies cost. Review workflow always worth it (prevents security breaches). Follows official Anthropic patterns and cc10x_V2-main progressive disclosure.
license: MIT
allowed-tools: Read, Write, Grep, Glob
---

# cc10x v3 Master Orchestrator

I am the ONE skill that orchestrates all cc10x systematic development workflows using TRUE progressive disclosure.

## How I Work: 3-Step Process

### Step 1: Analyze Your Message

I detect **task type** and **complexity**:

**Task Types:**
- **REVIEW** - "review", "audit", "check", "analyze", "find issues", "security scan"
- **PLAN** - "plan", "design", "architecture", "create plan", "PRD"
- **BUILD** - "implement", "build", "create feature", "add", "develop"
- **DEBUG** - "debug", "fix bug", "not working", "error", "investigate"
- **VALIDATE** - "validate", "verify", "check consistency", "does code match plan"

**Complexity Quick Assessment (1-5 scale):**
- Files affected? (1-3 = simple, 4-6 = moderate, 7+ = complex)
- Novel pattern or library? (novel = complex, library = simple)
- High-risk domain? (auth/payment/data = complex)

### Step 2: Make Decision (with Multi-Workflow Detection)

**Detect combined workflows** (end-to-end automation):

```
DETECT PATTERNS:
- "Plan and build" → PLAN + BUILD workflows
- "Review and refactor" → REVIEW + BUILD (refactoring context)
- "Debug and fix" → DEBUG + implementation
- "Plan, build, and review" → PLAN + BUILD + REVIEW
```

**Single workflow execution:**

```
IF task = REVIEW:
  → Always proceed (5-star feature, always worth it)
  → Load workflows/review.md
  → Execute review
  
IF task = PLAN:
  → Check complexity
  → IF complexity <= 2: Recommend manual, show token economics
  → IF complexity >= 4: Load workflows/plan.md
  → IF complexity = 3: Show tradeoffs, ask user
  → Execute planning
  
IF task = BUILD:
  → Check if plan exists
  → IF plan exists: Load workflows/build.md
  → IF no plan: Recommend create plan first (or offer quick planning)
  → Execute building
  
IF task = DEBUG:
  → Assess complexity
  → Simple bug? Recommend just fixing it
  → Complex bug? Load workflows/debug.md (LOG FIRST pattern)
  → Execute debugging
  
IF task = VALIDATE:
  → Check if plan exists in .claude/plans/
  → Plan exists? Load workflows/validate.md
  → No plan? Recommend create plan first
  → Execute validation
```

**Combined workflow execution:**

```
IF task = PLAN + BUILD:
  1. Execute PLANNING workflow (workflows/plan.md)
  2. Wait for Phase 0a user decision (proceed/customize/manual)
  3. IF proceed or customize: Complete planning
  4. Save plan to .claude/plans/FEATURE_[NAME].md
  5. AUTO-CONTINUE to BUILDING:
     - Load workflows/build.md
     - Load saved plan
     - Execute all phases
     - Deliver complete implementation
  
IF task = REVIEW + REFACTOR:
  1. Execute REVIEW workflow (workflows/review.md)
  2. IF issues found requiring code changes:
     - Load workflows/build.md with refactoring context
     - Implement fixes with TDD
     - Deliver improved code
  
IF task = DEBUG + FIX:
  1. Execute DEBUG workflow (workflows/debug.md)
  2. Identify root cause
  3. Implement fix with TDD
  4. Add regression test
  5. Deliver fix
```

### Step 3: Load Workflow & Execute

I load the appropriate workflow file from `workflows/` directory, which contains detailed execution instructions for that specific workflow.

**This is TRUE progressive disclosure:**
- Level 1: This SKILL.md (always loaded, ~150 lines, ~1,500 tokens)
- Level 2: Specific workflow file (loaded on-demand, 300-600 lines, ~3,000-6,000 tokens)
- **Total: 4,500-7,500 tokens vs old 13,000 tokens (50-75% savings!)**

---

## Workflow Files (Load Progressively)

### workflows/review.md (~400 lines)
**When:** Always valuable, prevents security breaches
**What:** 5 parallel AI agents (security, quality, performance, UX, accessibility)
**Token cost:** 20k-50k (worth it - found 38 issues in testing including 5 CRITICAL)

### workflows/plan.md (~600 lines)
**When:** Complexity 4-5 features needing architecture decisions
**What:** 7-phase planning (requirements → architecture → risk → complexity → testing → manifest → rollback/deployment)
**Token cost:** 30k-60k vs 15k manual (2-4x more, prevents architecture mistakes)

### workflows/build.md (~500 lines)
**When:** Want strict TDD enforcement, systematic implementation
**What:** Context analysis → Task breakdown → TDD cycles (risk analysis before each) → Test generation → Mandatory verification
**Token cost:** 40k-80k vs 20k manual (2-4x more, systematic quality)

### workflows/debug.md (~300 lines)
**When:** Complex bugs, root cause unclear
**What:** LOG FIRST pattern (logging → observation → hypothesis → minimal fix → cleanup)
**Token cost:** 15k-30k vs 5k manual (3-6x more, saves hours of guessing)

### workflows/validate.md (~200 lines)
**When:** Pre-PR checks, verify plan matches code
**What:** Cross-artifact validation (plan → code → tests → docs consistency)
**Token cost:** 20k-45k (team accountability, prevents drift)

---

## Error Handling

### If Workflow File Loading Fails

**Symptom:** Workflow file not found or loading error

**Actions:**
1. Check if workflow file exists in `workflows/` directory
2. If missing: Report error, suggest using /cc10x command
3. If present but failed: Retry once
4. If second failure: Fall back to basic execution without workflow
5. Report to user: "Workflow loading failed, providing manual guidance instead"

**Example:**
```
Attempted to load: workflows/plan.md
Error: File not found

Fallback: I'll provide manual planning guidance based on your request.
Quality may be lower without systematic workflow.
```

### If Agent Invocation Fails

**Symptom:** Agent doesn't respond or returns error

**Actions:**
1. Retry once (may be transient issue)
2. If second failure: Report to user with error details
3. Suggest fallback: "I can provide manual guidance instead of using the [agent-name] agent"
4. Continue with reduced workflow (skip failed agent phase)

**Example:**
```
Attempted to invoke: feature-planner agent
Error: Agent timeout after 60 seconds

Retrying... (attempt 2/2)
Error: Agent still unavailable

Fallback: Proceeding without formal PRD generation.
I'll create basic requirements analysis manually.
```

### If Skill Loading Fails

**Symptom:** Domain skill file not found

**Actions:**
1. Report which skill failed to load
2. Continue workflow without that specific skill content
3. Use general knowledge instead of specialized patterns
4. Note in output: "Proceeded without [skill-name] skill"

---

## Quick Reference

### When to Use Each Workflow

**REVIEW (always worth it):**
- Before every PR
- Any complexity level
- Prevents security breaches = infinite ROI

**PLAN (complexity 4-5):**
- 500+ lines of code
- 7+ files affected
- Novel patterns or architecture decisions
- High-risk domains (auth, payments, data)

**BUILD (complexity 4-5):**
- Want strict TDD enforcement
- Need systematic implementation
- Complexity justifies structure

**DEBUG (complex bugs):**
- Root cause unclear
- Spent >30 min guessing
- LOG FIRST pattern will save time

**VALIDATE (team projects):**
- Pre-PR validation
- Ensure plan matches code
- Periodic consistency checks

### When to Skip cc10x

**Skip for:**
- Simple features (1-2 complexity: <200 lines, using libraries)
- Obvious fixes (<5 lines, clear cause)
- Emergencies (production down - fix first, document later)
- Prototypes/MVPs (iterate fast first)

**Why skip?** Manual is 16-20x cheaper in tokens for simple tasks.

---

## End-to-End Automation

### Combined Workflows

**"Plan and build [feature]":**
1. Load workflows/plan.md → Full planning
2. Save plan to `.claude/plans/FEATURE_[NAME].md`
3. **Auto-continue:** Load workflows/build.md → Implementation
4. Deliver complete, tested implementation

**"Review and refactor [code]":**
1. Load workflows/review.md → Find issues
2. If refactoring needed: Load workflows/build.md with refactoring context
3. Deliver improved code

**"Debug and fix [issue]":**
1. Load workflows/debug.md → Identify root cause
2. If fix needed: Implement with TDD
3. Deliver fix with tests

---

## Reality Check

**I cost 3-20x MORE tokens than manual implementation.**

**Why?**
- Systematic multi-phase analysis
- Risk assessments
- Comprehensive documentation
- Quality enforcement

**Worth it when:**
- Complexity 4-5 (one prevented architecture mistake pays for planning)
- Security-sensitive (one breach prevented = infinite value)
- Team collaboration (documentation enables alignment)

**NOT worth it when:**
- Complexity 1-2 (just follow library docs)
- Simple fixes (just fix it)
- Time-sensitive (manual is faster)

**Exception:** REVIEW always worth it (prevents disasters)

---

## Remember

I orchestrate workflows by loading them progressively. Each workflow file contains detailed execution instructions optimized for that specific task type.

**The value is in:**
- Systematic thinking (prevents mistakes)
- Progressive disclosure (token-efficient)
- Proven patterns (cc10x_V2-main + v2 fusion)
- Honest positioning (use for right complexity)

**To invoke me:**
- Natural language: "Review this code for security"
- Slash command: `/cc10x review this code for security` (guaranteed loading)

**I'll detect your intent, assess complexity, recommend the right approach, and load only what's needed.**
