---
name: api-design-patterns
description: Focused API design guidance. Thin wrapper around the API section of design-patterns with a compact checklist and examples. Used by planning-workflow, planning-design-deployment, and code-reviewer when API contracts are in scope.
---

# API Design Patterns (Focused)

## Progressive Loading Stages

### Stage 1: Metadata
- Purpose: Design and review HTTP APIs that are consistent, evolvable, and safe
- When: Planning new endpoints, reviewing API changes, preventing breaking changes
- Core Rule: APIs are contracts; prefer compatibility and explicit versioning

---

### Stage 2: Quick Reference

#### API Checklist
```
Fundamentals
- [ ] RESTful nouns and proper HTTP verbs
- [ ] Consistent resource naming and casing
- [ ] Standard status codes and error schema
- [ ] Pagination, filtering, sorting where applicable
- [ ] Authentication and authorization model documented

Reliability & Evolution
- [ ] Timeouts and retries defined (idempotency where needed)
- [ ] Backward-compatible changes or explicit versioning
- [ ] Rate limiting and headers documented
- [ ] Deprecation policy and timeline

DevEx & Quality
- [ ] OpenAPI/Swagger kept current
- [ ] Examples for success and error cases
- [ ] Validation of inputs/outputs (types, enums, ranges)
- [ ] Monitoring, logging, trace IDs
```

#### Examples
**Good REST structure**
```http
GET /api/users          # list
GET /api/users/{id}     # fetch one
POST /api/users         # create
PUT /api/users/{id}     # replace
PATCH /api/users/{id}   # partial update
DELETE /api/users/{id}  # delete
```

**Error schema**
```json
{
  "error": { "code": "USER_NOT_FOUND", "message": "User 123 not found", "status": 404, "traceId": "..." }
}
```

**Versioning**
- Prefer URL or header versioning: /v1/users or Accept: application/vnd.app.v1+json
- Breaking changes require new version; deprecate old with headers and docs

**Idempotency**
- For POST operations that can be retried: require Idempotency-Key header and deduplicate server-side

---

### Stage 3: Review Procedure
1) Identify touched resources and operations
2) Compare to existing contracts and clients
3) Run through the checklist; flag any breaking changes
4) Update OpenAPI and examples; add error cases
5) Decide on versioning or compatibility strategy

---

### Stage 4: Outputs
- API Review Notes (summary of decisions, risks, follow-ups)
- Updated OpenAPI spec and example payloads

---

### Stage 5: Links
- See also: design-patterns (API section), security-patterns, performance-patterns, code-quality-patterns

