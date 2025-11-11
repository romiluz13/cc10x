#!/bin/bash
# cc10x v4.3.3 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# Pre-Compact Hook - cc10x Orchestration System
# Creates comprehensive snapshot before context compaction (auto-healing at 75% tokens)

set -e

# Configuration
PROJECT_ROOT="$(pwd)"
MEMORY_DIR=".claude/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"
LOG_FILE="$MEMORY_DIR/session.log"
METRICS_FILE="$MEMORY_DIR/session_metrics.json"
WORKING_PLAN_PATH="$MEMORY_DIR/WORKING_PLAN.md"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
SNAPSHOT_FILE="$SNAPSHOT_DIR/snapshot-$TIMESTAMP.md"
MAX_SNAPSHOTS=10

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date +'%Y-%m-%d %H:%M:%S')"
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE" 2>&1 || true
}

# Error handling
error_exit() {
    local message="$1"
    log "ERROR" "$message"
    echo "❌ Error: $message" >&2
    exit 1
}

# Success handling
success() {
    local message="$1"
    log "INFO" "$message"
    echo "✅ $message"
}

# Info handling
info() {
    local message="$1"
    log "INFO" "$message"
    echo "ℹ️  $message"
}

# Initialize directories
initialize() {
    log "INFO" "=== Pre-Compact Hook Started ==="
    log "INFO" "Project root: $PROJECT_ROOT"
    echo "DEBUG: Pre-compact hook started" >&2
    echo "DEBUG: Project root: $PROJECT_ROOT" >&2
    echo "DEBUG: Snapshot directory: $SNAPSHOT_DIR" >&2
    
    # Create snapshot directory if it doesn't exist (non-fatal)
    if mkdir -p "$SNAPSHOT_DIR" 2>/dev/null; then
        log "INFO" "Snapshot directory ready: $SNAPSHOT_DIR"
        echo "DEBUG: Snapshot directory created/verified" >&2
    else
        log "WARN" "Failed to create snapshot directory: $SNAPSHOT_DIR (will continue anyway)"
        echo "DEBUG: Warning - snapshot directory creation failed, continuing" >&2
        # Don't exit - try to continue anyway
    fi
    
    log "INFO" "Directories initialized"
}

# Get current session ID
get_session_id() {
    local session_file="$MEMORY_DIR/current_session.txt"
    if [ -f "$session_file" ]; then
        cat "$session_file" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# Get metrics if available
get_metrics() {
    if [ -f "$METRICS_FILE" ]; then
        cat "$METRICS_FILE" 2>/dev/null || echo "{}"
    else
        echo "{}"
    fi
}

# Get working plan if available
get_working_plan() {
    if [ -f "$WORKING_PLAN_PATH" ]; then
        cat "$WORKING_PLAN_PATH" 2>/dev/null || echo "No working plan available"
    else
        echo "No working plan available"
    fi
}

# Count files changed in git (if in git repo)
count_git_changes() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        local staged unstaged
        staged=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
        unstaged=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
        echo "$((staged + unstaged))"
    else
        echo "0"
    fi
}

# Create comprehensive snapshot
create_snapshot() {
    local session_id
    local metrics
    local working_plan
    local git_changes
    
    echo "DEBUG: Creating snapshot..." >&2
    session_id=$(get_session_id)
    metrics=$(get_metrics)
    working_plan=$(get_working_plan)
    git_changes=$(count_git_changes)
    
    log "INFO" "Creating snapshot: $SNAPSHOT_FILE"
    echo "DEBUG: Snapshot file: $SNAPSHOT_FILE" >&2
    info "Creating context snapshot before compaction..."
    echo ""
    
    # Create the snapshot file (non-fatal if it fails)
    if cat > "$SNAPSHOT_FILE" << EOF
# Context Snapshot - Auto-Healing

**Created**: $(date +'%Y-%m-%d %H:%M:%S %Z')
**Session ID**: $session_id
**Reason**: Auto-healing context compaction (75% token threshold reached)
**Project**: $PROJECT_ROOT

---

## Snapshot Purpose

This snapshot preserves critical context across token limit compaction events.
It enables seamless continuation of work after context window refresh.

---

## Session Metrics

\`\`\`json
$metrics
\`\`\`

---

## Working Plan (Current State)

\`\`\`markdown
$working_plan
\`\`\`

---

## Git Status

- **Changed files**: $git_changes

\`\`\`bash
$(git status --short 2>/dev/null || echo "Not a git repository")
\`\`\`

---

## Active Work (To Be Filled by Claude)

### Current Task
- Feature/Bug: [Claude will fill this automatically]
- Phase: [e.g., Implementation Phase 2 of 5]
- Progress: [e.g., 60% complete, 3/5 increments done]

### Recent Completions
- [What was just finished]
- [Important milestones reached]

### Next Steps
1. [Immediate next action]
2. [Following action]
3. [Subsequent actions]

---

## Key Decisions Made (To Be Filled by Claude)

### Architecture Decisions
- [Important technical choices]
- [Justifications for approaches taken]

### Pattern Discoveries
- [Codebase patterns found]
- [Project conventions identified]

### Important Context
- [Critical information to remember]
- [Gotchas discovered]
- [Dependencies identified]

---

## Pending Work (To Be Filled by Claude)

### Incomplete Tasks
- [Task 1: Status and blockers]
- [Task 2: Status and remaining work]

### Known Issues
- [Issue 1: Description and impact]
- [Issue 2: Description and plan]

### Deferred Items
- [Item 1: Reason for deferral]
- [Item 2: Future work]

---

## Quality Status (To Be Filled by Claude)

### Tests
- **Passing**: [X/Y tests]
- **Coverage**: [X%]
- **New tests added**: [N tests]

### Code Quality
- **Linting**: [Clean/Issues found]
- **Type checking**: [Pass/Fail]
- **Security**: [No issues/Issues found]

### Verification Status
- [ ] All tests passing
- [ ] No linting errors
- [ ] Security scan clean
- [ ] Performance acceptable
- [ ] Ready for commit

---

## Recovery Instructions

**When resuming after compaction:**

1. **Load Context**
   - Read this snapshot first
   - Review "Working Plan" section
   - Check "Active Work" for current status

2. **Resume Work**
   - Continue from "Next Steps"
   - Reference "Key Decisions Made" for context
   - Check "Pending Work" for remaining tasks

3. **Verify State**
   - Run tests to confirm current state
   - Check git status for uncommitted changes
   - Review metrics for session progress

4. **Seamless Continuation**
   - User should not notice the compaction
   - All context preserved
   - Work continues without interruption

---

## Technical Details

- **Snapshot timestamp**: $TIMESTAMP
- **Snapshot file**: $SNAPSHOT_FILE
- **Memory directory**: $MEMORY_DIR
- **Max snapshots retained**: $MAX_SNAPSHOTS

---

**This snapshot enables cc10x's auto-healing capability.**
**Context is preserved across compaction events for seamless continuation.**

---

## Notes

- This snapshot was automatically created at 75% token usage
- Claude will automatically fill in the marked sections
- Previous snapshots are retained (up to $MAX_SNAPSHOTS most recent)
- Snapshots are cleaned up automatically (oldest removed first)

EOF
    then
        log "INFO" "Snapshot created successfully"
        echo "DEBUG: Snapshot file written successfully" >&2
        success "Snapshot created: snapshot-$TIMESTAMP.md"
        echo ""
    else
        log "WARN" "Failed to create snapshot file: $SNAPSHOT_FILE (will continue anyway)"
        echo "DEBUG: Warning - snapshot creation failed, continuing" >&2
        # Don't exit - compaction can still proceed
    fi
    
    log "INFO" "Snapshot creation completed"

# Clean old snapshots
cleanup_old_snapshots() {
    log "INFO" "Cleaning old snapshots (keeping last $MAX_SNAPSHOTS)"
    info "Cleaning old snapshots (keeping last $MAX_SNAPSHOTS)..."
    
    local snapshot_count
    snapshot_count=$(find "$SNAPSHOT_DIR" -name "snapshot-*.md" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$snapshot_count" -le "$MAX_SNAPSHOTS" ]; then
        log "INFO" "Snapshot count ($snapshot_count) within limit ($MAX_SNAPSHOTS)"
        info "Snapshot count OK: $snapshot_count snapshots"
        echo ""
        return 0
    fi
    
    # Remove oldest snapshots beyond limit
    local to_remove=$((snapshot_count - MAX_SNAPSHOTS))
    log "INFO" "Removing $to_remove old snapshots"
    
    if ! find "$SNAPSHOT_DIR" -name "snapshot-*.md" -type f | sort | head -n "$to_remove" | xargs rm -f 2>/dev/null; then
        log "WARN" "Failed to clean some old snapshots"
        info "Warning: Couldn't clean all old snapshots"
        echo ""
        return 1
    fi
    
    log "INFO" "Old snapshots cleaned successfully"
    success "Cleaned $to_remove old snapshots"
    echo ""
}

# Update metrics for compaction event
update_metrics() {
    if [ -f "$METRICS_FILE" ]; then
        log "INFO" "Recording compaction event in metrics"
        # We can't easily update JSON in bash, so just log it
        log "INFO" "Compaction event: snapshot created at $TIMESTAMP"
    fi
}

# Display summary
display_summary() {
    local snapshot_count
    snapshot_count=$(find "$SNAPSHOT_DIR" -name "snapshot-*.md" 2>/dev/null | wc -l | tr -d ' ')
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📸 Context Snapshot Complete"
    echo ""
    echo "  Snapshot: snapshot-$TIMESTAMP.md"
    echo "  Location: $SNAPSHOT_DIR"
    echo "  Total snapshots: $snapshot_count"
    echo ""
    echo "🔄 Context Compaction Ready"
    echo ""
    echo "  What happens next:"
    echo "    1. Claude compacts current context"
    echo "    2. New context window opens"
    echo "    3. Snapshot is loaded automatically"
    echo "    4. Work continues seamlessly"
    echo ""
    success "Auto-healing snapshot preserved successfully"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Main execution
main() {
    echo "DEBUG: pre-compact.sh main() started" >&2
    
    # Initialize
    initialize
    
    # Create snapshot
    create_snapshot
    
    # Clean old snapshots
    cleanup_old_snapshots
    
    # Update metrics
    update_metrics
    
    # Display summary
    display_summary
    
    # Final log
    log "INFO" "Pre-compact hook complete"
    echo "DEBUG: Pre-compact hook completed successfully" >&2
    
    return 0
}

# Run main function
main

# Exit successfully
exit 0
