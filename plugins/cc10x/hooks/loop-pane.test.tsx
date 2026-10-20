import { expect, test } from 'claude-code/testing'

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
