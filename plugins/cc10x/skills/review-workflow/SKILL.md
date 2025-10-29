---
name: review-workflow
description: Coordinates the review workflow: loads domain skills, runs bundled analysis subagents, and compiles an evidence-backed report. Use when reviewing code quality, analyzing security vulnerabilities, assessing performance, auditing codebases, or conducting comprehensive code reviews.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Review Workflow

Orchestrates multi-dimensional code analysis.

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
