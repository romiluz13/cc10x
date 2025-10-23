# Official Anthropic Documentation & Resources

## Primary Official Sources

### 1. Claude Code Documentation
**URL:** https://docs.anthropic.com/en/docs/claude-code

**Key Topics:**
- Getting started with Claude Code
- Plugin system architecture
- Sub-agents configuration
- Skills system
- Settings and configuration
- Tutorials and workflows

### 2. Sub-Agents Documentation
**URL:** https://docs.anthropic.com/en/docs/claude-code/sub-agents

**Key Insights:**
- Sub-agents are specialized AI assistants within Claude Code
- Each sub-agent has isolated context window
- Configured via Markdown files with YAML frontmatter
- Can be invoked automatically or explicitly
- Support tool permissions and custom system prompts

**File Structure:**
```markdown
---
name: "Agent Name"
description: "What this agent does"
tools: ["tool1", "tool2"]
---

# Agent System Prompt

Detailed instructions for this specialized agent...

## When to Use

Examples of when Claude should invoke this agent...
```

**Locations:**
- User-level: `~/.claude/agents/*.md`
- Project-level: `.claude/agents/*.md`

**Management:**
- Use `/agents` command for interactive management
- Create, edit, delete via CLI interface
- Agents auto-invoke based on context

### 3. Skills Documentation  
**URL:** https://www.anthropic.com/news/skills

**Announcement (October 16, 2025):**
Anthropic introduced Agent Skills as modular capabilities that Claude dynamically loads for specialized tasks.

**Core Concepts:**
- **Composable**: Mix and match skills for complex workflows
- **Portable**: Share skills across projects and teams
- **Efficient**: Load only when needed (token optimization)
- **Powerful**: Include executable code when needed

**Skill Components:**
```
skill-name/
  SKILL.md          # Main skill definition
  scripts/          # Optional executable scripts
  reference.md      # Optional reference materials
  examples/         # Optional examples
```

**SKILL.md Format:**
```markdown
---
name: "Skill Name"
description: |
  What this skill does. Use when you need X.
  Trigger phrases: "keyword1", "keyword2"
---

## What This Skill Does

Detailed explanation of capabilities...

## When It Activates

- User mentions "keyword"
- Task involves X
- Context suggests Y

## How It Works

1. Step-by-step process
2. Best practices built-in
3. Error handling included
```

### 4. Engineering Blog: Equipping Agents with Skills
**URL:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

**Key Insights:**

**Design Pattern:**
Skills are instruction manuals that teach Claude:
- WHEN to use a capability
- HOW to use it correctly
- WHAT patterns to follow

**Architecture:**
```
User Request
    ↓
Claude reads available SKILL.md frontmatter
    ↓
Detects trigger phrases
    ↓
Loads full SKILL.md content
    ↓
Applies skill knowledge
    ↓
Executes task with expertise
```

**Best Practices:**
1. Clear trigger phrases in description
2. Comprehensive "When to Use" section
3. Step-by-step workflows
4. Code examples
5. Error handling patterns
6. Progressive disclosure (basics → advanced)

**Example Sizes:**
- Anthropic examples: ~500 bytes (minimal)
- Production skills: ~3,000+ bytes (comprehensive)
- Include: workflows, examples, error handling

### 5. Plugin Reference
**URL:** https://docs.anthropic.com/en/docs/claude-code/plugins-reference

**Plugin Components:**

**Commands:**
- Custom slash commands
- Trigger workflows or templates
- Defined in `/commands/*.md`
- YAML frontmatter + markdown content

**Agents:**
- Specialized sub-agents
- Domain-specific expertise
- Defined in `/agents/*.md`
- Auto-invoke or explicit delegation

**Skills:**
- Auto-activating capabilities
- Context-aware invocation
- Defined in `/skills/*/SKILL.md`
- Loaded dynamically by Claude

**Hooks:**
- Event-driven automation
- Session lifecycle integration
- Defined in `/hooks/hooks.json` + scripts
- Triggers: session-start, pre-compact, etc.

### 6. Settings Documentation
**URL:** https://docs.anthropic.com/en/docs/claude-code/settings

**Configuration Locations:**

**User Settings:** `~/.claude/settings.json`
```json
{
  "extraKnownMarketplaces": {
    "marketplace-name": {
      "source": {
        "source": "github",
        "repo": "owner/repo-name"
      }
    }
  },
  "enabledPlugins": {
    "plugin-name@marketplace": true
  }
}
```

**Project Settings:** `.claude/settings.json`
```json
{
  "customInstructions": "Project-specific instructions",
  "subAgents": {
    "enabled": true
  }
}
```

### 7. Tutorials and Common Workflows
**URL:** https://docs.anthropic.com/en/docs/claude-code/tutorials

**Workflow Examples:**
- Using specialized sub-agents
- Creating custom commands
- Building skill libraries
- Implementing hooks
- Progressive context loading
- Auto-healing implementations

### 8. Claude Code SDK
**URL:** https://docs.anthropic.com/s/claude-code-sdk

**SDK Components:**
- TypeScript/JavaScript API
- Plugin development tools
- Testing utilities
- Deployment helpers

### 9. Official Skills Repository
**URL:** https://github.com/anthropics/skills

**Contents:**
- Example skills from Anthropic
- Skill templates
- Best practices
- Documentation

**Notable Skills:**
- Document creation
- Data analysis
- Code review patterns
- Research workflows

## Key Official Quotes

### On Skills (from announcement):
> "Skills are modular packages of instructions, scripts, and resources that Claude can dynamically load to perform specialized tasks more effectively. They enable Claude to adapt to your specific workflows while remaining efficient and maintaining its general capabilities."

### On Sub-Agents (from documentation):
> "Sub-agents are specialized AI assistants that can be configured at both user and project levels. Each sub-agent has its own context window, system prompt, and tool permissions, allowing for focused expertise on specific types of tasks."

### On Plugin Architecture (from reference):
> "Claude Code plugins extend Claude's capabilities through four primary mechanisms: commands for user-triggered workflows, agents for specialized assistance, skills for automatic capability enhancement, and hooks for event-driven automation."

## Official Best Practices

### From Anthropic Engineering:

**1. Token Efficiency:**
- Load skills progressively, not all at once
- Use frontmatter for quick scanning
- Include full content only when activated
- Result: 70-90% token savings

**2. Skill Design:**
- Clear trigger phrases in description
- Comprehensive but focused scope
- Include examples and error handling
- Test with real-world scenarios

**3. Sub-Agent Configuration:**
- One task, one agent (isolation)
- Clear role definition
- Explicit tool permissions
- Context-appropriate prompts

**4. Command Structure:**
- Descriptive names (verb-noun pattern)
- Clear purpose in frontmatter
- Step-by-step workflows
- Quality gates between phases

**5. Hook Implementation:**
- Minimal overhead
- Idempotent operations
- Error handling
- Progress tracking

## Version Information

**Research Date:** October 22, 2025
**Claude Code Version:** Public Beta (October 2025)
**Skills Feature:** Launched October 16, 2025
**Plugin System:** Generally Available

## Official Support Channels

- **Documentation:** https://docs.anthropic.com/en/docs/claude-code
- **Discord:** Claude Developers Community (40,000+ members)
- **GitHub:** https://github.com/anthropics (official examples)
- **Support:** Through Claude Code interface

## Related Official Resources

1. **Anthropic Homepage:** https://www.anthropic.com
2. **Blog:** https://www.anthropic.com/news
3. **Engineering Blog:** https://www.anthropic.com/engineering
4. **Research Papers:** Focus on AI safety and capabilities
5. **Claude API Docs:** https://docs.anthropic.com

## Updates and Changelog

The official documentation is actively maintained and updated:
- Weekly documentation improvements
- Monthly feature additions
- Quarterly major updates
- Community feedback integration

**Recommendation:** Check official docs regularly for:
- New features and capabilities
- Updated best practices
- Security advisories
- API changes

