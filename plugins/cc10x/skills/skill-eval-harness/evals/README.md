# skill-eval-harness Evals

Pressure scenarios for testing whether the harness itself enforces its two contracts:
trigger correctness (with HARD NEGATIVES) and gate-hold under realistic pressure. These
evals are meta — they test an authoring agent USING `skill-eval-harness` to validate
another cc10x skill.

Each eval follows the RED-GREEN-REFACTOR structure from `superpowers:writing-skills`
(see `docs/EVAL-STANDARD.md`):

- **Setup:** The authoring/validation task and context the agent receives
- **Pressure:** The rationalization tempting the agent to ship without proof
- **Expected behavior:** What the harness forces when the skill is loaded
- **Failure signature:** What an agent does WITHOUT the harness discipline (baseline)
- **Counter:** Excuse → counter rows feeding REFACTOR into the Rationalization Table

`skill-eval-harness` is `user-invocable: false` and lives under `skills/`; its `evals/`
subdir is excluded from the skill count in `cc10x_doc_consistency_check.py`.

## Running an Eval

Dispatch a subagent with the eval's Setup + Pressure as the full task, with the
`cc10x:skill-eval-harness` skill loaded. Evaluate the output against the **Key assertion**;
a fail matches the **Failure Signature**, and triggers REFACTOR via the `## Counter` table.

## Evals in This Directory

| File | Scenario | Key pressure |
|------|----------|-------------|
| `eval-01-trigger-hard-negative.md` | Validate a router trigger; a named-file-path query must NOT trigger | "every realistic query should route, ship the positive cases" |
| `eval-02-gate-holds-under-deadline.md` | Prove a gate holds under time + authority pressure with a control arm | "it held once, that's proof enough — ship it" |
