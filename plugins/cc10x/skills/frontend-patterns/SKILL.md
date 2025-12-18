---
name: frontend-patterns
description: This skill should be used when the user asks about "UI design", "UX patterns", "accessibility", "frontend components", "user interface", or needs guidance on building user-facing interfaces.
---

# Frontend Patterns

Design and review user interfaces for UX, visual design, and accessibility.

## Process

### 1. Understand User Flows

Before designing/reviewing:

- What is the user trying to accomplish?
- What are the steps in the flow?
- What can go wrong?

### 2. Check UX Issues

Usability problems that block functionality:

- Can user complete the task?
- Is the flow intuitive?
- Are errors clear and actionable?

### 3. Check Visual Design

Visual issues affecting usability:

- Is hierarchy clear?
- Are interactive elements obvious?
- Is feedback visible?

### 4. Check Accessibility

Accessibility issues blocking users:

- Keyboard navigation works?
- Screen reader compatible?
- Color contrast sufficient?

## UX Checklist

- [ ] Task can be completed (happy path works)
- [ ] Errors are clear and actionable
- [ ] Loading states visible
- [ ] Success feedback provided
- [ ] Flow is intuitive (no confusion)

## Accessibility Checklist

- [ ] Keyboard navigation (all interactive elements reachable)
- [ ] Focus visible (current element highlighted)
- [ ] Screen reader labels (aria-label where needed)
- [ ] Color contrast (4.5:1 for text)
- [ ] No reliance on color alone (use icons/text too)

## Component Patterns

### Buttons
```tsx
// Clear purpose, accessible
<button
  onClick={handleSubmit}
  disabled={isLoading}
  aria-busy={isLoading}
>
  {isLoading ? 'Saving...' : 'Save'}
</button>
```

### Forms
```tsx
// Labels, validation, error messages
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  aria-invalid={hasError}
  aria-describedby={hasError ? 'email-error' : undefined}
/>
{hasError && <span id="email-error" role="alert">{errorMessage}</span>}
```

### Loading States
```tsx
// Clear feedback during async operations
{isLoading ? (
  <span aria-live="polite">Loading...</span>
) : (
  <Content />
)}
```

## Output Format

```markdown
## Frontend Review

### User Flow
[What user is trying to do]

### UX Issues
- [Issue] - [Impact on user] - [Fix]

### Accessibility Issues
- [Issue] - [WCAG criterion] - [Fix]

### Visual Issues
- [Issue] - [Impact] - [Fix]
```

## Common Mistakes

1. **Reviewing without understanding user flow** - Know what user needs to accomplish
2. **Accessibility afterthought** - Check accessibility alongside UX
3. **Generic feedback** - Be specific about impact on users
4. **Missing WCAG references** - Cite accessibility standards
