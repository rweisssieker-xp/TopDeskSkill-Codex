# Power BI Reporting for TOPdesk

Use this file for Power BI dashboards, semantic models, Power Query, DAX, OData reporting, KPI definitions, and report validation for TOPdesk or a custom Topdesk app.

For implementation-level DAX, M functions, RLS snippets, report wireframes, and validation packs, load `powerbi-recipes.md`.
For KPI terminology and naming conventions, load `glossary-data-dictionary.md`.

## Reporting Workflow

1. Define the audience: service desk lead, operations manager, application manager, executive, customer, or team operator.
2. Define the grain of each fact table before modeling. Example grains: one row per incident, one row per incident action, one row per status transition, one row per SLA target, one row per change activity.
3. Identify the source: TOPdesk OData feed, REST API export, database view, warehouse table, CSV export, or custom app database.
4. Build a star schema. Avoid using a wide transactional TOPdesk export directly as the main report model.
5. Create reusable measures for KPIs rather than embedding logic in visuals.
6. Validate counts against TOPdesk selections/reports or direct SQL/OData totals.
7. Document refresh, security, filters, and known data-quality limitations.

## Recommended Semantic Model

Fact tables:

- `FactIncident`: one row per incident/ticket; dates, caller, branch, category, priority, status, assigned group, created/closed/target timestamps, SLA flags.
- `FactIncidentAction`: one row per action/comment/status update; action date, actor, visibility, time spent, incident key.
- `FactStatusTransition`: one row per status change; from/to status, actor, transition timestamp, duration in previous status.
- `FactAssignmentTransition`: one row per assignment group/operator interval; from/to group, from/to operator, transition timestamp, duration in previous assignment.
- `FactIncidentDailySnapshot`: one row per incident per snapshot date; current status, group, operator, priority, category, branch, open/closed state.
- `FactChange`: one row per change; requester, coordinator, template/type, risk, impact, status, planned/actual dates.
- `FactChangeActivity`: one row per change activity/approval/task.
- `FactAssetSnapshot`: one row per asset at refresh time or snapshot date; type, status, owner, branch, lifecycle state.

Dimension tables:

- `DimDate`: role-play for created, closed, target, planned, action, and snapshot dates.
- `DimPerson`: callers/requesters; avoid exposing personal details unless required.
- `DimOperator`: operators and assignees.
- `DimOperatorGroup`: service teams.
- `DimBranch`: customer/site/company hierarchy.
- `DimCategory`: category/subcategory tree.
- `DimPriority`, `DimStatus`, `DimSource`, `DimAssetType`, `DimService`.

Modeling rules:

- Use surrogate keys in the model when available; keep TOPdesk external IDs for drill-through and reconciliation.
- Use single-direction relationships from dimensions to facts unless a specific many-to-many case requires a bridge table.
- Keep date/time columns in UTC or one documented business timezone; expose local business dates for SLA reporting.
- Use inactive relationships for alternate dates and activate them with `USERELATIONSHIP` in measures.
- Hide technical columns, raw IDs, and unused fields from report consumers.
- Prefer event/history facts for exact flow reporting. Use daily snapshots as a fallback or control layer when TOPdesk does not expose full history.

## History and Snapshot Pattern

Use two complementary paths for lifecycle and assignment reporting:

1. Event/history path:
   - Source: TOPdesk history, audit, action, or field-change data.
   - Model facts: `FactStatusTransition` and `FactAssignmentTransition`.
   - Required columns: incident key, changed timestamp, previous value, new value, actor, duration to next event.
   - Use this path for exact time in status, time in operator group, handoff analysis, and same-day changes.

2. Daily snapshot path:
   - Source: scheduled extraction job that stores the current incident state once per day.
   - Model fact: `FactIncidentDailySnapshot`.
   - Required columns: snapshot date, incident key, status, operator group, operator, priority, category, branch, created/closed timestamps.
   - Use this path for historical backlog, daily aging, approximate time in status/group, and validation when event history is incomplete.

Do not implement snapshot writing inside normal Power BI M transformations. Use a scheduled job, Fabric pipeline, dataflow, Azure Function, PowerShell, Python, or another controlled ingestion process to write the snapshot table, then let Power BI read it.

## Core Incident Measures

Adapt table and column names to the actual model.

```DAX
Incidents =
COUNTROWS ( FactIncident )

Open Incidents =
CALCULATE (
    [Incidents],
    FactIncident[IsClosed] = FALSE ()
)

Closed Incidents =
CALCULATE (
    [Incidents],
    FactIncident[IsClosed] = TRUE ()
)

Resolved Within SLA =
CALCULATE (
    [Closed Incidents],
    FactIncident[ResolvedWithinSla] = TRUE ()
)

SLA Compliance % =
DIVIDE ( [Resolved Within SLA], [Closed Incidents] )

Average Resolution Hours =
AVERAGEX (
    FILTER ( FactIncident, FactIncident[IsClosed] = TRUE () ),
    DATEDIFF ( FactIncident[CreatedAt], FactIncident[ClosedAt], HOUR )
)

Backlog Older Than 7 Days =
CALCULATE (
    [Open Incidents],
    FactIncident[CreatedAt] < TODAY () - 7
)
```

## Status and Flow Measures

Use status-transition facts when the report needs queue aging, handoff analysis, or cycle time.

```DAX
Average Time In Status Hours =
AVERAGE ( FactStatusTransition[DurationHours] )

Average Time In Operator Group Hours =
AVERAGE ( FactAssignmentTransition[DurationHours] )

Total Time In Operator Group Hours =
SUM ( FactAssignmentTransition[DurationHours] )

Reopened Incidents =
CALCULATE (
    DISTINCTCOUNT ( FactStatusTransition[IncidentKey] ),
    FactStatusTransition[ToStatusGroup] = "Reopened"
)

First Response Hours =
AVERAGEX (
    FILTER ( FactIncident, NOT ISBLANK ( FactIncident[FirstResponseAt] ) ),
    DATEDIFF ( FactIncident[CreatedAt], FactIncident[FirstResponseAt], HOUR )
)
```

Snapshot facts are useful when event history is unavailable or incomplete.

```DAX
Snapshot Incidents =
DISTINCTCOUNT ( FactIncidentDailySnapshot[IncidentKey] )

Snapshot Open Incidents =
CALCULATE (
    [Snapshot Incidents],
    FactIncidentDailySnapshot[IsClosed] = FALSE ()
)

Snapshot Days In Current Group =
COUNTROWS ( FactIncidentDailySnapshot )
```

For file-based imports, use `assets/topdesk-lifecycle-powerquery.pq` with the output of `topdesk-integration/scripts/sync_incident_lifecycle.py`.

## Power Query Guidance

- Prefer OData filtering and database views that reduce rows before import.
- Keep raw extraction queries separate from transformation/staging queries.
- Normalize nested TOPdesk objects into separate dimension queries instead of expanding everything into one table.
- Disable load for staging queries that are only intermediate transformations.
- Set data types explicitly for IDs, dates, booleans, durations, and numeric KPI fields.
- Use incremental refresh for large incident/action/history tables when the source supports reliable modified timestamps.
- Avoid hard-coded credentials, instance URLs, and tokens in `.pbix` files or M scripts.

Example OData shaping pattern:

```powerquery
let
    Source = OData.Feed(TopdeskODataUrl, null, [Implementation="2.0"]),
    Incidents = Source{[Name="Incidents", Signature="table"]}[Data],
    SelectedColumns = Table.SelectColumns(
        Incidents,
        {"id", "number", "creationDate", "modificationDate", "closed", "targetDate", "branch", "caller", "category", "status"}
    ),
    ChangedTypes = Table.TransformColumnTypes(
        SelectedColumns,
        {{"creationDate", type datetimezone}, {"modificationDate", type datetimezone}, {"closed", type logical}}
    )
in
    ChangedTypes
```

Treat entity/table names as placeholders until verified against the target TOPdesk OData feed.

## Dashboard Pages

Recommended report layout:

- **Service Desk Overview**: open backlog, created/closed trend, SLA compliance, aging buckets, priority mix, top categories.
- **Incident Flow**: status aging, first response time, resolution time, reopens, handoffs by group/operator.
- **SLA and Targets**: breached/near-breach tickets, target-date distribution, compliance by priority/category/branch.
- **Demand Analysis**: incoming incidents by channel, category, branch, caller group, service, and time period.
- **Change Performance**: changes by type/status/risk, approval duration, overdue activities, implementation success.
- **Asset and CI Insights**: incidents by asset type, problematic assets, lifecycle status, branch ownership, linked changes.
- **Knowledge Effectiveness**: incidents with linked knowledge, deflection candidates, article usage/review status when data exists.
- **Data Quality**: missing categories, missing branch/caller, unmapped external IDs, orphaned references, stale assets.
- **AI/KI Operations**: model suggestion volume, acceptance rate, override reasons, confidence bands, deflection rate, false-positive routing, and time saved.

## KPI Definitions

Define these explicitly in the report or model documentation:

- **Created incidents**: count by creation date, not modification date.
- **Closed/resolved incidents**: count by closure/resolution date; clarify whether cancelled records count.
- **Backlog**: open incidents at a point in time. Snapshot facts are best for historical backlog.
- **Time in status**: prefer status-transition history; use daily snapshots only as an approximation.
- **Time in operator group**: prefer assignment-transition history; use daily snapshots only as an approximation.
- **SLA compliance**: closed incidents meeting target; clarify pauses, reopened tickets, and excluded priorities.
- **First response time**: creation to first public operator response or first assignment/action; choose one and label it.
- **Resolution time**: creation to resolved/closed timestamp; clarify business hours vs calendar hours.
- **Reopen rate**: reopened incidents divided by closed incidents in the selected period.
- **Aging buckets**: use open duration as of refresh date or selected snapshot date.

## Validation Checklist

- Compare total incidents for a date range with TOPdesk Selections/Reports or a trusted SQL/OData query.
- Validate open/closed counts using lifecycle status, not only null close dates.
- Test date slicers against created date, closed date, and target date separately.
- Check row-level security by branch/customer/team before publishing.
- Verify personal data exposure and retention rules.
- Confirm scheduled refresh works with the chosen gateway/credential mode.
- Confirm report consumers understand refresh latency and KPI definitions.

For a concrete reconciliation pack and RLS examples, load `powerbi-recipes.md`.
