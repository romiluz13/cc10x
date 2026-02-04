# CC10x Orchestration (Always On)

IMPORTANT: ALWAYS invoke cc10x-router on ANY development task. First action, no exceptions.
IMPORTANT: Explore project first, then invoke the router.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: Never bypass the router. It is the system.
IMPORTANT: NEVER use Edit, Write, or Bash (for code changes) without first invoking cc10x-router.

**Skip CC10x ONLY when:**
- User EXPLICITLY says "don't use cc10x", "without cc10x", or "skip cc10x"
- No interpretation. No guessing. Only these exact opt-out phrases.

[CC10x]|entry: ./plugins/cc10x/skills/cc10x-router/SKILL.md

---

## Complementary Skills (Work Together with CC10x)

**Add to `~/.claude/CLAUDE.md`:**
```markdown
## Complementary Skills (Work Together with CC10x)

**Skills are additive, not exclusive.** CC10x provides orchestration. Domain skills provide expertise. Both work together.

**GATE:** Before writing code, check if task matches a skill below. If match, invoke it via `Skill(skill="...")`.

| When task involves... | Invoke |
|-----------------------|--------|
| MongoDB, schema, queries, indexes | `mongodb-agent-skills:mongodb-schema-design` or `mongodb-query-and-index-optimize` |
| React, Next.js, frontend, UI | `react-best-practices` |

[Skills Index]
|mongodb-agent-skills:{mongodb-schema-design/SKILL.md,mongodb-query-and-index-optimize/SKILL.md}
|vercel-agent-skills:{react-best-practices/SKILL.md}
```

**To add your own skills:** Add rows to the table and Skills Index above. Run `/help` to see all available skills.
