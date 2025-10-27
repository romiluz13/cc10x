# Quick Reference Guide

## JSON Schemas

### marketplace.json

```json
{
  "name": "marketplace-id",
  "owner": {"name": "Name", "email": "email@example.com"},
  "metadata": {
    "description": "Optional description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-id",
      "source": "./path" | {"source": "github", "repo": "owner/repo"},
      "description": "What plugin does",
      "version": "1.0.0",
      "author": {"name": "Author"},
      "homepage": "https://docs.url",
      "repository": "https://github.com/...",
      "license": "MIT",
      "keywords": ["tag1", "tag2"],
      "category": "category-name",
      "strict": true
    }
  ]
}
```

### plugin.json

```json
{
  "name": "plugin-id",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {"name": "Name", "email": "email@example.com"},
  "homepage": "https://docs.url",
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "commands": ["./custom/path"],
  "agents": ["./custom/path"],
  "skills": "./skills/",
  "hooks": "./hooks.json" | {...},
  "mcpServers": "./.mcp.json" | {...}
}
```

### SKILL.md

```markdown
---
name: skill-id
description: What skill does and when to use it. Include trigger keywords!
allowed-tools: Read, Grep, Glob  # Optional, Claude Code only
---

# Skill Name

## Quick Start
Basic instructions...

## Advanced
See [REFERENCE.md](REFERENCE.md)
```

### Subagent

```markdown
---
name: agent-id
description: When to use this agent
tools: Read, Grep, Glob  # Optional
model: sonnet  # Optional: sonnet, opus, haiku, inherit
---

# Agent Name

System prompt defining role and behavior...
```

### Slash Command

```markdown
---
description: What command does
argument-hint: [arg1] [arg2]  # Optional
allowed-tools: Bash(git*)  # Optional
model: sonnet  # Optional
---

Command prompt.
Use $ARGUMENTS or $1, $2 for args.
```

### hooks.json

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/script.sh",
          "timeout": 60
        }
      ]
    }
  ]
}
```

### .mcp.json

```json
{
  "mcpServers": {
    "server-name": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## Command Cheat Sheet

### Marketplace Commands

```bash
/plugin marketplace add owner/repo              # GitHub
/plugin marketplace add https://git.url/repo    # Git
/plugin marketplace add ./local-path            # Local
/plugin marketplace add https://url/marketplace.json  # Direct

/plugin marketplace list                        # List all
/plugin marketplace update <name>               # Update
/plugin marketplace remove <name>               # Remove
```

### Plugin Commands

```bash
/plugin                                         # Interactive UI
/plugin install <name>@<marketplace>            # Install
/plugin enable <name>@<marketplace>             # Enable
/plugin disable <name>@<marketplace>            # Disable
/plugin uninstall <name>@<marketplace>          # Uninstall
```

### Built-in Commands

```bash
/help               # All commands
/agents             # Manage subagents
/hooks              # View hooks
/model              # Change model
/permissions        # Manage permissions
/config             # Settings UI
/status             # System status
/cost               # Token usage
/mcp                # MCP servers
/memory             # Edit CLAUDE.md
/clear              # Clear conversation
/compact            # Compact context
```

### Debug Commands

```bash
claude --debug                                  # Debug mode
claude plugin validate .                        # Validate plugin
/context                                        # View context usage
```

## File Location Quick Reference

| Component | Project | User | Plugin |
|-----------|---------|------|--------|
| **Settings** | `.claude/settings.json` | `~/.claude/settings.json` | - |
| **Commands** | `.claude/commands/*.md` | `~/.claude/commands/*.md` | `commands/*.md` |
| **Agents** | `.claude/agents/*.md` | `~/.claude/agents/*.md` | `agents/*.md` |
| **Skills** | `.claude/skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` | `skills/*/SKILL.md` |
| **Hooks** | `.claude/settings.json` | `~/.claude/settings.json` | `hooks/hooks.json` |
| **MCP** | `.claude/settings.json` | `~/.claude/settings.json` | `.mcp.json` |
| **Memory** | `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | - |

## Priority Reference

| Component | Priority |
|-----------|----------|
| Project | Highest |
| Plugin | Medium |
| User | Lowest |

Project-level always overrides User-level for same component name.

## Field Validation Rules

### Skill Name
- Max: 64 characters
- Pattern: `[a-z0-9-]+` (lowercase, numbers, hyphens)
- No XML tags
- No reserved: "anthropic", "claude"

### Skill Description
- Max: 1024 characters
- Must be non-empty
- No XML tags
- Should include: what it does + when to use it

### Plugin Name
- Pattern: kebab-case
- No spaces
- Unique identifier

## Tool Names

### Core Tools
- `Read`, `Write`, `Edit`
- `Bash`, `Grep`, `Glob`
- `Task` (subagent invocation)
- `WebFetch`, `WebSearch`
- `Skill` (skill invocation)

### Tool Restrictions

```yaml
# Subagent
tools: Read, Grep, Glob

# Skill
allowed-tools: Read, Grep, Glob

# Slash command
allowed-tools: Bash(git*), Read

# SDK
allowedTools: ['Read', 'Grep', 'Glob']
```

## Hook Events Quick Reference

| Event | When | Matcher | Common Use |
|-------|------|---------|------------|
| **PreToolUse** | Before tool runs | Tool name | Validation, permission |
| **PostToolUse** | After tool runs | Tool name | Formatting, linting |
| **UserPromptSubmit** | Prompt submitted | None | Add context, validate |
| **Notification** | Claude notifies | None | Alerts, logging |
| **Stop** | Agent stops | None | Continue work, logging |
| **SubagentStop** | Subagent stops | None | Subagent continuation |
| **PreCompact** | Before compact | manual/auto | Checkpoint, save |
| **SessionStart** | Session starts | startup/resume | Setup, load context |
| **SessionEnd** | Session ends | None | Cleanup, logging |

## Hook Exit Codes

```bash
exit 0   # Success (stdout to user, except UserPromptSubmit adds to context)
exit 2   # Blocking error (stderr to Claude, blocks action)
exit 1   # Non-blocking error (stderr to user, continues)
```

## Model Selection

| Model | Use Case | Speed | Cost | Capability |
|-------|----------|-------|------|------------|
| **Haiku** | Simple tasks | Fastest | Lowest | Basic |
| **Sonnet** | Most tasks | Fast | Medium | Balanced |
| **Opus** | Complex tasks | Slower | Highest | Maximum |

Configure in:
- Subagent: `model: sonnet`
- SDK: `model: 'sonnet'`
- Command: `model: sonnet`

## Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Ask for permission |
| `plan` | Plan mode (safe) |
| `acceptEdits` | Auto-accept edits |
| `bypassPermissions` | Auto-approve all |

## Token Budgets

### Skills
- Metadata (Level 1): ~100 tokens/skill (always loaded)
- SKILL.md (Level 2): <5k tokens (loaded when triggered)
- Additional files (Level 3): Unlimited (on-demand)

### Context Window
- Total: ~200k tokens (Sonnet 4.5)
- System prompt: ~10k tokens
- Skill metadata: ~100 × N skills
- Conversation: Growing
- Active skills: ~5k/skill

## Common Patterns Quick Reference

### Skill with Script

```markdown
## Process PDF

Run analyzer:
```bash
python scripts/analyze.py input.pdf > output.json
```

Output format:
```json
{"field": {"type": "text", "x": 100, "y": 200}}
```
```

### Skill with Workflow

```markdown
## Workflow

Copy checklist:
```
- [ ] Step 1: Run analysis
- [ ] Step 2: Review output
- [ ] Step 3: Validate
- [ ] Step 4: Execute
```

**Step 1**: Run analysis...
**Step 2**: Review output...
```

### Skill with Conditional Logic

```markdown
## Workflow

1. Determine type:
   - **Type A?** → See [TYPE-A.md](TYPE-A.md)
   - **Type B?** → See [TYPE-B.md](TYPE-B.md)

2. Process accordingly
```

### Hook with Validation

```python
#!/usr/bin/env python3
import json, sys

input_data = json.load(sys.stdin)
# Validate...

if invalid:
    print("Error details", file=sys.stderr)
    sys.exit(2)  # Blocks and shows to Claude

sys.exit(0)
```

### SDK with Agents

```typescript
query({
  prompt: "Task",
  options: {
    agents: {
      'specialist': {
        description: 'When to use',
        prompt: 'System prompt',
        tools: ['Read', 'Grep'],
        model: 'sonnet'
      }
    }
  }
})
```

## Debugging Quick Guide

### Skill not triggering?

```bash
claude --debug
# Look for: "Loading skills from..."
# Check description has trigger keywords
```

### Hook not firing?

```bash
claude --debug
# Look for: "Executing hooks for..."
# Check matcher pattern
# Verify script executable: chmod +x
```

### Plugin not loading?

```bash
claude --debug
# Look for: "Loading plugin..."
# Check directory structure
# Validate JSON: claude plugin validate .
```

### Command not appearing?

```bash
/help
# Check if listed

ls .claude/commands/
# Verify file exists
```

## Authentication

```bash
# Anthropic API
export ANTHROPIC_API_KEY=your-key

# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
```

## Installation Quick Start

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Navigate to project
cd your-project

# Start
claude

# Add marketplace
/plugin marketplace add anthropics/skills

# Install skill
/plugin install pdf-processing@anthropics
```

## Create Your First...

### Skill

```bash
mkdir -p .claude/skills/my-skill
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What it does and when to use it
---

# My Skill

Instructions here...
EOF
```

### Command

```bash
mkdir -p .claude/commands
cat > .claude/commands/review.md << 'EOF'
---
description: Review code
---

Review this code for issues.
EOF
```

### Subagent

```bash
/agents
# > Create New Agent
# > Generate with Claude
```

### Plugin

```bash
mkdir my-plugin
cd my-plugin
mkdir -p .claude-plugin commands agents skills

cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0"
}
EOF
```

## Most Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Skill not triggering | Make description more specific with keywords |
| Plugin not loading | Check `.claude-plugin/` location, validate JSON |
| Hook not executing | Verify `chmod +x`, check matcher pattern |
| Command not found | Check file in `commands/` dir, restart Claude |
| MCP server failing | Use `${CLAUDE_PLUGIN_ROOT}`, check command exists |
| Path errors | Use forward slashes, not backslashes |

## Tips for AI Learning

1. **Start with 00-OVERVIEW.md** - Understand the architecture
2. **Focus on 04-SKILLS.md** - This is the NEW feature
3. **Skills use progressive disclosure** - 3 levels of loading
4. **Skills are model-invoked** - Claude chooses when to use
5. **Commands are user-invoked** - Explicit `/command`
6. **Plugins bundle components** - Distribution unit
7. **Marketplace distributes plugins** - Catalog system
8. **SDK enables programmatic agents** - TypeScript/Python
9. **Use examples in 08-EXAMPLES.md** - Real patterns
10. **Follow 09-BEST-PRACTICES.md** - Proven guidelines

