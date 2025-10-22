# Contributing to cc10x

Thank you for your interest in contributing to cc10x! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cc10x.git
   cd cc10x
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Adding a New Command

Commands orchestrate workflows by coordinating sub-agents and enforcing quality gates.

**Location**: `.claude-plugin/commands/`

**Structure**:
```markdown
---
name: command-name
description: Brief description of what this command does
---

# Command Title

## Command Usage
[Usage instructions]

## Workflow Overview
[Phase breakdown]

## Parallel Execution Rules
[Table showing max parallel agents per phase]

## Phase 1: [Name]
[Detailed phase description]

...
```

**Key Requirements**:
- Document all phases with estimated time/tokens
- Include parallel execution rules table
- Provide usage examples
- Define quality gates between phases
- Specify which sub-agents are used

### Adding a New Sub-Agent

Sub-agents are specialized workers that perform specific tasks.

**Location**: `agents/`

**Structure**:
```markdown
---
name: agent-name
description: What this agent does and when to use it
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
---

# Agent Title

## Your Role
[Agent's responsibility]

## Automatic Skills
You MUST use these skills (automatic invocation):
- **skill-name**: Description

## Analysis Framework
[Systematic approach to the task]

## Reporting Format
[Expected output structure]

## Quality Gates
[Validation criteria]
```

**Key Requirements**:
- Specify auto-invoked skills
- Define tools needed
- Document parallelization safety (read-only vs write)
- Include analysis framework
- Provide code examples with ❌ bad / ✅ good patterns

### Adding a New Skill

Skills provide domain expertise that auto-invokes within agents.

**Location**: `skills/skill-name/`

**Structure**: Create `SKILL.md` with 3-stage progressive loading:

```markdown
---
name: Skill Name
description: What this skill provides
progressive: true
---

# Skill Name

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)
- **Skill**: [Name]
- **Purpose**: [Core purpose]
- **When**: [When to use]
- **Core Rule**: [One critical rule]
- **Sections Available**: [What's in Stage 2 & 3]

---

### Stage 2: Quick Reference (triggered - ~500 tokens)
[Essential patterns, quick checks, critical examples]

---

### Stage 3: Detailed Guide (on-demand - ~2000-3000 tokens)
[Comprehensive content with detailed examples]
```

**Key Requirements**:
- Add `progressive: true` to frontmatter
- Keep Stage 1 under 50 tokens (metadata only)
- Keep Stage 2 under 500 tokens (quick reference)
- Include code examples with ❌ bad / ✅ good patterns
- Reference authoritative sources

## Code Standards

### Documentation
- All commands, agents, and skills must be fully documented
- Use clear, concise language
- Provide real-world examples
- Include code snippets with proper syntax highlighting

### Naming Conventions
- **Commands**: kebab-case (`feature-build`, `bug-fix`)
- **Agents**: kebab-case (`security-reviewer`, `context-analyzer`)
- **Skills**: kebab-case (`test-driven-development`, `security-patterns`)
- **Files**: Match component name (`feature-build.md`, `security-reviewer.md`)

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature (command, agent, or skill)
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(commands): add /refactor command for safe refactoring workflow
fix(agents): correct security-reviewer OWASP Top 10 checklist
docs(readme): update installation instructions
refactor(skills): optimize progressive loading token counts
```

## Pull Request Process

1. **Update documentation**: Ensure README.md reflects your changes
2. **Update plugin.json**: Add new components to the manifest
3. **Test thoroughly**: Validate all changes work as expected
4. **Update CHANGELOG.md**: Document your changes
5. **Create pull request** with:
   - Clear title following commit message convention
   - Description of changes
   - Testing performed
   - Screenshots/examples if applicable

### PR Template

```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] New command
- [ ] New sub-agent
- [ ] New skill
- [ ] Bug fix
- [ ] Documentation
- [ ] Other (specify)

## Components Added/Modified
- Commands: [list]
- Agents: [list]
- Skills: [list]

## Testing
- [ ] Tested command execution
- [ ] Validated progressive loading
- [ ] Checked parallel execution rules
- [ ] Verified quality gates

## Token Usage
- Estimated tokens: [count]
- Progressive loading tested: Yes/No

## Documentation
- [ ] README.md updated
- [ ] plugin.json updated
- [ ] CHANGELOG.md updated
- [ ] All components documented
```

## Quality Standards

### For Commands
- [ ] All phases documented
- [ ] Parallel execution rules table included
- [ ] Quality gates defined
- [ ] Token usage estimated
- [ ] Time duration estimated
- [ ] Usage examples provided

### For Sub-Agents
- [ ] Frontmatter complete
- [ ] Auto-invoked skills documented
- [ ] Parallelization safety noted
- [ ] Analysis framework defined
- [ ] Code examples included (❌ bad / ✅ good)
- [ ] Quality gates specified

### For Skills
- [ ] Progressive loading implemented (3 stages)
- [ ] `progressive: true` in frontmatter
- [ ] Stage 1 under 50 tokens
- [ ] Stage 2 under 500 tokens
- [ ] Stage 3 comprehensive
- [ ] Code examples with patterns
- [ ] References to authoritative sources

## Testing Guidelines

### Manual Testing
1. Load the command/agent/skill in Claude Code
2. Verify progressive loading works (skills)
3. Test parallel execution (commands)
4. Validate quality gates enforce standards
5. Check token usage is within estimates

### Integration Testing
- Test commands end-to-end
- Verify sub-agents invoke skills correctly
- Confirm parallel execution works without conflicts
- Validate auto-healing context (long sessions)

## Project Structure

```
cc10x/
├── .claude/                    # Claude Code configuration
│   ├── context/
│   │   ├── config.json        # Progressive loading config
│   │   └── rules/             # Always-loaded context
│   ├── memory/
│   │   └── working-plan.md    # Session memory
│   └── settings.json          # Hooks and configuration
├── .claude-plugin/
│   ├── commands/              # Workflow orchestration
│   └── plugin.json            # Plugin manifest
├── agents/                    # Specialized sub-agents
├── skills/                    # Domain expertise
├── CLAUDE.md                  # Orchestrator brain
├── README.md                  # Main documentation
├── CHANGELOG.md               # Version history
└── LICENSE                    # MIT License
```

## Design Principles

### 1. Progressive Loading
Load context in stages to save tokens:
- Stage 1 (50 tokens): Metadata only
- Stage 2 (500 tokens): Quick reference
- Stage 3 (Full): Detailed content (only when needed)

### 2. Parallel Execution
- ✅ Parallelize read-only agents (analyzers, reviewers)
- ❌ NEVER parallelize implementers (file conflicts)

### 3. Auto-Invoked Skills
Skills provide expertise automatically - no manual selection needed.

### 4. Quality Gates
Validate after EVERY phase - fail-fast, fix issues immediately.

### 5. TDD Enforcement
All implementation must follow RED-GREEN-REFACTOR cycle.

## Community

### Questions or Issues?
- Open an issue on GitHub
- Provide context and examples
- Include error messages if applicable

### Feature Requests
- Open an issue with `enhancement` label
- Describe the use case
- Explain expected behavior
- Consider submitting a PR!

## License

By contributing to cc10x, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to cc10x!** Your contributions help create better developer productivity tools for everyone. 🚀
