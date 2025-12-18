# Example: Well-Maintained STATUS.md

This example shows what a properly maintained STATUS.md looks like after several sessions of active development.

---

## Current State
Building user authentication module. Login component complete, working on registration flow.

## Last Session
- Date: 2024-01-15 16:30
- What was done: Completed login component with tests, started registration form UI
- Exit state: in-progress (registration form 60% complete)

## Active Work
- Component: UserRegistration
- Phase: BUILD Phase 4 (Component Loop)
- Status: Registration form UI done, validation logic next

## Critical Context
- Using React Hook Form for all forms (see patterns.md)
- Validation uses Zod schema (ADR-003)
- Auth tokens stored in httpOnly cookies (security requirement)
- Backend API expects camelCase fields
- Password must be 12+ chars with special char (constraint)

## Blockers
- Email verification service not yet configured (waiting on DevOps)
  - Workaround: Mock email service in dev environment
  - Tracking in blockers.md

---

# Example: NEXT-STEPS.md After Same Session

## Immediate (Do First)
1. Complete registration form validation logic
   - Use Zod schema like login (see learnings/patterns.md)
   - Handle all error cases from API
2. Connect registration form to /api/auth/register endpoint
   - API spec in context/apis.md
3. Add registration success redirect to login

## Soon (After Immediate)
- Add password strength indicator component
- Implement "forgot password" flow (depends on email service)
- Add social auth buttons (Google, GitHub)

## Later (When Time Permits)
- Add rate limiting to auth endpoints
- Implement session refresh mechanism
- Add audit logging for auth events

## Dependencies
- "Forgot password" blocked by email service configuration
- Social auth depends on OAuth credentials (in progress with DevOps)

---

# Example: CONTEXT-SNAPSHOT.md for Same Project

## Project
User authentication system for SaaS platform. Handles user registration, login, password management, and session management. Built with security-first approach using modern React patterns.

## Tech Stack
- Language: TypeScript 5.3
- Framework: Next.js 14 (App Router)
- Key Libraries:
  - react-hook-form (forms)
  - zod (validation)
  - next-auth (auth framework)
  - bcrypt (password hashing)

## Architecture
```
Client (React) → Next.js API Routes → Auth Service → PostgreSQL
                                    ↓
                              Redis (sessions)
```

## Key Files
- `src/app/auth/login/page.tsx` - Login page component
- `src/app/auth/register/page.tsx` - Registration page (in progress)
- `src/app/api/auth/[...nextauth]/route.ts` - NextAuth configuration
- `src/lib/auth/validation.ts` - Zod schemas for auth forms
- `src/lib/auth/session.ts` - Session management utilities

## Current Focus
Authentication module - specifically UserRegistration component

## Quick Commands
- Build: `npm run build`
- Test: `npm test`
- Run: `npm run dev`
- Test auth: `npm test -- --grep "auth"`

---

# Key Takeaways

1. **STATUS.md is concise but complete** - One glance tells you everything
2. **Critical Context includes gotchas** - Things AI needs to know to avoid mistakes
3. **NEXT-STEPS is prioritized** - Clear what to do first
4. **Dependencies are explicit** - Knows what's blocked
5. **CONTEXT-SNAPSHOT has quick commands** - Instant productivity

This is what "perfect context" looks like. Any new session reading these 3 files can immediately continue productive work.
