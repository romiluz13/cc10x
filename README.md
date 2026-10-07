<p align="center">
  <img src="assets/logo.png" alt="CC10x — The Loop Engine for Claude Code. Orange stylized X with starburst and CC10x wordmark." width="280" />
</p>

<h1 align="center">cc10x — The Loop Engine for Claude Code</h1>

<p align="center">
  <em>Same model. Same Claude Code. Different outcome.</em>
</p>

<p align="center">
  The agent forgets between turns. <strong>The harness remembers across runs.</strong><br />
  cc10x writes every workflow to disk — intent, evidence, verdicts, failures — so resume, review, and verification read from the artifact, not from a context window that's already gone.
</p>

<p align="center">
  <strong>1 router</strong> &nbsp;·&nbsp; <strong>14 specialist agents</strong> &nbsp;·&nbsp; <strong>21 skills</strong> &nbsp;·&nbsp; <strong>8 workflows</strong>
</p>

<p align="center">
  Fail-closed gates &nbsp;·&nbsp; survives compaction &nbsp;·&nbsp; dispatch-by-reference &nbsp;·&nbsp; test honesty gates &nbsp;·&nbsp; anti-anchored review
</p>

**Current version:** 12.10.0

---

## Install

cc10x needs **Python 3.9 or newer** on `PATH` (3.13 is the version the test suite runs on): every hook except the preflight is a `python3` script. A SessionStart preflight tells the agent when `python3` is missing or too old.

**Step 1 — Add the marketplace** (once per machine):

```bash
claude plugin marketplace add romiluz13/cc10x
```

**Step 2 — Install the plugin:**

```bash
claude plugin install cc10x@cc10x
```

Inside a Claude Code session the same two steps are `/plugin marketplace add romiluz13/cc10x` and `/plugin install cc10x@cc10x`.

Then say **"set up cc10x for me"** in Claude Code and restart. Done.

### Update

```bash
claude plugin update cc10x@cc10x --scope user
```

Use the scope you installed at (`user`, `project`, `local` or `managed`). Then run `/reload-plugins` in an open session, or restart Claude Code.

**Auto-update is off by default for third-party marketplaces** such as `romiluz13/cc10x`, so a new release does not arrive on its own. Either update by hand as above, or open `/plugin`, go to the **Marketplaces** tab, select the marketplace and choose **Enable auto-update**.

### Manual install from a clone

```bash
git clone https://github.com/romiluz13/cc10x.git
claude --plugin-dir "$PWD/cc10x/plugins/cc10x"
```

`--plugin-dir` loads the plugin for that one session only. Skills are then namespaced `cc10x:<skill>`, and the router is `cc10x:cc10x-router`.

### Recommended environment variables

| Variable | Why |
| --- | --- |
| `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` | Claude Code ships its task tools by default only on some models. cc10x works without them (it falls back to tracking the graph in the workflow artifact) but this restores them on every model. |
| `CLAUDE_CODE_TASK_LIST_ID` (optional) | Shares one task list across sessions. |
| `CLAUDE_CONFIG_DIR` (optional) | Moves Claude Code's configuration directory off `~/.claude`. Wherever this README says `~/.claude`, read `$CLAUDE_CONFIG_DIR`. |
| `CLAUDE_CODE_PLUGIN_CACHE_DIR` (optional) | Moves the plugins root off `~/.claude/plugins`. |

### Keep `.cc10x/` out of git

cc10x writes memory and workflow state under `.cc10x/` in each project. It is session state, not source, so gitignore `.cc10x/` in each project: add the line `.cc10x/` to its `.gitignore`. How it relates to Claude Code's own memory is under [Memory Persistence](#memory-persistence).

---

## Quick Start Examples

### Build Something

```
"build a user authentication system"

→ Router detects BUILD intent
→ Stops to resolve missing requirements first
→ component-builder drives RED → GREEN → REFACTOR
→ code-reviewer + failure-hunter run in parallel
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

### Test a Feature

```
"write an end-to-end test plan for checkout and run it"

→ Router detects QA intent
→ qa-researcher agents survey the code, specs and tickets, one source each
→ A test plan is reviewed by plan-gap-reviewer before anything is built
→ qa-harness-builder provisions the environment
→ code-reviewer + failure-hunter check the harness
→ qa-executor runs the plan and fills in the report
```

---

## Why cc10x

Ask Claude for something complex. It works for a while. Then it declares **"Done!"** — tests still red, refactor half-finished, and by message 40 it's contradicting itself because the context is gone.

**cc10x fixes the loop, not the prompt.** The same model, constrained and looped correctly, does better than the same model running free. That's the whole bet.

| The pain you know | How cc10x handles it |
| --- | --- |
| "Done!" on red tests | `integration-verifier` is independent of the builder. Phase-exit gates block advancement on partial evidence. |
| Silent failures nobody asked about | `failure-hunter` runs in parallel with review — greps for swallowed errors and empty catches. |
| Context falls apart after compaction | Workflow state on disk with stable UUIDs. Memory files the router auto-heals. |
| Planning is just a chat | Three planning modes chosen by intent, with a fresh anti-anchored review by a reviewer who never saw the planner's rationale. |
| 12 slash commands to remember | One router. Every request hits `cc10x-router` first. |
| `.claude/` prompt spam on every fanout | State lives at `.cc10x/` — outside `.claude/`, so the harness's sensitive-file gate never fires. |
| Green tests that prove nothing | Test Honesty Gates grep for `getByTestId('…-mock')`, `as any`, `.find()` bypass, `setTimeout()` waits. A hit can't count as PASS on that test's strength alone. |
| Reviewer findings that sound right but aren't | Every finding at confidence ≥80 needs a verbatim `file:line` quote or it's auto-demoted. The verifier independently re-reads the line and drops hallucinated findings before they can gate. |
| Orchestrator context rotting with pasted history | Dispatch by reference, not by blob — the diff is written to disk, the prompt passes a path, never a body. (One real dispatch hit 42k chars, 99% pasted history. The scar became law.) |

---

## How It Works

**You describe the work. cc10x routes it, brings in the right specialists, and keeps the bar for "done" higher than a convincing paragraph.**

```
                               YOU
                                │
                                ▼
                   ┌────────────────────────┐
                   │      cc10x-router      │  ◄── only entry point
                   │   detects intent       │
                   └────────────┬───────────┘
                                │
   ┌────────┬────────┬──────────┼───────┬───────┬────────┬──────────────────┐
   ▼        ▼        ▼          ▼       ▼       ▼        ▼                  ▼
 DEBUG     PLAN    REVIEW     ORIENT    QA    TRIAGE  CODEBASE-          BUILD
                                                      HEALTH          (the default)

   Each workflow is a chain of the specialist agents. The full table is below.

                 ┌──────────────────────────┐
                 │  STATE (every workflow)  │
                 │  activeContext.md        │
                 │  patterns.md             │
                 │  progress.md             │
                 │  {wf}.json + .events     │
                 └──────────────────────────┘
```

---

## The 8 Workflows

The router picks the workflow from the request's primary deliverable. When more than one fits, the lower priority number wins; anything that matches no other row is BUILD.

| Priority | Workflow | Trigger words | What happens |
| --- | --- | --- | --- |
| 1 | **DEBUG** | error, bug, fix, broken, crash, debug | Reproduce from evidence → isolate cause → validate fix → prove no regression (`bug-investigator` → `code-reviewer` → `integration-verifier`) |
| 2 | **PLAN** | plan, design, architect, roadmap, spec, brainstorm | Turn rough intent into an execution-ready plan with explicit decisions, then a bounded fresh review (`planner` → `plan-gap-reviewer`) |
| 3 | **REVIEW** | review, audit, analyze, assess | High-signal review with confidence thresholds and file:line citations (`code-reviewer`). Advisory only: never creates code-changing tasks |
| 4 | **ORIENT** | zoom out, explain, "how does X work", "walk me through" | Read-only orientation answered inline: no agents, no phase graph, no writes |
| 5 | **QA** | test, QA, e2e, integration test, test plan, regression | Testing the code is the deliverable: survey → test plan → plan review → environment → execution (`qa-researcher` ×N → `plan-gap-reviewer` → `qa-harness-builder` → `qa-executor`) |
| 6 | **TRIAGE** | triage, "incoming issues" | Categorize and verify incoming issues or PRs and write agent-ready briefs (`triage-agent`). Advisory only |
| 7 | **CODEBASE-HEALTH** | codebase health, deepening, shallow modules | Scan for deepening candidates and produce an HTML report (`architecture-scanner`). Advisory only |
| 8 | **BUILD** | build, implement, create, add (and everything else) | Clarify scope → TDD implementation → adversarial review → integration verification (`component-builder` → `code-reviewer` ∥ `failure-hunter` → `integration-verifier`) |

The router file is the source of truth for the table: [`plugins/cc10x/skills/cc10x-router/SKILL.md`](plugins/cc10x/skills/cc10x-router/SKILL.md), section 1.

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

IMPORTANT: For multi-step development work (build, debug, review, plan), do minimal orientation first, then invoke cc10x-router before planning, implementation, review, or code changes.
IMPORTANT: Minimal orientation means only the nearest project instructions, manifest, and immediate target surface. Do not do broad exploration before routing.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: The router is the default for multi-step development work. Route write-heavy BUILD/DEBUG work through it; the router's fail-closed gates and durable artifacts are the value. A small edit still routes: the router runs a single trivial change as BUILD with trivial scope (a reduced task graph that keeps the verifier's proof path), and anything that spans files, has separable concerns, or changes a contract gets the full chain.

Precedence (highest first): explicit user instructions > project standards (CLAUDE.md / repo conventions) > approved plans and design docs > domain-specific skills > cc10x internal skills > router defaults. The router enforces quality; it does not override the user.

**Skip CC10x ONLY when:**
- User EXPLICITLY says "don't use cc10x", "without cc10x", or "skip cc10x"
- No interpretation. No guessing. Only these exact opt-out phrases.

The router is the plugin skill `cc10x:cc10x-router`.

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
"Bash(mkdir -p .cc10x)",
"Bash(mkdir -p .cc10x/)",
"Bash(mkdir -p docs/plans)",
"Bash(mkdir -p docs/research)",
"Bash(mkdir -p docs/solutions)",
"Bash(git status)",
"Bash(git diff:*)",
"Bash(git log:*)",
"Bash(git branch:*)",
"Bash(git blame:*)",
"Bash(git ls-files:*)",
"Bash(git rev-parse:*)",
"Bash(python3:*)",
"Edit(.cc10x/**)"
```

> **What `Edit(.cc10x/**)` does.** It pre-approves file edits under `.cc10x/` at any depth, so memory files, workflow artifacts and QA files stop prompting on every write. Claude Code applies an `Edit(...)` rule to every file-editing tool, `Write` included, so one rule covers both; a `Write(.cc10x/*)` allow rule does nothing (Claude Code warns that only `Edit(...)` rules are matched), which is why this template no longer has one. Claude Code drops a project's `permissions.allow` entries until you trust the workspace, so put the rule in your user settings or trust the folder first.

> **What the `Bash` rules do.** The `mkdir -p` rules create fixed directories (a rule matches the command text exactly, so `.cc10x` and `.cc10x/` are two rules) and the `git` rules read repository state (`git branch:*` also lets Claude create branches; the git guard hook still denies pushes and forced deletes). `Bash(python3:*)` is broad: it approves any `python3` command, not just cc10x's tools. It is in the template because every BUILD phase records its base SHA (`git rev-parse HEAD`) and the router builds review diff packages and phase briefs by running plugin tools via `python3`; without it, every phase prompts mid-workflow. If you do not want to pre-approve every `python3` command, drop that rule and approve the plugin's `python3` calls when prompted.

### Step 4: Set User Standards (Optional)

Ask the user:
> "Do you have coding standards or principles you want cc10x agents to always follow? (e.g. 'always use TypeScript strict mode', 'follow SOLID principles', 'never use `any`', 'prefer functional patterns')"

**If user provides standards**, write them to the project's memory:

```
Bash(command="mkdir -p .cc10x")
# Check if patterns.md already exists (Read returns error = doesn't exist)
Read(file_path=".cc10x/patterns.md")

# If it DOESN'T exist — create with standards already populated:
Write(file_path=".cc10x/patterns.md", content="# Project Patterns\n<!-- CC10X MEMORY CONTRACT: Do not rename headings. Used as Edit anchors. -->\n\n## User Standards\n- {standard 1}\n- {standard 2}\n\n## Common Gotchas\n\n## Project SKILL_HINTS\n\n## Last Updated\n{date}")

# If it DOES exist — append under User Standards:
Edit(file_path=".cc10x/patterns.md",
     old_string="## User Standards",
     new_string="## User Standards\n- {standard 1}\n- {standard 2}")

Read(file_path=".cc10x/patterns.md")  # Verify
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
>
> "cc10x is set up! Please restart Claude Code to activate."

---

## Memory Persistence

cc10x survives context compaction. This is critical for long sessions.

```
.cc10x/
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

The live namespace is `.cc10x/` (memory `.cc10x/*.md`, workflow state `.cc10x/workflows/*`). Two legacy residue locations are ignored by current router hydration if present: `.claude/cc10x/` (pre-10.1.20, before the workflow state moved out of `.claude/` to escape the harness sensitive-file gate) and the version-segmented `.cc10x/v10/` layout (v10.x, before the namespace was de-versioned in v11). cc10x does not migrate either; a fresh `.cc10x/` is created on first use.

**Iron Law:** Every workflow loads memory at START and updates at END.

### How `.cc10x/` relates to Claude Code auto-memory

They are separate systems and neither replaces the other.

- **`.cc10x/` (cc10x memory):** per-project files that cc10x's router and agents read at the start and write at the end of each workflow, plus the workflow artifacts and event logs. They hold this project's task context, conventions and progress, and they live in the project directory.
- **Claude Code auto-memory:** notes Claude Code itself keeps for you across conversations, stored under your Claude configuration directory (`~/.claude`, or `$CLAUDE_CONFIG_DIR`), outside the project. cc10x neither reads nor writes it.

Use auto-memory for preferences that follow you across projects, and `.cc10x/` for what one project's workflows need to resume. Keep `.cc10x/` out of git, as above.

---

## Optional MCP Integrations

cc10x works out of the box with no MCPs required. These are **optional** — they unlock specific features when installed in your own Claude Code MCP settings.

| MCP | Feature Unlocked | How to Install |
| ----- | ----------------- | ---------------- |
| **[octocode](https://github.com/bgauryy/octocode-mcp)** | GitHub research: find packages, search code across repos, read PR history. Triggered automatically when planner or bug-investigator needs external research. | Install via Claude Code MCP settings using the server name `octocode` |
| **[brightdata](https://github.com/brightdata/brightdata-mcp)** | Web scraping for research tasks — used as fallback when web content is needed beyond GitHub. | Install via Claude Code MCP settings using the server name `brightdata` |

**Important:** CC10X no longer ships MCP server config inside the plugin. This avoids startup warnings for users who do not have Bright Data or Octocode credentials configured.

**Without these MCPs:** cc10x still works fully. The research agents degrade to built-in Claude Code tools and note the lower-confidence path in their outputs.

**With octocode installed:** When the router detects new/unfamiliar tech, 3+ failed debug attempts, or explicit research requests, it automatically calls octocode tools to search GitHub before invoking the planner or bug-investigator.

---

## Troubleshooting

### Claude Code keeps asking for permission to edit memory files

Add this line to `~/.claude/settings.json` under `permissions.allow`:

```json
"Edit(.cc10x/**)"
```

It covers the live `.cc10x/` namespace at any depth (see Step 3 of the setup instructions for what it does and why there is no `Write(...)` rule).

Or run **"Set up cc10x for me"** again — the setup wizard adds them automatically.

---

### cc10x asks for permission before writing plan/research docs

Working as intended. `.cc10x/` orchestration state is pre-permitted, but outward-facing project artifacts (`docs/plans/`, `docs/research/`, `docs/solutions/`) prompt for approval by design — trust-first friction, not missing configuration. Approve the write to continue.

---

### cc10x not activating in a specific project

The global `~/.claude/CLAUDE.md` activates cc10x in every project — you only need one install. If it's not activating in a specific project:

1. **Check if that project has its own `.claude/CLAUDE.md`** — open it and verify the cc10x section is present. If the project-level file exists but doesn't have the cc10x entry, add it there.
2. **Verify the router reference** — the CLAUDE.md section names the plugin skill `cc10x:cc10x-router`. A relative path like `plugins/cc10x/skills/cc10x-router/SKILL.md` only resolves inside the cc10x repo itself, not in your projects.
3. **Restart Claude Code** — or run `/reload-plugins` after a plugin change. A CLAUDE.md change is read on the next session start.
4. **Check Python** — if the session start printed a CC10X python warning, the hooks are silently off until Python 3.9 or newer is on `PATH`.

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
# Then install normally: /plugin install cc10x@cc10x
```

If that doesn't work, use the clone-and-`--plugin-dir` route from [Manual install from a clone](#manual-install-from-a-clone), then follow Step 2 in the setup guide above to add the cc10x section to `~/.claude/CLAUDE.md`.

---

### "Unknown skill cc10x:cc10x-router"

The cc10x plugin is not installed or is disabled. Check with:

```bash
claude plugin list
```

If it is listed as disabled, run `claude plugin enable cc10x@cc10x` (or open `/plugin` and use the **Installed** tab), then `/reload-plugins`.

---

## Architecture Deep Dive

Everything below the fold: how the loop actually works. For contributors and the curious — you do not need any of this to use cc10x.

<details>
<summary><strong>Runtime model, router kernel, agents, skills, hooks, diagrams, file layout</strong></summary>

### Runtime Model

#### 1. Router owns orchestration

`cc10x-router` is the only orchestration authority.

The router uses a **kernel + mandatory reference** shape:

- universal orchestration law stays inline in `cc10x-router/SKILL.md`
- workflow-specific playbooks and appendix-heavy artifact/remediation law live in `cc10x-router/references/*.md`
- the kernel explicitly tells Claude which reference must be read before BUILD / DEBUG / REVIEW / PLAN / QA / TRIAGE / CODEBASE-HEALTH branch logic continues

That keeps orchestration salient without turning the router into a context dump.

It decides:

- which workflow to run
- which subagent to invoke next
- when to pause for clarification or scope decisions
- when remediation is required
- when a workflow is allowed to advance
- when memory and workflow artifacts are finalized

Agents do not own workflow state. They return structured results. The router interprets them.

#### 2. Agents are narrow specialists

The 14 shipped subagents are intentionally specialized; the table under [The 14 Agents](#the-14-agents) lists each one. Each agent is optimized for one role. This keeps prompts sharper and makes workflow behavior easier to reason about.

#### 3. Skills are reusable local instructions

Skills are the reusable instruction layer that agents and the router depend on.

They provide:

- planning patterns
- TDD rules
- debugging patterns
- review rules
- research synthesis
- memory handling
- verification-before-completion discipline
- test-system design for the QA workflow

#### 4. Workflow artifacts are the durable truth

cc10x writes proof-of-work workflow state under:

```text
.cc10x/workflows/{wf}.json
.cc10x/workflows/{wf}.events.jsonl
```

These artifacts track:

- workflow type and task ids
- intent/spec context
- agent results
- evidence and quality state
- remediation history
- lifecycle events

The QA workflow also keeps its test plan, environment plan and report under `.cc10x/qa/`. This is what makes resume, review, and debugging more reliable than relying on chat context alone.

#### 5. Hooks are guardrails, not a second orchestrator

Hooks do not replace the router. They provide lightweight enforcement and diagnostics. Most of them only audit; the git guard and the QA isolation guard always deny. The table under [Hooks](#hooks) lists the registered events, and [`plugins/cc10x/hooks/README.md`](plugins/cc10x/hooks/README.md) is the one place that says exactly what each hook does and which can block.

#### 6. MCP is optional acceleration only

cc10x does **not** ship MCP server config inside the plugin.

If the user already has Claude Code MCP servers named:

- `octocode`
- `brightdata`

then research gets better automatically.

If not, the plugin still works. Research falls back to built-in Claude Code tools and records degraded confidence where appropriate.

---

### BUILD flow, up close

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   YOU: "build a user auth system"                                            │
│                                     ┌────────────────────────────────────┐   │
│                              ┌─────►│  component-builder                 │   │
│                              │      │  + TDD enforcement                 │   │
│   ┌────────────────────┐     │      │  + building and verification       │   │
│   │                    │     │      │    skills                          │   │
│   │   cc10x-router     │─────┤      └──────────────┬─────────────────────┘   │
│   │   (auto-detects    │     │                     │                         │
│   │    BUILD intent)   │     │      ┌──────────────▼─────────────────────┐   │
│   │                    │     │      │  code-reviewer ∥ failure-hunter    │   │
│   └────────────────────┘     │      │  (parallel execution)              │   │
│                              │      └──────────────┬─────────────────────┘   │
│                              │                     │                         │
│                              │      ┌──────────────▼─────────────────────┐   │
│                              └─────►│  integration-verifier              │   │
│                                     │  + E2E validation                  │   │
│                                     └────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

A trivial change (one file group, one failure mode) runs a reduced graph: `component-builder` → `integration-verifier`. The reviewer and hunter join when the work spans files or the builder reports scope growth.

---

### Architecture

```
USER REQUEST
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    cc10x-router (ONLY ENTRY POINT)              │
│              Detects intent → Routes to workflow                │
└─────────────────────────────────────────────────────────────────┘
     │
     ├── DEBUG ──► bug-investigator ──► code-reviewer ──► integration-verifier
     │
     ├── PLAN ───► exploration ──► planner ──► plan-gap-reviewer (bounded loop)
     │
     ├── REVIEW ─► code-reviewer
     │
     ├── ORIENT ─► inline orientation (no agents)
     │
     ├── QA ─────► qa-researcher (fan-out) ──► plan-gap-reviewer ──► qa-harness-builder
     │              ──► [code-reviewer ∥ failure-hunter] ──► qa-executor
     │
     ├── TRIAGE ─► triage-agent
     │
     ├── CODEBASE-HEALTH ─► architecture-scanner
     │
     └── BUILD ──► component-builder ──► [code-reviewer ∥ failure-hunter] ──► integration-verifier

MEMORY (.cc10x/)
├── activeContext.md  ◄── Current focus, decisions, learnings
├── patterns.md       ◄── Project conventions, common gotchas
└── progress.md       ◄── Completed work, remaining tasks

WORKFLOW STATE (.cc10x/workflows/)
├── {wf}.json         ◄── Durable workflow artifact
└── {wf}.events.jsonl ◄── Append-only workflow event log
```

---

### The 14 Agents

| Agent | Purpose | Key Behavior |
| ------- | --------- | -------------- |
| **component-builder** | Builds features | TDD: RED → GREEN → REFACTOR (no exceptions) |
| **bug-investigator** | Fixes bugs | LOG FIRST: Evidence before any fix |
| **code-reviewer** | Reviews code | Confidence ≥80%; 6-pass adversarial review (security, performance, quality, friction, plan validity, spec compliance) |
| **failure-hunter** | Hunts silent failures | Runs in parallel with code-reviewer; zero-tolerance for empty catches, log-only handlers, discarded errors |
| **integration-verifier** | E2E validation | Exit codes: PASS/FAIL with evidence |
| **doc-syncer** | Diff-driven documentation sync | Classifies doc impact; SKIPPED/PARTIAL/COMPLETE/FAIL contract gating Memory Update; honors `DIFF_DRIVEN_DOCS: skip` |
| **planner** | Creates plans | Saves to `docs/plans/` + updates memory |
| **plan-gap-reviewer** | Fresh plan challenge pass | Read-only anti-anchoring review before final plan handoff |
| **researcher** | Web + GitHub research (Bright Data / Octocode MCP accelerators, built-in fallbacks) | Saves findings to file |
| **triage-agent** | Triages incoming issues/PRs | Does not change project code; categorizes, verifies, checks redundancy + prior rejection, writes agent-ready briefs |
| **architecture-scanner** | Codebase health audit | Does not change project code; scans for shallow modules + deepening candidates, produces HTML report with before/after diagrams |
| **qa-researcher** | QA route: surveys ONE source (code, spec docs, tickets, or cc10x artifacts) | Read-only; produces a per-source report (user flow, system flow, user action inventory, observation points) that the router consolidates into the feature map — it does not write the test plan |
| **qa-harness-builder** | QA route: builds the test environment | Provisions services, isolation and fixtures; extends the existing live-harness manifest, never forks it |
| **qa-executor** | QA route: runs the plan and reports | Fills the router-seeded `qa-report.template.md` in place; teardown is verified, not assumed |

---

## The 21 Skills

Skills are **loaded automatically by agents**. You never invoke them directly.

| Skill | Used By | Purpose |
| ------- | --------- | --------- |
| **agent-common** | every agent except plan-gap-reviewer | Shared preamble: memory protocol, CONTRACT envelope, output rules |
| **memory-and-handoff** | main session (router-gated) | Persist context across compaction; portable handoff package |
| **verification** | component-builder, bug-investigator, code-reviewer, integration-verifier, doc-syncer, qa-harness-builder, qa-executor | Evidence before claims: gate function, validation levels, evidence array |
| **building** | component-builder, bug-investigator | TDD RED-GREEN-REFACTOR, false-RED guard, integration & live proof |
| **debugging** | bug-investigator | Root cause analysis, feedback loop first, blast radius after fix |
| **code-review** | code-reviewer, failure-hunter, main session | Adversarial review modes; verify human/external review feedback before agreeing or implementing |
| **planning** | planner | Comprehensive plans + plan completeness gate |
| **plan-review-gate** | planner | Final fail-closed plan sanity gate before handoff |
| **architecture** | planner, builder (router-gated) | System & API design for multi-component work |
| **frontend** | UI work (router-gated) | Authoring + critique modes: UX, accessibility, DESIGN.md, AI-slop detection |
| **exploration** | PLAN workflow (router-gated) | Design brainstorm + throwaway spike modes with machine-readable handoff |
| **diff-driven-docs** | doc-syncer | Doc impact classification + audit-doc format |
| **research** | planner, bug-investigator (via researcher agent) | Synthesis-only: how to interpret research results |
| **codebase-hygiene** | architecture-scanner (router-gated for other agents) | Semantic-duplicate audit + shallow-module deepening |
| **codebase-design** | planner, component-builder, bug-investigator, code-reviewer, architecture-scanner | Canonical deep-module vocabulary: module, interface, depth, seam, adapter, leverage, locality |
| **domain-modeling** | planner, doc-syncer, triage-agent; component-builder (read-only mode) | Active glossary discipline: challenge terms, sharpen language, write CONTEXT.md + ADRs |
| **mcp-cli** | researcher | On-demand MCP server use without permanent context pollution |
| **qa-strategy** | qa-researcher, qa-harness-builder, qa-executor (and read as a coverage lens by plan-gap-reviewer on QA plan reviews) | Test-system design: tier selection, scenario matrices, environment topology, fixture lifecycle, flake sources |
| **update** | maintainers | Maintenance meta-skill for updating cc10x itself |
| **cc10x-guide** | users asking about cc10x (model-invoked) | Answers questions about cc10x itself: install, setup, workflows, memory, troubleshooting; never executes work |
| **resolving-merge-conflicts** | any agent hitting a git conflict (model-invoked) | Resolve merge/rebase conflicts hunk by hunk by intent; never --abort |

> `cc10x-router` is the entry-point skill that routes every workflow; it ships alongside these 21. The per-agent preload list is in [`docs/agent-contract-registry.md`](docs/agent-contract-registry.md).

---

### Task-Based Orchestration

cc10x uses Claude Code's task tools for workflow coordination when they are available, and tracks the same graph in the workflow artifact when they are not:

```
┌─────────────────────────────────────────────────────────────────┐
│  BUILD: User Authentication                                     │
│  ├── component-builder (pending)                                │
│  ├── code-reviewer (blocked by: builder)                        │
│  ├── failure-hunter (blocked by: builder)                       │
│  └── integration-verifier (blocked by: reviewer, hunter)        │
└─────────────────────────────────────────────────────────────────┘
```

- **Dependency chains**: Agents wait for blockers to complete
- **Parallel execution**: reviewer + hunter run simultaneously
- **Resume capability**: TaskList() checks for active workflows; without task tools the router resumes from `.cc10x/workflows/*.json`
- **Router-owned completion**: the router completes a task after it validates the agent's contract
- **Router-owned advancement**: only the router decides whether a workflow can continue

---

### Hooks

The plugin ships these Claude Code-native hooks, registered in `plugins/cc10x/hooks/hooks.json`:

| Hook | Purpose |
| ------ | --------- |
| `PreToolUse` | Three guards: protected memory writes (audit by default), git operations (always blocks the destructive ones), QA isolation (always blocks quarantined reads and environment changes on the QA route) |
| `SessionStart` | Python preflight, then rehydrate workflow context after restart or compaction |
| `PostToolUse` | Audit workflow artifact integrity after writes (blocks a malformed artifact by default) |
| `TaskCompleted` | Validate CC10X task metadata before task completion (audit by default) |
| `PostCompact` | Capture compaction events for workflow telemetry |
| `SubagentStop` | Audit subagent outputs for required contract markers |
| `PreCompact` | Snapshot workflow state before compaction |
| `Stop` | Snapshot workflow state on session stop |
| `StopFailure` | Log API failure telemetry asynchronously |
| `InstructionsLoaded` | Audit instruction-file loading asynchronously |

These hooks are intentionally minimal. They improve reliability without turning the plugin into a second runtime. Which script runs on each event, which can block, and how to change a mode: [`plugins/cc10x/hooks/README.md`](plugins/cc10x/hooks/README.md).

---

### Plan → Build Automation

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

### Expected Behavior

#### When You Say "Build a Task Tracker"

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

### Files Structure

```
plugins/cc10x/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── hooks.json
│   ├── README.md
│   └── pre-commit
├── config/
│   └── hook-mode.json
├── scripts/                # hook scripts and the L1 test suites (test_cc10x_*.py)
│   ├── cc10x_{event_logger,git_guard,hooklib,posttooluse_artifact_guard,pretooluse_guard,qa_isolation_guard,sessionstart_context,state_persist,task_completed_guard}.py
│   └── cc10x_preflight.sh
├── tools/
│   ├── {doc_consistency_check,fixture_registry,harness_audit,latency_audit,live_harness_runner,phase_brief,preload_probe,prompt_clause_assertions,release_gate,review_package,token_usage_report,workflow_replay_check,worldclass_benchmark}.py
│   └── docs_rot_baseline.json
├── templates/
│   ├── {coverage-thresholds,live-harness.template}.json
│   └── {doc-target-overlay,qa-env-plan.template,qa-feature-map.template,qa-report.template,qa-setup.template,qa-test-plan.template}.md
├── tests/
│   ├── fixtures/
│   └── live/
├── evals/
│   ├── BASELINE.md
│   └── cases/
├── agents/
│   └── {architecture-scanner,bug-investigator,code-reviewer,component-builder,doc-syncer,failure-hunter,integration-verifier,plan-gap-reviewer,planner,qa-executor,qa-harness-builder,qa-researcher,researcher,triage-agent}.md
│
└── skills/
    ├── cc10x-router/
    │   ├── SKILL.md
    │   └── references/
    │       ├── {build,debug,review,plan,triage,codebase-health,qa}-workflow.md
    │       ├── workflow-artifact-and-hook-policy.md
    │       ├── remediation-and-research.md
    │       └── workflow-artifact.skeleton.json
    ├── agent-common/SKILL.md
    ├── architecture/SKILL.md
    ├── building/SKILL.md
    ├── cc10x-guide/SKILL.md
    ├── code-review/SKILL.md
    ├── codebase-design/SKILL.md
    ├── codebase-hygiene/SKILL.md
    ├── debugging/SKILL.md
    ├── diff-driven-docs/SKILL.md
    ├── domain-modeling/SKILL.md
    ├── exploration/SKILL.md
    ├── frontend/SKILL.md
    ├── mcp-cli/SKILL.md
    ├── memory-and-handoff/SKILL.md
    ├── plan-review-gate/SKILL.md
    ├── planning/SKILL.md
    ├── qa-strategy/SKILL.md
    ├── research/SKILL.md
    ├── resolving-merge-conflicts/SKILL.md
    ├── update/SKILL.md
    └── verification/SKILL.md
```

Some skills also carry a `references/` directory of their own (for example `skills/frontend/references/` and `skills/memory-and-handoff/references/`).

Developer docs live under `docs/`:

- [`docs/router-invariants.md`](docs/router-invariants.md), [`docs/prompt-invariants.md`](docs/prompt-invariants.md) and [`docs/agent-contract-registry.md`](docs/agent-contract-registry.md) are the maintained registries
- [`docs/cc10x-orchestration-safety.md`](docs/cc10x-orchestration-safety.md) is the safety model
- [`docs/prompt-change-checklist.md`](docs/prompt-change-checklist.md) holds the one release-gate list (section 7)
- [`docs/known-flaws.md`](docs/known-flaws.md) lists known platform limits and recovery patterns
- `docs/history/` keeps archived records of past work, each marked as historical

If you need to understand or evolve the harness, start there after reading `cc10x-router`.

</details>

---

## Version History

<details>
<summary><strong>Release history (v5.3 → v12.10.0)</strong></summary>

| Version | Highlights |
| --------- | ------------ |
| **v12.10.0** | Remediation release: agent-common is now delivered to 13 agents, Python 3.9 floor with a preflight hook, rewritten git guard, router consistency fixes, docs reset. See the CHANGELOG entry. |
| **v12.9.1** | Instruction-layer harmony: the install template in this README is byte-identical to the repo's own CLAUDE.md routing block. |
| **v12.9.0** | QA route: a sixth route for when testing the code is the deliverable (`qa-researcher`, `qa-harness-builder`, `qa-executor`, `qa-strategy`), plus the plan-review, debug-handoff and hook changes it depends on. |
| **v12.8.2** | Evidence-discipline wording imports from pstack; wording only, no routing, gate, hook or contract changes. |
| **v12.8.1** | Adversarially validated prompt-craft refinements; wording only. |
| **v12.8.0** | `cc10x-guide` skill (ask Claude about cc10x itself) and a documentation overhaul. |
| **v12.7.0** | Prompt-engineering prose reconciliation: behavior-preserving wording pass over skills, agents and router. |
| **v12.6.0** | Integrity reconciliation: audit-seam revival, router drift fixes, unified agent contracts, guard hardening. |
| **v12.5.0** | Matt Pocock skills integration, the enforced seam gate, and the advisory on-ramp workflows. |
| **v12.4.0** | Self-audit fixes: de-duplicated skills, wired decorative patterns, hook-enforced circuit breaker. |
| **v12.3.1** | `silent-failure-hunter` renamed `failure-hunter` to resolve an agent name conflict. |
| **v12.3.0** | 18 high-impact patterns adopted from six other repositories. |
| **v12.2.0** | Restored the standalone `failure-hunter` and parallel review. |
| **v12.1.0** | The Loop Engine: the harness reduced to its unique enforcement mechanisms. |
| **v11.1.0** | Execution-engine harvest from a system-level comparison with superpowers and matt-pocock skills. |
| **v11.0.0** | De-versioned state namespace: `.cc10x/v10/` became `.cc10x/`. |
| **v10.1.20** | Escape the Claude Code sensitive-file gate: workflow state root relocated from `.claude/cc10x/v10/` to `.cc10x/v10/` across every prompt surface, runtime hook, and fixture. Every router fanout, event-log append, and memory refresh is now silent in default-permission setups. Audit now catches runtime/prompt path drift so this class of regression fails self-tests before release. |
| **v10.1.19** | Harmony hardening release: contradiction cleanup across router-facing instructions, router-owned self-contained handoffs, phase-local BUILD context, early memory capture before validation, review/hunt fan-in at the router, and full docs/release metadata alignment. |
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

</details>

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
  <strong>cc10x v12.10.0</strong>
</p>
