---
name: risk-analysis
description: Provides a lightweight framework for identifying and mitigating risks across data flow, dependencies, UX, security, performance, and recovery. Use when planning features, reviewing code for risks, analyzing security vulnerabilities, assessing performance risks, or validating implementations to surface high-impact risks early.
allowed-tools: Read, Grep, Glob
---

# Risk Analysis

## Quick Start
- Map the system or feature using the seven-stage checklist (data flow, dependencies, timing, UX, security, performance, failure modes).
- Rate probability and impact for each risk, then record mitigations and owners.
- Escalate critical risks into the implementation plan or review report.

## Checklist Snapshot
- **Data Flow**: Validate input/output contracts, data retention, transformations.
- **Dependencies**: Identify external services, version locks, and fallback behaviour.
- **Timing/Concurrency**: Consider race conditions, locking, and idempotency.
- **UX & Accessibility**: Guard against confusing states or inaccessible flows.
- **Security & Compliance**: Enforce authn/authz, secrets handling, audit trails.
- **Performance & Scalability**: Document throughput assumptions, caching, load tests.
- **Failure & Recovery**: Define monitoring, rollback, incident response, and SLAs.

## Using the Playbook
- The comprehensive [Risk Analysis Playbook](PLAYBOOK.md) includes detailed questionnaires, scoring matrices, and sample mitigation plans.
- Reference it when creating risk registers or performing deep-dive audits.

## Integration Points
- Planning workflow: share top risks with `planning-architecture-risk` and `planning-design-deployment` outputs.
- Review workflow: summarise residual risks for the final report and highlight blockers.
- Build/debug workflows: ensure mitigations are verified before completion.

## References
- [Risk Analysis Playbook](PLAYBOOK.md)
- Related skills: `security-patterns`, `performance-patterns`, `verification-before-completion`
