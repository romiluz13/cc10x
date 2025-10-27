---
name: ux-patterns
description: User experience patterns and best practices for intuitive, user-friendly interfaces. Use when reviewing UX or designing user flows.
allowed-tools: Read, Grep
---

# UX Patterns & Best Practices

Proven patterns for creating excellent user experiences.

## User Feedback

### Loading States
```typescript
// ❌ No feedback
<button onClick={handleSubmit}>Submit</button>

// ✅ Clear loading state
<button onClick={handleSubmit} disabled={isLoading}>
  {isLoading ? 'Submitting...' : 'Submit'}
</button>
```

### Error Messages
```typescript
// ❌ Technical error
"Error: ECONNREFUSED 127.0.0.1:5432"

// ✅ User-friendly error
"We couldn't save your changes. Please check your connection and try again."
```

### Success Confirmation
```typescript
// ❌ Silent success
await saveData();

// ✅ Clear confirmation
await saveData();
showToast('Your changes have been saved', 'success');
```

## Form UX

### Inline Validation
```typescript
// ✅ Real-time validation
<input
  type="email"
  value={email}
  onChange={e => {
    setEmail(e.target.value);
    setError(validateEmail(e.target.value));
  }}
  aria-invalid={!!error}
  aria-describedby="email-error"
/>
{error && <span id="email-error" role="alert">{error}</span>}
```

### Clear Required Fields
```typescript
// ✅ Mark required fields
<label>
  Email <span aria-label="required">*</span>
  <input type="email" required />
</label>
```

### Input Helpers
```typescript
// ✅ Provide format hints
<label>
  Phone Number
  <input type="tel" placeholder="(555) 123-4567" />
  <span className="help-text">Format: (XXX) XXX-XXXX</span>
</label>
```

## Navigation & Layout

### Breadcrumbs
```typescript
// ✅ Show user location
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Laptop</li>
  </ol>
</nav>
```

### Clear CTAs (Call to Action)
```typescript
// ❌ Vague
<button>Click Here</button>

// ✅ Action-oriented
<button>Download Free Trial</button>
<button>Add to Cart</button>
<button>Start Your Free Trial</button>
```

### Visual Hierarchy
```css
/* ✅ Clear hierarchy */
h1 { font-size: 2.5rem; font-weight: 700; }
h2 { font-size: 2rem; font-weight: 600; }
h3 { font-size: 1.5rem; font-weight: 600; }
p { font-size: 1rem; line-height: 1.6; }
```

## Interaction Patterns

### Confirmation for Destructive Actions
```typescript
// ✅ Confirm before delete
<button onClick={() => {
  if (confirm('Are you sure you want to delete this item?')) {
    deleteItem();
  }
}}>
  Delete
</button>
```

### Progressive Disclosure
```typescript
// ✅ Show advanced options on demand
<details>
  <summary>Advanced Options</summary>
  <div>
    {/* Complex options */}
  </div>
</details>
```

### Keyboard Shortcuts
```typescript
// ✅ Add shortcuts for power users
useEffect(() => {
  function handleKeyPress(e: KeyboardEvent) {
    if ((e.metaKey || e.ctrlKey) && e.key === 's') {
      e.preventDefault();
      save();
    }
  }
  
  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, []);
```

## Mobile UX

### Touch Targets
```css
/* ✅ Minimum 44x44px touch targets */
button, a, input[type="checkbox"] {
  min-width: 44px;
  min-height: 44px;
}
```

### Responsive Design
```css
/* ✅ Mobile-first responsive */
.container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}
```

### Bottom Navigation (Mobile)
```typescript
// ✅ Easy thumb reach
<nav className="bottom-nav">
  <button>Home</button>
  <button>Search</button>
  <button>Profile</button>
</nav>
```

## Content UX

### Scannable Content
```markdown
✅ Good:
# Clear Heading
Short intro paragraph.

## Subsection with Bullet Points
- Key point 1
- Key point 2
- Key point 3

❌ Bad:
Long wall of text with no headings, bullets, or visual breaks...
```

### Meaningful Link Text
```html
<!-- ❌ Not accessible -->
<a href="/docs">Click here</a> to read our documentation.

<!-- ✅ Descriptive -->
Read our <a href="/docs">complete documentation</a>.
```

## Empty States

### Helpful Empty States
```typescript
// ❌ Just empty
<div className="orders">
  {orders.length === 0 && <p>No orders</p>}
</div>

// ✅ Actionable empty state
<div className="orders">
  {orders.length === 0 && (
    <div className="empty-state">
      <Icon name="shopping-bag" />
      <h3>No orders yet</h3>
      <p>When you place an order, it will appear here.</p>
      <button onClick={() => navigate('/shop')}>
        Start Shopping
      </button>
    </div>
  )}
</div>
```

## Micro-interactions

### Button Hover States
```css
button {
  background: #0066cc;
  transition: background 0.2s;
}

button:hover {
  background: #0052a3;
}

button:active {
  background: #003d7a;
  transform: translateY(1px);
}
```

### Focus Indicators
```css
/* ✅ Clear focus indicator */
*:focus-visible {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}
```

## Performance Perception

### Skeleton Screens
```typescript
// ✅ Show skeleton while loading
{isLoading ? (
  <SkeletonCard />
) : (
  <UserCard user={user} />
)}
```

### Optimistic Updates
```typescript
// ✅ Update UI immediately, rollback if fails
async function toggleLike() {
  setLiked(true); // Optimistic update
  setLikeCount(c => c + 1);
  
  try {
    await api.like(postId);
  } catch (error) {
    setLiked(false); // Rollback
    setLikeCount(c => c - 1);
    showError('Failed to like post');
  }
}
```

## Accessibility & UX

### Alt Text for Images
```html
<!-- ✅ Descriptive alt text -->
<img src="chart.png" alt="Sales increased 23% in Q4 2024" />
```

### Aria Labels for Icons
```html
<!-- ✅ Icon buttons with labels -->
<button aria-label="Close dialog">
  <CloseIcon />
</button>
```

## UX Writing

### Button Text
```typescript
// ❌ Generic
<button>OK</button>
<button>Submit</button>

// ✅ Specific
<button>Save Changes</button>
<button>Create Account</button>
<button>Download Report</button>
```

### Error Messages
```typescript
// ❌ Blame user
"You entered an invalid email"

// ✅ Helpful
"Please enter a valid email address (example@email.com)"
```

## Common UX Mistakes

❌ **Too Many Steps**: Simplify workflows
❌ **Hidden Navigation**: Make it obvious
❌ **No Feedback**: Always acknowledge actions
❌ **Unclear Errors**: Explain what went wrong and how to fix
❌ **Inconsistent Patterns**: Use consistent UI patterns
❌ **Tiny Touch Targets**: Minimum 44x44px
❌ **Auto-playing Media**: Let users control media
❌ **Disabled Copy**: Allow text selection

## UX Checklist

- [ ] Loading states for all async actions
- [ ] Error messages are user-friendly
- [ ] Success confirmations shown
- [ ] Forms have inline validation
- [ ] Required fields clearly marked
- [ ] CTAs are action-oriented
- [ ] Destructive actions require confirmation
- [ ] Touch targets >= 44x44px
- [ ] Mobile-responsive design
- [ ] Empty states are helpful
- [ ] Keyboard navigation works
- [ ] Focus indicators visible

## UX Testing Questions

1. Can users complete their task in < 3 clicks?
2. Do users know what will happen when they click?
3. Does the UI respond within 100ms?
4. Are error messages actionable?
5. Can users recover from mistakes easily?
