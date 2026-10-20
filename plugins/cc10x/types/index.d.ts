export type StepStatus = 'done' | 'running' | 'pending'
export type Step = {
  agent: string
  phase: string
  status: StepStatus
  decision: string | null
  at: string | null
  startedAt: number | null
  parallel: boolean
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
export type Spawn = { agent: string; atIndex: number; startedAt: number; phaseId: string }
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
    cc10x: { loop: LoopView; spawns: Spawn[] }
  }
}
