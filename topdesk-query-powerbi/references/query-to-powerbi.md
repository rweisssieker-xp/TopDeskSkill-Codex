# Query To Power BI Patterns

## Output Contract

For each business question, produce:

- Business question and decision owner.
- Fact grain and date basis.
- Source entities/tables and required fields.
- OData/API/SQL/query plan with tenant-specific assumptions marked.
- Power Query extraction plan.
- Fact/dimension mapping.
- DAX measure definitions.
- RLS and PII notes.
- Validation and reconciliation checks.

## Translation Rules

- "How many tickets came in?" means created incident count by creation date unless the user says otherwise.
- "Solved/closed" must name the lifecycle status and the date column used.
- SLA measures require numerator, denominator, paused time handling, and exclusion rules.
- Backlog is a snapshot or as-of calculation; do not mix it with simple created-minus-closed unless that is explicitly accepted.
- Reassignment and reopen metrics need event/history data; flag if only current-state exports are available.

## Query Design

- Keep OData filters close to source for date ranges and entity type restrictions.
- Keep semantic transformations in Power Query or the warehouse, not DAX, when they define reusable dimensions.
- Keep KPI calculations in DAX when they depend on report filter context.

