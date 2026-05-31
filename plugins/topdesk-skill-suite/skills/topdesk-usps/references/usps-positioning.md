# USPs and Positioning

Use this file when the user asks for USPs, value propositions, pitch text, stakeholder messaging, product positioning, feature benefits, roadmap framing, or business-case wording for TOPdesk apps, reporting, integrations, or AI/KI features.

## Core Positioning

Position the solution as a practical TOPdesk intelligence layer:

- It connects TOPdesk operational workflows, database-ready structure, Power BI analytics, and AI/KI assistance.
- It respects TOPdesk as the operational source while making data easier to govern, analyze, automate, and improve.
- It helps service teams move from reactive ticket handling to measurable, assisted, and auditable service operations.

## Primary USPs

- **TOPdesk-specific domain model**: Built around incidents, changes, assets, persons, operators, branches, knowledge, SLA, action logs, and supporting files rather than generic ticketing abstractions.
- **Schema-aware by design**: Separates TOPdesk IDs, local keys, reporting views, history tables, audit events, and AI suggestions so integrations and analytics stay reliable.
- **Power BI-ready data foundation**: Provides star-schema guidance, DAX measures, RLS patterns, KPI definitions, and reconciliation checks for service reporting.
- **AI/KI with human control**: Supports classification, routing, summaries, response drafts, semantic search, and SLA-risk prediction while preserving review, audit, privacy, and rollback.
- **OData/API verification first**: Uses tenant metadata, sample payloads, exports, and parser tools instead of guessing field names.
- **Operationally usable**: Includes runbooks, monitoring, refresh failure handling, deployment checks, and integration reconciliation.
- **Compliance-conscious**: Treats PII, internal notes, branch restrictions, API credentials, and AI context as sensitive from the start.
- **End-to-end validation**: Covers workflow tests, schema migration checks, Power BI count reconciliation, integration tests, and AI regression metrics.

## Max USP Library

- **One connected operating model**: Features, schema, OData/API, Power BI, AI/KI, security, operations, migration, and enablement are designed as one system rather than disconnected workstreams.
- **Tenant-proof mapping approach**: Starts from real OData metadata, API samples, and exports, so every customer tenant can be mapped without relying on brittle assumptions.
- **BI-first operational design**: Operational tables, reporting views, semantic models, and KPI definitions are aligned from the beginning.
- **AI with evidence and accountability**: Every AI suggestion can carry confidence, explanation, source references, prompt/model version, feedback, and audit status.
- **Human-in-the-loop where it matters**: Operators retain control over replies, closures, priority changes, sensitive tickets, and customer-facing actions.
- **Power BI that reconciles**: Counts are designed to match TOPdesk selections/exports or explain differences explicitly.
- **Governed self-service**: SSP workflows, knowledge deflection, and chatbot/RAG patterns respect visibility, branch/customer scope, and review status.
- **Operational resilience**: Runbooks, refresh audits, integration checkpoints, and schema-drift handling are built into the delivery model.
- **Data quality as a product feature**: Missing fields, duplicates, unknown dimensions, orphan links, and mapping gaps become visible, owned, and measurable.
- **Lifecycle intelligence**: Status changes, assignment-group handoffs, daily snapshots, durations, and sequence numbers make ticket flow measurable instead of only showing the current state.
- **Bottleneck evidence**: Waiting time by status and operator group identifies where incidents stall, which routing paths create handoff loops, and where service managers should intervene first.
- **Executive control layer**: Connects ticket-level evidence to management levers: SLA risk, backlog aging, routing quality, team workload, data quality, and improvement priority.
- **Auditable service history**: Every lifecycle KPI can be traced back to source export/API evidence, transition facts, daily snapshots, and documented KPI definitions.
- **No black-box lock-in**: Uses portable artifacts such as SQL, CSV, Python, Power Query, DAX, Markdown, and Power BI patterns rather than hiding the logic in a proprietary analytics layer.
- **Free tool, paid value**: The tool/skill assets themselves are free to use; value comes from faster analysis, reusable delivery assets, and reduced implementation effort. TOPdesk, Power BI, hosting, tenant access, implementation, and operations remain separate customer responsibilities.
- **Five-day proof path**: A focused proof-of-value can move from TOPdesk export/API evidence to reconciled bottleneck dashboard, lifecycle drill-through, and ROI hypothesis in one working week.
- **Data trust by design**: Reconciliation differences against TOPdesk selections/exports are surfaced, explained, and owned instead of being hidden behind dashboard totals.
- **Change-readiness for TOPdesk configuration**: Category, status, operator-group, form, and field changes are mapped, tested, and made reportable before they become reporting or automation problems.
- **Operations-ready delivery**: Refresh, schema drift, failed syncs, credential boundaries, package validation, and restart runbooks are part of the value, not afterthoughts.
- **Modular delivery**: Customers can start with reporting, schema cleanup, AI assist, integration, workflow redesign, or business-case discovery.
- **Reusable accelerators**: Templates, scripts, DAX snippets, SQL views, Power Query helpers, prompt schemas, and test cases reduce delivery effort.
- **Executive-ready narrative**: Technical work is tied to measurable outcomes: SLA compliance, time saved, reassignment reduction, reporting trust, deflection, and governance.
- **Operator adoption focus**: Training, quick references, feedback loops, and suggest-only AI reduce friction and improve trust.
- **Compliance by design**: PII, internal notes, secrets, RLS, audit, retention, and AI governance are explicit from the first design step.
- **Continuous improvement loop**: Reports reveal workflow/data issues, AI feedback improves suggestions, knowledge gaps become article candidates, and operations metrics drive roadmap decisions.

## USP Bundles

Data foundation bundle:

- Verified TOPdesk OData/API mapping.
- Clean local schema and reporting views.
- Data-quality dashboard.
- Reconciliation against TOPdesk exports.

Power BI bundle:

- Star-schema semantic model.
- KPI catalog.
- RLS by branch/customer/team.
- Report pages for executives, leads, operations, SLA, assets, knowledge, AI, and data quality.
- Lifecycle facts for status transitions, assignment transitions, and incident daily snapshots.

Lifecycle analytics bundle:

- Status transition fact with `ValidFrom`, `ValidTo`, duration, next status, actor, and sequence.
- Assignment transition fact with operator-group/operator handoffs, duration, and sequence.
- Daily incident snapshots for backlog trend, aging, open/closed state, current status, and current group.
- Power BI measures for time in status, time in group, reassignment rate, open snapshot days, and bottleneck analysis.
- Demo lifecycle data for proof-of-value workshops before production history is fully connected.

Executive control bundle:

- KPI cockpit for SLA risk, backlog age, waiting time, reassignment, routing quality, and improvement priority.
- Drill path from executive KPI to affected team, category, status, group, and individual incident timeline.
- Management-ready narrative that separates process bottlenecks, data-quality issues, configuration gaps, and AI/automation opportunities.

Audit and data trust bundle:

- Reconciliation checks against TOPdesk exports or UI selections.
- Traceable KPI definitions for created, open, closed, overdue, reassigned, time in status, and time in group.
- Source-to-report lineage across raw exports/API payloads, normalized history, snapshots, facts, DAX, and Power BI visuals.
- Explicit labeling of exact event history versus snapshot-only approximation.

No-lock-in delivery bundle:

- Portable CSV import files and SQL reporting views.
- Power Query and DAX templates that can be reviewed and adapted.
- Python scripts for repeatable ingestion and validation.
- Markdown handbooks, battlecards, runbooks, and proof-of-value material.
- No license fee for the skill/plugin assets themselves.

AI assist bundle:

- Ticket classification.
- Smart routing.
- Summaries.
- Draft replies with citations.
- Semantic search/RAG.
- Operator feedback and evaluation metrics.

Governance bundle:

- PII controls.
- Audit logging.
- Secrets handling.
- Human approval gates.
- Runbooks and release gates.
- Permission-aware AI/RAG patterns.
- Prompt/model versioning and feedback metrics.

Adoption bundle:

- Demo storyline.
- Training modules.
- Quick reference cards.
- Adoption metrics.
- Stakeholder-specific messaging.

## Stakeholder-Specific Value

For service desk leads:

- Reduce reassignment and triage effort.
- Improve backlog visibility and SLA focus.
- Standardize intake, categories, and resolution patterns.
- Surface near-breach tickets and repeat issues earlier.
- Identify status and group bottlenecks with duration and P90 evidence.
- Prove whether routing changes reduce handoffs and waiting time.

For operators:

- Better ticket context, summaries, and suggested next actions.
- Faster lookup of knowledge and similar incidents.
- Draft replies that remain operator-reviewed.
- Less manual classification and repetitive routing.

For application managers:

- Clear mapping between TOPdesk configuration, OData/API fields, local schema, and reports.
- Better control over categories, statuses, forms, supporting files, and automation.
- Safer rollout with test and validation checklists.
- Change-ready reporting when categories, statuses, operator groups, forms, or fields evolve.
- Schema-drift and refresh-failure runbooks that make operations supportable.

For management:

- Reliable KPIs with documented definitions.
- Power BI dashboards that reconcile with TOPdesk.
- Insight into demand, SLA, team workload, asset hotspots, and AI impact.
- Governance-ready reporting and auditability.
- Direct line from executive KPI to operational improvement action.
- One-week proof path for bottleneck, backlog, and ROI evidence.

For IT/security/compliance:

- Explicit PII handling and permission boundaries.
- RLS and branch/customer visibility controls.
- Auditable AI suggestions and integration changes.
- No secrets in source, prompts, logs, or operational tables.
- Traceable lifecycle KPIs for audit and compliance conversations.
- No black-box reporting logic; SQL, DAX, Power Query, and scripts stay reviewable.

For CFO/value stakeholders:

- Conservative ROI model for reporting effort, waiting-time reduction, reassignment reduction, and SLA-risk focus.
- Evidence-backed before/after metrics instead of anecdotal process claims.
- Clear separation between baseline, assumption, measured improvement, and estimated value.
- No tool-license cost for the accelerator itself; budget focus shifts to data access, implementation effort, adoption, and operational ownership.

## Feature-to-Benefit Map

| Feature | Benefit |
| --- | --- |
| OData metadata parser | Converts tenant schema into usable field catalogs |
| CSV export profiler | Quickly identifies field types, missing values, and top values |
| Schema blueprint | Speeds up database design and reduces reporting ambiguity |
| Reporting views | Stabilizes Power BI models against operational schema changes |
| DAX/KPI library | Makes service metrics consistent and explainable |
| Status transition fact | Shows how long incidents remain in each status |
| Assignment transition fact | Shows how long incidents remain with each operator group and where handoffs occur |
| Daily snapshot fact | Creates stichtag-style backlog and aging trends instead of relying only on live state |
| Reconciliation checks | Makes TOPdesk-vs-Power-BI differences visible and explainable |
| Source-to-report lineage | Supports audit conversations and troubleshooting |
| Portable SQL/CSV/M/DAX assets | Reduces lock-in and makes the solution reviewable |
| Free skill/plugin assets | Removes tool-license friction for proof-of-value and internal reuse |
| Runbooks and health reports | Makes refresh, sync, and schema-drift failures operable |
| RLS guidance | Protects branch/customer/team data in reports |
| AI classification | Reduces manual triage and improves routing consistency |
| AI summaries | Speeds handoffs and escalations |
| RAG/semantic search | Improves knowledge reuse and self-service quality |
| Feedback loop | Turns operator decisions into measurable improvement data |
| Runbooks | Makes failures diagnosable and recoverable |
| Validation pack | Prevents report, migration, integration, and AI regressions |

## Pitch Lines

Short:

- "A TOPdesk-focused intelligence layer for cleaner data, better reporting, safer automation, and operator-reviewed AI."
- "Make TOPdesk data reportable, auditable, and AI-ready without guessing tenant-specific schema details."
- "From TOPdesk tickets to Power BI KPIs and AI-assisted service workflows, with governance built in."
- "See not only how many tickets are open, but exactly where they waited and how long each handoff took."
- "Turn TOPdesk ticket flow into bottleneck, reassignment, and backlog-aging evidence."
- "In five days, move from TOPdesk export to reconciled lifecycle dashboard and ROI hypothesis."
- "Keep the reporting logic reviewable: SQL, CSV, Power Query, DAX, and documented KPI definitions."
- "Make differences between TOPdesk and Power BI explainable instead of political."
- "Start without an extra tool license; invest effort where value is proven."

Executive:

- "The solution turns TOPdesk operational data into governed analytics and assisted workflows, improving SLA visibility, triage quality, and service transparency while preserving audit and privacy controls."
- "It gives leadership a control layer for service operations: backlog aging, SLA risk, bottlenecks, routing quality, and improvement value with drill-through evidence."

Technical:

- "The approach uses TOPdesk OData/API metadata, explicit external IDs, normalized schema design, reporting views, Power BI semantic modeling, and auditable AI suggestion tables to create a reliable service-management data platform."
- "The implementation remains inspectable through SQL views, CSV facts, Python ingestion, Power Query imports, DAX measures, and validation scripts."

Operator-facing:

- "Operators keep control, but get faster classification, better context, draft replies, knowledge suggestions, and cleaner handoffs."

## Differentiators

- TOPdesk-specific instead of generic ITSM.
- Tenant-verification-first instead of hard-coded assumptions.
- BI, schema, integration, operations, and AI treated as one connected system.
- Lifecycle history and daily snapshots instead of only flat exports or current-state dashboards.
- Process-mining-light for TOPdesk: status paths, handoffs, waiting time, and reassignment loops without requiring a separate process-mining platform.
- Executive-to-incident drill path instead of static management summaries.
- Audit-ready lineage from source data to KPI to visual.
- No-lock-in implementation assets instead of opaque platform logic.
- Free accelerator assets instead of another paid analytics add-on.
- Five-day proof-of-value packaging for fast stakeholder validation.
- Human-in-the-loop AI, not unmanaged automation.
- Strong validation emphasis: every metric, mapping, and automation path must be reconcilable.

## Business Case Metrics

Use these to quantify value:

- Reduction in reassignment rate.
- Reduction in average time in status.
- Reduction in average time in operator group.
- Reduction in waiting-state share.
- Reduction in aging backlog by stichtag snapshot.
- Reduction in average first response time.
- Reduction in average resolution time.
- Increase in SLA compliance.
- Reduction in backlog older than threshold.
- Deflection rate through SSP/knowledge/chatbot.
- Operator AI suggestion acceptance rate.
- Time saved per ticket classification/summary/reply.
- Reduction in Power BI reconciliation differences.
- Reduction in integration failures or manual import corrections.
- Time to produce management reporting pack.
- Number of KPI definitions reconciled and signed off.
- Number of configuration changes tested before report rollout.
- Number of refresh/sync incidents resolved through runbooks.

## Roadmap Framing

Phase 1: Data foundation

- OData/export discovery, schema mapping, reporting views, Power BI model, KPI definitions.
- Baseline reconciliation and source-to-report lineage.

Phase 2: Workflow quality

- SSP form cleanup, category/routing standardization, SLA reporting, data-quality dashboard.
- Lifecycle bottleneck and reassignment review.

Phase 3: AI assist

- Suggest-only classification, summaries, knowledge suggestions, operator feedback.
- AI governance evidence: confidence, explanation, feedback, prompt/model version, and permission scope.

Phase 4: Controlled automation

- High-confidence low-risk auto-routing, duplicate detection, near-breach recommendations, runbook automation.
- Change-readiness checks before categories, statuses, groups, or forms change reporting behavior.

Phase 5: Continuous improvement

- AI monitoring, drift detection, KPI reviews, knowledge maintenance, service optimization.
- Quarterly before/after review for waiting time, reassignment, SLA risk, backlog aging, and reporting effort.

## Objection Handling

Objection: "TOPdesk already has reports."

- Response: "The goal is not to replace TOPdesk reports. The value is governed cross-module analytics, Power BI semantic modeling, RLS, historical views, reconciliation, and AI/automation telemetry that can be combined with other enterprise data."

Objection: "AI in helpdesk is risky."

- Response: "The design starts in suggest-only mode, separates internal and customer-visible content, logs suggestions and feedback, applies permissions before retrieval, and requires human review for sensitive or SLA-impacting actions."

Objection: "Our TOPdesk schema is tenant-specific."

- Response: "That is expected. The approach verifies OData metadata, API samples, and exports before mapping. It avoids hard-coded assumptions and produces a tenant-specific field catalog."

Objection: "Power BI numbers often do not match TOPdesk."

- Response: "The reporting workflow includes explicit KPI definitions and reconciliation against TOPdesk selections/exports so differences are visible, explained, and testable."

Objection: "This sounds like a large platform project."

- Response: "The roadmap is incremental: start with metadata discovery and core incident KPIs, then add workflow improvements, AI suggestions, and controlled automation only where value and risk are clear."

Objection: "We do not want another black-box reporting platform."

- Response: "The delivery uses reviewable artifacts: SQL, CSV, Python, Power Query, DAX, Markdown runbooks, and Power BI model patterns. The logic remains visible and portable."

Objection: "What does the tool cost?"

- Response: "The tool/skill assets themselves are free. Budget items are separate: existing TOPdesk/Power BI licensing, tenant/API access, implementation time, hosting or gateway operation, and optional support."

Objection: "We need proof quickly before committing."

- Response: "Use the five-day proof path: Day 1 data and KPI baseline, Day 2 tenant mapping, Day 3 lifecycle dashboard, Day 4 governance or AI proof, Day 5 ROI and roadmap decision."

Objection: "Historical TOPdesk data is incomplete."

- Response: "The model separates exact event history from daily snapshots. Exact history is used where available; snapshots preserve the state from the first run onward and make gaps explicit."

## Competitive Differentiation

Against generic ITSM analytics:

- More precise TOPdesk terminology and module mapping.
- Built-in handling of TOPdesk OData/API discovery and tenant-specific fields.
- Better connection between schema, reporting, workflow, and AI suggestions.
- More direct executive-to-incident evidence for TOPdesk-specific routing and lifecycle issues.

Against simple Power BI exports:

- Star schema and KPI governance rather than flat export visuals.
- Reconciliation and RLS patterns.
- Reporting views and data-quality checks.
- Historical transition facts and daily snapshots that preserve the process view after the live ticket has changed.
- Reconciliation, lineage, runbooks, and KPI definitions instead of dashboard-only delivery.

Against separate process-mining projects:

- Focused TOPdesk lifecycle measures without a heavy platform rollout.
- Directly usable Power BI facts for status paths, assignment handoffs, waiting time, and reassignment loops.
- Demo data and PoV packaging for fast validation with stakeholders.

Against standalone AI chatbots:

- Operator-reviewed suggestions.
- Audit trail and prompt/model versioning.
- Permission-aware retrieval and separation of internal/public content.
- Feedback loop and measurable acceptance/override rates.
- AI value tied back to TOPdesk KPIs such as reassignment, waiting time, first response, knowledge reuse, and operator edit rate.

Against custom one-off integrations:

- Idempotent sync patterns.
- External ID strategy.
- Integration run logging and reconciliation.
- Runbooks for failed sync and schema drift.

Against proprietary analytics platforms:

- Reviewable implementation assets in SQL, CSV, Python, Power Query, DAX, and Markdown.
- Customer-owned Power BI semantic model and KPI definitions.
- Lower adoption barrier for organizations already standardized on Microsoft analytics.
- No extra license fee for the accelerator assets themselves.

## Persona Pitch Snippets

Service desk lead:

- "Get a reliable view of backlog, SLA risk, category demand, reassignment, and where tickets waited longest, then use AI-assisted triage to reduce avoidable handoffs."

Operator:

- "Keep control of the ticket while getting better summaries, suggested categories, relevant knowledge, and draft replies."

Application manager:

- "Map TOPdesk configuration, OData fields, reports, and local schema into one maintainable model with clear validation checks."
- "Make category, status, group, and field changes report-ready before they break KPI trust."

CIO/IT leader:

- "Improve service transparency and operational efficiency without losing governance over data, permissions, or customer-visible communication."
- "Turn TOPdesk from current-state reporting into a measurable service-flow cockpit with trend, bottleneck, and improvement evidence."

Security/compliance:

- "Protect PII, branch visibility, internal notes, secrets, and AI context with explicit controls and audit records."
- "Trace lifecycle KPIs back to event history, snapshots, source files, and documented calculations."

CFO/value:

- "Use conservative before/after metrics to quantify reporting effort avoided, reassignment reduction, waiting-time reduction, and SLA-risk focus."
- "Because the tool itself is free, the business case can focus on implementation effort, operating model, and measurable service improvement."

## Demo Storyline

1. Start with an incoming incident from SSP or email.
2. Show classification and routing suggestion with confidence and explanation.
3. Show operator-reviewed summary and draft response with knowledge citations.
4. Show the incident flowing into the schema/reporting view.
5. Open Power BI dashboard with created/closed trend, backlog, SLA compliance, and category hotspots.
6. Drill into lifecycle analytics: status duration, operator-group duration, reassignment rate, and daily snapshot backlog.
7. Show one executive KPI drilling down to a team, category, and incident timeline.
8. Drill into reconciliation: TOPdesk export count, Power BI count, difference, and explanation.
9. Drill into data-quality or AI acceptance page.
10. Show audit trail, runbook evidence, and feedback loop.
11. Close with five-day proof path and roadmap: from governed reporting to suggest-only AI to controlled automation.

## ROI Calculation Pattern

Use conservative assumptions:

```text
monthly_time_saved_hours =
  monthly_ticket_volume
  * minutes_saved_per_ticket
  / 60

monthly_value =
  monthly_time_saved_hours
  * blended_operator_hourly_cost

annual_value =
  monthly_value * 12
```

Additional measurable value:

- Reduced SLA penalties or breach handling.
- Reduced manual reporting effort.
- Reduced reassignments.
- Reduced average waiting time in status or operator group.
- Reduced backlog aging visible in daily snapshots.
- Reduced escalation effort through earlier bottleneck detection.
- Reduced duplicate incidents.
- Faster onboarding through clearer workflows and knowledge.
- Lower audit/compliance remediation effort.
- Reduced time spent reconciling report disagreements.
- Reduced risk from untested TOPdesk configuration changes.
- Reduced support effort for refresh and sync failures through runbooks.

## Proof Points to Collect

- Before/after reassignment rate.
- Before/after average time in status.
- Before/after average time in operator group.
- Before/after waiting-state share.
- Snapshot trend for open incidents by age bucket.
- Before/after first response time.
- Before/after backlog older than 7/14/30 days.
- SLA compliance trend.
- AI suggestion acceptance rate.
- Average operator edit rate for draft replies.
- Number of reconciled Power BI KPIs.
- Number of data-quality issues found and resolved.
- Number of source-to-report lineage paths documented.
- Number of operational runbooks tested.
- Number of TOPdesk configuration changes validated against reporting impact.
- Five-day PoV outcome: go/no-go decision, quantified hypotheses, and next roadmap.

## Offer Packaging

Executive control package:

- Outcome: management cockpit for backlog, SLA risk, bottlenecks, routing quality, and value priority.
- Main audience: CIO, IT leadership, service owner, CFO.
- Proof: executive KPI cards with drill-through to lifecycle evidence and ROI assumptions.

Lifecycle bottleneck package:

- Outcome: status and operator-group waiting time, reassignment loops, daily backlog snapshots, and P90 bottlenecks.
- Main audience: service desk lead, operations manager, process owner.
- Proof: `FactStatusTransition`, `FactAssignmentTransition`, `FactIncidentDailySnapshot`, and ranked bottleneck visuals.

Data trust package:

- Outcome: reconciled Power BI numbers and documented KPI definitions.
- Main audience: management, reporting owner, application manager.
- Proof: TOPdesk-vs-Power-BI count reconciliation, source-to-report lineage, and signed-off KPI catalog.

Change-readiness package:

- Outcome: safer TOPdesk changes to categories, statuses, groups, forms, and fields.
- Main audience: application manager, process owner, reporting owner.
- Proof: before/after mapping, report impact checklist, validation cases, and rollback notes.

AI governance package:

- Outcome: suggest-only AI with audit, permissions, feedback, and KPI impact tracking.
- Main audience: service desk lead, operators, security, compliance.
- Proof: suggestion log, confidence/explanation, prompt/model version, feedback metrics, and acceptance/override reporting.

Operations-ready package:

- Outcome: refresh, sync, schema-drift, credential, and package validation runbooks.
- Main audience: IT operations, BI owner, integration owner.
- Proof: health report, MCP smoke test, plugin verification, package checksum, and tested runbooks.
