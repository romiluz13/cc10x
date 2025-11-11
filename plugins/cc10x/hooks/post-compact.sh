#!/usr/bin/env bash
# cc10x v4.3.3 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# Post-compact hook - fills snapshot templates with actual context and loads afterCompact instructions
# Based on dotai's proven post-compact recovery pattern

set -e

# Configuration
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
PROMPT_FILE="$PROJECT_DIR/.claude/prompt.json"
MEMORY_DIR="$PROJECT_DIR/.claude/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"
WORKFLOW_STATE_DIR="$MEMORY_DIR/workflow_state"
LOG_FILE="$MEMORY_DIR/session.log"

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date +'%Y-%m-%d %H:%M:%S')"
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE" 2>&1 || true
}

# Get most recent snapshot file
get_most_recent_snapshot() {
    if [ -d "$SNAPSHOT_DIR" ]; then
        find "$SNAPSHOT_DIR" -name "snapshot-*.md" -type f | sort | tail -1
    else
        echo ""
    fi
}

# Get most recent workflow checkpoint
get_most_recent_checkpoint() {
    local workflow_type="$1"
    if [ -d "$WORKFLOW_STATE_DIR" ] && [ -n "$workflow_type" ]; then
        find "$WORKFLOW_STATE_DIR" -name "${workflow_type}_*.json" -type f 2>/dev/null | sort | tail -1
    else
        # Try to find any checkpoint
        if [ -d "$WORKFLOW_STATE_DIR" ]; then
            find "$WORKFLOW_STATE_DIR" -name "*.json" -type f 2>/dev/null | sort | tail -1
        else
            echo ""
        fi
    fi
}

# Extract feature/bug name from checkpoint or working plan
extract_feature_name() {
    local checkpoint_file="$1"
    local feature_name="Unknown feature"
    
    # Try to extract from checkpoint
    if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
        if command -v jq >/dev/null 2>&1; then
            local name
            name=$(jq -r '.state.feature_name // .state.current_component // .state.current_bug // .workflow // empty' "$checkpoint_file" 2>/dev/null)
            if [ -n "$name" ] && [ "$name" != "null" ]; then
                feature_name="$name"
            fi
        fi
    fi
    
    # Fallback: try to extract from working plan
    local working_plan="$MEMORY_DIR/WORKING_PLAN.md"
    if [ -f "$working_plan" ]; then
        local plan_name
        plan_name=$(grep -i "^#\|^##" "$working_plan" | head -1 | sed 's/^#* *//' | sed 's/ *$//')
        if [ -n "$plan_name" ]; then
            feature_name="$plan_name"
        fi
    fi
    
    echo "$feature_name"
}

# Extract workflow phase from checkpoint
extract_phase() {
    local checkpoint_file="$1"
    local phase="Unknown phase"
    
    if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
        if command -v jq >/dev/null 2>&1; then
            local workflow_name
            local phase_name
            workflow_name=$(jq -r '.workflow // empty' "$checkpoint_file" 2>/dev/null)
            phase_name=$(jq -r '.phase // empty' "$checkpoint_file" 2>/dev/null)
            
            if [ -n "$workflow_name" ] && [ "$workflow_name" != "null" ] && [ -n "$phase_name" ] && [ "$phase_name" != "null" ]; then
                phase="$workflow_name: $phase_name"
            elif [ -n "$phase_name" ] && [ "$phase_name" != "null" ]; then
                phase="$phase_name"
            fi
        fi
    fi
    
    echo "$phase"
}

# Calculate progress from checkpoint
calculate_progress() {
    local checkpoint_file="$1"
    local progress="Progress unknown"
    
    if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
        if command -v jq >/dev/null 2>&1; then
            local workflow
            workflow=$(jq -r '.workflow // empty' "$checkpoint_file" 2>/dev/null)
            
            case "$workflow" in
                "build")
                    local total completed
                    total=$(jq '[.state.components[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
                    completed=$(jq '[.state.completed_components[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
                    if [ "$total" -gt 0 ]; then
                        local percent=$((completed * 100 / total))
                        progress="$percent% complete ($completed/$total components)"
                    fi
                    ;;
                "plan")
                    # Plan workflows have phases, estimate based on phase
                    local phase
                    phase=$(jq -r '.phase // empty' "$checkpoint_file" 2>/dev/null)
                    case "$phase" in
                        *"Phase_0"*) progress="0% complete (Functionality Analysis)" ;;
                        *"Phase_1"*) progress="20% complete (Requirements Intake)" ;;
                        *"Phase_2"*) progress="40% complete (Delegated Analysis)" ;;
                        *"Phase_3"*) progress="60% complete (Architecture Design)" ;;
                        *"Phase_4"*) progress="80% complete (Synthesis)" ;;
                        *"Phase_5"*) progress="90% complete (Verification)" ;;
                        *) progress="In progress" ;;
                    esac
                    ;;
                "review")
                    local total reviewed
                    total=$(jq '[.state.files_reviewed[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
                    reviewed=$(jq '[.state.files_reviewed[]? | select(.status == "reviewed")] | length' "$checkpoint_file" 2>/dev/null || echo "0")
                    if [ "$total" -gt 0 ]; then
                        local percent=$((reviewed * 100 / total))
                        progress="$percent% complete ($reviewed/$total files reviewed)"
                    fi
                    ;;
                "debug")
                    local total fixed
                    total=$(jq '[.state.bugs[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
                    fixed=$(jq '[.state.bugs[]? | select(.status == "fixed")] | length' "$checkpoint_file" 2>/dev/null || echo "0")
                    if [ "$total" -gt 0 ]; then
                        local percent=$((fixed * 100 / total))
                        progress="$percent% complete ($fixed/$total bugs fixed)"
                    fi
                    ;;
            esac
        fi
    fi
    
    echo "$progress"
}

# Extract recent completions from checkpoint
extract_recent_completions() {
    local checkpoint_file="$1"
    local completions=""
    
    if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
        if command -v jq >/dev/null 2>&1; then
            local workflow
            workflow=$(jq -r '.workflow // empty' "$checkpoint_file" 2>/dev/null)
            
            case "$workflow" in
                "build")
                    completions=$(jq -r '.state.completed_components[]? | "- " + .name + " (" + (.status // "completed") + ")"' "$checkpoint_file" 2>/dev/null | head -5)
                    ;;
                "review")
                    completions=$(jq -r '.state.files_reviewed[]? | select(.status == "reviewed") | "- " + .path + " reviewed"' "$checkpoint_file" 2>/dev/null | head -5)
                    ;;
                "debug")
                    completions=$(jq -r '.state.bugs[]? | select(.status == "fixed") | "- " + .name + " fixed"' "$checkpoint_file" 2>/dev/null | head -5)
                    ;;
            esac
        fi
    fi
    
    # Fallback: check git commits in last hour
    if [ -z "$completions" ] && git rev-parse --git-dir > /dev/null 2>&1; then
        completions=$(git log --since="1 hour ago" --pretty=format:"- %s" 2>/dev/null | head -5)
    fi
    
    if [ -z "$completions" ]; then
        completions="- No recent completions recorded"
    fi
    
    echo "$completions"
}

# Extract next steps from checkpoint
extract_next_steps() {
    local checkpoint_file="$1"
    local next_steps=""
    
    if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
        if command -v jq >/dev/null 2>&1; then
            local next_phase
            next_phase=$(jq -r '.next_phase // empty' "$checkpoint_file" 2>/dev/null)
            
            if [ -n "$next_phase" ] && [ "$next_phase" != "null" ]; then
                next_steps="1. Continue to $next_phase"
            fi
            
            # Add current component/bug if exists
            local current_item
            current_item=$(jq -r '.state.current_component // .state.current_bug // empty' "$checkpoint_file" 2>/dev/null)
            if [ -n "$current_item" ] && [ "$current_item" != "null" ]; then
                next_steps="$next_steps
2. Complete $current_item"
            fi
        fi
    fi
    
    if [ -z "$next_steps" ]; then
        next_steps="1. Review snapshot context
2. Continue workflow from last checkpoint
3. Verify current state"
    fi
    
    echo "$next_steps"
}

# Fill snapshot template with actual context
fill_snapshot_template() {
    local snapshot_file="$1"
    
    echo "DEBUG: fill_snapshot_template called with: $snapshot_file" >&2
    
    if [ -z "$snapshot_file" ] || [ ! -f "$snapshot_file" ]; then
        log "WARN" "No snapshot file found to fill"
        echo "DEBUG: No snapshot file found" >&2
        return 0
    fi
    
    log "INFO" "Filling snapshot template: $snapshot_file"
    echo "DEBUG: Filling snapshot template: $snapshot_file" >&2
    
    # Find most recent checkpoint (try all workflow types)
    local checkpoint_file=""
    echo "DEBUG: Searching for checkpoint files..." >&2
    for workflow in build plan review debug validate; do
        checkpoint_file=$(get_most_recent_checkpoint "$workflow")
        if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
            echo "DEBUG: Found checkpoint: $checkpoint_file" >&2
            break
        fi
    done
    
    if [ -z "$checkpoint_file" ] || [ ! -f "$checkpoint_file" ]; then
        echo "DEBUG: No checkpoint file found, will use fallback values" >&2
        log "WARN" "No checkpoint file found for snapshot filling"
    fi
    
    # Extract context
    local feature_name
    local phase
    local progress
    local completions
    local next_steps
    
    feature_name=$(extract_feature_name "$checkpoint_file")
    phase=$(extract_phase "$checkpoint_file")
    progress=$(calculate_progress "$checkpoint_file")
    completions=$(extract_recent_completions "$checkpoint_file")
    next_steps=$(extract_next_steps "$checkpoint_file")
    
    # Create temp file for replacement
    local temp_file
    temp_file=$(mktemp)
    
    # Use Python for more reliable text replacement
    echo "DEBUG: Starting Python script to fill template" >&2
    python3 <<PYTHON_SCRIPT
import re
import sys
import os

snapshot_file = "$snapshot_file"
feature_name = "$feature_name"
phase = "$phase"
progress = "$progress"
completions = """$completions"""
next_steps = """$next_steps"""
temp_file = "$temp_file"

try:
    # Check if snapshot file exists
    if not os.path.exists(snapshot_file):
        print(f"ERROR: Snapshot file does not exist: {snapshot_file}", file=sys.stderr)
        sys.exit(1)
    
    # Read snapshot file
    with open(snapshot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"DEBUG: Read snapshot file, length: {len(content)}", file=sys.stderr)
    
    # Replace simple placeholders
    content = content.replace('[Claude will fill this automatically]', feature_name)
    content = content.replace('[e.g., Implementation Phase 2 of 5]', phase)
    content = content.replace('[e.g., 60% complete, 3/5 increments done]', progress)
    
    # Replace Recent Completions section
    completions_pattern = r'### Recent Completions\n(?:- \[.*?\]\n)+'
    completions_replacement = f'### Recent Completions\n{completions}\n'
    content = re.sub(completions_pattern, completions_replacement, content, flags=re.MULTILINE)
    
    # Replace Next Steps section
    next_steps_pattern = r'### Next Steps\n(?:[0-9]+\. \[.*?\]\n)+'
    next_steps_replacement = f'### Next Steps\n{next_steps}\n'
    content = re.sub(next_steps_pattern, next_steps_replacement, content, flags=re.MULTILINE)
    
    # Write to temp file
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"DEBUG: Successfully wrote filled template to temp file", file=sys.stderr)
    sys.exit(0)
except Exception as e:
    print(f"ERROR: Error filling snapshot: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
    
    local python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        # Replace original file
        echo "DEBUG: Python script succeeded, moving temp file to snapshot" >&2
        mv "$temp_file" "$snapshot_file"
        log "INFO" "Snapshot template filled successfully"
        echo "DEBUG: Snapshot template filled successfully" >&2
    else
        echo "DEBUG: Python script failed (exit code: $python_exit_code), using sed fallback" >&2
        log "WARN" "Failed to fill snapshot template (Python failed, using simple sed replacement)"
        rm -f "$temp_file"
        # Fallback: simple sed replacement for critical fields only
        sed -i.bak \
            -e "s|\[Claude will fill this automatically\]|$feature_name|g" \
            -e "s|\[e\.g\., Implementation Phase 2 of 5\]|$phase|g" \
            -e "s|\[e\.g\., 60% complete, 3/5 increments done\]|$progress|g" \
            "$snapshot_file" 2>/dev/null || true
        rm -f "${snapshot_file}.bak" 2>/dev/null || true
        echo "DEBUG: Used sed fallback replacement" >&2
    fi
    
    log "INFO" "Snapshot template filling completed"
}

# Main execution
main() {
    echo "DEBUG: post-compact.sh started" >&2
    echo "DEBUG: PROJECT_DIR=$PROJECT_DIR" >&2
    echo "DEBUG: SNAPSHOT_DIR=$SNAPSHOT_DIR" >&2
    
    # Fill snapshot template if it exists
    local snapshot_file
    snapshot_file=$(get_most_recent_snapshot)
    
    echo "DEBUG: Most recent snapshot: $snapshot_file" >&2
    
    if [ -n "$snapshot_file" ]; then
        fill_snapshot_template "$snapshot_file"
    else
        log "INFO" "No snapshot file found to fill"
        echo "DEBUG: No snapshot file found to fill" >&2
    fi
    
    # Original functionality: Read and format afterCompact from prompt.json
    aftercompact_output=""
    if [ -f "$PROMPT_FILE" ]; then
        aftercompact_output=$(node -e "
            try {
                const data = require('$PROMPT_FILE');
                let output = '';

                // Format afterCompact sections
                if (data.afterCompact && Array.isArray(data.afterCompact) && data.afterCompact.length > 0) {
                    data.afterCompact.forEach(section => {
                        output += \`<\${section.tag}>\n\`;

                        // Add header if present
                        if (section.header) {
                            output += \`\${section.header}\n\n\`;
                        }

                        // Format instructions
                        if (section.instructions && Array.isArray(section.instructions)) {
                            output += \`**Instructions:**\n\`;
                            section.instructions.forEach(instruction => {
                                output += \`• \${instruction}\n\`;
                            });
                            output += \`\n\`;
                        }

                        // Format todos as checklist
                        if (section.todos && Array.isArray(section.todos)) {
                            output += \`**TodoWrite Checklist:**\n\`;
                            section.todos.forEach(todo => {
                                output += \`☐ \${todo}\n\`;
                            });
                        }

                        output += \`\n</\${section.tag}>\n\`;
                    });
                }

                console.log(output);
            } catch (error) {
                // Silently fail on parse errors
            }
        " 2>&1)
    fi

    # Escape output for JSON
    aftercompact_escaped=$(echo "$aftercompact_output" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | awk '{printf "%s\\n", $0}')

    # Output context injection as JSON
    if [ -n "$aftercompact_output" ]; then
        cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<CONTEXT-COMPACTION-RECOVERY>\nYour conversation context was just compacted.\n\n${aftercompact_escaped}\n</CONTEXT-COMPACTION-RECOVERY>"
  }
}
EOF
    fi

    exit 0
}

# Run main function
main
