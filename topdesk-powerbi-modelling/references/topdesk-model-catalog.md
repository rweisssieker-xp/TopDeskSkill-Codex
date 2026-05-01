# TOPdesk Model Catalog

## Facts

- `FactIncident`: created, closed, current status, caller, branch, category, priority, source, operator group.
- `FactIncidentEvent`: status changes, assignment changes, reopen events, response events.
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
- Changes Completed
- Active Assets
- Knowledge Article Usage

