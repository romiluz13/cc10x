# Memory Integration Reference

## Smart Storage Strategy (Functionality-Focused)

### What to Save (Only High-Value, Validated Functionality Data)

**1. Functionality Patterns** (with validation):

- User flow: Step-by-step how user uses functionality
- Admin flow: Step-by-step how admin manages functionality (if applicable)
- System flow: Step-by-step how system processes functionality
- Complexity score
- Success rate (how often functionality works)
- Usage count (how many times referenced)
- Last validated date
- Confidence level: high (>80% success), medium (60-80%), low (<60%)

**2. Functionality Failure Modes** (with success tracking):

- Error signature (regex pattern of error message)
- Functionality impact (how it breaks functionality)
- Root cause → Fix pattern mapping
- Success rate (how often fix worked)
- Occurrence count
- Last occurrence date
- Auto-delete if unused >30 days

**3. Functionality Component Orders** (with dependency validation):

- Functionality type → Component build order
- Functionality flow (user flow → system flow)
- Success rate (did order work?)
- Dependency graph hash (validate if deps changed)
- Last validated date
- Auto-invalidate if dependencies change

**4. User Functionality Preferences** (explicit only):

- Only save when user explicitly makes choice
- Never infer from behavior
- User can delete anytime

**5. Preset Preferences** (context management):

- Project path → preset name mapping
- Last used timestamp
- Usage count
- Detection accuracy (how often correct preset was selected)
- Auto-update after each preset selection

### What NOT to Save

- ❌ Generic patterns (not functionality-specific)
- ❌ Workflow history (use snapshots instead)
- ❌ Individual file changes (too granular)
- ❌ Exact code snippets (use functionality patterns instead)
- ❌ User conversation logs (privacy)
- ❌ Failed attempts without functionality learning value

---

## Memory Cleanup Rules (Functionality-Focused)

**Cleanup Timing** (CRITICAL - Explicit Trigger Points):

- **Trigger**: After each workflow completion (not during workflow, not per pattern storage)
- **Frequency**: Once per workflow (after all functionality pattern storage and validation complete)
- **Execution**: Run cleanup script immediately after storing patterns in "Result Compilation" phase
- **Failure Handling**: If cleanup script fails, log error to `.claude/memory/cleanup_errors.log` and continue workflow (cleanup failure does not block workflow completion)

**Automatic Cleanup** (run after each workflow):

1. **Functionality Patterns**:
   - Delete if success rate < 50% after 3+ uses
   - Delete if unused > 60 days
   - Keep top 20 most accurate functionality patterns per project

2. **Functionality Failure Modes**:
   - Delete if unused > 30 days
   - Delete if success rate < 60% after 5+ fixes
   - Auto-invalidate if related functionality patterns change

3. **Functionality Component Orders**:
   - Delete if dependency hash mismatch
   - Delete if success rate < 70%
   - Keep only for active functionality patterns

4. **User Functionality Preferences**:
   - Never auto-delete (user-controlled)

---

## Efficient Query Pattern (Functionality-Focused)

**Before Workflow**:

```bash
# 1. Load functionality patterns.json once (not per query)
# 2. Use jq to filter by functionality similarity
# 3. Sort by confidence + success rate
# 4. Return top 3 matches only
# 5. Cache results for workflow duration
```

**Query Example**:

```bash
# Find similar functionality patterns
jq '.functionality_patterns | to_entries |
  map(select(.value.user_flow | contains("upload"))) |
  sort_by(.value.success_rate) | reverse |
  .[0:3]' .claude/memory/patterns.json
```

---

## Pattern Validation After Workflow (Functionality-Focused)

**Required**: After workflow completes, validate stored functionality patterns:

1. Compare predicted functionality → actual functionality
2. Update success rate scores
3. Increment usage count
4. Update last validated date
5. If success rate drops, lower confidence
6. If success rate < threshold, mark for deletion

---

## Best Practices

1. **Save Only Validated Functionality Patterns**: Wait for workflow completion before saving
2. **Track Success Rate**: Always compare predicted vs actual functionality outcomes
3. **Auto-Cleanup**: Remove low-confidence functionality patterns automatically
4. **Semantic Matching**: Match by functionality signature (user flow, system flow), not exact text
5. **Confidence Levels**: Prioritize high-confidence functionality patterns
6. **Privacy**: Never store sensitive data or user conversations
7. **Efficiency**: Load functionality patterns once, cache for workflow duration

---

## Example Workflow Integration (Functionality-Focused)

**Build Workflow with Memory**:

```python
# Before building functionality
previous_patterns = memory.query("functionality similar to 'file upload'")
if previous_patterns:
    print(f"Previous similar functionality: {previous_patterns[0]['user_flow']}")

# During build
functionality_order = memory.retrieve("successful_functionality_order")
if functionality_order:
    use_order = functionality_order  # Use learned functionality order

# After build
memory.store({
    "key": "functionality_outcomes",
    "value": {
        "timestamp": now(),
        "functionality": "file_upload",
        "user_flow_works": True,
        "system_flow_works": True,
        "success": True
    }
})
```

---

## Session Summary Functions

### Generate Session Summary

**Purpose:** Create comprehensive session documentation from workflow completion.

**Process:**

1. Parse workflow report (Actions Taken, Findings, Recommendations)
2. Extract file changes, tool calls, accomplishments, decisions
3. Format using session-summary.md template structure
4. Save to `.claude/memory/session_summaries/session-{timestamp}.md`

**Template Structure** (based on dotai's session-summary.md):

```markdown
# Session Summary - [Month Day, Year]

## Session Overview

[2-3 sentences describing the main focus, what was worked on, and key outcomes]

## Files Modified

### Code Changes

- **`path/to/file.ts`** - [Detailed description of what changed and why]

## Tool Calls & Operations

### File Operations

- **Edit**: `file.ts:45-67` - [What was edited]
- **Write**: `newfile.md` - [What was created]

## Key Accomplishments

- **[Feature/Fix Name]**: [Specific implementation details and impact]

## Problems Solved

- **Issue**: [Problem description]
  - **Solution**: [How it was resolved]
  - **Files**: [Which files were modified]

## Technical Decisions

- **Decision**: [What was decided]
  - **Rationale**: [Why this approach was chosen]

## Next Steps

- **Immediate**: [Tasks that need to be done next session]
- **Short-term**: [Planned work for upcoming sessions]

## Session Metrics

- **Duration**: [Estimated session length]
- **Tool Calls**: [Total number of tool calls]
- **Files Changed**: [Number of files modified]
```

### Update Working Plan

**Purpose:** Update development working plan based on workflow completion.

**Process:**

1. Read `.claude/memory/WORKING_PLAN.md` if exists
2. Extract completed tasks from workflow report
3. Update plan with minimal surgical changes:
   - Move completed tasks to "Completed Recently"
   - Update "Current Phase" if changed
   - Refresh "Next Priorities" from Recommendations
   - Update session timestamp
4. Preserve overall structure and formatting

**Update Pattern** (minimal surgical changes):

```markdown
## Completed Recently

- [Task from workflow report] - [Date]

## Current Phase

[Workflow type: review/plan/build/debug/validate]

## Next Priorities

[From Recommendations section of workflow report]

## Session Reference

Last updated: [timestamp]
```
