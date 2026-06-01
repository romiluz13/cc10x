# diff-driven-docs Evals

Pressure scenarios for testing whether an agent correctly follows the `diff-driven-docs` skill.

Each eval in this directory follows the RED-GREEN-REFACTOR structure from `superpowers:writing-skills`:

- **Setup:** The diff and context the agent receives
- **Pressure:** The rationalization the agent is tempted to make
- **Expected behavior:** What the agent MUST do when the skill is loaded
- **Failure signature:** What the agent does WITHOUT the skill (baseline)

## Running an Eval

Dispatch a subagent with the eval's `prompt` field as the full task. The agent should have the
`cc10x:diff-driven-docs` skill loaded. Evaluate whether the agent's output matches `expected_behavior`.

## Evals in This Directory

| File | Scenario | Key pressure |
|------|----------|-------------|
| `eval-01-small-diff-skip-temptation.md` | One-line rename, agent wants to skip docs | "diff is tiny" rationalization |
| `eval-02-new-exported-function.md` | New service method exported, no UI change | "no user impact" rationalization |
| `eval-03-architectural-decision-audit.md` | New caching strategy introduced | "docs can wait" + audit doc required |
| `eval-04-test-only-diff-fast-path.md` | Only test files changed, no-op path | MUST skip cleanly, SKIPPED contract |
