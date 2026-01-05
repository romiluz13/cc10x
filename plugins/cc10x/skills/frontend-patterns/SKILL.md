---
name: frontend-patterns
description: |
  DO NOT invoke directly - loaded by workflow agents via cc10x-router.
  Conditionally loaded by: code-reviewer (UI code), component-builder (UI component), bug-investigator (UI bug), integration-verifier (UI flow testing), planner (UI planning).
  Provides frontend patterns: UX, visual design, accessibility, responsive design. Iron Law: NO UI DESIGN BEFORE USER FLOW IS UNDERSTOOD.
allowed-tools: Read, Grep, Glob
---

# Frontend Patterns

## Overview

User interfaces exist to help users accomplish tasks. Every UI decision should make the user's task easier or the interface more accessible.

**Core principle:** Design for user success, not aesthetic preference.

**Violating the letter of this process is violating the spirit of frontend design.**

## The Iron Law

```
NO UI DESIGN BEFORE USER FLOW IS UNDERSTOOD
```

If you haven't mapped what the user is trying to accomplish, you cannot design UI.

## Success Criteria Framework

**Every UI must have explicit success criteria:**

1. **Task completion**: Can user complete their goal?
2. **Error recovery**: Can user recover from mistakes?
3. **Accessibility**: Can all users access it?
4. **Performance**: Does it feel responsive?

## Universal Questions (Answer First)

**ALWAYS answer before designing/reviewing:**

1. **What is the user trying to accomplish?** - Specific task, not feature
2. **What are the steps?** - Click by click
3. **What can go wrong?** - Every error state
4. **Who might struggle?** - Accessibility needs
5. **What's the existing pattern?** - Project conventions

## User Flow First

**Before any UI work, map the flow:**

```
User Flow: Create Account
1. User lands on signup page
2. User enters email
3. User enters password
4. User confirms password
5. System validates inputs (inline)
6. User clicks submit
7. System processes (loading state)
8. Success: User sees confirmation + redirect
9. Error: User sees error + can retry
```

**For each step, identify:**
- What user sees
- What user does
- What feedback they get
- What can go wrong

## UX Review Checklist

| Check | Criteria | Example Issue |
|-------|----------|---------------|
| **Task completion** | Can user complete goal? | Button doesn't work |
| **Discoverability** | Can user find what they need? | Hidden navigation |
| **Feedback** | Does user know what's happening? | No loading state |
| **Error handling** | Can user recover from errors? | No error message |
| **Efficiency** | Can user complete task quickly? | Too many steps |

**Severity levels:**
- **BLOCKS**: User cannot complete task
- **IMPAIRS**: User can complete but with difficulty
- **MINOR**: Small friction, not blocking

## Accessibility Review Checklist (WCAG 2.1 AA)

| Check | Criterion | How to Verify |
|-------|-----------|---------------|
| **Keyboard** | All interactive elements keyboard accessible | Tab through entire flow |
| **Focus visible** | Current focus clearly visible | Tab and check highlight |
| **Focus order** | Logical tab order | Tab matches visual order |
| **Labels** | All inputs have labels | Check `<label>` or `aria-label` |
| **Alt text** | Images have meaningful alt | Check `alt` attributes |
| **Color contrast** | 4.5:1 for text, 3:1 for large | Use contrast checker |
| **Color alone** | Info not conveyed by color only | Check without color |
| **Screen reader** | Content accessible via SR | Test with VoiceOver/NVDA |

**For each issue found:**
```markdown
- [WCAG 2.1 1.4.3] Color contrast at `component:line`
  - Current: 3.2:1 (fails AA)
  - Required: 4.5:1
  - Fix: Change text color to #333 (7.1:1)
```

## Visual Design Checklist

| Check | Good | Bad |
|-------|------|-----|
| **Hierarchy** | Clear visual priority | Everything same size |
| **Spacing** | Consistent rhythm | Random gaps |
| **Alignment** | Elements aligned to grid | Misaligned elements |
| **Interactive states** | Hover/active/focus distinct | No state changes |
| **Feedback** | Clear response to actions | Silent interactions |

### Visual Creativity (Avoid AI Slop)

When creating frontends, avoid generic AI aesthetics:

- **Fonts**: Choose distinctive typography, not defaults (avoid Inter, Roboto, Arial, system fonts)
- **Colors**: Commit to cohesive palette. Dominant colors with sharp accents > safe gradients
- **Avoid**: Purple gradients on white, predictable layouts, cookie-cutter Bootstrap/Tailwind defaults

Make creative choices that feel designed for the specific context.

## Component Patterns

### Buttons
```tsx
// Primary action button with all states
<button
  type="button"
  onClick={handleAction}
  disabled={isLoading || isDisabled}
  aria-busy={isLoading}
  aria-disabled={isDisabled}
  className={cn(
    'btn-primary',
    isLoading && 'btn-loading'
  )}
>
  {isLoading ? (
    <>
      <Spinner aria-hidden />
      <span>Processing...</span>
    </>
  ) : (
    'Submit'
  )}
</button>
```

### Forms with Validation
```tsx
<form onSubmit={handleSubmit} noValidate>
  <div className="form-field">
    <label htmlFor="email">
      Email <span aria-hidden>*</span>
      <span className="sr-only">(required)</span>
    </label>
    <input
      id="email"
      type="email"
      value={email}
      onChange={handleChange}
      aria-invalid={errors.email ? 'true' : undefined}
      aria-describedby={errors.email ? 'email-error' : 'email-hint'}
      required
    />
    <span id="email-hint" className="hint">
      We'll never share your email
    </span>
    {errors.email && (
      <span id="email-error" role="alert" className="error">
        {errors.email}
      </span>
    )}
  </div>
</form>
```

### Loading States
```tsx
function DataList({ isLoading, data, error }) {
  if (isLoading) {
    return (
      <div aria-live="polite" aria-busy="true">
        <Spinner />
        <span>Loading items...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" className="error-state">
        <p>Failed to load items: {error.message}</p>
        <button onClick={retry}>Try again</button>
      </div>
    );
  }

  if (!data?.length) {
    return (
      <div className="empty-state">
        <p>No items found</p>
        <button onClick={createNew}>Create your first item</button>
      </div>
    );
  }

  return <ul>{data.map(item => <Item key={item.id} {...item} />)}</ul>;
}
```

### Error Messages
```tsx
// Inline error with recovery action
<div role="alert" className="error-banner">
  <Icon name="error" aria-hidden />
  <div>
    <p className="error-title">Upload failed</p>
    <p className="error-detail">File too large. Maximum size is 10MB.</p>
  </div>
  <button onClick={selectFile}>Choose different file</button>
</div>
```

## Responsive Design Checklist

| Breakpoint | Check |
|------------|-------|
| **Mobile (< 640px)** | Touch targets 44px+, no horizontal scroll |
| **Tablet (640-1024px)** | Layout adapts, navigation accessible |
| **Desktop (> 1024px)** | Content readable, not too wide |

## Red Flags - STOP and Reconsider

If you find yourself:

- Designing UI before mapping user flow
- Focusing on aesthetics before functionality
- Ignoring accessibility ("we'll add it later")
- Not handling error states
- Not providing loading feedback
- Using color alone to convey information
- Making decisions based on "it looks nice"

**STOP. Go back to user flow.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Most users don't use keyboard" | Some users ONLY use keyboard. |
| "We'll add accessibility later" | Retrofitting is 10x harder. |
| "Error states are edge cases" | Errors happen. Handle them. |
| "Loading is fast, no need for state" | Network varies. Show state. |
| "It looks better without labels" | Unlabeled inputs are inaccessible. |
| "Users can figure it out" | If it's confusing, fix it. |

## Output Format

```markdown
## Frontend Review: [Component/Feature]

### User Flow
[Step-by-step what user is trying to do]

### Success Criteria
- [ ] User can complete [task]
- [ ] User can recover from errors
- [ ] All users can access (keyboard, screen reader)
- [ ] Interface feels responsive

### UX Issues
| Severity | Issue | Location | Impact | Fix |
|----------|-------|----------|--------|-----|
| BLOCKS | [Issue] | `file:line` | [Impact] | [Fix] |

### Accessibility Issues
| WCAG | Issue | Location | Fix |
|------|-------|----------|-----|
| 1.4.3 | [Issue] | `file:line` | [Fix] |

### Visual Issues
| Issue | Location | Fix |
|-------|----------|-----|
| [Issue] | `file:line` | [Fix] |

### Recommendations
1. [Most critical fix]
2. [Second fix]
```

## Final Check

Before completing frontend work:

- [ ] User flow mapped and understood
- [ ] All states handled (loading, error, empty, success)
- [ ] Keyboard navigation works
- [ ] Screen reader tested
- [ ] Color contrast verified
- [ ] Touch targets adequate on mobile
- [ ] Error messages clear and actionable
- [ ] Success criteria met
