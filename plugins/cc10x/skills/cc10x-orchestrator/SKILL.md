---
name: cc10x-orchestrator
description: Primary orchestrator for cc10x. Interprets user intent and coordinates review, planning, build, and debug workflows in line with Anthropic's skills and subagent contracts. Honors focus requests, enforces evidence-first rules, and never invokes non-existent agents. Use for complex multi-step engineering tasks that need structured coordination.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# cc10x Orchestrator Skill

## Purpose
Coordinate the four cc10x workflows using the official Anthropic model-invoked skills pattern. The orchestrator:
- Identifies the requested outcome (review, plan, build, debug).
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

## Operation
1. **Intent and Context Check**
   - **Intent Keyword Mapping** (deterministic): Match user request to workflow using explicit keyword mapping:
     
     **Intent Keywords**:
     - **review**: ["review", "audit", "quality check", "security audit", "analyze code", "code review", "assess", "evaluate", "inspect", "examine"]
     - **plan**: ["plan", "design", "architect", "create plan", "roadmap", "strategy", "architecture", "system design", "feature design"]
     - **build**: ["build", "implement", "create", "write", "code", "develop", "make", "add feature", "implement feature", "build feature"]
     - **debug**: ["debug", "fix", "error", "bug", "investigate", "failure", "broken", "issue", "problem", "troubleshoot", "diagnose"]
     - **validate**: ["validate", "verify", "check", "confirm implementation", "alignment check", "consistency check"]
     
     **Matching Logic**:
     1. Scan user request for intent keywords (case-insensitive)
     2. Count matches per workflow (one keyword can match multiple workflows)
     3. If single workflow has >0 matches → select that workflow
     4. If multiple workflows have matches → Intent Disambiguation required
     5. If no matches → ask user: "Which workflow should I run? (review/plan/build/debug/validate)"
     
   - **Intent Disambiguation**: If user request contains multiple workflow keywords (e.g., "review and plan"), list detected workflows: [review, plan, build, debug]. Ask user: "I detected multiple intents. Which should I execute? (or 'both' for sequential)". Wait for explicit selection before proceeding.
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
   - **Skill Loading Verification**: After loading each skill referenced by the workflow, verify success:
     - Read first 100 chars of SKILL.md to confirm content loaded
     - If loading fails, report immediately: "Skill '{name}' failed to load: {error details}"
     - Present options: "Continue without {skill} (functionality reduced)? Abort workflow? Retry loading?"
     - Wait for user decision before proceeding
   - Follow workflow instructions exactly. Workflows now reference only real subagents and skills.
   - Record which domain skills are invoked so results can point to specific guidance files.
   
   **Subagent Invocation Rules** (CRITICAL):
   - **Verify existence FIRST**: Before invoking any subagent, verify it exists in `plugin.json` or `.claude/agents/`
   - **Check skip conditions**: Each workflow defines "when NOT to invoke" - check these BEFORE invocation
   - **Respect user overrides**: If user explicitly skips a subagent, document and skip it
   - **Sequential only**: Never invoke multiple subagents in parallel (each gets separate context window)
   - **Context isolation**: Each subagent starts fresh - provide all needed context explicitly
   - **Confirmation on skip**: If skipping subagent, ask user: "Skipping {subagent-name} due to {reason}. Proceed? (yes/no)"

### Tool Access Precedence
- When multiple skills are active, the orchestrator/workflow tool set governs delegation and verification. Domain skills may restrict themselves (e.g., Read/Grep/Glob), but they do not prevent the orchestrator/workflow from using `Task` or `Bash` to delegate/verify.

5. **Result Compilation**
   - Summarise findings with severity or priority (high/medium/low) based on evidence.
   - Link each recommendation to the skill or subagent that produced it.
   - Surface open questions and next-step offers without assuming consent.

   **Memory Integration** (filesystem-based, optimized):
   - **Validate Patterns First**: Compare predicted complexity → actual complexity
   - **Update Accuracy**: Calculate accuracy = (matches / total_uses) * 100
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

3. **Conflict Prevention Rules**:
   - Read-only subagents analyzing SAME code → PARALLEL (safe)
   - Subagents mutating DIFFERENT files → PARALLEL (safe)
   - Subagents with output dependencies → SEQUENTIAL (required)
   - Subagents in same workflow phase → Check dependencies first

4. **Fallback Strategy**:
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

## Complexity Rubric (1-5)

### Base Scoring
- **1** - Single function (<50 LOC), no external dependencies, no test changes, no config changes
- **2** - Single file (<200 LOC), trivial change, low risk, minimal test updates
- **3** - 2-5 files, moderate change, adds/updates tests, low/medium risk, some refactoring
- **4** - Multi-module change or new integration, notable risk/uncertainty, cross-file coordination needed
- **5** - Cross-cutting or architectural impact, migrations/rollout considerations, breaking changes

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
[Bullet list of key steps, tools used, subagents invoked, skills loaded]

## Findings / Decisions
[Workflow-specific sections with file:line citations where applicable]

## Verification Summary
Scope: <files/modules>
Criteria: <list of what was verified>
Commands:
- <command> -> exit <code>
- <command> -> exit <code>
Evidence:
- <log/report snippet>
- <test output snippet>
Risks / Follow-ups: <items still pending or needing attention>

## Recommendations / Next Steps
[Prioritized list of actionable next steps]

## Open Questions / Assumptions
[If any - list questions requiring user input or assumptions made]
```

**Validation**: Before presenting final report, verify:
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes commands with exit codes
- [ ] File:line citations provided for all findings
- [ ] Recommendations are prioritized
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

**Implementation**: Load `memory-tool-integration` skill for detailed guidance on filesystem-based memory usage patterns.

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
- Anthropic Context Editing: https://docs.claude.com/en/docs/build-with-claude/context-editing
- Anthropic Memory Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool

Keep this skill concise (<500 lines) and ASCII-only so it stays compliant with Anthropic marketplace requirements.
