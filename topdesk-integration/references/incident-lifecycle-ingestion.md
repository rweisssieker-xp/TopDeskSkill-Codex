# Incident Lifecycle Ingestion

Use this pattern when TOPdesk reporting must show how long incidents spent in each status or operator group.

## Outputs

The ingestion script `scripts/sync_incident_lifecycle.py` writes:

- `incident_daily_snapshots.csv`: staging file for daily current-state snapshots.
- `incident_status_history.csv`: normalized status field-change events.
- `incident_assignment_history.csv`: normalized operator group/operator field-change events.
- `FactStatusTransition.csv`: Power BI-ready status intervals with sequence, valid-from, valid-to, and duration.
- `FactAssignmentTransition.csv`: Power BI-ready assignment intervals with sequence, valid-from, valid-to, and duration.
- `incident_lifecycle_import_report.md`: row-count and completeness report.

## Snapshot Mode

Run this daily even if full event history is not available.

```powershell
$env:TOPDESK_BASE_URL = "https://example.topdesk.net"
$env:TOPDESK_USERNAME = "api-user"
$env:TOPDESK_APP_PASSWORD = "<secret>"

python topdesk-integration\scripts\sync_incident_lifecycle.py `
  --out tenant-output\incident-lifecycle `
  --snapshot-date (Get-Date -Format yyyy-MM-dd) `
  --write-raw
```

Schedule it with Windows Task Scheduler, Azure Automation, Fabric pipeline, GitHub Actions with a secure secret store, or another controlled runner. Do not place credentials in source files.

## History Mode

When TOPdesk exposes a tenant-specific history, audit, action, or field-change endpoint, pass it explicitly:

```powershell
python topdesk-integration\scripts\sync_incident_lifecycle.py `
  --out tenant-output\incident-lifecycle `
  --history-endpoint "/verified/history/endpoint"
```

The endpoint name is intentionally not hard-coded. Verify the real endpoint, permissions, pagination, and field names for the target TOPdesk tenant first.

## Export Mode

For offline testing or one-off migration profiling:

```powershell
python topdesk-integration\scripts\sync_incident_lifecycle.py `
  --incidents-json tenant-output\snapshots\incidents.json `
  --history-json tenant-output\snapshots\incident-history.json `
  --out tenant-output\incident-lifecycle `
  --snapshot-date 2026-05-09
```

## Power BI Import

Use `topdesk-powerbi/assets/topdesk-lifecycle-powerquery.pq` as the Power Query template. Create a text parameter `LifecycleImportRoot` pointing to the output folder, then create separate queries for:

- `FactIncidentDailySnapshot`
- `FactStatusTransition`
- `FactAssignmentTransition`

Prefer SQL/reporting views in production when available. CSV imports are useful for proof-of-value, tenant discovery, and simple scheduled file drops.

## Validation

- Compare incident counts with a TOPdesk selection for the snapshot date.
- Check whether history events exist for tickets known to have changed status or group.
- Reconcile same-day changes; snapshots cannot see multiple changes between two runs.
- Confirm whether durations should use calendar hours or business/SLA calendars.

