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

**Reference**: See [REFERENCE.md](./REFERENCE.md) for detailed mapping techniques including:

- Directory structure mapping commands
- File pattern discovery
- Module structure analysis
- Output format examples

**Use Grep/Glob to discover file structure**:

1. **Directory Structure**: See REFERENCE.md for commands
2. **File Patterns**: See REFERENCE.md for commands
3. **Module Structure**: See REFERENCE.md for commands

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
