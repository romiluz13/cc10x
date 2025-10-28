# Phase 4: APIs & Data Models

**Objective**: Establish contracts between frontend and backend  
**Duration**: 2-3 minutes

## API Endpoints

```markdown
[API Design]

POST /api/auth/register
Request:
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
Response (201 Created):
{
  "token": "eyJhbGc...",
  "user": {
    "id": "usr_123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2025-10-22T10:00:00Z"
  }
}
Error (400 Bad Request):
{
  "error": "Email already exists"
}

POST /api/auth/login
Request:
{
  "email": "user@example.com",
  "password": "securepassword123"
}
Response (200 OK):
{
  "token": "eyJhbGc...",
  "user": { ... }
}
Error (401 Unauthorized):
{
  "error": "Invalid credentials"
}
```

## Data Models

```markdown
[Database Schema]

Table: users
┌─────────────┬──────────────┬─────────────┐
│ Column      │ Type         │ Constraints │
├─────────────┼──────────────┼─────────────┤
│ id          │ UUID         │ PRIMARY KEY │
│ email       │ VARCHAR(255) │ UNIQUE, NOT NULL │
│ password_hash│ VARCHAR(255)│ NOT NULL    │
│ name        │ VARCHAR(255) │ NOT NULL    │
│ created_at  │ TIMESTAMP    │ DEFAULT NOW │
│ updated_at  │ TIMESTAMP    │ DEFAULT NOW │
└─────────────┴──────────────┴─────────────┘

Indexes:
- idx_users_email ON users(email)
```

## Quality Gate

- ✅ API contracts are complete and consistent
- ✅ Data models support all required operations
- ✅ Indexes for query performance
- ❌ If inconsistent → Align API with data model

