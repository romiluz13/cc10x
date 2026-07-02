# Performance And Layout

## Table of Contents
- [Responsive Layout Checks](#responsive-layout-checks)
- [Motion Rules](#motion-rules)
- [Content Overflow](#content-overflow)
- [Performance Guardrails](#performance-guardrails)
- [URL And View State](#url-and-view-state)
- [Color Modes](#color-modes)

## Responsive Layout Checks

Review at three widths:
- mobile: no horizontal scroll, touch targets still work
- tablet: navigation and density remain usable
- desktop: lines do not get unreadably wide

If a flex child should truncate, remember `min-w-0`.

## Motion Rules

Prefer:
- `transform` and `opacity`
- 150-300ms micro-interactions
- explicit transition properties
- honoring `prefers-reduced-motion`

Avoid:
- `transition: all`
- layout-shifting hover effects
- animation that blocks user action

## Content Overflow

Plan for short, medium, and absurdly long content.

Use:
- `truncate` for single-line overflow
- `line-clamp-*` for multi-line overflow
- `break-words` for URLs and long tokens
- placeholders for empty strings or arrays

## Performance Guardrails

Check:
- large lists are virtualized or bounded
- no layout reads in render
- below-the-fold images are lazy-loaded
- critical images or fonts are prioritized deliberately
- repeated expensive transforms are not recomputed in hot paths

## URL And View State

If the UI exposes meaningful state, consider syncing it to the URL:
- filters
- tabs
- sort
- pagination
- expanded detail panels

This improves shareability, refresh behavior, and back-button correctness.

## Color Modes

If light and dark mode both exist:
- check contrast in both
- avoid translucent surfaces that become unreadable in one mode
- set `color-scheme` deliberately when the platform should know
- ensure borders, focus rings, and disabled states stay visible
