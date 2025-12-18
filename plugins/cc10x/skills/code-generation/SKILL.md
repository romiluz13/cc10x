---
name: code-generation
description: This skill should be used when the user asks to "write code", "implement a function", "create a component", "generate code", or needs guidance on code implementation patterns and best practices.
---

# Code Generation

Generate code aligned with project patterns and functionality requirements.

## Process

### 1. Understand Requirements

Before writing code:

- What functionality is needed?
- What are the inputs and outputs?
- What are the edge cases?
- What project patterns exist?

### 2. Study Project Patterns

```bash
# Find similar code
grep -r "similar_pattern" --include="*.ts" src/ | head -10

# Check existing conventions
find src -name "*.ts" | head -20
```

Match: Naming conventions, file structure, coding style.

### 3. Write Minimal Code

Follow the principle of minimal implementation:

- Write only what's needed for the requirement
- No premature abstraction
- No over-engineering
- Keep it simple

### 4. Follow Project Conventions

Align with existing patterns:

- Naming: Match project naming style
- Structure: Match project file organization
- Style: Match project coding conventions
- Error handling: Match project error patterns

## Code Quality Checklist

Before completing:

- [ ] Handles expected inputs correctly
- [ ] Handles edge cases
- [ ] Follows project naming conventions
- [ ] Follows project structure
- [ ] No hardcoded values (use constants)
- [ ] No commented-out code
- [ ] No console.log debugging statements

## Common Patterns

### Functions
```typescript
// Clear name, typed parameters, return type
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Error Handling
```typescript
// Match project error handling patterns
try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  throw new AppError('Operation failed', { cause: error });
}
```

## Output

When generating code, provide:

1. The code implementation
2. Brief explanation of key decisions
3. Any assumptions made

## Common Mistakes

1. **Over-engineering** - Write minimal code, not framework
2. **Ignoring project patterns** - Match existing conventions
3. **Missing edge cases** - Handle errors and edge cases
4. **Premature abstraction** - Don't abstract until needed
