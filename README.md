# cc10x

### Router-Owned Claude Code Harness

**Current version:** 10.1.16

**Recommended: Create `~/.claude/CLAUDE.md` (global) so the router is always active across all projects.**

<p align="center">
  <strong>1 Router</strong> &nbsp;•&nbsp; <strong>9 Agents</strong> &nbsp;•&nbsp; <strong>14 Skills</strong> &nbsp;•&nbsp; <strong>4 Workflows</strong>
</p>

<p align="center">
  <em>An opinionated Claude Code harness for developers who want routing, state, and verification to behave like engineering infrastructure.</em>
</p>

---

## Why cc10x

cc10x is for developers who like Claude Code, but do not want to babysit it.

It makes the coding loop behave more like a disciplined engineering system:

- one router entry point
- explicit workflows instead of ad-hoc prompting
- specialist agents instead of one overloaded assistant
- memory and workflow artifacts that survive long sessions
- evidence before advancement: LOG FIRST, RED → GREEN → REFACTOR, expected vs actual verification

The point is not "more AI". The point is tighter execution:

```text
You describe the job. cc10x decides the workflow, loads the right context,
brings in narrow specialists, and blocks weak "done" states.
```

---

## What cc10x Is

cc10x is a **developer-focused Claude Code harness** packaged as a marketplace plugin.

Its job is straightforward:
- take `PLAN`, `BUILD`, `DEBUG`, `REVIEW`, and `RESEARCH` requests and route them through a known execution model
- keep orchestration in one place: `cc10x-router`
- split execution across specialist subagents instead of a single general prompt
- persist enough workflow state to survive long sessions, compaction, and handoffs
- stay native to Claude Code primitives: `skills`, `subagents`, `hooks`, and optional user-configured MCP

Short mental model:

```text
cc10x = a thin orchestration layer on top of Claude Code
      + durable workflow state
      + specialist agents
      + guardrails that fail closed
```

It is not a hosted product, background daemon, or parallel control plane. It is a Claude Code plugin that makes normal coding sessions more deterministic.

## What You Get

With cc10x installed, Claude Code stops behaving like a single assistant session and starts behaving like a routed workflow:

- `PLAN` that resolves intent, constraints, scenarios, and default decisions before code starts
- `BUILD` that pushes implementation through RED → GREEN → REFACTOR, then review, then verification
- `DEBUG` that starts from logs and observed behavior instead of guess-and-patch loops
- `REVIEW` that is adversarial by design and reports only confidence-backed findings
- `VERIFY` that checks scenarios, artifacts, and wiring before anything is treated as complete
- `RESEARCH` that can use Octocode/Bright Data when present, but does not collapse if they are absent

This is one execution model, not a stack of unrelated prompts.

## What 10.1 adds

- **Decision-grade planning** with `direct`, `execution_plan`, and `decision_rfc` modes selected by the router
- **Fresh planning review loop** with a bounded read-only `plan-gap-reviewer` pass before final plan acceptance
- **Adversarial spec gates** that stop BUILD when feasibility, completeness, or alignment is weak
- **Proof-oriented BUILD** with explicit checkpoint types, expected artifacts, proof states, and no auto-advance on partial evidence
- **Stricter VERIFY** that checks truths, artifacts, and wiring before any pass verdict
- **Stable workflow UUIDs** and **versioned v10 state** under `.claude/cc10x/v10/`
- **Advisory internal skills** where explicit user/project standards always outrank CC10X pattern skills

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
- `plan-gap-reviewer`
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
.claude/cc10x/v10/workflows/{wf}.json
.claude/cc10x/v10/workflows/{wf}.events.jsonl
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

**You describe the work. cc10x routes it, brings in the right specialists, and keeps the bar for "done" higher than a convincing paragraph.**

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
| **BUILD** | build, implement, create, make, write, add | Clarify scope → TDD implementation → adversarial review → integration verification |
| **DEBUG** | debug, fix, error, bug, broken, troubleshoot | Reproduce from evidence → isolate cause → validate fix → prove no regression |
| **REVIEW** | review, audit, check, analyze, assess | High-signal review with confidence thresholds and file:line citations |
| **PLAN** | plan, design, architect, roadmap, strategy | Turn rough intent into an execution-ready plan with explicit decisions |

---

## Quick Start Examples

### Build Something
```
"build a user authentication system"

→ Router detects BUILD intent
→ Stops to resolve missing requirements first
→ component-builder drives RED → GREEN → REFACTOR
→ code-reviewer + silent-failure-hunter run in parallel
→ integration-verifier checks wiring, artifacts, and behavior
→ Workflow state and memory are updated
```

### Fix a Bug
```
"debug the payment processing error"

→ Router detects DEBUG intent
→ Loads prior failures and project memory
→ bug-investigator starts from logs and observed behavior
→ code-reviewer checks the fix path
→ integration-verifier confirms the bug is actually closed
→ Useful findings go back into memory
```

### Review Code
```
"review this PR for security issues"

→ Router detects REVIEW intent
→ code-reviewer uses repo and git context
→ Reports findings only when confidence clears the bar
→ Every finding includes file:line evidence
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

## The 9 Agents

| Agent | Purpose | Key Behavior |
|-------|---------|--------------|
| **component-builder** | Builds features | TDD: RED → GREEN → REFACTOR (no exceptions) |
| **bug-investigator** | Fixes bugs | LOG FIRST: Evidence before any fix |
| **code-reviewer** | Reviews code | Confidence ≥80%: No vague feedback |
| **silent-failure-hunter** | Finds error gaps | Zero tolerance for empty catch blocks |
| **integration-verifier** | E2E validation | Exit codes: PASS/FAIL with evidence |
| **planner** | Creates plans | Saves to `docs/plans/` + updates memory |
| **plan-gap-reviewer** | Fresh plan challenge pass | Read-only anti-anchoring review before final plan handoff |
| **web-researcher** | Fetches web data via Bright Data + WebSearch | Saves findings to file |
| **github-researcher** | Searches GitHub repos + packages via Octocode MCP | Saves findings to file |

---

## The 14 Skills

Skills are **loaded automatically by agents** or invoked directly when user-invocable.

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
| **building-cc10x** | USER-INVOCABLE | Reference repo analysis, DNA fingerprint, harmony integration pipeline |
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
| **v10.1.15** | Hook expansion: 4 audit-only hooks (PreCompact, Stop, StopFailure, InstructionsLoaded) for workflow state persistence and telemetry. 6→10 hook events. Zero blocking, zero context injection, router remains sole authority. |
| **v10.1.14** | Multi-repo harmony integration: 29 certified patterns from 11 reference repos via 3-phase harmony pipeline. Test tampering detection, claim extraction, environment escape hatches, analysis paralysis guards, near-miss negative testing, de-sloppify scans, plans-are-prompts principle, professional objectivity hard rules. |
| **v10.1.13** | Ruflo harmony integration: 29 prompt engineering edits across 16 files — research quality heuristics, multi-language silent-failure detection, friction-scan thresholds, rollback decision trees, plan completeness gates, behavioral TDD focus, partial-phase review scoping, abstraction thresholds, split-brain contradiction handling, evidence-before-reporting hard rules |
| **v10.1.12** | Prompt engineering uplift: 15 techniques from mattpocock/skills integrated across 13 files — durable decisions, tracer bullets, vertical-slice TDD, dependency taxonomy, HITL/AFK phases, opinionated review, friction scan, scope assessment, domain context injection |
| **v10.1.11** | DAG-visible PLAN review loop: the full bounded planning review chain is now pre-created in the task graph, with explicit branch pruning and `plan-gap-reviewer` restored to `gpt-5.4-mini` |
| **v10.1.10** | Always-on fresh planning review: every saved plan artifact now queues the bounded `plan-gap-reviewer` task before final plan handoff, with replay coverage locking it in |
| **v10.1.4** | Fresh planning review cleanup: raw user request passed to `plan-gap-reviewer`, lighter read-only reviewer contract, bounded pass counting fixed, docs/version surfaces refreshed |
| **v10.1.3** | Planning recovery: code-grounded plans, explicit plan-vs-code gap surfacing, stronger repo-aware plan review, and planning-specific replay coverage |
| **v10.1.2** | Trust-preserving latency instrumentation: verifier workload telemetry, phase-exit vs extended-audit classification, no proof-gating change |
| **v10.1.1** | Prompt-only hardening: sharper anti-false-completion wording, better trigger/description hygiene, reduced prompt dilution, no orchestration/runtime changes |
| **v10.1.0** | Competition-grade release: decision-grade planning, adversarial plan gates, proof-oriented BUILD, harsher VERIFY, and benchmark-backed prompt/harness hardening |
| **v10.0.0** | Trust-first recovery: agreement-first planning, phase-gated BUILD, stable workflow UUIDs, versioned v10 state, advisory internal skills |
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
