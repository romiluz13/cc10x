# CC10x Orchestration (Always On)

IMPORTANT: ALWAYS invoke cc10x-router on ANY development task. First action, no exceptions.
IMPORTANT: Explore project first, then invoke the router.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: Never bypass the router. It is the system.

[CC10x]|entry: ./plugins/cc10x/skills/cc10x-router/SKILL.md

---

## Extending with Technology Skills (Optional)

CC10x handles orchestration (BUILD/DEBUG/REVIEW/PLAN). For technology-specific expertise, add skills to your `~/.claude/CLAUDE.md` (global).

**Why this works (Vercel Research):**
- Skills with invocation = 79% pass rate
- Index in CLAUDE.md = 100% pass rate
- See: https://vercel.com/blog/how-we-teach-ai-agents-to-write-better-nextjs

**Add to `~/.claude/CLAUDE.md`:**
```markdown
# Technology Skills (Always On)

IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for technology-specific tasks.

[Tech Skills Index]
|{skill-source}:{skill-name/SKILL.md,...}
```

**Example:**
```markdown
[Tech Skills Index]
|mongodb-agent-skills:{mongodb-schema-design/SKILL.md,mongodb-query-and-index-optimize/SKILL.md}
|vercel-agent-skills:{react-best-practices/SKILL.md,web-design-guidelines/SKILL.md}
```
