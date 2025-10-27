# CC10x Quick Start

Get started with CC10x in 5 minutes and build your first feature with AI assistance.

## Installation

1. Copy `plugins/cc10x` to your Claude Code plugins directory
2. Reload Claude Code
3. Ready! Type `/plan` to verify installation

## Your First Feature (5 Minutes)

Let's build a complete feature from start to finish.

### Step 1: Plan (2 minutes)

```bash
/plan "Add user settings page with theme toggle"
```

**What happens:**
- Planner researches your codebase
- Applies 8-dimensions risk analysis
- Creates `PLAN.md` with:
  - Scope clarity ("What We're Doing" vs "NOT Doing")
  - Phases with automated/manual verification split
  - Pause points for your confirmation

**Review the plan** - Make adjustments if needed.

### Step 2: Build (10-30 minutes)

```bash
/build PLAN.md balanced
```

**What happens:**
- Builder implements Phase 1
- Runs automated checks:
  ```
  ✅ Tests: 15/15 passing
  ✅ Type check: Clean
  ✅ Lint: Clean
  ✅ Build: Success
  ```
- ⏸️ **PAUSES** - "Please verify feature works in UI"
- **You test and confirm**: "Looks good!"
- Builder continues to Phase 2
- Repeats for each phase...

### Step 3: Review (3 minutes)

```bash
/review src/settings/
```

**What happens:**
- 5 specialized reviewers analyze in parallel:
  - Security: Checks for vulnerabilities
  - Quality: Assesses maintainability
  - Performance: Finds bottlenecks
  - UX: Reviews user experience
  - Accessibility: Verifies WCAG compliance
- Consolidated report with prioritized findings

**Fix issues** and re-review until clean.

## Common Commands

### Planning
```bash
/plan "feature description"
```
Creates comprehensive implementation plan with risk analysis.

### Building
```bash
/build PLAN.md balanced
```
Implements with pause points and verification.

Strategies: `fast`, `balanced` (default), `tdd`

### Testing
```bash
/test src/module/ all
```
Writes comprehensive test coverage.

Strategies: `unit`, `integration`, `e2e`, `all`

### Debugging
```bash
/debug "error description or log file"
```
Systematic debugging with LOG FIRST methodology.

### Reviewing
```bash
/review src/feature/
```
5-agent parallel review in 3 minutes.

## The Workflow Pattern

Every feature follows this pattern:

```
/plan → PLAN.md → /build → Code → /review → Fixes → Production
         ↓                    ↓              ↓
    Research +          Phase-by-Phase  Parallel
    Risk Analysis       + Pause Points  Reviewers
```

## Tips for Success

### 1. Trust the Complexity Gate
If builder warns "manual coding is 16x cheaper," it's probably right. CC10x is for complex tasks.

### 2. Actually Test at Pause Points
When builder pauses for manual verification:
- Open the app
- Test the feature
- Check edge cases
- Confirm or report issues

Don't just say "continue" without testing!

### 3. Review Early
Don't wait until everything is done. Run `/review` after each major component to catch issues early.

### 4. Read Plans Carefully
Good plans save implementation time. Review them thoroughly and request changes before building.

### 5. Use the Right Strategy
- **fast**: Quick prototypes, experiments
- **balanced**: Production features (recommended)
- **tdd**: Critical business logic

## Understanding the Output

### When Planner Creates a Plan:
```markdown
## What We're Doing (In Scope)
- ✅ User settings page
- ✅ Theme toggle (light/dark)
- ✅ Persistent storage

## What We're NOT Doing (Out of Scope)
- ❌ Advanced theme customization
- ❌ Profile settings (separate)

## Phase 1: UI Components
### Automated Verification:
- [ ] Tests pass
- [ ] Type check clean

### Manual Verification:
- [ ] Page renders correctly
- [ ] Toggle works smoothly

⏸️ PAUSE before Phase 2
```

### When Builder Pauses:
```
⏸️ Phase 1 Complete - Ready for Manual Verification

Automated verification passed:
✅ Tests: 8/8 passing
✅ Type check: Clean
✅ Lint: Clean
✅ Build: Success

Please verify manually:
- [ ] Settings page appears in nav
- [ ] Theme toggle button visible
- [ ] Click toggle changes theme

Confirm to proceed to Phase 2?
```

### When Reviewers Report:
```
## Security Findings
🟢 No critical issues

## Quality Findings
🟡 MEDIUM: SettingsComponent is 85 lines, consider splitting

## Performance Findings
🟢 No issues

## UX Findings
🟡 LOW: Loading state not shown during save

## Accessibility Findings
🔴 HIGH: Theme toggle missing aria-label
```

## Common Scenarios

### Bug Fixing
```bash
/debug "Login button not working on mobile Safari"
```

Debugger will:
1. Add strategic logging
2. Analyze patterns
3. Find root cause
4. Implement fix
5. Add regression test

### Adding Tests
```bash
/test src/auth/login.ts unit
```

Tester writes comprehensive unit tests with edge cases.

### Quick Review
```bash
/review src/new-component.ts
```

Fast feedback from 5 specialized reviewers.

## Next Steps

- **Read full README**: `plugins/cc10x/README.md`
- **Explore agents**: Check `agents/` directory to see capabilities
- **Review skills**: See `skills/` for progressive knowledge libraries
- **Check integration docs**: `docs/integration/` for technical details

## Need Help?

- **Commands not working**: Verify installation, reload Claude Code
- **Agents not activating**: Commands auto-delegate, check agent files exist
- **Hooks not triggering**: Ensure `.sh` files are executable

See README.md for comprehensive documentation.

---

**Happy 10x Development!** 🚀

Start with `/plan "your feature"` and let CC10x guide you to production-ready code.

