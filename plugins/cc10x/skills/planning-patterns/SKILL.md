---
name: planning-patterns
description: This skill should be used when the user asks to "plan a feature", "design requirements", "create a roadmap", "analyze risks", or needs guidance on requirements gathering and feature planning.
---

# Planning Patterns

Plan features by understanding requirements, identifying risks, and creating actionable roadmaps.

## Process

### 1. Understand Requirements

Before planning:

- What problem does this solve?
- Who are the users?
- What must it do? (functional requirements)
- What constraints exist? (non-functional requirements)

### 2. Map Functionality Flows

Document the flows:

- **User Flow**: What steps does user take?
- **Admin Flow**: What do admins need to do?
- **System Flow**: What does system do internally?

### 3. Identify Risks

For each flow, identify what can go wrong:

| Risk | Probability (1-5) | Impact (1-5) | Score | Mitigation |
|------|-------------------|--------------|-------|------------|
| API timeout | 3 | 4 | 12 | Retry with backoff |
| Invalid input | 4 | 2 | 8 | Validation layer |

### 4. Create Roadmap

Prioritize by risk score and dependencies:

- **Phase 1**: Core functionality (must-haves)
- **Phase 2**: Supporting features (should-haves)
- **Phase 3**: Polish (nice-to-haves)

## Requirements Checklist

- [ ] Problem statement clear
- [ ] Users identified
- [ ] Functional requirements listed
- [ ] Non-functional requirements listed (performance, security, scale)
- [ ] Constraints documented
- [ ] Success criteria defined

## Risk Assessment

For each risk:

1. **Identify**: What can go wrong?
2. **Score**: Probability (1-5) × Impact (1-5)
3. **Mitigate**: How to reduce or prevent?
4. **Contingency**: What if it happens anyway?

## Output Format

```markdown
## Feature Plan

### Problem Statement
[What problem this solves]

### Requirements
- Functional: [list]
- Non-functional: [list]
- Constraints: [list]

### Flows
- User Flow: [steps]
- System Flow: [steps]

### Risks
| Risk | P | I | Score | Mitigation |
|------|---|---|-------|------------|
| ... | ... | ... | ... | ... |

### Roadmap
- **Phase 1**: [core features]
- **Phase 2**: [supporting features]
- **Phase 3**: [polish]

### Success Criteria
[How to know it's done]
```

## Common Mistakes

1. **Planning without understanding problem** - Start with problem statement
2. **Missing risks** - Every feature has risks, identify them
3. **No prioritization** - Phases must be prioritized
4. **Vague requirements** - Requirements must be specific and testable
