# cc10x - Focused AI Development Assistant for Claude Code

**Smart orchestration that does what you ask. Fast results without losing focus.**

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://github.com/romiluz13/cc10x)
[![Version](https://img.shields.io/badge/version-2.1.0-green)](https://github.com/romiluz13/cc10x)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## What is cc10x?

A Claude Code plugin that provides **focused AI assistance** for software development:

- **Code Review** - Multi-dimensional analysis (security, quality, performance, UX, accessibility)
- **Feature Building** - Systematic implementation with quality enforcement
- **Bug Fixing** - LOG FIRST debugging approach
- **Validation** - Consistency checking across code, tests, and docs

**Core principle:** Does what you ask for. Nothing more.

---

## Installation

```bash
# Add marketplace
/plugin marketplace add romiluz13/cc10x

# Install plugin
/plugin install cc10x@cc10x
```

**Verify installation:**
```bash
/plugin      # Should list cc10x v2.1
```

---

## Usage

### Code Review

```bash
/cc10x review src/auth.js
```

Analyzes code across 5 dimensions and reports findings with specific fixes.

---

### Build Features

```bash
/cc10x build user authentication
```

Asks: Quick implementation or systematic approach?  
Delivers: Working code based on your choice.

---

### Fix Bugs

```bash
/cc10x fix login timeout issue
```

Uses LOG FIRST pattern: observe actual behavior, identify root cause, implement fix.

---

### Validate

```bash
/cc10x validate
```

Checks consistency between plans, code, tests, and documentation.

---

## Key Features

### Focused Execution

Only activates workflows you explicitly request. No forced orchestration.

**Example:**
- Ask for "build" → Gets built directly
- Ask for "review" → Gets reviewed only
- Ask for "plan and build" → Both workflows execute

**You control the depth.**

### Multi-Agent System

11 specialized agents handle different aspects:
- **Review agents** (parallel execution): Security, quality, performance, UX, accessibility
- **Execution agents**: Requirements, architecture, implementation, testing, deployment

**Agents activate only when needed for your specific request.**

### Quality Enforcement

- File size validation (<500 lines per file)
- TDD enforcement when requested
- Comprehensive error handling
- Production-ready code standards

---

## Commands

### `/cc10x review [target]`

Multi-dimensional code review.

**Analyzes:**
- Security vulnerabilities
- Code quality issues
- Performance bottlenecks
- UX problems
- Accessibility violations

**Time:** 3-5 minutes  
**Use:** Before every PR

---

### `/cc10x build [feature]`

Feature implementation.

**Offers two modes:**
- **Quick:** Direct implementation (fast)
- **Systematic:** Full TDD workflow (comprehensive)

**Time:** 45 minutes - 4 hours (depending on mode)  
**Use:** When building features

---

### `/cc10x fix [issue]`

Bug fixing with LOG FIRST pattern.

**Process:**
1. Add logging
2. Observe actual behavior
3. Identify root cause
4. Implement minimal fix
5. Add regression test

**Time:** 15-60 minutes  
**Use:** When debugging complex issues

---

### `/cc10x validate`

Cross-artifact consistency validation.

**Checks:**
- Code matches requirements
- Tests exist and pass
- Documentation current
- Risks addressed

**Time:** 10-20 minutes  
**Use:** Before merging, team projects

---

## Configuration

### User Rules Enforced

The plugin enforces best practices:
- Files under 500 lines (automatic validation)
- No placeholder code in implementations
- Comprehensive error handling
- Test coverage requirements
- TypeScript for JavaScript projects

**Configured via hooks and agent prompts.**

---

## Architecture

```
User Request
     ↓
cc10x Orchestrator (analyzes request)
     ↓
Activates specific agents needed
     ↓
Agents load relevant skills progressively
     ↓
Delivers focused result
```

**Simple. Direct. Focused on your request.**

---

## Skills

20 domain skills provide specialized knowledge:

**Planning & Architecture:**
- feature-planning, risk-analysis, deployment-patterns

**Development:**
- code-generation, test-driven-development, safe-refactoring

**Quality & Review:**
- code-review-patterns, security-patterns, performance-patterns

**Debugging & Navigation:**
- bug-fixing, systematic-debugging, codebase-navigation

**Design:**
- ui-design, ux-patterns, accessibility-patterns

**Orchestration:**
- task-breakdown, progress-tracker

**Skills load on-demand as agents need them.**

---

## When to Use

**Use cc10x for:**
- Code reviews (always valuable)
- Complex features (systematic approach prevents mistakes)
- Debugging (LOG FIRST saves time)
- Team projects (consistency validation)

**Skip cc10x for:**
- Trivial changes (faster to do manually)
- Emergencies (fix first, validate later)
- Simple library integrations (just follow docs)

**The orchestrator will recommend the right approach based on complexity.**

---

## Examples

### Review Before PR

```bash
/cc10x review src/features/payment/
```

Gets security, quality, and performance analysis before merging.

---

### Build with TDD

```bash
/cc10x build shopping cart feature
```

Chooses systematic mode → Full TDD implementation with tests.

---

### Quick Bug Fix

```bash
/cc10x fix form validation not working
```

LOG FIRST debugging → Root cause identified → Fix implemented.

---

## Requirements

- Claude Code installed
- Git (for version control)
- Development environment for your stack

---

## File Structure

```
.claude-plugin/
└── marketplace.json

plugins/cc10x/
├── .claude-plugin/
│   └── plugin.json
├── agents/          # 11 specialized agents
├── commands/        # Main command entry point
├── skills/          # 20 domain knowledge skills
├── hooks/           # Quality enforcement hooks
└── scripts/         # Validation scripts
```

---

## Contributing

Contributions welcome! 

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

See [GitHub Issues](https://github.com/romiluz13/cc10x/issues) for current work.

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Support

- **Issues:** https://github.com/romiluz13/cc10x/issues
- **Discussions:** https://github.com/romiluz13/cc10x/discussions

---

**cc10x - AI development assistance that stays focused on your goals.**
