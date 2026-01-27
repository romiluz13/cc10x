---
name: github-research
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: WebFetch, mcp__octocode__githubSearchCode, mcp__octocode__githubSearchRepositories, mcp__octocode__githubViewRepoStructure, mcp__octocode__githubGetFileContent, mcp__octocode__githubSearchPullRequests, mcp__octocode__packageSearch, mcp__context7__resolve-library-id, mcp__context7__query-docs, Read, Write, Edit, Bash
---

# External Code Research

## Overview

Research external patterns, documentation, and best practices from GitHub and library docs when AI knowledge is insufficient. Use Octocode MCP for GitHub research, Context7 MCP for library documentation, with WebFetch as final fallback.

**Core principle:** Research BEFORE building, not during. External research enhances planning, not execution.

**This skill is ONLY for external research.** Local codebase search is handled by other cc10x tools (Grep/Glob/Read).

## The Iron Law

```
NO EXTERNAL RESEARCH WITHOUT CLEAR AI KNOWLEDGE GAP OR EXPLICIT USER REQUEST
```

If AI training knowledge covers the technology well, skip external research - UNLESS user explicitly asks. This skill is for NEW technologies, complex integrations, unfamiliar APIs, and explicit user requests.

## When to Use

**ALWAYS invoke when:**
- User explicitly requests research ("research X", "how do others", "best practices", "find on github", "use octocode")
- Technology released after 2024 (AI knowledge cutoff)
- Complex integration patterns (auth, payments, real-time)
- Local debugging failed 3+ times with external service errors

**NEVER invoke when:**
- User says "quick" or "simple"
- Standard patterns AI knows well (CRUD, REST, React basics)
- Code review or refactoring tasks
- Technology released before 2024 (unless user explicitly asks)

**The rule:** Trust octocode for HOW. This skill only decides WHEN.

## Availability Check (REQUIRED)

**Before using Octocode tools, verify availability:**

```
# Try a simple package lookup to test MCP availability
mcp__octocode__packageSearch(name="express", ecosystem="npm")
```

**If Octocode unavailable → Fall back to Context7 MCP**
**If Context7 unavailable → Fall back to WebFetch**

## Research Process

### Phase 1: Confirm Need

Before using octocode tools, verify:
1. User explicitly requested research? → Proceed
2. Technology is post-2024? → Proceed
3. Complex integration with uncertainty? → Proceed
4. None of the above? → STOP. Use AI knowledge.

### Phase 2: Let Octocode Guide the Research

**Trust octocode's embedded guidance.** It will:
- Select the right tools and order
- Optimize queries for token efficiency
- Handle pagination and error recovery

**Your job:** Provide clear research goals in the tool parameters:
- `mainResearchGoal`: The overall question you're trying to answer
- `researchGoal`: What this specific query seeks to find
- `reasoning`: Why this query helps answer the main goal

### Phase 3: Summarize for cc10x Memory

Extract only what's needed for the task at hand:
- Key patterns/approaches found
- Gotchas or warnings discovered
- Specific code snippets (minimal)
- Links for future reference

**DO NOT dump entire files - summarize and cite.**

## Fallback Chain

```
TIER 1: Octocode MCP → TIER 2: Context7 MCP → TIER 3: WebFetch
```

Try each tier in order. Fall back only if current tier is unavailable or fails.

**NO LOCAL SEARCH** - This skill is for external research only. Local codebase search uses Grep/Glob/Read directly.

## Output Format

```markdown
## External Research Summary

**Knowledge Gap**: [What we didn't know]

**Research Conducted**:
- Source: [repo/docs URL]
- Query: [what we searched]

**Key Findings**:
1. [Pattern/approach found]
2. [Gotcha or warning]
3. [Relevant code snippet - minimal]

**Application to Task**:
[How this applies to current work]

**References Saved**:
- [URL for future debugging]
```

## Integration Points

**Two-Phase Execution (via cc10x-router):**

The router executes research BEFORE invoking agents. This is NOT a hint - it's a prerequisite.

```
1. Router detects github-research trigger (explicit request OR knowledge gap)
2. Router executes octocode tools directly (this skill's guidance)
3. Router passes research results to agent in prompt
```

**Research results passed to:**
- `planner` agent - For informed planning decisions
- `bug-investigator` agent - For external error patterns

**Never used during:**
- `code-reviewer` - Review focuses on code itself
- `silent-failure-hunter` - Speed is priority
- `integration-verifier` - Verification, not research

## Save Research (MANDATORY)

**Research insights are LOST after context compaction unless saved.** This section is NON-NEGOTIABLE.

### Step 1: Save Research File

```
# Create directory (permission-free)
Bash(command="mkdir -p docs/research")

# Save research using Write tool (permission-free for new files)
Write(file_path="docs/research/YYYY-MM-DD-<topic>-research.md", content="[full research from Output Format above]")
```

**File naming convention:** `YYYY-MM-DD-<topic>-research.md`
- Use today's date
- Use kebab-case for topic (e.g., `claude-code-tasks-system`, `react-server-components`)

### Step 2: Update Memory (Links Research to Memory)

**Use Edit tool (permission-free):**

```
# First read existing content
Read(file_path=".claude/cc10x/activeContext.md")

# Then append to Research References section using Edit
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## Research References",
     new_string="## Research References
| [Topic] | docs/research/YYYY-MM-DD-topic-research.md | [Key insight from findings] |")
```

**If Research References section doesn't exist, add it:**
```
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## Last Updated",
     new_string="## Research References
| Topic | File | Key Insight |
|-------|------|-------------|
| [Topic] | docs/research/YYYY-MM-DD-topic-research.md | [Key insight] |

## Last Updated")
```

### Step 3: Extract Patterns (Auto-Promote Learnings)

**If research found gotchas or reusable patterns, add to patterns.md:**

```
Read(file_path=".claude/cc10x/patterns.md")

Edit(file_path=".claude/cc10x/patterns.md",
     old_string="## Common Gotchas",
     new_string="## Common Gotchas
- [Gotcha from research]: [Solution] (Source: docs/research/YYYY-MM-DD-topic-research.md)")
```

**What to extract:**
- Error patterns and their solutions
- API quirks and workarounds
- Integration gotchas
- Best practices discovered

**What NOT to extract:**
- Task-specific implementation details
- One-time findings not applicable to future work
- Raw code snippets without context

### Step 4: Commit Research (Optional but Recommended)

```
Bash(command="git add docs/research/*.md")
Bash(command="git commit -m 'docs: add <topic> research'")
```

## Red Flags - Research NOT Complete

If you finish research WITHOUT:
- [ ] Saving to `docs/research/YYYY-MM-DD-topic-research.md`
- [ ] Updating `activeContext.md` with research reference
- [ ] Extracting patterns to `patterns.md` (if applicable)

**STOP. Research is NOT complete. Go back and save.**

## Why This Matters

```
WITHOUT SAVE:
Research → Context compaction → LOST FOREVER

WITH SAVE:
Research → docs/research/ → Memory reference → PERSISTS ACROSS SESSIONS
         → patterns.md → LEARNINGS COMPOUND
```

**Research without documentation is wasted effort.**
