---
name: root-cause-analysis
description: Identifies root causes with functionality-first, context-dependent approach. Use PROACTIVELY when investigating bugs. First understands expected functionality using universal questions and context-dependent flows, then identifies root causes specific to that functionality. Focuses on root causes that affect functionality, not generic root cause analysis. Provides specific fixes with examples.
allowed-tools: Read, Grep, Glob, Bash
---

# Root Cause Analysis - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before analyzing root causes, understand expected functionality using context-dependent analysis.

**Core Principle**: Understand what functionality should work (using universal questions and context-dependent flows), then identify root causes specific to that functionality. Root causes exist in the context of functionality, not in isolation.

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

**THEN Root Cause Analysis**: Identify why functionality breaks.

---

## Step 2: Root Cause Analysis (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only analyze root causes AFTER you understand expected functionality. Analyze root causes specific to functionality, not generic root causes.

### Functionality-Focused Root Cause Checklist

**Priority: Critical (Core Functionality)**:

- [ ] Root cause breaks user flow (user can't complete tasks)
- [ ] Root cause breaks system flow (system doesn't process)
- [ ] Root cause breaks integration flow (external systems don't work)
- [ ] Root cause breaks error handling (errors not handled)

**Priority: Important (Supporting Functionality)**:

- [ ] Root cause affects functionality performance (slows functionality)
- [ ] Root cause affects functionality reliability (unreliable functionality)

**Priority: Minor (Can Defer)**:

- [ ] Generic root causes that don't affect functionality
- [ ] Perfect root cause analysis (if functionality is fixed)

---

## Step 3: Provide Specific Root Cause Analysis Strategies (WITH EXAMPLES)

**CRITICAL**: Provide specific, actionable root cause analysis strategies with examples, not generic frameworks.

### Strategy 1: The 5 Whys Framework (Functionality-Focused)

**Example: File Upload Broken**

**Problem**: File upload doesn't work (breaks user flow)

```
Why 1: Why doesn't file upload work?
 Answer: Upload button handler not attached
 Impact: User can't upload files (breaks user flow)

Why 2: Why isn't upload button handler attached?
 Answer: Event listener not added in component mount
 Impact: Button click doesn't trigger functionality (breaks user flow)

Why 3: Why isn't event listener added?
 Answer: Component refactored, handler removed
 Impact: Refactoring broke functionality (breaks user flow)

Why 4: Why was handler removed?
 Answer: Refactoring didn't preserve functionality
 Impact: Functionality not preserved during refactoring (breaks user flow)

Why 5: Why didn't refactoring preserve functionality?
 Answer: No tests for upload functionality
 Impact: No safety net to catch functionality breakage

ROOT CAUSE: Missing tests for upload functionality
FIX: Add tests for upload functionality, then refactor safely
PREVENTION: Always test functionality before refactoring
```

**Specific Fix**:

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

### Strategy 2: Symptom-to-Cause Mapping (Functionality-Focused)

**Example: File Upload Broken**

**Symptom**: "User can't upload file" (breaks user flow)

**Possible Causes** (mapped to functionality flows):

1. **Upload button handler not attached** (breaks user flow step 2)
   - **Investigation**: Check component code for onClick handler
   - **Evidence**: No onClick prop, no event listener
   - **Fix**: Add onClick handler

2. **File validation fails** (breaks system flow step 2)
   - **Investigation**: Check logs for validation errors
   - **Evidence**: Logs show "Invalid file type"
   - **Fix**: Fix validation logic

3. **File storage fails** (breaks system flow step 3)
   - **Investigation**: Check logs for storage errors
   - **Evidence**: Logs show "S3 upload failed"
   - **Fix**: Fix storage configuration

4. **CRM API fails** (breaks system flow step 4)
   - **Investigation**: Check logs for CRM API errors
   - **Evidence**: Logs show "CRM API timeout"
   - **Fix**: Add retry logic, improve error handling

**Root Cause Identification**:

- Most likely: Upload button handler not attached (symptom matches, evidence found)
- Less likely: File validation fails (would show error message)
- Less likely: File storage fails (would show error message)
- Less likely: CRM API fails (would show error message)

### Strategy 3: Flow-Based Root Cause Analysis

**Example: File Upload Broken**

**Trace Expected Flow vs Observed Flow**:

**Expected Flow** (from functionality analysis):

1. User clicks upload button → Handler called
2. File selected → Validation runs
3. File validated → Storage called
4. File stored → CRM API called
5. CRM API responds → Success shown

**Observed Flow**:

1. User clicks upload button → ❌ Nothing happens
2. File selected → ❌ Never happens (button doesn't work)
3. File validated → ❌ Never happens
4. File stored → ❌ Never happens
5. CRM API responds → ❌ Never happens

**Analysis**:

- Flow breaks at step 1 (button click doesn't trigger handler)
- Root cause: Upload button handler not attached
- Fix: Add onClick handler to restore functionality

### Strategy 4: Evidence-Based Root Cause Analysis

**Example: File Upload Broken**

**Gather Evidence**:

1. **Browser Console**:

   ```
   Error: Cannot read property 'addEventListener' of null
   ```

2. **Component Code**:

   ```typescript
   // Current code (broken)
   export function UploadForm() {
     return <button id="upload-btn">Upload File</button>;
   }

   // Expected code (working)
   export function UploadForm({ onUpload }: UploadFormProps) {
     return <button onClick={onUpload}>Upload File</button>;
   }
   ```

3. **Recent Changes**:

   ```bash
   git log --oneline --since="2 days ago" -- src/components/UploadForm.tsx
   # Output: abc1234 Fix upload button handler

   git diff abc1234^..abc1234 src/components/UploadForm.tsx
   # Output: -document.getElementById('upload-btn').addEventListener('click', handleUpload);
   #         +// Upload button handler removed for refactoring
   ```

**Root Cause Analysis**:

- **Symptom**: Upload button doesn't work
- **Evidence**: Handler removed during refactoring, not replaced with onClick prop
- **Root Cause**: Refactoring broke functionality (handler removed, not replaced)
- **Underlying Cause**: Missing tests (no safety net to catch functionality breakage)
- **Fix**: Add onClick handler, add tests
- **Prevention**: Always test functionality before refactoring

### Strategy 5: Backward Tracing (Enhanced with dotai pattern)

**WHEN error is deep in call stack:**

**REQUIRED**: Trace backward through call chain to find original trigger.

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

**Process**:

1. **Observe the Symptom**
   - Error happens deep in execution (not at entry point)
   - Stack trace shows long call chain
   - Unclear where invalid data originated

2. **Find Immediate Cause**
   - What code directly causes this?
   - Read error message, check stack trace

3. **Ask: What Called This?**
   - Trace up the call stack
   - Find what function called this with bad value
   - Keep tracing up until you find the source

4. **Find Original Trigger**
   - Where did bad value originate?
   - What test/code triggers the problem?
   - Fix at source, not at symptom

**Example: Deep Call Stack Error**

**Symptom**: `Error: git init failed in /Users/jesse/project/packages/core`

**Trace chain**:

1. `git init` runs in `process.cwd()` ← empty cwd parameter
2. WorktreeManager called with empty projectDir
3. Session.create() passed empty string
4. Test accessed `context.tempDir` before beforeEach
5. setupCoreTest() returns `{ tempDir: '' }` initially

**Root cause:** Top-level variable initialization accessing empty value

**Fix:** Made tempDir a getter that throws if accessed before beforeEach

**Adding Stack Traces** (when can't trace manually):

```typescript
// Before the problematic operation
async function gitInit(directory: string) {
  const stack = new Error().stack;
  console.error("DEBUG git init:", {
    directory,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack,
  });

  await execFileAsync("git", ["init"], { cwd: directory });
}
```

**Critical:** Use `console.error()` in tests (not logger - may not show)

**Run and capture:**

```bash
npm test 2>&1 | grep 'DEBUG git init'
```

**Analyze stack traces:**

- Look for test file names
- Find the line number triggering the call
- Identify the pattern (same test? same parameter?)

**Key Principle**: NEVER fix just where the error appears. Trace back to find the original trigger, then fix at source.

---

## Root Cause Analysis Framework (Reference - Use AFTER Functionality Understood)

**⚠️ Use this framework to analyze functionality-specific root causes, not generic root causes**.

### The 5 Whys Framework (Functionality-Focused)

**Apply to functionality, not generically**:

**Problem**: [Functionality issue] (breaks [flow type])

```
Why 1: Why does [functionality issue] occur?
 Answer: [Immediate cause]
 Impact: [How it affects functionality]

Why 2: Why does [immediate cause] occur?
 Answer: [Deeper cause]
 Impact: [How it affects functionality]

Why 3: Why does [deeper cause] occur?
 Answer: [Even deeper cause]
 Impact: [How it affects functionality]

Why 4: Why does [even deeper cause] occur?
 Answer: [Process/system cause]
 Impact: [How it affects functionality]

Why 5: Why does [process/system cause] occur?
 Answer: [Root cause]
 Impact: [How it affects functionality]

ROOT CAUSE: [Root cause]
FIX: [Specific fix that restores functionality]
PREVENTION: [How to prevent functionality breakage]
```

**Focus**: Root causes that affect functionality, not generic root causes.

### Symptom-to-Cause Mapping (Functionality-Focused)

**Map symptoms to functionality root causes**:

```
Symptom: "[Functionality issue]" (breaks [flow type])
 Possible Causes:
   [Cause 1] (breaks [flow step])
   [Cause 2] (breaks [flow step])
   [Cause 3] (breaks [flow step])
 Investigation: [How to investigate each cause]
 Evidence: [What evidence to look for]
 Fix: [Specific fix for each cause]
```

**Focus**: Symptoms and causes related to functionality, not generic symptoms.

---

## Root Cause Analysis Checklist (Functionality-Focused)

**⚠️ Only check these AFTER functionality is understood**:

```
Investigation Process:
- [ ] Understand expected functionality (context-dependent analysis)
- [ ] Map observed behavior to expected behavior (where does flow break?)
- [ ] Reproduce functionality bug consistently
- [ ] Gather all relevant logs (functionality-related)
- [ ] Identify exact functionality failure point (which flow step?)
- [ ] Trace back to source (functionality root cause)
- [ ] Ask "Why?" 5 times (functionality-focused)
- [ ] Verify root cause (affects functionality)
- [ ] Plan prevention (prevents functionality issues)
- [ ] Implement fix (fixes functionality)
- [ ] Test thoroughly (verifies functionality works)
- [ ] Document findings (functionality-focused)
```

---

## Prevention Strategies (Functionality-Focused)

### Prevent Recurrence (Functionality-Focused)

**After finding root cause that affects functionality**:

1. **Understand why it happened** (functionality context):
   - Was it a missing feature? (functionality not implemented)
   - Was it a design flaw? (functionality design issue)
   - Was it an oversight? (functionality oversight)
   - Was it a refactoring mistake? (functionality not preserved)

2. **Implement prevention** (functionality-focused):
   - Add feature if missing (functionality feature)
   - Redesign if flawed (functionality redesign)
   - Add test if oversight (functionality test)
   - Add tests before refactoring (functionality safety net)

3. **Add safeguards** (functionality-focused):
   - Add monitoring (functionality monitoring)
   - Add alerts (functionality alerts)
   - Add tests (functionality tests)
   - Add integration tests (functionality E2E tests)

4. **Document learning** (functionality-focused):
   - Why it happened (functionality context)
   - How to prevent (functionality prevention)
   - What to watch for (functionality watch)

---

## Priority Classification

**Critical (Must Fix)**:

- Root cause breaks functionality (user flow, system flow, integration flow)
- Prevents functionality from working
- Breaks functionality completely

**Important (Should Fix)**:

- Root cause affects functionality negatively (slows functionality, unreliable functionality)
- Degrades functionality significantly

**Minor (Can Defer)**:

- Generic root causes that don't affect functionality
- Perfect root cause analysis (if functionality is fixed)

---

## When to Use

**Use PROACTIVELY when**:

- Investigating recurring bugs
- Understanding failure patterns
- Preventing recurrence

**Functionality-First Process**:

1. **First**: Understand expected functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Map observed behavior to expected behavior (where does flow break?)
3. **Then**: Identify root causes specific to that functionality
4. **Then**: Apply root cause frameworks to analyze functionality-specific root causes
5. **Then**: Provide specific fixes with examples
6. **Focus**: Root causes that affect functionality, not generic root causes

---

## Skill Overview

- **Skill**: Root Cause Analysis
- **Purpose**: Identify root causes with functionality-first, context-dependent approach (not generic root cause analysis)
- **When**: Investigating bugs, understanding failures, preventing recurrence
- **Core Rule**: Functionality first (context-dependent analysis), then root cause analysis. Map observed to expected, then identify root causes specific to functionality.

---

**Remember**: Root causes exist in the context of functionality. Don't analyze root causes generically - understand expected functionality first, map observed to expected, then identify root causes specific to functionality! Provide specific fixes with examples, not generic frameworks.
