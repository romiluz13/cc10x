---
name: safe-refactoring
description: Performs behavior-preserving code improvements including formatting, import organization, unused code removal, function extraction, variable renaming, and safe structural transformations without changing functionality. Use when cleaning up code after implementation, organizing imports, removing unused exports, simplifying complex functions through extraction, renaming for clarity, or improving code structure while keeping tests green. Emphasizes safety (tests must pass before and after), incremental changes (one refactoring at a time), and reversibility (can revert if tests break). Loaded when refactoring tasks needed or by quality-reviewer when suggesting code improvements. Critical principle tests must remain green throughout refactoring process.
license: MIT
---

# Safe Refactoring

## Progressive Loading Stages

### Stage 1: Metadata (startup - ~50 tokens)
- **Skill**: Safe Refactoring
- **Purpose**: Automatically apply safe, behavior-preserving improvements
- **When**: Auto-fix phase of code review, pre-commit hooks
- **Core Rule**: Run tests after EVERY change - rollback on failure
- **Sections Available**: Safe Fixes, Unsafe Fixes, Checkpoint Strategy

---

### Stage 2: Quick Reference (triggered - ~500 tokens)

#### Safe vs Unsafe Refactorings

```
✅ SAFE (Auto-fixable):
- [ ] Formatting (Prettier, ESLint --fix)
- [ ] Import sorting
- [ ] Unused variable/import removal
- [ ] const vs let (when immutable)
- [ ] Missing semicolons
- [ ] Whitespace normalization

❌ UNSAFE (Manual only):
- [ ] Renaming public APIs
- [ ] Logic changes
- [ ] Complex refactorings
- [ ] Database schema changes
- [ ] Breaking changes
```

#### Checkpoint-Driven Strategy

```
For each safe fix:
1. Apply change
2. Run tests
3. Tests pass? → Commit change
4. Tests fail? → Rollback, report
5. Continue with next fix
```

#### Safe Refactoring Examples

**Import Sorting**:
```typescript
// Before
import { z } from 'zod';
import React from 'react';
import { Button } from './Button';
import fs from 'fs';

// After (sorted: stdlib → external → internal)
import fs from 'fs';

import React from 'react';
import { z } from 'zod';

import { Button } from './Button';
```

**Unused Variables**:
```typescript
// Before
function calculateTotal(items) {
  const tax = 0.1; // Unused!
  const discount = 0;
  return items.reduce((sum, item) => sum + item.price, 0);
}

// After
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**const vs let**:
```typescript
// Before
let userId = req.user.id; // Never reassigned
let total = calculateTotal(); // Never reassigned

// After
const userId = req.user.id;
const total = calculateTotal();
```

---

### Stage 3: Detailed Guide (on-demand - ~2000 tokens)

## Safe Refactorings (Auto-fixable)

### 1. Formatting

**Tools**: Prettier, ESLint --fix

```bash
# Apply formatting
npx prettier --write "src/**/*.{ts,tsx,js,jsx}"

# Apply ESLint auto-fixes
npx eslint --fix "src/**/*.{ts,tsx,js,jsx}"
```

**Safe changes**:
- Indentation normalization
- Semicolon insertion
- Quote style (single vs double)
- Trailing commas
- Line breaks

**Why safe**: No behavior change, only formatting

### 2. Import Organization

**Sort imports**:
```typescript
// Before: Random order
import { Button } from './components/Button';
import React, { useState } from 'react';
import { z } from 'zod';
import path from 'path';

// After: Organized
// 1. Node.js built-ins
import path from 'path';

// 2. External packages
import React, { useState } from 'react';
import { z } from 'zod';

// 3. Internal modules
import { Button } from './components/Button';
```

**Tools**:
```bash
# Using eslint-plugin-import
npm install --save-dev eslint-plugin-import
```

**Why safe**: Doesn't change what's imported, only order

### 3. Unused Code Removal

**Unused imports**:
```typescript
// Before
import React from 'react';
import { useState, useEffect } from 'react'; // useEffect unused

// After
import React from 'react';
import { useState } from 'react';
```

**Unused variables**:
```typescript
// Before
function processOrder(order) {
  const timestamp = Date.now(); // Unused
  const userId = order.userId;
  return saveOrder(order);
}

// After
function processOrder(order) {
  const userId = order.userId;
  return saveOrder(order);
}
```

**Detection**:
```bash
# TypeScript unused variables
tsc --noUnusedLocals --noUnusedParameters

# ESLint
npx eslint src/ --rule 'no-unused-vars: error'
```

**Why safe**: Unused code can't affect behavior

### 4. Variable Declaration (const vs let)

```typescript
// Before
let config = loadConfig(); // Never reassigned
let data = await fetchData(); // Never reassigned

// After
const config = loadConfig();
const data = await fetchData();
```

**Detection**:
```bash
# ESLint prefer-const rule
npx eslint --fix --rule 'prefer-const: error'
```

**Why safe**: const doesn't change behavior, just prevents reassignment

### 5. Missing Type Annotations (TypeScript)

```typescript
// Before
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// After
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Why safe**: TypeScript infers types anyway, adding explicit types doesn't change behavior

## Unsafe Refactorings (Manual Only!)

### ❌ Never Auto-fix These

**1. Renaming**:
```typescript
// ❌ DON'T auto-rename public APIs
export function getUserById(id) {} // Used by external consumers

// Risk: Breaking changes for API consumers
```

**2. Logic Changes**:
```typescript
// ❌ DON'T change logic automatically
if (user.age > 18) {} // Should this be >= 18?

// Risk: Behavior change could introduce bugs
```

**3. Complex Refactorings**:
```typescript
// ❌ DON'T auto-refactor complex code
function processPayment(order, user, settings) {
  // 150 lines of complex logic
}

// Risk: High chance of breaking something
```

**4. Database/Schema Changes**:
```typescript
// ❌ DON'T auto-modify database queries
db.query('SELECT * FROM users'); // Should optimize?

// Risk: Performance regression, data corruption
```

**5. Authentication/Authorization**:
```typescript
// ❌ DON'T auto-modify security code
if (user.role === 'admin') {} // Extremely sensitive

// Risk: Security vulnerability
```

## Checkpoint-Driven Refactoring

**Strategy**: Apply one change at a time, test, commit

```typescript
async function applyRefactorings(fixes) {
  for (const fix of fixes) {
    try {
      // 1. Apply change
      applyFix(fix);

      // 2. Run tests
      const testsPass = await runTests();

      if (testsPass) {
        // 3. Commit if tests pass
        await git.commit(`refactor: ${fix.description}`);
        console.log(`✅ Applied: ${fix.description}`);
      } else {
        // 4. Rollback if tests fail
        await git.checkout('--', fix.files);
        console.log(`❌ Rolled back: ${fix.description} (tests failed)`);
      }
    } catch (error) {
      // 5. Rollback on any error
      await git.checkout('--', fix.files);
      console.log(`❌ Error: ${fix.description}`);
    }
  }
}
```

**Benefits**:
- Each change is isolated
- Test failures don't affect other fixes
- Easy to see what broke tests
- Can continue after rollback

## Pre-commit Hook Integration

**.husky/pre-commit**:
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Format staged files
npx prettier --write $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|tsx|js|jsx)$')

# Lint and auto-fix
npx eslint --fix $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|tsx|js|jsx)$')

# Re-add files (in case formatting changed them)
git add $(git diff --cached --name-only)

# Run tests
npm test
```

**Why useful**: Automatic safe fixes before every commit

## Safety Checklist

Before auto-fixing:
- [ ] All tests currently passing
- [ ] Git working directory clean
- [ ] Only safe refactorings selected

During auto-fixing:
- [ ] Apply one change at a time
- [ ] Run tests after each change
- [ ] Commit on success, rollback on failure

After auto-fixing:
- [ ] Review changes (git diff)
- [ ] Ensure all tests still pass
- [ ] No unintended behavior changes

## Common Safe Fixes

| Fix | Tool | Safe? | Risk |
|-----|------|-------|------|
| Formatting | Prettier | ✅ Yes | None |
| Import sorting | ESLint | ✅ Yes | None |
| Unused vars | ESLint | ✅ Yes | None |
| const vs let | ESLint | ✅ Yes | None |
| Missing semicolons | ESLint | ✅ Yes | None |
| Renaming | Manual | ❌ No | Breaking changes |
| Logic changes | Manual | ❌ No | Bugs |
| Complex refactor | Manual | ❌ No | Behavior change |

## References

- [Refactoring: Improving the Design of Existing Code](https://refactoring.com/)
- [Working Effectively with Legacy Code](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)
- [Prettier](https://prettier.io/)
- [ESLint](https://eslint.org/)

---

**Remember**: "If it ain't tested, it's broken." Run tests after EVERY auto-fix!
