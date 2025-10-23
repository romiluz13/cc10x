---
name: Verification Before Completion
description: |
  Comprehensive quality checklist ensuring code is production-ready before marking tasks complete. Use to verify all quality gates are met before commit or completion.
  
  Trigger phrases: "verify", "check before commit", "quality check", "verify complete",
  "pre-commit check", "verify quality", "completion check", "ready to commit",
  "verify production-ready", "check quality gates", "verification checklist",
  "ensure complete", "validate completion", "check before merge", "final verification".
  
  Activates on: pre-commit verification, completion checks, quality gate validation,
  production readiness assessment, final verification before tasks completion.
progressive: true
---

# Verification Before Completion

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)
- **Skill**: Verification Before Completion
- **Purpose**: Production-readiness quality gates
- **When**: Before marking tasks complete, before committing code
- **Core Rule**: Done = Works + Tested + Clean + Ready for production
- **Sections Available**: Quick Checklist, Detailed Checks, Failure Actions

---

### Stage 2: Quick Reference (triggered - ~500 tokens)

#### Quick Verification Checklist

Copy and complete before marking done:

```
Quality Verification:
- [ ] Tests exist and pass
- [ ] All tests run (not just new ones)
- [ ] No errors or warnings in output
- [ ] Code follows project conventions
- [ ] No debug code (console.log, debugger, etc.)
- [ ] Error handling present
- [ ] Edge cases covered
- [ ] Files properly organized
- [ ] Git commit ready
```

#### Run Tests

```bash
# Run all tests
npm test
# or
pytest
# or appropriate test command

# Confirm:
# ✅ All tests pass
# ✅ No errors or warnings
# ✅ Code coverage adequate
```

#### Check for Debug Code

```bash
grep -r "console.log\|debugger\|TODO\|FIXME" src/ --include="*.ts"

# Must return: No results
# ❌ If found: Remove all before committing
```

#### Verify Project Patterns

Check:
- **Naming**: Follows conventions (camelCase, PascalCase, UPPER_SNAKE)
- **Structure**: Files in correct locations
- **Imports**: Organized (external → internal → relative)
- **Exports**: Explicit (not barrel exports)

#### Error Handling Check

Every operation that can fail must handle errors:

```typescript
// ✅ Good
try {
  const data = await fetchData();
  return processData(data);
} catch (error) {
  logger.error('Failed to process data', error);
  throw new ProcessingError('Data processing failed', { cause: error });
}
```

```typescript
// ❌ Bad - no error handling
const data = await fetchData();
return processData(data);
```

#### Git Commit Ready

```bash
# Review diff
git diff --staged

# Confirm:
# ✅ Only intended changes
# ✅ No secrets or keys
# ✅ No sensitive data
# ✅ No binary files (unless intended)
```

#### If Verification Fails

**Don't mark complete.** Fix issues first:

| Issue | Action |
|-------|--------|
| Tests fail | Fix code or tests |
| Errors/warnings | Address all issues |
| Missing tests | Add tests (TDD) |
| Debug code present | Remove all debug code |
| Poor error handling | Add try-catch, validation |
| Style violations | Run formatter, fix manually |

---

### Stage 3: Detailed Content (on-demand - ~1500 tokens)

## Detailed Verification Checks

### 1. Tests Exist and Pass

```bash
npm test
```

**Confirm**:
- ✅ All new code has tests
- ✅ Tests were written FIRST (TDD)
- ✅ Tests pass consistently
- ✅ No flaky tests

**Test coverage**:
```bash
# View coverage report
npm test -- --coverage
```

**Target**: >80% coverage for new code

### 2. Full Test Suite

```bash
npm test  # Run ALL tests, not just new ones
```

**Confirm**:
- ✅ No regressions (existing tests still pass)
- ✅ All tests pass
- ✅ Test suite completes without errors

### 3. Clean Output

**Check for**:
- ❌ Errors in console
- ❌ Warnings
- ❌ Deprecation notices
- ❌ Type errors
- ❌ Linting failures

**All must be clean** before proceeding.

**Run linter**:
```bash
npm run lint
# or
eslint src/
```

### 4. Code Conventions

#### Naming

- **Functions**: camelCase, descriptive - `getUserById`, `validateEmail`
- **Variables**: camelCase, meaningful - `userData`, `isActive`
- **Classes**: PascalCase - `UserService`, `PaymentProcessor`
- **Constants**: UPPER_SNAKE_CASE - `MAX_RETRY_COUNT`

#### Structure

- ✅ Follows project patterns
- ✅ Files in correct locations
- ✅ Imports organized (external → internal → relative)
- ✅ Exports explicit

#### Style

- ✅ Consistent formatting
- ✅ No trailing whitespace
- ✅ Proper indentation
- ✅ Comments only where needed (explain WHY, not WHAT)

### 5. No Debug Code

**Search and remove**:

```bash
# Find debug code
grep -r "console.log" src/ --include="*.ts"
grep -r "debugger" src/ --include="*.ts"
grep -r "TODO" src/ --include="*.ts"
grep -r "FIXME" src/ --include="*.ts"
```

**Zero tolerance** for debug code in commits.

**Exceptions**:
- Logging in production (use logger.info, logger.error)
- TODO in comments IF tracked in issue tracker

### 6. Error Handling

**Every operation that can fail must handle errors**:

```typescript
// ✅ Good: Specific error, helpful message
try {
  const data = await fetchData();
  return processData(data);
} catch (error) {
  logger.error('Failed to process data', error);
  throw new ProcessingError('Data processing failed', { cause: error });
}
```

```typescript
// ❌ Bad: No error handling
const data = await fetchData();
return processData(data);
```

**Check**:
- ✅ All async operations wrapped in try-catch
- ✅ All validation throws specific errors
- ✅ All errors logged with context
- ✅ All errors have helpful messages

### 7. Edge Cases

**Check coverage for**:
- Empty inputs (`[]`, `''`, `null`, `undefined`)
- Null/undefined values
- Invalid types
- Boundary conditions (0, 1, max)
- Error states

```typescript
// ✅ Good: Edge cases covered
test('handles empty array', () => {
  expect(sum([])).toBe(0);
});

test('handles null input', () => {
  expect(() => sum(null)).toThrow('Input required');
});

test('handles single element', () => {
  expect(sum([5])).toBe(5);
});

test('handles negative numbers', () => {
  expect(sum([-1, -2])).toBe(-3);
});
```

### 8. File Organization

**Confirm**:
- ✅ New files in correct directories
- ✅ No temporary files committed (`.tmp`, `.bak`)
- ✅ No unused imports
- ✅ No commented-out code

**Remove unused imports**:
```bash
# Many editors can auto-remove
# Or use: eslint --fix
```

**Remove commented code**:
```typescript
// ❌ Bad: Commented-out code
// function oldImplementation() {
//   return 'old';
// }

function newImplementation() {
  return 'new';
}
```

**Git tracks history** - no need to keep commented code.

### 9. Git Commit Ready

#### Stage Files

```bash
git add <files>
```

#### Review Diff

```bash
git diff --staged
```

**Confirm**:
- ✅ Only intended changes
- ✅ No secrets or keys
- ✅ No sensitive data (passwords, API keys, tokens)
- ✅ No binary files (unless intended)
- ✅ No large files (>1MB, unless necessary)

#### Write Clear Commit Message

```bash
git commit -m "feat: add user authentication

- Implement JWT-based auth
- Add login and register endpoints
- Include comprehensive tests
- All tests passing"
```

**Format**:
- **Type**: `feat`, `fix`, `docs`, `refactor`, `test`
- **Description**: Clear, concise (< 72 chars for first line)
- **Body**: Bullet points describing changes
- **Co-author**: Include if AI-assisted

## Quick Verification (Small Changes)

For small changes (< 50 lines):

```
Quick Check:
- [ ] Test passes
- [ ] No errors
- [ ] Follows conventions
- [ ] Ready to commit
```

## Verification Failed?

**Don't mark complete.** Fix issues first:

| Issue | Action |
|-------|--------|
| Tests fail | Fix code or tests. Understand why failing. |
| Errors/warnings | Address all issues. Don't ignore warnings. |
| Missing tests | Add tests using TDD. Watch fail → pass. |
| Debug code present | Remove ALL console.log, debugger, TODOs. |
| Poor error handling | Add try-catch blocks, validation checks. |
| Style violations | Run formatter (`prettier`, `eslint --fix`). |
| Uncommitted changes | Stage and commit with clear message. |

## Final Confirmation

Before marking task complete:

```
I have verified:
✅ Tests exist and pass
✅ Full test suite passes
✅ No errors or warnings
✅ Code follows conventions
✅ No debug code
✅ Error handling present
✅ Edge cases covered
✅ Files organized properly
✅ Git commit ready

Task is COMPLETE and ready for review.
```

**Cannot confirm all items? Task is NOT complete.**

## Remember

**Done means**:
- ✅ Works correctly
- ✅ Tested thoroughly
- ✅ Clean and professional
- ✅ Ready for production
- ✅ Ready for code review

**Not done means**:
- ❌ "Works on my machine"
- ❌ "Tests added later"
- ❌ "Will fix warnings later"
- ❌ "Good enough for now"

**Quality is mandatory, not optional.**

## Automated Checks (Future)

Consider adding pre-commit hooks:

```bash
# .git/hooks/pre-commit
#!/bin/sh

# Run tests
npm test || exit 1

# Run linter
npm run lint || exit 1

# Check for debug code
if grep -r "console.log\|debugger" src/; then
  echo "Error: Debug code found"
  exit 1
fi
```

**Automation catches issues** before manual review.
