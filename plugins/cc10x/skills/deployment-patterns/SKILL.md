name: deployment-patterns
description: Summarises deployment and rollback guidance for production releases. Use when planning a rollout, staging strategy, or recovery playbook; consult the detailed playbook for full procedures.
allowed-tools: Read, Grep, Glob
---

# Deployment Patterns

## Quick Start
- Identify release goals, environments, and constraints.
- Choose a rollout pattern (blue/green, canary, phased) based on risk and observability.
- Prepare a rollback plan and monitoring checklist before shipping.

## Checklist
- Define success metrics (latency, errors, business KPIs) and alert thresholds.
- Automate pre-deploy validations: migrations, feature flags, configuration diffs.
- Stage rollout steps with approval gates and communication owners.
- Document rollback triggers, commands, and time boxes.
- Capture verification evidence after each stage (pair with `verification-before-completion`).

## Using the Playbook
- For detailed runbooks, operational roles, and incident drills, read the [Deployment Playbook](PLAYBOOK.md).
- Includes templates for change tickets, rollback matrices, and environment readiness checks.

## Integration Points
- Coordinate with `planning-design-deployment` subagent outputs.
- Share metrics and alerts with `risk-analysis` and `log-analysis-patterns` to track residual risk.

## References
- [Deployment Playbook](PLAYBOOK.md)
- Related skills: `risk-analysis`, `verification-before-completion`, `integration-patterns`
