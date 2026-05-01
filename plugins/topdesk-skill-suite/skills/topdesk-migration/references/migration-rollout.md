# Migration and Rollout

Use this file for TOPdesk app migrations, data migration, rollout planning, cutover, adoption, backfill, and legacy-report replacement.

## Migration Scope

Classify the migration:

- TOPdesk export/OData to local reporting database.
- Legacy helpdesk data into TOPdesk or a Topdesk app.
- Flat Power BI export to governed semantic model.
- Manual workflow to SSP/Change/Asset workflow.
- Suggest-only AI pilot to controlled production use.

## Discovery Checklist

- Source systems and owners.
- Entity scope: incidents, actions, persons, operators, branches, categories, changes, assets, knowledge, attachments.
- Historical date range.
- Required audit/history.
- PII and retention constraints.
- Target schema and reporting needs.
- Required reconciliation totals.
- Downtime or cutover constraints.

## Data Migration Plan

1. Inventory source fields and target fields.
2. Define identity mapping: local ID, TOPdesk ID, external ID, ticket/change number.
3. Map reference data first: branches, persons, operators, groups, categories, priorities, statuses.
4. Load facts after dimensions: incidents, actions, changes, assets, SLA events.
5. Load links and attachments after parent records.
6. Validate row counts, required fields, duplicates, orphan links, and date ranges.
7. Produce exception reports for manual cleanup.

## Cutover Plan

- Freeze or snapshot source data.
- Run final incremental sync.
- Validate totals and critical samples.
- Switch integrations/reports to new source.
- Keep rollback path for agreed period.
- Monitor failures and reconciliation deltas.
- Communicate known limitations and support channel.

## Adoption Plan

- Train operators on changed fields, routing, AI suggestions, and report interpretation.
- Provide application managers with mapping docs and runbooks.
- Provide management with KPI definitions and refresh expectations.
- Track adoption metrics: report usage, AI acceptance, override reasons, workflow errors, reopened tickets.

## Risk Register

| Risk | Mitigation |
| --- | --- |
| Field meaning differs from label | Verify with samples and TOPdesk admin |
| Missing external IDs | Create deterministic matching and exception queue |
| Historical categories changed | Preserve historical display labels |
| Power BI mismatch | Reconcile against TOPdesk selections/exports |
| PII in exports | Mask/minimize and restrict access |
| AI over-automation | Start suggest-only and audit all actions |

## Migration Acceptance Criteria

- Required entities loaded with agreed counts.
- Critical fields mapped and documented.
- Orphan records below agreed threshold or fully explained.
- Power BI KPIs reconcile within agreed tolerance.
- Security/RLS validated.
- Rollback or forward-fix plan documented.
- Business owner signs off on known gaps.
