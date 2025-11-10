# Code Generation - Examples

Reference code generation examples. Use AFTER understanding functionality and project patterns (see SKILL.md Steps 1-3).

## Example: File Upload to CRM (UI Feature)

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
