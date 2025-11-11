#!/usr/bin/env bash
# cc10x v4.4.0 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# Notification hook for compaction events
# Shows macOS notification before compaction

set -e

echo "DEBUG: notify-compact.sh started" >&2

# Check if terminal-notifier is installed
if ! command -v terminal-notifier &> /dev/null; then
  echo "DEBUG: terminal-notifier not installed, exiting silently" >&2
  # Silently fail if terminal-notifier not installed
  exit 0
fi

echo "DEBUG: terminal-notifier found, proceeding" >&2

# Read input data
DATA=$(cat || echo "")
echo "DEBUG: Read input data, length: ${#DATA}" >&2

# Extract transcript path (non-fatal jq parsing)
TRANSCRIPT=""
if command -v jq >/dev/null 2>&1; then
  TRANSCRIPT=$(echo "$DATA" | jq -r '.transcript_path // ""' 2>/dev/null || echo "")
  echo "DEBUG: Extracted transcript path: $TRANSCRIPT" >&2
else
  echo "DEBUG: jq not available, skipping transcript extraction" >&2
fi

# Extract title from transcript summary if available
TITLE="cc10x Workflow"
if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
  echo "DEBUG: Transcript file found, extracting summary" >&2
  SUMMARY=$(grep -m1 '"type":"summary"' "$TRANSCRIPT" 2>/dev/null | jq -r '.summary' 2>/dev/null || echo "")
  if [ -n "$SUMMARY" ]; then
    TITLE="$SUMMARY"
    echo "DEBUG: Using summary as title: $TITLE" >&2
  else
    echo "DEBUG: No summary found in transcript" >&2
  fi
else
  echo "DEBUG: No transcript file found, using default title" >&2
fi

# Show notification
echo "DEBUG: Showing notification with title: $TITLE" >&2
terminal-notifier \
  -message "Compacting conversation..." \
  -title "$TITLE" \
  -sound Bottle \
  2>/dev/null || {
    echo "DEBUG: Notification failed, continuing anyway" >&2
    true
  }

echo "DEBUG: notify-compact.sh completed" >&2
exit 0

