# TDD Examples

## Example: File Upload to CRM (UI Feature)

**Based on Functionality Analysis and Project Test Patterns**:

**1. RED - Write Failing Tests (For Functionality)**:

```typescript
// src/components/UploadForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UploadForm } from './UploadForm';
import { uploadFile } from '@/api/files';

jest.mock('@/api/files');

describe('UploadForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Test: User Flow - User can upload valid file
  it('allows user to upload valid file and shows success message', async () => {
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

  // Test: User Flow - User sees upload progress
  it('shows upload progress during upload', async () => {
    const mockUploadFile = uploadFile as jest.MockedFunction<typeof uploadFile>;
    let progressCallback: (progress: number) => void;

    mockUploadFile.mockImplementation((file, onProgress) => {
      progressCallback = onProgress;
      return Promise.resolve('file-123');
    });

    render(<UploadForm />);

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/drag and drop/i).closest('div')?.querySelector('input');

    if (input) {
      await userEvent.upload(input, file);
    }

    // Simulate progress updates
    progressCallback!(50);
    expect(await screen.findByText(/uploading.*50%/i)).toBeInTheDocument();

    progressCallback!(100);
    expect(await screen.findByText(/uploading.*100%/i)).toBeInTheDocument();
  });

  // Test: Error Handling - Invalid file type
  it('shows error message for invalid file type', async () => {
    render(<UploadForm />);

    const file = new File(['test content'], 'test.exe', { type: 'application/x-msdownload' });
    const input = screen.getByLabelText(/drag and drop/i).closest('div')?.querySelector('input');

    if (input) {
      await userEvent.upload(input, file);
    }

    expect(await screen.findByText(/file type not supported/i)).toBeInTheDocument();
  });

  // Test: Error Handling - File too large
  it('shows error message for file exceeding size limit', async () => {
    render(<UploadForm />);

    // Create a file larger than 10MB
    const largeContent = 'x'.repeat(11 * 1024 * 1024);
    const file = new File([largeContent], 'large.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/drag and drop/i).closest('div')?.querySelector('input');

    if (input) {
      await userEvent.upload(input, file);
    }

    expect(await screen.findByText(/exceeds.*10MB/i)).toBeInTheDocument();
  });

  // Test: Error Handling - Network failure
  it('shows error message when upload fails', async () => {
    const mockUploadFile = uploadFile as jest.MockedFunction<typeof uploadFile>;
    mockUploadFile.mockRejectedValue(new Error('Network error'));

    render(<UploadForm />);

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/drag and drop/i).closest('div')?.querySelector('input');

    if (input) {
      await userEvent.upload(input, file);
    }

    expect(await screen.findByText(/upload failed/i)).toBeInTheDocument();
  });

  // Test: System Flow - Calls onUploadSuccess callback
  it('calls onUploadSuccess callback when upload succeeds', async () => {
    const mockUploadFile = uploadFile as jest.MockedFunction<typeof uploadFile>;
    mockUploadFile.mockResolvedValue('file-123');
    const onUploadSuccess = jest.fn();

    render(<UploadForm onUploadSuccess={onUploadSuccess} />);

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/drag and drop/i).closest('div')?.querySelector('input');

    if (input) {
      await userEvent.upload(input, file);
    }

    await waitFor(() => {
      expect(onUploadSuccess).toHaveBeenCalledWith('file-123');
    });
  });
});
```

**2. GREEN - Minimal Implementation (To Make Tests Pass)**:

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
    maxSize: 10 * 1024 * 1024,
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
        <input {...getInputProps()} disabled={uploading} aria-label="Drag and drop a file here, or click to select" />
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

**3. REFACTOR - Clean Up (While Tests Stay Green)**:

```bash
# Run tests to verify they still pass
npm test UploadForm.test.tsx
# Expected: All tests pass

# Refactor: Extract constants
# Refactor: Extract helper functions
# Refactor: Improve error messages
# After each refactor, run tests again
```

**Focus**: Tests that verify functionality flows, aligned with project test patterns, not generic tests.

---

## Example: API Endpoint Testing (Backend API)

**Based on Functionality Analysis and Project Test Patterns**:

**1. RED - Write Failing Tests (For Functionality)**:

```typescript
// src/api/files/route.test.ts
import { describe, it, expect, beforeEach, vi } from "vitest";
import { GET, POST } from "./route";
import { NextRequest } from "next/server";

// Mock dependencies
vi.mock("@/lib/storage");
vi.mock("@/lib/db");

describe("POST /api/files", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // Test: Request Flow - Valid file upload
  it("accepts valid file upload and returns file ID", async () => {
    const formData = new FormData();
    const file = new File(["test content"], "test.pdf", {
      type: "application/pdf",
    });
    formData.append("file", file);

    const request = new NextRequest("http://localhost/api/files", {
      method: "POST",
      body: formData,
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(201);
    expect(data).toMatchObject({
      success: true,
      data: {
        fileId: expect.any(String),
      },
    });
  });

  // Test: Error Flow - Invalid file type
  it("rejects invalid file type with 400 error", async () => {
    const formData = new FormData();
    const file = new File(["test content"], "test.exe", {
      type: "application/x-msdownload",
    });
    formData.append("file", file);

    const request = new NextRequest("http://localhost/api/files", {
      method: "POST",
      body: formData,
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(400);
    expect(data).toMatchObject({
      success: false,
      error: expect.stringContaining("file type"),
    });
  });

  // Test: Error Flow - File too large
  it("rejects file exceeding size limit with 400 error", async () => {
    const largeContent = "x".repeat(11 * 1024 * 1024);
    const formData = new FormData();
    const file = new File([largeContent], "large.pdf", {
      type: "application/pdf",
    });
    formData.append("file", file);

    const request = new NextRequest("http://localhost/api/files", {
      method: "POST",
      body: formData,
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(400);
    expect(data).toMatchObject({
      success: false,
      error: expect.stringContaining("size limit"),
    });
  });

  // Test: Error Flow - Missing authentication
  it("rejects unauthenticated requests with 401 error", async () => {
    const formData = new FormData();
    const file = new File(["test content"], "test.pdf", {
      type: "application/pdf",
    });
    formData.append("file", file);

    const request = new NextRequest("http://localhost/api/files", {
      method: "POST",
      body: formData,
      // No Authorization header
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(401);
    expect(data).toMatchObject({
      success: false,
      error: expect.stringContaining("authentication"),
    });
  });

  // Test: Error Flow - Storage failure
  it("handles storage failure with 500 error", async () => {
    // Mock storage to throw error
    vi.mocked(storeFile).mockRejectedValue(new Error("Storage unavailable"));

    const formData = new FormData();
    const file = new File(["test content"], "test.pdf", {
      type: "application/pdf",
    });
    formData.append("file", file);

    const request = new NextRequest("http://localhost/api/files", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: "Bearer valid-token",
      },
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(500);
    expect(data).toMatchObject({
      success: false,
      error: expect.any(String),
    });
  });

  // Test: Request Flow - Valid file retrieval
  describe("GET /api/files/:id", () => {
    it("returns file metadata for valid file ID", async () => {
      const request = new NextRequest("http://localhost/api/files/file-123", {
        method: "GET",
        headers: {
          Authorization: "Bearer valid-token",
        },
      });

      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toMatchObject({
        success: true,
        data: {
          id: "file-123",
          name: expect.any(String),
          size: expect.any(Number),
          url: expect.any(String),
        },
      });
    });

    // Test: Error Flow - File not found
    it("returns 404 for non-existent file", async () => {
      const request = new NextRequest(
        "http://localhost/api/files/non-existent",
        {
          method: "GET",
          headers: {
            Authorization: "Bearer valid-token",
          },
        },
      );

      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(404);
      expect(data).toMatchObject({
        success: false,
        error: expect.stringContaining("not found"),
      });
    });
  });
});
```

**2. GREEN - Minimal Implementation (To Make Tests Pass)**:

```typescript
// src/api/files/route.ts
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { storeFile, getFileMetadata } from "@/lib/storage";
import { authenticate } from "@/lib/auth";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ALLOWED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "image/jpeg",
  "image/png",
];

const fileSchema = z.object({
  type: z.string().refine((type) => ALLOWED_TYPES.includes(type), {
    message: "File type not supported",
  }),
  size: z.number().max(MAX_FILE_SIZE, {
    message: "File exceeds size limit",
  }),
});

export async function POST(request: NextRequest) {
  try {
    // Authentication
    const user = await authenticate(request);
    if (!user) {
      return NextResponse.json(
        { success: false, error: "Authentication required" },
        { status: 401 },
      );
    }

    const formData = await request.formData();
    const file = formData.get("file") as File;

    if (!file) {
      return NextResponse.json(
        { success: false, error: "File is required" },
        { status: 400 },
      );
    }

    // Validation
    const validation = fileSchema.safeParse({
      type: file.type,
      size: file.size,
    });

    if (!validation.success) {
      return NextResponse.json(
        { success: false, error: validation.error.errors[0].message },
        { status: 400 },
      );
    }

    // Store file
    const fileId = await storeFile(file, user.id);

    return NextResponse.json(
      { success: true, data: { fileId } },
      { status: 201 },
    );
  } catch (error) {
    console.error("File upload error:", error);
    return NextResponse.json(
      { success: false, error: "Internal server error" },
      { status: 500 },
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    // Authentication
    const user = await authenticate(request);
    if (!user) {
      return NextResponse.json(
        { success: false, error: "Authentication required" },
        { status: 401 },
      );
    }

    const fileId = request.nextUrl.pathname.split("/").pop();
    if (!fileId) {
      return NextResponse.json(
        { success: false, error: "File ID is required" },
        { status: 400 },
      );
    }

    const metadata = await getFileMetadata(fileId);
    if (!metadata) {
      return NextResponse.json(
        { success: false, error: "File not found" },
        { status: 404 },
      );
    }

    return NextResponse.json(
      { success: true, data: metadata },
      { status: 200 },
    );
  } catch (error) {
    console.error("File retrieval error:", error);
    return NextResponse.json(
      { success: false, error: "Internal server error" },
      { status: 500 },
    );
  }
}
```

**3. REFACTOR - Clean Up (While Tests Stay Green)**:

```bash
# Run tests to verify they still pass
npm test route.test.ts
# Expected: All tests pass

# Refactor: Extract validation logic
# Refactor: Extract error handling
# Refactor: Improve error messages
# After each refactor, run tests again
```

**Focus**: Tests that verify API functionality flows (request flow, response flow, error flow), aligned with project test patterns, not generic tests.

## API Testing Patterns

### Comprehensive Test Coverage

- **Happy paths**: Test successful request/response flows
- **Error paths**: Test error scenarios (400, 401, 404, 500)
- **Edge cases**: Test boundary conditions, invalid inputs
- **Authentication**: Test authenticated and unauthenticated requests
- **Authorization**: Test permission checks

### Test Structure Organization

- **Describe blocks**: Group related tests by endpoint or functionality
- **BeforeEach/AfterEach**: Setup and cleanup between tests
- **Test naming**: Clear, descriptive test names that explain what's being tested
- **Arrange-Act-Assert**: Structure tests with clear setup, action, verification

### Testing Principles

- **Behavior over implementation**: Test what the API does, not how it does it
- **Realistic mock data**: Use realistic test data that matches production
- **Isolation**: Each test should be independent and not depend on other tests
- **Fast execution**: Tests should run quickly for fast feedback

### Tool Recommendations

- **Vitest/Jest**: Test framework
- **Supertest**: HTTP assertion library for API testing
- **MSW**: Mock Service Worker for mocking API calls
- **Zod**: Schema validation for request/response validation

### Realistic Mock Data Patterns

- **Factory functions**: Create test data factories for consistent test data
- **Fixtures**: Use fixtures for complex test data
- **Builders**: Use builder pattern for flexible test data creation
