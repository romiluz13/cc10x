---
name: project-structure-generation
description: Use when planning features and user request contains "project structure", "create doc", "generate project docs" - generates project structure documentation describing directory organization, file patterns, and architectural organization extracted from codebase analysis
---

# Project Structure Generation

## Overview

Generate project structure documentation describing directory organization, file patterns, and architectural organization extracted from codebase analysis. This helps developers understand how the project is organized and where to find specific types of files.

## Quick Start

Generate project structure documentation by analyzing codebase organization.

**Example:**

1. **Detect trigger**: User says "generate project docs" or "create project structure"
2. **Analyze structure**: Scan directories, identify patterns (components/, utils/, tests/)
3. **Extract patterns**: File naming conventions, organization principles
4. **Generate doc**: Create `project-structure.mdc` with directory tree and patterns

**Result:** Complete project structure documentation for onboarding and planning.

## When to Use

- User request contains "project structure", "create doc", "generate project docs"
- Documenting project organization for new team members
- Understanding codebase structure before planning features
- Creating project onboarding documentation

## Process

### 1. Directory Structure Analysis

- Scan project root directory structure
- Identify main directories and their purposes
- Analyze nested directory patterns
- Identify file organization patterns
- Extract architectural organization principles

### 2. File Pattern Analysis

- Identify file naming conventions
- Extract file type patterns (components, utilities, tests, etc.)
- Analyze file organization within directories
- Identify module boundaries and dependencies

### 3. Generate Structure Documentation

Create documentation covering:

- **Root Directory:** Main directories and their purposes
- **Source Structure:** Source code organization patterns
- **Test Structure:** Test file organization
- **Configuration:** Config file locations and purposes
- **Documentation:** Documentation file organization
- **Build Artifacts:** Build output locations

### 4. Save and Organize

- Create `.cursor/rules/` or `.claude/docs/` directory if needed
- Save as `project-structure.mdc`
- Include visual directory tree representation

## Document Structure

The generated document must include:

### Root Directory Overview

- Main directories and their purposes
- Configuration files location
- Documentation files location

### Source Code Organization

- Source directory structure
- Component organization patterns
- Utility and helper organization
- API/route organization

### Test Organization

- Test directory structure
- Test file naming conventions
- Test organization patterns

### Configuration Files

- Configuration file locations
- Purpose of each config file
- Environment-specific configurations

### Build and Output

- Build artifact locations
- Output directory structure
- Distribution patterns

## Output

- **Format:** Markdown (`.mdc`)
- **Location:** `.cursor/rules/` or `.claude/docs/`
- **Filename:** `project-structure.mdc`

## Integration with cc10x Orchestrator

This skill is invoked automatically by the PLAN workflow Phase 2 when:

- User request contains "project structure" keywords
- Missing project structure documentation is detected
- Structure documentation generation intent is identified

The skill executes BEFORE requirements intake, ensuring project structure is documented for planning.

## Troubleshooting

**Common Issues:**

1. **Structure documentation not generated**
   - **Symptom**: User requested but no documentation created
   - **Cause**: Trigger keywords not detected or skill not invoked
   - **Fix**: Check trigger keywords ("project structure", "create doc"), invoke skill manually if needed
   - **Prevention**: Verify trigger keywords in user request

2. **Incomplete structure analysis**
   - **Symptom**: Documentation missing directories or patterns
   - **Cause**: Didn't complete all analysis steps
   - **Fix**: Complete all 4 steps: directory analysis, file patterns, generate doc, save
   - **Prevention**: Always complete all analysis steps

3. **Documentation not saved in correct location**
   - **Symptom**: Documentation created but not in `.cursor/rules/` or `.claude/docs/`
   - **Cause**: Wrong save location
   - **Fix**: Save to `.cursor/rules/` or `.claude/docs/` as `project-structure.mdc`
   - **Prevention**: Always use correct save location

**If issues persist:**

- Verify trigger keywords were detected
- Check that all analysis steps were completed
- Ensure documentation saved to correct location
- Review process steps in skill
