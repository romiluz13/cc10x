# Harmony Rating System

## Rating Definitions

### NATIVE (Accept)
The pattern fits CC10x DNA so perfectly that a developer reading the file would not be able to tell where the original text ends and the new text begins. Same voice, same formatting, same severity model, same evidence requirements.

**NATIVE patterns must:**
- Use imperative voice with consequences
- Express rules as tables or numbered steps, not prose
- Include trigger + action + why for any new rule
- Target an existing file (no new files for prompt-text releases)
- Be purely additive (no existing text deleted or modified)
- Not touch YAML contracts, state machine transitions, or workflow graphs

### ACCEPTABLE (Drop)
The pattern could technically work in CC10x, but it would feel slightly foreign. Maybe the voice is slightly off, or it introduces a concept that CC10x doesn't have a native analog for, or it would require a structural change to feel right.

**Drop for perfect harmony.** The bar is high on purpose. Better to ship 5 NATIVE patterns than 20 ACCEPTABLE ones. Acceptable patterns accumulate into drift.

### RISKY (Reject)
The pattern conflicts with CC10x architecture, philosophy, or safety boundaries. Implementing it would either break something or create a competing control plane.

**Always reject. Explain the conflict clearly so it's not proposed again.**

---

## Real Examples from Past Releases

### v10.1.14 — Multi-Repo Patterns

**NATIVE example:** "Stale training data [EASY TO MISS] annotation"
- Why NATIVE: CC10x already uses [EASY TO MISS] annotations. This is the exact same pattern, applied to a new context (research orchestration). Same voice, same formatting.

**ACCEPTABLE example:** "Conversation threading across agents"
- Why dropped: CC10x agents are single-response. Threading requires conversational state that violates the structured scaffold principle.

**RISKY example:** "Agent self-loading of skills"
- Why rejected: CC10x router is the SOLE authority for skill loading. Agents self-loading creates a parallel control plane.

### v10.1.15 — Hook Expansion

**NATIVE example:** PreCompact hook (workflow state snapshot)
- Why NATIVE: Pure persistence. Writes to disk FOR the router. Never blocks. Never injects context. Follows existing Python thin-shim pattern via cc10x_hooklib.

**RISKY example (DROPPED after user challenge):** SubagentStart hook
- Why rejected: Would inject context into agent scaffolds at start time. This creates a SECOND context injection path that could drift from the router's scaffold. The router must be the ONLY source of agent context.

**RISKY example (DROPPED after user challenge):** TaskCreated hook
- Why rejected: Would validate task metadata at creation time. This second-guesses the router's own task creation. The router already owns task creation — a hook validating it creates a competing authority.

### v10.1.16 — BMAD-METHOD

**NATIVE example:** Zero-Finding Gate
- Why NATIVE: CC10x already has fail-closed gates. This extends the same pattern to catch a known failure mode (rubber-stamp approvals). Same severity model, same enforcement mechanism.

**ACCEPTABLE example:** Three-Layer Parallel Review
- Why dropped: CC10x ALREADY has a three-agent parallel review (reviewer + hunter + verifier). BMAD's version adds "Blind Hunter" (deliberately withholding context from agents), which violates CC10x's explicit handoff principle.

**RISKY example:** Multi-Agent Cross-Talk (Party Mode)
- Why rejected: CC10x agents are single-response. They never see each other's output mid-execution. The router mediates ALL inter-agent data flow. Cross-talk violates "agents receive ONLY structured prompt scaffold."

**RISKY example:** Merged Identity (Persona + Skill Role)
- Why rejected: Personality injection is explicitly foreign to CC10x DNA. CC10x agents have a "posture" (adversarial, auditor), not a "persona."

---

## The Challenge Test

When uncertain about a rating, apply this test:

**"Does this SUPPORT the router or COMPETE with it?"**

- SUPPORT = writes data to disk that the router can read later (persistence, telemetry, audit trails)
- COMPETE = injects context, validates router output, makes routing decisions, or creates a parallel control plane

If it competes, it's RISKY. No exceptions. This test caught SubagentStart and TaskCreated hooks that would have been accepted without it.

---

## Acceptance Rate Expectations

| Release Type | Raw Patterns | Expected Acceptance Rate |
|-------------|-------------|------------------------|
| Multi-repo analysis (many repos) | 300-500 | 5-10% |
| Single repo deep analysis | 30-50 | 15-25% |
| Hook/infrastructure expansion | 10-25 | 30-50% (but with stronger safety scrutiny) |

If your acceptance rate exceeds these ranges, revisit the NATIVE criteria. You may be rating ACCEPTABLE patterns as NATIVE.
