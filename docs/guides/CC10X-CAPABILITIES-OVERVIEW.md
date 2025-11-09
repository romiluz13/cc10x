# CC10X Capabilities Overview

## Core Orchestrator

**Title**: cc10x-orchestrator  
**Description**: Primary orchestrator that interprets user intent via explicit keyword mapping, selects workflows (review/plan/build/debug/validate), applies complexity gates (1-5 scale), coordinates subagents with dependency analysis, enforces evidence-first verification, and manages memory integration. Handles intent disambiguation, workflow existence verification, skill loading verification, subagent invocation rules (sequential/parallel), error recovery protocol (5-minute timeout), and memory cleanup.  
**Trigger**: Automatically activated on any user request in Claude Code when cc10x plugin is installed.  
**Orchestrator Integration**: Central coordinator; all workflows and subagents flow through it. Uses deterministic keyword mapping for intent detection, complexity rubric for gating, and unified parallel loading strategy for skills.

---

## Workflow 1: REVIEW

**Title**: Review Workflow - Evidence-Based Code Analysis  
**Description**: Multi-dimensional code analysis covering security (OWASP Top 10 via security-patterns), performance bottlenecks (N+1 queries, O(n\*n) loops, memory leaks), code quality (complexity, duplication, SOLID principles), UX friction points (missing feedback, confusing flows), and WCAG accessibility compliance (keyboard navigation, focus management, aria labeling). Produces findings grouped by severity (critical/high/medium/low) with file:line citations and remediation steps tied to skill guidance. Includes conflict resolution protocol for subagent disagreements, file size sanity checks (>500 lines), and scope validation (warns if <50 lines).  
**Trigger**: Keywords: "review", "audit", "quality check", "security audit", "analyze code", "code review", "assess", "evaluate", "inspect", "examine"  
**Orchestrator Integration**:

- Loads 9 required skills in parallel (all independent): project-context-understanding (MANDATORY), risk-analysis, security-patterns, performance-patterns, code-quality-patterns, ux-patterns, accessibility-patterns, verification-before-completion (MANDATORY), memory-tool-integration
- Conditionally loads: ui-design (if UI components detected), design-patterns (if design patterns mentioned), integration-patterns (if integration code detected), api-design-patterns (if API code detected), web-fetch-integration (if external standards needed)
- Invokes 3 subagents: analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility
  - **Parallel execution** for general/comprehensive reviews (all 3 read-only, isolated contexts, no dependencies)
  - **Single subagent** for focused reviews (security-focused → only analysis-risk-security, performance-focused → only analysis-performance-quality, UX-focused → only analysis-ux-accessibility)
- Applies scope size validation (warns if single file <50 lines or single function <20 lines)
- Uses memory for review patterns (top 3 highest-confidence, semantic matching via jq)
- Caches external standards documentation (Q&A pairs, 72h TTL for standards)
- Checkpoint system saves state after each phase for resumption

---

## Workflow 2: PLAN

**Title**: Planning Workflow - Structured Feature Design  
**Description**: Transforms requirements into complete planning artifacts. Includes requirements intake with completeness threshold (gates if >3 critical questions unanswered), architecture design (system context, container view, component breakdown, data models, integration points), risk analysis (7-stage framework: data flow, dependencies, timing, UX, security, performance, failure modes), API design (endpoints, schemas, authentication), component design (component tree, state management, interfaces), implementation roadmap (phases with file manifest and dependencies), testing strategy (unit/integration/E2E with coverage targets), and deployment strategy (build steps, monitoring, rollback triggers). Includes conflict resolution protocol for subagent disagreements and implementability checks (dependencies, feasibility, circular dependencies).  
**Trigger**: Keywords: "plan", "design", "architect", "create plan", "roadmap", "strategy", "architecture", "system design", "feature design"  
**Orchestrator Integration**:

- Loads 8 required skills in parallel (all independent): project-context-understanding (MANDATORY), requirements-analysis, feature-planning (MANDATORY), design-patterns (MANDATORY), architecture-patterns (MANDATORY), risk-analysis (MANDATORY), verification-before-completion (MANDATORY), memory-tool-integration
- Conditionally loads: ui-design (if UI features mentioned), api-design-patterns (if API planning detected), component-design-patterns (if component planning detected), web-fetch-integration (if external docs needed)
- Invokes 2 subagents sequentially (architecture → design dependency): planning-architecture-risk FIRST, then planning-design-deployment SECOND
- Applies complexity gate (warns if score <=2, requires explicit yes/no)
- Uses memory for complexity patterns (semantic match by signature: file_count, change_type, has_external_deps)
- Fetches external API/service documentation with Q&A caching (24h TTL for API specs, 48h for framework docs)
- Checkpoint system saves state after each phase

---

## Workflow 3: BUILD

**Title**: Build Workflow - TDD-Driven Implementation  
**Description**: Enforces strict TDD discipline (RED → GREEN → REFACTOR) for each component. Handles component identification, dependency-aware ordering (builds dependency graph, detects circular dependencies), component execution loop (component-builder → code-reviewer → integration-verifier per component, sequential within component, parallel between independent components), failure cascading (blocks dependent components if dependency fails), review feedback classification (blocking/important/suggestions), and aggregate verification (regression suite, coverage checks, build/lint). Includes file size sanity checks (>500 lines triggers refactor recommendation).  
**Trigger**: Keywords: "build", "implement", "create", "write", "code", "develop", "make", "add feature", "implement feature", "build feature"  
**Orchestrator Integration**:

- Loads 9 required skills in parallel (all independent): project-context-understanding (MANDATORY), requirements-analysis, security-patterns, code-quality-patterns (MANDATORY), code-generation (MANDATORY), component-design-patterns (MANDATORY), test-driven-development, verification-before-completion, memory-tool-integration
- Conditionally loads: ui-design (MANDATORY when UI components detected), design-patterns (if building APIs/components/integrations), performance-patterns (if performance-critical code detected), web-fetch-integration (if external docs needed)
- Invokes 3 subagents sequentially per component: component-builder → code-reviewer → integration-verifier (must remain sequential within component, parallelization applies BETWEEN components)
- Applies complexity gate (warns if score <=2)
- Uses memory for component orders (validates dependency_hash matches current deps), failure modes (high success_rate >60%), and build patterns
- Fetches library/framework documentation with Q&A caching (48h TTL for library docs)
- Checkpoint system saves state after each component

---

## Workflow 4: DEBUG

**Title**: Debug Workflow - Root Cause First  
**Description**: Systematic bug investigation using LOG FIRST methodology (gather logs/metrics before guessing). Includes bug classification (reproducible/intermittent/non-reproducible/external/performance/functional), bug independence analysis (parallel for independent bugs, sequential for related bugs), investigation timeout (3 attempts max, then escalation), root cause analysis (hypothesis formation, evidence gathering), targeted fix implementation (minimal changes), regression test writing (RED before fix, GREEN after), and escalation paths (additional logging, user-provided data, external dependency investigation). Includes bug type skill selection (performance-patterns for performance bugs, security-patterns for security bugs, integration-patterns for integration bugs).  
**Trigger**: Keywords: "debug", "fix", "error", "bug", "investigate", "failure", "broken", "issue", "problem", "troubleshoot", "diagnose"  
**Orchestrator Integration**:

- Loads 7 required skills in parallel (all independent): project-context-understanding (MANDATORY), systematic-debugging, log-analysis-patterns, root-cause-analysis, test-driven-development, verification-before-completion, memory-tool-integration
- Conditionally loads: performance-patterns (performance bugs), security-patterns (security bugs), integration-patterns (integration bugs), code-quality-patterns (code quality bugs), web-fetch-integration (if external resources needed)
- Invokes 3 subagents sequentially per bug: bug-investigator → code-reviewer → integration-verifier (must remain sequential within bug)
- Uses memory for failure modes (semantic match by error_pattern regex, top 3 highest success_rate >60%), fix patterns
- Fetches error documentation with Q&A caching (48h TTL for error docs)
- Checkpoint system saves state after each bug investigation

---

## Workflow 5: VALIDATE

**Title**: Validation Workflow - Cross-Artifact Consistency  
**Description**: Verifies alignment between plan, code, tests, and documentation. Includes plan vs code comparison (drift classification: intentional/accidental/missing/extra), code vs tests verification (coverage thresholds: unit 70% min/80% target, integration 50% min/60% target, E2E critical flows), coverage gap analysis (critical/important/acceptable gaps), edge case coverage verification, and documentation freshness verification (extracts code contracts: API endpoints, function signatures, data models, compares with docs, scores: fresh/stale/missing/incorrect). Produces alignment matrix (requirement → code → test → doc mapping) and drift analysis.  
**Trigger**: Keywords: "validate", "verify", "check", "confirm implementation", "alignment check", "consistency check"  
**Orchestrator Integration**:

- Loads 5 required skills in parallel (all independent): project-context-understanding (MANDATORY), requirements-analysis, test-driven-development (MANDATORY), verification-before-completion, memory-tool-integration
- Conditionally loads: code-quality-patterns (if code quality validation needed)
- No subagents (direct analysis by workflow)
- Uses memory for validation preferences
- Handles missing plan scenarios (options: run planning workflow first / code-only validation / user provides plan manually)

---

## Subagent 1: analysis-risk-security

**Title**: Security & Risk Analysis Subagent  
**Description**: Analyzes code for security vulnerabilities (OWASP Top 10: injection, broken authentication, sensitive data exposure) and architectural risks. Maps data flows and trust boundaries using risk-analysis stages. Inspects authentication, authorization, validation, secrets management, and dependency usage. Records risks with probability/impact ratings (1-5 scale) and concrete mitigations. Highlights missing controls or monitoring hooks. Produces findings grouped by severity with file:line citations and evidence snippets. Includes "Residual Risk" section summarizing remaining concerns.  
**Trigger**: Invoked by REVIEW workflow (always for security-focused reviews, parallel with others for general reviews)  
**Orchestrator Integration**: Receives scoped files and user notes, loads risk-analysis and security-patterns skills, outputs Security Findings and Architectural Risks sections with severity levels.

---

## Subagent 2: analysis-performance-quality

**Title**: Performance & Quality Analysis Subagent  
**Description**: Identifies performance problems (N+1 DB queries, O(n\*n) loops, memory leaks, bundle bloat) and code quality issues (high-complexity functions, duplication, unclear naming, SOLID violations). Includes grep or profiling commands if run, with outputs. Suggests targeted refactors with before/after sketches. Notes improvements already present. Produces Performance Findings and Quality Findings sections with severity levels, file:line citations, impact descriptions, and recommendations tied to skill guidance. Includes "Open Questions" section if clarification needed.  
**Trigger**: Invoked by REVIEW workflow (always for performance-focused reviews, parallel with others for general reviews)  
**Orchestrator Integration**: Receives scoped files and user notes, loads performance-patterns and code-quality-patterns skills, outputs Performance Findings and Quality Findings sections.

---

## Subagent 3: analysis-ux-accessibility

**Title**: UX & Accessibility Analysis Subagent  
**Description**: Evaluates UI components for usability and WCAG 2.1 AA compliance. Traces user journeys, identifies friction (missing states, unclear copy, confusing flows), applies WCAG guidance (semantics, focus management, color contrast, assistive tech support). References design-system expectations if they exist. Produces UX Findings and Accessibility Findings sections with severity levels, file:line citations, user consequence descriptions, and specific recommendations. Includes "Positive Observations" list when notable strengths exist.  
**Trigger**: Invoked by REVIEW workflow (always for UX-focused reviews, parallel with others for general reviews)  
**Orchestrator Integration**: Receives scoped files and user notes, loads ux-patterns and accessibility-patterns skills, outputs UX Findings and Accessibility Findings sections.

---

## Subagent 4: planning-architecture-risk

**Title**: Architecture & Risk Planning Subagent  
**Description**: Transforms requirements into architecture and risk insights. Creates system context (external actors and relationships), container view (major containers: services, databases, UIs with responsibilities), component breakdown (components with responsibilities, interfaces, dependencies, data), data models (entities with fields, types, relationships, constraints), data flow (source → transformations → sink), and integration points (external services with contracts and failure handling). Applies 7-stage risk analysis (data flow, dependency, timing, UX, security, performance, failure mode risks) with probability/impact scores (1-5 scale), mitigation strategies, and owners. Produces Architecture Summary and Risk Register with mandatory template format. Documents assumptions and open questions.  
**Trigger**: Invoked by PLAN workflow (FIRST, sequentially before planning-design-deployment)  
**Orchestrator Integration**: Receives requirements summary from Phase 1, loads architecture-patterns and risk-analysis skills, outputs architecture and risk register for design subagent.

---

## Subagent 5: planning-design-deployment

**Title**: Design & Deployment Planning Subagent  
**Description**: Builds on requirements and architecture outputs to deliver implementation roadmap. Creates API design (endpoints with HTTP methods, auth requirements, request/response schemas, rate limiting, caching, versioning), component design (component tree, state management approach, props/interfaces, reusability), implementation roadmap (phases with components, file manifest, dependencies, estimates), testing strategy (unit/integration/E2E mapped to requirements with coverage targets), and deployment strategy (build steps, environment configuration, database migrations, monitoring setup, rollback triggers and procedure). Produces Design & Deployment Plan with mandatory template format. Cross-references requirements, aligns with architecture, respects dependencies.  
**Trigger**: Invoked by PLAN workflow (SECOND, sequentially after planning-architecture-risk, receives architecture outputs)  
**Orchestrator Integration**: Receives requirements and architecture outputs, loads api-design-patterns, component-design-patterns, deployment-patterns, and verification-before-completion skills, outputs complete design plan.

---

## Subagent 6: component-builder

**Title**: Component Builder Subagent  
**Description**: Implements single component using strict TDD discipline. Restates component contract (props, API, side effects). Writes failing test first (RED) demonstrating desired behaviour, runs test and captures failing output. Implements minimal code to pass test (GREEN), re-runs test suite to confirm. Refactors for clarity while keeping tests green (REFACTOR). Checks accessibility or UI states if relevant. Produces updated/new source files with clear separation of concerns, test files proving behaviour, and Verification Summary with commands run, exit codes, and artefacts. Constraints: one component per invocation, no completion without seeing test fail then pass, surfaces open questions instead of guessing.  
**Trigger**: Invoked by BUILD workflow (FIRST in sequence per component, before code-reviewer)  
**Orchestrator Integration**: Receives component brief, loads component-design-patterns, code-generation, test-driven-development, and verification-before-completion skills, outputs TDD cycle evidence and implementation.

---

## Subagent 7: code-reviewer

**Title**: Code Reviewer Subagent  
**Description**: Reviews code changes for correctness, maintainability, and risk. Summarizes change and intent. Inspects for correctness, style, security (AuthN/AuthZ flows, input validation/output encoding, secrets handling, injection risks), performance (N+1 queries, nested loops, unnecessary re-renders), code quality (complexity, duplication, naming, error handling), and test completeness. References specific skill guidance for each observation. Flags blockers versus suggestions. Confirms whether existing tests cover the change. Produces Review Summary (intent, status: Approve with changes / Changes requested), Critical Findings, Important Findings, Suggestions, and Positive Notes when appropriate. Cites exact line numbers and explains risk.  
**Trigger**: Invoked by BUILD workflow (after component-builder) and DEBUG workflow (after bug-investigator)  
**Orchestrator Integration**: Receives code changes, loads code-quality-patterns, security-patterns, performance-patterns, and verification-before-completion skills, outputs review findings that can block or allow progression.

---

## Subagent 8: integration-verifier

**Title**: Integration Verifier Subagent  
**Description**: Validates integrations across components, APIs, and external services. Restates integration scenario (inputs, expected outcome, error paths). Executes or describes necessary integration tests (API calls, end-to-end flows, background jobs). Captures command output or logs to prove success or highlight failures. Identifies regressions or missing coverage. Produces timeline of tests run with command/output snippets, pass/fail status per scenario with evidence, and recommendations for additional monitoring or testing. Constraints: no success assumption without logs or test output, requests environment setup if missing rather than fabricating results.  
**Trigger**: Invoked by BUILD workflow (after code-reviewer) and DEBUG workflow (after code-reviewer)  
**Orchestrator Integration**: Receives component/bug context, loads integration-patterns, test-driven-development, log-analysis-patterns, and verification-before-completion skills, outputs integration test results.

---

## Subagent 9: bug-investigator

**Title**: Bug Investigator Subagent  
**Description**: Investigates single bug using systematic debugging. Restates observed behaviour vs expected result. Follows LOG FIRST mandate: gathers logs, traces, metrics before guessing. Reproduces bug (if not reproducible, stops and requests more data). Forms single hypothesis, implements minimal fix, writes regression test that fails before fix. Re-runs regression suite to prove fix, captures command output. Summarizes root cause narrative with evidence (log excerpts, stack traces), code changes and regression tests, Verification Summary with commands/exit codes, and follow-up actions (monitoring, clean-up, debt). Constraints: no speculative fixes without evidence, one bug per pass, requests orchestration if additional issues exist.  
**Trigger**: Invoked by DEBUG workflow (FIRST in sequence per bug, before code-reviewer)  
**Orchestrator Integration**: Receives bug context (reproduction steps, logs, error messages), loads systematic-debugging, log-analysis-patterns, root-cause-analysis, test-driven-development, and verification-before-completion skills, outputs root cause and fix with evidence.

---

## Supporting Capability 1: Memory Tool Integration

**Title**: Memory Tool Integration  
**Description**: Filesystem-based memory system (`.claude/memory/`) that stores complexity patterns (with signature: file_count, change_type, has_external_deps, has_security; predicted_score, actual_scores array, accuracy percentage, usage_count, confidence: high/medium/low), failure modes (error_pattern regex, root_causes array with cause/fix/success_rate/occurrences/last_seen), component orders (order array, success_rate, dependency_graph, validated_deps_hash), and user preferences (explicit only, never inferred). Uses semantic matching via jq (not exact text), top-N retrieval (top 3 highest-confidence), pattern validation after workflow (compare predicted vs actual, update accuracy, increment usage_count), and automatic cleanup (delete if accuracy <50% after 3+ uses, delete if unused >60 days, keep top 20 most accurate). NOTE: Anthropic Memory Tool API NOT available in Claude Code - uses filesystem-based approach. MCP memory servers available if configured.  
**Trigger**: Used automatically by all workflows before complexity scoring (query patterns) and after completion (store patterns, validate accuracy, run cleanup)  
**Orchestrator Integration**: Integrated into orchestrator Phase 0 (before complexity: load patterns once, cache for workflow duration, semantic match, top 3 only) and Phase 5 (after completion: validate patterns, update accuracy/confidence, store only validated patterns, run cleanup script).

---

## Supporting Capability 2: Web Fetch Integration

**Title**: Web Fetch Integration  
**Description**: Smart Q&A pair caching system for external documentation. Claude Code WebFetch requires BOTH `url` and `prompt` parameters, returns summarized answers (not raw content), uses 15-minute server-side caching. Caches Q&A pairs (not raw content) with hash-based deduplication (`{url}_{prompt}` hash), TTL-based expiration (API specs: 24h, library docs: 48h, framework docs: 48h, standards: 72h), cache corruption detection (validates cache_index.json JSON syntax, validates answer files exist, rebuilds index if corrupted), and graceful fallback (uses stale cache if fetch fails). Cache structure: `.claude/memory/web_cache/cache_index.json` maps `{url, prompt}` → cached answer file with TTL. Used for API specifications (targeted questions: endpoints, authentication, data models, error handling), library documentation (setup, patterns, integration), and standards/guidelines (OWASP, coding standards).  
**Trigger**: Used automatically when workflows detect external dependencies (APIs, services, frameworks, libraries mentioned)  
**Orchestrator Integration**: Integrated into orchestrator Phase 0 (external resource check: check cache first, use if valid TTL, re-fetch if expired, fetch if not cached, ask user permission before fetching) and workflow-specific phases (planning: API specs, build: library docs, review: standards, debug: error docs).

---

## Supporting Capability 3: Verification Before Completion

**Title**: Verification Before Completion  
**Description**: Evidence-first gate that blocks success claims without fresh verification. Core rule: "No success claims without fresh, local evidence collected after the latest change." Required actions: identify behaviour/acceptance criteria to prove, run necessary commands (tests, lint, build, manual reproduction) on current branch, capture command/arguments/exit code/essential output, map evidence to each acceptance criterion and edge case, produce Verification Summary before communicating completion. Verification Summary template includes: Scope, Criteria, Commands (with exit codes), Evidence (log/report snippets), Risks/Follow-ups. Red flags: missing output/exit codes, edge cases not exercised, reliance solely on remote CI, language like "should/probably/seems" replaces evidence.  
**Trigger**: Used automatically by all workflows before final reports (orchestrator Phase 5: result compilation)  
**Orchestrator Integration**: Invoked by orchestrator Phase 5 (result compilation) to validate all completion claims. All workflows must invoke this skill before presenting final results. All subagents include Verification Summary in their hand-off.

---

## Supporting Capability 4: Workflow State Persistence

**Title**: Workflow State Persistence  
**Description**: Checkpoint system that saves workflow state after each phase to `.claude/memory/workflow_state/{workflow}_{timestamp}.json`. Checkpoint format includes: workflow name, phase name, timestamp, state (files reviewed, subagents completed, findings, components, bugs, etc.), next_phase. Resume logic: reads most recent checkpoint (sorted by timestamp), validates checkpoint state (files present, subagents valid, components present), continues from next_phase with checkpoint state restored, asks user "Resuming from Phase {N}. Continue from checkpoint or restart?". Checkpoint triggers: after Phase 0, Phase 1, Phase 2 (after each subagent/component/bug), Phase 3, Phase 4 completion. Context restoration: if resuming after compaction or context unclear, uses checkpoint system; if no checkpoint, reads `.claude/memory/snapshots/` most recent snapshot and `.claude/memory/WORKING_PLAN.md` as fallback.  
**Trigger**: Automatically saves checkpoints after each workflow phase  
**Orchestrator Integration**: Integrated into all workflows for state persistence and restoration. Used when resuming after interruption or context compaction.

---

## Supporting Capability 5: Complexity Gating

**Title**: Complexity Gating  
**Description**: Complexity assessment using 1-5 scale rubric. Base scoring: 1 (single function <50 LOC, no external deps), 2 (single file <200 LOC, trivial change), 3 (2-5 files, moderate change), 4 (multi-module change, notable risk), 5 (cross-cutting impact, breaking changes). Edge case handling: mixed complexity uses highest score, unclear architectural impact defaults to score 4, refactor-only changes scored by file count/scope, dependency complexity adds +0.5 to +1.5. If complexity score <=2 for plan/build workflows, warns that cc10x is optimized for higher-risk work, presents lightweight warning script, waits for explicit yes/no approval, aborts if "no" or no answer.  
**Trigger**: Applied automatically in PLAN and BUILD workflows (Phase 0: complexity gate)  
**Orchestrator Integration**: Part of orchestrator Phase 0 (complexity gate) with explicit user approval required. Uses memory patterns as reference before scoring.

---

## Supporting Capability 6: Error Recovery Protocol

**Title**: Error Recovery Protocol  
**Description**: Standardized error handling with structured format. Provides: Context (what was attempted with evidence: file paths, commands run, error messages), Problem (what failed: specific error, exit code, failure point), Options (clear choices: Retry if transient error likely, Continue without {component} if optional, Abort workflow if critical failure, Custom user instructions), Impact (what each choice means), Default (recommended action: Abort for critical failures, Retry for transient, Continue without component for optional). Error Recovery Timeout: 5 minutes waiting for user response, timeout behavior (critical failures → Abort, transient failures → Retry once, optional failures → Continue without component), timeout notification and logging to `.claude/memory/workflow_history.json`. Critical rules: never fabricate outputs for missing agents, wait for explicit user decision, proceed with default after timeout.  
**Trigger**: Activated automatically when any skill/subagent/workflow fails  
**Orchestrator Integration**: Defined in orchestrator Phase 6 (failure handling) and used by all workflows. Applied when skill loading fails, subagent fails, workflow fails, or verification fails.
