# Proof Of Value Sprint

## Sprint Shape

- Day 1: discovery, data availability, KPI baseline.
- Day 2: tenant mapping and data-quality scan.
- Day 3: Power BI prototype, semantic model sketch, and lifecycle snapshot/transition proof.
- Day 4: AI/KI feature pack or automation proof.
- Day 5: demo, ROI, risks, next-step roadmap.

## Required Inputs

- OData metadata or API/entity sample.
- CSV exports for incidents, changes, assets, or knowledge.
- Incident event history, action log, audit export, or daily incident export for lifecycle reconstruction.
- KPI definitions and TOPdesk UI reconciliation samples.
- Security/RLS assumptions.
- Stakeholder priorities.

## Outputs

- Power BI proof page.
- Semantic model sketch.
- Lifecycle proof page with status duration, assignment duration, daily backlog snapshots, and reassignment rate.
- Data-quality findings.
- AI feature pack if in scope.
- ROI calculator.
- Executive decision memo.

## Lifecycle PoV Track

Use this track when the value hypothesis is bottleneck detection, handoff reduction, SLA focus, or backlog aging.

Inputs:

- Incident export with creation, modification, status, operator group, priority, category, target, and closed fields.
- Status or action history if available.
- Assignment/operator-group history if available.
- At least one daily snapshot export if exact history is not available yet.

Proof build:

- Generate `FactStatusTransition`, `FactAssignmentTransition`, and `FactIncidentDailySnapshot`.
- Reconcile incident counts against the source export.
- Validate that intervals have `ValidFrom`, `ValidTo`, `DurationHours`, and sequence.
- Build one drill-through example for a single incident and one aggregate bottleneck view.

Acceptance criteria:

- Stakeholders can see where a selected incident waited over time.
- Service desk lead can rank statuses and groups by average/P90 duration.
- Management can see open backlog trend by snapshot date and age bucket.
- Data gaps are explicitly labeled as event-history gaps or snapshot-only coverage.

Decision metrics:

- Reassignment rate.
- Average and P90 time in status.
- Average and P90 time in operator group.
- Waiting-state share.
- Open incidents by snapshot date and age bucket.
- SLA-risk backlog by group and priority.
