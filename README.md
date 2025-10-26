# cc10x v3 - The Perfect Fusion

**4+5 Architecture** + TRUE Progressive Disclosure + End-to-End Automation

> The best of cc10x_V2-main (simplicity, efficiency) + cc10x v2 (5-star review, risk analysis)

**Version:** 3.0.0 | **License:** MIT | **Status:** Production-Ready

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://github.com/romiluz13/cc10x)
[![4+5 Architecture](https://img.shields.io/badge/Agents-4%2B5-green)](https://github.com/romiluz13/cc10x)
[![Progressive Loading](https://img.shields.io/badge/Token%20Savings-50--75%25-brightgreen)](https://github.com/romiluz13/cc10x)
[![Version](https://img.shields.io/badge/version-3.0.0-green)](https://github.com/romiluz13/cc10x/releases)

---

## Quick Start

```bash
# Add marketplace
/plugin marketplace add romiluz13/cc10x

# Install cc10x
/plugin install cc10x@cc10x

# Try the killer feature (5-star review)
/cc10x review src/your-code.js
```

**Full guide:** [QUICK-START.md](QUICK-START.md)

---

## What is cc10x v3?

cc10x v3 is a systematic development system for Claude Code that combines:

**From cc10x_V2-main:**
- 4 focused execution agents (no overlap, clear roles)
- TRUE progressive disclosure (50-75% token savings)
- Lightweight orchestrator (150-line core + workflows on-demand)
- Hooks enforcement (PostToolUse validates <500 lines)

**From cc10x v2:**
- 5-star parallel review (security, quality, performance, UX, accessibility)
- 7-dimension risk analysis ("What Could Go Wrong?")
- Deployment patterns (rollback strategies, staged rollouts)
- Honest positioning (3-20x MORE tokens, use for complexity 4-5)

**New in v3:**
- Quick default plans (Phase 0a avoids 120k token waste)
- End-to-end automation (plan and build in one flow)
- ONE workflow scales naturally (simple to complex)
- Mandatory test verification (prevents false success reports)

---

## The 4+5 Architecture

### 4 Core Execution Agents (Sequential)

Based on cc10x_V2-main's proven pattern:

1. **feature-planner** - Product manager creating comprehensive PRDs
   - Scales: 200 lines (simple) to 1,000+ lines (complex)
   - Includes: Risk-aware planning, assumption validation

2. **architect** - System designer with technology decision framework
   - Scales: 150 lines (simple) to 1,000+ lines (complex)
   - Enforces: File size constraints, critical risk analysis

3. **code-writer** - TDD enforcer with strict quality standards
   - Merges: implementer + tdd-enforcer logic
   - Enforces: <500 lines, no placeholders, production-ready only
   - Features: Risk analysis before each increment

4. **test-generator** - Testing specialist targeting >80% coverage
   - Scales: 10-20 tests (simple) to 80-200 tests (complex)
   - Enforces: Mandatory user verification (prevents false reports)

### 5 Review Agents (Parallel) ⭐⭐⭐⭐⭐

**The only "real" autonomous agents** (proven in brutal testing):

5. **security-reviewer** - OWASP Top 10, injection, auth bypasses
6. **quality-reviewer** - Code smells, complexity, DRY/SOLID
7. **performance-analyzer** - O(n²) loops, N+1 queries, caching
8. **ux-reviewer** - Error messages, loading states, UX friction
9. **accessibility-reviewer** - WCAG 2.1 AA, keyboard nav, screen readers

**Capabilities:** Finds critical issues including SQL injection, exposed secrets, auth bypasses

---

## TRUE Progressive Disclosure

### How It Works

**Level 1: Metadata (Always Loaded - 100 tokens)**
```yaml
name: cc10x-orchestrator
description: [comprehensive 400-word description]
```

**Level 2: Core SKILL.md (Loaded When Triggered - 1,500 tokens)**
- Task detection (review/plan/build/debug/validate)
- Complexity assessment (1-5 scoring)
- Workflow selection
- References to workflow files

**Level 3: Workflow File (Loaded On-Demand - 3,000-6,000 tokens)**
- Only the specific workflow you need loads
- review.md (400 lines) OR plan.md (600 lines) OR build.md (500 lines) OR debug.md (300 lines) OR validate.md (200 lines)

**Token Savings:**
- v2 monolithic: 13,000 tokens always loaded
- v3 progressive: 1,500 (core) + 3,000-6,000 (workflow) = 4,500-7,500 tokens
- **Savings: 50-75%!**

### File Structure

```
cc10x-orchestrator/
├── SKILL.md (150 lines - lightweight core)
├── workflows/
│   ├── review.md (400 lines - loaded for review tasks)
│   ├── plan.md (600 lines - loaded for planning)
│   ├── build.md (500 lines - loaded for building)
│   ├── debug.md (300 lines - loaded for debugging)
│   └── validate.md (200 lines - loaded for validation)
└── templates/
    ├── quick-plan.md (200 lines - Phase 0a defaults)
    └── complexity-assessment.md (100 lines - scoring rubric)
```

**Inspired by cc10x_V2-main's progressive structure.**

---

## Quick Default Plans (Phase 0a)

### The Problem (v2)

```
User: "Plan authentication"
↓
Orchestrator generates 12 clarifying questions
↓
Never asks them (just proceeds with assumptions)
↓
120k tokens later...
↓
User: "Wait, I wanted OAuth! Why didn't you ask?"
↓
120k tokens wasted on wrong assumptions
```

### The Solution (v3)

```
User: "/cc10x plan authentication"
↓
Quick complexity: 5/5 (COMPLEX)
↓
Phase 0a: Quick default plan (3-5k tokens)
  - Shows intelligent defaults:
    * OAuth: NO (defer to v2)
    * Token expiry: 15min/7day
    * Storage: httpOnly cookies
    * Email verification: NO
  - Presents 3 options:
    (a) Proceed with defaults (fast track)
    (b) Customize (I'll ask questions)
    (c) Manual (quick guidance)
↓
User validates assumptions BEFORE 120k planning
↓
If (a): +30k for full planning = 35k total
If (b): +40k for questions + refined planning = 45k total
If (c): +2k for guidance, stop = 7k total

Prevents wasting 120k on wrong direction!
```

---

## End-to-End Automation

### Single Invocation, Complete Implementation

```
/cc10x plan and build authentication
```

**What happens:**
1. PLANNING workflow executes (30-40k tokens)
2. Plan saved to `.claude/plans/FEATURE_AUTH.md`
3. **AUTO-CONTINUES to BUILDING** (no second command!)
4. BUILD workflow loads plan and implements
5. Complete, tested implementation delivered

**vs v2:** Had to run `/feature-plan`, then `/feature-build` separately

### Supported Combinations

- `"plan and build [feature]"` → PLAN + BUILD
- `"review and refactor [code]"` → REVIEW + BUILD  
- `"debug and fix [issue]"` → DEBUG + implementation
- `"plan, build, and review [feature]"` → PLAN + BUILD + REVIEW (complete workflow!)

---

## The 5 Workflows

### REVIEW ⭐⭐⭐⭐⭐ (Always Worth It!)

**Use:** Before EVERY PR, any complexity

**Process:**
1. 5 agents execute in PARALLEL
2. Each analyzes from their dimension
3. Findings consolidated and prioritized
4. Report with specific fixes and line numbers

**Example results:** Can find 30+ issues across severity levels (CRITICAL, HIGH, MODERATE, LOW)

**Cost:** 20k-50k tokens
**ROI:** One prevented security breach = infinite value

```
/cc10x review src/auth.js
```

---

### PLANNING ⭐⭐⭐☆☆ (Complexity 4-5)

**Use:** Complex features needing architecture decisions

**Process:**
1. **Phase 0:** Complexity check (recommends skip if 1-2)
2. **Phase 0a:** Quick default plan with assumptions
3. **User validates:** Proceed / Customize / Manual
4. **Phases 1-7:** Full planning (if approved)
   - Requirements (feature-planner)
   - Architecture (architect)
   - Risk analysis (7 dimensions)
   - Testing strategy
   - File manifest
   - Rollback strategy
   - Deployment plan

**Cost:** 30-60k tokens (vs 15k manual)
**Worth it:** Complexity 4-5 (prevents architecture mistakes)

```
/cc10x plan real-time notifications
```

---

### BUILDING ⭐⭐☆☆☆ (Use with Caution)

**Use:** Complexity 4-5, want strict TDD

**Process:**
1. **Phase 0:** Strong complexity check (warns if simple)
2. **Phase 1:** Context analysis
3. **Phase 2:** Task breakdown (using task-breakdown skill)
4. **Phase 3:** TDD implementation (risk analysis → RED-GREEN-REFACTOR per increment)
5. **Phase 4:** Test generation (>80% coverage)
6. **Phase 5:** Multi-dimensional review (5 agents)
7. **Phase 6:** Finalization

**Important:** Previous versions had reliability issues with test reports. v3 requires MANDATORY user verification for accuracy.

**Cost:** 40-80k tokens (vs 20k manual)
**Skip for:** Complexity 1-2 (manual often better)

```
/cc10x build from plan authentication
```

Or end-to-end:
```
/cc10x plan and build authentication
```

---

### DEBUGGING ⭐⭐⭐☆☆ (LOG FIRST Pattern)

**Use:** Complex bugs, root cause unclear

**Process:**
1. Bug classification (obvious/unclear/complex)
2. Context gathering
3. **LOG FIRST investigation** (observe before fixing)
4. Root cause identification from logs
5. Minimal fix + regression test
6. Cleanup debug code

**Efficiency:** Can save hours by systematic investigation vs guessing

**Cost:** 15-30k tokens (vs 5k manual)
**Worth it:** Saves hours of assumption-driven debugging

```
/cc10x debug rate limiting not blocking requests
```

---

### VALIDATION ⭐⭐⭐☆☆ (Team Accountability)

**Use:** Team projects, pre-PR consistency checks

**Process:**
1. Plan → Code consistency (did we build what we planned?)
2. Code → Tests consistency (is code tested?)
3. Code → Docs consistency (is code documented?)
4. Risks → Mitigations consistency (were risks addressed?)
5. File Manifest → Actual consistency (matches plan?)

**Cost:** 20-45k tokens
**Worth it:** Team projects (prevents drift)

```
/cc10x validate
```

---

## 20 Domain Skills

Skills provide specialized knowledge, loaded progressively by agents:

**Orchestration (NEW in v3):**
1. **task-breakdown** - Converts plans to TODO.md
2. **progress-tracker** - Status reports and velocity

**Planning & Analysis:**
3. **feature-planning** - Requirements, architecture, testing (5 stages)
4. **risk-analysis** - 7-dimension "What Could Go Wrong?" framework
5. **deployment-patterns** - Rollback + deployment strategies (2 stages)

**Development:**
6. **code-generation** - Code patterns
7. **feature-building** - Implementation patterns
8. **test-driven-development** - RED-GREEN-REFACTOR (3 stages)
9. **safe-refactoring** - Refactoring patterns
10. **verification-before-completion** - Quality checklists

**Quality & Review:**
11. **code-review-patterns** - Code smells, refactoring catalog
12. **code-reviewing** - Review methodologies
13. **security-patterns** - OWASP Top 10, secure coding
14. **performance-patterns** - Optimization techniques
15. **accessibility-patterns** - WCAG 2.1 AA compliance

**Debugging & Navigation:**
16. **bug-fixing** - Bug fix strategies with classification
17. **systematic-debugging** - LOG FIRST pattern
18. **codebase-navigation** - Search and pattern discovery

**Design:**
19. **ui-design** - Lovable/Bolt-quality UI patterns
20. **ux-patterns** - UX best practices

---

## Installation

### From GitHub

```bash
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x
```

### Verify

```bash
/plugin      # Should show cc10x
/agents      # Should show 9 agents
```

**Full guide:** [QUICK-START.md](QUICK-START.md)

---

## Usage

### Natural Language (May Not Trigger - 0% rate in testing)

```
"Review this code for security"
"Plan authentication feature"
```

### Slash Command (Guaranteed Loading)

```bash
/cc10x review src/auth.js
/cc10x plan authentication
/cc10x plan and build real-time notifications
/cc10x debug login timeout
/cc10x validate
```

**Recommendation:** Use `/cc10x` for reliability (skill auto-triggering unreliable)

---

## Complexity Guide

cc10x v3 honestly assesses complexity and recommends the right approach:

| Score | Type | Files | Lines | cc10x Worth It? | Why |
|-------|------|-------|-------|-----------------|-----|
| 1 | TRIVIAL | 1 | <50 | ❌ No | Manual 20x cheaper |
| 2 | SIMPLE | 2-3 | 50-200 | ❌ No | Follow library docs |
| 3 | MODERATE | 4-6 | 200-500 | ⚠️ Maybe | If team docs valued |
| 4 | COMPLEX | 7-15 | 500-1000 | ✅ Yes | Prevents mistakes |
| 5 | VERY COMPLEX | 15+ | >1000 | ✅✅ Yes | Essential! |

**Special case:** REVIEW always worth it (prevents security breaches)

---

## Token Economics (Brutal Honesty)

### The Reality

**cc10x v3 costs 3-20x MORE tokens than manual** for most workflows.

**Why?**
- Systematic multi-phase analysis
- Risk assessments (7 dimensions)
- Comprehensive documentation
- Quality enforcement gates

**Worth it when:**
- Complexity 4-5 (one prevented architecture mistake >> token cost)
- Security-sensitive (one breach >> infinite tokens)
- Team collaboration (documentation enables alignment)

**NOT worth it when:**
- Complexity 1-2 (manual 16-20x cheaper and often better)
- Solo dev, familiar pattern
- Time-sensitive
- Token budget constrained

**Exception:** REVIEW always worth it!

### Comparison Table

| Workflow | cc10x Tokens | Manual Tokens | Multiplier | Worth It? |
|----------|--------------|---------------|------------|-----------|
| REVIEW | 20k-50k | N/A (would need 5 experts) | Always | ✅✅ YES |
| PLAN (simple) | 40k | 5k | 8x | ❌ NO |
| PLAN (complex) | 60k | 20k | 3x | ✅ YES |
| BUILD (simple) | 80k | 10k | 8x | ❌ NO |
| BUILD (complex) | 100k | 30k | 3.3x | ✅ YES |
| DEBUG | 25k | 8k | 3x | ✅ Maybe |
| VALIDATE | 35k | N/A | N/A | ⚠️ Teams only |

---

## Architecture Overview

```
USER REQUEST
  ↓
cc10x-orchestrator skill (150 lines, 1.5k tokens)
  ↓ Detects task type + complexity
  ↓ Loads appropriate workflow (3-6k tokens)
  ↓
WORKFLOW FILE (workflows/*.md)
  ↓ Orchestrates agents sequentially or parallel
  ↓
4 CORE AGENTS (execution)
  feature-planner → PRD creation
  architect → Design + complexity + manifest
  code-writer → TDD implementation
  test-generator → Comprehensive tests
  
5 REVIEW AGENTS (parallel)
  security → quality → performance → ux → accessibility
  ↓
20 DOMAIN SKILLS (loaded progressively)
  risk-analysis (7 stages)
  feature-planning (5 stages)
  deployment-patterns (2 stages)
  + 17 others
  ↓
PRODUCTION-READY OUTPUT
  Plans, Code, Tests, Documentation
```

---

## Quality Enforcement

### Automatic via PostToolUse Hook

After every Write/Edit operation:
- ✅ File size validated
- ✅ Warning if >500 lines
- ✅ Split suggestions provided

**From cc10x_V2-main hooks pattern.**

### Enforced by code-writer Agent

- ✅ No placeholders or TODOs
- ✅ Production-ready code only
- ✅ Comprehensive error handling
- ✅ All inputs validated
- ✅ TypeScript for JavaScript
- ✅ DRY and SOLID principles

### Required by test-generator Agent

- ✅ >80% coverage target
- ✅ Meaningful tests (not just coverage numbers)
- ✅ Unit + integration + e2e (based on complexity)
- ✅ **Mandatory user verification** (prevents false reports)

---

## What's NEW in v3?

### From cc10x_V2-main

✅ **4+5 agent architecture** (vs 11 overlapping agents)
✅ **TRUE progressive disclosure** (workflows in separate files)
✅ **PostToolUse hook** (enforces <500 lines automatically)
✅ **Lightweight orchestrator** (150 lines vs 1,325)
✅ **Simpler, clearer, more focused**

### From cc10x v2

✅ **5-star review workflow** (5 parallel agents, proven results)
✅ **7-dimension risk analysis** (prevents edge cases)
✅ **Deployment patterns** (rollback + staged rollouts)
✅ **Honest token economics** (3-20x MORE, not "savings")
✅ **Complexity assessment** (recommends skip for simple)

### New in v3

✅ **Quick default plans** (Phase 0a presents assumptions)
✅ **End-to-end automation** (plan and build in one flow)
✅ **ONE workflow scales** (simple to complex naturally)
✅ **Mandatory test verification** (user must confirm)
✅ **task-breakdown skill** (TODO.md generation)
✅ **progress-tracker skill** (velocity and status)

---

## Real-World Test Results

### REVIEW Workflow ⭐⭐⭐⭐⭐

**Test:** Authentication system review
- **Found:** 38 issues total
- **CRITICAL:** 5 (SQL injection, hardcoded secrets, auth bypass, XSS, missing transaction)
- **HIGH:** 12 (N+1 queries, memory leaks, race conditions)
- **Time:** 3 minutes
- **Tokens:** 35k
- **Verdict:** Worth every token!

### PLAN Workflow (Simple Feature) ❌

**Test:** Rate limiting with express-rate-limit (complexity 2)
- **cc10x:** 100k tokens, 90 minutes, comprehensive plan
- **Manual:** 5k tokens, 30 minutes, working code from library docs
- **Verdict:** cc10x was WORSE (20x more expensive, no better result)

**v3 Fix:** Quick complexity check recommends skip for simple features!

### BUILD Workflow ⚠️

**Test:** Rate limiting implementation
- **Issue:** Reported "All tests passing!" when 3/7 FAILED
- **Problem:** Agent didn't verify tests
- **v3 Fix:** MANDATORY user verification (must run `npm test` and confirm)

---

## When to Use cc10x v3

### ✅ Use For:

**REVIEW workflow:**
- Before EVERY PR (any complexity)
- Security audits
- Performance checks
- Quality reviews
- **Always worth it!**

**PLANNING workflow:**
- Complexity 4-5 features (500+ lines, 7+ files)
- Novel patterns (not in codebase)
- High-risk domains (auth, payments, data)
- Architecture decisions needed
- Team alignment required

**BUILDING workflow:**
- Complexity 4-5 (want strict TDD)
- High-risk implementations
- Systematic quality essential

**DEBUGGING workflow:**
- Complex bugs (root cause unclear)
- Spent >30 min without progress
- Multiple interacting systems

**VALIDATION workflow:**
- Team projects (accountability)
- Pre-PR consistency checks
- Complex features (verify nothing missed)

### ❌ Skip For:

- Simple features (complexity 1-2: use library docs, 16-20x cheaper)
- Obvious fixes (typos, syntax errors)
- Emergencies (fix first, document later)
- Prototypes/MVPs (iterate fast)
- Solo dev with familiar patterns
- Token budget constrained

**v3 will honestly tell you to skip if manual is better!**

---

## File Limits

All files in cc10x (and enforced in your code):

- **Components:** <200 lines
- **Utilities:** <300 lines  
- **Services:** <400 lines
- **Config:** <100 lines
- **Maximum:** 500 lines (hard limit)

**PostToolUse hook validates after EVERY file write.**

---

## Components

- **1 master orchestrator skill** (with progressive workflows)
- **9 sub-agents** (4 core execution + 5 review)
- **20 domain skills** (loaded progressively)
- **1 thin command wrapper** (/cc10x)
- **3 hooks** (SessionStart, PreCompact, PostToolUse)

---

## Contributing

To extend cc10x v3:

1. Add new agents in `plugins/cc10x/agents/` (if truly distinct role)
2. Add new skills in `plugins/cc10x/skills/` (follow official YAML spec)
3. Update workflow files in `skills/cc10x-orchestrator/workflows/`
4. Test with local marketplace
5. Document in README
6. Submit PR

---

## Philosophy

**cc10x v3 = The Perfect Fusion**

We took the BEST from two parallel projects:

**cc10x_V2-main gave us:**
- Simplicity (4 focused agents)
- Efficiency (TRUE progressive disclosure)
- Enforcement (PostToolUse hooks)
- Proven architecture

**cc10x v2 gave us:**
- Excellence (5-star review)
- Intelligence (7-dimension risk analysis)
- Strategy (deployment patterns)
- Honesty (real token economics)

**Result:** World-class systematic development system that's both powerful AND efficient.

---

## Support

- **Repository:** https://github.com/romiluz13/cc10x
- **Issues:** https://github.com/romiluz13/cc10x/issues
- **Quick Start:** [QUICK-START.md](QUICK-START.md)
- **User Guide:** [plugins/cc10x/CLAUDE.md](plugins/cc10x/CLAUDE.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

## License

MIT

---

**Built with:**
- BMAD methodology principles
- cc10x_V2-main progressive architecture
- cc10x v2 proven patterns
- Official Anthropic specifications
- Brutal real-world testing feedback

**Powered by Claude Sonnet 4.5**

**Use `/cc10x review` liberally. Use other workflows for complexity 4-5 only.**
