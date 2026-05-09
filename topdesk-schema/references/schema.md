# Topdesk App Database Schema Reference

Use this file for database design, ERD review, migrations, SQL, OData/reporting, and schema documentation for TOPdesk data or a custom Topdesk app. Local code, migrations, database dumps, OData metadata, API payloads, and exports override this generic model.

For terminology and canonical entity names, load `glossary-data-dictionary.md`.

## Source-of-Truth Rules

- TOPdesk SaaS/internal product database tables are not a stable public contract. Do not claim exact internal TOPdesk table names unless the user provides a database schema, vendor export, or official schema artifact.
- For real TOPdesk tenants, treat OData `$metadata`, API schemas, export columns, and configured supporting files as the verifiable schema.
- For a custom Topdesk app, model the TOPdesk business concepts explicitly and store TOPdesk IDs/numbers as external identifiers.
- For BI/reporting, prefer curated database views or OData entities over direct transactional tables.
- For concrete SQL table definitions, indexes, constraints, and reporting views, load `schema-blueprint.md`.
- For TOPdesk OData/API field catalogs and tenant mapping, load `odata-mapping.md`.

## Schema Discovery Checklist

Search local projects in this order:

1. Migrations: `migrations`, `db/migrate`, `prisma/migrations`, `alembic`, `Flyway`, `Liquibase`.
2. ORM models: `schema.prisma`, `models`, `entities`, `DbContext`, `typeorm`, `sequelize`, `efcore`.
3. SQL/schema files: `*.sql`, `schema`, `database`, `ddl`.
4. API DTOs and serializers: incident/change/asset/person request and response models.
5. Seed/reference data: categories, statuses, priorities, branches, permissions.
6. Reports/OData/query code: dashboards, exports, BI models.

Use `rg -n "incident|call|change|activity|asset|object|person|operator|branch|category|priority|status|sla|knowledge|attachment|audit|external|topdesk|odata"` to locate likely schema files.

## Canonical Entity Map

Core helpdesk entities:

- `incidents`: ticket/call records; link to caller/person, operator/group, branch, category, priority, status, SLA/target date, source, and external TOPdesk ID.
- `incident_actions` or `ticket_comments`: chronological actions, operator notes, public replies, system events, time spent, visibility.
- `incident_status_history`: append-only state transitions, actor, timestamp, reason.
- `changes`: controlled workflows; link requester, coordinator/operator, template, risk, impact, status, planned dates, linked assets/incidents.
- `change_activities`: tasks/approvals/implementation steps with owner, due date, status, sequence, and dependencies.
- `assets`: physical/logical assets; type/template, status, owner/person, branch/location, supplier, serial/inventory fields, external ID.
- `asset_relations`: graph edges between assets, persons, branches, incidents, changes, or contracts.
- `knowledge_items`: article content, title, status, visibility, category, owner, review date, publication metadata.
- `attachments`: file metadata linked polymorphically or via link tables to incidents, changes, assets, and knowledge items.

## TOPdesk Domain Schema Map

Use these as canonical business entities even when actual table/OData names differ.

### Incident Management

Incident/call records normally need these field groups:

- Identity: internal ID, TOPdesk ID, incident number, source system, source channel.
- Request context: brief description, request text, entry type/source, caller/person, branch, department, location, contact details snapshot.
- Classification: category, subcategory, service, call type, impact, urgency, priority, object/asset links.
- Assignment: operator, operator group, supplier/escalation party, reassignment history.
- Lifecycle: current status, processing status, closed flag, resolved/closed timestamp, reopen count, cancellation flag.
- SLA/planning: target date, response target, on-hold/pause intervals, escalation marker, breached marker.
- Communication: public replies, internal actions, email notifications, attachments.
- Audit: created/modified timestamps, created by, modified by, status/assignment history.

Recommended local tables:

- `incidents`
- `incident_actions`
- `incident_status_history`
- `incident_assignment_history`
- `incident_daily_snapshots`
- `incident_asset_links`
- `incident_person_links`
- `incident_attachments`
- `incident_sla_events`

### Supporting Files

Supporting Files are reference/master data used across modules:

- `persons`: callers/end users/customers.
- `operators`: service desk and back-office users.
- `operator_groups`: teams/assignment groups.
- `branches`: customer organizations/sites; many TOPdesk records are branch-scoped.
- `departments`, `locations`, `rooms`: organizational and physical location hierarchy.
- `suppliers`: external suppliers/escalation parties.
- `categories`: module-specific classification tree.
- `priorities`, `impact`, `urgency`: prioritization and SLA inputs.
- `statuses`: lifecycle states per module.
- `entry_types` or `sources`: email, SSP, phone, monitoring, API, import.

Preserve display names for history/reporting, but relate facts by stable IDs.

### Change Management

Change records should support workflow and approvals:

- Identity: ID, TOPdesk ID, change number, template/type.
- Request: requester/person, branch, reason, scope, linked incident/problem/assets.
- Governance: coordinator, operator group, risk, impact, approval status.
- Planning: planned start/end, implementation window, fallback plan, evaluation date.
- Lifecycle: current phase/status, activities, approvals, implementation result.

Recommended local tables:

- `changes`
- `change_activities`
- `change_approvals`
- `change_status_history`
- `change_asset_links`
- `change_incident_links`

### Asset Management

Modern TOPdesk Asset Management is template/type driven. Avoid assuming a fixed column set for all asset types.

Recommended local design:

- `assets`: stable asset identity, type/template, status, owner, branch, location, supplier, lifecycle dates.
- `asset_types` or `asset_templates`: metadata for asset categories.
- `asset_fields`: template field definitions when dynamic fields exist.
- `asset_field_values`: typed field values for flexible schemas.
- `asset_relations`: typed many-to-many relations between assets, persons, branches, incidents, changes, contracts, or suppliers.
- `asset_snapshots`: optional BI/history table for lifecycle reporting.

Use fixed columns for universal fields and field-value tables or JSON only for type-specific fields. Prefer typed columns/views for BI-critical fields.

### Knowledge Management

Knowledge records normally need:

- Article identity, title, summary, body/content, language.
- Category/service/module links.
- Visibility: operator-only, SSP/public, branch/customer restrictions.
- Workflow: draft, reviewed, published, archived.
- Ownership: author, owner, reviewer, review date.
- Usage: linked incidents, helpfulness, search terms if available.

Recommended local tables:

- `knowledge_items`
- `knowledge_versions`
- `knowledge_categories`
- `knowledge_visibility_rules`
- `knowledge_incident_links`

### SLA and Service Levels

Separate SLA definitions from observed SLA events:

- `service_levels`: service/SLA definitions, priority/category/branch applicability, response/resolution targets.
- `sla_calendars`: business hours, holidays, timezone.
- `incident_sla_targets`: calculated target dates for each incident.
- `incident_sla_events`: pauses, resumes, breaches, escalations, recalculations.

For reporting, store both raw timestamps and calculated business-duration fields when possible.

### Audit, History, and Security

Use append-only history where operational accountability matters:

- `audit_events`: who changed what, before/after summary, timestamp, source.
- `status_history`: work-item lifecycle transitions.
- `assignment_history`: group/operator handoffs.
- `daily_snapshots`: scheduled point-in-time state for historical backlog and fallback aging when event history is incomplete.
- `integration_runs`: sync job status, counts, errors, correlation IDs.
- `permission_assignments`: local app access model. Do not assume it equals TOPdesk permissions.

Supporting/reference entities:

- `persons`: callers/end users; branch, department, contact data, login/SSP identifiers, active flag.
- `operators`: service users; person link if applicable, group membership, permission profile, active flag.
- `operator_groups`: assignment groups/teams.
- `branches`: customer/company/site hierarchy. In TOPdesk, many records are branch-scoped.
- `departments`, `locations`, `rooms`: organizational/location reference data.
- `categories` and `subcategories`: classification trees per module.
- `priorities`, `impact`, `urgency`: priority calculation or fixed priority lists.
- `statuses`: module-specific states and terminal flags.
- `sla_targets` or `service_levels`: target times, pauses, escalation thresholds.
- `permissions` and `roles`: app authorization; never assume TOPdesk operator permissions map 1:1 to local roles.
- `audit_events`: append-only record of security-sensitive and business-critical changes.

## Relationship Guidance

- One person can have many incidents and changes.
- One branch can have many persons, assets, locations, incidents, and changes.
- One incident usually has one current status, one caller, optional assigned operator, optional assigned group, many actions, many attachments, and many linked assets/persons.
- One change has many activities and approvals; activities may have separate status and owner.
- Asset relationships are often many-to-many and typed; model them with relation tables, not fixed columns.
- Categories are often hierarchical; use parent IDs or closure tables depending on reporting needs.
- Status history and audit events should be append-only even when the main record stores current status.
- Dynamic asset fields should be related through asset type/template metadata or exposed through typed reporting views.
- SLA targets are derived from incident/change attributes plus calendars; keep recalculation history if SLA compliance is audited.

## Field and Constraint Guidance

- Keep local primary keys separate from TOPdesk external IDs. Example: `id` plus `topdesk_id` or `topdesk_number`.
- Use unique constraints for external IDs per source system: `(source_system, external_id)`.
- Add indexes on common filters: status, assigned group, operator, caller, branch, category, target date, created date, closed date, external ID.
- Use nullable foreign keys only where the workflow allows missing data. Document why each nullable relationship exists.
- Track `created_at`, `updated_at`, `created_by`, `updated_by`, and optionally `deleted_at`.
- Store time zones deliberately for SLA and reporting fields.
- Avoid storing secrets or API tokens in operational tables; use a secret store or encrypted config.

## TOPdesk OData/API Schema Discovery

For real TOPdesk reporting or integration tasks:

1. Inspect the OData service document and `$metadata` for entity sets, navigation properties, key fields, and data types.
2. Pull a small sample per entity and compare fields with the UI/export labels.
3. Identify lookup/navigation fields for caller/person, branch, operator, operator group, category, status, priority, and asset references.
4. Confirm date semantics: creation date, modification date, target date, closure date, action date.
5. Check whether fields are localized display values, stable IDs, or nested objects.
6. Build mapping tables from OData/API names to report/model names.

Document mappings like this:

| Business concept | OData/API field | Local/model field | Key/display | Notes |
| --- | --- | --- | --- | --- |
| Incident ID | verified from metadata | `topdesk_id` | key | Stable integration identifier |
| Incident number | verified from metadata | `number` | display | Human reference |
| Caller | verified navigation/object | `caller_person_id` | key | Join to person dimension |
| Branch | verified navigation/object | `branch_id` | key | Used for security/reporting |
| Status | verified field/object | `status_id` | key/display | Preserve status history separately |

Never hard-code these names without checking the target tenant/schema.

## Reporting Views

Create stable views for BI/reporting so report logic does not depend on raw transactional structure:

- `vw_incident_fact`: one row per incident with current state and key dates.
- `vw_incident_action_fact`: one row per action/comment.
- `vw_incident_status_transition_fact`: one row per status transition with duration.
- `vw_incident_assignment_transition_fact`: one row per operator group/operator assignment interval with duration.
- `vw_incident_daily_snapshot_fact`: one row per incident per snapshot date for backlog-as-of and approximate aging.
- `vw_change_fact`: one row per change.
- `vw_change_activity_fact`: one row per activity/approval.
- `vw_asset_dimension`: current asset dimension with flattened BI fields.
- `vw_person_dimension`, `vw_operator_dimension`, `vw_branch_dimension`, `vw_category_dimension`, `vw_date_dimension`.

Views should expose stable column names, hide raw JSON/dynamic fields, and precompute difficult SLA/calendar fields where possible.

For concrete SQL examples of these views, load `schema-blueprint.md`.

## Reporting Query Pattern

For operational reports, join from the work item outward:

```sql
select
  i.number,
  i.status_id,
  s.name as status_name,
  p.display_name as caller_name,
  b.name as branch_name,
  og.name as assigned_group,
  i.created_at,
  i.target_at,
  i.closed_at
from incidents i
left join statuses s on s.id = i.status_id
left join persons p on p.id = i.caller_person_id
left join branches b on b.id = i.branch_id
left join operator_groups og on og.id = i.assigned_group_id
where i.created_at >= :from_date
  and i.created_at < :to_date;
```

Adapt names to the actual local schema.

## Migration Review Checklist

- Confirm backfill for new non-null columns.
- Confirm foreign-key behavior on delete/update.
- Confirm indexes for new dashboard/API filters.
- Confirm audit/history preservation for status or assignment changes.
- Confirm data import idempotency when syncing from TOPdesk.
- Confirm tests cover old records, missing optional relations, and permission-sensitive fields.
