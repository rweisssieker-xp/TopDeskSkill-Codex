# USP Battlecards

## Persona Angles

- CIO: governed intelligence, reduced delivery risk, reusable platform.
- CFO: measurable ROI, reporting effort reduction, waiting-time value, better investment decisions.
- Service desk lead: fewer reassignments, SLA focus, operator productivity.
- Service desk lead: bottleneck evidence, shorter waiting time, fewer avoidable handoffs.
- Operator: better summaries, suggested replies, less context switching.
- Application manager: cleaner configuration, better tenant mapping, safer changes.
- Security/privacy: audit, PII controls, RLS, approval gates, traceable KPI lineage.
- BI owner: reconciled KPI definitions, source-to-report lineage, no black-box logic.
- IT operations: supportable refresh, sync, schema-drift, and package verification.

## Competitors

- Manual Excel reporting.
- Generic ChatGPT prompts.
- Pure Power BI implementation.
- Pure TOPdesk consulting.
- Point automation scripts.
- Separate process-mining platforms.
- Proprietary analytics platforms.
- Generic Copilot/ChatGPT workflows without TOPdesk evidence, permissions, or feedback loops.

## Battlecard Fields

- Positioning line.
- Top pains.
- Differentiators.
- Proof points.
- Objections and answers.
- Demo moment.
- Power BI evidence.
- AI/KI governance evidence.
- Reconciliation evidence.
- Runbook/operations evidence.

## Lifecycle Analytics Battlecard

Positioning line:

- "TOPdesk reporting that explains where incidents waited, not only how many are open."

Top pains:

- Current-state reports hide earlier status and assignment changes.
- Teams cannot prove where tickets stalled or why SLA risk increased.
- Reassignment and handoff loops are visible anecdotally but not measured consistently.
- Daily backlog trend is hard to reconstruct after tickets move or close.

Differentiators:

- Status transition fact with duration and sequence.
- Assignment transition fact with operator-group duration and handoff sequence.
- Daily snapshot fact for stichtag backlog, aging, and open/closed state.
- Power BI-ready KPIs for waiting time, reassignment rate, P90 duration, and bottleneck ranking.
- Demo lifecycle CSVs for workshops before production history is connected.

Proof points:

- Generated demo pack includes `FactIncidentDailySnapshot`, `FactStatusTransition`, and `FactAssignmentTransition`.
- Lifecycle validation checks required fields, interval order, duration math, and sequence continuity.
- SQL, DAX, Power Query, and model references all point to the same fact pattern.

Objections and answers:

- "TOPdesk already shows the ticket status." Response: "That is the current or ticket-level view. The lifecycle model preserves each interval, so you can measure how long a ticket stayed in every status and group."
- "We do not have perfect historical events yet." Response: "Use event history where available and daily snapshots from the first run onward. The model separates exact transitions from snapshot evidence, so gaps are explicit."
- "Process mining sounds too large." Response: "This is a focused TOPdesk lifecycle layer in Power BI: status paths, handoffs, waiting time, and backlog aging without a separate platform rollout."

Demo moment:

- Pick one incident and show the status timeline, assignment timeline, and daily snapshots side by side.
- Then aggregate to average/P90 time in status and operator group.
- Finish with a ranked bottleneck table by group, status, priority, or category.

Power BI evidence:

- Cards: open snapshot incidents, average time in status, average time in operator group, reassignment rate.
- Trend: open incident days by snapshot date.
- Bar chart: P90 duration by operator group or status.
- Detail table: incident key, sequence, status/group, valid from, valid to, duration.

## Executive Control Battlecard

Positioning line:

- "A TOPdesk service cockpit that turns ticket data into management levers."

Top pains:

- Leadership sees volumes but not the operational reason behind SLA risk or backlog growth.
- Service improvement priorities compete without comparable evidence.
- Reports stop at dashboard summaries and do not drill to process facts.

Differentiators:

- Executive KPI to group/category/status/incident drill path.
- Lifecycle duration and daily snapshot evidence behind management cards.
- ROI hypotheses tied to waiting time, reassignment, reporting effort, and SLA-risk focus.
- Separates process bottlenecks, configuration gaps, data-quality issues, and AI opportunities.

Proof points:

- Lifecycle facts and snapshots validate interval duration and trend history.
- KPI definitions and reconciliation checks show whether Power BI matches TOPdesk or why it differs.
- PoV package can show a management question, root cause, and next action in one week.

Objections and answers:

- "Executives do not need ticket detail." Response: "They need drill-through evidence when a KPI changes. The detail is not for daily use; it makes decisions defensible."
- "This is just another dashboard." Response: "The value is the control loop: KPI, bottleneck evidence, owner, action, and before/after measurement."

Demo moment:

- Start from SLA risk or aged backlog, drill into a group/status bottleneck, then open one incident timeline.

Power BI evidence:

- Executive cards: backlog, SLA at risk, average/P90 waiting time, reassignment rate, data trust score.
- Drill-through: category/group/status to incident timeline.
- Matrix: improvement priority by impact and evidence quality.

## Data Trust And Audit Battlecard

Positioning line:

- "Make TOPdesk reporting trustworthy by showing definitions, differences, and lineage."

Top pains:

- Management meetings debate numbers instead of decisions.
- Power BI totals differ from TOPdesk exports or UI selections.
- Audit/compliance stakeholders need to know where KPIs came from.

Differentiators:

- Explicit KPI definitions and grain per fact table.
- Reconciliation table for source count, Power BI count, difference, and explanation.
- Source-to-report lineage across export/API, staging, fact, measure, and visual.
- Clear distinction between exact event history and snapshot-only approximation.

Proof points:

- Reconciled incident counts and documented exceptions.
- DAX and Power Query templates are inspectable.
- Daily snapshots and transition facts preserve historical evidence after tickets change.

Objections and answers:

- "Power BI never matches operational systems perfectly." Response: "That is why the model documents grain, filters, and reconciliation differences instead of hiding them."
- "Audit does not need dashboards." Response: "Audit needs traceability. The dashboard is only one endpoint of the documented lineage."

Demo moment:

- Pick one KPI and show TOPdesk export count, model count, DAX definition, filters, and explanation of any difference.

## No-Lock-In Battlecard

Positioning line:

- "Reviewable TOPdesk intelligence without a proprietary analytics black box."

Top pains:

- Customers do not want another opaque platform.
- Reporting logic is hard to review, transfer, or operate.
- One-off scripts solve the immediate problem but create support risk.

Differentiators:

- Uses SQL, CSV, Python, Power Query, DAX, Markdown, and Power BI.
- Package verification creates a distributable ZIP and checksum.
- Runbooks and validation scripts make delivery repeatable.

Proof points:

- Plugin verification packages and tests 39 skills.
- Lifecycle demo data and import files can be inspected directly.
- Measures, queries, and scripts are versionable artifacts.

Objections and answers:

- "We already have Microsoft BI." Response: "This approach works with that standard instead of replacing it."
- "Custom scripts are risky." Response: "The scripts are paired with validation, package tests, checksums, and runbooks."

Demo moment:

- Show one metric flowing through CSV, Power Query, DAX, visual, and validation evidence.

## AI Governance Battlecard

Positioning line:

- "AI assistance for TOPdesk that stays measurable, permission-aware, and operator-controlled."

Top pains:

- Generic AI tools do not know TOPdesk context or permissions.
- Teams worry about customer-visible replies, PII, and internal notes.
- AI value is hard to prove after a pilot.

Differentiators:

- Suggest-only patterns with human review.
- Confidence, explanation, source references, prompt/model version, and feedback.
- Permission-aware retrieval and separation of internal/customer-visible content.
- AI KPIs tied to acceptance rate, edit rate, reassignment, first response, and knowledge reuse.

Proof points:

- AI suggestion tables and governance cockpit patterns.
- Operator feedback loop and acceptance/override metrics.
- Security and RLS guidance for sensitive ticket content.

Objections and answers:

- "AI in service desk is risky." Response: "The first phase is reviewed suggestions with audit and feedback, not unattended actions."
- "How do we prove AI value?" Response: "Track accepted suggestions, edits, time saved assumptions, and downstream service KPIs."

Demo moment:

- Show a routing or summary suggestion with confidence, source, operator action, and logged feedback.

## Operations Readiness Battlecard

Positioning line:

- "A TOPdesk intelligence solution that can be operated after the demo."

Top pains:

- Dashboards break when exports, fields, credentials, or refresh schedules change.
- Integrations fail without clear ownership or recovery steps.
- Plugin/package updates lack release evidence.

Differentiators:

- Refresh, sync, schema-drift, credential, and rollback runbooks.
- Plugin health report, MCP smoke test, package verification, checksum.
- Validation gates for skills, Python scripts, references, lifecycle demo data, and package extraction.

Proof points:

- `verify_plugin.ps1` syncs, validates, packages, tests, and writes checksum.
- Lifecycle validation checks row counts, required fields, interval order, duration math, and sequence continuity.
- `.mcp.json` is credential-neutral for distribution.

Objections and answers:

- "The demo works, but who supports it?" Response: "Operations readiness is part of the package: runbooks, validation gates, health report, and ownership model."
- "Credentials and tenant details are sensitive." Response: "The plugin bundle stays credential-neutral; tenant secrets belong in local environment configuration."

Demo moment:

- Run or show plugin verification evidence, package ZIP, checksum, and health report.
