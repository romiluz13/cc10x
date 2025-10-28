# BUILDING Workflow - TDD Implementation

**Triggered by:** User requests feature implementation



---

## Phase 0: Complexity Gate (STRONG)

**IF Complexity <= 2:**

STOP and show strong warning:

```
⚠️ STOP: This is SIMPLE (complexity 2/5)

This is straightforward and may not require systematic analysis.

Example: Rate Limiting
- Consider implementing manually for simpler features
- Use cc10x for review and complex features

Recommendation: Consider manual approach for simple features.
```

ASK: "Continue anyway? (yes/no)"

---

## Phase 1: Load Plan (if exists)

**Check for plan:**
```bash
ls .claude/plans/FEATURE_*.md 2>/dev/null
```

IF plan exists:
- Load it for context
- Use architecture decisions
- Follow file manifest

IF no plan:
- ASK: "Want me to create plan first?"
- If YES: Invoke PLANNING workflow, then return here
- If NO: Proceed with ad-hoc implementation (less systematic)

---

## Phase 2: Invoke Implementer Agent

Follow instructions in [../../agents/implementer.md](../../agents/implementer.md)

**Agent task:**
1. Implement feature using strict TDD
2. RED-GREEN-REFACTOR cycle enforcement
3. Write test first (RED)
4. Implement minimal code (GREEN)
5. Refactor (keep tests passing)
6. Repeat for each increment

**Agent loads skills:**
- `test-driven-development` skill (TDD patterns)
- `code-generation` skill (implementation patterns)
- `risk-analysis` skill (before each increment)

**TDD Enforcement:**
- Agent MUST write test before code
- Agent MUST see test fail (RED)
- Agent MUST implement minimal solution (GREEN)
- Agent MUST refactor without breaking tests

---

## Phase 3: Mandatory Test Verification

**CRITICAL: Do NOT trust agent's "all tests passing" report!**

**User MUST manually verify:**

```
Implementation complete. Agent reports: "All tests passing"

⚠️ VERIFY BEFORE TRUSTING:

Run tests yourself:
```bash
npm test        # or pytest, cargo test, etc.
```

Check output:
- ALL tests actually pass?
- No failures hidden in output?
- Coverage meets >80% goal?

If tests FAIL:
- Use DEBUG workflow to investigate
- Agent may have reported false success

If tests PASS:
- Verify coverage: npm test -- --coverage
- Ensure >80% coverage achieved
```

**Why this step?**
- Previous testing showed agents report "tests passing" when they fail
- Manual verification prevents false confidence
- You're the final quality gate

---

## Phase 4: Invoke Test Generator (if needed)

IF coverage < 80%:

Follow instructions in [../../agents/test-generator.md](../../agents/test-generator.md)

**Agent task:**
1. Analyze coverage gaps
2. Generate additional tests
3. Target >80% coverage
4. Focus on untested edge cases

**Agent loads skills:**
- `test-driven-development` skill (test patterns)

---

## Phase 5: Return Results

**Present implementation to user:**

```
Feature implemented!

Summary:
- Files created: X
- Files modified: Y
- Tests written: Z
- Coverage: W%

⚠️ IMPORTANT: I ran tests and they pass.
BUT: Please verify yourself (run: npm test)

What next?
- Review code for quality/security?
- Deploy to staging?
- Create documentation?
```

**DO NOT automatically review or deploy!**


