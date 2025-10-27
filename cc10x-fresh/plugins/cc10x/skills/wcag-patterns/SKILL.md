---
name: wcag-patterns
description: WCAG 2.1 accessibility patterns for keyboard navigation, screen readers, and inclusive design. Use when reviewing accessibility compliance.
allowed-tools: Read, Grep
---

# WCAG Accessibility Patterns

Web Content Accessibility Guidelines (WCAG 2.1) compliance patterns.

## Keyboard Navigation (2.1.1, 2.1.2)

### All Interactive Elements
```html
<!-- ✅ Keyboard accessible -->
<button onClick={handleClick}>Click Me</button>
<a href="/page">Link</a>

<!-- ❌ Not keyboard accessible -->
<div onClick={handleClick}>Clickable</div>
```

### Focus Management
```typescript
// ✅ Trap focus in modal
function Modal({ onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const firstFocusable = modalRef.current?.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    (firstFocusable as HTMLElement)?.focus();
  }, []);
  
  return (
    <div ref={modalRef} role="dialog" aria-modal="true">
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

### Skip Links
```html
<!-- ✅ Skip to main content -->
<a href="#main" class="skip-link">Skip to main content</a>
<nav>...</nav>
<main id="main">...</main>
```

## Screen Reader Support (4.1.2, 4.1.3)

### Semantic HTML
```html
<!-- ✅ Semantic -->
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>
<main>
  <article>
    <h1>Title</h1>
    <p>Content</p>
  </article>
</main>
<footer>...</footer>

<!-- ❌ Non-semantic -->
<div class="nav">
  <div class="link">Home</div>
</div>
<div class="content">
  <div class="title">Title</div>
</div>
```

### ARIA Labels
```html
<!-- ✅ Labeled button -->
<button aria-label="Close dialog">
  <XIcon />
</button>

<!-- ✅ Form labels -->
<label for="email">Email</label>
<input id="email" type="email" />

<!-- ✅ Fieldset for groups -->
<fieldset>
  <legend>Shipping Address</legend>
  <input type="text" name="address" />
  <input type="text" name="city" />
</fieldset>
```

### ARIA Roles
```html
<!-- ✅ Custom components with roles -->
<div role="alert" aria-live="polite">
  Your changes have been saved
</div>

<div role="tablist">
  <button role="tab" aria-selected="true">Tab 1</button>
  <button role="tab" aria-selected="false">Tab 2</button>
</div>

<div role="tabpanel">Content</div>
```

### Alt Text (1.1.1)
```html
<!-- ✅ Descriptive alt text -->
<img src="chart.png" alt="Bar chart showing 23% increase in sales" />

<!-- ✅ Decorative images -->
<img src="decoration.png" alt="" role="presentation" />

<!-- ❌ Missing or generic alt -->
<img src="photo.png" alt="image" />
```

## Visual Accessibility (1.4.3, 1.4.11)

### Color Contrast
```css
/* ✅ WCAG AA compliant (4.5:1 for normal text) */
.text {
  color: #333333; /* on white background */
}

/* ✅ WCAG AAA compliant (7:1) */
.text {
  color: #000000; /* on white background */
}

/* ❌ Insufficient contrast */
.text {
  color: #cccccc; /* on white - only 1.6:1 */
}
```

### Non-Color Indicators
```html
<!-- ❌ Color only -->
<span style="color: red">Error</span>

<!-- ✅ Icon + text + color -->
<span style="color: red">
  <ErrorIcon aria-hidden="true" />
  Error: Please check your input
</span>
```

### Focus Indicators
```css
/* ✅ Clear focus indicator */
button:focus-visible {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

/* ❌ Removed focus */
button:focus {
  outline: none; /* NEVER DO THIS */
}
```

## Content Structure (1.3.1, 2.4.6)

### Heading Hierarchy
```html
<!-- ✅ Proper hierarchy -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
  <h2>Another Section</h2>

<!-- ❌ Skipped levels -->
<h1>Page Title</h1>
<h4>Section</h4> <!-- Skipped h2, h3 -->
```

### Landmarks
```html
<!-- ✅ ARIA landmarks -->
<header role="banner">
  <nav role="navigation">...</nav>
</header>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

### Link Purpose (2.4.4)
```html
<!-- ❌ Ambiguous -->
<a href="/docs">Click here</a>

<!-- ✅ Clear purpose -->
<a href="/docs">Read the documentation</a>
```

## Forms & Input (3.3.1, 3.3.2)

### Error Identification
```html
<!-- ✅ Clear error messages -->
<label for="email">Email</label>
<input
  id="email"
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">
  Please enter a valid email address
</span>
```

### Required Fields
```html
<!-- ✅ Mark required -->
<label for="name">
  Name <span aria-label="required">*</span>
</label>
<input id="name" type="text" required aria-required="true" />
```

### Input Assistance
```html
<!-- ✅ Help text -->
<label for="password">Password</label>
<input
  id="password"
  type="password"
  aria-describedby="password-help"
/>
<span id="password-help">
  Must be at least 8 characters with 1 number
</span>
```

## Dynamic Content

### Live Regions
```html
<!-- ✅ Announce updates to screen readers -->
<div role="status" aria-live="polite" aria-atomic="true">
  Loading...
</div>

<div role="alert" aria-live="assertive">
  Error: Form submission failed
</div>
```

### Loading States
```html
<!-- ✅ Accessible loading indicator -->
<button disabled aria-busy="true">
  <span class="spinner" aria-hidden="true"></span>
  <span class="sr-only">Loading, please wait</span>
  Submitting...
</button>
```

## Tables (1.3.1)

### Data Tables
```html
<!-- ✅ Accessible table -->
<table>
  <caption>Monthly Sales Data</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Sales</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>$10,000</td>
    </tr>
  </tbody>
</table>
```

## Media (1.2.1, 1.2.2)

### Video Captions
```html
<!-- ✅ Captions and transcripts -->
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English" />
</video>
<details>
  <summary>Transcript</summary>
  <p>Video transcript text...</p>
</details>
```

## Mobile Accessibility

### Touch Targets (2.5.5)
```css
/* ✅ Minimum 44x44px */
button, a, input[type="checkbox"] {
  min-width: 44px;
  min-height: 44px;
  padding: 0.75rem;
}
```

### Zoom Support (1.4.4)
```html
<!-- ✅ Allow zoom -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- ❌ Disable zoom -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
```

## WCAG Compliance Levels

### Level A (Minimum)
- Keyboard access
- Alt text
- Color not sole indicator
- Captions for video

### Level AA (Target)
- Color contrast 4.5:1
- Resize text to 200%
- Multiple ways to find content
- Clear headings

### Level AAA (Enhanced)
- Color contrast 7:1
- Audio descriptions
- Sign language
- Reading level

## Testing Tools

### Manual Tests
```bash
# Tab through entire interface
# Use screen reader (NVDA/VoiceOver/JAWS)
# Test with keyboard only
# Check contrast ratios
# Validate HTML
```

### Automated Tests
```bash
# axe-core
npm install --save-dev @axe-core/cli
axe https://example.com

# Lighthouse
lighthouse https://example.com --only-categories=accessibility

# Pa11y
pa11y https://example.com
```

## Accessibility Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Alt text on all images
- [ ] Color contrast >= 4.5:1 (AA) or 7:1 (AAA)
- [ ] Proper heading hierarchy
- [ ] Form labels present
- [ ] Error messages clear
- [ ] ARIA attributes correct
- [ ] Screen reader tested
- [ ] Keyboard navigation tested
- [ ] Touch targets >= 44x44px
- [ ] Zoom allowed
- [ ] No keyboard traps

## Common ARIA Patterns

### Button
```html
<button type="button" aria-pressed="false">Toggle</button>
```

### Menu
```html
<button aria-haspopup="true" aria-expanded="false">Menu</button>
<ul role="menu">
  <li role="menuitem">Item 1</li>
</ul>
```

### Tabs
```html
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">
    Tab 1
  </button>
</div>
<div role="tabpanel" id="panel-1">Content</div>
```

## Resources

- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Practices: https://www.w3.org/WAI/ARIA/apg/
- Contrast Checker: https://webaim.org/resources/contrastchecker/

