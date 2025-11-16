# Planning Patterns Library

This document provides a comprehensive library of planning patterns covering requirements analysis, tech stack research, feature planning, and technical writing.

## Requirements Analysis Patterns

### Requirements Discovery Patterns

- **Socratic questioning approach**: Ask "why" before "how" to understand root needs
- **Stakeholder analysis**: Identify all stakeholders and their needs
- **Context understanding**: Understand business context before technical solutions
- **Completeness validation**: Ensure all functionality flows have requirements before implementation
- **PRD creation framework**: Structure Product Requirements Document with clear sections

### Requirements Gathering Patterns

- Stakeholder interviews
- User story mapping
- Use case analysis
- Requirement documentation

### Requirements Mapping Patterns

- Map requirements to user flows
- Map requirements to system flows
- Map requirements to integration flows
- Document requirement mappings

### Gap Identification Patterns

- Identify missing requirements
- Identify conflicting requirements
- Identify ambiguous requirements
- Document gaps

### Acceptance Criteria Patterns

- Given-When-Then format
- Testable criteria
- Functionality-aligned criteria
- Measurable outcomes

## Tech Stack Research Patterns

### Technology Evaluation Patterns

- **Always provide 2-3 options**: Compare alternatives with pros/cons
- **Evidence-based recommendations**: Back suggestions with examples, benchmarks, real-world usage
- **Integration assessment**: Evaluate how new tech integrates with existing stack
- **Cost analysis**: Consider API usage, infrastructure costs, quotas
- **Migration path**: Assess how changes affect existing features
- **Performance implications**: Evaluate optimization strategies and trade-offs

### Comparison Framework Patterns

- **Feature analysis**: Understand requirements + technical challenges
- **Recommended approach**: Primary recommendation with integration points
- **Alternative options**: 1-2 viable alternatives with trade-offs
- **Implementation considerations**: DB schema, API structure, state management, security
- **Next steps**: Concrete action items

### Trade-off Analysis Patterns

- Development complexity vs feature completeness
- Build-vs-buy decisions
- Immediate vs future needs
- Performance vs maintainability
- Cost vs functionality

### Context Analysis Patterns

- Full awareness of existing stack (frameworks, libraries, services)
- Edge runtime compatibility checks
- Cost considerations (API usage, infrastructure, quotas)
- Migration path assessment
- Performance implications

## Feature Planning Patterns

### Feature Breakdown Patterns

- **Feature breakdown methodology**: Break features into smaller, manageable pieces
- **Solo developer estimation**: Double initial estimate for realistic timelines
- **Phased implementation**: Implement in phases with clear milestones
- **Success criteria definition**: Define clear, measurable success criteria
- **Rollout planning**: Plan gradual rollout with monitoring

### Architecture Design Patterns

- Component breakdown
- System boundaries
- Integration points
- Technology selection

### Component Design Patterns

- Component responsibilities
- Component interfaces
- Component dependencies
- Component composition

### Implementation Roadmap Patterns

- Phased implementation
- Dependency ordering
- Risk mitigation
- Timeline estimation

### Complexity Assessment Patterns

- 1-5 complexity scale
- LOC estimation
- File count estimation
- Risk assessment
- Solo developer estimation (double initial estimate)

## Technical Writing Patterns

### Audience-First Writing Patterns

- **Understand audience**: Know who reads the documentation (developers, users, stakeholders)
- **Clarity over completeness**: Prioritize clear, actionable content over exhaustive coverage
- **Working examples always**: Include real, runnable examples in every section
- **Scan-friendly structure**: Use headings, lists, code blocks for easy scanning
- **Task completion focus**: Structure content around completing tasks, not explaining concepts

### Documentation Structure Patterns

- **Progressive disclosure**: Start simple, add complexity gradually
- **Task-oriented organization**: Organize by what users need to do, not by technical concepts
- **Quick start sections**: Provide immediate value with quick start guides
- **Reference sections**: Separate reference material from tutorials
- **Examples-first approach**: Lead with examples, explain concepts after

### Writing Quality Patterns

- **Active voice**: Use active voice for clarity
- **Specific language**: Avoid vague terms, be specific
- **Code examples**: Include complete, runnable code examples
- **Visual aids**: Use diagrams, screenshots, flowcharts when helpful
- **Error handling**: Document common errors and solutions

## Pattern Usage

Reference these patterns when planning:

1. **Requirements Analysis**: Use discovery, gathering, mapping, gap identification, acceptance criteria patterns
2. **Tech Stack Research**: Use evaluation, comparison framework, trade-off analysis, context analysis patterns
3. **Feature Planning**: Use feature breakdown, architecture design, component design, roadmap, complexity assessment patterns
4. **Technical Writing**: Use audience-first, documentation structure, writing quality patterns

## Pattern Composition

These patterns can be composed together:

- Requirements Discovery + Requirements Mapping = Complete requirements analysis
- Tech Stack Research + Feature Planning = Informed feature planning
- Requirements Analysis + Feature Planning = Complete planning
- Architecture Design + Component Design = Comprehensive design
- Requirements Mapping + Acceptance Criteria = Testable planning
- Feature Planning + Technical Writing = Complete documentation

See `plugins/cc10x/skills/shared-patterns/PATTERN-COMPOSITION.md` for composition guidelines.
