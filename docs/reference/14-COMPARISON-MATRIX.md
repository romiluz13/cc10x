# Comprehensive Comparison Matrix

## Skills vs Commands vs Subagents

### Feature Comparison

| Feature | Skills | Slash Commands | Subagents |
|---------|--------|----------------|-----------|
| **Invocation** | Model decides | User types `/cmd` | Model delegates |
| **Trigger** | Description match | Explicit call | Description match |
| **Discovery** | Automatic | Manual | Automatic |
| **Structure** | Directory + SKILL.md | Single .md file | Single .md file |
| **File Support** | Multiple files | Single file | Single file |
| **Scripts** | Yes (bundled, executable) | No | No |
| **Progressive Loading** | Yes (3 levels) | No (full load) | No |
| **Context Window** | Main (on-demand) | Main (immediate) | Separate |
| **Arguments** | No | Yes ($1, $2, $ARGUMENTS) | Via delegation |
| **Tool Restrictions** | Yes (`allowed-tools`) | Yes (`allowed-tools`) | Yes (`tools`) |
| **Model Override** | No | Yes (`model:`) | Yes (`model:`) |
| **Complexity** | High (complex workflows) | Low (simple prompts) | High (specialized tasks) |
| **Token Cost (Inactive)** | ~100 (metadata) | ~0 (not loaded) | ~0 (not loaded) |
| **Token Cost (Active)** | ~5k + on-demand | Full content | Separate context |
| **Best For** | Complex capabilities | Quick reusable prompts | Task delegation |
| **Example** | PDF processing | `/review` command | Security reviewer |
| **Released** | Oct 16, 2025 | Available since v1.0 | Available since v1.0 |

### When to Use

| Scenario | Use |
|----------|-----|
| Claude should automatically apply domain expertise | **Skill** |
| User wants explicit control over when to run | **Slash Command** |
| Need separate context for complex task | **Subagent** |
| Complex workflow with multiple files/scripts | **Skill** |
| Simple reusable prompt snippet | **Slash Command** |
| Task requires isolation from main conversation | **Subagent** |
| Need progressive content loading | **Skill** |
| Need to accept arguments from user | **Slash Command** |
| Want to run multiple specialized agents in parallel | **Subagent** |

### Code Examples

#### Skill
```markdown
# .claude/skills/pdf-processor/SKILL.md
---
name: pdf-processor
description: Extract text from PDFs. Use when working with PDF files.
---

Instructions...

See [FORMS.md](FORMS.md) for form filling.
```

Usage: `> Extract text from document.pdf` (automatic)

#### Command
```markdown
# .claude/commands/review.md
---
description: Review code for issues
---

Review this code for bugs and improvements.
```

Usage: `/review` (explicit)

#### Subagent
```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Security expert. Use for vulnerability scanning.
tools: Read, Grep, Glob
---

You are a security expert...
```

Usage: `> Use security-reviewer to scan the codebase` (delegation)

## Component Locations

| Component | Project | User | Plugin |
|-----------|---------|------|--------|
| **Settings** | `.claude/settings.json` | `~/.claude/settings.json` | N/A |
| **Commands** | `.claude/commands/*.md` | `~/.claude/commands/*.md` | `commands/*.md` |
| **Agents** | `.claude/agents/*.md` | `~/.claude/agents/*.md` | `agents/*.md` |
| **Skills** | `.claude/skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` | `skills/*/SKILL.md` |
| **Hooks** | `.claude/settings.json` | `~/.claude/settings.json` | `hooks/hooks.json` |
| **MCP** | `.claude/settings.json` | `~/.claude/settings.json` | `.mcp.json` |
| **Memory** | `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | N/A |

## Priority System

### Loading Priority

| Priority | Source | Overrides |
|----------|--------|-----------|
| **1 (Highest)** | Project (`.claude/`) | Everything |
| **2** | CLI args (`--agents`) | User, Plugin |
| **3** | Plugin | User |
| **4 (Lowest)** | User (`~/.claude/`) | Nothing |

### Conflict Resolution

**Same name skills**:
- Project skill overrides user skill
- User skill overrides plugin skill

**Same name commands**:
- Can coexist with namespace prefix
- `/command` vs `/plugin:command`

**Same name agents**:
- Project agent overrides user/plugin

## Distribution Methods

| Method | Best For | Setup |
|--------|----------|-------|
| **GitHub Marketplace** | Public/team sharing | `.claude-plugin/marketplace.json` in repo |
| **Git Marketplace** | Private repos | Git URL with marketplace.json |
| **Local Marketplace** | Development/testing | Local path with marketplace.json |
| **Direct Plugin** | Single plugin | Not via marketplace |
| **Settings.json** | Team auto-install | `extraKnownMarketplaces` field |

## Platform Availability

| Feature | Claude API | Claude Code | Agent SDK | Claude.ai |
|---------|-----------|-------------|-----------|-----------|
| **Pre-built Skills** | ✅ (pptx, xlsx, docx, pdf) | ❌ | ❌ | ✅ |
| **Custom Skills** | ✅ (upload via API) | ✅ (filesystem) | ✅ (filesystem) | ✅ (upload via UI) |
| **Subagents** | ❌ | ✅ | ✅ | ❌ |
| **Slash Commands** | ❌ | ✅ | ✅ | ❌ |
| **Hooks** | ❌ | ✅ | ✅ | ❌ |
| **Plugins** | ❌ | ✅ | ✅ | ❌ |
| **Marketplace** | ❌ | ✅ | ✅ | ❌ |
| **MCP** | ✅ (limited) | ✅ (full) | ✅ (full) | ✅ (limited) |

## Model Selection Guide

| Model | Speed | Cost | Capability | Use For |
|-------|-------|------|------------|---------|
| **Haiku** | Fastest | Lowest | Basic | Simple tasks, high volume |
| **Sonnet** | Fast | Medium | Strong | Most tasks, balanced |
| **Opus** | Slower | Highest | Maximum | Complex reasoning, security |

### When to Override Model

**Subagent/Command model field**:
```yaml
model: opus  # Use for this specific agent/command
```

**SDK**:
```typescript
agents: {
  'security': { model: 'opus' }  // More capable for security
  'formatter': { model: 'haiku' }  // Fast for simple tasks
}
```

## Tool Access Patterns

### By Use Case

| Use Case | Tools |
|----------|-------|
| **Read-only analysis** | `Read, Grep, Glob` |
| **Code review** | `Read, Grep, Glob` |
| **Test execution** | `Bash, Read, Grep` |
| **Code modification** | `Read, Edit, Write, Grep, Glob` |
| **Full development** | `Read, Edit, Write, Bash, Grep, Glob, WebSearch` |
| **Data analysis** | `Bash, Read, Write` |
| **Security scan** | `Read, Grep, Glob, Bash(security-tools:*)` |

### By Component Type

| Component | Syntax | Example |
|-----------|--------|---------|
| **Skill** | `allowed-tools:` | `allowed-tools: Read, Grep` |
| **Subagent** | `tools:` | `tools: Read, Grep, Glob` |
| **Command** | `allowed-tools:` | `allowed-tools: Bash(git*)` |
| **SDK** | `allowedTools:` | `allowedTools: ['Read', 'Grep']` |

## Hook Event Matrix

| Event | When Fires | Can Block | Output To | Common Use |
|-------|-----------|-----------|-----------|------------|
| **PreToolUse** | Before tool | Yes | Claude (on block) | Validation, permission |
| **PostToolUse** | After tool | No | Claude (on block) | Formatting, linting |
| **UserPromptSubmit** | Prompt submitted | Yes | Context (on success) | Add context, validate |
| **Notification** | Claude notifies | No | User only | Alerts, logging |
| **Stop** | Agent stops | Yes | Claude (on block) | Continue work |
| **SubagentStop** | Subagent stops | Yes | Subagent (on block) | Continue subagent |
| **PreCompact** | Before compact | No | User only | Checkpoint |
| **SessionStart** | Session starts | No | Context (stdout) | Setup, load context |
| **SessionEnd** | Session ends | No | User only | Cleanup, logging |

## Source Type Comparison

| Source Type | Format | Example | Best For |
|------------|---------|---------|----------|
| **GitHub** | `owner/repo` | `company/plugins` | Public/team repos |
| **Git** | Full URL | `https://gitlab.com/...` | Private Git servers |
| **Local** | File path | `./local-marketplace` | Development/testing |
| **URL** | Direct URL | `https://cdn.com/marketplace.json` | CDN distribution |

## Beta Headers (API)

| Feature | Header |
|---------|--------|
| **Skills** | `skills-2025-10-02` |
| **Code Execution** | `code-execution-2025-08-25` |
| **Files API** | `files-api-2025-04-14` |

All three required for Skills via API!

## Configuration Methods

| Method | Scope | Priority | Persistence |
|--------|-------|----------|-------------|
| **CLI flags** | Session | High | No |
| **settings.json** | Project/User | Medium | Yes |
| **Plugin config** | Plugin | Medium | Yes (with plugin) |
| **API params** | Request | Highest | No |

## Token Cost Comparison

Assuming 100 installed skills:

| Component | Startup Cost | Active Cost | Notes |
|-----------|--------------|-------------|-------|
| **Skills (metadata only)** | ~10k tokens | ~10k tokens | All metadata loaded |
| **Skills (1 active)** | ~10k tokens | ~15k tokens | +5k for active skill |
| **Skills (3 active)** | ~10k tokens | ~25k tokens | +15k for 3 skills |
| **Commands** | 0 tokens | Full content | Only when invoked |
| **Subagents** | ~100 tokens/agent | Separate context | Metadata in system prompt |

**Key insight**: Can install 100 skills for ~10k token cost. Skills only load when relevant!

## File Size Limits

| Component | Limit | Reason |
|-----------|-------|--------|
| **SKILL.md body** | < 500 lines | Performance (split into files if larger) |
| **Skill description** | 1024 chars | Schema validation |
| **Skill name** | 64 chars | Schema validation |
| **Additional skill files** | No limit | Loaded on-demand |
| **Command file** | No limit | Loaded when invoked |
| **Subagent file** | No limit | Loaded when delegated |

## Execution Context

| Component | Runs In | Has Access To |
|-----------|---------|---------------|
| **Skill** | Main agent context | Claude Code tools |
| **Skill script** | Bash execution | Filesystem, installed packages |
| **Subagent** | Separate context | Configured tools only |
| **Command** | Main agent context | Configured tools |
| **Hook** | Shell process | Filesystem, $CLAUDE_PROJECT_DIR |
| **MCP server** | Separate process | Configured in .mcp.json |

## Version Compatibility

| Component | Min Claude Code Version |
|-----------|------------------------|
| **Plugins** | 2.0.0 |
| **Skills** | 2.0.0 |
| **Marketplace** | 2.0.0 |
| **Subagents** | 2.0.0 |
| **Hooks** | 2.0.0 |
| **SlashCommand tool** | 1.0.124 |

## Summary Decision Matrix

### "I want to..."

| Goal | Use |
|------|-----|
| Add domain expertise Claude uses automatically | **Skill** |
| Create a reusable prompt I invoke manually | **Slash Command** |
| Delegate complex task with separate context | **Subagent** |
| React to events automatically | **Hook** |
| Connect external tools/APIs | **MCP Server** |
| Bundle multiple components | **Plugin** |
| Distribute plugins to team | **Marketplace** |
| Build custom agent programmatically | **Agent SDK** |
| Share team configuration | **settings.json** + git |
| Test before distributing | **Local marketplace** |

### "My use case is..."

| Use Case | Solution |
|----------|----------|
| Process PDFs with complex workflows | Skill with scripts |
| Quick code review shortcut | Slash command |
| Security scan needs isolation | Subagent |
| Auto-format on file save | Hook (PostToolUse) |
| Connect to company database | MCP server |
| Share all the above with team | Plugin |
| Distribute to community | Plugin + GitHub marketplace |
| Build SaaS with Claude | Agent SDK |
| Add context at session start | Hook (SessionStart) |
| Validate prompts before processing | Hook (UserPromptSubmit) |

### "I'm building for..."

| Audience | Strategy |
|----------|----------|
| **Myself** | User-level configs (`~/.claude/`) |
| **My team** | Project-level (`.claude/`) + git |
| **My company** | Private marketplace + settings.json |
| **Open source** | Public GitHub marketplace |
| **Customers/SaaS** | Agent SDK with API |

## Complexity Levels

| Level | Components | Example |
|-------|------------|---------|
| **Simple** | Single command | `/review` command |
| **Medium** | Subagent or simple skill | Security reviewer agent |
| **Complex** | Multi-file skill | PDF processor with scripts |
| **Advanced** | Plugin with multiple components | Company dev tools plugin |
| **Enterprise** | Marketplace with multiple plugins | Full company marketplace |

## Development Time Estimates

| Task | Estimated Time | Complexity |
|------|---------------|------------|
| Create simple slash command | 5 minutes | ⭐ |
| Create simple subagent | 10 minutes | ⭐ |
| Create simple skill (single file) | 15 minutes | ⭐⭐ |
| Create skill with scripts | 1-2 hours | ⭐⭐⭐ |
| Create hook | 30 minutes | ⭐⭐ |
| Create plugin (basic) | 30 minutes | ⭐⭐ |
| Create plugin (comprehensive) | 2-4 hours | ⭐⭐⭐⭐ |
| Create marketplace | 1 hour | ⭐⭐⭐ |
| Build SDK agent | 4-8 hours | ⭐⭐⭐⭐ |
| Full company marketplace | 1-2 weeks | ⭐⭐⭐⭐⭐ |

## Learning Curve

| Component | Learning Curve | Prerequisites |
|-----------|---------------|---------------|
| **Slash Command** | Low | Markdown |
| **Subagent** | Medium | Markdown, YAML, system prompts |
| **Skill (simple)** | Medium | Markdown, YAML, progressive disclosure |
| **Skill (complex)** | High | + Scripts, workflows, validation |
| **Hook** | High | JSON, bash, event handling |
| **Plugin** | Medium | File structure, manifest schema |
| **Marketplace** | Medium | JSON, Git, distribution |
| **Agent SDK** | High | TypeScript/Python, async programming |

## Common Combinations

### Pattern 1: Code Quality Plugin

```
Components:
- Command: /review (quick review)
- Skill: code-quality (deep analysis)
- Subagent: security-reviewer (security focus)
- Hook: Auto-lint on save

Result: Comprehensive code quality system
```

### Pattern 2: Deployment Pipeline

```
Components:
- Command: /deploy [env] (manual trigger)
- Skill: deployment-procedures (guides deployment)
- Subagent: deployment-agent (handles deployment)
- Hook: Pre-deployment validation
- MCP: Connect to deployment platform

Result: Complete deployment automation
```

### Pattern 3: Data Analysis Stack

```
Components:
- Skill: bigquery-analysis (SQL expertise)
- Skill: excel-processing (spreadsheet handling)
- Subagent: data-scientist (analysis tasks)
- Command: /analyze-sales (quick sales analysis)
- MCP: Database connections

Result: Full data analysis capability
```

## Sharing & Distribution

| Method | Scope | Setup Effort | Maintenance |
|--------|-------|--------------|-------------|
| **Git commit** | Team (project) | Low | Low |
| **Copy to ~/.claude/** | Personal | Very low | Manual sync |
| **Plugin (local)** | Development/test | Medium | Manual |
| **Plugin (GitHub)** | Team/public | Medium | Version control |
| **Marketplace (GitHub)** | Multi-plugin distribution | High | Catalog updates |
| **SDK deployment** | SaaS/API | High | Code deployment |

## Security Comparison

| Component | Risk Level | Mitigation |
|-----------|-----------|------------|
| **Skill** | Medium-High | Only from trusted sources, audit scripts |
| **Subagent** | Low-Medium | Tool restrictions, separate context |
| **Command** | Low | User explicitly invokes |
| **Hook** | High | Validates inputs, quote variables, sandbox |
| **Plugin** | Medium-High | Audit all components before install |
| **MCP Server** | Medium | Verify source, limit permissions |

## Performance Impact

| Component | Startup Impact | Runtime Impact |
|-----------|---------------|----------------|
| **Skill (metadata)** | ~100 tokens/skill | None if not triggered |
| **Skill (active)** | ~100 tokens | ~5k tokens + on-demand |
| **Subagent** | ~100 tokens metadata | Separate context |
| **Command** | None | Full load when invoked |
| **Hook** | None | Execution time (< 60s) |
| **Plugin** | Sum of components | Sum of components |

## Common Workflows Mapped

| Workflow | Primary Component | Supporting Components |
|----------|------------------|---------------------|
| **Automated testing** | Subagent (test-runner) | Hook (PostToolUse), Command (/test) |
| **Code review** | Skill (code-review) | Subagent (security), Hook (PostToolUse) |
| **Deployment** | Command (/deploy) | Skill (deployment), Hook (validation), MCP (platform) |
| **Documentation** | Skill (doc-generator) | Command (/docs), Hook (on code change) |
| **Security scanning** | Subagent (security) | Skill (security-patterns), Hook (PreToolUse) |
| **Data analysis** | Skill (bigquery) | Subagent (data-scientist), MCP (database) |

## Migration Paths

### From Commands to Skills

If your command is complex, convert to skill:

**Before** (command):
```markdown
# .claude/commands/process-pdf.md
Process PDF files...
[100 lines of instructions]
```

**After** (skill):
```
.claude/skills/pdf-processor/
├── SKILL.md (overview)
├── EXTRACTION.md (text extraction)
├── FORMS.md (form filling)
└── scripts/
    └── analyze.py
```

Benefits:
- Progressive loading
- Automatic invocation
- Bundled scripts
- Better organization

### From Subagents to Skills

If your subagent doesn't need separate context:

**Before** (subagent):
```markdown
# .claude/agents/pdf-expert.md
---
name: pdf-expert
description: PDF processing expert
---

Process PDFs...
```

**After** (skill):
```markdown
# .claude/skills/pdf-processor/SKILL.md
---
name: pdf-processor
description: Extract text from PDFs. Use when working with PDFs.
---

Process PDFs...
```

Benefits:
- Progressive loading
- Can bundle scripts
- Efficient context use

## Quick Decision Guide

```
Need domain expertise?
├─ Should Claude use automatically? → Skill
├─ Need separate context? → Subagent
└─ User controls when? → Command

Need automation?
└─ Event-based? → Hook

Need external tools?
└─ → MCP Server

Need to share?
├─ With team? → Git commit (.claude/)
├─ As package? → Plugin
└─ Multiple packages? → Marketplace

Need programmatic control?
└─ → Agent SDK
```

