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

create or replace view vw_branch_dimension as
select
  b.id as branch_key,
  b.topdesk_id,
  b.name as branch_name,
  b.is_active
from branches b;
