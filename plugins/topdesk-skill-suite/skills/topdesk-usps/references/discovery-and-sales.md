# Discovery and Sales Enablement

Use this file for discovery questions, qualification, workshop agendas, proposal structure, and value hypotheses.

## Discovery Questions

TOPdesk operations:

- How many incidents are created per month?
- Which channels create most demand: SSP, email, phone, monitoring, API?
- Which categories cause the highest volume or most reassignments?
- Which teams have the biggest backlog or SLA pressure?
- Where do incidents wait longest today: status, group, operator, category, supplier, or customer?
- Which handoffs are considered avoidable?
- Which status or routing changes are planned in the next 3-6 months?
- Are Change, Asset, Knowledge, and SSP actively used?

Reporting:

- Which TOPdesk reports are trusted today?
- Where do Power BI numbers disagree with TOPdesk?
- Which KPIs are used in management meetings?
- Is reporting needed by branch, customer, service, team, operator, category, or asset?
- Are there RLS/customer visibility requirements?
- Which KPI disagreements consume the most management or reporting time?
- Which KPIs need source-to-report lineage for audit, compliance, or steering meetings?
- Which reports need historical as-of views rather than current-state numbers?

Integration:

- Which systems create, enrich, or consume TOPdesk tickets?
- Are there external IDs already stored in TOPdesk?
- What imports/exports are manual today?
- What failed sync or data-quality issues happen repeatedly?
- Who owns recovery when refresh, sync, schema drift, or credentials fail?
- Are runbooks already documented and tested?

AI:

- Which work is repetitive: classification, routing, summaries, replies, knowledge lookup?
- Is there historical labeled ticket data?
- Are knowledge articles current and trusted?
- Which actions must always stay human-reviewed?
- What sensitive categories need stricter controls?
- Which AI outputs would need confidence, explanation, source references, prompt/model version, and operator feedback?
- Which KPIs should prove AI value: reassignment, first response, waiting time, edit rate, knowledge reuse, or deflection?

Governance:

- What PII and internal notes appear in tickets?
- Who may see customer/branch-specific data?
- What retention rules apply?
- What audit evidence is required?
- Does the organization prefer reviewable SQL/M/DAX/scripts over proprietary analytics logic?
- Which TOPdesk configuration changes need reporting impact checks before rollout?

Value and buying process:

- Who needs the executive control view: CIO, CFO, service owner, service desk lead, or application manager?
- Is a five-day proof-of-value enough for a go/no-go decision?
- Which single before/after metric would make the initiative credible?

## Qualification Signals

Strong fit:

- High ticket volume.
- Heavy Power BI/reporting need.
- Manual imports/exports.
- Frequent reassignment.
- Visible waiting-time or bottleneck complaints.
- Need for historical backlog or as-of reporting.
- Management needs traceable KPI evidence.
- TOPdesk data used in management reporting.
- Interest in AI but concern about governance.
- Multiple branches/customers or RLS requirements.
- Preference for Microsoft/Power BI assets over another black-box analytics platform.

Weak fit:

- Very low ticket volume.
- No reporting or integration need.
- No access to OData/API/export data.
- No owner for data quality or TOPdesk configuration.
- No stakeholder willing to define KPI truth or reconciliation rules.
- No operational owner for refresh/sync/runbook responsibility.

## Workshop Agenda

90-minute discovery:

1. Current TOPdesk usage and pain points.
2. Reporting/KPI walkthrough.
3. Data/API/OData availability.
4. Workflow and category/routing review.
5. AI opportunity scan.
6. Security and governance constraints.
7. Lifecycle bottleneck and snapshot-history discussion.
8. Reconciliation, audit, and no-lock-in requirements.
9. Prioritized roadmap and next artifacts.

## Proposal Structure

1. Executive summary.
2. Current pain points.
3. Proposed scope.
4. TOPdesk data foundation.
5. Power BI reporting package.
6. AI assist package.
7. Security and governance.
8. Lifecycle bottleneck and snapshot-history package.
9. Operational runbooks and support model.
10. Implementation phases.
11. Success metrics.
12. Required customer inputs.

## Value Hypotheses

- If classification suggestions are accepted for 50% of incoming tickets, triage effort decreases measurably.
- If reassignment rate drops, resolution time and operator frustration decrease.
- If Power BI KPIs reconcile with TOPdesk, management reporting trust increases.
- If KPI differences are explicit and explained, reporting discussions move from dispute to decision.
- If daily snapshots preserve backlog history, leadership can steer trends instead of only seeing refresh-state numbers.
- If status and assignment durations are measured, bottleneck actions can be prioritized by evidence.
- If runbooks cover refresh, sync, and schema drift, the solution becomes supportable after go-live.
- If artifacts stay reviewable in SQL, CSV, Python, Power Query, DAX, and Markdown, the customer avoids analytics lock-in.
- If knowledge suggestions are embedded in the workflow, repeated tickets become candidates for deflection.
- If AI suggestions are logged with feedback, model quality can improve without losing auditability.

## Five-Day Proof Path

Day 1: KPI truth and data availability.

- Confirm incident volume, trusted TOPdesk counts, required filters, and one target management question.
- Identify exact history availability versus snapshot-only fallback.

Day 2: Tenant mapping and data trust.

- Map incident fields, status, operator group, priority, category, branch, target, and closed fields.
- Produce first reconciliation view and data-quality findings.

Day 3: Lifecycle and executive cockpit.

- Build status duration, assignment duration, daily snapshot trend, reassignment, and backlog-aging proof visuals.
- Drill from one executive KPI to a single incident timeline.

Day 4: Governance, AI, or operations proof.

- Pick one: AI suggestion audit, RLS/security review, refresh/sync runbook, or change-readiness check.

Day 5: ROI and decision.

- Present before/after hypotheses, risks, required data gaps, operating model, and go/no-go roadmap.

## Persona Offer Modules

Executive control:

- Buyer: CIO, IT leader, service owner, CFO.
- Promise: one view of backlog, SLA risk, bottlenecks, routing quality, and improvement value.
- Proof: KPI cockpit with drill-through to lifecycle evidence and ROI assumptions.

Service desk optimization:

- Buyer: service desk lead, operations manager.
- Promise: reduce avoidable handoffs and waiting time.
- Proof: reassignment rate, time in status, time in group, P90 duration, age buckets.

Application management:

- Buyer: TOPdesk application manager.
- Promise: make categories, statuses, groups, forms, and fields report-ready before rollout.
- Proof: mapping catalog, report impact checklist, validation cases, schema-drift notes.

Data trust:

- Buyer: reporting owner, management team.
- Promise: make KPI definitions and TOPdesk-vs-Power-BI differences explicit.
- Proof: reconciliation table, lineage map, signed-off KPI catalog.

AI governance:

- Buyer: service desk lead, security, compliance.
- Promise: use AI in suggest-only mode with traceability and operator control.
- Proof: suggestion log, confidence/explanation, feedback metrics, permission scope, prompt/model version.

Operations readiness:

- Buyer: IT operations, BI owner, integration owner.
- Promise: keep the solution supportable after go-live.
- Proof: health report, package validation, refresh/sync/schema-drift runbooks, checksum.
