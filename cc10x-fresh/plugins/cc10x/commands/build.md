---
description: Implement features with optional TDD, code generation, and quality checks
argument-hint: [plan-file or feature-description]
---

# Feature Building Workflow

You are implementing a feature with production-quality code.

## Context
- Input: $ARGUMENTS
- Project files: !`find . -type f -name "*.ts" -o -name "*.js" -o -name "*.py" | head -20`
- Tests: !`find . -type f -name "*.test.*" -o -name "*_test.*" | wc -l`

## Complexity Gate

BEFORE starting:
1. Assess complexity (1-5 scale)
2. IF complexity <= 2: WARN user "Manual coding is 16x cheaper. Continue anyway?"
3. Wait for confirmation

## Your Task

### Phase 1: Setup
- Load existing plan (if provided)
- Understand requirements
- Identify files to modify/create

### Phase 2: Development Approach
Ask user: "Development approach?"
- **Fast**: Direct implementation, basic tests
- **TDD**: Test-first development
- **Balanced**: Implementation with comprehensive tests after

### Phase 3: Implementation
1. Write clean, modular code
2. Follow project conventions
3. Add inline documentation
4. Handle errors properly
5. Keep files < 500 lines (split if needed)

### Phase 4: Quality Checks
- Run linter
- Check for common issues
- Verify no TODOs or placeholders

### Phase 5: Testing
IF user chose TDD or Balanced:
- Write comprehensive tests
- Run tests
- Fix failures
- Verify coverage

## Best Practices
- ✅ Complete implementations only
- ✅ DRY principle
- ✅ SOLID principles
- ✅ Proper error handling
- ❌ NO placeholders
- ❌ NO TODOs
- ❌ NO incomplete code

## Output
- List of files changed
- Summary of implementation
- Test results (if applicable)
- Suggest: "Run `/review` for comprehensive code review"

