# Pattern Analysis - Phase 2

**Reference**: Part of `systematic-debugging` skill. See main SKILL.md for overview.

## Phase 2: Pattern Analysis (Functionality-Focused)

**CRITICAL**: Compare failing functionality to working functionality. Identify where expected flow diverges from observed flow.

## Pattern Analysis Process

### 1. Find Working Examples

**Locate similar working code** (same code type, similar functionality):

- Search codebase for similar functionality that works
- Identify patterns in working code
- Compare working pattern to failing pattern

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
```

### 2. Compare Failing to Working

**Compare failing paths to working examples**:

- Identify differences between working and failing code
- List every difference, however small
- Don't assume "that can't matter"

**Example: File Upload Broken**:

```typescript
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

### 3. Identify Differences

**List every difference** between working and failing:

- Code structure differences
- Pattern differences
- Configuration differences
- Dependency differences

**Focus**: Differences that affect functionality, not cosmetic differences.

### 4. Understand Dependencies

**What other components does this need?**:

- What settings, config, environment?
- What assumptions does it make?
- What dependencies must be available?

**Example: File Upload Broken**:

- Dependency: Event handler must be attached
- Assumption: Button element exists in DOM
- Configuration: None required

## Pattern Comparison Strategies

### Strategy 1: Code Pattern Comparison

**Compare code patterns**:

- Working pattern: onClick prop handler
- Failing pattern: addEventListener (removed)
- Difference: Missing event handler

### Strategy 2: Flow Pattern Comparison

**Compare functionality flows**:

- Working flow: User clicks → onClick fires → handler executes
- Failing flow: User clicks → no handler → nothing happens
- Difference: Handler missing

### Strategy 3: Configuration Comparison

**Compare configurations**:

- Working config: Feature flag enabled, API URL set
- Failing config: Feature flag disabled, API URL missing
- Difference: Configuration mismatch

## Root Cause Identification

**After pattern analysis, you should identify**:

- What's different between working and failing?
- Why does the difference break functionality?
- What needs to change to fix functionality?

**Example: File Upload Broken**:

- Difference: Missing onClick handler
- Why it breaks: Button click doesn't trigger functionality
- What to change: Add onClick prop handler

## Pattern Analysis Checklist

After pattern analysis:

- [ ] Found working examples (similar functionality)
- [ ] Compared failing to working
- [ ] Identified all differences
- [ ] Understood dependencies
- [ ] Identified root cause
- [ ] Understand why root cause breaks functionality

## Common Pattern Analysis Mistakes

**Avoid**:

- Not finding working examples
- Assuming differences don't matter
- Skipping dependency analysis
- Not understanding why difference breaks functionality

**Do**:

- Find working examples first
- List all differences
- Understand dependencies
- Understand why difference breaks functionality

---

**See Also**: `references/root-cause-investigation.md` for Phase 1 guidance, `references/implementation-verification.md` for Phases 3-4 guidance.
