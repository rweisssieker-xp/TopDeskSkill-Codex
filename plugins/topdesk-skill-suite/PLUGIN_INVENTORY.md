# TOPdesk Skill Suite Plugin Inventory

Generated: 2026-06-01T17:27:03+02:00

Skill count: 48

| Skill | References | Scripts | Assets |
| --- | ---: | ---: | ---: |
| `topdesk-action-sequences` | 1 | 0 | 0 |
| `topdesk-admin-config` | 1 | 0 | 0 |
| `topdesk-ai` | 4 | 0 | 0 |
| `topdesk-ai-adoption-ledger` | 1 | 1 | 0 |
| `topdesk-ai-feature-factory` | 2 | 1 | 3 |
| `topdesk-ai-governance-cockpit` | 2 | 1 | 3 |
| `topdesk-api-test-lab` | 0 | 1 | 0 |
| `topdesk-assets` | 1 | 0 | 0 |
| `topdesk-automation-sandbox` | 1 | 1 | 0 |
| `topdesk-changes` | 1 | 0 | 0 |
| `topdesk-compliance-pii` | 0 | 1 | 0 |
| `topdesk-data-quality` | 1 | 0 | 0 |
| `topdesk-decision-findings` | 1 | 1 | 0 |
| `topdesk-digital-twin-light` | 1 | 1 | 0 |
| `topdesk-enablement` | 1 | 0 | 0 |
| `topdesk-executive-narrative` | 1 | 1 | 0 |
| `topdesk-expert` | 26 | 3 | 0 |
| `topdesk-handbook` | 10 | 0 | 0 |
| `topdesk-integration` | 5 | 1 | 0 |
| `topdesk-knowledge` | 1 | 0 | 0 |
| `topdesk-major-incidents` | 1 | 0 | 0 |
| `topdesk-migration` | 1 | 0 | 0 |
| `topdesk-odata` | 3 | 4 | 0 |
| `topdesk-operations` | 3 | 0 | 1 |
| `topdesk-powerbi` | 10 | 5 | 3 |
| `topdesk-powerbi-dax` | 0 | 1 | 1 |
| `topdesk-powerbi-modelling` | 2 | 1 | 2 |
| `topdesk-powershell` | 2 | 1 | 1 |
| `topdesk-process-debt` | 1 | 1 | 0 |
| `topdesk-project-delivery` | 1 | 0 | 0 |
| `topdesk-proof-of-value` | 2 | 1 | 3 |
| `topdesk-python` | 2 | 1 | 1 |
| `topdesk-query-powerbi` | 2 | 1 | 1 |
| `topdesk-readiness-scoring` | 1 | 1 | 0 |
| `topdesk-report-factory` | 1 | 0 | 0 |
| `topdesk-roi-business-case` | 1 | 0 | 0 |
| `topdesk-schema` | 4 | 0 | 1 |
| `topdesk-security` | 3 | 0 | 0 |
| `topdesk-service-intelligence-runtime` | 1 | 5 | 1 |
| `topdesk-sla-optimizer` | 0 | 1 | 0 |
| `topdesk-template-pack` | 1 | 0 | 2 |
| `topdesk-tenant-drift` | 1 | 1 | 0 |
| `topdesk-tenant-mapping` | 1 | 1 | 0 |
| `topdesk-testing` | 2 | 0 | 1 |
| `topdesk-usp-battlecards` | 2 | 1 | 3 |
| `topdesk-usps` | 5 | 0 | 0 |
| `topdesk-visual-design` | 2 | 1 | 2 |
| `topdesk-workflows` | 3 | 0 | 0 |

## Skills

### `topdesk-action-sequences`

TOPdesk Action Sequences and automation design. Use for action sequence triggers, webhooks, API calls, payload mapping, idempotency, retries, error handling, safe automation boundaries, audit logging, and automation monitoring.

References:
- `references/action-sequences.md`

### `topdesk-admin-config`

TOPdesk administration and configuration design. Use for categories, statuses, priorities, impact/urgency, supporting files, branches, persons, operators, operator groups, permissions, SSP forms, service catalog items, change templates, asset templates, knowledge visibility, and configuration governance.

References:
- `references/admin-config.md`

### `topdesk-ai`

Design, implement, and evaluate AI/KI features for TOPdesk workflows. Use for ticket classification, smart routing, summaries, response suggestions, knowledge article generation, semantic search, RAG, chatbot/self-service assistants, duplicate detection, SLA-risk prediction, prompt templates, JSON schemas, operator feedback loops, AI governance, and regression evaluation.

References:
- `references/ai-features.md`
- `references/ai-prompts-and-evals.md`
- `references/security-compliance.md`
- `references/testing-validation.md`

### `topdesk-ai-adoption-ledger`

Build TOPdesk AI/KI adoption ledgers and monitoring summaries from suggestion logs, operator feedback, acceptance/edit/rejection events, override reasons, confidence, cost estimates, prompt/model versions, and value assumptions.

References:
- `references/ai-adoption-ledger.md`

Scripts:
- `scripts/build_ai_adoption_ledger.py`

### `topdesk-ai-feature-factory`

Generate complete governed AI/KI feature packs for TOPdesk. Use for turning an AI use case into feature scope, data contract, prompt design, JSON output schema, evaluation dataset, feedback loop, audit fields, rollout gates, Power BI monitoring measures, RLS/PII controls, and operator-facing acceptance criteria.

References:
- `references/ai-feature-factory.md`
- `references/powerbi-ai-monitoring.md`

Scripts:
- `scripts/new_ai_feature_pack.py`

Assets:
- `assets/ai-eval-dataset-template.csv`
- `assets/ai-feature-pack-template.md`
- `assets/ai-monitoring-measures.dax`

### `topdesk-ai-governance-cockpit`

Design Power BI governance cockpits for TOPdesk AI/KI features. Use for AI monitoring datasets, semantic models, DAX measures, report pages, prompt/model version tracking, suggestion acceptance, override reasons, confidence drift, cost, token usage, SLA impact, PII/policy findings, feedback loops, evaluation results, RLS, and audit reporting.

References:
- `references/governance-cockpit-model.md`
- `references/governance-kpis.md`

Scripts:
- `scripts/new_governance_cockpit_spec.py`

Assets:
- `assets/ai-governance-measures.dax`
- `assets/ai-governance-theme.json`
- `assets/governance-cockpit-spec-template.md`

### `topdesk-api-test-lab`

Use when testing live TOPdesk REST/API access, authentication, endpoint availability, paging behavior, response status codes, payload shapes, demo tenants, smoke tests, regression checks, and API readiness before building Power BI, Python, PowerShell, or AI features.

Scripts:
- `scripts/smoke_topdesk_api.py`

### `topdesk-assets`

TOPdesk Asset Management design, schema, analytics, and workflow support. Use for asset templates, dynamic asset fields, asset relations, owner/branch/location mapping, lifecycle, incident/change links, CMDB-like reporting, asset data quality, and asset KPIs.

References:
- `references/asset-management.md`

### `topdesk-automation-sandbox`

Review TOPdesk action sequences, webhooks, scheduled jobs, integration scripts, and automation designs for trigger quality, payload mapping, idempotency, retry behavior, rollback, dead-letter handling, PII, audit, human approval, and production go/no-go risk.

References:
- `references/automation-sandbox.md`

Scripts:
- `scripts/review_automation_risk.py`

### `topdesk-changes`

TOPdesk Change Management design and reporting. Use for change templates, standard/simple/extensive changes, activities, approvals, risk/impact, scheduling, linked incidents/assets, change audit, change KPIs, and change workflow tests.

References:
- `references/change-management.md`

### `topdesk-compliance-pii`

Use when reviewing TOPdesk exports, REST snapshots, field catalogs, Power BI datasets, AI prompts, RAG sources, reports, or demos for PII exposure, privacy minimization, masking, retention, security boundaries, and compliance risks.

Scripts:
- `scripts/scan_pii_catalog.py`

### `topdesk-data-quality`

TOPdesk data-quality analysis and cleanup planning. Use for missing callers/branches/categories/statuses, duplicate persons/assets, orphaned links, mapping gaps, invalid dates, unknown Power BI dimensions, RLS data risks, AI label quality, cleanup backlogs, and BI data-quality pages.

References:
- `references/data-quality.md`

### `topdesk-decision-findings`

Generate decision-ready TOPdesk findings from analysis CSV files, SLA findings, data-quality findings, process-debt outputs, AI governance rows, or manual finding drafts using a standard evidence, impact, risk, action, owner, and validation metric format.

References:
- `references/decision-findings.md`

Scripts:
- `scripts/build_decision_findings.py`

### `topdesk-digital-twin-light`

Run lightweight TOPdesk service desk what-if scenario scoring from baseline KPIs and scenario assumptions for routing, SLA thresholds, operator capacity, category cleanup, AI assistance, handoff reduction, and backlog improvement decisions.

References:
- `references/digital-twin-light.md`

Scripts:
- `scripts/run_digital_twin_light.py`

### `topdesk-enablement`

Create training, demos, onboarding, quick-reference material, role-based guides, adoption plans, and enablement content for TOPdesk apps, Power BI reports, integrations, workflows, and AI/KI features.

References:
- `references/training-demo.md`

### `topdesk-executive-narrative`

Generate management-ready TOPdesk executive narratives from decision-ready findings, readiness scorecards, drift findings, process-debt reports, AI adoption ledgers, automation risk cards, and proof-of-value outputs.

References:
- `references/executive-narrative.md`

Scripts:
- `scripts/build_executive_narrative.py`

### `topdesk-expert`

Expert guidance for TOPdesk helpdesk/service-management functionality, the database schema of a custom Topdesk app, Power BI reporting/analytics, and AI/KI features for TOPdesk data and workflows. Use when answering questions about TOPdesk modules, incidents, changes, assets, knowledge base, self-service portal, operators/persons, API behavior, integrations, reporting, OData/database tables, entity relationships, migrations, Power BI dashboards, semantic models, DAX, Power Query, KPI definitions, AI-assisted ticket classification, routing, summaries, response suggestions, knowledge article generation, semantic search, predictive insights, or when designing, querying, documenting, or validating the Topdesk app schema.

References:
- `references/ai-features.md`
- `references/ai-prompts-and-evals.md`
- `references/api-and-integrations.md`
- `references/architecture-operations.md`
- `references/artifact-checklists.md`
- `references/features.md`
- `references/glossary-data-dictionary.md`
- `references/installation-notes.md`
- `references/migration-rollout.md`
- `references/odata-mapping.md`
- `references/powerbi.md`
- `references/powerbi-advanced.md`
- `references/powerbi-build-maintain.md`
- `references/powerbi-kpi-catalog.md`
- `references/powerbi-model-review.md`
- `references/powerbi-recipes.md`
- `references/powerbi-report-spec-template.md`
- `references/powerbi-template-snippets.md`
- `references/schema.md`
- `references/schema-blueprint.md`
- `references/security-compliance.md`
- `references/skill-suite-usps.md`
- `references/testing-validation.md`
- `references/training-demo.md`
- `references/usage-examples.md`
- `references/usps-positioning.md`

Scripts:
- `scripts/generate_powerbi_pack.py`
- `scripts/parse_odata_metadata.py`
- `scripts/profile_topdesk_export.py`

### `topdesk-handbook`

Create, update, and tailor complete handbook sets for TOPdesk solutions. Use for admin handbooks, operator manuals, Power BI user/developer guides, AI/KI governance manuals, integration manuals, operations/runbook manuals, schema/data-model documentation, rollout guides, training material, executive handbooks, and documentation indexes.

References:
- `references/admin-handbook.md`
- `references/ai-governance-handbook.md`
- `references/executive-handbook.md`
- `references/integration-handbook.md`
- `references/operations-handbook.md`
- `references/operator-handbook.md`
- `references/powerbi-handbook.md`
- `references/rollout-handbook.md`
- `references/schema-handbook.md`
- `references/training-handbook.md`

### `topdesk-integration`

TOPdesk API, OData, import/export, action sequence, and automation integration design. Use for API users, authentication, idempotent sync, incident/change/asset/person imports, payload mapping, error handling, retries, reconciliation, observability, action sequences, and integration runbooks.

References:
- `references/api-and-integrations.md`
- `references/architecture-operations.md`
- `references/incident-lifecycle-ingestion.md`
- `references/odata-mapping.md`
- `references/testing-validation.md`

Scripts:
- `scripts/sync_incident_lifecycle.py`

### `topdesk-knowledge`

TOPdesk Knowledge Management design and optimization. Use for knowledge article lifecycle, review workflows, article quality, incident-to-knowledge conversion, deflection, SSP knowledge, RAG source quality, semantic search sources, and knowledge KPIs.

References:
- `references/knowledge-management.md`

### `topdesk-major-incidents`

Major incident management for TOPdesk. Use for major incident detection, duplicate clustering, escalation, communication cadence, war-room workflows, linked child incidents, service impact, workaround tracking, resolution, postmortems, knowledge updates, and major incident KPIs.

References:
- `references/major-incident-management.md`

### `topdesk-migration`

Plan and validate TOPdesk-related migrations and rollouts. Use for data migration, cutover, historical backfill, legacy report replacement, OData/export migration, reference-data mapping, rollout planning, adoption, exception reports, reconciliation, and migration acceptance criteria.

References:
- `references/migration-rollout.md`

### `topdesk-odata`

Discover, parse, map, and validate TOPdesk OData/API schemas and exports. Use for TOPdesk OData $metadata, entity sets, field catalogs, navigation properties, API payload mapping, CSV export profiling, tenant-specific schema discovery, Power BI source mapping, integration reconciliation, and data-quality analysis.

References:
- `references/api-and-integrations.md`
- `references/artifact-checklists.md`
- `references/odata-mapping.md`

Scripts:
- `scripts/generate_data_quality_findings.py`
- `scripts/generate_field_catalog.py`
- `scripts/parse_odata_metadata.py`
- `scripts/profile_topdesk_export.py`

### `topdesk-operations`

Architecture, deployment, monitoring, runbooks, backup, recovery, refresh, and operational readiness for TOPdesk apps, integrations, Power BI datasets, and AI/KI services. Use for environment planning, release checklists, failed sync runbooks, Power BI refresh failures, AI disable switches, alerting, credentials, and installation/update notes.

References:
- `references/architecture-operations.md`
- `references/installation-notes.md`
- `references/security-compliance.md`

Assets:
- `assets/runbook-template.md`

### `topdesk-powerbi`

Build, review, and validate Power BI reporting for TOPdesk data. Use for TOPdesk dashboards, semantic models, DAX measures, Power Query/OData extraction, row-level security, KPI definitions, report pages, reconciliation against TOPdesk selections/exports, refresh design, and BI data-quality checks.

References:
- `references/glossary-data-dictionary.md`
- `references/powerbi.md`
- `references/powerbi-advanced.md`
- `references/powerbi-build-maintain.md`
- `references/powerbi-kpi-catalog.md`
- `references/powerbi-model-review.md`
- `references/powerbi-recipes.md`
- `references/powerbi-report-spec-template.md`
- `references/powerbi-template-snippets.md`
- `references/testing-validation.md`

Scripts:
- `scripts/build_demo_powerbi_report_pack.py`
- `scripts/build_topdesk_pbir_report.py`
- `scripts/generate_powerbi_pack.py`
- `scripts/new_tabular_editor_datatable_script.py`
- `scripts/validate_topdesk_pbir_report.py`

Assets:
- `assets/topdesk-core-measures.dax`
- `assets/topdesk-lifecycle-powerquery.pq`
- `assets/topdesk-odata-functions.pq`

### `topdesk-powerbi-dax`

Use when creating, reviewing, or standardizing Power BI DAX measures for TOPdesk incidents, SLAs, backlog, routing, operators, branches, AI governance, adoption, quality, cost, risk, and executive service-management dashboards.

Scripts:
- `scripts/new_dax_measure_pack.py`

Assets:
- `assets/topdesk-core-measures.dax`

### `topdesk-powerbi-modelling`

Design, review, and harden Power BI semantic models for TOPdesk data. Use for star schemas, fact/dimension grain, relationships, DAX measure catalogs, calculation groups, field parameters, RLS/OLS, incremental refresh, aggregation tables, reconciliation, tenant mapping, and model documentation for TOPdesk incidents, changes, assets, knowledge, SLAs, operators, branches, and AI features.

References:
- `references/model-patterns.md`
- `references/topdesk-model-catalog.md`

Scripts:
- `scripts/new_semantic_model_spec.py`

Assets:
- `assets/measure-catalog-template.csv`
- `assets/semantic-model-spec-template.md`

### `topdesk-powershell`

Advanced PowerShell automation for TOPdesk delivery and operations. Use for writing, reviewing, hardening, testing, or packaging PowerShell scripts that work with TOPdesk APIs, OData exports, CSV/JSON artifacts, tenant mapping, Power BI refresh operations, migration batches, runbooks, Windows scheduled tasks, CI scripts, validation gates, and safe local automation.

References:
- `references/powershell-patterns.md`
- `references/topdesk-powershell-recipes.md`

Scripts:
- `scripts/Test-TopdeskPowerShellScript.ps1`

Assets:
- `assets/topdesk-script-template.ps1`

### `topdesk-process-debt`

Analyze TOPdesk lifecycle, incident, SLA, status-transition, assignment-transition, and reopen evidence for process debt such as handoff loops, waiting zones, stale ownership, long runners, category-routing waste, and improvement backlog candidates.

References:
- `references/process-debt.md`

Scripts:
- `scripts/analyze_process_debt.py`

### `topdesk-project-delivery`

Delivery planning for TOPdesk projects. Use for epics, user stories, acceptance criteria, roadmaps, milestones, estimates, dependencies, risks, project governance, delivery streams, and implementation backlogs for TOPdesk apps, Power BI, OData/API, AI/KI, workflow, migration, and enablement work.

References:
- `references/delivery-planning.md`

### `topdesk-proof-of-value`

Build TOPdesk proof-of-value sprint packs for AI, Power BI, OData/API, data quality, and service-management improvements. Use for PoV scope, inputs, outputs, demo storyline, acceptance criteria, ROI assumptions, Power BI proof dashboards, KPI baselines, implementation plan, stakeholder messaging, and go/no-go decision material.

References:
- `references/proof-of-value-sprint.md`
- `references/roi-and-powerbi-proof.md`

Scripts:
- `scripts/new_pov_pack.py`

Assets:
- `assets/pov-powerbi-measures.dax`
- `assets/proof-of-value-plan-template.md`
- `assets/roi-calculator-template.csv`

### `topdesk-python`

Advanced Python automation for TOPdesk data, APIs, OData, reporting, migration, testing, and delivery tooling. Use for writing, reviewing, hardening, testing, or packaging Python scripts that parse TOPdesk OData metadata, profile CSV/Excel exports, call TOPdesk REST APIs, generate field catalogs, create data-quality findings, build Power BI/reporting artifacts, run migration checks, or provide CLI utilities.

References:
- `references/python-patterns.md`
- `references/topdesk-python-recipes.md`

Scripts:
- `scripts/validate_topdesk_python.py`

Assets:
- `assets/topdesk_cli_template.py`

### `topdesk-query-powerbi`

Translate TOPdesk business questions into tenant-safe OData filters, SQL/reporting-view queries, Power Query extraction plans, DAX measure definitions, validation checks, and Power BI report requirements. Use when combining TOPdesk queries with Power BI modelling, KPI semantics, reconciliation, data-quality checks, or report implementation tasks.

References:
- `references/query-to-powerbi.md`
- `references/topdesk-query-examples.md`

Scripts:
- `scripts/new_query_powerbi_spec.py`

Assets:
- `assets/query-powerbi-spec-template.md`

### `topdesk-readiness-scoring`

Score TOPdesk reporting, AI/KI, data trust, automation, security/privacy, tenant mapping, and operations readiness from evidence checklists, proof-of-value inputs, production gates, or project intake artifacts.

References:
- `references/readiness-scoring.md`

Scripts:
- `scripts/score_readiness.py`

### `topdesk-report-factory`

Generate TOPdesk report implementation packs. Use for Power BI report specifications, semantic model plans, DAX measure backlogs, page and visual backlogs, RLS design, refresh plans, reconciliation checks, data-quality checks, and implementation user stories.

References:
- `references/report-factory.md`

### `topdesk-roi-business-case`

ROI and business-case modeling for TOPdesk initiatives. Use for benefit models, executive cases, value hypotheses, KPI baselines, time-saved calculations, SLA/reassignment/reporting savings, AI value, Power BI value, integration value, assumptions, risks, and success metrics.

References:
- `references/roi-business-case.md`

### `topdesk-schema`

Design, review, and validate database schemas for TOPdesk-like service-management apps. Use for incident/change/asset/person/operator/branch schemas, TOPdesk external IDs, relationships, constraints, indexes, migrations, audit/history tables, SLA tables, AI suggestion tables, ERDs, reporting views, and schema-to-Power-BI preparation.

References:
- `references/glossary-data-dictionary.md`
- `references/schema.md`
- `references/schema-blueprint.md`
- `references/testing-validation.md`

Assets:
- `assets/reporting-views-template.sql`

### `topdesk-security`

Security, privacy, compliance, and governance for TOPdesk apps, integrations, Power BI reports, and AI/KI features. Use for DSGVO/GDPR, PII, branch/customer permissions, operator roles, audit logging, secrets, API users, row-level security, retention, AI governance, and safe automation controls.

References:
- `references/architecture-operations.md`
- `references/security-compliance.md`
- `references/testing-validation.md`

### `topdesk-service-intelligence-runtime`

Operate the TOPdesk Service Intelligence workflow with connector checks, analyzer orchestration, run history, governance gates, and HTML/Markdown readouts.

References:
- `references/runtime-operating-model.md`

Scripts:
- `scripts/Register-ServiceIntelligenceSchedule.ps1`
- `scripts/run_service_intelligence.py`
- `scripts/service_intelligence_server.py`
- `scripts/topdesk_live_connector.py`
- `scripts/topdesk_secret_store.py`

Assets:
- `assets/runtime-config.example.json`

### `topdesk-sla-optimizer`

Use when analyzing TOPdesk incident SLA health, target dates, backlog, overdue work, priority coverage, routing quality, operator-group workload, ageing buckets, operational risk, and service improvement actions from REST snapshots or exports.

Scripts:
- `scripts/analyze_sla_backlog.py`

### `topdesk-template-pack`

Reusable templates for TOPdesk delivery. Use for SQL view templates, DAX templates, Power Query templates, AI prompt/JSON schemas, test templates, runbooks, discovery questionnaires, proposal outlines, workshop agendas, user stories, acceptance criteria, and project documentation templates.

References:
- `references/template-pack.md`

Assets:
- `assets/proposal-outline.md`
- `assets/user-story-template.md`

### `topdesk-tenant-drift`

Compare TOPdesk tenant field catalogs, OData/API exports, option sets, categories, statuses, priorities, operator groups, and KPI dependency maps to detect drift risks for Power BI, AI/KI, automations, security, and operations.

References:
- `references/tenant-drift.md`

Scripts:
- `scripts/compare_tenant_drift.py`

### `topdesk-tenant-mapping`

Tenant-specific TOPdesk field and model mapping. Use for OData metadata, API samples, CSV exports, UI labels, category/status/priority exports, entity inventories, field catalogs, local schema mapping, Power BI fact/dimension mapping, RLS/security mapping, and tenant-specific data-quality gaps.

References:
- `references/tenant-mapping.md`

Scripts:
- `scripts/profile_topdesk_rest.py`

### `topdesk-testing`

Test planning and validation for TOPdesk workflows, schemas, integrations, Power BI reports, and AI/KI features. Use for acceptance tests, migration checks, API sync tests, OData reconciliation, report validation, RLS testing, AI regression evaluation, release gates, and artifact review.

References:
- `references/artifact-checklists.md`
- `references/testing-validation.md`

Assets:
- `assets/test-case-template.md`

### `topdesk-usp-battlecards`

Create TOPdesk USP packs, persona messaging, competitive battlecards, demo storylines, executive one-pagers, before/after narratives, risk-to-value matrices, offer packaging, case-study templates, and Power BI/AI value propositions. Use when positioning TOPdesk AI, Power BI, OData/API, data quality, governance, workflow, or full skill-suite offerings.

References:
- `references/demo-storylines.md`
- `references/usp-battlecards.md`

Scripts:
- `scripts/new_battlecard.py`

Assets:
- `assets/battlecard-template.md`
- `assets/executive-one-pager-template.md`
- `assets/risk-to-value-matrix.csv`

### `topdesk-usps`

Create USPs, positioning, stakeholder value propositions, pitch text, business cases, feature-benefit maps, differentiators, roadmap messaging, and executive/operator/application-manager messaging for TOPdesk apps, Power BI reporting, OData/API integrations, and AI service-management features.

References:
- `references/discovery-and-sales.md`
- `references/features.md`
- `references/glossary-data-dictionary.md`
- `references/skill-suite-usps.md`
- `references/usps-positioning.md`

### `topdesk-visual-design`

Design Power BI report pages and dashboard UX for TOPdesk service-management analytics. Use for visual hierarchy, page layouts, KPI cards, trend charts, matrix/table design, drill-through, tooltip pages, filters/slicers, color semantics, accessibility, executive/operator/application-manager views, incident/change/asset/knowledge dashboards, and report storytelling.

References:
- `references/page-wireframes.md`
- `references/report-design-patterns.md`

Scripts:
- `scripts/new_report_page_spec.py`

Assets:
- `assets/report-page-spec-template.md`
- `assets/topdesk-report-theme.json`

### `topdesk-workflows`

TOPdesk workflow and Self-Service Portal design for incidents, changes, assets, knowledge, categories, forms, routing, SLAs, notifications, approvals, and operator/end-user processes. Use for SSP forms, incident intake, change templates, category trees, assignment rules, SLA handling, knowledge workflows, acceptance criteria, and workflow testing.

References:
- `references/features.md`
- `references/glossary-data-dictionary.md`
- `references/testing-validation.md`

