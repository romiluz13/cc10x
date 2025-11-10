# Complexity Assessment

Complexity gate and rubric for plan/build workflows.

## Complexity Gate (Plan/Build)

If the complexity score is 2 or lower, warn that cc10x is optimized for higher-risk work and ask whether to proceed (yes/no). Pause until the user answers. Abort if the answer is "no" or no answer is provided.

## Complexity Rubric (1-5) - Functionality First

**Note**: Complexity scoring should consider functional complexity (user flows, system flows, integration flows) in addition to technical complexity.

### Base Scoring

- **1** - Single function (<50 LOC), no external dependencies, no test changes, no config changes, single user flow
- **2** - Single file (<200 LOC), trivial change, low risk, minimal test updates, simple user flow
- **3** - 2-5 files, moderate change, adds/updates tests, low/medium risk, some refactoring, multiple user flows or admin flow
- **4** - Multi-module change or new integration, notable risk/uncertainty, cross-file coordination needed, complex user/admin/system flows
- **5** - Cross-cutting or architectural impact, migrations/rollout considerations, breaking changes, complex multi-flow functionality

### Edge Case Handling

**Mixed Complexity**: If changes include both trivial and complex parts:

- Use the **highest score** (assume maximum risk)
- Document: "Mixed complexity detected: {trivial parts} and {complex parts}. Scoring: {highest score}"

**Unclear Architectural Impact**: If impact is uncertain:

- Default to **score 4** (assume risk exists)
- Ask user: "I cannot determine architectural impact. Is this change cross-cutting or isolated? (isolated=3, cross-cutting=4-5)"

**Refactor-Only Changes**: If no functional changes, only code structure:

- Score based on **file count** and **scope of refactor**
- Refactor within 1-2 files = score 2
- Refactor across 3-5 files = score 3
- Refactor across modules = score 4
- Large-scale architectural refactor = score 5

**Dependency Complexity**: Consider dependency changes:

- No new dependencies = no adjustment
- New dependency with clear migration path = +0.5 to score
- New dependency requiring significant integration = +1 to score
- Breaking dependency updates = +1.5 to score

**Calculation Method**: Start with base score, apply adjustments above, round to nearest integer (1-5).

### Examples

Example 1: "Add user registration form"

- 1 new component file, 1 API endpoint, tests = 3 files
- New database migration = moderate change
- **Score: 3**

Example 2: "Replace payment processor"

- Multiple files affected (payment service, config, tests)
- External API integration change = high risk
- **Score: 4**

Example 3: "Fix typo in comment"

- Single file, single line
- **Score: 1**

Example 4: "Refactor authentication across all modules"

- Multiple modules affected, architectural change
- **Score: 5**
