# Session Learnings

Date: 2026-03-12

This file captures the durable lessons from this session so they do not remain implicit in chat only.

## 1. Trust beats cleverness

The strongest harnesses are not the ones with the most agents or the most markdown.
They are the ones that most reliably prevent silent divergence, false completion, skipped verification, and state loss.

## 2. Orchestration and prompt engineering are separate strengths

A repo can be strong because of:
- orchestration and process enforcement
- prompt quality and instruction sharpness
- both

These must be evaluated separately before they are combined.

## 3. CC10X improved materially during this session

The work completed in this session made CC10X stronger on:
- plan trust
- phase-gated execution
- explicit proof states
- workflow identity and v10 state isolation
- verifier harshness
- benchmark discipline

CC10X is stronger than it was at the start of the session.

## 4. CC10X is top-tier, but not first place yet

The honest conclusion after the benchmark rounds is:
- CC10X is in the top tier
- CC10X is not clearly first place yet

The strongest competitors remain:
- `metaswarm` on adversarial planning and reviewer posture
- `get-shit-done` on execution-language continuity
- `babysitter` on deterministic state/replay confidence
- `superpowers` on anti-false-completion wording

## 5. The main remaining gap is prompt sharpness

CC10X now has a strong centralized trust harness, but some refs still beat it on the English itself:
- harder PASS/FAIL reviewer voice
- better goal-backward execution language
- better anti-rationalization wording
- better trigger and description hygiene

## 6. Descriptions and trigger metadata are behavior

This is one of the most important lessons from the `skill-creator` reference and `superpowers`.

Descriptions are not passive metadata.
They influence model behavior, routing, and whether a skill is even loaded.
Bad descriptions can weaken a strong workflow.

## 7. Prompt dilution is a real failure mode

Prompt dilution happens when:
- too many surfaces say similar things differently
- advisory instructions sound authoritative
- summaries collapse richer workflows into shortcuts
- hard constraints are surrounded by soft text

This is one of the main risks for CC10X.

## 8. The best next phase is not more ranking

The best next phase is:
1. prompt-surface audit of the strongest refs and CC10X
2. prompt-by-prompt rewrite of CC10X core instruction surfaces
3. head-to-head behavior evals on canonical tasks

## 9. The competition target is specific

To win a serious harness competition, CC10X must become:
- better planning than `metaswarm`
- better execution and verification than `get-shit-done`
- more trustworthy state/recovery than `babysitter`
- sharper anti-slop wording than `superpowers`

That means the path to winning is not “be larger.”
It is “be sharper, stricter, and more coherent.”

## 10. What is proven vs not proven

Proven enough to act on:
- CC10X has a stronger trust contract than before
- CC10X is top-tier among the reviewed refs
- orchestration and prompt engineering must be judged separately

Not yet proven:
- that CC10X is first place overall
- that every meaningful instruction line in every top repo has been audited
- that current CC10X wins all live head-to-head behavioral evals
