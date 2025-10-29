---
name: systematic-debugging
description: Four-phase debugging discipline that enforces LOG FIRST, hypothesis-driven fixes, and regression tests. Use whenever diagnosing bugs, test failures, or unexpected behaviour.
allowed-tools: Read, Grep, Glob, Bash
---

# Systematic Debugging

## Core Principle
```
No fixes without root-cause evidence.
If you have not logged or observed the failing state, you are guessing.
```

## Four Phases
1. **Investigate**
   - Reproduce the issue reliably.
   - Capture complete error messages, logs, request/response payloads.
   - Inspect recent changes (`git log`, `git diff`).
2. **Pattern Analysis**
   - Compare failing paths to working examples.
   - Consult the relevant skill guidance (security-patterns, integration-patterns, etc.).
3. **Hypothesis + Minimal Fix**
   - State the suspected root cause in one sentence.
   - Write a failing regression test that proves the bug.
   - Apply the smallest change to make the test pass.
4. **Verification**
   - Run the regression test and surrounding suite; capture outputs.
   - Summarise the fix, evidence, and follow-up monitoring.

## LOG FIRST Playbook
Whenever data shape or external behaviour is unclear:
- Log the full object/response with `JSON.stringify(value, null, 2)`.
- Record headers, cookies, environment variables (masking secrets).
- For HTTP issues, log method, URL, payload, status, and body.
- For auth, log session claims, roles, and config.

## Deliverable Template
```
## Root Cause
- <what failed and why>

## Evidence
- Logs: <snippet>
- Commands: <command> -> exit <code>

## Fix
- Summary of change.
- Regression test: <file/test name>.

## Verification Summary
- <tests run, exit codes, residual risks>
```

## Anti-Patterns
- Applying multiple fixes without proving the cause.
- Trusting documentation over runtime data.
- Reporting success without logs/tests.

## References
- Official debugging guidance: `docs/reference/03-SUBAGENTS.md`
- Verification requirements: `plugins/cc10x/skills/verification-before-completion/SKILL.md`
