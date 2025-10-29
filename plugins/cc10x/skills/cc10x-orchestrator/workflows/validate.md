# VALIDATION Workflow - Cross-Artifact Consistency

**Triggered by:** User wants to confirm the implementation matches an existing plan, tests, or documentation set.

## Prerequisites
- Plan or requirements source identified (e.g., `.claude/plans/<feature>.md` or user-specified document).
- Scope of code to check (directories, modules, PR diff).

## Phase 0 - Intake
1. Confirm the artefacts to compare (plan, code, tests, docs).
2. If the plan is missing, offer to run the planning workflow first.

## Phase 1 - Plan vs Code
1. Load `requirements-analysis` and `verification-before-completion` skills.
2. Extract requirements/user stories from the plan.
3. For each requirement, locate corresponding code and note file/line references.
4. Record any drift (planned but not implemented, implemented but not planned).

## Phase 2 - Code vs Tests
1. Map implementation files to test suites.
2. Run the relevant test command and capture output.
3. If coverage data exists, capture the summary and highlight gaps.
4. List edge cases from the plan or risk analysis and verify they are covered.

Invocation pattern:
- Read `requirements-analysis` and the plan to anchor checks.
- Run only the necessary commands; capture command and exit code.
- If a step fails or is unclear, stop and ask for direction.

## Phase 3 - Code vs Documentation
1. Confirm READMEs/API docs/tutorials reflect the current behaviour.
2. Cite missing or outdated sections with file paths and suggested fixes.

## Phase 4 - Verification Summary
Document commands and artefacts reviewed:
```
# Verification Summary
Plan: <path>
Code scope: <files>
Tests run: <command + exit code>
Coverage: <if available>
Documentation reviewed: <paths>
```

Example:
Plan: docs/plan/checkout.md
Code scope: src/checkout/**, src/payments/**
Tests run: npm test -- tests/checkout.spec.ts -> exit 0
Coverage: 81% lines (statements 84%, branches 69%)
Documentation reviewed: README.md, docs/api/payments.md

## Phase 5 - Report
Provide a concise report:
- Alignment matrix (plan requirement -> code -> test -> docs).
- Missing items or inconsistencies.
- Recommendations for remediation.
- Optional follow-up offers (e.g., "Need help updating docs?").

## Failure Handling
- If plan files are missing or unreadable, stop and ask the user for direction.
- Do not fabricate coverage numbers or documentation status; cite actual evidence or mark as "not checked".

## References
- Skill structure: `docs/reference/04-SKILLS.md`
