# Service Intelligence Runtime Operating Model

The runtime turns the TOPdesk skill suite into a repeatable local operating process. It does not require hosted infrastructure. It can run from approved CSV exports, and it can check live connector readiness when tenant credentials are available.

## Operating Cadence

| Cadence | Activity | Output | Owner |
| --- | --- | --- | --- |
| Per setup | Connector and data evidence preflight | `operational-gates.csv` | TOPdesk application manager |
| Weekly | Process debt, SLA, drift, and automation-risk checks | Analyzer folders under the run output | Service desk lead |
| Monthly | Readiness, AI adoption, executive narrative | `runtime-readout.md` and `runtime-dashboard.html` | Service intelligence owner |
| Per change | Automation sandbox and tenant drift comparison | Go/No-Go evidence | Change owner |
| Scheduled local run | Windows Scheduled Task executes the runtime with approved config. | SQLite state DB and monitoring JSON | Runtime owner |
| Local status server | HTTP server exposes run status and dashboard from local state. | `/health`, `/api/runs`, `/api/modules`, `/dashboard` | Runtime owner |

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
- **Scheduled local mode**: use `Register-ServiceIntelligenceSchedule.ps1` to run the runtime on a controlled Windows host.
- **Local status server mode**: use `service_intelligence_server.py` to expose health and run status from SQLite and monitoring JSON.

## Persisted State

When `--state-db` is supplied, the runtime writes `runtime_runs` and `module_runs` tables to SQLite. This gives operators a queryable local ledger for run status, module status, output directories, stderr, blockers, and the full plan JSON.

When `--monitoring-json` is supplied, the runtime writes a compact status document with overall status, connector status, blocker count, module status counts, red gates, amber gates, and evidence paths.

## Secret Store

`topdesk_secret_store.py` writes `TOPDESK_BASE_URL`, `TOPDESK_USERNAME`, and `TOPDESK_APP_PASSWORD` from environment variables into a local Windows DPAPI-protected JSON file. The encrypted values are bound to the Windows user context that created them. `topdesk_live_connector.py` can read that store with `--secret-store`.

## Local API

`service_intelligence_server.py` reads the SQLite state database and monitoring JSON. It serves:

- `/health`: current status and state-file presence.
- `/api/runs`: recent runtime runs.
- `/api/modules`: module results.
- `/dashboard`: browser-readable operational status.

Set `SERVICE_INTELLIGENCE_ADMIN_TOKEN` to require `Authorization: Bearer <token>` for requests.

## Evidence Boundary

The runtime produces local evidence packs, persisted local state, monitoring status files, and a local status API. Multi-user storage, organization-wide monitoring, and support SLAs require customer infrastructure, access model, and support agreement decisions.

