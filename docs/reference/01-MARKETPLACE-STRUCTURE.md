# Marketplace Structure

## Overview

Plugin marketplaces are JSON catalogs that list available plugins and describe where to find them.

## Marketplace File Location

```
<repository-root>/
└── .claude-plugin/
    └── marketplace.json
```

## Marketplace Schema

```json
{
  "name": "marketplace-identifier",
  "owner": {
    "name": "Team Name",
    "email": "team@example.com"
  },
  "metadata": {
    "description": "Optional marketplace description",
    "version": "2.0.0",
    "pluginRoot": "./plugins"  // Optional: base path for plugins
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./path-or-config",
      "description": "What this plugin does",
      "version": "2.0.0",
      "author": { "name": "Author" },
      "homepage": "https://docs.example.com",
      "repository": "https://github.com/user/repo",
      "license": "MIT",
      "keywords": ["tag1", "tag2"],
      "category": "productivity"
    }
  ]
}
```

## Plugin Source Types

### 1. Relative Path (same repo)

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

### 2. GitHub Repository

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

### 3. Git Repository

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Advanced Plugin Entry

```json
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "team@company.com"
  },
  "homepage": "https://docs.company.com/plugins",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  
  // Custom component paths
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": [
    "./agents/security-reviewer.md",
    "./agents/compliance-checker.md"
  ],
  "skills": "./skills/",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
        }]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false  // If false, plugin.json is optional
}
```

## Management Commands

```bash
# Add marketplace
/plugin marketplace add owner/repo                    # GitHub
/plugin marketplace add https://gitlab.com/repo.git   # Git
/plugin marketplace add ./local-marketplace           # Local
/plugin marketplace add https://url.of/marketplace.json  # Direct URL

# List marketplaces
/plugin marketplace list

# Update marketplace
/plugin marketplace update marketplace-name

# Remove marketplace
/plugin marketplace remove marketplace-name
```

## Team Configuration

Configure automatic marketplace installation in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    },
    "project-specific": {
      "source": {
        "source": "git",
        "url": "https://git.company.com/project-plugins.git"
      }
    }
  }
}
```

When team members trust the repository, Claude Code automatically:
1. Installs these marketplaces
2. Installs any plugins in `enabledPlugins` field

## Environment Variables

**`${CLAUDE_PLUGIN_ROOT}`** - Absolute path to plugin directory

Use in:
- Hook commands
- MCP server paths
- Script references

Example:
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
}
```

## Plugin Discovery Rules

1. **Priority order**:
   - Project plugins (`.claude/`) - Highest
   - User plugins (`~/.claude/`)
   - Plugin marketplace plugins

2. **Name conflicts**:
   - Project-level takes precedence
   - Commands: Can coexist with namespace prefix
   - Skills/Agents: Name must be unique

## Field Requirements

### Required

- `name`: kebab-case, no spaces, unique identifier
- `plugins`: Array of plugin entries

### Plugin Entry Required

- `name`: Plugin identifier (kebab-case)
- `source`: Where to fetch the plugin

### Plugin Entry Optional

- `description`: Brief explanation
- `version`: Semantic version
- `author`: { name, email, url }
- `homepage`: Documentation URL
- `repository`: Source code URL
- `license`: SPDX identifier (MIT, Apache-2.0)
- `keywords`: Array of discovery tags
- `category`: Organization category
- `tags`: Additional searchability tags
- `strict`: Require plugin.json (default: true)
- Component paths: `commands`, `agents`, `skills`, `hooks`, `mcpServers`

## Distribution Strategies

### GitHub (Recommended)

Pros:
- Built-in version control
- Issue tracking
- Team collaboration
- Easy distribution

Setup:
1. Create repository
2. Add `.claude-plugin/marketplace.json`
3. Share: `owner/repo`

### GitLab / Other Git

Works with any git hosting:
```bash
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Local Development

For testing before distribution:
```bash
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

## Validation

Check marketplace before sharing:
```bash
# Validate JSON syntax
claude plugin validate .

# Add for testing
/plugin marketplace add ./path/to/marketplace

# Install test plugin
/plugin install test-plugin@marketplace-name
```

## Best Practices

1. **Use GitHub for distribution** (easiest)
2. **Version plugins** (semantic versioning)
3. **Document thoroughly** (README.md)
4. **Test before sharing** (local marketplace)
5. **Organize by category** (productivity, security, etc.)
6. **Keep source paths relative** (portability)
7. **Use `${CLAUDE_PLUGIN_ROOT}`** (not absolute paths)

