# Live Production-Like Testing

Use this reference when the accepted plan requires real, seeded, production-like verification.

## Goal

Produce proof from the real first-party system, not from mocks, narrative confidence, or replay fixtures alone.

## Required Command Shape

Run the harness with the manifest selected by the plan:

```bash
python3 plugins/cc10x/scripts/cc10x_live_harness_runner.py --manifest <path> --mode proof
python3 plugins/cc10x/scripts/cc10x_live_harness_runner.py --manifest <path> --mode stress
```

## Fail-Closed Rules

- If the plan requires live proof, do not substitute unit tests, replay fixtures, or manual checks as equivalent evidence.
- If setup, seed, or healthcheck cannot run because the environment is unavailable, report `BLOCKED` with the exact failing command and reason.
- If the harness runs and a named scenario fails, report `FAIL`.
- If stress is required but only proof ran, the task is incomplete.

## What Counts As Good Live Evidence

Each scenario should capture:
- `name`
- `given`
- `when`
- `then`
- `command`
- `expected`
- `actual`
- `exit_code`
- `status`

Map the runner output directly into the verifier's scenario table and evidence array.

## Coverage Guidance

Prefer a small number of meaningful scenarios over a large number of shallow checks:
- golden path
- critical negative path
- integration boundary or side-effect path
- retry or recovery path when queues/workers are involved
- stress profile when concurrency or throughput is material

## Environment Boundaries

- Test first-party behavior live whenever you control the environment.
- For third-party systems, prefer a real call only when it is safe, cheap, and resettable.
- Otherwise verify your integration boundary explicitly and record the limitation without pretending it is full end-to-end proof.
