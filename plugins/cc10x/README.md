# CC10x v3.0 - Intelligent AI Development Assistant

**Professional Claude Code plugin with orchestrated workflows, specialized agents, and progressive skills.**

## What is CC10x?

CC10x transforms complex development tasks into systematic, high-quality implementations through intelligent orchestration of specialized AI agents and progressive skill loading.

### Architecture Note: "Agents" vs Claude Code "Subagents"

**cc10x uses instruction-based agents** (NOT Claude Code subagents):

| Feature | cc10x Agents | Claude Code Subagents |
|---------|--------------|----------------------|
| **Context** | Shared (same) | Separate (isolated) |
| **Loading** | Progressive (file references) | Delegation (new instance) |
| **Purpose** | Specialized instructions | Task delegation |
| **Token Cost** | Efficient (shared context) | Expensive (separate contexts) |
| **Coordination** | Can coordinate (see each other) | Cannot coordinate (isolated) |

**Why this approach?**
- Enables coordination between agents (e.g., 5-agent parallel review with shared context)
- More token-efficient for orchestrated workflows
- Allows progressive loading of specialized instructions
- Better for systematic multi-agent analysis

**Trade-off**: No context isolation (all agents see same conversation)

### The Orchestration System

Unlike simple plugins that just delegate tasks, CC10x has an **intelligent orchestrator** that:

✅ **Detects your intent** from natural language ("review this code", "plan authentication")
✅ **Assesses complexity** (1-5 scoring) and recommends the right approach
✅ **Routes to workflows** (review, plan, build, debug) dynamically
✅ **Loads skills progressively** (40-60% token savings)
✅ **Prevents waste** (warns when manual is better)
✅ **Applies "What Could Go Wrong"** methodology at decision points

## Core Features

- **ONE KILLER FEATURE**: 5-agent parallel code review (security, quality, performance, UX, accessibility)
- **12 Specialized Agents**: Each with distinct expertise and clear DO/DON'T boundaries
- **21 Progressive Skills**: Load on-demand for maximum token efficiency
- **Intelligent Orchestration**: Automatically routes to the right workflow based on your intent
- **Complexity Gate**: Honestly recommends manual approach when cc10x would waste tokens
- **Automated Quality**: Hooks enforce <500 line files, mandatory test verification
- **"What Could Go Wrong"**: 7-dimension risk analysis at critical decision points

## Quick Start

```bash
# The killer feature - use before EVERY PR
/cc10x review src/auth.js

# Plan complex features (complexity 4-5)
/cc10x plan real-time notifications with WebSockets

# Build with TDD enforcement
/cc10x build from plan authentication

# Debug with LOG FIRST methodology
/cc10x debug login timeout issue
```

## How the Orchestration Works

### 1. You Invoke with Natural Language

```bash
/cc10x review this code for security issues
/cc10x plan authentication feature
/cc10x build user registration
/cc10x debug rate limiting not working
```

### 2. Orchestrator Analyzes Intent

- **Detects task type**: review / plan / build / debug
- **Assesses complexity**: 1-5 scoring based on files, patterns, risk
- **Applies FOCUS RULE**: Only executes what you explicitly requested

### 3. Complexity Gate (for plan/build)

**If complexity ≤ 2:**
```
⚠️ STOP: This is SIMPLE (2/5)

Token Economics:
- Manual: 5k tokens, 30-60 min
- cc10x: 80k tokens, verification required
- Multiplier: 16x MORE tokens

Recommendation: Implement manually. Use cc10x for review only.
```

**If complexity ≥ 4:**
```
✅ COMPLEX (4/5): Systematic planning prevents architecture mistakes.
Proceeding with comprehensive workflow...
```

### 4. Progressive Workflow Loading

**OLD (monolithic):** 13k tokens always loaded  
**NEW (progressive):** 3.5k core + 3-6k workflow on-demand = 6.5-9.5k total

**Savings:** 50-75% vs monolithic approach!

### 5. Workflow Execution

Orchestrator loads ONE workflow file:
- **review.md** → 5 parallel agents (security, quality, performance, UX, accessibility)
- **plan.md** → Feature planning with 7-dimension risk analysis
- **build.md** → TDD implementation with pause points
- **debug.md** → LOG FIRST systematic investigation

### 6. Context Management

- **Loads only what's needed**: Right agents + right skills for current task
- **"What Could Go Wrong"** at decision points: Proactive risk identification
- **Progressive skill loading**: Agents load domain knowledge as needed

## The 12 Specialized Agents

### Execution Agents (4)
- **feature-planner**: Creates comprehensive PRDs with user stories
- **architect**: Designs system architecture, technology decisions
- **tdd-enforcer**: Implements with strict RED-GREEN-REFACTOR
- **test-generator**: Writes comprehensive tests (>80% coverage)

### Review Agents (5) - Parallel Execution
- **security-reviewer**: OWASP Top 10, SQL injection, XSS, auth bypasses
- **quality-reviewer**: Code smells, DRY/SOLID, complexity metrics
- **performance-analyzer**: O(n²) loops, N+1 queries, memory leaks
- **ux-reviewer**: Error messages, loading states, UX friction
- **accessibility-reviewer**: WCAG 2.1 AA, keyboard nav, screen readers

### Specialist Agents (3)
- **requirements-analyst**: User stories, acceptance criteria
- **context-analyzer**: Codebase patterns, architectural context
- **devops-planner**: Deployment strategies, rollback plans

## The 21 Progressive Skills

**Risk & Planning:**
- risk-analysis (7 dimensions: "What Could Go Wrong")
- task-breakdown
- deployment-patterns

**Code Quality:**
- code-generation (templates & patterns)
- code-reviewing
- safe-refactoring
- verification-before-completion

**Security & Performance:**
- security-patterns (OWASP Top 10)
- performance-patterns (optimization techniques)

**Testing & Debugging:**
- test-driven-development
- systematic-debugging (LOG FIRST)
- bug-fixing

**UX & Accessibility:**
- ux-patterns (Nielsen's heuristics)
- ui-design
- accessibility-patterns (WCAG 2.1)

**Workflows:**
- feature-planning
- feature-building
- codebase-navigation
- progress-tracker

**Orchestration:**
- cc10x-orchestrator (the brain)

## Workflows

### 1. REVIEW ⭐⭐⭐⭐⭐ (Always Worth It!)

**Use:** Before EVERY PR, any complexity

```bash
/cc10x review src/auth.js
/cc10x audit src/features/payment/
```

**What happens:**
1. 5 agents launch in parallel (2-3 minutes)
2. Security finds: SQL injection, XSS, secrets, auth bypasses
3. Quality finds: Code smells, DRY violations, complexity >10
4. Performance finds: O(n²), memory leaks, N+1 queries
5. UX finds: Poor error messages, missing loading states
6. Accessibility finds: WCAG violations, keyboard issues

**Results:** Found 38 real issues in testing (5 CRITICAL, 12 HIGH)

**Verdict:** Worth EVERY token. One prevented breach >> infinite tokens.

### 2. PLANNING ⭐⭐⭐☆☆ (Complexity 4-5)

**Use:** Complex features (500+ lines, 7+ files, architecture decisions)

```bash
/cc10x plan real-time notifications with WebSockets
```

**What happens:**
1. **Complexity check** (1-5 scoring)
2. **Quick defaults** (Phase 0a: validate assumptions before waste)
3. **7-dimension risk analysis** ("What Could Go Wrong")
4. **Comprehensive PRD** (requirements, architecture, file manifest)
5. **Testing strategy** (unit, integration, e2e plans)
6. **Deployment strategy** (rollout, rollback)

**Output:** Complete plan in `.claude/plans/FEATURE_[NAME].md`

### 3. BUILDING ⭐⭐☆☆☆ (Use with Caution)

**Use:** Complexity 4-5, want strict TDD enforcement

```bash
/cc10x build from plan authentication
/cc10x plan and build authentication  # End-to-end
```

**What happens:**
1. **Complexity gate** (warns if manual is better)
2. **TDD cycles** (RED → GREEN → REFACTOR)
3. **Risk analysis** ("What Could Go Wrong" at each increment)
4. **Mandatory verification** (you must confirm tests pass)
5. **Pause points** (manual testing required)
6. **5-agent review** (before finalization)

**⚠️ Warning:** Requires manual test verification (can report false success)

### 4. DEBUGGING ⭐⭐⭐☆☆ (LOG FIRST)

**Use:** Complex bugs, root cause unclear, spent >30 min guessing

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

## Complexity Guide

The orchestrator **honestly** assesses complexity and recommends the right approach:

### Complexity 1-2: SIMPLE
- **Files:** 1-3
- **Lines:** <200
- **Examples:** Rate limiting (library), form validation (Zod), CSV export
- **Recommendation:** ❌ Skip cc10x (manual 16-20x cheaper)

### Complexity 3: MODERATE
- **Files:** 4-6
- **Lines:** 200-500
- **Examples:** User registration, pagination, search filters
- **Recommendation:** ⚠️ Maybe (if team docs valued, otherwise manual)

### Complexity 4-5: COMPLEX
- **Files:** 7-15+
- **Lines:** 500-1,000+
- **Examples:** Auth system, payments, real-time chat, RBAC, multi-tenancy
- **Recommendation:** ✅ Use cc10x (prevents architecture mistakes)

**Exception:** REVIEW always worth it (any complexity)

## Honest Positioning

### Token Economics

**cc10x v3 costs 3-20x MORE tokens than manual.**

| Workflow | Simple (1-2) | Complex (4-5) | Worth It? |
|----------|--------------|---------------|-----------|
| REVIEW | 20k-50k | 20k-50k | ✅✅ ALWAYS |
| PLANNING | 60k vs 5k manual | 60k vs 20k manual | ❌ / ✅ |
| BUILDING | 100k vs 10k manual | 100k vs 40k manual | ❌ / ✅ |
| DEBUGGING | 25k vs 8k manual | 30k vs 10k manual | ⚠️ Maybe |

**Why it costs more:**
- Systematic multi-phase analysis (not ad-hoc)
- Multiple specialized agents (not single perspective)
- Comprehensive risk assessment (7 dimensions)
- Complete documentation (plans, manifests, strategies)

**Worth it when:**
- **Complexity 4-5:** One prevented architecture mistake pays for all planning
- **High-risk domains:** Auth, payments, data integrity
- **Review workflow:** ALWAYS (prevents security breaches = infinite ROI)

**Not worth it when:**
- **Simple features (1-2):** Using libraries, obvious implementations
- **Emergencies:** Production down (fix first, document later)
- **Prototypes:** Iterate fast first, systematize later

**The orchestrator will honestly tell you to skip if manual is better!**

## Quality Enforcement

### PostToolUse Hooks (Automatic)

**After EVERY file write:**
- File size validated (<500 lines)
- Warning if exceeds limit
- Split suggestions provided

### Agent-Level Enforcement

- **No placeholders or TODOs** (rejects "implement this later")
- **Production-ready only** (complete implementations)
- **Comprehensive error handling** (all failure paths)
- **>80% test coverage** (meaningful tests, not just numbers)
- **Mandatory user verification** (prevents false "tests passing" reports)

## Installation

```bash
# Copy plugin to your Claude Code plugins directory
cp -r plugins/cc10x ~/.claude-code/plugins/

# Reload Claude Code
# Plugin auto-loads, orchestrator ready!
```

## When to Use CC10x

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

### ✅ Use BUILDING for:

- Complexity 4-5 (want strict TDD)
- High-risk implementations
- Need systematic quality

### ✅ Use DEBUGGING for:

- Complex bugs (root cause unclear)
- Spent >30 min without progress
- Multiple interacting systems

### ❌ Skip cc10x For:

- Simple features (1-2): Use library docs, 16-20x cheaper
- Obvious fixes: Typos, syntax errors, clear from error message
- Emergencies: Production down, fix now
- Prototypes/MVPs: Iterate fast first, systematize later

## Best Practices

### 1. Always Start with Review

```bash
/cc10x review src/
```

This is the ONLY universally valuable workflow. Use before every PR.

### 2. Trust the Complexity Assessment

When orchestrator says:
- "This is SIMPLE (2/5), manual is 16x cheaper" → **Listen!**
- "This is COMPLEX (5/5), systematic planning prevents disasters" → **Proceed!**

### 3. Use End-to-End for Complex Features

```bash
/cc10x plan and build real-time notifications
```

One command, complete implementation!

### 4. Always Verify Tests Manually

**Never trust "tests passing" reports!**

```bash
npm test
echo $?  # Must be 0
```

See results with YOUR EYES before proceeding.

### 5. Leverage Progressive Loading

The orchestrator loads only what's needed:
- Core (3.5k tokens)
- + Workflow on-demand (3-6k tokens)
- + Skills as needed (progressive)

**Total: 50-75% savings vs monolithic!**

## Architecture

```
User Request
     ↓
CLAUDE.md (Auto-loaded Orchestrator)
     ↓
cc10x-orchestrator Skill (Intelligent Routing)
     ↓
Workflow File (review/plan/build/debug)
     ↓
Specialized Agents (12 total)
     ↓
Domain Skills (21 total, progressive loading)
     ↓
Results with "What Could Go Wrong" Analysis
```

### Progressive Disclosure in Action

**You:** `/cc10x review src/auth.js`

**Orchestrator loads:**
1. Core (3.5k tokens) - always
2. review.md workflow (4k tokens) - on-demand
3. 5 review agents (1.5k tokens each) - parallel
4. Security patterns skill (2k tokens) - as needed

**Doesn't load:**
- plan.md, build.md, debug.md workflows
- Execution agents (planner, architect, tdd-enforcer)
- Testing, UX, deployment skills

**Result:** 15k tokens instead of 30k+ (50% savings!)

## File Limits (Enforced)

**USER RULE:**
- Components: <200 lines
- Utilities: <300 lines
- Services: <400 lines
- **Maximum: 500 lines (hard limit)**

PostToolUse hook validates after EVERY file write.

## Support

- **Quick Start**: See QUICKSTART.md
- **Full User Guide**: CLAUDE.md (auto-loaded)
- **Orchestrator Details**: skills/cc10x-orchestrator/SKILL.md

## License

MIT License - See LICENSE file

---

## Remember

**CC10x v3 = Intelligent Orchestration**

**Key Innovation:**
- **Not just delegation** → Intelligent routing based on intent
- **Not monolithic** → Progressive loading (50-75% token savings)
- **Not optimistic** → Honest about costs, recommends manual when better
- **Not autonomous** → YOU control, orchestrator guides systematically

**Philosophy:**
Use the right tool for the job.
- Simple? Go manual (16-20x cheaper).
- Complex? Use cc10x (prevents costly mistakes).
- Review? ALWAYS use (prevents disasters).

**Start with `/cc10x review` - the killer feature!**

