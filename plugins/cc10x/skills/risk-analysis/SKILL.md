---
name: risk-analysis
description: Universal "What Could Go Wrong?" critical thinking framework for pre-implementation audits. 7-dimensional analysis covering data flow transformations, dependency integration mapping, timing concurrency state management, user experience human factors, security validation, performance scalability, and failure modes recovery. Prevents bugs before they're written by systematically identifying edge cases. Use when analyzing feature designs for risks, reviewing code for vulnerabilities, planning deployments for failure scenarios, debugging complex issues for root causes, or validating implementations for edge cases. Particularly valuable before implementing high-risk features (authentication, payment processing, data handling) or when edge cases need systematic identification. Loaded progressively by master orchestrator in 7 stages, or explicitly invoked for specific dimension analysis.
license: MIT
---

# Risk Analysis - "What Could Go Wrong?" Methodology

**Core Philosophy:** "Every change is guilty until proven innocent"

Assume everything can fail. Find edge cases before production does.

---

## Progressive Loading Stages

**Focus:** Input validation, data transformations, output handling

**Critical Questions:**

**Input Sources:**
- Where does data originate? (user, API, database, file, cache, queue)
- What format? (JSON, XML, binary, form data, CSV, stream)
- Who controls input? (trusted internal vs untrusted external)
- Can input be manipulated before reaching code?

**Transformations:**
- How many transformation steps?
- Can intermediate states be invalid?
- Are transformations reversible or lossy?
- What happens at each transformation step?

**Output Destinations:**
- Where does data go? (UI, database, API, file, log, queue)
- What format expected by destination?
- What happens if destination unavailable?
- Can output be intercepted or tampered with?

**Edge Cases to Test:**
- **Missing:** null, undefined, None, empty string, empty array, missing keys
- **Wrong Type:** String when expecting number, object when expecting array
- **Wrong Format:** Invalid dates (2025-13-45), malformed JSON, corrupted binary
- **Extreme Values:** 0, negative numbers, MAX_INT, Infinity, NaN, huge strings (>10MB)
- **Special Characters:** SQL injection (`'; DROP TABLE--`), XSS (`<script>`), Unicode, emojis, null bytes

**Output Format:**
```markdown
### Data Flow Risks

#### CRITICAL:
- [Issue]: Input not validated for SQL injection
  - Location: users.controller.js line 45
  - Trigger: User submits `'; DROP TABLE users;--` in search field
  - Impact: Database compromise, complete data loss
  - Probability: HIGH (exposed public API endpoint)
  - Fix: Use parameterized queries: `db.query('SELECT * FROM users WHERE name = ?', [searchTerm])`

#### MODERATE:
- [Issue]: Missing data not handled
  - Location: profile.jsx line 23
  - Trigger: User record has null email in database
  - Impact: UI crashes, React error boundary triggered
  - Probability: MEDIUM (10% of users have no email)
  - Fix: Add null check: `email || 'No email provided'`

#### LOW:
- [Issue]: Large input not size-limited
  - Location: upload.handler.js line 12
  - Trigger: User uploads 500MB file
  - Impact: Server memory exhaustion
  - Probability: LOW (rarely happens)
  - Fix: Add size limit: `if (file.size > 10MB) reject()`
```

---

**Focus:** What this code depends on, what depends on this code

**Critical Questions:**

**Direct Dependencies:**
- What functions/modules/classes are called by this code?
- What libraries/packages are required?
- What external services are integrated? (APIs, databases, file systems)
- What versions are specified?

**Reverse Dependencies:**
- What other code calls THIS function/module/class?
- If I change this interface, what breaks?
- Are there duplicate implementations elsewhere that need syncing?
- Is this a shared utility or single-use?

**Shared State:**
- What global variables/singletons/caches are accessed?
- What database tables/collections are touched?
- What files/locks/resources are shared?
- What environment variables are read?

**Integration Points:**
- Is there a single source of truth, or is logic duplicated?
- Are there circular dependencies?
- What happens if a dependency is temporarily unavailable?
- Are dependency versions pinned or can they auto-update?

**Output Format:**
```markdown
### Dependency Risks

#### CRITICAL:
- [Issue]: Circular dependency detected
  - Location: auth.js imports users.js, users.js imports auth.js
  - Trigger: Module load order becomes critical
  - Impact: Application fails to start intermittently (race condition)
  - Probability: HIGH (happens 20% of deployments)
  - Fix: Extract shared code to utils/auth-helpers.js

#### MODERATE:
- [Issue]: Unpinned dependency version
  - Location: package.json - express: ^4.0.0 (allows 4.x updates)
  - Trigger: Express 5.0 releases with breaking changes
  - Impact: Auto-update breaks all API routes, production down
  - Probability: MEDIUM (express 5.0 coming soon)
  - Fix: Pin to exact version: "express": "4.18.2"

#### LOW:
- [Issue]: Duplicate validation logic
  - Location: client-validation.js and server-validation.js
  - Trigger: Update one but not the other
  - Impact: Client allows invalid input, server rejects inconsistently
  - Probability: MEDIUM (happened twice already)
  - Fix: Extract to shared validation schema (Zod/Yup)
```

---

**Focus:** Race conditions, state transitions, execution order

**Critical Questions:**

**Execution Order:**
- What if this runs BEFORE initialization complete?
- What if this runs AFTER cleanup/shutdown started?
- What if this runs DURING another critical operation?
- Can this be called multiple times simultaneously?

**Race Conditions:**
- Can two instances modify the same data concurrently?
- What if async operations complete out of order?
- Are there any "check-then-act" patterns (TOCTOU bugs)?
- Is there proper locking/synchronization?
- Are atomic operations used where needed?

**State Management:**
- What's the expected initial state?
- Can the state become invalid mid-operation?
- What happens if state is rolled back (transaction aborts)?
- Is state persisted correctly across restarts?
- Are state transitions validated?

**Critical Scenarios:**
- User clicks "submit" button twice rapidly (double-submit)
- Network request succeeds but response never arrives (timeout)
- Process crashes mid-transaction (data consistency)
- Cache invalidation happens during read (stale data served)
- System clock changes (DST switch, timezone change, NTP sync)

**Output Format:**
```markdown
### Timing & Concurrency Risks

#### CRITICAL:
- [Issue]: Race condition on payment processing
  - Location: checkout.service.js lines 45-67
  - Trigger: User clicks "Pay Now" twice within 200ms
  - Impact: Double charge to credit card, duplicate orders created
  - Probability: MEDIUM (happens ~10x/month with 10k users)
  - Fix: Add idempotency key, check order.status === 'pending' before processing

#### HIGH:
- [Issue]: State not persisted before process crash
  - Location: file-upload.service.js line 89
  - Trigger: Server restart/crash during 30-second upload
  - Impact: Partial file upload, corrupted file, no user notification
  - Probability: LOW but HIGH impact (data loss)
  - Fix: Write to temp file first, rename atomically, send success notification

#### MODERATE:
- [Issue]: Check-then-act race condition (TOCTOU)
  - Location: auth.middleware.js lines 34-38
  - Trigger: Check user.isActive, user gets deactivated, then proceed
  - Impact: Deactivated user can complete action for ~100ms window
  - Probability: LOW (small time window)
  - Fix: Use transaction with row lock: `SELECT ... FOR UPDATE`
```

---

**Focus:** How real users interact, accessibility, internationalization

**Critical Questions:**

**User Expectations:**
- What does the user SEE when this operation happens?
- What feedback does user get if it fails? (error message quality)
- How long do they wait before assuming it's broken?
- What happens if they navigate away mid-operation?
- Can they retry? Undo? Cancel?

**Accessibility:**
- Does this work with screen readers? (ARIA labels, semantic HTML)
- Can keyboard-only users operate this? (tab navigation, shortcuts)
- Is color the only indicator of state? (colorblind users)
- Are error messages understandable to non-technical users?
- Does this meet WCAG 2.1 AA standards?

**Internationalization:**
- Does this work in different languages/locales?
- Are dates/times handled correctly across timezones?
- Are numbers formatted correctly? (1,000.00 vs 1.000,00)
- Does text directionality work? (RTL languages like Arabic/Hebrew)
- Are string concatenations locale-safe?

**Device/Environment Variations:**
- Does this work on mobile? Tablet? Desktop?
- Does this work on slow 3G connections?
- Does this work offline (with service worker)?
- Does this work on older browsers/OS versions?
- Does this work with browser extensions (ad blockers)?

**Output Format:**
```markdown
### UX & Accessibility Risks

#### MODERATE:
- [Issue]: No loading indicator for slow operation
  - Location: dashboard.component.jsx line 34
  - Trigger: API request takes >3 seconds on slow connection
  - Impact: User thinks page is broken, clicks button again, duplicate requests
  - Probability: HIGH (30% of users on mobile)
  - Fix: Show spinner immediately, disable button during request

#### MODERATE:
- [Issue]: Error message too technical
  - Location: api.error.handler.js line 23
  - Trigger: Database connection fails
  - Impact: User sees "ECONNREFUSED 127.0.0.1:5432" and panics
  - Probability: LOW but confusing when happens
  - Fix: Show user-friendly: "Service temporarily unavailable. We're working on it."

#### LOW:
- [Issue]: Color-only status indicator
  - Location: order-status.jsx line 15
  - Trigger: Colorblind user can't distinguish red/green
  - Impact: User can't tell if order succeeded or failed
  - Probability: MEDIUM (8% of males are colorblind)
  - Fix: Add icons: ✓ (success) and ✕ (failure) plus color

#### LOW:
- [Issue]: No keyboard navigation support
  - Location: custom-dropdown.jsx
  - Trigger: Keyboard-only user tries to use dropdown
  - Impact: Feature completely unusable without mouse
  - Probability: LOW (<1% keyboard-only users)
  - Fix: Add onKeyDown handlers for Enter/Escape/Arrow keys
```

---

**Focus:** Authentication, authorization, injection attacks, data exposure

**Critical Questions:**

**Authentication & Authorization:**
- Who can trigger this operation? (anonymous, authenticated, admin)
- Is this protected by authentication middleware?
- Is this authorized per user/role? (fine-grained permissions)
- Can authorization be bypassed? (direct API calls, URL manipulation)
- Are sessions/tokens validated on every request?

**Input Validation:**
- Is input validated on BOTH client AND server?
- Can validation be bypassed via direct API calls? (skip client validation)
- Are there regex/parsing vulnerabilities? (ReDoS, parser exploits)
- Is there a whitelist of allowed values?
- Are file uploads restricted? (type, size, content)

**Injection Attacks:**
- **SQL Injection:** Are queries parameterized? (`?` placeholders)
- **XSS:** Is user input escaped before HTML output? (`<script>` tags)
- **Command Injection:** Are shell commands avoided? (`exec()` with user input)
- **Path Traversal:** Are file paths validated? (`../../../etc/passwd`)
- **NoSQL Injection:** Are MongoDB queries sanitized? (`$where`, `$regex`)
- **LDAP/XML/CSV Injection:** Are special characters escaped?

**Data Exposure:**
- Is sensitive data logged? (passwords, tokens, credit cards)
- Is sensitive data in error messages? (stack traces with secrets)
- Is sensitive data in URLs? (tokens in query params)
- Is sensitive data in browser cache/localStorage?
- Do API responses over-share data? (return all user fields)

**Common Vulnerabilities:**
- **CSRF:** Are state-changing operations protected? (CSRF tokens)
- **Insecure Direct Object References:** Can users access other users' data? (`/api/users/123`)
- **Unvalidated Redirects:** Can redirect be manipulated? (`?redirect=evil.com`)
- **Broken Access Control:** Are admin functions truly restricted?
- **Security Misconfiguration:** Are defaults secure? (debug mode off)

**Output Format:**
```markdown
### Security Risks

#### CRITICAL:
- [Issue]: SQL Injection vulnerability
  - Location: search.controller.js line 67: `db.query('SELECT * FROM products WHERE name = ' + searchTerm)`
  - Trigger: User searches for `'; DROP TABLE users;--`
  - Impact: Complete database compromise, all data lost or stolen
  - Probability: HIGH (exposed public API, easily exploitable)
  - Fix: Use parameterized queries: `db.query('SELECT * FROM products WHERE name = ?', [searchTerm])`

#### CRITICAL:
- [Issue]: Authentication bypass via direct API call
  - Location: admin.routes.js - no auth middleware on `/api/admin/users`
  - Trigger: Unauthenticated user directly calls API endpoint
  - Impact: Anonymous users can access all admin functions
  - Probability: HIGH (discovered in security audit)
  - Fix: Add auth middleware: `router.use('/api/admin', requireAdmin)`

#### HIGH:
- [Issue]: Sensitive data in logs
  - Location: auth.middleware.js line 34: `logger.error('Login failed', { email, password })`
  - Trigger: Every failed login attempt
  - Impact: Passwords stored in plain text logs, compliance violation
  - Probability: HIGH (happens constantly)
  - Fix: Redact password: `logger.error('Login failed', { email })`

#### HIGH:
- [Issue]: XSS vulnerability in user-generated content
  - Location: comment.component.jsx line 45: `<div dangerouslySetInnerHTML={{__html: comment.text}} />`
  - Trigger: User posts comment with `<script>alert('XSS')</script>`
  - Impact: Malicious script runs in other users' browsers, session hijacking
  - Probability: MEDIUM (requires user to post malicious content)
  - Fix: Sanitize HTML: use DOMPurify library or render as plain text

#### MODERATE:
- [Issue]: Insecure direct object reference
  - Location: orders.controller.js line 23: `/api/orders/:id` returns order without checking ownership
  - Trigger: User changes URL from `/orders/123` to `/orders/124`
  - Impact: Users can view other users' orders (PII exposure)
  - Probability: HIGH (easy to test different IDs)
  - Fix: Check ownership: `if (order.userId !== req.user.id) return 403`
```

---

**Focus:** Computational complexity, resource usage, caching

**Critical Questions:**

**Computational Complexity:**
- What's the Big O complexity? (O(n), O(n²), O(n log n))
- Are there nested loops over large datasets?
- Are there recursive calls without depth limits? (stack overflow risk)
- Is there unnecessary repeated computation? (could be cached/memoized)

**Data Volume:**
- Does this work with 0 items? (empty array/list)
- Does this work with 1 item? (edge case)
- Does this work with 1,000 items? (typical case)
- Does this work with 1,000,000 items? (scale case)
- What if a single item is huge? (10MB string, 5MB JSON object)
- Is pagination/streaming implemented for large datasets?

**Resource Usage:**
- **Memory:** Can this cause memory leaks? (event listeners not removed, closures holding refs)
- **CPU:** Can this block the main thread? (long synchronous operations)
- **Network:** How much bandwidth does this consume? (large payloads, polling frequency)
- **Disk:** Can this fill up disk space? (log files, temp files, uploads)
- **Connections:** Are database/API connections pooled and released?

**Caching & Optimization:**
- Is this result cacheable? (deterministic, no side effects)
- Can this be memoized? (pure function, called repeatedly with same input)
- Should this be debounced/throttled? (rapid repeated calls)
- Are expensive operations done lazily? (compute only when needed)
- Is there unnecessary re-rendering/re-computation?

**Output Format:**
```markdown
### Performance Risks

#### HIGH:
- [Issue]: O(n²) complexity on large dataset
  - Location: reports.service.js lines 45-52 (nested loops over users and orders)
  - Trigger: Admin exports full user report (10,000 users × 50 orders each)
  - Impact: Server timeout after 30+ seconds, request fails
  - Probability: MEDIUM (admins export reports monthly)
  - Fix: Optimize with SQL JOIN + index: reduce to O(n log n), 2 seconds

#### HIGH:
- [Issue]: Memory leak from unclosed database connections
  - Location: database.service.js line 89 - connection opened but never closed
  - Trigger: Long-running batch job (runs overnight for 6 hours)
  - Impact: Server crashes after 4-6 hours, job fails
  - Probability: HIGH (happens every week)
  - Fix: Add connection.close() in finally block, or use connection pool

#### MODERATE:
- [Issue]: No pagination on large list
  - Location: products.api.js line 34 - returns ALL products
  - Trigger: Catalog grows to 50,000 products
  - Impact: 20MB response, slow page load, browser hangs
  - Probability: MEDIUM (catalog growing by 1000/month)
  - Fix: Add pagination: limit 50, offset for pages

#### MODERATE:
- [Issue]: Expensive computation not cached
  - Location: dashboard.component.jsx - recalculates stats on every render
  - Trigger: User changes any dashboard filter (re-renders component)
  - Impact: UI feels sluggish, calculation takes 500ms each time
  - Probability: HIGH (users adjust filters frequently)
  - Fix: Use useMemo hook to cache calculation results

#### LOW:
- [Issue]: Blocking synchronous operation
  - Location: image-processor.js line 67 - synchronous image resize
  - Trigger: User uploads 10 images at once
  - Impact: Main thread blocked for 3 seconds, UI freezes
  - Probability: LOW (most users upload 1-2 images)
  - Fix: Use async/await with worker threads or queue
```

---

**Focus:** What can fail, error handling, graceful degradation, rollback

**Critical Questions:**

**What Can Fail:**
- **Network Requests:** Timeout, DNS failure, SSL certificate error, connection refused
- **Database Operations:** Connection lost, deadlock, constraint violation, query timeout
- **File Operations:** Permission denied, disk full, file locked by another process
- **External APIs:** Rate limited, deprecated, changed response format, service down
- **Third-Party Services:** AWS outage, Stripe downtime, CDN issues, regional failures

**Error Handling:**
- Are ALL errors caught? (try/catch, error boundaries, .catch())
- Are errors logged with sufficient context? (stack trace, request ID, user ID)
- Are error messages user-friendly? (not technical jargon)
- Can errors leak sensitive information? (stack traces with passwords)
- Is there a circuit breaker for cascading failures? (stop calling failing service)

**Graceful Degradation:**
- Can the system operate in read-only mode? (database writes fail)
- Can it fall back to cached data? (API unavailable)
- Can it queue operations for retry? (email service down)
- Can it skip non-critical features? (analytics fails, continue anyway)

**Recovery & Rollback:**
- Can partial failures be rolled back? (transaction semantics)
- Is there a way to manually retry? (admin panel, background job)
- Are idempotent operations guaranteed? (safe to retry without duplicates)
- Is there data backup/restore capability? (point-in-time recovery)

**Output Format:**
```markdown
### Failure Mode Risks

#### CRITICAL:
- [Issue]: No rollback on partial payment failure
  - Location: checkout.service.js lines 89-120
  - Trigger: Stripe charge succeeds, but order.save() fails (database error)
  - Impact: Customer charged but no order created, requires manual refund
  - Probability: LOW but CRITICAL impact (financial, legal)
  - Fix: Use two-phase commit pattern or Stripe's idempotency keys + retry logic

#### HIGH:
- [Issue]: No error handling for external API failure
  - Location: shipping.service.js line 45: `const rate = await shippingAPI.getRate()`
  - Trigger: Shipping API returns 500 error or times out
  - Impact: Order stuck in "processing" forever, no user notification
  - Probability: MEDIUM (API has 99.5% uptime = 43 minutes downtime/month)
  - Fix: Add try/catch, fallback to manual processing queue, notify user

#### HIGH:
- [Issue]: Database connection not released on error
  - Location: users.repository.js line 67 - connection acquired but not released in catch block
  - Trigger: Query throws error (malformed SQL, constraint violation)
  - Impact: Connection pool exhausted after 10 errors, all requests fail
  - Probability: MEDIUM (errors happen regularly)
  - Fix: Use try/finally or connection.release() in catch block

#### MODERATE:
- [Issue]: No circuit breaker for failing dependency
  - Location: recommendations.service.js - calls ML API on every request
  - Trigger: ML API is down, every request waits 30s for timeout
  - Impact: Entire site slows down, cascading failure
  - Probability: LOW (ML API usually reliable)
  - Fix: Implement circuit breaker pattern (stop calling after 3 failures, fallback to defaults)

#### MODERATE:
- [Issue]: File upload not cleaned up on error
  - Location: upload.handler.js line 89 - temp files created but not deleted if processing fails
  - Trigger: User uploads file, processing throws error
  - Impact: Disk fills up with orphaned temp files over time
  - Probability: MEDIUM (processing fails 5% of the time)
  - Fix: Add cleanup in finally block: `fs.unlink(tempFile)`

#### LOW:
- [Issue]: No retry mechanism for transient failures
  - Location: email.service.js - single attempt to send email
  - Trigger: Email service temporarily unavailable (network blip)
  - Impact: Important emails (password reset, order confirmation) not sent
  - Probability: LOW (service usually reliable)
  - Fix: Add exponential backoff retry (3 attempts with 1s, 2s, 4s delays)
```

---

## Invocation Methods

### Method 1: Explicit Invocation by Sub-Agents (Primary)

**When to use:** During planning, implementation, review phases

**How it works:**
- Sub-agents invoke specific stages based on phase
- Progressive loading: Only load relevant dimensions
- Token-efficient: Load only what's needed

**Examples:**

**Architect during planning (Phase 3):**
```
Invoke Skill: "cc10x:risk-analysis"
Stage: "Stage 1: Data Flow" + "Stage 5: Security"
Purpose: Identify data flow risks and security vulnerabilities early in design
```

**Implementer before coding increment:**
```
Invoke Skill: "cc10x:risk-analysis"
Stage: "Stage 3: Timing" + "Stage 7: Failure Modes"
Purpose: Consider concurrency issues and error handling before implementation
```

**Quality Reviewer during comprehensive review:**
```
Invoke Skill: "cc10x:risk-analysis"
Stage: ALL 7 stages
Purpose: Complete "what could go wrong?" analysis before deployment
```

**Security Reviewer (deep dive):**
```
Invoke Skill: "cc10x:risk-analysis"
Stage: "Stage 5: Security" (full deep dive)
Purpose: Comprehensive security vulnerability analysis
```

**DevOps Planner during deployment planning:**
```
Invoke Skill: "cc10x:risk-analysis"
Stage: "Stage 7: Failure Modes"
Purpose: Identify what can fail in production, plan rollback triggers
```

### Method 2: Manual Invocation by User

**When to use:** User wants explicit risk analysis

**Examples:**
```
User: "Use risk-analysis skill to analyze this payment processing code"
User: "Run what could go wrong analysis on my authentication system"
User: "Check for edge cases in this data transformation function"
```

### Method 3: Auto-Trigger (NOT WORKING)

**Status:** ⚠️ Skills don't currently auto-trigger in Claude Code

**Evidence:**
- Trigger phrases listed for future compatibility
- Extensive testing shows 0% auto-trigger rate
- Don't rely on auto-triggering

**Workaround:** Use commands (they explicitly invoke skills) or manual invocation

---

## When to Use This Skill

### Use for EVERY:
- Feature implementation (before coding)
- Code review (before merging)
- Architecture decision (before committing)
- Production deployment (before releasing)
- Bug fix (to ensure it doesn't introduce new bugs)

### Especially Critical For:
- Payment processing (financial risk)
- Authentication/authorization (security risk)
- Data migrations (data loss risk)
- External API integrations (availability risk)
- User-generated content (security/UX risk)

### Load Specific Stages When:
- **Stage 1:** Working with user input, APIs, databases
- **Stage 2:** Adding dependencies, changing interfaces
- **Stage 3:** Dealing with async code, state management
- **Stage 4:** Building user-facing features
- **Stage 5:** Handling sensitive data, auth, permissions
- **Stage 6:** Processing large datasets, expensive operations
- **Stage 7:** Integrating external services, critical operations

---

## Red Flags (Use This Skill Immediately)

If you catch yourself saying:
- ❌ "This will never happen in practice"
- ❌ "Users would never do that"
- ❌ "The documentation says it should work"
- ❌ "We can fix it later if it's a problem"
- ❌ "It's just a quick fix, we don't need to think about edge cases"

**STOP.** These are danger signs. Load this skill and do proper analysis.

---

## Success Metrics

**You're using this skill correctly when:**
- ✅ You find bugs during design/review, not production
- ✅ Your deployments succeed without rollbacks
- ✅ You proactively prevent issues
- ✅ Code reviews catch critical issues early
- ✅ Production incidents decrease over time

**You're NOT using it correctly when:**
- ❌ Still discovering bugs in production
- ❌ Frequent emergency rollbacks
- ❌ Saying "we didn't think about that"
- ❌ Treating this as a checkbox exercise
- ❌ Only using it for big changes (use for ALL changes)

---

## Remember

**Every assumption is a potential bug.**
**Every "obvious" logic has a non-obvious edge case.**
**Every "this will never happen" already happened in production somewhere.**

**Think like:**
- An attacker trying to break your system
- A confused user doing the unexpected
- Murphy's Law: "Anything that can go wrong, will go wrong"

**The goal:** Transform "Let's ship it and see" into "We've thought through every scenario and we're confident this is production-ready."
