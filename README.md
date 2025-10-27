# cc10x v3.0 - Intelligent AI Orchestration

**Professional Claude Code plugin with intelligent orchestration, specialized agents, and progressive skills**

[![Version](https://img.shields.io/badge/version-3.0.0-green)](https://github.com/romiluz13/cc10x)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://github.com/romiluz13/cc10x)

---

## What is CC10x?

An intelligent Claude Code plugin with **auto-loaded orchestrator** that coordinates 12 specialized agents + 21 progressive skills for systematic software development:

- **Code Review** - 5 parallel AI agents (security, quality, performance, UX, accessibility)
- **Feature Planning** - Comprehensive PRDs with risk analysis and architecture decisions
- **TDD Implementation** - Strict test-driven development with quality enforcement
- **LOG FIRST Debugging** - Systematic investigation over guessing

**Intelligent Orchestration:** Detects intent, assesses complexity, routes dynamically

**Progressive Loading:** Workflows load on-demand (50-75% token savings)

**Complexity Gate:** Honestly recommends manual when better (prevents waste)

**"What Could Go Wrong":** 7-dimension risk analysis integrated

---

## Installation

```bash
# Add marketplace
/plugin marketplace add romiluz13/cc10x

# Install plugin
/plugin install cc10x@cc10x

# Verify
/plugin  # Should show: cc10x v3.0.0
```

---

## Quick Start

**Natural language invocation:**

```
"review my auth code for security vulnerabilities"
"plan a user authentication feature"
"build a todo app with React"
"debug why login returns 401"
```

The orchestrator automatically detects your intent, assesses complexity, and executes the appropriate workflow.

---

## Architecture

```
User: "review my auth code"
    ↓ (natural language, no slash command)
    ↓
cc10x-orchestrator SKILL (220 lines)
    ↓ (detects: REVIEW workflow)
    ↓
Loads: workflows/review.md (400 lines)
    ↓ (explicit agent invocation)
    ↓
Invokes 5 Agents in Parallel:
    ├─→ security-reviewer → loads risk-analysis, security-patterns
    ├─→ quality-reviewer → loads code-generation skill
    ├─→ performance-analyzer → loads performance-patterns
    ├─→ ux-reviewer → loads ux-patterns
    └─→ accessibility-reviewer → loads accessibility-patterns
    ↓
Results compiled → returned to user
```

**Pure skills-based:** No commands, just skills coordinating agents

**Progressive:** Workflows load on-demand (only what's needed)

**Honest:** 3-20x MORE tokens than manual, use for complex features (4-5 complexity)

---

## The 4 Workflows

### 1. REVIEW (Always Worth It)

**Use:** Before every PR, any complexity

**What it does:**
- Invokes 5 specialized reviewer agents in parallel
- Security: SQL injection, XSS, auth bypasses
- Quality: Code smells, SOLID violations
- Performance: N+1 queries, memory leaks
- UX: Error messages, loading states
- Accessibility: WCAG violations, keyboard nav

**Token cost:** ~12k tokens  
**Time:** 3-7 minutes  
**Value:** One prevented security breach >> all tokens ever used

### 2. PLANNING (Complexity 4-5)

**Use:** Complex features (500+ lines, 7+ files, architecture decisions)  
**Skip:** Simple features (using libraries, obvious implementations)

**What it does:**
- Requirements analysis with user stories
- Architecture design with technology decisions
- 7-dimension risk assessment
- Testing strategy (>80% coverage goals)
- File manifest with estimated LOC
- Deployment and rollback strategies

**Token cost:** ~25k tokens  
**Worth it:** Prevents costly architecture mistakes

### 3. BUILDING (TDD Enforced)

**Use:** Complexity 4-5, want strict test-driven development  
**Skip:** Simple features (manual is 16x cheaper)

**What it does:**
- Strict TDD: RED → GREEN → REFACTOR
- Risk analysis before each increment
- Mandatory user test verification (prevents false success reports)
- >80% test coverage enforced

**Token cost:** ~30k tokens  
**Important:** You MUST manually verify tests pass

### 4. DEBUGGING (LOG FIRST)

**Use:** Complex bugs where root cause is unclear  
**Skip:** Obvious fixes (typos, syntax errors)

**What it does:**
- Add strategic logging (see actual data, don't guess)
- Reproduce with logging
- Analyze logs systematically
- Form hypothesis based on evidence
- Implement minimal fix
- Verify and clean up logging

**Token cost:** ~15k tokens  
**Value:** Saves hours of random guessing

---

## When to Use cc10x

### ✅ Always Use REVIEW
- Before every PR
- Security audits
- Any complexity
- **One prevented breach >> all tokens**

### ✅ Use PLANNING/BUILDING For:
- **Complexity 4-5** (500+ lines, 7+ files, novel patterns)
- High-risk domains (auth, payments, data integrity)
- Architecture decisions needed
- Team coordination required

**Examples:**
- Real-time notifications (WebSockets)
- Multi-tenancy with data isolation
- Payment processing (Stripe integration)
- Complex state management

### ❌ Skip cc10x For:
- **Complexity 1-2** (simple features using libraries)
- Obvious implementations
- Prototypes/MVPs
- Emergencies (production down)

**cc10x will honestly tell you to skip if manual is better!**

---

## Complexity Examples

**Simple (1-2): Skip cc10x**
- Add rate limiting using express-rate-limit
- Form validation with Zod
- CSV export with csv-parser
- **Manual is 16x cheaper and often better**

**Moderate (3): Maybe**
- User registration (4-6 files, standard patterns)
- Pagination with caching
- Search functionality

**Complex (4-5): Use cc10x**
- Authentication system (JWT + refresh, 10+ files)
- Payment integration (Stripe webhooks, 12+ files)
- Real-time chat (WebSocket + persistence, 14+ files)
- RBAC with middleware (10+ files)

---

## Progressive Loading

**Token efficiency through on-demand workflow loading:**

- **Initial load:** 3.5k tokens (orchestrator + agent/skill metadata)
- **Workflow:** +3-6k tokens (only requested workflow)
- **Agents:** +3k tokens (only invoked agents)
- **Skills:** +2-5k tokens (only needed sections)

**Total:** ~12k tokens for review (vs 10k monolithic = 20% savings)

**Key advantage:** Workflows you don't use aren't loaded

---

## THE FOCUS RULE

**Enforced gates prevent workflow creep:**

1. **Complexity gate:** Warns if feature is too simple, offers to skip
2. **Scope gate:** Only executes requested workflow (no auto-chaining)
3. **User confirmation:** Asks permission before expanding scope

**Example:**
```
You: "build todo app"
→ cc10x: "This is SIMPLE (2/5). Manual is 16x cheaper. Continue? (yes/no)"
→ You: "no"
→ cc10x: "Smart choice! Here's quick guidance..." (exits, saves 80k tokens)
```

---

## Honest Positioning

**cc10x costs 3-20x MORE tokens than manual implementation.**

**Why?**
- Systematic multi-phase analysis
- Multiple specialized agents
- Comprehensive risk assessment
- Complete documentation

**Worth it when:**
- Complexity 4-5 (one prevented mistake >> token cost)
- High-risk domains (security critical)
- Review workflow (ALWAYS - prevents breaches)

**Not worth it when:**
- Complexity 1-2 (manual faster and cheaper)
- Obvious implementations (follow library docs)
- Prototypes (iterate fast first)

**Use the right tool for the job.**

---

## Quality Enforcement

**PostToolUse Hook (Automatic):**
- Validates file size after every Write/Edit
- Warns if >500 lines
- Provides split suggestions

**Agent Enforcement:**
- No placeholders or TODOs
- Production-ready code only
- Comprehensive error handling
- >80% test coverage target

---

## Documentation

- **Quick Start:** [QUICK-START.md](QUICK-START.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **License:** [LICENSE](LICENSE)

---

## Support

- **Issues:** https://github.com/romiluz13/cc10x/issues
- **Repository:** https://github.com/romiluz13/cc10x

---

## License

MIT © Rom Iluz

---

**Start with code review - the killer feature that's always worth it!**

```
"review my code for security issues"
```
