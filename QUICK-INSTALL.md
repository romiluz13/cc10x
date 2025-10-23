# Quick Install cc10x

## The Simple Way (Copy Files)

This works immediately, no configuration needed:

```bash
# 1. Clone cc10x
git clone https://github.com/romiluz13/cc10x.git /tmp/cc10x

# 2. Go to your project
cd /path/to/your/project

# 3. Copy all components
cp -r /tmp/cc10x/.claude-plugin .
cp -r /tmp/cc10x/commands .
cp -r /tmp/cc10x/agents .
cp -r /tmp/cc10x/skills .
cp -r /tmp/cc10x/hooks .

# 4. Clean up
rm -rf /tmp/cc10x
```

## Verify It Works

Open your project in Claude Code and type:

```bash
/feature-plan Test feature
```

You should see the feature planning interface! 🎉

---

## All Available Commands

Once installed, you have:

- `/feature-plan` - Comprehensive PRD-style planning
- `/feature-build` - TDD-enforced implementation
- `/bug-fix` - Systematic debugging (LOG FIRST)
- `/review` - Multi-dimensional code review
- `/validate` - Cross-artifact validation

---

## Advanced: Register as Marketplace

If you want to use `/plugin` commands, add this to `~/.claude/settings.json`:

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

Then:
```bash
/plugin marketplace add cc10x
/plugin install cc10x@cc10x
```

But the simple copy method above works perfectly and is faster!

---

## Troubleshooting

**Commands don't appear?**
- Restart Claude Code
- Make sure you're in a trusted directory
- Check that `.claude-plugin/plugin.json` exists

**Still issues?**
- Open an issue: https://github.com/romiluz13/cc10x/issues

