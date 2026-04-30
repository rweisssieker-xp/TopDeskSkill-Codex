# TOPdesk Skill Index

This folder contains a TOPdesk-focused skill suite. Use `topdesk-expert` for broad cross-domain work and the focused skills when the task is narrow.

## Core Skill

| Skill | Use for |
| --- | --- |
| `topdesk-expert` | Broad TOPdesk work across features, schema, OData/API, Power BI, AI/KI, security, operations, migration, enablement, and USPs. |

## Focused Skills

| Skill | Use for |
| --- | --- |
| `topdesk-powerbi` | Power BI semantic models, DAX, Power Query, RLS, KPI catalogs, report specs, model review, refresh, reconciliation. |
| `topdesk-ai` | AI/KI classification, routing, summaries, response drafts, RAG, prompts, evaluations, governance. |
| `topdesk-odata` | OData `$metadata`, API field mapping, CSV export profiling, field catalogs, tenant schema discovery. |
| `topdesk-schema` | Database schema, ERDs, incidents/actions/history, assets, changes, constraints, indexes, reporting views. |
| `topdesk-security` | DSGVO/GDPR, PII, permissions, RLS, audit, secrets, AI governance, safe automation. |
| `topdesk-testing` | Acceptance tests, migration checks, integration validation, Power BI reconciliation, AI regression. |
| `topdesk-integration` | API syncs, imports, action sequences, idempotency, retries, observability, reconciliation. |
| `topdesk-operations` | Architecture, deployment, monitoring, backups, refresh failures, runbooks, installation notes. |
| `topdesk-workflows` | SSP forms, incident/change workflows, categories, routing, SLAs, notifications, acceptance criteria. |
| `topdesk-usps` | USPs, positioning, pitch text, business case, ROI, discovery questions, stakeholder messaging. |
| `topdesk-migration` | Data migration, cutover, backfill, rollout, adoption, legacy report replacement. |
| `topdesk-enablement` | Training, demos, onboarding, quick-reference cards, role-based guides, adoption metrics. |
| `topdesk-knowledge` | Knowledge base lifecycle, deflection, article quality, RAG source governance, knowledge KPIs. |
| `topdesk-assets` | Asset templates, dynamic fields, relations, lifecycle, incidents/changes linked to assets, asset KPIs. |
| `topdesk-changes` | Change templates, activities, approvals, risk/impact, scheduling, audit, change KPIs. |
| `topdesk-action-sequences` | Action Sequences, webhooks, API calls, idempotency, retries, error handling, monitoring. |
| `topdesk-data-quality` | Missing fields, duplicates, orphan links, unknown dimensions, mapping gaps, BI data-quality pages. |
| `topdesk-project-delivery` | Epics, user stories, roadmaps, estimates, milestones, dependencies, and delivery plans. |
| `topdesk-admin-config` | Categories, statuses, priorities, supporting files, branches, operators, SSP forms, templates, and governance. |
| `topdesk-major-incidents` | Major incident detection, escalation, communication, linked child incidents, postmortems, and KPIs. |
| `topdesk-report-factory` | Report specs, semantic model plans, DAX backlogs, page backlogs, RLS, refresh, and validation packs. |
| `topdesk-tenant-mapping` | Tenant-specific mappings from metadata, exports, samples, UI labels, schema, BI, RLS, and data quality. |
| `topdesk-roi-business-case` | ROI models, executive business cases, benefit baselines, assumptions, risks, and success metrics. |
| `topdesk-template-pack` | Reusable SQL, DAX, Power Query, prompt, runbook, proposal, workshop, and user-story templates. |

## Utility Scripts

`topdesk-odata/scripts`:

- `parse_odata_metadata.py`: OData `$metadata` XML to CSV catalogs.
- `profile_topdesk_export.py`: CSV export profiling.
- `generate_field_catalog.py`: CSV metadata catalogs to Markdown field catalog.
- `generate_data_quality_findings.py`: CSV profile to data-quality findings.

## Template Assets

- `topdesk-powerbi/assets/topdesk-core-measures.dax`
- `topdesk-powerbi/assets/topdesk-odata-functions.pq`
- `topdesk-schema/assets/reporting-views-template.sql`
- `topdesk-testing/assets/test-case-template.md`
- `topdesk-operations/assets/runbook-template.md`

## Recommended Invocation

- Broad ambiguous request: use `topdesk-expert`.
- Report/dashboard request: use `topdesk-powerbi`.
- Metadata/export mapping request: use `topdesk-odata`.
- AI feature request: use `topdesk-ai`.
- Database design request: use `topdesk-schema`.
- Governance/safety request: use `topdesk-security`.
- Test/release request: use `topdesk-testing`.
- Delivery/backlog request: use `topdesk-project-delivery`.
- Business-case request: use `topdesk-roi-business-case`.
- Tenant-specific mapping request: use `topdesk-tenant-mapping`.
