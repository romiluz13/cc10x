# Research Overview: Claude Code Plugins, Skills, and Sub-Agents

## Executive Summary

After conducting extensive research across 15+ repositories, official Anthropic documentation, and successful marketplace implementations, this document synthesizes the key findings about Claude Code's plugin ecosystem.

## Research Scope

**Primary Sources:**
- Official Anthropic documentation and cookbooks
- 3 major plugin marketplaces (EveryInc, jeremylongshore, ananddtyagi)
- 12+ individual plugin implementations
- Community resources and best practices

**Research Questions:**
1. What is a Claude Code plugin marketplace?
2. How do Claude Skills work?
3. How do Claude Sub-Agents work?
4. What file structures are required?
5. How are plugins installed and deployed?
6. What are common patterns and anti-patterns?

## Key Discoveries

### 1. Three Valid Architecture Patterns

**Pattern A: Single Plugin**
```
repo/
  .claude-plugin/
    plugin.json
  agents/
  commands/
  skills/
  hooks/
```
Used by: Individual plugins, focused tools
Installation: `/plugin install plugin-name@repo-name`

**Pattern B: Pure Marketplace**
```
repo/
  .claude-plugin/
    marketplace.json
  plugins/
    plugin-a/
      .claude-plugin/plugin.json
      agents/
      commands/
    plugin-b/
      ...
```
Used by: EveryInc, ananddtyagi, jeremylongshore
Installation: `/plugin marketplace add owner/repo` then `/plugin install plugin-name@marketplace-name`

**Pattern C: Hybrid (Rare)**
```
repo/
  .claude-plugin/
    plugin.json
    marketplace.json
  agents/           ← Main plugin
  commands/
  plugins/          ← Additional plugins
    plugin-a/
```
Used by: Advanced use cases only
NOT RECOMMENDED for most projects

### 2. Critical File Specifications

**plugin.json (Required for plugins)**
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": {
    "name": "Author Name",
    "email": "email@example.com",
    "url": "https://github.com/username"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/owner/repo.git"
  },
  "homepage": "https://github.com/owner/repo",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "commands": "./commands/",     // Optional
  "agents": "./agents/",         // Optional
  "skills": "./skills/",         // Optional
  "hooks": "./hooks/"            // Optional
}
```

**marketplace.json (Required for marketplaces)**
```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name",
    "email": "email@example.com",
    "url": "https://github.com/owner"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0",
    "homepage": "https://example.com"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "author": { "name": "Author" },
      "homepage": "https://example.com",
      "keywords": ["tag1"],
      "category": "productivity"
    }
  ]
}
```

### 3. Component Types

**Commands** - User-invoked workflows
- Format: Markdown files with YAML frontmatter
- Location: `/commands/*.md`
- Invocation: `/command-name`
- Example: `/feature-plan`, `/bug-fix`

**Sub-Agents** - Specialized AI workers
- Format: Markdown files with YAML frontmatter
- Location: `/agents/*.md`
- Invocation: Automatic based on context or explicit via task delegation
- Example: security-reviewer, implementer

**Skills** - Domain expertise that auto-invokes
- Format: `SKILL.md` in named subdirectory
- Location: `/skills/skill-name/SKILL.md`
- Invocation: Automatic when Claude detects relevance
- Example: TDD, security-patterns, UI-design

**Hooks** - Event-driven automation
- Format: Shell scripts + JSON configuration
- Location: `/hooks/hooks.json` + `/hooks/*.sh`
- Triggers: session-start, pre-compact, post-edit
- Example: Auto-healing context, progress tracking

### 4. Token Efficiency Patterns

**Progressive Loading** (from best practices):
- Stage 1: Load only plugin metadata (~5k tokens)
- Stage 2: Load active command/agent (~10-15k tokens)
- Stage 3: Load relevant skills on-demand
- Result: 93% token savings vs loading everything upfront

**Auto-Healing Context** (advanced pattern):
- Monitor token usage
- At 75% threshold, create snapshot
- Compact context by summarizing
- Restore essential state
- Continue seamlessly

### 5. Common Anti-Patterns

❌ **DON'T: Mix plugin.json and marketplace.json at root**
- Causes structural confusion
- Claude Code can't determine what to load

❌ **DON'T: Use incorrect source paths in marketplace**
- `"source": "./"` for marketplace is wrong
- Should be `"source": "./plugins/plugin-name"`

❌ **DON'T: Forget YAML frontmatter**
- Commands, agents, skills MUST have YAML headers
- Missing frontmatter = component not recognized

❌ **DON'T: Parallelize implementers**
- Multiple agents editing same files = conflicts
- Use sequential execution for implementation
- Parallelize only for analysis tasks

✅ **DO: Follow established patterns**
- Study successful implementations
- Use consistent directory structure
- Include comprehensive README

✅ **DO: Test thoroughly**
- Install locally before publishing
- Verify all commands work
- Check agent invocation
- Confirm skill auto-activation

## Architecture Decision: cc10x

**Problem:** cc10x had both plugin.json AND marketplace.json at root with agents/commands/skills directly in root directory.

**Analysis:**
- Goals: Single orchestration system with 4 commands, 7 agents, 16 skills
- Use case: Not distributing multiple plugins, just one comprehensive tool
- Pattern match: Single Plugin (Pattern A)

**Solution:**
- Remove marketplace.json
- Update plugin.json with component paths
- Keep existing directory structure
- Install as single plugin

**Rationale:**
- Aligns with project goals (one tool, not many)
- Simpler for users (one installation command)
- Easier to maintain (no marketplace complexity)
- Matches successful examples like compounding-engineering

## Installation Workflows

**For Single Plugin:**
```bash
# Add repository as plugin source
/plugin marketplace add owner/repo-name

# Install the plugin
/plugin install plugin-name@repo-name

# Verify commands work
/command-name
```

**For Marketplace Plugins:**
```bash
# Add marketplace
/plugin marketplace add owner/marketplace-repo

# Browse available plugins
/plugin

# Install specific plugin
/plugin install plugin-name@marketplace-name

# Verify
/command-name
```

## Success Metrics

Based on research, a successful plugin should:

1. ✅ **Discoverable**: Shows up in `/plugin` list after marketplace add
2. ✅ **Installable**: Installs without errors
3. ✅ **Functional**: Commands execute correctly
4. ✅ **Integrated**: Agents invoke automatically when relevant
5. ✅ **Smart**: Skills auto-activate based on context
6. ✅ **Documented**: Clear README with examples
7. ✅ **Maintained**: Version tracking, changelog, issues

## Next Steps

1. Implement Single Plugin pattern for cc10x
2. Remove marketplace.json
3. Update plugin.json with component paths
4. Test installation workflow
5. Document for users

## References

See detailed documentation in:
- 01-OFFICIAL-DOCS.md - Anthropic resources
- 02-MARKETPLACE-EXAMPLES.md - Successful marketplaces
- 03-PLUGIN-EXAMPLES.md - Individual plugin analysis
- 04-FILE-STRUCTURES.md - Detailed specifications
- 05-SKILLS-DEEP-DIVE.md - Skills system
- 06-SUB-AGENTS-DEEP-DIVE.md - Sub-agents system
- 07-COMMANDS-DEEP-DIVE.md - Commands system
- 08-INSTALLATION-GUIDE.md - Installation procedures
- 09-REPOSITORIES-LIST.md - All analyzed repositories

