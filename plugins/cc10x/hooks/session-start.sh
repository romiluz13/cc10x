#!/bin/bash
# cc10x - 10x Developer Productivity with Claude Code
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
    
    # Initialize log file
    if ! touch "$LOG_FILE" 2>/dev/null; then
        error_exit "Failed to create log file: $LOG_FILE"
    fi
    
    log "INFO" "Directories initialized successfully"
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
- Use /feature-plan to plan new features
- Use /feature-build to implement features
- Use /bug-fix to fix issues systematically
- Use /review for multi-dimensional code review

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
    echo "║              cc10x - 10x Developer Productivity              ║"
    echo "║         Intelligent Orchestration with Claude Code           ║"
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

# Display available commands
display_commands() {
    echo "🎯 Available Commands:"
    echo ""
    echo "  /feature-plan <description>"
    echo "    → Create comprehensive PRD-style feature plans"
    echo "    → Architecture, API design, edge cases, test strategy"
    echo "    → 93% token savings via progressive loading"
    echo ""
    echo "  /feature-build <description>"
    echo "    → Complete feature implementation with strict TDD"
    echo "    → Context analysis → Planning → Implementation → Verification"
    echo "    → Lovable/Bolt-quality UI, production-ready code"
    echo ""
    echo "  /bug-fix <description>"
    echo "    → Systematic debugging with LOG FIRST pattern"
    echo "    → Minimal targeted changes, comprehensive tests"
    echo "    → Root cause analysis, regression prevention"
    echo ""
    echo "  /review <path>"
    echo "    → Multi-dimensional code review (security, quality, performance, UX, a11y)"
    echo "    → Parallel analysis across 5 dimensions"
    echo "    → Prioritized findings with actionable recommendations"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Display stats
display_stats() {
    echo "📈 System Status:"
    echo ""
    
    # Count components
    local commands_count agents_count skills_count
    commands_count=$(find commands -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    agents_count=$(find agents -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    skills_count=$(find skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
    
    echo "  Commands: $commands_count loaded"
    echo "  Agents: $agents_count loaded"
    echo "  Skills: $skills_count loaded"
    echo ""
}

# Main execution
main() {
    # Initialize session
    initialize_session
    
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
    
    # Check for snapshots
    check_snapshots
    
    # Initialize metrics
    initialize_metrics "$session_id"
    
    # Display stats
    display_stats
    
    # Display commands
    display_commands
    
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
