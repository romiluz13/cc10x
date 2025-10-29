---
name: code-generation
description: Provides lightweight guidance for writing clean, maintainable production code and points to the detailed code-generation playbook. Use when implementing new functionality or refactoring existing code so it stays consistent with project conventions.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Generation

## Quick Start
- Confirm requirements and tests (pair with `test-driven-development`).
- Read existing modules to mirror naming, layout, and error-handling patterns.
- Follow the checklist below, then consult the full [Code Generation Playbook](PLAYBOOK.md) for deeper patterns.

## Checklist
- Prefer clarity over cleverness; keep functions focused and small.
- Preserve separation of concerns (single responsibility, dependency inversion).
- Handle errors explicitly and surface actionable messages.
- Cover edge cases and input validation before returning success.
- Keep public APIs stable; document breaking changes for review.

## Workflow Integration
1. **Plan** - Align with architecture and design decisions before writing code.
2. **Implement** - Write the minimal code required for passing tests while applying the checklist.
3. **Review** - Cross-check with `code-quality-patterns` and `verification-before-completion` before marking complete.

## When to Consult the Playbook
- Unsure which pattern to apply (factory vs. strategy, state management, async flows).
- Need naming or style conventions for a language/framework.
- Looking for examples of error handling, logging, or dependency boundaries.

## References
- [Code Generation Playbook](PLAYBOOK.md)
- Related skills: `test-driven-development`, `code-quality-patterns`, `security-patterns`
