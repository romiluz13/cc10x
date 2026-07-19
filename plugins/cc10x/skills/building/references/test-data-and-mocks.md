# Test Data And Mocks

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

## SDK-Style Interfaces for Mockability

When designing external integrations, prefer **specific SDK-style functions** over one generic fetcher:

```typescript
// BAD — generic fetcher: one mock returns many shapes, conditional logic in test setup
async function fetchFromApi(endpoint: string): Promise<any> { ... }

// GOOD — SDK-style: each function returns one specific shape, type-safe, easy to mock
async function getUser(id: string): Promise<User> { ... }
async function getOrg(id: string): Promise<Org> { ... }
async function listMembers(orgId: string): Promise<Member[]> { ... }
```

**Benefits:**

- Each mock returns one specific shape — no conditional logic in test setup
- Type safety per endpoint — the mock can't return the wrong shape
- Easy to see which external calls a test exercises — just look at which mocks are set up
- New endpoints add a new function, not a new branch in a generic handler

**Dependency injection pattern:** Pass external dependencies in rather than creating them internally.

```typescript
// BAD — can't mock without monkey-patching
function processOrder(order: Order) {
  const stripe = new StripeClient(config.secret);
  return stripe.charge(order.amount);
}

// GOOD — inject the dependency, mock at the boundary
function processOrder(order: Order, paymentClient: PaymentClient) {
  return paymentClient.charge(order.amount);
}
```
