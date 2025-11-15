# REVIEW Workflow - Evidence Based Code Analysis

**CRITICAL**: This workflow MUST be activated through cc10x-orchestrator. Do NOT execute this workflow directly. The orchestrator provides required context, coordinates skill loading, and manages subagent invocation. Direct execution bypasses all validation mechanisms.

**See SHARED-ENFORCEMENT.md for MANDATORY execution mode, enforcement rules, guardrails, and validation gates that apply to ALL workflows.**

**Triggered by:** User asks for review, audit, or quality/security checks.

## WHEN/HOW/WHY - REVIEW Workflow

### WHEN to Use This Workflow

**Keywords that trigger REVIEW workflow:**

- review, reviewing, reviewer, review this, review the
- audit, auditing, auditor, audit this
- analyze, analysis, analyzing, analyze this
- assess, assessment, assessing, assess this
- evaluate, evaluation, evaluating, evaluate this
- inspect, inspection, inspecting, inspect this
- examine, examination, examining, examine this

**Example user requests:**

- "review this authentication code"
- "audit this API for security issues"
- "analyze this component for performance"
- "assess code quality"

### HOW Orchestrator Selects This Workflow

**Detection Process:**

1. User says keyword like "review" → Orchestrator skill loads automatically (via description keywords)
2. Orchestrator scans user request for workflow keywords
3. If "review", "audit", "analyze", "assess", "evaluate", "inspect", or "examine" detected → REVIEW workflow selected
4. Orchestrator activates this workflow file
5. Workflow executes phases: Functionality Analysis → Input Validation → Load Skills → Analysis Subagents → Synthesis → Report

**Decision Tree:**

```
User request contains "review"/"audit"/"analyze"/"assess"/"evaluate"/"inspect"/"examine"?
├─ YES → REVIEW workflow
└─ NO → Check other workflow keywords
```

### WHY Use REVIEW Workflow vs Others

**Use REVIEW workflow when:**

- You need to analyze existing code for issues
- You need security/quality/performance/UX/accessibility checks
- You need code audit before PR merge
- You need to identify problems in existing code

**REVIEW vs PLAN:**

- REVIEW: Analyze existing code (backward-looking)
- PLAN: Design new features (forward-looking)

**REVIEW vs BUILD:**

- REVIEW: Analyze code (analysis)
- BUILD: Write code (creation)

**REVIEW vs DEBUG:**

- REVIEW: General code analysis (broad)
- DEBUG: Fix specific bugs (focused)

**REVIEW vs VALIDATE:**

- REVIEW: Analyze code quality (quality focus)
- VALIDATE: Verify alignment with plan (alignment focus)

**See SHARED-ENFORCEMENT.md for TL;DR Quick Checklist, Guardrails, and Runtime Compliance Checks.**

**See orchestrator REFERENCE.md for tool usage guides and search guidance.**

## Phase 0 - Functionality Analysis (MANDATORY)

**CRITICAL**: This phase MUST be completed before any skill loading or subagent dispatching. Understanding functionality is the foundation for all review activities.

**Purpose**: Understand what the code is supposed to do (user flows, admin flows, system flows) and verify it works before applying security, quality, performance, UX, or accessibility checks.

**Task Tool Usage** (phase tracking):

- Create tasks for all workflow phases at start:
  ```
  Task: Create tasks for workflow phases
  - Phase 0: Functionality Analysis (in_progress)
  - Phase 1: Input Validation (pending)
  - Phase 2: Load Required Skills (pending)
  - Phase 3: Dispatch Analysis Subagents (pending)
  - Phase 4: Synthesis (pending)
  - Phase 5: Verification Summary (pending)
  - Phase 5.5: Context Preservation (mandatory, pending)
  - Phase 6: Present Results (pending)
  ```
- Update task status as phases complete:
  ```
  Task: Update Phase 0 status to completed
  Task: Update Phase 1 status to in_progress
  ```

**Process**:

1. **Load Functionality Analysis Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`

**MANDATORY Visual Asset Check**:

**CRITICAL**: Run this bash command even if user says "no visuals":

```bash
# Check for visual assets in common locations
find . -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.pdf" \) \
  \( -path "*/mockups/*" -o -path "*/designs/*" -o -path "*/screenshots/*" -o -path "*/visuals/*" -o -path "*/assets/*" \) \
  2>/dev/null | head -20
```

**IF visual files found**:

- Analyze each visual file using Read tool (read first 100 lines to understand content)
- Document key design elements in functionality analysis
- Reference visuals in user flow documentation
- Note fidelity level (high/low) and design completeness
- Include visual references in findings section

**IF no visual files found**:

- Document: "No visual assets detected. Proceeding with code-only analysis."

2. **Analyze Target Scope**:
   - Read the files/directories to be reviewed
   - Understand the intended functionality
   - Document user flows, admin flows (if applicable), and system flows
   - Identify integration flows if external systems are involved
3. **Functional Verification**:
   - If possible, verify functionality works (run tests, check logs, manual verification)
   - Document any functional gaps or issues observed
   - If functionality cannot be verified, document limitation and proceed
4. **Research Needed** (if applicable):
   - Identify external APIs, constraints, or documentation needed
   - Plan external resource checks (will be executed in Phase 1)
5. **Output**: Complete functionality analysis using template format:

   ```markdown
   ## Functionality Analysis

   ### What Does User Need?

   [Clear description of functionality]

   ### User Flow

   1. [Step 1: User action]
   2. [Step 2: System response]
   3. [Step 3: User sees result]
      ...

   ### Admin Flow (if applicable)

   [Similar structure]

   ### System Flow

   1. [Step 1: System receives input]
   2. [Step 2: System processes]
   3. [Step 3: System stores/transforms]
   4. [Step 4: System sends output]
      ...

   ### Integration Flow (if applicable)

   [Similar structure]

   ### Research Needed (if applicable)

   - [ ] External API documentation
   - [ ] Integration constraints
   - [ ] Error handling patterns

   ### Functional Verification

   - [ ] User flow works (tested/verified)
   - [ ] Admin flow works (if applicable, tested/verified)
   - [ ] System flow works (tested/verified)
   - [ ] Integration flow works (if applicable, tested/verified)
   - [ ] Observed Functional Gaps/Issues: [list if any]
   ```

**Gate Check**: Before proceeding to Phase 1, ALL items below MUST be checked:

- [ ] Functionality analysis complete (user flow, admin flow if applicable, system flow documented)
- [ ] Functional verification attempted (run tests, check logs, manual verification) OR limitation documented
- [ ] Research needs identified (external APIs, constraints, documentation) if applicable
- [ ] Template format followed (all required sections completed)
- [ ] Functionality clear and understood (no ambiguous requirements)

**CRITICAL**: Do NOT proceed to Phase 1 until ALL items above are checked. If any item is incomplete:

- Ask user: "Functionality unclear. Please clarify: What is this code supposed to do? What are the user flows?"
- Do NOT proceed until functionality is understood and all gate check items are complete

**Ask Questions Tool Usage** (when functionality unclear):

- Use the askquestion tool to clarify requirements before proceeding
- Ask specific questions about functionality:
  - What are the specific user flows?
  - What are the acceptance criteria?
  - What are the constraints?
  - What are the dependencies?
- Proceed with functionality analysis using answers

**Example**:

```
Use the askquestion tool to clarify requirements:
- What are the specific user flows for this code?
- What are the acceptance criteria?
- What are the technical constraints?
- What are the business constraints?
```

**Memory Integration** (optimized):

- **Store Functionality Patterns**: After workflow completes, save successful functionality analysis patterns to `.claude/memory/patterns.json` (only if validated effective)
- **Query Similar Functionality**: Check `.claude/memory/patterns.json` for similar functionality patterns (use semantic match, top 3 only)

**Validation Gate** (before proceeding to Phase 1):

- [ ] Phase 0 complete (functionality analysis documented, gate checks passed)
- [ ] Output validated (format matches template, all required sections present)
- [ ] Evidence verified (flows documented, functional verification attempted or limitation documented)

**CRITICAL**: Do NOT proceed to Phase 1 until ALL validation items above are checked.

**Display Success Message** (after Phase 0 completion):

```
✅ Phase 0 Complete: Functionality Analysis

Analyzed:
- User flows: [X] flows identified
- Admin flows: [Y] flows identified (if applicable)
- System flows: [Z] flows identified
- Visual assets: [N] assets found (if any)

Verified:
- Functionality works: ✅ Yes / ⚠️ Limitation documented
- Test coverage: ✅ Adequate / ⚠️ Needs improvement

Next: Proceeding to Phase 1 - Input Validation
```

**Phase 0 Completion Checklist** (MANDATORY before proceeding to Phase 1):

**CRITICAL**: Do NOT proceed to Phase 1 until ALL items below are checked.

- [ ] Phase 0 success message displayed
- [ ] All required actions for Phase 0 completed
- [ ] All outputs validated (format, evidence, file:line citations)
- [ ] Actions Taken section updated with Phase 0 activities
- [ ] Gate check passed (if applicable)
- [ ] No errors or warnings requiring attention
- [ ] Phase 0 documented in Actions Taken with completion status

**Phase-Specific Checks**:

**Phase 0 (Functionality Analysis)**:

- [ ] Functionality analysis template completed
- [ ] User flows documented
- [ ] Admin flows documented (if applicable)
- [ ] System flows documented
- [ ] Integration flows documented (if applicable)
- [ ] Functional verification attempted or limitation documented
- [ ] Visual asset check completed (if applicable)

**If ANY item unchecked**:

- STOP workflow execution
- Complete missing items
- Re-run checklist
- Do NOT proceed until ALL items checked

**CRITICAL**: This checklist is non-negotiable. Workflow aborts if any item fails.

## Phase 1 - Input Validation

**Memory Integration** (optimized):

- **Load Preferences**: Query `.claude/memory/preferences.json` for review preferences (if exists)
- **Load Patterns Once**: Read `.claude/memory/patterns.json` ONCE, cache for workflow duration
- **Query Common Issues**: Use `jq` to filter patterns matching code type/structure (top 5 only)
- **Validation**: Only use patterns with high success_rate or frequent occurrences

1. Confirm files, directories, or patterns to review.
2. Ask for clarification if the scope is ambiguous.
3. **Scope Size Validation**: Define "very small" and handle accordingly:
   - Single file < 50 lines = warn: "Scope is small (1 file, {N} lines). Continue or use lighter review?"
   - Single function < 20 lines = warn: "Scope is very small (1 function, {N} lines). Continue?"
   - If user confirms, proceed; if not, ask for broader scope

**External Resource Check** (smart Q&A caching):

- **Check Cache First**: Lookup {url, prompt} combinations in `.claude/memory/web_cache/cache_index.json`
- **Cache Logic**:
  - Create hash from `{url}_{prompt}` for each planned question
  - Standards/Guidelines: 72h TTL (use shorter TTL since content changes)
  - If cached and TTL valid → use cached answer (skip fetch)
  - If cached but expired → re-fetch with same prompt
  - If not cached → WebFetch with prompt and cache answer
- Check if review needs external standards:
  - Security standards? → Ask: "What are the OWASP Top 10 security risks and how do I check for injection attacks, broken authentication, and sensitive data exposure?"
  - Coding standards? → Ask: "What are the coding standards for error handling, naming conventions, and code structure?"
  - Performance standards? → Ask: "What performance optimization techniques apply to [scenario]? How do I identify bottlenecks?"
- Ask user: "Should I fetch external standards? Will ask {N} targeted questions. Found {M} in cache. Proceed? (yes/no)"

**Workflow State Persistence** (Checkpoint System):

- **Checkpoint After Each Phase**: Save workflow state to `.claude/memory/workflow_state/review_{timestamp}.json`
- **Checkpoint Format**:
  ```json
  {
    "workflow": "review",
    "phase": "Phase_2_Dispatch_Analysis_Subagents",
    "timestamp": "2025-10-29T10:00:00Z",
    "state": {
      "files_reviewed": [...],
      "subagents_completed": [...],
      "findings": {...},
      "conflicts": [...]
    },
    "output_file": ".claude/docs/reviews/review-{timestamp}.md",
    "output_saved": false,
    "next_phase": "Phase_3_Synthesis"
  }
  ```
- **Resume Logic**: If resuming after interruption:
  1. Read most recent checkpoint: `jq -s 'sort_by(.timestamp) | reverse | .[0]' .claude/memory/workflow_state/review_*.json`
  2. Validate checkpoint state (files present, subagents valid)
  3. Continue from `next_phase` with checkpoint state restored
  4. Ask user: "Resuming from Phase {N}. Continue from checkpoint or restart?"
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2, Phase 3 (after each subagent), Phase 4, Phase 5 completion

**If resuming after compaction or context is unclear**, use checkpoint system:

- Read most recent checkpoint from `.claude/memory/workflow_state/review_*.json`
- If checkpoint exists: Restore state and continue from `next_phase`
- If no checkpoint: Read `.claude/memory/snapshots/` most recent `snapshot-*.md` and `.claude/memory/WORKING_PLAN.md` as fallback

**Validation Gate** (before proceeding to Phase 2):

- [ ] Phase 1 complete (inputs validated, scope confirmed, questions answered)
- [ ] Output validated (scope clear, files confirmed)
- [ ] Evidence verified (files exist, scope documented)

**CRITICAL**: Do NOT proceed to Phase 2 until ALL validation items above are checked.

**Display Success Message** (after Phase 1 completion):

```
✅ Phase 1 Complete: Input Validation

Validated:
- Files: [X] files validated
- Scope: ✅ Confirmed
- Questions: [Y] questions answered (if any)

Next: Proceeding to Phase 2 - Load Required Skills
```

**Phase 1 Completion Checklist** (MANDATORY before proceeding to Phase 2):

**CRITICAL**: Do NOT proceed to Phase 2 until ALL items below are checked.

- [ ] Phase 1 success message displayed
- [ ] All required actions for Phase 1 completed
- [ ] All outputs validated (format, evidence, file:line citations)
- [ ] Actions Taken section updated with Phase 1 activities
- [ ] Gate check passed (if applicable)
- [ ] No errors or warnings requiring attention
- [ ] Phase 1 documented in Actions Taken with completion status

**Phase-Specific Checks**:

**Phase 1 (Input Validation/Complexity Gate)**:

- [ ] Inputs validated (files exist, scope clear)
- [ ] Complexity assessed (if applicable)
- [ ] External resources checked (if applicable)
- [ ] User approval obtained (if complexity <=2)

**If ANY item unchecked**:

- STOP workflow execution
- Complete missing items
- Re-run checklist
- Do NOT proceed until ALL items checked

**CRITICAL**: This checklist is non-negotiable. Workflow aborts if any item fails.

## Phase 2 - Load Required Skills

**Required Skills** (all exist under `plugins/cc10x/skills/`):

- `project-context-understanding` - **MANDATORY** (understand project structure, dependencies, and conventions before reviewing)
- `session-summary` - **MANDATORY** (load early for context preservation across compaction)
- `risk-analysis`
- `code-review-patterns` (covers security, quality, performance)
- `review-workflow` - **MANDATORY** (workflow-specific guidance and coordination)
- `verification-before-completion` - **MANDATORY** (verify findings before completion)
- `memory-tool-integration` (filesystem-based memory always available)

**Conditional Skills**:

- `frontend-patterns` - **MANDATORY** when UI components detected (file patterns: `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.astro`, `components/`, `ui/`, `pages/`, `views/`, `src/components/`, `app/components/`, `lib/components/`, `shared/components/`)
- `design-patterns` - Load if design patterns mentioned or pattern review needed (keywords: "pattern", "design pattern", "API design", "component design", "architectural pattern", "structural pattern", "behavioral pattern", "creational pattern", "design system")
- `architecture-patterns` - Load if integration or API code detected (covers integration and API design patterns)
- `test-driven-development` - Load if integration code detected OR test files detected (file patterns: `*.test.{ts,tsx}`, `*.spec.{ts,tsx}`, `__tests__/`, `tests/`, `test/`, keywords: "test", "testing", "TDD", "unit test", "integration test", "e2e test", "spec")
- `debugging-patterns` - Load if integration code detected OR error handling code detected (file patterns: `*error*.{ts,tsx}`, `*exception*.{ts,tsx}`, `error-handlers/`, `exceptions/`, keywords: "error handling", "exception", "try-catch", "error recovery")
- `web-fetch-integration` - **MANDATORY** when external dependencies detected (keywords: "API", "endpoint", "REST", "GraphQL", "external service", "library", "package", "npm", "import", "require", "third-party", "external", "integration", "webhook")

**Detection Logic**:

- UI Components: File patterns `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.astro`, `components/`, `ui/`, `pages/`, `views/`, `src/components/`, `app/components/`, `lib/components/`, `shared/components/`, keywords "button", "modal", "layout", "component", "page", "screen", "view", "widget"
- Design Patterns: Keywords "pattern", "design pattern", "API design", "component design", "architectural pattern", "structural pattern", "behavioral pattern", "creational pattern", "design system"
- Integration Code: File patterns `*api*.{ts,tsx,js,jsx}`, `*service*.{ts,tsx}`, `*integration*.{ts,tsx}`, `api/`, `services/`, `integrations/`, `external/`, `third-party/`, `handlers/`, `resolvers/`, keywords "API", "endpoint", "fetch", "axios", "external service", "HTTP client", "RPC", "gRPC", "webhook", "third-party", "external API"
- API Code: File patterns `*api*.{ts,tsx}`, `*endpoint*.{ts,tsx}`, `routes/`, `controllers/`, `handlers/`, `resolvers/`, `services/`, `api/`, `endpoints/`, keywords "REST", "GraphQL", "endpoint", "route", "controller", "handler", "resolver", "service", "microservice"
- Test Files: File patterns `*.test.{ts,tsx}`, `*.spec.{ts,tsx}`, `__tests__/`, `tests/`, `test/`, keywords "test", "testing", "TDD", "unit test", "integration test", "e2e test", "spec"
- Error Handling: File patterns `*error*.{ts,tsx}`, `*exception*.{ts,tsx}`, `error-handlers/`, `exceptions/`, keywords "error handling", "exception", "try-catch", "error recovery"
- Config Files: File patterns `*.config.{js,ts,json}`, `*.env`, `config/`, keywords "config", "configuration", "settings"
- External Dependencies: Keywords "API", "endpoint", "REST", "GraphQL", "external service", "library", "package", "npm", "import", "require", "third-party", "external", "integration", "webhook"

**Skill Loading Strategy**:

- All required skills are independent (no dependencies between them)
- **Load all required skills in parallel** for faster initialization
- **Load conditional skills** (`frontend-patterns`, `design-patterns`, `architecture-patterns`, `debugging-patterns`, `test-driven-development`, `web-fetch-integration`) based on detection logic, still in parallel with required skills

**Skill Loading Verification Protocol**:
For each skill above:

1. Read first 100 chars of `plugins/cc10x/skills/{skill-name}/SKILL.md` to verify file exists
2. Parse YAML frontmatter to verify valid format
3. Check body content exists (not empty)
4. If any verification fails:
   - Report immediately: "Skill '{name}' failed to load: {error details}"
   - Present options:
     - **Continue without {skill}**: Proceed with reduced analysis (functionality reduced)
     - **Abort workflow**: Stop and verify skill exists (ensures complete analysis)
     - **Retry loading**: Attempt again (if transient error)
   - Wait for user decision before proceeding
5. Document successfully loaded skills in Actions Taken section

**If Skill Missing**:

- Report: "Required skill '{name}' not found. Available skills: [list]"
- Ask user: "Continue without {skill} or abort workflow?"

**Validation Gate** (before proceeding to Phase 3):

- [ ] Phase 2 complete (all required skills loaded, conditional skills loaded if detected)
- [ ] Output validated (skills loaded successfully, verification passed)
- [ ] Evidence verified (skill files exist, content loaded)

**CRITICAL**: Do NOT proceed to Phase 3 until ALL validation items above are checked.

**Display Success Message** (after Phase 2 completion):

```
✅ Phase 2 Complete: Skills Loaded

Loaded:
- Required skills: [X] skills loaded
- Conditional skills: [Y] skills detected and loaded (if any)

Next: Proceeding to Phase 3 - Dispatch Analysis Subagents
```

**Phase 2 Completion Checklist** (MANDATORY before proceeding to Phase 3):

**CRITICAL**: Do NOT proceed to Phase 3 until ALL items below are checked.

- [ ] Phase 2 success message displayed
- [ ] All required actions for Phase 2 completed
- [ ] All outputs validated (format, evidence, file:line citations)
- [ ] Actions Taken section updated with Phase 2 activities
- [ ] Gate check passed (if applicable)
- [ ] No errors or warnings requiring attention
- [ ] Phase 2 documented in Actions Taken with completion status

**Phase-Specific Checks**:

**Phase 2 (Load Required Skills)**:

- [ ] Skills Inventory Check completed (see orchestrator)
- [ ] ALL required skills loaded and documented
- [ ] Conditional skills loaded IF detected and documented
- [ ] Each skill marked as "loaded successfully" or "failed to load"

**If ANY item unchecked**:

- STOP workflow execution
- Complete missing items
- Re-run checklist
- Do NOT proceed until ALL items checked

**CRITICAL**: This checklist is non-negotiable. Workflow aborts if any item fails.

## Phase 3 - Dispatch Analysis Subagents

**When to Invoke Subagents**:

- **INVOKE** - Scope is substantial: Multiple files OR single file >100 lines OR explicit user request
- **INVOKE** - Code changes detected: Modified/new files present
- **INVOKE** - Always invoke `code-reviewer` subagent (covers security, quality, performance, UX, accessibility)

**When NOT to Invoke Subagents** (skip to save context/tokens):

- **SKIP** - Scope too small: Single file < 50 lines OR single function < 20 lines → Ask user: "Scope is very small ({N} lines). Skip subagent analysis or proceed?" (Always ask, don't auto-skip)
- **SKIP** - Read-only files: If scope contains only markdown/docs files (no code) → Ask user: "Scope contains only documentation files. Skip code review or proceed?" (Config files should be reviewed for security issues)
- **SKIP** - User explicitly skips: If user says "skip review" or "quick check only" → Document in Actions Taken and skip subagent invocation
- **SKIP** - No code files: If scope is empty or contains no code files → Report: "No code files in scope. Subagent analysis skipped."

**Subagent Selection & Execution Strategy**:

**Step 1: Request Focus Detection**:

- Scan user request for focus keywords:
  - "security" or "vulnerabilities" → Security-focused
  - "performance" or "optimization" → Performance-focused
  - "UX" or "accessibility" → UX/Accessibility-focused
  - General "review" or "audit" → Comprehensive review

**Step 2: File Scope Analysis**:

- **Multiple independent files** (2+ files, no dependencies between them):
  - Analyze file dependencies: Check if files import each other or share state
  - If independent: Review files in parallel using parallel subagent invocation
  - If dependent: Review sequentially (respect dependencies)
- **Single file or dependent files**: Review sequentially

**Step 3: Conditional Subagent Selection**:

- **IF focused request** (security/performance/UX mentioned):
  - Invoke ONLY the relevant subagent:
    - Security/Performance/Quality-focused → `code-reviewer` subagent (covers all dimensions)
    - UX/Accessibility-focused → `code-reviewer` subagent (covers UX, UI design, accessibility for UI code)
- **IF general request** (comprehensive review):
  - Invoke `code-reviewer` subagent (covers all dimensions):
    ```
    Execution:
    └─ code-reviewer (covers security, quality, performance, UX, accessibility)
    ```

- **Default behavior** (general/comprehensive review): Invoke `code-reviewer` subagent

**CRITICAL**: Before invoking `code-reviewer` subagent, verify required skills are loaded:

- ✅ `code-review-patterns` - Required skill (already loaded)
- ✅ `verification-before-completion` - Required skill (already loaded)
- ⚠️ `frontend-patterns` - Conditional skill (load if UI code detected) - Required for `code-reviewer` when UI code present

**If UI code detected**: Ensure `frontend-patterns` is loaded before invoking `code-reviewer`

- **INVOKE integration-verifier** - Integration code present: After code-reviewer completes (if invoked), if integration code detected → Invoke `integration-verifier` for integration verification
  - **When to invoke**: Integration code detected (API endpoints, external services, data flows, file patterns: `*api*.{ts,tsx}`, `*service*.{ts,tsx}`, `*integration*.{ts,tsx}`, `api/`, `services/`, `integrations/`, `external/`, `third-party/`, keywords: "API", "endpoint", "external service", "integration")
  - **When NOT to invoke**: No integration code detected, user explicitly skips integration verification
  - **Execution**: Sequential after code-reviewer (if invoked)

**CRITICAL**: Before invoking `integration-verifier` subagent, verify required skills are loaded:

- ⚠️ `architecture-patterns` - Conditional skill (load if integration code detected) - Required for `integration-verifier`
- ⚠️ `debugging-patterns` - Conditional skill (load if integration code detected) - Required for `integration-verifier`
- ⚠️ `test-driven-development` - Conditional skill (load if integration code detected) - Required for `integration-verifier`
- ✅ `verification-before-completion` - Required skill (already loaded)

**If integration code detected**: Ensure `architecture-patterns`, `debugging-patterns`, and `test-driven-development` are loaded before invoking `integration-verifier`

**Parallel Execution for Multiple Files**:

- **When to use parallel execution**: Multiple independent files (2+ files, no dependencies)
- **How to detect independence**: Files don't import each other, don't share state, operate independently
- **Execution mode**: Invoke `code-reviewer` subagent for each file in parallel
- **Fallback**: If parallel execution fails, retry sequentially

For each subagent (parallel or single), pass the scoped files and relevant user notes. Require every subagent to produce:

- Findings grouped by severity (critical, high, medium, low).
- File references including path and line numbers.
- Specific remediation steps tied to the skill guidance that surfaced them.

**Subagent Invocation Pattern**:

- Read the subagent's SUBAGENT.md to load its process and output format.
- Verify subagent exists before invoking: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SUBAGENT.md`
- Pass the same scope and relevant notes to the subagent.
- Require the specified outputs with file:line evidence.
- **Subagent Output Validation** (after subagent completes):
  - **Validation Checklist**:
    - [ ] Output format matches expected template (check required sections present)
    - [ ] All required fields present (findings by severity, file:line references, remediation steps)
    - [ ] File references include path:line where applicable
    - [ ] Findings grouped by severity (critical, high, medium, low)
    - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
    - [ ] Output is actionable (remediation steps provided)
  - **Validation Failure**: If output invalid:
    - Report: "Subagent '{name}' output validation failed: {missing_field}/{invalid_format}"
    - Options: Retry subagent / Request manual correction / Continue with partial output
    - Wait for user decision (with 5-minute timeout per orchestrator error recovery)
- **If subagent fails**:
  - Use Error Recovery Protocol (see orchestrator)
  - Report: "Subagent '{name}' failed: {error}"
  - Options: Retry / Continue without {subagent} / Abort workflow
  - Wait for user decision (with 5-minute timeout per orchestrator error recovery)

**Subagent Empty Findings Handling**:

- If subagent returns no findings, this may be normal (clean code) or suspicious (subagent didn't analyze)
- Verify: Did subagent analyze the correct scope? Check subagent output for confirmation
- If suspicious: Ask user "Subagent '{name}' found no issues. Is this expected, or should I investigate?"

**Parallel Execution Safety Guarantees**:

- Each subagent operates in isolated context (Claude subagent model)
- All subagents are read-only (Read, Grep, Glob tools only)
- No state mutations (analyzing same code, not modifying)
- No output dependencies (each produces independent findings)
- Validation occurs after all complete (prevents error propagation)
- Conflict resolution handles disagreements (synthesis phase)

**Parallel Execution Fallback**:

- If any subagent fails during parallel execution:
  - Log failure and continue with successful subagents
  - Retry failed subagent sequentially
  - Merge partial results in synthesis

**Validation Gate** (before proceeding to Phase 4):

- [ ] Phase 3 complete (analysis subagents invoked, outputs received, code-reviewer invoked if code changes detected, integration-verifier invoked if integration changes detected)
- [ ] Output validated (subagent outputs formatted correctly, file:line citations present)
- [ ] Evidence verified (findings include citations, recommendations actionable)

**CRITICAL**: Do NOT proceed to Phase 4 until ALL validation items above are checked.

**Display Success Message** (after Phase 3 completion):

```
✅ Phase 3 Complete: Analysis

Completed:
- Subagents invoked: [X] subagents executed
- Findings identified: [Y] findings across all categories
- Code reviewer: ✅ Invoked (if code changes detected)
- Integration verifier: ✅ Invoked (if integration changes detected)

Next: Proceeding to Phase 4 - Synthesis
```

**Phase 3 Completion Checklist** (MANDATORY before proceeding to Phase 4):

**CRITICAL**: Do NOT proceed to Phase 4 until ALL items below are checked.

- [ ] Phase 3 success message displayed
- [ ] All required actions for Phase 3 completed
- [ ] All outputs validated (format, evidence, file:line citations)
- [ ] Actions Taken section updated with Phase 3 activities
- [ ] Gate check passed (if applicable)
- [ ] No errors or warnings requiring attention
- [ ] Phase 3 documented in Actions Taken with completion status

**Phase-Specific Checks**:

**Phase 3 (Dispatch Subagents)**:

- [ ] Subagents Inventory Check completed (see orchestrator)
- [ ] ALL required subagents invoked and documented
- [ ] Execution mode documented (parallel/sequential)
- [ ] Skip decisions documented (if any)
- [ ] Each subagent output validated

**If ANY item unchecked**:

- STOP workflow execution
- Complete missing items
- Re-run checklist
- Do NOT proceed until ALL items checked

**CRITICAL**: This checklist is non-negotiable. Workflow aborts if any item fails.

**Review Workflow Inventory Validation** (MANDATORY after Phase 3):

- [ ] 3 analysis subagents documented in Actions Taken (or focused subagent if focused review)
- [ ] Execution mode documented (parallel IF comprehensive, single IF focused)
- [ ] code-reviewer documented IF code changes detected
- [ ] integration-verifier documented IF integration changes detected
- [ ] All subagent outputs validated
- [ ] No analysis subagent missing (unless focused review)
- [ ] No code-reviewer missing IF code changes detected
- [ ] No integration-verifier missing IF integration changes detected

**If ANY item missing**: STOP and invoke missing subagent immediately.

## Phase 4 - Synthesis

**Conflict Resolution Protocol**:
If subagents report conflicting findings:

1. Document the conflict explicitly with both positions:
   ```
   Conflict Detected:
   - code-reviewer: [finding/position covering security, quality, performance, UX, accessibility]
   ```
2. Identify root cause:
   - Different assumptions
   - Different priorities (security vs performance)
   - Different interpretations of code
3. Present to user with options:
   - **Accept both**: Document as alternative approaches
   - **Choose priority**: User selects which concern takes precedence
   - **Resolve with context**: Provide additional context to resolve
4. Document resolution in final report

**Synthesis Steps**:

1. Merge the subagent outputs, deduplicating identical issues (same file:line, same issue type).
2. Apply Conflict Resolution Protocol for any conflicts.
3. Highlight blockers (critical/high) before suggestions (medium/low).
4. **File size sanity check**: If any reviewed file exceeds ~500 lines:
   - Flag immediately in synthesis (don't wait for final report)
   - Provide concrete split plan: "File {path} ({N} lines) exceeds 500-line guideline. Suggested split: [list components/files]"
   - Ask user: "Proceed with split recommendation or mark as tech debt?"

**Task Tool Usage** (findings tracking):

- Create tasks for critical findings:
  ```
  Task: Create tasks for critical findings
  - Fix: [Issue] at [file:line] (pending)
  - Fix: [Issue] at [file:line] (pending)
  ```
- Update task status as findings are addressed:
  ```
  Task: Update [Issue] fix status to completed
  ```

````

**Validation Gate** (before proceeding to Phase 5):

**CRITICAL**: Execute this bash command to verify all required deliverables exist:

```bash
# Verify review report structure
REQUIRED_SECTIONS=("Executive Summary" "Functionality Analysis" "Findings" "Verification Summary")
REPORT_FILE="review-report.md"  # Adjust based on actual output file

if [ -f "$REPORT_FILE" ]; then
    MISSING_SECTIONS=()
    for section in "${REQUIRED_SECTIONS[@]}"; do
        if ! grep -q "## $section" "$REPORT_FILE"; then
            MISSING_SECTIONS+=("$section")
        fi
    done

    if [ ${#MISSING_SECTIONS[@]} -gt 0 ]; then
        echo "Error: Missing sections in review report: ${MISSING_SECTIONS[*]}"
        exit 1
    else
        echo "✓ All required sections present in review report"
    fi
else
    echo "Error: Review report file not found: $REPORT_FILE"
    exit 1
fi

# Verify file:line citations exist
if ! grep -qE '[a-zA-Z0-9_/-]+\.(ts|tsx|js|jsx|py|java|go):[0-9]+' "$REPORT_FILE"; then
    echo "Warning: No file:line citations found in review report"
    exit 1
else
    echo "✓ File:line citations present"
fi
````

**CRITICAL**: Do NOT proceed to Phase 5 until bash command exits with code 0.

**Display Success Message** (after Phase 4 completion):

```
✅ Phase 4 Complete: Synthesis

Synthesized:
- Critical issues: [X] issues
- High priority issues: [Y] issues
- Medium priority issues: [Z] issues
- Low priority issues: [W] issues
- Conflicts resolved: [N] conflicts (if any)

Next: Proceeding to Phase 5 - Verification Summary
```

**Phase 4 Completion Checklist** (MANDATORY before proceeding to Phase 5):

**CRITICAL**: Do NOT proceed to Phase 5 until ALL items below are checked.

- [ ] Phase 4 success message displayed
- [ ] All required actions for Phase 4 completed
- [ ] All outputs validated (format, evidence, file:line citations)
- [ ] Actions Taken section updated with Phase 4 activities
- [ ] Gate check passed (if applicable)
- [ ] No errors or warnings requiring attention
- [ ] Phase 4 documented in Actions Taken with completion status

**Phase-Specific Checks**:

**Phase 4+ (Workflow-Specific)**:

- [ ] Workflow-specific phase requirements met
- [ ] All outputs validated
- [ ] Actions Taken updated

**If ANY item unchecked**:

- STOP workflow execution
- Complete missing items
- Re-run checklist
- Do NOT proceed until ALL items checked

**CRITICAL**: This checklist is non-negotiable. Workflow aborts if any item fails.

**Validation Gate** (before proceeding to Phase 5):

- [ ] Phase 4 complete (findings synthesized, conflicts resolved, priorities assigned)
- [ ] Output validated (findings deduplicated, blockers highlighted, file size checks done)
- [ ] Evidence verified (all findings include file:line citations, recommendations actionable)

**CRITICAL**: Do NOT proceed to Phase 5 until ALL validation items above are checked.

## Phase 5 - Verification Summary

**MANDATORY**: Compose verification block using exact template:

```
## Verification Summary
Scope: <files reviewed>
Criteria: <list of what was verified - security, performance, quality, UX, accessibility>
Commands:
- <command> -> exit <code> (if any static analysis was run)
- <command> -> exit <code>
Evidence:
- <cited file:line references>
- <tool output snippets if any>
Outstanding Questions: <if clarification is needed>
```

**Evidence Quality Examples**:

- **Good evidence**: "HIGH - SQL injection via string concatenation - src/db/user.ts:42 - Evidence: user input concatenated into query without parameterization. Mitigation: use prepared statements (see code-review-patterns 'SQL Injection')."
- **Weak evidence**: "maybe insecure DB calls somewhere in user code" (reject - must cite specific file:line)

**Required**: Every finding must include file:line citation. If unable to cite, state "Insufficient evidence - requires manual review" instead of guessing.

**Validation Gate** (before proceeding to Phase 6):

- [ ] Phase 5 complete (verification summary generated, evidence documented)
- [ ] Output validated (verification summary includes commands, exit codes, evidence)
- [ ] Evidence verified (all claims supported by evidence, file:line citations present)

**CRITICAL**: Do NOT proceed to Phase 6 until ALL validation items above are checked.

**Display Success Message** (after Phase 5 completion):

```
✅ Phase 5 Complete: Verification Summary

Generated:
- Review report: ✅ Created with [X] findings
- Recommendations: [Y] recommendations provided
- Evidence: ✅ All claims supported by evidence

Next: Review workflow complete - Report ready
```

**Phase 5 Completion Checklist** (MANDATORY before proceeding to Phase 6):

**CRITICAL**: Do NOT proceed to Phase 6 until ALL items below are checked.

- [ ] Phase 5 success message displayed
- [ ] All required actions for Phase 5 completed
- [ ] All outputs validated (format, evidence, file:line citations)
- [ ] Actions Taken section updated with Phase 5 activities
- [ ] Gate check passed (if applicable)
- [ ] No errors or warnings requiring attention
- [ ] Phase 5 documented in Actions Taken with completion status

**Phase-Specific Checks**:

**Phase 5 (Verification Summary)**:

- [ ] Verification summary generated
- [ ] Evidence documented
- [ ] All claims supported by evidence

**If ANY item unchecked**:

- STOP workflow execution
- Complete missing items
- Re-run checklist
- Do NOT proceed until ALL items checked

**CRITICAL**: This checklist is non-negotiable. Workflow aborts if any item fails.

## Phase 5.5 - Context Preservation (MANDATORY)

**CRITICAL**: Create session summary before final deliverable to preserve context across compaction. This phase is MANDATORY and cannot be skipped.

**When to Create Session Summary**:

- Before Phase 6 (final deliverable) - MANDATORY
- Approaching token limits (75%+ usage)
- After major workflow phase completion (Phase 4 or Phase 5)
- End of session or workflow completion

**Process**:

1. **Load Session Summary Skill**:
   - Use Skill tool to load `session-summary` skill
   - Skill path: `plugins/cc10x/skills/session-summary/SKILL.md`

2. **Execute Session Summary**:
   - Follow skill instructions to create comprehensive summary
   - Archive previous session if exists (saves to `.claude/memory/session_summaries/session-{timestamp}.md`)
   - Prune old archives (keep only 10 most recent session summaries)
   - Analyze conversation transcript
   - Extract tool calls, file changes, accomplishments, decisions
   - Document next steps explicitly

3. **Save Session Summary**:
   - Save summary to `.claude/memory/session_summaries/session-{timestamp}.md` (archived)
   - Update `.claude/memory/CURRENT_SESSION.md` with latest summary
   - Ensure directory exists: `mkdir -p .claude/memory/session_summaries`
   - Verify old archives cleaned (only 10 most recent remain)

4. **Document in Actions Taken**:
   - Add entry: "Session summary created before Phase 6 (Context Preservation)"
   - Include summary path if available

**Bash Helper**:

```bash
# Create session summary directory if needed
mkdir -p .claude/memory/session_summaries

# Session summary will be created by Claude using session-summary skill
# Summary saved to: .claude/memory/CURRENT_SESSION.md
# Archived to: .claude/memory/session_summaries/session-{timestamp}.md
```

**Integration Note**:

- Session summary complements snapshot created by pre-compact hook
- Summary provides Claude-generated context analysis
- Snapshot provides programmatic context extraction
- Both are loaded by post-compact hook for comprehensive recovery

**Display Success Message** (after Phase 5.5 completion):

```
✅ Phase 5.5 Complete: Context Preservation

Completed:
- Session summary created and saved
- Previous session archived (if existed)
- Old archives pruned (kept 10 most recent)
- Summary file: .claude/memory/CURRENT_SESSION.md

Next: Proceeding to Phase 6 - Present Results
```

**Phase 5.5 Completion Checklist** (MANDATORY before proceeding to Phase 6):

**CRITICAL**: Do NOT proceed to Phase 6 until ALL items below are checked.

- [ ] Phase 5.5 success message displayed
- [ ] Session summary skill loaded successfully
- [ ] Session summary created and saved to `.claude/memory/CURRENT_SESSION.md`
- [ ] Previous session archived (if existed) to `.claude/memory/session_summaries/session-{timestamp}.md`
- [ ] Old archives pruned (only 10 most recent session summaries remain)
- [ ] Actions Taken section updated with Phase 5.5 activities
- [ ] Phase 5.5 documented in Actions Taken with completion status
- [ ] Session summary file exists and is non-empty

**Phase-Specific Checks**:

- [ ] Session summary contains all required sections (overview, files modified, tool calls, accomplishments, decisions, next steps)
- [ ] Summary file path verified: `.claude/memory/CURRENT_SESSION.md`
- [ ] Archive directory exists: `.claude/memory/session_summaries/`
- [ ] Archive cleanup verified (count session files, ensure ≤10 most recent)

**If ANY item unchecked**:

- STOP workflow execution
- Complete missing items
- Re-run checklist
- Do NOT proceed until ALL items checked

**CRITICAL**: This checklist is non-negotiable. Workflow aborts if any item fails.

**Validation Gate** (before proceeding to Phase 6):

- [ ] Phase 5.5 complete (session summary created, archived, saved)
- [ ] Session summary file exists: `.claude/memory/CURRENT_SESSION.md`
- [ ] Summary contains required sections (verify file is non-empty and well-formed)
- [ ] Actions Taken updated with Phase 5.5 completion

**CRITICAL**: Do NOT proceed to Phase 6 until ALL validation items above are checked.

## Phase 6 - Present Results

**CRITICAL**: Phase 5.5 (Context Preservation) MUST be completed before this phase.

**CRITICAL**: Save review report to disk before presenting (ensures persistence across compaction).

**Review Report Persistence** (MANDATORY):

1. **Save Review Report File**:
   - Extract feature/scope name from Phase 0 functionality analysis or user request
   - Use kebab-case for filename (e.g., `review-auth-code-20250129-143022.md`)
   - Save review report to `.claude/docs/reviews/review-{timestamp}.md`
   - Ensure `.claude/docs/reviews/` directory exists (create if needed)
   - Format: Use exact template from "MANDATORY OUTPUT FORMAT" section below
   - Include complete review report with all sections (Executive Summary, Actions Taken, Functionality Analysis, Findings, Verification Summary, Recommendations, Open Questions)

2. **Create Review Reference File** (MANDATORY):
   - Create `.claude/memory/current_review.txt` containing the review report path: `.claude/docs/reviews/review-{timestamp}.md`
   - This allows other workflows and hooks to find the active review
   - Example: `echo ".claude/docs/reviews/review-auth-code-20250129-143022.md" > .claude/memory/current_review.txt`

3. **Update Checkpoint with Output Path**:
   - Update most recent checkpoint (`.claude/memory/workflow_state/review_{timestamp}.json`) to include:
     ```json
     {
       "output_file": ".claude/docs/reviews/review-{timestamp}.md",
       "output_saved": true
     }
     ```

4. **Bash Command to Save Report**:

   ```bash
   # Create reviews directory if needed
   mkdir -p .claude/docs/reviews

   # Generate timestamp
   TIMESTAMP=$(date +%Y%m%d-%H%M%S)

   # Extract scope name from functionality analysis or use default
   SCOPE_NAME="review"  # Replace with actual scope from Phase 0

   # Save review report
   REVIEW_FILE=".claude/docs/reviews/review-${SCOPE_NAME}-${TIMESTAMP}.md"
   # Write complete review report to $REVIEW_FILE

   # Create reference file
   echo "$REVIEW_FILE" > .claude/memory/current_review.txt

   # Update checkpoint with output path
   # (Checkpoint update logic handled by workflow)
   ```

**Before Presenting** (optimized memory):

- **Store Common Issues** (only high-value):
  - Save issue patterns ONLY if appear frequently (>3 occurrences across files)
  - Format: `{issue_type, occurrence_count, common_location, fix_pattern}`
  - Update existing patterns: increment occurrence_count if pattern exists
- **Store Review Patterns** (only validated):
  - Save successful review approaches ONLY if validated effective
  - Track success rate: did approach find real issues?
- **Run Cleanup**: Execute memory cleanup script

## Quick Reference

**Phase Summary**:

- **Phase 0**: Functionality Analysis (MANDATORY FIRST) - Understand user/admin/system flows, verify functionality works
- **Phase 1**: Input Validation - Verify files exist, scope clear, questions answered
- **Phase 2**: Load Required Skills - Load project-context-understanding, security, quality, performance, UX, accessibility, verification skills in parallel
- **Phase 3**: Dispatch Analysis Subagents - Invoke analysis subagents based on scope (focused vs comprehensive), then code-reviewer and integration-verifier if changes detected
- **Phase 4**: Synthesis - Combine findings with file:line citations and evidence
- **Phase 5**: Verification Summary - Generate summary with functionality verification FIRST, then other checks
- **Phase 6**: Present Results - Format findings by severity with actionable recommendations

**Key Outputs**:

- Functionality analysis (user/admin/system flows)
- Security findings with file:line citations
- Performance findings with file:line citations
- Code quality findings with file:line citations
- UX findings with file:line citations
- Accessibility findings with file:line citations
- Verification summary with evidence

**Validation Requirements**:

- [ ] Phase 0 complete (functionality analysis done, gate checks passed)
- [ ] All required skills loaded successfully (including project-context-understanding and verification-before-completion)
- [ ] Subagents invoked correctly (existence verified, skip conditions checked, code-reviewer and integration-verifier invoked if changes detected)
- [ ] All findings include file:line citations
- [ ] Evidence provided for all claims (commands run, exit codes, logs)

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Review Report

## Executive Summary

[2-3 sentences summarizing total issues by severity, go/no-go recommendation, and overall code health status]

## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented]
- Skills loaded: project-context-understanding, risk-analysis, code-review-patterns, frontend-patterns, verification-before-completion
- Subagents invoked: code-reviewer[, integration-verifier if integration changes detected]
- Files reviewed: [list]
- Tools used: [Read, Grep, Glob, Bash if any]

## Functionality Analysis

[Include complete functionality analysis from Phase 0]

## Findings / Decisions

### Security Findings

- **CRITICAL**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **HIGH**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **MEDIUM**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **LOW**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]

### Performance Findings

[Same format as Security]

### Code Quality Findings

[Same format as Security]

### UX Findings

[Same format as Security]

### Accessibility Findings

[Same format as Security]

## Verification Summary

[Use exact template from Phase 4]

## Recommendations / Next Steps

[Prioritized list - CRITICAL first, then HIGH, then others]

## Open Questions / Assumptions

[If any conflicts were detected or clarification needed]
```

**Validation Before Presenting**:

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] All findings include file:line citations
- [ ] Verification Summary includes commands (if any) with exit codes
- [ ] Recommendations prioritized (CRITICAL → HIGH → MEDIUM → LOW)
- [ ] All subagents/skills documented in Actions Taken (including code-reviewer and integration-verifier if invoked)
- [ ] Conflicts documented if any
- [ ] **Review report saved to `.claude/docs/reviews/review-{timestamp}.md`** (MANDATORY)
- [ ] **Reference file created: `.claude/memory/current_review.txt`** (MANDATORY)
- [ ] **Checkpoint updated with output file path** (MANDATORY)

## Failure Handling

**Standardized Error Recovery Protocol** (use orchestrator's template):

If any skill or subagent fails:

1. **Context**: What was attempted (skill/subagent name, file path, command if any)
2. **Problem**: What failed (error message, exit code, file not found, etc.)
3. **Options**:
   - **Retry**: Attempt again (if transient error likely)
   - **Continue without {component}**: Proceed with reduced functionality
   - **Abort workflow**: Stop and restart
4. **Impact**: Explain what each choice means
5. **Default**: Recommended action

**Critical Rules**:

- Never fabricate findings for missing data; report the failure explicitly
- Never proceed without user decision when failure occurs
- Document all failures in Actions Taken section

## References

- Skill usage rules: `docs/reference/04-SKILLS.md`
- Subagent contract: `docs/reference/03-SUBAGENTS.md`
