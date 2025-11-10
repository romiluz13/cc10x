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

## Reference Materials

**For detailed patterns, caching strategies, and examples, see:**

- **REFERENCE.md**: Web Fetch Patterns, Smart Caching Strategy, Best Practices, Error Handling, Examples, Verification Checklist

---

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

## References

- Anthropic Web Fetch Tool: https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-fetch-tool
- cc10x Workflows: `plugins/cc10x/skills/cc10x-orchestrator/workflows/`

---

**Remember**: External docs exist to support functionality. Don't fetch docs generically - fetch docs related to functionality!
