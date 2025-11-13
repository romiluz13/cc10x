#!/bin/bash
# cc10x v4.5.0 - Orchestration plugin for Claude Code
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

# Check and validate workflow outputs before compaction
check_and_validate_workflow_outputs() {
    log "INFO" "Validating workflow outputs before compaction"
    echo "DEBUG: Checking workflow outputs before compaction" >&2
    
    local warnings=0
    
    # Check each workflow type
    for workflow in review build debug plan; do
        local checkpoint_file
        checkpoint_file=$(find "$MEMORY_DIR/workflow_state" -name "${workflow}_*.json" -type f 2>/dev/null | sort | tail -1)
        
        if [ -z "$checkpoint_file" ] || [ ! -f "$checkpoint_file" ]; then
            continue
        fi
        
        # Check if workflow is active (recent checkpoint, within last hour)
        local checkpoint_age
        if [ -f "$checkpoint_file" ]; then
            checkpoint_age=$(find "$checkpoint_file" -mmin -60 2>/dev/null | wc -l)
            if [ "$checkpoint_age" -eq 0 ]; then
                continue  # Checkpoint is old, workflow likely inactive
            fi
        fi
        
        # Extract output status from checkpoint
        if command -v jq >/dev/null 2>&1; then
            local output_saved
            local output_file
            local phase
            output_saved=$(jq -r '.output_saved // false' "$checkpoint_file" 2>/dev/null)
            output_file=$(jq -r '.output_file // empty' "$checkpoint_file" 2>/dev/null)
            phase=$(jq -r '.phase // empty' "$checkpoint_file" 2>/dev/null)
            
            # Check if workflow is in Phase 6 or later (should have saved output)
            if echo "$phase" | grep -q "Phase_6\|Phase_5"; then
                if [ "$output_saved" != "true" ]; then
                    log "WARN" "Workflow ${workflow} is in ${phase} but output not saved (output_saved: ${output_saved})"
                    echo "DEBUG: WARNING - ${workflow} workflow output not saved before compaction" >&2
                    warnings=$((warnings + 1))
                fi
            fi
            
            # Check if reference file exists but output file doesn't
            local reference_file="$MEMORY_DIR/current_${workflow}.txt"
            if [ -f "$reference_file" ]; then
                local ref_path
                ref_path=$(cat "$reference_file" 2>/dev/null)
                if [ -n "$ref_path" ] && [ ! -f "$ref_path" ]; then
                    log "WARN" "Reference file exists for ${workflow} but output file missing: $ref_path"
                    echo "DEBUG: WARNING - Reference file exists but output file missing for ${workflow}" >&2
                    warnings=$((warnings + 1))
                fi
            fi
        fi
    done
    
    if [ "$warnings" -gt 0 ]; then
        log "WARN" "Found $warnings workflow output validation warnings before compaction"
        echo "DEBUG: Found $warnings validation warnings" >&2
    else
        log "INFO" "All workflow outputs validated successfully"
        echo "DEBUG: All workflow outputs validated" >&2
    fi
    
    return 0
}

# Get workflow output summaries (first 200 lines of each output file)
get_workflow_output_summaries() {
    local summaries=""
    
    # Check for review output
    if [ -f "$MEMORY_DIR/current_review.txt" ]; then
        local review_file
        review_file=$(cat "$MEMORY_DIR/current_review.txt" 2>/dev/null)
        if [ -n "$review_file" ] && [ -f "$review_file" ]; then
            local review_summary
            review_summary=$(head -n 200 "$review_file" 2>/dev/null | sed 's/^/  /')
            if [ -n "$review_summary" ]; then
                summaries="${summaries}Review Report Summary:\n\`\`\`markdown\n${review_summary}\n\`\`\`\n\n"
            fi
        fi
    fi
    
    # Check for build output
    if [ -f "$MEMORY_DIR/current_build.txt" ]; then
        local build_file
        build_file=$(cat "$MEMORY_DIR/current_build.txt" 2>/dev/null)
        if [ -n "$build_file" ] && [ -f "$build_file" ]; then
            local build_summary
            build_summary=$(head -n 200 "$build_file" 2>/dev/null | sed 's/^/  /')
            if [ -n "$build_summary" ]; then
                summaries="${summaries}Build Summary:\n\`\`\`markdown\n${build_summary}\n\`\`\`\n\n"
            fi
        fi
    fi
    
    # Check for debug output
    if [ -f "$MEMORY_DIR/current_debug.txt" ]; then
        local debug_file
        debug_file=$(cat "$MEMORY_DIR/current_debug.txt" 2>/dev/null)
        if [ -n "$debug_file" ] && [ -f "$debug_file" ]; then
            local debug_summary
            debug_summary=$(head -n 200 "$debug_file" 2>/dev/null | sed 's/^/  /')
            if [ -n "$debug_summary" ]; then
                summaries="${summaries}Debug Summary:\n\`\`\`markdown\n${debug_summary}\n\`\`\`\n\n"
            fi
        fi
    fi
    
    if [ -z "$summaries" ]; then
        echo ""
    else
        echo -e "$summaries"
    fi
}

# Get workflow output files if active
get_workflow_outputs() {
    local outputs=""
    
    # Check for review output
    if [ -f "$MEMORY_DIR/current_review.txt" ]; then
        local review_file
        review_file=$(cat "$MEMORY_DIR/current_review.txt" 2>/dev/null)
        if [ -n "$review_file" ] && [ -f "$review_file" ]; then
            outputs="${outputs}Review report: $review_file\n"
        fi
    fi
    
    # Check for build output
    if [ -f "$MEMORY_DIR/current_build.txt" ]; then
        local build_file
        build_file=$(cat "$MEMORY_DIR/current_build.txt" 2>/dev/null)
        if [ -n "$build_file" ] && [ -f "$build_file" ]; then
            outputs="${outputs}Build summary: $build_file\n"
        fi
    fi
    
    # Check for debug output
    if [ -f "$MEMORY_DIR/current_debug.txt" ]; then
        local debug_file
        debug_file=$(cat "$MEMORY_DIR/current_debug.txt" 2>/dev/null)
        if [ -n "$debug_file" ] && [ -f "$debug_file" ]; then
            outputs="${outputs}Debug summary: $debug_file\n"
        fi
    fi
    
    # Check for plan output
    if [ -f "$MEMORY_DIR/current_plan.txt" ]; then
        local plan_file
        plan_file=$(cat "$MEMORY_DIR/current_plan.txt" 2>/dev/null)
        if [ -n "$plan_file" ] && [ -f "$plan_file" ]; then
            outputs="${outputs}Plan: $plan_file\n"
        fi
    fi
    
    if [ -z "$outputs" ]; then
        echo "No active workflow outputs found"
    else
        echo -e "$outputs"
    fi
}

# Extract git context (recent commits, branch, diffs)
extract_git_context() {
    local git_context=""
    
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo ""
        return 0
    fi
    
    # Current branch
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    git_context="${git_context}**Branch**: $branch\n\n"
    
    # Recent commits (last hour)
    local recent_commits
    recent_commits=$(git log --since="1 hour ago" --pretty=format:"- %s (%h)" 2>/dev/null | head -5)
    if [ -n "$recent_commits" ]; then
        git_context="${git_context}**Recent Commits** (last hour):\n${recent_commits}\n\n"
    fi
    
    # Staged files with diff summaries (first 50 lines)
    local staged_files
    staged_files=$(git diff --cached --name-only 2>/dev/null)
    local staged_count=0
    if [ -n "$staged_files" ]; then
        git_context="${git_context}**Staged Files**:\n"
        while IFS= read -r file; do
            if [ -n "$file" ]; then
                staged_count=$((staged_count + 1))
                local diff_summary
                diff_summary=$(git diff --cached "$file" 2>/dev/null | head -50 | sed 's/^/  /')
                git_context="${git_context}- \`$file\`\n\`\`\`\n${diff_summary}\n\`\`\`\n"
            fi
        done <<< "$staged_files"
        git_context="${git_context}\n"
    fi
    
    # Unstaged files with diff summaries (first 50 lines)
    local unstaged_files
    unstaged_files=$(git diff --name-only 2>/dev/null)
    local unstaged_count=0
    if [ -n "$unstaged_files" ]; then
        git_context="${git_context}**Unstaged Files**:\n"
        while IFS= read -r file; do
            if [ -n "$file" ]; then
                unstaged_count=$((unstaged_count + 1))
                local diff_summary
                diff_summary=$(git diff "$file" 2>/dev/null | head -50 | sed 's/^/  /')
                git_context="${git_context}- \`$file\`\n\`\`\`\n${diff_summary}\n\`\`\`\n"
            fi
        done <<< "$unstaged_files"
        git_context="${git_context}\n"
    fi
    
    # File change statistics
    git_context="${git_context}**File Change Statistics**: $((staged_count + unstaged_count)) files changed ($staged_count staged, $unstaged_count unstaged)\n"
    
    echo -e "$git_context"
}

# Extract file changes (recently modified files)
extract_file_changes() {
    local file_changes=""
    
    # Find recently modified files (last 2 hours)
    local recent_files
    if command -v find >/dev/null 2>&1; then
        recent_files=$(find "$PROJECT_ROOT" -type f -mmin -120 -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/.claude/*" 2>/dev/null | head -20)
        
        if [ -n "$recent_files" ]; then
            file_changes="${file_changes}**Recently Modified Files** (last 2 hours):\n"
            while IFS= read -r file; do
                if [ -n "$file" ] && [ -f "$file" ]; then
                    local file_size line_count file_type
                    file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "unknown")
                    line_count=$(wc -l < "$file" 2>/dev/null | tr -d ' ' || echo "unknown")
                    file_type="${file##*.}"
                    file_changes="${file_changes}- \`$file\` ($file_type, ${file_size} bytes, ${line_count} lines)\n"
                fi
            done <<< "$recent_files"
            file_changes="${file_changes}\n"
        fi
    fi
    
    echo -e "$file_changes"
}

# Extract workflow context from checkpoints
extract_workflow_context() {
    local workflow_context=""
    local WORKFLOW_STATE_DIR="$MEMORY_DIR/workflow_state"
    
    if [ ! -d "$WORKFLOW_STATE_DIR" ]; then
        echo ""
        return 0
    fi
    
    # Find most recent checkpoint (try all workflow types)
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
    
    if ! command -v jq >/dev/null 2>&1; then
        echo ""
        return 0
    fi
    
    # Extract workflow info
    local workflow_name phase next_phase
    workflow_name=$(jq -r '.workflow // empty' "$checkpoint_file" 2>/dev/null)
    phase=$(jq -r '.phase // empty' "$checkpoint_file" 2>/dev/null)
    next_phase=$(jq -r '.next_phase // empty' "$checkpoint_file" 2>/dev/null)
    
    if [ -n "$workflow_name" ] && [ "$workflow_name" != "null" ]; then
        workflow_context="${workflow_context}**Active Workflow**: $workflow_name\n"
    fi
    
    if [ -n "$phase" ] && [ "$phase" != "null" ]; then
        workflow_context="${workflow_context}**Current Phase**: $phase\n"
    fi
    
    if [ -n "$next_phase" ] && [ "$next_phase" != "null" ]; then
        workflow_context="${workflow_context}**Next Phase**: $next_phase\n"
    fi
    
    # Extract progress based on workflow type
    case "$workflow_name" in
        "build")
            local total completed
            total=$(jq '[.state.components[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
            completed=$(jq '[.state.completed_components[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
            if [ "$total" -gt 0 ]; then
                local percent=$((completed * 100 / total))
                workflow_context="${workflow_context}**Progress**: $percent% complete ($completed/$total components)\n"
            fi
            ;;
        "plan")
            case "$phase" in
                *"Phase_0"*) workflow_context="${workflow_context}**Progress**: 0% complete (Functionality Analysis)\n" ;;
                *"Phase_1"*) workflow_context="${workflow_context}**Progress**: 20% complete (Requirements Intake)\n" ;;
                *"Phase_2"*) workflow_context="${workflow_context}**Progress**: 40% complete (Delegated Analysis)\n" ;;
                *"Phase_3"*) workflow_context="${workflow_context}**Progress**: 60% complete (Architecture Design)\n" ;;
                *"Phase_4"*) workflow_context="${workflow_context}**Progress**: 80% complete (Synthesis)\n" ;;
                *"Phase_5"*) workflow_context="${workflow_context}**Progress**: 90% complete (Verification)\n" ;;
            esac
            ;;
        "review")
            local total reviewed
            total=$(jq '[.state.files_reviewed[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
            reviewed=$(jq '[.state.files_reviewed[]? | select(.status == "reviewed")] | length' "$checkpoint_file" 2>/dev/null || echo "0")
            if [ "$total" -gt 0 ]; then
                local percent=$((reviewed * 100 / total))
                workflow_context="${workflow_context}**Progress**: $percent% complete ($reviewed/$total files reviewed)\n"
            fi
            ;;
        "debug")
            local total fixed
            total=$(jq '[.state.bugs[]?] | length' "$checkpoint_file" 2>/dev/null || echo "0")
            fixed=$(jq '[.state.bugs[]? | select(.status == "fixed")] | length' "$checkpoint_file" 2>/dev/null || echo "0")
            if [ "$total" -gt 0 ]; then
                local percent=$((fixed * 100 / total))
                workflow_context="${workflow_context}**Progress**: $percent% complete ($fixed/$total bugs fixed)\n"
            fi
            ;;
    esac
    
    # Extract completed items
    local completions=""
    case "$workflow_name" in
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
    
    if [ -n "$completions" ]; then
        workflow_context="${workflow_context}\n**Recent Completions**:\n${completions}\n"
    fi
    
    echo -e "$workflow_context"
}

# Extract feature name from checkpoint or working plan
extract_feature_name() {
    local checkpoint_file=""
    local WORKFLOW_STATE_DIR="$MEMORY_DIR/workflow_state"
    
    # Find most recent checkpoint
    for workflow in build plan review debug validate; do
        checkpoint_file=$(find "$WORKFLOW_STATE_DIR" -name "${workflow}_*.json" -type f 2>/dev/null | sort | tail -1)
        if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ]; then
            break
        fi
    done
    
    local feature_name="Unknown feature"
    
    # Try to extract from checkpoint
    if [ -n "$checkpoint_file" ] && [ -f "$checkpoint_file" ] && command -v jq >/dev/null 2>&1; then
        local name
        name=$(jq -r '.state.feature_name // .state.current_component // .state.current_bug // .workflow // empty' "$checkpoint_file" 2>/dev/null)
        if [ -n "$name" ] && [ "$name" != "null" ]; then
            feature_name="$name"
        fi
    fi
    
    # Fallback: try to extract from working plan
    if [ "$feature_name" = "Unknown feature" ] && [ -f "$WORKING_PLAN_PATH" ]; then
        local plan_name
        plan_name=$(grep -i "^#\|^##" "$WORKING_PLAN_PATH" 2>/dev/null | head -1 | sed 's/^#* *//' | sed 's/ *$//')
        if [ -n "$plan_name" ]; then
            feature_name="$plan_name"
        fi
    fi
    
    echo "$feature_name"
}

# Extract key decisions from working plan
extract_key_decisions() {
    local decisions=""
    
    if [ ! -f "$WORKING_PLAN_PATH" ]; then
        echo ""
        return 0
    fi
    
    # Extract sections that might contain decisions
    local decision_sections
    decision_sections=$(grep -A 10 -i "decision\|decide\|choice\|approach\|pattern" "$WORKING_PLAN_PATH" 2>/dev/null | head -20)
    
    if [ -n "$decision_sections" ]; then
        decisions="${decisions}**From Working Plan**:\n\`\`\`\n${decision_sections}\n\`\`\`\n"
    fi
    
    echo -e "$decisions"
}

# Create comprehensive snapshot
create_snapshot() {
    local session_id
    local metrics
    local working_plan
    local git_changes
    local workflow_outputs
    local workflow_summaries
    
    echo "DEBUG: Creating snapshot..." >&2
    session_id=$(get_session_id)
    metrics=$(get_metrics)
    working_plan=$(get_working_plan)
    git_changes=$(count_git_changes)
    workflow_outputs=$(get_workflow_outputs)
    workflow_summaries=$(get_workflow_output_summaries)
    
    # Extract enriched context
    local feature_name
    local workflow_context
    local git_context
    local file_changes
    local key_decisions
    
    feature_name=$(extract_feature_name)
    workflow_context=$(extract_workflow_context)
    git_context=$(extract_git_context)
    file_changes=$(extract_file_changes)
    key_decisions=$(extract_key_decisions)
    
    # Extract next steps from workflow context
    local next_steps="1. Review snapshot context\n2. Continue workflow from last checkpoint\n3. Verify current state"
    if echo "$workflow_context" | grep -q "Next Phase"; then
        local next_phase
        next_phase=$(echo "$workflow_context" | grep "Next Phase" | sed 's/.*Next Phase**: //' | head -1)
        if [ -n "$next_phase" ] && [ "$next_phase" != "null" ]; then
            next_steps="1. Continue to $next_phase\n2. Verify current state\n3. Complete remaining tasks"
        fi
    fi
    
    # Extract recent completions from workflow context
    local recent_completions="- No recent completions recorded"
    if echo "$workflow_context" | grep -q "Recent Completions"; then
        recent_completions=$(echo "$workflow_context" | sed -n '/Recent Completions/,/^$/p' | tail -n +2 | head -10)
        if [ -z "$recent_completions" ]; then
            recent_completions="- No recent completions recorded"
        fi
    fi
    
    # Extract phase and progress from workflow context
    local phase="Unknown phase"
    local progress="Progress unknown"
    if echo "$workflow_context" | grep -q "Current Phase"; then
        phase=$(echo "$workflow_context" | grep "Current Phase" | sed 's/.*Current Phase**: //' | head -1)
    fi
    if echo "$workflow_context" | grep -q "Progress"; then
        progress=$(echo "$workflow_context" | grep "Progress" | sed 's/.*Progress**: //' | head -1)
    fi
    
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

## Git Context

$git_context

---

## File Changes

$file_changes

---

## Active Work

### Current Task
- Feature/Bug: $feature_name
- Phase: $phase
- Progress: $progress

### Recent Completions
$recent_completions

### Next Steps
$next_steps

### Active Workflow Context

$workflow_context

### Active Workflow Outputs (To Be Filled by Claude)

**CRITICAL**: If a workflow is active, capture its output file path:

- **Review Workflow**: Check `.claude/memory/current_review.txt` → If exists, read review report path
- **Build Workflow**: Check `.claude/memory/current_build.txt` → If exists, read build summary path
- **Debug Workflow**: Check `.claude/memory/current_debug.txt` → If exists, read debug summary path
- **Plan Workflow**: Check `.claude/memory/current_plan.txt` → If exists, read plan path

**Workflow Output Files**:
- Review report: [path from current_review.txt if exists]
- Build summary: [path from current_build.txt if exists]
- Debug summary: [path from current_debug.txt if exists]
- Plan: [path from current_plan.txt if exists]

**Active Workflow Outputs** (Auto-detected):

\`\`\`
$workflow_outputs
\`\`\`

**Note**: These outputs are preserved in snapshot to enable recovery after compaction.

**Workflow Output Summaries** (First 200 lines):

$workflow_summaries

---

## Key Decisions Made

$key_decisions

**Note**: Additional decisions may be documented in WORKING_PLAN.md or workflow checkpoints.

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
- Context extracted programmatically from git, checkpoints, and working plan
- Previous snapshots are retained (up to $MAX_SNAPSHOTS most recent)
- Snapshots are cleaned up automatically (oldest removed first)
- For comprehensive session summaries, see `.claude/memory/CURRENT_SESSION.md` or `.claude/memory/session_summaries/`

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

# Clean old workflow output files (keep last 20 per workflow type)
cleanup_old_outputs() {
    local MAX_OUTPUTS=20
    
    log "INFO" "Cleaning old workflow output files (keeping last $MAX_OUTPUTS per type)"
    echo "DEBUG: Cleaning old workflow outputs" >&2
    
    # Clean review outputs
    local review_dir="$PROJECT_ROOT/.claude/docs/reviews"
    if [ -d "$review_dir" ]; then
        local review_count
        review_count=$(find "$review_dir" -name "review-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
        if [ "$review_count" -gt "$MAX_OUTPUTS" ]; then
            local to_remove=$((review_count - MAX_OUTPUTS))
            find "$review_dir" -name "review-*.md" -type f | sort | head -n "$to_remove" | xargs rm -f 2>/dev/null || true
            log "INFO" "Cleaned $to_remove old review outputs"
        fi
    fi
    
    # Clean build outputs
    local build_dir="$PROJECT_ROOT/.claude/docs/builds"
    if [ -d "$build_dir" ]; then
        local build_count
        build_count=$(find "$build_dir" -name "build-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
        if [ "$build_count" -gt "$MAX_OUTPUTS" ]; then
            local to_remove=$((build_count - MAX_OUTPUTS))
            find "$build_dir" -name "build-*.md" -type f | sort | head -n "$to_remove" | xargs rm -f 2>/dev/null || true
            log "INFO" "Cleaned $to_remove old build outputs"
        fi
    fi
    
    # Clean debug outputs
    local debug_dir="$PROJECT_ROOT/.claude/docs/debug"
    if [ -d "$debug_dir" ]; then
        local debug_count
        debug_count=$(find "$debug_dir" -name "debug-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
        if [ "$debug_count" -gt "$MAX_OUTPUTS" ]; then
            local to_remove=$((debug_count - MAX_OUTPUTS))
            find "$debug_dir" -name "debug-*.md" -type f | sort | head -n "$to_remove" | xargs rm -f 2>/dev/null || true
            log "INFO" "Cleaned $to_remove old debug outputs"
        fi
    fi
    
    # Note: Plan outputs are kept indefinitely (they're referenced by build workflow)
    # Plans are cleaned up separately if needed
}

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
    
    # Validate workflow outputs before creating snapshot
    check_and_validate_workflow_outputs
    
    # Create snapshot
    create_snapshot
    
    # Clean old snapshots
    cleanup_old_snapshots
    
    # Clean old workflow outputs
    cleanup_old_outputs
    
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
