# Code Review Patterns Library

This document provides a comprehensive library of code review patterns covering security, quality, performance, refactoring, code explanation, and code cleanup.

## Refactoring Patterns

### Refactoring Methodology

- **Measure complexity metrics before/after**: Use cyclomatic complexity, maintainability index, code duplication metrics
- **Use proven refactoring catalog techniques**: Extract Function, Replace Conditional, Replace Magic Number, etc.
- **Incremental, safe transformations**: Small, testable changes that preserve functionality
- **Preserve functionality**: Zero behavior changes while improving structure
- **Validate improvements**: Confirm quality gains through testing

### Code Simplification Patterns

- **Complexity reduction**: Reduce cyclomatic complexity, nesting depth, cognitive load
- **Readability improvement**: Clear naming, extract complex expressions, reduce indirection
- **Cognitive load minimization**: Break complex logic into smaller, understandable pieces
- **Eliminate duplication**: Remove redundancy through abstraction and reuse

### Technical Debt Reduction Patterns

- **Duplication elimination**: Extract common patterns, create shared utilities
- **Anti-pattern removal**: Replace anti-patterns with proven patterns
- **Code smell detection**: Identify long methods, large classes, feature envy, etc.
- **Legacy code modernization**: Update old patterns to modern best practices

### Refactoring Catalog Techniques

- Extract Function/Method
- Extract Variable
- Replace Conditional with Polymorphism
- Replace Magic Number with Named Constant
- Replace Nested Conditional with Guard Clauses
- Consolidate Duplicate Conditional Fragments
- Replace Method with Method Object
- Introduce Parameter Object
- Replace Array with Object
- Replace Type Code with Class/Subclass

### Quality Metrics Patterns

- **Cyclomatic complexity**: Measure decision points (target: <10 per function)
- **Maintainability index**: Measure code maintainability (target: >70)
- **Code duplication**: Measure duplicate code percentage (target: <5%)
- **Code coverage**: Measure test coverage (target: >80% for critical paths)

### Safe Transformation Patterns

- **Behavior preservation**: Ensure refactoring doesn't change functionality
- **Incremental changes**: Make small, testable changes
- **Comprehensive testing**: Run tests after each refactoring step
- **Version control**: Commit after each successful refactoring step

## Security Patterns

### Authentication Patterns

- JWT token validation
- Session management
- OAuth flows
- Multi-factor authentication

### Authorization Patterns

- Role-based access control (RBAC)
- Permission checks
- Resource-level authorization
- API endpoint protection

### Input Validation Patterns

- SQL injection prevention
- XSS prevention
- CSRF protection
- File upload validation

### Secrets Management Patterns

- Environment variables
- Secret rotation
- Key management
- Credential storage

### Security Threat Modeling Patterns

- **Systematic vulnerability scanning**: Analyze code for security weaknesses
- **Threat modeling methodology**: Identify potential attack vectors and security risks
- **OWASP compliance verification**: Check adherence to OWASP Top 10 and industry standards
- **Risk impact assessment**: Evaluate business impact and likelihood (business impact + likelihood)
- **Concrete remediation guidance**: Specify security fixes with implementation steps

### Security Behavioral Patterns

- **Zero-trust principles**: Verify all inputs, authenticate all requests
- **Security-first mindset**: Security built in from the ground up
- **Think like an attacker**: Identify attack vectors, exploit vulnerabilities
- **Defense-in-depth strategies**: Multiple layers of security controls

## Code Quality Patterns

### SOLID Principles

- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle

### Complexity Patterns

- Cyclomatic complexity reduction
- Function length limits
- Nesting depth limits
- Cognitive complexity

### Duplication Patterns

- DRY (Don't Repeat Yourself)
- Code reuse
- Pattern extraction
- Template methods

### Maintainability Patterns

- Clear naming conventions
- Documentation standards
- Code organization
- Module boundaries

## Performance Patterns

### Performance Measurement-First Patterns

- **Measure first, optimize second**: Never assume bottlenecks - measure performance metrics first
- **Profile before optimizing**: Use Chrome DevTools, Lighthouse, React Profiler, Bundle Analyzer
- **Focus on critical paths**: Optimize paths affecting user experience
- **Validate improvements**: Confirm optimizations with before/after metrics
- **Document performance impact**: Record optimization strategies and measurable results

### Measurement Tools Patterns

- **Frontend**: Chrome DevTools Performance tab, Lighthouse CI, React DevTools Profiler, Bundle Analyzer
- **Backend**: Node.js profiler, Database query analyzer, APM tools
- **Load testing**: Stress testing, capacity planning, performance regression detection

### Frontend Performance Patterns

- **Core Web Vitals**: LCP, FID, CLS optimization
- **Bundle optimization**: Tree-shaking, code splitting, dynamic imports
- **Asset delivery**: Image optimization, font optimization, CDN usage
- **React/Next.js**: Memoization, code splitting, image optimization, font optimization

### Backend Performance Patterns

- **API response times**: Optimize endpoint performance
- **Query optimization**: Indexes, batch queries, select limits, pagination
- **Caching strategies**: Response caching, query result caching, CDN caching
- **Database optimization**: Indexes, query optimization, connection pooling

### Resource Optimization Patterns

- **Memory usage**: Fix leaks, avoid unnecessary object creation, clear intervals/timeouts
- **CPU efficiency**: Optimize algorithms, reduce computational complexity
- **Network performance**: Reduce payload size, parallel requests, debounce/throttle

### Query Optimization Patterns

- N+1 query prevention
- Database indexing
- Query batching
- Connection pooling

### Algorithm Patterns

- O(n\*n) loop optimization
- Efficient data structures
- Caching strategies
- Lazy loading

### Memory Patterns

- Memory leak prevention
- Resource cleanup
- Garbage collection optimization
- Memory profiling

### Bottleneck Patterns

- Latency reduction
- Throughput optimization
- Scalability patterns
- Load balancing

### Critical Path Analysis Patterns

- **User journey bottlenecks**: Identify slow paths in user flows
- **Load time optimization**: Reduce initial load time, optimize above-the-fold content
- **Interaction responsiveness**: Optimize user interactions (clicks, scrolls, inputs)

## Code Explanation Patterns

### Complexity Assessment Patterns

- **Metrics analysis**: Measure cyclomatic complexity, maintainability index, code duplication
- **Concept identification**: Identify key concepts, patterns, algorithms used
- **Pattern recognition**: Recognize design patterns, architectural patterns, code patterns
- **Progressive explanation**: Start simple, add complexity gradually (simple → complex)

### Visual Explanation Patterns

- **Mermaid flowcharts**: Visualize control flow, data flow, process flow
- **Class diagrams**: Show relationships, inheritance, composition
- **Sequence diagrams**: Show interactions, message passing, timing
- **Architecture diagrams**: Show system structure, component boundaries

### Explanation Structure Patterns

- **Overview first**: High-level summary before details
- **Progressive disclosure**: Start simple, add complexity gradually
- **Pattern recognition**: Explain patterns used, why they're used
- **Common pitfalls**: Identify common mistakes, how to avoid them

### Code Understanding Patterns

- **Purpose explanation**: What does this code do? Why does it exist?
- **Flow explanation**: How does data flow through this code?
- **Decision explanation**: Why were these design decisions made?
- **Trade-off explanation**: What are the trade-offs of this approach?

## Code Cleanup Patterns

### Code Smell Detection Patterns

- **Long methods**: Methods >50 lines (extract sub-methods)
- **Large classes**: Classes >500 lines (extract sub-classes)
- **Feature envy**: Methods that use more data from other classes than their own
- **Data clumps**: Groups of data that always appear together (extract object)
- **Primitive obsession**: Overuse of primitives instead of objects
- **Long parameter lists**: >5 parameters (extract parameter object)
- **Duplicate code**: Same code in multiple places (extract function)

### Refactoring Technique Catalog

- **Extract Function**: Extract repeated code into function
- **Extract Variable**: Extract complex expression into variable
- **Replace Conditional with Polymorphism**: Replace switch/if with polymorphism
- **Replace Magic Number**: Replace magic numbers with named constants
- **Replace Nested Conditional with Guard Clauses**: Early returns for clarity
- **Consolidate Duplicate Conditional**: Extract common conditionals
- **Replace Method with Method Object**: Extract complex method into object
- **Introduce Parameter Object**: Group related parameters
- **Replace Array with Object**: Use objects for structured data
- **Replace Type Code with Class**: Replace type codes with classes

### Modern Pattern Application

- **Optional chaining**: Use `?.` instead of nested conditionals
- **Nullish coalescing**: Use `??` instead of `||` for null/undefined checks
- **Template literals**: Use template strings instead of concatenation
- **Destructuring**: Use destructuring for cleaner variable assignment
- **Arrow functions**: Use arrow functions for concise syntax
- **Async/await**: Use async/await instead of promise chains

### Dead Code Removal Patterns

- **Unused imports**: Remove unused imports
- **Unused variables**: Remove unused variables
- **Unused functions**: Remove unused functions
- **Commented code**: Remove commented-out code (use version control)
- **Unreachable code**: Remove unreachable code paths

### Error Handling Improvement Patterns

- **Specific error types**: Use specific error types instead of generic Error
- **Error context**: Include context in error messages
- **Error recovery**: Provide recovery paths where possible
- **Error logging**: Log errors with sufficient context
- **Error boundaries**: Use error boundaries for graceful degradation

## Pattern Usage

Reference these patterns when reviewing code:

1. **Security Review**: Check authentication, authorization, input validation, secrets management, threat modeling
2. **Quality Review**: Check SOLID principles, complexity, duplication, maintainability, refactoring opportunities
3. **Performance Review**: Measure first, then optimize queries, algorithms, memory, bottlenecks, critical paths
4. **Refactoring**: Measure complexity, apply refactoring techniques, validate improvements
5. **Code Explanation**: Assess complexity, create visual diagrams, explain progressively
6. **Code Cleanup**: Detect code smells, apply refactoring techniques, remove dead code, improve error handling

## Pattern Composition

These patterns can be composed together:

- Security + Quality = Secure, maintainable code
- Quality + Performance = Efficient, maintainable code
- Security + Performance = Secure, efficient code
- Refactoring + Quality = Improved code structure
- Performance + Measurement = Data-driven optimization
- Code Explanation + Refactoring = Better understanding before improvement
- Code Cleanup + Refactoring = Systematic code improvement

See `plugins/cc10x/skills/shared-patterns/PATTERN-COMPOSITION.md` for composition guidelines.
