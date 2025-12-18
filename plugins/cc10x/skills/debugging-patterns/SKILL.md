---
name: debugging-patterns
description: This skill should be used when the user encounters an "error", "bug", "failure", asks to "debug", "fix", "troubleshoot", or needs guidance on systematic debugging and root cause analysis.
---

# Debugging Patterns

Debug systematically with evidence-first approach. LOG FIRST, then hypothesize.

## The LOG FIRST Rule

**NEVER guess at the problem. Always gather evidence first.**

```bash
# 1. Get the actual error
npm test 2>&1 | head -50

# 2. Check logs
cat logs/error.log | tail -100

# 3. Check recent changes
git log --oneline -10
git diff HEAD~1
```

## Process

### 1. Understand What's Broken

Before debugging:

- What should happen? (expected behavior)
- What actually happens? (actual behavior)
- When did it start? (recent changes)

### 2. Gather Evidence (LOG FIRST)

Collect evidence before forming hypotheses:

```bash
# Run the failing command
npm test -- --grep "failing test" 2>&1

# Check error logs
grep -i "error\|exception\|fail" logs/*.log | tail -20

# Check recent changes
git log --oneline --since="1 day ago"
```

### 3. Form Single Hypothesis

Based on evidence, form ONE hypothesis:

- What specific thing do you think is broken?
- Why do you think that? (cite evidence)
- How would you test this hypothesis?

### 4. Test Hypothesis

Test with minimal change:

- Make the smallest change that could fix it
- Run tests to verify
- Capture exit code as evidence

### 5. Write Regression Test

After fixing:

- Add test that would have caught this bug
- Verify test fails without fix, passes with fix

## Evidence Requirements

Every debugging session must capture:

- **Error message**: Exact error text
- **Stack trace**: Where the error occurred
- **Exit codes**: Command results (exit 0 = success, exit 1 = failure)
- **Recent changes**: What changed recently

## Output Format

```markdown
## Bug Investigation

### What's Broken
- **Expected**: [what should happen]
- **Actual**: [what happens]

### Evidence
- **Error**: [exact error message]
- **Command**: [command] → exit [code]
- **Recent changes**: [relevant commits]

### Root Cause
[What failed and why, with evidence]

### Fix
- **Change**: [summary]
- **File**: [path:line]
- **Test**: [regression test added]

### Verification
- [test command] → exit 0
- Functionality: Restored
```

## Common Mistakes

1. **Guessing without evidence** - Always LOG FIRST
2. **Multiple hypotheses at once** - Test ONE hypothesis at a time
3. **No regression test** - Always add test to prevent recurrence
4. **Missing exit codes** - Capture evidence of success/failure
