name: ux-patterns
description: Evaluates user experience quality including loading states, error handling, form usability, interaction design, user feedback mechanisms, and overall user flow coherence. Use when reviewing user-facing interfaces for UX improvements, designing user flows, improving error messages, analyzing form usability, or assessing interaction patterns. Identifies UX friction points, confusing interfaces, missing loading indicators, poor error messages, and interaction design issues. Loaded by the analysis-ux-accessibility subagent during the REVIEW workflow or by the orchestrator when UX analysis is needed. Complements risk-analysis Stage 4 (User Experience & Human Factors) with specific UX improvement patterns and techniques. Critical for customer-facing features where user satisfaction drives adoption.

# UX Patterns

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: UX Patterns
- **Purpose**: Ensure delightful, intuitive user experiences
- **When**: UX analysis, interaction design review, usability testing
- **Core Rule**: Never leave users guessing what's happening
- **Sections Available**: Loading States, Error Handling, Form UX, Feedback Patterns

---

### Stage 2: Quick Reference

#### UX Quick Checks

```
UX Checklist:
- [ ] Loading states for all async operations?
- [ ] User-friendly error messages (not technical)?
- [ ] Form validation inline (not just on submit)?
- [ ] Touch targets 44x44px on mobile?
- [ ] Consistent interaction patterns throughout?
- [ ] Clear feedback for all actions?
```

#### Critical UX Patterns

**Loading States**:
```typescript
// No loading state (users see blank screen)
function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => { fetchUsers().then(setUsers); }, []);
  return users.map(u => <User key={u.id} user={u} />);
}

// With loading state and skeleton
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchUsers()
      .then(setUsers)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Skeleton count={5} />;
  return users.map(u => <User key={u.id} user={u} />);
}
```

**Error Messages**:
```typescript
// Technical error (users confused)
catch (error) {
  alert(error.message); // "ERR_CONNECTION_REFUSED"
}

// User-friendly error (users understand + can recover)
catch (error) {
  showNotification({
    type: 'error',
    title: "Couldn't load your profile",
    message: "Please check your internet connection and try again.",
    action: { label: "Retry", onClick: retry }
  });
}
```

**Inline Form Validation**:
```typescript
// Validation only on submit (frustrating!)
<form onSubmit={handleSubmit}>
  <input name="email" />
  {/* User fills entire form, clicks submit, sees all errors at once */}
</form>

// Inline validation as user types
<input
  name="email"
  onChange={(e) => validateEmail(e.target.value)}
  onBlur={() => setTouched(true)}
/>
{touched && errors.email && (
  <span className="error">{errors.email}</span>
)}
```

---

### Stage 3: Detailed Guide

## Core UX Principles

### 1. Provide Immediate Feedback

Users need to know their action was registered.

**Loading States**:
- Show spinners/skeletons for async operations
- Use optimistic updates for quick actions
- Disable buttons while processing

**Action Feedback**:
```typescript
// Button states
<button
  disabled={isSubmitting}
  onClick={handleSubmit}
>
  {isSubmitting ? 'Saving...' : 'Save'}
</button>

// Success feedback
const [saved, setSaved] = useState(false);
<button onClick={() => {
  save();
  setSaved(true);
  setTimeout(() => setSaved(false), 2000);
}}>
  {saved ? 'Saved!' : 'Save'}
</button>
```

### 2. Error Handling

**User-Friendly Messages**:
```typescript
// Map technical errors to user-friendly messages
const errorMessages = {
  'NETWORK_ERROR': 'Unable to connect. Please check your internet connection.',
  'UNAUTHORIZED': 'Please log in to continue.',
  'NOT_FOUND': 'We couldn't find what you're looking for.',
  'SERVER_ERROR': 'Something went wrong on our end. Please try again.',
  'VALIDATION_ERROR': 'Please check your input and try again.'
};

function handleError(error) {
  const message = errorMessages[error.code] || errorMessages.SERVER_ERROR;
  showNotification({ type: 'error', message });
}
```

**Error Placement**:
- Show errors near the relevant field/action
- Use color + icon (not color alone)
- Provide recovery actions when possible

### 3. Form Design

**Inline Validation**:
```typescript
// Validate as user types (debounced)
const [email, setEmail] = useState('');
const [emailError, setEmailError] = useState('');

const validateEmail = useDebounce((value) => {
  if (!value) setEmailError('Email is required');
  else if (!isValidEmail(value)) setEmailError('Please enter a valid email');
  else setEmailError('');
}, 500);

<input
  value={email}
  onChange={(e) => {
    setEmail(e.target.value);
    validateEmail(e.target.value);
  }}
  aria-invalid={!!emailError}
  aria-describedby="email-error"
/>
{emailError && <span id="email-error" role="alert">{emailError}</span>}
```

**Clear Labels**:
```tsx
// Placeholder as label
<input type="text" placeholder="Email" />

// Proper label + placeholder
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  placeholder="name@example.com"
/>
```

### 4. Mobile Responsiveness

**Touch Targets**:
- Minimum 44x44px (iOS HIG)
- Adequate spacing between tappable elements

**Responsive Design**:
```css
/* Fixed widths */
.container { width: 1200px; }

/* Flexible layout */
.container {
  max-width: 1200px;
  width: 100%;
  padding: 0 1rem;
}

/* Mobile-first breakpoints */
@media (min-width: 768px) {
  .container { padding: 0 2rem; }
}
```

### 5. Consistency

**Design System**:
- Use consistent button styles
- Maintain uniform spacing
- Follow established patterns

**Interaction Patterns**:
- Same actions should work the same everywhere
- Predictable navigation
- Consistent terminology

## Common UX Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| No loading state | Users think app is broken | Add spinners/skeletons |
| Technical errors | Users confused | User-friendly messages |
| Validation on submit only | Frustrating form experience | Inline validation |
| Small touch targets | Hard to tap on mobile | Minimum 44x44px |
| Inconsistent patterns | Confusing navigation | Use design system |
| No action feedback | Users click multiple times | Show processing state |

## References

- [Nielsen's 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Material Design](https://material.io/design)

---

**Remember**: Users don't read error messages. They should never need to!
