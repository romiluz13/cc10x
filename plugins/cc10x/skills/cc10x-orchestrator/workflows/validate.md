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

### 1. Plan → Code Consistency

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
- ✅ IMPLEMENTED: `src/auth/register.controller.ts` (lines 12-45)
- ✅ TEST: `tests/auth/register.test.ts` (8 test cases)

REQ-F2: JWT token generation
- ✅ IMPLEMENTED: `src/auth/token.service.ts` (lines 28-67)
- ✅ TEST: `tests/auth/token.test.ts` (12 test cases)

REQ-F3: Refresh token rotation
- ❌ MISSING: No implementation found for token rotation
- ⚠️ DRIFT: Plan specified this, code doesn't implement it
```

---

### 2. Code → Tests Consistency

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
- ✅ Test file: `tests/auth/service.test.ts` (198 lines, 45 tests)
- ✅ Coverage: Functions 100%, Branches 92%, Lines 95%
- ✅ Edge cases: null input, malformed data, duplicates (all tested)

`src/auth/middleware.ts` (187 lines)
- ✅ Test file: `tests/auth/middleware.test.ts` (134 lines, 28 tests)
- ✅ Coverage: Functions 100%, Branches 88%, Lines 93%
- ⚠️ Missing: Integration test for expired token scenario

`src/auth/types.ts` (124 lines)
- ⚠️ No tests: Type-only file (acceptable)
```

---

### 3. Code → Documentation Consistency

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
- ✅ Authentication section added (lines 145-189)
- ✅ API endpoints documented
- ✅ Example usage included

API Documentation:
- ✅ `docs/api/auth.md` exists
- ✅ All endpoints documented (login, register, refresh)
- ✅ Request/response examples current

Inline Comments:
- ✅ Complex token rotation logic commented
- ✅ Security considerations noted
- ⚠️ Missing: Why we chose bcrypt cost factor 12 (should document rationale)
```

---

### 4. Risks → Mitigations Consistency

**Question:** Were identified risks actually mitigated?

**Process:**
1. Read risk assessment from plan (Phase 3b)
2. For each MEDIUM+ risk, verify mitigation implemented
3. Check code for risk prevention

**Example:**
```markdown
## Risk Mitigation Validation

RISK-01: SQL Injection (CRITICAL, Prob 3 × Impact 3 = 9)
- Mitigation planned: Use parameterized queries
- ✅ IMPLEMENTED: All database queries use Mongoose (auto-sanitized)
- ✅ VERIFIED: No raw SQL string concatenation

RISK-02: Weak Password Hashing (HIGH, 2 × 3 = 6)
- Mitigation planned: bcrypt with cost factor 12
- ✅ IMPLEMENTED: `crypto/password.ts` uses bcrypt(password, 12)
- ✅ TESTED: Hash format verified in tests

RISK-03: Token Replay Attacks (MEDIUM, 2 × 2 = 4)
- Mitigation planned: Short-lived access tokens (15 min)
- ✅ IMPLEMENTED: JWT expiry set to 900 seconds
- ❌ MISSING: Token blacklist not implemented (deferred to v2 per plan)
```

---

### 5. File Manifest → Actual Files Consistency

**Question:** Do created files match the plan?

**Process:**
1. Load File Change Manifest from plan (Phase 5b)
2. Check each planned file exists
3. Verify LOC within ±30% of estimates
4. Flag unplanned files (scope creep indicator)

**Example:**
```markdown
## File Manifest Validation

### CREATE Files

Planned: `src/auth/service.ts` (~350 lines)
Actual: `src/auth/service.ts` (352 lines)
Status: ✅ Match (variance: +0.6%)

Planned: `src/auth/middleware.ts` (~180 lines)
Actual: `src/auth/middleware.ts` (187 lines)
Status: ✅ Match (variance: +3.9%)

[...continue for all planned files...]

### MODIFY Files

Planned: `src/app.ts` (+25 lines)
Actual: `src/app.ts` (+28 lines)
Status: ✅ Match (close enough)

### Summary
- Planned files: 8
- Actual files: 9
- Unplanned: 1 file (`src/auth/constants.ts` - 45 lines)
  - Reason: Extracted magic numbers (good practice, acceptable)
  
- LOC planned: 1,200
- LOC actual: 1,104
- Variance: -8% (within ±30% ✅)

**Scope Control:** Minimal drift, one unplanned file justified
```

---

## Output Format

```markdown
## Cross-Artifact Validation Report

### Summary
- Total validations: 5
- Passing: 4 ✅
- Issues found: 3 ⚠️
- Critical issues: 0

---

## 1. Plan → Code Consistency ✅

**Requirements:**
- 12 functional requirements planned
- 12 implemented ✅
- 0 missing

**User Stories:**
- 8 stories planned
- 8 implemented ✅

**Acceptance Criteria:**
- 24 criteria planned
- 23 met ✅
- 1 deferred (documented as v2 feature)

**Status:** PASS - Code matches plan

---

## 2. Code → Tests Consistency ✅

**Test Coverage:**
- Functions: 100% ✅
- Branches: 91% ✅ (target >80%)
- Lines: 95% ✅ (target >90%)

**Test Files:**
- 8 implementation files
- 8 test files ✅
- All files have tests

**Edge Cases:**
- Risk analysis identified: 15 edge cases
- Tests cover: 14/15 ✅ (93%)
- Missing: 1 (browser-specific, needs E2E)

**Status:** PASS - Comprehensive test coverage

---

## 3. Code → Documentation Consistency ⚠️

**README:**
- ✅ Updated with auth section
- ✅ API usage examples included

**API Docs:**
- ✅ All endpoints documented

**Inline Comments:**
- ⚠️ Missing rationale for bcrypt cost factor choice
- ⚠️ Token rotation logic under-commented

**Status:** MINOR ISSUES - Add missing comments

---

## 4. Risks → Mitigations Consistency ✅

**Risks Identified:** 8 (from plan Phase 3b)

**Mitigations Implemented:**
- CRITICAL risks: 2 planned, 2 implemented ✅
- HIGH risks: 3 planned, 3 implemented ✅
- MEDIUM risks: 3 planned, 2 implemented, 1 deferred (documented) ✅

**Status:** PASS - All critical mitigations in place

---

## 5. File Manifest → Actual Consistency ✅

**Files:**
- Planned: 8 CREATE, 3 MODIFY, 0 DELETE
- Actual: 9 CREATE, 3 MODIFY, 0 DELETE
- Unplanned: 1 (constants.ts - justified)

**LOC:**
- Planned: 1,200 lines
- Actual: 1,104 lines
- Variance: -8% (within ±30% ✅)

**File Sizes:**
- Max file: 352 lines ✅ (<500 limit)
- All files within limits ✅

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

**Overall Validation:** ✅ PASS (4/5 passing, 1 minor issue)

---

## Validation Complete

Project shows strong plan-code consistency:
- ✅ All planned requirements implemented
- ✅ Comprehensive test coverage (>80%)
- ✅ Risk mitigations in place
- ✅ File manifest matches (minimal drift)
- ⚠️ Minor documentation gaps (easily fixed)

**Confidence Level:** HIGH - Safe to merge after documentation fixes
```

---

## Token Economics

**Cost:** 20k-45k tokens depending on codebase size

**Breakdown:**
- Plan loading: 2-5k
- Code scanning: 5-15k
- Test verification: 3-10k
- Risk validation: 5-10k
- Report generation: 5-10k

**Value:**
- Catches plan drift before it becomes technical debt
- Ensures requirements actually implemented
- Verifies risk mitigations in place
- Team accountability (did we do what we said?)

**Worth it when:**
- Team projects (alignment valuable)
- Complex features (verify nothing missed)
- Compliance requirements (documentation)

**Skip when:**
- Solo dev (you know what you built)
- No plan exists (nothing to validate)
- Already validated during BUILD workflow

---

## Remember

This workflow provides systematic verification that:
- **Code matches plan** (prevents drift)
- **Tests are comprehensive** (prevents bugs)
- **Documentation is current** (prevents confusion)
- **Risks are mitigated** (prevents incidents)

**Use before merge for team projects or complex features.**

**The value is in catching drift early before it becomes technical debt.**

