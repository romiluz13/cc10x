#!/usr/bin/env bash
# cc10x v4.3.3 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# UserPromptSubmit hook - Combined skills enforcement and verification checklist
# Based on dotai's proven beforeStart/beforeComplete pattern

set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
PROMPT_FILE="$PROJECT_DIR/.claude/prompt.json"

echo "DEBUG: user-prompt-submit.sh started" >&2
echo "DEBUG: PROJECT_DIR=$PROJECT_DIR" >&2
echo "DEBUG: PROMPT_FILE=$PROMPT_FILE" >&2

# Read and format prompt from JSON file (only if file exists)
if [ -f "$PROMPT_FILE" ]; then
  echo "DEBUG: Prompt file found, parsing with Node.js" >&2
  # Use Node.js to parse JSON and format output
  FORMATTED_OUTPUT=$(node -e "
    try {
      const data = require('$PROMPT_FILE');
      let output = '';

      // Format beforeStart sections
      if (data.beforeStart && Array.isArray(data.beforeStart) && data.beforeStart.length > 0) {
        data.beforeStart.forEach(section => {
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

          output += \`\n</\${section.tag}>\n\n\`;
        });
      }

      // Format beforeComplete sections
      if (data.beforeComplete && Array.isArray(data.beforeComplete) && data.beforeComplete.length > 0) {
        data.beforeComplete.forEach(section => {
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
              output += \`- [ ] \${todo}\n\`;
            });
          }

          output += \`</\${section.tag}>\`;
        });
      }

      console.log(output);
    } catch (error) {
      console.error('ERROR: Failed to parse prompt.json:', error.message);
      process.exit(1);
    }
  " 2>&1)
  
  local node_exit_code=$?
  if [ $node_exit_code -eq 0 ]; then
    echo "DEBUG: Node.js script succeeded" >&2
  else
    echo "DEBUG: Node.js script failed (exit code: $node_exit_code)" >&2
    FORMATTED_OUTPUT=""
  fi
else
  echo "DEBUG: Prompt file not found: $PROMPT_FILE" >&2
  FORMATTED_OUTPUT=""
fi

# Escape output for JSON (handle newlines and quotes)
FORMATTED_OUTPUT_ESCAPED=$(echo "$FORMATTED_OUTPUT" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | awk '{printf "%s\\n", $0}')

# Only output JSON if FORMATTED_OUTPUT is non-empty
if [ -n "$FORMATTED_OUTPUT" ]; then
  echo "DEBUG: Outputting JSON with formatted content" >&2
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "${FORMATTED_OUTPUT_ESCAPED}"
  }
}
EOF
else
  echo "DEBUG: No formatted output, exiting without JSON" >&2
fi

echo "DEBUG: user-prompt-submit.sh completed" >&2
exit 0

