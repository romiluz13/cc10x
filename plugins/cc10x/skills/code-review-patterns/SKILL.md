---
name: code-review-patterns
description: Context-aware code review analysis covering security, quality, and performance. Use PROACTIVELY when reviewing code. First understands functionality requirements and project patterns, then checks for security vulnerabilities, code quality issues, and performance bottlenecks that affect functionality. Provides specific remediation with code examples aligned with project patterns. Focuses on issues that block or degrade functionality, not generic checklists.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review Patterns - Context-Aware & Functionality First

## Purpose

This skill provides comprehensive code review analysis covering security, code quality, performance, refactoring, code explanation, and code cleanup. It understands functionality and project patterns before checking, focusing on issues that affect functionality and providing specific remediation aligned with project patterns.

**Unique Value**:

- Context-aware analysis (not generic checklists)
- Covers security, quality, performance, refactoring, explanation, cleanup in one skill
- Performance measurement-first approach (measure before optimizing)
- Refactoring methodology with complexity metrics and proven techniques
- Security threat modeling with systematic vulnerability scanning
- Code explanation with visual diagrams and progressive disclosure
- Code cleanup with code smell detection and refactoring catalog
- Focuses on issues affecting functionality
- Provides specific fixes with code examples
- Understands project patterns before checking

**When to Use**:

- After functionality is verified
- When reviewing code that implements features
- When checking for security, quality, or performance issues
- When refactoring code to improve structure
- When explaining complex code
- When cleaning up technical debt

---

## Quick Start

Review code by first understanding functionality and project patterns, then checking for security, quality, and performance issues affecting functionality.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Understand project patterns**: JWT auth, React hooks, REST APIs
3. **Check security**: Missing authentication → blocks functionality
4. **Check quality**: Unclear naming → hard to maintain
5. **Check performance**: N+1 queries → degrades functionality
6. **Provide fixes**: Specific code examples aligned with project patterns

**Result:** Security, quality, and performance issues affecting functionality identified and fixed.

## Functionality First Mandate

**BEFORE applying review checks, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (Security, performance constraints)
   - Dependencies: What does it need?
   - Edge Cases: What can go wrong?
   - Verification: How do we know it works?
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type):
   - UI Features → User Flow, Admin Flow, System Flow
   - Backend APIs → Request Flow, Response Flow, Error Flow, Data Flow
   - Utilities → Input Flow, Processing Flow, Output Flow, Error Flow
   - Integrations → Integration Flow, Data Flow, Error Flow, State Flow

3. **THEN understand project patterns** - Before checking

4. **THEN check security, quality, performance** - Only issues that affect functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any review checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this code supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc.)

3. **Verify Functionality Works**:
   - Does functionality work? (tested)
   - Do flows work? (tested)
   - Does error handling work? (tested)

---

### Phase 2: Understand Project Patterns (MANDATORY SECOND STEP)

**Before checking, understand how this project handles security, quality, and performance**:

1. **Map Security Patterns**:

   ```bash
   grep -r "jwt\|session\|oauth\|auth" --include="*.ts" | head -20
   grep -r "authorize\|permission\|role" --include="*.ts" | head -20
   grep -r "validate\|sanitize\|escape" --include="*.ts" | head -20
   ```

2. **Map Quality Patterns**:

   ```bash
   ls -R src/ | grep -E "\.(ts|tsx|js|jsx)$" | head -20
   grep -r "function \|const \|export const " --include="*.ts" | head -20
   cat .eslintrc.json 2>/dev/null || cat .prettierrc 2>/dev/null
   ```

3. **Map Performance Patterns**:
   ```bash
   grep -r "query\|fetch\|await\|Promise" --include="*.ts" | head -20
   grep -r "db\.\|database\|mongoose\|prisma" --include="*.ts" | head -20
   ```

**Document Project Patterns**:

- Security: Authentication (JWT/Sessions/OAuth), Authorization (RBAC/ABAC), Validation patterns
- Quality: Naming conventions, structure, style, testing patterns
- Performance: Caching strategies, database optimization, API optimization

---

### Phase 3: Security Analysis (Only Issues Affecting Functionality)

**After understanding functionality and project security model, check security**:

**Check Authentication** (if functionality requires auth):

- Is authentication implemented correctly?
- Does it prevent unauthorized access to functionality?
- Are tokens validated properly?

**Check Authorization** (if functionality requires authorization):

- Is authorization implemented correctly?
- Does it prevent unauthorized access to functionality?
- Are permissions checked at the right boundaries?

**Check Input Validation** (if functionality handles user input):

- Is input validated correctly?
- Does validation prevent functionality from working incorrectly?
- Are injection attacks prevented?

**Check Data Handling** (if functionality handles sensitive data):

- Is sensitive data handled securely?
- Is data encrypted at rest and in transit?
- Are secrets managed securely?

**Priority Classification**:

- **Critical**: Blocks functionality (injection attacks, broken auth)
- **Important**: Affects functionality (weak auth, missing validation)
- **Minor**: Doesn't affect functionality (security headers, perfect hashing)

---

### Phase 4: Code Quality Analysis (Only Issues Affecting Functionality or Maintainability)

**After understanding functionality and codebase conventions, check quality**:

**Check Readability** (if affects understanding functionality):

- Is code readable enough to understand what it does?
- Are names clear and aligned with codebase conventions?
- Is structure clear and aligned with codebase patterns?

**Check Maintainability** (if affects modifying functionality):

- Is code organized to support changes?
- Are functions/classes focused and aligned with codebase patterns?
- Is duplication preventing fixing bugs in one place?

**Check Error Handling** (if affects functionality):

- Is error handling present and aligned with codebase patterns?
- Are errors handled gracefully?
- Are error messages helpful?

**Priority Classification**:

- **Critical**: Blocks changes (unreadable code, high complexity)
- **Important**: Causes bugs or affects maintainability (missing error handling, long functions)
- **Minor**: Hard to understand or style issues (complexity metrics, perfect SOLID)

---

### Phase 5: Performance Analysis (Only Issues Affecting Functionality)

**After understanding functionality and performance requirements, check performance**:

**Check Latency** (if affects user experience):

- Are response times within requirements?
- Are there slow queries or API calls?
- Are there unnecessary operations?

**Check Throughput** (if affects scalability):

- Can system handle required throughput?
- Are there bottlenecks preventing scale?
- Are resources used efficiently?

**Check Database Performance** (if functionality uses database):

- Are queries optimized?
- Are there N+1 query problems?
- Are indexes used correctly?

**Priority Classification**:

- **Critical**: Blocks functionality (timeouts, crashes, errors)
- **Important**: Degrades UX (slow loading, laggy interactions)
- **Minor**: Optimizations (premature optimization, perfect caching)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Code Review Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Project Patterns Summary

[Brief summary of project patterns from Phase 2]

## Security Findings

### Critical Issues (Blocks Functionality)

- **Issue**: [Description]
- **Impact**: [How it blocks functionality]
- **Location**: [File:line]
- **Fix**: [Specific code example aligned with project patterns]
- **Priority**: Critical

### Important Issues (Affects Functionality)

[Similar format]

## Code Quality Findings

### Critical Issues (Blocks Changes)

[Similar format]

## Performance Findings

### Critical Issues (Blocks Functionality)

[Similar format]

## Recommendations

[Prioritized list - Critical first, then Important, then Minor]
```

---

## Reference Materials

**For detailed patterns, see**:

- **PATTERNS.md**: Complete pattern library covering security, quality, performance, refactoring, code explanation, code cleanup
- **Security Patterns**: Authentication, Authorization, Injection Prevention, File Upload, Secrets Management, Threat Modeling, OWASP Top 10
- **Quality Patterns**: Naming, Organization, Error Handling, Testing, Duplication, Complexity, SOLID Principles
- **Performance Patterns**: Measurement-first approach, Frontend optimization, Backend optimization, Critical path analysis, Database optimization
- **Refactoring Patterns**: Complexity metrics, Refactoring catalog techniques, Code simplification, Technical debt reduction
- **Code Explanation Patterns**: Complexity assessment, Visual diagrams (Mermaid), Progressive explanation, Pattern recognition
- **Code Cleanup Patterns**: Code smell detection, Refactoring techniques, Modern pattern application, Dead code removal

---

## Usage Guidelines

### For Review Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis)
2. **Then**: Complete Phase 2 (Understand Project Patterns)
3. **Then**: Complete Phases 3-5 (Security, Quality, Performance Analysis)
4. **Focus**: Issues that block or degrade functionality

### Key Principles

1. **Functionality First**: Always understand functionality before checking
2. **Context-Aware**: Understand project patterns before checking
3. **Specific Fixes**: Provide code examples aligned with project patterns
4. **Prioritize by Impact**: Critical (blocks functionality) > Important (affects functionality) > Minor (defer)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to review checks
2. **Ignoring Project Patterns**: Don't provide generic fixes - align with project patterns
3. **Generic Checklists**: Don't check everything - focus on functionality-affecting issues
4. **Missing Specific Fixes**: Don't just identify issues - provide specific code examples
5. **Wrong Priority**: Don't mark minor issues as critical - prioritize by functionality impact

---

## Troubleshooting

**Common Issues:**

1. **Review checks without understanding functionality**
   - **Symptom**: Finding issues that don't affect functionality
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first
   - **Prevention**: Always understand functionality before checking

2. **Generic fixes not aligned with project patterns**
   - **Symptom**: Fixes don't match project patterns
   - **Cause**: Didn't understand project patterns
   - **Fix**: Understand project patterns, provide aligned fixes
   - **Prevention**: Always understand project patterns first

**If issues persist:**

- Verify functionality analysis was completed first
- Check that project patterns were understood
- Ensure fixes align with project patterns

---

_This skill enables comprehensive code review analysis covering security, quality, and performance with functionality-first approach, providing specific remediation with code examples aligned with project patterns._
