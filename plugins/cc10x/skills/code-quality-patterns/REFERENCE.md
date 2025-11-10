# Code Quality Patterns - Reference

Reference materials for code quality analysis. Use AFTER understanding functionality and codebase conventions.

## Verification Before Completion

**Before marking code as complete, verify:**

```
Code Quality Verification:
- [ ] All tests passing (100% green)
- [ ] Code coverage > 80%
- [ ] No linting errors
- [ ] No type errors
- [ ] No console.log statements
- [ ] No TODO/FIXME comments
- [ ] All edge cases handled
- [ ] Error handling complete
- [ ] Performance acceptable
- [ ] Security review passed
- [ ] Documentation complete
- [ ] Ready for production
```

**Verification Checklist**:

1. Run tests: `npm test` (all passing)
2. Check coverage: `npm run coverage` (>80%)
3. Lint code: `npm run lint` (no errors)
4. Type check: `npm run type-check` (no errors)
5. Build: `npm run build` (succeeds)
6. Manual testing: Verify all features work
7. Security scan: Check for vulnerabilities
8. Performance: Verify acceptable speed
9. Documentation: Update README/comments
10. Final review: Code ready for production

## Code Quality Metrics

| Metric                | Good        | Warning | Bad   |
| --------------------- | ----------- | ------- | ----- |
| Cyclomatic Complexity | < 5         | 5-10    | > 10  |
| Function Length       | < 30 lines  | 30-50   | > 50  |
| Class Length          | < 200 lines | 200-300 | > 300 |
| Nesting Depth         | < 3         | 3-4     | > 4   |
| Code Duplication      | < 3%        | 3-5%    | > 5%  |
| Test Coverage         | > 90%       | 80-90%  | < 80% |
