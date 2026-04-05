# CC10X Prompt Surface Inventory

## Purpose

This inventory defines which prompt surfaces are allowed to affect trust-critical behavior and what kind of edits are safe on each.

## Tier 1: Trust-Critical Prompt Contracts

### planner
- Path: `plugins/cc10x/agents/planner.md`
- Role: agreement-first planning artifact creation
- Allowed edits: wording clarity, contract wording, output sections, codebase-reality checks, live-verification planning wording, examples, context-loading guidance
- Forbidden edits: anything that changes routing, approval semantics, plan-mode meaning, or build-start conditions
- Comparison references: `metaswarm` plan review, `get-shit-done` planning/execution contract, `cc10x-v7` planner usability
- Review requirement: audit + replay + manual semantic review

### component-builder
- Path: `plugins/cc10x/agents/component-builder.md`
- Role: current approved phase execution
- Allowed edits: TDD wording, anti-scope-creep wording, evidence phrasing, context-curation wording
- Forbidden edits: new checkpoints, altered phase-order semantics, changed remediation ownership
- Comparison references: `get-shit-done` executor, `superpowers` execution discipline
- Review requirement: audit + replay + manual semantic review

### integration-verifier
- Path: `plugins/cc10x/agents/integration-verifier.md`
- Role: fail-closed independent end-to-end verification
- Allowed edits: evidence wording, auditor tone, truths/artifacts/wiring exposition, output clarity
- Forbidden edits: accepting upstream approval as proof, weakening fail-closed logic, changing remediation flow
- Comparison references: `get-shit-done` verifier, `superpowers` verification-before-completion
- Review requirement: audit + replay + manual semantic review

### plan-review-gate
- Path: `plugins/cc10x/skills/plan-review-gate/SKILL.md`
- Role: fail-closed plan review boundary
- Allowed edits: adversarial tone, wording clarity, evidence expectations
- Forbidden edits: implying non-blocking review, fake reviewer isolation, or advisory-only output
- Comparison references: `metaswarm` plan-review-gate and adversarial rubric
- Review requirement: audit + replay + manual semantic review

### verification-before-completion
- Path: `plugins/cc10x/skills/verification-before-completion/SKILL.md`
- Role: fresh-evidence honesty layer before completion claims
- Allowed edits: compactness, anti-rationalization wording, live-proof wording, example cleanup
- Forbidden edits: relaxing fresh-evidence requirement or reducing scope to only tests/build
- Comparison references: `superpowers` verification-before-completion, `get-shit-done` goal-backward verification
- Review requirement: audit + replay + manual semantic review

## Tier 2: Strong Supporting Contracts

### plan-gap-reviewer
- Path: `plugins/cc10x/agents/plan-gap-reviewer.md`
- Role: fresh, read-only challenge pass for saved plans
- Allowed edits: reviewer wording, finding categories, evidence language, anti-anchoring rules
- Forbidden edits: granting write authority, workflow ownership, or user-question authority
- Comparison references: `metaswarm` adversarial planning, Claude Code subagent best practices
- Review requirement: audit + targeted semantic review

### bug-investigator
- Path: `plugins/cc10x/agents/bug-investigator.md`
- Role: evidence-first debugging with variant and blast-radius coverage
- Allowed edits: hypothesis wording, anti-hardcode wording, anti-loop wording, context-curation wording
- Forbidden edits: changing research escalation policy or fix/report ownership
- Comparison references: `get-shit-done` debugger, `superpowers` systematic-debugging
- Review requirement: audit + targeted semantic review

### session-memory
- Path: `plugins/cc10x/skills/session-memory/SKILL.md`
- Role: versioned memory load discipline, distillation rules, and router-subordinate memory-note protocol
- Allowed edits: compactness, reference navigation, distillation wording, context-budget guidance, and examples that preserve current ownership
- Forbidden edits: allowing write agents to edit `.claude/cc10x/v10/*.md` directly, changing the memory namespace or required headings, or weakening router-owned final persistence
- Comparison references: `get-shit-done` context-budget, `agent-skills` context-engineering, `skill-creator` reference-first packaging
- Review requirement: audit + targeted semantic review

### code-reviewer
- Path: `plugins/cc10x/agents/code-reviewer.md`
- Role: adversarial code review with remediation intent
- Allowed edits: rubric clarity, evidence language, confidence wording
- Forbidden edits: self-healing ownership changes or authority drift against router
- Comparison references: `superpowers` review skills, `metaswarm` auditor tone
- Review requirement: audit + targeted semantic review

### silent-failure-hunter
- Path: `plugins/cc10x/agents/silent-failure-hunter.md`
- Role: scan for silent-failure patterns and report truthful coverage
- Allowed edits: scan-language clarity, severity wording, output clarity
- Forbidden edits: self-healing behavior or weakening coverage-truth requirements
- Comparison references: internal benchmark notes, error-handling competitors where applicable
- Review requirement: audit + targeted semantic review

## Tier 3: Advisory Skill Metadata

### frontend-patterns
- Path: `plugins/cc10x/skills/frontend-patterns/SKILL.md`
- Role: advisory frontend guardrails
- Allowed edits: trigger accuracy, brevity, advisory clarifications, reference navigation, checklist extraction
- Forbidden edits: authority drift that competes with user/project standards
- Comparison references: `superpowers` writing-skills description hygiene
- Review requirement: audit only unless authority wording changes

### debugging-patterns
- Path: `plugins/cc10x/skills/debugging-patterns/SKILL.md`
- Role: advisory root-cause debugging reference
- Allowed edits: trigger accuracy, brevity, root-cause emphasis, reference navigation, playbook extraction
- Forbidden edits: language that authorizes shallow/local-only fixes
- Comparison references: `superpowers` writing-skills description hygiene
- Review requirement: audit only unless authority wording changes

### code-review-patterns
- Path: `plugins/cc10x/skills/code-review-patterns/SKILL.md`
- Role: advisory review-order, security, and quality heuristics
- Allowed edits: compactness, rubric clarity, reference navigation, checklist extraction
- Forbidden edits: authority drift that bypasses router-owned review agents
- Comparison references: `get-shit-done` review references, `superpowers` review skills
- Review requirement: audit only unless authority wording changes

### test-driven-development
- Path: `plugins/cc10x/skills/test-driven-development/SKILL.md`
- Role: advisory TDD discipline and verification-depth escalation
- Allowed edits: compactness, examples, reference navigation, live-proof escalation wording
- Forbidden edits: relaxing fail-first discipline or weakening delete-and-restart guidance
- Comparison references: `superpowers` test-driven-development, `agent-skills` testing references
- Review requirement: audit only unless authority wording changes

### architecture-patterns
- Path: `plugins/cc10x/skills/architecture-patterns/SKILL.md`
- Role: advisory architecture lens
- Allowed edits: trigger accuracy, advisory framing
- Forbidden edits: language that sounds like router-owned policy
- Comparison references: internal benchmark notes
- Review requirement: audit only unless authority wording changes

## Review Classification

Every prompt change must be classified before merge:
- `metadata_only`
- `wording_only_low_risk`
- `wording_only_trust_sensitive`
- `orchestration_sensitive` → not eligible for prompt-only release
