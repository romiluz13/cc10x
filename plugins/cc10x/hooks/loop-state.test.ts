import { expect, test } from 'claude-code/testing'

import type { LoopEvent, Spawn } from '../types'
import {
  BUILD_EXTRA_ROW,
  BUILD_FINISHING,
  BUILD_MID_PHASE,
  BUILD_PHASE_ID_KEY,
  BUILD_REMEDIATION,
  BUILD_TRIVIAL_MID,
  DEBUG_MID,
  FINISHED_BUILD,
  PLAN_AT_GAP1,
  QA_MID,
  TRIAGE_NEEDS_INFO,
  type LoopFixture,
} from './loop-fixtures'
import { REMEDIATION, ROUTES } from './loop-routes'
import { bandLine, deriveLoop, deriveSteps, isFinished, nextStep, parseEvents, type Artifact } from './loop-state'

// 2026-10-18T12:51:24Z, the second the case-2 APPROVE record carries.
const NOW = 1_792_327_884_000

function load(fixture: LoopFixture, patch: (artifact: Artifact) => void = () => {}) {
  const artifact = JSON.parse(fixture.artifactText) as Artifact
  patch(artifact)
  return { artifact, events: parseEvents(fixture.eventsText) }
}

function loop(fixture: LoopFixture, spawns: Spawn[] = [], patch?: (artifact: Artifact) => void) {
  const { artifact, events } = load(fixture, patch)
  return deriveLoop({ path: fixture.path, artifact, events, spawns, otherLive: 0, warnings: [] })
}

const row = (steps: { agent: string; phase: string }[], agent: string, phase?: string) =>
  steps.find(s => s.agent === agent && (phase === undefined || s.phase === phase))

const brief = (steps: { agent: string; phase: string; status: string; decision: string | null }[]) =>
  steps.map(s => `${s.agent}/${s.phase} ${s.status}${s.decision ? ' ' + s.decision : ''}`)

test('1. BUILD mid-phase: builder done PASS, reviewer, hunter and verifier pending', () => {
  const { artifact, events } = load(BUILD_MID_PHASE)
  const steps = deriveSteps(artifact, events, [])

  expect(row(steps, 'component-builder')).toMatchObject({ status: 'done', decision: 'PASS', phase: 'build-implement' })
  expect(row(steps, 'code-reviewer')?.status).toBe('pending')
  expect(row(steps, 'failure-hunter')?.status).toBe('pending')
  expect(row(steps, 'integration-verifier')?.status).toBe('pending')
})

test('2. a spawn after the boundary runs the row; a result at or after its index completes it', () => {
  const { artifact, events } = load(BUILD_MID_PHASE)
  const spawn: Spawn = { agent: 'code-reviewer', atIndex: events.length, startedAt: NOW, phaseId: 'P3', wf: String(artifact.workflow_uuid) }

  expect(row(deriveSteps(artifact, events, [spawn]), 'code-reviewer')).toMatchObject({ status: 'running', startedAt: NOW })

  // The router batches ts: the result may carry the same second as the spawn's clock.
  const approve: LoopEvent = {
    ts: '2026-10-18T12:51:24Z',
    event: 'result_persisted',
    agent: 'code-reviewer',
    phase: 'build-review',
    decision: 'APPROVE',
    reason: null,
    phaseId: 'P3',
  }
  expect(row(deriveSteps(artifact, [...events, approve], [spawn]), 'code-reviewer')).toMatchObject({
    status: 'done',
    decision: 'APPROVE',
  })
})

test('3. after remediation_created the chain is REMEDIATION.BUILD with the REM-FIX builder done FIXED', () => {
  const { artifact, events } = load(BUILD_REMEDIATION)
  const steps = deriveSteps(artifact, events, [])

  expect(steps.slice(0, REMEDIATION.BUILD.length).map(s => s.phase)).toEqual(REMEDIATION.BUILD.map(r => r.phase))
  expect(row(steps, 'component-builder')).toMatchObject({ status: 'done', decision: 'FIXED', phase: 'build-implement' })
  expect(row(steps, 'code-reviewer')).toMatchObject({ phase: 're-review', status: 'pending' })
})

test('4. isFinished mirrors the hooklib rule', () => {
  const finished = load(FINISHED_BUILD)
  const mid = load(BUILD_MID_PHASE)

  expect(isFinished(finished.artifact, finished.events)).toBe(true)
  expect(isFinished(mid.artifact, mid.events)).toBe(false)
})

test('5. single-pass routes: TRIAGE paused on needs_info; QA and DEBUG chains', () => {
  const triage = loop(TRIAGE_NEEDS_INFO)
  expect(triage.gate).toBe('needs_info')
  expect(row(triage.steps, 'triage-agent', 'triage')?.status).toBe('pending')

  const qa = loop(QA_MID)
  expect(qa.steps.slice(0, ROUTES.QA.length).map(s => s.phase)).toEqual(ROUTES.QA.map(r => r.phase))
  expect(row(qa.steps, 'qa-researcher', 'qa-research')?.status).toBe('done')
  expect(bandLine(qa, NOW)).toBe('cc10x QA · next: planner')

  const debug = loop(DEBUG_MID)
  expect(debug.steps.slice(0, ROUTES.DEBUG.length).map(s => s.phase)).toEqual(ROUTES.DEBUG.map(r => r.phase))
  expect(row(debug.steps, 'bug-investigator')?.status).toBe('done')
  expect(bandLine(debug, NOW)).toBe('cc10x DEBUG · next: code-reviewer')
})

test('6. PLAN as written on disk: cursor N/A, planner done NEEDS_CLARIFICATION, gap-1 next, extras kept', () => {
  const state = loop(PLAN_AT_GAP1)

  expect(state.cursor).toBe('N/A')
  expect(state.rawCursor).toBe('plan-create')
  expect(row(state.steps, 'planner', 'plan-create')).toMatchObject({ status: 'done', decision: 'NEEDS_CLARIFICATION' })
  expect(row(state.steps, 'plan-gap-reviewer', 'plan-review-gap-1')?.status).toBe('pending')
  expect(bandLine(state, NOW)).toBe('cc10x PLAN · next: plan-gap-reviewer')
  expect(brief(state.steps)).toContain('exploration/plan done DESIGN_SAVED')
})

test('7. a spawn recorded at or before a later boundary is stale', () => {
  const { artifact, events } = load(BUILD_MID_PHASE)
  const boundary = events.findIndex(e => e.event === 'phase_started' && e.phaseId === 'P3')
  expect(boundary).toBeGreaterThan(0)

  const stale: Spawn = { agent: 'code-reviewer', atIndex: boundary, startedAt: NOW, phaseId: 'P3', wf: String(artifact.workflow_uuid) }
  expect(row(deriveSteps(artifact, events, [stale]), 'code-reviewer')?.status).toBe('pending')
})

test('8. parseEvents skips junk and hook records, keeps indices dense, defaults phaseId to N/A', () => {
  const text = [
    '{"ts":"2026-10-20T06:32:53Z","event":"workflow_started","phase":"build","agent":"router","decision":"start"}',
    'not json',
    '{"ts":"2026-10-20T06:33:00Z","event":"artifact_mutated","agent":"hook","details":{"phase_id":"P1"}}',
    '{"ts":"2026-10-20T06:34:00Z","event":"result_persisted","phase":"build-implement","agent":"component-builder","decision":"PASS","reason":"P1 builder green","details":{"phase_id":"P1"}}',
    '',
  ].join('\n')
  const events = parseEvents(text)

  expect(events).toHaveLength(2)
  expect(events[0]).toMatchObject({ event: 'workflow_started', phaseId: 'N/A', decision: 'start', reason: null })
  expect(events[1]).toMatchObject({ event: 'result_persisted', agent: 'component-builder', phaseId: 'P1', reason: 'P1 builder green' })
})

test('9. bandLine names the phase, the running agent and the next step', () => {
  const { artifact, events } = load(BUILD_MID_PHASE)
  const spawn: Spawn = { agent: 'code-reviewer', atIndex: events.length, startedAt: NOW - 125_000, phaseId: 'P3', wf: String(artifact.workflow_uuid) }
  const state = deriveLoop({ path: BUILD_MID_PHASE.path, artifact, events, spawns: [spawn], otherLive: 0, warnings: [] })
  const line = bandLine(state, NOW)

  expect(line).toContain('BUILD P3/7')
  expect(line).toContain('code-reviewer running 2m05s')
  expect(line).toContain('next: integration-verifier')
})

test('10. an empty events array with a warning yields every chain row pending', () => {
  const { artifact } = load(BUILD_MID_PHASE)
  const state = deriveLoop({ path: BUILD_MID_PHASE.path, artifact, events: [], spawns: [], otherLive: 0, warnings: ['events log too large'] })

  expect(state.steps.length).toBe(ROUTES.BUILD.length)
  expect(state.steps.every(s => s.status === 'pending')).toBe(true)
  expect(state.warnings).toEqual(['events log too large'])
})

test('11. a trivial no-plan BUILD: cursor N/A, reduced chain, scope read from either location', () => {
  const expected = ['component-builder/build-implement done PASS', 'integration-verifier/build-verify pending', 'router/memory-finalize pending']
  const under = loop(BUILD_TRIVIAL_MID)

  expect(under.cursor).toBe('N/A')
  expect(under.rawCursor).toBeNull()
  expect(brief(under.steps)).toEqual(expected)
  expect(bandLine(under, NOW)).toBe('cc10x BUILD · next: integration-verifier')

  const top = loop(BUILD_TRIVIAL_MID, [], a => {
    a.build_scope = 'trivial'
    ;(a.results as Record<string, unknown>).build_scope = null
  })
  expect(brief(top.steps)).toEqual(expected)
})

test('12. finishing BUILD: build-finish done DONE, doc-syncer pending, next is the router memory step', () => {
  const state = loop(BUILD_FINISHING)

  expect(state.cursor).toBe('P7')
  expect(state.steps.slice(0, ROUTES.BUILD.length).map(s => s.phase)).toEqual(ROUTES.BUILD.map(r => r.phase))
  expect(row(state.steps, 'router', 'build-finish')).toMatchObject({ status: 'done', decision: 'DONE' })
  expect(row(state.steps, 'doc-syncer', 'build-doc-sync')?.status).toBe('pending')
  expect(row(state.steps, 'router', 'memory-finalize')?.status).toBe('pending')
  expect(bandLine(state, NOW)).toContain('BUILD P7/7')
  expect(bandLine(state, NOW)).toContain('next: router')

  const { artifact, events } = load(BUILD_FINISHING)
  expect(isFinished(artifact, events)).toBe(false)
})

test('13. the memory-finalize cursor window keeps the last phase id; PLAN stays N/A', () => {
  const flip = (a: Artifact) => {
    a.phase_cursor = 'memory-finalize'
  }
  const state = loop(BUILD_FINISHING, [], flip)
  const unflipped = loop(BUILD_FINISHING)

  expect(state.cursor).toBe('P7')
  expect(state.rawCursor).toBe('memory-finalize')
  expect(brief(state.steps)).toEqual(brief(unflipped.steps))
  expect(bandLine(state, NOW)).toContain('next: router')
  const { artifact, events } = load(BUILD_FINISHING, flip)
  expect(isFinished(artifact, events)).toBe(false)

  expect(loop(PLAN_AT_GAP1, [], flip).cursor).toBe('N/A')
})

test('14. normalized_phases keyed phase_id (0161b108 shape): cursor P1, four phases, builder done', () => {
  const state = loop(BUILD_PHASE_ID_KEY)

  expect(state.cursor).toBe('P1')
  expect(state.phases.length).toBe(4)
  expect(state.phases[0]).toEqual({ id: 'P1', status: 'in_progress' })
  expect(row(state.steps, 'component-builder')).toMatchObject({ status: 'done', decision: 'PASS', phase: 'build-implement' })
  expect(bandLine(state, NOW)).toBe('cc10x BUILD P1/4 · next: code-reviewer')
})

test('15. nextStep: a pending parallel sibling after a done sibling is next; after a running one it is skipped', () => {
  const step = (agent: string, status: 'done' | 'running' | 'pending', parallel = false) => ({
    agent,
    phase: agent,
    status,
    decision: null,
    at: null,
    startedAt: null,
    parallel,
    extra: false,
  })
  const afterDone = [step('component-builder', 'done'), step('code-reviewer', 'done', true), step('failure-hunter', 'pending', true), step('integration-verifier', 'pending')]
  expect(nextStep(afterDone)?.agent).toBe('failure-hunter')

  const afterRunning = [step('component-builder', 'done'), step('code-reviewer', 'running', true), step('failure-hunter', 'pending', true), step('integration-verifier', 'pending')]
  expect(nextStep(afterRunning)?.agent).toBe('integration-verifier')
})

test('16. a spawn recorded after the row\'s last result re-runs the row (re-dispatch without remediation_created)', () => {
  const { artifact, events } = load(BUILD_REMEDIATION)
  const again: Spawn = { agent: 'component-builder', atIndex: events.length, startedAt: NOW, phaseId: 'P1', wf: String(artifact.workflow_uuid) }

  expect(row(deriveSteps(artifact, events, []), 'component-builder')?.status).toBe('done')
  expect(row(deriveSteps(artifact, events, [again]), 'component-builder')).toMatchObject({ status: 'running', startedAt: NOW })
})

test('17. parseEvents stringifies a numeric phase_id and survives a BOM; the band collapses a missing type', () => {
  const text = [
    '\uFEFF{"ts":"2026-10-20T06:32:53Z","event":"workflow_started","phase":"build","agent":"router","decision":"start"}',
    '{"ts":"2026-10-20T06:34:00Z","event":"result_persisted","phase":"build-implement","agent":"component-builder","decision":"PASS","details":{"phase_id":3}}',
  ].join('\n')
  const events = parseEvents(text)
  expect(events).toHaveLength(2)
  expect(events[1].phaseId).toBe('3')

  const untyped = loop(QA_MID, [], a => {
    delete a.workflow_type
  })
  expect(bandLine(untyped, NOW)).toBe('cc10x')
})

const record = (event: string, agent = 'router', phase = '', decision: string | null = null, phaseId = 'N/A'): LoopEvent => ({
  ts: '2026-10-20T09:00:00Z',
  event,
  agent,
  phase,
  decision,
  reason: null,
  phaseId,
})

test('18. a repeated agent: a planner spawn after gap-1 runs re-plan only; plan-create keeps its decision', () => {
  const { artifact, events } = load(PLAN_AT_GAP1)
  const after = [...events, record('result_persisted', 'plan-gap-reviewer', 'plan-review-gap-1', 'FINDINGS')]
  const spawn: Spawn = { agent: 'planner', atIndex: after.length, startedAt: NOW, phaseId: 'N/A', wf: String(artifact.workflow_uuid) }
  const state = deriveLoop({ path: PLAN_AT_GAP1.path, artifact, events: after, spawns: [spawn], otherLive: 0, warnings: [] })

  expect(row(state.steps, 'planner', 'plan-create')).toMatchObject({ status: 'done', decision: 'NEEDS_CLARIFICATION' })
  expect(row(state.steps, 'planner', 're-plan')).toMatchObject({ status: 'running', startedAt: NOW })
  expect(bandLine(state, NOW)).toBe('cc10x PLAN · planner running 0m00s · next: plan-gap-reviewer')
})

test('19. a gap-1 spawn runs gap-1 only; gap-2 stays pending', () => {
  const { artifact, events } = load(PLAN_AT_GAP1)
  const spawn: Spawn = { agent: 'plan-gap-reviewer', atIndex: events.length, startedAt: NOW, phaseId: 'N/A', wf: String(artifact.workflow_uuid) }
  const steps = deriveSteps(artifact, events, [spawn])

  expect(row(steps, 'plan-gap-reviewer', 'plan-review-gap-1')?.status).toBe('running')
  expect(row(steps, 'plan-gap-reviewer', 'plan-review-gap-2')?.status).toBe('pending')
})

const artifactOf = (key: string): Artifact =>
  key === 'BUILD_TRIVIAL'
    ? { workflow_uuid: 'wf-1', workflow_type: 'BUILD', build_scope: 'trivial' }
    : key === 'QA_REGRESSION'
      ? { workflow_uuid: 'wf-1', workflow_type: 'QA', source_wf: 'wf-0' }
      : { workflow_uuid: 'wf-1', workflow_type: key }

test('20. on every ROUTES and REMEDIATION chain one spawn of any agent runs exactly one row', () => {
  const tables: [Record<string, { agent: string; phase: string }[]>, boolean][] = [
    [ROUTES, false],
    [REMEDIATION, true],
  ]
  for (const [table, remediation] of tables) {
    for (const [key, chain] of Object.entries(table)) {
      const artifact = artifactOf(key)
      const head = [record('workflow_started'), ...(remediation ? [record('remediation_created')] : [])]
      const allDone = [...head, ...chain.map(r => record('result_persisted', r.agent, r.phase, 'PASS'))]
      for (const events of [head, allDone]) {
        for (const agent of new Set(chain.map(r => r.agent))) {
          const spawn: Spawn = { agent, atIndex: events.length, startedAt: NOW, phaseId: 'N/A', wf: String(artifact.workflow_uuid) }
          const steps = deriveSteps(artifact, events, [spawn])
          const agents = chain.map(r => r.agent)
          // Not yet run: the first row of that agent; every row done: the last one (a re-dispatch).
          const expected = events === head ? agents.indexOf(agent) : agents.lastIndexOf(agent)
          const running = steps.flatMap((s, i) => (s.status === 'running' ? [i] : []))

          expect([key, remediation, agent, steps.slice(0, chain.length).map(s => s.phase)]).toEqual([key, remediation, agent, chain.map(r => r.phase)])
          expect([key, remediation, agent, running]).toEqual([key, remediation, agent, [expected]])
          expect([key, agent, steps.filter(s => s.status === 'done').length]).toEqual([key, agent, events === head ? 0 : chain.length - 1])
        }
      }
    }
  }
})

test('21. after remediation_created a never-run verifier result on build-verify completes the re-verify row (7e99ef54 events 1-97)', () => {
  const { artifact } = load(FINISHED_BUILD, a => {
    a.phase_cursor = 'P6'
  })
  const events = parseEvents(FINISHED_BUILD.eventsText.split('\n').slice(0, 97).join('\n'))
  expect(events[91]).toMatchObject({ event: 'remediation_created', phaseId: 'P6' })
  expect(events[96]).toMatchObject({ agent: 'integration-verifier', phase: 'build-verify', decision: 'FAIL', phaseId: 'P6' })

  expect(brief(deriveSteps(artifact, events, []))).toEqual([
    'component-builder/build-implement done FIXED',
    'code-reviewer/re-review done CHANGES_REQUESTED',
    'failure-hunter/re-hunt done ISSUES_FOUND',
    'integration-verifier/re-verify done FAIL',
    'doc-syncer/build-doc-sync pending',
    'router/build-finish pending',
    'router/memory-finalize pending',
  ])
})

test('22. an extra row never pins next: 0161b108 mid P4 reads next: router (memory step)', () => {
  const state = loop(BUILD_EXTRA_ROW)

  expect(state.cursor).toBe('P4')
  expect(row(state.steps, 'router', 'build-finish')).toMatchObject({ status: 'done', decision: 'pushed', extra: false })
  expect(row(state.steps, 'planner', 're-plan')).toMatchObject({ status: 'done', decision: 'PLAN_CREATED', extra: true })
  // 0161b108's remediation_history holds nine rounds; the band shows the breaker count unclamped.
  expect(bandLine(state, NOW)).toBe('cc10x BUILD P4/4 · next: router · rem 9/3')
})

test('23. normalized_phases: numeric and bare-string entries are their own ids; an entry with no id warns', () => {
  const state = loop(BUILD_MID_PHASE, [], a => {
    a.normalized_phases = ['P1', 2, { id: 3 }, { phase_id: 'P4' }, {}, null]
    a.phase_status = { P1: 'completed', '2': 'completed', '3': 'in_progress' }
    a.phase_cursor = '3'
  })

  expect(state.phases).toEqual([
    { id: 'P1', status: 'completed' },
    { id: '2', status: 'completed' },
    { id: '3', status: 'in_progress' },
    { id: 'P4', status: 'pending' },
    { id: '', status: 'pending' },
    { id: '', status: 'pending' },
  ])
  expect(state.cursor).toBe('3')
  expect(state.warnings).toEqual(['normalized_phases[4] has no id', 'normalized_phases[5] has no id'])
})

test('24. normalized_phases: id wins over a differing phase_id, with a warning', () => {
  const state = loop(BUILD_MID_PHASE, [], a => {
    a.normalized_phases = [{ id: 'P1', phase_id: 'P9' }, { id: 'P2', phase_id: 'P2' }]
  })

  expect(state.phases.map(p => p.id)).toEqual(['P1', 'P2'])
  expect(state.warnings).toEqual(['normalized_phases[0]: id P1 and phase_id P9 differ; using id'])
})

test('25. an unknown workflow_type yields no chain rows and a warning', () => {
  const state = loop(QA_MID, [], a => {
    a.workflow_type = 'NOPE'
  })

  expect(state.steps.filter(s => !s.extra)).toEqual([])
  expect(state.warnings).toEqual(['unknown workflow type: NOPE'])
})

const synthetic = (key: string, events: LoopEvent[]) =>
  deriveLoop({ path: '/repo/.cc10x/workflows/wf-1.json', artifact: artifactOf(key), events, spawns: [], otherLive: 0, warnings: [] })

test('26. DEBUG: a reused never-run verifier result on debug-verify completes the re-verify row', () => {
  const state = synthetic('DEBUG', [
    record('workflow_started'),
    record('result_persisted', 'bug-investigator', 'debug-investigate', 'PASS'),
    record('result_persisted', 'code-reviewer', 'debug-review', 'CHANGES_REQUESTED'),
    record('remediation_created'),
    record('result_persisted', 'bug-investigator', 'debug-investigate', 'FIXED'),
    record('result_persisted', 'code-reviewer', 're-review', 'APPROVE'),
    record('result_persisted', 'integration-verifier', 'debug-verify', 'PASS'),
  ])

  expect(brief(state.steps)).toEqual([
    'bug-investigator/debug-investigate done FIXED',
    'code-reviewer/re-review done APPROVE',
    'integration-verifier/re-verify done PASS',
    'router/memory-finalize pending',
  ])
  expect(bandLine(state, NOW)).toBe('cc10x DEBUG · next: router · rem 1/3')
})

test('27. QA: after re-qa-build the original qa-execute runs and completes the executor row', () => {
  const state = synthetic('QA', [
    record('workflow_started'),
    record('result_persisted', 'qa-harness-builder', 'qa-build', 'PASS'),
    record('remediation_created'),
    record('result_persisted', 'qa-harness-builder', 're-qa-build', 'PASS'),
    record('result_persisted', 'code-reviewer', 'qa-review', 'APPROVE'),
    record('result_persisted', 'failure-hunter', 'qa-hunt', 'CLEAN'),
    record('result_persisted', 'qa-executor', 'qa-execute', 'PASS'),
  ])

  expect(brief(state.steps)).toEqual([
    'qa-harness-builder/re-qa-build done PASS',
    'code-reviewer/qa-review done APPROVE',
    'failure-hunter/qa-hunt done CLEAN',
    'qa-executor/qa-execute done PASS',
    'router/memory-finalize pending',
  ])
  expect(bandLine(state, NOW)).toBe('cc10x QA · next: router · rem 1/3')
})

test('28. every REMEDIATION chain: an original-phase result completes a reused row; fresh remediation tasks stay pending', () => {
  // Router law (SKILL.md section 4 step 6c, remediation-and-research.md re-review loop): re-review, re-hunt
  // and re-qa-build are always new tasks; every other row reuses the original task and keeps its phase.
  const fresh = new Set(['re-review', 're-hunt', 're-qa-build'])
  for (const [key, chain] of Object.entries(REMEDIATION)) {
    chain.forEach((r, i) => {
      const own = ROUTES[key].filter(o => o.agent === r.agent)
      // A row whose agent the original route lacks (trivial BUILD's reviewer and hunter, a regression
      // run's harness builder, reviewer and hunter) has no original task: its own phase completes it.
      if (own.length === 0) {
        const steps = deriveSteps(artifactOf(key), [record('workflow_started'), record('remediation_created'), record('result_persisted', r.agent, r.phase, 'PASS')], [])
        expect([key, r.phase, steps[i].status, steps.filter(s => s.extra).length]).toEqual([key, r.phase, 'done', 0])
        return
      }
      const phase = own.some(o => o.phase === r.phase) ? r.phase : own[own.length - 1].phase
      const steps = deriveSteps(artifactOf(key), [record('workflow_started'), record('remediation_created'), record('result_persisted', r.agent, phase, 'PASS')], [])
      const want = fresh.has(r.phase) ? ['pending', 1] : ['done', 0]

      expect([key, r.phase, phase, steps[i].status, steps.filter(s => s.extra).length]).toEqual([key, r.phase, phase, ...want])
    })
  }
})

test('29. a trivial BUILD after remediation_created runs REM-FIX, re-review, re-hunt, re-verify, then memory', () => {
  const state = synthetic('BUILD_TRIVIAL', [
    record('workflow_started'),
    record('result_persisted', 'component-builder', 'build-implement', 'PASS'),
    record('result_persisted', 'integration-verifier', 'build-verify', 'FAIL'),
    record('remediation_created'),
    record('result_persisted', 'component-builder', 'build-verify', 'FIXED'),
    record('result_persisted', 'code-reviewer', 're-review', 'APPROVE'),
    record('result_persisted', 'failure-hunter', 're-hunt', 'CLEAN'),
  ])

  expect(brief(state.steps)).toEqual([
    'component-builder/build-implement done FIXED',
    'code-reviewer/re-review done APPROVE',
    'failure-hunter/re-hunt done CLEAN',
    'integration-verifier/re-verify pending',
    'router/memory-finalize pending',
  ])
  expect(bandLine(state, NOW)).toBe('cc10x BUILD · next: integration-verifier · rem 1/3')
})

test('30. a spawn from another workflow binds no row, even with atIndex beyond the events', () => {
  const { artifact, events } = load(PLAN_AT_GAP1)
  const at = { agent: 'plan-gap-reviewer', atIndex: events.length + 5, startedAt: NOW - 3_600_000, phaseId: 'N/A' }
  const foreign = loop(PLAN_AT_GAP1, [{ ...at, wf: 'wf-20261019T000000Z-00000000' }])

  expect(foreign.steps.some(s => s.status === 'running')).toBe(false)
  expect(bandLine(foreign, NOW)).toBe('cc10x PLAN · next: plan-gap-reviewer')

  // Same workflow binds; with no workflow_uuid the id falls back to workflow_id.
  const own = loop(PLAN_AT_GAP1, [{ ...at, wf: String(artifact.workflow_id) }], a => {
    delete a.workflow_uuid
  })
  expect(row(own.steps, 'plan-gap-reviewer', 'plan-review-gap-1')?.status).toBe('running')
})

test('31. rem counts the whole workflow like the circuit breaker: a P1 remediation still shows at cursor P2', () => {
  const p2 = (a: Artifact) => {
    a.phase_cursor = 'P2'
  }
  const state = loop(BUILD_REMEDIATION, [], p2)
  expect(state.cursor).toBe('P2')
  expect(state.rounds).toBe(1)
  expect(bandLine(state, NOW)).toContain('rem 1/3')

  // 7e99ef54 mid P3 carries three P1 rounds in remediation_history.
  expect(loop(BUILD_MID_PHASE).rounds).toBe(3)

  // Without a remediation_history array, every remediation_created in the log counts.
  const noHistory = loop(BUILD_MID_PHASE, [], a => {
    delete a.remediation_history
  })
  expect(noHistory.rounds).toBe(3)

  // A count past the breaker is shown as is, never clamped.
  const over = loop(BUILD_REMEDIATION, [], a => {
    p2(a)
    a.remediation_history = [{}, {}, {}, {}]
  })
  expect(bandLine(over, NOW)).toContain('rem 4/3')
})

test('32. a QA regression workflow (source_wf set) runs re-qa-execute then memory; DEBUG with source_wf keeps its chain', () => {
  const after = synthetic('QA_REGRESSION', [record('workflow_started'), record('result_persisted', 'qa-executor', 're-qa-execute', 'PASS')])
  expect(brief(after.steps)).toEqual(['qa-executor/re-qa-execute done PASS', 'router/memory-finalize pending'])
  expect(bandLine(after, NOW)).toBe('cc10x QA · next: router')

  // qa-workflow.md lets the regression run log qa-execute: it completes the same row.
  const logged = synthetic('QA_REGRESSION', [record('workflow_started'), record('result_persisted', 'qa-executor', 'qa-execute', 'PASS')])
  expect(brief(logged.steps)).toEqual(['qa-executor/re-qa-execute done PASS', 'router/memory-finalize pending'])

  const debug = deriveSteps({ workflow_uuid: 'wf-1', workflow_type: 'DEBUG', source_wf: 'wf-0' }, [record('workflow_started')], [])
  expect(debug.map(s => s.phase)).toEqual(ROUTES.DEBUG.map(r => r.phase))
})

test('33. build_scope standard in either location wins over trivial (escalation is one-way)', () => {
  const escalated = loop(BUILD_TRIVIAL_MID, [], a => {
    a.build_scope = 'trivial'
    ;(a.results as Record<string, unknown>).build_scope = 'standard'
  })
  expect(escalated.steps.slice(0, ROUTES.BUILD.length).map(s => s.phase)).toEqual(ROUTES.BUILD.map(r => r.phase))

  const top = loop(BUILD_TRIVIAL_MID, [], a => {
    a.build_scope = 'standard'
    ;(a.results as Record<string, unknown>).build_scope = 'trivial'
  })
  expect(top.steps.slice(0, ROUTES.BUILD.length).map(s => s.phase)).toEqual(ROUTES.BUILD.map(r => r.phase))
})

test('34. an empty workflow id never binds a spawn and warns; a foreign workflow\'s spawn is silent', () => {
  const { events } = load(PLAN_AT_GAP1)
  const at = { agent: 'plan-gap-reviewer', atIndex: events.length, startedAt: NOW, phaseId: 'N/A' }
  const anonymous = loop(PLAN_AT_GAP1, [{ ...at, wf: '' }], a => {
    delete a.workflow_uuid
    delete a.workflow_id
  })
  expect(anonymous.steps.some(s => s.status === 'running')).toBe(false)
  expect(anonymous.warnings).toEqual(['spawn of plan-gap-reviewer (workflow unknown) not bound to unknown'])

  // Another workflow's spawn is a correct non-match, not an anomaly: no warning.
  const foreign = loop(PLAN_AT_GAP1, [{ ...at, wf: 'wf-other' }])
  expect(foreign.steps.some(s => s.status === 'running')).toBe(false)
  expect(foreign.warnings).toEqual([])

  // A spawn dropped for another reason (before the boundary) is not a workflow mismatch.
  expect(loop(PLAN_AT_GAP1, [{ ...at, atIndex: 0, wf: 'wf-other' }]).warnings).toEqual([])
})

test('35. an empty workflow_uuid falls back to workflow_id', () => {
  const { artifact, events } = load(PLAN_AT_GAP1)
  const id = String(artifact.workflow_id)
  const state = loop(PLAN_AT_GAP1, [{ agent: 'plan-gap-reviewer', atIndex: events.length, startedAt: NOW, phaseId: 'N/A', wf: id }], a => {
    a.workflow_uuid = ''
  })
  expect(state.wf).toBe(id)
  expect(row(state.steps, 'plan-gap-reviewer', 'plan-review-gap-1')?.status).toBe('running')
})

test('36. every route a router path can remediate has a REMEDIATION chain; the rest warn instead of falling back', () => {
  // review-workflow.md forbids REVIEW remediation; PLAN, TRIAGE and CODEBASE-HEALTH create no REM-FIX.
  const never = ['PLAN', 'REVIEW', 'TRIAGE', 'CODEBASE-HEALTH']
  expect(Object.keys(ROUTES).filter(k => !never.includes(k)).sort()).toEqual(['BUILD', 'BUILD_TRIVIAL', 'DEBUG', 'QA', 'QA_REGRESSION'])
  expect(Object.keys(REMEDIATION).sort()).toEqual(['BUILD', 'BUILD_TRIVIAL', 'DEBUG', 'QA', 'QA_REGRESSION'])

  const warnings: string[] = []
  deriveSteps({ workflow_uuid: 'wf-1', workflow_type: 'REVIEW' }, [record('workflow_started'), record('remediation_created')], [], warnings)
  expect(warnings).toEqual(['no remediation chain for REVIEW'])
})

test('37. a remediated QA regression run: re-qa-build, a fresh qa-review / qa-hunt pair, then re-qa-execute', () => {
  const events = [
    record('workflow_started'),
    record('result_persisted', 'qa-executor', 're-qa-execute', 'FAIL'),
    record('remediation_created'),
  ]
  const spawn: Spawn = { agent: 'qa-harness-builder', atIndex: events.length, startedAt: NOW, phaseId: 'N/A', wf: 'wf-1' }
  const state = deriveLoop({ path: 'p', artifact: artifactOf('QA_REGRESSION'), events, spawns: [spawn], otherLive: 0, warnings: [] })

  expect(brief(state.steps)).toEqual([
    'qa-harness-builder/re-qa-build running',
    'code-reviewer/qa-review pending',
    'failure-hunter/qa-hunt pending',
    'qa-executor/re-qa-execute pending',
    'router/memory-finalize pending',
  ])
  expect(bandLine(state, NOW)).toBe('cc10x QA · qa-harness-builder running 0m00s · next: code-reviewer · rem 1/3')

  // The executor may log the rerun as qa-execute (REUSED): it completes re-qa-execute.
  const done = synthetic('QA_REGRESSION', [
    ...events,
    record('result_persisted', 'qa-harness-builder', 're-qa-build', 'PASS'),
    record('result_persisted', 'code-reviewer', 'qa-review', 'APPROVE'),
    record('result_persisted', 'failure-hunter', 'qa-hunt', 'CLEAN'),
    record('result_persisted', 'qa-executor', 'qa-execute', 'PASS'),
  ])
  expect(brief(done.steps)).toEqual([
    'qa-harness-builder/re-qa-build done PASS',
    'code-reviewer/qa-review done APPROVE',
    'failure-hunter/qa-hunt done CLEAN',
    'qa-executor/re-qa-execute done PASS',
    'router/memory-finalize pending',
  ])
  expect(done.warnings).toEqual([])
})

test('38. rem never lowers the breaker count: the larger of remediation_history and the log', () => {
  const head = [record('workflow_started'), record('remediation_created'), record('remediation_created')]
  const rounds = (history: unknown) =>
    deriveLoop({ path: 'p', artifact: { ...artifactOf('BUILD'), remediation_history: history }, events: head, spawns: [], otherLive: 0, warnings: [] }).rounds

  expect(rounds([{}])).toBe(2) // a missed history append
  expect(rounds([{}, {}, {}])).toBe(3) // a missed log record
  expect(rounds('n/a')).toBe(2) // not an array: the log alone
})

test('39. a workflow_type naming an Object.prototype key is an unknown type, not a throw', () => {
  for (const type of ['constructor', 'toString', '__proto__', 'hasOwnProperty']) {
    const state = loop(QA_MID, [], a => {
      a.workflow_type = type
    })
    expect(state.steps.filter(s => !s.extra)).toEqual([])
    expect(state.warnings).toEqual(['unknown workflow type: ' + type])
  }
  const remediated = deriveSteps({ workflow_uuid: 'wf-1', workflow_type: 'constructor' }, [record('remediation_created')], [])
  expect(remediated.filter(s => !s.extra)).toEqual([])
})
