# Power BI Model Patterns

## Star Schema

- Use facts for events and snapshots.
- Use dimensions for slicers, labels, and grouping.
- Avoid many-to-many relationships unless there is a clear bridge table.
- Use a dedicated date dimension and role-playing dates where needed.

## TOPdesk Grain Choices

- Incident fact: one row per incident.
- Incident event fact: one row per status/assignment event.
- SLA fact: one row per SLA target evaluation.
- Change fact: one row per change.
- Asset fact: one row per asset snapshot.

## DAX Rules

- Always create explicit measures.
- Use base measures, then derived measures.
- Keep business definitions in measure descriptions/specs.
- Avoid calculated columns for high-cardinality transformations that belong in Power Query or source views.

## Validation

- Reconcile row counts per fact.
- Reconcile created/closed/backlog against TOPdesk UI or export.
- Test RLS with at least one broad and one narrow user scope.

