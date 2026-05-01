# TOPdesk Tenant Mapping

Use this file for turning tenant-specific metadata, exports, and samples into verified mappings.

## Required Inputs

- OData `$metadata`.
- Entity sample rows.
- CSV export headers.
- TOPdesk UI screenshots when labels differ from API names.
- Category/status/priority/operator-group exports.
- Branch/person/security model.

## Mapping Outputs

- Entity inventory.
- Field catalog.
- Navigation/relationship map.
- Business concept map.
- Local database mapping.
- Power BI fact/dimension mapping.
- RLS/security mapping.
- Data-quality gaps.
- Unknowns requiring admin confirmation.

## Mapping Rule

Every mapped field must have:

- Source artifact.
- Source field.
- Business concept.
- Target field/table.
- Data type.
- Nullable/required status.
- Transformation rule.
- Validation method.
