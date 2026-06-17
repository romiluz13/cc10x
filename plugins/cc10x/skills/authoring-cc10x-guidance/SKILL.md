---
name: authoring-cc10x-guidance
description: "Use when writing or editing a cc10x skill, agent, or router rule, to choose the right form of guidance for the failure you are fixing."
allowed-tools: Read Grep Glob
user-invocable: false
---

# Authoring CC10x Guidance

> **DIVERGENCE FROM superpowers:writing-skills:** Forked and narrowed to cc10x. The red-green-refactor discipline, the mechanical-vs-judgment split, and the description-shape rule are shared. CC10x ADDS: the failure→form mapping grounded in the empirical prohibition-backfire finding, the SDO rule generalized from the 4-skill validator already in this repo, and the persuasion-lever map.

## Overview

cc10x is ~15 skills and ~10 agents of behavior-shaping text. Every edit to that text is a chance to reach for a PROHIBITION when a RECIPE was needed. The most common authoring mistake is fixing a bad OUTPUT by adding a "never do X" rule — which, empirically, makes the output worse.

**Core principle:** Match the form of the guidance to the TYPE of failure you observed. The failure type — not your instinct — picks the form.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO GUIDANCE EDIT WITHOUT AN OBSERVED BASELINE FAILURE
```

If you cannot point to a real agent failing in the specific way you are trying to fix, you are guessing — and guesses are how this corpus bloats. Observe the failure first.

## Match the Form to the Failure

The failure type determines the form. Diagnose the failure, then pick the matching row — do not default to a prohibition.

| Failure observed | Form to use | Why this form |
|------------------|-------------|---------------|
| **rule-violation-under-pressure** — the agent KNOWS the rule but talks itself out of it | A prohibition + a rationalization→rebuttal table | The knowledge is present; the gap is resolve. A prohibition restates the line; the table pre-empts the specific excuse that defeats it. |
| **wrong-output-SHAPE** — output is the wrong shape, too bloated, restates the spec, wrong format | A positive recipe / contract / template | The agent doesn't know the target shape. Show it. **Do NOT add a prohibition** — see the backfire finding below. |
| **omission** — a needed thing is silently left out | A REQUIRED structural slot the agent must fill | An empty named slot forces the omission to become visible; "remember to include X" does not. |
| **conditional-misapplication** — the agent applies a rule when it shouldn't, or skips it when it should | A predicate-keyed conditional: "WHEN X, do Y" | Binds the behavior to its trigger so it fires exactly when relevant and stays silent otherwise. |

### The empirical backfire finding (read this before adding any "never")

**Prohibitions backfire on shaping problems.** Adding "never restate the spec" to fix a bloated verdict makes verdicts MORE bloated, not less — the prohibition keeps the unwanted concept salient and the agent over-corrects around it. For taste and shape problems, the fix is to **DELETE the rules that are crowding the output and feed CONTEXT** (a worked example of the right shape), per the anti-over-prompting lesson: *fix output by deleting rules and feeding context, never by adding a counter-rule.*

The dividing line:
- **Taste / shape** → delete rules, feed context (a recipe or example). No gate.
- **Truth / safety violation** → THIS earns a gate (a prohibition, a hard stop, a verification step). Only here.

If you are not fixing a truth or safety violation, you almost certainly do not want a new prohibition.

## Red-Green-Refactor for Skills

No skill edit ships without first OBSERVING a baseline failure. This pairs with the skill-eval-harness skill.

1. **RED** — Reproduce the failure with a real agent run. Capture the actual bad output. If you can't make it fail, you can't prove your edit helped.
2. **GREEN** — Make the smallest edit (per the form-matching table) that turns the observed failure into the desired behavior. Re-run the same eval.
3. **REFACTOR** — Tighten the wording, remove anything the eval shows is inert, and confirm you didn't regress a sibling behavior.

An edit with no RED step is a guess. Guesses are how prohibitions accumulate and the corpus rots.

## The Mechanical-vs-Judgment Boundary

Put each check where it can actually run:

- **Mechanical / deterministic / greppable** → code (a hook or validator). A regex invariant, a required frontmatter field, a banned literal string — these are not prompt material. Prose asking the agent to "remember to check" a greppable thing is strictly weaker than a hook that enforces it.
- **Judgment / taste / context-dependent** → prompt guidance. Whether a verdict reads as bloated, whether an approach fits the codebase — no validator can score this; it belongs in the skill body.

Two anti-patterns to avoid: putting a greppable invariant in prose (it will drift and won't be enforced), and putting taste in a hook (it will false-positive and get disabled).

## M3 — Skill-Description-Shape Rule (SDO)

A skill or agent `description:` field MUST:

1. **State WHEN to use it** — triggers, symptoms, the situation that should pull this skill in. The description's whole job is routing.
2. **NEVER summarize what it does step-by-step.**

The reason is empirical, not stylistic: an agent that sees a step-summary in the description FOLLOWS the description and SKIPS reading the skill body. Documented case — a description that said "code review between tasks" caused agents to run ONE review when the body specified TWO. The summary became a ceiling on behavior.

cc10x already enforces a version of this via a validator on 4 skills. This generalizes the rule to ALL authored skills, agents, and router rules: descriptions are triggers, never summaries.

## Persuasion-Lever Map

When you do need to shape judgment in prose, these are the levers and where each lands:

| Lever | Lands when… |
|-------|-------------|
| **Spirit-over-letter framing** ("violating the letter is violating the spirit") | The failure is the agent gaming the literal wording while defeating the intent. |
| **Rationalization → rebuttal table** | The agent knows the rule but has a predictable excuse to skip it (pairs with a prohibition for rule-violation-under-pressure). |
| **Foundational principle** (one crisp "Core principle" line) | The behavior generalizes beyond the listed cases and you want the agent to extrapolate correctly. |
| **Worked example** (show the right shape, don't describe it) | The failure is SHAPE — this is the fix that replaces a prohibition. |

## The Bottom Line

Observe the failure. Name its type. Pick the matching form. If the failure is shape or taste, delete a rule and show an example — do not add a prohibition. Only truth and safety violations earn a gate. Mechanical checks go in code; judgment stays in prose; descriptions are triggers, never summaries.
