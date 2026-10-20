export type StepStatus = 'done' | 'running' | 'pending'
export type Step = {
  agent: string
  phase: string
  status: StepStatus
  decision: string | null
  at: string | null
  startedAt: number | null
  parallel: boolean
  // true for a result that fits no chain row (appended after the chain, always done)
  extra: boolean
}
export type LoopEvent = {
  ts: string
  event: string
  agent: string
  phase: string
  decision: string | null
  reason: string | null
  phaseId: string
}
// `wf` is the spawning workflow's workflow_uuid (else workflow_id): a spawn binds rows of that workflow only.
// `wf` '' means the workflow is unknown: such a spawn never binds a row.
export type Spawn = { agent: string; atIndex: number; startedAt: number; phaseId: string; wf: string }
export type LoopState = {
  wf: string
  path: string
  type: string
  request: string
  phases: { id: string; status: string }[]
  cursor: string
  rawCursor: string | null
  steps: Step[]
  gate: string | null
  rounds: number
  events: LoopEvent[]
  otherLive: number
  warnings: string[]
}
export type LoopView = {
  live: LoopState | null
  last: { wf: string; finishedAt: string } | null
  error: string | null
}

declare module 'claude-code' {
  interface PluginState {
    // `opened`: the live workflow ids the pane already opened for unasked (OD-1 B), newest last.
    cc10x: { loop: LoopView; spawns: Spawn[]; opened: string[] }
  }
}
