# Subagents

## Overview

Subagents are specialized AI assistants with:
- **Separate context windows** (prevents context pollution)
- **Custom system prompts** (specific expertise)
- **Tool restrictions** (limited permissions)
- **Task delegation** (Claude can invoke them)

## Key Benefits

1. **Context Preservation**: Each subagent operates independently
2. **Specialized Expertise**: Domain-specific instructions
3. **Reusability**: Use across projects
4. **Flexible Permissions**: Different tool access per subagent

## File Locations

```
Project subagents:
.claude/agents/*.md

User subagents:
~/.claude/agents/*.md

Plugin subagents:
<plugin>/agents/*.md
```

Priority: Project > User > Plugin

## File Format

```markdown
---
name: subagent-name
description: When to use this subagent
tools: Read, Grep, Glob  # Optional
model: sonnet            # Optional: sonnet, opus, haiku, inherit
---

# Subagent Name

System prompt defining role, capabilities, and approach.

## Instructions
Step-by-step guidance.

## Best practices
...
```

## Configuration Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `name` | Yes | Lowercase, hyphens only | `code-reviewer` |
| `description` | Yes | When to use this agent | `Expert code review. Use after code changes.` |
| `tools` | No | Comma-separated tools | `Read, Grep, Glob` |
| `model` | No | Model to use | `sonnet`, `opus`, `haiku`, `inherit` |

### Tool Options

- **Omit `tools`**: Inherits all tools (default)
- **Specify tools**: Restrict to listed tools only

Available tools: Read, Edit, Write, Bash, Grep, Glob, Task, WebFetch, WebSearch, etc.

### Model Options

- **`sonnet`**: Fast, balanced (default for subagents)
- **`opus`**: Most capable
- **`haiku`**: Fastest, economical
- **`inherit`**: Use main conversation's model

## Creating Subagents

### Option 1: Using /agents Command (Recommended)

```bash
/agents
# > Create New Agent
# > Generate with Claude (recommended)
# Describe your subagent, select tools, Claude generates it
```

### Option 2: Manual Creation

```bash
# Project subagent
mkdir -p .claude/agents
cat > .claude/agents/code-reviewer.md << 'EOF'
---
name: code-reviewer
description: Expert code review. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: inherit
---

# Code Reviewer

Senior code reviewer ensuring quality and security.

## Review Process
1. Run git diff to see changes
2. Focus on modified files
3. Begin review immediately
...
EOF
```

## Example Subagents

### Code Reviewer

```markdown
---
name: code-reviewer
description: Expert code review. Use proactively after writing/modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

# Code Reviewer

Senior code reviewer ensuring quality and security.

## When Invoked
1. Run git diff to see recent changes
2. Focus on modified files  
3. Begin review immediately

## Review Checklist
- Code is simple and readable
- Functions well-named
- No duplicated code
- Proper error handling
- No exposed secrets
- Input validation
- Good test coverage
- Performance considered

## Feedback Format
**Critical** (must fix):
- Security issues
- Breaking bugs

**Warnings** (should fix):
- Performance concerns
- Maintainability

**Suggestions** (consider):
- Style improvements
- Optimizations

Include specific examples for fixes.
```

### Debugger

```markdown
---
name: debugger
description: Debug specialist for errors, test failures, unexpected behavior. Use when encountering issues.
tools: Read, Edit, Bash, Grep, Glob
---

# Debugger

Root cause analysis expert.

## When Invoked
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate failure location
4. Implement minimal fix
5. Verify solution

## Process
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

## Output
For each issue provide:
- Root cause explanation
- Supporting evidence
- Specific code fix
- Testing approach
- Prevention recommendations

Fix underlying issue, not symptoms.
```

### Data Scientist

```markdown
---
name: data-scientist
description: SQL and BigQuery expert. Use for data analysis, queries, and insights.
tools: Bash, Read, Write
model: sonnet
---

# Data Scientist

SQL and BigQuery specialist.

## When Invoked
1. Understand data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery CLI (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

## Best Practices
- Optimized queries with proper filters
- Appropriate aggregations and joins
- Comment complex logic
- Format results for readability
- Data-driven recommendations

## Output
For each analysis:
- Explain query approach
- Document assumptions
- Highlight key findings
- Suggest next steps

Ensure queries are efficient and cost-effective.
```

## Using Subagents

### Automatic Delegation

Claude automatically delegates based on:
- Task description
- Subagent `description` field
- Current context

To encourage proactive use, include in description:
- "Use PROACTIVELY"
- "MUST BE USED"

### Explicit Invocation

```bash
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my changes
> Ask the debugger subagent to investigate this error
```

## CLI-Based Configuration

Define subagents dynamically using `--agents` flag:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use after code changes.",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

Priority: CLI > Project > User

## Managing Subagents

### View Available Subagents

```bash
/agents
```

### Create New Subagent

```bash
/agents
# > Create New Agent
# Choose: project or user level
# Generate with Claude (recommended)
```

### Edit Subagent

```bash
/agents
# > Select existing agent
# > Edit
```

### Delete Subagent

```bash
/agents
# > Select agent
# > Delete

# Or manually
rm .claude/agents/subagent-name.md
```

## Best Practices

1. **Generate with Claude first** - Then customize
2. **Single responsibility** - One clear purpose per subagent
3. **Detailed prompts** - Specific instructions and examples
4. **Limit tool access** - Only necessary tools
5. **Version control** - Commit project subagents to git
6. **Test thoroughly** - Try various scenarios
7. **Clear descriptions** - Include "when to use"

## Advanced Usage

### Chaining Subagents

```bash
> First use code-analyzer to find issues, then optimizer to fix them
```

### Dynamic Selection

Claude chooses subagents based on:
- Task keywords matching description
- Tool requirements
- Context clues

Make `description` specific and action-oriented.

## Performance Considerations

- **Context efficiency**: Subagents preserve main context
- **Latency**: Starting with clean slate adds initial latency
- **Parallelization**: Can run multiple subagents concurrently

## Tool Access Patterns

### Read-Only (analysis, review)
```yaml
tools: Read, Grep, Glob
```

### Test Execution
```yaml
tools: Bash, Read, Grep
```

### Code Modification
```yaml
tools: Read, Edit, Write, Grep, Glob
```

### Full Access (debugging)
```yaml
tools: Read, Edit, Write, Bash, Grep, Glob
```

## Common Patterns

### Security-Focused

```yaml
tools: Read, Grep, Glob  # No write access
model: opus              # Most capable for security
```

### Performance Testing

```yaml
tools: Bash, Read, Write  # Can run benchmarks
model: sonnet             # Balanced
```

### Documentation

```yaml
tools: Read, Write, Grep, Glob
model: sonnet
```

## Troubleshooting

**Subagent not triggering?**
- Check `description` is specific enough
- Include task-related keywords
- Add "Use when..." guidance

**Tool errors?**
- Verify tool names are correct
- Check tool is available in main agent
- Review tool permissions

**Context issues?**
- Subagents start fresh each invocation
- They don't see main conversation history
- Provide context in the delegation

