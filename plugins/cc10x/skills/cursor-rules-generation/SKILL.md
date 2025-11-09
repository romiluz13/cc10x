---
name: cursor-rules-generation
description: Use when planning features and user request contains "cursor rules", "create rule", "generate cursor rules" - generates Cursor rules documentation based on project patterns, conventions, and best practices extracted from codebase analysis
---

# Cursor Rules Generation

## Overview

Generate Cursor rules documentation based on project patterns, conventions, and best practices extracted from codebase analysis. Cursor rules help Claude Code understand project-specific conventions, coding standards, and architectural patterns.

## When to Use

- User request contains "cursor rules", "create rule", "generate cursor rules"
- Setting up new project conventions
- Documenting project-specific patterns and standards
- Onboarding new team members to project conventions

## Process

### 1. Codebase Pattern Analysis

- Analyze existing code patterns and conventions
- Identify naming conventions (files, functions, variables)
- Extract architectural patterns (component structure, API patterns)
- Identify testing patterns and conventions
- Extract code organization patterns

### 2. Configuration File Analysis

- Review existing `.cursor/rules/` files
- Check for existing conventions documentation
- Identify missing rule categories
- Analyze project structure for implicit conventions

### 3. Generate Cursor Rules

Create rule files covering:

- **Project Structure:** Directory organization, file naming
- **Code Style:** Formatting, naming conventions, code organization
- **Architecture Patterns:** Component patterns, API patterns, data flow
- **Testing Conventions:** Test structure, naming, patterns
- **Documentation Standards:** Comment style, README structure
- **Git Workflow:** Commit messages, branch naming, PR conventions

### 4. Save and Organize

- Create `.cursor/rules/` directory if needed
- Save rule files with descriptive names
- Update project documentation references

## Rule Categories

### Project Structure Rules

- Directory organization patterns
- File naming conventions
- Module organization principles

### Code Style Rules

- Formatting standards
- Naming conventions (camelCase, PascalCase, kebab-case)
- Code organization principles
- Import/export patterns

### Architecture Rules

- Component patterns
- API design patterns
- State management patterns
- Data flow conventions

### Testing Rules

- Test file organization
- Test naming conventions
- Testing patterns and best practices
- Mock/stub conventions

### Documentation Rules

- Comment style and standards
- README structure
- Code documentation patterns
- API documentation standards

## Output

- **Format:** Markdown (`.mdc`)
- **Location:** `.cursor/rules/`
- **Filename:** `[category]-rules.mdc` (e.g., `code-style-rules.mdc`, `architecture-rules.mdc`)

## Integration with cc10x Orchestrator

This skill is invoked automatically by the PLAN workflow Phase 2 when:

- User request contains "cursor rules" keywords
- Missing Cursor rules documentation is detected
- Rule generation intent is identified

The skill executes BEFORE requirements intake, ensuring project conventions are documented for planning.
