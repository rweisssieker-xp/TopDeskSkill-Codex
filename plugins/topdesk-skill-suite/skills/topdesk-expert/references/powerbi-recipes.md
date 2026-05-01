# Power BI Recipes for TOPdesk

Use this file for concrete DAX, Power Query, RLS, report layout, and validation packs.

## Power Query Patterns

Parameterize tenant URLs and date windows:

```powerquery
// Parameters: TopdeskODataUrl as text, RangeStart as datetime, RangeEnd as datetime
let
    Source = OData.Feed(TopdeskODataUrl, null, [Implementation="2.0"]),
    Incidents = Source{[Name="Incidents", Signature="table"]}[Data],
    Filtered = Table.SelectRows(
        Incidents,
        each [modificationDate] >= RangeStart and [modificationDate] < RangeEnd
    )
in
    Filtered
```

Flatten lookup objects safely:

```powerquery
let
    Expanded = Table.ExpandRecordColumn(
        SourceTable,
        "caller",
        {"id", "dynamicName"},
        {"CallerId", "CallerName"}
    )
in
    Expanded
```

Create date keys:

```powerquery
DateKey = Date.Year([CreatedDate]) * 10000 + Date.Month([CreatedDate]) * 100 + Date.Day([CreatedDate])
```

## Additional DAX Measures

```DAX
Created Incidents =
COUNTROWS ( FactIncident )

Closed Incidents by Closed Date =
CALCULATE (
    [Closed Incidents],
    USERELATIONSHIP ( FactIncident[ClosedDateKey], DimDate[DateKey] )
)

Open Backlog Snapshot =
CALCULATE (
    [Created Incidents],
    FactIncident[CreatedDate] <= MAX ( DimDate[Date] ),
    OR (
        ISBLANK ( FactIncident[ClosedDate] ),
        FactIncident[ClosedDate] > MAX ( DimDate[Date] )
    )
)

SLA Breached Incidents =
CALCULATE (
    [Closed Incidents],
    FactIncident[SlaBreached] = TRUE ()
)

SLA Breach % =
DIVIDE ( [SLA Breached Incidents], [Closed Incidents] )

Reassignment Count =
COUNTROWS ( FactAssignmentHistory )

Average Reassignments per Incident =
DIVIDE ( [Reassignment Count], DISTINCTCOUNT ( FactAssignmentHistory[IncidentKey] ) )

AI Suggestion Acceptance % =
DIVIDE (
    CALCULATE ( COUNTROWS ( FactAiSuggestion ), FactAiSuggestion[Status] = "accepted" ),
    COUNTROWS ( FactAiSuggestion )
)
```

## Row-Level Security

Branch-based RLS:

```DAX
[BranchId] IN
SELECTCOLUMNS (
    FILTER ( SecurityUserBranch, SecurityUserBranch[UserEmail] = USERPRINCIPALNAME () ),
    "BranchId", SecurityUserBranch[BranchId]
)
```

Operator-group RLS:

```DAX
[OperatorGroupId] IN
SELECTCOLUMNS (
    FILTER ( SecurityUserGroup, SecurityUserGroup[UserEmail] = USERPRINCIPALNAME () ),
    "OperatorGroupId", SecurityUserGroup[OperatorGroupId]
)
```

RLS guidance:

- Apply RLS to dimensions such as `DimBranch` or `DimOperatorGroup`, not every fact table.
- Test with "View as role" for customer and operator personas.
- Do not rely on hidden columns as a security boundary.

## Report Page Wireframes

Service desk overview:

- Top row: Open backlog, created today/week, closed today/week, SLA compliance, near-breach count.
- Middle: Created vs closed trend, backlog aging, incidents by priority.
- Bottom: top categories, top branches, assignment group workload.

AI operations:

- Top row: suggestions generated, acceptance %, average confidence, override count.
- Middle: acceptance by suggestion type, confidence band vs acceptance, false-positive categories.
- Bottom: operator feedback reasons, time saved estimate, drift by category/language/channel.

Data quality:

- Missing branch, missing caller, missing category, missing status, unmapped TOPdesk IDs.
- Duplicate persons/assets.
- Stale assets and orphaned links.

## Validation Pack

For every published report, produce:

- Date range used for reconciliation.
- TOPdesk selection/export used as comparison.
- Expected count, Power BI count, difference, explanation.
- Last refresh timestamp.
- Data-source URL/environment, without secrets.
- Known exclusions such as cancelled incidents or archived records.
