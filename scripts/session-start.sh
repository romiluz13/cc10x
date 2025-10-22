#!/bin/bash

# cc10x Session Start Hook
# Loads working plan and displays session context

set -e

WORKING_PLAN_PATH=".claude/memory/WORKING_PLAN.md"
REMEMBER_PATH=".claude/memory/REMEMBER.md"

echo "🚀 cc10x Session Starting..."
echo ""

# Check if working plan exists
if [ -f "$WORKING_PLAN_PATH" ]; then
    echo "📋 Loading working plan..."
    echo ""
    cat "$WORKING_PLAN_PATH"
    echo ""
else
    echo "ℹ️  No working plan found. Use /feature-plan to start a new feature."
    echo ""
fi

# Check if remember file exists (important context)
if [ -f "$REMEMBER_PATH" ]; then
    echo "💭 Important context loaded from REMEMBER.md"
    echo ""
fi

echo "✅ Session context loaded. Ready to work!"
echo ""
echo "Available commands:"
echo "  /feature-plan <description> - Plan a new feature"
echo "  /feature-build <description> - Build a feature"
echo "  /bug-fix <description> - Fix a bug systematically"
echo "  /review <files>  - Multi-dimensional code review"
echo ""
