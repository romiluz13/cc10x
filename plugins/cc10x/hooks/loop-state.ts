// Pure loop state: artifact + events log + spawn records -> LoopState. No engine calls here.
// Mirrors the router's step rule (SKILL.md section 4 step 6c) and the hooklib finished rule as the
// data on disk has them: every position is an index into the parsed events array, never a timestamp.
import type { LoopEvent, LoopState, Spawn, Step } from '../types'
import { REMEDIATION, ROUTES, type Route } from './loop-routes'

export type Artifact = Record<string, unknown>

const NO_PHASE = 'N/A'
const OPEN = new Set(['NEEDS_INFO', 'NEEDS_GRILLING'])
const TERMINAL = new Set(['memory_finalized', 'workflow_completed', 'workflow_failed'])
const RESULTS = new Set(['result_persisted', 'memory_finalized'])
// Router law (SKILL.md section 4 step 6c): a pending original verifier that has not run takes the
// re-verify slot and keeps its task phase, on BUILD and DEBUG alike. Every other remediation row is a
// new task with its own phase (re-review, re-hunt, re-qa-build) or reuses the original phase outright.
// A QA regression run may log its executor result as qa-execute (qa-workflow.md, `qa-execute` is independently re-runnable).
const REUSED: Record<string, string[]> = { 're-verify': ['build-verify', 'debug-verify'], 're-qa-execute': ['qa-execute'] }

const str = (v: unknown): string | null => (typeof v === 'string' ? v : null)
const obj = (v: unknown): Artifact => (v !== null && typeof v === 'object' && !Array.isArray(v) ? (v as Artifact) : {})
// null, missing, '' and 'N/A' are one phase id; any other value reads as its String form.
const phaseKey = (v: unknown): string => (v === null || v === undefined || v === '' ? NO_PHASE : String(v))
export const workflowOf = (artifact: Artifact): string => str(artifact.workflow_uuid) || str(artifact.workflow_id) || ''

export function parseEvents(text: string): LoopEvent[] {
  const out: LoopEvent[] = []
  for (const line of text.replace(/^\uFEFF/, '').split('\n')) {
    let raw: unknown
    try {
      raw = JSON.parse(line)
    } catch {
      continue
    }
    const r = obj(raw)
    if (typeof r.event !== 'string' || r.agent === 'hook') continue
    out.push({
      ts: str(r.ts) ?? '',
      event: r.event,
      agent: str(r.agent) ?? '',
      phase: str(r.phase) ?? '',
      decision: str(r.decision),
      reason: str(r.reason),
      phaseId: phaseKey(obj(r.details).phase_id),
    })
  }
  return out
}

// A string or number reads as its String form, like phaseKey on the events side; anything else, or '', has no id.
const idOf = (v: unknown): string | null => (typeof v === 'string' || typeof v === 'number' ? String(v) || null : null)

function phasesOf(artifact: Artifact, warnings: string[] = []): { id: string; status: string }[] {
  const raw = Array.isArray(artifact.normalized_phases) ? artifact.normalized_phases : []
  const status = obj(artifact.phase_status)
  return raw.map((p, i) => {
    // Entries are keyed `phase_id` (0161b108, 2026-10-15) or `id` (7e99ef54, 10-18; 419e2736, 10-20);
    // a bare string or number entry is its own id.
    const id = idOf(p) ?? idOf(obj(p).id)
    const phaseId = idOf(obj(p).phase_id)
    if (id !== null && phaseId !== null && id !== phaseId) {
      warnings.push('normalized_phases[' + i + ']: id ' + id + ' and phase_id ' + phaseId + ' differ; using id')
    }
    const key = id ?? phaseId ?? ''
    if (key === '') warnings.push('normalized_phases[' + i + '] has no id')
    return { id: key, status: str(status[key]) ?? 'pending' }
  })
}

// The comparison cursor: 'N/A' unless phase_cursor names a phase, or it is 'memory-finalize' on a
// phased workflow (the router flips it at the memory step, after build-finish; the last phase id still matches).
function cursorOf(artifact: Artifact): string {
  const raw = str(artifact.phase_cursor)
  const ids = phasesOf(artifact)
    .map(p => p.id)
    .filter(id => id !== '')
  if (raw !== null && ids.includes(raw)) return raw
  if (raw === 'memory-finalize' && ids.length > 0) return ids[ids.length - 1]
  return NO_PHASE
}

export function isFinished(artifact: Artifact, events: LoopEvent[]): boolean {
  if (artifact.phase_cursor === 'memory-finalize' && obj(artifact.phase_status)['memory-finalize'] === 'completed') return true
  const history = Array.isArray(artifact.status_history) ? artifact.status_history : []
  const last = obj(history[history.length - 1])
  const historyTerminal = typeof last.event === 'string' && TERMINAL.has(last.event)
  const newest = events[events.length - 1]
  if (newest === undefined) return historyTerminal
  const logTerminal = TERMINAL.has(newest.event)
  const historyTs = str(last.ts)
  // Router-written ISO stamps compare as strings; the later one decides when both exist and differ.
  if (historyTs !== null && newest.ts !== '' && historyTs !== newest.ts) {
    return historyTs > newest.ts ? historyTerminal : logTerminal
  }
  return historyTerminal || logTerminal
}

function boundaryOf(events: LoopEvent[], cursor: string): number {
  let boundary = -1
  let started = -1
  events.forEach((e, i) => {
    if (e.event === 'workflow_started') started = i
    const isBoundary =
      (e.event === 'remediation_created' || (e.event === 'phase_started' && cursor !== NO_PHASE)) && e.phaseId === cursor
    if (isBoundary) boundary = i
  })
  return boundary === -1 ? started : boundary
}

function chainOf(artifact: Artifact, remediation: boolean, warnings: string[]): Route[] {
  const type = str(artifact.workflow_type) ?? ''
  // Escalation to standard is one-way (build-workflow.md escalation rule): standard in either location wins.
  const scopes = [artifact.build_scope, obj(artifact.results).build_scope]
  const trivial = scopes.includes('trivial') && !scopes.includes('standard')
  const regression = type === 'QA' && str(artifact.source_wf)
  const key = type === 'BUILD' && trivial ? 'BUILD_TRIVIAL' : regression ? 'QA_REGRESSION' : type
  // Own keys only: a type naming an Object.prototype key ('constructor') is unknown, never a chain.
  const route = Object.hasOwn(ROUTES, key) ? ROUTES[key] : undefined
  const fix = Object.hasOwn(REMEDIATION, key) ? REMEDIATION[key] : undefined
  if (remediation && fix === undefined && route !== undefined) warnings.push('no remediation chain for ' + key)
  const chain = (remediation && fix) || route
  if (chain === undefined) warnings.push('unknown workflow type: ' + (type || '(missing)'))
  return chain ?? []
}

export function deriveSteps(artifact: Artifact, events: LoopEvent[], spawns: Spawn[], warnings: string[] = []): Step[] {
  const cursor = cursorOf(artifact)
  const boundary = boundaryOf(events, cursor)
  const chain = chainOf(artifact, events[boundary]?.event === 'remediation_created', warnings)
  const results = events
    .map((e, i) => ({ e, i }))
    .filter(({ e, i }) => i > boundary && RESULTS.has(e.event) && e.phaseId === cursor)
  const matches = (row: Route, e: LoopEvent) =>
    e.agent === row.agent && (row.anyPhase === true || e.phase === row.phase || REUSED[row.phase]?.includes(e.phase) === true)

  const steps: Step[] = chain.map(row => {
    const hits = results.filter(({ e }) => matches(row, e))
    const last = hits[hits.length - 1]
    const base = { agent: row.agent, phase: row.phase, parallel: row.parallel === true, startedAt: null, extra: false }
    if (last !== undefined && !OPEN.has(last.e.decision ?? '')) {
      return { ...base, status: 'done', decision: last.e.decision, at: last.e.ts }
    }
    return { ...base, status: 'pending', decision: last?.e.decision ?? null, at: last?.e.ts ?? null }
  })

  // A live spawn (this workflow's, after the boundary, no result of its agent at or after it) runs exactly
  // one row of its agent: the first not done in chain order, else the last (a re-dispatch without
  // remediation_created). Spawns outlive their workflow, so another workflow's spawn never binds, and
  // an unknown workflow ('') never binds on either side.
  const wf = workflowOf(artifact)
  for (const agent of new Set(chain.map(row => row.agent))) {
    const live = spawns.filter(
      s =>
        s.agent === agent &&
        s.phaseId === cursor &&
        s.atIndex > boundary &&
        !events.some((e, i) => i >= s.atIndex && e.event === 'result_persisted' && e.agent === s.agent),
    )
    // Another workflow's spawn is a correct non-match; only a spawn of no known workflow is an anomaly.
    for (const s of live) {
      if (s.wf === '') {
        warnings.push('spawn of ' + agent + ' (workflow unknown) not bound to ' + (wf || 'unknown'))
      }
    }
    const spawn = live.filter(s => s.wf !== '' && s.wf === wf).pop()
    if (spawn === undefined) continue
    const rows = steps.flatMap((s, i) => (s.agent === agent ? [i] : []))
    const at = rows.find(i => steps[i].status !== 'done') ?? rows[rows.length - 1]
    steps[at] = { ...steps[at], status: 'running', decision: null, at: null, startedAt: spawn.startedAt }
  }

  // Nothing the router logged is hidden: results that fit no chain row become extra done rows.
  const extras = new Map<string, Step>()
  for (const { e, i } of events.map((e, i) => ({ e, i }))) {
    if (i <= boundary || e.event !== 'result_persisted' || chain.some(row => matches(row, e))) continue
    extras.set(e.agent + '/' + e.phase, {
      agent: e.agent,
      phase: e.phase,
      status: 'done',
      decision: e.decision,
      at: e.ts,
      startedAt: null,
      parallel: false,
      extra: true,
    })
  }
  return [...steps, ...extras.values()]
}

// The next step: the first pending row after the last done or running chain row (extra rows never
// count), skipping the parallel siblings of a running row (they were dispatched together), else the
// first pending row (a skipped optional step never pins it once a later row completed).
export function nextStep(steps: Step[]): Step | undefined {
  let last = -1
  steps.forEach((s, i) => {
    if (s.status !== 'pending' && !s.extra) last = i
  })
  let from = last + 1
  while (last >= 0 && steps[last].status === 'running' && steps[last].parallel && steps[from]?.parallel) from += 1
  return steps.slice(from).find(s => s.status === 'pending') ?? steps.find(s => s.status === 'pending')
}

export function deriveLoop(input: {
  path: string
  artifact: Artifact
  events: LoopEvent[]
  spawns: Spawn[]
  otherLive: number
  warnings: string[]
}): LoopState {
  const { artifact, events } = input
  const cursor = cursorOf(artifact)
  const warnings = [...input.warnings]
  return {
    wf: workflowOf(artifact),
    path: input.path,
    type: str(artifact.workflow_type) ?? '',
    request: str(artifact.user_request) ?? '',
    phases: phasesOf(artifact, warnings),
    cursor,
    rawCursor: str(artifact.phase_cursor),
    steps: deriveSteps(artifact, events, input.spawns, warnings),
    gate: str(artifact.pending_gate),
    // Workflow-wide, like the circuit breaker (remediation-and-research.md): the larger of remediation_history
    // and the log's remediation_created count, since a missed append on either side never lowers it.
    rounds: Math.max(
      Array.isArray(artifact.remediation_history) ? artifact.remediation_history.length : 0,
      events.filter(e => e.event === 'remediation_created').length,
    ),
    events,
    otherLive: input.otherLive,
    warnings,
  }
}

export function elapsed(ms: number): string {
  const total = Math.max(0, Math.floor(ms / 1000))
  const m = Math.floor(total / 60)
  const s = String(total % 60).padStart(2, '0')
  return m >= 60 ? Math.floor(m / 60) + 'h' + String(m % 60).padStart(2, '0') + 'm' : m + 'm' + s + 's'
}

// The circuit breaker's remediation round cap.
export const BREAKER = 3

// The workflow-wide round count against the circuit breaker: 'N/3' up to it; past it the bare count,
// since '8/3' reads like a cap the count can never pass.
export const remediation = (rounds: number): string => (rounds > BREAKER ? String(rounds) : rounds + '/' + BREAKER)

export function bandLine(state: LoopState, now: number): string {
  // Plain concatenation throughout: this file stays free of engine calls and of template syntax.
  const head = ['cc10x', state.type, state.cursor === NO_PHASE ? '' : state.cursor + '/' + state.phases.length].filter(s => s !== '').join(' ')
  const running = state.steps.filter(s => s.status === 'running')
  const started = Math.min(...running.map(s => s.startedAt ?? now))
  const next = nextStep(state.steps)
  const segments = [
    running.length > 0 ? running.map(s => s.agent).join(' ‖ ') + ' running ' + elapsed(now - started) : '',
    next !== undefined ? 'next: ' + next.agent : '',
    state.rounds > 0 ? 'rem ' + remediation(state.rounds) : '',
    state.gate !== null ? 'gate: ' + state.gate : '',
  ]
  return [head, ...segments.filter(s => s !== '')].join(' · ')
}
