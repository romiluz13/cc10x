# Parallel Execution Strategy

Dependency analysis and parallel execution safety validation.

## Parallel Execution Strategy

**Dependency Analysis Protocol**:

1. **Build Dependency Graph**: For each workflow phase:
   - Identify all operations (subagents, skills, components, bugs)
   - Map dependencies: operation A → operation B (B requires A's output)
   - Map conflicts: operation A ⚠️ operation B (shared state, same files)
2. **Execution Mode Selection**:

   **PARALLEL (Safe)**:
   - ✅ No output dependencies (operation B doesn't need operation A's output)
   - ✅ Read-only operations (no state mutations)
   - ✅ Isolated contexts (separate subagent contexts)
   - ✅ Independent data (different files/components/bugs)
   - ✅ Validation after each (prevents error propagation)

   **SEQUENTIAL (Required)**:
   - ❌ Output → Input dependency (A's output feeds B's input)
   - ❌ State mutation → Read dependency (A mutates, B reads)
   - ❌ Validation gates (must wait for validation)
   - ❌ Feedback loops (B can trigger return to A)
   - ❌ Shared state (both modify same data)

3. **Workflow-Specific Parallel Execution Rules**:
   - **Review Workflow**: Analysis subagents (analysis-risk-security, analysis-performance-quality, analysis-ux-accessibility) CAN run in parallel IF comprehensive review (read-only, independent, isolated contexts)
   - **Plan Workflow**: Planning subagents MUST run sequentially (planning-architecture-risk → planning-design-deployment, architecture informs design)
   - **Build Workflow**: Component subagents MUST run sequentially per component (component-builder → code-reviewer → integration-verifier), but components can run in parallel IF independent
   - **Debug Workflow**: Bug subagents MUST run sequentially per bug (bug-investigator → code-reviewer → integration-verifier), but bugs can run in parallel IF independent
   - **Validate Workflow**: No subagents (direct comparisons)

4. **Conflict Prevention Rules**:
   - Read-only subagents analyzing SAME code → PARALLEL (safe)
   - Subagents mutating DIFFERENT files → PARALLEL (safe)
   - Subagents with output dependencies → SEQUENTIAL (required)
   - Subagents in same workflow phase → Check dependencies first

5. **Fallback Strategy**:
   - If parallel execution fails → Automatically fallback to sequential
   - Log fallback reason for debugging
   - Continue with remaining operations

## Parallel Execution Safety Validation

**Conflict Detection Checklist** (before parallel execution):

- [ ] No output dependencies (operation B doesn't need A's output)
- [ ] No shared state mutations (operations don't modify same data)
- [ ] Read-only operations (no write conflicts)
- [ ] Isolated contexts (separate subagent contexts)
- [ ] Validation gates (validation occurs after all complete)
- [ ] Error isolation (failure of one doesn't corrupt others)

**Fallback Triggers**:

- Any conflict detected → Automatically fallback to sequential
- Parallel execution fails → Retry sequentially
- User preference for sequential → Honor user choice
- Complexity threshold exceeded → Sequential for safety
