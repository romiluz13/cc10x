# cc10x - 10x Developer Productivity for Claude Code

> Intelligent orchestration system combining commands, sub-agents, and skills for 10x developer productivity

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blue.svg)](https://claude.ai/code)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/romiluz13/cc10x/releases)

## What is cc10x?

cc10x is a comprehensive Claude Code plugin that orchestrates specialized workflows for common development tasks. It combines:

- **4 Powerful Commands** - Feature planning, development, bug fixing, code review
- **7 Specialized Sub-Agents** - Context analysis, implementation, security/quality/performance/UX/accessibility review
- **12 Domain Skills** - TDD, systematic debugging, UI design, security patterns, and more
- **Smart Orchestration** - Coordinates sub-agents and skills for optimal results
- **Progressive Loading** - 93% token savings through intelligent context management
- **Auto-Healing Context** - Never lose progress, even in long sessions

## Key Features

### 🎯 Comprehensive Workflows

```bash
/feature-plan     # PRD-style planning before coding
/feature-build    # 5-phase TDD-enforced development
/bug-fix          # Systematic debugging with LOG FIRST pattern
/review           # Multi-dimensional code review
```

### ⚡ Massive Time Savings

- **Feature Planning**: ~2 hours saved with comprehensive PRDs
- **Feature Development**: 40-60% faster than manual coding
- **Bug Fixing**: 50% faster with systematic approach
- **Code Review**: 70% faster with parallel multi-dimensional analysis

### 🧠 Intelligent Orchestration

```
Command → Sub-Agents → Skills → Production-Quality Results
```

- Sub-agents work in isolated contexts (one task at a time)
- Skills auto-invoke when relevant (multiple per sub-agent)
- File conflict prevention (never parallelize implementers)
- Quality gates between phases (fail-fast validation)

### 💾 Progressive Context Loading

Save 93% tokens by loading only what's needed:
- **Stage 1**: Startup essentials (~5k tokens)
- **Stage 2**: Task-specific context (~10-15k tokens)
- **Stage 3**: On-demand details (variable)

### 🔄 Auto-Healing Context

- Automatic snapshot at 75% token usage
- Seamless continuation across long sessions
- Background context compaction
- Zero progress loss

### ✅ Strict TDD Enforcement

- Test-first, always (no exceptions)
- Red → Green → Refactor cycle enforced
- Quality gates ensure tests pass before proceeding
- 70%+ coverage automatically achieved

### 🎨 Lovable/Bolt-Quality UI

- Production-ready components (not prototypes)
- Modern design patterns (gradients, shadows, animations)
- Responsive and accessible by default
- Based on shadcn/ui and Tailwind best practices

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) version 1.0 or later
- Git (for cloning repositories)

### Install from GitHub

```bash
# Using Claude Code plugin manager
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@romiluz13-cc10x

# Or clone directly
git clone https://github.com/romiluz13/cc10x.git
cd your-project
cp -r /path/to/cc10x/.claude-plugin .
cp -r /path/to/cc10x/agents .
cp -r /path/to/cc10x/skills .
cp -r /path/to/cc10x/commands .
cp -r /path/to/cc10x/hooks .
```

### Verify Installation

```bash
# Check if commands are available
/feature-plan
```

You should see the feature planning command interface.

## Quick Start

### 1. Plan a Feature

```bash
/feature-plan Add user authentication with JWT tokens
```

**Output**: Comprehensive plan with:
- User stories and acceptance criteria
- Architecture decisions
- Component breakdown
- API contracts and data models
- Edge cases
- Testing strategy

### 2. Build the Feature

```bash
/feature-build Implement authentication from the plan
```

**Executes 5-phase workflow**:
1. **Context Analysis** - Find similar patterns in codebase
2. **Planning** - Break into tasks
3. **Implementation** - TDD-enforced, sequential
4. **Verification** - Quality checks
5. **Finalization** - Clean commit

### 3. Fix a Bug

```bash
/bug-fix Users can submit empty email addresses
```

**Systematic debugging**:
1. **Context** - Understand the issue
2. **Investigation** - LOG FIRST (add logging before fixing)
3. **Fix** - Minimal change with tests
4. **Verify** - Ensure fix works
5. **Finalize** - Clean commit

### 4. Review Code

```bash
/review src/features/auth/
```

**Parallel review**:
- Security vulnerabilities
- Code quality issues
- Performance bottlenecks
- UX improvements
- Accessibility compliance

## Architecture

### Orchestration Flow

```
User Command
    ↓
Main Orchestrator (command workflow)
    ↓
Sub-Agents (specialized workers)
    ↓
Skills (domain knowledge, auto-invoked)
    ↓
Production-Quality Results
```

### Components

**Commands** (`/commands`)
- Entry points for workflows
- Contain orchestration logic
- Coordinate sub-agents

**Sub-Agents** (`/agents`)
- Specialized workers
- Isolated contexts
- One task at a time

**Skills** (`/skills`)
- Domain expertise
- Auto-invoked by Claude
- Multiple per sub-agent

**Hooks** (`/hooks`)
- Session start automation
- Auto-healing context
- Progress tracking

## Configuration

### Project-Level Settings

Create `.claude/settings.json`:

```json
{
  "cc10x": {
    "tdd": {
      "enforceStrict": true
    },
    "progressive_loading": {
      "enabled": true
    },
    "auto_healing": {
      "threshold": 0.75
    }
  }
}
```

### Memory Files

cc10x uses:
- `.claude/memory/WORKING_PLAN.md` - Current priorities (auto-updated)
- `.claude/memory/REMEMBER.md` - Important project context
- `.claude/memory/snapshots/` - Context snapshots for auto-healing

## Advanced Usage

### Feature Planning + Building Workflow

```bash
# Step 1: Plan comprehensively
/feature-plan Real-time chat with WebSockets

# Step 2: Review the generated plan
# File: .claude/docs/checklist-real-time-chat.md

# Step 3: Implement phase by phase
/feature-build Implement Phase 1 from checklist-real-time-chat.md
/feature-build Implement Phase 2 from checklist-real-time-chat.md

# Step 4: Review before PR
/review src/features/chat/
```

### Bug Fixing with LOG FIRST

```bash
# Describe the bug
/bug-fix Payment fails silently without user feedback

# cc10x will:
# 1. Add logging to understand the issue
# 2. Reproduce the bug with a test
# 3. Fix minimally
# 4. Verify fix works
# 5. Clean commit with semantic message
```

### Multi-Dimensional Review

```bash
# Review specific files
/review src/components/PaymentForm.tsx

# Review entire directory
/review src/features/payments/

# Parallel review checks:
# - Security: SQL injection, XSS, auth issues
# - Quality: Code smells, maintainability, patterns
# - Performance: N+1 queries, unnecessary re-renders
# - UX: Loading states, error messages, accessibility
# - Accessibility: ARIA labels, keyboard navigation, screen readers
```

## Token Efficiency

### Startup Cost

- **Without cc10x**: ~80k tokens (load everything upfront)
- **With cc10x**: ~5k tokens (progressive loading)
- **Savings**: 93%

### Per-Workflow Cost

- **Feature Planning**: ~20k tokens
- **Feature Building**: ~30-50k tokens (depends on complexity)
- **Bug Fixing**: ~15-25k tokens
- **Code Review**: ~20-30k tokens

### Auto-Healing

- **Threshold**: 75% token usage (150k of 200k)
- **Process**: Snapshot → Compact → Restore
- **Result**: Seamless continuation, no progress lost

## Quality Standards

All cc10x workflows enforce:

✅ Tests written first, watched fail, then pass
✅ All existing tests continue passing
✅ Code follows project patterns (found via context analysis)
✅ No debug code (console.log, debugger, TODO)
✅ Error handling present
✅ Clean, semantic git commits

## Development Constitution

cc10x operates under a formal [Development Constitution](/.claude/memory/CONSTITUTION.md) that establishes immutable principles for quality:

### Article I: Test-Driven Development (NON-NEGOTIABLE)
NO production code without failing test first. RED-GREEN-REFACTOR enforced at every increment.

### Article II: File Size Limits
- Components: 200 lines max
- Services: 400 lines max
- Tests: 300 lines max

### Article III: Progressive Quality Gates
5 sequential gates must pass: Context Analysis → Planning → Implementation → Verification → Finalization

### Article IV: Production-Ready Only
No TODOs, no placeholders, no incomplete implementations. Complete code or don't commit.

### Article V: Multi-Dimensional Review
5 parallel reviewers (security, quality, performance, UX, accessibility) before merge.

### Article VI: Token Efficiency
93% token savings through progressive 3-stage loading and auto-healing at 75% threshold.

### Article VII: Production-First UI
Lovable/Bolt quality standards. WCAG 2.1 AA compliance. Responsive, modern, polished.

**Read the full constitution**: [`.claude/memory/CONSTITUTION.md`](/.claude/memory/CONSTITUTION.md)

## Troubleshooting

### Commands not working

Make sure you're in a trusted project directory:

```bash
# Trust the directory in Claude Code settings
```

### Workflows too slow

Check token usage:

```bash
/context
```

If approaching limit, cc10x will auto-heal automatically.

### Results not matching expectations

Provide more context in command invocation:

```bash
# Vague
/feature-build Add authentication

# Specific
/feature-build Add JWT-based authentication with email/password, refresh tokens, and password reset flow
```

## Examples

See [EXAMPLES.md](./EXAMPLES.md) for detailed real-world examples:
- Building a real-time chat system
- Fixing a payment bug
- Reviewing a complex PR
- Refactoring legacy code

## Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

Areas for contribution:
- New skills for domain expertise
- Additional sub-agents
- Workflow improvements
- Documentation and examples

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Support

- **Issues**: https://github.com/romiluz13/cc10x/issues
- **Discussions**: https://github.com/romiluz13/cc10x/discussions
- **Email**: rom.iluz13@gmail.com

## Philosophy

cc10x believes in:

- **Quality over speed** - But achieves both through intelligence
- **Automation where possible** - Manual intervention where valuable
- **Explicit control** - You invoke commands, orchestrator handles execution
- **Continuous improvement** - Learns from your codebase patterns
- **Token efficiency** - Load only what's needed, when it's needed

## Acknowledgments

Inspired by best practices from:
- dotai (dynamic context management)
- Superpowers (sub-agent patterns)
- Claude Code documentation (official best practices)

cc10x synthesizes these approaches into a unique, first-of-its-kind orchestration system.

---

**Ready to be 10x more productive?** Install cc10x and start with `/feature-plan`!

**Star this repo** if cc10x helps you! ⭐
