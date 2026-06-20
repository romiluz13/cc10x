---
name: frontend-design-critique
description: "Use when reviewing the visual/UX quality of a built UI — to score it against an anchored rubric, catch AI-slop patterns, and avoid one reasoning head rubber-stamping its own design."
allowed-tools: Read Grep Glob Bash
user-invocable: false
---

# Frontend Design Critique

## Overview

`frontend-patterns` tells you how to AUTHOR a UI (accessibility, states, responsive layout, visual direction). This skill is the other half: a READ-only CRITIQUE pass that judges a UI that already exists and emits scored findings. It does not edit. It scores and flags; the caller decides what to fix.

**Core principle:** A design self-graded by the head that built it is not reviewed — it is rationalized. Independence and an anchored scale are the whole point.

This skill is the critique/scoring pass. `frontend-patterns` is the authoring guidance. When they overlap (e.g. the two-altitude reflex check, the AI-slop reflex lists), cross-reference `frontend-patterns` rather than restating it — a second copy drifts.

## The Iron Law

```
TWO ISOLATED ASSESSMENTS BEFORE ONE VERDICT
```

If both assessments ran inside one reasoning pass, you did not critique — you anchored. Start over with A and B isolated.

## Two Isolated Assessments + Synthesis

cc10x already runs the **code-reviewer** and **silent-failure-hunter** in parallel on purpose (see `code-review-patterns`). Apply the same isolation to design.

- **Assessment A — design-director qualitative review.** An LLM reads the UI as a senior design director would: hierarchy, rhythm, restraint, whether the layout serves the task, whether it feels intentional or assembled. Score the rubric below. A forms its opinion WITHOUT running the ban-list scan.
- **Assessment B — AI-slop / pattern scan.** A SEPARATE pass that walks the ban-list and the deterministic detector (if available). B must NOT see A's conclusions — give it the artifact, not A's writeup. A checklist pass that can read the design-director's narrative silently converges on it.
- **Synthesis — reconcile only after both commit.** Where A and B independently agree → high confidence. Where B caught what A's eye glossed → keep it (a finding the other missed is the value of two passes, not noise). Where B's match is a false positive on inspection → drop it with a one-line reason.

**Why isolation is non-negotiable:** collapse A and B into one head and the first concern read biases the second — the director rationalizes away a slop smell, or the checklist over-weights a pattern the director already excused. Reconcile AFTER both have committed their lists, never during.

If you can only run one head, run B first (mechanical, no narrative), record it, THEN run A — never the reverse. A's narrative contaminates B; B's list barely colors A.

## Anchored 0-4 Rubric

Score each heuristic 0-4 against the explicit criteria. No half-points; pick the integer whose criteria match. Mirrors the anchored rubric in `code-review-patterns` so two critics land on the same number.

Heuristics (Nielsen-style, design-weighted):

- **Visual hierarchy** — does the eye land on what matters first?
- **Visual rhythm & spacing** — consistent spatial system, or random gaps?
- **Restraint & intentionality** — every element earns its place, or decoration-by-default?
- **Consistency & system fit** — matches its own tokens/components and neighboring flows?
- **Feedback & state legibility** — are loading/error/empty/active states visibly distinct?
- **Distinctiveness** — does it read as designed-for-this, or as a template?

| Score | Criteria |
|-------|----------|
| **0** | Broken or actively confusing. Hierarchy unreadable, states indistinguishable, or the layout fights the task |
| **1** | Works but generic and fragile. Template defaults, inconsistent rhythm, obvious AI-slop tells |
| **2** | Solid and competent, unremarkable. On-system, correct, nothing memorable — most real interfaces live here |
| **3** | Good. Intentional hierarchy, consistent system, distinctive without trying too hard. The bar you'd happily ship |
| **4** | Genuinely excellent. Every element earns its place, the composition is deliberate, and it could not be guessed from the category. Rare |

**Band → action & severity:**

| Total band (avg across heuristics) | Action | Severity of gaps |
|------------------------------------|--------|------------------|
| 0 | Do not ship — name the broken heuristic | P0 |
| 1 | Rework before ship — name each template tell | P1 |
| 2 | Ship with noted follow-ups | P2 |
| 3-4 | Ship | P3 (polish only) |

**Calibration — be honest.** Most real interfaces score mid-band (2). A 4 means genuinely excellent, not "looks fine." If every UI you critique scores 3-4, your scale is broken, not the design. Anti-grade-inflation is the job; a rubber-stamp critique is worse than none.

## AI-Slop Ban-List (Match and Refuse)

Assessment B matches the artifact against the current clichés below and refuses them by default. These are the present tells; the list is a moving target — prune a lane once it stops being a reflex, add new ones as they saturate (same discipline as `frontend-patterns`' reflex-reject lists).

| Slop pattern | Why it's a tell | Default verdict |
|--------------|-----------------|-----------------|
| Side-stripe / left-accent-border cards | Framework-starter default, signals "untouched" | Refuse |
| Gradient text headings | 2023-era AI-tool reflex | Refuse |
| Glassmorphism by default | Blur-everything with no rationale | Refuse |
| Hero-metric template ("10x / 99.9% / 500ms" stat row) | Pasted-in social proof shape | Refuse |
| Identical card grids (N equal boxes, no hierarchy) | No editorial decision was made | Refuse |
| Modal as the first-thought container | Reaching for a modal before considering inline/page | Refuse |
| Cream + serif + terracotta "editorial" palette | The current anti-AI reflex (reflex #2) | Refuse |
| Black + acid-lime/green accent | The current anti-corporate reflex (reflex #2) | Refuse |

**Two-altitude reflex check (cross-reference, do not duplicate).** `frontend-patterns` owns the full first-order / second-order definition. As a critique reflex: (1) could you guess the theme + palette from the **category alone**? (2) could you guess it from **category + anti-references** (what the category now flees toward)? If either is yes, flag it as generic and require rework. See `frontend-patterns` → "Two-Altitude Reflex Check" for the canonical version.

A ban-list match is a finding, not an automatic 0 — record it in B, then let synthesis decide severity against A's read. A single justified glassmorphism panel in an otherwise distinctive UI is not the same as glassmorphism-as-default.

## Optional Deterministic Detector (Best-Effort)

The upstream `impeccable` technique ships an npx slop-detector. cc10x must NOT hard-depend on it. Treat any external detector as best-effort:

- If a detector is configured/available (e.g. an `npx` tool the repo already uses), run it in Assessment B and fold its output into the scan.
- If no detector is present, the ban-list scan still runs by hand — the checklist above IS the floor. Never block the critique on a missing tool, and never invent a tool call.
- Probe cheaply before assuming: `Glob`/`Grep` for an existing config, or check `package.json` scripts. Do not install anything.

## RTL / Hebrew-Aware Notes

When the UI is RTL (Hebrew, Arabic), the critique adds:

- **Mirroring correctness** — does layout, icon direction, and progress/flow direction mirror, or is it LTR with translated strings bolted on?
- **Logical properties** — `margin-inline-start` / `padding-inline` etc. over hard-coded `left`/`right`, so the design holds in both directions.
- **Mixed-direction runs** — Latin tokens (brand names, numbers, code) inside RTL text should not break alignment or punctuation placement.
- **Typography** — Latin-first font stacks often render Hebrew flat; flag a missing intentional Hebrew face as a distinctiveness gap, not just a nit.

## Output Format

```markdown
## Design Critique: [Screen/Component]

### Assessment A — Design Director (qualitative)
[2-4 sentences: what works, what reads as assembled vs. intentional]

### Assessment B — Slop / Pattern Scan
- [match] Gradient text heading at `file:line` — ban-list: gradient text
- [match] Equal 4-card grid, no hierarchy at `file:line`
- Detector: [ran / not available — manual scan only]

### Synthesis
| Heuristic | Score 0-4 | Note |
|-----------|-----------|------|
| Visual hierarchy | 2 | ... |
| Visual rhythm & spacing | 1 | ... |
| Restraint & intentionality | 2 | ... |
| Consistency & system fit | 3 | ... |
| Feedback & state legibility | 2 | ... |
| Distinctiveness | 1 | ... |

**Band:** [avg] → [action]

**Agreed (high confidence):** [A and B both flagged]
**Detector-only (kept):** [B caught, A's eye missed]
**False positives (dropped):** [match + one-line reason]

### Required reworks
| Severity | Finding | Location | Fix direction |
|----------|---------|----------|---------------|
| P1 | [finding] | `file:line` | [direction, not a diff] |
```

## Red Flags — STOP and Re-critique

- Ran A and B in one reasoning pass (or let A's narrative reach B)
- Every heuristic scored 3-4 (grade inflation — re-read against the criteria)
- Zero findings on a non-trivial UI (insufficient depth, not perfect design — re-scan the ban-list)
- Flagged a slop pattern with no `file:line` (a finding without evidence is not a finding)
- Started editing the UI (this skill critiques; it does not edit)
- Skipped the RTL checks on an RTL UI

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I'll just do both passes in my head at once" | That IS the anchoring failure. Isolate A and B. |
| "It looks clean, score it a 4" | Clean and unremarkable is a 2. A 4 is rare and earned. |
| "The detector isn't installed, skip the scan" | The ban-list is the floor; scan by hand. |
| "Glassmorphism is fine, everyone uses it" | Default-glass is a tell. Justify it or refuse it. |
| "It's RTL but the strings are translated, done" | Translated ≠ mirrored. Check direction, not just text. |
| "Critique found nothing" | Zero findings on real UI means shallow review. Re-scan. |
```
