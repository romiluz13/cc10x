---
name: web-fetch-integration
description: Integrates WebFetch tool with functionality-first approach. Use PROACTIVELY when workflows need external documentation for functionality. First understands functionality requirements (user flow, admin flow, system flow, integration flow), then fetches external docs related to that functionality. Focuses on fetching functionality-related docs (API specs, integration constraints), not generic documentation. Loads web pages and PDFs from URLs for comprehensive context.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Web Fetch Integration - Functionality First

## Functionality First Mandate

**BEFORE fetching external docs, understand functionality**:

1. **What functionality needs external docs?**
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?
   - What are the integration flows?

2. **THEN fetch docs** - Fetch external docs related to that functionality

3. **Use patterns** - Apply web fetch patterns AFTER functionality is understood

---

## Purpose

Integrate Anthropic's Web Fetch Tool to load external documentation, API specifications, and reference materials into workflows with functionality-first approach. This enables workflows to access current external resources when needed for functionality.

---

## When to Use

**Use Web Fetch for** (Functionality-Focused):

- Loading external API documentation for functionality integration (REST APIs, SDKs, libraries)
- Fetching reference guides for functionality implementation (framework docs, language specs)
- Loading API specifications for functionality planning (OpenAPI/Swagger specs)
- Fetching external PDFs for functionality standards (standards, specifications, guides)
- Accessing current documentation for functionality (latest versions, updates)

**Use Cases by Workflow** (Functionality-Focused):

**Planning Workflow**:

- Load API specifications for functionality integration planning
- Fetch framework documentation for functionality architecture decisions
- Load external service documentation for functionality integration

**Build Workflow**:

- Load library documentation during functionality implementation
- Fetch SDK examples for functionality integration
- Load framework guides for functionality component building

**Review Workflow**:

- Fetch security best practices for functionality security checks
- Load coding standards for functionality quality checks
- Access external code quality guidelines for functionality review

**Debug Workflow**:

- Load error documentation for functionality debugging
- Fetch troubleshooting guides for functionality issues
- Access stack trace analysis resources for functionality bugs

---

## WebFetch Tool Usage (Claude Code)

**Availability**: ✅ WebFetch is available in Claude Code (built-in tool)

**CRITICAL: How Claude Code WebFetch Works**

Claude Code's WebFetch is **different** from the API version:

**API WebFetch** (beta, not in Claude Code):

- Returns full raw content (HTML/PDF)
- Single URL parameter

**Claude Code WebFetch** (built-in):

- **Requires BOTH `url` and `prompt` parameters**
- Returns **summarized answer**, NOT raw content
- Pipeline: Fetch → Convert to Markdown (max 100KB) → Haiku 3.5 summary → Answer

**Usage Pattern** (Functionality-Focused):

```bash
# WRONG (assumes raw content):
WebFetch(url="https://api.example.com/openapi.json")
→ Returns: Full JSON spec (THIS DOESN'T WORK IN CLAUDE CODE)

# CORRECT (functionality-focused prompt):
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What are all the API endpoint paths, HTTP methods, and required parameters for file upload functionality?"
)
→ Returns: "The API has POST /api/files/upload for file uploads, requires file parameter..."
```

**Key Constraints**:

- ❌ Cannot fetch raw API specs for parsing
- ❌ Cannot load full documentation pages
- ❌ Cannot cache raw HTML/JSON content
- ✅ Can ask specific functionality questions and get targeted answers
- ✅ Built-in 15-minute caching (server-side, automatic)
- ✅ Domain validation (blocks malicious domains)

**Best Practice** (Functionality-Focused):
Use multiple targeted functionality questions instead of expecting full content:

- Question 1: "What are all the API endpoints for file upload functionality?"
- Question 2: "What authentication method is required for file upload?"
- Question 3: "What are the data models for file upload and their fields?"

---

## Integration Points (Functionality-Focused)

### Planning Workflow

**Phase 1 - Requirements Intake** (Functionality-Focused):

- If external APIs mentioned for functionality, ask targeted questions:
  - "What are all the API endpoints and HTTP methods for [functionality]?"
  - "What authentication method is required for [functionality]?"
  - "What are the main data models for [functionality] and their fields?"
- If frameworks mentioned for functionality, ask:
  - "How do I set up and configure this framework for [functionality]?"
  - "What are the core concepts and patterns for [functionality]?"
  - "What are the integration requirements for [functionality]?"
- If external services mentioned for functionality, ask:
  - "What are the service capabilities and limitations for [functionality]?"
  - "How do I integrate with this service for [functionality]?"
  - "What are the pricing and rate limits for [functionality]?"

**Phase 2 - Architecture Design** (Functionality-Focused):

- Ask about functionality integration patterns: "What are best practices for integrating [service] with [framework] for [functionality]?"
- Ask about functionality architecture: "What architectural patterns are recommended for [functionality]?"
- Ask about functionality best practices: "What are the recommended approaches for [functionality scenario]?"

### Build Workflow (Functionality-Focused)

**Before Component Building**:

- If new library used for functionality, ask:
  - "How do I install and initialize this library for [functionality]?"
  - "What are the most common usage patterns and examples for [functionality]?"
  - "How do I handle errors and edge cases for [functionality]?"
- If SDK integration needed for functionality, ask:
  - "How do I set up the SDK for [functionality]?"
  - "What are the initialization patterns for [functionality]?"
  - "How do I make API calls with the SDK for [functionality]?"
- If framework guides needed for functionality, ask:
  - "How do I implement [functionality] in this framework?"
  - "What are the recommended patterns for [functionality task]?"

**During Integration** (Functionality-Focused):

- For external APIs, ask:
  - "How do I authenticate with this API for [functionality]?"
  - "What's the request/response format for [functionality]?"
  - "How do I handle errors from this API for [functionality]?"
- For integration guides, ask:
  - "How do I integrate [service] with [component] for [functionality]?"
  - "What are common integration pitfalls for [functionality]?"
- For troubleshooting, ask:
  - "What are common errors for [functionality] and how do I fix them?"
  - "How do I debug integration issues for [functionality]?"

### Review Workflow (Functionality-Focused)

**Security Review**:

- Ask: "What are the OWASP Top 10 security risks for [functionality] and how do I check for them?"
- Ask: "What security vulnerabilities should I look for in [functionality code type]?"
- Ask: "What are best practices for [functionality security concern]?"

**Performance Review**:

- Ask: "What performance optimization techniques apply to [functionality scenario]?"
- Ask: "How do I profile and identify bottlenecks in [functionality technology]?"
- Ask: "What are performance best practices for [functionality component]?"

### Debug Workflow (Functionality-Focused)

**During Investigation**:

- Ask: "What does this error [error code/message] mean for [functionality] and how do I fix it?"
- Ask: "How do I troubleshoot [functionality symptom] in [technology]?"
- Ask: "What are common causes of [functionality issue type] and their solutions?"

---

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

---

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
    },
    "What authentication is required for file upload functionality?": {
      "answer": "OAuth2 Bearer token...",
      "fetched_at": "2025-10-29T10:05:00Z",
      "ttl_hours": 24,
      "expires_at": "2025-10-30T10:05:00Z",
      "workflow_used": ["planning"],
      "functionality": "file_upload"
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

### Cache Index Format (Simplified)

```json
{
  "url_prompt_hash": {
    "url": "https://api.example.com/openapi.json",
    "prompt": "What are all the API endpoints for file upload functionality?",
    "answer_file": ".claude/memory/web_cache/qa_pairs/abc123_def456.json",
    "ttl_hours": 24,
    "last_fetched": "2025-10-29T10:00:00Z",
    "expires_at": "2025-10-30T10:00:00Z",
    "fetch_count": 2,
    "workflow_used": ["planning", "build"],
    "functionality": "file_upload"
  }
}
```

### Cache Cleanup

**Automatic Cleanup** (run weekly):

- Delete cached files if TTL expired >30 days
- Remove unused cache entries (>90 days unused)
- Keep cache_index.json clean

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

**Cache Corruption Handling**:

- **Detection**: Validate `cache_index.json` is valid JSON before use
- **Recovery**: If corrupted, attempt to rebuild from cache files
- **Fallback**: If rebuild fails, clear cache index and re-fetch
- **Validation**: Verify cached files exist before using (files may be deleted but index not updated)
- **Error Handling**: Log corruption events to `.claude/memory/web_cache/corruption.log` for debugging

---

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

## Cache Implementation

### Cache Check Function (Q&A Based)

```bash
#!/bin/bash
# Check cache before fetching URL with prompt
# Returns cached answer if available

check_cache() {
  local url="$1"
  local prompt="$2"
  local cache_index=".claude/memory/web_cache/cache_index.json"

  # Create hash from URL + prompt combination
  local query_hash=$(echo -n "${url}:${prompt}" | sha256sum | cut -d' ' -f1)

  # Validate cache_index.json exists and is valid JSON
  if [ ! -f "$cache_index" ]; then
    echo "CACHE_MISS"
    return 2
  fi

  # Validate JSON syntax (cache corruption detection)
  if ! jq empty "$cache_index" 2>/dev/null; then
    # Cache index corrupted - rebuild or clear
    echo "CACHE_CORRUPTED: Clearing cache_index.json" >&2
    rm -f "$cache_index"
    echo "CACHE_MISS"
    return 2
  fi

  # Check if query_hash exists in cache
  local cached_entry=$(jq -r ".[\"$query_hash\"] // empty" "$cache_index" 2>/dev/null)
  if [ -n "$cached_entry" ] && [ "$cached_entry" != "null" ]; then
    local expires=$(echo "$cached_entry" | jq -r '.expires_at // empty' 2>/dev/null)
    local answer_file=$(echo "$cached_entry" | jq -r '.answer_file // empty' 2>/dev/null)

    # Validate answer file exists
    if [ -z "$answer_file" ] || [ ! -f "$answer_file" ]; then
      # Answer file missing - remove from index
      jq "del(.[\"$query_hash\"])" "$cache_index" > "$cache_index.tmp" && mv "$cache_index.tmp" "$cache_index"
      echo "CACHE_MISS"
      return 2
    fi

    # Check if TTL valid
    local expires_ts=$(date -d "$expires" +%s 2>/dev/null)
    local now_ts=$(date +%s)
    if [ -n "$expires_ts" ] && [ "$expires_ts" -gt "$now_ts" ]; then
      # Return cached answer
      local answer=$(cat "$answer_file")
      echo "CACHE_HIT:$answer"
      return 0
    else
      echo "CACHE_EXPIRED:$answer_file"
      return 1
    fi
  fi

  echo "CACHE_MISS"
  return 2
}
```

### Cache Save Function (Q&A Based)

```bash
#!/bin/bash
# Save fetched answer to cache (Q&A pair)

save_to_cache() {
  local url="$1"
  local prompt="$2"
  local answer="$3"
  local ttl_hours="${4:-24}"  # Default 24 hours

  local cache_dir=".claude/memory/web_cache"
  local cache_index="$cache_dir/cache_index.json"

  mkdir -p "$cache_dir/qa_pairs"

  # Create hash from URL + prompt
  local query_hash=$(echo -n "${url}:${prompt}" | sha256sum | cut -d' ' -f1)
  local answer_file="$cache_dir/qa_pairs/${query_hash}.json"

  # Save answer to file
  echo "$answer" > "$answer_file"

  # Update cache index
  local expires_at=$(date -d "+$ttl_hours hours" -Iseconds)
  jq --arg hash "$query_hash" \
     --arg url "$url" \
     --arg prompt "$prompt" \
     --arg file "$answer_file" \
     --arg ttl "$ttl_hours" \
     --arg expires "$expires_at" \
     '.[$hash] = {
       "url": $url,
       "prompt": $prompt,
       "answer_file": $file,
       "ttl_hours": ($ttl | tonumber),
       "last_fetched": (now | strftime("%Y-%m-%dT%H:%M:%SZ")),
       "expires_at": $expires,
       "fetch_count": ((.[$hash].fetch_count // 0) + 1),
       "workflow_used": ((.[$hash].workflow_used // []) + [$ENV.WORKFLOW_NAME])
     }' "$cache_index" > "$cache_index.tmp" 2>/dev/null || echo "{}" > "$cache_index.tmp"
  mv "$cache_index.tmp" "$cache_index"
}
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

## Priority Classification

**Critical (Must Fetch)**:

- External API docs for functionality integration (blocks functionality)
- Framework docs for functionality implementation (blocks functionality)
- Service docs for functionality integration (blocks functionality)

**Important (Should Fetch)**:

- Standards for functionality review (affects functionality quality)
- Best practices for functionality (affects functionality quality)

**Minor (Can Defer)**:

- Generic documentation (if functionality docs are sufficient)
- Perfect documentation (if functionality works)

---

## When to Use

**Use PROACTIVELY when**:

- Planning functionality that needs external APIs
- Building functionality that needs external libraries
- Reviewing functionality against external standards
- Debugging functionality issues with external services

**Functionality-First Process**:

1. **First**: Understand functionality requirements (user flow, admin flow, system flow, integration flow)
2. **Then**: Fetch external docs related to that functionality
3. **Then**: Use fetched docs to support functionality
4. **Focus**: Fetch docs related to functionality, not generic docs

---

## Skill Overview

- **Skill**: Web Fetch Integration
- **Purpose**: Integrate WebFetch with functionality-first approach (not generic documentation fetching)
- **When**: Workflows need external documentation for functionality
- **Core Rule**: Functionality first, then fetch docs. Fetch functionality-related docs, not generic docs.

---

## References

- Anthropic Web Fetch Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-fetch-tool
- cc10x Workflows: `plugins/cc10x/skills/cc10x-orchestrator/workflows/`

---

**Remember**: External docs exist to support functionality. Don't fetch docs generically - fetch docs related to functionality!
