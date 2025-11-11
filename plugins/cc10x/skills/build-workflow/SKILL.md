---
name: build-workflow
description: MUST be activated through cc10x-orchestrator - do not use directly. Orchestrator coordinates this build workflow with functionality-first approach. First understands functionality requirements (user flow, admin flow, system flow), then builds features to implement that functionality. Focuses on making functionality work first, then optimizing. Loads shared skills and invokes component-builder, code-reviewer, and integration-verifier sequentially. Use when orchestrator detects build intent.
allowed-tools: Read, Grep, Glob, Task, Bash
---

# Build Workflow - Functionality First

## Functionality First Mandate

**BEFORE building features, understand functionality**:

1. **What functionality needs to be built?**
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?

2. **THEN build** - Build features to implement that functionality

3. **Use TDD** - Apply TDD AFTER functionality is understood

---

TDD-driven implementation with review and integration verification, functionality-first approach.

## Quick Start

Build features using TDD cycle after understanding functionality.

**Example:**

1. **Understand functionality**: User uploads files (User Flow: select → upload → confirm)
2. **Phase 0**: Complete functionality analysis
3. **TDD Cycle**: Write failing test (RED) → Implement code (GREEN) → Refactor
4. **Invoke subagents**: component-builder → code-reviewer → integration-verifier
5. **Verify**: All tests pass, functionality works

**Result:** Feature built with TDD, functionality verified, code reviewed.

## Requirements

**Dependencies:**

- `cc10x-orchestrator` - Must be activated through orchestrator (do not use directly)
- `test-driven-development` - Required for TDD cycle
- `code-generation` - Required for code implementation
- `verification-before-completion` - Required for completion verification

**Prerequisites:**

- Phase 0 (Functionality Analysis) completed via orchestrator
- Complexity assessment completed (score ≤2 to proceed)
- Project context understood

**Tool Access:**

- Required tools: Read, Grep, Glob, Task, Bash
- Task tool: Used to invoke subagents (component-builder, code-reviewer, integration-verifier)

**Subagents:**

- component-builder - Builds code components
- code-reviewer - Reviews code for issues
- integration-verifier - Verifies integration works

## Process

For complete instructions, see `plugins/cc10x/skills/cc10x-orchestrator/workflows/build.md`.

## Quick Reference

**Decision Tree**:

```
BUILD NEEDED?
│
├─ Understand Functionality First
│  ├─ User/Admin/System flows identified? → Continue
│  └─ Not identified? → STOP, complete functionality analysis first
│
├─ Complexity Check
│  ├─ Score <=2? → Continue
│  └─ Score >2? → STOP, break down into smaller components
│
├─ TDD Cycle (Per Component)
│  ├─ RED: Write failing test → Continue
│  ├─ GREEN: Make test pass → Continue
│  ├─ REFACTOR: Improve code → Continue
│  └─ Component complete? → Next component
│
├─ Review & Integration
│  ├─ code-reviewer → integration-verifier (sequential)
│  ├─ All checks pass? → Continue
│  └─ Issues found? → Fix and re-verify
│
└─ Verify
   ├─ Functionality works? → Complete
   └─ Functionality broken? → Return to TDD cycle
```

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

## Troubleshooting

**Common Issues:**

1. **TDD cycle not followed**
   - **Symptom**: Code written without failing test first
   - **Cause**: Skipped RED step in TDD cycle
   - **Fix**: Delete code, write failing test first, verify it fails, then implement
   - **Prevention**: Always follow RED → GREEN → REFACTOR cycle

2. **Functionality analysis skipped**
   - **Symptom**: Building without understanding user/admin/system flows
   - **Cause**: Skipped Phase 0 (Functionality Analysis)
   - **Fix**: Complete functionality analysis first, then proceed
   - **Prevention**: Never skip Phase 0

3. **Subagents not invoked**
   - **Symptom**: Code written directly instead of using subagents
   - **Cause**: Bypassed orchestrator subagent dispatch
   - **Fix**: Use Task tool to invoke component-builder, code-reviewer, integration-verifier
   - **Prevention**: Always invoke subagents through orchestrator

**If issues persist:**

- Verify Phase 0 (Functionality Analysis) was completed
- Check that TDD cycle was followed (RED → GREEN → REFACTOR)
- Ensure subagents were invoked, not bypassed
- Review workflow instructions in `workflows/build.md`

**Validation Checklist**:

- [ ] Executive Summary present (2-3 sentences)
- [ ] Verification Summary includes all commands with exit codes
- [ ] All components documented with TDD cycle evidence
- [ ] Review feedback classified (blocking/important/suggestions)
- [ ] Integration status documented with evidence
- [ ] Recommendations prioritized
- [ ] All subagents/skills documented in Actions Taken
