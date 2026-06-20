---
name: brainstorming
description: "Internal cc10x skill, loaded by the planner in the PLAN workflow. Use when exploring intent, requirements, and design options before a plan is written, emitting a machine-readable design handoff."
allowed-tools: Read Grep Glob AskUserQuestion Write Edit Bash
user-invocable: false
---

# Brainstorming Ideas Into Designs

> **DIVERGENCE FROM superpowers:brainstorming:** Lightly forked. The one-question-at-a-time / present-alternatives / validate-incrementally discipline is shared. CC10x ADDS: the Spec File Workflow, the AskUserQuestion interview machinery, the full design-document template, the router-owned machine-readable handoff that carries the design forward into the PLAN workflow, a front-of-flow scope-triage gate that decomposes multi-subsystem requests and brainstorms only the first sub-project, a Design Self-Review gate that scans the produced design for placeholders, contradictions, and ambiguity before the handoff, an accreting domain glossary plus inline ADR-on-rejection notes (durable vocabulary + rejected-alternative decisions, emitted via the router-owned handoff to feed ORIENT and the planner downstream), and a gated synthesize-now fast path that drafts the design from existing context when goal + constraints + acceptance are already evident, skipping the full interview.

## Overview

Help turn rough ideas into fully formed designs through collaborative dialogue. Don't jump to solutions - explore the problem space first.

**Core principle:** Understand what to build BEFORE designing how to build it.
Use the user's language for domain concepts; do not invent new terminology when the repo or prompt already has a stable name for the thing.

**Violating the letter of this process is violating the spirit of brainstorming.**

## The Iron Law

```
NO DESIGN WITHOUT UNDERSTANDING PURPOSE AND CONSTRAINTS
```

If you can't articulate why the user needs this and what success looks like, you're not ready to design.

## When to Use

**ALWAYS before:**
- Creating new features
- Building new components
- Adding new functionality
- Modifying existing behavior
- Making architectural decisions

**Signs you need to brainstorm:**
- Requirements feel vague
- Multiple approaches seem valid
- Success criteria unclear
- User intent ambiguous

## Spec File Workflow (Optional)

If user references a spec file (SPEC.md, spec.md, plan.md):

1. **Read existing spec** - Use as interview foundation
2. **Interview to expand** - Fill gaps using Phase 2 questions
3. **Write back** - Save expanded design to same file

```
# Check for existing spec (permission-free)
Read(file_path="SPEC.md")  # or spec.md if that doesn't exist
```

## The Process

### Phase 1: Understand Context

**Before asking questions:**

1. Check project state (files, docs, recent commits)
2. Understand what exists
3. Identify relevant patterns

```
# Check recent context (permission-free) — skip if commands fail (new/empty project)
Bash(command="git log --oneline -10 2>/dev/null || echo 'No git history'")
Bash(command="ls src/ 2>/dev/null || ls . 2>/dev/null || echo 'Empty project'")
```
**If project is empty/new:** Skip project scan, start from user's description.

### Phase 1.5: Scope Triage (Decomposition Gate — Front of Flow)

**Before opening the interview, decide whether this is ONE design or MANY.** Brainstorming produces a single coherent design that anchors a single plan. A request that spans multiple independent subsystems will produce a sprawling, unfocused design and a planner that can't sequence it.

**Trigger:** The request describes 2+ pieces that could be built, tested, and shipped on their own — different surfaces (e.g. a backend API + a CLI + a dashboard), different data stores, different deploy targets, or pieces joined only by "and."

**If the request is a single subsystem:** Skip this gate, go straight to Phase 2.

**If the request is multi-subsystem:** Do NOT try to brainstorm all of it at once. Emit a decomposition recommendation, then brainstorm only the FIRST sub-project:

```markdown
## Scope Triage: Decomposition Recommended

This request spans multiple independent subsystems. Brainstorming all of them in one design would be unfocused. Recommended decomposition:

### Independent pieces
1. **[Sub-project A]** — [one line: what it is, why it stands alone]
2. **[Sub-project B]** — [one line]
3. **[Sub-project C]** — [one line]

### Relationships
- [A → B: how they connect, what A produces that B consumes, or "independent"]
- [shared contracts / interfaces between pieces]

### Recommended build order
1. [first — usually the piece others depend on, or the riskiest/most foundational]
2. [second]
3. [third]

**Proceeding with sub-project #1 ([name]) now.** The remaining pieces are captured above; the router carries them forward so each gets its own brainstorm → design when its turn comes.
```

After emitting the recommendation, run the normal flow (Phase 2 onward) for the FIRST sub-project ONLY. Do not interview across all pieces at once — each sub-project earns its own pass.

### Phase 1.6: Synthesize-Now Fast Path (Gated — Skip the Interview When Intent Is Already Complete)

**Before opening the interview, check whether the conversation already contains enough to draft the design.** brainstorming defaults to interviewing — but when the user has already told you everything an interview would extract, re-asking it as multiple-choice is noise. In that case, synthesize the design from existing context and present it for confirmation instead of running Phase 2.

**Gate — take the fast path ONLY when all three are already evident from the prompt, repo context, or prior conversation:**
1. **Goal** — what to build and the problem it solves is stated, not inferred.
2. **Constraints** — limitations, requirements, and what's out of scope are stated or clearly bounded.
3. **Acceptance** — how we'll know it works (success criteria) is stated or unambiguous.

If ANY of the three is missing or fuzzy, do NOT synthesize — run the normal interview (Phase 2 onward). When in doubt, interview. This is the conservative default; the fast path is the exception for when re-interviewing would only repeat what the user already said.

**If the gate passes:**

1. Skip Phase 2's AskUserQuestion sequence. Draft the design directly from the existing context using the Output: Design Document template.
2. Still run Phase 3 (Explore Approaches) lightly — present the chosen approach and the rejected alternatives so the ADR-on-rejection note still gets captured. Synthesizing does not skip recording why the design is what it is.
3. Present the synthesized design for confirmation in ONE pass, not section-by-section:

```markdown
## Synthesized Design (from existing context — confirm or correct)

I have enough from our conversation to draft this directly rather than interview. Here is the design as I understand it:

[full design from the Output: Design Document template]

**Confirm this is right, or tell me what to change.** If anything is wrong or missing, I'll fall back to a targeted question instead of re-running the full interview.
```

4. On confirmation, run the Design Self-Review Gate and proceed to the handoff as normal. On correction, fix the named gap inline (one targeted question if needed) — do not restart the full interview.

Everything downstream (glossary accretion, ADR notes, self-review, handoff) is identical whether the design came from the interview or the fast path.

### Phase 2: Explore the Idea (One Question at a Time)

**MANDATORY: Cover all 5 dimensions below, but only call AskUserQuestion for dimensions that are still unresolved after reading the user prompt, repo context, and any existing design/spec. Stop as soon as the intent contract is complete.**

Skip a question when the answer is already explicit and high-confidence. In that case:
- write the inferred answer into your working notes
- mention the assumption in the final design summary
- continue to the next unresolved dimension

If only 1-2 dimensions remain unclear, ask only those 1-2 questions. Do not force a 5-question interview when the request is already concrete.

**Q1 — Call AskUserQuestion NOW:**
```
AskUserQuestion({
  questions: [{
    question: "What problem does this solve for users?",
    header: "Purpose",
    multiSelect: false,
    options: [
      { label: "New feature", description: "Adding new functionality" },
      { label: "Bug fix", description: "Fixing broken behavior" },
      { label: "Refactor", description: "Improving existing code structure" },
      { label: "Something else", description: "I'll describe it" }
    ]
  }]
})
```

**Q2 — Call AskUserQuestion NOW (after Q1 answered):**
```
AskUserQuestion({
  questions: [{
    question: "Who will use this?",
    header: "Users",
    multiSelect: false,
    options: [
      { label: "Developers", description: "Engineering team or API consumers" },
      { label: "End users", description: "People using the product UI" },
      { label: "Admins", description: "Administrative or ops users" },
      { label: "Internal team", description: "Internal tooling only" }
    ]
  }]
})
```

**Q3 — Call AskUserQuestion NOW (after Q2 answered):**
```
AskUserQuestion({
  questions: [{
    question: "How will we know this works well?",
    header: "Success",
    multiSelect: false,
    options: [
      { label: "Tests pass", description: "Automated tests verify behavior" },
      { label: "Performance target met", description: "Specific speed or throughput goal" },
      { label: "User completes task", description: "End-to-end user flow works" },
      { label: "Describe it", description: "I'll type my own success criteria" }
    ]
  }]
})
```

**Q4 — Call AskUserQuestion NOW (after Q3 answered):**
```
AskUserQuestion({
  questions: [{
    question: "What limitations or requirements exist?",
    header: "Constraints",
    multiSelect: true,
    options: [
      { label: "No constraints", description: "No special requirements" },
      { label: "Performance", description: "Speed, memory, or throughput targets" },
      { label: "Security", description: "Auth, permissions, or data protection" },
      { label: "Time / deadline", description: "Must ship by a specific date" }
    ]
  }]
})
```

**Q5 — Call AskUserQuestion NOW (after Q4 answered):**
```
AskUserQuestion({
  questions: [{
    question: "What's the scope of this change?",
    header: "Scope",
    multiSelect: false,
    options: [
      { label: "Single module", description: "One focused area of the codebase (Recommended)" },
      { label: "Single file", description: "Isolated to one file" },
      { label: "Full feature", description: "Multiple files, end-to-end" },
      { label: "Cross-cutting", description: "Touches many parts of the system" }
    ]
  }]
})
```

**Optional Q6 (ask only when the user seems to have unexpressed aspirations):** "If there were no constraints, what would the ideal version look like?" This unlocks hidden requirements and aspirational features — capture them, then apply YAGNI to defer what is not essential.

**Q7 — Out-of-scope discovery (always ask):** "What is explicitly NOT part of this? What should we defer?" Document answers in the Out of Scope section of the design document. This prevents scope creep from assumptions about what "should" be included.

**After the unresolved dimensions are answered:** Verify the collected intent passes the Intent Completeness Gate before proceeding:
1. **Small enough** — intent fits in one paragraph without losing specifics.
2. **Contradiction-free** — no answer conflicts with another answer or a stated constraint.
3. **Sufficiently specific** — a builder agent could act on it without asking clarifying questions.

If ANY check fails, ask one more targeted question to resolve the gap. Do NOT proceed with ambiguous or contradictory intent. Once all three checks pass, proceed to Phase 3 with collected answers. Do not force the full 7-question sequence when the intent contract is already complete.

**Accrete the domain glossary as you go.** Whenever the interview names or sharpens a domain term — the user gives a concept a stable name, you pin down a fuzzy word to one precise meaning, or the repo/prompt already has a load-bearing name for a thing — record it as a glossary entry in your working notes. This is *vocabulary*, not conventions: the nouns and verbs this project uses for its domain, each with the meaning agreed during the interview. Keep using the user's word; do not invent a synonym once a term is named. The glossary accumulates across the interview and is emitted in the handoff so ORIENT and the planner speak the project's language downstream.

```markdown
## Domain Glossary
- **[Term]** — [precise meaning agreed during brainstorming; note if it sharpens or replaces a vaguer earlier word]
- **[Term]** — [meaning]
```

### Phase 3: Explore Approaches

**Always present 2-3 options with trade-offs:**

```markdown
## Approaches

### Option A: [Name] (Recommended)
**Approach**: [Brief description]
**Pros**: [Benefits]
**Cons**: [Drawbacks]
**Why recommended**: [Reasoning]

### Option B: [Name]
**Approach**: [Brief description]
**Pros**: [Benefits]
**Cons**: [Drawbacks]

### Option C: [Name]
**Approach**: [Brief description]
**Pros**: [Benefits]
**Cons**: [Drawbacks]

Which direction feels right?
```

**Capture an ADR-on-rejection note for load-bearing decisions.** When the chosen direction *rejects* an alternative that mattered — a real fork where the road not taken was plausible — record it as an inline ADR-style note so the rejection is durable, not lost the moment the conversation moves on. A future builder (or you, downstream) should not have to re-litigate a settled choice. Record only load-bearing rejections; do not log every trivial preference.

```markdown
## Decisions (ADR notes)
- **Decision**: [what was chosen]
  **Rejected**: [the alternative(s) not taken]
  **Why**: [the reason the rejected option lost — the constraint or trade-off that decided it]
```

These ADR notes live in the design document and are emitted in the handoff alongside the glossary, so the planner inherits *why* the design is shaped this way, not just what it is.

### Phase 4: Present Design Incrementally

**Once approach chosen, present design in sections (200-300 words each):**

1. **Architecture Overview** - High-level structure (establishes shared mental model before details)
   > "Does this architecture make sense so far?"

2. **Components** - Key pieces (names the parts referenced in all later discussion)
   > "Do these components cover what you need?"

3. **Data Flow** - How data moves (validates components actually connect — catches orphaned pieces)
   > "Does this data flow work for your use case?"

4. **Error Handling** - What can go wrong (only meaningful after happy path is agreed)
   > "Are these error cases covered?"

5. **Testing Strategy** - How to verify (depends on all prior sections being stable)
   > "Does this testing approach give you confidence?"

**After each section, ask if it looks right before continuing.**

## Key Principles

### One Question at a Time
```
✅ "What problem does this solve?"
   [Wait for answer]
   "Who will use it?"
   [Wait for answer]

❌ "What problem does this solve, who will use it,
    what are the constraints, and what's the success criteria?"
```

### Multiple Choice Preferred
```
✅ "Which approach fits better?
    A. Simple file-based storage
    B. Database with caching
    C. External service integration"

❌ "How do you want to handle storage?"
```

### YAGNI Ruthlessly
```
✅ "You mentioned analytics - is that needed for v1
    or can we defer it?"

❌ Adding analytics, caching, and multi-tenancy
   because "we might need them later"
```

### Explore Alternatives
```
✅ Presenting 3 approaches with trade-offs
   before asking which to pursue

❌ Jumping straight to your preferred solution
```

### Incremental Validation
```
✅ "Here's the data model [200 words].
    Does this match your mental model?"

❌ Presenting the entire design in one 2000-word block
```

## Red Flags & Rationalizations

The generic brainstorming red flags (designing without knowing the purpose, jumping to implementation, presenting one approach, asking compound/leading questions, accepting vague answers) and the excuse/reality table are core discipline — assumed, not repeated here (see superpowers:brainstorming). If you catch any of them: STOP and go back to Phase 2. cc10x adds the one-question-at-a-time interview machinery, the design-doc template, and the router-owned handoff below.

## Output: Design Document

After brainstorming, save the validated design:

```markdown
# [Feature Name] Design

## Purpose
[What problem this solves]

## Users
[Who will use this]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Out of Scope
- [Explicitly excluded 1]
- [Explicitly excluded 2]

## Approach Chosen
[Which option and why]

## Domain Glossary
- **[Term]** — [precise meaning agreed during brainstorming]
[Omit this section only if no domain terms were named or sharpened.]

## Decisions (ADR notes)
- **Decision**: [what was chosen]
  **Rejected**: [alternative not taken]
  **Why**: [the constraint or trade-off that decided it]
[Omit this section only if no load-bearing alternative was rejected.]

## Architecture
[High-level structure]

## Components
[Key pieces]

## Data Flow
[How data moves]

## Error Handling
[What can go wrong and how handled]

## Testing Strategy
[How to verify]

## Observability (if applicable)
- Logging: [what to log]
- Metrics: [what to track]
- Alerts: [when to alert]

## UI Mockup (if applicable)
[ASCII mockup for UI features]

## Questions Resolved
- Q: [Question asked]
  A: [Answer given]
```

## UI Mockup (For UI Features Only)

For UI features, include ASCII mockup in the design:

```
┌─────────────────────────────────────────┐
│  [Component Name]                       │
├─────────────────────────────────────────┤
│  [Header/Navigation]                    │
├─────────────────────────────────────────┤
│                                         │
│  [Main content area]                    │
│                                         │
│  [Input fields, buttons, etc.]          │
│                                         │
├─────────────────────────────────────────┤
│  [Footer/Actions]                       │
└─────────────────────────────────────────┘
```

**Skip this for API-only or backend features.**

## Design Self-Review Gate (MANDATORY — before the handoff)

The Intent Completeness Gate (Phase 2) checks the inputs. This gate checks the OUTPUT: the design you just wrote is about to anchor the planner, so scan it once for the failures that quietly corrupt downstream plans. Read the design file top to bottom against these four checks and **fix inline** — there is no second review pass.

1. **No placeholders / TBD.** Scan for `TODO`, `TBD`, `[bracketed placeholder]`, `???`, or "decide later." Every section the template asked for must hold a real decision, not a stub. If a section truly does not apply, say so explicitly ("N/A — no UI") rather than leaving it blank or templated.
2. **Internally consistent.** No section contradicts another: the components named in Architecture all appear in Data Flow; Error Handling covers the failure modes the chosen Approach introduces; Success Criteria don't conflict with the stated Constraints or Out of Scope. Resolve any conflict in favor of the user's stated intent.
3. **Single-plan scope.** The design must describe ONE coherent thing a single plan can sequence. If — despite the front-of-flow triage — the design grew to span multiple independent subsystems, decompose it: narrow this design to the first sub-project and record the rest in Out of Scope (so the router carries them forward). One design → one plan.
4. **No two-way-ambiguous requirements.** Any requirement that could be read two valid ways is a planner trap. Pick ONE interpretation and state it explicitly in the design (e.g. "retries: exactly 3, then dead-letter" not "retries as needed"). Do not pass ambiguity downstream.

Apply every fix directly to the saved design file (Edit/Write — permission-free). This is a self-review: no agents spawned, no re-review loop. Once the four checks pass, proceed to the handoff.

## Saving the Design (MANDATORY)

**One direct save and one router handoff are required - design file plus machine-readable handoff.**

### Step 1: Save Design File (Use Write tool - NO PERMISSION NEEDED)

```
# Resolve absolute project directory FIRST (prevents wrong-CWD save — CC10X-006)
Bash(command="pwd")  # Store output as PROJECT_DIR
# Example: if pwd = /workspace/github-horoscope, use that as prefix

# Create directory using absolute path
Bash(command="mkdir -p {PROJECT_DIR}/docs/plans")

# Then save design using Write tool (permission-free)
# IMPORTANT: Use absolute path. Relative paths save to workspace root, not project dir.
Write(file_path="{PROJECT_DIR}/docs/plans/YYYY-MM-DD-<feature>-design.md", content="[full design content from template above]")
# Naming convention: always use -design.md suffix (brainstorming output) vs -plan.md suffix (planner output) — prevents collision in docs/plans/

# Do NOT auto-commit — let the user decide when to commit
```

### Step 2: Emit Router-Owned Handoff (CRITICAL)

Do **NOT** edit `.cc10x/*.md` from brainstorming.

Instead, end your response with this machine-readable handoff so the router can carry the design forward and let memory finalization persist it once:

```yaml
### Brainstorming Handoff (MACHINE-READABLE)
DESIGN_FILE: "{PROJECT_DIR}/docs/plans/YYYY-MM-DD-<feature>-design.md"
DESIGN_SUMMARY: "[one-sentence summary of the chosen design]"
MEMORY_NOTES:
  glossary:
    - term: "[Term]"
      meaning: "[precise meaning agreed during brainstorming]"
  decisions:
    - decision: "[what was chosen]"
      rejected: "[alternative not taken]"
      why: "[the constraint or trade-off that decided it]"
```

`MEMORY_NOTES` carries the accreted glossary and ADR-on-rejection notes to the router. Do **NOT** write memory yourself — emit the notes here and let the router-owned memory finalization persist them once. Omit a sub-key (or the whole `MEMORY_NOTES` block) if there were no glossary terms or rejected alternatives this pass. The router feeds the glossary to ORIENT (so it speaks the project's vocabulary) and both glossary and decisions to the planner.

**WHY BOTH:** The design file is the artifact. The handoff tells the router what to pass to planner and what to persist later. Memory stays single-writer and router-owned.

## Pre-Handoff Design Check (Optional)

Before presenting the saved design to the user, consider reviewing it for:

- **Architecture:** Does this follow existing codebase patterns? Are dependencies sound? Are integration points clean?
- **Security:** Auth/authz at every entry point? Input validation defined? No secrets in design?

If concerns found, revise the design file before presenting. This is a self-review — no agents spawned.

## After Brainstorming

**Announce to the user:**

> "Design saved to `{DESIGN_FILE}`. Router will carry the design reference forward and manage any research or planning transitions automatically."

The router handles workflow transitions — do not prompt the user for next steps. The router will proceed to research and/or planning automatically.

## Final Check

Before completing brainstorming:

- [ ] Purpose clearly articulated
- [ ] Users identified
- [ ] Success criteria defined
- [ ] Constraints documented
- [ ] Out of scope explicit
- [ ] Multiple approaches explored
- [ ] Design validated incrementally
- [ ] Document saved
