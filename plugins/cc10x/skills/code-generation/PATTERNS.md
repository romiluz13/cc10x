# Code Generation Patterns Library

This document provides a comprehensive library of code generation patterns covering API scaffolding, component scaffolding, page scaffolding, and security patterns.

## API Scaffolding Patterns

### Next.js 15 App Router Patterns

- **Route handlers**: Use `route.ts` files in `app/api/` directory
- **Route segments**: Organize routes by feature, not by type
- **Server components**: Use server components by default, client components when needed
- **Streaming**: Use streaming for better performance
- **Suspense boundaries**: Use Suspense for loading states

### API Route Structure Patterns

```typescript
// app/api/resource/route.ts
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const schema = z.object({
  // Define schema
});

export async function GET(request: NextRequest) {
  // GET handler
}

export async function POST(request: NextRequest) {
  // POST handler with validation
}
```

### Zod Validation Patterns

- **Request validation**: Validate all inputs with Zod schemas
- **Response validation**: Validate responses for type safety
- **Error handling**: Return validation errors in consistent format
- **Type inference**: Use Zod's type inference for TypeScript types

### Consistent Error Response Format

```typescript
// Success response
{
  data: T,
  success: true
}

// Error response
{
  error: string,
  success: false
}
```

### TypeScript Strict Typing Patterns

- **Strict mode**: Use TypeScript strict mode
- **Type inference**: Leverage TypeScript's type inference
- **Generic types**: Use generics for reusable code
- **Type guards**: Use type guards for runtime type checking

### API Security Patterns

- **Input sanitization**: Sanitize all user inputs
- **CORS configuration**: Configure CORS properly
- **Rate limiting**: Implement rate limiting for API endpoints
- **Authentication**: Verify authentication before processing
- **Authorization**: Check permissions before allowing actions

## Component Scaffolding Patterns

### React 19 Feature Usage

- **`use()` hook**: Use for reading promises and context
- **`useActionState()` hook**: Use for form actions with state
- **`useFormStatus()` hook**: Use for form submission status
- **`useOptimistic()` hook**: Use for optimistic updates
- **Server components**: Use server components by default

### Component Type Selection

- **Presentational components**: Display-only components (no state, no side effects)
- **Container components**: Components that manage state and side effects
- **Compound components**: Components that work together (e.g., Select + Option)

### Component Structure Patterns

```typescript
// Presentational component
interface ComponentProps {
  // Props definition
}

export function Component({ prop1, prop2 }: ComponentProps) {
  return (
    // JSX
  );
}

// Container component
export function ContainerComponent() {
  const [state, setState] = useState();

  useEffect(() => {
    // Side effects
  }, []);

  return <PresentationalComponent {...props} />;
}
```

### TypeScript Strict Typing Patterns

- **Props interfaces**: Define clear prop interfaces
- **Default props**: Use default parameters for optional props
- **Children types**: Use `React.ReactNode` for children
- **Event handlers**: Type event handlers properly

### Accessibility-First Approach

- **Semantic HTML**: Use semantic HTML elements
- **ARIA labels**: Add ARIA labels where needed
- **Keyboard navigation**: Ensure keyboard accessibility
- **Focus management**: Manage focus properly
- **Screen reader support**: Ensure screen reader compatibility

### Performance Optimization Patterns

- **Memoization**: Use `React.memo()` for expensive components
- **Code splitting**: Use dynamic imports for code splitting
- **Lazy loading**: Lazy load components when possible
- **Optimistic updates**: Use optimistic updates for better UX

### Code Quality Standards

- **Component size**: Keep components <200 lines
- **Single responsibility**: One component, one purpose
- **Prop drilling prevention**: Use context for deep prop passing
- **Error boundaries**: Use error boundaries for error handling

## Page Scaffolding Patterns

### Next.js 15 App Router Page Patterns

- **Server components**: Use server components by default
- **Client components**: Use `'use client'` directive when needed
- **Metadata**: Use metadata API for SEO
- **Loading states**: Use `loading.tsx` for loading states
- **Error states**: Use `error.tsx` for error states

### Page Structure Patterns

```typescript
// app/feature/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
};

export default async function Page() {
  // Server component logic
  return (
    // JSX
  );
}
```

### Data Fetching Patterns

- **Server-side fetching**: Fetch data in server components
- **Streaming**: Use streaming for better performance
- **Suspense**: Use Suspense for loading states
- **Error handling**: Handle errors gracefully

## Security Patterns

### Multi-Layer Security Approach

- **Authentication**: Verify user identity
- **Authorization**: Check user permissions
- **Input validation**: Validate all inputs
- **Rate limiting**: Prevent abuse
- **CORS**: Configure CORS properly

### Stack-Specific Auth Patterns

- **NextAuth.js**: Use NextAuth.js for authentication
- **Custom auth**: Implement custom auth when needed
- **Token-based**: Use JWT tokens for stateless auth
- **Session-based**: Use sessions for stateful auth

### Security Checklist Patterns

- [ ] Authentication implemented
- [ ] Authorization checks in place
- [ ] Input validation on all endpoints
- [ ] Rate limiting configured
- [ ] CORS configured properly
- [ ] Secrets in environment variables
- [ ] Error messages don't leak sensitive info
- [ ] HTTPS enforced in production

### Common Auth Patterns

- **Token-based auth**: JWT tokens for API authentication
- **User-based auth**: User-specific permissions
- **Role-based auth**: Role-based access control (RBAC)

### Error Handling Security Patterns

- **Generic error messages**: Don't leak sensitive information
- **Error logging**: Log errors securely
- **Error boundaries**: Use error boundaries for graceful degradation

## Pattern Usage

Reference these patterns when generating code:

1. **API Generation**: Use Next.js 15 App Router patterns, Zod validation, consistent error format, TypeScript strict typing, security patterns
2. **Component Generation**: Use React 19 features, component type selection, TypeScript strict typing, accessibility-first, performance optimization, code quality standards
3. **Page Generation**: Use Next.js 15 App Router page patterns, data fetching patterns
4. **Security**: Use multi-layer security approach, stack-specific auth patterns, security checklist, common auth patterns, error handling security

## Pattern Composition

These patterns can be composed together:

- API Scaffolding + Security = Secure API endpoints
- Component Scaffolding + Accessibility = Accessible components
- Component Scaffolding + Performance = Optimized components
- Page Scaffolding + Data Fetching = Complete pages
- Security + Error Handling = Secure error handling

See `plugins/cc10x/skills/shared-patterns/PATTERN-COMPOSITION.md` for composition guidelines.
