# Service Intelligence Runtime

The Service Intelligence Runtime is the operational layer for the TOPdesk Skill Suite. It connects the individual skills into a repeatable local run with connector preflight, approved data inputs, analyzer execution, run history, governance gates, and stakeholder readouts.

It is not a hosted SaaS service. It runs locally from approved exports by default. Optional live access requires tenant-controlled TOPdesk credentials and an explicit endpoint selection.

## What Is Now Implemented

- `topdesk-service-intelligence-runtime` skill.
- Runtime config example: `skills/topdesk-service-intelligence-runtime/assets/runtime-config.example.json`.
- Orchestrator CLI: `skills/topdesk-service-intelligence-runtime/scripts/run_service_intelligence.py`.
- Live connector helper: `skills/topdesk-service-intelligence-runtime/scripts/topdesk_live_connector.py`.
- Runtime operating model: `skills/topdesk-service-intelligence-runtime/references/runtime-operating-model.md`.
- Scheduler registration script: `skills/topdesk-service-intelligence-runtime/scripts/Register-ServiceIntelligenceSchedule.ps1`.
- Secret store CLI: `skills/topdesk-service-intelligence-runtime/scripts/topdesk_secret_store.py`.
- Local status server: `skills/topdesk-service-intelligence-runtime/scripts/service_intelligence_server.py`.
- Outputs: `runtime-plan.json`, `runtime-readout.md`, `runtime-dashboard.html`, `operational-gates.csv`, `runtime-history.jsonl`, optional SQLite state DB, and optional monitoring JSON.

## Operating Modes

| Mode | Purpose | Data Movement |
| --- | --- | --- |
| Dry run | Validate config, inputs, modules, and gates. | No analyzer execution. |
| Exports mode | Run analyzers from approved CSV files. | Local files only. |
| Connector preflight | Check required environment variables. | No TOPdesk data fetch. |
| Live export | Fetch one approved REST/OData endpoint to JSON or CSV. | Requires explicit credentials and endpoint. |
| Scheduled local run | Register the runtime as a Windows Scheduled Task. | Uses approved local config and environment. |
| Secret store | Protect TOPdesk credentials with Windows DPAPI. | Local encrypted JSON bound to the Windows user. |
| Local status server | Serve runtime health and run history. | Local HTTP endpoints backed by SQLite and monitoring JSON. |

## Required Environment Variables For Live Access

```powershell
$env:TOPDESK_BASE_URL = "https://your-tenant.topdesk.net"
$env:TOPDESK_USERNAME = "<username>"
$env:TOPDESK_APP_PASSWORD = "<application-password>"
```

Run preflight:

```powershell
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\topdesk_live_connector.py preflight
```

Write and use a local encrypted secret store:

```powershell
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\topdesk_secret_store.py set --store .\tenant-output\runtime\topdesk-secrets.dpapi.json
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\topdesk_live_connector.py preflight --secret-store .\tenant-output\runtime\topdesk-secrets.dpapi.json
```

Export an approved endpoint:

```powershell
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\topdesk_live_connector.py export --endpoint /tas/api/incidents --out .\tenant-output\incidents.json --format json
```

## Runtime Run

Create a runtime config from the example, then run:

```powershell
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\run_service_intelligence.py --config .\runtime-config.json --out-dir .\tenant-output\runtime --dry-run
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\run_service_intelligence.py --config .\runtime-config.json --out-dir .\tenant-output\runtime
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\run_service_intelligence.py --config .\runtime-config.json --out-dir .\tenant-output\runtime --state-db .\tenant-output\runtime\service-intelligence.sqlite --monitoring-json .\tenant-output\runtime\runtime-monitoring.json
```

Register a local schedule after governance approval:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\Register-ServiceIntelligenceSchedule.ps1 -ConfigPath .\runtime-config.json -OutDir .\tenant-output\runtime -StateDb .\tenant-output\runtime\service-intelligence.sqlite -MonitoringJson .\tenant-output\runtime\runtime-monitoring.json -WhatIf
```

Serve the local dashboard and API:

```powershell
$env:SERVICE_INTELLIGENCE_ADMIN_TOKEN = "<local-admin-token>"
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\service_intelligence_server.py --state-db .\tenant-output\runtime\service-intelligence.sqlite --monitoring-json .\tenant-output\runtime\runtime-monitoring.json
```

Endpoints:

- `GET /health`
- `GET /api/runs`
- `GET /api/modules`
- `GET /dashboard`

## Governance Rules

- Keep credentials out of source files.
- Use the DPAPI secret store or a customer-managed secret tool for scheduled local operation.
- Prefer approved exports until the customer has approved live endpoint use.
- Run PII review before sharing generated reports, screenshots, prompts, logs, or CSVs.
- Treat `runtime-dashboard.html` as local evidence unless sanitized for publication.
- Enable local scheduling only after owner, retention, monitoring, disable path, and support model are documented.

## Customer-Owned Enterprise Extensions

The local plugin now includes runtime execution, local scheduling, DPAPI secret storage, SQLite state, monitoring JSON, and a local HTTP status server. Enterprise extensions that depend on customer infrastructure are scoped per customer:

- Customer-managed vault integration.
- Central multi-user database or object storage.
- Multi-user web application with organization auth.
- Enterprise monitoring and alerting integration.
- Support SLA and operating responsibility.

