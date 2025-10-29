---
name: code-quality-patterns
description: Identifies maintainability, readability, complexity, duplication, and technical-debt issues. Used by the review, build, and debug workflows to provide actionable quality feedback.
---

# Code Quality Patterns

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: Code Quality Patterns
- **Purpose**: Identify code quality issues and ensure maintainability
- **When**: Code review, quality analysis, refactoring planning
- **Core Rule**: Code is read 10x more than written - optimize for readers
- **Sections Available**: Complexity Metrics, DRY Principles, SOLID Patterns, Quick Checks

---

### Stage 2: Quick Reference

#### Code Quality Checklist

```
Quality Metrics:
- [ ] Cyclomatic Complexity < 10 per function
- [ ] Function length < 50 lines
- [ ] Class length < 300 lines
- [ ] Nesting depth < 4 levels
- [ ] Code duplication < 5%
- [ ] Test coverage > 80%
- [ ] No console.log in production
- [ ] No TODO/FIXME comments
```

#### File Size Policy

Keep files readable and focused. Default guidance:

- Aim for files under 500 lines
- Soft caps by type:
  - Components: < 200 lines
  - Utilities: < 300 lines
  - Services: < 400 lines
  - Config: < 100 lines

When a file exceeds its cap, propose a concrete split plan (by responsibility):

```
example/large-file.ts (780 lines)
  → core.ts (business logic)
  → utils.ts (helpers)
  → types.ts (interfaces/types)
  → adapters.ts (I/O, boundaries)
```

Quick detection:
```bash
find src -type f -name "*.*" -maxdepth 4 -print0 \
  | xargs -0 wc -l 2>/dev/null \
  | sort -n | tail -20
```

Flag oversized files during review/build/debug and suggest a split before closing the task.

#### Critical Quality Patterns

**Function Complexity** (Cyclomatic Complexity):
```typescript
// HIGH COMPLEXITY (CC = 8)
function processUser(user) {
  if (user.age > 18) {
    if (user.verified) {
      if (user.active) {
        if (user.premium) {
          // ... 20 lines
        } else {
          // ... 15 lines
        }
      }
    }
  }
}

// LOW COMPLEXITY (CC = 1)
function processUser(user) {
  if (!isEligible(user)) return;
  handlePremiumUser(user);
}

function isEligible(user) {
  return user.age > 18 && user.verified && user.active;
}
```

**DRY Principle** (Don't Repeat Yourself):
```typescript
// DUPLICATION
function validateEmail(email) {
  if (!email.includes('@')) throw new Error('Invalid email');
  if (email.length < 5) throw new Error('Email too short');
}

function validatePhone(phone) {
  if (!phone.includes('-')) throw new Error('Invalid phone');
  if (phone.length < 10) throw new Error('Phone too short');
}

// REUSABLE
function validate(value, pattern, minLength, fieldName) {
  if (!pattern.test(value)) throw new Error(`Invalid ${fieldName}`);
  if (value.length < minLength) throw new Error(`${fieldName} too short`);
}

validate(email, /@/, 5, 'email');
validate(phone, /-/, 10, 'phone');
```

**Naming Conventions**:
```typescript
// BAD NAMES
const d = new Date();
const x = users.filter(u => u.age > 18);
function fn(a, b) { return a + b; }

// GOOD NAMES
const currentDate = new Date();
const adultUsers = users.filter(user => user.age > 18);
function calculateTotal(subtotal, tax) { return subtotal + tax; }
```

#### Red Flags 
```bash
# Find high complexity functions
grep -r "if.*if.*if" src/ --include="*.ts"

# Find long functions
wc -l src/**/*.ts | sort -n | tail -20

# Find duplication
jscpd src/

# Find console.log
grep -r "console\." src/ --include="*.ts"

# Find TODO/FIXME
grep -r "TODO\|FIXME" src/ --include="*.ts"
```

---

### Stage 3: Detailed Guide

## SOLID Principles

### S: Single Responsibility Principle

**What**: Each class/function should have ONE reason to change.

```typescript
// MULTIPLE RESPONSIBILITIES
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }

  save() {
    // Saving to database
    db.insert('users', this);
  }

  sendEmail() {
    // Sending email
    emailService.send(this.email, 'Welcome!');
  }

  generateReport() {
    // Generating report
    return `User: ${this.name}`;
  }
}

// SINGLE RESPONSIBILITY
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }
}

class UserRepository {
  save(user) {
    db.insert('users', user);
  }
}

class EmailService {
  sendWelcome(user) {
    this.send(user.email, 'Welcome!');
  }
}

class UserReporter {
  generate(user) {
    return `User: ${user.name}`;
  }
}
```

### O: Open/Closed Principle

**What**: Open for extension, closed for modification.

```typescript
// VIOLATES OCP
class PaymentProcessor {
  process(payment) {
    if (payment.type === 'credit') {
      // Process credit card
    } else if (payment.type === 'paypal') {
      // Process PayPal
    } else if (payment.type === 'stripe') {
      // Process Stripe
    }
  }
}

// FOLLOWS OCP
interface PaymentMethod {
  process(payment): Promise<void>;
}

class CreditCardProcessor implements PaymentMethod {
  process(payment) { /* ... */ }
}

class PayPalProcessor implements PaymentMethod {
  process(payment) { /* ... */ }
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}
  process(payment) {
    return this.method.process(payment);
  }
}
```

### L: Liskov Substitution Principle

**What**: Subtypes must be substitutable for their base types.

```typescript
// VIOLATES LSP
class Bird {
  fly() { return 'flying'; }
}

class Penguin extends Bird {
  fly() { throw new Error('Penguins cannot fly'); }
}

// FOLLOWS LSP
class Bird {
  move() { return 'moving'; }
}

class FlyingBird extends Bird {
  fly() { return 'flying'; }
}

class Penguin extends Bird {
  swim() { return 'swimming'; }
}
```

### I: Interface Segregation Principle

**What**: Clients should not depend on interfaces they don't use.

```typescript
// VIOLATES ISP
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { throw new Error('Robots do not eat'); }
  sleep() { throw new Error('Robots do not sleep'); }
}

// FOLLOWS ISP
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class Robot implements Workable {
  work() { /* ... */ }
}

class Human implements Workable, Eatable, Sleepable {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
}
```

### D: Dependency Inversion Principle

**What**: Depend on abstractions, not concretions.

```typescript
// VIOLATES DIP
class UserService {
  private db = new MongoDBClient();

  getUser(id) {
    return this.db.collection('users').findOne({ _id: id });
  }
}

// FOLLOWS DIP
interface Database {
  findOne(collection: string, query: any): Promise<any>;
}

class UserService {
  constructor(private db: Database) {}

  getUser(id) {
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}
```

## Code Quality Metrics

| Metric | Good | Warning | Bad |
|--------|------|---------|-----|
| Cyclomatic Complexity | < 5 | 5-10 | > 10 |
| Function Length | < 30 lines | 30-50 | > 50 |
| Class Length | < 200 lines | 200-300 | > 300 |
| Nesting Depth | < 3 | 3-4 | > 4 |
| Code Duplication | < 3% | 3-5% | > 5% |
| Test Coverage | > 90% | 80-90% | < 80% |

## Code Quality Checklist

- [ ] All functions have single responsibility
- [ ] No function exceeds 50 lines
- [ ] No class exceeds 300 lines
- [ ] Cyclomatic complexity < 10 per function
- [ ] No code duplication (DRY principle)
- [ ] Meaningful variable/function names
- [ ] No console.log in production code
- [ ] No TODO/FIXME comments
- [ ] Test coverage > 80%
- [ ] SOLID principles followed
- [ ] No magic numbers (use constants)
- [ ] Error handling present
- [ ] Comments explain WHY, not WHAT

---

## Verification Before Completion

**Before marking code as complete, verify:**

```
Code Quality Verification:
- [ ] All tests passing (100% green)
- [ ] Code coverage > 80%
- [ ] No linting errors
- [ ] No type errors
- [ ] No console.log statements
- [ ] No TODO/FIXME comments
- [ ] All edge cases handled
- [ ] Error handling complete
- [ ] Performance acceptable
- [ ] Security review passed
- [ ] Documentation complete
- [ ] Ready for production
```

**Verification Checklist**:
1. Run tests: `npm test` (all passing)
2. Check coverage: `npm run coverage` (>80%)
3. Lint code: `npm run lint` (no errors)
4. Type check: `npm run type-check` (no errors)
5. Build: `npm run build` (succeeds)
6. Manual testing: Verify all features work
7. Security scan: Check for vulnerabilities
8. Performance: Verify acceptable speed
9. Documentation: Update README/comments
10. Final review: Code ready for production

---

**Remember**: Code quality is an investment in the future. Clean code saves time and money!
