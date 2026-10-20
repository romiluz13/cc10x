import { atom, read, update } from 'claude-code'
import type { CoreEngineInterface, Register } from 'claude-code'

import type { LoopView, Spawn } from '../types'
import { REMEDIATION, ROUTES } from './loop-routes'
import { bandLine, deriveLoop, isFinished, parseEvents, workflowOf, type Artifact } from './loop-state'

const PANE = 'cc10x-loop'
const WORKFLOWS = '.cc10x/workflows'
const EMPTY: LoopView = { live: null, last: null, error: null }
export const loop = atom({ plugin: 'cc10x', key: 'loop' } as const, EMPTY)
export const spawns = atom({ plugin: 'cc10x', key: 'spawns' } as const, [] as Spawn[])

// Every agent some chain dispatches (the router is no spawn).
const AGENTS = new Set(
  [...Object.values(ROUTES), ...Object.values(REMEDIATION)]
    .flat()
    .map(row => row.agent)
    .filter(agent => agent !== 'router'),
)
// The engine resolves a plugin agent's type to `<pluginName>:<agent>`; `provider.plugin` is the
// plugin id (`cc10x@cc10x`, `cc10x@inline`), so the type, not the provider, names a cc10x agent.
const SPAWNED = /^cc10x:([a-z-]+)$/

type Api = Pick<CoreEngineInterface, 'session' | 'fs' | 'state'>

// The newest not-finished workflow under .cc10x/workflows, newest artifact first (at most 20).
// A bad artifact is skipped and named in `error`; when it is the one shown, the shown view stays.
async function scan($: Api, previous: LoopView): Promise<LoopView> {
  const dir = (await $.session.root()) + '/' + WORKFLOWS
  // No workflows directory: nothing has run here, which is idle, not an error. Any other list failure throws.
  if (!(await $.fs.exists(dir))) return EMPTY
  const entries = await $.fs.list(dir)
  const names = new Set(entries.map(f => f.name))
  const artifacts = entries
    .filter(f => f.kind === 'file' && /^wf-.*\.json$/.test(f.name))
    .sort((a, b) => b.mtimeMs - a.mtimeMs)
    .slice(0, 20)
  const recorded = await read($, spawns)
  const errors: string[] = []
  let last: LoopView['last'] = null
  for (const [i, file] of artifacts.entries()) {
    const path = dir + '/' + file.name
    const log = file.name.replace(/\.json$/, '.events.jsonl')
    // The router writes the artifact before its log: a log not there yet is no events on the newest
    // artifact; an older artifact without one is an abandoned orphan, never live.
    if (i > 0 && !names.has(log)) continue
    try {
      const raw: unknown = JSON.parse(await $.fs.read(path))
      if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) throw new Error(path + ' is not a JSON object')
      const artifact = raw as Artifact
      const events = names.has(log) ? parseEvents(await $.fs.read(dir + '/' + log)) : []
      if (isFinished(artifact, events)) {
        last ??= { wf: workflowOf(artifact), finishedAt: events[events.length - 1]?.ts ?? '' }
        continue
      }
      // shortcut: otherLive stays 0 because the scan stops at the first live workflow; count the rest if the pane needs it.
      const live = deriveLoop({ path, artifact, events, spawns: recorded, otherLive: 0, warnings: [] })
      return { live, last, error: errors.join('; ') || null }
    } catch (err) {
      const message = path + ': ' + (err instanceof Error ? err.message : String(err))
      if (previous.live?.path === path) return { live: previous.live, last, error: [...errors, message].join('; ') }
      errors.push(message)
    }
  }
  return { live: null, last, error: errors.join('; ') || null }
}

// Hooks of parallel calls run concurrently: only the latest-started read writes its view.
let seq = 0

// Re-reads the live workflow into the loop atom and returns the view it read, written or not.
// A failure keeps the previous view and records why.
async function readLoop($: Api): Promise<LoopView> {
  const gen = ++seq
  const previous = await read($, loop)
  let view: LoopView
  try {
    view = await scan($, previous)
  } catch (err) {
    view = { ...previous, error: err instanceof Error ? err.message : String(err) }
  }
  if (gen === seq) await update($, loop, () => view)
  return view
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    try {
      await $.command.register({
        name: PANE,
        description: 'Show the cc10x workflow loop in a pane',
      })
    } catch (err) {
      $.ui.log(`cc10x: command.register failed: ${err instanceof Error ? err.message : String(err)}`)
    }

    const started = await next(e)
    await readLoop($)

    return started
  }).catch(($, e, next) => {
    $.ui.log(`cc10x: loop read failed: ${next.error.message ?? next.error.kind}`)

    return next(e)
  })

  // The router writes its artifact and events log with Edit, Write or Bash: re-read after such a call.
  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    const target = e.tool === 'Bash' ? e.command : e.tool === 'Edit' || e.tool === 'Write' ? e.file_path : ''
    if (target.includes(WORKFLOWS + '/')) await readLoop($)

    return ran
  }).catch(($, e, next) => {
    $.ui.log(`cc10x: loop refresh failed: ${next.error.message ?? next.error.kind}`)

    return next(e)
  })

  // Records a started cc10x chain agent against the live workflow as it stands now, then re-reads so the row runs.
  on('agent.spawn', async ($, e, next) => {
    const started = await next(e)
    const agent = SPAWNED.exec(e.subagentType)?.[1]
    if (started.deny === undefined && agent !== undefined && AGENTS.has(agent)) {
      // A router write the tool.call filter missed may have moved the boundary: read before recording,
      // and record from this read even when a parallel spawn's newer read superseded its write.
      const { live } = await readLoop($)
      const spawn: Spawn = {
        agent,
        atIndex: live?.events.length ?? 0,
        startedAt: await $.clock.now(),
        phaseId: live?.cursor ?? 'N/A',
        wf: live?.wf ?? '',
      }
      await update($, spawns, list => [...list, spawn].slice(-50))
      await readLoop($)
    }

    return started
  }).catch(async ($, e, next) => {
    // `next.called` is always true here (the hook calls next first): the replay tells whether the spawn itself failed.
    const replay = next(e)
    const spawned = await replay.then(() => true, () => false)
    $.ui.log(`cc10x: ${spawned ? 'spawn record failed' : 'spawn failed'}: ${next.error.message ?? next.error.kind}`)

    return replay
  })

  on('turn.complete', async ($, e, next) => {
    const done = await next(e)
    await readLoop($)

    return done
  }).catch(($, e, next) => {
    $.ui.log(`cc10x: loop refresh failed: ${next.error.message ?? next.error.kind}`)

    return next(e)
  })

  on('command.run', { command: PANE }, async $ => {
    const opened = await $.ui.open({ id: PANE, title: 'cc10x loop' })

    return {
      text: opened.isPlaced
        ? 'cc10x loop pane opened.'
        : `cc10x loop pane waiting: ${opened.reason}`,
    }
  }).catch(($, e, next) => ({
    // A registered command has no engine core: answer here, or the user sees
    // the engine's "no command.run hook answered it" hint instead of the reason.
    text: `cc10x loop pane did not open: ${next.error.message ?? next.error.kind}`,
  }))

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const { live, error } = await read($, loop)
    if (e.props.hasSurvey || live === null) return next(e)
    const { Text } = $.ui.resolve(e)
    // A failed re-read keeps the old view: say so, or the band reads as current.
    const stale = error === null ? '' : ' · stale'

    return <Text dimColor>{bandLine(live, await $.clock.now()) + stale}</Text>
  }).catch(($, e, next) => {
    $.ui.log(`cc10x: band render failed: ${next.error.message ?? next.error.kind}`)

    return next(e)
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, ($, e) => {
    const { Text } = $.ui.resolve(e)

    return <Text dimColor>no live workflow</Text>
  }).catch(($, e, next) => {
    $.ui.log(`cc10x: pane render failed: ${next.error.message ?? next.error.kind}`)

    return next(e)
  })
}
