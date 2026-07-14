# Market Research: What AI Developers Need From a Paid Agentic-Engineering Keynote

**Date:** 2026-07-13

**Purpose:** Ground Rom Iluz’s keynote and Auto-Pi proof-of-concept in the current concerns, language, and disagreements of AI developers and engineering leaders.

**Method:** First-party platform guidance and original talks establish technical facts; original Hacker News and Reddit posts establish *illustrative* community language. Social posts are not survey data and must not be presented as market prevalence.

## Executive conclusion

The market does **not** primarily need another talk announcing that agents write code. The credible version of this keynote must answer the harder question:

> **How do I get more agent autonomy without becoming the exhausted human workflow engine, QA department, and last line of defense?**

Across official guidance from Anthropic and OpenAI, original conference talks, and developer discussions, four durable needs recur:

1. **Context that remains usable over long work.** Agents need a legible repository, focused task context, durable progress artifacts, and a way to retrieve information just in time—not a giant prompt or an ever-growing memory dump.
2. **A defined operating loop, not a clever prompt.** Developers ask for plans, explicit definitions of done, role separation, feedback signals, and bounded recovery when the agent is wrong.
3. **Evidence before trust.** Tests, browser checks, logs, traces, review, and visible acceptance criteria are the desired proof. “The agent said it is done” is explicitly insufficient.
4. **Human attention moves up the stack; it does not disappear.** Product definition, architecture, safety, visual/E2E QA, and taste become more—not less—important. The keynote must name this trade-off honestly.

**The positioning opportunity:** Rom should not sell *harness* and *loop engineering* as new jargon. He should begin with the audience’s lived failure: *“I asked the agent to do the right thing. It declared victory. I opened the result and found the missing states, missing evidence, and weak QA.”* Then introduce the harness as the concrete answer: a system that makes correct work easier to continue and incomplete work harder to falsely call complete.

## Evidence hierarchy

| Tier | What it can support | Sources used |
| --- | --- | --- |
| **1 — First-party engineering guidance** | Claims about recommended agent architecture and documented failure modes | Anthropic engineering; OpenAI Codex engineering/docs |
| **2 — Original practitioner talks** | The speaker’s stated view of workflow changes and future skills | Andrew Ng at AI Dev 26; Birgitta Böckeler at QCon London |
| **3 — Original community discussions** | Vocabulary, frustration, and concrete examples of what individual developers report | Hacker News and r/ClaudeCode threads |
| **Not evidence** | Market-size claims, adoption rates, ROI, or universal developer sentiment | Search-result snippets, reposts, product marketing without an attributable study |

## What the market is actually trying to solve

### 1. The real problem is reliability across a workflow—not initial code generation

Anthropic describes long-running coding agents failing in two familiar ways: trying to do too much in one session and leaving undocumented partial work, or seeing partial progress later and prematurely declaring the job complete. Its recommended countermeasures are an initializer, a structured feature list, incremental work, durable progress notes, git history, and explicit end-to-end verification. [^anthropic-long-running]

OpenAI makes the complementary point: the engineer’s role shifts toward designing environments, specifying intent, and building feedback loops that let agents work reliably. In its Codex case study, OpenAI says progress was initially slow because the environment was underspecified—not because the model was incapable. [^openai-harness]

**Keynote implication:** The paid value is a practical mental model for designing an environment where an agent can *prove* progress. “Use agents harder” is not a model. “Specify → execute narrowly → observe → independently check → record the learning → continue or stop” is.

### 2. Context is an engineering surface, not a longer prompt

Anthropic explicitly frames context as finite and subject to diminishing returns (“context rot”). Its guidance is to curate the smallest high-signal set of information that can produce the desired behavior; use clear, non-overlapping tools; load references just in time; and use compaction, structured notes, and specialized subagents for long-horizon work. [^anthropic-context]

OpenAI’s Codex guidance maps this to a practical interface: give the agent a goal, relevant context, constraints, and a concrete “done when” condition. It recommends durable repository guidance (`AGENTS.md`), planning for complex work, tests/validation/review, and only adding tools that eliminate a real manual loop. [^openai-best-practices]

**Keynote implication:** “Prompt → context → harness → loop” can work as a memorable progression, but only after it is translated into ordinary developer artifacts: a task definition, scoped files, a test/acceptance contract, a progress record, and observable feedback.

### 3. The bottleneck has shifted—but it has not vanished

Andrew Ng’s original AI Dev 26 talk says coding agents enable fast assembly of building blocks, while product-definition work becomes a bottleneck. He also names compliance and marketing as constraints that can become slow relative to implementation. His proposed AI-engineer skill set combines coding-agent fluency, knowledge of modern AI building blocks, and basic product-management instincts. [^ng-talk]

A r/ClaudeCode author describes the same shift in plainer language: their role has become “Agent Orchestrator & Manual QA Tester.” They report that the hard part is visual, state-heavy E2E testing, where generated tests can be slow and brittle. [^reddit-final-boss]

**Keynote implication:** Do not promise “developers no longer code.” Say: **the scarce resource is moving from keystrokes to judgment, product clarity, and trustworthy verification.** This is a stronger and more honest reason to invest in an operating system for agents.

### 4. Developers want governance without becoming the governor of every step

One recent r/ClaudeCode author asks for a configurable workflow with “evidence, gates, and a dashboard.” Their stated failure is precise: the agent reports completion after 20 minutes, then the human sees missing states, skipped checks, weak QA, incomplete UX, and no evidence. They want phases, required outputs, human approval points, completion rules, and visible blocked gates—not another prompt. [^reddit-gates]

That post is **illustrative and potentially circular**: its requested product shape closely resembles the CC10x/keynote domain, and a single post cannot establish demand size. It is still useful as exact language for a failure the keynote can demonstrate rather than claim to have statistically measured.

**Keynote implication:** The audience will understand “evidence gate” only when they first see the painful alternative: a plausible-looking agent completion that fails a visible requirement. The demo should make the gate tangible.

## How AI developers speak about the problem

This is the audience vocabulary worth echoing—not as buzzwords, but as the wording around a concrete example.

| Market language | Where it appears | What it means for the talk |
| --- | --- | --- |
| “slow code,” “design partner,” “rubber ducking” | Hacker News workflow thread [^hn-workflow] | Experts do not necessarily want blind delegation; they want the agent to surface assumptions and edge cases. |
| “spec driven development,” “smaller subtasks,” “restart the session” | Hacker News workflow thread [^hn-workflow] | Long work needs recoverable artifacts, not one giant agent run. |
| “agent orchestrator,” “manual QA tester,” “final boss” | r/ClaudeCode E2E discussion [^reddit-final-boss] | The emotional cost is not merely bugs; it is being moved into a new, exhausting human bottleneck. |
| “missing states,” “missing evidence,” “skipped checks,” “what exactly counts as done” | r/ClaudeCode workflow-gates discussion [^reddit-gates] | This is the best language for the opening problem and the test the POC must pass. |
| “treat it as another potentially fallible team member” | Hacker News workflow discussion [^hn-workflow] | The audience responds to calibrated trust, not claims of magic or replacement. |
| “different models write the code vs review it” | Hacker News workflow discussion [^hn-workflow] | Independent review/anti-anchoring is intuitive when described as separation of duties. |

## Important contradictions to preserve, not smooth over

A credible keynote should make these tensions explicit. They are not errors in the research; they are the market’s real design constraints.

### Autonomy versus control

- OpenAI describes a high-throughput, Codex-first environment in which agents often drive review and merge, while human review is not always required. It also says this requires repository knowledge, architecture boundaries, agent-accessible observability, recurring cleanup, and recovery loops. [^openai-harness]
- Community participants still describe manual review, test suites, sandboxing, and uncertainty about whether they understand agent-generated systems well enough. [^hn-workflow]

**Resolution for the talk:** Autonomy is not a binary switch. It is earned per workflow by giving an agent a limited authority, clear signals, and a cheap way to detect/reverse bad work.

### More structure versus less ceremony

- Anthropic recommends explicit feature lists, incremental progress, progress artifacts, and E2E checks for long-running work. [^anthropic-long-running]
- OpenAI argues that at very high throughput, some conventional blocking merge gates can become counterproductive; correction can be cheaper than waiting in that specific operating environment. [^openai-harness]

**Resolution for the talk:** Do not prescribe one universal gate. Teach the decision rule: **increase the gate where the impact is high or a defect is hard to detect; shorten it where feedback is fast and rollback is cheap.**

### More context versus better context

- Developers commonly add instructions, memory, tools, and documentation to improve an agent.
- Anthropic warns that bloated context and overlapping tools create ambiguity and lost focus. [^anthropic-context]

**Resolution for the talk:** The asset is not “more memory.” It is *retrievable, scoped, current context plus a mechanism to discard stale detail.*

## What a paid keynote must deliver

A paid session should give the room three things that a free product update rarely does:

1. **Recognition:** articulate the failure better than attendees can (“the agent finished” is not the same event as “the task is complete”).
2. **A transferable model:** a four-part operating model attendees can apply Monday morning:
   - **Intent:** one outcome, constraints, and observable definition of done.
   - **Context:** the minimum current knowledge and tools needed for this task.
   - **Feedback:** tests, browser/user-flow checks, logs/traces, review, or product evidence the agent can inspect.
   - **Control:** bounded retries, a stop/escalation rule, and a durable record of what was learned.
3. **Believable proof:** a live or recorded trace in which the system encounters a real defect, fails the right gate, exposes the evidence, and either repairs it or stops safely. A happy-path terminal montage is not proof of an engineering system.

### Recommended proof sequence for the keynote

1. Start with an intentionally incomplete agent result: a feature that compiles or passes a narrow test but misses a real acceptance condition.
2. Show the condition in plain language before showing any architecture or vocabulary.
3. Run Auto-Pi/CC10x against it and make the audience see:
   - the scoped task and definition of done;
   - which context/tool is loaded and why;
   - the signal that rejects the false completion (test, browser check, review, log, or explicit human gate);
   - the bounded repair attempt or clean stop;
   - the artifact left for the next run/person.
4. Finish by showing the policy that will prevent that *class* of failure next time—not merely the patch that fixed today’s bug.

This order turns “harness” and “loop” into an observed causal mechanism rather than a vocabulary lesson.

## Auto-Pi positioning constraints

No public, attributable evidence for a Rom Iluz/agentic-engineering project named **Auto-Pi** was found in the web and GitHub discovery searches performed for this brief. That does **not** prove it is absent; it means external validation should not be implied.

Until Auto-Pi has reproducible public evidence, position it as:

- **A proof of mechanism:** “Here is the POC I built to make the loop visible.”
- **An experimental system:** show its boundaries and a failure case, rather than presenting it as a settled platform.
- **A teaching instrument:** its job in the talk is to let the audience inspect feedback, gates, recovery, and human escalation.

Do **not** position it as:

- proof that every agentic workflow is now reliable;
- a replacement for product judgment, UX/E2E validation, security review, or human accountability;
- a product with adoption, reliability, or productivity metrics unless the claim has a reproducible measurement and a source.

### Claim-discipline rules for the later word-by-word review

- Attribute external performance numbers to the original organization/person and state the operating context.
- Separate a **demonstrated POC trace** from a **general market claim**.
- Mark every numeric claim as one of: measured by Rom, measured by another party, illustrative, or unsupported.
- Replace universal claims (“agents do X,” “this solves Y”) with bounded claims that name the condition and evidence.

## Research limitations and next evidence to collect

- The Hacker News and Reddit threads provide language and examples, not representative sampling or adoption statistics.
- One YouTube workflow video could not be scraped through Bright Data due to a site-permission restriction. Two original talks were available through the video extractor and are included below.
- The research did not inspect a public Auto-Pi repository, live demo, test trace, or measurements because none was located from the supplied name. Before the keynote rewrite, capture one reproducible Auto-Pi run with raw inputs, artifacts, test/verification output, and a known failure/recovery path.
- The next phase should be the requested **word-by-word brutal review** of `keynote.html`, using this brief as the rubric. It should classify every sentence as: audience pain, supported claim, demonstration instruction, metaphor, unsupported assertion, or unsubstantiated metric.

## Source ledger

| Source | Evidence tier | Key use in this brief |
| --- | --- | --- |
| Anthropic, “[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)” (2025-09-29) | 1 | Finite context, context rot, high-signal context, just-in-time retrieval, structured notes, compaction, subagents. |
| Anthropic, “[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)” | 1 | Initializer/coding-agent split, incremental work, feature list, progress artifacts, premature completion, browser E2E verification. |
| OpenAI, “[Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)” (2026-02-11) | 1 | Engineer role shift, underspecified environments, feedback loops, agent legibility, observability, architecture, high-throughput trade-offs, entropy cleanup. |
| OpenAI, “[Codex best practices](https://developers.openai.com/codex/learn/best-practices)” | 1 | Goal/context/constraints/done-when prompt structure, durable repo guidance, planning, validation, skills, and bounded tool use. |
| Andrew Ng, “[The Future of Software Engineering](https://www.youtube.com/watch?v=g8um2AEf5ZA)” — AI Dev 26, San Francisco | 2 | Original speaker remarks on coding agents, product bottlenecks, rapidly changing building blocks, current documentation, and human skill development. |
| Birgitta Böckeler, “[State of Play: AI Coding Agents](https://www.youtube.com/watch?v=_R83pFpUWyM)” — QCon London | 2 | Original speaker framing of context, harness feedforward/feedback, structural checks, risk assessment, and steering. |
| Hacker News, “[Ask HN: What is your (AI) dev tech stack / workflow?](https://news.ycombinator.com/item?id=48413629)” | 3 | Original participant language about slow code, TDD, specs, review independence, sandboxing, and loss of comprehension. |
| Hacker News, “[Lessons for Agentic Coding: What should we do when code is cheap?](https://news.ycombinator.com/item?id=48019025)” | 3 | Original debate about output versus the non-coding constraints on product delivery. |
| r/ClaudeCode, “[Agentic coding is amazing... until you hit the final boss](https://www.reddit.com/r/ClaudeCode/comments/1r63p2q/agentic_coding_is_amazing_until_you_hit_the_final/)” | 3 | Original practitioner report on agent-orchestration, durable learning, manual QA, and state-heavy E2E pain. |
| r/ClaudeCode, “[Is there a tool that makes AI coding agents follow a configurable workflow with evidence, gates, and a dashboard?](https://www.reddit.com/r/ClaudeCode/comments/1u8udeb/is_there_a_tool_that_makes_ai_coding_agents/)” | 3 | Original statement of the evidence/gates/definition-of-done failure; treated as illustrative only and flagged as potentially circular. |

[^anthropic-context]: Anthropic, “Effective context engineering for AI agents,” 2025-09-29, <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
[^anthropic-long-running]: Anthropic, “Effective harnesses for long-running agents,” <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
[^openai-harness]: OpenAI, “Harness engineering: leveraging Codex in an agent-first world,” 2026-02-11, <https://openai.com/index/harness-engineering/>
[^openai-best-practices]: OpenAI, “Best practices — Codex,” <https://developers.openai.com/codex/learn/best-practices>
[^ng-talk]: Andrew Ng, “The Future of Software Engineering,” AI Dev 26, <https://www.youtube.com/watch?v=g8um2AEf5ZA>
[^reddit-final-boss]: r/ClaudeCode, “Agentic coding is amazing... until you hit the final boss,” <https://www.reddit.com/r/ClaudeCode/comments/1r63p2q/agentic_coding_is_amazing_until_you_hit_the_final/>
[^reddit-gates]: r/ClaudeCode, “Is there a tool that makes AI coding agents follow a configurable workflow with evidence, gates, and a dashboard?”, <https://www.reddit.com/r/ClaudeCode/comments/1u8udeb/is_there_a_tool_that_makes_ai_coding_agents/>
[^hn-workflow]: Hacker News, “Ask HN: What is your (AI) dev tech stack / workflow?”, <https://news.ycombinator.com/item?id=48413629>
