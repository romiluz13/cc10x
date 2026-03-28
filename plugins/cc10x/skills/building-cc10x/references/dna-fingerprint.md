# CC10x DNA Fingerprint Template

Use this template to generate a fresh DNA fingerprint before every harmony integration. The fingerprint is the standard against which all extracted patterns are judged.

## How to Generate

Read these CC10x files and produce a fingerprint covering all 11 dimensions below:
- `plugins/cc10x/skills/cc10x-router/SKILL.md` (read in chunks — >1100 lines)
- 3-4 agent files (component-builder, integration-verifier, code-reviewer, bug-investigator)
- 3-4 skill files (planning-patterns, code-generation, test-driven-development, code-review-patterns)
- `plugins/cc10x/hooks/hooks.json` and `plugins/cc10x/config/hook-mode.json`

## The 11 Dimensions

### 1. Voice & Tone
Capture: Is it imperative? Declarative? Conversational? What severity words are used? How are commands phrased?

### 2. Formatting Patterns
Capture: Tables vs bullets vs prose? Header hierarchy? Code blocks? Separators? YAML vs JSON?

### 3. How Rules Are Expressed
Capture: Severity tiers? Consequences stated? Trigger-action-why structure? [EASY TO MISS] annotations?

### 4. Structural Patterns
Capture: Section organization? Numbered steps vs bullets? Decision trees? Contract envelopes?

### 5. Safety/Guard Patterns
Capture: Gate types? Circuit breakers? Proof reconciliation? What triggers a halt?

### 6. Context Management
Capture: How state flows between agents? Memory architecture? Task metadata? What agents receive?

### 7. Quality Gates
Capture: Verification levels? Evidence requirements? What counts as proof?

### 8. Professional Objectivity
Capture: Tone when results contradict? Forbidden language? Evidence vs assertion?

### 9. Emergency Patterns
Capture: What happens when stuck? When conflicted? When verification fails?

### 10. Rhythm & Cadence
Capture: Single-response rule? Parallel execution rules? Remediation loop rhythm?

### 11. NATIVE vs PATCHED ON
Capture: What BELONGS in CC10x? What signals external origin? This is the most important dimension — it defines the harmony filter.

## Current Fingerprint Summary (as of v10.1.16)

**Voice:** Imperative with extreme precision. MUST/NEVER/MANDATORY/CRITICAL. No passive suggestions. Professional and unflinching.

**Formatting:** Pipe tables dominate. YAML contracts as machine-readable output. Numbered steps. Code blocks as binding specs. `---` separators.

**Rules:** Three-tier: Hard Rules (CRITICAL/MANDATORY with consequences), Gates (conditional blocking with `GATE:` prefix), Heuristics ([EASY TO MISS] warnings). Each rule has trigger + action + why.

**Safety:** Fail-closed gates (plan_trust_gate, phase_exit_gate, failure_stop_gate, memory_sync_gate). Circuit breakers (3 remediation loops max). Proof reconciliation triple (truths + artifacts + wiring).

**Context:** Explicit handoff via structured scaffold. Memory files are source of truth. Workflow artifact (.json) is durable identity. Task metadata is scoped recovery. Agents receive ONLY structured prompt scaffold.

**Quality:** Three verification levels. TDD cycle proof (RED exit 1, GREEN exit 0). Professional objectivity — sentiment does not override evidence.

**NATIVE signals:** Deterministic metadata contracts, memory architecture with stable anchors, workflow artifact as durable state, tables for rule matrices, [EASY TO MISS] warnings, YAML Router Contracts, phase cursor model, proof reconciliation triple.

**PATCHED ON signals:** Skill loading outside SKILL_HINTS, agents creating tasks directly, unscoped task lookups, prose-only verdicts, personality/persona injection, emoji, conversational tone, step-file micro-architecture, progressive disclosure, halt-before-menu within agents, multi-agent cross-talk.
