---
name: systematic-debugging
description: Debugs issues with functionality-first, context-dependent approach. Use PROACTIVELY when diagnosing bugs. First understands expected functionality using universal questions and context-dependent flows, then maps observed behavior to expected behavior, then investigates bugs systematically. Focuses on bugs that affect functionality, not generic debugging patterns. Enforces LOG FIRST, hypothesis-driven fixes, and regression tests. Provides specific debugging strategies with examples.
allowed-tools: Read, Grep, Glob, Bash
---

# Systematic Debugging - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before debugging, understand expected functionality using context-dependent analysis.

**Core Principle**: Understand what functionality should work (using universal questions and context-dependent flows), then map observed behavior to expected behavior, then debug bugs that affect functionality. Bugs exist in the context of functionality, not in isolation.

---

## Step 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

### Reference Template

**Reference**: See [Functionality Analysis Template](../cc10x-orchestrator/templates/functionality-analysis.md) for complete template.

### Process

1. **Detect Code Type**: Identify if this is UI, API, Utility, Integration, Database, Configuration, CLI, or Background Job
2. **Universal Questions First**: Answer Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Answer flow questions based on code type:
   - **UI**: User Flow, Admin Flow, System Flow
   - **API**: Request Flow, Response Flow, Error Flow, Data Flow
   - **Integration**: Integration Flow, Data Flow, Error Flow, State Flow
   - **Database**: Migration Flow, Query Flow, Data Flow, State Flow
   - **Background Jobs**: Job Flow, Processing Flow, State Flow, Error Flow
   - **CLI**: Command Flow, Processing Flow, Output Flow, Error Flow
   - **Configuration**: Configuration Flow, Validation Flow, Error Flow
   - **Utility**: Input Flow, Processing Flow, Output Flow, Error Flow

### Example: File Upload Broken (UI Feature)

**Universal Questions (Expected)**:

**Purpose**: Users should be able to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements (Expected)**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely in S3
- Must send file metadata to CRM API
- Must display upload progress to user
- Must handle errors gracefully

**Context-Dependent Flows (Expected - UI Feature)**:

**User Flow (Expected)**:

1. User navigates to "Upload File" page
2. User selects file from device
3. User sees upload progress indicator (0% → 100%)
4. User sees success message: "File uploaded successfully"
5. User sees link to view uploaded file

**System Flow (Expected)**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type and size
3. System stores file in secure storage (S3 bucket)
4. System sends file metadata to CRM API
5. System stores file record in database
6. System returns success response to user

**Observed Behavior (What's Broken)**:

- ❌ User Flow Broken: User clicks upload → nothing happens (no progress, no response)
- ❌ System Flow Broken: No server logs, no API call, file not stored

**Mapping Observed to Expected**:

- Expected: User sees upload progress → Observed: No progress indicator
- Expected: System receives request → Observed: No request received
- Expected: System validates file → Observed: Validation never runs
- Expected: System stores file → Observed: File not stored

**THEN Debug**: Investigate why upload button doesn't trigger functionality.

---

## Step 2: Systematic Debugging Process (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only debug AFTER you understand expected functionality and have mapped observed to expected. Debug bugs that affect functionality, not generic bugs.

### Core Principle

```
No fixes without root-cause evidence.
If you have not logged or observed the failing state, you are guessing.
```

**Functionality-First Debugging**:

1. **Understand Expected Functionality**: What should work? (context-dependent analysis)
2. **Map Observed to Expected**: What's broken? (compare observed to expected flows)
3. **Investigate**: Reproduce the bug, capture evidence
4. **Pattern Analysis**: Compare failing paths to working examples
5. **Hypothesis + Minimal Fix**: Fix the bug affecting functionality
6. **Verification**: Verify functionality works

### Four Phases

#### 1. Investigate (Functionality-Focused)

**Focus on functionality, not generic investigation**:

- Reproduce the functionality issue reliably (follow expected flow, observe where it breaks)
- Capture complete error messages, logs, request/response payloads related to functionality
- Inspect recent changes (`git log`, `git diff`) that might affect functionality
- Map observed behavior to expected behavior (where does the flow break?)

**Multi-Component Diagnostic Instrumentation** (Enhanced with dotai pattern):

**WHEN system has multiple components (CI → build → signing, API → service → database):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

```
For EACH component boundary:
  - Log what data enters component
  - Log what data exits component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks
THEN analyze evidence to identify failing component
THEN investigate that specific component
```

**Example (multi-layer system):**

```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"

# Layer 3: Signing script
echo "=== Keychain state: ==="
security list-keychains
security find-identity -v

# Layer 4: Actual signing
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

**This reveals:** Which layer fails (secrets → workflow ✓, workflow → build ✗)

**Example: File Upload Broken**:

```bash
# Reproduce functionality issue
# Expected: User clicks upload → progress shown → file uploaded
# Observed: User clicks upload → nothing happens

# Check browser console
# Expected: No errors
# Observed: Error: "Cannot read property 'addEventListener' of null"

# Check server logs
# Expected: POST /api/files/upload request received
# Observed: No request received

# Check recent changes
git log --oneline --since="2 days ago" -- src/components/UploadForm.tsx
# Output: abc1234 Fix upload button handler

git diff abc1234^..abc1234 src/components/UploadForm.tsx
# Output: -document.getElementById('upload-btn').addEventListener('click', handleUpload);
#         +// Upload button handler removed for refactoring
```

**Evidence Captured**:

- Browser console error: "Cannot read property 'addEventListener' of null"
- No server logs (request never sent)
- Recent change removed event listener

#### 2. Pattern Analysis (Functionality-Focused)

**Compare failing functionality to working functionality**:

- Compare failing paths to working examples (same code type, similar functionality)
- Identify where expected flow diverges from observed flow
- Consult relevant skill guidance (security-patterns, integration-patterns, etc.) **only if affects functionality**

**Example: File Upload Broken**:

```typescript
// Working: Other buttons work fine
// File: src/components/Button.tsx
export function Button({ onClick, children }: ButtonProps) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}
// Pattern: onClick prop passed directly to button

// Failing: Upload button doesn't work
// File: src/components/UploadForm.tsx
export function UploadForm() {
  return (
    <button id="upload-btn">
      Upload File
    </button>
  );
}
// Pattern: No onClick handler, relies on addEventListener (which was removed)

// Comparison: Working buttons use onClick prop, failing button uses addEventListener
// Root cause: Event listener removed, onClick prop not added
```

#### 3. Hypothesis + Minimal Fix (Functionality-Focused)

**Fix bugs affecting functionality**:

- State the suspected root cause in one sentence (how it affects functionality)
- Write a failing regression test that proves the bug affects functionality
- Apply the smallest change to make functionality work

**Hypothesis Testing Approach** (Enhanced with dotai pattern):

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help
   - Research more

**Architecture Questioning After 3+ Failed Fixes** (Enhanced with dotai pattern):

**If 3+ Fixes Failed: Question Architecture**

**Pattern indicating architectural problem:**

- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**

- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing symptoms?

**Discuss with your human partner before attempting more fixes**

This is NOT a failed hypothesis - this is a wrong architecture.

**Example: File Upload Broken**:

**Hypothesis**: Upload button handler removed, breaking user flow (user can't upload files).

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

#### 4. Verification (Functionality-Focused)

**Verify functionality works**:

- Run the regression test and surrounding suite; capture outputs
- Verify functionality works (user flow, admin flow, system flow)
- Summarise the fix, evidence, and follow-up monitoring

**Example: File Upload Broken**:

```bash
# Run regression test
npm test UploadForm.test.tsx
# Output: PASS (handler called)

# Verify user flow
# Expected: User clicks upload → progress shown → file uploaded
# Observed: ✅ User clicks upload → progress shown → file uploaded

# Verify system flow
# Expected: POST /api/files/upload request received
# Observed: ✅ POST /api/files/upload request received (from server logs)

# Verification Summary
# Functionality verified: ✅ User flow works, ✅ System flow works
# Tests: npm test UploadForm.test.tsx -> exit 0
# Fix: Added onClick prop handler to restore upload functionality
```

---

## LOG FIRST Playbook (Functionality-Focused)

**Log functionality-related data**:

Whenever functionality behavior is unclear:

- Log the full object/response with `JSON.stringify(value, null, 2)` (functionality data)
- Record headers, cookies, environment variables (masking secrets) (functionality context)
- For HTTP issues, log method, URL, payload, status, and body (functionality requests)
- For auth, log session claims, roles, and config (functionality auth)

**Focus**: Log data that helps understand functionality, not generic logging.

**Example: File Upload Broken**:

```typescript
// Log functionality data
console.log(
  "Upload request:",
  JSON.stringify(
    {
      file: {
        name: file.name,
        type: file.type,
        size: file.size,
      },
      timestamp: new Date().toISOString(),
    },
    null,
    2,
  ),
);

// Log functionality context
console.log("Upload context:", {
  userId: session.userId,
  apiUrl: process.env.API_URL,
  uploadEnabled: config.uploadEnabled,
});

// Log functionality request
console.log("Upload HTTP request:", {
  method: "POST",
  url: "/api/files/upload",
  headers: {
    "Content-Type": "multipart/form-data",
    Authorization: "Bearer ***",
  },
  payload: formData,
});
```

---

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

---

## Anti-Patterns

- **Skipping functionality understanding**: Don't debug without understanding expected functionality
- **Generic debugging**: Don't debug bugs that don't affect functionality
- **Applying multiple fixes**: Don't fix without proving the cause affects functionality
- **Trusting documentation**: Don't trust docs over runtime data for functionality
- **Reporting success without logs/tests**: Always verify functionality works
- **Not mapping observed to expected**: Always compare observed behavior to expected flows

---

## Priority Classification

**Critical (Must Fix)**:

- Blocks functionality (breaks user flow, system flow, integration flow)
- Prevents feature from working
- Breaks functionality completely

**Important (Should Fix)**:

- Affects functionality negatively (degrades user experience, slows functionality)
- Degrades functionality significantly

**Minor (Can Defer)**:

- Doesn't affect functionality (cosmetic issues, minor performance)
- Generic bugs not related to functionality

---

## When to Use

**Use PROACTIVELY when**:

- Diagnosing bugs
- Test failures
- Unexpected behavior

**Functionality-First Process**:

1. **First**: Understand expected functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Map observed behavior to expected behavior (where does the flow break?)
3. **Then**: Investigate bugs that affect functionality
4. **Then**: Fix bugs systematically
5. **Focus**: Bugs that affect functionality, not generic bugs

---

## Skill Overview

- **Skill**: Systematic Debugging
- **Purpose**: Debug issues with functionality-first, context-dependent approach (not generic debugging)
- **When**: Diagnosing bugs, test failures, unexpected behavior
- **Core Rule**: Functionality first (context-dependent analysis), then debug. Map observed to expected, then fix bugs affecting functionality.

---

## References

- Official debugging guidance: `docs/reference/03-SUBAGENTS.md`
- Verification requirements: `plugins/cc10x/skills/verification-before-completion/SKILL.md`

---

**Remember**: Bugs exist in the context of functionality. Don't debug generically - understand expected functionality, map observed to expected, then debug bugs that affect functionality! Provide specific debugging strategies with examples, not generic patterns.
