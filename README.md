# cc10x - The Perfect Claude Code Workflow System

> **v5.9.1** | 6 Agents | 11 Skills | 1 Router | Memory Persistence | TDD Enforcement | Plan→Build Automation

**cc10x is what Claude Code should be.** It transforms Claude from a helpful assistant into a disciplined engineering system that never cuts corners.

---

## Why cc10x is Perfect

### The Problem with Vanilla Claude Code

Without cc10x, Claude Code:
- **Guesses** instead of investigating (fixes bugs without checking logs)
- **Skips tests** ("I'll add tests later" = never)
- **Claims success without evidence** ("It should work now")
- **Forgets context** on long sessions (compaction loses everything)
- **Picks random skills** instead of following workflows

### What cc10x Fixes

| Problem | cc10x Solution |
|---------|---------------|
| Guessing at bugs | **LOG FIRST** - Evidence before fixes |
| Skipping tests | **TDD Enforcement** - RED-GREEN-REFACTOR or nothing |
| "It works" claims | **Verification** - Exit code 0 or it didn't happen |
| Context loss | **Memory Persistence** - Survives compaction |
| Random skill picking | **Single Router** - One entry point, correct workflow |
| False positives | **Confidence Scoring** - Only report issues with 80%+ confidence |
| Building wrong thing | **User Confirmation Gates** - Clarify before implementing |

---

## Architecture

```
USER REQUEST
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│                    cc10x-router (ONLY ENTRY POINT)          │
│  AUTO-EXECUTE on: build, review, debug, plan, fix, etc.     │
└─────────────────────────────────────────────────────────────┘
     │
     ├── BUILD intent ──► component-builder ──► code-reviewer ──► silent-failure-hunter ──► integration-verifier
     │
     ├── REVIEW intent ─► code-reviewer (or silent-failure-hunter for error handling)
     │
     ├── DEBUG intent ──► bug-investigator ──► code-reviewer ──► integration-verifier
     │
     └── PLAN intent ───► planner

MEMORY (.claude/cc10x/)
├── activeContext.md  ◄── Current focus, decisions, learnings
├── patterns.md       ◄── Project conventions, gotchas
└── progress.md       ◄── Completed work, remaining tasks
```

---

## The 6 Agents

| Agent | Role | Tools | Key Behavior |
|-------|------|-------|--------------|
| **component-builder** | Builds features | Read, Edit, Write, Bash, Grep, Glob, Skill | TDD: RED-GREEN-REFACTOR |
| **bug-investigator** | Fixes bugs | Read, Edit, Write, Bash, Grep, Glob, Skill | LOG FIRST: Evidence before fixes |
| **code-reviewer** | Reviews code | Read, Write, Bash, Grep, Glob, Skill | Confidence scoring: Only report >= 80% |
| **integration-verifier** | Verifies E2E | Read, Write, Bash, Grep, Glob, Skill | Evidence-based: Exit codes matter |
| **planner** | Creates plans | Read, Write, Bash, Grep, Glob, Skill | Saves plans to `docs/plans/` + updates memory |
| **silent-failure-hunter** | Audits errors | Read, Write, Bash, Grep, Glob, Skill | Zero tolerance for empty catch blocks |

### Why These Tools?

- **Edit**: Only for agents that modify code (builder, bug-fix)
- **Write**: All agents (for memory updates, saving outputs)
- **Bash**: All agents (for running tests, memory load command)
- **Grep/Glob**: All agents (for searching codebase)
- **Skill**: All agents (for loading conditional skills)

---

## The 11 Skills

Skills are **loaded by agents**, not invoked directly. This prevents Claude from picking skills randomly.

| Skill | Always Loaded By | Conditionally Loaded By | Purpose |
|-------|------------------|------------------------|---------|
| **session-memory** | ALL agents | - | Persist context across compaction |
| **test-driven-development** | component-builder, bug-investigator | - | RED-GREEN-REFACTOR enforcement |
| **code-generation** | component-builder | - | Write minimal code, match patterns |
| **debugging-patterns** | bug-investigator, integration-verifier | - | LOG FIRST, root cause analysis |
| **code-review-patterns** | code-reviewer, silent-failure-hunter | - | Two-stage review, security, quality |
| **planning-patterns** | planner | - | Comprehensive plans, TDD tasks |
| **brainstorming** | - | planner (idea exploration) | Explore ideas before implementation |
| **architecture-patterns** | planner, integration-verifier | code-reviewer, component-builder, bug-investigator | System design, API design |
| **frontend-patterns** | - | code-reviewer, component-builder, bug-investigator, integration-verifier, planner | UX, accessibility, visual design |
| **verification-before-completion** | ALL agents | - | Evidence before claims |
| **cc10x-router** | ENTRY POINT | - | Routes to correct workflow |

---

## The 4 Workflows

### BUILD Workflow

**Trigger**: "build", "implement", "create", "make", "write", "add", "develop", "code"

```
1. LOAD MEMORY (activeContext, patterns, progress)
2. CLARIFY REQUIREMENTS (CRITICAL: DO NOT SKIP)
   - What exactly needs to be built?
   - What are the acceptance criteria?
   - What edge cases should be handled?
   - WAIT for user answers
3. INVOKE component-builder (TDD cycle)
4. INVOKE code-reviewer (confidence scoring)
5. INVOKE silent-failure-hunter (if error handling code)
6. INVOKE integration-verifier (end-to-end)
7. UPDATE MEMORY (learnings, decisions, progress)
```

### REVIEW Workflow

**Trigger**: "review", "audit", "check", "analyze"

```
1. LOAD MEMORY
2. INVOKE code-reviewer
   - Check git history (git log, git blame)
   - Verify functionality first
   - Security, quality, performance review
   - Only report issues with confidence >= 80
3. UPDATE MEMORY
```

### DEBUG Workflow

**Trigger**: "debug", "fix", "error", "bug", "broken", "troubleshoot"

```
1. LOAD MEMORY (check Common Gotchas!)
2. INVOKE bug-investigator
   - LOG FIRST: Gather evidence before fixing
   - Root cause analysis
   - Minimal targeted fix
   - Regression test
3. INVOKE code-reviewer (review the fix)
4. INVOKE integration-verifier (verify fix works)
5. UPDATE MEMORY (add to Common Gotchas!)
```

### PLAN Workflow

**Trigger**: "plan", "design", "architect", "roadmap", "strategy"

```
1. LOAD MEMORY
2. INVOKE planner
   - Understand functionality
   - Design architecture
   - Identify risks
   - Create roadmap
3. UPDATE MEMORY (save architectural decisions)
```

---

## Expected Behavior

### When You Say "Build a Task Tracker"

**CORRECT (cc10x v5.9.1)**:
```
Detected BUILD intent. Executing BUILD workflow.

Loading memory...
[Runs memory load command]

Clarifying requirements (CRITICAL: DO NOT SKIP):
1. What framework/language should I use? (Node.js, Python, etc.)
2. Should tasks have priorities, due dates, or categories?
3. CLI app or web app?
4. Any specific features beyond basic CRUD?

Waiting for your answers before invoking component-builder.
```

**WRONG (without cc10x)**:
```
I'll help you build a task tracker! Let me start by creating the files...

[Writes code without asking questions]
[Skips tests]
[Claims "it should work"]
```

### When You Say "Fix the Login Bug"

**CORRECT (cc10x v5.9.1)**:
```
Detected DEBUG intent. Executing DEBUG workflow.

Loading memory...
[Checks Common Gotchas for similar issues]

Understanding the issue:
1. What error message are you seeing?
2. What's the expected behavior vs actual behavior?
3. When did it start happening?

Waiting for details before invoking bug-investigator with LOG FIRST approach.
```

**WRONG (without cc10x)**:
```
The login bug is probably caused by [guesses at random cause].

Let me try this fix... [changes code without checking logs]

It should work now! [no verification]
```

### When You Say "Review This PR"

**CORRECT (cc10x v5.9.1)**:
```
Detected REVIEW intent. Executing REVIEW workflow.

Loading memory...

Invoking code-reviewer...

## Review Summary

### Git Context
- Recent commits: [relevant changes]
- Authors: [who touched these files]

### Skills Loaded
- code-review-patterns: loaded
- verification-before-completion: loaded

## Critical Findings (confidence >= 80)
- [95] SQL injection risk - src/api.ts:42
  - Fix: Use parameterized queries

## Important Findings (confidence >= 80)
- [85] Missing input validation - src/form.ts:18
  - Fix: Add email format check
```

**WRONG (without cc10x)**:
```
The code looks good overall. I noticed a few things:
- Maybe add some comments?
- The variable names could be better
- Have you considered using TypeScript?

[Vague feedback, no file:line citations, no confidence levels]
```

---

## Memory Persistence

cc10x survives context compaction. This is critical for long sessions.

### Memory Files

```
.claude/cc10x/
├── activeContext.md   # What we're working on NOW
│   - Current Task
│   - Active Decisions (and WHY)
│   - Learnings from this session
│   - Immediate Next Steps
│
├── patterns.md        # Project conventions
│   - Code Patterns (how this project writes code)
│   - Common Gotchas (bugs we've seen and fixes)
│   - Architectural Decisions (and rationale)
│
└── progress.md        # What's done, what's left
    - Completed Items (with evidence)
    - Remaining Tasks
    - Blockers
```

### Iron Law

```
EVERY WORKFLOW MUST:
1. LOAD memory at START (and before key decisions)
2. UPDATE memory at END (and after learnings/decisions)
```

**Failure to update memory = incomplete workflow.**

---

## Plan→Build Automation (v5.9.1)

cc10x connects planning to building automatically. No more lost plans.

### Two-Step Save Pattern

When you create a plan:
1. **Save artifact** → `docs/plans/YYYY-MM-DD-<feature>-plan.md`
2. **Update memory** → `.claude/cc10x/activeContext.md` references the plan

### Automatic Plan Detection

When component-builder starts, it:
```bash
# Extracts plan reference from memory
PLAN_REF=$(grep -oE 'docs/plans/[^ ]*\.md' .claude/cc10x/activeContext.md)

# If plan exists, shows it
if [ -f "$PLAN_REF" ]; then
  cat "$PLAN_REF"
  echo "=== FOLLOW THESE TASKS IN ORDER ==="
fi
```

### Why This Matters

| Without cc10x | With cc10x v5.9.1 |
|---------------|-------------------|
| Plan exists only in conversation | Plan saved to file |
| Compaction loses the plan | Plan survives compaction |
| Builder doesn't know about plan | Builder auto-loads plan |
| Manual copy-paste needed | Automatic handoff |

### Example Flow

```
Day 1: "Plan a task tracker"
  → Planner creates docs/plans/2025-01-05-task-tracker-plan.md
  → Memory updated: "Plan ready at docs/plans/..."

Day 2: "Build it"
  → Router detects BUILD intent
  → component-builder loads memory
  → grep finds plan reference
  → cat shows plan content
  → Builder follows plan tasks with TDD
```

---

## Why This System is the Best

### 1. Single Entry Point (Router)

Other systems let Claude pick any skill randomly. cc10x has ONE entry point that routes to the correct workflow. No more:
- "Let me use brainstorming..." when you said "build"
- "Let me load planning-patterns..." when you said "fix"

### 2. Agents with Correct Tools

Every agent has exactly the tools it needs:
- Builders have Edit (they modify code)
- Analyzers don't have Edit (they only report)
- ALL agents have Write (for memory updates)
- ALL agents have Bash (for running tests/commands)

### 3. TDD Enforcement

The component-builder agent MUST follow RED-GREEN-REFACTOR:
1. Write failing test (RED)
2. Write minimal code to pass (GREEN)
3. Clean up (REFACTOR)

**No exceptions.** If you wrote code before the test, delete it and start over.

### 4. Evidence-Based Verification

No "it should work" claims. cc10x requires:
- Exit code 0 from test runs
- Actual command output
- Pass/fail evidence

### 5. Confidence Scoring

The code-reviewer only reports issues with confidence >= 80%. This eliminates:
- False positives
- Nitpicks
- Style preferences
- "Maybe this is an issue?"

### 6. User Confirmation Gates

BUILD workflow MUST clarify requirements before implementing:
- What exactly needs to be built?
- What are the acceptance criteria?
- WAIT for user answers

If user says "whatever you think", state your recommendation and get confirmation.

### 7. Memory That Survives

Context compaction loses everything in vanilla Claude. cc10x persists:
- What you're working on
- Decisions made and why
- Common gotchas
- Progress tracking

### 8. Silent Failure Hunting

The silent-failure-hunter agent finds error handling issues with zero tolerance:
- Empty catch blocks
- Log-only catches (user never knows)
- Generic "Something went wrong" messages
- Fallbacks without logging

---

## Installation

```bash
# Add marketplace
/plugin marketplace add romiluz13/cc10x

# Install plugin
/plugin install cc10x@romiluz13

# Restart Claude Code
```

---

## Quick Start

```bash
# BUILD - Creates features with TDD
"build a user authentication system"

# REVIEW - Audits code with confidence scoring
"review this PR for security issues"

# DEBUG - Fixes bugs with LOG FIRST
"debug the payment processing error"

# PLAN - Creates comprehensive plans
"plan the microservices architecture"
```

---

## Files Changed in v5.6.0

### Agents (6 files)
- `plugins/cc10x/agents/component-builder.md`
- `plugins/cc10x/agents/bug-investigator.md`
- `plugins/cc10x/agents/code-reviewer.md`
- `plugins/cc10x/agents/integration-verifier.md`
- `plugins/cc10x/agents/planner.md`
- `plugins/cc10x/agents/silent-failure-hunter.md`

### Skills (11 files)
- `plugins/cc10x/skills/cc10x-router/SKILL.md`
- `plugins/cc10x/skills/session-memory/SKILL.md`
- `plugins/cc10x/skills/test-driven-development/SKILL.md`
- `plugins/cc10x/skills/code-generation/SKILL.md`
- `plugins/cc10x/skills/debugging-patterns/SKILL.md`
- `plugins/cc10x/skills/code-review-patterns/SKILL.md`
- `plugins/cc10x/skills/planning-patterns/SKILL.md`
- `plugins/cc10x/skills/brainstorming/SKILL.md`
- `plugins/cc10x/skills/architecture-patterns/SKILL.md`
- `plugins/cc10x/skills/frontend-patterns/SKILL.md`
- `plugins/cc10x/skills/verification-before-completion/SKILL.md`

---

## Version History

- **v5.9.1** - Plan→Build connection: grep+cat FORCES plan into builder context (100% confidence)
- **v5.9.0** - Two-step save pattern: Artifact file + memory update, AskUserQuestion usage, UI mockups in brainstorming, observability section
- **v5.8.1** - Strengthened router bypass prevention - all agents and skills explicitly prevent direct invocation
- **v5.7.3** - Removed action keywords from agent descriptions (prevents router bypass!)
- **v5.7.2** - Fixed skill documentation inconsistencies (accurate agent→skill mappings)
- **v5.7.1** - Added verification-before-completion to silent-failure-hunter
- **v5.7.0** - Fixed agent keyword conflicts (agents were bypassing router!)
- **v5.6.0** - Fixed agent tool misconfigurations (planner couldn't save plans!)
- **v5.5.0** - Fixed skill keyword conflicts (router is now ONLY entry point)
- **v5.4.0** - Fixed router to AUTO-EXECUTE instead of listing capabilities
- **v5.3.0** - Added confidence scoring, user confirmation gates, silent-failure-hunter
- **v5.2.0** - Added session memory with READ+WRITE triggers

---

## License

MIT License

---

## Contributing

- Star the repository
- Report issues
- Suggest improvements

---

_cc10x v5.9.1 | The Perfect Claude Code Workflow System_
