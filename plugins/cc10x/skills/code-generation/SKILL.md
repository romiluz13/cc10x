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

## Step 4: Provide Specific Implementations (WITH EXAMPLES)

**CRITICAL**: Provide specific, actionable code implementations with examples, not generic patterns.

### Example: File Upload to CRM (UI Feature)

**Based on Functionality Analysis and Project Patterns**:

**1. UploadForm Component** (implements User Flow):

```typescript
// src/components/UploadForm.tsx
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadFile } from '@/api/files';
import { cn } from '@/lib/utils';

interface UploadFormProps {
  onUploadSuccess?: (fileId: string) => void;
}

export function UploadForm({ onUploadSuccess }: UploadFormProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    onDrop: async (acceptedFiles) => {
      if (acceptedFiles.length === 0) return;

      const file = acceptedFiles[0];
      setUploading(true);
      setProgress(0);
      setError(null);

      try {
        const fileId = await uploadFile(file, (progressPercent) => {
          setProgress(progressPercent);
        });

        setUploading(false);
        setProgress(100);
        onUploadSuccess?.(fileId);
      } catch (err) {
        setUploading(false);
        setError(err instanceof Error ? err.message : 'Upload failed');
      }
    },
    onDropRejected: (rejectedFiles) => {
      const rejection = rejectedFiles[0];
      if (rejection.errors.some(e => e.code === 'file-too-large')) {
        setError('File exceeds 10MB limit');
      } else if (rejection.errors.some(e => e.code === 'file-invalid-type')) {
        setError('File type not supported. Only PDF, DOCX, JPG, PNG allowed.');
      } else {
        setError('File upload rejected');
      }
    }
  });

  return (
    <div className="upload-form">
      <div
        {...getRootProps()}
        className={cn(
          'upload-dropzone',
          isDragActive && 'upload-dropzone-active',
          uploading && 'upload-dropzone-disabled'
        )}
      >
        <input {...getInputProps()} disabled={uploading} />
        {uploading ? (
          <div className="upload-progress">
            <div className="progress-bar" style={{ width: `${progress}%` }} />
            <span>Uploading... {progress}%</span>
          </div>
        ) : (
          <div className="upload-prompt">
            <p>Drag and drop a file here, or click to select</p>
            <p className="upload-hint">PDF, DOCX, JPG, PNG up to 10MB</p>
          </div>
        )}
      </div>

      {error && (
        <div className="upload-error" role="alert">
          {error}
        </div>
      )}

      {progress === 100 && !error && (
        <div className="upload-success">
          File uploaded successfully!
        </div>
      )}
    </div>
  );
}
```

**2. File Upload API** (implements System Flow):

```typescript
// src/api/files.ts
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api";

export interface UploadProgress {
  loaded: number;
  total: number;
}

export async function uploadFile(
  file: File,
  onProgress?: (progressPercent: number) => void,
): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post<{ fileId: string }>(
      `${API_BASE_URL}/files/upload`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total && onProgress) {
            const progressPercent = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total,
            );
            onProgress(progressPercent);
          }
        },
        timeout: 30000, // 30 seconds
      },
    );

    return response.data.fileId;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === "ECONNABORTED") {
        throw new Error("Upload timeout. Please try again.");
      }
      if (error.response?.status === 413) {
        throw new Error("File exceeds size limit.");
      }
      if (error.response?.status === 415) {
        throw new Error("File type not supported.");
      }
      throw new Error(error.response?.data?.message || "Upload failed");
    }
    throw error;
  }
}
```

**3. File Service** (implements System Flow):

```typescript
// src/services/storage.ts
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { v4 as uuidv4 } from "uuid";

const s3Client = new S3Client({
  region: process.env.AWS_REGION || "us-east-1",
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

const BUCKET_NAME = process.env.AWS_S3_BUCKET!;

export interface FileMetadata {
  id: string;
  name: string;
  type: string;
  size: number;
  url: string;
  uploadedAt: Date;
}

export async function storeFile(file: File): Promise<FileMetadata> {
  const fileId = uuidv4();
  const fileExtension = file.name.split(".").pop();
  const key = `uploads/${fileId}.${fileExtension}`;

  try {
    await s3Client.send(
      new PutObjectCommand({
        Bucket: BUCKET_NAME,
        Key: key,
        Body: await file.arrayBuffer(),
        ContentType: file.type,
        ServerSideEncryption: "AES256",
      }),
    );

    const url = `https://${BUCKET_NAME}.s3.amazonaws.com/${key}`;

    return {
      id: fileId,
      name: file.name,
      type: file.type,
      size: file.size,
      url,
      uploadedAt: new Date(),
    };
  } catch (error) {
    throw new Error(
      `Failed to store file: ${error instanceof Error ? error.message : "Unknown error"}`,
    );
  }
}
```

**4. CRM Client** (implements Integration Flow):

```typescript
// src/services/crm-client.ts
import axios from "axios";

const CRM_API_URL = process.env.CRM_API_URL!;
const CRM_API_KEY = process.env.CRM_API_KEY!;

export interface CRMFileMetadata {
  name: string;
  type: string;
  size: number;
  url: string;
  uploadedAt: string;
}

export interface CRMFileResponse {
  fileId: string;
  status: "success" | "error";
  message?: string;
}

export async function syncFileToCRM(
  metadata: CRMFileMetadata,
): Promise<string> {
  let retries = 3;
  let lastError: Error | null = null;

  while (retries > 0) {
    try {
      const response = await axios.post<CRMFileResponse>(
        `${CRM_API_URL}/files`,
        metadata,
        {
          headers: {
            Authorization: `Bearer ${CRM_API_KEY}`,
            "Content-Type": "application/json",
          },
          timeout: 5000,
        },
      );

      if (response.data.status === "success") {
        return response.data.fileId;
      }

      throw new Error(response.data.message || "CRM API returned error");
    } catch (error) {
      lastError = error instanceof Error ? error : new Error("Unknown error");
      retries--;

      if (retries > 0) {
        // Exponential backoff
        await new Promise((resolve) =>
          setTimeout(resolve, Math.pow(2, 3 - retries) * 1000),
        );
      }
    }
  }

  throw new Error(
    `Failed to sync file to CRM after retries: ${lastError?.message}`,
  );
}
```

**5. Backend API Route** (implements System Flow):

```typescript
// src/api/routes/files.ts
import { Router } from "express";
import multer from "multer";
import { storeFile } from "@/services/storage";
import { syncFileToCRM } from "@/services/crm-client";
import { db } from "@/lib/db";

const router = Router();
const upload = multer({
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "image/jpeg",
      "image/png",
    ];

    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error("File type not supported"));
    }
  },
});

router.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file provided" });
    }

    // Store file
    const fileMetadata = await storeFile(req.file);

    // Sync to CRM
    const crmFileId = await syncFileToCRM({
      name: fileMetadata.name,
      type: fileMetadata.type,
      size: fileMetadata.size,
      url: fileMetadata.url,
      uploadedAt: fileMetadata.uploadedAt.toISOString(),
    });

    // Store in database
    await db.files.create({
      id: fileMetadata.id,
      name: fileMetadata.name,
      type: fileMetadata.type,
      size: fileMetadata.size,
      url: fileMetadata.url,
      crmFileId,
      uploadedAt: fileMetadata.uploadedAt,
    });

    res.json({ fileId: fileMetadata.id });
  } catch (error) {
    console.error("Upload error:", error);
    res.status(500).json({
      error: error instanceof Error ? error.message : "Upload failed",
    });
  }
});

export default router;
```

**Focus**: Code that implements functionality flows, aligned with project patterns, not generic code.

---

## Code Generation Checklist (Reference - Use AFTER Functionality Understood)

**⚠️ Only check these AFTER functionality is understood**:

- Prefer clarity over cleverness; keep functions focused and small (supports functionality understanding)
- Preserve separation of concerns (supports functionality maintenance)
- Handle errors explicitly and surface actionable messages (supports functionality reliability)
- Cover edge cases and input validation before returning success (supports functionality reliability)
- Keep public APIs stable; document breaking changes for review (supports functionality evolution)
- Align with project patterns (follows existing structure and conventions)

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
