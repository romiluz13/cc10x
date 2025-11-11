# Implementation & Verification - Phases 3-4

**Reference**: Part of `systematic-debugging` skill. See main SKILL.md for overview.

## Phase 3: Hypothesis + Minimal Fix (Functionality-Focused)

**CRITICAL**: Fix bugs affecting functionality. State root cause, write regression test, apply minimal fix.

## Hypothesis Testing Approach

### 1. Form Single Hypothesis

**State clearly**: "I think X is the root cause because Y"

- Write it down
- Be specific, not vague
- Explain how it affects functionality

**Example: File Upload Broken**:

- Hypothesis: Upload button handler removed, breaking user flow (user can't upload files).
- Root cause: Event listener removed, onClick prop not added
- Impact: User flow broken (user can't upload files)

### 2. Test Minimally

**Make the SMALLEST possible change** to test hypothesis:

- One variable at a time
- Don't fix multiple things at once
- Test hypothesis, not implement full solution

### 3. Verify Before Continuing

**Did it work?**:

- Yes → Phase 4 (Verification)
- Didn't work? Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

**Say "I don't understand X"**:

- Don't pretend to know
- Ask for help
- Research more

## Minimal Fix Pattern

**Fix bugs affecting functionality**:

- State the suspected root cause in one sentence (how it affects functionality)
- Write a failing regression test that proves the bug affects functionality
- Apply the smallest change to make functionality work

**Example: File Upload Broken**:

**Hypothesis**: Upload button handler removed, breaking user flow.

**Regression Test**:

```typescript
// src/components/UploadForm.test.tsx
it('calls upload handler when upload button clicked', async () => {
  const handleUpload = jest.fn();
  render(<UploadForm onUpload={handleUpload} />);

  await userEvent.click(screen.getByRole('button', { name: /upload/i }));

  expect(handleUpload).toHaveBeenCalledTimes(1);
});
// Expected: PASS
// Observed: FAIL (handler not called)
```

**Minimal Fix**:

```typescript
// src/components/UploadForm.tsx
export function UploadForm({ onUpload }: UploadFormProps) {
  return (
    <button onClick={onUpload}>
      Upload File
    </button>
  );
}
// Change: Add onClick prop handler (minimal change to restore functionality)
```

## Architecture Questioning After 3+ Failed Fixes

**If 3+ Fixes Failed: Question Architecture**

**Pattern indicating architectural problem**:

- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals**:

- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing symptoms?

**Discuss with your human partner before attempting more fixes**

This is NOT a failed hypothesis - this is a wrong architecture.

## Phase 4: Verification (Functionality-Focused)

**CRITICAL**: Verify functionality works. Run tests, verify flows, summarize fix.

## Verification Process

### 1. Run Regression Test

**Run the regression test and surrounding suite**:

- Test should pass (proving fix works)
- Surrounding tests should still pass (proving no regressions)
- Capture test outputs

**Example: File Upload Broken**:

```bash
# Run regression test
npm test UploadForm.test.tsx
# Output: PASS (handler called)
```

### 2. Verify Functionality Works

**Verify functionality works** (user flow, admin flow, system flow):

- Test the specific functionality that was broken
- Verify all related flows work
- Check for edge cases

**Example: File Upload Broken**:

```bash
# Verify user flow
# Expected: User clicks upload → progress shown → file uploaded
# Observed: ✅ User clicks upload → progress shown → file uploaded

# Verify system flow
# Expected: POST /api/files/upload request received
# Observed: ✅ POST /api/files/upload request received (from server logs)
```

### 3. Summarize Fix

**Summarize the fix, evidence, and follow-up monitoring**:

- What was broken?
- What was the root cause?
- What was the fix?
- What evidence supports the fix?
- What monitoring is needed?

## Deliverable Template

```
## Functionality Analysis
- Expected functionality: [description from context-dependent analysis]
- Observed behavior: [what's actually happening]
- Mapping: [where expected flow diverges from observed flow]

## Root Cause
- <what failed and why - how it affects functionality>

## Evidence
- Logs: <snippet related to functionality>
- Commands: <command> -> exit <code>
- Observed vs Expected: <comparison>

## Fix
- Summary of change (how it fixes functionality).
- Regression test: <file/test name>.

## Verification Summary
- Functionality verified: ✅ User flow works, ✅ System flow works
- <tests run, exit codes, residual risks>
```

## Verification Checklist

After verification:

- [ ] Regression test passes
- [ ] Surrounding tests pass (no regressions)
- [ ] User flow works
- [ ] System flow works
- [ ] Integration flow works (if applicable)
- [ ] Edge cases handled
- [ ] Fix summarized with evidence

## Common Verification Mistakes

**Avoid**:

- Skipping regression test
- Not verifying functionality flows
- Assuming fix works without testing
- Not summarizing fix and evidence

**Do**:

- Run regression test first
- Verify all functionality flows
- Test edge cases
- Summarize fix with evidence

---

**See Also**: `references/root-cause-investigation.md` for Phase 1 guidance, `references/pattern-analysis.md` for Phase 2 guidance.
