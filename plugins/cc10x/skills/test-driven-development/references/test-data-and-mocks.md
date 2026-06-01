# Test Data And Mocks

## Table of Contents
- [Factory Pattern](#factory-pattern)
- [Mock Only Boundaries](#mock-only-boundaries)
- [Common Boundary Mocks](#common-boundary-mocks)
- [Environment And Time](#environment-and-time)
- [Mock Quality Gate](#mock-quality-gate)

## Factory Pattern

Prefer small factory helpers over repeated object literals:

```typescript
const getMockUser = (overrides?: Partial<User>): User => ({
  id: '123',
  name: 'John Doe',
  email: 'john@example.com',
  role: 'user',
  ...overrides,
});
```

This keeps each test focused on the field that matters.

## Mock Only Boundaries

Mock:
- network calls
- databases when isolation requires it
- time
- third-party services

Do not mock:
- your own core business logic
- internal collaborators you control
- the very module under test

If you must mock everything to write the test, the design probably needs work.

## Common Boundary Mocks

Typical examples:
- `global.fetch`
- a database client wrapper
- cache or queue adapters
- auth provider SDKs

Keep mocks thin. The point is to isolate the boundary, not recreate the system.

## Environment And Time

When tests depend on environment or time:
- set env vars in setup and clean them up in teardown
- use fake timers deliberately
- restore global state after the test

Leaking env or timer state across tests creates false failures.

## Mock Quality Gate

Reconsider the design when:
- mock setup is longer than the test body
- the mock defines more behavior than the production code path
- the assertion proves the mock was called but not that behavior changed

The test should still teach you something real about the system.
