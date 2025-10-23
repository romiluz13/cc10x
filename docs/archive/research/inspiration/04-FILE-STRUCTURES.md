# File Structure Specifications

## Complete File Format Reference

Detailed specifications for all Claude Code plugin file types and structures.

---

## plugin.json

**Location:** `.claude-plugin/plugin.json`
**Required:** Yes (for plugins)
**Format:** JSON

### Complete Schema

```json
{
  "name": "string (required)",
  "version": "string (required, semver)",
  "description": "string (required)",
  "author": {
    "name": "string (required)",
    "email": "string (optional)",
    "url": "string (optional)"
  },
  "repository": {
    "type": "string (optional, usually 'git')",
    "url": "string (optional)"
  },
  "homepage": "string (optional)",
  "bugs": {
    "url": "string (optional)"
  },
  "license": "string (optional, but recommended)",
  "keywords": ["array", "of", "strings"],
  "category": "string (optional)",
  "tags": ["array", "of", "strings"],
  "commands": "string (optional, path like './commands/')",
  "agents": "string (optional, path like './agents/')",
  "skills": "string (optional, path like './skills/')",
  "hooks": "string (optional, path like './hooks/')",
  "mcp": {
    "server": "string (path to MCP server entry)",
    "tools": ["array", "of", "tool", "names"]
  }
}
```

### Minimal Example

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What my plugin does",
  "author": {
    "name": "Your Name"
  }
}
```

### Complete Example

```json
{
  "name": "cc10x",
  "version": "1.0.0",
  "description": "Intelligent orchestration system combining commands, sub-agents, and skills for 10x developer productivity",
  "author": {
    "name": "Rom Iluz",
    "email": "rom.iluz13@gmail.com",
    "url": "https://github.com/romiluz13"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/romiluz13/cc10x.git"
  },
  "homepage": "https://github.com/romiluz13/cc10x",
  "bugs": {
    "url": "https://github.com/romiluz13/cc10x/issues"
  },
  "license": "MIT",
  "keywords": [
    "orchestration",
    "productivity",
    "sub-agents",
    "skills",
    "workflow",
    "tdd",
    "code-review"
  ],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/"
}
```

### Field Descriptions

**name** (required)
- Plugin identifier
- Used in installation: `/plugin install name@marketplace`
- Lowercase, hyphenated (kebab-case)
- No spaces

**version** (required)
- Semantic versioning (semver)
- Format: MAJOR.MINOR.PATCH
- Example: 1.0.0, 2.1.3

**description** (required)
- One-line summary
- Clear value proposition
- 100-200 characters ideal
- Shows in plugin listings

**author** (required)
- name: Required
- email: Optional but recommended
- url: Optional, GitHub profile

**keywords** (recommended)
- Array of strings
- Helps discovery
- Common categories: productivity, code-review, debugging, etc.

**commands/agents/skills/hooks** (optional)
- Paths to component directories
- Relative to plugin.json location
- Usually `"./commands/"`, `"./agents/"`, etc.
- Claude will scan these directories

---

## marketplace.json

**Location:** `.claude-plugin/marketplace.json`
**Required:** Yes (for marketplaces)
**Format:** JSON

### Complete Schema

```json
{
  "name": "string (required)",
  "owner": {
    "name": "string (required)",
    "email": "string (optional)",
    "url": "string (optional)"
  },
  "metadata": {
    "description": "string (required)",
    "version": "string (required)",
    "homepage": "string (optional)"
  },
  "plugins": [
    {
      "name": "string (required)",
      "source": "string (required, path like './plugins/plugin-name')",
      "description": "string (required)",
      "version": "string (required)",
      "author": {
        "name": "string (required)",
        "url": "string (optional)"
      },
      "homepage": "string (optional)",
      "repository": "string (optional)",
      "license": "string (optional)",
      "keywords": ["array"],
      "category": "string (optional)",
      "tags": ["array"]
    }
  ]
}
```

### Example

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/yourusername"
  },
  "metadata": {
    "description": "Collection of useful plugins",
    "version": "1.0.0",
    "homepage": "https://your-marketplace-site.com"
  },
  "plugins": [
    {
      "name": "plugin-one",
      "source": "./plugins/plugin-one",
      "description": "First plugin in marketplace",
      "version": "1.0.0",
      "author": {
        "name": "Plugin Author",
        "url": "https://github.com/author"
      },
      "homepage": "https://github.com/owner/marketplace/tree/main/plugins/plugin-one",
      "keywords": ["utility", "productivity"],
      "category": "productivity"
    }
  ]
}
```

### Key Points

**source field:**
- MUST point to subdirectory
- Format: `"./plugins/plugin-name"`
- NOT `"./"` (common mistake)

**Each plugin:**
- Must have its own subdirectory
- Must have .claude-plugin/plugin.json inside
- Marketplace.json is just the catalog

---

## Command Files

**Location:** `commands/*.md`
**Format:** Markdown with YAML frontmatter
**Extension:** `.md`

### Template

```markdown
---
name: command-name
description: Brief description of what this command does
aliases: [alt-name, another-name]  # Optional
---

# Command Name

Detailed explanation of the command's purpose and functionality.

## What It Does

Clear description of:
- Primary function
- Key features
- Expected outcomes

## Usage

```bash
/command-name [arguments]
```

Examples:
```bash
/command-name simple-example
/command-name "example with spaces"
/command-name --flag value
```

## Parameters

**param1** (required)
- Description
- Type: string
- Example: "value"

**param2** (optional)
- Description
- Type: boolean
- Default: false

## Workflow

1. **Step 1:** What happens first
   - Detail A
   - Detail B

2. **Step 2:** Next action
   - Detail C
   - Detail D

3. **Step 3:** Final step
   - Detail E
   - Detail F

## Output

What the user can expect:
- Created files
- Modified files
- Generated reports
- Status messages

## Examples

### Example 1: Basic Usage

```bash
/command-name basic
```

Result: Description of what happens

### Example 2: Advanced Usage

```bash
/command-name advanced --with-options
```

Result: Description of outcome

## Notes

Additional information:
- Best practices
- Tips and tricks
- Common gotchas
- Related commands

## See Also

- /related-command-1
- /related-command-2
```

### YAML Frontmatter

**Required fields:**
- `name`: Command identifier (used as `/name`)
- `description`: One-line summary

**Optional fields:**
- `aliases`: Alternative command names
- `hidden`: true/false (hide from listings)
- `category`: Grouping category

---

## Agent Files

**Location:** `agents/*.md`
**Format:** Markdown with YAML frontmatter
**Extension:** `.md`

### Template

```markdown
---
name: agent-name
description: Agent's role and expertise
tools: ["tool1", "tool2", "tool3"]  # Optional
auto_invoke: true  # Optional, default false
---

# Agent Name

Specialized AI assistant for [domain/task].

## Role

This agent is responsible for:
- Primary responsibility
- Secondary responsibility
- Areas of expertise

## When to Use This Agent

Invoke this agent when:
- Situation 1 requiring this expertise
- Situation 2 where this agent helps
- Context X where this agent is optimal

**Examples of triggering contexts:**
- User mentions "keyword related to domain"
- Task involves [specific technology]
- Code review for [specific aspect]

## Expertise

### Domain Knowledge
- Technology stack expertise
- Best practices for X
- Common patterns in Y
- Anti-patterns to avoid

### Capabilities
- What this agent can do
- Tools available to agent
- Analysis capabilities
- Code generation abilities

## System Prompt

Detailed instructions for how this agent should behave:

You are a [role] specializing in [domain]. Your responsibilities include:

1. **Analysis:** [How to analyze]
2. **Recommendations:** [How to recommend]
3. **Implementation:** [How to implement]
4. **Validation:** [How to validate]

### Guidelines

- Follow [specific methodology]
- Prioritize [specific values]
- Always [specific requirement]
- Never [specific prohibition]

### Examples

**Example 1: [Scenario]**
User request: "[Example user request]"

Agent response approach:
1. [First step]
2. [Second step]
3. [Third step]

**Example 2: [Another scenario]**
[Similar structure]

## Tool Usage

If tools specified in frontmatter:

### tool1
When to use: [Description]
How to use: [Instructions]

### tool2
When to use: [Description]
How to use: [Instructions]

## Quality Standards

This agent maintains these standards:
- Standard 1
- Standard 2
- Standard 3

## Output Format

When this agent completes its task:
- Specific format for results
- What to include
- What to exclude
- How to present findings

## Coordination

How this agent works with others:
- Hands off to [other agent] when [condition]
- Receives input from [other agent]
- Collaborates with [other agent] on [task]
```

### YAML Frontmatter

**Required fields:**
- `name`: Agent identifier
- `description`: Agent's role

**Optional fields:**
- `tools`: Array of tool names agent can use
- `auto_invoke`: Whether Claude should auto-invoke
- `priority`: Invocation priority (1-10)

---

## Skill Files

**Location:** `skills/skill-name/SKILL.md`
**Format:** Markdown with YAML frontmatter
**Extension:** `SKILL.md` (capitalized)
**Directory:** Each skill in its own subdirectory

### Template

```markdown
---
name: "Skill Name"
description: |
  Concise description of what this skill does.
  Include trigger phrases and when to use.
  Examples: "use when X", "activate on Y"
---

## What This Skill Does

Comprehensive explanation of the skill's capabilities and purpose.

Key capabilities:
- Capability 1
- Capability 2
- Capability 3

## When It Activates

This skill automatically activates when:
- User mentions "[trigger phrase]"
- Task involves [specific context]
- Claude detects [pattern or need]

**Trigger phrases:**
- "phrase one"
- "phrase two"
- "related keyword"

## How It Works

### Step-by-Step Process

1. **Phase 1: [Phase Name]**
   - Action A
   - Action B
   - Decision point X

2. **Phase 2: [Phase Name]**
   - Action C
   - Action D
   - Validation Y

3. **Phase 3: [Phase Name]**
   - Action E
   - Action F
   - Completion Z

### Decision Logic

```
If condition A:
  → Action 1
Else if condition B:
  → Action 2
Else:
  → Action 3
```

## Examples

### Example 1: [Use Case]

**User says:** "[Example user input]"

**Skill activates automatically**

**Process:**
1. Skill recognizes "[trigger]"
2. Loads full instructions
3. Executes workflow:
   - Step A
   - Step B
   - Step C
4. Produces output

**Result:** [Description of outcome]

### Example 2: [Another Use Case]

[Similar structure]

## Best Practices

Built-in best practices:
- Practice 1
- Practice 2
- Practice 3

## Error Handling

How this skill handles errors:
- Error type 1 → Response A
- Error type 2 → Response B
- Unknown errors → Response C

## Code Examples

If applicable, include code examples:

```python
# Example code this skill might generate
def example_function():
    # Best practice pattern
    pass
```

```javascript
// Another example
const example = () => {
  // Pattern this skill follows
};
```

## Related Skills

This skill works well with:
- Related Skill 1 - [When to use together]
- Related Skill 2 - [How they complement]

## Progressive Disclosure

### Basic Usage
Simple explanation for beginners

### Advanced Usage
Complex scenarios and edge cases

### Expert Usage
Optimization and customization

## Quality Criteria

Output from this skill meets these standards:
- Criterion 1
- Criterion 2
- Criterion 3

## Notes

Additional information:
- Special considerations
- Edge cases
- Limitations
- Future enhancements
```

### YAML Frontmatter

**Required fields:**
- `name`: Skill name (quoted string)
- `description`: Multi-line description with trigger phrases

**Recommended in description:**
- What the skill does
- When to use it
- Trigger phrases
- Key benefits

### Skill Size Recommendations

**Anthropic examples:** ~500 bytes (minimal)
**Production skills:** 3,000-5,000 bytes (comprehensive)
**Best practice:** Include workflows, examples, error handling

---

## Hooks Configuration

**Location:** `hooks/hooks.json` + script files
**Format:** JSON config + executable scripts

### hooks.json

```json
{
  "hooks": {
    "session-start": {
      "description": "Run when Claude Code session starts",
      "script": "./session-start.sh",
      "timeout": 5000,
      "async": false
    },
    "pre-compact": {
      "description": "Run before context compaction",
      "script": "./pre-compact.sh",
      "timeout": 3000,
      "async": false
    },
    "post-edit": {
      "description": "Run after file edits",
      "script": "./post-edit.sh",
      "timeout": 2000,
      "async": true
    }
  }
}
```

### Hook Script Template (session-start.sh)

```bash
#!/bin/bash
# Session Start Hook
# Runs when Claude Code session begins

set -euo pipefail

# Define paths
PROJECT_ROOT="$(pwd)"
MEMORY_DIR=".claude/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"

# Create directories if needed
mkdir -p "$MEMORY_DIR"
mkdir -p "$SNAPSHOT_DIR"

# Load previous state if exists
if [ -f "$MEMORY_DIR/WORKING_PLAN.md" ]; then
    echo "Loaded working plan from previous session"
fi

# Initialize session tracking
SESSION_ID="$(date +%Y%m%d_%H%M%S)"
echo "$SESSION_ID" > "$MEMORY_DIR/current_session.txt"

# Output for Claude
echo "Session initialized: $SESSION_ID"
echo "Working plan loaded"
echo "Ready for orchestration"

exit 0
```

### Hook Best Practices

**Performance:**
- Keep hooks fast (<5 seconds)
- Use async when possible
- Avoid blocking operations

**Reliability:**
- Handle errors gracefully
- Always exit with status code
- Log important actions

**Safety:**
- Don't modify critical files
- Check for existence before reading
- Use error handling (set -e)

---

## Directory Structure Standards

### Single Plugin

```
plugin-name/
  .claude-plugin/
    plugin.json              ← Plugin metadata
  commands/
    command-1.md
    command-2.md
  agents/
    agent-1.md
    agent-2.md
  skills/
    skill-1/
      SKILL.md
    skill-2/
      SKILL.md
  hooks/
    hooks.json
    session-start.sh
    pre-compact.sh
  README.md                  ← User documentation
  CLAUDE.md                  ← Claude instructions (optional)
  LICENSE
  CHANGELOG.md               ← Version history
```

### Marketplace

```
marketplace-name/
  .claude-plugin/
    marketplace.json         ← Marketplace catalog
  plugins/
    plugin-a/
      .claude-plugin/
        plugin.json
      commands/
      agents/
      README.md
    plugin-b/
      .claude-plugin/
        plugin.json
      commands/
      skills/
      README.md
  README.md                  ← Marketplace overview
  CONTRIBUTING.md            ← Contribution guidelines
```

---

## Naming Conventions

**Plugins:**
- kebab-case: `my-plugin-name`
- Lowercase only
- Hyphens separate words
- No special characters

**Commands:**
- kebab-case: `command-name.md`
- Descriptive verb-noun pairs
- Examples: `feature-plan.md`, `bug-fix.md`

**Agents:**
- kebab-case: `agent-role.md`
- Role-based names
- Examples: `security-reviewer.md`, `implementer.md`

**Skills:**
- kebab-case directory: `skill-name/`
- SKILL.md file (capitalized)
- Examples: `test-driven-development/SKILL.md`

---

## Common Mistakes

❌ **Wrong file extension:**
- Commands should be `.md`, not `.txt` or `.markdown`
- Skills must be `SKILL.md` (capitalized)

❌ **Missing YAML frontmatter:**
- All components need `---` delimited frontmatter
- Must be at start of file

❌ **Incorrect paths:**
- In plugin.json: Use `"./commands/"` not `"commands"`
- In marketplace.json: Use `"./plugins/name"` not `"./"

❌ **Wrong directory structure:**
- Skills need subdirectory: `skills/name/SKILL.md`
- Not: `skills/name.md`

---

## Validation Checklist

✅ **plugin.json:**
- Valid JSON
- Required fields present
- Paths are correct
- Version is semver

✅ **Commands:**
- .md extension
- YAML frontmatter
- Clear description
- Usage examples

✅ **Agents:**
- .md extension
- YAML frontmatter
- Role defined
- Examples provided

✅ **Skills:**
- Subdirectory structure
- SKILL.md filename
- YAML frontmatter
- Trigger phrases

✅ **Hooks:**
- hooks.json valid JSON
- Scripts are executable
- Error handling present
- Fast execution

