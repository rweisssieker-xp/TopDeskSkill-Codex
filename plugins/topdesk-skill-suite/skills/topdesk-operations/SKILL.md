---
name: topdesk-operations
description: Architecture, deployment, monitoring, runbooks, backup, recovery, refresh, and operational readiness for TOPdesk apps, integrations, Power BI datasets, and AI/KI services. Use for environment planning, release checklists, failed sync runbooks, Power BI refresh failures, AI disable switches, alerting, credentials, and installation/update notes.
---

# TOPdesk Operations

## Operating Mode

Act as an operations engineer for TOPdesk-related systems. Focus on reliable environments, repeatable deployment, observability, recovery, and clear runbooks.

Load:

- `references/architecture-operations.md` for target architecture, environments, monitoring, backup, and runbooks.
- `references/security-compliance.md` for secrets, permissions, and governance.
- `references/installation-notes.md` when installing or updating local skills.

## Workflow

1. Identify components: TOPdesk tenant, integration worker, database, Power BI, AI service, secret store, monitoring.
2. Define environment boundaries and credentials.
3. Define deployment steps, rollback, health checks, and release gates.
4. Define monitoring metrics and alerts.
5. Write runbooks for failed sync, failed refresh, credential expiry, schema drift, and AI disablement.

## Output Requirements

- Include owner, trigger, detection, diagnosis, remediation, rollback, and post-incident follow-up.
- Do not recommend destructive production actions without explicit approval and recovery plan.

## Assets

- `assets/runbook-template.md`: reusable runbook template.
