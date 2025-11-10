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

## Reference Materials

**For detailed design principles, token systems, typography, layout, and state design patterns, see:**

- **REFERENCE.md**: Design Principles, Token Systems, Typography Decision Framework, Layout Decision Framework, State Design Patterns, Design System Checklist

---

## Integration with Other Skills

- `ux-patterns`: Complements with interaction behavior and UX flows
- `accessibility-patterns`: Enforces WCAG compliance in visual design
- `component-design-patterns`: Applies visual tokens to component APIs
- `design-patterns`: Coordinates with API and integration patterns

---

## Integration with Other Skills

- `ux-patterns`: Complements with interaction behavior and UX flows
- `accessibility-patterns`: Enforces WCAG compliance in visual design
- `component-design-patterns`: Applies visual tokens to component APIs
- `design-patterns`: Coordinates with API and integration patterns
