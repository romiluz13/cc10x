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
