# Power BI Handbook

Audience: BI developers, service leads, managers, and report consumers.

## Model Overview

Recommended model:

- Facts: incidents, actions, status transitions, changes, activities, assets, AI suggestions.
- Dimensions: date, branch, person, operator, group, category, priority, status, source, asset type.
- Security: branch/customer/team RLS.

## KPI Rules

- Created incidents use created date.
- Closed incidents use closed date.
- Backlog is open tickets at a point in time.
- SLA compliance must define eligibility, pauses, and excluded records.
- Reopen rate requires status history or reopen count.

## Consumer Guidance

- Check refresh timestamp.
- Check active filters.
- Use drill-through for detail.
- Treat unknown dimension members as data-quality issues.
- Do not compare reports unless KPI definitions match.

## Developer Checklist

- Star schema in place.
- Date table marked.
- RLS tested.
- DAX uses base measures.
- Counts reconcile with TOPdesk selections/exports.
- Data-quality page exists.
