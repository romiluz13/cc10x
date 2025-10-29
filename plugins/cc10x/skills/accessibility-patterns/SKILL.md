---
name: accessibility-patterns
description: Ensures WCAG 2.1 AA compliance with semantic HTML, proper ARIA labeling, keyboard navigation, screen reader support, color contrast requirements, and focus management. Use when building UI components for accessibility compliance, reviewing interfaces for WCAG violations, auditing frontend code for a11y issues, implementing keyboard navigation, or ensuring screen reader compatibility. Provides accessibility checklists, ARIA pattern guides, semantic HTML templates, and remediation strategies for common violations. Loaded by the analysis-ux-accessibility subagent during the REVIEW workflow or by the orchestrator when accessibility compliance is needed. Critical for customer-facing applications, enterprise software, government systems, or any application requiring legal compliance.
---

# Accessibility Patterns

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: Accessibility Patterns
- **Purpose**: Ensure applications are usable by everyone
- **When**: Accessibility audits, WCAG compliance checks
- **Core Rule**: Keyboard-only navigation must work for all features
- **Sections Available**: WCAG 2.1 Quick Checks, ARIA Patterns, Keyboard Nav, Screen Readers

---

### Stage 2: Quick Reference

#### WCAG 2.1 Level AA Quick Checks

```
Accessibility Checklist:
- [ ] All interactive elements keyboard accessible?
- [ ] All images have alt text?
- [ ] Color contrast 4.5:1 for text?
- [ ] All form inputs have labels?
- [ ] Focus indicators visible?
- [ ] No keyboard traps?
- [ ] Semantic HTML used (not div soup)?
```

#### Critical Accessibility Patterns

**Keyboard Navigation**:
```tsx
// Div as button (not keyboard accessible)
<div onClick={handleClick}>Submit</div>

// Proper button (keyboard accessible)
<button onClick={handleClick}>Submit</button>

// Custom element with keyboard support
<span
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') handleClick();
  }}
>
  Submit
</span>
```

**Alt Text**:
```tsx
// Missing alt text
<img src="logo.png" />

// Decorative image with alt text
<img src="decoration.png" alt="decoration" />

// Descriptive alt text
<img src="logo.png" alt="Company name logo" />

// Decorative image hidden
<img src="decoration.png" alt="" aria-hidden="true" />
```

**Form Labels**:
```tsx
// No label
<input type="text" placeholder="Email" />

// Proper label
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Or aria-label
<input type="email" aria-label="Email address" />
```

**Color Contrast**:
```css
/* Low contrast (3.2:1) */
color: #7B7B7B;
background: #CCCCCC;

/* WCAG AA compliant (4.5:1) */
color: #5A5A5A;
background: #FFFFFF;
```

---

### Stage 3: Detailed Guide

For the full detailed guidance, see [reference/accessibility-detailed.md](reference/accessibility-detailed.md).

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

**Remember**: Accessibility is not optional. 15% of the world has a disability!

