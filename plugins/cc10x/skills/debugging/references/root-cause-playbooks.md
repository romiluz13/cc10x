# Root-Cause Playbooks

## Table of Contents
- [How To Use This Reference](#how-to-use-this-reference)
- [Build And Type Failures](#build-and-type-failures)
- [Test Failures](#test-failures)
- [Runtime Failures](#runtime-failures)
- [Browser And Console Failures](#browser-and-console-failures)
- [Intermittent And Async Failures](#intermittent-and-async-failures)
- ["It Worked Before"](#it-worked-before)
- [Multi-Component Boundary Tracing](#multi-component-boundary-tracing)
- [Nearby Duplicate Scan](#nearby-duplicate-scan)

## How To Use This Reference

Read only the section that matches the failure shape in front of you. Keep the main
`SKILL.md` as the control plane: Phase 1 root-cause work first, then pattern
analysis, then hypothesis testing, then implementation.

## Build And Type Failures

Start with deterministic commands:

```bash
npx tsc --noEmit --pretty
npm run build
npx eslint . --ext .ts,.tsx
```

Use this order:
1. Read the first real error, not the whole scrollback.
2. Jump to the failing symbol with LSP.
3. Compare against a nearby working pattern in the same codebase.
4. Fix the smallest type, import, or config mismatch first.

Common root-cause buckets:
- missing type annotation or wrong generic
- null/undefined path not guarded
- import path or export shape drift
- alias/config mismatch between tooling layers
- JSX structure broken earlier than the reported line

## Test Failures

Use this order:
1. Read the exact assertion failure and stack trace.
2. Check whether the test setup is lying.
3. Trace the unexpected value back to its source.
4. Decide whether the bug is in the test, fixture, or production code.

Quick prompts for yourself:
- "What observable behavior failed?"
- "What input created the bad value?"
- "What is the nearest passing test for the same area?"

## Runtime Failures

Use this order:
1. Capture the full stack trace and reproduction steps.
2. Inspect the thrown line.
3. Identify the first invalid value.
4. Trace backward through callers until you find the original trigger.
5. Fix at the source, not at the crash site.

If you are tempted to add a defensive null check immediately, stop and confirm
whether the value is actually allowed to be null there.

## Browser And Console Failures

For UI bugs, request or collect clean console evidence:
1. Clear the console.
2. Reproduce once.
3. Copy the grouped errors and warnings.

Then check:
- repeated errors pointing to the same render path
- hidden CORS or network failures
- hydration or state-order issues
- unexpected value shapes in props or API responses

If console evidence is thin, add temporary boundary logging at the event handler,
state update, and render boundary. Remove it after the root cause is confirmed.

## Intermittent And Async Failures

Look for:
- shared mutable state
- stale closures
- unordered async completion
- missing cleanup on unmount/dispose
- retries without idempotency

Stabilize the reproduction before fixing:
- run the failing test repeatedly
- narrow the time window
- log ordering, not just values
- capture which branch ran first

## "It Worked Before"

Use `git bisect` when a regression has a clear good state:

```bash
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit-or-tag>
git bisect run CI=true npm test -- --grep "failing behavior"
git bisect reset
```

After identifying the breaking commit, ask:
- what assumption changed?
- what contract drifted?
- what related call sites now need the same fix?

## Multi-Component Boundary Tracing

When a bug crosses components or services, instrument boundaries once to learn
where the truth changes:

```text
entry input -> transformed payload -> downstream response -> final state
```

At each boundary, capture:
- the incoming shape
- the outgoing shape
- the config/env values that affect branching
- the component or service name

Do not instrument everything. Add logs only at the handoff points where the
value could be corrupted, dropped, or reinterpreted.

## Nearby Duplicate Scan

After you find the root cause, scan for the same signature nearby before
declaring success:

```bash
rg -n "same_bad_pattern|same_api|same_assumption" src test
```

Check for:
- sibling handlers using the same broken assumption
- parallel code paths with the same missing guard
- duplicate data transforms that drifted together

Fixing one instance while leaving its duplicates behind is a partial diagnosis,
not a finished investigation.
