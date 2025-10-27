#!/bin/bash

# CC10x File Size Check Hook
# Enforces 500-line file size limit

# Read hook input from stdin
input=$(cat)

# Extract file path from tool_input
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.target_file // empty')

# Skip if no file path
if [ -z "$file_path" ]; then
  exit 0
fi

# Skip if file doesn't exist yet
if [ ! -f "$file_path" ]; then
  exit 0
fi

# Count lines
line_count=$(wc -l < "$file_path" | tr -d ' ')

# Check limit
if [ "$line_count" -gt 500 ]; then
  cat << EOF
{
  "continue": true,
  "messages": [
    {
      "type": "text",
      "text": "⚠️  **FILE SIZE WARNING**\n\nFile \`$file_path\` has **$line_count lines** (limit: 500)\n\n**Action Required:** Please split this file into smaller, focused modules.\n\n**Best Practices:**\n- Keep functions small (< 50 lines)\n- Extract related functions into separate modules\n- Create focused, single-responsibility files\n\nThis improves maintainability and follows CC10x standards."
    }
  ]
}
EOF
  exit 2
fi

# Pass - file is within limits
exit 0

