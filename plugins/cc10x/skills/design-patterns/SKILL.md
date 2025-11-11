---
name: design-patterns
description: Comprehensive design patterns with functionality-first approach. Use PROACTIVELY when planning features. First understands functionality (user flow, admin flow, system flow, integration flow), then designs APIs/components/integrations to support that functionality. Focuses on design that enables functionality, not generic design patterns. Provides design checklists, best practices, and patterns for all three domains.
---

# Design Patterns - Functionality First

## Functionality First Mandate

**BEFORE designing APIs/components/integrations, understand functionality**:

1. **What functionality needs APIs/components/integrations?**
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?
   - What are the integration flows?

2. **THEN design** - Design APIs/components/integrations to support that functionality

3. **Use patterns** - Apply design patterns AFTER functionality is understood

---

## Quick Start

Design APIs/components/integrations by first understanding functionality, then applying design patterns.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Design API**: REST endpoint with versioning, error handling
3. **Design component**: Reusable UploadForm with composition
4. **Design integration**: S3 integration with retry strategy

**Result:** APIs/components/integrations designed to support functionality.

**Comprehensive patterns for API, Component, and Integration design.**

## Progressive Loading Stages

### Stage 1: Metadata

**Domains Covered:**

- **API Design**: RESTful principles, versioning, error handling, rate limiting
- **Component Design**: Composition, reusability, props design, state management
- **Integration Design**: Retry strategies, circuit breaker, error handling, reliability

**Core Rules:**

- APIs are contracts - breaking changes hurt users
- Components are building blocks - design for reuse
- Integrations fail - design for failure

---

### Stage 2: Quick Reference

## API Design Checklist

```
REST Principles:
- [ ] Use HTTP verbs correctly (GET, POST, PUT, DELETE, PATCH)
- [ ] Resources are nouns, not verbs (/users not /getUsers)
- [ ] Status codes are correct (200, 201, 400, 401, 403, 404, 500)
- [ ] Consistent naming (snake_case or camelCase, not mixed)
- [ ] Pagination implemented for list endpoints
- [ ] Filtering and sorting supported
- [ ] Rate limiting implemented
- [ ] API versioning strategy defined
- [ ] Error responses consistent
- [ ] Documentation complete
```

**RESTful Endpoints**:

```typescript
// GOOD: Resources with HTTP verbs
GET / api / users; // List all users
GET / api / users / 123; // Get user 123
POST / api / users; // Create new user
PUT / api / users / 123; // Update user 123
DELETE / api / users / 123; // Delete user 123
PATCH / api / users / 123; // Partial update
```

**Error Responses**:

```typescript
// CONSISTENT
{
  error: {
    code: 'USER_NOT_FOUND',
    message: 'User with ID 123 not found',
    status: 404,
    timestamp: '2024-01-15T10:30:00Z'
  }
}
```

---

## Component Design Checklist

```
Component Structure:
- [ ] Single responsibility (one reason to change)
- [ ] Props are well-defined and documented
- [ ] Props have default values where appropriate
- [ ] Props are validated (PropTypes or TypeScript)
- [ ] Component is reusable across contexts
- [ ] No hardcoded values or strings
- [ ] State is minimal and necessary
- [ ] Side effects are managed (useEffect)
- [ ] Composition over inheritance
- [ ] No prop drilling (use context if needed)
```

**Composition Over Inheritance**:

```typescript
// COMPOSITION (PREFER)
function Button({ children, variant = 'default', ...props }) {
  return <button className={`btn btn-${variant}`} {...props}>{children}</button>;
}

function PrimaryButton(props) {
  return <Button variant="primary" {...props} />;
}
```

**Props Design**:

```typescript
// GROUPED PROPS
<UserCard user={{
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  phone: '555-1234',
  address: '123 Main St'
}} />
```

---

## Integration Design Checklist

```
Integration Reliability:
- [ ] Retry logic implemented (exponential backoff)
- [ ] Circuit breaker pattern used
- [ ] Timeouts configured
- [ ] Error handling comprehensive
- [ ] Logging and monitoring in place
- [ ] Rate limiting respected
- [ ] Webhooks validated
- [ ] Data synchronization idempotent
- [ ] Fallback strategies defined
- [ ] Documentation complete
```

**Retry with Exponential Backoff**:

```typescript
// WITH RETRY
async function fetchWithRetry(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url);
      if (response.ok) return response.json();
      if (response.status >= 500) throw new Error("Server error");
      return response.json();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}
```

**Circuit Breaker Pattern**:

```typescript
// CIRCUIT BREAKER
class CircuitBreaker {
  constructor(fn, { threshold = 5, timeout = 60000 } = {}) {
    this.fn = fn;
    this.threshold = threshold;
    this.timeout = timeout;
    this.failures = 0;
    this.state = "CLOSED"; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }

  async call(...args) {
    if (this.state === "OPEN") {
      if (Date.now() < this.nextAttempt) {
        throw new Error("Circuit breaker is OPEN");
      }
      this.state = "HALF_OPEN";
    }

    try {
      const result = await this.fn(...args);
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = "CLOSED";
  }

  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = "OPEN";
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

---

### Stage 3: Detailed Guide

## API Design Best Practices

### RESTful Principles

**Resource-Oriented Design**:

- Use nouns for resources: `/users`, `/posts`, `/comments`
- Use HTTP verbs for actions: GET (read), POST (create), PUT (update), DELETE (delete)
- Use hierarchical URLs for relationships: `/users/123/posts`, `/posts/456/comments`

### Versioning Strategies

**URL Versioning** (explicit):

```
GET /api/v1/users
GET /api/v2/users
```

**Header Versioning** (implicit):

```
GET /api/users
Accept: application/vnd.myapi.v2+json
```

### Error Handling

**Consistent Error Format**:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "status": 400,
    "details": {
      "field": "email",
      "reason": "required"
    },
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## Component Design Best Practices

### Composition Patterns

**Render Props**:

```typescript
function DataFetcher({ url, children }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData);
  }, [url]);
  return children(data);
}

// Usage
<DataFetcher url="/api/users">
  {users => <UserList users={users} />}
</DataFetcher>
```

**Higher-Order Components**:

```typescript
function withDataFetching(Component, url) {
  return function DataFetchingComponent(props) {
    const [data, setData] = useState(null);
    useEffect(() => {
      fetch(url).then(r => r.json()).then(setData);
    }, []);
    return <Component data={data} {...props} />;
  };
}
```

### State Management

**Minimal State**:

- Only store data that changes
- Derive computed values instead of storing them
- Use context for shared state, not for everything

---

## Integration Design Best Practices

### Reliability Patterns

**Idempotency**:

- Design operations to be safe to retry
- Use idempotency keys for critical operations
- Ensure repeated calls produce same result

**Monitoring & Observability**:

- Log all integration calls (request, response, errors)
- Track success/failure rates
- Alert on circuit breaker state changes
- Monitor retry counts and backoff delays

---

## Troubleshooting

**Common Issues:**

1. **Design patterns applied without understanding functionality**
   - **Symptom**: Patterns applied but don't support functionality flows
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, then apply patterns
   - **Prevention**: Always understand functionality before applying patterns

2. **Generic patterns instead of functionality-focused**
   - **Symptom**: Patterns follow generic best practices but don't support functionality
   - **Cause**: Didn't map functionality flows to pattern needs
   - **Fix**: Map flows to patterns, apply patterns to support flows
   - **Prevention**: Always map functionality to pattern needs first

3. **Patterns not aligned with project conventions**
   - **Symptom**: Patterns don't match project's design patterns
   - **Cause**: Didn't understand project patterns
   - **Fix**: Understand project patterns, align design
   - **Prevention**: Always understand project patterns first

**If issues persist:**

- Verify functionality analysis was completed first
- Check that functionality flows were mapped to pattern needs
- Ensure patterns align with project conventions
- Review pattern libraries for detailed guidance

**Remember**: Good design prevents bugs, improves maintainability, and scales with your system.
