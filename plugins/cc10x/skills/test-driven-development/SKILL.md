---
name: test-driven-development
description: Enforces TDD with functionality-first, context-dependent approach. Use PROACTIVELY when building features. First understands functionality requirements using universal questions and context-dependent flows, then writes tests verifying that functionality, then implements code to make tests pass. Understands project test patterns and conventions. Focuses on tests that verify functionality works, not generic test coverage. Enforces the RED -> GREEN -> REFACTOR loop with mandatory command execution and verification. Provides specific test examples.
allowed-tools: Read, Grep, Glob, Bash
---

# Test-Driven Development (TDD) - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before writing tests, understand functionality using context-dependent analysis.

**Core Principle**: Understand what functionality needs to be built (using universal questions and context-dependent flows), then write tests that verify that functionality works. Tests exist to verify functionality, not for their own sake.

---

## Quick Start

Write tests by first understanding functionality, then writing tests that verify it works.

**Example:**

1. **Understand functionality**: User uploads file (User Flow: select → upload → confirm)
2. **Write failing test** (RED): `test('user can upload valid file', () => { ... })` → test fails
3. **Write minimal code** (GREEN): Implement upload functionality → test passes
4. **Refactor** (REFACTOR): Clean up code while keeping tests green

**Result:** Tests that verify functionality works, implemented through TDD cycle.

## Requirements

**Dependencies:**

- Functionality analysis template - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
- Project test patterns understanding - Must analyze existing test patterns before writing tests

**Prerequisites:**

- Step 1: Context-Dependent Functionality Analysis completed (MANDATORY FIRST STEP)
- Step 2: Project test patterns analyzed (test framework, test structure, naming conventions)

**Tool Access:**

- Required tools: Read, Grep, Glob, Bash
- Read tool: To analyze project test patterns
- Grep tool: To find similar test patterns
- Bash tool: To run tests and verify TDD cycle (RED → GREEN → REFACTOR)

**Related Skills:**

- `code-generation` - Generate code after tests written
- `verification-before-completion` - Verify tests pass before completion

**TDD Cycle Enforcement:**

- RED: Write failing test, verify it fails (Bash command required)
- GREEN: Write minimal code, verify test passes (Bash command required)
- REFACTOR: Improve code while keeping tests green (Bash command required)

---

## Examples

### Example: File Upload Feature (UI Feature)

**Context:** Building file upload component with TDD

**Functionality Flow:**

- User Flow: Select file → Upload → See progress → Get confirmation
- Error Flow: Invalid file type → Show error message

**RED - Write Failing Tests:**

```typescript
// src/components/UploadForm.test.tsx
describe('UploadForm', () => {
  it('allows user to upload valid file and shows success message', async () => {
    // Test implementation
    const mockUploadFile = uploadFile as jest.MockedFunction<typeof uploadFile>;
    mockUploadFile.mockResolvedValue('file-123');

    render(<UploadForm />);
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/drag and drop/i).closest('div')?.querySelector('input');

    if (input) {
      await userEvent.upload(input, file);
    }

    await waitFor(() => {
      expect(mockUploadFile).toHaveBeenCalledWith(file, expect.any(Function));
    });

    expect(await screen.findByText(/file uploaded successfully/i)).toBeInTheDocument();
  });

  it('shows upload progress during upload', async () => {
    // Test progress functionality
  });

  it('shows error message for invalid file type', async () => {
    // Test error handling
  });
});
```

**GREEN - Minimal Implementation:**

```typescript
// src/components/UploadForm.tsx
export function UploadForm({ onUploadSuccess }: UploadFormProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  // Minimal implementation to make tests pass
  // ...
}
```

**REFACTOR - Clean Up:**

```bash
# Run tests to verify they still pass
npm test UploadForm.test.tsx
# Expected: All tests pass

# Refactor: Extract constants, helper functions
# After each refactor, run tests again
```

**Result:** Tests verify functionality flows, aligned with project test patterns.

**See [EXAMPLES.md](EXAMPLES.md) for complete example with all test cases.**

## Step 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

### Reference Template

**Reference**: See [Functionality Analysis Template](../cc10x-orchestrator/templates/functionality-analysis.md) for complete template.

### Process

1. **Detect Code Type**: Identify if this is UI, API, Utility, Integration, Database, Configuration, CLI, or Background Job
2. **Universal Questions First**: Answer Purpose, Requirements, Constraints, Dependencies, Edge Cases, Verification, Context
3. **Context-Dependent Flows**: Answer flow questions based on code type:
   - **UI**: User Flow, Admin Flow, System Flow
   - **API**: Request Flow, Response Flow, Error Flow, Data Flow
   - **Integration**: Integration Flow, Data Flow, Error Flow, State Flow
   - **Database**: Migration Flow, Query Flow, Data Flow, State Flow
   - **Background Jobs**: Job Flow, Processing Flow, State Flow, Error Flow
   - **CLI**: Command Flow, Processing Flow, Output Flow, Error Flow
   - **Configuration**: Configuration Flow, Validation Flow, Error Flow
   - **Utility**: Input Flow, Processing Flow, Output Flow, Error Flow

### Example: File Upload to CRM (UI Feature)

**Universal Questions**:

**Purpose**: Users need to upload files to their CRM system. Files should be stored securely and accessible to authorized users.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must validate file type and size (max 10MB)
- Must store files securely in S3
- Must send file metadata to CRM API
- Must display upload progress to user
- Must handle errors gracefully

**Constraints**:

- Performance: Upload must complete within 30 seconds for files up to 10MB
- Scale: Must handle 100 concurrent uploads
- Security: Files must be encrypted at rest, access controlled
- Storage: 100GB storage limit

**Dependencies**:

- Files: `components/UploadForm.tsx`, `api/files.ts`, `services/storage.ts`, `services/crm-client.ts`
- APIs: CRM API (POST /crm/files)
- Services: S3 storage service, CRM API service
- Libraries: `aws-sdk`, `axios`, `react-dropzone`

**Edge Cases**:

- File exceeds size limit
- Invalid file type
- Network failure during upload
- CRM API unavailable
- Storage quota exceeded

**Verification**:

- E2E tests: Complete user flow from upload to CRM visibility
- Acceptance criteria: File appears in CRM within 5 seconds
- Success metrics: 99% upload success rate, <30s upload time

**Context**:

- Location: `src/features/file-upload/`
- Codebase structure: React frontend, Node.js backend, PostgreSQL database
- Architecture: MVC pattern, RESTful API

**Context-Dependent Flows (UI Feature)**:

**User Flow**:

1. User navigates to "Upload File" page
2. User selects file from device
3. User sees upload progress indicator (0% → 100%)
4. User sees success message: "File uploaded successfully"
5. User sees link to view uploaded file

**System Flow**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type and size
3. System stores file in secure storage (S3 bucket)
4. System sends file metadata to CRM API
5. System stores file record in database
6. System returns success response to user

**Integration Flow**:

1. System sends file metadata to CRM API (POST /crm/files)
2. CRM API stores file reference
3. CRM API returns file ID
4. System receives response and updates local record

---

## Step 2: Understand Project Test Patterns (BEFORE Writing Tests)

**CRITICAL**: Understand how this project writes tests before writing tests.

### Project Context Analysis

1. **Read Existing Tests**:
   - Similar test files (how are they structured?)
   - Test naming conventions (describe/it, test, it?)
   - Test organization (unit tests, integration tests, E2E tests?)
   - Mocking patterns (jest.fn, msw, nock?)

2. **Identify Test Patterns**:
   - Test framework (Jest, Vitest, Mocha, Cypress?)
   - Assertion library (expect, assert, chai?)
   - Test utilities (render, screen, userEvent?)
   - Mocking approach (manual mocks, auto mocks, MSW?)

3. **Understand Test Conventions**:
   - How are tests organized? (co-located, separate test files?)
   - How are mocks structured? (manual mocks, **mocks** folders?)
   - How are test data managed? (fixtures, factories, builders?)

### Example: Project Test Patterns

**From existing tests** (`src/components/Button.test.tsx`):

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

**Identified Patterns**:

- React Testing Library for component tests
- `describe`/`it` for test structure
- `render`/`screen` for rendering and queries
- `userEvent` for user interactions
- `jest.fn()` for mocks
- Co-located test files (`.test.tsx`)

**Conventions**:

- Tests co-located with components
- Use `screen` queries (getByRole, getByText)
- Use `userEvent` for interactions
- Mock functions with `jest.fn()`

---

## Step 3: TDD Process (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only write tests AFTER you understand functionality and project test patterns. Write tests that verify functionality works, not generic test coverage.

### Core Rule

```
No production code without a failing test first.
If code exists before the test, delete it and start from the test.
```

**Functionality-First TDD**:

1. **Understand Functionality**: What needs to be built? (context-dependent analysis)
2. **Understand Test Patterns**: How does this project write tests?
3. **RED**: Write failing test for functionality
4. **GREEN**: Write minimal code to make test pass
5. **REFACTOR**: Clean up while keeping tests green

### Functionality-Focused Test Checklist

**Priority: Critical (Core Functionality)**:

- [ ] Tests verify user flow works (user can complete tasks)
- [ ] Tests verify admin flow works (if applicable, admin can manage)
- [ ] Tests verify system flow works (system processes correctly)
- [ ] Tests verify integration flow works (if applicable, external systems work)
- [ ] Tests verify error handling works (errors handled correctly)
- [ ] Tests align with project test patterns (follows existing structure)

**Priority: Important (Supporting Functionality)**:

- [ ] Tests verify edge cases (boundary conditions)
- [ ] Tests are readable (can understand functionality being tested)

**Priority: Minor (Can Defer)**:

- [ ] Perfect test coverage (if functionality is tested)
- [ ] Ideal test structure (if functionality is tested)
- [ ] Perfect test naming (if functionality is tested)

---

## Step 4: Provide Specific Test Examples (WITH EXAMPLES)

**CRITICAL**: Provide specific, actionable test examples, not generic patterns.

For complete test examples including RED-GREEN-REFACTOR cycle with full code, see [EXAMPLES.md](EXAMPLES.md).

---

## Verification Summary Template

```
# Verification Summary

Functionality Verified:
- [ ] User flow works (tested)
- [ ] Admin flow works (if applicable, tested)
- [ ] System flow works (tested)
- [ ] Integration flow works (if applicable, tested)
- [ ] Error handling works (tested)

Tests: npm test UploadForm.test.tsx -> exit 0
New tests:
  - User can upload valid file
  - User sees upload progress
  - Error handling for invalid file type
  - Error handling for file too large
  - Error handling for network failure
  - onUploadSuccess callback called
Notes: All functionality tests passing
```

Include this block whenever reporting completion.

---

## Anti-Patterns to Avoid

- **Skipping functionality understanding**: Don't write tests without understanding functionality
- **Generic tests**: Don't write tests that don't verify functionality
- **Skipping the failing test step**: Don't assume tests would fail
- **Adding multiple behaviors in one test**: Keep tests focused on one functionality behavior
- **Writing large implementations before running tests**: Write minimal code for functionality
- **Claiming success without captured command output**: Always verify with commands
- **Ignoring project test patterns**: Don't write tests that don't align with project conventions

---

## Priority Classification

**Critical (Must Have)**:

- Tests verify core functionality (user flow, system flow, integration flow)
- Tests align with project test patterns (follows existing structure)
- Blocks functionality if missing
- Required for functionality to work

**Important (Should Have)**:

- Tests verify edge cases (boundary conditions)
- Tests are readable (can understand functionality being tested)

**Minor (Can Defer)**:

- Perfect test coverage (if functionality is tested)
- Ideal test structure (if functionality is tested)
- Perfect test naming (if functionality is tested)

---

## When to Use

**Use PROACTIVELY when**:

- Building new features
- Fixing bugs
- Refactoring code

**Functionality-First Process**:

1. **First**: Understand functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Understand project test patterns and conventions
3. **Then**: Write tests that verify functionality works (RED)
4. **Then**: Implement code to make tests pass (GREEN)
5. **Then**: Refactor while keeping tests green (REFACTOR)
6. **Focus**: Tests that verify functionality, not generic test coverage

---

## Skill Overview

- **Skill**: Test-Driven Development
- **Purpose**: Enforce TDD with functionality-first, context-dependent approach (not generic test coverage)
- **When**: Building features, fixing bugs, refactoring
- **Core Rule**: Functionality first (context-dependent analysis), then tests, then code. Understand project test patterns, then write tests aligned with patterns to verify functionality.

---

## References

- Official skills guidance: `docs/reference/04-SKILLS.md`
- Related skills: `code-generation`, `verification-before-completion`

---

## Troubleshooting

**Common Issues:**

1. **Tests don't verify functionality**
   - **Symptom**: Tests pass but functionality doesn't work
   - **Cause**: Tests written without understanding functionality first
   - **Fix**: Complete Step 1 (Functionality Analysis), rewrite tests to verify flows
   - **Prevention**: Always understand functionality before writing tests

2. **Tests don't follow project patterns**
   - **Symptom**: Tests use different patterns than existing tests
   - **Cause**: Skipped Step 2 (Understand Project Test Patterns)
   - **Fix**: Analyze existing tests, rewrite using project patterns
   - **Prevention**: Always read existing tests before writing new ones

3. **TDD cycle not followed (RED → GREEN → REFACTOR)**
   - **Symptom**: Code written before tests, or tests written after code
   - **Cause**: Skipped RED step or wrote code before test fails
   - **Fix**: Delete code, write failing test first, then implement
   - **Prevention**: Always write failing test first, verify it fails

**If issues persist:**

- Verify functionality analysis was completed first
- Check that project test patterns were analyzed
- Review EXAMPLES.md for complete TDD examples
- Ensure tests verify functionality flows

---

**Remember**: Tests exist to verify functionality works. Don't write tests generically - write tests aligned with project patterns to verify functionality! Provide specific test examples, not generic patterns.
