# Forward-Test Prompts

Use these prompts to test whether each skill gives useful, concrete outputs. Run in a fresh context when possible.

## Core

### topdesk-expert

```text
Use $topdesk-expert to design an end-to-end TOPdesk incident analytics and AI-assist solution. Include schema, OData mapping, Power BI pages, AI suggestions, security, tests, and rollout.
```

Expected: cross-domain plan with references to schema, OData, Power BI, AI, security, testing, and migration.

## Power BI

### topdesk-powerbi

```text
Use $topdesk-powerbi to create a Power BI report specification for TOPdesk incident SLA reporting. Include fact/dimension model, DAX measures, RLS, refresh, report pages, and reconciliation checks.
```

Expected: report spec, DAX ideas, RLS and validation.

## OData

### topdesk-odata

```text
Use $topdesk-odata to explain how to process a TOPdesk OData $metadata file and CSV export into a field catalog, Power BI mapping, and data-quality findings.
```

Expected: script usage, outputs, mapping process.

## AI/KI

### topdesk-ai

```text
Use $topdesk-ai to design a suggest-only AI ticket classification and routing feature for TOPdesk. Include input fields, JSON output schema, confidence thresholds, human review, audit, and evaluation metrics.
```

Expected: use case, prompt/output schema, governance, metrics.

## Schema

### topdesk-schema

```text
Use $topdesk-schema to design a database schema for TOPdesk incidents, actions, status history, assignment history, SLA events, and Power BI reporting views.
```

Expected: tables, relationships, indexes, reporting views, migration tests.

## Security

### topdesk-security

```text
Use $topdesk-security to review a TOPdesk AI response-suggestion feature for PII, internal notes, RLS, audit logging, and DSGVO/GDPR risks.
```

Expected: risks, controls, audit, tests.

## Testing

### topdesk-testing

```text
Use $topdesk-testing to create an acceptance and regression test plan for a TOPdesk Power BI dashboard and OData integration.
```

Expected: test cases, reconciliation, RLS, refresh, integration checks.

## Integration

### topdesk-integration

```text
Use $topdesk-integration to design an idempotent sync from TOPdesk incidents into a local reporting database. Include identity mapping, payload mapping, retries, dead-letter handling, and reconciliation.
```

Expected: integration design with errors and observability.

## Operations

### topdesk-operations

```text
Use $topdesk-operations to write a runbook for a failed TOPdesk-to-Power BI refresh caused by OData schema drift.
```

Expected: trigger, detection, diagnosis, remediation, rollback/forward fix.

## Workflows

### topdesk-workflows

```text
Use $topdesk-workflows to design an SSP form and incident workflow for laptop replacement requests. Include fields, routing, SLA, notifications, and acceptance tests.
```

Expected: workflow with form fields, routing, SLA, tests.

## USPs

### topdesk-usps

```text
Use $topdesk-usps to create executive USPs and a business case for a TOPdesk Power BI and AI-assist initiative.
```

Expected: stakeholder value, metrics, objection handling.

## Migration

### topdesk-migration

```text
Use $topdesk-migration to plan migration from CSV-based TOPdesk reporting to a governed OData and Power BI semantic model.
```

Expected: phases, cutover, validation, risks.

## Enablement

### topdesk-enablement

```text
Use $topdesk-enablement to create a 60-minute training plan for service desk operators using AI suggestions and the new Power BI dashboard.
```

Expected: agenda, role-specific guidance, quick reference.

## Knowledge

### topdesk-knowledge

```text
Use $topdesk-knowledge to design a knowledge article lifecycle and deflection KPI model for repeated password reset incidents.
```

Expected: lifecycle, quality checklist, KPIs.

## Assets

### topdesk-assets

```text
Use $topdesk-assets to design asset templates and reporting for laptops, monitors, and mobile phones, including dynamic fields and incident links.
```

Expected: asset model, relations, data quality, KPIs.

## Changes

### topdesk-changes

```text
Use $topdesk-changes to design a standard change workflow for employee onboarding with activities, approvals, linked assets, and KPIs.
```

Expected: change template, activities, approvals, tests.

## Action Sequences

### topdesk-action-sequences

```text
Use $topdesk-action-sequences to design a safe action sequence that notifies Teams when a VIP incident is near SLA breach.
```

Expected: trigger, preconditions, payload, retries, audit, monitoring.

## Data Quality

### topdesk-data-quality

```text
Use $topdesk-data-quality to define checks and a Power BI data-quality page for missing branch/category/caller, duplicate persons, orphan assets, and unknown dimensions.
```

Expected: checks, severity, fixes, BI page.

## Project Delivery

### topdesk-project-delivery

```text
Use $topdesk-project-delivery to create a phased delivery roadmap, epics, user stories, estimates, risks, and acceptance criteria for a TOPdesk Power BI and AI-assist project.
```

Expected: roadmap, epics, stories, dependencies, acceptance criteria.

## Admin Config

### topdesk-admin-config

```text
Use $topdesk-admin-config to review and redesign TOPdesk categories, statuses, operator groups, SSP form fields, and configuration governance for incident intake.
```

Expected: admin configuration recommendations and governance checks.

## Major Incidents

### topdesk-major-incidents

```text
Use $topdesk-major-incidents to design a TOPdesk major incident workflow with detection, escalation, communications, linked incidents, and postmortem KPIs.
```

Expected: major incident lifecycle and communication cadence.

## Report Factory

### topdesk-report-factory

```text
Use $topdesk-report-factory to generate a complete implementation pack for a TOPdesk service desk operations dashboard.
```

Expected: report spec, model, DAX backlog, pages, RLS, validation.

## Tenant Mapping

### topdesk-tenant-mapping

```text
Use $topdesk-tenant-mapping to turn TOPdesk OData metadata and CSV exports into a verified field catalog, schema mapping, Power BI mapping, and unknowns list.
```

Expected: mapping outputs and validation method.

## ROI Business Case

### topdesk-roi-business-case

```text
Use $topdesk-roi-business-case to build an executive ROI model for reducing TOPdesk triage effort with AI classification and Power BI operational reporting.
```

Expected: formulas, assumptions, benefits, metrics, risks.

## Template Pack

### topdesk-template-pack

```text
Use $topdesk-template-pack to create a reusable proposal outline and user-story template for a TOPdesk reporting and AI project.
```

Expected: concise reusable templates.

## Handbook

### topdesk-handbook

```text
Use $topdesk-handbook to create a complete operator and Power BI handbook for a TOPdesk service desk analytics and AI-assist rollout.
```

Expected: role-specific handbook structure with procedures, checklists, governance, and maintenance notes.
