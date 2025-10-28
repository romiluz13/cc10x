# Best Practices & Guidelines

## Skill Development (CRITICAL - NEW FEATURE)

### Writing Effective Skills

#### 1. Concise is Key

The context window is shared. Only add what Claude doesn't already know.

✅ **Good** (50 tokens):
```markdown
## Extract PDF text

Use pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

❌ **Bad** (150 tokens):
```markdown
## Extract PDF text

PDF (Portable Document Format) files are common files containing text and images.
To extract text, you'll need a library. There are many libraries available,
but we recommend pdfplumber because it's easy to use and handles most cases...
```

Claude already knows what PDFs are!

#### 2. Write Specific Descriptions

**Description must include**:
- What the skill does
- When to use it
- Trigger keywords users would mention

✅ **Good**:
```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format.
```

❌ **Too vague**:
```yaml
description: Helps with documents
```

#### 3. Use Progressive Disclosure

**Keep SKILL.md < 500 lines**:

```
skill/
├── SKILL.md (overview, < 500 lines)
├── reference.md (details)
├── examples.md (examples)
└── scripts/ (utilities)
```

**SKILL.md**:
```markdown
# Quick operations here

For advanced features, see [reference.md](reference.md).
For examples, see [examples.md](examples.md).
```

**Only references one level deep!**

✅ Good:
```
SKILL.md → reference.md ✓
SKILL.md → examples.md ✓
```

❌ Too deep:
```
SKILL.md → advanced.md → details.md → specifics.md ✗
```

#### 4. Set Appropriate Freedom Levels

**High freedom** (text instructions):
```markdown
## Code Review
1. Analyze structure
2. Check for bugs
3. Suggest improvements
```

**Medium freedom** (parameterized scripts):
```markdown
## Generate Report
```python
def generate_report(data, format="markdown", include_charts=True):
    # Customize as needed
```
```

**Low freedom** (specific scripts):
```markdown
## Database Migration

Run EXACTLY this:
```bash
python scripts/migrate.py --verify --backup
```

Do NOT modify flags.
```

#### 5. Provide Workflows with Checklists

```markdown
## PDF Form Filling Workflow

Copy this checklist:

```
Task Progress:
- [ ] Step 1: Analyze form (run analyze_form.py)
- [ ] Step 2: Create mapping (edit fields.json)
- [ ] Step 3: Validate (run validate_fields.py)
- [ ] Step 4: Fill form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

[Detailed steps follow...]
```

#### 6. Implement Feedback Loops

```markdown
## Workflow
1. Make changes
2. **Validate**: `python scripts/validate.py`
3. If validation fails:
   - Review errors
   - Fix issues
   - **Run validation again**
4. Only proceed when validation passes
```

#### 7. Use Scripts for Deterministic Operations

Scripts should:
- Handle errors explicitly
- Not punt to Claude
- Document configuration values

✅ **Good**:
```python
def process_file(path):
    """Process file, creating if missing."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
```

❌ **Bad**:
```python
def process_file(path):
    return open(path).read()  # Punts errors to Claude
```

### Skill Testing Strategy

**Build evaluations FIRST**:

1. Run Claude without skill on representative tasks
2. Document specific failures
3. Create 3+ test scenarios
4. Establish baseline performance
5. Write minimal skill to address gaps
6. Iterate based on evaluations

### Skill Iteration with Claude

**Two-instance pattern**:

1. **Claude A** (expert): Helps design/refine skill
2. **Claude B** (user): Uses skill for real work
3. **You**: Observe Claude B, report to Claude A

Workflow:
1. Complete task with Claude A (normal prompting)
2. Identify reusable patterns
3. Ask Claude A to create skill
4. Test with Claude B on similar tasks
5. Observe Claude B's behavior
6. Return to Claude A with feedback
7. Iterate

### Skill Security

🚨 **ONLY use skills from trusted sources!**

**Before installing**:
1. Read all bundled files (SKILL.md, scripts, etc.)
2. Check scripts for malicious code
3. Review external dependencies
4. Verify network calls
5. Test in isolated environment

**Red flags**:
- Unexpected network calls
- External URL fetching
- Suspicious file access patterns
- Operations not matching description

## Subagent Best Practices

### 1. Generate with Claude First

```bash
/agents
# > Create New Agent
# > Generate with Claude
# Describe purpose, Claude generates it
# Then customize to your needs
```

### 2. Single Responsibility

✅ One focus:
- "Security code reviewer"
- "Test execution specialist"
- "Documentation generator"

❌ Too broad:
- "General helper"
- "Development assistant"

### 3. Detailed Prompts

Include:
- Specific instructions
- Examples
- Constraints
- Expected output format

### 4. Limit Tool Access

Only grant necessary tools:

```yaml
# Read-only reviewer
tools: Read, Grep, Glob

# Test runner
tools: Bash, Read, Grep

# Code modifier
tools: Read, Edit, Write, Grep, Glob
```

### 5. Action-Oriented Descriptions

Include "when to use" guidance:

```yaml
description: Expert code reviewer. Use PROACTIVELY after code changes.
```

Keywords that help:
- "Use PROACTIVELY"
- "MUST BE USED when..."
- "Use immediately after..."

## Plugin Development

### 1. Clear Single Purpose

Each plugin should have one clear responsibility:

✅ Good:
- "Deployment automation tools"
- "Security scanning suite"
- "Testing framework"

❌ Too broad:
- "Development helpers"
- "Utility tools"

### 2. Standard Structure

Always use standard directories:

```
plugin/
├── .claude-plugin/plugin.json
├── commands/
├── agents/
├── skills/
├── hooks/
└── .mcp.json
```

NOT inside `.claude-plugin/`!

### 3. Use Environment Variables

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
}
```

Never use absolute paths!

### 4. Documentation

Include:
- README.md with installation/usage
- Examples for each component
- Troubleshooting section
- Changelog

### 5. Semantic Versioning

```
MAJOR.MINOR.PATCH
2.1.3

MAJOR: Breaking changes (2.0.0)
MINOR: New features (1.1.0)
PATCH: Bug fixes (1.0.1)
```

### 6. Test Locally First

```bash
# Create test marketplace
mkdir test-marketplace
# Add plugin
# Test installation
/plugin marketplace add ./test-marketplace
/plugin install my-plugin@test-marketplace
```

## Marketplace Organization

### Categorize Plugins

```json
{
  "plugins": [
    {
      "name": "deployer",
      "category": "deployment",
      "keywords": ["ci-cd", "production"]
    },
    {
      "name": "security-scan",
      "category": "security",
      "keywords": ["vulnerability", "scanning"]
    },
    {
      "name": "test-gen",
      "category": "testing",
      "keywords": ["unit-tests", "coverage"]
    }
  ]
}
```

### Version Pinning

For stability, pin versions:

```json
{
  "plugins": [
    {
      "name": "critical-tool",
      "version": "2.1.0",  // Specific version
      "source": "..."
    }
  ]
}
```

## Hook Best Practices

### 1. Validate Inputs

```python
import json
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
if not tool_name:
    sys.exit(1)
```

### 2. Quote Shell Variables

✅ Good:
```bash
file_path="$1"
echo "Processing: $file_path"
```

❌ Bad:
```bash
file_path=$1
echo Processing: $file_path
```

### 3. Block Path Traversal

```python
file_path = tool_input.get("file_path", "")
if ".." in file_path:
    print("Path traversal blocked", file=sys.stderr)
    sys.exit(2)
```

### 4. Skip Sensitive Files

```python
SENSITIVE = [".env", ".git/", "id_rsa", ".aws/"]

if any(s in file_path for s in SENSITIVE):
    print("Sensitive file blocked", file=sys.stderr)
    sys.exit(2)
```

### 5. Use Project Directory

```json
{
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"
}
```

Not absolute paths!

## Slash Command Best Practices

### 1. Clear Descriptions

```yaml
description: Review code for security vulnerabilities and performance issues
```

Not: "Helper command"

### 2. Argument Hints

```yaml
argument-hint: [filename] [priority]
```

Helps users know what to pass.

### 3. Use File References

```markdown
Review @$1 for issues
Compare @src/old.js with @src/new.js
```

### 4. Bash for Dynamic Context

```markdown
## Context
- Git status: !`git status`
- Current branch: !`git branch --show-current`

## Task
Create commit based on above changes.
```

## SDK Best Practices

### 1. Load Project Settings

```typescript
{
  settingSources: ['project']  // Loads CLAUDE.md, skills, etc.
}
```

### 2. Use Appropriate Models

```typescript
agents: {
  'quick-task': { model: 'haiku' },     // Fast, cheap
  'normal-task': { model: 'sonnet' },   // Balanced
  'complex-task': { model: 'opus' }     // Most capable
}
```

### 3. Restrict Tools Appropriately

```typescript
// Read-only analysis
allowedTools: ['Read', 'Grep', 'Glob']

// Code modification
allowedTools: ['Read', 'Edit', 'Write', 'Bash']

// Full access
allowedTools: '*'  // or omit
```

### 4. Handle Errors

```typescript
try {
  for await (const message of result) {
    if (message.type === 'error') {
      console.error('Agent error:', message.error);
      // Handle gracefully
    }
  }
} catch (error) {
  console.error('Fatal error:', error);
  // Cleanup, retry, alert
}
```

### 5. Track Costs

```typescript
{
  trackCosts: true
}

// Monitor usage
if (message.type === 'usage') {
  console.log(`Tokens: ${message.tokens}, Cost: $${message.cost}`);
}
```

## Team Collaboration

### 1. Repository-Level Config

Commit to git:
```
.claude/
├── settings.json     # Marketplaces, plugins
├── commands/         # Team commands
├── agents/           # Team agents
└── skills/           # Team skills
```

### 2. Local Overrides

Don't commit personal preferences:
```
.claude/settings.local.json  # Add to .gitignore
```

### 3. Plugin Distribution

1. Create company marketplace
2. Add to settings.json
3. Team auto-gets plugins on clone

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  },
  "enabledPlugins": [
    "deployment@company-tools",
    "security@company-tools"
  ]
}
```

## Performance Optimization

### 1. Skill Token Budgets

- Metadata: ~100 tokens (always loaded)
- SKILL.md: < 5k tokens (loaded when triggered)
- Additional files: Unlimited (on-demand)

Keep SKILL.md concise!

### 2. Subagent Context Management

Subagents start fresh:
- Preserves main context
- May add latency initially
- Worth it for complex tasks

### 3. Progressive Loading

Structure skills for lazy loading:

```markdown
# SKILL.md (always loaded when triggered)
Quick reference here...

For details: [REFERENCE.md](REFERENCE.md)  (loaded only if needed)
```

## Common Anti-Patterns

### ❌ Deeply Nested References

Don't do:
```
SKILL.md → advanced.md → details.md → specifics.md
```

Do:
```
SKILL.md → reference.md ✓
SKILL.md → examples.md ✓
```

### ❌ Windows-Style Paths

Don't: `scripts\helper.py`
Do: `scripts/helper.py`

### ❌ Too Many Options

Don't:
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image...
```

Do:
```markdown
Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pytesseract instead.
```

### ❌ Time-Sensitive Info

Don't:
```markdown
If before August 2025, use old API.
After August 2025, use new API.
```

Do:
```markdown
## Current Method
Use v2 API: `api.example.com/v2`

## Old Patterns
<details>
<summary>Legacy v1 (deprecated 2025-08)</summary>
...
</details>
```

### ❌ Vague Tool Restrictions

Don't:
```yaml
tools: Bash  # Too broad!
```

Do:
```yaml
allowed-tools: Bash(git*), Bash(npm test:*)  # Specific commands
```

## Naming Conventions

### Skills

Use gerund form (verb + -ing):

✅ Good:
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`

❌ Avoid:
- `helper`, `utils`, `tools` (vague)
- `documents`, `data` (generic)
- `anthropic-helper` (reserved words)

### Plugins

Use clear, descriptive names:

✅ Good:
- `deployment-automation`
- `security-scanner`
- `test-generator`

❌ Avoid:
- `dev-tools` (vague)
- `plugin1` (meaningless)

### Commands

Action-oriented:

✅ Good:
- `/deploy`
- `/review-pr`
- `/generate-tests`

❌ Avoid:
- `/helper`
- `/do-stuff`

### Subagents

Role-based:

✅ Good:
- `code-reviewer`
- `security-scanner`
- `test-runner`

❌ Avoid:
- `agent1`
- `helper`

## File Organization

### Project Structure

```
project/
├── .claude/
│   ├── settings.json         # Marketplaces, plugins, hooks
│   ├── commands/             # Project commands
│   ├── agents/               # Project subagents
│   ├── skills/               # Project skills
│   │   ├── skill-1/
│   │   │   └── SKILL.md
│   │   └── skill-2/
│   │       ├── SKILL.md
│   │       ├── reference.md
│   │       └── scripts/
│   └── hooks/
│       └── format.sh
├── .gitignore
└── src/
```

### What to Commit

✅ Commit:
- `.claude/settings.json`
- `.claude/commands/`
- `.claude/agents/`
- `.claude/skills/`
- `.claude/hooks/` (scripts)

❌ Don't commit:
- `.claude/settings.local.json` (personal)
- `.claude-plugin/` (generated)
- Session transcripts

### .gitignore

```gitignore
# Claude Code
.claude/settings.local.json
.claude/.cache/
.claude/transcripts/
```

## Marketplace Best Practices

### 1. Semantic Versioning

```json
{
  "version": "2.1.0",
  "plugins": [
    {
      "name": "critical-plugin",
      "version": "1.5.0"  // Pin critical plugins
    },
    {
      "name": "optional-plugin",
      "version": "latest"  // Latest for non-critical
    }
  ]
}
```

### 2. Clear Categorization

```json
{
  "plugins": [
    {"name": "deploy", "category": "deployment"},
    {"name": "scan", "category": "security"},
    {"name": "test", "category": "testing"},
    {"name": "docs", "category": "documentation"}
  ]
}
```

### 3. Comprehensive Metadata

```json
{
  "name": "plugin-name",
  "description": "Clear description of what plugin does",
  "version": "2.0.0",
  "author": {"name": "Team", "email": "team@example.com"},
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/repo",
  "license": "MIT",
  "keywords": ["relevant", "searchable", "tags"]
}
```

### 4. Testing Before Distribution

```bash
# Validate JSON
claude plugin validate .

# Test locally
/plugin marketplace add ./marketplace
/plugin install test-plugin@marketplace

# Verify all components work
/help  # Check commands
/agents  # Check subagents
# Test hooks trigger correctly
```

## Security Best Practices

### Skills Security

1. **Audit before installing**
2. **Check for network calls**
3. **Review bundled scripts**
4. **Verify no secret exposure**
5. **Test in sandbox first**

### Hook Security

1. **Validate all inputs**
2. **Quote shell variables**
3. **Block path traversal**
4. **Use absolute paths**
5. **Skip sensitive files**
6. **Test thoroughly**

### MCP Security

1. **Verify server source**
2. **Review permissions**
3. **Limit tool access**
4. **Monitor usage**
5. **Use authentication**

## Debugging Strategies

### Skill Not Triggering?

1. Check description specificity
2. Verify file location
3. Validate YAML syntax
4. Enable debug: `claude --debug`
5. Test with exact keywords from description

### Hook Not Firing?

1. Check matcher pattern
2. Verify script executable: `chmod +x`
3. Test command manually
4. Check JSON syntax
5. Run `claude --debug`

### Plugin Not Loading?

1. Validate plugin.json
2. Check directory structure
3. Verify component paths
4. Test with `claude --debug`
5. Check marketplace.json

## Performance Guidelines

### Context Window Management

**Total budget**: ~200k tokens (Claude Sonnet 4.5)

**Budget allocation**:
- System prompt: ~10k tokens
- Skill metadata: ~100 tokens × N skills
- Conversation history: Growing
- Active skill content: ~5k tokens per skill
- Tool outputs: Variable

**Optimization**:
- Keep SKILL.md < 500 lines
- Use progressive disclosure
- Split large content into files
- Let Claude load on-demand

### Subagent Usage

**When to use**:
- Complex specialized tasks
- Need separate context
- Parallel execution

**When NOT to use**:
- Simple tasks
- Context is relevant
- Quick operations

### Hook Performance

- Keep hooks fast (< 5 seconds)
- Use `timeout` for safety
- Avoid expensive operations
- Cache results when possible

## Testing Strategies

### Unit Test Skills

Create evaluation suite:

```json
{
  "skills": ["my-skill"],
  "query": "Test query",
  "expected_behavior": [
    "Should do X",
    "Should handle Y",
    "Should validate Z"
  ]
}
```

### Integration Test Plugins

1. Install in test project
2. Try each component:
   - Commands: `/command-name`
   - Agents: Check `/agents`
   - Skills: Trigger with relevant query
   - Hooks: Trigger events
3. Verify behavior
4. Test edge cases

### Test Subagents

1. Create test scenarios
2. Invoke explicitly: "Use X subagent to..."
3. Verify separate context
4. Check tool restrictions work
5. Test automatic delegation

## Documentation Standards

### README.md Template

```markdown
# Plugin Name

Brief description of what plugin does.

## Installation

```bash
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace
```

## Components

- **Commands**: `/deploy`, `/review`
- **Agents**: security-reviewer, performance-tester
- **Skills**: code-quality, deployment
- **Hooks**: Auto-format, auto-test

## Usage

[Examples of each component]

## Configuration

[Any required setup]

## Troubleshooting

[Common issues and solutions]

## License

MIT
```

### SKILL.md Template

```markdown
---
name: skill-name
description: What it does and when to use it. Include trigger keywords.
allowed-tools: Read, Grep  # Optional
---

# Skill Name

## Quick Start
Basic usage for common case...

## Advanced
For advanced features, see [REFERENCE.md](REFERENCE.md)

## Examples
See [EXAMPLES.md](EXAMPLES.md)

## Requirements
List any dependencies...
```

## Version Control

### What to Track

```bash
git add .claude/settings.json       # ✅ Config
git add .claude/commands/           # ✅ Commands
git add .claude/agents/             # ✅ Agents
git add .claude/skills/             # ✅ Skills
git add .claude/hooks/              # ✅ Hook scripts
```

### What to Ignore

```bash
# .gitignore
.claude/settings.local.json
.claude/.cache/
.claude/transcripts/
.claude-plugin/  # Generated
```

## Continuous Improvement

1. **Monitor usage**: Watch how team uses plugins/skills
2. **Gather feedback**: Ask what's missing or confusing
3. **Iterate quickly**: Update based on real usage
4. **Version properly**: Communicate changes
5. **Document changes**: Keep changelog updated
6. **Test with all models**: Haiku, Sonnet, Opus
7. **Share learnings**: Document patterns that work

