---
name: review-workflow
description: MUST be activated through cc10x-orchestrator - do not use directly. Orchestrator coordinates this review workflow with functionality-first approach. First understands functionality (user flow, admin flow, system flow), then reviews code for issues affecting that functionality. Focuses on finding real issues that affect functionality, not generic code review. Loads domain skills, runs bundled analysis subagents, and compiles an evidence-backed report. Use when orchestrator detects review intent.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Review Workflow - Functionality First

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

## Process

For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/review.md`.

## Quick Reference

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

**Validation Checklist**:

- [ ] Executive Summary present (2-3 sentences)
- [ ] All findings include file:line citations
- [ ] Verification Summary includes commands with exit codes
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken
