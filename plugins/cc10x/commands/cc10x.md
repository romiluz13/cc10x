---
name: cc10x
description: Invokes cc10x master orchestrator skill for systematic development workflows (review, plan, build, debug, validate)
argument-hint: describe your task (e.g., "review src/auth.js" or "plan authentication feature")
---

# cc10x Command

This command loads the `cc10x-orchestrator` master skill and passes your request through.

## Purpose

The cc10x command is a thin wrapper that ensures the master orchestrator skill loads. While you can invoke skills directly with natural language ("review this code"), skill auto-triggering isn't 100% reliable (brutal testing showed 0% trigger rate). This command guarantees the skill loads.

## Usage

```bash
/cc10x [your request]
```

### Examples

**Code Review:**
```bash
/cc10x review src/auth.js
/cc10x audit src/features/payment/ for security issues
/cc10x check this code for performance problems
```

**Feature Planning:**
```bash
/cc10x plan authentication with JWT
/cc10x design real-time notifications architecture
/cc10x create PRD for multi-tenancy
```

**Feature Building:**
```bash
/cc10x build authentication feature from the plan
/cc10x implement payment processing with Stripe
/cc10x develop user dashboard
```

**Bug Fixing:**
```bash
/cc10x debug why rate limiting isn't working
/cc10x fix bug: users can submit empty emails
/cc10x investigate login timeout issue
```

**Validation:**
```bash
/cc10x validate implementation against plan
/cc10x verify code matches requirements
/cc10x check consistency
```

## How It Works

1. You type: `/cc10x [your request]`
2. Command loads: `cc10x-orchestrator` master skill
3. Skill analyzes: Task type + complexity
4. Skill chooses: Appropriate workflow (REVIEW/PLAN/BUILD/DEBUG/VALIDATE)
5. Skill orchestrates: Sub-agents + domain skills
6. Skill delivers: Production-ready results

## Alternative Invocation Methods

### Natural Language (May Not Always Trigger)

```
"Review this code for security issues"
"Plan authentication feature"
```

If the master orchestrator skill triggers, it will work. But testing showed skills don't auto-trigger reliably.

### Explicit Skill Invocation (Guaranteed)

```
"Use cc10x-orchestrator skill to review src/auth.js"
"Apply cc10x-orchestrator skill to plan authentication"
```

This always works (forces skill loading).

### Slash Command (This File - Guaranteed)

```
/cc10x review src/auth.js
```

Also always works (this command loads the skill).

## What the Master Orchestrator Does

The `cc10x-orchestrator` skill contains all workflow logic:

**WORKFLOW 1: REVIEW** ⭐⭐⭐⭐⭐
- 5 agents in parallel (security, quality, performance, UX, accessibility)
- Found 38 issues in testing (5 CRITICAL)
- Always worth it

**WORKFLOW 2: PLANNING**
- Checks complexity FIRST
- Recommends skip if simple (complexity 1-2)
- 7-phase systematic planning for complex features (4-5)

**WORKFLOW 3: BUILDING**
- Strong complexity check (don't waste tokens on simple!)
- TDD-enforced with risk analysis before each increment
- MUST verify tests manually (agents can report false success)

**WORKFLOW 4: DEBUGGING**
- LOG FIRST pattern (prevents guessing)
- Systematic investigation
- Saves hours for complex bugs

**WORKFLOW 5: VALIDATION**
- 5-dimension consistency checking
- Plan-code-tests-docs validation

## Complexity Guide

The orchestrator will assess complexity and recommend:

- **1-2 (TRIVIAL/SIMPLE):** ❌ Skip cc10x (manual 16-20x cheaper)
- **3 (MODERATE):** ⚠️ Maybe (if team docs valued)
- **4-5 (COMPLEX/VERY COMPLEX):** ✅ Use cc10x (prevents mistakes)
- **REVIEW:** ✅✅ Always use (5⭐ killer feature)

## Remember

This command just loads the master orchestrator skill. All intelligence lives in the skill.

**Philosophy:** Skills orchestrate, commands are just wrappers.

**Use:** `/cc10x` when you want to guarantee the skill loads, or use natural language if you're feeling lucky!

