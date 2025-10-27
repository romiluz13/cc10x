---
description: Create detailed implementation plan with architecture, tasks, and risk analysis
argument-hint: [feature-description]
---

# Feature Planning Workflow

You are creating a comprehensive implementation plan.

## Context
- Feature: $ARGUMENTS
- Current project state: !`ls -la`
- Git status: !`git status --short`

## Your Task

Create a detailed plan including:

1. **Requirements Analysis**
   - Parse feature description
   - Identify core vs optional requirements
   - List dependencies and assumptions

2. **Architecture Design**
   - Component structure
   - Data flow
   - Integration points
   - Technology choices

3. **Task Breakdown**
   - Split into implementable tasks
   - Estimate complexity (1-5 scale)
   - Identify dependencies
   - Suggest order

4. **Risk Analysis**
   - Use the `8-dimensions` skill for comprehensive risk assessment
   - Identify critical risks
   - Propose mitigation strategies

5. **Success Criteria**
   - Define done
   - List test scenarios
   - Performance targets
   - UX requirements

## Output Format

```markdown
# Implementation Plan: [Feature Name]

## Requirements
- ...

## Architecture
- ...

## Tasks
1. [Task 1] (complexity: X)
2. [Task 2] (complexity: Y)
...

## Risks & Mitigation
- ...

## Success Criteria
- ...

## Estimated Effort
- Total complexity: X
- Suggested approach: [Fast/Balanced/Systematic]
```

## Next Steps
After plan approval, use `/build` to implement.

