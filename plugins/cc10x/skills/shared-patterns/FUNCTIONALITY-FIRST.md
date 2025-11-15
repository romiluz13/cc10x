# Functionality First Pattern

This is a shared pattern used across all consolidated skills. It ensures that functionality analysis is completed before applying specialized checks.

## Core Principle

**Understand what functionality needs to be built/reviewed/debugged/planned FIRST, then apply specialized checks.**

## Mandatory Steps

### Step 1: Context-Dependent Functionality Analysis

**BEFORE applying any specialized checks, complete functionality analysis**:

1. **Load Functionality Analysis Template**:
   - Reference: `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md`
   - Complete Phase 1: Universal Questions
   - Complete Phase 2: Context-Dependent Flow Questions (based on code type)

2. **Understand Functionality**:
   - What is this code supposed to do?
   - What functionality does user need?
   - What are the flows? (User, Admin, System, Integration, etc.)

3. **Verify Functionality Works** (for review/debug):
   - Does functionality work? (tested)
   - Do flows work? (tested)
   - Does error handling work? (tested)

### Step 2: Understand Project Patterns

**BEFORE checking, understand how this project handles patterns**:

1. **Map Project Patterns**:

   ```bash
   # Find project patterns
   grep -r "pattern" --include="*.md" --include="*.ts" --include="*.tsx" plugins/cc10x/skills/ | head -20
   ```

2. **Understand Project Conventions**:
   - How does this project handle similar patterns?
   - What conventions are used?
   - What patterns are established?

### Step 3: Apply Specialized Checks

**ONLY AFTER functionality analysis and pattern understanding**:

- Apply specialized checks (security, quality, performance, UX, etc.)
- Focus on issues that affect functionality
- Provide specific fixes aligned with project patterns

## Universal Questions (Phase 1)

From functionality analysis template:

- **Purpose**: What problem does this solve?
- **Requirements**: What must it do?
- **Constraints**: What are the limits?
- **Dependencies**: What does it need?
- **Edge Cases**: What can go wrong?
- **Verification**: How do we know it works?
- **Context**: Where does it fit?

## Context-Dependent Flow Questions (Phase 2)

Based on code type:

- **UI Features** → User Flow, Admin Flow, System Flow
- **Backend APIs** → Request Flow, Response Flow, Error Flow, Data Flow
- **Utilities** → Input Flow, Processing Flow, Output Flow, Error Flow
- **Integrations** → Integration Flow, Data Flow, Error Flow, State Flow
- **Database** → Migration Flow, Query Flow, Data Flow, State Flow

## Reference

See `plugins/cc10x/skills/cc10x-orchestrator/templates/functionality-analysis.md` for complete template.
