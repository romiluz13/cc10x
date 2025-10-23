# Commands Deep Dive

## What Are Commands?

Commands are user-invoked workflows that trigger specific orchestration sequences in Claude Code.

**Invocation:** `/command-name [arguments]`
**Purpose:** Entry points for structured workflows
**Format:** Markdown files with YAML frontmatter

## Command Anatomy

### File Structure
```
commands/feature-plan.md
```

### Basic Template
```markdown
---
name: command-name
description: One-line description
aliases: [alt1, alt2]  # Optional
---

# Command Title

Detailed instructions for executing this workflow...
```

## Command Types

### 1. Workflow Commands
Orchestrate multi-phase processes:
```markdown
---
name: feature-build
description: Implements features with 5-phase TDD workflow
---

Phases:
1. Context Analysis
2. Planning
3. Implementation (TDD-enforced)
4. Verification
5. Finalization
```

### 2. Generation Commands
Generate artifacts:
```markdown
---
name: generate-docs
description: Generates comprehensive documentation
---

Creates:
- README.md
- API documentation
- Code comments
- Examples
```

### 3. Analysis Commands
Perform analysis:
```markdown
---
name: analyze-codebase
description: Analyzes codebase patterns and quality
---

Analyzes:
- Code structure
- Complexity
- Test coverage
- Technical debt
```

### 4. Orchestration Commands
Coordinate agents:
```markdown
---
name: review
description: Multi-dimensional code review
---

Coordinates:
- Security reviewer
- Quality reviewer
- Performance analyzer
- UX reviewer
- Accessibility reviewer
```

## Best Practices

### Naming
✅ Verb-noun pattern: `feature-plan`, `bug-fix`, `code-review`
✅ Descriptive: Clear what it does
✅ Concise: 2-3 words maximum
✅ Hyphenated: Use kebab-case

### Description
✅ One clear sentence
✅ Explain value proposition
✅ Hint at workflow
✅ Include key features

### Content
✅ Phase-based structure
✅ Clear instructions per phase
✅ Quality gates between phases
✅ Examples of usage
✅ Expected outcomes

## Command Patterns

### Pattern 1: Multi-Phase Workflow
```markdown
## Phase 1: Preparation
- Gather context
- Understand requirements
- Plan approach

## Phase 2: Execution
- Implement solution
- Follow patterns
- Apply best practices

## Phase 3: Validation
- Run tests
- Check quality
- Verify requirements

## Phase 4: Finalization
- Clean up
- Document
- Commit changes
```

### Pattern 2: Agent Orchestration
```markdown
## Orchestration Flow

1. **Analyze** (Context Analyzer Agent)
   - Discover patterns
   - Understand codebase

2. **Implement** (Implementer Agent)
   - Write code
   - Follow TDD

3. **Review** (Multiple Review Agents in parallel)
   - Security check
   - Quality review
   - Performance analysis

4. **Finalize** (Main Claude)
   - Integrate feedback
   - Commit changes
```

### Pattern 3: Quality Gates
```markdown
## Execution with Gates

### Step 1: Write Tests
- Create test file
- Define test cases
- **GATE:** Tests must fail initially

### Step 2: Implement
- Write minimum code
- **GATE:** Tests must pass

### Step 3: Refactor
- Improve code quality
- **GATE:** Tests still pass

### Step 4: Commit
- Stage changes
- **GATE:** All tests pass
```

## Command Arguments

### Simple Arguments
```markdown
Usage: /command-name <required-arg>

Example:
/feature-plan "Add user authentication"
```

### Optional Arguments
```markdown
Usage: /command-name <feature> [--detail level]

Examples:
/feature-plan "Add auth" --detail minimal
/feature-plan "Add auth" --detail complete
```

### Flags
```markdown
Usage: /command-name [--flag]

Flags:
--skip-tests: Skip test generation
--force: Override safety checks
--verbose: Detailed output
```

## Examples from cc10x

### /feature-plan
```markdown
---
name: feature-plan
description: Creates comprehensive PRD-style feature plans
---

# Feature Planning Command

Generates detailed feature plans with:
- Requirements analysis
- Architecture decisions
- Component breakdown
- API contracts
- Testing strategy
- Implementation roadmap
```

### /feature-build
```markdown
---
name: feature-build
description: Implements features with TDD-enforced 5-phase workflow
---

# Feature Build Command

Five-phase implementation:
1. Context Analysis - Find patterns
2. Planning - Break into tasks
3. Implementation - TDD-enforced
4. Verification - Quality checks
5. Finalization - Clean commit
```

### /bug-fix
```markdown
---
name: bug-fix
description: Systematic debugging with LOG FIRST pattern
---

# Bug Fix Command

Systematic debugging:
1. Context - Understand issue
2. Investigation - LOG FIRST
3. Fix - Minimal change + test
4. Verify - Ensure fix works
5. Finalize - Clean commit
```

### /review
```markdown
---
name: review
description: Multi-dimensional parallel code review
---

# Code Review Command

Parallel review:
- Security vulnerabilities
- Code quality
- Performance bottlenecks
- UX improvements
- Accessibility compliance
```

## Resources

- **Format:** Markdown with YAML frontmatter
- **Location:** `commands/*.md`
- **Invocation:** `/command-name`
- **Examples:** See cc10x commands/
