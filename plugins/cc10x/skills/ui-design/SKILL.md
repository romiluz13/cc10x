---
name: ui-design
description: Generates beautiful modern UIs matching Lovable and Bolt quality standards with modern gradients, smooth animations, proper spacing, and built-in accessibility. Transforms basic components into polished production-ready interfaces using design system principles, Tailwind CSS patterns, and React component best practices. Use when creating UI components, designing user interfaces, building frontend features, implementing design systems, or developing production-quality UI elements. Provides component library patterns, animation techniques, responsive design strategies, and accessibility integration. Particularly valuable for customer-facing features where UI quality matters. Loaded when frontend implementation needed or explicitly requested for UI design tasks.
license: MIT
---

# UI Design - Lovable/Bolt Quality

**Core Philosophy**: Every UI component should be beautiful, accessible, and delightful to use. No more basic, unstyled interfaces - create stunning UIs that users love.

---

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)

- **Skill**: UI Design
- **Purpose**: Generate Lovable/Bolt-quality beautiful, modern UIs
- **When**: Any frontend component, form, page, or UI element
- **Core Rule**: Use modern gradients, proper spacing, smooth animations, and accessibility
- **Why Different**: Lovable/Bolt create stunning UIs because they have killer design system prompts
- **Sections Available**: Design System (colors, spacing, shadows), Component Library, Animation Patterns, Responsive Design

---

### Stage 2: Quick Reference (triggered - ~500 tokens)

## The Lovable/Bolt Formula

What makes their UIs stunning:

### 1. Modern Color Gradients (Not Flat Colors!)

```tsx
// ❌ BAD: Flat, boring
<div className="bg-blue-600">

// ✅ GOOD: Beautiful gradient
<div className="bg-gradient-to-r from-indigo-600 to-purple-600">

// ✅ GREAT: Multi-stop gradient with depth
<div className="bg-gradient-to-br from-indigo-50 via-white to-purple-50">
```

**Quick Palette**:
- Primary: `from-indigo-600 to-purple-600`
- Success: `from-emerald-500 to-green-500`
- Warning: `from-amber-500 to-orange-500`
- Error: `from-rose-500 to-red-500`
- Neutral: `from-gray-50 to-gray-100`

### 2. Proper Spacing (Tailwind Scale)

```tsx
// ❌ BAD: Inconsistent spacing
<div className="p-3 mb-5">

// ✅ GOOD: Consistent Tailwind scale
<div className="p-8 mb-8">  // 8, 12, 16, 24 (multiples of 4)
```

**Spacing Scale**: 4, 8, 12, 16, 24, 32, 48, 64

### 3. Shadows & Depth (Not Flat!)

```tsx
// ❌ BAD: No depth
<div className="bg-white border">

// ✅ GOOD: Beautiful depth
<div className="bg-white rounded-2xl shadow-xl border border-gray-100">
```

**Shadow Scale**: `shadow-sm` → `shadow-md` → `shadow-lg` → `shadow-xl` → `shadow-2xl`

### 4. Smooth Animations

```tsx
// ❌ BAD: Instant, jarring
<button onClick={...}>

// ✅ GOOD: Smooth hover
<button className="transform hover:scale-105 transition-all duration-200">
```

### 5. Rounded Corners (Modern!)

```tsx
// ❌ BAD: Sharp corners or too rounded
<div className="rounded">

// ✅ GOOD: Modern, balanced
<div className="rounded-xl">  // lg, xl, 2xl (12-16px sweet spot)
```

## Quick Component Patterns

### Button (Lovable Level)
```tsx
<button className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200">
  Click Me
</button>
```

### Card (Modern)
```tsx
<div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-shadow">
  Content
</div>
```

### Input (Polished)
```tsx
<input className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all" />
```

---

### Stage 3: Detailed Guide (on-demand - ~3500 tokens)

## Complete Design System

### Color System (Modern Gradients)

#### Primary Colors (Actions)
```tsx
// Buttons, CTAs, interactive elements
bg-gradient-to-r from-indigo-600 to-purple-600
bg-gradient-to-br from-indigo-500 to-purple-600
bg-gradient-to-r from-blue-600 to-indigo-600

// Backgrounds (subtle)
bg-gradient-to-br from-indigo-50 via-white to-purple-50
bg-gradient-to-r from-blue-50 to-indigo-50
```

#### Success Colors
```tsx
// Success messages, confirmations
bg-gradient-to-r from-emerald-500 to-green-500
bg-gradient-to-br from-emerald-50 to-green-50
```

#### Warning Colors
```tsx
// Warnings, pending states
bg-gradient-to-r from-amber-500 to-orange-500
bg-gradient-to-br from-amber-50 to-orange-50
```

#### Error Colors
```tsx
// Errors, destructive actions
bg-gradient-to-r from-rose-500 to-red-500
bg-gradient-to-br from-rose-50 to-red-50
```

#### Neutral Colors
```tsx
// Text on backgrounds
text-gray-900  // Headings
text-gray-700  // Body text
text-gray-600  // Secondary text
text-gray-400  // Placeholder text

// Backgrounds
bg-gray-50     // Subtle background
bg-gray-100    // Hover states
bg-white       // Cards, modals
```

### Spacing System (Consistent Scale)

```tsx
// Padding (inside components)
p-2   // 8px  - Tight
p-4   // 16px - Normal
p-6   // 24px - Comfortable
p-8   // 32px - Spacious
p-12  // 48px - Very spacious

// Margin (between components)
space-y-4   // 16px - Normal
space-y-6   // 24px - Comfortable
space-y-8   // 32px - Spacious
space-y-12  // 48px - Section breaks

// Gap (flexbox/grid)
gap-2   // 8px  - Tight
gap-4   // 16px - Normal
gap-6   // 24px - Comfortable
gap-8   // 32px - Spacious
```

**Golden Rule**: Use multiples of 4 (4, 8, 12, 16, 24, 32, 48, 64)

### Shadow System (Depth & Elevation)

```tsx
// Subtle (hovering just above page)
shadow-sm   // Cards at rest
shadow-md   // Slight hover

// Medium (clear elevation)
shadow-lg   // Elevated cards
shadow-xl   // Important cards, modals

// Dramatic (floating above everything)
shadow-2xl  // Dropdowns, popovers, tooltips

// Colored shadows (extra special)
shadow-xl shadow-indigo-500/20  // Indigo glow
```

**Usage Pattern**:
```tsx
// Hover effect (Lovable style)
className="shadow-lg hover:shadow-xl transition-shadow duration-300"
```

### Border System

```tsx
// Subtle borders
border border-gray-200    // Default cards
border border-gray-300    // Inputs at rest

// Medium borders
border-2 border-gray-300  // Inputs (thicker)
border-2 border-indigo-500  // Inputs (focused)

// Strong borders
border-4 border-indigo-500  // Emphasis

// No border with shadow (modern)
border-0 shadow-xl  // Clean, elevated look
```

### Rounded Corners System

```tsx
// Subtle
rounded-lg   // 8px  - Small components
rounded-xl   // 12px - Medium components (MOST COMMON)
rounded-2xl  // 16px - Large components, cards
rounded-3xl  // 24px - Very large, special

// Full round
rounded-full  // Buttons, avatars, badges

// Specific corners
rounded-t-xl  // Top only (modals)
rounded-b-xl  // Bottom only
```

**Golden Rule**: Use `rounded-xl` (12px) for most things, `rounded-2xl` (16px) for cards

---

## Complete Component Library

### Buttons

#### Primary Button (CTA)
```tsx
<button className="group relative px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-indigo-300">
  <span className="flex items-center gap-2">
    <Icon className="w-5 h-5 group-hover:scale-110 transition-transform" />
    Primary Action
  </span>
</button>
```

#### Secondary Button
```tsx
<button className="px-6 py-3 bg-white text-indigo-600 border-2 border-indigo-600 rounded-xl font-semibold hover:bg-indigo-50 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-indigo-300">
  Secondary Action
</button>
```

#### Ghost Button
```tsx
<button className="px-6 py-3 text-gray-700 rounded-xl font-semibold hover:bg-gray-100 transition-all duration-200">
  Tertiary Action
</button>
```

#### Destructive Button
```tsx
<button className="px-6 py-3 bg-gradient-to-r from-rose-500 to-red-500 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-200">
  Delete
</button>
```

#### Button with Loading State
```tsx
<button className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg" disabled={loading}>
  {loading ? (
    <span className="flex items-center gap-2">
      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
      Loading...
    </span>
  ) : (
    'Submit'
  )}
</button>
```

### Cards

#### Basic Card (Modern)
```tsx
<div className="bg-white rounded-2xl shadow-xl hover:shadow-2xl transition-shadow duration-300 p-8 border border-gray-100">
  <h3 className="text-2xl font-bold text-gray-900 mb-4">Card Title</h3>
  <p className="text-gray-600 leading-relaxed">Card content goes here with proper line height and color.</p>
</div>
```

#### Card with Icon Header
```tsx
<div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
  <div className="flex items-center gap-4 mb-6">
    <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl flex items-center justify-center">
      <Icon className="w-6 h-6 text-white" />
    </div>
    <div>
      <h3 className="text-2xl font-bold text-gray-900">Card Title</h3>
      <p className="text-sm text-gray-500">Subtitle</p>
    </div>
  </div>
  <p className="text-gray-600 leading-relaxed">Content</p>
</div>
```

#### Interactive Card (Clickable)
```tsx
<button className="w-full text-left bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 p-8 border border-gray-100 transform hover:-translate-y-1">
  <h3 className="text-2xl font-bold text-gray-900 mb-4">Interactive Card</h3>
  <p className="text-gray-600">Click me!</p>
  <div className="mt-4 flex items-center text-indigo-600 font-semibold">
    Learn more <span className="ml-2">→</span>
  </div>
</button>
```

#### Card with Gradient Background
```tsx
<div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-xl p-8 text-white">
  <h3 className="text-2xl font-bold mb-4">Premium Feature</h3>
  <p className="opacity-90 leading-relaxed">White text on gradient background.</p>
</div>
```

### Forms & Inputs

#### Text Input (Polished)
```tsx
<div className="space-y-2">
  <label className="block text-sm font-medium text-gray-700">
    Email Address
  </label>
  <input
    type="email"
    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all duration-200 outline-none"
    placeholder="you@example.com"
  />
</div>
```

#### Input with Icon
```tsx
<div className="relative">
  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
    <Icon className="h-5 w-5 text-gray-400" />
  </div>
  <input
    type="text"
    className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all"
    placeholder="Search..."
  />
</div>
```

#### Input with Error State
```tsx
<div className="space-y-2">
  <label className="block text-sm font-medium text-gray-700">Email</label>
  <input
    type="email"
    className="w-full px-4 py-3 border-2 border-rose-500 rounded-xl focus:border-rose-500 focus:ring-4 focus:ring-rose-100 transition-all"
    placeholder="you@example.com"
  />
  <p className="text-sm text-rose-600 flex items-center gap-1">
    <Icon className="w-4 h-4" />
    Please enter a valid email address
  </p>
</div>
```

#### Textarea
```tsx
<textarea
  rows={4}
  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all resize-none"
  placeholder="Enter your message..."
/>
```

#### Select Dropdown
```tsx
<select className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all appearance-none bg-white cursor-pointer">
  <option>Select an option</option>
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

#### Checkbox (Custom Styled)
```tsx
<label className="flex items-center gap-3 cursor-pointer group">
  <input
    type="checkbox"
    className="w-5 h-5 border-2 border-gray-300 rounded checked:bg-indigo-600 checked:border-indigo-600 focus:ring-4 focus:ring-indigo-100 transition-all"
  />
  <span className="text-gray-700 group-hover:text-gray-900">Remember me</span>
</label>
```

#### Radio Button (Custom Styled)
```tsx
<label className="flex items-center gap-3 cursor-pointer group">
  <input
    type="radio"
    name="option"
    className="w-5 h-5 border-2 border-gray-300 text-indigo-600 focus:ring-4 focus:ring-indigo-100 transition-all"
  />
  <span className="text-gray-700 group-hover:text-gray-900">Option 1</span>
</label>
```

### Loading States

#### Skeleton Loader (Beautiful!)
```tsx
<div className="animate-pulse space-y-4">
  <div className="h-12 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 rounded-xl"></div>
  <div className="h-12 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 rounded-xl w-3/4"></div>
  <div className="h-12 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 rounded-xl w-1/2"></div>
</div>
```

#### Spinner (Smooth)
```tsx
<div className="flex items-center justify-center">
  <svg className="animate-spin h-8 w-8 text-indigo-600" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
  </svg>
</div>
```

#### Loading Card
```tsx
<div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
  <div className="animate-pulse space-y-4">
    <div className="flex items-center gap-4">
      <div className="w-12 h-12 bg-gray-200 rounded-xl"></div>
      <div className="flex-1 space-y-2">
        <div className="h-4 bg-gray-200 rounded w-1/4"></div>
        <div className="h-3 bg-gray-200 rounded w-1/2"></div>
      </div>
    </div>
    <div className="space-y-2">
      <div className="h-3 bg-gray-200 rounded"></div>
      <div className="h-3 bg-gray-200 rounded w-5/6"></div>
    </div>
  </div>
</div>
```

### Error States

#### Error Message (Inline)
```tsx
<div className="bg-rose-50 border-2 border-rose-200 rounded-xl p-4 flex items-start gap-3">
  <Icon className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
  <div>
    <h4 className="text-sm font-semibold text-rose-900 mb-1">Error</h4>
    <p className="text-sm text-rose-700">Something went wrong. Please try again.</p>
  </div>
</div>
```

#### Error Card
```tsx
<div className="bg-white rounded-2xl shadow-xl p-8 border-2 border-rose-200">
  <div className="flex flex-col items-center text-center">
    <div className="w-16 h-16 bg-rose-100 rounded-full flex items-center justify-center mb-4">
      <Icon className="w-8 h-8 text-rose-600" />
    </div>
    <h3 className="text-2xl font-bold text-gray-900 mb-2">Oops! Something went wrong</h3>
    <p className="text-gray-600 mb-6">We couldn't process your request. Please try again.</p>
    <button className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg">
      Try Again
    </button>
  </div>
</div>
```

### Empty States

#### Empty State (With Illustration)
```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <div className="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mb-6">
    <Icon className="w-12 h-12 text-gray-400" />
  </div>
  <h3 className="text-2xl font-bold text-gray-900 mb-2">No items yet</h3>
  <p className="text-gray-600 mb-6 max-w-md">
    Get started by creating your first item. It only takes a few seconds!
  </p>
  <button className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg">
    Create First Item
  </button>
</div>
```

---

## Animation Patterns

### Hover Effects
```tsx
// Scale up (buttons, cards)
className="transform hover:scale-105 transition-transform duration-200"

// Lift up (cards)
className="transform hover:-translate-y-1 transition-transform duration-200"

// Scale + lift (interactive cards)
className="transform hover:scale-105 hover:-translate-y-1 transition-all duration-200"

// Shadow increase (depth)
className="shadow-lg hover:shadow-2xl transition-shadow duration-300"

// Background change
className="bg-white hover:bg-gray-50 transition-colors duration-200"
```

### Entrance Animations (Framer Motion)
```tsx
import { motion } from 'framer-motion';

// Fade in from bottom
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: "easeOut" }}
>
  Content
</motion.div>

// Fade in with scale
<motion.div
  initial={{ opacity: 0, scale: 0.95 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>

// Stagger children (lists)
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    visible: { transition: { staggerChildren: 0.1 } }
  }}
>
  {items.map(item => (
    <motion.div
      key={item.id}
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
      }}
    >
      {item}
    </motion.div>
  ))}
</motion.div>
```

### Focus Animations
```tsx
// Ring on focus (inputs, buttons)
className="focus:ring-4 focus:ring-indigo-100 transition-all"

// Border on focus (inputs)
className="border-2 border-gray-200 focus:border-indigo-500 transition-colors"

// Combined (best practice)
className="border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all"
```

---

## Responsive Design Rules

### Mobile-First Approach
```tsx
// Base: Mobile (default)
// sm: 640px (small tablets)
// md: 768px (tablets)
// lg: 1024px (desktops)
// xl: 1280px (large desktops)

<div className="px-4 sm:px-6 lg:px-8">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {/* Responsive grid */}
  </div>
</div>
```

### Typography Responsive
```tsx
// Headings scale with screen size
<h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold">
  Responsive Heading
</h1>

// Body text
<p className="text-base lg:text-lg text-gray-600">
  Readable on all devices
</p>
```

### Padding/Margin Responsive
```tsx
// Tighter on mobile, spacious on desktop
<div className="p-4 md:p-8 lg:p-12">

// Smaller gaps on mobile
<div className="space-y-4 md:space-y-6 lg:space-y-8">
```

---

## Accessibility Built-In

### Semantic HTML
```tsx
// ✅ GOOD: Semantic
<button>Click</button>
<nav>Navigation</nav>
<main>Content</main>
<header>Header</header>

// ❌ BAD: Non-semantic
<div onClick={...}>Click</div>
```

### ARIA Labels
```tsx
// Icon-only buttons
<button aria-label="Close modal">
  <XIcon className="w-5 h-5" />
</button>

// Form inputs
<input
  type="email"
  aria-label="Email address"
  aria-describedby="email-error"
/>
<p id="email-error" className="text-rose-600">Invalid email</p>
```

### Keyboard Navigation
```tsx
// Focus visible
className="focus:outline-none focus:ring-4 focus:ring-indigo-300"

// Tab index for custom components
<div role="button" tabIndex={0} onKeyPress={handleKeyPress}>
  Custom clickable
</div>
```

### Color Contrast (WCAG AA)
```tsx
// ✅ GOOD: High contrast
<div className="bg-white text-gray-900">  // 21:1 ratio

// ✅ GOOD: Adequate contrast
<div className="bg-gray-100 text-gray-800">  // 7:1 ratio

// ❌ BAD: Low contrast
<div className="bg-gray-100 text-gray-400">  // 2.5:1 ratio (fails AA)
```

---

## Complete Page Examples

### Login Page (Lovable Quality)
```tsx
<div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center p-4">
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="w-full max-w-md"
  >
    <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
      {/* Logo */}
      <div className="flex justify-center mb-8">
        <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center">
          <Logo className="w-8 h-8 text-white" />
        </div>
      </div>

      {/* Heading */}
      <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
        Welcome Back
      </h1>
      <p className="text-center text-gray-600 mb-8">
        Sign in to your account to continue
      </p>

      {/* Form */}
      <form className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            type="email"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            type="password"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all"
            placeholder="••••••••"
          />
        </div>

        <div className="flex items-center justify-between">
          <label className="flex items-center gap-2">
            <input type="checkbox" className="w-4 h-4 border-2 border-gray-300 rounded checked:bg-indigo-600" />
            <span className="text-sm text-gray-600">Remember me</span>
          </label>
          <a href="#" className="text-sm text-indigo-600 hover:text-indigo-700 font-medium">
            Forgot password?
          </a>
        </div>

        <button className="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200">
          Sign In
        </button>
      </form>

      {/* Footer */}
      <p className="mt-8 text-center text-sm text-gray-600">
        Don't have an account?{' '}
        <a href="#" className="text-indigo-600 hover:text-indigo-700 font-semibold">
          Sign up
        </a>
      </p>
    </div>
  </motion.div>
</div>
```

---

## Summary: The Lovable/Bolt Formula

### 1. Always Use Gradients (Not Flat)
- `bg-gradient-to-r from-X to-Y` for buttons, backgrounds
- `bg-gradient-to-br from-X via-Y to-Z` for page backgrounds

### 2. Proper Spacing (Multiples of 4)
- 4, 8, 12, 16, 24, 32, 48, 64
- Use `space-y-8` for comfortable vertical spacing

### 3. Modern Rounded Corners
- `rounded-xl` (12px) for most components
- `rounded-2xl` (16px) for cards
- `rounded-full` for avatars, badges

### 4. Beautiful Shadows
- `shadow-xl` for cards
- `shadow-2xl` for modals
- Hover: `hover:shadow-2xl` for depth

### 5. Smooth Animations
- `transition-all duration-200` for most hovers
- `transition-shadow duration-300` for shadow changes
- Framer Motion for entrance animations

### 6. Accessibility
- Always use semantic HTML
- Add ARIA labels for icon-only buttons
- Use `focus:ring-4` for visible focus
- Ensure color contrast meets WCAG AA

**Result**: Stunning, modern UIs that users love! 🎨
