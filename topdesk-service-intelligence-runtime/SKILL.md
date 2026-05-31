---
name: topdesk-service-intelligence-runtime
description: Operate the TOPdesk Service Intelligence workflow with connector checks, analyzer orchestration, run history, governance gates, and HTML/Markdown readouts.
license: MIT
---

# TOPdesk Service Intelligence Runtime

Use this skill when a user wants to move from individual TOPdesk accelerator scripts to an operational run: connector readiness, data inputs, analyzer execution, evidence outputs, governance gates, and repeatable reporting.

## What This Skill Provides

- Runtime configuration schema for local TOPdesk exports and optional live API/OData access.
- Connector preflight checks for `TOPDESK_BASE_URL`, `TOPDESK_USERNAME`, and `TOPDESK_APP_PASSWORD`.
- Orchestration for Tenant Drift, Process Debt, AI Adoption Ledger, Automation Sandbox, Readiness Scoring, Digital Twin Light, and Executive Narrative.
- Run history as JSONL so repeated executions can be compared.
- HTML and Markdown runtime readouts for stakeholders.
- Production gates that state what is ready, blocked, or requires tenant-specific credentials.

## Boundaries

- State hosted monitoring, SaaS operation, or unattended production execution only when the deployment, owner, scheduler, secret store, monitoring, and support model exist.
- Do not fetch live TOPdesk data unless the tenant has approved credentials, purpose, scope, and retention.
- Treat live connector use as tenant-specific. The plugin ships scripts and operating artifacts; the customer controls credentials and environment.

## Standard Workflow

1. Create or edit a runtime config from `assets/runtime-config.example.json`.
2. Run a dry plan first:

   ```bash
   python topdesk-service-intelligence-runtime/scripts/run_service_intelligence.py --config runtime-config.json --out-dir out/runtime --dry-run
   ```

3. Run connector preflight if live access is in scope:

   ```bash
   python topdesk-service-intelligence-runtime/scripts/topdesk_live_connector.py preflight
   ```

4. Execute the runtime against approved exports:

   ```bash
   python topdesk-service-intelligence-runtime/scripts/run_service_intelligence.py --config runtime-config.json --out-dir out/runtime
   ```

5. Review `runtime-readout.md`, `runtime-dashboard.html`, `runtime-plan.json`, `runtime-history.jsonl`, and `operational-gates.csv`.

## Inputs

The runtime config accepts these optional sections:

- `tenant`: Tenant name and environment label.
- `inputs`: CSV paths for catalogs, incidents, status transitions, assignment transitions, AI usage, automation scenarios, readiness checklist, baseline metrics, and digital-twin scenarios.
- `modules`: Boolean flags for the analyzers to run.
- `governance`: Owner, retention, PII policy, approval reference, and production gate state.
- `connector`: Optional live access mode. Keep `enabled` false until credentials and approval are ready.

## Outputs

- `runtime-plan.json`: resolved modules, inputs, blockers, and commands.
- `runtime-readout.md`: human-readable operating report.
- `runtime-dashboard.html`: local HTML dashboard for run status and gates.
- `operational-gates.csv`: gate-by-gate readiness evidence.
- `runtime-history.jsonl`: append-only run ledger.
