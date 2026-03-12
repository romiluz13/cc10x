# Prompt Engineering Round 2: Head-to-Head Audit

Date: 2026-03-12

## Purpose

This round evaluates the strongest harnesses from the instruction layer outward.

The question is not:
- which repo has the most features
- which repo has the biggest framework
- which repo has the most markdown

The question is:

`Which instruction surfaces most reliably make Claude Code generate and maintain better code?`

This audit is the prompt/instruction counterpart to the orchestration round.

## Scope

This round is systematic, but it is not universal.

It covers the **highest-leverage instruction surfaces** in the core coding loop:
- entry instructions
- planning prompts
- execution prompts
- verification prompts
- review prompts
- gating/rubric prompts

It does **not** yet cover every long-tail command, every docs page, or every secondary prompt in every repo.

That means:
- this round is strong enough to rank the serious contenders on prompt engineering for the core loop
- it is not enough to claim “every single instruction in every repo has been fully audited”

## Repos And Surfaces Audited

### CC10X

Audited surfaces:
- `plugins/cc10x/skills/cc10x-router/SKILL.md`
- `plugins/cc10x/agents/planner.md`
- `plugins/cc10x/agents/component-builder.md`
- `plugins/cc10x/agents/integration-verifier.md`
- `plugins/cc10x/agents/bug-investigator.md`
- `plugins/cc10x/skills/plan-review-gate/SKILL.md`
- `plugins/cc10x/skills/verification-before-completion/SKILL.md`
- `plugins/cc10x/skills/debugging-patterns/SKILL.md`
- `plugins/cc10x/skills/frontend-patterns/SKILL.md`

### Metaswarm

Audited surfaces:
- `AGENTS.md`
- `skills/start/SKILL.md`
- `skills/orchestrated-execution/SKILL.md`
- `skills/plan-review-gate/SKILL.md`
- `rubrics/plan-review-rubric-adversarial.md`

### Get Shit Done

Audited surfaces:
- `agents/gsd-planner.md`
- `agents/gsd-executor.md`
- `agents/gsd-verifier.md`
- `agents/gsd-plan-checker.md`
- `commands/gsd/execute-phase.md`

### Babysitter

Audited surfaces:
- `CLAUDE.md`
- `plugins/babysitter-codex/SKILL.md`
- `plugins/babysitter-codex/AGENTS.md`
- `.claude/agents/code-reviewer.md`

### Superpowers

Audited surfaces:
- `skills/verification-before-completion/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/writing-skills/SKILL.md`

### Meta Reference

Audited surface:
- official `skill-creator` skill in Codex local system skills

This is not a harness peer. It is a meta-instruction reference for writing cleaner, more trigger-accurate skills.

## Audit Dimensions

Each repo was judged on these dimensions:

1. **Authority hierarchy**
   - Does the system clearly define what overrides what?
2. **Decision discipline**
   - Does it distinguish straightforward work from architecture or multi-option work?
3. **Planning sharpness**
   - Does the plan become a reliable execution contract?
4. **Execution guidance**
   - Does the executor know exactly how to proceed and when to stop?
5. **Verification rigor**
   - Does the wording prevent false completion and narrative bluffing?
6. **Adversarial review quality**
   - Are reviewers real auditors or just polite collaborators?
7. **Negative constraints**
   - Does the system clearly say what must never happen?
8. **Prompt-surface coherence**
   - Do prompts reinforce each other, or do they contradict each other?
9. **Maintainability of the prompt stack**
   - Is the instruction system likely to stay sharp under change?

## What I Learned

## 1. Metaswarm has the strongest adversarial prompt design

Metaswarm is still the best reviewed repo on adversarial plan language.

Why:
- its plan review gate is genuinely reviewer-shaped, not just a checklist
- its adversarial rubric is explicit about PASS/FAIL, evidence, and no-suggestions mode
- reviewer isolation is not implied; it is named and defended
- the system repeatedly distinguishes collaborative review from contract verification

What it does better than CC10X today:
- stronger audit voice
- better anti-anchoring language
- clearer independent-review semantics

What limits it:
- more of the system still depends on excellent English and social protocol than on one centralized product contract

## 2. Get Shit Done has the strongest execution-language stack

GSD’s real strength is not one prompt. It is the way planning, execution, verification, and plan-checking are written as one chain.

Why:
- `PLAN.md is the prompt` is one of the strongest execution ideas in the whole set
- the planner is unusually explicit about decision fidelity and deferred ideas
- the executor has strong deviation rules and checkpoint semantics
- the verifier and plan-checker both reason goal-backward, which is exactly the right abstraction

What it does better than CC10X today:
- richer executor instructions
- stronger plan-as-execution-artifact discipline
- better practical “what to do when reality differs from plan” language

What limits it:
- the prompt surface is very large
- the system depends on many markdown layers and workflow files
- that increases regression risk and makes the prompt stack harder to reason about globally

## 3. Superpowers has the sharpest anti-false-completion wording

Superpowers is not the strongest full harness here, but it is one of the strongest instruction systems on truthfulness and anti-rationalization.

Why:
- its verification skill is still one of the best single prompt surfaces in the set
- it says the quiet part out loud: skipping verification is lying
- it is unusually good at catching rationalization patterns
- `writing-skills` contains a very important discovery: bad descriptions cause models to obey the description instead of loading the real skill

That last point matters a lot.

It means:
- trigger descriptions are not metadata fluff
- bad summaries can destroy a good workflow
- description design is part of behavior design

CC10X should steal this insight aggressively.

## 4. Babysitter is stronger as process code than as English prompt design

Babysitter is extremely serious as a deterministic orchestration framework.
But in this round, the English instruction surfaces are not as strong as the best prompt-first competitors.

Why:
- much of babysitter’s real strength lives in symbolic process code, not prompt wording
- the user-facing instructions are solid, but they are less sharp than metaswarm/GSD/superpowers in the core code-quality loop
- the plugin-facing prompts are practical and operational, but not the strongest on code-generation behavior itself

This is not a criticism of the product.
It is a scope distinction:
- Babysitter wins more through process enforcement
- Metaswarm/GSD/Superpowers win more through prompt engineering

## 5. CC10X is now much sharper, but it still is not the strongest prompt stack

The recent CC10X changes materially improved the prompt layer:
- explicit `plan_mode`
- explicit `verification_rigor`
- clearer spec gate language
- harsher proof language in BUILD and VERIFY
- better separation between advisory skills and authoritative contracts

That matters.

CC10X is now clearly stronger than it was at the beginning of this session.

But it still does not beat the best reference on every important prompt dimension:
- metaswarm is still stronger on adversarial planning language
- GSD is still stronger on execution and goal-backward workflow phrasing
- superpowers is still stronger on anti-false-completion rhetoric

## 6. The official skill-creator reference adds a crucial meta-lesson

The most important meta-prompt insight from the official `skill-creator` plus `superpowers:writing-skills` is this:

`Descriptions and trigger metadata are part of the behavior contract.`

That means:
- a misleading description can override a great body
- a workflow summary in metadata can collapse a richer flow into a shortcut
- trigger accuracy and progressive disclosure are first-class prompt-engineering concerns

CC10X still has work to do here in some internal skills and top-level descriptions.

## Head-to-Head Ranking: Prompt Engineering

This ranking is only for the **instruction layer**, not for overall orchestration implementation.

### 1. Metaswarm

Why first:
- best adversarial planning language
- best independent reviewer framing
- best PASS/FAIL review contract

### 2. Get Shit Done

Why second:
- best execution-system language
- best planner/executor/verifier continuity
- strongest “plans are prompts” mindset

### 3. CC10X

Why third:
- now much stronger and more coherent than before
- strongest centralized trust direction among prompt-driven contenders
- still not as sharp as metaswarm on adversarial planning
- still not as rich as GSD on execution-language detail

### 4. Superpowers

Why fourth:
- elite anti-false-completion wording
- excellent skill-writing meta-lessons
- weaker than the top three as a complete end-to-end harness prompt system

### 5. Babysitter

Why fifth:
- English prompt surfaces are solid
- but its real edge is more in symbolic orchestration than in prompt sharpness

## Combined Competition Position

If I combine:
- the orchestration round
- this prompt-engineering round

the current honest combined ranking is:

1. `metaswarm`
2. `get-shit-done`
3. `CC10X`
4. `babysitter`
5. `superpowers`

That is the brutal ranking today.

## Can CC10X Win?

Yes.

## Is CC10X first place today?

No.

## Why not?

Because first place requires winning both layers together:
- orchestration trust
- prompt sharpness

CC10X is now very competitive on orchestration trust.
It is not yet the best prompt-engineering system in the set.

## What CC10X Must Still Steal

### From Metaswarm
- truly adversarial reviewer posture
- cleaner isolation language
- harder PASS/FAIL planning gates

### From Get Shit Done
- richer executor contracts
- stronger plan-as-prompt thinking
- better goal-backward plan and verification language

### From Superpowers
- stronger anti-rationalization language
- better trigger-description hygiene
- more explicit “this is lying, not done” phrasing where it matters

### From Babysitter
- keep symbolic state/replay confidence as a differentiator
- do not let prompt ambition weaken deterministic trust

## The Main Risk

The main risk for CC10X is not “too little structure.”

It is:

`prompt dilution`

That happens when:
- too many surfaces say similar things differently
- advisory skills start competing with contracts
- descriptions summarize too much and become shortcuts
- strong rules are surrounded by weaker, softer text

If CC10X wants first place, the next phase should be:
- prompt-by-prompt tightening
- reduction of redundant language
- better separation between trigger metadata, contract text, and reference guidance

## Honest Claim After This Round

After this round, I can honestly say:

- We now have a serious, systematic prompt-engineering comparison for the highest-leverage instruction surfaces in the strongest refs.
- We do **not** yet have a total audit of every meaningful line in every repo.
- CC10X is clearly in the top tier.
- CC10X is not yet the best prompt-engineering system in the set.

## Next Step

The next correct step is not another high-level ranking.

It is a repo-local rewrite program:

1. reduce redundant prompt wording
2. harden descriptions and trigger metadata
3. sharpen adversarial review language
4. strengthen execution instructions with more explicit stop conditions
5. keep advisory skills from competing with authoritative contracts

That is the work that can move CC10X from top-tier to first place.

## Coverage Ledger

This round is systematic for the core coding loop, but it is not a total repo-wide word audit.

Covered well enough to rank:
- entry instructions
- planning prompts
- execution prompts
- verification prompts
- review prompts
- gating and rubric prompts

Not yet covered exhaustively:
- every secondary command prompt
- every template installed into user repos
- every hook message in every competitor
- every long-tail skill in large repos
- every cross-file wording conflict outside the core loop

So the correct claim after this round is:
- the head-to-head prompt-engineering comparison is strong for the highest-leverage instruction surfaces
- it is not yet exhaustive for every meaningful line in every repo

## Proven Vs Unproven

### Proven enough to act on

- `metaswarm` is stronger than CC10X on adversarial planning language
- `get-shit-done` is stronger than CC10X on execution-language continuity
- `superpowers` is stronger than CC10X on anti-false-completion wording
- CC10X is now in the top tier on prompt engineering

### Still unproven

- that CC10X is the strongest prompt system overall
- that no hidden long-tail prompt surface in another repo is better
- that every instruction conflict in CC10X has already been found
