# VALIDATION Workflow

**Cross-Artifact Consistency Verification**

## When to Use

Use this workflow for:
- Pre-PR validation (ensure plan matches code)
- Periodic audits (check consistency)
- Team accountability (did we build what we planned?)
- Post-implementation review

**Skip for:**
- No plan exists (nothing to validate against)
- Already used BUILD workflow (includes validation)
- Solo dev who doesn't create plans

---

## Prerequisites

This workflow requires a plan file exists:
- `.claude/plans/FEATURE_[NAME].md`

If no plan exists, recommend creating one first or skip validation.

---

## Validation Dimensions

### 1. Plan âCode Consistency

**Question:** Did we build what we planned?

**Process:**
1. Read plan from `.claude/plans/FEATURE_[NAME].md`
2. Extract requirements, user stories, acceptance criteria
3. Search codebase for implementations
4. Verify each requirement has corresponding code

**Example:**
```markdown
## Requirement Validation

REQ-F1: User registration with email/password
- âIMPLEMENTED: `src/auth/register.controller.ts` (lines 12-45)
- âTEST: `tests/auth/register.test.ts` (8 test cases)

REQ-F2: JWT token generation
- âIMPLEMENTED: `src/auth/token.service.ts` (lines 28-67)
- âTEST: `tests/auth/token.test.ts` (12 test cases)

REQ-F3: Refresh token rotation
- âMISSING: No implementation found for token rotation
- â ï¸DRIFT: Plan specified this, code doesn't implement it
```

---

### 2. Code âTests Consistency

**Question:** Is implemented code comprehensively tested?

**Process:**
1. List all implemented files
2. Check for corresponding test files
3. Verify coverage >80%
4. Check edge cases from risk analysis are tested

**Example:**
```markdown
## Test Coverage Validation

`src/auth/service.ts` (352 lines)
- âTest file: `tests/auth/service.test.ts` (198 lines, 45 tests)
- âCoverage: Functions 100%, Branches 92%, Lines 95%
- âEdge cases: null input, malformed data, duplicates (all tested)

`src/auth/middleware.ts` (187 lines)
- âTest file: `tests/auth/middleware.test.ts` (134 lines, 28 tests)
- âCoverage: Functions 100%, Branches 88%, Lines 93%
- â ï¸Missing: Integration test for expired token scenario

`src/auth/types.ts` (124 lines)
- â ï¸No tests: Type-only file (acceptable)
```

---

### 3. Code âDocumentation Consistency

**Question:** Is code properly documented?

**Process:**
1. Check if README updated (if public APIs changed)
2. Verify API documentation exists
3. Check inline comments for complex logic
4. Validate examples are current

**Example:**
```markdown
## Documentation Validation

README.md:
- âAuthentication section added (lines 145-189)
- âAPI endpoints documented
- âExample usage included

API Documentation:
- â`docs/api/auth.md` exists
- âAll endpoints documented (login, register, refresh)
- âRequest/response examples current

Inline Comments:
- âComplex token rotation logic commented
- âSecurity considerations noted
- â ï¸Missing: Why we chose bcrypt cost factor 12 (should document rationale)
```

---

### 4. Risks âMitigations Consistency

**Question:** Were identified risks actually mitigated?

**Process:**
1. Read risk assessment from plan (Phase 3b)
2. For each MEDIUM+ risk, verify mitigation implemented
3. Check code for risk prevention

**Example:**
```markdown
## Risk Mitigation Validation

RISK-01: SQL Injection (CRITICAL, Prob 3 ÃImpact 3 = 9)
- Mitigation planned: Use parameterized queries
- âIMPLEMENTED: All database queries use Mongoose (auto-sanitized)
- âVERIFIED: No raw SQL string concatenation

RISK-02: Weak Password Hashing (HIGH, 2 Ã3 = 6)
- Mitigation planned: bcrypt with cost factor 12
- âIMPLEMENTED: `crypto/password.ts` uses bcrypt(password, 12)
- âTESTED: Hash format verified in tests

RISK-03: Token Replay Attacks (MEDIUM, 2 Ã2 = 4)
- Mitigation planned: Short-lived access tokens (15 min)
- âIMPLEMENTED: JWT expiry set to 900 seconds
- âMISSING: Token blacklist not implemented (deferred to v2 per plan)
```

---

### 5. File Manifest âActual Files Consistency

**Question:** Do created files match the plan?

**Process:**
1. Load File Change Manifest from plan (Phase 5b)
2. Check each planned file exists
3. Verify LOC within Â±30% of estimates
4. Flag unplanned files (scope creep indicator)

**Example:**
```markdown
## File Manifest Validation

### CREATE Files

Planned: `src/auth/service.ts` (~350 lines)
Actual: `src/auth/service.ts` (352 lines)
Status: âMatch (variance: +0.6%)

Planned: `src/auth/middleware.ts` (~180 lines)
Actual: `src/auth/middleware.ts` (187 lines)
Status: âMatch (variance: +3.9%)

[...continue for all planned files...]

### MODIFY Files

Planned: `src/app.ts` (+25 lines)
Actual: `src/app.ts` (+28 lines)
Status: âMatch (close enough)

### Summary
- Planned files: 8
- Actual files: 9
- Unplanned: 1 file (`src/auth/constants.ts` - 45 lines)
  - Reason: Extracted magic numbers (good practice, acceptable)

- LOC planned: 1,200
- LOC actual: 1,104
- Variance: -8% (within Â±30% â)

**Scope Control:** Minimal drift, one unplanned file justified
```

---

## Output Format

```markdown
## Cross-Artifact Validation Report

### Summary
- Total validations: 5
- Passing: 4 â
- Issues found: 3 â ï¸
- Critical issues: 0

---

## 1. Plan âCode Consistency â

**Requirements:**
- 12 functional requirements planned
- 12 implemented â
- 0 missing

**User Stories:**
- 8 stories planned
- 8 implemented â

**Acceptance Criteria:**
- 24 criteria planned
- 23 met â
- 1 deferred (documented as v2 feature)

**Status:** PASS - Code matches plan

---

## 2. Code âTests Consistency â

**Test Coverage:**
- Functions: 100% â
- Branches: 91% â(target >80%)
- Lines: 95% â(target >90%)

**Test Files:**
- 8 implementation files
- 8 test files â
- All files have tests

**Edge Cases:**
- Risk analysis identified: 15 edge cases
- Tests cover: 14/15 â(93%)
- Missing: 1 (browser-specific, needs E2E)

**Status:** PASS - Comprehensive test coverage

---

## 3. Code âDocumentation Consistency â ï¸

**README:**
- âUpdated with auth section
- âAPI usage examples included

**API Docs:**
- âAll endpoints documented

**Inline Comments:**
- â ï¸Missing rationale for bcrypt cost factor choice
- â ï¸Token rotation logic under-commented

**Status:** MINOR ISSUES - Add missing comments

---

## 4. Risks âMitigations Consistency â

**Risks Identified:** 8 (from plan Phase 3b)

**Mitigations Implemented:**
- CRITICAL risks: 2 planned, 2 implemented â
- HIGH risks: 3 planned, 3 implemented â
- MEDIUM risks: 3 planned, 2 implemented, 1 deferred (documented) â

**Status:** PASS - All critical mitigations in place

---

## 5. File Manifest âActual Consistency â

**Files:**
- Planned: 8 CREATE, 3 MODIFY, 0 DELETE
- Actual: 9 CREATE, 3 MODIFY, 0 DELETE
- Unplanned: 1 (constants.ts - justified)

**LOC:**
- Planned: 1,200 lines
- Actual: 1,104 lines
- Variance: -8% (within Â±30% â)

**File Sizes:**
- Max file: 352 lines â(<500 limit)
- All files within limits â

**Status:** PASS - Minimal scope drift

---

## Issues Requiring Attention

### Minor Issues (Fix Before Merge)

1. **Add comment explaining bcrypt cost factor**
   - File: `src/crypto/password.ts`
   - Line: 12
   - Action: Document why cost factor 12 chosen

2. **Add comments to token rotation logic**
   - File: `src/auth/service.ts`
   - Lines: 78-95
   - Action: Explain refresh token rotation strategy

3. **Add E2E test for browser-specific scenario**
   - Missing: Token handling in browser storage
   - Action: Create Cypress/Playwright test (or defer to integration testing)

### No Critical Issues

All CRITICAL and HIGH priority items validated successfully.

---

## Recommendations

1. **Fix minor documentation gaps** (15 min)
2. **Consider E2E test** for browser scenario (30 min or defer)
3. **Ready to merge** after documentation fixes

**Overall Validation:** âPASS (4/5 passing, 1 minor issue)

---

## Validation Complete

Project shows strong plan-code consistency:
- âAll planned requirements implemented
- âComprehensive test coverage (>80%)
- âRisk mitigations in place
- âFile manifest matches (minimal drift)
- â ï¸Minor documentation gaps (easily fixed)

**Confidence Level:** HIGH - Safe to merge after documentation fixes
```

---


---

## Remember

This workflow provides systematic verification that:
- **Code matches plan** (prevents drift)
- **Tests are comprehensive** (prevents bugs)
- **Documentation is current** (prevents confusion)
- **Risks are mitigated** (prevents incidents)

**Use before merge for team projects or complex features.**

**The value is in catching drift early before it becomes technical debt.**

