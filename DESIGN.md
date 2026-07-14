---
name: Harness & Loop Engineering Keynote
description: Electric Print field guide for senior builders designing agent harnesses and loops
colors:
  primary: "#EA3F20"
  secondary: "#2646D8"
  tertiary: "#1C8A63"
  memory-gold: "#D3911A"
  neutral-bg: "#E8E4DC"
  neutral-ink: "#141312"
  neutral-muted: "#625E57"
typography:
  display:
    fontFamily: "Archivo Narrow, Arial Narrow, Arial, sans-serif"
    fontSize: "clamp(3.75rem, 8vw, 8.5rem)"
    fontWeight: "900"
  body:
    fontFamily: "Archivo, Arial, sans-serif"
    fontSize: "clamp(1rem, 1.5vw, 1.35rem)"
    fontWeight: "600"
  mono:
    fontFamily: "IBM Plex Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "0.8rem"
    fontWeight: "600"
rounded:
  none: "0"
  tight: "2px"
spacing:
  slide-x: "clamp(2rem, 6vw, 7rem)"
  slide-y: "clamp(2rem, 5vh, 5rem)"
  signal-gap: "0.75rem"
components:
  signal-rule:
    backgroundColor: "{colors.neutral-ink}"
    textColor: "{colors.neutral-bg}"
    rounded: "{rounded.none}"
  evidence-mark:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.neutral-bg}"
    rounded: "{rounded.tight}"
  decision-mark:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral-ink}"
    rounded: "{rounded.tight}"
---

## Overview

**Creative North Star: "The Electric Field Manual."** This keynote looks like the engineering document people keep because it changes how they work. It combines the confidence of a printed technical manifesto with the energy of a live system under load. The surface is warm paper and dark ink, not a dark-mode agent dashboard.

**The Meaningful Color Rule.** Color always names a role: warning red means a decision or control boundary, cobalt means system structure or context, green means verified evidence, and gold means durable memory or a handoff. Color never exists merely to make a slide look futuristic.

**The One-Message Slide Rule.** A slide speaks one sentence. It may contain a diagram, a field note, or an artifact, but it never becomes a documentation page. Visual rhythm alternates between manifesto typography, dense technical diagrams, evidence snapshots, and quiet field notes.

**The Motion Carries State Rule.** Motion reveals relationships, not decoration. Signal paths draw in, evidence changes a verdict, and a new state replaces the old one. Use precise cuts and short ink-reveal timing. Never use looping ambient particles, bounce, elastic easing, or terminal-rain effects.

## Colors

**The Print-and-Signal Rule.** The paper and ink are the stage. Use warning red, cobalt, verified green, and memory gold with decisive restraint, but use them generously when they communicate system meaning. A slide that could swap all color roles without changing its meaning has failed.

- **Paper** is the primary slide field. It makes technical material feel public, direct, and human rather than trapped in a developer tool.
- **Ink** carries architecture, primary type, rules, and folios.
- **Warning red** marks control, failure, boundary, and decisive action. It must never become generic error decoration.
- **Cobalt** marks structure, routing, context, and system maps.
- **Verified green** marks evidence, successful validation, and a proven condition.
- **Memory gold** marks persistence, handoff, history, and durable learning.

## Typography

**The Headline Is an Instrument Rule.** Display type is compressed, oversized, and physical. Headlines use tight tracking and deliberate line breaks to create pressure and release. Do not use floating centered marketing copy or sentence-case platitudes.

**The Annotation Is Evidence Rule.** Mono type is reserved for folios, labels, source identifiers, system states, arrows, and field notes. It must look like an engineering annotation, not fake code wallpaper.

Body copy is short, muscular, and spoken. It uses concrete verbs: select, constrain, inspect, prove, preserve, and escalate. The deck never uses “revolution,” “magic,” “10×,” or generic claims about the future.

## Elevation

**The Flat Paper Rule.** Surfaces are flat. Separation comes from ink rules, hard color blocks, cropping, whitespace, and scale. Shadows, translucent glass, blur, and floating SaaS panels are prohibited.

**The Field Note Rule.** When a detail needs emphasis, use a small printed annotation, source tag, or edge-aligned stamp. Never introduce an ornamental callout card or a colored side stripe.

## Components

- **Manifesto slide:** enormous display statement, a single colored intervention, folio, and one small field label.
- **System map:** paper or ink background; role-colored nodes and arrows; no equal-card grid. The direction of the diagram must remain clear if the color disappears.
- **Workflow strip:** a horizontal or vertical contract with explicit state transitions, evidence point, and escalation branch.
- **Evidence artifact:** a framed real trace, source excerpt, test outcome, or decision record. It must be readable and explain why it changed the next state.
- **Field note:** a short, edge-aligned principle or trade-off with a source marker.
- **Open-source x-ray:** two host columns only when they reveal the same reusable design decision. Never compare products feature-for-feature.
- **Motion:** diagram lines reveal with a fast ease-out; verdict state changes use a clean cut; reduced visual complexity is preferred over ornamental animation.

## Do's and Don'ts

**Do** make the field visible: show workflows, tools, state, evidence, and decisions as engineering artifacts.

**Do** make CC10x and Auto-Pi inspectable evidence for a portable discipline.

**Do** use color to carry system meaning and typography to carry emotion.

**Don't** make the deck look like an AI product landing page, a terminal emulator, a cyberpunk movie poster, or a generic investor deck.

**Don't** use glassmorphism, gradient text, hero metrics, identical cards, decorative glow, terminal rain, or stock “future” imagery.

**Don't** turn source claims into authority theatre. A source must illuminate a design choice, not substitute for one.
