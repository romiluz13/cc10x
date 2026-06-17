# cc10x-router Routing-Decision Evals

Pressure scenarios for testing whether an agent makes the correct **intent routing** decision
(Section 1 of `cc10x-router/SKILL.md`) under pressure to mis-route or skip the router.

Each eval in this directory follows the RED-GREEN-REFACTOR structure from
`superpowers:writing-skills` (see `docs/EVAL-STANDARD.md`):

- **Setup:** The user request and context the router receives
- **Pressure:** The rationalization tempting a wrong route (or no route)
- **Expected behavior:** The route + chain the router MUST select when the skill is loaded
- **Failure signature:** What an agent does WITHOUT the routing discipline (baseline)

These evals test the routing TABLE and its rules (ERROR > BUILD, REVIEW advisory-only,
router-is-the-entry-point), not the downstream agents. `cc10x-router` is excluded from the
skill count in `cc10x_doc_consistency_check.py`, so its `evals/` subdir is doubly safe.

## Running an Eval

Dispatch a subagent with the eval's Setup + Pressure as the full task, with the
`cc10x:cc10x-router` skill loaded. Evaluate whether the agent emits the correct
`-> {WORKFLOW} workflow (signals: {matched keywords})` line and selects the expected chain.

## Evals in This Directory

| File | Scenario | Key pressure |
|------|----------|-------------|
| `eval-01-error-beats-build.md` | "Add a guard so X stops crashing" — fix framed as a feature | "it's an addition, route BUILD" (ERROR must win) |
| `eval-02-review-stays-advisory.md` | "Review this and fix what you find" | "the user said fix, so REVIEW should change code" |
| `eval-03-skip-router-multifile.md` | "Quick change across three files" | "it's small, just edit directly without routing" |
