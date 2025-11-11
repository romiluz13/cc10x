#!/usr/bin/env bash
# cc10x v4.3.9 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# Pre-prompt hook - Ensures orchestrator is loaded for code tasks
# Checks if user request matches workflow keywords and ensures orchestrator is loaded

set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
PROMPT_FILE="$PROJECT_DIR/.claude/prompt.json"

echo "DEBUG: pre-prompt.sh started" >&2
echo "DEBUG: PROJECT_DIR=$PROJECT_DIR" >&2
echo "DEBUG: PROMPT_FILE=$PROMPT_FILE" >&2

# Workflow keywords that should trigger orchestrator
WORKFLOW_KEYWORDS=(
  "review" "audit" "analyze" "assess" "evaluate" "inspect" "examine"
  "plan" "design" "architect" "roadmap" "strategy" "architecture" "system design"
  "build" "implement" "create" "write" "code" "develop" "make" "add feature" "implement feature" "build feature"
  "debug" "fix" "error" "bug" "investigate" "failure" "broken" "issue" "problem" "troubleshoot" "diagnose"
  "validate" "verify" "check" "confirm implementation" "alignment check" "consistency check"
)

# Code-writing keywords that should trigger orchestrator
CODE_KEYWORDS=(
  "write code" "create component" "build component" "implement feature"
  "add function" "create file" "write function" "implement"
)

# Read prompt from JSON file (if exists)
if [ -f "$PROMPT_FILE" ]; then
  echo "DEBUG: Prompt file found, parsing with Node.js" >&2
  USER_PROMPT=$(node -e "
    try {
      const data = require('$PROMPT_FILE');
      console.log(data.prompt || '');
    } catch (error) {
      console.error('ERROR: Failed to parse prompt.json:', error.message);
      console.log('');
      process.exit(1);
    }
  " 2>&1 || echo "")
  
  local node_exit_code=$?
  if [ $node_exit_code -eq 0 ]; then
    echo "DEBUG: Node.js script succeeded" >&2
  else
    echo "DEBUG: Node.js script failed (exit code: $node_exit_code)" >&2
    USER_PROMPT=""
  fi
else
  echo "DEBUG: Prompt file not found: $PROMPT_FILE" >&2
  USER_PROMPT=""
fi

echo "DEBUG: User prompt length: ${#USER_PROMPT}" >&2

# Check if prompt contains workflow keywords
should_load_orchestrator=false
matched_keywords=()

echo "DEBUG: Checking for workflow keywords..." >&2
for keyword in "${WORKFLOW_KEYWORDS[@]}" "${CODE_KEYWORDS[@]}"; do
  if echo "$USER_PROMPT" | grep -qi "$keyword"; then
    should_load_orchestrator=true
    matched_keywords+=("$keyword")
    echo "DEBUG: Matched keyword: $keyword" >&2
  fi
done

# If orchestrator should be loaded, output warning
if [ "$should_load_orchestrator" = true ]; then
  echo "DEBUG: Orchestrator enforcement triggered, outputting JSON" >&2
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PrePrompt",
    "additionalContext": "⚠️ ORCHESTRATOR ENFORCEMENT: Detected workflow keywords: ${matched_keywords[*]}. You MUST load cc10x-orchestrator skill FIRST before proceeding. DO NOT write code directly - use orchestrator to invoke subagents."
  }
}
EOF
else
  echo "DEBUG: No workflow keywords detected, skipping orchestrator enforcement" >&2
fi

echo "DEBUG: pre-prompt.sh completed" >&2
exit 0

