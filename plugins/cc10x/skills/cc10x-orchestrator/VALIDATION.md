# Orchestrator Validation and Reporting

Validation checklists, evidence requirements, and final report formatting.

## Evidence-First Expectations

- Reviews must cite file paths and line numbers.
- Planning, build, and debug workflows must run the relevant verification commands before claiming completion.
- For every success statement, include a short "Verification Summary" that lists commands run, exit codes, and artefacts.

## Final Report - Output Format (REQUIRED)

**MANDATORY TEMPLATE** - All workflows must use this exact structure:

```markdown
# [Workflow Name] Report

## Executive Summary

[2-3 sentences summarizing outcome, key findings, and overall status]

## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented]
  [Bullet list of key steps, tools used, subagents invoked, skills loaded]

## Functionality Analysis

[Include complete functionality analysis from Phase 0 - user flows, admin flows, system flows, functional verification]

## Findings / Decisions

[Workflow-specific sections with file:line citations where applicable]

## Verification Summary

Scope: <files/modules>
Criteria: <list of what was verified - functionality FIRST, then other checks>
Commands:

- <command> -> exit <code>
- <command> -> exit <code>
  Evidence:
- <log/report snippet>
- <test output snippet>
  Risks / Follow-ups: <items still pending or needing attention>

## Recommendations / Next Steps

[Prioritized list of actionable next steps - functionality issues FIRST, then other concerns]

## Open Questions / Assumptions

[If any - list questions requiring user input or assumptions made]
```

**Pre-Final-Report Validation** (MANDATORY before presenting final report):

**CRITICAL**: This validation prevents incomplete reports. Execute BEFORE presenting final report.

1. **Phase Completion Audit**:
   - [ ] Phase 0 completed (functionality analysis)
   - [ ] All workflow phases completed (check workflow-specific phase list)
   - [ ] All phase success messages displayed
   - [ ] All gate checks passed
   - [ ] All phase completion checklists verified

2. **Skills Audit**:
   - [ ] Skills Inventory Check completed (see Phase 2)
   - [ ] ALL required skills from workflow Phase 2 loaded and documented in Actions Taken
   - [ ] ALL conditional skills loaded IF detection logic matched and documented
   - [ ] Each skill documented in Actions Taken with load status
   - [ ] No required skill missing
   - [ ] No conditional skill missing IF detection logic matched

3. **Subagents Audit**:
   - [ ] Subagents Inventory Check completed (see Phase 3)
   - [ ] ALL subagents that should be invoked are documented in Actions Taken
   - [ ] Execution mode documented (parallel/sequential)
   - [ ] Skip decisions documented with reasons (if any skipped)
   - [ ] Output validation documented for each subagent
   - [ ] No required subagent missing
   - [ ] No subagent listed that shouldn't have been invoked

4. **Evidence Audit**:
   - [ ] Functionality verification documented FIRST in Verification Summary
   - [ ] All findings have file:line citations
   - [ ] All commands have exit codes
   - [ ] Verification summary complete
   - [ ] No placeholder text ("TODO", "TBD", "FIXME") in critical sections

5. **Actions Taken Audit**:
   - [ ] Phase 0: Functionality Analysis documented
   - [ ] Phase 1: Input Validation/Complexity Gate documented
   - [ ] Phase 2: Skills loaded documented (ALL required + conditional IF detected)
   - [ ] Phase 3: Subagents invoked documented (ALL that should be invoked)
   - [ ] Phase 4+: Workflow-specific phases documented
   - [ ] Execution mode documented (parallel/sequential)
   - [ ] Skip decisions documented (if any)
   - [ ] Phase completion messages documented

6. **Workflow-Specific Audit**:

   **Review Workflow**:
   - [ ] code-reviewer documented
   - [ ] integration-verifier documented IF integration changes detected

   **Plan Workflow**:
   - [ ] planner documented

   **Build Workflow**:
   - [ ] component-builder documented for each component
   - [ ] code-reviewer documented for each component (unless skipped)
   - [ ] integration-verifier documented for each component (unless skipped)
   - [ ] Sequential execution per component documented
   - [ ] Parallel execution between components documented (if independent)

   **Debug Workflow**:
   - [ ] bug-investigator documented for each bug
   - [ ] code-reviewer documented for each bug (unless skipped)
   - [ ] integration-verifier documented for each bug (unless skipped)
   - [ ] Sequential execution per bug documented
   - [ ] Parallel execution between bugs documented (if independent)

   **Validate Workflow**:
   - [ ] No subagents documented (direct analysis only)

**If ANY audit fails**:

- STOP final report generation
- Report: "CRITICAL: Pre-final-report validation failed. Missing: {list missing items}"
- Complete missing items
- Re-run all audits
- Do NOT present final report until ALL audits pass

**CRITICAL**: This validation is non-negotiable. Final report generation aborts if any audit fails.

**Validation**: Before presenting final report, verify:

**Actions Taken Validation** (CRITICAL - before final report):

**CRITICAL**: This validation ensures Actions Taken section is complete and accurate.

**Required Structure**:

```markdown
## Actions Taken

- Functionality analysis completed: [user flow, admin flow, system flow documented]
- Phase 0: Functionality Analysis ✅ Complete
- Phase 1: [Phase name] ✅ Complete
- Phase 2: Skills Loaded ✅ Complete
  - Required skills loaded: [list ALL required skills with status]
  - Conditional skills loaded: [list conditional skills IF detected with status]
- Phase 3: Subagents Invoked ✅ Complete
  - Subagents invoked: [list ALL subagents that should be invoked with status]
  - Execution mode: [parallel/sequential for each group]
  - Skip decisions: [list any skipped subagents with reasons]
- Phase 4+: [Workflow-specific phases] ✅ Complete
- Tools used: [list tools used]
- Commands run: [list key commands with exit codes]
```

**Validation Checklist**:

- [ ] Phase 0: Functionality Analysis documented
- [ ] ALL required skills listed (check against workflow Phase 2 required skills list)
- [ ] ALL conditional skills listed IF detected (check against detection logic)
- [ ] ALL subagents invoked listed (check against workflow Phase 3 subagent list)
- [ ] Skip decisions documented (if any subagents/skills skipped, reason documented)
- [ ] Execution mode documented (parallel/sequential for each subagent group)
- [ ] Phase completion messages documented (all phases completed)
- [ ] Verification summary includes functionality verification FIRST
- [ ] No required skill missing
- [ ] No required subagent missing (unless skip condition met)
- [ ] No phase missing

**If ANY item missing**:

- Do NOT proceed to final report
- Complete missing items first
- Re-run validation
- Do NOT present final report until ALL items validated

- [ ] Functionality analysis complete (from Phase 0)
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes functionality verification FIRST, then other checks
- [ ] File:line citations provided for all findings
- [ ] Recommendations are prioritized (functionality issues first)
- [ ] All subagents/skills used are documented in Actions Taken

## Validation Checklist

**CRITICAL**: Before proceeding to the next phase, ALL items below MUST be checked. In Strict Mode, workflow aborts if any validation fails.

**Mandatory Validation Steps** (before proceeding):

- [ ] Phase 0 complete and verified (functionality analysis complete, all gate checks passed)
- [ ] Phase 5.5 complete (session summary created, file exists, Actions Taken updated)
- [ ] Skills loaded successfully (all required skills loaded, conditional skills loaded if detected)
- [ ] Subagents invoked correctly (existence verified, skip conditions checked, dependencies analyzed, execution mode determined)
- [ ] Outputs validated (format matches expected template, all required fields present, file:line citations provided)
- [ ] Evidence provided for all claims (file:line citations for code references, exit codes for commands, logs/artifacts for verification)

**Strict Mode** (optional, recommended for production):

**Strict Mode Enforcement** (default for production):

**CRITICAL**: Strict Mode is enabled by default. Workflow aborts if any validation fails.

**Enforcement Points**:

1. **Phase 0 Enforcement**:
   - Workflow aborts if Phase 0 not completed FIRST
   - Workflow aborts if functionality analysis incomplete
   - Workflow aborts if gate check fails

2. **Skills Loading Enforcement**:
   - Workflow aborts if Actions Taken section missing required skills
   - Workflow aborts if any required skill not loaded (unless user explicitly skipped)
   - Workflow aborts if conditional skill should be loaded but missing (detection logic matched)
   - Skills Inventory Check must pass before proceeding

3. **Subagents Invocation Enforcement**:
   - Workflow aborts if Actions Taken section missing required subagents
   - Workflow aborts if any required subagent not invoked (unless skip condition met)
   - Workflow aborts if subagent output invalid (format mismatch, missing fields)
   - Subagents Inventory Check must pass before proceeding

4. **Evidence Enforcement**:
   - Workflow aborts if findings lack file:line citations
   - Workflow aborts if commands lack exit codes
   - Workflow aborts if verification summary incomplete
   - Workflow aborts if placeholder text in critical sections

5. **Phase 5.5 Enforcement**:
   - Workflow aborts if Phase 5.5 not completed before Phase 6
   - Workflow aborts if session summary file missing or empty
   - Workflow aborts if session summary missing required sections
   - Phase 5.5 Completion Checklist must pass before proceeding

6. **Actions Taken Enforcement**:
   - Workflow aborts if Actions Taken section missing
   - Workflow aborts if any phase not documented
   - Workflow aborts if execution mode not documented
   - Workflow aborts if skip decisions not documented (if any skipped)

**Disabling Strict Mode** (not recommended):

- User can disable Strict Mode by setting `STRICT_MODE=false` in environment or context
- Disabling Strict Mode allows workflow to continue with warnings instead of aborting
- Warnings are still logged and reported, but workflow continues
- **Recommendation**: Keep Strict Mode enabled for production workflows
