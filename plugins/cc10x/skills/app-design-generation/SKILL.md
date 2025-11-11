---
name: app-design-generation
description: Use when planning features and user request contains "app design", "design doc", "create design document" - generates comprehensive application design document based on deep codebase analysis and user input, providing high-level overview of architecture, core features, user experience, and business logic
---

# App Design Generation

## Overview

Generate comprehensive Application Design Document based on deep codebase analysis and user input. The document provides a high-level overview of the application's architecture, core features, user experience, and business logic while remaining technology-agnostic and focused on the "what" rather than the "how".

## Quick Start

Generate app design document by analyzing codebase and user input.

**Example:**

1. **Detect trigger**: User says "create design document" or "app design"
2. **Analyze codebase**: Deep dive into structure, features, user flows
3. **Interactive Q&A**: Ask about architecture, features, business logic
4. **Generate doc**: Create comprehensive design document with architecture, features, UX

**Result:** Complete application design document for planning and onboarding.

## When to Use

- User request contains "app design", "design doc", "create design document"
- Planning new features and need high-level design documentation
- Onboarding new team members who need application overview
- Documenting application architecture and business logic

## Process

### 1. Initial Analysis

- Analyze project structure and existing codebase
- Review package.json for project name and dependencies
- Check for existing documentation in .cursor/rules/
- Identify key application features and patterns
- Think deeply about the application's purpose and architecture

### 2. Codebase Deep Dive

Analyze the codebase to understand:

- **Application Structure:** Main modules, features, and components
- **User Flows:** Authentication, navigation, key user journeys
- **Data Models:** Conceptual relationships and entities
- **Business Logic:** Core rules, workflows, and processes
- **Integrations:** External services and APIs
- **Security Patterns:** Authentication and authorization approaches

### 3. Interactive Q&A Session

**CRITICAL:** Ask project stage question FIRST, then 4-7 additional questions:

- Use lettered/numbered options for easy response
- Focus on business goals and user needs
- Gather context for proper documentation

**Required Questions:**

1. **Project Stage Assessment** (Ask First!):
   - Pre-MVP / MVP / Production / Enterprise

2. **Application Purpose & Users:**
   - What is the primary problem your application solves?
   - Who are your target users and what are their main goals?

3. **Unique Value Proposition:**
   - What makes your application unique compared to existing solutions?

4. **User Roles & Permissions:**
   - What different types of users interact with your system?

5. **Core User Journeys:**
   - What are the 2-3 most critical user flows?

6. **Business Model & Growth:**
   - How does this application generate value?

7. **Integration Ecosystem:**
   - What external services must you integrate with?

### 4. Update Project Configuration

Based on project stage response:

- Update `.cursor/rules/project-status.mdc` with current stage
- Set appropriate DO/DON'T priorities for the stage
- Document stage-specific development guidelines

### 5. Generate Document

Create comprehensive app design document following standard structure:

- Introduction (overview, purpose, target audience, value proposition)
- Core Features (feature categories with purpose, functionalities, UX considerations)
- User Experience (personas, journeys, interface principles, accessibility)
- System Architecture (components, data flow, integrations, security)
- Business Logic (rules, processes, data models, workflows, validation)
- Future Considerations (enhancements, scalability, integrations, roadmap)

### 6. Save and Organize

- Create `.cursor/rules/` directory if needed
- Save as `app-design-document.mdc`
- Suggest next steps (tech stack doc, PRD, etc.)

## Document Structure

The generated document must follow this high-level structure:

### Introduction

- Application overview and purpose
- Target audience and user base
- Core value proposition
- Business context and goals

### Core Features

- Feature Category 1: Purpose, functionalities, UX considerations
- Feature Category 2: Purpose, functionalities, UX considerations
- [Additional feature categories as needed]

### User Experience

- User personas and roles
- Key user journeys and flows
- Interface design principles
- Accessibility and usability considerations

### System Architecture

- High-level system components
- Data flow and relationships
- Integration points and external services
- Security and privacy approach

### Business Logic

- Core business rules and processes
- Data models and relationships (conceptual)
- Workflow and state management
- Validation and business constraints

### Future Considerations

- Planned enhancements and features
- Scalability considerations
- Potential integrations
- Long-term vision and roadmap

## Writing Principles

### DO:

- **Business Focus:** Describe WHAT the application does, not HOW
- **User Value:** Emphasize benefits and outcomes for users
- **Clear Language:** Write for non-technical stakeholders
- **Visual Thinking:** Use diagrams and flows where helpful
- **Future Ready:** Consider growth and evolution paths

### DON'T:

- **Technical Details:** No code snippets or implementation specifics
- **Technology Stack:** Save for tech-stack.mdc document
- **Database Schemas:** Keep data models conceptual
- **API Specifications:** Focus on capabilities, not endpoints
- **Performance Metrics:** Describe goals, not technical benchmarks

- Suggest next steps (tech stack doc, PRD, etc.)

## Troubleshooting

**Common Issues:**

1. **Design document not generated**
   - **Symptom**: User requested but no document created
   - **Cause**: Trigger keywords not detected or skill not invoked
   - **Fix**: Check trigger keywords ("app design", "design doc"), invoke skill manually if needed
   - **Prevention**: Verify trigger keywords in user request

2. **Incomplete codebase analysis**
   - **Symptom**: Document missing key features or architecture details
   - **Cause**: Didn't complete deep codebase analysis
   - **Fix**: Complete all analysis steps: structure, features, flows, models, integrations
   - **Prevention**: Always complete deep codebase analysis

3. **Document not saved in correct location**
   - **Symptom**: Document created but not in `.cursor/rules/`
   - **Cause**: Wrong save location
   - **Fix**: Save to `.cursor/rules/` as `app-design-document.mdc`
   - **Prevention**: Always use correct save location

**If issues persist:**

- Verify trigger keywords were detected
- Check that deep codebase analysis was completed
- Ensure document saved to correct location
- Review process steps in skill

## Output

- **Format:** Markdown (`.mdc`)
- **Location:** `.cursor/rules/`
- **Filename:** `app-design-document.mdc`

## Integration with cc10x Orchestrator

This skill is invoked automatically by the PLAN workflow Phase 2 when:

- User request contains documentation keywords
- Missing design documentation is detected
- Documentation generation intent is identified

The skill executes BEFORE requirements intake, ensuring design documentation is available for planning.
