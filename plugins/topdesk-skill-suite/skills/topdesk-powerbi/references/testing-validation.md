# Testing and Validation for TOPdesk Workflows

Use this file for acceptance tests, migration checks, BI reconciliation, integration tests, and AI regression validation.

For deployment gates, runbooks, monitoring, and recovery procedures, load `architecture-operations.md`.

## Incident Workflow Tests

- Create incident from SSP with caller, branch, category, priority, and attachment.
- Create incident from email/API with missing optional fields.
- Assign to operator group and operator.
- Change status through normal lifecycle.
- Add public reply and internal note; verify visibility separation.
- Link asset and knowledge item.
- Close, reopen, and close again; verify status history and reopen count.
- Verify SLA target, pause/resume, breach, and escalation behavior.

## Change Workflow Tests

- Create standard change from template.
- Create extensive change with activities and approval.
- Assign activity to group/operator.
- Link incident and asset.
- Complete activities out of order if allowed; block if not allowed.
- Verify approval audit and final evaluation.

## Asset Tests

- Import asset with template/type and dynamic fields.
- Update owner/person and branch/location.
- Link asset to incident and change.
- Create asset relation and validate graph direction/type.
- Verify reporting view exposes BI-critical fields.

## Schema Migration Checklist

- Backfill required columns.
- Preserve external IDs and historical numbers.
- Add indexes for new filters and joins.
- Validate FK behavior on delete/update.
- Recompute reporting views.
- Run old and new report counts side by side.
- Verify rollback path for failed migration.

## Integration Tests

- Authenticate with dedicated API user.
- Pull one page and multiple pages.
- Handle rate limits/transient failures.
- Update an existing record idempotently.
- Detect duplicate external IDs.
- Log success and failure counts.
- Reconcile imported totals with TOPdesk export/OData.

## Power BI Validation

- Compare incident totals by created month.
- Compare open backlog by status.
- Compare closed incidents by closed month.
- Compare SLA compliance with TOPdesk report/selection.
- Validate RLS with branch/customer test users.
- Validate incremental refresh boundaries.
- Check hidden technical fields and PII exposure.

## PBIP/PBIR Validation

For generated report-as-code projects, validate both file contracts and actual Desktop behavior:

- Run `scripts/validate_topdesk_pbir_report.py --project <pbip-folder>`.
- Confirm the root `.pbip` has exactly one report artifact and no separate semantic-model artifact.
- Confirm `definition.pbir` binds the report to the semantic model with `datasetReference.byPath`.
- Confirm `pages/pages.json` uses `pageOrder` and has a valid `activePageName`.
- Confirm `version.json`, `report.json`, `page.json`, and every `visual.json` validate against their schemas.
- Confirm every visual field reference resolves to an existing TMDL table, column, or measure.
- Open the `.pbip` in Power BI Desktop and verify that page tabs are visible, the status bar reports the expected page count, and standard visuals render on the canvas.
- Record any Desktop-only warnings separately, especially Q&A deprecation prompts or missing custom visual messages for advanced visual types.

## AI Regression Tests

- Classification top-1/top-3 accuracy on historical tickets.
- Routing reassignment rate before/after.
- Sensitive ticket detection precision/recall.
- Reply draft citation coverage.
- Hallucination review on sampled replies.
- Semantic search permission leakage test.
- Multilingual/noisy ticket cases.
- Prompt/model version comparison before rollout.

## Release Gate

Before release, record:

- Environment and data source.
- Schema version/migration ID.
- Report version or app build.
- Test data set and date range.
- Pass/fail summary.
- Known risks and owner.
- PBIP/PBIR Desktop smoke-test evidence, including page count and unresolved visual warnings.
