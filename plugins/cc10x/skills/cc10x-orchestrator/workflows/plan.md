# PLANNING Workflow - Structured Feature Design

**Triggered by:** User asks to plan, architect, or design a feature or system update.

## Phase 0 - Complexity Gate
1. Estimate complexity using the orchestrator's Complexity Rubric (files changed, novelty, and risk cues).
2. If the score <=2, warn that cc10x is optimized for higher-risk work and wait for an explicit "yes" before proceeding.

## Phase 1 - Requirements Intake
- Load the `requirements-analysis` skill.
- Extract goals, stakeholders, user stories, acceptance criteria, assumptions, and open questions.
- Ask for clarification if critical information is missing.

## Phase 2 - Delegated Analysis
Run the bundled planning subagents sequentially, sharing the Phase 1 notes as context:
1. `planning-architecture-risk` (loads `architecture-patterns` and `risk-analysis`).
2. `planning-design-deployment` (loads `api-design-patterns`, `component-design-patterns`, and `deployment-patterns`).

Each subagent must:
- Reference the skill sections used to make decisions.
- Produce actionable outputs (diagrams, data models, API specs, risk register, deployment steps).
- Identify outstanding assumptions that require user confirmation.

Invocation pattern:
- Read the subagent's SKILL.md to load its process and output format.
- Provide the requirements summary and constraints.
- Require the specified outputs with clear traceability to requirements.
- If the subagent fails, stop and ask whether to retry or continue.

## Phase 3 - Synthesis
1. Merge subagent outputs into a single plan outline.
2. Resolve conflicts or highlight them for the user.
3. Build a file manifest and phased roadmap, noting dependencies.

## Phase 4 - Verification Summary
Before marking the plan as ready, include:
```
# Verification Summary
Inputs: <sources reviewed>
Decisions: <key architecture decisions with rationale>
Open Questions: <items awaiting user confirmation>
```

Example:
Inputs: requirements doc, existing API patterns
Decisions: JWT auth (stateless, mobile-friendly), event-driven webhooks (async resilience)
Open Questions: Stripe vs PayPal for payments? Monitoring SLA requirements?

## Phase 5 - Deliverable
Provide a markdown report containing:
- Requirements overview (user stories + acceptance criteria).
- Architecture and component design.
- API/data models.
- Risk assessment with mitigations.
- Testing strategy and deployment plan.
- File manifest and implementation phases.

Offer optional next steps (for example, "Run build workflow for Phase 1?") without assuming consent.

## Failure Handling
- If a subagent fails, stop and ask whether to retry or continue without it.
- Do not fabricate architecture decisions; clearly mark any sections that could not be produced.

## References
- Skill format: `docs/reference/04-SKILLS.md`
- Subagent expectations: `docs/reference/03-SUBAGENTS.md`
