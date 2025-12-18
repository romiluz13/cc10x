---
name: cc10x-router
description: This skill should be used when the user asks to "build", "implement", "create", "review", "audit", "debug", "fix", "plan", or "design" something. Routes requests to appropriate agents (component-builder, code-reviewer, bug-investigator, planner) based on detected intent.
---

# cc10x Router - Simple Workflow Coordination

Route user requests to the appropriate agent based on intent detection.

## Intent Detection

Detect intent from user request and route to the appropriate workflow:

| Intent Keywords | Workflow | Agent Chain |
|-----------------|----------|-------------|
| build, implement, create, write, add, make | BUILD | component-builder → code-reviewer → integration-verifier |
| review, audit, check, analyze, assess | REVIEW | code-reviewer |
| debug, fix, error, bug, troubleshoot, broken | DEBUG | bug-investigator → code-reviewer → integration-verifier |
| plan, design, architect, roadmap, strategy | PLAN | planner |

## Workflow Execution

### BUILD Workflow

When user wants to build/implement/create something:

1. **Understand what to build** - Clarify requirements if unclear
2. **Invoke component-builder** - Uses TDD cycle (RED → GREEN → REFACTOR)
3. **Invoke code-reviewer** - Reviews the built code
4. **Invoke integration-verifier** - Verifies end-to-end functionality

### REVIEW Workflow

When user wants to review/audit code:

1. **Understand what to review** - Identify files/PR/changes
2. **Invoke code-reviewer** - Reviews for security, quality, performance

### DEBUG Workflow

When user encounters errors/bugs:

1. **Understand what's broken** - Clarify the error/symptom
2. **Invoke bug-investigator** - Uses LOG FIRST approach to diagnose and fix
3. **Invoke code-reviewer** - Reviews the fix
4. **Invoke integration-verifier** - Verifies fix works end-to-end

### PLAN Workflow

When user wants to plan/design:

1. **Understand what to plan** - Clarify scope and goals
2. **Invoke planner** - Creates architecture, identifies risks, builds roadmap

## Agent Invocation

Use Task tool to invoke agents:

```
Task(subagent_type="cc10x:component-builder", prompt="Build [component description]")
Task(subagent_type="cc10x:code-reviewer", prompt="Review [code/PR description]")
Task(subagent_type="cc10x:bug-investigator", prompt="Debug [error description]")
Task(subagent_type="cc10x:integration-verifier", prompt="Verify [integration description]")
Task(subagent_type="cc10x:planner", prompt="Plan [feature description]")
```

## Sequential vs Parallel

- **BUILD workflow**: Sequential (component-builder → code-reviewer → integration-verifier)
- **DEBUG workflow**: Sequential (bug-investigator → code-reviewer → integration-verifier)
- **REVIEW workflow**: Single agent (code-reviewer)
- **PLAN workflow**: Single agent (planner)

Always run agents sequentially when outputs depend on previous steps.

## Output Format

After workflow completion, provide:

```markdown
## Workflow Summary

- **Intent**: [BUILD/REVIEW/DEBUG/PLAN]
- **Agents Used**: [list]
- **Result**: [success/issues found]

## Key Outcomes

[Summary of what was accomplished]

## Next Steps

[If any follow-up needed]
```
