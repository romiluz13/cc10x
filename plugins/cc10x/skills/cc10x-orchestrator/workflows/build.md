# BUILD Workflow - TDD Driven Implementation

**CRITICAL**: This workflow MUST be activated through cc10x-orchestrator. Do NOT execute this workflow directly. The orchestrator provides required context, coordinates skill loading, and manages subagent invocation. Direct execution bypasses all validation mechanisms.

**See SHARED-ENFORCEMENT.md for MANDATORY execution mode, enforcement rules, guardrails, and validation gates that apply to ALL workflows.**

**Triggered by:** User requests implementation or feature build work.

## WHEN/HOW/WHY - BUILD Workflow

### WHEN to Use This Workflow

**Keywords that trigger BUILD workflow:**

- build, building, builder, build a, build the
- implement, implementation, implementing
- create, creating, create a, create the
- write code, write a, write the, coding, code
- develop, development, developing, developer
- make, making, make a, make the
- add feature, implement feature, build feature

**Example user requests:**

- "build a user profile component"
- "implement authentication"
- "create a file upload feature"
- "write code for user registration"

### HOW Orchestrator Selects This Workflow

**Detection Process:**

1. User says keyword like "build" → Orchestrator skill loads automatically (via description keywords)
2. Orchestrator scans user request for workflow keywords
3. If "build", "implement", "create", "write code", "develop", or "make" detected → BUILD workflow selected
4. Orchestrator activates this workflow file
5. Workflow executes phases: Functionality Analysis → Complexity Gate → Component Queue → TDD Build → Review → Integration → Delivery

**Decision Tree:**

```
User request contains "build"/"implement"/"create"/"write code"/"develop"/"make"?
├─ YES → BUILD workflow
└─ NO → Check other workflow keywords
```

### WHY Use BUILD Workflow vs Others

**Use BUILD workflow when:**

- You need to write new code/components
- You need to implement features
- You need to create new functionality
- You need TDD-driven implementation (RED → GREEN → REFACTOR)

**BUILD vs PLAN:**

- BUILD: Write code to implement features (execution)
- PLAN: Design architecture before building (design)

**BUILD vs REVIEW:**

- BUILD: Create new code (creation)
- REVIEW: Analyze existing code (analysis)

**BUILD vs DEBUG:**

- BUILD: Write new code (forward)
- DEBUG: Fix broken code (backward)

**BUILD vs VALIDATE:**

- BUILD: Create implementation (creation)
- VALIDATE: Verify implementation matches plan (verification)

**See SHARED-ENFORCEMENT.md for TL;DR Quick Checklist, Guardrails, and Runtime Compliance Checks.**

**See orchestrator REFERENCE.md for tool usage guides and search guidance.**

## Phase 0 - Functionality Analysis (MANDATORY)

**CRITICAL**: This phase MUST be completed before any complexity gate, skill loading, or subagent dispatching. Understanding functionality requirements is the foundation for all build activities.

**Purpose**: Understand what functionality needs to be built (user flows, admin flows, system flows) and what acceptance criteria must be met before implementing components.

**Task Tool Usage** (phase tracking):

- Create tasks for all workflow phases at start:
  ```
  Task: Create tasks for workflow phases
  - Phase 0: Functionality Analysis (in_progress)
  - Phase 1: Complexity Gate (pending)
  - Phase 2: Shared Context (pending)
  - Phase 3: Component Queue (pending)
  - Phase 4: Component Execution Loop (pending)
  - Phase 5: Aggregate Verification (pending)
  - Phase 6: Delivery (pending)
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

2. **Analyze Requirements**:
   - Read user request and any provided requirements/plan
   - Understand the intended functionality
   - Document user flows, admin flows (if applicable), and system flows
   - Identify integration flows if external systems are involved
   - Extract acceptance criteria for each flow
3. **Research Planning** (if applicable):
   - Identify external APIs that need documentation
   - Identify integration constraints or limitations
   - Plan external resource checks (will be executed in Phase 1)
4. **Output**: Complete functionality analysis using template format:

   ```markdown
   ## Functionality Analysis

   ### What Functionality Needs to be Built?

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
   - [ ] Data format requirements
   - [ ] Authentication requirements
   - [ ] Rate limits/quotas
   - [ ] Error handling patterns

   ### Acceptance Criteria

   - [ ] User flow works (testable criteria)
   - [ ] Admin flow works (if applicable, testable criteria)
   - [ ] System flow works (testable criteria)
   - [ ] Integration flow works (if applicable, testable criteria)
   - [ ] Error handling works (testable criteria)
   ```

**Gate Check**: Before proceeding to Phase 1, ALL items below MUST be checked:

- [ ] Functionality analysis complete (user flow, admin flow if applicable, system flow, integration flow if applicable documented)
- [ ] Acceptance criteria defined (testable, measurable, extracted from flows)
- [ ] Research needs identified (external APIs, constraints, documentation) if applicable
- [ ] External dependencies identified (libraries, services, APIs) if applicable
- [ ] Template format followed (all required sections completed)
- [ ] Functionality clear and understood (no ambiguous requirements)

**CRITICAL**: Do NOT proceed to Phase 1 until ALL items above are checked. If any item is incomplete:

- Ask user: "Functionality unclear. Please clarify: What functionality needs to be built? What are the user flows? What are the acceptance criteria?"
- Do NOT proceed until functionality is understood and all gate check items are complete

**Display Success Message** (after Phase 0 completion):

```
✅ Phase 0 Complete: Functionality Analysis

Analyzed:
- Components to build: [X] components identified
- Acceptance criteria: [Y] criteria defined
- User flows: [Z] flows documented
- Visual assets: [N] assets found (if any)

Next: Proceeding to Phase 1 - Complexity Gate
```

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
- What are the specific user flows for this feature?
- What are the acceptance criteria?
- What are the technical constraints?
- What are the business constraints?
```

**Memory Integration** (optimized):

- **Store Functionality Patterns**: After workflow completes, save successful functionality analysis patterns to `.claude/memory/patterns.json` (only if validated effective)
- **Query Similar Functionality**: Check `.claude/memory/patterns.json` for similar functionality patterns (use semantic match, top 3 only)

## Phase 1 - Complexity Gate

**Memory Integration** (optimized):

- **Load Once**: Read `.claude/memory/patterns.json` ONCE, cache for workflow duration
- **Semantic Match**: Use `jq` to filter by build signature (similar to planning pattern)
- **Top 3 Only**: Return top 3 highest-confidence patterns
- **Component Orders**: Check `.claude/memory/patterns.json` for component_orders matching task type
- **Validate Dependencies**: If component order found, verify dependency_hash matches current deps

- Estimate scope. If complexity <=2, present the lightweight warning and wait for explicit approval before continuing.
- Confirm repositories, directories, and acceptance criteria.

**External Resource Check** (smart Q&A caching):

- **Check Cache First**: Lookup {url, prompt} combinations in `.claude/memory/web_cache/cache_index.json`
- **Cache Logic**:
  - Create hash from `{url}_{prompt}` for each planned question
  - If cached and TTL valid → use cached answer (skip fetch)
  - If cached but expired → re-fetch with same prompt
  - If not cached → WebFetch with prompt and cache answer (library docs: 48h TTL)
- **Deduplication**: Track {url, prompt} combinations fetched in this workflow
- Check if build requires external documentation:
  - Libraries/frameworks mentioned? → Plan questions:
    - "How do I install and initialize this library?"
    - "What are the most common usage patterns and code examples?"
    - "How do I handle errors and edge cases?"
  - SDKs mentioned? → Plan questions about setup, initialization, API calls
  - External APIs? → Plan questions about authentication, request format, error handling
- Ask user: "Detected external dependencies: {list}. Will ask {N} targeted questions. Found {M} in cache. Proceed? (yes/no)"

**Workflow State Persistence** (Checkpoint System):

- **Checkpoint After Each Phase**: Save workflow state to `.claude/memory/workflow_state/build_{timestamp}.json`
- **Checkpoint Format**:
  ```json
  {
    "workflow": "build",
    "phase": "Phase_2_Component_Queue",
    "timestamp": "2025-10-29T10:00:00Z",
    "state": {
      "components": [{name, status, dependencies}],
      "component_queue": [...],
      "completed_components": [...],
      "blocked_components": [...],
      "current_component": "ComponentName"
    },
    "next_phase": "Phase_3_Component_Execution_Loop"
  }
  ```
- **Resume Logic**: If resuming after interruption:
  1. Read most recent checkpoint: `jq -s 'sort_by(.timestamp) | reverse | .[0]' .claude/memory/workflow_state/build_*.json`
  2. Validate checkpoint state (components present, queue valid)
  3. Continue from `next_phase` with checkpoint state restored
  4. Ask user: "Resuming from Phase {N}, Component {name}. Continue from checkpoint or restart?"
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2, Phase 3, Phase 4 (after each component), Phase 5 completion

**If resuming after compaction or context is unclear**, use checkpoint system:

- Read most recent checkpoint from `.claude/memory/workflow_state/build_*.json`
- If checkpoint exists: Restore state and continue from `next_phase`
- If no checkpoint: Read `.claude/memory/snapshots/` most recent `snapshot-*.md` and `.claude/memory/WORKING_PLAN.md` as fallback

**Display Success Message** (after Phase 1 completion):

```
✅ Phase 1 Complete: Complexity Gate

Assessed:
- Complexity score: [1-5]
- Status: ✅ Proceeding / ⚠️ Low complexity warning shown
- External dependencies: [N] dependencies detected (if any)

Next: Proceeding to Phase 2 - Shared Context
```

## Phase 2 - Shared Context

**Required Skills**:

- `project-context-understanding` - **MANDATORY** (understand project patterns, conventions, and structure before building)
- `requirements-analysis`
- `security-patterns`
- `code-quality-patterns` - **MANDATORY** (build quality code with SOLID principles, maintainability)
- `code-generation` - **MANDATORY** (code generation patterns and best practices)
- `component-design-patterns` - **MANDATORY** (component design patterns and best practices)
- `test-driven-development`
- `verification-before-completion`
- `memory-tool-integration` (filesystem-based memory always available)
- `web-fetch-integration` (if external docs needed)

**Conditional Skills**:

- `ui-design` - **MANDATORY** when UI components detected (file patterns: _.tsx, _.jsx, \*.vue, components/, ui/)
- `design-patterns` - Load if building APIs, components, or integrations
- `performance-patterns` - Load if performance-critical code detected (keywords: performance, optimization, fast, efficient, bottleneck)

**Detection Logic**:

- UI Components: File patterns `*.tsx`, `*.jsx`, `*.vue`, `components/`, `ui/`, component names (Form, Button, Modal, etc.), or user requests UI components
- Design Patterns: Building APIs, components, or integrations mentioned in requirements
- Performance-Critical Code: Keywords "performance", "optimization", "fast", "efficient", "bottleneck"

**Skill Loading Strategy**:

- All required skills are independent (no dependencies between them)
- **Load all required skills in parallel** for faster initialization
- **Load conditional skills** (`ui-design`, `design-patterns`, `performance-patterns`, `web-fetch-integration`) based on detection logic, still in parallel with required skills

**Memory Integration** (optimized):

- **Load Preferences**: Query `.claude/memory/preferences.json` for build preferences (if exists)
- **Retrieve Build Patterns**: Check `.claude/memory/patterns.json` for component_orders matching task type
- **Validate Dependencies**: If component order found, verify dependency_hash matches current project deps
- **Load Failure Modes**: Check `.claude/memory/failure_modes.json` for common build failures (only high success_rate > 60%)

**External Documentation** (smart caching):

- If external libraries/frameworks needed:
  - **Check Cache First**: Lookup library doc URLs in `.claude/memory/web_cache/cache_index.json`
  - **Use Cache if Valid**: If cached and TTL valid → use cache (skip fetch)
  - **Fetch if Needed**: If not cached or expired → fetch and cache with 14-day TTL
  - Load SDK examples (same cache-first approach)
  - Include in build context

**Skill Loading Verification Protocol**:
For each skill above:

1. Read first 100 chars of `plugins/cc10x/skills/{skill-name}/SKILL.md` to verify file exists
2. Parse YAML frontmatter to verify valid format
3. Check body content exists (not empty)
4. If any verification fails:
   - Report immediately: "Skill '{name}' failed to load: {error details}"
   - Present options: Continue without {skill} / Abort workflow / Retry loading
   - Wait for user decision before proceeding
5. Document successfully loaded skills in Actions Taken section

**Requirements Summary**:
After loading skills, summarise:

- Requirements: [list from requirements-analysis]
- Constraints: [technical, business, timeline]
- Acceptance Tests: [measurable criteria]
- Dependencies: [external services, libraries, other components]

**MANDATORY: Reusable Code Search**

**CRITICAL**: Do NOT proceed to component building until reusable code search is complete.

**Process**:

1. **Search for Similar Features**:
   - Extract key functionality patterns from Phase 0 analysis
   - Use Grep to find similar functionality: `Grep("pattern-keyword", path="src/")`
   - Use Glob to find similar components: `Glob("src/components/**/*{similar}*.{tsx,jsx}")`
   - Use Glob to find similar APIs: `Glob("src/api/**/*{similar}*.ts")`
   - Document all patterns found with file paths

2. **Analyze Existing Patterns**:
   - Read similar components/APIs using Read tool
   - Note patterns to follow (naming conventions, structure, error handling)
   - Identify reusable code (utilities, hooks, services)
   - Document architectural patterns used

3. **Document Findings**:
   - List reusable components with file paths: `file:line-range`
   - List reusable APIs/services with file paths
   - List reusable utilities/hooks with file paths
   - Note patterns to follow in component building
   - Reference existing code in component design

**Output Format**:

```markdown
## Reusable Code Analysis

### Similar Components Found

- `src/components/Button.tsx:1-50` - Button component pattern
- `src/components/Modal.tsx:1-80` - Modal component pattern

### Similar APIs Found

- `src/api/auth.ts:10-30` - Authentication API pattern

### Reusable Utilities

- `src/utils/validation.ts:1-20` - Validation utilities

### Patterns to Follow

- Component structure: [pattern description]
- API structure: [pattern description]
- Error handling: [pattern description]
```

**CRITICAL**: Use findings to build components following existing patterns. Do NOT create new patterns if existing ones can be reused.

**Display Success Message** (after Phase 2 completion):

```
✅ Phase 2 Complete: Shared Context

Established:
- Reusable patterns: [X] patterns found
- Test patterns: [Y] patterns identified
- Skills loaded: [Z] skills loaded
- Context ready: ✅ Yes

Next: Proceeding to Phase 3 - Component Queue
```

**CRITICAL VALIDATION GATE - Before Phase 3**:

**Checklist** (ALL must pass before proceeding):

- [ ] Phase 2: Skills loaded complete
- [ ] Actions Taken section updated with ALL required skills listed
- [ ] Skills Inventory Check passed (ALL required skills loaded, conditional skills loaded IF detected)
- [ ] Each skill marked as "loaded successfully" or "failed to load" in Actions Taken

**If validation fails**: STOP workflow, load missing skills, update Actions Taken, re-run Skills Inventory Check, then proceed.

## Phase 3 - Component Queue

**Component Identification**:

1. Break the request into discrete components or tasks.
2. For each component, prepare a concise brief:
   ```
   Component: {name}
   Goal: {what it does}
   Inputs: {what it receives}
   Outputs: {what it produces}
   Dependencies: {other components/services}
   Acceptance Criteria: {how to verify}
   ```

**Task Tool Usage** (component tracking):

- Create tasks for each component to build:
  ```
  Task: Create component build tasks
  - Component: [ComponentName] (pending)
  - Component: [ComponentName] (pending)
  ```
- Update task status as components build:
  ```
  Task: Update [ComponentName] status to completed
  Task: Update [ComponentName] status to in_progress
  ```

**Dependency-Aware Ordering**:
BEFORE creating component queue:

1. Identify dependencies between components (which components depend on which)
2. Build dependency graph
3. Order queue by dependency graph (no component before its dependencies)
4. If circular dependencies detected:
   - Flag immediately: "Circular dependency detected: {component A} → {component B} → {component A}"
   - Ask user: "Resolve circular dependency before proceeding or mark as risk?"
5. If no dependencies, proceed with user-specified order or logical grouping
6. **Mark dependencies**: Store dependency graph: `{component: [dependencies]}` for failure cascading

**Ask Questions Tool Usage** (for UI components):

- If UI components detected and UI requirements unclear, use the askquestion tool:
  - What styling framework should be used?
  - What are the layout requirements?
  - What are the design system constraints?
  - What are the accessibility requirements?
- Proceed with UI component build using answers

**Component Execution Strategy**:

1. **Build Dependency Graph** (already exists above):
   - Map: `{component: [dependencies]}`
   - Identify independent components (no dependencies on each other)
2. **Execution Mode Selection**:

   **PARALLEL (Safe for Independent Components)**:
   - ✅ Different components (no shared code)
   - ✅ Isolated subagent contexts (separate execution)
   - ✅ No dependencies (component A doesn't need component B)
   - ✅ Validation per component (prevents cascade)

   **SEQUENTIAL (Required for Dependent Components)**:
   - ❌ Component depends on another component
   - ❌ Shared code or interfaces
   - ❌ Integration dependencies

3. **Component Execution Plan**:

   ```
   Dependency Graph Analysis:
   - Component A: no deps → Can start immediately
   - Component B: no deps → Can start immediately (parallel with A)
   - Component C: depends on A → Must wait for A
   - Component D: depends on B → Must wait for B

   Execution Order:
   Phase 1 (Parallel): A + B (independent, execute simultaneously)
   Phase 2 (Sequential): C (after A completes), D (after B completes)
   ```

**Component Failure Cascading Logic**:

- **Failure Detection**: If component fails (component-builder fails, blocking review feedback, integration failure):
  1. Mark component status: `{component_name}: FAILED` with reason
  2. **Check Dependency Graph**: Identify all components that depend on failed component
  3. **Mark Dependencies**: For each dependent component:
     - Change status: `{dependent_component}: BLOCKED (depends on {failed_component})`
     - Add to blocked queue: `blocked_components: [{name, reason, depends_on}]`
  4. **User Decision**: Present:

     ```
     Component Failure Cascade Detected:
     - Component 1: FAILED ({reason})
     - Component 2: BLOCKED (depends on Component 1)
     - Component 3: BLOCKED (depends on Component 1)

     Options:
     1. Fix Component 1 first → Then continue with Component 2, 3
     2. Skip Component 1 → Build Component 2, 3 separately (if possible)
     3. Abort workflow → Restart after fixing Component 1
     ```

  5. **Wait for User Decision**: Don't proceed until user chooses path
  6. **Documentation**: Log failure cascade in Actions Taken: "Component 1 failed → Component 2, 3 blocked"

**Execution Policy**:

- Independent components (no dependencies) → Execute in parallel
- Dependent components → Execute sequentially after dependencies complete
- If user requests explicit sequential execution, honor user preference
- Document component execution order (parallel groups, sequential dependencies) in Actions Taken section
- **Skip blocked components** until dependencies resolved

## Phase 4 - Component Execution Loop

**Per-Component Subagent Sequence** (ALWAYS SEQUENTIAL):

- component-builder → code-reviewer → integration-verifier
- Must remain sequential (reviewer needs builder output, verifier needs reviewer approval)
- Parallelization applies BETWEEN components, not WITHIN component

**CRITICAL**: After EACH subagent invocation, you MUST:

1. Update Actions Taken IMMEDIATELY (mark subagent as "invoked successfully" or "skipped" with reason)
2. Document execution mode (sequential/parallel)
3. Document subagent outputs (files created, tests run, exit codes)

**CRITICAL**: Before proceeding to Phase 5, you MUST:

1. Perform Subagents Inventory Check (verify ALL required subagents invoked)
2. Verify Actions Taken updated with ALL subagents documented
3. For BUILD workflow: Verify TDD cycle evidence present (RED → GREEN → REFACTOR with exit codes)

**If validation fails**: STOP workflow, invoke missing subagents, update Actions Taken, re-run Subagents Inventory Check, then proceed.

For every component:

**When to Invoke Subagents**:

- **INVOKE** - Component building needed: Always invoke `component-builder` (required for TDD)
- **INVOKE** - Code changes made: After component-builder completes, invoke `code-reviewer` (always)
- **INVOKE** - Integration checks needed: After review passes, invoke `integration-verifier` (always unless user skips)

**When NOT to Invoke Subagents**:

- **SKIP** - Component already built: If component exists and user says "skip build, just review" → Skip `component-builder`, only invoke `code-reviewer`
- **SKIP** - User explicitly skips review: If user says "skip review" or "quick build" → Skip `code-reviewer`, proceed to integration
- **SKIP** - User explicitly skips integration: If user says "skip integration checks" → Skip `integration-verifier`, proceed to next component
- **SKIP** - Component is dependency-only: If component is pure dependency (e.g., package.json update, config file) → Skip `code-reviewer` (no security/code quality concerns), only invoke `integration-verifier` if integration depends on it
- **SKIP** - Trivial changes: If change is single line/comment → Skip `code-reviewer` and `integration-verifier`, just invoke `component-builder` for verification

**Conflict Prevention**:

- **Never invoke multiple builders simultaneously**: Each component gets its own `component-builder` invocation
- **Sequential review**: Review happens AFTER build completes, not in parallel
- **Sequential integration**: Integration check happens AFTER review, not in parallel
- **One bug at a time**: If debugging needed, finish bug-investigator before invoking code-reviewer

**Display Success Message** (after Phase 3 completion):

```
✅ Phase 3 Complete: Component Queue

Queued:
- Components: [X] components queued
- Dependencies: ✅ Mapped
- Execution order: ✅ Determined

Next: Proceeding to Phase 4 - Component Execution Loop
```

**CRITICAL VALIDATION GATE - Before Phase 4**:

**Checklist** (ALL must pass before proceeding):

- [ ] Phase 3: Component queue complete
- [ ] Actions Taken section updated with component queue documented
- [ ] Dependencies mapped and execution order determined
- [ ] Component briefs prepared for all components

**If validation fails**: STOP workflow, complete missing items, update Actions Taken, then proceed.

## Phase 4 - Component Execution Loop

**Default Sequence** (unless user skips):

1. Invoke `component-builder` with the brief. Require:
   - Failing test first (RED) with command output captured.
   - Minimal implementation (GREEN).
   - Refactor while keeping tests green.
   - Verification log referencing commands executed.
2. Invoke `code-reviewer` on the resulting changes (unless user skipped). Expect:
   - Findings with file/line references.
   - Security/performance considerations tied to the relevant skills.
   - Recommendations or approval status.
3. Invoke `integration-verifier` to confirm broader system behaviour (unless user skipped). Expect:
   - Integration or end-to-end checks.
   - Additional tests or scripts run, plus their outputs.
4. Consolidate notes. Address blocking review feedback before moving to the next component.
5. File size sanity check: Before moving on, scan changed files; if any exceeds ~500 lines, propose a concrete refactor/split plan.

**Subagent Invocation Pattern** (for each subagent):

- Verify subagent exists: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SUBAGENT.md`
- Read the subagent's SUBAGENT.md to load its process and output format.
- Pass the component brief and relevant context.
- Require the specified outputs with file:line evidence and commands/exit codes where relevant.
- **Subagent Output Validation** (after subagent completes):
  - **Validation Checklist**:
    - [ ] Output format matches expected template (check required sections present)
    - [ ] All required fields present (TDD cycle evidence, review findings, integration results)
    - [ ] File references include path:line where applicable
    - [ ] Commands included with exit codes
    - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
    - [ ] Output is actionable (not just descriptions)
  - **Validation Failure**: If output invalid:
    - Report: "Subagent '{name}' output validation failed: {missing_field}/{invalid_format}"
    - Options: Retry subagent / Request manual correction / Continue with partial output
    - Wait for user decision (with 5-minute timeout per orchestrator error recovery)
- **On failure**: Use Error Recovery Protocol
  - Options: Retry / Continue without {subagent} / Abort workflow
  - Wait for user decision (with 5-minute timeout per orchestrator error recovery)

**Review Feedback Classification**:
When code-reviewer provides feedback, classify:

- **Blocking**: Security vulnerabilities, breaking bugs, missing tests, incomplete implementation
  - Action: Block, return to component-builder with feedback, don't proceed until resolved
- **Important**: Performance concerns, code quality issues, missing edge cases
  - Action: Flag but allow proceed with user approval; ask: "Proceed with {issue} or fix now?"
- **Suggestions**: Code style, minor optimizations, documentation
  - Action: Document in tech debt, proceed, include in final report

**Failure Recovery Protocol**:
If component-builder fails:

- **At RED phase**: Document expected failure, ask user if test is correct
- **At GREEN phase**: Document implementation attempt, ask user for guidance
- **At REFACTOR phase**: Keep GREEN state, report partial completion, ask how to proceed

**Rollback Strategy**:
If integration-verifier finds breaking changes:

1. Document breaking change: "Integration failure: {component} breaks {integration}"
2. Options:
   - **Rollback component**: Revert component changes, restart from component-builder
   - **Fix integration**: Update integration code to accommodate component
   - **Accept breaking change**: Document as intentional change
3. Ask user which approach
4. Document decision in Actions Taken

**Example (TDD Cycle for a Component)**:

```
Component: User authentication validator
- RED: npm test tests/auth.spec.ts -> exit 1 (expected validateToken to be defined)
- GREEN: implement validateToken in src/auth.ts:42 -> npm test -> exit 0
- REFACTOR: extract helper isExpired() -> npm test -> exit 0
- REVIEW: code-reviewer -> "approved, consider rate limiting" (suggestion, proceed)
- INTEGRATION: integration-verifier -> e2e login flow passes -> exit 0
```

**Display Success Message** (after Phase 4 completion):

```
✅ Phase 4 Complete: Component Execution

Built:
- Components: [X] components built
- Tests: [Y] tests passing
- Reviews: ✅ Completed
- Integration: ✅ Verified

Next: Proceeding to Phase 5 - Aggregate Verification
```

**Build Workflow Inventory Validation** (MANDATORY after Phase 4):

- [ ] component-builder documented for EACH component in Actions Taken
- [ ] code-reviewer documented for EACH component (unless skipped)
- [ ] integration-verifier documented for EACH component (unless skipped)
- [ ] Sequential execution per component documented
- [ ] Parallel execution between components documented (if independent)
- [ ] All subagent outputs validated
- [ ] No component missing subagent sequence

**If ANY item missing**: STOP and invoke missing subagent immediately.

## Phase 5 - Aggregate Verification

**Before Verification** (optimized memory):

- **Validate Component Order**:
  - If component order worked successfully → update success_rate
  - If order failed → don't save, or update with lower success_rate
  - Validate dependency_hash matches current project (recalculate deps hash)
- **Store Only Validated Patterns**:
  - **Component Order**: Save ONLY if success_rate ≥ 70% and dependency_hash matches
  - Format: `{order: [...], success_rate, dependency_graph, validated_deps_hash, last_validated}`
  - **TDD Patterns**: Save successful patterns ONLY if validated across multiple components
  - **Review Feedback**: Save common patterns ONLY if appear frequently (>3 occurrences)
- **Pattern Validation**:
  - Compare predicted complexity → actual complexity
  - Update accuracy and confidence scores
  - Mark low-accuracy patterns for deletion
- **Run Cleanup**: Execute memory cleanup script after storing

**MANDATORY**: After all components complete, run comprehensive verification:

1. Run project regression suite: `npm test` (or equivalent)
2. Capture output and exit code
3. If coverage available, capture: `npm run coverage`
4. Run build/lint: `npm run build && npm run lint` (or equivalent)
5. Compose Verification Summary using exact template:

```
## Verification Summary
Scope: <components implemented>
Criteria: <all acceptance criteria>
Commands:
- npm test -> exit <code>
- npm run coverage -> exit <code> (coverage: {percentage}%)
- npm run build -> exit <code>
- npm run lint -> exit <code>
Evidence:
- <test output snippets>
- <coverage report if available>
- <build artifacts>
Risks / Follow-ups: <tech debt, suggestions, known issues>
- External Sources: <list any external documentation fetched and used>
```

**Validation Gate** (before proceeding to Phase 6):

**CRITICAL**: Execute this bash command to verify all components built and tests pass:

```bash
# Verify components exist
COMPONENT_FILES=("src/components/NewComponent.tsx" "src/components/NewComponent.test.tsx")  # Adjust based on actual components
MISSING_COMPONENTS=()

for file in "${COMPONENT_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_COMPONENTS+=("$file")
    fi
done

if [ ${#MISSING_COMPONENTS[@]} -gt 0 ]; then
    echo "Error: Missing component files: ${MISSING_COMPONENTS[*]}"
    exit 1
else
    echo "✓ All component files created"
fi

# Verify tests pass (if test command exists)
if command -v npm >/dev/null 2>&1 && [ -f "package.json" ]; then
    if npm test 2>&1 | grep -q "failing\|FAIL"; then
        echo "Error: Tests are failing"
        exit 1
    else
        echo "✓ All tests passing"
    fi
elif command -v pytest >/dev/null 2>&1; then
    if pytest 2>&1 | grep -q "FAILED\|failed"; then
        echo "Error: Tests are failing"
        exit 1
    else
        echo "✓ All tests passing"
    fi
else
    echo "Warning: No test runner detected, skipping test verification"
fi
```

**CRITICAL**: Do NOT proceed to Phase 6 until bash command exits with code 0.

**Display Success Message** (after Phase 5 completion):

```
✅ Phase 5 Complete: Verification

Verified:
- All components: ✅ Verified
- Tests: ✅ All passing
- Build: ✅ Successful
- Lint: ✅ Passed (if applicable)

Next: Proceeding to Phase 6 - Delivery
```

## Phase 6 - Delivery

**Display Success Message** (after Phase 6 completion):

```
✅ Phase 6 Complete: Build Complete

Delivered:
- Components: [X] components delivered
- Tests: [Y] tests passing
- Build report: ✅ Generated
- Ready for use: ✅ Yes

Next: Build workflow complete - All components delivered
```

## Quick Reference

**Phase Summary**:

- **Phase 0**: Functionality Analysis (MANDATORY FIRST) - Understand functionality requirements, document flows, extract acceptance criteria
- **Phase 1**: Complexity Gate - Assess complexity (1-5 scale), gate check if <=2
- **Phase 2**: Shared Context - Load required skills, establish shared context
- **Phase 3**: Component Queue - Build components sequentially per component (component-builder → code-reviewer → integration-verifier)
- **Phase 4**: Testing - Run tests and verify functionality works
- **Phase 5**: Integration Verification - Verify integration works
- **Phase 6**: Delivery - Generate build report with functionality verification FIRST

**Key Outputs**:

- Functionality analysis (user/admin/system flows)
- Component implementations with tests
- Test results with exit codes
- Integration verification results
- Build report with evidence

**Validation Requirements**:

- [ ] Phase 0 complete (functionality analysis done, gate checks passed)
- [ ] Complexity assessed and gated if <=2
- [ ] All required skills loaded successfully
- [ ] Components built sequentially with tests
- [ ] Tests run and exit codes verified (all passing)
- [ ] Functionality verified before claiming completion
- [ ] Evidence provided for all claims (test results, exit codes, file:line citations)

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Build Report

## Executive Summary

[2-3 sentences summarizing components implemented, overall status, and key outcomes]

## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented, acceptance criteria defined]
- Skills loaded: requirements-analysis, security-patterns, test-driven-development, verification-before-completion
- Subagents invoked: component-builder, code-reviewer, integration-verifier
- Components built: [list in order]
- Tools used: [Read, Edit, Write, Bash, Task]

## Functionality Analysis

[Include complete functionality analysis from Phase 0]

## Findings / Decisions

### Component Breakdown

For each component:

- **Component {name}**:
  - TDD Cycle: RED → GREEN → REFACTOR (commands and exit codes)
  - Key Changes: [file:line diffs summary]
  - Tests Added: [list]
  - Review Status: [approved/changes requested with details]
  - Integration Status: [pass/fail with evidence]

### Reviews & Integration

- code-reviewer findings: [resolved/open with file:line]
- integration-verifier scenarios: [pass/fail with logs]
- Blocking Issues: [list if any]
- Tech Debt: [suggestions documented]

## Verification Summary

[Use exact template from Phase 4]

## Recommendations / Next Steps

[Prioritized: Blocking issues first, then tech debt, then enhancements]

## Open Questions / Assumptions

[If any decisions need clarification or assumptions made]
```

**Validation Before Presenting**:

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes all commands with exit codes
- [ ] All components documented with TDD cycle evidence
- [ ] Review feedback classified (blocking/important/suggestions)
- [ ] Integration status documented with evidence
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken

**Offer Optional Next Steps**:

- "Run review workflow on implemented code?" (without assuming consent)
- "Run deployment workflow?" (without assuming consent)

## Failure Handling

**Standardized Error Recovery Protocol** (use orchestrator's template):

If any subagent or test fails:

1. **Context**: What was attempted (component, subagent, phase, command)
2. **Problem**: What failed (error message, exit code, test failure)
3. **Options**:
   - **Retry**: Attempt again (if transient error likely)
   - **Continue without {component}**: Skip component, proceed with others
   - **Abort workflow**: Stop and restart
4. **Impact**: Explain what each choice means
5. **Default**: Recommended action

**Critical Rules**:

- Do not mark components complete without verification summary
- Do not proceed past blocking review feedback
- Document all failures in Actions Taken section
- Never fabricate test results or verification evidence

## References

- Skills guide: `docs/reference/04-SKILLS.md`
- Subagent contract: `docs/reference/03-SUBAGENTS.md`
