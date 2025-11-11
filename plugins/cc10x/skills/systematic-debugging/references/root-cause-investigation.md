# Root Cause Investigation - Phase 1

**Reference**: Part of `systematic-debugging` skill. See main SKILL.md for overview.

## Phase 1: Investigate (Functionality-Focused)

**CRITICAL**: Focus on functionality, not generic investigation. Reproduce the functionality issue, capture evidence related to functionality, map observed to expected.

## Investigation Process

### 1. Reproduce the Functionality Issue

**Reproduce reliably** (follow expected flow, observe where it breaks):

- Follow the expected functionality flow step by step
- Observe where the flow breaks
- Note the exact point of failure

**Example: File Upload Broken**:

```bash
# Reproduce functionality issue
# Expected: User clicks upload → progress shown → file uploaded
# Observed: User clicks upload → nothing happens
```

### 2. Capture Evidence Related to Functionality

**Capture complete error messages, logs, request/response payloads**:

- Error messages that indicate functionality failure
- Logs showing functionality flow breakdown
- Request/response payloads related to functionality
- Browser console errors (for UI issues)
- Server logs (for API issues)

**Example: File Upload Broken**:

```bash
# Check browser console
# Expected: No errors
# Observed: Error: "Cannot read property 'addEventListener' of null"

# Check server logs
# Expected: POST /api/files/upload request received
# Observed: No request received
```

### 3. Inspect Recent Changes

**Inspect recent changes** (`git log`, `git diff`) that might affect functionality:

- Check git history for changes to functionality-related files
- Review diffs to see what changed
- Identify changes that might break functionality

**Example: File Upload Broken**:

```bash
# Check recent changes
git log --oneline --since="2 days ago" -- src/components/UploadForm.tsx
# Output: abc1234 Fix upload button handler

git diff abc1234^..abc1234 src/components/UploadForm.tsx
# Output: -document.getElementById('upload-btn').addEventListener('click', handleUpload);
#         +// Upload button handler removed for refactoring
```

### 4. Map Observed to Expected

**Map observed behavior to expected behavior** (where does the flow break?):

- Compare each step of expected flow to observed flow
- Identify where they diverge
- Focus investigation on the divergence point

**Example: File Upload Broken**:

- Expected: User sees upload progress → Observed: No progress indicator
- Expected: System receives request → Observed: No request received
- Expected: System validates file → Observed: Validation never runs
- Expected: System stores file → Observed: File not stored

**Divergence Point**: User clicks upload → nothing happens (expected: progress shown)

## Multi-Component Diagnostic Instrumentation

**WHEN system has multiple components** (CI → build → signing, API → service → database):

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

**Example (multi-layer system)**:

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

**This reveals**: Which layer fails (secrets → workflow ✓, workflow → build ✗)

## Evidence Capture Checklist

After investigation, you should have:

- [ ] Reproduced the functionality issue reliably
- [ ] Captured error messages/logs related to functionality
- [ ] Inspected recent changes that might affect functionality
- [ ] Mapped observed behavior to expected behavior
- [ ] Identified where expected flow diverges from observed flow
- [ ] (If multi-component) Added diagnostic instrumentation and identified failing component

## Evidence Summary Template

```
## Evidence Captured

- Browser console error: [error message]
- Server logs: [log snippet]
- Recent changes: [git commit/diff summary]
- Observed vs Expected: [divergence point]
- Failing component: [if multi-component system]
```

## Common Investigation Mistakes

**Avoid**:

- Investigating without understanding expected functionality
- Capturing generic logs instead of functionality-related logs
- Skipping reproduction step
- Not mapping observed to expected
- Assuming root cause without evidence

**Do**:

- Understand expected functionality first
- Capture functionality-related evidence
- Reproduce reliably
- Map observed to expected
- Gather evidence before hypothesizing

---

**See Also**: `references/pattern-analysis.md` for Phase 2 guidance, `references/implementation-verification.md` for Phases 3-4 guidance.
