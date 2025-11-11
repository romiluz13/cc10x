# Workflow Output Persistence Patterns

**CRITICAL**: This document defines MANDATORY persistence patterns for all workflows. All workflows MUST follow these patterns to ensure outputs survive context compaction and workflow interruptions.

## Standard Persistence Pattern

All workflows MUST implement the following persistence pattern in Phase 6 (final phase):

### 1. Save Output File

**Pattern**:

- Extract feature/scope name from Phase 0 functionality analysis or user request
- Use kebab-case for filename (e.g., `{workflow}-{scope}-{timestamp}.md`)
- Save output to `.claude/docs/{workflow}/{workflow}-{timestamp}.md`
- Ensure directory exists (create if needed)
- Format: Use exact template from workflow's "MANDATORY OUTPUT FORMAT" section

**Workflow-Specific Paths**:

- **Review**: `.claude/docs/reviews/review-{scope}-{timestamp}.md`
- **Build**: `.claude/docs/builds/build-{scope}-{timestamp}.md`
- **Debug**: `.claude/docs/debug/debug-{scope}-{timestamp}.md`
- **Plan**: `.claude/docs/plans/{feature-name}-plan.md` (already implemented)

**Bash Template**:

```bash
# Create directory if needed
mkdir -p .claude/docs/{workflow}

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Extract scope name from functionality analysis or use default
SCOPE_NAME="{workflow}"  # Replace with actual scope from Phase 0

# Save output file
OUTPUT_FILE=".claude/docs/{workflow}/{workflow}-${SCOPE_NAME}-${TIMESTAMP}.md"
# Write complete output to $OUTPUT_FILE
```

### 2. Create Reference File

**Pattern**:

- Create `.claude/memory/current_{workflow}.txt` containing the output file path
- This allows hooks and other workflows to find the active workflow output
- Overwrites previous reference (only one active workflow per type)

**Workflow-Specific Reference Files**:

- **Review**: `.claude/memory/current_review.txt`
- **Build**: `.claude/memory/current_build.txt`
- **Debug**: `.claude/memory/current_debug.txt`
- **Plan**: `.claude/memory/current_plan.txt` (already implemented)

**Bash Template**:

```bash
# Create reference file
echo "$OUTPUT_FILE" > .claude/memory/current_{workflow}.txt
```

### 3. Update Checkpoint with Output Path

**Pattern**:

- Update most recent checkpoint (`.claude/memory/workflow_state/{workflow}_{timestamp}.json`) to include:
  ```json
  {
    "output_file": ".claude/docs/{workflow}/{workflow}-{timestamp}.md",
    "output_saved": true
  }
  ```
- This enables checkpoint-based recovery to find the output file

**Checkpoint Format**:
All workflow checkpoints MUST include:

```json
{
  "workflow": "{workflow}",
  "phase": "Phase_N_...",
  "timestamp": "2025-01-29T10:00:00Z",
  "state": {...},
  "output_file": ".claude/docs/{workflow}/{workflow}-{timestamp}.md",
  "output_saved": false,
  "next_phase": "Phase_N+1_..."
}
```

**Update Logic**:

- Set `output_saved: false` initially (when checkpoint created)
- Set `output_saved: true` when output file is saved in Phase 6
- Update `output_file` with actual path when saved

## Compaction Safety

### Pre-Compact Hook Integration

The pre-compact hook (`pre-compact.sh`) automatically captures workflow outputs and extracts context:

1. **Validation**: Validates workflow outputs before compaction (warns if outputs not saved)
2. **Detection**: Checks for reference files (`.claude/memory/current_{workflow}.txt`)
3. **Capture**: Reads output file paths from reference files
4. **Summaries**: Includes first 200 lines of each output file in snapshot
5. **Snapshot**: Includes output paths and summaries in snapshot "Active Workflow Outputs" section
6. **Context Extraction**: Extracts git context, file changes, workflow state, and key decisions programmatically
7. **Enrichment**: Fills snapshot placeholders with real data (feature names, phases, progress, completions, next steps)
8. **Preservation**: Output paths and summaries survive compaction in snapshot
9. **Cleanup**: Automatically cleans old output files (keeps last 20 per workflow type)

**Validation Function**:

- `check_and_validate_workflow_outputs()`: Checks if workflows are active but outputs not saved, logs warnings

**Summary Function**:

- `get_workflow_output_summaries()`: Extracts first 200 lines of each output file for context recovery

**Context Extraction Functions**:

- `extract_git_context()`: Extracts recent commits, branch, staged/unstaged files with diffs, file change statistics
- `extract_file_changes()`: Lists recently modified files (last 2 hours) with sizes and line counts
- `extract_workflow_context()`: Extracts active workflow, current phase, progress, completed items, next steps from checkpoints
- `extract_feature_name()`: Extracts feature name from checkpoints or working plan
- `extract_key_decisions()`: Extracts key decisions from working plan

### Post-Compact Hook Integration

The post-compact hook (`post-compact.sh`) restores workflow outputs and loads comprehensive context:

1. **Restore from Snapshot**: Reads output paths from snapshot "Active Workflow Outputs" section
2. **Restore from Checkpoints**: If snapshot doesn't have outputs, restores from checkpoint `output_file` field
3. **Reference**: Recreates reference files (`.claude/memory/current_{workflow}.txt`) if missing
4. **Load Session Summary**: Loads comprehensive Claude-generated session summary from `.claude/memory/CURRENT_SESSION.md` or archive
5. **Combine Context**: Combines session summary (highest priority) → snapshot → afterCompact → workflow outputs
6. **Context**: Includes all context sources in restored context with proper priority ordering

**Restoration Functions**:

- `restore_workflow_outputs()`: Extracts output paths from snapshot and recreates reference files
- `restore_missing_references_from_checkpoints()`: Falls back to checkpoints if snapshot doesn't have outputs
- `fill_snapshot_template()`: Fills snapshot template placeholders with extracted context data

### Session Summary Integration

**CRITICAL**: Session summaries provide comprehensive Claude-generated context analysis before compaction.

**Session Summary Skill**:

- Skill path: `plugins/cc10x/skills/session-summary/SKILL.md`
- Creates comprehensive session documentation analyzing conversation transcript
- Extracts tool calls, file changes, accomplishments, decisions, next steps
- Saves to `.claude/memory/CURRENT_SESSION.md` and archives to `.claude/memory/session_summaries/session-{timestamp}.md`

**Workflow Integration**:

- **Phase 5.5 - Context Preservation**: Optional but recommended phase in all workflows
- Created before Phase 6 (final deliverable) when approaching token limits or after major phases
- Workflows load and execute session-summary skill to create comprehensive summaries
- Summaries complement programmatic snapshot extraction for complete context preservation

**When to Create Session Summary**:

- Approaching token limits (75%+ usage or user indicates)
- After major workflow phase completion (Phase 4 or Phase 5)
- Before final deliverable phase (Phase 6)
- User explicitly requests session summary

**Skip Conditions**:

- Context is small (<50% token usage)
- User explicitly skips
- Workflow is very simple (complexity <=2)
- No significant work completed

**Context Priority Order** (post-compact hook):

1. **Session Summary** (highest priority - most comprehensive, Claude-generated)
2. **Snapshot** (programmatic context extraction with real data)
3. **afterCompact Instructions** (from prompt.json)
4. **Workflow Outputs** (via reference files, restored automatically)

## Validation Checklist

Before completing Phase 6, ALL workflows MUST verify:

- [ ] Output file saved to `.claude/docs/{workflow}/{workflow}-{timestamp}.md`
- [ ] Reference file created: `.claude/memory/current_{workflow}.txt`
- [ ] Checkpoint updated with `output_file` and `output_saved: true`
- [ ] Output file contains complete report (all required sections)
- [ ] Output file path is valid and file exists

## Recovery Patterns

### From Checkpoint

If resuming from checkpoint:

1. Read checkpoint: `jq -s 'sort_by(.timestamp) | reverse | .[0]' .claude/memory/workflow_state/{workflow}_*.json`
2. Check `output_file` field: If exists and `output_saved: true`, output is available
3. Load output: Read output file if needed for context
4. Continue: Resume from `next_phase` with output available

### From Snapshot

If resuming from snapshot:

1. Read snapshot: Most recent `snapshot-*.md` from `.claude/memory/snapshots/`
2. Check "Active Workflow Outputs" section: Find output file paths
3. Load outputs: Read output files if needed for context
4. Restore references: Recreate reference files if needed

## Implementation Status

- ✅ **Plan Workflow**: Already implements persistence pattern + Phase 5.5 session summary integration
- ✅ **Review Workflow**: Added in Phase 6 (Phase 6 - Present Results) + Phase 5.5 session summary integration
- ✅ **Build Workflow**: Added in Phase 6 (Phase 6 - Delivery) + Phase 5.5 session summary integration
- ✅ **Debug Workflow**: Added in Phase 6 (Phase 6 - Report) + Phase 5.5 session summary integration
- ✅ **Pre-Compact Hook**: Captures workflow outputs automatically, validates before compaction, includes summaries, extracts context programmatically, fills snapshots with real data
- ✅ **Post-Compact Hook**: Restores workflow outputs from snapshot and checkpoints, loads session summaries, combines all context sources
- ✅ **Output Cleanup**: Automatically cleans old output files (keeps last 20 per workflow type)
- ✅ **Checkpoint Recovery**: Restores missing reference files from checkpoint `output_file` field
- ✅ **Session Summary Skill**: Created comprehensive session summary skill for Claude-generated context analysis
- ✅ **Context Extraction**: Pre-compact hook extracts git context, file changes, workflow state, and decisions programmatically

## Examples

### Review Workflow Example

```bash
# Phase 6: Present Results
mkdir -p .claude/docs/reviews
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SCOPE_NAME="auth-code-review"  # From Phase 0
REVIEW_FILE=".claude/docs/reviews/review-${SCOPE_NAME}-${TIMESTAMP}.md"

# Write review report to file
cat > "$REVIEW_FILE" << 'EOF'
# Review Report
...
EOF

# Create reference file
echo "$REVIEW_FILE" > .claude/memory/current_review.txt

# Update checkpoint
jq '.output_file = "'"$REVIEW_FILE"'" | .output_saved = true' \
  .claude/memory/workflow_state/review_*.json > .claude/memory/workflow_state/review_updated.json
mv .claude/memory/workflow_state/review_updated.json .claude/memory/workflow_state/review_*.json
```

### Build Workflow Example

```bash
# Phase 6: Delivery
mkdir -p .claude/docs/builds
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
FEATURE_NAME="user-authentication"  # From Phase 0
BUILD_FILE=".claude/docs/builds/build-${FEATURE_NAME}-${TIMESTAMP}.md"

# Write build summary to file
cat > "$BUILD_FILE" << 'EOF'
# Build Report
...
EOF

# Create reference file
echo "$BUILD_FILE" > .claude/memory/current_build.txt

# Update checkpoint
jq '.output_file = "'"$BUILD_FILE"'" | .output_saved = true' \
  .claude/memory/workflow_state/build_*.json > .claude/memory/workflow_state/build_updated.json
mv .claude/memory/workflow_state/build_updated.json .claude/memory/workflow_state/build_*.json
```

## Critical Rules

1. **MANDATORY**: All workflows MUST save outputs before presenting results
2. **MANDATORY**: All workflows MUST create reference files
3. **MANDATORY**: All workflows MUST update checkpoints with output paths
4. **MANDATORY**: Validation checklist MUST be completed before Phase 6 completion
5. **CRITICAL**: Outputs MUST be saved BEFORE compaction occurs (pre-compact hook captures them)

## References

- Review Workflow: `plugins/cc10x/skills/cc10x-orchestrator/workflows/review.md`
- Build Workflow: `plugins/cc10x/skills/cc10x-orchestrator/workflows/build.md`
- Debug Workflow: `plugins/cc10x/skills/cc10x-orchestrator/workflows/debug.md`
- Plan Workflow: `plugins/cc10x/skills/cc10x-orchestrator/workflows/plan.md`
- Pre-Compact Hook: `plugins/cc10x/hooks/pre-compact.sh`
- Post-Compact Hook: `plugins/cc10x/hooks/post-compact.sh`
