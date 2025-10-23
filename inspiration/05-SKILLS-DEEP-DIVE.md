# Agent Skills Deep Dive

## What Are Agent Skills?

Agent Skills are **instruction manuals** that teach Claude Code WHEN and HOW to use capabilities automatically, without explicit user commands.

**Announced:** October 16, 2025 by Anthropic
**Purpose:** Auto-activating capabilities that Claude loads based on context
**Key Feature:** No slash command needed - natural language activation

## The Four-Step Flow

### 1. DISCOVERY (Marketplace)
```
User browses marketplace
Finds plugin with useful skills
Installs: /plugin install plugin-name@marketplace
```

### 2. INSTALLATION (Files Copied)
```
Plugin files copied to system
Including skills/*/SKILL.md files
Ready for Claude to discover
```

### 3. STARTUP (Claude Learns)
```
Claude Code reads SKILL.md frontmatter from ALL installed plugins
Loads trigger phrases: "ansible playbook", "security audit"
Now Claude knows these skills exist and when to use them
```

### 4. USAGE (Automatic Activation)
```
User: "Create an Ansible playbook for Apache"
Claude: Sees "ansible playbook" trigger → reads full SKILL.md
Claude: Activates skill with correct workflow automatically!
```

## Real Example: Before vs After

### WITHOUT Agent Skills
```
User: "Create ansible playbook"
Claude: "I have ansible-playbook-creator installed somewhere...
         Let me manually search and figure out how to use it..."
Result: ❌ Plugin sits unused, you have to name it explicitly
```

### WITH Agent Skills
```
User: "Create ansible playbook"
Claude: *Recognizes trigger phrase instantly*
        *Reads SKILL.md for workflow*
        "I'll use ansible-playbook-creator for this!"
        *Automatically applies best practices*
Result: ✅ Instant activation, correct usage, zero thinking
```

## SKILL.md Anatomy

### Required Structure

```markdown
---
name: "Skill Name"
description: |
  What the skill does. Use when you need X.
  Trigger with "keyword" or "create Y for Z".
---

## How It Works
1. Step-by-step process
2. Best practices included
3. Error handling built-in

## When to Use This Skill
- Specific situation 1
- Specific situation 2
- Specific situation 3

## Examples
User: "Example request"
Skill activates → Process → Output
```

### What Goes in SKILL.md

**1. Description (YAML frontmatter):**
- Clear purpose statement
- Trigger phrases (critical!)
- When to use hints
- Keep it concise but complete

**2. How It Works:**
- Multi-phase workflow
- Step-by-step instructions
- Decision points
- Best practices

**3. When to Use:**
- Clear activation scenarios
- User intent patterns
- Context clues
- Example phrases

**4. Examples:**
- Real-world use cases
- Input → Process → Output
- Multiple scenarios
- Edge cases

**5. Code Examples (if applicable):**
- Templates
- Patterns
- Common structures
- Error handling

## Trigger Phrases: The Secret Sauce

Trigger phrases in the description tell Claude WHEN to activate.

### Good Trigger Phrases

✅ **Specific and action-oriented:**
```yaml
description: |
  Creates Ansible playbooks for infrastructure automation.
  Use when you need to "create ansible playbook" or "automate
  server configuration" or "deploy infrastructure as code".
```

✅ **Multiple variations:**
```yaml
description: |
  Performs security audits. Trigger with "security audit",
  "check for vulnerabilities", "review security", or "scan for issues".
```

✅ **Context-aware:**
```yaml
description: |
  Optimizes database queries. Use when user mentions "slow queries",
  "database performance", "optimize SQL", or "speed up database".
```

### Bad Trigger Phrases

❌ **Too vague:**
```yaml
description: "Does stuff with databases"
# Claude won't know when to use this
```

❌ **No triggers:**
```yaml
description: "A useful tool for development"
# Missing activation phrases
```

❌ **Too specific:**
```yaml
description: "Use exactly when user types: create ansible playbook for nginx"
# Too narrow, misses variations
```

## Size Matters

### Anthropic Examples
- **Size:** ~500 bytes
- **Content:** Minimal description and basic instructions
- **Purpose:** Demonstration

### Production Skills
- **Size:** 3,000-5,000 bytes
- **Content:** Comprehensive workflows, examples, error handling
- **Purpose:** Real-world usage

**Best Practice:** Include:
- Detailed multi-phase workflows
- Multiple examples
- Code templates
- Error handling patterns
- Progressive disclosure (basics → advanced)

## Skills vs Commands

### Commands (Explicit Invocation)
```bash
# User must know and type the command
/feature-plan "Add user authentication"
```
- Require explicit `/command` trigger
- User must remember command name
- Manual invocation
- Good for: Primary workflows

### Skills (Automatic Activation)
```
# Natural language, no command needed
"Plan out the user authentication feature"
```
- Claude detects intent from conversation
- No command to remember
- Automatic activation
- Good for: Supporting capabilities

### When to Use Each

**Use Commands for:**
- Main workflows (feature-plan, bug-fix, review)
- Entry points to orchestration
- Explicit user-triggered processes
- Primary product features

**Use Skills for:**
- Supporting capabilities (TDD, security-patterns)
- Domain expertise
- Auto-enhancement
- Background knowledge

**Best Practice:** Combine both!
- Commands orchestrate workflows
- Skills enhance with expertise
- Commands call skills automatically
- Skills provide domain knowledge

## One Skill Per Plugin?

**No!** Multiple skills per plugin are encouraged.

### Anthropic's Skills Powerkit Example
```
skills-powerkit/
  skills/
    plugin-creator/SKILL.md      ← Skill 1
    plugin-validator/SKILL.md    ← Skill 2
    marketplace-manager/SKILL.md ← Skill 3
    plugin-auditor/SKILL.md      ← Skill 4
    version-bumper/SKILL.md      ← Skill 5
```

Five related skills in one plugin!

### cc10x Example
```
cc10x/
  skills/
    test-driven-development/SKILL.md
    systematic-debugging/SKILL.md
    security-patterns/SKILL.md
    ui-design/SKILL.md
    code-generation/SKILL.md
    # ... 16 skills total
```

All related to 10x productivity workflows.

### Organizing Multiple Skills

**By Domain:**
```
testing-toolkit/
  skills/
    unit-testing/SKILL.md
    integration-testing/SKILL.md
    e2e-testing/SKILL.md
```

**By Workflow:**
```
feature-development/
  skills/
    planning/SKILL.md
    implementation/SKILL.md
    review/SKILL.md
```

**By Technology:**
```
javascript-expert/
  skills/
    react-patterns/SKILL.md
    node-best-practices/SKILL.md
    typescript-patterns/SKILL.md
```

## Agent Skills in Action

### Example: TDD Skill

```markdown
---
name: "Test-Driven Development"
description: |
  Enforces test-first development. Use when implementing features,
  fixing bugs, or adding functionality. Trigger with "implement",
  "add feature", "create function", "write code".
---

## What This Skill Does

Ensures test-driven development:
1. Write test first
2. Watch it fail (Red)
3. Make it pass (Green)
4. Refactor if needed
5. Repeat

## When It Activates

- User says "implement [feature]"
- Task involves writing code
- Adding new functionality
- Creating new components

## How It Works

**Phase 1: Test First**
- Write test for desired functionality
- Make test specific and clear
- Include edge cases

**Phase 2: Red**
- Run test
- Confirm it fails
- Understand why it fails

**Phase 3: Green**
- Write minimal code to pass
- No extra features
- Just make it work

**Phase 4: Refactor**
- Improve code quality
- Maintain passing tests
- Optimize if needed

**Phase 5: Commit**
- Commit with semantic message
- Include test in commit
- Document what was added

[... more detail ...]
```

When user says "implement user authentication":
1. Claude detects "implement" trigger
2. Reads TDD skill
3. Applies TDD workflow automatically
4. Writes test first, then code
5. No need to remind Claude about TDD!

## Auto-Invocation Mechanics

### How Claude Decides

1. **Frontmatter Scan (Fast)**
   - Reads YAML description from all skills
   - Builds trigger phrase index
   - Takes <100ms

2. **Context Matching**
   - User input analyzed
   - Matches against trigger phrases
   - Semantic similarity check

3. **Relevance Scoring**
   - Multiple skills might match
   - Scores by relevance
   - Selects best fit(s)

4. **Full Skill Load**
   - Reads complete SKILL.md
   - Applies instructions
   - Executes workflow

### Token Efficiency

**Without Skills:**
- Load all documentation upfront
- ~80k tokens for comprehensive docs
- Most content unused

**With Skills:**
- Load frontmatter only (~5k tokens)
- Load full skill when needed (~15k tokens)
- 70-90% token savings!

## Creating Effective Skills

### Step 1: Define Clear Purpose
```
What does this skill do?
When should it activate?
What problem does it solve?
```

### Step 2: Identify Trigger Phrases
```
List all ways users might request this
Consider variations
Include context clues
Think about natural language
```

### Step 3: Write Comprehensive Workflow
```
Break into phases
Step-by-step instructions
Decision points
Error handling
Best practices
```

### Step 4: Include Examples
```
Real-world scenarios
Input → Process → Output
Multiple use cases
Edge cases
```

### Step 5: Test and Iterate
```
Install and use
Try different phrasings
Check auto-activation
Refine trigger phrases
Improve instructions
```

## Common Patterns

### Pattern 1: Implementation Skill
```yaml
name: "Feature Implementation"
description: |
  Implements features following project patterns.
  Use when "implementing", "building", "creating" features.
```

### Pattern 2: Review Skill
```yaml
name: "Code Review"
description: |
  Reviews code for quality and security.
  Trigger with "review", "check", "audit" code.
```

### Pattern 3: Optimization Skill
```yaml
name: "Performance Optimization"
description: |
  Optimizes code performance.
  Use when "slow", "optimize", "improve performance".
```

### Pattern 4: Generation Skill
```yaml
name: "Documentation Generator"
description: |
  Generates documentation from code.
  Trigger with "document", "create docs", "generate README".
```

## Best Practices

✅ **Clear Trigger Phrases**
- Multiple variations
- Natural language
- Action-oriented

✅ **Comprehensive Workflows**
- Step-by-step
- Decision logic
- Error handling

✅ **Real Examples**
- Multiple scenarios
- Input/output shown
- Edge cases covered

✅ **Progressive Disclosure**
- Start simple
- Add complexity
- Expert-level details

✅ **Test Thoroughly**
- Try different phrases
- Verify auto-activation
- Check output quality

## Anti-Patterns

❌ **Vague Description**
```yaml
description: "Helps with development"
# Claude won't know when to use it
```

❌ **No Examples**
```markdown
## How It Works
Do the thing correctly.
# Too vague, no examples
```

❌ **Too Broad**
```yaml
name: "Everything Skill"
description: "Does all development tasks"
# One skill = one focused capability
```

❌ **Too Specific**
```yaml
description: "Only for React 18.2.0 apps using TypeScript 5.0.4"
# Too narrow, won't activate often enough
```

## Future of Skills

**Current (October 2025):**
- Auto-activation from description
- Markdown instructions
- Optional code execution

**Coming Soon:**
- Skill composition (skills calling skills)
- Skill marketplaces
- Skill analytics (activation stats)
- Version management
- Skill dependencies

## Resources

- **Official Docs:** https://www.anthropic.com/news/skills
- **Engineering Blog:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Anthropic Skills Repo:** https://github.com/anthropics/skills
- **Community Examples:** Search GitHub for "SKILL.md"

