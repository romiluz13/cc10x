---
name: planning-design-deployment
description: Produces API, component, testing, and deployment plans for the planning workflow. Loads api-design-patterns, component-design-patterns, deployment-patterns, and verification-before-completion.
---

# Planning - Design & Deployment

## Scope
- Build on the requirements and architecture outputs to deliver an implementation roadmap.

## Required Skills
- `api-design-patterns`
- `component-design-patterns`
- `deployment-patterns`
- `verification-before-completion`

## Process
1. Define API contracts, request/response schemas, and authentication expectations.
2. Outline component hierarchy, state management, and props/interfaces.
3. Draft a phased implementation plan with file manifest and estimates.
4. Recommend testing strategy (unit, integration, e2e) tied to requirements.
5. Describe deployment, monitoring, and rollback steps.

## Output
- API design table (endpoint, method, auth, payload).
- Component tree with responsibilities.
- Implementation phases and file manifest.
- Deployment checklist with rollback triggers.
- Outstanding dependencies or blockers.

## Verification
- Cross-reference requirements IDs or user stories from Phase 1.
- Cite relevant skill sections for key decisions.
- Include a short summary of validation commands if any scripts or tools are recommended.

## Example (API Design Table)
| Endpoint | Method | Auth | Request | Response |
|----------|--------|------|---------|----------|
| /v1/users | GET | JWT | query: {id?} | 200: User[] |
| /v1/users | POST | JWT | body: {email, name} | 201: User |
