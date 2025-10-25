# Claude Code Marketplace Documentation

## 🚨 CRITICAL: New Features Outside Knowledge Cutoff

This documentation covers **new features released in October 2025**:

- **Agent Skills** (Oct 16, 2025) - Model-invoked capabilities with progressive disclosure
- **Plugin Marketplace** (Oct 9, 2025) - Distribution system for extensions
- **Subagents** - Specialized AI workers with separate contexts

## Documentation Index

### Quick Navigation

| File | Topic | Priority |
|------|-------|----------|
| **00-OVERVIEW.md** | System architecture & concepts | 🔴 START HERE |
| **01-MARKETPLACE-STRUCTURE.md** | Marketplace.json schema & distribution | 🔴 CRITICAL |
| **02-PLUGINS.md** | Plugin system & development | 🔴 CRITICAL |
| **03-SUBAGENTS.md** | Specialized AI workers | 🟡 IMPORTANT |
| **04-SKILLS.md** | Agent Skills (NEW!) | 🔴 CRITICAL |
| **05-SLASH-COMMANDS.md** | User-invoked commands | 🟡 IMPORTANT |
| **06-HOOKS.md** | Event-driven automation | 🟢 USEFUL |
| **07-SDK.md** | Programmatic agent building | 🟡 IMPORTANT |
| **08-EXAMPLES.md** | Complete real-world examples | 🟢 USEFUL |
| **09-BEST-PRACTICES.md** | Development guidelines | 🟢 USEFUL |

## Learning Path

### For AI Learning This System

**Step 1: Core Concepts** (30 min)
1. Read `00-OVERVIEW.md` - Understand architecture
2. Read `04-SKILLS.md` - **CRITICAL NEW FEATURE**
3. Review comparison table in 00-OVERVIEW.md

**Step 2: Marketplace System** (20 min)
1. Read `01-MARKETPLACE-STRUCTURE.md`
2. Read `02-PLUGINS.md`
3. Understand distribution model

**Step 3: Components** (40 min)
1. Read `03-SUBAGENTS.md` - Specialized workers
2. Read `05-SLASH-COMMANDS.md` - User commands
3. Read `06-HOOKS.md` - Event automation

**Step 4: Implementation** (30 min)
1. Read `07-SDK.md` - Programmatic usage
2. Read `08-EXAMPLES.md` - Real patterns
3. Read `09-BEST-PRACTICES.md` - Guidelines

**Total learning time: ~2 hours**

### For Building a Marketplace

**Required Reading**:
1. `00-OVERVIEW.md` - Concepts
2. `01-MARKETPLACE-STRUCTURE.md` - Schema
3. `02-PLUGINS.md` - Plugin structure
4. `04-SKILLS.md` - Skills (most powerful feature)
5. `08-EXAMPLES.md` - Patterns
6. `09-BEST-PRACTICES.md` - Guidelines

## Key Concepts Summary

### 1. Marketplace
**What**: JSON catalog of plugins
**Where**: `.claude-plugin/marketplace.json`
**Purpose**: Distribute plugins to teams/community

### 2. Plugin
**What**: Bundle of components (commands, agents, skills, hooks, MCP)
**Where**: Repository with `.claude-plugin/plugin.json`
**Purpose**: Shareable extension package

### 3. Subagent
**What**: Specialized AI with separate context
**Where**: `.claude/agents/*.md`
**Purpose**: Task delegation, context isolation

### 4. Skill (NEW! CRITICAL!)
**What**: Model-invoked capability with progressive disclosure
**Where**: `.claude/skills/*/SKILL.md`
**Purpose**: Extend Claude's capabilities automatically
**Loading**: 3 levels (metadata → instructions → resources)

### 5. Slash Command
**What**: User-invoked prompt shortcut
**Where**: `.claude/commands/*.md`
**Purpose**: Reusable prompt snippets

### 6. Hook
**What**: Event-driven automation
**Where**: `.claude/settings.json` (hooks field)
**Purpose**: Automate workflows on events

### 7. Agent SDK
**What**: TypeScript/Python SDK for building agents
**Where**: npm/pip package
**Purpose**: Programmatic agent development

## Decision Tree

### When to Use What?

```
Need to extend capabilities?
├─ Claude should decide when to use? → Skill
├─ User should explicitly invoke? → Slash Command
├─ Need task delegation? → Subagent
├─ React to events? → Hook
└─ Programmatic control? → SDK

Need to distribute?
├─ Single extension? → Plugin
├─ Multiple plugins? → Marketplace
└─ Team sharing? → Git repo + settings.json

Need external tools?
└─ → MCP Server (in plugin or standalone)
```

### Skills vs Commands vs Subagents

| Question | Answer |
|----------|--------|
| Complex workflow with scripts? | **Skill** |
| Quick reusable prompt? | **Slash Command** |
| Specialized task with separate context? | **Subagent** |
| Automatic invocation needed? | **Skill** or **Subagent** |
| User controls when to run? | **Slash Command** |
| Need progressive loading? | **Skill** |
| Single markdown file enough? | **Slash Command** or **Subagent** |
| Need bundled scripts/resources? | **Skill** |

## Quick Reference

### Installation

```bash
# Add marketplace
/plugin marketplace add owner/repo

# Install plugin
/plugin install plugin-name@marketplace-name

# View commands
/help

# Manage agents
/agents

# Check hooks
/hooks
```

### File Locations

```
Project (shared):
.claude/
├── settings.json
├── commands/*.md
├── agents/*.md
├── skills/*/SKILL.md
└── hooks/*.sh

User (personal):
~/.claude/
├── settings.json
├── commands/*.md
├── agents/*.md
└── skills/*/SKILL.md

Plugin:
<plugin>/
├── .claude-plugin/plugin.json
├── commands/*.md
├── agents/*.md
├── skills/*/SKILL.md
├── hooks/hooks.json
└── .mcp.json
```

### Environment Variables

```bash
${CLAUDE_PLUGIN_ROOT}   # Plugin directory
$CLAUDE_PROJECT_DIR     # Project root
$CLAUDE_ENV_FILE        # Env file (SessionStart only)
$CLAUDE_CODE_REMOTE     # "true" if web, empty if CLI
```

### Command Reference

```bash
# Marketplaces
/plugin marketplace add <source>
/plugin marketplace list
/plugin marketplace update <name>
/plugin marketplace remove <name>

# Plugins
/plugin install <name>@<marketplace>
/plugin enable <name>@<marketplace>
/plugin disable <name>@<marketplace>
/plugin uninstall <name>@<marketplace>

# Agents
/agents

# Other
/help                    # All commands
/model                   # Change model
/permissions             # Manage permissions
/cost                    # Token usage
/config                  # Settings UI
```

## Critical Differences: Skills vs Commands

This is the MOST IMPORTANT distinction to understand:

### Skills (Model-Invoked)

```markdown
---
name: pdf-processor
description: Extract text from PDFs. Use when working with PDF files.
---

# PDF Processor
Instructions...
```

Usage:
```bash
> Extract text from document.pdf
# Claude sees "PDF" in request
# Claude sees "PDF" in skill description
# Claude AUTOMATICALLY loads and uses skill
```

### Slash Commands (User-Invoked)

```markdown
---
description: Review code
---

Review this code for issues.
```

Usage:
```bash
/review
# USER explicitly types /review
# Claude does NOT choose when to use it
```

**When to use which**:
- **Skill**: Claude should automatically use when relevant
- **Command**: User controls exactly when to invoke

## Progressive Disclosure Explained

This is unique to Skills and CRITICAL to understand:

```
Skill: pdf-processing

Level 1 (Startup - ~100 tokens):
└── Metadata: "PDF processing - extract text, fill forms"
    
Level 2 (Triggered - ~5k tokens):
└── SKILL.md body: Instructions, workflows, references

Level 3+ (As Needed - Unlimited):
├── FORMS.md (referenced from SKILL.md)
├── REFERENCE.md (referenced from SKILL.md)  
└── scripts/*.py (executed, not loaded!)
```

**Key insight**: Only Level 1 has constant cost. Levels 2+ load only when needed!

You can install 100 skills and only pay ~10k tokens for metadata!

## Common Gotchas

### 1. Directory Structure

❌ **WRONG**:
```
plugin/
└── .claude-plugin/
    ├── plugin.json
    ├── commands/      # WRONG LOCATION!
    └── skills/        # WRONG LOCATION!
```

✅ **CORRECT**:
```
plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/          # At plugin root!
└── skills/            # At plugin root!
```

### 2. Skill Description

❌ **Too vague**:
```yaml
description: Helps with files
```

✅ **Specific**:
```yaml
description: Extract text from PDF files, fill forms, merge documents. Use when working with PDFs or when user mentions PDF, forms, or document extraction.
```

### 3. Path References

❌ **Windows paths**:
```markdown
See [guide](scripts\helper.py)
```

✅ **Unix paths**:
```markdown
See [guide](scripts/helper.py)
```

### 4. Tool Permissions

❌ **Too broad**:
```yaml
tools: Bash  # Allows ANY bash command!
```

✅ **Specific**:
```yaml
allowed-tools: Bash(git*), Bash(npm test:*)
```

## Resources

### Official Links

- **Docs**: https://docs.claude.com/en/docs/claude-code/overview
- **Skills**: https://docs.claude.com/en/docs/claude-code/skills
- **Marketplace**: https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
- **SDK**: https://docs.claude.com/en/api/agent-sdk/overview
- **GitHub**: https://github.com/anthropics/claude-code

### Example Repositories

- **Official Skills**: https://github.com/anthropics/skills
- **Official Plugins**: https://github.com/anthropics/claude-code
- **Cookbook**: https://github.com/anthropics/claude-cookbooks/tree/main/skills

### Community Resources

- **Discord**: https://www.anthropic.com/discord
- **Support**: https://support.claude.com/

## Version Information

- **Documentation Version**: October 2025
- **Claude Code**: v1.0+
- **Claude Model**: Sonnet 4.5
- **Skills**: Released Oct 16, 2025
- **Marketplace**: Released Oct 9, 2025
- **SDK**: Latest (formerly Claude Code SDK)

## Next Steps

1. **Read 00-OVERVIEW.md** for architecture
2. **Read 04-SKILLS.md** for the NEW feature
3. **Read 08-EXAMPLES.md** for practical patterns
4. **Start building!**

## Support

For issues or questions:
1. Check troubleshooting sections in each doc
2. Review examples in `08-EXAMPLES.md`
3. Consult official docs (links above)
4. Ask in Discord community

