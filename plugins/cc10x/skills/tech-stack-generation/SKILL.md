---
name: tech-stack-generation
description: Use when planning features and user request contains "tech stack", "technical stack", "create tech stack" - generates comprehensive technical stack documentation from codebase analysis, documenting all technologies, frameworks, libraries, development tools, deployment strategies, and implementation patterns with specific versions and configurations
---

# Tech Stack Generation

## Overview

Generate comprehensive Tech Stack Documentation based on deep codebase analysis. Document all technologies, frameworks, libraries, development tools, deployment strategies, and implementation patterns with specific versions and configurations.

## When to Use

- User request contains "tech stack", "technical stack", "create tech stack"
- Planning new features and need technical documentation
- Onboarding new developers who need technical context
- Documenting technology decisions and configurations

## Process

### 1. Automated Technical Discovery

- Parse package.json for all dependencies
- Analyze configuration files (tsconfig, vite.config, next.config, etc.)
- Detect database setup (Prisma, Drizzle, TypeORM, etc.)
- Identify testing frameworks and tools
- Scan for CI/CD configurations
- Check deployment configurations

### 2. Deep Code Analysis

Examine codebase for:

- **Architecture Patterns:** Monorepo structure, module organization
- **Framework Usage:** Next.js app router vs pages, API routes
- **State Management:** Zustand, Redux, Context API patterns
- **Styling Approach:** Tailwind, CSS modules, styled-components
- **Type Safety:** TypeScript strictness, validation libraries
- **API Design:** REST, GraphQL, tRPC implementation
- **Authentication:** Auth libraries and session management
- **Testing Strategy:** Unit, integration, E2E test patterns

### 3. Interactive Technical Q&A

Ask 4-6 deployment and infrastructure questions:

- Use numbered/lettered options
- Focus on non-discoverable information
- Gather hosting, monitoring, and workflow details

**Required Questions:**

1. **Deployment & Infrastructure:**
   - Where is your application currently deployed? (Vercel, AWS, Railway/Render, Self-hosted, Other, Not deployed)

2. **Database Hosting:**
   - How is your database hosted? (Managed service, Cloud provider, Self-hosted, Local only)

3. **Monitoring & Operations:**
   - What observability tools do you use? (Error tracking, Analytics, Monitoring, Logging, None yet)

4. **Development Workflow:**
   - What's your Git workflow? (Feature branches, Trunk-based, GitFlow, Direct to main)

5. **Environment Management:**
   - How do you manage environments? (Multiple deployments, Preview deployments, Single production, Local only)

6. **External Services:**
   - Which external services do you integrate with? (Payment, Email, File storage, Authentication, Search, Other APIs)

### 4. Generate Comprehensive Documentation

Create detailed tech stack document with:

- Specific version numbers
- Configuration examples
- Command references
- Architecture diagrams (when applicable)

### 5. Save and Organize

- Create `.cursor/rules/` if needed
- Save as `tech-stack.mdc`
- Update CLAUDE.md commands section

## Document Structure

The generated document must follow this technical structure:

### Overview

- Brief description of the application's technical nature
- Technology stack summary
- Architecture approach (monolith, microservices, etc.)

### Programming Language & Runtime

- Primary programming language and version
- Runtime environment and version
- Type system and language features used

### Frontend

- UI Framework/Library and version
- Styling approach and frameworks
- Component libraries and design systems
- State management solutions
- Build tools and bundlers
- Browser support and compatibility

### Backend

- Backend framework and architecture
- API design (REST, GraphQL, tRPC, etc.)
- Authentication and authorization
- Middleware and security
- File handling and uploads

### Database & Storage

- Database type and version
- ORM/Query builder
- Schema management and migrations
- Caching solutions
- File storage solutions
- Data backup and recovery

### Development Tools & Workflow

- Package manager
- Code formatting and linting
- Type checking and compilation
- Testing frameworks and strategies
- Development server and hot reload
- Version control workflow

### Deployment & Infrastructure

- Hosting platform and services
- Build and deployment pipeline
- Environment configuration
- Domain and DNS management
- SSL/TLS and security
- Monitoring and logging

### External Integrations

- Third-party APIs and services
- Payment processing
- Email services
- Analytics and tracking
- Error monitoring
- Performance monitoring

### Quality Assurance & Testing

- Testing strategy and frameworks
- Code coverage tools
- End-to-end testing
- Performance testing
- Security testing
- Code review process

### Schemas & Data Models

- Database schema (if applicable)
- API schemas and validation
- Type definitions and interfaces
- Data relationships and constraints

## Documentation Principles

### DO Include:

- **Exact Versions:** Lock file versions, not just ranges
- **Configuration Examples:** Actual config snippets from the project
- **Command Reference:** All npm scripts and their purposes
- **Setup Instructions:** Step-by-step for new developers
- **Architecture Decisions:** Why specific technologies were chosen
- **Integration Details:** How services connect and communicate

### DON'T Include:

- **Generic Descriptions:** Avoid Wikipedia-style explanations
- **Outdated Information:** Only document what's actually used
- **Wishful Thinking:** Document current state, not future plans
- **Sensitive Data:** No API keys, secrets, or credentials
- **Redundant Info:** Link to official docs instead of copying

## Output

- **Format:** Markdown (`.mdc`)
- **Location:** `.cursor/rules/`
- **Filename:** `tech-stack.mdc`

## Integration with cc10x Orchestrator

This skill is invoked automatically by the PLAN workflow Phase 2 when:

- User request contains "tech stack" keywords
- Missing tech stack documentation is detected
- Technical documentation generation intent is identified

The skill executes BEFORE requirements intake, ensuring technical documentation is available for planning.
