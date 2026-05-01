# TOPdesk Query Examples

## Incident Intake

- Grain: one incident.
- Date basis: creation date.
- Common dimensions: branch, caller, category, priority, source, operator group, status.
- Measures: incidents created, incidents closed, backlog, SLA met, first response met.

## Change Throughput

- Grain: one change or one change activity depending on the question.
- Date basis: request date, planned start/end, completion date.
- Common dimensions: change type, risk, impact, template, approver group, status.

## Asset Workload

- Grain: one asset, one asset relation, or one incident-asset link.
- Common dimensions: asset type, location, branch, owner, lifecycle status.
- Measures: assets active, incidents by asset, changes by asset, stale assets.

## Knowledge Deflection

- Grain: one article, one view/search event, or one incident linked to knowledge.
- Measures: article usage, article freshness, deflection proxy, linked incident count.

