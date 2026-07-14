# Harness Engineering and Loop Engineering

**Purpose.** Keynote briefing for senior developers. This is a vocabulary and production-pattern guide, not a product comparison. It uses seven sources: official OpenAI, Anthropic, and LangChain material, one official OpenAI source repository, and one original talk identified below as speaker opinion. These labels are emerging rather than settled standards—LangChain explicitly says the framework/runtime/harness boundaries remain blurry [5].

## Definitions

**Harness engineering** is the engineering of the controllable system around a model that lets it do a particular job safely and repeatably: it supplies task-relevant context, tools and an execution environment; maintains state; applies deterministic policy and approvals; observes results; and decides what happens next. In LangChain’s concise formulation, *agent = model + harness*; the harness is the scaffolding that connects the model to the real world [6]. OpenAI describes the associated work as designing environments, specifications, and feedback loops rather than merely asking for a better answer [1].

**Loop engineering** is the narrower practice of designing the repeated control cycle: choose the next bounded unit of work, run an agent, inspect evidence, persist a handoff, then either continue, retry differently, stop, or escalate. A loop is normally **inside** a harness; it is not synonymous with the entire harness. Anthropic’s long-running example uses an initializer followed by coding sessions that each select one feature, validate it, commit progress, and leave structured state for the next session [3].

Neither term names a universal architecture or proves a market trend. They are useful names for a design focus: make the agent’s *environment and feedback* as deliberately engineered as its prompt.

## Boundaries: related terms, without conflation

| Term | Owns | Is not |
| --- | --- | --- |
| **Harness** | The operating envelope for an agent: context, tools, state, policies, observation, and control decisions. | Just a system prompt, a model, or a tool list. |
| **Workflow** | The intended business/development process and its stages (for example: intake → implement → review → release). | Necessarily an agentic or repeated process. A conventional workflow can call a harness at one stage. |
| **Loop** | Repetition and termination: the unit of work, evidence required to advance, retry/recovery, budget, and escalation. | The whole workflow or a guarantee of progress. |
| **Skill** | A reusable, task-specific procedure/instruction bundle, often paired with tools and checks. | The control plane; a skill does not itself decide global scheduling, budgets, or approvals. |
| **Sub-agent** | A delegated model run with a narrow role or fresh context (for example, planner, generator, evaluator). | A required component. Anthropic’s two prompts may be called separate agents even when the system prompt, tools, and harness are otherwise the same [3]. |
| **Memory** | Information that survives or is retrieved across turns/runs: repository artifacts, session state, or a durable store. | The current context window. The harness chooses what to retrieve, write, compact, or hand off. |
| **Router** | Selection and dispatch: which workflow, skill, model, or agent role receives an item. | The agent’s reasoning or the loop itself. It is one possible harness control-plane module. |

### What it looks like in production

A useful **conceptual** shape—not a prescribed architecture—is:

```text
request/event → router/workflow selection → harness policy + task context
                                      ↓
                         bounded agent/tool loop ↔ sandbox, services, repository
                                      ↓
                   validation/observability → persist handoff → repeat | escalate | stop
```

The important engineering artifacts are often ordinary software artifacts: explicit task/feature lists, version control, scripts that recreate the environment, tool outputs, test evidence, durable state, CI checks, traces, and approval records. Anthropic’s example uses a feature list, progress log, `init.sh`, git history, and end-to-end browser checks [3]. OpenAI describes worktree-local app instances plus browser, logs, metrics, and traces exposed to the agent [1].

**Local production example — CC10x only.** This repository’s `cc10x-router` is a concrete local implementation of the router/workflow slice: it routes PLAN/REVIEW/ORIENT/BUILD intent, specifies durable workflow artifacts under `.cc10x/workflows/`, and names gates for plan trust, phase exit, failures, and memory synchronization (`plugins/cc10x/skills/cc10x-router/SKILL.md`). It illustrates an explicit controller around agent work; it is not evidence that all harnesses need that routing model, nor a claim about performance. No Auto-Pi material was inspected or required.

## Five production patterns worth recognizing

1. **Session handoff plus incremental completion.** An initializer converts a broad request into a structured, initially failing feature list and working environment. Later runs read progress and git history, verify a baseline, complete one feature, then commit and record the next handoff. This directly addresses fresh-context and premature-completion failures [3].
2. **Make the target system legible to the agent.** Give the harness isolated execution plus the same evidence a developer would use: browser automation for UI behavior and queryable logs, metrics, and traces. OpenAI reports doing this per worktree so an agent can reproduce and validate a change against its own instance [1].
3. **Separate production from evaluation.** For difficult, long-running creation, a planner can decompose, a generator can build, and an evaluator can grade against explicit criteria before another iteration. Anthropic presents this as one three-agent harness design, not as a universal requirement [4].
4. **Put deterministic controls at loop seams.** Middleware/hooks can enforce policies, human approval, PII handling, retries, fallbacks, call limits, and observability before or after model/tool calls. Such controls belong in executable logic rather than relying solely on a prompt [6].
5. **Treat repository knowledge and invariants as executable infrastructure.** OpenAI’s case uses a compact map into versioned documentation, structural tests/linters, and recurring cleanup tasks. The point is to make constraints discoverable and mechanically checkable for later runs—not to encode every rule in one giant instruction file [1].

These patterns can be built with custom code or frameworks. LangChain’s distinction is helpful here: a framework provides abstractions, a runtime supplies production concerns such as durable execution and persistence, and a harness is a more opinionated, task-ready assembly. The author also cautions that these categories overlap [5]. OpenAI’s open-source Agents SDK is an example of reusable primitives—agents, handoffs, guardrails, sessions, tracing, and a Runner—rather than a mandate for a particular application architecture [2].

## Five concrete things attendees can build

1. **An issue-to-validated-fix lane.** Route a bug report to an isolated worktree; make the agent reproduce it, implement the smallest change, run unit and browser/API checks, attach evidence, and open a reviewable change. Escalate when the evidence is ambiguous.
2. **A multi-session feature builder.** Turn an approved feature specification into an immutable-or-controlled checklist, initialize the repo and test path once, then have each run deliver one verifiable slice with a commit and structured handoff [3].
3. **An approval-gated operations assistant.** Let a model gather context and draft an action, while deterministic middleware redacts/enforces policy, limits calls, records trace data, and pauses before consequential actions for a human decision [6].
4. **A planner–maker–reviewer quality loop.** Give each role a bounded artifact and acceptance criteria: a planner produces tasks, a maker changes the target, and an evaluator validates behavior and reports defects for the next bounded iteration [4].
5. **A repository legibility and maintenance loop.** Periodically inspect documentation links, architectural dependency rules, test health, or style invariants; file narrowly scoped remediation work with machine-checkable evidence. OpenAI’s described doc-gardening and structural checks show the shape of this pattern [1].

Start with one task type whose success can be checked independently. Define the stop condition, action permissions, cost/time budget, evidence required to advance, and human escalation path before increasing autonomy.

## Common failure modes and design responses

- **One-shotting a long task.** The model exhausts context mid-change and the next run guesses what happened. Use small increments, explicit handoff artifacts, a clean-state requirement, and version control [3].
- **False completion.** The agent sees partial progress or passing unit checks and declares victory. Keep a structured acceptance list; only change a completion state after the prescribed end-to-end evidence [3].
- **Invisible reality.** Code-only reasoning misses UI, runtime, or operational failures. Supply safe browser/API probes and relevant logs, metrics, and traces; recognize their limitations rather than treating them as perfect oracles [1][3].
- **Prompt-only governance.** A prompt may be ignored or become stale. Put non-negotiable policies, limits, retries, and approval gates in deterministic code at model/tool boundaries [6].
- **Context overload and stale instructions.** A monolithic manual crowds out the task and drifts. Use a small entry map, progressive disclosure, versioned source-of-truth artifacts, and checks for freshness [1].
- **Pattern replication and accumulated entropy.** Agents reuse existing weak patterns at high volume. Encode architectural/taste invariants mechanically and run bounded cleanup; do not infer that a model will self-correct without feedback [1].
- **Unbounded iteration.** A loop can retry expensively without gaining evidence. Set step/call/time budgets and make “escalate/stop” a first-class outcome; LangChain lists call limits and retry/fallback controls as harness concerns [6].

## Original-talk note: speaker opinion, not evidence

In the original **Boris Cherny, “Claude Code & the Future of Engineering”** YouTube talk, the speaker characterizes loops as “the simplest thing that works” and says he believes they are the future; he also offers the view that harness importance may diminish as models improve [7]. That is a practitioner’s opinion. It does **not** establish a universal architecture, adoption rate, or performance result.

## Source ledger (seven sources)

1. **OpenAI — “Harness engineering: leveraging Codex in an agent-first world.”** <https://openai.com/index/harness-engineering/> — Primary production account for feedback loops, legibility, repository artifacts, mechanical invariants, and stated limits of generalization.
2. **OpenAI — `openai/openai-agents-python` repository.** <https://github.com/openai/openai-agents-python> — Original source repository inspected for the SDK’s agent/runner, handoff, guardrail, session, tracing, and sandbox-boundary materials.
3. **Anthropic — “Effective harnesses for long-running agents.”** <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents> — Primary long-horizon harness example and its failure modes, artifacts, and validation practices.
4. **Anthropic — “Harness design for long-running application development.”** <https://www.anthropic.com/engineering/harness-design-long-running-apps> — Primary example of planner/generator/evaluator, structured handoffs, and context resets.
5. **LangChain — “Agent Frameworks, Runtimes, and Harnesses—oh my!”** <https://www.langchain.com/blog/agent-frameworks-runtimes-and-harnesses-oh-my> — First-party, explicitly qualified vocabulary for framework/runtime/harness boundaries.
6. **LangChain — “How to Build a Custom Agent Harness.”** <https://www.langchain.com/blog/how-to-build-a-custom-agent-harness> — First-party explanation of the agent loop, context-delivery role, middleware, policies, retries, limits, and human-in-the-loop controls.
7. **Boris Cherny / Acquired — “Claude Code & the Future of Engineering.”** <https://www.youtube.com/watch?v=SlGRN8jh2RI> — Original YouTube talk; retained only for the clearly labeled speaker-opinion note above.

## Scope and evidence limits

The OpenAI and Anthropic articles are reports of their own systems and experiments, not independent benchmarks. Their stated experiences and figures are not generalized here. This brief makes no claim about universal architecture, market adoption, reliability, cost, or performance beyond what the cited source explicitly reports.
