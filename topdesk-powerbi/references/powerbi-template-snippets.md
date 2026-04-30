# Power BI Template Snippets

Use this file for reusable DAX and M snippets.

## Date Table DAX

```DAX
DimDate =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2035, 12, 31 ) ),
    "DateKey", YEAR ( [Date] ) * 10000 + MONTH ( [Date] ) * 100 + DAY ( [Date] ),
    "Year", YEAR ( [Date] ),
    "MonthNo", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "YYYY-MM" ),
    "Quarter", "Q" & FORMAT ( [Date], "Q" ),
    "Weekday", FORMAT ( [Date], "dddd" ),
    "IsWeekend", WEEKDAY ( [Date], 2 ) > 5
)
```

## Measures Table DAX

```DAX
Measures = DATATABLE ( "MeasureGroup", STRING, { { "TOPdesk" } } )
```

## Aging Bucket Column

```DAX
Aging Bucket =
SWITCH (
    TRUE (),
    FactIncident[OpenAgeDays] <= 1, "0-1 days",
    FactIncident[OpenAgeDays] <= 3, "2-3 days",
    FactIncident[OpenAgeDays] <= 7, "4-7 days",
    FactIncident[OpenAgeDays] <= 14, "8-14 days",
    FactIncident[OpenAgeDays] <= 30, "15-30 days",
    "30+ days"
)
```

## Confidence Band Column

```DAX
Confidence Band =
SWITCH (
    TRUE (),
    FactAiSuggestion[Confidence] >= 0.90, "High",
    FactAiSuggestion[Confidence] >= 0.70, "Medium",
    FactAiSuggestion[Confidence] >= 0.50, "Low",
    "Very low"
)
```

## Power Query Date Key Function

```powerquery
(inputDate as nullable date) as nullable number =>
if inputDate = null then null
else Date.Year(inputDate) * 10000 + Date.Month(inputDate) * 100 + Date.Day(inputDate)
```

## Power Query Safe Record Field

```powerquery
(recordValue as any, fieldName as text) as any =>
try Record.Field(recordValue, fieldName) otherwise null
```

## Refresh Audit Table

```powerquery
let
    Source = #table(
        type table [RefreshAt = datetimezone, Environment = text],
        {{DateTimeZone.UtcNow(), EnvironmentName}}
    )
in
    Source
```
