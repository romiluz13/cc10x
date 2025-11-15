#!/usr/bin/env bash
# cc10x v4.7.0 - Post-Compact Hook (Simplified)
# Restores workflow state and outputs after context compaction

set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
MEMORY_DIR="$PROJECT_DIR/.claude/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"

# Get most recent snapshot
get_most_recent_snapshot() {
    if [ -d "$SNAPSHOT_DIR" ]; then
        find "$SNAPSHOT_DIR" -name "snapshot-*.md" -type f | sort | tail -1
    else
        echo ""
    fi
}

# Restore workflow outputs from snapshot
restore_workflow_outputs() {
    local snapshot_file="$1"
    
    if [ -z "$snapshot_file" ] || [ ! -f "$snapshot_file" ]; then
        return 0
    fi
    
    # Extract workflow output paths from snapshot
    local outputs_section
    outputs_section=$(grep -A 20 "Workflow Outputs" "$snapshot_file" 2>/dev/null || echo "")
    
    if [ -z "$outputs_section" ]; then
        return 0
    fi
    
    # Extract and restore review output
    local review_path
    review_path=$(echo "$outputs_section" | grep "review:" | sed 's/.*review: //' | sed 's/[[:space:]]*$//')
    if [ -n "$review_path" ] && [ -f "$PROJECT_DIR/$review_path" ]; then
        echo "$review_path" > "$MEMORY_DIR/current_review.txt" 2>/dev/null || true
    fi
    
    # Extract and restore build output
    local build_path
    build_path=$(echo "$outputs_section" | grep "build:" | sed 's/.*build: //' | sed 's/[[:space:]]*$//')
    if [ -n "$build_path" ] && [ -f "$PROJECT_DIR/$build_path" ]; then
        echo "$build_path" > "$MEMORY_DIR/current_build.txt" 2>/dev/null || true
    fi
    
    # Extract and restore debug output
    local debug_path
    debug_path=$(echo "$outputs_section" | grep "debug:" | sed 's/.*debug: //' | sed 's/[[:space:]]*$//')
    if [ -n "$debug_path" ] && [ -f "$PROJECT_DIR/$debug_path" ]; then
        echo "$debug_path" > "$MEMORY_DIR/current_debug.txt" 2>/dev/null || true
    fi
    
    # Extract and restore plan output
    local plan_path
    plan_path=$(echo "$outputs_section" | grep "plan:" | sed 's/.*plan: //' | sed 's/[[:space:]]*$//')
    if [ -n "$plan_path" ] && [ -f "$PROJECT_DIR/$plan_path" ]; then
        echo "$plan_path" > "$MEMORY_DIR/current_plan.txt" 2>/dev/null || true
    fi
}

# Load session summary
load_session_summary() {
    local CURRENT_SESSION_FILE="$MEMORY_DIR/CURRENT_SESSION.md"
    if [ -f "$CURRENT_SESSION_FILE" ]; then
        cat "$CURRENT_SESSION_FILE" 2>/dev/null || echo ""
    else
        # Fallback: try archive
        local SESSION_SUMMARIES_DIR="$MEMORY_DIR/session_summaries"
        if [ -d "$SESSION_SUMMARIES_DIR" ]; then
            local latest_summary
            latest_summary=$(find "$SESSION_SUMMARIES_DIR" -name "session-*.md" -type f 2>/dev/null | sort | tail -1)
            if [ -n "$latest_summary" ] && [ -f "$latest_summary" ]; then
                cat "$latest_summary" 2>/dev/null || echo ""
            fi
        fi
    fi
}

# Main
snapshot_file=$(get_most_recent_snapshot)

if [ -n "$snapshot_file" ]; then
    restore_workflow_outputs "$snapshot_file"
    
    # Load snapshot content
    local snapshot_content=""
    if [ -f "$snapshot_file" ]; then
        snapshot_content=$(cat "$snapshot_file" 2>/dev/null || echo "")
    fi
    
    # Load session summary
    local session_summary_content
    session_summary_content=$(load_session_summary)
    
    # Build combined context
    local combined_context=""
    
    if [ -n "$session_summary_content" ]; then
        combined_context="<SESSION-SUMMARY>\n${session_summary_content}\n</SESSION-SUMMARY>\n\n"
    fi
    
    if [ -n "$snapshot_content" ]; then
        combined_context="${combined_context}<SNAPSHOT>\n${snapshot_content}\n</SNAPSHOT>\n\n"
    fi
    
    # Output context injection as JSON
    if [ -n "$combined_context" ]; then
        if command -v jq >/dev/null 2>&1; then
            printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' \
                "$(printf %s "$combined_context" | jq -Rs .)"
        else
            printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' \
                "$(printf %s "$combined_context" | python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()))')"
        fi
    fi
    fi

    exit 0
