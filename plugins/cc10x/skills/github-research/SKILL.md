---
name: github-research
description: "Internal skill. Use cc10x-router for all development tasks."
allowed-tools: WebFetch, mcp__octocode__githubSearchCode, mcp__octocode__githubSearchRepositories, mcp__octocode__githubViewRepoStructure, mcp__octocode__githubGetFileContent, mcp__octocode__githubSearchPullRequests, mcp__octocode__packageSearch, mcp__context7__resolve-library-id, mcp__context7__query-docs
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
