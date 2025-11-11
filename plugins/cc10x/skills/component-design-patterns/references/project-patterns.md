# Project Component Patterns

**Reference**: Part of `component-design-patterns` skill. See main SKILL.md for overview.

## Phase 2: Understand Project's Component Patterns

**CRITICAL**: Before designing components, understand how this project designs components.

## Process

### 1. Load Project Context Understanding

**Load `project-context-understanding` skill** to understand project structure and conventions.

### 2. Map Component Patterns

**Find component structure**:

```bash
# Find component structure
find src/components -type f -name "*.tsx" | head -20

# Find component patterns
grep -r "interface.*Props\|type.*Props" --include="*.tsx" | head -20

# Find state management patterns
grep -r "useState\|useReducer\|redux\|zustand" --include="*.tsx" | head -20
```

**Map component conventions**:

```bash
# Find component naming conventions
ls -R src/components | grep -E "\.(tsx|jsx)$"

# Find component composition patterns
grep -r "children\|render\|slot" --include="*.tsx" | head -20

# Find UI library patterns
grep -r "import.*from.*@mui\|import.*from.*antd\|import.*from.*chakra" --include="*.tsx" | head -20
```

### 3. Document Project's Component Patterns

**Document**:

- Component Structure: Functional components, class components, hooks
- Component Naming: PascalCase, kebab-case, etc.
- Props Patterns: Interface definitions, prop types, default props
- State Management: useState, useReducer, Redux, Zustand, etc.
- UI Library: Material UI, Ant Design, Chakra UI, custom, etc.
- Composition Patterns: Compound components, render props, children, etc.

## Example Output

```
Project Component Patterns:
Component Structure:
- Functional components with hooks
- TypeScript interfaces for props
- Custom hooks for logic

Component Naming:
- PascalCase for components (UploadForm)
- kebab-case for files (upload-form.tsx)

Props Patterns:
- Interface definitions (interface UploadFormProps)
- Required vs optional props
- Default props for optional values

State Management:
- useState for local state
- useReducer for complex state
- Context API for shared state

UI Library:
- Material UI (MUI) components
- Custom components in components/ui/

Composition Patterns:
- Compound components for related components
- Render props for flexible composition
- Children prop for wrapper components
```

## Pattern Analysis Checklist

After pattern analysis:

- [ ] Component structure identified
- [ ] Component naming conventions identified
- [ ] Props patterns identified
- [ ] State management patterns identified
- [ ] UI library identified
- [ ] Composition patterns identified
- [ ] Ready for component design

---

**See Also**: `references/functionality-mapping.md` for functionality analysis, `references/component-design.md` for component design.
