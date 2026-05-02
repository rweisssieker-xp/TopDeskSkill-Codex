# Power BI Report Specification Template

Use this file to produce a concrete report specification.

## Report Metadata

- Report name:
- Audience:
- Workspace:
- Environment:
- Data source:
- Refresh frequency:
- RLS required:
- Owner:
- Last reviewed:

## Page Specification

For each page:

```text
Page:
Audience:
Purpose:
Default filters:
Visuals:
  - Visual:
    Measure:
    Dimensions:
    Drill-through:
    Tooltip:
Interactions:
Export allowed:
RLS notes:
Validation source:
```

For PBIR report-as-code output, each page should also have:

```text
PBIR page id:
PBIR page order:
Canvas size:
Native visuals only:
Unsupported/custom visual dependency:
Desktop smoke result:
```

## Required Pages

Executive Overview:

- KPI cards: open backlog, created, closed, SLA compliance, near breach.
- Trends: created vs closed, backlog over time.
- Breakdown: branch, category, priority, operator group.

Service Desk Operations:

- Queue by group/operator.
- Aging buckets.
- Near-breach and breached open tickets.
- Reassignment and reopen indicators.

SLA Deep Dive:

- SLA compliance by category, priority, branch, group.
- Breach count and near-breach count.
- Target-date distribution.

Data Quality:

- Missing branch/caller/category/status.
- Unknown dimensions.
- Duplicate candidates.
- Reconciliation delta.

AI Operations:

- Suggestion count.
- Acceptance/override rate.
- Confidence bands.
- Override reasons.
- Model/prompt version trend.

## Info Page

Include:

- KPI definitions.
- Refresh timestamp.
- Source systems.
- Known exclusions.
- RLS explanation.
- Support owner.

## PBIR Acceptance Criteria

- The generated `.pbip` opens in Power BI Desktop with page tabs visible.
- The report has a non-empty `pages/pages.json` with `pageOrder`.
- Every listed page has a `page.json` and at least one `visual.json`.
- Visuals use model measures and fields rather than hard-coded KPI values except for static labels.
- Native visuals are preferred for generated packs; Q&A, smart narrative, decomposition tree, and other advanced/custom visuals require explicit documentation and a Desktop smoke-test note.
