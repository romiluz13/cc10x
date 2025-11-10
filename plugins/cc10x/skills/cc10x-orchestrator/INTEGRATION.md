# Orchestrator Integration Guides

Memory integration, web fetch integration, and context editing strategies.

## Memory Integration

**Purpose**: Use filesystem-based memory (`.claude/memory/`) to persist workflow state, patterns, and preferences across conversations.

**NOTE**: Anthropic's Memory Tool (API beta) is **NOT available in Claude Code**. This integration uses filesystem-based memory.

**Memory Usage**:

- **Before Complexity Scoring**: Query `.claude/memory/patterns.json` for similar tasks and use learned complexity scores as reference
- **After Workflow Completion**: Store workflow outcomes, learned patterns, and user preferences in JSON files
- **Pattern Learning**: Store complexity patterns, failure modes, and successful approaches in `.claude/memory/`

**What to Store**:

- Complexity patterns: `.claude/memory/patterns.json` → Task types → complexity scores → accuracy
- Failure modes: `.claude/memory/failure_modes.json` → Common errors → root causes → fixes
- User preferences: `.claude/memory/preferences.json` → Review depth, build approach, test coverage targets
- Workflow checkpoints: `.claude/memory/snapshots/` → Phase progress, component state, pending tasks

**Implementation**: See `plugins/cc10x/skills/memory-tool-integration/SKILL.md` for detailed guidance on filesystem-based memory usage patterns, including query patterns, storage procedures, and cleanup scripts.

**Memory Integration** (filesystem-based, optimized):

- **Validate Patterns First**: Compare predicted complexity → actual complexity
- **Update Accuracy**: Calculate accuracy = (matches / total_uses) \* 100
- **Update Confidence**: high (>80%), medium (60-80%), low (<60%)
- **Store Only Validated**: Only save patterns with accuracy > 50% after 3+ uses
- **Efficient Storage**: Use `Bash` + `jq` to update JSON files atomically
- **Run Cleanup**: Execute memory cleanup script after storing
- **Update Only**: Don't create new patterns without validation

**Memory Cleanup** (after workflow):

- Delete complexity patterns with accuracy < 50% (after 3+ uses)
- Delete unused patterns > 60 days old
- Keep top 20 most accurate patterns per project
- Delete failure modes unused > 30 days
- Delete failure modes with success rate < 60%

**Session Summary Generation** (automatic after workflow completion):

**CRITICAL:** This happens in Orchestrator Phase 5, AFTER all workflow phases complete. Workflow Phase 0-6 execute first, then Orchestrator Phase 5 compiles results.

**Process:**

1. **Load Memory Skill:** Reference `memory-tool-integration` skill
2. **Generate Session Summary:**
   - Extract file changes from workflow report (Actions Taken section)
   - Extract tool calls from Actions Taken section
   - Extract accomplishments from Findings/Decisions
   - Extract decisions from Recommendations
   - Extract next steps from Open Questions
3. **Save Session Summary:**
   - Format: Use dotai's session-summary.md template structure
   - Save to: `.claude/memory/session_summaries/session-{timestamp}.md`
   - Archive: If CURRENT_SESSION.md exists, archive to ARCHIVE/sessions/ (keep last 10)
4. **Update Working Plan** (if WORKING_PLAN.md exists):
   - Load `memory-tool-integration` skill
   - Update WORKING_PLAN.md with:
     - Completed tasks (from workflow report)
     - Current phase (from workflow type)
     - Next priorities (from Recommendations)
     - Session timestamp
   - Use minimal surgical updates (don't rewrite entire file)

## Web Fetch Integration

**Purpose**: Use Web Fetch Tool to load external documentation, API specifications, and reference materials when needed.

**When to Use**:

- External APIs mentioned: Fetch API documentation before planning
- Libraries/frameworks: Load documentation before building
- External services: Fetch service docs for integration
- Reference materials: Load guides, standards, best practices

**Integration Points**:

- **Planning Workflow**: Fetch API specs, framework docs, integration guides
- **Build Workflow**: Load library docs, SDK examples, framework guides
- **Review Workflow**: Fetch security standards, coding guidelines, best practices
- **Debug Workflow**: Load error docs, troubleshooting guides, stack trace resources

**Best Practices**:

- Cache frequently accessed docs
- Validate URLs before fetching
- Extract only relevant sections
- Cite sources in workflow output

**Integration**: Load `web-fetch-integration` skill for detailed guidance on web fetch usage.

**External Resource Check** (smart caching):

- **Check Cache First**: Lookup URL in `.claude/memory/web_cache/cache_index.json`
- **Use Cache if Valid**: If cached and TTL valid → use cache (skip fetch)
- **Re-fetch if Expired**: If cached but expired → re-fetch
- **Deduplication**: Track URLs fetched in this workflow, avoid duplicates
- **Batch Detection**: If multiple URLs needed, batch-fetch when possible
- Ask user: "Detected external dependencies: {list}. Check cache or fetch documentation? (yes/no)"

## Context Editing (Sep 2025)

**Available Strategies**:

- Clear older tool results when approaching limits
- Clear thinking blocks automatically (`clear_thinking_20251015`)
- Automatic context cleanup for long conversations

**For Long Workflows**:

- Explicit checkpointing at major phases
- Summarizing intermediate results
- Document state between phases
