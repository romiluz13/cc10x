# CC10X Prompt Surface Inventory

> **Status note:** Synced to `v10.1.20` on 2026-05-06. Structural contract last changed on 2026-04-12 (`v10.1.19`); `v10.1.20` is a state-root path migration (`.claude/cc10x/` → `.cc10x/`) with no prompt-surface changes.

## Purpose

This inventory defines which prompt surfaces are allowed to affect trust-critical behavior and what kind of edits are safe on each.

The router kernel and `cc10x-router/references/*.md` are intentionally excluded
from prompt-only tiers here. They are orchestration surfaces and must be
changed with replay + audit + Claude validation, not treated as ordinary prompt
copy.

## Tier 1: Trust-Critical Prompt Contracts

### planner
- Path: `plugins/cc10x/agents/planner.md`
- Role: agreement-first planning artifact creation
- Allowed edits: wording clarity, contract wording, output sections, codebase-reality checks, live-verification planning wording, examples, context-loading guidance
- Forbidden edits: anything that changes routing, approval semantics, plan-mode meaning, or build-start conditions
- Comparison references: `metaswarm` plan review, `get-shit-done` planning/execution contract, `cc10x-v7` planner usability
- Review requirement: audit + replay + manual semantic review

### planning-patterns
- Path: `plugins/cc10x/skills/planning-patterns/SKILL.md`
- Role: planner save discipline and router-subordinate memory intent guidance
- Allowed edits: wording clarity, plan-save examples, `MEMORY_NOTES` guidance, live-verification wording
- Forbidden edits: direct writes to `.cc10x/*.md`, altered plan-mode semantics, or bypassing router-owned memory finalization
- Comparison references: `get-shit-done` artifact-first planning, `skill-creator` reference-backed skill design
- Review requirement: audit + replay + manual semantic review

### brainstorming
- Path: `plugins/cc10x/skills/brainstorming/SKILL.md`
- Role: inline design clarification and planner handoff
- Allowed edits: clarification wording, design template structure, handoff wording, save examples
- Forbidden edits: direct writes to `.cc10x/*.md`, changing the brainstorming handoff schema, or bypassing planner handoff
- Comparison references: `metaswarm` clarification discipline, `get-shit-done` design-before-plan behavior
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
- Forbidden edits: allowing write agents to edit `.cc10x/*.md` directly, changing the memory namespace or required headings, or weakening router-owned final persistence
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
- Role: advisory frontend guardrails and spec-aligned project-local DESIGN.md authoring guidance
- Allowed edits: trigger accuracy, brevity, advisory clarifications, reference navigation, checklist extraction, DESIGN.md authoring guidance
- Forbidden edits: authority drift that competes with user/project standards or copying external brand/design references as project authority
- Comparison references: DESIGN.md format specification and `superpowers` writing-skills description hygiene
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

### prototyping
- Path: `plugins/cc10x/skills/prototyping/SKILL.md`
- Role: advisory throwaway-spike mode (answer ONE design question, then delete-or-absorb)
- Allowed edits: trigger accuracy, branch guidance, close-out/disposition wording
- Forbidden edits: weakening the hard wall (spike "no tests/no abstractions" must never leak into BUILD; absorb is a fresh gated BUILD, not promotion)
- Comparison references: `matt-pocock` prototype skill
- Review requirement: audit only unless the hard-wall or precedence wording changes

### finding-duplicate-functions
- Path: `plugins/cc10x/skills/finding-duplicate-functions/SKILL.md`
- Role: advisory semantic-duplicate audit for LLM-grown codebases (loaded by the reviewer or run standalone)
- Allowed edits: phase clarity, high-risk-zone table, model-tier wiring, common-mistakes
- Forbidden edits: language that authorizes deleting a duplicate without confirming the survivor has tests + callers updated + suite re-run
- Comparison references: `superpowers-lab` finding-duplicate-functions
- Review requirement: audit only unless authority wording changes

### mcp-cli
- Path: `plugins/cc10x/skills/mcp-cli/SKILL.md`
- Role: advisory on-demand MCP invocation (transient, not permanently mounted)
- Allowed edits: discovery/call/cleanup flow, install prereq, guard safety pattern
- Forbidden edits: language that turns a missing-capability/fallback message into a hard blocker
- Comparison references: `superpowers-lab` mcp-cli
- Review requirement: audit only unless authority wording changes

### receiving-code-review
- Path: `plugins/cc10x/skills/receiving-code-review/SKILL.md`
- Role: main-session discipline for verifying human/external review feedback before agreeing or implementing
- Allowed edits: the 6-step loop, forbidden-responses table, YAGNI-grep step, when-to-push-back
- Forbidden edits: language that restores performative agreement or that lets a suggestion be implemented without verification; weakening the user>standards>plan precedence
- Comparison references: `superpowers` receiving-code-review
- Review requirement: audit only unless authority/precedence wording changes

### codebase-deepening
- Path: `plugins/cc10x/skills/codebase-deepening/SKILL.md`
- Role: advisory retrofit/deepening analysis for shallow modules in existing code (read-only; proposes, does not edit)
- Allowed edits: deletion-test framing, diagnosis flow, candidate-badge presentation, two-adapters seam application
- Forbidden edits: language that turns it into an ungated rewrite path bypassing the BUILD chain
- Comparison references: `matt-pocock` improve-codebase-architecture, local `codebase-design` vocabulary
- Review requirement: audit only unless it stops routing refactors through BUILD

### frontend-design-critique
- Path: `plugins/cc10x/skills/frontend-design-critique/SKILL.md`
- Role: read-only design-quality critique (two isolated assessments + anchored rubric + AI-slop ban-list)
- Allowed edits: rubric criteria, ban-list maintenance, isolation/synthesis protocol, RTL notes
- Forbidden edits: making the optional deterministic detector a hard dependency; collapsing the two assessments into one head
- Comparison references: `matt-pocock` impeccable critique
- Review requirement: audit only unless it competes with frontend-patterns authority

### handoff-package
- Path: `plugins/cc10x/skills/handoff-package/SKILL.md`
- Role: portable cross-session/cross-tool handoff doc (repo-external, reference-by-path, secrets-redacted)
- Allowed edits: doc contents, location recipe, suggested-skills pointer
- Forbidden edits: writing the handoff into the repo, pasting artifact contents instead of referencing, or dropping the redaction rule
- Comparison references: `matt-pocock` handoff
- Review requirement: audit only unless the redaction/location rules change

## Review Classification

Every prompt change must be classified before merge:
- `metadata_only`
- `wording_only_low_risk`
- `wording_only_trust_sensitive`
- `orchestration_sensitive` → not eligible for prompt-only release
