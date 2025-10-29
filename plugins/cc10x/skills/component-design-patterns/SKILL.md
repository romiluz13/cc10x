---
name: component-design-patterns
description: Focused component design guidance. Thin wrapper around the Component section of design-patterns with a compact checklist and examples. Used by component-builder, planning-workflow, and code-reviewer.
---

# Component Design Patterns (Focused)

## Progressive Loading Stages

### Stage 1: Metadata
- Purpose: Design components that are reusable, composable, accessible, and testable
- When: Building UI components, refactoring, planning component APIs
- Core Rule: Single responsibility; composition over inheritance; accessibility by default

---

### Stage 2: Quick Reference

#### Component Checklist
```
Structure & API
- [ ] Single responsibility (one reason to change)
- [ ] Clear props interface (typed + documented)
- [ ] Sensible defaults and minimal required props
- [ ] Controlled vs uncontrolled usage is explicit

Reusability & Composition
- [ ] Composition patterns (slots, render props, compound components) when appropriate
- [ ] No hardcoded values or strings; use tokens/config
- [ ] Styles themable and responsive

Quality & a11y
- [ ] Keyboard navigation and focus states
- [ ] ARIA roles/labels as needed
- [ ] Performance: memoization where it matters; avoid unnecessary re-renders
- [ ] Tests exist (unit + basic interactions)
```

#### Examples
**Typed Props**
```ts
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'link';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

**Compound Components**
```tsx
<Button>
  <Button.Icon />
  <Button.Label>Save</Button.Label>
</Button>
```

**Controlled vs Uncontrolled**
- Controlled: value, onChange; Uncontrolled: defaultValue, ref

---

### Stage 3: Review Procedure
1) Inspect props shape and defaults
2) Verify a11y and interaction states
3) Check reusability and composition opportunities
4) Confirm tests cover interactions and error states

---

### Stage 4: Outputs
- Component Review Notes (decisions, risks, follow-ups)
- Checklist outcomes and any action items

---

### Stage 5: Links
- See also: design-patterns (Component section), ux-patterns, accessibility-patterns, test-driven-development

