# Orchestrator Workflow Coordination

Detailed workflow coordination, skill loading optimization, and subagent invocation rules.

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
