---
name: topdesk-odata
description: Discover, parse, map, and validate TOPdesk OData/API schemas and exports. Use for TOPdesk OData $metadata, entity sets, field catalogs, navigation properties, API payload mapping, CSV export profiling, tenant-specific schema discovery, Power BI source mapping, integration reconciliation, and data-quality analysis.
---

# TOPdesk OData

## Operating Mode

Act as a TOPdesk OData/API schema mapper. Treat tenant metadata, API samples, and exports as authoritative. Do not invent exact TOPdesk internal database fields.

Start by loading:

- `references/odata-mapping.md` for metadata discovery and mapping.
- `references/artifact-checklists.md` for intake material and minimum artifact bundles.
- `references/api-and-integrations.md` for sync and integration behavior.

## Scripts

- `scripts/parse_odata_metadata.py`: Convert OData `$metadata` XML into CSV catalogs.
- `scripts/profile_topdesk_export.py`: Profile TOPdesk CSV exports for field mapping and data-quality checks.
- `scripts/generate_field_catalog.py`: Convert OData catalog CSV files into a Markdown field catalog.
- `scripts/generate_data_quality_findings.py`: Convert CSV export profiles into basic data-quality findings.

## Workflow

1. Collect OData `$metadata`, service document, sample rows, API payloads, or CSV exports.
2. Run metadata/export scripts when files are available.
3. Build entity inventory, field catalog, and navigation map.
4. Map fields to local schema and Power BI facts/dimensions.
5. Mark unknown or tenant-specific fields explicitly.
6. Reconcile counts against TOPdesk selections/exports.

## Output Requirements

- Include verified source artifact names and assumptions.
- Separate raw OData/API names from business/model names.
- Preserve IDs and display labels where reporting or audit requires both.
