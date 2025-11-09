#!/usr/bin/env bash
# cc10x v4.3.0 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# Notification hook for workflow completion
# Shows macOS notification when workflow completes

set -euo pipefail

# Check if terminal-notifier is installed
if ! command -v terminal-notifier &> /dev/null; then
  # Silently fail if terminal-notifier not installed
  exit 0
fi

# Read input data
DATA=$(cat)

# Extract transcript path
TRANSCRIPT=$(echo "$DATA" | jq -r '.transcript_path // ""' 2>/dev/null || echo "")

# Extract title from transcript summary if available
TITLE="cc10x Workflow"
if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
  SUMMARY=$(grep -m1 '"type":"summary"' "$TRANSCRIPT" 2>/dev/null | jq -r '.summary' 2>/dev/null || echo "")
  if [ -n "$SUMMARY" ]; then
    TITLE="$SUMMARY"
  fi
fi

# Extract workflow name if available
WORKFLOW=$(echo "$DATA" | jq -r '.workflow // "cc10x"' 2>/dev/null || echo "cc10x")

# Show notification
terminal-notifier \
  -message "Workflow completed: $WORKFLOW" \
  -title "$TITLE" \
  -sound Ping \
  2>/dev/null || true

exit 0

