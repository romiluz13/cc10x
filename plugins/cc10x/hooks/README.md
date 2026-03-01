# cc10x Hooks

Optional deterministic quality gates. These complement cc10x's agent-based
review with shell-level enforcement. They run at commit time, independent
of any LLM.

## Install

```bash
cp plugins/cc10x/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## What it does

Blocks `git commit` if your test suite fails. No test runner configured?
Hook exits 0 (passes through). No surprises.
