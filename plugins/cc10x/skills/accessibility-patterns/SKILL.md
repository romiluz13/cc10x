---
name: accessibility-patterns
description: Ensures WCAG 2.1 AA compliance with semantic HTML, proper ARIA labeling, keyboard navigation, screen reader support, color contrast requirements, and focus management. Use when building UI components for accessibility compliance, reviewing interfaces for WCAG violations, auditing frontend code for a11y issues, implementing keyboard navigation, or ensuring screen reader compatibility. Provides accessibility checklists, ARIA pattern guides, semantic HTML templates, and remediation strategies for common violations. Loaded by accessibility-reviewer agent during REVIEW workflow or master orchestrator when accessibility compliance needed. Critical for customer-facing applications, enterprise software, government systems, or any application requiring legal compliance.
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
- [ ] Color contrast â4.5:1 for text?
- [ ] All form inputs have labels?
- [ ] Focus indicators visible?
- [ ] No keyboard traps?
- [ ] Semantic HTML used (not div soup)?
```

#### Critical Accessibility Patterns

**Keyboard Navigation**:
```tsx
// âDiv as button (not keyboard accessible)
<div onClick={handleClick}>Submit</div>

// âProper button (keyboard accessible)
<button onClick={handleClick}>Submit</button>

// âCustom element with keyboard support
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
// âMissing alt text
<img src="logo.png" />

// âDecorative image with alt text
<img src="decoration.png" alt="decoration" />

// âDescriptive alt text
<img src="logo.png" alt="Company name logo" />

// âDecorative image hidden
<img src="decoration.png" alt="" aria-hidden="true" />
```

**Form Labels**:
```tsx
// âNo label
<input type="text" placeholder="Email" />

// âProper label
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// âOr aria-label
<input type="email" aria-label="Email address" />
```

**Color Contrast**:
```css
/* âLow contrast (3.2:1) */
color: #7B7B7B;
background: #CCCCCC;

/* âWCAG AA compliant (4.5:1) */
color: #5A5A5A;
background: #FFFFFF;
```

---

### Stage 3: Detailed Guide

## WCAG 2.1 Level AA Compliance

### 1. Perceivable

#### 1.1.1 Non-text Content (Level A)
All images, icons, and non-text content must have text alternatives.

```tsx
// Images
<img src="chart.png" alt="Sales chart showing 20% growth in Q4" />

// Icons
<button>
  <TrashIcon aria-hidden="true" />
  <span>Delete</span>
</button>

// Or with aria-label
<button aria-label="Delete item">
  <TrashIcon />
</button>

// Decorative images
<img src="divider.png" alt="" role="presentation" />
```

#### 1.4.3 Contrast (Minimum) (Level AA)
- Normal text: 4.5:1 contrast ratio
- Large text (18pt+ or 14pt+ bold): 3:1 contrast ratio

**Testing**:
```bash
# Use browser dev tools:
# Chrome DevTools âElements âStyles âColor picker âContrast ratio
```

**Common Issues**:
```css
/* âToo low */
color: #999; background: #fff; /* 2.8:1 */

/* âWCAG AA compliant */
color: #767676; background: #fff; /* 4.5:1 */
color: #fff; background: #007bff; /* 4.5:1 */
```

### 2. Operable

#### 2.1.1 Keyboard (Level A)
All functionality available via keyboard.

**Interactive Elements**:
```tsx
// âClick-only
<div onClick={handleAction}>Action</div>

// âKeyboard accessible
<button onClick={handleAction}>Action</button>

// âCustom with keyboard
<div
  role="button"
  tabIndex={0}
  onClick={handleAction}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleAction();
    }
  }}
>
  Action
</div>
```

**Modal Focus Management**:
```tsx
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef();
  const previousFocusRef = useRef();

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement;
      modalRef.current?.focus();
    } else {
      previousFocusRef.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
    >
      {children}
    </div>
  );
}
```

#### 2.4.7 Focus Visible (Level AA)
Focus indicators must be visible.

```css
/* âRemoving focus outline */
*:focus {
  outline: none;
}

/* âCustom focus indicator */
button:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

/* âOr use :focus-visible */
button:focus-visible {
  outline: 2px solid #007bff;
}
```

### 3. Understandable

#### 3.3.2 Labels or Instructions (Level A)
Form inputs must have clear labels.

```tsx
// âPlaceholder as label
<input type="text" placeholder="Email" />

// âProper label
<label htmlFor="email">Email address</label>
<input id="email" type="email" />

// âWith description
<label htmlFor="password">
  Password
  <span className="hint">Must be at least 12 characters</span>
</label>
<input
  id="password"
  type="password"
  aria-describedby="password-hint"
/>
<span id="password-hint">
  Must contain uppercase, lowercase, number, and symbol
</span>
```

#### 3.3.3 Error Suggestion (Level AA)
Error messages must be clear and suggest corrections.

```tsx
// âVague error
{errors.email && <span>Invalid</span>}

// âClear error with suggestion
{errors.email && (
  <span role="alert">
    Please enter a valid email address (e.g., name@example.com)
  </span>
)}
```

### 4. Robust

#### 4.1.2 Name, Role, Value (Level A)
UI components must have accessible names and roles.

```tsx
// âNo accessible name
<button>
  <Icon name="close" />
</button>

// âWith accessible name
<button aria-label="Close dialog">
  <Icon name="close" aria-hidden="true" />
</button>

// âCustom component
<div
  role="button"
  aria-pressed={isActive}
  tabIndex={0}
>
  Toggle
</div>
```

## ARIA Patterns

### Live Regions

```tsx
// Announce dynamic content to screen readers
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Urgent announcements
<div aria-live="assertive">
  {errorMessage}
</div>
```

### Landmark Roles

```tsx
// Use semantic HTML
<header>...</header>
<nav>...</nav>
<main>...</main>
<aside>...</aside>
<footer>...</footer>

// Or ARIA roles
<div role="banner">...</div>
<div role="navigation">...</div>
<div role="main">...</div>
```

## Common A11y Anti-Patterns

```tsx
// ð© Div soup
<div onClick={handler}>Click me</div>

// ð© Missing alt
<img src="photo.jpg" />

// ð© Removing outlines
*:focus { outline: none; }

// ð© Placeholder as label
<input placeholder="Name" />

// ð© Low contrast
color: #999; background: #eee;

// ð© No keyboard support
<span onClick={handler}>Action</span>
```

## Testing Tools

```bash
# Automated testing
npm install --save-dev axe-core jest-axe

# Manual testing
# 1. Tab through entire page (keyboard only)
# 2. Use screen reader (NVDA, JAWS, VoiceOver)
# 3. Check contrast with browser dev tools
# 4. Run axe DevTools extension

# Lighthouse audit
npx lighthouse https://example.com --only-categories=accessibility
```

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

**Remember**: Accessibility is not optional. 15% of the world has a disability!
