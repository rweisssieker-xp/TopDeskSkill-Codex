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
- **Modular delivery**: Customers can start with reporting, schema cleanup, AI assist, integration, workflow redesign, or business-case discovery.
- **Reusable accelerators**: Templates, scripts, DAX snippets, SQL views, Power Query helpers, prompt schemas, and test cases reduce delivery effort.
- **Executive-ready narrative**: Technical work is tied to measurable outcomes: SLA compliance, time saved, reassignment reduction, reporting trust, deflection, and governance.
- **Operator adoption focus**: Training, quick references, feedback loops, and suggest-only AI reduce friction and improve trust.
- **Compliance by design**: PII, internal notes, secrets, RLS, audit, retention, and AI governance are explicit from the first design step.
- **Continuous improvement loop**: Reports reveal workflow/data issues, AI feedback improves suggestions, knowledge gaps become article candidates, and operations metrics drive roadmap decisions.

## Skill Suite Meta-USP

A complete TOPdesk delivery and intelligence skill system: tenant-verified, Power BI-ready, AI-governed, auditable, operationalizable, and business-case-ready from discovery to production operations.

Use this when positioning the skill system itself rather than a customer project:

- 39 validated specialized skills.
- Tenant metadata and exports treated as source of truth.
- Deep Power BI model, KPI, DAX, RLS, and reconciliation support.
- Lifecycle history with status transitions, assignment transitions, and daily snapshots.
- AI/KI patterns with human review, audit, PII controls, and feedback loops.
- End-to-end delivery from discovery to operations and ROI.
- Scripts and templates for repeatable execution.
- Handbook, CI, validation, packaging, and release support.

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

For operators:

- Better ticket context, summaries, and suggested next actions.
- Faster lookup of knowledge and similar incidents.
- Draft replies that remain operator-reviewed.
- Less manual classification and repetitive routing.

For application managers:

- Clear mapping between TOPdesk configuration, OData/API fields, local schema, and reports.
- Better control over categories, statuses, forms, supporting files, and automation.
- Safer rollout with test and validation checklists.

For management:

- Reliable KPIs with documented definitions.
- Power BI dashboards that reconcile with TOPdesk.
- Insight into demand, SLA, team workload, asset hotspots, and AI impact.
- Governance-ready reporting and auditability.

For IT/security/compliance:

- Explicit PII handling and permission boundaries.
- RLS and branch/customer visibility controls.
- Auditable AI suggestions and integration changes.
- No secrets in source, prompts, logs, or operational tables.

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

Executive:

- "The solution turns TOPdesk operational data into governed analytics and assisted workflows, improving SLA visibility, triage quality, and service transparency while preserving audit and privacy controls."

Technical:

- "The approach uses TOPdesk OData/API metadata, explicit external IDs, normalized schema design, reporting views, Power BI semantic modeling, and auditable AI suggestion tables to create a reliable service-management data platform."

Operator-facing:

- "Operators keep control, but get faster classification, better context, draft replies, knowledge suggestions, and cleaner handoffs."

## Differentiators

- TOPdesk-specific instead of generic ITSM.
- Tenant-verification-first instead of hard-coded assumptions.
- BI, schema, integration, operations, and AI treated as one connected system.
- Lifecycle history and daily snapshots instead of only flat exports or current-state dashboards.
- Process-mining-light for TOPdesk: status paths, handoffs, waiting time, and reassignment loops without requiring a separate process-mining platform.
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

## Roadmap Framing

Phase 1: Data foundation

- OData/export discovery, schema mapping, reporting views, Power BI model, KPI definitions.

Phase 2: Workflow quality

- SSP form cleanup, category/routing standardization, SLA reporting, data-quality dashboard.

Phase 3: AI assist

- Suggest-only classification, summaries, knowledge suggestions, operator feedback.

Phase 4: Controlled automation

- High-confidence low-risk auto-routing, duplicate detection, near-breach recommendations, runbook automation.

Phase 5: Continuous improvement

- AI monitoring, drift detection, KPI reviews, knowledge maintenance, service optimization.

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

## Competitive Differentiation

Against generic ITSM analytics:

- More precise TOPdesk terminology and module mapping.
- Built-in handling of TOPdesk OData/API discovery and tenant-specific fields.
- Better connection between schema, reporting, workflow, and AI suggestions.

Against simple Power BI exports:

- Star schema and KPI governance rather than flat export visuals.
- Reconciliation and RLS patterns.
- Reporting views and data-quality checks.
- Historical transition facts and daily snapshots that preserve the process view after the live ticket has changed.

Against separate process-mining projects:

- Focused TOPdesk lifecycle measures without a heavy platform rollout.
- Directly usable Power BI facts for status paths, assignment handoffs, waiting time, and reassignment loops.
- Demo data and PoV packaging for fast validation with stakeholders.

Against standalone AI chatbots:

- Operator-reviewed suggestions.
- Audit trail and prompt/model versioning.
- Permission-aware retrieval and separation of internal/public content.
- Feedback loop and measurable acceptance/override rates.

Against custom one-off integrations:

- Idempotent sync patterns.
- External ID strategy.
- Integration run logging and reconciliation.
- Runbooks for failed sync and schema drift.

## Persona Pitch Snippets

Service desk lead:

- "Get a reliable view of backlog, SLA risk, category demand, reassignment, and where tickets waited longest, then use AI-assisted triage to reduce avoidable handoffs."

Operator:

- "Keep control of the ticket while getting better summaries, suggested categories, relevant knowledge, and draft replies."

Application manager:

- "Map TOPdesk configuration, OData fields, reports, and local schema into one maintainable model with clear validation checks."

CIO/IT leader:

- "Improve service transparency and operational efficiency without losing governance over data, permissions, or customer-visible communication."
- "Turn TOPdesk from current-state reporting into a measurable service-flow cockpit with trend, bottleneck, and improvement evidence."

Security/compliance:

- "Protect PII, branch visibility, internal notes, secrets, and AI context with explicit controls and audit records."

## Demo Storyline

1. Start with an incoming incident from SSP or email.
2. Show classification and routing suggestion with confidence and explanation.
3. Show operator-reviewed summary and draft response with knowledge citations.
4. Show the incident flowing into the schema/reporting view.
5. Open Power BI dashboard with created/closed trend, backlog, SLA compliance, and category hotspots.
6. Drill into lifecycle analytics: status duration, operator-group duration, reassignment rate, and daily snapshot backlog.
7. Drill into data-quality or AI acceptance page.
8. Show audit trail and feedback loop.
9. Close with roadmap: from suggest-only to controlled automation.

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
