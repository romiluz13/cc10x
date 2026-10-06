# Prompt Change Checklist

Use this checklist for every future CC10X prompt edit.

## 1. Classify The Change

Choose exactly one:
- `metadata_only`
- `wording_only_low_risk`
- `wording_only_trust_sensitive`
- `orchestration_sensitive`

If the change is `orchestration_sensitive`, stop. Do not ship it as a prompt-only round.

## 2. Semantic Drift Review

Review each changed prompt against these questions:

- Authority drift: did explicit user instructions, `CLAUDE.md`, or repo standards lose precedence?
- Obligation drift: did `must`, `required`, `blocking`, or `fail` weaken into `should`, `prefer`, `recommend`, or `can`?
- Scope drift: did advisory language become policy, or policy become advisory?
- Approval drift: did a recommendation, default, or example become implied approval?
- Duplication drift: did a second version of the same rule appear with slightly different wording?
- Runtime drift risk: does the new wording imply new behavior even if code did not change?

If any answer is “yes” and the change is not intentionally designed and documented, reject the edit.

## 3. Tier-Based Review Requirements

### Tier 1 changed
- Run `python3 plugins/cc10x/tools/harness_audit.py`
- Run `python3 plugins/cc10x/tools/workflow_replay_check.py`
- Perform manual semantic review
- Perform prompt diff review against the prior version
- Write/update a benchmark note

### Tier 2 changed
- Run audit
- Perform targeted semantic review
- Add benchmark note only if trust-sensitive language changed

### Tier 3 changed
- Run audit
- Check description hygiene
- No replay review needed unless authority wording changed

## 4. Required Manual Review Outcomes

For each changed Tier 1 prompt, confirm:
- fail-closed behavior preserved
- no hidden approval drift
- authority hierarchy preserved
- no workflow-topology implication introduced
- required trust phrases or contract markers still present

## 5. Benchmark Note Requirements

Every major prompt-only round must record:
- what changed
- why it is safe
- which external reference or prior pattern informed it
- which prompt surfaces changed
- whether the change copied wording, structure, or only principle
- which invariants were intentionally untouched
- the honest claim boundary after the change

## 6. Merge Gate

Do not merge a prompt-only change unless:
- audit passes
- replay checks pass
- manual review is complete for all changed Tier 1 prompts
- the change classification is recorded
- the benchmark note exists when required

## 7. Release Gate

Run the gate from the repo root before any merge or release:

```
python3 plugins/cc10x/tools/release_gate.py
```

It runs these nine steps in order; `--list` prints the ids, `--only <step-id>` (repeatable) runs a subset, `--strict` is forwarded to `harness_audit`, and `--allow-no-pytest` / `--allow-no-claude` skip those steps loudly instead of failing:

1. `harness_audit`: `python3 plugins/cc10x/tools/harness_audit.py`
2. `doc_consistency_check`: `python3 plugins/cc10x/tools/doc_consistency_check.py`
3. `prompt_clause_assertions`: `python3 plugins/cc10x/tools/prompt_clause_assertions.py`
4. `workflow_replay_check`: `python3 plugins/cc10x/tools/workflow_replay_check.py`
5. `pytest`: `uv run --no-project --with pytest python -m pytest plugins/cc10x/scripts -q`
6. `suite_qa_phase_invariants`: `python3 plugins/cc10x/scripts/test_cc10x_qa_phase_invariants.py`
7. `suite_review_package`: `python3 plugins/cc10x/scripts/test_cc10x_review_package.py`
8. `suite_token_usage_report`: `python3 plugins/cc10x/scripts/test_cc10x_token_usage_report.py`
9. `plugin_validate`: `claude plugin validate plugins/cc10x`

Pytest limitation: plain `python3 -m pytest` fails with ModuleNotFoundError when pytest is not installed, so the runner tries it first and falls back to `uv run --no-project --with pytest`. Pytest meaningfully collects only `test_cc10x_guards.py`; the three script-style suites run on `__main__`, which is why they are separate steps.

Fast loop per task: `--only harness_audit --only prompt_clause_assertions --only workflow_replay_check --only pytest`.

`plugins/cc10x/tools/worldclass_benchmark.py` is never a gate and is never run as part of it.

Version-bump surfaces to update together on a release:
- `plugins/cc10x/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- README version references
- `CHANGELOG.md`
- registry status lines
