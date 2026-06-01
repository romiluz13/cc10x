# DESIGN.md Authoring

Use this reference when creating or updating a spec-aligned project-local `DESIGN.md` from a screenshot, existing UI, user preferences, or a chosen visual inspiration.

## Priority

`DESIGN.md` is a project-local visual contract. It is subordinate to explicit user instructions, repo design-system constraints, accessibility requirements, and approved plans. It is stronger than generic frontend taste.

Do not copy a screenshot or a brand. Extract the durable design system behind it.

## Format Contract

Write `DESIGN.md` as two harmonized layers:

- YAML front matter: machine-readable design tokens. These are the normative values agents and tools should preserve.
- Markdown body: human-readable rationale. This explains why the tokens exist and how to apply them.

Prefer front matter even though the format allows it to be omitted. A useful minimum includes:

```yaml
---
version: alpha
name: <project or design-system name>
description: <one-sentence visual identity>
colors:
  primary: "#..."
  on-primary: "#..."
typography:
  body-md:
    fontFamily: <font family>
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: 4px
spacing:
  sm: 8px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
---
```

Use token references like `{colors.primary}` instead of duplicating values. Component variants such as hover, active, and pressed should be separate related component tokens, for example `button-primary-hover`.

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
6. When Node/network tooling is available, validate with `npx @google/design.md lint DESIGN.md`; treat errors as blockers and warnings as review items.

## Stable Structure

Use the canonical section order. Sections may be omitted when irrelevant, but present sections should stay in this order and should not be duplicated:

```md
# DESIGN.md

## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
```

`## Brand & Style` may replace `## Overview`. `## Layout & Spacing` may replace `## Layout`. `## Elevation` may replace `## Elevation & Depth`.

Keep extra sections rare. If the project needs accessibility, responsive, motion, or agent-prompt guidance, fold it into the closest canonical section or add it after the canonical sections without disrupting their order.

## Token Rules

- Use `colors`, `typography`, `rounded`, `spacing`, and `components` as the primary token groups.
- Colors must be sRGB hex values such as `"#1A1C1E"`.
- Dimensions should use `px`, `em`, or `rem`; unitless line-height is acceptable.
- Typography tokens may define `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, `fontFeature`, and `fontVariation`.
- Component token properties should prefer `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, and `width`.
- Unknown token names are acceptable when valid and useful; unknown component properties may warn, so use them only when the project needs them.
- Avoid broken references. Every `{path.to.token}` must point to an existing token.
- Include at least a `primary` color when colors are defined, and include typography tokens when colors are defined.

## Extraction Rules

- Convert screenshot colors into semantic roles such as `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`, and component-specific roles.
- Describe typography by role and feeling before naming exact fonts. Use exact fonts only when known, available, or explicitly requested.
- Capture spacing as a tokenized rhythm: compact, airy, editorial, dashboard-dense, cinematic, etc.
- Translate components into reusable token-backed rules: buttons, cards, nav, inputs, tables, modals, charts, and empty/error states.
- Include anti-patterns in `## Do's and Don'ts`: what would make the UI feel wrong.
- Include responsive and motion expectations in the closest canonical section unless the project truly needs a separate section.
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

## Validation Rules

- Run `npx @google/design.md lint DESIGN.md` when practical and non-disruptive.
- Fix `broken-ref` and duplicate-section findings before implementation.
- Review warnings for missing `primary`, low contrast, orphaned tokens, missing typography, missing optional token sections, and section-order drift.
- Use `npx @google/design.md diff before.md after.md` for substantial revisions when both versions are available.
