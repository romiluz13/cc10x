---
name: performance-patterns
description: Identifies performance bottlenecks, N+1 database queries, inefficient algorithms with O(n) complexity, memory leaks, unnecessary re-renders, and optimization opportunities. Use when analyzing code for performance improvements, reviewing slow endpoints or pages, optimizing database queries, debugging memory issues, or planning performance-critical features. Provides optimization techniques, caching strategies, algorithm complexity analysis, and profiling guidance. Loaded by the analysis-performance-quality subagent during the REVIEW workflow or by the orchestrator when performance analysis is needed. Complements risk-analysis Stage 6 (Performance & Scalability) with specific optimization patterns and techniques.
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
- [ ] Algorithms: O(n) loops avoided?
- [ ] Frontend: React memoization used?
- [ ] Memory: Intervals/listeners cleaned up?
- [ ] Bundle: Code splitting implemented?
- [ ] Caching: Expensive calculations memoized?
```

#### Critical Anti-Patterns

**N+1 Query Problem**:
```typescript
// N+1: 1 + N queries
const orders = await db.query('SELECT * FROM orders');
for (const order of orders) {
  order.customer = await db.query('SELECT * FROM customers WHERE id = $1', [order.customer_id]);
}

// Single JOIN query
const orders = await db.query(`
  SELECT orders.*, customers.*
  FROM orders
  LEFT JOIN customers ON orders.customer_id = customers.id
`);
```

**O(n) Nested Loops**:
```typescript
// O(n) complexity
for (let i = 0; i < arr.length; i++) {
  for (let j = 0; j < arr.length; j++) {
    if (arr[i] === arr[j] && i !== j) duplicates.push(arr[i]);
  }
}

// O(n) with Set
const seen = new Set();
const duplicates = new Set();
for (const item of arr) {
  if (seen.has(item)) duplicates.add(item);
  seen.add(item);
}
```

**Unnecessary Re-renders** (React):
```typescript
// New function every render
function UserList({ users }) {
  const handleClick = (id) => console.log(id); // New function!
  return users.map(u => <User onClick={handleClick} />);
}

// Memoized callback
const UserList = memo(function UserList({ users }) {
  const handleClick = useCallback((id) => console.log(id), []);
  return users.map(u => <User onClick={handleClick} />);
});
```

#### Quick Detection Commands

```bash
# Find N+1 candidates
grep -rn "for.*of\|forEach" src/ -A 3 | grep -i "query\|find"

# Find O(n) nested loops
grep -rn "for.*for" src/ --include="*.ts"

# Find memory leak candidates
grep -rn "setInterval\|addEventListener" src/ --include="*.ts"

# Check bundle size
npm run build -- --stats
```

---

### Stage 3: Detailed Guide

For the full detailed guidance, see [reference/performance-detailed.md](reference/performance-detailed.md).

## References

- [Web Vitals](https://web.dev/vitals/)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)
- [Database Performance Explained](https://use-the-index-luke.com/)
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)

---

**Remember**: Premature optimization is the root of all evil - profile first, optimize second!
