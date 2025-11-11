# Changelog

## [4.3.9] - 2025-01-29

### Added

- **Workflow Output Persistence**: Comprehensive persistence system for all workflow outputs (review, build, debug)
  - All workflows now save outputs to `.claude/docs/{workflow}/` directories in Phase 6
  - Reference files created (`.claude/memory/current_{workflow}.txt`) for easy access
  - Checkpoints updated with `output_file` and `output_saved` fields
- **Pre-Compact Hook Enhancements**:
  - Validation function checks if workflows are active but outputs not saved (warns before compaction)
  - Captures workflow output paths in snapshots
  - Includes output summaries (first 200 lines) in snapshots for better context recovery
  - Automatic cleanup of old output files (keeps last 20 per workflow type)
- **Post-Compact Hook Enhancements**:
  - Restores workflow output reference files from snapshots
  - Falls back to checkpoints if snapshot doesn't have outputs
  - Ensures outputs survive context compaction
- **PERSISTENCE-PATTERNS.md**: Comprehensive documentation of persistence patterns, recovery mechanisms, and examples

### Fixed

- **Output Loss During Compaction**: Fixed critical issue where review/build/debug outputs were lost during context compaction
- **Missing Output Restoration**: Fixed issue where workflow outputs weren't restored after compaction
- **No Output Validation**: Added validation to warn if outputs aren't saved before compaction

### Changed

- **Review Workflow Phase 6**: Added mandatory output persistence with save instructions and validation checklist
- **Build Workflow Phase 6**: Added mandatory output persistence with save instructions and validation checklist
- **Debug Workflow Phase 6**: Added mandatory output persistence with save instructions and validation checklist
- **Checkpoint Format**: Updated to include `output_file` and `output_saved` fields for all workflows

## [4.3.8] - 2025-01-29

### Added

- **Quick Start Sections**: Added Quick Start sections to all 39 skills with concise usage examples and step-by-step guidance
- **Troubleshooting Sections**: Added Troubleshooting sections to 38 skills covering common issues, symptoms, causes, fixes, and prevention strategies
- **Examples Sections**: Added inline Examples sections to 6 high-value skills (`code-generation`, `requirements-analysis`, `test-driven-development`, `verification-before-completion`, `security-patterns`, `context-preset-management`) with complete functionality-focused examples
- **Requirements/Dependencies Sections**: Added Requirements/Dependencies sections to 14 workflow, tool-using, and pattern skills clarifying prerequisites, tool access, and related skills
- **Skill Improvement Template**: Created `.skill-improvement-template.md` to standardize future skill enhancements

### Changed

- **Description Optimization**: Optimized all 39 skill descriptions to meet skill-writer guide standards:
  - All descriptions ≤1024 characters
  - All include "what it does" (provides/generates/identifies/etc.)
  - All include "when to use" (use when/use proactively/auto-load)
  - All include trigger words (keywords/intent scenarios)
- **Standardized Structure**: All skills now follow consistent section ordering: Overview → Quick Start → When to Use → Instructions → Examples → Troubleshooting → References
- **Enhanced Discoverability**: Descriptions optimized with explicit trigger words for improved Claude Search discovery

### Fixed

- **Missing Description Components**: Fixed 6 skills missing description components (`cc10x-orchestrator`, `context-preset-management`, `parallel-agent-dispatch`, `project-context-understanding`, `skill-discovery`, `verification-before-completion`)

## [4.3.7] - 2025-01-29

### Added

- **Progressive Disclosure**: Refactored 5 large skills (>400 lines) with progressive disclosure architecture:
  - `deployment-patterns` (557 → 187 lines + 4 reference files)
  - `systematic-debugging` (489 → 230 lines + 3 reference files)
  - `root-cause-analysis` (511 → 197 lines + 3 reference files)
  - `component-design-patterns` (495 → 173 lines + 3 reference files)
  - `risk-analysis` (493 → 150 lines + 4 reference files)
- **Iron Law Statements**: Added Iron Law enforcement statements to key skills:
  - `deployment-patterns`: "NO DEPLOYMENT WITHOUT VERIFICATION FIRST"
  - `systematic-debugging`: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"
  - `review-workflow`: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
  - `verification-before-completion`: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
  - `skill-authoring`: "NO SKILL WITHOUT IDENTIFYING FAILURE PATTERNS FIRST"
- **Decision Trees**: Added decision trees to all workflow skills for clear navigation:
  - `review-workflow`, `debug-workflow`, `build-workflow`, `planning-workflow`
- **Red Flags Sections**: Added red flags sections to prevent common mistakes:
  - `deployment-patterns`, `systematic-debugging`
- **Skill Reference Analyzer**: Added script to analyze skill references and build dependency tree
- **Dependency Tree Visualization**: Generated ASCII tree visualization of all skill/workflow connections

### Changed

- **Token Efficiency**: Reduced entry point sizes to ~200 lines with progressive disclosure
- **Reference Files**: Created focused reference files (200-300 lines each) for detailed guidance
- **Workflow Skills**: Enhanced with decision trees and Iron Law statements

### Fixed

- **No Orphaned Skills**: Verified all skills are referenced in correct workflows
- **No Orphaned Subagents**: Verified all subagents are referenced in workflows

## [4.3.6] - 2025-01-29

### Fixed

- **Hook Execution Order**: Fixed critical bug where snapshots were filled but never loaded into context after compaction. Post-compact hook now loads and outputs snapshot content as additionalContext.
- **JSON Escaping**: Fixed error-prone manual sed/awk JSON escaping in post-compact.sh. Now uses proper jq or Python json.dumps() for reliable JSON output.
- **Error Handling**: Added comprehensive error handling for mktemp, mv operations, and checkpoint extraction with fallback mechanisms.
- **Hook Timeouts**: Increased timeout values for pre-compact.sh and post-compact.sh from 3000ms to 5000ms to accommodate complex file I/O operations.

### Changed

- **Post-Compact Hook**: Enhanced to load snapshot content after filling and output as JSON additionalContext, ensuring snapshots are injected into context after compaction.
- **Hook Error Handling**: Improved resilience with fallback mechanisms for all critical operations.

## [4.3.3] - 2025-01-29

### Added

- **Auto-Fill Snapshots**: Post-compact hook now automatically fills snapshot templates with actual context from workflow checkpoints (feature name, phase, progress, completions, next steps)
- **Plan Reference System**: Plan workflow now creates `.claude/memory/current_plan.txt` reference file pointing to plan location for build workflow access
- **Plan Access Priority Order**: Build workflow now checks plan location in priority order: current_plan.txt → WORKING_PLAN.md → docs/plans/ → snapshot
- **Active Plan Display**: Session start hook now displays active plan path if available

### Changed

- **Post-Compact Hook**: Enhanced to extract context from workflow checkpoints and fill snapshot placeholders with actual values using Python-based replacement
- **Plan Workflow Phase 6**: Added mandatory plan saving instructions with bash example for creating plan reference file
- **Build Workflow Phase 2**: Added comprehensive plan access section with priority order and helper function
- **Memory Integration Docs**: Added plan saving pattern and plan reference pattern documentation with priority order

### Fixed

- **Snapshot Templates**: Fixed issue where snapshots remained as templates with placeholders instead of being filled with actual context
- **Plan Folder Disconnect**: Fixed critical flaw where plans saved to `.claude/docs/plans/` were not accessible to build workflow (now uses current_plan.txt reference)

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
