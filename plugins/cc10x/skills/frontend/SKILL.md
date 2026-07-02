---
name: frontend
description: |
  Two-mode frontend skill: (1) authoring — accessibility, responsive layout,
  loading/error states, performance, DESIGN.md authoring, visual direction;
  (2) critique — READ-only scored review of built UI against anchored rubric,
  AI-slop detection, two isolated assessments. Router invokes mode via context.
allowed-tools: Read Grep Glob Bash LSP
user-invocable: false
---

# Frontend (Authoring + Critique)

Two modes: `authoring` (build UI with patterns) and `critique` (score built UI). Both share the visual-direction rules below.

## Reference Files

Read only what's needed:

- `references/ui-state-and-feedback.md` — loading/error/empty/success ordering, skeleton vs spinner
- `references/accessibility-and-forms.md` — WCAG, keyboard/focus, labels, form patterns, mobile
- `references/performance-and-layout.md` — responsive, motion, overflow, URL state, light/dark mode
- `references/design-md-authoring.md` — creating/updating DESIGN.md from screenshots, existing UI, preferences
- `references/design-md-inspiration-index.md` — style references when user asks for direction

## Shared Visual Direction Rules

### Two-Altitude Reflex Check

Before committing a visual direction, run both tests:

1. **First-order:** Could you guess the theme/palette from the category alone? ("Fintech → blue + sans-serif.") If yes → generic. Reject.
2. **Second-order:** Could you guess it from category + anti-references? Once everyone "avoids the purple gradient," the avoidance becomes a reflex — fintech dodging blue lands on the same off-black + lime. If predictable given what people flee toward → still generic. Reject.

The cure: derive direction from the specific product, audience, and content — not from the category or what the category is fleeing.

### Reflex-Reject Lists (maintained, pruned as families saturate)

| Reflex-reject fonts | Reflex-reject aesthetic lanes |
| --------------------- | ------------------------------- |
| Inter, Roboto, Arial, system-ui defaults | Purple/violet gradient on white (AI-tool reflex #1) |
| Geist / Geist Mono (over-saturated) | Off-black + acid-lime "anti-corporate" (reflex #2) |
| Space Grotesk as default "modern" pick | Warm-beige + serif "anti-AI" editorial (reflex #2) |
| Generic Google-Fonts pairing of the month | Glassmorphism cards on gradient mesh |

Prune a lane out once it stops being a reflex; add new families as they saturate. A stale blocklist becomes its own reflex.

### Anti-patterns Blocklist

| Anti-pattern | Fix |
| -------------- | ----- |
| `user-scalable=no`, `maximum-scale=1` | Remove — blocks accessibility zoom |
| `transition: all` | List properties explicitly |
| `outline-none` without replacement | Add `focus-visible:ring-*` |
| `<div onClick>` | Use `<button>` or `<a>` |
| Images without `width`/`height` | Add dimensions (prevents CLS) |
| Form inputs without labels | Add `<label>` or `aria-label` |
| Icon buttons without `aria-label` | Add `aria-label` |
| Emoji as UI icons (🚀 ✨) | Use SVG icons (Heroicons, Lucide) |
| Hardcoded date/number formats | Use `Intl.DateTimeFormat` |
| `autoFocus` everywhere | Use sparingly, desktop only |

### Motion Rules

Animate `transform`/`opacity` only — never `width`/`height`/`top`/`left`. List transition properties explicitly. 150-300ms for micro-interactions. Honor `prefers-reduced-motion`. Allow animation cancellation.

---

## Mode: AUTHORING

Design for user success, not aesthetic preference. Map user flow before writing UI. State order: Error → Loading (no data) → Empty → Success.

### Mock-Fidelity Inventory (No Silent Loss)

A build can pass every test and still quietly omit the hero or signature motif. Once a design/mock is approved, before coding, INVENTORY its major visible ingredients:

| Ingredient | Implementation path |
| ------------ | --------------------- |
| Hero / focal moment | Build now / phase 2 (explicit) / cut (approved) |
| Signature motifs | Build now / approximate / cut (approved) |
| Sections | Build now / phase 2 (explicit) / cut (approved) |
| Interactions | Build now / static fallback / cut (approved) |
| States (empty/loading/error) | Build now (states are not optional) |

Every ingredient gets exactly one path. "Cut" and "phase 2" are legitimate, but only when explicitly named — never reached by omission. Treat any silently-dropped major ingredient as a P0 fidelity defect.

### Design-System Drift Classifier

When a feature deviates from the design system, classify the root cause:

| Root cause | Fix |
| ------------ | ----- |
| **Missing token** — system has no value for this need | Add the token to the system, then use it |
| **One-off impl** — token/component exists, but feature reimplemented locally | Swap to shared component/token; delete the one-off |
| **Conceptual misalignment** — feature's interaction model fights the system's | Rework the flow — patching pixels won't fix it |

**Flow-shape match:** a feature's flow shape must match its neighbors. Modal vs full-page, save-on-blur vs explicit submit — inconsistency reads as broken even when every pixel is on-system. Treat unexplained flow-shape mismatch as conceptual-misalignment.

---

## Mode: CRITIQUE

READ-only. Scores and flags; caller decides what to fix. A design self-graded by the head that built it is not reviewed — it is rationalized.

### Two Isolated Assessments + Synthesis

**Assessment A — design-director qualitative review.** Read the UI as a senior design director would: hierarchy, rhythm, restraint, intentionality. Score the rubric. A forms its opinion WITHOUT running the ban-list scan.

**Assessment B — AI-slop / pattern scan.** SEPARATE pass walking the ban-list. B must NOT see A's conclusions — give it the artifact, not A's writeup.

**Synthesis — reconcile only after both commit.** Where A and B independently agree → high confidence. Where B caught what A's eye glossed → keep it. Where B's match is a false positive → drop with one-line reason.

If only one head: run B first (mechanical, no narrative), record it, THEN run A — never the reverse. A's narrative contaminates B; B's list barely colors A.

### Anchored 0-4 Rubric

Heuristics: visual hierarchy, visual rhythm & spacing, restraint & intentionality, consistency & system fit, feedback & state legibility, distinctiveness.

| Score | Criteria |
| ------- | ---------- |
| 0 | Broken or actively confusing |
| 1 | Works but generic and fragile. Template defaults, AI-slop tells |
| 2 | Solid, competent, unremarkable. Most real interfaces live here |
| 3 | Good. Intentional hierarchy, consistent system, distinctive |
| 4 | Genuinely excellent. Every element earns its place. Rare |

| Band (avg) | Action | Severity |
| ----------- | -------- | ---------- |
| 0 | Do not ship | P0 |
| 1 | Rework before ship | P1 |
| 2 | Ship with noted follow-ups | P2 |
| 3-4 | Ship | P3 (polish only) |

Be honest. Most interfaces score mid-band (2). A 4 is rare and earned. Anti-grade-inflation is the job.

### AI-Slop Ban-List

| Slop pattern | Default verdict |
| -------------- | ----------------- |
| Side-stripe / left-accent-border cards | Refuse |
| Gradient text headings | Refuse |
| Glassmorphism by default | Refuse |
| Hero-metric template (stat row) | Refuse |
| Identical card grids (no hierarchy) | Refuse |
| Modal as first-thought container | Refuse |
| Cream + serif + terracotta "editorial" palette | Refuse |
| Black + acid-lime/green accent | Refuse |

A ban-list match is a finding, not an automatic 0 — let synthesis decide severity against A's read.

### Optional Deterministic Detector

If an npx slop-detector is configured/available, run it in Assessment B. If not, the ban-list scan runs by hand. Never block on a missing tool, never invent a tool call.

### RTL / Hebrew-Aware Notes

When UI is RTL: check mirroring correctness (layout, icon direction, progress/flow), logical properties (`margin-inline-start` over hard-coded `left`/`right`), mixed-direction runs (Latin tokens in RTL text), and typography (missing intentional Hebrew face = distinctiveness gap).
