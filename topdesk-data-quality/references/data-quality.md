# TOPdesk Data Quality

Use this file for data-quality checks, mapping gaps, duplicates, orphan references, missing fields, Power BI data-quality pages, and cleanup backlogs.

## Core Checks

Incidents:

- Missing caller/person.
- Missing branch.
- Missing category/subcategory.
- Missing priority/status.
- Open tickets with closed timestamp or closed tickets without closed timestamp.
- Target date missing for SLA-eligible tickets.
- Free-text asset references without asset link.

Supporting files:

- Duplicate persons by email/employee number.
- Inactive operators assigned to open tickets.
- Branches without active persons.
- Categories not used or overused.
- Status values not mapped to open/closed groups.

Assets:

- Missing type/template.
- Missing owner/branch.
- Duplicate serial/inventory number.
- Orphan relations.
- Stale lifecycle status.

Power BI:

- Facts with missing dimension keys.
- Unknown/blank dimension members.
- Row counts not reconciling to TOPdesk.
- Date columns with invalid/null values.
- RLS leakage risk through unmapped branches.

AI/KI:

- Training examples with inconsistent labels.
- Categories with too few examples.
- Sensitive tickets missing flags.
- Knowledge articles past review date.
- Suggestions without feedback status.

## Data Quality Scoring

Score each check:

- Severity: high, medium, low.
- Impact: reporting, workflow, SLA, security, AI, integration.
- Owner: application manager, service desk lead, data engineer, security.
- Fix type: automated, bulk cleanup, manual review, configuration change.

## Output Format

For findings, provide:

| Check | Finding | Impact | Suggested fix | Owner | Priority |
| --- | --- | --- | --- | --- | --- |

## BI Data Quality Page

Recommended visuals:

- Missing caller/branch/category counts.
- Unknown dimension members by source.
- Duplicate person/asset candidates.
- Orphan links by entity.
- Trend of data-quality issues over time.
- Cleanup backlog by owner and priority.

## Power BI Data Quality Measures

```DAX
Incidents Missing Branch :=
CALCULATE (
    COUNTROWS ( FactIncident ),
    ISBLANK ( FactIncident[BranchKey] )
        || FactIncident[BranchKey] = "unknown"
)

Incidents Missing Category :=
CALCULATE (
    COUNTROWS ( FactIncident ),
    ISBLANK ( FactIncident[CategoryKey] )
        || FactIncident[CategoryKey] = "unknown"
)

Incidents Missing Caller :=
CALCULATE (
    COUNTROWS ( FactIncident ),
    ISBLANK ( FactIncident[CallerPersonKey] )
        || FactIncident[CallerPersonKey] = "unknown"
)

Data Quality Issue Count :=
[Incidents Missing Branch]
    + [Incidents Missing Category]
    + [Incidents Missing Caller]
```

## Power BI Data Quality Table

Create a fact-like table for issue tracking:

- `IssueKey`
- `EntityType`
- `EntityKey`
- `IssueType`
- `Severity`
- `ImpactArea`
- `DetectedAt`
- `Owner`
- `Status`
- `SuggestedFix`

Use it for trend reporting and cleanup ownership.
