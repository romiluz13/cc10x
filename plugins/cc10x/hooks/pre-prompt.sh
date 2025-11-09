#!/usr/bin/env bash
# cc10x v4.2.0 - Orchestration plugin for Claude Code
# Copyright (c) 2025 Rom Iluz
# Licensed under MIT License

# Pre-prompt hook - Ensures orchestrator is loaded for code tasks
# Checks if user request matches workflow keywords and ensures orchestrator is loaded

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
PROMPT_FILE="$PROJECT_DIR/.claude/prompt.json"

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
  USER_PROMPT=$(node -e "
    try {
      const data = require('$PROMPT_FILE');
      console.log(data.prompt || '');
    } catch (error) {
      console.log('');
    }
  " 2>&1 || echo "")
else
  USER_PROMPT=""
fi

# Check if prompt contains workflow keywords
should_load_orchestrator=false
matched_keywords=()

for keyword in "${WORKFLOW_KEYWORDS[@]}" "${CODE_KEYWORDS[@]}"; do
  if echo "$USER_PROMPT" | grep -qi "$keyword"; then
    should_load_orchestrator=true
    matched_keywords+=("$keyword")
  fi
done

# If orchestrator should be loaded, output warning
if [ "$should_load_orchestrator" = true ]; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PrePrompt",
    "additionalContext": "⚠️ ORCHESTRATOR ENFORCEMENT: Detected workflow keywords: ${matched_keywords[*]}. You MUST load cc10x-orchestrator skill FIRST before proceeding. DO NOT write code directly - use orchestrator to invoke subagents."
  }
}
EOF
fi

exit 0

