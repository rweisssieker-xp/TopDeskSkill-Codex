# Build and Maintain Power BI Data

Use this file when the user asks to build, generate, maintain, refresh, repair, or evolve Power BI datasets/semantic models for TOPdesk data.

## Capability Boundary

This skill can generate implementation artifacts:

- Power Query M starter queries.
- DAX measure files.
- TMDL semantic-model skeletons.
- Report specifications.
- PBIP/PBIR report-as-code projects with pages and visual containers.
- Maintenance runbooks.
- RLS and reconciliation plans.

It should not publish to Power BI Service, set credentials, or modify tenant workspaces unless explicit credentials/tooling and approval are available.

## Generator Script

Use:

```bash
python scripts/generate_powerbi_pack.py --tables tables.csv --measures measures.csv --out powerbi_pack
```

For an importable Power BI Project with a TMDL semantic model and PBIR report definition, use:

```bash
python scripts/build_topdesk_pbir_report.py --semantic-model <existing.SemanticModel> --out powerbi_pack/topdesk-demo-report/pbip --project-name topdeskdemo
python scripts/validate_topdesk_pbir_report.py --project powerbi_pack/topdesk-demo-report/pbip
```

`tables.csv` columns:

```csv
table,role,source_entity,key,display,incremental_column,rls_column
FactIncident,Fact,Incidents,IncidentKey,Number,modificationDate,BranchKey
DimBranch,Dimension,Branches,BranchKey,BranchName,modificationDate,BranchKey
```

`measures.csv` columns:

```csv
name,expression,folder,description
Created Incidents,"COUNTROWS ( FactIncident )",Incidents,Count created incidents
Open Incidents,"CALCULATE ( [Created Incidents], FactIncident[IsClosed] = FALSE () )",Incidents,Current open incidents
```

Outputs:

- `powerquery/*.pq`
- `dax/measures.dax`
- `tmdl/model.tmdl`
- `REPORT_SPEC.md`
- `MAINTENANCE_RUNBOOK.md`

PBIP/PBIR outputs:

- `<name>.pbip`
- `<name>.SemanticModel/definition/*.tmdl`
- `<name>.SemanticModel/definition.pbism`
- `<name>.Report/definition.pbir`
- `<name>.Report/definition/report.json`
- `<name>.Report/definition/version.json`
- `<name>.Report/definition/pages/pages.json`
- `<name>.Report/definition/pages/<ReportSection*>/page.json`
- `<name>.Report/definition/pages/<ReportSection*>/visuals/<visualId>/visual.json`
- `topdesk-pbir-manifest.json`

## PBIR Structure Contract

Power BI Desktop expects a PBIP/PBIR project to follow the current project layout closely. Use this contract when generating or repairing reports:

- The root `.pbip` file must contain one report artifact: `"artifacts": [{"report": {"path": "<name>.Report"}}]`.
- Do not add a separate `semanticModel` artifact to `.pbip`; the report binds to the model through `definition.pbir`.
- `<name>.Report/definition.pbir` should contain the PBIR definition-properties `$schema`, `"version": "4.0"`, and `"datasetReference": {"byPath": {"path": "../<name>.SemanticModel"}}`.
- `definition/pages/pages.json` must use `pageOrder` and `activePageName`; do not use a `pages` array.
- Include `definition/version.json` with the Fabric `versionMetadata/1.0.0` schema and version `2.0.0`.
- Keep report metadata compatible with tested PBIR schemas: report `3.2.0`, page `2.1.0`, visualContainer `2.7.0`, PBIR definition properties `2.0.0`, PBISM definition properties `1.0.0`.
- The semantic model folder must include `definition/database.tmdl` and `definition.pbism`.

## Desktop Compatibility Notes

Power BI Desktop must have these preview settings enabled before opening generated projects:

- Power BI Project `.pbip` save option.
- Store semantic model using TMDL format.
- Store reports using enhanced metadata format, PBIR.

Generated reports should prefer native visual types. Q&A visuals can trigger the Power BI Desktop deprecation dialog, and advanced visual types such as `smartNarrative` or `decompositionTree` can require custom visual availability in the report. For generated demo packs, prefer replacing those with native cards, tables, bar/line/area charts, matrices, slicers, scatter charts, and donut charts unless the target Desktop environment is known to support the advanced visuals.

## Maintenance Workflow

1. Monitor scheduled refresh and row counts.
2. Detect schema drift via OData metadata comparison.
3. Rebuild generated pack when source mapping changes.
4. Reconcile created/closed/backlog/SLA counts.
5. Update RLS mapping when branch/customer/team access changes.
6. Log changes in release notes.

## Build Checklist

- Source entities verified against OData metadata.
- Incremental refresh column identified.
- Facts and dimensions separated.
- Date table and date roles defined.
- RLS columns identified.
- Data-quality checks defined.
- Reconciliation source agreed.
- PBIP/PBIR validator passes without schema errors.
- Desktop smoke test opens the `.pbip` and confirms visible page tabs and report visuals.
