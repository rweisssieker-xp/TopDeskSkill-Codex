# Power BI Model Review Checklist

Use this file to review an existing TOPdesk Power BI model or PBIX documentation.

## Model Structure

- Facts and dimensions are separated.
- Date table exists and is marked as date table.
- Relationship directions are mostly single-direction.
- Many-to-many relationships are justified.
- Inactive relationships are documented and used with `USERELATIONSHIP`.
- Technical columns are hidden.
- Measures are centralized in a measures table.

## TOPdesk Semantics

- Created, modified, target, resolved, and closed dates are separate.
- Open/closed status is derived consistently.
- Cancelled records are handled explicitly.
- SLA eligibility is explicit.
- Branch/customer/team fields support RLS.
- Categories/statuses/priorities are mapped to dimensions.
- Historical labels are preserved where needed.

## DAX Quality

- Measures use base measures instead of repeating logic.
- DIVIDE is used instead of raw division.
- Date-role measures use `USERELATIONSHIP`.
- Backlog logic handles open tickets correctly.
- SLA measures document excluded records.
- AI measures separate generated, accepted, edited, rejected.

## Power Query Quality

- Source parameters are used.
- Staging queries have load disabled.
- Types are set explicitly.
- Nested TOPdesk objects are expanded safely.
- Incremental refresh filters are applied early.
- Secrets are not hard-coded.
- Query names distinguish raw, staging, and model tables.

## Security

- RLS roles exist where branch/customer/team visibility is required.
- RLS tested with named users.
- Detail pages and exports respect RLS.
- PII is hidden or masked for broad audiences.
- Dataset permissions are documented.

## Validation

- Created incident count reconciles.
- Closed incident count reconciles.
- Current backlog reconciles.
- SLA compliance difference is explained.
- Branch totals reconcile.
- Refresh audit is visible.
