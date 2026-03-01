---
name: research
description: "Internal skill. Synthesis guidance loaded via SKILL_HINTS by planner and bug-investigator when research files are available."
allowed-tools: Read, Write, Edit, Bash
---

# Research Synthesis Guidance

## Overview

This skill is loaded via SKILL_HINTS by `cc10x:planner` and `cc10x:bug-investigator` when the router passes research files in the prompt. It provides instructions for synthesizing web and GitHub research findings.

**This skill does NOT execute research.** Research execution is done by:
- `cc10x:web-researcher` — runs Bright Data + WebSearch (spawned by router)
- `cc10x:github-researcher` — runs Octocode MCP tools (spawned by router, in parallel)

## Synthesis Goal

After the router passes both research file paths in your prompt, read those files and produce a synthesis that:
1. Answers the knowledge gap (the `Reason` field from your prompt)
2. Identifies the top 2-3 actionable patterns
3. Lists gotchas with solutions
4. Provides specific references for debugging

## What Makes Good Synthesis

**Include:**
- Cross-source confirmation (when web + GitHub agree on a pattern, it's reliable)
- Conflict resolution (when sources disagree, prefer GitHub real code over docs)
- Gotchas the user probably hasn't considered
- Specific code snippets only when they materially change the recommendation

**Exclude:**
- Raw dump of all findings (summarize)
- Obvious things the AI already knows
- Findings not relevant to the specific `Reason` for research

## Synthesis Format

```markdown
## Web Findings
[3-5 bullets from web research. Focus on patterns and gotchas.]

## GitHub Findings
[3-5 bullets from GitHub. Focus on real implementation patterns.]

## Synthesis

**Knowledge Gap answered:** [One sentence: what we now know that we didn't before]

**Recommended approach:** [1-3 sentences: what to do]

**Top patterns to apply:**
1. [Specific, actionable pattern]
2. [Specific, actionable pattern]

**Gotchas to avoid:**
- [Gotcha]: [Solution]

**References for debugging:**
- [URL or GitHub repo path]
```

## Handling Partial Research

If web researcher returned `[Web phase unavailable]`:
- Note it in the synthesis header: "Web research unavailable — GitHub only"
- Do not fabricate web findings
- Reduce confidence in synthesis accordingly

If GitHub researcher returned `[GitHub phase unavailable]`:
- Note it in the synthesis header: "GitHub research unavailable — Web only"
- Use web findings only for synthesis

If BOTH unavailable:
- Write: "Research unavailable — all sources down. Proceeding with AI knowledge only."
- Return STATUS=PARTIAL in Router Contract

## Memory Update After Synthesis

After writing the merged file:

```
Read(file_path=".claude/cc10x/activeContext.md")
Edit(file_path=".claude/cc10x/activeContext.md",
     old_string="## References",
     new_string="## References\n- Research: `{merged_file}` → {1-line insight}")
Read(file_path=".claude/cc10x/activeContext.md")  # VERIFY
```

Extract gotchas to patterns.md only if research found novel gotchas (not obvious ones).
