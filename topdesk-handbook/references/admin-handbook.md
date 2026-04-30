# Admin Handbook

Audience: TOPdesk application managers and platform owners.

## Scope

Configuration governance for categories, statuses, priorities, supporting files, operator groups, SSP forms, templates, knowledge visibility, asset templates, and change workflows.

## Responsibilities

- Own configuration quality.
- Maintain supporting files.
- Coordinate changes with reporting, security, and operations owners.
- Validate downstream impact on Power BI, integrations, and AI.

## Core Procedures

Category update:

1. Confirm business reason.
2. Check reporting and routing impact.
3. Avoid duplicates and ambiguous labels.
4. Update mapping documentation.
5. Validate Power BI dimensions and historical reporting.

SSP form change:

1. Define audience and request type.
2. Keep fields minimal.
3. Mark required fields deliberately.
4. Test routing, SLA, notifications, and reporting fields.
5. Communicate change to operators.

Operator group update:

1. Confirm owner and members.
2. Check active/inactive operators.
3. Validate assignment rules.
4. Validate RLS/reporting if group is used in Power BI.

## Checklist

- Categories are reportable.
- Statuses map to open/closed/cancelled.
- Supporting files have owners.
- Templates match real workflows.
- Configuration changes are tested before production.
