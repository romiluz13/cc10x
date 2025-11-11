---
name: verification-before-completion
description: Provides evidence-first verification gate with functionality-first approach. Use PROACTIVELY before claiming completion, saying "done", "fixed", or "ready". First verifies functionality works (user flow, admin flow, system flow), then verifies other concerns. Blocks success claims without fresh verification evidence. Apply before saying "done", "fixed", or "ready".
allowed-tools: Read, Grep, Glob, Bash
---

# Verification Before Completion - Functionality First

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**CRITICAL**: Before claiming completion, verify functionality. No success claims without fresh, local evidence collected after the latest change.

## Functionality First Mandate

**BEFORE claiming completion, verify functionality**:

1. **Does functionality work?**
   - Does user flow work? (tested)
   - Does admin flow work? (tested, if applicable)
   - Does system flow work? (tested)
   - Does integration flow work? (tested, if applicable)

2. **THEN verify other concerns** - Security, quality, performance, etc.

3. **Use evidence** - Commands, exit codes, artifacts

---

## Quick Start

Verify functionality works before claiming completion.

**Example:**

1. **Identify functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Run verification**: `npm test -- --testNamePattern="file upload"` → exit 0
3. **Capture evidence**: All upload tests pass, user flow works
4. **Then verify other concerns**: Security, performance (if applicable)

**Result:** Completion claim backed by fresh verification evidence.

## Core Rule

```
No success claims without fresh, local evidence collected after the latest change.
Functionality verification is MANDATORY FIRST STEP.
```

---

## Required Actions

### Step 1: Functionality Verification (MANDATORY FIRST STEP)

**Before any other verification, verify functionality**:

1. **Identify functionality to verify**:
   - What functionality was built/fixed?
   - What are the user flows?
   - What are the admin flows?
   - What are the system flows?

2. **Verify functionality works**:
   - Run functionality tests (user flow, admin flow, system flow)
   - Capture command, arguments, exit code, and essential output
   - Map evidence to each functionality acceptance criterion

**Example**:

```bash
# Functionality verification
npm test -- --testNamePattern="file upload" -> exit 0
# Evidence: All file upload tests pass (user flow works)

npm test -- --testNamePattern="admin file list" -> exit 0
# Evidence: Admin file list tests pass (admin flow works)

npm test -- --testNamePattern="crm integration" -> exit 0
# Evidence: CRM integration tests pass (system flow works)
```

### Step 2: Other Verification (After Functionality Works)

**After functionality is verified, verify other concerns**:

1. **Identify other concerns to verify**:
   - Security (if affects functionality)
   - Quality (if affects functionality)
   - Performance (if affects functionality)

2. **Run verification commands**:
   - Run tests, lint, build, manual reproduction
   - Capture command, arguments, exit code, and essential output
   - Map evidence to each acceptance criterion

---

## Verification Summary Template

```
# Verification Summary

## Functionality Verification (MANDATORY FIRST)

### User Flow
- [ ] User flow works (tested)
- Command: <command> -> exit <code>
- Evidence: <log/report snippet>

### Admin Flow (if applicable)
- [ ] Admin flow works (tested)
- Command: <command> -> exit <code>
- Evidence: <log/report snippet>

### System Flow
- [ ] System flow works (tested)
- Command: <command> -> exit <code>
- Evidence: <log/report snippet>

### Integration Flow (if applicable)
- [ ] Integration flow works (tested)
- Command: <command> -> exit <code>
- Evidence: <log/report snippet>

## Other Verification (After Functionality Works)

Scope: <files/modules>
Criteria: <list>
Commands:
- <command> -> exit <code>
Evidence:
- <log/report snippet>
Risks / Follow-ups: <items still pending>
```

---

## Red Flags - Do Not Claim Completion If

**Functionality Red Flags**:

- Functionality not verified (user flow, admin flow, system flow)
- Functionality tests missing or failing
- Functionality broken (user can't complete tasks, system doesn't process)

**Evidence Red Flags**:

- Output and exit codes are missing or from previous runs
- Edge cases (error paths, limits, security checks) were not exercised
- The verification relies solely on remote CI without local confirmation
- Language such as "should", "probably", or "seems" replaces evidence

---

## Priority Classification

**Critical (Must Verify)**:

- Functionality works (user flow, admin flow, system flow)
- Blocks completion if functionality broken

**Important (Should Verify)**:

- Security (if affects functionality)
- Quality (if affects functionality)
- Performance (if affects functionality)

**Minor (Can Defer)**:

- Perfect test coverage (if functionality works)
- Ideal metrics (if functionality works)

---

## When to Use

**Use PROACTIVELY when**:

- Claiming completion
- Marking tasks as done
- Declaring fixes complete
- Stating readiness

**Functionality-First Process**:

1. **First**: Verify functionality works (user flow, admin flow, system flow)
2. **Then**: Verify other concerns (security, quality, performance)
3. **Then**: Produce Verification Summary with evidence
4. **Focus**: Functionality verification is mandatory, other verification is important

---

## Interaction Notes

- Workflows must invoke this skill before presenting final results
- **MANDATORY**: Functionality verification must be first step
- Subagents (builder, reviewer, verifier, investigator) include functionality verification in their hand-off
- If verification cannot be performed, state exactly why and request direction rather than assuming success

---

## Skill Overview

- **Skill**: Verification Before Completion
- **Purpose**: Evidence-first gate with functionality-first approach (not generic verification)
- **When**: Before claiming completion, marking tasks as done
- **Core Rule**: Functionality first, then other verification. Functionality verification is mandatory.

---

## Examples

### Example: Verifying File Upload Feature Completion

**Context:** Verifying file upload feature before claiming completion

**Step 1: Functionality Verification (MANDATORY FIRST)**

```bash
# Test user flow
npm test -- --testNamePattern="file upload"
# Expected: exit 0

# Test system flow
npm test -- --testNamePattern="file validation"
# Expected: exit 0

# Test integration flow
npm test -- --testNamePattern="CRM sync"
# Expected: exit 0
```

**Evidence Captured:**

```
Functionality Verified:
- [x] User flow works (tested) - Users can upload files, see progress, get confirmation
- [x] System flow works (tested) - File validation, storage, CRM sync work
- [x] Error handling works (tested) - Invalid file types, size limits, network errors handled

Commands:
- npm test -- --testNamePattern="file upload" -> exit 0
- npm test -- --testNamePattern="file validation" -> exit 0
- npm test -- --testNamePattern="CRM sync" -> exit 0
```

**Step 2: Other Verification (After Functionality)**

```bash
# Security check
npm run lint:security
# Expected: exit 0

# Code quality check
npm run lint
# Expected: exit 0
```

**Result:** Completion claim backed by fresh verification evidence showing functionality works.

## References

- Skill contract: `docs/reference/04-SKILLS.md`
- Related skills: `test-driven-development`, `verification-before-completion`

---

## Troubleshooting

**Common Issues:**

1. **Verification evidence missing or stale**
   - **Symptom**: Evidence from previous runs, not fresh
   - **Cause**: Didn't run verification commands after latest change
   - **Fix**: Run verification commands again, capture fresh evidence
   - **Prevention**: Always run verification after each change

2. **Functionality not verified first**
   - **Symptom**: Other concerns verified but functionality broken
   - **Cause**: Skipped Step 1 (Functionality Verification)
   - **Fix**: Verify functionality first, then other concerns
   - **Prevention**: Always verify functionality before other checks

3. **Evidence doesn't map to acceptance criteria**
   - **Symptom**: Evidence present but doesn't prove functionality works
   - **Cause**: Evidence doesn't match what needs verification
   - **Fix**: Map evidence to each acceptance criterion explicitly
   - **Prevention**: Always map evidence to criteria

**If issues persist:**

- Verify functionality was tested first
- Check that fresh evidence was collected
- Ensure evidence maps to acceptance criteria
- Review verification summary template

---

**Remember**: Functionality verification is mandatory. Don't claim completion without verifying functionality works!
