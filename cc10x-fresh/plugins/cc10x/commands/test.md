---
description: Write and run comprehensive tests (unit, integration, e2e)
argument-hint: [test-type] [target-files]
---

# Testing Workflow

You are creating comprehensive test coverage.

## Context
- Target: $ARGUMENTS
- Existing tests: !`find . -type f \( -name "*.test.*" -o -name "*_test.*" \) | wc -l`
- Test framework: !`cat package.json 2>/dev/null | grep -E "(jest|vitest|pytest|mocha)" || echo "Detect from project"`

## Your Task

### Phase 1: Test Strategy
Ask user: "What type of tests?"
- **Unit**: Individual functions/classes
- **Integration**: Component interactions
- **E2E**: Full user workflows
- **All**: Comprehensive coverage

### Phase 2: Test Planning
1. Identify test scenarios
2. List edge cases
3. Define expected behaviors
4. Plan test data/fixtures

### Phase 3: Test Writing
Write tests with:
- Clear descriptions
- Arrange-Act-Assert pattern
- Comprehensive assertions
- Edge case coverage
- Error scenario testing

### Phase 4: Execution
1. Run tests
2. Collect results
3. Report coverage
4. Identify gaps

### Phase 5: Fix & Iterate
IF tests fail:
- Analyze failures
- Fix code or tests
- Re-run
- Loop until all pass

## Test Quality Checklist
- [ ] All happy paths covered
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] Null/undefined handled
- [ ] Boundary conditions tested
- [ ] Integration points verified
- [ ] Performance acceptable

## Output
```markdown
# Test Results

## Coverage
- Unit: X%
- Integration: Y%
- E2E: Z%
- Overall: W%

## Results
- ✅ Passed: N
- ❌ Failed: M
- ⏭️ Skipped: K

## Gaps
- [List any uncovered scenarios]

## Recommendations
- [Suggest additional tests if needed]
```

