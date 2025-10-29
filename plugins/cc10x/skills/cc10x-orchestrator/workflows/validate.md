# VALIDATION Workflow - Cross-Artifact Consistency

**Triggered by:** User wants to confirm the implementation matches an existing plan, tests, or documentation set.

## Prerequisites
- Plan or requirements source identified (e.g., `.claude/plans/<feature>.md` or user-specified document).
- Scope of code to check (directories, modules, PR diff).

## Phase 0 - Intake

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

## Phase 1 - Plan vs Code

**Required Skills**:
- `requirements-analysis`
- `verification-before-completion`
- `memory-tool-integration` (filesystem-based memory always available)

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

## Phase 2 - Code vs Tests

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

## Phase 3 - Code vs Documentation

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

## Phase 4 - Verification Summary

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

## Phase 5 - Report

**MANDATORY OUTPUT FORMAT** - Use exact template from orchestrator:

```markdown
# Validation Report

## Executive Summary
[2-3 sentences summarizing alignment status, key drifts, coverage status, and overall validation outcome]

## Actions Taken
- Skills loaded: requirements-analysis, verification-before-completion, test-driven-development
- Plan reviewed: <path>
- Code scope: <files/modules>
- Tests run: <commands with exit codes>
- Documentation reviewed: <paths>
- Tools used: [Read, Grep, Glob, Bash]

## Findings / Decisions

### Alignment Matrix
| Requirement/User Story | Code Location | Test Coverage | Documentation | Status | Drift Type |
|------------------------|---------------|---------------|---------------|--------|------------|
| Story 1 | src/auth.ts:42 | Covered (test: auth.spec.ts:10) | Documented | Aligned | None |
| Story 2 | src/payment.ts:100 | Partial (test: payment.spec.ts:20) | Documented | Partial | Missing implementation |
| Story 3 | N/A | Missing | Missing | Missing | Missing |

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
