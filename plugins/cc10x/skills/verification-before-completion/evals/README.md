# verification-before-completion Evals

Pressure scenarios for testing whether an agent correctly follows the
`verification-before-completion` skill.

Each eval in this directory follows the RED-GREEN-REFACTOR structure from
`superpowers:writing-skills` (see `docs/EVAL-STANDARD.md`):

- **Setup:** The prompt and context the agent receives
- **Pressure:** The rationalization the agent is tempted to make
- **Expected behavior:** What the agent MUST do when the skill is loaded
- **Failure signature:** What the agent does WITHOUT the skill (baseline)

## Running an Eval

Dispatch a subagent with the eval's Setup + Pressure as the full task. The agent should have the
`cc10x:verification-before-completion` skill loaded. Evaluate whether the agent's output matches
`expected_behavior` — specifically, whether every completion claim carries fresh evidence from
this session.

## Evals in This Directory

| File | Scenario | Key pressure |
|------|----------|-------------|
| `eval-01-should-pass-without-running.md` | Edit made, no command run, agent wants to call it done | "the change is obviously right, it should pass" |
| `eval-02-trust-agent-success-report.md` | Subagent reports success, parent about to mark complete | "the agent said it succeeded, that's enough" |
| `eval-03-partial-evidence-extrapolation.md` | Lint passed; agent claims build + tests pass too | "lint is green, so the rest is fine" |
