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

**Availability**: ✅ WebFetch is available in Claude Code (listed in available tools)

**Basic Usage**:
- WebFetch tool is automatically available in Claude Code
- Use `WebFetch` in `allowed-tools` to ensure access
- Tool handles fetching web pages and PDFs

**Example Integration**:
```bash
# Claude Code automatically uses WebFetch when needed
# Just mention URLs in context, Claude will fetch them

# During planning workflow - mention API spec URL
# "I need to fetch https://api.example.com/openapi.json for API design"

# During build workflow - mention library docs
# "Fetch https://docs.library.com/getting-started for implementation guidance"
```

**Explicit Usage** (if needed):
- WebFetch tool is model-invoked automatically when URLs are referenced
- No explicit API calls needed - Claude Code handles it
- Results are included in context automatically

## Integration Points

### Planning Workflow

**Phase 1 - Requirements Intake**:
- If external APIs mentioned, fetch API documentation
- If frameworks mentioned, fetch framework docs
- If external services mentioned, fetch service docs

**Phase 2 - Architecture Design**:
- Fetch integration patterns from external sources
- Load external architecture guides
- Access best practice documentation

### Build Workflow

**Before Component Building**:
- Fetch library documentation if new library used
- Load SDK examples if SDK integration needed
- Access framework guides for implementation

**During Integration**:
- Fetch API documentation for external services
- Load integration guides
- Access troubleshooting resources

### Review Workflow

**Security Review**:
- Fetch OWASP guidelines (if not in skills)
- Load security best practices from external sources
- Access vulnerability databases

**Performance Review**:
- Fetch performance optimization guides
- Load profiling tool documentation
- Access benchmarking resources

### Debug Workflow

**During Investigation**:
- Fetch error documentation
- Load troubleshooting guides
- Access stack trace analysis resources

## Web Fetch Patterns

### Pattern 1: API Specification Loading

```python
# Fetch API spec for planning
def load_api_spec(api_url):
    spec_url = f"{api_url}/openapi.json"  # or swagger.json
    spec = web_fetch(url=spec_url)
    return parse_spec(spec)
```

### Pattern 2: Documentation Loading

```python
# Fetch library docs during build
def load_library_docs(library_name):
    docs_url = f"https://docs.{library_name}.com"
    docs = web_fetch(url=docs_url)
    return extract_examples(docs)
```

### Pattern 3: Reference Material Loading

```python
# Fetch reference guides
def load_reference_guide(guide_url):
    guide = web_fetch(url=guide_url)
    return parse_markdown(guide)
```

## Smart Caching Strategy (AI Coding Assistant Optimized)

### Cache Structure

```
.claude/memory/web_cache/
├── api_specs/
│   ├── stripe_api_v1.json (with timestamp)
│   └── github_api_v3.json (with timestamp)
├── library_docs/
│   └── react_query_v5.md (with timestamp)
├── framework_docs/
│   └── nextjs_v14.md (with timestamp)
└── cache_index.json (URL → file mapping, TTL, last_fetched)
```

### Cache Index Format

```json
{
  "https://stripe.com/docs/api": {
    "cached_file": ".claude/memory/web_cache/api_specs/stripe_api_v1.json",
    "ttl_days": 7,
    "last_fetched": "2025-10-22T10:00:00Z",
    "expires_at": "2025-10-29T10:00:00Z",
    "fetch_count": 3,
    "workflow_used": ["planning", "build"]
  }
}
```

### TTL Strategy

- **API Specifications**: 7 days (APIs change frequently)
- **Library Documentation**: 14 days (version updates)
- **Framework Docs**: 30 days (major releases)
- **Standards/Guidelines**: 90 days (stable content)

### Smart Fetching Rules

**Cache-First Strategy**:
1. **Check Cache Index**: Lookup URL in `cache_index.json`
2. **Validate TTL**: If cached and TTL valid → use cache (no fetch)
3. **Expired Cache**: If cached but expired → re-fetch
4. **Not Cached**: If not cached → fetch and cache
5. **Update Index**: Always update cache_index.json

**Deduplication**:
- Track URLs fetched in current workflow
- Same URL in same workflow = use cached (already fetched)
- Batch fetch multiple URLs when possible

**Graceful Fallback**:
- If fetch fails → use cached version (even if expired)
- Log fetch failure for debugging
- Notify user if using stale cache

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

### Cache Check Function

```bash
#!/bin/bash
# Check cache before fetching URL
# Includes cache corruption handling

check_cache() {
  local url="$1"
  local cache_index=".claude/memory/web_cache/cache_index.json"
  
  # Validate cache_index.json exists and is valid JSON
  if [ ! -f "$cache_index" ]; then
    echo "CACHE_MISS"
    return 2
  fi
  
  # Validate JSON syntax (cache corruption detection)
  if ! jq empty "$cache_index" 2>/dev/null; then
    # Cache index corrupted - rebuild from cache files
    echo "CACHE_CORRUPTED: Rebuilding cache_index.json" >&2
    rebuild_cache_index "$cache_index"
    if ! jq empty "$cache_index" 2>/dev/null; then
      # Rebuild failed - clear cache and start fresh
      echo "CACHE_REBUILD_FAILED: Clearing cache" >&2
      rm -f "$cache_index"
      echo "CACHE_MISS"
      return 2
    fi
  fi
  
  # Check if URL in cache index
  local cached=$(jq -r ".[\"$url\"] // empty" "$cache_index" 2>/dev/null)
  if [ -n "$cached" ] && [ "$cached" != "null" ]; then
    local expires=$(echo "$cached" | jq -r '.expires_at // empty' 2>/dev/null)
    local cached_file=$(echo "$cached" | jq -r '.cached_file // empty' 2>/dev/null)
    
    # Validate cached file exists
    if [ -z "$cached_file" ] || [ ! -f "$cached_file" ]; then
      # Cached file missing - remove from index
      jq "del(.[\"$url\"])" "$cache_index" > "$cache_index.tmp" && mv "$cache_index.tmp" "$cache_index"
      echo "CACHE_MISS"
      return 2
    fi
    
    # Check if TTL valid
    if [ -n "$expires" ] && [ "$(date -d "$expires" +%s 2>/dev/null)" -gt "$(date +%s)" ]; then
      echo "CACHE_HIT:$cached_file"
      return 0
    else
      echo "CACHE_EXPIRED:$cached_file"
      return 1
    fi
  fi
  
  echo "CACHE_MISS"
  return 2
}

# Rebuild cache index from existing cache files
rebuild_cache_index() {
  local cache_index="$1"
  local cache_dir=".claude/memory/web_cache"
  
  echo "{}" > "$cache_index"
  
  # Rebuild from cached files (if any exist)
  find "$cache_dir" -type f -name "*.json" -o -name "*.md" | while read -r cached_file; do
    # Extract URL from file metadata or skip (re-fetch later)
    # For now, just clear corrupted index - re-fetch will rebuild properly
    true
  done
}
```

### Cache Save Function

```bash
#!/bin/bash
# Save fetched content to cache

save_to_cache() {
  local url="$1"
  local content_file="$2"
  local ttl_days="${3:-7}"  # Default 7 days
  
  local cache_dir=".claude/memory/web_cache"
  local cache_index="$cache_dir/cache_index.json"
  
  mkdir -p "$cache_dir/api_specs" "$cache_dir/library_docs" "$cache_dir/framework_docs"
  
  # Determine cache subdirectory based on URL pattern
  local subdir="api_specs"
  if [[ "$url" =~ "docs\.(library|framework)" ]]; then
    subdir="library_docs"
  fi
  
  local cached_file="$cache_dir/$subdir/$(echo "$url" | md5sum | cut -d' ' -f1).json"
  cp "$content_file" "$cached_file"
  
  # Update cache index
  local expires_at=$(date -d "+$ttl_days days" -Iseconds)
  jq --arg url "$url" \
     --arg file "$cached_file" \
     --arg ttl "$ttl_days" \
     --arg expires "$expires_at" \
     '.[$url] = {
       "cached_file": $file,
       "ttl_days": ($ttl | tonumber),
       "last_fetched": (now | strftime("%Y-%m-%dT%H:%M:%SZ")),
       "expires_at": $expires,
       "fetch_count": ((.[$url].fetch_count // 0) + 1)
     }' "$cache_index" > "$cache_index.tmp"
  mv "$cache_index.tmp" "$cache_index"
}
```

## Verification Checklist

**Before Fetching**:
- [ ] Check `cache_index.json` for URL
- [ ] If cached and TTL valid → use cache (skip fetch)
- [ ] If cached but expired → mark for re-fetch
- [ ] If not cached → proceed with fetch
- [ ] Verify URL is valid and accessible

**After Fetching**:
- [ ] Save to cache with appropriate TTL
- [ ] Update cache_index.json
- [ ] Validate fetched content is relevant
- [ ] Extract only needed sections
- [ ] Cite source in workflow output
- [ ] Track which workflow used this cache

**On Fetch Failure**:
- [ ] Check for stale cache (even if expired)
- [ ] Use stale cache if available
- [ ] Log failure for debugging
- [ ] Notify user if using stale cache

## Examples

### Example 1: Planning with External API

```python
# Planning workflow - Phase 1
user_request = "Integrate with Stripe API"

# Fetch Stripe API docs
stripe_docs = web_fetch(url="https://stripe.com/docs/api")
payment_patterns = extract_patterns(stripe_docs)

# Use in architecture design
design_api_integration(stripe_docs, payment_patterns)
```

### Example 2: Build with Library Docs

```python
# Build workflow - Before component
library = "react-query"

# Fetch library docs
react_query_docs = web_fetch(url="https://tanstack.com/query/latest")
examples = extract_examples(react_query_docs)

# Use in implementation
implement_with_guidance(examples)
```

### Example 3: Review with External Standards

```python
# Review workflow - Security review
security_guidelines = web_fetch(url="https://owasp.org/www-project-top-ten/")

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

