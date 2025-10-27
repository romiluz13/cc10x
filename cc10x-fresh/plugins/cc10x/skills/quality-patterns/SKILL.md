---
name: quality-patterns
description: Code quality patterns, SOLID principles, and maintainability best practices. Use when reviewing code quality or refactoring.
allowed-tools: Read, Grep
---

# Code Quality Patterns

Best practices for writing maintainable, high-quality code.

## SOLID Principles

### S - Single Responsibility
**One class/function = One reason to change**

✅ Good:
```typescript
class UserRepository {
  findById(id: string): Promise<User> { ... }
  save(user: User): Promise<void> { ... }
}

class UserValidator {
  validate(user: User): ValidationResult { ... }
}
```

❌ Bad:
```typescript
class UserManager {
  findById(id: string) { ... }
  save(user: User) { ... }
  validate(user: User) { ... }
  sendEmail(user: User) { ... }
  generateReport(user: User) { ... }
}
```

### O - Open/Closed
**Open for extension, closed for modification**

✅ Good:
```typescript
interface PaymentMethod {
  process(amount: number): Promise<void>;
}

class CreditCard implements PaymentMethod {
  process(amount: number) { ... }
}

class PayPal implements PaymentMethod {
  process(amount: number) { ... }
}
```

### L - Liskov Substitution
**Subtypes must be substitutable for base types**

✅ Good:
```typescript
class Rectangle {
  constructor(public width: number, public height: number) {}
  area(): number { return this.width * this.height; }
}

class Square {
  constructor(public side: number) {}
  area(): number { return this.side * this.side; }
}
```

### I - Interface Segregation
**Many specific interfaces > One general interface**

✅ Good:
```typescript
interface Readable {
  read(): string;
}

interface Writable {
  write(data: string): void;
}

class File implements Readable, Writable { ... }
class Console implements Writable { ... }
```

### D - Dependency Inversion
**Depend on abstractions, not concretions**

✅ Good:
```typescript
class UserService {
  constructor(private db: DatabaseInterface) {}
}
```

❌ Bad:
```typescript
class UserService {
  private db = new MySQLDatabase();
}
```

## DRY (Don't Repeat Yourself)

✅ Good:
```typescript
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Use everywhere
if (!validateEmail(user.email)) { ... }
```

❌ Bad:
```typescript
// Repeated 10 times across codebase
if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(user.email)) { ... }
```

## Complexity Management

### Keep Functions Small
**Target: < 50 lines, < 10 cyclomatic complexity**

✅ Good:
```typescript
function processOrder(order: Order): Result {
  if (!isValid(order)) return Result.error('Invalid');
  
  const payment = processPayment(order);
  if (payment.failed) return Result.error('Payment failed');
  
  updateInventory(order);
  sendConfirmation(order);
  
  return Result.success();
}
```

❌ Bad:
```typescript
function processOrder(order: Order): Result {
  // 200 lines of nested if/else
  // Cyclomatic complexity: 35
}
```

### Reduce Nesting
**Max 3-4 levels**

✅ Good:
```typescript
function process(data: Data): Result {
  if (!data) return Result.error('No data');
  if (!data.valid) return Result.error('Invalid');
  if (!data.ready) return Result.error('Not ready');
  
  return performProcess(data);
}
```

❌ Bad:
```typescript
function process(data: Data): Result {
  if (data) {
    if (data.valid) {
      if (data.ready) {
        if (data.approved) {
          // Deep nesting
        }
      }
    }
  }
}
```

## Naming Conventions

### Variables & Functions
```typescript
// ✅ Descriptive names
const activeUserCount = users.filter(u => u.isActive).length;
function calculateTotalPrice(items: Item[]): number { ... }

// ❌ Cryptic names
const auc = users.filter(u => u.isActive).length;
function calc(items: Item[]): number { ... }
```

### Boolean Names
```typescript
// ✅ is/has/can prefix
isActive, hasPermission, canDelete

// ❌ Ambiguous
active, permission, delete
```

### Constants
```typescript
// ✅ UPPER_SNAKE_CASE
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.example.com';

// ❌ Mixed case
const maxRetryAttempts = 3;
```

## Error Handling

### Proper Error Handling
```typescript
// ✅ Specific error types
class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

try {
  validateUser(user);
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn('Validation failed', { field: error.field });
    return res.status(400).json({ error: error.message });
  }
  throw error; // Re-throw unexpected errors
}
```

### Never Swallow Errors
```typescript
// ❌ Silent failure
try {
  riskyOperation();
} catch (error) {
  // Nothing - ERROR HIDDEN!
}

// ✅ Log or re-throw
try {
  riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error });
  throw error;
}
```

## Code Organization

### File Structure
```typescript
// ✅ Related code together
src/
  users/
    user.model.ts
    user.service.ts
    user.controller.ts
    user.types.ts
  orders/
    ...

// ❌ Scattered
src/
  models/
    user.model.ts
    order.model.ts
  services/
    user.service.ts
    order.service.ts
```

### Import Organization
```typescript
// ✅ Grouped imports
// 1. External dependencies
import express from 'express';
import { z } from 'zod';

// 2. Internal modules
import { UserService } from './services/user';
import { config } from './config';

// 3. Types
import type { User, Order } from './types';
```

## Documentation

### When to Comment
```typescript
// ✅ Complex logic explanation
// Binary search requires sorted array
// Time complexity: O(log n)
function binarySearch(arr: number[], target: number): number {
  ...
}

// ❌ Obvious comments
// This function adds two numbers
function add(a: number, b: number): number {
  return a + b; // Return sum
}
```

### JSDoc for Public APIs
```typescript
/**
 * Processes a payment transaction
 * @param amount - Amount in cents
 * @param method - Payment method (credit_card, paypal)
 * @returns Transaction ID or throws PaymentError
 * @throws {PaymentError} When payment processing fails
 */
export async function processPayment(
  amount: number,
  method: PaymentMethod
): Promise<string> {
  ...
}
```

## Quality Metrics

### Good Targets
- **Cyclomatic Complexity**: < 10 per function
- **Function Length**: < 50 lines
- **File Length**: < 500 lines
- **Test Coverage**: > 80%
- **Duplication**: < 5%
- **TypeScript**: 100% type coverage

### Quick Checks
```bash
# Find long functions (> 50 lines)
# Find high complexity
# Check test coverage
npm run test:coverage

# Find duplication
npx jscpd src/
```

## Refactoring Patterns

### Extract Method
```typescript
// Before
function renderUser(user: User) {
  // 20 lines of complex logic
}

// After
function renderUser(user: User) {
  const fullName = formatUserName(user);
  const avatar = getUserAvatar(user);
  return `${fullName} ${avatar}`;
}
```

### Replace Magic Numbers
```typescript
// ❌ Magic numbers
if (user.age > 18) { ... }
setTimeout(callback, 3600000);

// ✅ Named constants
const ADULT_AGE = 18;
const ONE_HOUR_MS = 60 * 60 * 1000;

if (user.age > ADULT_AGE) { ... }
setTimeout(callback, ONE_HOUR_MS);
```

## Anti-Patterns to Avoid

❌ **God Objects**: Classes that do everything
❌ **Shotgun Surgery**: One change requires many file edits
❌ **Tight Coupling**: Classes depend on implementation details
❌ **Premature Optimization**: Optimizing before measuring
❌ **Cargo Cult**: Copying patterns without understanding
