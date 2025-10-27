# Agent Skills (NEW!)

## 🚨 CRITICAL: This is the NEW feature (Released Oct 16, 2025)

Skills are **model-invoked** capabilities that Claude uses automatically when relevant. This is fundamentally different from slash commands (user-invoked).

## Skills vs Commands vs Subagents

| Feature | Skills | Slash Commands | Subagents |
|---------|--------|----------------|-----------|
| **Invocation** | Model (automatic) | User (explicit `/cmd`) | Model (delegated) |
| **Discovery** | Description-based | Name-based | Description-based |
| **Structure** | SKILL.md + resources | Single .md file | Single .md file |
| **Progressive Loading** | Yes (3 levels) | No (full load) | No |
| **Context Window** | On-demand | Immediate | Separate |
| **Bundled Files** | Unlimited | Single file | Single file |
| **Scripts** | Yes (executable) | No | No |
| **Use Case** | Complex workflows | Quick prompts | Task delegation |

## Progressive Disclosure (3 Levels)

### Level 1: Metadata (Always Loaded)

```yaml
---
name: pdf-processing
description: Extract text/tables from PDFs, fill forms. Use when working with PDFs or document extraction.
---
```

- Loaded at startup (~100 tokens per skill)
- Added to system prompt
- Claude sees: Skill exists and when to use it
- **No context penalty for installed but unused skills**

### Level 2: Instructions (Loaded When Triggered)

```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For API reference, see [REFERENCE.md](REFERENCE.md).
```

- Loaded when skill matches task
- Claude reads SKILL.md via bash
- ~5k tokens budget for SKILL.md
- References to additional files

### Level 3: Resources (Loaded As Needed)

```
pdf-skill/
├── SKILL.md              # Main instructions
├── FORMS.md              # Form-filling guide (loaded if referenced)
├── REFERENCE.md          # API reference (loaded if referenced)
└── scripts/
    ├── analyze_form.py   # Executed, not loaded into context
    └── validate.py       # Executed, not loaded into context
```

- Additional markdown files: Loaded when referenced
- Scripts: **Executed via bash, never loaded into context!**
- Effectively unlimited bundled content

## File Structure

```
skill-name/
├── SKILL.md              # Required: Main file
├── reference.md          # Optional: Additional docs
├── examples.md           # Optional: Examples
└── scripts/              # Optional: Executable scripts
    └── helper.py
```

## SKILL.md Format

```markdown
---
name: skill-name
description: What this does and when to use it. MUST include trigger keywords!
allowed-tools: Read, Grep, Glob  # Optional: restrict tools (Claude Code only)
---

# Skill Name

## Quick Start
Basic usage instructions...

## Advanced
For advanced usage, see [reference.md](reference.md)

## Examples
See [examples.md](examples.md) for patterns
```

### Field Requirements

**`name`**:
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags
- No reserved words: "anthropic", "claude"

**`description`**:
- Max 1024 characters  
- MUST be specific - include both:
  - What the skill does
  - When to use it (trigger keywords)
- No XML tags

**`allowed-tools`** (Claude Code only):
- Comma-separated tool list
- When skill is active, Claude uses ONLY these tools
- If omitted, inherits all tools

## File Locations

```
Project skills:
.claude/skills/skill-name/
└── SKILL.md

User skills:
~/.claude/skills/skill-name/
└── SKILL.md

Plugin skills:
<plugin>/skills/skill-name/
└── SKILL.md
```

## How Claude Uses Skills

1. **Startup**: Load all skill metadata (name + description)
2. **User request**: "Extract text from this PDF"
3. **Skill matching**: Claude sees `pdf-processing` description matches
4. **Load skill**: `bash: cat .claude/skills/pdf-processing/SKILL.md`
5. **Optional**: Read additional files if referenced
6. **Execute**: Run scripts via bash (output only, not code)

## Example: Simple Skill (Single File)

```markdown
---
name: commit-message-generator
description: Generate clear commit messages from git diffs. Use when writing commits or reviewing staged changes.
---

# Commit Message Generator

## Instructions

1. Run `git diff --staged` to see changes
2. Suggest commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best Practices
- Use present tense
- Explain what and why, not how
```

Usage:
```bash
> Help me write a commit message
# Claude automatically uses this skill
```

## Example: Multi-File Skill with Scripts

```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

**SKILL.md**:
```markdown
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
---

# PDF Processing

## Quick Start
Extract text:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements
Packages must be installed:
```bash
pip install pypdf pdfplumber
```
```

**FORMS.md**:
```markdown
# PDF Form Filling

## Workflow
1. Run: `python scripts/analyze_form.py input.pdf`
2. Edit generated `fields.json`
3. Validate: `python scripts/validate.py fields.json`
4. Fill: `python scripts/fill_form.py input.pdf fields.json output.pdf`
```

Claude loads FORMS.md only when form filling is needed.

## Skill with Tool Restrictions

```markdown
---
name: code-reviewer
description: Review code for best practices. Use when reviewing code or checking PRs.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review Checklist
1. Code organization
2. Error handling
3. Performance
4. Security
5. Test coverage

## Instructions
1. Read target files (Read tool)
2. Search patterns (Grep)
3. Find related files (Glob)
4. Provide detailed feedback
```

When this skill is active, Claude can ONLY use Read, Grep, and Glob.

## Creating Skills

### Option 1: Manual Creation

```bash
# Project skill
mkdir -p .claude/skills/my-skill
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What it does and when to use it
---

# My Skill

Instructions here...
EOF
```

### Option 2: Via API (for Custom Skills)

See API documentation for programmatic creation.

### Option 3: Via Plugins

Bundle skills in plugin's `skills/` directory.

## Testing Skills

After creating, test by asking relevant questions:

```bash
# If skill description mentions "PDF files"
> Can you help me extract text from this PDF?

# Claude should automatically use the skill
# Check /context to see if skill was loaded
```

## Debugging Skills

**Skill not triggering?**

1. **Check description specificity**
   ```yaml
   # Too vague
   description: Helps with documents
   
   # Specific (good)
   description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
   ```

2. **Verify file location**
   ```bash
   ls .claude/skills/skill-name/SKILL.md
   ls ~/.claude/skills/skill-name/SKILL.md
   ```

3. **Check YAML syntax**
   ```bash
   head -n 10 .claude/skills/skill-name/SKILL.md
   ```

4. **Enable debug mode**
   ```bash
   claude --debug
   # Watch for skill loading messages
   ```

## Best Practices

### Writing Descriptions

**Include both what AND when**:

✅ Good:
```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format.
```

❌ Too vague:
```yaml
description: For files
```

### Structuring Skills

**Keep SKILL.md < 500 lines**:
- Core instructions in SKILL.md
- Split detailed content into separate files
- Use references: `[details](DETAILS.md)`

**Organize by domain**:
```
bigquery-skill/
├── SKILL.md (overview)
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

SKILL.md:
```markdown
**Finance**: Revenue, ARR → [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline → [reference/sales.md](reference/sales.md)
```

### Using Scripts

**Scripts are for**:
- Deterministic operations
- Complex algorithms
- Performance-critical tasks

**Example**:
```markdown
## Form Analysis

Run the analyzer:
```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200}
}
```
```

### Avoiding Deeply Nested References

✅ One level deep:
```
SKILL.md → advanced.md
SKILL.md → reference.md
SKILL.md → examples.md
```

❌ Too deep:
```
SKILL.md → advanced.md → details.md → specifics.md
```

## Common Patterns

### Template Pattern

```markdown
## Report Structure

ALWAYS use this template:

```markdown
# [Analysis Title]

## Executive Summary
[One paragraph overview]

## Key Findings
- Finding 1
- Finding 2

## Recommendations
1. Action 1
2. Action 2
```
```

### Examples Pattern

```markdown
## Commit Message Format

**Example 1:**
Input: Added user authentication
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation
```

**Example 2:**
Input: Fixed date bug
Output:
```
fix(reports): correct date formatting

Use UTC timestamps consistently
```
```

### Conditional Workflow Pattern

```markdown
## Workflow

1. Determine task type:
   - **Creating?** → Follow creation workflow
   - **Editing?** → Follow editing workflow

2. Creation workflow:
   - Use library X
   - Build from scratch

3. Editing workflow:
   - Modify existing
   - Validate changes
```

## Security Considerations

🚨 **ONLY use skills from trusted sources!**

Skills can:
- Execute code in your environment
- Access files Claude can access
- Make network requests (in some contexts)
- Direct Claude to take actions

**Before installing untrusted skills**:
1. Read all bundled files
2. Check scripts for malicious code
3. Review external dependencies
4. Verify network calls
5. Test in isolated environment first

## Where Skills Work

| Platform | Pre-built Skills | Custom Skills |
|----------|------------------|---------------|
| **Claude API** | Yes (pptx, xlsx, docx, pdf) | Yes (upload via API) |
| **Claude Code** | No | Yes (filesystem) |
| **Agent SDK** | No | Yes (filesystem) |
| **Claude.ai** | Yes | Yes (upload via UI) |

## Limitations

1. **No cross-platform sync**: Skills uploaded to one platform don't sync to others
2. **Sharing scope**:
   - Claude.ai: Per-user only
   - API: Workspace-wide
   - Claude Code: Project or user level
3. **Runtime constraints**:
   - No network access in code execution
   - No runtime package installation
   - Pre-installed packages only

## Token Budgets

- **Metadata (Level 1)**: ~100 tokens per skill
- **SKILL.md (Level 2)**: Keep under 5k tokens
- **Additional files (Level 3)**: No practical limit (loaded on-demand)

## Skill Invocation Flow

```
User: "Extract text from this PDF"
  ↓
Claude: Check skill metadata
  ↓
Match found: pdf-processing
  ↓
bash: cat .claude/skills/pdf-processing/SKILL.md
  ↓
(Instructions loaded into context)
  ↓
Claude: Need form details?
  ↓
bash: cat .claude/skills/pdf-processing/FORMS.md
  ↓
(Optional details loaded)
  ↓
Execute task with loaded knowledge
```

Only relevant content enters context window!

