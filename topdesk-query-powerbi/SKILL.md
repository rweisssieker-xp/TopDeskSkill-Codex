---
name: topdesk-query-powerbi
description: Translate TOPdesk business questions into tenant-safe OData filters, SQL/reporting-view queries, Power Query extraction plans, DAX measure definitions, validation checks, and Power BI report requirements. Use when combining TOPdesk queries with Power BI modelling, KPI semantics, reconciliation, data-quality checks, or report implementation tasks.
---

# TOPdesk Query Power BI

Use this skill to turn a TOPdesk reporting question into an implementable query-to-model specification.

## Workflow

1. Restate the business question as measurable facts, dimensions, filters, date logic, and grain.
2. Identify source path: TOPdesk OData, REST API, CSV export, SQL/reporting view, or warehouse.
3. Draft query artifacts in this order: source entity/table, filters, joins/navigation, incremental boundaries, output fields.
4. Define Power BI model impact: fact table, dimensions, relationships, DAX measures, RLS, refresh, validation.
5. Include reconciliation checks against TOPdesk UI selections, exports, or trusted source counts.
6. Flag tenant-specific assumptions: field names, status/category labels, SLA semantics, branch/customer security, and PII.

## References

- Load `references/query-to-powerbi.md` for translation patterns and output structure.
- Load `references/topdesk-query-examples.md` for common incident/change/asset/knowledge reporting questions.

## Assets

- Use `assets/query-powerbi-spec-template.md` for implementation specs.

## Scripts

- Use `scripts/new_query_powerbi_spec.py` to generate a starter spec from a business question.

