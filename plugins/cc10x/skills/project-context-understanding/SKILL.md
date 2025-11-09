---
name: project-context-understanding
description: Deeply understands project structure, dependencies, connections, architecture patterns, and conventions. Use PROACTIVELY before any major planning/build/review to map codebase structure, dependencies, connections, and patterns. Essential for context-aware analysis and personalized recommendations. Maps files, directories, modules, dependencies (internal/external), imports/exports, API calls, data flows, architecture patterns, and codebase conventions.
allowed-tools: Read, Grep, Glob, Bash
---

# Project Context Understanding - Deep Codebase Mapping

## Purpose

This skill provides deep understanding of project structure, dependencies, connections, architecture patterns, and conventions. It maps the entire codebase to enable context-aware analysis and personalized recommendations.

**Unique Value**:

- Maps entire codebase structure (files, directories, modules)
- Maps dependencies (internal and external)
- Maps connections (imports, exports, API calls, data flows)
- Understands architecture patterns used
- Identifies codebase conventions and style
- Tracks relationships between components

**When to Use**:

- Before any major planning/build/review
- When understanding codebase structure is critical
- When dependencies need to be mapped
- When architecture patterns need to be identified
- When codebase conventions need to be understood

---

## Functionality First Mandate

**BEFORE mapping project context, understand what you're analyzing**:

1. **What is the purpose of this analysis?**
   - What functionality are we planning/building/reviewing?
   - What context do we need to understand?

2. **What scope is relevant?**
   - Entire codebase or specific modules?
   - Frontend, backend, or both?
   - Specific features or components?

3. **THEN map project context** - Map structure, dependencies, connections relevant to the functionality

---

## Process

### Phase 1: Understand Analysis Purpose (MANDATORY FIRST STEP)

**Before mapping, clarify**:

1. **What functionality are we analyzing?**
   - What problem are we solving?
   - What feature/component/code are we working with?

2. **What context do we need?**
   - Codebase structure?
   - Dependencies?
   - Architecture patterns?
   - Codebase conventions?
   - All of the above?

3. **What scope is relevant?**
   - Entire codebase?
   - Specific directories/modules?
   - Related files only?

**Example**:

- **Purpose**: Planning file upload feature
- **Context Needed**: Backend API structure, storage services, CRM integration patterns
- **Scope**: `src/api/`, `src/services/`, `src/integrations/`

---

### Phase 2: Map Codebase Structure

**Use Grep/Glob to discover file structure**:

1. **Directory Structure**:

   ```bash
   # Map top-level directories
   ls -la

   # Map source directories
   find src -type d -maxdepth 3

   # Map component directories
   find . -type d -name "components" -o -name "pages" -o -name "views"
   ```

2. **File Patterns**:

   ```bash
   # Map file types
   find . -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx"

   # Map test files
   find . -name "*.test.*" -o -name "*.spec.*"

   # Map configuration files
   find . -name "*.config.*" -o -name "*.json" -o -name "*.yaml"
   ```

3. **Module Structure**:

   ```bash
   # Map entry points
   grep -r "export.*default" --include="*.ts" --include="*.tsx"

   # Map module exports
   grep -r "^export " --include="*.ts" --include="*.tsx"
   ```

**Document**:

- Directory structure (tree format)
- File organization patterns
- Module boundaries
- Entry points

**Example Output**:

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

---

### Phase 3: Map Dependencies

**Analyze dependency files**:

1. **External Dependencies**:

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

2. **Internal Dependencies**:

   ```bash
   # Map internal imports
   grep -r "^import.*from.*['\"]\./" --include="*.ts" --include="*.tsx"

   # Map relative imports
   grep -r "^import.*from.*['\"]\.\./" --include="*.ts" --include="*.tsx"
   ```

3. **Dependency Graph**:
   - Map which modules depend on which
   - Map external library usage
   - Map internal module relationships

**Document**:

- External dependencies (libraries, frameworks)
- Internal dependencies (module relationships)
- Dependency graph (text-based visualization)

**Example Output**:

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

---

### Phase 4: Map Connections

**Map imports, exports, API calls, data flows**:

1. **Import/Export Relationships**:

   ```bash
   # Map imports
   grep -r "^import " --include="*.ts" --include="*.tsx" | head -50

   # Map exports
   grep -r "^export " --include="*.ts" --include="*.tsx" | head -50
   ```

2. **API Calls**:

   ```bash
   # Map API endpoints
   grep -r "fetch\|axios\|request" --include="*.ts" --include="*.tsx"

   # Map route definitions
   grep -r "router\.\|app\.(get|post|put|delete)" --include="*.ts"
   ```

3. **Data Flow**:

   ```bash
   # Map data transformations
   grep -r "\.map\|\.filter\|\.reduce" --include="*.ts" --include="*.tsx"

   # Map state management
   grep -r "useState\|useReducer\|redux" --include="*.ts" --include="*.tsx"
   ```

**Document**:

- Import/export relationships
- API call patterns
- Data flow paths
- State management patterns

**Example Output**:

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

---

### Phase 5: Identify Architecture Patterns

**Identify architectural patterns used**:

1. **Architecture Type**:
   - Monolith vs Microservices
   - MVC vs MVVM vs Clean Architecture
   - Server-side vs Client-side rendering
   - REST vs GraphQL vs gRPC

2. **Pattern Indicators**:

   ```bash
   # MVC indicators
   grep -r "controller\|model\|view" --include="*.ts" -i

   # Microservices indicators
   grep -r "service\|api\|gateway" --include="*.ts" -i

   # Component patterns
   grep -r "component\|container\|presentational" --include="*.tsx" -i
   ```

3. **Design Patterns**:
   - Singleton, Factory, Observer, etc.
   - React patterns (Hooks, HOCs, Render Props)
   - Node.js patterns (Middleware, Controllers, Services)

**Document**:

- Architecture type
- Design patterns used
- Pattern examples

**Example Output**:

```
Architecture Patterns:
Type: Monolithic MVC with React frontend
Patterns:
- MVC: Controllers in api/, Models in services/, Views in components/
- Repository Pattern: services/storage.ts abstracts S3
- Service Layer: Business logic in services/
- Component Pattern: React functional components with hooks
```

---

### Phase 6: Identify Codebase Conventions

**Identify naming, structure, style conventions**:

1. **Naming Conventions**:

   ```bash
   # File naming
   ls -R | grep -E "\.(ts|tsx|js|jsx)$"

   # Function naming
   grep -r "function \|const \|export const " --include="*.ts" | head -20

   # Component naming
   grep -r "export.*function\|export.*const.*=" --include="*.tsx" | head -20
   ```

2. **Structure Conventions**:
   - File organization patterns
   - Directory naming patterns
   - Module organization patterns

3. **Style Conventions**:

   ```bash
   # Read style guide if exists
   cat .eslintrc.json 2>/dev/null || cat .prettierrc 2>/dev/null || echo "No style config found"

   # Analyze code style from examples
   head -50 src/components/UploadForm.tsx
   ```

**Document**:

- Naming conventions (files, functions, components, variables)
- Structure conventions (directory organization, file organization)
- Style conventions (formatting, linting rules)

**Example Output**:

```
Codebase Conventions:
Naming:
- Files: kebab-case (upload-form.tsx)
- Components: PascalCase (UploadForm)
- Functions: camelCase (uploadFile)
- Constants: UPPER_SNAKE_CASE (MAX_FILE_SIZE)

Structure:
- Components in components/
- Pages in pages/
- API routes in api/
- Services in services/
- Utils in utils/

Style:
- TypeScript strict mode
- ESLint with React plugin
- Prettier for formatting
- 2-space indentation
```

---

### Phase 7: Create Dependency Graph Visualization

**Create text-based dependency graph**:

1. **Module Dependencies**:
   - Map which modules import from which
   - Identify circular dependencies
   - Identify dependency chains

2. **External Dependencies**:
   - Map external library usage
   - Identify critical dependencies
   - Identify version constraints

3. **Visualization**:

   ```
   Dependency Graph:

   components/UploadForm
     ├─> api/files
     │     ├─> services/storage
     │     │     └─> aws-sdk (external)
     │     └─> services/crm-client
     │           └─> axios (external)
     └─> utils/validation
           └─> (no dependencies)
   ```

**Document**:

- Module dependency graph
- External dependency usage
- Critical dependency paths

---

### Phase 8: Track Component Relationships

**Track relationships between components**:

1. **Component Hierarchy**:
   - Parent-child relationships
   - Component composition patterns
   - Shared component usage

2. **Data Flow**:
   - Props flow (parent → child)
   - State flow (component → state management)
   - Event flow (child → parent)

3. **Service Relationships**:
   - Service dependencies
   - Service composition
   - Service interfaces

**Document**:

- Component relationships
- Data flow patterns
- Service relationships

**Example Output**:

```
Component Relationships:
UploadForm (parent)
  ├─> FileInput (child)
  │     └─> Receives: onFileSelect, accept, maxSize
  │     └─> Emits: fileSelected event
  ├─> ProgressBar (child)
  │     └─> Receives: progress (0-100)
  └─> ErrorMessage (child)
        └─> Receives: error message

Data Flow:
User selects file → FileInput → UploadForm → api/files → storage service
```

---

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Project Context Analysis

## Analysis Purpose

[What functionality are we analyzing? What context do we need?]

## Codebase Structure

[Directory structure, file organization, module boundaries]

## Dependencies

[External dependencies, internal dependencies, dependency graph]

## Connections

[Import/export relationships, API calls, data flows]

## Architecture Patterns

[Architecture type, design patterns, pattern examples]

## Codebase Conventions

[Naming conventions, structure conventions, style conventions]

## Dependency Graph

[Text-based visualization of dependencies]

## Component Relationships

[Component hierarchy, data flow, service relationships]

## Key Insights

[Summary of critical findings relevant to functionality]
```

---

## Usage Guidelines

### For Planning

1. **Map entire codebase structure** to understand where new features fit
2. **Map dependencies** to understand integration points
3. **Map architecture patterns** to follow existing patterns
4. **Map conventions** to maintain consistency

### For Building

1. **Map relevant modules** to understand where to add code
2. **Map dependencies** to understand what's available
3. **Map patterns** to follow existing patterns
4. **Map conventions** to maintain code style

### For Review

1. **Map affected modules** to understand impact
2. **Map dependencies** to check for breaking changes
3. **Map patterns** to verify pattern compliance
4. **Map conventions** to verify style compliance

---

## Key Principles

1. **Purpose-Driven**: Map context relevant to functionality being analyzed
2. **Comprehensive**: Map structure, dependencies, connections, patterns, conventions
3. **Visual**: Use text-based visualizations for clarity
4. **Actionable**: Provide insights that inform decisions
5. **Efficient**: Use Grep/Glob to discover patterns quickly
6. **Accurate**: Verify findings by reading actual files

---

## Common Mistakes to Avoid

1. **Mapping Everything**: Don't map entire codebase if only specific modules are relevant
2. **Missing Dependencies**: Don't forget to map internal dependencies
3. **Ignoring Patterns**: Don't miss architectural patterns that inform design
4. **Generic Analysis**: Don't provide generic analysis - be specific to codebase
5. **No Verification**: Don't assume structure - verify by reading files
6. **Missing Connections**: Don't forget to map import/export relationships

---

_This skill enables context-aware analysis and personalized recommendations by deeply understanding project structure, dependencies, connections, architecture patterns, and conventions._
