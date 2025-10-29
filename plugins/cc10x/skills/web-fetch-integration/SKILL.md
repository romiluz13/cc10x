---
name: web-fetch-integration
description: Integrates WebFetch tool (available in Claude Code) for loading external documentation, API specifications, and reference materials. Use when workflows need external documentation, API specs, reference guides, or external resources to complete tasks. Loads web pages and PDFs from URLs for comprehensive context.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Web Fetch Integration

## Purpose

Integrate Anthropic's Web Fetch Tool to load external documentation, API specifications, and reference materials into workflows. This enables workflows to access current external resources when needed.

## When to Use

**Use Web Fetch for**:
- Loading external API documentation (REST APIs, SDKs, libraries)
- Fetching reference guides (framework docs, language specs)
- Loading API specifications (OpenAPI/Swagger specs)
- Fetching external PDFs (standards, specifications, guides)
- Accessing current documentation (latest versions, updates)

**Use Cases by Workflow**:

**Planning Workflow**:
- Load API specifications for integration planning
- Fetch framework documentation for architecture decisions
- Load external service documentation

**Build Workflow**:
- Load library documentation during implementation
- Fetch SDK examples for integration
- Load framework guides for component building

**Review Workflow**:
- Fetch security best practices from external sources
- Load coding standards from team docs
- Access external code quality guidelines

**Debug Workflow**:
- Load error documentation from external sources
- Fetch troubleshooting guides
- Access stack trace analysis resources

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

**Usage Pattern**:
```bash
# WRONG (assumes raw content):
WebFetch(url="https://api.example.com/openapi.json")
→ Returns: Full JSON spec (THIS DOESN'T WORK IN CLAUDE CODE)

# CORRECT (prompt-based):
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What are all the API endpoint paths, HTTP methods, and required parameters?"
)
→ Returns: "The API has the following endpoints: POST /auth/login requires username and password, GET /users/{id} returns user details..."
```

**Key Constraints**:
- ❌ Cannot fetch raw API specs for parsing
- ❌ Cannot load full documentation pages  
- ❌ Cannot cache raw HTML/JSON content
- ✅ Can ask specific questions and get targeted answers
- ✅ Built-in 15-minute caching (server-side, automatic)
- ✅ Domain validation (blocks malicious domains)

**Best Practice**:
Use multiple targeted questions instead of expecting full content:
- Question 1: "What are all the API endpoints?"
- Question 2: "What authentication method is required?"
- Question 3: "What are the data models and their fields?"

## Integration Points

### Planning Workflow

**Phase 1 - Requirements Intake**:
- If external APIs mentioned, ask targeted questions:
  - "What are all the API endpoints and HTTP methods?"
  - "What authentication method is required?"
  - "What are the main data models and their fields?"
- If frameworks mentioned, ask:
  - "How do I set up and configure this framework?"
  - "What are the core concepts and patterns?"
  - "What are the integration requirements?"
- If external services mentioned, ask:
  - "What are the service capabilities and limitations?"
  - "How do I integrate with this service?"
  - "What are the pricing and rate limits?"

**Phase 2 - Architecture Design**:
- Ask about integration patterns: "What are best practices for integrating [service] with [framework]?"
- Ask about architecture: "What architectural patterns are recommended for [use case]?"
- Ask about best practices: "What are the recommended approaches for [scenario]?"

### Build Workflow

**Before Component Building**:
- If new library used, ask:
  - "How do I install and initialize this library?"
  - "What are the most common usage patterns and examples?"
  - "How do I handle errors and edge cases?"
- If SDK integration needed, ask:
  - "How do I set up the SDK?"
  - "What are the initialization patterns?"
  - "How do I make API calls with the SDK?"
- If framework guides needed, ask:
  - "How do I implement [feature] in this framework?"
  - "What are the recommended patterns for [task]?"

**During Integration**:
- For external APIs, ask:
  - "How do I authenticate with this API?"
  - "What's the request/response format?"
  - "How do I handle errors from this API?"
- For integration guides, ask:
  - "How do I integrate [service] with [component]?"
  - "What are common integration pitfalls?"
- For troubleshooting, ask:
  - "What are common errors and how do I fix them?"
  - "How do I debug integration issues?"

### Review Workflow

**Security Review**:
- Ask: "What are the OWASP Top 10 security risks and how do I check for them?"
- Ask: "What security vulnerabilities should I look for in [code type]?"
- Ask: "What are best practices for [security concern]?"

**Performance Review**:
- Ask: "What performance optimization techniques apply to [scenario]?"
- Ask: "How do I profile and identify bottlenecks in [technology]?"
- Ask: "What are performance best practices for [component]?"

### Debug Workflow

**During Investigation**:
- Ask: "What does this error [error code/message] mean and how do I fix it?"
- Ask: "How do I troubleshoot [symptom] in [technology]?"
- Ask: "What are common causes of [issue type] and their solutions?"

## Web Fetch Patterns (Claude Code)

### Pattern 1: API Specification Loading (Question-Based)

```bash
# CORRECT: Ask targeted questions about API
# Planning workflow - gather API information

# Question 1: Endpoints
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What are all the API endpoint paths, HTTP methods, and their purposes?"
)

# Question 2: Authentication
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What authentication method is required? How do I get an access token?"
)

# Question 3: Data Models
WebFetch(
  url="https://api.example.com/openapi.json",
  prompt="What are the main data models, their fields, types, and relationships?"
)

# Question 4: Error Handling
WebFetch(
  url="https://api.example.com/docs",
  prompt="What error codes does this API return and what do they mean?"
)
```

### Pattern 2: Library Documentation Loading

```bash
# CORRECT: Ask specific implementation questions
# Build workflow - get implementation guidance

# Question 1: Getting Started
WebFetch(
  url="https://docs.library.com/getting-started",
  prompt="How do I install and initialize this library? What's the basic setup?"
)

# Question 2: Common Patterns
WebFetch(
  url="https://docs.library.com/patterns",
  prompt="What are the most common usage patterns and code examples?"
)

# Question 3: Integration
WebFetch(
  url="https://docs.library.com/integration",
  prompt="How do I integrate this library with [framework]? What's the recommended approach?"
)
```

### Pattern 3: Standards and Guidelines

```bash
# CORRECT: Ask about specific guidelines
# Review workflow - check against standards

WebFetch(
  url="https://owasp.org/www-project-top-ten/",
  prompt="What are the OWASP Top 10 security risks and how do I check for them in code?"
)

WebFetch(
  url="https://example.com/coding-standards",
  prompt="What are the coding standards for error handling, naming conventions, and code structure?"
)
```

## Smart Caching Strategy (Q&A Pair Caching)

**CRITICAL**: Claude Code WebFetch returns answers, not raw content. Cache Q&A pairs!

### Cache Structure

```
.claude/memory/web_cache/
├── qa_pairs/
│   ├── {url_hash}_{prompt_hash}.json
│   └── ...
└── cache_index.json (Maps {url, prompt} → cached answer)
```

### Cache Entry Format

```json
{
  "https://api.example.com/openapi.json": {
    "What are all the API endpoints?": {
      "answer": "The API has POST /auth/login, GET /users/{id}...",
      "fetched_at": "2025-10-29T10:00:00Z",
      "ttl_hours": 24,
      "expires_at": "2025-10-30T10:00:00Z",
      "workflow_used": ["planning"],
      "cache_file": ".claude/memory/web_cache/qa_pairs/abc123_def456.json"
    },
    "What authentication is required?": {
      "answer": "OAuth2 Bearer token...",
      "fetched_at": "2025-10-29T10:05:00Z",
      "ttl_hours": 24,
      "expires_at": "2025-10-30T10:05:00Z",
      "workflow_used": ["planning"]
    }
  }
}
```

### Cache Index Format (Simplified)

```json
{
  "url_prompt_hash": {
    "url": "https://api.example.com/openapi.json",
    "prompt": "What are all the API endpoints?",
    "answer_file": ".claude/memory/web_cache/qa_pairs/abc123_def456.json",
    "ttl_hours": 24,
    "last_fetched": "2025-10-29T10:00:00Z",
    "expires_at": "2025-10-30T10:00:00Z",
    "fetch_count": 2,
    "workflow_used": ["planning", "build"]
  }
}
```

### TTL Strategy (Hours-Based)

- **API Specifications**: 24 hours (APIs change frequently, answers may become outdated)
- **Library Documentation**: 48 hours (version updates, usage patterns change)
- **Framework Docs**: 48 hours (examples and best practices evolve)
- **Standards/Guidelines**: 72 hours (even stable content has updates)

**Rationale**: Since we cache answers (not raw content), shorter TTLs ensure answers stay current. Answers summarize content at fetch time, so re-fetching with same prompt may yield updated information.

### Smart Fetching Rules (Q&A Based)

**Cache-First Strategy**:
1. **Hash Query**: Create hash from `{url}_{prompt}` combination
2. **Check Cache Index**: Lookup hash in `cache_index.json`
3. **Validate TTL**: If cached and TTL valid → return cached answer (no fetch)
4. **Expired Cache**: If cached but expired → re-fetch with same prompt
5. **Not Cached**: If not cached → fetch with prompt and cache answer
6. **Update Index**: Always update cache_index.json with new Q&A pair

**Deduplication**:
- Track `{url, prompt}` combinations fetched in current workflow
- Same query in same workflow = use cached answer (already fetched)
- Different prompts on same URL = different cache entries (ask different questions)

**Graceful Fallback**:
- If fetch fails → use cached answer (even if expired)
- Log fetch failure for debugging
- Notify user if using stale cache

**Prompt Consistency**:
- Use same prompt wording for same URL to maximize cache hits
- Standardize common questions (e.g., "What are the API endpoints?")

**Cache Corruption Handling**:
- **Detection**: Validate `cache_index.json` is valid JSON before use
- **Recovery**: If corrupted, attempt to rebuild from cache files
- **Fallback**: If rebuild fails, clear cache index and re-fetch
- **Validation**: Verify cached files exist before using (files may be deleted but index not updated)
- **Error Handling**: Log corruption events to `.claude/memory/web_cache/corruption.log` for debugging

### Cache Cleanup

**Automatic Cleanup** (run weekly):
- Delete cached files if TTL expired >30 days
- Remove unused cache entries (>90 days unused)
- Keep cache_index.json clean

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
    docs = web_fetch(url=url)
except FetchError:
    # Fallback: Use local documentation
    docs = read_local_docs(url)
    log("Used local docs, fetch failed")
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
user_request = "Integrate with Stripe API"

# Question 1: Get all endpoints
endpoints = WebFetch(
  url="https://stripe.com/docs/api",
  prompt="What are all the API endpoint paths, HTTP methods, and their purposes?"
)

# Question 2: Get authentication details
auth_info = WebFetch(
  url="https://stripe.com/docs/api/authentication",
  prompt="How do I authenticate requests? What API keys are needed and where do I get them?"
)

# Question 3: Get payment models
payment_models = WebFetch(
  url="https://stripe.com/docs/api/payment_intents",
  prompt="What are the PaymentIntent data model fields and their types? What are required vs optional fields?"
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
  prompt="How do I install and set up react-query? What's the basic configuration?"
)

# Question 2: Common patterns
usage_patterns = WebFetch(
  url="https://tanstack.com/query/latest/docs/react/guides/queries",
  prompt="What are the most common query patterns and code examples for fetching data?"
)

# Question 3: Mutations
mutations_info = WebFetch(
  url="https://tanstack.com/query/latest/docs/react/guides/mutations",
  prompt="How do I handle mutations? What's the pattern for POST/PUT/DELETE operations?"
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

## Integration with cc10x

**Orchestrator Integration**:
- Check if external resources needed
- Fetch before workflow starts if needed
- Cache fetched resources for workflow duration

**Workflow Integration**:
- Add web fetch step before phases that need external docs
- Store fetched content for reference
- Include fetched sources in Verification Summary

## References

- Anthropic Web Fetch Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-fetch-tool
- cc10x Workflows: `plugins/cc10x/skills/cc10x-orchestrator/workflows/`

