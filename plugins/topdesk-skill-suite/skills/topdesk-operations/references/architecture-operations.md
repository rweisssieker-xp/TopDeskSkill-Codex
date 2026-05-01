# Architecture and Operations

Use this file for target architecture, deployment, environments, monitoring, backup, runbooks, and operational design.

## Reference Architecture

Typical components:

- TOPdesk tenant as operational service-management system.
- Integration worker for REST/OData/API sync.
- Operational app database for custom features and local state.
- Reporting warehouse or curated reporting schema.
- Power BI semantic model and reports.
- AI/KI service layer for classification, summarization, semantic search, and suggestions.
- Secret store for TOPdesk credentials, AI provider keys, database credentials, and Power BI gateway secrets.
- Observability stack for logs, metrics, traces, integration runs, and alerts.

Data flow:

1. TOPdesk API/OData/export provides operational data.
2. Integration worker normalizes data into local schema or warehouse.
3. Reporting views expose stable BI facts and dimensions.
4. Power BI imports or queries curated views.
5. AI/KI features read permitted records and write auditable suggestions.
6. Operators review suggestions before business-critical updates are applied to TOPdesk.

## Environments

Use separate environments:

- `dev`: synthetic or anonymized data.
- `test`: controlled integration with TOPdesk sandbox/test tenant when available.
- `staging`: production-like schema and refresh cadence, masked data where possible.
- `prod`: production tenant, production DB, monitored jobs, approved credentials.

Never test destructive TOPdesk updates against production without explicit approval and rollback.

## Deployment Checklist

- Migrations applied and reversible.
- Integration worker configured with least-privilege API user.
- Secrets loaded from approved secret store.
- Power BI dataset parameters point to the right environment.
- Gateway and scheduled refresh validated.
- AI prompts/model versions pinned.
- RLS/security tested with named users.
- Monitoring and alerts enabled.
- Runbook updated for failed sync, failed refresh, and AI disable switch.

## Monitoring

Track:

- Integration success/failure counts.
- Records read/written/skipped/failed.
- API latency, rate limits, authentication failures.
- Last successful sync timestamp per entity.
- Power BI refresh duration and failure reason.
- AI suggestion volume, acceptance, confidence, and error rate.
- Queue backlog, SLA risk, and near-breach incidents.

Alert on:

- No successful sync in expected window.
- Sudden drop/spike in imported records.
- Repeated API authentication failures.
- Power BI refresh failure.
- AI output validation failures.
- RLS/security test failure.

## Backup and Recovery

- Back up operational app database before schema migrations.
- Keep migration rollback scripts or forward-fix plan.
- Store integration checkpoints so failed syncs can resume safely.
- Keep raw import snapshots only as long as retention policy allows.
- Document restore time objective and restore point objective.

## Runbooks

Failed TOPdesk sync:

1. Check API credentials and tenant availability.
2. Check rate limits and response errors.
3. Review `integration_runs` and failed record details.
4. Retry idempotently from last successful checkpoint.
5. Escalate if schema/metadata changed.

Power BI refresh failure:

1. Check gateway status and credentials.
2. Check source schema changes.
3. Refresh staging queries.
4. Compare row counts after fix.
5. Publish only after validation checks pass.

AI disable switch:

1. Stop auto-apply paths first.
2. Keep suggest-only or fully disable by feature flag.
3. Preserve existing suggestions and audit records.
4. Notify operators if workflow controls change.
