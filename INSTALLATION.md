# cc10x Installation Guide

## Method 1: Register as Known Marketplace (Recommended)

This method allows you to use `/plugin` commands in Claude Code.

### Step 1: Edit Claude Code Settings

Open or create `~/.claude/settings.json` and add:

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

### Step 2: Install in Claude Code

```bash
/plugin marketplace add cc10x
/plugin install cc10x@cc10x
```

### Step 3: Verify

```bash
/feature-plan Test
```

You should see the feature planning command interface!

---

## Method 2: Manual Installation (Quick Start)

Copy files directly to your project:

```bash
# Navigate to your project
cd /path/to/your-project

# Clone cc10x
git clone https://github.com/romiluz13/cc10x.git /tmp/cc10x

# Copy components
cp -r /tmp/cc10x/.claude-plugin .
cp -r /tmp/cc10x/commands .
cp -r /tmp/cc10x/agents .
cp -r /tmp/cc10x/skills .
cp -r /tmp/cc10x/hooks .

# Clean up
rm -rf /tmp/cc10x
```

### Verify Installation

In Claude Code:

```bash
/feature-plan Test
```

---

## Method 3: Development Mode (Symlinks)

For development, use symlinks to avoid copying files:

```bash
# Navigate to your project
cd /path/to/your-project

# Create symlinks
ln -s /Users/rom.iluz/Dev/cc10x_v2/.claude-plugin .
ln -s /Users/rom.iluz/Dev/cc10x_v2/commands .
ln -s /Users/rom.iluz/Dev/cc10x_v2/agents .
ln -s /Users/rom.iluz/Dev/cc10x_v2/skills .
ln -s /Users/rom.iluz/Dev/cc10x_v2/hooks .
```

Changes to cc10x source files are immediately reflected!

---

## Troubleshooting

### Commands Don't Appear

**Issue:** Typing `/feature-plan` doesn't show the command

**Solutions:**
1. Verify `.claude-plugin/plugin.json` exists in your project
2. Check that `commands/` directory contains `.md` files
3. Restart Claude Code
4. Try in a trusted directory (Claude Code may block untrusted locations)

### "Plugin Not Found" Error

**Issue:** `/plugin install` fails

**Solution:** Use Method 1 (extraKnownMarketplaces) or Method 2 (manual copy)

Claude Code's `/plugin install` command requires plugins to be registered in `~/.claude/settings.json`.

### YAML Frontmatter Errors

**Issue:** Commands/agents don't load

**Solution:** 
1. Check all `.md` files have valid YAML frontmatter
2. Ensure `---` delimiters are present
3. Validate YAML syntax (no tabs, proper spacing)

### Hooks Don't Execute

**Issue:** Session-start hooks don't run

**Solution:**
1. Verify `hooks/hooks.json` exists
2. Check shell scripts are executable: `chmod +x hooks/*.sh`
3. Review Claude Code logs for hook execution errors

---

## What Gets Installed

When you install cc10x, you get:

- **5 Commands**: `/feature-plan`, `/feature-build`, `/bug-fix`, `/review`, `/validate`
- **7 Sub-Agents**: implementer, context-analyzer, security-reviewer, quality-reviewer, performance-analyzer, ux-reviewer, accessibility-reviewer
- **16 Skills**: TDD, systematic-debugging, security-patterns, performance-patterns, accessibility-patterns, ui-design, and more
- **3 Hooks**: session-start, pre-compact, auto-healing context

All components work together seamlessly through intelligent orchestration.

---

## Next Steps

After installation:

1. **Read the docs**: Check `README.md` for usage examples
2. **Try feature planning**: `/feature-plan Add user authentication`
3. **Build a feature**: `/feature-build Implement the planned feature`
4. **Review code**: `/review src/`
5. **Read the constitution**: `.claude/memory/CONSTITUTION.md` for development principles

---

## Uninstallation

To remove cc10x from a project:

```bash
cd /path/to/your-project

rm -rf .claude-plugin
rm -rf commands
rm -rf agents
rm -rf skills
rm -rf hooks
```

To remove from global settings:

Edit `~/.claude/settings.json` and remove the `cc10x` entry from `extraKnownMarketplaces`.

---

## Support

- **Issues**: https://github.com/romiluz13/cc10x/issues
- **Documentation**: https://github.com/romiluz13/cc10x
- **License**: MIT

