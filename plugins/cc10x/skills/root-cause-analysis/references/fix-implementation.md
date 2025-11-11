# Fix Implementation & Prevention

**Reference**: Part of `root-cause-analysis` skill. See main SKILL.md for overview.

## Root Cause Fixes (Functionality-Focused)

**CRITICAL**: Fix root causes that affect functionality. Fix at source, not at symptom.

## Fix Implementation Process

### 1. Understand Root Cause

**What is the root cause?**:

- How does it affect functionality?
- Why does it break functionality?
- What needs to change to fix functionality?

### 2. Plan Fix

**Plan fix that restores functionality**:

- Fix at source (not symptom)
- Minimal change (restore functionality)
- Test-driven (write test first)
- Verify functionality works

### 3. Implement Fix

**Apply fix**:

- Make minimal change
- Test functionality
- Verify fix works
- Check for regressions

### 4. Verify Fix

**Verify functionality works**:

- Run tests
- Test functionality flows
- Check edge cases
- Monitor functionality metrics

## Example: File Upload Broken

**Root Cause**: Upload button handler removed, breaking user flow.

**Fix Plan**:

- Add onClick handler to restore functionality
- Add test to prevent regression
- Verify user flow works

**Fix Implementation**:

```typescript
// Add test for upload functionality
it('calls upload handler when upload button clicked', async () => {
  const handleUpload = jest.fn();
  render(<UploadForm onUpload={handleUpload} />);

  await userEvent.click(screen.getByRole('button', { name: /upload/i }));

  expect(handleUpload).toHaveBeenCalledTimes(1);
});

// Fix: Add onClick handler to restore functionality
export function UploadForm({ onUpload }: UploadFormProps) {
  return (
    <button onClick={onUpload}>
      Upload File
    </button>
  );
}
```

**Verification**:

- Test passes (handler called)
- User flow works (upload → progress → success)
- System flow works (request received → file stored)

## Prevention Strategies (Functionality-Focused)

**After finding root cause that affects functionality**:

### 1. Understand Why It Happened (Functionality Context)

**Was it**:

- Missing feature? (functionality not implemented)
- Design flaw? (functionality design issue)
- Oversight? (functionality oversight)
- Refactoring mistake? (functionality not preserved)

**Example**: Refactoring mistake - handler removed, not replaced with onClick prop.

### 2. Implement Prevention (Functionality-Focused)

**Add prevention**:

- Add feature if missing (functionality feature)
- Redesign if flawed (functionality redesign)
- Add test if oversight (functionality test)
- Add tests before refactoring (functionality safety net)

**Example**: Add tests before refactoring to catch functionality breakage.

### 3. Add Safeguards (Functionality-Focused)

**Add safeguards**:

- Add monitoring (functionality monitoring)
- Add alerts (functionality alerts)
- Add tests (functionality tests)
- Add integration tests (functionality E2E tests)

**Example**: Add E2E test for upload functionality to catch regressions.

### 4. Document Learning (Functionality-Focused)

**Document**:

- Why it happened (functionality context)
- How to prevent (functionality prevention)
- What to watch for (functionality watch)

**Example**: Document that refactoring must preserve functionality, add tests first.

## Fix Verification Checklist

After implementing fix:

- [ ] Root cause fixed at source
- [ ] Functionality restored
- [ ] Tests pass (regression test + surrounding tests)
- [ ] User flow works
- [ ] System flow works
- [ ] Integration flow works (if applicable)
- [ ] Edge cases handled
- [ ] Prevention strategies implemented
- [ ] Safeguards added
- [ ] Learning documented

## Common Fix Mistakes

**Avoid**:

- Fixing symptom instead of root cause
- Making multiple changes at once
- Not testing functionality after fix
- Not implementing prevention
- Not documenting learning

**Do**:

- Fix at source
- Make minimal change
- Test functionality
- Implement prevention
- Document learning

---

**See Also**: `references/functionality-analysis.md` for functionality analysis, `references/analysis-strategies.md` for analysis strategies.
