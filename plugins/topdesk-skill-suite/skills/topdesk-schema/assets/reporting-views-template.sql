-- TOPdesk reporting views template.
-- Adapt table and column names to the actual schema.

create or replace view vw_incident_fact as
select
  i.id as incident_key,
  i.topdesk_id,
  i.topdesk_number,
  i.created_at,
  i.modified_at,
  i.target_at,
  i.closed_at,
  i.is_closed,
  i.sla_breached,
  i.caller_person_id,
  i.branch_id,
  i.category_id,
  i.priority_id,
  i.status_id,
  i.assigned_group_id,
  i.assigned_operator_id
from incidents i
where i.deleted_at is null;

create or replace view vw_incident_status_transition_fact as
select
  h.id as transition_key,
  h.incident_id as incident_key,
  row_number() over (partition by h.incident_id order by h.changed_at) as status_sequence,
  h.from_status_id,
  h.to_status_id,
  h.changed_by_operator_id,
  h.changed_at as valid_from_at,
  coalesce(
    lead(h.changed_at) over (partition by h.incident_id order by h.changed_at),
    i.closed_at,
    now()
  ) as valid_to_at,
  extract(epoch from (
    coalesce(
      lead(h.changed_at) over (partition by h.incident_id order by h.changed_at),
      i.closed_at,
      now()
    ) - h.changed_at
  )) / 3600.0 as duration_hours
from incident_status_history h
join incidents i on i.id = h.incident_id
where i.deleted_at is null;

create or replace view vw_incident_assignment_transition_fact as
select
  h.id as transition_key,
  h.incident_id as incident_key,
  row_number() over (partition by h.incident_id order by h.changed_at) as assignment_sequence,
  h.from_group_id,
  h.to_group_id as operator_group_id,
  h.from_operator_id,
  h.to_operator_id as operator_id,
  h.changed_by_operator_id,
  h.changed_at as valid_from_at,
  coalesce(
    lead(h.changed_at) over (partition by h.incident_id order by h.changed_at),
    i.closed_at,
    now()
  ) as valid_to_at,
  extract(epoch from (
    coalesce(
      lead(h.changed_at) over (partition by h.incident_id order by h.changed_at),
      i.closed_at,
      now()
    ) - h.changed_at
  )) / 3600.0 as duration_hours
from incident_assignment_history h
join incidents i on i.id = h.incident_id
where i.deleted_at is null;

create or replace view vw_incident_daily_snapshot_fact as
select
  s.snapshot_date,
  s.incident_id as incident_key,
  s.topdesk_id,
  s.topdesk_number,
  s.status_id,
  s.assigned_group_id,
  s.assigned_operator_id,
  s.priority_id,
  s.category_id,
  s.branch_id,
  s.created_at,
  s.modified_at,
  s.target_at,
  s.closed_at,
  s.is_closed,
  s.snapshot_loaded_at
from incident_daily_snapshots s;

create or replace view vw_branch_dimension as
select
  b.id as branch_key,
  b.topdesk_id,
  b.name as branch_name,
  b.is_active
from branches b;
