# AGENTS.md (CC10x Orchestration - Always On)

## Compact Instructions
Preserve: "CC10x orchestration ACTIVE. Resume via cc10x-router."

IMPORTANT: ALWAYS invoke cc10x-router on ANY development task. First action, no exceptions.
IMPORTANT: Explore project first, then invoke the router.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: Never bypass the router. It is the system.

[CC10x Orchestration Index]|root: ./plugins/cc10x
|router: skills/cc10x-router/SKILL.md
|agents: agents/{component-builder,bug-investigator,code-reviewer,silent-failure-hunter,integration-verifier,planner}.md
|skills: skills/{architecture-patterns,brainstorming,code-generation,code-review-patterns,debugging-patterns,frontend-patterns,github-research,planning-patterns,session-memory,test-driven-development,verification-before-completion}/SKILL.md

---

## Extending CC10x with Technology Skills (Optional)

CC10x handles orchestration (BUILD/DEBUG/REVIEW/PLAN workflows). For technology-specific expertise (MongoDB, React, etc.), add your skills to `~/.claude/CLAUDE.md` (global, applies to all projects).

**Why this pattern works (Vercel Research):**
- Skills with invocation = 79% pass rate (agent must decide to invoke)
- Index in CLAUDE.md = 100% pass rate (always available, no decision point)
- See: https://vercel.com/blog/how-we-teach-ai-agents-to-write-better-nextjs

**To add your technology skills:**

1. Check what skills you have installed (plugins, ~/.claude/skills/, etc.)
2. Add to your `~/.claude/CLAUDE.md`:

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
|vercel-agent-skills:{react-best-practices/SKILL.md,web-design-guidelines/SKILL.md,composition-patterns/SKILL.md}
```

**Rules:**
- CC10x orchestration (this file) = PRIMARY, never modify
- Technology skills = ADDITIVE, in your personal ~/.claude/CLAUDE.md
- Both use retrieval-led reasoning (agent reads files when needed)
