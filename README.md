# cc10x - Intelligent Development Workflows

A Claude Code plugin that provides systematic development workflows through orchestrated skills and subagents. Automates code review, feature planning, implementation, and debugging with structured, repeatable processes.

## Quick Start

### Installation

Install directly in Claude Code:

```bash
/plugin install cc10x
```

Restart Claude Code to activate the plugin.

### Basic Usage

The orchestrator detects your intent and invokes the appropriate workflow:

```
Review this authentication module for security issues
→ Triggers REVIEW workflow

Plan a payment processing feature
→ Triggers PLAN workflow

Implement user profile management
→ Triggers BUILD workflow

Fix the memory leak in data pipeline
→ Triggers DEBUG workflow
```

---

## Four Core Workflows

### REVIEW - Multi-Dimensional Code Analysis

Systematic code review across security, quality, performance, UX, and accessibility dimensions.

**When to use**:
- Before merging pull requests
- Security audits
- Performance optimization
- UX evaluation
- Accessibility compliance checks

**What it provides**:
- Security vulnerability identification (OWASP Top 10)
- Performance bottleneck detection
- Code quality assessment (complexity, duplication, maintainability)
- UX friction point analysis
- WCAG accessibility compliance check

---

### PLAN - Strategic Feature Planning

Comprehensive planning for features and architecture with requirements analysis, design decisions, and risk assessment.

**When to use**:
- New feature development
- Architecture design
- Technical decision making
- Risk assessment before implementation

**What it provides**:
- Requirements analysis with acceptance criteria
- Architecture design with system context and component breakdown
- Risk identification across 7 dimensions (data flow, dependencies, timing, UX, security, performance, failure modes)
- Implementation roadmap with file manifest and phased approach
- Deployment strategy with rollback plans

---

### BUILD - TDD-Driven Implementation

Test-driven development workflow with component building, code review, and integration verification.

**When to use**:
- Implementing new features
- Building components
- Adding functionality to existing codebase

**What it provides**:
- RED → GREEN → REFACTOR cycle enforcement
- Component implementation with tests
- Code quality verification
- Integration testing
- Evidence-based verification before completion

---

### DEBUG - Systematic Bug Investigation

Log-first debugging methodology for root cause analysis and systematic fixes.

**When to use**:
- Investigating production issues
- Fixing bugs
- Understanding unexpected behavior
- Performance debugging

**What it provides**:
- Log-first evidence gathering (prevents assumption-driven debugging)
- Root cause identification
- Targeted fix implementation
- Regression prevention
- Verification of fix effectiveness

---

## Skills Architecture

The plugin includes 26 specialized skills organized into domains:

### Code Quality & Security
- **security-patterns**: OWASP Top 10, injection prevention, authentication decision frameworks
- **code-quality-patterns**: SOLID principles, complexity metrics, maintainability patterns
- **performance-patterns**: Bottleneck identification, optimization techniques, profiling guidance

### Design & Planning
- **feature-planning**: Requirements gathering, architecture design, implementation roadmaps
- **requirements-analysis**: Stakeholder analysis, acceptance criteria, scope management
- **architecture-patterns**: System design, component boundaries, integration patterns
- **risk-analysis**: 7-stage risk framework (data flow, dependencies, timing, UX, security, performance, failure modes)

### User Experience
- **ux-patterns**: Loading states, error handling, form usability, user flows
- **ui-design**: Visual hierarchy, design tokens, layout systems, state design
- **accessibility-patterns**: WCAG compliance, keyboard navigation, screen reader support

### Implementation
- **test-driven-development**: RED → GREEN → REFACTOR discipline, test patterns
- **code-generation**: SOLID principles, DRY methodology, project conventions
- **component-design-patterns**: Composition, reusability, API design

### Deployment & Operations
- **deployment-patterns**: 3-level rollback (flag/config/code), staged rollouts, monitoring
- **systematic-debugging**: LOG FIRST methodology, evidence-based debugging
- **log-analysis-patterns**: Structured logging, log aggregation, parsing techniques

---

## Subagents Architecture

9 specialized subagents execute workflows:

### Review Workflow
- **analysis-risk-security**: Security vulnerabilities, risk assessment
- **analysis-performance-quality**: Performance bottlenecks, code quality metrics
- **analysis-ux-accessibility**: UX friction points, accessibility compliance

### Plan Workflow
- **planning-architecture-risk**: System architecture, component design, risk identification
- **planning-design-deployment**: API design, deployment strategy, rollback plans

### Build Workflow
- **component-builder**: TDD implementation, component building
- **code-reviewer**: Quality and security verification
- **integration-verifier**: Integration testing, evidence-based completion

### Debug Workflow
- **bug-investigator**: Log analysis, root cause identification, fix implementation

---

## Progressive Disclosure

Skills use 3-level progressive loading:

**Level 1: Metadata** - Skill name and description (always loaded)
```yaml
---
name: security-patterns
description: Identifies OWASP Top 10 vulnerabilities including SQL injection, XSS, authentication bypasses...
---
```

**Level 2: Quick Reference** - Core patterns and decision frameworks (loaded when triggered)
- Decision matrices (JWT vs Sessions vs OAuth, RBAC vs ABAC)
- Before/after examples showing quality differences
- Quick checklists and red flags

**Level 3: Detailed Guide** - Comprehensive patterns and examples (loaded as needed)
- Complete pattern catalog
- Edge case handling
- Integration with other skills

---

## Workflow Invocation

The orchestrator detects intent from natural language:

```
"Review this code for security" → REVIEW workflow
"Plan authentication system" → PLAN workflow
"Build user registration" → BUILD workflow
"Debug login issue" → DEBUG workflow
```

### Complexity Gating

The orchestrator assesses complexity before proceeding:

**Complexity Scale (1-5)**:
- **1-2**: Simple changes - recommends direct implementation
- **3**: Moderate - planning workflow adds value
- **4-5**: Complex - comprehensive planning critical

**Complexity Example**:
```
Task: Add a validation helper function
Complexity: 1 (trivial)
Recommendation: "This is a simple change. Implement directly?"
```

---

## Evidence-Based Verification

All workflows enforce evidence-first completion:

**Before marking complete**:
- Run tests: `npm test` → capture exit code and output
- Check coverage: `npm run coverage` → verify >80%
- Verify build: `npm run build` → confirm success
- Manual testing: Document steps and results

**No success claims without command outputs**

---

## When to Use Each Workflow

### Use REVIEW when:
- Before merging pull requests
- Security-critical code changes
- Performance optimization needed
- UX evaluation required
- Accessibility compliance checking

### Use PLAN when:
- Starting new features (complexity 4-5)
- Making architectural decisions
- Assessing deployment risks
- Coordinating team implementation

### Use BUILD when:
- Implementing planned features
- Building new components
- Adding functionality with tests
- Quality standards enforcement needed

### Use DEBUG when:
- Production issues occurring
- Bugs need systematic investigation
- Root cause analysis required
- Prevention strategies needed

---

## File Structure

```
cc10x/
├── .claude-plugin/
│   └── plugin.json                    # Plugin configuration
├── skills/                            # 26 specialized skills
│   ├── cc10x-orchestrator/           # Main orchestrator
│   ├── security-patterns/            # Security guidance
│   ├── feature-planning/             # Planning templates
│   ├── test-driven-development/      # TDD patterns
│   └── ...                           # Other domain skills
├── subagents/                         # 9 workflow subagents
│   ├── analysis-risk-security/       # Security analysis
│   ├── component-builder/            # TDD implementation
│   ├── bug-investigator/             # Debugging
│   └── ...                           # Other subagents
├── hooks/                             # Lifecycle hooks
│   └── session-start.sh              # Session initialization
└── scripts/                           # Validation scripts
    └── validate-skill-references.sh
```

---

## Verification

Check installation success:

```bash
# List installed plugins
/plugins list

# Verify cc10x appears

# Test workflow invocation
"Review this code for quality"
# Should trigger REVIEW workflow
```

---

## Documentation

- **Skills Reference**: See `skills/` directory for individual skill documentation
- **Subagents Reference**: See `subagents/` directory for subagent specifications
- **Workflow Documentation**: See `skills/cc10x-orchestrator/workflows/` for workflow details

---

## Design Principles

**Progressive Disclosure**: Load only what's needed when it's needed
**Evidence-First**: No success claims without verification
**Principles Over Prescriptions**: Teach decision frameworks, not rigid checklists
**Systematic Processes**: Repeatable workflows with clear stages

---

## License

MIT License - See LICENSE file for details

---

## Contributing

For improvements or issues:
1. Check existing documentation in `skills/` and `subagents/`
2. Review workflow specifications
3. Submit detailed reports with examples

---

**Version**: 3.0.0
**Status**: Production Ready
**Last Updated**: 2025-10-29
