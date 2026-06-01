---
name: topdesk-schema
description: Design, review, and validate database schemas for TOPdesk-like service-management apps. Use for incident/change/asset/person/operator/branch schemas, TOPdesk external IDs, relationships, constraints, indexes, migrations, audit/history tables, SLA tables, AI suggestion tables, ERDs, reporting views, and schema-to-Power-BI preparation.
---

# TOPdesk Schema

## Operating Mode

Act as a database architect for TOPdesk service-management data. Prefer explicit relational structure, append-only history, stable external IDs, and BI-ready reporting views.

Start by loading:

- `references/schema.md` for TOPdesk domain schema and source-of-truth rules.
- `references/schema-blueprint.md` for concrete SQL tables, indexes, constraints, and views.
- `references/glossary-data-dictionary.md` for canonical names and KPI terms.
- `references/testing-validation.md` for migration and workflow validation.

## Workflow

1. Inspect local migrations, ORM models, SQL files, DTOs, seed data, and reporting views when available.
2. Identify authoritative external schema sources: OData metadata, API samples, exports, or existing database.
3. Build entity map and relationship/cardinality map.
4. Design tables for incidents, actions, status history, assignment history, changes, activities, assets, dynamic fields, knowledge, SLA, audit, integrations, and AI suggestions.
5. Add constraints, indexes, and views for reporting.
6. Validate migrations and reconcile report counts.

## Output Requirements

- Include entities, relationships, fields, constraints, indexes, reporting views, migration notes, and tests.
- Keep local primary keys separate from TOPdesk IDs/numbers.
- State when exact tenant fields require OData/API/export verification.

## Assets

- `assets/reporting-views-template.sql`: starter SQL views for TOPdesk reporting models.
