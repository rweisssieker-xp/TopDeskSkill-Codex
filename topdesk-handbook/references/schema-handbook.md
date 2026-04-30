# Schema Handbook

Audience: data architects, database engineers, and BI developers.

## Design Rules

- Keep local primary keys separate from TOPdesk IDs/numbers.
- Store current state on main records and history in append-only tables.
- Model many-to-many links with bridge tables.
- Use reporting views for Power BI.
- Store AI suggestions separately from operational facts.

## Core Entities

- Incidents.
- Incident actions.
- Status history.
- Assignment history.
- Persons.
- Operators.
- Operator groups.
- Branches.
- Categories.
- Priorities.
- Changes and activities.
- Assets and relations.
- Knowledge items.
- SLA events.
- Audit events.

## Migration Checklist

- Backfill required fields.
- Validate foreign keys.
- Preserve historical labels.
- Add indexes for reports.
- Reconcile counts.
- Test rollback or forward-fix.
