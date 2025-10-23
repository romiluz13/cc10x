# cc10x Marketplace Installation Guide

## Overview

cc10x is a Claude Code marketplace that distributes the cc10x plugin - a comprehensive orchestration system for 10x developer productivity.

---

## Method 1: Via Marketplace (Recommended)

This is the official and easiest installation method.

### Step 1: Add the Marketplace

```bash
/plugin marketplace add romiluz13/cc10x
```

This registers cc10x as a known marketplace in Claude Code.

### Step 2: Install the Plugin

```bash
/plugin install cc10x@cc10x
```

This installs the cc10x plugin from the cc10x marketplace.

### Step 3: Verify

```bash
/feature-plan Test
```

You should see the feature planning command interface!

---

## Method 2: Via Settings File

For advanced users or automation, you can edit Claude Code settings directly.

### Edit Settings

Open or create `~/.claude/settings.json`:

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

Then restart Claude Code. The plugin will be automatically available.

---

## What Gets Installed

When you install cc10x, you get the complete plugin:

### 5 Commands

- `/feature-plan` - Comprehensive PRD-style planning with risk assessment
- `/feature-build` - 5-phase TDD-enforced implementation
- `/bug-fix` - Systematic debugging with LOG FIRST pattern
- `/review` - Multi-dimensional parallel code review (5 dimensions)
- `/validate` - Cross-artifact consistency validation

### 7 Sub-Agents

- `implementer` - Writes production code with TDD
- `context-analyzer` - Finds patterns in your codebase
- `security-reviewer` - Security audits (OWASP)
- `quality-reviewer` - Code quality checks
- `performance-analyzer` - Performance optimization
- `ux-reviewer` - UX improvements
- `accessibility-reviewer` - WCAG 2.1 AA compliance

### 16 Skills

- feature-planning, feature-building, bug-fixing
- test-driven-development, code-generation
- systematic-debugging, safe-refactoring
- security-patterns, performance-patterns
- accessibility-patterns, ux-patterns
- ui-design, code-reviewing, code-review-patterns
- codebase-navigation, verification-before-completion

### 3 Hooks

- `session-start` - Initialize on session start
- `pre-compact` - Context preservation
- Auto-healing context management

---

## Verification Steps

### 1. Check Plugin Installed

```bash
/plugin list
```

You should see `cc10x@cc10x` in the list.

### 2. Test Commands

Try each command:

```bash
/feature-plan Add user authentication
/review src/
/validate .
```

### 3. Check Agent Loading

Commands will automatically invoke sub-agents. Watch for agent loading messages in Claude Code.

### 4. Verify Skills Active

Skills auto-activate on trigger phrases. Try mentioning "TDD" or "security" in a conversation.

---

## Troubleshooting

### Commands Don't Appear

**Issue:** Typing `/feature-plan` doesn't show the command

**Solutions:**
1. Restart Claude Code
2. Verify plugin installed: `/plugin list`
3. Check you're in a trusted directory
4. Try reinstalling: 
   ```bash
   /plugin uninstall cc10x@cc10x
   /plugin install cc10x@cc10x
   ```

### Marketplace Not Found

**Issue:** `/plugin marketplace add romiluz13/cc10x` fails

**Solutions:**
1. Check internet connection
2. Try full URL: `/plugin marketplace add https://github.com/romiluz13/cc10x`
3. Manual settings method (Method 2 above)

### Plugin Installation Fails

**Issue:** `/plugin install cc10x@cc10x` fails

**Solutions:**
1. Ensure marketplace is added first
2. Check Claude Code has permissions
3. View logs for specific error
4. Try via settings file (Method 2)

### YAML/Syntax Errors

**Issue:** Plugin loads but commands fail

**Solution:** Report this as a bug at https://github.com/romiluz13/cc10x/issues - this shouldn't happen in v1.1.0!

---

## Uninstallation

To remove cc10x:

```bash
# Remove the plugin
/plugin uninstall cc10x@cc10x

# Remove the marketplace (optional)
/plugin marketplace remove cc10x
```

Or manually edit `~/.claude/settings.json` to remove the `cc10x` entries.

---

## Next Steps

After installation:

1. **Read the docs**: Check [README.md](./README.md) for usage examples
2. **Try feature planning**: `/feature-plan Add user authentication`
3. **Build a feature**: `/feature-build Implement the planned feature`
4. **Review code**: `/review src/`
5. **Read the constitution**: View development principles

---

## Support

- **Issues**: https://github.com/romiluz13/cc10x/issues
- **Documentation**: https://github.com/romiluz13/cc10x
- **License**: MIT

---

## System Requirements

- Claude Code version 1.0 or later
- Internet connection (for marketplace installation)
- Trusted project directory
