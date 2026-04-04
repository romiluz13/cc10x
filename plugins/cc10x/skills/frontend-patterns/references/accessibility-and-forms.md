# Accessibility And Forms

## Table of Contents
- [Keyboard And Focus](#keyboard-and-focus)
- [Labels And Names](#labels-and-names)
- [Contrast And Meaning](#contrast-and-meaning)
- [Form Input Rules](#form-input-rules)
- [Touch And Mobile Considerations](#touch-and-mobile-considerations)
- [Quick Checklist](#quick-checklist)

## Keyboard And Focus

Check:
- every interactive element is reachable with keyboard
- focus is visible
- tab order matches the reading order
- dialogs, drawers, and menus manage focus deliberately

Never replace a semantic control with a clickable `div`.

## Labels And Names

Check:
- every input has a visible label or a correct accessible name
- icon-only buttons have `aria-label`
- images have meaningful alt text when they convey content
- hint and error text is associated with the control

## Contrast And Meaning

Check:
- text contrast meets WCAG AA
- status is not conveyed by color alone
- disabled and inactive states remain understandable

## Form Input Rules

Use:
- the correct input type (`email`, `tel`, `url`)
- `autocomplete` where the browser can help
- `inputMode` for mobile keyboards when useful
- `spellCheck={false}` for emails, codes, and usernames

Do not:
- block paste on passwords or codes
- hide required state only in color or placeholder text
- leave errors unfocused after submit

When submit fails, focus the first invalid field if the flow supports it.

## Touch And Mobile Considerations

Check:
- touch targets are at least 44px
- tap behavior is deliberate and not double-fire prone
- safe-area padding is respected where needed
- modal or drawer scroll behavior does not trap or leak scroll unexpectedly

## Quick Checklist

Before completing a UI task:
- keyboard path works
- labels are present
- focus is visible
- contrast is sufficient
- form errors are announced clearly
- touch targets are usable on mobile
