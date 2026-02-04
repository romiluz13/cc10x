# cc10x

### The Intelligent Orchestrator for Claude Code

**Current version:** 6.0.17

**Recommended: Create `~/.claude/CLAUDE.md` (global) so the router is always active across all projects.**

<p align="center">
  <strong>1 Router</strong> &nbsp;•&nbsp; <strong>6 Agents</strong> &nbsp;•&nbsp; <strong>12 Skills</strong> &nbsp;•&nbsp; <strong>4 Workflows</strong>
</p>

<p align="center">
  <em>Stop picking skills manually. Let the system work for you.</em>
</p>

---

## The Problem With Other Plugins

Most Claude Code plugins are **bloated and over-engineered**:

```
❌ 50+ skills you'll never use
❌ 30+ agents with overlapping responsibilities
❌ No guidance on WHEN to use WHAT
❌ You end up using nothing because it's overwhelming
```

**cc10x is different.** One intelligent router detects your intent and automatically orchestrates the right agents with the right skills. You just work.

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   YOU: "build a user auth system"                                            │
│                                     ┌────────────────────────────────────┐   │
│                              ┌─────►│  component-builder                 │   │
│                              │      │  + TDD enforcement                 │   │
│   ┌────────────────────┐     │      │  + code-generation skill           │   │
│   │                    │     │      └──────────────┬─────────────────────┘   │
│   │   cc10x-router     │─────┤                     │                         │
│   │   (auto-detects    │     │      ┌──────────────▼─────────────────────┐   │
│   │    BUILD intent)   │     │      │  code-reviewer ∥ silent-failure    │   │
│   │                    │     │      │  (parallel execution)              │   │
│   └────────────────────┘     │      └──────────────┬─────────────────────┘   │
│                              │                     │                         │
│                              │      ┌──────────────▼─────────────────────┐   │
│                              └─────►│  integration-verifier              │   │
│                                     │  + E2E validation                  │   │
│                                     └────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**You say what you want. cc10x figures out the rest.**

---

## Installation

```bash
# Add marketplace
/plugin marketplace add romiluz13/cc10x

# Install plugin
/plugin install cc10x@romiluz13

# Restart Claude Code
```

### Recommended: Pre-approve memory commands

cc10x uses `.claude/cc10x/` for memory persistence. To avoid repeated permission prompts (especially on Windows), add to your project's `.claude/settings.json`:

```{
  "permissions": {
    "allow": [
      "Bash(mkdir -p .claude/cc10x)",
      "Bash(mkdir -p docs/plans)",
      "Bash(mkdir -p docs/research)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git blame:*)",
      "Bash(git ls-files:*)"
    ]
  }
}
```

**That's it.** cc10x activates automatically on development keywords.

---

## Global CLAUDE.md (Required)

Create `~/.claude/CLAUDE.md` with the content below. This activates cc10x across all your projects.

**For Claude Code:** After creating this file, scan the user's installed skills (`/plugin list`, `~/.claude/skills/`) and add them to the Complementary Skills table. Skills work TOGETHER with cc10x - they don't conflict.

---

```markdown
# CC10x Orchestration (Always On)

IMPORTANT: ALWAYS invoke cc10x-router on ANY development task. First action, no exceptions.
IMPORTANT: Explore project first, then invoke the router.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: Never bypass the router. It is the system.
IMPORTANT: NEVER use Edit, Write, or Bash (for code changes) without first invoking cc10x-router.

**Skip CC10x ONLY when:**
- User EXPLICITLY says "don't use cc10x", "without cc10x", or "skip cc10x"
- No interpretation. No guessing. Only these exact opt-out phrases.

[CC10x]|entry: ./plugins/cc10x/skills/cc10x-router/SKILL.md

---

## Complementary Skills (Work Together with CC10x)

**Skills are additive, not exclusive.** CC10x provides orchestration. Domain skills provide expertise. Both work together.

**GATE:** Before writing code, check if task matches a skill below. If match, invoke it via `Skill(skill="...")`.

| When task involves... | Invoke |
|-----------------------|--------|
| MongoDB, schema, queries, indexes | `mongodb-agent-skills:mongodb-schema-design` or `mongodb-query-and-index-optimize` |
| React, Next.js, frontend, UI | `react-best-practices` |
| *[Claude: Add user's other installed skills here]* | |

[Skills Index]
|mongodb-agent-skills:{mongodb-schema-design/SKILL.md,mongodb-query-and-index-optimize/SKILL.md}
|vercel-agent-skills:{react-best-practices/SKILL.md}
```

---

## The 4 Workflows

| Intent | Trigger Words | What Happens |
|--------|---------------|--------------|
| **BUILD** | build, implement, create, make, write, add | TDD cycle → Code review → Silent failure hunt → Integration verify |
| **DEBUG** | debug, fix, error, bug, broken, troubleshoot | Log-first investigation → Review fix → Verify works |
| **REVIEW** | review, audit, check, analyze, assess | Multi-dimensional review with 80%+ confidence scoring |
| **PLAN** | plan, design, architect, roadmap, strategy | Comprehensive planning with external research |

---

## What Makes cc10x Different

<table>
<tr>
<td width="50%">

### Without cc10x

```
❌ Claude guesses at bugs
❌ Skips tests ("I'll add later")
❌ Claims "it should work"
❌ Forgets context on compaction
❌ Picks random skills
❌ No verification evidence
```

</td>
<td width="50%">

### With cc10x

```
✓ LOG FIRST - evidence before fixes
✓ TDD enforced - RED-GREEN-REFACTOR
✓ Exit code 0 or it didn't happen
✓ Memory persists across sessions
✓ Router picks the right workflow
✓ Confidence scoring (≥80% only)
```

</td>
</tr>
</table>

---

## Quick Start Examples

### Build Something
```
"build a user authentication system"

→ Router detects BUILD intent
→ Clarifies requirements FIRST (won't skip this)
→ component-builder with TDD
→ code-reviewer + silent-failure-hunter (parallel)
→ integration-verifier
→ Memory updated
```

### Fix a Bug
```
"debug the payment processing error"

→ Router detects DEBUG intent
→ Checks memory for Common Gotchas
→ bug-investigator with LOG FIRST
→ code-reviewer validates fix
→ integration-verifier confirms
→ Added to Common Gotchas
```

### Review Code
```
"review this PR for security issues"

→ Router detects REVIEW intent
→ code-reviewer with git context
→ Only reports issues with ≥80% confidence
→ File:line citations for every finding
```

---

## Architecture

```
USER REQUEST
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    cc10x-router (ONLY ENTRY POINT)              │
│              Detects intent → Routes to workflow                │
└─────────────────────────────────────────────────────────────────┘
     │
     ├── BUILD ──► component-builder ──► [code-reviewer ∥ silent-failure-hunter] ──► integration-verifier
     │
     ├── DEBUG ──► bug-investigator ──► code-reviewer ──► integration-verifier
     │
     ├── REVIEW ─► code-reviewer
     │
     └── PLAN ───► planner

MEMORY (.claude/cc10x/)
├── activeContext.md  ◄── Current focus, decisions, learnings
├── patterns.md       ◄── Project conventions, common gotchas
└── progress.md       ◄── Completed work, remaining tasks
```

---

## The 6 Agents

| Agent | Purpose | Key Behavior |
|-------|---------|--------------|
| **component-builder** | Builds features | TDD: RED → GREEN → REFACTOR (no exceptions) |
| **bug-investigator** | Fixes bugs | LOG FIRST: Evidence before any fix |
| **code-reviewer** | Reviews code | Confidence ≥80%: No vague feedback |
| **silent-failure-hunter** | Finds error gaps | Zero tolerance for empty catch blocks |
| **integration-verifier** | E2E validation | Exit codes: PASS/FAIL with evidence |
| **planner** | Creates plans | Saves to `docs/plans/` + updates memory |

---

## The 12 Skills

Skills are **loaded automatically by agents**. You never invoke them directly.

| Skill | Used By | Purpose |
|-------|---------|---------|
| **session-memory** | WRITE agents | Persist context across compaction |
| **verification-before-completion** | ALL agents | Evidence before claims |
| **test-driven-development** | builder, bug-investigator | RED-GREEN-REFACTOR enforcement |
| **code-generation** | component-builder | Minimal code, match patterns |
| **debugging-patterns** | bug-investigator, verifier | Root cause analysis |
| **code-review-patterns** | code-reviewer, hunter | Security, quality, performance |
| **planning-patterns** | planner | Comprehensive plans |
| **architecture-patterns** | ALL agents | System & API design |
| **frontend-patterns** | ALL agents | UX, accessibility |
| **brainstorming** | planner | Idea exploration |
| **github-research** | planner, bug-investigator (conditional) | External package research |
| **cc10x-router** | ENTRY POINT | Routes to correct workflow |

---

## Memory Persistence

cc10x survives context compaction. This is critical for long sessions.

```
.claude/cc10x/
├── activeContext.md   # What you're working on NOW
│   - Current task
│   - Active decisions (and WHY)
│   - Learnings this session
│
├── patterns.md        # Project conventions
│   - Code patterns
│   - Common gotchas (bugs → fixes)
│   - Architectural decisions
│
└── progress.md        # What's done, what's left
    - Completed items (with evidence)
    - Remaining tasks
    - Blockers
```

**Iron Law:** Every workflow loads memory at START and updates at END.

---

## Task-Based Orchestration

cc10x uses Claude Code's Tasks system for workflow coordination:

```
┌─────────────────────────────────────────────────────────────────┐
│  BUILD: User Authentication                                     │
│  ├── component-builder (pending)                                │
│  ├── code-reviewer (blocked by: builder)                        │
│  ├── silent-failure-hunter (blocked by: builder)                │
│  └── integration-verifier (blocked by: reviewer, hunter)        │
└─────────────────────────────────────────────────────────────────┘
```

- **Dependency chains**: Agents wait for blockers to complete
- **Parallel execution**: reviewer + hunter run simultaneously
- **Resume capability**: TaskList() checks for active workflows
- **Automatic handoff**: Each agent updates status when done

---

## Plan → Build Automation

Plans don't get lost. They flow automatically to the build phase.

```
Day 1: "plan a task tracker"
  → Planner creates docs/plans/2025-01-29-task-tracker-plan.md
  → Memory updated with plan reference

Day 2: "build it"
  → Router detects BUILD
  → component-builder finds plan in memory
  → Follows plan phases with TDD
```

---

## Expected Behavior

### When You Say "Build a Task Tracker"

**cc10x Response:**
```
Detected BUILD intent. Executing BUILD workflow.

Loading memory...
✓ Memory loaded

Clarifying requirements (REQUIRED):
1. What framework/language? (Node.js, Python, etc.)
2. Should tasks have priorities, due dates, categories?
3. CLI app or web app?
4. Any features beyond basic CRUD?

Waiting for your answers before proceeding.
```

**Without cc10x:**
```
I'll help you build a task tracker! Let me start...
[Writes code without asking]
[Skips tests]
[Claims "it should work"]
```

---

## Version History

| Version | Highlights |
|---------|------------|
| **v6.0.0** | Orchestration hardening: Tasks contract correctness + Task-enforced gates + re-review loop |
| **v5.25.1** | GSD-inspired enhancements (wiring verification, hypothesis criteria) |
| **v5.25.0** | Critical orchestration fixes + README redesign |
| **v5.24.0** | Research persistence with THREE-PHASE pattern |
| **v5.23.0** | Plan-task linkage (legacy: metadata.planFile; now deprecated) |
| **v5.22.0** | Stub detection patterns |
| **v5.21.0** | Task-based orchestration with TaskCreate/TaskUpdate |
| **v5.20.0** | Goal-backward verification lens |
| **v5.13.0** | Parallel agent execution (~30-50% faster) |
| **v5.10.0** | Anthropic Claude 4.x best practices |
| **v5.9.1** | Plan→Build automatic connection |

<details>
<summary>Full version history</summary>

- **v6.0.0** - Orchestration hardening:
  - Tasks contract correctness (no undocumented TaskCreate fields; canonical TaskUpdate object form)
  - CC10X task namespacing + safer resume rules
  - Task-enforced gates + re-review loop after remediation (prevents unreviewed changes)
- **v5.25.1** - GSD-inspired enhancements: Wiring verification patterns, hypothesis quality criteria, cognitive biases table
- **v5.25.0** - Critical orchestration fixes: Plan propagation, results collection, skill hierarchy, validation + README redesign
- **v5.24.0** - Research Documentation Persistence: THREE-PHASE research pattern
- **v5.23.0** - Plan-Task Linkage: metadata.planFile for context recovery (legacy; deprecated in v6.0.0)
- **v5.22.0** - Stub Detection Patterns: GSD-inspired stub detection
- **v5.21.0** - Task-Based Orchestration: TaskCreate, TaskUpdate, TaskList integration
- **v5.20.0** - Goal-Backward Lens: Verification enhancements
- **v5.19.0** - OWASP Reference + Minimal Diffs + ADR patterns
- **v5.18.0** - Two-Phase github-research
- **v5.13.1** - Bulletproof chain enforcement
- **v5.13.0** - Parallel agent execution
- **v5.12.1** - Fixed orphan skills
- **v5.12.0** - Pre-publish audit
- **v5.11.0** - Workflow chain enforcement
- **v5.10.6** - Foolproof Router with decision tree
- **v5.10.5** - Complete Permission-Free Audit
- **v5.10.4** - True Permission-Free Memory
- **v5.10.3** - Fixed invalid agent color
- **v5.10.2** - Permission-Free Memory
- **v5.10.1** - Router Supremacy
- **v5.10.0** - Anthropic Claude 4.x alignment
- **v5.9.1** - Plan→Build connection
- **v5.9.0** - Two-step save pattern
- **v5.8.1** - Router bypass prevention
- **v5.7.0** - Fixed agent keyword conflicts
- **v5.6.0** - Fixed agent tool misconfigurations
- **v5.5.0** - Fixed skill keyword conflicts
- **v5.4.0** - Router AUTO-EXECUTE
- **v5.3.0** - Confidence scoring, silent-failure-hunter

</details>

---

## Files Structure

```
plugins/cc10x/
├── agents/
│   ├── component-builder.md
│   ├── bug-investigator.md
│   ├── code-reviewer.md
│   ├── integration-verifier.md
│   ├── planner.md
│   └── silent-failure-hunter.md
│
└── skills/
    ├── cc10x-router/SKILL.md
    ├── session-memory/SKILL.md
    ├── test-driven-development/SKILL.md
    ├── code-generation/SKILL.md
    ├── debugging-patterns/SKILL.md
    ├── code-review-patterns/SKILL.md
    ├── planning-patterns/SKILL.md
    ├── brainstorming/SKILL.md
    ├── architecture-patterns/SKILL.md
    ├── frontend-patterns/SKILL.md
    ├── github-research/SKILL.md
    └── verification-before-completion/SKILL.md
```

---

## Contributing

- Star the repository
- Report issues
- Suggest improvements

---

## License

MIT License

---

<p align="center">
  <strong>cc10x v6.0.17</strong><br>
  <em>The Intelligent Orchestrator for Claude Code</em>
</p>
