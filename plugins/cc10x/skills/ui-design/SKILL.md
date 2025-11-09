---
name: ui-design
description: Visual design principles with functionality-first approach. Use PROACTIVELY when designing UI for functionality. First understands functionality (user flow, admin flow), then designs UI to support that functionality. Focuses on UI that enables functionality, not generic visual design. Covers visual hierarchy, design tokens, layout systems, typography, and state design.
---

# UI Design - Functionality First

## Functionality First Mandate

**BEFORE designing UI, understand functionality**:

1. **What functionality needs UI?**
   - What are the user flows?
   - What are the admin flows?

2. **THEN design UI** - Design UI to support that functionality

3. **Use principles** - Apply visual design principles AFTER functionality is understood

---

# UI Design - Stage 1: Metadata

## Skill Overview

**Name**: UI Design (Visual Systems)
**Purpose**: Create visually consistent, accessible, scalable interfaces through principles and systems
**When to Use**: Designing new UI, establishing design systems, evaluating visual quality
**Core Rule**: Systems before components - establish tokens and principles first
**Sections Available**: Design Principles, Token Systems, Layout Frameworks, State Design

---

## When to Use This Skill

**Always use when**:

- Creating new UI components
- Establishing design system or style guide
- Refactoring visual inconsistencies
- Building customer-facing interfaces

**Specific triggers**:

- User requests "beautiful", "modern", "professional", or "polished" UI
- Building dashboard, landing page, or product interface
- Component library or design system creation
- Visual redesign or modernization project

---

# Stage 2: Design Principles

## Core Principle: Visual Hierarchy

**WHY**: Users scan interfaces in predictable patterns (F-pattern, Z-pattern). Guide their eye deliberately.

### The Hierarchy Toolkit

**Size** - Larger = more important

```css
/* WEAK hierarchy - all similar size */
h1 {
  font-size: 18px;
}
h2 {
  font-size: 16px;
}
body {
  font-size: 14px;
}

/* STRONG hierarchy - clear scale */
h1 {
  font-size: 36px;
} /* 2.57x body */
h2 {
  font-size: 24px;
} /* 1.71x body */
body {
  font-size: 14px;
}
```

**Weight** - Bolder = more emphasis

```css
/* WEAK - all same weight */
.title,
.subtitle,
.body {
  font-weight: 400;
}

/* STRONG - weight conveys hierarchy */
.title {
  font-weight: 700;
} /* Bold for titles */
.subtitle {
  font-weight: 600;
} /* Semi-bold for subtitles */
.body {
  font-weight: 400;
} /* Regular for body */
.muted {
  font-weight: 300;
} /* Light for de-emphasis */
```

**Color** - Darker = primary, Lighter = secondary

```css
/* PRIMARY content - high contrast */
.primary-text {
  color: #111;
} /* 95% contrast on white */

/* SECONDARY content - medium contrast */
.secondary-text {
  color: #666;
} /* 60% contrast */

/* TERTIARY content - low contrast */
.tertiary-text {
  color: #999;
} /* 40% contrast */
```

**Spacing** - More space = visual separation

```css
/* Group related items closely */
.card-title {
  margin-bottom: 4px;
}
.card-subtitle {
  margin-bottom: 16px;
} /* 4x larger gap before body */
.card-body {
  margin-bottom: 24px;
}
```

---

## Principle: Rhythm and Pace

**WHY**: Consistent spacing creates visual rhythm. Random spacing feels chaotic.

### Decision Framework: Spacing Scales

**When to use 4px scale** (4, 8, 12, 16, 24, 32, 48, 64):

- Modern, tight designs
- Dense information (dashboards, tables)
- Component libraries (easier mental math)

**When to use 8px scale** (8, 16, 24, 32, 48, 64, 96):

- Spacious, breathing room designs
- Marketing sites, landing pages
- Simpler scale (fewer options = more consistency)

**When to use modular scale** (1em, 1.25em, 1.5em, 2em, 3em):

- Typography-driven designs
- Long-form content (blogs, documentation)
- Responsive designs (scales with font size)

**Example: Applying 8px scale**

```css
:root {
  --space-xs: 8px; /* Tight: icon-to-text */
  --space-sm: 16px; /* Compact: form fields */
  --space-md: 24px; /* Comfortable: card padding */
  --space-lg: 32px; /* Generous: section padding */
  --space-xl: 48px; /* Spacious: hero sections */
}

.button {
  padding: var(--space-xs) var(--space-sm); /* 8px vertical, 16px horizontal */
  margin-bottom: var(--space-md); /* 24px between buttons */
}
```

---

## Principle: Intentionality

**WHY**: Every visual decision should have a reason. Arbitrary choices create inconsistency.

### Decision Framework: Color Purpose

**Semantic colors** (meaning-driven):

```css
:root {
  /* Status colors */
  --color-success: #10b981; /* Green for positive actions */
  --color-warning: #f59e0b; /* Orange for caution */
  --color-error: #ef4444; /* Red for errors */
  --color-info: #3b82f6; /* Blue for information */

  /* Brand colors */
  --color-primary: #your-brand; /* Call-to-action */
  --color-secondary: #complement; /* Supporting actions */
}

/* USE semantic names, NOT color names */
.button-primary {
  background: var(--color-primary);
} /* Good */
.button-blue {
  background: var(--color-primary);
} /* Bad - not semantic */
```

**When to use semantic colors**:

- Status indicators (success, warning, error)
- Call-to-action buttons
- Alerts and notifications

**When to use neutral colors**:

- Text hierarchy (primary, secondary, tertiary)
- Borders and dividers
- Backgrounds and surfaces

---

## Principle: Coherence

**WHY**: Consistent patterns reduce cognitive load. Users learn once, apply everywhere.

### Button States Example

**INCONSISTENT** - each button has different hover behavior:

```css
.button-primary:hover {
  transform: scale(1.1);
}
.button-secondary:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.button-danger:hover {
  border-width: 2px;
}
```

**COHERENT** - all buttons share state pattern:

```css
.button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button:active {
  transform: translateY(0);
  box-shadow: none;
}

.button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

# Stage 3: Design Token Systems

## Token Philosophy

**Tokens are variables with purpose**. They enable:

1. **Consistency** - reuse same values
2. **Maintainability** - change once, update everywhere
3. **Theming** - swap token values for dark mode, brand variants
4. **Scale** - add new components using existing tokens

---

## Decision Framework: Token Structure

### Flat Tokens (Small Projects)

```css
:root {
  --blue: #3b82f6;
  --space-2: 8px;
  --font-md: 14px;
}
```

**Use when**: <10 components, single theme, small team

### Semantic Tokens (Medium Projects)

```css
:root {
  --color-primary: #3b82f6;
  --color-text: #111;
  --space-comfortable: 16px;
}
```

**Use when**: Growing component library, need theming, multiple developers

### Tiered Tokens (Large Projects)

```css
:root {
  /* Primitive tokens */
  --blue-500: #3b82f6;
  --space-2: 8px;

  /* Semantic tokens (reference primitives) */
  --color-primary: var(--blue-500);
  --space-button-padding: var(--space-2);

  /* Component tokens (reference semantic) */
  --button-primary-bg: var(--color-primary);
}
```

**Use when**: Design system, multi-brand, accessibility variations

---

## Typography Decision Framework

### When to use System Fonts

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```

**Use when**:

- Performance critical (no web font loading)
- Dashboard, admin interfaces
- Fast, utilitarian design

**Benefits**: 0ms load time, native OS feel, accessible
**Tradeoffs**: Less brand personality

### When to use Custom Fonts

```css
font-family: "Inter", sans-serif;
```

**Use when**:

- Brand identity matters (marketing, product sites)
- Design differentiation needed
- Budget for font licensing

**Best practices**:

- Load only 2-3 weights (400, 600, 700)
- Use `font-display: swap` to show fallback during load
- Self-host for performance (avoid Google Fonts latency)

---

## Layout Decision Framework

### Flexbox vs Grid

**Use Flexbox when**:

- Single direction (row or column)
- Items naturally size themselves
- Navigation bars, toolbars
- Simple card layouts

```css
.toolbar {
  display: flex;
  gap: 16px;
  align-items: center; /* Vertical centering */
}
```

**Use Grid when**:

- Two-dimensional layouts (rows AND columns)
- Explicit sizing needed
- Dashboard layouts, image galleries
- Complex responsive patterns

```css
.dashboard {
  display: grid;
  grid-template-columns: 200px 1fr; /* Sidebar + main */
  grid-template-rows: 60px 1fr; /* Header + content */
  gap: 16px;
}
```

---

## Responsive Design Decision Framework

### Mobile-First vs Desktop-First

**Mobile-First** (default styles for mobile, enhance for desktop):

```css
.card {
  padding: 16px;
  font-size: 14px;
}

@media (min-width: 768px) {
  .card {
    padding: 24px;
    font-size: 16px;
  }
}
```

**Use when**: Content-focused sites, broad audience, mobile traffic >50%

**Desktop-First** (default for desktop, simplify for mobile):

```css
.dashboard {
  display: grid;
  grid-template-columns: 250px 1fr 300px; /* Sidebar + main + aside */
}

@media (max-width: 1024px) {
  .dashboard {
    grid-template-columns: 1fr; /* Stack on mobile */
  }
}
```

**Use when**: Complex dashboards, B2B tools, desktop-primary users

---

## Breakpoint Decision Framework

**Minimal (3 breakpoints)**:

```css
/* Mobile: 0-767px */
/* Tablet: 768-1023px */
@media (min-width: 768px) {
}
/* Desktop: 1024px+ */
@media (min-width: 1024px) {
}
```

**Use when**: Simple layouts, rapid prototyping

**Standard (5 breakpoints)**:

```css
/* xs: 0-639px */
/* sm: 640-767px */
@media (min-width: 640px) {
}
/* md: 768-1023px */
@media (min-width: 768px) {
}
/* lg: 1024-1279px */
@media (min-width: 1024px) {
}
/* xl: 1280px+ */
@media (min-width: 1280px) {
}
```

**Use when**: Production sites, design systems, broad device support

---

# Stage 4: State Design

## The 7 Essential States

Every interactive component needs these states designed:

1. **Default** - Initial appearance
2. **Hover** - Mouse over (desktop only)
3. **Active** - Being clicked/pressed
4. **Focus** - Keyboard navigation (CRITICAL for accessibility)
5. **Disabled** - Cannot be interacted with
6. **Loading** - Operation in progress
7. **Error** - Validation failed or operation error

---

## State Design Patterns

### Loading States

**Decision Framework**:

**Skeleton screens** (when content structure is known):

```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}
```

**Use when**: Cards, lists, tables (known structure)

**Spinners** (when content structure unknown):

```css
.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}
```

**Use when**: Initial page load, indeterminate operations

**Progress bars** (when progress is measurable):

```html
<progress value="45" max="100">45%</progress>
```

**Use when**: File uploads, multi-step forms, batch operations

---

## Focus State (Accessibility Critical)

**ALWAYS visible**:

```css
.button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* NEVER remove focus outline without replacement */
/* BAD: */
.button:focus {
  outline: none;
} /* ❌ Breaks keyboard navigation */

/* GOOD: */
.button:focus-visible {
  outline: 2px solid var(--color-primary); /* ✅ Custom but visible */
}
```

---

# Stage 5: Design System Checklist

```
Foundation (Required):
- [ ] Spacing scale defined (4px, 8px, or modular)
- [ ] Color system (semantic + neutral + status)
- [ ] Typography scale (sizes, weights, line heights)
- [ ] Border radius values (0, 4px, 8px, 16px, full)

Layout (Required):
- [ ] Breakpoints defined and documented
- [ ] Grid system or flexbox patterns
- [ ] Container max-widths
- [ ] Responsive strategy (mobile-first or desktop-first)

States (Required):
- [ ] All 7 states designed for buttons
- [ ] Focus states highly visible
- [ ] Loading patterns chosen
- [ ] Error states designed

Accessibility (Required):
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 large text)
- [ ] Focus indicators visible
- [ ] Touch targets ≥44x44px
- [ ] Text resizable to 200% without loss

Advanced (Optional):
- [ ] Dark mode / theme variants
- [ ] Motion/animation tokens
- [ ] Elevation/shadow system
- [ ] Icon system
```

---

## Before/After: Weak vs Strong Hierarchy

**WEAK** - flat hierarchy, no clear focus:

```css
.card-title {
  font-size: 16px;
  font-weight: 400;
  color: #333;
}
.card-subtitle {
  font-size: 14px;
  font-weight: 400;
  color: #444;
}
.card-body {
  font-size: 14px;
  font-weight: 400;
  color: #333;
}
```

**STRONG** - clear hierarchy, guides the eye:

```css
.card-title {
  font-size: 24px;
  font-weight: 700;
  color: #111;
  margin-bottom: 4px;
}
.card-subtitle {
  font-size: 14px;
  font-weight: 500;
  color: #666;
  margin-bottom: 16px;
}
.card-body {
  font-size: 14px;
  font-weight: 400;
  color: #444;
  line-height: 1.6;
}
```

**Result**: Title is 71% larger, 75% bolder, 30% darker than body. Subtitle is visually secondary through color and weight.

---

## Integration with Other Skills

- `ux-patterns`: Complements with interaction behavior and UX flows
- `accessibility-patterns`: Enforces WCAG compliance in visual design
- `component-design-patterns`: Applies visual tokens to component APIs
- `design-patterns`: Coordinates with API and integration patterns
