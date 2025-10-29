# BUILD Workflow - TDD Driven Implementation

**Triggered by:** User requests implementation or feature build work.

## Phase 0 - Complexity Gate
- Estimate scope. If complexity <=2, present the lightweight warning and wait for explicit approval before continuing.
- Confirm repositories, directories, and acceptance criteria.

## Phase 1 - Shared Context
Load these skills into shared context:
- `requirements-analysis`
- `security-patterns`
- `test-driven-development`
- `verification-before-completion`

Summarise requirements, constraints, and acceptance tests before delegating work.

## Phase 2 - Component Queue
1. Break the request into discrete components or tasks.
2. For each component, prepare a concise brief (goal, inputs, outputs, dependencies).
3. Execute the loop below for each component; process components sequentially without overlap. If the user requests parallel runs, confirm scope and handle them as separate sequential passes.

## Phase 3 - Component Execution Loop
For every component:
1. Invoke `component-builder` with the brief. Require:
   - Failing test first (RED) with command output captured.
   - Minimal implementation (GREEN).
   - Refactor while keeping tests green.
   - Verification log referencing commands executed.
2. Invoke `code-reviewer` on the resulting changes. Expect:
   - Findings with file/line references.
   - Security/performance considerations tied to the relevant skills.
   - Recommendations or approval status.
3. Invoke `integration-verifier` to confirm broader system behaviour. Expect:
   - Integration or end-to-end checks.
   - Additional tests or scripts run, plus their outputs.
4. Consolidate notes. Address blocking review feedback before moving to the next component.

Invocation pattern (for each subagent above):
- Read the subagent's SKILL.md to load its process and output format.
- Pass the component brief and relevant context.
- Require the specified outputs with file:line evidence and commands/exit codes where relevant.
- On failure, stop and ask whether to retry or continue.

Example (TDD Cycle for a Component):
Component: User authentication validator
- RED: npm test tests/auth.spec.ts -> exit 1 (expected validateToken to be defined)
- GREEN: implement validateToken in src/auth.ts:42 -> npm test -> exit 0
- REFACTOR: extract helper isExpired() -> npm test -> exit 0
- REVIEW: code-reviewer -> "approved, consider rate limiting"
- INTEGRATION: integration-verifier -> e2e login flow passes

## Phase 4 - Aggregate Verification
After all components are complete:
- Run the project's regression or test suite as appropriate.
- Produce a `Verification Summary` covering commands run, exit codes, coverage metrics (if applicable), and artefacts.

## Phase 5 - Delivery
Report back with:
- Components implemented and status of review/integration feedback.
- Evidence from tests and verification steps.
- Known follow-up work or tech debt.
- Optional prompt offering to run the review or deployment workflow if the user wants further assistance.

## Failure Handling
- If any subagent or test fails, stop, surface the failure, and ask for user direction.
- Do not mark components complete without the verification summary or without resolving reviewer blockers.

## References
- Skills guide: `docs/reference/04-SKILLS.md`
- Subagent contract: `docs/reference/03-SUBAGENTS.md`
