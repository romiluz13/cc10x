# Accessibility Pattern Library

## Keyboard Navigation

**Understand accessibility requirements first, then check**:

### Keyboard Accessible Buttons

```tsx
// BAD - Div as button (flag if prevents access)
<div onClick={handleClick}>Submit</div>

// GOOD - Proper button (aligned with project pattern)
<button onClick={handleClick}>Submit</button>

// GOOD - Custom element with keyboard support (aligned with project pattern)
<span
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Submit
</span>
```

### Keyboard Navigation Order

```tsx
// BAD - Tab order not logical (flag if prevents navigation)
<div>
  <button tabIndex={3}>Third</button>
  <button tabIndex={1}>First</button>
  <button tabIndex={2}>Second</button>
</div>

// GOOD - Logical tab order (aligned with project pattern)
<div>
  <button tabIndex={0}>First</button>
  <button tabIndex={0}>Second</button>
  <button tabIndex={0}>Third</button>
</div>
```

### Focus Trapping (Modals)

```tsx
// Focus trap in modal (aligned with project pattern)
function Modal({ children, onClose }) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== "Tab") return;
      const focusable = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
      );
      if (!focusable?.length) return;

      const first = focusable[0] as HTMLElement;
      const last = focusable[focusable.length - 1] as HTMLElement;

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    document.addEventListener("keydown", handleTab);
    return () => document.removeEventListener("keydown", handleTab);
  }, []);

  return <div ref={modalRef}>{children}</div>;
}
```

## Screen Reader Support

**Understand accessibility requirements first, then check**:

### Form Labels

```tsx
// BAD - Missing label (flag if prevents understanding)
<input type="text" name="email" />

// GOOD - Proper label (aligned with project pattern)
<label htmlFor="email">Email</label>
<input type="text" id="email" name="email" />

// GOOD - aria-label (aligned with project pattern)
<input type="text" aria-label="Email" name="email" />
```

### Alt Text

```tsx
// BAD - Missing alt text (flag if prevents understanding)
<img src="upload-icon.png" />

// GOOD - Descriptive alt text (aligned with project pattern)
<img src="upload-icon.png" alt="Upload file" />

// GOOD - Decorative image (aligned with project pattern)
<img src="decoration.png" alt="" role="presentation" />
```

### Status Announcements

```tsx
// Status announcement (aligned with project pattern)
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {statusMessage}
</div>

// Progress announcement (aligned with project pattern)
<div
  role="progressbar"
  aria-valuenow={progress}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="Upload progress"
>
  {progress}%
</div>
```

## Color Contrast

**Understand accessibility requirements first, then check**:

### Contrast Ratios

- **Normal text**: 4.5:1 (WCAG AA), 7:1 (WCAG AAA)
- **Large text**: 3:1 (WCAG AA), 4.5:1 (WCAG AAA)
- **UI components**: 3:1 (WCAG AA)

### Color-Only Indicators

```tsx
// BAD - Color-only indicator (flag if prevents understanding)
<span style={{ color: 'red' }}>Error</span>

// GOOD - Color + text/icon (aligned with project pattern)
<span style={{ color: 'red' }}>
  <Icon name="error" aria-hidden="true" />
  Error: Invalid file type
</span>
```

## Focus Management

**Understand accessibility requirements first, then check**:

### Focus Indicators

```css
/* Focus indicator (aligned with project pattern) */
button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}
```

### Focus Restoration

```tsx
// Focus restoration after modal closes (aligned with project pattern)
function Modal({ children, onClose }) {
  const triggerRef = useRef<HTMLButtonElement>(null);

  const handleClose = () => {
    onClose();
    // Restore focus to trigger
    setTimeout(() => triggerRef.current?.focus(), 0);
  };

  return (
    <>
      <button ref={triggerRef} onClick={handleOpen}>
        Open Modal
      </button>
      <Modal onClose={handleClose}>{children}</Modal>
    </>
  );
}
```

## Semantic HTML

**Understand accessibility requirements first, then check**:

### Semantic Elements

```tsx
// BAD - Div soup (flag if prevents understanding)
<div onClick={handleClick}>
  <div>Click me</div>
</div>

// GOOD - Semantic HTML (aligned with project pattern)
<button onClick={handleClick}>Click me</button>

// BAD - Generic div for navigation
<div>
  <div>Home</div>
  <div>About</div>
</div>

// GOOD - Semantic nav (aligned with project pattern)
<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>
```

### ARIA Roles

```tsx
// ARIA roles (aligned with project pattern)
<div role="button" tabIndex={0} onClick={handleClick}>
  Custom Button
</div>

<div role="alert" aria-live="assertive">
  Error message
</div>

<div role="dialog" aria-labelledby="modal-title">
  <h2 id="modal-title">Modal Title</h2>
  {children}
</div>
```
