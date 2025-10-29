---
name: test-driven-development
description: Enforces the RED -> GREEN -> REFACTOR loop with mandatory command execution and verification. Use for any implementation or bug fix work before writing production code.
allowed-tools: Read, Grep, Glob, Bash
---

# Test-Driven Development (TDD)

## Core Rule
```
No production code without a failing test first.
If code exists before the test, delete it and start from the test.
```

## Quick Checklist
- Write one failing test that demonstrates the desired behaviour.
- Run the test and capture the failure output.
- Write the smallest amount of code to make the test pass.
- Run the full suite (or focused set) and capture success output.
- Refactor while keeping tests green.
- Record a short verification summary with commands and exit codes.

## Working Process
1. **RED - Write Failing Test**
   - Describe the scenario in the test name.
   - Keep the test focused on one behaviour.
   - Run `npm test <target>` (or equivalent) and paste the failing snippet.
2. **GREEN - Minimal Implementation**
   - Implement only what is required for the test.
   - Re-run the same command plus any impacted suites; ensure exit code is 0.
3. **REFACTOR - Clean Up**
   - Remove duplication, rename for clarity, extract helpers.
   - Re-run tests after each refactor step.

## Verification Summary Template
```
# Verification Summary
Tests: <command> -> exit 0
New tests: <list>
Notes: <coverage or follow-up if applicable>
```
Include this block whenever reporting completion.

## Anti-Patterns to Avoid
- Skipping the failing test step or assuming it would fail.
- Adding multiple behaviours in one test.
- Writing large implementations before running tests.
- Claiming success without captured command output.

## References
- Official skills guidance: `docs/reference/04-SKILLS.md`
