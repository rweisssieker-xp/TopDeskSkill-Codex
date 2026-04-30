# Relational Schema Blueprint for a Topdesk App

Use this file when the user wants a concrete database model, ERD, migration plan, SQL tables, indexes, constraints, or reporting views. Adapt names and types to the target database and ORM.

## Blueprint Rules

- Keep `id` as the local primary key and `topdesk_id` / `topdesk_number` as external references.
- Use append-only history for status, assignment, SLA, audit, integration, and AI suggestions.
- Model dynamic asset fields through metadata/value tables or typed reporting views.
- Build BI on stable views, not on raw operational tables.
- Add `created_at`, `updated_at`, `created_by`, `updated_by`, and `deleted_at` where operationally useful.

## Core SQL Skeleton

```sql
create table branches (
  id uuid primary key,
  topdesk_id text unique,
  name text not null,
  code text,
  parent_branch_id uuid references branches(id),
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table persons (
  id uuid primary key,
  topdesk_id text unique,
  employee_number text,
  display_name text not null,
  email text,
  phone text,
  branch_id uuid references branches(id),
  department text,
  location text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table operator_groups (
  id uuid primary key,
  topdesk_id text unique,
  name text not null,
  is_active boolean not null default true
);

create table operators (
  id uuid primary key,
  topdesk_id text unique,
  person_id uuid references persons(id),
  display_name text not null,
  email text,
  is_active boolean not null default true
);

create table operator_group_members (
  operator_id uuid not null references operators(id),
  operator_group_id uuid not null references operator_groups(id),
  valid_from timestamptz not null default now(),
  valid_to timestamptz,
  primary key (operator_id, operator_group_id, valid_from)
);

create table categories (
  id uuid primary key,
  topdesk_id text,
  module text not null,
  name text not null,
  parent_category_id uuid references categories(id),
  is_active boolean not null default true,
  unique (module, topdesk_id)
);

create table statuses (
  id uuid primary key,
  topdesk_id text,
  module text not null,
  name text not null,
  status_group text,
  is_closed boolean not null default false,
  is_cancelled boolean not null default false,
  sort_order int,
  unique (module, topdesk_id)
);

create table priorities (
  id uuid primary key,
  topdesk_id text,
  name text not null,
  rank int not null,
  response_target_minutes int,
  resolution_target_minutes int,
  unique (topdesk_id)
);
```

## Incident Tables

```sql
create table incidents (
  id uuid primary key,
  topdesk_id text unique,
  topdesk_number text unique,
  source_system text not null default 'topdesk',
  source_channel text,
  brief_description text not null,
  request_text text,
  caller_person_id uuid references persons(id),
  branch_id uuid references branches(id),
  category_id uuid references categories(id),
  priority_id uuid references priorities(id),
  status_id uuid references statuses(id),
  assigned_operator_id uuid references operators(id),
  assigned_group_id uuid references operator_groups(id),
  impact text,
  urgency text,
  created_at timestamptz not null,
  modified_at timestamptz,
  target_at timestamptz,
  first_response_at timestamptz,
  resolved_at timestamptz,
  closed_at timestamptz,
  is_closed boolean not null default false,
  is_reopened boolean not null default false,
  reopen_count int not null default 0,
  sla_breached boolean,
  deleted_at timestamptz
);

create index ix_incidents_created_at on incidents(created_at);
create index ix_incidents_status_group on incidents(status_id, assigned_group_id);
create index ix_incidents_branch_category on incidents(branch_id, category_id);
create index ix_incidents_target_open on incidents(target_at) where is_closed = false;

create table incident_actions (
  id uuid primary key,
  incident_id uuid not null references incidents(id),
  topdesk_id text,
  action_type text not null,
  body text,
  is_public boolean not null default false,
  actor_operator_id uuid references operators(id),
  actor_person_id uuid references persons(id),
  time_spent_minutes int,
  action_at timestamptz not null,
  created_at timestamptz not null default now()
);

create table incident_status_history (
  id uuid primary key,
  incident_id uuid not null references incidents(id),
  from_status_id uuid references statuses(id),
  to_status_id uuid not null references statuses(id),
  changed_by_operator_id uuid references operators(id),
  changed_at timestamptz not null,
  reason text
);

create table incident_assignment_history (
  id uuid primary key,
  incident_id uuid not null references incidents(id),
  from_group_id uuid references operator_groups(id),
  to_group_id uuid references operator_groups(id),
  from_operator_id uuid references operators(id),
  to_operator_id uuid references operators(id),
  changed_by_operator_id uuid references operators(id),
  changed_at timestamptz not null,
  reason text
);
```

## Change, Asset, Knowledge, Attachment

```sql
create table changes (
  id uuid primary key,
  topdesk_id text unique,
  topdesk_number text unique,
  title text not null,
  requester_person_id uuid references persons(id),
  branch_id uuid references branches(id),
  coordinator_operator_id uuid references operators(id),
  status_id uuid references statuses(id),
  change_type text,
  risk_level text,
  impact text,
  planned_start_at timestamptz,
  planned_end_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null,
  modified_at timestamptz
);

create table change_activities (
  id uuid primary key,
  change_id uuid not null references changes(id),
  title text not null,
  activity_type text,
  sequence_no int,
  owner_operator_id uuid references operators(id),
  owner_group_id uuid references operator_groups(id),
  status_id uuid references statuses(id),
  due_at timestamptz,
  completed_at timestamptz
);

create table asset_types (
  id uuid primary key,
  topdesk_id text unique,
  name text not null
);

create table assets (
  id uuid primary key,
  topdesk_id text unique,
  asset_number text,
  asset_type_id uuid references asset_types(id),
  name text not null,
  status text,
  owner_person_id uuid references persons(id),
  branch_id uuid references branches(id),
  location text,
  supplier text,
  serial_number text,
  lifecycle_start_at date,
  lifecycle_end_at date,
  modified_at timestamptz
);

create table asset_field_values (
  asset_id uuid not null references assets(id),
  field_name text not null,
  field_type text not null,
  value_text text,
  value_number numeric,
  value_date date,
  value_boolean boolean,
  primary key (asset_id, field_name)
);

create table asset_relations (
  id uuid primary key,
  from_asset_id uuid not null references assets(id),
  to_asset_id uuid references assets(id),
  relation_type text not null,
  related_entity_type text,
  related_entity_id uuid,
  valid_from timestamptz,
  valid_to timestamptz
);

create table knowledge_items (
  id uuid primary key,
  topdesk_id text unique,
  title text not null,
  summary text,
  body text,
  category_id uuid references categories(id),
  owner_operator_id uuid references operators(id),
  visibility text not null,
  status text not null,
  language_code text,
  published_at timestamptz,
  review_at timestamptz,
  modified_at timestamptz
);

create table attachments (
  id uuid primary key,
  topdesk_id text,
  entity_type text not null,
  entity_id uuid not null,
  file_name text not null,
  content_type text,
  file_size_bytes bigint,
  storage_uri text not null,
  uploaded_by_operator_id uuid references operators(id),
  uploaded_at timestamptz not null
);
```

## SLA, Audit, Integration, AI

```sql
create table service_levels (
  id uuid primary key,
  name text not null,
  branch_id uuid references branches(id),
  category_id uuid references categories(id),
  priority_id uuid references priorities(id),
  response_target_minutes int,
  resolution_target_minutes int,
  calendar_name text,
  is_active boolean not null default true
);

create table incident_sla_events (
  id uuid primary key,
  incident_id uuid not null references incidents(id),
  event_type text not null,
  event_at timestamptz not null,
  target_at timestamptz,
  breached boolean,
  details jsonb
);

create table audit_events (
  id uuid primary key,
  entity_type text not null,
  entity_id uuid not null,
  action text not null,
  actor_type text not null,
  actor_id uuid,
  occurred_at timestamptz not null default now(),
  source text,
  before_json jsonb,
  after_json jsonb
);

create table integration_runs (
  id uuid primary key,
  source_system text not null,
  run_type text not null,
  started_at timestamptz not null,
  finished_at timestamptz,
  status text not null,
  records_read int default 0,
  records_written int default 0,
  records_failed int default 0,
  error_summary text
);

create table ai_suggestions (
  id uuid primary key,
  entity_type text not null,
  entity_id uuid not null,
  suggestion_type text not null,
  suggested_value jsonb not null,
  confidence numeric(5,4),
  explanation text,
  model_name text,
  prompt_version text,
  status text not null default 'pending',
  created_at timestamptz not null default now()
);
```

## Reporting Views

```sql
create view vw_incident_fact as
select
  i.id as incident_key,
  i.topdesk_id,
  i.topdesk_number,
  i.source_channel,
  i.created_at,
  i.target_at,
  i.first_response_at,
  i.resolved_at,
  i.closed_at,
  i.is_closed,
  i.reopen_count,
  i.sla_breached,
  i.caller_person_id,
  i.branch_id,
  i.category_id,
  i.priority_id,
  i.status_id,
  i.assigned_group_id,
  i.assigned_operator_id,
  extract(epoch from (i.closed_at - i.created_at)) / 3600.0 as resolution_hours
from incidents i
where i.deleted_at is null;

create view vw_incident_status_transition_fact as
select
  h.id as transition_key,
  h.incident_id as incident_key,
  h.from_status_id,
  h.to_status_id,
  h.changed_at,
  lead(h.changed_at) over (partition by h.incident_id order by h.changed_at) as next_changed_at
from incident_status_history h;

create view vw_asset_dimension as
select
  a.id as asset_key,
  a.topdesk_id,
  a.asset_number,
  a.name,
  at.name as asset_type,
  a.status,
  a.owner_person_id,
  a.branch_id,
  a.location,
  a.supplier
from assets a
left join asset_types at on at.id = a.asset_type_id;
```

## ERD Summary

- `branches` -> `persons`, `assets`, `incidents`, `changes`
- `persons` -> caller/requester/owner relationships
- `operators` + `operator_groups` -> assignment and ownership
- `categories`, `statuses`, `priorities` -> module reference dimensions
- `incidents` -> actions, status history, assignment history, SLA events, attachments, AI suggestions
- `changes` -> activities, approvals, asset/incident links
- `assets` -> dynamic field values and typed relations
- `knowledge_items` -> categories, visibility, incident links, AI retrieval chunks
