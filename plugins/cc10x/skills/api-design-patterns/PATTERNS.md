# API Design Pattern Library

## RESTful Structure

**Understand functionality first, then apply REST patterns** (aligned with project conventions):

**RESTful Endpoints** (mapped from functionality flows):

```http
# Based on User Flow: File Upload
POST /api/v1/files/upload          # Start upload (Request Flow Step 1)
GET /api/v1/files/{id}              # Get file info (User Flow Step 5)
GET /api/v1/files/{id}/download     # Download file (User Flow Step 5)

# Based on Admin Flow: File Management
GET /api/v1/files                   # List files (Admin Flow Step 2)
  ?userId=user_123                  # Filter by user
  &type=pdf                         # Filter by type
  &page=1&limit=20                  # Pagination
DELETE /api/v1/files/{id}           # Delete file (Admin Flow Step 5)

# Based on System Flow: File Processing
POST /api/v1/files/{id}/process     # Process file (System Flow)
GET /api/v1/files/{id}/status       # Get processing status (System Flow)
```

## Request/Response Schemas

**Design schemas to support functionality** (aligned with project conventions):

**Request Schema** (aligned with functionality requirements):

```typescript
// Request schema for file upload (aligned with functionality)
interface UploadFileRequest {
  file: File; // Multipart file
  metadata: {
    name: string; // File name
    type: string; // File type (PDF, DOCX, JPG, PNG)
    description?: string; // Optional description
  };
}

// Validation (aligned with functionality constraints)
const uploadSchema = z.object({
  file: z
    .instanceof(File)
    .refine((file) => file.size <= 10 * 1024 * 1024, "File exceeds 10MB limit")
    .refine(
      (file) =>
        [
          "application/pdf",
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
          "image/jpeg",
          "image/png",
        ].includes(file.type),
      "Invalid file type",
    ),
  metadata: z.object({
    name: z.string().min(1),
    type: z.string(),
    description: z.string().optional(),
  }),
});
```

**Response Schema** (aligned with functionality needs):

```typescript
// Response schema for file upload (aligned with functionality)
interface UploadFileResponse {
  file: {
    id: string; // File ID (for user flow: view file)
    name: string; // File name
    type: string; // File type
    size: number; // File size
    url: string; // Storage URL (for user flow: download)
    crmFileId?: string; // CRM file ID (for integration flow)
    status: "uploaded" | "processing" | "failed"; // Status (for user flow: progress)
    uploadedAt: string; // Upload timestamp (for admin flow: filter by date)
  };
}
```

## Error Handling

**Design errors to support functionality** (aligned with project error format):

**Error Schema** (aligned with functionality error cases):

```typescript
// Error schema (aligned with project error format)
interface ApiError {
  error: {
    code: string; // Error code (aligned with functionality)
    message: string; // User-friendly message (aligned with functionality)
    status: number; // HTTP status code
    details?: Record<string, any>; // Additional details (aligned with functionality)
  };
}

// Error examples (aligned with functionality error cases)
const errors = {
  FILE_TOO_LARGE: {
    code: "FILE_TOO_LARGE",
    message: "File exceeds 10MB limit",
    status: 413,
    details: { maxSize: "10MB", fileSize: "15MB" },
  },
  INVALID_FILE_TYPE: {
    code: "INVALID_FILE_TYPE",
    message: "File type not supported. Please upload PDF, DOCX, JPG, or PNG",
    status: 400,
    details: { allowedTypes: ["PDF", "DOCX", "JPG", "PNG"] },
  },
  CRM_API_ERROR: {
    code: "CRM_API_ERROR",
    message: "Failed to sync file to CRM. Please try again",
    status: 502,
    details: { retryable: true },
  },
};
```

## Authentication & Authorization

**Design auth to support functionality** (aligned with project auth patterns):

**Authentication** (aligned with functionality security):

```typescript
// Authentication middleware (aligned with project JWT pattern)
import { authenticate } from "../middleware/auth";

app.post("/api/v1/files/upload", authenticate, uploadHandler);
// authenticate middleware validates JWT token
// Sets req.user with user info
```

**Authorization** (aligned with functionality access control):

```typescript
// Authorization check (aligned with functionality)
function canUploadFile(user: User, file: File): boolean {
  // User can upload their own files
  // Admin can upload any file
  return file.userId === user.id || user.role === "admin";
}
```

## Versioning

**Version APIs to support functionality evolution** (aligned with project versioning):

**Versioning Strategy** (aligned with project URL versioning):

```http
# URL versioning (aligned with project /api/v1/ pattern)
POST /api/v1/files/upload    # Current version
POST /api/v2/files/upload    # New version (breaking changes)

# Deprecation (aligned with functionality evolution)
HTTP/1.1 200 OK
Deprecation: true
Sunset: "2024-12-31"
Link: </api/v2/files/upload>; rel="successor-version"
```
