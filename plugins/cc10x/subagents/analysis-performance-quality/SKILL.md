---
name: analysis-performance-quality
description: Parallel subagent for REVIEW workflow. Analyzes code for performance bottlenecks and quality issues. Loads performance-patterns and code-quality-patterns skills. Runs in parallel with other analysis subagents for 3x faster reviews.
---

# Analysis Performance & Quality Subagent

**Parallel analysis of performance bottlenecks and code quality issues.**

## When Used

Dispatched by REVIEW workflow when analyzing code for:
- Performance bottlenecks
- Code quality issues
- Complexity problems
- Code duplication
- SOLID principle violations

## Workflow

**Pattern**: Parallel execution (runs simultaneously with other subagents)  
**Skills Loaded**: performance-patterns, code-quality-patterns  
**Time**: ~2-3 minutes (parallel with others)  

---

## Phase 1: Load Skills

**Load in independent context:**

1. **performance-patterns**
   - Database query optimization
   - Caching strategies
   - Memory management
   - Network optimization
   - Bottleneck identification

2. **code-quality-patterns**
   - Complexity metrics
   - Code duplication
   - SOLID principles
   - Naming conventions
   - Technical debt

---

## Phase 2: Analyze Performance

**Check for performance bottlenecks:**

### Database Queries
- [ ] No N+1 queries
- [ ] Queries optimized
- [ ] Indexes used
- [ ] Joins efficient
- [ ] Pagination implemented

### Caching
- [ ] Caching used appropriately
- [ ] Cache invalidation correct
- [ ] Cache hit rates good
- [ ] No stale data
- [ ] TTL configured

### Memory Management
- [ ] No memory leaks
- [ ] Efficient data structures
- [ ] Garbage collection working
- [ ] Large objects handled
- [ ] Streaming used for large data

### Network Optimization
- [ ] Minimal API calls
- [ ] Batch requests used
- [ ] Compression enabled
- [ ] CDN used
- [ ] Connection pooling

---

## Phase 3: Analyze Code Quality

**Check for code quality issues:**

### Complexity
- [ ] Cyclomatic complexity < 10
- [ ] Functions < 50 lines
- [ ] Nesting depth < 4
- [ ] No god objects
- [ ] Clear responsibilities

### Duplication
- [ ] No code duplication
- [ ] DRY principle followed
- [ ] Shared utilities used
- [ ] No copy-paste code
- [ ] Reusable components

### SOLID Principles
- [ ] Single responsibility
- [ ] Open/closed principle
- [ ] Liskov substitution
- [ ] Interface segregation
- [ ] Dependency inversion

### Naming
- [ ] Clear variable names
- [ ] Clear function names
- [ ] Clear class names
- [ ] Consistent conventions
- [ ] No abbreviations

---

## Phase 4: Compile Findings

**Organize performance and quality findings:**

### Critical Issues ð´
- Performance disasters
- Critical complexity
- Major duplication
- SOLID violations

### Important Issues ð¡
- Performance concerns
- Code quality problems
- Maintainability issues
- Technical debt

### Nice to Have ð¢
- Performance optimizations
- Code improvements
- Refactoring suggestions

---

## Phase 5: Return Results

**Provide performance and quality analysis:**

```markdown
## Performance Analysis

### Bottlenecks
- [Bottleneck 1]: [Description]
  - Location: [File:Line]
  - Impact: [Impact]
  - Fix: [Suggestion]

### Optimization Opportunities
- [Opportunity 1]: [Description]
  - Potential gain: [Gain]
  - Effort: [Effort]

## Code Quality Analysis

### Complexity Issues
- [Issue 1]: [Description]
  - Location: [File:Line]
  - Complexity: [Metric]
  - Fix: [Suggestion]

### Duplication
- [Duplication 1]: [Description]
  - Locations: [Files]
  - Fix: [Suggestion]

### Quality Metrics
- Cyclomatic complexity: X
- Code duplication: X%
- SOLID compliance: X%
```

---

## Integration

**Runs in parallel with:**
- analysis-risk-security
- analysis-ux-accessibility

**Merged by**: review-workflow

**Result**: 3x faster code review (2-3 min vs 7 min)

