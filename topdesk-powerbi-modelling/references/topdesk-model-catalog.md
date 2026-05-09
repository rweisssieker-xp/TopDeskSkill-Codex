# TOPdesk Model Catalog

## Facts

- `FactIncident`: created, closed, current status, caller, branch, category, priority, source, operator group.
- `FactIncidentEvent`: generic status changes, assignment changes, reopen events, response events, and audit-derived events.
- `FactStatusTransition`: one row per incident status interval with valid-from, valid-to, from status, to status, actor, and duration.
- `FactAssignmentTransition`: one row per incident assignment interval with valid-from, valid-to, operator group, operator, actor, and duration.
- `FactIncidentDailySnapshot`: one row per incident per snapshot date with status, operator group, operator, branch, category, priority, open/closed state, and target/closed timestamps.
- `FactSla`: target type, due date, completion date, breach flag, pause duration.
- `FactChange`: change type, risk, impact, template, status, requester, planned dates.
- `FactAssetSnapshot`: asset, type, owner, branch, location, lifecycle status.

## Dimensions

- `DimDate`
- `DimBranch`
- `DimPerson`
- `DimOperator`
- `DimOperatorGroup`
- `DimCategory`
- `DimPriority`
- `DimStatus`
- `DimAsset`
- `DimKnowledgeArticle`

## Core Measures

- Incidents Created
- Incidents Closed
- Backlog
- SLA Met %
- Median Resolution Hours
- Reopened Incidents
- Reassignment Count
- Time in Status Hours
- Time in Operator Group Hours
- Snapshot Open Incidents
- Snapshot Days in Status
- Snapshot Days in Operator Group
- Changes Completed
- Active Assets
- Knowledge Article Usage

## Source Priority

- Use `FactStatusTransition` and `FactAssignmentTransition` when TOPdesk history, audit, or field-change data is available.
- Use `FactIncidentDailySnapshot` when only current incident state can be extracted reliably.
- Keep both paths when possible: event facts provide exact intra-day timing, snapshots provide backlog-as-of reporting and completeness checks.
