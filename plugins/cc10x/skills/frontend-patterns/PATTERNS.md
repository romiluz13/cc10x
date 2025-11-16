# Frontend Patterns Library

This document provides a comprehensive library of frontend patterns covering UX, UI design, and accessibility.

## UX Patterns

### User Flow Patterns

- Step-by-step user interactions
- Flow optimization
- Friction point identification
- Flow completion tracking

### Loading State Patterns

- Loading indicators
- Skeleton screens
- Progressive loading
- Loading feedback

### Error Handling Patterns

- Error messages
- Error recovery
- Error prevention
- Error feedback

### Form Validation Patterns

- Input validation
- Real-time feedback
- Error display
- Success confirmation

### Action Feedback Patterns

- Button states
- Success indicators
- Progress indicators
- Confirmation dialogs

## UI Design Patterns

### Design Thinking & Aesthetic Direction

- **Purpose-driven design**: Understand what problem the interface solves and who uses it
- **Bold aesthetic direction**: Choose clear conceptual direction (minimal, maximalist, retro-futuristic, organic, luxury, playful, editorial, brutalist, art deco, soft, industrial, etc.)
- **Tone selection**: Pick an extreme aesthetic direction and execute with precision
- **Differentiation**: Identify what makes the interface UNFORGETTABLE and memorable
- **Intentionality over intensity**: Bold maximalism and refined minimalism both work - key is intentionality

### Visual Hierarchy Patterns

- Information architecture
- Content prioritization
- Visual weight
- Typography hierarchy

### Design Token Patterns

- Color systems
- Typography scales
- Spacing systems
- Component tokens

### Advanced Typography Patterns

- **Distinctive font selection**: Choose fonts that are beautiful, unique, and interesting
- **Avoid generic fonts**: Avoid Inter, Roboto, Arial, system fonts - opt for distinctive choices
- **Font pairing**: Pair distinctive display fonts with refined body fonts
- **Characterful fonts**: Unexpected, characterful font choices that elevate aesthetics
- Text sizing
- Line height
- Text contrast

### Color & Theme Patterns

- **Cohesive aesthetic**: Commit to a cohesive aesthetic direction
- **CSS variables**: Use CSS variables for consistency
- **Dominant colors with accents**: Dominant colors with sharp accents outperform timid, evenly-distributed palettes
- **Avoid generic color schemes**: Avoid cliched color schemes (particularly purple gradients on white backgrounds)
- **Theme variation**: Vary between light and dark themes, different color palettes
- **Context-specific character**: Make color choices that feel genuinely designed for the context

### Motion & Animation Patterns

- **Animations for effects**: Use animations for effects and micro-interactions
- **CSS-only solutions**: Prioritize CSS-only solutions for HTML
- **Motion library**: Use Motion library for React when available
- **High-impact moments**: Focus on high-impact moments - one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions
- **Staggered reveals**: Use animation-delay for staggered reveals
- **Scroll-triggering**: Use scroll-triggering animations
- **Hover states**: Hover states that surprise
- **State transitions**: Component state transitions

### Spatial Composition Patterns

- **Unexpected layouts**: Break away from predictable layouts
- **Asymmetry**: Use asymmetry for visual interest
- **Overlap**: Overlapping elements for depth
- **Diagonal flow**: Diagonal flow instead of only horizontal/vertical
- **Grid-breaking elements**: Elements that break the grid
- **Negative space**: Generous negative space OR controlled density
- Grid systems
- Responsive layouts
- Container patterns
- Alignment patterns

### Backgrounds & Visual Details Patterns

- **Atmosphere and depth**: Create atmosphere and depth rather than defaulting to solid colors
- **Contextual effects**: Add contextual effects and textures that match the overall aesthetic
- **Gradient meshes**: Creative gradient meshes
- **Noise textures**: Noise textures for visual interest
- **Geometric patterns**: Geometric patterns
- **Layered transparencies**: Layered transparencies for depth
- **Dramatic shadows**: Dramatic shadows for elevation
- **Decorative borders**: Decorative borders
- **Custom cursors**: Custom cursors that match the aesthetic
- **Grain overlays**: Grain overlays for texture

### State Design Patterns

- Component states
- State transitions
- State feedback
- State persistence

### Avoiding Generic AI Aesthetics

- **Avoid generic fonts**: Never use Inter, Roboto, Arial, system fonts
- **Avoid cliched color schemes**: Avoid purple gradients on white backgrounds, predictable color schemes
- **Avoid predictable layouts**: Avoid cookie-cutter design that lacks context-specific character
- **Vary aesthetics**: Never converge on common choices (like Space Grotesk) across generations
- **Context-specific design**: Make unexpected choices that feel genuinely designed for the context
- **Match complexity to vision**: Maximalist designs need elaborate code; minimalist designs need restraint and precision

## Accessibility Patterns

### Keyboard Navigation Patterns

- Tab order
- Keyboard shortcuts
- Focus management
- Keyboard-only navigation

### Screen Reader Patterns

- ARIA labels
- Semantic HTML
- Screen reader announcements
- Content structure

### Color Contrast Patterns

- WCAG compliance
- Contrast ratios
- Color-blind considerations
- Text readability

### Focus Management Patterns

- Focus indicators
- Focus trapping
- Focus restoration
- Focus order

## Pattern Usage

Reference these patterns when reviewing or designing frontend:

1. **Design Thinking**: Choose bold aesthetic direction, understand purpose, identify differentiation
2. **UX Review**: Check user flows, loading states, error handling, form validation, action feedback
3. **UI Review**: Check visual hierarchy, design tokens, layout systems, typography, color themes, motion, spatial composition, visual details
4. **Accessibility Review**: Check keyboard navigation, screen reader support, color contrast, focus management
5. **Aesthetic Excellence**: Ensure distinctive, memorable design that avoids generic AI aesthetics

## Pattern Composition

These patterns can be composed together:

- Design Thinking + UI Design = Distinctive, memorable interfaces
- UX + UI = Complete user experience
- UI + Accessibility = Inclusive design
- UX + Accessibility = Accessible user experience
- Motion + Spatial Composition = Dynamic, engaging layouts
- Typography + Color Theme = Cohesive aesthetic identity

## Design Principles

1. **Bold Intentionality**: Choose a clear conceptual direction and execute with precision
2. **Distinctive Choices**: Make unexpected choices that feel genuinely designed for the context
3. **Avoid Generic AI Aesthetics**: Never use generic fonts, cliched color schemes, or predictable layouts
4. **Match Complexity to Vision**: Maximalist designs need elaborate code; minimalist designs need restraint
5. **Production-Grade**: All designs must be functional, production-grade code
6. **Meticulously Refined**: Every detail matters - typography, spacing, colors, motion, textures

See `plugins/cc10x/skills/shared-patterns/PATTERN-COMPOSITION.md` for composition guidelines.

## Reference

Inspired by Anthropic's [frontend-design skill](https://github.com/anthropics/skills/tree/main/frontend-design) for creative design excellence and aesthetic direction.
