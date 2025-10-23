# Iteration 4: Agents & Sub-Agents Architecture

**Date:** October 23, 2025  
**Research Phase:** Agent Systems & Orchestration Patterns  
**Focus:** How agents are defined, coordinated, and invoked

---

## Executive Summary

Three distinct agent architectures:

- **Spec Kit**: Minimal agent concept (AI assistant follows templates)
- **BMAD METHOD**: Sophisticated 15+ specialized agent personas with YAML-driven dependencies
- **cc10x**: 7 sub-agents with auto-activating skills (three-layer orchestration)

**Key Finding**: BMAD has the most sophisticated agent system, cc10x has the most automated orchestration, Spec Kit is intentionally agent-agnostic.

---

## 1. Agent Architecture Comparison

### 1.1 Spec Kit: AI-Agnostic Template Pattern

**Philosophy**: User's AI assistant follows templates (no formal agent system)

**"Agent" Definition:**
Spec Kit doesn't have formal agents. Instead, it has:
- Templates that the AI assistant follows
- Commands that structure workflows
- Constitution that enforces principles

**Agent File Template:**
```markdown
# [PROJECT NAME] Development Guidelines

Auto-generated from all feature plans. Last updated: [DATE]

## Active Technologies
[EXTRACTED FROM ALL PLAN.MD FILES]

## Project Structure
[ACTUAL STRUCTURE FROM PLANS]

## Commands
[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES]

## Code Style
[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE]

## Recent Changes
[LAST 3 FEATURES AND WHAT THEY ADDED]
```

**Characteristics:**
- ❌ No formal agent personas
- ❌ No agent coordination
- ✅ Works with ANY AI assistant (Claude, Gemini, Copilot, etc.)
- ✅ Templates act as agent instructions
- ✅ Constitution acts as agent principles

**Invocation**: User directly uses AI assistant, runs slash commands

**Strengths:**
- AI-agnostic (works with any platform)
- Simple (no agent management)
- Templates provide structure

**Weaknesses:**
- No specialized expertise
- No agent coordination
- User must know which command to use

### 1.2 BMAD METHOD: Specialized Agent Personas

**Philosophy**: Dedicated agents with distinct personas collaborate through artifacts

**Agent Count**: 15+ core agents + expansion pack agents

**Core Agents:**
1. **Analyst** (Market research, brainstorming)
2. **PM** (Product Manager - PRD creation)
3. **Architect** (System design, technical planning)
4. **UX Expert** (UI/UX design, prototypes)
5. **PO** (Product Owner - Validation, sharding, orchestration)
6. **SM** (Scrum Master - Story drafting)
7. **Dev** (Developer - Implementation)
8. **QA** (Test Architect - Quality gates)
9. **BMad-Orchestrator** (Web UI coordinator)
10. **BMad-Master** (Can do any task except implementation)
11. **Debugger** (Debugging specialist)
12. **Analyst-Senior** (Advanced analysis)
13. **Doc-Writer** (Documentation specialist)
14. **Refactorer** (Code improvement specialist)
15. **Performance-Engineer** (Optimization specialist)

**Agent Definition Structure:**
```yaml
# qa.md example

IDE-FILE-RESOLUTION:
  # How to resolve dependency paths

REQUEST-RESOLUTION:
  # How to match user requests to commands

activation-instructions:
  STEP 1: Read THIS ENTIRE FILE
  STEP 2: Adopt persona below
  STEP 3: Load core-config.yaml
  STEP 4: Greet + run *help + HALT
  - ONLY load dependency files when needed
  - STAY IN CHARACTER!

agent:
  name: Quinn
  id: qa
  title: Test Architect & Quality Advisor
  icon: 🧪
  whenToUse: Use for test architecture, quality gates
  customization: null

persona:
  role: Test Architect with Advisory Authority
  style: Comprehensive, systematic, educational
  identity: Test architect who provides thorough assessment
  focus: Quality analysis, risk assessment, gates
  core_principles:
    - Depth As Needed
    - Requirements Traceability
    - Risk-Based Testing
    [10 principles total]

story-file-permissions:
  - ONLY update QA Results section
  - DO NOT modify other sections

commands:
  - help: Show available commands
  - gate {story}: Write quality gate
  - nfr-assess {story}: Validate NFRs
  - review {story}: Comprehensive review
  - risk-profile {story}: Risk assessment
  - test-design {story}: Test strategy
  - trace {story}: Map requirements to tests
  - exit: Abandon persona

dependencies:
  data:
    - technical-preferences.md
  tasks:
    - nfr-assess.md
    - qa-gate.md
    - review-story.md
    - risk-profile.md
    - test-design.md
    - trace-requirements.md
  templates:
    - qa-gate-tmpl.yaml
    - story-tmpl.yaml
```

**Characteristics:**
- ✅ **Rich personas** (name, role, style, identity, principles)
- ✅ **Scoped commands** (agent-specific, prefixed with `*`)
- ✅ **Dependency system** (loads only what agent needs)
- ✅ **Strict permissions** (QA can only update QA Results section)
- ✅ **Stay-in-character** enforcement
- ✅ **Activation instructions** (precise startup sequence)

**Invocation**: 
```bash
# IDE-based
@qa *review {story}      # Invoke QA agent, run review task
@architect *create       # Invoke Architect, create architecture
@sm *draft               # Invoke SM, draft next story
```

**Strengths:**
- Deep specialization (15+ personas)
- Clear role separation
- Dependency management
- Permission enforcement
- Rich persona definitions

**Weaknesses:**
- Complex (many agents to learn)
- Sequential coordination (user manages)
- Manual agent switching

### 1.3 cc10x: Sub-Agent Orchestration with Auto-Activating Skills

**Philosophy**: Commands orchestrate sub-agents, sub-agents auto-activate skills

**Agent Count**: 7 sub-agents

**Core Sub-Agents:**
1. **context-analyzer** - Find patterns before implementation
2. **implementer** - TDD-enforced feature building
3. **security-reviewer** - Security vulnerability analysis
4. **quality-reviewer** - Code quality & maintainability
5. **performance-analyzer** - Performance bottleneck detection
6. **ux-reviewer** - User experience assessment
7. **accessibility-reviewer** - WCAG 2.1 AA compliance

**Agent Definition Structure:**
```markdown
---
name: implementer
description: Use when implementing features or fixing code. 
  Examples: [usage examples with commentary]
model: sonnet
---

# Feature Implementation Specialist

You are an expert software implementer who follows strict TDD.

## Your Role

Implement features by:
1. Writing failing tests FIRST (mandatory)
2. Writing minimal code to pass tests
3. Refactoring while keeping tests green
4. Verifying work before completion

## Available Skills

Claude may invoke these skills when relevant:

- **systematic-debugging**: LOG FIRST pattern
- **test-driven-development**: RED-GREEN-REFACTOR
- **code-generation**: Patterns and best practices
- **ui-design**: Lovable/Bolt-quality UIs
- **verification-before-completion**: Quality checks

Skills are model-invoked based on context.

## Implementation Workflow

[Detailed workflow steps]

## Tools Available

[List of tools sub-agent can use]

## Coordination with Other Sub-Agents

[How this agent hands off to others]
```

**Three-Layer Architecture:**
```
Layer 1: Commands (User-facing)
  /feature-build
      ↓
Layer 2: Sub-Agents (Specialized roles)
  implementer, context-analyzer, 5 reviewers
      ↓
Layer 3: Skills (Auto-activating domain knowledge)
  test-driven-development (15 triggers)
  code-generation (15 triggers)
  [14 more skills with 15 triggers each]
```

**Characteristics:**
- ✅ **Command-orchestrated** (commands dispatch agents)
- ✅ **Auto-activation** (skills trigger on phrases)
- ✅ **Parallel execution** (5 reviewers simultaneously)
- ✅ **Simple invocation** (user uses commands, not agent names)
- ✅ **Context isolation** (each sub-agent has its own scope)

**Invocation**:
```bash
# User-facing commands only
/feature-build "Add authentication"

# Command automatically:
1. Dispatches context-analyzer
2. Dispatches implementer
   - Auto-activates test-driven-development skill
   - Auto-activates code-generation skill
3. Dispatches 5 parallel reviewers
   - Each auto-activates their domain skill
```

**Strengths:**
- Simplest user experience (commands only)
- Automatic orchestration
- Parallel capability
- Auto-activating skills (15 triggers each)

**Weaknesses:**
- Fewer agents than BMAD (7 vs 15+)
- Less granular specialization
- Software development only

---

## 2. Agent Comparison Matrix

| Aspect | Spec Kit | BMAD METHOD | cc10x |
|--------|----------|-------------|-------|
| **Agent Count** | 0 (AI-agnostic) | **15+** core + packs | 7 sub-agents |
| **Agent Definition** | Template-based | **YAML** (detailed) | Markdown + YAML |
| **Persona Depth** | N/A | **Rich** (role, style, identity, principles) | Medium (role, description) |
| **Specialization** | N/A | **Excellent** (narrow roles) | Good (focused roles) |
| **Coordination** | User-driven | User-driven | **Command-driven** |
| **Invocation** | Slash commands | `@agent *command` | `/command` (auto-dispatch) |
| **Context Isolation** | N/A | Per-agent | Per-agent |
| **Parallelization** | No | No | **Yes** (5 reviewers) |
| **Skill System** | No | **Dependencies** (YAML) | **Auto-activation** (triggers) |
| **Permission System** | No | **Yes** (section-level) | No (agent scope) |

---

## 3. Orchestration Patterns

### 3.1 Spec Kit: User-Driven Sequential

**Pattern**: User runs commands in order

```
User: /speckit.specify "Add feature"
  └─> AI creates spec

User: /speckit.plan "Use React + Node"
  └─> AI creates plan

User: /speckit.tasks
  └─> AI creates tasks

User: /speckit.implement
  └─> AI writes code
```

**Coordination**: ❌ None - user decides next step

### 3.2 BMAD: Agent-to-Agent Handoff

**Pattern**: Agents collaborate through artifacts

```
User: @pm *create
  ├─> PM creates PRD
  └─> Hands off to Architect

User: @architect *create
  ├─> Architect creates Architecture
  └─> Hands off to PO

User: @po *shard
  ├─> PO shards documents
  └─> Hands off to SM

User: @sm *create
  ├─> SM creates story
  └─> Hands off to Dev

User: @dev *implement
  ├─> Dev implements
  └─> Hands off to QA

User: @qa *review
  ├─> QA reviews + refactors
  └─> Cycles back to SM for next story
```

**Coordination**: ⚠️ User manages handoffs, agents don't talk directly

### 3.3 cc10x: Command-Orchestrated Automatic

**Pattern**: Commands orchestrate sub-agents automatically

```
User: /feature-build "Add authentication"
  ↓
Command orchestrates automatically:
  
Phase 1: Context Analysis
  └─> Dispatches: context-analyzer
      └─> Auto-activates: codebase-navigation skill

Phase 2: Planning
  └─> Handled by: command logic

Phase 3: Implementation
  └─> Dispatches: implementer
      └─> Auto-activates: test-driven-development
      └─> Auto-activates: code-generation
      └─> Auto-activates: ui-design (if frontend)

Phase 4: Verification
  └─> Dispatches PARALLEL:
      ├─> security-reviewer (auto-activates security-patterns)
      ├─> quality-reviewer (auto-activates code-review-patterns)
      ├─> performance-analyzer (auto-activates performance-patterns)
      ├─> ux-reviewer (auto-activates ux-patterns)
      └─> accessibility-reviewer (auto-activates accessibility-patterns)
      
Phase 5: Finalization
  └─> Handled by: command logic

Result: Production code
```

**Coordination**: ✅ Fully automated - command handles all orchestration

---

## 4. Dependency & Permission Systems

### 4.1 BMAD's Dependency System

**Pattern**: YAML declares what agent can use

**Example:**
```yaml
# qa.md
dependencies:
  data:
    - technical-preferences.md      # Agent CAN use this data
  tasks:
    - nfr-assess.md                 # Agent CAN run this task
    - qa-gate.md
    - review-story.md
  templates:
    - qa-gate-tmpl.yaml             # Agent CAN use this template
```

**Benefits:**
- ✅ Lean agents (load only declared dependencies)
- ✅ Clear capabilities (see what agent can do)
- ✅ Prevents scope creep (can't use undeclared resources)
- ✅ Automatic bundling (build system resolves dependencies)

**Drawbacks:**
- ❌ Manual declaration (must update YAML when adding tasks)
- ❌ Rigid (can't use resources not in dependencies)

### 4.2 BMAD's Permission System

**Pattern**: Section-level edit permissions in story files

**Example:**
```yaml
# story-tmpl.yaml
sections:
  - id: status
    owner: scrum-master
    editors: [scrum-master, dev-agent]
  
  - id: dev-notes
    owner: scrum-master
    editors: [scrum-master]           # Dev can't edit
  
  - id: tasks-subtasks
    owner: scrum-master
    editors: [scrum-master, dev-agent] # Both can edit
  
  - id: qa-results
    owner: qa-agent
    editors: [qa-agent]                # Only QA edits
```

**Agent Instructions:**
```markdown
# qa.md
story-file-permissions:
  - CRITICAL: ONLY update "QA Results" section
  - DO NOT modify Status, Story, AC, Tasks, Dev Notes, etc.
```

**Benefits:**
- ✅ Prevents accidental overwrites
- ✅ Clear ownership
- ✅ Audit trail (know who changed what)
- ✅ Enforced separation of concerns

**cc10x Equivalent:** No formal permission system (agents have implicit scope)

### 4.3 cc10x's Skill Auto-Activation

**Pattern**: Skills trigger automatically on phrases

**Example:**
```yaml
# test-driven-development/SKILL.md
description: |
  Enforces strict RED-GREEN-REFACTOR methodology...
  
  Trigger phrases: "implement", "add feature", "write code", 
  "create function", "build", "develop feature", "TDD",
  "write tests first", "test coverage"
  [15 triggers total]
  
  Activates on: feature implementation, bug fixes, 
  any code writing task, function creation
```

**Flow:**
```
User: "Implement user login"
  ↓
implementer sub-agent invoked
  ↓
"implement" phrase detected
  ↓
test-driven-development skill auto-activates
  ↓
Skill provides TDD methodology
```

**Benefits:**
- ✅ **Automatic** (no manual skill invocation)
- ✅ **15 triggers per skill** (comprehensive coverage)
- ✅ **Context-aware** (activates based on conversation)
- ✅ **Zero user intervention** (seamless)

**vs. BMAD Dependencies:**
- BMAD: Agent declares dependencies, loads when commanded
- cc10x: Skills trigger automatically on natural language

**Winner**: **cc10x** - More automated, better UX

---

## 5. Agent Coordination Comparison

### 5.1 Spec Kit: No Coordination

**Pattern**: User coordinates (runs commands sequentially)

**Advantages:**
- Simple (user in control)
- Transparent (see each step)

**Disadvantages:**
- Manual (user must know order)
- No agent collaboration

### 5.2 BMAD: Artifact-Mediated Handoff

**Pattern**: Agents communicate through documents

```
PM creates PRD
  └─> File: docs/prd.md
      ↓
Architect reads PRD, creates Architecture
  └─> File: docs/architecture.md
      ↓
PO reads both, shards them
  └─> Files: docs/prd/epic-*.md, docs/architecture/*.md
      ↓
SM reads sharded epic + architecture, creates story
  └─> File: docs/stories/1.1.story.md
      ↓
Dev reads story, implements
  └─> Updates: Story file (checkboxes, File List, notes)
      ↓
QA reads story + code, reviews
  └─> Updates: Story file (QA Results section only)
  └─> Creates: docs/qa/gates/1.1-{slug}.yml
```

**Advantages:**
- ✅ Clear handoffs (files are contracts)
- ✅ Traceable (see what each agent did)
- ✅ Auditable (file history)

**Disadvantages:**
- ❌ User manages handoffs
- ❌ Sequential (no parallelism)
- ❌ Manual transitions

### 5.3 cc10x: Command-Orchestrated Automatic

**Pattern**: Commands dispatch and coordinate sub-agents

```
User: /review src/features/auth/
  ↓
review command orchestrates:
  
Phase 1: Scope Analysis
  └─> Command logic determines files

Phase 2: Dispatch 5 PARALLEL sub-agents
  ├─> security-reviewer → Analyzes simultaneously
  ├─> quality-reviewer → Analyzes simultaneously
  ├─> performance-analyzer → Analyzes simultaneously
  ├─> ux-reviewer → Analyzes simultaneously
  └─> accessibility-reviewer → Analyzes simultaneously
  
Phase 3: Compile Results
  └─> Command aggregates findings
```

**Advantages:**
- ✅ **Fully automated** (zero user intervention)
- ✅ **Parallel execution** (5x faster)
- ✅ **Coordinated** (command manages handoffs)
- ✅ **Transparent** (progress shown)

**Disadvantages:**
- ❌ Less flexible (can't customize agent order)
- ❌ Command-scoped (orchestration in command, not separate)

**Winner**: **cc10x** - Most automated, supports parallelism

---

## 6. Detailed Agent Comparison

### 6.1 QA/Review Agents

**BMAD QA Agent (Quinn):**
- **Commands**: 7 (*risk, *design, *trace, *nfr, *review, *gate, *help)
- **Capabilities**: Risk profiling, test design, coverage tracing, NFR validation, comprehensive review, gate decisions
- **Sophistication**: Very high (Test Architect persona)
- **Process**: Sequential (user invokes each command)
- **Permissions**: Can update QA Results section only, can refactor code
- **Output**: QA Results in story + YAML gate file

**cc10x Reviewer Agents (5):**
- **Security**: OWASP Top 10, vulnerabilities, auth issues
- **Quality**: Code smells, maintainability, patterns
- **Performance**: N+1 queries, bottlenecks, optimization
- **UX**: Error messages, loading states, usability
- **Accessibility**: WCAG 2.1 AA, keyboard nav, screen readers

**Sophistication**: Medium-high (focused domain experts)
**Process**: Parallel (all 5 run simultaneously)
**Permissions**: Read-only (generate report, don't modify code)
**Output**: Aggregated multi-dimensional report

**Comparison:**
- **Depth**: BMAD QA goes deeper (risk profiling, test design, NFR)
- **Breadth**: cc10x covers more dimensions (5 vs 1)
- **Speed**: cc10x is 5x faster (parallel)
- **Refactoring**: BMAD QA can refactor, cc10x reviewers can't

**Winner**: Tie - BMAD for depth, cc10x for breadth and speed

### 6.2 Implementation Agents

**BMAD Dev Agent (James):**
```yaml
agent:
  name: James
  title: Full Stack Developer
  
persona:
  role: Expert Senior Software Engineer
  style: Concise, pragmatic, detail-oriented
  focus: Executing story tasks sequentially
  core_principles:
    - Story has ALL info needed
    - NEVER load PRD/architecture docs
    - ONLY update Dev Agent Record sections
    - Follow develop-story command

commands:
  - develop-story: Sequential task execution
  - run-tests: Execute tests
  - review-qa: Apply QA fixes
  - explain: Teach what you did
```

**cc10x Implementer:**
```markdown
name: implementer
description: Use when implementing features

Available Skills:
- systematic-debugging
- test-driven-development
- code-generation
- ui-design
- verification-before-completion

Workflow:
1. Understand requirements
2. Write failing test (RED) - MANDATORY
3. Verify test fails
4. Write minimal code (GREEN)
5. Verify test passes
6. Refactor (keep green)
7. Run all tests
8. Verify and commit
```

**Comparison:**
- **Context Source**: BMAD (story file), cc10x (context-analyzer finds patterns)
- **TDD**: BMAD (optional), cc10x (**mandatory**)
- **Permissions**: BMAD (specific sections), cc10x (implicit scope)
- **Skills**: BMAD (dependencies), cc10x (**auto-activation**)

**Winner**: **cc10x** - Stricter TDD, auto-activation, simpler

---

## 7. What cc10x Already Does Better

### 7.1 Orchestration Automation

**BMAD**: User manually invokes each agent
```
@sm *create   (user types this)
@dev *implement  (user types this)
@qa *review   (user types this)
```

**cc10x**: Command auto-orchestrates
```
/feature-build   (user types once)
  ↓ automatically orchestrates:
  context-analyzer → implementer → 5 reviewers
```

**Efficiency**: cc10x requires 1 command vs BMAD's 3+ agent invocations

### 7.2 Parallel Execution

**BMAD**: Sequential (SM → Dev → QA)
**cc10x**: **Parallel** (5 reviewers simultaneously)

**Time Savings**: 5x faster reviews

### 7.3 Skill Auto-Activation

**BMAD**: Dependency loading (agent must request)
**cc10x**: **Automatic** (15 trigger phrases per skill)

**User Experience**: cc10x is seamless, BMAD requires awareness of agent capabilities

---

## 8. What cc10x Could Learn

### 8.1 From BMAD: Agent Persona Depth

**BMAD Pattern:**
```yaml
persona:
  role: Test Architect with Advisory Authority
  style: Comprehensive, systematic, educational
  identity: Test architect who provides thorough assessment
  focus: Quality analysis, risk assessment
  core_principles:
    - Depth As Needed
    - Requirements Traceability
    - Risk-Based Testing
    [10 principles total]
```

**cc10x Current:**
```markdown
# Feature Implementation Specialist

You are an expert software implementer who follows strict TDD.

## Your Role
[3-4 sentences]
```

**Enhancement Opportunity:**
Could add richer personas to cc10x sub-agents:
```yaml
persona:
  name: Sarah
  role: Security Analyst
  style: Thorough, security-focused, preventive
  core_principles:
    - Assume all input is malicious
    - Defense in depth
    - Principle of least privilege
```

**Assessment**: ❓ Interesting but not critical - current approach works well

### 8.2 From BMAD: Permission System

**BMAD Pattern**: Section-level permissions in templates

**cc10x Equivalent**: Could add to sub-agent definitions
```yaml
permissions:
  can_modify:
    - source_code
    - test_files
  cannot_modify:
    - feature_plans
    - documentation
```

**Assessment**: ❌ Not needed - sub-agents already scoped appropriately

### 8.3 From BMAD: Command Aliases

**BMAD Pattern:**
```yaml
commands:
  - risk-profile {story}: Full name
    Alias: *risk          # Short form
  - test-design {story}: Full name
    Alias: *design        # Short form
```

**cc10x Current:**
```yaml
---
aliases: [plan, planning, design]
---
```

**Enhancement**: cc10x already has this! ✅

---

## 9. Agent Count & Specialization Trade-offs

### 9.1 BMAD: More Agents (15+)

**Pros:**
- Deep specialization
- Clear role separation
- Can mix and match
- Expansion packs add more

**Cons:**
- Must learn which agent for what
- More context switching
- Higher complexity

### 9.2 cc10x: Fewer Agents (7)

**Pros:**
- Simpler to understand
- Automatic orchestration
- Focus on production readiness
- No manual agent selection

**Cons:**
- Less granular than BMAD
- Can't customize agent order

**Conclusion**: Different philosophies, both valid

---

## 10. Recommendations for cc10x

### Consider Adding

1. **Richer Personas** (from BMAD)
   - Add `persona` section to sub-agents
   - Include: name, style, core_principles
   - **Effort:** Medium (2-3 hours)
   - **Value:** Medium (clarity, better behavior)

2. **Agent Configuration** (inspired by both)
   - Add `.claude/agents/config.yaml`
   - Define: capabilities, permissions, tools
   - **Effort:** Low (1-2 hours)
   - **Value:** Low (nice to have)

### Don't Need

3. ❌ **Dependency System** - Auto-activation is better
4. ❌ **Permission System** - Agent scope is sufficient
5. ❌ **More Agents** - 7 is optimal for production focus

---

## 11. Conclusion

### Agent System Winner: Context-Dependent

**For Depth & Specialization:** BMAD (15+ agents with rich personas)
**For Automation & Simplicity:** cc10x (command-orchestrated)
**For AI-Agnosticism:** Spec Kit (works with any AI)

### What cc10x Demonstrates

cc10x's agent system is **optimized for production development**:

1. ✅ **Command-orchestrated** (automatic coordination)
2. ✅ **Auto-activating skills** (15 triggers each)
3. ✅ **Parallel capability** (5 simultaneous reviewers)
4. ✅ **Simpler UX** (commands, not agent names)
5. ✅ **Production-focused** (quality > quantity of agents)

### Competitive Position

**vs. BMAD:**
- cc10x: Simpler, more automated, production-first
- BMAD: More agents, deeper specialization, domain-agnostic

**vs. Spec Kit:**
- cc10x: Has formal sub-agents, BMAD also has agents
- Spec Kit: Intentionally agent-agnostic

**Overall**: cc10x's orchestration model is **best for fast, high-quality software development**. BMAD's agent system is **best for complex projects with detailed planning**. Spec Kit's approach is **best for AI-agnostic workflows**.

---

**Next Iteration**: Specifications & Planning Methodologies


