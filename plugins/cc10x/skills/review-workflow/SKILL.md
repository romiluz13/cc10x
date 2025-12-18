---
name: review-workflow
description: Evidence-based code review workflow. Use when reviewing PRs, auditing code, or checking changes. Focuses on security, quality, performance, and accessibility issues.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Review Workflow - Functionality First

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**CRITICAL**: Before reviewing code, understand functionality. Before claiming completion, verify with fresh evidence.

## Functionality First Mandate

**BEFORE reviewing code, understand functionality**:

1. **What functionality is being reviewed?**
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?

2. **THEN review** - Review code for issues affecting that functionality

3. **Use subagents** - Apply review subagents AFTER functionality is understood

---

Orchestrates multi-dimensional code analysis with functionality-first approach.

## Quick Start

Review code by first understanding functionality, then checking for issues affecting it.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Load domain skills**: code-review-patterns (consolidates security-patterns, code-quality-patterns, performance-patterns), frontend-patterns (consolidates ux-patterns, ui-design, accessibility-patterns)
3. **Run subagents**: code-reviewer subagent checks for issues affecting functionality
4. **Compile report**: Evidence-backed findings with file:line citations
5. **Verify**: Fresh evidence collected, functionality verified

**Result:** Comprehensive review focused on functionality-affecting issues.

## Requirements

**Dependencies:**

- `cc10x-orchestrator` - Must be activated through orchestrator (do not use directly)
- Domain skills (code-review-patterns, frontend-patterns) - Loaded based on review scope
- Analysis subagents - code-reviewer subagent (consolidates all review dimensions)

**Prerequisites:**

- Phase 0 (Functionality Analysis) completed via orchestrator
- Functionality flows understood (user flow, admin flow, system flow)

**Tool Access:**

- Required tools: Read, Grep, Glob, Task, Bash
- Task tool: Used to invoke analysis subagents

**Review Scope:**

- Security - Checks security issues affecting functionality
- Code Quality - Checks quality issues affecting maintainability
- Performance - Checks performance issues affecting functionality
- Accessibility - Checks accessibility issues blocking functionality

## Process

For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/review.md`.

## Quick Reference

**Decision Tree**:

```
REVIEW NEEDED?
│
├─ Understand Functionality First
│  ├─ User/Admin/System flows identified? → Continue
│  └─ Not identified? → STOP, complete functionality analysis first
│
├─ Load Domain Skills
│  ├─ Skills loaded? → Continue
│  └─ Not loaded? → Load risk, security, performance, quality, UX, a11y skills
│
├─ Run Analysis Subagents
│  ├─ Subagents run sequentially? → Continue
│  └─ Parallel execution? → STOP, run sequentially
│
└─ Compile Report
   ├─ Evidence-backed findings? → Complete
   └─ Missing evidence? → STOP, gather evidence first
```

- Loads: risk, security, performance, quality, UX, a11y skills
- Runs: analysis subagents sequentially (no parallelism)
- Outputs: severity-ranked findings with file:line evidence and a Verification Summary

## Output Format (REQUIRED)

**MANDATORY TEMPLATE** - Use exact structure from orchestrator:

```markdown
# Review Report

## Executive Summary

[2-3 sentences summarizing total issues by severity, go/no-go recommendation, and overall code health status]

## Actions Taken

- Skills loaded: [list]
- Subagents invoked: [list]
- Files reviewed: [list]
- Tools used: [list]

## Findings / Decisions

### Security Findings

- **CRITICAL**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **HIGH**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **MEDIUM**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]
- **LOW**: [Issue] at [file:line] – [Impact] – [Fix] – [Evidence]

### Performance Findings

[Same format as Security]

### Code Quality Findings

[Same format as Security]

### UX Findings

[Same format as Security]

### Accessibility Findings

[Same format as Security]

## Verification Summary

Scope: <files reviewed>
Criteria: <list of what was verified>
Commands:

- <command> -> exit <code>
  Evidence:
- <cited file:line references>
- <tool output snippets if any>
  Outstanding Questions: <if clarification needed>

## Recommendations / Next Steps

[Prioritized: CRITICAL → HIGH → MEDIUM → LOW]

## Open Questions / Assumptions

[If any conflicts detected or clarification needed]
```

## Troubleshooting

**Common Issues:**

1. **Functionality not understood before review**
   - **Symptom**: Reviewing code without understanding what it should do
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, then review
   - **Prevention**: Always understand functionality before reviewing

2. **Missing evidence or file:line citations**
   - **Symptom**: Findings without evidence or citations
   - **Cause**: Didn't capture evidence during review
   - **Fix**: Review again, capture evidence and citations
   - **Prevention**: Always include file:line citations and evidence

3. **Generic issues instead of functionality-focused**
   - **Symptom**: Finding generic code quality issues, not functionality-affecting
   - **Cause**: Didn't focus on functionality-affecting issues
   - **Fix**: Refocus review on issues affecting functionality flows
   - **Prevention**: Always prioritize functionality-affecting issues

**If issues persist:**

- Verify functionality analysis was completed first
- Check that evidence was captured with file:line citations
- Ensure review focuses on functionality-affecting issues
- Review workflow instructions in `workflows/review.md`

**Validation Checklist**:

- [ ] Executive Summary present (2-3 sentences)
- [ ] All findings include file:line citations
- [ ] Verification Summary includes commands with exit codes
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken
