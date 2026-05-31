---
name: topdesk-powerbi
description: Build, review, and validate Power BI reporting for TOPdesk data. Use for TOPdesk dashboards, semantic models, DAX measures, Power Query/OData extraction, row-level security, KPI definitions, report pages, reconciliation against TOPdesk selections/exports, refresh design, and BI data-quality checks.
---

# TOPdesk Power BI

## Operating Mode

Act as a Power BI modeler for TOPdesk service-management data. Prefer star schemas, explicit KPI definitions, stable reporting views, and validated counts over ad hoc visuals.

Start by loading:

- `references/powerbi.md` for model design, KPI definitions, and report pages.
- `references/powerbi-recipes.md` for DAX, Power Query, RLS, wireframes, and validation recipes.
- `references/powerbi-advanced.md` for detailed dataset architecture, DAX catalogs, OData patterns, RLS, deployment, refresh, and reconciliation.
- `references/powerbi-kpi-catalog.md` for KPI definitions across incidents, changes, assets, knowledge, AI, and data quality.
- `references/powerbi-report-spec-template.md` for report/page specifications and required report pages.
- `references/powerbi-model-review.md` for reviewing existing PBIX/model documentation.
- `references/powerbi-template-snippets.md` for reusable DAX and Power Query snippets.
- `references/powerbi-build-maintain.md` for generating and maintaining Power BI implementation packs.
- `references/glossary-data-dictionary.md` when naming or KPI semantics matter.
- `references/testing-validation.md` when validating counts, refresh, RLS, or release readiness.

## Workflow

1. Identify data source: TOPdesk OData, API export, CSV, SQL view, warehouse, or custom app database.
2. Define fact grain before writing DAX.
3. Map dimensions: date, branch, caller/person, operator, operator group, category, priority, status, source, asset type.
4. Define KPI semantics: created, closed, backlog, SLA compliance, first response, resolution, reopen, reassignment.
5. Design RLS before publishing any report with person, branch, or customer data.
6. Reconcile Power BI counts against TOPdesk selections/exports or trusted SQL/OData queries.

## Output Requirements

- Include model layout, relationships, measures, page layout, filters, RLS, refresh, and validation notes.
- Treat sample OData/table names as placeholders until verified against the target tenant.
- Call out PII exposure and branch/customer security risks.
- For PBIP/PBIR output, document the Desktop preview settings, schema/file contract, generated page count, visual count, and any Desktop-only visual warnings.

## Assets

- `assets/topdesk-core-measures.dax`: reusable DAX measure template.
- `assets/topdesk-lifecycle-powerquery.pq`: Power Query templates for lifecycle snapshot, status transition, and assignment transition CSV imports.
- `assets/topdesk-odata-functions.pq`: reusable Power Query helper snippets.
- `assets/demo-lifecycle/*.csv`: small versioned demo tables for incident daily snapshots, status transitions, and assignment transitions.

## Scripts

- `scripts/generate_powerbi_pack.py`: Generate Power Query, DAX, TMDL skeleton, report spec, and maintenance runbook from CSV table/measure specs.
- `scripts/build_demo_powerbi_report_pack.py`: Build a sanitized import-ready Power BI report pack from TOPdesk REST tenant profile artifacts.
- `scripts/build_topdesk_pbir_report.py`: Generate a PBIP/PBIR report-as-code project with report pages, visual containers, KPI cards, charts, tables, and a copied TMDL semantic model. The generated project uses a report-only `.pbip` artifact and binds the report to the model through `definition.pbir`.
- `scripts/validate_topdesk_pbir_report.py`: Validate generated PBIP/PBIR JSON schemas, required project files, page order metadata, and all visual measure/column references against the TMDL semantic model.
