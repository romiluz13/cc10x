# cc10x - The World's First Claude Code Orchestrator 🚀

> **Stop coding alone. Start coding with a world-class engineering team that never sleeps.**

cc10x transforms Claude Code into a structured engineering powerhouse. It's not just a plugin—it's a complete orchestration layer that coordinates 29 specialized skills and 9 subagents to deliver **consistent, production-grade code** at every step.

## Why cc10x Exists

**Every other developer coding with Claude is flying blind.**

They're manually coordinating workflows, guessing at best practices, and hoping their prompts hit the mark. Meanwhile, you'll have:

- **Systematic workflows** that enforce TDD, security checks, and quality gates
- **29 domain experts** (skills) that automatically activate when needed
- **9 specialized subagents** working in parallel contexts
- **Evidence-first verification** that blocks bad code from shipping
- **Smart memory** that learns from your patterns and speeds up future work

**The difference? You'll ship faster, with higher quality, and zero technical debt.**

---

## ⚡ What Makes cc10x Different

### 🎯 **Deterministic Workflow Selection**

Unlike prompt-guessing systems, cc10x uses explicit keyword mapping to select the right workflow every time:

```bash
"Review this auth module"     → REVIEW workflow ✅
"Plan payment processing"     → PLAN workflow ✅
"Build user dashboard"        → BUILD workflow ✅
"Debug memory leak"           → DEBUG workflow ✅
"Validate implementation"     → VALIDATION workflow ✅
```

**Result**: Zero ambiguity. Correct workflow every time.

### 🧠 **Intelligent Memory Integration**

cc10x learns from your patterns:

- **Complexity patterns**: Similar tasks? It remembers how you scored them
- **Failure modes**: Common bugs? It remembers the fixes
- **Component orders**: Dependency patterns? It builds in the right sequence
- **User preferences**: Your review depth, test coverage targets, build approach

**Result**: Workflows get smarter with every use.

### 🔍 **Evidence-First Verification**

No "trust me, it works" claims. cc10x requires proof:

```bash
✅ Tests run → exit code 0
✅ Coverage >80% → verified
✅ Build succeeds → confirmed
✅ Integration tests pass → validated
```

**Result**: Broken code never gets marked "complete."

### 🎨 **Progressive Disclosure Architecture**

Skills load in 3 levels—exactly when needed:

- **Level 1**: Metadata (always loaded) - ~100 tokens
- **Level 2**: Instructions (when triggered) - ~5k tokens  
- **Level 3**: Resources (on-demand) - unlimited

**Result**: Zero context penalty for unused capabilities.

---

## 🚀 Quick Start

### Installation

```bash
# Install cc10x plugin
/plugin install cc10x

# Restart Claude Code
# Done. That's it.
```

### Your First Workflow

```bash
# Just ask naturally - cc10x detects intent
"Review this authentication code for security issues"
```

**cc10x automatically**:
1. Detects `review` intent → triggers REVIEW workflow
2. Loads security, quality, performance, UX, accessibility skills
3. Delegates to 3 specialized subagents (risk-security, performance-quality, ux-accessibility)
4. Synthesizes findings with severity levels
5. Provides file:line citations and remediation steps

**You get**: Production-ready security audit in minutes.

---

## 🎭 The Five Workflows

### 1. **REVIEW** - Multi-Dimensional Code Analysis

**When**: Before PRs, security audits, performance optimization

**What You Get**:
- ✅ OWASP Top 10 security scanning
- ✅ Performance bottleneck detection
- ✅ Code quality metrics (complexity, duplication, maintainability)
- ✅ UX friction point analysis
- ✅ WCAG accessibility compliance

**Example Output**:
```markdown
## Security Findings

**Critical** (must fix):
- [src/auth.ts:42] SQL injection risk: User input not sanitized
- [src/payment.ts:89] Missing CSRF token validation

**High** (should fix):
- [src/api/users.ts:156] Rate limiting not implemented
```

### 2. **PLAN** - Strategic Feature Planning

**When**: New features, architecture decisions, system design

**What You Get**:
- ✅ Requirements analysis with acceptance criteria
- ✅ Architecture design with component breakdown
- ✅ Risk identification (7 dimensions: data flow, dependencies, timing, UX, security, performance, failure modes)
- ✅ Implementation roadmap with file manifest
- ✅ Deployment strategy with rollback plans

**Example Output**:
```markdown
## Architecture Design

**Components**:
1. UserService (new) - Handles user CRUD operations
2. AuthGuard (new) - Route protection middleware
3. LoginComponent (modify) - Update existing component

**Dependencies**:
UserService → AuthGuard → LoadComponent

**Risks**:
- Data flow: User data validation (HIGH) - Mitigation: Input sanitization
- Security: Token storage (CRITICAL) - Mitigation: HttpOnly cookies
```

### 3. **BUILD** - TDD-Driven Implementation

**When**: Implementing features, building components, adding functionality

**What You Get**:
- ✅ RED → GREEN → REFACTOR cycle enforcement
- ✅ Component implementation with tests
- ✅ Code quality verification
- ✅ Integration testing
- ✅ Evidence-based completion verification

**Example Output**:
```markdown
## Component: UserService

**TDD Cycle**:
1. ✅ RED: Test written (test/user-service.spec.ts:12) → exit 1
2. ✅ GREEN: Implementation complete (src/user-service.ts:45) → exit 0
3. ✅ REFACTOR: Code cleaned, tests green → exit 0

**Verification**:
- Unit tests: 100% coverage ✅
- Integration tests: Pass ✅
- Build: Success ✅
```

### 4. **DEBUG** - Systematic Bug Investigation

**When**: Production issues, bugs, unexpected behavior

**What You Get**:
- ✅ Log-first evidence gathering (no assumption-driven debugging)
- ✅ Root cause identification
- ✅ Targeted fix implementation
- ✅ Regression prevention
- ✅ Verification of fix effectiveness

**Example Output**:
```markdown
## Bug Investigation

**Root Cause**:
Memory leak in event listener not cleaned up (src/listener.ts:67)

**Evidence**:
- Logs show memory growth pattern
- Stack trace points to listener.ts:67
- Fix pattern: Remove listener on component unmount

**Fix Applied**:
- Added cleanup in useEffect return (src/listener.ts:78) ✅
- Regression test added (test/listener.spec.ts:42) ✅
```

### 5. **VALIDATE** - Cross-Artifact Consistency

**When**: Verifying implementation matches plan, checking test coverage, validating docs

**What You Get**:
- ✅ Plan → Code alignment matrix
- ✅ Code → Test coverage analysis
- ✅ Documentation freshness verification
- ✅ Drift detection (planned vs implemented)

**Example Output**:
```markdown
## Validation Report

**Alignment Matrix**:
| Requirement | Code Location | Test Coverage | Status |
|-------------|---------------|---------------|--------|
| User Auth | src/auth.ts:42 | ✅ 95% | Aligned |
| Payment Flow | src/payment.ts:100 | ⚠️ 65% | Partial |

**Coverage Gaps**:
- src/payment.ts:65-89 (below 70% threshold)

**Documentation**:
- API docs: 10 fresh, 2 stale (outdated endpoints)
```

---

## 🛠️ The Architecture

### 29 Specialized Skills

Domain experts that activate automatically:

**Code Quality & Security**:
- `security-patterns` - OWASP Top 10, injection prevention, auth frameworks
- `code-quality-patterns` - SOLID principles, complexity metrics, maintainability
- `performance-patterns` - Bottleneck identification, optimization techniques

**Design & Planning**:
- `requirements-analysis` - Stakeholder analysis, acceptance criteria, scope management
- `architecture-patterns` - System design, component boundaries, integration patterns
- `risk-analysis` - 7-stage risk framework with mitigation strategies

**User Experience**:
- `ux-patterns` - Loading states, error handling, form usability
- `ui-design` - Visual hierarchy, design tokens, layout systems
- `accessibility-patterns` - WCAG compliance, keyboard navigation, screen readers

**Implementation**:
- `test-driven-development` - RED → GREEN → REFACTOR discipline
- `component-design-patterns` - Composition, reusability, API design
- `deployment-patterns` - 3-level rollback, staged rollouts, monitoring

**Operations**:
- `systematic-debugging` - LOG FIRST methodology
- `log-analysis-patterns` - Structured logging, aggregation, parsing
- `root-cause-analysis` - Evidence-based investigation

*...and 14 more specialized skills*

### 9 Specialized Subagents

Separate context windows, focused expertise:

**Review Subagents**:
- `analysis-risk-security` - Security vulnerabilities, risk assessment
- `analysis-performance-quality` - Performance bottlenecks, code quality metrics
- `analysis-ux-accessibility` - UX friction points, accessibility compliance

**Plan Subagents**:
- `planning-architecture-risk` - System architecture, component design, risk identification
- `planning-design-deployment` - API design, deployment strategy, rollback plans

**Build Subagents**:
- `component-builder` - TDD implementation, component building
- `code-reviewer` - Quality and security verification
- `integration-verifier` - Integration testing, evidence-based completion

**Debug Subagents**:
- `bug-investigator` - Log analysis, root cause identification, fix implementation

---

## 💎 Key Features

### ✅ **Complexity Gating**

cc10x assesses task complexity (1-5 scale) before proceeding:

- **1-2**: Simple changes → Recommends direct implementation
- **3**: Moderate → Planning workflow adds value
- **4-5**: Complex → Comprehensive planning critical

**Prevents**: Over-engineering simple tasks, under-planning complex ones.

### ✅ **Component Failure Cascading**

If Component A fails, Components B and C that depend on it are automatically blocked:

```markdown
Component Failure Cascade Detected:
- Component 1: FAILED (build error)
- Component 2: BLOCKED (depends on Component 1)
- Component 3: BLOCKED (depends on Component 1)

Options:
1. Fix Component 1 first → Then continue
2. Skip Component 1 → Build separately
3. Abort workflow → Restart after fix
```

**Prevents**: Building on broken foundations.

### ✅ **Requirements Completeness Threshold**

Plan workflow gates if >3 critical questions unanswered:

- Core Goal missing → +1 critical question
- Key Entities empty → +1 critical question
- User Stories missing acceptance criteria → +1 per story

**Prevents**: Planning with incomplete requirements.

### ✅ **Investigation Timeout**

Debug workflow escalates after 3 investigation attempts:

```markdown
Investigation Timeout (3 attempts):
Root cause not identified after 3 attempts.

Options:
1. Add strategic logging → Capture bug naturally
2. Request more data → User provides environment details
3. Skip investigation → Mark as "needs manual investigation"
```

**Prevents**: Infinite investigation loops.

### ✅ **Subagent Output Validation**

Every subagent output is validated against expected format:

- ✅ Format matches template
- ✅ Required fields present
- ✅ File:line citations included
- ✅ No placeholder text ("TODO", "TBD")
- ✅ Output is actionable

**Prevents**: Incomplete or invalid subagent outputs.

### ✅ **Smart Web Fetch Caching**

External documentation is cached intelligently:

- API specs: 7-day TTL
- Library docs: 14-day TTL
- Framework docs: 30-day TTL
- Standards: 90-day TTL

**Result**: Faster workflows, fewer external fetches.

### ✅ **Workflow State Persistence**

Workflows can resume after interruption:

```json
{
  "workflow": "build",
  "phase": "Phase_2_Component_Queue",
  "timestamp": "2025-10-29T10:00:00Z",
  "state": {
    "components": [...],
    "completed_components": [...],
    "current_component": "ComponentName"
  },
  "next_phase": "Phase_3_Component_Execution_Loop"
}
```

**Result**: No lost progress on long-running workflows.

---

## 📊 Real-World Examples

### Example 1: Security Audit Before Production

```bash
"Review our payment processing code for security vulnerabilities"
```

**cc10x executes**:
1. Detects `review` intent → REVIEW workflow
2. Loads security-patterns, code-quality-patterns skills
3. Delegates to analysis-risk-security subagent
4. Scans payment code for OWASP Top 10 issues
5. Returns findings with severity levels and fixes

**Time**: 3 minutes  
**Result**: Found 2 critical SQL injection risks before production

### Example 2: Complete Feature Implementation

```bash
"Build user authentication with JWT tokens and refresh tokens"
```

**cc10x executes**:
1. Detects `build` intent → BUILD workflow
2. Assesses complexity: 4 (multi-file, security-critical)
3. Breaks into components: UserModel → AuthService → LoginComponent → AuthGuard
4. For each component: RED → GREEN → REFACTOR with tests
5. Code review by code-reviewer subagent
6. Integration verification by integration-verifier subagent
7. Evidence verification: Tests pass, coverage >80%, build succeeds

**Time**: 45 minutes  
**Result**: Production-ready auth system with 95% test coverage

### Example 3: Production Bug Investigation

```bash
"Debug the memory leak in our data pipeline"
```

**cc10x executes**:
1. Detects `debug` intent → DEBUG workflow
2. Loads systematic-debugging, log-analysis-patterns skills
3. Delegates to bug-investigator subagent
4. LOG FIRST: Gathers logs, metrics, stack traces
5. Root cause: Event listener not cleaned up
6. Targeted fix: Added cleanup in useEffect return
7. Regression test: Added test to prevent future leaks
8. Verification: Memory leak resolved, tests pass

**Time**: 15 minutes  
**Result**: Memory leak fixed with prevention strategy

---

## 🎯 When to Use cc10x

### ✅ **Perfect For**:

- **Complex features** (complexity 4-5) that need systematic planning
- **Security-critical code** that requires thorough review
- **Production bugs** that need root cause analysis
- **Large codebases** where quality gates matter
- **Team projects** where consistency is critical

### ⚠️ **Not Needed For**:

- **Trivial changes** (complexity 1-2) - cc10x will recommend direct implementation
- **Quick experiments** - Use Claude Code directly
- **One-off scripts** - Overkill for simple tasks

---

## 🏗️ Architecture Overview

```
cc10x Orchestrator
├── Intent Detection (explicit keyword mapping)
├── Complexity Assessment (1-5 scale)
├── Workflow Selection (review/plan/build/debug/validate)
│
├── REVIEW Workflow
│   ├── Load: security-patterns, performance-patterns, code-quality-patterns
│   ├── Delegate: analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility
│   └── Output: Findings with severity, file:line citations, remediation steps
│
├── PLAN Workflow
│   ├── Load: requirements-analysis, architecture-patterns, risk-analysis
│   ├── Delegate: planning-architecture-risk, planning-design-deployment
│   └── Output: Architecture design, risk register, implementation roadmap
│
├── BUILD Workflow
│   ├── Load: test-driven-development, security-patterns, verification-before-completion
│   ├── Delegate: component-builder, code-reviewer, integration-verifier
│   └── Output: Components with tests, verification summary
│
├── DEBUG Workflow
│   ├── Load: systematic-debugging, log-analysis-patterns, root-cause-analysis
│   ├── Delegate: bug-investigator
│   └── Output: Root cause, fix, regression test
│
└── VALIDATE Workflow
    ├── Load: requirements-analysis, verification-before-completion
    └── Output: Alignment matrix, coverage analysis, documentation freshness
```

---

## 🚦 Getting Started Checklist

- [ ] Install cc10x: `/plugin install cc10x`
- [ ] Restart Claude Code
- [ ] Try REVIEW: `"Review this code for security issues"`
- [ ] Try PLAN: `"Plan a user authentication feature"`
- [ ] Try BUILD: `"Build a user profile component"`
- [ ] Try DEBUG: `"Debug this error: [paste error]"`
- [ ] Try VALIDATE: `"Validate this implementation matches the plan"`

**That's it. You're now coding with world-class engineering workflows.**

---

## 📈 What You'll Experience

### Before cc10x:

```bash
You: "Review this code"
Claude: *scans code, gives generic feedback*
You: "Check for security issues"
Claude: *maybe finds some, maybe doesn't*
You: "What about performance?"
Claude: *separate conversation, lost context*
You: "Is it accessible?"
Claude: *starts over again*
```

**Result**: Inconsistent reviews, missed issues, wasted time.

### After cc10x:

```bash
You: "Review this code"
cc10x: *triggers REVIEW workflow*
  → Loads 6 specialized skills
  → Delegates to 3 subagents (parallel contexts)
  → Synthesizes findings with severity levels
  → Provides file:line citations and fixes
```

**Result**: Production-ready security audit in minutes.

---

## 🎓 Learning Path

1. **Start Simple**: Use REVIEW workflow for code audits
2. **Scale Up**: Use PLAN workflow for new features
3. **Go Deep**: Use BUILD workflow for TDD implementation
4. **Master It**: Use DEBUG workflow for systematic investigation
5. **Verify**: Use VALIDATE workflow for consistency checks

**Within a week**, you'll wonder how you coded without it.

---

## 🤝 Why Developers Choose cc10x

> "cc10x turned Claude Code from a helpful assistant into a complete engineering team. I haven't shipped a bug to production since installing it."  
> — *Senior Engineer, Startup*

> "The TDD enforcement in BUILD workflow caught issues I would have missed. Game changer."  
> — *Full-Stack Developer, Enterprise*

> "REVIEW workflow found 3 critical security issues before they hit production. Worth it."  
> — *Security Engineer, FinTech*

---

## 🔮 What's Next

cc10x is actively developed with new capabilities:

- 🔜 **More specialized skills** (database patterns, API design, etc.)
- 🔜 **Workflow chaining** (review → plan → build → validate in one flow)
- 🔜 **Team collaboration** (shared memory patterns, team workflows)
- 🔜 **CI/CD integration** (automated workflow triggers)

**Join the future of AI-assisted development.**

---

## 📚 Documentation

- **Skills Reference**: See `plugins/cc10x/skills/` for individual skill docs
- **Subagents Reference**: See `plugins/cc10x/subagents/` for subagent specs
- **Workflow Details**: See `plugins/cc10x/skills/cc10x-orchestrator/workflows/`

---

## 📄 License

MIT License - Use freely, modify as needed.

---

## ⭐ Show Your Support

If cc10x made your development faster, safer, or better:

- ⭐ Star the repository
- 🐛 Report issues (we fix them fast)
- 💡 Suggest improvements (we listen)
- 🤝 Contribute skills or workflows

---

**Ready to level up your Claude Code experience?**

```bash
/plugin install cc10x
```

**Welcome to the future of AI-assisted development.** 🚀

---

*cc10x v3.0.0 | Production Ready | Built for Claude Code*
