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
- Executive control page with KPI-to-incident drill-through.
- Reconciliation page with TOPdesk count, model count, difference, and explanation.
- Source-to-report lineage note for at least one critical KPI.
- Operations readiness note covering refresh/sync/schema-drift ownership.
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

## Executive Control PoV Track

Use this track when the buyer needs management steering, service transparency, or investment justification.

Inputs:

- One executive question, such as "Why is backlog increasing?" or "Where is SLA risk concentrated?"
- Agreed KPI definitions for open, created, closed, overdue, reassigned, and aged backlog.
- TOPdesk source count or UI selection for reconciliation.

Proof build:

- Build an executive page with backlog, SLA risk, reassignment, waiting time, and data trust.
- Add drill-through from KPI to group/category/status and one incident timeline.
- Label the likely action: routing change, category cleanup, knowledge work, staffing review, or AI assist pilot.

Acceptance criteria:

- Leadership can move from KPI to evidence in under two drill steps.
- Each KPI has an owner, definition, and source/reconciliation note.
- The final recommendation separates process, configuration, data, and automation actions.

## Data Trust PoV Track

Use this track when the pain is reporting disagreement or low management trust.

Inputs:

- TOPdesk export or UI count for the chosen reporting period.
- Current Power BI/reporting count if available.
- Existing KPI definitions, filters, and known disputes.

Proof build:

- Create a reconciliation table with source count, model count, difference, and explanation.
- Document grain, filter assumptions, date logic, and closed/open logic.
- Trace one KPI from source field to fact table to DAX measure to visual.

Acceptance criteria:

- Stakeholders agree whether differences are data quality, filter logic, timing, or definition issues.
- At least one disputed KPI is made explainable.
- The next data-quality or definition actions are explicit.

## No-Lock-In PoV Track

Use this track when the customer wants reviewable, portable implementation assets.

Proof build:

- Show SQL or CSV facts, Power Query import, DAX measure, report visual, and validation script for one KPI.
- Package or identify the reusable assets needed for handover.
- Confirm where tenant credentials and secrets live outside source control.

Acceptance criteria:

- Customer can inspect the metric logic without a proprietary black box.
- Delivery artifacts are versionable and supportable.
- Security-sensitive values are not embedded in the plugin/package.

## Operations Readiness PoV Track

Use this track when go-live support risk is a decision factor.

Proof build:

- Define refresh/sync/schema-drift failure scenarios.
- Produce or reference runbooks for retry, credential validation, source schema changes, and package verification.
- Run plugin/package verification where in scope.

Acceptance criteria:

- Operational owner is known.
- Recovery steps are documented.
- Package or script validation evidence exists.
