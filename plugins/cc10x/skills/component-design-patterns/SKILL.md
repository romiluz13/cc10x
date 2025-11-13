---
name: component-design-patterns
description: Context-aware component design that understands component requirements from flows before designing. Use PROACTIVELY when planning features that need UI components. First understands functionality requirements and maps them to component needs, then designs component hierarchy to support that functionality. Provides specific component designs with examples aligned with project component patterns. Focuses on components that enable functionality.
allowed-tools: Read, Grep, Glob
---

# Component Design Patterns - Context-Aware & Functionality First

## Purpose

This skill provides context-aware component design that understands component requirements from flows before designing. It maps functionality to components and designs components to support functionality, providing specific component designs with examples aligned with project component patterns.

## Functionality First Mandate

**CRITICAL**: Before designing components, complete context-dependent functionality analysis.

**Core Principle**: Understand functionality requirements first, then understand project component patterns, then design components to support functionality.

## Quick Start

Design components by first understanding functionality, then mapping to component needs.

**Example:**

1. **Understand functionality**: File upload feature (User Flow: select → upload → confirm)
2. **Understand project patterns**: React functional components, TypeScript interfaces
3. **Map to components**: UploadForm (select), ProgressBar (upload), SuccessMessage (confirm)
4. **Design hierarchy**: UploadForm contains ProgressBar and SuccessMessage

**Result:** Component hierarchy designed to support functionality using project patterns.

## Quick Decision Tree

```
COMPONENT DESIGN NEEDED?
│
├─ Understand Functionality First
│  ├─ Context-dependent analysis complete? → Continue
│  └─ Not complete? → STOP, complete functionality analysis first
│
├─ Understand Project Patterns
│  ├─ Component patterns identified? → Continue
│  └─ Not identified? → Analyze project component patterns first
│
└─ Design Components
   ├─ Map flows to components? → Design component hierarchy
   └─ Flows not mapped? → STOP, map flows to components first
```

## When to Use

**Use PROACTIVELY when**:

- Planning features that need UI components
- Designing component architecture
- Reviewing component interfaces

## Core Process Overview

### Phase 1: Context-Dependent Functionality Analysis (MANDATORY FIRST STEP)

**Before any component design, complete functionality analysis**:

1. **Load Functionality Analysis Template**: Reference `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
2. **Complete Phase 1**: Universal Questions (especially Constraints - component constraints)
3. **Complete Phase 2**: Context-Dependent Flow Questions (UI Features - User Flow, Admin Flow, System Flow)
4. **Understand Component Requirements**: What UI components are needed? (from User Flow, Admin Flow, System Flow)

**Reference**: `references/functionality-mapping.md` for detailed functionality analysis and component requirement mapping.

### Phase 2: Understand Project's Component Patterns (MANDATORY SECOND STEP)

**Before designing components, understand how this project designs components**:

1. **Load Project Context Understanding**: Load `project-context-understanding` skill
2. **Map Component Patterns**: Component structure, naming, props, state management, UI library, composition patterns
3. **Document Project's Component Patterns**: Structure, naming, props, state, UI library, composition

**Reference**: `references/project-patterns.md` for detailed project component pattern analysis.

### Phase 3: Component Design (Design to Support Functionality)

**After understanding functionality and project component patterns, design components**:

1. **Map Functionality to Components**: For each functionality flow, identify component needs
2. **Design Component Hierarchy**: Parent-child relationships aligned with functionality flows
3. **Design Component Interfaces**: Props, state, events aligned with functionality needs
4. **Design Component Contracts**: Input contracts, output contracts, state contracts

**Reference**: `references/component-design.md` for detailed component design patterns, examples, and checklist.

## Component Design Pattern Library

**Reference**: See [PATTERNS.md](./PATTERNS.md) for detailed component design patterns including:

- Component structure (props, hierarchy, composition)
- State management patterns
- Component checklist

## Quick Reference

| Phase                         | Key Activities                             | Success Criteria                             |
| ----------------------------- | ------------------------------------------ | -------------------------------------------- |
| **1. Functionality Analysis** | Context-dependent analysis, flow questions | Component requirements identified            |
| **2. Project Patterns**       | Analyze component patterns, conventions    | Project patterns understood                  |
| **3. Component Design**       | Map flows to components, design hierarchy  | Components designed to support functionality |

## Reference Files

**For detailed component design guidance, see**:

- **PATTERNS.md**: Component design patterns, structure, state management, component checklist
- **`references/functionality-mapping.md`**: Functionality analysis, component requirement mapping, flow-to-component mapping, examples
- **`references/project-patterns.md`**: Project component pattern analysis, structure patterns, naming conventions, state management patterns, UI library patterns, composition patterns
- **`references/component-design.md`**: Component design patterns, hierarchy design, interface design, contract design, examples, checklist

## Priority Classification

**Critical (Must Have - Core Functionality)**:

- Components support core functionality (user flow, admin flow)
- Blocks functionality if missing
- Required for functionality to work

**Important (Should Have - Supporting Functionality)**:

- Components support functionality growth
- Components support functionality changes
- Components support functionality accessibility

**Minor (Can Defer - Pattern Compliance)**:

- Perfect component structure (if functionality is supported)
- Ideal composition patterns (if functionality is supported)
- Perfect prop types (if functionality is supported)

## Output Format

**MANDATORY TEMPLATE** - Use this exact structure:

```markdown
# Component Design Report

## Functionality Analysis Summary

[Brief summary of functionality from Phase 1]

## Project Component Patterns Summary

[Brief summary of project component patterns from Phase 2]

## Component Design

### Components

[For each component: Name, Purpose, Props, State, Hierarchy, Flow Step, Example, Priority]

### Component Hierarchy

[Component hierarchy mapped from functionality flows]

### Component Contracts

[Component interfaces and contracts aligned with functionality]

## Recommendations

[Prioritized list - Critical first, then Important, then Minor]
```

## Key Principles

1. **Functionality First**: Always understand functionality before designing components
2. **Context-Aware**: Understand project component patterns before designing
3. **Map Flows to Components**: Map functionality flows to component hierarchy
4. **Specific Designs**: Provide specific component designs with examples aligned with project patterns
5. **Prioritize by Impact**: Critical (core functionality) > Important (supporting functionality) > Minor (pattern compliance)

## Common Mistakes to Avoid

1. **Skipping Functionality Analysis**: Don't jump straight to component design
2. **Ignoring Project Patterns**: Don't design without understanding project component patterns
3. **Generic Component Patterns**: Don't apply generic patterns - design to support functionality
4. **Missing Specific Designs**: Don't just describe components - provide specific code examples aligned with project patterns
5. **No Flow Mapping**: Don't just list components - map them to functionality flows
6. **Wrong Priority**: Don't prioritize pattern compliance over functionality support

## Integration with Orchestrator

This skill is loaded by orchestrator workflows when component design is detected. The orchestrator coordinates:

- Functionality analysis (Phase 0)
- Skill loading (Phase 2)
- Component design execution

**CRITICAL**: Maintain functionality-first approach. Component design must follow functionality analysis.

---

## Troubleshooting

**Common Issues:**

1. **Component design without understanding functionality**
   - **Symptom**: Components designed but don't support functionality flows
   - **Cause**: Skipped functionality analysis
   - **Fix**: Complete functionality analysis first, then design components
   - **Prevention**: Always understand functionality before component design

2. **Generic component patterns instead of functionality-focused**
   - **Symptom**: Components follow generic patterns but don't support functionality
   - **Cause**: Didn't map functionality flows to component needs
   - **Fix**: Map flows to components, design to support flows
   - **Prevention**: Always map functionality to component needs first

3. **Component designs not aligned with project patterns**
   - **Symptom**: Components don't match project's component patterns
   - **Cause**: Didn't understand project component patterns
   - **Fix**: Understand project patterns, align component design
   - **Prevention**: Always understand project patterns first

**If issues persist:**

- Verify functionality analysis was completed first
- Check that functionality flows were mapped to components
- Ensure component designs align with project patterns
- Review reference files for detailed guidance

---

_This skill enables context-aware component design that understands component requirements from flows and designs components to support functionality, providing specific component designs with examples aligned with project component patterns._
