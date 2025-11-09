---
name: performance-patterns
description: Context-aware performance analysis that understands performance requirements before checking. Use PROACTIVELY when reviewing code that handles user interactions, database queries, or API calls. First understands functionality requirements and performance constraints, then checks for performance bottlenecks that affect functionality. Provides specific optimizations with benchmarks and expected impact. Focuses on performance issues that degrade user experience or break functionality, not premature optimization.
allowed-tools: Read, Grep, Glob, Bash
---

# Performance Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware performance analysis that understands performance requirements before checking. It focuses on performance issues that affect functionality, providing specific optimizations with benchmarks and expected impact.

**Unique Value**:

- Understands performance requirements before checking
- Focuses on performance issues affecting functionality
- Provides specific optimizations with benchmarks
- Understands project's performance characteristics

**When to Use**:

- After functionality is verified
- When reviewing code that handles user interactions, database queries, or API calls
- When performance issues might affect functionality

---

## Functionality First Mandate

**BEFORE applying performance checks, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (Performance constraints: latency, throughput, scale)
   - Dependencies: What does it need?
   - Edge Cases: What can go wrong? (Performance edge cases)
   - Verification: How do we know it works? (Performance tests, benchmarks)
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type):
   - UI Features → User Flow, Admin Flow, System Flow
   - Backend APIs → Request Flow, Response Flow, Error Flow, Data Flow
   - Utilities → Input Flow, Processing Flow, Output Flow, Error Flow
   - Integrations → Integration Flow, Data Flow, Error Flow, State Flow

3. **THEN understand performance requirements** - Before checking performance

4. **THEN check performance** - Only performance issues that affect functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any performance checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions (especially Constraints - performance requirements)
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this code supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc. - context-dependent)

3. **Understand Performance Requirements** (from Constraints):
   - Latency: How fast must it respond?
   - Throughput: How many requests per second?
   - Scale: How many users/concurrent operations?
   - Resource limits: Memory, CPU, network?

4. **Verify Functionality Works**:
   - Does functionality work? (tested)
   - Do flows work? (tested)
   - Does error handling work? (tested)

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely
- Must send file metadata to CRM API
- Must display upload progress to user

**Constraints** (Performance):

- Latency: Upload must complete within 30 seconds for files up to 10MB
- Throughput: Must handle 100 concurrent uploads
- Scale: Must support 1000 users uploading simultaneously
- Resource limits: 2GB memory, 4 CPU cores

**User Flow**:

1. User clicks "Upload File" button
2. User selects file from device
3. User sees upload progress indicator
4. User sees success message with file link

**System Flow**:

1. System receives file upload request
2. System validates file type and size
3. System stores file in secure storage
4. System sends file metadata to CRM API
5. System returns success response

**Functional Verification**:

- ✅ User can upload file (tested)
- ✅ File appears in CRM (tested)
- ✅ Error handling works (tested)

---

### Phase 2: Understand Performance Requirements (MANDATORY SECOND STEP)

**Before checking performance, understand performance requirements**:

1. **Extract Performance Requirements from Constraints**:
   - Latency: Response time requirements (e.g., < 3s for API calls, < 1s for UI interactions)
   - Throughput: Requests per second (e.g., 100 req/s)
   - Scale: Concurrent users/operations (e.g., 1000 concurrent users)
   - Resource limits: Memory, CPU, network (e.g., 2GB memory, 4 CPU cores)

2. **Map Performance-Critical Paths**:
   - Identify paths that affect user experience (user flows)
   - Identify paths that affect system performance (system flows)
   - Identify bottlenecks (database queries, API calls, file operations)

3. **Understand Project's Performance Characteristics**:

   ```bash
   # Find performance-critical code
   grep -r "query\|fetch\|await\|Promise" --include="*.ts" | head -20

   # Find database operations
   grep -r "db\.\|database\|mongoose\|prisma" --include="*.ts" | head -20

   # Find API calls
   grep -r "fetch\|axios\|request" --include="*.ts" | head -20
   ```

4. **Identify Performance Patterns Used**:
   - Caching strategies (Redis, Memcached, in-memory)
   - Database optimization (indexing, query optimization)
   - API optimization (batching, pagination)
   - Frontend optimization (code splitting, lazy loading)

**Document Performance Requirements**:

- Latency: Response time requirements
- Throughput: Requests per second
- Scale: Concurrent users/operations
- Resource limits: Memory, CPU, network
- Performance-critical paths: User flows, system flows, bottlenecks

**Example Output**:

```
Performance Requirements:
Latency:
- API calls: < 500ms (p95)
- UI interactions: < 100ms
- File uploads: < 30s for 10MB files

Throughput:
- API endpoints: 100 req/s
- File uploads: 10 concurrent uploads

Scale:
- Concurrent users: 1000
- Database connections: 100

Resource Limits:
- Memory: 2GB
- CPU: 4 cores
- Network: 100Mbps

Performance-Critical Paths:
- User flow: Upload button → File selection → Upload progress → Success
- System flow: File validation → Storage upload → CRM API sync → Response
- Bottlenecks: File storage (S3), CRM API calls
```

---

### Phase 3: Performance Analysis (Only Issues Affecting Functionality)

**After understanding functionality and performance requirements, check performance**:

1. **Map Performance Issues to Functionality**:
   - For each functionality flow, identify performance risks
   - Check if performance issues affect functionality
   - Prioritize: Critical (blocks functionality) > Important (degrades UX) > Minor (optimizations)

2. **Check Latency** (if affects user experience):
   - Are response times within requirements?
   - Are there slow queries or API calls?
   - Are there unnecessary operations?

3. **Check Throughput** (if affects scalability):
   - Can system handle required throughput?
   - Are there bottlenecks preventing scale?
   - Are resources used efficiently?

4. **Check Memory** (if affects stability):
   - Are there memory leaks?
   - Is memory usage within limits?
   - Are resources cleaned up properly?

5. **Check Database Performance** (if functionality uses database):
   - Are queries optimized?
   - Are there N+1 query problems?
   - Are indexes used correctly?

**Provide Specific Optimizations with Benchmarks**:

For each performance issue found, provide:

- **Issue**: Clear description of the performance issue
- **Impact**: How it affects functionality (latency, throughput, stability)
- **Location**: File path and line number
- **Current Performance**: Measured or estimated performance
- **Fix**: Specific optimization with expected performance improvement
- **Benchmark**: Expected improvement (e.g., "50% faster", "reduces latency from 2s to 500ms")
- **Priority**: Critical, Important, or Minor

**Example**:

````markdown
## Performance Finding: N+1 Query Problem

**Issue**: File list endpoint performs N+1 queries, loading user data for each file separately.

**Impact**: Blocks functionality - endpoint times out with >100 files, breaking file list feature.

**Location**: `src/api/files.ts:45`

**Current Performance**:

- 100 files = 101 queries (1 + 100)
- Response time: 2.5s (exceeds 500ms requirement)
- Timeout occurs with >150 files

**Current Code**:

```typescript
app.get("/api/files", authenticate, async (req, res) => {
  const files = await db.query("SELECT * FROM files WHERE userId = $1", [
    req.user.id,
  ]);
  for (const file of files) {
    file.user = await db.query("SELECT * FROM users WHERE id = $1", [
      file.userId,
    ]);
  }
  res.json(files);
});
```
````

**Fix** (with JOIN to eliminate N+1):

```typescript
app.get("/api/files", authenticate, async (req, res) => {
  const files = await db.query(
    `
    SELECT files.*, users.name as userName, users.email as userEmail
    FROM files
    LEFT JOIN users ON files.userId = users.id
    WHERE files.userId = $1
  `,
    [req.user.id],
  );
  res.json(files);
});
```

**Benchmark**:

- 100 files = 1 query (was 101)
- Response time: 200ms (was 2.5s)
- Improvement: 92% faster, eliminates timeout

**Priority**: Critical (blocks functionality)

````

---

## Performance Pattern Library (Reference - Use AFTER Understanding Performance Requirements)

### Database Performance Patterns

**Understand performance requirements first, then check**:

**N+1 Query Problem** (only flag if causes timeouts or errors):
```typescript
// Check: Does N+1 cause timeouts?
// BAD - N+1 queries (flag if causes timeouts)
const orders = await db.query('SELECT * FROM orders');
for (const order of orders) {
  order.customer = await db.query('SELECT * FROM customers WHERE id = $1', [order.customer_id]);
}

// GOOD - Single JOIN query (fix if N+1 causes issues)
const orders = await db.query(`
  SELECT orders.*, customers.*
  FROM orders
  LEFT JOIN customers ON orders.customer_id = customers.id
`);
````

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

---

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

---

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

---

## Priority Classification

**Critical (Must Fix - Blocks Functionality)**:

- Blocks functionality (timeouts, crashes, errors)
- Prevents feature from working (out of memory, query failures)
- Breaks user flows (page crashes, functionality unavailable)
- Examples:
  - N+1 queries causing timeouts
  - Memory leaks causing crashes
  - O(n²) algorithms timing out on real data

**Important (Should Fix - Degrades UX)**:

- Affects functionality negatively (slow loading, laggy interactions)
- Degrades user experience significantly (> 3s load times, > 1s interactions)
- Examples:
  - Slow queries degrading UX (> 500ms)
  - Unnecessary re-renders causing UI lag
  - Large bundles slowing initial load (> 3s)

**Minor (Can Defer - Optimizations)**:

- Doesn't affect functionality (premature optimization)
- Generic best practices (perfect caching, ideal bundle size)
- Examples:
  - Micro-optimizations (if functionality performs acceptably)
  - Perfect caching (if current performance meets requirements)
  - Ideal bundle size (if initial load is acceptable)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Performance Analysis Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Performance Requirements Summary

[Brief summary of performance requirements from Phase 2]

## Performance Findings

### Critical Issues (Blocks Functionality)

[For each critical issue:]

- **Issue**: [Description]
- **Impact**: [How it blocks functionality]
- **Location**: [File:line]
- **Current Performance**: [Measured/estimated performance]
- **Fix**: [Specific optimization]
- **Benchmark**: [Expected improvement]
- **Priority**: Critical

### Important Issues (Degrades UX)

[For each important issue:]

- **Issue**: [Description]
- **Impact**: [How it degrades UX]
- **Location**: [File:line]
- **Current Performance**: [Measured/estimated performance]
- **Fix**: [Specific optimization]
- **Benchmark**: [Expected improvement]
- **Priority**: Important

### Minor Issues (Optimizations)

[For each minor issue:]

- **Issue**: [Description]
- **Impact**: [Why it's minor]
- **Location**: [File:line]
- **Fix**: [Specific optimization - optional]
- **Priority**: Minor

## Recommendations

[Prioritized list of optimizations - Critical first, then Important, then Minor]
```

---

## Usage Guidelines

### For Review Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis - especially Constraints)
2. **Then**: Complete Phase 2 (Understand Performance Requirements)
3. **Then**: Complete Phase 3 (Performance Analysis - Only Issues Affecting Functionality)
4. **Focus**: Performance issues that block functionality or degrade UX significantly

### Key Principles

1. **Functionality First**: Always understand functionality before checking performance
2. **Requirements-Driven**: Understand performance requirements before checking
3. **Specific Optimizations**: Provide optimizations with benchmarks and expected impact
4. **Prioritize by Impact**: Critical (blocks functionality) > Important (degrades UX) > Minor (optimizations)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to performance checks
2. **Ignoring Performance Requirements**: Don't check everything - focus on requirements
3. **Premature Optimization**: Don't optimize if functionality performs acceptably
4. **Missing Benchmarks**: Don't just identify issues - provide expected performance improvements
5. **Wrong Priority**: Don't mark minor optimizations as critical - prioritize by functionality impact
6. **No Code Examples**: Don't just describe issues - show how to optimize with expected impact

---

_This skill enables context-aware performance analysis that understands performance requirements and focuses on performance issues affecting functionality, providing specific optimizations with benchmarks and expected impact._
