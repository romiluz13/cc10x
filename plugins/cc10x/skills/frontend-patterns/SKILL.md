---
name: frontend-patterns
description: "Use when frontend UI work needs accessibility, responsive layout, loading/error states, performance guardrails, or DESIGN.md authoring from screenshots, existing UI, user preferences, or chosen visual inspiration under an approved visual direction."
allowed-tools: Read Grep Glob LSP
---

# Frontend Patterns

## Overview

User interfaces exist to help users accomplish tasks. Every UI decision should make the user's task easier or the interface more accessible.

**Core principle:** Design for user success, not aesthetic preference.

This skill is advisory in v10. Explicit user instructions, `CLAUDE.md`, repo standards, and approved plans override every suggestion here.

## Reference Files

Read only the references needed for the current UI task:

- `references/ui-state-and-feedback.md` for loading/error/empty/success ordering, skeleton vs spinner, and mutation feedback
- `references/accessibility-and-forms.md` for WCAG-oriented checks, keyboard/focus, labels, form patterns, and mobile usability
- `references/performance-and-layout.md` for responsive checks, motion, overflow, URL state, performance guardrails, and light/dark mode checks
- `references/design-md-authoring.md` for creating or updating a project-local `DESIGN.md` from screenshots, existing UI, user preferences, or a selected inspiration style
- `references/design-md-inspiration-index.md` only when the user asks for a style reference, brand-like direction, moodboard, or DESIGN.md-style examples

## Focus Areas (Reference Pattern)

- **React component architecture** (hooks, context, performance)
- **Responsive CSS** with Tailwind/CSS-in-JS
- **State management** (Redux, Zustand, Context API)
- **Frontend performance** (lazy loading, code splitting, memoization)
- **Accessibility** (WCAG compliance, ARIA labels, keyboard navigation)

## Approach (Reference Pattern)

1. **Component-first thinking** - reusable, composable UI pieces
2. **Mobile-first responsive design** - start small, scale up
3. **Performance budgets** - aim for sub-3s load times
4. **Semantic HTML** and proper ARIA attributes
5. **Type safety** with TypeScript when applicable

## Advisory Guardrails

Use this skill to add:
- accessibility checks
- responsive/layout verification
- performance and loading-state checks
- optional style ideas when the user explicitly wants them

Do not use this skill to override an explicit visual direction, component contract, or approved workflow.

## Component Output Checklist

**Every frontend deliverable should include:**

- [ ] Complete React component with props interface
- [ ] Styling solution (Tailwind classes or styled-components)
- [ ] State management implementation if needed
- [ ] Basic unit test structure
- [ ] Accessibility checklist for the component
- [ ] Performance considerations and optimizations

**Focus on working code over explanations. Include usage examples in comments.**

## The Iron Law

```
NO UI DESIGN BEFORE USER FLOW IS UNDERSTOOD
```

If you haven't mapped what the user is trying to accomplish, you cannot design UI.

## Design Thinking (Pre-Code)

Before writing any UI code, commit to answers for:

1. **Purpose**: What specific problem does this interface solve?
2. **Tone**: Choose an aesthetic direction and commit to it:
   - Brutally minimal, maximalist, retro-futuristic, organic/natural
   - Luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw
   - Art deco/geometric, soft/pastel, industrial/utilitarian
3. **Constraints**: Framework requirements, performance budget, accessibility level
4. **Differentiation**: What's the ONE thing someone will remember about this UI?

**Key insight:** Bold maximalism and refined minimalism both work. The enemy is indecision and generic defaults.

## DESIGN.md Authoring

Read `references/design-md-authoring.md` before creating or updating a project-local `DESIGN.md`, especially when the user provides screenshots, existing UI, visual preferences, or asks the agent to preserve a design direction.

When inspiration is needed, read `references/design-md-inspiration-index.md` to choose a style family. Treat inspiration as input to the project's own design contract, not as an instruction to copy another company's UI.

## UI State References

Read `references/ui-state-and-feedback.md` before finalizing loading, error,
empty, success, or mutation states. Keep the state order explicit; do not invent
UI states ad hoc.

## Motion & Animation

| Rule | Do | Don't |
|------|-----|-------|
| **Reduced motion** | Honor `prefers-reduced-motion` | Ignore user preferences |
| **Properties** | Animate `transform`/`opacity` only | Animate `width`/`height`/`top`/`left` |
| **Transitions** | List properties explicitly | Use `transition: all` |
| **Duration** | 150-300ms for micro-interactions | Too fast (<100ms) or slow (>500ms) |
| **Interruptible** | Allow animation cancellation | Lock UI during animation |

```css
/* CORRECT: Compositor-friendly, respects preferences */
@media (prefers-reduced-motion: no-preference) {
  .card { transition: transform 200ms ease-out, opacity 200ms ease-out; }
  .card:hover { transform: translateY(-2px); opacity: 0.95; }
}
```

## Accessibility And Forms

Read `references/accessibility-and-forms.md` when the task touches keyboard
navigation, forms, labels, focus, contrast, or touch ergonomics.

## Success Criteria Framework

**Every UI must have explicit success criteria:**

1. **Task completion**: Can user complete their goal?
2. **Error recovery**: Can user recover from mistakes?
3. **Accessibility**: Can all users access it?
4. **Performance**: Does it feel responsive?

## Layout And Performance References

Read `references/performance-and-layout.md` for responsive checks, motion rules,
overflow handling, URL state, touch/mobile, and color-mode validation.

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
- **Icons**: Use SVG icons (Heroicons, Lucide, Simple Icons). **NEVER use emoji as UI icons**
- **Cursor**: Add `cursor-pointer` to ALL clickable elements
- **Hover**: Use color/opacity transitions. Avoid `scale` transforms that shift layout
- **Backgrounds**: Add depth with subtle textures, gradients, or grain instead of flat colors

Make creative choices that feel designed for the specific context. No two designs should look the same.

### Spatial Composition (Break the Grid)

Move beyond safe, centered layouts:

| Technique | Effect | When to Use |
|-----------|--------|-------------|
| **Asymmetry** | Dynamic tension, visual interest | Hero sections, feature highlights |
| **Overlap** | Depth, connection between elements | Cards, images, testimonials |
| **Diagonal flow** | Energy, movement | Landing pages, marketing |
| **Grid-breaking** | Emphasis, surprise | Key CTAs, focal points |
| **Generous negative space** | Luxury, breathing room | Premium products, editorial |
| **Controlled density** | Information-rich, productive | Dashboards, data-heavy UIs |

**Rule:** Match spatial composition to the aesthetic direction chosen in Design Thinking. Minimalist = negative space. Maximalist = controlled density.

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

## Anti-patterns Blocklist (Flag These)

| Anti-pattern | Why It's Wrong | Fix |
|--------------|----------------|-----|
| `user-scalable=no` | Blocks accessibility zoom | Remove it |
| `maximum-scale=1` | Blocks accessibility zoom | Remove it |
| `transition: all` | Performance + unexpected effects | List properties explicitly |
| `outline-none` without replacement | Removes focus indicator | Add `focus-visible:ring-*` |
| `<div onClick>` | Not keyboard accessible | Use `<button>` or `<a>` |
| Images without `width`/`height` | Causes layout shift (CLS) | Add explicit dimensions |
| Form inputs without labels | Inaccessible | Add `<label>` or `aria-label` |
| Icon buttons without `aria-label` | Unnamed to screen readers | Add `aria-label` |
| Emoji icons (🚀 ✨ 💫) | Unprofessional, inconsistent | Use SVG icons |
| Hardcoded date/number formats | Breaks internationalization | Use `Intl.DateTimeFormat` |
| `autoFocus` everywhere | Disorienting, mobile issues | Use sparingly, desktop only |

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

## UI States Checklist (CRITICAL)

**Before completing ANY UI component:**

### States
- [ ] Error state handled and shown to user
- [ ] Loading state shown ONLY when no data exists
- [ ] Empty state provided for all collections/lists
- [ ] Success state with appropriate feedback
- [ ] Non-trivial state-order or skeleton/spinner decisions checked against `references/ui-state-and-feedback.md`

### Buttons & Mutations
- [ ] Buttons disabled during async operations
- [ ] Buttons show loading indicator
- [ ] Mutations have onError handler with user feedback
- [ ] No double-click possible on submit buttons

### Data Handling
- [ ] State order: Error → Loading (no data) → Empty → Success
- [ ] All user actions have feedback (toast/visual)

## Final Check

Before completing frontend work:

- [ ] User flow mapped and understood
- [ ] All states handled (loading, error, empty, success)
- [ ] Keyboard navigation works
- [ ] Screen reader tested
- [ ] Color contrast verified (4.5:1 minimum)
- [ ] Touch targets adequate on mobile (44px+)
- [ ] Error messages clear and actionable
- [ ] Success criteria met
- [ ] No emoji icons (SVG only)
- [ ] `prefers-reduced-motion` respected
- [ ] Light/dark mode contrast verified
- [ ] `cursor-pointer` on all clickable elements
- [ ] No `transition: all` in codebase
