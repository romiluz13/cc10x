---
name: ui-design
description: Visual/UI design guidance complementary to ux-patterns. Covers tokens, layout, typography, color, states, responsiveness, and theming. Used by component-builder and planning-workflow when visual fidelity matters.
---

# UI Design (Visual Systems)

## Progressive Loading Stages

### Stage 1: Metadata
- Purpose: Create visually consistent, accessible, and scalable interfaces
- When: Designing new UI, refactoring visuals, or establishing component styles
- Core Rule: Ship consistent tokens first; components inherit from tokens

---

### Stage 2: Quick Reference

#### UI Checklist
```
Design Tokens
- [ ] Spacing scale (4/8 px or consistent modular scale)
- [ ] Typography scale (font sizes, weights, line heights)
- [ ] Color system (semantic roles + WCAG contrast)
- [ ] Radii, borders, shadows, motion

Layout & Responsiveness
- [ ] Grid and breakpoints defined (xs/sm/md/lg/xl)
- [ ] Containers, gutters, and max widths consistent
- [ ] Mobile-first; test at three breakpoints

States & Interactions
- [ ] Hover/active/focus/disabled/pressed states
- [ ] Focus ring visible and accessible
- [ ] Loading, empty, error, and success states

Theming & i18n
- [ ] Light/dark mode tokens
- [ ] RTL/LTR support assumptions captured
- [ ] Dynamic density (comfortable/compact)
```

#### Examples
**CSS Variables (Tokens)**
```css
:root {
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --font-sm: 12px; --font-md: 14px; --font-lg: 16px; --line: 1.5;
  --fg: #111; --fg-muted: #444; --bg: #fff; --accent: #3b82f6;
}
```

**Buttons from Tokens**
```css
.button {
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-md);
  color: var(--fg);
  background: var(--bg);
  border: 1px solid var(--fg-muted);
  border-radius: 8px;
}
.button.primary { background: var(--accent); color: white; }
.button:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
```

**Contrast**
- Body text  4.5:1; Large text  3:1 (WCAG AA)

---

### Stage 3: Review Procedure
1) Confirm tokens exist; avoid ad-hoc colors/sizes
2) Verify states (hover/active/focus/disabled/loading)
3) Check responsiveness at xs/sm/lg
4) Validate contrast and a11y affordances

---

### Stage 4: Outputs
- UI Decision Record (tokens used, state definitions, responsive behavior)
- Screenshots or storybook refs at three breakpoints

---

### Stage 5: Links
- See also: ux-patterns (UX behaviors), accessibility-patterns (a11y), design-patterns (Component)

