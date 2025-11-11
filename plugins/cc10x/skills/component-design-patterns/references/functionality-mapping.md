# Functionality Mapping - Component Requirements

**Reference**: Part of `component-design-patterns` skill. See main SKILL.md for overview.

## Phase 1: Context-Dependent Functionality Analysis

**CRITICAL**: Before designing components, complete functionality analysis to understand component requirements.

## Process

### 1. Load Functionality Analysis Template

**Reference**: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`

**Complete Phase 1**: Universal Questions (especially Constraints - component constraints)
**Complete Phase 2**: Context-Dependent Flow Questions (UI Features - User Flow, Admin Flow, System Flow)

### 2. Understand Functionality

**Answer**:

- What is this feature supposed to do?
- What functionality does user need?
- What are the user flows? (Step-by-step user interactions)

### 3. Understand Component Requirements (from flows)

**Map flows to component needs**:

- **User Flow** → UI components for user interactions
- **Admin Flow** → UI components for admin interactions
- **System Flow** → Components for system processing

## Example: File Upload to CRM

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

**Component Requirements from User Flow**:

- Upload button component (Step 1-2)
- File input component (Step 3)
- Progress indicator component (Step 4)
- Success/error message component (Step 5)
- File link component (Step 6)

**Admin Flow**:

1. Admin sees file list
2. Admin can filter by user/date/type
3. Admin can download files
4. Admin can delete files

**Component Requirements from Admin Flow**:

- File list component (Step 1)
- Filter component (Step 2)
- Download button component (Step 3)
- Delete button component (Step 4)

**System Flow**:

1. System receives file upload request (POST /api/files/upload)
2. System validates file type and size
3. System stores file in secure storage (S3 bucket)
4. System sends file metadata to CRM API
5. System stores file record in database
6. System returns success response to user

**Component Requirements from System Flow**:

- API client component (Step 1, 4)
- Validation logic component (Step 2)
- Storage service component (Step 3)
- Database service component (Step 5)

## Flow-to-Component Mapping

**Mapping Pattern**:

- Each flow step → Component responsibility
- Related flow steps → Component grouping
- Flow dependencies → Component hierarchy

**Example Mapping**:

- User Flow Steps 1-5 → UploadForm component (handles upload flow)
- Admin Flow Steps 1-4 → FileListAdmin component (handles admin file management)
- System Flow Steps 1-6 → Backend services (handles system processing)

## Component Requirement Checklist

After functionality analysis:

- [ ] User Flow analyzed → UI component requirements identified
- [ ] Admin Flow analyzed → Admin component requirements identified
- [ ] System Flow analyzed → System component requirements identified
- [ ] Component requirements mapped to flows
- [ ] Ready for project pattern analysis

---

**See Also**: `references/project-patterns.md` for project pattern analysis, `references/component-design.md` for component design.
