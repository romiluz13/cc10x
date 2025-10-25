---
name: code-review-patterns
description: Analyzes code quality using Martin Fowler refactoring catalog to detect code smells, identify refactoring opportunities, assess maintainability, and suggest improvements. Checks for long functions, duplicate code, high complexity, god objects, inappropriate intimacy, and other anti-patterns. Use when reviewing code for quality improvements, planning refactoring efforts, assessing technical debt, enforcing best practices, or conducting pre-PR quality checks. Provides specific refactoring techniques with before-after examples. Loaded by quality-reviewer agent during REVIEW workflow or master orchestrator when code quality analysis needed. Complements risk-analysis skill (which focuses on bugs/risks) by focusing on maintainability and clean code principles.
license: MIT
---

# Code Review Patterns

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)
- **Skill**: Code Review Patterns
- **Purpose**: Identify code smells and maintainability issues
- **When**: Code review, quality analysis, refactoring planning
- **Core Rule**: Code is read 10x more than written - optimize for readability
- **Sections Available**: Code Smells, Refactoring Opportunities, Clean Code Principles

---

### Stage 2: Quick Reference (triggered - ~500 tokens)

#### Code Quality Quick Checks

```
Quality Checklist:
- [ ] Functions < 50 lines?
- [ ] Cyclomatic complexity < 10?
- [ ] No duplicated code?
- [ ] Clear, descriptive names?
- [ ] Single Responsibility Principle followed?
- [ ] Test coverage adequate?
```

#### Common Code Smells

**Long Method** (>50 lines):
```typescript
// ❌ 120-line method
function processOrder(order, user, settings) {
  // Validation (20 lines)
  // Business logic (60 lines)
  // Database updates (30 lines)
  // Email sending (10 lines)
}

// ✅ Extracted methods
function processOrder(order, user, settings) {
  validateOrder(order, user);
  const processed = applyBusinessRules(order, settings);
  saveOrder(processed);
  sendConfirmationEmail(user, processed);
  return processed;
}
```

**Duplicated Code**:
```typescript
// ❌ Repeated validation
function createUser(data) {
  if (!data.email) throw new Error('Email required');
  if (!data.name) throw new Error('Name required');
  // ... create
}
function updateUser(id, data) {
  if (!data.email) throw new Error('Email required');
  if (!data.name) throw new Error('Name required');
  // ... update
}

// ✅ Extracted validation
function validateUserData(data) {
  if (!data.email) throw new Error('Email required');
  if (!data.name) throw new Error('Name required');
}
```

**Poor Naming**:
```typescript
// ❌ Unclear names
function getData(d) {
  const arr = [];
  for (let i = 0; i < d.length; i++) {
    if (d[i].s === 1) arr.push(d[i]);
  }
  return arr;
}

// ✅ Clear names
function getActiveUsers(users) {
  return users.filter(user => user.status === UserStatus.Active);
}
```

**God Class** (too many responsibilities):
```typescript
// ❌ Does everything
class UserManager {
  create() {}
  update() {}
  delete() {}
  validateEmail() {}
  hashPassword() {}
  sendEmail() {}
  generateReport() {}
  exportCSV() {}
}

// ✅ Single Responsibility
class UserRepository { create() {} update() {} delete() {} }
class UserValidator { validateEmail() {} }
class PasswordService { hash() {} }
class EmailService { send() {} }
```

---

### Stage 3: Detailed Guide (on-demand - ~2500 tokens)

## Code Smells Catalog

### Bloaters

#### Long Method
**Symptom**: Method > 50 lines
**Impact**: Hard to understand, test, and maintain
**Refactoring**: Extract Method

```typescript
// Before: 80-line method
function calculatePrice(product, user, coupon) {
  // Tax calculation (15 lines)
  // Discount application (20 lines)
  // Shipping calculation (25 lines)
  // Final price calculation (20 lines)
}

// After: Extracted methods
function calculatePrice(product, user, coupon) {
  const basePrice = product.price;
  const tax = calculateTax(basePrice, user.location);
  const discount = applyDiscount(basePrice, coupon, user);
  const shipping = calculateShipping(product, user.address);
  return basePrice + tax - discount + shipping;
}
```

#### Large Class
**Symptom**: Class > 300 lines or > 10 methods
**Impact**: Violates Single Responsibility Principle
**Refactoring**: Extract Class

```typescript
// Before: 500-line god class
class OrderProcessor {
  // Order management (100 lines)
  // Payment processing (150 lines)
  // Inventory updates (100 lines)
  // Email notifications (100 lines)
  // Report generation (50 lines)
}

// After: Split responsibilities
class OrderManager { /* Order CRUD */ }
class PaymentProcessor { /* Payment logic */ }
class InventoryService { /* Stock management */ }
class NotificationService { /* Emails */ }
class ReportGenerator { /* Reports */ }
```

#### Long Parameter List
**Symptom**: > 4 parameters
**Impact**: Hard to remember order, difficult to call
**Refactoring**: Introduce Parameter Object

```typescript
// Before: Too many parameters
function createOrder(
  userId, productId, quantity, address,
  paymentMethod, couponCode, giftWrap, notes
) {}

// After: Parameter object
interface CreateOrderParams {
  userId: string;
  productId: string;
  quantity: number;
  address: Address;
  payment: PaymentInfo;
  options?: OrderOptions;
}

function createOrder(params: CreateOrderParams) {}
```

### Object-Orientation Abusers

#### Switch Statements
**Symptom**: Long switch/if-else chains
**Impact**: Violates Open/Closed Principle
**Refactoring**: Replace with Polymorphism

```typescript
// Before: Switch statement
function calculateShipping(type, weight) {
  switch (type) {
    case 'standard':
      return weight * 0.5;
    case 'express':
      return weight * 1.5;
    case 'overnight':
      return weight * 3.0;
  }
}

// After: Polymorphism
interface ShippingMethod {
  calculate(weight: number): number;
}

class StandardShipping implements ShippingMethod {
  calculate(weight: number) { return weight * 0.5; }
}
class ExpressShipping implements ShippingMethod {
  calculate(weight: number) { return weight * 1.5; }
}
```

### Change Preventers

#### Divergent Change
**Symptom**: One class changed for many different reasons
**Impact**: High coupling
**Refactoring**: Extract Class

```typescript
// Before: Changes for many reasons
class User {
  // Changed when: user data structure changes
  getName() {}
  getEmail() {}

  // Changed when: authentication logic changes
  login() {}
  logout() {}

  // Changed when: permission system changes
  hasPermission() {}
  grantPermission() {}
}

// After: Separated concerns
class User { getName() {} getEmail() {} }
class AuthService { login() {} logout() {} }
class PermissionService { check() {} grant() {} }
```

#### Shotgun Surgery
**Symptom**: One change requires changes in many classes
**Impact**: Easy to miss a spot
**Refactoring**: Move Method/Field, Inline Class

### Dispensables

#### Comments
**Symptom**: Excessive or explanatory comments
**Impact**: Code should be self-explanatory
**Refactoring**: Extract Method, Rename Variable

```typescript
// Before: Comments explain bad code
function calc(a, b, c) {
  // Calculate tax
  const t = a * 0.1;
  // Apply discount
  const d = b > 100 ? 0.2 : 0;
  // Return final price
  return a + t - (a * d);
}

// After: Self-documenting code
function calculateFinalPrice(basePrice, quantity, discount) {
  const tax = calculateTax(basePrice);
  const discountAmount = applyDiscount(basePrice, discount);
  return basePrice + tax - discountAmount;
}
```

#### Duplicate Code
**Symptom**: Same code in multiple places
**Impact**: Bug fixes must be applied everywhere
**Refactoring**: Extract Method/Class

### Couplers

#### Feature Envy
**Symptom**: Method uses another class more than its own
**Impact**: Poor cohesion
**Refactoring**: Move Method

```typescript
// Before: Feature Envy
class Order {
  calculateTotal() {
    // Uses customer class heavily
    const discount = this.customer.getDiscount();
    const tierMultiplier = this.customer.getTierMultiplier();
    const loyaltyPoints = this.customer.getLoyaltyPoints();
    // ... complex calculation using customer data
  }
}

// After: Moved to customer
class Customer {
  calculateOrderTotal(order: Order) {
    const discount = this.getDiscount();
    const tierMultiplier = this.getTierMultiplier();
    // ... calculation uses own data
  }
}
```

## Clean Code Principles

### Naming

**Functions**: Verbs (what they do)
```typescript
getUserById()    // ✅
validateEmail()  // ✅
user()           // ❌
```

**Variables**: Nouns (what they are)
```typescript
const userData = {...};      // ✅
const isActive = true;       // ✅
const get = {...};           // ❌
```

**Booleans**: is/has/can prefix
```typescript
isValid, hasPermission, canEdit  // ✅
valid, permission, edit          // ❌
```

### Functions

**Do One Thing**:
```typescript
// ❌ Does multiple things
function saveUserAndSendEmail(user) {
  db.save(user);
  email.send(user.email, 'Welcome!');
}

// ✅ Single responsibility
function saveUser(user) {
  db.save(user);
}
function sendWelcomeEmail(user) {
  email.send(user.email, 'Welcome!');
}
```

**Small Functions**: < 20 lines ideal, < 50 lines max

**Few Parameters**: 0-2 ideal, 3 acceptable, 4+ refactor

### Comments

```typescript
// ❌ Explaining bad code
// Loop through users
for (let i = 0; i < u.length; i++) {
  // Check if active
  if (u[i].s === 1) {
    // Add to array
    a.push(u[i]);
  }
}

// ✅ Code explains itself
const activeUsers = users.filter(user => user.isActive);
```

## Refactoring Checklist

Before refactoring:
- [ ] All tests passing
- [ ] Commit current working state
- [ ] Understand the code fully

During refactoring:
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Commit after each successful refactoring

After refactoring:
- [ ] All tests still passing
- [ ] Code more readable
- [ ] No behavior changes

## References

- [Refactoring: Improving the Design of Existing Code](https://refactoring.com/) - Martin Fowler
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) - Robert C. Martin
- [Code Smells](https://refactoring.guru/refactoring/smells) - Refactoring Guru

---

**Remember**: "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler
