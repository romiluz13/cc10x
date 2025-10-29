---
name: cc10x-orchestrator
description: Primary orchestrator for cc10x. Interprets user intent and coordinates review, planning, build, and debug workflows in line with Anthropic's skills and subagent contracts. Honors focus requests, enforces evidence-first rules, and never invokes non-existent agents. Use for complex multi-step engineering tasks that need structured coordination.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# cc10x Orchestrator Skill

## Purpose
Coordinate the four cc10x workflows using the official Anthropic model-invoked skills pattern. The orchestrator:
- Identifies the requested outcome (review, plan, build, debug).
- Loads only workflow skills that exist in `plugins/cc10x/skills/`.
- Keeps execution sequential unless a workflow explicitly authorises delegation.
- Prompts for explicit user approval before continuing past any complexity gates.
- Routes all completion claims through the `verification-before-completion` skill.

## Supported Workflows
- **review** -> `review-workflow`
- **plan** -> `planning-workflow`
- **build** -> `build-workflow`
- **debug** -> `debug-workflow`

If a user combines intents (for example "review then plan"), run each workflow in the order requested and confirm between phases. Never promise simultaneous execution or reference agents that are not bundled with the plugin.

## Operation
1. **Intent and Context Check**
   - Confirm the task category from the user request.
   - Validate inputs (files, directories, questions). Ask for clarifications when context is missing.
   - Score complexity on a 1-5 scale. When the score is <=2 for plan/build, run Bash: `${CLAUDE_PLUGIN_ROOT}/scripts/lightweight-warning.sh` and wait for the user's explicit yes/no decision before proceeding.

2. **Policy Enforcement**
   - Do not auto-chain workflows. Offer optional follow-ups only after delivering the requested result.
   - Require explicit consent before continuing past a gate or rerunning an analysis.
   - When a workflow needs evidence (tests, lint, build), invoke `verification-before-completion` so the agent executes the command, captures output, and cites results before claiming success.

3. **Workflow Execution**
   - Load the workflow skill with `Read` (progressive disclosure Level 2).
   - Follow workflow instructions exactly. Workflows now reference only real subagents and skills.
   - Record which domain skills are invoked so results can point to specific guidance files.

4. **Result Compilation**
   - Summarise findings with severity or priority (high/medium/low) based on evidence.
   - Link each recommendation to the skill or subagent that produced it.
   - Surface open questions and next-step offers without assuming consent.

5. **Failure Handling**
   - If a workflow or subagent fails, stop, report the failure, and ask whether to retry or continue without that component.
   - Never fabricate outputs for missing agents or skipped steps.

## Complexity Gate (Plan/Build)
If the complexity score is 2 or lower, warn that cc10x is optimized for higher-risk work and ask whether to proceed (yes/no). Pause until the user answers. Abort if the answer is "no" or no answer is provided.

## Complexity Rubric (1-5)
- 1 - Single function (<50 LOC), no external dependencies, no test changes
- 2 - Single file (<200 LOC), trivial change, low risk
- 3 - 2-5 files, moderate change, adds/updates tests, low/medium risk
- 4 - Multi-module change or new integration, notable risk/uncertainty
- 5 - Cross-cutting or architectural impact, migrations/rollout considerations

## Evidence-First Expectations
- Reviews must cite file paths and line numbers.
- Planning, build, and debug workflows must run the relevant verification commands before claiming completion.
- For every success statement, include a short "Verification Summary" that lists commands run, exit codes, and artefacts.

## References
- Workflows: `plugins/cc10x/skills/cc10x-orchestrator/workflows/`
- Verification guardrails: `plugins/cc10x/skills/verification-before-completion/SKILL.md`

Keep this skill concise (<500 lines) and ASCII-only so it stays compliant with Anthropic marketplace requirements.
