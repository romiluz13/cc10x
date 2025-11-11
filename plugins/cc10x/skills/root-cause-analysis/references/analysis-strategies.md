# Analysis Strategies - Root Cause Identification

**Reference**: Part of `root-cause-analysis` skill. See main SKILL.md for overview.

## Root Cause Analysis Strategies

**CRITICAL**: Apply these strategies AFTER functionality is understood. Focus on root causes that affect functionality.

## Strategy 1: The 5 Whys Framework (Functionality-Focused)

**Apply "Why?" 5 times**, focusing on how each answer affects functionality.

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

**Focus**: Each "Why?" must explain how it affects functionality, not generic causes.

## Strategy 2: Symptom-to-Cause Mapping (Functionality-Focused)

**Map symptoms to functionality root causes**. Investigate each possible cause, gather evidence, identify most likely root cause.

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

**Focus**: Map symptoms to functionality flows, not generic symptoms.

## Strategy 3: Flow-Based Root Cause Analysis

**Trace expected flow vs observed flow**. Identify where flow breaks, analyze why it breaks at that point.

**Example: File Upload Broken**

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

**Focus**: Trace functionality flows, not generic execution flows.

## Strategy 4: Evidence-Based Root Cause Analysis

**Gather evidence** (logs, code, recent changes). Analyze evidence to identify root cause. Verify root cause with evidence.

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

**Focus**: Evidence related to functionality, not generic evidence.

## Strategy 5: Backward Tracing (Deep Call Stack)

**WHEN error is deep in call stack**: Trace backward through call chain to find original trigger. Fix at source, not at symptom.

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

**Run and capture**:

```bash
npm test 2>&1 | grep 'DEBUG git init'
```

**Analyze stack traces**:

- Look for test file names
- Find the line number triggering the call
- Identify the pattern (same test? same parameter?)

**Key Principle**: NEVER fix just where the error appears. Trace back to find the original trigger, then fix at source.

## Strategy Selection Guide

| Situation                     | Use This Strategy        |
| ----------------------------- | ------------------------ |
| Need systematic analysis      | 5 Whys Framework         |
| Symptom clear, causes unclear | Symptom-to-Cause Mapping |
| Flow breakdown obvious        | Flow-Based Analysis      |
| Evidence available            | Evidence-Based Analysis  |
| Deep call stack error         | Backward Tracing         |

---

**See Also**: `references/functionality-analysis.md` for functionality analysis, `references/fix-implementation.md` for fix implementation.
