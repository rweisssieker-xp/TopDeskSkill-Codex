# Artifact Checklists

Use this file when the user wants to provide real TOPdesk/project material or asks what artifacts are needed for a tenant-specific answer.

## TOPdesk Tenant Artifacts

Ask for or inspect:

- OData `$metadata` XML.
- OData service document.
- Sample rows for incidents, persons, operators, branches, categories, statuses, changes, assets, and knowledge items.
- API response examples for create/update workflows.
- Export column headers from TOPdesk reports/selections.
- Screenshots or configuration exports for SSP forms, Change templates, Asset templates, Action Sequences, and Selections.
- Category tree, priority matrix, SLA/service definitions, operator groups, branch hierarchy.

When the user provides CSV exports, run:

```bash
python scripts/profile_topdesk_export.py export.csv --out export_profile
```

Use `export_profile/column_profile.csv` to identify candidate keys, display fields, status values, category fields, date fields, and data-quality issues.

## App/Database Artifacts

Inspect:

- Migration files.
- ORM schema/models/entities.
- SQL DDL and views.
- Seed/reference data.
- Existing ETL/integration code.
- API DTOs and serializers.
- Test fixtures.
- Existing dashboards or BI models.

## Power BI Artifacts

Inspect:

- `.pbix` or exported model documentation when available.
- Power Query M scripts.
- DAX measures.
- Relationship diagram screenshots.
- RLS role definitions.
- Refresh settings and gateway notes.
- Reconciliation exports from TOPdesk.

## AI/KI Artifacts

Inspect:

- Historical labeled incidents.
- Accepted categories and assignment groups.
- Knowledge articles and standard solutions.
- Operator feedback/override examples.
- Prompt templates and model config.
- Evaluation datasets and previous metric reports.
- PII/redaction rules.

## Minimum Useful Bundle

If the user can provide only a small bundle, prefer:

1. OData `$metadata`.
2. 20 sample incidents.
3. Category/status/priority/operator-group exports.
4. Existing Power BI measures or desired KPI definitions.
5. 20 resolved incidents with final category, group, and resolution text for AI examples.

## Output After Artifact Review

Produce:

- Verified entity/field catalog.
- Gap list and unknowns.
- Mapping to local schema and Power BI model.
- Data-quality findings.
- Security/PII risks.
- Implementation backlog with priorities.
