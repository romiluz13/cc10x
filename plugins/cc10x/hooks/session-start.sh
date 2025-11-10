#!/bin/bash
# cc10x v4.3.3 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# Session Start Hook - cc10x Orchestration System
# Initializes session with progress tracking and context management

set -euo pipefail

# Configuration
PROJECT_ROOT="$(pwd)"
MEMORY_DIR=".claude/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"
LOG_FILE="$MEMORY_DIR/session.log"
METRICS_FILE="$MEMORY_DIR/session_metrics.json"
WORKING_PLAN_PATH="$MEMORY_DIR/WORKING_PLAN.md"
REMEMBER_PATH="$MEMORY_DIR/REMEMBER.md"

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date +'%Y-%m-%d %H:%M:%S')"
    # Ensure directory exists before logging
    mkdir -p "$MEMORY_DIR" 2>/dev/null || true
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

# Initialize session
initialize_session() {
    log "INFO" "=== Session Start ==="
    log "INFO" "Project root: $PROJECT_ROOT"
    
    # Create directories if they don't exist
    if ! mkdir -p "$MEMORY_DIR" 2>/dev/null; then
        error_exit "Failed to create memory directory: $MEMORY_DIR"
    fi
    
    if ! mkdir -p "$SNAPSHOT_DIR" 2>/dev/null; then
        error_exit "Failed to create snapshot directory: $SNAPSHOT_DIR"
    fi
    
    # Ensure .claude directory exists
    if ! mkdir -p ".claude" 2>/dev/null; then
        error_exit "Failed to create .claude directory"
    fi
    
    # Auto-setup context.json if missing (critical for orchestrator enforcement)
    setup_context_json
    
    # Setup notifications (optional but recommended)
    setup_notifications
    
    # Initialize log file
    if ! touch "$LOG_FILE" 2>/dev/null; then
        error_exit "Failed to create log file: $LOG_FILE"
    fi
    
    log "INFO" "Directories initialized successfully"
}

# Setup context.json automatically if missing
setup_context_json() {
    local CONTEXT_JSON=".claude/context.json"
    local PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-plugins/cc10x}"
    local TEMPLATE_PATH="$PLUGIN_ROOT/templates/context.json"
    
    # Check if context.json already exists
    if [ -f "$CONTEXT_JSON" ]; then
        log "INFO" "context.json already exists, skipping auto-setup"
        return 0
    fi
    
    # Try to find template in plugin directory
    if [ ! -f "$TEMPLATE_PATH" ]; then
        # Try alternative paths
        TEMPLATE_PATH="plugins/cc10x/templates/context.json"
        if [ ! -f "$TEMPLATE_PATH" ]; then
            log "WARN" "context.json template not found at $TEMPLATE_PATH, skipping auto-setup"
            return 0
        fi
    fi
    
    # Find the actual plugin skill path (works for both local and marketplace installations)
    local ORCHESTRATOR_SKILL_PATH=""
    # Try marketplace installation path first
    if [ -f "$PLUGIN_ROOT/skills/cc10x-orchestrator/SKILL.md" ]; then
        ORCHESTRATOR_SKILL_PATH="$PLUGIN_ROOT/skills/cc10x-orchestrator/SKILL.md"
    elif [ -f "plugins/cc10x/skills/cc10x-orchestrator/SKILL.md" ]; then
        ORCHESTRATOR_SKILL_PATH="plugins/cc10x/skills/cc10x-orchestrator/SKILL.md"
    else
        # Try to find it relative to CLAUDE_PLUGIN_ROOT
        if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/skills/cc10x-orchestrator/SKILL.md" ]; then
            ORCHESTRATOR_SKILL_PATH="$CLAUDE_PLUGIN_ROOT/skills/cc10x-orchestrator/SKILL.md"
        else
            log "WARN" "Could not find orchestrator skill path, using default"
            ORCHESTRATOR_SKILL_PATH="plugins/cc10x/skills/cc10x-orchestrator/SKILL.md"
        fi
    fi
    
    # Create context.json with correct path
    if [ -f "$TEMPLATE_PATH" ]; then
        # Use sed to replace the hardcoded path with the actual path
        if sed "s|\"path\": \"plugins/cc10x/skills/cc10x-orchestrator/SKILL.md\"|\"path\": \"$ORCHESTRATOR_SKILL_PATH\"|g" "$TEMPLATE_PATH" > "$CONTEXT_JSON" 2>/dev/null; then
            log "INFO" "Auto-created context.json from template with path: $ORCHESTRATOR_SKILL_PATH"
            success "Auto-created .claude/context.json (required for orchestrator enforcement)"
        else
            log "WARN" "Failed to create context.json from template, user may need to create manually"
            info "⚠️  context.json not found. Please create .claude/context.json for orchestrator enforcement."
        fi
    else
        log "WARN" "context.json template not found, skipping auto-setup"
        info "⚠️  context.json template not found. Please create .claude/context.json manually."
    fi
}

# Setup terminal-notifier for notifications (optional but recommended)
setup_notifications() {
    local NOTIFIER_CHECK_FILE="$MEMORY_DIR/.notifier_checked"
    
    # Only check once per project (not every session)
    if [ -f "$NOTIFIER_CHECK_FILE" ]; then
        return 0
    fi
    
    # Check if terminal-notifier is installed
    if command -v terminal-notifier &> /dev/null; then
        log "INFO" "terminal-notifier found, notifications enabled"
        touch "$NOTIFIER_CHECK_FILE" 2>/dev/null || true
        return 0
    fi
    
    # Try to install via brew if available
    if command -v brew &> /dev/null; then
        log "INFO" "Attempting to install terminal-notifier via brew"
        if brew install terminal-notifier &>/dev/null 2>&1; then
            success "Installed terminal-notifier - notifications enabled"
            touch "$NOTIFIER_CHECK_FILE" 2>/dev/null || true
            return 0
        else
            log "WARN" "brew install terminal-notifier failed"
        fi
    fi
    
    # If brew install fails or brew not available, inform user once
    log "WARN" "terminal-notifier not found, notifications disabled"
    info "💡 Tip: Install terminal-notifier for workflow completion notifications:"
    info "   brew install terminal-notifier"
    touch "$NOTIFIER_CHECK_FILE" 2>/dev/null || true
}

# Generate session ID
generate_session_id() {
    local session_id
    session_id="$(date +%Y%m%d_%H%M%S)"
    echo "$session_id" > "$MEMORY_DIR/current_session.txt" 2>/dev/null || {
        error_exit "Failed to write session ID"
    }
    echo "$session_id"
}

# Check for active plan
check_active_plan() {
    local CURRENT_PLAN_FILE="$MEMORY_DIR/current_plan.txt"
    
    if [ -f "$CURRENT_PLAN_FILE" ]; then
        local plan_path
        plan_path=$(cat "$CURRENT_PLAN_FILE" 2>/dev/null | tr -d '\n' | tr -d '\r')
        
        if [ -n "$plan_path" ] && [ -f "$plan_path" ]; then
            log "INFO" "Active plan found: $plan_path"
            echo ""
            echo "📋 Active Plan: $plan_path"
            echo ""
            return 0
        else
            log "WARN" "current_plan.txt exists but plan file not found: $plan_path"
        fi
    fi
    
    return 0
}

# Load or create working plan
load_working_plan() {
    if [ -f "$WORKING_PLAN_PATH" ]; then
        log "INFO" "Working plan found: $WORKING_PLAN_PATH"
        success "Working plan loaded from previous session"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cat "$WORKING_PLAN_PATH" 2>/dev/null || {
            log "WARN" "Failed to read working plan"
            info "Working plan exists but couldn't be read"
        }
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        return 0
    else
        log "INFO" "No working plan found, creating default"
        if ! cat > "$WORKING_PLAN_PATH" << 'EOF'
# Current Priorities

## Active Tasks
- None yet

## Completed
- None yet

## Notes
- Session started: $(date)

## Next Steps
1. Review codebase structure
2. Identify immediate priorities
3. Create feature plans before building
EOF
        then
            log "WARN" "Failed to create default working plan"
            info "Couldn't create default working plan (will continue without it)"
            return 1
        fi
        
        log "INFO" "Default working plan created"
        info "No previous working plan found (created new one)"
        echo ""
        return 0
    fi
}

# Load important context
load_remember() {
    if [ -f "$REMEMBER_PATH" ]; then
        log "INFO" "Remember file found: $REMEMBER_PATH"
        success "Important context loaded from REMEMBER.md"
        echo ""
        return 0
    else
        log "INFO" "No remember file found"
        info "No REMEMBER.md found (optional context file)"
        echo ""
        return 0
    fi
}

# Check for previous snapshots
check_snapshots() {
    local snapshot_count
    snapshot_count=$(find "$SNAPSHOT_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$snapshot_count" -gt 0 ]; then
        log "INFO" "Found $snapshot_count previous snapshots"
        info "Found $snapshot_count previous context snapshots"
    else
        log "INFO" "No previous snapshots found"
        info "No previous snapshots (auto-healing will create them at 75% token usage)"
    fi
    echo ""
}

# Initialize session metrics
initialize_metrics() {
    local session_id="$1"
    local start_time
    start_time="$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%FT%TZ)"
    
    if ! cat > "$METRICS_FILE" << EOF
{
  "session_id": "$session_id",
  "start_time": "$start_time",
  "project_root": "$PROJECT_ROOT",
  "commands_executed": 0,
  "agents_invoked": 0,
  "skills_activated": 0,
  "files_modified": 0,
  "tests_run": 0,
  "commits_made": 0
}
EOF
    then
        log "WARN" "Failed to create metrics file"
        info "Metrics tracking unavailable (will continue without it)"
        return 1
    fi
    
    log "INFO" "Session metrics initialized"
    return 0
}

# Display welcome message
display_welcome() {
    local session_id="$1"
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║                    cc10x v4.3.3                              ║"
    echo "║         Orchestration Plugin for Claude Code                  ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    success "Session initialized successfully"
    echo ""
    echo "📊 Session ID: $session_id"
    echo "📂 Project: $PROJECT_ROOT"
    echo "💾 Memory: $MEMORY_DIR"
    echo ""
}


# Display stats
display_stats() {
    echo "📈 System Status:"
    echo ""
    
    # Count components
    local commands_count agents_count skills_count
    commands_count=$(find commands -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    agents_count=$(( \
        $(find agents -name "*.md" 2>/dev/null | wc -l | tr -d ' ') + \
        $(find subagents -name "*.md" 2>/dev/null | wc -l | tr -d ' ') \
    ))
    skills_count=$(find skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
    
    echo "  Commands: $commands_count loaded"
    echo "  Agents: $agents_count loaded"
    echo "  Skills: $skills_count loaded"
    echo ""
}

# Main execution
read_hook_input() {
    if [ -t 0 ]; then
        HOOK_INPUT=""
        return 0
    fi
    HOOK_INPUT=$(cat || true)
}

get_hook_field() {
    local field="$1"
    if [ -z "${HOOK_INPUT:-}" ]; then
        echo ""
        return 0
    fi
    if command -v jq >/dev/null 2>&1; then
        echo "$HOOK_INPUT" | jq -r ".${field} // empty" 2>/dev/null || echo ""
    else
        # Fallback: naive parse for simple top-level string fields
        echo "$HOOK_INPUT" | sed -n "s/.*\"${field}\"[[:space:]]*:[[:space:]]*\"\(.*\)\".*/\1/p" | head -n1
    fi
}

load_latest_snapshot() {
    if [ ! -d "$SNAPSHOT_DIR" ]; then
        echo ""
        return 0
    fi
    local latest
    latest=$(ls -1t "$SNAPSHOT_DIR"/snapshot-*.md 2>/dev/null | head -n1 || true)
    if [ -n "$latest" ] && [ -f "$latest" ]; then
        cat "$latest"
    else
        echo ""
    fi
}

load_skill_discovery() {
    local skill_file="${CLAUDE_PLUGIN_ROOT:-plugins/cc10x}/skills/skill-discovery/SKILL.md"
    if [ -f "$skill_file" ]; then
        cat "$skill_file" 2>/dev/null || echo ""
    else
        echo ""
    fi
}

main() {
    # Initialize session
    initialize_session
    # Read hook input (if any)
    read_hook_input

    # If resuming after compaction, emit JSON additionalContext ONLY and exit
    local source snapshot_content
    source=$(get_hook_field "source")
    if [ "$source" = "compact" ]; then
        snapshot_content=$(load_latest_snapshot)
        if [ -n "$snapshot_content" ]; then
            # Prefer jq for JSON string escape; fallback to Python if jq not available
            if command -v jq >/dev/null 2>&1; then
                printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' \
                    "$(printf %s "$snapshot_content" | jq -Rs .)"
            else
                printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' \
                    "$(printf %s "$snapshot_content" | python -c 'import sys,json;print(json.dumps(sys.stdin.read()))')"
            fi
        fi
        return 0
    fi

    # Load skill-discovery skill for all session starts (startup, resume, clear)
    local skill_discovery_content
    skill_discovery_content=$(load_skill_discovery)
    if [ -n "$skill_discovery_content" ]; then
        # Escape output for JSON
        local skill_discovery_escaped
        if command -v jq >/dev/null 2>&1; then
            skill_discovery_escaped=$(printf %s "$skill_discovery_content" | jq -Rs .)
        else
            skill_discovery_escaped=$(printf %s "$skill_discovery_content" | python -c 'import sys,json;print(json.dumps(sys.stdin.read()))')
        fi
        
        # Output skill-discovery as additionalContext
        printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' \
            "$skill_discovery_escaped"
    fi

    # Generate session ID
    local session_id
    session_id=$(generate_session_id)
    log "INFO" "Session ID: $session_id"
    
    # Display welcome
    display_welcome "$session_id"
    
    # Load working plan
    load_working_plan
    
    # Load remember context
    load_remember
    
    # Check for active plan
    check_active_plan
    
    # Check for snapshots
    check_snapshots
    
    # Initialize metrics
    initialize_metrics "$session_id"
    
    # Display stats
    display_stats

    # Final message
    log "INFO" "Session start complete"
    success "Ready for orchestration! 🚀"
    echo ""
    
    return 0
}

# Run main function
main

# Exit successfully
exit 0
