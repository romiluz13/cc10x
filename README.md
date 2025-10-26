# cc10x v2.1 - Focused Orchestrator

**Does what you ask. Delivers results fast. No endless loops.**

**Version:** 2.1.0 | **License:** MIT | **Status:** Production-Ready

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://github.com/romiluz13/cc10x)
[![Focused](https://img.shields.io/badge/Orchestration-Focused-green)](https://github.com/romiluz13/cc10x)
[![Version](https://img.shields.io/badge/version-2.1.0-green)](https://github.com/romiluz13/cc10x/releases)

---

## The Problem We Solved

**Previous versions:**
```
You: "Build a simple todo app"
→ cc10x: "Let me do security review first..."
→ cc10x: "Now risk analysis..."
→ cc10x: "Now deployment planning..."
→ 4 hours later...
→ You: "WHERE'S MY TODO APP?!"
```

**v2.1 with THE FOCUS RULE:**
```
You: "Build a simple todo app"
→ cc10x: "Building todo app."
→ 45 minutes later: Working todo app delivered!
```

**THE FOCUS RULE: Do what user asked. Nothing more.**

---

## Quick Start

```bash
# Install
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x

# Use (just ask for what you want!)
/cc10x review src/auth.js       # Reviews security
/cc10x build todo app           # Builds todo app  
/cc10x fix login bug            # Fixes the bug
```

**No endless orchestration. Just results.**

---

## The 4 Core Workflows

### 1. REVIEW (5-Star - Always Valuable)

**Use:** Before every PR

```bash
/cc10x review src/auth.js
```

**What happens:**
- 5 agents analyze in parallel (security, quality, performance, UX, accessibility)
- Finds critical issues (SQL injection, memory leaks, WCAG violations)
- Reports with specific fixes
- **Done in 3-5 minutes**

**Delivers:** Issue report with fixes  
**Focus:** ONLY reviews what you asked for

---

### 2. BUILD (Delivers Working Code)

**Use:** When you want to build something

```bash
/cc10x build authentication feature
```

**What happens:**
1. Quick complexity check
2. **Asks you:** "Quick build (fast) or systematic (comprehensive)?"
3. If quick: Builds it directly (45-90 min)
4. If systematic: Full TDD workflow (2-4 hours)
5. **Delivers working code**

**Focus:** Builds what you asked for, THEN asks if you want more

---

### 3. FIX (LOG FIRST Debugging)

**Use:** When you have a bug

```bash
/cc10x fix rate limiting not working
```

**What happens:**
1. Adds logging to see actual data
2. Reproduces bug, observes logs
3. Identifies root cause
4. Implements fix
5. Adds regression test
6. **Done in 15-45 minutes**

**Focus:** Fixes the bug, doesn't analyze your entire architecture

---

### 4. VALIDATE (Optional - Team Projects)

**Use:** Pre-PR consistency checks

```bash
/cc10x validate
```

**What happens:**
- Checks plan matches code
- Verifies tests exist
- **Done in 10-20 minutes**

**Focus:** Quick validation, not comprehensive audit

---

## The Focus Rule

**At the core of v2.1:**

```markdown
🎯 DO WHAT USER ASKED. NOTHING MORE.

User: "Build app" → Build app (NO forced planning!)
User: "Review security" → Review security (NO quality/performance/UX added!)
User: "Fix bug" → Fix bug (NO architecture analysis!)

Default: DIRECT EXECUTION (fast, focused)
Systematic: ONLY if user explicitly requests
```

**This is embedded in the orchestrator to prevent endless loops.**

---

## Architecture

### 11 Specialized Agents

**5 Review Agents (Parallel):**
- security-reviewer
- quality-reviewer
- performance-analyzer
- ux-reviewer
- accessibility-reviewer

**6 Execution Agents (Used as needed):**
- requirements-analyst (planning)
- architect (design)
- context-analyzer (codebase exploration)
- implementer (TDD implementation)
- tdd-enforcer (quality gates)
- devops-planner (deployment)

**The orchestrator only activates agents needed for YOUR task!**

### 20 Domain Skills

Skills provide knowledge, loaded progressively by agents:
- risk-analysis (7-dimension framework)
- feature-planning, test-driven-development
- security-patterns, performance-patterns
- deployment-patterns, bug-fixing
- +13 other specialized skills

---

## Token Economics (Honest)

**cc10x costs more tokens than manual** for systematic workflows.

**Why use it?**
- Review: Finds issues you'd miss (worth it!)
- Build (systematic): Prevents architecture mistakes (complex features only)
- Fix: LOG FIRST saves hours of guessing

**When to skip:**
- Simple tasks (<200 lines, using libraries)
- Obvious fixes
- When you just want it done fast

**v2.1 difference:** Doesn't force systematic on simple tasks anymore!

---

## Quality Enforcement

- PostToolUse hook validates <500 lines after every file write
- TDD enforcer ensures tests written first
- Review agents find real issues
- But only when YOU ask for it!

---

## Installation

```bash
# From GitHub
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x

# Verify
/plugin      # Should show cc10x v2.1
/agents      # Should show 11 agents
```

---

## What's Different in v2.1

### From v2.0

**Fixed:** Endless orchestration loops
**Added:** THE FOCUS RULE (does what you ask)
**Kept:** All working agents and execution logic
**Improved:** User controls flow, not orchestrator

### From v3.0 (Reverted)

**Why we reverted:**
- v3 had meta-instructions ("Load workflow") with no execution
- Caused never-ending loops
- Lost focus on user's actual request

**What we kept from v3:**
- PostToolUse hook (good addition!)
- task-breakdown skill
- progress-tracker skill

---

## Usage Philosophy

**Simple tasks:**
```
/cc10x build todo list
→ Asks: Quick or systematic?
→ Default: Quick (delivers fast!)
```

**Complex tasks:**
```
/cc10x build multi-tenant authentication
→ Assesses: High complexity
→ Recommends: Systematic approach
→ Delivers: Comprehensive solution
```

**YOU control the depth. Orchestrator suggests, you decide.**

---

## Support

- **Repository:** https://github.com/romiluz13/cc10x
- **Quick Start:** [QUICK-START.md](QUICK-START.md)
- **Issues:** https://github.com/romiluz13/cc10x/issues

---

## License

MIT

---

**cc10x v2.1: Focused orchestration that respects your time and delivers what you asked for.**

**Use `/cc10x review` before every PR. Use `/cc10x build` when you want it done right. Simple or systematic - your choice!**
