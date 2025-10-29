---
name: review-workflow
description: Coordinates the review workflow: loads domain skills, runs bundled analysis subagents, and compiles an evidence-backed report.
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
Return a consolidated review report:

1) Executive Summary (go/no-go guidance)
2) Findings by Category
   - Security (CRITICAL/HIGH/MEDIUM/LOW): [Issue] at [file:line] – [Impact] – [Fix]
   - Performance: …
   - Code Quality: …
   - UX: …
   - Accessibility: …
3) Verification Summary (commands → exit codes; artefacts if any)
4) Recommendations (prioritized)
5) Open Questions / Assumptions
