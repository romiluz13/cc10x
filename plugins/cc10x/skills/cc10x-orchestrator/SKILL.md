---
name: cc10x-orchestrator
description: AUTO-LOAD when user says: plan, planning, planner, plan a, plan the, plan for, design, designing, designer, design a, design the, architect, architecture, architectural, system design, roadmap, road map, strategy, strategic planning, feature planning, project planning, implementation plan, build, building, builder, build a, build the, implement, implementation, implementing, create, creating, create a, create the, write code, write a, write the, coding, code, develop, development, developing, developer, make, making, make a, make the, add feature, implement feature, build feature, review, reviewing, reviewer, review this, review the, audit, auditing, auditor, audit this, analyze, analysis, analyzing, analyze this, assess, assessment, assessing, assess this, evaluate, evaluation, evaluating, evaluate this, inspect, inspection, inspecting, inspect this, examine, examination, examining, examine this, debug, debugging, debugger, debug this, fix, fixing, fix this, fix the, fix a, error, errors, error in, error with, bug, bugs, bug in, bug with, investigate, investigation, investigating, failure, failures, failed, failing, broken, broke, break, breaking, issue, issues, issue with, problem, problems, troubleshoot, troubleshooting, diagnose, diagnosis, validate, validation, validating, validate this, verify, verification, verifying, verify this, check, checking, check this, check the, confirm implementation, alignment check, consistency check. CRITICAL - LOAD THIS FIRST: MANDATORY entry point for ALL code tasks. You MUST load this skill BEFORE writing any code. This orchestrator coordinates subagents (component-builder, code-reviewer, integration-verifier) - do NOT write code directly. Always starts with Phase 0: Functionality Analysis. Enforces TDD cycle (RED → GREEN → REFACTOR), Actions Taken tracking, memory integration, and web fetch integration. DO NOT bypass orchestrator validation mechanisms.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# cc10x Orchestrator Skill - Functionality First

## 🚨 EXECUTION MODE - THIS IS NOT DOCUMENTATION 🚨

**CRITICAL**: This skill file contains EXECUTABLE INSTRUCTIONS, not reference documentation.

**YOU MUST:**

1. **Load this skill using Skill tool** - NOT just Read tool
   - Use: `Skill(skill="cc10x:cc10x-orchestrator")` or equivalent
   - Do NOT just read the file - you must ACTIVATE the skill
2. **Execute workflows as step-by-step instructions** - NOT as summaries
   - When workflow says "Run this bash command" → YOU MUST RUN IT
   - When workflow says "DO NOT proceed until" → YOU MUST STOP AND VALIDATE
   - When workflow says "You MUST invoke subagents" → YOU MUST USE Task TOOL
3. **Treat CRITICAL markers as hard stops** - NOT suggestions
   - CRITICAL = MANDATORY = MUST DO = HARD STOP IF SKIPPED
4. **Execute validation gates literally** - NOT conceptually
   - Check each item in checklist
   - Run validation commands
   - Verify evidence exists
   - Do NOT proceed until ALL checks pass

**IF YOU READ THIS AS DOCUMENTATION INSTEAD OF EXECUTING IT:**

- ❌ You will skip mandatory steps
- ❌ You will bypass validation gates
- ❌ You will write code directly instead of invoking subagents
- ❌ Workflow will fail validation

**CORRECT APPROACH:**

1. Load orchestrator skill → Skill activates workflow
2. Execute each phase literally → Follow step-by-step
3. Run all bash commands → Capture output
4. Invoke all subagents → Use Task tool
5. Validate at each gate → Check checklist items

## 🚨 AUTO-LOAD TRIGGERS - READ THIS FIRST 🚨

**This skill MUST be loaded automatically when user request contains ANY of these keywords:**

**PLAN Workflow Keywords:**

- plan, planning, planner, plan a, plan the, plan for
- design, designing, designer, design a, design the
- architect, architecture, architectural, system design
- roadmap, road map, strategy, strategic planning
- feature planning, project planning, implementation plan

**BUILD Workflow Keywords:**

- build, building, builder, build a, build the
- implement, implementation, implementing
- create, creating, create a, create the
- write code, write a, write the, coding, code
- develop, development, developing, developer
- make, making, make a, make the
- add feature, implement feature, build feature

**REVIEW Workflow Keywords:**

- review, reviewing, reviewer, review this, review the
- audit, auditing, auditor, audit this
- analyze, analysis, analyzing, analyze this
- assess, assessment, assessing, assess this
- evaluate, evaluation, evaluating, evaluate this
- inspect, inspection, inspecting, inspect this
- examine, examination, examining, examine this

**DEBUG Workflow Keywords:**

- debug, debugging, debugger, debug this
- fix, fixing, fix this, fix the, fix a
- error, errors, error in, error with
- bug, bugs, bug in, bug with
- investigate, investigation, investigating
- failure, failures, failed, failing
- broken, broke, break, breaking
- issue, issues, issue with, problem, problems
- troubleshoot, troubleshooting, diagnose, diagnosis

**VALIDATE Workflow Keywords:**

- validate, validation, validating, validate this
- verify, verification, verifying, verify this
- check, checking, check this, check the
- confirm implementation, alignment check, consistency check

**If user request contains ANY keyword above → LOAD THIS SKILL IMMEDIATELY**

**Examples:**

- User says "plan a feature" → Load orchestrator → PLAN workflow activates
- User says "build a component" → Load orchestrator → BUILD workflow activates
- User says "review this code" → Load orchestrator → REVIEW workflow activates
- User says "debug this error" → Load orchestrator → DEBUG workflow activates
- User says "validate implementation" → Load orchestrator → VALIDATE workflow activates

## CRITICAL ENFORCEMENT - READ THIS FIRST

**🚨 BYPASS PREVENTION - DO NOT WRITE CODE DIRECTLY 🚨**

**CRITICAL RULES** (Violation = Incomplete Results):

1. **DO NOT write code directly** - You MUST invoke subagents instead:
   - BUILD workflow: component-builder → code-reviewer → integration-verifier
   - REVIEW workflow: analysis subagents → code-reviewer (if changes) → integration-verifier (if integration)
   - PLAN workflow: planning-architecture-risk → planning-design-deployment
   - DEBUG workflow: bug-investigator → code-reviewer → integration-verifier
   - VALIDATE workflow: Direct analysis (no subagents)

2. **DO NOT skip TDD cycle** - For BUILD workflow, you MUST follow RED → GREEN → REFACTOR:
   - RED: Write failing test first, capture output with exit code
   - GREEN: Minimal implementation, run test, capture exit code
   - REFACTOR: Clean up while tests green, verify exit code
   - Do NOT mark component complete without seeing test fail then pass

3. **DO NOT skip Actions Taken tracking** - You MUST maintain Actions Taken section in real-time:
   - Update IMMEDIATELY after each activation (skill loading, subagent invocation, phase completion)
   - Never proceed to next phase without updating Actions Taken
   - Verify Actions Taken updated before each phase transition
   - Before final report, verify ALL phases documented in Actions Taken

4. **DO NOT skip inventory checks** - You MUST perform:
   - Skills Inventory Check before Phase 3 (verify ALL required skills loaded)
   - Subagents Inventory Check before Phase 4 (verify ALL required subagents invoked)
   - If ANY missing, STOP workflow execution, fix immediately, re-validate

5. **DO NOT skip memory integration** - You MUST use:
   - Query patterns before complexity scoring (load patterns.json ONCE, cache for workflow duration)
   - Store patterns after workflow completion (validate first, update accuracy)
   - Store user preferences (explicit only, never inferred)
   - Store workflow checkpoints

6. **DO NOT skip web fetch integration** - You MUST use:
   - When external APIs/libraries/frameworks mentioned, fetch documentation
   - Use question-based prompts (not raw content requests)
   - Check cache first, use cache if valid, fetch if needed
   - Cache results with appropriate TTL

**If you violate ANY of these rules, the workflow will FAIL validation and you will be forced to correct before proceeding.**

## TL;DR Quick Checklist

**CRITICAL**: Complete ALL items below. Skipping any item will cause workflow validation to FAIL.

- [ ] **LOAD ORCHESTRATOR FIRST** - This skill MUST be loaded before any code tasks
- [ ] Detect user intent (review/plan/build/debug/validate) using keyword matching
- [ ] Execute Phase 0: Functionality Analysis FIRST (understand user/admin/system flows, verify functionality works)
- [ ] Execute Phase 0: Context Preset Detection (automatically detect task type and load appropriate preset)
- [ ] Load required skills in parallel (if independent) or sequentially (if dependencies exist)
- [ ] Load conditional skills based on detection logic (UI detected → load ui-design, etc.)
- [ ] **UPDATE Actions Taken** - Document skills loaded IMMEDIATELY after loading
- [ ] **PERFORM Skills Inventory Check** - Verify ALL required skills loaded before Phase 3
- [ ] **DO NOT write code directly** - Invoke subagents instead (component-builder → code-reviewer → integration-verifier)
- [ ] **FOR BUILD workflow** - Follow TDD cycle: RED (failing test) → GREEN (minimal code) → REFACTOR (clean up)
- [ ] Invoke subagents based on conditions and dependencies (check skip conditions, analyze dependencies)
- [ ] **UPDATE Actions Taken** - Document subagents invoked IMMEDIATELY after invocation
- [ ] **PERFORM Subagents Inventory Check** - Verify ALL required subagents invoked before Phase 4
- [ ] **USE memory integration** - Query patterns before complexity, store patterns after completion
- [ ] **USE web fetch integration** - Fetch external docs when APIs/libraries mentioned
- [ ] Validate outputs before proceeding (check format, evidence, file:line citations)
- [ ] Generate verification summary with evidence (commands run, exit codes, artifacts)
- [ ] Use Error Recovery Protocol if any component fails (context → problem → options → impact → default)
- [ ] **VALIDATE Actions Taken** - Verify ALL phases documented before final report

## Guardrails

**CRITICAL**: These guardrails MUST be followed in all workflows. Violations lead to incomplete or incorrect results.

- **Functionality First**: Always understand functionality (user flows, admin flows, system flows) BEFORE applying specialized checks (security, quality, performance, UX, accessibility, architecture). Verify functionality works BEFORE checking other concerns.

- **Evidence Required**: Every claim must include file:line citations or command outputs. No assertions without proof. Use `file:line` format for code references, include exit codes for commands.

- **No Placeholders**: Never use "TODO", "TBD", "FIXME" in critical sections (functionality analysis, findings, recommendations, verification summaries). Complete all required sections before proceeding.

- **Validation Mandatory**: Validate all outputs before proceeding to next phase. Check format, evidence, file:line citations, exit codes. Do NOT proceed until validation passes.

- **Scope Awareness**: Keep changes tightly scoped to requested outcome. Don't expand beyond user's request unless explicitly asked. Focus on what was requested, not what "could be improved."

- **Phase 0 Enforcement**: Phase 0: Functionality Analysis MUST be completed before any skill loading or subagent dispatching. This is non-negotiable.

- **Error Recovery**: Always use Error Recovery Protocol when failures occur. Provide context, problem, options, impact, and default action. Wait for user decision before proceeding.

## Runtime Compliance Checks

**CRITICAL**: These validation gates are executed automatically at key checkpoints. If validation fails, workflow STOPS and you MUST fix issues before proceeding.

### Validation Point 1: Before Phase 2 (Skills Loading)

**Checklist** (ALL must pass):

- [ ] Phase 0: Functionality Analysis complete (user flow, admin flow if applicable, system flow documented)
- [ ] Actions Taken section exists and Phase 0 documented
- [ ] Gate checks passed (if applicable)

**If validation fails**: STOP workflow, complete missing items, re-validate, then proceed.

### Validation Point 2: Before Phase 3 (Subagent Invocation)

**Checklist** (ALL must pass):

- [ ] Phase 2: Skills loaded complete
- [ ] Actions Taken section updated with ALL required skills listed
- [ ] Skills Inventory Check passed (ALL required skills loaded, conditional skills loaded IF detected)
- [ ] Each skill marked as "loaded successfully" or "failed to load" in Actions Taken

**If validation fails**: STOP workflow, load missing skills, update Actions Taken, re-run Skills Inventory Check, then proceed.

### Validation Point 3: Before Phase 4 (Synthesis)

**Checklist** (ALL must pass):

- [ ] Phase 3: Subagents invoked complete
- [ ] Actions Taken section updated with ALL required subagents listed
- [ ] Subagents Inventory Check passed (ALL required subagents invoked, execution mode documented)
- [ ] Each subagent marked as "invoked successfully" or "skipped" with reason in Actions Taken
- [ ] For BUILD workflow: TDD cycle evidence present (RED → GREEN → REFACTOR with exit codes)

**If validation fails**: STOP workflow, invoke missing subagents, update Actions Taken, re-run Subagents Inventory Check, then proceed.

### Validation Point 4: Before Final Report

**Checklist** (ALL must pass):

- [ ] ALL workflow phases completed
- [ ] Actions Taken section complete (ALL phases documented)
- [ ] Skills Inventory Check passed
- [ ] Subagents Inventory Check passed
- [ ] Memory integration used (patterns queried before complexity, stored after completion)
- [ ] Web fetch integration used (if external APIs/libraries mentioned)
- [ ] Pre-Final-Report Validation passed (see orchestrator validation section)

**If validation fails**: STOP final report generation, complete missing items, re-run all validations, then proceed.

### Automatic Validation Execution

**When**: These checks run automatically at each validation point above.

**How**:

1. Read Actions Taken section
2. Verify required items present
3. If ANY item missing → STOP workflow, report missing items, force correction
4. Re-validate after correction
5. Only proceed when ALL items pass

**Enforcement**: Workflow CANNOT proceed past validation point until ALL checks pass.

**CRITICAL**: Every workflow MUST start with functionality analysis before applying specialized checks (security, quality, performance, UX, accessibility, architecture, etc.).

**Core Principle**: Understand what the code/feature is supposed to do (user flows, admin flows, system flows) and verify it works BEFORE checking other concerns.

**Mandatory First Step**: Before loading any skills or dispatching any subagents:

1. **Understand Functionality**: What does the user need? What are the user flows? Admin flows? System flows?
2. **Verify Functionality**: Does it work? Test if possible, verify with evidence.
3. **THEN Apply Specialized Checks**: Only after functionality is understood and verified, apply security, quality, performance, UX, accessibility, architecture checks.

**Functionality Analysis Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for standard format.

## Purpose

Coordinate the five cc10x workflows using the official Anthropic model-invoked skills pattern. The orchestrator:

- Identifies the requested outcome (review, plan, build, debug, validate).
- Loads only workflow skills that exist in `plugins/cc10x/skills/`.
- Analyzes dependencies and parallelizes subagents where safe (read-only, independent, isolated contexts).
- Falls back to sequential execution for operations with dependencies or shared state.
- Prompts for explicit user approval before continuing past any complexity gates.
- Routes all completion claims through the `verification-before-completion` skill.

## Supported Workflows

- **review** -> `review-workflow`
- **plan** -> `planning-workflow`
- **build** -> `build-workflow`
- **debug** -> `debug-workflow`
- **validate** -> `VALIDATION workflow` (see `workflows/validate.md`)

If a user combines intents (for example "review then plan"), run each workflow in the order requested and confirm between phases. Never promise simultaneous execution or reference agents that are not bundled with the plugin.

## Before Any Task

**Context Checklist** (complete ALL before proceeding):

- [ ] Read user request and understand intent (what does user want to accomplish?)
- [ ] Check existing workflows/skills/subagents (verify what's available in `plugins/cc10x/skills/` and `plugins/cc10x/subagents/`)
- [ ] Load functionality analysis template (`plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`)
- [ ] Identify code type (UI/API/Utility/Integration/Database/Configuration/CLI/Background Job) if applicable
- [ ] Run Phase 0: Functionality Analysis (understand user/admin/system flows, verify functionality works)

**CRITICAL**: Do NOT proceed to workflow execution until ALL items above are checked. If any item is incomplete, complete it before proceeding.

## Operation

1. **Functionality Analysis (MANDATORY FIRST STEP)**
   - **Before any workflow execution**: Complete functionality analysis using the functionality analysis template
   - **Load Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - **Analyze User Request**: Understand what functionality is needed (user flows, admin flows, system flows)
   - **Document Flows**: Document user flows, admin flows (if applicable), system flows, integration flows (if applicable)
   - **Verify Functionality**: If possible, verify functionality works (test, check logs, manual verification)
   - **Gate Check**: Do NOT proceed to workflow execution until functionality analysis is complete
   - **If Functionality Unclear**: Ask user: "Functionality unclear. Please clarify: What functionality is needed? What are the user flows?"
2. **Context Preset Detection (AUTOMATIC)**
   - **After functionality analysis, before skill loading**: Automatically detect task type and load appropriate context preset
   - **Load Skill**: Load `context-preset-management` skill to handle preset detection
   - **Detection Process**:
     1. **Analyze User Request**: Scan for task type indicators (frontend/backend/full-stack keywords)
     2. **File Pattern Detection**: Use `Glob` to detect file patterns:
        - `Glob("**/*.{tsx,jsx}")` → frontend detected
        - `Glob("**/api/**")` → backend detected
        - Both → app preset
     3. **Memory Check**: Check `.claude/memory/preset_preferences.json` for remembered preset preference
     4. **Preset Selection**: Select appropriate preset (frontend/backend/app) based on detection
     5. **Load Rules**: Load alwaysApply rules + preset-specific rules from `.claude/context.json`
     6. **Store Preference**: Save selected preset to memory for future reference
   - **Preset Selection Logic**:
     - Frontend indicators + frontend files → `frontend` preset
     - Backend indicators + backend files → `backend` preset
     - Both indicators + both file types → `app` preset
     - No clear indicators → Check memory for last used preset, or use default (`app`)
   - **Error Handling**: If context.json missing or preset not found, use default preset (`app`) and continue workflow
   - **Output**: Context summary with selected preset and loaded rules
   - **Integration**: This step is automatic and transparent - no user commands required
3. **Intent and Context Check**

   **CRITICAL:** Phase 0 (Functionality Analysis) and Context Preset Detection MUST be complete before proceeding.

   **Error Detection** (after Phase 0 and Context Preset Detection, before intent detection):

   **Detection Logic:**
   - User request contains bash output or error messages
   - Error count == 1 (single error)
   - Error message is clear and actionable
   - Fix is obvious (syntax error, missing import, typo, etc.)

   **Decision Tree:**

   ```
   User request contains error?
   ├─ Single clear error + obvious fix?
   │   └─ YES → Load `quick-error-fixing` skill
   │       └─ Execute quick fix
   │           ├─ Fix succeeds → Done (no workflow needed)
   │           └─ Fix fails → Fall back to DEBUG workflow
   │   └─ NO → Continue to intent detection (existing flow)
   └─ Multiple/complex errors?
       └─ YES → Skip quick fix, proceed to DEBUG workflow
   ```

   **Quick Fix Criteria:**
   - Syntax errors (missing semicolon, bracket, etc.)
   - Import errors (missing import statement)
   - Type errors (simple type mismatches)
   - Typo errors (variable name typos)
   - Single file errors (not cross-file issues)

   **If Quick Fix Applies:**
   1. Load `quick-error-fixing` skill
   2. Execute fix (read error, identify cause, apply fix, verify)
   3. If fix succeeds → Report success, done
   4. If fix fails → Report failure, proceed to DEBUG workflow

   **If Quick Fix Doesn't Apply:**
   - Continue to intent detection (existing flow unchanged)

   **Skill Authoring Detection** (before workflow selection):

   **Detection Logic:**
   - Keywords: "create skill", "write skill", "new skill", "skill authoring", "author skill"
   - User request explicitly mentions creating/writing skills

   **If Skill Authoring Detected:**
   1. Load `skill-authoring` skill directly (no workflow needed)
   2. Execute skill authoring process
   3. Done (no workflow execution)

   **If Skill Authoring Not Detected:**
   - Continue to intent detection decision tree (existing flow)

   - **Intent Detection Decision Tree**: Match user request to workflow using visual decision tree:

     ```
     User request?
     ├─ Contains "create skill"/"write skill"/"new skill"/"skill authoring"/"author skill"?
     │   └─ YES → Load `skill-authoring` skill (no workflow needed)
     │   └─ NO → Continue
     ├─ Contains "review"/"audit"/"analyze"/"assess"/"evaluate"/"inspect"/"examine"?
     │   └─ YES → Review workflow
     │   └─ NO → Continue
     ├─ Contains "plan"/"design"/"architect"/"roadmap"/"strategy"/"architecture"/"system design"?
     │   └─ YES → Plan workflow
     │   └─ NO → Continue
     ├─ Contains "build"/"implement"/"create"/"write"/"code"/"develop"/"make"/"add feature"?
     │   └─ YES → Build workflow
     │   └─ NO → Continue
     ├─ Contains "debug"/"fix"/"error"/"bug"/"investigate"/"failure"/"broken"/"issue"/"problem"/"troubleshoot"/"diagnose"?
     │   └─ YES → Debug workflow
     │   └─ NO → Continue
     ├─ Contains "validate"/"verify"/"check"/"confirm implementation"/"alignment check"/"consistency check"?
     │   └─ YES → Validate workflow
     │   └─ NO → Continue
     ├─ Multiple keywords matched?
     │   └─ YES → Intent Disambiguation required
     │   └─ NO → Continue
     └─ No keywords matched?
         └─ YES → Ask user: "Which workflow should I run? (review/plan/build/debug/validate)"
     ```

     **Matching Logic**:
     1. Scan user request for intent keywords (case-insensitive)
     2. Count matches per workflow (one keyword can match multiple workflows)
     3. If single workflow has >0 matches → select that workflow
     4. If multiple workflows have matches → Intent Disambiguation required
     5. If no matches → ask user: "Which workflow should I run? (review/plan/build/debug/validate)"

     **Examples**:
     - "Review my code" → Review workflow (single match)
     - "Review and plan the feature" → Intent Disambiguation (multiple matches)
     - "Fix the bug" → Debug workflow (single match)
     - "Make it better" → Ask user (no matches)

   - **Intent Disambiguation**: If user request contains multiple workflow keywords (e.g., "review and plan"), list detected workflows: [review, plan, build, debug, validate]. Ask user: "I detected multiple intents. Which should I execute? (or 'both' for sequential)". Wait for explicit selection before proceeding.
   - Validate inputs (files, directories, questions). Ask for clarifications when context is missing.

   **Memory Integration** (filesystem-based, optimized):
   - **Efficient Query**: Load `.claude/memory/patterns.json` ONCE, cache for workflow duration
   - **Semantic Match**: Use `jq` to filter by task signature (file_count, type, deps) - not exact text
   - **Top Matches Only**: Return top 3 highest-confidence patterns
   - **Check User Preferences**: Load `.claude/memory/preferences.json` if exists
   - **Validation**: Only use patterns with confidence="high" or accuracy > 70%

   **External Resource Check** (smart caching):
   - **Check Cache First**: Lookup URL in `.claude/memory/web_cache/cache_index.json`
   - **Use Cache if Valid**: If cached and TTL valid → use cache (skip fetch)
   - **Re-fetch if Expired**: If cached but expired → re-fetch
   - **Deduplication**: Track URLs fetched in this workflow, avoid duplicates
   - **Batch Detection**: If multiple URLs needed, batch-fetch when possible
   - Ask user: "Detected external dependencies: {list}. Check cache or fetch documentation? (yes/no)"
   - Score complexity on a 1-5 scale using the expanded Complexity Rubric below. When the score is <=2 for plan/build, run Bash: `${CLAUDE_PLUGIN_ROOT}/scripts/lightweight-warning.sh` and wait for the user's explicit yes/no decision before proceeding.

## Skill Loading Optimization

**Skill Loading Decision Tree**:

```
Workflow requires skills?
├─ Identify required skills (from workflow Phase 2)
│   └─ Required skills exist?
│       ├─ YES → Continue
│       └─ NO → Report error, ask user: "Required skill '{name}' not found. Continue without it? (yes/no)"
├─ Identify conditional skills (from workflow detection logic)
│   └─ Detection logic check
│       ├─ UI components detected? → Load ui-design
│       ├─ Design patterns mentioned? → Load design-patterns
│       ├─ Feature planning needed? → Load feature-planning
│       └─ None detected → Skip conditional skills
├─ Check skill dependencies
│   └─ Skills have dependencies?
│       ├─ YES → Build dependency graph
│       │   └─ Load in topological order (sequential)
│       └─ NO → No dependencies
├─ Determine loading strategy
│   └─ All skills independent?
│       ├─ YES → Load all in parallel (faster)
│       └─ NO → Load sequentially (respect dependencies)
└─ Verify loading success
    └─ All skills loaded?
        ├─ YES → Continue to subagent invocation
        └─ NO → Error Recovery Protocol
```

**Unified Parallel Loading Strategy**:

1. **Identify Skill Dependencies**:
   - Map skill dependencies: skill A → skill B (B requires A)
   - Check if skills are independent (no dependencies)

2. **Load Strategy**:

   **PARALLEL Loading**:
   - ✅ Independent skills (no dependencies) → Load simultaneously
   - ✅ Faster initialization (all skills ready together)

   **SEQUENTIAL Loading**:
   - ❌ Skills with dependencies → Load in topological order
   - ❌ Dependent skill waits for prerequisite

3. **Implementation**:

   ```
   Example: Review workflow requires 8 skills

   Dependency Analysis:
   - risk-analysis: no deps → Parallel group 1
   - security-patterns: no deps → Parallel group 1
   - performance-patterns: no deps → Parallel group 1
   - code-quality-patterns: no deps → Parallel group 1
   - ux-patterns: no deps → Parallel group 1
   - accessibility-patterns: no deps → Parallel group 1
   - memory-tool-integration: no deps → Parallel group 1
   - web-fetch-integration: no deps → Parallel group 1

   Load all 8 skills in parallel (no dependencies)
   ```

**Update all workflow Phase 1 sections** to use "Load all independent skills in parallel" instead of mixed strategies.

2. **Workflow Existence Verification**
   - Before loading any workflow skill, verify it exists: Read first 100 chars of `plugins/cc10x/skills/{workflow-name}/SKILL.md`.
   - If workflow doesn't exist, report: "Workflow '{name}' not found. Available workflows: [review, plan, build, debug, validate]".
   - Ask user: "Choose an available workflow or specify custom instructions?"

3. **Policy Enforcement**
   - Do not auto-chain workflows. Offer optional follow-ups only after delivering the requested result.
   - Require explicit consent before continuing past a gate or rerunning an analysis.
   - When a workflow needs evidence (tests, lint, build), invoke `verification-before-completion` so the agent executes the command, captures output, and cites results before claiming success.

4. **Workflow Execution**
   - Load the workflow skill with `Read` (progressive disclosure Level 2).
   - **CRITICAL**: Ensure workflow executes Phase 0: Functionality Analysis FIRST before any skill loading or subagent dispatching
   - **Verify Phase 0**: Check that workflow includes Phase 0: Functionality Analysis (MANDATORY)
   - **Coordination Verification** (before proceeding):
     - [ ] Intent detected correctly (verify keyword matching)
     - [ ] Workflow exists (verify workflow file exists)
     - [ ] Phase 0 executed (verify functionality analysis complete)
     - [ ] Gate checks passed (verify all gate checks passed)
   - **Skill Loading Verification**: After loading each skill referenced by the workflow, verify success:
     - Read first 100 chars of SKILL.md to confirm content loaded
     - If loading fails, report immediately: "Skill '{name}' failed to load: {error details}"
     - Present options: "Continue without {skill} (functionality reduced)? Abort workflow? Retry loading?"
     - Wait for user decision before proceeding
   - **Skill Loading Coordination**:
     - Identify required skills (from workflow Phase 2)
     - Identify conditional skills (from workflow detection logic)
     - Check detection logic for conditional skills BEFORE loading
     - Load all independent skills in parallel (faster initialization)
     - Verify each skill loaded successfully

   **Skills Inventory Check** (MANDATORY before proceeding to Phase 3):

   **CRITICAL**: This check prevents missing required skills. Execute BEFORE any subagent invocation.
   1. **Read Workflow Phase 2 Section**:
      - Read workflow file Phase 2 section to get complete required skills list
      - Read workflow file Phase 2 section to get conditional skills detection logic
      - Document expected skills: {list all required + conditional if detected}

   2. **Check Actions Taken Section**:
      - Read Actions Taken section (or create if not exists)
      - Verify ALL required skills are listed with load status
      - Verify conditional skills are listed IF detection logic matched
      - Verify each skill marked as "loaded successfully" or "failed to load"

   3. **Inventory Validation**:
      - [ ] ALL required skills from workflow Phase 2 listed in Actions Taken
      - [ ] Each required skill marked as "loaded successfully" or "failed to load"
      - [ ] Conditional skills listed IF detection logic matched
      - [ ] Each conditional skill marked as "loaded successfully" or "failed to load" IF detected
      - [ ] No required skill missing from Actions Taken
      - [ ] No conditional skill missing IF detection logic matched

   4. **If ANY required skill missing**:
      - STOP workflow execution
      - Report: "CRITICAL: Required skill '{name}' missing from Actions Taken. Loading now."
      - Load missing skill immediately
      - Update Actions Taken section
      - Re-run inventory check

   5. **If conditional skill should have been detected but not listed**:
      - STOP workflow execution
      - Report: "CRITICAL: Conditional skill '{name}' should be loaded (detection logic matched) but missing. Loading now."
      - Check detection logic again
      - Load skill if detection logic matches
      - Update Actions Taken section
      - Re-run inventory check

   6. **If conditional skill listed but detection logic doesn't match**:
      - Document: "Conditional skill '{name}' loaded but detection logic doesn't match. Continuing."
      - Continue (not critical, but document for review)

   **CRITICAL**: Do NOT proceed to Phase 3 (subagent invocation) until ALL items above are checked and validated.

   **Real-Time Activation Tracking** (MANDATORY):

   **Purpose**: Track all activations in real-time to prevent misses.

   **Tracking Format**:
   Maintain running inventory in Actions Taken section:

   ```markdown
   ## Actions Taken (Real-Time Tracking)

   ### Phase 0: Functionality Analysis

   - ✅ Completed: [timestamp]
   - User flows: [count] documented
   - Admin flows: [count] documented (if applicable)
   - System flows: [count] documented

   ### Phase 1: [Phase Name]

   - ✅ Completed: [timestamp]
   - [Phase-specific activities]

   ### Phase 2: Skills Loaded

   - ✅ Completed: [timestamp]
   - Required skills loaded:
     - ✅ project-context-understanding (loaded successfully)
     - ✅ [skill-name] (loaded successfully)
     - ❌ [skill-name] (failed to load: [reason])
   - Conditional skills loaded (IF detected):
     - ✅ [skill-name] (detected: [reason], loaded successfully)
   - Skills Inventory Check: ✅ Passed

   ### Phase 3: Subagents Invoked

   - ✅ Completed: [timestamp]
   - Subagents invoked:
     - ✅ analysis-risk-security (invoked successfully, parallel group 1)
     - ✅ analysis-performance-quality (invoked successfully, parallel group 1)
     - ✅ analysis-ux-accessibility (invoked successfully, parallel group 1)
     - ✅ code-reviewer (invoked successfully, sequential after analysis, code changes detected)
     - ✅ integration-verifier (invoked successfully, sequential after code-reviewer, integration changes detected)
   - Execution mode: Parallel (analysis subagents), Sequential (code-reviewer → integration-verifier)
   - Skip decisions: None
   - Subagents Inventory Check: ✅ Passed

   ### Phase 4+: [Workflow-Specific]

   - ✅ Completed: [timestamp]
   - [Workflow-specific activities]
   ```

   **Update Rules**:
   - Update Actions Taken IMMEDIATELY after each activation
   - Never proceed to next phase without updating Actions Taken
   - Verify Actions Taken updated before each phase transition
   - Use checkmarks (✅) for completed, (❌) for failed, (⏭️) for skipped

   **Validation**:
   - Before each phase transition: Verify Actions Taken updated
   - Before final report: Verify ALL phases documented in Actions Taken
   - If Actions Taken not updated: STOP and update before proceeding

   - Follow workflow instructions exactly. Workflows now reference only real subagents and skills.
   - Record which domain skills are invoked so results can point to specific guidance files.

   **Subagent Invocation Rules** (CRITICAL):

   **Subagent Invocation Decision Tree**:

   ```
   Workflow requires subagents?
   ├─ Verify subagent exists (check plugins/cc10x/subagents/)
   │   └─ Subagent exists?
   │       ├─ YES → Continue
   │       └─ NO → Report error, ask user: "Subagent '{name}' not found. Skip it? (yes/no)"
   ├─ Check skip conditions (from workflow definition)
   │   └─ Skip condition met?
   │       ├─ YES → Skip subagent, ask user: "Skipping {name} due to {reason}. Proceed? (yes/no)"
   │       └─ NO → Continue
   ├─ Analyze dependencies
   │   └─ Build dependency graph
   │       ├─ Subagent A → Subagent B (B needs A's output)?
   │       │   └─ YES → Sequential execution required
   │       │   └─ NO → Check conflicts
   │       └─ Subagents modify same files?
   │           └─ YES → Sequential execution required
   │           └─ NO → Check execution mode
   ├─ Determine execution mode
   │   └─ All conditions met for parallel?
   │       ├─ YES (no dependencies, read-only, isolated contexts, independent data) → Parallel execution
   │       └─ NO → Sequential execution
   ├─ Prepare context
   │   └─ All context provided?
   │       ├─ YES → Invoke subagent
   │       └─ NO → Gather missing context, then invoke
   └─ Validate output
       └─ Output valid?
           ├─ YES → Continue to next subagent or workflow phase
           └─ NO → Error Recovery Protocol
   ```

   - **Verify existence FIRST**: Before invoking any subagent, verify it exists in `plugins/cc10x/subagents/`
   - **Check skip conditions**: Each workflow defines "when NOT to invoke" - check these BEFORE invocation
   - **Dependency Analysis**: Build dependency graph BEFORE invocation:
     - Map dependencies: subagent A → subagent B (B requires A's output)
     - Check conflicts: subagents modifying same files
     - Determine execution mode: parallel (safe) vs sequential (required)
   - **Coordination Verification** (before subagent invocation):
     - [ ] Subagent exists (verify subagent file exists)
     - [ ] Skip conditions checked (verify "when NOT to invoke" checked)
     - [ ] Dependencies analyzed (verify dependency graph built)
     - [ ] Execution mode determined (verify parallel vs sequential)
     - [ ] Context prepared (verify all context provided)
   - **Respect user overrides**: If user explicitly skips a subagent, document and skip it
   - **Sequential only**: Never invoke multiple subagents in parallel UNLESS all conditions met:
     - ✅ No output dependencies (operation B doesn't need operation A's output)
     - ✅ Read-only operations (no state mutations)
     - ✅ Isolated contexts (separate subagent contexts)
     - ✅ Independent data (different files/components/bugs)
     - ✅ Validation after each (prevents error propagation)
   - **Context isolation**: Each subagent starts fresh - provide all needed context explicitly
   - **Confirmation on skip**: If skipping subagent, ask user: "Skipping {subagent-name} due to {reason}. Proceed? (yes/no)"
   - **Output Validation** (after subagent completes):
     - [ ] Output format matches expected template (check required sections present)
     - [ ] All required fields present (findings, file:line citations, commands, exit codes)
     - [ ] File references include path:line where applicable
     - [ ] Commands included with exit codes (if applicable)
     - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
     - [ ] Output is actionable (not just descriptions)
   - **Error Recovery**: If subagent fails, use Error Recovery Protocol

   **Subagents Inventory Check** (MANDATORY before Phase 3 completion):

   **CRITICAL**: This check prevents missing required subagents. Execute AFTER all subagents should have been invoked.
   1. **Read Workflow Phase 3 Section**:
      - Read workflow file Phase 3 section to get subagent invocation rules
      - Read "When to Invoke Subagents" section
      - Read "When NOT to Invoke Subagents" section
      - Document expected subagents: {list all that should be invoked}

   2. **Check Actions Taken Section**:
      - Read Actions Taken section
      - Verify ALL subagents that should be invoked are listed
      - Verify execution mode documented (parallel/sequential)
      - Verify skip decisions documented (if any skipped)

   3. **Inventory Validation**:
      - [ ] ALL subagents that should be invoked are listed in Actions Taken
      - [ ] Each subagent marked as "invoked successfully" or "skipped" with reason
      - [ ] Execution mode documented (parallel/sequential for each subagent group)
      - [ ] Skip decisions documented with reasons (if any skipped)
      - [ ] No required subagent missing from Actions Taken
      - [ ] No subagent listed that shouldn't have been invoked (check skip conditions)

   4. **Workflow-Specific Validation**:

      **Review Workflow**:
      - [ ] Analysis subagents listed (analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility)
      - [ ] Execution mode documented (parallel IF comprehensive, single IF focused)
      - [ ] code-reviewer listed IF code changes detected
      - [ ] integration-verifier listed IF integration changes detected

      **Plan Workflow**:
      - [ ] planning-architecture-risk listed (FIRST, sequential)
      - [ ] planning-design-deployment listed (SECOND, sequential)
      - [ ] Sequential execution documented
      - [ ] Architecture outputs passed to design subagent documented

      **Build Workflow**:
      - [ ] component-builder listed for each component
      - [ ] code-reviewer listed for each component (unless skipped)
      - [ ] integration-verifier listed for each component (unless skipped)
      - [ ] Sequential execution per component documented
      - [ ] Parallel execution between independent components documented

      **Debug Workflow**:
      - [ ] bug-investigator listed for each bug
      - [ ] code-reviewer listed for each bug (unless skipped)
      - [ ] integration-verifier listed for each bug (unless skipped)
      - [ ] Sequential execution per bug documented
      - [ ] Parallel execution between independent bugs documented

      **Validate Workflow**:
      - [ ] No subagents (direct analysis only)
      - [ ] Documented as "No subagents - direct analysis"

   5. **If ANY required subagent missing**:
      - STOP workflow execution
      - Report: "CRITICAL: Required subagent '{name}' missing from Actions Taken. Checking skip conditions..."
      - Check skip conditions from workflow Phase 3
      - If skip condition NOT met → Invoke subagent immediately
      - If skip condition met → Document skip decision in Actions Taken
      - Update Actions Taken section
      - Re-run inventory check

   6. **If subagent listed but shouldn't have been invoked**:
      - Document: "Subagent '{name}' invoked but skip condition met. Continuing."
      - Continue (not critical, but document for review)

   **CRITICAL**: Do NOT proceed to Phase 4 (synthesis) until ALL items above are checked and validated.

### Tool Access Precedence

- When multiple skills are active, the orchestrator/workflow tool set governs delegation and verification. Domain skills may restrict themselves (e.g., Read/Grep/Glob), but they do not prevent the orchestrator/workflow from using `Task` or `Bash` to delegate/verify.

## Ask Questions Tool Usage

**Purpose**: Clarify requirements and gather missing information before proceeding

**When to Use**:

- Phase 0: Functionality Analysis (when functionality unclear)
- Plan Workflow: Requirements gathering
- Build Workflow: UI requirements for UI components
- Debug Workflow: Bug clarification

**Usage Pattern**:

```
Use the askquestion tool to clarify requirements:
- [Specific questions about functionality/requirements]
```

**Example**:

```
Use the askquestion tool to clarify requirements:
- What are the specific user flows?
- What are the acceptance criteria?
- What are the constraints?
```

## Task Tool Usage

**Purpose**: Track workflow progress and manage task queues

**When to Use**:

- Phase tracking (all workflows)
- Component build queue (Build workflow)
- Review findings tracking (Review workflow)
- Planning checklist (Plan workflow)

**Usage Pattern**:

```
Task: Create tasks for [purpose]
- Task 1: [description] (status)
- Task 2: [description] (status)

Task: Update [task] status to [new_status]
```

**Example**:

```
Task: Create tasks for workflow phases
- Phase 0: Functionality Analysis (in_progress)
- Phase 1: Input Validation (pending)
- Phase 2: Load Skills (pending)
```

## Tool Selection Guide

| Task                    | Tool          | When to Use                                                            | Example                                    |
| ----------------------- | ------------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| Clarify requirements    | Ask Questions | Functionality unclear, missing requirements, need user input           | "What are the specific user flows?"        |
| Track workflow progress | Task          | Phase tracking, component queue, findings tracking, planning checklist | "Task: Create tasks for workflow phases"   |
| Find files by pattern   | Glob          | Need to find files matching pattern (e.g., `*.ts`, `**/test/**`)       | `Glob("**/*.test.ts")`                     |
| Search file content     | Grep          | Need to find text/patterns in files                                    | `Grep("function.*test")`                   |
| Read file contents      | Read          | Need to read specific file or section                                  | `Read("path/to/file.ts")`                  |
| Execute shell commands  | Bash          | Need to run commands, check exit codes, verify functionality           | `Bash("npm test")`                         |
| Fetch external docs     | WebFetch      | Need external API docs, library docs, reference materials              | `WebFetch("https://api.example.com/docs")` |

**Tool Selection Logic**:

- **Finding files**: Use `Glob` for pattern matching, `Grep` for content search
- **Reading files**: Use `Read` for specific files, `Grep` for searching across files
- **User interaction**: Use `Ask Questions` for clarification, `Task` for progress tracking
- **Verification**: Use `Bash` to run tests/commands, check exit codes
- **External resources**: Use `WebFetch` for documentation, cache results

## Search Guidance

**CRITICAL**: Choose the right tool for the search task. Using the wrong tool wastes tokens and time.

**When to Use Glob** (file discovery):

- Finding files by name pattern: `Glob("**/*.test.ts")`
- Finding files in specific directories: `Glob("src/components/**/*.tsx")`
- Discovering project structure: `Glob("**/*.json")` to find config files
- **Example**: "Find all test files" → `Glob("**/*.test.{ts,tsx,js,jsx}")`

**When to Use Grep** (content search):

- Searching for function/class names: `Grep("function.*authenticate")`
- Finding imports/exports: `Grep("import.*from.*api")`
- Searching for patterns across files: `Grep("TODO|FIXME|HACK")`
- Finding specific code patterns: `Grep("useState|useEffect")`
- **Example**: "Find all uses of authentication function" → `Grep("authenticate")`

**When to Use Read** (specific file access):

- Reading a known file: `Read("src/api/auth.ts")`
- Reading configuration files: `Read("package.json")`
- Reading workflow/skill files: `Read("plugins/cc10x/skills/review-workflow/SKILL.md")`
- Reading specific sections: `Read("file.ts", offset=100, limit=50)`
- **Example**: "Read the orchestrator skill" → `Read("plugins/cc10x/skills/cc10x-orchestrator/SKILL.md")`

**Search Strategy** (combine tools efficiently):

1. **Discovery Phase**: Use `Glob` to find relevant files
2. **Content Phase**: Use `Grep` to search within discovered files
3. **Detail Phase**: Use `Read` to read specific files/sections
4. **Example**:
   - Step 1: `Glob("**/*auth*.ts")` → Find auth-related files
   - Step 2: `Grep("function.*login", path="src/auth/")` → Find login functions
   - Step 3: `Read("src/auth/login.ts")` → Read specific implementation

**Anti-Patterns** (what NOT to do):

- ❌ Using `Grep` to find files by name (use `Glob` instead)
- ❌ Using `Read` to search for patterns (use `Grep` instead)
- ❌ Reading entire large files when you only need a section (use `Read` with offset/limit)
- ❌ Using `Glob` to search file contents (use `Grep` instead)

## Validation Checklist

**CRITICAL**: Before proceeding to the next phase, ALL items below MUST be checked. In Strict Mode, workflow aborts if any validation fails.

**Mandatory Validation Steps** (before proceeding):

- [ ] Phase 0 complete and verified (functionality analysis complete, all gate checks passed)
- [ ] Skills loaded successfully (all required skills loaded, conditional skills loaded if detected)
- [ ] Subagents invoked correctly (existence verified, skip conditions checked, dependencies analyzed, execution mode determined)
- [ ] Outputs validated (format matches expected template, all required fields present, file:line citations provided)
- [ ] Evidence provided for all claims (file:line citations for code references, exit codes for commands, logs/artifacts for verification)

**Strict Mode** (optional, recommended for production):

**Strict Mode Enforcement** (default for production):

**CRITICAL**: Strict Mode is enabled by default. Workflow aborts if any validation fails.

**Enforcement Points**:

1. **Phase 0 Enforcement**:
   - Workflow aborts if Phase 0 not completed FIRST
   - Workflow aborts if functionality analysis incomplete
   - Workflow aborts if gate check fails

2. **Skills Loading Enforcement**:
   - Workflow aborts if Actions Taken section missing required skills
   - Workflow aborts if any required skill not loaded (unless user explicitly skipped)
   - Workflow aborts if conditional skill should be loaded but missing (detection logic matched)
   - Skills Inventory Check must pass before proceeding

3. **Subagents Invocation Enforcement**:
   - Workflow aborts if Actions Taken section missing required subagents
   - Workflow aborts if any required subagent not invoked (unless skip condition met)
   - Workflow aborts if subagent should be invoked but missing (skip condition NOT met)
   - Subagents Inventory Check must pass before proceeding

4. **Phase Transition Enforcement**:
   - Workflow aborts if any phase skipped without documentation
   - Workflow aborts if phase completion checklist not verified
   - Workflow aborts if gate check fails
   - All phase transitions require explicit checklist completion

5. **Final Report Enforcement**:
   - Workflow aborts if Pre-Final-Report Validation fails
   - Workflow aborts if Actions Taken validation fails
   - Workflow aborts if any required section missing
   - All audits must pass before presenting final report

**Error Recovery**:

- When Strict Mode enforcement triggers:
  - Report: "CRITICAL: Strict Mode enforcement failed. Missing: {list}"
  - Use Error Recovery Protocol
  - Options: Fix missing items / Abort workflow / Disable Strict Mode (user approval required)
  - Wait for user decision before proceeding

**CRITICAL**: Strict Mode cannot be disabled without explicit user approval. Default is enabled.

When Strict Mode is enabled:

- Workflow aborts immediately if any validation step fails
- No partial results are accepted
- All evidence must be provided before proceeding
- Error Recovery Protocol is triggered on any validation failure

**Usage**: Enable Strict Mode by adding "strict mode" to user request or by default for production workflows.

5. **Result Compilation**
   - Summarise findings with severity or priority (high/medium/low) based on evidence.
   - Link each recommendation to the skill or subagent that produced it.
   - Surface open questions and next-step offers without assuming consent.

   **Notification Integration** (automatic via hooks):
   - **Workflow Completion**: Stop hook automatically sends macOS notification when workflow completes
   - **Notification Content**: Includes workflow name and conversation summary title
   - **No Action Required**: Notifications are automatic and transparent - no user commands needed
   - **Prerequisites**: Requires `terminal-notifier` CLI installed (`brew install terminal-notifier`)
   - **Graceful Failure**: If terminal-notifier not installed, notification is silently skipped (workflow continues normally)

   **Session Summary Generation** (automatic after workflow completion):

   **CRITICAL:** This happens in Orchestrator Phase 5, AFTER all workflow phases complete. Workflow Phase 0-6 execute first, then Orchestrator Phase 5 compiles results.

   **Process:**
   1. **Load Memory Skill:** Reference `memory-tool-integration` skill
   2. **Generate Session Summary:**
      - Extract file changes from workflow report (Actions Taken section)
      - Extract tool calls from Actions Taken section
      - Extract accomplishments from Findings/Decisions
      - Extract decisions from Recommendations
      - Extract next steps from Open Questions
   3. **Save Session Summary:**
      - Format: Use dotai's session-summary.md template structure
      - Save to: `.claude/memory/session_summaries/session-{timestamp}.md`
      - Archive: If CURRENT_SESSION.md exists, archive to ARCHIVE/sessions/ (keep last 10)
   4. **Update Working Plan** (if WORKING_PLAN.md exists):
      - Load `memory-tool-integration` skill
      - Update WORKING_PLAN.md with:
        - Completed tasks (from workflow report)
        - Current phase (from workflow type)
        - Next priorities (from Recommendations)
        - Session timestamp
      - Use minimal surgical updates (don't rewrite entire file)

   **Memory Integration** (filesystem-based, optimized):
   - **Validate Patterns First**: Compare predicted complexity → actual complexity
   - **Update Accuracy**: Calculate accuracy = (matches / total_uses) \* 100
   - **Update Confidence**: high (>80%), medium (60-80%), low (<60%)
   - **Store Only Validated**: Only save patterns with accuracy > 50% after 3+ uses
   - **Efficient Storage**: Use `Bash` + `jq` to update JSON files atomically
   - **Run Cleanup**: Execute memory cleanup script after storing
   - **Update Only**: Don't create new patterns without validation

   **Memory Cleanup** (after workflow):
   - Delete complexity patterns with accuracy < 50% (after 3+ uses)
   - Delete unused patterns > 60 days old
   - Keep top 20 most accurate patterns per project
   - Delete failure modes unused > 30 days
   - Delete failure modes with success rate < 60%

6. **Failure Handling**
   - If a workflow or subagent fails, use the standardized Error Recovery Protocol:

   ## Error Recovery Protocol

   **Error Recovery Decision Tree**:

   ```
   Error occurred?
   ├─ Skill loading failed?
   │   ├─ File missing?
   │   │   └─ YES → Report error, offer: Retry / Continue without / Abort
   │   │   └─ NO → Continue
   │   ├─ Parse error?
   │   │   └─ YES → Report error, offer: Retry / Continue without / Abort
   │   │   └─ NO → Continue
   │   └─ Unknown error?
   │       └─ YES → Report error, offer: Retry / Continue without / Abort
   │       └─ NO → Continue
   ├─ Subagent invocation failed?
   │   ├─ Subagent missing?
   │   │   └─ YES → Report error, offer: Skip / Abort
   │   │   └─ NO → Continue
   │   ├─ Output invalid?
   │   │   └─ YES → Report error, offer: Retry / Request correction / Continue
   │   │   └─ NO → Continue
   │   └─ Execution error?
   │       └─ YES → Report error, offer: Retry / Skip / Abort
   │       └─ NO → Continue
   └─ Workflow execution failed?
       ├─ Phase 0 incomplete?
       │   └─ YES → Complete Phase 0, then retry
       │   └─ NO → Continue
       ├─ Validation failed?
       │   └─ YES → Fix issues, then retry
       │   └─ NO → Continue
       └─ Unknown error?
           └─ YES → Report error, offer: Retry / Abort
           └─ NO → Continue
   ```

   When any component fails, provide:
   1. **Context**: What was attempted (with evidence - file paths, commands run, error messages)
   2. **Problem**: What failed (specific error, exit code, or failure point)
   3. **Options**: Clear choices with implications:
      - **Retry**: Attempt again (if transient error likely)
      - **Continue without {component}**: Proceed with reduced functionality (if optional)
      - **Abort workflow**: Stop and restart (if critical failure)
      - **Custom**: User provides alternative instructions
   4. **Impact**: What each choice means:
      - Retry: May succeed, adds time
      - Continue: Workflow proceeds but missing {component} outputs
      - Abort: Loses progress, starts fresh
   5. **Default**: Recommended action (usually "Abort" for critical failures, "Retry" for transient)

   **Error Recovery Checklists** (step-by-step recovery paths):

   **Checklist 1: Skill Loading Failed**
   - [ ] Error detected (skill file missing, parse error, unknown error)
   - [ ] Identify error type (file missing / parse error / unknown)
   - [ ] Select recovery path (Retry / Continue without / Abort)
   - [ ] Execute recovery action
   - [ ] Validate recovery success (skill loaded / workflow continues / workflow aborted)
   - [ ] Continue workflow or abort

   **Checklist 2: Subagent Invocation Failed**
   - [ ] Error detected (subagent missing / output invalid / execution error)
   - [ ] Identify error type (missing / invalid output / execution error)
   - [ ] Select recovery path (Skip / Retry / Request correction / Abort)
   - [ ] Execute recovery action
   - [ ] Validate recovery success (subagent skipped / retried / corrected / workflow aborted)
   - [ ] Continue workflow or abort

   **Checklist 3: Workflow Execution Failed**
   - [ ] Error detected (Phase 0 incomplete / validation failed / unknown error)
   - [ ] Identify error type (Phase 0 incomplete / validation failed / unknown)
   - [ ] Select recovery path (Complete Phase 0 / Fix issues / Retry / Abort)
   - [ ] Execute recovery action
   - [ ] Validate recovery success (Phase 0 completed / issues fixed / workflow retried / workflow aborted)
   - [ ] Continue workflow or abort

   Example Error Recovery Message:

   ```
   ## Error Recovery Required

   **Context**: Attempted to load workflow skill 'review-workflow'
   - Read: plugins/cc10x/skills/review-workflow/SKILL.md
   - Error: File not found

   **Problem**: Review workflow skill file missing or inaccessible

   **Options**:
   1. **Retry**: Check alternative path or permissions
   2. **Continue without review workflow**: Use manual review process
   3. **Abort workflow**: Stop and verify cc10x plugin installation

   **Impact**:
   - Retry: May resolve if path/permission issue
   - Continue: Review functionality reduced
   - Abort: Ensures clean state but loses progress

   **Recommended**: Abort workflow (ensures clean state)

   **Please respond**: [Retry / Continue / Abort] or [Custom instruction]
   ```

   **Error Recovery Timeout**:
   - **Timeout Duration**: 5 minutes waiting for user response
   - **Timeout Behavior**:
     - Critical failures (workflow missing, skill loading failed): **Abort workflow** (default)
     - Transient failures (network error, file lock): **Retry once** (default)
     - Optional failures (subagent missing): **Continue without component** (default)
   - **Timeout Notification**: "No response after 5 minutes. Taking default action: {action}. Workflow {status}."
   - **Timeout Logging**: Log timeout event to `.claude/memory/workflow_history.json` with timestamp and default action taken
   - Never fabricate outputs for missing agents or skipped steps.
   - Wait for explicit user decision before proceeding (do not assume).
   - After timeout, proceed with default action and log the decision.

## Parallel Execution Strategy

**Dependency Analysis Protocol**:

1. **Build Dependency Graph**: For each workflow phase:
   - Identify all operations (subagents, skills, components, bugs)
   - Map dependencies: operation A → operation B (B requires A's output)
   - Map conflicts: operation A ⚠️ operation B (shared state, same files)
2. **Execution Mode Selection**:

   **PARALLEL (Safe)**:
   - ✅ No output dependencies (operation B doesn't need operation A's output)
   - ✅ Read-only operations (no state mutations)
   - ✅ Isolated contexts (separate subagent contexts)
   - ✅ Independent data (different files/components/bugs)
   - ✅ Validation after each (prevents error propagation)

   **SEQUENTIAL (Required)**:
   - ❌ Output → Input dependency (A's output feeds B's input)
   - ❌ State mutation → Read dependency (A mutates, B reads)
   - ❌ Validation gates (must wait for validation)
   - ❌ Feedback loops (B can trigger return to A)
   - ❌ Shared state (both modify same data)

3. **Workflow-Specific Parallel Execution Rules**:
   - **Review Workflow**: Analysis subagents (analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility) CAN run in parallel IF comprehensive review (read-only, independent, isolated contexts)
   - **Plan Workflow**: Planning subagents MUST run sequentially (planning-architecture-risk → planning-design-deployment, architecture informs design)
   - **Build Workflow**: Component subagents MUST run sequentially per component (component-builder → code-reviewer → integration-verifier), but components can run in parallel IF independent
   - **Debug Workflow**: Bug subagents MUST run sequentially per bug (bug-investigator → code-reviewer → integration-verifier), but bugs can run in parallel IF independent
   - **Validate Workflow**: No subagents (direct comparisons)

4. **Conflict Prevention Rules**:
   - Read-only subagents analyzing SAME code → PARALLEL (safe)
   - Subagents mutating DIFFERENT files → PARALLEL (safe)
   - Subagents with output dependencies → SEQUENTIAL (required)
   - Subagents in same workflow phase → Check dependencies first

5. **Fallback Strategy**:
   - If parallel execution fails → Automatically fallback to sequential
   - Log fallback reason for debugging
   - Continue with remaining operations

## Parallel Execution Safety Validation

**Conflict Detection Checklist** (before parallel execution):

- [ ] No output dependencies (operation B doesn't need A's output)
- [ ] No shared state mutations (operations don't modify same data)
- [ ] Read-only operations (no write conflicts)
- [ ] Isolated contexts (separate subagent contexts)
- [ ] Validation gates (validation occurs after all complete)
- [ ] Error isolation (failure of one doesn't corrupt others)

**Fallback Triggers**:

- Any conflict detected → Automatically fallback to sequential
- Parallel execution fails → Retry sequentially
- User preference for sequential → Honor user choice
- Complexity threshold exceeded → Sequential for safety

## Complexity Gate (Plan/Build)

If the complexity score is 2 or lower, warn that cc10x is optimized for higher-risk work and ask whether to proceed (yes/no). Pause until the user answers. Abort if the answer is "no" or no answer is provided.

## Complexity Rubric (1-5) - Functionality First

**Note**: Complexity scoring should consider functional complexity (user flows, system flows, integration flows) in addition to technical complexity.

### Base Scoring

- **1** - Single function (<50 LOC), no external dependencies, no test changes, no config changes, single user flow
- **2** - Single file (<200 LOC), trivial change, low risk, minimal test updates, simple user flow
- **3** - 2-5 files, moderate change, adds/updates tests, low/medium risk, some refactoring, multiple user flows or admin flow
- **4** - Multi-module change or new integration, notable risk/uncertainty, cross-file coordination needed, complex user/admin/system flows
- **5** - Cross-cutting or architectural impact, migrations/rollout considerations, breaking changes, complex multi-flow functionality

### Edge Case Handling

**Mixed Complexity**: If changes include both trivial and complex parts:

- Use the **highest score** (assume maximum risk)
- Document: "Mixed complexity detected: {trivial parts} and {complex parts}. Scoring: {highest score}"

**Unclear Architectural Impact**: If impact is uncertain:

- Default to **score 4** (assume risk exists)
- Ask user: "I cannot determine architectural impact. Is this change cross-cutting or isolated? (isolated=3, cross-cutting=4-5)"

**Refactor-Only Changes**: If no functional changes, only code structure:

- Score based on **file count** and **scope of refactor**
- Refactor within 1-2 files = score 2
- Refactor across 3-5 files = score 3
- Refactor across modules = score 4
- Large-scale architectural refactor = score 5

**Dependency Complexity**: Consider dependency changes:

- No new dependencies = no adjustment
- New dependency with clear migration path = +0.5 to score
- New dependency requiring significant integration = +1 to score
- Breaking dependency updates = +1.5 to score

**Calculation Method**: Start with base score, apply adjustments above, round to nearest integer (1-5).

### Examples

Example 1: "Add user registration form"

- 1 new component file, 1 API endpoint, tests = 3 files
- New database migration = moderate change
- **Score: 3**

Example 2: "Replace payment processor"

- Multiple files affected (payment service, config, tests)
- External API integration change = high risk
- **Score: 4**

Example 3: "Fix typo in comment"

- Single file, single line
- **Score: 1**

Example 4: "Refactor authentication across all modules"

- Multiple modules affected, architectural change
- **Score: 5**

## Quick Reference

**Workflow Indicators** (intent keywords):

- **Review**: review, audit, check, analyze, security, quality, performance, UX, accessibility
- **Plan**: plan, design, architect, structure, feature planning
- **Build**: build, implement, create, code, develop, feature
- **Debug**: debug, fix, error, bug, investigate, troubleshoot
- **Validate**: validate, verify, check alignment, compare

**File Purposes**:

- **Orchestrator Skill** (`plugins/cc10x/skills/cc10x-orchestrator/SKILL.md`): Main coordination logic, intent detection, workflow routing
- **Workflow Files** (`plugins/cc10x/skills/cc10x-orchestrator/workflows/*.md`): Workflow-specific instructions, phases, skill/subagent coordination
- **Skill Files** (`plugins/cc10x/skills/*/SKILL.md`): Domain-specific expertise, patterns, best practices
- **Subagent Files** (`plugins/cc10x/subagents/*/SUBAGENT.md`): Specialized AI personalities for specific tasks
- **Templates** (`plugins/cc10x/skills/cc10x-orchestrator/templates/*.md`): Reusable templates for functionality analysis

**Essentials** (must-know):

1. **Functionality First**: Always understand functionality (user/admin/system flows) BEFORE applying specialized checks
2. **Phase 0 Mandatory**: All workflows MUST execute Phase 0: Functionality Analysis FIRST
3. **Evidence Required**: All findings must include file:line citations or command exit codes
4. **Parallel Loading**: Load all independent skills in parallel for faster initialization
5. **Validation Gates**: Validate outputs between phases before proceeding
6. **Error Recovery**: Use Error Recovery Protocol with clear options and impacts

## Evidence-First Expectations

- Reviews must cite file paths and line numbers.
- Planning, build, and debug workflows must run the relevant verification commands before claiming completion.
- For every success statement, include a short "Verification Summary" that lists commands run, exit codes, and artefacts.

## Final Report - Output Format (REQUIRED)

**MANDATORY TEMPLATE** - All workflows must use this exact structure:

```markdown
# [Workflow Name] Report

## Executive Summary

[2-3 sentences summarizing outcome, key findings, and overall status]

## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented]
  [Bullet list of key steps, tools used, subagents invoked, skills loaded]

## Functionality Analysis

[Include complete functionality analysis from Phase 0 - user flows, admin flows, system flows, functional verification]

## Findings / Decisions

[Workflow-specific sections with file:line citations where applicable]

## Verification Summary

Scope: <files/modules>
Criteria: <list of what was verified - functionality FIRST, then other checks>
Commands:

- <command> -> exit <code>
- <command> -> exit <code>
  Evidence:
- <log/report snippet>
- <test output snippet>
  Risks / Follow-ups: <items still pending or needing attention>

## Recommendations / Next Steps

[Prioritized list of actionable next steps - functionality issues FIRST, then other concerns]

## Open Questions / Assumptions

[If any - list questions requiring user input or assumptions made]
```

**Pre-Final-Report Validation** (MANDATORY before presenting final report):

**CRITICAL**: This validation prevents incomplete reports. Execute BEFORE presenting final report.

1. **Phase Completion Audit**:
   - [ ] Phase 0 completed (functionality analysis)
   - [ ] All workflow phases completed (check workflow-specific phase list)
   - [ ] All phase success messages displayed
   - [ ] All gate checks passed
   - [ ] All phase completion checklists verified

2. **Skills Audit**:
   - [ ] Skills Inventory Check completed (see Phase 2)
   - [ ] ALL required skills from workflow Phase 2 loaded and documented in Actions Taken
   - [ ] ALL conditional skills loaded IF detection logic matched and documented
   - [ ] Each skill documented in Actions Taken with load status
   - [ ] No required skill missing
   - [ ] No conditional skill missing IF detection logic matched

3. **Subagents Audit**:
   - [ ] Subagents Inventory Check completed (see Phase 3)
   - [ ] ALL subagents that should be invoked are documented in Actions Taken
   - [ ] Execution mode documented (parallel/sequential)
   - [ ] Skip decisions documented with reasons (if any skipped)
   - [ ] Output validation documented for each subagent
   - [ ] No required subagent missing
   - [ ] No subagent listed that shouldn't have been invoked

4. **Evidence Audit**:
   - [ ] Functionality verification documented FIRST in Verification Summary
   - [ ] All findings have file:line citations
   - [ ] All commands have exit codes
   - [ ] Verification summary complete
   - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections

5. **Actions Taken Audit**:
   - [ ] Phase 0: Functionality Analysis documented
   - [ ] Phase 1: Input Validation/Complexity Gate documented
   - [ ] Phase 2: Skills loaded documented (ALL required + conditional IF detected)
   - [ ] Phase 3: Subagents invoked documented (ALL that should be invoked)
   - [ ] Phase 4+: Workflow-specific phases documented
   - [ ] Execution mode documented (parallel/sequential)
   - [ ] Skip decisions documented (if any)
   - [ ] Phase completion messages documented

6. **Workflow-Specific Audit**:

   **Review Workflow**:
   - [ ] 3 analysis subagents documented (or focused subagent if focused review)
   - [ ] code-reviewer documented IF code changes detected
   - [ ] integration-verifier documented IF integration changes detected
   - [ ] Parallel execution documented IF comprehensive review

   **Plan Workflow**:
   - [ ] planning-architecture-risk documented (FIRST)
   - [ ] planning-design-deployment documented (SECOND)
   - [ ] Sequential execution documented
   - [ ] Architecture outputs passed documented

   **Build Workflow**:
   - [ ] component-builder documented for each component
   - [ ] code-reviewer documented for each component (unless skipped)
   - [ ] integration-verifier documented for each component (unless skipped)
   - [ ] Sequential execution per component documented
   - [ ] Parallel execution between components documented (if independent)

   **Debug Workflow**:
   - [ ] bug-investigator documented for each bug
   - [ ] code-reviewer documented for each bug (unless skipped)
   - [ ] integration-verifier documented for each bug (unless skipped)
   - [ ] Sequential execution per bug documented
   - [ ] Parallel execution between bugs documented (if independent)

   **Validate Workflow**:
   - [ ] No subagents documented (direct analysis only)

**If ANY audit fails**:

- STOP final report generation
- Report: "CRITICAL: Pre-final-report validation failed. Missing: {list missing items}"
- Complete missing items
- Re-run all audits
- Do NOT present final report until ALL audits pass

**CRITICAL**: This validation is non-negotiable. Final report generation aborts if any audit fails.

**Validation**: Before presenting final report, verify:

**Actions Taken Validation** (CRITICAL - before final report):

**CRITICAL**: This validation ensures Actions Taken section is complete and accurate.

**Required Structure**:

```markdown
## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented]
- Phase 0: Functionality Analysis ✅ Complete
- Phase 1: [Phase name] ✅ Complete
- Phase 2: Skills Loaded ✅ Complete
  - Required skills loaded: [list ALL required skills with status]
  - Conditional skills loaded: [list conditional skills IF detected with status]
- Phase 3: Subagents Invoked ✅ Complete
  - Subagents invoked: [list ALL subagents that should be invoked with status]
  - Execution mode: [parallel/sequential for each group]
  - Skip decisions: [list any skipped subagents with reasons]
- Phase 4+: [Workflow-specific phases] ✅ Complete
- Tools used: [list tools used]
- Commands run: [list key commands with exit codes]
```

**Validation Checklist**:

- [ ] Phase 0: Functionality Analysis documented
- [ ] ALL required skills listed (check against workflow Phase 2 required skills list)
- [ ] ALL conditional skills listed IF detected (check against detection logic)
- [ ] ALL subagents invoked listed (check against workflow Phase 3 subagent list)
- [ ] Skip decisions documented (if any subagents/skills skipped, reason documented)
- [ ] Execution mode documented (parallel/sequential for each subagent group)
- [ ] Phase completion messages documented (all phases completed)
- [ ] Verification summary includes functionality verification FIRST
- [ ] No required skill missing
- [ ] No required subagent missing (unless skip condition met)
- [ ] No phase missing

**If ANY item missing**:

- Do NOT proceed to final report
- Complete missing items first
- Re-run validation
- Do NOT present final report until ALL items validated

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes functionality verification FIRST, then other checks
- [ ] File:line citations provided for all findings
- [ ] Recommendations are prioritized (functionality issues first)
- [ ] All subagents/skills used are documented in Actions Taken

## Memory Integration

**Purpose**: Use filesystem-based memory (`.claude/memory/`) to persist workflow state, patterns, and preferences across conversations.

**NOTE**: Anthropic's Memory Tool (API beta) is **NOT available in Claude Code**. This integration uses filesystem-based memory.

**Memory Usage**:

- **Before Complexity Scoring**: Query `.claude/memory/patterns.json` for similar tasks and use learned complexity scores as reference
- **After Workflow Completion**: Store workflow outcomes, learned patterns, and user preferences in JSON files
- **Pattern Learning**: Store complexity patterns, failure modes, and successful approaches in `.claude/memory/`

**What to Store**:

- Complexity patterns: `.claude/memory/patterns.json` → Task types → complexity scores → accuracy
- Failure modes: `.claude/memory/failure_modes.json` → Common errors → root causes → fixes
- User preferences: `.claude/memory/preferences.json` → Review depth, build approach, test coverage targets
- Workflow checkpoints: `.claude/memory/snapshots/` → Phase progress, component state, pending tasks

**Implementation**: See `plugins/cc10x/skills/memory-tool-integration/SKILL.md` for detailed guidance on filesystem-based memory usage patterns, including query patterns, storage procedures, and cleanup scripts.

## Web Fetch Integration

**Purpose**: Use Web Fetch Tool to load external documentation, API specifications, and reference materials when needed.

**When to Use**:

- External APIs mentioned: Fetch API documentation before planning
- Libraries/frameworks: Load documentation before building
- External services: Fetch service docs for integration
- Reference materials: Load guides, standards, best practices

**Integration Points**:

- **Planning Workflow**: Fetch API specs, framework docs, integration guides
- **Build Workflow**: Load library docs, SDK examples, framework guides
- **Review Workflow**: Fetch security standards, coding guidelines, best practices
- **Debug Workflow**: Load error docs, troubleshooting guides, stack trace resources

**Best Practices**:

- Cache frequently accessed docs
- Validate URLs before fetching
- Extract only relevant sections
- Cite sources in workflow output

**Integration**: Load `web-fetch-integration` skill for detailed guidance on web fetch usage.

## Context Editing (Sep 2025)

**Available Strategies**:

- Clear older tool results when approaching limits
- Clear thinking blocks automatically (`clear_thinking_20251015`)
- Automatic context cleanup for long conversations

**For Long Workflows**:

- Explicit checkpointing at major phases
- Summarizing intermediate results
- Document state between phases

## References

- Workflows: `plugins/cc10x/skills/cc10x-orchestrator/workflows/`
- Verification guardrails: `plugins/cc10x/skills/verification-before-completion/SKILL.md`
- Orchestration Coordination Matrix: `audit/orchestration-coordination-matrix.md` (complete skill/subagent activation matrix)
- Anthropic Context Editing: https://docs.claude.com/en/docs/build-with-claude/context-editing
- Anthropic Memory Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool

Keep this skill concise (<500 lines) and ASCII-only so it stays compliant with Anthropic marketplace requirements.
