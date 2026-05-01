# TOPdesk PowerShell Recipes

## OData Export Fetch

- Accept `-BaseUrl`, `-Endpoint`, `-OutFile`, and credential source.
- Build URLs from normalized pieces, not manual slash concatenation.
- Save raw export snapshots before transformation when the result supports reconciliation.
- Record row counts, timestamp, endpoint, and filter in a manifest JSON next to the export.

## Migration Batch Validation

- Read CSV with `Import-Csv -Encoding UTF8`.
- Validate required columns before row-level checks.
- Emit findings as objects with `Severity`, `Row`, `Field`, `Message`, and `SuggestedFix`.
- Write findings to CSV and JSON for both human review and automation.

## Power BI Refresh Runbook

- Keep tenant/workspace/dataset identifiers as parameters.
- Use environment variables or secure stores for tokens.
- Capture start/end timestamps, status, request id, and failure details.
- Produce a concise incident-ready summary.

## TOPdesk API Update

- Default to dry run.
- Batch requests with stable idempotency keys when the API supports them.
- Log external IDs and result statuses, not full PII payloads.
- Stop on schema mismatches before any remote write.

