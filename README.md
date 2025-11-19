# cc10x - Claude Code Orchestrator

> **Orchestration plugin for Claude Code with 5 workflows: review, plan, build, debug, validate.**

cc10x provides structured workflows that coordinate 24 domain skills, 5 workflow skills, and 9 subagents to deliver consistent, production-grade code.

## What cc10x Provides

cc10x provides structured workflows for Claude Code:

- **Systematic workflows** that enforce TDD, security checks, and quality gates
- **24 domain skills** that activate when needed
- **5 workflow skills** for orchestration and workflow management
- **9 specialized subagents** working in parallel contexts
- **Evidence-first verification** that requires proof before completion
- **Memory integration** that learns from your patterns

---

## What Makes cc10x Different

### 🎯 **Orchestrator-First Architecture**

**The cc10x-orchestrator is the MANDATORY entry point for all workflows**:

- **Single Entry Point**: All workflows MUST be activated through the orchestrator, not directly
- **Automatic Activation**: Orchestrator activates automatically on any user request (review, plan, build, debug, validate)
- **Centralized Coordination**: Orchestrator coordinates skill loading, subagent invocation, and validation
- **Validation Enforcement**: All validation mechanisms (Skills Inventory Check, Subagents Inventory Check, Phase Checklists) only work when orchestrator runs

**Result**: Consistent, validated execution across all workflows.

### 🎯 **Functionality-First Approach**

**Every workflow starts with understanding functionality**:

- **Phase 0: Functionality Analysis** (MANDATORY FIRST STEP)
  - Understands user flows, admin flows, system flows
  - Verifies functionality works before applying specialized checks
  - Extracts acceptance criteria and requirements
  - Documents flows and integration points

**Result**: Workflows understand what needs to be done before doing it.

### 🎯 **Deterministic Workflow Selection**

cc10x uses explicit keyword mapping to select the right workflow:

```bash
"Review this auth module"     → REVIEW workflow ✅
"Plan payment processing"     → PLAN workflow ✅
"Build user dashboard"        → BUILD workflow ✅
"Debug memory leak"           → DEBUG workflow ✅
"Validate implementation"     → VALIDATION workflow ✅
```

**Result**: Correct workflow selection based on keywords.

### 🎯 **Automatic Context Preset Detection**

cc10x automatically detects task type and loads appropriate context:

- **Frontend tasks**: Detects React/Vue components → loads frontend preset
- **Backend tasks**: Detects API/server code → loads backend preset
- **Full-stack tasks**: Detects both → loads app preset

**Result**: Right context loaded automatically, no manual configuration needed.

### 🧠 **Memory Integration**

cc10x learns from your patterns:

- **Complexity patterns**: Similar tasks? It remembers how you scored them
- **Failure modes**: Common bugs? It remembers the fixes
- **Component orders**: Dependency patterns? It builds in the right sequence
- **User preferences**: Your review depth, test coverage targets, build approach

**Result**: Workflows improve with usage.

### 🔍 **Evidence-First Verification**

No "trust me, it works" claims. cc10x requires proof:

```bash
✅ Tests run → exit code 0
✅ Coverage >80% → verified
✅ Build succeeds → confirmed
✅ Integration tests pass → validated
```

**Result**: Code completion requires evidence.

### 🎨 **Progressive Disclosure Architecture**

Skills load in 3 levels—exactly when needed:

- **Level 1**: Metadata (always loaded) - ~100 tokens
- **Level 2**: Instructions (when triggered) - ~5k tokens
- **Level 3**: Resources (on-demand) - unlimited

**Result**: Skills load only when needed.

---

## 🚀 Quick Start

### Installation

1. Add the marketplace

```bash
/plugin marketplace add romiluz13/cc10x
```

2. Install the plugin

```bash
/plugin install cc10x@romiluz13
```

3. Restart Claude Code

### Your First Workflow

Just ask naturally - cc10x detects intent:

```
Review the uncommitted changes
```

**cc10x executes**:

1. **Phase 0**: Functionality Analysis → Understands what the code does
2. Detects `review` intent → triggers REVIEW workflow
3. Loads security, quality, performance, UX, accessibility skills (parallel)
4. Delegates to 3 specialized subagents (risk-security, performance-quality, ux-accessibility) in parallel
5. Synthesizes findings with severity levels
6. Provides file:line citations and remediation steps

**Output**: Security audit with findings and fixes.

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

### 2. **PLAN** - Feature Planning

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

## The Architecture

### 24 Domain Skills

Domain experts that activate automatically:

**Code Quality & Security**:

- `code-review-patterns` - Security, quality, and performance analysis (consolidates security-patterns, code-quality-patterns, performance-patterns)
- OWASP Top 10, injection prevention, SOLID principles, complexity metrics, bottleneck identification

**Design & Planning**:

- `planning-patterns` - Requirements analysis and feature planning (consolidates requirements-analysis, feature-planning)
- `architecture-patterns` - System design, component boundaries, API design, integration patterns
- `risk-analysis` - 7-stage risk framework with mitigation strategies

**User Experience**:

- `frontend-patterns` - UX, UI design, and accessibility (consolidates ux-patterns, ui-design, accessibility-patterns)
- Loading states, error handling, visual hierarchy, WCAG compliance, keyboard navigation

**Implementation**:

- `test-driven-development` - RED → GREEN → REFACTOR discipline
- `component-design-patterns` - Composition, reusability, API design
- `deployment-patterns` - 3-level rollback, staged rollouts, monitoring

**Operations**:

- `debugging-patterns` - Systematic debugging, log analysis, root cause analysis (consolidates systematic-debugging, log-analysis-patterns, root-cause-analysis)
- LOG FIRST methodology, structured logging, evidence-based investigation

### 5 Workflow Skills

Orchestration and workflow management:

- `cc10x-orchestrator` - Primary orchestrator, intent detection, workflow coordination
- `review-workflow` - Review workflow coordination
- `planning-workflow` - Planning workflow coordination
- `build-workflow` - Build workflow coordination
- `debug-workflow` - Debug workflow coordination

### 5 Specialized Subagents

Separate context windows, focused expertise:

**Review Subagents**:

- `code-reviewer` - Comprehensive review covering security, quality, performance, UX, and accessibility (consolidates analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility)

**Plan Subagents**:

- `planner` - Comprehensive planning covering architecture, risks, API design, component design, testing, and deployment (consolidates planning-architecture-risk, planning-design-deployment)

**Build Subagents**:

- `component-builder` - TDD implementation, component building
- `code-reviewer` - Quality and security verification
- `integration-verifier` - Integration testing, evidence-based completion

**Debug Subagents**:

- `bug-investigator` - Log analysis, root cause identification, fix implementation

---

## 💎 Key Features

### ✅ **Functionality-First Mandate**

**Every workflow enforces Phase 0: Functionality Analysis FIRST**:

- Understands what functionality needs to be built/reviewed/debugged
- Documents user flows, admin flows, system flows
- Verifies functionality works before applying specialized checks
- Extracts acceptance criteria and requirements

**Prevents**: Building/reviewing/debugging without understanding what needs to be done.

### ✅ **Complexity Gating**

cc10x assesses task complexity (1-5 scale) after functionality analysis:

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

### ✅ **Web Fetch Caching**

External documentation is cached with TTL-based expiration:

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
2. Loads code-review-patterns skill (consolidates security-patterns, code-quality-patterns, performance-patterns)
3. Delegates to code-reviewer subagent (consolidates analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility)
4. Scans payment code for OWASP Top 10 issues, performance bottlenecks, and code quality issues
5. Returns findings with severity levels and fixes

**Time**: 3 minutes  
**Output**: Found 2 critical SQL injection risks before production

### Example 2: Complete Feature Implementation

```bash
"Build user authentication with JWT tokens and refresh tokens"
```

**cc10x executes**:

1. **Phase 0**: Functionality Analysis → Understands auth requirements and flows
2. Detects `build` intent → BUILD workflow
3. Assesses complexity: 4 (multi-file, security-critical)
4. Breaks into components: UserModel → AuthService → LoginComponent → AuthGuard
5. For each component: RED → GREEN → REFACTOR with tests (sequential per component)
6. Independent components run in parallel
7. Code review by code-reviewer subagent (after builder)
8. Integration verification by integration-verifier subagent (after reviewer)
9. Evidence verification: Tests pass, coverage >80%, build succeeds

**Time**: 45 minutes  
**Output**: Production-ready auth system with 95% test coverage

### Example 3: Production Bug Investigation

```bash
"Debug the memory leak in our data pipeline"
```

**cc10x executes**:

1. **Phase 0**: Functionality Analysis → Understands expected vs observed behavior
2. Detects `debug` intent → DEBUG workflow
3. Loads debugging-patterns skill (consolidates systematic-debugging, log-analysis-patterns, root-cause-analysis)
4. Delegates to bug-investigator subagent
5. LOG FIRST: Gathers logs, metrics, stack traces
6. Root cause: Event listener not cleaned up
7. Targeted fix: Added cleanup in useEffect return
8. Regression test: Added test to prevent future leaks
9. Verification: Memory leak resolved, tests pass

**Time**: 15 minutes  
**Output**: Memory leak fixed with prevention strategy

---

## When to Use cc10x

### Use cc10x for:

- **Complex features** (complexity 4-5) that need systematic planning
- **Security-critical code** that requires thorough review
- **Production bugs** that need root cause analysis
- **Large codebases** where quality gates matter
- **Team projects** where consistency is critical

### Not needed for:

- **Trivial changes** (complexity 1-2) - cc10x will recommend direct implementation
- **Quick experiments** - Use Claude Code directly
- **One-off scripts** - Overkill for simple tasks

---

## 🏗️ Architecture Overview

```
cc10x Orchestrator
├── Phase 0: Functionality Analysis (MANDATORY FIRST)
│   ├── Understand user/admin/system flows
│   ├── Verify functionality works
│   └── Extract acceptance criteria
├── Context Preset Detection (automatic)
│   ├── Detect task type (frontend/backend/app)
│   └── Load appropriate context preset
├── Intent Detection (explicit keyword mapping)
├── Complexity Assessment (1-5 scale)
├── Workflow Selection (review/plan/build/debug/validate)
│
├── REVIEW Workflow
│   ├── Phase 0: Functionality Analysis ✅
│   ├── Load: code-review-patterns, frontend-patterns (parallel)
│   ├── Delegate: code-reviewer → integration-verifier (if integration changes detected)
│   └── Output: Findings with severity, file:line citations, remediation steps
│
├── PLAN Workflow
│   ├── Phase 0: Functionality Analysis ✅
│   ├── Load: planning-patterns, architecture-patterns, risk-analysis (parallel)
│   ├── Delegate: planner
│   └── Output: Architecture design, risk register, implementation roadmap
│
├── BUILD Workflow
│   ├── Phase 0: Functionality Analysis ✅
│   ├── Load: test-driven-development, code-review-patterns, verification-before-completion (parallel)
│   ├── Delegate: component-builder → code-reviewer → integration-verifier (sequential per component)
│   └── Output: Components with tests, verification summary
│
├── DEBUG Workflow
│   ├── Phase 0: Functionality Analysis ✅
│   ├── Load: debugging-patterns, code-review-patterns (parallel)
│   ├── Delegate: bug-investigator → code-reviewer → integration-verifier (sequential per bug)
│   └── Output: Root cause, fix, regression test
│
└── VALIDATE Workflow
    ├── Phase 0: Functionality Analysis ✅
    ├── Load: planning-patterns, verification-before-completion (parallel)
    └── Output: Alignment matrix, coverage analysis, documentation freshness
```

---

## 🚦 Getting Started Checklist

- [ ] Add marketplace: `/plugin marketplace add romiluz13/cc10x`
- [ ] Install cc10x: `/plugin install cc10x@romiluz13`
- [ ] Restart Claude Code
- [ ] Try REVIEW: `"Review this code for security issues"`
- [ ] Try PLAN: `"Plan a user authentication feature"`
- [ ] Try BUILD: `"Build a user profile component"`
- [ ] Try DEBUG: `"Debug this error: [paste error]"`
- [ ] Try VALIDATE: `"Validate this implementation matches the plan"`

**That's it. You're ready to use cc10x workflows.**

---

## Workflow Comparison

### Without cc10x:

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

### With cc10x:

```bash
You: "Review this code"
cc10x: *triggers REVIEW workflow*
  → Loads code-review-patterns and frontend-patterns skills
  → Delegates to code-reviewer subagent (consolidated review expertise)
  → Synthesizes findings with severity levels
  → Provides file:line citations and fixes
```

**Output**: Security audit with findings and fixes.

---

## Getting Started

1. **Start Simple**: Use REVIEW workflow for code audits
2. **Scale Up**: Use PLAN workflow for new features
3. **Go Deep**: Use BUILD workflow for TDD implementation
4. **Master It**: Use DEBUG workflow for systematic investigation
5. **Verify**: Use VALIDATE workflow for consistency checks

---

## Documentation

- **Skills Reference**: See `plugins/cc10x/skills/` for individual skill docs
- **Subagents Reference**: See `plugins/cc10x/subagents/` for subagent specs
- **Workflow Details**: See `plugins/cc10x/skills/cc10x-orchestrator/workflows/`

---

## License

MIT License - Use freely, modify as needed.

---

## Contributing

- ⭐ Star the repository
- 🐛 Report issues
- 💡 Suggest improvements
- 🤝 Contribute skills or workflows

---

## Installation

```bash
# Step 1: Add the marketplace
/plugin marketplace add romiluz13/cc10x

# Step 2: Install the plugin
/plugin install cc10x@romiluz13
```

---

_cc10x v4.9.0 | Production Ready | Built for Claude Code_
