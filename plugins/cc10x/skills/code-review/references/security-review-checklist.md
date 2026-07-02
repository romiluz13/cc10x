# Security Review Checklist

## Table of Contents
- [Quick Scan Commands](#quick-scan-commands)
- [Input And Output Boundaries](#input-and-output-boundaries)
- [Authentication And Authorization](#authentication-and-authorization)
- [Secrets And Sensitive Data](#secrets-and-sensitive-data)
- [Network And Request Safety](#network-and-request-safety)
- [Files, Storage, And Background Jobs](#files-storage-and-background-jobs)
- [Dependencies And Configuration](#dependencies-and-configuration)
- [Finding Format](#finding-format)

## Quick Scan Commands

Prefer tight searches over generic fear:

```bash
rg -n "(api[_-]?key|password|secret|token)\\s*[:=]" src test
rg -n "(eval\\(|innerHTML\\s*=|dangerouslySetInnerHTML)" src
rg -n "(query|exec)\\s*\\(" src
rg -n "console\\.log|print\\(" src
```

These are triage tools, not verdicts. Every hit still needs semantic review.

## Input And Output Boundaries

Check:
- user input validated at the boundary
- allowlists used where practical
- string lengths and numeric ranges constrained
- redirect URLs or callbacks validated
- output encoding preserved for HTML or rich text
- file types and sizes constrained before processing

Common real failures:
- SQL injection
- XSS
- open redirect
- path traversal

## Authentication And Authorization

Check:
- every protected route verifies identity
- every resource access verifies ownership or role
- admin flows actually require admin permissions
- tokens, sessions, or API keys are scoped and validated
- retries or background jobs do not bypass auth assumptions

Look especially at new endpoints, new service methods, and new queue consumers.

## Secrets And Sensitive Data

Check:
- no hardcoded credentials
- no secrets committed to config or examples
- logs do not emit tokens, passwords, or private payloads
- sensitive fields are excluded from API responses
- fallback values do not silently expose unsafe defaults

## Network And Request Safety

Check:
- outbound URLs are validated before fetches or webhooks
- CORS rules are explicit, not wildcard by default
- request timeouts and retry behavior are sane
- error payloads do not leak stack traces or internals in production

If a feature talks to external services, review SSRF and retry amplification risk.

## Files, Storage, And Background Jobs

Check:
- uploads are validated before storage or parsing
- storage paths cannot escape intended roots
- queued jobs validate payload shape before acting
- cached or persisted data does not outlive its trust assumptions

## Dependencies And Configuration

Check:
- new dependencies are necessary and maintained
- config defaults are safe in production
- debug flags or permissive dev behavior are not promoted to prod
- security headers or cookie settings are preserved where relevant

## Finding Format

Use concrete phrasing:

```markdown
- [CRITICAL] Missing authorization check at `path:line`
  - Risk: any authenticated user can access another tenant's data
  - Evidence: route reads `tenantId` from params without verifying ownership
  - Fix: enforce ownership or role check before query
```

If you cannot describe the exploit path and evidence, the finding is not ready.
