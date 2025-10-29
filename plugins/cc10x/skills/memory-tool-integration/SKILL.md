---
name: memory-tool-integration
description: Provides memory patterns for workflows using filesystem-based memory (.claude/memory/) and MCP memory servers. Use when workflows need to remember patterns, preferences, or checkpoints across sessions. Stores learned complexity patterns, common failure modes, user preferences, and workflow state. NOTE: Anthropic Memory Tool (API beta) not available in Claude Code - uses filesystem-based approach instead.
allowed-tools: Read, Grep, Glob, Bash
---

# Memory Integration

## Purpose

Provide memory functionality for cc10x workflows using filesystem-based memory. **NOTE**: Anthropic's Memory Tool (API beta feature) is **NOT available in Claude Code**. This skill uses filesystem-based memory (`.claude/memory/`) and provides patterns for future API integration if Memory Tool becomes available.

## Availability

- ✅ **Filesystem Memory**: Available in Claude Code (`.claude/memory/` directory)
- ✅ **MCP Memory Servers**: Available via MCP servers if configured (e.g., `claude-code-memory`, `viralvoodoo-claude-code-memory`)
- ❌ **Memory Tool API**: NOT available in Claude Code (API beta only, requires `context-management-2025-06-27` header)

**Note**: If MCP memory servers are configured, they can be used in addition to or instead of filesystem memory. Check `.claude/settings.json` for MCP server configuration.

## When to Use

**Always use Memory Tool for**:
- Storing learned complexity patterns (how complexity was scored for similar tasks)
- Common failure modes encountered (bugs, errors, resolution patterns)
- User workflow preferences (preferred review depth, build approach)
- Workflow checkpoints (for resuming long-running tasks)

**Consider using for**:
- Cross-session workflow state (if API available)
- Learned architectural patterns
- Frequently used verification commands

## Memory Implementation (Claude Code)

**Filesystem-Based Memory** (Currently Available):
```bash
# Store patterns in JSON files
echo '{"complexity_patterns": {...}}' > .claude/memory/patterns.json

# Read patterns
cat .claude/memory/patterns.json | jq '.'

# Query patterns (via grep/jq)
grep -r "similar_task" .claude/memory/patterns.json
```

**Future API Integration** (If Memory Tool becomes available):
```python
# Store information (API only - not available in Claude Code)
memory.store({
    "key": "complexity_patterns",
    "value": {
        "similar_task": "3 files, moderate risk -> score 3",
        "pattern": "multi-file changes = score 3+"
    }
})

# Retrieve information
memory.retrieve("complexity_patterns")

# Query memories
memory.query("What complexity patterns have we learned?")
```

## Integration Points

### Orchestrator Integration

**Before Complexity Scoring**:
1. Query memory for similar tasks: `memory.query("tasks similar to {current_task}")`
2. If similar tasks found, use learned complexity scores as reference
3. Store new complexity pattern after scoring: `memory.store({task_type: score, rationale})`

**After Workflow Completion**:
1. Store workflow outcome: `memory.store({workflow: "build", outcome: "success", time: "2h", complexity: 4})`
2. Store any patterns learned: `memory.store({pattern: "component order matters", reason: "dependency issue"})`

### Workflow Integration

**Build Workflow**:
- Store component build order patterns
- Remember successful TDD patterns
- Track common review feedback

**Debug Workflow**:
- Store root cause patterns
- Remember successful fix strategies
- Track common failure modes

**Planning Workflow**:
- Store architectural decision patterns
- Remember risk assessment patterns
- Track common planning approaches

**Review Workflow**:
- Store code quality patterns
- Remember security check patterns
- Track common issues found

## Optimized Memory Storage Structure

### Complexity Patterns (Enhanced)
```json
{
  "complexity_patterns": {
    "auth_feature_multi_file": {
      "signature": {
        "file_count": "3-5",
        "change_type": "feature",
        "has_external_deps": true,
        "has_security": true
      },
      "predicted_score": 4,
      "actual_scores": [4, 4, 3, 4],
      "accuracy": 0.875,
      "usage_count": 12,
      "last_used": "2025-10-29",
      "last_validated": "2025-10-28",
      "confidence": "high"
    }
  }
}
```

### Failure Modes (Enhanced)
```json
{
  "failure_modes": {
    "TypeError_cannot_read_null": {
      "error_pattern": "TypeError: Cannot read property '.*' of null",
      "root_causes": [
        {
          "cause": "Missing null check before property access",
          "fix": "Add optional chaining or null check",
          "success_rate": 0.92,
          "occurrences": 8,
          "last_seen": "2025-10-29"
        }
      ],
      "most_common_location": "frontend/components",
      "auto_delete_if_unused_days": 30
    }
  }
}
```

### Component Orders (Enhanced)
```json
{
  "component_orders": {
    "auth_feature": {
      "order": ["UserModel", "AuthService", "LoginComponent", "AuthGuard"],
      "success_rate": 0.95,
      "dependency_graph": {
        "UserModel": [],
        "AuthService": ["UserModel"],
        "LoginComponent": ["AuthService"],
        "AuthGuard": ["AuthService"]
      },
      "validated_deps_hash": "abc123",
      "last_validated": "2025-10-29"
    }
  }
}
```

### User Preferences (Minimal)
```json
{
  "user_preferences": {
    "review_depth": "comprehensive",
    "build_approach": "incremental",
    "test_coverage_target": 80,
    "updated": "2025-10-29"
  }
}
```

## Implementation Guidance

### Step 1: Use Filesystem-Based Memory (Claude Code)

**Current Implementation** (Claude Code):
```bash
# Create memory directory if needed
mkdir -p .claude/memory

# Store patterns in JSON files
cat > .claude/memory/patterns.json << EOF
{
  "complexity_patterns": {},
  "failure_modes": {},
  "user_preferences": {}
}
EOF
```

**Future API Integration** (If Memory Tool becomes available):
```bash
# Check if Memory Tool is available (API only)
# If not available, use filesystem-based memory (.claude/memory/)
```

### Step 2: Store Patterns

**Filesystem-Based** (Claude Code):
```bash
# Store patterns in JSON file
jq '.complexity_patterns["auth_task"] = {
  "task": "Add user authentication",
  "scored": 4,
  "reasoning": "Multiple files, security risk, external integration"
}' .claude/memory/patterns.json > .claude/memory/patterns.json.tmp
mv .claude/memory/patterns.json.tmp .claude/memory/patterns.json
```

**Future API Integration** (If Memory Tool becomes available):
```python
# Store learned pattern (API only)
memory.store({
    "key": "complexity_assessment",
    "value": {
        "task": "Add user authentication",
        "scored": 4,
        "reasoning": "Multiple files, security risk, external integration",
        "actual_complexity": "matched_score"
    }
})
```

### Step 3: Query Memory

**Filesystem-Based** (Claude Code):
```bash
# Query patterns using grep/jq
similar=$(jq '.complexity_patterns | to_entries | map(select(.value.task | contains("auth")))' .claude/memory/patterns.json)
if [ -n "$similar" ]; then
    # Use learned complexity score as reference
    reference_score=$(echo "$similar" | jq -r '.[0].value.scored')
fi
```

**Future API Integration** (If Memory Tool becomes available):
```python
# Query for similar patterns (API only)
similar = memory.query("tasks similar to 'add authentication'")
if similar:
    # Use learned complexity score as reference
    reference_score = similar[0]["scored"]
```

### Step 4: Update Memory

After learning new patterns:
```python
# Update existing memory
patterns = memory.retrieve("complexity_patterns")
patterns["new_pattern"] = {"score": 3, "pattern": "..."}
memory.store({"key": "complexity_patterns", "value": patterns})
```

## Current Implementation (Claude Code)

**Filesystem-Based Memory** (Always Available):
- Use filesystem-based memory: `.claude/memory/`
- Store patterns in `.claude/memory/patterns.json`
- Use existing snapshot system for checkpoints
- Store preferences in `.claude/memory/preferences.json`
- Query via `grep`, `jq`, or `Read` tool

**Future API Integration** (If Memory Tool becomes available):
- Fallback to filesystem if Memory Tool unavailable
- Migrate patterns to API when available

## Smart Storage Strategy (AI Coding Assistant Optimized)

### What to Save (Only High-Value, Validated Data)

**1. Complexity Patterns** (with validation):
- Task signature: file_count, change_type, has_external_deps, has_security
- Predicted complexity score
- Actual complexity scores (array for validation)
- Accuracy percentage (predicted vs actual match rate)
- Usage count (how many times referenced)
- Last validated date
- Confidence level: high (>80% accuracy), medium (60-80%), low (<60%)

**2. Failure Modes** (with success tracking):
- Error signature (regex pattern of error message)
- Root cause → Fix pattern mapping
- Success rate (how often fix worked)
- Occurrence count
- Last occurrence date
- Auto-delete if unused >30 days

**3. Component Orders** (with dependency validation):
- Task type → Component build order
- Success rate (did order work?)
- Dependency graph hash (validate if deps changed)
- Last validated date
- Auto-invalidate if dependencies change

**4. User Preferences** (explicit only):
- Only save when user explicitly makes choice
- Never infer from behavior
- User can delete anytime

### What NOT to Save

- ❌ Workflow history (use snapshots instead)
- ❌ Individual file changes (too granular)
- ❌ Exact code snippets (use patterns instead)
- ❌ User conversation logs (privacy)
- ❌ Failed attempts without learning value

### Memory Cleanup Rules

**Cleanup Timing** (CRITICAL - Explicit Trigger Points):
- **Trigger**: After each workflow completion (not during workflow, not per pattern storage)
- **Frequency**: Once per workflow (after all pattern storage and validation complete)
- **Execution**: Run cleanup script immediately after storing patterns in "Result Compilation" phase
- **Failure Handling**: If cleanup script fails, log error to `.claude/memory/cleanup_errors.log` and continue workflow (cleanup failure does not block workflow completion)
- **Timing Details**:
  - **When**: After orchestrator's "Result Compilation" phase completes
  - **After**: All patterns have been stored and validated
  - **Before**: Final report presentation
  - **Order**: Pattern storage → Pattern validation → Cleanup execution → Final report

**Automatic Cleanup** (run after each workflow):
1. **Complexity Patterns**:
   - Delete if accuracy < 50% after 3+ uses
   - Delete if unused > 60 days
   - Keep top 20 most accurate patterns per project

2. **Failure Modes**:
   - Delete if unused > 30 days
   - Delete if success rate < 60% after 5+ fixes
   - Auto-invalidate if related code patterns change

3. **Component Orders**:
   - Delete if dependency hash mismatch
   - Delete if success rate < 70%
   - Keep only for active project patterns

4. **User Preferences**:
   - Never auto-delete (user-controlled)

### Efficient Query Pattern

**Before Workflow**:
```bash
# 1. Load patterns.json once (not per query)
# 2. Use jq to filter by signature similarity
# 3. Sort by confidence + accuracy
# 4. Return top 3 matches only
# 5. Cache results for workflow duration
```

**Query Example**:
```bash
# Find similar complexity patterns
jq '.complexity_patterns | to_entries | 
  map(select(.value.signature.file_count == "3-5")) |
  sort_by(.value.accuracy) | reverse |
  .[0:3]' .claude/memory/patterns.json
```

### Pattern Validation After Workflow

**Required**: After workflow completes, validate stored patterns:
1. Compare predicted complexity → actual complexity
2. Update accuracy scores
3. Increment usage count
4. Update last validated date
5. If accuracy drops, lower confidence
6. If accuracy < threshold, mark for deletion

## Best Practices

1. **Save Only Validated Patterns**: Wait for workflow completion before saving
2. **Track Accuracy**: Always compare predicted vs actual outcomes
3. **Auto-Cleanup**: Remove low-confidence patterns automatically
4. **Semantic Matching**: Match by task signature, not exact text
5. **Confidence Levels**: Prioritize high-confidence patterns
6. **Privacy**: Never store sensitive data or user conversations
7. **Efficiency**: Load patterns once, cache for workflow duration

## Example Workflow Integration

**Build Workflow with Memory**:
```python
# Before building
previous_patterns = memory.query("similar builds")
if previous_patterns:
    print(f"Previous similar build took {previous_patterns[0]['time']}")

# During build
component_order = memory.retrieve("successful_component_order")
if component_order:
    use_order = component_order  # Use learned order

# After build
memory.store({
    "key": "build_outcomes",
    "value": {
        "timestamp": now(),
        "components": component_list,
        "time": build_time,
        "success": True
    }
})
```

## Memory Cleanup Implementation

### Cleanup Function (Run After Each Workflow)

**Execution Context**:
- **When**: After workflow completion, in orchestrator's "Result Compilation" phase
- **Trigger**: After pattern storage and validation complete
- **Command**: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/memory-cleanup.sh` (or inline bash using jq)
- **Error Handling**: If cleanup fails, log error and continue (don't abort workflow)

```bash
#!/bin/bash
# Memory cleanup script - run after workflow completion
# TIMING: Execute after orchestrator Result Compilation phase, after pattern storage
# ERROR HANDLING: Log errors but don't abort workflow

CLEANUP_THRESHOLD_DAYS_COMPLEXITY=60
CLEANUP_THRESHOLD_DAYS_FAILURE=30
MIN_ACCURACY_COMPLEXITY=0.5
MIN_SUCCESS_RATE_FAILURE=0.6

# Clean complexity patterns
jq --arg days "$CLEANUP_THRESHOLD_DAYS_COMPLEXITY" \
   --arg min_acc "$MIN_ACCURACY_COMPLEXITY" \
   '.complexity_patterns |= with_entries(
     select(
       (.value.accuracy >= ($min_acc | tonumber)) and
       (.value.last_used | fromdateiso8601 > (now - ($days | tonumber | . * 86400)))
     )
   ) | .complexity_patterns |= (to_entries | sort_by(.value.accuracy) | reverse | .[0:20] | from_entries)' \
   .claude/memory/patterns.json > .claude/memory/patterns.json.tmp
mv .claude/memory/patterns.json.tmp .claude/memory/patterns.json

# Clean failure modes
jq --arg days "$CLEANUP_THRESHOLD_DAYS_FAILURE" \
   --arg min_success "$MIN_SUCCESS_RATE_FAILURE" \
   '.failure_modes |= with_entries(
     select(
       (.value.root_causes[0].success_rate >= ($min_success | tonumber)) and
       (.value.last_seen | fromdateiso8601 > (now - ($days | tonumber | . * 86400)))
     )
   )' .claude/memory/failure_modes.json > .claude/memory/failure_modes.json.tmp
mv .claude/memory/failure_modes.json.tmp .claude/memory/failure_modes.json
```

### Pattern Validation After Workflow

**Required Steps**:
1. Load predicted complexity from memory
2. Compare with actual complexity experienced
3. Update accuracy: `(matches / total_uses) * 100`
4. Update confidence: high (>80%), medium (60-80%), low (<60%)
5. Increment usage_count
6. Update last_validated timestamp
7. If accuracy < 50% after 3+ uses → mark for deletion

## Verification Checklist

**Before Using Memory**:
- [ ] Check if `.claude/memory/patterns.json` exists
- [ ] Load patterns once, cache for workflow duration
- [ ] Validate pattern signature matches current task
- [ ] Check confidence level (prefer high-confidence patterns)

**After Workflow Completion**:
- [ ] Validate stored patterns (compare predicted vs actual)
- [ ] Update accuracy scores
- [ ] Update usage counts
- [ ] Run cleanup function
- [ ] Store only validated, high-value patterns
- [ ] Document memory usage in Actions Taken

## References

- Anthropic Memory Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool
- cc10x Memory System: `.claude/memory/` directory
- Workflow Integration: See orchestrator for integration points

