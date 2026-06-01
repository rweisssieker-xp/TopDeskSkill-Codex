---
name: topdesk-tenant-drift
description: Compare TOPdesk tenant field catalogs, OData/API exports, option sets, categories, statuses, priorities, operator groups, and KPI dependency maps to detect drift risks for Power BI, AI/KI, automations, security, and operations.
---

# TOPdesk Tenant Drift

Use this skill when a user needs to compare two TOPdesk tenant evidence snapshots or explain why reports, AI prompts, automations, or KPI definitions may have changed meaning.

## Workflow

1. Identify baseline and current evidence: field catalogs, OData metadata exports, REST profile CSVs, option exports, category/status/group lists, or KPI dependency maps.
2. Run `scripts/compare_tenant_drift.py` when two CSV catalogs are available.
3. Classify changes by impact: Power BI, AI/KI, automation, security/privacy, and operations.
4. Produce a drift report with owner suggestion, recommended action, and validation metric.
5. Use the generated CSV and Markdown report as the tenant-drift evidence pack for review and remediation.

## Inputs

The script accepts CSV files with flexible column names. Best results use columns such as `entity`, `entity_set`, `table`, `field`, `property`, `name`, `type`, `label`, `nullable`, `required`, `option`, or `endpoint`.

## Outputs

- `tenant-drift-findings.csv`
- `tenant-drift-report.md`

## References

- Load `references/tenant-drift.md` for impact classes, output interpretation, and remediation patterns.
