# PLANNING Workflow - Structured Feature Design

**Triggered by:** User asks to plan, architect, or design a feature or system update.

## Phase 0 - Complexity Gate

**Memory Integration** (optimized):
- **Load Once**: Read `.claude/memory/patterns.json` ONCE, cache for workflow duration
- **Semantic Match**: Use `jq` to filter by signature (file_count, change_type, has_external_deps) - not exact text
- **Top 3 Only**: Return top 3 highest-confidence patterns (confidence="high" or accuracy > 70%)
- **Efficient Query**: `jq '.complexity_patterns | to_entries | map(select(.value.signature.file_count == "3-5")) | sort_by(.value.accuracy) | reverse | .[0:3]' .claude/memory/patterns.json`
- If similar task found: "Found similar task in memory: {task} scored {score}, accuracy {accuracy}%. Use as reference?"

1. Estimate complexity using the orchestrator's Complexity Rubric (files changed, novelty, and risk cues).
2. If the score <=2, warn that cc10x is optimized for higher-risk work and wait for an explicit "yes" before proceeding.
3. **External Resource Check** (smart caching):
   - **Check Cache First**: Lookup URLs in `.claude/memory/web_cache/cache_index.json`
   - **Cache Logic**:
     - If cached and TTL valid → use cache (skip fetch)
     - If cached but expired → re-fetch
     - If not cached → fetch and cache with TTL (API specs: 7 days, framework docs: 30 days)
   - **Deduplication**: Track URLs fetched in this workflow, avoid duplicates
   - Check if planning requires external documentation:
     - External APIs mentioned? → Check cache, then fetch API specifications if needed
     - External services mentioned? → Check cache, then fetch service documentation if needed
     - Frameworks mentioned? → Check cache, then fetch framework documentation if needed
   - Ask user: "Detected external dependencies: {list}. Found {N} in cache, need to fetch {M} more. Proceed? (yes/no)"
   - If yes, fetch missing docs and include in planning context
4. If resuming after compaction or context is unclear, read the latest snapshot and working plan:
   - Read `.claude/memory/snapshots/` most recent `snapshot-*.md`
   - Read `.claude/memory/WORKING_PLAN.md`

## Phase 1 - Requirements Intake

**Load Requirements Skill**:
- Load the `requirements-analysis` skill.
- Load `memory-tool-integration` skill (filesystem-based memory always available)
- Load `web-fetch-integration` skill (if external docs needed)
- **Skill Loading Verification**: Verify skill loaded successfully (read first 100 chars, parse YAML, check content)
- If loading fails, use Error Recovery Protocol

**Memory Integration** (optimized):
- **Load Preferences**: Query `.claude/memory/preferences.json` for user preferences (if exists)
- **Query Requirements Patterns**: Check `.claude/memory/patterns.json` for similar requirements (use semantic match, top 3 only)
- **Validation Before Storage**: Only store requirements patterns after workflow completes and validates accuracy

**External Documentation** (smart caching):
- If external APIs/services mentioned in requirements:
  - **Check Cache First**: Lookup API spec URLs in `.claude/memory/web_cache/cache_index.json`
  - **Use Cache if Valid**: If cached and TTL valid → use cache (skip fetch)
  - **Fetch if Needed**: If not cached or expired → fetch and cache with 7-day TTL
  - Load service documentation (same cache-first approach)
  - Include in requirements context

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
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2, Phase 3, Phase 4 completion

## Phase 2 - Delegated Analysis
Run the bundled planning subagents sequentially, sharing the Phase 1 notes as context:
1. `planning-architecture-risk` (loads `architecture-patterns` and `risk-analysis`).
2. `planning-design-deployment` (loads `api-design-patterns`, `component-design-patterns`, and `deployment-patterns`).

Each subagent must:
- Reference the skill sections used to make decisions.
- Produce actionable outputs (diagrams, data models, API specs, risk register, deployment steps).
- Identify outstanding assumptions that require user confirmation.

**Subagent Invocation Pattern**:
- Verify subagent exists: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SKILL.md` or `SUBAGENT.md`
- Read the subagent's SKILL.md to load its process and output format.
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

## Phase 3 - Synthesis

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

## Phase 4 - Verification Summary

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

## Phase 5 - Deliverable

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

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Planning Report

## Executive Summary
[2-3 sentences summarizing scope, constraints, goals, and overall plan status]

## Actions Taken
- Skills loaded: requirements-analysis, architecture-patterns, risk-analysis, api-design-patterns, component-design-patterns, deployment-patterns
- Subagents invoked: planning-architecture-risk, planning-design-deployment
- Inputs reviewed: [list]
- Tools used: [list]

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
