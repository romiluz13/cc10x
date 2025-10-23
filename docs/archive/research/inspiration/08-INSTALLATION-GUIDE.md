# Installation Guide

## Installation Methods

### Method 1: Via Plugin Marketplace (Recommended)

```bash
# Add the repository as a plugin marketplace
/plugin marketplace add romiluz13/cc10x

# Install the plugin
/plugin install cc10x@cc10x

# Verify installation
/feature-plan Test
```

### Method 2: Via GitHub URL

```bash
# Add using full GitHub URL
/plugin marketplace add https://github.com/romiluz13/cc10x

# Install
/plugin install cc10x@cc10x
```

### Method 3: Manual Installation

```bash
# Clone the repository
git clone https://github.com/romiluz13/cc10x.git

# Copy to project
cd your-project
cp -r /path/to/cc10x/.claude-plugin .
cp -r /path/to/cc10x/agents .
cp -r /path/to/cc10x/commands .
cp -r /path/to/cc10x/skills .
cp -r /path/to/cc10x/hooks .

# Restart Claude Code
```

## Verification Steps

### 1. Check Plugin Installed

```bash
/plugin
# Should show cc10x in the list
```

### 2. Test Commands

```bash
/feature-plan "Test feature"
# Should start feature planning workflow
```

### 3. Verify Agents

```bash
/agents
# Should list: context-analyzer, implementer, security-reviewer, etc.
```

### 4. Check Skills

Skills auto-load at session start. Try:

```
"I need to implement a new feature with test-driven development"
# Should activate TDD skill automatically
```

## Troubleshooting

### Plugin Not Showing Up?

**Problem:** `/plugin` doesn't list cc10x

**Solutions:**
1. Check you added marketplace: `/plugin marketplace add romiluz13/cc10x`
2. Verify you're in a trusted directory
3. Restart Claude Code
4. Check `.claude-plugin/plugin.json` exists

### Commands Not Working?

**Problem:** `/feature-plan` not recognized

**Solutions:**
1. Verify plugin installed: `/plugin`
2. Check commands directory: `ls commands/`
3. Verify YAML frontmatter in command files
4. Restart Claude Code session

### Agents Not Invoking?

**Problem:** Sub-agents not activating

**Solutions:**
1. Check `.claude/agents/` or `~/.claude/agents/`
2. Verify YAML frontmatter valid
3. Check agent descriptions have clear triggers
4. Use `/agents` to list available agents

### Skills Not Auto-Activating?

**Problem:** Skills don't trigger automatically

**Solutions:**
1. Check `skills/*/SKILL.md` structure
2. Verify YAML frontmatter complete
3. Check trigger phrases in description
4. Try explicit phrases from skill descriptions

## Updating

### Update Plugin

```bash
# Pull latest changes
cd /path/to/cc10x
git pull origin main

# If manually installed, copy files again
cp -r .claude-plugin /your/project/
cp -r agents /your/project/
# ... etc

# Or reinstall via marketplace
/plugin remove cc10x
/plugin install cc10x@cc10x
```

### Check Version

```bash
# Check plugin.json for version
cat .claude-plugin/plugin.json | grep version
```

## Uninstallation

### Via Plugin Manager

```bash
/plugin remove cc10x
```

### Manual Removal

```bash
# Remove from project
rm -rf .claude-plugin
rm -rf agents
rm -rf commands
rm -rf skills
rm -rf hooks

# Or keep .claude-plugin but remove marketplace reference
# Edit .claude/settings.json
```

## Configuration

### Project-Level Settings

Create `.claude/settings.json`:

```json
{
  "cc10x": {
    "tdd": {
      "enforceStrict": true
    },
    "progressive_loading": {
      "enabled": true
    },
    "auto_healing": {
      "threshold": 0.75
    }
  }
}
```

### User-Level Settings

Edit `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "cc10x": {
      "source": {
        "source": "github",
        "repo": "romiluz13/cc10x"
      }
    }
  },
  "enabledPlugins": {
    "cc10x@cc10x": true
  }
}
```

## Requirements

- Claude Code version 1.0 or later
- Git (for cloning repositories)
- Trusted project directory
- Terminal access (for some features)

## Post-Installation

### 1. Read Documentation

```bash
# In project root
cat README.md
cat CLAUDE.md
```

### 2. Try Commands

```bash
/feature-plan "Simple test feature"
/bug-fix "Test bug description"
/review src/
```

### 3. Configure Memory

Create memory files:

```bash
mkdir -p .claude/memory
echo "# Current Priorities" > .claude/memory/WORKING_PLAN.md
echo "# Important Context" > .claude/memory/REMEMBER.md
```

### 4. Set Up Hooks (Optional)

Hooks should work automatically if `/hooks/hooks.json` exists.

Verify:
```bash
cat hooks/hooks.json
```

## Getting Help

- **Issues:** https://github.com/romiluz13/cc10x/issues
- **Discussions:** https://github.com/romiluz13/cc10x/discussions
- **Documentation:** Check README.md and CLAUDE.md
- **Examples:** See commands/ and agents/ for examples

## Common Installation Scenarios

### Scenario 1: New Project

```bash
cd new-project
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x
/feature-plan "First feature"
```

### Scenario 2: Existing Project

```bash
cd existing-project
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x
/review src/  # Review existing code
```

### Scenario 3: Team Installation

Add to `.claude/settings.json` in repo:

```json
{
  "extraKnownMarketplaces": {
    "cc10x": {
      "source": {
        "source": "github",
        "repo": "romiluz13/cc10x"
      }
    }
  }
}
```

Team members: `/plugin install cc10x@cc10x`

## Success Checklist

✅ Plugin shows in `/plugin` list
✅ Commands work: `/feature-plan`
✅ Agents listed in `/agents`
✅ Skills auto-activate on trigger phrases
✅ Hooks execute (check logs)
✅ Memory files created
✅ Documentation accessible

## Next Steps

1. Read CLAUDE.md for usage guidance
2. Try `/feature-plan` on a real feature
3. Use `/review` on existing code
4. Customize settings if needed
5. Share with team

## Resources

- **Repository:** https://github.com/romiluz13/cc10x
- **Issues:** https://github.com/romiluz13/cc10x/issues
- **Discussions:** https://github.com/romiluz13/cc10x/discussions
- **Author:** rom.iluz13@gmail.com
