# Iteration 1: Repository Structure & Core Concepts

**Date:** October 23, 2025  
**Research Phase:** Structure & Methodology Analysis  
**Repositories Analyzed:**
- GitHub Spec Kit (github/spec-kit) - 40.9k stars
- BMAD METHOD (bmad-code-org/BMAD-METHOD) - 19.5k stars
- cc10x (romiluz13/cc10x) - Our project

---

## Executive Summary

Both Spec Kit and BMAD METHOD represent sophisticated approaches to AI-assisted development, each with distinct philosophies:

- **Spec Kit**: Specification-Driven Development (SDD) where specifications become executable and generate code
- **BMAD METHOD**: Agentic Agile Development with dedicated planning agents and context-engineered development
- **cc10x**: Orchestration-driven workflow combining commands, sub-agents, and skills for production-ready development

**Key Finding**: cc10x already incorporates elements from both methodologies while adding unique orchestration capabilities they lack.

---

## 1. Repository Structure Comparison

### 1.1 Directory Organization

#### Spec Kit Structure
```
spec-kit/
├── .devcontainer/         # Development container config
├── .github/               # GitHub Actions & workflows
├── docs/                  # Documentation (installation, quickstart, local dev)
├── media/                 # Images, GIFs, videos
├── memory/                # Constitution.md (project principles)
├── scripts/               # Bash & PowerShell automation
│   ├── bash/
│   └── powershell/
├── src/specify_cli/       # Python CLI tool implementation
├── templates/             # Spec, plan, tasks, agent templates
│   ├── commands/
│   ├── agent-file-template.md
│   ├── plan-template.md
│   ├── spec-template.md
│   └── tasks-template.md
├── AGENTS.md              # Agent system documentation
├── spec-driven.md         # Core methodology document
└── pyproject.toml         # Python package definition
```

**Key Characteristics:**
- **Python-based CLI** (`src/specify_cli/`)
- **Template-driven** (specs, plans, tasks)
- **Memory folder** with constitution pattern
- **Multi-platform scripts** (bash + PowerShell)
- **Heavy documentation focus**

#### BMAD METHOD Structure
```
BMAD-METHOD/
├── bmad-core/             # Core framework (the brain)
│   ├── agents/            # Individual agent definitions
│   ├── agent-teams/       # Team bundles (collections of agents)
│   ├── checklists/        # QA checklists
│   ├── data/              # Knowledge base, preferences
│   ├── tasks/             # Reusable task definitions
│   ├── templates/         # Document templates
│   └── workflows/         # Workflow definitions (YAML)
├── common/                # Shared utilities
│   ├── tasks/
│   └── utils/
├── docs/                  # Documentation
├── expansion-packs/       # Domain-specific extensions
│   ├── bmad-2d-phaser-game-dev/
│   ├── bmad-infrastructure-devops/
│   └── [more packs...]
├── tools/                 # Build & deployment tools
│   ├── builders/          # Web bundle builder
│   ├── flattener/
│   ├── installer/
│   └── upgraders/
└── dist/                  # Built web bundles (.txt files)
    └── teams/
```

**Key Characteristics:**
- **Modular agent system** (`bmad-core/`)
- **Expansion pack architecture** (domain extensibility)
- **Build system** for web UI bundles
- **YAML-based workflows** with Mermaid diagrams
- **Node.js/JavaScript-based**

#### cc10x Structure
```
cc10x/
├── .claude-plugin/        # Plugin metadata
│   └── plugin.json
├── agents/                # 7 sub-agents (specialized reviewers)
│   ├── accessibility-reviewer.md
│   ├── context-analyzer.md
│   ├── implementer.md
│   ├── performance-analyzer.md
│   ├── quality-reviewer.md
│   ├── security-reviewer.md
│   └── ux-reviewer.md
├── commands/              # 4 orchestration commands
│   ├── bug-fix.md
│   ├── feature-build.md
│   ├── feature-plan.md
│   └── review.md
├── skills/                # 16 auto-activating skills
│   ├── accessibility-patterns/
│   ├── bug-fixing/
│   ├── test-driven-development/
│   ├── ui-design/
│   └── [12 more...]
├── hooks/                 # Session & context management
│   ├── session-start.sh
│   ├── pre-compact.sh
│   └── hooks.json
└── inspiration/           # Research documentation
```

**Key Characteristics:**
- **Plugin architecture** (Claude Code native)
- **Three-layer system** (commands → agents → skills)
- **Auto-activation via triggers** (skills)
- **Hook system** for lifecycle management
- **Minimal, focused structure**

### 1.2 Structure Comparison Table

| Aspect | Spec Kit | BMAD METHOD | cc10x | Winner |
|--------|----------|-------------|-------|--------|
| **Organization** | Template-driven | Agent-centric | Plugin-centric | Tie (different models) |
| **Modularity** | Medium (templates) | High (agents+packs) | High (3-layer) | **BMAD/cc10x** |
| **Extensibility** | Medium (templates) | Excellent (packs) | Good (skills) | **BMAD** |
| **Simplicity** | Medium (CLI tool) | Complex (build sys) | Simple (no build) | **cc10x** |
| **File Count** | ~50 core files | ~200+ files | ~35 core files | **cc10x** (focused) |

---

## 2. Core Methodology Concepts

### 2.1 Spec Kit: Specification-Driven Development (SDD)

**Philosophy:** "Specifications don't serve code—code serves specifications."

**Core Principles:**
1. **Power Inversion** - Specifications become executable, generating code rather than guiding it
2. **Executable Specifications** - Specs are precise, complete, unambiguous enough to generate working systems
3. **Continuous Refinement** - Iterative improvement of specifications over time
4. **Research-Driven Context** - Research agents gather technical context throughout
5. **Bidirectional Feedback** - Production reality informs specification evolution
6. **Branching for Exploration** - Multiple implementations from same spec

**Key Commands:**
- `/speckit.constitution` - Create project governing principles
- `/speckit.specify` - Define what to build (requirements)
- `/speckit.plan` - Create technical implementation plan
- `/speckit.tasks` - Generate actionable task list
- `/speckit.implement` - Execute tasks according to plan

**Workflow:**
```
Constitution → Specification → Plan → Tasks → Implementation
```

**Memory Management:**
- **Constitution.md** - Project governing principles (immutable)
- Located in `memory/` directory
- Templates enforce constitutional compliance
- Phase gates check against constitution

### 2.2 BMAD METHOD: Agentic Agile Development

**Philosophy:** "Dedicated agents collaborate through context-engineered workflows."

**Core Innovations:**
1. **Agentic Planning** - Analyst, PM, Architect agents collaborate on detailed PRDs/Architecture
2. **Context-Engineered Development** - Scrum Master creates hyper-detailed stories with full context
3. **Two-Phase Approach** - Planning (web UI) → Development (IDE)
4. **Agent Teams** - Pre-packaged collections for specific purposes
5. **Expansion Packs** - Domain extensibility beyond software development

**Key Agents:**
- **Analyst** - Brainstorming, market research, brief creation
- **PM (Product Manager)** - PRD creation from briefs
- **Architect** - Architecture design from PRDs
- **PO (Product Owner)** - Validation, sharding, orchestration
- **SM (Scrum Master)** - Story drafting with extreme detail
- **Dev** - Sequential implementation
- **QA (Test Architect)** - Risk profiling, test design, quality gates
- **BMad-Orchestrator** - Web UI multi-agent coordinator
- **BMad-Master** - Can perform any task (except implementation)

**Workflow:**
```
Analyst → PM (PRD) → Architect → PO (Shard) → SM (Story) → Dev → QA → Repeat
```

**Memory Management:**
- **core-config.yaml** - Configuration for project structure
- **PRD sharding** - Break large documents into epics/stories
- **Architecture sharding** - Break architecture into focused documents
- **Story files** - Contain full context for dev agent
- **devLoadAlwaysFiles** - Persistent context for dev agent

### 2.3 cc10x: Orchestration-Driven Workflow

**Philosophy:** "Orchestrate specialized sub-agents and auto-activating skills for production-ready results."

**Core Principles:**
1. **Three-Layer Architecture** - Commands orchestrate agents, agents use skills
2. **Strict TDD Enforcement** - RED-GREEN-REFACTOR mandatory (no exceptions)
3. **Progressive Loading** - 93% token savings via staged context
4. **Auto-Healing Context** - Snapshots at 75% token usage
5. **Multi-Dimensional Verification** - Parallel review across 5 dimensions
6. **Production-First** - Lovable/Bolt-quality UI, complete implementations

**Key Commands:**
- `/feature-plan` - PRD-style planning with architecture decisions
- `/feature-build` - 5-phase TDD-enforced implementation
- `/bug-fix` - LOG FIRST systematic debugging
- `/review` - Parallel multi-dimensional code review

**Workflow:**
```
Command → Sub-Agent(s) → Auto-Activated Skills → Quality Gates → Production Code
```

**Memory Management:**
- **Session tracking** - session-start.sh with metrics
- **Context snapshots** - pre-compact.sh at 75% tokens
- **Progressive loading** - 3-stage context loading
- **Hook system** - Lifecycle event management
- **Working plan** - `.claude/memory/WORKING_PLAN.md`

---

## 3. Detailed Concept Comparison

### 3.1 Planning Approach

| Aspect | Spec Kit | BMAD METHOD | cc10x |
|--------|----------|-------------|-------|
| **Document Type** | Specification | PRD | Feature Plan (PRD-style) |
| **Creation Method** | Template-driven | Agent collaboration | Command-driven |
| **Tech Stack** | Separate (in plan) | In Architecture doc | In feature plan |
| **Granularity** | Spec → Plan → Tasks | Brief → PRD → Arch → Stories | Feature Description → Plan |
| **Validation** | Constitution gates | PO Master Checklist | Quality gates in workflow |
| **Iteration** | Continuous refinement | PO updates & re-shards | Plan then build (or iterate) |

**Analysis:**
- Spec Kit: Most formal, constitution-enforced
- BMAD: Most collaborative, agent-driven
- cc10x: Most pragmatic, command-driven

### 3.2 Agent/Sub-Agent Systems

| Aspect | Spec Kit | BMAD METHOD | cc10x |
|--------|----------|-------------|-------|
| **Agent Count** | Variable (AI-agnostic) | 15+ core agents | 7 sub-agents |
| **Agent Type** | Generic AI assistants | Specialized roles | Specialized reviewers |
| **Coordination** | User-driven | Orchestrator-driven | Command-driven |
| **Parallelization** | Not specified | Sequential (SM→Dev) | Parallel (5 reviewers) |
| **Context Isolation** | Not specified | Per-agent context | Per-agent context |
| **Agent Definition** | Minimal (templates) | Detailed (MD + YAML) | Detailed (MD + YAML) |

**Key Differences:**
- **Spec Kit**: Agents are user's AI assistant following templates
- **BMAD**: Agents are distinct personas with specific workflows
- **cc10x**: Sub-agents are specialized roles invoked by commands

### 3.3 Quality & Testing

| Aspect | Spec Kit | BMAD METHOD | cc10x |
|--------|----------|-------------|-------|
| **TDD Enforcement** | Mentioned in constitution | Not strictly enforced | **STRICT (mandatory)** |
| **Test Strategy** | Part of spec/plan | QA agent (*design task) | Built into workflows |
| **Quality Gates** | Constitution phases | QA gates (PASS/CONCERNS/FAIL) | Per-phase quality gates |
| **Review Process** | Not specified | QA agent *review task | Multi-dimensional parallel |
| **Test Coverage** | Not specified | QA *trace task | Required >80% |

**Winner: cc10x** - Strictest TDD enforcement, most comprehensive quality gates

### 3.4 Memory & Context Management

| Aspect | Spec Kit | BMAD METHOD | cc10x |
|--------|----------|-------------|-------|
| **Primary Pattern** | Constitution.md | config.yaml + sharding | Hooks + snapshots |
| **Context Preservation** | Not specified | Story files | Pre-compact snapshots |
| **Token Optimization** | Not specified | Document sharding | **Progressive loading (93%)** |
| **Session Management** | Not specified | Per-agent | session-start.sh |
| **Auto-Healing** | Not specified | Not specified | **Yes (75% threshold)** |
| **Metrics Tracking** | Not specified | Not specified | **Yes (hooks)** |

**Winner: cc10x** - Most sophisticated context management, auto-healing, token optimization

---

## 4. Unique Strengths

### 4.1 What Spec Kit Does Best

1. **Constitutional Framework** - Immutable principles enforced through templates
2. **Specification Focus** - Treats specs as primary artifacts, code as output
3. **Template Quality** - Sophisticated templates with LLM instructions
4. **AI-Agnostic** - Works with Claude, Gemini, Copilot, Cursor, etc.
5. **CLI Tool** - Python-based `specify` CLI for bootstrapping

### 4.2 What BMAD METHOD Does Best

1. **Agent Specialization** - 15+ distinct agent personas with clear roles
2. **Expansion Packs** - Extensible to any domain (game dev, writing, business)
3. **QA Agent (Quinn)** - Sophisticated Test Architect with risk profiling
4. **Document Sharding** - Break large docs into manageable pieces
5. **Web UI Support** - Pre-built bundles for web-based AI platforms
6. **Workflow Visualization** - Mermaid diagrams for planning & dev cycles

### 4.3 What cc10x Does Best

1. **Strict TDD Enforcement** - RED-GREEN-REFACTOR mandatory, no exceptions
2. **Progressive Loading** - 93% token savings through staged context
3. **Auto-Healing** - Automatic snapshots at 75% token usage
4. **Multi-Dimensional Review** - 5 parallel reviewers (security, quality, performance, UX, a11y)
5. **Production-First** - Lovable/Bolt-quality UI generation
6. **Skill Auto-Activation** - 15 trigger phrases per skill for automatic invocation
7. **Simplest Structure** - No build system, plugin-native, minimal files

---

## 5. What cc10x Can Learn

### 5.1 From Spec Kit

✅ **Already Implemented:**
- Commands act like their slash commands
- Templates embedded in skills
- Quality gates in workflows
- Multi-phase workflows

❓ **Consider Adding:**
1. **Constitution Pattern** - Similar to Spec Kit's immutable principles
   - Could create `CONSTITUTION.md` in `.claude/memory/`
   - Define project-specific principles (like TDD enforcement)
   - Reference in commands and agents
   - **Assessment**: Interesting but may be overkill - cc10x already enforces principles through commands

2. **Explicit Tech Stack Templates**
   - Spec Kit has clear separation: spec (no tech) → plan (with tech)
   - cc10x mixes them in feature-plan
   - **Assessment**: Current approach is more pragmatic, no change needed

### 5.2 From BMAD METHOD

✅ **Already Implemented:**
- Sub-agents similar to their specialized agents
- Skills similar to their tasks
- Hooks similar to their lifecycle management

❓ **Consider Adding:**
1. **Document Sharding Pattern**
   - BMAD shards large PRDs/Architecture into epics/stories
   - cc10x could shard large feature plans into sub-features
   - **Assessment**: Useful for very large features, but cc10x's progressive loading achieves similar results

2. **QA Risk Profiling** (*risk command)
   - BMAD's QA agent assesses risks before development
   - cc10x could add risk assessment to feature-plan
   - **Assessment**: Good idea! Could enhance planning phase

3. **Expansion Pack Architecture**
   - BMAD's extensibility to non-software domains
   - cc10x is software-focused
   - **Assessment**: Out of scope, but the architecture (skills as plugins) supports this

4. **Config File Pattern**
   - BMAD's `core-config.yaml` for project-specific settings
   - cc10x hardcodes paths
   - **Assessment**: Not critical, but could improve flexibility

---

## 6. Competitive Positioning

### 6.1 Strengths Comparison Matrix

| Strength | Spec Kit | BMAD | cc10x | Best |
|----------|----------|------|-------|------|
| **TDD Enforcement** | Mentioned | Optional | **STRICT** | **cc10x** |
| **Token Efficiency** | - | Sharding | **93% savings** | **cc10x** |
| **Auto-Healing** | - | - | **Yes** | **cc10x** |
| **Quality Review** | Gates | QA agent | **5 parallel** | **cc10x** |
| **Constitutional Framework** | **Excellent** | Medium | Good | **Spec Kit** |
| **Agent Specialization** | Low | **Excellent** | Good | **BMAD** |
| **Extensibility** | Medium | **Excellent** | Good | **BMAD** |
| **Simplicity** | Medium | Complex | **Simple** | **cc10x** |
| **Documentation** | **Excellent** | Excellent | Excellent | **Tie** |
| **Production UI** | - | - | **Lovable/Bolt** | **cc10x** |

### 6.2 Workflow Philosophy Comparison

**Spec Kit**: "Specifications are king, code serves specs"
- **Strength**: Treats intent as primary artifact
- **Weakness**: Requires maintaining specifications alongside code

**BMAD METHOD**: "Specialized agents collaborate on detailed context"
- **Strength**: Clear role separation, comprehensive planning
- **Weakness**: Complex multi-agent coordination, environment switching (web → IDE)

**cc10x**: "Orchestrate specialized agents for production-ready results"
- **Strength**: Simple, focused, production-first, single environment
- **Weakness**: Software development only (not domain-agnostic)

---

## 7. Key Insights

### 7.1 Architectural Insights

1. **Three Distinct Approaches**
   - Spec Kit: Document-centric (specifications drive everything)
   - BMAD: Agent-centric (agents collaborate through documents)
   - cc10x: Orchestration-centric (commands orchestrate agents & skills)

2. **Complexity vs Simplicity**
   - Spec Kit: Medium (CLI tool + templates)
   - BMAD: High (build system, web bundles, many agents)
   - cc10x: Low (plugin-native, no build step)

3. **Context Management Maturity**
   - Spec Kit: Basic (constitution pattern)
   - BMAD: Good (sharding, config files)
   - cc10x: Excellent (progressive loading, auto-healing, hooks)

### 7.2 Methodology Insights

1. **Planning Granularity**
   - Spec Kit: Spec → Plan → Tasks (3 levels)
   - BMAD: Brief → PRD → Arch → Epic → Story (5 levels)
   - cc10x: Feature Plan → Implementation (2 levels)

2. **Quality Enforcement**
   - Spec Kit: Constitutional gates
   - BMAD: QA agent with advisory authority
   - cc10x: Mandatory quality gates in every phase

3. **Agent Coordination**
   - Spec Kit: User coordinates
   - BMAD: Orchestrator coordinates
   - cc10x: Commands coordinate

---

## 8. Conclusion

### What cc10x Already Does Better

1. ✅ **Stricter TDD Enforcement** - Mandatory RED-GREEN-REFACTOR
2. ✅ **Better Token Efficiency** - 93% savings vs their approaches
3. ✅ **Auto-Healing Context** - Neither has this
4. ✅ **Multi-Dimensional Review** - 5 parallel reviewers vs sequential
5. ✅ **Simpler Structure** - Plugin-native, no build system
6. ✅ **Production-First UI** - Lovable/Bolt quality built-in
7. ✅ **Skill Auto-Activation** - 15 triggers per skill

### What Could Be Learned

1. ❓ **Constitution Pattern** - Interesting but maybe overkill
2. ✅ **Risk Profiling** - Could add to feature-plan (good idea!)
3. ❓ **Document Sharding** - Progressive loading already solves this
4. ❓ **Config File** - Nice to have but not critical

### Confidence Statement

**cc10x demonstrates equal or superior capabilities compared to Spec Kit and BMAD METHOD across most dimensions:**

- **Quality Gates**: cc10x's mandatory multi-dimensional review exceeds both
- **Context Management**: cc10x's auto-healing and progressive loading are unique
- **Simplicity**: cc10x's plugin-native architecture is simpler than both
- **TDD Enforcement**: cc10x's strict enforcement exceeds both
- **Production Focus**: cc10x's Lovable/Bolt-quality UI is unique

**Areas where they excel:**
- Spec Kit: Constitutional framework, AI-agnostic design
- BMAD: Agent specialization, domain extensibility

**Overall Assessment**: cc10x is **production-ready and competitive** with these 40k+ and 19k+ star projects, with unique advantages in quality enforcement, token efficiency, and context management.

---

**Next Iteration**: Commands & Workflows Deep Dive


