# Live Verification Strategy

Use this reference when the request calls for production-like confidence instead of mock-only confidence.

## Goal

Plan a live verification lane that exercises the real first-party system with seeded or resettable data, real API calls, and named scenarios that the verifier can re-run.

## What The Plan Must Name

Always include a `### Live Verification Strategy` section with:
- `Manifest`: path to the harness manifest JSON
- `Environment ownership`: what is first-party, what is external, and what is intentionally stubbed at the boundary
- `Setup`: install or boot commands
- `Reset/Seed`: commands that create a repeatable starting state
- `Health`: command that proves the system is ready before proof runs
- `Proof scenarios`: named Given/When/Then scenarios with exact commands
- `Stress scenarios`: required only when latency, concurrency, or queue depth matter
- `Cleanup`: command that returns the environment to a safe state

## Planning Rules

- Prefer ephemeral or resettable environments over shared long-lived state.
- Prefer first-party end-to-end proof over testing third-party vendors directly.
- Keep external dependencies explicit. If a third-party cannot be safely exercised live, test your boundary and record the limitation.
- Name real data prerequisites: accounts, tokens, fixture records, background workers, and feature flags.
- Make every scenario replayable. If the data cannot be reset, the scenario is not trustworthy enough.
- Keep stress and proof lanes separate. Proof answers "does the flow work?"; stress answers "does it still work under load?"

## Section Template

```md
### Live Verification Strategy
- Manifest: `plugins/cc10x/tests/live/manifests/<name>.json`
- Environment ownership: first-party API + database are live; payment gateway is boundary-checked only
- Setup: `docker compose up -d`
- Reset/Seed: `npm run db:reset && npm run db:seed:e2e`
- Health: `curl -sf http://127.0.0.1:3000/api/health`
- Proof scenarios:
  - `Golden path: signup creates account`
  - `Negative path: expired token is rejected`
  - `Recovery path: retry completes queued job`
- Stress scenarios:
  - `Signup burst stays within threshold`
- Cleanup: `docker compose down --remove-orphans`
```

## Runner Shape

The verifier uses the generic runner:

```bash
python3 plugins/cc10x/scripts/cc10x_live_harness_runner.py --manifest <path> --mode proof
python3 plugins/cc10x/scripts/cc10x_live_harness_runner.py --manifest <path> --mode stress
```

Build the plan around those commands so live proof remains deterministic enough to audit.
