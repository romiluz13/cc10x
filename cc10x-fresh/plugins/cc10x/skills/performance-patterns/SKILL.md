---
name: performance-patterns
description: Performance optimization patterns for algorithms, databases, memory, and frontend. Use when analyzing performance or optimizing slow code.
allowed-tools: Read, Grep, Bash
---

# Performance Optimization Patterns

Proven patterns for improving speed, memory usage, and scalability.

## Algorithm Optimization

### Choose Right Data Structure
```typescript
// ❌ O(n) lookup
const users = ['alice', 'bob', 'charlie'];
if (users.includes(username)) { ... } // O(n)

// ✅ O(1) lookup
const users = new Set(['alice', 'bob', 'charlie']);
if (users.has(username)) { ... } // O(1)
```

### Avoid Nested Loops
```typescript
// ❌ O(n²)
for (const user of users) {
  for (const order of orders) {
    if (order.userId === user.id) { ... }
  }
}

// ✅ O(n) with Map
const ordersByUser = new Map();
for (const order of orders) {
  if (!ordersByUser.has(order.userId)) {
    ordersByUser.set(order.userId, []);
  }
  ordersByUser.get(order.userId).push(order);
}

for (const user of users) {
  const userOrders = ordersByUser.get(user.id) || [];
}
```

## Database Optimization

### Solve N+1 Problem
```typescript
// ❌ N+1 queries
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findAll({ where: { userId: user.id } });
}

// ✅ 2 queries with eager loading
const users = await User.findAll({
  include: [Order]
});
```

### Add Indexes
```sql
-- ❌ Full table scan
SELECT * FROM users WHERE email = 'user@example.com';

-- ✅ Indexed lookup
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
```

### Pagination
```typescript
// ❌ Loading all records
const users = await User.findAll(); // 1M records!

// ✅ Pagination
const users = await User.findAll({
  limit: 20,
  offset: page * 20
});
```

### Select Only Needed Fields
```typescript
// ❌ Select everything
SELECT * FROM users;

// ✅ Select specific fields
SELECT id, name, email FROM users;
```

## Caching Strategies

### Memoization
```typescript
// ❌ Recompute every time
function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2); // Exponential!
}

// ✅ Memoized
const fibCache = new Map<number, number>();
function fibonacci(n: number): number {
  if (n <= 1) return n;
  if (fibCache.has(n)) return fibCache.get(n)!;
  
  const result = fibonacci(n - 1) + fibonacci(n - 2);
  fibCache.set(n, result);
  return result;
}
```

### HTTP Caching
```typescript
// ✅ Cache static assets
app.use('/static', express.static('public', {
  maxAge: '1y',
  immutable: true
}));

// ✅ ETag for dynamic content
app.get('/api/users', (req, res) => {
  const users = getUsers();
  const etag = generateEtag(users);
  
  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();
  }
  
  res.setHeader('ETag', etag);
  res.json(users);
});
```

### Redis Caching
```typescript
// ✅ Cache expensive queries
async function getUser(id: string): Promise<User> {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  
  const user = await db.users.findById(id);
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 3600);
  return user;
}
```

## Memory Optimization

### Avoid Memory Leaks
```typescript
// ❌ Memory leak - event listener not removed
class Component {
  mount() {
    window.addEventListener('resize', this.handleResize);
  }
}

// ✅ Cleanup
class Component {
  mount() {
    window.addEventListener('resize', this.handleResize);
  }
  
  unmount() {
    window.removeEventListener('resize', this.handleResize);
  }
}
```

### Stream Large Files
```typescript
// ❌ Load entire file in memory
const data = await fs.readFile('large-file.txt');
processData(data);

// ✅ Stream processing
const stream = fs.createReadStream('large-file.txt');
stream.on('data', chunk => processChunk(chunk));
```

## Frontend Performance

### Code Splitting
```typescript
// ❌ Bundle everything
import { HeavyComponent } from './heavy';

// ✅ Lazy load
const HeavyComponent = lazy(() => import('./heavy'));
```

### Virtual Scrolling
```typescript
// ❌ Render 10,000 items
{items.map(item => <Item key={item.id} {...item} />)}

// ✅ Virtual scrolling
<VirtualList
  items={items}
  renderItem={item => <Item {...item} />}
  height={600}
  itemHeight={50}
/>
```

### Debounce/Throttle
```typescript
// ❌ Call on every keystroke
<input onChange={e => searchAPI(e.target.value)} />

// ✅ Debounce
const debouncedSearch = debounce(searchAPI, 300);
<input onChange={e => debouncedSearch(e.target.value)} />
```

### Memoize React Components
```typescript
// ❌ Re-render on every parent change
function ExpensiveComponent({ data }) {
  // Heavy computation
}

// ✅ Memo
const ExpensiveComponent = memo(function({ data }) {
  // Heavy computation
}, (prev, next) => prev.data.id === next.data.id);
```

### Image Optimization
```html
<!-- ❌ Large image -->
<img src="photo-5mb.jpg" />

<!-- ✅ Optimized with responsive images -->
<picture>
  <source srcset="photo-small.webp" media="(max-width: 640px)" type="image/webp" />
  <source srcset="photo-medium.webp" media="(max-width: 1024px)" type="image/webp" />
  <img src="photo-large.webp" alt="Photo" loading="lazy" />
</picture>
```

## Network Optimization

### Batch Requests
```typescript
// ❌ Multiple requests
await fetch('/api/user/1');
await fetch('/api/user/2');
await fetch('/api/user/3');

// ✅ Batch request
await fetch('/api/users?ids=1,2,3');
```

### Request Deduplication
```typescript
// ✅ Deduplicate simultaneous requests
const pendingRequests = new Map();

async function fetchUser(id: string): Promise<User> {
  if (pendingRequests.has(id)) {
    return pendingRequests.get(id);
  }
  
  const promise = fetch(`/api/users/${id}`).then(r => r.json());
  pendingRequests.set(id, promise);
  
  try {
    return await promise;
  } finally {
    pendingRequests.delete(id);
  }
}
```

### Compression
```typescript
// ✅ Enable gzip/brotli
import compression from 'compression';
app.use(compression());
```

## Async Optimization

### Parallel vs Sequential
```typescript
// ❌ Sequential (slow)
const user = await fetchUser();
const orders = await fetchOrders();
const products = await fetchProducts();
// Total: 300ms + 200ms + 150ms = 650ms

// ✅ Parallel (fast)
const [user, orders, products] = await Promise.all([
  fetchUser(),
  fetchOrders(),
  fetchProducts()
]);
// Total: max(300ms, 200ms, 150ms) = 300ms
```

### Async Batching
```typescript
// ✅ Batch async operations
async function processItems(items: Item[]) {
  const BATCH_SIZE = 10;
  
  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);
    await Promise.all(batch.map(item => processItem(item)));
  }
}
```

## Performance Metrics

### Core Web Vitals
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

### Backend Metrics
- **Response Time**: < 200ms (API), < 1s (pages)
- **Throughput**: Requests per second
- **Error Rate**: < 1%
- **Database Query Time**: < 50ms

### Quick Profiling
```typescript
// Measure function execution time
console.time('operation');
expensiveOperation();
console.timeEnd('operation');

// Performance API
const start = performance.now();
await operation();
const duration = performance.now() - start;
console.log(`Operation took ${duration}ms`);
```

## Optimization Checklist

- [ ] Database queries indexed
- [ ] N+1 problems resolved
- [ ] Caching implemented
- [ ] Code splitting enabled
- [ ] Images optimized
- [ ] Lazy loading used
- [ ] Bundle size < 200KB (initial)
- [ ] No memory leaks
- [ ] Async operations parallelized
- [ ] Compression enabled

## When to Optimize

✅ **Optimize When:**
- Profiling shows real bottleneck
- Users report slow performance
- Metrics exceed targets

❌ **Don't Optimize:**
- Without measuring first
- Premature optimization
- At cost of readability (unless critical)
