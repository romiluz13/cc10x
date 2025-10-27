---
name: code-generation
description: Code generation patterns and templates for common implementations. Use when implementing features to follow best practices.
allowed-tools: Read, Edit, Write, Grep
---

# Code Generation Patterns

Essential templates for generating production-quality code.

## REST API Endpoint (TypeScript + Express)

```typescript
import { Router } from 'express';
import { z } from 'zod';
import { asyncHandler } from '../middleware/asyncHandler';
import { authenticate, authorize } from '../middleware/auth';
import { UserService } from '../services/UserService';

const router = Router();
const userService = new UserService();

// Input validation schema
const createUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(2).max(100),
  role: z.enum(['user', 'admin']).default('user')
});

// GET /users
router.get('/users', authenticate, authorize('admin'), asyncHandler(async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const users = await userService.findAll({
    page: Number(page),
    limit: Number(limit)
  });
  res.json({ data: users });
}));

// POST /users
router.post('/users', authenticate, authorize('admin'), asyncHandler(async (req, res) => {
  const validated = createUserSchema.parse(req.body);
  const user = await userService.create(validated);
  res.status(201).json({ data: user, message: 'User created successfully' });
}));

export default router;
```

## Service Layer

```typescript
import { UserRepository } from '../repositories/UserRepository';
import { ValidationError, NotFoundError } from '../errors';
import { logger } from '../utils/logger';

export class UserService {
  constructor(private userRepository = new UserRepository()) {}
  
  async findById(id: string) {
    if (!id) throw new ValidationError('User ID is required');
    
    try {
      return await this.userRepository.findById(id);
    } catch (error) {
      logger.error('Failed to find user', { userId: id, error });
      throw error;
    }
  }
  
  async create(data) {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) throw new ValidationError('Email already in use');
    
    try {
      const user = await this.userRepository.create(data);
      logger.info('User created', { userId: user.id });
      return user;
    } catch (error) {
      logger.error('Failed to create user', { data, error });
      throw error;
    }
  }
}
```

## Repository Pattern

```typescript
export class UserRepository {
  async findById(id: string) {
    return await db.users.findUnique({
      where: { id },
      select: { id: true, email: true, name: true, role: true }
    });
  }
  
  async findAll(options: { page: number; limit: number }) {
    return await db.users.findMany({
      skip: (options.page - 1) * options.limit,
      take: options.limit,
      orderBy: { createdAt: 'desc' }
    });
  }
  
  async create(data) {
    return await db.users.create({ data });
  }
  
  async update(id: string, data) {
    return await db.users.update({ where: { id }, data });
  }
}
```

## React Component

```typescript
import { useState, useEffect } from 'react';

export function UserList({ onUserSelect }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    loadUsers();
  }, []);
  
  async function loadUsers() {
    try {
      setLoading(true);
      setError(null);
      const data = await userService.findAll();
      setUsers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }
  
  if (loading) return <LoadingSpinner message="Loading users..." />;
  if (error) return <ErrorMessage message={error} onRetry={loadUsers} />;
  if (users.length === 0) return <div>No users found</div>;
  
  return (
    <ul className="user-list">
      {users.map(user => (
        <li key={user.id}>
          <button onClick={() => onUserSelect?.(user)}>
            <span>{user.name}</span>
            <span>{user.email}</span>
          </button>
        </li>
      ))}
    </ul>
  );
}
```

## Custom Hook

```typescript
import { useState, useEffect } from 'react';

export function useAsync(asyncFunction, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  async function execute() {
    try {
      setLoading(true);
      setError(null);
      const result = await asyncFunction();
      setData(result);
      options.onSuccess?.(result);
      return result;
    } catch (err) {
      setError(err);
      options.onError?.(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }
  
  useEffect(() => {
    if (options.immediate !== false) execute();
  }, []);
  
  return { data, loading, error, execute };
}
```

## Error Classes

```typescript
export class AppError extends Error {
  constructor(message, statusCode = 500, code = 'INTERNAL_ERROR') {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.name = this.constructor.name;
  }
}

export class ValidationError extends AppError {
  constructor(message, field) {
    super(message, 400, 'VALIDATION_ERROR');
    this.field = field;
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}
```

## Middleware

```typescript
// Error handler
export function errorHandler(err, req, res, next) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { message: err.message, code: err.code }
    });
  }
  
  logger.error('Unexpected error', { error: err });
  res.status(500).json({
    error: { message: 'Internal server error', code: 'INTERNAL_ERROR' }
  });
}

// Async handler wrapper
export function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Authentication
export async function authenticate(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) throw new UnauthorizedError('No token provided');
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}

// Authorization
export function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) throw new UnauthorizedError('Not authenticated');
    if (!roles.includes(req.user.role)) throw new ForbiddenError('Insufficient permissions');
    next();
  };
}
```

## Test Template

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { UserService } from './UserService';
import { ValidationError } from '../errors';

vi.mock('../repositories/UserRepository');

describe('UserService', () => {
  let userService;
  let userRepository;
  
  beforeEach(() => {
    userRepository = new UserRepository();
    userService = new UserService(userRepository);
  });
  
  describe('findById', () => {
    it('should return user when found', async () => {
      const mockUser = { id: '1', name: 'Test', email: 'test@example.com' };
      userRepository.findById.mockResolvedValue(mockUser);
      
      const result = await userService.findById('1');
      
      expect(result).toEqual(mockUser);
      expect(userRepository.findById).toHaveBeenCalledWith('1');
    });
    
    it('should throw ValidationError for empty ID', async () => {
      await expect(userService.findById('')).rejects.toThrow(ValidationError);
    });
  });
  
  describe('create', () => {
    it('should create user successfully', async () => {
      const createData = { name: 'Test', email: 'test@example.com', role: 'user' };
      const mockUser = { id: '1', ...createData };
      
      userRepository.findByEmail.mockResolvedValue(null);
      userRepository.create.mockResolvedValue(mockUser);
      
      const result = await userService.create(createData);
      
      expect(result).toEqual(mockUser);
    });
  });
});
```

## Best Practices

✅ **Do:**
- Include error handling everywhere
- Add type safety (TypeScript)
- Write comprehensive tests
- Log appropriately (debug, info, error)
- Validate all inputs
- Follow SOLID principles
- Keep functions small (< 50 lines)
- Use meaningful, descriptive names
- Handle async/await properly
- Return consistent response formats

❌ **Don't:**
- Skip error handling
- Use `any` type in TypeScript
- Hardcode sensitive values
- Ignore edge cases
- Leave TODOs or placeholders
- Create large classes (> 300 lines)
- Mix multiple concerns in one function
- Expose sensitive data in responses
- Forget to await promises
- Return inconsistent formats

## Common Patterns

### Pagination
```typescript
const { page = 1, limit = 20 } = req.query;
const users = await service.findAll({
  skip: (page - 1) * limit,
  take: limit
});
```

### Error Response
```typescript
res.status(statusCode).json({
  error: { message, code, field }
});
```

### Success Response
```typescript
res.status(200).json({
  data: result,
  message: 'Operation successful'
});
```

### Validation
```typescript
const schema = z.object({
  email: z.string().email(),
  age: z.number().min(18)
});
const validated = schema.parse(input);
```

### Logging
```typescript
logger.debug('Operation started', { context });
logger.info('Operation completed', { result });
logger.error('Operation failed', { error });
```
