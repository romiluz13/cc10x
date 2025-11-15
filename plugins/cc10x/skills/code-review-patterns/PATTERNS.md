# Code Review Patterns Library

This document provides a comprehensive library of code review patterns covering security, quality, and performance.

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

## Pattern Usage

Reference these patterns when reviewing code:

1. **Security Review**: Check authentication, authorization, input validation, secrets management
2. **Quality Review**: Check SOLID principles, complexity, duplication, maintainability
3. **Performance Review**: Check queries, algorithms, memory, bottlenecks

## Pattern Composition

These patterns can be composed together:

- Security + Quality = Secure, maintainable code
- Quality + Performance = Efficient, maintainable code
- Security + Performance = Secure, efficient code

See `plugins/cc10x/skills/shared-patterns/PATTERN-COMPOSITION.md` for composition guidelines.
