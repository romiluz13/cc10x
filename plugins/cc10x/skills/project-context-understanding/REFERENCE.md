# Project Context Understanding Reference

## Codebase Structure

**Map structure to understand functionality context**:

### Directory Structure

```bash
# Map top-level directories
ls -la

# Map source directories
find src -type d -maxdepth 3

# Map component directories
find . -type d -name "components" -o -name "pages" -o -name "views"
```

### File Patterns

```bash
# Map file types
find . -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx"

# Map test files
find . -name "*.test.*" -o -name "*.spec.*"

# Map configuration files
find . -name "*.config.*" -o -name "*.json" -o -name "*.yaml"
```

### Module Structure

```bash
# Map entry points
grep -r "export.*default" --include="*.ts" --include="*.tsx"

# Map module exports
grep -r "^export " --include="*.ts" --include="*.tsx"
```

**Output Format**:

```
Codebase Structure:
├── src/
│   ├── components/        # React components
│   ├── pages/             # Page components
│   ├── api/               # API routes
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   └── types/             # TypeScript types
├── tests/
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
└── config/                # Configuration files
```

## Dependencies

**Map dependencies to understand functionality context**:

### External Dependencies

```bash
# Read package.json (Node.js)
cat package.json | jq '.dependencies, .devDependencies'

# Read requirements.txt (Python)
cat requirements.txt

# Read go.mod (Go)
cat go.mod

# Read Cargo.toml (Rust)
cat Cargo.toml
```

### Internal Dependencies

```bash
# Map internal imports
grep -r "^import.*from.*['\"]\./" --include="*.ts" --include="*.tsx"

# Map relative imports
grep -r "^import.*from.*['\"]\.\./" --include="*.ts" --include="*.tsx"
```

**Output Format**:

```
Dependencies:
External:
- react (^18.0.0)
- express (^4.18.0)
- aws-sdk (^2.1000.0)
- axios (^1.0.0)

Internal:
- components/UploadForm → api/files → services/storage
- components/UploadForm → services/crm-client
- api/files → services/storage
- api/files → services/crm-client
```

## Connections

**Map connections to understand functionality flow**:

### Import/Export Relationships

```bash
# Map imports
grep -r "^import " --include="*.ts" --include="*.tsx" | head -50

# Map exports
grep -r "^export " --include="*.ts" --include="*.tsx" | head -50
```

### API Calls

```bash
# Map API endpoints
grep -r "fetch\|axios\|request" --include="*.ts" --include="*.tsx"

# Map route definitions
grep -r "router\.\|app\.(get|post|put|delete)" --include="*.ts"
```

### Data Flow

```bash
# Map data transformations
grep -r "\.map\|\.filter\|\.reduce" --include="*.ts" --include="*.tsx"

# Map state management
grep -r "useState\|useReducer\|redux" --include="*.ts" --include="*.tsx"
```

**Output Format**:

```
Connections:
Import/Export:
- components/UploadForm imports from api/files
- api/files imports from services/storage
- api/files imports from services/crm-client

API Calls:
- components/UploadForm → POST /api/files/upload
- api/files → POST /crm/files (external)
- api/files → PUT s3://bucket/files/{id} (external)

Data Flow:
- File → UploadForm → api/files → storage service → S3
- File metadata → api/files → crm-client → CRM API
```

## Architecture Patterns

**Identify patterns to understand functionality context**:

### Architecture Type

- Monolith vs Microservices
- MVC vs MVVM vs Clean Architecture
- Server-side vs Client-side rendering
- REST vs GraphQL vs gRPC

### Pattern Indicators

```bash
# MVC indicators
grep -r "controller\|model\|view" --include="*.ts" -i

# Microservices indicators
grep -r "service\|api\|gateway" --include="*.ts" -i

# Component patterns
grep -r "component\|container\|presentational" --include="*.tsx" -i
```

**Output Format**:

```
Architecture Patterns:
Type: MVC (Model-View-Controller)
Patterns:
- Controllers: src/controllers/
- Models: src/models/
- Views: src/views/

Design Patterns:
- Singleton: services/ConfigService.ts
- Factory: factories/FileFactory.ts
- Observer: utils/EventEmitter.ts
```

## Codebase Conventions

**Identify conventions to understand functionality context**:

### Naming Conventions

```bash
# Component naming
find src/components -name "*.tsx" | head -10

# File naming
find src -name "*.ts" -o -name "*.tsx" | head -20

# Variable naming
grep -r "const [a-z]" --include="*.ts" --include="*.tsx" | head -20
```

### Structure Conventions

```bash
# Component structure
grep -r "export.*function\|export.*const" --include="*.tsx" | head -20

# File organization
find src -type f -name "*.ts" -o -name "*.tsx" | head -20
```

### Style Conventions

```bash
# Code style (check .prettierrc, .eslintrc)
cat .prettierrc
cat .eslintrc

# TypeScript config
cat tsconfig.json
```

**Output Format**:

```
Codebase Conventions:
Naming:
- Components: PascalCase (UploadForm.tsx)
- Files: kebab-case (upload-form.tsx)
- Variables: camelCase (uploadFile)

Structure:
- Components: One component per file
- Exports: Named exports preferred
- Imports: Absolute imports from src/

Style:
- Indentation: 2 spaces
- Quotes: Single quotes
- Semicolons: Yes
```

## Dependency Graph Visualization

**Visualize dependencies to understand functionality context**:

```
Dependency Graph:
components/UploadForm
  ├── api/files
  │   ├── services/storage
  │   └── services/crm-client
  └── utils/validation
      └── types/file

services/storage
  └── aws-sdk

services/crm-client
  └── axios
```

## Component Relationships

**Map relationships to understand functionality context**:

### Component Hierarchy

```
Component Hierarchy:
App
├── UploadPage
│   ├── UploadForm
│   │   ├── FileInput
│   │   ├── UploadProgress
│   │   └── SuccessMessage
│   └── FileViewer
└── AdminPage
    ├── FileList
    │   ├── FileFilters
    │   └── FileCard[]
    └── FileActions
```

### Data Flow

```
Data Flow:
User Input → UploadForm → api/files → storage service → S3
File Metadata → api/files → crm-client → CRM API
File Record → api/files → database
```

### Service Relationships

```
Service Relationships:
storage service → S3 (external)
crm-client → CRM API (external)
database → PostgreSQL (external)
```
