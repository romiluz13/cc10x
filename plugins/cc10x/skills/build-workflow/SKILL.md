---
name: build-workflow
description: Coordinates feature implementation via TDD, review, and integration verification. Loads shared skills and invokes component-builder, code-reviewer, and integration-verifier sequentially. Use when implementing new features, building components, or developing software following TDD practices.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Build Workflow

TDD-driven implementation with review and integration verification.

## Process
For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/build.md`.

## Quick Reference
- Gate: use orchestrator Complexity Rubric; confirm if score <=2
- Loop: RED -> GREEN -> REFACTOR; capture verification outputs
- Subagents: component-builder -> code-reviewer -> integration-verifier (sequential)

## Output Format (REQUIRED)

**MANDATORY TEMPLATE** - Use exact structure from orchestrator:

```markdown
# Build Report

## Executive Summary
[2-3 sentences summarizing components implemented, overall status, and key outcomes]

## Actions Taken
- Skills loaded: [list]
- Subagents invoked: [list]
- Components built: [list in order]
- Tools used: [list]

## Findings / Decisions

### Component Breakdown
For each component:
- **Component {name}**:
  - TDD Cycle: RED → GREEN → REFACTOR (commands and exit codes)
  - Key Changes: [file:line diffs summary]
  - Tests Added: [list]
  - Review Status: [approved/changes requested with details]
  - Integration Status: [pass/fail with evidence]

### Reviews & Integration
- code-reviewer findings: [resolved/open with file:line]
- integration-verifier scenarios: [pass/fail with logs]
- Blocking Issues: [list if any]
- Tech Debt: [suggestions documented]

## Verification Summary
Scope: <components implemented>
Criteria: <all acceptance criteria>
Commands:
- <command> -> exit <code>
Evidence:
- <test output snippets>
- <coverage report if available>
- <build artifacts>
Risks / Follow-ups: <tech debt, suggestions, known issues>

## Recommendations / Next Steps
[Prioritized: Blocking issues first, then tech debt, then enhancements]

## Open Questions / Assumptions
[If any decisions need clarification or assumptions made]
```

**Validation Checklist**:
- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes all commands with exit codes
- [ ] All components documented with TDD cycle evidence
- [ ] Review feedback classified (blocking/important/suggestions)
- [ ] Integration status documented with evidence
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken
