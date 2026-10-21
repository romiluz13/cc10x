// Route table only: the task chain the router runs per workflow type, in dispatch order.
// `parallel` rows run side by side; `anyPhase` matches the agent's result on any task phase
// (REM-FIX carries the originating task's phase). Python pins every phase to the router enum
// and every agent to a file under agents/ (scripts/test_cc10x_loop_routes.py).
export type Route = { agent: string; phase: string; parallel?: boolean; anyPhase?: boolean }

const finish: Route[] = [
  { agent: 'doc-syncer', phase: 'build-doc-sync' },
  { agent: 'router', phase: 'build-finish' },
  { agent: 'router', phase: 'memory-finalize' },
]
const memory: Route = { agent: 'router', phase: 'memory-finalize' }

export const ROUTES: Record<string, Route[]> = {
  BUILD: [
    { agent: 'component-builder', phase: 'build-implement' },
    { agent: 'code-reviewer', phase: 'build-review', parallel: true },
    { agent: 'failure-hunter', phase: 'build-hunt', parallel: true },
    { agent: 'integration-verifier', phase: 'build-verify' },
    ...finish,
  ],
  BUILD_TRIVIAL: [
    { agent: 'component-builder', phase: 'build-implement' },
    { agent: 'integration-verifier', phase: 'build-verify' },
    memory,
  ],
  PLAN: [
    { agent: 'planner', phase: 'plan-create' },
    { agent: 'plan-gap-reviewer', phase: 'plan-review-gap-1' },
    { agent: 'planner', phase: 're-plan' },
    { agent: 'plan-gap-reviewer', phase: 'plan-review-gap-2' },
    memory,
  ],
  DEBUG: [
    { agent: 'bug-investigator', phase: 'debug-investigate' },
    { agent: 'code-reviewer', phase: 'debug-review' },
    { agent: 'integration-verifier', phase: 'debug-verify' },
    memory,
  ],
  REVIEW: [{ agent: 'code-reviewer', phase: 'review-audit' }, memory],
  QA: [
    { agent: 'qa-researcher', phase: 'qa-research' },
    { agent: 'planner', phase: 'qa-plan' },
    { agent: 'plan-gap-reviewer', phase: 'qa-plan-review' },
    { agent: 'planner', phase: 'qa-re-plan' },
    { agent: 'plan-gap-reviewer', phase: 'qa-plan-review-2' },
    { agent: 'qa-harness-builder', phase: 'qa-preflight' },
    { agent: 'qa-harness-builder', phase: 'qa-build' },
    { agent: 'code-reviewer', phase: 'qa-review', parallel: true },
    { agent: 'failure-hunter', phase: 'qa-hunt', parallel: true },
    { agent: 'qa-executor', phase: 'qa-execute' },
    memory,
  ],
  // A QA workflow with source_wf set is a regression run (qa-workflow.md section 6): the executor only.
  QA_REGRESSION: [{ agent: 'qa-executor', phase: 're-qa-execute' }, memory],
  TRIAGE: [{ agent: 'triage-agent', phase: 'triage' }, memory],
  'CODEBASE-HEALTH': [{ agent: 'architecture-scanner', phase: 'codebase-health' }, memory],
}

export const REMEDIATION: Record<string, Route[]> = {
  BUILD: [
    { agent: 'component-builder', phase: 'build-implement', anyPhase: true },
    { agent: 'code-reviewer', phase: 're-review', parallel: true },
    { agent: 'failure-hunter', phase: 're-hunt', parallel: true },
    { agent: 'integration-verifier', phase: 're-verify' },
    ...finish,
  ],
  // A trivial BUILD runs the same re-review loop and skips doc-sync and finishing.
  BUILD_TRIVIAL: [
    { agent: 'component-builder', phase: 'build-implement', anyPhase: true },
    { agent: 'code-reviewer', phase: 're-review', parallel: true },
    { agent: 'failure-hunter', phase: 're-hunt', parallel: true },
    { agent: 'integration-verifier', phase: 're-verify' },
    memory,
  ],
  DEBUG: [
    { agent: 'bug-investigator', phase: 'debug-investigate', anyPhase: true },
    { agent: 'code-reviewer', phase: 're-review' },
    { agent: 'integration-verifier', phase: 're-verify' },
    memory,
  ],
  QA: [
    { agent: 'qa-harness-builder', phase: 're-qa-build' },
    { agent: 'code-reviewer', phase: 'qa-review', parallel: true },
    { agent: 'failure-hunter', phase: 'qa-hunt', parallel: true },
    // The original qa-execute runs after a re-qa-build; re-qa-execute is a regression run in its own workflow.
    { agent: 'qa-executor', phase: 'qa-execute' },
    memory,
  ],
  // A harness defect in a regression run routes to re-qa-build, then a fresh qa-review / qa-hunt pair
  // and the rerun (qa-workflow.md section 6). REVIEW, PLAN, TRIAGE and CODEBASE-HEALTH never remediate.
  QA_REGRESSION: [
    { agent: 'qa-harness-builder', phase: 're-qa-build' },
    { agent: 'code-reviewer', phase: 'qa-review', parallel: true },
    { agent: 'failure-hunter', phase: 'qa-hunt', parallel: true },
    { agent: 'qa-executor', phase: 're-qa-execute' },
    memory,
  ],
}
