# cc10x

### Router-Owned Claude Code Harness

**Current version:** 9.1.1

**Recommended: Create `~/.claude/CLAUDE.md` (global) so the router is always active across all projects.**

<p align="center">
  <strong>1 Router</strong> &nbsp;•&nbsp; <strong>8 Agents</strong> &nbsp;•&nbsp; <strong>13 Skills</strong> &nbsp;•&nbsp; <strong>4 Workflows</strong>
</p>

<p align="center">
  <em>Orchestrated skills, specialist subagents, durable workflow state, and evidence-first execution for Claude Code.</em>
</p>

---

## Why cc10x

cc10x is what Claude Code should feel like for serious software work:

- one router entry point
- explicit workflows instead of ad-hoc prompting
- specialist agents instead of one overloaded assistant
- memory and workflow artifacts that survive long sessions
- evidence before advancement: LOG FIRST, RED → GREEN → REFACTOR, expected vs actual verification

If the short pitch matters:

```text
You provide intent. cc10x routes the workflow, loads the right context,
invokes the right specialists, and refuses to advance on weak evidence.
```

---

## What cc10x Is

cc10x is a **developer-focused Claude Code harness** packaged as a marketplace plugin.

It is designed for one specific job:
- route `PLAN`, `BUILD`, `DEBUG`, `REVIEW`, and `RESEARCH` work through a consistent workflow
- keep orchestration ownership in one place: `cc10x-router`
- use specialist subagents for execution, review, verification, and research
- persist enough state to resume safely after long sessions or compaction
- stay aligned with official Claude Code plugin conventions: `skills`, `subagents`, `hooks`, and optional user-configured MCP

If you want a short mental model:

```text
cc10x = router + workflow artifacts + specialist agents + minimal hooks
```

It is not a scheduler, background service, or external platform. It is a Claude Code plugin that makes the core engineering loop more reliable inside normal Claude Code sessions.

## What You Get

With cc10x installed, Claude Code gains:

- `PLAN` with intent-first planning, constraints, scenarios, and defaults
- `BUILD` with TDD-first implementation and post-build review/verification
- `DEBUG` with log-first investigation, regression proof, and research fallback
- `REVIEW` with adversarial review and confidence-based findings
- `VERIFY` with BDD-style scenario evidence and fail-closed advancement rules
- `RESEARCH` with optional Octocode/Bright Data acceleration and graceful fallback

This is still one coherent harness, not a bag of disconnected skills.

## What 9.1 adds

- **Intent-first planning** for complex work, with explicit goal, constraints, scenarios, and defaults
- **BDD-style evidence** across BUILD, DEBUG, and VERIFY using named scenarios with expected vs actual proof
- **DDD-style domain language preservation** so plans and scenarios use the product's real terms instead of invented abstractions
- **Proof-of-work workflow artifacts** under `.claude/cc10x/workflows/`
- **Plugin-native hooks and optional user-configured MCP** aligned with Claude Code plugin conventions
- **Built-in harness audit** for manifest/docs/router drift

---

## Runtime Model

### 1. Router owns orchestration

`cc10x-router` is the only orchestration authority.

It decides:
- which workflow to run
- which subagent to invoke next
- when to pause for clarification or scope decisions
- when remediation is required
- when a workflow is allowed to advance
- when memory and workflow artifacts are finalized

Agents do not own workflow state. They return structured results. The router interprets them.

### 2. Agents are narrow specialists

The shipped subagents are intentionally specialized:
- `planner`
- `component-builder`
- `bug-investigator`
- `code-reviewer`
- `silent-failure-hunter`
- `integration-verifier`
- `web-researcher`
- `github-researcher`

Each agent is optimized for one role. This keeps prompts sharper and makes workflow behavior easier to reason about.

### 3. Skills are reusable local instructions

Skills are the reusable instruction layer that agents and the router depend on.

They provide:
- planning patterns
- TDD rules
- debugging patterns
- review rules
- research synthesis
- memory handling
- verification-before-completion discipline

### 4. Workflow artifacts are the durable truth

cc10x writes proof-of-work workflow state under:

```text
.claude/cc10x/workflows/{wf}.json
.claude/cc10x/workflows/{wf}.events.jsonl
```

These artifacts track:
- workflow type and task ids
- intent/spec context
- agent results
- evidence and quality state
- remediation history
- lifecycle events

This is what makes resume, review, and debugging more reliable than relying on chat context alone.

### 5. Hooks are guardrails, not a second orchestrator

cc10x ships a minimal Claude Code-native hook set:
- `PreToolUse`
- `SessionStart`
- `PostToolUse`
- `TaskCompleted`

Hooks do not replace the router. They provide lightweight enforcement and diagnostics:
- protected file and workflow write checks
- resume context hydration
- workflow artifact integrity audit
- task metadata validation

This follows the official Claude Code pattern: hooks are small guardrails around tool use, not a parallel control plane.

### 6. MCP is optional acceleration only

cc10x does **not** ship MCP server config inside the plugin.

If the user already has Claude Code MCP servers named:
- `octocode`
- `brightdata`

then research gets better automatically.

If not, the plugin still works. Research falls back to built-in Claude Code tools and records degraded confidence where appropriate.

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

**You provide the development intent. cc10x selects the workflow, runs the right specialists, and enforces evidence before advancement.**

---

## Installation

### Step 1: Install Plugin

```bash
# Add marketplace
/plugin marketplace add romiluz13/cc10x

# Install plugin
/plugin install cc10x@romiluz13
```

### Step 2: Setup Config Files

Copy this README, paste it into Claude Code, and say: **"Set up cc10x for me"**

### Step 3: Restart Claude Code

Done!

---

## Claude Setup Instructions

This section is written for Claude Code to follow when the user says "set up cc10x for me".

**When user says "set up cc10x", "install cc10x", or similar:**

### Step 1: Check Existing Files
- Read `~/.claude/CLAUDE.md` (may not exist)
- Read `~/.claude/settings.json` (may not exist)

### Step 2: Update `~/.claude/CLAUDE.md`

**If file doesn't exist:** CREATE with the template below.
**If file exists:** PREPEND the cc10x section below, keep user's existing content.

> **Multi-project note:** The global `~/.claude/CLAUDE.md` activates cc10x in **every** project automatically — you do not need to reinstall or reconfigure per project. Only add the cc10x section to a project's `.claude/CLAUDE.md` if that project has its own conflicting CLAUDE.md already.

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

[CC10x]|entry: cc10x:cc10x-router

---

## Complementary Skills (Work Together with CC10x)

**Skills are additive, not exclusive.** CC10x provides orchestration. Domain skills provide expertise. Both work together.

**GATE:** Before writing code, check if task matches a skill below. If match, invoke it via `Skill(skill="...")`.

| When task involves... | Invoke |
|-----------------------|--------|
| *(Add user's installed skills here)* | |
```

### Step 3: Update `~/.claude/settings.json`

**If file doesn't exist:** CREATE with the template below.
**If file exists:** MERGE these permissions into the existing `permissions.allow` array (don't overwrite!):

```json
"Bash(mkdir -p .claude/cc10x)",
"Bash(mkdir -p docs/plans)",
"Bash(mkdir -p docs/research)",
"Bash(git status)",
"Bash(git diff:*)",
"Bash(git log:*)",
"Bash(git branch:*)",
"Edit(.claude/cc10x/*)",
"Write(.claude/cc10x/*)"
```

> **Why the Edit/Write permissions?** cc10x memory files (`activeContext.md`, `patterns.md`, `progress.md`) live in `.claude/cc10x/`. Without these lines, Claude Code will prompt you for permission on every memory write. Adding them pre-approves edits to that folder only.

### Step 4: Set User Standards (Optional)

Ask the user:
> "Do you have coding standards or principles you want cc10x agents to always follow? (e.g. 'always use TypeScript strict mode', 'follow SOLID principles', 'never use `any`', 'prefer functional patterns')"

**If user provides standards**, write them to the project's memory:
```
Bash(command="mkdir -p .claude/cc10x")
# Check if patterns.md already exists (Read returns error = doesn't exist)
Read(file_path=".claude/cc10x/patterns.md")

# If it DOESN'T exist — create with standards already populated:
Write(file_path=".claude/cc10x/patterns.md", content="# Project Patterns\n<!-- CC10X MEMORY CONTRACT: Do not rename headings. Used as Edit anchors. -->\n\n## User Standards\n- {standard 1}\n- {standard 2}\n\n## Architecture Patterns\n\n## Code Conventions\n\n## Common Gotchas\n\n## Last Updated\n{date}")

# If it DOES exist — append under User Standards:
Edit(file_path=".claude/cc10x/patterns.md",
     old_string="## User Standards",
     new_string="## User Standards\n- {standard 1}\n- {standard 2}")

Read(file_path=".claude/cc10x/patterns.md")  # Verify
```

**If user skips:** No action. The memory file will be created on first workflow run with an empty `## User Standards` section for them to fill in later.

### Step 5: Scan Installed Skills & Add to Table

**Where to find installed skills:**
1. `~/.claude/settings.json` → check `enabledPlugins` object (plugins with value `true`)
2. `~/.claude/plugins/installed_plugins.json` → detailed plugin info
3. `~/.claude/skills/` → personal skills (all projects)
4. `.claude/skills/` → project-specific skills

**Skill naming in table:**
- **Plugin skills:** `plugin-name:skill-name` (e.g., `mongodb-agent-skills:mongodb-schema-design`)
- **Personal/project skills:** just the skill name (e.g., `react-best-practices`)

**Example:** If user has these:
```
# In enabledPlugins:
"mongodb-agent-skills@mongodb-agent-skills": true

# In ~/.claude/skills/:
react-best-practices/SKILL.md
```

**Add to the Complementary Skills table:**
```markdown
| When task involves... | Invoke |
|-----------------------|--------|
| MongoDB, schema, queries | `mongodb-agent-skills:mongodb-schema-design` |
| React, Next.js, UI | `react-best-practices` |
```

### Step 6: Confirm
> "cc10x is set up! Please restart Claude Code to activate."

---

## The 4 Workflows

| Intent | Trigger Words | What Happens |
|--------|---------------|--------------|
| **BUILD** | build, implement, create, make, write, add | TDD cycle → Code review → Silent failure hunt → Integration verify |
| **DEBUG** | debug, fix, error, bug, broken, troubleshoot | Log-first investigation → Review fix → Verify works |
| **REVIEW** | review, audit, check, analyze, assess | Multi-dimensional review with 80%+ confidence scoring |
| **PLAN** | plan, design, architect, roadmap, strategy | Comprehensive planning with external research |

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

WORKFLOW STATE (.claude/cc10x/workflows/)
├── {wf}.json         ◄── Durable workflow artifact
└── {wf}.events.jsonl ◄── Append-only workflow event log
```

---

## The 8 Agents

| Agent | Purpose | Key Behavior |
|-------|---------|--------------|
| **component-builder** | Builds features | TDD: RED → GREEN → REFACTOR (no exceptions) |
| **bug-investigator** | Fixes bugs | LOG FIRST: Evidence before any fix |
| **code-reviewer** | Reviews code | Confidence ≥80%: No vague feedback |
| **silent-failure-hunter** | Finds error gaps | Zero tolerance for empty catch blocks |
| **integration-verifier** | E2E validation | Exit codes: PASS/FAIL with evidence |
| **planner** | Creates plans | Saves to `docs/plans/` + updates memory |
| **web-researcher** | Fetches web data via Bright Data + WebSearch | Saves findings to file |
| **github-researcher** | Searches GitHub repos + packages via Octocode MCP | Saves findings to file |

---

## The 13 Skills

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
| **plan-review-gate** | planner | Final plan sanity gate before handoff |
| **research** | planner, bug-investigator (via github-researcher agent) | Synthesis-only: guides agents on how to interpret research results; GitHub execution is handled by the `github-researcher` agent |
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
- **Router-owned advancement**: only the router decides whether a workflow can continue

---

## Hooks

The plugin ships four Claude Code-native hooks:

| Hook | Purpose |
|------|---------|
| `PreToolUse` | Guard protected files and workflow-owned writes |
| `SessionStart` | Rehydrate workflow context after restart or compaction |
| `PostToolUse` | Audit workflow artifact integrity after writes |
| `TaskCompleted` | Validate CC10X task metadata before task completion |

These hooks are intentionally minimal. They improve reliability without turning the plugin into a second runtime.

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
| **v9.1.1** | Removed shipped MCP config to avoid startup warnings; MCP research remains optional via user-configured Claude Code MCP servers named `brightdata` and `octocode` |
| **v9.1.0** | Publication polish: intent-first planning, BDD-style scenario evidence, DDD-style domain language preservation, proof-of-work workflow artifacts, built-in harness drift audit |
| **v9.0.0** | Plugin-native packaging: bundled Claude Code hooks, optional plugin MCP acceleration, router-owned research quality model, workflow artifacts as durable truth |
| **v8.5.0** | Fix 1: READ-ONLY task completion as explicit mandatory gate (3-GATE). Fix 2b: CRITICAL+HIGH scope question via text (Rule 1a-SCOPE + Scope Decision Resume + scope-aware re-hunt) |
| **v8.0.0** | Radical simplification — remove Router Contract YAML from read-only agents; text-based verdict extraction; JUST_GO session mode; ~280 lines removed |
| **v7.9.0** | OBS-2/3/4/6/7/8/10/11/12/13/14 batch fix — self-healing verifier, explicit DEBUG-RESET marker, conditional frontend-patterns load |
| **v7.8.0** | OBS-1/9/15/16/DEBUG-RESET — 5-issue fix, 13/13 smoke test pass |
| **v6.0.21** | User standards support; multi-project docs; Linux install troubleshooting |
| **v6.0.20** | Agent self-report task completion; MCP docs; permissions fix for memory files |
| **v6.0.19** | Babysitter-inspired: Multi-signal HARD/SOFT scoring, evidence arrays, decision checkpoints, completion guard |
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

- **v8.0.0** - Radical Simplification: Removed Router Contract YAML from code-reviewer, silent-failure-hunter, integration-verifier. Replaced ~200-line YAML validation block in router with 30-line text extraction (reads heading from first 5 lines). Added JUST_GO session mode (AUTO_PROCEED flag). Simplified Empty Answer Guard — only ⚠️ REVERT gates block; all others auto-default. Removed REM-EVIDENCE retry loop (root cause of 6/6 stress test failures). Net: ~280 lines removed, 0 new complexity.
- **v7.9.0** - OBS-2/3/4/6/7/8/10/11/12/13/14 batch fix: self-healing integration-verifier (creates REM-FIX + blocks own task), explicit DEBUG-RESET marker written by router, conditional frontend-patterns load (.tsx/.jsx/.vue/.css/.scss/.html only)
- **v7.8.0** - OBS-1/9/15/16/DEBUG-RESET 5-issue fix, 13/13 smoke test pass
- **v6.0.19** - Babysitter-inspired enhancements: Multi-signal HARD/SOFT scoring (per-dimension review), evidence array protocol (structured proof), decision checkpoints (mandatory pause points), completion guard (final gate before Router Contract)
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
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   └── hooks.json
├── scripts/
│   ├── cc10x_harness_audit.py
│   ├── cc10x_hooklib.py
│   ├── cc10x_posttooluse_artifact_guard.py
│   ├── cc10x_pretooluse_guard.py
│   ├── cc10x_sessionstart_context.py
│   ├── cc10x_task_completed_guard.py
│   └── cc10x_workflow_replay_check.py
├── tests/
│   └── fixtures/
├── agents/
│   ├── component-builder.md
│   ├── bug-investigator.md
│   ├── code-reviewer.md
│   ├── integration-verifier.md
│   ├── planner.md
│   ├── silent-failure-hunter.md
│   ├── web-researcher.md
│   └── github-researcher.md
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
    ├── research/SKILL.md
    └── verification-before-completion/SKILL.md
```

Additional developer docs live under:

```text
docs/cc10x-orchestration-bible.md
docs/cc10x-orchestration-logic-analysis.md
docs/cc10x-orchestration-safety.md
docs/router-invariants.md
```

If you need to understand or evolve the harness, start there after reading `cc10x-router`.

---

## Optional MCP Integrations

cc10x works out of the box with no MCPs required. These are **optional** — they unlock specific features when installed in your own Claude Code MCP settings.

| MCP | Feature Unlocked | How to Install |
|-----|-----------------|----------------|
| **[octocode](https://github.com/nicepkg/octocode)** | GitHub research: find packages, search code across repos, read PR history. Triggered automatically when planner or bug-investigator needs external research. | Install via Claude Code MCP settings using the server name `octocode` |
| **[brightdata](https://github.com/nicepkg/mcp-brightdata)** | Web scraping for research tasks — used as fallback when web content is needed beyond GitHub. | Install via Claude Code MCP settings using the server name `brightdata` |

**Important:** CC10X no longer ships MCP server config inside the plugin. This avoids startup warnings for users who do not have Bright Data or Octocode credentials configured.

**Without these MCPs:** cc10x still works fully. The research agents degrade to built-in Claude Code tools and note the lower-confidence path in their outputs.

**With octocode installed:** When the router detects new/unfamiliar tech, 3+ failed debug attempts, or explicit research requests, it automatically calls octocode tools to search GitHub before invoking the planner or bug-investigator.

---

## Troubleshooting

### Claude Code keeps asking for permission to edit memory files

Add these two lines to `~/.claude/settings.json` under `permissions.allow`:

```json
"Edit(.claude/cc10x/*)",
"Write(.claude/cc10x/*)"
```

Or run **"Set up cc10x for me"** again — the setup wizard adds them automatically.

---

### cc10x not activating in a specific project

The global `~/.claude/CLAUDE.md` activates cc10x in every project — you only need one install. If it's not activating in a specific project:

1. **Check if that project has its own `.claude/CLAUDE.md`** — open it and verify the cc10x section is present. If the project-level file exists but doesn't have the cc10x entry, add it there.
2. **Verify the entry format** — use `[CC10x]|entry: cc10x:cc10x-router` (plugin reference). A relative path like `./plugins/cc10x/...` only works in the cc10x repo itself, not in your projects.
3. **Restart Claude Code** — the plugin system requires a restart after any CLAUDE.md change.

---

### Ubuntu / Linux install error: EXDEV cross-device link

If you see:
```
Error: Failed to install: EXDEV: cross-device link not permitted
```

This is a Linux filesystem issue — `/tmp` and your home directory are on different filesystems, so the installer can't `rename()` across them. Fix:

```bash
# Set TMPDIR to a directory on the same filesystem as your home:
mkdir -p ~/.claude/tmp
TMPDIR=~/.claude/tmp claude
# Then install normally: /plugin install cc10x@romiluz13
```

If that doesn't work, install manually:
```bash
# Clone directly into the plugins directory
git clone https://github.com/romiluz13/cc10x.git ~/.claude/plugins/cc10x
```
Then follow Step 2 in the setup guide above to add the cc10x entry to `~/.claude/CLAUDE.md`.

---

### "Unknown skill cc10x:cc10x-router"

The cc10x plugin is disabled. Run:
```
/plugins enable cc10x
```
Then retry your command.

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
  <strong>cc10x v8.3.0</strong><br>
  <em>The Intelligent Orchestrator for Claude Code</em>
</p>
