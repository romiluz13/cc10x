# DESIGN.md Authoring

Use this reference when creating or updating a project-local `DESIGN.md` from a screenshot, existing UI, user preferences, or a chosen visual inspiration.

## Priority

`DESIGN.md` is a project-local visual contract. It is subordinate to explicit user instructions, repo design-system constraints, accessibility requirements, and approved plans. It is stronger than generic frontend taste.

Do not copy a screenshot or a brand. Extract the durable design system behind it.

## Workflow

1. Inspect source input:
   - screenshot, existing UI, product copy, user preference, or inspiration reference
   - identify durable signals, not one-off content
2. Extract visual language:
   - atmosphere and density
   - color roles and contrast intent
   - typography feel and hierarchy
   - spacing rhythm and layout grid
   - component shapes, borders, radius, and elevation
   - motion/interaction style
   - responsive behavior
   - accessibility constraints
3. Ask only if a critical preference is ambiguous:
   - light/dark default
   - strict brand match vs loose inspiration
   - playful vs serious tone
   - high-density product UI vs editorial/marketing layout
4. Write or update `DESIGN.md` in the stable structure below.
5. Before frontend implementation, read `DESIGN.md` as the visual contract and preserve repo/user constraints.

## Stable Structure

```md
# DESIGN.md

## Visual Theme & Atmosphere
## Color Palette & Roles
## Typography Rules
## Component Styling
## Layout Principles
## Depth & Elevation
## Motion & Interaction
## Responsive Behavior
## Accessibility Guardrails
## Do's And Don'ts
## Agent Prompt Guide
```

## Extraction Rules

- Convert screenshot colors into semantic roles such as `background`, `surface`, `primary`, `accent`, `border`, `muted`, `success`, `warning`, and `danger`.
- Describe typography by role and feeling before naming exact fonts. Use exact fonts only when known, available, or explicitly requested.
- Capture spacing as a rhythm: compact, airy, editorial, dashboard-dense, cinematic, etc.
- Translate components into reusable rules: buttons, cards, nav, inputs, tables, modals, charts, and empty/error states.
- Include anti-patterns: what would make the UI feel wrong.
- Include responsive rules even if the screenshot is desktop-only.
- Include accessibility guardrails: contrast, focus, keyboard, touch targets, reduced motion, and non-color status cues.

## Screenshot-Specific Rules

- If the screenshot is partial, mark unknowns as assumptions instead of inventing a full design system.
- Preserve the user's preferences over the screenshot if they conflict.
- If multiple screenshots conflict, write the shared system first and list variants explicitly.
- Do not mention private screenshot contents beyond the design rules needed by the project.

## Inspiration Rules

Use inspiration references to choose a direction, not to clone:
- "Vercel-like" means monochrome precision and developer clarity, not copied pages.
- "Linear-like" means calm dense product UI and refined hierarchy, not copied components.
- "MongoDB-like" means green developer trust and documentation clarity, not copied branding.

If a user asks for exact brand imitation, pause and frame it as "inspired by" unless they own the brand or explicitly confirm they want a close internal mock.
