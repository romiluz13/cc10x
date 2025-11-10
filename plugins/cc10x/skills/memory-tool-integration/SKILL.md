---
name: memory-tool-integration
description: Provides memory patterns with functionality-first approach. Use PROACTIVELY when workflows need to remember functionality patterns, preferences, or checkpoints. First understands functionality (user flow, admin flow, system flow), then stores functionality-related patterns. Focuses on storing functionality patterns, not generic patterns. Uses filesystem-based memory (.claude/memory/) and MCP memory servers. NOTE: Converted from hooks to skill - now model-invoked.
allowed-tools: Read, Grep, Glob, Bash
---

# Memory Integration - Functionality First

## Functionality First Mandate

**BEFORE storing memory, understand functionality**:

1. **What functionality patterns should be remembered?**
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?

2. **THEN store memory** - Store functionality-related patterns

3. **Use patterns** - Apply memory patterns AFTER functionality is understood

---

## Purpose

Provide memory functionality for cc10x workflows using filesystem-based memory with functionality-first approach. **NOTE**: Converted from hooks to skill - now model-invoked (more reliable than hooks).

**CRITICAL CHANGE**: Memory is now a skill, not hooks. This makes it more reliable and easier to debug.

---

## Availability

- ✅ **Filesystem Memory**: Available in Claude Code (`.claude/memory/` directory)
- ✅ **MCP Memory Servers**: Available via MCP servers if configured (e.g., `claude-code-memory`, `viralvoodoo-claude-code-memory`)
- ❌ **Memory Tool API**: NOT available in Claude Code (API beta only, requires `context-management-2025-06-27` header)

**Note**: If MCP memory servers are configured, they can be used in addition to or instead of filesystem memory. Check `.claude/settings.json` for MCP server configuration.

---

## When to Use

**Always use Memory Tool for** (Functionality-Focused):

- Storing learned functionality patterns (how functionality was built, user flows, system flows)
- Common functionality failure modes (bugs that broke functionality, resolution patterns)
- User functionality preferences (preferred functionality approaches)
- Workflow checkpoints (for resuming long-running functionality tasks)

**Consider using for**:

- Cross-session functionality state (if API available)
- Learned functionality architectural patterns
- Frequently used functionality verification commands

---

## Memory Implementation (Claude Code)

**Filesystem-Based Memory** (Currently Available):

```bash
# Store functionality patterns in JSON files
echo '{"functionality_patterns": {...}}' > .claude/memory/patterns.json

# Read functionality patterns
cat .claude/memory/patterns.json | jq '.'

# Query functionality patterns (via grep/jq)
grep -r "file_upload" .claude/memory/patterns.json
```

**Future API Integration** (If Memory Tool becomes available):

```python
# Store functionality information (API only - not available in Claude Code)
memory.store({
    "key": "functionality_patterns",
    "value": {
        "file_upload": {
            "user_flow": "click upload → select file → see progress → see success",
            "system_flow": "receive file → validate → store → send to CRM → return success",
            "complexity": 3
        }
    }
})

# Retrieve functionality information
memory.retrieve("functionality_patterns")

# Query functionality memories
memory.query("What functionality patterns have we learned for file uploads?")
```

---

## Integration Points

### Orchestrator Integration (Functionality-Focused)

**Before Complexity Scoring**:

1. Query memory for similar functionality: `memory.query("functionality similar to {current_functionality}")`
2. If similar functionality found, use learned patterns as reference
3. Store new functionality pattern after scoring: `memory.store({functionality_type: pattern, user_flow, system_flow})`

**After Workflow Completion**:

1. Store functionality outcome: `memory.store({workflow: "build", functionality: "file_upload", outcome: "success", user_flow_works: true})`
2. Store functionality patterns learned: `memory.store({pattern: "file upload user flow", user_flow: "click → select → progress → success"})`

### Workflow Integration (Functionality-Focused)

**Build Workflow**:

- Store functionality build patterns (user flow, system flow)
- Remember successful functionality TDD patterns
- Track functionality review feedback

**Debug Workflow**:

- Store functionality root cause patterns
- Remember successful functionality fix strategies
- Track functionality failure modes

**Planning Workflow**:

- Store functionality architectural patterns
- Remember functionality risk assessment patterns
- Track functionality planning approaches

**Review Workflow**:

- Store functionality quality patterns
- Remember functionality security check patterns
- Track functionality issues found

---

## Optimized Memory Storage Structure (Functionality-Focused)

### Functionality Patterns (Enhanced)

```json
{
  "functionality_patterns": {
    "file_upload": {
      "user_flow": "click upload → select file → see progress → see success → view file",
      "admin_flow": "see file list → filter files → download files → delete files",
      "system_flow": "receive file → validate → store → send to CRM → return success",
      "complexity": 3,
      "success_rate": 0.95,
      "usage_count": 12,
      "last_used": "2025-10-29",
      "last_validated": "2025-10-28",
      "confidence": "high"
    }
  }
}
```

### Failure Modes (Functionality-Focused)

```json
{
  "failure_modes": {
    "file_upload_button_not_working": {
      "error_pattern": "Upload button click does nothing",
      "functionality_impact": "Breaks user flow",
      "root_causes": [
        {
          "cause": "Event listener not attached",
          "fix": "Attach event listener in component mount",
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

### Component Orders (Functionality-Focused)

```json
{
  "component_orders": {
    "file_upload_feature": {
      "order": ["UploadForm", "FileInput", "UploadProgress", "FileViewer"],
      "functionality_flow": "user flow → system flow",
      "success_rate": 0.95,
      "dependency_graph": {
        "UploadForm": [],
        "FileInput": ["UploadForm"],
        "UploadProgress": ["UploadForm"],
        "FileViewer": ["UploadForm"]
      },
      "validated_deps_hash": "abc123",
      "last_validated": "2025-10-29"
    }
  }
}
```

### User Preferences (Functionality-Focused)

```json
{
  "user_preferences": {
    "functionality_approach": "user_flow_first",
    "review_depth": "functionality_focused",
    "build_approach": "make_it_work_first",
    "updated": "2025-10-29"
  }
}
```

### Preset Preferences (Context Management)

```json
{
  "preset_preferences": {
    "project_path": "/path/to/project",
    "preset": "frontend",
    "last_used": "2025-01-27T10:30:00Z",
    "usage_count": 5,
    "detection_accuracy": 0.95
  }
}
```

**Purpose**: Remember context preset preferences per project to improve automatic detection accuracy.

**Storage**: `.claude/memory/preset_preferences.json`

**Usage**:

- Store preset preference after orchestrator Phase 0 context preset detection
- Load preset preference on next session if task type unclear
- Track usage count and detection accuracy for improvement

**Integration**: Used by `context-preset-management` skill during orchestrator Phase 0.

---

## Implementation Guidance

### Step 1: Use Filesystem-Based Memory (Claude Code)

**Current Implementation** (Claude Code):

```bash
# Create memory directory if needed
mkdir -p .claude/memory

# Store functionality patterns in JSON files
cat > .claude/memory/patterns.json << EOF
{
  "functionality_patterns": {},
  "failure_modes": {},
  "user_preferences": {}
}
EOF
```

### Step 2: Store Functionality Patterns

**Filesystem-Based** (Claude Code):

```bash
# Store functionality patterns in JSON file
jq '.functionality_patterns["file_upload"] = {
  "user_flow": "click upload → select file → see progress → see success",
  "system_flow": "receive file → validate → store → send to CRM → return success",
  "complexity": 3
}' .claude/memory/patterns.json > .claude/memory/patterns.json.tmp
mv .claude/memory/patterns.json.tmp .claude/memory/patterns.json
```

### Step 3: Query Functionality Memory

**Filesystem-Based** (Claude Code):

```bash
# Query functionality patterns using grep/jq
similar=$(jq '.functionality_patterns | to_entries | map(select(.value.user_flow | contains("upload")))' .claude/memory/patterns.json)
if [ -n "$similar" ]; then
    # Use learned functionality pattern as reference
    reference_pattern=$(echo "$similar" | jq -r '.[0].value')
fi
```

---

## Reference Materials

For detailed guidance on memory storage strategies, cleanup rules, query patterns, validation, best practices, workflow integration, and session summary functions, see [REFERENCE.md](REFERENCE.md).

---

## Verification Checklist (Functionality-Focused)

**Before Using Memory**:

- [ ] Check if `.claude/memory/patterns.json` exists
- [ ] Load functionality patterns once, cache for workflow duration
- [ ] Validate functionality pattern signature matches current functionality
- [ ] Check confidence level (prefer high-confidence functionality patterns)

**After Workflow Completion**:

- [ ] Validate stored functionality patterns (compare predicted vs actual functionality)
- [ ] Update success rate scores
- [ ] Update usage counts
- [ ] Run cleanup function
- [ ] Store only validated, high-value functionality patterns
- [ ] Document memory usage in Actions Taken

---

## Skill Overview

- **Skill**: Memory Integration
- **Purpose**: Provide memory with functionality-first approach (not generic memory)
- **When**: Workflows need to remember functionality patterns, preferences, checkpoints
- **Core Rule**: Functionality first, then memory. Store functionality patterns, not generic patterns.

---

## References

- Anthropic Memory Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool
- cc10x Memory System: `.claude/memory/` directory
- Detailed reference: [REFERENCE.md](REFERENCE.md)

---

**Remember**: Memory exists to help remember functionality patterns. Don't store generic patterns - store functionality patterns!
