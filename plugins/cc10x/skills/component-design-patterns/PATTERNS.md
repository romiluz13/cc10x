# Component Design Pattern Library

## Component Structure

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
```

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
