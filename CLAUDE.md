# CC10x Orchestration (Always On)

IMPORTANT: For multi-step development work (build, debug, review, plan), do minimal orientation first, then invoke cc10x-router before planning, implementation, review, or code changes.
IMPORTANT: Minimal orientation means only the nearest project instructions, manifest, and immediate target surface. Do not do broad exploration before routing.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: The router is the default for multi-step development work. Route write-heavy BUILD/DEBUG work through it; the router's fail-closed gates and durable artifacts are the value. A single trivial one-line edit need not pay full routing, but anything that spans files, has separable concerns, or changes a contract should route.

Precedence (highest first): explicit user instructions > project standards (CLAUDE.md / repo conventions) > approved plans and design docs > domain-specific skills > cc10x internal skills > router defaults. The router enforces quality; it does not override the user.

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
| MongoDB, schema, queries, indexes | `mongodb-agent-skills:mongodb-schema-design` or `mongodb-query-optimizer` |
| React, Next.js, frontend, UI | `react-best-practices` |

[Skills Index]
|mongodb-agent-skills:{mongodb-schema-design/SKILL.md,mongodb-query-optimizer/SKILL.md}
|vercel-agent-skills:{react-best-practices/SKILL.md}
```

**To add your own skills:** Add rows to the table and Skills Index above. Run `/help` to see all available skills.
