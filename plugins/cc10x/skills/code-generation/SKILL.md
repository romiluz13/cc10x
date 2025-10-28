---
name: code-generation
description: Provides patterns, conventions, and best practices for writing clean maintainable production-ready code following SOLID principles, DRY methodology, and project-specific conventions. Use when implementing new functionality with high quality standards, writing production code, creating functions or classes, adding features to existing codebase, or generating implementations that follow established patterns. Ensures consistency with codebase conventions, proper error handling, comprehensive edge case coverage, and maintainable code structure. Loaded by implementer agent during code writing phases or when quality code generation needed. Complements test-driven-development skill (which focuses on testing discipline) by focusing on code quality and patterns.
license: MIT
---

# Code Generation

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: Code Generation
- **Purpose**: Clean code patterns, naming conventions, best practices
- **When**: All code implementation (features, fixes, refactors)
- **Core Principle**: Write code humans read first, machines execute second
- **Sections Available**: Quick Reference, Naming Guide, Error Handling, Organization, Anti-Patterns

---

### Stage 2: Quick Reference

#### Core Principles
1. **Clear over clever** - Self-explanatory code
2. **Simple over complex** - Solve simply first
3. **Single responsibility** - One function, one job
4. **Explicit errors** - Handle failures gracefully
5. **Follow patterns** - Consistency with existing code

#### Naming Quick Rules
```
Functions:    camelCase    getUserById, validateEmail
Variables:    camelCase    userData, isActive, totalCount
Booleans:     is/has/...   isValid, hasPermission
Classes:      PascalCase   UserService, PaymentProcessor
Interfaces:   PascalCase   UserData, ApiResponse
Constants:    UPPER_SNAKE  MAX_RETRY_COUNT, API_BASE_URL
```

#### Function Size
- **Target**: 5-15 lines
- **If longer**: Extract sub-functions
- **One thing**: Single responsibility only

#### Error Handling Pattern
```typescript
try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  logger.error('Operation failed', { context, error });
  throw new SpecificError('Descriptive message', { cause: error });
}
```

#### Code Quality Checklist
```
- [ ] Clear, descriptive names (no abbreviations)
- [ ] Single responsibility per function
- [ ] Proper error handling with context
- [ ] No code duplication
- [ ] Comments explain WHY, not WHAT
- [ ] Follows project patterns
```

#### Common Patterns

**Service Class**:
```typescript
export class FeatureService {
  constructor(private db: Database, private logger: Logger) {}

  async mainMethod(): Promise<Result> {
    // Implementation
  }
}
```

**Error Handling**:
```typescript
if (!resource) {
  throw new NotFoundError(`Resource not found: ${id}`);
}
```

**Validation**:
```typescript
if (!input.email || !isValidEmail(input.email)) {
  throw new ValidationError('Valid email required');
}
```

---

### Stage 3: Detailed Content

## Naming Conventions (Detailed)

### Functions and Variables

```typescript
// ✅ Good: Clear, describes purpose
function calculateMonthlyRevenue(transactions: Transaction[]): number {
  return transactions
    .filter(t => t.type === 'revenue')
    .reduce((sum, t) => sum + t.amount, 0);
}

const userEmailAddress = user.email;
const isAuthenticationValid = validateToken(token);
```

```typescript
// ❌ Bad: Unclear, abbreviated
function calcRev(txns: any[]): number {
  return txns.filter(t => t.t === 'r').reduce((s, t) => s + t.a, 0);
}

const usrEml = user.email;
const isValid = validate(token);
```

**Detailed Rules**:
- **Functions**: `verbNoun` (camelCase) - `getUserById`, `validateEmail`, `processPayment`
- **Variables**: `noun` or `adjectiveNoun` (camelCase) - `userData`, `isActive`, `totalCount`
- **Booleans**: `is/has/should` prefix - `isValid`, `hasPermission`, `shouldRetry`
- **Constants**: `UPPER_SNAKE_CASE` - `MAX_RETRY_COUNT`, `API_BASE_URL`

### Classes and Types

```typescript
// ✅ Good: PascalCase, descriptive
class UserAuthenticationService {
  private tokenValidator: TokenValidator;

  async authenticateUser(credentials: UserCredentials): Promise<AuthResult> {
    // Implementation
  }
}

interface PaymentProcessorConfig {
  apiKey: string;
  webhookUrl: string;
  retryAttempts: number;
}

type OrderStatus = 'pending' | 'processing' | 'completed' | 'failed';
```

**Rules**:
- **Classes**: PascalCase - `UserService`, `PaymentProcessor`, `DatabaseConnection`
- **Interfaces**: PascalCase - `UserData`, `ApiResponse`, `ConfigOptions`
- **Types**: PascalCase - `UserId`, `TransactionType`, `ErrorCode`

## Function Design (Detailed)

### Single Responsibility

```typescript
// ✅ Good: Each function does one thing
async function createUser(userData: CreateUserInput): Promise<User> {
  const validatedData = validateUserInput(userData);
  const hashedPassword = await hashPassword(validatedData.password);
  const user = await saveUserToDatabase({ ...validatedData, password: hashedPassword });
  await sendWelcomeEmail(user.email);
  return user;
}

function validateUserInput(input: CreateUserInput): ValidatedUserInput {
  if (!input.email || !isValidEmail(input.email)) {
    throw new ValidationError('Valid email required');
  }
  if (!input.password || input.password.length < 8) {
    throw new ValidationError('Password must be at least 8 characters');
  }
  return input as ValidatedUserInput;
}
```

```typescript
// ❌ Bad: Does too much, hard to test
async function createUser(email: string, password: string): Promise<User> {
  // Validation
  if (!email || !email.includes('@')) throw new Error('Invalid');
  if (!password || password.length < 8) throw new Error('Invalid');

  // Hashing
  const salt = crypto.randomBytes(16);
  const hash = crypto.pbkdf2Sync(password, salt, 1000, 64, 'sha512');

  // Database
  const user = await db.query('INSERT INTO users...');

  // Email
  await sendgrid.send({ to: email, subject: 'Welcome'... });

  return user;
}
```

### Keep Functions Small

**Target**: 5-15 lines per function

```typescript
// ✅ Good: Readable, testable
function processOrder(order: Order): ProcessedOrder {
  validateOrder(order);
  const items = calculateOrderItems(order);
  const totals = calculateOrderTotals(items);
  const taxes = calculateTaxes(totals, order.location);
  return { ...order, items, totals, taxes, status: 'processed' };
}

function validateOrder(order: Order): void {
  if (!order.items || order.items.length === 0) {
    throw new ValidationError('Order must contain items');
  }
  if (!order.customerId) {
    throw new ValidationError('Customer ID required');
  }
}
```

## Error Handling (Detailed)

### Custom Error Classes

```typescript
// ✅ Good: Specific error types, helpful messages
class OrderProcessingError extends Error {
  constructor(
    message: string,
    public orderId: string,
    public cause?: Error
  ) {
    super(message);
    this.name = 'OrderProcessingError';
  }
}

async function processPayment(order: Order): Promise<PaymentResult> {
  try {
    const payment = await paymentGateway.charge({
      amount: order.total,
      customerId: order.customerId
    });
    return { success: true, transactionId: payment.id };
  } catch (error) {
    logger.error('Payment processing failed', { orderId: order.id, error });
    throw new OrderProcessingError(
      `Failed to process payment for order ${order.id}`,
      order.id,
      error as Error
    );
  }
}
```

```typescript
// ❌ Bad: Generic errors, no context
async function processPayment(order: any) {
  try {
    const payment = await gateway.charge(order.total);
    return payment;
  } catch (e) {
    throw new Error('Payment failed');
  }
}
```

### Error Handling Patterns

**For operations that can fail**:
```typescript
try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  logger.error('Operation failed', { context, error });
  throw new SpecificError('Descriptive message', { cause: error });
}
```

**For validation**:
```typescript
if (!isValid(input)) {
  throw new ValidationError(`Invalid input: ${reason}`);
}
```

**For missing resources**:
```typescript
const user = await findUser(id);
if (!user) {
  throw new NotFoundError(`User not found: ${id}`);
}
```

## Code Organization

### File Structure

```
src/
├── features/
│   ├── auth/
│   │   ├── auth.service.ts      # Business logic
│   │   ├── auth.controller.ts   # HTTP handlers
│   │   ├── auth.types.ts        # Types/interfaces
│   │   └── auth.test.ts         # Tests
│   └── orders/
│       ├── orders.service.ts
│       ├── orders.controller.ts
│       ├── orders.types.ts
│       └── orders.test.ts
├── shared/
│   ├── utils/
│   ├── types/
│   └── errors/
└── config/
```

### Import Organization

```typescript
// ✅ Good: Grouped and ordered
// 1. External dependencies
import { Request, Response } from 'express';
import { z } from 'zod';

// 2. Internal modules (absolute imports)
import { DatabaseService } from '@/shared/database';
import { Logger } from '@/shared/logger';

// 3. Relative imports (same feature)
import { UserService } from './user.service';
import { CreateUserInput, User } from './user.types';

// 4. Types only
import type { AuthContext } from '@/features/auth';
```

### Export Patterns

```typescript
// ✅ Good: Explicit exports
export { UserService } from './user.service';
export { UserController } from './user.controller';
export type { User, CreateUserInput, UpdateUserInput } from './user.types';
```

```typescript
// ❌ Bad: Barrel exports (slow)
export * from './user.service';
export * from './user.controller';
```

## Follow Project Patterns

### Before Implementing

```bash
# 1. Find similar features
grep -r "similar_feature_name" src/

# 2. Read existing implementations
# Note: patterns, structure, naming

# 3. Follow the same approach
```

**Example**: Implementing authentication?
1. Search: `grep -r "auth" src/`
2. Find: `src/features/auth/`
3. Follow: Same structure, patterns, error handling

### Consistency Matters

**In a project using**:
- Services for business logic → Create `feature.service.ts`
- Controllers for HTTP → Create `feature.controller.ts`
- Zod for validation → Use Zod schemas
- Custom error classes → Create feature-specific errors

**Don't introduce new patterns without reason.**

## Documentation

### When to Comment

```typescript
// ✅ Good: Explains WHY (non-obvious reasoning)
// Using exponential backoff to avoid overwhelming the API
// after a rate limit error
const delay = Math.pow(2, attempt) * 1000;

// Stripe requires idempotency keys for retry safety
// https://stripe.com/docs/api/idempotent_requests
const idempotencyKey = generateIdempotencyKey(order.id);
```

```typescript
// ❌ Bad: Explains WHAT (code already shows)
// Set delay to 2 to the power of attempt times 1000
const delay = Math.pow(2, attempt) * 1000;

// Generate idempotency key
const idempotencyKey = generateIdempotencyKey(order.id);
```

### Function Documentation

**Only document public APIs**:

```typescript
/**
 * Processes a refund for a completed order
 *
 * @param orderId - The ID of the order to refund
 * @param amount - Refund amount (must be <= order total)
 * @param reason - Reason for refund (for audit trail)
 * @returns Refund transaction details
 * @throws {NotFoundError} If order doesn't exist
 * @throws {ValidationError} If amount exceeds order total
 * @throws {RefundError} If payment gateway rejects refund
 */
async function processRefund(
  orderId: string,
  amount: number,
  reason: string
): Promise<RefundResult> {
  // Implementation
}
```

**Don't document private/internal functions** - code should be self-explanatory.

## Performance Considerations

### Avoid Premature Optimization

```typescript
// ✅ Good: Clear, correct, fast enough
function findUsersByRole(users: User[], role: string): User[] {
  return users.filter(user => user.role === role);
}
```

```typescript
// ❌ Bad: Over-optimized, hard to read
function findUsersByRole(users: User[], role: string): User[] {
  const result: User[] = [];
  const len = users.length;
  for (let i = 0; i < len; ++i) {
    if (users[i].role === role) result[result.length] = users[i];
  }
  return result;
}
```

**Optimize only if**:
- Profiling shows bottleneck
- User-facing performance issue
- Handling large data sets (10k+ items)

### When to Optimize

**Database queries**:
```typescript
// ✅ Good: Single query with join
const orders = await db.query(`
  SELECT o.*, u.email, u.name
  FROM orders o
  JOIN users u ON o.user_id = u.id
  WHERE o.status = 'pending'
`);
```

```typescript
// ❌ Bad: N+1 query problem
const orders = await db.query('SELECT * FROM orders WHERE status = ?', ['pending']);
for (const order of orders) {
  order.user = await db.query('SELECT * FROM users WHERE id = ?', [order.user_id]);
}
```

**Async operations**:
```typescript
// ✅ Good: Parallel independent operations
const [user, orders, preferences] = await Promise.all([
  fetchUser(id),
  fetchOrders(id),
  fetchPreferences(id)
]);
```

```typescript
// ❌ Bad: Sequential when could be parallel
const user = await fetchUser(id);
const orders = await fetchOrders(id);
const preferences = await fetchPreferences(id);
```

## Code Smells to Avoid

### No Magic Numbers

```typescript
// ✅ Good: Named constants
const MAX_LOGIN_ATTEMPTS = 3;
const SESSION_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes

if (loginAttempts >= MAX_LOGIN_ATTEMPTS) {
  lockAccount();
}
```

```typescript
// ❌ Bad: Unexplained numbers
if (loginAttempts >= 3) {
  lockAccount();
}
```

### No Code Duplication

```typescript
// ✅ Good: Extract shared logic
function validateEmail(email: string): void {
  if (!email || !isValidEmailFormat(email)) {
    throw new ValidationError('Valid email required');
  }
}

function createUser(data: CreateUserInput) {
  validateEmail(data.email);
  // ...
}

function updateUser(id: string, data: UpdateUserInput) {
  if (data.email) {
    validateEmail(data.email);
  }
  // ...
}
```

### No Deep Nesting

```typescript
// ✅ Good: Early returns, flat structure
function processOrder(order: Order): ProcessedOrder {
  if (!order.items || order.items.length === 0) {
    throw new ValidationError('Order must contain items');
  }

  if (!order.customerId) {
    throw new ValidationError('Customer ID required');
  }

  const items = calculateItems(order);
  const totals = calculateTotals(items);
  return { ...order, items, totals, status: 'processed' };
}
```

## Final Checklist

```
Production Ready:
- [ ] Names are clear and descriptive
- [ ] Functions are small and focused
- [ ] Errors handled with context
- [ ] No code duplication
- [ ] No magic numbers or strings
- [ ] Follows project patterns
- [ ] Edge cases covered
- [ ] Comments explain WHY, not WHAT
- [ ] No premature optimization
- [ ] Tests exist and pass (TDD)
```

## Remember

**Good code is**:
- ✅ Easy to read and understand
- ✅ Easy to modify and extend
- ✅ Easy to test
- ✅ Easy to debug

**Good code is NOT**:
- ❌ Clever or impressive
- ❌ Using every language feature
- ❌ Over-engineered for future needs
- ❌ Optimized before profiling

**Write code for the next developer (probably you in 6 months).**
