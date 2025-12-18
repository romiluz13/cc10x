---
name: code-review-patterns
description: This skill should be used when the user asks to "review code", "audit security", "check code quality", "review a PR", or needs guidance on code review for security, quality, and performance issues.
---

# Code Review Patterns

Review code for security, quality, and performance issues.

## Process

### 1. Understand Functionality First

Before reviewing:

- What is this code supposed to do?
- What are the user flows?
- What are the system flows?

### 2. Verify It Works

Check functionality before other concerns:

- Does the code achieve its purpose?
- Do tests pass?
- Does it handle expected inputs?

### 3. Review for Issues

Check in order of priority:

1. **Security** - Vulnerabilities that could be exploited
2. **Quality** - Code that's hard to maintain
3. **Performance** - Code that's unnecessarily slow

## Security Checklist

- [ ] Input validation (no injection vulnerabilities)
- [ ] Authentication checks (authorized access only)
- [ ] No secrets in code (API keys, passwords)
- [ ] Safe SQL queries (parameterized)
- [ ] XSS prevention (escaped output)
- [ ] CSRF protection (tokens for state changes)

## Quality Checklist

- [ ] Clear naming (intent obvious from names)
- [ ] Single responsibility (each function does one thing)
- [ ] No code duplication (DRY where appropriate)
- [ ] Error handling (failures handled gracefully)
- [ ] Testable code (dependencies injectable)

## Performance Checklist

- [ ] No N+1 queries (batch database calls)
- [ ] Efficient loops (no unnecessary iterations)
- [ ] Appropriate caching (repeated expensive operations cached)
- [ ] Memory management (no leaks, large objects cleaned up)

## Severity Classification

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Blocks functionality or security vulnerability | Must fix before merge |
| Important | Affects functionality or significant quality issue | Should fix before merge |
| Minor | Style issues, minor improvements | Can merge, fix later |

## Output Format

```markdown
## Code Review Summary

- **Status**: Approve / Changes Requested
- **Functionality**: Works / Broken

## Critical Issues
- [Issue] at [file:line] - [Fix recommendation]

## Important Issues
- [Issue] at [file:line] - [Fix recommendation]

## Minor Issues
- [Issue] at [file:line] - [Suggestion]
```

## Common Mistakes

1. **Reviewing without understanding functionality** - Know what code should do first
2. **Generic feedback** - Be specific with file:line citations
3. **Missing severity** - Classify issues by impact
4. **No fix recommendations** - Provide actionable suggestions
