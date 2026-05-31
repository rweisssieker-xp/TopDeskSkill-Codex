# Service Intelligence Runtime Operating Model

The runtime turns the TOPdesk skill suite into a repeatable local operating process. It does not require hosted infrastructure. It can run from approved CSV exports, and it can check live connector readiness when tenant credentials are available.

## Operating Cadence

| Cadence | Activity | Output | Owner |
| --- | --- | --- | --- |
| Per setup | Connector and data evidence preflight | `operational-gates.csv` | TOPdesk application manager |
| Weekly | Process debt, SLA, drift, and automation-risk checks | Analyzer folders under the run output | Service desk lead |
| Monthly | Readiness, AI adoption, executive narrative | `runtime-readout.md` and `runtime-dashboard.html` | Service intelligence owner |
| Per change | Automation sandbox and tenant drift comparison | Go/No-Go evidence | Change owner |

## Production Gates

- **Credential gate**: named API user or app password is configured outside source control.
- **Scope gate**: API/OData endpoints and exported files are approved for the stated purpose.
- **PII gate**: fields are minimized, masked, or approved before AI or external sharing.
- **Reconciliation gate**: KPI counts reconcile against TOPdesk UI or controlled exports.
- **Automation gate**: trigger, payload, idempotency, retry, rollback, audit, and owner are documented.
- **Operations gate**: run owner, retention, logs, disable path, and escalation path are defined.

## Runtime Modes

- **Exports mode**: run all modules from customer-approved CSV exports. This is the default and safest operating mode.
- **Preflight mode**: verify environment variables and URL shape without exporting data.
- **Live fetch mode**: fetch selected REST/OData endpoints into local files after tenant approval. This requires explicit credentials and endpoint selection.

## Evidence Boundary

The runtime produces local evidence packs. It does not imply continuous monitoring, production automation, or hosted storage. Those capabilities require a separate deployment decision, secret store, scheduler, monitoring, access model, and support agreement.

