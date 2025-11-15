# Pattern Composition Guidelines

This document provides guidelines for composing patterns across consolidated skills.

## Pattern Dependencies

### Core Patterns (No Dependencies)

- `functionality-first` - Base pattern for all skills
- `project-context-understanding` - Required for all workflows

### Composite Patterns

- `code-review-patterns` = `functionality-first` + `security-patterns` + `quality-patterns` + `performance-patterns`
- `debugging-patterns` = `functionality-first` + `systematic-debugging` + `log-analysis` + `root-cause-analysis`
- `planning-patterns` = `functionality-first` + `requirements-analysis` + `feature-planning`
- `frontend-patterns` = `functionality-first` + `ux-patterns` + `ui-design` + `accessibility-patterns`

## Pattern Reusability

### Shared Components

1. **Functionality Analysis** - Used by all skills
2. **Project Pattern Understanding** - Used by all skills
3. **Context-Dependent Flow Analysis** - Used by all skills

### Skill-Specific Components

1. **Security Checks** - Only in `code-review-patterns`
2. **Debugging Strategies** - Only in `debugging-patterns`
3. **Planning Templates** - Only in `planning-patterns`
4. **UX/UI/Accessibility Checks** - Only in `frontend-patterns`

## Pattern Versioning

Patterns are versioned by skill version:

- `code-review-patterns` v1.0 uses `functionality-first` v1.0
- All consolidated skills use the same `functionality-first` pattern version

## Pattern Composition Rules

1. **Always include functionality-first** - All skills must start with functionality analysis
2. **Understand project patterns** - All skills must understand project conventions
3. **Apply specialized checks** - Only after functionality and patterns are understood
4. **Provide specific fixes** - All fixes must align with project patterns
