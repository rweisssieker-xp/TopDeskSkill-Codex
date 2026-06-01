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
- CIO: service intelligence operating model, decision-to-action loop, readiness gates.
- CFO: evidence-backed value hypotheses, process debt cost, AI adoption value, reporting effort reduction.
- Process owner: improvement backlog from data-quality, lifecycle, SLA, and routing evidence.
- Implementation partner: repeatable consulting IP packaged as customer-owned artifacts.

## Competitors

- Manual Excel reporting.
- Generic ChatGPT prompts.
- Pure Power BI implementation.
- Pure TOPdesk consulting.
- Point automation scripts.
- Separate process-mining platforms.
- Proprietary analytics platforms.
- Generic Copilot/ChatGPT workflows without TOPdesk evidence, permissions, or feedback loops.
- Generic AI adoption dashboards with no TOPdesk-specific acceptance, override, or process-impact evidence.
- Heavy process-mining rollouts where a lightweight TOPdesk lifecycle proof would be enough.

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

## Tenant Drift Radar Battlecard

Positioning line:

- "Detect TOPdesk tenant drift before it silently breaks reporting, automation, or AI."

Top pains:

- Categories, statuses, fields, groups, permissions, and OData/API shapes change over time.
- Power BI reports and AI prompts can degrade without an obvious error.
- Teams cannot explain why the same KPI or automation behaved differently after configuration changes.

Differentiators:

- Compares previous and current field catalogs, labels, option sets, endpoint availability, and KPI dependencies.
- Classifies impact for Power BI, AI/KI, automation, security, and operations.
- Separates harmless metadata changes from changes that require model, prompt, automation, or RLS review.

Proof points:

- Tenant mapping and OData skills already produce field catalogs and mapping evidence.
- Plugin verification and production-readiness gates provide a repeatable package boundary.
- Drift can be reported as Markdown and CSV without storing tenant credentials in source.

Objections and answers:

- "We do not change TOPdesk often." Response: "Even small category, group, or custom-field changes can alter reporting filters, routing logic, or AI context."
- "Power BI refresh tells us when something breaks." Response: "Refresh only catches some failures. Drift radar also catches semantic changes that still refresh but change meaning."

Demo moment:

- Show two field catalogs and a drift table with change type, affected KPI, risk class, owner, and recommended action.

## Process Debt Detector Battlecard

Positioning line:

- "Expose the hidden service-process debt behind backlog, SLA risk, and operator frustration."

Top pains:

- Handoff loops, stale ownership, reopen patterns, category waste, and status waiting zones are discussed anecdotally.
- Teams know work is stuck but cannot prioritize which process issue matters most.
- Improvement backlogs are often opinion-driven instead of evidence-driven.

Differentiators:

- Uses lifecycle facts, SLA findings, data-quality findings, and routing evidence.
- Converts patterns into backlog-ready findings with impact, evidence, owner suggestion, and validation metric.
- Keeps the scope lightweight: focused TOPdesk process evidence, not a broad process-mining rollout.

Proof points:

- Lifecycle demo data already models status and assignment transitions.
- SLA optimizer and data-quality skills provide complementary risk signals.
- Power BI-ready measures can show before/after movement after process changes.

Objections and answers:

- "We already know our pain points." Response: "This turns known pain into ranked evidence and validates whether fixes worked."
- "Process mining is too much." Response: "This is a targeted TOPdesk analyzer for handoffs, waits, reopens, ownership, and routing."

Demo moment:

- Start with aged backlog, drill into repeated handoffs, show a process-debt finding, and convert it to an improvement backlog item.

## AI Adoption Ledger Battlecard

Positioning line:

- "Prove whether TOPdesk AI assistance is adopted, trusted, edited, rejected, and worth scaling."

Top pains:

- AI pilots look good in demos but lose credibility after rollout.
- Acceptance, edit effort, override reasons, costs, and downstream impact are not tracked consistently.
- Security and operations teams need evidence before AI expands to customer-visible work.

Differentiators:

- Tracks suggestion type, confidence, source reference, accepted/edited/rejected state, override reason, cost estimate, and time-saved assumption.
- Links AI adoption to service KPIs such as reassignment, first response, knowledge reuse, and SLA-risk focus.
- Maintains operator control and auditability instead of unattended automation claims.

Proof points:

- AI governance cockpit patterns already include prompt/model version, feedback loops, confidence, and cost.
- Security guidance covers PII, permission-aware retrieval, and human approval.
- DAX and Power BI patterns can report adoption and override trends.

Objections and answers:

- "AI value is hard to measure." Response: "The ledger turns use into measurable adoption, edit effort, override reasons, and value assumptions."
- "Operators may not trust AI." Response: "Trust is measured directly through acceptance, edits, rejection, and feedback."

Demo moment:

- Show an AI suggestion lifecycle from generated recommendation to operator action, override reason, and governance metric.

## Automation Safety Sandbox Battlecard

Positioning line:

- "Review TOPdesk automations before production: trigger, payload, retry, rollback, PII, and audit."

Top pains:

- Action sequences and scripts can create duplicate work, noisy updates, or hard-to-debug failures.
- Automation design often skips rollback, idempotency, dead-letter, and PII review.
- Teams need a go/no-go gate before enabling workflow-changing actions.

Differentiators:

- Scores trigger quality, payload mapping, idempotency, retry behavior, rollback path, dead-letter handling, audit fields, and human approval boundaries.
- Produces an automation risk card before production use.
- Keeps credentials and customer tenant details outside plugin source.

Proof points:

- Action sequence skill already covers triggers, payload mapping, retries, idempotency, monitoring, and audit.
- Production-readiness gates require rollback or disable procedures for automated workflows.
- Runbook templates support operational handover.

Objections and answers:

- "It is only a small automation." Response: "Small automations still need idempotency, error handling, and audit when they touch tickets or customer-visible updates."
- "We can test manually." Response: "Manual testing is useful; the sandbox makes the risk checklist repeatable and reviewable."

Demo moment:

- Walk through one proposed action sequence and produce a risk card with go/no-go recommendation.

## Service Desk Digital Twin Light Battlecard

Positioning line:

- "Run lightweight TOPdesk what-if scenarios before changing routing, SLA, capacity, or AI support."

Top pains:

- Process changes are approved without clear expected KPI movement.
- Leaders ask whether fewer handoffs, category cleanup, or AI routing would matter, but teams lack a bounded simulation.
- Heavy process-mining or simulation platforms can be too large for early decisions.

Differentiators:

- Uses existing lifecycle, SLA, routing, and data-quality evidence for simple scenario assumptions.
- Models expected direction of impact for handoffs, waiting time, SLA risk, backlog age, or operator-group load.
- Keeps assumptions explicit and reviewable.

Proof points:

- Lifecycle facts and daily snapshots provide baseline behavior.
- ROI and proof-of-value skills already structure value hypotheses and assumptions.
- Outputs remain Markdown/CSV/Power BI-ready, not a black-box simulation.

Objections and answers:

- "A simple model is not exact." Response: "It is decision support, not a forecast guarantee. The value is explicit assumptions and comparable scenarios."
- "We need real proof." Response: "Use the scenario to choose a controlled pilot, then validate with before/after KPIs."

Demo moment:

- Compare three scenarios: reduce reassignments, clean categories, or add AI routing support, then rank by expected impact and confidence.

## Readiness Scoring Battlecard

Positioning line:

- "Know whether the tenant is ready for reporting, AI, automation, and operations before investing."

Top pains:

- Projects start before data, permissions, ownership, privacy, or operations are ready.
- Readiness risks appear late, after demos or report work already consumed budget.
- Stakeholders need a simple view of blockers and next actions.

Differentiators:

- Scores reporting readiness, AI readiness, data trust, automation readiness, security/privacy, and operations readiness.
- Converts red/amber/green scores into blockers, required evidence, and recommended next step.
- Works for sales qualification, proof-of-value, project kickoff, and steering readout.

Proof points:

- Production-readiness gates already define tenant, data, privacy, operations, and commercial boundaries.
- Testing and security skills provide acceptance, RLS, PII, and release-gate checks.
- Proof-of-value and project-delivery skills can turn scores into a roadmap.

Objections and answers:

- "Scoring sounds subjective." Response: "The score is based on explicit evidence requirements and documented blockers."
- "We want to start building." Response: "Readiness scoring prevents building on missing permissions, unclear data, or unsupported operating models."

Demo moment:

- Show a readiness scorecard with one red blocker, two amber risks, and a next-step plan.

## Decision-Ready Findings Battlecard

Positioning line:

- "Every TOPdesk analysis should end with an action-ready finding, not only a chart."

Top pains:

- Dashboards show symptoms but do not assign owner, risk, or next action.
- Management readouts need concise decisions, not only detailed report pages.
- Technical findings often fail to become improvement work.

Differentiators:

- Standard finding format: finding, evidence, business impact, risk, recommended action, owner, validation metric.
- Reusable across report factory, proof-of-value, SLA optimizer, data quality, AI governance, and operations.
- Makes workshop outputs backlog-ready.

Proof points:

- Existing skills already produce data-quality, SLA, lifecycle, AI, and report evidence.
- Project delivery and proof-of-value skills can convert findings into epics, stories, and acceptance criteria.
- Executive one-pager templates support decision readouts.

Objections and answers:

- "We just need the data." Response: "Data is useful, but improvement requires a decision, owner, and validation metric."
- "Owners are political." Response: "The finding can propose an owner and make unresolved ownership visible as a risk."

Demo moment:

- Convert one SLA-risk visual into a finding card with evidence, action, owner, and 30-day validation metric.

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

- Offline lifecycle pack includes `FactIncidentDailySnapshot`, `FactStatusTransition`, and `FactAssignmentTransition`.
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

- Plugin verification packages and tests 48 skills.
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

## Service Intelligence Runtime Battlecard

Positioning line:

- "A repeatable TOPdesk operating cycle, not another one-off analysis."

Top pains:

- Individual reports and scripts do not create a monthly operating rhythm.
- Live connector discussions stall because credentials, scope, retention, and owner are unclear.
- Management needs one readout across drift, process debt, AI adoption, automation risk, readiness, and next actions.

Differentiators:

- Runtime config connects approved exports, optional connector preflight, module selection, governance owner, retention, and approval reference.
- Orchestrator runs the analyzer packs and writes a run plan, run history, operational gates, Markdown readout, and local HTML dashboard.
- Live access remains explicit and tenant-controlled through environment variables and endpoint-level export commands.

Proof points:

- `run_service_intelligence.py` executes the local operating cycle.
- `topdesk_live_connector.py preflight` checks credential readiness without fetching data.
- Runtime outputs include `runtime-plan.json`, `runtime-readout.md`, `runtime-dashboard.html`, `operational-gates.csv`, and `runtime-history.jsonl`.

Objections and answers:

- "Is this now a hosted product?" Response: "No. It is a local runtime and operating model. Hosting, scheduler, secret store, web app, monitoring, and support are scoped separately."
- "Can it use real TOPdesk data?" Response: "Yes, when the tenant approves credentials, endpoints, purpose, retention, and security controls. Until then it runs from approved exports."

Demo moment:

- Run a dry plan, then execute the runtime on approved sample exports and open the generated HTML dashboard plus operational gates.
