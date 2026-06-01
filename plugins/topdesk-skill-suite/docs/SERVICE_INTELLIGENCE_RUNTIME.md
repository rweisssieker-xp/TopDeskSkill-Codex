# Service Intelligence Runtime

The Service Intelligence Runtime is the operational layer for the TOPdesk Skill Suite. It connects the individual skills into a repeatable local run with connector preflight, approved data inputs, analyzer execution, run history, governance gates, and stakeholder readouts.

It is not a hosted SaaS service. It runs locally from approved exports by default. Optional live access requires tenant-controlled TOPdesk credentials and an explicit endpoint selection.

## What Is Now Implemented

- `topdesk-service-intelligence-runtime` skill.
- Runtime config example: `skills/topdesk-service-intelligence-runtime/assets/runtime-config.example.json`.
- Orchestrator CLI: `skills/topdesk-service-intelligence-runtime/scripts/run_service_intelligence.py`.
- Live connector helper: `skills/topdesk-service-intelligence-runtime/scripts/topdesk_live_connector.py`.
- Runtime operating model: `skills/topdesk-service-intelligence-runtime/references/runtime-operating-model.md`.
- Outputs: `runtime-plan.json`, `runtime-readout.md`, `runtime-dashboard.html`, `operational-gates.csv`, and `runtime-history.jsonl`.

## Operating Modes

| Mode | Purpose | Data Movement |
| --- | --- | --- |
| Dry run | Validate config, inputs, modules, and gates. | No analyzer execution. |
| Exports mode | Run analyzers from approved CSV files. | Local files only. |
| Connector preflight | Check required environment variables. | No TOPdesk data fetch. |
| Live export | Fetch one approved REST/OData endpoint to JSON or CSV. | Requires explicit credentials and endpoint. |

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

Export an approved endpoint:

```powershell
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\topdesk_live_connector.py export --endpoint /tas/api/incidents --out .\tenant-output\incidents.json --format json
```

## Runtime Run

Create a runtime config from the example, then run:

```powershell
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\run_service_intelligence.py --config .\runtime-config.json --out-dir .\tenant-output\runtime --dry-run
python .\plugins\topdesk-skill-suite\skills\topdesk-service-intelligence-runtime\scripts\run_service_intelligence.py --config .\runtime-config.json --out-dir .\tenant-output\runtime
```

## Governance Rules

- Keep credentials out of source files.
- Prefer approved exports until the customer has approved live endpoint use.
- Run PII review before sharing generated reports, screenshots, prompts, logs, or CSVs.
- Treat `runtime-dashboard.html` as local evidence unless sanitized for publication.
- Do not enable unattended scheduling until owner, retention, monitoring, disable path, and support model are documented.

## Remaining Product Deployment Decisions

These are outside the free plugin package and must be scoped per customer:

- Hosted scheduler or workflow runner.
- Managed secret store.
- Central database or object storage.
- Web application with multi-user auth.
- Monitoring and alerting.
- Support SLA and operating responsibility.

