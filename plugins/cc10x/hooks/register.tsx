import { atom } from 'claude-code'
import type { Register } from 'claude-code'

import type { LoopView, Spawn } from '../types'

const PANE = 'cc10x-loop'
const EMPTY: LoopView = { live: null, last: null, error: null }
// Filled from P3 on; declared here so the state keys exist from the first load.
export const loop = atom({ plugin: 'cc10x', key: 'loop' } as const, EMPTY)
export const spawns = atom({ plugin: 'cc10x', key: 'spawns' } as const, [] as Spawn[])

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: PANE,
      description: 'Show the cc10x workflow loop in a pane',
    })

    return next(e)
  }).catch(($, e, next) => {
    $.ui.log(`cc10x: command.register failed: ${next.error.message ?? next.error.kind}`)

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

  on('ui.render', { component: 'AbovePrompt' }, ($, e, next) => next(e)).catch(
    ($, e, next) => {
      $.ui.log(`cc10x: band render failed: ${next.error.message ?? next.error.kind}`)

      return next(e)
    },
  )

  on('ui.render', { component: 'Pane', requestId: PANE }, ($, e) => {
    const { Text } = $.ui.resolve(e)

    return <Text dimColor>no live workflow</Text>
  }).catch(($, e, next) => {
    $.ui.log(`cc10x: pane render failed: ${next.error.message ?? next.error.kind}`)

    return next(e)
  })
}
