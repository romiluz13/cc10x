---
name: code-generation
description: Generates code with functionality-first, context-dependent approach. Use PROACTIVELY when building features. First understands functionality requirements using universal questions and context-dependent flows, then generates code aligned with project patterns to implement that functionality. Understands project codebase structure, conventions, and patterns. Focuses on making functionality work first, then optimizing. Provides specific implementations with examples.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Generation - Functionality First, Context-Dependent

## Functionality First Mandate

**CRITICAL**: Before generating code, understand functionality using context-dependent analysis.

**Core Principle**: Understand what functionality needs to be built (using universal questions and context-dependent flows), then generate code aligned with project patterns to implement that functionality. Code exists to implement functionality, not for its own sake.

---

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

## Step 2: Understand Project Patterns (BEFORE Generating Code)

**CRITICAL**: Understand how this project structures code before generating code.

### Project Context Analysis

1. **Read Existing Code**:
   - Similar components/services/utilities (how are they structured?)
   - Naming conventions (camelCase, PascalCase, kebab-case?)
   - File organization (feature-based, layer-based, type-based?)
   - Import patterns (relative paths, absolute paths, aliases?)

2. **Identify Project Patterns**:
   - Component structure (functional components, class components, hooks?)
   - Service structure (classes, functions, modules?)
   - Error handling (try-catch, Result types, error boundaries?)
   - State management (local state, context, Redux, Zustand?)

3. **Understand Project Conventions**:
   - How are features organized? (feature folders, shared folders?)
   - How are APIs structured? (REST, GraphQL, RPC?)
   - How are tests written? (Jest, Vitest, unit tests, integration tests?)

### Example: Project Patterns

**From existing code** (`src/components/Button.tsx`):

```typescript
import React from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
  children: React.ReactNode;
}

export function Button({ variant = 'primary', onClick, children }: ButtonProps) {
  return (
    <button
      className={cn('btn', variant === 'primary' ? 'btn-primary' : 'btn-secondary')}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

**Identified Patterns**:

- Functional components with TypeScript interfaces
- Props destructuring with default values
- `cn` utility for className composition
- Path alias `@/lib/utils`
- Named exports

**Conventions**:

- Components in `src/components/`
- Utilities in `src/lib/`
- TypeScript interfaces for props
- Named exports for components

---

## Step 3: Generate Code (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only generate code AFTER you understand functionality and project patterns. Generate code aligned with project patterns to implement functionality.

### Functionality-Focused Code Checklist

**Priority: Critical (Core Functionality)**:

- [ ] Code implements user flow (user can complete tasks)
- [ ] Code implements admin flow (if applicable, admin can manage)
- [ ] Code implements system flow (system processes correctly)
- [ ] Code implements integration flow (if applicable, external systems work)
- [ ] Code implements error handling (errors handled correctly)
- [ ] Code aligns with project patterns (follows existing structure)

**Priority: Important (Supporting Functionality)**:

- [ ] Code handles edge cases (boundary conditions)
- [ ] Code is readable (can understand functionality)
- [ ] Code is testable (can test functionality)

**Priority: Minor (Can Defer)**:

- [ ] Perfect code structure (if functionality works)
- [ ] Ideal design patterns (if functionality works)
- [ ] Perfect error handling (if functionality works)

---

---

## Reference Materials

**For detailed examples and checklist, see:**

- **EXAMPLES.md**: Complete code generation examples (File Upload to CRM implementation)
- **REFERENCE.md**: Code Generation Checklist

---

---

## Priority Classification

**Critical (Must Have)**:

- Code implements core functionality (user flow, system flow, integration flow)
- Code aligns with project patterns (follows existing structure)
- Blocks functionality if missing
- Required for functionality to work

**Important (Should Have)**:

- Code supports functionality growth
- Code supports functionality changes
- Code supports functionality reliability
- Code is readable and testable

**Minor (Can Defer)**:

- Perfect code structure (if functionality works)
- Ideal design patterns (if functionality works)
- Perfect error handling (if functionality works)

---

## When to Use

**Use PROACTIVELY when**:

- Implementing new functionality
- Refactoring existing code
- Building features

**Functionality-First Process**:

1. **First**: Understand functionality using context-dependent analysis (universal questions + context-dependent flows)
2. **Then**: Understand project patterns and conventions
3. **Then**: Generate code aligned with project patterns to implement functionality
4. **Then**: Make functionality work first, then optimize
5. **Focus**: Code that implements functionality, not generic code patterns

---

## Skill Overview

- **Skill**: Code Generation
- **Purpose**: Generate code with functionality-first, context-dependent approach (not generic code patterns)
- **When**: Building features, refactoring code
- **Core Rule**: Functionality first (context-dependent analysis), then code. Understand project patterns, then generate code aligned with patterns to implement functionality.

---

## References

- [Code Generation Playbook](PLAYBOOK.md) - Detailed patterns (use AFTER functionality understood)
- Related skills: `test-driven-development`, `code-quality-patterns`, `security-patterns`

---

**Remember**: Code exists to implement functionality. Don't generate code generically - generate code aligned with project patterns to implement functionality! Provide specific implementations with examples, not generic patterns.
