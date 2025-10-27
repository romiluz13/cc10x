# CC10x v3.0 - Intelligent AI Development Assistant

Professional Claude Code plugin with specialized agents, progressive skills, and automated quality enforcement.

## Overview

CC10x transforms complex development tasks into systematic, high-quality implementations through intelligent orchestration of specialized AI agents and progressive skill loading.

## Core Features

- **10 Specialized Agents** - Each with distinct expertise and clear boundaries
- **9 Progressive Skills** - Load on-demand for 40-60% token efficiency
- **5-Agent Parallel Review** - Comprehensive analysis in 3 minutes
- **Automated Quality Gates** - Built-in verification and size limits
- **Strategic Pause Points** - Human verification at critical moments

## Quick Start

```bash
# Plan a feature
/plan "Add user authentication with JWT"

# Implement phase-by-phase
/build PLAN.md balanced

# Comprehensive review
/review src/auth/
```

## Workflow

```
/plan → Comprehensive Plan → /build → Production Code → /review → Validated
         ↓                    ↓                           ↓
    8-dimensions         Phase-by-Phase            5 Parallel
    Risk Analysis        + Pause Points             Reviewers
```

## Commands

### `/plan [feature-description]`
Creates comprehensive implementation plans with risk analysis and phase breakdown.

**Features:**
- Researches existing codebase patterns
- 8-dimensions risk analysis framework
- Clear scope definition (doing vs not doing)
- Phases with automated/manual verification split
- Pause points for human confirmation

**Example:**
```bash
/plan "Add user profile with avatar upload and validation"
```

### `/build [plan-file] [strategy]`
Implements features phase-by-phase with quality verification.

**Strategies:**
- `fast` - Direct implementation, basic tests
- `balanced` - Complete implementation with comprehensive tests (default)
- `tdd` - Test-driven development

**Features:**
- No placeholders or TODOs
- Automated checks (tests, lint, type check, build)
- Strategic pause points for manual verification
- Complexity gate warns if manual coding is more efficient

**Example:**
```bash
/build PLAN.md balanced
```

### `/test [target] [strategy]`
Generates comprehensive test coverage.

**Strategies:**
- `unit` - Function/class level tests
- `integration` - Component interaction tests
- `e2e` - Full user workflow tests
- `all` - Comprehensive coverage

**Features:**
- >80% coverage target
- Happy paths, edge cases, error scenarios
- AAA pattern (Arrange, Act, Assert)

**Example:**
```bash
/test src/auth/auth.service.ts all
```

### `/debug [error-description]`
Systematic debugging with LOG FIRST methodology.

**Features:**
- Strategic logging before changes
- Pattern analysis
- Root cause identification (not symptoms)
- Minimal fix
- Regression test

**Example:**
```bash
/debug "Login fails with 500 for OAuth users"
```

### `/review [target]`
Parallel 5-agent code review in 3 minutes.

**Reviewers:**
- Security - Vulnerabilities, exploits
- Quality - Maintainability, complexity
- Performance - Bottlenecks, optimization
- UX - User flows, error handling
- Accessibility - WCAG compliance

**Example:**
```bash
/review src/new-feature/
```

## Agents

### Planning & Implementation

**Planner** - Comprehensive plans with verification split
- Researches codebase patterns
- Applies 8-dimensions risk framework
- Defines clear scope boundaries
- Creates phased implementation plan

**Builder** - Production-quality implementation
- Phase-by-phase execution
- Automated verification (tests, lint, build)
- Strategic pause points
- No placeholders or incomplete code

**Tester** - Comprehensive test coverage
- Unit, integration, and E2E tests
- >80% coverage target
- Edge cases and error scenarios

**Debugger** - Systematic issue resolution
- LOG FIRST methodology
- Root cause analysis
- Minimal targeted fixes
- Regression test creation

### Specialized Reviewers (Parallel Execution)

**Security Reviewer** - Vulnerability analysis
- Real exploitable issues
- Proof-of-concept demonstrations
- Mitigation strategies

**Quality Reviewer** - Maintainability assessment
- SOLID principles
- Complexity metrics
- Technical debt identification

**Performance Analyzer** - Efficiency optimization
- Bottleneck identification
- Algorithmic improvements
- Caching strategies

**UX Reviewer** - User experience evaluation
- Flow analysis
- Error message clarity
- Intuitive interactions

**Accessibility Reviewer** - WCAG compliance
- Level AA standards
- Screen reader compatibility
- Keyboard navigation

### Utilities

**Codebase Mapper** - Project structure navigation
- Architecture understanding
- Dependency analysis
- Pattern identification

## Skills (Progressive Loading)

Skills load metadata (~100 tokens) first, full content (~5k tokens) only when needed:

- **8-dimensions** - Comprehensive risk analysis framework
- **security-patterns** - Secure coding practices
- **quality-patterns** - SOLID principles, maintainability
- **performance-patterns** - Optimization strategies
- **testing-patterns** - Test design and coverage
- **systematic-debugging** - Scientific debugging methodology
- **code-generation** - Production patterns and templates
- **ux-patterns** - Nielsen's usability heuristics
- **wcag-patterns** - Web accessibility guidelines

## Architecture

### Three-Layer System

```
Commands (User Interface)
   ↓
Agents (Specialized Workers)
   ↓
Skills (Knowledge Libraries)
```

### Design Principles

**1. Explicit Boundaries**
Every agent has defined DO/DON'T responsibilities to prevent overlap.

**2. Verification Split**
Plans separate automated (tests, lint) from manual (UI, UX) verification.

**3. Progressive Loading**
Skills load incrementally, saving 40-60% tokens vs verbose approaches.

**4. Strategic Pauses**
Human confirmation required before proceeding to next phase.

## Automated Hooks

### File Size Enforcement
Automatically checks files don't exceed 500 lines, warning when limits reached.

### Session Start
Provides context and recommendations at session initialization.

## Complete Example: Authentication Feature

```bash
# Step 1: Plan (2 minutes)
/plan "Add JWT authentication with refresh tokens"
```

**Planner Output:**
```markdown
## What We're Doing
- JWT authentication
- Refresh token mechanism
- Secure token storage

## What We're NOT Doing
- OAuth providers (future phase)
- Multi-factor auth (separate epic)

## Phase 1: Database Schema
Automated Verification:
- Tests pass
- Type check clean
Manual Verification:
- Schema correctness
- No data loss risk
⏸️ PAUSE
```

```bash
# Step 2: Build (20-30 minutes)
/build PLAN.md balanced
```

**Builder Output:**
```
Implementing Phase 1...

✅ Tests: 12/12 passing
✅ Type check: Clean
✅ Lint: Clean
✅ Build: Success

⏸️ Phase 1 Complete - Manual Verification Required

Please verify:
- [ ] Migration script looks correct
- [ ] Indexes are appropriate
- [ ] No data loss risk

Confirm to proceed to Phase 2?
```

*You verify → Confirm*

```bash
# Step 3: Review (3 minutes)
/review src/auth/
```

**Review Output:**
```
Security: ⚠️ HIGH - JWT secret hardcoded, use env variable
Quality: ✅ Clean, well-structured
Performance: ✅ No issues
UX: ⚠️ LOW - Error messages could be more specific
Accessibility: N/A (backend)
```

## Best Practices

### 1. Trust the Pause Points
Actually test features when builder pauses - catches issues early.

### 2. Review Incrementally
Run `/review` during development, not just at the end.

### 3. Read Plans Thoroughly
Plans save implementation time - review and adjust before building.

### 4. Choose Right Strategy
- **fast**: Prototypes, experiments
- **balanced**: Production features
- **tdd**: Critical business logic

### 5. Respect Complexity Gate
If warned "manual is cheaper," it's probably right.

## When to Use CC10x

### ✅ Ideal For:
- Complex features (complexity >= 3)
- Comprehensive code reviews
- Consistent quality standards
- New project scaffolding
- Large refactoring efforts
- Learning best practices

### ❌ Not Ideal For:
- Trivial tasks (complexity <= 2)
- Single-line changes
- Quick config tweaks
- Emergency hotfixes (unless systematic approach needed)

## Installation

1. Copy `plugins/cc10x` directory to your Claude Code plugins folder
2. Reload Claude Code
3. Verify with `/plan` command

## Requirements

- Claude Code (latest version)
- Git (for some commands)
- Project with test/lint setup (for automated verification)

## Performance Metrics

- **Token Efficiency**: 40-60% savings via progressive loading
- **Review Speed**: 3 minutes (5 parallel agents) vs 15 minutes (sequential)
- **Quality**: 8-dimensions risk coverage
- **Cost Awareness**: Complexity gate prevents waste

## Troubleshooting

### Commands Not Appearing
- Verify `plugins/cc10x` in correct location
- Reload Claude Code
- Check `.claude-plugin/plugin.json` exists

### Hooks Not Triggering
- Ensure `.sh` files executable: `chmod +x plugins/cc10x/hooks/*.sh`
- Validate `hooks/hooks.json` syntax

### Agents Not Activating
- Commands automatically delegate to agents
- Check agent files exist in `agents/` directory

## License

MIT License - See LICENSE file

---

**CC10x v3.0** - Professional AI Development Assistant

Built for Claude Code | Production Ready | Open Source
