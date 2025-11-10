# Performance Patterns - Pattern Library

Reference performance patterns. Use AFTER understanding functionality and performance requirements (see SKILL.md Phases 1-2).

## Performance Pattern Library

### Database Performance Patterns

**Understand performance requirements first, then check**:

**N+1 Query Problem** (only flag if causes timeouts or errors):

```typescript
// Check: Does N+1 cause timeouts?
// BAD - N+1 queries (flag if causes timeouts)
const orders = await db.query("SELECT * FROM orders");
for (const order of orders) {
  order.customer = await db.query("SELECT * FROM customers WHERE id = $1", [
    order.customer_id,
  ]);
}

// GOOD - Single JOIN query (fix if N+1 causes issues)
const orders = await db.query(`
  SELECT orders.*, customers.*
  FROM orders
  LEFT JOIN customers ON orders.customer_id = customers.id
`);
```

**Missing Indexes** (only flag if queries are slow):

```typescript
// Check: Are queries slow due to missing indexes?
// BAD - Full table scan (flag if slow)
SELECT * FROM users WHERE email = 'user@example.com';
-- Missing index on email column

// GOOD - Indexed query (add index if queries are slow)
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
```

### Algorithm Performance Patterns

**Understand performance requirements first, then check**:

**O(n²) Nested Loops** (only flag if causes timeouts):

```typescript
// Check: Does O(n²) cause timeouts?
// BAD - O(n²) complexity (flag if causes timeouts on real data)
for (let i = 0; i < arr.length; i++) {
  for (let j = 0; j < arr.length; j++) {
    if (arr[i] === arr[j] && i !== j) duplicates.push(arr[i]);
  }
}

// GOOD - O(n) with Set (fix if O(n²) causes issues)
const seen = new Set();
const duplicates = new Set();
for (const item of arr) {
  if (seen.has(item)) duplicates.add(item);
  seen.add(item);
}
```

### Frontend Performance Patterns

**Understand performance requirements first, then check**:

**Unnecessary Re-renders** (only flag if causes UI lag):

```typescript
// Check: Do re-renders cause UI lag?
// BAD - New function every render (flag if causes lag)
function UserList({ users }) {
  const handleClick = (id) => console.log(id); // New function!
  return users.map(u => <User onClick={handleClick} />);
}

// GOOD - Memoized callback (fix if re-renders cause lag)
const UserList = memo(function UserList({ users }) {
  const handleClick = useCallback((id) => console.log(id), []);
  return users.map(u => <User onClick={handleClick} />);
});
```

**Large Bundle Size** (only flag if initial load is slow):

```typescript
// Check: Is initial load slow due to bundle size?
// BAD - All code loaded upfront (flag if initial load > 3s)
import { HeavyComponent } from "./heavy-component";

// GOOD - Code splitting (fix if initial load is slow)
const HeavyComponent = lazy(() => import("./heavy-component"));
```

### Memory Leak Patterns

**Understand performance requirements first, then check**:

**Missing Cleanup** (only flag if causes crashes):

```typescript
// Check: Do memory leaks cause crashes?
// BAD - Missing cleanup (flag if causes memory leaks)
useEffect(() => {
  const interval = setInterval(() => {
    // Do something
  }, 1000);
  // Missing cleanup!
}, []);

// GOOD - With cleanup (fix if memory leaks cause crashes)
useEffect(() => {
  const interval = setInterval(() => {
    // Do something
  }, 1000);
  return () => clearInterval(interval); // Cleanup
}, []);
```

### Caching Patterns

**Understand performance requirements first, then check**:

**Missing Caching** (only flag if causes repeated slow operations):

```typescript
// Check: Are repeated operations slow?
// BAD - No caching (flag if causes repeated slow operations)
async function getUser(id) {
  return await db.query("SELECT * FROM users WHERE id = $1", [id]);
}

// GOOD - With caching (fix if repeated operations are slow)
import { cache } from "../utils/cache";

async function getUser(id) {
  const cached = cache.get(`user:${id}`);
  if (cached) return cached;

  const user = await db.query("SELECT * FROM users WHERE id = $1", [id]);
  cache.set(`user:${id}`, user, 300); // 5 min TTL
  return user;
}
```

## Performance Detection Commands

**Only run if functionality is slow or performance requirements are not met**:

```bash
# Find N+1 query candidates (only if queries are slow)
grep -rn "for.*of\|forEach" src/ -A 3 | grep -i "query\|find\|await"

# Find O(n²) nested loops (only if algorithms are slow)
grep -rn "for.*for" src/ --include="*.ts"

# Find memory leak candidates (only if app crashes or memory grows)
grep -rn "setInterval\|addEventListener\|setTimeout" src/ --include="*.ts"

# Check bundle size (only if initial load is slow)
npm run build -- --stats 2>/dev/null || echo "Build command not available"

# Profile performance (only if performance issues detected)
node --prof script.js  # Node.js profiling
```

## Performance Quick Checks

### Performance Checklist

- [ ] Database: N+1 queries eliminated?
- [ ] Algorithms: O(n²) loops avoided?
- [ ] Frontend: React memoization used?
- [ ] Memory: Intervals/listeners cleaned up?
- [ ] Bundle: Code splitting implemented?
- [ ] Caching: Expensive calculations memoized?

### Critical Anti-Patterns

**N+1 Query Problem**:

```typescript
// N+1: 1 + N queries
const orders = await db.query("SELECT * FROM orders");
for (const order of orders) {
  order.customer = await db.query("SELECT * FROM customers WHERE id = $1", [
    order.customer_id,
  ]);
}

// Single JOIN query
const orders = await db.query(`
  SELECT orders.*, customers.*
  FROM orders
  LEFT JOIN customers ON orders.customer_id = customers.id
`);
```

**O(n²) Nested Loops**:

```typescript
// BAD - O(n²) complexity
for (let i = 0; i < arr.length; i++) {
  for (let j = 0; j < arr.length; j++) {
    if (arr[i] === arr[j] && i !== j) duplicates.push(arr[i]);
  }
}

// GOOD - O(n) with Set
const seen = new Set();
const duplicates = new Set();
for (const item of arr) {
  if (seen.has(item)) duplicates.add(item);
  seen.add(item);
}
```
