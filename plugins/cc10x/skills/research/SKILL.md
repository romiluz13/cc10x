---
name: research
description: "Internal skill. Synthesis guidance loaded via SKILL_HINTS by planner and bug-investigator when research files are available."
allowed-tools: Read
---

# Research Synthesis Guidance

## Overview

This skill is loaded via SKILL_HINTS by `cc10x:planner` and `cc10x:bug-investigator` when the router passes research files in the prompt. It provides instructions for synthesizing web and GitHub research findings.

**This skill does NOT execute research.** Research execution is done by:
- `cc10x:web-researcher` — prefers Bright Data, falls back to WebSearch/WebFetch
- `cc10x:github-researcher` — prefers Octocode MCP, falls back to package/docs/GitHub web research

## Synthesis Goal

After the router passes research file paths in your prompt, read the available files and produce a synthesis that:
1. Answers the knowledge gap (the `Reason` field from your prompt)
2. Identifies the top 2-3 actionable patterns
3. Lists gotchas with solutions
4. Provides specific references for debugging
5. Reflects evidence quality honestly
6. States the single finding that most changed the recommendation

## What Makes Good Synthesis

**Include:**
- Cross-source confirmation (when web + GitHub agree on a pattern, it's reliable)
- Conflict resolution (when sources disagree, prefer GitHub real code over docs)
- Confidence calibration from the router-provided `## Research Quality` block
- Gotchas the user probably hasn't considered
- Specific code snippets only when they materially change the recommendation

**Exclude:**
- Raw dump of all findings (summarize)
- Obvious things the AI already knows
- Findings not relevant to the specific `Reason` for research

## Synthesis Format

```markdown
## Evidence Quality
- Web: [high / medium / low / none]
- GitHub: [high / medium / low / none]
- Overall confidence: [high / medium / low]

## Web Findings
[3-5 bullets from web research. Focus on patterns and gotchas.]

## GitHub Findings
[3-5 bullets from GitHub. Focus on real implementation patterns.]

## Synthesis

**Knowledge Gap answered:** [One sentence: what we now know that we didn't before]

**Recommended approach:** [1-3 sentences: what to do]

**What changed the recommendation most:** [single sentence]

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
- State clearly: "Research unavailable — all sources down. Proceeding with AI knowledge only."
- Lower confidence and rely on repo-local evidence first.

Quality weighting:
- `high`: multiple concrete sources or code-backed findings
- `medium`: one strong source or partial cross-confirmation
- `low`: indirect, sparse, or web-only/package-only signals
- `none`: no usable external findings

## Memory Output

Do not edit `.claude/cc10x/*.md` directly from this skill or from the host agent.

Instead, surface the most durable takeaway through the host agent's `MEMORY_NOTES`, for example:
- one research-backed gotcha worth preserving
- one reference path worth indexing
- one confidence caveat if research quality was degraded
