# PLANNING Workflow - Structured Feature Design

**CRITICAL**: This workflow MUST be activated through cc10x-orchestrator. Do NOT execute this workflow directly. The orchestrator provides required context, coordinates skill loading, and manages subagent invocation. Direct execution bypasses all validation mechanisms.

**See SHARED-ENFORCEMENT.md for MANDATORY execution mode, enforcement rules, guardrails, and validation gates that apply to ALL workflows.**

**Triggered by:** User asks to plan, architect, or design a feature or system update.

## WHEN/HOW/WHY - PLAN Workflow

### WHEN to Use This Workflow

**Keywords that trigger PLAN workflow:**

- plan, planning, planner, plan a, plan the, plan for
- design, designing, designer, design a, design the
- architect, architecture, architectural, system design
- roadmap, road map, strategy, strategic planning
- feature planning, project planning, implementation plan

**Example user requests:**

- "plan a user authentication feature"
- "design a payment processing system"
- "create an architecture for file uploads"
- "I need a roadmap for this feature"

### HOW Orchestrator Selects This Workflow

**Detection Process:**

1. User says keyword like "plan" → Orchestrator skill loads automatically (via description keywords)
2. Orchestrator scans user request for workflow keywords
3. If "plan", "design", "architect", "roadmap", or "strategy" detected → PLAN workflow selected
4. Orchestrator activates this workflow file
5. Workflow executes phases: Functionality Analysis → Requirements → Architecture → Design → Deployment

**Decision Tree:**

```
User request contains "plan"/"design"/"architect"/"roadmap"/"strategy"?
├─ YES → PLAN workflow
└─ NO → Check other workflow keywords
```

### WHY Use PLAN Workflow vs Others

**Use PLAN workflow when:**

- You need to design architecture before building
- You need to identify risks and mitigation strategies
- You need to create implementation roadmap
- You need to plan deployment strategy
- You need to gather requirements and acceptance criteria

**PLAN vs BUILD:**

- PLAN: Design architecture, identify risks, create roadmap (no code written)
- BUILD: Implement components using TDD (code written)

**PLAN vs REVIEW:**

- PLAN: Design new features (forward-looking)
- REVIEW: Analyze existing code (backward-looking)

**PLAN vs DEBUG:**

- PLAN: Design solutions (proactive)
- DEBUG: Fix broken code (reactive)

**PLAN vs VALIDATE:**

- PLAN: Create new plans (creation)
- VALIDATE: Verify implementation matches plan (verification)

**See SHARED-ENFORCEMENT.md for TL;DR Quick Checklist, Guardrails, and Runtime Compliance Checks.**

**See orchestrator REFERENCE.md for tool usage guides and search guidance.**

## Phase 0 - Functionality Analysis (MANDATORY)

**CRITICAL**: This phase MUST be completed before any complexity gate, skill loading, or subagent dispatching. Understanding functionality is the foundation for all planning activities.

**Purpose**: Understand what functionality needs to be planned (user flows, admin flows, system flows, integration flows) and what research is needed before designing architecture, APIs, components, or deployment.

**Task Tool Usage** (phase tracking):

- Create tasks for all workflow phases at start:
  ```
  Task: Create tasks for workflow phases
  - Phase 0: Functionality Analysis (in_progress)
  - Phase 1: Complexity Gate (pending)
  - Phase 2: Requirements Intake (pending)
  - Phase 3: Delegated Analysis (pending)
  - Phase 4: Synthesis (pending)
  - Phase 5: Verification Summary (pending)
  - Phase 5.5: Context Preservation (mandatory, pending)
  - Phase 6: Deliverable (pending)
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
   - Read user request and any provided requirements
   - Understand the intended functionality
   - Document user flows, admin flows (if applicable), system flows, and integration flows
   - Identify external APIs, constraints, or documentation needed
3. **Research Planning** (if applicable):
   - Identify external APIs that need documentation
   - Identify integration constraints or limitations
   - Plan external resource checks (will be executed in Phase 1)
4. **Output**: Complete functionality analysis using template format:

   ```markdown
   ## Functionality Analysis

   ### What Functionality Needs Planning?

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
   ```

**Gate Check**: Before proceeding to Phase 1, ALL items below MUST be checked:

- [ ] Functionality analysis complete (user flow, admin flow if applicable, system flow, integration flow if applicable documented)
- [ ] Research needs identified (external APIs, constraints, documentation) if applicable
- [ ] External dependencies identified (libraries, services, APIs) if applicable
- [ ] Template format followed (all required sections completed)
- [ ] Functionality clear and understood (no ambiguous requirements)

**CRITICAL**: Do NOT proceed to Phase 1 until ALL items above are checked. If any item is incomplete:

- Ask user: "Functionality unclear. Please clarify: What functionality needs to be planned? What are the user flows? What are the system flows?"
- Do NOT proceed until functionality is understood and all gate check items are complete

**Display Success Message** (after Phase 0 completion):

```
✅ Phase 0 Complete: Functionality Analysis

Analyzed:
- User flows: [X] flows identified
- Admin flows: [Y] flows identified (if applicable)
- System flows: [Z] flows identified
- Integration flows: [W] flows identified (if applicable)
- Research items: [N] items needed (if any)
- Visual assets: [M] assets found (if any)

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
- **Semantic Match**: Use `jq` to filter by signature (file_count, change_type, has_external_deps) - not exact text
- **Top 3 Only**: Return top 3 highest-confidence patterns (confidence="high" or accuracy > 70%)
- **Efficient Query**: `jq '.complexity_patterns | to_entries | map(select(.value.signature.file_count == "3-5")) | sort_by(.value.accuracy) | reverse | .[0:3]' .claude/memory/patterns.json`
- If similar task found: "Found similar task in memory: {task} scored {score}, accuracy {accuracy}%. Use as reference?"

1. Estimate complexity using the orchestrator's Complexity Rubric (files changed, novelty, and risk cues).
2. If the score <=2, warn that cc10x is optimized for higher-risk work and wait for an explicit "yes" before proceeding.
3. **External Resource Check** (smart Q&A caching):
   - **Check Cache First**: Lookup {url, prompt} combinations in `.claude/memory/web_cache/cache_index.json`
   - **Cache Logic**:
     - Create hash from `{url}_{prompt}` for each planned question
     - If cached and TTL valid → use cached answer (skip fetch)
     - If cached but expired → re-fetch with same prompt
     - If not cached → fetch with prompt and cache answer (TTL: API specs 24h, framework docs 48h)
   - **Deduplication**: Track {url, prompt} combinations fetched in this workflow
   - Check if planning requires external documentation:
     - External APIs mentioned? → Plan targeted questions:
       - "What are all the API endpoints, HTTP methods, and their purposes?"
       - "What authentication method is required and how do I get credentials?"
       - "What are the main data models, their fields, and relationships?"
     - External services mentioned? → Plan questions about service capabilities, integration, limits
     - Frameworks mentioned? → Plan questions about setup, patterns, concepts
   - Ask user: "Detected external dependencies: {list}. Will ask {N} targeted questions. Found {M} in cache. Proceed? (yes/no)"
   - If yes, use WebFetch with prompts (check cache first, fetch if needed) and include answers in planning context
4. If resuming after compaction or context is unclear, read the latest snapshot and working plan:
   - Read `.claude/memory/snapshots/` most recent `snapshot-*.md`
   - Read `.claude/memory/WORKING_PLAN.md`

**Display Success Message** (after Phase 1 completion):

```
✅ Phase 1 Complete: Complexity Gate

Assessed:
- Complexity score: [1-5]
- Status: ✅ Proceeding / ⚠️ Low complexity warning shown
- External dependencies: [N] dependencies detected (if any)

Next: Proceeding to Phase 2 - Requirements Intake
```

## Phase 2 - Requirements Intake

**CRITICAL:** Phase 0 (Functionality Analysis) MUST be complete before proceeding.

**Optional: Documentation Generation** (at start of Phase 2, before requirements intake):

**Detection Logic:**

- Keywords: "document", "docs", "generate docs", "create design doc", "tech stack", "cursor rules", "app design"
- File patterns: Missing `.cursor/rules/app-design-document.mdc` or `.cursor/rules/tech-stack.mdc`
- User request contains documentation intent

**If Documentation Needed:**

1. **Detect Documentation Type:**
   - "app design" / "design doc" → Load `app-design-generation` skill
   - "tech stack" / "technical stack" → Load `tech-stack-generation` skill
   - "cursor rules" / "create rule" → Load `cursor-rules-generation` skill
   - "project structure" / "create doc" → Load `project-structure-generation` skill

2. **Execute Documentation Generation:**
   - Load appropriate skill (app-design-generation, tech-stack-generation, etc.)
   - Follow skill's process (codebase analysis, Q&A, document generation)
   - Save to `.cursor/rules/` directory
   - Update `.claude/memory/documentation_state.json` with generation timestamp

3. **Continue to Requirements Intake:**
   - Documentation complete → Proceed to alignment step
   - Documentation skipped → Continue to alignment step (existing flow)

**If Documentation Not Needed:**

- Continue directly to alignment step (existing flow unchanged)

**Alignment Step** (at start of Phase 2, before requirements gathering):

**Purpose:** Ensure understanding and alignment before planning begins.

**Process:**

1. **Use AskUserQuestion Tool:**
   - Question 1: "What are you trying to accomplish?" (clear understanding)
   - Question 2: "How should we approach this?" (step-by-step plan)
   - Question 3: "Which files/modules will be affected?" (file changes)
   - Question 4: "What risks or constraints should we consider?" (potential issues)
   - Question 5: "How will we know this is complete?" (success criteria)

2. **Wait for User Approval:**
   - Document alignment in Phase 0 Functionality Analysis
   - Proceed to requirements intake only after approval
   - If user skips alignment → Continue to requirements intake (existing flow unchanged)

**Integration:**

- Alignment responses feed into requirements intake
- Alignment documented in Phase 0 Functionality Analysis
- Alignment ensures requirements gathering is focused and efficient
- After alignment → Continue to "Integration with Brainstorming Skill" section below

**Integration with Brainstorming Skill**:

- **Load Skill**: Reference `brainstorming` skill for requirements refinement
- **Use Pattern**: Create design document incrementally (`.claude/docs/plans/<topic>-design.md`), ask questions using AskUserQuestion tool, update document after each answer
- **Output**: Refined requirements and design document ready for Phase 3

**Load Requirements Skills**:

- `project-context-understanding` - **MANDATORY** (understand existing architecture, dependencies, and conventions before planning)
- `requirements-analysis`
- `feature-planning` - **MANDATORY** (provides feature planning guidance)
- `design-patterns` - **MANDATORY** (provides API/component/integration patterns)
- `architecture-patterns` - **MANDATORY** (provides architecture design patterns)
- `risk-analysis` - **MANDATORY** (provides risk analysis framework)
- `verification-before-completion` - **MANDATORY** (verify plan completeness and accuracy before completion)
- `memory-tool-integration` (filesystem-based memory always available)
- `web-fetch-integration` (if external docs needed)

**Conditional Skills**:

- `ui-design` - Load if UI features mentioned (keywords: UI, interface, design, form, dashboard)
- `api-design-patterns` - Load if API planning detected (keywords: API, endpoint, REST, GraphQL, route)
- `component-design-patterns` - Load if component planning detected (keywords: component, UI component, React component, Vue component)
- `deployment-patterns` - Load if deployment planning detected (keywords: deploy, deployment, production, staging, CI/CD, infrastructure) - Required for `planning-design-deployment` subagent

**Detection Logic**:

- UI Features: Keywords "UI", "interface", "design", "form", "dashboard"
- API Planning: Keywords "API", "endpoint", "REST", "GraphQL", "route"
- Component Planning: Keywords "component", "UI component", "React component", "Vue component"
- Deployment Planning: Keywords "deploy", "deployment", "production", "staging", "CI/CD", "infrastructure", "Docker", "Kubernetes", "AWS", "cloud"

**Skill Loading Strategy**:

- All required skills are independent (no dependencies between them)
- **Load all required skills in parallel** for faster initialization
- **Load conditional skills** (`ui-design`, `api-design-patterns`, `component-design-patterns`, `deployment-patterns`, `web-fetch-integration`) based on detection logic, still in parallel with required skills
- **Skill Loading Verification**: Verify each skill loaded successfully (read first 100 chars, parse YAML, check content)
- If loading fails, use Error Recovery Protocol

**Memory Integration** (optimized):

- **Load Preferences**: Query `.claude/memory/preferences.json` for user preferences (if exists)
- **Query Requirements Patterns**: Check `.claude/memory/patterns.json` for similar requirements (use semantic match, top 3 only)
- **Validation Before Storage**: Only store requirements patterns after workflow completes and validates accuracy

**External Documentation** (smart Q&A caching):

- If external APIs/services mentioned in requirements:
  - **Plan Targeted Questions**: For each API/service, plan 3-4 specific questions:
    - Endpoints: "What are all the API endpoint paths, HTTP methods, and required parameters?"
    - Authentication: "How do I authenticate requests? What credentials are needed?"
    - Data Models: "What are the main data models, their fields, types, and relationships?"
    - Error Handling: "What error codes does this API return and what do they mean?"
  - **Check Cache First**: For each {url, prompt} combo, check cache_index.json
  - **Use Cache if Valid**: If cached and TTL valid → use cached answer (skip fetch)
  - **Fetch if Needed**: If not cached or expired → WebFetch with prompt and cache answer (24h TTL)
  - Include answers in requirements context (NOT raw content)

**Requirements Extraction Template**:
Use this structure for requirements intake:

```markdown
# Requirements Intake

## Core Goal

[One sentence describing the primary objective]

## Key Entities

[Users, data, systems involved]

## Key Operations

[CRUD operations, workflows, integrations]

## User Stories

- As a [role], I want [action] so that [benefit]
  - Acceptance Criteria:
    - [ ] Criterion 1 (measurable, testable)
    - [ ] Criterion 2 (measurable, testable)

## Stakeholders

[Roles and their concerns]

## Constraints

- Technical: [technology, performance, scale]
- Business: [timeline, budget, resources]
- Compliance: [regulations, standards]

## Assumptions

[List assumptions being made]

## Open Questions

[List questions requiring user input]
```

**Requirements Completeness Threshold**:

- **Critical Questions**: Count unanswered questions in Core Goal, Key Entities, Key Operations, User Stories (with acceptance criteria), Stakeholders, Constraints
- **Threshold**: If >3 critical questions unanswered → **Abort and request clarification**
- **Threshold Logic**:
  - Core Goal missing or vague → +1 critical question
  - Key Entities empty → +1 critical question
  - Key Operations empty → +1 critical question
  - User Stories missing acceptance criteria → +1 per story
  - Stakeholders empty → +1 critical question
  - Constraints empty → +1 critical question (assume some constraints exist)
- **Gate Check**: After requirements extraction, count critical questions:
  ```
  Critical Questions Count: {N}
  Threshold: 3
  Status: {N <= 3: "Requirements complete enough to proceed" | N > 3: "ABORT - Critical information missing"}
  ```
- **If Threshold Exceeded**:
  - Document: "Requirements incomplete: {list of missing items}. Total critical questions: {N} (threshold: 3)"
  - Ask user: "Critical information missing: {list}. Provide details before proceeding or mark assumptions explicit?"
  - **Do NOT proceed** until critical questions <= 3 or user explicitly confirms assumptions

**If Requirements Incomplete** (within threshold):

- Document what's missing: "Missing: [list]"
- Ask user: "Critical information missing: [list]. Provide details or proceed with assumptions?"
- If proceeding with assumptions, document them clearly in Open Questions section
- **Store in Memory**: Save requirements patterns for future similar tasks

**Ask Questions Tool Usage** (for requirements gathering):

- Use the askquestion tool to gather missing requirements:
  - What are the user stories?
  - What are the acceptance criteria?
  - What are the technical constraints?
  - What are the business constraints?
  - What are the dependencies?
- Proceed with planning using gathered requirements

**Task Tool Usage** (planning checklist):

- Create tasks for planning phases:
  ```
  Task: Create planning checklist
  - Requirements gathered (pending)
  - Architecture designed (pending)
  - Risks identified (pending)
  - Plan compiled (pending)
  ```
- Update task status as planning progresses

**Workflow State Persistence** (Checkpoint System):

- **Checkpoint After Each Phase**: Save workflow state to `.claude/memory/workflow_state/plan_{timestamp}.json`
- **Checkpoint Format**:
  ```json
  {
    "workflow": "plan",
    "phase": "Phase_1_Requirements_Intake",
    "timestamp": "2025-10-29T10:00:00Z",
    "state": {
      "requirements": {...},
      "complexity_score": 4,
      "external_docs_fetched": [...],
      "assumptions": [...],
      "open_questions": [...]
    },
    "next_phase": "Phase_2_Delegated_Analysis"
  }
  ```
- **Resume Logic**: If resuming after interruption:
  1. Read most recent checkpoint: `jq -s 'sort_by(.timestamp) | reverse | .[0]' .claude/memory/workflow_state/plan_*.json`
  2. Validate checkpoint state (requirements present, phase valid)
  3. Continue from `next_phase` with checkpoint state restored
  4. Ask user: "Resuming from Phase {N}. Continue from checkpoint or restart?"
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2, Phase 3, Phase 4, Phase 5 completion

**Display Success Message** (after Phase 2 completion):

```
✅ Phase 2 Complete: Requirements Intake

Gathered:
- Requirements: [X] requirements gathered
- Reusable patterns: [Y] patterns found (if any)
- User stories: [Z] stories with acceptance criteria
- Constraints: [W] constraints identified

Next: Proceeding to Phase 3 - Delegated Analysis
```

## Phase 3 - Delegated Analysis

**MANDATORY: Reusable Code Search**

**CRITICAL**: Do NOT proceed to architecture design until reusable code search is complete.

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
   - Note patterns to follow in architecture design
   - Reference existing code in architecture decisions

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

**CRITICAL**: Reference reusable code in architecture design section. Do NOT design new patterns if existing ones can be reused.

**When to Invoke Subagents**:

- **INVOKE** - Architecture needed: Complexity score >= 3 OR multi-file/multi-component work → Invoke `planning-architecture-risk`
- **INVOKE** - Design/deployment needed: Any build work requires API design OR component design OR deployment planning → Invoke `planning-design-deployment`
- **INVOKE** - Complete planning: Both subagents needed for comprehensive planning (default for complexity >= 3)

**When NOT to Invoke Subagents**:

- **SKIP** - Complexity too low: Complexity score <= 2 → Skip `planning-architecture-risk` (architecture not needed), ask user: "Low complexity ({score}). Skip architecture planning? (yes/no)"
- **SKIP** - No API/component design needed: If work is pure refactoring or config changes (no new APIs/components) → Skip `planning-design-deployment`, only invoke `planning-architecture-risk` if complexity >= 3
- **SKIP** - User explicitly skips: If user says "skip architecture" or "skip design" → Skip corresponding subagent, document in Actions Taken
- **SKIP** - Single-file trivial change: If change is single file, <200 lines, no architectural impact → Skip both subagents, proceed with build workflow directly
- **SKIP** - Architecture already exists: If user says "architecture already defined" → Skip `planning-architecture-risk`, only invoke `planning-design-deployment` if needed

**Conflict Prevention**:

- **Sequential execution**: Always run `planning-architecture-risk` FIRST, then `planning-design-deployment` (architecture informs design)
- **No parallel execution**: Never invoke both simultaneously (architecture decisions needed before design)
- **Share context**: `planning-design-deployment` receives architecture outputs from `planning-architecture-risk` as input

**Subagent Dependency**:

- `planning-design-deployment` DEPENDS on `planning-architecture-risk` outputs (architecture, risk register)
- If `planning-architecture-risk` fails or skipped, provide minimal context to `planning-design-deployment` and flag limitation

**Default Sequence** (unless conditions above met):
Run the bundled planning subagents sequentially, sharing the Phase 1 notes as context:

1. `planning-architecture-risk` (loads `architecture-patterns` and `risk-analysis`) - FIRST.
2. `planning-design-deployment` (loads `api-design-patterns`, `component-design-patterns`, and `deployment-patterns`) - SECOND (receives architecture outputs).

**Integration with Feature Planning Skill**:

- **Load Skill**: Reference `feature-planning` skill (enhanced with writing-plans patterns) for detailed implementation plan creation
- **Use Pattern**: Create detailed implementation plan with bite-sized tasks, incremental plan file updates, exact file paths, complete code examples
- **Output**: Detailed implementation plan (`.claude/docs/plans/<feature-name>-plan.md`) ready for execution

**Integration with Planning Workflow Skill**:

- **Load Skill**: Reference `planning-workflow` skill (enhanced with executing-plans patterns) for batch execution guidance
- **Use Pattern**: Execute plan in batches (default: first 3 tasks), report between batches, verify after each batch
- **Output**: Execution guidance and checkpoint coordination

Each subagent must:

- Reference the skill sections used to make decisions.
- Produce actionable outputs (diagrams, data models, API specs, risk register, deployment steps).
- Identify outstanding assumptions that require user confirmation.

**Subagent Invocation Pattern**:

- Verify subagent exists: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SUBAGENT.md`
- Read the subagent's SUBAGENT.md to load its process and output format.
- Provide the requirements summary and constraints from Phase 1.
- Require the specified outputs with clear traceability to requirements.
- **Subagent Output Validation** (after subagent completes):
  - **Validation Checklist**:
    - [ ] Output format matches expected template (check required sections present)
    - [ ] All required fields present (architecture views, risk register, API design, etc.)
    - [ ] File references include path:line where applicable
    - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections
    - [ ] Output is actionable (not just descriptions)
  - **Validation Failure**: If output invalid:
    - Report: "Subagent '{name}' output validation failed: {missing_field}/{invalid_format}"
    - Options: Retry subagent / Request manual correction / Continue with partial output
    - Wait for user decision
- **If subagent fails**: Use Error Recovery Protocol
  - Options: Retry / Continue without {subagent} / Abort workflow
  - Wait for user decision (with 5-minute timeout per orchestrator error recovery)

**Subagent Output Requirements**:
Each subagent must produce:

- Actionable outputs (diagrams, data models, API specs, risk register, deployment steps)
- Traceability: Link each decision back to specific requirements
- Assumptions: List any assumptions made
- Open Questions: Items requiring user confirmation

**Display Success Message** (after Phase 3 completion):

```
✅ Phase 3 Complete: Architecture Design

Designed:
- Components: [X] components designed
- APIs: [Y] APIs planned
- Architecture decisions: [Z] decisions made
- Risks identified: [W] risks assessed

Next: Proceeding to Phase 4 - Synthesis
```

**Plan Workflow Inventory Validation** (MANDATORY after Phase 3):

- [ ] planning-architecture-risk documented in Actions Taken (FIRST)
- [ ] planning-design-deployment documented in Actions Taken (SECOND)
- [ ] Sequential execution documented
- [ ] Architecture outputs passed to design subagent documented
- [ ] All subagent outputs validated
- [ ] No planning subagent missing (unless skip condition met)

**If ANY item missing**: STOP and invoke missing subagent immediately.

## Phase 4 - Synthesis

**Conflict Resolution Protocol**:
If subagents disagree on architecture decisions:

1. Document both positions explicitly:
   ```
   Conflict Detected:
   - planning-architecture-risk: [decision/position] - Rationale: [reason]
   - planning-design-deployment: [conflicting decision/position] - Rationale: [reason]
   ```
2. Identify root cause:
   - Different assumptions (e.g., scalability requirements)
   - Different priorities (e.g., speed vs maintainability)
   - Different interpretations of requirements
3. Present to user with options:
   - **Accept architecture subagent's view**: [reason]
   - **Accept design subagent's view**: [reason]
   - **Hybrid approach**: Combine both (document how)
   - **Provide additional context**: User clarifies to resolve
4. Document resolution clearly in final plan

**Synthesis Steps**:

1. Merge subagent outputs into a single plan outline.
2. Apply Conflict Resolution Protocol for any conflicts.
3. Build file manifest and phased roadmap, noting dependencies between components.
4. **Dependency Validation**: Check for circular dependencies - if found, flag immediately and ask user to resolve.

**Implementability Check** (BEFORE finalizing plan):
For each component, verify:

- [ ] Dependencies identified and available (libraries, services, APIs)
- [ ] Technical feasibility confirmed (skills, technology available)
- [ ] Effort estimated and realistic (time, complexity)
- [ ] No circular dependencies (component A depends on B, B depends on A)
- [ ] Data contracts defined (inputs/outputs clear)
- [ ] Integration points identified (APIs, events, shared state)

If any check fails:

- Flag immediately: "Implementability concern: {issue}"
- Ask user: "Resolve {issue} before proceeding or mark as risk?"

**Validation Gate** (before proceeding to Phase 5):

**CRITICAL**: Execute this bash command to verify all required planning deliverables exist:

```bash
# Verify planning deliverables exist
REQUIRED_FILES=("plan.md" "architecture.md")
PLANNING_DIR="docs/planning"  # Adjust based on actual output directory

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PLANNING_DIR/$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "Error: Missing planning files: ${MISSING_FILES[*]}"
    exit 1
else
    echo "✓ All required planning files created"
fi

# Verify plan.md has required sections
if [ -f "$PLANNING_DIR/plan.md" ]; then
    REQUIRED_SECTIONS=("Functionality Analysis" "Architecture" "API Design" "Component Design")
    MISSING_SECTIONS=()
    for section in "${REQUIRED_SECTIONS[@]}"; do
        if ! grep -q "## $section" "$PLANNING_DIR/plan.md"; then
            MISSING_SECTIONS+=("$section")
        fi
    done

    if [ ${#MISSING_SECTIONS[@]} -gt 0 ]; then
        echo "Error: Missing sections in plan.md: ${MISSING_SECTIONS[*]}"
        exit 1
    else
        echo "✓ All required sections present in plan.md"
    fi
fi
```

**CRITICAL**: Do NOT proceed to Phase 5 until bash command exits with code 0.

**Display Success Message** (after Phase 4 completion):

```
✅ Phase 4 Complete: Synthesis

Synthesized:
- Architecture decisions: [X] decisions documented
- Risks identified: [Y] risks assessed
- Components planned: [Z] components
- Dependencies mapped: [W] dependencies

Next: Proceeding to Phase 5 - Verification Summary
```

## Phase 5 - Verification Summary

**MANDATORY**: Use exact template:

```
## Verification Summary
Scope: <feature/system planned>
Inputs: <sources reviewed - requirements, existing code, patterns>
Decisions: <key architecture decisions with rationale>
- Decision 1: [what] - Rationale: [why] - Impact: [consequences]
- Decision 2: [what] - Rationale: [why] - Impact: [consequences]
Open Questions: <items awaiting user confirmation>
Implementability: <all checks passed or concerns flagged>
```

**Example**:

```
## Verification Summary
Scope: User authentication system
Inputs: requirements doc, existing API patterns, security guidelines
Decisions:
- JWT auth - Rationale: Stateless, mobile-friendly, scalable - Impact: No server-side sessions
- Event-driven webhooks - Rationale: Async resilience, decoupling - Impact: Eventual consistency
Open Questions: Stripe vs PayPal for payments? Monitoring SLA requirements?
Implementability: All dependencies available, team has skills, no circular dependencies
```

**Display Success Message** (after Phase 5 completion):

```
✅ Phase 5 Complete: Planning

Delivered:
- Planning deliverables: [X] deliverables created
- Architecture: ✅ Documented
- Risks: ✅ Assessed
- Ready for build: ✅ Yes

Next: Planning workflow complete - Ready for build
```

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

Next: Proceeding to Phase 6 - Deliverable
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

## Phase 6 - Deliverable

**CRITICAL**: Phase 5.5 (Context Preservation) MUST be completed before this phase.

**CRITICAL**: After saving the plan file, create plan reference for build workflow access.

**Plan Saving** (MANDATORY after plan creation):

1. **Save Plan File**: Save detailed implementation plan to `.claude/docs/plans/<feature-name>-plan.md`
   - Extract feature name from Phase 0 functionality analysis or user request
   - Use kebab-case for filename (e.g., `user-authentication-plan.md`)
   - Ensure `.claude/docs/plans/` directory exists (create if needed)

2. **Create Plan Reference** (MANDATORY):
   - Create `.claude/memory/current_plan.txt` containing the plan path: `.claude/docs/plans/<feature-name>-plan.md`
   - This allows build workflow to find the active plan
   - Example: `echo ".claude/docs/plans/user-authentication-plan.md" > .claude/memory/current_plan.txt`

3. **Update WORKING_PLAN.md** (optional but recommended):
   - Update `.claude/memory/WORKING_PLAN.md` with reference to full plan
   - Add line: "See full plan: `.claude/docs/plans/<feature-name>-plan.md`"
   - Preserve existing content, just add reference

**Plan Reference Format**:

```bash
# Create plan reference file
PLAN_DIR=".claude/docs/plans"
FEATURE_NAME="user-authentication"  # Extract from functionality analysis
PLAN_FILE="$PLAN_DIR/${FEATURE_NAME}-plan.md"

# Ensure directory exists
mkdir -p "$PLAN_DIR"

# Save plan reference
echo "$PLAN_FILE" > .claude/memory/current_plan.txt

# Update WORKING_PLAN.md with reference
if [ -f ".claude/memory/WORKING_PLAN.md" ]; then
    echo "" >> .claude/memory/WORKING_PLAN.md
    echo "## Active Plan" >> .claude/memory/WORKING_PLAN.md
    echo "See full plan: $PLAN_FILE" >> .claude/memory/WORKING_PLAN.md
fi
```

**Before Finalizing** (optimized memory):

- **Pattern Validation**:
  - Compare predicted complexity (from Phase 0) → actual complexity experienced
  - Calculate accuracy: `(predicted_match_actual ? 1 : 0) / 1` (first use) or `(matches / total_uses)` (subsequent)
  - Update confidence: high (>80%), medium (60-80%), low (<60%)
- **Store Only Validated Patterns**:
  - **Complexity Pattern**: Save to `.claude/memory/patterns.json` ONLY if accuracy can be calculated (after completion)
  - Format: `{signature: {file_count, change_type, deps}, predicted_score, actual_scores: [score], accuracy, usage_count, confidence}`
  - **Architectural Patterns**: Save common approaches IF validated successful
  - **User Preferences**: Save ONLY if user explicitly made choice (never infer)
- **Update Existing Patterns**:
  - If pattern exists, update: accuracy, usage_count, last_validated, confidence
  - If accuracy < 50% after 3+ uses → mark for deletion (cleanup will remove)
- **Run Cleanup**: Execute memory cleanup script after storing patterns

## Quick Reference

**Phase Summary**:

- **Phase 0**: Functionality Analysis (MANDATORY FIRST) - Understand what functionality needs planning, document flows, plan research
- **Phase 1**: Complexity Gate - Assess complexity (1-5 scale), gate check if <=2
- **Phase 2**: Requirements Intake - Gather requirements using Ask Questions tool if needed, load required skills
- **Phase 3**: Architecture Design - Invoke planning subagents sequentially (architecture-risk → design-deployment)
- **Phase 4**: Plan Synthesis - Synthesize plan with functionality-first approach
- **Phase 5**: Deliverable Generation - Generate planning deliverable

**Key Outputs**:

- Functionality analysis (user/admin/system flows)
- Architecture decisions with trade-offs
- API designs with examples
- Component designs with examples
- Deployment strategies with examples
- Risk mitigation strategies
- Planning deliverable document

**Validation Requirements**:

- [ ] Phase 0 complete (functionality analysis done, gate checks passed)
- [ ] Complexity assessed and gated if <=2
- [ ] All required skills loaded successfully
- [ ] Subagents invoked correctly (existence verified, dependencies analyzed, sequential execution)
- [ ] All design decisions justified with functionality requirements
- [ ] Evidence provided for all claims (file:line citations, examples)

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Planning Report

## Executive Summary

[2-3 sentences summarizing scope, constraints, goals, and overall plan status]

## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow, integration flow documented]
- Skills loaded: requirements-analysis, architecture-patterns, risk-analysis, api-design-patterns, component-design-patterns, deployment-patterns
- Subagents invoked: planning-architecture-risk, planning-design-deployment
- Inputs reviewed: [list]
- Tools used: [list]

## Functionality Analysis

[Include complete functionality analysis from Phase 0]

## Findings / Decisions

### Requirements Overview

- Goals: [list]
- User Stories: [list with acceptance criteria]
- Stakeholders: [list]
- Constraints: [list]

### Architecture & Component Design

- System Context: [textual diagram]
- Container View: [components and responsibilities]
- Component Breakdown: [detailed components]
- Data Models: [tables, entities, relationships]

### API/Data Models

- Endpoints: [list with contracts]
- Data Models: [entities with fields]
- Integration Points: [external services, events]

### Risk Register

- Risk 1: [description] - Probability: [1-5] - Impact: [1-5] - Score: [P×I] - Mitigation: [action] - Owner: [role]
- Risk 2: [same format]

### Implementation Roadmap

- Phase 1: [components] - Dependencies: [list] - Files: [manifest]
- Phase 2: [components] - Dependencies: [list] - Files: [manifest]

### Testing & Deployment Strategy

- Unit Testing: [approach]
- Integration Testing: [approach]
- Deployment: [strategy, rollback plan]

## Verification Summary

[Use exact template from Phase 4]

## Recommendations / Next Steps

[Prioritized: Critical decisions needed, then implementation phases]

## Open Questions / Assumptions

[If any conflicts detected, implementability concerns, or assumptions made]
```

**Validation Before Presenting**:

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes inputs, decisions, open questions
- [ ] All architecture decisions have rationale
- [ ] Risk register includes probability/impact scores
- [ ] File manifest and roadmap include dependencies
- [ ] Implementability checks documented
- [ ] Conflicts resolved or flagged
- [ ] All subagents/skills documented in Actions Taken

**Offer Optional Next Steps**:

- "Run build workflow for Phase 1?" (without assuming consent)
- "Review this plan before implementation?" (without assuming consent)

## Failure Handling

**Standardized Error Recovery Protocol** (use orchestrator's template):

If any skill or subagent fails:

1. **Context**: What was attempted (skill/subagent name, phase, input provided)
2. **Problem**: What failed (error message, missing output, invalid format)
3. **Options**:
   - **Retry**: Attempt again (if transient error likely)
   - **Continue without {component}**: Proceed with partial plan (document what's missing)
   - **Abort workflow**: Stop and restart
4. **Impact**: Explain what each choice means
5. **Default**: Recommended action

**Critical Rules**:

- Do not fabricate architecture decisions; clearly mark any sections that could not be produced
- Never proceed without user decision when failure occurs
- Document all failures in Actions Taken section
- If planning cannot proceed without failed component, abort rather than fabricate

## References

- Skill format: `docs/reference/04-SKILLS.md`
- Subagent expectations: `docs/reference/03-SUBAGENTS.md`
