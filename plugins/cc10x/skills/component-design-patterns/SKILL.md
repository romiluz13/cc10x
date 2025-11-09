---
name: component-design-patterns
description: Context-aware component design that understands component requirements from flows before designing. Use PROACTIVELY when planning features that need UI components. First understands functionality requirements and maps them to component needs, then designs component hierarchy to support that functionality. Provides specific component designs with examples aligned with project component patterns. Focuses on components that enable functionality, not generic component patterns.
allowed-tools: Read, Grep, Glob
---

# Component Design Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware component design that understands component requirements from flows before designing. It maps functionality to components and designs components to support functionality, providing specific component designs with examples aligned with project component patterns.

**Unique Value**:

- Understands component requirements before designing
- Designs components to support functionality
- Provides specific component designs with examples
- Understands project's component patterns

**When to Use**:

- When planning features that need UI components
- When designing component architecture
- When reviewing component interfaces

---

## Functionality First Mandate

**BEFORE designing components, complete context-dependent functionality analysis**:

1. **Complete Phase 1: Universal Questions** (from functionality analysis template):
   - Purpose: What problem does this solve?
   - Requirements: What must it do?
   - Constraints: What are the limits? (Component constraints: accessibility, performance)
   - Dependencies: What does it need? (UI libraries, state management)
   - Edge Cases: What can go wrong? (Component error cases)
   - Verification: How do we know it works? (Component tests)
   - Context: Where does it fit?

2. **Complete Phase 2: Context-Dependent Flow Questions** (based on code type - UI Features):
   - User Flow: Step-by-step how users interact with the feature
   - Admin Flow: Step-by-step how admins manage the feature (if applicable)
   - System Flow: Step-by-step how the system processes user actions

3. **THEN understand project's component patterns** - Before designing components

4. **THEN design components** - Design component hierarchy to support functionality

**Reference**: See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.

---

## Process

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any component design, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions (especially Constraints - component constraints)
   - Complete Phase 2: Context-Dependent Flow Questions (UI Features - User Flow, Admin Flow, System Flow)

2. **Understand Functionality**:
   - What is this feature supposed to do?
   - What functionality does user need?
   - What are the user flows? (Step-by-step user interactions)

3. **Understand Component Requirements** (from flows):
   - What UI components are needed? (from User Flow)
   - What admin components are needed? (from Admin Flow)
   - What data flow is needed? (from System Flow)

**Example**: File Upload to CRM

**Purpose**: Users need to upload files to their CRM system via UI.

**Requirements**:

- Must accept file uploads (PDF, DOCX, JPG, PNG)
- Must display upload progress
- Must show success/error feedback
- Must allow admins to view, download, and delete files

**User Flow**:

1. User sees "Upload File" button
2. User clicks button
3. User selects file from device
4. User sees upload progress (0% → 100%)
5. User sees success message with file link
6. User clicks link to view file

**Admin Flow**:

1. Admin sees file list
2. Admin can filter by user/date/type
3. Admin can download files
4. Admin can delete files

---

### Phase 2: Understand Project's Component Patterns (MANDATORY SECOND STEP)

**Before designing components, understand how this project designs components**:

1. **Load Project Context Understanding**:
   - Load `project-context-understanding` skill
   - Map project's component patterns (composition, props, state)
   - Identify component conventions used
   - Identify UI library/framework used
   - Identify state management patterns used

2. **Map Component Patterns**:

   ```bash
   # Find component structure
   find src/components -type f -name "*.tsx" | head -20

   # Find component patterns
   grep -r "interface.*Props\|type.*Props" --include="*.tsx" | head -20

   # Find state management patterns
   grep -r "useState\|useReducer\|redux\|zustand" --include="*.tsx" | head -20
   ```

3. **Map Component Conventions**:

   ```bash
   # Find component naming conventions
   ls -R src/components | grep -E "\.(tsx|jsx)$"

   # Find component composition patterns
   grep -r "children\|render\|slot" --include="*.tsx" | head -20

   # Find UI library patterns
   grep -r "import.*from.*@mui\|import.*from.*antd\|import.*from.*chakra" --include="*.tsx" | head -20
   ```

**Document Project's Component Patterns**:

- Component Structure: Functional components, class components, hooks
- Component Naming: PascalCase, kebab-case, etc.
- Props Patterns: Interface definitions, prop types, default props
- State Management: useState, useReducer, Redux, Zustand, etc.
- UI Library: Material UI, Ant Design, Chakra UI, custom, etc.
- Composition Patterns: Compound components, render props, children, etc.

**Example Output**:

```
Project Component Patterns:
Component Structure:
- Functional components with hooks
- TypeScript interfaces for props
- Custom hooks for logic

Component Naming:
- PascalCase for components (UploadForm)
- kebab-case for files (upload-form.tsx)

Props Patterns:
- Interface definitions (interface UploadFormProps)
- Required vs optional props
- Default props for optional values

State Management:
- useState for local state
- useReducer for complex state
- Context API for shared state

UI Library:
- Material UI (MUI) components
- Custom components in components/ui/

Composition Patterns:
- Compound components for related components
- Render props for flexible composition
- Children prop for wrapper components
```

---

### Phase 3: Component Design (Design to Support Functionality)

**After understanding functionality and project component patterns, design components**:

1. **Map Functionality to Components**:
   - For each functionality flow, identify component needs
   - Map user flows → components (UI components for user interactions)
   - Map admin flows → components (UI components for admin interactions)
   - Map system flows → components (components for system processing)

2. **Design Component Hierarchy** (based on functionality):
   - Design parent-child relationships aligned with functionality flows
   - Design component composition aligned with functionality needs
   - Design component boundaries aligned with functionality responsibilities

3. **Design Component Interfaces** (based on functionality):
   - Design props aligned with functionality needs
   - Design state aligned with functionality requirements
   - Design events aligned with functionality flows

4. **Design Component Contracts** (based on functionality):
   - Design input contracts (props, events)
   - Design output contracts (rendered output, callbacks)
   - Design state contracts (internal state, external state)

**Provide Specific Component Designs with Examples**:

For each component, provide:

- **Component**: Component name and purpose
- **Purpose**: Functionality it supports
- **Props**: Props interface with examples (aligned with project patterns)
- **State**: State management (aligned with project patterns)
- **Hierarchy**: Parent-child relationships
- **Flow Step**: Which functionality flow step it supports
- **Example**: Specific component code example (aligned with project patterns)

**Example**:

````markdown
## Component: UploadForm

**Purpose**: Supports user flow - file upload functionality

**Functionality Flow Step**: User Flow Steps 1-5 (button click → file selection → progress → success)

**Props** (aligned with project interface pattern):

```typescript
interface UploadFormProps {
  onUpload: (file: File) => Promise<void>; // User Flow Step 3: file selection
  onProgress?: (progress: number) => void; // User Flow Step 4: progress
  onSuccess?: (fileId: string) => void; // User Flow Step 5: success
  onError?: (error: string) => void; // Error handling
  maxSize?: number; // Constraint: max file size
  acceptedTypes?: string[]; // Constraint: accepted file types
}
```
````

**State** (aligned with project useState pattern):

```typescript
const [file, setFile] = useState<File | null>(null);
const [uploading, setUploading] = useState(false);
const [progress, setProgress] = useState(0);
const [error, setError] = useState<string | null>(null);
```

**Component Code** (aligned with project functional component + MUI pattern):

```tsx
import { Button, LinearProgress, Alert } from "@mui/material";
import { useState } from "react";

export function UploadForm({
  onUpload,
  onProgress,
  onSuccess,
  onError,
  maxSize = 10 * 1024 * 1024,
  acceptedTypes = ["application/pdf", "image/jpeg", "image/png"],
}: UploadFormProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (selectedFile: File) => {
    // Validate file type
    if (!acceptedTypes.includes(selectedFile.type)) {
      setError("Invalid file type");
      return;
    }
    // Validate file size
    if (selectedFile.size > maxSize) {
      setError("File exceeds size limit");
      return;
    }
    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setProgress(0);
    try {
      await onUpload(file);
      onSuccess?.("file_123");
      setFile(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Upload failed";
      setError(errorMessage);
      onError?.(errorMessage);
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept={acceptedTypes.join(",")}
        onChange={(e) =>
          e.target.files?.[0] && handleFileSelect(e.target.files[0])
        }
        disabled={uploading}
      />
      {uploading && <LinearProgress variant="determinate" value={progress} />}
      {error && <Alert severity="error">{error}</Alert>}
      <Button onClick={handleUpload} disabled={!file || uploading}>
        {uploading ? "Uploading..." : "Upload File"}
      </Button>
    </div>
  );
}
```

**Priority**: Critical (core functionality)

````

---

## Component Design Pattern Library (Reference - Use AFTER Understanding Functionality and Project Component Patterns)

### Component Structure

**Design structure to support functionality** (aligned with project patterns):

**Component Props** (mapped from functionality flows):
```tsx
// Component: UploadForm (supports user flow)
interface UploadFormProps {
  onUpload: (file: File) => Promise<void>; // User Flow Step 3: file selection
  onProgress?: (progress: number) => void; // User Flow Step 4: progress
  onSuccess?: (fileId: string) => void; // User Flow Step 5: success
  onError?: (error: string) => void; // Error handling
}

// Component: FileList (supports admin flow)
interface FileListProps {
  files: File[]; // Admin Flow Step 1: file list
  onFilter?: (filter: Filter) => void; // Admin Flow Step 2: filter
  onDownload?: (fileId: string) => void; // Admin Flow Step 3: download
  onDelete?: (fileId: string) => void; // Admin Flow Step 4: delete
}
````

### Component Hierarchy

**Design hierarchy to support functionality** (aligned with project structure):

**Component Hierarchy** (mapped from functionality flows):

```
App
├── UploadPage (User Flow)
│   ├── UploadForm (User Flow Steps 1-5)
│   │   ├── FileInput (User Flow Step 2: file selection)
│   │   ├── UploadProgress (User Flow Step 4: progress)
│   │   └── SuccessMessage (User Flow Step 5: success)
│   └── FileViewer (User Flow Step 6: view file)
└── AdminPage (Admin Flow)
    ├── FileList (Admin Flow Steps 1-4)
    │   ├── FileFilters (Admin Flow Step 2: filter)
    │   └── FileCard[] (Admin Flow Step 1: file display)
    └── FileActions (Admin Flow Steps 3-4: download, delete)
```

### Component Composition

**Design composition to support functionality** (aligned with project composition patterns):

**Compound Components** (if project uses compound components):

```tsx
// Compound Components (aligned with project pattern)
<UploadForm>
  <UploadForm.Input />
  <UploadForm.Progress />
  <UploadForm.Success />
</UploadForm>
```

**Render Props** (if project uses render props):

```tsx
// Render Props (aligned with project pattern)
<FileList>
  {({ files, filter, download, delete }) => (
    <FileCardList files={files} />
  )}
</FileList>
```

**Children Pattern** (if project uses children):

```tsx
// Children Pattern (aligned with project pattern)
<UploadForm>
  <FileInput />
  <UploadProgress />
  <SuccessMessage />
</UploadForm>
```

### State Management

**Design state to support functionality** (aligned with project state patterns):

**Local State** (aligned with project useState pattern):

```tsx
// Local state for component (aligned with project pattern)
const [file, setFile] = useState<File | null>(null);
const [uploading, setUploading] = useState(false);
const [progress, setProgress] = useState(0);
```

**Shared State** (aligned with project state management pattern):

```tsx
// Shared state (aligned with project Context/Redux pattern)
const { files, uploadFile } = useFileContext();
// OR
const files = useSelector((state) => state.files);
const dispatch = useDispatch();
```

---

## Component Checklist

### Structure & API

- [ ] Single responsibility (one reason to change)
- [ ] Clear props interface (typed + documented)
- [ ] Sensible defaults and minimal required props
- [ ] Controlled vs uncontrolled usage is explicit

### Reusability & Composition

- [ ] Composition patterns (slots, render props, compound components) when appropriate
- [ ] No hardcoded values or strings; use tokens/config
- [ ] Styles themable and responsive

### Quality & Accessibility

- [ ] Keyboard navigation and focus states
- [ ] ARIA roles/labels as needed
- [ ] Performance: memoization where it matters; avoid unnecessary re-renders
- [ ] Tests exist (unit + basic interactions)

### Examples

**Typed Props**:

```ts
interface ButtonProps {
  variant?: "primary" | "secondary" | "link";
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

**Compound Components**:

```tsx
<Button>
  <Button.Icon />
  <Button.Label>Save</Button.Label>
</Button>
```

**Controlled vs Uncontrolled**:

- Controlled: value, onChange; Uncontrolled: defaultValue, ref

---

## Priority Classification

**Critical (Must Have - Core Functionality)**:

- Components support core functionality (user flow, admin flow)
- Blocks functionality if missing
- Required for functionality to work
- Examples:
  - Components for user interactions (upload form, progress)
  - Components for admin interactions (file list, filters)
  - Component hierarchy supporting functionality flows

**Important (Should Have - Supporting Functionality)**:

- Components support functionality growth
- Components support functionality changes
- Components support functionality accessibility
- Examples:
  - Reusable components (if supports functionality)
  - Accessible components (if supports functionality)
  - Testable components (if supports functionality)

**Minor (Can Defer - Pattern Compliance)**:

- Perfect component structure (if functionality is supported)
- Ideal composition patterns (if functionality is supported)
- Perfect prop types (if functionality is supported)

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Component Design Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Project Component Patterns Summary

[Brief summary of project component patterns from Phase 2]

## Component Design

### Components

[For each component:]

- **Component**: [Name and purpose]
- **Purpose**: [Functionality it supports]
- **Props**: [Props interface with examples]
- **State**: [State management]
- **Hierarchy**: [Parent-child relationships]
- **Flow Step**: [Which functionality flow step it supports]
- **Example**: [Specific component code example]
- **Priority**: [Critical, Important, or Minor]

### Component Hierarchy

[Component hierarchy mapped from functionality flows]

### Component Contracts

[Component interfaces and contracts aligned with functionality]

## Recommendations

[Prioritized list of component designs - Critical first, then Important, then Minor]
```

---

## Usage Guidelines

### For Planning Workflow

1. **First**: Complete Phase 1 (Context-Dependent Functionality Analysis - especially User/Admin Flows)
2. **Then**: Complete Phase 2 (Understand Project Component Patterns)
3. **Then**: Complete Phase 3 (Component Design - Design to Support Functionality)
4. **Focus**: Components that enable functionality, not generic component patterns

### Key Principles

1. **Functionality First**: Always understand functionality before designing components
2. **Context-Aware**: Understand project component patterns before designing
3. **Map Flows to Components**: Map functionality flows to component hierarchy
4. **Specific Designs**: Provide specific component designs with examples aligned with project patterns
5. **Prioritize by Impact**: Critical (core functionality) > Important (supporting functionality) > Minor (pattern compliance)

---

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to component design
2. **Ignoring Project Patterns**: Don't design without understanding project component patterns
3. **Generic Component Patterns**: Don't apply generic patterns - design to support functionality
4. **Missing Specific Designs**: Don't just describe components - provide specific code examples aligned with project patterns
5. **No Flow Mapping**: Don't just list components - map them to functionality flows
6. **Wrong Priority**: Don't prioritize pattern compliance over functionality support

---

_This skill enables context-aware component design that understands component requirements from flows and designs components to support functionality, providing specific component designs with examples aligned with project component patterns._
