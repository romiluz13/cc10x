---
description: Comprehensive parallel code review by 5 specialized reviewers (security, quality, performance, UX, accessibility)
argument-hint: [files or directory]
---

# Comprehensive Code Review Workflow

You are orchestrating a comprehensive code review with 5 parallel specialized reviewers.

## Context
- Target: $ARGUMENTS
- Files to review: !`git diff --name-only HEAD~1 2>/dev/null || find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" \) -mtime -1`
- Recent changes: !`git log --oneline -5`

## THE FOCUS RULE
⚠️ **CRITICAL**: Only review what was explicitly requested. DO NOT expand scope.

## Review Scope

IF no argument: Review recent changes (last commit)
IF files specified: Review ONLY those files
IF directory: Review files in that directory only

## Your Task

### Phase 1: Scope Definition
1. List exact files to review
2. Confirm with user if needed
3. Load file contents

### Phase 2: Invoke 5 Parallel Reviewers

**EXECUTE THESE CONCURRENTLY using sub-agents:**

#### 1. Security Reviewer (`security-reviewer` agent)
- Authentication/authorization issues
- Input validation gaps
- SQL injection risks
- XSS vulnerabilities
- Secret exposure
- Dependency vulnerabilities

#### 2. Quality Reviewer (`quality-reviewer` agent)
- Code complexity
- Duplication
- Naming conventions
- Error handling
- Code organization
- Best practices

#### 3. Performance Analyzer (`performance-analyzer` agent)
- Algorithmic efficiency
- Database query optimization
- Memory leaks
- Unnecessary computations
- Bundle size impact
- Caching opportunities

#### 4. UX Reviewer (`ux-reviewer` agent)
- User flow clarity
- Error messages
- Loading states
- Accessibility (WCAG)
- Mobile responsiveness
- Visual consistency

#### 5. Accessibility Checker (`accessibility-reviewer` agent)
- Keyboard navigation
- Screen reader support
- Color contrast
- ARIA labels
- Focus management
- Semantic HTML

### Phase 3: Synthesis
1. Wait for all 5 reviewers to complete
2. Collect findings
3. Deduplicate issues
4. Prioritize by severity:
   - 🔴 CRITICAL: Must fix before merge
   - 🟠 HIGH: Should fix soon
   - 🟡 MEDIUM: Consider fixing
   - 🔵 LOW: Nice to have

### Phase 4: Report

```markdown
# Code Review Results

## Summary
- Files reviewed: N
- Total issues: X
- Critical: A | High: B | Medium: C | Low: D

## Critical Issues (🔴 MUST FIX)
1. [Issue from Reviewer] - [Description]
   - File: [path:line]
   - Impact: [Why critical]
   - Fix: [Suggested solution]

## High Priority (🟠 SHOULD FIX)
...

## Medium Priority (🟡 CONSIDER)
...

## Low Priority (🔵 OPTIONAL)
...

## Positive Findings
- [Things done well]

## Recommendations
- [Overall suggestions]
```

## Success Criteria
- All 5 reviewers completed
- Issues categorized by severity
- Actionable recommendations provided
- No scope creep beyond requested files

