# cc10x v2 - Skills-First Systematic Development

**ONE master orchestrator skill** + 11 specialized agents + 17 domain skills

> Architecture: Skills orchestrate workflows, not commands. Natural language preferred.

**Version:** 2.0.0 | **License:** MIT | **Status:** Production-Ready

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://github.com/romiluz13/cc10x)
[![Skills First](https://img.shields.io/badge/Architecture-Skills%20First-green)](https://github.com/romiluz13/cc10x)
[![Version](https://img.shields.io/badge/version-2.0.0-green)](https://github.com/romiluz13/cc10x/releases)

---

## 🎯 Skills-First Architecture

cc10x v2.0 is built on **skills as orchestrators**, following official Anthropic patterns.

```
MASTER ORCHESTRATOR SKILL
  cc10x-orchestrator
    ↓ Detects task type from your message
    ↓ Chooses appropriate workflow
    ↓ Invokes specialized agents
    ↓ Loads domain skills progressively
    
11 SUB-AGENTS (Workers)
  5 review agents (parallel) ⭐⭐⭐⭐⭐
  4 planning agents (sequential)
  2 implementation agents
  
17 DOMAIN SKILLS (Knowledge)
  risk-analysis (7 stages) ← "What Could Go Wrong?"
  feature-planning (5 stages)
  deployment-patterns (2 stages)
  + 14 other specialized skills
```

**No slash commands needed!** Just describe what you need in natural language.

*(Optional /cc10x command available as wrapper to ensure skill loads)*

---

## ⭐ The Killer Feature

**REVIEW Workflow** - Always worth it, use before EVERY PR

```
"Review this code for security issues"
"Audit src/auth.js"
"Check src/features/payment/ for vulnerabilities"
```

**What happens:**
- 5 AI agents launch in parallel
- Analyze: Security, Quality, Performance, UX, Accessibility
- Find real issues with specific fixes

**Real test results:**
- Found: 38 issues (5 CRITICAL, 12 HIGH, 21 MODERATE/LOW)
- CRITICAL: SQL injection, hardcoded secrets, auth bypass, XSS, missing transactions
- Time: 2-3 minutes
- Verdict: ⭐⭐⭐⭐⭐

**One prevented security breach >> any token cost**

---

## 🚀 Quick Start

### Installation

```bash
# Add cc10x marketplace
/plugin marketplace add romiluz13/cc10x

# Install cc10x plugin
/plugin install cc10x@cc10x
```

### Usage (3 Methods)

**Method 1: Natural Language (Preferred)**
```
"Review this code for issues"
"Plan authentication feature with JWT"
"Debug why rate limiting isn't working"
```

The master orchestrator skill should trigger and handle your request.

**Method 2: Explicit Skill Invocation (Guaranteed)**
```
"Use cc10x-orchestrator skill to review src/auth.js"
"Use cc10x-orchestrator skill to plan payment processing"
```

This ALWAYS works (forces skill loading).

**Method 3: Slash Command (Guaranteed)**
```bash
/cc10x review src/auth.js
/cc10x plan authentication feature
/cc10x debug login timeout
```

Also always works (thin wrapper that loads master skill).

---

## 📚 The 5 Workflows

### 1. REVIEW ⭐⭐⭐⭐⭐ (Use for Everything!)

```
"Review src/auth.js for security"
/cc10x audit src/features/payment/
```

**Always worth it!** Finds CRITICAL security issues, performance bugs, code quality problems.

**Tokens:** 20k-50k (worth every token)

---

### 2. PLANNING (Use for Complexity 4-5)

```
"Plan real-time notifications with WebSockets"
/cc10x design multi-tenancy architecture
```

**Complexity check FIRST!**
- Complexity 1-2: Recommends skip (16-20x cheaper to go manual)
- Complexity 3: Shows tradeoffs, asks preference
- Complexity 4-5: Proceeds with comprehensive planning

**Phases:** Requirements → Context → Architecture → Risk Analysis → Complexity → Testing → Roadmap → Manifest → Rollback → Deployment

**Tokens:** 3.2k (simple, stops early) or 5.2k (complex, full workflow)

---

### 3. BUILDING (Use for Complexity 4-5, Verify Tests!)

```
"Build authentication feature from the plan"
/cc10x implement payment processing
```

**Strong complexity check!** Will STRONGLY recommend manual if complexity <3.

**Process:** TDD with risk analysis before each increment, file manifest verification, MANDATORY test verification

⚠️ **CRITICAL:** Must manually verify tests pass (don't trust "all tests passing" claims!)

**Tokens:** 60k-150k (8-16x MORE than manual)

---

### 4. DEBUGGING (Use for Complex Bugs)

```
"Debug why rate limiting isn't working"
/cc10x investigate login timeout
```

**LOG FIRST pattern:** Add logging, see actual data, fix based on observations (not assumptions)

**Real test:** Saved 2 hours vs random guessing

**Tokens:** 15k-30k

---

### 5. VALIDATION (Use for Team Accountability)

```
"Validate this against the plan"
/cc10x verify implementation consistency
```

**5 dimensions:** Plan-Code, Code-Tests, Code-Docs, Risk Mitigation, File Manifest

**Tokens:** 20k-45k

---

## 💎 What Makes cc10x Special

### "What Could Go Wrong?" Methodology

**7-Dimension Risk Analysis** integrated everywhere:

1. Data Flow & Transformations (nulls, validation, edge cases)
2. Dependency & Integration (circular deps, version conflicts)
3. Timing, Concurrency & State (race conditions)
4. User Experience & Human Factors (accessibility, error messages)
5. Security & Validation (SQL injection, XSS, auth)
6. Performance & Scalability (O(n²), memory leaks)
7. Failure Modes & Recovery (error handling)

**Invoked:** Before architecture decisions, before each implementation increment, during comprehensive reviews

### Cursor IDE Enhancements

- **Complexity Assessment:** 1-5 scoring, recommends skip if simple
- **File Change Manifests:** CREATE/MODIFY/DELETE breakdown, prevents scope creep
- **Rollback Strategies:** < 5 min recovery procedures
- **Deployment Plans:** 5-stage risk-aware rollout

### Mandatory Verification

**Prevents false "tests passing" reports:**
- Must run actual test command
- Must verify exit code = 0
- Must see ✓ symbols with YOUR EYES
- Never trust reports without proof

---

## ⚠️ Honest Reality

### Token Economics

**cc10x costs 3-20x MORE tokens than manual implementation.**

| Complexity | cc10x | Manual | Worth It? |
|------------|-------|--------|-----------|
| 1 (TRIVIAL) | 40k | 2k | ❌ NO |
| 2 (SIMPLE) | 80k | 5k | ❌ NO |
| 3 (MODERATE) | 100k | 15k | ⚠️ MAYBE |
| 4 (COMPLEX) | 120k | 30k | ✅ YES |
| 5 (VERY COMPLEX) | 180k | 50k | ✅✅ YES |

**Exception:** REVIEW always worth it (prevents security breaches)

**Why more expensive?** Systematic analysis, risk assessment, comprehensive documentation

**When worth it?** Complexity 4-5 where one prevented architecture mistake pays for planning

---

### When to Use cc10x

✅ **Use for:**
- ALL code reviews (REVIEW workflow ⭐⭐⭐⭐⭐)
- Complex features (4-5 complexity)
- High-risk changes (auth, payments, data)
- Team collaboration (docs valued)

❌ **Skip for:**
- Simple features (1-2 complexity)
- Well-documented libraries (read docs instead)
- Time-sensitive (manual faster)
- Solo dev, familiar patterns

---

## 📖 Documentation

- [CLAUDE.md](plugins/cc10x/CLAUDE.md) - Complete user guide
- [Technical Architecture](plugins/cc10x/README.md) - Deep dive into skills-first design
- [CHANGELOG](CHANGELOG.md) - Version history
- [Installation](docs/INSTALLATION.md) - Setup instructions

---

## 🎓 Real-World Test Results

### Test 1: Simple Feature (Rate Limiting) ❌

**cc10x:** 100k tokens, reported "tests passing", actually 3/7 FAILED
**Manual:** 30 min, 5k tokens, working code
**Lesson:** Don't use cc10x for simple library integrations!

### Test 2: Code Review ✅

**cc10x:** 3 min, 35k tokens, found 38 issues (5 CRITICAL)
**Lesson:** REVIEW workflow is killer feature!

### Test 3: Autonomous Dev (No cc10x) ✅

**Task:** Build landing page
**No cc10x:** 10 min, 15k tokens, professional result
**Lesson:** cc10x not required for straightforward tasks!

---

## 🏗️ Technical Details

### Master Orchestrator Skill

**File:** `plugins/cc10x/skills/cc10x-orchestrator/SKILL.md`

**Contains:** All 5 workflow implementations (~800 lines)

**How it works:**
1. Analyzes your message (task type + complexity)
2. Makes decision (proceed/recommend skip)
3. Executes chosen workflow
4. Orchestrates agents + skills
5. Delivers results

### The 11 Sub-Agents

**5 Working Agents** (Review) ⭐⭐⭐⭐⭐
- security-reviewer, quality-reviewer, performance-analyzer, ux-reviewer, accessibility-reviewer

**4 Planning Agents** (v2.0 NEW)
- architect, devops-planner, requirements-analyst, tdd-enforcer

**2 Implementation Agents**
- context-analyzer, implementer

### The 18 Skills

**Master:** cc10x-orchestrator (THE orchestrator)

**NEW v2.0:** risk-analysis (7 stages), deployment-patterns (2 stages)

**Enhanced:** feature-planning (5 stages), test-driven-development (3 stages)

**Domain:** 14 other specialized skills (security, performance, UX, etc.)

---

## 🚀 Contributing

Found an issue? Have a suggestion?

1. Check [existing issues](https://github.com/romiluz13/cc10x/issues)
2. Create new issue with details
3. Submit PR with tests

---

## 📄 License

MIT - See [LICENSE](LICENSE)

---

## 💡 Philosophy

**Skills are the future.** They orchestrate workflows, invoke agents, load knowledge progressively.

**Use the right tool for the job:**
- Simple features? Manual (faster, cheaper)
- Complex features? cc10x (systematic, prevents mistakes)
- All code? REVIEW workflow (⭐⭐⭐⭐⭐)

**Be honest about costs. Be clear about value. Let users decide.**

---

**Start with REVIEW workflow (⭐⭐⭐⭐⭐) - it's the best part of cc10x!**
