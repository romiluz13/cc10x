# test-driven-development Evals

Pressure scenarios for testing whether an agent correctly follows the `test-driven-development` skill.

Each eval in this directory follows the RED-GREEN-REFACTOR structure from `superpowers:writing-skills`
(see `docs/EVAL-STANDARD.md`):

- **Setup:** The prompt and context the agent receives
- **Pressure:** The rationalization the agent is tempted to make
- **Expected behavior:** What the agent MUST do when the skill is loaded
- **Failure signature:** What the agent does WITHOUT the skill (baseline)

## Running an Eval

Dispatch a subagent with the eval's Setup + Pressure as the full task. The agent should have the
`cc10x:test-driven-development` skill loaded. Evaluate whether the agent's output matches `expected_behavior`.

## Evals in This Directory

| File | Scenario | Key pressure |
|------|----------|-------------|
| `eval-01-tests-after-rationalization.md` | Feature with the code already half-formed in the agent's head | "I'll write the test right after, it's faster" |
| `eval-02-too-simple-to-test.md` | A one-line validation helper | "this is too trivial to bother testing first" |
| `eval-03-keep-code-as-reference.md` | Agent already wrote the implementation before any test | "deleting it is wasteful, I'll keep it as reference" |
