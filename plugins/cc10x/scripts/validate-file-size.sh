#!/bin/bash

# Validate files don't exceed 500 lines (USER RULE - CRITICAL!)
# Runs after every Write/Edit tool use via PostToolUse hook

# Read input from stdin if provided
if [ -t 0 ]; then
  # No stdin, exit silently
  exit 0
fi

# Try to parse JSON input from tool
file_path=$(echo "$STDIN" | jq -r '.tool_input.file_path // .tool_input.target_file // empty' 2>/dev/null)

# If jq failed or no file path, try reading directly
if [ -z "$file_path" ]; then
  exit 0
fi

# Check if file exists
if [ -f "$file_path" ]; then
  line_count=$(wc -l < "$file_path" 2>/dev/null || echo "0")
  
  if [ "$line_count" -gt 500 ]; then
    echo "⚠️  WARNING: $file_path exceeds 500 lines ($line_count lines)" >&2
    echo "" >&2
    echo "USER RULE VIOLATION: Files must be < 500 lines!" >&2
    echo "" >&2
    echo "This is a CRITICAL user rule. Split immediately:" >&2
    echo "  - Components: <200 lines" >&2
    echo "  - Utilities: <300 lines" >&2
    echo "  - Services: <400 lines" >&2
    echo "  - Config: <100 lines" >&2
    echo "" >&2
    echo "Example split strategy:" >&2
    echo "  large-file.ts ($line_count lines)" >&2
    echo "    ↓ Split into:" >&2
    echo "  core.ts (350 lines)" >&2
    echo "  utils.ts (250 lines)" >&2
    echo "  types.ts (150 lines)" >&2
    echo "" >&2
    exit 1
  fi
fi

exit 0

