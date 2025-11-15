# Debugging Patterns Library

This document provides a comprehensive library of debugging patterns covering systematic debugging, root cause analysis, and log analysis.

## Systematic Debugging Patterns

### LOG FIRST Pattern

- Capture evidence before fixes
- Log full error context
- Record state at failure point
- Document reproduction steps

### Hypothesis-Driven Patterns

- Form hypotheses from evidence
- Test hypotheses systematically
- Validate fixes with tests
- Document findings

### Investigation Patterns

- Reproduce issues reliably
- Capture complete error messages
- Inspect recent changes
- Map observed to expected behavior

## Root Cause Analysis Patterns

### 5 Whys Pattern

- Ask "why" five times
- Trace to root cause
- Identify contributing factors
- Document causal chain

### Symptom-to-Cause Mapping

- Map symptoms to causes
- Identify root symptoms
- Trace symptom chains
- Document mappings

### Flow-Based Analysis

- Trace execution flows
- Identify flow breakpoints
- Map flow deviations
- Document flow paths

### Evidence-Based Analysis

- Gather evidence first
- Analyze evidence systematically
- Form conclusions from evidence
- Validate conclusions

## Log Analysis Patterns

### Flow Tracing Patterns

- Trace requests through logs
- Follow execution paths
- Identify log patterns
- Map log flows

### Pattern Comparison Patterns

- Compare working vs failing logs
- Identify pattern differences
- Correlate log events
- Document patterns

### Error Analysis Patterns

- Parse error logs
- Categorize errors
- Identify error patterns
- Trace error sources

### Performance Analysis Patterns

- Analyze performance logs
- Identify bottlenecks
- Measure execution times
- Document performance patterns

## Pattern Usage

Reference these patterns when debugging:

1. **Systematic Debugging**: Use LOG FIRST, hypothesis-driven approaches
2. **Root Cause Analysis**: Use 5 Whys, symptom-to-cause mapping, flow-based analysis
3. **Log Analysis**: Use flow tracing, pattern comparison, error analysis

## Pattern Composition

These patterns can be composed together:

- LOG FIRST + Root Cause Analysis = Evidence-based debugging
- Root Cause Analysis + Log Analysis = Comprehensive investigation
- Systematic Debugging + Log Analysis = Structured debugging

See `plugins/cc10x/skills/shared-patterns/PATTERN-COMPOSITION.md` for composition guidelines.
