# Advanced Power BI for TOPdesk

Use this file for detailed TOPdesk Power BI dataset design, DAX catalogs, Power Query/OData patterns, RLS, deployment, refresh, and report UX.

## Dataset Architecture

Recommended layers:

1. **Raw/Staging queries**: OData/API/CSV/SQL extraction with minimal renaming. Disable load.
2. **Normalized queries**: Flatten nested TOPdesk objects, split dimensions, standardize dates and IDs. Disable load when intermediate.
3. **Model tables**: Facts and dimensions with stable names and typed columns. Enable load.
4. **Measures table**: Dedicated table for DAX measures.
5. **Security tables**: User-to-branch/customer/team mappings for RLS.
6. **Validation tables**: Reconciliation snapshots, refresh audit, data-quality checks.

Naming:

- Facts: `FactIncident`, `FactIncidentAction`, `FactStatusTransition`, `FactChange`, `FactChangeActivity`, `FactAssetSnapshot`, `FactAiSuggestion`.
- Dimensions: `DimDate`, `DimBranch`, `DimPerson`, `DimOperator`, `DimOperatorGroup`, `DimCategory`, `DimPriority`, `DimStatus`, `DimSource`, `DimAsset`, `DimAssetType`, `DimKnowledge`.
- Bridges: `BridgeIncidentAsset`, `BridgeIncidentKnowledge`, `BridgeUserBranch`, `BridgeUserOperatorGroup`.

## Relationship Rules

- Use one-to-many single-direction relationships from dimensions to facts.
- Use inactive date relationships for closed/target/modified dates and activate with `USERELATIONSHIP`.
- Use bridge tables for many-to-many links such as incident-assets or user-branches.
- Avoid bi-directional relationships unless a specific security or bridge scenario requires it and is tested.
- Hide surrogate keys and raw technical columns.

## Core Date Measures

```DAX
Created Incidents :=
COUNTROWS ( FactIncident )

Closed Incidents :=
CALCULATE (
    COUNTROWS ( FactIncident ),
    FactIncident[IsClosed] = TRUE (),
    USERELATIONSHIP ( FactIncident[ClosedDateKey], DimDate[DateKey] )
)

Modified Incidents :=
CALCULATE (
    COUNTROWS ( FactIncident ),
    USERELATIONSHIP ( FactIncident[ModifiedDateKey], DimDate[DateKey] )
)

Open Incidents Current :=
CALCULATE (
    [Created Incidents],
    FactIncident[IsClosed] = FALSE ()
)

Backlog As Of Date :=
VAR SelectedDate = MAX ( DimDate[Date] )
RETURN
CALCULATE (
    COUNTROWS ( FactIncident ),
    FactIncident[CreatedDate] <= SelectedDate,
    OR (
        ISBLANK ( FactIncident[ClosedDate] ),
        FactIncident[ClosedDate] > SelectedDate
    )
)
```

## SLA Measures

```DAX
SLA Eligible Incidents :=
CALCULATE (
    [Created Incidents],
    FactIncident[IsSlaEligible] = TRUE ()
)

SLA Met Incidents :=
CALCULATE (
    [Closed Incidents],
    FactIncident[IsSlaEligible] = TRUE (),
    FactIncident[SlaBreached] = FALSE ()
)

SLA Compliance % :=
DIVIDE ( [SLA Met Incidents], [Closed Incidents] )

Near Breach Open Incidents :=
CALCULATE (
    [Open Incidents Current],
    FactIncident[MinutesToTarget] >= 0,
    FactIncident[MinutesToTarget] <= 240
)

Breached Open Incidents :=
CALCULATE (
    [Open Incidents Current],
    FactIncident[TargetDate] < NOW ()
)
```

## Flow and Quality Measures

```DAX
Average Resolution Hours :=
AVERAGEX (
    FILTER ( FactIncident, FactIncident[IsClosed] = TRUE () ),
    FactIncident[ResolutionHours]
)

Median Resolution Hours :=
MEDIANX (
    FILTER ( FactIncident, FactIncident[IsClosed] = TRUE () ),
    FactIncident[ResolutionHours]
)

First Response Hours :=
AVERAGEX (
    FILTER ( FactIncident, NOT ISBLANK ( FactIncident[FirstResponseDateTime] ) ),
    FactIncident[FirstResponseHours]
)

Reopened Incidents :=
CALCULATE (
    [Created Incidents],
    FactIncident[ReopenCount] > 0
)

Reopen Rate % :=
DIVIDE ( [Reopened Incidents], [Closed Incidents] )

Reassigned Incidents :=
CALCULATE (
    DISTINCTCOUNT ( FactAssignmentHistory[IncidentKey] ),
    FactAssignmentHistory[AssignmentSequence] > 1
)

Reassignment Rate % :=
DIVIDE ( [Reassigned Incidents], [Created Incidents] )
```

## AI/KI Measures

```DAX
AI Suggestions :=
COUNTROWS ( FactAiSuggestion )

AI Accepted Suggestions :=
CALCULATE (
    [AI Suggestions],
    FactAiSuggestion[SuggestionStatus] = "accepted"
)

AI Acceptance % :=
DIVIDE ( [AI Accepted Suggestions], [AI Suggestions] )

Average AI Confidence :=
AVERAGE ( FactAiSuggestion[Confidence] )

AI Override % :=
DIVIDE (
    CALCULATE ( [AI Suggestions], FactAiSuggestion[SuggestionStatus] IN { "edited", "rejected" } ),
    [AI Suggestions]
)
```

## Power Query OData Patterns

Parameter table:

- `TopdeskODataUrl`
- `RangeStart`
- `RangeEnd`
- `EnvironmentName`

Incremental refresh filter:

```powerquery
let
    Source = OData.Feed(TopdeskODataUrl, null, [Implementation="2.0"]),
    Entity = Source{[Name="Incidents", Signature="table"]}[Data],
    Filtered = Table.SelectRows(
        Entity,
        each [modificationDate] >= RangeStart and [modificationDate] < RangeEnd
    )
in
    Filtered
```

Safe nested expansion:

```powerquery
let
    AddCallerId = Table.AddColumn(SourceTable, "CallerId", each try [caller][id] otherwise null, type text),
    AddCallerName = Table.AddColumn(AddCallerId, "CallerName", each try [caller][dynamicName] otherwise null, type text)
in
    AddCallerName
```

Unknown dimension member:

```powerquery
let
    Unknown = #table(
        type table [StatusKey = text, StatusName = text, StatusGroup = text],
        {{"unknown", "Unknown", "Unknown"}}
    ),
    Combined = Table.Combine({Unknown, StatusDimension})
in
    Combined
```

## RLS Patterns

Branch RLS:

```DAX
DimBranch[BranchKey] IN
SELECTCOLUMNS (
    FILTER ( SecurityUserBranch, SecurityUserBranch[UserEmail] = USERPRINCIPALNAME () ),
    "BranchKey", SecurityUserBranch[BranchKey]
)
```

Team RLS:

```DAX
DimOperatorGroup[OperatorGroupKey] IN
SELECTCOLUMNS (
    FILTER ( SecurityUserOperatorGroup, SecurityUserOperatorGroup[UserEmail] = USERPRINCIPALNAME () ),
    "OperatorGroupKey", SecurityUserOperatorGroup[OperatorGroupKey]
)
```

Validation:

- Test at least one unrestricted admin, one branch-limited user, one team-limited user, and one user with no mapping.
- Verify detail tables, drill-through pages, exports, and tooltips respect RLS.

## Report Pages

Executive overview:

- SLA compliance, backlog trend, created/closed trend, aging, top services/categories, branch comparison.

Service desk operations:

- Open queue by group/operator, near-breach, aging buckets, reassignment, first response.

Demand and categories:

- Volume by category/subcategory, source channel, branch, service, time pattern, repeated issues.

SLA deep dive:

- Breaches by priority/category/branch/group, time to target, paused tickets, historical trend.

Asset insights:

- Incidents by asset type, problematic assets, assets past lifecycle, incidents linked to changes.

Knowledge and deflection:

- Article usage, linked incidents, deflection candidates, review overdue, reopen after knowledge usage.

AI operations:

- Suggestions, acceptance, override, confidence bands, false-positive categories, drift signals.

Data quality:

- Missing dimension links, unknowns, duplicates, orphan links, reconciliation deltas.

## Deployment and Refresh

- Use deployment pipelines or separate workspaces for dev/test/prod.
- Parameterize source URLs and environment names.
- Avoid hard-coded credentials in M.
- Configure gateway ownership and backup owner.
- Enable incremental refresh for large incidents/actions/history tables.
- Publish a refresh audit table with last successful refresh and source row counts.
- Document known exclusions and KPI definitions on an info page.

## Reconciliation Matrix

| KPI | TOPdesk comparison source | Power BI source | Tolerance | Notes |
| --- | --- | --- | --- | --- |
| Created incidents | TOPdesk selection/export | `FactIncident` by created date | 0 or explained | Exclude deleted/archived only if documented |
| Closed incidents | TOPdesk selection/export | `FactIncident` by closed date | 0 or explained | Clarify cancelled records |
| Open backlog | TOPdesk current selection | `IsClosed = false` | 0 or explained | Snapshot needed for historical backlog |
| SLA compliance | TOPdesk report | SLA measures | agreed | Clarify pause/business-hours logic |
| Branch totals | TOPdesk branch filter | `DimBranch` + RLS | 0 or explained | Check unmapped branches |
