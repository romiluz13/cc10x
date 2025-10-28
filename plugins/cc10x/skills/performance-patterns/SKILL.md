---
name: performance-patterns
description: Identifies performance bottlenecks, N+1 database queries, inefficient algorithms with O(n¬≤) complexity, memory leaks, unnecessary re-renders, and optimization opportunities. Use when analyzing code for performance improvements, reviewing slow endpoints or pages, optimizing database queries, debugging memory issues, or planning performance-critical features. Provides optimization techniques, caching strategies, algorithm complexity analysis, and profiling guidance. Loaded by performance-analyzer agent during REVIEW workflow or master orchestrator when performance analysis needed. Complements risk-analysis Stage 6 (Performance & Scalability) with specific optimization patterns and techniques.
license: MIT
---

# Performance Patterns

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: Performance Patterns
- **Purpose**: Identify performance bottlenecks and optimization opportunities
- **When**: Performance analysis, code review, optimization tasks
- **Core Rule**: Measure first, optimize second (no premature optimization)
- **Sections Available**: N+1 Queries, Big O Complexity, Memory Leaks, Caching, Quick Checks

---

### Stage 2: Quick Reference

#### Performance Quick Checks

```
Performance Checklist:
- [ ] Database: N+1 queries eliminated?
- [ ] Algorithms: O(n¬≤) loops avoided?
- [ ] Frontend: React memoization used?
- [ ] Memory: Intervals/listeners cleaned up?
- [ ] Bundle: Code splitting implemented?
- [ ] Caching: Expensive calculations memoized?
```

#### Critical Anti-Patterns

**N+1 Query Problem**:
```typescript
// ‚ùN+1: 1 + N queries
const orders = await db.query('SELECT * FROM orders');
for (const order of orders) {
  order.customer = await db.query('SELECT * FROM customers WHERE id = $1', [order.customer_id]);
}

// ‚úSingle JOIN query
const orders = await db.query(`
  SELECT orders.*, customers.*
  FROM orders
  LEFT JOIN customers ON orders.customer_id = customers.id
`);
```

**O(n¬≤) Nested Loops**:
```typescript
// ‚ùO(n¬≤) complexity
for (let i = 0; i < arr.length; i++) {
  for (let j = 0; j < arr.length; j++) {
    if (arr[i] === arr[j] && i !== j) duplicates.push(arr[i]);
  }
}

// ‚úO(n) with Set
const seen = new Set();
const duplicates = new Set();
for (const item of arr) {
  if (seen.has(item)) duplicates.add(item);
  seen.add(item);
}
```

**Unnecessary Re-renders** (React):
```typescript
// ‚ùNew function every render
function UserList({ users }) {
  const handleClick = (id) => console.log(id); // New function!
  return users.map(u => <User onClick={handleClick} />);
}

// ‚úMemoized callback
const UserList = memo(function UserList({ users }) {
  const handleClick = useCallback((id) => console.log(id), []);
  return users.map(u => <User onClick={handleClick} />);
});
```

#### Quick Detection Commands

```bash
# Find N+1 candidates
grep -rn "for.*of\|forEach" src/ -A 3 | grep -i "query\|find"

# Find O(n¬≤) nested loops
grep -rn "for.*for" src/ --include="*.ts"

# Find memory leak candidates
grep -rn "setInterval\|addEventListener" src/ --include="*.ts"

# Check bundle size
npm run build -- --stats
```

---

### Stage 3: Detailed Guide

## Performance Optimization Patterns

### 1. Database Query Optimization

#### N+1 Query Problem (Most Common!)

**Detection**:
```typescript
// Pattern: Query in loop
const items = await getAll();
for (const item of items) {
  const related = await getRelated(item.id); // N queries!
}
```

**Solutions**:

**A. Use JOIN**:
```typescript
const items = await db.query(`
  SELECT items.*, related.*
  FROM items
  LEFT JOIN related ON items.id = related.item_id
`);
```

**B. Use IN clause (batch fetch)**:
```typescript
const items = await getAll();
const itemIds = items.map(i => i.id);
const related = await db.query(`
  SELECT * FROM related WHERE item_id = ANY($1)
`, [itemIds]);

// Map related back to items
const relatedMap = new Map(related.map(r => [r.item_id, r]));
items.forEach(item => {
  item.related = relatedMap.get(item.id);
});
```

**C. Use ORM eager loading**:
```typescript
// Prisma
const items = await prisma.item.findMany({
  include: { related: true } // Single query with JOIN
});

// TypeORM
const items = await itemRepository.find({
  relations: ['related']
});
```

#### Missing Database Indexes

**Detection**:
```sql
-- Check query execution plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;
-- If you see "Seq Scan" ‚ÜMissing index!
```

**Solution**:
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

**Common indexes needed**:
```sql
-- Foreign keys
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_products_category_id ON products(category_id);

-- Frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Composite indexes
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
```

### 2. Algorithmic Complexity

#### Common Complexity Classes

```
O(1)      - Constant: Hash map lookup, array index
O(log n)  - Logarithmic: Binary search, balanced tree
O(n)      - Linear: Single loop, array.map
O(n log n)- Linearithmic: Merge sort, quick sort
O(n¬≤)     - Quadratic: Nested loops (AVOID!)
O(2‚Åø)     - Exponential: Recursive Fibonacci (AVOID!)
```

#### O(n¬≤) ‚ÜO(n) Optimizations

**Problem: Find duplicates**:
```typescript
// ‚ùO(n¬≤) - 10,000 items = 100M operations
function findDuplicates(arr) {
  const dups = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) dups.push(arr[i]);
    }
  }
  return dups;
}

// ‚úO(n) - 10,000 items = 10K operations
function findDuplicates(arr) {
  const seen = new Set();
  const dups = new Set();
  for (const item of arr) {
    if (seen.has(item)) dups.add(item);
    seen.add(item);
  }
  return Array.from(dups);
}
```

**Problem: Find intersection**:
```typescript
// ‚ùO(n √m) - nested indexOf
function intersection(arr1, arr2) {
  return arr1.filter(x => arr2.indexOf(x) !== -1);
}

// ‚úO(n + m) - Set lookup
function intersection(arr1, arr2) {
  const set2 = new Set(arr2);
  return arr1.filter(x => set2.has(x));
}
```

### 3. Frontend Performance (React)

#### Prevent Unnecessary Re-renders

**Use React.memo**:
```typescript
// ‚ùRe-renders when parent re-renders
function UserCard({ user }) {
  return <div>{user.name}</div>;
}

// ‚úOnly re-renders when user changes
const UserCard = memo(function UserCard({ user }) {
  return <div>{user.name}</div>;
});
```

**Use useMemo for expensive calculations**:
```typescript
// ‚ùRecalculates on every render
function Cart({ items }) {
  const total = items.reduce((sum, item) => sum + item.price * item.qty, 0);
  return <div>Total: ${total}</div>;
}

// ‚úOnly recalculates when items change
function Cart({ items }) {
  const total = useMemo(
    () => items.reduce((sum, item) => sum + item.price * item.qty, 0),
    [items]
  );
  return <div>Total: ${total}</div>;
}
```

**Use useCallback for event handlers**:
```typescript
// ‚ùNew function every render ‚Üchild re-renders
function Parent() {
  const [count, setCount] = useState(0);
  const handleClick = () => setCount(c => c + 1);
  return <Child onClick={handleClick} />;
}

// ‚úStable function reference
function Parent() {
  const [count, setCount] = useState(0);
  const handleClick = useCallback(() => setCount(c => c + 1), []);
  return <Child onClick={handleClick} />;
}
```

#### Virtualize Long Lists

```typescript
// ‚ùRenders 10,000 DOM nodes
function CommentList({ comments }) {
  return (
    <div>
      {comments.map(c => <Comment key={c.id} comment={c} />)}
    </div>
  );
}

// ‚úOnly renders visible items (~20 DOM nodes)
import { FixedSizeList } from 'react-window';

function CommentList({ comments }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={comments.length}
      itemSize={100}
    >
      {({ index, style }) => (
        <Comment
          key={comments[index].id}
          comment={comments[index]}
          style={style}
        />
      )}
    </FixedSizeList>
  );
}
```

### 4. Memory Leak Prevention

#### Clear Intervals/Timeouts

```typescript
// ‚ùMemory leak - interval never cleared
function startPolling() {
  setInterval(() => fetchData(), 1000);
}

// ‚úCleanup in useEffect
function usePolling() {
  useEffect(() => {
    const interval = setInterval(() => fetchData(), 1000);
    return () => clearInterval(interval);
  }, []);
}
```

#### Remove Event Listeners

```typescript
// ‚ùMemory leak - listener not removed
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);

// ‚úCleanup listener
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

### 5. Bundle Size Optimization

#### Code Splitting

```typescript
// ‚ùEverything in one bundle
import Dashboard from './Dashboard';
import Settings from './Settings';
import Reports from './Reports';

// ‚úLazy load routes
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));
const Reports = lazy(() => import('./Reports'));

<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/settings" element={<Settings />} />
    <Route path="/reports" element={<Reports />} />
  </Routes>
</Suspense>
```

#### Tree Shaking

```typescript
// ‚ùImports entire library
import _ from 'lodash';
import moment from 'moment';

// ‚úImport only what's needed
import debounce from 'lodash/debounce';
import { format } from 'date-fns'; // Much smaller than moment
```

### 6. Caching Strategies

#### HTTP Caching

```typescript
// ‚ùNo caching
app.get('/api/products', (req, res) => {
  const products = getProducts();
  res.json(products);
});

// ‚úCache for 1 hour
app.get('/api/products', (req, res) => {
  const products = getProducts();
  res.set('Cache-Control', 'public, max-age=3600');
  res.json(products);
});
```

#### Memoization

```typescript
// ‚ùExpensive calculation repeated
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2); // O(2‚Åø)!
}

// ‚úMemoized
const fibCache = new Map();
function fibonacci(n) {
  if (n <= 1) return n;
  if (fibCache.has(n)) return fibCache.get(n);
  const result = fibonacci(n - 1) + fibonacci(n - 2);
  fibCache.set(n, result);
  return result; // O(n)
}
```

## Performance Measurement

### Profiling Commands

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log

# React profiling
# Use React DevTools Profiler tab

# Database query timing
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;

# Bundle analysis
npx webpack-bundle-analyzer dist/stats.json

# Lighthouse audit
npx lighthouse https://example.com --view
```

### Performance Metrics

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| Time to Interactive | < 3.8s | 3.8s - 7.3s | > 7.3s |
| First Contentful Paint | < 1.8s | 1.8s - 3.0s | > 3.0s |
| Largest Contentful Paint | < 2.5s | 2.5s - 4.0s | > 4.0s |
| Total Bundle Size | < 200 KB | 200 KB - 500 KB | > 500 KB |
| API Response Time | < 200ms | 200ms - 1s | > 1s |
| Database Query Time | < 50ms | 50ms - 200ms | > 200ms |

## References

- [Web Vitals](https://web.dev/vitals/)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)
- [Database Performance Explained](https://use-the-index-luke.com/)
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)

---

**Remember**: "Premature optimization is the root of all evil" - Profile first, optimize second!
