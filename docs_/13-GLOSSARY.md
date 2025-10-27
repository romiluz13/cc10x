# Glossary

## Core Terms

### Agent
General term for AI assistant. In Claude Code context, can refer to:
- Main Claude Code agent
- Subagent (specialized worker)

### Agent SDK
TypeScript/Python SDK for building custom AI agents programmatically. Formerly "Claude Code SDK".

### Allowed Tools
Tools that a skill, subagent, or command is permitted to use. Syntax varies:
- Subagent: `tools: Read, Grep, Glob`
- Skill: `allowed-tools: Read, Grep, Glob`
- SDK: `allowedTools: ['Read', 'Grep', 'Glob']`

### Anthropic-Managed Skill
Pre-built skill provided by Anthropic (pptx, xlsx, docx, pdf). Available via API.

## C

### CLAUDE.md
Project memory file containing instructions that persist across sessions. Located at:
- `.claude/CLAUDE.md` (project)
- `~/.claude/CLAUDE.md` (user)
- `CLAUDE.md` (root)

### Code Execution Tool
Claude API tool that provides secure sandbox for running code. Required for Skills.

### Command
See "Slash Command"

### Context Window
The amount of text/tokens Claude can consider at once (~200k tokens for Sonnet 4.5).

### Custom Skill
User-created skill (vs Anthropic-managed pre-built skills).

## D

### Description Field
Critical metadata field that determines when skills/agents are triggered. Must include:
- What it does
- When to use it
- Trigger keywords

## F

### Frontmatter
YAML metadata block at start of markdown files. Used in:
- Skills: `name`, `description`, `allowed-tools`
- Subagents: `name`, `description`, `tools`, `model`
- Commands: `description`, `argument-hint`, `allowed-tools`, `model`

## H

### Hook
Event-driven automation that executes commands when specific events occur.

Hook Events:
- PreToolUse, PostToolUse
- UserPromptSubmit
- Stop, SubagentStop
- SessionStart, SessionEnd
- PreCompact, Notification

### Hook Input
JSON data sent to hook via stdin containing event details and context.

### Hook Output
Response from hook via stdout (JSON) or exit code determining next action.

## K

### Kebab-Case
Naming convention using lowercase letters, numbers, and hyphens. Required for:
- Plugin names: `my-plugin`
- Skill names: `pdf-processing`
- Marketplace names: `company-tools`

## L

### Level 1, 2, 3 Loading
Progressive disclosure levels for Skills:
- **Level 1**: Metadata (name, description) - Always loaded (~100 tokens)
- **Level 2**: Instructions (SKILL.md body) - Loaded when triggered (~5k tokens)
- **Level 3**: Resources (additional files, scripts) - Loaded as needed (unlimited)

## M

### Marketplace
JSON catalog listing available plugins. Located at `.claude-plugin/marketplace.json`.

### Matcher
Pattern used in hooks to filter which tools trigger the hook. Supports:
- Exact match: `Write`
- Multiple: `Write|Edit`
- Regex: `Notebook.*`
- All: `*` or `""`

### MCP (Model Context Protocol)
Protocol for connecting Claude to external tools and services. MCP servers provide tools accessible as `mcp__server__tool`.

### Model-Invoked
Claude automatically decides when to use (Skills, Subagents). Opposite of User-Invoked.

## P

### Permission Mode
Controls how Claude asks for tool permission:
- `default`: Ask user
- `plan`: Plan mode (safe)
- `acceptEdits`: Auto-accept edits
- `bypassPermissions`: Auto-approve all

### Plugin
Bundle of components (commands, agents, skills, hooks, MCP) distributed as single package.

### Plugin Manifest
`plugin.json` file describing plugin metadata and configuration.

### Progressive Disclosure
Architecture pattern where content loads in stages (3 levels) as needed. Unique to Skills.

### Project-Level
Configuration/components stored in `.claude/` (shared with team via git).

## S

### Skill
**NEW FEATURE (Oct 16, 2025)**: Model-invoked capability with progressive disclosure. Located in `skills/*/SKILL.md`.

Key characteristics:
- Model-invoked (automatic)
- 3-level loading
- Can include scripts
- Unlimited bundled content

### SKILL.md
Required file for each skill containing:
- YAML frontmatter (name, description)
- Markdown instructions
- References to additional files

### Slash Command
User-invoked prompt shortcut. Format: `/command-name [args]`

Stored in:
- `.claude/commands/*.md` (project)
- `~/.claude/commands/*.md` (user)

### Source Handler
Component that fetches plugins from different sources (GitHub, Git, local, URL).

### Subagent
Specialized AI worker with separate context window, custom system prompt, and tool restrictions.

Stored in:
- `.claude/agents/*.md` (project)
- `~/.claude/agents/*.md` (user)

### System Prompt
Instructions defining agent's role and behavior. Can be:
- Base system prompt
- Subagent prompt (in frontmatter)
- Skill instructions (in SKILL.md)
- CLAUDE.md content

## T

### Tool
Action Claude can perform. Core tools:
- File: Read, Write, Edit
- Search: Grep, Glob
- Execute: Bash
- Web: WebFetch, WebSearch
- Agent: Task (subagent), Skill (skill invocation)

### Tool Restriction
Limiting which tools an agent/skill can use. Improves:
- Security (prevent unwanted actions)
- Focus (reduce decision space)
- Performance (fewer options to consider)

## U

### User-Invoked
User explicitly triggers (Slash Commands). Opposite of Model-Invoked.

### User-Level
Configuration/components stored in `~/.claude/` (personal, not shared).

## V

### Version
Semantic version (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes (2.0.0)
- MINOR: New features (1.1.0)
- PATCH: Bug fixes (1.0.1)

## Y

### YAML Frontmatter
Metadata block at start of markdown files enclosed by `---`:

```yaml
---
name: skill-name
description: What it does
---
```

## Acronyms

- **API**: Application Programming Interface
- **CLI**: Command Line Interface
- **MCP**: Model Context Protocol
- **SDK**: Software Development Kit
- **YAML**: YAML Ain't Markup Language

## Comparison Table

### Model-Invoked vs User-Invoked

| Aspect | Model-Invoked | User-Invoked |
|--------|---------------|--------------|
| **What** | Skills, Subagents | Slash Commands |
| **Trigger** | Claude decides | User types `/cmd` |
| **When** | Automatic based on context | Explicit invocation |
| **Discovery** | Description matching | Name matching |

### Project vs User vs Plugin

| Aspect | Project | User | Plugin |
|--------|---------|------|--------|
| **Location** | `.claude/` | `~/.claude/` | `<plugin>/` |
| **Sharing** | Git (team) | Personal | Marketplace |
| **Priority** | Highest | Lowest | Medium |
| **Scope** | Current project | All projects | When enabled |

### Skills vs Commands

| Aspect | Skills | Commands |
|--------|--------|----------|
| **Invocation** | Model (automatic) | User (explicit) |
| **Structure** | Directory with SKILL.md | Single .md file |
| **Loading** | Progressive (3 levels) | Immediate (full) |
| **Scripts** | Yes (bundled) | No |
| **Arguments** | No | Yes ($1, $2, $ARGUMENTS) |
| **Use Case** | Complex capabilities | Quick prompts |

### Subagents vs Skills

| Aspect | Subagents | Skills |
|--------|-----------|--------|
| **Purpose** | Task delegation | Capability extension |
| **Context** | Separate window | Main window (on-demand) |
| **Invocation** | Task-based | Capability-based |
| **System Prompt** | Custom prompt | Instructions in SKILL.md |
| **Best For** | Complex tasks needing isolation | Domain expertise |

## Environment Variables

| Variable | Scope | Value | Usage |
|----------|-------|-------|-------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin | Plugin absolute path | Hook/MCP paths |
| `$CLAUDE_PROJECT_DIR` | Hook | Project root | Hook scripts |
| `$CLAUDE_ENV_FILE` | SessionStart | Env file path | Persist env vars |
| `$CLAUDE_CODE_REMOTE` | Hook | "true" or empty | Detect web vs CLI |
| `$ANTHROPIC_API_KEY` | Global | API key | Authentication |
| `$CLAUDE_CODE_USE_BEDROCK` | Global | "1" | Enable Bedrock |
| `$CLAUDE_CODE_USE_VERTEX` | Global | "1" | Enable Vertex |

## File Extensions

- `.md`: Markdown (commands, agents, skills, documentation)
- `.json`: JSON (plugin.json, marketplace.json, hooks.json, .mcp.json)
- `.jsonl`: JSON Lines (conversation transcripts)

## Reserved Words

Cannot use in skill/plugin names:
- "anthropic"
- "claude"

## Common Abbreviations

- **PR**: Pull Request
- **MCP**: Model Context Protocol
- **SDK**: Software Development Kit
- **API**: Application Programming Interface
- **CLI**: Command Line Interface
- **YAML**: YAML Ain't Markup Language
- **JSON**: JavaScript Object Notation
- **JWT**: JSON Web Token (often in examples)
- **ARR**: Annual Recurring Revenue (often in examples)
- **MRR**: Monthly Recurring Revenue (often in examples)

## File Naming Patterns

### Skills
- Directory: `kebab-case` (e.g., `pdf-processing`)
- File: Always `SKILL.md` (capitalized)
- Additional files: Any name (e.g., `FORMS.md`, `reference.md`)

### Commands
- File: `kebab-case.md` (e.g., `deploy.md`)
- Command name: File name without extension

### Subagents
- File: `kebab-case.md` (e.g., `code-reviewer.md`)
- Agent name: From `name` field in frontmatter

### Plugins
- Directory: `kebab-case`
- Manifest: `.claude-plugin/plugin.json`

### Marketplaces
- Manifest: `.claude-plugin/marketplace.json`
- Name: `kebab-case`

## Quick Lookups

### "What file should I edit?"

| Task | File |
|------|------|
| Add marketplace | None (use `/plugin marketplace add`) |
| Configure team marketplace | `.claude/settings.json` |
| Create skill | `.claude/skills/name/SKILL.md` |
| Create command | `.claude/commands/name.md` |
| Create subagent | `.claude/agents/name.md` |
| Add hook | `.claude/settings.json` |
| Configure MCP | `.claude/settings.json` |
| Project memory | `.claude/CLAUDE.md` |

### "Where does X come from?"

| Component | Source |
|-----------|--------|
| Pre-built skills (pptx, xlsx) | Anthropic (API only) |
| Custom skills | User/Project/Plugin |
| Subagents | User/Project/Plugin |
| Commands | User/Project/Plugin/Built-in |
| Hooks | User/Project/Plugin |
| MCP servers | User/Project/Plugin |

### "What can I customize?"

| Level | What | How |
|-------|------|-----|
| User | Personal prefs | `~/.claude/` |
| Project | Team shared | `.claude/` + git |
| Plugin | Reusable extensions | Plugin + marketplace |
| CLI | One-off config | `--agents`, `--model` flags |

## Status Indicators

When viewing in `/help` or `/agents`:

- `(project)`: From project `.claude/`
- `(user)`: From user `~/.claude/`
- `(plugin:name)`: From plugin
- `(project:frontend)`: From project subdirectory

## Common Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| "Missing YAML frontmatter" | SKILL.md lacks `---` | Add frontmatter |
| "Invalid name format" | Name not kebab-case | Use lowercase-with-hyphens |
| "Plugin not found" | Wrong marketplace/name | Check `/plugin marketplace list` |
| "Tool not found" | MCP tool wrong name | Use `ServerName:tool_name` |
| "Permission denied" | Tool needs approval | Check permission mode |
| "Skill name conflict" | Duplicate skill name | Rename or check priority |

## Useful Snippets

### Check What's Loaded

```bash
/help                 # All commands
/agents               # All subagents
# Ask Claude: "What skills are available?"
/config               # Settings UI
/status               # System status
```

### Debug Mode

```bash
claude --debug
```

Look for:
```
[DEBUG] Loading skills from...
[DEBUG] Loading plugins...
[DEBUG] Registered skill: name
[DEBUG] Executing hooks for...
```

### Validate Before Use

```bash
claude plugin validate .
```

### Test Locally

```bash
/plugin marketplace add ./local-marketplace
/plugin install test-plugin@local-marketplace
```

