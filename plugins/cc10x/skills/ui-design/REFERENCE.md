# UI Design - Reference

Reference design principles, token systems, typography, layout, and state design patterns. Use AFTER understanding functionality (see SKILL.md).

## Design Principles

### Core Principle: Visual Hierarchy

**WHY**: Users scan interfaces in predictable patterns (F-pattern, Z-pattern). Guide their eye deliberately.

**The Hierarchy Toolkit**:

- **Size** - Larger = more important
- **Weight** - Bolder = more emphasis
- **Color** - Higher contrast = more attention
- **Position** - Top-left = most important

### Principle: Rhythm and Pace

**WHY**: Consistent spacing creates visual rhythm. Random spacing feels chaotic.

**Decision Framework: Spacing Scales**:

- **4px scale** (4, 8, 12, 16, 24, 32, 48, 64): Modern, tight designs, dense information
- **8px scale** (8, 16, 24, 32, 48, 64, 96): Spacious designs, marketing sites
- **Modular scale** (1em, 1.25em, 1.5em, 2em, 3em): Typography-driven designs

### Principle: Intentionality

**WHY**: Every visual decision should have a reason. Arbitrary choices create inconsistency.

**Decision Framework: Color Purpose**:

- **Semantic colors**: Status indicators, call-to-action buttons, alerts
- **Neutral colors**: Text hierarchy, borders, backgrounds

### Principle: Coherence

**WHY**: Consistent patterns reduce cognitive load. Users learn once, apply everywhere.

**Button States Example**: All buttons share same state pattern (hover, active, focus).

## Token Systems

### Token Philosophy

**Tokens are variables with purpose**. They enable:

1. **Consistency** - reuse same values
2. **Maintainability** - change once, update everywhere
3. **Theming** - swap token values for dark mode, brand variants
4. **Scale** - add new components using existing tokens

### Decision Framework: Token Structure

**Flat Tokens** (Small Projects): <10 components, single theme, small team

**Semantic Tokens** (Medium Projects): Growing component library, need theming, multiple developers

**Tiered Tokens** (Large Projects): Design system, multi-brand, accessibility variations

## Typography Decision Framework

### When to use System Fonts

**Use when**: Performance critical, rapid prototyping, native app feel

### When to use Custom Fonts

**Use when**: Brand identity critical, marketing sites, design system

## Layout Decision Framework

### Grid vs Flexbox

**Grid**: 2D layouts (dashboards, complex forms)

**Flexbox**: 1D layouts (navigation, cards, buttons)

### Responsive Design Decision Framework

**Mobile-First**: Content-focused sites, broad audience, mobile traffic >50%

**Desktop-First**: Complex dashboards, B2B tools, desktop-primary users

### Breakpoint Decision Framework

**Minimal (3 breakpoints)**: Simple layouts, rapid prototyping

**Standard (5 breakpoints)**: Production sites, design systems, broad device support

## State Design Patterns

### The 7 Essential States

Every interactive component needs these states designed:

1. **Default** - Initial appearance
2. **Hover** - Mouse over (desktop only)
3. **Active** - Being clicked/pressed
4. **Focus** - Keyboard navigation (CRITICAL for accessibility)
5. **Disabled** - Cannot be interacted with
6. **Loading** - Operation in progress
7. **Error** - Validation failed or operation error

### Loading States

**Skeleton screens**: When content structure is known (cards, lists, tables)

**Spinners**: When content structure unknown (initial page load, indeterminate operations)

**Progress bars**: When progress is measurable (file uploads, multi-step forms)

### Focus State (Accessibility Critical)

**ALWAYS visible**: Never remove focus outline without replacement. Use `:focus-visible` for custom but visible focus indicators.

## Design System Checklist

**Foundation (Required)**:

- [ ] Spacing scale defined (4px, 8px, or modular)
- [ ] Color system (semantic + neutral + status)
- [ ] Typography scale (sizes, weights, line heights)
- [ ] Border radius values (0, 4px, 8px, 16px, full)

**Layout (Required)**:

- [ ] Breakpoints defined and documented
- [ ] Grid system or flexbox patterns
- [ ] Container max-widths
- [ ] Responsive strategy (mobile-first or desktop-first)

**States (Required)**:

- [ ] All 7 states designed for buttons
- [ ] Focus states highly visible
- [ ] Loading patterns chosen
- [ ] Error states designed

**Accessibility (Required)**:

- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 large text)
- [ ] Focus indicators visible
- [ ] Touch targets ≥44x44px
- [ ] Text resizable to 200% without loss
