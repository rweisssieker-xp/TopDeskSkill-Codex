# Build and Maintain Power BI Data

Use this file when the user asks to build, generate, maintain, refresh, repair, or evolve Power BI datasets/semantic models for TOPdesk data.

## Capability Boundary

This skill can generate implementation artifacts:

- Power Query M starter queries.
- DAX measure files.
- TMDL semantic-model skeletons.
- Report specifications.
- Maintenance runbooks.
- RLS and reconciliation plans.

It should not publish to Power BI Service, set credentials, or modify tenant workspaces unless explicit credentials/tooling and approval are available.

## Generator Script

Use:

```bash
python scripts/generate_powerbi_pack.py --tables tables.csv --measures measures.csv --out powerbi_pack
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
