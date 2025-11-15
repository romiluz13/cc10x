#!/bin/bash
# cc10x v4.7.0 - Pre-Compact Hook (Simplified)
# Creates snapshot before context compaction to preserve workflow state

set -e

PROJECT_ROOT="$(pwd)"
MEMORY_DIR=".claude/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
SNAPSHOT_FILE="$SNAPSHOT_DIR/snapshot-$TIMESTAMP.md"
MAX_SNAPSHOTS=10

# Initialize directories
mkdir -p "$SNAPSHOT_DIR" 2>/dev/null || true

# Get workflow state
get_workflow_state() {
    local state=""
    local WORKFLOW_STATE_DIR="$MEMORY_DIR/workflow_state"
    
    if [ ! -d "$WORKFLOW_STATE_DIR" ]; then
        echo ""
        return 0
    fi
    
    # Find most recent checkpoint
    local checkpoint_file=""
    for workflow in build plan review debug validate; do
        checkpoint_file=$(find "$WORKFLOW_STATE_DIR" -name "${workflow}_*.json" -type f 2>/dev/null | sort | tail -1)
        if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
            break
        fi
    done
    
    if [ -z "$checkpoint_file" ] || [ ! -f "$checkpoint_file" ]; then
        echo ""
        return 0
    fi
    
    if command -v jq >/dev/null 2>&1; then
        local workflow_name phase
    workflow_name=$(jq -r '.workflow // empty' "$checkpoint_file" 2>/dev/null)
    phase=$(jq -r '.phase // empty' "$checkpoint_file" 2>/dev/null)
    
    if [ -n "$workflow_name" ] && [ "$workflow_name" != "null" ]; then
            state="Workflow: $workflow_name, Phase: $phase"
        fi
    fi
    
    echo "$state"
}

# Get workflow output paths
get_workflow_outputs() {
    local outputs=""
    
    for workflow in review build debug plan; do
        local ref_file="$MEMORY_DIR/current_${workflow}.txt"
        if [ -f "$ref_file" ]; then
            local output_path
            output_path=$(cat "$ref_file" 2>/dev/null)
            if [ -n "$output_path" ] && [ -f "$output_path" ]; then
                outputs="${outputs}- ${workflow}: $output_path\n"
            fi
        fi
    done
    
    echo -e "$outputs"
}

# Create snapshot
create_snapshot() {
    local workflow_state
    local workflow_outputs
    
    workflow_state=$(get_workflow_state)
    workflow_outputs=$(get_workflow_outputs)
    
    cat > "$SNAPSHOT_FILE" << EOF
# Context Snapshot

**Created**: $(date +'%Y-%m-%d %H:%M:%S')
**Reason**: Context compaction (75% token threshold)

## Workflow State

$workflow_state

## Workflow Outputs

$workflow_outputs

## Git Status

\`\`\`bash
$(git status --short 2>/dev/null || echo "Not a git repository")
\`\`\`

## Recovery Instructions

1. Load this snapshot after compaction
2. Continue workflow from last checkpoint
3. Verify current state

EOF
    
    echo "✅ Snapshot created: snapshot-$TIMESTAMP.md"
}

# Clean old snapshots
cleanup_old_snapshots() {
    local snapshot_count
    snapshot_count=$(find "$SNAPSHOT_DIR" -name "snapshot-*.md" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$snapshot_count" -gt "$MAX_SNAPSHOTS" ]; then
    local to_remove=$((snapshot_count - MAX_SNAPSHOTS))
        find "$SNAPSHOT_DIR" -name "snapshot-*.md" -type f | sort | head -n "$to_remove" | xargs rm -f 2>/dev/null || true
    fi
}

# Main
    create_snapshot
    cleanup_old_snapshots
    
exit 0
