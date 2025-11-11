# Component Design Patterns & Examples

**Reference**: Part of `component-design-patterns` skill. See main SKILL.md for overview.

## Phase 3: Component Design (Design to Support Functionality)

**CRITICAL**: After understanding functionality and project component patterns, design components to support functionality.

## Component Design Process

### 1. Map Functionality to Components

**For each functionality flow, identify component needs**:

- Map user flows → components (UI components for user interactions)
- Map admin flows → components (UI components for admin interactions)
- Map system flows → components (components for system processing)

### 2. Design Component Hierarchy

**Design parent-child relationships** aligned with functionality flows:

- Design component composition aligned with functionality needs
- Design component boundaries aligned with functionality responsibilities

### 3. Design Component Interfaces

**Design props, state, events** aligned with functionality needs:

- Props aligned with functionality requirements
- State aligned with functionality requirements
- Events aligned with functionality flows

### 4. Design Component Contracts

**Design input/output/state contracts**:

- Input contracts (props, events)
- Output contracts (rendered output, callbacks)
- State contracts (internal state, external state)

## Component Design Example

**Component: UploadForm**

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

## Component Design Checklist

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

## Common Patterns

**Typed Props**:

```typescript
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

- Controlled: value, onChange
- Uncontrolled: defaultValue, ref

---

**See Also**: `references/functionality-mapping.md` for functionality analysis, `references/project-patterns.md` for project patterns.
