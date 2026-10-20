import type { AgentSpawnArgs, On } from 'claude-code'
import { expect, test, type TestBody } from 'claude-code/testing'

import { BUILD_MID_PHASE, FINISHED_BUILD, type LoopFixture } from './loop-fixtures'
import { parseEvents } from './loop-state'
import type { LoopView, Spawn } from '../types'

// 2026-10-18T12:51:24Z, the second the reviewer APPROVE line below carries.
const NOW = 1_792_327_884_000
const WF = 'wf-20261018T112922Z-7e99ef54'
const APPROVE =
  '{"ts": "2026-10-18T12:51:24Z", "wf": "' + WF + '", "event": "result_persisted", "phase": "build-review", "agent": "code-reviewer", "decision": "APPROVE", "details": {"phase_id": "P3"}}\n'

type Kit = Parameters<TestBody>[0]

const bandProps = (hasSurvey = false) => ({
  hasSurvey,
  isWorking: true,
  maxRows: 3,
  bodyColumns: 100,
  scroll: { offset: 0, bodyRows: 3 },
  view: {},
})

// The disk beneath the plugin. `listing` 'missing': no .cc10x/workflows (fs.exists false, fs.list rejects);
// 'denied': the directory exists but fs.list rejects. `log` false leaves the newest artifact's events log
// unwritten; `older` lists more artifacts behind it, each a minute older, each with its log unless named in
// `noLog`. `denyRead` rejects every fs.read; `hold` answers ms to delay one fs.read by. Tests change these
// fields between refreshes.
type Disk = {
  fixture: LoopFixture
  log: boolean
  older: LoopFixture[]
  noLog: string[]
  listing: 'files' | 'empty' | 'missing' | 'denied'
  denyRead: boolean
  hold: (path: string) => number
}

function answerFs(on: On, fixture: LoopFixture): Disk {
  const disk: Disk = { fixture, log: true, older: [], noLog: [], listing: 'files', denyRead: false, hold: () => 0 }
  const eventsPath = (f: LoopFixture) => f.path.replace(/\.json$/, '.events.jsonl')
  const name = (p: string) => p.slice(p.lastIndexOf('/') + 1)
  const entry = (path: string, text: string, mtimeMs: number) =>
    ({ name: name(path), kind: 'file', size: text.length, mtimeMs, isLink: false }) as const
  on('session.root', () => ({ value: '/repo' }))
  on('clock.now', () => ({ value: NOW }))
  on('fs.exists', () => ({ value: disk.listing !== 'missing' }))
  on('fs.list', () => {
    if (disk.listing === 'missing') return { deny: 'ENOENT: no such directory' }
    if (disk.listing === 'denied') return { deny: 'EACCES: list refused' }
    if (disk.listing === 'empty') return { value: [] }
    const files = [entry(disk.fixture.path, disk.fixture.artifactText, NOW)]
    if (disk.log) files.push(entry(eventsPath(disk.fixture), disk.fixture.eventsText, NOW))
    disk.older.forEach((f, i) => {
      files.push(entry(f.path, f.artifactText, NOW - 60_000 * (i + 1)))
      if (!disk.noLog.includes(f.path)) files.push(entry(eventsPath(f), f.eventsText, NOW - 60_000 * (i + 1)))
    })
    return { value: files }
  })
  on('fs.read', async (_, e) => {
    if (disk.denyRead) return { deny: 'EACCES: read refused' }
    const ms = disk.hold(e.path)
    if (ms > 0) await new Promise(resolve => setTimeout(resolve, ms))
    for (const f of [disk.fixture, ...disk.older]) {
      const logged = f === disk.fixture ? disk.log : !disk.noLog.includes(f.path)
      if (e.path === f.path) return { value: f.artifactText }
      if (e.path === eventsPath(f) && logged) return { value: f.eventsText }
    }
    return { deny: 'ENOENT: ' + e.path }
  })
  return disk
}

// What the plugin last wrote to its atoms: the test spies on `state.set` and lets the kit store it.
function watchState(on: On) {
  const seen: { loop?: LoopView; spawns?: Spawn[] } = {}
  on('state.set', (_, e, next) => {
    const w = e as { plugin: string; key: string; value: unknown }
    if (w.plugin === 'cc10x' && (w.key === 'loop' || w.key === 'spawns')) Object.assign(seen, { [w.key]: w.value })
    return next(e)
  })
  return seen
}

// The rest of the engine: every other call the hooks make, answered plainly.
// `refuse` names engine calls that answer `{ deny }` instead.
// 'agent.spawn!' makes the core spawn itself throw.
function engine(on: On, logs: string[] = [], refuse: ('command.register' | 'agent.spawn' | 'agent.spawn!')[] = []) {
  on('command.register', () => (refuse.includes('command.register') ? { deny: 'refused' } : { value: { command: 'cc10x-loop' } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('tool.call', () => ({ result: {} }))
  on('agent.spawn', () => {
    if (refuse.includes('agent.spawn!')) throw new Error('core spawn down')
    return refuse.includes('agent.spawn') ? { deny: 'another plugin refused' } : { model: 'test', agentId: 'agent-1' }
  })
  on('turn.complete', (_, e) => ({ text: e.answer }))
  on('ui.log', (_, e) => {
    logs.push(e.text)
    return { value: undefined }
  })
  on('ui.render', ($, e) => {
    const { Text } = $.ui.resolve(e)
    return <Text>engine</Text>
  })
  return watchState(on)
}

const band = async ($: Kit, surface: 'terminal' | 'desktop' = 'terminal', hasSurvey = false) => {
  const ui = await $.ui.mount({ plugin: 'cc10x', component: 'AbovePrompt', surface, props: bandProps(hasSurvey) })
  const text = (await ui.find({ type: 'Text', text: /./ }))?.text
  await ui.unmount()
  return text
}

const start = ($: Kit) =>
  $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })

// The engine fills `provider` with the plugin id (`name@marketplace`); the test kit passes it through as given.
const fromCc10x = (subagentType: string, provider = 'cc10x@cc10x') =>
  ({ prompt: 'run', description: subagentType, subagentType, provider: { plugin: provider, tier: 'user' } }) as AgentSpawnArgs
const reviewer = fromCc10x('cc10x:code-reviewer')
const hunter = fromCc10x('cc10x:failure-hunter')
const turnDone = { answer: '', durationMs: 1, isAborted: false, turnId: 't1', reason: 'answer' } as const
const line = (event: string, phase: string, agent: string, decision: string) =>
  JSON.stringify({ ts: '2026-10-18T12:51:24Z', wf: WF, event, phase, agent, decision, details: { phase_id: 'P3' } }) + '\n'
const rows = (view: LoopView | undefined) =>
  Object.fromEntries((view?.live?.steps ?? []).map(s => [s.agent + '/' + s.phase, s.status]))

test('/cc10x-loop opens the pane and says so', async ($, on) => {
  // Nothing sits beneath the plugin: each hook here stands for the engine.
  const opens: string[] = []
  on('command.register', () => ({ value: { command: 'cc10x-loop' } }))
  on('ui.open', (_, e) => {
    opens.push(e.id)
    return { value: { isPlaced: true } }
  })
  on('session.start', (_, e) => ({ cwd: e.cwd }))

  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ran = await $.command.run({ command: 'cc10x-loop', args: '' })

  expect(opens).toEqual(['cc10x-loop'])
  expect(ran.text).toBe('cc10x loop pane opened.')
})

test('/cc10x-loop reports a pane the surface could not place', async ($, on) => {
  on('command.register', () => ({ value: { command: 'cc10x-loop' } }))
  on('ui.open', () => ({ value: { isPlaced: false, reason: 'too narrow' } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))

  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ran = await $.command.run({ command: 'cc10x-loop', args: '' })

  expect(ran.text).toBe('cc10x loop pane waiting: too narrow')
})

test('/cc10x-loop answers with the reason when the pane does not open', async ($, on) => {
  on('command.register', () => ({ value: { command: 'cc10x-loop' } }))
  on('ui.open', () => ({ deny: 'surface refused' }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))

  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })
  const ran = await $.command.run({ command: 'cc10x-loop', args: '' })

  expect(ran.text).toContain('did not open')
  expect(ran.text).toContain('surface refused')
})

test('a refused command.register is logged, not swallowed', async ($, on) => {
  const logs: string[] = []
  on('command.register', () => ({ deny: 'refused' }))
  on('ui.log', (_, e) => {
    logs.push(e.text)
    return { value: undefined }
  })
  on('session.start', (_, e) => ({ cwd: e.cwd }))

  await $.session.start({ cwd: '/repo', surface: 'terminal', isInteractive: true })

  expect(logs.some(line => line.includes('command.register failed'))).toBe(true)
  expect(logs.some(line => line.includes('refused'))).toBe(true)
})

test('band 1/6. the band names the live BUILD phase, on terminal and desktop', async ($, on) => {
  engine(on)
  answerFs(on, BUILD_MID_PHASE)
  await start($)

  for (const surface of ['terminal', 'desktop'] as const) {
    expect(await band($, surface)).toMatch(/^cc10x BUILD P3\/7 · next: code-reviewer/)
    expect(await band($, surface)).not.toMatch(/stale/)
  }
})

test('band 2/3/7. a reviewer spawn runs; the APPROVE line after it moves next on', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  await $.agent.spawn(reviewer)

  expect(await band($)).toMatch(/code-reviewer running 0m00s/)
  expect(state.spawns).toEqual([
    { agent: 'code-reviewer', atIndex: parseEvents(BUILD_MID_PHASE.eventsText).length, startedAt: NOW, phaseId: 'P3', wf: WF },
  ])

  // The router appends the reviewer's result with a Bash call; that call refreshes the loop.
  disk.fixture = { ...BUILD_MID_PHASE, eventsText: BUILD_MID_PHASE.eventsText + APPROVE }
  await $.tool.call({ tool: 'Bash', command: "printf '...' >> .cc10x/workflows/" + WF + '.events.jsonl' })

  const after = await band($)
  expect(after).toMatch(/next: /)
  expect(after).not.toMatch(/code-reviewer running/)
})

test('band 2b. a call that does not touch .cc10x/workflows/ does not refresh; turn.complete does', async ($, on) => {
  engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  disk.listing = 'empty'

  await $.tool.call({ tool: 'Bash', command: 'ls' })
  expect(await band($)).toMatch(/^cc10x BUILD/)

  await $.turn.complete({ answer: '', durationMs: 1, isAborted: false, turnId: 't1', reason: 'answer' })
  expect(await band($)).toBe('engine')
})

test('band spawn. a spawn outside any chain or before a live workflow never binds', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  disk.listing = 'missing'
  await start($)
  await $.agent.spawn(reviewer)
  await $.agent.spawn({ prompt: 'x', subagentType: 'general-purpose' })

  expect(state.spawns).toEqual([{ agent: 'code-reviewer', atIndex: 0, startedAt: NOW, phaseId: 'N/A', wf: '' }])
})

test('band wf. a spawn recorded against workflow A does not run a row of workflow B', async ($, on) => {
  engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  await $.agent.spawn(reviewer)
  expect(await band($)).toMatch(/code-reviewer running/)

  // Workflow B: the same artifact and log under another id (same cursor, same indices).
  const other = (text: string) => text.split('7e99ef54').join('0000beef')
  disk.fixture = {
    path: other(BUILD_MID_PHASE.path),
    artifactText: other(BUILD_MID_PHASE.artifactText),
    eventsText: other(BUILD_MID_PHASE.eventsText),
  }
  await $.turn.complete({ answer: '', durationMs: 1, isAborted: false, turnId: 't1', reason: 'answer' })

  const b = await band($)
  expect(b).toMatch(/^cc10x BUILD P3\/7 · next: code-reviewer/)
  expect(b).not.toMatch(/running/)
})

test('band 4. no workflow files: the band yields', async ($, on) => {
  engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  disk.listing = 'empty'
  await start($)

  expect(await band($)).toBe('engine')
})

test('band 4b. no .cc10x/workflows directory is the idle state, not an error', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  disk.listing = 'missing'
  await start($)

  expect(await band($)).toBe('engine')
  expect(state.loop).toEqual({ live: null, last: null, error: null })
})

test('band 4c. a read failure keeps the previous live workflow and records the error', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  disk.denyRead = true
  await $.turn.complete({ answer: '', durationMs: 1, isAborted: false, turnId: 't1', reason: 'answer' })

  const view = state.loop!
  expect(view.live?.wf).toBe(WF)
  expect(view.error).toContain('EACCES: read refused')
  expect(await band($)).toMatch(/^cc10x BUILD P3\/7.* · stale$/)
})

test('band 4d. an artifact that is not a JSON object is an error, never passed on', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)

  for (const artifactText of ['null', '[1]', '{"workflow_uuid": ']) {
    disk.fixture = { ...BUILD_MID_PHASE, artifactText }
    await $.turn.complete({ answer: '', durationMs: 1, isAborted: false, turnId: 't1', reason: 'answer' })
    const view = state.loop!
    expect(view.live?.wf).toBe(WF)
    expect(view.error).not.toBe(null)
  }
})

test('band 4e. a workflow_type naming an Object.prototype key draws with a warning, no throw', async ($, on) => {
  const logs: string[] = []
  const state = engine(on, logs)
  answerFs(on, { ...BUILD_MID_PHASE, artifactText: BUILD_MID_PHASE.artifactText.replace('"workflow_type": "BUILD"', '"workflow_type": "constructor"') })
  await start($)

  const view = state.loop!
  expect(view.error).toBe(null)
  expect(view.live?.warnings).toContain('unknown workflow type: constructor')
  expect(await band($)).toMatch(/^cc10x constructor P3\/7/)
  expect(logs).toEqual([])
})

test('band 4f. a finished workflow is no live band: the band yields and last names it', async ($, on) => {
  const state = engine(on)
  answerFs(on, FINISHED_BUILD)
  await start($)

  const view = state.loop!
  expect(view.live).toBe(null)
  expect(view.last?.wf).toBe(WF)
  expect(view.last?.finishedAt).toMatch(/^2026-10-/)
  expect(await band($)).toBe('engine')
})

test('band 5. a survey above the prompt: the band yields', async ($, on) => {
  engine(on)
  answerFs(on, BUILD_MID_PHASE)
  await start($)

  expect(await band($, 'terminal', true)).toBe('engine')
})

test('fix 1. parallel reviewer and hunter spawns: a slower, older scan never overwrites the newer view', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  // The hunter's first read is a little slow, so the reviewer's re-read starts with only the reviewer
  // recorded; that re-read is slower still and ends after the hunter's re-read saw both spawns.
  let reads = 0
  let held = false
  disk.hold = path => {
    if (path !== BUILD_MID_PHASE.path) return 0
    reads += 1
    if (reads === 2) return 20
    if (held || state.spawns?.length !== 1) return 0
    held = true
    return 60
  }
  await Promise.all([$.agent.spawn(reviewer), $.agent.spawn(hunter)])
  await new Promise(resolve => setTimeout(resolve, 100))

  expect(held).toBe(true)
  expect(rows(state.loop)).toMatchObject({ 'code-reviewer/build-review': 'running', 'failure-hunter/build-hunt': 'running' })
})

test('fix 2a. an artifact listed before its events log is live, with no error', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  disk.log = false
  await start($)

  expect(state.loop?.error).toBe(null)
  expect(state.loop?.live?.wf).toBe(WF)
  expect(state.loop?.live?.events).toEqual([])
})

const otherWf = (f: LoopFixture): LoopFixture => {
  const other = (text: string) => text.split('7e99ef54').join('0000beef')
  return { path: other(f.path), artifactText: other(f.artifactText), eventsText: other(f.eventsText) }
}

test('fix 2b. a corrupt older artifact behind a finished newer one: last set, error recorded, band yields', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, FINISHED_BUILD)
  disk.older = [{ ...otherWf(BUILD_MID_PHASE), artifactText: '{"workflow_uuid": ' }]
  await start($)

  expect(state.loop?.live).toBe(null)
  expect(state.loop?.last?.wf).toBe(WF)
  expect(state.loop?.error).toContain('wf-20261018T112922Z-0000beef.json')
  expect(await band($)).toBe('engine')
})

test('fix 2c. an orphan artifact (no log) behind a live workflow that just finished: the band yields', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  const orphan = otherWf(BUILD_MID_PHASE)
  disk.older = [orphan]
  disk.noLog = [orphan.path]
  await start($)
  expect(await band($)).toMatch(/^cc10x BUILD P3\/7/)

  disk.fixture = FINISHED_BUILD
  await $.turn.complete(turnDone)

  expect(state.loop?.live).toBe(null)
  expect(state.loop?.last?.wf).toBe(WF)
  expect(await band($)).toBe('engine')
})

test('fix 3. fs.list refused on an existing directory is an error, not idle', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  disk.listing = 'denied'
  await $.turn.complete(turnDone)

  expect(state.loop?.live?.wf).toBe(WF)
  expect(state.loop?.error).toContain('EACCES: list refused')
})

test('fix 4. a bare code-reviewer from another provider is not recorded', async ($, on) => {
  const state = engine(on)
  answerFs(on, BUILD_MID_PHASE)
  await start($)
  await $.agent.spawn(fromCc10x('code-reviewer', 'my-project'))

  expect(state.spawns).toBe(undefined)
})

test('fix 5. a boundary appended by an unfiltered call, then a spawn: the row runs', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  disk.fixture = { ...BUILD_MID_PHASE, eventsText: BUILD_MID_PHASE.eventsText + line('phase_started', 'build', 'router', 'start') }
  await $.tool.call({ tool: 'Bash', command: 'printf "$LINE" >> "$LOG"' })
  await $.agent.spawn(reviewer)

  expect(rows(state.loop)['code-reviewer/build-review']).toBe('running')
})

test('fix 6. a refused command.register still reads the loop at session start', async ($, on) => {
  const logs: string[] = []
  engine(on, logs, ['command.register'])
  answerFs(on, BUILD_MID_PHASE)
  await start($)

  expect(logs.some(l => l.includes('command.register failed') && l.includes('refused'))).toBe(true)
  expect(await band($)).toMatch(/^cc10x BUILD P3\/7/)
})

test('fix 7. a spawn another plugin refused is not recorded', async ($, on) => {
  const state = engine(on, [], ['agent.spawn'])
  answerFs(on, BUILD_MID_PHASE)
  await start($)
  await $.agent.spawn(reviewer)

  expect(state.spawns).toBe(undefined)
})

test('wave 8 / 1. a cc10x agent loaded with --plugin-dir (provider cc10x@inline) is recorded', async ($, on) => {
  const state = engine(on)
  answerFs(on, BUILD_MID_PHASE)
  await start($)
  await $.agent.spawn(fromCc10x('cc10x:code-reviewer', 'cc10x@inline'))

  expect(state.spawns?.map(s => s.agent)).toEqual(['code-reviewer'])
})

test('wave 8 / 2. parallel spawns after an unfiltered boundary: each records from its own read, both rows run', async ($, on) => {
  const state = engine(on)
  const disk = answerFs(on, BUILD_MID_PHASE)
  await start($)
  disk.fixture = { ...BUILD_MID_PHASE, eventsText: BUILD_MID_PHASE.eventsText + line('phase_started', 'build', 'router', 'start') }
  await $.tool.call({ tool: 'Bash', command: 'printf "$LINE" >> "$LOG"' })
  // Artifact reads from here: 1 the reviewer's first scan (fast, superseded by 2, so it never writes);
  // 2 the hunter's first scan (slow, superseded by 3); 3 the reviewer's re-read (slower, superseded by 4);
  // 4 the hunter's re-read writes. Neither first scan's view reaches the atom before its spawn records.
  let reads = 0
  disk.hold = path => {
    if (path !== BUILD_MID_PHASE.path) return 0
    reads += 1
    return reads === 2 ? 30 : reads === 3 ? 60 : 0
  }
  await Promise.all([$.agent.spawn(reviewer), $.agent.spawn(hunter)])

  expect(reads).toBe(4)
  expect(rows(state.loop)).toMatchObject({ 'code-reviewer/build-review': 'running', 'failure-hunter/build-hunt': 'running' })
})

test('wave 8 / 4. a core spawn that throws is logged as a spawn failure, not a record failure', async ($, on) => {
  const logs: string[] = []
  engine(on, logs, ['agent.spawn!'])
  answerFs(on, BUILD_MID_PHASE)
  await start($)
  await $.agent.spawn(reviewer).catch(() => undefined)

  expect(logs.some(l => l.startsWith('cc10x: spawn failed'))).toBe(true)
  expect(logs.some(l => l.includes('spawn record failed'))).toBe(false)
})
