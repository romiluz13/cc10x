---
name: progress-tracker
description: Tracks project progress by analyzing TODO lists and generates comprehensive status reports with velocity metrics, blocker identification, and completion estimates. Use when checking project status, generating progress summaries, or identifying bottlenecks.
license: MIT
---

# Progress Tracker Skill

Monitors task completion and generates comprehensive progress reports.

## When to Use

This skill is invoked when:
- User requests progress report ("What's the status?", "How are we doing?")
- Need to identify blockers
- Want velocity metrics
- Periodic status updates

## Workflow

1. **Read TODO.md** from `.claude/tasks/TODO.md`
2. **Count completed tasks** (checked boxes vs total)
3. **Identify blockers** (tasks marked as blocked or stuck)
4. **Calculate velocity** (tasks completed per session/day)
5. **Generate status report** with metrics and recommendations

## Report Format

```markdown
# Progress Report - [Date]

## Summary
- Total tasks: 25
- Completed: 18 (72%)
- In progress: 3 (12%)
- Blocked: 1 (4%)
- Pending: 3 (12%)

---

## Completed This Session
- ✅ Task 4: Implement auth service (<400 lines)
  - Status: Complete
  - LOC: 352 lines (within estimate)
  - Tests: 28 passing
  
- ✅ Task 5: Create login component (<200 lines)
  - Status: Complete
  - LOC: 187 lines (within estimate)
  - Tests: 15 passing
  
- ✅ Task 7: Write unit tests (>80% coverage)
  - Status: Complete
  - Coverage achieved: 94% (target was 80%)
  - Tests: 47 total, all passing

---

## Currently In Progress
- 🔄 Task 8: Integration tests (50% complete)
  - Started: Today
  - Estimated completion: Tomorrow
  - Blocker: None
  
- 🔄 Task 9: API documentation (in review)
  - Started: Today
  - Status: Draft complete, needs review
  
- 🔄 Task 6: Add validation utilities (70% complete)
  - Started: Yesterday
  - Remaining: Edge case tests

---

## Next Up (Priority Order)
- 📋 Task 10: README updates (high priority)
- 📋 Task 11: Deployment configuration (high priority)
- 📋 Task 12: Performance optimization (medium priority)

---

## Blockers

### Blocker 1: Third-Party API Integration

- **Task:** Task 13 (External API integration)
- **Type:** External dependency
- **Impact:** HIGH (blocks Tasks 14, 15)
- **Reported:** 2 days ago
- **Status:** Active
- **Owner:** External team
- **Action Required:** Daily follow-up with vendor
- **Alternative:** Mock implementation ready for testing
- **ETA:** 2 days
- **Mitigation:** Using mock API for development, will swap to real when ready

---

## Metrics

### Velocity
- Tasks completed today: 5
- Tasks completed this week: 18
- Average completion time: 2.3 hours/task
- Trend: ⬆️ Accelerating (was 3.1 hours/task last week)
- Estimated remaining time: 2 days (7 tasks × 2.3 hours / 8 hours per day)

### Quality Metrics
- Test coverage: 94% (target: >80%) ✅
- Linter errors: 0 ✅
- Files >500 lines: 0 ✅ (all within limit)
- Open review comments: 3 (minor, non-blocking)

### Phase Completion
- Phase 1 (Setup): 100% ✅ (3/3 tasks)
- Phase 2 (Core Implementation): 83% (5/6 tasks)
- Phase 3 (Testing): 60% (3/5 tasks)
- Phase 4 (Documentation): 20% (1/5 tasks)

---

## Risks & Concerns

### Risk 1: Testing Phase Behind Schedule

- **Severity:** 🔶 MEDIUM
- **Description:** Testing phase 1 day behind schedule
- **Impact:** May delay delivery by 1 day
- **Mitigation:** Allocate extra focus on integration tests, defer optimization
- **Action:** Complete Task 8 (integration tests) as top priority tomorrow

### Risk 2: API Integration Dependency

- **Severity:** 🔶 MEDIUM
- **Description:** External API keys still not received
- **Impact:** Blocks 2 tasks, affects final delivery if not resolved
- **Mitigation:** Using mock implementation for testing, can deploy without external integration
- **Action:** Escalate with vendor, prepare to launch with mock if necessary

---

## Recommendations

1. **Focus on completing integration tests** (Task 8) - Highest priority
2. **Start documentation in parallel** (Task 9-10 can proceed while testing)
3. **Escalate API blocker** (Task 13) - Daily follow-up with vendor
4. **Schedule code review session** for completed implementation
5. **Consider deploying with mock** if external API not ready

---

## Next Session Focus

**Top priorities for next session:**
1. Complete Task 8 (integration tests) - 2-3 hours
2. Resolve blocker for Task 13 (API keys) - follow-up
3. Start Task 10 (README documentation) - 1 hour

**Goal:** Reach 85% completion by end of session

---

## Trend Analysis

### This Week vs Last Week
- Completion rate: 72% (was 45%) - ⬆️ 60% improvement
- Tasks per day: 3.6 (was 2.3) - ⬆️ 57% improvement
- Average task time: 2.3 hours (was 3.1 hours) - ⬆️ 26% improvement

**Trend:** ✅ Accelerating - Team velocity increasing

### Projected Completion
Based on current velocity:
- Remaining tasks: 7
- Average time: 2.3 hours/task
- Working hours per day: 8 hours
- **Estimated completion: 2 days (Friday EOD)**

---

## Health Status

**Overall Project Health: ✅ ON TRACK**

**Green Indicators:**
- ✅ Velocity increasing
- ✅ Quality metrics all green
- ✅ No critical blockers
- ✅ Team morale high

**Yellow Indicators:**
- ⚠️ Testing phase slightly behind
- ⚠️ External dependency pending

**Red Indicators:**
- None

**Confidence Level:** HIGH - 85% confidence in Friday delivery
```

## Progress Analysis

### Calculate Completion Rate

```
Completion Rate = (Completed Tasks / Total Tasks) × 100

Example: 18 completed / 25 total = 72%
```

### Identify Trends

- **Accelerating:** Completion rate increasing over time (good!)
- **On Track:** Steady progress, predictable velocity
- **Slowing:** Completion rate decreasing (investigate causes)
- **Blocked:** No progress on critical path (escalate immediately)

### Estimate Completion

```
Remaining Time = (Remaining Tasks × Average Task Time) / Daily Working Hours

Example: (7 tasks × 2.3 hours) / 8 hours = 2.0 days
```

## Status Indicators

### Task Status Symbols

- ✅ Completed (checked box in TODO.md)
- 🔄 In Progress (mentioned in recent work)
- 📋 Pending (unchecked, not started)
- 🚫 Blocked (external dependency or issue)
- ⏸️ Paused (deprioritized temporarily)
- ❌ Cancelled (no longer needed)

### Priority Indicators

- 🔴 Critical (P0) - Must complete today
- 🟠 High (P1) - Should complete this week
- 🟡 Medium (P2) - Complete this sprint
- 🟢 Low (P3) - Nice to have

### Health Indicators

- ✅ On track (green) - Meeting targets, no issues
- ⚠️ At risk (yellow) - Slightly behind, manageable
- 🚨 Critical (red) - Significantly delayed, needs intervention

## Tracking Categories

### 1. Task Progress

Track individual tasks:
```markdown
### Task Details

Task 8: Integration tests
- Status: 🔄 In Progress (50%)
- Priority: 🟠 High (P1)
- Assignee: test-generator sub-agent
- Started: [Date]
- Est. Completion: Tomorrow
- Blockers: None
- Notes: API endpoint tests complete, auth flow tests in progress
```

### 2. Phase Progress

Track by development phase:
```markdown
### Phase Breakdown

Phase 2: Core Implementation (83% complete)
- Task 4: ✅ Complete (auth service)
- Task 5: ✅ Complete (login component)
- Task 6: 🔄 In Progress 70% (validation utilities)
- Task 7: ✅ Complete (unit tests)

Next task: Complete Task 6
Estimated phase completion: Tomorrow
```

### 3. Quality Metrics Dashboard

Track quality indicators:
```markdown
### Quality Dashboard

Code Quality:
- Linter errors: 0 ✅
- Type errors: 0 ✅
- Security vulnerabilities: 0 ✅
- File size violations: 0 ✅

Test Quality:
- Coverage: 94% ✅ (target >80%)
- Passing tests: 156/156 ✅
- Test execution time: 2.3s ✅
- Flaky tests: 0 ✅

Documentation:
- API docs: 80% complete
- README: 60% complete
- Inline comments: Good ✅
```

### 4. Velocity Tracking

Track team/individual velocity:
```markdown
### Velocity Metrics

This Week:
- Tasks completed: 18
- Average per day: 3.6
- Estimated remaining: 7 tasks
- Projected completion: Friday

Last Week:
- Tasks completed: 15
- Trend: ⬆️ +20% improvement

2-Week Average:
- 2.9 tasks per day
- Stable velocity ✅
```

## Blocker Management

### Blocker Template

```markdown
### Blocker: [Title]

- **Task Affected:** Task 13 (API integration)
- **Type:** External dependency / Technical / Resource / Decision
- **Severity:** High / Medium / Low
- **Impact:** Blocks 2 downstream tasks
- **Reported:** [Date]
- **Status:** Active / Resolved / Escalated
- **Owner:** External team / Internal developer
- **Action Required:** Daily follow-up with vendor
- **Alternative:** Mock implementation available
- **ETA:** 2 days
- **Escalation Path:** Manager if not resolved by [date]
```

### Blocker Types

- **Technical:** Code/architecture issues preventing progress
- **External:** Third-party dependencies, vendor delays
- **Resource:** Team capacity, availability issues
- **Decision:** Awaiting stakeholder input, approval needed
- **Environment:** Tooling, infrastructure, access issues

## Report Frequency

### Daily Standup Report (Quick)

```markdown
## Daily Update - [Date]

Yesterday:
- ✅ Completed: 3 tasks (Tasks 4, 5, 7)
- 🔄 Progress: 2 tasks (Tasks 6, 8)

Today:
- 🎯 Focus: Tasks 6, 8, 9
- ⏰ Goals: Complete integration tests, start documentation

Blockers:
- 🚫 Task 13: API keys still pending (escalating today)
```

### Weekly Status Report (Comprehensive)

```markdown
## Weekly Report - Week [N]

Summary: 72% complete, on track for Friday delivery

This Week:
- Completed: 18 tasks (was 10 last week)
- Quality: All metrics green ✅
- Risks: 2 medium (testing delay, API dependency)
- Velocity: +20% improvement

Next Week:
- Focus: Complete testing & documentation phases
- Goals: Reach 100% completion
- Deploy: Staging environment Thursday, production Friday
```

## Automated Tracking

### Reading TODO.md

Process:
1. Read `.claude/tasks/TODO.md`
2. Count total checkboxes (all tasks)
3. Count checked checkboxes (completed tasks)
4. Identify task dependencies (from "depends on" notes)
5. Extract phase information (from headings)
6. Note any blockers mentioned in task descriptions

### Calculating Metrics

For each phase:
1. Count phase tasks
2. Count completed tasks in phase
3. Calculate completion percentage
4. Identify bottlenecks (tasks stuck for >2 days)
5. Estimate remaining time (uncompleted × average velocity)

## Best Practices

1. **Update frequently** - Daily for active projects, weekly for maintenance
2. **Be honest** - Report actual status, not desired status
3. **Highlight blockers early** - Surface issues before they cascade
4. **Track trends** - Look for patterns (velocity increasing/decreasing)
5. **Celebrate wins** - Acknowledge completed work explicitly
6. **Adjust estimates** - Update based on actual velocity, not initial guesses
7. **Include context** - Explain why delays happen (not just "behind schedule")
8. **Provide recommendations** - Actionable next steps, not just metrics

## Integration with Orchestrator

When orchestrator receives "Show progress" or "Status update" request:

1. Load this skill
2. Read current `.claude/tasks/TODO.md`
3. Analyze completion status across all phases
4. Calculate velocity and quality metrics
5. Generate formatted progress report
6. Identify next priorities based on dependencies
7. Surface any blockers requiring attention
8. Provide actionable recommendations

## Remember

Progress tracking provides visibility and accountability. Good progress reports enable:
- **Early blocker identification** (prevents cascading delays)
- **Accurate estimates** (based on actual velocity, not guesses)
- **Team alignment** (everyone knows status)
- **Risk mitigation** (trends show issues before they're critical)

**Report honestly, update frequently, provide actionable recommendations.**

