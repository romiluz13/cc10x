# CC10x Orchestration (Always On)

IMPORTANT: For multi-step development work (build, debug, review, plan), do minimal orientation first, then invoke cc10x-router before planning, implementation, review, or code changes.
IMPORTANT: Minimal orientation means only the nearest project instructions, manifest, and immediate target surface. Do not do broad exploration before routing.
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for orchestration decisions.
IMPORTANT: The router is the default for multi-step development work. Route write-heavy BUILD/DEBUG work through it; the router's fail-closed gates and durable artifacts are the value. A small edit still routes: the router runs a single trivial change as BUILD with trivial scope (a reduced task graph that keeps the verifier's proof path), and anything that spans files, has separable concerns, or changes a contract gets the full chain.

Precedence (highest first): explicit user instructions > project standards (CLAUDE.md / repo conventions) > approved plans and design docs > domain-specific skills > cc10x internal skills > router defaults. The router enforces quality; it does not override the user.

**Skip CC10x ONLY when:**
- User EXPLICITLY says "don't use cc10x", "without cc10x", or "skip cc10x"
- No interpretation. No guessing. Only these exact opt-out phrases.

In this repository the router is the skill at `plugins/cc10x/skills/cc10x-router/SKILL.md`.
