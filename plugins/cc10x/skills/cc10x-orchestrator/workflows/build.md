# BUILD Workflow - TDD Driven Implementation

**Triggered by:** User requests implementation or feature build work.

## Phase 0 - Complexity Gate

**Memory Integration** (optimized):
- **Load Once**: Read `.claude/memory/patterns.json` ONCE, cache for workflow duration
- **Semantic Match**: Use `jq` to filter by build signature (similar to planning pattern)
- **Top 3 Only**: Return top 3 highest-confidence patterns
- **Component Orders**: Check `.claude/memory/patterns.json` for component_orders matching task type
- **Validate Dependencies**: If component order found, verify dependency_hash matches current deps

- Estimate scope. If complexity <=2, present the lightweight warning and wait for explicit approval before continuing.
- Confirm repositories, directories, and acceptance criteria.

**External Resource Check** (smart caching):
- **Check Cache First**: Lookup URLs in `.claude/memory/web_cache/cache_index.json`
- **Cache Logic**:
  - If cached and TTL valid → use cache (skip fetch)
  - If cached but expired → re-fetch
  - If not cached → fetch and cache (library docs: 14 days TTL)
- **Deduplication**: Track URLs fetched in this workflow
- Check if build requires external documentation:
  - Libraries/frameworks mentioned? → Check cache, then fetch library documentation if needed
  - SDKs mentioned? → Check cache, then fetch SDK examples if needed
  - External APIs? → Check cache, then fetch API integration guides if needed
- Ask user: "Detected external dependencies: {list}. Found {N} in cache, need to fetch {M} more. Proceed? (yes/no)"

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
- **Checkpoint Triggers**: After Phase 0, Phase 1, Phase 2, Phase 3 (after each component), Phase 4 completion

**If resuming after compaction or context is unclear**, use checkpoint system:
  - Read most recent checkpoint from `.claude/memory/workflow_state/build_*.json`
  - If checkpoint exists: Restore state and continue from `next_phase`
  - If no checkpoint: Read `.claude/memory/snapshots/` most recent `snapshot-*.md` and `.claude/memory/WORKING_PLAN.md` as fallback

## Phase 1 - Shared Context

**Required Skills**:
- `requirements-analysis`
- `security-patterns`
- `test-driven-development`
- `verification-before-completion`
- `memory-tool-integration` (filesystem-based memory always available)
- `web-fetch-integration` (if external docs needed)

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

## Phase 2 - Component Queue

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

**Sequential Execution Policy**:
- Process components sequentially without overlap
- If user requests parallel runs, confirm scope and handle as separate sequential passes
- Document component order in Actions Taken section
- **Skip blocked components** until dependencies resolved

## Phase 3 - Component Execution Loop
For every component:
1. Invoke `component-builder` with the brief. Require:
   - Failing test first (RED) with command output captured.
   - Minimal implementation (GREEN).
   - Refactor while keeping tests green.
   - Verification log referencing commands executed.
2. Invoke `code-reviewer` on the resulting changes. Expect:
   - Findings with file/line references.
   - Security/performance considerations tied to the relevant skills.
   - Recommendations or approval status.
3. Invoke `integration-verifier` to confirm broader system behaviour. Expect:
   - Integration or end-to-end checks.
   - Additional tests or scripts run, plus their outputs.
4. Consolidate notes. Address blocking review feedback before moving to the next component.
5. File size sanity check: Before moving on, scan changed files; if any exceeds ~500 lines, propose a concrete refactor/split plan.

**Subagent Invocation Pattern** (for each subagent):
- Verify subagent exists: Read first 100 chars of `plugins/cc10x/subagents/{subagent-name}/SKILL.md` or `SUBAGENT.md`
- Read the subagent's SKILL.md to load its process and output format.
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

## Phase 4 - Aggregate Verification

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

## Phase 5 - Delivery

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Build Report

## Executive Summary
[2-3 sentences summarizing components implemented, overall status, and key outcomes]

## Actions Taken
- Skills loaded: requirements-analysis, security-patterns, test-driven-development, verification-before-completion
- Subagents invoked: component-builder, code-reviewer, integration-verifier
- Components built: [list in order]
- Tools used: [Read, Edit, Write, Bash, Task]

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
