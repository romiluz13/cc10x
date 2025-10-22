# Coding Standards - cc10x

**Universal coding conventions for all cc10x development**

---

## Core Principles

1. **Clarity over cleverness** - Code should be self-explanatory
2. **Simplicity over complexity** - Solve simply first, optimize later
3. **Tests are mandatory** - No production code without tests (TDD)
4. **Consistency is key** - Follow existing patterns
5. **Quality is non-negotiable** - All quality gates must pass

---

## File Structure

### Skills

```
skills/
└── skill-name/
    ├── SKILL.md                    # Skill documentation
    └── script.ts                   # (Optional) Executable code
```

**SKILL.md format**:
```markdown
---
name: skill-name
description: One-line description (< 100 chars)
progressive: true                   # Enable progressive loading
---

# Skill Name

## Progressive Loading Stages

### Stage 1: Metadata (50 tokens)
- Essential info only
- What this skill provides
- When to use it

### Stage 2: Quick Reference (500 tokens)
- Core principles (5-7 rules)
- Common patterns (2-3 examples)
- Quick checklist

### Stage 3: Full Content (3000 tokens)
- Complete documentation
- Detailed examples
- Edge cases
- Anti-patterns

[Full content here...]
```

### Sub-Agents

```
agents/
└── agent-name.md
```

**agent-name.md format**:
```markdown
---
name: agent-name
description: One-line description (< 100 chars)
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
---

# Agent Name

You are [role description].

## Your Role
[Clear responsibilities]

## Automatic Skills
You MUST use these skills (automatic invocation):
- **skill-1**: Purpose
- **skill-2**: Purpose

## Workflow
[Step-by-step process]

## Remember
[Key constraints and rules]
```

### Commands

```
.claude-plugin/commands/
└── command-name.md
```

**command-name.md format**:
```markdown
---
name: command-name
description: One-line description (< 100 chars)
---

You are orchestrating [workflow name].

## Command Usage
```
/command-name <parameters>
```

## Workflow Overview
[Phases with arrows]

## Phase Details
[Detailed phase descriptions]

## Quality Gates
[Validation checkpoints]

## Remember
[Critical rules]
```

---

## Naming Conventions

### Files and Directories

```
✅ GOOD:
- kebab-case for files: test-driven-development.md
- kebab-case for directories: codebase-navigation/
- Descriptive names: verification-before-completion.md

❌ BAD:
- camelCase: testDrivenDevelopment.md
- snake_case: test_driven_development.md
- Abbreviations: tdd.md, ver-comp.md
```

### Skills and Agents

```
✅ GOOD:
name: test-driven-development
name: context-analyzer

❌ BAD:
name: TDD
name: contextAnalyzer
name: context_analyzer
```

### Commands

```
✅ GOOD:
name: feature-build
name: bug-fix

❌ BAD:
name: featureBuild
name: feature_build
```

---

## Documentation Style

### Headings

```markdown
# H1 - Title Only
## H2 - Major Sections
### H3 - Subsections
#### H4 - Rarely used
```

### Code Examples

```markdown
```typescript
// ✅ Good: Clear, commented, realistic
async function getUserById(id: string): Promise<User> {
  const user = await db.users.findOne({ id });
  if (!user) {
    throw new NotFoundError(`User not found: ${id}`);
  }
  return user;
}
```

```typescript
// ❌ Bad: No comments, unrealistic
function get(id) {
  return db.find(id);
}
```
```

### Checklists

```markdown
✅ GOOD format:
```
Quality Verification:
- [ ] Tests exist and pass
- [ ] All tests run (not just new ones)
- [ ] No errors or warnings
```

❌ BAD format:
1. Tests exist
2. All tests run
3. No errors
```

### Formatting

- **Bold** for emphasis: `**important**`
- *Italic* for definitions: `*term*`
- `Code` for inline code: `` `variable` ``
- > Blockquotes for warnings: `> Warning: ...`
- Lists use `-` (not `*` or `+`)

---

## Content Guidelines

### Be Concise

```
✅ GOOD (concise):
"Write failing test FIRST. No production code without failing test."

❌ BAD (verbose):
"Before you write any production code, it is absolutely critical and mandatory that you first write a test that fails, demonstrating that the feature you're about to implement does not currently exist..."
```

### Be Specific

```
✅ GOOD (specific):
"Run: npm test
Confirm: All tests pass, no errors, coverage >80%"

❌ BAD (vague):
"Make sure everything works and the tests are good"
```

### Use Examples

```
✅ GOOD (with example):
"Use PascalCase for classes:
```typescript
export class UserService { }
```
"

❌ BAD (no example):
"Use PascalCase for classes"
```

---

## Quality Standards

### Skills (SKILL.md)

**Requirements**:
- [ ] Progressive loading structure (Stage 1/2/3)
- [ ] Stage 1: <100 tokens (metadata only)
- [ ] Stage 2: <600 tokens (quick reference)
- [ ] Stage 3: <3500 tokens (full content)
- [ ] Clear examples for common patterns
- [ ] Anti-patterns documented
- [ ] Frontmatter complete (name, description, progressive)

### Sub-Agents (agent.md)

**Requirements**:
- [ ] Clear role definition
- [ ] Automatic skills listed
- [ ] Step-by-step workflow
- [ ] Constraints documented
- [ ] Frontmatter complete (name, description, tools, model)
- [ ] <1500 tokens total

### Commands (command.md)

**Requirements**:
- [ ] Usage example provided
- [ ] Workflow phases visualized
- [ ] Quality gates specified
- [ ] Parallel execution rules clear
- [ ] Error handling documented
- [ ] Frontmatter complete (name, description)
- [ ] <3000 tokens total

---

## Version Control

### Commit Messages

**Format**: Semantic commits

```bash
# Feature
git commit -m "feat: add user authentication"

# Bug fix
git commit -m "fix: resolve JWT expiration issue"

# Documentation
git commit -m "docs: update progressive loading guide"

# Refactor
git commit -m "refactor: simplify context loading logic"

# Test
git commit -m "test: add edge cases for TDD skill"
```

**Always include**:
```
feat: [description]

- [Change 1]
- [Change 2]
- [Change 3]

🤖 Generated with Claude Code (cc10x)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Branching

```
main - Production-ready code
develop - Active development (not used in early stage)
feature/* - Feature branches (if needed for major work)
```

---

## Testing Standards

### TDD Workflow

```
1. Write failing test (RED)
2. Verify test fails correctly
3. Write minimal code (GREEN)
4. Verify test passes
5. Refactor (keep green)
6. Repeat
```

**No exceptions** - All code follows TDD.

### Test File Naming

```
✅ GOOD:
src/features/auth/auth.service.ts
src/features/auth/auth.test.ts

tests/integration/api.test.ts
tests/e2e/user-flow.test.ts
```

---

## Error Handling

### Custom Error Classes

```typescript
// ✅ GOOD: Specific, contextual
class NotFoundError extends Error {
  constructor(message: string, public resourceId: string) {
    super(message);
    this.name = 'NotFoundError';
  }
}

throw new NotFoundError('User not found', userId);
```

```typescript
// ❌ BAD: Generic, no context
throw new Error('Not found');
```

### Try-Catch Pattern

```typescript
// ✅ GOOD: Specific error handling
try {
  const user = await fetchUser(id);
  return processUser(user);
} catch (error) {
  logger.error('Failed to process user', { userId: id, error });
  throw new UserProcessingError(
    `Failed to process user ${id}`,
    { cause: error }
  );
}
```

---

## Performance Considerations

### Token Efficiency

```
✅ GOOD:
- Progressive loading (5k vs 80k startup)
- Isolated sub-agent contexts
- Auto-healing at 75%

❌ BAD:
- Loading full docs upfront
- Sharing full conversation with sub-agents
- Hitting 200k limit
```

### Execution Speed

```
✅ GOOD:
- Parallel read-only agents (context, analysis, review)
- Sequential implementers (prevent conflicts)
- Quality gates early (fail fast)

❌ BAD:
- Parallel implementers (file conflicts)
- Skipping quality gates (bugs in production)
- Late validation (wasted work)
```

---

## Final Checklist

Before any commit:

```
Code Quality:
- [ ] Follows naming conventions
- [ ] Documentation is concise
- [ ] Examples are included
- [ ] Progressive loading (if skill)
- [ ] Frontmatter complete
- [ ] <3000 tokens (skills/commands)
- [ ] <1500 tokens (agents)

Testing (for code):
- [ ] Tests exist (TDD)
- [ ] Tests pass
- [ ] Coverage adequate

Standards:
- [ ] No debug code
- [ ] Error handling present
- [ ] Semantic commit message
- [ ] Co-authored by Claude
```

---

**Remember**: These standards ensure consistency, quality, and maintainability across the cc10x codebase.
