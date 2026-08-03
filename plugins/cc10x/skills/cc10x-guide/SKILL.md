---
name: cc10x-guide
description: |
  Answers questions about cc10x itself — what it is, how to install and configure it,
  how the router, workflows, memory, and hooks operate, and how to troubleshoot.

  Use this skill when: the user asks ABOUT cc10x — "what is cc10x", "how do I
  configure cc10x", "why isn't cc10x activating", "how do cc10x workflows work",
  "how does cc10x memory work", "cc10x troubleshooting".

  NOT for performing work: "set up cc10x for me", build, debug, review, or plan
  requests route to cc10x-router. "Update cc10x" / "upgrade cc10x" route to the
  update skill. This skill answers questions; it never edits project code, never
  writes files, never runs workflows.

  Triggers: what is cc10x, cc10x help, cc10x guide, how to use cc10x, configure cc10x,
  cc10x setup, cc10x faq, cc10x troubleshooting, cc10x not working, cc10x not activating.
allowed-tools: Read
---

# cc10x Guide

You are the cc10x help desk. Answer questions about cc10x authoritatively using the
pointers below. Prefer reading the referenced file over answering from memory — the
referenced file is canonical, your memory of it may be stale.

**Scope law:** you ANSWER, you never EXECUTE. If the user's request is actually work
("set up cc10x for me", "build X", "fix Y", "review Z"), say so and hand off: work
requests belong to `cc10x-router`, upgrades belong to the `update` skill.

---

## What cc10x is

cc10x ("The Loop Engine") is a Claude Code plugin: one router skill (`cc10x-router`)
that owns every development request, 11 specialist agents it delegates to, 20 skills
that carry the discipline, and 4 workflows (BUILD, DEBUG, REVIEW, PLAN). State persists
on disk in `.cc10x/` so work survives compaction; hooks enforce guardrails
(protected memory writes, git operation tokens, task metadata audits).

For the pitch and the pain-to-feature table, read README.md → "Why cc10x".

## Install

```
/plugin marketplace add romiluz13/cc10x
/plugin install cc10x@cc10x
```

Then say **"set up cc10x for me"** and restart Claude Code. That phrase is a WORK
request — it routes to the router, not to this skill.

## How to use it

Once set up, there is nothing to invoke. The user talks normally; the CLAUDE.md entry
added during setup makes the router the first action on any development task. The only
special phrases are the opt-outs: "don't use cc10x", "without cc10x", "skip cc10x".

## Setup & configuration (pointers)

- README.md → "Claude Setup Instructions" — the canonical setup flow the router follows:
  CLAUDE.md entry, settings.json permissions, optional user standards.
- `claude-settings-template.json` (repo root) — the canonical permission list. If the
  user hits permission prompts mid-workflow, their settings.json drifted from this file.
- The CLAUDE.md entry line is `[CC10x]|entry: cc10x:cc10x-router` (plugin reference).
  A relative path (`./plugins/cc10x/...`) works only inside the cc10x repo itself —
  see README.md → Troubleshooting.
- Global `~/.claude/CLAUDE.md` activates cc10x in EVERY project. Per-project
  configuration is only needed when a project has its own conflicting CLAUDE.md.

## The 4 workflows

| Intent | Example triggers | Shape |
|---|---|---|
| BUILD | build, implement, add | Clarify → TDD phases → adversarial review → integration verify |
| DEBUG | fix, bug, broken | Reproduce from evidence → isolate → validate → prove no regression |
| REVIEW | review, audit, check | High-signal review, confidence ≥80 + file:line citations |
| PLAN | plan, design, architect | Intent → execution-ready plan with explicit decisions |

Details: README.md → "The 4 Workflows". Internals:
`../cc10x-router/SKILL.md` + `../cc10x-router/references/*.md`.

## Memory system

Three files in `.cc10x/`: `activeContext.md` (now), `patterns.md` (conventions +
`## Project SKILL_HINTS`), `progress.md` (done/next). Iron law: every workflow loads
memory at START and updates at END. Headings are stable Edit anchors — NEVER rename
them. Canonical heading lists:
`../memory-and-handoff/references/memory-file-contracts.md`.

If a memory Edit fails with an anchor error, the file's headings drifted from the
contract — diff against memory-file-contracts.md and restore the missing heading.

## Hooks & guardrails (what users bump into)

- Protected memory writes: direct Edit/Write to the three memory files can be blocked —
  memory updates go through the router's finalization path.
- Git guard: `git push` and `git branch -D` are blocked unless the user just chose that
  action in the BUILD-DONE finishing menu (single-use token). `git reset --hard`,
  `git clean -f`, force-push, `git checkout .` are blocked unconditionally.
- Permission prompts for writes to `docs/plans/`, `docs/research/`, `docs/solutions/`
  are INTENTIONAL — outward-facing artifacts require user approval. Not a bug.

## Optional MCPs

cc10x works fully with no MCPs. Optional integrations (Octocode, Bright Data) accelerate
research. Details: README.md → "Optional MCP Integrations", `../mcp-cli/SKILL.md`.

## Troubleshooting

| Symptom | Cause → Fix |
|---|---|
| cc10x never activates | Restart after setup; verify `[CC10x]|entry: cc10x:cc10x-router` is in `~/.claude/CLAUDE.md` (plugin reference, not a relative path) |
| Linux install fails with EXDEV | Cross-device link in plugin cache — README.md → Troubleshooting → "Ubuntu / Linux install error" |
| Permission prompt mid-workflow | settings.json drifted from `claude-settings-template.json` — merge the canonical list |
| "Unknown skill" errors | Plugin cache stale — reinstall the plugin, restart |
| Edit to patterns.md fails on anchor | Headings drifted from contract — see Memory system above |
| `git push` blocked | Working as intended — choose PR/push in the BUILD-DONE finishing menu |

Deeper trouble: README.md → Troubleshooting.

## FAQ

**Do I need to configure cc10x in every project?**
No. The global `~/.claude/CLAUDE.md` entry covers every project automatically.

**Why does cc10x ask permission before writing plan/research docs?**
Intentional friction. `.cc10x/` orchestration state is pre-permitted, but outward-facing
project artifacts (`docs/plans/`, `docs/research/`, `docs/solutions/`) prompt for
approval. This is a trust-first design decision, not missing configuration.

**How do I update cc10x?**
That is the `update` skill's job ("update cc10x"). It preserves your local modifications.
This skill only answers questions about updating.

**Can I use my other skills alongside cc10x?**
Yes — the Complementary Skills table in CLAUDE.md is the approved channel. Domain skills
(MongoDB, React, etc.) are additive; the router still owns orchestration.

**How do I bypass cc10x for one task?**
Say "skip cc10x" (or "without cc10x" / "don't use cc10x"). Only those exact opt-out
phrases bypass the router.

**Where is the full documentation?**
README.md (user-facing), then `docs/cc10x-orchestration-bible.md` for the deep model.
