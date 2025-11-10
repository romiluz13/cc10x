# Code Quality Patterns - Pattern Library

Reference patterns for code quality analysis. Use AFTER understanding codebase conventions (see SKILL.md Phase 2).

## Quality Pattern Library

### Naming Conventions

**Understand codebase naming conventions first, then check**:

**Function Naming** (aligned with codebase pattern):

```typescript
// Check: Are function names clear and aligned with codebase?
// BAD (if codebase uses camelCase)
function process_data(file) {}

// GOOD (aligned with codebase camelCase pattern)
function processFileData(file) {}

// Check: Do names indicate functionality?
// BAD - Can't understand what it does
function process(user) {}

// GOOD - Clear what functionality does
function validateAndSaveUser(user) {}
```

**Variable Naming** (aligned with codebase pattern):

```typescript
// Check: Are variable names clear?
// BAD - Can't understand what data represents
const d = new Date();
const x = users.filter((u) => u.age > 18);

// GOOD - Clear what data represents (aligned with codebase)
const currentDate = new Date();
const adultUsers = users.filter((user) => user.age > 18);
```

**Component Naming** (aligned with codebase pattern):

```typescript
// Check: Are component names aligned with codebase PascalCase?
// BAD (if codebase uses PascalCase)
function upload_form() {}

// GOOD (aligned with codebase PascalCase pattern)
function UploadForm() {}
```

### Code Organization Patterns

**Understand codebase organization patterns first, then check**:

**File Organization** (aligned with codebase structure):

```typescript
// Check: Is code organized according to codebase structure?
// BAD (if codebase separates components and utils)
// components/UploadForm.tsx (contains utility functions)

// GOOD (aligned with codebase structure)
// components/UploadForm.tsx (component only)
// utils/file-validation.ts (utilities)
```

**Function Organization** (aligned with codebase patterns):

```typescript
// Check: Are functions organized according to codebase patterns?
// BAD (if codebase uses small focused functions)
function handleUpload(file) {
  // 100 lines of validation, upload, sync logic
}

// GOOD (aligned with codebase pattern of small focused functions)
function handleUpload(file) {
  validateFile(file);
  const url = uploadFile(file);
  syncToCRM(url);
}

function validateFile(file) {
  /* ... */
}
function uploadFile(file) {
  /* ... */
}
function syncToCRM(url) {
  /* ... */
}
```

### Error Handling Patterns

**Understand codebase error handling patterns first, then check**:

**Error Handling** (aligned with codebase pattern):

```typescript
// Check: Is error handling aligned with codebase patterns?
// BAD (if codebase uses custom error classes)
try {
  await uploadFile(file);
} catch (error) {
  console.log(error);
}

// GOOD (aligned with codebase custom error class pattern)
import { FileUploadError } from "../errors/file-upload-error";

try {
  await uploadFile(file);
} catch (error) {
  throw new FileUploadError("Failed to upload file", { cause: error });
}
```

### Testing Patterns

**Understand codebase testing patterns first, then check**:

**Test Organization** (aligned with codebase testing patterns):

```typescript
// Check: Are tests aligned with codebase testing patterns?
// BAD (if codebase uses Jest with React Testing Library)
// No tests

// GOOD (aligned with codebase Jest + React Testing Library pattern)
import { render, screen } from '@testing-library/react';
import { UploadForm } from './UploadForm';

describe('UploadForm', () => {
  it('should upload file successfully', async () => {
    render(<UploadForm />);
    // Test implementation aligned with codebase patterns
  });
});
```

### Code Duplication Patterns

**Understand codebase DRY patterns first, then check**:

**Duplication** (only flag if prevents fixing bugs in one place):

```typescript
// Check: Does duplication prevent fixing bugs in one place?
// BAD - Bug fix needs to be applied in multiple places
function validateEmail(email) {
  if (!email.includes("@")) throw new Error("Invalid email");
  if (email.length < 5) throw new Error("Email too short");
}

function validatePhone(phone) {
  if (!phone.includes("-")) throw new Error("Invalid phone");
  if (phone.length < 10) throw new Error("Phone too short");
}

// GOOD - Bug fix in one place (aligned with codebase validation pattern)
import { z } from "zod"; // If codebase uses Zod

const emailSchema = z.string().email().min(5);
const phoneSchema = z.string().regex(/^-/).min(10);

function validateEmail(email) {
  return emailSchema.parse(email);
}

function validatePhone(phone) {
  return phoneSchema.parse(phone);
}
```

### Complexity Patterns

**Understand codebase complexity tolerance first, then check**:

**Function Complexity** (only flag if prevents understanding functionality):

```typescript
// Check: Does complexity prevent understanding functionality?
// BAD - Can't understand what functionality does
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

// GOOD - Clear functionality (aligned with codebase pattern of small functions)
function processUser(user) {
  if (!isEligible(user)) return;
  handlePremiumUser(user);
}

function isEligible(user) {
  return user.age > 18 && user.verified && user.active;
}

function handlePremiumUser(user) {
  if (user.premium) {
    // ... premium logic
  } else {
    // ... regular logic
  }
}
```

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
    db.insert("users", this);
  }

  sendEmail() {
    // Sending email
    emailService.send(this.email, "Welcome!");
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
    db.insert("users", user);
  }
}

class EmailService {
  sendWelcome(user) {
    this.send(user.email, "Welcome!");
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
    if (payment.type === "credit") {
      // Process credit card
    } else if (payment.type === "paypal") {
      // Process PayPal
    } else if (payment.type === "stripe") {
      // Process Stripe
    }
  }
}

// FOLLOWS OCP
interface PaymentMethod {
  process(payment): Promise<void>;
}

class CreditCardProcessor implements PaymentMethod {
  process(payment) {
    /* ... */
  }
}

class PayPalProcessor implements PaymentMethod {
  process(payment) {
    /* ... */
  }
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
  fly() {
    return "flying";
  }
}

class Penguin extends Bird {
  fly() {
    throw new Error("Penguins cannot fly");
  }
}

// FOLLOWS LSP
class Bird {
  move() {
    return "moving";
  }
}

class FlyingBird extends Bird {
  fly() {
    return "flying";
  }
}

class Penguin extends Bird {
  swim() {
    return "swimming";
  }
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
  work() {
    /* ... */
  }
  eat() {
    throw new Error("Robots do not eat");
  }
  sleep() {
    throw new Error("Robots do not sleep");
  }
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
  work() {
    /* ... */
  }
}

class Human implements Workable, Eatable, Sleepable {
  work() {
    /* ... */
  }
  eat() {
    /* ... */
  }
  sleep() {
    /* ... */
  }
}
```

### D: Dependency Inversion Principle

**What**: Depend on abstractions, not concretions.

```typescript
// VIOLATES DIP
class UserService {
  private db = new MongoDBClient();

  getUser(id) {
    return this.db.collection("users").findOne({ _id: id });
  }
}

// FOLLOWS DIP
interface Database {
  findOne(collection: string, query: any): Promise<any>;
}

class UserService {
  constructor(private db: Database) {}

  getUser(id) {
    return this.db.findOne("users", { id });
  }
}
```
