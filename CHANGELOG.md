# Changelog

## [6.0.19] - 2026-02-15

### Added

- **Multi-Signal Scoring** (code-reviewer agent + code-review-patterns skill)
  - Review passes now produce per-dimension HARD/SOFT signals (Security, Correctness, Performance, Maintainability, UX)
  - HARD:0 on any dimension = CONFIDENCE:0 regardless of other scores
  - Router can create targeted REM-FIX tasks ("Fix security" not "Fix something")
  - Inspired by Babysitter's `score.md` per-signal rubric

- **Evidence Array Protocol** (verification skill + integration-verifier + component-builder)
  - Every PASS/APPROVE claim must include structured `EVIDENCE:` block
  - Format: `[command] → exit [code]: [result summary]`
  - SCENARIOS_PASSED count must match EVIDENCE entries — mismatch = INVALID
  - Eliminates vibes-based completion claims

- **Decision Checkpoints** (component-builder + planner + bug-investigator)
  - Mandatory AskUserQuestion triggers: >3 files beyond plan, pattern choices, API contract breaks, new dependencies
  - Planner marks `[CHECKPOINT]` decisions in plan output — pre-approved during BUILD
  - Bug-investigator pauses when hypothesis confidence gap <20 between H1/H2

- **Completion Guard** (verification skill + integration-verifier)
  - Final 4-point gate before Router Contract emission: acceptance criteria, evidence array, no stubs, fresh verification
  - Integration-verifier adds pre-completion checklist: scenarios count, orphan processes, stub scan, build check, goal-backward

### Notes

- ADJACENT risk level — no router, task protocol, agent chain, or memory anchor changes
- 7 files changed, 158 insertions, 0 deletions (pure additions)
- Smoke test: 42/42 passed
- All edited files remain under 500-line soft cap
- Inspired by competitive analysis of a5c-ai/babysitter orchestration framework

## [6.0.18] - 2026-02-04

### Added

- **Complementary Skills Handoff** (Router + All 6 Agents)
  - Router now reads CLAUDE.md Complementary Skills table and passes matching skills to agents via SKILL_HINTS
  - All 6 agents now have explicit `## SKILL_HINTS (If Present)` section
  - Agents invoke skills via `Skill(skill="{name}")` after memory load
  - Fixes gap where complementary skills (react-best-practices, mongodb-agent-skills) weren't reaching subagents

### Changed

- Router: +1 line - "Also check CLAUDE.md Complementary Skills table and include matching skills in SKILL_HINTS"
- All agents: +3 lines each - SKILL_HINTS section with invoke instruction

### Notes

- Based on Vercel article: passive context (CLAUDE.md) beats active retrieval
- Router can see CLAUDE.md (runs in main Claude context), subagents cannot
- This bridges the gap: Router reads → passes to agents → agents invoke

## [6.0.17] - 2026-02-04

### Added

- **Planner Clarification Gate** (planner.md)
  - Planner now asks clarifying questions BEFORE planning when requirements are ambiguous
  - Decision table: vague idea → AskUserQuestion, multiple interpretations → AskUserQuestion with options
  - If 3+ questions needed → invokes brainstorming skill for structured discovery

- **Circuit Breaker Research Option** (cc10x-router)
  - When 3+ remediations fail, "Research best practices" is now the recommended first option
  - Triggers `github-research` skill to find external patterns before retrying
  - Options: Research (recommended) / Fix locally / Skip / Abort

### Notes

- ADJACENT risk level (no router decision tree or agent chain changes)
- 2 files changed: planner.md, cc10x-router/SKILL.md
- Fixes gap where AI wouldn't ask clarifying questions

## [6.0.16] - 2026-02-04

### Fixed

- **SKILL_HINTS now MUST be invoked** (Router)
  - Changed: "Load IMMEDIATELY after memory" → "INVOKE via Skill() - not optional"
  - Added explicit instruction: "Call `Skill(skill='{skill-name}')` immediately after memory load"
  - Fixes bug where agents received hints but didn't invoke complementary skills (react-best-practices, mongodb-agent-skills)

- **Plans include Recommended Skills for BUILD** (Planner)
  - Plan output now lists skills component-builder should invoke
  - Example: React/Next.js → `Skill(skill="react-best-practices")`
  - Double safety: Skill invocation in plan + explicit SKILL_HINTS instruction

### Notes

- ADJACENT risk level (no router decision tree, agent chain, or task protocol changes)
- 2 files changed: cc10x-router/SKILL.md, planner.md
- ~8 lines added total
- Version sync: plugin.json, README.md, CHANGELOG.md all aligned to 6.0.16

## [6.0.15] - 2026-02-03

### Added

- **User Confirmation Gate** (github-research)
  - Asks user before any research: "Do you want me to research GitHub and web for this task?"
  - Bypass conditions: User said "research", debug workflow with 3+ failures
  - Prevents unwanted research delays - user controls external calls

- **Parallel Search Chain** (github-research)
  - Tier 1: Octocode + Bright Data execute in SAME message (parallel)
  - Different strengths: Octocode for real code, Bright Data for docs/tutorials
  - Merge strategy: Code patterns from Octocode, context/warnings from Bright Data

- **3-Tier Fallback System** (github-research)
  - Tier 1: Parallel Search (Octocode + Bright Data MCP)
  - Tier 2: Native Claude Code (WebSearch + WebFetch) if MCP unavailable
  - Tier 3: Ask User for Context if all automated sources fail
  - Graceful degradation - never fails silently

- **New Tools Added** (github-research frontmatter)
  - `WebSearch` - Native Claude Code fallback
  - `AskUserQuestion` - User gate + final fallback
  - `mcp__brightdata__search_engine` - Google/Bing search
  - `mcp__brightdata__scrape_as_markdown` - Doc scraping

### Notes

- ADJACENT risk level (skill-only change, no router/agent chain modifications)
- No Bible invariants affected
- User experience improvement: Research happens when user wants it

## [6.0.14] - 2026-02-03

### Changed

- **Simplified Skill Loading** (All 6 Agents + Router + Bible)
  - Moved domain skills (frontend-patterns, architecture-patterns) to agent frontmatter
  - Removed redundant SKILL_HINTS for skills now preloaded via frontmatter
  - Only `github-research` remains conditional via SKILL_HINTS (external API cost)
  - Updated agents: code-reviewer, silent-failure-hunter, integration-verifier (added domain skills)
  - Updated agents: bug-investigator, planner (removed github-research from frontmatter)
  - Updated router: Simplified SKILL_HINTS table to github-research only
  - Updated Bible: 3 sections updated to reflect simplified model

### Rationale

- SKILL_HINTS keyword detection was fragile (could miss patterns)
- Skills are guidance, not commands - irrelevant parts ignored by agent
- One loading mechanism (frontmatter) is simpler than two (frontmatter + hints)
- github-research stays conditional to avoid unnecessary external API calls

### Fixed

- Removed human-oriented version notes from AI instructions (router and Bible)
  - Removed "v6.0.13+" notes and "Simplified Loading" subsection
  - AI instructions should state current facts, not version history

### Notes

- CRITICAL risk level change, but only removes redundancy
- Smoke test: All checks pass
- No Bible invariants affected (skill loading is documented, not invariant)

## [6.0.13] - 2026-02-03

### Fixed

- **FLAW-16: Task Status Update Unreliability** (Router + All 6 Agents)
  - Router now owns task status updates - calls `TaskUpdate(completed)` after agent returns
  - Agents no longer call TaskUpdate for their own task (unreliable in sub-agent context)
  - Based on Claude Code sub-agent research: Task() return is the deterministic handoff point
  - Updated: Router lines 372, 589 + all 6 agent Task Completion sections

- **FLAW-18: Remediation Re-Review Logic in Prose** (Router)
  - Replaced dense paragraphs with pseudocode flowchart
  - AI can execute pseudocode more reliably than prose
  - Updated: Router lines 475-495

### Changed

- **Bible + Logic Analysis docs updated** to reflect new task status ownership
  - Bible: Lines 110, 113, 399
  - Logic Analysis: Lines 235, 493, 509

### Notes

- Both fixes are ADJACENT risk level (no chain/DAG changes)
- 10 flaws remaining (was 12)
- Research: Sub-agents run in isolated context; don't rely on sub-agent bookkeeping

## [6.0.12] - 2026-02-02

### Added

- **LSP Tool Support Expanded** (7 skills, 3 agents)
  - Added LSP to `code-review-patterns`, `debugging-patterns`, `architecture-patterns` (with usage guidance sections)
  - Added LSP to `frontend-patterns`, `code-generation`, `planning-patterns`, `verification-before-completion`
  - All 6 agents already had LSP - now skills guide usage

- **Git Bisect Example** (debugging-patterns)
  - Full step-by-step workflow for "it worked before" scenarios
  - Includes automated bisect with test command

- **architecture-patterns Skill** (component-builder agent)
  - Added to component-builder frontmatter skills for backend work support

### Notes

- All changes are ADJACENT risk level (safe patterns)
- Smoke test: 19/19 passed
- No Bible invariants affected

## [6.0.11] - 2026-02-02

### Fixed

- **FLAW-20: "Active Decisions" Documentation Drift** (session-memory)
  - 11 references to "Active Decisions table" → "Decisions section"
  - Aligns with actual template that uses `## Decisions`

- **FLAW-21: Canonical Sections Documentation Drift** (session-memory + router)
  - Line 361: Old sections (`## Plan Reference`, etc.) → correct sections (`## References`, `## Decisions`)
  - Router: "Research References table" → "References section"
  - Aligns with merged `## References` section in template

### Notes

- Documentation-only fixes (no functional changes)
- Bible already aligned with source of truth (no changes needed)
- Source of truth: `plugins/cc10x/agents/` + `plugins/cc10x/skills/` as harmonized system

## [6.0.10] - 2026-02-02

### Fixed

- **FLAW-15: Plan Reference Section Mismatch** (Router)
  - Router now looks for `## References` + `- Plan:` instead of old `## Plan Reference` format
  - Fixes plan detection that was silently failing

- **FLAW-16: Agent Follow-up Task Naming** (All 5 Agents + Router)
  - All agents now use `CC10X TODO:` prefix for follow-up tasks
  - Router has new TODO handling section (lines 553-571)
  - User gets visibility + control over non-blocking discoveries

- **FLAW-17: Task Owner Check** (Bible)
  - Removed owner check from task availability criteria (CC10x doesn't use owners)

- **FLAW-18: planning-patterns Outdated Anchor** (planning-patterns)
  - Changed `## Active Workflow Tasks` → `## Tasks` to match session-memory template

- **FLAW-19: integration-verifier Non-namespaced Task** (integration-verifier)
  - Added `CC10X TODO:` prefix for verification failure tasks

### Changed

- **Bible Task Types Table** expanded to show ALL task prefixes
- **7 total flaws now fixed** (1, 2, 15, 16, 17, 18, 19)

### Notes

- External AI review validated orchestration - 5/6 claims were real issues
- All functional files, agents, skills, router, and Bible now perfectly aligned
- Zero risk of Edit anchor failures or orphaned tasks

## [6.0.9] - 2026-02-01

### Added

- **Code Review Patterns Enhancement** (308 → 324 lines)
  - **Pattern Recognition Criteria**: 4 criteria for identifying undocumented conventions during reviews (Tribal, Opinionated, Unusual, Consistent)
  - Guidance for documenting discovered patterns in CLAUDE.md or standards

### Notes

- SAFE edit to existing skill (no orchestration impact)
- Improvement extracted from `agent-os` reference audit
- File remains well under 500-line limit (324 lines)
- Follows cc10x-orchestration-safety protocol (edit-only, no new files)

## [6.0.8] - 2026-02-01

### Added

- **Debugging Patterns Enhancement** (436 → 469 lines)
  - **Meta-Debugging: Your Own Code**: Mindset for debugging code you wrote (fighting your own mental model)
  - **When to Restart Investigation**: 5 criteria for starting over (2+ hours stuck, 3+ failed fixes, can't explain behavior, debugging the debugger, fix works but don't know why) plus restart protocol

- **Verification Enhancement** (355 → 398 lines)
  - **Export/Import Verification**: Scripts to check that exports are actually imported AND used (not just imported)
  - **Auth Protection Verification**: Scripts to verify sensitive routes check authentication

### Notes

- All changes are SAFE edits to existing skills (no orchestration impact)
- Improvements extracted from `get-shit-done` reference audit
- All files remain under 500-line limit
- Follows cc10x-orchestration-safety protocol (edit-only, no new files)

## [6.0.7] - 2026-02-01

### Added

- **TDD Skill Enhancements** (386 → 470 lines)
  - **Coverage Threshold**: 80%+ coverage target for branches, functions, lines, statements
  - **Test Smells Table**: 8 anti-patterns with examples and fixes (testing implementation, dependent tests, mocking everything, giant setup, magic numbers, test name lies, no assertions, commented tests)
  - **Mocking Examples**: Common mock patterns for Supabase, Fetch/API, Redis, environment variables, and time

- **Debugging Patterns Enhancement** (399 → 436 lines)
  - **Build & Type Errors Quick Reference**: 9 common TypeScript/build error patterns with causes and fixes
  - **Minimal Diff Strategy**: Explicit guidance on fixing without over-engineering
  - **Build Error Priority Table**: CRITICAL/HIGH/MEDIUM severity classification

- **Code Review Security Enhancement** (266 → 308 lines)
  - **Security Quick-Scan Commands**: 4 bash commands to detect hardcoded secrets, SQL injection risks, dangerous patterns, and console.log
  - **Critical Security Patterns Table**: 6 patterns with risk, detection, and fix guidance
  - **OWASP Top 10 Quick Reference**: Complete list for easy reference

### Notes

- All changes are SAFE edits to existing skills (no orchestration impact)
- Improvements extracted from `everything-claude-code` reference audit
- All files remain under 500-line limit
- Follows cc10x-orchestration-safety protocol (edit-only, no new files)

## [6.0.6] - 2026-02-01

### Added

- **Enhanced Frontend Patterns Skill** (582 lines, was 396)
  - Extracted best practices from Vercel Web Interface Guidelines, Anti-AI Slop SKILL, and UI/UX Pro Max
  - New sections:
    - **Design Thinking (Pre-Code)**: Purpose, Tone, Constraints, Differentiation framework
    - **Motion & Animation**: `prefers-reduced-motion`, compositor-friendly properties, timing rules
    - **Typography Rules**: Ellipsis, curly quotes, non-breaking spaces, `tabular-nums`, `text-wrap: balance`
    - **Content Overflow Handling**: `truncate`, `line-clamp`, `min-w-0` for flex children
    - **Form Best Practices**: `autocomplete`, `inputMode`, never block paste, spellcheck off
    - **Spatial Composition**: Asymmetry, overlap, diagonal flow, grid-breaking, negative space
    - **Anti-patterns Blocklist**: 11 concrete items to flag with fixes
    - **Light/Dark Mode**: Contrast rules, opacity values, `color-scheme`, `theme-color`
    - **Performance Rules**: Virtualization, lazy loading, preconnect, font preload
    - **URL & State Management**: Deep-linking, query params for filters/tabs/pagination
    - **Touch & Mobile**: 44px targets, `touch-action`, `overscroll-behavior`, safe areas
  - Expanded Visual Creativity with icons (SVG only, no emoji), cursor, hover, backgrounds
  - Expanded Final Check with 5 additional verification items

### Changed

- **Frontend Patterns Skill** now covers comprehensive UI/UX guidelines from multiple industry sources
- Follows cc10x-orchestration-safety protocol (edit-only, no new files)

## [6.0.5] - 2026-01-31

### Changed

- **Ultra-Conservative Skill Cleanup**
  - Removed only 3 truly redundant sections (-41 lines total)
  - session-memory: Removed "The Bottom Line" (restates Iron Law)
  - planning-patterns: Removed "Remember" (repeats earlier content)
  - debugging-patterns: Removed "Real-World Impact" (statistics don't affect AI)

### Preserved

- All philosophical statements ("Violating the letter is violating the spirit")
- All "Why This Matters" sections (provide context for rules)
- All conceptual frameworks (Context Tiers, Quick Index, etc.)
- All Rationalization Prevention tables
- All Bible-mandated content (100%)

## [6.0.4] - 2026-01-31

### Added

- **Debug Attempt Tracking Format** (FLAW 8 Fix)
  - Explicit `[DEBUG-N]:` format for tracking debugging attempts in activeContext.md
  - Router counts lines matching `[DEBUG-N]:` pattern to trigger external research after 3+ failures
  - Bug-investigator documents required format with examples
  - Session-memory template includes format placeholder

### Changed

- **Router** (cc10x-router/SKILL.md:214-223)
  - Added "Debug Attempt Counting" section with format specification
  - Added "What counts as an attempt" clarification (hypothesis tested with code change, NOT reading/thinking)

- **Bug-Investigator** (bug-investigator.md:93-108)
  - Added "Debug Attempt Format (REQUIRED for DEBUG workflow)" section
  - Includes examples and explains why format is needed

- **Session-Memory** (session-memory/SKILL.md:381)
  - Added `[DEBUG-N]:` format to Recent Changes template

### Fixed

- **Research trigger undefined** (FLAW 8)
  - Root cause: "3+ local debugging attempts failed" had no defined format
  - Solution: `[DEBUG-N]: {what was tried} → {result}` format enables reliable counting

## [6.0.3] - 2026-01-31

### Added

- **Stable Anchor Registry** (session-memory)
  - Defined 7 guaranteed anchors: `## Recent Changes`, `## Learnings`, `## References`, `## Last Updated`, `## Common Gotchas`, `## Completed`, `## Verification`
  - Explicit guidance: NEVER use table headers or checkbox text as anchors

- **Read-Edit-Verify Pattern** (MANDATORY)
  - 4-step sequence: Read → Verify Anchor → Edit → Verify Change
  - Added to session-memory and all agent files
  - Prevents "Error editing file" by ensuring anchors exist before use

- **Extended Template Validation Gate** (Router)
  - Now validates all canonical sections in activeContext.md and progress.md
  - Auto-heals any missing sections using `## Last Updated` fallback

### Changed

- **activeContext.md Template** (12 → 8 sections)
  - Merged: `## Active Decisions` + `## Learnings This Session` → `## Decisions` + `## Learnings`
  - Merged: `## Plan Reference` + `## Design Reference` + `## Research References` → `## References`
  - Removed: `## User Preferences Discovered` (goes in Learnings)

- **progress.md Template** (8 → 5 sections)
  - Merged: `## Active Workflow Tasks` + `## In Progress` + `## Remaining` → `## Tasks`
  - Changed: `## Verification Evidence` table → `## Verification` bullets
  - Removed: `## Known Issues`, `## Evolution of Decisions`, `## Implementation Results`

- **Skills** (Table → Bullet Anchors)
  - github-research: Changed from table header to `## References` anchor
  - planning-patterns: Changed from `## Plan Reference` to `## References` anchor
  - brainstorming: Changed from `## Design Reference` to `## References` anchor

- **All Agents** (R-E-V Reminder)
  - Added "Memory Updates (Read-Edit-Verify)" section with stable anchors list
  - component-builder, bug-investigator, planner, integration-verifier, code-reviewer

### Fixed

- **"Error editing file" on Memory Operations**
  - Root cause: 14 different Edit anchors, many brittle (table headers, optional sections)
  - Solution: 7 stable anchors guaranteed to exist + Read-Edit-Verify pattern

### Notes

- Reduced anchor count from 14 to 7 (50% reduction)
- All table-header anchors eliminated
- Backward compatible: Template Validation Gate auto-heals old projects

## [6.0.2] - 2026-01-31

### Added

- **Template Validation Gate** (Router - Backward Compatibility Fix)
  - Router now auto-heals old projects by adding missing canonical sections
  - Checks for `## Plan Reference`, `## Design Reference`, `## Research References` after loading memory
  - If missing, inserts them before `## Last Updated` using a single Edit operation
  - Idempotent: runs once per project (subsequent sessions find sections present)

### Fixed

- **Silent Edit Failures on Old Projects**
  - v6.0.1 introduced targeted Edit anchors (e.g., `old_string="## Plan Reference"`)
  - Projects created before v6.0.1 lacked these sections, causing Edits to fail silently
  - Template Validation Gate ensures anchors exist before any skill tries to use them

### Notes

- This is a backward compatibility fix for projects migrating from pre-6.0.1 versions
- New projects are unaffected (templates already include canonical sections)

## [6.0.1] - 2026-01-31

### Added

- **Parallel-Safety Rules** (fixes FLAW 5 - memory race condition)
  - Router now instructs: "Avoid memory edits during parallel phases"
  - code-reviewer has explicit parallel-safety rule for BUILD workflow
  - Memory updates deferred to workflow-final checkpoint

- **Memory Update Targets** (all agents)
  - Each agent now has explicit guidance on which files/sections to update
  - Reduces ambiguity and prevents over-writing

- **Session Memory "Guts" Documentation**
  - Added "What Memory Actually Is" section explaining memory surfaces
  - Added Promotion Ladder (observation → pattern → artifact → evidence)
  - Added Ownership rules (who reads/writes)
  - Added Concurrency Rule for parallel phases

- **Canonical Sections in activeContext.md template**
  - `## Plan Reference` and `## Design Reference` now in template
  - Ensures Edit anchors exist for all new projects

### Changed

- **Agent Tools**
  - code-reviewer: `Write` → `Edit` (proper tool for memory updates)
  - integration-verifier: `Write` → `Edit`
  - planner: added `Edit` tool

- **Agent Modes**
  - code-reviewer: READ-ONLY for repo code (memory edits still allowed)
  - integration-verifier: READ-ONLY for repo code
  - planner: READ-ONLY for repo code (plan files + memory still writable)

- **Memory Loading**
  - All agents now read all 3 memory files (activeContext, patterns, progress)
  - Previously some agents only read 1-2 files

- **Edit Patterns**
  - brainstorming/planning-patterns: changed from whole-file replacement to small targeted edits
  - github-research: Edit anchor changed to table header row for stability

### Notes

- This release completes the FLAW 5 fix from the orchestration analysis
- Small targeted edits require canonical sections to exist (handled by updated templates)

## [6.0.0] - 2026-01-31

### Added

- **Tasks Contract Hardening (official-schema aligned)**
  - CC10X Tasks are now namespaced (subjects prefixed with `CC10X ...`) to prevent collisions and enable safer resumption.
  - Router notes official task-list sharing via `CLAUDE_CODE_TASK_LIST_ID` and treats TaskLists as potentially long-lived.

- **Task-Enforced Orchestration Gates (Flaw 4)**
  - Missing critical evidence now creates a `CC10X REM-EVIDENCE:` task and blocks downstream tasks via `addBlockedBy`.
  - Critical issues now create `CC10X REM-FIX:` tasks and block downstream tasks.
  - BUILD workflows enforce a **re-review loop after remediation** (re-run reviewer + hunter before integration verification).

### Changed

- Router + planning skills no longer rely on undocumented TaskCreate fields (e.g., `metadata`).
- Task examples standardized to canonical object-form calls (e.g., `TaskUpdate({ taskId: ..., status: \"...\" })`).

### Notes

- This release hardens orchestration reliability; it is intentionally strict to protect the system.

## [5.25.3] - 2026-01-30

### Added

- **Anti-Hardcode Gate** (bug-investigator)
  - Variant scan required before fixing (locale/config/roles/runtime/time/data/concurrency/network/cache)
  - Regression tests must cover at least one non-default variant when applicable

### Changed

- bug-investigator now **TDD-first** for DEBUG:
  - RED regression test before fix, GREEN after
  - Output requires TDD evidence + variant coverage summary
- Router validation requires bug-investigator TDD evidence + variant coverage before proceeding

### Notes

- No changes to task DAGs or workflow order
- Router change is validation-only (evidence gate)

## [5.25.2] - 2025-01-29

### Added

- **Iterative Retrieval Pattern** (stolen from Everything Claude Code)
  - Added to bug-investigator: Context Retrieval step for large codebase debugging
  - Added to planner: Context Retrieval step before designing features
  - Pattern: DISPATCH (broad) → EVALUATE (score 0-1) → REFINE (narrow) → LOOP (max 3)
  - Stop condition: 3+ files with relevance ≥0.7 AND no critical gaps

### Changed

- bug-investigator Process section: Steps renumbered (new step 3, old 3-8 → 4-9)
- planner Process section: Steps renumbered (new step 2, old 2-6 → 3-7)

### Notes

- Zero orchestration impact: Pure guidance content in SAFE zones
- No changes to: router, agent chains, output formats, task system

## [5.25.1] - 2025-01-29

### Added

- **Wiring Verification Patterns** (verification-before-completion skill)
  - Component → API check: grep patterns to verify fetch calls exist and response is used
  - API → Database check: grep patterns to verify queries exist and results are returned
  - Red flags table for common wiring stubs
  - Line count minimums by file type (Component: 15, API: 10, Hook: 10)

- **Hypothesis Quality Criteria** (debugging-patterns skill)
  - Falsifiability requirement: "A good hypothesis can be proven wrong"
  - Bad vs Good hypothesis examples (vague → specific)
  - Cognitive biases table: Confirmation, Anchoring, Availability, Sunk Cost with antidotes

### Changed

- Enhanced stub detection with GSD-inspired wiring verification patterns
- Enhanced debugging guidance with scientific hypothesis criteria

## [5.25.0] - 2025-01-29

### Added

- **Plan File Propagation (FIX 1)**: Router now passes `Plan File:` explicitly in agent prompt
  - component-builder checks prompt's Task Context for plan file path
  - No longer relies on inaccessible task metadata

- **Results Collection (FIX 2)**: New pattern for parallel agent output passing
  - Router collects code-reviewer + silent-failure-hunter findings
  - Passes merged findings to integration-verifier in prompt
  - Task system handles coordination, router handles content

- **Skill Loading Hierarchy (FIX 3)**: Documented 3-tier skill loading priority
  - Tier 1: Agent frontmatter `skills:` (automatic preload)
  - Tier 2: Router's SKILL_HINTS (mandatory, agent must load)
  - Tier 3: Agent's Skill Triggers (optional, agent judgment)

- **Enhanced Post-Agent Validation (FIX 4)**: Structured validation with required sections table
  - Per-agent required sections and evidence documented
  - Options: create remediation task OR ask user
  - Soft validation to avoid breaking workflows

### Changed

- **Agent Invocation Template**: Restructured with clear markdown sections
  - Task Context, User Request, Requirements, Memory Summary, Project Patterns, SKILL_HINTS
  - Consistent format across all agent invocations

- **README Redesign**: Complete visual overhaul as landing page
  - Strong positioning vs bloated plugins (50+ skills, 30+ agents problem)
  - Visual flow diagram showing orchestration
  - Side-by-side comparison (without vs with cc10x)
  - Collapsible version history

## [5.24.1] - 2025-01-28

### Fixed

- **Research Persistence** - Added atomic checkpoint guidance to `github-research/SKILL.md`
  - Documentation reminder to save research + update memory sequentially
  - Prevents research files from becoming orphaned during context compaction

- **TDD Evidence Template** - Enhanced `component-builder.md` output format
  - Output template now includes exit code evidence for RED (exit 1) and GREEN (exit 0) phases
  - Builder self-enforces TDD discipline through structured output

- **Plan Reading Discipline** - Added plan-reading reminder to `component-builder.md`
  - Builder reads plan file when provided (legacy references to `metadata.planFile` are deprecated as of v6.0.0)
  - Self-enforced responsibility (no external validation)

- **Silent Failure Hunter** - Enhanced `silent-failure-hunter.md` with active fixing
  - Changed from read-only to active fixer for CRITICAL silent failures
  - Empty catch blocks and silent failures fixed immediately, not deferred
  - HIGH/MEDIUM issues still create follow-up tasks

- **Rollback Strategy** - Added rollback decision tree to `integration-verifier.md`
  - Three explicit options when verification fails: Create Fix Task, Revert Branch, or Document & Continue
  - Prevents broken state from being left unaddressed

- **DEBUG Research Triggers** - Aligned DEBUG workflow research triggers in `cc10x-router/SKILL.md`
  - Added missing "3+ local debugging attempts failed" trigger
  - Now consistent with skill trigger table

### Removed

- **Router Post-Agent Validation** - Removed from `cc10x-router/SKILL.md`
  - Router is a one-shot starter, not a persistent orchestrator
  - Cannot validate agent outputs after invocation (architectural reality)
  - Agent self-discipline is the enforcement mechanism

### Changed

- **Agent Self-Enforcement Approach**: All agent improvements rely on self-discipline
  - Gates and checklists are for agents to follow, not router to enforce
  - Router starts workflow, agents are responsible for quality

## [5.24.0] - 2025-01-27

### Added

- **Research Documentation Persistence**: Research insights no longer lost after context compaction
  - `github-research` skill: Added mandatory 4-step save process
  - `cc10x-router`: Added `RESEARCH_PERSISTED` gate to workflows
  - `session-memory`: Added Research References table to activeContext template
  - Research saved to `docs/research/YYYY-MM-DD-topic-research.md`
  - Auto-extraction of gotchas to `patterns.md` with source tracking

### Changed

- **THREE-PHASE Research Pattern**: Replaced TWO-PHASE with persistence step
  - Phase 1: Execute research (octocode tools)
  - Phase 2: PERSIST to docs/research/ + update memory
  - Phase 3: Pass results to agent

## [5.23.0] - 2025-01-27

### Added

- **Plan-Task Linkage (legacy; deprecated in v6.0.0)**: Tasks included `metadata.planFile` for context recovery
  - BUILD workflow tasks referenced plan file in description and metadata
  - Enables agents to access original plan during execution
  - Supports resume capability with full plan context

## [5.22.0] - 2025-01-25

### Added

- **Stub Detection Patterns**: Added to verification-before-completion skill
  - Universal stubs: TODO/FIXME markers, empty returns
  - React component stubs: placeholder divs, no-op handlers
  - API route stubs: unimplemented responses, empty JSON
  - Function stubs: throw errors, debug artifacts
  - Quick stub check bash commands for pre-completion scanning

## [5.21.0] - 2025-01-25

### Added

- **Tasks System Integration**: Replaced text-based workflow signals with Anthropic's new Tasks system
  - Router creates task hierarchy with `TaskCreate` at workflow start
  - Agents call `TaskUpdate(status="completed")` when done
  - Dependencies managed via `blockedBy` for proper chain execution
  - `TaskList()` check at startup enables resume capability across sessions

- **Task-Based Orchestration**: New orchestration pattern for all 4 workflows
  - BUILD: component-builder → [code-reviewer ∥ silent-failure-hunter] → integration-verifier
  - DEBUG: bug-investigator → code-reviewer → integration-verifier
  - REVIEW: code-reviewer (single agent)
  - PLAN: planner (single agent)

- **Chain Execution Loop**: Task-based execution replacing text signal parsing
  - Parallel execution when multiple tasks unblocked simultaneously
  - Sync points via blockedBy dependencies
  - Clear completion criteria: all tasks status="completed"

- **New Gates**: TASKS_CHECKED, TASKS_CREATED, ALL_TASKS_COMPLETED

### Removed

- **Text-Based Workflow Signals**: Removed from all 6 agents
  - WORKFLOW_CONTINUES, NEXT_AGENT, PARALLEL_AGENTS
  - PARALLEL_COMPLETE, SYNC_NEXT, CHAIN_PROGRESS, CHAIN_COMPLETE

### Changed

- **Agent Output Format**: Simplified to Summary, Changes, Findings, Task Status
- **planning-patterns**: Added Task-Based Execution Tracking section
- **session-memory**: Added Active Workflow Tasks table to progress.md structure

## [5.20.0] - 2025-01-20

### Added

- **Goal-Backward Lens**: Added to verification-before-completion skill
  - TRUTHS: What observable user-facing behaviors exist?
  - ARTIFACTS: What files, endpoints, tests were created?
  - WIRING: What's connected (component → API → database)?

## [5.19.0] - 2025-01-19

### Added

- **OWASP Top 10 Reference**: Added link to OWASP Top 10 in code-review-patterns Security Review Checklist
- **Minimal Diffs Principle**: Added section to code-generation skill emphasizing focused changes without scope creep
- **Architecture Decision Records (ADR)**: Added ADR pattern template to planning-patterns for documenting architectural decisions

### Notes

- Console.log check already exists in verification-before-completion/SKILL.md:152

## [5.18.0] - 2025-01-14

### Fixed

- **Two-Phase GitHub Research Enforcement**: Fixed critical issue where planner agent was ignoring SKILL_HINTS for github-research
  - Router now executes research FIRST using octocode tools directly (not as advisory hint)
  - Research results are passed to planner/bug-investigator in prompt
  - Research is now a PREREQUISITE, not a hint that can be skipped
  - Added RESEARCH_EXECUTED gate before planner when github-research detected

- **Explicit Research Request Trigger**: Added "research" to router triggers and explicit user request detection
  - Keywords: "research", "github", "octocode", "find on github", "how do others", "best practices"
  - Ensures router activates when user explicitly asks for GitHub research

### Changed

- **github-research Skill Simplified**: Reduced from ~201 lines to ~138 lines (31% smaller)
  - Removed duplicated octocode guidance (octocode MCP handles HOW)
  - Skill now focuses on WHEN to invoke and OUTPUT format for cc10x memory
  - Updated Iron Law: "NO EXTERNAL RESEARCH WITHOUT CLEAR AI KNOWLEDGE GAP OR EXPLICIT USER REQUEST"
  - Updated Integration Points to reflect Two-Phase execution model

- **cc10x-router Workflows**: Updated PLAN and DEBUG workflows
  - PLAN: Execute research FIRST, then invoke planner with results
  - DEBUG: Execute research FIRST for external service errors, then invoke bug-investigator

### Added

- **New SKILL_HINTS Detection Row**: Explicit user request detection for github-research
  - Pattern: User says "research", "github", "octocode", "find on github", "how do others", "best practices"
  - Agents: planner, bug-investigator

## [5.15.0] - 2025-01-11

### Added

- **Token-Aware Memory Efficiency**: Enhanced session-memory skill with guidelines for large memory files
  - Quick Index Pattern: Optional index header for files exceeding 200 lines
  - Selective Loading: Load memory sections on-demand using offset/limit
  - Pruning Guidelines: Keep memory files trim, archive old content

- **Pre-Compaction Memory Safety**: Proactive memory updates to prevent context loss
  - Context Length Awareness: Recognize when sessions are getting long
  - Proactive Update Triggers: Update memory before auto-compact erases context
  - Checkpoint Pattern: Mid-session checkpoints for critical decisions
  - Red Flags table: Clear signals for when to update memory immediately

### Changed

- **session-memory Skill**: Added 146 lines of memory efficiency and safety guidance

## [5.14.0] - 2025-01-10

### Added

- **LSP Tool for All Agents**: Added Language Server Protocol (LSP) tool to all 6 agents
  - Enables go-to-definition, find-references, and hover documentation
  - Enhances code analysis capabilities for all workflows
  - Particularly valuable for bug-investigator (code path tracing) and code-reviewer (reference tracking)

- **Agent Context Isolation**: Added `context: fork` to all 6 agents
  - Each agent now runs in an isolated forked context
  - Prevents state leakage between agents in workflow chains
  - Improves reliability of parallel execution (code-reviewer ∥ silent-failure-hunter)

### Changed

- **All 6 Agents Updated**:
  - component-builder: Added LSP, context:fork
  - bug-investigator: Added LSP, context:fork
  - code-reviewer: Added LSP, context:fork
  - silent-failure-hunter: Added LSP, context:fork
  - integration-verifier: Added LSP, context:fork
  - planner: Added LSP, context:fork

### Compatibility

- Requires Claude Code v2.0.74+ for LSP tool support
- Requires Claude Code v2.1.0+ for `context: fork` feature
- Recommended: Claude Code v2.1.3+ for best experience

## [5.11.0] - 2025-01-06

### Fixed

- **Workflow Chain Enforcement**: Fixed critical issue where BUILD workflow stopped after component-builder
  - Root cause: Agent chains were documented but not enforced - Claude had no signal to continue
  - Added `WORKFLOW_CONTINUES` and `NEXT_AGENT` output signals to all agents
  - Added Chain Enforcement section to cc10x-router with explicit continuation rules
  - All 4 workflows now have complete chain coverage (BUILD, DEBUG, REVIEW, PLAN)

### Changed

- **component-builder**: Now outputs `NEXT_AGENT: code-reviewer` after completion
- **code-reviewer**: Context-aware - continues chain in BUILD/DEBUG, ends in REVIEW
- **silent-failure-hunter**: Now outputs `NEXT_AGENT: integration-verifier`
- **integration-verifier**: Outputs `WORKFLOW_CONTINUES: NO` to signal chain completion
- **bug-investigator**: Now outputs `NEXT_AGENT: code-reviewer` for DEBUG workflow
- **planner**: Outputs `WORKFLOW_CONTINUES: NO` (single-agent workflow)
- **cc10x-router**: Added Chain Enforcement section with explicit loop instructions

### Impact

- BUILD workflow now executes full chain: component-builder → [code-reviewer ∥ silent-failure-hunter] → integration-verifier
- DEBUG workflow now executes full chain: bug-investigator → code-reviewer → integration-verifier
- REVIEW and PLAN workflows properly signal completion
- Claude can no longer "forget" to invoke subsequent agents in the chain

## [5.8.1] - 2025-01-XX

### Fixed

- **Router Bypass Prevention**: Strengthened all agent and skill descriptions to explicitly prevent direct invocation
  - Added explicit router references to `integration-verifier` and `silent-failure-hunter` agents
  - Added router workflow context to `session-memory` and `verification-before-completion` skills
  - Enhanced router description as "THE ONLY ENTRY POINT FOR CC10X" with critical warning
  - All 17 components (6 agents + 11 skills) now explicitly prevent direct invocation
  - Production-ready protection against router bypass for millions of users

### Impact

- Zero ambiguity about router being the only entry point
- Explicit prevention of direct agent/skill invocation
- Consistent messaging across all components
- Memory flow integrity guaranteed (router loads memory first, updates last)

## [5.7.1] - 2025-12-21

### Fixed

- **silent-failure-hunter**: Added missing `verification-before-completion` skill
  - Agent audits error handling and reports findings
  - Now verifies findings before reporting (evidence-based)
  - All 5 code-touching agents now have verification skill

### Skill Loading Matrix (Updated)

| Agent | Auto-Loaded Skills |
|-------|-------------------|
| component-builder | session-memory, test-driven-development, code-generation, verification-before-completion |
| bug-investigator | session-memory, debugging-patterns, test-driven-development, verification-before-completion |
| code-reviewer | session-memory, code-review-patterns, verification-before-completion |
| integration-verifier | session-memory, architecture-patterns, debugging-patterns, verification-before-completion |
| silent-failure-hunter | session-memory, code-review-patterns, **verification-before-completion** ← ADDED |
| planner | session-memory, planning-patterns, architecture-patterns |

Note: planner doesn't need verification (creates plans, doesn't verify code)

## [5.7.0] - 2025-12-21

### Fixed

- **Agent Keyword Collision with Router**: Fixed critical issue where agent descriptions had same trigger keywords as cc10x-router, causing Claude to invoke agents directly instead of using workflows
  - **Same bug as v5.5.0 (skills) but for agents**
  - All 6 agents now say "Invoked by X workflow via cc10x-router. DO NOT invoke directly"
  - Removed workflow trigger keywords (build, debug, review, plan, etc.) from agent descriptions
  - Router is now the ONLY entry point - agents are only invoked BY workflows

### Root Cause

When user said "build a task tracker", Claude could match EITHER:
1. cc10x-router skill (keyword: "build") → Correct: Full workflow
2. component-builder agent (keyword: "build") → WRONG: Bypasses router

Claude sometimes picked the agent directly, bypassing:
- Memory loading
- User confirmation gates
- Agent chain (builder → reviewer → verifier)

### Fix Applied

Agents no longer have workflow trigger keywords. Only cc10x-router responds to:
`build, implement, create, make, write, add, develop, code, feature, component, app, application, review, audit, check, analyze, debug, fix, error, bug, broken, troubleshoot, plan, design, architect, roadmap, strategy`

### Agent Description Changes

| Agent | Before | After |
|-------|--------|-------|
| component-builder | "Triggers on build, create, implement..." | "Invoked by BUILD workflow. DO NOT invoke directly" |
| code-reviewer | "Triggers on review, audit, check..." | "Invoked by REVIEW workflow. DO NOT invoke directly" |
| bug-investigator | "Triggers on debug, fix, error, bug..." | "Invoked by DEBUG workflow. DO NOT invoke directly" |
| planner | "Triggers on plan, design, architect..." | "Invoked by PLAN workflow. DO NOT invoke directly" |
| integration-verifier | "Triggers on verify, validate..." | "Invoked by BUILD/DEBUG workflows. DO NOT invoke directly" |
| silent-failure-hunter | "Triggers on error handling, audit errors..." | "Invoked by BUILD/REVIEW workflows. DO NOT invoke directly" |

## [5.6.0] - 2025-12-21

### Fixed

- **Agent Tool Misconfiguration**: Fixed critical issue where agents were missing essential tools
  - **planner**: Was missing Write/Bash - couldn't save plans or run memory commands!
  - **silent-failure-hunter**: Was missing Write/Skill - couldn't update memory or load conditional skills!
  - **code-reviewer**: Was missing Write - couldn't update memory at end of review!
  - **integration-verifier**: Was missing Write - couldn't save verification results!
  - **component-builder**: Was missing Grep/Glob - couldn't search codebase for patterns!

### Changed

- All 6 agents now have consistent tool configuration:
  - **Builders** (component-builder, bug-investigator): Read, Edit, Write, Bash, Grep, Glob, Skill
  - **Analyzers** (code-reviewer, integration-verifier, planner, silent-failure-hunter): Read, Write, Bash, Grep, Glob, Skill
- Edit tool reserved for agents that modify code (builders)
- Write tool for all agents (needed for memory updates)
- Bash tool for all agents (needed for memory load command)

### Agent Tool Matrix

| Agent | Edit | Write | Bash | Grep | Glob | Skill |
|-------|------|-------|------|------|------|-------|
| component-builder | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| bug-investigator | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| code-reviewer | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| integration-verifier | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| planner | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| silent-failure-hunter | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |

## [5.5.0] - 2025-12-20

### Fixed

- **Skill Keyword Conflicts**: Fixed critical issue where individual skills had same trigger keywords as router, causing Claude to match skills directly instead of using router
  - All 9 skills now say "Loaded by X agent. DO NOT invoke directly - use X workflow via cc10x-router"
  - Removed workflow trigger keywords (build, debug, review, plan, etc.) from individual skill descriptions
  - Router is now the ONLY entry point for workflow keywords

### Changed

- **test-driven-development**: Now loaded by component-builder agent only
- **code-generation**: Now loaded by component-builder agent only
- **debugging-patterns**: Now loaded by bug-investigator agent only
- **code-review-patterns**: Now loaded by code-reviewer agent only
- **planning-patterns**: Now loaded by planner agent only
- **brainstorming**: Now loaded by planner agent only
- **frontend-patterns**: Now loaded by code-reviewer agent (for UI code) only
- **architecture-patterns**: Now loaded by planner/code-reviewer agents only
- **verification-before-completion**: Now loaded by ALL agents automatically

### Root Cause

In v5.4.0, when user said "build a task tracker", Claude matched BOTH:
1. cc10x-router (keyword: "build")
2. test-driven-development skill (keyword: "build")

Claude picked the individual skill instead of the router, bypassing workflow orchestration.

### Fix Applied

Skills no longer have workflow trigger keywords. Only cc10x-router responds to:
`build, implement, create, make, write, add, develop, code, feature, component, app, application, review, audit, check, analyze, debug, fix, error, bug, broken, troubleshoot, plan, design, architect, roadmap, strategy`

## [5.4.0] - 2025-12-20

### Fixed

- **Router Auto-Execute Enforcement**: Fixed critical issue where Claude would list cc10x capabilities instead of executing workflows
  - Changed description from passive "should be used" to aggressive "AUTO-LOAD AND EXECUTE"
  - Added "What NOT To Do" section explicitly forbidding capability listing
  - Added 3 execution examples showing the RIGHT way to respond
  - Router now triggers on expanded keywords: app, application, feature, component, develop, code

### Changed

- **Router Title**: Changed from "Simple Workflow Coordination" to "Workflow Execution Engine"
- **Router Behavior**: Now explicitly states "THIS IS AN EXECUTION ENGINE, NOT DOCUMENTATION"
- **Plugin Description**: Updated to emphasize "AUTO-EXECUTE routing (not just describe capabilities)"

### Key Behavior Change

**Before v5.4.0** (WRONG):
```
user: "build a task tracker"
assistant: "cc10x has these capabilities: brainstorming, planning, building..."
```

**After v5.4.0** (CORRECT):
```
user: "build a task tracker"
assistant: "Detected BUILD intent. Executing BUILD workflow.
Loading memory...
Clarifying requirements:
1. What framework?
2. What features?
..."
```

## [5.3.0] - 2025-12-20

### Added

- **Confidence Scoring**: code-reviewer now rates findings 0-100, only reports issues with confidence >= 80
  - Reduces false positives and improves signal-to-noise ratio
  - Self-check questions before reporting any issue
  - Output format includes confidence scores

- **User Confirmation Gates**: BUILD workflow now REQUIRES user confirmation before implementing
  - Phase 1 "CLARIFY REQUIREMENTS" marked as "CRITICAL: DO NOT SKIP"
  - Must present questions to user and wait for answers
  - If user says "whatever you think", state recommendation and get confirmation

- **Git History Context**: code-reviewer checks git blame and recent commits
  - Run `git log --oneline -10 -- <file>` for recent changes
  - Run `git blame <file>` for authorship context
  - Check if similar issues were fixed before
  - Output format includes Git Context section

- **Silent Failure Hunter**: New specialized agent for error handling audits
  - Triggers on "error handling", "audit errors", "catch blocks", "silent failures"
  - Zero tolerance for empty catch blocks, log-only catches, generic error messages
  - Integrated into BUILD workflow (after code-reviewer, if error handling code)
  - Severity rating: CRITICAL / HIGH / MEDIUM / LOW

### Changed

- BUILD workflow: Added clarification step and silent-failure-hunter
- REVIEW workflow: Can now invoke silent-failure-hunter for error handling focus
- code-reviewer output format: Now includes confidence scores and git context
- Intent Detection: Added "error handling, audit errors, catch blocks, silent failures" routing

### Architecture

```
Router (cc10x-router)
    |
    +-- BUILD -> component-builder -> code-reviewer -> silent-failure-hunter -> integration-verifier
    +-- REVIEW -> code-reviewer (or silent-failure-hunter for error focus)
    +-- DEBUG -> bug-investigator -> code-reviewer -> integration-verifier
    +-- PLAN -> planner

Agents (6 total)
    +-- component-builder (TDD cycle)
    +-- code-reviewer (confidence scoring, git context)
    +-- bug-investigator (LOG FIRST)
    +-- integration-verifier (end-to-end)
    +-- planner (architecture, risks)
    +-- silent-failure-hunter (error handling audits) [NEW]
```

## [5.2.0] - 2025-12-20

### Added

- **Session Memory Skill**: New mandatory memory persistence system
  - `session-memory` skill auto-loaded by all 5 agents as FIRST skill
  - Iron Law: LOAD at START, UPDATE at END (both mandatory)
  - Three memory files: `activeContext.md`, `patterns.md`, `progress.md`
  - Persists context across conversation compaction

- **READ Triggers**: Explicit guidance for WHEN to load memory
  - File Selection Matrix (which file for which situation)
  - Decision Integration (check memory before any decision)
  - Read BEFORE actions table (architectural decisions, implementation choices, debugging)
  - READ Red Flags and READ Excuses tables

- **Skills Auto-Loading**: Agents now auto-load skills via frontmatter
  - Added `skills:` field to all 5 agent definitions
  - Skills loaded automatically without manual `Skill()` calls
  - Conditional skills still use `Skill()` tool when needed

- **Tool Restrictions**: Read-only skills now have `allowed-tools`
  - code-review-patterns: Read, Grep, Glob
  - planning-patterns: Read, Grep, Glob
  - brainstorming: Read, Grep, Glob
  - architecture-patterns: Read, Grep, Glob
  - frontend-patterns: Read, Grep, Glob

### Improved

- **Skill Descriptions**: All 9 skills have specific trigger keywords
  - Added "Triggers on:" phrases for better discovery
  - More specific "when to use" guidance

- **Router Workflows**: Enhanced memory operations in all 4 workflows
  - Step 0: LOAD ALL 3 memory files (not just activeContext)
  - CHECK points during workflow (before decisions)
  - Dual verification checklist (READ + WRITE)

- **Agent Consistency**: All agents follow same pattern
  - MANDATORY FIRST: Load Memory section in all agents
  - session-memory as first skill in all agents
  - Conditional skills documented in each agent

### Architecture

```
Router (cc10x-router)
    │
    ├── BUILD → component-builder → code-reviewer → integration-verifier
    ├── REVIEW → code-reviewer
    ├── DEBUG → bug-investigator → code-reviewer → integration-verifier
    └── PLAN → planner

Memory (.claude/cc10x/)
    ├── activeContext.md (current focus, decisions, learnings)
    ├── patterns.md (project conventions, gotchas)
    └── progress.md (completed, remaining, evidence)
```

## [4.8.0] - 2025-11-15

### Added

- **Refactor Comparison Framework**: Comprehensive comparison and ranking system
  - Created measurement tools for all 15 refactor comparison parameters
  - Added comparison scripts to extract metrics from both branches
  - Generated comprehensive ranking reports with detailed analysis
  - All 15 parameters now score 90+ (overall score: 93.57/100)

- **Shared Patterns Library**: Pattern reusability improvements
  - Created `shared-patterns/FUNCTIONALITY-FIRST.md` for common functionality-first pattern
  - Created `shared-patterns/PATTERN-COMPOSITION.md` for pattern composition guidelines
  - Reduces duplication across consolidated skills

- **Pattern Documentation**: Enhanced documentation for consolidated skills
  - Added `PATTERNS.md` to `code-review-patterns` (security, quality, performance patterns)
  - Added `PATTERNS.md` to `debugging-patterns` (systematic debugging, root cause, log analysis)
  - Added `PATTERNS.md` to `planning-patterns` (requirements analysis, feature planning)
  - Added `PATTERNS.md` to `frontend-patterns` (UX, UI design, accessibility)

### Fixed

- **Integration Completeness Measurement**: Fixed false positives
  - Updated integration measurement to exclude subagents from skill validation
  - Added subagent whitelist (code-reviewer, integration-verifier, component-builder, bug-investigator, planner)
  - Added tool whitelist (jq, grep, curl, wget, sed, awk, find, xargs)
  - Score improved from 70.3 → 100

### Improved

- **All Parameters Enhanced**: Comprehensive improvements across all dimensions
  - Integration Completeness: 70.3 → 100 (perfect score)
  - Maintainability: 50.4 → 91.5 (+41.1 points)
  - Documentation Quality: 76.3 → 97.5 (+21.2 points)
  - Performance: 53.5 → 93.55 (+40.05 points)
  - Developer Experience: 61.3 → 91.75 (+30.45 points)
  - Workflow Efficiency: 61.3 → 92.2 (+30.9 points)
  - Extensibility: 60.0 → 100 (perfect score)
  - Architectural Quality: 70.0 → 100 (perfect score)
  - Code Volume: 79.2 → 90.0 (+10.8 points)
  - Error Handling: 85.0 → 92.0 (+7 points)
  - Overall Score: 76.13 → 93.57 (+17.44 points)

## [4.7.0] - 2025-11-13

### Added

- **Complete System Integration**: Perfect integration of all workflows, skills, and subagents
  - Integrated 5 orphan skills into PLAN workflow:
    - `app-design-generation` (conditional skill for app design documents)
    - `tech-stack-generation` (conditional skill for tech stack documentation)
    - `cursor-rules-generation` (conditional skill for cursor rules)
    - `project-structure-generation` (conditional skill for project structure docs)
    - `brainstorming` (conditional skill for requirements refinement)
  - Added skill verification before subagent invocation in all workflows
  - Verified all subagent-skill dependencies are correct

### Fixed

- **Integration Issues**: Fixed all integration gaps
  - Fixed duplicate step numbers in BUILD workflow
  - Ensured all conditional skills are properly detected and loaded
  - Verified all subagent-skill dependencies before invocation
  - Achieved perfect integration: 0 orphan skills, 0 orphan subagents

### Changed

- **Workflow Skill Loading**: Enhanced skill loading verification
  - All workflows now verify required skills are loaded before subagent invocation
  - PLAN workflow: Verifies skills before `planner` subagent
  - REVIEW workflow: Verifies skills before `code-reviewer` and `integration-verifier`
  - BUILD workflow: Verifies skills before `component-builder`, `code-reviewer`, and `integration-verifier`
  - DEBUG workflow: Verifies skills before `bug-investigator`, `code-reviewer`, and `integration-verifier`

## [4.5.0] - 2025-01-29

### Changed

- **Phase 5.5 Made Mandatory**: Context Preservation phase is now mandatory in all workflows
  - Changed from "Optional but Recommended" to "MANDATORY" in all workflow files
  - Added validation gates that block Phase 6 until Phase 5.5 completes
  - Added Phase 5.5 Completion Checklist with mandatory verification steps
  - Updated orchestrator enforcement to require Phase 5.5 completion
  - Updated validation documentation to include Phase 5.5 enforcement
  - Session summaries are now automatically created before final deliverables

### Added

- **Archive Cleanup Documentation**: Explicit archive management and cleanup verification
  - All workflows now document archive pruning (keeps 10 most recent session summaries)
  - Added archive cleanup verification to Phase 5.5 Completion Checklist
  - Updated success messages to include archive cleanup confirmation
  - Added archive cleanup verification step in all workflow processes
  - Updated persistence patterns to document automatic archive pruning

### Fixed

- **Context Preservation Reliability**: Ensured session summaries are always created before compaction
  - Removed skip conditions that allowed Phase 5.5 to be bypassed
  - Added enforcement mechanisms to prevent workflow progression without session summaries
  - Context preservation is now consistent and reliable across all workflows

## [4.4.0] - 2025-01-29

### Added

- **Session Summary Skill**: Comprehensive session summary creation for context preservation
  - New skill: `plugins/cc10x/skills/session-summary/SKILL.md`
  - Creates Claude-generated comprehensive session documentation
  - Analyzes conversation transcript to extract tool calls, file changes, accomplishments, decisions
  - Saves to `.claude/memory/CURRENT_SESSION.md` and archives to `.claude/memory/session_summaries/session-{timestamp}.md`
  - Archives previous sessions automatically (keeps last 10)
- **Pre-Compact Hook Context Extraction**: Enhanced programmatic context extraction before compaction
  - `extract_git_context()`: Extracts recent commits, branch, staged/unstaged files with diffs, file change statistics
  - `extract_file_changes()`: Lists recently modified files (last 2 hours) with sizes and line counts
  - `extract_workflow_context()`: Extracts active workflow, current phase, progress, completed items, next steps from checkpoints
  - `extract_feature_name()`: Extracts feature name from checkpoints or working plan
  - `extract_key_decisions()`: Extracts key decisions from working plan
  - Snapshots now filled with real data instead of placeholders
  - Git context, file changes, workflow state automatically included in snapshots
- **Post-Compact Hook Session Summary Loading**: Enhanced context recovery after compaction
  - Loads session summary from `.claude/memory/CURRENT_SESSION.md` (highest priority)
  - Falls back to most recent session summary from archive if CURRENT_SESSION.md missing
  - Combines context sources in priority order: Session Summary → Snapshot → afterCompact → Workflow Outputs
  - Comprehensive context recovery with both Claude-generated and programmatic data
- **Workflow Session Summary Integration**: Phase 5.5 added to all workflows
  - **Plan Workflow**: Phase 5.5 - Context Preservation (before Phase 6)
  - **Build Workflow**: Phase 5.5 - Context Preservation (before Phase 6)
  - **Review Workflow**: Phase 5.5 - Context Preservation (before Phase 6)
  - **Debug Workflow**: Phase 5.5 - Context Preservation (before Phase 6)
  - Workflows load and execute session-summary skill when approaching token limits or after major phases
  - Session summaries complement programmatic snapshot extraction

### Fixed

- **Snapshot Template Placeholders**: Fixed critical issue where snapshots contained placeholders that never got filled
  - Pre-compact hook now extracts and fills all placeholders with real data
  - Feature names, phases, progress, completions, next steps extracted from checkpoints and working plan
  - Git context and file changes extracted programmatically
  - Key decisions extracted from working plan
- **Context Loss During Compaction**: Fixed issue where context was lost because snapshots were empty templates
  - Snapshots now contain real extracted data
  - Session summaries provide comprehensive Claude-generated analysis
  - Post-compact hook loads both sources for complete context recovery

### Changed

- **Pre-Compact Hook**: Enhanced to extract context programmatically and fill snapshots with real data
  - Replaced placeholder sections with extracted data
  - Added git context extraction with diff summaries
  - Added file change tracking
  - Added workflow state extraction from checkpoints
  - Snapshots now contain actionable context instead of templates
- **Post-Compact Hook**: Enhanced to load session summaries and combine all context sources
  - Loads session summary as highest priority context source
  - Combines session summary, snapshot, afterCompact, and workflow outputs
  - Proper priority ordering ensures most comprehensive context is available
- **All Workflows**: Added Phase 5.5 - Context Preservation for session summary creation
  - Phase 5.5 is optional but recommended before Phase 6
  - Workflows can create session summaries when approaching token limits
  - Session summaries preserve comprehensive context across compaction

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
