# Claude Code Marketplace - Overview

## What is Claude Code?

Claude Code is Anthropic's agentic coding tool that runs in your terminal/web, helping you turn ideas into code. It's powered by Claude Sonnet 4.5 and features a revolutionary marketplace system for extending capabilities.

## Core Architecture

```
Claude Code Ecosystem
├── Marketplace System (plugin distribution)
├── Plugin System (extensions)
├── Subagents (specialized AI workers)
├── Skills (modular capabilities - NEW!)
├── Slash Commands (user-invoked)
├── Hooks (event automation)
└── Agent SDK (programmatic access)
```

## Key Concepts

### 1. **Marketplace** (Distribution Layer)
- JSON catalog of plugins
- Git-based distribution (GitHub, GitLab, local)
- Team-wide plugin sharing
- Version management

### 2. **Plugins** (Extension Packages)
Bundle multiple components:
- Commands (slash commands)
- Agents (subagents)
- Skills (NEW - model-invoked capabilities)
- Hooks (event handlers)
- MCP servers (external tools)

### 3. **Subagents** (Specialized Workers)
- Separate context windows
- Custom system prompts
- Specific tool access
- Task delegation

### 4. **Skills** (NEW - Model-Invoked Capabilities)
**CRITICAL: This is the NEW feature outside your knowledge cutoff!**

Skills vs Commands:
- **Skills**: Model-invoked (Claude decides when to use)
- **Commands**: User-invoked (explicit `/command` call)

Skills provide:
- Progressive disclosure (3 levels of loading)
- Filesystem-based architecture
- Executable scripts
- On-demand context loading

### 5. **Slash Commands**
User-invoked shortcuts:
- `/command-name [args]`
- Markdown files with frontmatter
- Project or personal scope

### 6. **Hooks**
Event-driven automation:
- PreToolUse, PostToolUse
- SessionStart, SessionEnd
- UserPromptSubmit
- Notification, Stop, etc.

### 7. **Agent SDK**
Build custom agents programmatically:
- TypeScript/Python SDKs
- Full Claude Code features
- Production-ready agents

## Installation Flow

```bash
# Add marketplace
/plugin marketplace add owner/repo

# Browse plugins
/plugin

# Install plugin
/plugin install plugin-name@marketplace-name
```

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest
├── commands/                 # Slash commands
├── agents/                   # Subagents
├── skills/                   # Agent Skills (NEW!)
│   └── my-skill/
│       └── SKILL.md
├── hooks/
│   └── hooks.json           # Event handlers
└── .mcp.json                # MCP servers
```

## Skills vs Commands vs Subagents

| Feature | Skills | Commands | Subagents |
|---------|--------|----------|-----------|
| **Invocation** | Model (automatic) | User (explicit) | Model (delegated) |
| **Structure** | SKILL.md + resources | Single .md file | Single .md file |
| **Progressive Loading** | Yes (3 levels) | No | No |
| **Context Window** | On-demand | Full load | Separate |
| **Use Case** | Complex capabilities | Quick prompts | Task delegation |

## Critical: Skills Architecture

Skills use **progressive disclosure** (3 levels):

1. **Level 1: Metadata** (always loaded)
   - `name` and `description` from YAML frontmatter
   - ~100 tokens per skill
   - Loaded at startup

2. **Level 2: Instructions** (loaded when triggered)
   - SKILL.md body content
   - <5k tokens
   - Loaded when skill matches task

3. **Level 3: Resources** (loaded as needed)
   - Additional files, scripts
   - Unlimited size
   - Loaded/executed only when referenced

## Directory Locations

```
Project-level:
.claude/
├── settings.json
├── commands/
├── agents/
├── skills/
└── hooks/

User-level:
~/.claude/
├── settings.json
├── commands/
├── agents/
├── skills/
└── hooks/
```

## Version Info
- Claude Code: Latest (v1.0+)
- Claude Sonnet: 4.5
- Skills: Released Oct 16, 2025
- Marketplace: Released Oct 9, 2025

