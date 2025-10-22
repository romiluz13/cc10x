# cc10x - 10x Developer Productivity with Claude Code

Welcome! You're using **cc10x**, an intelligent orchestration system that combines commands, sub-agents, and skills to dramatically accelerate development workflows.

## What is cc10x?

cc10x provides four powerful workflows for common development tasks:

1. **Feature Planning** (`/feature-plan`) - Comprehensive PRD-style planning before coding
2. **Feature Development** (`/feature-build`) - Complete implementation with TDD enforcement
3. **Bug Fixing** (`/bug-fix`) - Systematic debugging with LOG FIRST pattern
4. **Code Review** (`/review`) - Multi-dimensional analysis (security, quality, performance, UX, accessibility)

Each workflow orchestrates specialized sub-agents and auto-invokes relevant skills to deliver production-quality results efficiently.

## Quick Start

### Planning a Feature

```
/feature-plan Add user authentication with JWT tokens
```

Creates comprehensive feature plan including:
- Requirements analysis and edge cases
- Architecture decisions and API design
- Database schema and integration points
- Security considerations
- Implementation roadmap

### Building a Feature

```
/feature-build Add user authentication based on the plan
```

Executes 5-phase development workflow:
1. **Context Analysis** - Find similar patterns in your codebase
2. **Planning** - Break into implementable tasks
3. **Implementation** - TDD-enforced sequential development
4. **Verification** - Multi-dimensional quality checks
5. **Finalization** - Clean commit with semantic message

### Fixing a Bug

```
/bug-fix Users can submit empty email addresses
```

Runs systematic debugging workflow:
1. **Context** - Understand the issue
2. **Investigation** - LOG FIRST (add logging before fixing)
3. **Fix** - Minimal, targeted change with tests
4. **Verify** - Ensure fix works and doesn't break anything
5. **Finalize** - Clean commit

### Reviewing Code

```
/review src/features/auth/
```

Parallel multi-dimensional review:
- Security patterns and vulnerabilities
- Code quality and maintainability
- Performance bottlenecks
- UX improvements
- Accessibility compliance

## Key Features

### Progressive Context Loading
- **93% token savings** - Load only what's needed, when it's needed
- Stage 1: Startup essentials (5k tokens)
- Stage 2: Task-specific context (10-15k tokens)
- Stage 3: On-demand details (variable)

### Auto-Healing Context
- **Automatic snapshot at 75% token usage** - Never lose progress
- Seamless continuation across long sessions
- Background context compaction

### Strict TDD Enforcement
- **Test-first, always** - No exceptions
- Red → Green → Refactor cycle enforced
- Quality gates ensure tests pass before proceeding

### File Conflict Prevention
- **Never parallelize implementation** - One implementer at a time
- Safe parallelization for analysis tasks
- Automatic conflict detection

### Lovable/Bolt-Quality UI
- **Production-ready components** - Not prototypes
- Responsive, accessible, polished
- Based on modern design patterns

## How It Works

```
You (user)
  ↓ invoke command
Main Orchestrator (command workflow)
  ↓ dispatch
Specialized Sub-Agents (implementer, reviewers, analyzers)
  ↓ auto-invoke
Domain Skills (TDD, code-generation, security-patterns, etc.)
  ↓ produce
Production-Quality Results
```

**Sub-Agents**: Specialized workers with isolated contexts (one task at a time)
**Skills**: Domain expertise that auto-invokes when relevant (multiple per sub-agent)

## When to Use Each Workflow

| Workflow | Use When | Time Savings |
|----------|----------|--------------|
| `/feature-plan` | Starting new feature, need architecture clarity | ~2 hours saved in planning |
| `/feature-build` | Implementing planned feature | 40-60% faster than manual |
| `/bug-fix` | Issue reported, need systematic fix | 50% faster debugging |
| `/review` | Before PR, after implementation, code audit | 70% faster than manual review |

## Best Practices

1. **Plan Before Building** - Use `/feature-plan` first for complex features
2. **Trust the Process** - Let workflows orchestrate, don't micromanage
3. **One Workflow at a Time** - Complete current workflow before starting another
4. **Review Often** - Run `/review` after each feature or bug fix
5. **Watch Token Usage** - Auto-healing kicks in at 75%, but stay aware

## Quality Standards

All cc10x workflows enforce:
- ✅ Tests written first, watched fail, then pass
- ✅ All existing tests continue passing
- ✅ Code follows project patterns (found via context analysis)
- ✅ No debug code (console.log, debugger, TODO)
- ✅ Error handling present
- ✅ Clean, semantic git commits

## Configuration

cc10x works out of the box, but you can customize:
- `.claude/settings.json` - Workflow preferences
- `.claude/memory/WORKING_PLAN.md` - Current priorities (auto-updated)
- `.claude/memory/REMEMBER.md` - Important project context

## Need Help?

- **Commands not working?** - Make sure you're in a trusted project directory
- **Workflows too slow?** - Check token usage with `/context` command
- **Results not matching expectations?** - Provide more context in command invocation
- **Bug reports**: https://github.com/romiluz13/cc10x/issues

## Philosophy

cc10x believes in:
- **Quality over speed** - But achieves both through intelligence
- **Automation where possible** - Manual intervention where valuable
- **Explicit control** - You invoke commands, orchestrator handles execution
- **Continuous improvement** - Learns from your codebase patterns

---

**Ready to be 10x more productive?** Start with `/feature-plan` for your next feature!
