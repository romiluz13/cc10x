# Changelog

## [4.3.2] - 2025-01-29

### Added

- **EXECUTION MODE Warnings**: Added explicit "EXECUTION MODE - THIS IS NOT DOCUMENTATION" sections to orchestrator skill and all 5 workflow files. Makes it clear that workflows are executable instructions, not reference documentation. Prevents Claude Code from reading workflows as docs instead of executing them step-by-step.

### Changed

- **Orchestrator Skill**: Added explicit instructions that skill must be loaded using Skill tool (not just Read tool), and workflows must be executed as step-by-step instructions.
- **All Workflow Files**: Added execution mode warnings explicitly stating CRITICAL markers are hard stops, validation gates are mandatory checks, and subagent invocation is required.

### Fixed

- **Workflow Execution Issue**: Fixed issue where Claude Code was reading workflow files as documentation instead of executing them as step-by-step instructions.

## [4.3.1] - 2025-01-29

### Added

- **Automatic terminal-notifier Setup**: Added automatic check and installation of terminal-notifier for workflow completion notifications. Checks once per project, auto-installs via brew if available (like dotai), and informs user once if installation not possible.

### Changed

- **Session Start Hook**: Enhanced to automatically setup terminal-notifier on first session, ensuring notifications work automatically for users with brew.

## [4.3.0] - 2025-01-29

### Added

- **Super Keyword-Dense Orchestrator Description**: Enhanced orchestrator frontmatter description with explicit "AUTO-LOAD when user says:" keyword triggers at the start, making orchestrator discoverable for 95%+ of workflow requests
- **Explicit Keyword Triggers Section**: Added comprehensive "AUTO-LOAD TRIGGERS" section to orchestrator skill with all workflow keywords listed by category (PLAN, BUILD, REVIEW, DEBUG, VALIDATE)
- **Enhanced Skill-Discovery Enforcement**: Made orchestrator loading mandatory and explicit in skill-discovery checklist with keyword detection logic and validation steps
- **WHEN/HOW/WHY Sections**: Added comprehensive WHEN/HOW/WHY sections to all 5 workflow files explaining keywords, detection process, decision trees, and workflow comparisons
- **Quick Reference Guide**: Created `QUICK-REFERENCE.md` for one-page reference on orchestrator activation and workflow selection
- **Enhanced Context.json Rule**: Updated orchestrator rule description with explicit keyword triggers and example activation flow
- **Testing Checklist**: Created comprehensive testing checklist for orchestrator activation scenarios

### Changed

- **Orchestrator Description**: Frontmatter now starts with explicit keyword triggers ("AUTO-LOAD when user says: plan, planning, planner...") making it highly discoverable
- **Skill-Discovery Protocol**: Enhanced checklist to force orchestrator loading FIRST before any other skill check
- **Workflow Files**: All 5 workflows now have clear WHEN/HOW/WHY sections explaining activation and selection

### Fixed

- **Orchestrator Auto-Loading**: Fixed issue where orchestrator didn't auto-load when user said "plan" or other workflow keywords
- **Skill Discovery**: Fixed issue where skill-discovery didn't explicitly force orchestrator loading
- **Keyword Matching**: Enhanced keyword matching with semantic variants (planning, planner, plan a, etc.)

## [4.2.0] - 2025-01-29

### Added

- **Automatic Orchestrator Enforcement System**: Comprehensive enforcement mechanisms that automatically force Claude Code to use orchestrator without requiring user action
- **Context.json AlwaysApply Rules**: Created 7 alwaysApply rules in `.claude/context.json` to enforce orchestrator usage, subagent invocation, TDD cycle, Actions Taken tracking, memory integration, and web fetch integration
- **Enhanced Orchestrator Description**: Expanded orchestrator skill description with comprehensive workflow keywords and explicit bypass prevention warnings
- **Runtime Compliance Checks**: Added 4 validation checkpoints (before Phase 2, Phase 3, Phase 4, and Final Report) that automatically stop workflow if validation fails
- **Workflow Enforcement Instructions**: Added explicit "DO NOT write code directly" warnings and validation gates to all 5 workflow files
- **Validation Script**: Created `scripts/validate-orchestrator-compliance.sh` to programmatically validate orchestrator compliance
- **Enhanced Subagent Descriptions**: Added critical warnings to all subagent files preventing direct invocation
- **Pre-Prompt Hook**: Created optional pre-prompt hook to detect workflow keywords and warn if orchestrator should be loaded

### Changed

- **Orchestrator Skill**: Enhanced with comprehensive enforcement section, runtime validation gates, and explicit checklists
- **All Workflow Files**: Added critical enforcement sections and validation gates before key phases
- **Subagent Files**: Enhanced with explicit warnings and TDD cycle requirements

### Fixed

- **Direct Code Writing Bypass**: Fixed issue where Claude Code could write code directly without invoking subagents
- **TDD Cycle Skipping**: Fixed issue where BUILD workflow could skip RED → GREEN → REFACTOR cycle
- **Actions Taken Tracking**: Fixed issue where Actions Taken section could be skipped or incomplete
- **Inventory Checks**: Fixed issue where Skills/Subagents Inventory Checks could be skipped

## [4.1.0] - 2025-01-27

### Changed

- **Orchestrator as Mandatory Entry Point**: Updated orchestrator description to be most discoverable with all workflow keywords ("reviewing code", "planning features", "building components", "debugging errors", "validating implementations")
- **Workflow Activation**: All workflow skills now require orchestrator activation - workflows cannot be activated directly
- **Subagent Invocation**: All subagents now require orchestrator context - subagents cannot be invoked directly
- **Skill Discovery Protocol**: Updated skill-discovery to check orchestrator FIRST instead of before orchestrator runs

### Added

- **Workflow File Warnings**: Added explicit CRITICAL warnings at top of all workflow definition files reinforcing orchestrator requirement
- **Validation Enforcement**: All validation mechanisms (Skills Inventory Check, Subagents Inventory Check, Phase Checklists, Pre-Final-Report Validation) now work correctly as orchestrator always runs first

### Fixed

- **Activation Path Issues**: Fixed uncontrolled bypass mechanisms that allowed workflows/subagents to be activated without orchestrator
- **Orchestrator Discoverability**: Improved orchestrator description to match common user request keywords, ensuring orchestrator activates for 95%+ of requests

## [4.0.0] - 2025-01-27

### Changed

- Updated version to 4.0.0
- Removed marketing language from descriptions
- Made plugin descriptions more factual and developer-focused
- Removed internal ranking references

### Added

- Comprehensive system audit completed
- Functionality-first approach documented across all workflows
- Production readiness verification completed

## [3.2.0] - 2025-10-29

### Added

- **Subagent Activation Logic**: Explicit "when to invoke" and "when NOT to invoke" conditions for all workflows
- **Conflict Prevention**: Sequential execution rules and dependency management to prevent overlapping subagent work
- **User Override Support**: Explicit skip conditions that respect user preferences
- **Subagent Format Compliance**: All subagents follow `03-SUBAGENTS.md` format exactly

### Fixed

- **Subagent File Naming**: Renamed 5 subagents from `SKILL.md` to `SUBAGENT.md` (correct format)
- **Plugin.json References**: Updated all 9 subagent references to use `SUBAGENT.md`
- **Workflow References**: Updated all workflow files to reference `SUBAGENT.md` consistently
- **Emoji Cleanup**: Removed all emojis from workflow files, replaced with text markers (`**INVOKE**` / `**SKIP**`)

### Enhanced

- **Review Workflow**: Added scope-based skip logic, selection logic for focused reviews
- **Build Workflow**: Added skip conditions for trivial changes, dependency-only updates
- **Debug Workflow**: Added skip conditions for non-reproducible bugs, trivial fixes
- **Plan Workflow**: Added complexity-based skip logic, dependency management (architecture → design)
- **Orchestrator**: Added subagent invocation rules (verify existence, check skip conditions, respect overrides)

### Changes

- Workflow files now use text markers instead of emojis for professional compatibility
- All subagents verified to follow exact format from documentation
- Enhanced activation logic prevents conflicts and wasted context

## [3.1.0] - 2025-10-29

### Added

- Memory integration (filesystem-based)
- Web-fetch caching with Q&A pairs
- Workflow state persistence
- Deterministic intent mapping
- Error recovery timeouts
- Subagent output validation
- Component failure cascading
- Requirements completeness threshold
- Investigation timeout
- Validation workflow improvements
- Cache corruption handling

## [3.0.0] - 2025-10-28

Initial release of cc10x v3 with orchestration system.
