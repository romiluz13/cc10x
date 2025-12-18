---
name: verification-before-completion
description: This skill should be used before claiming "done", "fixed", "complete", "ready", or any completion claim. Requires fresh verification evidence before success claims.
---

# Verification Before Completion

Never claim completion without fresh verification evidence.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Before saying "done", "fixed", "complete", or "ready":

1. Run verification commands
2. Capture exit codes
3. Show evidence

## Process

### 1. Define Verification Criteria

What must be true for completion?

- Tests pass?
- Build succeeds?
- Functionality works?
- No regressions?

### 2. Run Verification Commands

```bash
# Run tests
npm test
# Expected: exit 0

# Run build
npm run build
# Expected: exit 0

# Run specific verification
npm test -- --grep "feature being completed"
# Expected: exit 0
```

### 3. Capture Evidence

For each command, capture:

- Command run
- Exit code
- Relevant output snippet

### 4. Only Then Claim Completion

With evidence in hand, claim completion.

## Verification Checklist

Before claiming completion:

- [ ] All relevant tests pass (exit 0)
- [ ] Build succeeds (exit 0)
- [ ] Feature functionality verified
- [ ] No regressions introduced
- [ ] Evidence captured for each check

## Output Format

```markdown
## Verification Summary

### Scope
[What was completed]

### Criteria
[What was verified]

### Evidence

| Check | Command | Exit Code | Result |
|-------|---------|-----------|--------|
| Tests | `npm test` | 0 | PASS |
| Build | `npm run build` | 0 | PASS |
| Feature | `npm test -- --grep "feature"` | 0 | PASS |

### Status
COMPLETE - All verifications passed with evidence
```

## Common Mistakes

1. **Claiming done without running tests** - Always run verification
2. **Missing exit codes** - Capture exit codes as evidence
3. **Stale evidence** - Evidence must be fresh (from this session)
4. **Partial verification** - Verify ALL criteria, not just some
