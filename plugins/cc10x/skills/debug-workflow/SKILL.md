---
name: debug-workflow
description: MUST be activated through cc10x-orchestrator - do not use directly. Orchestrator coordinates this debug workflow with functionality-first approach. First understands what functionality is broken (user flow, admin flow, system flow), then debugs bugs affecting that functionality. Focuses on bugs that affect functionality, not generic debugging. Loads investigation skills and delegates to bug-investigator, code-reviewer, and integration-verifier sequentially. Use when orchestrator detects debug intent.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Debug Workflow - Functionality First

## Functionality First Mandate

**BEFORE debugging bugs, understand functionality**:

1. **What functionality is broken?**
   - What are the user flows? (what should happen)
   - What are the admin flows? (what should happen)
   - What are the system flows? (what should happen)

2. **THEN debug** - Debug bugs affecting that functionality

3. **Use systematic approach** - Apply debugging process AFTER functionality is understood

---

Systematic debugging with evidence-first verification, functionality-first approach.

## Quick Start

Debug bugs by first understanding expected functionality, then investigating systematically.

**Example:**

1. **Understand expected functionality**: File upload should work (User Flow: select → upload → confirm)
2. **Reproduce bug**: Upload fails with error message
3. **Investigate**: bug-investigator → code-reviewer → integration-verifier (sequential)
4. **Find root cause**: Missing file validation
5. **Fix & verify**: Add validation, test passes, functionality works

**Result:** Bug fixed with systematic investigation, functionality restored.

## Requirements

**Dependencies:**

- `cc10x-orchestrator` - Must be activated through orchestrator (do not use directly)
- `debugging-patterns` - Required for systematic debugging approach (consolidates systematic-debugging, log-analysis-patterns, root-cause-analysis)
- Investigation skills - Loaded based on bug type

**Prerequisites:**

- Phase 0 (Functionality Analysis) completed via orchestrator
- Expected functionality understood (what should work)
- Bug reproducible and confirmed

**Tool Access:**

- Required tools: Read, Grep, Glob, Task, Bash
- Task tool: Used to invoke subagents (bug-investigator, code-reviewer, integration-verifier)

**Subagents:**

- bug-investigator - Investigates bugs systematically
- code-reviewer - Reviews code for issues
- integration-verifier - Verifies integration works

## Process

For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/debug.md`.

## Quick Reference

**Decision Tree**:

```
DEBUG NEEDED?
│
├─ Understand Functionality First
│  ├─ Expected flows identified? → Continue
│  └─ Not identified? → STOP, complete functionality analysis first
│
├─ Confirm Reproduction
│  ├─ Bug reproducible? → Continue
│  └─ Not reproducible? → STOP, gather more information
│
├─ Investigate (Sequential Loop)
│  ├─ bug-investigator → code-reviewer → integration-verifier
│  ├─ Root cause found? → Continue to Fix
│  └─ Not found? → Continue investigation loop
│
├─ Fix & Test
│  ├─ Fix applied? → Write regression test
│  ├─ Test passes (GREEN)? → Continue
│  └─ Test fails (RED)? → Return to investigation
│
└─ Verify
   ├─ Functionality works? → Complete
   └─ Functionality broken? → Return to investigation
```

- Intake: confirm repro, errors/logs, recent changes
- Loop: bug-investigator -> code-reviewer -> integration-verifier (sequential)
- Evidence: logs + failing test -> fix -> GREEN; include Verification Summary

## Output Format (REQUIRED)

**MANDATORY TEMPLATE** - Use exact structure from orchestrator:

```markdown
# Debug Report

## Executive Summary

[2-3 sentences summarizing root cause, fix status, and overall resolution]

## Actions Taken

- Skills loaded: [list]
- Subagents invoked: [list]
- Bugs investigated: [list]
- Tools used: [list]

## Findings / Decisions

### Bug {name}

- **Root Cause**: [what failed and why]
- **Evidence**: [log excerpts, stack traces, code paths]
- **Fix**: [what changed, file:line]
- **Regression Test**: [test name, file:line]
- **Verification**: [command outputs showing RED → GREEN]

### Reproduction

- Steps: [detailed reproduction steps]
- Environment: [OS, dependencies, config]
- Error Messages: [full error messages]
- Logs: [relevant log snippets]

### Investigation Timeline

- [Hypothesis 1]: [result]
- [Hypothesis 2]: [result]
- [Root Cause Found]: [explanation]

### Fix & Regression Test

- Changes: [file:line diffs summary]
- Tests Added: [list]
- GREEN Proof: [command outputs]

### Reviews & Integration

- code-reviewer findings: [resolved/open]
- integration-verifier scenarios: [pass/fail with logs]

## Verification Summary

Scope: <bugs investigated>
Bugs fixed: <list>
Criteria: <what was verified>
Commands:

- <command> -> exit <code>
  Evidence:
- <log snippets showing bug>
- <test output showing RED then GREEN>
- <integration test results>
  Residual risk: <items to monitor, edge cases not covered>

## Recommendations / Next Steps

[Prioritized: Monitoring setup, additional tests, prevention measures]

## Troubleshooting

**Common Issues:**

1. **Expected functionality not understood**
   - **Symptom**: Debugging without knowing what should work
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, understand expected flows
   - **Prevention**: Always understand expected functionality before debugging

2. **Bug not reproducible**
   - **Symptom**: Can't reproduce the bug
   - **Cause**: Didn't gather enough information
   - **Fix**: Gather more information, check logs, ask user for details
   - **Prevention**: Always confirm bug is reproducible before investigating

3. **Root cause not found**
   - **Symptom**: Fixes symptoms but bug returns
   - **Cause**: Didn't complete root cause investigation
   - **Fix**: Use debugging-patterns skill, complete investigation
   - **Prevention**: Always find root cause before fixing

**If issues persist:**

- Verify expected functionality was understood first
- Check that bug is reproducible
- Ensure root cause investigation was completed
- Review workflow instructions in `workflows/debug.md`

## Open Questions / Assumptions

[If escalation needed, external dependencies unavailable, or assumptions made]
```

**Validation Checklist**:

- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes commands with exit codes
- [ ] Root cause clearly explained with evidence
- [ ] Regression test documented with RED → GREEN proof
- [ ] Reviews and integration status documented
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken
