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
NO EXTERNAL RESEARCH WITHOUT CLEAR AI KNOWLEDGE GAP
```

If AI training knowledge covers the technology well, skip external research. This skill is for NEW technologies, complex integrations, and unfamiliar APIs.

## When to Use

**Signs you need external research:**
- Technology released after 2024 (AI knowledge cutoff)
- User mentions unfamiliar framework/library by name
- Integration pattern is complex (auth, payments, real-time)
- Local debugging failed 3+ times with same error
- User explicitly asks "how do others" or "best practices"
- Error message references external service behavior
- Documentation needed for third-party API

**Signs you DON'T need external research:**
- Standard patterns AI knows well (CRUD, REST, React basics)
- Simple bug with clear cause
- Code review (focus on the code itself)
- Refactoring existing code
- User says "quick" or "simple"
- Technology released before 2024 (AI has training data)

## Availability Check (REQUIRED)

**Before using Octocode tools, verify availability:**

```
# Try a simple package lookup to test MCP availability
mcp__octocode__packageSearch(name="express", ecosystem="npm")
```

**If Octocode unavailable → Fall back to Context7 MCP**
**If Context7 unavailable → Fall back to WebFetch**

## Research Process

### Phase 1: Confirm AI Knowledge Gap

Before external research, confirm the gap:
1. Is this technology released after 2024? (AI cutoff)
2. Is this a complex integration pattern I'm uncertain about?
3. Does the user explicitly need current documentation?

**If any are YES → Proceed to external research**

### Phase 2: Structured External Research

**For new technology documentation:**
```
packageSearch(name="<package>", ecosystem="npm|python")
→ githubViewRepoStructure(owner, repo, depth=1)
→ githubSearchCode(keywordsToSearch=["example", "usage"])
→ githubGetFileContent(matchString="<pattern>")
```

**For best practices/patterns:**
```
githubSearchRepositories(topicsToSearch=["<topic>"], stars=">1000")
→ githubSearchCode(keywordsToSearch=["<pattern>"])
→ githubGetFileContent(matchString="<implementation>")
```

**For debugging external issues:**
```
githubSearchPullRequests(owner, repo, query="<error>", state="closed")
→ Review PR comments for solutions
```

**Using Context7 for library documentation (TIER 2 fallback):**
```
# Step 1: Get library ID
mcp__context7__resolve-library-id(query="authentication", libraryName="next-auth")
→ Returns: /nextauthjs/next-auth

# Step 2: Query docs with specific question
mcp__context7__query-docs(libraryId="/nextauthjs/next-auth", query="How to set up JWT authentication")
→ Returns: Relevant documentation snippets
```

### Phase 3: Summarize Findings

**Extract only what's needed:**
- Key patterns/approaches found
- Gotchas or warnings discovered
- Specific code snippets (minimal)
- Links for future reference

**DO NOT dump entire files - summarize and cite.**

## Fallback Chain

```
TIER 1: Octocode MCP (GitHub research)
        ├── mcp__octocode__packageSearch (fastest - get repo URL)
        ├── mcp__octocode__githubSearchRepositories
        ├── mcp__octocode__githubSearchCode
        ├── mcp__octocode__githubViewRepoStructure
        ├── mcp__octocode__githubGetFileContent
        └── mcp__octocode__githubSearchPullRequests
        ↓ (if MCP unavailable/fails)

TIER 2: Context7 MCP (Library documentation)
        ├── mcp__context7__resolve-library-id (get library ID first)
        └── mcp__context7__query-docs (then fetch docs)
        ↓ (if MCP unavailable/fails)

TIER 3: WebFetch (Final fallback)
        └── WebFetch("<documentation-url>")
```

**NO LOCAL SEARCH** - This skill is for external research only. Local codebase search uses Grep/Glob/Read directly.

## Token Efficiency (CRITICAL)

**Octocode has built-in minification (30-70% reduction), but still optimize:**

| Do | Don't |
|----|-------|
| `matchString="function auth"` | `fullContent=true` on large files |
| `limit=5` for searches | `limit=100` (token explosion) |
| Get `metadata` first for PRs | `fullContent` on all PRs |
| One focused query | Multiple broad queries |

## Red Flags - STOP External Research

If you find yourself:

- Researching technology AI knows well (pre-2024)
- Searching for basic/well-known patterns (CRUD, REST, etc.)
- Dumping entire files into context (use matchString!)
- Researching during TDD RED→GREEN cycle (BUILD phase)
- Researching simple bugs (local debugging first)
- Making 5+ queries without finding useful info

**STOP. External research is a tool, not a crutch.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Let me check GitHub first" | Only if tech is post-2024 or complex integration |
| "I'll get more examples" | One good example is enough |
| "The docs might have changed" | Most APIs are stable - trust AI knowledge for basics |
| "Quick search won't hurt" | Token cost + time cost + context switching |
| "Maybe there's a newer pattern" | Use external research for NEW tech, not different approaches |

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

**Invoked by:**
- `planner` agent - During planning phase
- `bug-investigator` agent - When local debugging exhausted

**Never invoked by:**
- `code-reviewer` - Review focuses on code itself
- `silent-failure-hunter` - Speed is priority
- `integration-verifier` - Verification, not research
