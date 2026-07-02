# Integration And Live Proof

## Table of Contents
- [Choose The Right Verification Depth](#choose-the-right-verification-depth)
- [When Unit Tests Are Enough](#when-unit-tests-are-enough)
- [When To Escalate To Integration Tests](#when-to-escalate-to-integration-tests)
- [When To Escalate To E2E Or Live Harness Proof](#when-to-escalate-to-e2e-or-live-harness-proof)
- [Live-Proof Triggers](#live-proof-triggers)
- [Coordination With CC10X Live Verification](#coordination-with-cc10x-live-verification)

## Choose The Right Verification Depth

TDD starts with unit or focused behavior tests, but it does not end there when
the risk profile is higher.

Think in layers:
- unit tests prove local behavior
- integration tests prove boundary wiring
- E2E or live harness proof proves the system truth the user cares about

## When Unit Tests Are Enough

Unit or focused component tests are usually enough for:
- pure logic
- isolated validation
- presentational UI behavior
- small refactors with unchanged boundaries

## When To Escalate To Integration Tests

Escalate when the change crosses a real boundary:
- route to service
- service to database
- UI to API
- queue producer to consumer
- cache or background side effects

The test should exercise the real collaboration, not just the local branch.

## When To Escalate To E2E Or Live Harness Proof

Escalate beyond integration when the user or accepted plan needs confidence in:
- seeded workflows
- browser flows
- real API calls
- background job orchestration
- cross-service side effects
- load or stress behavior

At that point, unit tests are necessary but not sufficient.

## Live-Proof Triggers

Treat these as strong signals:
- "production-like"
- "real data"
- "real API calls"
- "connect all the dots"
- "seed the database"
- "stress test"

When these appear, do not claim the work is verified with unit tests alone.

## Coordination With CC10X Live Verification

If the plan requires live proof:
- read `plugins/cc10x/skills/planning-patterns/references/live-verification-strategy.md`
- read `plugins/cc10x/skills/verification-before-completion/references/live-production-testing.md`
- use the harness manifest and proof commands defined there

The TDD cycle still matters. Live proof is the outer confidence ring, not a
replacement for test-first discipline.
