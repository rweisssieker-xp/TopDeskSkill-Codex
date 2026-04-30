# TOPdesk Asset Management

Use this file for asset templates, dynamic fields, asset relations, lifecycle, schema, analytics, and links to incidents/changes.

## Asset Modeling

Core fields:

- Asset ID / TOPdesk ID.
- Name/number.
- Asset type/template.
- Status/lifecycle state.
- Owner/person.
- Branch/location.
- Supplier/contract.
- Serial/inventory fields.
- Lifecycle start/end.

Dynamic fields:

- Use template metadata plus typed field values.
- Promote BI-critical dynamic fields into reporting views.
- Keep historical display values where ownership or location changes matter.

## Relations

Model relations as typed edges:

- Asset to asset.
- Asset to person.
- Asset to branch/location.
- Asset to incident.
- Asset to change.
- Asset to supplier/contract.

Avoid fixed columns for relationship types that can vary by asset template.

## Workflow Uses

- Incident enrichment by linked asset.
- Change impact analysis.
- Problem detection by recurring asset incidents.
- Lifecycle replacement planning.
- Supplier/contract analysis.

## Data Quality Checks

- Assets without type/template.
- Assets without owner/branch.
- Duplicate serial numbers or inventory numbers.
- Stale assets with no modification date.
- Orphan asset relations.
- Incidents with free-text asset references but no asset link.

## Asset KPIs

- Incidents by asset type.
- Top problematic assets.
- Assets with repeated incidents in rolling window.
- Changes by asset type.
- Assets past lifecycle date.
- Missing owner/branch rate.
