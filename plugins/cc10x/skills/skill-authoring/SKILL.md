---
name: skill-authoring
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment - applies TDD to process documentation by anticipating failure patterns (RED), writing skill addressing those patterns (GREEN), then closing loopholes through application (REFACTOR)
---

# Skill Authoring

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

**cc10x skills live in `plugins/cc10x/skills/` directory**

You identify common failure patterns (baseline behavior), write the skill (documentation) addressing those patterns, then verify through application scenarios, and refactor (close loopholes).

**Core principle:** If you didn't identify what agents naturally do wrong, you don't know if the skill prevents the right failures.

**REQUIRED BACKGROUND:** You MUST understand test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept             | Skill Creation                                   |
| ----------------------- | ------------------------------------------------ |
| **Test case**           | Anticipated failure pattern from experience      |
| **Production code**     | Skill document (SKILL.md)                        |
| **Test fails (RED)**    | Identify common mistakes without skill           |
| **Test passes (GREEN)** | Skill addresses those specific mistakes          |
| **Refactor**            | Close loopholes while maintaining clarity        |
| **Write test first**    | Identify failure patterns BEFORE writing skill   |
| **Watch it fail**       | Document exact rationalizations from experience  |
| **Minimal code**        | Write skill addressing those specific violations |
| **Watch it pass**       | Verify skill clarity through application         |
| **Refactor cycle**      | Find new rationalizations → plug → re-verify     |

The entire skill creation process follows RED-GREEN-REFACTOR.

## When to Create a Skill

**Create when:**

- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**

- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)

## Skill Types

### Technique

Concrete method with steps to follow (condition-based-waiting, root-cause-tracing)

### Pattern

Way of thinking about problems (flatten-with-flags, test-invariants)

### Reference

API docs, syntax guides, tool documentation

## Directory Structure

```
plugins/cc10x/skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

**Flat namespace** - all skills in one searchable namespace

**Separate files for:**

1. **Heavy reference** (100+ lines) - API docs, comprehensive syntax
2. **Reusable tools** - Scripts, utilities, templates

**Keep inline:**

- Principles and concepts
- Code patterns (< 50 lines)
- Everything else

## SKILL.md Structure

**Frontmatter (YAML):**

- Only two fields supported: `name` and `description`
- Max 1024 characters total
- `name`: Use letters, numbers, and hyphens only (no parentheses, special chars)
- `description`: Third-person, includes BOTH what it does AND when to use it
  - Start with "Use when..." to focus on triggering conditions
  - Include specific symptoms, situations, and contexts
  - Keep under 500 characters if possible

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms] - [what the skill does and how it helps, written in third person]
---

# Skill Name

## Overview

What is this? Core principle in 1-2 sentences.

## When to Use

Bullet list with SYMPTOMS and use cases
When NOT to use

## Core Pattern (for techniques/patterns)

Before/after code comparison

## Quick Reference

Table or bullets for scanning common operations

## Implementation

Inline code for simple patterns
Link to file for heavy reference or reusable tools

## Common Mistakes

What goes wrong + fixes
```

## Claude Search Optimization (CSO)

**Critical for discovery:** Future Claude needs to FIND your skill

### 1. Rich Description Field

**Purpose:** Claude reads description to decide which skills to load for a given task. Make it answer: "Should I read this skill right now?"

**Format:** Start with "Use when..." to focus on triggering conditions, then explain what it does

**Content:**

- Use concrete triggers, symptoms, and situations that signal this skill applies
- Describe the _problem_ (race conditions, inconsistent behavior) not _language-specific symptoms_ (setTimeout, sleep)
- Keep triggers technology-agnostic unless the skill itself is technology-specific
- If skill is technology-specific, make that explicit in the trigger
- Write in third person (injected into system prompt)

```yaml
# ❌ BAD: Too abstract, vague, doesn't include when to use
description: For async testing

# ❌ BAD: First person
description: I can help you with async tests when they're flaky

# ✅ GOOD: Starts with "Use when", describes problem, then what it does
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently - replaces arbitrary timeouts with condition polling for reliable async tests
```

### 2. Keyword Coverage

Use words Claude would search for:

- Error messages: "Hook timed out", "ENOTEMPTY", "race condition"
- Symptoms: "flaky", "hanging", "zombie", "pollution"
- Synonyms: "timeout/hang/freeze", "cleanup/teardown/afterEach"
- Tools: Actual commands, library names, file types

### 3. Descriptive Naming

**Use active voice, verb-first:**

- ✅ `creating-skills` not `skill-creation`
- ✅ `writing-skills` not `skill-writing`

### 4. Token Efficiency (Critical)

**Problem:** Frequently-referenced skills load into EVERY conversation. Every token counts.

**Target word counts:**

- Frequently-loaded skills: <200 words total
- Other skills: <500 words (still be concise)

**Techniques:**

**Move details to tool help:**

```bash
# ❌ BAD: Document all flags in SKILL.md
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N

# ✅ GOOD: Reference --help
search-conversations supports multiple modes and filters. Run --help for details.
```

**Use cross-references:**

```markdown
# ❌ BAD: Repeat workflow details

When implementing feature, follow these 20 steps...
[20 lines of repeated instructions from another skill]

# ✅ GOOD: Reference other skill

For implementation workflow, REQUIRED: Use [other-skill-name] for complete process.
```

**Eliminate redundancy:**

- Don't repeat what's in cross-referenced skills
- Don't explain what's obvious from command
- Don't include multiple examples of same pattern

**Name by what you DO or core insight:**

- ✅ `condition-based-waiting` > `async-test-helpers`
- ✅ `using-skills` not `skill-usage`
- ✅ `root-cause-tracing` > `debugging-techniques`

**Gerunds (-ing) work well for processes:**

- `creating-skills`, `testing-skills`, `debugging-with-logs`
- Active, describes the action you're taking

## The Iron Law (Same as TDD)

```
NO SKILL WITHOUT IDENTIFYING FAILURE PATTERNS FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before identifying what it prevents? Delete it. Start over.
Edit skill without identifying new failure patterns? Same violation.

**No exceptions:**

- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Don't keep unverified changes as "reference"
- Don't "adapt" while applying
- Delete means delete

**REQUIRED BACKGROUND:** The test-driven-development skill explains why this matters. Same principles apply to documentation.

## Integration with cc10x Orchestrator

**Orchestrator-Driven Skill Loading:**

- Skills are loaded by workflows based on detection logic
- Skills can be required (always loaded) or conditional (loaded based on detection)
- Skills load in parallel when independent
- Skills load sequentially when dependencies exist

**Skill Discovery:**

- Use `skill-discovery` skill to find relevant skills before workflow selection
- Orchestrator will then load workflow-specific skills automatically
- Your skill discovery ensures no skills are missed

## Common Rationalizations for Skipping Verification

| Excuse                          | Reality                                                                 |
| ------------------------------- | ----------------------------------------------------------------------- |
| "Skill is obviously clear"      | Clear to you ≠ clear to other agents. Verify it.                        |
| "It's just a reference"         | References can have gaps, unclear sections. Verify information access.  |
| "Verification is overkill"      | Unverified skills have issues. Always. 15 min verification saves hours. |
| "I'll verify if problems arise" | Problems = agents can't use skill. Verify BEFORE deploying.             |
| "Too tedious to verify"         | Verification is less tedious than debugging bad skill in production.    |
| "I'm confident it's good"       | Overconfidence guarantees issues. Verify anyway.                        |
| "Academic review is enough"     | Reading ≠ using. Verify through application.                            |
| "No time to verify"             | Deploying unverified skill wastes more time fixing it later.            |

**All of these mean: Verify before deploying. No exceptions.**

## Summary

**Starting any skill creation:**

1. Identify failure patterns FIRST (RED)
2. Write skill addressing those patterns (GREEN)
3. Verify through application (REFACTOR)
4. Close loopholes found during verification

**Skill has checklist?** TodoWrite for every item.

**Finding a relevant skill = mandatory to read and use it. Not optional.**
