# Sub-Agents Deep Dive

## What Are Sub-Agents?

Sub-agents are **specialized AI assistants** within Claude Code that handle specific tasks with focused expertise. Think of them as expert consultants you can call upon for specialized work.

**Key Characteristics:**
- Isolated context window (task-focused)
- Custom system prompt (role-specific)
- Tool permissions (security-scoped)
- Auto or manual invocation

## Sub-Agents vs Main Claude

### Main Claude
- General-purpose assistant
- Broad knowledge
- Handles coordination
- Dispatches to specialists

### Sub-Agents
- Domain experts
- Focused expertise
- Isolated context
- Single responsibility

**Analogy:** Main Claude is the project manager, sub-agents are specialized engineers.

## Configuration

### File Structure
```
.claude/agents/security-reviewer.md      # Project-level
~/.claude/agents/code-optimizer.md       # User-level
```

### Basic Template
```markdown
---
name: agent-name
description: What this agent specializes in
tools: ["read_file", "grep", "codebase_search"]
---

# Agent Name

System prompt defining the agent's behavior, expertise, and approach.

## When to Use This Agent

Examples of situations where this agent should be invoked...
```

### Complete Example
```markdown
---
name: security-reviewer
description: Expert security auditor for code review
tools: [
  "read_file",
  "grep",
  "codebase_search",
  "run_terminal_cmd"
]
auto_invoke: true
priority: 8
---

# Security Reviewer Agent

You are an expert security auditor specializing in application security.

## Your Role

- Identify security vulnerabilities
- Check authentication/authorization
- Review input validation
- Assess cryptographic implementations
- Evaluate API security
- Check for OWASP Top 10 issues

## Approach

1. **Scan for Common Vulnerabilities**
   - SQL injection points
   - XSS vulnerabilities
   - CSRF tokens
   - Authentication flaws

2. **Review Security Patterns**
   - Input sanitization
   - Output encoding
   - Secure session management
   - Proper error handling

3. **Check Best Practices**
   - Principle of least privilege
   - Defense in depth
   - Fail securely
   - No security through obscurity

## Tools Usage

- `read_file`: Read code for review
- `grep`: Search for security patterns
- `codebase_search`: Find similar vulnerabilities
- `run_terminal_cmd`: Run security scanners

## Output Format

Provide findings as:
```
# Security Review Results

## Critical Issues
- [Issue 1]
- [Issue 2]

## Warnings
- [Warning 1]

## Recommendations
- [Recommendation 1]
```

## When to Invoke

Automatically activate when:
- User mentions "security review"
- Code review requested
- Authentication/authorization changes
- External API integration
```

## Invocation Methods

### 1. Automatic (Recommended)
```markdown
---
auto_invoke: true
---
```
Claude detects context and invokes automatically.

**Triggers:**
- User mentions agent role ("security review", "performance check")
- Task matches agent expertise
- Code context suggests need

### 2. Explicit via Task Delegation
```
Main Claude decides:
"This requires security expertise. Let me delegate to security-reviewer agent."

Invokes sub-agent explicitly
Sub-agent completes task
Returns results to main Claude
```

### 3. Manual via Command
```markdown
User can request specific agent:
"Use the security-reviewer agent to check this code"
```

## Tool Permissions

### Why Restrict Tools?

**Security:** Agents only get tools they need
**Performance:** Fewer tools = faster decisions
**Clarity:** Clear scope of capabilities

### Common Tool Sets

**Reader Agent:**
```yaml
tools: ["read_file", "list_dir", "grep"]
```

**Analyzer Agent:**
```yaml
tools: ["read_file", "grep", "codebase_search"]
```

**Implementer Agent:**
```yaml
tools: ["read_file", "search_replace", "write", "run_terminal_cmd"]
```

**Reviewer Agent:**
```yaml
tools: ["read_file", "grep", "codebase_search"]
```

**Full Access Agent:**
```yaml
tools: ["*"]  # All available tools
```

## Context Isolation

### The Problem Without Isolation
```
Main Claude context: 150k tokens
Task A context: +30k tokens
Task B context: +40k tokens
Task C context: +50k tokens
Total: 270k tokens → Context overflow!
```

### The Solution With Sub-Agents
```
Main Claude: 10k tokens (coordination only)
Sub-agent A: 30k tokens (isolated, disposed after)
Sub-agent B: 40k tokens (isolated, disposed after)
Sub-agent C: 50k tokens (isolated, disposed after)
No overflow, efficient memory usage!
```

## Agent Patterns

### Pattern 1: Reviewer Agent
```markdown
---
name: code-quality-reviewer
description: Reviews code for quality and maintainability
tools: ["read_file", "grep", "codebase_search"]
---

Reviews code against quality standards:
- Code smells
- Design patterns
- Maintainability
- Test coverage
```

**Use Case:** Code review workflows

### Pattern 2: Implementer Agent
```markdown
---
name: feature-implementer
description: Implements features following TDD
tools: ["read_file", "search_replace", "write", "run_terminal_cmd"]
---

Implements features with test-first approach:
- Write tests first
- Implement functionality
- Refactor for quality
- Verify all tests pass
```

**Use Case:** Feature development workflows

### Pattern 3: Analyzer Agent
```markdown
---
name: context-analyzer
description: Analyzes codebase for patterns and conventions
tools: ["read_file", "grep", "codebase_search"]
---

Discovers project patterns:
- File structure conventions
- Naming patterns
- Common libraries
- Architectural decisions
```

**Use Case:** Before implementing changes

### Pattern 4: Specialist Agent
```markdown
---
name: performance-optimizer
description: Optimizes code for performance
tools: ["read_file", "grep", "codebase_search", "run_terminal_cmd"]
---

Identifies and fixes performance issues:
- Slow database queries
- Inefficient algorithms
- Memory leaks
- Unnecessary re-renders
```

**Use Case:** Performance improvement workflows

## Multi-Agent Coordination

### Sequential Pattern
```
Workflow:
1. Analyzer Agent → Discovers patterns
2. Implementer Agent → Writes code
3. Reviewer Agent → Reviews quality
4. Main Claude → Integrates results
```

**Use Case:** Feature development with quality gates

### Parallel Pattern
```
Workflow:
              ┌─ Security Reviewer
Main Claude ──┼─ Quality Reviewer
              ├─ Performance Analyzer
              └─ UX Reviewer
                      ↓
              Aggregate results
```

**Use Case:** Multi-dimensional code review

### Hierarchical Pattern
```
Main Claude (Orchestrator)
    ↓
Senior Engineer Agent (Coordinator)
    ├─ Backend Specialist
    ├─ Frontend Specialist
    └─ DevOps Specialist
```

**Use Case:** Complex projects with sub-specializations

## Agent Communication

### Handoff Pattern
```
Agent A completes task:
"I've implemented the authentication feature.
 Passing to security-reviewer for audit."

Agent B receives context:
"Reviewing authentication implementation from Agent A..."
```

### Results Pattern
```
Agent completes:
"Task completed. Results:
 - Created 3 files
 - Modified 2 files
 - All tests passing
 
 Ready for next phase."

Main Claude:
"Excellent. Proceeding to review phase..."
```

## Best Practices

### 1. Single Responsibility
✅ **Do:** One agent, one focus
```
security-reviewer → Security only
performance-optimizer → Performance only
```

❌ **Don't:** Jack-of-all-trades
```
general-reviewer → Everything (too broad)
```

### 2. Clear Role Definition
✅ **Do:** Specific expertise
```
name: rails-code-reviewer
description: Expert in Ruby on Rails code review
```

❌ **Don't:** Vague role
```
name: code-helper
description: Helps with code
```

### 3. Appropriate Tool Access
✅ **Do:** Minimum necessary tools
```
tools: ["read_file", "grep"]  # Reader needs these
```

❌ **Don't:** All tools always
```
tools: ["*"]  # Unless truly needed
```

### 4. Clear Invocation Triggers
✅ **Do:** Specific contexts
```
## When to Use
- Security review requested
- Authentication changes
- External API integration
```

❌ **Don't:** Always active
```
## When to Use
- Everything
```

### 5. Quality Output Format
✅ **Do:** Structured results
```
## Security Review Results
### Critical Issues
### Warnings
### Recommendations
```

❌ **Don't:** Unstructured text
```
Found some issues, here they are...
```

## Common Agent Types

### Development Agents
- `implementer` - Writes code
- `refactorer` - Improves code
- `debugger` - Fixes bugs
- `test-writer` - Creates tests

### Review Agents
- `code-quality-reviewer` - Quality check
- `security-reviewer` - Security audit
- `performance-analyzer` - Performance review
- `ux-reviewer` - UX assessment
- `accessibility-reviewer` - Accessibility check

### Analysis Agents
- `context-analyzer` - Pattern discovery
- `architecture-analyst` - Design review
- `dependency-analyzer` - Dependency audit
- `complexity-analyzer` - Complexity metrics

### Specialized Agents
- `frontend-specialist` - React/Vue/Angular
- `backend-specialist` - Node/Python/Rails
- `database-expert` - SQL/NoSQL optimization
- `devops-specialist` - Infrastructure/CI/CD

## Agent Lifecycle

### 1. Definition
Create agent file with role and tools

### 2. Registration
Claude Code loads agent at session start

### 3. Invocation
Agent activated when needed

### 4. Execution
Agent completes task with isolated context

### 5. Results
Agent returns results, context disposed

### 6. Cleanup
Agent context released, memory freed

## Management Commands

### View Agents
```bash
/agents
```
Shows list of available agents

### Create Agent
```bash
/agents
# Interactive menu: Create new agent
```

### Edit Agent
```bash
/agents
# Interactive menu: Select and edit
```

### Delete Agent
```bash
/agents
# Interactive menu: Select and delete
```

## Debugging Agents

### Agent Not Invoking?

**Check:**
1. File location correct? (`.claude/agents/` or `~/.claude/agents/`)
2. Valid YAML frontmatter?
3. Clear invocation triggers in description?
4. Auto-invoke enabled?

### Agent Failing?

**Check:**
1. Required tools available?
2. Tool permissions correct?
3. System prompt clear?
4. Error handling present?

### Agent Slow?

**Check:**
1. Too many tools? (reduce to minimum)
2. Context too large? (focus scope)
3. Complex prompt? (simplify)
4. Unnecessary file reads? (optimize)

## Examples from cc10x

### Context Analyzer
```markdown
---
name: context-analyzer
description: Analyzes codebase patterns before implementation
tools: ["read_file", "grep", "codebase_search", "list_dir"]
---

Discovers project conventions:
- File structure patterns
- Naming conventions
- Common libraries
- Testing patterns
- Code organization
```

### Implementer
```markdown
---
name: implementer
description: Implements features using TDD
tools: ["read_file", "search_replace", "write", "run_terminal_cmd"]
---

TDD-enforced implementation:
- Write tests first
- Make tests fail
- Implement features
- Make tests pass
- Refactor
```

### Security Reviewer
```markdown
---
name: security-reviewer
description: Audits code for security vulnerabilities
tools: ["read_file", "grep", "codebase_search"]
---

Security audit:
- OWASP Top 10
- Authentication/authorization
- Input validation
- Injection vulnerabilities
- Cryptography review
```

## Resources

- **Official Docs:** https://docs.anthropic.com/en/docs/claude-code/sub-agents
- **Management:** Use `/agents` command
- **Examples:** Search GitHub for "claude sub-agents"
- **Best Practices:** Study successful implementations

