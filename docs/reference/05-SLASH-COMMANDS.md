# Slash Commands

## Overview

Slash commands are **user-invoked** shortcuts (not model-invoked like Skills).

```bash
/command-name [arguments]
```

## Commands vs Skills

| Feature | Slash Commands | Skills |
|---------|----------------|--------|
| **Invocation** | User types `/cmd` | Model chooses automatically |
| **Use Case** | Quick prompts | Complex capabilities |
| **Structure** | Single .md file | SKILL.md + resources |
| **Arguments** | Yes ($1, $2, $ARGUMENTS) | No |
| **Bash Execution** | Yes (!`command`) | Via scripts |
| **File References** | Yes (@file) | Via references |

## File Locations

```
Project commands:
.claude/commands/*.md

User commands:
~/.claude/commands/*.md

Plugin commands:
<plugin>/commands/*.md
```

## File Format

```markdown
---
description: Brief command description
argument-hint: [arg1] [arg2]  # Optional
allowed-tools: Bash(git*)     # Optional
model: sonnet                  # Optional
disable-model-invocation: true # Optional
---

Command prompt content here.
Use $ARGUMENTS or $1, $2 for parameters.
```

## Simple Example

File: `.claude/commands/review.md`

```markdown
---
description: Review code for bugs and improvements
---

Review this code for:
- Security vulnerabilities
- Performance issues  
- Code style violations
```

Usage:
```bash
/review
# Claude reviews current code
```

## Arguments Example

### Using $ARGUMENTS (all args as string)

File: `.claude/commands/fix-issue.md`

```markdown
---
description: Fix GitHub issue
argument-hint: [issue-number]
---

Fix issue #$ARGUMENTS following our coding standards and best practices.
```

Usage:
```bash
/fix-issue 123
# $ARGUMENTS becomes "123"

/fix-issue 123 high-priority
# $ARGUMENTS becomes "123 high-priority"
```

### Using Positional Args ($1, $2, $3...)

File: `.claude/commands/review-pr.md`

```markdown
---
description: Review pull request
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

Usage:
```bash
/review-pr 456 high alice
# $1 = "456"
# $2 = "high"
# $3 = "alice"
```

## Bash Command Execution

Execute bash commands BEFORE command runs using `!` prefix:

File: `.claude/commands/commit.md`

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your Task

Based on the above changes, create a single git commit.
```

The `!` prefix executes commands and includes output in context.

## File References

Include file contents using `@` prefix:

```markdown
Review the implementation in @src/utils/helpers.js

Compare @src/old-version.js with @src/new-version.js
```

## Extended Thinking

Trigger extended thinking by including keywords:

```markdown
Think carefully and analyze the following code...
```

## Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `description` | Brief description (required if no content) | `Review code for issues` |
| `argument-hint` | Argument guide for autocomplete | `[filename] [priority]` |
| `allowed-tools` | Restrict tools command can use | `Bash(git*), Read, Grep` |
| `model` | Override model | `sonnet`, `opus`, `haiku` |
| `disable-model-invocation` | Prevent SlashCommand tool from calling | `true` |

## Complete Example

File: `.claude/commands/security-scan.md`

```markdown
---
description: Security scan of codebase
argument-hint: [directory]
allowed-tools: Bash(grep*), Bash(find*), Read, Grep
model: opus
---

# Security Scan

Scan directory: ${1:-.}

## Check for:
- Hardcoded secrets
- SQL injection risks
- XSS vulnerabilities
- Insecure dependencies
- Exposed API keys

## Commands to run:
!`git ls-files ${1:-.} | head -20`

Review files for security issues.
```

Usage:
```bash
/security-scan src/
```

## Namespacing with Subdirectories

Organize commands in subdirectories:

```
.claude/commands/
├── frontend/
│   ├── component.md
│   └── style.md
└── backend/
    ├── api.md
    └── database.md
```

- Subdirectory appears in description: "(project:frontend)"
- Command name remains simple: `/component`
- File `frontend/component.md` → command `/component`

## Plugin Commands

Plugins can provide commands:

```
my-plugin/
└── commands/
    └── deploy.md
```

Invocation:
```bash
/deploy              # Direct (if no conflicts)
/my-plugin:deploy    # Prefixed (always works)
```

## MCP Commands

MCP servers can expose prompts as commands:

```bash
/mcp__github__list_prs
/mcp__github__pr_review 456
```

Format: `/mcp__<server>__<prompt>` [args]

## SlashCommand Tool

**NEW**: Claude can invoke slash commands via `SlashCommand` tool!

Requirements:
- Command must have `description` field
- Command must NOT have `disable-model-invocation: true`

Example:
```markdown
> Run /write-unit-test when writing tests
```

Claude can now call `/write-unit-test` automatically.

### Disable SlashCommand Tool

```bash
/permissions
# Add to deny rules: SlashCommand
```

Or for specific command:
```yaml
disable-model-invocation: true
```

### Character Budget

SlashCommand tool has 15k character budget for descriptions.

Set custom limit:
```bash
export SLASH_COMMAND_TOOL_CHAR_BUDGET=20000
```

## Management Commands

```bash
# View all commands
/help

# Interactive command list
/plugin
```

Built-in commands:
- `/add-dir`, `/agents`, `/bug`, `/clear`
- `/compact`, `/config`, `/cost`, `/doctor`
- `/help`, `/init`, `/login`, `/logout`
- `/mcp`, `/memory`, `/model`, `/permissions`
- `/pr_comments`, `/review`, `/sandbox`, `/rewind`
- `/status`, `/terminal-setup`, `/usage`, `/vim`

## Creating Commands

### Step 1: Create File

```bash
# Project command
mkdir -p .claude/commands
cat > .claude/commands/optimize.md << 'EOF'
---
description: Analyze code for performance issues
argument-hint: [file-path]
---

Analyze this code for performance issues and suggest optimizations:
@$1
EOF
```

### Step 2: Use Command

```bash
/optimize src/utils.js
```

### Step 3: Iterate

Edit `.claude/commands/optimize.md` and changes take effect next run.

## Best Practices

1. **Clear descriptions** - Users need to understand what command does
2. **Argument hints** - Help users know what to pass
3. **Specific prompts** - Better than vague instructions
4. **Use file references** - `@file` includes content
5. **Bash for context** - `!`command`` adds dynamic info
6. **Tool restrictions** - Limit to necessary tools
7. **Version control** - Commit project commands to git

## Common Patterns

### Code Review

```markdown
---
description: Review code for quality
---

Review @$1 for:
- Logic errors
- Security issues
- Performance problems
- Code style
```

### Documentation Generation

```markdown
---
description: Generate API documentation
argument-hint: [source-file]
---

Generate comprehensive API documentation for @$1 including:
- Function signatures
- Parameter descriptions
- Return values
- Usage examples
```

### Testing

```markdown
---
description: Generate unit tests
argument-hint: [file-to-test]
---

Generate comprehensive unit tests for @$1:
- Cover all functions
- Edge cases
- Error conditions
- Integration scenarios
```

## Debugging

**Command not appearing?**

```bash
/help
# Check if command is listed

ls .claude/commands/
# Verify file exists

cat .claude/commands/my-command.md
# Check YAML is valid
```

**Arguments not working?**

- Use `$ARGUMENTS` for all args as string
- Use `$1`, `$2` etc. for individual args
- Check `argument-hint` matches usage

**Bash execution failing?**

- Ensure `allowed-tools` includes `Bash(command:*)`
- Check command syntax
- Test command manually first

## Examples Repository

See official examples:
```bash
/plugin marketplace add anthropics/claude-code
/plugin install example-commands
```

