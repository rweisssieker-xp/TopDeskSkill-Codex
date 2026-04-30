# Operations Handbook

Audience: operations owners and support engineers.

## Components

- TOPdesk tenant.
- Integration worker.
- Reporting database.
- Power BI dataset/report.
- AI/KI service.
- Secret store.
- Monitoring/alerting.

## Standard Runbooks

Failed sync:

1. Check TOPdesk availability and credentials.
2. Check latest integration run.
3. Inspect failed records.
4. Retry from checkpoint.
5. Escalate schema drift if fields changed.

Failed Power BI refresh:

1. Check gateway and credentials.
2. Check source schema changes.
3. Run dataset refresh manually in test.
4. Reconcile row counts.
5. Publish after validation.

AI disable:

1. Disable auto-apply first.
2. Keep audit records.
3. Notify operators.
4. Review recent suggestions.

## Monitoring

- Sync success.
- Refresh success.
- API errors.
- Reconciliation deltas.
- AI validation errors.
- SLA backlog and near breaches.
