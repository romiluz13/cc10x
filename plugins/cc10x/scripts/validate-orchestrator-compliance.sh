#!/usr/bin/env bash
set -euo pipefail

# Validate orchestrator compliance by checking workflow state and memory files
# This script is called automatically by orchestrator at key checkpoints

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
MEMORY_DIR="$ROOT_DIR/.claude/memory"
WORKFLOW_STATE_DIR="$MEMORY_DIR/workflow_state"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

validation_failed=false
missing_items=()

# Function to check if Actions Taken section exists in workflow state
check_actions_taken() {
  local workflow="$1"
  local phase="$2"
  
  # Check for workflow state file
  # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
  local state_file=$(find "$WORKFLOW_STATE_DIR" -name "${workflow}_*.json" -type f | sort -r | head -1)
  
  if [[ -z "$state_file" ]]; then
    echo -e "${RED}✗${NC} Actions Taken: No workflow state file found for $workflow workflow"
    validation_failed=true
    missing_items+=("Actions Taken section for $workflow workflow")
    return 1
  fi
  
  # Check if Actions Taken section exists in state file
  if ! jq -e '.actions_taken' "$state_file" >/dev/null 2>&1; then
    echo -e "${RED}✗${NC} Actions Taken: Missing actions_taken section in workflow state"
    validation_failed=true
    missing_items+=("Actions Taken section in workflow state")
    return 1
  fi
  
  echo -e "${GREEN}✓${NC} Actions Taken: Found in workflow state"
  return 0
}

# Function to check if required skills are loaded
check_skills_inventory() {
  local workflow="$1"
  # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
  local state_file=$(find "$WORKFLOW_STATE_DIR" -name "${workflow}_*.json" -type f | sort -r | head -1)
  
  if [[ -z "$state_file" ]]; then
    echo -e "${YELLOW}⚠${NC} Skills Inventory: Cannot check (no workflow state file)"
    return 0
  fi
  
  # Check if skills are documented in Actions Taken
  if jq -e '.actions_taken.skills_loaded' "$state_file" >/dev/null 2>&1; then
    # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
    local skills_count=$(jq '.actions_taken.skills_loaded | length' "$state_file" 2>/dev/null || echo "0")
    if [[ "$skills_count" -gt 0 ]]; then
      echo -e "${GREEN}✓${NC} Skills Inventory: $skills_count skills documented"
      return 0
    fi
  fi
  
  echo -e "${RED}✗${NC} Skills Inventory: No skills documented in Actions Taken"
  validation_failed=true
  missing_items+=("Skills inventory check")
  return 1
}

# Function to check if required subagents are invoked
check_subagents_inventory() {
  local workflow="$1"
  # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
  local state_file=$(find "$WORKFLOW_STATE_DIR" -name "${workflow}_*.json" -type f | sort -r | head -1)
  
  if [[ -z "$state_file" ]]; then
    echo -e "${YELLOW}⚠${NC} Subagents Inventory: Cannot check (no workflow state file)"
    return 0
  fi
  
  # Check if subagents are documented in Actions Taken
  if jq -e '.actions_taken.subagents_invoked' "$state_file" >/dev/null 2>&1; then
    # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
    local subagents_count=$(jq '.actions_taken.subagents_invoked | length' "$state_file" 2>/dev/null || echo "0")
    if [[ "$subagents_count" -gt 0 ]]; then
      echo -e "${GREEN}✓${NC} Subagents Inventory: $subagents_count subagents documented"
      return 0
    fi
  fi
  
  echo -e "${RED}✗${NC} Subagents Inventory: No subagents documented in Actions Taken"
  validation_failed=true
  missing_items+=("Subagents inventory check")
  return 1
}

# Function to check if TDD cycle was followed (for BUILD workflow)
check_tdd_cycle() {
  local workflow="$1"
  
  if [[ "$workflow" != "build" ]]; then
    return 0  # TDD only applies to BUILD workflow
  fi

  # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
  local state_file=$(find "$WORKFLOW_STATE_DIR" -name "${workflow}_*.json" -type f | sort -r | head -1)
  
  if [[ -z "$state_file" ]]; then
    echo -e "${YELLOW}⚠${NC} TDD Cycle: Cannot check (no workflow state file)"
    return 0
  fi
  
  # Check for TDD cycle evidence (RED → GREEN → REFACTOR)
  if jq -e '.actions_taken.tdd_cycle' "$state_file" >/dev/null 2>&1; then
    # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
    local has_red=$(jq -e '.actions_taken.tdd_cycle.red' "$state_file" >/dev/null 2>&1 && echo "true" || echo "false")
    # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
    local has_green=$(jq -e '.actions_taken.tdd_cycle.green' "$state_file" >/dev/null 2>&1 && echo "true" || echo "false")
    # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
    local has_refactor=$(jq -e '.actions_taken.tdd_cycle.refactor' "$state_file" >/dev/null 2>&1 && echo "true" || echo "false")
    
    if [[ "$has_red" == "true" && "$has_green" == "true" && "$has_refactor" == "true" ]]; then
      echo -e "${GREEN}✓${NC} TDD Cycle: RED → GREEN → REFACTOR documented"
      return 0
    fi
  fi
  
  echo -e "${RED}✗${NC} TDD Cycle: Missing TDD cycle evidence (RED → GREEN → REFACTOR)"
  validation_failed=true
  missing_items+=("TDD cycle evidence")
  return 1
}

# Function to check if memory integration was used
check_memory_integration() {
  # Check if patterns.json exists and has recent activity
  local patterns_file="$MEMORY_DIR/patterns.json"
  
  if [[ -f "$patterns_file" ]]; then
    # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
    local file_age=$(find "$patterns_file" -mtime -1 2>/dev/null && echo "recent" || echo "old")
    if [[ "$file_age" == "recent" ]]; then
      echo -e "${GREEN}✓${NC} Memory Integration: patterns.json found and recently updated"
      return 0
    else
      echo -e "${YELLOW}⚠${NC} Memory Integration: patterns.json exists but not recently updated"
      return 0  # Not a failure, just a warning
    fi
  fi
  
  echo -e "${YELLOW}⚠${NC} Memory Integration: patterns.json not found (may be first run)"
  return 0  # Not a failure, memory integration is optional for first run
}

# Function to check if web fetch integration was used
check_web_fetch_integration() {
  local cache_index="$MEMORY_DIR/web_cache/cache_index.json"
  
  if [[ -f "$cache_index" ]]; then
    # shellcheck disable=SC2155 # Exit code masking is intentional with set -euo pipefail
    local cache_count=$(jq '.entries | length' "$cache_index" 2>/dev/null || echo "0")
    if [[ "$cache_count" -gt 0 ]]; then
      echo -e "${GREEN}✓${NC} Web Fetch Integration: $cache_count cached entries found"
      return 0
    fi
  fi
  
  echo -e "${YELLOW}⚠${NC} Web Fetch Integration: No web cache found (may not be needed)"
  return 0  # Not a failure, web fetch is conditional
}

# Main validation function
main() {
  local workflow="${1:-}"
  local phase="${2:-}"
  
  if [[ -z "$workflow" ]]; then
    echo "Usage: $0 <workflow> [phase]"
    echo "  workflow: build|review|plan|debug|validate"
    echo "  phase: Phase number (optional, for phase-specific checks)"
    exit 1
  fi
  
  echo "Validating orchestrator compliance for $workflow workflow..."
  echo ""
  
  # Always check Actions Taken
  check_actions_taken "$workflow" "$phase"
  
  # Check Skills Inventory (before Phase 3)
  if [[ -z "$phase" ]] || [[ "$phase" -ge 3 ]]; then
    check_skills_inventory "$workflow"
  fi
  
  # Check Subagents Inventory (before Phase 4)
  if [[ -z "$phase" ]] || [[ "$phase" -ge 4 ]]; then
    check_subagents_inventory "$workflow"
  fi
  
  # Check TDD Cycle (for BUILD workflow, before Phase 4)
  if [[ "$workflow" == "build" ]] && { [[ -z "$phase" ]] || [[ "$phase" -ge 4 ]]; }; then
    check_tdd_cycle "$workflow"
  fi
  
  # Check Memory Integration (optional, informational)
  check_memory_integration
  
  # Check Web Fetch Integration (optional, informational)
  check_web_fetch_integration
  
  echo ""
  
  if [[ "$validation_failed" == "true" ]]; then
    echo -e "${RED}VALIDATION FAILED${NC}"
    echo ""
    echo "Missing items:"
    for item in "${missing_items[@]}"; do
      echo "  - $item"
    done
    echo ""
    echo "Please fix the issues above before proceeding."
    exit 1
  else
    echo -e "${GREEN}VALIDATION PASSED${NC}"
    exit 0
  fi
}

main "$@"

