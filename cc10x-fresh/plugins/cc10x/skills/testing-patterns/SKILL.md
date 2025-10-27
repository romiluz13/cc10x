---
name: testing-patterns
description: Testing patterns for unit, integration, and E2E tests with comprehensive coverage strategies.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Testing Patterns & Best Practices

Comprehensive testing strategies for production-quality code.

## Test Structure (AAA Pattern)

```typescript
describe('Feature', () => {
  it('should behavior when condition', () => {
    // Arrange - Setup test data and dependencies
    const input = { ... };
    const expected = { ... };
    
    // Act - Execute the code being tested
    const result = functionUnderTest(input);
    
    // Assert - Verify the outcome
    expect(result).toEqual(expected);
  });
});
```

## Unit Testing

### Testing Functions
```typescript
import { calculateTotal } from './calculator';

describe('calculateTotal', () => {
  it('should sum all item prices', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ];
    
    const total = calculateTotal(items);
    
    expect(total).toBe(35); // (10*2) + (5*3)
  });
  
  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
  
  it('should handle items with zero price', () => {
    const items = [{ price: 0, quantity: 5 }];
    expect(calculateTotal(items)).toBe(0);
  });
  
  it('should throw error for negative prices', () => {
    const items = [{ price: -10, quantity: 1 }];
    expect(() => calculateTotal(items)).toThrow('Price cannot be negative');
  });
});
```

### Testing Classes
```typescript
import { UserService } from './UserService';
import { UserRepository } from './UserRepository';

// Mock dependencies
vi.mock('./UserRepository');

describe('UserService', () => {
  let userService: UserService;
  let mockRepository: jest.Mocked<UserRepository>;
  
  beforeEach(() => {
    mockRepository = new UserRepository() as jest.Mocked<UserRepository>;
    userService = new UserService(mockRepository);
  });
  
  afterEach(() => {
    vi.clearAllMocks();
  });
  
  describe('findById', () => {
    it('should return user when found', async () => {
      const mockUser = { id: '1', name: 'Test' };
      mockRepository.findById.mockResolvedValue(mockUser);
      
      const result = await userService.findById('1');
      
      expect(result).toEqual(mockUser);
      expect(mockRepository.findById).toHaveBeenCalledWith('1');
      expect(mockRepository.findById).toHaveBeenCalledTimes(1);
    });
  });
});
```

## Mocking

### Mock Functions
```typescript
const mockFn = vi.fn();

// Configure return value
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: 'async' }); // For promises
mockFn.mockRejectedValue(new Error('Failed')); // For errors

// Assertions
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenCalledTimes(3);
```

### Mock Modules
```typescript
// Mock entire module
vi.mock('../services/api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: '1' }),
  updateUser: vi.fn()
}));

// Partial mock (keep some real implementations)
vi.mock('../utils/helpers', async () => {
  const actual = await vi.importActual('../utils/helpers');
  return {
    ...actual,
    someFunction: vi.fn() // Override this one
  };
});
```

### Mock Timers
```typescript
describe('setTimeout behavior', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  
  afterEach(() => {
    vi.restoreAllMocks();
  });
  
  it('should call callback after delay', () => {
    const callback = vi.fn();
    
    setTimeout(callback, 1000);
    
    expect(callback).not.toHaveBeenCalled();
    
    vi.advanceTimersByTime(1000);
    
    expect(callback).toHaveBeenCalledTimes(1);
  });
});
```

## Integration Testing

### API Integration Tests
```typescript
import request from 'supertest';
import app from '../app';
import { db } from '../db';

describe('POST /api/users', () => {
  beforeEach(async () => {
    await db.users.deleteMany(); // Clean database
  });
  
  it('should create user successfully', async () => {
    const userData = {
      name: 'Test User',
      email: 'test@example.com'
    };
    
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);
    
    expect(response.body.data).toMatchObject({
      name: userData.name,
      email: userData.email
    });
    expect(response.body.data.id).toBeDefined();
    
    // Verify in database
    const user = await db.users.findUnique({
      where: { email: userData.email }
    });
    expect(user).toBeTruthy();
  });
  
  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'invalid' })
      .expect(400);
    
    expect(response.body.error).toBeDefined();
  });
  
  it('should return 409 for duplicate email', async () => {
    const userData = { name: 'Test', email: 'test@example.com' };
    
    await request(app).post('/api/users').send(userData);
    
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(409);
    
    expect(response.body.error).toContain('already exists');
  });
});
```

## React Testing

### Component Testing
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserList } from './UserList';
import { userService } from '../services/userService';

vi.mock('../services/userService');

describe('UserList', () => {
  it('should display loading state initially', () => {
    vi.mocked(userService.findAll).mockResolvedValue([]);
    
    render(<UserList />);
    
    expect(screen.getByText('Loading users...')).toBeInTheDocument();
  });
  
  it('should display users when loaded', async () => {
    const mockUsers = [
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' }
    ];
    vi.mocked(userService.findAll).mockResolvedValue(mockUsers);
    
    render(<UserList />);
    
    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeInTheDocument();
      expect(screen.getByText('Bob')).toBeInTheDocument();
    });
  });
  
  it('should display error message on failure', async () => {
    vi.mocked(userService.findAll).mockRejectedValue(new Error('API Error'));
    
    render(<UserList />);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to load users/)).toBeInTheDocument();
    });
  });
  
  it('should call onUserSelect when user clicked', async () => {
    const mockUsers = [{ id: '1', name: 'Alice', email: 'alice@example.com' }];
    vi.mocked(userService.findAll).mockResolvedValue(mockUsers);
    const onUserSelect = vi.fn();
    
    render(<UserList onUserSelect={onUserSelect} />);
    
    await waitFor(() => screen.getByText('Alice'));
    
    fireEvent.click(screen.getByText('Alice'));
    
    expect(onUserSelect).toHaveBeenCalledWith(mockUsers[0]);
  });
});
```

### Hook Testing
```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useAsync } from './useAsync';

describe('useAsync', () => {
  it('should execute function immediately', async () => {
    const asyncFn = vi.fn().mockResolvedValue('data');
    
    const { result } = renderHook(() => useAsync(asyncFn, { immediate: true }));
    
    expect(result.current.loading).toBe(true);
    
    await waitFor(() => {
      expect(result.current.data).toBe('data');
      expect(result.current.loading).toBe(false);
    });
  });
  
  it('should handle errors', async () => {
    const asyncFn = vi.fn().mockRejectedValue(new Error('Failed'));
    
    const { result } = renderHook(() => useAsync(asyncFn, { immediate: true }));
    
    await waitFor(() => {
      expect(result.current.error).toEqual(new Error('Failed'));
      expect(result.current.loading).toBe(false);
    });
  });
});
```

## E2E Testing (Playwright/Cypress)

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('should register new user successfully', async ({ page }) => {
    // Navigate
    await page.goto('/register');
    
    // Fill form
    await page.fill('[name="name"]', 'Test User');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123');
    
    // Submit
    await page.click('button[type="submit"]');
    
    // Verify success
    await expect(page.locator('.success-message')).toContainText('Registration successful');
    
    // Verify navigation
    await expect(page).toHaveURL('/dashboard');
  });
  
  test('should show validation errors', async ({ page }) => {
    await page.goto('/register');
    
    await page.click('button[type="submit"]'); // Submit empty form
    
    await expect(page.locator('.error-message')).toContainText('Name is required');
  });
});
```

## Test Coverage

### Aim for 80%+ Coverage
```bash
# Run tests with coverage
npm run test:coverage

# View coverage report
open coverage/index.html
```

### What to Test
✅ **Test:**
- All business logic
- Error handling
- Edge cases
- Boundary conditions
- User interactions
- API integrations

❌ **Don't Test:**
- External libraries
- Simple getters/setters
- Framework code
- Configuration files

## Test Organization

```
src/
  components/
    UserList.tsx
    UserList.test.tsx          # Co-located tests
  services/
    userService.ts
    userService.test.ts
tests/
  integration/
    api.test.ts                # Integration tests
  e2e/
    user-registration.spec.ts  # E2E tests
  helpers/
    testUtils.tsx              # Test utilities
```

## Testing Best Practices

### ✅ Do
- Test behavior, not implementation
- Use descriptive test names
- One assertion per test (when possible)
- Keep tests independent
- Clean up after tests
- Mock external dependencies
- Test edge cases
- Write tests first (TDD)

### ❌ Don't
- Test implementation details
- Use vague test names ("it works")
- Have tests depend on each other
- Skip cleanup
- Test too many things at once
- Have flaky tests
- Ignore failing tests

## Test Naming Convention

```typescript
// ✅ Good - Describes behavior
it('should return 404 when user not found')
it('should validate email format')
it('should disable submit button while loading')

// ❌ Bad - Vague or implementation-focused
it('works')
it('test user service')
it('calls findById')
```

## Snapshot Testing

```typescript
import { render } from '@testing-library/react';
import { UserCard } from './UserCard';

it('should match snapshot', () => {
  const user = { id: '1', name: 'Test', email: 'test@example.com' };
  const { container } = render(<UserCard user={user} />);
  
  expect(container).toMatchSnapshot();
});
```

## Performance Testing

```typescript
it('should complete under 100ms', async () => {
  const start = performance.now();
  
  await expensiveOperation();
  
  const duration = performance.now() - start;
  expect(duration).toBeLessThan(100);
});
```

## Testing Checklist

- [ ] All happy paths tested
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Null/undefined handled
- [ ] Boundary conditions tested
- [ ] Async operations tested
- [ ] Mocks used appropriately
- [ ] Tests are deterministic
- [ ] Tests are fast (< 1s each)
- [ ] Coverage >= 80%

