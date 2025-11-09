# VALIDATION Workflow - Cross-Artifact Consistency

**CRITICAL**: This workflow MUST be activated through cc10x-orchestrator. Do NOT execute this workflow directly. The orchestrator provides required context, coordinates skill loading, and manages subagent invocation. Direct execution bypasses all validation mechanisms.

**🚨 CRITICAL ENFORCEMENT - DO NOT WRITE CODE DIRECTLY 🚨**

**MANDATORY RULES** (Violation = Workflow Failure):

1. **DO NOT write code directly** - This workflow uses direct analysis (no subagents), but you MUST:
   - Follow orchestrator validation mechanisms
   - Update Actions Taken IMMEDIATELY after each phase
   - Never skip Actions Taken tracking

2. **DO NOT skip Actions Taken tracking** - Update Actions Taken IMMEDIATELY after:
   - Each phase completed (mark phase as complete)
   - Each comparison performed (plan vs code, code vs tests, code vs docs)
   - Never proceed to next phase without updating Actions Taken

3. **DO NOT skip memory integration** - You MUST:
   - Query patterns before complexity scoring (load patterns.json ONCE, cache for workflow duration)
   - Store patterns after workflow completion (validate first, update accuracy)

4. **DO NOT skip web fetch integration** - You MUST:
   - When external APIs/libraries/frameworks mentioned, fetch documentation
   - Use question-based prompts (not raw content requests)
   - Check cache first, use cache if valid, fetch if needed

**If you violate ANY of these rules, Phase 4 validation will FAIL and you will be forced to correct before proceeding.**

**Triggered by:** User wants to confirm the implementation matches an existing plan, tests, or documentation set.

## Prerequisites

- Plan or requirements source identified (e.g., `.claude/plans/<feature>.md` or user-specified document).
- Scope of code to check (directories, modules, PR diff).

## TL;DR Quick Checklist

**CRITICAL**: Complete ALL items below. Skipping any item will cause workflow validation to FAIL.

- [ ] Complete Phase 0: Functionality Analysis FIRST (understand validation requirements, map functionality from plan/code/tests)
- [ ] Load plan/requirements and code scope
- [ ] **UPDATE Actions Taken** - Document plan/requirements loaded IMMEDIATELY
- [ ] Compare plan vs code (functionality alignment, missing features, extra features)
- [ ] **UPDATE Actions Taken** - Document plan vs code comparison IMMEDIATELY
- [ ] Compare code vs tests (test coverage, missing tests, untested code)
- [ ] **UPDATE Actions Taken** - Document code vs tests comparison IMMEDIATELY
- [ ] Compare code vs documentation (documentation accuracy, missing docs)
- [ ] **UPDATE Actions Taken** - Document code vs docs comparison IMMEDIATELY
- [ ] Generate validation report with functionality verification FIRST, then consistency checks

## Guardrails

**CRITICAL**: These guardrails MUST be followed in the Validate workflow. Violations lead to incomplete or incorrect validation.

- **Functionality First**: Always understand what functionality is being validated (user flows, admin flows, system flows) BEFORE comparing plan vs code, code vs tests, or code vs documentation.

- **Evidence Required**: Every validation finding must include file:line citations or specific references. No assertions without proof.

- **Alignment Focus**: Validate alignment between artifacts (plan, code, tests, docs). Focus on functionality alignment, not style or minor inconsistencies.

- **Scope Awareness**: Validate only what was requested. Don't expand beyond the requested scope unless explicitly asked.

## Search Guidance

**CRITICAL**: Use the right tool for each search task in the Validate workflow.

**Phase 0 - Functionality Analysis**:

- **Discovery**: Use `Glob` to find plan/requirements files (`Glob(".claude/plans/**/*.md")` or `Glob("docs/**/*.md")`)
- **Content Search**: Use `Grep` to find functionality references (`Grep("user flow|admin flow|system flow")`)
- **Detail Reading**: Use `Read` to read plan/requirements files (`Read(".claude/plans/feature.md")` for plan)
- **Example**: Validating implementation against plan:
  - Step 1: `Glob(".claude/plans/**/*.md")` → Find plan files
  - Step 2: `Grep("functionality|feature|requirement", path=".claude/plans")` → Find requirements
  - Step 3: `Read(".claude/plans/feature.md")` → Read plan details

**Phase 1 - Intake**:

- **Plan Discovery**: Use `Glob` to find plan files (`Glob("**/*plan*.md")` or `Glob("**/*requirements*.md")`)
- **Code Scope**: Use `Glob` to find code files (`Glob("src/**/*.{ts,tsx}")` for TypeScript files)
- **Test Discovery**: Use `Glob` to find test files (`Glob("**/*.test.{ts,tsx}")`)

**Phase 2 - Plan vs Code**:

- **Feature Mapping**: Use `Grep` to find feature implementations (`Grep("function.*featureName")`)
- **Requirement Mapping**: Use `Grep` to find requirement references (`Grep("TODO|FIXME|requirement")`)

**Phase 3 - Code vs Tests**:

- **Test Coverage**: Use `Grep` to find test cases (`Grep("describe|it|test")`)
- **Implementation Mapping**: Use `Grep` to find implementations (`Grep("export.*function")`)

**Anti-Patterns**:

- ❌ Using `Read` to search for patterns (use `Grep` instead)
- ❌ Using `Grep` to find files by name (use `Glob` instead)
- ❌ Reading entire large files when only a section is needed (use `Read` with offset/limit)

## Phase 0 - Functionality Analysis (MANDATORY)

**CRITICAL**: This phase MUST be completed before any intake, skill loading, or validation checks. Understanding functionality is the foundation for all validation activities.

**Purpose**: Understand what functionality is being validated (user flows, admin flows, system flows) and what the plan/code/tests/documentation should cover before comparing artifacts.

**Task Tool Usage** (phase tracking):

- Create tasks for all workflow phases at start:
  ```
  Task: Create tasks for workflow phases
  - Phase 0: Functionality Analysis (in_progress)
  - Phase 1: Intake (pending)
  - Phase 2: Plan vs Code (pending)
  - Phase 3: Code vs Tests (pending)
  - Phase 4: Code vs Documentation (pending)
  - Phase 5: Verification Summary (pending)
  - Phase 6: Report (pending)
  ```
- Update task status as phases complete:
  ```
  Task: Update Phase 0 status to completed
  Task: Update Phase 1 status to in_progress
  ```

**Process**:

1. **Load Functionality Analysis Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
2. **Analyze Plan/Requirements** (if available):
   - Read plan or requirements document
   - Understand intended functionality
   - Document user flows, admin flows (if applicable), system flows, and integration flows
3. **Analyze Code**:
   - Read code scope to be validated
   - Understand what functionality is implemented
   - Document implemented user flows, admin flows (if applicable), and system flows
4. **Output**: Complete functionality analysis using template format:

   ```markdown
   ## Functionality Analysis

   ### What Functionality is Being Validated?

   [Clear description of functionality]

   ### User Flow (from plan/code)

   1. [Step 1: User action]
   2. [Step 2: System response]
   3. [Step 3: User sees result]
      ...

   ### Admin Flow (if applicable)

   [Similar structure]

   ### System Flow (from plan/code)

   1. [Step 1: System receives input]
   2. [Step 2: System processes]
   3. [Step 3: System stores/transforms]
   4. [Step 4: System sends output]
      ...

   ### Integration Flow (if applicable)

   [Similar structure]
   ```

**Gate Check**: Before proceeding to Phase 1, ALL items below MUST be checked:

- [ ] Functionality analysis complete (user flow, admin flow if applicable, system flow, integration flow if applicable documented)
- [ ] Plan/requirements understood (if available) OR documented as missing
- [ ] Code scope understood (what code is being validated)
- [ ] Functionality mapped from plan/code/tests (clear understanding of what should be validated)
- [ ] Template format followed (all required sections completed)
- [ ] Functionality clear and understood (no ambiguous requirements)

**CRITICAL**: Do NOT proceed to Phase 1 until ALL items above are checked. If any item is incomplete:

- Ask user: "Functionality unclear. Please clarify: What functionality is being validated? What are the user flows? What should the plan/code/tests cover?"
- Do NOT proceed until functionality is understood and all gate check items are complete

**Display Success Message** (after Phase 0 completion):

```
✅ Phase 0 Complete: Functionality Analysis

Analyzed:
- Flows: [X] flows identified
- Acceptance criteria: [Y] criteria defined
- Plan/requirements: ✅ Reviewed (if available)

Next: Proceeding to Phase 1 - Intake
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

- **Store Validation Patterns**: After workflow completes, save successful validation patterns to `.claude/memory/patterns.json` (only if validated effective)
- **Query Similar Validations**: Check `.claude/memory/patterns.json` for similar validation patterns (use semantic match, top 3 only)

## Phase 1 - Intake

**Memory Integration** (optimized):

- **Load Preferences**: Query `.claude/memory/preferences.json` for validation preferences (if exists)
- **Load Patterns Once**: Read `.claude/memory/patterns.json` ONCE, cache for workflow duration

1. Confirm the artefacts to compare (plan, code, tests, docs).
2. **Missing Plan Handling**:
   - If plan is missing:
     - Options: Run planning workflow first / Use code-only validation / User provides plan manually
     - Ask user: "Plan not found. Run planning workflow first, validate code-only, or provide plan manually?"
     - Wait for user decision (with 5-minute timeout per orchestrator error recovery)
   - If plan exists but unclear: Ask user to clarify plan location or format
3. **Scope Validation**: Confirm code scope is clear and accessible
   - If scope ambiguous: Ask user to specify directories/files/patterns

**Display Success Message** (after Phase 1 completion):

```
✅ Phase 1 Complete: Input Validation

Validated:
- Files: [X] files validated
- Scope: ✅ Confirmed
- Plan: ✅ Found / ⚠️ Missing (if applicable)

Next: Proceeding to Phase 2 - Plan vs Code
```

## Phase 2 - Plan vs Code

**Required Skills**:

- `project-context-understanding` - **MANDATORY** (understand project structure, dependencies, and conventions before validating)
- `requirements-analysis`
- `test-driven-development` - **MANDATORY** (test coverage analysis and validation)
- `verification-before-completion`
- `memory-tool-integration` (filesystem-based memory always available)

**Conditional Skills**:

- `code-quality-patterns` - Load if code quality validation needed (keywords: quality, maintainability, complexity, SOLID)

**Detection Logic**:

- Code Quality Validation: Keywords "quality", "maintainability", "complexity", "SOLID"

**Skill Loading Strategy**:

- All required skills are independent (no dependencies between them)
- **Load all required skills in parallel** for faster initialization
- **Load conditional skills** (`code-quality-patterns`) based on detection logic, still in parallel with required skills

**Skill Loading Verification Protocol**:

- Verify each skill loads successfully (read first 100 chars, parse YAML, check content)
- If loading fails, use Error Recovery Protocol (see orchestrator)

1. Extract requirements/user stories from the plan.
2. For each requirement, locate corresponding code and note file/line references.
3. **Drift Classification** (CRITICAL):
   - **Drift Taxonomy**:
     - **Intentional Drift**: Code differs from plan but documented in plan (e.g., "Planned X, implemented Y due to constraint")
       - Classification: Documented change with rationale
       - Action: Accept if rationale valid, flag if rationale missing
     - **Accidental Drift**: Code differs from plan without documentation
       - Classification: Unexpected deviation
       - Action: Flag for review, ask user if intentional
     - **Missing Implementation**: Planned but not implemented
       - Classification: Incomplete implementation
       - Action: Flag as gap, ask user if deferred or missed
     - **Extra Implementation**: Implemented but not planned
       - Classification: Scope creep
       - Action: Flag for review, ask user if intentional addition
   - **Drift Recording Format**:
     ```
     Drift: {requirement/user_story}
     Type: {Intentional/Accidental/Missing/Extra}
     Plan: {what was planned}
     Actual: {what was implemented}
     Location: {file:line if applicable}
     Rationale: {if documented}
     Action: {what needs to happen}
     ```
   - **Drift Threshold**: If >5 accidental drifts → Flag as "Significant drift detected"
4. **Alignment Matrix**: Create requirement → code mapping:
   ```
   | Requirement | Code Location | Status | Drift Type |
   |-------------|---------------|--------|------------|
   | User Story 1 | src/auth.ts:42 | Implemented | None |
   | User Story 2 | src/payment.ts:100 | Partial | Missing implementation |
   | User Story 3 | N/A | Missing | Missing |
   ```

**Display Success Message** (after Phase 2 completion):

```
✅ Phase 2 Complete: Plan vs Code

Compared:
- Requirements: [X] requirements checked
- Drift detected: [Y] drifts (if any)
- Alignment: ✅ Verified

Next: Proceeding to Phase 3 - Code vs Tests
```

**Validate Workflow Inventory Validation** (MANDATORY after Phase 2):

- [ ] No subagents documented (direct analysis only)
- [ ] Documented as "No subagents - direct analysis"
- [ ] All validation phases completed

**If subagents listed**: STOP and remove (validate workflow has no subagents).

## Phase 3 - Code vs Tests

**Required Skills**:

- `test-driven-development`
- `verification-before-completion`

1. Map implementation files to test suites.
2. Run the relevant test command and capture output (with exit code).
3. **Coverage Thresholds** (per component type):
   - **Unit Tests**: Target 80% coverage (threshold: 70% minimum)
     - If < 70%: Flag as "Coverage below threshold"
     - If 70-80%: Note as "Coverage acceptable but below target"
     - If >= 80%: Mark as "Coverage meets target"
   - **Integration Tests**: Target 60% coverage (threshold: 50% minimum)
     - If < 50%: Flag as "Integration coverage below threshold"
     - If 50-60%: Note as "Integration coverage acceptable but below target"
     - If >= 60%: Mark as "Integration coverage meets target"
   - **E2E Tests**: Target critical flows only (no percentage threshold)
     - Verify: All critical user flows covered
     - Missing flows: Flag as "Critical E2E test missing"
4. **Coverage Gap Analysis**:
   - Extract coverage report: `npm run coverage` or equivalent
   - Identify files/modules with coverage below threshold
   - Classify gaps:
     - **Critical Gaps**: Core business logic, security-critical code, payment flows
     - **Important Gaps**: Utility functions, helper methods
     - **Acceptable Gaps**: Config files, type definitions (if no logic)
   - Report: "Coverage gaps: {list} - {classification}"
5. **Edge Case Coverage**:
   - Extract edge cases from plan or risk analysis
   - Verify each edge case has test:
     - Covered: Test exists and passes
     - Missing: Edge case identified but no test
     - Failed: Test exists but fails
   - Report: "Edge case coverage: {N} covered, {M} missing, {K} failed"

Invocation pattern:

- Read `requirements-analysis` and the plan to anchor checks.
- Run only the necessary commands; capture command and exit code.
- If a step fails or is unclear, stop and ask for direction.

**Validation Gate** (before proceeding to Phase 4):

**CRITICAL**: Execute this bash command to verify validation is complete:

```bash
# Verify validation outputs exist
VALIDATION_OUTPUTS=("validation-report.md" "test-results.json")  # Adjust based on actual outputs
MISSING_OUTPUTS=()

for output in "${VALIDATION_OUTPUTS[@]}"; do
    if [ ! -f "$output" ]; then
        MISSING_OUTPUTS+=("$output")
    fi
done

if [ ${#MISSING_OUTPUTS[@]} -gt 0 ]; then
    echo "Error: Missing validation outputs: ${MISSING_OUTPUTS[*]}"
    exit 1
else
    echo "✓ All validation outputs created"
fi

# Verify validation passed (check exit codes from validation commands)
if [ -f "test-results.json" ]; then
    if grep -q "\"passed\": false" "test-results.json"; then
        echo "Error: Validation tests failed"
        exit 1
    else
        echo "✓ All validation tests passed"
    fi
fi
```

**CRITICAL**: Do NOT proceed to Phase 4 until bash command exits with code 0.

**Display Success Message** (after Phase 3 completion):

```
✅ Phase 3 Complete: Code vs Tests

Verified:
- Test coverage: [X]% coverage
- Tests passing: ✅ Yes
- Coverage gaps: [Y] gaps identified (if any)

Next: Proceeding to Phase 4 - Code vs Documentation
```

## Phase 4 - Code vs Documentation

**Documentation Freshness Verification Method**:

1. **Extract Code Contracts**:
   - API endpoints: Extract from route definitions → `GET /api/users`, `POST /api/users`
   - Function signatures: Extract from source code → `function authenticateUser(email, password)`
   - Data models: Extract from type definitions → `interface User { id, email, name }`
   - Configuration: Extract from config files → `{ port: 3000, db: "mongodb://..." }`
2. **Compare with Documentation**:
   - **API Documentation**: Extract endpoints from docs (OpenAPI/Swagger, README.md)
     - Compare: Code endpoints vs Doc endpoints
     - Flag: Missing endpoints in docs, extra endpoints in docs, parameter mismatches
   - **Function Documentation**: Extract function docs (JSDoc, README)
     - Compare: Code signatures vs Doc signatures
     - Flag: Missing functions in docs, outdated signatures, missing parameters
   - **Data Model Documentation**: Extract models from docs
     - Compare: Code models vs Doc models
     - Flag: Missing fields, extra fields, type mismatches
3. **Freshness Scoring**:
   - **Fresh** (matches code): Documentation accurate
   - **Stale** (partially matches): Documentation outdated (list differences)
   - **Missing** (no docs): Documentation missing
   - **Incorrect** (conflicts with code): Documentation incorrect (cite conflicts)
4. **Cite Missing/Outdated Sections**:
   - Format: `{file}:{line_start}-{line_end}` or `{file}:{section}` → Issue: {description}
   - Example: `README.md:API-Endpoints` → Issue: Missing endpoint `DELETE /api/users/:id`
   - Include suggested fixes in recommendations

**Display Success Message** (after Phase 4 completion):

```
✅ Phase 4 Complete: Code vs Documentation

Verified:
- Documentation freshness: ✅ Checked
- Missing docs: [X] items (if any)
- Outdated docs: [Y] items (if any)

Next: Proceeding to Phase 5 - Verification Summary
```

## Phase 5 - Verification Summary

**MANDATORY**: Use exact template:

```
## Verification Summary
Plan: <path>
Code scope: <files/modules>
Requirements checked: <N> requirements/user stories
Drift detected: <N> intentional, <M> accidental, <K> missing, <L> extra
Tests run: <command> -> exit <code>
Coverage: <percentage>% lines (<statements>% statements, <branches>% branches)
  - Unit tests: <coverage>% (threshold: 70%, target: 80%)
  - Integration tests: <coverage>% (threshold: 50%, target: 60%)
  - E2E tests: <N> critical flows covered
Coverage gaps: <list of files/modules below threshold>
Edge cases: <N> covered, <M> missing, <K> failed
Documentation reviewed: <paths>
Documentation freshness: <N> fresh, <M> stale, <K> missing, <L> incorrect
Outstanding issues: <list items requiring attention>
```

**Example**:

```
## Verification Summary
Plan: docs/plan/checkout.md
Code scope: src/checkout/**, src/payments/**
Requirements checked: 12 user stories
Drift detected: 2 intentional, 1 accidental, 0 missing, 1 extra
Tests run: npm test -- tests/checkout.spec.ts -> exit 0
Coverage: 81% lines (84% statements, 69% branches)
  - Unit tests: 85% (threshold: 70%, target: 80%) - PASSED
  - Integration tests: 72% (threshold: 50%, target: 60%) - PASSED
  - E2E tests: 3 critical flows covered - PASSED
Coverage gaps: src/utils/helpers.ts (45% - below threshold)
Edge cases: 8 covered, 2 missing, 0 failed
Documentation reviewed: README.md, docs/api/payments.md
Documentation freshness: 10 fresh, 2 stale, 1 missing, 0 incorrect
Outstanding issues: Missing E2E test for checkout cancellation flow, outdated API docs for DELETE endpoint
```

**Display Success Message** (after Phase 5 completion):

```
✅ Phase 5 Complete: Validation Complete

Validated:
- Requirements: [X] requirements checked
- Tests: ✅ Coverage verified
- Documentation: ✅ Reviewed
- Validation report: ✅ Generated

Next: Validation workflow complete - Report ready
```

## Phase 6 - Report

## Quick Reference

**Phase Summary**:

- **Phase 0**: Functionality Analysis (MANDATORY FIRST) - Understand validation requirements, map functionality from plan/code/tests
- **Phase 1**: Intake - Load plan/requirements and code scope
- **Phase 2**: Plan vs Code - Compare plan vs code (functionality alignment, missing features, extra features)
- **Phase 3**: Code vs Tests - Compare code vs tests (test coverage, missing tests, untested code)
- **Phase 4**: Code vs Documentation - Compare code vs documentation (documentation accuracy, missing docs)
- **Phase 5**: Synthesis - Synthesize validation findings
- **Phase 6**: Report - Generate validation report with functionality verification FIRST

**Key Outputs**:

- Functionality analysis (user/admin/system flows from plan/code/tests)
- Plan vs Code alignment findings
- Code vs Tests coverage findings
- Code vs Documentation accuracy findings
- Validation report with evidence

**Validation Requirements**:

- [ ] Phase 0 complete (functionality analysis done, gate checks passed)
- [ ] Plan/requirements loaded successfully
- [ ] Code scope identified
- [ ] All comparisons completed (plan vs code, code vs tests, code vs docs)
- [ ] All findings include file:line citations or specific references
- [ ] Evidence provided for all claims (file:line citations, test coverage, doc references)

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Validation Report

## Executive Summary

[2-3 sentences summarizing alignment status, key drifts, coverage status, and overall validation outcome]

## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented]
- Skills loaded: requirements-analysis, verification-before-completion, test-driven-development
- Plan reviewed: <path>
- Code scope: <files/modules>
- Tests run: <commands with exit codes>
- Documentation reviewed: <paths>
- Tools used: [Read, Grep, Glob, Bash]

## Functionality Analysis

[Include complete functionality analysis from Phase 0]

## Findings / Decisions

### Alignment Matrix

| Requirement/User Story | Code Location      | Test Coverage                      | Documentation | Status  | Drift Type             |
| ---------------------- | ------------------ | ---------------------------------- | ------------- | ------- | ---------------------- |
| Story 1                | src/auth.ts:42     | Covered (test: auth.spec.ts:10)    | Documented    | Aligned | None                   |
| Story 2                | src/payment.ts:100 | Partial (test: payment.spec.ts:20) | Documented    | Partial | Missing implementation |
| Story 3                | N/A                | Missing                            | Missing       | Missing | Missing                |

### Drift Analysis

- **Intentional Drifts**: {N} documented changes with rationale
- **Accidental Drifts**: {M} unexpected deviations requiring review
- **Missing Implementation**: {K} planned but not implemented
- **Extra Implementation**: {L} implemented but not planned

### Coverage Analysis

- **Unit Test Coverage**: {percentage}% (threshold: 70%, target: 80%)
- **Integration Test Coverage**: {percentage}% (threshold: 50%, target: 60%)
- **E2E Test Coverage**: {N} critical flows covered
- **Coverage Gaps**: {list files/modules below threshold}
- **Edge Case Coverage**: {N} covered, {M} missing, {K} failed

### Documentation Freshness

- **Fresh** (matches code): {N} sections
- **Stale** (partially matches): {M} sections - {list}
- **Missing**: {K} sections - {list}
- **Incorrect** (conflicts): {L} sections - {list}

## Verification Summary

[Use exact template from Phase 4]

## Recommendations / Next Steps

[Prioritized: Critical drifts first, then coverage gaps, then documentation issues]

## Open Questions / Assumptions

[If any drifts need clarification, coverage threshold exceptions, or documentation decisions]
```

**Validation Before Presenting**:

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] Alignment matrix includes all requirements/user stories
- [ ] Drift analysis classifies all drifts
- [ ] Coverage analysis includes thresholds and gaps
- [ ] Documentation freshness verified with code contracts
- [ ] Verification Summary includes all commands with exit codes
- [ ] Recommendations prioritized

## Failure Handling

- If plan files are missing or unreadable, stop and ask the user for direction.
- Do not fabricate coverage numbers or documentation status; cite actual evidence or mark as "not checked".

## References

- Skill structure: `docs/reference/04-SKILLS.md`
