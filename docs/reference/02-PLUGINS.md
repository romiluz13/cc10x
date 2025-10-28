# Plugin System

## Overview

Plugins package multiple components (commands, agents, skills, hooks, MCP servers) into distributable extensions.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: Manifest
├── commands/                 # Slash commands
│   ├── status.md
│   └── deploy.md
├── agents/                   # Subagents
│   ├── security-reviewer.md
│   └── performance-tester.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/
│   └── hooks.json           # Event handlers
├── .mcp.json                # MCP server config
├── scripts/                 # Utility scripts
│   ├── security-scan.sh
│   └── format-code.py
└── README.md
```

**CRITICAL**: All component directories (commands/, agents/, skills/, hooks/) must be at plugin root, NOT inside `.claude-plugin/`!

## Plugin Manifest (plugin.json)

### Minimal Example

```json
{
  "name": "plugin-name",
  "version": "2.0.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name"
  }
}
```

### Complete Example

```json
{
  "name": "deployment-tools",
  "version": "2.1.0",
  "description": "Deployment automation tools",
  "author": {
    "name": "Dev Team",
    "email": "dev@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["deployment", "ci-cd"],
  
  // Custom component paths (optional)
  "commands": ["./custom/commands/"],
  "agents": ["./custom/agents/"],
  "skills": "./skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json"
}
```

## Component Types

### 1. Commands (Slash Commands)

Location: `commands/`

File: `commands/deploy.md`
```markdown
---
description: Deploy to production
argument-hint: [environment]
---

# Deploy Command

Deploy application to specified environment.
```

Invocation:
```bash
/deploy production
# Or with plugin prefix
/plugin-name:deploy production
```

### 2. Agents (Subagents)

Location: `agents/`

File: `agents/security-reviewer.md`
```markdown
---
description: Security code review specialist
---

# Security Reviewer

Expert in security vulnerabilities and best practices.

## Review Checklist
- Input validation
- SQL injection risks
- XSS vulnerabilities
- ...
```

### 3. Skills (NEW!)

Location: `skills/`

File: `skills/code-reviewer/SKILL.md`
```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and maintainability. Use when reviewing code or PRs.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer Skill

Comprehensive code review following team standards.

## Review Process
1. Read changed files
2. Check security patterns
3. Verify test coverage
...
```

### 4. Hooks

Location: `hooks/hooks.json`

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

### 5. MCP Servers

Location: `.mcp.json`

```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

## Plugin Manifest Fields

### Required

- `name`: Unique identifier (kebab-case)

### Metadata (Optional)

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Semantic version |
| `description` | string | Brief explanation |
| `author` | object | {name, email, url} |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | License identifier |
| `keywords` | array | Discovery tags |

### Component Paths (Optional)

| Field | Type | Description |
|-------|------|-------------|
| `commands` | string\|array | Custom command paths |
| `agents` | string\|array | Custom agent paths |
| `skills` | string | Custom skills path |
| `hooks` | string\|object | Hook config or inline |
| `mcpServers` | string\|object | MCP config or inline |

## Path Behavior

**Important**: Custom paths SUPPLEMENT default directories!

Example:
```json
{
  "commands": ["./specialized/deploy.md"]
}
```

This loads:
1. Default `commands/` directory
2. PLUS `./specialized/deploy.md`

## Environment Variables

**`${CLAUDE_PLUGIN_ROOT}`**: Absolute path to plugin directory

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

## Plugin Commands

```bash
# Install plugin
/plugin install plugin-name@marketplace-name

# Enable disabled plugin
/plugin enable plugin-name@marketplace-name

# Disable plugin (keep installed)
/plugin disable plugin-name@marketplace-name

# Uninstall plugin
/plugin uninstall plugin-name@marketplace-name

# List all plugins
/plugin

# Browse and install (interactive)
/plugin
# > Browse Plugins
```

## Development Workflow

### 1. Create Plugin Structure

```bash
mkdir my-plugin
cd my-plugin
mkdir -p .claude-plugin commands agents skills hooks
```

### 2. Create Manifest

`.claude-plugin/plugin.json`:
```json
{
  "name": "my-plugin",
  "version": "2.0.0",
  "description": "My custom plugin",
  "author": {"name": "Your Name"}
}
```

### 3. Add Components

Add commands, agents, skills, etc. to respective directories.

### 4. Test Locally

```bash
# Create test marketplace
mkdir test-marketplace
cd test-marketplace
mkdir .claude-plugin

# Create marketplace.json
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "test-marketplace",
  "owner": {"name": "Developer"},
  "plugins": [{
    "name": "my-plugin",
    "source": "./my-plugin"
  }]
}
EOF

# Add marketplace
/plugin marketplace add ./test-marketplace

# Install plugin
/plugin install my-plugin@test-marketplace
```

### 5. Iterate

After changes:
```bash
/plugin uninstall my-plugin@test-marketplace
/plugin install my-plugin@test-marketplace
```

## Debugging

```bash
# Run with debug output
claude --debug

# Validate plugin
claude plugin validate .

# Check structure
tree -a my-plugin/
```

Look for:
```
[DEBUG] Loading plugin: my-plugin
[DEBUG] Found commands: ...
[DEBUG] Found agents: ...
[DEBUG] Found skills: ...
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Plugin not loading | Invalid JSON | Validate JSON syntax |
| Commands not appearing | Wrong directory | Ensure `commands/` at root |
| Hooks not firing | Script not executable | `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use env variable |
| Path errors | Absolute paths | Use relative paths |

## Best Practices

1. **Single purpose per plugin** - One clear responsibility
2. **Clear documentation** - README.md with examples
3. **Version properly** - Use semantic versioning
4. **Test thoroughly** - Use local marketplace
5. **Organize logically** - Group related components
6. **Use environment variables** - `${CLAUDE_PLUGIN_ROOT}`
7. **Avoid absolute paths** - Keep portable
8. **Document dependencies** - List required tools/packages

## Distribution

Once tested:

1. **Push to Git** (GitHub/GitLab)
2. **Create marketplace.json** in separate repo
3. **Share marketplace URL**: `owner/repo`
4. **Users install**: `/plugin marketplace add owner/repo`

## Semantic Versioning

Follow semver (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes (2.0.0)
- **MINOR**: New features (1.1.0)
- **PATCH**: Bug fixes (1.0.1)

Update `version` in `plugin.json` on each release.

