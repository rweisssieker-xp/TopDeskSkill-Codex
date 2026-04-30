# TOPdesk OData/API Mapping

Use this file when discovering a real TOPdesk tenant schema, building field catalogs, mapping OData/API payloads to a database, or reconciling Power BI with TOPdesk.

## Discovery Workflow

1. Open the OData service document and `$metadata` for the target tenant.
2. List entity sets, keys, field names, data types, nullable flags, and navigation properties.
3. Pull 5-20 sample rows per entity.
4. Compare fields with TOPdesk UI labels and export columns.
5. Record mappings in a tenant-specific table. Do not assume another tenant has identical optional fields.

## Field Catalog Template

| Entity set | Field | Type | Nullable | Business concept | Local/model field | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| verified | verified | verified | verified | Incident ID | `topdesk_id` | Use metadata |
| verified | verified | verified | verified | Incident number | `topdesk_number` | Human reference |
| verified | verified | verified | verified | Caller/person | `caller_person_id` | Navigation or lookup |
| verified | verified | verified | verified | Branch | `branch_id` | Important for RLS |
| verified | verified | verified | verified | Category | `category_id` | May be nested |
| verified | verified | verified | verified | Status | `status_id` | Preserve history separately |

## Common Business Concepts to Find

Incident:

- ID/key, number, brief description, request text.
- Creation, modification, target, response, resolved, closed timestamps.
- Caller/person, branch, department, location.
- Category/subcategory, priority, impact, urgency.
- Status/processing status, assigned operator, assigned group.
- Source/channel, linked assets, linked changes, action history, attachments.

Person/operator/branch:

- Person ID, display name, email, branch, department, active flag.
- Operator ID, name, email, active flag, group memberships.
- Branch ID, name, parent branch, active flag.

Assets:

- Asset ID, number/name, template/type, status.
- Owner/person, branch/location, supplier.
- Dynamic fields and relations.

Changes:

- Change ID/number, requester, coordinator, type/template.
- Status/phase, risk/impact, planned and actual dates.
- Activities, approvals, linked incidents/assets.

## Mapping Rules

- Store both ID and display name when reporting needs historical labels.
- For dimensions, use stable IDs as keys and display names as attributes.
- For nested objects, split into dimensions unless the data is truly one-off.
- For multi-value links, create bridge tables.
- For dynamic asset fields, create a typed field-value table and selected reporting views.
- For Power BI, rename fields to business-friendly names in the model, not in raw extraction queries.

## Power BI Mapping Output

When the target is Power BI, produce:

- Raw OData query/entity name.
- Model table name.
- Fact/dimension classification.
- Key column.
- Display column.
- Date columns and intended role.
- Relationship target.
- RLS relevance.
- Incremental refresh column.
- Data-quality checks.

Example:

| OData entity | Model table | Role | Key | Display | Dates | RLS | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| verified incidents entity | `FactIncident` | Fact | IncidentKey | Number | Created/Closed/Modified/Target | Branch | Use modified date for incremental refresh |
| verified branches entity | `DimBranch` | Dimension | BranchKey | BranchName | Modified | Yes | Required for branch/customer RLS |

## Reconciliation Queries

Validate each source before using it:

- Total incidents created by month.
- Open incidents by status.
- Closed incidents by month.
- Incidents by category/subcategory.
- Incidents by branch.
- Distinct caller/person count.
- Assignment group distribution.
- Modified records since last refresh.

## Tenant Mapping Artifact

When the user provides metadata or samples, produce:

1. Entity-set inventory.
2. Field catalog.
3. Relationship/navigation map.
4. Local schema mapping.
5. Power BI fact/dimension mapping.
6. Data-quality issues.
7. Unknowns requiring TOPdesk admin/API documentation.

## Metadata Parser

When the user provides a TOPdesk OData `$metadata` XML file, run:

```bash
python scripts/parse_odata_metadata.py metadata.xml --out odata_catalog
```

Outputs:

- `entity_sets.csv`: entity set names and entity types.
- `properties.csv`: entity type properties, data types, nullable flags, and key markers.
- `navigation_properties.csv`: relationships/navigation properties.

Use the CSV files to produce a tenant-specific field catalog and BI mapping. Treat parser output as discovery input, not final business naming.
