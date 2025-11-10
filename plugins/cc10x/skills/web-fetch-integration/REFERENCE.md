# Web Fetch Integration - Reference

Reference patterns, caching strategies, and examples for web fetch integration. Use AFTER understanding functionality (see SKILL.md).

## Web Fetch Patterns (Functionality-Focused)

### Pattern 1: API Specification Loading (Functionality-Focused)

```bash
# CORRECT: Ask targeted functionality questions about API
# Planning workflow - gather API information for functionality

# Question 1: Functionality endpoints
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What are all the API endpoint paths, HTTP methods, and their purposes for file upload functionality?"
)

# Question 2: Functionality authentication
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What authentication method is required for file upload functionality? How do I get an access token?"
)

# Question 3: Functionality data models
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What are the main data models for file upload functionality, their fields, types, and relationships?"
)

# Question 4: Functionality error handling
WebFetch(
  url="https://api.example.com/docs",
  prompt="What error codes does this API return for file upload functionality and what do they mean?"
)
```

### Pattern 2: Library Documentation Loading (Functionality-Focused)

```bash
# CORRECT: Ask specific functionality implementation questions
# Build workflow - get implementation guidance for functionality

# Question 1: Functionality getting started
WebFetch(
  url="https://docs.library.com/getting-started",
  prompt="How do I install and initialize this library for file upload functionality? What's the basic setup?"
)

# Question 2: Functionality common patterns
WebFetch(
  url="https://docs.library.com/patterns",
  prompt="What are the most common usage patterns and code examples for file upload functionality?"
)

# Question 3: Functionality integration
WebFetch(
  url="https://docs.library.com/integration",
  prompt="How do I integrate this library with [framework] for file upload functionality? What's the recommended approach?"
)
```

### Pattern 3: Standards and Guidelines (Functionality-Focused)

```bash
# CORRECT: Ask about specific functionality guidelines
# Review workflow - check against standards for functionality

WebFetch(
  url="https://owasp.org/www-project-top-ten/",
  prompt="What are the OWASP Top 10 security risks for file upload functionality and how do I check for them in code?"
)

WebFetch(
  url="https://example.com/coding-standards",
  prompt="What are the coding standards for error handling, naming conventions, and code structure for file upload functionality?"
)
```

## Smart Caching Strategy (Functionality-Focused Q&A Pair Caching)

**CRITICAL**: Claude Code WebFetch returns answers, not raw content. Cache Q&A pairs for functionality!

### Cache Structure (Functionality-Focused)

```
.claude/memory/web_cache/
├── qa_pairs/
│   ├── {url_hash}_{prompt_hash}.json
│   └── ...
└── cache_index.json (Maps {url, prompt} → cached functionality answer)
```

### Cache Entry Format (Functionality-Focused)

```json
{
  "https://api.example.com/openapi.json": {
    "What are all the API endpoints for file upload functionality?": {
      "answer": "The API has POST /api/files/upload for file uploads, requires file parameter...",
      "fetched_at": "2025-10-29T10:00:00Z",
      "ttl_hours": 24,
      "expires_at": "2025-10-30T10:00:00Z",
      "workflow_used": ["planning"],
      "functionality": "file_upload",
      "cache_file": ".claude/memory/web_cache/qa_pairs/abc123_def456.json"
    }
  }
}
```

### TTL Strategy (Functionality-Focused)

- **API Specifications**: 24 hours (APIs change frequently, functionality answers may become outdated)
- **Library Documentation**: 48 hours (version updates, functionality usage patterns change)
- **Framework Docs**: 48 hours (functionality examples and best practices evolve)
- **Standards/Guidelines**: 72 hours (even stable functionality content has updates)

**Rationale**: Since we cache answers (not raw content), shorter TTLs ensure functionality answers stay current. Answers summarize content at fetch time, so re-fetching with same prompt may yield updated functionality information.

### Smart Fetching Rules (Functionality-Focused Q&A Based)

**Cache-First Strategy**:

1. **Hash Query**: Create hash from `{url}_{prompt}` combination (functionality-focused)
2. **Check Cache Index**: Lookup hash in `cache_index.json`
3. **Validate TTL**: If cached and TTL valid → return cached functionality answer (no fetch)
4. **Expired Cache**: If cached but expired → re-fetch with same functionality prompt
5. **Not Cached**: If not cached → fetch with functionality prompt and cache answer
6. **Update Index**: Always update cache_index.json with new functionality Q&A pair

**Deduplication** (Functionality-Focused):

- Track `{url, prompt}` combinations fetched in current workflow
- Same functionality query in same workflow = use cached answer (already fetched)
- Different prompts on same URL = different cache entries (ask different functionality questions)

**Graceful Fallback**:

- If fetch fails → use cached functionality answer (even if expired)
- Log fetch failure for debugging
- Notify user if using stale functionality cache

**Prompt Consistency** (Functionality-Focused):

- Use same prompt wording for same functionality URL to maximize cache hits
- Standardize common functionality questions (e.g., "What are the API endpoints for [functionality]?")

## Best Practices

1. **Cache Aggressively**: Cache all external docs with appropriate TTL
2. **Check Cache First**: Always check cache_index.json before fetching
3. **Respect TTLs**: Re-fetch when expired, not before
4. **Deduplicate**: Prevent duplicate fetches in same workflow
5. **Fail Gracefully**: Use stale cache if fetch fails
6. **Extract Relevant Sections**: Only extract needed parts of fetched content
7. **Cite Sources**: Always cite external sources in workflow output
8. **Track Usage**: Log which workflows use which cached docs

## Error Handling

**If Web Fetch Fails**:

```python
try:
    docs = web_fetch(url=url, prompt=prompt)
except FetchError:
    # Fallback: Use local documentation or cached answer
    docs = read_local_docs(url) or get_cached_answer(url, prompt)
    log("Used local docs or cache, fetch failed")
```

**If URL Invalid**:

```python
if not is_valid_url(url):
    ask_user("Please provide valid URL for documentation")
    return None
```

## Examples

### Example 1: Planning with External API (Question-Based)

```bash
# Planning workflow - Phase 1
user_request = "Integrate with Stripe API for payment functionality"

# Question 1: Get all endpoints
endpoints = WebFetch(
  url="https://stripe.com/docs/api",
  prompt="What are all the API endpoint paths, HTTP methods, and their purposes for payment processing?"
)

# Question 2: Get authentication details
auth_info = WebFetch(
  url="https://stripe.com/docs/api/authentication",
  prompt="How do I authenticate requests for payment functionality? What API keys are needed and where do I get them?"
)

# Question 3: Get payment models
payment_models = WebFetch(
  url="https://stripe.com/docs/api/payment_intents",
  prompt="What are the PaymentIntent data model fields and their types for payment functionality? What are required vs optional fields?"
)

# Use answers in architecture design
design_api_integration(endpoints, auth_info, payment_models)
```

### Example 2: Build with Library Docs (Question-Based)

```bash
# Build workflow - Before component
library = "react-query"

# Question 1: Setup
setup_info = WebFetch(
  url="https://tanstack.com/query/latest/docs/react/overview",
  prompt="How do I install and set up react-query for data fetching functionality? What's the basic configuration?"
)

# Question 2: Common patterns
usage_patterns = WebFetch(
  url="https://tanstack.com/query/latest/docs/react/guides/queries",
  prompt="What are the most common query patterns and code examples for fetching data functionality?"
)

# Question 3: Mutations
mutations_info = WebFetch(
  url="https://tanstack.com/query/latest/docs/react/guides/mutations",
  prompt="How do I handle mutations for data updates? What's the pattern for POST/PUT/DELETE operations?"
)

# Use in implementation
implement_with_guidance(setup_info, usage_patterns, mutations_info)
```

### Example 3: Review with External Standards (Question-Based)

```bash
# Review workflow - Security review
security_guidelines = WebFetch(
  url="https://owasp.org/www-project-top-ten/",
  prompt="What are the OWASP Top 10 security risks for 2021? How do I check for injection attacks, broken authentication, and sensitive data exposure in code?"
)

# Use in security analysis
analyze_with_owasp(security_guidelines)
```

## Verification Checklist (Q&A Based)

**Before Fetching**:

- [ ] Create hash from `{url}_{prompt}` combination
- [ ] Check `cache_index.json` for query hash
- [ ] If cached and TTL valid → use cached answer (skip fetch)
- [ ] If cached but expired → mark for re-fetch with same prompt
- [ ] If not cached → proceed with fetch using prompt
- [ ] Verify URL is valid and accessible
- [ ] Verify prompt is specific and clear

**After Fetching**:

- [ ] Save answer (not raw content) to cache with appropriate TTL
- [ ] Update cache_index.json with Q&A pair entry
- [ ] Validate answer is relevant to prompt
- [ ] Use consistent prompt wording for same questions
- [ ] Cite source URL in workflow output
- [ ] Track which workflow used this cache entry

**On Fetch Failure**:

- [ ] Check for stale cached answer (even if expired)
- [ ] Use stale answer if available
- [ ] Log failure for debugging
- [ ] Notify user if using stale cache
- [ ] Consider alternative phrasing of prompt
